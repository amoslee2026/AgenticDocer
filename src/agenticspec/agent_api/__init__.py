"""M06 Agent 接口（§3 M06；REQ-M06-F01/F02）——面向 coding agent 的结构化读写 HTTP 面。

装配（见 :mod:`agenticspec.app`）：

.. code-block:: python

    from agenticspec.agent_api import router as agent_router
    app.include_router(agent_router)

对外契约：:mod:`agenticspec.agent_api.router`（端点在模块文档的表里）；
共享依赖项与写入门：:mod:`agenticspec.agent_api.deps`、`router.validate_write`。
"""

from __future__ import annotations

from .deps import (
    AdminAuth,
    AuthDep,
    DatabaseDep,
    ErrorResponse,
    ReadAuth,
    ReviewAuth,
    StorageDep,
    ValidationRejected,
    WriteAuth,
    authorize_doc,
    request_database,
    request_storage,
)
from .router import NodeUpsert, RefWrite, RenderOutput, SectionDTO, router, validate_write

__all__ = [
    "AdminAuth",
    "DatabaseDep",
    "ErrorResponse",
    "NodeUpsert",
    "ReadAuth",
    "RefWrite",
    "RenderOutput",
    "SectionDTO",
    "ReviewAuth",
    "StorageDep",
    "ValidationRejected",
    "WriteAuth",
    "authorize_doc",
    "request_database",
    "request_storage",
    "router",
    "validate_write",
]
