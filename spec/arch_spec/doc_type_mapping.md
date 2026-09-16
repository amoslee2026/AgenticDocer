---
title: doc_type → 文档类型映射与行业标准对齐（方案 C）
type: composite
purpose: architecture
audience: both
direction: input
status: draft
version: "1.0.0"
section_meta: "@meta"
---

# doc_type 映射与行业标准对齐

> **背景**：用户质问「不同类型的文档要参考相应的行业标准或成熟模板，设立不同的 schema，这一点是否有遵守？」——核实结论为**主体未落实**。本文档是方案 C（全做）的落地依据。
>
> 上游：`../idea/idea.md` §4（分文档类型的 Schema 建议）、§8（参考的成熟标准）。
> 相关：`architecture_specification.md` §3.0（类型定义）、§3 M01（schema 注册）、ADR-006（粒度与锚）。

## 1. 现状与缺口（核实于 2026-09-17）

| idea.md 要求 | 实现状态 | 证据 |
|---|---|---|
| 三类文档共享内容原子、各自组合（§3 决策 4） | ✅ 已实现 | `model/atoms.py` 8 类原子 + `doc_types.py` 组合规则机制 |
| register/bitfield 表变体（§4.2） | ✅ 已实现 | `ATOM_VARIANTS` 含 `table.register_field` |
| state_machine 结构化（§4.2） | ✅ 已实现 | `ATOM_VARIANTS` 含 `figure.state_machine` |
| 规范性关键词（RFC2119/8174） | ✅ 已实现 | `terms` 表（11 条种子，`data/terms_seed.yaml`） |
| `source_ref` 审计可追溯（§4.2） | ✅ 已实现 | `docs.source_ref` + frontmatter 映射 |
| **30+ 文档类型的逐类型字段 schema（§4.5）** | ❌ **未实现** | 仅 5 个粗粒度 `doc_type`，且 `lang`/`tool-manual`/`product`/`safety` **四条规则与 `standard` 完全相同** |
| DocBook RefEntry 字段（§4.1） | ❌ 未实现 | `tool-manual` 无 `tool_context` 等专属字段 |
| UCIS/vPlan 对齐（§4.3） | ❌ 未实现 | spec 标「延后」但未记入已知限制 |
| MRD/PRD 的 `traces_to` 链（§4.5） | ⚠️ 机制有、约束无 | `refs.traces_to` 存在，但 `product` 类型无必填约束 |

**缺口成因**（有记录的范围裁剪，非疏漏）：
- **B7**（首批文档类型）：「**仅行业标准 spec**」，依据 v0.1 §9 试点 + C7（standards 7 份语料）；回退「逐类型扩展」
- **Q6**（组合规则时机）：「随首个非 `standard` 类型引入时定义」；`schemas` 表已预留扩展位

**但三处为真实缺陷**：
1. **五个 doc_type 规则实质相同** → 差异化是空壳，易被误认为已支持；
2. **从 idea.md 30+ 类型到 5 个 doc_type 的映射无记录** → **追溯断裂**（正是 P2 要解决的问题）；
3. **非 standard 类型的差异化从未被验证**（无语料、无测试）。

## 2. 映射表（修缺陷 2）

idea.md §4.5 的 30+ 类型 → 本系统 `doc_type`（仍为 5 值：细分只加 `meta.doc_subtype`）：

| idea.md 文档类型（§4.5） | 本系统 `doc_type` | 专属字段（来自 idea.md） | 首版状态 |
|---|---|---|---|
| 行业标准协议（PCIe/AMBA/JEDEC/CXL） | `standard` | `spec_org` / `spec_revision` / 规范性关键词 / `source_ref` | **✅ 已交付（有语料）** |
| 语言/脚本语法手册（Verilog/TCL/SDC/UPF） | `lang` | `command_name` / `syntax` / `parameters[]` / `tool_context` | **本文档落实** |
| EDA 工具手册（命令参考） | `tool-manual` | 同 `lang` + **强制** `tool_context`（厂商+版本，§4.1） | **本文档落实** |
| MRD / PRD | `product` | `market_context` / `acceptance_criteria` / **`traces_to`** | **本文档落实** |
| Architecture Spec / MAS / IP 设计规格 / 接口规格 | `product` | `component` / `interfaces_ref` / `module_name` / `port_list` | **本文档落实**（同 `product`，字段差异入 `meta`） |
| 寄存器/编程手册 | `product` | `register_address` / `module_ref` + `table.register_field` 变体 | **本文档落实** |
| 时钟复位/低功耗/SoC 集成规格 | `product` | `clock_domain_name` / `power_domain_name` / `address_map` 变体 | 登记（变体延后） |
| Verification Plan | `product` | **UCIS/vPlan** 结构（`feature→sub-feature→coverage_item→test→status`） | **§4 落实** |
| Test Plan / Coverage Plan / Testbench 架构 | `product` | `test_id` / `pass_criteria` / `coverage_group_name` | **本文档落实** |
| Bug/问题跟踪报告 | `product` | `severity` / `repro_steps` / `root_cause` | 登记（轻量纳入） |
| Floorplan / SDC / DFT / Signoff / 封装规格 | `product` | `block_name` / `scan_chain_config` / `tool_used` / `package_type` | 登记 |
| 驱动开发 / Boot 流程规格 | `product` | `driver_name` / `boot_stage_table` | 登记 |
| PDK / Foundry 规则 / 可靠性规格 | `standard` | `source_ref` + clause 结构（§4.5「处理方式同行业标准 spec」） | **登记**（同 `standard`） |
| 设计评审报告 / ECO / Errata / Release Notes / Datasheet / App Note | `product` | `review_type` / `eco_id` / `affected_revision` / `version` | 登记（Datasheet = 渲染视图，不建模） |
| 安全分析报告（FMEA/FTA）/ 认证合规 | `safety` | `failure_mode_table` 变体 / `standard_ref` / `audit_trail` | **本文档落实**（含新变体） |

> **收敛原则**：idea.md 的多数类型落在 `product` 大类下，差异体现在 **`meta` 字段**（不新增 `doc_type`），因为它们的**内容原子组合相同**（clause + table + figure + example），差异只在业务元数据。仅当**内容原子组合确实不同**时才新增 `doc_type`（如 `safety` 需要 `failure_mode_table` 变体）。

## 3. 五个 doc_type 的差异化规则（修缺陷 1）

（详见 `architecture_specification.md` §3 M01 的实现契约；此处为设计依据）

| doc_type | `allowed_atom_types` | `required_atom_types` | `required_meta_fields` | 专属变体 |
|---|---|---|---|---|
| `standard` | 八类全 | `clause` | C5 十七字段 | `table.register_field`、`figure.state_machine` |
| `lang` | `clause`/`definition`/`code`/`example`/`note`/`cross_ref`/`table` | `clause` | `command_name`、`syntax`、`tool_context` | — |
| `tool-manual` | 同 `lang` + `figure` | `clause` | 同 `lang` 三元组（**`tool_context` 语义更强**——idea.md L164「在 4.1 基础上**额外强调** `tool_context`」，故非「仅此一项」，实现裁决 2026-09-17） | — |
| `product` | 八类全 | `clause` | `doc_subtype`、`traces_to`（需求追溯链）、`owner` | **3 变体**：`table.register_field`（§2 寄存器手册）、`figure.state_machine`（§4.5 MAS pipeline / 时钟复位 reset sequence / Boot flow）、`table.coverage_matrix`（UCIS/vPlan）——实现裁决 2026-09-17，原表只列 UCIS/vPlan 属漏写 |
| `safety` | 八类全 | `clause`（**注意：不含 `table.failure_mode`**，见下） | `standard_ref`、`audit_trail` | **`table.failure_mode`（新增，白名单而非必备）** |

> **变体必备性裁决（2026-09-17，真实语料驱动）**：`safety` 的 `table.failure_mode` 为
> **allowed（白名单）而非 required**。理由：实测三份真实安全语料（`neqsim-FMEA.md` 是 FMEA
> *方法说明*、`protective-stop-FMEDA.md` 是 FMEDA *参数表*、`cdriscv-FMEDA.md` 无管道表）
> **均不含失效模式工作表**——若设为必备，M09A 门禁会**拒收真实文档**。
> 「有则用变体，无则不强制」；需强制的场景由 `meta.doc_subtype`（如 `fmea-worksheet`）承担。
>
> **通用原则**：**变体不应作为 `required_atom_types`**——真实文档的形态差异大，
> 必备约束只应用于「所有该类型文档必然具备」的原子（如 `clause`）。

## 4. UCIS/vPlan 对齐（修缺陷 3）

`idea.md` §4.3 + §9：「verification plan 建议优先对齐 Accellera **UCIS** 或 **vPlan XML**（feature → sub-feature → coverage item → test → status）」，§9 已「**确定对齐**」。

**落地方案**：
- 新增原子变体 **`table.coverage_matrix`**：字段 `feature` / `sub_feature` / `coverage_item` / `test` / `status`；
- `verification_plan_format`（`ucis`|`vplan`|`native`）为 **`product` 子类型粒度**（`meta.doc_subtype == "verification-plan"` 时必填），`DocTypeRule` 的 doc_type 粒度表达不了 → 落在 **importer 映射层**（`doc_type_map.missing_verification_plan_meta`），**不进 `DOC_TYPE_RULES`**（实现裁决 2026-09-17）；
- **导入/导出**：`importer` 增 vPlan XML 解析（若语料可得）；无真实 vPlan 语料时，**仅实现导入器接口 + 用合成 XML 验证**。

> **验证边界**（重要）：UCIS/vPlan 的**真实语料当前不存在**于 `spec/standards/`。故本项的验收为「接口 + 合成样例通过」，**非真实端到端**。此边界必须显式记录。

## 5. 验证边界声明（如实标注）

**语料获取（2026-09-17，用户指示「部分真实语料可以从网络搜索获得」→ 已调研 + 下载）**：

已确认可下载的**公开/许可清晰**的真实语料（调研报告：实测 HTTP 状态码 + 许可核查）：

| doc_type | 获取的真实语料 | 来源 | 许可 |
|---|---|---|---|
| `standard` | ✅ 7 份（PCIe/CXL/JEDEC/AMBA） | 原有 | 已审核 |
| **`lang`** | ✅ Tcl man pages（`.n`，RefEntry 原型）+ OpenSTA `Commands.md`（283 命令节） | tcltk/tcl、parallaxsw/OpenSTA | BSD 式 / GPL-3.0 |
| **`tool-manual`** | ✅ Verilator 用户指南 + 诊断码表 | verilator/verilator | LGPL-3.0/Artistic-2.0 |
| **`product`** | ✅ OpenTitan testplan（`feature/test/stage/tests` + countermeasure 追溯 + register/bitfield）+ RISC-V ISA Manual（条款 + 位域表） | lowRISC/opentitan、riscv/riscv-isa-manual | Apache-2.0 / CC-BY-4.0 |
| **`safety`** | ✅ neqsim FMEA（RPN=S·O·D）+ protective-stop FMEDA + cdriscv FMEDA | equinor/neqsim 等 | Apache-2.0 |
| **UCIS** | ✅ pyucis UCIS XML fixtures（5 份）+ AMIQ fc4sc gold | fvutils/pyucis、amiq-consulting/fc4sc | Apache-2.0 |
| **vPlan XML** | ⚠️ **无许可清晰来源**（社区样本 `kei-seu/I2C` 仓库无 LICENSE） | — | **替代**：用 OpenTitan testplan 作 vPlan 结构的许可清晰替身 |

**验证边界（更新后）**：

| doc_type | 真实语料 | 可验证范围 |
|---|---|---|
| `standard` | ✅ | **端到端**（导入→存储→渲染→P4 逐字节） |
| `lang` / `tool-manual` / `product` / `safety` / UCIS | ✅ 已获取 | **端到端可达**（语料为原始格式：nroff/rst/hjson/adoc/md/xml，需 `importer` 支持或转换） |
| vPlan XML（专有格式） | ❌ 无许可源 | 导入器接口 + 合成 XML |

> **入库许可说明**：上述语料均为**开源许可**（BSD 式 / GPL-3.0 / LGPL-3.0 / Apache-2.0 / CC-BY-4.0），已附 LICENSE 文件于 `spec/standards/DOWNLOADED.md`。**GPL/LGPL 语料仅作测试 fixture，不派生作品**（测试用途，不修改、不链接）。
>
> **不得声称**：vPlan XML 的端到端验证（无许可语料）；其余类型语料已到位，但**格式转换完成前**只有 `safety`（md）可直接跑通，其余需转换器。

**格式转换需求（后续工作项）**：

| 目录 | 文件数 | 格式 | 转换需求 |
|---|---|---|---|
| `safety/` | 3 | `.md` | ✅ 无需转换（补 frontmatter 即可） |
| `ucis/` | 6 | `.xml` | ✅ 经 `importer/vplan.py`（UCIS 解析器已实现） |
| `lang/` | 21 | **nroff `.n`** | ⚠️ **需 nroff→markdown 转换器** |
| `lang/` | 1 | `.md` | ✅ 无需转换 |
| `tool-manual/` | 2 | **`.rst`** | ⚠️ **需 rst→markdown 转换器** |
| `product/` | 5 | **`.hjson`/`.adoc`** | ⚠️ **需转换器** |

**格式转换器不在本轮范围**：转换器本身是新工具（涉 nroff/rst/hjson/adoc 四种格式），且转换质量直接影响 P4 保真——应作为独立工作项评估（可参考 M03 的规则库模式）。**本轮的验证边界如实为**：`safety` 端到端可达；`ucis` 经解析器可达；其余三类「语料已获取但需转换」。

## 相关

- `../idea/idea.md` §4（分文档类型 Schema 建议）、§8（参考标准）
- `architecture_specification.md` §3.0/§3 M01/§4（DDL）
- `ADR-006`（结构化粒度与锚策略）
