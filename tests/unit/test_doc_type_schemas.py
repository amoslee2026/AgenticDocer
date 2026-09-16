"""方案 C 的验收面：五类 doc_type 差异化规则 + 两个新原子变体（REQ-M01-F01/F03）。

逐条对照 `spec/arch_spec/doc_type_mapping.md` §3（五类差异化规则表）与 §4（UCIS/vPlan 对齐）；
字段来源 `spec/idea/idea.md` §4.1（DocBook `RefEntry`）、§4.3（UCIS/vPlan）、§4.5（逐类型字段）。

**验证边界**（映射文档 §5，如实声明）：`lang` / `tool-manual` / `product` / `safety` 与 UCIS/vPlan
在 `spec/standards/` 中**没有真实语料**，本文件只是 schema 定义 + 合成样例的单元验证，
**不构成端到端验证**——只有 `standard` 有 7 份真实语料可做导入→存储→渲染逐字节验证。
"""

from __future__ import annotations

import jsonschema
import pytest

import agenticdocer.model.doc_types as doc_types_module
from agenticdocer.model import (
    ATOM_SCHEMAS,
    ATOM_TYPES,
    ATOM_VARIANTS,
    C5_META_FIELDS,
    DOC_TYPE_RULES,
    DOC_TYPES,
    TABLE_ATOMS,
    DocTypeRule,
    allowed_atom_variants,
    derive_text,
    get_doc_type_rule,
    html_to_text,
    is_atom_allowed,
    is_variant_allowed,
    missing_required_meta,
    register_doc_type_rule,
)

# ── 映射表 §3 的逐条口径（期望值在此**独立书写**，与 doc_types.py 对照，避免同源假绿）──

LANG_BASES: tuple[str, ...] = ("clause", "definition", "table", "code", "example", "note", "cross_ref")
"""§4.1 语法手册基底原子：八类去掉 `figure`。"""

EXPECTED: dict[str, dict[str, object]] = {
    "standard": {
        "allowed": frozenset(ATOM_TYPES),
        "variants": ("table.register_field", "figure.state_machine"),
        "required_atoms": ("clause",),
        "meta": C5_META_FIELDS,
    },
    "lang": {
        "allowed": frozenset(LANG_BASES),
        "variants": (),
        "required_atoms": ("clause",),
        "meta": ("command_name", "syntax", "tool_context"),
    },
    "tool-manual": {
        "allowed": frozenset({*LANG_BASES, "figure"}),
        "variants": (),
        "required_atoms": ("clause",),
        "meta": ("command_name", "syntax", "tool_context"),
    },
    "product": {
        "allowed": frozenset(ATOM_TYPES),
        "variants": ("table.register_field", "figure.state_machine", "table.coverage_matrix"),
        "required_atoms": ("clause",),
        "meta": ("doc_subtype", "traces_to", "owner"),
    },
    "safety": {
        "allowed": frozenset(ATOM_TYPES),
        "variants": ("table.failure_mode",),
        "required_atoms": ("clause", "table.failure_mode"),
        "meta": ("standard_ref", "audit_trail"),
    },
}


# ── 1. 五类规则逐条验证（映射表 §3）────────────────────────────────────────


@pytest.mark.parametrize("doc_type", DOC_TYPES)
def test_rule_matches_mapping_table_section_3(doc_type: str) -> None:
    rule = get_doc_type_rule(doc_type)
    expected = EXPECTED[doc_type]

    assert set(rule.allowed_atom_types) == expected["allowed"]
    assert rule.allowed_atom_variants == expected["variants"]
    assert rule.required_atom_types == expected["required_atoms"]
    assert rule.required_meta_fields == expected["meta"]


@pytest.mark.parametrize("doc_type", DOC_TYPES)
def test_required_meta_gap_reporting_follows_the_rule(doc_type: str) -> None:
    rule = get_doc_type_rule(doc_type)

    assert missing_required_meta(doc_type, {}) == list(rule.required_meta_fields)
    assert missing_required_meta(doc_type, None) == list(rule.required_meta_fields)
    complete = dict.fromkeys(rule.required_meta_fields, "x")
    assert missing_required_meta(doc_type, complete) == []
    assert missing_required_meta(doc_type, {**complete, "extra": "x"}) == []


def test_required_meta_reports_only_the_missing_ones() -> None:
    assert missing_required_meta("lang", {"command_name": "create_clock"}) == ["syntax", "tool_context"]
    assert missing_required_meta("safety", {"audit_trail": "AUD-1"}) == ["standard_ref"]
    assert missing_required_meta("product", {"doc_subtype": "prd", "owner": "lxx"}) == ["traces_to"]


def test_doc_type_domain_stays_at_five_values() -> None:
    """收敛原则（映射表 §2）：不新增第 6 个 doc_type；product 细分走 `meta.doc_subtype`。"""
    assert DOC_TYPES == ("standard", "lang", "tool-manual", "product", "safety")
    assert set(DOC_TYPE_RULES) == set(DOC_TYPES)
    with pytest.raises(KeyError):
        get_doc_type_rule("whitepaper")


# ── 2. 差异化确实生效（防退回「空壳」）─────────────────────────────────────


def test_five_rules_are_not_five_clones_of_standard() -> None:
    """映射文档 §1 缺陷 1 的回归防线：五类签名互异，且非 standard 类**不得**等于 standard 的两元组。"""
    signatures = {
        (rule.allowed_atom_types, rule.required_meta_fields, rule.allowed_atom_variants)
        for rule in DOC_TYPE_RULES.values()
    }
    assert len(signatures) == len(DOC_TYPES)

    baseline = get_doc_type_rule("standard")
    for doc_type in DOC_TYPES:
        if doc_type == "standard":
            continue
        rule = get_doc_type_rule(doc_type)
        assert (
            rule.allowed_atom_types,
            rule.required_meta_fields,
        ) != (
            baseline.allowed_atom_types,
            baseline.required_meta_fields,
        ), f"{doc_type} 与 standard 全等（空壳差异化）"


@pytest.mark.parametrize("doc_type", DOC_TYPES)
def test_variant_whitelist_is_enforced_per_doc_type(doc_type: str) -> None:
    """变体不随基底原子自动放行：`table.failure_mode` 只属 `safety`，`table.coverage_matrix` 只属 `product`。"""
    rule = get_doc_type_rule(doc_type)
    for variant in ATOM_VARIANTS:
        expected = variant in EXPECTED[doc_type]["variants"] and variant.split(".", 1)[0] in rule.allowed_atom_types
        assert is_variant_allowed(doc_type, variant) is expected
        assert is_atom_allowed(doc_type, variant) is expected
    assert set(allowed_atom_variants(doc_type)) == set(EXPECTED[doc_type]["variants"])


def test_lang_and_tool_manual_differ_by_figure_and_share_command_meta() -> None:
    """§4.1 + §4.5 尾注：工具手册 = 语法手册 + `figure`；`tool_context`（厂商+版本）两者皆必填。"""
    lang, tool_manual = get_doc_type_rule("lang"), get_doc_type_rule("tool-manual")

    assert set(tool_manual.allowed_atom_types) - set(lang.allowed_atom_types) == {"figure"}
    assert tool_manual.required_meta_fields == lang.required_meta_fields
    assert "tool_context" in tool_manual.required_meta_fields
    assert allowed_atom_variants("lang") == allowed_atom_variants("tool-manual") == ()


def test_unknown_variants_and_atoms_are_never_allowed() -> None:
    for doc_type in DOC_TYPES:
        assert not is_atom_allowed(doc_type, "table.typo")
        assert not is_atom_allowed(doc_type, "not-an-atom")
        assert not is_variant_allowed(doc_type, "clause")
        assert not is_variant_allowed(doc_type, "table.register_field.typo")


def test_register_rule_validates_variant_whitelist(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(doc_types_module, "DOC_TYPE_RULES", dict(DOC_TYPE_RULES))

    register_doc_type_rule(
        DocTypeRule(
            doc_type="lang",
            allowed_atom_types=LANG_BASES,
            allowed_atom_variants=("table.register_field",),
        )
    )
    assert allowed_atom_variants("lang") == ("table.register_field",)
    assert is_atom_allowed("lang", "table.register_field")

    with pytest.raises(ValueError, match="未注册变体"):
        register_doc_type_rule(
            DocTypeRule(
                doc_type="lang",
                allowed_atom_types=LANG_BASES,
                allowed_atom_variants=("table.typo",),
            )
        )
    with pytest.raises(ValueError, match="基底未放行"):
        register_doc_type_rule(
            DocTypeRule(
                doc_type="lang",
                allowed_atom_types=("clause",),
                allowed_atom_variants=("table.register_field",),
            )
        )
    with pytest.raises(ValueError, match="超出允许集合"):
        register_doc_type_rule(
            DocTypeRule(doc_type="lang", allowed_atom_types=LANG_BASES, required_atom_types=("figure",))
        )


# ── 3. 新变体 schema 良构 + 合成样例 ────────────────────────────────────────

FAILURE_MODE_ROW: dict[str, object] = {
    "failure_mode": "CDC 路径无同步器",
    "effect": "亚稳态传播到下游寄存器",
    "severity": "8",
    "detection_method": "CDC 静态检查 + 门级仿真",
    "rpn": 120,
}
COVERAGE_ROW: dict[str, object] = {
    "feature": "DMA",
    "sub_feature": "descriptor fetch",
    "coverage_item": "cross: outstanding x burst_len",
    "test": "dma_random_test",
    "status": "covered",
}
FAILURE_MODE_FRAGMENT = (
    "<table><tr><th>失效模式</th><th>影响</th><th>严重度</th><th>检测方法</th><th>RPN</th></tr>"
    "<tr><td>CDC 路径无同步器</td><td>亚稳态传播到下游寄存器</td><td>8</td>"
    "<td>CDC 静态检查 + 门级仿真</td><td>120</td></tr></table>"
)
COVERAGE_FRAGMENT = (
    "<table><tr><th>feature</th><th>sub_feature</th><th>coverage_item</th><th>test</th><th>status</th></tr>"
    "<tr><td>DMA</td><td>descriptor fetch</td><td>cross: outstanding x burst_len</td>"
    "<td>dma_random_test</td><td>covered</td></tr></table>"
)
TABLE_META: dict[str, object] = {"rows": 2, "cols": 5, "cells": 10, "max_colspan": 1}

NEW_VARIANTS = (
    ("table.failure_mode", "modes", FAILURE_MODE_ROW, FAILURE_MODE_FRAGMENT),
    ("table.coverage_matrix", "matrix", COVERAGE_ROW, COVERAGE_FRAGMENT),
)


def _content(row_key: str, row: dict[str, object], fragment: str) -> dict[str, object]:
    return {"fragment": fragment, "meta": TABLE_META, row_key: [row]}


@pytest.mark.parametrize(("atom_type", "row_key", "row", "fragment"), NEW_VARIANTS)
def test_new_variant_schema_is_well_formed(
    atom_type: str, row_key: str, row: dict[str, object], fragment: str
) -> None:
    schema = ATOM_SCHEMAS[atom_type]

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False
    assert schema["required"] == ["text", "fragment", "meta", row_key]
    assert set(schema["properties"]) == {"text", "fragment", "meta", row_key}
    assert atom_type in ATOM_VARIANTS
    assert atom_type in TABLE_ATOMS  # E1-a：fragment 为原样 HTML 片段
    assert schema["properties"]["text"]["minLength"] == 1

    rows = schema["properties"][row_key]
    assert rows["type"] == "array" and rows["minItems"] == 1
    assert rows["items"]["additionalProperties"] is False
    assert set(rows["items"]["properties"]) == set(row)
    assert rows["items"]["type"] == "object"
    jsonschema.Draft202012Validator.check_schema(schema)


def test_failure_mode_rows_carry_the_fmea_fields() -> None:
    """idea.md §4.5 FMEA 行：失效模式/影响/严重度/检测方法/RPN（+ 可选 mitigation）。"""
    items = ATOM_SCHEMAS["table.failure_mode"]["properties"]["modes"]["items"]

    assert items["required"] == ["failure_mode", "effect", "severity", "detection_method", "rpn"]
    assert "mitigation" not in items["required"]
    assert items["properties"]["rpn"]["type"] == "integer"
    assert items["properties"]["mitigation"]["type"] == "string"


def test_coverage_matrix_rows_carry_the_ucis_vplan_chain() -> None:
    """idea.md §4.3 / 映射文档 §4：feature → sub-feature → coverage item → test → status。"""
    items = ATOM_SCHEMAS["table.coverage_matrix"]["properties"]["matrix"]["items"]

    assert items["required"] == ["feature", "sub_feature", "coverage_item", "test", "status"]


@pytest.mark.parametrize(("atom_type", "row_key", "row", "fragment"), NEW_VARIANTS)
def test_new_variant_content_validates_and_rejects_bad_content(
    atom_type: str, row_key: str, row: dict[str, object], fragment: str
) -> None:
    validator = jsonschema.Draft202012Validator(ATOM_SCHEMAS[atom_type])
    content = _content(row_key, row, fragment)

    assert list(validator.iter_errors(content)) == []

    def _violations(payload: dict[str, object]) -> set[str]:
        return {error.validator for error in validator.iter_errors(payload)}

    assert "additionalProperties" in _violations({**content, "typo": 1})
    assert "additionalProperties" in _violations({**content, row_key: [{**row, "typo": 1}]})
    assert "required" in _violations({key: value for key, value in content.items() if key != row_key})
    assert "required" in _violations({**content, row_key: [{key: value for key, value in row.items() if key != "rpn"}] }
                                      if row_key == "modes" else {**content, row_key: [{key: value for key, value in row.items() if key != "status"}]})
    assert "minItems" in _violations({**content, row_key: []})


@pytest.mark.parametrize(("atom_type", "row_key", "row", "fragment"), NEW_VARIANTS)
def test_derive_text_of_new_variants_comes_from_the_fragment(
    atom_type: str, row_key: str, row: dict[str, object], fragment: str
) -> None:
    """E1-a：表格类变体的 `content.text` 由原样 `fragment` 去标签派生（唯一生成口径）。"""
    derived = derive_text(atom_type, _content(row_key, row, fragment))

    assert derived == html_to_text(fragment)
    assert derived and derived != fragment
    with pytest.raises(ValueError):
        derive_text(atom_type, {row_key: [row]})  # 无 fragment → 派生为空即写入错误


@pytest.mark.parametrize(("atom_type", "row_key", "row", "fragment"), NEW_VARIANTS)
def test_new_variants_must_be_synthesized_as_real_tables(
    atom_type: str, row_key: str, row: dict[str, object], fragment: str
) -> None:
    """M09A `M01.table.format` 前提：`fragment` 含 `<table>` → 合成样例的 `format` 必须是 html。"""
    validator = jsonschema.Draft202012Validator(ATOM_SCHEMAS[atom_type])

    assert list(validator.iter_errors(_content(row_key, row, fragment))) == []
    assert "<table" in str(fragment).lower()
