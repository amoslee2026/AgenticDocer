"""M10 鉴权异常（§6 错误映射：401 未认证 / 403 授权拒绝；S10 审计字段）。

异常同时承载**可审计的失败原因**（``reason``）与请求自述身份（``claimed_key_id``）——
审计事件据此写 ``claimed_*`` 前缀字段（S10：失败事件不得把自述值写进
``user_id``/``key_fingerprint`` 列，防污染审计）。

| 异常 | 状态码 | 场景 |
|---|---|---|
| :class:`AuthenticationError` | 401 | 缺凭据 / 时间窗越界 / 验签失败 / nonce 重放 / 会话过期 |
| :class:`SignatureFormatError` | 401 | SSHSIG 帧、namespace、曲线不受支持（格式层拒绝） |
| :class:`SignatureVerificationError` | 401 | 帧可解析但密码学校验失败（含公钥不匹配） |
| :class:`RateLimitError` | 429 | ``/auth/challenge``、``/auth/login`` 按 IP 限流（S7） |
| :class:`BootstrapError` | 500 | 自举失败（无公钥文件 / 键文件不可读） |

403 复用 M02 的 :class:`~agenticspec.store.ForbiddenError`（语义与状态码一致，
不引入第二套映射）。
"""

from __future__ import annotations

from typing import Any, Final

from agenticspec.observability import DTO_AUTH_REJECTED
from agenticspec.store import StoreError

__all__ = [
    "BOOTSTRAP_HINT",
    "AUTH_REJECTED_CODE",
    "AuthError",
    "AuthenticationError",
    "BootstrapError",
    "RateLimitError",
    "SignatureFormatError",
    "SignatureVerificationError",
]

AUTH_REJECTED_CODE: Final = str(DTO_AUTH_REJECTED)
"""审计/日志统一错误码（M12 metrics 契约：鉴权失败用 ``error_code=DTO_AUTH_REJECTED``）。"""

BOOTSTRAP_HINT: Final = (
    "库内不存在 active admin，系统 fail-closed（S9/REQ-M10-F05c）："
    "请先执行 `uv run agenticspec auth bootstrap`（使用 ADMIN_SSH_PUBKEY_FILE 指向的公钥）完成自举"
)


class AuthError(StoreError):
    """M10 鉴权/授权失败基类。

    ``reason`` 是**稳定、可聚合**的失败原因（写入审计事件 ``payload.reason``）；
    ``claimed_key_id`` 是请求自述的密钥指纹（仅用于 ``claimed_*`` 审计字段与日志，
    绝不作为身份依据）。
    """

    status_code: int = 401
    code: str | None = AUTH_REJECTED_CODE

    def __init__(
        self,
        message: str,
        *,
        reason: str,
        claimed_key_id: str | None = None,
        entity: str | None = "auth",
        entity_id: Any = None,
    ) -> None:
        super().__init__(message, entity=entity, entity_id=entity_id)
        self.reason = reason
        self.claimed_key_id = claimed_key_id


class AuthenticationError(AuthError):
    """凭据缺失或不可信（→ 401）。"""

    status_code = 401


class SignatureFormatError(AuthError):
    """SSHSIG 结构/策略层拒绝（解码失败、版本、namespace、曲线、哈希算法）。

    与 :class:`SignatureVerificationError` 的区别仅在「拒绝发生在解析阶段还是密码学阶段」；
    两者对外都是 401，分开是为了审计与排障可分辨（RFC-ish 帧错误 vs 真签名错）。
    """

    status_code = 401


class SignatureVerificationError(AuthError):
    """签名校验失败（含签名所用公钥与登记公钥不一致）。"""

    status_code = 401


class RateLimitError(AuthError):
    """按 IP 限流触发（S7：``AUTH_RATE_LIMIT_PER_MIN``）。"""

    status_code = 429


class BootstrapError(StoreError):
    """自举失败（部署/环境问题，非客户端错误 → 500）。"""

    status_code = 500
