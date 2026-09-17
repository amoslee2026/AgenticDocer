"""批注仓储（REQ-M02-F05：open/resolved/orphaned；A4 乐观锁）。

`comments.node_id` / `target_event_id` 外键按 ADR-009 降级，故节点存在性由应用层校验；
节点软删时批注**不级联删除**，而是置 `orphaned` 并保留（A2）——同事务由
`nodes.delete_node` 调用 `orphan_comments_in`。
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from typing import Any, Final
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from agenticspec.model import Comment, CommentState, WriteContext, new_uuid7
from .errors import ConflictError, NotFoundError, ValidationError
from .events import append_event
from .repository import Repository
from .rows import as_uuid, build_model, field_deltas, now, row_to_dict
from .schema import comments, events, nodes

__all__ = ["COMMENT_COLUMNS", "CommentRepository", "fetch_comment", "orphan_comments_in"]

COMMENT_COLUMNS: Final = tuple(comments.c)

_STATES: Final = ("open", "resolved", "orphaned")
_SYSTEM_CTX: Final = WriteContext(actor="system", source="system")
"""孤立化由节点删除驱动、无调用方身份：`actor`/`source` 记为 `system`（§6 A3 取值规则）。"""


async def fetch_comment(session: AsyncSession, comment_id: UUID | str) -> dict[str, Any] | None:
    row = (
        await session.execute(
            select(*COMMENT_COLUMNS).where(comments.c.comment_id == as_uuid(comment_id))
        )
    ).first()
    return row_to_dict(row) if row is not None else None


async def _require_active_node(session: AsyncSession, node_id: UUID | str) -> dict[str, Any]:
    """ADR-009：`comments.node_id` 外键降级 → 应用层校验节点存在且未软删。"""
    row = (
        await session.execute(
            select(nodes.c.node_id, nodes.c.version, nodes.c.status).where(
                nodes.c.node_id == as_uuid(node_id)
            )
        )
    ).first()
    if row is None or row.status != "active":
        raise NotFoundError(
            f"node {node_id} not found or deleted; comments anchor to live nodes (A2)",
            entity="node",
            entity_id=node_id,
        )
    return row_to_dict(row)


async def _latest_node_event_id(session: AsyncSession, node_id: UUID | str) -> UUID | None:
    """节点最近一条事件的 id —— 批注锚点（REQ-M02-F05「批注创建锚定 target_event_id」）。"""
    return (
        await session.execute(
            select(events.c.event_id)
            .where(events.c.entity == "node", events.c.entity_id == str(node_id))
            .order_by(events.c.ts.desc(), events.c.event_id.desc())
            .limit(1)
        )
    ).scalar_one_or_none()


async def orphan_comments_in(
    session: AsyncSession,
    node_id: UUID | str,
    ctx: WriteContext,
    *,
    ts: datetime | None = None,
) -> int:
    """把节点的 `open` 批注置 `orphaned`（同事务；返回影响条数）。

    模块级函数：`nodes.delete_node` 在自己的事务内直接调用，不新开事务（REQ-M02-F04）。
    """
    node_uuid = as_uuid(node_id)
    rows = (
        await session.execute(
            select(*COMMENT_COLUMNS).where(
                comments.c.node_id == node_uuid, comments.c.state == "open"
            )
        )
    ).all()
    timestamp = ts or now()
    for row in rows:
        before = row_to_dict(row)
        # 状态变更同样走乐观锁版本（A4）：orphaned 是可观测的状态迁移，须 bump version
        updated = {**before, "state": "orphaned", "version": before["version"] + 1}
        await session.execute(
            update(comments)
            .where(comments.c.comment_id == before["comment_id"])
            .values(state="orphaned", version=updated["version"])
        )
        await append_event(
            session,
            entity="comment",
            entity_id=before["comment_id"],
            op="update",
            payload=field_deltas(before, updated),
            actor=ctx.actor,
            ts=timestamp,
        )
    return len(rows)


class CommentRepository(Repository):
    """§3 M02 的批注读写面。"""

    async def create_comment(
        self,
        node_id: UUID | str,
        body: str,
        expected_version: int | None,
        ctx: WriteContext,
    ) -> Comment:
        """新建批注。

        `expected_version` 是**被批注节点**的版本：给定且与当前不符 → `ConflictError`
        （评审者读到的是旧内容）。`target_event_id` 取该节点最近事件，锚定评审时点。
        """
        if not body:
            raise ValidationError("comment body must be non-empty", entity="comment")
        async with self.db.transaction() as session:
            node = await _require_active_node(session, node_id)
            if expected_version is not None and expected_version != node["version"]:
                raise ConflictError(
                    f"node {node_id} version mismatch: expected {expected_version}, "
                    f"stored {node['version']}",
                    entity="node",
                    entity_id=node_id,
                )
            timestamp = now()
            record = {
                "comment_id": new_uuid7(),
                "node_id": node["node_id"],
                "target_event_id": await _latest_node_event_id(session, node["node_id"]),
                "body": body,
                "state": "open",
                "author": ctx.actor,
                "version": 1,
                "ts": timestamp,
            }
            await session.execute(insert(comments).values(**record))
            await append_event(
                session,
                entity="comment",
                entity_id=record["comment_id"],
                op="create",
                payload=field_deltas({}, record, include_unchanged=True),
                actor=ctx.actor,
                ts=timestamp,
            )
            return build_model(Comment, record)

    async def update_comment_state(
        self,
        comment_id: UUID | str,
        state: CommentState,
        expected_version: int,
        ctx: WriteContext,
    ) -> Comment:
        """流转批注状态（A4 乐观锁）。状态未变时幂等返回，不写事件。"""
        if state not in _STATES:
            raise ValidationError(
                f"unknown comment state {state!r}; expected one of {list(_STATES)}",
                entity="comment",
                entity_id=comment_id,
            )
        async with self.db.transaction() as session:
            before = await fetch_comment(session, comment_id)
            if before is None:
                raise NotFoundError(
                    f"comment {comment_id} not found", entity="comment", entity_id=comment_id
                )
            if before["version"] != expected_version:
                raise ConflictError(
                    f"comment {comment_id} version mismatch: expected {expected_version}, "
                    f"stored {before['version']}",
                    entity="comment",
                    entity_id=comment_id,
                )
            if before["state"] == state:
                return build_model(Comment, before)
            timestamp = now()
            updated = {**before, "state": state, "version": before["version"] + 1}
            await session.execute(
                update(comments)
                .where(comments.c.comment_id == before["comment_id"])
                .values(state=state, version=updated["version"])
            )
            await append_event(
                session,
                entity="comment",
                entity_id=before["comment_id"],
                op="update",
                payload=field_deltas(before, updated),
                actor=ctx.actor,
                ts=timestamp,
            )
            return build_model(Comment, updated)

    async def orphan_comments(self, node_id: UUID | str) -> None:
        """独立调用入口（`nodes.delete_node` 走同事务的内部函数）。

        无 `ctx` 参数（§3 M02 契约签名如此）：孤立化由节点删除驱动而非用户操作，
        事件 actor 记为 `system`/`source=system`。
        """
        async with self.db.transaction() as session:
            await orphan_comments_in(session, node_id, _SYSTEM_CTX)

    async def get_comment(self, comment_id: UUID | str) -> Comment:
        async with self.db.session() as session:
            row = await fetch_comment(session, comment_id)
        if row is None:
            raise NotFoundError(
                f"comment {comment_id} not found", entity="comment", entity_id=comment_id
            )
        return build_model(Comment, row)

    async def list_comments(
        self,
        node_id: UUID | str,
        states: Sequence[CommentState] | None = None,
    ) -> list[Comment]:
        """节点批注列表（默认全部状态，按创建时间序）。"""
        statement = select(*COMMENT_COLUMNS).where(comments.c.node_id == as_uuid(node_id))
        if states is not None:
            statement = statement.where(comments.c.state.in_(tuple(states)))
        statement = statement.order_by(comments.c.ts, comments.c.comment_id)
        async with self.db.session() as session:
            rows = (await session.execute(statement)).all()
        return [build_model(Comment, row_to_dict(row)) for row in rows]
