---
title: ADR-002 纯 PostgreSQL 存储与 LightRAG 同库共存
type: composite
purpose: adr
audience: both
direction: input
status: approved
version: "1.1.0"
section_meta: "@meta"
---

# ADR-002: 纯 PostgreSQL 存储 + LightRAG 同实例同库不同表

## Status
Accepted（2026-09-16）

## Context
- 内容模型：≤10^5 节点（B10 v1.1）、8 表（含 JSONB 内容与引用边）+ append-only 事件日志。
- 检索需确定性引用图（多跳 ≤2 跳）与未来语义检索（LightRAG）。
- 本机已有 PG 16.15 实例（Podman `pgvector/pgvector:pg16`：mem0/vectest/gigapie_* 在用）。

## Decision
1. 全部结构化数据入**纯 PostgreSQL**（新建 database `agenticdocer`），不引入图数据库。
2. LightRAG 未来**同实例同库不同表**共存（其表名 `LIGHTRAG_*`，按 `workspace` 列隔离——源码核实，Q1）；联调暂缓（C7）。

## Trade-offs
| 维度 | 纯 PG（采用） | PG + Neo4j | 独立 LightRAG 实例 |
|---|---|---|---|
| 基础设施面 | 1 个实例 | 2+ | 2 实例 |
| 多跳查询 | 递归 CTE（≤2 跳，够用） | 图查询更强 | — |
| 共存风险 | 表名空间隔离（前缀） | — | 无 |
| 迁移成本（LightRAG JSON→PG） | 一次性配置变更 | 同左 | 无（维持 JSON） |

## Consequences
- Positive：备份/运维单点（pg_dump）；事务一致性覆盖事件+实体（P2）。
- Negative：图查询能力受 SQL 限制（超 2 跳/复杂图算法需重评估）。
- Risks：LightRAG 大表与业务表同库的容量/清理（`workspace` 隔离 + 独立 schema 评估留待联调）。

## Alternatives Considered
| 方案 | 优点 | 缺点 | 放弃理由 |
|---|---|---|---|
| 图数据库（Neo4j 等） | 原生图遍历 | 新基础设施；数据双写一致性 | ≤100k 节点、≤2 跳，SQL 足够（v0.1 §9 已否决） |
| 独立 LightRAG 实例（保持 JSON） | 无迁移 | 语义索引与权威源脱节风险 | Q1 已证同库可行；联调前置条件已列 |
