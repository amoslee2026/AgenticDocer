"""M02 存储层异常类型（§6 横切：ConflictError→409、ValidationError→422、NotFound→404、Forbidden→403）。"""

from __future__ import annotations

from typing import Any

__all__ = [
    "StoreError",
    "ConflictError",
    "NotFoundError",
    "ValidationError",
    "ForbiddenError",
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


def translate_integrity_error(exc: BaseException, *, entity: str, entity_id: Any = None) -> StoreError:
    """DB 完整性错误 → 存储层异常（唯一键→409、外键/非空/CHECK→422）。

    不 import SQLAlchemy：按 duck typing 读 asyncpg 的 `constraint_name`/`sqlstate`
    （`IntegrityError.orig`），保持本模块零依赖。
    """
    orig = getattr(exc, "orig", exc)
    constraint = getattr(orig, "constraint_name", None) or ""
    sqlstate = getattr(orig, "sqlstate", None) or getattr(orig, "pgcode", None) or ""
    detail = f"{entity} write violated database constraint {constraint!r}" if constraint else (
        f"{entity} write violated database constraint: {orig}"
    )
    if sqlstate == "23505" or "unique" in orig.__class__.__name__.lower():
        if "anchor" in constraint:
            return ConflictError(
                f"{detail}（(doc_id, anchor) 唯一：同文档锚冲突）",
                code="DTO_ANCHOR_CONFLICT",
                entity=entity,
                entity_id=entity_id,
            )
        return ConflictError(detail, entity=entity, entity_id=entity_id)
    if sqlstate in {"23503", "23502", "23514"} or orig.__class__.__name__ in {
        "ForeignKeyViolationError",
        "NotNullViolationError",
        "CheckViolationError",
    }:
        return ValidationError(detail, entity=entity, entity_id=entity_id)
    return ValidationError(detail, entity=entity, entity_id=entity_id)
