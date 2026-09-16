"""M10 FastAPI 鉴权面（REQ-M10-F01；S2/S3/S4/S6/S7/S10/S14）。

* :func:`verify_signature`——**agent 路径**（每请求签名）：按 S3/S7 顺序
  ``时间窗 → 公钥查表（active） → 验签 → 验签通过后才 INSERT nonce``；
* :func:`resolve_request_identity` / :func:`require_auth`——**请求级依赖项**：
  有 Cookie 走会话（WebUI），否则走签名（agent）；两者都无 → 401（fail-closed）；
* :data:`EXEMPT_PATHS` / :func:`is_exempt`——**S4 唯一豁免白名单**（清单外无凭据必 401；
  ``/docs``、``/openapi.json``、``/redoc`` **不豁免**，由 M06/M07 在非开发模式禁用）；
* :func:`cookie_secure` / :func:`session_cookie_kwargs`——**S6**：非 loopback 部署
  （TLS 反向代理终止）Cookie 强制 ``Secure``；``AUTH_COOKIE_SECURE`` 可显式覆盖；
* 失败一律落 ``auth`` 审计事件（S1/S10，:func:`agenticdocer.auth.users.log_auth_failure`）
  并记 M12 日志 ``error_code=DTO_AUTH_REJECTED``。

**身份来源（S14）**：一律取自验签结果/会话行，**不读 ``X-Actor``**；``source`` 由凭据类型
判定（Cookie → ``webui``，签名 → ``agent``）。
"""

from __future__ import annotations

import os
import string
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Final

from fastapi import Depends, HTTPException, Request, Response

from agenticdocer.model import Model, User, WriteContext
from agenticdocer.observability import DTO_AUTH_REJECTED, get_logger
from agenticdocer.store import Database, ForbiddenError, get_database

from .errors import AuthError, AuthenticationError, BOOTSTRAP_HINT
from .sessions import (
    SESSION_COOKIE_NAME,
    resolve_session,
    session_ttl_seconds,
    session_token_hash,
    signature_max_skew_seconds,
from fastapi import Depends, HTTPException, Request, Response

from agenticdocer.model import Model, User, WriteContext, WriteSource
from agenticdocer.observability import DTO_AUTH_REJECTED, get_logger
from agenticdocer.store import Database, ForbiddenError, get_database

from .errors import BOOTSTRAP_HINT, AuthError, AuthenticationError
from .sessions import (
    SESSION_COOKIE_NAME,
    consume_nonce,
    future_skew_seconds,
    resolve_session,
    session_token_hash,
    session_ttl_seconds,
    signature_max_skew_seconds,
)
from .signing import normalize_key_id, request_payload
from .sshsig import verify_sshsig
from .users import (
    authorize_user,
    fetch_active_key,
    fetch_user,
    log_auth_failure,
    user_from_row,
)
    future_skew_seconds,
    consume_nonce,
)
from .signing import normalize_key_id, request_payload
from .sshsig import verify_sshsig
from .users import (
    authorize_user,
    fetch_active_key,
    fetch_user,
    log_auth_failure,
    user_from_row,
)

__all__ = [
    "EXEMPT_PATHS",
    "EXEMPT_PREFIXES",
    "MIN_NONCE_CHARS",
    "NONCE_HEADER",
    "SESSION_COOKIE_NAME",
    "SIGNATURE_HEADER",
    "TIMESTAMP_HEADER",
    "SshSigHeaders",
    "clear_session_cookie",
    "client_ip",
    "cookie_secure",
    "current_context",
    "is_exempt",
    "normalize_path",
    "raw_path",
    "require_auth",
    "require_permission",
    "resolve_request_identity",
    "session_cookie_kwargs",
    "set_session_cookie",
    "verify_signature",
    "write_context",
]

log = get_logger("m10.middleware")

SIGNATURE_HEADER: Final = "X-SSH-Signature"
KEY_ID_HEADER: Final = "X-SSH-Key-Id"
TIMESTAMP_HEADER: Final = "X-Timestamp"
NONCE_HEADER: Final = "X-Nonce"

MIN_NONCE_CHARS: Final = 22
"""``X-Nonce`` 下界：≥128 位随机（base64/urlsafe 编码 ≥22 字符，§3 M06）。"""

MAX_NONCE_CHARS: Final = 512
"""``X-Nonce`` 上界（防止把 nonces 表当存储用）。"""

_NONCE_ALPHABET: Final = frozenset(string.ascii_letters + string.digits + "-_+/=")

EXEMPT_PATHS: Final[tuple[str, ...]] = (
    "/",
    "/healthz",
    "/api/v1/auth/challenge",
    "/api/v1/auth/login",
    "/auth/challenge",
    "/auth/login",
)
"""**S4 唯一豁免白名单**（其余端点无凭据必 401）。"""

EXEMPT_PREFIXES: Final[tuple[str, ...]] = ("/assets/login-",)
"""登录页静态资源前缀（仅限白名单文件，不含业务数据）。"""

EXEMPT_GET_ONLY: Final[tuple[str, ...]] = ("/",)
"""仅读方法豁免的路径（``POST /`` 之类不在白名单内，须鉴权）。"""

_NO_USERS_REASON: Final = "missing_credentials"


def normalize_path(path: str) -> str:
    """路径归一（去掉尾部斜杠，保留根路径）——豁免判定与审计端点名共用。"""
    normalized = path or "/"
    if not normalized.startswith("/"):
        normalized = "/" + normalized
    while len(normalized) > 1 and normalized.endswith("/"):
        normalized = normalized[:-1]
    return normalized


def is_exempt(path: str, method: str = "GET") -> bool:
    """是否命中豁免白名单（S4）。"""
    normalized = normalize_path(path)
    if normalized in EXEMPT_GET_ONLY:
        return method.upper() in ("GET", "HEAD")
    if normalized in EXEMPT_PATHS:
        return True
    return normalized.startswith(EXEMPT_PREFIXES)


@dataclass(frozen=True, slots=True)
class SshSigHeaders:
    """``X-SSH-*`` 头（§3 M06；**无 ``X-Actor``**，S14）。"""

    signature: str
    key_id: str
    timestamp: str
    nonce: str

    @classmethod
    def parse(cls, headers: Any) -> SshSigHeaders:
        """缺失任一必需头 → 401（``missing_credentials``）。"""
        values = {
            name: (headers.get(name) or "").strip()
            for name in (SIGNATURE_HEADER, KEY_ID_HEADER, TIMESTAMP_HEADER, NONCE_HEADER)
        }
        missing = [name for name, value in values.items() if not value]
        if missing:
            raise AuthenticationError(
                f"缺少签名头 {sorted(missing)}（§3 M06：{SIGNATURE_HEADER}/{KEY_ID_HEADER}/"
                f"{TIMESTAMP_HEADER}/{NONCE_HEADER}）",
                reason=_NO_USERS_REASON,
            )
        nonce = values[NONCE_HEADER]
        if not MIN_NONCE_CHARS <= len(nonce) <= MAX_NONCE_CHARS or not set(nonce) <= _NONCE_ALPHABET:
            raise AuthenticationError(
                f"{NONCE_HEADER} 不合法（需 ≥{MIN_NONCE_CHARS} 字符的 base64/urlsafe 随机串）",
                reason="bad_nonce",
            )
        return cls(
            signature=values[SIGNATURE_HEADER],
            key_id=values[KEY_ID_HEADER],
            timestamp=values[TIMESTAMP_HEADER],
            nonce=nonce,
        )

    @classmethod
    def present(cls, headers: Any) -> bool:
        """是否携带签名头（用于区分「Cookie 路径」与「签名路径」）。"""
        return bool((headers.get(SIGNATURE_HEADER) or "").strip())


def parse_timestamp(text: str) -> datetime:
    """解析 ``X-Timestamp``（ISO 8601；无时区按 UTC）→ 401 on 解析失败。"""
    candidate = text.strip()
    if candidate.endswith(("Z", "z")):
        candidate = candidate[:-1] + "+00:00"
    try:
        moment = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise AuthenticationError(
            f"{TIMESTAMP_HEADER} 不是合法 ISO 8601 时间：{text!r}", reason="bad_timestamp"
        ) from exc
    return moment.astimezone(timezone.utc) if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def check_timestamp(moment: datetime, *, reference: datetime | None = None) -> None:
    """时间窗校验（S3）：偏移 ∈ ``[−future_skew, +max_skew]``，否则 401。"""
    reference = reference or datetime.now(timezone.utc)
    offset = (reference - moment).total_seconds()
    if offset < -future_skew_seconds():
        raise AuthenticationError(
            f"{TIMESTAMP_HEADER} 超前 {-offset:.0f}s（未来容忍 {future_skew_seconds()}s，S3）",
            reason="timestamp_future",
        )
    if offset > signature_max_skew_seconds():
        raise AuthenticationError(
            f"{TIMESTAMP_HEADER} 过期 {offset:.0f}s（容忍 {signature_max_skew_seconds()}s，S3）",
            reason="timestamp_expired",
        )


def raw_path(request: Request) -> str:
    """请求行中的 **RAW_PATH**（含 query 原样字节；不百分号解码、不规范化，S2）。"""
    query = request.scope.get("query_string") or b""
    path = request.scope.get("path") or request.url.path
    suffix = "?" + query.decode("latin-1") if query else ""
    return f"{path}{suffix}"


def client_ip(request: Request) -> str | None:
    """客户端 IP（``AUTH_TRUSTED_PROXY=1`` 时才采信 ``X-Forwarded-For`` 首段）。"""
    if os.environ.get("AUTH_TRUSTED_PROXY", "0") not in ("0", "", "false", "False"):
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
    return request.client.host if request.client is not None else None


def auth_database(request: Request) -> Database | None:
    """应用注入的 ``Database``（``app.state.auth_db``/``app.state.db``）；无则用进程单例。"""
    state = getattr(request.app, "state", None)
    for attribute in ("auth_db", "db", "database"):
        database = getattr(state, attribute, None)
        if isinstance(database, Database):
            return database
    return None


def _db_or_default(db: Database | None) -> Database:
    return db if db is not None else get_database()


class AuthContext(Model):
    """一次已鉴权请求的身份上下文（M06/M07 据此构造 ``WriteContext``）。"""

    user: User
    source: str
    """凭据类型（S14）：``agent``（签名）/ ``webui``（会话 Cookie）。"""

    key_fingerprint: str | None = None
    """签名路径的 ``key_id``（会话路径为 ``None``）。"""

    session_hash: str | None = None
    """会话路径的 ``token_hash``（明文 token 不进入上下文）。"""

    @property
    def actor(self) -> str:
        """审计串（§6 A3：``WriteContext.actor`` 为 str）。"""
        return str(self.user.user_id)


def write_context(context: AuthContext) -> WriteContext:
    """把请求身份转成存储层 ``WriteContext``（``actor`` 取验签结果，``source`` 取凭据类型）。"""
    return WriteContext(actor=context.actor, source=context.source)  # type: ignore[arg-type]


async def verify_signature(
    method: str,
    path: str,
    body: bytes,
    headers: SshSigHeaders,
    *,
    db: Database | None = None,
    ip: str | None = None,
) -> AuthContext:
    """agent 路径验签（§3 M06 / S2 / S3 / S7）。

    顺序：① 时间窗 → ② 公钥查表（active **且属主 active**）→ ③ SSHSIG 验签 →
    ④ **验签通过后才 INSERT nonce**（未认证请求不写库）。
    """
    database = _db_or_default(db)
    moment = parse_timestamp(headers.timestamp)
    check_timestamp(moment)
    key_id = normalize_key_id(headers.key_id)
    with log.timer("auth_verify", route=normalize_path(path), method=method.upper()):
        async with database.session() as session:
            key = await fetch_active_key(session, key_id)
            if key is None:
                raise ForbiddenError(
                    f"公钥 {key_id} 未注册或其属主已禁用（S8）",
                    entity="auth",
                    entity_id=key_id,
                )
            user_row = await fetch_user(session, key["user_id"])
        if user_row is None or user_row["status"] != "active":
            raise ForbiddenError(
                f"用户 {key['user_id']} 不可用（S8）", entity="auth", entity_id=key_id
            )
        payload = request_payload(method, path, body, headers.timestamp, headers.nonce)
        verify_sshsig(key["public_key"], headers.signature, payload)
        async with database.transaction() as session:
            await consume_nonce(session, headers.nonce, key["user_id"])
    return AuthContext(
        user=user_from_row(user_row),
        source="agent",
        key_fingerprint=key["key_id"],
    )


async def _no_users() -> bool:
    from sqlalchemy import func, select

    from agenticdocer.store.schema import users as users_table

    async with get_database().session() as session:
        count = (
            await session.execute(select(func.count()).select_from(users_table))
        ).scalar_one()
    return int(count) == 0


async def resolve_request_identity(
    request: Request, *, db: Database | None = None
) -> AuthContext:
    """Cookie（WebUI）或签名头（agent）→ :class:`AuthContext`；两者皆无 → 401（fail-closed）。"""
    database = db if db is not None else auth_database(request)
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if token:
        user = await resolve_session(token, db=database)
        if user is None:
            raise AuthenticationError(
                "会话无效/已过期（S8/S15，请重新登录）", reason="invalid_session"
            )
        return AuthContext(user=user, source="webui", session_hash=session_token_hash(token))
    headers = SshSigHeaders.parse(request.headers)
    return await verify_signature(
        request.method,
        raw_path(request),
        await request.body(),
        headers,
        db=database,
        ip=client_ip(request),
    )


def http_error(exc: Exception) -> HTTPException:
    """领域异常 → ``HTTPException``（401/403/429），``detail`` 带 ``code``/``reason``。"""
    if isinstance(exc, AuthError):
        detail: dict[str, Any] = {
            "error": str(DTO_AUTH_REJECTED),
            "reason": exc.reason,
            "message": exc.message,
        }
        headers = {"WWW-Authenticate": 'SSHSIG realm="agenticdocer"'} if exc.status_code == 401 else None
        return HTTPException(status_code=exc.status_code, detail=detail, headers=headers)
    return HTTPException(
        status_code=getattr(exc, "status_code", 403),
        detail={"error": str(DTO_AUTH_REJECTED), "reason": "forbidden",
                "message": getattr(exc, "message", str(exc))},
    )


async def _audit_failure(request: Request, exc: Exception, status_code: int) -> None:
    """失败审计（S1/S10）+ M12 日志（鉴权失败码 DTO_AUTH_REJECTED）。"""
    reason = getattr(exc, "reason", "forbidden")
    endpoint = normalize_path(request.url.path)
    ip = client_ip(request)
    log.warn(
        "auth rejected",
        op="auth_reject",
        route=endpoint,
        method=request.method,
        status=status_code,
        error_code=DTO_AUTH_REJECTED,
        reason=reason,
    )
    await log_auth_failure(
        reason,
        ip=ip,
        endpoint=endpoint,
        method=request.method,
        status_code=status_code,
        claimed_key_id=(request.headers.get(KEY_ID_HEADER) or None),
        db=auth_database(request),
    )


async def require_auth(request: Request) -> AuthContext:
    """**依赖项**：端点参数 ``ctx: AuthContext = Depends(require_auth)``。

    失败：401（无/坏凭据、时间窗、验签、重放）/ 403（公钥未注册、属主禁用）/ 429（限流）；
    失败同时落 ``auth`` 审计事件与 M12 日志（``error_code=DTO_AUTH_REJECTED``）。
    """
    try:
        return await resolve_request_identity(request)
    except (AuthError, ForbiddenError) as exc:
        if isinstance(exc, AuthenticationError) and exc.reason == _NO_USERS_REASON:
            if await _no_users():
                exc = AuthenticationError(exc.message + "；" + BOOTSTRAP_HINT, reason=exc.reason)
        await _audit_failure(request, exc, getattr(exc, "status_code", 401))
        raise http_error(exc) from exc


def require_permission(perm: str) -> Any:
    """**依赖项工厂**：要求角色/grant 覆盖某权限（无目标；带目标判定用 ``authorize_user``）。"""

    async def dependency(
        request: Request, context: AuthContext = Depends(require_auth)
    ) -> AuthContext:
        try:
            await authorize_user(context.user, perm, db=auth_database(request))
        except ForbiddenError as exc:
            raise http_error(exc) from exc
        return context

    dependency.__name__ = f"require_permission_{perm}"
    return dependency


def current_context(context: AuthContext = Depends(require_auth)) -> AuthContext:
    """别名依赖项（端点里读起来更顺：``ctx: AuthContext = Depends(current_context)``）。"""
    return context


# ------------------------------------------------------------------- Cookie（S6）


def _env_flag(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    return raw not in ("0", "false", "False")


def cookie_secure(request: Request | None = None) -> bool:
    """会话 Cookie 是否带 ``Secure``（S6）。

    判定顺序：``AUTH_COOKIE_SECURE`` 显式覆盖 → TLS 反向代理头（``AUTH_TRUSTED_PROXY=1``
    时的 ``X-Forwarded-Proto: https``）→ 请求 scheme ``https`` → **非 loopback 监听**
    （``API_HOST``）→ 默认 ``False``（仅 loopback 明文部署）。
    """
    override = os.environ.get("AUTH_COOKIE_SECURE")
    if override:
        return override not in ("0", "false", "False")
    if request is not None:
        if _env_flag("AUTH_TRUSTED_PROXY", False):
            if (request.headers.get("X-Forwarded-Proto") or "").lower() == "https":
                return True
        if request.url.scheme == "https":
            return True
    return not _is_loopback(os.environ.get("API_HOST", "127.0.0.1"))


def _is_loopback(host: str) -> bool:
    candidate = host.strip().strip("[]").lower()
    if candidate in ("localhost", "::1", ""):
        return True
    if candidate.startswith("127."):
        return True
    return False


def session_cookie_kwargs(request: Request | None = None) -> dict[str, Any]:
    """``Response.set_cookie`` 参数（httpOnly / SameSite=Lax / Secure / TTL）。"""
    return {
        "key": SESSION_COOKIE_NAME,
        "httponly": True,
        "samesite": "lax",
        "secure": cookie_secure(request),
        "path": "/",
        "max_age": session_ttl_seconds(),
    }


def set_session_cookie(
    response: Response, token: str, request: Request | None = None
) -> None:
    """签发会话 Cookie（明文 token 只在此处进入客户端）。"""
    kwargs = session_cookie_kwargs(request)
    response.set_cookie(value=token, **kwargs)


def clear_session_cookie(response: Response, request: Request | None = None) -> None:
    """清除会话 Cookie（``POST /auth/logout``）。"""
    kwargs = session_cookie_kwargs(request)
    response.delete_cookie(
        key=kwargs["key"], path=kwargs["path"], secure=kwargs["secure"],
        httponly=kwargs["httponly"], samesite=kwargs["samesite"],
    )
