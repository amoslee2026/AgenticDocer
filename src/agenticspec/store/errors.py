"""M02 存储层异常类型（§6 横切：ConflictError→409、ValidationError→422、NotFound→404、Forbidden→403）。"""

from __future__ import annotations

import re
from typing import Any

__all__ = [
    "StoreError",
    "ConflictError",
    "NotFoundError",
    "ValidationError",
    "ForbiddenError",
    "translate_integrity_error",
]


class StoreError(Exception):
    """存储层异常基类。

    ``status_code`` 供 M06/M07 HTTP 适配层直接映射；``code`` 为 M12 错误码
    （``DTO_*``，见 §3 M12「错误码扩展」），无对应码时为 ``None``。
    """

    status_code: int = 500
    code: str | None = None

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        entity: str | None = None,
        entity_id: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        if code is not None:
            self.code = code
        self.entity = entity
        self.entity_id = entity_id


class ConflictError(StoreError):
    """乐观锁版本不匹配 / 唯一约束冲突（→ 409，可重试）。"""

    status_code = 409


class NotFoundError(StoreError):
    """实体不存在，或已被软删且调用方未要求包含已删行（→ 404）。"""

    status_code = 404


class ValidationError(StoreError):
    """写入载荷或引用完整性校验失败（→ 422）。"""

    status_code = 422


class ForbiddenError(StoreError):
    """授权拒绝（→ 403）。用户级 RBAC 判定在 M10，此处仅供存储层拒绝越权写入。"""

    status_code = 403


_CONSTRAINT_RE = re.compile(r'constraint "([^"]+)"')
_UNIQUE_SQLSTATE = "23505"
_VALIDATION_SQLSTATES = frozenset({"23503", "23502", "23514"})


def _constraint_name(orig: BaseException) -> str:
    """尽力取出违反的约束名。

    SQLAlchemy 的 asyncpg 适配层把原始异常包一层（`orig` 是适配错误，`__cause__`
    才是 asyncpg 异常），且**分区表**上的唯一约束在报错里是分区级名字
    （如 `nodes_p48_doc_id_anchor_key`），故先走属性链、再回退到报文解析。
    """
    candidates: list[Any] = [orig, getattr(orig, "__cause__", None), getattr(orig, "__context__", None)]
    for candidate in candidates:
        name = getattr(candidate, "constraint_name", None)
        if name:
            return str(name)
    match = _CONSTRAINT_RE.search(str(orig))
    return match.group(1) if match else ""


def translate_integrity_error(exc: BaseException, *, entity: str, entity_id: Any = None) -> StoreError:
    """DB 完整性错误 → 存储层异常（唯一键→409、外键/非空/CHECK→422）。

    不 import SQLAlchemy：按 duck typing 读 `IntegrityError.orig` 的
    `sqlstate`/`constraint_name`，保持本模块零依赖。
    """
    orig = getattr(exc, "orig", exc)
    constraint = _constraint_name(orig)
    sqlstate = getattr(orig, "sqlstate", None) or getattr(orig, "pgcode", None) or ""
    detail = (
        f"{entity} write violated database constraint {constraint!r}"
        if constraint
        else f"{entity} write violated database constraint: {orig}"
    )
    if sqlstate == _UNIQUE_SQLSTATE or "unique" in type(orig).__name__.lower():
        if "anchor" in constraint:
            return ConflictError(
                f"{detail}（(doc_id, anchor) 唯一：同文档锚冲突）",
                code="DTO_ANCHOR_CONFLICT",
                entity=entity,
                entity_id=entity_id,
            )
        return ConflictError(detail, entity=entity, entity_id=entity_id)
    return ValidationError(detail, entity=entity, entity_id=entity_id)
