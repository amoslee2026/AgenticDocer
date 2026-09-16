"""M07 WebUI API（§3 M07；REQ-M07-F01..F06）——M08 前端唯一依赖的 HTTP 契约面。

装配（见 :mod:`agenticdocer.app`）：

.. code-block:: python

    from agenticdocer.webui_api import router as webui_router
    app.include_router(webui_router)

对外契约：:mod:`agenticdocer.webui_api.router`（端点在模块文档的表里）；
鉴权端点由 M10 提供（:mod:`agenticdocer.auth.router`），本包不重复实现。
"""

from __future__ import annotations

from .router import (
    CommentCreate,
    CommentStateChange,
    DiffEntry,
    DiffSummary,
    DocDiff,
    GrantCreate,
    KeyAdd,
    KeyRevoke,
    RoleInfo,
    SchemaRegister,
    StatusChange,
    TermUpsert,
    UserCreate,
    UserPatch,
    UserView,
    router,
)

__all__ = [
    "CommentCreate",
    "CommentStateChange",
    "DiffEntry",
    "DiffSummary",
    "DocDiff",
    "GrantCreate",
    "KeyAdd",
    "KeyRevoke",
    "RoleInfo",
    "SchemaRegister",
    "StatusChange",
    "TermUpsert",
    "UserCreate",
    "UserPatch",
    "UserView",
    "router",
]
