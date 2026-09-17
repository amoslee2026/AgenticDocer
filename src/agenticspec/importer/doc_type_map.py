"""M03 文档类型映射表（方案 C 追溯层）：idea.md §4.5 的 30+ 文档类型 → `docs.doc_type`。

**权威依据**：`spec/arch_spec/doc_type_mapping.md` §2（映射表）+ §4（UCIS/vPlan 对齐）。
本模块是那张表的**机器可读形式**（唯一副本）：frontmatter 推断（:mod:`agenticspec.importer.
frontmatter`）与测试（`tests/unit/test_doc_type_mapping.py`）都引用它，映射不散落多处。

两条纪律：

1. **`doc_type` 只有 5 值**（`:data:`agenticspec.model.DOC_TYPES`，与 DDL 的 CHECK 同域）。
   idea.md 的中等粒度类型按「收敛原则」落到 `doc_type` + `meta.doc_subtype`——多数类型的
   **内容原子组合相同**（clause + table + figure + example），差异只在业务元数据，
   故不为其新增 `doc_type`；
2. **不在此处定义 schema**（P5 单点）：本模块只做「类型名 → `doc_type`/`doc_subtype`」的
   **分类**；原子 schema 在 :mod:`agenticspec.model.atoms`，组合规则在
   :mod:`agenticspec.model.doc_types`。

**验证边界**（映射表 §5）：仅 `standard` 有真实语料（7 份）可端到端验证；本模块登记的其余
类型**只有 schema 定义 + 合成样例**，不得声称端到端验证。
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Final

from agenticspec.model import DOC_TYPES

__all__ = [
    "STATUS_DELIVERED",
    "STATUS_SPECIFIED",
    "STATUS_REGISTERED",
    "STATUSES",
    "STANDARDS",
    "DocTypeMapping",
    "IDEA_DOC_TYPES",
    "SPEC_ROWS",
    "PRODUCT_SUBTYPES",
    "MAPPINGS_BY_SLUG",
    "ALIASES",
    "RESOLVABLE_KEYS",
    "UnknownDocTypeError",
    "DocTypeResolution",
    "resolve_doc_type",
    "mapping_for",
    "subtypes_for",
    "VERIFICATION_PLAN_SUBTYPE",
    "VERIFICATION_PLAN_FORMATS",
    "missing_verification_plan_meta",
    "invalid_verification_plan_format",
]

# ── 首版状态（对应映射表 §2「首版状态」列）────────────────────────────────

STATUS_DELIVERED: Final = "delivered"
"""已交付：有真实语料，端到端可验证（当前仅 `standard`）。"""

STATUS_SPECIFIED: Final = "specified"
"""本文档（方案 C）落实：schema/变体已定义，单元验证 + 合成样例。"""

STATUS_REGISTERED: Final = "registered"
"""登记：类型已映射到 `doc_type`，专属字段/变体延后（映射表 §2 标注「登记」）。"""

STATUSES: Final = (STATUS_DELIVERED, STATUS_SPECIFIED, STATUS_REGISTERED)

# ── 参考的行业标准（idea.md §8）──────────────────────────────────────────

STD_NISO_STS: Final = "NISO STS (ANSI/NISO Z39.102)"
STD_DOCBOOK_REFENTRY: Final = "DocBook RefEntry"
STD_RFC2119: Final = "RFC2119/8174 规范性关键词"
STD_TRACEABILITY: Final = "需求追溯实践（ISO 26262 / DO-254；ReqIF 交换格式）"
STD_UCIS_VPLAN: Final = "Accellera UCIS / vPlan XML (Cadence vManager / Siemens Questa)"

STANDARDS: Final = (
    STD_NISO_STS,
    STD_DOCBOOK_REFENTRY,
    STD_RFC2119,
    STD_TRACEABILITY,
    STD_UCIS_VPLAN,
)
"""本系统引用的成熟标准集合（每个映射条目必须声明其 `standard`）。"""


@dataclass(frozen=True)
class DocTypeMapping:
    """一条「idea.md 文档类型 → `doc_type`（+ `doc_subtype`）」映射。

    字段与映射表 §2 的列一一对应，另加可被 frontmatter 直接书写的 `slug` 与别名。
    """

    slug: str
    """稳定标识（`spec_type`/`doc_subtype` 的推荐取值，kebab-case）。"""

    label: str
    """idea.md 中的类型名（中文/原文，便于与上游文档对照）。"""

    doc_type: str
    """本系统 `doc_type`（5 值之一）。"""

    doc_subtype: str | None
    """`product` 大类的细分（写入 `meta.doc_subtype`）；非细分类型为 ``None``。"""

    spec_row: str
    """所属的映射表 §2 行（组标签，与 §2 首列逐字相同）。"""

    standard: str
    """参考的行业标准/成熟模板（:data:`STANDARDS` 之一）。"""

    idea_fields: tuple[str, ...]
    """idea.md §4.5 给出的关键字段（追溯上游设计依据）。"""

    status: str
    """首版状态（:data:`STATUSES` 之一）。"""

    note: str | None = None
    """补充说明（如「渲染视图，不建模」）。"""


# ── 映射表 §2 的逐行落实（idea.md §4.5 的 30+ 类型）──────────────────────
#
# 顺序 = idea.md §4.5 与映射表 §2 的阅读顺序；`spec_row` 逐字复制 §2 首列。

IDEA_DOC_TYPES: tuple[DocTypeMapping, ...] = (
    # 行业标准协议（§4.2）：NISO STS 风格 clause + 规范性关键词 + 专属表/图变体。
    DocTypeMapping(
        slug="industry-standard",
        label="行业标准协议（PCIe/AMBA/JEDEC/CXL）",
        doc_type="standard",
        doc_subtype="industry-protocol",
        spec_row="行业标准协议（PCIe/AMBA/JEDEC/CXL）",
        standard=STD_NISO_STS,
        idea_fields=(
            "clause",
            "normative_keywords(RFC2119)",
            "definition",
            "table.register_field",
            "figure.state_machine",
            "source_ref",
        ),
        status=STATUS_DELIVERED,
    ),
    # 语言/脚本语法手册（§4.1）：DocBook RefEntry 结构。
    DocTypeMapping(
        slug="lang-manual",
        label="语言/脚本语法手册（Verilog/TCL/SDC/UPF）",
        doc_type="lang",
        doc_subtype="lang-manual",
        spec_row="语言/脚本语法手册（Verilog/TCL/SDC/UPF）",
        standard=STD_DOCBOOK_REFENTRY,
        idea_fields=(
            "command_name",
            "syntax",
            "parameters",
            "semantics",
            "examples",
            "see_also",
            "tool_context",
        ),
        status=STATUS_SPECIFIED,
    ),
    DocTypeMapping(
        slug="grammar-ref",
        label="文法产生式参考（IEEE 1800 附录 A BNF）",
        doc_type="lang",
        doc_subtype="grammar-ref",
        spec_row="语言/脚本语法手册（Verilog/TCL/SDC/UPF）",
        standard=STD_DOCBOOK_REFENTRY,
        idea_fields=("rule_name", "production", "semantics", "composes_from"),
        status=STATUS_SPECIFIED,
    ),
    # EDA 工具手册：同 §4.1，但 `tool_context`（厂商+版本）**必填**——同一命令在不同工具/
    # 版本语义可能不同。
    DocTypeMapping(
        slug="eda-command-ref",
        label="EDA 工具手册（命令参考）",
        doc_type="tool-manual",
        doc_subtype="eda-command-ref",
        spec_row="EDA 工具手册（命令参考）",
        standard=STD_DOCBOOK_REFENTRY,
        idea_fields=(
            "command_name",
            "syntax",
            "parameters",
            "semantics",
            "examples",
            "see_also",
            "tool_context(必填：厂商+版本)",
        ),
        status=STATUS_SPECIFIED,
    ),
    # 需求定义（§4.5）：追溯链起点。
    DocTypeMapping(
        slug="mrd",
        label="MRD（市场需求文档）",
        doc_type="product",
        doc_subtype="mrd",
        spec_row="MRD / PRD",
        standard=STD_TRACEABILITY,
        idea_fields=("market_context", "requirement", "priority", "target_segment", "rationale"),
        status=STATUS_SPECIFIED,
    ),
    DocTypeMapping(
        slug="prd",
        label="PRD（产品需求文档）",
        doc_type="product",
        doc_subtype="prd",
        spec_row="MRD / PRD",
        standard=STD_TRACEABILITY,
        idea_fields=(
            "requirement",
            "normative_keywords",
            "acceptance_criteria",
            "priority",
            "owner",
            "traces_to[MRD]",
        ),
        status=STATUS_SPECIFIED,
    ),
    # 架构与设计规格（§4.5）。
    DocTypeMapping(
        slug="architecture-spec",
        label="Architecture Spec（架构规格书）",
        doc_type="product",
        doc_subtype="architecture-spec",
        spec_row="Architecture Spec / MAS / IP 设计规格 / 接口规格",
        standard=STD_TRACEABILITY,
        idea_fields=("component", "interfaces_ref", "traces_to[PRD]", "block_diagram(figure)"),
        status=STATUS_SPECIFIED,
    ),
    DocTypeMapping(
        slug="mas",
        label="MAS（微架构规格书）",
        doc_type="product",
        doc_subtype="mas",
        spec_row="Architecture Spec / MAS / IP 设计规格 / 接口规格",
        standard=STD_TRACEABILITY,
        idea_fields=(
            "module_name",
            "pipeline/state_machine(figure)",
            "timing_constraints_ref",
            "power_domain_ref",
            "traces_to[Architecture Spec]",
        ),
        status=STATUS_SPECIFIED,
    ),
    DocTypeMapping(
        slug="ip-design-spec",
        label="IP/模块设计规格书",
        doc_type="product",
        doc_subtype="ip-design-spec",
        spec_row="Architecture Spec / MAS / IP 设计规格 / 接口规格",
        standard=STD_TRACEABILITY,
        idea_fields=("ip_name", "version", "port_list", "parameter_list", "integration_notes"),
        status=STATUS_SPECIFIED,
    ),
    DocTypeMapping(
        slug="interface-spec",
        label="接口规格书",
        doc_type="product",
        doc_subtype="interface-spec",
        spec_row="Architecture Spec / MAS / IP 设计规格 / 接口规格",
        standard=STD_TRACEABILITY,
        idea_fields=(
            "interface_name",
            "protocol_ref",
            "signal_table",
            "timing_diagram(figure)",
            "compliance_notes",
        ),
        status=STATUS_SPECIFIED,
    ),
    DocTypeMapping(
        slug="register-manual",
        label="寄存器/编程手册",
        doc_type="product",
        doc_subtype="register-manual",
        spec_row="寄存器/编程手册",
        standard=STD_TRACEABILITY,
        idea_fields=(
            "table.register_field(bit_range/field_name/access_type/reset_value)",
            "register_address",
            "module_ref",
            "programming_sequence(example)",
        ),
        status=STATUS_SPECIFIED,
    ),
    DocTypeMapping(
        slug="clock-reset-spec",
        label="时钟复位规格书",
        doc_type="product",
        doc_subtype="clock-reset-spec",
        spec_row="时钟复位/低功耗/SoC 集成规格",
        standard=STD_TRACEABILITY,
        idea_fields=(
            "clock_domain_name",
            "reset_domain_name",
            "frequency_divider_table",
            "reset_type",
            "reset_sequence(state_machine)",
            "cdc_notes",
        ),
        status=STATUS_REGISTERED,
        note="专属字段已登记；变体（frequency_divider_table）延后（映射表 §2）。",
    ),
    DocTypeMapping(
        slug="power-intent-spec",
        label="低功耗设计规格（UPF）",
        doc_type="product",
        doc_subtype="power-intent-spec",
        spec_row="时钟复位/低功耗/SoC 集成规格",
        standard=STD_TRACEABILITY,
        idea_fields=(
            "power_domain_name",
            "power_states_table",
            "upf_code_ref(code)",
            "power_sequence(state_machine)",
        ),
        status=STATUS_REGISTERED,
        note="专属字段已登记；变体（power_states_table）延后（映射表 §2）。",
    ),
    DocTypeMapping(
        slug="soc-integration-spec",
        label="SoC 集成规格书",
        doc_type="product",
        doc_subtype="soc-integration-spec",
        spec_row="时钟复位/低功耗/SoC 集成规格",
        standard=STD_TRACEABILITY,
        idea_fields=(
            "block_diagram(figure)",
            "ip_instance_list",
            "interconnect_topology",
            "address_map",
        ),
        status=STATUS_REGISTERED,
        note="专属字段已登记；地址映射表变体延后（映射表 §2）。",
    ),
    # 验证（§4.3）：verification plan 对齐 UCIS/vPlan（见 importer/vplan.py）。
    DocTypeMapping(
        slug="verification-plan",
        label="Verification Plan（验证计划）",
        doc_type="product",
        doc_subtype="verification-plan",
        spec_row="Verification Plan",
        standard=STD_UCIS_VPLAN,
        idea_fields=(
            "feature",
            "sub_feature",
            "coverage_item",
            "test",
            "status",
            "traces_to[需求/架构 spec ID]",
        ),
        status=STATUS_SPECIFIED,
    ),
    DocTypeMapping(
        slug="test-plan",
        label="Test Plan/测试点",
        doc_type="product",
        doc_subtype="test-plan",
        spec_row="Test Plan / Coverage Plan / Testbench 架构",
        standard=STD_TRACEABILITY,
        idea_fields=(
            "test_id",
            "test_type(directed/random/formal)",
            "pass_criteria",
            "traces_to[verification plan feature]",
        ),
        status=STATUS_SPECIFIED,
    ),
    DocTypeMapping(
        slug="coverage-plan",
        label="Coverage Plan（覆盖率计划）",
        doc_type="product",
        doc_subtype="coverage-plan",
        spec_row="Test Plan / Coverage Plan / Testbench 架构",
        standard=STD_UCIS_VPLAN,
        idea_fields=(
            "coverage_group_name",
            "coverage_points",
            "cross_coverage",
            "traces_to[verification plan feature]",
        ),
        status=STATUS_SPECIFIED,
    ),
    DocTypeMapping(
        slug="testbench-arch",
        label="Testbench 架构文档",
        doc_type="product",
        doc_subtype="testbench-arch",
        spec_row="Test Plan / Coverage Plan / Testbench 架构",
        standard=STD_TRACEABILITY,
        idea_fields=("component_list", "interface_ref", "code_ref(UVM)"),
        status=STATUS_SPECIFIED,
    ),
    DocTypeMapping(
        slug="bug-report",
        label="Bug/问题跟踪报告",
        doc_type="product",
        doc_subtype="bug-report",
        spec_row="Bug/问题跟踪报告",
        standard=STD_TRACEABILITY,
        idea_fields=("severity", "repro_steps(example)", "root_cause", "resolution", "traces_to"),
        status=STATUS_REGISTERED,
        note="过程管理仍走 issue tracking；此处仅作知识沉淀/检索的轻量纳入（idea.md §4.5）。",
    ),
    # 物理设计/后端（§4.5）。
    DocTypeMapping(
        slug="floorplan-spec",
        label="Floorplan 规格",
        doc_type="product",
        doc_subtype="floorplan-spec",
        spec_row="Floorplan / SDC / DFT / Signoff / 封装规格",
        standard=STD_TRACEABILITY,
        idea_fields=(
            "block_name",
            "area_constraint",
            "aspect_ratio",
            "placement_diagram(figure)",
            "pin_assignment_table",
        ),
        status=STATUS_REGISTERED,
    ),
    DocTypeMapping(
        slug="sdc",
        label="时序约束文档（SDC）",
        doc_type="product",
        doc_subtype="sdc",
        spec_row="Floorplan / SDC / DFT / Signoff / 封装规格",
        standard=STD_DOCBOOK_REFENTRY,
        idea_fields=("code(SDC 脚本)", "constraint_type(create_clock/set_false_path)", "parameters"),
        status=STATUS_REGISTERED,
        note="按「脚本文件」处理：code block + 语义注解，复用 §4.1 语法手册模式。",
    ),
    DocTypeMapping(
        slug="dft-spec",
        label="DFT 规格（scan/ATPG 计划）",
        doc_type="product",
        doc_subtype="dft-spec",
        spec_row="Floorplan / SDC / DFT / Signoff / 封装规格",
        standard=STD_TRACEABILITY,
        idea_fields=("scan_chain_config", "atpg_plan", "traces_to[design spec test mode]"),
        status=STATUS_REGISTERED,
    ),
    DocTypeMapping(
        slug="signoff-report",
        label="Signoff 报告（STA/IR Drop/EM/DRC/LVS）",
        doc_type="product",
        doc_subtype="signoff-report",
        spec_row="Floorplan / SDC / DFT / Signoff / 封装规格",
        standard=STD_TRACEABILITY,
        idea_fields=(
            "tool_used",
            "tool_version",
            "metric_table",
            "status(pass/fail/waived)",
            "waiver_reason",
        ),
        status=STATUS_REGISTERED,
        note="存「结构化摘要 + 原始工具报告归档链接」，不做逐字结构化（idea.md §4.5）。",
    ),
    DocTypeMapping(
        slug="package-spec",
        label="封装规格",
        doc_type="product",
        doc_subtype="package-spec",
        spec_row="Floorplan / SDC / DFT / Signoff / 封装规格",
        standard=STD_TRACEABILITY,
        idea_fields=("package_type", "pinout_table", "thermal_electrical_characteristics"),
        status=STATUS_REGISTERED,
    ),
    # 软件/固件（§4.5）。
    DocTypeMapping(
        slug="driver-spec",
        label="驱动开发规格",
        doc_type="product",
        doc_subtype="driver-spec",
        spec_row="驱动开发 / Boot 流程规格",
        standard=STD_DOCBOOK_REFENTRY,
        idea_fields=("driver_name", "target_hardware_ref", "api_list", "register_access_notes"),
        status=STATUS_REGISTERED,
        note="`api_list` 复用 DocBook RefEntry 思路（idea.md §4.5）。",
    ),
    DocTypeMapping(
        slug="boot-spec",
        label="Boot 流程规格",
        doc_type="product",
        doc_subtype="boot-spec",
        spec_row="驱动开发 / Boot 流程规格",
        standard=STD_TRACEABILITY,
        idea_fields=("boot_stage_table", "flow_diagram(state_machine)", "reset/clock spec 引用"),
        status=STATUS_REGISTERED,
    ),
    # 制造与工艺（§4.5）：处理方式同行业标准 spec（`source_ref` + clause 结构）。
    DocTypeMapping(
        slug="pdk-doc",
        label="PDK 文档",
        doc_type="standard",
        doc_subtype="pdk-doc",
        spec_row="PDK / Foundry 规则 / 可靠性规格",
        standard=STD_NISO_STS,
        idea_fields=("device_model_table", "source_ref(foundry 原文档)"),
        status=STATUS_REGISTERED,
        note="外部摄入文档：处理方式同行业标准 spec（idea.md §4.5）。",
    ),
    DocTypeMapping(
        slug="foundry-rules",
        label="Foundry 设计规则（DRC/LVS rule deck）",
        doc_type="standard",
        doc_subtype="foundry-rules",
        spec_row="PDK / Foundry 规则 / 可靠性规格",
        standard=STD_NISO_STS,
        idea_fields=("rule_id", "rule_type(DRC/LVS)", "rule_script(code)", "layer_ref"),
        status=STATUS_REGISTERED,
    ),
    DocTypeMapping(
        slug="reliability-spec",
        label="可靠性规格",
        doc_type="standard",
        doc_subtype="reliability-spec",
        spec_row="PDK / Foundry 规则 / 可靠性规格",
        standard=STD_NISO_STS,
        idea_fields=("reliability_metric(EM/TDDB/NBTI)", "test_condition_table", "pass_criteria"),
        status=STATUS_REGISTERED,
    ),
    # 项目管理与质量（§4.5）。
    DocTypeMapping(
        slug="design-review-report",
        label="设计评审报告/Checklist",
        doc_type="product",
        doc_subtype="design-review-report",
        spec_row="设计评审报告 / ECO / Errata / Release Notes / Datasheet / App Note",
        standard=STD_TRACEABILITY,
        idea_fields=("review_type", "checklist_items", "action_items", "traces_to[被评审 spec ID]"),
        status=STATUS_REGISTERED,
    ),
    DocTypeMapping(
        slug="eco-record",
        label="ECO 记录",
        doc_type="product",
        doc_subtype="eco-record",
        spec_row="设计评审报告 / ECO / Errata / Release Notes / Datasheet / App Note",
        standard=STD_TRACEABILITY,
        idea_fields=(
            "eco_id",
            "reason",
            "affected_modules",
            "change_description",
            "approval_status",
            "traces_to[bug/需求 ID]",
        ),
        status=STATUS_REGISTERED,
    ),
    DocTypeMapping(
        slug="errata-sheet",
        label="勘误表（Errata Sheet）",
        doc_type="product",
        doc_subtype="errata-sheet",
        spec_row="设计评审报告 / ECO / Errata / Release Notes / Datasheet / App Note",
        standard=STD_TRACEABILITY,
        idea_fields=(
            "affected_revision",
            "issue_description",
            "workaround",
            "status(open/fixed_in_next_rev)",
            "traces_to[register/spec clause]",
        ),
        status=STATUS_REGISTERED,
    ),
    DocTypeMapping(
        slug="release-notes",
        label="Release Notes",
        doc_type="product",
        doc_subtype="release-notes",
        spec_row="设计评审报告 / ECO / Errata / Release Notes / Datasheet / App Note",
        standard=STD_TRACEABILITY,
        idea_fields=("version", "release_date", "change_list", "关联 errata"),
        status=STATUS_REGISTERED,
    ),
    DocTypeMapping(
        slug="datasheet",
        label="面向客户的 Datasheet",
        doc_type="product",
        doc_subtype="datasheet",
        spec_row="设计评审报告 / ECO / Errata / Release Notes / Datasheet / App Note",
        standard=STD_TRACEABILITY,
        idea_fields=("渲染视图：architecture spec/register spec 的子集 + 面向客户措辞层",),
        status=STATUS_REGISTERED,
        note="不单独建模内容原子——定义为**渲染视图**（idea.md §4.5）；此条目仅为映射完整性。",
    ),
    DocTypeMapping(
        slug="app-note",
        label="Application Note",
        doc_type="product",
        doc_subtype="app-note",
        spec_row="设计评审报告 / ECO / Errata / Release Notes / Datasheet / App Note",
        standard=STD_TRACEABILITY,
        idea_fields=("topic", "use_case_description", "example", "traces_to[产品/register spec]"),
        status=STATUS_REGISTERED,
    ),
    # 功能安全（§4.5）：专属表变体 `table.failure_mode`。
    DocTypeMapping(
        slug="fmea-fta",
        label="安全分析报告（FMEA/FTA）",
        doc_type="safety",
        doc_subtype="fmea-fta",
        spec_row="安全分析报告（FMEA/FTA）/ 认证合规",
        standard=STD_TRACEABILITY,
        idea_fields=(
            "table.failure_mode(失效模式/影响/严重度/检测方法/RPN)",
            "traces_to[相关设计模块]",
            "mitigation",
        ),
        status=STATUS_SPECIFIED,
    ),
    DocTypeMapping(
        slug="certification-compliance",
        label="认证/合规文档",
        doc_type="safety",
        doc_subtype="certification-compliance",
        spec_row="安全分析报告（FMEA/FTA）/ 认证合规",
        standard=STD_TRACEABILITY,
        idea_fields=(
            "standard_ref",
            "compliance_evidence_table",
            "audit_trail",
        ),
        status=STATUS_SPECIFIED,
    ),
)

SPEC_ROWS: tuple[str, ...] = tuple(dict.fromkeys(mapping.spec_row for mapping in IDEA_DOC_TYPES))
"""映射表 §2 的行标签（按出现顺序去重）——测试拿它与 §2 表格逐行比对（防遗漏/防漂移）。"""

MAPPINGS_BY_SLUG: dict[str, DocTypeMapping] = {mapping.slug: mapping for mapping in IDEA_DOC_TYPES}
"""`slug` → 映射条目（`spec_type`/`doc_subtype` 的推荐取值）。"""

PRODUCT_SUBTYPES: tuple[str, ...] = tuple(
    mapping.doc_subtype
    for mapping in IDEA_DOC_TYPES
    if mapping.doc_type == "product" and mapping.doc_subtype is not None
)
"""`product` 大类的全部细分（写入 `meta.doc_subtype`；不新增 `doc_type`）。"""


# ── importer 侧别名（frontmatter `spec_type` 的自然写法）─────────────────
#
# 上游文档（人工/agent 书写 frontmatter）常写 idea.md 的类型名或其英文缩写；
# 别名在此**归一**到 :data:`MAPPINGS_BY_SLUG` 的 slug，避免把判定散落到调用方。

ALIASES: dict[str, str] = {
    # 行业标准 / 制造工艺
    "standards-spec": "industry-standard",
    "protocol-standard": "industry-standard",
    "bus-protocol": "industry-standard",
    "ip-pdk": "pdk-doc",
    "rule-deck": "foundry-rules",
    "drc-lvs-rules": "foundry-rules",
    "reliability": "reliability-spec",
    # 语言/工具手册
    "language-manual": "lang-manual",
    "syntax-manual": "lang-manual",
    "script-manual": "lang-manual",
    "grammar": "grammar-ref",
    "bnf": "grammar-ref",
    "eda-manual": "eda-command-ref",
    "command-reference": "eda-command-ref",
    "tool-reference": "eda-command-ref",
    # 需求定义
    "market-requirements": "mrd",
    "product-requirements": "prd",
    # 架构与设计规格
    "arch-spec": "architecture-spec",
    "architecture-specification": "architecture-spec",
    "micro-architecture-spec": "mas",
    "microarchitecture-spec": "mas",
    "module-design-spec": "ip-design-spec",
    "design-spec": "ip-design-spec",
    "interface-specification": "interface-spec",
    "register-guide": "register-manual",
    "programming-guide": "register-manual",
    "register-programming-guide": "register-manual",
    "clock-reset-specification": "clock-reset-spec",
    "upf": "power-intent-spec",
    "power-intent": "power-intent-spec",
    "soc-integration": "soc-integration-spec",
    "soc-spec": "soc-integration-spec",
    # 验证
    "vplan": "verification-plan",
    "ucis": "verification-plan",
    "verification": "verification-plan",
    "testpoint": "test-plan",
    "test-point": "test-plan",
    "testpoints": "test-plan",
    "coverage": "coverage-plan",
    "testbench": "testbench-arch",
    "bug-tracking": "bug-report",
    "issue-report": "bug-report",
    # 物理设计/后端
    "floorplan": "floorplan-spec",
    "timing-constraints": "sdc",
    "timing-constraint-doc": "sdc",
    "dft": "dft-spec",
    "atpg-plan": "dft-spec",
    "signoff": "signoff-report",
    "sta-report": "signoff-report",
    "packaging-spec": "package-spec",
    "package-specification": "package-spec",
    # 软件/固件
    "driver-specification": "driver-spec",
    "driver-dev-spec": "driver-spec",
    "boot-specification": "boot-spec",
    "boot-flow": "boot-spec",
    # 项目管理与质量
    "design-review": "design-review-report",
    "review-report": "design-review-report",
    "checklist": "design-review-report",
    "eco": "eco-record",
    "errata": "errata-sheet",
    "release-note": "release-notes",
    "application-note": "app-note",
    # 功能安全
    "fmea": "fmea-fta",
    "fta": "fmea-fta",
    "safety-analysis": "fmea-fta",
    "safety-analysis-report": "fmea-fta",
    "certification": "certification-compliance",
    "compliance-doc": "certification-compliance",
}
"""别名 → slug（`spec_type` 的宽松写法；`slug` 本身与 5 个 `doc_type` 值优先）。"""

RESOLVABLE_KEYS: frozenset[str] = frozenset({*DOC_TYPES, *MAPPINGS_BY_SLUG, *ALIASES})
"""`spec_type` 的全部合法写法（5 个 `doc_type` 值 + slug + 别名）。"""


class UnknownDocTypeError(ValueError):
    """`spec_type` 既不是 `doc_type` 取值域、也不是已知类型别名/slug。"""


@dataclass(frozen=True)
class DocTypeResolution:
    """frontmatter `spec_type` 的归一结果。"""

    doc_type: str
    doc_subtype: str | None
    mapping: DocTypeMapping | None
    raw: str

    @property
    def canonical(self) -> bool:
        """输入本身即 `doc_type` 取值域（未借助别名/slug）→ 无细分信息可推。"""
        return self.mapping is None


def resolve_doc_type(raw: str) -> DocTypeResolution:
    """`frontmatter.spec_type` → ``(doc_type, doc_subtype)``（方案 C 追溯层入口）。

    判定优先级：**`doc_type` 取值域** → **slug** → **别名**（大小写/空白宽松）。
    未知取值抛 :class:`UnknownDocTypeError`（调用方转 ``ValidationError``）。
    """
    key = raw.strip().lower()
    if key in DOC_TYPES:
        return DocTypeResolution(doc_type=key, doc_subtype=None, mapping=None, raw=raw)
    slug = key if key in MAPPINGS_BY_SLUG else ALIASES.get(key)
    if slug is None:
        raise UnknownDocTypeError(raw)
    mapping = MAPPINGS_BY_SLUG[slug]
    return DocTypeResolution(
        doc_type=mapping.doc_type, doc_subtype=mapping.doc_subtype, mapping=mapping, raw=raw
    )


def mapping_for(slug: str) -> DocTypeMapping:
    """按 slug 取映射条目；未知 → :class:`UnknownDocTypeError`。"""
    try:
        return MAPPINGS_BY_SLUG[slug]
    except KeyError:
        raise UnknownDocTypeError(slug) from None


def subtypes_for(doc_type: str) -> tuple[str, ...]:
    """该 `doc_type` 下已登记的细分（`meta.doc_subtype` 合法取值）。"""
    return tuple(
        mapping.doc_subtype
        for mapping in IDEA_DOC_TYPES
        if mapping.doc_type == doc_type and mapping.doc_subtype is not None
    )


# ── `verification-plan` 子类型的额外必填项（映射表 §4：UCIS/vPlan 对齐）─────
#
# 模型层 `DocTypeRule` 是 **doc_type 粒度**（5 值）；子类型粒度的必填项只此一处，
# 故落在映射层（区别于 `model.doc_types.missing_required_meta` 的 doc_type 粒度判定）。

VERIFICATION_PLAN_SUBTYPE: Final = "verification-plan"
"""细分 `product/verification-plan`（idea.md §4.3 的验证计划）。"""

VERIFICATION_PLAN_FORMATS: Final = ("ucis", "vplan", "native")
"""验证计划的来源/交换格式（映射表 §4）：UCIS、vPlan XML、或本系统原生结构。"""


def missing_verification_plan_meta(meta: Mapping[str, Any] | None) -> list[str]:
    """验证计划子类型缺失的必填字段（空列表 = 通过；`verification_plan_format` 见 §4）。"""
    present = meta or {}
    value = str(present.get("verification_plan_format", "")).strip()
    return [] if value else ["verification_plan_format"]


def invalid_verification_plan_format(meta: Mapping[str, Any] | None) -> str | None:
    """`verification_plan_format` 的非法值（``None`` = 合法或未提供）。"""
    value = str((meta or {}).get("verification_plan_format", "")).strip().lower()
    if not value or value in VERIFICATION_PLAN_FORMATS:
        return None
    return value
