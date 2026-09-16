"""M05 集成测试：**真实 PG**（`importer.parse_markdown` + `commit_document` 铺数据 → 真库 refs 图 + FTS）。

覆盖：

- 四种 kind 的方向/跳数截断在真库成立（REQ-M05-F01：`traces_to` 2 跳、`composes_from`/`see_also`
  1 跳、`source_ref` 从不参与）；
- 去重保留最短路径、排序（跳数 → doc 序 → ordinal）、起点不入结果；
- 软删过滤（L5）、文档级引用与悬空边的丢弃（M09B `broken_refs` 口径）；
- **分区（ADR-009 V16）**：`EXPLAIN` 实测「带 doc_id 只扫 1 个分区 / 不带扫全部 64 个」；
  带与不带 `doc_id` 结果一致（含跨文档边的正向与逆向）；
- FTS（ADR-005）：真实语料命中带 `score`、相关度排序、`limit`、deleted 过滤、空查询短路。

`conftest.py` 在 PG 不可用时整体 skip（无库环境仍全绿）。
"""

from __future__ import annotations

import json
import pathlib
import re

import pytest
from sqlalchemy import text

from agenticdocer.importer import commit_document, parse_markdown
from agenticdocer.model import Node, WriteContext, new_uuid7
from agenticdocer.retrieve import search_text, traverse
from agenticdocer.store import NotFoundError, Storage, ValidationError

pytestmark = pytest.mark.integration

ROOT = pathlib.Path(__file__).resolve().parents[2]
CORPUS = ROOT / "spec" / "standards"
CTX = WriteContext(actor="tester", source="importer")

_ENTITY_TABLES = ("comments", "refs", "nodes", "docs", "assets")
_SECTIONS = ("概述", "细节", "接口", "时序", "附录", "术语", "错误处理")


async def count(database, sql: str, **params) -> int:
    async with database.session() as session:
        return int((await session.execute(text(sql), params)).scalar_one())


@pytest.fixture(autouse=True)
async def clean_database(database):
    """每个用例前清空实体表（起点为空库，断言不依赖其它用例）。

    `events` 对应用角色 append-only（A15 库层强制），故不可清——本文件的断言只看当前态
    （nodes/refs），不需要事件增量。
    """
    async with database.transaction() as session:
        for table in _ENTITY_TABLES:
            await session.execute(text(f"DELETE FROM {table}"))
    return database


def synthetic_document(spec_id: str) -> str:
    """合成标准文档：1 个 level-1 + 7 个 level-2 条款（8 个 clause，供四类 kind 分用）。"""
    body = "\n".join(
        f"## 1.{index} {name}\n\n{name}正文。\n" for index, name in enumerate(_SECTIONS, 1)
    )
    return f"""---
title: 遍历与检索测试规范
type: composite
purpose: spec
audience: both
direction: input
status: approved
version: "1.0.0"
section_meta: "@meta"
spec_id: {spec_id}
spec_type: standard
spec_org: TEST
spec_revision: "1.0"
source: corpus/01_raw/specifications/test/traverse.pdf
converted_by: mineru
converted_at: 2026-08-31
reviewed_by: tester
reviewed_at: 2026-08-31
---

# 1 总则

总则正文。

{body}"""


async def import_synthetic(
    storage: Storage, tmp_path: pathlib.Path, spec_id: str
) -> tuple[str, list[Node]]:
    """写盘 → `parse_markdown` → `commit_document`，返回 `(doc_id, 按 ordinal 序的 clause 节点)`。"""
    source = tmp_path / f"{spec_id}.md"
    source.write_text(synthetic_document(spec_id), encoding="utf-8")
    result = parse_markdown(source)
    outcome = await commit_document(result, CTX, storage=storage)
    nodes = [
        node for node in await storage.get_doc_nodes(outcome.doc_id) if node.atom_type == "clause"
    ]
    assert len(nodes) == len(_SECTIONS) + 1, "合成文档应产出 8 个 clause 节点"
    return outcome.doc_id, nodes


async def link(storage: Storage, src: Node, dst: Node, kind: str) -> None:
    """节点级建边（`src` 携带 ref，`dst` 为被引用节点）。"""
    await storage.add_ref(src.node_id, dst.doc_id, dst.node_id, kind, CTX)  # type: ignore[arg-type]


def as_tuples(hits) -> list[tuple[object, int, list[str]]]:
    return [(hit.node_id, hit.hops, hit.via) for hit in hits]


# ── kind 规则（方向 / 跳数截断 / via）───────────────────────────────────


async def test_traverse_kind_rules_on_real_graph(
    storage: Storage, database, tmp_path: pathlib.Path
) -> None:
    """四类 kind 的方向与跳数截断在真库成立。"""
    doc_id, nodes = await import_synthetic(storage, tmp_path, "SPEC-STD-TRAV-1.0")
    n1, n2, n3, n4, n5, n6, n7, n8 = nodes

    await link(storage, n1, n2, "traces_to")
    await link(storage, n2, n3, "traces_to")  # traces_to 链：n1 → n2 → n3
    await link(storage, n4, n5, "composes_from")
    await link(storage, n5, n6, "composes_from")  # composes_from 链：n4 → n5 → n6
    await link(storage, n7, n8, "see_also")
    await link(storage, n8, n1, "source_ref")  # 叶引用：不参与遍历

    # traces_to：up（dst→src）2 跳，`via` 记录最短路径的 kind 序列
    one = await traverse(n3.node_id, 1, doc_id=doc_id, storage=storage)
    assert as_tuples(one) == [(n2.node_id, 1, ["traces_to"])]
    two = await traverse(n3.node_id, 2, doc_id=doc_id, storage=storage)
    assert as_tuples(two) == [
        (n2.node_id, 1, ["traces_to"]),
        (n1.node_id, 2, ["traces_to", "traces_to"]),
    ]
    assert n3.node_id not in {hit.node_id for hit in two}, "起点自身不入结果"
    assert as_tuples(await traverse(n3.node_id, 9, doc_id=doc_id, storage=storage)) == as_tuples(
        two
    ), "超过 MAX_HOPS 无额外命中"

    # composes_from：down（src→dst）1 跳，hops=2 也不得扩到 n6
    assert as_tuples(await traverse(n4.node_id, 2, doc_id=doc_id, storage=storage)) == [
        (n5.node_id, 1, ["composes_from"])
    ]
    assert as_tuples(await traverse(n5.node_id, 1, doc_id=doc_id, storage=storage)) == [
        (n6.node_id, 1, ["composes_from"])
    ]

    # see_also：双向 1 跳
    assert [hit.node_id for hit in await traverse(n7.node_id, 1, doc_id=doc_id, storage=storage)] == [
        n8.node_id
    ]
    assert [hit.node_id for hit in await traverse(n8.node_id, 1, doc_id=doc_id, storage=storage)] == [
        n7.node_id
    ]

    # source_ref（n8 → n1）从不参与：src 侧与 dst 侧、任何跳数都不可达
    assert await traverse(n1.node_id, 2, doc_id=doc_id, storage=storage) == []
    assert [
        hit.node_id for hit in await traverse(n8.node_id, 9, doc_id=doc_id, storage=storage)
    ] == [n7.node_id], "n8 的 source_ref 出边不得被跟随"
    assert (
        await count(database, "SELECT count(*) FROM refs WHERE kind = 'source_ref'") == 1
    ), "source_ref 边存在但不可达 → 证明是遍历规则而非边缺失"

    # 结果类型契约（§3.0 TraversalHit）
    assert two[0].doc_id == doc_id and two[0].anchor == n2.anchor


async def test_traverse_dedup_and_ordering_across_documents(
    storage: Storage, tmp_path: pathlib.Path
) -> None:
    """去重保留最短路径 + 排序 = 跳数 → doc 序 → ordinal（跨文档）。"""
    doc_a, nodes_a = await import_synthetic(storage, tmp_path, "SPEC-STD-TRAV-A")
    doc_b, nodes_b = await import_synthetic(storage, tmp_path, "SPEC-STD-TRAV-B")
    hub, second, far = nodes_a[0], nodes_a[1], nodes_a[2]

    await link(storage, second, hub, "see_also")  # hub 的 1 跳（双向入边）
    await link(storage, far, hub, "see_also")  # hub 的 1 跳
    await link(storage, nodes_b[1], hub, "see_also")  # doc_b[1]：1 跳可达
    await link(storage, nodes_b[0], far, "traces_to")  # doc_b[0]：经 far 的 2 跳
    await link(storage, nodes_b[1], far, "traces_to")  # 同一节点 2 跳亦可达 → 必须保留 1 跳

    hits = await traverse(hub.node_id, 2, doc_id=doc_a, storage=storage)
    assert [(hit.doc_id, hit.hops) for hit in hits] == [
        (doc_a, 1),  # second
        (doc_a, 1),  # far
        (doc_b, 1),  # nodes_b[1]（同时是 2 跳可达，去重保留最短）
        (doc_b, 2),  # nodes_b[0]
    ]
    by_node = {hit.node_id: hit for hit in hits}
    assert by_node[second.node_id].via == ["see_also"]
    assert by_node[nodes_b[1].node_id].hops == 1 and by_node[nodes_b[1].node_id].via == ["see_also"]
    assert by_node[nodes_b[0].node_id].via == ["see_also", "traces_to"]
    assert [hit.node_id for hit in hits].count(nodes_b[1].node_id) == 1
    assert hub.node_id not in by_node


# ── 软删 / 文档级与悬空边（L5、ADR-009）───────────────────────────────


async def test_traverse_filters_deleted_and_can_include_them(
    storage: Storage, tmp_path: pathlib.Path
) -> None:
    """默认过滤 `status='deleted'`（既不返回也不再展开）；`include_deleted=True` 放开。"""
    doc_id, nodes = await import_synthetic(storage, tmp_path, "SPEC-STD-TRAV-DEL")
    n1, n2, n3 = nodes[0], nodes[1], nodes[2]
    await link(storage, n1, n2, "traces_to")
    await link(storage, n2, n3, "traces_to")

    middle = await storage.get_node(n2.node_id, doc_id=doc_id)
    await storage.delete_node(middle.node_id, middle.version, CTX)

    assert await traverse(n3.node_id, 2, doc_id=doc_id, storage=storage) == [], "软删节点断链"
    kept = await traverse(n3.node_id, 2, doc_id=doc_id, storage=storage, include_deleted=True)
    assert [(hit.node_id, hit.hops) for hit in kept] == [(n2.node_id, 1), (n1.node_id, 2)]
    with pytest.raises(NotFoundError):
        await traverse(n2.node_id, 1, doc_id=doc_id, storage=storage)
    restored = await traverse(
        n2.node_id, 1, doc_id=doc_id, storage=storage, include_deleted=True
    )
    assert [hit.node_id for hit in restored] == [n1.node_id]


async def test_traverse_skips_doc_level_and_dangling_refs(
    storage: Storage, database, tmp_path: pathlib.Path
) -> None:
    """文档级引用（`dst_node_id IS NULL`）与悬空目标不产生命中，也不报错（M09B 口径）。"""
    doc_id, nodes = await import_synthetic(storage, tmp_path, "SPEC-STD-TRAV-DOCLVL")
    src, peer = nodes[0], nodes[1]
    await storage.add_ref(src.node_id, doc_id, None, "see_also", CTX)  # 文档级（引用未解析）
    await storage.add_ref(src.node_id, doc_id, new_uuid7(), "see_also", CTX)  # 悬空目标
    await link(storage, src, peer, "composes_from")

    assert await count(database, "SELECT count(*) FROM refs") == 3
    hits = await traverse(src.node_id, 2, doc_id=doc_id, storage=storage)
    assert [hit.node_id for hit in hits] == [peer.node_id], "只有落到存活节点的那条边产生命中"


async def test_traverse_root_missing_or_malformed(storage: Storage, tmp_path: pathlib.Path) -> None:
    """不存在的起点 → `NotFoundError`；非法入参 → `ValidationError`（不写库）。"""
    doc_id, nodes = await import_synthetic(storage, tmp_path, "SPEC-STD-TRAV-ROOT")
    with pytest.raises(NotFoundError):
        await traverse(new_uuid7(), 1, storage=storage)
    with pytest.raises(NotFoundError):
        await traverse(new_uuid7(), 1, doc_id=doc_id, storage=storage)
    with pytest.raises(ValidationError):
        await traverse(nodes[0].node_id, -1, storage=storage)
    with pytest.raises(ValidationError):
        await traverse("not-a-uuid", 1, storage=storage)


# ── 分区（ADR-009 V16）──────────────────────────────────────────────────


async def plan_partitions(database, sql: str, **params) -> set[str]:
    """`EXPLAIN (ANALYZE, FORMAT JSON)` 计划中出现过的 `nodes` 分区名集合。"""
    async with database.session() as session:
        rows = (await session.execute(text(f"EXPLAIN (ANALYZE, FORMAT JSON) {sql}"), params)).all()
    plan = rows[0][0]
    if not isinstance(plan, str):
        plan = json.dumps(plan, default=str)
    return set(re.findall(r"nodes_p\d+", plan))


async def test_partition_pruning_by_doc_id(
    storage: Storage, database, tmp_path: pathlib.Path
) -> None:
    """带 `doc_id` 只扫 1 个分区；不带则扫全部 64 个（ADR-009 V16 的实测口径）。"""
    doc_id, nodes = await import_synthetic(storage, tmp_path, "SPEC-STD-TRAV-PART")
    node_id = nodes[0].node_id

    pruned = await plan_partitions(
        database,
        "SELECT node_id, doc_id, anchor, ordinal FROM nodes WHERE doc_id = :d AND node_id = :n",
        d=doc_id,
        n=node_id,
    )
    unpruned = await plan_partitions(
        database,
        "SELECT node_id, doc_id, anchor, ordinal FROM nodes WHERE node_id = :n",
        n=node_id,
    )
    assert len(pruned) == 1, f"带 doc_id 应只扫 1 个分区：{sorted(pruned)}"
    assert len(unpruned) == 64, f"不带 doc_id 应扫全部分区：{len(unpruned)}"


async def test_doc_id_hint_does_not_change_results(storage: Storage, tmp_path: pathlib.Path) -> None:
    """`doc_id` 只是分区裁剪提示：带与不带结果一致（含跨文档边的正向/逆向）。"""
    doc_a, nodes_a = await import_synthetic(storage, tmp_path, "SPEC-STD-TRAV-HINT-A")
    doc_b, nodes_b = await import_synthetic(storage, tmp_path, "SPEC-STD-TRAV-HINT-B")
    await link(storage, nodes_a[0], nodes_b[0], "see_also")  # 跨文档边

    hinted = await traverse(nodes_a[0].node_id, 1, doc_id=doc_a, storage=storage)
    unhinted = await traverse(nodes_a[0].node_id, 1, storage=storage)
    assert [(hit.node_id, hit.doc_id, hit.hops) for hit in hinted] == [
        (hit.node_id, hit.doc_id, hit.hops) for hit in unhinted
    ]
    assert [(hit.node_id, hit.doc_id) for hit in hinted] == [(nodes_b[0].node_id, doc_b)]
    # 逆向（dst→src）跨分区：目标 doc 未知 → 裸 node_id 解析（降级路径），结果仍须正确
    reverse = await traverse(nodes_b[0].node_id, 1, doc_id=doc_b, storage=storage)
    assert [(hit.node_id, hit.doc_id) for hit in reverse] == [(nodes_a[0].node_id, doc_a)]


# ── FTS（ADR-005 / REQ-M05-F02）─────────────────────────────────────────


def corpus_path() -> pathlib.Path:
    path = CORPUS / "amba" / "IHI0024_AMBA_APB_spec.md"
    if not path.is_file():
        pytest.skip(f"语料缺失：{path}")
    return path


@pytest.fixture
async def apb(storage: Storage, clean_database) -> str:
    """真实语料入库（单文档 ≈1.3k 节点）；显式依赖清理夹具，确保起点为空库。"""
    result = parse_markdown(corpus_path())
    outcome = await commit_document(result, CTX, storage=storage)
    return outcome.doc_id


async def test_search_text_hits_real_corpus_with_score(storage: Storage, apb: str) -> None:
    """真实语料 FTS：命中带 `score`、按相关度降序、字段与 `nodes` 行一致。"""
    hits = await search_text("transfer", 50, storage=storage)
    assert hits, "真实语料应命中 transfer"
    assert len(hits) <= 50
    scores = [hit.score for hit in hits]
    assert all(score > 0 for score in scores)
    assert scores == sorted(scores, reverse=True), "按相关度降序"
    for hit in hits:
        assert hit.doc_id == apb
        row = await storage.get_node(hit.node_id, doc_id=hit.doc_id)
        assert row.anchor == hit.anchor
        assert "transfer" in str(row.content["text"]).lower()

    assert len(await search_text("transfer", 3, storage=storage)) <= 3
    assert await search_text('"transfer" or handshake', 20, storage=storage), "websearch 语法可用"
    assert await search_text("zzzquuxnonexistent", 10, storage=storage) == []
    assert await search_text("   ", 10, storage=storage) == []
    assert await search_text("the", 10, storage=storage) == [], "纯停用词产出空 tsquery，不报错"


async def test_search_text_filters_deleted_and_validates_input(storage: Storage, apb: str) -> None:
    """deleted 默认被滤除（`include_deleted` 可放开）；limit/类型入参校验。"""
    hits = await search_text("transfer", 5, storage=storage)
    victim = await storage.get_node(hits[0].node_id, doc_id=hits[0].doc_id)
    await storage.delete_node(victim.node_id, victim.version, CTX)

    after = await search_text("transfer", 50, storage=storage)
    assert victim.node_id not in {hit.node_id for hit in after}
    kept = await search_text("transfer", 50, storage=storage, include_deleted=True)
    assert victim.node_id in {hit.node_id for hit in kept}

    with pytest.raises(ValidationError):
        await search_text("transfer", 0, storage=storage)
    with pytest.raises(ValidationError):
        await search_text(None, 10, storage=storage)  # type: ignore[arg-type]
