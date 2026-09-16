"""M02 表定义（SQLAlchemy Core）——字段与约束逐字对齐 §4 DDL，分区按 ADR-009 §4.2。

设计要点：

- **13 表**：`docs` `nodes` `refs` `events` `comments` `schemas` `assets` `terms`
  `users` `ssh_keys` `grants` `sessions` `nonces`（§4）。
- **分区**：`nodes` HASH(doc_id) 64 分区、`events` RANGE(ts) 按月 + DEFAULT（ADR-009 §1）。
  分区子表**不建 Table 对象**（保持 metadata 恰为 13 表）；DDL 由本模块的分区函数生成。
- **主键含分区键**（ADR-009）：`nodes` → `(node_id, doc_id)`；`events` → `(event_id, ts)`。
- **外键降级（ADR-009 §1 六处）**：分区表参与的外键在 PG 无法成立，改为应用层校验
  （见 `nodes.py`/`refs.py`/`comments.py`）；仅保留 `nodes.doc_id → docs(doc_id)`
  与身份四表（`users` 不分区）的外键。
- **append-only**：`events` 无 UPDATE/DELETE 路径，库层由 `privilege_statements()`
  的授权口径兜底（P2）。
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Final, Sequence

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    Computed,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    SmallInteger,
    Table,
    TIMESTAMP,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.dialects.postgresql import UUID as PGUUID

__all__ = [
    "NODES_PARTITION_COUNT",
    "TABLES",
    "assets",
    "comments",
    "docs",
    "events",
    "events_partition_name",
    "events_partition_statements",
    "grants",
    "metadata",
    "nodes",
    "nodes_partition_name",
    "nodes_partition_statements",
    "nonces",
    "privilege_statements",
    "refs",
    "schemas",
    "sessions",
    "ssh_keys",
    "terms",
    "users",
]

metadata = MetaData()

NODES_PARTITION_COUNT: Final = 64
"""ADR-009 §1：`nodes` HASH(doc_id) 64 分区。"""

EVENTS_PARTITION_PREFIX: Final = "events_"
EVENTS_DEFAULT_PARTITION: Final = "events_default"


def _pk_uuid(name: str) -> Column[Any]:
    return Column(name, PGUUID(as_uuid=True), primary_key=True)


def _uuid(name: str, *, nullable: bool = True) -> Column[Any]:
    return Column(name, PGUUID(as_uuid=True), nullable=nullable)


def _ts(name: str, *, nullable: bool = False, default_now: bool = True) -> Column[Any]:
    return Column(
        name,
        TIMESTAMP(timezone=True),
        nullable=nullable,
        server_default=text("now()") if default_now else None,
    )


# --------------------------------------------------------------------- 文档与节点

docs: Final = Table(
    "docs",
    metadata,
    Column("doc_id", Text, primary_key=True),
    Column("doc_type", Text, nullable=False),
    Column("title", Text, nullable=False),
    Column("meta", JSONB, nullable=False, server_default=text("'{}'::jsonb")),
    Column("source_ref", Text),
    Column("status", Text, nullable=False, server_default=text("'draft'")),
    Column("version", BigInteger, nullable=False, server_default=text("1")),
    _ts("created_at"),
    _ts("updated_at"),
    CheckConstraint(
        "doc_type IN ('standard','lang','tool-manual','product','safety')",
        name="docs_doc_type_check",
    ),
    CheckConstraint(
        "status IN ('draft','reviewed','approved')",
        name="docs_status_check",
    ),
)

nodes: Final = Table(
    "nodes",
    metadata,
    _pk_uuid("node_id"),
    Column("doc_id", Text, ForeignKey("docs.doc_id"), primary_key=True),
    Column("atom_type", Text, nullable=False),
    Column("format", Text, nullable=False, server_default=text("'md'")),
    Column("ordinal", Integer, nullable=False),
    # ADR-009：nodes.parent_node_id → nodes(node_id) 外键降级（应用层校验，见 nodes.py）
    _uuid("parent_node_id"),
    Column("level", SmallInteger),
    Column("anchor", Text, nullable=False),
    Column("content", JSONB, nullable=False),
    Column("status", Text, nullable=False, server_default=text("'active'")),
    Column("version", BigInteger, nullable=False, server_default=text("1")),
    _ts("created_at"),
    _ts("updated_at"),
    Column(
        "text_fts",
        TSVECTOR,
        Computed("to_tsvector('english', coalesce(content->>'text',''))", persisted=True),
    ),
    CheckConstraint("format IN ('md','html','text')", name="nodes_format_check"),
    CheckConstraint("status IN ('active','deleted')", name="nodes_status_check"),
    UniqueConstraint("doc_id", "anchor", name="nodes_doc_anchor_key"),
    postgresql_partition_by="HASH (doc_id)",
)

Index("idx_nodes_doc_ordinal", nodes.c.doc_id, nodes.c.ordinal)
Index("idx_nodes_parent", nodes.c.parent_node_id)
Index("idx_nodes_fts", nodes.c.text_fts, postgresql_using="gin")

# ------------------------------------------------------------------------- 引用边

refs: Final = Table(
    "refs",
    metadata,
    _pk_uuid("ref_id"),
    # ADR-009：refs.src_node_id / dst_node_id → nodes 外键降级（M09B broken_refs 兜底）
    _uuid("src_node_id", nullable=False),
    Column("dst_doc_id", Text, nullable=False),
    _uuid("dst_node_id"),
    Column("kind", Text, nullable=False),
    CheckConstraint(
        "kind IN ('traces_to','see_also','composes_from','source_ref')",
        name="refs_kind_check",
    ),
    # PG15+：NULL 参与唯一性（文档级引用 dst_node_id IS NULL 合法，A5/R1）
    UniqueConstraint(
        "src_node_id",
        "dst_doc_id",
        "dst_node_id",
        "kind",
        name="refs_unique",
        postgresql_nulls_not_distinct=True,
    ),
)

Index("idx_refs_dst", refs.c.dst_doc_id, refs.c.dst_node_id)
Index("idx_refs_src", refs.c.src_node_id)

# --------------------------------------------------------------------- 事件（审计）

events: Final = Table(
    "events",
    metadata,
    _pk_uuid("event_id"),
    Column("entity", Text, nullable=False),
    Column("entity_id", Text, nullable=False),
    Column("op", Text, nullable=False),
    Column("payload", JSONB, nullable=False),
    Column("actor", Text, nullable=False),
    # PK 含分区键（ADR-009）：events PK = (event_id, ts)
    Column("ts", TIMESTAMP(timezone=True), primary_key=True, nullable=False, server_default=text("now()")),
    CheckConstraint(
        "entity IN ('doc','node','ref','comment','schema','auth')",
        name="events_entity_check",
    ),
    postgresql_partition_by="RANGE (ts)",
)

Index("idx_events_entity", events.c.entity, events.c.entity_id, events.c.ts)
Index("idx_events_ts", events.c.ts)

# ------------------------------------------------------------------------- 批注

comments: Final = Table(
    "comments",
    metadata,
    _pk_uuid("comment_id"),
    # ADR-009：comments.node_id / target_event_id 外键降级（软删方案下无级联，A2）
    _uuid("node_id", nullable=False),
    _uuid("target_event_id"),
    Column("body", Text, nullable=False),
    Column("state", Text, nullable=False, server_default=text("'open'")),
    Column("author", Text, nullable=False),
    Column("version", BigInteger, nullable=False, server_default=text("1")),
    _ts("ts"),
    CheckConstraint("state IN ('open','resolved','orphaned')", name="comments_state_check"),
)

Index("idx_comments_node", comments.c.node_id, comments.c.state)

# ------------------------------------------------------------- 形态 / 资产 / 词表

schemas: Final = Table(
    "schemas",
    metadata,
    Column("type_name", Text, primary_key=True),
    Column("json_schema", JSONB, nullable=False),
    Column("version", Integer, nullable=False, server_default=text("1"), primary_key=True),
)

assets: Final = Table(
    "assets",
    metadata,
    Column("asset_id", Text, primary_key=True),
    Column("mime", Text, nullable=False),
    Column("bytes", BigInteger, nullable=False),
    Column("origin", Text),
    Column("path", Text, nullable=False),
)

terms: Final = Table(
    "terms",
    metadata,
    Column("term", Text, primary_key=True),
    # ADR-009：terms.definition_node_id 外键降级
    _uuid("definition_node_id"),
    Column("kind", Text, nullable=False),
    CheckConstraint(
        "kind IN ('glossary','normative-keyword')",
        name="terms_kind_check",
    ),
)

# ------------------------------------------------------------------ 鉴权与用户（M10）

users: Final = Table(
    "users",
    metadata,
    _pk_uuid("user_id"),
    Column("username", Text, nullable=False, unique=True),
    Column("role", Text, nullable=False),
    Column("status", Text, nullable=False, server_default=text("'active'")),
    _ts("created_at"),
    _ts("updated_at"),
    CheckConstraint(
        "role IN ('admin','editor','reviewer','reader')",
        name="users_role_check",
    ),
    CheckConstraint("status IN ('active','disabled')", name="users_status_check"),
)

ssh_keys: Final = Table(
    "ssh_keys",
    metadata,
    Column("key_id", Text, primary_key=True),
    Column("user_id", PGUUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False),
    Column("public_key", Text, nullable=False),
    Column("key_type", Text, nullable=False),
    _ts("added_at"),
    _ts("revoked_at", nullable=True, default_now=False),
    UniqueConstraint("user_id", "key_id", name="ssh_keys_user_id_key_id_key"),
    CheckConstraint(
        "key_type IN ('ssh-ed25519','rsa-sha2-512','rsa-sha2-256')",
        name="ssh_keys_key_type_check",
    ),
)

Index("idx_ssh_keys_user", ssh_keys.c.user_id, postgresql_where=text("revoked_at IS NULL"))

grants: Final = Table(
    "grants",
    metadata,
    _pk_uuid("grant_id"),
    Column("user_id", PGUUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False),
    Column("scope", Text, nullable=False),
    Column("value", Text, nullable=False),
    Column("permission", Text, nullable=False),
    Column("granted_by", PGUUID(as_uuid=True), ForeignKey("users.user_id")),
    _ts("granted_at"),
    UniqueConstraint("user_id", "scope", "value", "permission", name="grants_user_id_scope_value_permission_key"),
    CheckConstraint("scope IN ('doc_type','doc')", name="grants_scope_check"),
    CheckConstraint("permission IN ('read','write','review')", name="grants_permission_check"),
)

sessions: Final = Table(
    "sessions",
    metadata,
    _pk_uuid("session_id"),
    Column("user_id", PGUUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False),
    Column("token_hash", Text, nullable=False, unique=True),
    _ts("created_at"),
    _ts("expires_at", default_now=False, nullable=False),
    _ts("last_seen_at"),
)

Index("idx_sessions_expiry", sessions.c.expires_at)

nonces: Final = Table(
    "nonces",
    metadata,
    Column("nonce", Text, primary_key=True),
    Column("user_id", PGUUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE")),
    _ts("seen_at"),
)

Index("idx_nonces_seen", nonces.c.seen_at)

TABLES: Final = tuple(metadata.tables)

# ------------------------------------------------------------------- 分区 DDL 生成


def nodes_partition_name(index: int) -> str:
    """`nodes_p<i>`（§4.2 命名）。"""
    return f"nodes_p{index}"


def nodes_partition_statements(modulus: int = NODES_PARTITION_COUNT) -> list[str]:
    """64 个 HASH 分区 DDL（`CREATE TABLE IF NOT EXISTS`，可重复执行）。"""
    return [
        f"CREATE TABLE IF NOT EXISTS {nodes_partition_name(i)} PARTITION OF nodes "
        f"FOR VALUES WITH (MODULUS {modulus}, REMAINDER {i})"
        for i in range(modulus)
    ]


def events_partition_name(month_start: datetime) -> str:
    """`events_<YYYYMM>`（月份起点决定分区名）。"""
    return f"{EVENTS_PARTITION_PREFIX}{month_start:%Y%m}"


def _month_start(moment: datetime) -> datetime:
    return moment.astimezone(timezone.utc).replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )


def _next_month(month_start: datetime) -> datetime:
    year, month = month_start.year, month_start.month
    return month_start.replace(year=year + 1, month=1) if month == 12 else month_start.replace(month=month + 1)


def events_partition_statements(
    reference: datetime | None = None,
    *,
    ahead_months: int = 3,
    include_default: bool = True,
) -> list[str]:
    """当前月 + 未来 ``ahead_months`` 个月分区，以及 DEFAULT 兜底分区（ADR-009 V3）。

    预建保证「缺分区不致写入失败」；DEFAULT 分区让维护任务漏建月份时写入仍成功，
    由 M09B `perf_health`（`DTO_PARTITION_MISSING`）告警。
    """
    start = _month_start(reference or datetime.now(timezone.utc))
    statements: list[str] = []
    for offset in range(ahead_months + 1):
        month = start
        for _ in range(offset):
            month = _next_month(month)
        following = _next_month(month)
        statements.append(
            f"CREATE TABLE IF NOT EXISTS {events_partition_name(month)} PARTITION OF events "
            f"FOR VALUES FROM ('{month.isoformat()}') TO ('{following.isoformat()}')"
        )
    if include_default:
        statements.append(
            f"CREATE TABLE IF NOT EXISTS {EVENTS_DEFAULT_PARTITION} PARTITION OF events DEFAULT"
        )
    return statements


# ----------------------------------------------------------------- 角色授权 DDL（P2）

MUTABLE_TABLES: Final[tuple[str, ...]] = (
    "docs",
    "nodes",
    "refs",
    "comments",
    "schemas",
    "assets",
    "terms",
    "users",
    "ssh_keys",
    "grants",
    "sessions",
    "nonces",
)
"""允许 UPDATE/DELETE 的表；`events`（及其全部月分区）只给 SELECT/INSERT（P2 append-only）。"""


def privilege_statements(
    connection: Any,
    *,
    app_role: str = "agenticdocer_app",
    include_default_privileges: bool = True,
) -> tuple[list[str], list[str]]:
    """产出 §4.3 的 GRANT/REVOKE 语句（返回 `(statements, skipped_notes)`）。

    工作方式说明（与 §4.3 的关系）：§4.3 写的是
    「`GRANT S,I,U,D ON ALL TABLES` 后 `REVOKE UPDATE, DELETE ON events`」。分区化之后
    该口径**不足**——PG 的分区各自持有 ACL，仅 REVOKE 父表无法阻止经父表路由的
    UPDATE/DELETE 落到月分区；且 `ALTER DEFAULT PRIVILEGES` 会把 U/D 授给**未来**的 events
    月分区，使 append-only 随时间失效。故此处**强化**为：逐表列出（含分区）授予 S/I，
    仅 `MUTABLE_TABLES` 追加 U/D，默认权限只授 S/I。语义是 §4.3 的超集，不变量更强。

    角色不存在时跳过（建库阶段由 §4.3 的 `CREATE ROLE` 负责，迁移不创建角色）。
    """
    notes: list[str] = []
    rows = connection.execute(
        text("SELECT 1 FROM pg_roles WHERE rolname = :role"), {"role": app_role}
    ).first()
    if rows is None:
        notes.append(f"role {app_role!r} absent: grants skipped (owner creates roles per §4.3)")
        return [], notes

    statements = [
        f"GRANT CONNECT ON DATABASE {connection.dialect.identifier_preparer.quote(connection.engine.url.database)} TO {app_role}",
        f"GRANT USAGE ON SCHEMA public TO {app_role}",
        f"GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO {app_role}",
    ]
    partitions = connection.execute(
        text(
            "SELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace "
            "WHERE n.nspname = 'public' AND c.relkind = 'r' ORDER BY c.relname"
        )
    ).scalars()
    for relname in partitions:
        statements.append(f"GRANT SELECT, INSERT ON TABLE {relname} TO {app_role}")
        if relname in MUTABLE_TABLES:
            statements.append(f"GRANT UPDATE, DELETE ON TABLE {relname} TO {app_role}")
        else:
            statements.append(f"REVOKE UPDATE, DELETE, TRUNCATE ON TABLE {relname} FROM {app_role}")
    if include_default_privileges:
        statements.append(
            f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT ON TABLES TO {app_role}"
        )
    return statements, notes
