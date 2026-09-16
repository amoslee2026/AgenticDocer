"""FastAPI 埋点中间件（ADR-010 §2/§3.1、REQ-M12-F02/F03）。
2. 计时并记录 `route`、`method`、`status`、`dur`。`route` 取**路由模板**
   （`/api/v1/docs/{doc_id}`，非原始路径 → 指标基数可控）；**路由匹配前**就被拒的请求
   （M10 签名验证 401 等中间件层拒答、404）归入 :data:`UNROUTED` 单一桶，原始路径仍写在
   ctx 的 `path` 字段供下钻；
3. 响应头回写 `X-Request-Id`，便于客户端与服务端日志对齐；
4. 状态码分级：`<400` INFO；`4xx` WARN（`401/403` 带 `DTO_AUTH_REJECTED`）；
   `>=500` ERROR（未捕获异常额外落 `.tracebacks` 轨迹）。

**装配要求（不变量）**：`install(app)` 必须在鉴权中间件**之后**调用——Starlette 的
「最后加入者最外层」（`add_middleware` 为 `insert(0)` + 逆序包装）。否则被拒请求既不进本层、
也无 `X-Request-Id`，`/admin/metrics` 的 `authFailures` 恒 0 且无法 `trace --rid`
（不影响可追责性：审计权威源是 PG `events(entity='auth')`，见 ADR-010 审计分离原则）。
回归用例：`test_middleware_logs_rejection_raised_by_inner_middleware`。
"""

from __future__ import annotations

import time
from typing import Any

from agentic_logger import ErrorCode
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from agenticdocer.observability.error_codes import DTO_AUTH_REJECTED
from agenticdocer.observability.logger import ModuleLogger, get_logger
from agenticdocer.observability.rid import new_rid, set_rid

REQUEST_ID_HEADER = "X-Request-Id"

#: 未认证/未授权的 HTTP 状态码 → `DTO_AUTH_REJECTED`。
_AUTH_STATUS = frozenset({401, 403})

DEFAULT_MODULE = "m12.middleware"

#: 未匹配到路由时的 `route` 占位值。
#:
#: **中间件层拒答发生在路由匹配之前**（如 M10 的签名验证 401），此时 `scope["route"]`
#: 尚未写入。若回落原始路径，每个被拒路径都会成为独立指标桶（`/docs/SPEC-1`、
#: `/docs/SPEC-2`…）→ 基数爆炸且每桶计数为 1，`authFailures` 与错误率失去意义。
#: 故统一归入该桶；原始路径仍完整保留在 ctx 的 `path` 字段供下钻。
UNROUTED = "<unrouted>"


def _route_of(request: Request) -> str:
    """路由模板（如 `/api/v1/docs/{doc_id}`）；未匹配时返回 :data:`UNROUTED`。"""
    route = request.scope.get("route")
    path = getattr(route, "path", None)
    return path if isinstance(path, str) and path else UNROUTED


class ObservabilityMiddleware(BaseHTTPMiddleware):
    """请求级埋点中间件（rid + 耗时 + 状态码）。"""

    def __init__(self, app: ASGIApp, module: str = DEFAULT_MODULE) -> None:
        super().__init__(app)
        self._logger: ModuleLogger = get_logger(module)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        rid = new_rid()
        set_rid(rid)
        request.state.rid = rid
        started = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception as exc:
            self._log(request, 500, started, exc=exc)
            raise

        self._log(request, response.status_code, started)
        response.headers[REQUEST_ID_HEADER] = rid
        return response

    def _log(
        self,
        request: Request,
        status: int,
        started: float,
        exc: BaseException | None = None,
    ) -> None:
        dur = int((time.perf_counter() - started) * 1000)
        route = _route_of(request)
        fields: dict[str, Any] = {
            "route": route,
            "path": request.url.path,
            "method": request.method,
            "status": status,
            "dur": dur,
        }
        message = f"{request.method} {route} {status}"
        if exc is not None:
            self._logger.exception(message, exc, **fields)
        elif status >= 500:
            self._logger.error(message, error_code=ErrorCode.INTERNAL_UNEXPECTED, **fields)
        elif status >= 400:
            error_code = str(DTO_AUTH_REJECTED) if status in _AUTH_STATUS else None
            self._logger.warn(message, error_code=error_code, **fields)
        else:
            self._logger.info(message, **fields)


def install(app: Any, module: str = DEFAULT_MODULE) -> None:
    """把埋点中间件加入 FastAPI 应用（须在应用启动前调用）。"""
    app.add_middleware(ObservabilityMiddleware, module=module)


__all__ = ["DEFAULT_MODULE", "REQUEST_ID_HEADER", "ObservabilityMiddleware", "install"]
