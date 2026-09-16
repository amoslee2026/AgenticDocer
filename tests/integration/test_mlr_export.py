"""M-LR 集成测试：真实 PostgreSQL（`DATABASE_URL`）+ 真实 M02/M04/M05。

不需要运行的场景（无 PG / 无凭据）由 `conftest.py` 整体 skip，不会 fail。

覆盖：

* 导出包端到端——`nodes.jsonl` 文本与 **M04 整档渲染正文**同源（同一库读路径）；
* `graph.jsonl` 含节点树父子与 **M05 `traverse` 真实遍历**得到的 `traces_to` 上游链
  （1 跳 + 2 跳）、``see_also``；refs 形态的 `composes_from` 与节点树父子**去重**；
* 包的确定性（同状态两次导出 `nodes.jsonl`/`graph.jsonl` 逐字节一致）与覆盖写；
* 增量流与 M02 事件日志**同源**（同一游标下序列一致）且游标 token 续拉为半开区间
  （断言只依赖「严格晚于游标」，故对并行写入者鲁棒）；
* P6/C7：导出与拉流过程**无外部网络**（socket 层断言，放行 loopback 上的 PG）、不触碰 lightRAG。

测试数据用唯一 `doc_id` 前缀（`SPEC-MLR-<hex>`），本文件自身不清表、不 drop schema；但共享
`conftest.py` 的 session 级 `migrated_schema` 会 `DROP SCHEMA public CASCADE` + `alembic
upgrade`——故**需独占库**，或以隔离库运行（`TEST_DATABASE_URL=<独立库>`；本次即如此验证）。
"""

from __future__ import annotations

import json
import socket
import sys
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest
from sqlalchemy import text

from agenticdocer.mlr import change_stream, cursor_token, export_package
from agenticdocer.mlr.export import (
    EXPORT_GRAPH_FILE,
    EXPORT_MANIFEST_FILE,
    EXPORT_NODES_FILE,
)
from agenticdocer.model import DocIn, NodeIn, WriteContext
from agenticdocer.render import body_text
from agenticdocer.store import NotFoundError, Storage

pytestmark = pytest.mark.integration

CTX = WriteContext(actor="mlr-tester", source="cli")


# ── 铺数据 ────────────────────────────────────────────────────────────────


def doc_in(doc_id: str, title: str) -> DocIn:
    return DocIn(
        doc_id=doc_id,
        doc_type="standard",
        title=title,
        meta={"spec_revision": "3.2", "spec_org": "CXL"},
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


@pytest.fixture
def doc_ids() -> tuple[str, str]:
    """唯一文档对（避开并行 agent 的测试数据）。"""
    tag = uuid4().hex[:10]
    return f"SPEC-MLR-A-{tag}", f"SPEC-MLR-B-{tag}"


async def seed(storage: Storage, doc_ids: tuple[str, str]) -> dict[str, Any]:
    """两文档 + 节点树 + refs。

    ``traces_to`` 链（有向边 ``src → dst``）：``clause → mid → top``——故 ``top`` 反向
    （"up"）1 跳可达 ``mid``、2 跳可达 ``clause``。
    """
    doc_a, doc_b = doc_ids
    await storage.upsert_doc(doc_in(doc_a, "CXL 一致性规范"), None, CTX)
    await storage.upsert_doc(doc_in(doc_b, "CXL 协议层规范"), None, CTX)

    heading = await storage.upsert_node(
        node_in(doc_a, ordinal=0, level=2, fragment="## 1 概览\n\n本章给出一致性模型。"), None, CTX
    )
    clause = await storage.upsert_node(
        node_in(doc_a, ordinal=1, parent=heading.node_id, fragment="条款 1.1：一致性由 MESI 保证。"),
        None,
        CTX,
    )
    # 无 fragment → M04 按 atom_type 合成（导出文本应与之一致）
    code = await storage.upsert_node(
        node_in(doc_a, ordinal=2, atom_type="code", fragment=None, text="print('coherent')"),
        None,
        CTX,
    )
    mid = await storage.upsert_node(
        node_in(doc_b, ordinal=0, fragment="上游定义：coherent agent。"), None, CTX
    )
    top = await storage.upsert_node(
        node_in(doc_b, ordinal=1, fragment="更上游定义：home agent。"), None, CTX
    )

    await storage.add_ref(clause.node_id, doc_b, mid.node_id, "traces_to", CTX)
    await storage.add_ref(mid.node_id, doc_b, top.node_id, "traces_to", CTX)
    await storage.add_ref(code.node_id, doc_b, mid.node_id, "see_also", CTX)
    # refs 形态的 composes_from：与节点树父子是同一条关系 → 导出应去重
    await storage.add_ref(heading.node_id, doc_a, clause.node_id, "composes_from", CTX)

    return {"heading": heading, "clause": clause, "code": code, "mid": mid, "top": top}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def only(relations: list[dict[str, Any]], **match: Any) -> dict[str, Any]:
    """断言恰好一条关系命中给定字段。"""
    found = [rel for rel in relations if all(rel[key] == value for key, value in match.items())]
    assert len(found) == 1, f"expected exactly one relation matching {match}, got {found}"
    return found[0]


def block_external_network(monkeypatch: pytest.MonkeyPatch) -> list[Any]:
    """P6/C7：放行 loopback（PG）与非 INET 地址，外部网络一律判违规。

    返回已被拦截的连接地址清单——调用方据此断言**守卫确实被触发过**（否则「无外部网络」
    的断言是空的）。
    """
    original_connect = socket.socket.connect
    seen: list[Any] = []

    def guarded_connect(self: socket.socket, address: Any, *args: Any, **kwargs: Any) -> Any:
        seen.append(address)
        host = address[0] if isinstance(address, tuple) else None
        if isinstance(host, bytes):
            host = host.decode()
        if isinstance(host, str) and host != "localhost" and not host.startswith("127."):
            raise AssertionError(f"external network access attempted: {address!r}")
        return original_connect(self, address, *args, **kwargs)

    def blocked(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("external network access attempted via socket.create_connection")

    monkeypatch.setattr(socket.socket, "connect", guarded_connect)
    monkeypatch.setattr(socket, "create_connection", blocked)
    return seen


# ── 导出包：文本与 M04 同源 ───────────────────────────────────────────────


async def test_export_package_texts_match_document_render(
    storage: Storage, tmp_path: Path, doc_ids: tuple[str, str]
) -> None:
    await seed(storage, doc_ids)
    doc_a, doc_b = doc_ids
    result = await export_package([doc_a, doc_b], tmp_path / "pkg", storage=storage)

    nodes = await storage.list_nodes_for_docs([doc_a, doc_b])
    assert (result.out_path, result.docs, result.nodes) == (str(tmp_path / "pkg"), 2, len(nodes))
    assert len(nodes) == 5

    records = read_jsonl(tmp_path / "pkg" / EXPORT_NODES_FILE)
    assert [record["node_id"] for record in records] == [str(node.node_id) for node in nodes]
    assert set(records[0]) == {"node_id", "doc_id", "anchor", "text"}

    by_anchor = {record["anchor"]: record["text"] for record in records}
    assert by_anchor[f"{doc_a}#0"] == "## 1 概览\n\n本章给出一致性模型。"
    assert by_anchor[f"{doc_a}#1"] == "条款 1.1：一致性由 MESI 保证。"
    assert by_anchor[f"{doc_a}#2"] == "```\nprint('coherent')\n```"

    # 与 M04 的整档渲染正文逐字节同源（导出不是另一套渲染口径）
    for partition in (doc_a, doc_b):
        owned = [node for node in nodes if node.doc_id == partition]
        exported = "\n\n".join(
            record["text"] for record in records if record["doc_id"] == partition
        )
        assert exported == body_text(owned)


# ── 导出包：图关系（父子 + M05 遍历） ─────────────────────────────────────


async def test_export_package_graph_has_hierarchy_and_traverse_chains(
    storage: Storage, tmp_path: Path, doc_ids: tuple[str, str]
) -> None:
    seeded = await seed(storage, doc_ids)
    doc_a, doc_b = doc_ids
    heading, clause, code = seeded["heading"], seeded["clause"], seeded["code"]
    mid, top = seeded["mid"], seeded["top"]

    await export_package([doc_a, doc_b], tmp_path, storage=storage)
    relations = read_jsonl(tmp_path / EXPORT_GRAPH_FILE)

    # 节点树父子：heading（父/整体）composes_from clause（子/部分）
    hierarchy = only(
        relations, node_id=str(heading.node_id), related_node_id=str(clause.node_id), hops=1
    )
    assert (hierarchy["origin"], hierarchy["kinds"], hierarchy["direction"]) == (
        "hierarchy",
        ["composes_from"],
        "out",
    )
    # refs 形态的 composes_from 与之重复 → 只留 hierarchy 一条
    assert len([rel for rel in relations if rel["kinds"] == ["composes_from"]]) == 1

    # traces_to 上游链（1 跳）：从 top 反向可达 mid
    one_hop = only(relations, node_id=str(top.node_id), related_node_id=str(mid.node_id), hops=1)
    assert (one_hop["kinds"], one_hop["direction"], one_hop["origin"]) == (
        ["traces_to"],
        "in",
        "traverse",
    )
    assert (one_hop["doc_id"], one_hop["related_doc_id"]) == (doc_b, doc_b)

    # traces_to 上游链（2 跳，默认 hops=2）：从 top 反向可达 clause，方向为多跳路径
    two_hop = only(relations, node_id=str(top.node_id), related_node_id=str(clause.node_id), hops=2)
    assert (two_hop["kinds"], two_hop["direction"]) == (["traces_to", "traces_to"], None)
    assert (two_hop["doc_id"], two_hop["related_doc_id"]) == (doc_b, doc_a)

    # see_also（双向语义）：两侧各一条，direction="both"
    see_also = [rel for rel in relations if rel["kinds"] == ["see_also"]]
    assert {(rel["direction"], rel["hops"]) for rel in see_also} == {("both", 1)}
    assert {(rel["node_id"], rel["related_node_id"]) for rel in see_also} == {
        (str(code.node_id), str(mid.node_id)),
        (str(mid.node_id), str(code.node_id)),
    }

    # 包内计数与文件行数一致
    manifest = json.loads((tmp_path / EXPORT_MANIFEST_FILE).read_text(encoding="utf-8"))
    assert manifest["counts"]["relations"] == len(relations)
    assert (
        manifest["counts"]["relations_hierarchy"] + manifest["counts"]["relations_traverse"]
        == len(relations)
    )
    assert manifest["counts"]["relations_hierarchy"] == 1
    assert manifest["doc_ids"] == [doc_a, doc_b]
    assert manifest["graph_hops"] == 2
    assert manifest["counts"]["nodes"] == 5


async def test_export_package_graph_hops_one_excludes_two_hop_chains(
    storage: Storage, tmp_path: Path, doc_ids: tuple[str, str]
) -> None:
    """`hops=1` 只给 1 跳可达关系（2 跳链不出现）——跳数参数确实透传到 M05。"""
    seeded = await seed(storage, doc_ids)
    doc_a, doc_b = doc_ids
    await export_package([doc_a, doc_b], tmp_path, storage=storage, hops=1)
    relations = read_jsonl(tmp_path / EXPORT_GRAPH_FILE)
    assert not [rel for rel in relations if rel["hops"] > 1]
    assert only(
        relations,
        node_id=str(seeded["top"].node_id),
        related_node_id=str(seeded["mid"].node_id),
        hops=1,
    )
    assert not [
        rel
        for rel in relations
        if rel["related_node_id"] == str(seeded["clause"].node_id)
        and rel["node_id"] == str(seeded["top"].node_id)
    ]


# ── 导出包：确定性、覆盖、错误 ────────────────────────────────────────────


async def test_export_package_is_reproducible_and_overwrites(
    storage: Storage, tmp_path: Path, doc_ids: tuple[str, str]
) -> None:
    await seed(storage, doc_ids)
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


async def test_export_package_rejects_unknown_doc(
    storage: Storage, tmp_path: Path, doc_ids: tuple[str, str]
) -> None:
    doc_a, _ = doc_ids
    await seed(storage, doc_ids)
    with pytest.raises(NotFoundError):
        await export_package([doc_a, "SPEC-MLR-GONE"], tmp_path, storage=storage)
    assert not (tmp_path / EXPORT_NODES_FILE).exists()


# ── 增量流：与 M02 事件日志同源、游标续拉 ─────────────────────────────────


async def test_change_stream_matches_changes_since_and_resumes_half_open(
    storage: Storage, doc_ids: tuple[str, str]
) -> None:
    seeded = await seed(storage, doc_ids)
    doc_a, doc_b = doc_ids

    reference = await storage.changes_since(limit=100_000)
    drained = [event async for event in change_stream(storage=storage)]
    order = [(event.ts, event.event_id) for event in drained]
    assert order == sorted(order), "stream must be ordered by (ts, event_id)"
    # 流与 M02 同源；并行写入者可能追加事件 → 以 reference 为前缀比对
    assert [str(event.event_id) for event in drained[: len(reference)]] == [
        str(event.event_id) for event in reference
    ]

    # 种子数据都出现在流里（doc/node/ref 三类增量）
    seeded_ids = {doc_a, doc_b, *(str(node.node_id) for node in seeded.values())}
    assert seeded_ids <= {event.entity_id for event in drained}
    assert any(event.entity == "ref" and event.op == "add" for event in drained)

    # 游标续拉：严格晚于 token（半开区间，不重）
    token_event = drained[max(len(drained) // 2, 0)]
    bound = (token_event.ts, str(token_event.event_id))
    resumed = [event async for event in change_stream(cursor_token(token_event), storage=storage)]
    assert all((event.ts, str(event.event_id)) > bound for event in resumed)

    # entity 过滤与 M02 同口径
    node_only = [event async for event in change_stream(entity="node", storage=storage)]
    assert node_only and all(event.entity == "node" for event in node_only)

# ── P6/C7：无外部网络、不触碰 lightRAG ───────────────────────────────────


async def test_export_and_stream_need_no_external_network(
    storage: Storage,
    tmp_path: Path,
    doc_ids: tuple[str, str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """导出与拉流只碰 PG（loopback）+ 本地文件；外部网络一律判违规。"""
    doc_a, doc_b = doc_ids
    # 守卫须在**首次连库之前**装好（连接池一建立就不再新建连接 → 否则是空断言）
    seen = block_external_network(monkeypatch)
    await seed(storage, doc_ids)

    result = await export_package([doc_a, doc_b], tmp_path, storage=storage)
    drained = [event async for event in change_stream(storage=storage)]

    assert result.nodes == 5
    assert drained
    # 守卫确实拦到了 PG 连接（否则「无外部网络」是空断言）
    assert seen, "network guard was never exercised"
    hosts = {address[0] for address in seen if isinstance(address, tuple)}
    assert hosts and all(host.startswith("127.") or host == "localhost" for host in hosts)
    assert not [name for name in sys.modules if name.split(".")[0] == "lightrag"]


async def test_export_and_stream_write_no_database_rows(
    storage: Storage, tmp_path: Path, doc_ids: tuple[str, str]
) -> None:
    """C7：导出与拉流是**纯读路径**——实体表与 `events` 行数不变（不摄入、不记账）。"""
    await seed(storage, doc_ids)
    doc_a, doc_b = doc_ids
    before = await _row_counts(storage)

    await export_package([doc_a, doc_b], tmp_path, storage=storage)
    [event async for event in change_stream(storage=storage)]

    assert await _row_counts(storage) == before


async def _row_counts(storage: Storage) -> dict[str, int]:
    counts: dict[str, int] = {}
    for table in ("docs", "nodes", "refs", "events", "comments"):
        async with storage.db.session() as session:
            counts[table] = (await session.execute(text(f"SELECT count(*) FROM {table}"))).scalar_one()
    return counts
