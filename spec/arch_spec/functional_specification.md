> [!NOTE]
> **Annotations present.** This file contains reviewer feedback.
> `==highlights==` flag text for discussion. `%%comments%%` are inline notes (hidden in preview, visible in source).
> `~~deletions~~` suggest removal. `> [!EDIT]` blocks are change requests. `> [!TODO]` blocks are instructions to execute.
> These markers are intentional — do not remove or "clean up" without asking the reviewer.

---
title: 功能规格书 — 芯片设计知识库系统
type: composite
purpose: spec
audience: both
direction: input
status: approved
version: "1.4.0"
section_meta: "@meta"
---

# 功能规格书

生成：2026-09-16（it.arch Phase 3）。输入基线：`../idea/design_doc.md` v1.1.0（模块 M01–M09 + M-LR）。环境事实与调研见 `research_report.md`。

> **v1.3 修订（批注 B11）**：新增 REQ-M07-F06（文档 diff）、REQ-M08-F05（可编辑表格）、REQ-M10-F01..F05（鉴权与用户管理）、REQ-M11-F01..F07（CLI 工具族与 skill，含 `docer-annotations` 人类标注调取）；REQ-M05-F01/F02 改注为**内部实现**（批注 B5）。**批注原文保留**于各处置点。

> 编号规则：`REQ-M##-F##`（M## = 模块，F## = 模块内功能序）。优先级：P0 = 阶段 1（地基+闭环）；P1 = 阶段 2（人机接口）；P2 = 阶段 3（增值）。

## 功能列表

> [!TODO] 应该提供文档版本管理，获取文档diff
>
> **处置（B11）**：已落地为 REQ-M07-F06（文档版本 diff API）+ REQ-M11-F02（CLI/skill 层 diff）。版本管理本体由 `events` append-only + `apply_events` 重放支持（REQ-M02-F03/F04 已覆盖），本次补充**面向使用者的 diff 呈现**。
>
> [!TODO] 应该提供skill和CLI 为提供文档导入，删除，修改和读取，另外专用skill调取人类用户的标注；
>
> **处置（B3/B11）**：已落地为 REQ-M11-F01..F04（CLI 工具族）、REQ-M11-F05..F07（skill 清单，含 `docer-annotations` 专用标注调取 skill）。详见架构规范 §9。


| REQ_ID | 功能 | 模块 | 优先级 | 阶段 |
|---|---|---|---|---|
| REQ-M01-F01 | 原子类型 Schema 注册 | M01 | P0 | 1 |
| REQ-M01-F02 | 节点结构与锚规则约束 | M01 | P0 | 1 |
| REQ-M01-F03 | doc_type 组合规则 | M01 | P2 | 3（随首个非 standard 类型） |
| REQ-M02-F01 | 节点 CRUD + 乐观锁 | M02 | P0 | 1 |
| REQ-M02-F02 | 引用边管理（含 ref 事件） | M02 | P0 | 1 |
| REQ-M02-F03 | 事件日志 append-only + 重放 | M02 | P0 | 1 |
| REQ-M02-F04 | 事务一致性（事件+实体同事务） | M02 | P0 | 1 |
| REQ-M02-F05 | 批注 CRUD（open/resolved/orphaned） | M02 | P1 | 2 |
| REQ-M02-F06 | 资产表读写（sha256 寻址） | M02 | P1 | 2 |
| REQ-M03-F01 | markdown 解析器（规则库+提议） | M03 | P0 | 1 |
| REQ-M03-F02 | CLI 审核器 | M03 | P0 | 1 |
| REQ-M03-F03 | 入库（经校验的事务写入） | M03 | P0 | 1 |
| REQ-M03-F04 | 未映射内容兜底 | M03 | P0 | 1 |
| REQ-M03-F05 | 图片资产导入 | M03 | P1 | 2 |
| REQ-M04-F01 | 文档渲染（HTML 片段直通） | M04 | P0 | 1 |
| REQ-M04-F02 | normalize() 规范化表示 | M04 | P0 | 1 |
| REQ-M04-F03 | 渲染产物落盘（build/rendered/） | M04 | P1 | 2 |
| REQ-M05-F01 | refs 多跳检索（**内部实现**，供 M-LR；B5） | M05 | P2 | 3 |
| REQ-M05-F02 | 关键词检索（**内部实现**，供质量门/导出；B5） | M05 | P2 | 3 |
| REQ-M06-F01 | 结构化读写 API | M06 | P1 | 2 |
| REQ-M06-F02 | lint 自修复闭环 | M06 | P1 | 2 |
| REQ-M07-F01 | 表单数据 API | M07 | P1 | 2 |
| REQ-M07-F02 | 结构化 diff API | M07 | P1 | 2 |
| REQ-M07-F03 | 批注 API | M07 | P1 | 2 |
| REQ-M07-F04 | 状态流转 API | M07 | P1 | 2 |
| REQ-M07-F05 | 版本历史 API | M07 | P1 | 2 |
| REQ-M07-F06 | 文档版本 diff API（B11） | M07 | P1 | 2 |
| REQ-M08-F01 | schema 驱动表单引擎 | M08 | P1 | 2 |
| REQ-M08-F02 | 结构化 diff 视图 | M08 | P1 | 2 |
| REQ-M08-F03 | 批注面板（含 orphaned） | M08 | P1 | 2 |
| REQ-M08-F04 | 追溯与历史视图 | M08 | P1 | 2 |
| REQ-M08-F05 | 可编辑表格视图（B6） | M08 | P2 | 3 |
| REQ-M09-F01 | M09A schema 校验引擎 | M09 | P0 | 1 |
| REQ-M09-F02 | M09B 质量门 | M09 | P2 | 3 |
| REQ-MLR-F01 | LightRAG 导出包（渲染文本+node_id） | M-LR | P2 | 3 |
| REQ-MLR-F02 | 增量事件流接口 | M-LR | P2 | 3 |
| REQ-M10-F01 | SSH 公钥签名鉴权（全端点，B2） | M10 | P0 | 1 |
| REQ-M10-F02 | WebUI 会话登录（挑战-响应，B2） | M10 | P0 | 1 |
| REQ-M10-F03 | 用户与 SSH 公钥管理（admin，A1/B3） | M10 | P0 | 1 |
| REQ-M10-F04 | RBAC 四角色 + 文档集级授权（B3） | M10 | P0 | 1 |
| REQ-M10-F05 | 管理员自举与鉴权审计（B2） | M10 | P0 | 1 |
| REQ-M11-F01 | CLI：导入/删除/修改/读取工具族（B3/B11） | M11 | P1 | 2 |
| REQ-M11-F02 | CLI：文档版本 diff（B11） | M11 | P1 | 2 |
| REQ-M11-F03 | CLI：用户与授权管理（admin，B3） | M11 | P0 | 1 |
| REQ-M11-F04 | CLI：自动签名与身份传递（B2） | M11 | P0 | 1 |
| REQ-M11-F05 | Skill：docer-import/read/write/render（B3） | M11 | P1 | 2 |
| REQ-M11-F06 | **Skill：docer-annotations 调取人类标注**（B11） | M11 | P1 | 2 |
| REQ-M11-F07 | Skill：docer-diff 变更感知（B11） | M11 | P2 | 3 |
| REQ-M12-F01 | AgenticLogger 全面接入（全模块统一出口） | M12 | P0 | 1 |
| REQ-M12-F02 | 请求级追踪（rid 贯穿鉴权→API→存储→渲染） | M12 | P0 | 1 |
| REQ-M12-F03 | 在线性能指标（API/慢查询/鉴权/渲染） | M12 | P1 | 2 |
| REQ-M12-F04 | 性能基准套件（tests/perf/，可复现验收） | M12 | P1 | 2 |
| REQ-M12-F05 | 容量健康巡检（分区/索引/膨胀/连接池/归档） | M12 | P1 | 2 |
| REQ-M12-F06 | **运行期 LLM 无关约束（P6）的机械验证** | M12 | P0 | 1 |

## 功能详细说明

### REQ-M01-F01: 原子类型 Schema 注册

八类原子（`clause`/`definition`/`table`/`figure`/`code`/`example`/`note`/`cross_ref`）的 JSON Schema 定义与变体（`table.register_field`、`figure.state_machine`），持久化于 `schemas` 表（`type_name`/`json_schema`/`version`）。

**验收标准**：八类 + 2 变体 schema 齐全且可被 M09A 加载；schema 变更产生 `schema` 事件；无 schema 的 `atom_type` 写入被拒。

### REQ-M01-F02: 节点结构与锚规则约束

节点字段（`format` ∈ {md,html,text}、`parent_node_id`、`level`、`anchor`）的构造与校验规则：锚 = 章节号路径 + 标题 slug，重复标题（同父同题）按「正文摘要 sha256[:8]」消歧、正文亦同者加同级序号；构造仅依赖文档内容与同级计数。


### REQ-M01-F02: 节点结构与锚规则约束（续）
**验收标准**：锚消歧口径 = 「同父路径+同标题 → 正文摘要 sha256[:8]；正文亦同 → 同级序号」（A1）；对实测 219×「Test Steps:」（同父同题）全组生成**互异**锚，且两次相同解析结果逐字节一致（幂等）。

### REQ-M01-F03: doc_type 组合规则

`doc_type → 允许原子类型/必填字段` 的规则模型（随首个非 `standard` 类型引入，Q6）。

**验收标准**：非 `standard` 类型文档引入时，组合规则可配置并被 M03/M09A 消费。

### REQ-M02-F01: 节点 CRUD + 乐观锁

节点读取/创建/更新/删除；更新携带 `version`，不匹配返回 409（可重试）；成功则 `version+1`。

**验收标准**：并发更新同一节点，后到者得 409 且库内数据为前写者结果；无静默丢失更新。

### REQ-M02-F02: 引用边管理（含 ref 事件）

`refs` 的增删（`add`/`remove`），每次变更写 `ref` 事件（payload：`{src, dst_doc, dst_node, kind}`，与 §3.5 规范表一致）。

**验收标准**：任意 refs 变更后，`events` 中存在对应 ref 行；M-LR 增量可从事件流重建 ref 变更序列。

### REQ-M02-F03: 事件日志 append-only + 重放

`events` 仅允许插入（无 UPDATE/DELETE 路径）；提供按实体/时间重放得到历史视图（含字段级 diff）。

**验收标准**：代码审计无 events 更新/删除语句；对任一节点重放其全部事件 == 当前态（M09B 巡检一致）；重放含 `before/after` 字段级 diff。

### REQ-M02-F04: 事务一致性（事件+实体同事务）

每个写操作以单事务提交事件行 + 实体变更；失败整体回滚。

**验收标准**：注入事务中途失败，库内既无孤立事件也无未记录变更（无撕裂状态）。

### REQ-M02-F05: 批注 CRUD（open/resolved/orphaned）

批注创建（锚定 `target_event_id`）、解决（resolved）、节点删除后置 `orphaned`（保留不级联）。

**验收标准**：节点**软删**（`delete_node`，乐观锁校验）后 `status=deleted` 且批注仍在并置 `state=orphaned`（同事务触发 `orphan_comments`）；读路径默认过滤已删节点；历史视图可按批注的 `target_event_id` 定位其锚定版本。

### REQ-M02-F06: 资产表读写（sha256 寻址）

`assets` 行读写（`asset_id`=sha256、mime、bytes、origin、path）；重复导入去重。

**验收标准**：同 id 资产二次导入不产生重复行；缺失资产记录为 `assets.missing` 违规项（M09B）。

### REQ-M03-F01: markdown 解析器（规则库+提议）

将 markdown（+frontmatter）解析为原子提议：每提议携带 `rule_id`（命中规则）、`待确认` 标志（启发式解析）与来源行号；frontmatter 字段按 C5 规范校验。

**验收标准**：对 7 份语料解析完成；**规则覆盖率（携带 rule_id 的源块数 ÷ 总源块数）≥95%**；提议含来源定位（文件+行区间）。

### REQ-M03-F02: CLI 审核器

`agenticdocer-import review <doc_slug>`（等价 `python -m agenticdocer.importer review`）：逐条展示提议（内容+rule_id+待确认标志），支持 通过/拒绝/修正/批量通过待确认/查看未映射清单。

**验收标准**：可在无 WebUI 环境完整走通审核；批量通过仅作用于非待确认项或显式指定；审核动作落审计输出。

### REQ-M03-F03: 入库（经校验的事务写入）

审核通过的提议经 M09A（schema 级）校验后，以事务写入 `docs`/`nodes`/`refs`/`events`。

**验收标准**：非法提议被拒且报出违规明细；成功入库后可立即渲染（M04）且往返一致。

### REQ-M03-F04: 未映射内容兜底

无法映射八类原子的块（目录/许可/残余 HTML 等）降级为 `note`/`code`（`format:html`）原子保留，**不计入规则覆盖率**；统计「兜底率与待确认条数」。

**验收标准**：兜底块 100% 存在于库（抽样可查）；统计报告含兜底率与待确认条数；无静默丢弃（源块数 = 承接 + 兜底）。

### REQ-M03-F05: 图片资产导入

按两类引用取件（md 形式 `images/<sha256>.jpg` + HTML `<img src>`，后者 80 处均在 `<table>` 片段内）、校验哈希、写 `assets`；缺失不阻断。

**验收标准**：抽样图片哈希一致；缺失图片报告 `assets.missing` 清单。

### REQ-M04-F01: 文档渲染（HTML 片段直通）

节点树 → Markdown 文档：`format:html` 片段原样回写（零改写）；frontmatter 按 C5 字段回写；图片以相对路径指向导出资产。

**验收标准**（两式并列，判定口径见 §3 M04）：(a) 解析保真 `normalize(doc_id) == normalize_markdown(src)`；(b) 渲染保真 `normalize_markdown(<产物文件>) == normalize_markdown(src)`（覆盖 HTML 直通/内联标记/frontmatter 回写破坏；images 按重写前哈希路径集合比较）。HTML 表格行列数与单元格文本保真。

### REQ-M04-F02: normalize() 规范化表示

定义并实现规范化函数：标题序列（层级+文本）、表格（行列+单元格文本）、代码块内容、图片引用集、列表结构、内联标记保真集。

**验收标准**：normalize 对语料输出稳定（两次运行逐字节一致）；作为往返一致性的唯一判定口径。

### REQ-M04-F03: 渲染产物落盘（build/rendered/）

渲染产物输出至 `build/rendered/`（不在 spec/、不被 ingest 扫描）；导出 `build/rendered/assets/`。

**验收标准**：产物目录可整体删除重建；无产物写入 `spec/` 下路径。

### REQ-M05-F01: refs 多跳检索（CTE）

按 `traces_to`（上游，默认 1 跳、可 2 跳）、`composes_from`（下游 1 跳）、`see_also`（双向 1 跳）遍历；节点集去重保留最短路径；环截断；排序 = 跳数→文档序→ordinal。

**验收标准**：构造含环与重复路径的 fixture，结果符合去重/排序规则；`source_ref` 不参与多跳。

### REQ-M05-F02: 关键词检索

PG FTS（english 起步）全文检索 + 结果含 node_id 与文档锚。

**验收标准**：`tests/fixtures/search_goldenset.yaml`（≥30 条 `query → 期望 node_id`，一次性人工标注入库）命中率 ≥90%；性能：`tests/perf/` 固定查询集（≥100 次，7 份语料全量入库后，本机 PG 16.15）P95 <200ms。

### REQ-M06-F01: 结构化读写 API

面向 agent 的读写接口：JSON Schema 约束的节点/文档写操作（含乐观锁）、读操作；写成功后联动渲染。

**验收标准**：非法结构 100% 被拒；写-渲染联动闭环；契约测试通过。

### REQ-M06-F02: lint 自修复闭环

校验失败返回结构化违规清单（含修复建议字段），支持 agent 修正后重试。

**验收标准**：典型违规（缺必填、锚冲突、非法 format）返回可操作建议；重试成功路径闭环。

### REQ-M07-F01..F05: WebUI 后端 API

表单数据（节点读写）、结构化 diff（按 events）、批注、状态流转、版本历史五组 API（OpenAPI 描述）。

**验收标准**：OpenAPI 契约生成且与实现一致；M08 仅依赖契约可并行开发；diff 展示字段级新旧值。

### REQ-M08-F01..F04: WebUI 前端

schema 驱动表单引擎（Q3 ADR 裁决实现）；（结构化 diff 视图）；批注面板（含 orphaned）；追溯与历史视图。

**验收标准**：e2e 动作——仅向 `schemas` 表插入一个新 `atom_type`（**不改任何前端文件**）后出现可用表单（「零手写 UI」的机械判据）；diff 视图并排展示新旧值；批注/历史交互闭环。

### REQ-M09-F01: M09A schema 校验引擎

JSON Schema 校验规则库；服务 M03 提议校验与 M06 写入校验（阶段 1 随 M01 交付）。

**验收标准**：违规清单含字段路径与规则 id；规则库可单测覆盖。

### REQ-M09-F02: M09B 质量门

断链检测、术语校验（`terms` 表）、assets 缺失、渲染一致性（消费 normalize）、events↔当前态一致性巡检。

**验收标准**：五类违规各有 detector 与报告；断链注入被检出（端到端用例）。

### REQ-MLR-F01: LightRAG 导出包（渲染文本+node_id）

将渲染文本与 node_id metadata 打包为可导入格式（**联调暂缓，C7**）。

**验收标准**：导出包字段完整（文本+node_id 映射）；不依赖 lightRAG 在线。

### REQ-MLR-F02: 增量事件流接口

基于 events 的增量变更流（供 M-LR 消费）。

**验收标准**：可重放式拉取（since 游标）；与 M02 事件日志一致。

### REQ-M07-F06: 文档版本 diff API（B11）

`GET /api/v1/docs/{id}/diff?from=&to=`：按 `events` 重放两个时间点（或版本号）的文档状态，返回**结构化 diff**——按 node_id 对齐，逐字段给出 `{before, after}`，并标注节点级操作（新增/修改/软删/引用变化）。

**验收标准**：(a) 对任意两次写入间的变更，diff 输出覆盖全部被改节点且无多余节点；(b) 每条变更含 `nodeId`/`anchor`/`field`/`before`/`after`；(c) 与 `apply_events` 重放结果一致（同一折叠口径，P5）；(d) 无变更时返回空 diff（非 404）。

### REQ-M08-F05: 可编辑表格视图（B6）

当文档 frontmatter `editable_tables: true`（或 doc_type 在可编辑白名单）且用户角色 ≥ editor 时，`table` 原子渲染为可编辑控件（单元格可编辑、行列增删）；提交经 `PATCH /api/v1/nodes/{node_id}/table` 回写（服务端转 content，携带 `expectedVersion` 乐观锁）。

**验收标准**：(a) 非 editor 角色或未开启开关时，表格为只读；(b) 编辑提交后节点 `content` 更新且产生 `node` 事件（字段级 diff）；(c) 并发编辑冲突返回 409；(d) **HTML `<table>` 片段（含其中 80 处 `<img>` 引用的形态）不转为可编辑控件**（保持零改写直通，P4）——**V24 修正**：原写「1,099 处」有误（1,099 = md 1,019 + HTML `<img>` 80 的总数；其中仅 80 处位于 HTML 表格片段内）。

### REQ-M10-F01: SSH 公钥签名鉴权（全端点）

所有 HTTP 端点（含读）要求 SSH 签名：请求头 `X-SSH-Signature`/`X-SSH-Key-Id`/`X-Timestamp`/`X-Nonce`/`X-Actor`；签名载荷 = `METHOD\nPATH\nSHA256(body)\nTimestamp\nNonce`。服务端按「时间窗 → nonce 未复用 → 公钥查表 → 验签」顺序校验。

**验收标准**：(a) 有效签名通过，`actor` 解析为 `user_id`；(b) 篡改 body/path/时间戳任一 → 401；(c) 重放同一 nonce → 401；(d) 时间戳偏移 >300s → 401；(e) 未注册公钥 → 403；(f) `X-Actor` 与验签身份不一致 → 403；(g) 无凭据 → 401（**fail-closed**）。

### REQ-M10-F02: WebUI 会话登录（挑战-响应）

`POST /auth/challenge` 取一次性 nonce（TTL 120s）→ 客户端用 SSH 私钥签名 → `POST /auth/login` 验签通过后签发会话 Cookie（httpOnly/SameSite=Lax，TTL 8h 滑动续期）；`POST /auth/logout` 销毁。

**验收标准**：(a) 有效签名登录成功并 Set-Cookie；(b) nonce 复用/过期 → 401；(c) 会话过期后请求 → 401；(d) logout 后原 Cookie 失效；(e) 会话 token 在 DB 仅存 SHA256 哈希（明文不入库）。

### REQ-M10-F03: 用户与 SSH 公钥管理（admin）

`GET/POST /api/v1/users`、`PATCH/DELETE /api/v1/users/{id}`、`POST /api/v1/users/{id}/keys`（登记/吊销公钥）。

**验收标准**：(a) 仅 admin 可访问（其他角色 403）；(b) 禁用用户后其所有密钥立即失效（后续请求 401）；(c) 吊销单个密钥不影响同用户其他密钥；(d) 用户变更落 `auth` 事件（审计）；(e) 用户名唯一冲突返回 409。

### REQ-M10-F04: RBAC 四角色 + 文档集级授权

四角色基线权限（见架构 §3 M10 权限矩阵）+ `grants` 表按 `doc_type`/`doc`/`repo` 授予额外权限；`authorize(user, perm, target)` 判定：角色基线 ∪ 有效 grant，**grant 不可超越角色上限**。

**验收标准**：(a) reader 写操作 → 403；(b) reviewer 可批注与审批但不能改正文；(c) editor 不可管理用户；(d) 文档集级 grant 生效范围精确（他 doc 不受影响）；(e) 越权 grant 尝试（如给 reader 授 write）被拒。

### REQ-M10-F05: 管理员自举与鉴权审计

`ADMIN_SSH_PUBKEY_FILE` 指向的公钥在首次 migrate/启动时创建 admin 用户（幂等）；无任何用户时系统 fail-closed（全部请求 401 并提示自举步骤）。鉴权失败（401/403）与用户/授权/密钥变更落 `events`（`entity='auth'`）。

**验收标准**：(a) 空库启动 → 自举成功后 admin 可用；(b) 重复自举幂等（不重复创建）；(c) 无 `users` 行时所有端点 401 且错误信息指向自举；(d) 每次鉴权失败产生 `auth` 事件（含时间戳/端点/失败原因，不含密钥材料）。

### REQ-M11-F01: CLI 工具族（导入/删除/修改/读取）

统一入口 `agenticdocer`，提供 `import`/`import review`/`doc list|get|delete`/`node get|put|delete`/`comment list|add|resolve`/`render`/`stats`（完整清单见架构 §9.2）。

**验收标准**：(a) 每条命令可独立完成其语义操作并输出结构化结果（`--json`）；(b) 权限不足时以非零退出码 + 明确错误信息拒绝；(c) 读命令失败不影响库状态；(d) 所有命令（除 `auth bootstrap`）自动附带签名。

### REQ-M11-F02: CLI 文档版本 diff

`agenticdocer doc diff <doc_id> [--from <ts|version>] [--to <ts|version>]`：输出与 REQ-M07-F06 同口径的结构化 diff（人可读表格 + `--json` 机器可读）。

**验收标准**：(a) 输出与 API 版本结果一致（同一实现）；(b) `--from/--to` 缺省时以「当前 vs 上一次变更」为默认区间；(c) 无变更时输出空且退出码 0。

### REQ-M11-F03: CLI 用户与授权管理

`agenticdocer user add|list|disable|role`、`user key add|revoke`、`grant add|list|rm`（admin 专属）。

**验收标准**：(a) 非 admin 执行 → 退出码非零 + 明确拒绝信息；(b) 效果与 WebUI 等价（同一 M10 服务层）；(c) 操作落 `auth` 事件。

### REQ-M11-F04: CLI 自动签名与身份传递

CLI 从 `~/.ssh/` 或 `AGENTICDOCER_SSH_KEY` 读取私钥，自动生成签名头；`agenticdocer auth whoami` 显示当前身份/角色/公钥指纹。

**验收标准**：(a) 无私钥时给出明确错误与获取指引（非堆栈）；(b) 私钥与登记公钥不匹配时 403 并提示；(c) `auth bootstrap` 是唯一无需签名的命令。

### REQ-M11-F05: Skill：docer-import / read / write / render

`skills/` 下四个 skill 定义，封装对应 CLI 命令的调用语义（何时用、如何解读输出、失败重试策略、所需角色）。

**验收标准（V17 修复：改为可机械验证）**：(a) `skills/` 下 6 个 skill 定义均含 `name`/`description`/前置角色/底层命令**四字段**，且可被 JSON Schema 校验通过；(b) 用固定 prompt 驱动参考 agent（或 CLI `--dry-run` 干跑模式）能成功调用底层命令并返回结构化输出（`--json`）；(c) 权限不足时输出**包含所需角色名与授权命令原文**（如 `需 editor 角色；执行：agenticdocer grant add --username X --scope doc_type --value Y --permission write`）。

### REQ-M11-F06: Skill：docer-annotations 调取人类标注（B11 专项）

专用 skill，供 agent 读取人类用户在 WebUI 中留下的批注：支持按 `doc_id`/`node_id`/`state`（open/resolved/orphaned）筛选，返回批注正文、作者、锚定版本（`target_event_id`）及该版本上下文。

**验收标准**：(a) 能列出指定文档的全部开放批注（含锚定节点与版本）；(b) 能按 `target_event_id` 取回批注所指的历史节点内容（供 agent 理解「人类在说什么」）；(c) 含 orphaned 批注（节点已软删）的专门查询路径；(d) 只读，不修改批注状态（状态变更属 reviewer 职责，走 `comment resolve`）。

### REQ-M11-F07: Skill：docer-diff 变更感知

封装 `agenticdocer doc diff`，供 agent 在动手前感知他方（人类或其他 agent）对文档的改动。


**验收标准**：(a) 返回结构化变更摘要（节点数/字段数/操作类型分布）；(b) 与 M11-F02 同口径；(c) 建议工作流中明确「先 diff 后 write」的时序（避免基于过期版本写入）。

### 安全评审（S1–S16）验收项补充

以下为对抗评审（SecAuthReview，2026-09-16）发现并已修复的设计缺陷，**其验收标准已并入上文对应 REQ**，此处汇总索引：

| 修复 | 已并入 | 关键验收项 |
|---|---|---|
| S1：`events.entity` 增 `'auth'` | REQ-M10-F05 | DDL CHECK 与 Event Literal 含 `'auth'`；审计事件可插入 |
| S2：签名载荷含 query string | REQ-M10-F01 | **篡改 query 任一参数 → 401**（如 `expected_version`） |
| S3：nonce TTL ≥ 2×时间窗 | REQ-M10-F01 | 未来时间戳请求在时间窗内无法重放 |
| S4：豁免清单 | REQ-M10-F01 | 仅 `/auth/challenge`、`/auth/login`、登录页资源、`/healthz` 豁免；**清单外无凭据必 401**；`/docs` 与 `/openapi.json` 非开发模式禁用 |
| S5：grant 形式化 | REQ-M10-F04 | 角色为**硬上限**（reader+write grant 永远 403）；越权 grant 在**授予与判定两处**均拒；`repo` scope 已删 |
| S6：TLS 强制 | REQ-M10-F02 | 非 loopback 监听必须 TLS；Cookie `Secure`；状态变更仅接受 JSON |
| S7：限流与不写库 | REQ-M10-F01/F05 | 未认证请求不写 nonces；challenge/login 按 IP 限流；失败事件聚合 |
| S8：会话随用户禁用失效 | REQ-M10-F03 | disable 用户后**既有会话立即 401**（resolve_session JOIN status） |
| S9：最后管理员防护 | REQ-M10-F03 | 不可删/禁/降级自身与最后一个 active admin（409）；bootstrap 语义统一为「无 active admin 时可重复」 |
| S10：审计防污染 | REQ-M10-F05 | 失败事件 `actor='anonymous'`，自述身份记 `claimed_*` |
| S11：签名格式统一 | REQ-M10-F01 | SSHSIG + namespace `agenticdocer@auth`；RSA 用 PSS；两条客户端路径共用验签器 |
| S12：删除 WebAuthn 悬空路径 | REQ-M10-F02 | 登录仅两条方式（CLI 签名粘贴 / 签名文件） |
| S13：token 熵 | REQ-M10-F02 | `secrets.token_urlsafe(32)`（256 位 CSPRNG） |
| S14：删除 `X-Actor` | REQ-M06-F01 | 身份一律取自验签结果；`source` 由凭据类型判定 |
| S15：会话清理 | REQ-M10-F02 | 过期会话由定期任务删除（与 nonce 清理同任务） |
| S16：残余风险声明 | — | §4.1.1 已声明（无 RLS 的库内横向越权风险 + 升级触发条件） |

### REQ-M12-F01: AgenticLogger 全面接入

所有模块统一经 `observability/logger.py` 适配层调用 AgenticLogger SDK（`program="agenticdocer"`，`command=<模块/子命令>`）；禁止业务代码直接 `print`/`import logging`。

**验收标准**：(a) 每个模块产生结构化 JSONL 日志（含 `module`/`rid`/`ts`）；(b) lint 规则检出并拒绝业务代码中的 `print`/`logging` 直接使用（白名单仅适配层）；(c) 日志按 `INTERCHANGE.md` 规范可被 `agentic-logger` CLI 解析（`agentic-logger stats` 有输出）。

### REQ-M12-F02: 请求级追踪（rid 贯穿）

每次 HTTP 请求或 CLI 调用生成一个 `rid`，贯穿 M10 鉴权 → M06/M07 路由 → M02 存储 → M04 渲染全链路。

**验收标准**：(a) 单次请求的所有日志行共享同一 `rid`；(b) `agenticdocer logs trace --rid <id>` 输出该请求完整链路（含各阶段 `dur`）；(c) 并发请求的 `rid` 不串（ContextVar 正确传播，含 async 任务）。

### REQ-M12-F03: 在线性能指标

采集 API 耗时（端点 × P50/95/99）、错误率（端点 × error_code）、慢查询 Top-N（> `SLOW_QUERY_MS`）、鉴权失败率、渲染耗时（整档/章节）、导入进度；经 `GET /api/v1/admin/metrics?since=&window=` 查询快照。

**验收标准**：(a) 指标端点返回 `MetricsSnapshot` 结构且数值与实际请求相符（注入已知延迟的测试请求验证）；(b) 仅 admin 可访问（其他角色 403）；(c) 慢查询被正确识别（构造 > 阈值查询）；(d) 超指标请求产生 `error_code=DTO_PERF_EXCEEDED`。

### REQ-M12-F04: 性能基准套件

`tests/perf/` 提供 `bench_point_query.py`（点查 P95）、`bench_render.py`（整档+章节）、`bench_auth.py`（验签+会话）、`bench_scale.py`（合成 10,000 文档）、`bench_import.py`（导入吞吐与覆盖率）。

**验收标准**：(a) 每个基准可独立运行并输出所测指标（P50/P95/P99 或吞吐）；(b) 结果落 `build/perf.json`（可对比历史）；(c) `bench_scale.py` 完成 10k 文档灌入并测得分区后点查/渲染指标（ADR-009 规模验收证据）；(d) 基准在无 LLM 凭据、断网环境可运行（P6）。

### REQ-M12-F05: 容量健康巡检

巡检表/分区行数与膨胀、索引使用率（`idx_scan=0` 建议清理）、autovacuum 滞后、连接池饱和度、events 分区完整性与归档逾期；输出 `HealthReport`（`verdict` + `advice`）。

**验收标准**：(a) `agenticdocer stats --health` 输出全部巡检项；(b) 构造缺失分区/膨胀/连接池打满场景时 `verdict` 转为 `degraded`/`fail` 且 `advice` 给出具体建议；(c) 接入 M09B `perf_health` detector（质量门可调用）。

### REQ-M12-F06: 运行期 LLM 无关约束（P6）的机械验证

验证系统任何运行路径都不依赖 LLM。

**验收标准**（四项全过）：(a) `import` 白名单 lint 通过——业务代码无 `openai`/`anthropic`/`transformers`/`torch`/`litellm` 等推理 SDK 引用；(b) **断网环境下全功能测试通过**（e2e 在 `--no-network` 或屏蔽出网时全绿）；(c) `uv tree` 依赖树无推理类依赖；(d) 端到端测试在**无任何 LLM 凭据**（无相关环境变量）环境下通过。


## 不支持的功能（声明）

复杂可配置工作流引擎、多项目多层级组织、报表仪表盘、PLM/ALM 双向集成、全自动 PDF/markdown 直转、完整 URN 注册表（B8 简化）、HTML 片段结构化拆解（E1-a 否决）、商业 CCMS 采购（v0.1 §9）、**飞书多维文档集成（B7 明确排除）**。
