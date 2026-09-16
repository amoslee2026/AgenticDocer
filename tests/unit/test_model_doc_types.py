"""M01 doc_type 组合规则测试（REQ-M01-F03，Q6）。"""

from __future__ import annotations

import pytest

import agenticdocer.model.doc_types as doc_types
from agenticdocer.model import (
    ATOM_TYPES,
    C5_META_FIELDS,
    DOC_TYPE_RULES,
    DOC_TYPES,
    DocTypeRule,
    allowed_atom_types,
    get_doc_type_rule,
    is_atom_allowed,
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
        assert set(rule.required_atom_types) <= set(rule.allowed_atom_types)


def test_standard_rule_is_the_pilot_baseline():
    rule = get_doc_type_rule("standard")

    assert rule.allowed_atom_types == ATOM_TYPES
    assert rule.required_atom_types == ("clause",)
    assert rule.required_meta_fields == C5_META_FIELDS
    assert len(C5_META_FIELDS) == 17


def test_non_standard_rules_defer_c5_requirement_to_q6():
    for doc_type in ("lang", "tool-manual", "product", "safety"):
        rule = get_doc_type_rule(doc_type)
        assert rule.allowed_atom_types == ATOM_TYPES
        assert rule.required_meta_fields == ()
        assert missing_required_meta(doc_type, {}) == []


def test_allowed_atom_types_and_variant_handling():
    assert allowed_atom_types("standard") == ATOM_TYPES
    assert is_atom_allowed("standard", "clause")
    assert is_atom_allowed("standard", "table.register_field")  # 变体随基底原子放行
    assert not is_atom_allowed("standard", "clause.typo")
    assert not is_atom_allowed("standard", "not-an-atom")


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
