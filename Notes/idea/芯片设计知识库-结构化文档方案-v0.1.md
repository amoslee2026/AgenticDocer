# 芯片设计知识库：结构化文档管理方案（初步）

版本：v0.1

---

## 1. 背景

芯片设计全流程涉及种类繁多、结构异构的文档体系，覆盖从需求定义到量产交付的各个阶段。这些文档需要严格遵守各自的格式规范、语言/脚本语法，同时要支持 coding agent 参与编写与维护，并保留人类评审、批注的协作空间。主要文档类型包括（按流程阶段分组，非穷尽）：

| 阶段 | 文档类型 |
|---|---|
| 需求定义 | MRD（市场需求文档）、PRD（产品需求文档） |
| 架构与设计规格 | 架构规格书（Architecture Spec）、微架构规格书（MAS）、IP/模块设计规格书、接口规格书、寄存器/编程手册（Register/Programming Guide）、时钟复位规格书、低功耗设计规格（Power Intent/UPF 相关文档）、SoC 集成规格书 |
| 验证 | 验证计划（Verification Plan）、测试点/测试计划（Test Plan）、Testbench 架构文档、覆盖率计划（Coverage Plan）、Bug/问题跟踪报告 |
| 物理设计/后端 | Floorplan 规格、时序约束文档（SDC 等）、DFT 规格（scan/ATPG 计划）、Signoff 报告（STA/IR Drop/EM/DRC/LVS）、封装规格 |
| 软件/固件相关 | 驱动开发规格、Boot 流程规格 |
| 制造与工艺 | PDK 文档、Foundry 设计规则（DRC/LVS rule deck）、可靠性规格 |
| 行业标准协议 | PCIe、AXI/AMBA、DDR/JEDEC、USB、MIPI 等总线/接口协议标准 |
| 语言/脚本语法手册 | Verilog/SystemVerilog/VHDL、TCL、UPF、SDC 等语言与脚本语法手册 |
| EDA 工具手册 | 各类 EDA 工具（综合、仿真、布局布线、时序分析、DFT 等）的使用手册、命令参考手册、脚本语言手册（如各厂商 TCL 方言的命令参考） |
| 项目管理与质量 | 设计评审报告/Checklist、ECO 记录、勘误表（Errata Sheet）、Release Notes、面向客户的 Datasheet、Application Note |
| 功能安全（如涉及） | 安全分析报告（FMEA/FTA）、认证/合规文档 |

这些文档共同的痛点是：格式规范繁多且严格、彼此存在引用依赖关系、且需要 coding agent 与人类协同编写维护——这是本方案要解决的核心问题（见第 2 节）。

## 2. 需要解决的问题

| 编号 | 问题 | 说明 |
|---|---|---|
| P1 | 格式合规性 | coding agent 难以 100% 严格遵守 Markdown 等文档格式规范、工具脚本语法，长期维护下容易出现格式漂移 |
| P2 | 跨文档精确引用 | 多份文档（spec 之间、spec 与内部文档之间）存在依赖关系，Markdown 缺乏稳定的跨文档引用机制，标题/路径变化即断链 |
| P3 | 人机协作评审 | 需要支持人类通过评审和批注的方式与 coding agent 协同编辑文档，且批注不能破坏正文格式或被 agent 误覆盖 |
| P4 | 检索与多跳推理 | 知识库定位为精准检索，且 spec 间依赖关系要求支持多跳推理 |
| P5 | 文档异构性 | 语法手册、工业标准 spec、内部产品 spec 三类文档的结构差异大，需要既能分别建模又不重复造轮子的 schema 体系 |

## 3. 总体方案思路

核心原则：**把"格式合规性"从模型能力问题转化为工具链的确定性保证**，即 agent 不直接生成最终格式的文本，而是读写结构化 Schema，由确定性渲染层负责生成人类可读的呈现形式。

```
┌─────────────────────────────────────────────────────┐
│  结构化内容数据库（PostgreSQL，权威源）                 │
│  - 内容原子：requirement / definition / table /       │
│    figure(+state_machine) / code block / example /    │
│    note / cross-reference                              │
│  - 每个节点：稳定 ID（URN）+ source_ref + traces_to    │
│  - 变更以 append-only 事件日志记录（版本与结构化 diff）│
└───────────────┬─────────────────────┬─────────────────┘
                │                     │
      结构化读写（agent/工具调用）     渲染（schema → 呈现）
                │                     │
    ┌───────────▼─────────┐   ┌───────▼────────────┐
    │ agent（结构化生成/  │   │ WebUI（人类阅读/    │
    │ 修改 + lint 闭环）   │   │ 评审/批注）          │
    └──────────────────────┘   │ Markdown/HTML/PDF   │
                                │ 导出（按需）          │
                                └──────────────────────┘
                │
      渲染文本 + node_id metadata（增量同步）
                │
    ┌───────────▼─────────────┐
    │ LightRAG 语义索引层      │
    │（同一 PG 实例，同库不同表）│
    │ 补充"确定性引用图谱"之外  │
    │ 的语义关联，供模糊检索用  │
    └──────────────────────────┘
```

关键设计决策：

1. **内容与呈现分离**：结构化 Schema 是唯一权威源，Markdown/HTML/PDF 都是渲染产物，格式合规性由渲染层保证，而非依赖 agent 严格自律。
2. **确定性引用图谱 + 语义索引图谱并存**：结构化 DB 里的引用关系（`traces_to`）是精确、可审计的确定性图；LightRAG 基于渲染文本自动抽取的图是概率性语义关联，两者互补，检索时先走确定性引用做精确定位，再用语义图做召回补充。
3. **评审与内容解耦**：人类批注作为独立记录，指向内容节点的稳定 ID，不嵌入正文，避免 agent 编辑时污染批注、或批注污染格式。
4. **三类文档共享一套内容原子，各自组合 + 专属元数据**，避免重复建设 schema 和渲染/校验工具链。

## 4. 分文档类型的 Schema 建议

### 4.1 语言/工具语法手册（Verilog、TCL、SystemVerilog、SDC、UPF 等）

- 参考先例：**DocBook `RefEntry`**（即 man page 结构：NAME/SYNOPSIS/DESCRIPTION/OPTIONS/EXAMPLES/SEE ALSO），以及语言参考站（如 cppreference）对文法产生式的组织方式。
- 建议字段：`command_name`、`syntax`（原始语法串，不过度结构化）、`parameters[{name,type,desc}]`、`semantics`、`examples[{code,explain}]`、`see_also[refs]`、`tool_context`（适用的 EDA 工具及版本——同一 TCL 命令在不同厂商工具中语义可能不同，必须显式标注）。
- 语法/文法类内容（如 IEEE 1800 附录 A 的 BNF）：每条产生式作为节点，字段为 `rule_name`、`production`（原始 EBNF 文本）、语义说明、`composes_from`（引用的其他规则）。

### 4.2 行业标准 spec（PCIe、AXI/AMBA、DDR/JEDEC 等）

- 参考先例：**NISO STS（Standards Tag Suite, ANSI/NISO Z39.102）**——ISO/IEC 等标准化组织专门用于标准文档结构化著录的 XML schema，是 JATS 的扩展。
- 建议字段/内容类型：
  - `clause/subclause`（可嵌套编号）+ **规范性关键词标注**（SHALL/SHOULD/MAY/MUST，参照 RFC2119 风格，便于后续按强制性/建议性过滤）
  - `definition`（术语表条目）
  - **register/bitfield 表**（专属表格变体）：`bit_range, field_name, access_type, reset_value, description`
  - `state_machine`（协议状态图，如 PCIe LTSSM）：结构化存储 `states[]`、`transitions[{from,to,condition}]`，支持多跳推理，而非仅存图片引用
  - `source_ref`：指向原始 PDF 的页码/章节号，保证审计可追溯——与现有"PDF 转 Markdown 人工核对"流程衔接

### 4.3 内部产品 spec（MRD、架构 spec、MAS spec、测试点、verification plan）

- 参考先例：**需求追溯（Requirements Traceability）**实践（ISO 26262/DO-254 功能安全流程标配，DOORS/Jama Connect/Polarion 等工具的核心模式）。
- 通用字段：`requirement/clause` + `rationale` + `priority/status` + `traces_to[上游ID列表]`，内容原子与 4.2 通用（复用同一套）。
- **verification plan 建议优先对齐现成标准**：Accellera **UCIS（Unified Coverage Interchange Standard）**，或 Cadence vManager / Siemens Questa 的 **vPlan XML** 格式（feature → sub-feature → coverage item → test → status）。若已使用相关 EDA 工具做验证签核，直接对齐/导入该格式可与现有覆盖率流程打通，避免重复建模。

### 4.4 跨类型共享的内容原子

`requirement/clause`（带规范性关键词 + source_ref + traces_to）、`definition`、`table`（通用 + register-field 变体）、`figure/diagram`（+ 可选结构化 state_machine）、`code/syntax block`、`example`、`note`、`cross-reference`。三类文档仅是这组原子的不同组合，渲染、lint、图谱边生成逻辑可完全复用。

以下所有类型默认继承的公共字段，不逐项重复列出：`id`（稳定 URN）、`version/revision`、`status`（draft/reviewed/approved 等）、`traces_to`（上游追溯 ID 列表，适用于需求类文档）、`source_ref`（外部摄入文档需注明原文页码/章节）。

### 4.5 逐类型 Schema 字段建议

**需求定义**

| 类型 | 关键字段 |
|---|---|
| MRD | `market_context`、`requirement`（text）、`priority`、`target_segment`、`rationale` |
| PRD | `requirement` + 规范性关键词、`acceptance_criteria`、`priority`、`owner`、`traces_to`[MRD] |

**架构与设计规格**（内容原子以 `requirement/clause`、`table`、`figure` 为主）

| 类型 | 关键字段 |
|---|---|
| Architecture Spec | `component`（所属子系统）、`interfaces_ref`（引用接口规格书 clause）、`traces_to`[PRD]、block diagram（figure） |
| MAS（微架构规格书） | `module_name`、pipeline/state_machine（figure）、`timing_constraints_ref`、`power_domain_ref`、`traces_to`[Architecture Spec] |
| IP/模块设计规格书 | `ip_name`/`version`、`port_list`（name/direction/width/description 表）、`parameter_list`（可配置参数表）、`integration_notes` |
| 接口规格书 | `interface_name`、`protocol_ref`（关联行业标准 spec 的具体条款 ID）、`signal_table`（信号名/方向/宽度/描述）、timing diagram（figure）、`compliance_notes`（与标准差异说明） |
| 寄存器/编程手册 | 复用 register/bitfield 表（`bit_range`/`field_name`/`access_type`/`reset_value`/`description`）、`register_address`、`module_ref`、`programming_sequence`（example） |
| 时钟复位规格书 | `clock_domain_name`/`reset_domain_name`、`frequency_divider_table`、`reset_type`、reset sequence（state_machine）、`cdc_notes` |
| 低功耗设计规格（UPF） | `power_domain_name`、`power_states_table`（状态/电压/描述）、`upf_code_ref`（code block）、power sequence（state_machine） |
| SoC 集成规格书 | top-level block diagram（figure）、`ip_instance_list`（IP名/实例名/版本/配置）、`interconnect_topology`、**`address_map`**（起始地址/结束地址/所属模块，建议单独建模为专属表变体） |

**验证**

| 类型 | 关键字段 |
|---|---|
| Verification Plan | 建议直接对齐 vPlan/UCIS 结构：`feature`→`sub-feature`→`coverage_item`→`test`→`status`；`traces_to`[需求/架构 spec ID] 是需求追溯链的关键节点 |
| Test Plan/测试点 | `test_id`、`test_type`（directed/random/formal）、`pass_criteria`、`traces_to`[verification plan feature] |
| Testbench 架构文档 | 复用 architecture spec 模式：`component_list`（agent/scoreboard/checker 表）、`interface_ref`（关联 DUT 接口规格）、代码引用（UVM 组件） |
| Coverage Plan | `coverage_group_name`、`coverage_points`（bin名/描述/目标 表）、`cross_coverage`、`traces_to`[verification plan feature] |
| Bug/问题跟踪报告 | `severity`、`repro_steps`（example）、`root_cause`、`resolution`、`traces_to`[相关需求/测试 ID]；建议这类过程性记录以知识沉淀/检索为目的轻量纳入，过程管理仍走专门的 issue tracking 系统 |

**物理设计/后端**

| 类型 | 关键字段 |
|---|---|
| Floorplan 规格 | `block_name`、`area_constraint`、`aspect_ratio`、placement diagram（figure）、`pin_assignment_table` |
| 时序约束文档（SDC） | 按"脚本文件"处理：`code block`（实际 SDC 脚本）+ 语义注解（约束类型如 create_clock/set_false_path + 参数说明），复用 4.1 语法手册模式 |
| DFT 规格 | `scan_chain_config`（chain名/长度/关联flop 表）、`atpg_plan`（test_mode 列表+覆盖率目标）、`traces_to`[design spec 的 test mode 相关字段] |
| Signoff 报告（STA/IR Drop/EM/DRC/LVS） | `tool_used`/`tool_version`、`metric_table`（违例数/corner/结果）、`status`（pass/fail/waived）+`waiver_reason`；建议存"结构化摘要 + 原始工具报告归档链接"，不做逐字结构化 |
| 封装规格 | `package_type`、`pinout_table`（pin号/名称/功能）、`thermal_electrical_characteristics` |

**软件/固件相关**

| 类型 | 关键字段 |
|---|---|
| 驱动开发规格 | `driver_name`、`target_hardware_ref`（关联 register spec）、`api_list`（函数名/参数/描述/示例，复用 DocBook RefEntry 思路）、`register_access_notes` |
| Boot 流程规格 | `boot_stage_table`（阶段名/顺序/描述）、flow diagram（state_machine）、依赖的 reset/clock spec 引用 |

**制造与工艺**（多为外部摄入文档，处理方式同行业标准 spec：`source_ref` + clause 结构）

| 类型 | 关键字段 |
|---|---|
| PDK 文档 | `device_model_table`（器件模型参数）、`source_ref`（foundry 原文档） |
| Foundry 设计规则（DRC/LVS rule deck） | `rule_id`、`rule_type`（DRC/LVS）、规则脚本片段（code block）+ 语义说明、`layer_ref` |
| 可靠性规格 | `reliability_metric`（EM/TDDB/NBTI 等）、`test_condition_table`、`pass_criteria` |

**行业标准协议 / 语言脚本语法手册 / EDA 工具手册**：已在 4.1–4.2 给出具体字段建议（NISO STS 风格 clause+规范性关键词+register-field表+state_machine；DocBook RefEntry 风格 command/syntax/parameters/examples）。EDA 工具手册在 4.1 基础上额外强调 `tool_context`（厂商+版本）字段，因同一命令在不同工具/版本间语义可能不同。

**项目管理与质量**

| 类型 | 关键字段 |
|---|---|
| 设计评审报告/Checklist | `review_type`、`checklist_items`（item/状态/备注 表）、`action_items`（描述/owner/due_date/status 表）、`traces_to`[被评审的 spec ID] |
| ECO 记录 | `eco_id`、`reason`、`affected_modules`（关联 design spec ID）、`change_description`（diff式）、`approval_status`、`traces_to`[原始 bug/需求 ID] |
| 勘误表（Errata Sheet） | `affected_revision`、`issue_description`、`workaround`、`status`（open/fixed_in_next_rev）、`traces_to`[相关 register/spec clause] |
| Release Notes | `version`/`release_date`、`change_list`（类型/描述/traces_to ID 表）、关联 errata |
| 面向客户的 Datasheet | 不单独建模内容原子，建议定义为"渲染视图"——从 architecture spec/register spec 等选取子集 + 面向客户措辞层，复用 `pinout_table` 等已有结构 |
| Application Note | `topic`/`use_case_description`，内容以 `example` 为主（场景+代码/配置示例）、`traces_to`[关联产品/register spec] |

**功能安全（如涉及）**

| 类型 | 关键字段 |
|---|---|
| 安全分析报告（FMEA/FTA） | `failure_mode_table`（失效模式/影响/严重度/检测方法/RPN，建议作为专属表变体，类似 register table 的处理方式）、`traces_to`[相关设计模块]、`mitigation` |
| 认证/合规文档 | `standard_ref`（指向安全标准具体条款，类似 `source_ref`）、`compliance_evidence_table`（要求条款 vs 证据材料）、`audit_trail` |

## 5. Agent 协作与格式合规机制

- **Agent 输出结构化字段，而非直接输出最终格式文本**：通过 function calling / JSON Schema 约束（可选 grammar-constrained decoding，如 Outlines/guidance-ai）保证结构合法。
- **Lint + 自修复闭环**：对确需生成文本的场景（如渲染后的 Markdown 导出），接入 markdownlint/remark-lint + Vale（可定制芯片行业术语规则），将报错反馈给 agent 自我修正，直至通过。
- **Git PR 式评审流程**：agent 的修改以结构化 diff（按 node_id 对比字段变化）呈现，人类通过 webui 评审、批注；批注独立存储、指向 node_id，不侵入正文。

### 5.1 自研 WebUI 的建议 MVP 功能范围

参考商业 CCMS 的核心能力，但只做真正需要的这几项，避免重蹈"过度设计导致工具变重"的覆辙：

| 功能 | 说明 |
|---|---|
| Schema 驱动的渲染/编辑表单 | 每种内容原子（requirement/table/figure/code block 等）对应一套表单模板，新增文档类型只需定义 schema，不需要为每种类型手写 UI——可参考 **Sanity Studio**（开源、MIT 协议）"schema → 自动生成编辑表单"的实现思路，不接入其云服务，只借鉴渲染引擎的设计模式，实际后端仍对接自建的 PostgreSQL |
| 结构化 diff 展示 | 按 node_id 做字段级对比（新旧值并排展示），而非文本行级 diff |
| 批注（独立于正文） | 评论指向具体 node_id，支持 open/resolved 状态，不写入正文字段 |
| 追溯关系查看 | 以简单表格形式列出某节点的上游/下游 `traces_to` 关系即可满足 v0 需求，图形化可视化作为后续迭代项，不必一开始就做 |
| 状态流转 | draft/reviewed/approved 等基础状态 + 审批记录，不需要复杂工作流引擎 |
| 版本历史 | 基于 append-only 变更日志，展示某节点的历史版本列表，支持回看 |

明确**不做**的部分（这些正是商业 CCMS 显重的原因）：复杂可配置工作流引擎、多项目多层级组织架构管理、内置报表仪表盘、与外部 PLM/ALM 系统的双向集成。这些如果未来确有需求，再按需增量添加。

## 6. 检索层（LightRAG）集成方式

- LightRAG 与结构化内容库**同一 PG 实例、同库不同表**，通过 `node_id` 关联，不做跨系统同步。
- 喂给 LightRAG 的是**渲染后的纯文本片段**（而非原始 JSON），并在 metadata 中携带 `node_id`，使语义检索命中后可直接回查结构化权威记录。
- 增量更新：结构化 DB 的 append-only 变更日志驱动 LightRAG 的增量索引更新，避免全量重跑；接受语义索引层的短暂滞后，正确性始终以结构化 DB 为准。
- 职责划分：结构化 DB 中的引用关系是**确定性图**（精确引用/追溯），LightRAG 图是**概率性语义关联**（补充未显式建模但语义相关的内容），检索时两者结合使用。

## 7. 建议技术栈

| 层次 | 建议方案 |
|---|---|
| 结构化内容存储 | PostgreSQL（JSONB 存节点内容）+ 关系表存引用边；或图数据库承载引用图谱 |
| 版本与变更管理 | Append-only 变更事件日志（event sourcing 思路），支持结构化 diff 与历史回溯 |
| 渲染层 | Schema-type → 模板的映射引擎，产出 Markdown/HTML/PDF |
| 格式校验 | markdownlint/remark-lint + Vale（自定义规则） |
| Agent 结构化输出约束 | Function calling / JSON Schema；可选 Outlines、guidance-ai 等 grammar-constrained decoding |
| 语义检索 | LightRAG（同 PG 实例，同库不同表） |
| 评审协作 | WebUI（结构化 diff 呈现 + 独立批注表，指向 node_id） |

## 8. 参考/准寻的成熟标准

- **DocBook `RefEntry`**：命令/API 参考文档结构（语法手册）
- **NISO STS（ANSI/NISO Z39.102）**：标准文档结构化著录（行业标准 spec）
- **RFC2119 风格规范性关键词**：SHALL/SHOULD/MAY/MUST 标注
- **Accellera UCIS / vPlan（Cadence vManager、Siemens Questa）**：verification plan 结构化互换格式
- **需求追溯实践（ISO 26262 / DO-254 常用模式，DOORS/Jama Connect/Polarion 等工具体现）**：MRD/架构 spec/MAS 的追溯链设计
- **Portable Text（Sanity 提出的 block 化富文本模型）**：内容原子设计思路参考

## 9. 待明确事项

- ~~结构化内容存储最终选型~~ → **已确定**：纯 PostgreSQL（JSONB），不引入独立图数据库；引用关系图在 PG 内建模为关系表，多跳/语义检索由 LightRAG 层承担（图 RAG 检索）。
- WebUI 评审工具：**已确定自研**，不采购 DOORS/Jama/Polarion 等商业 CCMS/需求管理工具——这类工具面向的是合规审计场景，定价按席位、部署偏重，若暂无强制认证需求（如 ISO 26262），性价比不高。追溯关系（`traces_to`）这一核心概念已在自建 PG schema 中实现，无需额外采购。如未来需要与外部供应商/客户交换需求数据，可评估 **ReqIF（Requirements Interchange Format）** 这一开放交换格式；**Doorstop**、**strictdoc** 是两个开源轻量级 Git-based 需求追溯工具，可作为字段设计参考。自研 WebUI 的建议 MVP 功能范围见 5.1。
- ~~verification plan 是否直接对齐现有 EDA 工具的 vPlan/UCIS 格式~~ → **已确定**：对齐 Accellera UCIS / vPlan 格式导入导出。
- 首批试点文档类型与范围: GigaRAG里的规范文档
