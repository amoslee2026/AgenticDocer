---
title: 架构规范 — 芯片设计知识库系统
type: composite
purpose: architecture
audience: both
direction: input
status: approved
version: "1.2.0"
section_meta: "@meta"
---

# 架构规范

生成：2026-09-16（it.arch Phase 4）。上游：`functional_specification.md`、`../idea/design_doc.md` v1.1.0。

> **v1.2 修订**（A1–A25 闭环）：锚策略（A1）、软删语义（A2）、WriteContext/actor（A3）、comments 乐观锁（A4）、refs 主键（A5）、资产存储与端点（A6）、HTML `<img>` 覆盖（A7）、M08 schema 端点（A8）、渲染签名（A9）、FTS 生成列（A10）、序列化口径（A11）、CLI 统一（A12）、提议持久化（A13）、类型定义补全（A14）、角色/GRANT（A15）、schema/terms 写入路径（A16）、docs 级方法（A17）、事件 fold 规范（A18）、跳数语义（A19）、可测判据（A20，落在 functional_spec）、summary_report（A21）、frontmatter 映射（A22）、悬空引用（A23）、手册路径（A24）、Agent Context/分层/依赖矩阵/非功能（A25）。

## 1. 原则、Agent Context 与依赖规则

### 1.1 原则（可验证的不变量）

| # | 原则 | 验证方式 |
|---|---|---|
| P1 | 结构化库为唯一权威源；人类可读格式均为渲染产物 | 无代码路径从渲染产物反向写库 |
| P2 | 一切写入 = 事件 + 实体同事务；events 仅追加 | 事务注入测试；角色 REVOKE 审计（§5.2） |
| P3 | 依赖单向：模块仅依赖已交付模块；**交付序见 `../idea/design_doc.md` §12（B14）** | import 方向 lint 规则（§1.3 矩阵） |
| P4 | HTML 片段与内联标记原样直通（零改写）；**唯一例外**：产物层图片 `src` 重写（含片段内 `<img>`，A7）——normalize.images 以重写前哈希路径集合为口径 | 往返测试（normalize 等价，§3 M04） |
| P5 | 口径唯一：normalize()、rule_id、anchor 各为单一判定口径 | 各自单测固定 |

### 1.2 Agent Context

| 项 | 值 |
|---|---|
| 开发形态 | 单 Agent 串行实现（模块按 M 编号交付序）；WebUI 前端可并行（仅依赖 §3 M07 契约） |
| 模块数量 | 9 模块（M01–M09）+ 1 边界（M-LR）≤10 |
| 依赖深度 | 最长链 M01 → M02 → M03 → M04 → M06/M07（深度 5） |
| 参考文档 | 本规范 + `../idea/design_doc.md`（设计依据）+ `../idea/clarifications.md`（B/Q 台账） |

### 1.3 分层归属与依赖规则矩阵

| 层 | 模块 | 可见性 |
|---|---|---|
| L1 模型层 | M01 | 全部可见（无依赖） |
| L2 存储层 | M02 | 依赖 L1 |
| L3 领域服务层 | M03, M04, M05, M09 | 依赖 L1–L2 |
| L4 接口层 | M06, M07 | 依赖 L1–L3 |
| L5 前端 | M08 | 仅依赖 M07 的 OpenAPI 契约 |
| L6 边界 | M-LR | 依赖 L2/M04（导出），被集成方消费 |

**允许依赖（√）/禁止（×）**：

| 从 ↓ / 到 → | M01 | M02 | M03 | M04 | M05 | M09 | M06 | M07 | M08 | M-LR |
|---|---|---|---|---|---|---|---|---|---|---|
| M02 | √ | — | × | × | × | × | × | × | × | × |
| M03 | √ | √ | — | × | × | √(9A) | × | × | × | × |
| M04 | √ | √ | × | — | × | × | × | × | × | × |
| M05 | × | √ | × | × | — | × | × | × | × | × |
| M09 | √ | √ | × | √(9B) | × | — | × | × | × | × |
| M06 | √ | √ | × | √ | × | √(9A) | — | × | × | × |
| M07 | √ | √ | × | √ | × | × | × | — | × | × |
| M08 | × | × | × | × | × | × | × | √(HTTP) | — | × |
| M-LR | × | √ | × | √ | × | × | × | × | × | — |

### 1.4 非功能需求（量化，与 B10 对齐）

| 指标 | 目标 | 测量口径 |
|---|---|---|
| 规模 | ≤100k 节点、≤500 文档（条款级粒度基线） | 库内计数（`SELECT count(*)`） |
| 点查延迟 | PG 查询 P95 <200ms | 基准脚本 `tests/perf/`：7 份语料全量入库后固定查询集（≥100 次）取 P95，本机 PG 16.15 |
| 渲染 | 单文档 <3s | 同基准脚本（最大文档 CXL 3.59MB） |
| 语义检索（联调后） | P95 <5s | LightRAG 侧基准 |
| 解析 | 规则覆盖率 ≥95%；零静默丢弃 | `import stats` 输出（口径见 functional_spec REQ-M03-F01/F04） |

## 2. 代码结构与模块映射

```
src/agenticdocer/
├── model/       # M01（schemas.py, anchors.py, atoms.py, doc_types.py）
├── store/       # M02（db.py, nodes.py, refs.py, events.py, comments.py, assets.py, docs.py）
├── importer/    # M03（parser/, rules/, cli.py, proposals.py, assets_sync.py）
├── render/      # M04（renderer.py, normalize.py, __main__.py）
├── retrieve/    # M05（traverse.py, search.py）
├── agent_api/   # M06（router.py）
├── webui_api/   # M07（router.py）
├── m09/         # M09（engine_9a.py, quality_9b/）
├── mlr/         # M-LR（export.py, stream.py）
├── cli.py       # 统一 CLI 装配（import/render/stats 子命令）
└── app.py       # FastAPI 装配（含 M08 静态挂载）
webui/           # M08（React+TS+Vite）
tests/           # 单元/集成/e2e + fixtures/search_goldenset.yaml + perf/
alembic/         # DDL 迁移（AB4）
```

## 3. 模块接口契约

### 3.0 公共类型定义（A14）

```python
# agenticdocer/model/types.py（片段）
UUID7 = UUID                     # UUIDv7：应用侧生成（时间有序）

class WriteContext(BaseModel):   # A3：一切写入的身份与来源
    actor: str                   # 非空；取值规则见 §6
    source: Literal["agent","webui","cli","importer","system"]

class NodeIn(BaseModel):
    node_id: UUID7 | None; doc_id: str; atom_type: str
    format: Literal["md","html","text"] = "md"
    ordinal: int; parent_node_id: UUID7 | None; level: int | None
    anchor: str; content: dict
class Node(NodeIn):
    node_id: UUID7; status: Literal["active","deleted"]; version: int
    created_at: datetime; updated_at: datetime

class RawFallback(BaseModel):    # 未映射块兜底（note/code）
    atom_type: Literal["note","code"]; format: Literal["html","md"]
    text: str; source_lines: tuple[int,int]
class UnmappedBlock(BaseModel):
    source_lines: tuple[int,int]; reason: str; fallback: RawFallback

class Proposal(BaseModel):
    proposal_id: str             # 稳定（doc_slug + 源行区间）
    rule_id: str; confident: bool
    source_lines: tuple[int,int]
    atom: NodeIn | RawFallback
class ParseStats(BaseModel):
    total_blocks: int; rule_covered: int; fallback: int; pending: int
class ParseResult(BaseModel):
    doc_meta: dict; proposals: list[Proposal]; unmapped: list[UnmappedBlock]; stats: ParseStats

class RefKind = Literal["traces_to","see_also","composes_from","source_ref"]
class Event(BaseModel):
    event_id: UUID7; entity: Literal["doc","node","ref","comment","schema"]
    entity_id: str; op: Literal["create","update","delete","status","add","remove"]
    payload: dict; actor: str; ts: datetime
class Comment(BaseModel):
    comment_id: UUID7; node_id: UUID7; target_event_id: UUID7 | None
    body: str; state: Literal["open","resolved","orphaned"]
    author: str; version: int; ts: datetime
class NodeSnapshot(BaseModel):   # apply_events 折叠结果（A18）
    node: Node | None; history: list[Event]
class SearchHit(BaseModel):     node_id: UUID7; doc_id: str; anchor: str; score: float
class TraversalHit(BaseModel):  node_id: UUID7; doc_id: str; anchor: str; hops: int; via: list[RefKind]
class RenderResult(BaseModel):  doc_id: str; out_path: str; assets_exported: int
class CommitResult(BaseModel):  doc_id: str; nodes_created: int; refs_created: int; stats: ParseStats
class QualityReport(BaseModel): detector_id: str; violations: list[Violation]
class ExportResult(BaseModel):  out_path: str; docs: int; nodes: int
class Violation(BaseModel):     rule_id: str; path: str; message: str; fix_hint: str | None
class DocIn(BaseModel):         doc_id: str; doc_type: str; title: str; meta: dict; source_ref: str | None
class Doc(DocIn):               status: "DocStatus"; version: int; created_at: datetime; updated_at: datetime
DocStatus = Literal["draft","reviewed","approved"]
CommentState = Literal["open","resolved","orphaned"]
class AssetSyncReport(BaseModel): fetched: int; missing: list[str]; total_refs: int
class QualityScope(BaseModel):  doc_ids: list[str] | None; detectors: list[str] | None
```

### M01 内容模型

```python
ATOM_TYPES = ("clause","definition","table","figure","code","example","note","cross_ref")
ATOM_VARIANTS = ("table.register_field","figure.state_machine")
DOC_TYPES = ("standard","lang","tool-manual","product","safety")     # A22 取值域（Q6 随首个非 standard 扩组合规则）

def get_json_schema(atom_type: str) -> dict: ...                     # schemas 表缓存加载
def register_schema(atom_type: str, schema: dict, version: int, ctx: WriteContext) -> None: ...  # A16 写入路径
def validate(atom_type: str, content: dict) -> list[Violation]: ...  # 委托 M09A
def derive_text(atom_type: str, content: dict) -> str: ...           # A10/R5：生成 content.text（必填）
    """HTML 片段 → 纯文本（去标签；表格按行列序拼接单元格文本）；md/文本类原样。
       约束：M01 保证一切节点 content.text 非空（FTS 生成列与检索依赖）。"""
def upsert_term(term: str, definition_node_id: UUID7 | None, kind: Literal["glossary","normative-keyword"],
                ctx: WriteContext) -> None: ...                      # R10：terms 写入路径（M03 导入 definition 原子、M07 API、种子文件 data/terms_seed.yaml）

def make_anchor(doc_id: str, chapter_path: list[str], title: str,
                occurrence_index: int, body_digest: str) -> str:     # A1 修订
    """锚 = <doc_id>#<章节号路径>·<slug(title)>；消歧优先级：
       ① 同父路径+同标题唯一 → 无后缀；
       ② 重复 → 追加 '~' + body_digest[:8]（正文摘要，非标题）；
       ③ 正文亦相同 → 追加 '~' + occurrence_index（同级稳定计数）。
       稳定性：仅依赖文档内容与同级计数；同一源文档重复解析结果逐字节一致；
       源文档改版时按 (章节号路径, slug) 匹配 + 人工确认迁移（design_doc §5.4）。"""
```

### M02 存储层（所有写方法统一携带 `ctx: WriteContext`，A3）

```python
class Storage:
    # 读
    async def get_node(self, node_id: UUID7) -> Node: ...            # 默认过滤 status='active'（A2）
    async def get_doc_nodes(self, doc_id: str, include_deleted: bool = False) -> list[Node]: ...
    async def get_doc(self, doc_id: str) -> Doc: ...
    # 文档级写（A17）
    async def list_docs(self, status: DocStatus | None = None) -> list[Doc]: ...   # R7
    async def update_doc_status(self, doc_id: str, status: DocStatus,
                                expected_version: int, ctx: WriteContext) -> Doc: ...  # 409
    # 节点写
    async def upsert_node(self, node: NodeIn, expected_version: int | None,
                          ctx: WriteContext) -> Node: ...            # 409；写 node 事件（同事务）
    async def delete_node(self, node_id: UUID7, expected_version: int,
                          ctx: WriteContext) -> None: ...            # A2：软删 seen below
    """delete_node 语义（A2）：UPDATE nodes SET status='deleted', version+1（乐观锁校验）；
       写 node 事件 op=delete（payload 含 before snapshot）；同事务 orphan_comments(node_id)。"""
    # 引用边（A5）
    async def add_ref(self, src: UUID7, dst_doc: str, dst_node: UUID7 | None,
                      kind: RefKind, ctx: WriteContext) -> None: ... # 写 ref 事件（payload {op:add,src,dst_doc,dst_node,kind}）
    async def remove_ref(self, src: UUID7, dst_doc: str, dst_node: UUID7 | None,
                         kind: RefKind, ctx: WriteContext) -> None: ...  # 对称参数
    # 事件（A18）
    async def replay(self, entity: str, entity_id: str, upto: datetime | None = None) -> list[Event]: ...
    def apply_events(self, entity: str, events: list[Event]) -> NodeSnapshot | dict: ...  # L7：node→NodeSnapshot；doc/comment→dict；ref/schema→行集重建（规则见 §3.5）
    # 批注（A4 乐观锁）
    async def create_comment(self, node_id: UUID7, body: str,
                             expected_version: int | None, ctx: WriteContext) -> Comment: ...
    async def update_comment_state(self, comment_id: UUID7, state: CommentState,
                                   expected_version: int, ctx: WriteContext) -> Comment: ...  # 409
    async def orphan_comments(self, node_id: UUID7) -> None: ...      # delete_node 内部调用
    # 资产（A6）
    async def put_asset(self, data: bytes, mime: str, origin: str) -> str: ...  # -> asset_id(sha256)
    async def get_asset_path(self, asset_id: str) -> Path: ...        # 文件系统 content-addressed
    async def list_missing_assets(self, doc_id: str | None = None) -> list[str]: ...
```

**资产字节存储（A6）**：`assets` 表存元数据，字节落**文件系统 content-addressed 目录** `ASSET_STORE_DIR`（默认 `data/assets/<sha256[:2]>/<sha256>.<ext>`）；`assets.path` 记录相对路径；`get_asset_path` 校验存在性。读取端点见 M06/M07（§3 各表）。M03 导入接口见 `assets_sync.fetch_assets(refs, source_root) -> AssetSyncReport`。

### M03 导入解析

```python
# 接口
def parse_markdown(path: Path, doc_slug: str) -> ParseResult: ...
async def commit(result: ParseResult, ctx: WriteContext) -> CommitResult: ...   # 经 M09A -> M02 事务

# 提议持久化（A13）：工作目录 data/import_work/<doc_slug>/
#   proposals.json   解析输出（含 proposal_id）
#   review_state.json 审核状态（每 proposal：pending/accepted/rejected/amended(含修正 JSON)）
# doc_slug 定义：源文件名去 .md（如 IHI0024_AMBA_APB_spec）

# 资产同步（A6/A7：覆盖 md 引用与 HTML <img src>）
def fetch_assets(refs: list[str], source_root: Path) -> AssetSyncReport: ...

# CLI（A12 统一入口：console script `agenticdocer-import` 与 `python -m agenticdocer.importer` 等价）
#   parse  <src.md> [--doc-slug S]           → proposals.json
#   review <doc_slug>                        → 交互审核（更新 review_state.json）
#   commit <doc_slug> [--actor importer]     → 校验 + 入库 + 统计
#   stats  <doc_slug>                        → 规则覆盖率/兜底率/待确认条数
```

### M04 渲染引擎

```python
def render_document(doc_id: str, out_dir: Path) -> RenderResult:
    """节点树（status='active'，按 ordinal）→ Markdown：format=html 片段零改写直通；
    frontmatter 按 §6（frontmatter 映射）回写；图片（含 HTML 片段内 <img src>，A7）重写为
    assets/<sha256>.<ext> 相对路径，并从资产存储导出至 out_dir/assets/。"""
def normalize(doc_id: str) -> NormalForm: ...                  # 库侧（节点树）
def normalize_markdown(source: str | Path) -> NormalForm: ...  # 源侧（markdown 文本）
# 往返断言调用式（REQ-M04-F01）：normalize(doc_id) == normalize_markdown(src)
# 渲染入口：`agenticdocer-render <doc_id>` 或 `python -m agenticdocer.render`（入参为 doc_id=spec_id）

class NormalForm(BaseModel):
    headings: list[tuple[int, str]]          # (level, text)
    tables: list[TableNF]                    # TableNF(rows, cols, cells: list[list[str]])
    code_blocks: list[str]
    images: list[str]                        # 含 HTML <img> 的 src 集合（重写前哈希路径集合）
    lists: list[list[str]]
    inline_markers: list[str]
```

### M05 图遍历与检索

```python
KIND_RULES: dict[RefKind, tuple[Literal["up","down","both"], bool, int]] = {   # (方向, 参与多跳, 最大跳数) A19
    "traces_to": ("up", True, 2), "composes_from": ("down", True, 1),
    "see_also": ("both", True, 1), "source_ref": ("up", False, 0),
}
def traverse(node_id: UUID7, hops: int = 1) -> list[TraversalHit]:
    """hops 按各 kind 的 max_hops 截断（hops=2 仅扩 traces_to）；去重保留最短路径；环截断；
    排序：跳数 → doc 序 → ordinal；默认过滤 status='deleted' 节点（L5）。"""
def search_text(q: str, limit: int = 50) -> list[SearchHit]: ...   # FTS（ADR-005），返回含 score；默认过滤 deleted（L5）
```

### M06 Agent 接口（HTTP）

| 方法/路径 | 语义 | 关键错误 |
|---|---|---|
| `GET /api/v1/nodes/{node_id}` | 节点读（含 version） | 404 |
| `GET /api/v1/docs/{doc_id}/nodes` | 文档节点树（默认 active） | 404 |
| `POST /api/v1/nodes` | 结构化写入（NodeIn + expected_version） | 422/409 |
| `DELETE /api/v1/nodes/{node_id}?expected_version=` | **软删**（A2，写 delete 事件 + orphan 批注） | 404/409 |
| `POST /api/v1/refs` / `DELETE /api/v1/refs` | 引用边增删（body: src,dst_doc,dst_node,kind） | 404/422 |
| `GET /api/v1/nodes/{node_id}/traverse?hops=` | 多跳遍历（→ TraversalHit[]） | 404 |
| `GET /api/v1/search?q=&limit=` | 关键词检索（→ SearchHit[]） | — |
| `GET /api/v1/assets/{asset_id}` | 资产字节流 | 404 |
| `POST /api/v1/docs/{doc_id}/render` | 触发渲染 | 404 |

**身份（A3）**：写端点要求 `X-Actor` 请求头（非空；缺失 → 422）；映射 `WriteContext(source="agent")`。

### M07 WebUI API

| 方法/路径 | 语义 |
|---|---|
| `GET /api/v1/docs` / `GET /api/v1/docs/{id}` | 文档列表/详情（含 version/status） |
| `GET/POST /api/v1/nodes` 等 | **复用 M06 端点**（同一实现集；source="webui" 由 X-Actor 决定；表单与 agent 共用契约，R8） |
| `GET /api/v1/schemas/{atom_type}` | **schema 端点**（表单引擎数据源；A8） |
| `GET /api/v1/events?entity=&entity_id=&since=` | 结构化 diff 数据源 |
| `GET /api/v1/events/replay?node_id=&upto=` | 版本历史（apply_events 折叠） |
| `POST /api/v1/comments` / `PATCH /api/v1/comments/{id}` | 批注创建 / `{state, expectedVersion}`（409；A4） |
| `POST /api/v1/docs/{id}/status` | `{status, expectedVersion}`（409；A17） |
| `GET /api/v1/assets/{asset_id}` | 资产读取（A6） |

**前端契约（TS）**（A11 序列化口径：后端 pydantic `alias_generator=to_camel`，JSON 一律 camelCase）：

```ts
export type AtomType = "clause"|"definition"|"table"|"figure"|"code"|"example"|"note"|"cross_ref";
export interface NodeDTO {
  nodeId: string; docId: string; atomType: AtomType; format: "md"|"html"|"text";
  anchor: string; parentNodeId: string | null; level: number | null;
  content: unknown; version: number; status: "active"|"deleted";
}
export interface EventDTO { eventId: string; entity: "doc"|"node"|"ref"|"comment"|"schema";
  entityId: string; op: string; payload: Record<string, unknown>; actor: string; ts: string; }
export interface CommentDTO { commentId: string; nodeId: string; targetEventId: string | null;
  body: string; state: "open"|"resolved"|"orphaned"; author: string; version: number; ts: string; }
export interface SchemaDTO { typeName: string; version: number; jsonSchema: Record<string, unknown>; }
```

### M09 校验

```python
# M09A（阶段 1）
def validate_proposal(atom_type: str, content: dict) -> list[Violation]: ...
def validate_write(node: NodeIn) -> list[Violation]: ...
# M09B（阶段 3）
def run_quality_gate(scope: QualityScope) -> list[QualityReport]:
    """detector_id ∈ {broken_refs, terms, assets_missing, render_consistency,
       events_consistency}；render_consistency 消费 M04.normalize；
       events_consistency 用 M02.apply_events 重放比对当前态。"""
```

### M-LR LightRAG 边界（暂缓联调，C7）

```python
def export_package(doc_ids: list[str], out_dir: Path) -> ExportResult: ...
    """jsonl: {node_id, doc_id, anchor, text}；来自渲染文本。"""
async def change_stream(since: str | None) -> AsyncIterator[Event]: ...   # events 游标流
```

### 3.5 事件载荷与折叠规范（A18）

| entity | op | payload 形状 | 折叠规则（apply_events） |
|---|---|---|---|
| doc | create/update/status | `{field: {before, after}, …}` | 逐字段覆盖到 doc 行快照 |
| node | create/update/delete | `{field: {before, after}, …}`；delete 含 `before` 全量 | create 建快照；update 逐字段覆盖；delete 置 `status=deleted` |
| ref | add/remove | `{src, dst_doc, dst_node, kind}` | add 追加 refs 行；remove 移除对应行 |
| comment | create/update | `{field: {before, after}, …}` | 逐字段覆盖批注快照 |
| schema | create/update | `{type_name, version, diff}` | 记录 schema 版本历史 |

## 4. 数据库 DDL（PostgreSQL 16，database `agenticdocer`；v1.2）

```sql
CREATE TABLE docs (
  doc_id     text PRIMARY KEY,                -- SPEC-*（映射见 §6 frontmatter 映射表）
  doc_type   text NOT NULL CHECK (doc_type IN ('standard','lang','tool-manual','product','safety')),
  title      text NOT NULL,
  meta       jsonb NOT NULL DEFAULT '{}',
  source_ref text,
  status     text NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','reviewed','approved')),
  version    bigint NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE nodes (
  node_id        uuid PRIMARY KEY,
  doc_id         text NOT NULL REFERENCES docs(doc_id),
  atom_type      text NOT NULL,
  format         text NOT NULL DEFAULT 'md' CHECK (format IN ('md','html','text')),
  ordinal        integer NOT NULL,
  parent_node_id uuid REFERENCES nodes(node_id) ON DELETE SET NULL,
  level          smallint,
  anchor         text NOT NULL,
  content        jsonb NOT NULL,             -- 约定：content.text 必填（检索源，A10）
  status         text NOT NULL DEFAULT 'active' CHECK (status IN ('active','deleted')),  -- A2 软删
  version        bigint NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (doc_id, anchor)
);
CREATE INDEX idx_nodes_doc_ordinal ON nodes (doc_id, ordinal);
CREATE INDEX idx_nodes_parent      ON nodes (parent_node_id);
CREATE INDEX idx_nodes_content_gin ON nodes USING gin (content jsonb_path_ops);
ALTER TABLE nodes ADD COLUMN text_fts tsvector
  GENERATED ALWAYS AS (to_tsvector('english', coalesce(content->>'text',''))) STORED;   -- A10
CREATE INDEX idx_nodes_fts ON nodes USING gin (text_fts);

CREATE TABLE refs (                              -- A5/R1 修订：代理主键 + NULL 参与唯一
  ref_id      uuid PRIMARY KEY,
  src_node_id uuid NOT NULL REFERENCES nodes(node_id) ON DELETE CASCADE,
  dst_doc_id  text NOT NULL,
  dst_node_id uuid REFERENCES nodes(node_id) ON DELETE SET NULL,
  kind        text NOT NULL CHECK (kind IN ('traces_to','see_also','composes_from','source_ref'))
);
ALTER TABLE refs ADD CONSTRAINT refs_unique UNIQUE NULLS NOT DISTINCT
  (src_node_id, dst_doc_id, dst_node_id, kind);  -- PG15+：NULL 参与唯一性（文档级引用 dst_node_id IS NULL 合法）
CREATE INDEX idx_refs_dst ON refs (dst_doc_id, dst_node_id);
-- 外部叶引用：dst_doc_id 约定 'EXT:<uri>'（kind=source_ref）

CREATE TABLE events (                            -- append-only
  event_id  uuid PRIMARY KEY,
  entity    text NOT NULL CHECK (entity IN ('doc','node','ref','comment','schema')),
  entity_id text NOT NULL,
  op        text NOT NULL,
  payload   jsonb NOT NULL,
  actor     text NOT NULL,                       -- 取值规则 §6（A3）
  ts        timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_events_entity ON events (entity, entity_id, ts);
CREATE INDEX idx_events_ts     ON events (ts);

CREATE TABLE comments (
  comment_id      uuid PRIMARY KEY,
  node_id         uuid NOT NULL REFERENCES nodes(node_id),   -- 软删方案下无需级联（A2）
  target_event_id uuid REFERENCES events(event_id),
  body            text NOT NULL,
  state           text NOT NULL DEFAULT 'open' CHECK (state IN ('open','resolved','orphaned')),
  author          text NOT NULL,
  version         bigint NOT NULL DEFAULT 1,                 -- A4
  ts              timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_comments_node ON comments (node_id, state);

CREATE TABLE schemas (
  type_name   text NOT NULL,
  json_schema jsonb NOT NULL,
  version     integer NOT NULL DEFAULT 1,
  PRIMARY KEY (type_name, version)
);

CREATE TABLE assets (
  asset_id text PRIMARY KEY,                   -- sha256 hex
  mime     text NOT NULL,
  bytes    bigint NOT NULL,
  origin   text,
  path     text NOT NULL                       -- 相对 ASSET_STORE_DIR（A6）
);

CREATE TABLE terms (
  term               text PRIMARY KEY,
  definition_node_id uuid REFERENCES nodes(node_id) ON DELETE SET NULL,
  kind               text NOT NULL CHECK (kind IN ('glossary','normative-keyword'))
);
```

### 4.1 角色与权限（A15）

```sql
-- 属主：agenticdocer（database owner，建库时创建）
CREATE ROLE agenticdocer LOGIN PASSWORD '…';             -- 属主角色（alembic 迁移使用）
CREATE ROLE agenticdocer_app LOGIN PASSWORD '…';         -- 应用连接角色（最小权限）
GRANT CONNECT ON DATABASE agenticdocer TO agenticdocer_app;
GRANT USAGE ON SCHEMA public TO agenticdocer_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO agenticdocer_app;
ALTER DEFAULT PRIVILEGES FOR ROLE agenticdocer IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO agenticdocer_app;   -- L4：后续新表默认授权
REVOKE UPDATE, DELETE ON events FROM agenticdocer_app;  -- append-only 强制（P2）
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO agenticdocer_app;
```

## 5. 部署与运行（AB1/AB2/B15）

```
systemd --user: agenticdocer-api.service
  ExecStart: uv run agenticdocer-api --host 127.0.0.1 --port 8787
  Environment: DATABASE_URL=postgresql+asyncpg://agenticdocer_app@127.0.0.1:5432/agenticdocer
               ASSET_STORE_DIR=/home/lxx/wrk/AgenticDocer/data/assets
               IMPORT_WORK_DIR=/home/lxx/wrk/AgenticDocer/data/import_work
               RENDER_OUT_DIR=/home/lxx/wrk/AgenticDocer/build/rendered
  静态托管: FastAPI mount / -> webui/dist（AB2）
开发期: Vite devserver (5173) -> proxy /api -> 127.0.0.1:8787
测试库: agenticdocer_test（AB3，可重建；同角色授权）
```

## 6. 横切关注点

| 关注点 | 约定 |
|---|---|
| 身份（A3） | 写路径一律 `WriteContext(actor, source)`：M06/M07 取 `X-Actor` 头（空 → 422）；CLI 默认 `actor=cli, source=cli`；M03 默认 `actor=importer, source=importer`；系统任务 `actor=system, source=system` |
| 序列化（A11） | pydantic `alias_generator=to_camel`；HTTP JSON 一律 camelCase；DB 与 Python 内部 snake_case |
| 日志 | Agentic Logger SDK（AGENTS.md 强制）；结构化字段：module(M##)、event_id、doc_id、rule_id |
| 错误 | ConflictError→409、ValidationError→422、NotFound→404；Violation 结构统一 |
| ID | 应用侧 UUIDv7（时间有序）；`doc_id` 采用 `SPEC-*` 映射（A22，映射表见 §6） |
| 时间 | UTC（timestamptz）；展示本地化 |
| 配置 | 环境变量（§5 清单）；默认值指向仓库 `data/`、`build/`（gitignore） |

**frontmatter → docs 映射（A22，C5 十七字段，含 spec 专属 4 项）**：`title→title`；`spec_id→doc_id`；`spec_type→doc_type`；`spec_org`/`spec_revision`/`source`/`converted_*`/`reviewed_*`/`ingested_at`/`status`（approved→approved 等）→ `meta` JSONB 全量保真 + `source_ref→source`；`type/purpose/audience/direction/version/section_meta` → `meta`。必填校验：C5 十七字段（title/type/purpose/audience/direction/status/version/section_meta/spec_id/spec_type/spec_org/spec_revision/source/converted_by/converted_at/reviewed_by/reviewed_at）。

## 7. 与 idea 层的偏差声明

无。A1–A25 修订均为本层落实与补全，不改变 idea v1.1.0 的任何决策方向；其中 A1（锚消歧）、A7（HTML `<img>` 覆盖）、A20（可测判据细化）需同步回写 idea 对应表述（已在下文 §7.1 列明，回写已完成）。

### 7.1 回写记录

| 项 | idea 文档 | 修订 |
|---|---|---|
| A1 | design_doc §5.4 / ADR-006 | 锚消歧改为「正文摘要 + 同级序号」；稳定性表述改「仅依赖文档内容与同级计数」 |
| A7 | design_doc §5.2 | 图片引用数更正：md 形式 1,019 + HTML `<img>` 80（合计 1,099）；策略覆盖 HTML 内 img |
| A20 | functional_specification（本包） | 判据细化：goldenset 文件、perf 脚本、e2e 动作 |
