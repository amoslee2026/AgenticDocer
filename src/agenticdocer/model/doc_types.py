"""doc_type → 允许原子类型 / 必填字段 的组合规则（REQ-M01-F03，Q6）。

规则表是 M03（导入提议）与 M09A（校验）的**共同输入**（P5 口径单点），可经
:func:`register_doc_type_rule` 覆盖或扩展：Q6 约定非 `standard` 类型的组合规则随首个该类
文档引入时细化，此处给出可运行的基线（全部原子可用、必备条款、`meta` 无额外必填）。

`standard` 的 `required_meta_fields` = §6「frontmatter → docs 映射（C5 十七字段）」，
即行业标准类文档入库时 `docs.meta` 必须完整保真的字段集合。
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .atoms import ATOM_SCHEMAS, ATOM_TYPES
from .types import DocType, Model

__all__ = [
    "DOC_TYPES",
    "C5_META_FIELDS",
    "DocTypeRule",
    "DOC_TYPE_RULES",
    "register_doc_type_rule",
    "get_doc_type_rule",
    "allowed_atom_types",
    "is_atom_allowed",
    "missing_required_meta",
]

DOC_TYPES: tuple[str, ...] = ("standard", "lang", "tool-manual", "product", "safety")

C5_META_FIELDS: tuple[str, ...] = (
    "title",
    "type",
    "purpose",
    "audience",
    "direction",
    "status",
    "version",
    "section_meta",
    "spec_id",
    "spec_type",
    "spec_org",
    "spec_revision",
    "source",
    "converted_by",
    "converted_at",
    "reviewed_by",
    "reviewed_at",
)
"""§6：frontmatter → `docs.meta` 的 C5 十七字段（必填校验口径）。"""


class DocTypeRule(Model):
    """单条组合规则。``allowed_atom_types`` 用基底原子名（八类），变体随其基底放行。"""

    doc_type: DocType
    allowed_atom_types: tuple[str, ...]
    required_atom_types: tuple[str, ...] = ()
    required_meta_fields: tuple[str, ...] = ()


DOC_TYPE_RULES: dict[str, DocTypeRule] = {
    # 首批试点类型（B7/C7）：八类原子全可用，必备条款级节点（ADR-006 最小节点），
    # meta 必填 C5 十七字段（§6 映射表）。
    "standard": DocTypeRule(
        doc_type="standard",
        allowed_atom_types=ATOM_TYPES,
        required_atom_types=("clause",),
        required_meta_fields=C5_META_FIELDS,
    ),
    # 以下四类为 A22 取值域内的扩展类型，基线同 standard，C5 十七字段暂不强制（Q6 细化）。
    "lang": DocTypeRule(doc_type="lang", allowed_atom_types=ATOM_TYPES, required_atom_types=("clause",)),
    "tool-manual": DocTypeRule(
        doc_type="tool-manual", allowed_atom_types=ATOM_TYPES, required_atom_types=("clause",)
    ),
    "product": DocTypeRule(doc_type="product", allowed_atom_types=ATOM_TYPES, required_atom_types=("clause",)),
    "safety": DocTypeRule(doc_type="safety", allowed_atom_types=ATOM_TYPES, required_atom_types=("clause",)),
}
"""doc_type → 组合规则（基线；经 :func:`register_doc_type_rule` 覆盖）。"""


def register_doc_type_rule(rule: DocTypeRule) -> None:
    """注册/覆盖一条组合规则（Q6：非 standard 类型细化时由 M03/M09A 调用）。"""
    unknown = [atom for atom in rule.allowed_atom_types if atom not in ATOM_TYPES]
    if unknown:
        raise ValueError(f"{rule.doc_type} 的 allowed_atom_types 含未注册原子：{unknown}")
    DOC_TYPE_RULES[rule.doc_type] = rule


def get_doc_type_rule(doc_type: str) -> DocTypeRule:
    """取 doc_type 的组合规则；未定义 → :class:`KeyError`（docs.doc_type 受 DDL CHECK 约束）。"""
    try:
        return DOC_TYPE_RULES[doc_type]
    except KeyError:
        raise KeyError(f"未定义 doc_type 组合规则：{doc_type!r}；已定义：{sorted(DOC_TYPE_RULES)}") from None


def allowed_atom_types(doc_type: str) -> tuple[str, ...]:
    """该 doc_type 允许的基底原子类型。"""
    return get_doc_type_rule(doc_type).allowed_atom_types


def is_atom_allowed(doc_type: str, atom_type: str) -> bool:
    """已注册的变体名（``table.register_field``）按其基底原子（``table``）判定；
    未注册的类型名（拼错、臆造变体）一律不放行（REQ-M01-F01：无 schema 不得写入）。"""
    if atom_type not in ATOM_SCHEMAS:
        return False
    return atom_type.split(".", 1)[0] in get_doc_type_rule(doc_type).allowed_atom_types


def missing_required_meta(doc_type: str, meta: Mapping[str, Any] | None) -> list[str]:
    """返回 `meta` 缺失的必填字段（空列表 = 通过），供 M03/M09A 校验消费。"""
    present = meta or {}
    return [field_name for field_name in get_doc_type_rule(doc_type).required_meta_fields if field_name not in present]

