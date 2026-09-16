---
title: spec 登记索引
type: composite
purpose: readme
audience: both
direction: input
status: approved
version: "1.0.0"
section_meta: "@meta"
---

# spec 登记索引

`spec/` 内容的两张登记表：表 1 = 物理集中的权威文档；表 2 = 活跃项目工程 spec 的引用登记（不迁移，归档时晋升为表 1 条目）。

## 表 1：物理集中文档（7）

| spec_id | 路径（相对 spec/） | spec_type | spec_org | 规范版本 | status | 原始来源（GigaRAG） |
|---|---|---|---|---|---|---|
| SPEC-STD-PCIE-5.0 | standards/pcie/PCI_Express_Base_Specification_Revision_5.0.md | standard | PCI-SIG | 5.0 v1.0 | approved | corpus/01_raw/specifications/pcie/ |
| SPEC-STD-CXL-3.2 | standards/cxl/CXL_Specification_rev3p2_ver1p0.md | standard | CXL Consortium | r3.2 v1.0 | approved | corpus/01_raw/specifications/cxl/ |
| SPEC-STD-HBM4-JESD270-4A | standards/jedec/JEDEC_JESD270-4A_HBM4_2025.md | standard | JEDEC | JESD270-4A | approved | corpus/01_raw/specifications/hbm/ |
| SPEC-STD-AMBA-AHB-C | standards/amba/IHI0033C_AMBA_AHB_spec.md | standard | ARM | IHI0033C | approved | corpus/01_raw/specifications/amba/ |
| SPEC-STD-AMBA-AHB-LITE-B | standards/amba/IHI0033B_AMBA5_AHB_AHB-Lite_spec.md | standard | ARM | IHI0033B | approved | corpus/01_raw/specifications/amba/ |
| SPEC-STD-AMBA-APB | standards/amba/IHI0024_AMBA_APB_spec.md | standard | ARM | IHI0024 | approved | corpus/01_raw/specifications/amba/ |
| SPEC-STD-AMBA-AXI-K | standards/amba/IHI0022K_AMBA_AXI_ACE_protocol_spec.md | standard | ARM | IHI0022K | approved | corpus/01_raw/specifications/amba/ |

> 原始来源子目录名以各文件 frontmatter `source` 字段为准（迁移时原样保留，不作猜测改写）。

## 表 2：外部工程 spec 引用登记（3）

| 引用 ID | 项目路径 | 内容 | 类型 | 项目状态 |
|---|---|---|---|---|
| REF-GIGAPIE-SPEC | ~/wrk/GigaPie/spec/ | 工程流水线 spec：arch_spec/ impl_spec/ test_plan/ checklist/ | product | active |
| REF-ARION-PRD | ~/wrk/Arion/spec/PRD/ | 芯片 PRD：Arion_IODie_PRD.md、IO扩展芯粒整体设计方案（2 个 md 版本，另 docx/drawio 源件） | product | active |
| REF-NOVA-ARCHEXPLORER | ~/wrk/nova2026/archExplorer/spec/ | 芯片设计模拟器 spec（含 archive/ 归档） | product | active |

## 维护规则

- 新增物理集中文档：先 `spec/README.md` 移交流程，后本表 1 加行
- 引用晋升：项目归档时把表 2 行 mv 入 spec/ 并改写为表 1 行（棘轮单向，不降级）
