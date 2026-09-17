"""M01 领域模型层（L1）：公共类型、UUIDv7、原子 Schema、锚规则、doc_type 组合规则。

本层**无依赖且与 LLM 无关**（§1.3 L1；P6）。上层统一从这里取模型：

    from agenticspec.model import NodeIn, Event, new_uuid7
"""

from .anchors import (
    DIGEST_LEN,
    EMPTY_SLUG,
    SLUG_MAX_CHARS,
    SectionRef,
    anchor_base,
    assign_anchors,
    body_digest,
    make_anchor,
    normalize_body,
    section_path_str,
    slugify,
)
from .atoms import (
    ATOM_SCHEMAS,
    ATOM_TYPES,
    ATOM_VARIANTS,
    TABLE_ATOMS,
    UnknownAtomTypeError,
    derive_text,
    get_atom_schema,
    html_to_text,
)
from .doc_types import (
    C5_META_FIELDS,
    DOC_TYPE_RULES,
    DOC_TYPES,
    LANG_ATOM_TYPES,
    LANG_META_FIELDS,
    DocTypeRule,
    allowed_atom_types,
    allowed_atom_variants,
    get_doc_type_rule,
    is_atom_allowed,
    is_variant_allowed,
    missing_required_meta,
    register_doc_type_rule,
)
from .types import *  # noqa: F403 —— 公共类型直出，清单见 types.__all__
from .types import __all__ as _TYPES_ALL
from .uuid7 import new_uuid7, uuid7_timestamp_ms

__all__ = [
    *_TYPES_ALL,
    # uuid7
    "new_uuid7",
    "uuid7_timestamp_ms",
    # anchors（ADR-006 + A1）
    "DIGEST_LEN",
    "EMPTY_SLUG",
    "SLUG_MAX_CHARS",
    "SectionRef",
    "anchor_base",
    "assign_anchors",
    "body_digest",
    "make_anchor",
    "normalize_body",
    "section_path_str",
    "slugify",
    # atoms（八类 + 4 变体，A10）
    "ATOM_SCHEMAS",
    "ATOM_TYPES",
    "ATOM_VARIANTS",
    "TABLE_ATOMS",
    "UnknownAtomTypeError",
    "derive_text",
    "get_atom_schema",
    "html_to_text",
    # doc_type 组合规则（REQ-M01-F03）
    "C5_META_FIELDS",
    "LANG_ATOM_TYPES",
    "LANG_META_FIELDS",
    "DOC_TYPE_RULES",
    "DOC_TYPES",
    "DocTypeRule",
    "allowed_atom_types",
    "allowed_atom_variants",
    "get_doc_type_rule",
    "is_atom_allowed",
    "is_variant_allowed",
    "missing_required_meta",
    "register_doc_type_rule",
]
