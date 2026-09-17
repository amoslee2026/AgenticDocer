"""doc_type → 允许原子类型 / 变体白名单 / 必填字段 的组合规则（REQ-M01-F03，Q6）。

规则表是 M03（导入提议）与 M09A（校验）的**共同输入**（P5 口径单点），可经
:func:`register_doc_type_rule` 覆盖或扩展。

**差异化依据**：`spec/arch_spec/doc_type_mapping.md` §2（idea.md 30+ 文档类型 → 5 个 doc_type
的映射与收敛原则）与 §3（五类差异化规则表）；字段取自 `spec/idea/idea.md` §4.1（DocBook
`RefEntry`）、§4.3（UCIS/vPlan）、§4.5（逐类型字段）。五类的 ``allowed_atom_types`` /
``required_meta_fields`` / ``allowed_atom_variants`` 必须**实质不同**，不得退回「四条规则复制
``standard``」的空壳状态（该缺陷见映射文档 §1 缺陷 1）。

`standard` 的 `required_meta_fields` = §6「frontmatter → docs 映射（C5 十七字段）」，
即行业标准类文档入库时 `docs.meta` 必须完整保真的字段集合。

**验证边界**（映射文档 §5）：仅 `standard` 有真实语料，其余四类与 UCIS/vPlan 只有 schema
定义 + 合成样例——**不得声称端到端验证**。
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .atoms import ATOM_SCHEMAS, ATOM_TYPES, ATOM_VARIANTS
from .types import DocType, Model

__all__ = [
    "DOC_TYPES",
    "C5_META_FIELDS",
    "LANG_META_FIELDS",
    "LANG_ATOM_TYPES",
    "DocTypeRule",
    "DOC_TYPE_RULES",
    "register_doc_type_rule",
    "get_doc_type_rule",
    "allowed_atom_types",
    "allowed_atom_variants",
    "is_atom_allowed",
    "is_variant_allowed",
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

LANG_META_FIELDS: tuple[str, ...] = ("command_name", "syntax", "tool_context")
"""§4.1 DocBook `RefEntry`：命令级元数据（NAME/SYNOPSIS + 适用工具）。

`lang`（语言/脚本语法手册：Verilog/TCL/SDC/UPF）与 `tool-manual`（EDA 工具手册）共用；
`tool_context` 记「厂商 + 版本」——同一命令在不同厂商工具/版本间语义可能不同，§4.1 要求显式标注。
"""

LANG_ATOM_TYPES: tuple[str, ...] = ("clause", "definition", "table", "code", "example", "note", "cross_ref")
"""§4.1 语法手册可用的基底原子：八类去掉 `figure`（命令参考以文/码/表示例为主）。

`tool-manual` 在本元组之上放行 `figure`；`standard`/`product`/`safety` 用八类全集。
"""


class DocTypeRule(Model):
    """单条组合规则。

    ``allowed_atom_types`` 用基底原子名（八类）；``allowed_atom_variants`` 是**变体白名单**
    （``table.register_field`` 等形式），空元组 = 该类**不放行任何变体**——变体是类型专属的结构化
    表示，按 doc_type 显式枚举，不随基底原子自动放行。``required_atom_types`` 可含变体名
    （如 `safety` 的 ``table.failure_mode``）。
    """

    doc_type: DocType
    allowed_atom_types: tuple[str, ...]
    required_atom_types: tuple[str, ...] = ()
    required_meta_fields: tuple[str, ...] = ()
    allowed_atom_variants: tuple[str, ...] = ()


DOC_TYPE_RULES: dict[str, DocTypeRule] = {
    # 行业标准 spec（PCIe/CXL/JEDEC/AMBA）：首批试点类型（B7/C7），八类原子全可用 +
    # NISO STS 结构化变体（§4.2 register/bitfield 表、state_machine），
    # 必备条款级节点（ADR-006 最小节点），meta 必填 C5 十七字段（§6 映射表）。
    "standard": DocTypeRule(
        doc_type="standard",
        allowed_atom_types=ATOM_TYPES,
        required_atom_types=("clause",),
        required_meta_fields=C5_META_FIELDS,
        allowed_atom_variants=("table.register_field", "figure.state_machine"),
    ),
    # 语言/脚本语法手册（Verilog/TCL/SDC/UPF，§4.1）：无图、无结构化变体；meta 必填命令级三元组。
    "lang": DocTypeRule(
        doc_type="lang",
        allowed_atom_types=LANG_ATOM_TYPES,
        required_atom_types=("clause",),
        required_meta_fields=LANG_META_FIELDS,
    ),
    # EDA 工具手册（§4.1 + §4.5 尾注）：在 `lang` 之上放行 `figure`（工具流程/GUI 示意）；
    # `tool_context`（厂商 + 版本）为差异化必填项。
    "tool-manual": DocTypeRule(
        doc_type="tool-manual",
        allowed_atom_types=(*LANG_ATOM_TYPES, "figure"),
        required_atom_types=("clause",),
        required_meta_fields=LANG_META_FIELDS,
    ),
    # 内部产品 spec（MRD/PRD/架构/MAS/IP/接口/寄存器/验证/测试/评审/ECO/Errata…，§4.3+§4.5）：
    # 八类原子全可用；细分靠 `meta.doc_subtype`（映射文档 §2 收敛原则），故只约束共性必填
    # （子类型标识 + 需求追溯链 + 责任人）；变体含寄存器表、state_machine 与 UCIS/vPlan 覆盖矩阵。
    "product": DocTypeRule(
        doc_type="product",
        allowed_atom_types=ATOM_TYPES,
        required_atom_types=("clause",),
        required_meta_fields=("doc_subtype", "traces_to", "owner"),
        allowed_atom_variants=("table.register_field", "figure.state_machine", "table.coverage_matrix"),
    ),
    # 功能安全（FMEA/FTA + 认证合规，§4.5）：八类原子 + 唯一专属变体 `table.failure_mode`；
    # 必填 `standard_ref`（指向安全标准具体条款）与 `audit_trail`（审计留痕）。
    #
    # **变体非必备（实现裁决 2026-09-17，真实语料驱动）**：`table.failure_mode` 仅入
    # `allowed_atom_variants`（白名单），**不列入 `required_atom_types`**——因为真实安全文档
    # 未必含失效模式表（实测：`neqsim-FMEA.md` 是 FMEA *方法说明*（叙述+代码示例），
    # `protective-stop-FMEDA.md` 是 FMEDA *参数表*，`cdriscv-FMEDA.md` 无管道表）。
    # 若把变体设为必备，M09A 门禁会拒收这些真实文档——「有则用变体，无则不强制」。
    # 需要强制失效模式表的场景，应由具体 `meta.doc_subtype`（如 `fmea-worksheet`）承担。
    "safety": DocTypeRule(
        doc_type="safety",
        allowed_atom_types=ATOM_TYPES,
        required_atom_types=("clause",),
        required_meta_fields=("standard_ref", "audit_trail"),
        allowed_atom_variants=("table.failure_mode",),
    ),
}


def register_doc_type_rule(rule: DocTypeRule) -> None:
    """注册/覆盖一条组合规则（Q6：非 standard 类型细化时由 M03/M09A 调用）。

    写入前做四项单点校验，防规则表自身悬空：基底原子须为八类之一；变体名须已注册
    （``ATOM_VARIANTS``）**且**其基底在该类的 ``allowed_atom_types`` 内；``required_atom_types``
    须落在「允许基底 ∪ 变体白名单」内。
    """
    unknown = [atom for atom in rule.allowed_atom_types if atom not in ATOM_TYPES]
    if unknown:
        raise ValueError(f"{rule.doc_type} 的 allowed_atom_types 含未注册原子：{unknown}")
    unknown_variants = [variant for variant in rule.allowed_atom_variants if variant not in ATOM_VARIANTS]
    if unknown_variants:
        raise ValueError(f"{rule.doc_type} 的 allowed_atom_variants 含未注册变体：{unknown_variants}")
    orphans = [
        variant for variant in rule.allowed_atom_variants if variant.split(".", 1)[0] not in rule.allowed_atom_types
    ]
    if orphans:
        raise ValueError(f"{rule.doc_type} 的 allowed_atom_variants 基底未放行：{orphans}")
    unrequired = [
        atom
        for atom in rule.required_atom_types
        if atom not in rule.allowed_atom_types and atom not in rule.allowed_atom_variants
    ]
    if unrequired:
        raise ValueError(f"{rule.doc_type} 的 required_atom_types 超出允许集合：{unrequired}")
    DOC_TYPE_RULES[rule.doc_type] = rule


def get_doc_type_rule(doc_type: str) -> DocTypeRule:
    """取 doc_type 的组合规则；未定义 → :class:`KeyError`（docs.doc_type 受 DDL CHECK 约束）。"""
    try:
        return DOC_TYPE_RULES[doc_type]
    except KeyError:
        raise KeyError(f"未定义 doc_type 组合规则：{doc_type!r}；已定义：{sorted(DOC_TYPE_RULES)}") from None


def allowed_atom_types(doc_type: str) -> tuple[str, ...]:
    """该 doc_type 允许的**基底**原子类型（变体见 :func:`allowed_atom_variants`）。"""
    return get_doc_type_rule(doc_type).allowed_atom_types


def allowed_atom_variants(doc_type: str) -> tuple[str, ...]:
    """该 doc_type 允许的变体白名单（空元组 = 不放行任何变体）。"""
    return get_doc_type_rule(doc_type).allowed_atom_variants


def is_variant_allowed(doc_type: str, atom_type: str) -> bool:
    """`atom_type` 是否为该 doc_type 放行的**变体**（白名单判定；非变体名恒 False）。

    供 M09A 区分 `M01.doc_type.variant`（变体未获该类放行）与 `M01.doc_type.atom`（基底原子不允许）。
    """
    if atom_type not in ATOM_VARIANTS:
        return False
    rule = get_doc_type_rule(doc_type)
    return atom_type in rule.allowed_atom_variants and atom_type.split(".", 1)[0] in rule.allowed_atom_types


def is_atom_allowed(doc_type: str, atom_type: str) -> bool:
    """基底原子按 ``allowed_atom_types`` 判定；变体须在该类**白名单**内
    （``table.register_field`` 不再随基底 ``table`` 自动放行）；
    未注册的类型名（拼错、臆造变体）一律不放行（REQ-M01-F01：无 schema 不得写入）。"""
    if atom_type not in ATOM_SCHEMAS:
        return False
    if atom_type in ATOM_VARIANTS:
        return is_variant_allowed(doc_type, atom_type)
    return atom_type in get_doc_type_rule(doc_type).allowed_atom_types


def missing_required_meta(doc_type: str, meta: Mapping[str, Any] | None) -> list[str]:
    """返回 `meta` 缺失的必填字段（空列表 = 通过），供 M03/M09A 校验消费。"""
    present = meta or {}
    return [field_name for field_name in get_doc_type_rule(doc_type).required_meta_fields if field_name not in present]

