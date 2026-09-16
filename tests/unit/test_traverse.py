"""M05 图遍历单测（纯逻辑，不需要 PG）——跳数截断 / 去重保留最短 / 环截断 / 软删过滤 / 排序。

数据库侧（分区裁剪、FTS）留给 `tests/integration/test_retrieve.py`；本文件把 `_walk` 的
取边与解析函数替换为内存图，使「图语义」可脱离 PG 逐条验证（fixture 的边写在用例里，
不从生产代码生成）。
"""

from __future__ import annotations

import pathlib
from uuid import UUID

import pytest

from agenticdocer.model import RefKind, TraversalHit, new_uuid7
from agenticdocer.retrieve import KIND_RULES, MAX_HOPS, expandable_kinds, traverse
from agenticdocer.retrieve.traverse import _NodeRow, _walk
from agenticdocer.store import ValidationError


class Graph:
    """内存 refs 图：`ref(kind, src, dst)` 建边；节点元数据（doc/anchor/ordinal/status）自持。"""

    def __init__(self) -> None:
        self.edges: dict[str, list[tuple[UUID, UUID]]] = {}
        self.nodes: dict[UUID, tuple[str, str, int, str]] = {}

    def node(self, ordinal: int = 0, *, doc_id: str = "DOC-A", status: str = "active") -> UUID:
        node_id = new_uuid7()
        self.nodes[node_id] = (doc_id, f"{doc_id}#{ordinal}", ordinal, status)
        return node_id

    def ref(self, kind: RefKind, src: UUID, dst: UUID) -> None:
        self.edges.setdefault(kind, []).append((src, dst))

    def row(self, node_id: UUID) -> _NodeRow:
        doc_id, anchor, ordinal, _status = self.nodes[node_id]
        return _NodeRow(node_id, doc_id, anchor, ordinal)

    # ── `_walk` 的注入面（签名与生产实现一致）──────────────────────────────

    async def fetch_out(self, sources, kind):
        """`src→dst`：目标 doc 取自边自身；目标不在图里则 doc 未知（悬空边）。"""
        srcs = {node_id for node_id, _doc_id in sources}
        return [
            (src, dst, self.nodes[dst][0] if dst in self.nodes else None)
            for src, dst in self.edges.get(kind, [])
            if src in srcs
        ]

    async def fetch_in(self, sources, kind):
        """`dst→src`：目标永远是前端节点，doc 未知。"""
        dsts = {node_id for node_id, _doc_id in sources}
        return [(dst, src, None) for src, dst in self.edges.get(kind, []) if dst in dsts]

    async def resolve(self, probes, include_deleted):
        rows: list[_NodeRow] = []
        for node_id, _doc_id in probes:
            if node_id not in self.nodes:
                continue
            if self.nodes[node_id][3] == "deleted" and not include_deleted:
                continue
            rows.append(self.row(node_id))
        return rows

    async def walk(self, node_id: UUID, hops: int = 1, *, include_deleted: bool = False):
        return await _walk(
            self.row(node_id),
            hops,
            fetch_out=self.fetch_out,
            fetch_in=self.fetch_in,
            resolve_nodes=self.resolve,
            include_deleted=include_deleted,
        )


async def walked(
    graph: Graph, node_id: UUID, hops: int = 1, *, include_deleted: bool = False
) -> list[TraversalHit]:
    """跑 `_walk` 并把结果转成契约类型（与 `traverse()` 的返回口径一致）。"""
    reached, _unpruned = await graph.walk(node_id, hops, include_deleted=include_deleted)
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


# ── KIND_RULES / 跳数截断（§3 M05 + A19）─────────────────────────────────


def test_kind_rules_match_spec() -> None:
    """规则表逐字冻结规范值；键序即同跳 tie-break 序。"""
    assert KIND_RULES == {
        "traces_to": ("up", True, 2),
        "composes_from": ("down", True, 1),
        "see_also": ("both", True, 1),
        "source_ref": ("up", False, 0),
    }
    assert MAX_HOPS == 2


def test_expandable_kinds_by_step() -> None:
    """`hops` 按 kind 的 `max_hops` 截断：hops=2 仅扩 traces_to；source_ref 永不参与。"""
    assert expandable_kinds(0) == ()
    assert expandable_kinds(1) == ("traces_to", "composes_from", "see_also")
    assert expandable_kinds(2) == ("traces_to",)
    assert expandable_kinds(3) == ()


async def test_traces_to_traverses_two_hops_upstream() -> None:
    """`traces_to` 2 跳（design_doc §6.4：up = dst→src，命中在被引用侧）。"""
    graph = Graph()
    a, b, c = graph.node(0), graph.node(1), graph.node(2)
    graph.ref("traces_to", a, b)
    graph.ref("traces_to", b, c)

    one = await walked(graph, c, 1)
    assert [hit.node_id for hit in one] == [b]
    assert one[0].hops == 1 and one[0].via == ["traces_to"]

    two = await walked(graph, c, 2)
    assert [(hit.node_id, hit.hops, hit.via) for hit in two] == [
        (b, 1, ["traces_to"]),
        (a, 2, ["traces_to", "traces_to"]),
    ]
    # 起点自身不出现；hops 超过 MAX_HOPS 无额外效果（链只有 2 跳）
    assert c not in {hit.node_id for hit in two}
    assert [hit.node_id for hit in await walked(graph, c, 9)] == [b, a]


async def test_composes_from_is_single_hop() -> None:
    """`composes_from` 下游 1 跳：hops=2 也不得扩第二跳。"""
    graph = Graph()
    x, y, z = graph.node(0), graph.node(1), graph.node(2)
    graph.ref("composes_from", x, y)
    graph.ref("composes_from", y, z)

    assert [hit.node_id for hit in await walked(graph, x, 2)] == [y]
    assert [hit.node_id for hit in await walked(graph, y, 2)] == [z]


async def test_see_also_is_bidirectional_single_hop() -> None:
    """`see_also` 双向 1 跳（两向都命中，且不再延伸第二跳）。"""
    graph = Graph()
    m, n, deeper = graph.node(0), graph.node(1), graph.node(2)
    graph.ref("see_also", m, n)
    graph.ref("see_also", n, deeper)

    assert [hit.node_id for hit in await walked(graph, m, 1)] == [n]
    both = await walked(graph, n, 1)
    assert sorted(hit.node_id for hit in both) == sorted([m, deeper])
    # 1 跳上限：hops=2 时 step2 仅剩 traces_to，see_also 不再延伸
    assert [hit.node_id for hit in await walked(graph, m, 2)] == [n]


async def test_source_ref_never_participates() -> None:
    """`source_ref` 不参与多跳（max_hops=0）——两侧、任何跳数都不可达。"""
    graph = Graph()
    s, t = graph.node(0), graph.node(1)
    graph.ref("source_ref", s, t)

    assert await walked(graph, s, 1) == []
    assert await walked(graph, s, 2) == []
    assert await walked(graph, t, 1) == []
    assert await walked(graph, t, 2) == []


async def test_hops_zero_returns_nothing() -> None:
    graph = Graph()
    a, b = graph.node(0), graph.node(1)
    graph.ref("see_also", a, b)
    assert await walked(graph, a, 0) == []


# ── 去重 / 环 / 排序 ─────────────────────────────────────────────────────


async def test_cycle_is_truncated_and_root_excluded() -> None:
    """环回到起点不产生命中；链式环不无限递归。"""
    graph = Graph()
    a, b, c = graph.node(0), graph.node(1), graph.node(2)
    graph.ref("traces_to", a, b)
    graph.ref("traces_to", b, c)
    graph.ref("traces_to", c, a)  # 环 a→b→c→a

    hits = await walked(graph, a, 5)
    assert [(hit.node_id, hit.hops) for hit in hits] == [(c, 1), (b, 2)]


async def test_self_loop_yields_nothing() -> None:
    graph = Graph()
    a = graph.node(0)
    graph.ref("traces_to", a, a)
    assert await walked(graph, a, 2) == []


async def test_dedup_keeps_shortest_path() -> None:
    """同一节点既在 1 跳（see_also）又可在 2 跳（traces_to）达时，保留最短路径。"""
    graph = Graph()
    a, b, c = graph.node(0), graph.node(1), graph.node(2)
    graph.ref("traces_to", a, b)
    graph.ref("traces_to", b, c)
    graph.ref("see_also", a, c)  # a 与 c 直接相关 → 1 跳可达

    hits = await walked(graph, c, 2)
    assert [(hit.node_id, hit.hops, hit.via) for hit in hits] == [
        (a, 1, ["see_also"]),
        (b, 1, ["traces_to"]),
    ]
    # 重复调用结果完全一致（确定序）
    again = await walked(graph, c, 2)
    assert [hit.node_id for hit in again] == [hit.node_id for hit in hits]


async def test_ordering_is_hops_then_doc_then_ordinal() -> None:
    """排序 = 跳数 → doc 序（doc_id 升序）→ ordinal。"""
    graph = Graph()
    hub = graph.node(0, doc_id="DOC-Z")
    far = graph.node(3, doc_id="DOC-Z")
    b5 = graph.node(5, doc_id="DOC-B")
    a9 = graph.node(9, doc_id="DOC-A")
    a2 = graph.node(2, doc_id="DOC-A")
    for target in (b5, a9, a2, far):
        graph.ref("see_also", hub, target)
    graph.ref("traces_to", graph.node(4, doc_id="DOC-A"), far)  # 2 跳命中：doc 序最前也排最后

    hits = await walked(graph, hub, 2)
    assert [(hit.doc_id, hit.anchor, hit.hops) for hit in hits] == [
        ("DOC-A", "DOC-A#2", 1),
        ("DOC-A", "DOC-A#9", 1),
        ("DOC-B", "DOC-B#5", 1),
        ("DOC-Z", "DOC-Z#3", 1),
        ("DOC-A", "DOC-A#4", 2),
    ]


# ── 软删过滤（L5）───────────────────────────────────────────────────────


async def test_deleted_node_filtered_and_not_expanded() -> None:
    """软删节点默认既不返回也不再展开；`include_deleted=True` 时二者放开。"""
    graph = Graph()
    a, b, c = graph.node(0), graph.node(1, status="deleted"), graph.node(2)
    graph.ref("traces_to", a, b)
    graph.ref("traces_to", b, c)

    assert await walked(graph, c, 2) == []
    kept = await walked(graph, c, 2, include_deleted=True)
    assert [(hit.node_id, hit.hops) for hit in kept] == [(b, 1), (a, 2)]


async def test_missing_target_node_is_skipped() -> None:
    """悬空边（目标不在 `nodes`）不产生命中（M09B `broken_refs` 的口径）。"""
    graph = Graph()
    a, ghost = graph.node(0), new_uuid7()
    graph.ref("see_also", a, ghost)
    assert await walked(graph, a, 1) == []


async def test_unpruned_probe_counted() -> None:
    """up 方向命中节点 doc 未知 → 计入不可裁剪探针数（ADR-009 V16 的观测面）。"""
    graph = Graph()
    a, b = graph.node(0), graph.node(1)
    graph.ref("traces_to", a, b)
    _reached, unpruned = await graph.walk(b, 1)
    assert unpruned == 1


# ── 入参校验（不触碰 PG）────────────────────────────────────────────────


async def test_traverse_rejects_negative_hops() -> None:
    with pytest.raises(ValidationError):
        await traverse(new_uuid7(), -1)


async def test_traverse_rejects_malformed_node_id() -> None:
    with pytest.raises(ValidationError):
        await traverse("not-a-uuid", 1)


# ── ADR-008 边界守护（静态检查，不需要 PG）──────────────────────────────


def test_retrieve_exposes_no_public_endpoint() -> None:
    assert sources, "retrieve 包不得为空"
    assert "fastapi" not in sources.lower(), "内部实现不得引入 FastAPI"
    assert "APIRouter" not in sources and "include_router" not in sources
    assert "@router." not in sources
    assert "router" not in sources
