"""M01 领域模型：公共类型定义（架构规范 §3.0 / §3 M10 / §4 DDL）。

权威来源：`spec/arch_spec/architecture_specification.md` §3.0「公共类型定义（A14）」、
§3 M10「身份与密钥」、§3.5「事件载荷与折叠规范」、§4「数据库 DDL」。

约定：
- **序列化口径（§6 横切，A11）**：Python/DB 内部一律 snake_case；HTTP JSON 一律 camelCase。
  经 ``alias_generator=to_camel`` 实现——``model_dump(by_alias=True)`` 出 camelCase，
  ``model_validate`` 同时接受 snake_case 与 camelCase（``populate_by_name=True``）。
- **未知字段一律拒绝**（``extra="forbid"``）：写入契约必须显式，避免 agent 提交的拼错字段
  被静默丢弃（P1：结构化库为唯一权威源）。
- **可选性照抄 §3.0**：写作 ``X | None`` 而未给默认值者仍是**必填**字段（调用方显式传
  ``None``）；仅 §3.0 写明的默认值存在（``NodeIn.format="md"``、``DocTypeTarget.kind``、
  ``DocTarget.kind``）。§3.0 未定义的类型（``Ref``/``SchemaDef``/``Asset``/``Term``/
  ``Session``）按 §4 DDL 列定义推导，§3 M10 的 ``User``/``SshKey``/``Grant`` 亦按 §4 DDL
  补全列（Main 裁决 2026-09-16：M10/M02 需回读三表全列），可选性沿用同一口径（DB nullable
  列 → 必填的 ``X | None``；DB 有默认值的列不设 Python 默认值，值以库为准）。
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

# ── 基础类型与取值域（单一判定口径：各枚举仅在此处定义一次）────────────────

UUID7 = UUID
"""UUIDv7：应用侧生成（时间有序）——生成器见 :mod:`agenticdocer.model.uuid7`。"""

Format = Literal["md", "html", "text"]
NodeStatus = Literal["active", "deleted"]  # A2：软删
DocStatus = Literal["draft", "reviewed", "approved"]
CommentState = Literal["open", "resolved", "orphaned"]
RefKind = Literal["traces_to", "see_also", "composes_from", "source_ref"]
AtomType = Literal["clause", "definition", "table", "figure", "code", "example", "note", "cross_ref"]
DocType = Literal["standard", "lang", "tool-manual", "product", "safety"]  # A22 取值域
EntityKind = Literal["doc", "node", "ref", "comment", "schema", "auth"]
WriteSource = Literal["agent", "webui", "cli", "importer", "system"]
RoleName = Literal["admin", "editor", "reviewer", "reader"]
UserStatus = Literal["active", "disabled"]
GrantScope = Literal["doc_type", "doc"]  # S5：repo scope 已删除（无数据模型支撑）
GrantPermission = Literal["read", "write", "review"]  # S5：无 'admin'（不可经由 grant 提权）
TermKind = Literal["glossary", "normative-keyword"]
SshKeyType = Literal["ssh-ed25519", "rsa-sha2-512", "rsa-sha2-256"]  # §4 DDL ssh_keys.key_type

EventOp = Literal[
    "create",
    "update",
    "delete",
    "status",
    "add",
    "remove",
    # §3.5：auth 审计事件（B2）——§3.0 的 6 值字面量漏列，此处按 §3.5 补齐
    "login",
    "logout",
    "fail",
    "user_change",
    "grant_change",
    "key_change",
]
"""事件 op 取值域 = §3.0（实体事件）∪ §3.5（auth 审计事件）。

§3.5 为「事件载荷与折叠」的权威表：`doc`/`node`/`comment`/`schema` 用 create/update/delete/status，
`ref` 用 add/remove，`auth` 用 login/logout/fail/user_change/grant_change/key_change。
（DDL `events.op` 为无 CHECK 的 text，故模型层是本取值域的唯一机检口径。）
"""


class Model(BaseModel):
    """全部公共类型的基类：camelCase 序列化（§6）+ 未知字段拒绝 + 按字段名填充。"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )


# ── §3.0：写入身份、节点、文档 ──────────────────────────────────────────


class WriteContext(Model):
    """A3：一切写入的身份与来源（取值规则见 §6；M06/M07 由验签结果填充，不信任客户端自述）。"""

    actor: str = Field(min_length=1)
    source: WriteSource


class NodeIn(Model):
    """节点写入输入（§3.0）。``node_id`` 为空时由调用方经 ``new_uuid7()`` 生成。"""

    node_id: UUID7 | None
    doc_id: str = Field(min_length=1)
    atom_type: str = Field(min_length=1)
    format: Format = "md"
    ordinal: int = Field(ge=0)
    parent_node_id: UUID7 | None
    level: int | None
    anchor: str = Field(min_length=1)
    content: dict[str, Any]


class Node(NodeIn):
    """节点当前态（含软删状态与乐观锁版本）。"""

    node_id: UUID7
    status: NodeStatus
    version: int = Field(ge=1)
    created_at: datetime
    updated_at: datetime
    # 注：nodes.text_fts 为生成列（§4 DDL / A10），非领域字段，不在模型中。


class DocIn(Model):
    """文档写入输入（§3.0）。``meta`` 保真承载 frontmatter 全量（§6 映射表）。"""

    doc_id: str = Field(min_length=1)
    doc_type: str = Field(min_length=1)
    title: str
    meta: dict[str, Any]
    source_ref: str | None


class Doc(DocIn):
    """文档当前态。"""

    status: DocStatus
    version: int = Field(ge=1)
    created_at: datetime
    updated_at: datetime


# ── §3.0：M03 导入解析的提议与统计 ─────────────────────────────────────


class RawFallback(Model):
    """未映射块兜底（note/code），不丢弃源内容（design_doc §6.1）。"""

    atom_type: Literal["note", "code"]
    format: Literal["html", "md"]
    text: str
    source_lines: tuple[int, int]


class UnmappedBlock(Model):
    source_lines: tuple[int, int]
    reason: str
    fallback: RawFallback


class Proposal(Model):
    proposal_id: str = Field(min_length=1)
    rule_id: str = Field(min_length=1)
    confident: bool
    source_lines: tuple[int, int]
    atom: Union[NodeIn, RawFallback]


class ParseStats(Model):
    total_blocks: int = Field(ge=0)
    rule_covered: int = Field(ge=0)
    fallback: int = Field(ge=0)
    pending: int = Field(ge=0)


class ParseResult(Model):
    doc_meta: dict[str, Any]
    proposals: list[Proposal]
    unmapped: list[UnmappedBlock]
    stats: ParseStats


# ── §3.0：事件、引用、批注、快照 ───────────────────────────────────────


class Event(Model):
    """append-only 变更日志（P2）。载荷形状与折叠规则见 §3.5。"""

    event_id: UUID7
    entity: EntityKind
    entity_id: str = Field(min_length=1)
    op: EventOp
    payload: dict[str, Any]
    actor: str = Field(min_length=1)
    ts: datetime


class Ref(Model):
    """引用边（§4 DDL `refs`；A5 修订：代理主键 + NULL 参与唯一）。"""

    ref_id: UUID7
    src_node_id: UUID7
    dst_doc_id: str = Field(min_length=1)
    dst_node_id: UUID7 | None
    kind: RefKind


class Comment(Model):
    """批注（独立表，不触 `nodes.content`；A4：``version`` 为乐观锁）。"""

    comment_id: UUID7
    node_id: UUID7
    target_event_id: UUID7 | None
    body: str
    state: CommentState
    author: str = Field(min_length=1)
    version: int = Field(ge=1)
    ts: datetime


class NodeSnapshot(Model):
    """`apply_events` 折叠结果（A18）：``node=None`` 表示折叠序列中无 create。"""

    node: Node | None
    history: list[Event]


class SchemaDef(Model):
    """Schema 注册表行（§4 DDL `schemas`）；八类原子 + 2 变体由 M01 定义（见 `atoms.py`）。"""

    type_name: str = Field(min_length=1)
    json_schema: dict[str, Any]
    version: int = Field(ge=1)


class Asset(Model):
    """内容寻址资产（§4 DDL `assets`；``asset_id`` = sha256 hex）。"""

    asset_id: str = Field(min_length=1)
    mime: str = Field(min_length=1)
    bytes: int = Field(ge=0)
    origin: str | None
    path: str


class Term(Model):
    """术语/规范性关键词（R10；§4 DDL `terms`）。"""

    term: str = Field(min_length=1)
    definition_node_id: UUID7 | None
    kind: TermKind


class Violation(Model):
    """统一违规结构（§6：M09A/M09B 与 M06 错误映射共用）。"""

    rule_id: str = Field(min_length=1)
    path: str
    message: str
    fix_hint: str | None


# ── §3.0：检索/渲染/提交/导出结果 ──────────────────────────────────────


class SearchHit(Model):
    node_id: UUID7
    doc_id: str
    anchor: str
    score: float


class TraversalHit(Model):
    node_id: UUID7
    doc_id: str
    anchor: str
    hops: int = Field(ge=0)
    via: list[RefKind]


class RenderResult(Model):
    doc_id: str
    out_path: str
    assets_exported: int = Field(ge=0)


class CommitResult(Model):
    doc_id: str
    nodes_created: int = Field(ge=0)
    refs_created: int = Field(ge=0)
    stats: ParseStats


class QualityReport(Model):
    detector_id: str = Field(min_length=1)
    violations: list[Violation]


class ExportResult(Model):
    out_path: str
    docs: int = Field(ge=0)
    nodes: int = Field(ge=0)


class AssetSyncReport(Model):
    fetched: int = Field(ge=0)
    missing: list[str]
    total_refs: int = Field(ge=0)


class QualityScope(Model):
    doc_ids: list[str] | None
    detectors: list[str] | None


# ── §3.0：授权目标（S5 修复：repo scope 已删除）─────────────────────────


class DocTypeTarget(Model):
    kind: Literal["doc_type"] = "doc_type"
    value: str = Field(min_length=1)


class DocTarget(Model):
    kind: Literal["doc"] = "doc"
    value: str = Field(min_length=1)


#: 任务书命名的别名（与 §3.0 的类同物）：授权目标 = 文档类型 | 文档
GrantTargetDocType = DocTypeTarget
GrantTargetDoc = DocTarget
GrantTarget = Union[DocTypeTarget, DocTarget]


# ── §3 M10：身份、密钥、授权、会话 ─────────────────────────────────────


class User(Model):
    """§3 M10 + §4 DDL 补列（Main 裁决 2026-09-16：M10/M02 需回读 `users` 全列）。

    ``user_id`` 统一取 ``UUID7``（对齐 DDL ``uuid`` 列；§3 M10 代码块中的 ``str`` 为笔误，
    同块内 ``Session.user_id`` 又写 uuid 语义）。审计字符串 ``WriteContext.actor`` 仍为
    ``str``，由 M10 在写入派生值时显式 ``str(user_id)`` 一次转换（转换点收敛在一处）。
    """

    user_id: UUID7
    username: str = Field(min_length=1)
    role: RoleName
    status: UserStatus
    created_at: datetime
    updated_at: datetime


class SshKey(Model):
    """§3 M10 + §4 DDL 补列（Main 裁决 2026-09-16）。``key_id`` = SHA256 指纹
    （与 `ssh-keygen -lf` 一致）；``user_id`` 按 DDL 为 uuid 列，故取 ``UUID7``。"""

    key_id: str = Field(min_length=1)
    fingerprint: str = Field(min_length=1)
    user_id: UUID7
    public_key: str = Field(min_length=1)
    key_type: SshKeyType
    added_at: datetime
    revoked_at: datetime | None


class Grant(Model):
    """文档集级授权（B3）。取值域按 **S5 修复**（§3.0/§4 DDL）：scope ∈ {doc_type, doc}、
    permission ∈ {read, write, review}；§3 M10 代码块仍写作 repo/admin，已被 S5 取代。
    ``granted_by``/``granted_at`` 为 §4 DDL 列（Main 裁决 2026-09-16 补入）。"""

    grant_id: str = Field(min_length=1)
    user_id: UUID7
    scope: GrantScope
    value: str = Field(min_length=1)
    permission: GrantPermission
    granted_by: UUID7 | None
    granted_at: datetime


class Session(Model):
    """WebUI 会话（§4 DDL `sessions`；明文 token 仅存 Cookie，库内仅存 SHA256）。

    ``user_id`` 与 ``User.user_id`` 同为 ``UUID7``（Main 裁决 2026-09-16 统一口径）。
    """

    session_id: UUID7
    user_id: UUID7
    token_hash: str = Field(min_length=1)
    created_at: datetime
    expires_at: datetime
    last_seen_at: datetime


__all__ = [
    # 基础类型与取值域
    "UUID7",
    "Format",
    "NodeStatus",
    "DocStatus",
    "CommentState",
    "RefKind",
    "AtomType",
    "DocType",
    "EntityKind",
    "EventOp",
    "WriteSource",
    "RoleName",
    "TermKind",
    "SshKeyType",
    "GrantScope",
    "GrantPermission",
    "TermKind",
    "Model",
    # 身份与节点/文档
    "WriteContext",
    "NodeIn",
    "Node",
    "DocIn",
    "Doc",
    # 导入提议
    "RawFallback",
    "UnmappedBlock",
    "Proposal",
    "ParseStats",
    "ParseResult",
    # 事件与实体
    "Event",
    "Ref",
    "Comment",
    "NodeSnapshot",
    "SchemaDef",
    "Asset",
    "Term",
    "Violation",
    # 结果类型
    "SearchHit",
    "TraversalHit",
    "RenderResult",
    "CommitResult",
    "QualityReport",
    "ExportResult",
    "AssetSyncReport",
    "QualityScope",
    # 授权目标
    "DocTypeTarget",
    "DocTarget",
    "GrantTargetDocType",
    "GrantTargetDoc",
    "GrantTarget",
    # M10 身份
    "User",
    "SshKey",
    "Grant",
    "Session",
]
