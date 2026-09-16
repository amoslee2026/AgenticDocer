---
title: ADR-001 模块化单体与内部 OpenAPI 契约
type: composite
purpose: adr
audience: both
direction: input
status: approved
version: "1.1.0"
section_meta: "@meta"
---

# ADR-001: 模块化单体 + 内部 OpenAPI 契约

## Status
Accepted（2026-09-16）

## Context
系统为单机单用户知识库（C4/B6），9 个功能模块 + 1 个集成边界；需支持 coding agent 与人类并行开发（WebUI 前端可独立工作流）。

## Decision
采用**模块化单体**：单 Python 包 `src/agenticdocer/`（M01–M09 目录对应）+ React 前端 `webui/`；前后端以 **OpenAPI 契约**（FastAPI 自动生成）为边界；服务以单进程 `agenticdocer-api` 交付（前端静态挂载）。

## Trade-offs
| 维度 | 模块化单体（采用） | 微服务 | 纯单体（无契约边界） |
|---|---|---|---|
| 运维复杂度 | 低（单进程） | 高（N 服务） | 最低 |
| 前后端并行 | 契约先行可行 | 天然 | 差（耦合） |
| Agent 上下文 | 单仓库连贯 | 跨仓库分散 | 单仓库 |
| 拆分空间 | 模块边界清晰，可后拆 | — | 差 |

## Consequences
- Positive：开发/部署/调试单点；契约测试可验证（REQ-M07-F01..F05）；Agent 按 M 编号顺序实现。
- Negative：单进程承载全部流量（规模 ≤10^5 节点，无压力）。
- Risks：契约漂移 → 以 OpenAPI 快照测试缓解。

## Alternatives Considered
| 方案 | 优点 | 缺点 | 放弃理由 |
|---|---|---|---|
| 微服务拆分 | 独立伸缩 | 运维与调试成本（单机场景无收益） | C4/B6 单机单用户 |
| 前后端同仓不设契约 | 最快起步 | 前端阻塞于后端实现细节 | 破坏并行开发 |
