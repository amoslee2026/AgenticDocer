"""M03 集成测试：**真实语料**（`spec/standards` 7 份）× **真实 PG**（导入 → 审核 → 入库 → 资产）。

`conftest.py` 在 PG 不可用时整体 skip（无库环境仍全绿）。断言口径：

- 规则覆盖率 ≥95%（design_doc §10 口径：携带 `rule_id` 的源块 ÷ 总源块）；
- **零静默丢弃**：正文每个非空行都被某节点覆盖（行级），兜底块 100% 入库（REQ-M03-F04）；
- **P4 零改写**：HTML 表格片段原样进 `content.fragment`（format=html），且为源文本子串；
- 幂等：重复导入不产生重复节点/事件（M02「无变化不写事件」）；
- 图片资产：1,099 处引用（md 1,019 + HTML 80）被识别；缺失不阻断、报告 `assets.missing`。
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import re

import pytest
from sqlalchemy import text

from agenticdocer.importer import (
    check_proposals,
    commit_document,
    commit_document_bulk,
    fallback_anchors,
    load_review_state,
    parse_markdown,
    report,
    run_commit,
    run_parse,
    run_review,
    save_parse_result,
    save_review_state,
)
from agenticdocer.importer.cli import PROPOSALS_NAME, selected_proposals
from agenticdocer.model import C5_META_FIELDS, RawFallback, WriteContext
from agenticdocer.store import Storage, ValidationError

pytestmark = pytest.mark.integration

ROOT = pathlib.Path(__file__).resolve().parents[2]
CORPUS = ROOT / "spec" / "standards"
CTX = WriteContext(actor="importer", source="importer")

#: 每份语料都应命中的原子类型（`example`/`cross_ref` 与 `definition` 为语料相关）
_ATOM_KEYS = ("clause", "table", "figure", "note")
_ATOM_DOMAIN = {"clause", "definition", "table", "figure", "code", "example", "note", "cross_ref"}


def corpus_paths() -> list[pathlib.Path]:
    paths = sorted(CORPUS.glob("*/*.md"))
    if len(paths) < 7:
        pytest.skip(f"语料缺失（需 7 份）：{CORPUS}")
    return paths


@pytest.fixture(scope="session")
def corpus_results() -> dict[str, object]:
    """7 份语料的解析结果（会话级缓存：解析确定性，重复解析无收益）。"""
    return {path.name: parse_markdown(path) for path in corpus_paths()}


@pytest.fixture(scope="function")
def apb_result():
    return parse_markdown(CORPUS / "amba" / "IHI0024_AMBA_APB_spec.md")


async def count(database, sql: str, **params) -> int:
    async with database.session() as session:
        return int((await session.execute(text(sql), params)).scalar_one())


async def scalars(database, sql: str, **params) -> list:
    async with database.session() as session:
        return list((await session.execute(text(sql), params)).scalars())


async def rows(database, sql: str, **params) -> list:
    async with database.session() as session:
        return list((await session.execute(text(sql), params)).all())


_ENTITY_TABLES = ("comments", "refs", "nodes", "docs", "assets")


@pytest.fixture(autouse=True)
async def clean_database(database):
    """每个用例前清空实体表（幂等/计数断言依赖空库起点）。

    `events` 对应用角色是 append-only（仅 INSERT/SELECT，A15 库层强制），故**不可清**——
    涉及事件的断言一律用「提交前后增量」，与历史事件共存。
    """
    async with database.transaction() as session:
        for table in _ENTITY_TABLES:
            await session.execute(text(f"DELETE FROM {table}"))
    return database


def cross_ref_document() -> str:
    """合成文档：条款树 + 表格 + 列表 + 目录区兜底 + 交叉引用（覆盖 refs 边与兜底入库）。"""
    return """---
title: 交叉引用测试规范
type: composite
purpose: spec
audience: both
direction: input
status: approved
version: "1.0.0"
section_meta: "@meta"
spec_id: SPEC-STD-CROSS-1.0
spec_type: standard
spec_org: TEST
spec_revision: "1.0"
source: corpus/01_raw/specifications/test/cross.pdf
converted_by: mineru
converted_at: 2026-08-31
reviewed_by: tester
reviewed_at: 2026-08-31
---
# 1 概述

概述正文。

## 1.1 细节

细节正文。

See Section 1.1 for details.

<table><tr><td>A</td><td>B</td></tr></table>

- 列表项

## Contents

1. 概述 .. ...... 1
"""


def write_doc(tmp_path: pathlib.Path) -> pathlib.Path:
    source = tmp_path / "cross.md"
    source.write_text(cross_ref_document(), encoding="utf-8")
    return source


def accept_all(work_dir: pathlib.Path, doc_slug: str) -> None:
    """把工作区里全部提议标为 accepted（等价于 `review` 批量通过后的状态）。"""
    state = load_review_state(doc_slug, work_dir=work_dir)
    for item in state.items.values():
        item.decision = "accepted"
    save_review_state(state, work_dir=work_dir)


# ── 语料解析：覆盖率 / 计数 / P4 / 零丢弃 ────────────────────────────────


def test_corpus_parse_report(corpus_results) -> None:
    """7 份真实语料的解析报告：覆盖率、块数、原子计数、兜底、引用识别。"""
    totals = {"blocks": 0, "covered": 0, "fallback": 0, "proposals": 0, "md_refs": 0, "html_refs": 0, "f04": 0}
    atoms: dict[str, int] = {}
    lines = ["", f"{'doc':52s} {'blocks':>7s} {'covered':>7s} {'fallback':>8s} {'nodes':>6s} {'cov':>7s}"]
    for name, result in corpus_results.items():
        stats = result.stats
        summary = report(result)
        assert summary["coverage"] >= 0.95, f"{name} 规则覆盖率 {summary['coverage']:.4f} < 0.95"
        assert stats.total_blocks == stats.rule_covered + stats.fallback, "块账目必须闭合（零静默丢弃）"
        assert stats.fallback == len(result.unmapped), "兜底块必须全部进未映射清单"
        assert stats.pending >= stats.fallback, "兜底块必须进待确认清单（design_doc §10）"
        assert set(summary["atom_types"]) <= _ATOM_DOMAIN, summary["atom_types"]
        for key in _ATOM_KEYS:
            assert summary["atom_types"].get(key, 0) > 0, f"{name} 缺 {key} 原子"
        for key, value in summary["atom_types"].items():
            atoms[key] = atoms.get(key, 0) + value
        totals["blocks"] += stats.total_blocks
        totals["covered"] += stats.rule_covered
        totals["fallback"] += stats.fallback
        totals["proposals"] += len(result.proposals)
        totals["md_refs"] += summary["asset_refs"]["md"]
        totals["html_refs"] += summary["asset_refs"]["html"]
        totals["f04"] += summary["rules"].get("F04.table.text-empty", 0)
        lines.append(
            f"{name:52s} {stats.total_blocks:7d} {stats.rule_covered:7d} {stats.fallback:8d} "
            f"{len(result.proposals):6d} {summary['coverage']:7.4f}"
        )
    lines.append(
        f"TOTAL blocks={totals['blocks']} covered={totals['covered']} fallback={totals['fallback']} "
        f"nodes={totals['proposals']} coverage={totals['covered'] / totals['blocks']:.4f} atoms={atoms}"
    )
    print("\n".join(lines))

    # 规模基线（ADR-006：条款级最小节点 ≈9.4k；本实现含列表 note ≈10k）
    assert 30_000 <= totals["blocks"] <= 40_000
    assert 9_000 <= totals["proposals"] <= 12_000
    assert totals["covered"] / totals["blocks"] >= 0.95
    # design_doc §5.2 实测口径：md 形式 1,019 + HTML <img> 80 = 1,099
    assert totals["md_refs"] == 1_019
    assert totals["html_refs"] == 80
    # HTML 表格 2,440（§5.1 实测）= table 原子 + F04 兜底（无文本投影的表格壳）
    assert atoms["table"] + totals["f04"] == 2_440
    assert totals["f04"] == 1, "仅 1 处无文本表格壳（PCIe §7.9.2.4：转换器把图包成 1×1 表格）"
    assert atoms["definition"] > 0  # 术语区词条（PCIe「Terms and Acronyms」+ AMBA Glossary）
    assert atoms["note"] > 0        # 列表 + 目录区兜底
    assert atoms["figure"] == 1_019
    assert atoms["code"] == 9


def test_corpus_line_coverage_is_complete(corpus_results) -> None:
    """零静默丢弃（行级）：正文每个非空行都被某节点的来源区间覆盖。"""
    for name, result in corpus_results.items():
        path = next(item for item in corpus_paths() if item.name == name)
        body_start = result.doc_meta["body_start"]
        body_lines = path.read_text(encoding="utf-8").split("\n")[body_start - 1 :]
        covered: set[int] = set()
        for proposal in result.proposals:
            covered.update(range(proposal.source_lines[0], proposal.source_lines[1] + 1))
        missing = [
            index + body_start
            for index, line in enumerate(body_lines)
            if line.strip() and (index + body_start) not in covered
        ]
        assert missing == [], f"{name} 有 {len(missing)} 个非空源行未被任何节点覆盖"


def test_corpus_html_tables_are_verbatim_passthrough(corpus_results) -> None:
    """P4 零改写：`<table>` 片段原样进 content.fragment（format=html），且为源文本子串。"""
    for name, result in corpus_results.items():
        path = next(item for item in corpus_paths() if item.name == name)
        source = path.read_text(encoding="utf-8")
        tables = [p for p in result.proposals if p.atom.atom_type == "table"]
        shells = [p for p in result.proposals if p.rule_id == "F04.table.text-empty"]
        assert len(tables) + len(shells) == source.count("<table"), f"{name}: 表格节点数与源 <table> 不一致"
        for proposal in shells:  # 兜底路径同样零改写（原文整段保留在 content.fragment）
            assert proposal.atom.format == "html"
            assert proposal.atom.text in source
        for proposal in tables:
            atom = proposal.atom
            fragment = atom.content["fragment"]
            assert atom.format == "html"
            assert fragment.startswith("<table") and fragment.rstrip().endswith("</table>")
            assert fragment in source, "表格片段必须是源文本的逐字节切片"
            meta = atom.content["meta"]
            assert set(meta) == {"rows", "cols", "cells", "max_colspan"}
            assert meta["rows"] >= 1 and meta["cols"] >= meta["max_colspan"] >= 1
            assert atom.content["text"].strip(), "A10：表格原子 text 非空"


def test_corpus_figures_are_content_addressed(corpus_results) -> None:
    for name, result in corpus_results.items():
        for proposal in (p for p in result.proposals if p.atom.atom_type == "figure"):
            content = proposal.atom.content
            assert re.fullmatch(r"[0-9a-f]{64}", content["asset_ref"]), content
            assert "fragment" not in content, "figure 无 fragment（M01 schema；渲染期由 M04 合成）"
            assert content["text"].strip()


def test_corpus_proposals_pass_schema_gate(corpus_results) -> None:
    """全部语料提议通过校验（M09A 等价 schema + 锚唯一 + A10），无一例外。"""
    for name, result in corpus_results.items():
        assert check_proposals(result) == [], f"{name} 存在违规提议"


# ── 入库（真实 PG）──────────────────────────────────────────────────────


async def test_commit_small_real_document(storage: Storage, database, apb_result) -> None:
    result = apb_result
    doc_id = result.doc_meta["doc_id"]
    events_before = await count(
        database,
        "SELECT count(*) FROM events WHERE entity = 'node' AND op = 'create' AND payload->'doc_id'->>'after' = :d",
        d=doc_id,
    )
    outcome = await commit_document(result, CTX, storage=storage)
    assert outcome.doc_id == "SPEC-STD-AMBA-APB"
    assert outcome.nodes_created == len(result.proposals)
    assert outcome.refs_created == 0
    assert outcome.stats == result.stats

    async with database.session() as session:
        doc = (
            await session.execute(
                text("SELECT doc_type, status, meta, source_ref FROM docs WHERE doc_id = :d"), {"d": doc_id}
            )
        ).one()
    assert doc.doc_type == "standard" and doc.status == "approved"
    assert doc.source_ref.endswith("IHI0024_AMBA_APB_spec.pdf")
    for field in C5_META_FIELDS:
        assert field in doc.meta, f"docs.meta 缺 C5 字段 {field}"
    assert doc.meta["doc_slug"] == "IHI0024_AMBA_APB_spec"

    node_count = await count(database, "SELECT count(*) FROM nodes WHERE doc_id = :d", d=doc_id)
    distinct = await count(database, "SELECT count(DISTINCT anchor) FROM nodes WHERE doc_id = :d", d=doc_id)
    assert node_count == len(result.proposals) == distinct
    assert await count(
        database,
        "SELECT count(*) FROM nodes WHERE doc_id = :d AND coalesce(content->>'text','') = ''",
        d=doc_id,
    ) == 0, "A10：一切节点 content.text 非空"
    formats = set(await scalars(database, "SELECT DISTINCT format FROM nodes WHERE doc_id = :d", d=doc_id))
    assert formats <= {"md", "html"}
    levels = set(await scalars(database, "SELECT DISTINCT level FROM nodes WHERE doc_id = :d", d=doc_id))
    assert levels <= {1, 2, 3, None}
    assert await count(
        database,
        "SELECT count(*) FROM nodes WHERE doc_id = :d AND level IS NOT NULL AND level > 1 "
        "AND parent_node_id IS NULL",
        d=doc_id,
    ) == 0, "非顶层条款必须有父节点（level + ordinal 栈重建）"
    assert await count(
        database,
        "SELECT count(*) FROM nodes WHERE doc_id = :d AND level IS NULL AND parent_node_id IS NULL",
        d=doc_id,
    ) == 0, "独立原子必须挂在所属条款下"
    node_events = await count(
        database,
        "SELECT count(*) FROM events WHERE entity = 'node' AND op = 'create' AND payload->'doc_id'->>'after' = :d",
        d=doc_id,
    )
    assert node_events - events_before == outcome.nodes_created, "每次节点创建对应一条 create 事件"


async def test_commit_is_idempotent(storage: Storage, database, apb_result) -> None:
    result = apb_result
    doc_id = result.doc_meta["doc_id"]
    first = await commit_document(result, CTX, storage=storage)
    nodes = await count(database, "SELECT count(*) FROM nodes WHERE doc_id = :d", d=doc_id)
    events = await count(database, "SELECT count(*) FROM events")
    assert first.nodes_created == len(result.proposals)
    second = await commit_document(result, CTX, storage=storage)
    assert second.nodes_created == 0, "重复导入不得新建节点（幂等）"
    assert await count(database, "SELECT count(*) FROM nodes WHERE doc_id = :d", d=doc_id) == nodes
    assert await count(database, "SELECT count(*) FROM events") == events, "无变化不得写事件（M02 幂等）"


async def test_fallback_blocks_are_persisted_verbatim(storage: Storage, database) -> None:
    """REQ-M03-F04：兜底块 100% 入库且原文保真（抽样可查 → 此处逐条全查）。"""
    result = parse_markdown(CORPUS / "jedec" / "JEDEC_JESD270-4A_HBM4_2025.md")
    assert result.unmapped, "该语料应有兜底块（目录区）"
    outcome = await commit_document(result, CTX, storage=storage)
    doc_id = outcome.doc_id
    anchors = fallback_anchors(result)
    fallback_ids = [p.proposal_id for p in result.proposals if isinstance(p.atom, RawFallback)]
    assert len(anchors) == len(fallback_ids) == len(result.unmapped)
    for proposal in result.proposals:
        if not isinstance(proposal.atom, RawFallback):
            continue
        found = await rows(
            database,
            "SELECT atom_type, format, content->>'fragment', content->>'text' FROM nodes "
            "WHERE doc_id = :d AND anchor = :a",
            d=doc_id,
            a=anchors[proposal.proposal_id],
        )
        assert found, f"兜底块未入库：{proposal.proposal_id}（{proposal.source_lines}）"
        atom_type, fmt, fragment, node_text = found[0]
        assert atom_type == "note" and fmt in ("md", "html")
        assert fragment == proposal.atom.text, "兜底块原文必须逐字节保真"
        assert node_text.strip()


async def test_missing_assets_do_not_block_import(storage: Storage, database, apb_result, tmp_path) -> None:
    """REQ-M03-F05：资产缺失不阻断；缺失清单与 M02 `list_missing_assets` 判据一致。"""
    result = apb_result
    doc_slug = result.doc_meta["doc_slug"]
    work = tmp_path / "work"
    save_parse_result(result, doc_slug=doc_slug, work_dir=work)
    accept_all(work, doc_slug)
    assert len(result.doc_meta["asset_refs"]["refs"]) == 8
    outcome = await run_commit(
        doc_slug, work_dir=work, storage=storage, source_root=tmp_path / "no_such_source_root"
    )
    assert outcome.assets is not None
    assert outcome.assets.total_refs == 8 and outcome.assets.fetched == 0
    assert len(outcome.assets.missing) == 8
    assert outcome.commit.nodes_created == len(result.proposals)
    # 导入期缺资产可由库内数据复现：figure.asset_ref 无对应 assets 行。
    # 注：M02 `list_missing_assets` 的口径是「渲染产物引用」（`assets/<sha>.<ext>`，即 M04 产物再
    # 导入后的形态），导入期引用（源 `images/<sha>.jpg` + figure.asset_ref）不在其扫描范围——
    # 导入期缺失清单由本模块的 AssetSyncReport.missing 承载（REQ-M03-F05），两者共存不冲突。
    missing_shas = await scalars(
        database,
        "SELECT DISTINCT n.content->>'asset_ref' FROM nodes n "
        "LEFT JOIN assets a ON a.asset_id = n.content->>'asset_ref' "
        "WHERE n.doc_id = :d AND n.content->>'asset_ref' IS NOT NULL AND a.asset_id IS NULL",
        d=result.doc_meta["doc_id"],
    )
    assert sorted(missing_shas) == sorted(
        ref.rsplit("/", 1)[-1].removesuffix(".jpg") for ref in result.doc_meta["asset_refs"]["refs"]
    )


async def test_asset_bytes_land_in_cas(storage: Storage, database, tmp_path) -> None:
    """取件成功路径：sha256 校验 → CAS 落盘 + `assets` 行（重复导入去重）。"""
    payload = b"\x89PNG\r\n\x1a\nfake-image-bytes"
    sha = hashlib.sha256(payload).hexdigest()
    source_root = tmp_path / "src"
    (source_root / "images").mkdir(parents=True)
    (source_root / "images" / f"{sha}.png").write_bytes(payload)
    markdown = cross_ref_document().replace("SPEC-STD-CROSS-1.0", "SPEC-STD-ASSET-1.0")
    markdown = markdown.replace("# 1 概述", f"# 1 概述\n\n![](images/{sha}.png)")
    source = tmp_path / "asset.md"
    source.write_text(markdown, encoding="utf-8")
    work = tmp_path / "work"
    result = run_parse(source, "asset-doc", work_dir=work)
    figures = [p for p in result.proposals if p.atom.atom_type == "figure"]
    assert len(figures) == 1 and figures[0].atom.content["asset_ref"] == sha
    accept_all(work, "asset-doc")

    first = await run_commit("asset-doc", work_dir=work, storage=storage, source_root=source_root)
    assert first.assets is not None and first.assets.fetched == 1 and first.assets.missing == []
    asset = await storage.get_asset(sha)
    assert asset.bytes == len(payload) and asset.mime == "image/png"
    assert (pathlib.Path(storage.store_dir) / asset.path).is_file()
    assert await storage.list_missing_assets(result.doc_meta["doc_id"]) == []

    second = await run_commit("asset-doc", work_dir=work, storage=storage, source_root=source_root)
    assert second.assets is not None and second.assets.fetched == 1
    assert await count(database, "SELECT count(*) FROM assets") == 1, "同 id 资产不得重复落行"


# ── 审核 → 入库 全流程（业务函数；含 refs 边与拒绝留痕）─────────────────


def _reslug(text: str, doc_id: str) -> str:
    return text.replace("SPEC-STD-AMBA-APB", doc_id)


async def _snapshot(database, doc_id: str) -> tuple[list[tuple], dict[tuple[str, str], int], set[str]]:
    """节点快照（锚剥 doc 前缀 + 父锚归一）+ 事件计数 + node create 事件的锚集合。"""
    node_rows = await rows(
        database,
        "SELECT n.anchor, n.atom_type, n.format, n.ordinal, n.level, n.status, n.version, "
        "n.content::text, coalesce(p.anchor, '') FROM nodes n "
        "LEFT JOIN nodes p ON p.node_id = n.parent_node_id WHERE n.doc_id = :d ORDER BY n.ordinal, n.anchor",
        d=doc_id,
    )
    nodes_norm = [
        (row[0].replace(doc_id, "DOC"), row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8].replace(doc_id, "DOC"))
        for row in node_rows
    ]
    event_rows = await rows(
        database,
        "SELECT entity, op, count(*) FROM events WHERE payload->'doc_id'->>'after' = :d "
        "OR payload->>'dst_doc' = :d GROUP BY entity, op",
        d=doc_id,
    )
    counts = {(row[0], row[1]): int(row[2]) for row in event_rows}
    anchors = {
        row[0]
        for row in await scalars(
            database,
            "SELECT payload->'anchor'->>'after' FROM events WHERE entity = 'node' AND op = 'create' "
            "AND payload->'doc_id'->>'after' = :d",
            d=doc_id,
        )
        if row
    }
    return nodes_norm, counts, {anchor.replace(doc_id, "DOC") for anchor in anchors}


async def test_bulk_path_is_semantically_equivalent(storage: Storage, database, tmp_path) -> None:
    """A/B 等价（PerfBench 指定验收）：批量路径与逐节点路径产出**相同库状态**。

    同一源文本落成两个 doc_id（`SEQ` 逐节点 / `BULK` 批量）；比较锚（剥 doc 前缀）、
    atom_type/format/ordinal/level/status/version/content、**父链（父锚归一）**，
    以及事件（`(entity, op)` 计数 + node create 事件的锚集合）。node_id 为 uuid7 随机，
    不参与比较（两路都是新分配）。
    """
    text = (CORPUS / "jedec" / "JEDEC_JESD270-4A_HBM4_2025.md").read_text(encoding="utf-8")
    seq_doc, bulk_doc = "SPEC-STD-EQ-SEQ", "SPEC-STD-EQ-BULK"
    seq_src, bulk_src = tmp_path / "seq.md", tmp_path / "bulk.md"
    seq_src.write_text(_reslug(text, seq_doc), encoding="utf-8")
    bulk_src.write_text(_reslug(text, bulk_doc), encoding="utf-8")
    seq_result = parse_markdown(seq_src)
    bulk_result = parse_markdown(bulk_src)

    seq_out = await commit_document(seq_result, CTX, storage=storage)
    bulk_out = await commit_document_bulk(bulk_result, CTX, storage=storage)
    assert seq_out.nodes_created == bulk_out.nodes_created == len(seq_result.proposals)
    assert seq_out.stats == bulk_out.stats

    seq_snapshot = await _snapshot(database, seq_doc)
    bulk_snapshot = await _snapshot(database, bulk_doc)
    assert seq_snapshot[0] == bulk_snapshot[0], "节点行（含父链）必须逐字段一致"
    assert seq_snapshot[1] == bulk_snapshot[1], "事件 (entity, op) 计数必须一致"
    assert seq_snapshot[2] == bulk_snapshot[2], "node create 事件的锚集合必须一致"

    # 幂等（批量路径）：二次提交不新建节点、不写事件
    nodes_before = await count(database, "SELECT count(*) FROM nodes WHERE doc_id = :d", d=bulk_doc)
    events_before = await count(database, "SELECT count(*) FROM events")
    again = await commit_document_bulk(bulk_result, CTX, storage=storage)
    assert again.nodes_created == 0
    assert await count(database, "SELECT count(*) FROM nodes WHERE doc_id = :d", d=bulk_doc) == nodes_before
    assert await count(database, "SELECT count(*) FROM events") == events_before

    # initial_load 仅限空文档（Main 要求的显式区分）
    with pytest.raises(ValidationError, match="initial_load"):
        await commit_document_bulk(bulk_result, CTX, storage=storage, bulk_mode="initial_load")
    # 空文档可用 initial_load
    empty_result = parse_markdown(tmp_path / "bulk.md") if False else bulk_result
    live = await commit_document_bulk(
        parse_markdown(_write_variant(tmp_path, text, "SPEC-STD-EQ-INIT")),
        CTX,
        storage=storage,
        bulk_mode="initial_load",
    )
    assert live.nodes_created == len(bulk_result.proposals)


def _write_variant(tmp_path: pathlib.Path, text: str, doc_id: str) -> pathlib.Path:
    path = tmp_path / f"{doc_id}.md"
    path.write_text(_reslug(text, doc_id), encoding="utf-8")
    return path


async def test_review_then_commit_creates_refs(storage: Storage, database, tmp_path) -> None:
    source = write_doc(tmp_path)
    work = tmp_path / "work"
    result = run_parse(source, "cross-doc", work_dir=work)
    cross = [p for p in result.proposals if p.atom.atom_type == "cross_ref"]
    assert len(cross) == 1 and cross[0].atom.content.get("target_anchor")
    target = next(p for p in result.proposals if p.atom.anchor == cross[0].atom.content["target_anchor"])

    refs_before = await count(
        database,
        "SELECT count(*) FROM events WHERE entity = 'ref' AND op = 'add' AND payload->>'dst_doc' = :d",
        d="SPEC-STD-CROSS-1.0",
    )
    state = run_review(
        "cross-doc", work_dir=work, answers=iter(["a", "a"]), out=lambda _: None, accept_confident=True
    )
    assert all(item.decision == "accepted" for item in state.items.values())
    outcome = await run_commit("cross-doc", work_dir=work, storage=storage, sync_assets_too=False)
    assert outcome.accepted == len(result.proposals)
    assert outcome.commit.nodes_created == len(result.proposals)
    assert outcome.commit.refs_created == 1
    assert outcome.violations == []
    payload = json.loads((work / "cross-doc" / "commit_report.json").read_text(encoding="utf-8"))
    assert payload["docId"] == "SPEC-STD-CROSS-1.0" and payload["assets"] is None

    by_anchor = dict(
        zip(
            await scalars(database, "SELECT anchor FROM nodes WHERE doc_id = :d", d="SPEC-STD-CROSS-1.0"),
            await scalars(database, "SELECT node_id FROM nodes WHERE doc_id = :d", d="SPEC-STD-CROSS-1.0"),
        )
    )
    refs = await storage.list_refs(by_anchor[cross[0].atom.anchor])
    assert [(ref.dst_doc_id, ref.dst_node_id, ref.kind) for ref in refs] == [
        ("SPEC-STD-CROSS-1.0", by_anchor[target.atom.anchor], "see_also")
    ]
    assert await count(
        database,
        "SELECT count(*) FROM events WHERE entity = 'ref' AND op = 'add' AND payload->>'dst_doc' = :d",
        d="SPEC-STD-CROSS-1.0",
    ) - refs_before == 1, "本次提交新增 1 条 ref add 事件（events 为 append-only，按增量断言）"


async def test_rejected_proposals_are_not_committed(storage: Storage, database, tmp_path) -> None:
    source = write_doc(tmp_path)
    work = tmp_path / "work"
    result = run_parse(source, "cross-doc", work_dir=work)
    rejected = next(p for p in result.proposals if p.atom.atom_type == "table")
    state = load_review_state("cross-doc", work_dir=work)
    for item in state.items.values():
        item.decision = "accepted"
    state.items[rejected.proposal_id].decision = "rejected"
    save_review_state(state, work_dir=work)

    outcome = await run_commit("cross-doc", work_dir=work, storage=storage, sync_assets_too=False)
    assert outcome.rejected == 1
    assert outcome.commit.nodes_created == len(result.proposals) - 1
    assert await count(
        database,
        "SELECT count(*) FROM nodes WHERE doc_id = :d AND anchor = :a",
        d="SPEC-STD-CROSS-1.0",
        a=rejected.atom.anchor,
    ) == 0, "被拒绝的提议不得入库"


async def test_commit_rejects_invalid_proposals(storage: Storage, database, tmp_path) -> None:
    source = write_doc(tmp_path)
    result = run_parse(source, "cross-doc", work_dir=tmp_path / "work")
    broken = result.model_copy(deep=True)
    broken.proposals[0].atom.content["text"] = ""
    with pytest.raises(ValidationError) as excinfo:
        await commit_document(broken, CTX, storage=storage)
    assert "content.text" in str(excinfo.value)
    assert await count(database, "SELECT count(*) FROM docs WHERE doc_id = :d", d="SPEC-STD-CROSS-1.0") == 0
    assert await count(database, "SELECT count(*) FROM nodes WHERE doc_id = :d", d="SPEC-STD-CROSS-1.0") == 0


async def test_review_workspace_contract(tmp_path) -> None:
    """工作区契约（A13）：proposals.json 可往返；审核筛选口径可复核。"""
    source = write_doc(tmp_path)
    work = tmp_path / "work"
    result = run_parse(source, "cross-doc", work_dir=work)
    payload = json.loads((work / "cross-doc" / PROPOSALS_NAME).read_text(encoding="utf-8"))
    assert payload["rule_set_version"] and payload["report"]["coverage"] >= 0.8
    assert {item["proposalId"] for item in payload["result"]["proposals"]} == {
        proposal.proposal_id for proposal in result.proposals
    }
    assert len(selected_proposals(result, ["p0001", "p0002"])) == 2
    assert len(selected_proposals(result, None)) == len(result.proposals)
    assert result.stats.fallback == 1 and result.unmapped[0].fallback.format == "md"
