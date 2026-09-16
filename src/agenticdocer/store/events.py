"""事件表仓储（append-only，REQ-M02-F03/F04）。

`events` 只有 INSERT 路径——本模块**不提供** update/delete 方法（P2 不变量在代码层的
落地）；库层另有 §4.3 的授权口径兜底（见 `schema.privilege_statements`）。

写入侧与 `fold.apply_events` 构成载荷契约：见 `fold.py` 模块文档。
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any, Final
from uuid import UUID

from sqlalchemy import insert, select, tuple_
from sqlalchemy.ext.asyncio import AsyncSession

from agenticdocer.model import Event, NodeSnapshot, WriteContext, new_uuid7
from .errors import ValidationError
from .fold import apply_events as _apply_events
from .fold import entity_ops
from .repository import Repository
from .rows import as_uuid, build_model, now, row_to_dict
from .schema import events

__all__ = [
    "EVENT_COLUMNS",
    "EventRepository",
    "append_event",
    "changes_since",
    "fetch_events",
]

EVENT_COLUMNS: Final = tuple(events.c)
"""显式列（避免 `SELECT *` 与模型字段漂移）。"""


def _as_entity_id(entity_id: str | UUID) -> str:
    return str(entity_id)


async def append_event(
    session: AsyncSession,
    *,
    entity: str,
    entity_id: str | UUID,
    op: str,
    payload: Mapping[str, Any],
    actor: str,
    ts: datetime | None = None,
) -> Event:
    """追加一条事件（调用方负责与实体变更同事务，P2）。

    `(entity, op)` 取值域按 §3.5 表校验（DDL 层 `op` 是自由文本，无 CHECK）。
    """
    ops = entity_ops(entity)
    if op not in ops:
        raise ValidationError(
            f"op {op!r} is not valid for entity {entity!r}; expected one of {list(ops)}",
            entity=entity,
            entity_id=entity_id,
        )
    if not actor:
        raise ValidationError("event actor must be non-empty (§6：身份写入 WriteContext.actor)")
    record = {
        "event_id": new_uuid7(),
        "entity": entity,
        "entity_id": _as_entity_id(entity_id),
        "op": op,
        "payload": dict(payload),
        "actor": actor,
        "ts": ts or now(),
    }
    await session.execute(insert(events).values(**record))
    return build_model(Event, record)


async def fetch_events(
    session: AsyncSession,
    entity: str,
    entity_id: str | UUID,
    *,
    upto: datetime | None = None,
) -> list[Event]:
    """按时间重放序列（`ts, event_id` 定序：UUIDv7 时间有序，保证可判定）。"""
    entity_ops(entity)
    statement = select(*EVENT_COLUMNS).where(
        events.c.entity == entity,
        events.c.entity_id == _as_entity_id(entity_id),
    )
    if upto is not None:
        statement = statement.where(events.c.ts <= upto)
    statement = statement.order_by(events.c.ts, events.c.event_id)
    result = await session.execute(statement)
    return [build_model(Event, row_to_dict(row)) for row in result]


class EventRepository(Repository):
    """§3 M02：`replay` / `apply_events`，以及 M10 审计事件写入。"""

    async def replay(
        self,
        entity: str,
        entity_id: str | UUID,
        upto: datetime | None = None,
    ) -> list[Event]:
        """重放某实体的全部事件（`upto` 为含端上界）。"""
        async with self.db.session() as session:
            return await fetch_events(session, entity, entity_id, upto=upto)

    def apply_events(self, entity: str, events: Sequence[Event]) -> NodeSnapshot | dict[str, Any]:
        """折叠（纯函数，委托 `fold.apply_events`；§3 M02 L7）。"""
        return _apply_events(entity, events)

    async def log_auth_event(
        self,
        *,
        op: str,
        actor: str,
        payload: Mapping[str, Any],
    ) -> Event:
        """鉴权审计事件（§3.5 第 6 行：追加，不参与实体折叠；B2）。"""
        async with self.db.transaction() as session:
            return await append_event(
                session, entity="auth", entity_id=actor, op=op, payload=payload, actor=actor
            )

    async def changes_since(
        self,
        *,
        since_ts: datetime | None = None,
        since_event_id: UUID | str | None = None,
        entity: str | None = None,
        limit: int = 1000,
    ) -> list[Event]:
        """全库事件增量扫描（M-LR `change_stream` 用）：按 `(ts, event_id)` 定序，**严格晚于游标**。

        游标语义：
        - 同时给 `since_ts` + `since_event_id` → 行值比较 `(ts, event_id) > (…, …)`，
          调用方用上批最后一条事件续扫即可**不重不漏**；
        - 只给 `since_ts` → `ts > since_ts`（同一个半开区间口径）；
        - 都不给 → 从头（最早事件）开始。
        `entity` 可选过滤（如只看 `node`）。

        注（ADR-009 §4 V4）：`events` 为权威溯源、永久保留；未来超期分区 `DETACH` 到
        `events_archive` 后，本方法与 `replay` 都应改走 `events_all` 视图——归档落地时在此
        统一切换（口径单点），调用方无需改。
        """
        if limit < 1:
            raise ValidationError(f"limit must be >= 1, got {limit}")
        statement = select(*EVENT_COLUMNS)
        if since_ts is not None:
            if since_event_id is not None:
                statement = statement.where(
                    tuple_(events.c.ts, events.c.event_id)
                    > (since_ts, as_uuid(since_event_id))
                )
            else:
                statement = statement.where(events.c.ts > since_ts)
        if entity is not None:
            entity_ops(entity)
            statement = statement.where(events.c.entity == entity)
        statement = statement.order_by(events.c.ts, events.c.event_id).limit(limit)
        async with self.db.session() as session:
            rows = (await session.execute(statement)).all()
        return [build_model(Event, row_to_dict(row)) for row in rows]
