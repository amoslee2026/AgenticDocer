"""M07 WebUI API（§3 M07；REQ-M07-F01..F06）——M08 前端**唯一**依赖的 HTTP 契约面。

| 分组 | 端点 |
|---|---|
| 文档 | `GET /docs`、`GET /docs/{doc_id}`、`POST /docs/{doc_id}/status`（A17 乐观锁） |
| 表单数据源 | `GET /schemas`、`GET /schemas/{atom_type}`、`POST /schemas`（A8/A16） |
| 结构化 diff | `GET /events`、`GET /docs/{doc_id}/diff`（B11/REQ-M07-F06） |
| 版本历史 | `GET /events/replay`（`apply_events` 折叠，A18） |
| 术语 | `GET /terms`、`POST /terms`（R10） |
| 批注 | `POST /comments`、`GET /comments`、`PATCH /comments/{id}`（A4 乐观锁） |
| 表格回写 | `PATCH /nodes/{node_id}/table`（B6/V8：行列 JSON → `content`） |
| 管理 | `GET /admin/metrics`、`GET /admin/health`（**admin 专属**，ADR-010） |
| 用户与授权 | `/users`、`/users/{id}/keys`、`/roles`、`/grants`（**admin 专属**，B3/A1；服务层在 M10） |

**与 M06 的分工（R8）**：表单与 agent **共用同一实现集**——`GET/POST /nodes`、
`GET /docs/{id}/nodes`、`/docs/{id}/sections`、`/docs/{id}/render`、`/assets/{id}` 在
:mod:`agenticdocer.agent_api`；本模块只提供「WebUI 专属视图」（列表/diff/schema/术语/批注/
表格编辑/管理端点）。**`/auth/*` 由 M10 提供**（:mod:`agenticdocer.auth.router`），此处不重复实现。

**鉴权（S4/S5/S14）**：全部端点需凭据；写端点另按角色硬上限 + grant 收窄判定。
`source` 由凭据类型判定（Cookie → `webui`，签名 → `agent`），**不读 `X-Actor`**。

**序列化（A11）**：HTTP JSON 一律 camelCase（pydantic `alias_generator=to_camel`）。
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any, Final, Literal, Sequence
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import Field
from sqlalchemy import insert, select, update

from agenticdocer.auth import (
    ROLE_PERMISSIONS,
    add_ssh_key,
    create_grant,
    create_user,
    delete_grant,
    delete_user,
    list_grants,
    list_users,
    revoke_ssh_key,
    update_user,
    write_context,
)
from agenticdocer.model import (
    ATOM_SCHEMAS,
    Comment,
    CommentState,
    Doc,
    DocStatus,
    EntityKind,
    Event,
    Grant,
    GrantPermission,
    GrantScope,
    Model,
    Node,
    NodeSnapshot,
    RoleName,
    SchemaDef,
    SshKey,
    Term,
    User,
    get_atom_schema,
)
# `UserStatus` 属 §3.0 取值域但未列入 `model.__all__`；从定义处取（M10 `users.py` 同口径）
from agenticdocer.model.types import UserStatus
from agenticdocer.observability import (
    HealthReport,
    MetricsSnapshot,
    get_logger,
    health,
    snapshot,
)
from agenticdocer.render import TableEdit, resolve_table_mode, write_table_edit
from agenticdocer.store import (
    ConflictError,
    Database,
    ForbiddenError,
    NotFoundError,
    Storage,
    ValidationError,
    append_event,
    apply_events,
    build_model,
    now,
)
from agenticdocer.store.rows import row_to_dict
# `EVENT_COLUMNS`/`COMMENT_COLUMNS` 未列入 `store.__all__`（它们服务于 M02 内部查询）；
# M07 的事件/批注聚合视图直取列清单，口径仍由 M02 单点定义（P5）
from agenticdocer.store.comments import COMMENT_COLUMNS
from agenticdocer.store.events import EVENT_COLUMNS
from agenticdocer.store.schema import (
    comments as comments_table,
    events as events_table,
    nodes as nodes_table,
    refs as refs_table,
    schemas as schemas_table,
    ssh_keys as ssh_keys_table,
    terms as terms_table,
)

from .deps import (
    AdminAuth,
    DatabaseDep,
    ReadAuth,
    ReviewAuth,
    StorageDep,
    WriteAuth,
    authorize_doc,
)

__all__ = [
    "CommentCreate",
    "CommentStateChange",
    "DiffEntry",
    "DiffSummary",
    "DocDiff",
    "GrantCreate",
    "KeyAdd",
    "KeyRevoke",
    "RoleInfo",
    "SchemaRegister",
    "StatusChange",
    "TermUpsert",
    "UserCreate",
    "UserPatch",
    "UserView",
    "router",
]

log = get_logger("m07.api")

router = APIRouter(prefix="/api/v1", tags=["webui"])

_EVENT_BATCH: Final = 500
"""事件批量读取的 `entity_id IN (…)` 分片大小（避免超长 SQL）。"""

_DEFAULT_WINDOW_SECONDS: Final = 3600

_NODE_DIFF_FIELDS: Final = (
    "atom_type",
    "format",
    "ordinal",
    "parent_node_id",
    "level",
    "anchor",
    "content",
    "status",
    "version",
)
"""逐字段比较的节点字段（`doc_id` 不入列：分区键不可变）。"""

_ISO_SUFFIX: Final = "Z"


# ── 请求/响应 DTO（§3 M07 TS 契约的 Python 侧；camelCase 由 `Model` 保证）──


class SchemaRegister(Model):
    """`POST /api/v1/schemas` 请求体（A16：schema 写入路径）。"""

    type_name: str = Field(min_length=1)
    json_schema: dict[str, Any]
    version: int = Field(default=1, ge=1)


class TermUpsert(Model):
    """`POST /api/v1/terms` 请求体（R10：术语写入路径）。"""

    term: str = Field(min_length=1)
    definition_node_id: UUID | None = None
    kind: TermKind = "glossary"


class CommentCreate(Model):
    """`POST /api/v1/comments` 请求体；`expectedVersion` 为**被批注节点**的版本（A4 语义）。"""

    node_id: UUID
    body: str = Field(min_length=1)
    expected_version: int | None = None


class CommentStateChange(Model):
    """`PATCH /api/v1/comments/{id}` 请求体（`{state, expectedVersion}`，A4）。"""

    state: CommentState
    expected_version: int


class StatusChange(Model):
    """`POST /api/v1/docs/{id}/status` 请求体（`{status, expectedVersion}`，A17）。"""

    status: DocStatus
    expected_version: int


class UserCreate(Model):
    """`POST /api/v1/users` 请求体（admin 专属，B3）。"""

    username: str = Field(min_length=1)
    role: RoleName


class UserPatch(Model):
    """`PATCH /api/v1/users/{id}` 请求体（改角色/状态；两者至少给一个）。"""

    role: RoleName | None = None
    status: UserStatus | None = None


class UserView(User):
    """`GET /api/v1/users` 条目：M10 `User` + 未吊销公钥指纹集（§3 M07 `UserDTO.keyFingerprints`）。"""

    key_fingerprints: list[str] = []


class KeyAdd(Model):
    """`POST /api/v1/users/{id}/keys` 请求体（登记公钥，B3）。"""

    public_key: str = Field(min_length=1)


class KeyRevoke(Model):
    """`DELETE /api/v1/users/{id}/keys` 请求体（吊销单个公钥）。

    指纹形如 `SHA256:<base64>`，其 base64 **含 `/` 与 `+`**，故走请求体而**非**路径/query
    （避免路径分段与 `+`→空格 的解码陷阱）。
    """

    key_id: str = Field(min_length=1)


class GrantCreate(Model):
    """`POST /api/v1/grants` 请求体（S5：`permission` 无 `admin`，不扩权）。"""

    user_id: UUID
    scope: GrantScope
    value: str = Field(min_length=1)
    permission: GrantPermission


class RoleInfo(Model):
    """`GET /api/v1/roles` 条目（四角色与其权限集，B3/A15）。"""

    role: RoleName
    permissions: list[str]


class DiffEntry(Model):
    """一条 diff 变更（REQ-M07-F06：`nodeId`/`anchor`/`field`/`before`/`after` + 节点级 op）。

    - `op="added"` / `"deleted"`：节点级变更，`field="node"`（`before`/`after` 为节点视图）；
    - `op="modified"`：**逐字段**一条（`field` 为字段名，值为新旧值）；
    - `field="ref"`：引用边变化（`before`/`after` 为 `{src, dstDoc, dstNode, kind}`）。
    """

    node_id: UUID | None = None
    anchor: str | None = None
    op: Literal["added", "modified", "deleted"]
    field: str
    before: Any = None
    after: Any = None


class DiffSummary(Model):
    """`changes` 的计数（逐条计；`refs` = 引用变化条目数）。"""

    added: int = 0
    modified: int = 0
    deleted: int = 0
    refs: int = 0


class DocDiff(Model):
    """`GET /api/v1/docs/{id}/diff` 响应（REQ-M07-F06）；无变更时 `changes=[]`（非 404）。"""

    doc_id: str
    from_ts: datetime | None
    to_ts: datetime | None
    changes: list[DiffEntry]
    summary: DiffSummary


# ── 文档 ────────────────────────────────────────────────────────────────


@router.get("/docs", response_model=list[Doc])
async def list_docs(
    context: ReadAuth,
    storage: StorageDep,
    status: DocStatus | None = Query(default=None, description="按状态过滤（省略 → 全部）"),
) -> list[Doc]:
    """文档清单（含 `version`/`status`，A17/R7）。"""
    with log.timer("query", table="docs", status=status):
        return await storage.list_docs(status)


@router.get("/docs/{doc_id}", response_model=Doc)
async def get_doc(doc_id: str, context: ReadAuth, storage: StorageDep, db: DatabaseDep) -> Doc:
    """文档详情（含 `meta` 全量 frontmatter，M08 表格可编辑开关的来源）。"""
    return await authorize_doc(context, "read", doc_id, storage=storage, db=db)


@router.post("/docs/{doc_id}/status", response_model=Doc)
async def set_doc_status(
    doc_id: str,
    payload: StatusChange,
    context: ReviewAuth,
    storage: StorageDep,
    db: DatabaseDep,
) -> Doc:
    """状态流转（draft→reviewed→approved）；`expectedVersion` 不匹配 → 409（A17）。"""
    await authorize_doc(context, "review", doc_id, storage=storage, db=db)
    with log.timer("query", table="docs", doc_id=doc_id):
        return await storage.update_doc_status(
            doc_id, payload.status, payload.expected_version, write_context(context)
        )


# ── schema（A8/A16：表单引擎数据源）────────────────────────────────────


@router.get("/schemas", response_model=list[SchemaDef])
async def list_schemas(context: ReadAuth, db: DatabaseDep) -> list[SchemaDef]:
    """全部 schema：`schemas` 注册表 ∪ M01 内建八类 + 2 变体（同名以注册表为准）。

    M08 表单引擎**零手写 UI** 的数据源（REQ-M08-F01/§J 判据：仅向 `schemas` 表插一行即出现表单）。
    """
    with log.timer("query", table="schemas"):
        registered = await _schema_rows(db)
    merged = {
        name: SchemaDef(type_name=name, json_schema=schema, version=1)
        for name, schema in ATOM_SCHEMAS.items()
    }
    merged.update(registered)
    return [merged[name] for name in sorted(merged)]


@router.get("/schemas/{atom_type}", response_model=SchemaDef)
async def get_schema(atom_type: str, context: ReadAuth, db: DatabaseDep) -> SchemaDef:
    """单个 atom_type 的 schema（未注册 → 404）。"""
    with log.timer("query", table="schemas", atom_type=atom_type):
        registered = await _schema_rows(db)
    if atom_type in registered:
        return registered[atom_type]
    try:
        return SchemaDef(type_name=atom_type, json_schema=get_atom_schema(atom_type), version=1)
    except UnknownAtomTypeError as exc:
        raise NotFoundError(
            f"schema {atom_type!r} not found", entity="schema", entity_id=atom_type
        ) from exc


@router.post("/schemas", response_model=SchemaDef)
async def register_schema(
    payload: SchemaRegister,
    context: WriteAuth,
    db: DatabaseDep,
) -> SchemaDef:
    """注册 schema（A16）：同 `(type_name, version)` 已存在 → 409；写 `schema` 事件（§3.5）。"""
    actor = write_context(context).actor
    stamp = now()
    async with db.transaction() as session:
        current = (
            await session.execute(
                select(schemas_table.c.version)
                .where(schemas_table.c.type_name == payload.type_name)
                .order_by(schemas_table.c.version.desc())
                .limit(1)
            )
        ).first()
        duplicate = (
            await session.execute(
                select(schemas_table.c.version).where(
                    schemas_table.c.type_name == payload.type_name,
                    schemas_table.c.version == payload.version,
                )
            )
        ).first()
        if duplicate is not None:
            raise ConflictError(
                f"schema {payload.type_name}@{payload.version} 已存在",
                entity="schema",
                entity_id=payload.type_name,
            )
        await session.execute(
            insert(schemas_table).values(
                type_name=payload.type_name,
                json_schema=payload.json_schema,
                version=payload.version,
            )
        )
        await append_event(
            session,
            entity="schema",
            entity_id=payload.type_name,
            op="create" if current is None else "update",
            payload={
                "type_name": payload.type_name,
                "version": payload.version,
                "diff": {"previous_version": current.version if current is not None else None},
            },
            actor=actor,
            ts=stamp,
        )
    log.info(
        "schema registered",
        op="register_schema",
        type_name=payload.type_name,
        version=payload.version,
    )
    return SchemaDef(
        type_name=payload.type_name, json_schema=payload.json_schema, version=payload.version
    )


async def _schema_rows(db: Database) -> dict[str, SchemaDef]:
    """`schemas` 表按 `type_name` 取**最高版本**行（表小，Python 侧归并）。"""
    async with db.session() as session:
        rows = (await session.execute(select(*schemas_table.c))).all()
    latest: dict[str, SchemaDef] = {}
    for row in rows:
        record = row_to_dict(row)
        name = str(record["type_name"])
        version = int(record["version"])
        if name not in latest or version >= latest[name].version:
            latest[name] = SchemaDef(
                type_name=name, json_schema=record["json_schema"], version=version
            )
    return latest


# ── 术语（R10）────────────────────────────────────────────────────────


@router.get("/terms", response_model=list[Term])
async def list_terms(
    context: ReadAuth,
    db: DatabaseDep,
    kind: TermKind | None = Query(default=None, description="glossary | normative-keyword"),
) -> list[Term]:
    """术语表（M09B 术语校验与导出用；按 term 升序）。"""
    statement = select(*terms_table.c)
    if kind is not None:
        statement = statement.where(terms_table.c.kind == kind)
    statement = statement.order_by(terms_table.c.term)
    with log.timer("query", table="terms", kind=kind):
        async with db.session() as session:
            rows = (await session.execute(statement)).all()
    return [build_model(Term, row_to_dict(row)) for row in rows]


@router.post("/terms", response_model=Term)
async def upsert_term(
    payload: TermUpsert,
    context: WriteAuth,
    storage: StorageDep,
    db: DatabaseDep,
) -> Term:
    """术语写入（R10）：按 `term` upsert；`definitionNodeId` 给定则校验节点存在（404）。

    **事件缺席说明**：`terms` 在 §3.5/§4 DDL 的事件实体取值域（`doc`/`node`/`ref`/`comment`/
    `schema`/`auth`）中**无归属**，故本写入只落表 + M12 日志，不产生 `events` 行。
    """
    term = payload.term.strip()
    if payload.definition_node_id is not None:
        await storage.get_node(payload.definition_node_id, include_deleted=True)
    record = {
        "term": term,
        "definition_node_id": payload.definition_node_id,
        "kind": payload.kind,
    }
    async with db.transaction() as session:
        existing = (
            await session.execute(select(terms_table.c.term).where(terms_table.c.term == term))
        ).first()
        if existing is None:
            await session.execute(insert(terms_table).values(**record))
        else:
            await session.execute(
                update(terms_table)
                .where(terms_table.c.term == term)
                .values(definition_node_id=record["definition_node_id"], kind=record["kind"])
            )
    log.info(
        "term upserted",
        op="upsert_term",
        term=term,
        kind=payload.kind,
        actor=write_context(context).actor,
    )
    return Term(
        term=term, definition_node_id=payload.definition_node_id, kind=payload.kind
    )


# ── 批注（A4；REQ-M07-F03）──────────────────────────────────────────────


@router.post("/comments", response_model=Comment, status_code=201)
async def post_comment(
    payload: CommentCreate,
    context: ReviewAuth,
    storage: StorageDep,
    db: DatabaseDep,
) -> Comment:
    """创建批注：锚点取被批注节点的最近事件（M02 口径）；节点版本不匹配 → 409。"""
    node = await storage.get_node(payload.node_id)
    await authorize_doc(context, "review", node.doc_id, storage=storage, db=db)
    comment = await storage.create_comment(
        payload.node_id, payload.body, payload.expected_version, write_context(context)
    )
    log.info(
        "comment created",
        op="create_comment",
        comment_id=str(comment.comment_id),
        node_id=str(payload.node_id),
    )
    return comment


@router.get("/comments", response_model=list[Comment])
async def list_comments(
    context: ReadAuth,
    storage: StorageDep,
    db: DatabaseDep,
    node_id: UUID | None = Query(default=None, description="按节点取（与 doc_id 二选一）"),
    doc_id: str | None = Query(default=None, description="按文档取全部节点的批注（二选一）"),
    state: list[CommentState] | None = Query(default=None, description="可重复；省略 → 全部状态"),
) -> list[Comment]:
    """批注列表（M08 批注面板含 `orphaned`；M11 `comment list` / `docer-annotations`）。"""
    if (node_id is None) == (doc_id is None):
        raise HTTPException(
            status_code=400, detail={"error": "bad_request", "message": "node_id 与 doc_id 必须二选一"}
        )
    if node_id is not None:
        node = await storage.get_node(node_id, include_deleted=True)
        await authorize_doc(context, "read", node.doc_id, storage=storage, db=db)
        with log.timer("query", table="comments", node_id=str(node_id)):
            return await storage.list_comments(node_id, state)
    assert doc_id is not None  # 二选一已在上方判定
    await authorize_doc(context, "read", doc_id, storage=storage, db=db)
    statement = (
        select(*COMMENT_COLUMNS)
        .join(nodes_table, nodes_table.c.node_id == comments_table.c.node_id)
        .where(nodes_table.c.doc_id == doc_id)
    )
    if state is not None:
        statement = statement.where(comments_table.c.state.in_(tuple(state)))
    statement = statement.order_by(comments_table.c.ts, comments_table.c.comment_id)
    with log.timer("query", table="comments", doc_id=doc_id):
        async with db.session() as session:
            rows = (await session.execute(statement)).all()
    return [build_model(Comment, row_to_dict(row)) for row in rows]


@router.patch("/comments/{comment_id}", response_model=Comment)
async def patch_comment(
    comment_id: UUID,
    payload: CommentStateChange,
    context: ReviewAuth,
    storage: StorageDep,
    db: DatabaseDep,
) -> Comment:
    """批注状态流转（`{state, expectedVersion}`）；版本不匹配 → 409（A4）。"""
    comment = await storage.get_comment(comment_id)
    node = await storage.get_node(comment.node_id, include_deleted=True)
    await authorize_doc(context, "review", node.doc_id, storage=storage, db=db)
    return await storage.update_comment_state(
        comment_id, payload.state, payload.expected_version, write_context(context)
    )


# ── 表格编辑回写（B6/V8）────────────────────────────────────────────────


@router.patch("/nodes/{node_id}/table", response_model=Node)
async def patch_table(
    node_id: UUID,
    payload: TableEdit,
    context: WriteAuth,
    storage: StorageDep,
    db: DatabaseDep,
) -> Node:
    """行列 JSON → `content` 回写（M04 `write_table_edit`）；不可编辑形态 → 403（B6 判定）。

    判定用 M04 `resolve_table_mode`（P5 单一口径）：`html` 片段恒不可编辑（P4 零改写直通）。
    """
    node = await storage.get_node(node_id)
    doc = await authorize_doc(context, "write", node.doc_id, storage=storage, db=db)
    mode = resolve_table_mode(doc, node, context.user)
    if not mode.editable:
        raise ForbiddenError(
            f"节点 {node_id} 的表格不可编辑（{mode.reason}）", entity="node", entity_id=node_id
        )
    with log.timer("query", table="nodes", doc_id=node.doc_id):
        return await write_table_edit(node, payload, write_context(context), storage=storage)


# ── 事件、版本历史与文档 diff（A18/B11；REQ-M07-F05/F06）────────────────


@router.get("/events", response_model=list[Event])
async def list_events(
    context: ReadAuth,
    db: DatabaseDep,
    entity: EntityKind | None = Query(default=None),
    entity_id: str | None = Query(default=None),
    since: datetime | None = Query(default=None, description="含端下界（`ts >= since`）"),
    limit: int = Query(default=200, ge=1, le=1000),
) -> list[Event]:
    """事件查询（结构化 diff 数据源；按 `ts` 升序返回前 `limit` 条）。"""
    statement = select(*EVENT_COLUMNS)
    if entity is not None:
        statement = statement.where(events_table.c.entity == entity)
    if entity_id is not None:
        statement = statement.where(events_table.c.entity_id == entity_id)
    if since is not None:
        statement = statement.where(events_table.c.ts >= _as_utc(since))
    statement = statement.order_by(events_table.c.ts, events_table.c.event_id).limit(limit)
    with log.timer("query", table="events", entity=entity):
        async with db.session() as session:
            rows = (await session.execute(statement)).all()
    return [build_model(Event, row_to_dict(row)) for row in rows]


@router.get("/events/replay", response_model=NodeSnapshot)
async def replay_node(
    node_id: UUID,
    context: ReadAuth,
    storage: StorageDep,
    db: DatabaseDep,
    upto: str | None = Query(
        default=None, description="ISO 时间戳或 event_id（含端上界；省略 → 当前态）"
    ),
) -> NodeSnapshot:
    """节点版本历史（`apply_events` 折叠，A18）：`node` 为折叠态，`history` 为事件序列。"""
    node = await storage.get_node(node_id, include_deleted=True)
    await authorize_doc(context, "read", node.doc_id, storage=storage, db=db)
    moment = await _resolve_upto(upto, db)
    with log.timer("query", table="events", node_id=str(node_id)):
        events = await storage.replay("node", node_id, moment)
    folded = apply_events("node", events)
    if not isinstance(folded, NodeSnapshot):  # `entity="node"` 恒返回 NodeSnapshot（类型收窄）
        raise ValidationError("apply_events 未返回 NodeSnapshot", entity="node", entity_id=node_id)
    return folded


@router.get("/docs/{doc_id}/diff", response_model=DocDiff)
async def doc_diff(
    doc_id: str,
    context: ReadAuth,
    storage: StorageDep,
    db: DatabaseDep,
    from_: str | None = Query(default=None, alias="from", description="ISO 时间戳或版本号"),
    to: str | None = Query(default=None, description="ISO 时间戳或版本号；省略 → 当前态"),
) -> DocDiff:
    """文档版本 diff（REQ-M07-F06，B11）：按 `events` 折叠两个时点后逐字段比较。

    - `from`/`to`：ISO 时间戳，或 `docs.version` 口径的版本号（第 N 个 doc 事件）；
      省略 `to` → 当前态；省略 `from` → **上一次变更**（REQ-M11-F02 默认区间）；
    - 变更按 `node_id` 对齐，逐字段给出 `{before, after}`；节点级 `added`/`deleted` 与
      引用边变化合并入同一 `changes`；无变更 → `changes=[]`（非 404）。
    """
    doc = await authorize_doc(context, "read", doc_id, storage=storage, db=db)
    with log.timer("query", table="events", doc_id=doc_id):
        doc_events = await storage.replay("doc", doc_id)
    to_ts = _resolve_point(doc_events, to, default=None) if to is not None else None
    from_default = doc_events[-2].ts if len(doc_events) >= 2 else None
    from_ts = _resolve_point(doc_events, from_, default=from_default)

    with log.timer("query", table="nodes", doc_id=doc_id):
        doc_nodes = await storage.get_doc_nodes(doc_id, include_deleted=True)
    node_ids = [node.node_id for node in doc_nodes]
    node_events = await _load_node_events(db, node_ids)
    before_nodes = _fold_nodes(node_events, from_ts)
    after_nodes = _fold_nodes(node_events, to_ts)

    low = from_ts or (doc_events[0].ts if doc_events else None)
    ref_events = await _load_ref_events(db, low, to_ts)
    ref_events = [event for event in ref_events if _ref_src(event) in _id_texts(node_ids)]
    before_refs = _fold_refs(ref_events, from_ts)
    after_refs = _fold_refs(ref_events, to_ts)

    changes = _node_changes(before_nodes, after_nodes)
    ref_changes = _ref_changes(before_refs, after_refs)
    summary = DiffSummary(
        added=sum(1 for entry in changes if entry.op == "added"),
        modified=sum(1 for entry in changes if entry.op == "modified"),
        deleted=sum(1 for entry in changes if entry.op == "deleted"),
        refs=len(ref_changes),
    )
    log.info(
        "doc diff computed",
        op="doc_diff",
        doc_id=doc.doc_id,
        changes=len(changes) + len(ref_changes),
        from_ts=str(from_ts),
        to_ts=str(to_ts),
    )
    return DocDiff(
        doc_id=doc.doc_id,
        from_ts=from_ts,
        to_ts=to_ts,
        changes=[*changes, *ref_changes],
        summary=summary,
    )


# ── 管理端点（admin 专属，ADR-010）──────────────────────────────────────


@router.get("/admin/metrics", response_model=MetricsSnapshot)
async def admin_metrics(
    context: AdminAuth,
    since: datetime | None = Query(default=None, description="窗口起点（省略 → 近 window 秒）"),
    window: int = Query(default=_DEFAULT_WINDOW_SECONDS, ge=1, le=86400),
) -> MetricsSnapshot:
    """在线指标快照（端点耗时/慢查询/鉴权失败/渲染，ADR-010）。"""
    moment = _as_utc(since) if since is not None else datetime.now(timezone.utc) - timedelta(
        seconds=window
    )
    return snapshot(moment, window)


@router.get("/admin/health", response_model=HealthReport)
async def admin_health(context: AdminAuth, db: DatabaseDep) -> HealthReport:
    """容量健康巡检（分区/索引/膨胀/连接池/归档，ADR-010 §5）。"""
    return await health(engine=db.engine)


# ── 用户、公钥与授权（admin 专属；服务层 = M10）─────────────────────────


@router.get("/users", response_model=list[UserView])
async def list_users_endpoint(
    context: AdminAuth,
    db: DatabaseDep,
    status: UserStatus | None = Query(default=None),
) -> list[UserView]:
    """用户清单（含各用户未吊销公钥指纹集，§3 M07 `UserDTO`）。"""
    users = await list_users(status=status, db=db)
    fingerprints = await _key_fingerprints(db)
    return [
        UserView(**user.model_dump(), key_fingerprints=fingerprints.get(user.user_id, []))
        for user in users
    ]


@router.post("/users", response_model=User, status_code=201)
async def create_user_endpoint(payload: UserCreate, context: AdminAuth, db: DatabaseDep) -> User:
    """创建用户（用户名重复 → 409；角色取值域 → 422）。"""
    return await create_user(payload.username, payload.role, actor=context.actor, db=db)


@router.patch("/users/{user_id}", response_model=User)
async def patch_user(
    user_id: UUID,
    payload: UserPatch,
    context: AdminAuth,
    db: DatabaseDep,
) -> User:
    """改角色/状态（S9：不可操作自身与最后一个 active admin）。"""
    if payload.role is None and payload.status is None:
        raise ValidationError("role 与 status 至少给一个", entity="auth", entity_id=user_id)
    return await update_user(
        user_id,
        role=payload.role,
        status=payload.status,
        actor=context.actor,
        actor_id=context.user.user_id,
        db=db,
    )


@router.delete("/users/{user_id}", status_code=204)
async def delete_user_endpoint(user_id: UUID, context: AdminAuth, db: DatabaseDep) -> Response:
    """删除用户（级联密钥/授权/会话；S9 自我保护同上）。"""
    await delete_user(user_id, actor=context.actor, actor_id=context.user.user_id, db=db)
    return Response(status_code=204)


@router.post("/users/{user_id}/keys", response_model=SshKey, status_code=201)
async def add_key(
    user_id: UUID,
    payload: KeyAdd,
    context: AdminAuth,
    db: DatabaseDep,
) -> SshKey:
    """登记 SSH 公钥（格式/类型/强度不合规 → 422；公钥已属他人 → 409）。"""
    return await add_ssh_key(user_id, payload.public_key, actor=context.actor, db=db)


@router.delete("/users/{user_id}/keys", status_code=204)
async def revoke_key(
    user_id: UUID,
    payload: KeyRevoke,
    context: AdminAuth,
    db: DatabaseDep,
) -> Response:
    """吊销单个公钥（不影响同用户其他密钥；指纹经请求体传递，见 `KeyRevoke`）。"""
    await revoke_ssh_key(user_id, payload.key_id, actor=context.actor, db=db)
    return Response(status_code=204)


@router.get("/roles", response_model=list[RoleInfo])
async def list_roles(context: ReadAuth) -> list[RoleInfo]:
    """角色清单（四角色 + 各自权限集）。

    **无 POST**：§4 DDL 无 `roles` 表——四角色为固定取值域（`ROLE_PERMISSIONS`），
    可变的是「角色 ↔ 文档集」的 grant（`POST /grants`），故不存在「创建角色」的写入面。
    """
    return [
        RoleInfo(role=role, permissions=sorted(permissions))
        for role, permissions in sorted(ROLE_PERMISSIONS.items())
    ]


@router.get("/grants", response_model=list[Grant])
async def list_grants_endpoint(
    context: AdminAuth,
    db: DatabaseDep,
    user_id: UUID | None = Query(default=None, description="省略 → 全部用户的授权"),
) -> list[Grant]:
    """文档集级授权清单（S5：scope ∈ {doc_type, doc}）。"""
    return await list_grants(user_id=user_id, db=db)


@router.post("/grants", response_model=Grant, status_code=201)
async def create_grant_endpoint(payload: GrantCreate, context: AdminAuth, db: DatabaseDep) -> Grant:
    """授予文档集级授权（授予侧即校验越权：`role_permits` 不过 → 422，S5）。"""
    return await create_grant(
        payload.user_id,
        payload.scope,
        payload.value,
        payload.permission,
        actor=context.actor,
        granted_by=context.user.user_id,
        db=db,
    )


@router.delete("/grants/{grant_id}", status_code=204)
async def delete_grant_endpoint(grant_id: UUID, context: AdminAuth, db: DatabaseDep) -> Response:
    """撤销一条授权。"""
    await delete_grant(grant_id, actor=context.actor, db=db)
    return Response(status_code=204)


# ── 内部：时间点解析、事件装载与折叠 ───────────────────────────────────


def _as_utc(moment: datetime) -> datetime:
    """naive 时间按 UTC 解释（与库内 `timestamptz` 口径一致）。"""
    return moment if moment.tzinfo is not None else moment.replace(tzinfo=timezone.utc)


def _parse_moment(text: str) -> datetime | None:
    """ISO 8601 文本 → 时间点；不可解析 → `None`（交由版本号分支判错）。"""
    candidate = text.strip()
    if candidate.endswith(_ISO_SUFFIX):
        candidate = candidate[: -len(_ISO_SUFFIX)] + "+00:00"
    try:
        return _as_utc(datetime.fromisoformat(candidate))
    except ValueError:
        return None


def _resolve_point(doc_events: Sequence[Event], spec: str | None, *, default: datetime | None) -> datetime | None:
    """`from`/`to` → 时间点：省略 → `default`；整数 → 第 N 个 doc 事件的 `ts`；ISO → 原样。"""
    if spec is None or not spec.strip():
        return default
    moment = _parse_moment(spec)
    if moment is not None:
        return moment
    try:
        index = int(spec)
    except ValueError:
        raise ValidationError(
            f"{spec!r} 既不是 ISO 时间戳也不是版本号", entity="doc"
        ) from None
    if index < 1 or index > len(doc_events):
        raise ValidationError(
            f"版本号 {index} 超出该文档的事件数（{len(doc_events)}）", entity="doc"
        )
    return doc_events[index - 1].ts


async def _resolve_upto(upto: str | None, db: Database) -> datetime | None:
    """`upto` → 时间点：ISO；或 event_id（UUID7 → 取该事件 `ts`，含端重放）。"""
    if upto is None or not upto.strip():
        return None
    moment = _parse_moment(upto)
    if moment is not None:
        return moment
    try:
        event_id = UUID(upto.strip())
    except ValueError:
        raise ValidationError(
            f"upto={upto!r} 既不是 ISO 时间戳也不是 event_id", entity="event", entity_id=upto
        ) from None
    async with db.session() as session:
        row = (
            await session.execute(
                select(events_table.c.ts).where(events_table.c.event_id == event_id)
            )
        ).first()
    if row is None:
        raise NotFoundError(f"event {upto} not found", entity="event", entity_id=upto)
    return _as_utc(row.ts)


async def _load_node_events(db: Database, node_ids: Sequence[UUID]) -> list[Event]:
    """文档全部节点的事件（**不带时间下界**：折叠需要各节点自己的 create）。"""
    events: list[Event] = []
    for start in range(0, len(node_ids), _EVENT_BATCH):
        chunk = [str(node_id) for node_id in node_ids[start : start + _EVENT_BATCH]]
        statement = (
            select(*EVENT_COLUMNS)
            .where(events_table.c.entity == "node", events_table.c.entity_id.in_(chunk))
            .order_by(events_table.c.ts, events_table.c.event_id)
        )
        async with db.session() as session:
            rows = (await session.execute(statement)).all()
        events.extend(build_model(Event, row_to_dict(row)) for row in rows)
    events.sort(key=lambda event: (event.ts, event.event_id))
    return events


async def _load_ref_events(
    db: Database, low: datetime | None, high: datetime | None
) -> list[Event]:
    """`ref` 事件的候选集（按 `ts` 窗口裁剪；`src` 归属在调用侧按 payload 过滤）。

    下界取 `from_ts`（无则文档自身首个事件的 `ts`）：节点的 ref 事件必然晚于其所属文档创建。
    """
    statement = select(*EVENT_COLUMNS).where(events_table.c.entity == "ref")
    if low is not None:
        statement = statement.where(events_table.c.ts >= low)
    if high is not None:
        statement = statement.where(events_table.c.ts <= high)
    statement = statement.order_by(events_table.c.ts, events_table.c.event_id)
    async with db.session() as session:
        rows = (await session.execute(statement)).all()
    return [build_model(Event, row_to_dict(row)) for row in rows]


def _id_texts(node_ids: Sequence[UUID]) -> set[str]:
    """节点 id 的文本形态（与 `events.entity_id` / ref payload `src` 的落库口径一致）。"""
    return {str(node_id) for node_id in node_ids}


def _ref_src(event: Event) -> str | None:
    payload = event.payload or {}
    src = payload.get("src")
    return str(src) if src is not None else None


def _fold_nodes(events: Sequence[Event], moment: datetime | None) -> dict[UUID, Node]:
    """节点事件 → 该时点的节点态（`apply_events` 折叠，A18/P5 单一口径）。"""
    grouped: dict[str, list[Event]] = defaultdict(list)
    for event in events:
        if moment is None or event.ts <= moment:
            grouped[event.entity_id].append(event)
    states: dict[UUID, Node] = {}
    for entity_id, group in grouped.items():
        folded = apply_events("node", group)
        if isinstance(folded, NodeSnapshot) and folded.node is not None:
            states[UUID(entity_id)] = folded.node
    return states


def _fold_refs(events: Sequence[Event], moment: datetime | None) -> set[tuple[Any, ...]]:
    """引用边事件 → 该时点的边集合（add 追加 / remove 移除，§3.5）。"""
    keys: set[tuple[Any, ...]] = set()
    for event in events:
        if moment is not None and event.ts > moment:
            continue
        payload = event.payload or {}
        key = (
            str(payload.get("src")),
            str(payload.get("dst_doc")),
            str(payload.get("dst_node")) if payload.get("dst_node") is not None else None,
            str(payload.get("kind")),
        )
        if event.op == "add":
            keys.add(key)
        else:
            keys.discard(key)
    return keys


def _node_view(node: Node) -> dict[str, Any]:
    """节点视图（camelCase + JSON 安全；用于 diff 的 `before`/`after`）。"""
    return node.model_dump(by_alias=True, mode="json")


def _node_changes(before: dict[UUID, Node], after: dict[UUID, Node]) -> list[DiffEntry]:
    """两时点节点态 → 变更清单（新增/修改/软删；修改逐字段）。"""
    changes: list[DiffEntry] = []
    for node_id in sorted(before.keys() | after.keys(), key=str):
        old = before.get(node_id)
        new = after.get(node_id)
        if old is None and new is not None:
            changes.append(
                DiffEntry(
                    node_id=node_id,
                    anchor=new.anchor,
                    op="added",
                    field="node",
                    before=None,
                    after=_node_view(new),
                )
            )
            continue
        if old is not None and new is None:
            changes.append(
                DiffEntry(
                    node_id=node_id,
                    anchor=old.anchor,
                    op="deleted",
                    field="node",
                    before=_node_view(old),
                    after=None,
                )
            )
            continue
        assert old is not None and new is not None  # 上方两分支已覆盖 None 情形
        if old.status != "deleted" and new.status == "deleted":
            changes.append(
                DiffEntry(
                    node_id=node_id,
                    anchor=old.anchor,
                    op="deleted",
                    field="node",
                    before=_node_view(old),
                    after=_node_view(new),
                )
            )
            continue
        for field in _NODE_DIFF_FIELDS:
            old_value = getattr(old, field)
            new_value = getattr(new, field)
            if old_value != new_value:
                changes.append(
                    DiffEntry(
                        node_id=node_id,
                        anchor=new.anchor,
                        op="modified",
                        field=field,
                        before=_jsonable(old_value),
                        after=_jsonable(new_value),
                    )
                )
    return changes


def _ref_changes(
    before: set[tuple[Any, ...]], after: set[tuple[Any, ...]]
) -> list[DiffEntry]:
    """两时点引用边集合 → 变更清单（节点 id 仍存在的边挂到该节点，否则 `nodeId=None`）。"""
    changes: list[DiffEntry] = []
    for key in sorted(before - after, key=str):
        changes.append(
            DiffEntry(
                node_id=_maybe_uuid(key[0]),
                op="deleted",
                field="ref",
                before=_ref_view(key),
                after=None,
            )
        )
    for key in sorted(after - before, key=str):
        changes.append(
            DiffEntry(
                node_id=_maybe_uuid(key[0]),
                op="added",
                field="ref",
                before=None,
                after=_ref_view(key),
            )
        )
    return changes


def _ref_view(key: tuple[Any, ...]) -> dict[str, Any]:
    return {"src": key[0], "dstDoc": key[1], "dstNode": key[2], "kind": key[3]}


def _maybe_uuid(value: Any) -> UUID | None:
    try:
        return UUID(str(value))
    except (TypeError, ValueError):
        return None


def _jsonable(value: Any) -> Any:
    """UUID/日期 → JSON 安全值（diff 载荷里也可能出现嵌套 UUID）。"""
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


async def _key_fingerprints(db: Database) -> dict[UUID, list[str]]:
    """用户 → 未吊销公钥指纹集（`GET /users` 的 `keyFingerprints`）。"""
    statement = (
        select(ssh_keys_table.c.user_id, ssh_keys_table.c.key_id)
        .where(ssh_keys_table.c.revoked_at.is_(None))
        .order_by(ssh_keys_table.c.key_id)
    )
    async with db.session() as session:
        rows = (await session.execute(statement)).all()
    grouped: dict[UUID, list[str]] = defaultdict(list)
    for row in rows:
        grouped[row.user_id].append(str(row.key_id))
    return grouped
