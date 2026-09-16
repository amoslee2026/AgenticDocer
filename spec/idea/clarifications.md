---
title: 澄清与假设台账 — 芯片设计知识库系统（it.idea 完整模式）
type: composite
purpose: spec
audience: both
direction: input
status: approved
version: "1.0.0"
section_meta: "@meta"
---

# 澄清与假设台账 — 芯片设计知识库系统

生成：2026-09-16（it.idea 完整模式，auto_approve=true）。输入：`芯片设计知识库-结构化文档方案-v0.1.md`（idea 源）+ 用户指令（2026-09-16：所有 spec/idea 归档 `./spec`；暂不导入 GigaRAG 文档，先开发本系统，GigaRAG markdown 作测试语料）。

## 0. 与前一任务的边界

「集中所有 spec 到 spec 目录」为独立子任务（quick 模式，已执行完毕，见 `../..//docs/plans/2026-09-16-spec-central-directory.md` 与 `assumptions.md`）。本文件是**系统本体**（知识库软件）的澄清台账。

## 1. 澄清后的需求边界

**scope（范围内，S 编号）**：
| S | 能力 | 来源 |
|---|---|---|
| S1 | 结构化内容库：PG+JSONB 存内容原子与引用边 | v0.1 §3/§4 |
| S2 | append-only 变更事件日志（版本与结构化 diff） | v0.1 §3/§7 |
| S3 | 渲染层：schema → Markdown（首批）/HTML/PDF（按需） | v0.1 §3/§7 |
| S4 | Agent 结构化读写 + lint 自修复闭环 | v0.1 §5 |
| S5 | LightRAG 语义索引边界（渲染文本 + node_id） | v0.1 §6 |
| S6 | WebUI（MVP）：schema 表单/结构化 diff/批注/追溯/状态/版本历史 | v0.1 §5.1 |
| S7 | 测试语料就绪（`spec/standards/` 7 份 markdown 作 fixture） | 用户指令 |

**out of scope（范围锁定，v0.1 §5.1 明示不做）**：复杂可配置工作流引擎、多项目多层级组织管理、内置报表仪表盘、与外部 PLM/ALM 双向集成、全自动 PDF 直转。

**constraints（C 编号）**：
| C | 约束 |
|---|---|
| C1 | 格式合规由工具链确定性保证，不依赖 agent 自律（v0.1 §3 核心原则） |
| C2 | 稳定 ID：文件级 `SPEC-*` 起步；条款级 ID 在结构化建模引入（节点主键 + 章节锚 alias） |
| C3 | 批注独立存储、指向 node_id、不侵入正文 |
| C4 | 单机部署（systemd --user），无外部暴露 |
| C5 | mySkills 文档元数据规范为文档 frontmatter 基线（AGENTS.md 强制） |
| C6 | 不保留向后兼容（AGENTS.md）；无外部使用者期间直接演进 |
| C7 | **禁止向 lightRAG 导入任何 GigaRAG 文档**（用户明令；spec/README ⛔） |
| C8 | 复用既有资产：`spec/standards/`（语料）、`scripts/upgrade_frontmatter.py`（元数据先例）、本机 PG 实例 |

## 2. 假设台账（assumptions）

| # | 假设/模糊点 | 采用的默认 | 依据 | 影响 | 回退方式 |
|---|---|---|---|---|---|
| B1 | 系统落地形态 | 模块化单体：Python(FastAPI) 后端 + PG + React/TS WebUI；单机 systemd --user | v0.1 §7 + 知识库「单 Agent/中小项目→模块化单体」+ 本机运维惯例 | 架构按 M01–M09 单体多模块 | 模块边界清晰可拆 |
| B2 | PG 实例 | 复用本机现有 PG 实例，新建 database `agenticdocer`（与既有消费方隔离） | LocalServices.md（pgvector Podman :5432 运行中）；新实例运维成本高 | 连接参数配置化 | 可迁独立实例 |
| B3 | LightRAG 集成深度 | 首批仅定义边界接口（导出渲染文本+node_id、增量驱动）；**暂不联调摄入**（C7） | 用户指令 + v0.1 §6 | M-LightRAG 模块接口完整、实现后置 | 摄入恢复后按接口接入 |
| B4 | WebUI 前端栈 | React + TypeScript（+Vite）；表单引擎候选 RJSF/JSON Forms 或自研轻量，Phase 5 由 ADR 裁决 | v0.1 §5.1（借鉴 Sanity Studio 思路，不接其云） | M08 前端按 schema 驱动设计 | 引擎与 UI 分层可换 |
| B5 | 后端框架 | FastAPI + 异步（asyncpg/SQLAlchemy 2.x 异步） | 生态惯例；Agent 熟悉度高 | API 用 OpenAPI 契约描述 | 框架与接口解耦 |
| B6 | 单用户/无鉴权 | 绑 127.0.0.1，无登录；审计靠 git + 事件日志 | 单机单用户；v0.1 无鉴权需求 | 省略 authn/authz | 需要时加反代+OIDC |
| B7 | 首批文档类型 | 行业标准 spec（clause+规范性关键词+register 表+state_machine+source_ref） | v0.1 §9 试点 + C7（standards 7 份为语料） | 功能规格以该类型为主线 | 逐类型扩展 |
| B8 | 节点 ID 方案 | DB 主键 = UUIDv7；human alias = `<doc_id>#<章节锚>`；不使用全局 URN 注册表 | v0.1 §3 的 URN 对本机单库过早 | 引用边以 (uuid, alias) 表达 | 需要时升级注册表 |
| B9 | 渲染先导格式 | Markdown 先行（对 7 份语料做往返一致性测试）；HTML/PDF 后置 | v0.1 §7「按需」 | 模板引擎先 MD 模板 | 模板分层可加格式 |
| B10 | 性能/规模量化 | 单库 ≤10k 节点、≤200 份文档；PG 查询 P95 <200ms；单文档渲染 <3s；语义检索 P95 <5s | 保守默认（替代"适当/尽量"） | 无需分布式/缓存层 | 超限再评估 |
| B11 | 结构化录入 | 半自动：解析器提议 + 人工/agent 审核（不做全自动直转） | GigaRAG 原则「自动解析质量不可控」（其 README L5） | 需「提议-审核」工具链（M03） | 高置信段可批量自动通过 |
| B12 | 测试策略 | 语料回归：7 份 markdown 为 fixture，断言解析→存储→渲染往返保真（frontmatter/表格/条款标题） | 用户指令 | 测试计划以此为核心 | 增补合成 fixture |
| B13 | 与 GigaRAG 关系 | 只消费其产物（经 spec/ 移交），不反向写入 | spec/README 移交流程 | 集成边界=文件系统 | — |
| B14 | 实施顺序（依赖序） | M01 内容模型 → M02 存储 → M03 导入解析 → M04 渲染 → M06 Agent 接口 → M07/M08 WebUI → M05 检索 → M09 质量 → LightRAG 联调 | 数据依赖链（解析器是渲染/检索前提） | it.mas 按此序 | 渲染层与 M08 表单引擎可并行（同 schema 驱动） |
| B15 | 服务进程形态 | 两个 user 服务：`agenticdocer-api`（FastAPI，含渲染/lint）与静态前端（可由 API 直接托管）；PG 复用现有实例 | 简化运维（LocalServices 惯例） | 部署文档按此 | 可拆更多服务 |

## 3. 开放问题（open_questions，不阻塞）

| Q | 问题 | 现状 |
|---|---|---|
| Q1 | LightRAG PG 后端能否「同实例同库不同表」共存？ | **已解决**（本地源码证据 2026-09-16）：lightrag-hku 1.5.6 含 `kg/postgres_impl.py`、`kg/pgtable_impl.py`；表名 `LIGHTRAG_*`（含 workspace 列/索引），与业务表天然隔离，**支持同库多表共存** |
| Q2 | 本机 PG 实例现状（现有 database/凭据/容量）；node/npm 可用性 | **已解决**（2026-09-16 实测，本机 TeraFab）：PG **16.15**（Podman 容器 `pgvector/pgvector:pg16`，:5432 可达），现有库 mem0/vectest/gigapie_gigapie/gigapie_test → 新建 `agenticdocer` 库可行；node v22.22.3 / npm 10.9.8 可用；uv 0.12.7 + Python 3.11 可用（系统 python3=3.6.8 过老）；**/mnt/big10T 不存在**（数据落 home）；lightRAG v1.5.6 运行中（JSON 文件模式） |
| Q3 | 表单引擎选型（RJSF/JSON Forms/自研） | Phase 5 ADR |
| Q4 | 结构化粒度（条款 vs 段落为最小节点） | 试点裁决，ADR 记录 |
| Q5 | 渲染模板引擎（Jinja2 vs 程序化生成） | Phase 5 ADR |
