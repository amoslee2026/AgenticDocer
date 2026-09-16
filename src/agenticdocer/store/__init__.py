"""M02 存储层（§3 M02 契约）。

- `Storage`：节点/文档/引用/批注/资产/事件的完整读写面；
- 写路径统一要求 `WriteContext`，并在单事务内落「事件 + 实体」（P2）；
- `events` append-only（无 update/delete 方法，库层授权兜底）；
- 模型类型经 `_compat` 绑定 M01（`agenticdocer.model`），M01 未就绪时用契约等价的
  最小实现——**M01 落地后 `_compat` 的 fallback 分支即死代码**。
"""

from __future__ import annotations

from agenticdocer.model import (
    UUID7,
    Asset,
    Comment,
    CommentState,
    Doc,
    DocIn,
    DocStatus,
    Event,
    MODEL_LAYER_READY,
    Node,
    NodeIn,
    NodeSnapshot,
    Ref,
    RefKind,
    WriteContext,
    new_uuid7,
)
from .assets import ASSET_REF_PATTERN, AssetRepository, asset_store_dir
from .comments import CommentRepository
from .db import Database, database_url, get_database
from .docs import DocRepository
from .errors import (
    ConflictError,
    ForbiddenError,
    NotFoundError,
    StoreError,
    ValidationError,
    translate_integrity_error,
)
from .events import EventRepository, append_event, fetch_events
from .fold import ENTITY_OPS, apply_events
from .nodes import NodeRepository
from .refs import RefRepository
from .rows import as_uuid, build_model, field_deltas, jsonable, now
from .storage import Storage, get_storage

__all__ = [
    "ASSET_REF_PATTERN",
    "ENTITY_OPS",
    "MODEL_LAYER_READY",
    "UUID7",
    "Asset",
    "AssetRepository",
    "Comment",
    "CommentRepository",
    "CommentState",
    "ConflictError",
    "Database",
    "Doc",
    "DocIn",
    "DocRepository",
    "DocStatus",
    "Event",
    "EventRepository",
    "ForbiddenError",
    "Node",
    "NodeIn",
    "NodeRepository",
    "NodeSnapshot",
    "NotFoundError",
    "Ref",
    "RefKind",
    "RefRepository",
    "Storage",
    "StoreError",
    "ValidationError",
    "WriteContext",
    "append_event",
    "apply_events",
    "as_uuid",
    "asset_store_dir",
    "build_model",
    "database_url",
    "fetch_events",
    "field_deltas",
    "get_database",
    "get_storage",
    "jsonable",
    "new_uuid7",
    "now",
    "translate_integrity_error",
]
