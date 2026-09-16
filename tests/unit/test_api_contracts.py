"""M06/M07 接口契约测试（OpenAPI 形状 + 全端点鉴权；**不需要 PG**）。

判据来源：`spec/arch_spec/architecture_specification.md` §3 M06/M07（端点表 + TS 契约）、
§5（`DEV_MODE` 与非 loopback 判定）、`functional_specification.md` REQ-M06-F01/F02、
REQ-M07-F01..F06。断言的是**契约形状**（路径/方法/字段名/参数），不触库、不启进程。
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any, Final

import pytest
from fastapi.routing import APIRoute
from httpx import ASGITransport, AsyncClient

from agenticdocer.app import create_app, dev_mode
from agenticdocer.auth.middleware import EXEMPT_PATHS, is_exempt

M06_ROUTES: Final[dict[str, set[str]]] = {
    "/api/v1/nodes": {"POST"},
    "/api/v1/nodes/{node_id}": {"GET", "DELETE"},
    "/api/v1/refs": {"POST", "DELETE"},
    "/api/v1/docs/{doc_id}/nodes": {"GET"},
    "/api/v1/docs/{doc_id}/sections": {"GET"},
    "/api/v1/docs/{doc_id}/render": {"GET", "POST"},
    "/api/v1/assets/{asset_id}": {"GET"},
}
"""§3 M06 端点表（**不含**已移除的 `/nodes/{id}/traverse` 与 `/search`，B5/ADR-008）。"""

M07_ROUTES: Final[dict[str, set[str]]] = {
    "/api/v1/docs": {"GET"},
    "/api/v1/docs/{doc_id}": {"GET"},
    "/api/v1/docs/{doc_id}/status": {"POST"},
    "/api/v1/docs/{doc_id}/diff": {"GET"},
    "/api/v1/schemas": {"GET", "POST"},
    "/api/v1/schemas/{atom_type}": {"GET"},
    "/api/v1/events": {"GET"},
    "/api/v1/events/replay": {"GET"},
    "/api/v1/terms": {"GET", "POST"},
    "/api/v1/comments": {"GET", "POST"},
    "/api/v1/comments/{comment_id}": {"PATCH"},
    "/api/v1/nodes/{node_id}/table": {"PATCH"},
    "/api/v1/admin/metrics": {"GET"},
    "/api/v1/admin/health": {"GET"},
    "/api/v1/users": {"GET", "POST"},
    "/api/v1/users/{user_id}": {"PATCH", "DELETE"},
    "/api/v1/users/{user_id}/keys": {"POST", "DELETE"},
    "/api/v1/roles": {"GET"},
    "/api/v1/grants": {"GET", "POST"},
    "/api/v1/grants/{grant_id}": {"DELETE"},
}
"""§3 M07 端点表（`/auth/*` 由 M10 提供，另列于 `M10_ROUTES`）。"""

M10_ROUTES: Final[dict[str, set[str]]] = {
    "/api/v1/auth/challenge": {"POST"},
    "/api/v1/auth/login": {"POST"},
    "/api/v1/auth/logout": {"POST"},
    "/api/v1/auth/me": {"GET"},
}
"""§3 M10（B2）：鉴权端点由 M10 的 router 装配，M06/M07 **不得重复实现**。"""

TS_CONTRACT_FIELDS: Final[dict[str, set[str]]] = {
    "Node": {
        "nodeId",
        "docId",
        "atomType",
        "format",
        "anchor",
        "parentNodeId",
        "level",
        "content",
        "version",
        "status",
    },
    "Doc": {"docId", "docType", "title", "status", "version", "updatedAt"},
    "Comment": {
        "commentId",
        "nodeId",
        "targetEventId",
        "body",
        "state",
        "author",
        "version",
        "ts",
    },
    "Event": {"eventId", "entity", "entityId", "op", "payload", "actor", "ts"},
    "SchemaDef": {"typeName", "version", "jsonSchema"},
    "UserView": {"userId", "username", "role", "status", "keyFingerprints", "createdAt"},
    "Grant": {"userId", "scope", "value", "permission"},
    "SectionInfo": {"nodeId", "anchor", "title", "level", "ordinal", "childCount"},
    "Violation": {"ruleId", "path", "message", "fixHint"},
}
"""§3 M07「前端契约（TS）」逐字段对照（camelCase，A11 序列化口径）。"""


# ------------------------------------------------------------------ 夹具


@pytest.fixture(scope="module")
def spec() -> dict[str, Any]:
    """装配后的 OpenAPI 文档（非 DEV_MODE 也**可按需导出**，仅 HTTP 面 `/openapi.json` 被禁用）。"""
    return create_app(dev=False).openapi()


def _iter_api_routes(container: Any) -> Iterator[APIRoute]:
    """递归收集 `APIRoute`（FastAPI 0.141 的 `include_router` 产生嵌套 `_IncludedRouter`）。"""
    for route in getattr(container, "routes", []) or []:
        if isinstance(route, APIRoute):
            yield route
            continue
        nested = getattr(route, "original_router", None) or getattr(route, "router", None) or route
        if nested is not route:
            yield from _iter_api_routes(nested)


def _dependency_names(dependant: Any) -> set[str]:
    """依赖链上的 callable 名（含传递依赖）。"""
    names: set[str] = set()
    for dependency in getattr(dependant, "dependencies", []) or []:
        call = getattr(dependency, "call", None)
        if call is not None:
            names.add(getattr(call, "__name__", str(call)))
        names |= _dependency_names(dependency)
    return names


# -------------------------------------------------- 端点表与契约形状


def test_route_table_matches_spec(spec: dict[str, Any]) -> None:
    """§3 M06/M07/M10 端点表**逐条**存在，且无表外路径。"""
    paths = spec["paths"]
    expected = {**M06_ROUTES, **M07_ROUTES, **M10_ROUTES}
    missing: list[str] = []
    for path, methods in expected.items():
        for method in methods:
            if method.lower() not in paths.get(path, {}):
                missing.append(f"{method} {path}")
    assert not missing, f"缺失端点：{missing}"

    extra = {
        f"{method.upper()} {path}"
        for path, operations in paths.items()
        if path not in expected
        for method in operations
    } | {
        f"{method.upper()} {path}"
        for path, operations in paths.items()
        if path in expected
        for method in operations
        if method.upper() not in expected[path]
    }
    assert not extra, f"表外端点（未在 §3 端点表内）：{sorted(extra)}"


def test_removed_m05_endpoints_are_absent(spec: dict[str, Any]) -> None:
    """B5/ADR-008：`/nodes/{id}/traverse` 与 `/search` **不得**出现（检索属 LightRAG）。"""
    assert not [path for path in spec["paths"] if "traverse" in path or "search" in path]


def test_ts_contract_field_names(spec: dict[str, Any]) -> None:
    """§3 M07 TS 契约字段（camelCase）与实现的序列化字段一致。"""
    schemas = spec["components"]["schemas"]
    for model, fields in TS_CONTRACT_FIELDS.items():
        assert model in schemas, f"OpenAPI 缺少模型 {model}"
        properties = set(schemas[model].get("properties", {}))
        assert fields <= properties, f"{model} 缺字段：{sorted(fields - properties)}"


def test_write_contracts_expose_optimistic_locks(spec: dict[str, Any]) -> None:
    """写入契约的乐观锁字段名（camelCase）与 `expectedVersion` 口径一致。"""
    schemas = spec["components"]["schemas"]
    assert "expectedVersion" in schemas["NodeUpsert"]["properties"]
    assert "expectedVersion" in schemas["TableEdit"]["properties"]
    assert "expectedVersion" in schemas["StatusChange"]["properties"]
    assert "expectedVersion" in schemas["CommentStateChange"]["properties"]
    # 节点写入体 = §3.0 `NodeIn` 全字段 + `expectedVersion`（§3 M06「NodeIn + expected_version」）
    node_in_fields = {
        "nodeId",
        "docId",
        "atomType",
        "format",
        "ordinal",
        "parentNodeId",
        "level",
        "anchor",
        "content",
    }
    assert node_in_fields <= set(schemas["NodeUpsert"]["properties"])


def test_diff_contract(spec: dict[str, Any]) -> None:
    """REQ-M07-F06：`from`/`to` 查询参数 + 逐字段 `{before, after}` + `nodeId`/`anchor`/`field`。"""
    operation = spec["paths"]["/api/v1/docs/{doc_id}/diff"]["get"]
    params = {param["name"] for param in operation["parameters"]}
    assert {"from", "to"} <= params
    entry = spec["components"]["schemas"]["DiffEntry"]["properties"]
    assert {"nodeId", "anchor", "op", "field", "before", "after"} <= set(entry)
    diff = spec["components"]["schemas"]["DocDiff"]["properties"]
    assert {"docId", "fromTs", "toTs", "changes", "summary"} <= set(diff)


def test_admin_endpoints_are_present_and_scoped(spec: dict[str, Any]) -> None:
    """ADR-010：`/admin/metrics`、`/admin/health` 存在并返回指标/健康报告结构。"""
    assert "/api/v1/admin/metrics" in spec["paths"]
    assert "/api/v1/admin/health" in spec["paths"]
    schemas = spec["components"]["schemas"]
    assert {"windowSeconds", "endpoints", "slowQueries", "authFailures", "render"} <= set(
        schemas["MetricsSnapshot"]["properties"]
    )
    assert {"tables", "indexes", "partitions", "pool", "verdict", "advice"} <= set(
        schemas["HealthReport"]["properties"]
    )


def test_openapi_is_exportable_json(spec: dict[str, Any]) -> None:
    """契约可导出为 JSON（M08 前端据此生成客户端类型）。"""
    assert spec["openapi"].startswith("3.")
    assert spec["info"]["title"] == "AgenticDocer API"
    payload = json.dumps(spec, ensure_ascii=False)
    assert "X-Actor" not in payload and "x-actor" not in payload


# ------------------------------------------------------------ 端点鉴权（S4）


def test_every_business_endpoint_requires_credentials() -> None:
    """S4：**豁免清单外**所有端点都挂 `require_auth`/`require_permission`；豁免端点不挂。"""
    application = create_app(dev=False)
    bare: list[str] = []
    unexpected_deps: list[str] = []
    for route in _iter_api_routes(application):
        names = _dependency_names(route.dependant)
        guarded = any(
            name == "require_auth" or name.startswith("require_permission_") for name in names
        )
        exempt = is_exempt(route.path)
        if exempt and guarded:
            unexpected_deps.append(route.path)
        if not exempt and not guarded:
            bare.append(f"{sorted(route.methods)} {route.path}")
    assert not bare, f"未挂鉴权依赖的业务端点：{bare}"
    assert not unexpected_deps, f"豁免端点不应要求凭据：{unexpected_deps}"


def test_exempt_paths_are_the_s4_whitelist() -> None:
    """S4 白名单：`/`、`/healthz`、`/auth/challenge`、`/auth/login` + 登录页静态资源。"""
    assert set(EXEMPT_PATHS) == {
        "/",
        "/healthz",
        "/api/v1/auth/challenge",
        "/api/v1/auth/login",
        "/auth/challenge",
        "/auth/login",
    }
    assert is_exempt("/healthz") is True
    assert is_exempt("/assets/login-app.js") is True
    # 明确**不豁免**：文档面与业务端点
    for path in ("/docs", "/openapi.json", "/redoc", "/api/v1/docs", "/api/v1/admin/health"):
        assert is_exempt(path) is False, path



def test_docs_surface_disabled_outside_dev_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    """非 `DEV_MODE`：`/docs`、`/redoc`、`/openapi.json` 全部禁用（`None`，S4）。"""
    monkeypatch.delenv("DEV_MODE", raising=False)
    application = create_app()
    assert application.docs_url is None
    assert application.redoc_url is None
    assert application.openapi_url is None


def test_docs_surface_enabled_only_on_loopback(monkeypatch: pytest.MonkeyPatch) -> None:
    """`DEV_MODE=1` 且 loopback → 开启；非 loopback → 仍禁用（S4）。"""
    monkeypatch.setenv("DEV_MODE", "1")
    monkeypatch.setenv("API_HOST", "127.0.0.1")
    assert dev_mode() is True
    application = create_app()
    assert application.docs_url == "/docs"
    assert application.openapi_url == "/openapi.json"

    monkeypatch.setenv("API_HOST", "0.0.0.0")
    assert dev_mode() is False
    assert create_app().openapi_url is None


async def test_healthz_probe_without_credentials() -> None:
    """`/healthz` 豁免鉴权（ASGI 直连，不触库即 200；探针不含业务信息，S4）。"""
    application = create_app(dev=False)
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
