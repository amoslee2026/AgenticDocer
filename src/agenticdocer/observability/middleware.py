"""FastAPI 埋点中间件（ADR-010 §2/§3.1、REQ-M12-F02/F03）。

每个 HTTP 请求：

1. 生成 rid 并写入 ContextVar（下游 M10 鉴权 → M06/M07 路由 → M02 存储 → M04 渲染
   的所有日志行共享同一 rid）；
2. 计时并记录 `route`（路由模板，非原始路径 → 指标基数可控）、`method`、`status`、`dur`；
3. 响应头回写 `X-Request-Id`，便于客户端与服务端日志对齐；
4. 状态码分级：`<400` INFO；`4xx` WARN（`401/403` 带 `DTO_AUTH_REJECTED`）；
   `>=500` ERROR（未捕获异常额外落 `.tracebacks` 轨迹）。

装配（`app.py`）：`agenticdocer.observability.install(app)`。
"""

from __future__ import annotations

import time
from typing import Any

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


def _route_of(request: Request) -> str:
    """路由模板（如 `/api/v1/docs/{doc_id}`）；未匹配到路由时回落原始路径。"""
    route = request.scope.get("route")
    path = getattr(route, "path", None)
    return path if isinstance(path, str) and path else request.url.path


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
            self._logger.error(message, error_code="INTERNAL_UNEXPECTED", **fields)
        elif status >= 400:
            error_code = str(DTO_AUTH_REJECTED) if status in _AUTH_STATUS else None
            self._logger.warn(message, error_code=error_code, **fields)
        else:
            self._logger.info(message, **fields)


def install(app: Any, module: str = DEFAULT_MODULE) -> None:
    """把埋点中间件加入 FastAPI 应用（须在应用启动前调用）。"""
    app.add_middleware(ObservabilityMiddleware, module=module)


__all__ = ["DEFAULT_MODULE", "REQUEST_ID_HEADER", "ObservabilityMiddleware", "install"]
