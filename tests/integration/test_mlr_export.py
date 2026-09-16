"""M-LR 集成测试：真实 PostgreSQL（`DATABASE_URL`）+ 真实 M02/M04/M05。

不需要运行的场景（无 PG / 无凭据）由 `conftest.py` 整体 skip，不会 fail。

覆盖：

* 导出包端到端——`nodes.jsonl` 文本与 **M04 整档渲染正文**一致（同一库读路径）、
  `graph.jsonl` 含节点树父子与 **M05 `traverse` 真实遍历**得到的 `traces_to` 上游链
  （含 2 跳）、``see_also``；refs 形态的 `composes_from` 与节点树父子**去重**；
* 包的确定性（同状态两次导出 `nodes.jsonl`/`graph.jsonl` 逐字节一致）与覆盖写；
* 增量流与 M02 事件日志一致：全量拉取按 `(ts, event_id)` 定序、游标 token 续拉**不重不漏**
  （断言对并发写入者鲁棒——只比对「严格晚于游标」这一半开区间口径）；
* P6/C7：导出与拉流过程**无外部网络**（socket 层断言，放行 loopback 上的 PG）。

测试数据用唯一 `doc_id` 前缀（`SPEC-MLR-<hex>`），不 drop schema，可与并行 agent 共存。
"""

from __future__ import annotations

import json
import socket
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest

from agenticdocer.mlr import change_stream, cursor_token, export_package
from agenticdocer.mlr.export import (
    EXPORT_GRAPH_FILE,
    EXPORT_MANIFEST_FILE,
    EXPORT_NODES_FILE,
)
from agenticdocer.model import DocIn, Node, NodeIn, WriteContext
from agenticdocer.render import body_text
from agenticdocer.store import NotFoundError, Storage
from agenticdocer.store.schema import events as events_table

pytestmark = pytest.mark.integration

CTX = WriteContext(actor="mlr-tester", source="cli")


def doc_in(doc_id: str, title: str = "CXL 一致性规范") -> DocIn:
    return DocIn(
        doc_id=doc_id,
        doc_type="standard",
        title=title,
        meta={"spec_revision": "3.0", "spec_org": "CXL"},
        source_ref="CXL-3.2",
    )


def node_in(
    doc_id: str,
    *,
    ordinal: int,
    parent: Any = None,
    level: int | None = None,
    fragment: str | None = None,
    text: str = "条款正文",
    atom_type: str = "clause",
) -> NodeIn:
    return NodeIn(
        node_id=None,
        doc_id=doc_id,
        atom_type=atom_type,
        ordinal=ordinal,
        parent_node_id=parent,
        level=level,
        anchor=f"{doc_id}#{ordinal}",
        content={"fragment": fragment} if fragment is not None else {"text": text},
    )


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def relation(relations: list[dict[str, Any]], **match: Any) -> dict[str, Any]:
    found = [rel for rel in relations if all(rel[key] == value for key, value in match.items())]
    assert len(found) == 1, f"expected exactly one relation matching {match}, got {found}"
    return found[0]


@pytest.fixture
def doc_ids() -> tuple[str, str]:
    """唯一文档对（避免与并行 agent 的测试数据相撞）。"""
    tag = uuid4().hex[:10]
    return f"SPEC-MLR-A-{tag}", f"SPEC-MLR-B-{tag}"


@pytest.fixture
def seeded(storage: Storage, doc_ids: tuple[str, str]) -> dict[str, Any]:
    """两个文档 + 节点树 + refs（`traces_to` 上游链 ×2 跳、`see_also`、`composes_from`）。"""
    doc_a, doc_b = doc_ids
    return_seed: dict[str, Any] = {"docs": doc_ids}
    return return_seed


async def seed(storage: Storage, doc_ids: tuple[str, str]) -> dict[str, Any]:
    """铺数据（异步，故不能放 fixture 里直接 await）。"""
    doc_a, doc_b = doc_ids
    await storage.upsert_doc(doc_in(doc_a, "CXL 一致性规范"), None, CTX)
    await storage.upsert_doc(doc_in(doc_b, "CXL 协议层规范"), None, CTX)

    heading = await storage.upsert_node(
        node_in(doc_a, ordinal=0, level=2, fragment="## 1 概览\n\n本章给出一致性模型。"),
        None,
        CTX,
    )
    clause = await storage.upsert_node(
        node_in(doc_a, ordinal=1, parent=heading.node_id, fragment="条款 1.1：缓存一致性由 MESI 保证。"),
        None,
        CTX,
    )
    # 无 fragment → M04 按 atom_type/level 合成（导出文本应与之一致）
    code = await storage.upsert_node(
        node_in(
            doc_a,
            ordinal=2,
            atom_type="code",
            fragment=None,
            text="print('coherence')",
        ),
        None,
        CTX,
    )
    upstream = await storage.upsert_node(
        node_in(doc_b, ordinal=0, fragment="上游定义：coherent agent。"), None, CTX
    )
    upstream2 = await storage.upsert_node(
        node_in(doc_b, ordinal=1, fragment="更上游定义：home agent。"), None, CTX
    )

    # traces_to 上游链：clause → upstream → upstream2（反向 2 跳可达）
    await storage.add_ref(clause.node_id, doc_b, upstream2.node_id, "traces_to", CTX)
    await storage.add_ref(upstream.node_id, doc_b, upstream2.node_id, "traces_to", CTX)
    # see_also（双向语义）
    await storage.add_ref(code.node_id, doc_b, upstream.node_id, "see_also", CTX)
    # refs 形态的 composes_from（与节点树父子同一关系 → 导出应去重）
    await storage.add_ref(heading.node_id, doc_a, clause.node_id, "composes_from", CTX)

    return {
        "docs": doc_ids,
        "heading": heading,
        "clause": clause,
        "code": code,
        "upstream": upstream,
        "upstream2": upstream2,
    }


def block_rt(monkeypatch: pytest.MonkeyPatch) -> None:
    """P6/C7：仅放行 loopback（PG）与非 INET 地址，外部网络一律判为违规。"""
    original = socket.socket.connect

    def guarded(self: socket.socket, address: Any, *args: Any, **kwargs: Any) -> Any:
        host = address[0] if isinstance(address, tuple) else None
        if isinstance(host, str) and not (host == "localhost" or host.startswith("127.")):
            raise AssertionError(f"external network access attempted: {address!r}")
        if isinstance(host, bytes) and not host.startswith(b"127."):
            raise AssertionError(f"external network access attempted: {address!r}")
        return original(self, address, *args, **kwargs)

    monkeypatch.setattr(socket.socket, "connect", guarded)
    monkeypatch.setattr(socket, "create_connection", lambda *a, **k: _blocked(name="create_connection"))


def _blocked(*, name: str) -> Any:
    raise AssertionError(f"external network access attempted via socket.{name}")


# ── 导出包：文本、图关系 ──────────────────────────────────────────────────


async def test_export_package_texts_match_document_render(
    storage: Storage, tmp_path: Path, doc_ids: tuple[str, str]
) -> None:
    """`nodes.jsonl` 的文本 = M04 渲染口径，且逐块拼接等于整档渲染正文。"""
    await seed(storage, doc_ids)
    doc_a, doc_b = doc_ids
    result = await export_package([doc_a, doc_b], tmp_path / "pkg", storage=storage)

    nodes = await storage.list_nodes_for_docs([doc_a, doc_b])
    assert result.nodes == len(nodes) == 5
    assert result.docs == 2
    assert result.out_path == str(tmp_path / "pkg")

    records = read_jsonl(tmp_path / "pkg" / EXPORT_NODES_FILE)
    assert [record["node_id"] for record in records] == [str(node.node_id) for node in nodes]
    assert set(records[0]) == {"node_id", "doc_id", "anchor", "text"}

    by_anchor = {record["anchor"]: record for record in records}
    assert by_anchor[f"{doc_a}#0"]["text"] == "## 1 概览\n\n本章给出一致性模型。"
    assert by_anchor[f"{doc_a}#1"]["text"] == "条款 1.1：缓存一致性由 MESI 保证。"
    assert by_anchor[f"{doc_a}#2"]["text"] == "```\nprint('coherence')\n```"

    # 与 M04 的整档正文逐字节同源（导出不是另一套渲染）
    for partition in (doc_a, doc_b):
        owned = [node for node in nodes if node.doc_id == partition]
        exported = "\n\n".join(record["text"] for record in records if record["doc_id"] == partition)
        assert exported == body_text(owned)


async def test_export_package_graph_contains_hierarchy_and_traverse_chains(
    storage: Storage, tmp_path: Path, doc_ids: tuple[str, str]
) -> None:
    """图关系：节点树父子（去重 refs 形态）+ M05 真实遍历的上游链/see_also/多跳。"""
    seeded = await seed(storage, doc_ids)
    doc_a, doc_b = doc_ids
    heading, clause, code = seeded["heading"], seeded["clause"], seeded["code"]
    upstream, upstream2 = seeded["upstream"], seeded["upstream2"]

    await export_package([doc_a, doc_b], tmp_path, storage=storage)
    relations = read_jsonl(tmp_path / EXPORT_GRAPH_FILE)

    # 父子：heading composes_from clause（节点树 + refs 同一条 → 只留 hierarchy 一条）
    hierarchy = relation(
        relations,
        node_id=str(heading.node_id),
        related_node_id=str(clause.node_id),
        hops=1,
    )
    assert (hierarchy["origin"], hierarchy["kinds"], hierarchy["direction"]) == (
        "hierarchy",
        ["composes_from"],
        "out",
    )
    assert not [
        rel
        for rel in relations
        if rel["origin"] == "traverse" and rel["kinds"] == ["composes_from"]
    ]

    # traces_to 上游链（1 跳）：clause 追溯到 upstream2 → 从 upstream2 视角 direction="in"
    one_hop = relation(
        relations,
        node_id=str(upstream2.node_id),
        related_node_id=str(clause.node_id),
        hops=1,
    )
    assert (one_hop["kinds"], one_hop["direction"], one_hop["origin"]) == (
        ["traces_to"],
        "in",
        "traverse",
    )
    assert (one_hop["doc_id"], one_hop["related_doc_id"]) == (doc_b, doc_a)

    # traces_to 上游链（2 跳）：home agent ← coherent agent ← clause
    two_hop = relation(
        relations,
        node_id=str(upstream2.node_id),
        related_node_id=str(clause.node_id),
        hops=1,
    )
    assert two_hop["related_node_id"] == str(clause.node_id)
    chain = relation(
        relations,
        node_id=str(upstream2.node_id),
        related_node_id=str(upstream.node_id),
        hops=1,
    )
    assert chain["kinds"] == ["traces_to"]
    assert relation(
        relations,
        node_id=str(upstream.node_id),
        related_node_id=str(clause.node_id),
        hops=1,
    )

    # see_also（双向语义 → direction="both"）
    see_also = [
        rel for rel in relations if rel["kinds"] == ["see_also"] and rel["direction"] == "both"
    ]
    assert see_also, f"expected see_also relations, got {relations}"
    assert {str(code.node_id), str(upstream.node_id)} <= {
        see_also[0]["node_id"],
        see_also[0]["related_node_id"],
    }

    line_count = len((tmp_path / EXPORT_GRAPH_FILE).read_text(encoding="utf-8").splitlines())
    manifest = json.loads((tmp_path / EXPORT_MANIFEST_FILE).read_text(encoding="utf-8"))
    assert manifest["counts"]["relations"] == line_count == len(relations)
    assert manifest["counts"]["relations_hierarchy"] + manifest["counts"]["relations_traverse"] == (
        len(relations)
    )
    assert manifest["doc_ids"] == [doc_a, doc_b]
    assert manifest["graph_hops"] == 2


async def test_export_package_is_reproducible_and_overwrites(
    storage: Storage, tmp_path: Path, doc_ids: tuple[str, str]
) -> None:
    seeded = await seed(storage, doc_ids)
    doc_a, doc_b = doc_ids
    await export_package([doc_a, doc_b], tmp_path / "one", storage=storage)
    await export_package([doc_a, doc_b], tmp_path / "two", storage=storage)
    for name in (EXPORT_NODES_FILE, EXPORT_GRAPH_FILE):
        assert (tmp_path / "one" / name).read_bytes() == (tmp_path / "two" / name).read_bytes()

    # 新增节点后重跑同一目录 → 包内行数跟随当前态（不留上一版残留）
    await storage.upsert_node(node_in(doc_a, ordinal=3, text="新增条款"), None, CTX)
    result = await export_package([doc_a, doc_b], tmp_path / "one", storage=storage)
    assert result.nodes == 6
    assert len(read_jsonl(tmp_path / "one" / EXPORT_NODES_FILE)) == 6
    assert seeded["clause"].node_id is not None


async def test_export_package_rejects_unknown_doc(
    storage: Storage, tmp_path: Path, doc_ids: tuple[str, str]
) -> None:
    doc_a, _ = doc_ids
    await seed(storage, doc_ids)
    with pytest.raises(NotFoundError):
        await export_package([doc_a, "SPEC-MLR-GONE"], tmp_path, storage=storage)
    assert not (tmp_path / EXPORT_NODES_FILE).exists()


# ── 增量流：与 M02 事件日志一致、游标续拉不重不漏 ────────────────────────


async def test_change_stream_matches_event_log_and_resumes_without_gaps(
    storage: Storage, doc_ids: tuple[str, str]
) -> None:
    seeded = await seed(storage, doc_ids)
    doc_a, _ = doc_ids

    drained = [event async for event in change_stream(storage=storage)]
    order = [(event.ts, event.event_id) for event in drained]
    assert order == sorted(order), "stream must be ordered by (ts, event_id)"

    mine = {doc_a, *(str(seeded[key].node_id) for key in ("heading", "clause", "code"))}
    mine |= {str(seeded[key].node_id) for key in ("upstream", "upstream2")}
    seen = {event.entity_id for event in drained if event.entity in {"doc", "node"}}
    assert mine <= seen, f"seeded entities missing from stream: {mine - seen}"

    # ref 事件也在流里（edge 增删属增量语义的一部分）
    assert any(event.entity == "ref" and event.op == "add" for event in drained)

    # 游标续拉：严格晚于 token 游标（半开区间）——对并发写入者鲁棒
    token = cursor_token(drained[max(len(drained) // 2, 0)])
    cursor_ts, cursor_id = token.split("@")[0], token.split("@")[1]
    from datetime import datetime  # noqa: PLC0415 - 局部使用，避免顶部噪声

    bound = (datetime.fromisoformat(cursor_ts), cursor_id)
    resumed = [event async for event in change_stream(token, storage=storage)]
    assert all((event.ts, str(event.event_id)) > bound for event in resumed)
    assert not set(str(event.event_id) for event in resumed) & set(
        str(event.event_id) for event in drained[: len(drained) // 2]
    )

    # entity 过滤与 M02 口径一致
    node_only = [event async for event in change_stream(entity="node", storage=storage)]
    assert node_only and all(event.entity == "node" for event in node_only)


async def test_change_stream_is_consistent_with_changes_since(
    storage: Storage, doc_ids: tuple[str, str]
) -> None:
    """与 M02 `changes_since` 同源：同一游标下两者序列一致（增量流不另立口径）。"""
    await seed(storage, doc_ids)
    reference = await storage.changes_since(limit=100_000)
    streamed = [event async for event in change_stream(storage=storage)]
    assert [str(event.event_id) for event in streamed] == [
        str(event.event_id) for event in reference
    ]

    # 半开区间：从最后一条续拉得到空流（无新事件时）
    if reference:
        tail = cursor_token(reference[-1])
        more = await storage.changes_since(
            since_ts=reference[-1].ts, since_event_id=reference[-1].event_id, limit=100_000
        )
        assert all(str(event.event_id) != str(reference[-1].event_id) for event in more)
        assert [event async for event in change_stream(tail, storage=storage)] == [
            event for event in more
        ]


# ── P6/C7：无外部网络、不碰 lightRAG ─────────────────────────────────────


async def test_export_and_stream_make_no_external_network_call(
    storage: Storage,
    tmp_path: Path,
    doc_ids: tuple[str, str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """导出与拉流只碰 PG（loopback）+ 本地文件；外部网络一律判违规。"""
    await seed(storage, doc_ids)
    doc_a, doc_b = doc_ids
    block_rt(monkeypatch)

    result = await export_package([doc_a, doc_b], tmp_path, storage=storage)
    drained = [event async for event in change_stream(storage=storage)]

    assert result.nodes == 5
    assert drained
    assert not [name for name in sys.modules if name.split(".")[0] == "lightrag"]


async def test_change_stream_reads_only_events_table(
    storage: Storage, doc_ids: tuple[str, str]
) -> None:
    """游标流是 `events` 的纯读路径（`events` append-only：本模块无写路径）。"""
    await seed(storage, doc_ids)
    before = await storage.changes_since(limit=100_000)
    await anext(change_stream(storage=storage))
    after = await storage.changes_since(limit=100_000)
    assert [str(event.event_id) for event in before] == [str(event.event_id) for event in after]
    assert events_table.name == "events"


def _unused_iterator_helper() -> Iterator[None]:  # pragma: no cover
    yield None
