"""文档仓储（A17：docs 级方法 + 状态流转乐观锁；R7：`list_docs`）。"""

from __future__ import annotations

from typing import Any, Final

from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ._compat import Doc, DocIn, DocStatus, WriteContext
from .errors import ConflictError, NotFoundError, ValidationError, translate_integrity_error
from .events import append_event
from .repository import Repository
from .rows import build_model, field_deltas, now, row_to_dict
from .schema import docs

__all__ = ["DOC_COLUMNS", "DocRepository", "fetch_doc"]

DOC_COLUMNS: Final = tuple(docs.c)
_STATUSES: Final = ("draft", "reviewed", "approved")
_MUTABLE_FIELDS: Final = ("doc_type", "title", "meta", "source_ref")


async def fetch_doc(session: AsyncSession, doc_id: str) -> dict[str, Any] | None:
    row = (await session.execute(select(*DOC_COLUMNS).where(docs.c.doc_id == doc_id))).first()
    return row_to_dict(row) if row is not None else None


class DocRepository(Repository):
    """§3 M02 的文档读写面（乐观锁与节点一致）。"""

    async def get_doc(self, doc_id: str) -> Doc:
        async with self.db.session() as session:
            row = await fetch_doc(session, doc_id)
        if row is None:
            raise NotFoundError(f"doc {doc_id} not found", entity="doc", entity_id=doc_id)
        return build_model(Doc, row)

    async def list_docs(self, status: DocStatus | None = None) -> list[Doc]:
        """文档清单（R7）；`status` 省略则不过滤（含 draft/reviewed/approved）。"""
        statement = select(*DOC_COLUMNS)
        if status is not None:
            statement = statement.where(docs.c.status == status)
        statement = statement.order_by(docs.c.doc_id)
        async with self.db.session() as session:
            rows = (await session.execute(statement)).all()
        return [build_model(Doc, row_to_dict(row)) for row in rows]

    async def upsert_doc(
        self,
        doc: DocIn,
        expected_version: int | None,
        ctx: WriteContext,
    ) -> Doc:
        """创建或更新文档元信息（M03 入库用；`status` 不进本方法，走 `update_doc_status`）。"""
        incoming = doc.model_dump()
        doc_id = incoming["doc_id"]
        async with self.db.transaction() as session:
            existing = await fetch_doc(session, doc_id)
            timestamp = now()
            if existing is None:
                if expected_version is not None:
                    raise ConflictError(
                        f"doc {doc_id} does not exist but expected_version={expected_version} was given",
                        entity="doc",
                        entity_id=doc_id,
                    )
                record = {
                    "doc_id": doc_id,
                    "doc_type": incoming["doc_type"],
                    "title": incoming["title"],
                    "meta": incoming.get("meta") or {},
                    "source_ref": incoming.get("source_ref"),
                    "status": "draft",
                    "version": 1,
                    "created_at": timestamp,
                    "updated_at": timestamp,
                }
                try:
                    await session.execute(insert(docs).values(**record))
                except IntegrityError as exc:
                    raise translate_integrity_error(exc, entity="doc", entity_id=doc_id) from exc
                await append_event(
                    session,
                    entity="doc",
                    entity_id=doc_id,
                    op="create",
                    payload=field_deltas({}, record, include_unchanged=True),
                    actor=ctx.actor,
                    ts=timestamp,
                )
                return build_model(Doc, record)

            if expected_version is not None and expected_version != existing["version"]:
                raise ConflictError(
                    f"doc {doc_id} version mismatch: expected {expected_version}, "
                    f"stored {existing['version']}",
                    entity="doc",
                    entity_id=doc_id,
                )
            candidate = {**existing, **{f: incoming.get(f) for f in _MUTABLE_FIELDS}}
            content_deltas = field_deltas(existing, candidate)
            if not content_deltas:
                return build_model(Doc, existing)
            version = existing["version"] + 1
            record = {**candidate, "version": version, "updated_at": timestamp}
            # 载荷含 version/updated_at，重放可与当前行逐字段比对（M09B events_consistency）
            deltas = field_deltas(existing, record)
            values = {field: record[field] for field in content_deltas}
            values["version"] = version
            values["updated_at"] = timestamp
            await session.execute(update(docs).where(docs.c.doc_id == doc_id).values(**values))
            await append_event(
                session,
                entity="doc",
                entity_id=doc_id,
                op="update",
                payload=deltas,
                actor=ctx.actor,
                ts=timestamp,
            )
            return build_model(Doc, record)

    async def update_doc_status(
        self,
        doc_id: str,
        status: DocStatus,
        expected_version: int,
        ctx: WriteContext,
    ) -> Doc:
        """状态流转（draft→reviewed→approved）；不匹配 → 409（A17）。"""
        if status not in _STATUSES:
            raise ValidationError(
                f"unknown doc status {status!r}; expected one of {list(_STATUSES)}",
                entity="doc",
                entity_id=doc_id,
            )
        async with self.db.transaction() as session:
            existing = await fetch_doc(session, doc_id)
            if existing is None:
                raise NotFoundError(f"doc {doc_id} not found", entity="doc", entity_id=doc_id)
            if existing["version"] != expected_version:
                raise ConflictError(
                    f"doc {doc_id} version mismatch: expected {expected_version}, "
                    f"stored {existing['version']}",
                    entity="doc",
                    entity_id=doc_id,
                )
            if existing["status"] == status:
                return build_model(Doc, existing)
            timestamp = now()
            record = {**existing, "status": status, "version": existing["version"] + 1, "updated_at": timestamp}
            await session.execute(
                update(docs)
                .where(docs.c.doc_id == doc_id)
                .values(status=status, version=record["version"], updated_at=timestamp)
            )
            await append_event(
                session,
                entity="doc",
                entity_id=doc_id,
                op="status",
                payload=field_deltas(existing, record),
                actor=ctx.actor,
                ts=timestamp,
            )
            return build_model(Doc, record)
