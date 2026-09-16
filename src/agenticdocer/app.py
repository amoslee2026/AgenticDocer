"""FastAPI 装配（M06/M07/M10/M12 的单一挂载点；§5 部署、§6 横切、ADR-007/ADR-010）。

| 装配项 | 内容 |
|---|---|
| 路由 | M10 `/api/v1/auth/*`（`auth.router`）+ M06 `agent_api` + M07 `webui_api` |
| 中间件 | `observability.install()`：请求级 rid/耗时/状态码埋点（ADR-010） |
| 静态 | `WEBUI_DIST_DIR`（默认 `webui/dist`）存在时挂载于 `/`（M08 前端产物）；不存在则纯 API |
| 探针 | `GET /healthz`（S4 豁免；**不含任何业务/版本信息**） |
| 文档面 | `/docs`、`/redoc`、`/openapi.json`：**非 `DEV_MODE` 一律 `None`**（S4）；`DEV_MODE=1` 且监听 loopback 才开 |
| 生命周期 | 启动：管理员自举（REQ-M10-F05）+ 过期清理（S15）→ 每 `PURGE_INTERVAL_SECONDS`（默认 3600）清理一次 |

**错误映射（§6 横切）**：`ConflictError`→409、`ValidationError`→422（携 `violations[]`）、
`NotFoundError`→404、`ForbiddenError`→403；请求体契约错误同样归一为 422 + `violations[]`
（REQ-M06-F02：agent 据 `fixHint` 自修复重试）。

**部署入口**：`agenticdocer-api`（pyproject `[project.scripts]`）→ :func:`main`，读
`API_HOST`/`API_PORT`（默认 `127.0.0.1:8787`，§5 安全默认：非 loopback 必须经 TLS 反代）；
也可 `uvicorn agenticdocer.app:app`（模块级 :data:`app` 已装配）。
"""

from __future__ import annotations

import argparse
import asyncio
import ipaddress
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress
from pathlib import Path
from typing import Any, Final

import uvicorn
import yaml
from sqlalchemy import insert, select, update
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from agenticdocer.auth import (
    BOOTSTRAP_HINT,
    admin_pubkey_file,
    assert_auth_coverage,
    bootstrap_admin,
    purge_expired,
)

from agenticdocer import __version__
from agenticdocer.agent_api import ErrorResponse
from agenticdocer.agent_api import router as agent_router
from agenticdocer.auth.router import router as auth_router
from agenticdocer.observability import get_logger, install
from agenticdocer.store import Database, StoreError, Storage, get_database
from agenticdocer.store.schema import terms as terms_table
from agenticdocer.webui_api import router as webui_router

__all__ = [
    "DEFAULT_API_HOST",
    "DEFAULT_API_PORT",
    "app",
    "create_app",
    "dev_mode",
    "main",
    "mount_webui",
    "webui_dist",
]

log = get_logger("app.api")

DEFAULT_API_HOST: Final = "127.0.0.1"
"""默认监听地址（§5 安全默认：无 TLS 时仅 loopback——明文 HTTP 下会话 Cookie 可被嗅探）。"""

DEFAULT_API_PORT: Final = 8787
"""默认端口（§5 systemd 单元）。"""

DEFAULT_WEBUI_DIST: Final = "webui/dist"
"""M08 前端构建产物目录（`WEBUI_DIST_DIR` 可覆盖）。"""

DEFAULT_PURGE_INTERVAL_SECONDS: Final = 3600
"""过期清理周期（S15：会话 + nonce 同一任务）。"""

DEFAULT_TERMS_SEED: Final = "data/terms_seed.yaml"
"""规范用语种子文件（`TERMS_SEED` 可覆盖；§5：随 migrate/启动载入 `terms` 表）。"""

_MIN_PURGE_INTERVAL_SECONDS: Final = 60

_STATUS_ERRORS: Final = {
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    409: "conflict",
    422: "validation",
}
"""HTTP 状态 → 稳定错误串（`code` 字段另给 `DTO_*`，§3 M12）。"""

ERROR_RESPONSES: Final[dict[int, dict[str, Any]]] = {
    status: {"model": ErrorResponse, "description": description}
    for status, description in (
        (401, "无凭据或凭据无效（S4：豁免清单外 fail-closed）"),
        (403, "角色或文档集级授权不足（S5）"),
        (404, "实体不存在（或已软删，A2）"),
        (409, "乐观锁版本不匹配或唯一约束冲突（可重试）"),
        (422, "请求/载荷校验失败；携 `violations[]` 与 `fixHint`（REQ-M06-F02）"),
    )
}
"""全局错误响应声明（§6 错误映射）：让错误形状（含 `Violation`）进入 OpenAPI。"""


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


def _is_loopback(host: str) -> bool:
    candidate = host.strip().strip("[]").lower()
    if candidate in ("", "localhost"):
        return True
    try:
        return ipaddress.ip_address(candidate).is_loopback
    except ValueError:
        return False


def dev_mode() -> bool:
    """是否开发模式（`/docs` 等开启）：`DEV_MODE=1` **且** 监听 loopback（S4）。

    非 loopback 监听时即使用 `DEV_MODE=1` 也保持禁用——文档面与 OpenAPI 是内部实现细节，
    不应随对外监听暴露。
    """
    if not _env_flag("DEV_MODE", False):
        return False
    host = os.environ.get("API_HOST", DEFAULT_API_HOST)
    if not _is_loopback(host):
        log.warn(
            "DEV_MODE 与非 loopback 监听冲突：仍禁用 /docs、/openapi.json（S4）",
            op="app_config",
            host=host,
        )
        return False
    return True


def webui_dist() -> Path:
    """M08 构建产物目录（`WEBUI_DIST_DIR`，默认仓库 `webui/dist`）。"""
    return Path(os.environ.get("WEBUI_DIST_DIR", DEFAULT_WEBUI_DIST))


def mount_webui(application: FastAPI) -> bool:
    """把 M08 前端产物挂到 `/`（存在才挂）；返回是否挂载。

    `/` 与登录页静态资源属 S4 豁免白名单；API 路由先注册，故 `/api/v1/*` 不受挂载影响。
    """
    dist = webui_dist()
    if not (dist / "index.html").is_file():
        log.info("webui/dist 不存在：跳过静态托管（纯 API 部署）", op="mount_webui", path=str(dist))
        return False
    application.mount("/", StaticFiles(directory=dist, html=True), name="webui")
    log.info("M08 前端产物已挂载", op="mount_webui", path=str(dist))
    return True


# ── 异常处理器（§6 横切：领域异常 → HTTP）──────────────────────────────


async def store_error_handler(request: Request, exc: StoreError) -> JSONResponse:
    """存储/授权领域异常 → 409/422/404/403（`violations[]` 随 422 返回）。"""
    detail: dict[str, Any] = {
        "error": _STATUS_ERRORS.get(exc.status_code, "store_error"),
        "message": exc.message,
    }
    if exc.code is not None:
        detail["code"] = str(exc.code)
    if exc.entity is not None:
        detail["entity"] = exc.entity
    if exc.entity_id is not None:
        detail["entityId"] = str(exc.entity_id)
    violations = getattr(exc, "violations", None)
    if violations:
        detail["violations"] = [item.model_dump(by_alias=True) for item in violations]
    log.warn(
        "request rejected",
        op="store_error",
        status=exc.status_code,
        route=request.url.path,
        method=request.method,
        code=str(exc.code) if exc.code is not None else None,
    )
    return JSONResponse(status_code=exc.status_code, content=detail)


async def request_validation_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """请求体/查询参数契约错误 → 422 + `violations[]`（REQ-M06-F02 的自修复入口）。"""
    violations = [_request_violation(error) for error in exc.errors()]
    log.warn(
        "request contract violated",
        op="request_validation",
        status=422,
        route=request.url.path,
        method=request.method,
        violations=len(violations),
    )
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation",
            "message": "请求不符接口契约（见 violations）",
            "violations": violations,
        },
    )


def _request_violation(error: Any) -> dict[str, Any]:
    """pydantic 错误项 → `Violation` 形态（camelCase；带可操作 `fixHint`）。"""
    location = [str(part) for part in error.get("loc", ())]
    kind = str(error.get("type", "invalid"))
    field = location[-1] if location else ""
    if kind == "missing":
        fix_hint: str | None = f"补齐必填字段 {field}"
    elif kind == "extra_forbidden":
        fix_hint = f"移除未声明字段 {field}"
    else:
        fix_hint = None
    return {
        "ruleId": f"api.request.{kind}",
        "path": "/".join(location),
        "message": str(error.get("msg", "")),
        "fixHint": fix_hint,
    }


# ── 生命周期（自举 + 过期清理，REQ-M10-F05/S15）────────────────────────


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    """启动自举与清理守护；退出时取消守护并释放自建连接池。"""
    database: Database = application.state.db
    await _bootstrap_admin(database)
    await _load_terms_seed(database)
    await _purge_once(database)
    purger = asyncio.create_task(_purge_loop(database), name="agenticdocer-purge")
    log.info("API 就绪", op="startup", routes=len(application.routes))
    try:
        yield
    finally:
        purger.cancel()
        with suppress(asyncio.CancelledError):
            await purger
        if application.state.owns_db:
            await database.dispose()
        log.info("API 已停止", op="shutdown")


async def _bootstrap_admin(database: Database) -> None:
    """管理员自举（REQ-M10-F05）：公钥文件存在才执行，否则保持 fail-closed 并提示自举步骤。"""
    path = admin_pubkey_file()
    if not path.is_file():
        log.warn(
            "管理员公钥文件不存在：跳过自举（无用户时全端点 401，系统 fail-closed）",
            op="bootstrap_admin",
            path=str(path),
            hint=BOOTSTRAP_HINT,
        )
        return
    user = await bootstrap_admin(path, db=database)
    log.info(
        "管理员自举完成（幂等）",
        op="bootstrap_admin",
        username=user.username,
        user_id=str(user.user_id),
    )


async def _load_terms_seed(database: Database) -> int:
    """幂等载入规范用语种子（§5 `TERMS_SEED`；R10 的第三个写入路径，另两条为 M03 导入与 M07 API）。

    只做「缺失即插、`kind` 漂移即纠偏」，**不删除**非种子条目——语料自身的 glossary 由 M03 写入，
    不属种子管辖。种子文件不存在则跳过（记录告警），与管理员自举同一「缺配置即降级」口径。

    :returns: 本次新插入的行数（0 即「已是最新」，幂等可重跑）。
    """
    path = Path(os.environ.get("TERMS_SEED", DEFAULT_TERMS_SEED)).expanduser()
    if not path.is_file():
        log.warn("术语种子文件不存在：跳过载入", op="terms_seed", path=str(path))
        return 0
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    declared = payload.get("terms") or []
    if not isinstance(declared, list):
        raise ValueError(f"{path}: `terms` 必须是列表（TERMS_SEED 格式）")
    inserted = 0
    async with database.transaction() as session:
        for entry in declared:
            term = str((entry or {}).get("term") or "").strip()
            kind = str((entry or {}).get("kind") or "normative-keyword")
            if not term:
                raise ValueError(f"{path}: 条目缺 `term` 字段")
            existing = (
                await session.execute(
                    select(terms_table.c.kind).where(terms_table.c.term == term)
                )
            ).first()
            if existing is None:
                await session.execute(
                    insert(terms_table).values(
                        term=term, definition_node_id=None, kind=kind
                    )
                )
                inserted += 1
            elif existing.kind != kind:
                await session.execute(
                    update(terms_table).where(terms_table.c.term == term).values(kind=kind)
                )
    log.info(
        "术语种子载入完成",
        op="terms_seed",
        path=str(path),
        declared=len(declared),
        inserted=inserted,
    )
    return inserted


async def _purge_loop(database: Database) -> None:
    """周期性过期清理（S15）：会话 + 过期 nonce + 鉴权失败聚合。"""
    interval = max(
        _MIN_PURGE_INTERVAL_SECONDS,
        _env_int("PURGE_INTERVAL_SECONDS", DEFAULT_PURGE_INTERVAL_SECONDS),
    )
    while True:
        await asyncio.sleep(interval)
        await _purge_once(database)


async def _purge_once(database: Database) -> None:
    """单次清理；失败只记日志（后台守护不得因一次库故障拖垮 API）。"""
    try:
        report = await purge_expired(db=database)
    except Exception as exc:  # noqa: BLE001 —— 守护任务的任何失败都降级为「下一轮重试」
        log.error(
            "过期清理失败（下一轮重试）",
            op="purge_expired",
            reason=f"{type(exc).__name__}: {exc}",
        )
        return
    log.info(
        "过期清理完成",
        op="purge_expired",
        sessions=report.sessions,
        nonces=report.nonces,
        failure_aggregates=report.failure_aggregates,
    )


# ── 应用工厂与入口 ─────────────────────────────────────────────────────


def create_app(
    *,
    storage: Storage | None = None,
    db: Database | None = None,
    dev: bool | None = None,
) -> FastAPI:
    """装配 API 应用。

    :param storage: 注入 M02 `Storage`（测试/嵌入式用）；缺省按 `db` 构造。
    :param db: 注入 `Database`；缺省用进程单例（`DATABASE_URL`）。注入者保留所有权（不 dispose）。
    :param dev: 覆盖开发模式判定（`/docs` 开关，S4）；缺省读 `DEV_MODE` + loopback 判定。
    """
    development = dev_mode() if dev is None else dev
    database = db if db is not None else get_database()
    application = FastAPI(
        title="AgenticDocer API",
        version=__version__,
        summary="芯片设计知识库：结构化库为唯一权威源（M06 Agent 接口 + M07 WebUI API）",
        docs_url="/docs" if development else None,
        redoc_url="/redoc" if development else None,
        openapi_url="/openapi.json" if development else None,
        responses=ERROR_RESPONSES,
        lifespan=lifespan,
    )
    application.state.db = database
    application.state.auth_db = database
    application.state.storage = storage if storage is not None else Storage(database)
    application.state.owns_db = db is None



    @application.get("/healthz", include_in_schema=False)
    async def healthz() -> dict[str, str]:
        """进程存活探针（S4 豁免；不返回业务数据、版本或依赖状态）。"""
        return {"status": "ok"}

    application.include_router(auth_router)
    application.include_router(agent_router)
    application.include_router(webui_router)
    application.add_exception_handler(StoreError, store_error_handler)
    application.add_exception_handler(RequestValidationError, request_validation_handler)

    # AUD-6/S4 启动期自检：漏挂鉴权依赖的非豁免路由 → 装配即失败（而非静默开放）
    assert_auth_coverage(application)

    # M12 埋点中间件**最后**装入（Starlette：后加入者最外层）——只有观测在最外层，被内层
    # 鉴权中间件拒绝的请求才会带上 rid 进日志（否则 `/admin/metrics` 的 authFailures 恒 0、
    # `trace --rid` 追不到 401 互操作问题）
    install(application)
    # AUD-6/S4 启动期自检：漏挂鉴权依赖的非豁免路由 → 装配即失败（而非静默开放）
    assert_auth_coverage(application)

    mounted = mount_webui(application)
    log.info(
        "API 装配完成",
        op="create_app",
        routes=len(application.routes),
        dev_mode=development,
        webui=mounted,
    )
    return application


app = create_app()
"""模块级应用（`uvicorn agenticdocer.app:app` 直接可用）。"""


def main(argv: list[str] | None = None) -> int:
    """`agenticdocer-api` 入口：`--host`/`--port` 优先，缺省读 `API_HOST`/`API_PORT`。

    `API_HOST` 同时决定 S4（`DEV_MODE` 仅 loopback 开文档面）与 S6（非 loopback 强制 Secure
    Cookie），故命令行的 `--host` 会写回该环境变量，保证两处判定与实际监听一致。
    """
    parser = argparse.ArgumentParser(
        prog="agenticdocer-api", description="AgenticDocer API（M06/M07/M10/M12）"
    )
    parser.add_argument("--host", default=os.environ.get("API_HOST", DEFAULT_API_HOST))
    parser.add_argument("--port", type=int, default=_env_int("API_PORT", DEFAULT_API_PORT))
    args = parser.parse_args(argv)
    os.environ["API_HOST"] = args.host
    log.info("API 启动", op="main", host=args.host, port=args.port)
    uvicorn.run(create_app(), host=args.host, port=args.port)
    return 0


if __name__ == "__main__":  # pragma: no cover - 进程入口
    raise SystemExit(main())
