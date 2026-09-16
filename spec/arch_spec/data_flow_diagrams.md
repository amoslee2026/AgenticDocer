---
title: 数据流向图 — 芯片设计知识库系统
type: composite
purpose: architecture
audience: llm
direction: input
status: approved
version: "1.2.0"
section_meta: "@meta"
---

# 数据流向图

生成：2026-09-16（it.arch Phase 4）。模块编号见 `architecture_specification.md` §2。

## DF-1 系统级数据流（导入到消费）

```mermaid
flowchart LR
    subgraph SRC["来源"]
        GR["GigaRAG 产物<br/>spec/standards/*.md<br/>(+ images/)"]
    end
    subgraph IN["导入（M03）"]
        P["解析器<br/>提议(rule_id)"] --> RV["CLI 审核器<br/>(阶段2: M07)"]
    end
    subgraph VAL["校验"]
        A9["M09A<br/>schema 校验"]
    end
    subgraph DB["权威源（M02/PG）"]
        N[("nodes/refs")] 
        E[("events 事件日志")]
        C[("comments")]
        S[("schemas/assets/terms")]
    end
    subgraph OUT["产出"]
        R["M04 渲染"] --> BR["build/rendered/<br/>(+assets/)"]
        EX["M-LR 导出包<br/>(渲染文本+node_id)"]
    end
    GR --> P
    RV --> A9 --> N
    A9 --> E
    N --> R
    N --> EX
    E -. "增量（C7 解禁后）" .-> EX
    EX -. "暂缓" .-> LR[("LightRAG")]
```

## DF-2 写入路径（Agent 结构化写）

```mermaid
sequenceDiagram
    participant A as Agent(M06)
    participant V as M09A
    participant S as M02(PG)
    participant R as M04
    A->>V: NodeIn + expected_version
    V-->>A: Violation[]（拒）
    V-->>S: 校验通过 → M02 开启事务
    S->>S: INSERT events（字段级 diff）
    S->>S: UPDATE nodes（version+1）
    S->>S: 事务提交
    S->>R: 触发文档重渲染
    R-->>S: RenderResult
    S-->>A: 结果 + 产物路径（经 M06 返回，L9）
```

## DF-3 评审路径（人类）

```mermaid
flowchart LR
    H["人类（M08）"] -->|读| W7["M07 API"]
    W7 -->|events payload| H
    H -->|批注/状态| W7 --> CM[("comments/status")] 
    CM --> EV[("events: comment/status")]
    EV --> HIST["历史视图（重放）"]
```

## DF-4 检索路径

```mermaid
flowchart LR
    Q["查询（ID/关键词/多跳）"] --> M5["M05"]
    M5 -->|点查| N2[("nodes")] 
    M5 -->|"递归 CTE（refs）"| R2[("refs")]
    M5 -->|"FTS（tsvector）"| N2
    M5 -->|"语义（联调后）"| LR2[("LightRAG")]
    N2 --> HIT["命中集<br/>node_id+证据链"]
    R2 --> HIT
    LR2 -->|node_id 回查| N2
```

## 数据驻留与边界

| 数据 | 位置 | 生命周期 |
|---|---|---|
| 权威内容（nodes/refs/events/comments/schemas/assets/terms） | PG `agenticdocer` | 永久（append-only 事件） |
| 渲染产物 | `build/rendered/` | 可重建（派生） |
| 导入快照（源 markdown） | `spec/standards/` | 只读（勿编辑；改版经 M03 重导入） |
| LightRAG 索引 | 现：`/home/lxx/lightrag/rag_storage`（JSON）；迁移后：同 PG 实例 `LIGHTRAG_*` 表 | 派生（可重建） |
