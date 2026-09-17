"""管理员自举（REQ-M10-F05；ADR-007 §4；**S9 语义统一**）。

**触发条件（统一语义）**：**不存在 ``status='active'`` 的 admin** 时执行——可重复救援；
已存在 active admin 时**幂等跳过**，且**不因键文件变更改写 DB**（以 DB 为准）。

救援路径（无 active admin 时）：

1. 读 ``ADMIN_SSH_PUBKEY_FILE``（默认 ``data/admin_keys/admin.pub``）→ 指纹 ``key_id``；
2. 该指纹已登记 → 取其属主：**激活 + 升为 admin + 密钥解吊销**；
3. 未登记 → ``ADMIN_USERNAME``（默认 ``admin``）用户存在则复用（同样激活+升权），否则新建；
4. 落 ``auth`` 审计事件（``user_change`` + ``key_change``，``actor='system'``）。

**fail-closed**：无 active admin 且自举失败（文件缺失/不可读/公钥不合规）→
:class:`~agenticspec.auth.errors.BootstrapError`，错误信息指向自举步骤；系统在无
active admin 期间对**所有**端点 401（M06/M07 侧由 :func:`agenticspec.auth.middleware.require_auth`
的 ``missing_credentials`` 分支给出同样的提示，S9/C 项）。
"""

from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy import insert, select, update

from agenticspec.model import User, new_uuid7
from agenticspec.observability import get_logger
from agenticspec.store import Database, append_event, get_database, now

from .errors import BOOTSTRAP_HINT, BootstrapError, SignatureFormatError
from .sshsig import validate_public_key
from .users import (
    DEFAULT_ADMIN_USERNAME,
    fetch_user,
    fetch_user_by_username,
    user_from_row,
)

__all__ = [
    "admin_pubkey_file",
    "admin_username",
    "bootstrap_admin",
    "has_active_admin",
]

log = get_logger("m10.bootstrap")

DEFAULT_ADMIN_PUBKEY_FILE: Path = (
    Path(__file__).resolve().parents[3] / "data" / "admin_keys" / "admin.pub"
)
"""``ADMIN_SSH_PUBKEY_FILE`` 缺省位置（§5 部署；``data/admin_keys/`` 已 gitignore）。"""


def admin_pubkey_file() -> Path:
    """自举公钥文件路径（``ADMIN_SSH_PUBKEY_FILE``）。"""
    configured = os.environ.get("ADMIN_SSH_PUBKEY_FILE")
    return Path(configured).expanduser() if configured else DEFAULT_ADMIN_PUBKEY_FILE


def admin_username() -> str:
    """自举管理员用户名（``ADMIN_USERNAME``，默认 ``admin``）。"""
    return os.environ.get("ADMIN_USERNAME") or DEFAULT_ADMIN_USERNAME


async def has_active_admin(*, db: Database | None = None) -> bool:
    """是否存在 active admin（：S9 触发条件）。"""
    from agenticspec.store.schema import users as users_table

    database = db if db is not None else get_database()
    statement = (
        select(users_table.c.user_id)
        .where(users_table.c.role == "admin", users_table.c.status == "active")
        .limit(1)
    )
    async with database.session() as session:
        return (await session.execute(statement)).first() is not None


def _read_public_key(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise BootstrapError(
            f"自举公钥文件不可读：{path}（{exc.strerror or exc}）。{BOOTSTRAP_HINT}"
        ) from exc
    line = " ".join(text.split())
    if not line:
        raise BootstrapError(f"自举公钥文件为空：{path}。{BOOTSTRAP_HINT}")
    return line


async def bootstrap_admin(
    public_key_path: Path | str | None = None, *, db: Database | None = None
) -> User:
    """按 S9 语义自举 admin：**不存在 active admin 时**创建/救援，否则幂等返回现有 admin。"""
    from agenticspec.store.schema import ssh_keys, users as users_table

    database = db if db is not None else get_database()
    async with database.transaction() as session:
        existing = (
            await session.execute(
                select(users_table.c.user_id)
                .where(users_table.c.role == "admin", users_table.c.status == "active")
                .limit(1)
            )
        ).first()
        if existing is not None:
            row = await fetch_user(session, existing[0])
            log.info(
                "bootstrap skipped（已存在 active admin）",
                op="bootstrap",
                user_id=str(existing[0]),
            )
            return user_from_row(row)

        path = Path(public_key_path).expanduser() if public_key_path else admin_pubkey_file()
        line = _read_public_key(path)
        try:
            info = validate_public_key(line)
        except SignatureFormatError as exc:
            raise BootstrapError(
                f"自举公钥不合规（{path}）：{exc.message}。{BOOTSTRAP_HINT}"
            ) from exc
        key_id = info.fingerprint
        stamp = now()
        key_row = (
            await session.execute(select(ssh_keys.c.user_id).where(ssh_keys.c.key_id == key_id))
        ).first()
        user_row = await fetch_user(session, key_row[0]) if key_row is not None else None
        if user_row is None:
            user_row = await fetch_user_by_username(session, admin_username())
        if user_row is None:
            record = {
                "user_id": new_uuid7(),
                "username": admin_username(),
                "role": "admin",
                "status": "active",
                "created_at": stamp,
                "updated_at": stamp,
            }
            await session.execute(insert(users_table).values(**record))
            user_row = record
            action = "bootstrap_create"
        else:
            await session.execute(
                update(users_table)
                .where(users_table.c.user_id == user_row["user_id"])
                .values(role="admin", status="active", updated_at=stamp)
            )
            user_row = {**user_row, "role": "admin", "status": "active", "updated_at": stamp}
            action = "bootstrap_rescue"
        if key_row is None:
            await session.execute(
                insert(ssh_keys).values(
                    key_id=key_id,
                    user_id=user_row["user_id"],
                    public_key=line,
                    key_type=info.ssh_key_type,
                    added_at=stamp,
                    revoked_at=None,
                )
            )
        else:
            await session.execute(
                update(ssh_keys)
                .where(ssh_keys.c.key_id == key_id)
                .values(revoked_at=None, public_key=line, key_type=info.ssh_key_type)
            )
        await append_event(
            session,
            entity="auth",
            entity_id=str(user_row["user_id"]),
            op="user_change",
            payload={
                "user_id": str(user_row["user_id"]),
                "action": action,
                "role": "admin",
                "status": "active",
                "reason": "bootstrap（无 active admin，S9 救援语义）",
                "key_fingerprint": key_id,
            },
            actor="system",
            ts=stamp,
        )
        await append_event(
            session,
            entity="auth",
            entity_id=str(user_row["user_id"]),
            op="key_change",
            payload={
                "user_id": str(user_row["user_id"]),
                "action": "add_key",
                "key_fingerprint": key_id,
                "reason": "bootstrap",
            },
            actor="system",
            ts=stamp,
        )
    log.info(
        "admin bootstrapped",
        op="bootstrap",
        user_id=str(user_row["user_id"]),
        key_id=key_id,
        action=action,
    )
    return user_from_row(user_row)
