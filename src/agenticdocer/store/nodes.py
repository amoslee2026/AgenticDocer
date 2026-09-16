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

from agenticdocer.model import Node, NodeIn, WriteContext, new_uuid7
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

    async def get_subtree(
        self,
        root_node_id: UUID | str,
        *,
        doc_id: str | None = None,
        include_deleted: bool = False,
    ) -> list[Node]:
        """取 `root_node_id` 及其**全部后代**（`ordinal` 序；默认只 `status='active'`）。

        实现：沿 `parent_node_id` 的递归 CTE（`idx_nodes_parent`）。与 `get_doc_nodes`
        的排序/过滤语义**逐字一致**（P5 口径唯一）——故 `render_section` 可用它替代
        「取全档再内存过滤」，使章节渲染从 O(全文) 回到 O(章节)。

        `doc_id` 可选：`nodes` 按 `doc_id` HASH 分区，给出即可把整棵子树的递归裁剪到
        单一分区（ADR-009 V16 的同一思路）。

        语义约定（与 `get_doc_nodes` 对齐，非「按祖先状态剪枝」）：递归**遍历完整父子链**，
        `status` 过滤只作用于**结果集**。因此软删的中间节点不会砍掉其下仍 active 的后代；
        反之若 `root` 本身已软删，默认结果不含它、但含其 active 后代（`include_deleted=True`
        则一并返回）。理由：`get_doc_nodes` 也只按 status 过滤、不看祖先状态，两处口径必须一致。
        """
        root_id = as_uuid(root_node_id)
        seed = select(nodes.c.node_id, nodes.c.parent_node_id).where(nodes.c.node_id == root_id)
        if doc_id is not None:
            seed = seed.where(nodes.c.doc_id == doc_id)
        subtree = seed.cte("subtree", recursive=True)
        child = select(nodes.c.node_id, nodes.c.parent_node_id).join(
            subtree, nodes.c.parent_node_id == subtree.c.node_id
        )
        if doc_id is not None:
            # 递归项带上分区键 → 整棵子树只扫一个分区（ADR-009 V16 的同一思路）
            child = child.where(nodes.c.doc_id == doc_id)
        subtree = subtree.union_all(child)
        statement = select(*NODE_COLUMNS).where(nodes.c.node_id.in_(select(subtree.c.node_id)))
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
            # 仅当父节点引用变化时才做外键降级后的应用层校验（ADR-009），避免热路径多一次查询
            if incoming.get("parent_node_id") != existing["parent_node_id"]:
                await self._assert_parent_exists(session, incoming.get("parent_node_id"))
            candidate = {**existing, **incoming}
            content_deltas = field_deltas(existing, candidate)
            if not content_deltas:
                return build_model(Node, existing)
            version = existing["version"] + 1
            record = {**candidate, "version": version, "updated_at": timestamp}
            # 事件载荷覆盖全部变化（含 version/updated_at），使重放结果与当前行逐字段一致
            # （M09B `events_consistency` 判据）；SQL 只写真正变化的列。
            deltas = field_deltas(existing, record)
            values = {field: record[field] for field in deltas}
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
            deleted = {
                **before,
                "status": "deleted",
                "version": before["version"] + 1,
                "updated_at": timestamp,
            }
            await session.execute(
                update(nodes)
                .where(nodes.c.node_id == before["node_id"], nodes.c.doc_id == before["doc_id"])
                .values(status="deleted", version=deleted["version"], updated_at=timestamp)
            )
            # §3.5「delete 含 before 全量」：逐字段给出 before；after 为删除后的行值，
            # 使重放与当前行一致（内容字段 after == before，等价于 before 全量）。
            await append_event(
                session,
                entity="node",
                entity_id=before["node_id"],
                op="delete",
                payload=field_deltas(before, deleted, include_unchanged=True),
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
