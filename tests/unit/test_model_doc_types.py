"""M01 doc_type 组合规则测试（REQ-M01-F03，Q6）。"""

from __future__ import annotations

import pytest

import pytest

import agenticdocer.model.doc_types as doc_types
from agenticdocer.model import (
    ATOM_TYPES,
    ATOM_VARIANTS,
    C5_META_FIELDS,
    DOC_TYPE_RULES,
    DOC_TYPES,
    DocTypeRule,
    allowed_atom_types,
    allowed_atom_variants,
    get_doc_type_rule,
    is_atom_allowed,
    is_variant_allowed,
    missing_required_meta,
    register_doc_type_rule,
)


def test_doc_type_domain_matches_ddl_check():
    assert DOC_TYPES == ("standard", "lang", "tool-manual", "product", "safety")
    assert set(DOC_TYPE_RULES) == set(DOC_TYPES)


def test_every_rule_is_consistent_with_registered_atoms():
    for doc_type, rule in DOC_TYPE_RULES.items():
        assert rule.doc_type == doc_type
        assert set(rule.allowed_atom_types) <= set(ATOM_TYPES)
        assert set(rule.allowed_atom_variants) <= set(ATOM_VARIANTS)
        # 变体白名单不得悬空：基底必须在 allowed_atom_types 内；required 落在允许集合内
        assert {variant.split(".", 1)[0] for variant in rule.allowed_atom_variants} <= set(
            rule.allowed_atom_types
        )
        assert set(rule.required_atom_types) <= set(rule.allowed_atom_types) | set(rule.allowed_atom_variants)


def test_standard_rule_is_the_pilot_baseline():
    rule = get_doc_type_rule("standard")

    assert rule.allowed_atom_types == ATOM_TYPES
    assert rule.required_atom_types == ("clause",)
    assert rule.required_meta_fields == C5_META_FIELDS
    assert len(C5_META_FIELDS) == 17


def test_non_standard_rules_do_not_inherit_the_c5_baseline():
    """C5 十七字段是行业标准类（NISO STS 著录）的专有必填口径；其余四类各有自己的必填元数据
    （逐条对照见 tests/unit/test_doc_type_schemas.py；此处只守「未退回 standard 复制」不变量）。"""
    for doc_type in ("lang", "tool-manual", "product", "safety"):
        rule = get_doc_type_rule(doc_type)

        assert rule.required_meta_fields != C5_META_FIELDS
        assert missing_required_meta(doc_type, {}) == list(rule.required_meta_fields)
        assert missing_required_meta(doc_type, dict.fromkeys(rule.required_meta_fields, "x")) == []


def test_allowed_atom_types_and_variant_handling():
    assert allowed_atom_types("standard") == ATOM_TYPES
    assert is_atom_allowed("standard", "clause")
    assert is_atom_allowed("standard", "table.register_field")  # 变体白名单放行
    assert not is_atom_allowed("standard", "table.failure_mode")  # safety 专属变体
    assert not is_atom_allowed("standard", "table.coverage_matrix")  # product 专属变体
    assert not is_atom_allowed("standard", "clause.typo")
    assert not is_atom_allowed("standard", "not-an-atom")


def test_variant_whitelist_is_explicit_per_doc_type():
    assert allowed_atom_variants("standard") == ("table.register_field", "figure.state_machine")
    assert allowed_atom_variants("safety") == ("table.failure_mode",)
    assert allowed_atom_variants("lang") == ()  # 显式空集：语法手册无结构化变体
    assert is_variant_allowed("safety", "table.failure_mode")
    assert not is_variant_allowed("safety", "table.register_field")
    assert not is_variant_allowed("lang", "table.register_field")
    assert not is_variant_allowed("standard", "clause")  # 非变体名恒 False


def test_missing_required_meta_reports_gaps_for_standard():
    assert missing_required_meta("standard", {}) == list(C5_META_FIELDS)
    assert missing_required_meta("standard", None) == list(C5_META_FIELDS)
    complete = {field_name: "x" for field_name in C5_META_FIELDS}
    assert missing_required_meta("standard", complete) == []
    assert missing_required_meta("standard", {**complete, "extra": "x"}) == []


def test_unknown_doc_type_is_rejected():
    with pytest.raises(KeyError):
        get_doc_type_rule("whitepaper")
    with pytest.raises(KeyError):
        allowed_atom_types("whitepaper")


def test_register_doc_type_rule_overrides_and_validates(monkeypatch):
    monkeypatch.setattr(doc_types, "DOC_TYPE_RULES", dict(DOC_TYPE_RULES))

    register_doc_type_rule(
        DocTypeRule(doc_type="product", allowed_atom_types=("clause", "table"), required_atom_types=("clause",))
    )

    assert allowed_atom_types("product") == ("clause", "table")
    assert not is_atom_allowed("product", "figure")

    with pytest.raises(ValueError):
        register_doc_type_rule(DocTypeRule(doc_type="lang", allowed_atom_types=("clause", "not-an-atom")))
    with pytest.raises(Exception):
        DocTypeRule(doc_type="whitepaper", allowed_atom_types=("clause",))
