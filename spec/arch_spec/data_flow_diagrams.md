---
title: 数据流向图 — 芯片设计知识库系统
type: composite
purpose: architecture
audience: llm
direction: input
status: approved
version: "1.3.0"
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

## DF-4 检索路径（v1.3 收窄：B5/B8）

```mermaid
flowchart LR
    AQ["agent 查询"] --> LR["LightRAG<br/>（语义检索主入口）"]
    LR -->|导出包：渲染文本+node_id| MLR["M-LR 导出"]
    MLR -->|内部调用 refs 图结构| M5["M05（内部）"]
    M5 --> R2[("refs")]
    LR -->|node_id 回查正文| M6["M06 点查"]
    M6 --> N2[("nodes")]
    N2 --> HIT["命中集"]
    note1["本系统不暴露 /search 与 /traverse（ADR-008）"]
```

> **变更（B5/B8）**：原 DF-4 中「关键词检索 FTS」与「多跳遍历」的**公开入口已移除**；M05 降级为 M-LR 内部依赖。系统内检索能力：按 ID 直读（M06 点查）+ 文档树/章节树浏览（M06）；语义与关键词检索由 LightRAG 承担。

## DF-5 鉴权与写入链（v1.3 新增：B2/B3）

```mermaid
sequenceDiagram
    participant U as 人类用户
    participant CLI as CLI/Skill<br/>(agent 侧)
    participant WEB as WebUI<br/>(浏览器)
    participant M10 as M10 鉴权
    participant DB as PG<br/>(users/keys/grants/nonces/sessions)
    participant API as M06/M07
    participant ST as M02 存储

    Note over U,CLI: 路径 A：agent 每请求签名
    U->>CLI: 运行 agent（继承 SSH 私钥）
    CLI->>M10: 请求 + X-SSH-Signature/Key-Id/Timestamp/Nonce/Actor
    M10->>DB: 时间窗校验 → nonce 唯一性 → 公钥查表
    DB-->>M10: user_id + role + grants
    M10->>M10: Ed25519 验签 → authorize(perm, target)
    alt 验签/授权失败
        M10-->>CLI: 401/403 + 审计事件（entity=auth）
    else 通过
        M10->>API: 注入 WriteContext(actor=user_id, source=agent)
        API->>ST: 事务：events + 实体
        ST-->>API: 提交
        API-->>CLI: 结果
    end

    Note over U,WEB: 路径 B：WebUI 挑战-响应换会话
    U->>WEB: 打开登录页
    WEB->>M10: POST /auth/challenge
    M10->>DB: 写 nonce（TTL 120s）
    M10-->>WEB: nonce
    WEB->>CLI: 本地签名（agenticdocer auth sign）
    CLI-->>WEB: signature
    WEB->>M10: POST /auth/login {keyFingerprint, nonce, signature}
    M10->>DB: 验签 → 建 session（仅存 token SHA256）
    M10-->>WEB: Set-Cookie: agenticdocer_session（httpOnly, TTL 8h）
    WEB->>M10: 后续请求带 Cookie
    M10->>DB: resolve_session → user + role + grants
    M10->>API: 注入 WriteContext(actor=user_id, source=webui)
    API-->>WEB: 结果
```

**鉴权审计流**：所有 401/403、用户/授权/密钥变更 → `events(entity='auth', op∈{login,logout,fail,user_change,grant_change,key_change})` → 供审计查询（不参与实体折叠）。
***```

## 数据驻留与边界

| 数据 | 位置 | 生命周期 |
|---|---|---|
| 权威内容（nodes/refs/events/comments/schemas/assets/terms/docs/**users/ssh_keys/grants/sessions/nonces**） | PG `agenticdocer`（nodes 按 doc_id HASH 64 分区；events 按 ts 月分区） | 永久（append-only 事件；events 分区 >24 月归档）；nonces TTL 300s、sessions TTL 8h |
| 渲染产物 | `build/rendered/`（含 `sections/<anchor>.md`） | 可重建（派生） |
| 导入快照（源 markdown） | `spec/standards/` | 只读（勿编辑；改版经 M03 重导入） |
| LightRAG 索引 | 现：`/home/lxx/lightrag/rag_storage`（JSON）；迁移后：同 PG 实例 `LIGHTRAG_*` 表 | 派生（可重建） |
| **SSH 公钥（管理员自举）** | `data/admin_keys/admin.pub`（gitignore） | 部署期输入；入库后以 DB 为准 |
| **SSH 私钥** | 用户 `~/.ssh/`（**系统从不持有**） | 由用户自行管理 |
