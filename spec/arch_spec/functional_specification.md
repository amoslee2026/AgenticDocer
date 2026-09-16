---
title: 功能规格书 — 芯片设计知识库系统
type: composite
purpose: spec
audience: both
direction: input
status: approved
version: "1.2.0"
section_meta: "@meta"
---

# 功能规格书

生成：2026-09-16（it.arch Phase 3）。输入基线：`../idea/design_doc.md` v1.1.0（模块 M01–M09 + M-LR）。环境事实与调研见 `research_report.md`。

> 编号规则：`REQ-M##-F##`（M## = 模块，F## = 模块内功能序）。优先级：P0 = 阶段 1（地基+闭环）；P1 = 阶段 2（人机接口）；P2 = 阶段 3（增值）。

## 功能列表

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
| REQ-M05-F01 | refs 多跳检索（CTE） | M05 | P2 | 3 |
| REQ-M05-F02 | 关键词检索 | M05 | P2 | 3 |
| REQ-M06-F01 | 结构化读写 API | M06 | P1 | 2 |
| REQ-M06-F02 | lint 自修复闭环 | M06 | P1 | 2 |
| REQ-M07-F01 | 表单数据 API | M07 | P1 | 2 |
| REQ-M07-F02 | 结构化 diff API | M07 | P1 | 2 |
| REQ-M07-F03 | 批注 API | M07 | P1 | 2 |
| REQ-M07-F04 | 状态流转 API | M07 | P1 | 2 |
| REQ-M07-F05 | 版本历史 API | M07 | P1 | 2 |
| REQ-M08-F01 | schema 驱动表单引擎 | M08 | P1 | 2 |
| REQ-M08-F02 | 结构化 diff 视图 | M08 | P1 | 2 |
| REQ-M08-F03 | 批注面板（含 orphaned） | M08 | P1 | 2 |
| REQ-M08-F04 | 追溯与历史视图 | M08 | P1 | 2 |
| REQ-M09-F01 | M09A schema 校验引擎 | M09 | P0 | 1 |
| REQ-M09-F02 | M09B 质量门 | M09 | P2 | 3 |
| REQ-MLR-F01 | LightRAG 导出包（渲染文本+node_id） | M-LR | P2 | 3 |
| REQ-MLR-F02 | 增量事件流接口 | M-LR | P2 | 3 |

## 功能详细说明

### REQ-M01-F01: 原子类型 Schema 注册

八类原子（`clause`/`definition`/`table`/`figure`/`code`/`example`/`note`/`cross_ref`）的 JSON Schema 定义与变体（`table.register_field`、`figure.state_machine`），持久化于 `schemas` 表（`type_name`/`json_schema`/`version`）。

**验收标准**：八类 + 2 变体 schema 齐全且可被 M09A 加载；schema 变更产生 `schema` 事件；无 schema 的 `atom_type` 写入被拒。

### REQ-M01-F02: 节点结构与锚规则约束

节点字段（`format` ∈ {md,html,text}、`parent_node_id`、`level`、`anchor`）的构造与校验规则：锚 = 章节号路径 + 标题 slug，重复标题（同父同题）按「正文摘要 sha256[:8]」消歧、正文亦同者加同级序号；构造仅依赖文档内容与同级计数。

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

按 `images/<sha256>.jpg` 引用从 GigaRAG 目录取件、校验哈希、写 `assets`；缺失不阻断。

**验收标准**：抽样图片哈希一致；缺失图片报告 `assets.missing` 清单。

### REQ-M04-F01: 文档渲染（HTML 片段直通）

节点树 → Markdown 文档：`format:html` 片段原样回写（零改写）；frontmatter 按 C5 字段回写；图片以相对路径指向导出资产。

**验收标准**：`normalize(render(store(parse(src)))) == normalize(src)`（判定口径：本节 §3 M04 `normalize()` 与 `../idea/design_doc.md` §10）；HTML 表格行列数与单元格文本保真；图片集合（含 HTML `<img>`）一致。

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

## 不支持的功能（声明）

复杂可配置工作流引擎、多项目多层级组织、报表仪表盘、PLM/ALM 双向集成、全自动 PDF/markdown 直转、完整 URN 注册表（B8 简化）、HTML 片段结构化拆解（E1-a 否决）、商业 CCMS 采购（v0.1 §9）。
