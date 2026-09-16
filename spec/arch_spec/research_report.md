---
title: 调研报告 — 芯片设计知识库系统（it.arch Phase 2）
type: narrative
purpose: research
audience: llm
direction: input
status: approved
version: "1.1.0"
section_meta: "@meta"
---

# 调研报告（Phase 2）

生成：2026-09-16。**降级声明 ⚠️**：本机外网受限（国际站点经代理不稳），并行调研代理不可用；本报告以**本机实测 + 本地源码证据 + 少量 web 检索**构成，未运行完整 it.deepresearch 流程。

## 1. 关键事实（实测/源码级）

### 1.1 LightRAG 存储后端（Q1）
| 事实 | 证据 |
|---|---|
| lightrag-hku **1.5.6** 已安装（uv tool） | `/home/lxx/.local/share/uv/tools/lightrag-hku/lib/python3.11/site-packages/lightrag/` |
| PG 后端实现存在 | `kg/postgres_impl.py`（408KB）、`kg/pgtable_impl.py`（70KB） |
| 表名 `LIGHTRAG_*` 且按 `workspace` 列/索引隔离 | `postgres_impl.py`：`INSERT INTO LIGHTRAG_VDB_CHUNKS (… workspace …)`、`idx_lightrag_doc_status_workspace_content_hash` |
| 存储后端可配置 | `kg/__init__.py` `STORAGE_IMPLEMENTATIONS`：KV/GRAPH/VECTOR/DOC_STATUS 四类实现清单 |
| 当前运行形态 = **JSON 文件模式** | 进程参数 `--working-dir /home/lxx/lightrag/rag_storage --input-dir /home/lxx/lightrag/inputs`；`.env` 无 `*_STORAGE` 键 |
| 官方定位 | PostgreSQL 为推荐生产后端（"four storage roles with pgvector and AGE"，web 检索佐证） |

**结论**：同实例同库多表共存可行（前缀隔离）；迁移为后期配置变更（C7 暂缓）。

### 1.2 运行环境（Q2，本机 TeraFab 实测）
| 项 | 事实 |
|---|---|
| PG | **16.15**，Podman 容器 `pgvector/pgvector:pg16`，`0.0.0.0:5432` 可达；现有库：postgres / mem0 / vectest / gigapie_gigapie / gigapie_test |
| Node/npm | v22.22.3 / 10.9.8（WebUI 可行） |
| Python | 系统 3.6.8（不可用）；uv 0.12.7 + uv 管理 3.11（lightrag 环境实证可用） |
| 磁盘 | `/mnt/big10T` **不存在**；数据落 home 分区 |
| 端口占用 | 9621（lightRAG）、8090（GigaPie 控制面）、7474/7687（Neo4j）、5432（PG）→ 新服务避开 |

### 1.3 测试语料实测（spec/standards/ 7 份）
| 指标 | 值 |
|---|---|
| 体积/行数 | 8,812,225 B ≈ **8.8MB** / 75,694 行（最大单文件 CXL 3,594,622 B / 31,072 行） |
| 标题行 | 5,954 |
| 表格形态 | **100% HTML 标记**：`<table>` 2,440 / `<tr>` 19,763 / `<td>` 79,817；57,005 单元格带 `colspan/rowspan/bgcolor/align` |
| 内联标记 | `<sup>/<br>` 等 ≥239 行 |
| 图片引用 | md 形式 `images/<sha256>.jpg` × 1,019 + HTML `<img>` × 80（合计 **1,099**）；实物在 GigaRAG `corpus/02_converted/specifications/*/auto/images/` |
| 标题重复 | CXL「Test Steps:」×219、「Fail Conditions:」×217、「Pass Criteria:」×214；PCIe「IMPLEMENTATION NOTE」×154；HBM4「Wrapper Data Register」×21；无编号标题存在（AMBA「Chapter A2」「Part C Glossary」） |

**对设计的直接影响**：催生 v1.1 的 E1（HTML 直通策略）、E2（资产模型）、E7（稳定锚）修订（已内化于 `../idea/design_doc.md`）。

### 1.4 生态与先例（web 检索 + v0.1 既有引用）
| 先例 | 采纳点 |
|---|---|
| docs-as-code 集中式 docs repo 拓扑 | 中央权威源（本仓库 spec/）+ 项目内工作文档（引用登记）— 与本项目分工一致 |
| StrictDoc / Doorstop（Git-based 需求工具） | 字段设计参考（v0.1 §9 已引）；本设计未采用其格式（模型不匹配异构文档） |
| Sanity 的 Portable Text / schema→表单 | WebUI 表单引擎设计思路（M08）；不接其云服务（v0.1 §5.1） |
| RFC2119 规范性关键词 | `terms` 表（normative-keyword）与条款标注（v0.1 §4.2） |
| Accellera UCIS / vPlan | verification 类型延后落地（idea/design §2 延后声明） |

## 2. 技术选型评估（Agent-aware 知识库框架）

| 候选 | Agent 熟悉度 | 类型系统 | 文档 | 评级 |
|---|---|---|---|---|
| Python 3.11 + FastAPI + SQLAlchemy 2.x | ★★★★★ | 类型提示 + pydantic | 完善 | **采用** |
| PostgreSQL 16 + JSONB | ★★★★★ | SQL DDL + 类型 | 完善 | **采用** |
| React + TS + Vite | ★★★★★ | 强类型 | 完善 | **采用** |
| Jest/Vitest + pytest | ★★★★★ | — | 完善 | **采用** |
| 图数据库（Neo4j 等） | ★★★ | — | 完善 | 否决（≤100k 节点，PG 足够；v0.1 §9） |
| strictdoc 作为承载 | ★★★★ | 弱（自有格式） | 完善 | 否决（异构文档建模受限） |

## 3. 风险修正（相对 idea 层）

| 项 | 调研结论 |
|---|---|
| Q1 同库多表 | ✅ 源码级可行，风险清零；剩余风险 = JSON→PG 迁移策略（列为联调前置） |
| Q2 环境 | ✅ 全部可用（node/uv/PG16.15）；新增事实：/mnt/big10T 缺失（落点改 home） |
| 解析器难度 | ⚠️ 实测确认 HTML 表格/图片/重复标题为三大难点 → v1.1 已给出对策（直通/资产/哈希锚） |
| 外网依赖 | ⚠️ 国际访问不稳；一切交付不依赖外网（本地栈全就绪） |
