---
title: 执行摘要 — 芯片设计知识库系统（it.idea 完整模式）
type: composite
purpose: spec
audience: both
direction: input
status: approved
version: "1.1.0"
section_meta: "@meta"
---

# 执行摘要

生成：2026-09-16（it.idea 完整模式，AgenticDocer）。本摘要为 `design_doc.md` 的浓缩版；系统开发按本组文档推进，下一步 handoff → it.arch（架构规范）。

## 一句话

为芯片设计全流程文档建立**结构化 Schema 为唯一权威源**的知识库系统：agent 走结构化读写（格式合规由渲染层确定性保证），人类走 WebUI 评审（批注指向 node_id 不触正文），检索确定性引用图为主、LightRAG 语义为辅。

## 关键决策

| 决策 | 结论 | 依据 |
|---|---|---|
| 总体方案 | **方案 A：自研模块化单体**（Python/FastAPI + PG + React WebUI） | 加权 4.45 vs B 3.00 / C 3.25（trade_off_matrix.md） |
| 存储 | 纯 PostgreSQL 16.15 + JSONB，不引图库 | v0.1 §9 + 节点量级 ≤100k（B10 v1.1 实测校准） |
| LightRAG | 同实例**同库不同表**（`LIGHTRAG_*` 前缀）可行（源码核实）；**暂缓联调**（用户明令） | Q1 已解决；C7 |
| 导入方式 | 半自动：解析器提议 + 审核（不做全自动直转） | GigaRAG 原则 + B11 |
| 系统结构 | 9 模块 M01–M09 + M-LR 边界（模块化单体，≤10 模块） | design_doc §4 |

## 环境事实（本机 TeraFab，2026-09-16 实测）

| 项 | 事实 | 对设计的影响 |
|---|---|---|
| PG | **16.15**，Podman 容器 `pgvector/pgvector:pg16`，:5432 可达；现有库：mem0/vectest/gigapie_gigapie/gigapie_test | 直接复用，新建 `agenticdocer` 库（B2 ✓） |
| lightRAG | v1.5.6 运行中（JSON 文件模式，storage=/home/lxx/lightrag/rag_storage）；PG 后端能力存在（`kg/postgres_impl.py`） | 同库多表路径可行；迁移为后期配置变更（C7 暂缓） |
| Node/npm | v22.22.3 / 10.9.8 | WebUI（React+Vite）开发可行（B4 ✓） |
| Python | 系统 python3=3.6.8（过老）；**uv 0.12.7 + uv 管理 Python 3.11 可用**（lightrag 工具环境实证） | 后端一律 uv 管理 3.11+ 环境 |
| 磁盘 | `/mnt/big10T` **不存在**（AGENTS.md 首选落点不可用）；数据落 home 分区 | 运行数据落 /home（PG 容器卷 + 仓库内） |

## 交付阶段（依赖序）

1. **地基+闭环**：M01 内容模型（+M09A 校验引擎）→ M02 存储 → M03 导入解析 → M04 渲染 —— 里程碑：`spec/standards/` 7 份语料全链路往返测试（规则覆盖率 ≥95%，见 design_doc §10）
2. **人机接口**：M06 Agent 接口（lint 闭环）+ M07 API / M08 WebUI（契约先行，可并行）
3. **增值**：M05 多跳检索 → M09B 质量门 → M-LR 联调（解禁后）

## 测试语料（用户指令）

`spec/standards/` 7 份已审核行业规范 markdown（PCIe 5.0 / CXL 3.2 / HBM4 / AMBA×4，**实测 ≈8.8MB / 75,694 行**；表格为 HTML 标记、含 1,019 处图片引用〔实物在 GigaRAG〕）——解析→存储→渲染回归 fixture（B12）。**注意：不得向其 lightRAG 导入（C7）**。

## 已知风险

1. 解析器（M03）对 3.4MB 大文档的性能与正确性——半自动审核 + 分章增量 + 回归常态化
2. Q3 表单引擎 / Q4 节点粒度 / Q5 模板引擎 / Q6 doc_type 组合规则——it.arch 阶段 ADR 裁决
3. GigaRAG `ingest.sh` 默认 `LIGHTRAG_INPUT_DIR=/mnt/big10T/...` 与本机实际路径不符——恢复摄入前须以环境变量覆盖（已记录，C7 期间不触发）

## 状态

- it.idea（本组文档 v1.1.0）：**完成**——设计/方案/矩阵/澄清/摘要 + 对抗评审（20 项问题全部闭环，最终结论：无阻塞）
- 下一步：it.arch（架构规范：功能规格、架构规范、数据流/工作流图、ADR）
