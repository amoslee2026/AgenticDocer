"""M09B `events_consistency` detector：events 重放 vs 当前态（REQ-M02-F03 验收 / ADR-009）。

`events` 是 append-only 的**权威变更日志**（P2）：任一实体的当前行必须等于其事件序列
按 §3.5 折叠（M02 `apply_events`）的结果。ADR-009 把 `events` 改为 `(event_id, ts)` 分区表、
外键降级后，这条「重放 == 当前态」是事件与实体之间**唯一**的完整性兼底，故本 detector
直接消费 M02 的折叠实现（不另写折叠逻辑，P5）。

判据：

* `M09B.events.node_drift` / `M09B.events.doc_drift` — 重放某字段 ≠ 当前行同字段
  （`path = nodes/<id>#<field>`，逐字段一条，便于按字段定位修复）；
* `M09B.events.no_create` — 当前行存在但事件序列里没有 `create`（折叠不出快照）：事件
  与实体**未同事务**写入或事件被绕过（P2 违规）；
* `M09B.events.op_invalid` — 事件的 `op` 不在该实体的合法取值域（§3.5；DDL 层是自由文本）；
* `M09B.events.orphan` — 有事件但其 entity 无对应当前行（软删会保留行，故这代表硬删/丢行）。

作用域：`doc_ids=None` 时按全库取数（事件亦全量取该 entity，避免巨型 `IN` 列表）；给定
`doc_ids` 时节点按 `doc_id` 裁剪、事件按 `entity_id ∈ 该文档节点` 裁剪。
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Final

from sqlalchemy import Select, select

from agenticspec.model import Doc, Event, Node, Violation
from agenticspec.store import ValidationError, apply_events
from agenticspec.store.rows import build_model
from agenticspec.store.schema import events as events_table

from .context import GateContext

__all__ = [
    "DETECTOR_ID",
    "MAX_ORPHAN_REPORTS",
    "RULES_EVENTS_CONSISTENCY",
    "detect",
    "judge_docs",
    "judge_nodes",
    "judge_orphans",
]

DETECTOR_ID: Final = "events_consistency"

RULE_NODE_DRIFT: Final = "M09B.events.node_drift"
RULE_DOC_DRIFT: Final = "M09B.events.doc_drift"
RULE_NO_CREATE: Final = "M09B.events.no_create"
RULE_OP_INVALID: Final = "M09B.events.op_invalid"
RULE_ORPHAN: Final = "M09B.events.orphan"

RULES_EVENTS_CONSISTENCY: tuple[str, ...] = (
    RULE_NODE_DRIFT,
    RULE_DOC_DRIFT,
    RULE_NO_CREATE,
    RULE_OP_INVALID,
    RULE_ORPHAN,
)

MAX_ORPHAN_REPORTS: Final = 500
"""单次巡检最多逐条报出的孤儿事件数（超出部分只进日志，避免报告被淹没）。"""


def _canonical(model: Any) -> dict[str, Any]:
    """模型 → 可比较字典（`mode="json"`：UUID/datetime 与事件载荷同口径）。"""
    return model.model_dump(mode="json")


def _drift(
    *, rule_id: str, path: str, entity: str, expected: Mapping[str, Any], actual: Mapping[str, Any]
) -> list[Violation]:
    """逐字段比较（键并集，逐字段一条违规）。"""
    violations: list[Violation] = []
    for field in sorted(set(expected) | set(actual)):
        want = expected.get(field)
        got = actual.get(field)
        if want == got:
            continue
        violations.append(
            Violation(
                rule_id=rule_id,
                path=f"{path}#{field}",
                message=(
                    f"{entity} 的事件重放与当前态不一致：{field} 重放={want!r} 当前={got!r}"
                    "（events 为权威源，§3.5 折叠应为逐字段恒等）"
                ),
                fix_hint=(
                    f"核对 {entity} 的写入路径是否绕过事件（P2：事件与实体同事务）；"
                    "必要时以当前态为准补写补偿事件（events append-only，不可改历史）"
                ),
            )
        )
    return violations


def _fold(entity: str, history: Sequence[Event]) -> tuple[Any, Violation | None]:
    """折叠事件；`op` 越界 → `(None, 违规)`（不抛出，质量门必须给出结论）。"""
    try:
        return apply_events(entity, history), None
    except ValidationError as exc:
        first = history[0]
        return None, Violation(
            rule_id=RULE_OP_INVALID,
            path=f"{entity}s/{first.entity_id}",
            message=f"事件 op 越界：{exc}",
            fix_hint="修正写入侧的事件 op（取值域见 §3.5 / M02 fold.ENTITY_OPS）",
        )


def _incomplete(model: Any, fields: Sequence[str]) -> list[str]:
    """折叠结果缺失的字段（`_fold_*` 对部分状态会退回 `model_construct`，快照不完整）。"""
    return sorted(set(fields) - set(model.model_fields_set))


def _no_create(path: str, subject: str, detail: str) -> Violation:
    return Violation(
        rule_id=RULE_NO_CREATE,
        path=path,
        message=f"{subject}缺 create（折叠不出完整快照）：{detail}",
        fix_hint="补齐 create 事件（含全量 before 字段）或重导该文档（P2：事件与实体同事务）",
    )


def judge_nodes(
    rows: Sequence[Node], history: Mapping[str, Sequence[Event]]
) -> list[Violation]:
    """节点判据（纯函数）：重放折叠结果 vs 当前行逐字段比较。"""
    violations: list[Violation] = []
    for node in rows:
        node_id = str(node.node_id)
        path = f"nodes/{node_id}"
        recorded = history.get(node_id)
        if not recorded:
            violations.append(
                _no_create(path, "节点存在但无任何事件", f"{node_id}（doc_id={node.doc_id}）")
            )
            continue
        snapshot, problem = _fold("node", recorded)
        if problem is not None:
            violations.append(problem)
            continue
        if snapshot.node is None:
            violations.append(
                _no_create(path, "节点事件序列", f"{node_id}，op={[event.op for event in recorded]}")
            )
            continue
        missing = _incomplete(snapshot.node, tuple(Node.model_fields))
        if missing:
            violations.append(
                _no_create(
                    path,
                    "节点事件序列",
                    f"{node_id}，折叠结果缺字段 {missing}（事件数={len(recorded)}）",
                )
            )
            continue
        violations.extend(
            _drift(
                rule_id=RULE_NODE_DRIFT,
                path=path,
                entity="node",
                expected=_canonical(snapshot.node),
                actual=_canonical(node),
            )
        )
    return violations


def judge_docs(
    rows: Sequence[Doc], history: Mapping[str, Sequence[Event]]
) -> list[Violation]:
    """文档判据（纯函数）：`apply_events('doc', …)` → `Doc` 逐字段比较。"""
    violations: list[Violation] = []
    for doc in rows:
        doc_id = doc.doc_id
        path = f"docs/{doc_id}"
        recorded = history.get(doc_id)
        if not recorded:
            violations.append(_no_create(path, "文档存在但无任何事件", doc_id))
            continue
        folded, problem = _fold("doc", recorded)
        if problem is not None:
            violations.append(problem)
            continue
        missing = sorted(set(Doc.model_fields) - set(folded))
        if missing:
            violations.append(
                _no_create(
                    path,
                    "文档事件序列",
                    f"{doc_id}，折叠结果缺字段 {missing}（事件数={len(recorded)}）",
                )
            )
            continue
        violations.extend(
            _drift(
                rule_id=RULE_DOC_DRIFT,
                path=path,
                entity="doc",
                expected=_canonical(Doc.model_validate(folded)),
                actual=_canonical(doc),
            )
        )
    return violations


def judge_orphans(
    history: Mapping[str, Sequence[Event]], present: set[str], *, entity: str
) -> list[Violation]:
    """有事件但当前行不存在（软删会保留行；故代表硬删或丢行）。"""
    violations: list[Violation] = []
    orphans = sorted(set(history) - present)
    for entity_id in orphans[:MAX_ORPHAN_REPORTS]:
        violations.append(
            Violation(
                rule_id=RULE_ORPHAN,
                path=f"{entity}s/{entity_id}",
                message=(
                    f"{entity} 有事件但当前态行不存在：{entity_id}"
                    f"（事件数={len(history[entity_id])}）——events 为权威源，行不该消失"
                ),
                fix_hint="按事件重放恢复该行（或确认是否为测试/运维的直接 DELETE，需留痕）",
            )
        )
    return violations


# ── 取数 ─────────────────────────────────────────────────────────────────


def _events_statement(entity: str, entity_ids: Sequence[str] | None) -> Select[Any]:
    statement = (
        select(*tuple(events_table.c))
        .where(events_table.c.entity == entity)
        .order_by(events_table.c.ts, events_table.c.event_id)
    )
    if entity_ids is not None:
        statement = statement.where(events_table.c.entity_id.in_(tuple(entity_ids)))
    return statement


def _group(rows: Sequence[Mapping[str, Any]]) -> dict[str, list[Event]]:
    """事件行（`RowMapping`）→ `entity_id → 按 ts 定序的事件序列`。"""
    grouped: dict[str, list[Event]] = {}
    for row in rows:
        event = build_model(Event, dict(row))
        grouped.setdefault(str(event.entity_id), []).append(event)
    return grouped


async def detect(ctx: GateContext) -> list[Violation]:
    """执行 events ↔ 当前态巡检（节点 + 文档两类实体）。"""
    docs = await ctx.storage.list_docs()
    if ctx.doc_ids is not None:
        wanted = set(ctx.doc_ids)
        docs = [doc for doc in docs if doc.doc_id in wanted]
    doc_ids = [doc.doc_id for doc in docs]
    nodes = await ctx.storage.list_nodes_for_docs(doc_ids, include_deleted=True) if doc_ids else []
    node_ids = [str(node.node_id) for node in nodes]

    async with ctx.storage.db.session() as session:
        node_events = _group(
            (
                await session.execute(
                    _events_statement("node", node_ids if ctx.doc_ids is not None else None)
                )
            )
            .mappings()
            .all()
        )
        doc_events = _group(
            (
                await session.execute(
                    _events_statement("doc", doc_ids if ctx.doc_ids is not None else None)
                )
            )
            .mappings()
            .all()
        )

    violations = [
        *judge_nodes(nodes, node_events),
        *judge_docs(docs, doc_events),
    ]
    if ctx.doc_ids is None:
        violations.extend(judge_orphans(node_events, set(node_ids), entity="node"))
        violations.extend(judge_orphans(doc_events, set(doc_ids), entity="doc"))
        total_orphans = len(set(node_events) - set(node_ids)) + len(set(doc_events) - set(doc_ids))
        if total_orphans > MAX_ORPHAN_REPORTS:
            ctx.logger.warn("orphan events exceed report cap", orphans=total_orphans)
    return violations


