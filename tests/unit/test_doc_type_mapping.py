"""方案 C 的 (a) 追溯 + (c) UCIS/vPlan 落实验收（M03 导入/映射层）。

逐条对照 `spec/arch_spec/doc_type_mapping.md`（权威依据）：本文件**直接从 §2 的 Markdown 表格**
解析出行标签、`doc_type` 与「首版状态」，与 `importer/doc_type_map.py` 的机器可读映射表对照——
表格改了而代码没跟上（或反之）即红，映射不会散落成两套口径。

覆盖：
1. §2 映射表的**逐行落实**（idea.md 30+ 类型 → 5 个 `doc_type`，不新增 `doc_type`）；
2. frontmatter 的 `spec_type` 归一（slug/别名/大小写）与 `product` 细分 `meta.doc_subtype` 落位；
3. §4 的 UCIS/vPlan：`table.coverage_matrix` 的解析、原子构造与反向导出；
4. `standard` 的既有导入路径零变化（+ 无关 doc_type 的导入不被阻断）。

**验证边界**（映射表 §5，如实声明）：本文件全部为**合成样例**（手写 frontmatter 文本 +
手写 vPlan XML，非真实语料）。`spec/standards/` 中没有 `lang`/`tool-manual`/`product`/`safety`
与 vPlan/UCIS 的真实文件，故**不构成端到端验证**；真实语料的端到端验证只有 `standard`
（7 份，见 `tests/integration/test_import_pipeline.py`、`tests/unit/test_parser.py`）。
"""

from __future__ import annotations

import pathlib
import re

import jsonschema
import pytest

from agenticdocer.importer import parse_text
from agenticdocer.importer.doc_type_map import (
    ALIASES,
    IDEA_DOC_TYPES,
from agenticdocer.importer import check_proposals, parse_text
    PRODUCT_SUBTYPES,
    RESOLVABLE_KEYS,
    SPEC_ROWS,
    STANDARDS,
    STATUS_DELIVERED,
    STATUS_REGISTERED,
    STATUS_SPECIFIED,
    STATUSES,
    VERIFICATION_PLAN_FORMATS,
    VERIFICATION_PLAN_SUBTYPE,
    UnknownDocTypeError,
    invalid_verification_plan_format,
    missing_verification_plan_meta,
    resolve_doc_type,
    subtypes_for,
)
from agenticdocer.importer.frontmatter import doc_in_from_meta, parse_frontmatter
from agenticdocer.importer.vplan import (
    COVERAGE_MATRIX_ATOM,
    MATRIX_FIELDS,
    UNASSIGNED_TEST,
    UNNAMED,
    UNKNOWN_STATUS,
    coverage_matrix_atom,
    coverage_matrix_content,
    parse_vplan,
)
from agenticdocer.model import DOC_TYPES, get_atom_schema
from agenticdocer.store import ValidationError

ROOT = pathlib.Path(__file__).resolve().parents[2]
MAPPING_DOC = ROOT / "spec" / "arch_spec" / "doc_type_mapping.md"
SECTION_TWO = re.compile(r"^## 2\. 映射表", re.MULTILINE)

# ---------------------------------------------------------------- §2 映射表


def _section_two_rows() -> list[tuple[str, str, str]]:
    """`doc_type_mapping.md` §2 表格 → ``(类型标签, doc_type, 首版状态原文)``。"""
    text = MAPPING_DOC.read_text(encoding="utf-8")
    start = SECTION_TWO.search(text)
    assert start is not None, f"映射表 §2 标题缺失：{MAPPING_DOC}"
    rest = text[start.start() :]
    following = rest.find("\n## ", 1)
    section = rest if following == -1 else rest[:following]
    rows: list[tuple[str, str, str]] = []
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 4 or cells[0].startswith("idea.md") or set(cells[1]) <= set("-: "):
            continue
        rows.append((cells[0], cells[1].strip("`"), cells[3]))
    return rows


def _expected_status(cell: str) -> str:
    """§2「首版状态」原文 → 机器可读状态（`已交付` → delivered，`登记` → registered）。"""
    if "已交付" in cell:
        return STATUS_DELIVERED
    if "登记" in cell:
        return STATUS_REGISTERED
    return STATUS_SPECIFIED


def test_section_two_table_rows_all_implemented() -> None:
    """§2 每行都有实现，且 `doc_type`/首版状态与表格逐行一致（防遗漏、防漂移）。"""
    rows = _section_two_rows()
    assert len(rows) >= 15, "§2 映射表行数异常（表格被改？）"
    for label, doc_type, status_cell in rows:
        entries = [mapping for mapping in IDEA_DOC_TYPES if mapping.spec_row == label]
        assert entries, f"映射表 §2 行未落实：{label!r}"
        assert {entry.doc_type for entry in entries} == {doc_type}, f"{label}: doc_type 不一致"
        assert {entry.status for entry in entries} == {_expected_status(status_cell)}, (
            f"{label}: 首版状态与 §2 表格不一致"
        )


def test_spec_rows_match_parsed_table() -> None:
    """`SPEC_ROWS`（代码侧行标签）与 §2 表格标签集合逐字相等。"""
    assert set(SPEC_ROWS) == {label for label, _, _ in _section_two_rows()}
    assert len(SPEC_ROWS) == len(set(SPEC_ROWS))


def test_mapping_entries_are_well_formed() -> None:
    """条目自洽：slug 唯一、`doc_type` 在取值域（**只有 5 值**）、细分唯一、标准/字段齐备。"""
    slugs = [mapping.slug for mapping in IDEA_DOC_TYPES]
    assert len(set(slugs)) == len(slugs), "slug 必须唯一"
    subtypes = [mapping.doc_subtype for mapping in IDEA_DOC_TYPES if mapping.doc_subtype]
    assert len(set(subtypes)) == len(subtypes), "doc_subtype 是全局取值域，不得重名"
    assert {mapping.doc_type for mapping in IDEA_DOC_TYPES} == set(DOC_TYPES), (
        "idea.md 的类型必须覆盖且只覆盖 5 个 doc_type（不新增 doc_type）"
    )
    for mapping in IDEA_DOC_TYPES:
        assert mapping.status in STATUSES
        assert mapping.standard in STANDARDS, f"{mapping.slug} 未标注参考标准（idea.md §8）"
        assert mapping.idea_fields, f"{mapping.slug} 未记录 idea.md §4.5 关键字段"
        assert mapping.slug == mapping.slug.lower().strip()
        if mapping.doc_type == "product":
            assert mapping.doc_subtype, "product 大类必须有细分（meta.doc_subtype）"
        elif mapping.doc_subtype is None:
            assert mapping.doc_type in DOC_TYPES


def test_aliases_do_not_shadow_slugs_or_doc_types() -> None:
    """别名表自洽：小写、指向已登记 slug，且不与 slug/`doc_type` 值重名（重名会被静默覆盖）。"""
    for alias, slug in ALIASES.items():
        assert alias == alias.strip().lower()
        assert alias not in MAPPINGS_BY_SLUG, f"别名 {alias!r} 与 slug 重名"
        assert alias not in DOC_TYPES, f"别名 {alias!r} 与 doc_type 值重名"
        assert slug in MAPPINGS_BY_SLUG, f"别名 {alias!r} 指向未登记 slug {slug!r}"
    assert RESOLVABLE_KEYS == {*DOC_TYPES, *MAPPINGS_BY_SLUG, *ALIASES}


# ---------------------------------------------------------------- spec_type 归一


@pytest.mark.parametrize("mapping", IDEA_DOC_TYPES, ids=lambda mapping: mapping.slug)
def test_every_slug_resolves(mapping) -> None:
    """映射表 §2 的每个类型都能被 frontmatter 归一（大小写/空白宽松）。"""
    for raw in (mapping.slug, mapping.slug.upper(), f"  {mapping.slug}  "):
        resolution = resolve_doc_type(raw)
        assert resolution.doc_type == mapping.doc_type
        assert resolution.doc_subtype == mapping.doc_subtype
        assert resolution.mapping is mapping
        assert not resolution.canonical


@pytest.mark.parametrize(("alias", "slug"), sorted(ALIASES.items()))
def test_every_alias_resolves(alias: str, slug: str) -> None:
    """别名（人工/agent 的常见写法）同样归一到同一 `(doc_type, doc_subtype)`。"""
    expected = MAPPINGS_BY_SLUG[slug]
    resolution = resolve_doc_type(alias)
    assert (resolution.doc_type, resolution.doc_subtype) == (
        expected.doc_type,
        expected.doc_subtype,
    )


@pytest.mark.parametrize("doc_type", DOC_TYPES)
def test_doc_type_values_resolve_canonically(doc_type: str) -> None:
    """5 个 `doc_type` 值本身仍是合法 `spec_type`（且不推断细分 → `standard` 路径零变化）。"""
    resolution = resolve_doc_type(doc_type)
    assert resolution.canonical
    assert resolution.doc_type == doc_type
    assert resolution.doc_subtype is None


@pytest.mark.parametrize("raw", ["novel", "", "  ", "test_plan", "architecure-spec"])
def test_unknown_spec_type_is_rejected(raw: str) -> None:
    with pytest.raises(UnknownDocTypeError):
        resolve_doc_type(raw)


# ---------------------------------------------------------------- frontmatter（合成样例）

C5_TEMPLATE = """---
title: {title}
type: composite
purpose: spec
audience: both
direction: input
status: draft
version: "0.1.0"
section_meta: "@meta"
spec_id: {spec_id}
spec_type: {spec_type}
spec_org: INTERNAL
spec_revision: "r0"
source: corpus/internal/{spec_id}.md
converted_by: unit-test
converted_at: 2026-09-17
reviewed_by: unit-test
reviewed_at: 2026-09-17
{extra}---
"""


def _doc(spec_type: str, *, extra: str = "", spec_id: str = "SPEC-UNIT-1.0") -> str:
    """合成 frontmatter（非真实语料）+ 一段正文。"""
    return C5_TEMPLATE.format(title="单元样例", spec_id=spec_id, spec_type=spec_type, extra=extra)


PRODUCT_EXTRA = "traces_to: [PRD-DEMO-1]\nowner: alice\n"
LANG_EXTRA = 'command_name: "create_clock"\nsyntax: "create_clock [-period p]"\ntool_context: "VendorX 2024.1"\n'
SAFETY_EXTRA = 'standard_ref: "ISO 26262-5:2018 §7"\naudit_trail: "review-42"\n'


def test_standard_canonical_path_is_unchanged() -> None:
    """`spec_type: standard` 的导入路径零变化：`meta` = frontmatter 全量 + `doc_slug`，无细分键。"""
    fm = parse_frontmatter(_doc("standard"), doc_slug="std")
    assert fm.doc_type == "standard"
    assert fm.doc_subtype is None
    assert set(fm.meta) == {*fm.fields, "doc_slug"}
    assert fm.doc_meta["doc_subtype"] is None
    assert doc_in_from_meta(fm.doc_meta).meta == fm.meta


@pytest.mark.parametrize(
    ("spec_type", "doc_type", "doc_subtype", "extra"),
    [
        ("mas", "product", "mas", PRODUCT_EXTRA),
        ("verification-plan", "product", "verification-plan", f"{PRODUCT_EXTRA}verification_plan_format: vplan\n"),
        ("eda-manual", "tool-manual", "eda-command-ref", LANG_EXTRA),
        ("lang-manual", "lang", "lang-manual", LANG_EXTRA),
        ("pdk-doc", "standard", "pdk-doc", ""),
        ("fmea", "safety", "fmea-fta", SAFETY_EXTRA),
    ],
)
def test_alias_spec_type_lands_in_doc_type_and_meta(
    spec_type: str, doc_type: str, doc_subtype: str, extra: str
) -> None:
    """别名写法的 `spec_type` → 正确的 `doc_type`，细分落 `meta.doc_subtype`（往返不丢）。"""
    fm = parse_frontmatter(_doc(spec_type, extra=extra), doc_slug="alias")
    assert fm.doc_type == doc_type
    assert fm.doc_subtype == doc_subtype
    assert fm.meta["doc_subtype"] == doc_subtype
    assert fm.fields["spec_type"] == spec_type, "frontmatter 全量保真（原文不改写）"
    assert doc_in_from_meta(fm.doc_meta).meta["doc_subtype"] == doc_subtype


@pytest.mark.parametrize("subtype", PRODUCT_SUBTYPES)
def test_every_product_subtype_is_accepted(subtype: str) -> None:
    """`meta.doc_subtype` 的全部登记细分都可用（细分只加 `meta`，不新增 `doc_type`）。"""
    extra = f"{PRODUCT_EXTRA}doc_subtype: {subtype}\n"
    if subtype == VERIFICATION_PLAN_SUBTYPE:
        extra += "verification_plan_format: ucis\n"
    fm = parse_frontmatter(_doc("product", extra=extra), doc_slug="product")
    assert fm.doc_type == "product"
    assert fm.doc_subtype == subtype
    assert fm.meta["doc_subtype"] == subtype


def test_product_subtype_declared_explicitly_wins() -> None:
    """显式 `doc_subtype` 覆盖泛型 `spec_type: product`，并校验取值域。"""
    fm = parse_frontmatter(
        _doc("product", extra=f"{PRODUCT_EXTRA}doc_subtype: register-manual\n"), doc_slug="reg"
    )
    assert fm.doc_subtype == "register-manual"
    with pytest.raises(ValidationError, match="doc_subtype"):
        parse_frontmatter(
            _doc("standard", extra="doc_subtype: mas\n"),
            doc_slug="bad",
        )


def test_product_requires_subtype_traces_to_and_owner() -> None:
    """`product` 的必填项由 `model.doc_types` 单点判定（P5），frontmatter 只消费。"""
    with pytest.raises(ValidationError, match="doc_subtype"):
        parse_frontmatter(_doc("product", extra=PRODUCT_EXTRA), doc_slug="p1")
    with pytest.raises(ValidationError, match="traces_to"):
        parse_frontmatter(
            _doc("product", extra="owner: alice\ndoc_subtype: mas\n"), doc_slug="p2"
        )
    with pytest.raises(ValidationError, match="owner"):
        parse_frontmatter(
            _doc("product", extra="traces_to: [PRD-DEMO-1]\ndoc_subtype: mas\n"), doc_slug="p3"
        )


@pytest.mark.parametrize(
    ("spec_type", "extra", "missing"),
    [
        ("lang", "", "tool_context"),
        ("tool-manual", LANG_EXTRA, None),
        ("safety", SAFETY_EXTRA, None),
    ],
)
def test_lang_and_safety_required_meta(
    spec_type: str, extra: str, missing: str | None
) -> None:
    """`lang`/`tool-manual` 的命令级三元组与 `safety` 的安全元数据必填（映射表 §3）。"""
    if missing is None:
        fm = parse_frontmatter(_doc(spec_type, extra=extra), doc_slug=spec_type)
        assert fm.doc_type == spec_type
        return
    with pytest.raises(ValidationError, match=missing):
        parse_frontmatter(_doc(spec_type, extra=extra), doc_slug=spec_type)


def test_verification_plan_format_is_required_and_typed() -> None:
    """§4：`verification-plan` 子类型必填 `verification_plan_format`（ucis|vplan|native）。"""
    assert missing_verification_plan_meta({}) == ["verification_plan_format"]
    assert invalid_verification_plan_format({}) is None
    assert invalid_verification_plan_format({"verification_plan_format": "CSV"}) == "csv"
    for fmt in VERIFICATION_PLAN_FORMATS:
        parse_frontmatter(
            _doc(
                "verification-plan",
                extra=f"{PRODUCT_EXTRA}verification_plan_format: {fmt}\n",
            ),
            doc_slug="vp",
        )
    with pytest.raises(ValidationError, match="verification_plan_format"):
        parse_frontmatter(_doc("verification-plan", extra=PRODUCT_EXTRA), doc_slug="vp2")
    with pytest.raises(ValidationError, match="非法"):
        parse_frontmatter(
            _doc(
                "verification-plan",
                extra=f"{PRODUCT_EXTRA}verification_plan_format: csv\n",
            ),
            doc_slug="vp3",
        )


def test_unknown_spec_type_message_keeps_a22_wording() -> None:
    """未知 `spec_type` 仍报取值域（A22），且提示别名表（迁移友好）。"""
    with pytest.raises(ValidationError, match="spec_type"):
        parse_frontmatter(_doc("novel"), doc_slug="bad")


# ---------------------------------------------------------------- 导入不阻断


def test_standard_document_import_path_is_unaffected() -> None:
    """`standard` 的解析链路（frontmatter → 块 → 原子提议）不受新映射层影响。"""
    result = parse_text(
        _doc("standard") + "# 1 绪论\n\n这是正文段落，长度足够成为一个条款。\n",
        doc_slug="std",
    )
    assert result.doc_meta["doc_type"] == "standard"
    assert result.doc_meta["doc_subtype"] is None
    assert "doc_subtype" not in result.doc_meta["frontmatter"]
    assert [proposal.atom.atom_type for proposal in result.proposals] == ["clause"]


def test_non_standard_document_import_is_not_blocked() -> None:
    """非 `standard` 的文档在有必填 meta 时同样能走完整解析链路（不因新规则被挡）。"""
    result = parse_text(
        _doc("mas", extra=PRODUCT_EXTRA)
        + "# 1 数据通路\n\n描述模块的数据通路与流水线级数，长度足够。\n",
        doc_slug="mas",
    )
    assert result.doc_meta["doc_type"] == "product"
    assert result.doc_meta["doc_subtype"] == "mas"
    assert [proposal.atom.atom_type for proposal in result.proposals] == ["clause"]


# 合成样例（非真实语料）：正文仅用于触发提议路径，表为普通 table 而非 safety 的必备变体。
_FAILURE_MODE_BODY = (
    "# 1 安全分析\n\n失效模式与影响分析正文。\n\n"
    "<table><tr><th>failure_mode</th></tr><tr><td>stuck-at</td></tr></table>\n"
)


def test_required_atom_variants_are_enforced_in_proposal_path() -> None:
    """`safety` 的必备**变体** `table.failure_mode` 在提议路径被强制（M01.doc_type.required）。

    回归 SchemaValidate 报告的跨模块缺口：判据曾只查 `clause`，变体类必备项无人强制。
    """
    safety = parse_text(_doc("safety", extra=SAFETY_EXTRA) + _FAILURE_MODE_BODY, doc_slug="safety")
    violations = [item for item in check_proposals(safety) if item.rule_id == "M01.doc_type.required"]
    assert len(violations) == 1, "只缺 table.failure_mode（clause 已由标题命中）"
    assert "table.failure_mode" in violations[0].message
    standard = parse_text(_doc("standard") + _FAILURE_MODE_BODY, doc_slug="std2")
    assert "M01.doc_type.required" not in {item.rule_id for item in check_proposals(standard)}


# ---------------------------------------- §4 vPlan/UCIS（合成样例，非真实语料）

# 合成样例（非真实语料）：`spec/standards/` 中无 vPlan/UCIS 文件，故按映射表 §4 的层级手写。
VPLAN_XML = """<?xml version="1.0" encoding="UTF-8"?>
<vPlan name="demo-plan" version="1.0">
  <feature name="F1 数据通路">
    <sub_feature name="SF1 写通道">
      <coverage_item name="CI1 写响应顺序" status="covered">
        <test name="t_write_order" status="pass"/>
        <test name="t_write_order_stress" status="fail"/>
      </coverage_item>
      <coverage_item name="CI2 写超时" status="uncovered"/>
    </sub_feature>
    <sub_feature name="SF2 读通道">
      <coverage_item name="CI3 读重排" status="planned">
        <test name="t_read_reorder" status="planned"/>
      </coverage_item>
    </sub_feature>
  </feature>
  <feature name="F2 复位">
    <coverage_item name="CI4 复位序列" status="covered">
      <test name="t_reset" status="pass"/>
    </coverage_item>
  </feature>
</vPlan>
"""

UCIS_XML = """<ucis name="demo-ucis">
  <feature name="F1">
    <coverage_item name="CI1">
      <test name="t1" status="pass"/>
    </coverage_item>
    <coverage_item name="CI2">
      <test name="t2"/>
    </coverage_item>
  </feature>
</ucis>
"""


def test_parse_vplan_synthetic_sample() -> None:
    """合成 vPlan XML → 行数与层级正确（`feature→sub_feature→coverage_item→test`）。"""
    plan = parse_vplan(VPLAN_XML)
    assert plan.name == "demo-plan"
    assert plan.format == "vplan"
    assert len(plan.rows) == 5, "CI1×2 + CI2(缺口) + CI3 + CI4"
    assert [(row.feature, row.sub_feature, row.coverage_item, row.test) for row in plan.rows] == [
        ("F1 数据通路", "SF1 写通道", "CI1 写响应顺序", "t_write_order"),
        ("F1 数据通路", "SF1 写通道", "CI1 写响应顺序", "t_write_order_stress"),
        ("F1 数据通路", "SF1 写通道", "CI2 写超时", None),
        ("F1 数据通路", "SF2 读通道", "CI3 读重排", "t_read_reorder"),
        ("F2 复位", UNNAMED, "CI4 复位序列", "t_reset"),
    ]


def test_parse_vplan_status_and_gap_resolution() -> None:
    """状态口径：覆盖项状态优先（逐测试的判定保留在 `test_status`）；缺口显式留痕。"""
    plan = parse_vplan(VPLAN_XML)
    first = plan.rows[0]
    assert first.status == "covered", "coverage_item@status 优先"
    assert first.test_status == "pass", "test@status 保留，不丢测试判定"
    gaps = plan.coverage_gaps
    assert [row.coverage_item for row in gaps] == ["CI2 写超时"]
    assert gaps[0].is_gap and gaps[0].status == "uncovered"
    assert plan.rows[4].sub_feature == UNNAMED, "feature 直挂 coverage_item → 层级缺位占位"


def test_matrix_rows_are_complete_and_non_empty() -> None:
    """`matrix` 每行五字段齐备且非空（M01 变体 schema 要求 + 缺口用哨兵值）。"""
    plan = parse_vplan(VPLAN_XML)
    for row in plan.matrix_rows():
        assert set(row) == set(MATRIX_FIELDS)
        assert all(isinstance(value, str) and value.strip() for value in row.values())
    assert plan.matrix_rows()[2]["test"] == UNASSIGNED_TEST


def test_coverage_matrix_atom_conforms_to_model_schema() -> None:
    """原子构造合 M01 变体 schema（P5：schema 只在 model 定义，此处只消费）。"""
    plan = parse_vplan(VPLAN_XML)
    atom = coverage_matrix_atom(plan.rows)
    assert atom["atom_type"] == COVERAGE_MATRIX_ATOM
    assert atom["format"] == "html", "E1-a：fragment 是真实 <table> → format 必须是 html"
    content = atom["content"]
    jsonschema.validate(instance=content, schema=get_atom_schema(COVERAGE_MATRIX_ATOM))
    assert content["matrix"] == list(plan.matrix_rows())
    assert "<table" in content["fragment"]
    assert content["meta"] == {"rows": 6, "cols": 5, "cells": 30, "max_colspan": 1}
    assert "CI1 写响应顺序" in content["text"], "A10：content.text 由 M01 单点派生（非空）"


def test_coverage_matrix_content_rejects_empty_rows() -> None:
    with pytest.raises(ValidationError, match="至少一行"):
        coverage_matrix_content(())


def test_vplan_export_round_trips_rows() -> None:
    """反向导出（§4「导出若成本低」）：`parse(export(plan)) == plan`，逐字段不丢。"""
    plan = parse_vplan(VPLAN_XML)
    exported = plan.to_xml()
    assert exported.startswith("<?xml")
    assert "<feature name=" in exported and "<coverage_item" in exported
    again = parse_vplan(exported)
    assert again.rows == plan.rows
    assert again.name == plan.name
    assert again.matrix_rows() == plan.matrix_rows()


def test_ucis_root_and_status_fallback() -> None:
    """UCIS 根元素可用；状态口径：覆盖项缺 → 退测试状态 → 再缺为 `unknown`（不臆造）。"""
    plan = parse_vplan(UCIS_XML)
    assert plan.format == "ucis"
    assert [row.status for row in plan.rows] == ["pass", UNKNOWN_STATUS]
    assert [row.test_status for row in plan.rows] == ["pass", None]
    assert parse_vplan(UCIS_XML, name="override").name == "override"


@pytest.mark.parametrize(
    "xml_text",
    [
        "<not-a-plan><feature name='F'/></not-a-plan>",
        "<vPlan name='empty'/>",
        "<vPlan><feature name='F'></vPlan>",
        "<!DOCTYPE vPlan [<!ENTITY x 'y'>]><vPlan><feature name='F'/></vPlan>",
    ],
)
def test_vplan_rejects_malformed_input(xml_text: str) -> None:
    with pytest.raises(ValidationError):
        parse_vplan(xml_text)


def test_vplan_module_does_not_touch_model_schema() -> None:
    """P5：导入器不自建 schema——变体 schema 的键集合由 model 提供，导入器只引用其名。"""
    schema = get_atom_schema(COVERAGE_MATRIX_ATOM)
    assert set(schema["required"]) == {"text", "fragment", "meta", "matrix"}
    assert set(subtypes_for("product")) == set(PRODUCT_SUBTYPES)
