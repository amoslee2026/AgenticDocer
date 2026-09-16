"""M-LR 单测：导出包生成（REQ-MLR-F01）与增量事件流（REQ-MLR-F02）。

不碰库：`Storage` 用替身（实现 `get_doc` / `list_nodes_for_docs` / `changes_since` 三个
被调方法），`traverse` 用 monkeypatch 注入——M05 的真实遍历在集成测试
（`tests/integration/test_mlr_export.py`）里验，本文件只验 M-LR 自己的口径：
包格式、图关系构造与去重、确定性、游标语法、批分页与续拉不重不漏、P6 无网络。
"""

from __future__ import annotations

import json
import socket
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import pytest

from agenticdocer.mlr import export as export_module
from agenticdocer.mlr.export import (
    EXPORT_GRAPH_FILE,
    EXPORT_MANIFEST_FILE,
    EXPORT_NODES_FILE,
    export_package,
    node_record,
)
from agenticdocer.mlr.stream import _parse_cursor, change_stream, cursor_token
from agenticdocer.model import Doc, Event, Node, TraversalHit, new_uuid7, uuid7_timestamp_ms
from agenticdocer.store import NotFoundError, ValidationError

TS = datetime(2026, 9, 16, 10, 0, 0, tzinfo=timezone.utc)
DOC_A = "SPEC-A"
DOC_B = "SPEC-B"


# ── 替身与构造助手 ────────────────────────────────────────────────────────


def _doc(doc_id: str) -> Doc:
    return Doc(
        doc_id=doc_id,
        doc_type="standard",
        title=f"{doc_id} 标题",
        meta={},
        source_ref=None,
        status="approved",
        version=1,
        created_at=TS,
        updated_at=TS,
    )


def _node(
    doc_id: str,
    ordinal: int,
    *,
    content: dict[str, Any] | None = None,
    parent: UUID | None = None,
    level: int | None = None,
    atom_type: str = "clause",
    status: str = "active",
) -> Node:
    return Node(
        node_id=new_uuid7(),
        doc_id=doc_id,
        atom_type=atom_type,
        format="md",
        ordinal=ordinal,
        parent_node_id=parent,
        level=level,
        anchor=f"{doc_id}#n{ordinal}",
        content={"fragment": f"正文 {ordinal}"} if content is None else content,
        status=status,  # type: ignore[arg-type]
        version=1,
        created_at=TS,
        updated_at=TS,
    )


def _event(
    entity: str,
    entity_id: str,
    op: str,
    ts: datetime,
    event_id: UUID | None = None,
) -> Event:
    return Event(
        event_id=event_id or new_uuid7(),
        entity=entity,  # type: ignore[arg-type]
        entity_id=entity_id,
        op=op,  # type: ignore[arg-type]
        payload={},
        actor="tester",
        ts=ts,
    )


def _event_anchored(entity: str, entity_id: str, op: str, *, offset_ms: int = 0) -> Event:
    """`ts` 由 `event_id` 内嵌毫秒推导——复刻 `append_event` 的取值顺序（先 id 后 `ts`）。

    这正是裸 `event_id` 游标可解析的前提（`mlr.stream._resolve_exact` 的窗口假设）。
    """
    event_id = new_uuid7()
    ts = datetime.fromtimestamp(uuid7_timestamp_ms(event_id) / 1000, tz=timezone.utc)
    return _event(entity, entity_id, op, ts + timedelta(milliseconds=offset_ms), event_id=event_id)


class _FakeStorage:
    """`Storage` 替身：只实现 M-LR 调用到的三个方法。

    `changes_since` 是 M02 半开区间语义（`(ts, event_id) > 游标`）的**参考实现**——
    流的批分页/续拉逻辑据此对照，无需 PG。
    """

    def __init__(
        self,
        docs: list[Doc] | None = None,
        nodes: list[Node] | None = None,
        events: list[Event] | None = None,
    ) -> None:
        self.docs = {doc.doc_id: doc for doc in docs or []}
        self.nodes = nodes or []
        self.events = events or []
        self.calls: list[dict[str, Any]] = []

    async def get_doc(self, doc_id: str) -> Doc:
        if doc_id not in self.docs:
            raise NotFoundError(f"doc {doc_id} not found", entity="doc", entity_id=doc_id)
        return self.docs[doc_id]

    async def list_nodes_for_docs(
        self, doc_ids: list[str], include_deleted: bool = False
    ) -> list[Node]:
        wanted = set(doc_ids)
        return [
            node
            for node in sorted(self.nodes, key=lambda n: (n.doc_id, n.ordinal))
            if node.doc_id in wanted and (include_deleted or node.status == "active")
        ]

    async def changes_since(
        self,
        *,
        since_ts: datetime | None = None,
        since_event_id: UUID | str | None = None,
        entity: str | None = None,
        limit: int = 1000,
    ) -> list[Event]:
        self.calls.append(
            {"since_ts": since_ts, "since_event_id": since_event_id, "entity": entity, "limit": limit}
        )
        cursor = None if since_event_id is None else UUID(str(since_event_id))
        ordered = sorted(self.events, key=lambda event: (event.ts, event.event_id))
        out = []
        for event in ordered:
            if since_ts is not None:
                if cursor is not None and not (event.ts, event.event_id) > (since_ts, cursor):
                    continue
                if cursor is None and not event.ts > since_ts:
                    continue
            if entity is not None and event.entity != entity:
                continue
            out.append(event)
        return out[:limit]


def _fake_traverse(hits: dict[UUID, list[TraversalHit]]):
    """按起点返回预置命中（签名与 M05 `traverse` 一致）。"""

    async def traverse(
        node_id: UUID | str,
        hops: int = 1,
        *,
        doc_id: str | None = None,
        storage: Any = None,
        include_deleted: bool = False,
    ) -> list[TraversalHit]:
        return hits.get(UUID(str(node_id)), [])

    return traverse


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


@pytest.fixture
def no_relations(monkeypatch: pytest.MonkeyPatch) -> None:
    """把 M05 `traverse` 换成空结果——真实遍历需 PG，见集成测试。"""
    monkeypatch.setattr(export_module, "traverse", _fake_traverse({}))


# ── nodes.jsonl：文本来自 M04 渲染口径 ────────────────────────────────────


def test_node_record_uses_fragment_verbatim() -> None:
    """有 `content.fragment` → 逐字节直通（P4）。"""
    node = _node(DOC_A, 0, content={"fragment": "## 概览\n\n条款原文，含 <table></table>"})
    assert node_record(node)["text"] == "## 概览\n\n条款原文，含 <table></table>"


def test_node_record_synthesizes_when_fragment_absent() -> None:
    """无 fragment → 按 `atom_type`/`level` 合成（M04 `_synthesize`）。"""
    heading = _node(DOC_A, 1, content={"text": "概览"}, level=2, atom_type="clause")
    code = _node(DOC_A, 2, content={"language": "py", "text": "print(1)"}, atom_type="code")
    assert node_record(heading)["text"] == "## 概览"
    assert node_record(code)["text"] == "```py\nprint(1)\n```"


def test_node_record_has_exactly_the_specified_fields() -> None:
    """§3 M-LR 规定的 jsonl 形状，不多不少。"""
    node = _node(DOC_A, 3)
    record = node_record(node)
    assert set(record) == {"node_id", "doc_id", "anchor", "text"}
    assert record["node_id"] == str(node.node_id)
    assert record["doc_id"] == DOC_A
    assert record["anchor"] == node.anchor


# ── 导出包：文件、计数、确定性 ────────────────────────────────────────────


async def test_export_package_writes_three_files_and_counts(
    tmp_path: Path, no_relations: None
) -> None:
    nodes = [_node(DOC_A, 0), _node(DOC_A, 1), _node(DOC_B, 0, content={"text": ""})]
    store = _FakeStorage([_doc(DOC_A), _doc(DOC_B)], nodes)
    result = await export_package([DOC_A, DOC_B], tmp_path / "pkg", storage=store)

    assert (result.out_path, result.docs, result.nodes) == (str(tmp_path / "pkg"), 2, 3)
    records = _read_jsonl(tmp_path / "pkg" / EXPORT_NODES_FILE)
    assert [record["node_id"] for record in records] == [str(node.node_id) for node in nodes]
    assert records[1]["text"] == "正文 1"

    manifest = json.loads((tmp_path / "pkg" / EXPORT_MANIFEST_FILE).read_text(encoding="utf-8"))
    assert manifest["doc_ids"] == [DOC_A, DOC_B]
    assert manifest["counts"]["nodes"] == 3
    assert manifest["counts"]["docs"] == 2
    assert manifest["counts"]["text_empty"] == 1
    assert manifest["files"] == {"nodes": EXPORT_NODES_FILE, "relations": EXPORT_GRAPH_FILE}


async def test_export_package_defaults_skip_deleted_nodes(
    tmp_path: Path, no_relations: None
) -> None:
    nodes = [_node(DOC_A, 0), _node(DOC_A, 1, status="deleted")]
    store = _FakeStorage([_doc(DOC_A)], nodes)
    result = await export_package([DOC_A], tmp_path, storage=store)
    assert result.nodes == 1
    assert len(_read_jsonl(tmp_path / EXPORT_NODES_FILE)) == 1


async def test_export_package_is_deterministic(tmp_path: Path, no_relations: None) -> None:
    """同一库状态 → `nodes.jsonl`/`graph.jsonl` 逐字节一致。"""
    parent = _node(DOC_A, 0, level=1)
    child = _node(DOC_A, 1, parent=parent.node_id)
    store = _FakeStorage([_doc(DOC_A)], [child, parent])
    await export_package([DOC_A], tmp_path / "one", storage=store)
    await export_package([DOC_A], tmp_path / "two", storage=store)
    for name in (EXPORT_NODES_FILE, EXPORT_GRAPH_FILE):
        assert (tmp_path / "one" / name).read_bytes() == (tmp_path / "two" / name).read_bytes()


async def test_export_package_overwrites_previous_package(
    tmp_path: Path, no_relations: None
) -> None:
    """重跑不留上一版残留行（同名文件整体覆盖）。"""
    store = _FakeStorage([_doc(DOC_A)], [_node(DOC_A, 0), _node(DOC_A, 1)])
    await export_package([DOC_A], tmp_path, storage=store)
    store.nodes = [_node(DOC_A, 0)]
    await export_package([DOC_A], tmp_path, storage=store)
    assert len(_read_jsonl(tmp_path / EXPORT_NODES_FILE)) == 1


async def test_export_package_empty_doc_ids_yields_empty_package(tmp_path: Path) -> None:
    store = _FakeStorage()
    result = await export_package([], tmp_path, storage=store)
    assert (result.docs, result.nodes) == (0, 0)
    assert (tmp_path / EXPORT_NODES_FILE).read_text(encoding="utf-8") == ""
    assert (tmp_path / EXPORT_GRAPH_FILE).read_text(encoding="utf-8") == ""


async def test_export_package_deduplicates_doc_ids(tmp_path: Path, no_relations: None) -> None:
    """重复 doc_id 去重保序（否则 `docs` 计数与包内容不符）。"""
    store = _FakeStorage([_doc(DOC_A), _doc(DOC_B)], [_node(DOC_A, 0), _node(DOC_B, 0)])
    result = await export_package([DOC_B, DOC_B, DOC_A], tmp_path, storage=store)
    assert (result.docs, result.nodes) == (2, 2)
    manifest = json.loads((tmp_path / EXPORT_MANIFEST_FILE).read_text(encoding="utf-8"))
    assert manifest["doc_ids"] == [DOC_B, DOC_A]


async def test_export_package_missing_doc_raises_not_found(tmp_path: Path) -> None:
    store = _FakeStorage([_doc(DOC_A)])
    with pytest.raises(NotFoundError):
        await export_package([DOC_A, "SPEC-GONE"], tmp_path, storage=store)
    assert not (tmp_path / EXPORT_NODES_FILE).exists()


async def test_export_package_rejects_non_positive_hops(tmp_path: Path) -> None:
    store = _FakeStorage([_doc(DOC_A)])
    with pytest.raises(ValidationError):
        await export_package([DOC_A], tmp_path, storage=store, hops=0)


# ── graph.jsonl：父子关系 + M05 可达关系、方向、去重 ─────────────────────


async def test_graph_relations_include_hierarchy_and_traverse(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    parent = _node(DOC_A, 0, level=1)
    child = _node(DOC_A, 1, parent=parent.node_id)
    other_doc_node = _node(DOC_B, 0)
    hits = {
        child.node_id: [
            # 上游链：child 追溯到 other_doc_node（有向边 child → other）→ direction="in"
            TraversalHit(
                node_id=other_doc_node.node_id,
                doc_id=DOC_B,
                anchor=other_doc_node.anchor,
                hops=1,
                via=["traces_to"],
            )
        ],
        parent.node_id: [
            # 同一条父子关系也被 traverse 命中（refs 形态）→ 与 hierarchy 记录去重
            TraversalHit(
                node_id=child.node_id,
                doc_id=DOC_A,
                anchor=child.anchor,
                hops=1,
                via=["composes_from"],
            ),
            # 多跳路径 → direction=None
            TraversalHit(
                node_id=other_doc_node.node_id,
                doc_id=DOC_B,
                anchor=other_doc_node.anchor,
                hops=2,
                via=["traces_to", "traces_to"],
            ),
        ],
    }
    monkeypatch.setattr(export_module, "traverse", _fake_traverse(hits))
    store = _FakeStorage([_doc(DOC_A), _doc(DOC_B)], [parent, child, other_doc_node])

    await export_package([DOC_A, DOC_B], tmp_path, storage=store, hops=2)
    relations = _read_jsonl(tmp_path / EXPORT_GRAPH_FILE)

    # 1 条 hierarchy（父子）+ 2 条 traverse（上游链、多跳）——refs 形态的 composes_from 已去重
    assert len(relations) == 3
    hierarchy = [rel for rel in relations if rel["origin"] == "hierarchy"]
    assert len(hierarchy) == 1
    assert (hierarchy[0]["node_id"], hierarchy[0]["related_node_id"]) == (
        str(parent.node_id),
        str(child.node_id),
    )
    assert (hierarchy[0]["kinds"], hierarchy[0]["hops"], hierarchy[0]["direction"]) == (
        ["composes_from"],
        1,
        "out",
    )

    upstream = next(rel for rel in relations if rel["kinds"] == ["traces_to"])
    assert (upstream["node_id"], upstream["doc_id"]) == (str(child.node_id), DOC_A)
    assert (upstream["related_node_id"], upstream["related_doc_id"]) == (
        str(other_doc_node.node_id),
        DOC_B,
    )
    assert (upstream["hops"], upstream["direction"], upstream["origin"]) == (1, "in", "traverse")

    multi_hop = next(rel for rel in relations if rel["hops"] == 2)
    assert (multi_hop["kinds"], multi_hop["direction"]) == (["traces_to", "traces_to"], None)

    manifest = json.loads((tmp_path / EXPORT_MANIFEST_FILE).read_text(encoding="utf-8"))
    assert manifest["counts"]["relations_hierarchy"] == 1
    assert manifest["counts"]["relations_traverse"] == 2


async def test_traverse_deduplicates_multi_path_relations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """同一 `(node_id, related, hops, kinds)` 只出现一次（不同来源或重复命中均去重）。"""
    src = _node(DOC_A, 0)
    dst = _node(DOC_A, 1)
    same = [
        TraversalHit(node_id=dst.node_id, doc_id=DOC_A, anchor=dst.anchor, hops=1, via=["see_also"])
    ]
    hits = {src.node_id: same + same + same}
    monkeypatch.setattr(export_module, "traverse", _fake_traverse(hits))
    store = _FakeStorage([_doc(DOC_A)], [src, dst])

    await export_package([DOC_A], tmp_path, storage=store, hops=1)
    relations = _read_jsonl(tmp_path / EXPORT_GRAPH_FILE)
    assert len(relations) == 1
    assert relations[0]["direction"] == "both"


async def test_graph_relation_field_set(tmp_path: Path, no_relations: None) -> None:
    parent = _node(DOC_A, 0, level=1)
    child = _node(DOC_A, 1, parent=parent.node_id)
    store = _FakeStorage([_doc(DOC_A)], [parent, child])
    await export_package([DOC_A], tmp_path, storage=store)
    relation = _read_jsonl(tmp_path / EXPORT_GRAPH_FILE)[0]
    assert set(relation) == {
        "node_id",
        "doc_id",
        "related_node_id",
        "related_doc_id",
        "hops",
        "kinds",
        "direction",
        "origin",
    }


# ── P6：导出过程无网络 ────────────────────────────────────────────────────


async def test_export_makes_no_network_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, no_relations: None
) -> None:
    """P6/C7：导出只读本库 + 写本地文件——连 socket 都不该创建。"""

    def _blocked(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("network access attempted during export (P6/C7 violation)")

    monkeypatch.setattr(socket, "socket", _blocked)  # 连 socket 对象都不允许创建
    monkeypatch.setattr(socket, "create_connection", _blocked)
    parent = _node(DOC_A, 0, level=1)
    child = _node(DOC_A, 1, parent=parent.node_id)
    store = _FakeStorage([_doc(DOC_A)], [parent, child])

    await export_package([DOC_A], tmp_path, storage=store)
    assert (tmp_path / EXPORT_NODES_FILE).exists()
    assert not [name for name in sys.modules if name.split(".")[0] == "lightrag"]


# ── 增量流：游标语法 ──────────────────────────────────────────────────────


def test_cursor_token_round_trips_through_parse() -> None:
    event = _event("node", "n1", "create", TS)
    cursor = _parse_cursor(cursor_token(event))
    assert (cursor.ts, cursor.event_id) == (event.ts, event.event_id)


def test_parse_cursor_accepts_none_and_blank_as_head() -> None:
    for value in (None, "", "   "):
        cursor = _parse_cursor(value)
        assert (cursor.ts, cursor.event_id, cursor.pending_id) == (None, None, None)


def test_parse_cursor_accepts_iso_timestamp_with_and_without_zone() -> None:
    aware = _parse_cursor("2026-09-16T10:00:00+02:00")
    naive = _parse_cursor("2026-09-16T08:00:00")
    assert aware.ts == naive.ts
    assert naive.ts is not None and naive.ts.tzinfo is timezone.utc


def test_parse_cursor_accepts_bare_uuid7_as_pending() -> None:
    event_id = new_uuid7()
    cursor = _parse_cursor(str(event_id))
    assert (cursor.ts, cursor.event_id, cursor.pending_id) == (None, None, event_id)


def test_parse_cursor_rejects_invalid_timestamp() -> None:
    with pytest.raises(ValidationError):
        _parse_cursor("2026-09-16T10:00:00@not-a-uuid")


def test_parse_cursor_rejects_non_uuid7_event_id() -> None:
    with pytest.raises(ValidationError):
        _parse_cursor(str(uuid4()))


# ── 增量流：批分页与续拉（不重不漏） ─────────────────────────────────────


async def test_change_stream_yields_all_events_in_order_and_stops() -> None:
    events = [
        _event("node", f"n{i}", "create", TS + timedelta(milliseconds=i)) for i in range(5)
    ]
    store = _FakeStorage(events=events)
    got = [event async for event in change_stream(batch_size=2, storage=store)]
    assert [event.entity_id for event in got] == ["n0", "n1", "n2", "n3", "n4"]
    # 3 次拉取：2 + 2 + 1（末批不满即结束，不再多跑一次确认）
    assert [call["limit"] for call in store.calls] == [2, 2, 2]


async def test_change_stream_resumes_exactly_from_cursor_token() -> None:
    events = [
        _event("node", f"n{i}", "create", TS + timedelta(milliseconds=i)) for i in range(4)
    ]
    store = _FakeStorage(events=events)
    first = [event async for event in change_stream(batch_size=2, storage=store)]
    assert len(first) == 4

    store.calls.clear()
    resumed = [event async for event in change_stream(cursor_token(first[1]), storage=store)]
    assert [event.entity_id for event in resumed] == ["n2", "n3"]


async def test_change_stream_same_timestamp_events_are_not_skipped() -> None:
    """同一 `ts` 的多条事件靠 `event_id` 定序续拉——只按 `ts` 会漏（M02 口径）。"""
    same_ts = TS + timedelta(seconds=1)
    events = [_event("node", f"n{i}", "create", same_ts) for i in range(3)]
    store = _FakeStorage(events=events)
    got = [event async for event in change_stream(batch_size=2, storage=store)]
    assert len(got) == 3

    store.calls.clear()
    resumed = [event async for event in change_stream(cursor_token(got[0]), storage=store)]
    assert resumed == got[1:]


async def test_change_stream_coarse_timestamp_cursor_is_strictly_after() -> None:
    events = [
        _event("node", "n0", "create", TS),
        _event("node", "n1", "create", TS + timedelta(seconds=1)),
    ]
    store = _FakeStorage(events=events)
    got = [event async for event in change_stream(TS.isoformat(), storage=store)]
    assert [event.entity_id for event in got] == ["n1"]


async def test_change_stream_bare_event_id_cursor_resolves_exactly() -> None:
    """裸 `event_id` 游标：`ts` 从库里解析（`append_event` 先取 id 后取 `ts`）。"""
    events = [
        _event_anchored("node", "n0", "create"),
        _event_anchored("node", "n1", "create", offset_ms=5),
    ]
    store = _FakeStorage(events=events)
    got = [event async for event in change_stream(str(events[0].event_id), storage=store)]
    assert [event.entity_id for event in got] == ["n1"]


async def test_change_stream_unknown_event_id_cursor_is_rejected() -> None:
    store = _FakeStorage(events=[_event("node", "n0", "create", TS)])
    with pytest.raises(ValidationError):
        [event async for event in change_stream(str(new_uuid7()), storage=store)]


async def test_change_stream_filters_by_entity() -> None:
    events = [
        _event("node", "n0", "create", TS),
        _event("doc", DOC_A, "status", TS + timedelta(milliseconds=1)),
        _event("node", "n1", "create", TS + timedelta(milliseconds=2)),
    ]
    store = _FakeStorage(events=events)
    got = [event async for event in change_stream(entity="node", storage=store)]
    assert [event.entity_id for event in got] == ["n0", "n1"]


async def test_change_stream_empty_and_invalid_batch_size() -> None:
    store = _FakeStorage()
    assert [event async for event in change_stream(storage=store)] == []
    with pytest.raises(ValidationError):
        [event async for event in change_stream(batch_size=0, storage=store)]
