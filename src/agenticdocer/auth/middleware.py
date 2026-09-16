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
  并记 M12 日志 ``error_code=DTO_AUTH_REJECTED``（ctx 用 ``route``/``method``/``status``）。

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

__all__ = [
    "EXEMPT_PATHS",
    "EXEMPT_PREFIXES",
    "KEY_ID_HEADER",
    "MIN_NONCE_CHARS",
    "NONCE_HEADER",
    "SESSION_COOKIE_NAME",
    "SIGNATURE_HEADER",
    "TIMESTAMP_HEADER",
    "AuthContext",
    "SshSigHeaders",
    "check_timestamp",
    "clear_session_cookie",
    "client_ip",
    "cookie_secure",
    "current_context",
    "is_exempt",
    "normalize_path",
    "parse_timestamp",
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
"""``X-Nonce`` 上界（防止把 ``nonces`` 表当存储用）。"""

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

_NO_CREDENTIALS_REASON: Final = "missing_credentials"
_FORBIDDEN_REASON: Final = "forbidden"


def normalize_path(path: str) -> str:
    """路径归一（去尾部斜杠、保留根路径）——豁免判定与审计端点名共用。"""
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


DOC_PATHS: Final[tuple[str, ...]] = ("/openapi.json", "/docs", "/redoc", "/docs/oauth2-redirect")
"""FastAPI 自带文档路由。**不在豁免白名单**（S4 要求非开发模式禁用，由 M06/M07 以
``docs_url=None`` 落地）；仅作 :func:`assert_auth_coverage` 的默认忽略项，避免把框架路由
误判为「漏挂鉴权」的漏洞路由。"""


def _route_guards(route: Any) -> set[Any]:
    """收集一个 ``APIRoute`` 依赖树里的全部依赖可调用对象（含嵌套 ``Depends``）。"""
    guards: set[Any] = set()
    stack = [getattr(route, "dependant", None)]
    while stack:
        dependant = stack.pop()
        if dependant is None:
            continue
        call = getattr(dependant, "call", None)
        if call is not None:
            guards.add(call)
        stack.extend(getattr(dependant, "dependencies", []) or [])
    return guards


def find_unguarded_routes(app: Any, *, ignore: tuple[str, ...] = DOC_PATHS) -> list[str]:
    """列出**未挂鉴权依赖**且不在豁免白名单内的路由（``"METHOD /path"``）。

    S4「清单外端点无凭据必 401」的**运行时强制点**：逐端点挂 ``Depends(require_auth)`` 时，
    新增路由漏挂即为静默开放；本函数把它降级为启动期可检出的错误。
    """
    from fastapi.routing import APIRoute

    unguarded: list[str] = []
    for route in getattr(app, "routes", []) or []:
        if not isinstance(route, APIRoute):
            continue
        path = normalize_path(getattr(route, "path", "") or "")
        if path in ignore:
            continue
        methods = sorted(m for m in (route.methods or set()) if m not in ("HEAD", "OPTIONS"))
        if methods and all(is_exempt(path, method) for method in methods):
            continue
        if require_auth in _route_guards(route):
            continue
        for method in methods or ["*"]:
            unguarded.append(f"{method} {path}")
    return unguarded


def assert_auth_coverage(app: Any, *, ignore: tuple[str, ...] = DOC_PATHS) -> None:
    """启动期自检：存在漏挂鉴权的非豁免路由即抛 ``RuntimeError``（fail-fast）。

    M06/M07 在 ``app`` 装配完成后调用一次；这是让 :func:`is_exempt` 成为**可执行断言**
    而非文档摆设的唯一代价最低方式——不必在请求路径上二次验签（那会重复消费 nonce）。
    """
    unguarded = find_unguarded_routes(app, ignore=ignore)
    if unguarded:
        raise RuntimeError(
            "S4 鉴权覆盖自检失败：以下路由既不在豁免白名单、也未挂 require_auth 依赖 —— "
            f"{unguarded}。请为其加上 Depends(require_auth)/Depends(require_permission(...))，"
            "或（确属公开资源）加入 EXEMPT_PATHS。"
        )

@dataclass(frozen=True, slots=True)
class SshSigHeaders:
    """``X-SSH-*`` 头（§3 M06；**无 ``X-Actor``**，S14）。"""

    signature: str
    key_id: str
    timestamp: str
    nonce: str

    @classmethod
    def present(cls, headers: Any) -> bool:
        """是否携带签名（用于区分「Cookie 路径」与「签名路径」）。"""
        return bool((headers.get(SIGNATURE_HEADER) or "").strip())

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
                f"缺少签名头 {sorted(missing)}（§3 M06：{SIGNATURE_HEADER} / {KEY_ID_HEADER} / "
                f"{TIMESTAMP_HEADER} / {NONCE_HEADER}）",
                reason=_NO_CREDENTIALS_REASON,
            )
        nonce = values[NONCE_HEADER]
        if (
            not MIN_NONCE_CHARS <= len(nonce) <= MAX_NONCE_CHARS
            or not set(nonce) <= _NONCE_ALPHABET
        ):
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


def parse_timestamp(text: str) -> datetime:
    """解析 ``X-Timestamp``（ISO 8601；无时区按 UTC）→ 解析失败即 401。"""
    candidate = text.strip()
    if candidate.endswith(("Z", "z")):
        candidate = candidate[:-1] + "+00:00"
    try:
        moment = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise AuthenticationError(
            f"{TIMESTAMP_HEADER} 不是合法 ISO 8601 时间：{text!r}", reason="bad_timestamp"
        ) from exc
    return (
        moment.astimezone(timezone.utc) if moment.tzinfo else moment.replace(tzinfo=timezone.utc)
    )


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
    """请求行中的 **RAW_PATH**（路径 + ``?`` + query 的**原样字节**；不百分号解码、不规范化，S2）。

    取 ASGI ``scope["raw_path"]``（请求行里未经解码的字节，**可选字段**）而非 ``scope["path"]``
    （已被百分号解码）——后者会让「签编码形态 vs 签解码形态」成为未写入规范的隐式耦合
    （SecAudit AUD-2）。字节经 ``latin-1`` 还原为字符串，与 ``request_payload`` 的编码口径
    在 **ASCII 目标**上逐字节一致；客户端契约因此是：**签请求行里那个（percent-encoded）目标串**，
    不要先解码。非 ASCII 字节不会静默错配——会验签失败（fail-closed）。

    服务器未实现 ``raw_path``（ASGI 允许省略）时回落到解码路径并**告警一次**：此时客户端必须
    改签解码形态，属降级而非默认口径。
    """
    query = request.scope.get("query_string") or b""
    suffix = "?" + query.decode("latin-1") if query else ""
    raw = request.scope.get("raw_path")
    if raw:
        return raw.decode("latin-1") + suffix
    _warn_missing_raw_path()
    return str(request.scope.get("path") or request.url.path) + suffix


_MISSING_RAW_PATH_WARNED: bool = False


def _warn_missing_raw_path() -> None:
    """ASGI ``raw_path`` 缺失时的**一次性**告警（避免逐请求刷日志）。"""
    global _MISSING_RAW_PATH_WARNED
    if _MISSING_RAW_PATH_WARNED:
        return
    _MISSING_RAW_PATH_WARNED = True
    log.warn(
        "ASGI scope 未提供 raw_path：回落解码路径拼载荷（客户端须签解码形态）",
        op="raw_path",
    )


def client_ip(request: Request) -> str | None:
    """客户端 IP（限流与审计的键）。

    ``AUTH_TRUSTED_PROXY=1`` 时才采信 ``X-Forwarded-For``，且取**由可信代理追加的那一段**：
    从**右往左数第 ``AUTH_PROXY_COUNT``（默认 1）** 段。取首段（旧实现）等于把限流键交给
    客户端伪造（SecAudit AUD-1：逐次改首段即可无限打 ``/auth/challenge`` 并让 ``nonces``
    无界增长）。

    契约：**可信反代必须 append（而非透传客户端已给的 XFF）**；链长不足 ``AUTH_PROXY_COUNT``
    时视为头不可信，回落直连对端地址（宁可收紧，不可放松）。
    """
    peer = request.client.host if request.client is not None else None
    if not _env_flag("AUTH_TRUSTED_PROXY", False):
        return peer
    forwarded = request.headers.get("X-Forwarded-For")
    if not forwarded:
        return peer
    hops = [part.strip() for part in forwarded.split(",") if part.strip()]
    trusted_hops = max(1, _env_int("AUTH_PROXY_COUNT", 1))
    if len(hops) < trusted_hops:
        return peer
    return hops[-trusted_hops]


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
    source: WriteSource
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
    """请求身份 → 存储层 ``WriteContext``（``actor`` 取验签结果，``source`` 取凭据类型）。"""
    return WriteContext(actor=context.actor, source=context.source)


async def verify_signature(
    method: str,
    path: str,
    body: bytes,
    headers: SshSigHeaders,
    *,
    db: Database | None = None,
) -> AuthContext:
    """agent 路径验签（§3 M06 / S2 / S3 / S7）。

    顺序：① 时间窗 → ② 公钥查表（``revoked_at IS NULL`` 且属主 active）→ ③ SSHSIG 验签 →
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
        user=user_from_row(user_row), source="agent", key_fingerprint=key["key_id"]
    )


async def _no_users(db: Database | None) -> bool:
    from sqlalchemy import func, select

    from agenticdocer.store.schema import users as users_table

    async with _db_or_default(db).session() as session:
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
                "会话无效/已过期（S8/S15；请重新登录）", reason="invalid_session"
            )
        return AuthContext(user=user, source="webui", session_hash=session_token_hash(token))
    headers = SshSigHeaders.parse(request.headers)
    return await verify_signature(
        request.method, raw_path(request), await request.body(), headers, db=database
    )


def http_error(exc: Exception) -> HTTPException:
    """领域异常 → ``HTTPException``（401/403/429），``detail`` 带 ``code``/``reason``。"""
    if isinstance(exc, AuthError):
        headers = (
            {"WWW-Authenticate": 'SSHSIG realm="agenticdocer"'}
            if exc.status_code == 401
            else None
        )
        return HTTPException(
            status_code=exc.status_code,
            detail={
                "error": str(DTO_AUTH_REJECTED),
                "reason": exc.reason,
                "message": exc.message,
            },
            headers=headers,
        )
    return HTTPException(
        status_code=int(getattr(exc, "status_code", 403)),
        detail={
            "error": str(DTO_AUTH_REJECTED),
            "reason": _FORBIDDEN_REASON,
            "message": str(getattr(exc, "message", exc)),
        },
    )


async def _audit_failure(request: Request, exc: Exception, status_code: int) -> None:
    """失败审计（S1/S10）+ M12 日志（鉴权失败码 ``DTO_AUTH_REJECTED``）。"""
    reason = str(getattr(exc, "reason", _FORBIDDEN_REASON))
    endpoint = normalize_path(request.url.path)
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
        ip=client_ip(request),
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
        failure: Exception = exc
        if isinstance(exc, AuthenticationError) and exc.reason == _NO_CREDENTIALS_REASON:
            database = auth_database(request)
            if await _no_users(database):
                failure = AuthenticationError(
                    f"{exc.message}；{BOOTSTRAP_HINT}", reason=exc.reason
                )
        await _audit_failure(request, failure, int(getattr(failure, "status_code", 401)))
        raise http_error(failure) from exc


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
    """别名依赖项（端点里更顺：``ctx: AuthContext = Depends(current_context)``）。"""
    return context


# -------------------------------------------------------------------- Cookie（S6）


def _env_flag(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    return raw not in ("0", "false", "False")



def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


def cookie_secure(request: Request | None = None) -> bool:
    """会话 Cookie 是否带 ``Secure``（S6）。

    顺序：``AUTH_COOKIE_SECURE`` 显式覆盖 → TLS 反向代理头（``AUTH_TRUSTED_PROXY=1`` 时的
    ``X-Forwarded-Proto: https``）→ 请求 scheme ``https`` → **非 loopback 监听**（``API_HOST``）
    → 默认 ``False``（仅 loopback 明文部署，§5）。
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
    return candidate.startswith("127.")


def session_cookie_kwargs(request: Request | None = None) -> dict[str, Any]:
    """``Response.set_cookie`` 参数（httpOnly / SameSite=Lax / Secure / TTL 8h）。"""
    return {
        "key": SESSION_COOKIE_NAME,
        "httponly": True,
        "samesite": "lax",
        "secure": cookie_secure(request),
        "path": "/",
        "max_age": session_ttl_seconds(),
    }


def set_session_cookie(response: Response, token: str, request: Request | None = None) -> None:
    """签发会话 Cookie（明文 token 只在此处进入客户端）。"""
    response.set_cookie(value=token, **session_cookie_kwargs(request))


def clear_session_cookie(response: Response, request: Request | None = None) -> None:
    """清除会话 Cookie（``POST /auth/logout``）。"""
    kwargs = session_cookie_kwargs(request)
    response.delete_cookie(
        key=kwargs["key"],
        path=kwargs["path"],
        secure=kwargs["secure"],
        httponly=kwargs["httponly"],
        samesite=kwargs["samesite"],
    )
