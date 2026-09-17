---
title: spec 目录规范
type: composite
purpose: spec
audience: both
direction: input
status: approved
version: "1.0.0"
section_meta: "@meta"
---

# spec/ — 芯片设计知识库 spec 集中目录

本仓库（AgenticSpec）是芯片设计知识库的 **spec 权威源**；`spec/` 是所有 spec 文档与 idea 文档的唯一集中存放点。设计依据：`idea/芯片设计知识库-结构化文档方案-v0.1.md`（下称 v0.1 方案；自 `Notes/idea/` 归位）。

## 目录分类（对齐 v0.1 §1 文档类型）

| 子目录 | 内容 | 状态 |
|---|---|---|
| `standards/<org>/` | 标准组织正式规范：PCIe/AMBA/CXL/JEDEC/UCIe/IEEE 1800 LRM/RISC ISA 等 | 已建（首批 7 份） |
| `lang/` | 语言/脚本语法手册：EDA 厂商 TCL 方言命令参考、工具语法手册等非标准组织出版物 | 定义即建（首份文档移交时创建） |
| `product/` | 内部产品 spec：PRD/架构 spec/MAS/接口规格等 | 同上 |
| `safety/` | 功能安全分析：FMEA/FTA/认证合规 | 同上 |
| `idea/` | idea 文档：立项方案、假设记录（assumptions）、对抗评审记录（.review）；it-idea 产物默认落此目录 | 已建（首批：v0.1 方案、本计划假设与评审记录） |

边界细则（假设 A12）：标准组织（PCI-SIG/ARM/JEDEC/CXL/UCIe/IEEE/RISC-V International）发布的正式规范入 `standards/`；EDA 厂商的语法参考/教程手册入 `lang/`。

## 命名规范

- 文件名保持来源惯例（如 `IHI0022K_AMBA_AXI_ACE_protocol_spec.md`）；新增文档建议 `<来源编号或协议名>.md`
- **basename 全局唯一**（硬约束：ingest.sh 按 basename 与 lightRAG 核对结果）
- 文件级稳定 ID：`SPEC-<类>-<名称>-<版本>`，登记于 frontmatter `spec_id` 与 `INDEX.md`

## frontmatter 规范（v2）

mySkills 文档元数据（AGENTS.md 强制）+ spec 专属字段 + GigaRAG 流水线溯源字段：

```yaml
---
# --- mySkills 文档元数据（必填）---
title: PCI Express Base Specification Revision 5.0 Version 1.0
type: composite            # 固定
purpose: spec              # 固定
audience: both
direction: input           # 知识库供 LLM 检索消费
status: approved           # approved=审核通过采信；review=已迁移但缺 reviewed_by；draft=转换完成未审核（不应出现在 spec/）
version: "1.0.0"           # 本仓库元数据版本（非规范版本）
section_meta: "@meta"      # 固定
# --- spec 专属字段（必填）---
spec_id: SPEC-STD-PCIE-5.0
spec_type: standard        # standard | lang | tool-manual | product | safety
spec_org: PCI-SIG          # 制定组织
spec_revision: "5.0 v1.0"  # 原始规范版本号
# --- 流水线溯源（GigaRAG 移交时必须已存在）---
source: corpus/01_raw/specifications/pcie/PCI_Express_Base_Specification_Revision_5.0.pdf
converted_by: mineru
converted_at: 2026-08-31
reviewed_by: lxx
reviewed_at: 2026-08-31
# --- 导入标记（ingest.sh 幂等追加，勿手工写）---
ingested_at: 2026-09-16
---
```

| 字段 | 必填 | 说明 |
|---|---|---|
| mySkills 八项（title/type/purpose/audience/direction/status/version/section_meta） | 是 | 见 `~/wrk/mySkills/docs/meta-fields-reference.md` §1 |
| spec_id / spec_type / spec_org / spec_revision | 是 | 参考 v0.1 §4.4 公共字段（id/version/status/source_ref）的文件级落地，spec_type/spec_org 为本目录新增扩展；条款级 URN 属后续结构化 DB（超本阶段范围） |
| source / converted_by / converted_at / reviewed_by / reviewed_at | 是 | GigaRAG 移交前置条件；`source` 指向 GigaRAG `corpus/01_raw/` 原始 PDF（假设 A4） |
| ingested_at | 导入后由脚本追加 | LightRAG 导入标记（幂等） |

## 移交流程（GigaRAG → spec/）

1. GigaRAG 内完成人工转换（`02_converted/`）与人工审核（`03_reviewed/`）——GigaRAG 工作流不变
2. GigaRAG 留底：`git -C ~/wrk/GigaRAG add corpus/03_reviewed && git -C ~/wrk/GigaRAG commit -m "chore(corpus): reviewed 留底（移交前存档）"`
3. `mv` 至 `spec/standards/<org>/`（org = 小写组织名：pcie/amba/cxl/jedec/ucie/ieee/…）
4. 补全 frontmatter v2 字段：`uv run --no-project python3 scripts/upgrade_frontmatter.py spec/standards/<org>/<file>.md`（脚本幂等；新文档需先在脚本 `REGISTRY` 登记三专属字段）
5. `spec/INDEX.md` 表 1 登记
6. `git add spec/ scripts/ && git commit`

## 与 LightRAG 的关系

> **⛔ 摄入暂缓（用户指令 2026-09-16）**：在 AgenticSpec 系统开发完成前**不执行任何 lightRAG 摄入**；`standards/` 下的 markdown 先作为新系统的**测试语料**。下方命令为系统就绪后的参考路径，当前禁止执行。

- 摄入：`SPEC_SRC_DIR=$HOME/wrk/AgenticSpec/spec/standards KEEP_IN_PLACE=1 ~/wrk/GigaRAG/scripts/ingest.sh`（递归扫描；已带 `ingested_at` 的文件自动跳过防重复入库；`DRY_RUN=1` 仅列出待导入）
- **权威文件导入后不移动**：`KEEP_IN_PLACE=1` 时成功件原地追加 `ingested_at`；失败件保留原处
- 职责划分见 v0.1 §6：本目录=确定性权威源；LightRAG=渲染文本的语义索引，滞后无害
