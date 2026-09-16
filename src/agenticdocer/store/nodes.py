"""节点仓储（REQ-M02-F01 乐观锁、REQ-M02-F04 事件同事务、A2 软删）。

不变量：

- 一切写操作在 `Database.transaction()` 内完成：**事件行 + 实体变更同事务**（P2）；
- 更新/删除携带 `expected_version`，不匹配 → `ConflictError`（409）；
- 删除是软删（`status='deleted'` + `version+1`），同事务 `orphan_comments`；
- `get_node`/`get_doc_nodes` 默认过滤 `status='active'`（A2）。

ADR-009 外键降级：`parent_node_id` 无 DB 外键，故写入时由应用层校验父节点存在
（`_assert_parent_exists`）。`doc_id` 的外键**保留**（docs 不分区），由 DB 兜底。
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Final
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ._compat import Node, NodeIn, WriteContext, new_uuid7
from .comments import orphan_comments_in
from .errors import ConflictError, NotFoundError, ValidationError, translate_integrity_error
from .events import append_event
from .repository import Repository
from .rows import as_uuid, build_model, field_deltas, now, row_to_dict
from .schema import nodes

__all__ = ["NODE_COLUMNS", "NodeRepository", "fetch_node", "node_values"]

NODE_COLUMNS: Final = tuple(column for column in nodes.c if column.name != "text_fts")
"""显式列：`text_fts` 是生成列，不在模型里（也无需回传）。"""

_MUTABLE_FIELDS: Final = (
    "doc_id",
    "atom_type",
    "format",
    "ordinal",
    "parent_node_id",
    "level",
    "anchor",
    "content",
)


def node_values(
    node_id: UUID,
    incoming: dict[str, Any],
    *,
    created_at: Any,
    status: str = "active",
    version: int = 1,
) -> dict[str, Any]:
    """节点行值（DB 列名口径）。"""
    return {
        **{field: incoming.get(field) for field in _MUTABLE_FIELDS},
        "node_id": node_id,
        "status": status,
        "version": version,
        "created_at": created_at,
        "updated_at": created_at,
    }


async def fetch_node(
    session: AsyncSession,
    node_id: UUID | str,
    *,
    doc_id: str | None = None,
    include_deleted: bool = False,
) -> dict[str, Any] | None:
    """取节点行（列名字典）；`doc_id` 提供分区裁剪（ADR-009 V16）。"""
    statement = select(*NODE_COLUMNS).where(nodes.c.node_id == as_uuid(node_id))
    if doc_id is not None:
        statement = statement.where(nodes.c.doc_id == doc_id)
    if not include_deleted:
        statement = statement.where(nodes.c.status == "active")
    row = (await session.execute(statement)).first()
    return row_to_dict(row) if row is not None else None


class NodeRepository(Repository):
    """§3 M02 的节点读写面。"""

    async def get_node(
        self,
        node_id: UUID | str,
        *,
        doc_id: str | None = None,
        include_deleted: bool = False,
    ) -> Node:
        """单节点读取（默认 `status='active'`，A2）。

        `doc_id` 可选：`nodes` 按 `doc_id` HASH 分区，传 `doc_id` 可将点查裁剪到单一
        分区（ADR-009 V16；`node_id` 单列点查需 Append 全部 64 分区）。
        """
        async with self.db.session() as session:
            row = await fetch_node(
                session, node_id, doc_id=doc_id, include_deleted=include_deleted
            )
        if row is None:
            raise NotFoundError(f"node {node_id} not found", entity="node", entity_id=node_id)
        return build_model(Node, row)

    async def get_doc_nodes(self, doc_id: str, include_deleted: bool = False) -> list[Node]:
        """文档全部节点（`ordinal` 序；默认过滤软删）。"""
        statement = select(*NODE_COLUMNS).where(nodes.c.doc_id == doc_id)
        if not include_deleted:
            statement = statement.where(nodes.c.status == "active")
        statement = statement.order_by(nodes.c.ordinal, nodes.c.node_id)
        async with self.db.session() as session:
            rows = (await session.execute(statement)).all()
        return [build_model(Node, row_to_dict(row)) for row in rows]

    async def upsert_node(
        self,
        node: NodeIn,
        expected_version: int | None,
        ctx: WriteContext,
    ) -> Node:
        """创建或更新节点（`node_id` 缺省则新建）。

        - `expected_version is None`：不校验版本；`node_id` 不存在则创建；
        - `expected_version` 给定：行必须存在且版本相等，否则 `ConflictError`；
        - 无字段变化时按幂等处理：不写事件、不增版本，直接返回当前行。
        """
        incoming = node.model_dump()
        node_id = incoming.pop("node_id", None)
        async with self.db.transaction() as session:
            existing = (
                await fetch_node(session, node_id, include_deleted=True)
                if node_id is not None
                else None
            )
            timestamp = now()
            if existing is None:
                if expected_version is not None:
                    raise ConflictError(
                        f"node {node_id} does not exist but expected_version={expected_version} was given",
                        entity="node",
                        entity_id=node_id,
                    )
                new_id = node_id or new_uuid7()
                await self._assert_parent_exists(session, incoming.get("parent_node_id"))
                record = node_values(new_id, incoming, created_at=timestamp)
                try:
                    await session.execute(insert(nodes).values(**record))
                except IntegrityError as exc:
                    raise translate_integrity_error(exc, entity="node", entity_id=new_id) from exc
                await append_event(
                    session,
                    entity="node",
                    entity_id=new_id,
                    op="create",
                    payload=field_deltas({}, record, include_unchanged=True),
                    actor=ctx.actor,
                    ts=timestamp,
                )
                return build_model(Node, record)

            if existing["status"] == "deleted":
                raise NotFoundError(
                    f"node {node_id} is deleted; soft-deleted nodes are not updatable (A2)",
                    entity="node",
                    entity_id=node_id,
                )
            if expected_version is not None and expected_version != existing["version"]:
                raise ConflictError(
                    f"node {node_id} version mismatch: expected {expected_version}, "
                    f"stored {existing['version']}",
                    entity="node",
                    entity_id=node_id,
                )
            if incoming["doc_id"] != existing["doc_id"]:
                raise ValidationError(
                    f"node {node_id}: doc_id is the nodes partition key "
                    f"({existing['doc_id']} → {incoming['doc_id']} unsupported)",
                    entity="node",
                    entity_id=node_id,
                )
            await self._assert_parent_exists(session, incoming.get("parent_node_id"))
            candidate = {**existing, **incoming}
            deltas = field_deltas(existing, candidate)
            if not deltas:
                return build_model(Node, existing)
            version = existing["version"] + 1
            record = {**candidate, "version": version, "updated_at": timestamp}
            values = {field: record[field] for field in deltas}
            values["version"] = version
            values["updated_at"] = timestamp
            try:
                await session.execute(
                    update(nodes)
                    .where(nodes.c.node_id == existing["node_id"], nodes.c.doc_id == existing["doc_id"])
                    .values(**values)
                )
            except IntegrityError as exc:
                raise translate_integrity_error(exc, entity="node", entity_id=node_id) from exc
            await append_event(
                session,
                entity="node",
                entity_id=existing["node_id"],
                op="update",
                payload=deltas,
                actor=ctx.actor,
                ts=timestamp,
            )
            return build_model(Node, record)

    async def delete_node(
        self,
        node_id: UUID | str,
        expected_version: int,
        ctx: WriteContext,
    ) -> None:
        """软删节点（A2）：`status='deleted'`、`version+1`、写 delete 事件（before 全量），
        同事务把该节点的 open 批注置 `orphaned`。
        """
        async with self.db.transaction() as session:
            before = await fetch_node(session, node_id, include_deleted=True)
            if before is None or before["status"] == "deleted":
                raise NotFoundError(f"node {node_id} not found", entity="node", entity_id=node_id)
            if before["version"] != expected_version:
                raise ConflictError(
                    f"node {node_id} version mismatch: expected {expected_version}, "
                    f"stored {before['version']}",
                    entity="node",
                    entity_id=node_id,
                )
            timestamp = now()
            await session.execute(
                update(nodes)
                .where(nodes.c.node_id == before["node_id"], nodes.c.doc_id == before["doc_id"])
                .values(status="deleted", version=before["version"] + 1, updated_at=timestamp)
            )
            await append_event(
                session,
                entity="node",
                entity_id=before["node_id"],
                op="delete",
                payload=field_deltas(before, {}, include_unchanged=True),
                actor=ctx.actor,
                ts=timestamp,
            )
            await orphan_comments_in(session, before["node_id"], ctx, ts=timestamp)

    async def list_nodes_for_docs(
        self, doc_ids: Sequence[str], include_deleted: bool = False
    ) -> list[Node]:
        """多文档节点（M09B 质量门 / M-LR 导出用）。"""
        if not doc_ids:
            return []
        statement = select(*NODE_COLUMNS).where(nodes.c.doc_id.in_(tuple(doc_ids)))
        if not include_deleted:
            statement = statement.where(nodes.c.status == "active")
        statement = statement.order_by(nodes.c.doc_id, nodes.c.ordinal, nodes.c.node_id)
        async with self.db.session() as session:
            rows = (await session.execute(statement)).all()
        return [build_model(Node, row_to_dict(row)) for row in rows]

    async def _assert_parent_exists(self, session: AsyncSession, parent_node_id: Any) -> None:
        """ADR-009：`parent_node_id` 外键降级 → 应用层校验（M09B 亦有孤儿 parent 巡检）。"""
        if parent_node_id is None:
            return
        row = (
            await session.execute(
                select(nodes.c.node_id, nodes.c.status).where(
                    nodes.c.node_id == as_uuid(parent_node_id)
                )
            )
        ).first()
        if row is None:
            raise ValidationError(
                f"parent_node_id {parent_node_id} does not exist (ADR-009：外键已降级为应用层校验)",
                entity="node",
                entity_id=parent_node_id,
            )
