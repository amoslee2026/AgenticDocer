---
title: 架构规范 — 芯片设计知识库系统
type: composite
purpose: architecture
audience: both
direction: input
status: approved
version: "1.1.0"
section_meta: "@meta"
---

# 架构规范

生成：2026-09-16（it.arch Phase 4）。上游：`functional_specification.md`（REQ 清单）、`../idea/design_doc.md` v1.1.0。模块编号 M01–M09 + M-LR 沿用 idea 层。

## 1. 架构原则（可验证的不变量）

| # | 原则 | 验证方式 |
|---|---|---|
| P1 | 结构化库为唯一权威源；一切人类可读格式均为渲染产物 | 无代码路径从渲染产物反向写库 |
| P2 | 一切写入 = 事件 + 实体同事务；events 仅追加 | 事务注入测试；REVOKE 审计 |
| P3 | 依赖单向：模块仅依赖已交付的更低编号模块（交付序见 §9） | import 方向检查（lint 规则） |
| P4 | HTML 片段与内联标记原样直通（零改写） | 往返测试（normalize 等价） |
| P5 | 口径唯一：normalize()（渲染一致性）、rule_id（解析覆盖率）、anchor（引用） | 各自单测固定 |

## 2. 代码结构与模块映射

```
src/agenticdocer/
├── model/       # M01 内容模型与 Schema 注册表（schemas.py, anchors.py, atoms.py）
├── store/       # M02 存储层（db.py, nodes.py, refs.py, events.py, comments.py, assets.py）
├── importer/    # M03 导入解析（parser/, rules/, cli.py, assets_sync.py）
├── render/      # M04 渲染（renderer.py, templates/, normalize.py）
├── retrieve/    # M05 图遍历与检索（traverse.py, search.py）
├── agent_api/   # M06 Agent 接口（router.py, contracts.py）
├── webui_api/   # M07 WebUI API（router.py）
├── m09/         # M09 校验（engine_9a.py, quality_9b/)
├── mlr/         # M-LR LightRAG 边界（export.py, stream.py）
└── app.py       # FastAPI 装配（含 M08 前端静态挂载）
webui/           # M08 前端（React+TS+Vite，schema 驱动表单引擎）
tests/           # 单元 + 集成 + e2e（语料回归）
alembic/         # DDL 迁移（AB4）
```

## 3. 模块接口契约

### M01 内容模型

```python
# agenticdocer/model/atoms.py
ATOM_TYPES = ("clause","definition","table","figure","code","example","note","cross_ref")
ATOM_VARIANTS = ("table.register_field", "figure.state_machine")

# agenticdocer/model/schemas.py
def get_json_schema(atom_type: str) -> dict: ...          # 从 schemas 表缓存加载
def validate(atom_type: str, content: dict) -> list[Violation]: ...   # 委托 M09A

# agenticdocer/model/anchors.py
def make_anchor(doc_id: str, chapter_path: list[str], title: str) -> str:
    """章节号路径；重复标题加内容 sha256[:8] 消歧；与位置无关（幂等）。"""

# 核心类型（pydantic）
class NodeIn(BaseModel):      node_id: UUID | None; doc_id: str; atom_type: str
                              format: Literal["md","html","text"]="md"; ordinal: int
                              parent_node_id: UUID | None; level: int | None
                              anchor: str; content: dict
class Violation(BaseModel):   rule_id: str; path: str; message: str; fix_hint: str | None
```

### M02 存储层

```python
class Storage:
    async def get_node(self, node_id: UUID) -> Node: ...
    async def get_doc_nodes(self, doc_id: str) -> list[Node]: ...          # 按 ordinal
    async def upsert_node(self, node: NodeIn, expected_version: int | None) -> Node: ...
        # 乐观锁：版本不符 -> ConflictError(409)；成功则 version+1 且写 node 事件（同事务）
    async def add_ref(self, src: UUID, dst_doc: str, dst_node: UUID | None, kind: RefKind) -> None
    async def remove_ref(self, src: UUID, dst_doc: str, kind: RefKind) -> None
    async def replay(self, entity: str, entity_id: str, upto: datetime | None = None) -> list[Event]
    async def create_comment(self, node_id: UUID, body: str, author: str) -> Comment
        # target_event_id = 该节点最新事件的 event_id
    async def resolve_comment(self, comment_id: UUID) -> None
    async def orphan_comments(self, node_id: UUID) -> None    # 节点删除时调用
    async def put_asset(self, data: bytes, mime: str, origin: str) -> str   # 返回 sha256
    async def get_asset(self, asset_id: str) -> bytes

class ConflictError(Exception): ...   # 映射 HTTP 409
```

### M03 导入解析

```python
# agenticdocer/importer/parser.py
class Proposal(BaseModel):  rule_id: str; confident: bool             # confident=False 即「待确认」
                            source_lines: tuple[int,int]; atom: NodeIn | RawFallback
class ParseResult(BaseModel): doc_meta: dict; proposals: list[Proposal]
                              unmapped: list[UnmappedBlock]
                              stats: ParseStats   # total_blocks, rule_covered, fallback

def parse_markdown(path: Path) -> ParseResult: ...
# 规则库：agenticdocer/importer/rules/*.py（每规则一个 rule_id：
#   heading.path / clause.numbered / table.html / figure.image / code.fence /
#   list.nested / note.marker / xref.anchor …）
# 未映射块 -> RawFallback（note/code, format=html|md），不计入规则覆盖率

async def commit(result: ParseResult) -> CommitResult:   # 经 M09A -> M02 事务写库
```

CLI（REQ-M03-F02）：

```
python -m agenticdocer.import parse  <file.md>            # 输出提议清单（json/md）
python -m agenticdocer.import review <doc_slug>           # 交互：通过/拒绝/修正/批量确认待确认项
python -m agenticdocer.import commit <doc_slug>           # 校验 + 事务入库 + 统计报告
python -m agenticdocer.import stats  <doc_slug>           # 规则覆盖率/兜底率/待确认条数
```

### M04 渲染引擎

```python
def render_document(doc_id: str, out_dir: Path) -> RenderResult:
    """节点树 -> Markdown：format=html 原样回写；frontmatter 按 C5 回写；
    图片写为 assets/<sha256>.jpg 相对路径（从 assets 表导出到 out_dir/assets/）。"""

class NormalForm(BaseModel):
    headings: list[tuple[int,str]]; tables: list[TableNF]   # TableNF(rows,cols,cells[list[str]])
    code_blocks: list[str]; images: list[str]; lists: list[list[str]]
    inline_markers: list[str]
def normalize(doc_id: str) -> NormalForm: ...
```

### M05 图遍历与检索

```python
KIND_RULES: dict[RefKind, tuple[Literal["up","down","both"], bool]] = {
    "traces_to": ("up", True), "composes_from": ("down", True),
    "see_also": ("both", True), "source_ref": ("up", False),   # False=不参与多跳
}
def traverse(node_id: UUID, hops: int = 1) -> list[TraversalHit]:
    """递归 CTE；去重保留最短路径；环截断；排序：跳数→doc 序→ordinal。"""
def search_text(q: str, limit: int = 50) -> list[SearchHit]: ...   # FTS（ADR-005）
```

### M06 Agent 接口（HTTP，OpenAPI 由 FastAPI 生成）

| 方法/路径 | 语义 | 关键错误 |
|---|---|---|
| `GET /api/v1/nodes/{node_id}` | 节点读（含 version） | 404 |
| `GET /api/v1/docs/{doc_id}/nodes` | 文档节点树 | 404 |
| `POST /api/v1/nodes` | 结构化写入（body: NodeIn + expected_version） | 422 schema；409 乐观锁 |
| `POST /api/v1/refs` / `DELETE /api/v1/refs` | 引用边增删 | 404/422 |
| `POST /api/v1/docs/{doc_id}/render` | 触发渲染（建库产物） | 404 |
| `GET /api/v1/search?q=&hops=` | 检索 | — |

### M07 WebUI API

| 方法/路径 | 语义 |
|---|---|
| `GET /api/v1/docs` / `GET /api/v1/docs/{id}` | 文档列表/详情 |
| `GET /api/v1/events?entity=&entity_id=` | 结构化 diff 数据源 |
| `GET /api/v1/events/replay?node_id=&upto=` | 版本历史 |
| `POST /api/v1/comments` / `PATCH /api/v1/comments/{id}` | 批注创建/状态 |
| `POST /api/v1/docs/{id}/status` | 状态流转（draft/reviewed/approved） |

**前端契约（TS，M08 依赖：仅此接口面）**：

```ts
export type AtomType = "clause"|"definition"|"table"|"figure"|"code"|"example"|"note"|"cross_ref";
export interface NodeDTO {
  nodeId: string; docId: string; atomType: AtomType; format: "md"|"html"|"text";
  anchor: string; parentNodeId: string | null; level: number | null;
  content: unknown; version: number; status: string;
}
export interface EventDTO {
  eventId: string; entity: "doc"|"node"|"ref"|"comment"|"schema"; entityId: string;
  op: string; payload: Record<string, unknown>; actor: string; ts: string;
}
export interface CommentDTO { commentId: string; nodeId: string; targetEventId: string;
  body: string; state: "open"|"resolved"|"orphaned"; author: string; ts: string; }
```

### M09 校验

```python
# M09A（阶段 1）
def validate_proposal(atom_type: str, content: dict) -> list[Violation]: ...
def validate_write(node: NodeIn) -> list[Violation]: ...

# M09B（阶段 3）
def run_quality_gate(scope: QualityScope) -> QualityReport:
    """五类 detector：broken_refs / terms / assets_missing /
       render_consistency（消费 M04.normalize）/ events_consistency（重放比对）。
       违规明细含 detector_id + 定位。"""
```

### M-LR LightRAG 边界（暂缓联调，C7）

```python
def export_package(doc_ids: list[str], out_dir: Path) -> ExportResult:
    """渲染文本 + node_id 映射（jsonl: {node_id, text, doc_id, anchor}）。"""
async def change_stream(since: str | None) -> AsyncIterator[Event]: ...   # events 游标流
```

## 4. 数据库 DDL（PostgreSQL 16，database `agenticdocer`）

```sql
CREATE TABLE docs (
  doc_id     text PRIMARY KEY,                -- SPEC-*
  doc_type   text NOT NULL,                   -- standard | ...
  title      text NOT NULL,
  meta       jsonb NOT NULL DEFAULT '{}',     -- frontmatter 全集（C5）
  source_ref text,
  status     text NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','reviewed','approved')),
  version    bigint NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE nodes (
  node_id        uuid PRIMARY KEY,            -- UUIDv7（应用侧生成）
  doc_id         text NOT NULL REFERENCES docs(doc_id),
  atom_type      text NOT NULL,
  format         text NOT NULL DEFAULT 'md' CHECK (format IN ('md','html','text')),
  ordinal        integer NOT NULL,
  parent_node_id uuid REFERENCES nodes(node_id) ON DELETE SET NULL,
  level          smallint,
  anchor         text NOT NULL,
  content        jsonb NOT NULL,
  status         text NOT NULL DEFAULT 'active',
  version        bigint NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (doc_id, anchor)
);
CREATE INDEX idx_nodes_doc_ordinal ON nodes (doc_id, ordinal);
CREATE INDEX idx_nodes_parent      ON nodes (parent_node_id);
CREATE INDEX idx_nodes_content_gin ON nodes USING gin (content jsonb_path_ops);

CREATE TABLE refs (
  src_node_id uuid NOT NULL REFERENCES nodes(node_id) ON DELETE CASCADE,
  dst_doc_id  text NOT NULL,
  dst_node_id uuid REFERENCES nodes(node_id) ON DELETE SET NULL,
  kind        text NOT NULL CHECK (kind IN ('traces_to','see_also','composes_from','source_ref')),
  PRIMARY KEY (src_node_id, dst_doc_id, kind)
);
CREATE INDEX idx_refs_dst ON refs (dst_doc_id, dst_node_id);

CREATE TABLE events (                          -- append-only：REVOKE UPDATE/DELETE
  event_id  uuid PRIMARY KEY,                  -- UUIDv7（时序有序）
  entity    text NOT NULL CHECK (entity IN ('doc','node','ref','comment','schema')),
  entity_id text NOT NULL,
  op        text NOT NULL,                     -- create|update|delete|status|add|remove
  payload   jsonb NOT NULL,                    -- 字段级 diff {field:{before,after}} / ref {src,dst,kind}
  actor     text NOT NULL,
  ts        timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_events_entity ON events (entity, entity_id, ts);
CREATE INDEX idx_events_ts     ON events (ts);

CREATE TABLE comments (
  comment_id      uuid PRIMARY KEY,
  node_id         uuid NOT NULL REFERENCES nodes(node_id),   -- 不级联：保留 orphaned
  target_event_id uuid REFERENCES events(event_id),
  body            text NOT NULL,
  state           text NOT NULL DEFAULT 'open' CHECK (state IN ('open','resolved','orphaned')),
  author          text NOT NULL,
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
  origin   text,                               -- 如 GigaRAG images 路径
  path     text
);

CREATE TABLE terms (
  term               text PRIMARY KEY,
  definition_node_id uuid REFERENCES nodes(node_id) ON DELETE SET NULL,
  kind               text NOT NULL CHECK (kind IN ('glossary','normative-keyword'))
);

-- append-only 强制（应用角色）
REVOKE UPDATE, DELETE ON events FROM agenticdocer_app;
```

> 缺失资产（`assets.missing`）为 **M09B 报告项**，不建库内行（design_doc §5 assets 行注）。

## 5. 部署与运行（AB1/AB2/B15）

```
systemd --user: agenticdocer-api.service
  ExecStart: uv run agenticdocer-api --host 127.0.0.1 --port 8787
  Environment: DATABASE_URL=postgresql+asyncpg://agenticdocer@127.0.0.1:5432/agenticdocer
  静态托管: FastAPI mount / -> webui/dist（AB2）
开发期: Vite devserver (5173) -> proxy /api -> 127.0.0.1:8787
测试库: agenticdocer_test（AB3，可重建）
```

## 6. 横切关注点

| 关注点 | 约定 |
|---|---|
| 日志 | **Agentic Logger SDK**（AGENTS.md 强制）；结构化字段：module(M##)、event_id、doc_id、rule_id |
| 错误 | 领域错误（ConflictError/ValidationError/NotFound）映射 HTTP（409/422/404）；违规清单结构统一（Violation） |
| ID 生成 | 应用侧 UUIDv7（全局单调趋势，事件排序友好） |
| 时间 | UTC 存储（timestamptz）；展示按本地时区 |
| 配置 | 环境变量（DATABASE_URL、PORT、RENDER_OUT_DIR 默认 build/rendered）|

## 7. 与 idea 层的偏差声明

无。E1–E20/N1–N8 修订已固化于 idea v1.1.0；本规范为其架构级展开（接口/DDL/API/CLI/部署）。
