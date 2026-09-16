---
title: 对抗评审问题清单 — 芯片设计知识库系统（it.arch Phase 6）
type: composite
purpose: review
audience: both
direction: output
status: approved
version: "1.1.0"
section_meta: "@meta"
---

# 对抗评审问题清单（arch_spec）

**评审对象**：`spec/arch_spec/` 全量产物 —— architecture_specification.md / functional_specification.md / user_manual.md / data_flow_diagrams.md / workflow_diagrams.md / ADR-001..006 / research_report.md / clarifications.md / traceability/requirements_matrix.arch.csv
**权威基线**：`spec/idea/` v1.1.0（design_doc §5.1–§5.4/§6.4/§10/§12、clarifications B1–B16/Q1–Q6、.review/issues.md 的 E1–E20 + N1–N8）
**方法**：只读评审；语料数字与结构对 `spec/standards/*/*.md` 实测复算，环境事实对本机实测复算；未修改任何既有文件。

## 汇总

| ID | Severity | 一句话 |
|---|---|---|
| A1 | CRITICAL | 锚构造规则在实测语料上无法生成互异锚（CXL 219×「Test Steps:」同父同题同锚），必撞 `UNIQUE (doc_id, anchor)`，REQ-M01-F02 验收不可能通过 |
| A2 | HIGH | 节点删除语义三处不自洽：`comments.node_id` 外键阻断硬删，规格又无删除接口，orphaned 不可实现 |
| A3 | HIGH | 全部写方法无 actor 参数，`events.actor NOT NULL` 取值来源未定义 |
| A4 | HIGH | `comments` 表缺 `version` 列，违反 idea §5.3 的乐观锁承诺（docs/nodes/comments） |
| A5 | HIGH | `refs` 主键不含 `dst_node_id` + `remove_ref` 缺 dst_node 参数：节点级多引用不可表达、不可单条删除 |
| A6 | HIGH | assets 闭环三缺口：字节存储位置未定义、无读取端点、M03 无资产导入接口 |
| A7 | HIGH | 语料 1,099 处图片引用中 80 处为 HTML `<img>`（全在 `<table>` 片段内），资产/渲染/normalize 策略未覆盖；报告数字 1,019 不准 |
| A8 | HIGH | M08「仅此接口面」契约缺 schema 端点与节点读写端点归属，表单引擎无数据源 |
| A9 | MEDIUM | `normalize(doc_id)` / `render_document(...)` 签名无法表达 REQ-M04-F01 的往返断言，`RenderResult` 未定义 |
| A10 | MEDIUM | FTS 生成列未进 DDL + `content.text` 未约束 + HTML 表格无 text 字段 → 表格内容不可检索 |
| A11 | MEDIUM | 前端契约 camelCase 与后端 pydantic/DDL snake_case 无序列化口径 |
| A12 | MEDIUM | CLI 入口自相矛盾（`agenticdocer.import` vs 包目录 `importer/`）；`python -m agenticdocer.render` 无定义 |
| A13 | MEDIUM | parse→review→commit 的提议清单落盘/审核状态持久化与 `doc_slug` 未定义，三步骤无法闭环 |
| A14 | MEDIUM | 14 个被签名引用的类型（Node/RawFallback/RefKind/Event/TraversalHit/…）无字段定义 |
| A15 | MEDIUM | append-only 强制落不了地：REVOKE 引用未创建角色 `agenticdocer_app`，§5 连接用户却是 `agenticdocer`，无属主/GRANT 策略 |
| A16 | MEDIUM | schemas 注册、doc_type 组合规则、terms 词表三者无写入路径与载体（3 条 REQ 无实现面） |
| A17 | MEDIUM | M02 无任何 docs 级方法、状态流转无 `expectedVersion`；`docs.version` 形同虚设 |
| A18 | MEDIUM | `events.payload` 形状与重放 fold 语义未定义，M09B `events_consistency` 与 REQ-M02-F03 验收不可实现 |
| A19 | MEDIUM | 每-kind 跳数上限无法用单一 `hops` 表达；`GET /search?q=&hops=` 语义与返回类型未定义 |
| A20 | MEDIUM | 三条验收标准不可机械验证（「人工标注集」、「P95<200ms」口径、「零手写 UI」） |
| A21 | MEDIUM | Phase 6 交付物 `summary_report.md` 缺失（在 it.mas handoff transfer_files 清单内） |
| A22 | MEDIUM | frontmatter→docs 列映射与 `doc_type` 取值域未定；REQ-M03-F01「按 C5 规范校验」无字段清单 |
| A23 | LOW | 悬空章节引用：arch §1 P3「交付序见 §9」（本文只有 §1–§7）、functional REQ-M04-F01「（§测试策略）」 |
| A24 | LOW | user_manual 快速开始路径缺 `amba/` 层级，照抄即失败 |
| A25 | LOW | 缺 it.arch Phase 4 模板要求的章节（Agent Context / 分层归属 / 依赖规则矩阵 / 依赖 DAG / 非功能需求量化） |

## 问题清单

### A1 锚构造在实测语料上无法满足「互异」，必撞 UNIQUE 约束

- **Severity**：CRITICAL
- **位置**：`architecture_specification.md` §3 M01 L59-60（`make_anchor(doc_id, chapter_path, title)`）、§4 DDL L234（`UNIQUE (doc_id, anchor)`）；`ADR/ADR-006-结构化粒度与锚策略.md` §Decision（锚策略）；`functional_specification.md` REQ-M01-F02 L69（验收标准）；idea `design_doc.md` §5.4（E7）
- **问题**：锚规则为「章节号路径 + 重复标题按标题内容 sha256[:8] 消歧」，而函数签名只接收 `doc_id`/`chapter_path`/`title` 三个入参（没有正文、没有位置信息），因此「同一父路径 + 同一标题」的两个节点必然产生同一锚。该情形在指定语料中大量存在，且**正是验收标准点名的例子**：CXL 的 219 处 `## Test Steps:` 全部直属同一个无编号章 `# Power Management`（父路径与标题逐字符相同；同族还有 Fail Conditions 217 次、Pass Criteria 214 次）；按「父路径 + 标题」分组统计，全语料组内重复的额外出现合计 1,301 次（CXL 999、PCIe 164、HBM4 132、AXI 6）。这些节点的第二个开始插入即违反 `UNIQUE (doc_id, anchor)`（或被迫 upsert 覆盖，静默丢节点），REQ-M01-F02「生成互异且稳定的锚」与 P5「anchor 作为引用口径」均不成立。
- **修复建议**：二选一并同步修订 E7/REQ-M01-F02 与 ADR-006 的措辞：(a) 锚内加入「父路径 + 标题 + 同级出现序号」的确定性消歧，把「与插入位置无关」改述为「仅依赖文档内稳定计数，重排/重导入不漂移」；(b) 扩展签名为 `make_anchor(doc_id, chapter_path, title, occurrence_index, body_digest)`，用**正文摘要**（而非标题摘要）参与消歧，并在 REQ-M01-F02 写明「同标题块以正文哈希区分，正文亦相同者以同级序号区分」。

### A2 节点删除语义缺失且与批注 orphaned 需求互斥

- **Severity**：HIGH
- **位置**：`architecture_specification.md` §4 DDL L230（`nodes.status` 无 CHECK）、L261-267（`comments.node_id uuid NOT NULL REFERENCES nodes(node_id)`，L263 注释「不级联：保留 orphaned」）、L240-246（refs 用 `ON DELETE CASCADE`/`SET NULL`）；§3 M02 L84（`orphan_comments`）；`functional_specification.md` REQ-M02-F05 L105
- **问题**：REQ-M02-F05 与 idea §6.3 要求「节点删除后批注仍在且 `state=orphaned`」，但 `comments.node_id` 是 NOT NULL 外键且无 `ON DELETE` 子句（默认 NO ACTION），只要批注存在，节点行就**删不掉**；同时 §3 M02 没有任何删除接口（只有 `orphan_comments`）、M06 也没有 `DELETE /nodes/{id}`，`nodes.status`（默认 `'active'`）既无 CHECK 也无取值域说明。结果是三处假定不一致：refs 假定硬删（级联/SET NULL）、comments 假定软删（保留 orphaned）、REQ 断言删除后批注可查——任选一种实现都会违反另外两处。附带：`orphan_comments(node_id)` 本身也无法被任何已声明的操作触发。
- **修复建议**：明确「节点删除 = 软删」并补齐链路：`nodes.status text NOT NULL DEFAULT 'active' CHECK (status IN ('active','deleted'))`；§3 M02 增 `delete_node(node_id, expected_version, actor)`（置 status='deleted'、写 node 事件、同事务调用 `orphan_comments`）；M06 增 `DELETE /api/v1/nodes/{node_id}`；写明所有读路径默认过滤 `status='active'`。（若坚持硬删，则 `comments.node_id` 必须可空 + `ON DELETE SET NULL`，并重写 orphaned 语义。）

### A3 写路径未定义 actor 传递口径，`events.actor NOT NULL` 无来源

- **Severity**：HIGH
- **位置**：`architecture_specification.md` §4 DDL L255（`actor text NOT NULL`）；§3 M02 L76-86（`upsert_node`/`add_ref`/`remove_ref`/`resolve_comment`/`orphan_comments`/`put_asset`）；§3 M01 L63-66（`NodeIn` 无 actor）；§6 横切关注点 L310-318（无 actor 约定）
- **问题**：P2 要求「一切写入 = 事件 + 实体同事务」，即每个写方法都要自己写 `events` 行，而 `events.actor` 是 NOT NULL；但所有写方法签名都没有 actor（或等效的写上下文）参数，`NodeIn` 也不携带 actor，规格未定义身份的取值来源（HTTP 头 / CLI 身份 / contextvar / 默认值）。实现者只能自行发明（例如硬编码 "system"），审计追溯（B6：审计靠事件日志）随之失效。
- **修复建议**：在 §3 M02 的所有写方法末尾加 `actor: str`，或统一引入 `WriteContext(actor: str, source: Literal['agent','webui','cli','importer'])` 参数；在 §6 横切关注点写明取值规则（M06/M07 由请求头 `X-Actor` 注入、CLI 默认 `cli`、M03 导入默认 `importer`、系统任务默认 `system`），并要求 M06/M07 在 401/422 层面拒绝空 actor。

### A4 `comments` 表缺乐观锁列，E5 在批注路径落空

- **Severity**：HIGH
- **位置**：`architecture_specification.md` §4 DDL L261-267（comments 无 `version`）、§3 M02 L83（`resolve_comment(comment_id)`）、§3 M07 L163（`PATCH /api/v1/comments/{id}`）；idea `design_doc.md` §5.3 L162；`functional_specification.md` REQ-M02-F05 L101-105
- **问题**：idea v1.1 §5.3 明确「`docs`/`nodes`/`comments` 带 `version` 列做乐观锁——写入请求携带读到版本，不匹配返回 409」；arch DDL 中 docs、nodes 都落实了 `version bigint`，**comments 漏项**；`resolve_comment` 也没有 `expected_version`，M07 的批注状态接口因此没有任何并发保护：两人同时对同一批注执行 resolve/orphan 时后写者静默覆盖。
- **修复建议**：`comments` 增 `version bigint NOT NULL DEFAULT 1`；`resolve_comment(comment_id, expected_version, actor)`（不符抛 ConflictError→409）；M07 `PATCH /api/v1/comments/{id}` body 定为 `{state, expectedVersion}` 并返回 409 语义，与 M06 保持一致。

### A5 `refs` 主键与 `remove_ref` 签名使节点级引用不可表达/不可删除

- **Severity**：HIGH
- **位置**：`architecture_specification.md` §4 DDL L240-247（PK L245：`(src_node_id, dst_doc_id, kind)`）；§3 M02 L78-79（`add_ref` 有 dst_node，`remove_ref` 无）；`functional_specification.md` REQ-M02-F02 L83-87、REQ-M05-F01 L161-165
- **问题**：(1) 主键未含 `dst_node_id`——同一源节点指向同一目标文档、同一 kind 的多条**节点级**引用只能存 1 行（规范文档中「一条 clause 同时参见目标文档的多个条款」是常态），第 2 条 INSERT 直接违主键，M05 的多跳与「证据链」不可实现；(2) `add_ref(src, dst_doc, dst_node, kind)` 与 `remove_ref(src, dst_doc, kind)` 不对称，无法删除单条节点级引用，只能按「文档 + kind」整批删除（误删风险）；(3) `source_ref`（idea §6.4：指向外部 PDF 等叶引用）在 `dst_doc_id NOT NULL` 下没有承载位——外部资源标识被迫塞进文档 ID 列，且该列无外键无格式约束。
- **修复建议**：主键改为 `(src_node_id, dst_doc_id, dst_node_id, kind)` 并用 PG15+ 的 `UNIQUE NULLS NOT DISTINCT`（或引入代理键 `ref_id uuid PRIMARY KEY` + 唯一约束）；`remove_ref` 增 `dst_node: UUID | None` 参数（None 表示文档级引用）；为外部叶引用明确承载（新增 `dst_uri text` 或约定 `dst_doc_id = 'EXT:<path>'`）并在 DDL 注释中写死。

### A6 assets 闭环三缺口：字节存储、读取端点、导入接口

- **Severity**：HIGH
- **位置**：`architecture_specification.md` §4 DDL L279-285（assets）、§3 M02 L85-86（`put_asset`/`get_asset`）、§3 M04 L122-124（「从 assets 表导出到 out_dir/assets/」）；§2 L32（`assets_sync.py`）；§3 M03 L91-117（无资产接口/子命令）；`functional_specification.md` REQ-M02-F06 L107-111、REQ-M03-F05 L137-141
- **问题**：(1) **字节无处安放**——assets 表只有 `asset_id/mime/bytes(bigint)/origin/path`，没有 `bytea` 列，`path` 语义未定义（GigaRAG 源路径？本系统 CAS 路径？），而 `put_asset(data: bytes, mime, origin) -> sha256` 必须写、`get_asset(asset_id) -> bytes` 必须读、M04 还要「从 assets 表导出」——三者都没有可读来源；(2) **读取端点缺失**——11 个 API 端点中没有 `GET /api/v1/assets/{asset_id}`，M08 无法显示 figure（节点里存的是 `asset_ref`=sha256）与 HTML 表格内嵌图片（见 A7）；(3) **导入接口缺失**——§2 列了 `importer/assets_sync.py`，但 §3 M03 无签名、CLI 无子命令，REQ-M03-F05（P1，去 GigaRAG 目录取件/校验 sha256/写 assets/缺失不阻断）没有实现面。
- **修复建议**：(1) 定死字节存储：新增 `data bytea NOT NULL`（小规模最简单）或明确 `ASSET_STORE_DIR` + `path` 语义（`<root>/<sha256>` 两段式寻址）与写入/去重规则，并在 §3 M02 注明 `put_asset` 幂等（同 sha256 不重复写）；(2) 增 `GET /api/v1/assets/{asset_id}`（返回字节 + `Content-Type: mime` + 强缓存），并纳入 M08 依赖的接口面；(3) §3 M03 增 `assets_sync(doc_meta: dict, refs: list[str], src_root: Path) -> AssetSyncResult` 与 CLI 子命令（如 `assets <doc_slug>`），报告 `imported/deduped/missing` 三项计数。

### A7 图片引用有两种形态（HTML `<img>` 80 处），资产与渲染策略未覆盖，且报告计数不准

- **Severity**：HIGH
- **位置**：`research_report.md` L46（图片引用 ×1,019）；`functional_specification.md` REQ-M03-F05 L139、REQ-M04-F01 L145-147、REQ-M04-F02 L149-153；`architecture_specification.md` §3 M04 L122-124；`ADR/ADR-004-渲染引擎与模板策略.md`（P4 零改写）
- **问题**：实测语料图片引用共 **1,099** 处，分两种语法：markdown `![](images/<sha256>.jpg)` **1,019** 处 + HTML `<img src="images/<sha256>.jpg">` **80** 处（CXL 77 / PCIe 2 / HBM4 1）；research_report 的 1,019 只统计了前者，且公式化地传播进 idea B10 与设计文档（「图片引用 1,019 处」）。已逐处复核：**80 处 HTML 引用全部位于 `<table>` 片段内部**（例：CXL `...<td rowspan=1 colspan=1><img src="images/00bbd...jpg"/></td>...`），即 E1 规定必须「零改写」的原子。由此有三重后果：(a) REQ-M03-F05 若按字面实现成只识别 markdown 形态，将漏掉 80 处取件并错误产出 `assets.missing`（资产导入不完整）；(b) M04 要求「图片写为 `assets/<sha256>.jpg` 相对路径」，对 HTML 片段内的 `<img src="images/...">` 要么改写（违反 P4/E1 零改写与 normalize 的内联标记保真断言），要么不改写（产物中路径悬空、图片失效）；(c) 往返断言 `normalize(render(store(parse(src)))) == normalize(src)` 中的「图片引用集」若按路径比较，重写后的 `assets/...` 与源 `images/...` 必然不等。
- **修复建议**：(1) 把 research_report（及派生 B10/§5.2 数字）更正为 1,099（1,019 md + 80 HTML），并在流水线中记录两种形态；(2) REQ-M03-F05 写明抽取规则覆盖 `![](...)` 与 `<img src="...">` 两种语法（含 HTML 实体/引号变体）；(3) 在 E2/M04 明确「HTML 片段内的图片 src 重写属于渲染期产物重写，不算片段改写」，并把 `normalize` 的图片引用集口径定为 **asset_id（sha256）集合**而非路径集合，使往返断言可判定。

### A8 M08 的「仅此接口面」缺 schema 端点与节点读写端点

- **Severity**：HIGH
- **位置**：`architecture_specification.md` §3 M07 L156-181（端点表 + L166「前端契约（TS，M08 依赖：仅此接口面）」）；§3 M06 L147-154；`ADR/ADR-003-表单引擎选型.md` §Decision；`functional_specification.md` REQ-M07-F01 L185-188、REQ-M08-F01 L193-195
- **问题**：REQ-M08-F01 要求「表单由 schema 自动生成（新增原子类型零手写 UI）」，ADR-003 也写「schema 直接从 M01 `schemas` 表加载」，但 **M06/M07 共 11 个端点里没有任何 `/schemas` 端点**——前端根本取不到 JSON Schema，表单引擎没有数据源；同时 M07 端点表没有「节点读写」端点，而 REQ-M07-F01 明列「表单数据（节点读写）」属 M07 五组 API（节点写只在 M06，且被标注为「面向 agent」）。M08 是否允许调用 M06 端点未声明，契约边界不闭合，REQ-M07-F01「M08 仅依赖契约可并行开发」不成立。
- **修复建议**：M07 增 `GET /api/v1/schemas` 与 `GET /api/v1/schemas/{atom_type}`（含变体列表与版本），TS 契约补 `SchemaDTO { typeName, jsonSchema, version }`；节点读写要么在 M07 复述（`GET/POST /api/v1/nodes`），要么显式声明「M08 复用 M06 节点端点，鉴权与 actor 规则相同」，并把 M06 端点表注释从「面向 agent」改为「agent + WebUI 共用」。

### A9 `normalize`/`render_document` 签名无法表达往返判据

- **Severity**：MEDIUM
- **位置**：`architecture_specification.md` §3 M04 L122-130；`functional_specification.md` REQ-M04-F01 L147、REQ-M04-F02 L149-153；`workflow_diagrams.md` WF-1（normalize 往返判定）；idea `design_doc.md` §10
- **问题**：核心验收断言写作 `normalize(render(store(parse(src)))) == normalize(src)`，但 M04 只声明 `normalize(doc_id: str) -> NormalForm` 与 `render_document(doc_id, out_dir) -> RenderResult`：断言的右端需要一个「作用于 markdown 源文本/文件」的 normalize 入口（`src` 是 Path），左端 `render(...)` 返回的是 `RenderResult` 而非 doc_id，且 `RenderResult` 字段未定义（无从知道产物路径/规格化结果字段名）。按现有签名，REQ-M04-F01 的核心验收与 P4 的「往返测试」都无法机械执行。
- **修复建议**：显式定义两个入口（`normalize_markdown(source: str | Path) -> NormalForm` 与 `normalize_doc(doc_id: str) -> NormalForm`），或在 §3 说明 `normalize` 接受「源文本/文件路径/文档 ID」三种形态；同时定义 `RenderResult { doc_id, out_path, normalized: NormalForm, asset_ids: list[str] }`，并在 REQ-M04-F01 写明断言的精确调用式。

### A10 FTS 生成列未进 DDL，且检索用文本字段无处生成

- **Severity**：MEDIUM
- **位置**：`ADR/ADR-005-关键词检索实现.md` §Decision L21、§Risks L35；`architecture_specification.md` §4 DDL L236-238（只有 jsonb_path_ops GIN，无 tsvector）；§3 M01 L54-56；`functional_specification.md` REQ-M05-F02 L167-171
- **问题**：ADR-005 决定用 `to_tsvector('english', coalesce(content->>'text',''))` 的生成列/表达式索引建 GIN，并在 Risks 承认「依赖 M01 约束 `content.text` 必填」；但 (a) §4 的规范 DDL 完全没有该列/索引（现有的 `idx_nodes_content_gin` 是 jsonb_path_ops，只服务 JSONB 包含查询，不加速全文检索）；(b) §3 M01 的 schema 与校验契约没有任何「`content.text` 必填」的约束；(c) E1 规定 table 原子存 `content.fragment`（HTML）+ `content.meta{rows,cols,cells,max_colspan}`，没有 `text` 字段——而语料表格 100% 是 HTML（2,440 块），这些内容经 `content->>'text'` 一律检索不到，REQ-M05-F02「语料抽样关键词可命中预期节点」在表格内容上必然失败。
- **修复建议**：在 §4 DDL 增 `text_tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', coalesce(content->>'text',''))) STORED` + `CREATE INDEX idx_nodes_tsv ON nodes USING gin (text_tsv)`；在 §3 M01 规定 `content.text` 为**检索用必填字段**，并给出 HTML 原子（table/figure）的 text 生成规则（剥离标签后的纯文本，不得原样塞 HTML），与 ADR-005 的 Risks 条目对齐。

### A11 前端契约 camelCase 与后端 snake_case 无序列化口径

- **Severity**：MEDIUM
- **位置**：`architecture_specification.md` §3 M07 L166-181（TS 契约 `nodeId/docId/atomType/parentNodeId/targetEventId/eventId`）与 §3 M01 L63-66、§4 DDL（snake_case 列名）；§6 横切关注点 L310-318（无序列化约定）
- **问题**：TS 契约把线路字段名定为 camelCase，而后端 pydantic 模型与 DDL 全为 snake_case，规格未定义 HTTP JSON 的命名口径（FastAPI/pydantic 默认输出 snake_case，需显式 alias generator 才输出 camelCase）。照现状实现，M08 按契约取 `nodeId` 会得到 `undefined`，REQ-M07-F01/REQ-M08-F01「契约先行、并行开发」在集成时必然返工。
- **修复建议**：二选一定死并写进 §6 横切关注点：「HTTP JSON 一律 snake_case（与 DDL/pydantic 同名，零转换）」或「HTTP JSON 一律 camelCase（后端 `model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)`，并补契约测试断言键名）」。

### A12 CLI 入口与包结构自相矛盾，渲染 CLI 无定义

- **Severity**：MEDIUM
- **位置**：`architecture_specification.md` §2 L32（`importer/`，含 `cli.py`）与 §3 M03 L113-116（`python -m agenticdocer.import ...`）；`user_manual.md` L25-30（另用 `python -m agenticdocer.render`）；§3 M04 L122（只有函数签名）
- **问题**：文档内两处冲突：包目录是 `agenticdocer/importer/`，而 CLI 命令写成 `python -m agenticdocer.import`（`import` 是 Python 关键字，模块无法用常规 import 语句引用，对静态检查/IDE/pickle/重构工具普遍不友好）；此外 user_manual 的 `python -m agenticdocer.render <doc_slug>` 在 §2/§3 均无对应入口（`render/` 未定义 `__main__.py`，M04 只有 `render_document(doc_id, out_dir)`），REQ-M03-F02 与用户手册的快速开始都因此只有一种可选解释。
- **修复建议**：统一为 `agenticdocer.importer`（命令 `python -m agenticdocer.importer parse|review|commit|stats`），在 §2 标注各 CLI 的 `__main__.py` 位置；为 M04 补 CLI 契约（`python -m agenticdocer.render <doc_slug> [--out build/rendered]`）或明确「渲染只经 M06 `POST /api/v1/docs/{id}/render`」并同步删改 user_manual §1。

### A13 parse→review→commit 三步骤缺状态契约

- **Severity**：MEDIUM
- **位置**：`architecture_specification.md` §3 M03 L99-108（`parse_markdown`/`commit(result)`）与 L113-116（CLI）；`functional_specification.md` REQ-M03-F02 L119-123、REQ-M03-F03 L125-129
- **问题**：`parse <file.md>` 只「输出提议清单（json/md）」，没有落盘路径与格式约定；`review <doc_slug>`、`commit <doc_slug>` 只接收 `doc_slug`（未定义是 `SPEC-STD-*` 的 doc_id 还是文件名），而程序化签名是 `commit(result: ParseResult)`（需要内存中的提议集合与审核结论）。评审结论（通过/拒绝/修正）如何持久化、`commit` 如何重建 `ParseResult`、被拒绝项如何留痕，全无规定——REQ-M03-F02「可在无 WebUI 环境完整走通审核」与 REQ-M03-F03「经校验的事务写入」缺少状态契约，实现者只能自造文件格式。
- **修复建议**：定义提议清单的持久化契约（建议 `build/import/<doc_slug>.proposals.json`，字段含 `proposal_id/rule_id/confident/source_lines/atom/decision/edited_atom/reviewed_at`），规定 `parse` 写入、`review` 原地更新并追加审计轨迹、`commit` 读取并调用 `commit(result: ParseResult)`；明确 `doc_slug = frontmatter spec_id`（即 `docs.doc_id`）或把 CLI 参数改为提议文件路径。

### A14 被签名引用的 14 个类型无字段定义

- **Severity**：MEDIUM
- **位置**：`architecture_specification.md` §3 L62-66、L94-108、L126-130、L140-142、L186-195、L200-202
- **问题**：以下类型在签名中被引用但从未定义字段：`Node`（几乎所有方法的返回类型）、`RawFallback`、`UnmappedBlock`、`ParseStats`、`CommitResult`、`RefKind`、`Event`、`Comment`、`TraversalHit`、`SearchHit`、`QualityScope`、`QualityReport`、`RenderResult`、`ExportResult`（`TableNF` 仅一行注释）。it.mas/it.tdd 需要字段级契约才能实现（含返回值的可空性与示例），当前只能靠猜测——这正是 it.arch「接口完整铁律（含 TBD 信号名则 Phase 4 不通过）」要避免的情形。
- **修复建议**：在 §3 末尾增设「类型定义表」，逐条给出字段名/类型/可空性/示例，至少覆盖上述 14 个类型；`RefKind` 定为 4 值枚举；`TraversalHit` 至少含 `{node_id, hops, path: list[RefRef], anchor}`；`SearchHit` 含 `{node_id, anchor, rank}`；`QualityScope` 含 `{kind: 'all'|'doc'|'node', doc_id?}`。

### A15 append-only 强制不可落地（角色不存在、与连接用户不一致）

- **Severity**：MEDIUM
- **位置**：`architecture_specification.md` §4 DDL L294（`REVOKE UPDATE, DELETE ON events FROM agenticdocer_app;`）与 §5 L305（`DATABASE_URL=postgresql+asyncpg://agenticdocer@127.0.0.1:5432/agenticdocer`）；§1 P2 L21（验证方式「REVOKE 审计」）
- **问题**：P2 的 append-only 不变量在库层只靠这条 REVOKE，但 (a) DDL 与部署段都没有 `CREATE ROLE`/`GRANT`，角色 `agenticdocer_app` 不存在，语句不可执行（`alembic upgrade head` 直接报错）；(b) §5 的连接用户是 `agenticdocer`，与 REVOKE 目标角色名不一致——谁是应用角色未定义；(c) 未说明表的属主与非属主前提（属主天然可 UPDATE/DELETE，REVOKE 不构成任何约束），也未提 TRUNCATE 权限与 `events` 的 `SELECT`/`INSERT` 授权。REQ-M02-F03 的库层强制实际为空。
- **修复建议**：补齐权限闭环：`CREATE ROLE agenticdocer_owner LOGIN;`（建表/迁移）、`CREATE ROLE agenticdocer_app LOGIN;`（应用连接，§5 连接串同步改为 `agenticdocer_app`），`GRANT INSERT, SELECT ON events TO agenticdocer_app;`、其余表按需 `SELECT/INSERT/UPDATE/DELETE`、`REVOKE TRUNCATE ON events FROM agenticdocer_app;`，并写明「Alembic 以 owner 角色执行、应用以 app 角色连接」的两套凭据与迁移脚本位置。

### A16 schemas 注册、doc_type 组合规则、terms 词表三者无写入路径

- **Severity**：MEDIUM
- **位置**：`architecture_specification.md` §3 M01 L54-56（只有 `get_json_schema`）、§4 DDL L272-277（schemas）、L287-291（terms）；`functional_specification.md` REQ-M01-F01 L63、REQ-M01-F03 L71-75、REQ-M09-F02 L205-207；`traceability/requirements_matrix.arch.csv` L4、L7、L32
- **问题**：三处「只有表、没有写入路径与载体」：(1) **schemas**——无注册/更新接口（M01 只有读），REQ-M01-F01 的验收「schema 变更产生 `schema` 事件」无从产生，8 类 + 2 变体 schema 的种子方式（代码常量 or alembic data migration）也未规定；(2) **doc_type 组合规则**——REQ-M01-F03 要求「`doc_type → 允许原子类型/必填字段` 可配置并被 M03/M09A 消费」，但 `schemas` 表只有 `(type_name, json_schema, version)`，无承载位、无 API，traceability L4 把该 REQ 指向 §3 M01，而该处无任何相关内容（悬空映射）；(3) **terms**——M09B 术语校验的数据源，但全包没有写入路径（无导入规则、无端点、无 CLI、无种子），REQ-M09-F02 的术语 detector 无数据可查。
- **修复建议**：三者各自补载体与写入路径：schemas 增 `put_schema(type_name, json_schema, actor)` + `PUT /api/v1/schemas/{atom_type}`（写 `schema` 事件）并明确种子迁移编号；doc_type 规则增 `doc_types(doc_type text PRIMARY KEY, allowed_atoms text[], required_fields jsonb)` 表（或在 schemas 中约定 `type_name = 'doc_type:<name>'`），并写入 M01/M09A 契约；terms 增写入路径（M03 解析 glossary 规则 + `POST /api/v1/terms` 或 CLI `python -m agenticdocer.importer terms <file>`）。

### A17 M02 无 docs 级方法，状态流转与文档乐观锁无实现面

- **Severity**：MEDIUM
- **位置**：`architecture_specification.md` §3 M02 L73-88（无任何 docs 方法）、§4 DDL L208-218（docs.version L215）、§3 M07 L160/L164（`GET /api/v1/docs`、`POST /api/v1/docs/{id}/status`）；`functional_specification.md` REQ-M07-F01/F04 L43-46、L185-188
- **问题**：docs 承载「文档元数据 + 状态流转 draft→reviewed→approved + 乐观锁 version」，但 M02 只有 node/ref/event/comment/asset 方法，没有 `get_doc/list_docs/upsert_doc/set_doc_status`；M07 的 `GET /api/v1/docs`、`GET /api/v1/docs/{id}`、`POST /api/v1/docs/{id}/status` 因此没有下层实现面，且状态流转端点的 body 未定义（是否携带 `expectedVersion`？谁写 `doc`+`status` 事件？），`docs.version` 形同虚设。REQ-M07-F04（状态流转，P1）与 REQ-M03-F03 的 docs 写入都缺契约。
- **修复建议**：§3 M02 增 `get_doc(doc_id) -> Doc`、`list_docs(status: str | None) -> list[Doc]`、`upsert_doc(meta: DocIn, expected_version: int | None, actor: str) -> Doc`、`set_doc_status(doc_id, status, expected_version, actor)`（同事务写 `doc`/`status` 事件）；M07 端点表补 `POST /api/v1/docs/{id}/status` 的 body（`{status, expectedVersion}`）与 409 语义。

### A18 事件 payload 形状与重放 fold 语义未定义

- **Severity**：MEDIUM
- **位置**：`architecture_specification.md` §4 DDL L253-254（payload 说明仅一行注释）、§3 M02 L80（`replay(...) -> list[Event]`）；§3 M09 L191-194（`events_consistency` 重放比对）；`functional_specification.md` REQ-M02-F03 L89-93
- **问题**：`events.payload` 的结构只有 DDL 行尾一句注释（字段级 diff `{field:{before,after}}` / ref `{src,dst,kind}`），没有定义各 `op`（create/update/delete/status/add/remove）× 各 `entity`（doc/node/ref/comment/schema）的精确 payload 形状，也没有定义「如何把事件序列折叠回当前态」（create 是否全量、update 的字段路径写法、delete/status 的表达、ref 增删如何反映到 refs 行）。M09B 的 `events_consistency`（重放 ↔ 当前态比对）与 REQ-M02-F03 的验收「对任一节点重放其全部事件 == 当前态」都依赖这套语义，而 `replay()` 只返回事件列表，没有 apply/reconstruct 接口。
- **修复建议**：在 §3 M02 增 `apply_events(entity, entity_id, upto: datetime | None) -> dict`（或 M09B 侧 `reconstruct(node_id, upto) -> NodeSnapshot`）；在 §4 或附录给「op × entity → payload schema + 折叠规则」规范表（含 ref 事件如何从事件流重建 refs 行），供 M09B 巡检、M07 版本历史视图与 M-LR 增量共用。

### A19 每-kind 跳数上限与 `/search` 语义未闭合

- **Severity**：MEDIUM
- **位置**：`architecture_specification.md` §3 M05 L136-142（`KIND_RULES`、`traverse(node_id, hops=1)`）、§3 M06 L154（`GET /api/v1/search?q=&hops=`）；`functional_specification.md` REQ-M05-F01 L161-165、REQ-M05-F02 L167-171；idea `design_doc.md` §6.4
- **问题**：(1) idea §6.4 与 REQ-M05-F01 规定 `traces_to` 默认 1 跳、可扩 2 跳，`composes_from`/`see_also` 仅 1 跳，而 `KIND_RULES` 只编码（方向, 是否参与多跳），不含跳数上限，单一 `hops` 参数无法表达按 kind 的差异——`traverse(node_id, hops=2)` 会把 `see_also` 也走 2 跳（与 §6.4 表冲突），两种实现都可能自称合规；(2) `GET /api/v1/search?q=&hops=` 语义未定义：没有 `node_id` 却带 `hops`，与 M05 的两个函数（`search_text(q, limit)`、`traverse(node_id, hops)`）无法对应，返回类型（`SearchHit` / `TraversalHit` / 联合）与 `limit` 参数都未说明。
- **修复建议**：`KIND_RULES` 值改为 `(direction, multi_hop, max_hops)` 并在 §3 M05 写明「`hops` 按 kind 上限截断」的规则；把 M06 检索端点拆为 `GET /api/v1/search?q=&limit=`（→ `SearchHit[]`）与 `GET /api/v1/nodes/{node_id}/traverse?hops=`（→ `TraversalHit[]`），或在同一端点显式定义 `hops` 与返回结构。

### A20 三条验收标准不可机械验证

- **Severity**：MEDIUM
- **位置**：`functional_specification.md` REQ-M05-F02 L171（「人工标注集」「P95 <200ms」）、REQ-M08-F01..F04 L193-195（「零手写 UI」）；同族 REQ-M02-F01 L81
- **问题**：(1) 「语料抽样关键词可命中预期节点（**人工标注集**）」——该标注集在 arch 包内无定义、无来源、无规模、无命中率阈值，任何实现都无法据此判定通过与否；(2) 「P95 <200ms（B10）」——无测量口径（数据集与规模、查询集合、并发度、冷/热缓存、测量工具与判定脚本），不同实现可各自声明达标；(3) 「表单由 schema 自动生成（**新增原子类型零手写 UI**）」——「零手写」无机械判据。
- **修复建议**：(1) 定义 `tests/fixtures/search_goldenset.yaml`（建议 ≥30 条 `query → 期望 node_id`，一次性人工标注并入库），断言命中率（如 =100% 或 ≥90%）；(2) 定义基准脚本 `tests/perf/test_search_p95.py`（对 7 份语料全量入库后跑固定 query 集 N≥100 次取 P95，环境=本机 PG 16.15），并把阈值写进断言；(3) 定义「零手写」的验收动作：仅向 `schemas` 插入一个新 `atom_type`（不改任何前端文件）后出现可用表单（e2e 断言）。

### A21 Phase 6 交付物 `summary_report.md` 缺失

- **Severity**：MEDIUM
- **位置**：`spec/arch_spec/`（目录中无 `summary_report.md`）；对照 mySkills it.arch `references/output-spec.md`「Phase 6 输出：总结报告」与 `SKILL.md` handoff `transfer_files: {{OUTPUT_DIR}}/summary_report.md`；`spec/arch_spec/.logs/arch-init.log` L2（管线状态停在 Phase 2 记录）
- **问题**：it.arch 的 Phase 6 产物 `summary_report.md`（文档清单 / 关键决策汇总 / 风险清单 / Agent 自检结果 / 下一步行动 / Checklist 完成情况）在本包中完全缺失；它既在 skill 的输出结构清单内，也在 it.mas handoff 的 `transfer_files` 中，完成标准还要求「arch_spec/ 中所有 Phase 产物文件均存在且非空」。缺失使 it.mas 交接没有决策与风险汇总面（`.manifest.json` 亦未落地）。
- **修复建议**：补 `summary_report.md`：按模板给出文档清单（含 traceability CSV）、ADR-001..006 决策汇总、风险清单（合并 idea §11 与本清单 A1–A25）、下一步行动（it.mas 模块顺序 M01/M09A → M02 → M03 → M04 → M06 → M07/M08 → M05 → M09B → M-LR）、Checklist 完成情况（含本清单闭环状态），并写入 `.review/issues.md` 的最终结论。

### A22 frontmatter→docs 列映射与 `doc_type` 取值域未定

- **Severity**：MEDIUM
- **位置**：`architecture_specification.md` §4 DDL L208-218（L210 `doc_type text NOT NULL -- standard | ...`、L212 `meta -- frontmatter 全集（C5）`）；`functional_specification.md` REQ-M03-F01 L115
- **问题**：导入时「frontmatter → docs 行」的映射口径未定义。语料 frontmatter 实测含 `title/source/converted_by/converted_at/reviewed_by/reviewed_at/type/purpose/audience/direction/version/section_meta/spec_type/spec_id/spec_org/spec_revision/status`（共 17 项），但规格没有说明哪一项进 `doc_id`（应为 `spec_id`）、哪一项进 `doc_type`（应为 `spec_type`，其取值域 `standard|lang|tool-manual|product|safety` 只在 DDL 行尾写作注释，无 CHECK）、哪一项进 `source_ref`、其余如何进 `meta`；REQ-M03-F01 又要求「frontmatter 字段按 **C5** 规范校验」，而包内没有给出 C5 字段清单的可解析出处（实际分别散落在 `~/wrk/mySkills/docs/meta-fields-reference.md` 与 `spec/README.md`「frontmatter 规范（v2）」）。M03/M09A 只能自行发明映射，docs 行内容不可复现。
- **修复建议**：在 §4 或 §3 M03 给出映射表（`doc_id ← spec_id`、`doc_type ← spec_type`（并给 CHECK 取值域）、`title ← title`、`source_ref ← source`、`meta ← frontmatter 全集原样保存`）与必填字段清单（引用 `spec/README.md` 的 frontmatter v2 小节），并把 REQ-M03-F01 的「按 C5 规范校验」替换为可枚举的字段级别表。

### A23 悬空章节引用

- **Severity**：LOW
- **位置**：`architecture_specification.md` §1 L22（P3「交付序见 §9」）；`functional_specification.md` REQ-M04-F01 L147（「（§测试策略）」）
- **问题**：arch 规范全文只有 §1–§7，不存在 §9（交付序实际在 idea `design_doc.md` §12「实施顺序」）；functional_specification.md 没有「测试策略」章节（测试策略/normalize 口径在 idea `design_doc.md` §10 与本包 §3 M04）。实现者按 §9、§测试策略 检索会落空，P3 的「import 方向检查」规则无处可依。
- **修复建议**：改为「交付序见 `../idea/design_doc.md` §12（实施顺序，B14）」；把「（§测试策略）」改为「（判定口径见 §3 M04 `normalize()` 与 `../idea/design_doc.md` §10）」。

### A24 用户手册快速开始路径错误

- **Severity**：LOW
- **位置**：`user_manual.md` L25（`uv run python -m agenticdocer.import parse ../spec/standards/IHI0024_AMBA_APB_spec.md`）
- **问题**：语料按组织分子目录存放（实测 `spec/standards/amba/IHI0024_AMBA_APB_spec.md`），命令缺少 `amba/` 层级，照抄即报文件不存在；`../spec/...` 的当前目录基准也未说明（README 的移交流程使用 `spec/standards/<org>/`）。
- **修复建议**：改为 `spec/standards/amba/IHI0024_AMBA_APB_spec.md`，并注明「在仓库根目录（`/home/lxx/wrk/AgenticDocer`）执行」。

### A25 缺 it.arch Phase 4 模板要求的章节

- **Severity**：LOW
- **位置**：`architecture_specification.md`（缺章节）；对照 mySkills it.arch `references/output-spec.md`「Phase 4 输出：系统架构规范」
- **问题**：模板要求的若干章节在本包中缺失：Agent Context（单 Agent 串行 / 模块数量 / 依赖深度）、分层归属声明（各 M 模块的层归属与可见性）、依赖规则矩阵（层间允许/禁止依赖 + 理由）、依赖 DAG 可视化与依赖级别表（本包仅有 §2 目录树与 P3 的一句话原则）、非功能需求量化（B10：≤100k 节点 / ≤500 文档 / PG 查询 P95<200ms / 单文档渲染 <3s / 语义检索 P95<5s）。这些是 it.mas 判定模块边界、import 方向与性能验收的直接输入。
- **修复建议**：按模板补两节：§「Agent Context / 分层归属 / 依赖规则矩阵 / 依赖级别与 DAG」（DAG 可沿用 idea `design_doc.md` §4 依赖图，但需在 arch 包内自洽出现）与 §「非功能需求」（B10 量化目标 + 测量口径，与 A20 的判据对齐）。

## 核对说明（已复核未发现问题 / 边界声明）

- **语料数字复算（对 `spec/standards/*/*.md` 实测）**：8,812,225 B ✓、行数 75,694（`wc -l` 口径）✓、标题行 5,954 ✓、`<table>` 2,440 / `<tr>` 19,763 / `<td>` 79,817 ✓、带 `colspan/rowspan/bgcolor/align` 单元格 57,005 ✓、含 `<sup>/<br>` 行 239 ✓、CXL「Test Steps:」219 /「Fail Conditions:」217 /「Pass Criteria:」214 ✓、PCIe「IMPLEMENTATION NOTE」154（149×`##` + 5×`#`）✓、HBM4「Wrapper Data Register」21 ✓、最大单文件 CXL 3,594,622 B / 31,072 行 ✓。**唯一不符项为图片引用数（见 A7）**。
- **环境事实复算（本机实测）**：PG :5432 在听（容器 `pgvector/pgvector:pg16`）✓、9621/8090/7474/7687 已占用 ✓、node v22.22.3 / npm 10.9.8 / uv 0.12.7 / 系统 python3=3.6.8 ✓、8787 空闲（AB1 端口选择可行）✓、`/mnt/big10T` 不存在 ✓。
- **一致性抽查通过项**：34 条 REQ 与 traceability CSV 34 行一一对应 ✓；DDL 8 表与 A-D2 清单一致 ✓；`format`/`docs.status`/`events.entity`/`refs.kind`/`comments.state` 枚举在 DDL、DTO、REQ 三处一致 ✓；REQ-M09-F02「五类 detector」与 §3 M09 描述一致 ✓；ADR-001/002/003/004/005/006 的 Decision 与正文及 REQ 无相互否定 ✓；P1–P5 与 idea v1.1 的 E1–E20 修订方向一致（E1 直通、E2 资产、E3 事件、E5 事务、E6 批注、E7 锚的策略均已进入 arch 层，但落实度见 A1/A4/A5/A6/A7）✓。
- **Mermaid 渲染未验证**：本机无渲染器（`mmdc`/`mermaid` 均不存在，外网受限无法安装），未做渲染级校验；已人工核对 5 个文件的全部 12 个图块（含 `A & B --> C` 合并边、`-. "label" .->` 虚线带标签、`stateDiagram-v2`、sequence 自消息与括注），**未发现可判定的语法错误**。语义层面一处轻微不一致：`data_flow_diagrams.md` DF-2 中「事务开始」由 M09A 发起，而 §3 的事务归属是 M02，建议按 M02 开事务重画（非阻塞）。

## 复核结论（v1.2，2026-09-16；逐项重读核对）

复核方式：重读 v1.2 全部产物（architecture_specification.md 487 行、functional_specification.md、user_manual.md、research_report.md、data_flow_diagrams.md、ADR-006、summary_report.md）并回查 idea design_doc §5.2/§5.4 回写；对语料/环境数字再次实测复算。

### 已闭环（15 项）

| 项 | 核实点 |
|---|---|
| A1 | `make_anchor(doc_id, chapter_path, title, occurrence_index, body_digest)`（arch L161-168）+ 消歧优先级「正文摘要 sha256[:8] → 同级序号」；ADR-006 §Decision 2、functional REQ-M01-F02 L67-69、idea design_doc §5.4 L171-172 同步（219×Test Steps 可互异） |
| A2 | nodes.status CHECK('active','deleted')（L366）、软删 delete_node 语义（L187-189）、M06 DELETE（L273）、读路径默认过滤（L176-177）、REQ-M02-F05 已改软删口径 |
| A3 | WriteContext（L104-106）贯穿 M02 全部写方法（L176-208）、§6 取值规则（L467）、M06 空 actor→422（L279-280） |
| A4 | comments.version（L408）、update_comment_state(expected_version)（L201-202）、M07 PATCH {state,expectedVersion}（L291） |
| A6 | 资产字节落 ASSET_STORE_DIR CAS（L210/455）、get_asset_path（L205）、M06/M07 增 GET /assets/{id}（L278/L293）、M03 fetch_assets（L225）、assets.path NOT NULL（L427） |
| A11 | §6 序列化口径 alias_generator=to_camel（L468）与 TS camelCase 契约一致 |
| A13 | 提议持久化 data/import_work/<doc_slug>/{proposals.json,review_state.json} + doc_slug 定义（L219-222） |
| A15 | §4.1 角色与 GRANT/REVOKE（L437-447）+ §5 连接串改用 agenticdocer_app（L454） |
| A16（schema 部分） | register_schema(...)（L158）+ DB 映射与 DOC_TYPES 取值域 CHECK（L155/L346） |
| A18 | §3.5 事件载荷与折叠规范表（L331-339）+ apply_events（L197） |
| A19 | KIND_RULES 三元组含 max_hops（L256-259）、traverse 按 kind 截断、M06 拆 /search 与 /nodes/{id}/traverse（L275-277） |
| A20 | functional REQ-M05-F02 goldenset ≥30 条/命中率 ≥90% + tests/perf 口径；REQ-M08 零手写=e2e |
| A21 | summary_report.md 已补（产物清单/决策/风险/自检/下一步） |
| A23 | P3 改指 design_doc §12（L26）、REQ-M04-F01 改指 §3 M04 + design §10 |
| A24 | user_manual §1 路径改为 spec/standards/amba/… + 「在仓库根目录执行」（L27） |
| A25 | §1.2 Agent Context、§1.3 分层与依赖矩阵、§1.4 非功能量化（L30-72） |

### 阻塞残留（10 项，R1–R10）

#### R1（HIGH，原 A5 未完全闭环）refs 主键含可空列，文档级/外部叶引用不可写、SET NULL 永不触发

- **位置**：`architecture_specification.md` L379-389（L382 `dst_node_id uuid REFERENCES nodes(node_id) ON DELETE SET NULL`；L384 `CONSTRAINT refs_pk PRIMARY KEY (src_node_id, dst_doc_id, dst_node_id, kind)`；L386-387 `UNIQUE NULLS NOT DISTINCT` 同列集）
- **问题**：PRIMARY KEY 对其全部列隐含 NOT NULL，因此 L382 声明的可空列 `dst_node_id` 实际被强制非空：(a) 文档级引用（只指目标文档、不指具体节点）与被引用节点后续删除时想保留的「文档级」形态全部写不进去；(b) L389 约定的外部叶引用 `dst_doc_id='EXT:<uri>'`（kind=source_ref，无对应节点）同样无法落库；(c) `ON DELETE SET NULL` 作用在 PK 列上永远不可能成功执行——删除被引用节点会直接报错，而非按声明置空；(d) L386-387 的 UNIQUE 与主键列集完全相同，是冗余约束（主键已更强）。
- **修复建议**：去掉该主键，改为代理主键 `ref_id uuid PRIMARY KEY`（应用侧 UUIDv7）+ `CONSTRAINT refs_unique UNIQUE NULLS NOT DISTINCT (src_node_id, dst_doc_id, dst_node_id, kind)`；`remove_ref` 已按 (src,dst_doc,dst_node,kind) 对称删除，无需再改。若坚持用业务列做主键，则必须把 `dst_node_id` 改为 NOT NULL 并为文档级引用规定哨兵值（不推荐，破坏 SET NULL 语义）。

#### R2（MEDIUM，原 A9 未闭环）往返断言仍不可执行：normalize 无「源 markdown」入口

- **位置**：`architecture_specification.md` L241（`def normalize(doc_id: str) -> NormalForm`）、L237-242（render 入口）、`functional_specification.md` L147（`normalize(render(store(parse(src)))) == normalize(src)`，判定口径指向 §3 M04）
- **问题**：v1.2 补了 `RenderResult`/`NormalForm` 定义，但仍只有 `normalize(doc_id)`：断言右端的 `src` 是 markdown 源（Path/文本），左端 `render(...)` 返回 `RenderResult` 而非 doc_id，且 normalize 只读库内 content（不读渲染产物），因此该断言既写不出来、也验不到渲染层。REQ-M04-F01（P0）与 P4 的往返判据仍不可机械执行。
- **修复建议**：新增 `normalize_markdown(source: str | Path) -> NormalForm`（与 `normalize_doc(doc_id)` 并存），或在 §3 M04 写明 `normalize` 接受「源文本/路径/文档 ID」三形态；REQ-M04-F01 写明精确调用式（如 `normalize_markdown(render_path(r)) == normalize_markdown(src)`）。

#### R3（MEDIUM，原 A7 未完全闭环）P4「HTML 片段零改写」与 M04「片段内 img src 重写」并存，未声明例外

- **位置**：`architecture_specification.md` L27（P4）与 L238-240（M04 docstring：`format=html 片段零改写直通` + `图片（含 HTML 片段内 <img src>，A7）重写为 assets/<sha256>.<ext>`）
- **问题**：同一实现对象上并存两条互斥要求（E1 的零改写 vs 图片路径重写），规格未声明哪一条优先、也未说明重写是否只发生在产物层。it.tdd 无法判定表内 `<img>`（实测 80 处，全部位于 `<table>` 片段内）该不该改。
- **修复建议**：在 P4 与 M04 写明唯一例外：「HTML 片段零改写；唯一例外=片段内图片 `src` 在渲染产物中重写为 `assets/<sha256>.<ext>`（重写仅发生于产物层，库内 content 不变；normalize 的 images 集合以重写前的 asset_id/哈希路径集合比较——L248 已如此定义，补齐 P4 侧即可）」。

#### R4（MEDIUM，原 A14 未完全闭环）仍有 7 个被引用但未定义的类型

- **位置**：`architecture_specification.md` L146/L159（`Violation`）、L178/L180/L181（`Doc`/`DocIn`/`DocStatus`）、L201（`CommentState`）、L210/L225（`AssetSyncReport`）、L317（`QualityScope`）
- **问题**：§3.0 类型块补齐了多数类型，但上述 7 个仍是「只出现、未定义」（`Violation` 在 v1.1 的 M01 块中曾定义，v1.2 重写后丢失）。这些正是 it.mas/it.tdd 需要字段级契约的返回/参数类型。
- **修复建议**：在 §3.0 补：`Violation{rule_id,path,message,fix_hint|None}`、`DocIn{doc_id?,doc_type,title,meta,source_ref?}`、`Doc`（docs 行全集+version/status）、`DocStatus=Literal['draft','reviewed','approved']`、`CommentState=Literal['open','resolved','orphaned']`、`QualityScope{kind:Literal['all','doc','node'],doc_id?}`、`AssetSyncReport{imported:int,deduped:int,missing:list[str]}`。

#### R5（MEDIUM，原 A10 未完全闭环）`content.text 必填` 只在 DDL 注释；HTML 原子如何产出 text 未定义

- **位置**：`architecture_specification.md` L365（`content jsonb NOT NULL, -- 约定：content.text 必填（检索源，A10）`）、L375-377（生成列 `to_tsvector('english', coalesce(content->>'text',''))`）、`ADR/ADR-005-关键词检索实现.md` §Risks；对照 idea §5.1（table 原子 `content.fragment`+`content.meta`）
- **问题**：必填约定未落到 M01 的 schema/校验契约（L150-159 无该规则，v1.2 全文未出现 `fragment`），也未定义 HTML 原子（table/figure）的 text 生成方式。语料表格 100% 为 HTML（2,440 块），若解析器不给这类原子写 `content.text`，FTS 生成列对其为空，REQ-M05-F02 的 goldenset（表格关键词查询）会失败。
- **修复建议**：M01 写明「所有原子 `content.text` 必填（检索源）；HTML 原子由剥离标签后的纯文本生成」，并让 `table`/`figure` 的 JSON Schema 含 `text`（与 E1 的 `fragment`+`meta` 并存，不改直通策略）。

#### R6（MEDIUM，原 A12 未完全闭环）functional_spec 仍写旧 CLI；render 的 doc_slug/doc_id 口径不一

- **位置**：`functional_specification.md` L121（`python -m agenticdocer.import review <doc>`）、`user_manual.md` L30（`uv run agenticdocer-render IHI0024_AMBA_APB_spec`）与 `architecture_specification.md` L242（`agenticdocer-render <doc_id>`）、L227（`agenticdocer-import`/`-m agenticdocer.importer`）
- **问题**：A12 的统一只落在 arch 规范与 user_manual 的 import 命令上：functional REQ-M03-F02 仍规定关键字模块名 `agenticdocer.import`（正是 A12 判定为不可用的形式）；且 `agenticdocer-render` 在手册里收 `doc_slug`（IHI0024_AMBA_APB_spec）而在 M04 契约里收 `doc_id`（SPEC-*），实现者需自行猜测。
- **修复建议**：functional L121 改为 `agenticdocer-import review <doc_slug>`（并注明 doc_slug 定义）；在 §3 M04 或 user_manual 明确 render 接受 `doc_slug` 还是 `doc_id`（建议按 M03 的 doc_slug 统一，或两者都接受）。

#### R7（MEDIUM，原 A17 未完全闭环）M07 有文档列表端点，M02 无 list_docs

- **位置**：`architecture_specification.md` L286（`GET /api/v1/docs` 文档列表）与 M02 方法集 L174-208（有 get_doc/create_doc/update_doc_status，无 list_docs）
- **问题**：按本规范的分层（M07 仅依赖 M01/M02/M04，M02 是唯一 DB 访问层），文档列表没有实现面；REQ-M07-F01 的「文档列表」无法按契约落地。
- **修复建议**：M02 增 `list_docs(status: DocStatus | None = None) -> list[Doc]`（可附分页参数），或在 M07 表注明该端点由 M02 不承担、改由何处提供（不建议绕过分层）。

#### R8（MEDIUM，原 A8 未完全闭环）`/api/v1/nodes` 在 M06 与 M07 重复声明；新 schema 端点无 TS 契约

- **位置**：`architecture_specification.md` L270/L272（M06 表）与 L287（M07 表，注明「与 M06 同契约；A8 归属 M07」）；TS 契约 L299-311 无 `SchemaDTO`（对照 L288 `GET /api/v1/schemas/{atom_type}`）
- **问题**：同一条路径同时出现在两个模块的端点表里且分属两个 router（`agent_api/router.py`、`webui_api/router.py`），归属自相矛盾（表内声称归 M07，M06 表仍保留注册项），实现期易出现重复路由/OpenAPI 重复 path；同时 M08 的「唯一接口面」TS 契约没有 schema 响应类型，表单引擎取到 JSON 后的字段名（camelCase）只能靠猜。
- **修复建议**：§3 M06 行改为引用式（如「节点读写端点定义见 M07；M06 复用同 handler」）或明确由 `app.py` 只注册一次；在 TS 契约块补 `export interface SchemaDTO { typeName: string; jsonSchema: Record<string, unknown>; version: number }`。

#### R9（MEDIUM，新引入）悬空引用「§3.4」（映射实际在 §6）

- **位置**：`architecture_specification.md` L345（`-- SPEC-*（映射见 §3.4 A22）`）、L471（`（A22 见 §3.4）`）、L239（`frontmatter 按 §3.4 映射回写`）；实际映射在 L475（§6 横切关注点）——§3 只有 `3.0` 与 `3.5`，无 §3.4
- **问题**：A22 的修复文档在同一修订轮内引入了新的悬空章节引用（与 A23 同类缺陷），三处引用均指向不存在的章节，读者/实现者无法定位映射表；`§3` 的编号也出现 3.0→3.5 的空档。
- **修复建议**：把 L475 的映射块移到 §3 内并编为 `### 3.4 frontmatter → docs 映射（A22）`（同时消掉编号空档），或把 L345/L471/L239 的引用统一改为 `§6`。

#### R10（MEDIUM，原 A16 未完全闭环）terms 无写入路径；doc_type 组合规则载体仍缺

- **位置**：`architecture_specification.md` L16（v1.2 修订声称「schema/terms 写入路径（A16）」）、L430-433（terms DDL）、L318（M09B terms detector）；`functional_specification.md` L205（REQ-M09-F02 术语校验数据源 = `terms` 表）
- **问题**：schema 的写入路径已落（L158 `register_schema`），但 `terms` 仍只有建表语句与 detector 引用：没有导入规则、没有 API/CLI、没有种子数据，M09B 的术语校验无数据可查（REQ-M09-F02，P2/阶段 3）；`doc_type → 允许原子类型/必填字段` 的规则模型同样只有取值域（L155 `DOC_TYPES`）而无载体（summary L43 的 Q6 延后登记可接受，但 L16 的「已补」表述与实际不符）。
- **修复建议**：补 terms 写入路径（M03 `glossary`/`normative-keyword` 解析规则 + `POST /api/v1/terms` 或 CLI `agenticdocer-import terms <file>`，或明确「随 M09B 由人工 SQL 种子」）；把 L16 的修订措辞改为「terms 载体=DDL，写入路径随 M09B 阶段定义」，doc_type 规则注明 Q6 延后。

### 非阻塞残留（L1–L9）

| ID | 位置 | 说明 |
|---|---|---|
| L1 | functional_specification.md L8 / user_manual.md L8 / research_report.md L8 / ADR-006 L8 / data_flow_diagrams.md L8 | 版本号未随 v1.2 同步（arch 与 summary 已 1.2.0，其余仍 1.1.0，尽管其中多数文件本轮被修订） |
| L2 | summary_report.md L22 vs L36 | 「DDL 9 表」与「8 业务表」自相矛盾（实际 8 表：docs/nodes/refs/events/comments/schemas/assets/terms） |
| L3 | architecture_specification.md L475 | 「17 字段 + spec 专有四字段必填」重复计数——实测语料 frontmatter 共 17 字段且已含 `spec_id/spec_type/spec_org/spec_revision` |
| L4 | architecture_specification.md L440-447 | 属主角色 `agenticdocer` 只在注释中出现、无 `CREATE ROLE`；缺 `ALTER DEFAULT PRIVILEGES`（后续迁移新建表将无 app 角色授权） |
| L5 | architecture_specification.md L256-263 | M05 未声明过滤 `status='deleted'`（软删后遍历/检索仍可能命中已删节点） |
| L6 | functional_specification.md L139 / L86 | REQ-M03-F05 未同步「md + HTML `<img>` 两语法」；REQ-M02-F02 的 ref payload 写作 `{op, src, dst, kind}` 与 §3.5 `{src, dst_doc, dst_node, kind}` 字段名不一致 |
| L7 | architecture_specification.md L197 | `apply_events` 仅产出 `NodeSnapshot`，doc/ref/comment/schema 的折叠规则（§3.5）无对应入口 |
| L8 | user_manual.md L43 | 锚示例 `SPEC-STD-AMBA-APB#3.2.1` 未含新格式的 `·slug(title)` 段 |
| L9 | data_flow_diagrams.md L48-49 | DF-2 中渲染结果仍由 M04 直达 Agent（未经过 M06 返回）；事务归属已按 M02 修订 |

## 复核结论（第 2 轮，R1–R10 / L1–L9 闭环核对）

复核方式：重读 v1.2 定稿的全部产物（architecture_specification.md 505 行）并逐项比对声明；除下列 4 项外，R1–R10 与 L1–L9 均已核实闭环。

### 已闭环（R1–R10，10/10）

| 项 | 核实点 |
|---|---|
| R1 | refs 改为代理主键 `ref_id uuid PRIMARY KEY`（arch L383），`dst_node_id` 可空（L385）+ `refs_unique UNIQUE NULLS NOT DISTINCT (src_node_id,dst_doc_id,dst_node_id,kind)`（L387-388），冗余主键已删，注释明确「文档级引用 dst_node_id IS NULL 合法」；ON DELETE SET NULL 可生效 |
| R2 | M04 增 `normalize_markdown(source: str \| Path)`（L254）与调用式注释（L255）——但调用式本身仍有残留问题，见 N2 |
| R3 | P4（L27）已声明唯一例外：产物层图片 src 重写（含片段内 `<img>`），normalize.images 以重写前哈希路径集合为口径 |
| R4 | §3.0 补齐 `Violation`（L148）/`DocIn`/`Doc`/`DocStatus`（L149-151）/`CommentState`（L152）/`AssetSyncReport`（L153）/`QualityScope`（L154） |
| R5 | M01 增 `derive_text(atom_type, content)`（L167-169：HTML 去标签、表格按行列序拼接）+「content.text 必填（FTS 依赖）」约束 |
| R6 | functional REQ-M03-F02（L121）改为 `agenticdocer-import review <doc_slug>`（等价 `python -m agenticdocer.importer review`）；user_manual L30 改为 `agenticdocer-render SPEC-STD-AMBA-APB`（doc_id）并注明 doc_slug 仅导入工作区 |
| R7 | M02 增 `list_docs(status: DocStatus \| None)`（L192） |
| R8 | M07 节点行改为「**复用 M06 端点**（同一实现集）」（L306）；TS 契约补 `SchemaDTO`（L322） |
| R9 | 三处引用已改指 §6（M04 docstring L247、docs DDL 注释 L361、§6 ID 行 L486）；映射表标题改为「C5 十七字段，含 spec 专属 4 项」（L491） |
| R10 | M01 增 `upsert_term(...)`（L170-171），三路径（M03 导入 definition 原子 / M07 API / 种子 `data/terms_seed.yaml`）——其中「M07 API」路径未在 M07 端点表落行，见 N3 |

### 已闭环（L1–L9，9/9）

L1 五份文件版本已升 1.2.0（functional L8 / user_manual L8 / research_report L8 / ADR-006 L8 / data_flow L8）；L2 summary_report L22 已改「DDL 8 表」；L3 映射标题与必填清单去重（C5 十七字段，含 spec 专属 4 项）；L4 §4.1 补 `CREATE ROLE agenticdocer`（属主）+ `ALTER DEFAULT PRIVILEGES FOR ROLE agenticdocer`（L~449）；L5 M05 `traverse`/`search_text` 均注明默认过滤 `status='deleted'`（L~270-272）；L6 functional L85 的 ref payload 已改 `{src, dst_doc, dst_node, kind}`（与 §3.5 一致）；L7 `apply_events(entity, events) -> NodeSnapshot | dict`（L207）；L8 user_manual L43 锚示例已含 `·slug` 与 `~正文摘要` 说明；L9 DF-2 改为 `R-->>S: RenderResult` → `S-->>A: 结果 + 产物路径`（经 M06 返回，data_flow L63-64）。（workflow_diagrams.md 与 clarifications.md 本轮未修订，保留 1.1.0，可接受。）

### 本轮阻塞残留（2 项，N1–N2）

#### N1（MEDIUM，新引入）悬空引用「§5.2」（权限与角色实际在 §4.1）

- **位置**：`architecture_specification.md` L25（P2 行的验证方式：`事务注入测试；角色 REVOKE 审计（§5.2）`）
- **问题**：本规范只有 §5「部署与运行」（单一代码块，无子节），角色与权限在 §4.1（`### 4.1 角色与权限（A15）`），不存在 §5.2。P2 的库层强制手段（REVOKE 审计）无法按图索骥——与已修复的 R9（§3.4）属同一类悬空引用，是本轮修订引入。
- **修复建议**：把 `（§5.2）` 改为 `（§4.1 角色与权限）`；全包再扫一遍 `§\d+\.\d+` 形式引用，确保每个子节引用都真实存在。

#### N2（MEDIUM，原 A9/R2 未完全闭环）往返判据两份文档不一致，且调用式丢掉了渲染环节

- **位置**：`functional_specification.md` L147（`验收标准：normalize(render(store(parse(src)))) == normalize(src)`，判定口径指向 §3 M04 `normalize()`）与 `architecture_specification.md` L253-255（`normalize(doc_id)`=库侧、`normalize_markdown(source)`=源侧、`往返断言调用式（REQ-M04-F01）：normalize(doc_id) == normalize_markdown(src)`）
- **问题**：(a) 同一验收标准在 REQ 与架构两处写成**两个不同的表达式**：functional 的 `normalize(render(store(parse(src))))` 对新签名而言不成立（`normalize` 已明确为「库侧（节点树）」、只收 doc_id，`render(...)` 返回 `RenderResult` 而非 doc_id/text，无法入参）；(b) 架构给出的新调用式 `normalize(doc_id) == normalize_markdown(src)` 只比较「已入库的库侧规范化表示」与「源 markdown 规范化表示」，**不再经过渲染产物**——而 P4 的核心不变量（HTML 片段零改写直通、片段内 `<img>` 重写规则、frontmatter 回写）只有在渲染产物上才可被破坏，`normalize` 读库侧节点树时这些缺陷不会被该断言检出，REQ-M04-F01（P0）的关键验收因此出现检测盲区。
- **修复建议**：(a) 把 functional L147 改为与 §3 M04 完全一致的调用式；(b) 补足渲染环节，例如「`normalize_markdown(<产物文件>) == normalize_markdown(src)`」（产物侧 normalize，images 集合按 asset_id/重写前哈希路径集合比较）或「`normalize(doc_id) == normalize_markdown(<产物文件>)` 二式并列」，并在 §3 M04 与 REQ-M04-F01 写明两式的各自适用范围。

### 本轮非阻塞残留（2 项，N3–N4）

| ID | 位置 | 说明 |
|---|---|---|
| N3 | architecture_specification.md L170-171 vs M07 端点表 L303-311 | `upsert_term` 注释把「M07 API」列为 terms 写入路径之一，但 M07 端点表无 terms 端点；种子文件 `data/terms_seed.yaml` 也未出现在 §2 目录映射/§5 环境清单中（不影响 M09B 阶段实现，建议补行或改注「随 M09B 定义」） |
| N4 | functional_specification.md L139 | REQ-M03-F05 正文/验收仍只描述 `images/<sha256>.jpg` 引用一种写法，未同步架构 M03 已覆盖的两种语法（md `![](...)` + HTML `<img src>`）；该 REQ 是 P1 且其验收（抽样哈希一致 / 缺失清单）直接影响 80 处 HTML 内嵌图片，建议补一句 |

## 结论

存在 2 个阻塞残留（N1–N2），非阻塞残留 2 项（N3–N4）。除 N1/N2 外，首轮 A1–A25 与复核 R1–R10 / L1–L9 均已闭环。
