---
title: it.arch Phase 1 澄清与假设台账 — 芯片设计知识库系统
type: composite
purpose: spec
audience: both
direction: input
status: approved
version: "1.0.0"
section_meta: "@meta"
---

# Phase 1 澄清与假设台账

生成：2026-09-16（auto 模式，auto_approve=true）。输入：`spec/idea/芯片设计知识库-结构化文档方案-v0.1.md`（下称 v0.1）+ 用户指令（2026-09-16：所有 spec/idea 归档 `./spec`；**暂不导入 GigaRAG 文档，先开发本系统，GigaRAG markdown 作测试语料**）。

## 1. 澄清后的需求边界（clarified_requirements）

**scope（范围内）**：
- S1 结构化内容库：PostgreSQL + JSONB 存内容原子（requirement/clause、definition、table〔+register-field 变体〕、figure〔+state_machine〕、code block、example、note、cross-reference），引用边（`traces_to`）为关系表（v0.1 §3/§4.4）
- S2 append-only 变更事件日志：版本与结构化 diff（v0.1 §3/§7）
- S3 渲染层：schema-type → 模板映射，产出 Markdown（首批）/HTML/PDF（按需）（v0.1 §3/§7）
- S4 Agent 结构化读写接口：function calling / JSON Schema 约束的结构化生成与修改 + lint 自修复闭环（v0.1 §5）
- S5 语义索引集成：LightRAG（渲染文本 + node_id metadata，增量索引）（v0.1 §6）
- S6 WebUI（MVP）：schema 驱动表单、结构化 diff、批注（指向 node_id）、追溯关系表格、状态流转、版本历史（v0.1 §5.1）
- S7 测试语料就绪：`spec/standards/` 7 份行业规范 markdown 作为首批系统测试输入（用户指令）

**constraints（约束）**：
- C1 格式合规由工具链确定性保证（渲染层），不依赖 agent 自律（v0.1 §3 核心原则）
- C2 引用为稳定 ID（URN 风格文件级 `SPEC-*` 起步，条款级 ID 在结构化建模时引入）
- C3 批注独立存储、指向 node_id、不侵入正文（v0.1 §3/§5）
- C4 单机部署（本机 user mode 服务），无外部暴露需求
- C5 mySkills 文档元数据规范（`~/wrk/mySkills/docs/meta-fields-reference.md`）为文档 frontmatter 基线（AGENTS.md 强制）
- C6 不保留向后兼容（AGENTS.md）；无外部使用者期间直接演进
- C7 **禁止向 lightRAG 导入任何 GigaRAG 文档**（用户明令；摄入能力已就绪但暂缓，见 spec/README ⛔）
- C8 现有资产复用：`spec/standards/`（语料）、`spec/idea/`（设计输入）、`scripts/upgrade_frontmatter.py`（元数据模式先例）

**tech_preferences（技术倾向，待 ADR 裁决）**：
- T1 存储：纯 PostgreSQL（JSONB）+ 关系表；不引入独立图数据库（v0.1 §9 已定）
- T2 语义检索：LightRAG（同 PG 实例，同库不同表）（v0.1 §6）
- T3 评审工具：自研 WebUI，不采购商业 CCMS（v0.1 §9 已定）
- T4 verification plan 结构对齐 UCIS/vPlan（v0.1 §9 已定；适用时）
- T5 语言/框架：Python 后端（adaptive 检测 + 现有脚本生态）；WebUI 前端与表单引擎选型待 ADR

**明确不做（范围锁定，v0.1 §5.1）**：复杂可配置工作流引擎、多项目多层级组织管理、内置报表仪表盘、与外部 PLM/ALM 双向集成。

## 2. 假设台账（assumptions）

| # | 假设/模糊点 | 采用的默认 | 依据 | 影响 | 回退方式 |
|---|---|---|---|---|---|
| B1 | 系统落地形态 | 单体服务：Python 后端（API + 渲染 + lint）+ PG + 自研 WebUI；单机 systemd --user 部署 | v0.1 §7 + 本机运维惯例（LocalServices.md） | 架构文档按单体多模块设计（M00X 模块划分） | 模块化接口可后续拆分 |
| B2 | PG 实例复用 | 复用本机现有 PostgreSQL 实例（新 database `agenticdocer`）；不新建实例 | 本机已有 pgvector(Podman):5432 运行中；新实例运维成本高 | LightRAG 若也走 PG 后端则同实例不同 database/schema——**与 v0.1「同库不同表」表述有出入，待 Phase 2 核实后裁决（开放问题 Q1）** | 可迁移至独立实例（连接串配置化） |
| B3 | LightRAG 集成深度 | 首批仅做「结构化 DB 为权威源 + 渲染文本可导出喂 LightRAG」的**边界设计**；实际联调等系统开发完成后（用户明令暂缓摄入） | 用户指令 C7 + v0.1 §6 | 架构中 LightRAG 为独立模块 M0XX，接口定义完整但实现可后置 | 摄入恢复后按接口接入 |
| B4 | WebUI 前端技术栈 | React + TypeScript（借鉴 Sanity Studio「schema → 自动生成编辑表单」的思路，自研渲染引擎，不接入其云服务） | v0.1 §5.1 明示借鉴该模式 | 前端模块与表单引擎设计按其语义 | 引擎与 UI 分层，可换框架 |
| B5 | 后端框架 | FastAPI（Python 生态默认，异步友好，OpenAPI 原生） | 生态惯例；无颠覆性理由不选更重框架 | API 契约用 OpenAPI 描述 | 接口定义与框架解耦 |
| B6 | 单用户/无鉴权 | WebUI 与 API 绑定 127.0.0.1，无登录体系；写操作审计靠 git + append-only 事件日志 | 单机单用户场景（LocalServices 惯例）；v0.1 无鉴权需求 | 架构省略 authn/authz 模块 | 需要时加反代 + OIDC |
| B7 | 首批文档类型 | 结构化建模从「行业标准 spec」（standards/ 7 份）起步：clause + 规范性关键词 + register 表 + state_machine + source_ref | v0.1 §9 试点范围 + 用户指令（GigaRAG markdown 作测试） | 功能规格以该类型为主线，其余类型（语法手册/内部 spec）schema 预留 | 逐类型扩展 |
| B8 | 条款级 ID 方案 | 条款 ID = `SPEC-*`（文件级）+ 章节路径锚（如 `§11.2.3`）+ 内容哈希消歧；不引入完整 URN 注册表 | 复杂 URN 体系（v0.1 §3 提及）对本机单库场景过早 | 引用边（traces_to）以「文件级 ID + 章节锚」表达 | 需要时升级为全局注册表 |
| B9 | 渲染先导格式 | Markdown（复用已审核 markdown 语料做对照测试）；HTML/PDF 后置 | v0.1 §7「Markdown/HTML/PDF（按需）」 | 渲染模板与一致性测试先针对 Markdown 往返 | 模板引擎分层，格式后加 |
| B10 | 性能/规模量化目标 | 单库 ≤10k 内容节点、≤200 份 spec；检索（PG 查询）P95 <200ms；渲染单文档 <3s；LightRAG 检索 P95 <5s | v0.1 未量化（保守默认，替代「适当/尽量」） | 架构无需分布式/缓存层 | 超限再评估 |
| B11 | 结构化录入方式 | markdown 语料**半自动**转结构化（解析器提议 + 人工/agent 审核修正），不做全自动直转 | GigaRAG 核心原则「自动解析质量不可控」（README L5）；v0.1 §5 agent 结构化生成框架 | 需「转换/提议-审核/确认」工具链（新增模块） | 高置信解析段可批量自动通过 |
| B12 | 测试策略 | 语料回归：以 `spec/standards/` 7 份 markdown 为 fixture，断言「解析→存储→渲染」往返一致性（frontmatter/表格/条款标题保真） | 用户指令（GigaRAG markdown 做测试） | 测试计划（it.test-plan 阶段）以此为核心场景 | 增补合成 fixture |
| B13 | 与 GigaRAG 的关系 | GigaRAG 保持转换/审核流水线；本系统**只消费**其产物（经 spec/ 移交）；不反向写入 | 既有分工（spec/README 移交流程） | 集成边界清晰：文件系统（spec/）+ 未来可选 PG 同实例 | — |
| B14 | 交付顺序（实施顺序，非工期） | 依赖序：M 内容模型/DB schema → 解析与导入（含审核工具链）→ 渲染 → agent 读写接口 + lint → WebUI → LightRAG 边界联调 | 数据依赖链（B11 的解析器是渲染/检索的前提） | it.mas 按此顺序生成模块规格 | 可并行：渲染层与 WebUI 表单引擎（同 schema 驱动，接口先定） |

## 3. 开放问题（open_questions，不阻塞 auto 推进）

- **Q1**：LightRAG 的 PG 后端能否「同实例同库不同表」与结构化内容库共存？（B2 待核实；Phase 2 调研项。若不能，则退化为「同实例不同 database」或「不同实例」，ADR 记录）
- **Q2**：pgvector(Podman):5432 实例的现有用途与容量（是否有其他消费方；能否加 database）——Phase 2 本地探查。
- **Q3**：WebUI 表单引擎自研工作量 vs 借鉴方向的取舍（React 生态中 RJSF/JSON Forms 等成熟库 vs 自研）——Phase 5 ADR。
- **Q4**：结构化节点粒度（条款为最小节点 vs 段落级）——随 B7 首批类型试点裁决，ADR 记录。
