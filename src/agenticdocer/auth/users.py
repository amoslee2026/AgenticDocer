"""M10 用户 / SSH 公钥 / 授权管理（REQ-M10-F03/F04；S9；S1/S10 审计）。

写路径一律**单事务「实体 + 审计事件」**（与 M02 的 P2 口径一致）；审计事件
``entity='auth'``，op ∈ {``user_change``, ``key_change``, ``grant_change``, ``fail``,
``login``, ``logout``}（§3.5）。

**S9 最后管理员防护**（违规 → 409）：

* 不可 disable / demote / delete **自身**（``actor_id`` = 操作者 ``user_id``）；
* 不可操作**最后一个 active admin**（提示先指定继任者）。

**S10 审计防污染**：失败事件 ``actor='anonymous'``；请求自述身份只写 ``claimed_*``
字段，绝不写 ``user_id``/``key_fingerprint``（本模块的写方法均要求 ``actor`` 显式传参，
由 M06/M07 从**验签结果**取值，不信任客户端自述）。

**公钥登记口径**：``key_id`` = ``SHA256:<base64>`` 指纹（与 ``ssh-keygen -lf`` 一致）；
同一公钥**只允许登记到一个用户**（否则身份归属不唯一）；吊销保留行（审计），重新登记
同一 ``(user, key)`` 复用该行并清空 ``revoked_at``。
"""

from __future__ import annotations

import threading
import time
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Final

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from agenticdocer.model import Grant, GrantScope, SshKey, User, new_uuid7
from agenticdocer.model.types import UserStatus
from agenticdocer.observability import get_logger
from agenticdocer.store import (
    ConflictError,
    Database,
    Event,
    ForbiddenError,
    NotFoundError,
    ValidationError,
    append_event,
    build_model,
    get_database,
    now,
    translate_integrity_error,
)
from agenticdocer.store.rows import as_uuid, row_to_dict
from agenticdocer.store.schema import grants, ssh_keys, users

from .errors import SignatureFormatError
from .rbac import ROLE_PERMISSIONS, authorize, validate_grant
from .signing import normalize_key_id
from .sshsig import validate_public_key

__all__ = [
    "DEFAULT_ADMIN_USERNAME",
    "GRANT_COLUMNS",
    "USER_COLUMNS",
    "add_ssh_key",
    "authorize_user",
    "count_active_admins",
    "create_grant",
    "create_user",
    "delete_grant",
    "delete_user",
    "fetch_active_key",
    "fetch_grants",
    "fetch_user",
    "fetch_user_by_username",
    "find_active_key",
    "find_user_by_username",
    "flush_auth_failure_aggregates",
    "get_user",
    "grant_from_row",
    "list_grants",
    "list_ssh_keys",
    "list_users",
    "load_grants",
    "log_auth_event",
    "log_auth_failure",
    "revoke_ssh_key",
    "ssh_key_from_row",
    "update_user",
    "user_from_row",
]

log = get_logger("m10.users")

DEFAULT_ADMIN_USERNAME: Final = "admin"

USER_COLUMNS: Final = tuple(users.c)
KEY_COLUMNS: Final = tuple(ssh_keys.c)
GRANT_COLUMNS: Final = tuple(grants.c)

_FAILURE_BUCKET_SECONDS: Final = 300
"""失败审计聚合窗口（§3 M10：按 ``(ip, 5min)`` 聚合，避免审计淹没）。"""


class _FailureBucket:
    """``(ip, reason)`` 在当前窗口内的失败计数（进程内，仅用于审计去噪）。"""

    __slots__ = ("bucket", "count", "endpoint", "method", "status_code")

    def __init__(
        self, bucket: int, endpoint: str | None, method: str | None, status_code: int
    ) -> None:
        self.bucket = bucket
        self.count = 0
        self.endpoint = endpoint
        self.method = method
        self.status_code = status_code


_failure_buckets: dict[tuple[str, str], _FailureBucket] = {}
_failure_lock = threading.Lock()


def _db(db: Database | None) -> Database:
    return db if db is not None else get_database()


def _mapping(row: Any) -> dict[str, Any]:
    """SQLAlchemy 行 / 普通 dict → 列名字典（写入路径回读刚构造的记录时用 dict）。"""
    return dict(row) if isinstance(row, Mapping) else row_to_dict(row)


def user_from_row(row: Any) -> User:
    """``users`` 行 → :class:`~agenticdocer.model.User`。"""
    return build_model(User, _mapping(row))


def ssh_key_from_row(row: Any) -> SshKey:
    """``ssh_keys`` 行 → :class:`~agenticdocer.model.SshKey`。

    DDL 无 ``fingerprint`` 列（``key_id`` 即指纹），M01 模型要求该字段，故此处补齐。
    """
    data = _mapping(row)
    data["fingerprint"] = data["key_id"]
    return build_model(SshKey, data)


def grant_from_row(row: Any) -> Grant:
    """``grants`` 行 → :class:`~agenticdocer.model.Grant`。"""
    return build_model(Grant, _mapping(row))


# ------------------------------------------------------------ 行读取（事务内共享）


async def fetch_user(session: AsyncSession, user_id: Any) -> dict[str, Any] | None:
    row = (
        await session.execute(select(*USER_COLUMNS).where(users.c.user_id == user_id))
    ).first()
    return row_to_dict(row) if row is not None else None


async def fetch_user_by_username(
    session: AsyncSession, username: str
) -> dict[str, Any] | None:
    row = (
        await session.execute(select(*USER_COLUMNS).where(users.c.username == username))
    ).first()
    return row_to_dict(row) if row is not None else None


async def fetch_active_key(session: AsyncSession, key_id: str) -> dict[str, Any] | None:
    """按 ``key_id`` 取**可用**公钥：``revoked_at IS NULL`` 且**属主 ``status='active'``**。

    S8：用户被 disable 后其密钥立即不可用（既有签名/会话同步失效）。
    """
    statement = (
        select(*KEY_COLUMNS)
        .join(users, users.c.user_id == ssh_keys.c.user_id)
        .where(
            ssh_keys.c.key_id == key_id,
            ssh_keys.c.revoked_at.is_(None),
            users.c.status == "active",
        )
    )
    row = (await session.execute(statement)).first()
    return row_to_dict(row) if row is not None else None


async def fetch_grants(session: AsyncSession, user_id: Any) -> list[dict[str, Any]]:
    statement = (
        select(*GRANT_COLUMNS)
        .where(grants.c.user_id == user_id)
        .order_by(grants.c.granted_at, grants.c.grant_id)
    )
    return [row_to_dict(row) for row in (await session.execute(statement)).all()]


async def count_active_admins(session: AsyncSession) -> int:
    """``status='active'`` 且 ``role='admin'`` 的用户数（S9 判据）。"""
    statement = select(func.count()).select_from(users).where(
        users.c.role == "admin", users.c.status == "active"
    )
    return int((await session.execute(statement)).scalar_one())


# --------------------------------------------------------------------- 用户管理


async def list_users(
    *, status: UserStatus | None = None, db: Database | None = None
) -> list[User]:
    statement = select(*USER_COLUMNS)
    if status is not None:
        statement = statement.where(users.c.status == status)
    statement = statement.order_by(users.c.created_at, users.c.username)
    async with _db(db).session() as session:
        rows = (await session.execute(statement)).all()
    return [user_from_row(row) for row in rows]


async def get_user(user_id: Any, *, db: Database | None = None) -> User:
    async with _db(db).session() as session:
        row = await fetch_user(session, user_id)
    if row is None:
        raise NotFoundError(f"user {user_id} not found", entity="auth", entity_id=str(user_id))
    return user_from_row(row)


async def find_user_by_username(username: str, *, db: Database | None = None) -> User | None:
    async with _db(db).session() as session:
        row = await fetch_user_by_username(session, username)
    return user_from_row(row) if row is not None else None


async def create_user(
    username: str,
    role: str,
    *,
    actor: str,
    status: UserStatus = "active",
    db: Database | None = None,
) -> User:
    """创建用户（用户名唯一冲突 → 409；角色/状态取值域 → 422）。"""
    name = username.strip()
    if not name:
        raise ValidationError("username must be non-empty", entity="auth")
    if role not in ROLE_PERMISSIONS:
        raise ValidationError(
            f"unknown role {role!r}; expected one of {sorted(ROLE_PERMISSIONS)}", entity="auth"
        )
    if status not in ("active", "disabled"):
        raise ValidationError(f"unknown status {status!r}", entity="auth")
    stamp = now()
    record = {
        "user_id": new_uuid7(),
        "username": name,
        "role": role,
        "status": status,
        "created_at": stamp,
        "updated_at": stamp,
    }
    async with _db(db).transaction() as session:
        try:
            await session.execute(insert(users).values(**record))
        except IntegrityError as exc:
            raise translate_integrity_error(exc, entity="auth", entity_id=name) from exc
        await append_event(
            session,
            entity="auth",
            entity_id=str(record["user_id"]),
            op="user_change",
            payload={
                "user_id": str(record["user_id"]),
                "action": "create_user",
                "username": name,
                "role": role,
                "status": status,
            },
            actor=actor,
            ts=stamp,
        )
    log.info("user created", op="create_user", user_id=str(record["user_id"]), role=role)
    return user_from_row(record)


async def update_user(
    user_id: Any,
    *,
    role: str | None = None,
    status: UserStatus | None = None,
    actor: str,
    actor_id: Any = None,
    db: Database | None = None,
) -> User:
    """改角色/状态（S9：不可动自身，不可动最后一个 active admin）。"""
    if role is not None and role not in ROLE_PERMISSIONS:
        raise ValidationError(
            f"unknown role {role!r}; expected one of {sorted(ROLE_PERMISSIONS)}", entity="auth"
        )
    if status is not None and status not in ("active", "disabled"):
        raise ValidationError(f"unknown status {status!r}", entity="auth")
    async with _db(db).transaction() as session:
        row = await fetch_user(session, user_id)
        if row is None:
            raise NotFoundError(
                f"user {user_id} not found", entity="auth", entity_id=str(user_id)
            )
        new_role = role or row["role"]
        new_status = status or row["status"]
        if new_role == row["role"] and new_status == row["status"]:
            return user_from_row(row)
        demoting = row["role"] == "admin" and new_role != "admin"
        disabling = row["status"] == "active" and new_status == "disabled"
        if actor_id is not None and str(actor_id) == str(user_id) and (demoting or disabling):
            raise ConflictError(
                "不可 disable/demote 自身（S9：请由其他 admin 操作）",
                entity="auth",
                entity_id=str(user_id),
            )
        if row["role"] == "admin" and row["status"] == "active" and (demoting or disabling):
            if await count_active_admins(session) <= 1:
                raise ConflictError(
                    "不可操作最后一个 active admin（S9：请先指定继任者）",
                    entity="auth",
                    entity_id=str(user_id),
                )
        stamp = now()
        await session.execute(
            update(users)
            .where(users.c.user_id == user_id)
            .values(role=new_role, status=new_status, updated_at=stamp)
        )
        await append_event(
            session,
            entity="auth",
            entity_id=str(user_id),
            op="user_change",
            payload={
                "user_id": str(user_id),
                "action": "update_user",
                "role": new_role,
                "status": new_status,
                "before": {"role": row["role"], "status": row["status"]},
            },
            actor=actor,
            ts=stamp,
        )
    log.info(
        "user updated", op="update_user", user_id=str(user_id), role=new_role, status=new_status
    )
    return user_from_row({**row, "role": new_role, "status": new_status, "updated_at": stamp})


async def delete_user(
    user_id: Any, *, actor: str, actor_id: Any = None, db: Database | None = None
) -> None:
    """删除用户（级联密钥/授权/会话）；S9 同 :func:`update_user`。

    ``grants.granted_by`` 是**无级联动作**的外键（§4 DDL），被删用户若曾授出授权，
    直接删行会触发 FK 违规（500）。故先把其授出记录的 ``granted_by`` 置空——**授权本身
    保留**（被授权人不受影响），「谁授的」由本函数的 ``auth`` 事件保留可追溯。
    """
    async with _db(db).transaction() as session:
        row = await fetch_user(session, user_id)
        if row is None:
            raise NotFoundError(
                f"user {user_id} not found", entity="auth", entity_id=str(user_id)
            )
        if actor_id is not None and str(actor_id) == str(user_id):
            raise ConflictError(
                "不可 delete 自身（S9：请由其他 admin 操作）",
                entity="auth",
                entity_id=str(user_id),
            )
        if row["role"] == "admin" and row["status"] == "active":
            if await count_active_admins(session) <= 1:
                raise ConflictError(
                    "不可删除最后一个 active admin（S9：请先指定继任者）",
                    entity="auth",
                    entity_id=str(user_id),
                )
        nulled = await session.execute(
            update(grants).where(grants.c.granted_by == user_id).values(granted_by=None)
        )
        await session.execute(delete(users).where(users.c.user_id == user_id))
        await append_event(
            session,
            entity="auth",
            entity_id=str(user_id),
            op="user_change",
            payload={
                "user_id": str(user_id),
                "action": "delete_user",
                "role": row["role"],
                "nulled_granted_by": nulled.rowcount or 0,
            },
            actor=actor,
            ts=now(),
        )
    log.info("user deleted", op="delete_user", user_id=str(user_id))


# --------------------------------------------------------------------- SSH 公钥


async def list_ssh_keys(
    user_id: Any, *, include_revoked: bool = False, db: Database | None = None
) -> list[SshKey]:
    statement = select(*KEY_COLUMNS).where(ssh_keys.c.user_id == user_id)
    if not include_revoked:
        statement = statement.where(ssh_keys.c.revoked_at.is_(None))
    statement = statement.order_by(ssh_keys.c.added_at, ssh_keys.c.key_id)
    async with _db(db).session() as session:
        rows = (await session.execute(statement)).all()
    return [ssh_key_from_row(row) for row in rows]


async def find_active_key(key_id: str, *, db: Database | None = None) -> SshKey | None:
    """按 ``key_id`` 查可用公钥（省略 ``SHA256:`` 前缀亦可；无匹配 → ``None``）。"""
    async with _db(db).session() as session:
        row = await fetch_active_key(session, normalize_key_id(key_id))
    return ssh_key_from_row(row) if row is not None else None


async def add_ssh_key(
    user_id: Any, public_key_line: str, *, actor: str, db: Database | None = None
) -> SshKey:
    """登记公钥（格式/类型/强度不合规 → 422；同一公钥已属他人 → 409）。"""
    line = " ".join(public_key_line.split())
    try:
        info = validate_public_key(line)
    except SignatureFormatError as exc:
        raise ValidationError(
            f"公钥不合规：{exc.message}", entity="auth", entity_id=str(user_id)
        ) from exc
    key_id = info.fingerprint
    if info.bits is not None:
        log.info(
            "RSA 公钥已登记", op="add_key", key_id=key_id, rsa_bits=info.bits
        )
    stamp = now()
    async with _db(db).transaction() as session:
        if await fetch_user(session, user_id) is None:
            raise NotFoundError(
                f"user {user_id} not found", entity="auth", entity_id=str(user_id)
            )
        existing = (
            await session.execute(select(*KEY_COLUMNS).where(ssh_keys.c.key_id == key_id))
        ).first()
        existing_row = row_to_dict(existing) if existing is not None else None
        if existing_row is not None:
            if str(existing_row["user_id"]) != str(user_id):
                raise ConflictError(
                    f"公钥 {key_id} 已登记给其他用户（身份归属必须唯一）",
                    entity="auth",
                    entity_id=key_id,
                )
            if existing_row["revoked_at"] is None:
                raise ConflictError(
                    f"公钥 {key_id} 已登记且处于有效状态", entity="auth", entity_id=key_id
                )
            await session.execute(
                update(ssh_keys)
                .where(ssh_keys.c.key_id == key_id)
                .values(revoked_at=None, public_key=line, key_type=info.ssh_key_type, added_at=stamp)
            )
            await append_event(
                session,
                entity="auth",
                entity_id=str(user_id),
                op="key_change",
                payload={
                    "user_id": str(user_id),
                    "action": "re_add_key",
                    "key_fingerprint": key_id,
                    "reason": "previously_revoked",
                },
                actor=actor,
                ts=stamp,
            )
            record = {
                **existing_row,
                "revoked_at": None,
                "public_key": line,
                "key_type": info.ssh_key_type,
                "added_at": stamp,
            }
        else:
            record = {
                "key_id": key_id,
                "user_id": user_id,
                "public_key": line,
                "key_type": info.ssh_key_type,
                "added_at": stamp,
                "revoked_at": None,
            }
            try:
                await session.execute(insert(ssh_keys).values(**record))
            except IntegrityError as exc:
                raise translate_integrity_error(exc, entity="auth", entity_id=key_id) from exc
            await append_event(
                session,
                entity="auth",
                entity_id=str(user_id),
                op="key_change",
                payload={
                    "user_id": str(user_id),
                    "action": "add_key",
                    "key_fingerprint": key_id,
                },
                actor=actor,
                ts=stamp,
            )
    log.info("ssh key registered", op="add_key", key_id=key_id, user_id=str(user_id))
    return ssh_key_from_row(record)


async def revoke_ssh_key(
    user_id: Any, key_id: str, *, actor: str, db: Database | None = None
) -> SshKey:
    """吊销单个公钥（不影响同用户其他密钥；已吊销则幂等返回）。"""
    normalized = normalize_key_id(key_id)
    async with _db(db).transaction() as session:
        row = (
            await session.execute(
                select(*KEY_COLUMNS).where(
                    ssh_keys.c.user_id == user_id, ssh_keys.c.key_id == normalized
                )
            )
        ).first()
        if row is None:
            raise NotFoundError(
                f"ssh key {normalized} of user {user_id} not found",
                entity="auth",
                entity_id=normalized,
            )
        record = row_to_dict(row)
        if record["revoked_at"] is not None:
            return ssh_key_from_row(record)
        stamp = now()
        await session.execute(
            update(ssh_keys).where(ssh_keys.c.key_id == normalized).values(revoked_at=stamp)
        )
        await append_event(
            session,
            entity="auth",
            entity_id=str(user_id),
            op="key_change",
            payload={
                "user_id": str(user_id),
                "action": "revoke_key",
                "key_fingerprint": normalized,
            },
            actor=actor,
            ts=stamp,
        )
    log.info("ssh key revoked", op="revoke_key", key_id=normalized, user_id=str(user_id))
    return ssh_key_from_row({**record, "revoked_at": stamp})


# ----------------------------------------------------------------------- 授权


async def list_grants(*, user_id: Any = None, db: Database | None = None) -> list[Grant]:
    statement = select(*GRANT_COLUMNS)
    if user_id is not None:
        statement = statement.where(grants.c.user_id == user_id)
    statement = statement.order_by(grants.c.granted_at, grants.c.grant_id)
    async with _db(db).session() as session:
        rows = (await session.execute(statement)).all()
    return [grant_from_row(row) for row in rows]


async def load_grants(user_id: Any, *, db: Database | None = None) -> list[Grant]:
    """某用户的 grant 集合（供 :func:`authorize_user` 判定）。"""
    async with _db(db).session() as session:
        rows = await fetch_grants(session, user_id)
    return [grant_from_row(row) for row in rows]


async def create_grant(
    user_id: Any,
    scope: GrantScope,
    value: str,
    permission: str,
    *,
    actor: str,
    granted_by: Any = None,
    db: Database | None = None,
) -> Grant:
    """授予文档集级授权（**S5 授予侧校验**：越权 grant 在此即 422）。"""
    stamp = now()
    async with _db(db).transaction() as session:
        row = await fetch_user(session, user_id)
        if row is None:
            raise NotFoundError(
                f"user {user_id} not found", entity="auth", entity_id=str(user_id)
            )
        validate_grant(row["role"], scope, value, permission)
        record = {
            "grant_id": new_uuid7(),
            "user_id": user_id,
            "scope": scope,
            "value": value,
            "permission": permission,
            "granted_by": granted_by if granted_by is not None else _as_actor(actor),
            "granted_at": stamp,
        }
        try:
            await session.execute(insert(grants).values(**record))
        except IntegrityError as exc:
            raise translate_integrity_error(exc, entity="auth", entity_id=str(user_id)) from exc
        await append_event(
            session,
            entity="auth",
            entity_id=str(user_id),
            op="grant_change",
            payload={
                "user_id": str(user_id),
                "action": "add_grant",
                "scope": scope,
                "value": value,
                "permission": permission,
            },
            actor=actor,
            ts=stamp,
        )
    log.info(
        "grant added",
        op="add_grant",
        user_id=str(user_id),
        scope=scope,
        value=value,
        permission=permission,
    )
    return grant_from_row(record)


def _as_actor(actor: str) -> Any:
    """``actor`` 审计串 → ``granted_by`` 外键（非 UUID 的审计串如 ``system`` → ``None``）。"""
    try:
        return as_uuid(actor)
    except (ValueError, AttributeError, TypeError):
        return None


async def delete_grant(grant_id: Any, *, actor: str, db: Database | None = None) -> Grant:
    """撤销一条授权。"""
    async with _db(db).transaction() as session:
        row = (
            await session.execute(select(*GRANT_COLUMNS).where(grants.c.grant_id == grant_id))
        ).first()
        if row is None:
            raise NotFoundError(
                f"grant {grant_id} not found", entity="auth", entity_id=str(grant_id)
            )
        record = row_to_dict(row)
        await session.execute(delete(grants).where(grants.c.grant_id == grant_id))
        await append_event(
            session,
            entity="auth",
            entity_id=str(record["user_id"]),
            op="grant_change",
            payload={
                "user_id": str(record["user_id"]),
                "action": "remove_grant",
                "scope": record["scope"],
                "value": record["value"],
                "permission": record["permission"],
            },
            actor=actor,
            ts=now(),
        )
    log.info("grant removed", op="remove_grant", grant_id=str(grant_id))
    return grant_from_row(record)


async def authorize_user(
    user: User,
    perm: str,
    target: Any = None,
    *,
    db: Database | None = None,
    doc_type: str | None = None,
) -> None:
    """读取 grant → 判定（:func:`agenticdocer.auth.rbac.authorize`）→ 违规落审计事件。

    M06/M07 的推荐入口：判定逻辑在 ``rbac``（纯函数、可单测），此处负责 I/O 与审计。

    **审计归因**（SecAudit AUD-4）：此处身份**已通过验签/会话**，与 S10 针对的「未验证身份」
    不同。为既不违反 S10 字面（失败事件 ``actor='anonymous'``）又不丢失确定性归因，事件仍记
    ``actor='anonymous'``，但把已验证身份写进 ``payload.verified_user_id``——与 ``claimed_*``
    （自述值）在字段名上明确区分。
    """
    grants = await load_grants(user.user_id, db=db)
    try:
        authorize(user, perm, target, grants=grants, doc_type=doc_type)
    except ForbiddenError:
        await log_auth_failure(
            "forbidden",
            status_code=403,
            verified_user_id=str(user.user_id),
            db=db,
        )
        raise


# ------------------------------------------------------------------- 审计事件


async def log_auth_event(
    op: str, actor: str, payload: dict[str, Any], *, db: Database | None = None
) -> Event:
    """写一条 ``entity='auth'`` 审计事件（S1：DDL CHECK 与 Event Literal 均含 ``auth``）。"""
    async with _db(db).transaction() as session:
        return await append_event(
            session, entity="auth", entity_id=actor, op=op, payload=payload, actor=actor
        )


async def log_auth_failure(
    reason: str,
    *,
    ip: str | None = None,
    endpoint: str | None = None,
    method: str | None = None,
    status_code: int = 401,
    claimed_key_id: str | None = None,
    claimed_user_id: str | None = None,
    verified_user_id: str | None = None,
    db: Database | None = None,
) -> None:
    """鉴权失败审计（REQ-M10-F05d/e；**S10**）。

    载荷只含**失败原因**、``claimed_*``（请求自述身份，未经核验）与 ``verified_user_id``
    （**已验签/会话核验的身份**，仅授权拒绝即 403 场景才有），不含密钥材料、不写身份列；
    ``actor`` 恒为 ``anonymous``（S10 字面）。按 ``(ip, reason, verified_user_id, 5min)``
    聚合：窗口内首条落事件、后续只计数，换窗时补一条 ``occurrences`` 汇总事件（避免审计淹没，S7）。
    聚合键含已验证身份，故**每个被拒主体的首条事件都带确定性归因**（SecAudit AUD-4）。
    """
    bucket_start = int(time.time() // _FAILURE_BUCKET_SECONDS)
    key = (ip or "unknown", reason, verified_user_id or "")
    pending: _FailureBucket | None = None
    with _failure_lock:
        current = _failure_buckets.get(key)
        if current is not None and current.bucket == bucket_start:
            current.count += 1
            return
        if current is not None and current.count > 1:
            pending = current
        entry = _FailureBucket(bucket_start, endpoint, method, status_code)
        entry.count = 1
        _failure_buckets[key] = entry
    if pending is not None:
        await _write_failure_event(
            reason,
            ip=ip,
            bucket=pending,
            aggregated=True,
            verified_user_id=verified_user_id,
            db=db,
        )
    await _write_failure_event(
        reason,
        ip=ip,
        bucket=_FailureBucket(bucket_start, endpoint, method, status_code),
        aggregated=False,
        claimed_key_id=claimed_key_id,
        claimed_user_id=claimed_user_id,
        verified_user_id=verified_user_id,
        db=db,
    )


async def _write_failure_event(
    reason: str,
    *,
    ip: str | None,
    bucket: _FailureBucket,
    aggregated: bool,
    claimed_key_id: str | None = None,
    claimed_user_id: str | None = None,
    db: Database | None = None,
) -> None:
    payload: dict[str, Any] = {
        "reason": reason,
        "ip": ip,
        "endpoint": bucket.endpoint,
        "method": bucket.method,
        "status": bucket.status_code,
        "occurrences": bucket.count,
        "bucket_start": datetime.fromtimestamp(
            bucket.bucket * _FAILURE_BUCKET_SECONDS, tz=timezone.utc
        ).isoformat(),
    }
    if aggregated:
        payload["aggregated"] = True
    if claimed_key_id is not None:
        payload["claimed_key_id"] = claimed_key_id
    if claimed_user_id is not None:
        payload["claimed_user_id"] = claimed_user_id
    try:
        await log_auth_event("fail", "anonymous", payload, db=db)
    except Exception:  # noqa: BLE001 - 审计失败不得掩盖 401/403 本身
        log.error("鉴权失败审计事件写入失败", op="log_auth_failure", reason=reason, ip=ip)


async def flush_auth_failure_aggregates(*, db: Database | None = None) -> int:
    """把已过窗的失败计数写成汇总事件（由 :func:`sessions.purge_expired` 同任务调用）。"""
    current_bucket = int(time.time() // _FAILURE_BUCKET_SECONDS)
    with _failure_lock:
        stale = [
            (key, entry)
            for key, entry in _failure_buckets.items()
            if entry.bucket < current_bucket
        ]
        for key, _ in stale:
            _failure_buckets.pop(key, None)
    written = 0
    for (ip, reason), entry in stale:
        if entry.count <= 1:
            continue
        await _write_failure_event(reason, ip=ip, bucket=entry, aggregated=True, db=db)
        written += 1
    return written


def reset_failure_aggregates() -> None:
    """清空失败聚合窗口（测试/进程重启用，与 ``sessions.reset_rate_limits`` 对称）。"""
    with _failure_lock:
        _failure_buckets.clear()
