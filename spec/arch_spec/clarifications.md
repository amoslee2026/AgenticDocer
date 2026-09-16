---
title: it.arch Phase 1 澄清（v1.1 更新）— 架构级输入确认
type: composite
purpose: spec
audience: both
direction: input
status: approved
version: "1.1.0"
section_meta: "@meta"
---

# it.arch Phase 1 澄清（v1.1 更新）

> 更新：2026-09-16。此前版本基于 v0.1 草案直接推进（已按用户指示暂停）；现 it.idea 完整模式已交付并通过对抗评审（**无阻塞**），本文件切换为**以 finalized idea 文档为权威输入**。

## 0. 输入基线（权威）

| 输入 | 路径 | 说明 |
|---|---|---|
| 设计文档 v1.1.0 | `../idea/design_doc.md` | 系统设计（M01–M09 + M-LR、数据模型、流程、边界、测试判据、实施顺序） |
| 方案分析 v1.1.0 | `../idea/approach_analysis.md` | 方案 A 选定（加权 4.45/3.00/3.25） |
| 决策矩阵 v1.1.0 | `../idea/trade_off_matrix.md` | D1–D8 倾向 + 否决清单 |
| 澄清台账 v1.1.0 | `../idea/clarifications.md` | S/C/B/Q 全量（B1–B16、Q1–Q6；Q1/Q2 已解决） |
| 执行摘要 v1.1.0 | `../idea/summary.md` | 浓缩版 |
| 源方案 v0.1 | `../idea/芯片设计知识库-结构化文档方案-v0.1.md` | 立项文本 |
| 评审记录 | `../idea/.review/issues.md` | 20 项问题全部闭环（E1–E20 + N1–N8） |

**继承约束（不变）**：C1–C8（idea/clarifications §1），特别是 C7（**禁止向 lightRAG 导入 GigaRAG 文档**）与「所有 spec/idea 归档 ./spec」。

## 1. 本阶段（it.arch）需产出的架构级决策

| 编号 | 事项 | 产出 |
|---|---|---|
| A-D1 | 模块接口契约（M01–M09 + M-LR 的 API/函数级签名与数据类型） | architecture_specification.md |
| A-D2 | 数据库 DDL（docs/nodes/refs/events/comments/schemas/assets/terms 共 8 表）与索引 | architecture_specification.md |
| A-D3 | 表单引擎选型（Q3：RJSF / JSON Forms / 轻量自研） | ADR |
| A-D4 | 渲染模板引擎选型（Q5：Jinja2 vs 程序化） | ADR |
| A-D5 | 关键词检索实现（FTS english vs pg_trgm；索引策略） | ADR |
| A-D6 | 节点粒度最终裁决（Q4：条款级基线确认） | ADR |
| A-D7 | CLI 审核器命令面（阶段 1 交付物）接口定义 | architecture_specification.md |
| A-D8 | 部署单元与端口（agenticdocer-api 监听端口、前端托管方式） | architecture_specification.md |

## 2. 环境事实（已实测，继承 idea/clarifications Q2）

- PG 16.15（Podman `pgvector/pgvector:pg16`，:5432）→ 新建 database `agenticdocer`
- lightRAG v1.5.6 运行中（JSON 文件模式；PG 后端代码存在，迁移为后期配置变更）
- node v22.22.3 / npm 10.9.8；uv 0.12.7（Python 3.11）；系统 python3=3.6.8（不可用）
- `/mnt/big10T` 不存在（数据落 home）；本机主机名 TeraFab
- 语料：`spec/standards/` 7 份（8.8MB / 75,694 行，HTML 表格、1,019 图片引用）

## 3. 架构级假设（补充 idea 层，B 系列延续）

| # | 假设 | 默认 | 回退 |
|---|---|---|---|
| AB1 | API 端口 | `agenticdocer-api` 监听 `127.0.0.1:8787`（不与现有服务冲突：9621/8090/7474/5432 已占） | 端口配置化 |
| AB2 | 前端托管 | 构建产物由 FastAPI 静态挂载（单进程交付；开发期 Vite devserver 反代） | 独立静态服务 |
| AB3 | 测试数据库 | 同实例 `agenticdocer_test` 库（pytest 集成用例专用，可重建） | 容器内临时库 |
| AB4 | 迁移工具 | Alembic（SQLAlchemy 配套）管理 DDL 版本 | 手写 SQL 脚本目录 |
| AB5 | 包结构 | 单包 `src/agenticdocer/`（模块目录与 M 编号对应，Agent-friendly） | 拆分发包（无必要） |
