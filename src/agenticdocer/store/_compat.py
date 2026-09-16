"""M01 领域模型契约的兼容绑定层（临时）。

M02 只依赖 §3.0「公共类型定义」的**公共契约**。本模块在 `agenticdocer.model`
可导入时直接绑定其类型；不可导入时（M01 并行开发中）绑定下方的最小本地实现，
使存储层可独立开发与测试。

落地后收敛：M01 就绪后，本文件的 fallback 分支成为死代码，
`MISSING_FROM_MODEL_LAYER` 会列出未被 M01 提供的符号；届时删除 fallback 并把各
模块的 `from ._compat import ...` 改为 `from agenticdocer.model import ...`。
"""

from __future__ import annotations

import os
import time
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

__all__ = [
    "UUID7",
    "MODEL_LAYER_READY",
    "MISSING_FROM_MODEL_LAYER",
    "Asset",
    "Comment",
    "CommentState",
    "Doc",
    "DocIn",
    "DocStatus",
    "Event",
    "Node",
    "NodeIn",
    "NodeSnapshot",
    "Ref",
    "RefKind",
    "WriteContext",
    "new_uuid7",
]

UUID7 = UUID
RefKind = Literal["traces_to", "see_also", "composes_from", "source_ref"]
DocType = Literal["standard", "lang", "tool-manual", "product", "safety"]
DocStatus = Literal["draft", "reviewed", "approved"]
CommentState = Literal["open", "resolved", "orphaned"]

# ---------------------------------------------------------------- 本地最小实现

_MODEL_CONFIG = ConfigDict(
    alias_generator=to_camel,
    populate_by_name=True,
    extra="forbid",
)


class _WriteContext(BaseModel):
    """A3：一切写入的身份与来源。"""

    model_config = _MODEL_CONFIG

    actor: str
    source: Literal["agent", "webui", "cli", "importer", "system"]


class _NodeIn(BaseModel):
    model_config = _MODEL_CONFIG

    node_id: UUID | None = None
    doc_id: str
    atom_type: str
    format: Literal["md", "html", "text"] = "md"
    ordinal: int
    parent_node_id: UUID | None = None
    level: int | None = None
    anchor: str
    content: dict


class _Node(_NodeIn):
    node_id: UUID
    status: Literal["active", "deleted"] = "active"
    version: int = 1
    created_at: datetime
    updated_at: datetime


class _Event(BaseModel):
    model_config = _MODEL_CONFIG

    event_id: UUID
    entity: Literal["doc", "node", "ref", "comment", "schema", "auth"]
    entity_id: str
    # DDL 为自由文本（§4 `op text NOT NULL`，无 CHECK）；取值域见 §3.5。
    # §3.0 的 6 值 Literal 与 §3.5 的 auth 审计 op 冲突，此处以 DDL 为准。
    op: str
    payload: dict
    actor: str
    ts: datetime


class _NodeSnapshot(BaseModel):
    model_config = _MODEL_CONFIG

    node: _Node | None = None
    history: list[_Event] = []


class _DocIn(BaseModel):
    model_config = _MODEL_CONFIG

    doc_id: str
    doc_type: str
    title: str
    meta: dict = {}
    source_ref: str | None = None


class _Doc(_DocIn):
    status: DocStatus = "draft"
    version: int = 1
    created_at: datetime
    updated_at: datetime


class _Comment(BaseModel):
    model_config = _MODEL_CONFIG

    comment_id: UUID
    node_id: UUID
    target_event_id: UUID | None = None
    body: str
    state: CommentState = "open"
    author: str
    version: int = 1
    ts: datetime


class _Ref(BaseModel):
    model_config = _MODEL_CONFIG

    ref_id: UUID
    src_node_id: UUID
    dst_doc_id: str
    dst_node_id: UUID | None = None
    kind: RefKind


class _Asset(BaseModel):
    model_config = _MODEL_CONFIG

    asset_id: str
    mime: str
    bytes: int
    origin: str | None = None
    path: str


def _local_new_uuid7() -> UUID:
    """UUIDv7（RFC 9562）：48 位毫秒时间戳 + 版本/变体位 + 74 位随机，时间有序。"""
    ms = time.time_ns() // 1_000_000
    rand = int.from_bytes(os.urandom(10), "big")
    value = (ms & 0xFFFF_FFFF_FFFF) << 80
    value |= 0x7 << 76
    value |= ((rand >> 68) & 0xFFF) << 64
    value |= 0b10 << 62
    value |= rand & ((1 << 62) - 1)
    return UUID(int=value)


# ------------------------------------------------------------- 契约绑定（M01 优先）

_MODEL: Any = None
_UUID7_MOD: Any = None
try:  # pragma: no cover - 分支取决于 M01 是否已交付
    import agenticdocer.model as _imported_model
    import agenticdocer.model.uuid7 as _imported_uuid7

    _MODEL = _imported_model
    _UUID7_MOD = _imported_uuid7
except Exception:  # noqa: BLE001 - M01 未就绪时退回本地实现
    _MODEL = None
    _UUID7_MOD = None

MODEL_LAYER_READY = _MODEL is not None
MISSING_FROM_MODEL_LAYER: tuple[str, ...] = ()
_BINDINGS: list[str] = []


def _bind(name: str, local: Any) -> Any:
    if _MODEL is not None and hasattr(_MODEL, name):
        return getattr(_MODEL, name)
    if _MODEL is not None:
        _BINDINGS.append(name)
    return local


WriteContext = _bind("WriteContext", _WriteContext)
NodeIn = _bind("NodeIn", _NodeIn)
Node = _bind("Node", _Node)
Event = _bind("Event", _Event)
NodeSnapshot = _bind("NodeSnapshot", _NodeSnapshot)
DocIn = _bind("DocIn", _DocIn)
Doc = _bind("Doc", _Doc)
Comment = _bind("Comment", _Comment)
Ref = _bind("Ref", _Ref)
Asset = _bind("Asset", _Asset)

if _UUID7_MOD is not None and hasattr(_UUID7_MOD, "new_uuid7"):
    new_uuid7 = _UUID7_MOD.new_uuid7
else:
    new_uuid7 = _local_new_uuid7
    if _MODEL is not None:
        _BINDINGS.append("new_uuid7")

MISSING_FROM_MODEL_LAYER = tuple(_BINDINGS)

UTC = timezone.utc
