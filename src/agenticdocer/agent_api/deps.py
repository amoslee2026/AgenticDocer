"""M06/M07 共享依赖项（§3 M06/M07；S4/S5/S14）。

| 依赖项 | 语义 |
|---|---|
| `request_storage` / `request_database` | 应用注入（`app.state.storage` / `app.state.db`）；缺省回落进程单例——与 M10 的 `auth_database` 取**同一** `Database` |
| `AuthDep` | 仅要求凭据（`require_auth`）：无凭据 401（**S4：豁免清单外 fail-closed**） |
| `ReadAuth` / `WriteAuth` / `ReviewAuth` / `AdminAuth` | 角色权限门槛（`require_permission`，四角色硬上限，S5） |
| `authorize_doc` | **文档级授权**：读 `docs` 行取 `doc_type` 后按 `DocTarget` /doc_type 收窄判定（S5：grant 只收窄、不扩权） |

**身份纪律（S14）**：M06/M07 **不读 `X-Actor`**——`WriteContext` 由 `auth.write_context(ctx)`
从验签结果/会话行派生（`actor` = 验签所得 `user_id`，`source` = 凭据类型）：

.. code-block:: python

    from agenticdocer.auth import write_context
    from agenticdocer.agent_api.deps import WriteAuth, StorageDep

    @router.post("/nodes")
    async def post_node(payload: NodeUpsert, context: WriteAuth, storage: StorageDep) -> Node:
        return await storage.upsert_node(node, payload.expected_version, write_context(context))
"""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import Depends, Request

from agenticdocer.auth import (
    AuthContext,
    authorize_user,
    require_auth,
    require_permission,
)
from agenticdocer.auth.rbac import MANAGE_USERS
from agenticdocer.observability import get_logger
from agenticdocer.model import Doc, DocTarget, Model, Violation
from agenticdocer.store import (
    Database,
    Storage,
    ValidationError,
    get_database,
    get_storage,
)

__all__ = [
    "AdminAuth",
    "AuthDep",
    "DatabaseDep",
    "ErrorResponse",
    "ReadAuth",
    "ReviewAuth",
    "StorageDep",
    "ValidationRejected",
    "WriteAuth",
    "authorize_doc",
    "request_database",
    "request_storage",
]


def request_storage(request: Request) -> Storage:
    """应用注入的 `Storage`（`app.state.storage`）；无则回落进程单例装配。"""
    injected = getattr(request.app.state, "storage", None)
    return injected if isinstance(injected, Storage) else get_storage()


def request_database(request: Request) -> Database:
    """应用注入的 `Database`（`app.state.db`）；无则回落进程单例（`DATABASE_URL`）。"""
    injected = getattr(request.app.state, "db", None)
    return injected if isinstance(injected, Database) else get_database()



StorageDep = Annotated[Storage, Depends(request_storage)]
DatabaseDep = Annotated[Database, Depends(request_database)]

AuthDep = Annotated[AuthContext, Depends(require_auth)]
ReadAuth = Annotated[AuthContext, Depends(require_permission("read"))]
WriteAuth = Annotated[AuthContext, Depends(require_permission("write"))]
ReviewAuth = Annotated[AuthContext, Depends(require_permission("review"))]
AdminAuth = Annotated[AuthContext, Depends(require_permission(MANAGE_USERS))]


class ValidationRejected(ValidationError):
    """写入门失败（REQ-M06-F02）：携带**结构化违规清单**供 agent 自修复后重试。

    存储层的 `ValidationError` 只有 message；HTTP 适配层需要 `Violation` 清单
    （`rule_id`/`path`/`message`/`fix_hint`）——由 `app.py` 的异常处理器序列化为
    ``422 {"error": "validation", "violations": [...]}``。
    """

    def __init__(
        self,
        violations: list[Violation],
        *,
        message: str | None = None,
        entity: str | None = None,
        entity_id: Any = None,
    ) -> None:
        super().__init__(
            message or f"{len(violations)} 项校验失败（见 violations）",
            entity=entity,
            entity_id=entity_id,
        )
        self.violations = violations


async def authorize_doc(
    context: AuthContext,
    perm: str,
    doc_id: str,
    *,
    storage: Storage,
    db: Database | None = None,
) -> Doc:
    """文档级授权（S5）：读 `docs` 行（不存在 → 404）后按角色 + grant 收窄判定。

    返回该 `Doc`，调用方复用它取 `doc_type`（避免二次点查）。
    """
    doc = await storage.get_doc(doc_id)
    await authorize_user(
        context.user,
        perm,
        DocTarget(value=doc.doc_id),
        db=db,
        doc_type=doc.doc_type,
    )
    return doc


class ErrorResponse(Model):
    """统一错误响应体（§6 错误映射；`app.py` 的异常处理器按此形状序列化）。

    - 401/403/404/409：`error` + `message`（+ 可选的 `code`/`entity`/`entityId`）；
    - 422：额外给出 `violations[]`（REQ-M06-F02：agent 据 `fixHint` 修正后重试）；
    - `code` 为 M12 的 `DTO_*` 业务错误码（如 `DTO_ANCHOR_CONFLICT`）。

    本模型经 `FastAPI(responses=…)` 挂到各错误状态码（见 `app.create_app`），使 M08/M11
    客户端能从 OpenAPI 取到**类型化**的错误契约，而非仅文档描述。
    """

    error: str
    message: str
    code: str | None = None
    entity: str | None = None
    entity_id: str | None = None
    violations: list[Violation] = []
