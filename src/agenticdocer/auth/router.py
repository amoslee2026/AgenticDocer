"""M10 鉴权端点（REQ-M10-F02/F03；S4 豁免清单内的三个端点在此实现）。

| 方法/路径 | 鉴权 | 说明 |
|---|---|---|
| ``POST /api/v1/auth/challenge`` | 豁免（S4） | 签发一次性 nonce（TTL 120s，按 IP 限流） |
| ``POST /api/v1/auth/login`` | 豁免（S4） | 提交 SSHSIG → 验签 → 签发会话 Cookie（S13） |
| ``POST /api/v1/auth/logout`` | **需鉴权** | 销毁会话并清 Cookie（S4：豁免清单外必鉴权） |
| ``GET /api/v1/auth/me`` | 需鉴权 | 当前身份（``SessionDTO``，供登录页/whoami） |

装配：``app.include_router(router)``（M06/M07 侧）；依赖项从 ``app.state.auth_db`` /
``app.state.db`` 取 ``Database``（缺省回落进程单例，见 ``middleware.auth_database``）。

**失败审计（S10）**：登录失败由本模块落 ``auth`` 事件，``claimed_key_id`` 取请求自述的
``keyFingerprint``（绝不写身份列）；请求级失败（依赖项）在 ``middleware`` 落。
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, Request, Response

from agenticdocer.model import Grant, RoleName, User
from agenticdocer.observability import get_logger
from agenticdocer.store import ForbiddenError

from .errors import AuthError
from .middleware import (
    AuthContext,
    auth_database,
    clear_session_cookie,
    client_ip,
    http_error,
    normalize_path,
    require_auth,
    set_session_cookie,
)
from .sessions import SESSION_COOKIE_NAME, Challenge, LoginResult, create_challenge, login, logout
from .users import list_grants, log_auth_failure

__all__ = ["LoginRequest", "SessionDTO", "router"]

log = get_logger("m10.api")

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class LoginRequest:
    """占位说明：真正的请求体模型见 :class:`LoginRequest` 定义（pydantic ``Model``）。"""


from pydantic import BaseModel  # noqa: E402 - 见下方模型定义（保持模块顶部 import 顺序）


class LoginRequest(BaseModel):  # noqa: F811 - 覆盖占位
    """登录请求体（S12 两条路径：CLI 签名粘贴 / 上传签名文件，均提交 SSHSIG）。"""

    model_config = {"populate_by_name": True, "extra": "forbid"}

    key_fingerprint: str
    nonce: str
    signature: str


class SessionDTO(BaseModel):
    """会话身份快照（§3 M07 ``SessionDTO``：camelCase 序列化）。"""

    model_config = {"populate_by_name": True, "alias_generator": _to_camel, "extra": "forbid"}

    user_id: str
    username: str
    role: RoleName
    permissions: list[Grant]
    expires_at: datetime | None = None


@router.post("/challenge", response_model=Challenge)
async def post_challenge(request: Request) -> Challenge:
    """签发登录挑战 nonce（豁免端点；按 IP 限流，S7）。"""
    return await create_challenge(client_ip(request), db=auth_database(request))


@router.post("/login", response_model=SessionDTO)
async def post_login(
    payload: LoginRequest, request: Request, response: Response
) -> SessionDTO:
    """挑战-响应登录：验签通过 → Set-Cookie（httpOnly/SameSite=Lax/Secure，S6/S13）。"""
    try:
        result = await login(
            payload.key_fingerprint,
            payload.nonce,
            payload.signature,
            db=auth_database(request),
            ip=client_ip(request),
        )
    except (AuthError, ForbiddenError) as exc:
        await log_auth_failure(
            str(getattr(exc, "reason", "login_failed")),
            ip=client_ip(request),
            endpoint=normalize_path(request.url.path),
            method=request.method,
            status_code=int(getattr(exc, "status_code", 401)),
            claimed_key_id=payload.key_fingerprint,
            db=auth_database(request),
        )
        raise http_error(exc) from exc
    set_session_cookie(response, result.token, request)
    return await _session_dto(result, auth_database(request))


@router.post("/logout", status_code=204)
async def post_logout(
    request: Request,
    response: Response,
    context: AuthContext = Depends(require_auth),
) -> Response:
    """销毁会话（**需鉴权**：S4 豁免清单外端点无凭据必 401）。"""
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if token:
        await logout(token=token, db=auth_database(request))
    clear_session_cookie(response, request)
    response.status_code = 204
    log.info("logout", op="logout", user_id=context.actor)
    return response


@router.get("/me", response_model=SessionDTO)
async def get_me(
    request: Request, context: AuthContext = Depends(require_auth)
) -> SessionDTO:
    """当前身份（含 grant 权限快照，供登录页与 M11 ``auth whoami``）。"""
    grants = await list_grants(user_id=context.user.user_id, db=auth_database(request))
    return SessionDTO(
        user_id=str(context.user.user_id),
        username=context.user.username,
        role=context.user.role,
        permissions=grants,
        expires_at=None,
    )


async def _session_dto(result: LoginResult, db: Any) -> SessionDTO:
    user: User = result.user
    grants = await list_grants(user_id=user.user_id, db=db)
    return SessionDTO(
        user_id=str(user.user_id),
        username=user.username,
        role=user.role,
        permissions=grants,
        expires_at=result.session.expires_at,
    )
