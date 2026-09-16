"""§3.5「事件载荷与折叠规范」单测——纯函数，不需要 PG。

载荷形状**逐字**写在用例里（不从生产代码生成），使本文件成为 §3.5 的独立口径检查；
`rows.field_deltas` 与 `fold.apply_events` 的互认另有一组「写入侧 → 折叠」往返断言。
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

import pytest

from agenticdocer.store import ValidationError
from agenticdocer.model import Event, NodeSnapshot, new_uuid7
from agenticdocer.store.fold import ENTITY_OPS, apply_events
from agenticdocer.store.rows import build_model, field_deltas

TS = datetime(2026, 9, 16, 8, 0, tzinfo=timezone.utc)
TS2 = datetime(2026, 9, 16, 9, 30, tzinfo=timezone.utc)
DOC_ID = "SPEC-APB"
NODE_ID = UUID("01930000-0000-7000-8000-000000000001")
PARENT_ID = UUID("01930000-0000-7000-8000-0000000000ff")


def event(entity: str, entity_id: str, op: str, payload: dict, ts: datetime = TS) -> Event:
    """构造事件（走 `build_model`，与读路径同口径 → 对 M01 别名配置不敏感）。"""
    return build_model(
        Event,
        {
            "event_id": new_uuid7(),
            "entity": entity,
            "entity_id": entity_id,
            "op": op,
            "payload": payload,
            "actor": "tester",
            "ts": ts,
        },
    )


def delta(before, after) -> dict:
    return {"before": before, "after": after}


NODE_ROW = {
    "node_id": str(NODE_ID),
    "doc_id": DOC_ID,
    "atom_type": "clause",
    "format": "md",
    "ordinal": 7,
    "parent_node_id": str(PARENT_ID),
    "level": 2,
    "anchor": "SPEC-APB#3.1·signal-timing",
    "content": {"text": "APB 信号时序要求（含中文）"},
    "status": "active",
    "version": 1,
    "created_at": TS.isoformat(),
    "updated_at": TS.isoformat(),
}

CREATE_PAYLOAD = {field: delta(None, value) for field, value in NODE_ROW.items()}


# --------------------------------------------------------------------------- node


def test_node_create_builds_snapshot() -> None:
    snapshot = apply_events("node", [event("node", str(NODE_ID), "create", CREATE_PAYLOAD)])

    assert isinstance(snapshot, NodeSnapshot)
    assert snapshot.node is not None
    assert snapshot.node.node_id == NODE_ID
    assert snapshot.node.doc_id == DOC_ID
    assert snapshot.node.parent_node_id == PARENT_ID
    assert snapshot.node.status == "active"
    assert snapshot.node.version == 1
    assert snapshot.node.created_at == TS
    assert snapshot.node.content["text"] == "APB 信号时序要求（含中文）"
    assert len(snapshot.history) == 1


def test_node_update_overwrites_only_given_fields() -> None:
    snapshot = apply_events(
        "node",
        [
            event("node", str(NODE_ID), "create", CREATE_PAYLOAD),
            event(
                "node",
                str(NODE_ID),
                "update",
                {"content": delta(NODE_ROW["content"], {"text": "修订后的正文"}), "version": delta(1, 2)},
                ts=TS2,
            ),
        ],
    )

    assert snapshot.node is not None
    assert snapshot.node.content == {"text": "修订后的正文"}
    assert snapshot.node.version == 2
    assert snapshot.node.anchor == NODE_ROW["anchor"]
    assert len(snapshot.history) == 2


def test_node_delete_marks_deleted_and_keeps_before_values() -> None:
    """delete 载荷「before 全量 + after 为删除后行值」（写入侧口径）。"""
    deleted = {**NODE_ROW, "status": "deleted", "version": 2, "updated_at": TS2.isoformat()}
    snapshot = apply_events(
        "node",
        [
            event("node", str(NODE_ID), "create", CREATE_PAYLOAD),
            event(
                "node",
                str(NODE_ID),
                "delete",
                field_deltas(NODE_ROW, deleted, include_unchanged=True),
                ts=TS2,
            ),
        ],
    )

    assert snapshot.node is not None
    assert snapshot.node.status == "deleted"
    assert snapshot.node.version == 2
    assert snapshot.node.updated_at == TS2
    assert snapshot.node.content == NODE_ROW["content"]


def test_node_delete_with_after_none_encoding_falls_back_to_before() -> None:
    """兼容编码：after 恒为 None，此时按 §3.5「delete 含 before 全量」取 before。"""
    payload = {field: delta(value, None) for field, value in NODE_ROW.items()}
    snapshot = apply_events("node", [event("node", str(NODE_ID), "delete", payload)])

    assert snapshot.node is not None
    assert snapshot.node.status == "deleted"
    assert snapshot.node.anchor == NODE_ROW["anchor"]
    assert snapshot.node.ordinal == 7


def test_node_delete_only_reconstructs_from_before() -> None:
    payload = {field: delta(value, None) for field, value in NODE_ROW.items()}
    snapshot = apply_events("node", [event("node", str(NODE_ID), "delete", payload)])

    assert snapshot.node is not None
    assert snapshot.node.doc_id == DOC_ID


def test_node_empty_history_yields_null_node() -> None:
    snapshot = apply_events("node", [])

    assert isinstance(snapshot, NodeSnapshot)
    assert snapshot.node is None
    assert snapshot.history == []


def test_node_entity_id_fills_missing_node_id() -> None:
    payload = {k: v for k, v in CREATE_PAYLOAD.items() if k != "node_id"}
    snapshot = apply_events("node", [event("node", str(NODE_ID), "create", payload)])

    assert snapshot.node is not None
    assert snapshot.node.node_id == NODE_ID
    assert snapshot.node.status == "active"


# ---------------------------------------------------------------------- doc/comment


def test_doc_fold_applies_create_update_and_status() -> None:
    result = apply_events(
        "doc",
        [
            event(
                "doc",
                DOC_ID,
                "create",
                {
                    "doc_id": delta(None, DOC_ID),
                    "doc_type": delta(None, "standard"),
                    "title": delta(None, "AMBA APB 规范"),
                    "meta": delta(None, {"spec_revision": "2.0"}),
                    "source_ref": delta(None, "IHI0024"),
                    "status": delta(None, "draft"),
                    "version": delta(None, 1),
                    "created_at": delta(None, TS.isoformat()),
                    "updated_at": delta(None, TS.isoformat()),
                },
            ),
            event("doc", DOC_ID, "update", {"title": delta("AMBA APB 规范", "AMBA APB 规范 v2.0"),
                                            "version": delta(1, 2)}, ts=TS2),
            event(
                "doc",
                DOC_ID,
                "status",
                {"status": delta("draft", "reviewed"), "version": delta(2, 3)},
                ts=TS2,
            ),
        ],
    )

    assert isinstance(result, dict)
    assert result["doc_id"] == DOC_ID
    assert result["title"] == "AMBA APB 规范 v2.0"
    assert result["status"] == "reviewed"
    assert result["version"] == 3
    assert result["meta"] == {"spec_revision": "2.0"}


def test_comment_fold_tracks_state_transitions() -> None:
    comment_id = new_uuid7()
    result = apply_events(
        "comment",
        [
            event(
                "comment",
                str(comment_id),
                "create",
                {
                    "comment_id": delta(None, str(comment_id)),
                    "node_id": delta(None, str(NODE_ID)),
                    "target_event_id": delta(None, None),
                    "body": delta(None, "此处时序可疑"),
                    "state": delta(None, "open"),
                    "author": delta(None, "lxx"),
                    "version": delta(None, 1),
                    "ts": delta(None, TS.isoformat()),
                },
            ),
            event(
                "comment",
                str(comment_id),
                "update",
                {"state": delta("open", "resolved"), "version": delta(1, 2)},
                ts=TS2,
            ),
        ],
    )

    assert result["comment_id"] == comment_id
    assert result["state"] == "resolved"
    assert result["version"] == 2
    assert result["body"] == "此处时序可疑"


# ---------------------------------------------------------------------- ref/schema/auth


def test_ref_fold_rebuilds_row_set() -> None:
    other = str(new_uuid7())
    add = {"src": str(NODE_ID), "dst_doc": "SPEC-AXI", "dst_node": other, "kind": "traces_to"}
    doc_level = {"src": str(NODE_ID), "dst_doc": "SPEC-AXI", "dst_node": None, "kind": "see_also"}

    result = apply_events(
        "ref",
        [
            event("ref", str(new_uuid7()), "add", add),
            event("ref", str(new_uuid7()), "add", doc_level),
            event("ref", str(new_uuid7()), "remove", add, ts=TS2),
        ],
    )

    assert result["refs"] == [
        {"src_node_id": str(NODE_ID), "dst_doc_id": "SPEC-AXI", "dst_node_id": None, "kind": "see_also"}
    ]


def test_ref_fold_ignores_duplicate_adds() -> None:
    add = {"src": str(NODE_ID), "dst_doc": "SPEC-AXI", "dst_node": None, "kind": "traces_to"}
    result = apply_events(
        "ref",
        [event("ref", str(new_uuid7()), "add", add), event("ref", str(new_uuid7()), "add", add, ts=TS2)],
    )

    assert len(result["refs"]) == 1


def test_schema_fold_records_version_history() -> None:
    result = apply_events(
        "schema",
        [
            event("schema", "clause", "create", {"type_name": "clause", "version": 1, "diff": None}),
            event("schema", "clause", "update", {"type_name": "clause", "version": 2, "diff": {"+": "note"}}, ts=TS2),
        ],
    )

    assert result["type_name"] == "clause"
    assert result["current_version"] == 2
    assert [v["version"] for v in result["versions"]] == [1, 2]
    assert result["versions"][1]["diff"] == {"+": "note"}


def test_auth_events_are_appended_not_folded() -> None:
    result = apply_events(
        "auth",
        [
            event("auth", "user-1", "login", {"user_id": "user-1", "key_fingerprint": "SHA256:abc", "ip": "127.0.0.1"}),
            event("auth", "user-1", "fail", {"user_id": "user-1", "reason": "bad signature"}, ts=TS2),
            event("auth", "user-1", "logout", {"user_id": "user-1"}, ts=TS2),
        ],
    )

    assert [row["op"] for row in result["audit"]] == ["login", "fail", "logout"]
    assert result["audit"][0]["payload"]["key_fingerprint"] == "SHA256:abc"


# ------------------------------------------------------------------- 契约与边界


def test_entity_ops_covers_spec_table() -> None:
    assert set(ENTITY_OPS) == {"doc", "node", "ref", "comment", "schema", "auth"}
    assert ENTITY_OPS["node"] == ("create", "update", "delete")
    assert ENTITY_OPS["ref"] == ("add", "remove")
    assert "login" in ENTITY_OPS["auth"]


def test_unknown_entity_rejected() -> None:
    with pytest.raises(ValidationError):
        apply_events("asset", [])


def test_op_not_valid_for_entity_rejected() -> None:
    with pytest.raises(ValidationError):
        apply_events("node", [event("node", str(NODE_ID), "add", {})])
    with pytest.raises(ValidationError):
        apply_events("ref", [event("ref", str(NODE_ID), "create", {})])
    with pytest.raises(ValidationError):
        apply_events("doc", [event("doc", DOC_ID, "delete", {})])


def test_writer_payload_round_trips_through_fold() -> None:
    """写入侧 `field_deltas` ↔ 折叠的互认：create/update/delete 三态逐字段一致。"""
    row = dict(NODE_ROW)
    create = event(
        "node", str(NODE_ID), "create", field_deltas({}, row, include_unchanged=True)
    )
    updated_row = {**row, "content": {"text": "第二版"}, "version": 2, "updated_at": TS2.isoformat()}
    update = event("node", str(NODE_ID), "update", field_deltas(row, updated_row), ts=TS2)
    deleted_row = {**updated_row, "status": "deleted", "version": 3, "updated_at": TS2.isoformat()}
    delete = event(
        "node",
        str(NODE_ID),
        "delete",
        field_deltas(updated_row, deleted_row, include_unchanged=True),
        ts=TS2,
    )

    snapshot = apply_events("node", [create, update])
    assert snapshot.node is not None
    assert snapshot.node.version == 2
    assert snapshot.node.content == {"text": "第二版"}

    snapshot = apply_events("node", [create, update, delete])
    assert snapshot.node is not None
    assert snapshot.node.version == 3
    assert snapshot.node.status == "deleted"


def test_fold_is_deterministic() -> None:
    events = [
        event("node", str(NODE_ID), "create", CREATE_PAYLOAD),
        event("node", str(NODE_ID), "update", {"version": delta(1, 2)}, ts=TS2),
    ]

    first = apply_events("node", events)
    second = apply_events("node", events)

    assert first == second
    assert first.node.model_dump() == second.node.model_dump()  # type: ignore[union-attr]


def test_flat_row_payload_is_accepted() -> None:
    """扁平整行载荷（外部/历史形态）：字段值按 after 解释。"""
    snapshot = apply_events("node", [event("node", str(NODE_ID), "create", dict(NODE_ROW))])

    assert snapshot.node is not None
    assert snapshot.node.doc_id == DOC_ID
    assert snapshot.node.anchor == NODE_ROW["anchor"]


def test_before_wrapper_payload_is_accepted() -> None:
    payload = {"before": {**NODE_ROW, "status": "deleted"}, "after": {"status": "deleted"}}
    snapshot = apply_events("node", [event("node", str(NODE_ID), "delete", payload)])

    assert snapshot.node is not None
    assert snapshot.node.status == "deleted"
    assert snapshot.node.doc_id == DOC_ID
