"""引用边仓储（REQ-M02-F02：增删各写一条 ref 事件，§3.5 扁平载荷 `{src, dst_doc, dst_node, kind}`）。

ADR-009 外键降级：`refs.src_node_id` / `dst_node_id` 无 DB 外键。
- `src` 由应用层校验（引用必须出自**存活**节点）；
- `dst` **不校验**：文档级引用 `dst_node_id IS NULL`、外部叶引用 `dst_doc_id='EXT:<uri>'`
  合法，悬空目标由 M09B `broken_refs` 巡检报告——这正是外键降级后的兜底口径。
"""

from __future__ import annotations

from typing import Any, Final
from uuid import UUID

from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ._compat import Ref, RefKind, WriteContext, new_uuid7
from .errors import NotFoundError, ValidationError, translate_integrity_error
from .events import append_event
from .repository import Repository
from .rows import as_uuid, build_model, jsonable, now, row_to_dict
from .schema import nodes, refs

__all__ = ["REF_COLUMNS", "REF_KINDS", "RefRepository"]

REF_COLUMNS: Final = tuple(refs.c)
REF_KINDS: Final = ("traces_to", "see_also", "composes_from", "source_ref")


def _check_kind(kind: str) -> None:
    if kind not in REF_KINDS:
        raise ValidationError(
            f"unknown ref kind {kind!r}; expected one of {list(REF_KINDS)}", entity="ref"
        )


def _predicate(src: UUID, dst_doc: str, dst_node: UUID | None, kind: str) -> list[Any]:
    """三元组 + kind 的匹配条件（`dst_node_id IS NULL` 需显式判空）。"""
    conditions: list[Any] = [
        refs.c.src_node_id == src,
        refs.c.dst_doc_id == dst_doc,
        refs.c.kind == kind,
    ]
    conditions.append(
        refs.c.dst_node_id.is_(None) if dst_node is None else refs.c.dst_node_id == dst_node
    )
    return conditions


def _payload(src: UUID, dst_doc: str, dst_node: UUID | None, kind: str) -> dict[str, Any]:
    return jsonable(
        {"src": src, "dst_doc": dst_doc, "dst_node": dst_node, "kind": kind}
    )


class RefRepository(Repository):
    """§3 M02 的引用边读写面。"""

    async def add_ref(
        self,
        src: UUID | str,
        dst_doc: str,
        dst_node: UUID | str | None,
        kind: RefKind,
        ctx: WriteContext,
    ) -> None:
        """新增引用边（重复边 → `ConflictError`，唯一约束 `refs_unique` NULLS NOT DISTINCT）。"""
        _check_kind(kind)
        src_uuid = as_uuid(src)
        dst_uuid = as_uuid(dst_node) if dst_node is not None else None
        async with self.db.transaction() as session:
            row = (
                await session.execute(
                    select(nodes.c.status).where(nodes.c.node_id == src_uuid)
                )
            ).first()
            if row is None or row.status != "active":
                raise NotFoundError(
                    f"ref source node {src} not found or deleted (ADR-009：外键降级为应用层校验)",
                    entity="ref",
                    entity_id=src,
                )
            ref_id = new_uuid7()
            try:
                await session.execute(
                    insert(refs).values(
                        ref_id=ref_id,
                        src_node_id=src_uuid,
                        dst_doc_id=dst_doc,
                        dst_node_id=dst_uuid,
                        kind=kind,
                    )
                )
            except IntegrityError as exc:
                raise translate_integrity_error(exc, entity="ref", entity_id=ref_id) from exc
            await append_event(
                session,
                entity="ref",
                entity_id=ref_id,
                op="add",
                payload=_payload(src_uuid, dst_doc, dst_uuid, kind),
                actor=ctx.actor,
                ts=now(),
            )

    async def remove_ref(
        self,
        src: UUID | str,
        dst_doc: str,
        dst_node: UUID | str | None,
        kind: RefKind,
        ctx: WriteContext,
    ) -> None:
        """删除引用边（边不存在 → `NotFoundError`）。"""
        _check_kind(kind)
        src_uuid = as_uuid(src)
        dst_uuid = as_uuid(dst_node) if dst_node is not None else None
        async with self.db.transaction() as session:
            result = await session.execute(
                delete(refs).where(*_predicate(src_uuid, dst_doc, dst_uuid, kind))
            )
            if not result.rowcount:
                raise NotFoundError(
                    f"ref {kind} {src} → {dst_doc}/{dst_node} not found",
                    entity="ref",
                    entity_id=src,
                )
            await append_event(
                session,
                entity="ref",
                entity_id=src_uuid,
                op="remove",
                payload=_payload(src_uuid, dst_doc, dst_uuid, kind),
                actor=ctx.actor,
                ts=now(),
            )

    async def list_refs(self, src_node_id: UUID | str) -> list[Ref]:
        """出边（`src_node_id`，外键降级后依赖 `idx_refs_src`）。"""
        statement = (
            select(*REF_COLUMNS)
            .where(refs.c.src_node_id == as_uuid(src_node_id))
            .order_by(refs.c.kind, refs.c.dst_doc_id)
        )
        async with self.db.session() as session:
            rows = (await session.execute(statement)).all()
        return [build_model(Ref, row_to_dict(row)) for row in rows]

    async def list_refs_to(
        self, dst_doc_id: str, dst_node_id: UUID | str | None = None
    ) -> list[Ref]:
        """入边（`idx_refs_dst`）：文档级或节点级。"""
        statement = select(*REF_COLUMNS).where(refs.c.dst_doc_id == dst_doc_id)
        if dst_node_id is not None:
            statement = statement.where(refs.c.dst_node_id == as_uuid(dst_node_id))
        async with self.db.session() as session:
            rows = (await session.execute(statement)).all()
        return [build_model(Ref, row_to_dict(row)) for row in rows]
