"""M09A 单测：规则集自证 + 逐规则缺陷注入（REQ-M09-F01 / REQ-M06-F02）。

不碰数据库：M09A 是纯函数层（jsonschema + M01 模型 + M01 `derive_text`）。

`rule_id` 覆盖测（`test_rule_catalog_is_exhaustive`）保证「登记了但永不触发」的死规则不会
存在；`fix_hint` 断言保证 M06 lint 自修复闭环（REQ-M06-F02）的输入可用。三个 id
（`M09A.atom.schema` / `A10.content.text` / `M01.doc_type.atom`）与 M03 `check_proposals`
逐字相同——同一判据全局只有一个 id（P5）。
"""

from __future__ import annotations

import re
from collections.abc import Callable

import pytest

from agenticspec.model import (
    ATOM_SCHEMAS,
    DOC_TYPE_RULES,
    DOC_TYPES,
    NodeIn,
    Violation,
    derive_text,
    new_uuid7,
)
from agenticspec.model.doc_types import DocTypeRule
from agenticspec.m09 import (
    RULES_9A,
    RULE_ANCHOR_DOC_ID,
    RULE_ATOM_SCHEMA,
    RULE_ATOM_UNKNOWN,
    RULE_CONTENT_TEXT,
    RULE_CONTENT_TEXT_DRIFT,
    RULE_CONTENT_TEXT_EMPTY,
    RULE_CROSS_REF_EXTERNAL_NODE,
    RULE_DOC_TYPE_ATOM,
    RULE_DOC_TYPE_VARIANT,
    RULE_PARENT_SELF,
    RULE_TABLE_FORMAT,
    validate_proposal,
    validate_write,
)
from agenticspec.store.schema import docs

DOC_ID = "SPEC-STD-AMBA-APB"
ANCHOR = f"{DOC_ID}#1·overview"
SHA = "a" * 64
META = {"rows": 1, "cols": 1, "cells": 1, "max_colspan": 1}
TABLE_HTML = "<table><tr><td>a</td></tr></table>"
TABLE_MD = "| a | b |\n| --- | --- |\n| 1 | 2 |"

#: 每个原子的**合法** content。`text` 显式给出或由 M01 `derive_text` 生成（`figure` 系列与
#: `cross_ref` 无 `fragment`，必须显式给 `text`——M01 派生口径不允许二者皆空）。
VALID: dict[str, dict] = {
    "clause": {"fragment": "## 1 Overview\n\nBody text."},
    "definition": {"term": "Anchor", "fragment": "Anchor: a stable node address."},
    "table": {"fragment": TABLE_HTML, "meta": META},
    "table.register_field": {
        "fragment": TABLE_HTML,
        "meta": META,
        "register": "CTRL",
        "fields": [{"field": "EN", "access": "rw"}],
    },
    # 以下两个变体为方案 C 新增（`doc_type_mapping.md` §3/§4）。**合成样例，非真实语料**：
    # `safety`（FMEA/FTA）与 vPlan/UCIS 覆盖矩阵当前无语料（§5 验证边界），只能单元验证。
    "table.failure_mode": {
        "fragment": TABLE_HTML,
        "meta": META,
        "modes": [
            {
                "failure_mode": "时钟丢失",
                "effect": "状态机停摆",
                "severity": "8",
                "detection_method": "DFT 扫描",
                "rpn": 24,
            }
        ],
    },
    "table.coverage_matrix": {
        "fragment": TABLE_HTML,
        "meta": META,
        "matrix": [
            {
                "feature": "APB",
                "sub_feature": "wrap",
                "coverage_item": "cg_wrap",
                "test": "apb_wrap_test",
                "status": "covered",
            }
        ],
    },
    "figure": {"asset_ref": SHA, "caption": "APB timing", "text": "Figure: APB timing"},
    "figure.state_machine": {
        "states": ["IDLE", "RUN"],
        "transitions": [{"from": "IDLE", "to": "RUN"}],
        "text": "States: IDLE, RUN",
    },
    "code": {"language": "sv", "fragment": "always_ff @(posedge clk) begin end"},
    "example": {"fragment": "Example 1: read then write."},
    "note": {"fragment": "- first\n- second"},
    "cross_ref": {
        "ref_kind": "see_also",
        "target_doc_id": DOC_ID,
        "target_anchor": ANCHOR,
        "text": "See Section 1 Overview.",
    },
}


def content(atom_type: str, **overrides: object) -> dict:
    """构造合法 content（缺 `text` 时按 M01 口径派生），并按 `overrides` 注入缺陷。"""
    payload = {**VALID[atom_type], **overrides}
    if "text" not in payload:
        payload["text"] = derive_text(atom_type, payload)
    return payload


def node(atom_type: str = "clause", **overrides: object) -> NodeIn:
    """构造 `NodeIn`（默认合法；overrides 覆盖原子/锚/父节点/内容等字段）。"""
    fields: dict = {
        "node_id": None,
        "doc_id": DOC_ID,
        "atom_type": atom_type,
        "format": "md",
        "ordinal": 1,
        "parent_node_id": None,
        "level": 1,
        "anchor": ANCHOR,
        "content": content(atom_type),
    }
    fields.update(overrides)
    return NodeIn(**fields)


# ── 规则集自证 ────────────────────────────────────────────────────────────


def test_rule_ids_are_unique_and_namespaced() -> None:
    """`RULES_9A` 无重复、非空，且 id 属于 M09A/M01/A10 三个判据域。"""
    assert len(set(RULES_9A)) == len(RULES_9A) >= 9
    assert all(RULES_9A)
    assert all(
        item.startswith(("M09A.", "M01.", "A10.")) for item in RULES_9A
    ), f"规则 id 命名空间非法：{RULES_9A}"


def test_every_registered_atom_accepts_its_valid_sample() -> None:
    """八类 + 2 变体的合法样本零违规（防规则过严导致误报）。"""
    assert set(VALID) == set(ATOM_SCHEMAS)
    for atom_type in ATOM_SCHEMAS:
        assert validate_proposal(atom_type, content(atom_type)) == [], atom_type


def test_valid_node_passes_write_validation() -> None:
    assert validate_write(node(), doc_type="standard") == []


# ── 逐规则缺陷注入（含 fix_hint 判据）────────────────────────────────────


def _unknown_atom() -> list[Violation]:
    return validate_proposal("heading", {"text": "x"})


def _extra_property() -> list[Violation]:
    return validate_proposal("clause", content("clause", bogus=1))


def _missing_text() -> list[Violation]:
    return validate_proposal("clause", {"fragment": "## 1 Overview"})


def _text_drift() -> list[Violation]:
    return validate_proposal("table", content("table", text="WRONG"))


def _text_derived_empty() -> list[Violation]:
    return validate_proposal("table", {"fragment": "<table></table>", "text": "占位", "meta": META})


def _anchor_without_doc_id() -> list[Violation]:
    return validate_write(node(anchor="SPEC-OTHER#1·x"))


def _self_parent() -> list[Violation]:
    same = new_uuid7()
    return validate_write(node(node_id=same, parent_node_id=same))


def _table_format_mismatch() -> list[Violation]:
    return validate_write(node("table", format="md", content=content("table")))


def _external_ref_with_node() -> list[Violation]:
    return validate_write(
        node(
            "cross_ref",
            content=content(
                "cross_ref",
                target_doc_id="EXT:https://example.com/spec",
                target_node_id=str(new_uuid7()),
            ),
        )
    )


def _doc_type_variant() -> list[Violation]:
    """`standard` 拒绝 `safety` 专属变体（基底 `table` 放行 → 成因在变体白名单）。"""
    return validate_write(node("table.failure_mode", format="html"), doc_type="standard")


DEFECTS: dict[str, Callable[[], list[Violation]]] = {
    RULE_ATOM_UNKNOWN: _unknown_atom,
    RULE_ATOM_SCHEMA: _extra_property,
    RULE_CONTENT_TEXT: _missing_text,
    RULE_CONTENT_TEXT_DRIFT: _text_drift,
    RULE_CONTENT_TEXT_EMPTY: _text_derived_empty,
    RULE_ANCHOR_DOC_ID: _anchor_without_doc_id,
    RULE_PARENT_SELF: _self_parent,
    RULE_TABLE_FORMAT: _table_format_mismatch,
    RULE_CROSS_REF_EXTERNAL_NODE: _external_ref_with_node,
    RULE_DOC_TYPE_VARIANT: _doc_type_variant,
}


@pytest.mark.parametrize("rule_id", sorted(DEFECTS))
def test_rule_detects_injected_defect(rule_id: str) -> None:
    """每条规则都有人为制造的缺陷样本，且违规带定位与修复建议（REQ-M06-F02）。"""
    violations = DEFECTS[rule_id]()
    hits = [item for item in violations if item.rule_id == rule_id]
    assert hits, f"{rule_id} 未命中，实际：{[item.rule_id for item in violations]}"
    assert all(isinstance(item, Violation) for item in violations)
    assert all(item.path for item in violations)
    assert all(item.message for item in violations)
    assert all(item.fix_hint for item in violations), "违规必须带修复建议（REQ-M06-F02）"


def test_rule_catalog_is_exhaustive() -> None:
    """无死规则：`RULES_9A` = 缺陷样本可命中的 id 全集（`M01.doc_type.atom` 见后文差异化测）。"""
    assert set(DEFECTS) | {RULE_DOC_TYPE_ATOM} == set(RULES_9A)


def test_doc_type_rule_rejects_disallowed_atom_and_restores() -> None:
    """`M01.doc_type.atom`：组合规则（Q6 可扩展）判定，id 与 M03 共用。"""
    original = DOC_TYPE_RULES["product"]
    try:
        DOC_TYPE_RULES["product"] = DocTypeRule(
            doc_type="product", allowed_atom_types=("clause",), required_atom_types=("clause",)
        )
        hits = [
            item
            for item in validate_write(node("table"), doc_type="product")
            if item.rule_id == RULE_DOC_TYPE_ATOM
        ]
        assert hits and hits[0].fix_hint
        assert validate_write(node("clause"), doc_type="product") == []
    finally:
        DOC_TYPE_RULES["product"] = original


# ── 其它不变量 ───────────────────────────────────────────────────────────


def test_unknown_atom_message_lists_registered_types() -> None:
    violation = validate_proposal("nope", {"text": "x"})[0]
    assert violation.rule_id == RULE_ATOM_UNKNOWN
    assert violation.path == "atomType"
    for atom_type in ("clause", "table.register_field"):
        assert atom_type in violation.message


def test_non_mapping_content_is_reported_once() -> None:
    violations = validate_proposal("clause", ["not", "an", "object"])  # type: ignore[arg-type]
    assert [item.rule_id for item in violations] == [RULE_ATOM_SCHEMA]
    assert violations[0].path == "content"
    assert violations[0].fix_hint


def test_blank_text_is_owned_by_a10_rule_only() -> None:
    """空白 `text`：`A10.content.text` 拥有该判据，schema 的 required 文案被剔除（不重复报）。"""
    violations = validate_proposal("clause", content("clause", text="   "))
    assert [item.rule_id for item in violations] == [RULE_CONTENT_TEXT]


def test_missing_text_reported_alongside_other_schema_errors() -> None:
    """`text` 缺失与非法字段是不同修复动作 → 并列报告（各自带 fix_hint）。"""
    violations = validate_proposal("clause", {"fragment": "x", "bogus": 1})
    assert {item.rule_id for item in violations} == {RULE_ATOM_SCHEMA, RULE_CONTENT_TEXT}
    assert all(item.fix_hint for item in violations)


def test_schema_error_suppresses_derived_text_rules() -> None:
    """形态未通过 schema 时不叠加派生类判据（同一根因只报需要修的那一刻）。"""
    violations = validate_proposal("table", {"fragment": TABLE_HTML, "text": "WRONG"})
    assert {item.rule_id for item in violations} == {RULE_ATOM_SCHEMA}


def test_table_format_accepts_both_p4_forms() -> None:
    """E1-a 两式：html 片段 ↔ `format='html'`；md 管道表 ↔ `format='md'`。"""
    assert validate_write(node("table", format="html", content=content("table"))) == []
    assert (
        validate_write(
            node("table", format="md", content=content("table", fragment=TABLE_MD))
        )
        == []
    )


def test_cross_ref_external_without_node_is_clean() -> None:
    payload = content("cross_ref", target_doc_id="EXT:https://example.com/spec")
    assert validate_write(node("cross_ref", content=payload)) == []


def test_variant_atom_schema_is_loaded_from_m01() -> None:
    """变体与基底共用 M01 schema 表；缺 `fields` 时**逐字段**报出（路径与建议都指到该字段）。"""
    payload = content("table.register_field")
    payload.pop("fields")
    violations = validate_proposal("table.register_field", payload)
    assert {item.rule_id for item in violations} == {RULE_ATOM_SCHEMA}
    hit = next(item for item in violations if item.path == "content.fields")
    assert "content.fields" in hit.fix_hint
    assert all(item.fix_hint for item in violations)


# ── `fix_hint` 粒度（REQ-M06-F02：agent 依建议自修复重试）──────────────────

_HINT_CASES: list[tuple[str, str, dict, str, str]] = [
    # (标签, atom_type, content, 期望 path, 期望 hint 片段)
    ("required-单字段", "table", {"fragment": TABLE_HTML, "text": "a"}, "content.meta", "`content.meta`"),
    (
        "required-多字段",
        "table.register_field",
        {"text": "x"},
        "content.fields",
        "`content.fields`",
    ),
    (
        "type",
        "table",
        {"fragment": 123, "text": "a", "meta": META},
        "content.fragment",
        "类型应为 string，实际 int",
    ),
    (
        "enum",
        "cross_ref",
        {"text": "See x", "ref_kind": "nope", "target_doc_id": DOC_ID},
        "content.ref_kind",
        "取值应为 `traces_to`、`see_also`、`composes_from`、`source_ref` 之一",
    ),
    (
        "additionalProperties-单字段",
        "clause",
        {"text": "x", "bogus": 1},
        "content.bogus",
        "移除未声明字段：`content.bogus`",
    ),
]


@pytest.mark.parametrize(
    ("label", "atom_type", "payload", "expected_path", "hint_fragment"),
    _HINT_CASES,
    ids=[case[0] for case in _HINT_CASES],
)
def test_schema_hint_is_field_level(
    label: str,
    atom_type: str,
    payload: dict,
    expected_path: str,
    hint_fragment: str,
) -> None:
    """四类 validator 的 `fix_hint` 必须指到**具体字段/取值**（而非规则级文案）。"""
    violations = validate_proposal(atom_type, payload)
    hits = [item for item in violations if item.path == expected_path]
    assert hits, f"{label}: 未报出 {expected_path}，实际 {[item.path for item in violations]}"
    assert hint_fragment in hits[0].fix_hint
    assert hits[0].message


def test_required_hint_is_deduplicated_per_field() -> None:
    """jsonschema 对多个缺失字段会重复整份 `required` 清单 → 本实现按字段展开且不重复。"""
    violations = validate_proposal("table.register_field", {"text": "x"})
    paths = [item.path for item in violations]
    assert paths == ["content.fields", "content.fragment", "content.meta", "content.register"]
    assert len(paths) == len(set(paths))


def test_unregistered_validator_falls_back_to_rule_level_hint() -> None:
    """未细分文案的校验器（`pattern`）回落规则级文案，但路径仍精确到字段。"""
    violations = validate_proposal("figure", {"text": "f", "asset_ref": "NOT-HEX"})
    assert [item.path for item in violations] == ["content.asset_ref"]
    assert "ATOM_SCHEMAS['figure']" in violations[0].fix_hint


def test_anchor_rule_uses_doc_id_prefix() -> None:
    """锚判据是 `<doc_id>#` 前缀（M01 锚构造口径），不是「非空」。"""
    hits = [
        item
        for item in validate_write(node(anchor="SPEC-OTHER#1"))
        if item.rule_id == RULE_ANCHOR_DOC_ID
    ]
    assert hits and DOC_ID in hits[0].message
    assert validate_write(node(anchor=f"{DOC_ID}#2·x")) == []


def test_validation_is_deterministic() -> None:
    """同输入两次调用逐字段一致（M06 重试闭环与 lint 快照依赖）。"""
    target = content("table", text="WRONG")
    first = validate_proposal("table", target)
    second = validate_proposal("table", target)
    assert [item.model_dump() for item in first] == [item.model_dump() for item in second]


# ── doc_type 差异化（方案 C：同一原子在不同 doc_type 下判定不同）─────────────


def test_same_atom_differs_across_doc_types() -> None:
    """**差异化真实生效**：`figure` 在 `standard` 放行、在 `lang` 拒绝（基底原子判据）。

    `lang`（语言/脚本手册，§4.1 DocBook RefEntry 语义）无图；`standard` 八类全收。
    这是 idea.md §4「不同文档类型设立不同 schema」的最小可观测后果——修复前五类规则
    逐字段相同，本断言在那种状态下必然失败（`lang` 会放行 `figure`）。
    """
    assert validate_write(node("figure"), doc_type="standard") == []
    hits = [
        item
        for item in validate_write(node("figure"), doc_type="lang")
        if item.rule_id == RULE_DOC_TYPE_ATOM
    ]
    assert hits and hits[0].path == "atomType" and hits[0].fix_hint


def test_variant_whitelist_is_per_doc_type() -> None:
    """变体白名单逐 `doc_type`：`table.failure_mode` 在 `safety` 通过、在 `standard` 拒。

    **合成样例，非真实语料**（`safety` 无语料，`doc_type_mapping.md` §5）——本断言证明的是
    **规则生效**，不是端到端导入能力。
    """
    node_failure_mode = node("table.failure_mode", format="html")
    assert validate_write(node_failure_mode, doc_type="safety") == []
    hits = [
        item
        for item in validate_write(node_failure_mode, doc_type="standard")
        if item.rule_id == RULE_DOC_TYPE_VARIANT
    ]
    assert hits and "table.failure_mode" in hits[0].message
    assert hits[0].path == "atomType" and hits[0].fix_hint


def test_variant_whitelist_rejects_standard_variant_in_safety() -> None:
    """反向：`table.register_field` 在 `standard`/`product` 放行、在 `safety` 拒（白名单互不通用）。"""
    register_field = node("table.register_field", format="html")
    for doc_type in ("standard", "product"):
        assert validate_write(register_field, doc_type=doc_type) == [], doc_type
    hits = [
        item
        for item in validate_write(register_field, doc_type="safety")
        if item.rule_id == RULE_DOC_TYPE_VARIANT
    ]
    # 建议里必须列出该类**允许的**变体（`safety` → `table.failure_mode`）：agent 依此改写重试
    assert hits and "table.failure_mode" in hits[0].message
    assert "table.failure_mode" in hits[0].fix_hint


def test_base_atom_exclusion_outranks_variant_rule() -> None:
    """成因归类：基底原子被排除时**恒**报 `M01.doc_type.atom`（不因名字含点而报变体规则）。"""
    ids = {item.rule_id for item in validate_write(node("figure.state_machine"), doc_type="lang")}
    assert ids == {RULE_DOC_TYPE_ATOM}


def test_ucis_coverage_matrix_is_product_only() -> None:
    """`table.coverage_matrix`（UCIS/vPlan，§4）仅 `product` 放行。**合成样例，非真实语料**。"""
    matrix = node("table.coverage_matrix", format="html")
    assert validate_write(matrix, doc_type="product") == []
    hits = [
        item
        for item in validate_write(matrix, doc_type="standard")
        if item.rule_id == RULE_DOC_TYPE_VARIANT
    ]
    assert hits and hits[0].fix_hint


# ── DDL 取值域一致性（模型层 ↔ §4 DDL）────────────────────────────────────


def test_doc_type_domain_matches_ddl_check() -> None:
    """`M01.DOC_TYPES` 与 §4 DDL `docs_doc_type_check` 取值域逐项一致（防漂移）。

    同一取值域的两处载体：模型层决定组合规则判据（M09A `M01.doc_type.*`），DDL 决定
    `docs.doc_type` 可写值。只改一侧即坏——放宽 DDL 会写出无规则的 `doc_type`
    （`get_doc_type_rule` 抛 `KeyError`），只加模型值则写入被 DB 拒。
    方案 C 的结论是**保持 5 值**，故 DDL 无需变更；本断言把该结论钉死（含顺序：`DOC_TYPES`
    是判据域口径，DDL 列表须与之一致）。
    """
    constraint = next(item for item in docs.constraints if item.name == "docs_doc_type_check")
    assert tuple(re.findall(r"'([^']*)'", str(constraint.sqltext))) == DOC_TYPES
