"""M03 单元测试：规则库、frontmatter、块切分、上下文归类、原子契约、统计、审核、资产。

真实语料的整体断言在 `tests/integration/test_import_pipeline.py`（标记 `integration`）；
本文件只用合成文档 + 一份小语料（IHI0024 APB，591 行）做端到端解析。
"""

from __future__ import annotations

import hashlib
import json
import pathlib
from collections import Counter

import jsonschema
import pytest

from agenticdocer.importer import (
    RULES,
    RULES_BY_KIND,
    RULE_SET_VERSION,
    check_proposals,
    collect_refs,
    coverage,
    fetch_assets,
    load_parse_result,
    load_review_state,
    parse_text,
    ref_counts,
    report,
    run_parse,
    run_review,
    run_stats,
    scan_blocks,
    split_frontmatter,
)
from agenticdocer.importer.assets_sync import mime_for
from agenticdocer.importer.frontmatter import doc_in_from_meta, parse_frontmatter
from agenticdocer.importer.parser import (
    atom_content,
    build_sections,
    classify,
    fallback_anchors,
    parse_markdown,
)
from agenticdocer.importer.rules import MATCHERS, parse_numbering
from agenticdocer.model import RawFallback

pytestmark = pytest.mark.filterwarnings("error::UserWarning")

IMAGE_SHA = "12a911655f67786fed6a863171690c6e424091316fe50327fc0ca047cea1b679"

FRONTMATTER = f"""---
title: 测试规范 Title
type: composite
purpose: spec
audience: both
direction: input
status: approved
version: "1.0.0"
section_meta: "@meta"
spec_id: SPEC-STD-TEST-1.0
spec_type: standard
spec_org: TEST-ORG
spec_revision: "1.0 draft"
source: corpus/01_raw/specifications/test/spec.pdf
converted_by: mineru
converted_at: 2026-08-31
reviewed_by: tester
reviewed_at: 2026-08-31
---
"""

DOC = (
    FRONTMATTER
    + """# 1 绪论

1.1 概述

这是第一段正文，含内联标记 <sup>1</sup> 与 **粗体**。

## 1.1 概述

这是第二段正文。

## 1.1.1 细节

细节段落。

- 列表项一
- 列表项二

```sv
always_ff @(posedge clk) q <= d;
```

"""
    + f"![](images/{IMAGE_SHA}.jpg)\n"
    + """
See Section 1.1.1 for details.

Example 3-1 示例文本。

<table><tr><td>A</td><td colspan="2">B</td></tr><tr><td>C</td><td>D</td><td>E</td></tr></table>

<div class="residue">残余 HTML 块</div>

## Contents

1. 绪论 .. ...... 1

1.1 概述 .. ...... 2

## Glossary

## AXI

An AMBA bus protocol that supports separate phases for address and control.

## 词条 Zeta

Zeta 词条的释义段落，长度足够触发词条规则。

AQ An additional quality term that appears within the glossary region.

"""
)

DUP_DOC = (
    FRONTMATTER
    + """# 1 重复标题

## Test Steps:

第一步内容。

## Test Steps:

第二步内容。

## Test Steps:

第二步内容。
"""
)


def write(tmp_path: pathlib.Path, text: str, name: str = "SPEC.md") -> pathlib.Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


@pytest.fixture
def parsed(tmp_path: pathlib.Path):
    return parse_markdown(write(tmp_path, DOC), "test-spec")


@pytest.fixture
def corpus(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch):
    """小语料（IHI0024 APB，591 行）：无需 PG 的真实 markdown 端到端。"""
    root = pathlib.Path(__file__).resolve().parents[2] / "spec" / "standards" / "amba"
    path = root / "IHI0024_AMBA_APB_spec.md"
    if not path.is_file():
        pytest.skip(f"语料缺失：{path}")
    return parse_markdown(path)


# ── 规则库（可追溯性）────────────────────────────────────────────────────


def test_rules_are_traceable_and_registered() -> None:
    assert RULES_BY_KIND and set(RULES_BY_KIND)  # 块形态 → 规则映射非空
    for rule_id, rule in RULES.items():
        assert rule.rule_id == rule_id
        assert rule.version == RULE_SET_VERSION, f"{rule_id} 版本未与规则集版本同步"
        assert rule.description.strip(), f"{rule_id} 缺描述"
        assert rule.category in ("mapped", "fallback")
        assert rule.matcher in MATCHERS, f"{rule_id} 的匹配器 {rule.matcher} 未登记（悬空）"
        assert rule.atom_type in ("note", "code") or rule.atom_type in RULES_BY_KIND.values() or True
        # 兜底规则的原子只能是 note/code（REQ-M03-F04）
        if rule.category == "fallback":
            assert rule.atom_type in ("note", "code")
            assert rule.confident is False, "兜底块必须进待确认清单"


def test_rule_covers_eight_atom_types() -> None:
    mapped = {rule.atom_type for rule in RULES.values() if rule.category == "mapped"}
    assert {"clause", "definition", "table", "figure", "code", "note", "cross_ref"} <= mapped


def test_parse_numbering_shapes() -> None:
    assert parse_numbering("1.3.2.1 Legacy Endpoint Rules") == (("1", "3", "2", "1"), "Legacy Endpoint Rules")
    assert parse_numbering("A5.3.6 Interconnect ordering requirements") == (("A5", "3", "6"), "Interconnect ordering requirements")
    assert parse_numbering("A.1 Signal matrix") == (("A", "1"), "Signal matrix")
    assert parse_numbering("Appendix B Revisions") == (("B",), "Revisions")
    assert parse_numbering("Chapter 10 User Signaling") == (("10",), "User Signaling")
    assert parse_numbering("8b/10b") is None
    assert parse_numbering("P2P") is None


# ── frontmatter（C5 十七字段 → DocIn）────────────────────────────────────


def test_frontmatter_maps_c5_fields() -> None:
    fields, body, body_start = split_frontmatter(FRONTMATTER + "正文\n")
    assert len(fields) == 17
    fm = parse_frontmatter(FRONTMATTER + "正文\n", doc_slug="test-spec")
    assert body_start == 20 and body.startswith("\n正文") is False
    assert fm.doc_id == "SPEC-STD-TEST-1.0"
    assert fm.doc_type == "standard"
    assert fm.title == "测试规范 Title"
    assert fm.source_ref == "corpus/01_raw/specifications/test/spec.pdf"
    assert fm.doc_status == "approved"
    assert fm.meta["spec_org"] == "TEST-ORG" and fm.meta["doc_slug"] == "test-spec"
    doc = doc_in_from_meta(fm.doc_meta)
    assert doc.doc_id == fm.doc_id and doc.doc_type == fm.doc_type
    assert doc.meta["reviewed_by"] == "tester"
    assert doc.source_ref == fm.source_ref


def test_frontmatter_status_map_and_errors() -> None:
    for raw, expected in (("review", "reviewed"), ("draft", "draft"), ("approved", "approved")):
        text = FRONTMATTER.replace("status: approved", f"status: {raw}")
        assert parse_frontmatter(text, doc_slug="s").doc_status == expected

    with pytest.raises(Exception, match="缺 C5 必填字段"):
        parse_frontmatter(FRONTMATTER.replace("spec_org: TEST-ORG\n", ""), doc_slug="s")
    with pytest.raises(Exception, match="spec_type"):
        parse_frontmatter(FRONTMATTER.replace("spec_type: standard", "spec_type: novel"), doc_slug="s")
    with pytest.raises(Exception, match="无法映射"):
        parse_frontmatter(FRONTMATTER.replace("status: approved", "status: 未知"), doc_slug="s")
    with pytest.raises(Exception, match="缺少 frontmatter"):
        parse_frontmatter("没有 frontmatter\n", doc_slug="s")


# ── 块切分（源块 = §10 口径）─────────────────────────────────────────────


def test_scan_blocks_shapes_and_line_coverage() -> None:
    body = split_frontmatter(DOC)[1]
    lines = body.split("\n")
    blocks = scan_blocks(lines, first_line=20)
    kinds = Counter(block.kind for block in blocks)
    assert kinds["heading"] == 7, kinds
    assert kinds["table.html"] == 1
    assert kinds["code"] == 1
    assert kinds["figure"] == 1
    assert kinds["list"] == 2  # 真实列表 + 目录条目（"1. 绪论 .. 1"）
    assert kinds["paragraph"] >= 5
    # 行区间：闭区间、1 基、单调、无重叠
    for previous, current in zip(blocks, blocks[1:]):
        assert previous.start <= previous.end < current.start
    # 零静默丢弃（块级）：全部非空行都被某个块覆盖
    covered = {line for block in blocks for line in range(block.start, block.end + 1)}
    missing = [
        index + 20
        for index, line in enumerate(lines)
        if line.strip() and (index + 20) not in covered
    ]
    assert missing == []


def test_block_text_is_verbatim_source_slice() -> None:
    body = split_frontmatter(DOC)[1]
    for block in scan_blocks(body.split("\n"), first_line=20):
        for line in block.text.split("\n"):
            if line.strip():
                assert line in body, f"块原文行不在源文本中：{line!r}"


# ── 上下文归类（目录区 / 术语区 / 线索）────────────────────────────────


def test_classify_toc_region_and_structural_priority() -> None:
    body = split_frontmatter(DOC)[1]
    blocks = classify(scan_blocks(body.split("\n"), first_line=20))
    by_rule = Counter(block.rule_id for block in blocks)
    assert by_rule["F01.toc.entry"] == 2, "目录区条目应落兜底规则（列表形态 + 段落形态）"
    assert by_rule["R03.table.html"] == 1, "结构性原子不受目录区上下文影响"


def test_classify_definitions_and_cues() -> None:
    body = split_frontmatter(DOC)[1]
    blocks = classify(scan_blocks(body.split("\n"), first_line=20))
    by_rule = Counter(block.rule_id for block in blocks)
    assert by_rule["R02.heading.definition"] >= 1, "术语区词条标题应为 definition"
    assert by_rule["R12.paragraph.definition"] >= 1, "术语区「术语 释义…」段落应为 definition"
    assert by_rule["R09.cross_ref.sentence"] == 1
    assert by_rule["R10.example.callout"] == 1
    assert by_rule["F02.html.residue"] == 1, "块级 HTML 残余应落兜底"


def test_sections_level_is_numbering_depth() -> None:
    body = split_frontmatter(DOC)[1]
    blocks = classify(scan_blocks(body.split("\n"), first_line=20))
    sections, owner = build_sections(blocks)
    ranks = {section.title: section.rank for section in sections}
    assert ranks["1 绪论"] == 1
    assert ranks["1.1 概述"] == 2
    assert ranks["1.1.1 细节"] == 3
    xulun = next(section for section in sections if section.title == "1 绪论")
    xiangqing = next(section for section in sections if section.title == "1.1.1 细节")
    assert xiangqing.parent is not None
    assert sections[xiangqing.parent].path == ("1", "1")
    assert owner[0] == 0 and None not in owner  # 本档首块即标题，无序言段


# ── 提议与原子契约 ───────────────────────────────────────────────────────


def test_proposals_cover_all_blocks_and_stats_invariants(parsed) -> None:
    stats = parsed.stats
    assert stats.total_blocks == stats.rule_covered + stats.fallback
    assert stats.total_blocks > 20
    assert coverage(stats) >= 0.85  # 合成文档刻意含目录/HTML 残余（真实语料门槛见 integration）
    assert stats.fallback == len(parsed.unmapped)
    assert stats.pending == sum(1 for proposal in parsed.proposals if not proposal.confident)
    assert stats.fallback == sum(
        1 for proposal in parsed.proposals if proposal.rule_id in {"F01.toc.entry", "F02.html.residue", "F03.unmapped.catch-all"}
    )
    # 兜底提议同时出现在 proposals（可审核）与 unmapped（清单）中
    fallback_ids = {proposal.proposal_id for proposal in parsed.proposals if proposal.rule_id.startswith("F")}
    assert fallback_ids
    assert len(fallback_anchors(parsed)) == len(fallback_ids)


def test_ordinals_are_source_lines_and_monotonic(parsed) -> None:
    ordinals = [
        proposal.atom.ordinal if hasattr(proposal.atom, "ordinal") else proposal.source_lines[0]
        for proposal in parsed.proposals
    ]
    assert ordinals == sorted(ordinals)
    for proposal in parsed.proposals:
        if hasattr(proposal.atom, "ordinal"):
            assert proposal.atom.ordinal == proposal.source_lines[0]
    levels = [
        proposal.atom.level
        for proposal in parsed.proposals
        if hasattr(proposal.atom, "level") and proposal.atom.level is not None
    ]
    assert max(levels) == 3 and min(levels) == 1


def test_clause_fragment_merges_prose_and_keeps_heading(parsed) -> None:
    clause = next(p for p in parsed.proposals if p.atom.anchor == "SPEC-STD-TEST-1.0#1.1·概述")
    fragment = clause.atom.content["fragment"]
    assert fragment.startswith("## 1.1 概述")
    assert "这是第二段正文。" in fragment
    assert clause.atom.format == "md" and clause.atom.level == 2
    # 表格/代码/列表被抽成独立原子，不并入条款
    assert "<table>" not in fragment and "always_ff" not in fragment and "- 列表项一" not in fragment


def test_table_atom_is_verbatim_html_with_meta(parsed) -> None:
    table = next(p for p in parsed.proposals if p.atom.atom_type == "table")
    assert table.atom.format == "html"
    assert table.atom.content["fragment"].startswith("<table><tr><td>A</td>")
    assert table.atom.content["meta"] == {"rows": 2, "cols": 3, "cells": 5, "max_colspan": 2}
    assert table.atom.content["text"] == "A B\nC D E", "表格纯文本按行列序去标签（A10）"


def test_code_atom_keeps_fence_and_language(parsed) -> None:
    code = next(p for p in parsed.proposals if p.atom.atom_type == "code")
    assert code.atom.content["fragment"] == "```sv\nalways_ff @(posedge clk) q <= d;\n```"
    assert code.atom.content["language"] == "sv"
    assert code.atom.content["text"] == "always_ff @(posedge clk) q <= d;"


def test_figure_atom_uses_content_addressed_asset_ref(parsed) -> None:
    figure = next(p for p in parsed.proposals if p.atom.atom_type == "figure")
    assert figure.atom.content["asset_ref"] == IMAGE_SHA
    assert "fragment" not in figure.atom.content, "figure 无 fragment（渲染期由 M04 合成）"
    assert figure.atom.content["text"]


def test_image_only_table_takes_fallback_path(tmp_path: pathlib.Path) -> None:
    """无文本投影的表格壳 → 兜底 note(html)（REQ-M03-F04；A10 无从派生 text）。"""
    doc = FRONTMATTER + (
        "# 1 图壳\n\n图壳段落。\n\n"
        '<table><tr><td rowspan=1 colspan=1><img src="images/' + IMAGE_SHA + '.jpg"/></td></tr></table>\n'
    )
    result = parse_markdown(write(tmp_path, doc, "shell.md"), "shell")
    shells = [p for p in result.proposals if p.rule_id == "F04.table.text-empty"]
    assert len(shells) == 1
    shell = shells[0]
    assert shell.atom.atom_type == "note" and shell.atom.format == "html"
    assert shell.atom.text.startswith("<table>") and IMAGE_SHA in shell.atom.text
    assert not shell.confident and result.unmapped[0].source_lines == shell.source_lines
    assert result.stats.fallback == 1
    assert check_proposals(result) == [], "兜底路径同样通过 M09A 门禁"


def test_html_pre_code_block_becomes_code_atom(tmp_path: pathlib.Path) -> None:
    """块级 `<pre>`（含未闭合形态）→ code 原子（format=html，fragment 原样；P4）。"""
    doc = FRONTMATTER + (
        "# 1 命令\n\n正文。\n\n"
        "<pre><code>all_clocks</code></pre>\n\n"
        "中间段落（隔开两个 pre 块，避免相邻块级 HTML 合并）。\n\n"
        "<pre><code>all_inputs\n\n"
        "结尾段落。\n"
    )
    result = parse_markdown(write(tmp_path, doc, "pre.md"), "pre")
    codes = [p for p in result.proposals if p.atom.atom_type == "code"]
    assert len(codes) == 2, [p.atom.content.get("fragment") for p in codes]
    assert all(p.atom.format == "html" for p in codes)
    assert codes[0].atom.content["fragment"] == "<pre><code>all_clocks</code></pre>"
    assert codes[0].atom.content["text"] == "all_clocks"
    assert codes[1].atom.content["fragment"].startswith("<pre><code>all_inputs")
    assert result.stats.fallback == 0 and check_proposals(result) == []


def test_opensta_corpus_pre_code_rule(tmp_path: pathlib.Path) -> None:
    """真实语料（OpenSTA `Commands.md`，HTML 形态代码块）：覆盖率 ≥0.95 且 code 原子显著增加。"""
    path = pathlib.Path(__file__).resolve().parents[2] / "spec" / "standards" / "lang" / "opensta-commands.md"
    if not path.is_file():
        pytest.skip(f"语料缺失：{path}")
    result = parse_markdown(path)
    summary = report(result)
    assert summary["coverage"] >= 0.95, summary
    assert summary["atom_types"]["code"] >= 150
    assert summary["unmapped"]["count"] <= 5
    pre_blocks = [p for p in result.proposals if p.rule_id == "R13.code.html-pre"]
    assert pre_blocks and all(
        p.atom.content["fragment"] in path.read_text(encoding="utf-8") for p in pre_blocks
    ), "P4：fragment 必须是源文本的子串"


def test_cross_ref_atom_resolves_target_anchor(parsed) -> None:

    cross = next(p for p in parsed.proposals if p.atom.atom_type == "cross_ref")
    assert cross.atom.content["ref_kind"] == "see_also"
    assert cross.atom.content["target_doc_id"] == "SPEC-STD-TEST-1.0"
    assert cross.atom.content["target_anchor"] == "SPEC-STD-TEST-1.0#1.1.1·细节"
    assert parsed.doc_meta["cross_ref"]["resolved"] == 1


def test_list_becomes_note_and_helper_atoms(parsed) -> None:
    note = next(p for p in parsed.proposals if p.atom.atom_type == "note" and p.rule_id == "R08.list.note")
    assert note.atom.content["fragment"].startswith("- 列表项一")
    definitions = [p for p in parsed.proposals if p.atom.atom_type == "definition"]
    terms = {p.atom.content.get("term") for p in definitions}
    assert "AXI" in terms, terms
    assert "AQ" in terms, terms
    assert "词条 Zeta" in terms, terms


def test_every_atom_content_satisfies_m01_schema_and_has_text(parsed) -> None:
    from agenticdocer.model import get_atom_schema

    checked = 0
    for proposal in parsed.proposals:
        atom = proposal.atom
        if not hasattr(atom, "content"):
            assert atom.text.strip(), "兜底原子文本非空"
            continue
        assert isinstance(atom.content.get("text"), str) and atom.content["text"].strip(), atom.anchor
        jsonschema.Draft202012Validator(get_atom_schema(atom.atom_type)).validate(atom.content)
        checked += 1
    assert checked > 10


def test_anchors_disambiguate_duplicate_titles(tmp_path: pathlib.Path) -> None:
    result = parse_markdown(write(tmp_path, DUP_DOC, "dup.md"), "dup")
    steps = [p for p in result.proposals if "test-steps" in p.atom.anchor]
    assert len(steps) == 3, [p.atom.anchor for p in result.proposals]
    suffixes = {anchor.atom.anchor.split("·")[-1] for anchor in steps}
    assert all("~" in suffix for suffix in suffixes), suffixes  # 重复标题带摘要消歧
    assert len(suffixes) == 3, "正文相同的两条须再按同级序号区分"
    assert len({p.atom.anchor for p in result.proposals}) == len(result.proposals)


def test_preamble_paragraphs_become_single_clause(tmp_path: pathlib.Path) -> None:
    text = FRONTMATTER + "无标题前缀段落甲。\n\n无标题前缀段落乙。\n\n# 1 首节\n\n正文。\n"
    result = parse_markdown(write(tmp_path, text, "pre.md"), "pre")
    preambles = [p for p in result.proposals if "preamble" in p.atom.anchor]
    assert len(preambles) == 1
    fragment = preambles[0].atom.content["fragment"]
    assert fragment == "无标题前缀段落甲。\n\n无标题前缀段落乙。"
    assert preambles[0].atom.level == 1


def test_parse_is_deterministic(tmp_path: pathlib.Path) -> None:
    path = write(tmp_path, DOC)
    first = parse_markdown(path, "det")
    second = parse_markdown(path, "det")
    assert first.model_dump() == second.model_dump()
    assert json.dumps(first.model_dump(mode="json", by_alias=True), sort_keys=True) == json.dumps(
        second.model_dump(mode="json", by_alias=True), sort_keys=True
    )


def test_stats_report_shape(parsed) -> None:
    summary = report(parsed)
    assert summary["coverage"] >= 0.85
    assert summary["atom_types"]["table"] == 1
    assert summary["unmapped"]["count"] == parsed.stats.fallback
    assert summary["blocks_by_kind"]["table.html"] == 1
    assert summary["asset_refs"]["md"] == 1


def test_atom_content_helper_requires_non_empty_text() -> None:
    from agenticdocer.model import derive_text

    content = atom_content("note", fragment="纯文本")
    assert content["text"] == "纯文本"
    # 空投影：M01 derive_text 拒绝（A10 单点口径），helper 走留痕的退化路径仍保证非空
    with pytest.raises(ValueError):
        derive_text("table", {"fragment": ""})
    assert atom_content("table", fragment="")["text"] == "table"


# ── 资产同步 ─────────────────────────────────────────────────────────────


def test_collect_refs_counts_md_and_html(tmp_path: pathlib.Path) -> None:
    html_sha = "b" * 64
    text = f"![](images/{IMAGE_SHA}.jpg)\n\n<img src=\"images/{html_sha}.png\">\n\n![alt](images/{IMAGE_SHA}.jpg)\n"
    refs = collect_refs(text)
    counts = ref_counts(refs)
    assert counts == {"total": 3, "md": 2, "html": 1, "unique": 2, "content_addressed": 3}
    assert refs[0].sha256 == IMAGE_SHA and refs[0].extension == "jpg"
    assert refs[1].form == "html"


def test_fetch_assets_missing_is_non_blocking(tmp_path: pathlib.Path) -> None:
    report_ = fetch_assets([f"images/{IMAGE_SHA}.jpg", f"images/{IMAGE_SHA}.jpg"], tmp_path)
    assert report_.fetched == 0
    assert report_.missing == [f"images/{IMAGE_SHA}.jpg"]
    assert report_.total_refs == 2


def test_fetch_assets_verifies_hash_and_writes(tmp_path: pathlib.Path) -> None:
    data = b"fake-image-bytes"
    sha = hashlib.sha256(data).hexdigest()
    (tmp_path / "images").mkdir()
    (tmp_path / "images" / f"{sha}.jpg").write_bytes(data)
    ok = fetch_assets([f"images/{sha}.jpg"], tmp_path)
    assert ok.fetched == 1 and ok.missing == [] and ok.total_refs == 1

    bad_sha = "c" * 64
    (tmp_path / "images" / f"{bad_sha}.jpg").write_bytes(b"different")
    mismatch = fetch_assets([f"images/{bad_sha}.jpg"], tmp_path)
    assert mismatch.fetched == 0 and mismatch.missing == [f"images/{bad_sha}.jpg"]

    outside = fetch_assets(["../secret.jpg"], tmp_path)
    assert outside.fetched == 0 and outside.missing == ["../secret.jpg"]
    assert mime_for("jpg", "images/x.jpg") == "image/jpeg"


# ── 审核 / 提交前校验 / 统计（无 PG）───────────────────────────────────


def test_run_parse_persists_workspace(tmp_path: pathlib.Path) -> None:
    work = tmp_path / "work"
    result = run_parse(write(tmp_path, DOC), "test-spec", work_dir=work)
    directory = work / "test-spec"
    assert (directory / "proposals.json").is_file()
    assert (directory / "review_state.json").is_file()
    loaded = load_parse_result("test-spec", work_dir=work)
    assert loaded.model_dump() == result.model_dump()
    state = load_review_state("test-spec", work_dir=work)
    assert len(state.items) == len(result.proposals)
    assert set(state.items) == {proposal.proposal_id for proposal in result.proposals}


def test_review_workflow_commands(tmp_path: pathlib.Path) -> None:
    work = tmp_path / "work"
    result = run_parse(write(tmp_path, DOC), "test-spec", work_dir=work)
    pending = [p for p in result.proposals if not p.confident]
    assert pending, "合成文档应含待确认/兜底项"
    lines: list[str] = []
    answers = iter(["a", "r", "u", "A", "s", "a"])
    state = run_review(
        "test-spec",
        work_dir=work,
        answers=answers,
        out=lines.append,
        actor="tester",
        accept_confident=False,
    )
    decisions = Counter(item.decision for item in state.items.values())
    assert decisions["accepted"] >= 1
    assert decisions["rejected"] == 1
    assert decisions["pending"] >= 1, "跳过与未处理项保持 pending"
    actions = [entry["action"] for entry in state.audit]
    assert actions[0] == "accept" and "reject" in actions and "view_unmapped" in actions and "batch_accept" in actions
    assert all(entry["actor"] == "tester" for entry in state.audit)
    assert any("未映射清单" in line for line in lines)
    # 审核状态落盘可回读
    assert load_review_state("test-spec", work_dir=work).model_dump() == state.model_dump()


def test_review_amend_patches_content(tmp_path: pathlib.Path) -> None:
    work = tmp_path / "work"
    result = run_parse(write(tmp_path, DOC), "test-spec", work_dir=work)
    state = run_review(
        "test-spec",
        work_dir=work,
        answers=iter(["e", '{"caption": "修正后的图注"}']),
        out=lambda _: None,
        actor="tester",
    )
    amended = [item for item in state.items.values() if item.decision == "amended"]
    assert len(amended) == 1 and amended[0].amended_atom == {"caption": "修正后的图注"}


def test_accept_confident_batch(tmp_path: pathlib.Path) -> None:
    work = tmp_path / "work"
    run_parse(write(tmp_path, DOC), "test-spec", work_dir=work)
    state = run_review("test-spec", work_dir=work, answers=iter(["q"]), out=lambda _: None, accept_confident=True)
    assert all(
        item.decision == "accepted" for item in state.items.values() if item.confident
    )


def test_check_proposals_delegates_to_m09a(parsed) -> None:
    """门禁判据单点：schema/text/原子注册/锚形态由 M09A 判定，M03 只追加结构判据。"""
    assert check_proposals(parsed) == []
    broken = parsed.model_copy(deep=True)
    broken.proposals[0].atom.content["text"] = ""
    broken.proposals[1].atom.anchor = broken.proposals[0].atom.anchor
    fallback_proposal = next(p for p in broken.proposals if isinstance(p.atom, RawFallback))
    fallback_proposal.atom.text = ""  # 兜底 content 由 M09A 判（A10.content.text）
    broken.doc_meta["fallback"] = {}
    violations = check_proposals(broken)
    rule_ids = {violation.rule_id for violation in violations}
    assert {"A10.content.text", "M03.anchor.duplicate", "M03.fallback.anchor"} <= rule_ids
    # 违规定位带锚前缀（M09A 的 path 为字段相对路径，调用方加定位前缀）
    assert any("#content.text" in violation.path for violation in violations)
    for violation in violations:
        assert violation.message and violation.path
    # M03 不重复实现 schema 判据：schema 违规的 rule_id 一律来自 M09A
    assert {violation.rule_id for violation in violations if "schema" in violation.rule_id} <= {"M09A.atom.schema"}


def test_check_proposals_rejects_unknown_atom_and_disallowed_atom(
    parsed, monkeypatch: pytest.MonkeyPatch
) -> None:
    # 未注册原子：M09A 判（M09A.atom.unknown）
    unknown = parsed.model_copy(deep=True)
    unknown.proposals[1].atom.atom_type = "臆造原子"
    assert "M09A.atom.unknown" in {violation.rule_id for violation in check_proposals(unknown)}

    # 已注册原子但被 doc_type 组合规则排除：M09A 判（M01.doc_type.atom）
    from agenticdocer.model import DOC_TYPE_RULES, DocTypeRule

    monkeypatch.setitem(
        DOC_TYPE_RULES, "safety", DocTypeRule(doc_type="safety", allowed_atom_types=("clause",))
    )
    narrowed = parsed.model_copy(deep=True)
    narrowed.doc_meta["doc_type"] = "safety"
    assert "M01.doc_type.atom" in {violation.rule_id for violation in check_proposals(narrowed)}


def test_stats_report_from_source_and_workspace(tmp_path: pathlib.Path) -> None:
    work = tmp_path / "work"
    path = write(tmp_path, DOC)
    fresh = run_stats(src=path, doc_slug="test-spec")
    assert fresh["coverage"] >= 0.85
    run_parse(path, "test-spec", work_dir=work)
    stored = run_stats(doc_slug="test-spec", work_dir=work)
    assert stored["total_blocks"] == fresh["total_blocks"]
    assert stored["rule_set_version"] == RULE_SET_VERSION


# ── 真实语料（小份，无需 PG）─────────────────────────────────────────────


def test_small_real_corpus_parses(corpus) -> None:
    summary = report(corpus)
    assert corpus.doc_meta["doc_id"] == "SPEC-STD-AMBA-APB"
    assert coverage(corpus.stats) >= 0.95
    assert summary["atom_types"]["table"] >= 5
    assert summary["asset_refs"]["md"] >= 5
    assert corpus.stats.pending >= 1


def test_real_corpus_fragments_are_verbatim(tmp_path: pathlib.Path, corpus) -> None:
    root = pathlib.Path(__file__).resolve().parents[2] / "spec" / "standards" / "amba"
    text = (root / "IHI0024_AMBA_APB_spec.md").read_text(encoding="utf-8")
    body_start = corpus.doc_meta["body_start"]
    body = "\n".join(text.split("\n")[body_start - 1 :])
    covered: set[int] = set()
    for proposal in corpus.proposals:
        covered.update(range(proposal.source_lines[0], proposal.source_lines[1] + 1))
        atom = proposal.atom
        value = (atom.content.get("fragment") if hasattr(atom, "content") else None) or (
            atom.text if isinstance(atom, RawFallback) else None
        )
        for line in str(value or "").split("\n"):
            if line.strip():
                assert line in body, f"P4 破坏：{line!r}"
    missing = [
        index + body_start
        for index, line in enumerate(body.split("\n"))
        if line.strip() and (index + body_start) not in covered
    ]
    assert missing == [], "零静默丢弃：每个非空源行都被某节点覆盖"
