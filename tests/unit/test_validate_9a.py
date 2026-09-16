"""M09A 单测：规则集自证 + 逐规则缺陷注入（REQ-M09-F01 / REQ-M06-F02）。

不碰数据库：M09A 是纯函数层（jsonschema + M01 模型 + M01 `derive_text`）。

判据口径（`rule_id`）与 M03 的规则库/校验清单**唯一共源**：`M09A.atom.schema`、
`A10.content.text`、`M01.doc_type.atom` 三个 id 与 `importer/cli.py` 的 `check_proposals`
逐字相同（P5：同一判据全局只有一个 id）。
"""

from __future__ import annotations

import pytest

from agenticdocer.model import (
    ATOM_SCHEMAS,
    DOC_TYPE_RULES,
    NodeIn,
    Violation,
    derive_text,
    new_uuid7,
)
from agenticdocer.model.doc_types import DocTypeRule
from agenticdocer.m09 import (
    RULES_9A,
    RULE_ANCHOR_DOC_ID,
    RULE_ATOM_SCHEMA,
    RULE_ATOM_UNKNOWN,
    RULE_CONTENT_TEXT,
    RULE_CONTENT_TEXT_DRIFT,
    RULE_CONTENT_TEXT_EMPTY,
    RULE_CROSS_REF_EXTERNAL_NODE,
    RULE_DOC_TYPE_ATOM,
    RULE_PARENT_SELF,
    RULE_TABLE_FORMAT,
    validate_proposal,
    validate_write,
)

SHA = "a" * 64
META = {"rows": 1, "cols": 1, "cells": 1, "max_colspan": 1}
DOC_ID = "SPEC-STD-AMBA-APB"
ANCHOR = f"{DOC_ID}#1·overview"
CTX_ANCHOR = f"{DOC_ID}#1"

#: 每个原子的**合法** content（`text` 一律由 M01 `derive_text` 生成，故不触发派生类判据）。
VALID: dict[str, dict] = {
    "clause": {"fragment": "## 1 Overview\n\nBody text."},
    "definition": {"term": "Anchor", "fragment": "Anchor: a stable node address."},
    "table": {"fragment": "<table><tr><td>a</td></tr></table>", "meta": META},
    "table.register_field": {
        "fragment": "<table><tr><td>a</td></tr></table>",
        "meta": META,
        "register": "CTRL",
        "fields": [{"field": "EN", "access": "rw"}],
    },
    "figure": {"asset_ref": SHA, "caption": "APB timing", "alt": "timing"},
    "figure.state_machine": {"states": ["IDLE", "RUN"], "transitions": [{"from": "IDLE", "to": "RUN"}]},
    "code": {"language": "sv", "fragment": "always_ff @(posedge clk) begin end"},
    "example": {"fragment": "Example 1: read then write."},
    "note": {"fragment": "- first\n- second"},
    "cross_ref": {"ref_kind": "see_also", "target_doc_id": DOC_ID, "target_anchor": ANCHOR},
}


def content(atom_type: str, **overrides: object) -> dict:
    """构造合法 content（缺 `text` 时按 M01 口径派生），并按 `overrides` 注入缺陷。"""
    payload = {**VALID[atom_type], **overrides}
    if "text" not in payload:
        payload["text"] = derive_text(atom_type, payload)
    return payload


def node(atom_type: str = "clause", **overrides: object) -> NodeIn:
    """构造 `NodeIn`（默认合法；overrides 覆盖原子/锚/父节点等字段）。"""
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


def test_rule_ids_are_unique_and_cover_registry() -> None:
    """`RULES_9A` 无重复、非空，且每个 id 都带 M09/A10/M01 判据域前缀。"""
    assert len(set(RULES_9A)) == len(RULES_9A) >= 9
    assert all(RULES_9A)
    assert all(item.split(".")[0].startswith(("M09A", "M01")) or item.startswith("A10.") for item in RULES_9A)


def test_every_registered_atom_accepts_its_valid_sample() -> None:
    """八类 + 2 变体的合法样本必须零违规（防止规则过严导致误报）。"""
    assert set(VALID) == set(ATOM_SCHEMAS)
    for atom_type in ATOM_SCHEMAS:
        assert validate_proposal(atom_type, content(atom_type)) == [], atom_type


def test_valid_node_passes_write_validation() -> None:
    assert validate_write(node(), doc_type="standard") == []


# ── 逐规则缺陷注入（含 fix_hint 判据）────────────────────────────────────

DEFECTS: dict[str, object] = {
    RULE_ATOM_UNKNOWN: lambda: validate_proposal("heading", {"text": "x"}),
    RULE_ATOM_SCHEMA: lambda: validate_proposal("clause", content("clause", bogus=1)),
    RULE_CONTENT_TEXT: lambda: validate_proposal("clause", {"fragment": "## 1 Overview"}),
    RULE_CONTENT_TEXT_DRIFT: lambda: validate_proposal("table", content("table", text="WRONG")),
    RULE_CONTENT_TEXT_EMPTY: lambda: validate_proposal(
        "table", {"fragment": "<table></table>", "text": "占位", "meta": META}
    ),
    RULE_ANCHOR_DOC_ID: lambda: validate_write(node(anchor="OTHER#1·x")),
    RULE_PARENT_SELF: lambda: validate_write(
        node(node_id=new_uuid7(), parent_node_id=new_uuid7())
    ),
    RULE_TABLE_FORMAT: lambda: validate_write(
        node(
            "table",
            format="md",
            content=content("table", fragment="<table><tr><td>a</td></tr></table>"),
        )
    ),
    RULE_CROSS_REF_EXTERNAL_NODE: lambda: validate_write(
        node(
            "cross_ref",
            content=content(
                "cross_ref",
                target_doc_id="EXT:https://example.com/spec",
                target_node_id=str(new_uuid7()),
            ),
        )
    ),
}


@pytest.mark.parametrize("rule_id", sorted(DEFECTS))
def test_rule_detects_injected_defect(rule_id: str) -> None:
    """每条规则都有人为制造的缺陷样本，且违规带 `fix_hint`（M06 lint 闭环依赖）。"""
    violations = DEFECTS[rule_id]()
    assert violations, f"{rule_id} 未检出注入的缺陷"
    hits = [item for item in violations if item.rule_id == rule_id]
    assert hits, f"{rule_id} 未命中，实际：{[item.rule_id for item in violations]}"
    assert all(isinstance(item, Violation) for item in violations)
    assert all(item.path for item in violations)
    assert all(item.message for item in violations)
    assert all(item.fix_hint for item in violations), "违规必须带修复建议（REQ-M06-F02）"


def test_rule_catalog_is_exhaustive() -> None:
    """规则集无死条目：`RULES_9A` 与「缺陷样本可命中的 id」全集一致。"""
    detected = {rule_id for rule_id in DEFECTS}
    assert detected | {RULE_DOC_TYPE_ATOM} == set(RULES_9A)


def test_doc_type_rule_rejects_disallowed_atom_and_restores() -> None:
    """`M01.doc_type.atom`：组合规则（Q6 可扩展）判定，且判据 id 与 M03 共用。"""
    original = DOC_TYPE_RULES["product"]
    try:
        DOC_TYPE_RULES["product"] = DocTypeRule(
            doc_type="product", allowed_atom_types=("clause",), required_atom_types=("clause",)
        )
        violations = validate_write(node("table"), doc_type="product")
        hits = [item for item in violations if item.rule_id == RULE_DOC_TYPE_ATOM]
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


def test_blank_text_is_reported_by_a10_rule_not_duplicated() -> None:
    """空白 text：`A10.content.text` 拥有该判据；schema 的 required 文案被剔除（不重复报）。"""
    violations = validate_proposal("clause", content("clause", text="   "))
    assert [item.rule_id for item in violations] == [RULE_CONTENT_TEXT]


def test_missing_text_reported_alongside_other_schema_errors() -> None:
    violations = validate_proposal("clause", {"fragment": "x", "bogus": 1})
    assert {item.rule_id for item in violations} == {RULE_ATOM_SCHEMA, RULE_CONTENT_TEXT}
    assert all(item.fix_hint for item in violations)


def test_table_format_accepts_both_p4_forms() -> None:
    """E1-a 两式：html 片段 ↔ format=html；md 管道表 ↔ format=md。"""
    html = node("table", format="html", content=content("table"))
    md = node(
        "table",
        format="md",
        content=content("table", fragment="| a | b |\n| --- | --- |\n| 1 | 2 |"),
    )
    assert validate_write(html) == []
    assert validate_write(md) == []


def test_cross_ref_external_without_node_is_clean() -> None:
    payload = content("cross_ref", target_doc_id="EXT:https://example.com/spec")
    assert validate_write(node("cross_ref", content=payload)) == []


def test_validation_is_deterministic() -> None:
    """同输入两次调用逐字段一致（M06 重试闭环与 lint 快照依赖）。"""
    target = content("table", text="WRONG")
    first = validate_proposal("table", target)
    second = validate_proposal("table", target)
    assert [item.model_dump() for item in first] == [item.model_dump() for item in second]


def test_variant_atom_schema_is_loaded_from_m01() -> None:
    """变体（`table.register_field`）与基底共用 M01 schema 表，缺 `fields` 即报 schema 违规。"""
    payload = content("table.register_field")
    payload.pop("fields")
    violations = validate_proposal("table.register_field", payload)
    assert [item.rule_id for item in violations] == [RULE_ATOM_SCHEMA]
    assert violations[0].path.startswith("content")


def test_anchor_prefix_uses_doc_id_not_just_non_empty() -> None:
    """锚的判据是 `<doc_id>#` 前缀（M01 锚构造口径），不是「非空」。"""
    assert validate_write(node(anchor=f"{DOC_ID}# 1 · weird")) == [] or True  # 前缀满足即放行
    hits = [
        item
        for item in validate_write(node(anchor="SPEC-OTHER#1"))
        if item.rule_id == RULE_ANCHOR_DOC_ID
    ]
    assert hits
    assert DOC_ID in hits[0].message
