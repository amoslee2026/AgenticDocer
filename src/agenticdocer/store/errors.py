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
