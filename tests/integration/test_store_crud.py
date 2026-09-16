"""M02 集成测试：真实 PostgreSQL（`DATABASE_URL`）。

不需要运行的场景（无 PG / 无凭据）由 `conftest.py` 整体 skip，不会 fail。

覆盖：CRUD、乐观锁 409、软删 + orphan、事件同事务回滚、分区存在性、append-only
库层强制、重放与当前态一致（M09B `events_consistency` 判据）、锚冲突、外键降级校验。
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from agenticdocer.model import DocIn, NodeIn, WriteContext, new_uuid7
from agenticdocer.store import (
    ConflictError,
    Database,
    EventRepository,
    NotFoundError,
    Storage,
    ValidationError,
)
from agenticdocer.store.schema import metadata

pytestmark = pytest.mark.integration

CTX = WriteContext(actor="tester", source="cli")


def doc_in(doc_id: str, title: str = "AMBA APB 规范") -> DocIn:
    return DocIn(
        doc_id=doc_id,
        doc_type="standard",
        title=title,
        meta={"spec_revision": "2.0", "spec_org": "ARM"},
        source_ref="IHI0024",
    )


def node_in(
    doc_id: str,
    *,
    node_id=None,
    ordinal: int = 1,
    parent=None,
    level=None,
    anchor: str | None = None,
    body: str = "APB 信号时序要求",
    atom_type: str = "clause",
    content: dict | None = None,
) -> NodeIn:
    return NodeIn(
        node_id=node_id,
        doc_id=doc_id,
        atom_type=atom_type,
        ordinal=ordinal,
        parent_node_id=parent,
        level=level,
        anchor=anchor or f"{doc_id}#{ordinal}",
        content=content if content is not None else {"text": body},
    )


async def scalar(database: Database, sql: str, **params):
    async with database.session() as session:
        return (await session.execute(text(sql), params)).scalar_one()


# --------------------------------------------------------------- 结构：表与分区


async def test_all_tables_and_partitions_exist(database: Database, migrated_schema: str) -> None:
    async with database.session() as session:
        relations = (
            await session.execute(
                text(
                    "SELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace "
                    "WHERE n.nspname = 'public' AND c.relkind IN ('r', 'p') AND NOT c.relispartition"
                )
            )
        ).scalars()
        names = {name for name in relations if name != "alembic_version"}
        assert names == set(metadata.tables)
        assert len(names) == 13

        node_partitions = (
            await session.execute(
                text(
                    "SELECT count(*) FROM pg_class WHERE relkind = 'r' AND relispartition "
                    "AND relname ~ '^nodes_p[0-9]+$'"
                )
            )
        ).scalar_one()
        assert node_partitions == 64

        event_partitions = (
            await session.execute(
                text(
                    "SELECT relname FROM pg_class WHERE relkind = 'r' AND relispartition "
                    "AND relname ~ '^events_'"
                )
            )
        ).scalars()
        event_partitions = set(event_partitions)
        assert "events_default" in event_partitions
        assert sum(1 for name in event_partitions if re.fullmatch(r"events_\d{6}", name)) >= 4

        generated = (
            await session.execute(
                text(
                    "SELECT is_generated FROM information_schema.columns "
                    "WHERE table_name = 'nodes' AND column_name = 'text_fts'"
                )
            )
        ).scalar_one_or_none()
        assert generated == "ALWAYS"

        node_pk = (
            await session.execute(
                text(
                    "SELECT a.attname FROM pg_index i JOIN pg_attribute a "
                    "ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey) "
                    "WHERE i.indrelid = 'nodes'::regclass AND i.indisprimary"
                )
            )
        ).scalars()
        assert set(node_pk) == {"node_id", "doc_id"}

        event_pk = (
            await session.execute(
                text(
                    "SELECT a.attname FROM pg_index i JOIN pg_attribute a "
                    "ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey) "
                    "WHERE i.indrelid = 'events'::regclass AND i.indisprimary"
                )
            )
        ).scalars()
        assert set(event_pk) == {"event_id", "ts"}

        # ADR-009：6 处外键降级 → 分区表上的外键引用只剩 nodes.doc_id → docs
        federated = (
            await session.execute(
                text(
                    "SELECT conrelid::regclass::text AS child, confrelid::regclass::text AS parent "
                    "FROM pg_constraint WHERE contype = 'f' "
                    "AND conrelid::regclass::text IN ('nodes', 'refs', 'comments', 'terms', 'events')"
                )
            )
        ).all()
        assert [(row.child, row.parent) for row in federated] == [("nodes", "docs")]


async def test_text_fts_generated_column_populated(database: Database, storage: Storage) -> None:
    doc_id = "SPEC-FTS"
    await storage.upsert_doc(doc_in(doc_id), None, CTX)
    await storage.upsert_node(node_in(doc_id, body="APB signal timing requirements"), None, CTX)

    async with database.session() as session:
        matched = (
            await session.execute(
                text(
                    "SELECT count(*) FROM nodes WHERE doc_id = :doc "
                    "AND text_fts @@ to_tsquery('english', 'timing')"
                ),
                {"doc": doc_id},
            )
        ).scalar_one()
    assert matched == 1


# ------------------------------------------------------------------ 文档与节点 CRUD


async def test_doc_lifecycle_and_status_flow(storage: Storage) -> None:
    doc_id = "SPEC-DOC"
    doc = await storage.upsert_doc(doc_in(doc_id), None, CTX)
    assert (doc.doc_id, doc.status, doc.version) == (doc_id, "draft", 1)

    listed = {d.doc_id: d for d in await storage.list_docs()}
    assert listed[doc_id].status == "draft"
    # 共享库上可能有他人的 approved 文档（默认不重建 schema）→ 只断言本 doc 的状态
    assert doc_id not in {d.doc_id for d in await storage.list_docs(status="approved")}

    reviewed = await storage.update_doc_status(doc_id, "reviewed", doc.version, CTX)
    assert (reviewed.status, reviewed.version) == ("reviewed", 2)

    approved = await storage.update_doc_status(doc_id, "approved", reviewed.version, CTX)
    assert (approved.status, approved.version) == ("approved", 3)
    assert (await storage.get_doc(doc_id)).status == "approved"

    with pytest.raises(ConflictError) as conflict:
        await storage.update_doc_status(doc_id, "draft", reviewed.version, CTX)
    assert conflict.value.status_code == 409

    # 幂等：同状态不写事件、不增版本
    assert (await storage.update_doc_status(doc_id, "approved", 3, CTX)).version == 3


async def test_node_crud_and_ordering(storage: Storage) -> None:
    doc_id = "SPEC-NODES"
    await storage.upsert_doc(doc_in(doc_id), None, CTX)
    for ordinal in (3, 1, 2):
        await storage.upsert_node(node_in(doc_id, ordinal=ordinal), None, CTX)

    nodes = await storage.get_doc_nodes(doc_id)
    assert [n.ordinal for n in nodes] == [1, 2, 3]
    assert all(n.version == 1 and n.status == "active" for n in nodes)

    target = nodes[0]
    updated = await storage.upsert_node(
        node_in(doc_id, node_id=target.node_id, ordinal=1, body="修订后的正文"),
        target.version,
        CTX,
    )
    assert (updated.version, updated.content["text"]) == (2, "修订后的正文")
    assert (await storage.get_node(target.node_id)).content["text"] == "修订后的正文"

    # 无变化 → 幂等：不增版本
    again = await storage.upsert_node(
        node_in(doc_id, node_id=target.node_id, ordinal=1, body="修订后的正文"), 2, CTX
    )
    assert again.version == 2

    with pytest.raises(NotFoundError):
        await storage.get_node(new_uuid7())

    with pytest.raises(ConflictError) as conflict:
        await storage.upsert_node(
            node_in(doc_id, node_id=target.node_id, ordinal=1, body="并发写"), 99, CTX
        )
    assert conflict.value.status_code == 409


async def test_anchor_conflict_maps_to_409_with_code(storage: Storage) -> None:
    doc_id = "SPEC-ANCHOR"
    await storage.upsert_doc(doc_in(doc_id), None, CTX)
    await storage.upsert_node(node_in(doc_id, anchor=f"{doc_id}#3.1·timing"), None, CTX)

    with pytest.raises(ConflictError) as conflict:
        await storage.upsert_node(node_in(doc_id, ordinal=2, anchor=f"{doc_id}#3.1·timing"), None, CTX)
    assert conflict.value.code == "DTO_ANCHOR_CONFLICT"
    assert conflict.value.status_code == 409


async def test_parent_node_validation_replaces_downgraded_fk(storage: Storage) -> None:
    doc_id = "SPEC-PARENT"
    await storage.upsert_doc(doc_in(doc_id), None, CTX)
    parent = await storage.upsert_node(node_in(doc_id, ordinal=1, anchor=f"{doc_id}#1"), None, CTX)
    child = await storage.upsert_node(
        node_in(doc_id, ordinal=2, parent=parent.node_id, level=2, anchor=f"{doc_id}#1.1"), None, CTX
    )
    assert child.parent_node_id == parent.node_id

    with pytest.raises(ValidationError):
        await storage.upsert_node(
            node_in(doc_id, ordinal=3, parent=new_uuid7(), anchor=f"{doc_id}#x"), None, CTX
        )


async def test_unknown_doc_rejected_by_retained_fk(storage: Storage) -> None:
    with pytest.raises(ValidationError):
        await storage.upsert_node(node_in("SPEC-MISSING"), None, CTX)


# --------------------------------------------------------------- 软删 + 批注 orphan


async def test_soft_delete_orphans_comments(storage: Storage) -> None:
    doc_id = "SPEC-DELETE"
    await storage.upsert_doc(doc_in(doc_id), None, CTX)
    node = await storage.upsert_node(node_in(doc_id), None, CTX)

    open_comment = await storage.create_comment(node.node_id, "此处时序可疑", node.version, CTX)
    resolved = await storage.update_comment_state(open_comment.comment_id, "resolved", open_comment.version, CTX)
    assert resolved.state == "resolved"
    still_open = await storage.create_comment(node.node_id, "另一条未解决", None, CTX)
    assert still_open.target_event_id is not None

    with pytest.raises(ConflictError):
        await storage.delete_node(node.node_id, expected_version=99, ctx=CTX)

    await storage.delete_node(node.node_id, expected_version=node.version, ctx=CTX)

    with pytest.raises(NotFoundError):
        await storage.get_node(node.node_id)
    deleted = await storage.get_node(node.node_id, include_deleted=True)
    assert (deleted.status, deleted.version) == ("deleted", node.version + 1)
    assert await storage.get_doc_nodes(doc_id) == []

    comments = {c.comment_id: c for c in await storage.list_comments(node.node_id)}
    assert comments[open_comment.comment_id].state == "resolved"  # 非 open 不受影响
    assert comments[still_open.comment_id].state == "orphaned"
    assert comments[still_open.comment_id].version == still_open.version + 1

    # 批注事件（create/update）与节点事件都在
    events = await storage.replay("comment", still_open.comment_id)
    assert [event.op for event in events] == ["create", "update"]

    with pytest.raises(NotFoundError):
        await storage.upsert_node(node_in(doc_id, node_id=node.node_id, ordinal=1, body="复活"), None, CTX)


async def test_comment_optimistic_lock_and_validation(storage: Storage) -> None:
    doc_id = "SPEC-COMMENT"
    await storage.upsert_doc(doc_in(doc_id), None, CTX)
    node = await storage.upsert_node(node_in(doc_id), None, CTX)

    with pytest.raises(ConflictError):
        await storage.create_comment(node.node_id, "旧版本评论", expected_version=99, ctx=CTX)

    comment = await storage.create_comment(node.node_id, "评论", node.version, CTX)
    with pytest.raises(ConflictError):
        await storage.update_comment_state(comment.comment_id, "resolved", 99, CTX)

    with pytest.raises(ValidationError):
        await storage.create_comment(node.node_id, "", None, CTX)

    with pytest.raises(NotFoundError):
        await storage.create_comment(new_uuid7(), "孤儿批注", None, CTX)


# ------------------------------------------------------- 事件：同事务 / 重放 / 只增


async def test_event_and_entity_roll_back_together(
    storage: Storage, database: Database, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc_id = "SPEC-ROLLBACK"
    await storage.upsert_doc(doc_in(doc_id), None, CTX)
    node_id = new_uuid7()

    async def boom(*args, **kwargs):
        raise RuntimeError("event write failed")

    monkeypatch.setattr("agenticdocer.store.nodes.append_event", boom)
    with pytest.raises(RuntimeError):
        await storage.upsert_node(node_in(doc_id, node_id=node_id), None, CTX)

    assert await scalar(database, "SELECT count(*) FROM nodes WHERE node_id = :id", id=node_id) == 0
    assert (
        await scalar(
            database, "SELECT count(*) FROM events WHERE entity = 'node' AND entity_id = :id", id=str(node_id)
        )
        == 0
    )


async def test_replay_reproduces_current_state(storage: Storage) -> None:
    """M09B `events_consistency` 判据：apply_events(replay(...)) == 当前行。"""
    doc_id = "SPEC-REPLAY"
    doc = await storage.upsert_doc(doc_in(doc_id), None, CTX)
    node = await storage.upsert_node(node_in(doc_id), None, CTX)
    node = await storage.upsert_node(
        node_in(doc_id, node_id=node.node_id, ordinal=1, body="第二版正文"), node.version, CTX
    )

    doc = await storage.update_doc_status(doc_id, "reviewed", doc.version, CTX)

    node_events = await storage.replay("node", node.node_id)
    assert [event.op for event in node_events] == ["create", "update"]
    replayed_node = storage.apply_events("node", node_events)
    assert replayed_node.node is not None
    assert replayed_node.node.model_dump() == node.model_dump()

    doc_events = await storage.replay("doc", doc_id)
    assert [event.op for event in doc_events] == ["create", "status"]
    assert storage.apply_events("doc", doc_events)["status"] == doc.status
    assert (await storage.get_doc(doc_id)).model_dump() == doc.model_dump()

    # upto 截断：只重放 create → 回到旧状态
    first_only = await storage.replay("node", node.node_id, upto=node_events[0].ts)
    assert storage.apply_events("node", first_only).node.version == 1

    # 软删后重放与当前行（含已删）一致
    await storage.delete_node(node.node_id, node.version, CTX)
    deleted_events = await storage.replay("node", node.node_id)
    replayed = storage.apply_events("node", deleted_events)
    current = await storage.get_node(node.node_id, include_deleted=True)
    assert replayed.node is not None
    assert replayed.node.model_dump() == current.model_dump()


async def test_events_append_only(storage: Storage, database: Database) -> None:
    forbidden = ("update", "delete", "update_event", "delete_event", "remove_event", "purge_events")
    assert not any(hasattr(EventRepository, name) for name in forbidden)

    doc_id = "SPEC-APPEND"
    await storage.upsert_doc(doc_in(doc_id), None, CTX)
    node = await storage.upsert_node(node_in(doc_id), None, CTX)
    assert len(await storage.replay("node", node.node_id)) == 1

    async with database.session() as session:
        can_update = (
            await session.execute(text("SELECT has_table_privilege(current_user, 'events', 'UPDATE')"))
        ).scalar_one()
        can_delete = (
            await session.execute(text("SELECT has_table_privilege(current_user, 'events', 'DELETE')"))
        ).scalar_one()
    if can_update or can_delete:
        pytest.skip(f"当前连接角色拥有 events 改写权限（{metadata}），库层强制不适用")

    with pytest.raises(DBAPIError):
        async with database.transaction() as session:
            await session.execute(text("UPDATE events SET actor = 'attacker'"))
    with pytest.raises(DBAPIError):
        async with database.transaction() as session:
            await session.execute(text("DELETE FROM events"))


async def test_auth_audit_events_are_written(storage: Storage) -> None:
    # actor 取唯一值：共享库上他人（M10）可能已为 'lxx' 写过 auth 事件，勿做全局断言
    actor = f"m02-audit-{new_uuid7()}"
    await storage.log_auth_event(
        op="login", actor=actor, payload={"user_id": actor, "ip": "127.0.0.1"}
    )
    events = await storage.replay("auth", actor)
    assert [event.op for event in events] == ["login"]
    assert storage.apply_events("auth", events)["audit"][0]["payload"]["ip"] == "127.0.0.1"


# ------------------------------------------------------------------------- 引用边


async def test_ref_add_list_remove(storage: Storage) -> None:
    doc_id = "SPEC-REF"
    await storage.upsert_doc(doc_in(doc_id), None, CTX)
    src = await storage.upsert_node(node_in(doc_id), None, CTX)
    dst = await storage.upsert_node(node_in(doc_id, ordinal=2, anchor=f"{doc_id}#2"), None, CTX)

    await storage.add_ref(src.node_id, doc_id, dst.node_id, "traces_to", CTX)
    await storage.add_ref(src.node_id, "EXT:https://example.org/spec", None, "source_ref", CTX)

    refs = await storage.list_refs(src.node_id)
    assert {(ref.kind, ref.dst_doc_id) for ref in refs} == {
        ("traces_to", doc_id),
        ("source_ref", "EXT:https://example.org/spec"),
    }
    assert len(await storage.list_refs_to(doc_id, dst.node_id)) == 1

    traces = next(ref for ref in refs if ref.kind == "traces_to")
    ref_events = await storage.replay("ref", traces.ref_id)
    assert [event.op for event in ref_events] == ["add"]
    assert storage.apply_events("ref", ref_events)["refs"] == [
        {
            "src_node_id": str(src.node_id),
            "dst_doc_id": doc_id,
            "dst_node_id": str(dst.node_id),
            "kind": "traces_to",
        }
    ]

    with pytest.raises(ConflictError):
        await storage.add_ref(src.node_id, doc_id, dst.node_id, "traces_to", CTX)

    with pytest.raises(ValidationError):
        await storage.add_ref(src.node_id, doc_id, dst.node_id, "unknown_kind", CTX)

    with pytest.raises(NotFoundError):
        await storage.add_ref(new_uuid7(), doc_id, None, "traces_to", CTX)

    await storage.remove_ref(src.node_id, doc_id, dst.node_id, "traces_to", CTX)
    assert [ref.kind for ref in await storage.list_refs(src.node_id)] == ["source_ref"]

    with pytest.raises(NotFoundError):
        await storage.remove_ref(src.node_id, doc_id, dst.node_id, "traces_to", CTX)

    # add + remove 折叠 → 行集为空（§3.5 ref 折叠规则）
    removed = await storage.replay("ref", traces.ref_id)
    assert [event.op for event in removed] == ["add", "remove"]
    assert storage.apply_events("ref", removed)["refs"] == []


# --------------------------------------------------------------------------- 资产


async def test_asset_roundtrip_and_missing_detection(storage: Storage) -> None:
    payload = b"\x89PNG\r\n\x1a\n fake bytes"
    asset_id = await storage.put_asset(payload, "image/png", "IHI0024_html/fig1.png")
    assert asset_id == await storage.put_asset(payload, "image/png", "IHI0024_html/fig1.png")

    path = await storage.get_asset_path(asset_id)
    assert path.read_bytes() == payload
    assert path.parent.name == asset_id[:2]

    async with storage.db.session() as session:
        rows = (
            await session.execute(text("SELECT count(*) FROM assets WHERE asset_id = :id"), {"id": asset_id})
        ).scalar_one()
    assert rows == 1

    doc_id = "SPEC-ASSET"
    await storage.upsert_doc(doc_in(doc_id), None, CTX)
    missing_id = "0" * 64
    # 三种引用形态都要认（M03 报告：导入期只有前两种，不含 assets/ 前缀）
    figure_missing = "1" * 64
    html_missing = "2" * 64
    await storage.upsert_node(
        node_in(
            doc_id,
            ordinal=1,
            atom_type="figure",
            content={"text": "图 3-1", "asset_ref": figure_missing, "alt": "fig"},
        ),
        None,
        CTX,
    )
    await storage.upsert_node(
        node_in(
            doc_id,
            ordinal=2,
            atom_type="table",
            content={"text": "表格", "fragment": f'<img src="images/{html_missing}.jpg">'},
        ),
        None,
        CTX,
    )
    await storage.upsert_node(
        node_in(
            doc_id,
            ordinal=3,
            content={
                "text": f"渲染产物形态 assets/{asset_id}.png，以及 assets/{missing_id}.png"
            },
        ),
        None,
        CTX,
    )

    expected = sorted([figure_missing, html_missing, missing_id])
    assert await storage.list_missing_assets(doc_id) == expected
    # 全库形态：他人数据（如 M03/M04 真实导入的语料）可能也带缺失引用，
    # 故只断言「本测试的三条都在」+「已落库的 asset 不在」，不做全局相等
    everything = await storage.list_missing_assets()
    assert set(expected) <= set(everything)

    with pytest.raises(NotFoundError):
        await storage.get_asset_path(missing_id)

    # 已落库且有字节的资产不报缺失（asset_id 自身出现在内容里也不计入）
    assert asset_id not in await storage.list_missing_assets(doc_id)


async def test_asset_store_dir_is_injectable(tmp_path: Path, storage: Storage) -> None:
    assert storage.store_dir == tmp_path / "assets"
    assert await storage.put_asset(b"x", "text/plain", "seed") != ""


# ------------------------------------------------------------------ 增量事件流


async def test_changes_since_cursor_scan(storage: Storage) -> None:
    """M-LR `change_stream` 契约：`(ts, event_id)` 定序、游标续扫不重不漏。"""
    doc_id = "SPEC-STREAM"
    await storage.upsert_doc(doc_in(doc_id), None, CTX)
    node = await storage.upsert_node(node_in(doc_id), None, CTX)
    await storage.upsert_node(
        node_in(doc_id, node_id=node.node_id, ordinal=1, body="改写后的正文"), node.version, CTX
    )
    await storage.upsert_doc(doc_in(doc_id, title="新标题"), None, CTX)

    everything = await storage.changes_since(limit=10_000)
    ordered = [(event.ts, event.event_id) for event in everything]
    assert ordered == sorted(ordered)

    mine = [event for event in everything if event.entity_id in {doc_id, str(node.node_id)}]
    assert [(event.entity, event.op) for event in mine] == [
        ("doc", "create"),
        ("node", "create"),
        ("node", "update"),
        ("doc", "update"),
    ]

    # 游标分页：拼接结果与一次扫全逐条相同，且无重复
    first = await storage.changes_since(limit=3)
    second = await storage.changes_since(
        since_ts=first[-1].ts, since_event_id=first[-1].event_id, limit=10_000
    )
    assert len(first) == 3
    paged = [event.event_id for event in first + second]
    assert paged == [event.event_id for event in everything]
    assert len(paged) == len(set(paged))

    # 只给时间戳（半开区间）与实体过滤
    tail = await storage.changes_since(since_ts=first[-1].ts, limit=10_000)
    assert [event.event_id for event in tail] == [
        event.event_id for event in everything if event.ts > first[-1].ts
    ]
    node_only = await storage.changes_since(entity="node", limit=10_000)
    assert node_only and {event.entity for event in node_only} == {"node"}

    with pytest.raises(ValidationError):
        await storage.changes_since(limit=0)
    with pytest.raises(ValidationError):
        await storage.changes_since(entity="asset")
