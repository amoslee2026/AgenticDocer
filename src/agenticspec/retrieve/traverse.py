"""M05 refs 图遍历（**内部实现，无公开端点**——ADR-008）。

权威依据：

- `architecture_specification.md` §3 M05：`KIND_RULES`（方向/参与多跳/最大跳数）与
  `traverse(node_id, hops=1)` 契约、`TraversalHit` 返回类型；
- `functional_specification.md` REQ-M05-F01：跳数、去重保留最短路径、环截断、排序口径；
- `design_doc.md` §6.4「kind × 遍历方向 × 参与跳数」表——**本模块 `up`/`down`
  箭头的唯一出处**（见下「方向口径」）；
- `ADR-005`（关键词检索）/`ADR-008`（降级为内部接口）/`ADR-009`（`nodes` 分区）。

消费方：M-LR 导出（构造 LightRAG 图结构上下文，主要）、M09B 质量门（次要）。
**不得**被 M06/M07 装配为端点（ADR-008 边界表：「refs 图遍历（多跳）= 内部 M05」）。

方向口径
--------

`KIND_RULES[kind][0]` 取自 design_doc §6.4 的箭头（该表是方向语义的**唯一**书面出处；
arch/functional spec 只写「上游/下游/双向」，未定义箭头）：

======================  ==========  =========================================================
kind                    方向        含义（`src` = 携带 ref 的节点，`dst` = 被引用节点）
======================  ==========  =========================================================
``traces_to``           ``up``      dst→src：命中点在**被引用侧**，返回引用它的节点
``composes_from``       ``down``    src→dst：命中点在**引用侧**，返回它组成的节点
``see_also``            ``both``    两侧全覆盖（双向 1 跳）
``source_ref``          ``up``      `max_hops=0` → 任何跳数下都不参与（叶引用）
======================  ==========  =========================================================

跳数口径
--------

第 ``step`` 跳允许跟随的 kind = :func:`expandable_kinds`：``step <= max_hops`` 且
（``multi_hop`` 为真或 ``step == 1``）。故：

- ``hops=1``：`traces_to`（up）、`composes_from`（down）、`see_also`（both）；
- ``hops=2``：**仅**追加 `traces_to`（其余 kind 已被各自 `max_hops` 截断）；
- ``source_ref``：``max_hops=0`` → 从不跟随（「不参与多跳」的最强读法）。

软删与悬空（L5 / ADR-009）
--------------------------

- 默认过滤 `status='deleted'` 节点：软删节点**既不返回也不再展开**（视作已从图中摘除）；
  `include_deleted=True` 时二者一并放开。
- `dst_node_id IS NULL` 的**文档级引用**与指向不存在节点的悬空边都不产生命中：前者无
  节点可落，后者在 `nodes` 解析时被丢弃（这正是 M09B `broken_refs` 的巡检口径）。

分区策略（ADR-009 V16）
-----------------------

`nodes` 按 `doc_id` HASH 64 分区，按 `node_id` 单列点查无法裁剪。遍历时**能带 `doc_id`
就带**：

- 根节点：调用方给 `doc_id=` 即裁剪到单分区（缺省则全 64 分区 Append）；
- 前沿节点恒持有 `doc_id`（由上一跳解析得到），故 `refs.src_node_id`（down 取边）与
  `refs.dst_doc_id`（up 取边；`idx_refs_dst`）两侧都可裁剪；
- 命中节点的元数据解析按 `doc_id` 分组发查询：down 方向由 `refs.dst_doc_id` 给出
  `doc_id`（裁剪），up 方向只能拿 `node_id` 裸查（不可裁剪，计入 `unpruned` 计数并落
  `info` 日志）。

其他口径
--------

- 排序：跳数升序 → `doc_id` 升序（「文档序」；`docs` 无序列列，以 doc_id 为序）→
  `ordinal` → `node_id`（末位仅取确定性）；
- 起点自身**不**出现在结果里（`hops >= 1`）；同跳多路径命中时取确定序最前者（前沿序 →
  kind 序 → 目标 doc_id → 目标 node_id），保证同一图两次调用结果一致；
- 纯查询、无事件、无 LLM（P6）。
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from typing import Final, Literal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agenticspec.model import RefKind, TraversalHit
from agenticspec.observability import get_logger, slow_query_ms
from agenticspec.store import NotFoundError, Storage, ValidationError, as_uuid, get_storage
from agenticspec.store.schema import nodes, refs

__all__ = ["KIND_RULES", "MAX_HOPS", "Direction", "expandable_kinds", "traverse"]

log = get_logger("m05.traverse")

Direction = Literal["up", "down", "both"]

KIND_RULES: Final[dict[RefKind, tuple[Direction, bool, int]]] = {
    "traces_to": ("up", True, 2),
    "composes_from": ("down", True, 1),
    "see_also": ("both", True, 1),
    "source_ref": ("up", False, 0),
}
"""`(方向, 参与多跳, 最大跳数)`（§3 M05 / A19）。键序即同跳命中的稳定 tie-break 序。"""

MAX_HOPS: Final = max(rule[2] for rule in KIND_RULES.values())
"""可达最大跳数（`traces_to` 的 2 跳）——`hops` 超过它无额外效果。"""


def expandable_kinds(step: int) -> tuple[RefKind, ...]:
    """第 `step` 跳允许跟随的 kind 元组（`hops` 按各 kind 的 `max_hops` 截断）。

    `source_ref` 的 `max_hops=0` 使其在任何跳数下都不可达；`composes_from`/`see_also`
    为 1，故 `hops=2` 时**仅** `traces_to` 追加一跳（REQ-M05-F01）。
    """
    if step < 1:
        return ()
    return tuple(
        kind
        for kind, (_direction, multi_hop, max_hops) in KIND_RULES.items()
        if step <= max_hops and (multi_hop or step == 1)
    )


@dataclass(frozen=True, slots=True)
class _NodeRow:
    """命中节点元数据（`nodes` 行投影，不含内容）。"""

    node_id: UUID
    doc_id: str
    anchor: str
    ordinal: int


@dataclass(frozen=True, slots=True)
class _Reached:
    """BFS 到达项：节点 + 跳数 + 最短路径的 kind 序列（`TraversalHit.via`）。"""

    node: _NodeRow
    hops: int
    via: tuple[RefKind, ...]


@dataclass(frozen=True, slots=True)
class _Candidate:
    """一步扩展的候选目标：目标节点 + 已知 `doc_id`（up 方向未知）+ 来源与 kind 序。"""

    node_id: UUID
    doc_id: str | None
    origin_index: int
    kind_index: int
    kind: RefKind
    via: tuple[RefKind, ...]

    @property
    def order(self) -> tuple[int, int, str, str]:
        """同跳多路径的稳定取舍序（前沿序 → kind 序 → 目标 doc_id → 目标 node_id）。"""
        return (self.origin_index, self.kind_index, self.doc_id or "", str(self.node_id))


#: 沿边取一步（`src→dst`）：前沿 `(node_id, doc_id)` → `(来源, 目标, 目标 doc_id)`。
FetchEdges = Callable[
    [Sequence[tuple[UUID, str]], RefKind],
    Awaitable[list[tuple[UUID, UUID, str | None]]],
]
#: 命中节点元数据解析：`(node_id, doc_id|None)` 探针 → 存活节点行。
ResolveNodes = Callable[
    [Sequence[tuple[UUID, str | None]], bool],
    Awaitable[list[_NodeRow]],
]


async def _walk(
    root: _NodeRow,
    hops: int,
    *,
    fetch_out: FetchEdges,
    fetch_in: FetchEdges,
    resolve_nodes: ResolveNodes,
    include_deleted: bool,
) -> tuple[list[_Reached], int]:
    """纯 BFS 核心（取边/解析函数可注入，故无需 PG 即可验证跳数/去重/环）。

    返回 `(按 跳数→doc_id→ordinal 排序的命中, 不可裁剪的元数据探针数)`。
    """
    reached: dict[UUID, _Reached] = {}
    visited: set[UUID] = {root.node_id}  # 含起点：环回到起点不产生命中（环截断）
    frontier: tuple[_Reached, ...] = (_Reached(root, 0, ()),)
    unpruned = 0

    for step in range(1, hops + 1):
        kinds = expandable_kinds(step)
        if not kinds:
            break
        sources = tuple((item.node.node_id, item.node.doc_id) for item in frontier)
        origin_index = {item.node.node_id: index for index, item in enumerate(frontier)}
        candidates: list[_Candidate] = []
        seen: set[UUID] = set()
        for kind_index, kind in enumerate(kinds):
            direction = KIND_RULES[kind][0]
            edges: list[tuple[UUID, UUID, str | None]] = []
            if direction in ("down", "both"):
                edges += await fetch_out(sources, kind)
            if direction in ("up", "both"):
                edges += await fetch_in(sources, kind)
            for origin, target, target_doc in sorted(
                set(edges), key=lambda edge: (origin_index[edge[0]], str(edge[1]))
            ):
                if target in visited or target in seen:
                    continue
                seen.add(target)
                candidates.append(
                    _Candidate(
                        node_id=target,
                        doc_id=target_doc,
                        origin_index=origin_index[origin],
                        kind_index=kind_index,
                        kind=kind,
                        via=frontier[origin_index[origin]].via + (kind,),
                    )
                )
        if not candidates:
            break
        candidates.sort(key=lambda candidate: candidate.order)
        unpruned += sum(1 for candidate in candidates if candidate.doc_id is None)
        rows = {
            row.node_id: row
            for row in await resolve_nodes(
                tuple((candidate.node_id, candidate.doc_id) for candidate in candidates),
                include_deleted,
            )
        }
        next_frontier: list[_Reached] = []
        for candidate in candidates:
            row = rows.get(candidate.node_id)
            if row is None:
                continue  # 不存在或已软删：不返回，也不再展开（L5）
            visited.add(candidate.node_id)
            hit = _Reached(node=row, hops=step, via=candidate.via)
            reached[candidate.node_id] = hit
            next_frontier.append(hit)
        if not next_frontier:
            break
        frontier = tuple(next_frontier)

    ordered = sorted(
        reached.values(),
        key=lambda item: (item.hops, item.node.doc_id, item.node.ordinal, str(item.node.node_id)),
    )
    return ordered, unpruned


async def _fetch_out(
    session: AsyncSession, sources: Sequence[tuple[UUID, str]], kind: RefKind
) -> list[tuple[UUID, UUID, str | None]]:
    """`src→dst` 取边（`idx_refs_src`，ADR-009 新增）；目标 doc 取自 `refs.dst_doc_id`。"""
    if not sources:
        return []
    statement = select(refs.c.src_node_id, refs.c.dst_node_id, refs.c.dst_doc_id).where(
        refs.c.src_node_id.in_([node_id for node_id, _doc_id in sources]),
        refs.c.kind == kind,
        refs.c.dst_node_id.is_not(None),  # 文档级引用（dst_node_id IS NULL）无节点可落
    )
    return [tuple(row) for row in (await session.execute(statement)).all()]


async def _fetch_in(
    session: AsyncSession, sources: Sequence[tuple[UUID, str]], kind: RefKind
) -> list[tuple[UUID, UUID, str | None]]:
    """`dst→src` 取边（`idx_refs_dst` 按 `doc_id` 裁剪）；目标在 `src` 侧，doc 未知 → None。"""
    if not sources:
        return []
    grouped: dict[str, list[UUID]] = {}
    for node_id, doc_id in sources:
        grouped.setdefault(doc_id, []).append(node_id)
    rows: list[tuple[UUID, UUID, str | None]] = []
    for doc_id, node_ids in grouped.items():
        statement = select(refs.c.dst_node_id, refs.c.src_node_id).where(
            refs.c.dst_doc_id == doc_id,
            refs.c.dst_node_id.in_(node_ids),
            refs.c.kind == kind,
        )
        rows.extend((dst, src, None) for dst, src in (await session.execute(statement)).all())
    return rows


async def _resolve_nodes(
    session: AsyncSession,
    probes: Sequence[tuple[UUID, str | None]],
    include_deleted: bool,
) -> list[_NodeRow]:
    """解析节点元数据；`doc_id` 已知的探针按分区裁剪（ADR-009 V16）。"""
    if not probes:
        return []
    grouped: dict[str, list[UUID]] = {}
    unknown: list[UUID] = []
    for node_id, doc_id in probes:
        if doc_id is None:
            unknown.append(node_id)
        else:
            grouped.setdefault(doc_id, []).append(node_id)
    columns = (nodes.c.node_id, nodes.c.doc_id, nodes.c.anchor, nodes.c.ordinal)
    rows: list[_NodeRow] = []
    for doc_id, node_ids in grouped.items():
        statement = select(*columns).where(nodes.c.doc_id == doc_id, nodes.c.node_id.in_(node_ids))
        if not include_deleted:
            statement = statement.where(nodes.c.status == "active")
        rows.extend(_NodeRow(*row) for row in (await session.execute(statement)).all())
    if unknown:  # 分区键未知：全 64 分区 Append（ADR-009 V16 的已知降级路径）
        statement = select(*columns).where(nodes.c.node_id.in_(unknown))
        if not include_deleted:
            statement = statement.where(nodes.c.status == "active")
        rows.extend(_NodeRow(*row) for row in (await session.execute(statement)).all())
    return rows


async def traverse(
    node_id: UUID | str,
    hops: int = 1,
    *,
    doc_id: str | None = None,
    storage: Storage | None = None,
    include_deleted: bool = False,
) -> list[TraversalHit]:
    """refs 多跳遍历（§3 M05；内部接口，ADR-008）。

    参数：
        node_id: 起点节点（不存在或已软删 → `NotFoundError`，除 `include_deleted=True`）。
        hops: 跳数上限；各 kind 再按 `max_hops` 截断（`hops=2` 仅扩 `traces_to`）。
        doc_id: 起点的 `doc_id`（ADR-009 V16 分区裁剪；缺失则全 64 分区探测）。给错会按
            「不存在」处理（与 M02 `get_node` 同口径：它是裁剪提示而非模糊匹配）。
        storage: `Storage` 注入（缺省取进程级单例），便于 M-LR/M09B 与测试装配。
        include_deleted: 同时纳入 `status='deleted'` 节点（默认过滤，L5）。

    返回：`TraversalHit[]`，按 跳数 → `doc_id` → `ordinal` 排序；**不含起点自身**。
    """
    if hops < 0:
        raise ValidationError(f"hops must be >= 0, got {hops}", entity="node", entity_id=node_id)
    try:
        root_id = as_uuid(node_id)
    except (ValueError, AttributeError, TypeError) as exc:
        raise ValidationError(
            f"invalid node_id {node_id!r}", entity="node", entity_id=node_id
        ) from exc
    store = get_storage() if storage is None else storage
    with log.timer("traverse", budget_ms=slow_query_ms(), node_id=str(node_id), hops=hops):
        async with store.db.session() as session:
            roots = await _resolve_nodes(session, ((root_id, doc_id),), include_deleted)
            if not roots:
                raise NotFoundError(
                    f"node {node_id} not found or deleted", entity="node", entity_id=node_id
                )
            root = roots[0]

            async def fetch_out(
                sources: Sequence[tuple[UUID, str]], kind: RefKind
            ) -> list[tuple[UUID, UUID, str | None]]:
                return await _fetch_out(session, sources, kind)

            async def fetch_in(
                sources: Sequence[tuple[UUID, str]], kind: RefKind
            ) -> list[tuple[UUID, UUID, str | None]]:
                return await _fetch_in(session, sources, kind)

            async def resolve_nodes(
                probes: Sequence[tuple[UUID, str | None]], with_deleted: bool
            ) -> list[_NodeRow]:
                return await _resolve_nodes(session, probes, with_deleted)

            reached, unpruned = (
                await _walk(
                    root,
                    min(hops, MAX_HOPS),
                    fetch_out=fetch_out,
                    fetch_in=fetch_in,
                    resolve_nodes=resolve_nodes,
                    include_deleted=include_deleted,
                )
                if hops > 0
                else ([], 0)
            )
    log.info(
        "traverse",
        node_id=str(node_id),
        doc_id=root.doc_id,
        hops=min(hops, MAX_HOPS),
        hits=len(reached),
        unpruned=unpruned,
    )
    return [
        TraversalHit(
            node_id=item.node.node_id,
            doc_id=item.node.doc_id,
            anchor=item.node.anchor,
            hops=item.hops,
            via=list(item.via),
        )
        for item in reached
    ]
