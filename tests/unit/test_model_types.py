"""M01 公共类型测试：字段口径、camelCase 序列化（§6）、边界校验、组合与嵌套。"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from agenticdocer.model import (
    Asset,
    AssetSyncReport,
    Comment,
    CommitResult,
    Doc,
    DocIn,
    DocTarget,
    DocTypeTarget,
    Event,
    ExportResult,
    Grant,
    GrantTarget,
    Node,
    NodeIn,
    NodeSnapshot,
    ParseResult,
    ParseStats,
    Proposal,
    QualityReport,
    QualityScope,
    RawFallback,
    Ref,
    RenderResult,
    SchemaDef,
    SearchHit,
    Session,
    SshKey,
    Term,
    TraversalHit,
    UnmappedBlock,
    User,
    Violation,
    WriteContext,
)

NOW = datetime(2026, 9, 16, 12, 0, 0, tzinfo=timezone.utc)


def node_in_payload(**overrides: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "node_id": None,
        "doc_id": "SPEC-STD-PCIE-5.0",
        "atom_type": "clause",
        "ordinal": 0,
        "parent_node_id": None,
        "level": 1,
        "anchor": "SPEC-STD-PCIE-5.0#11.2.3·timing",
        "content": {"text": "Timing parameters"},
    }
    payload.update(overrides)
    return payload


def node_payload(**overrides: Any) -> dict[str, Any]:
    payload = node_in_payload(**overrides)
    payload.update(
        node_id=uuid4(), status="active", version=1, created_at=NOW, updated_at=NOW
    )
    return payload


# ── NodeIn / Node（§3.0 + §4 DDL）────────────────────────────────────────


def test_node_in_defaults_and_field_names():
    node = NodeIn(**node_in_payload())

    assert node.format == "md"
    assert node.node_id is None
    assert node.parent_node_id is None
    assert node.level == 1


def test_node_in_serializes_camel_case_only_via_alias():
    node = NodeIn(**node_in_payload())
    camel = node.model_dump(by_alias=True)

    assert set(camel) == {
        "nodeId",
        "docId",
        "atomType",
        "format",
        "ordinal",
        "parentNodeId",
        "level",
        "anchor",
        "content",
    }
    assert node.model_dump()["doc_id"] == "SPEC-STD-PCIE-5.0"


def test_node_in_accepts_both_snake_and_camel_input():
    camel = NodeIn(**node_in_payload()).model_dump(by_alias=True)
    camel["parentNodeId"] = str(uuid4())
    camel["format"] = "html"

    node = NodeIn.model_validate(camel)

    assert node.format == "html"
    assert isinstance(node.parent_node_id, UUID)


def test_node_in_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        NodeIn(**node_in_payload(spelling_mistake=1))


def test_node_in_rejects_blank_doc_id_and_negative_ordinal():
    with pytest.raises(ValidationError):
        NodeIn(**node_in_payload(doc_id=""))
    with pytest.raises(ValidationError):
        NodeIn(**node_in_payload(ordinal=-1))


def test_node_in_rejects_unknown_format():
    with pytest.raises(ValidationError):
        NodeIn(**node_in_payload(format="rst"))


def test_atom_type_is_open_string_with_schema_closed_set():
    """§3.0 将 atom_type 定为 str；闭集约束由 M01 的 schema 注册表承担（REQ-M01-F01）。"""
    from agenticdocer.model import UnknownAtomTypeError, get_atom_schema

    assert NodeIn(**node_in_payload(atom_type="not-an-atom")).atom_type == "not-an-atom"
    with pytest.raises(UnknownAtomTypeError):
        get_atom_schema("not-an-atom")
    with pytest.raises(UnknownAtomTypeError):
        get_atom_schema("clause.typo")


def test_node_requires_status_version_and_timestamps():
    payload = node_payload()
    for missing in ("status", "version", "created_at", "updated_at", "node_id"):
        broken = dict(payload)
        broken.pop(missing)
        with pytest.raises(ValidationError):
            Node(**broken)


def test_node_status_and_version_bounds():
    with pytest.raises(ValidationError):
        Node(**node_payload(status="orphaned"))
    with pytest.raises(ValidationError):
        Node(**node_payload(version=0))


def test_node_has_no_generated_fts_column():
    """nodes.text_fts 为 PG 生成列（§4 DDL / A10），非领域字段。"""
    assert "text_fts" not in Node.model_fields


def test_node_json_round_trip_is_camel_case():
    node = Node(**node_payload())
    restored = Node.model_validate_json(node.model_dump_json(by_alias=True))

    assert restored == node
    assert '"docId"' in node.model_dump_json(by_alias=True)
    assert "doc_id" not in node.model_dump_json(by_alias=True)


def test_node_snapshot_allows_absent_node():
    snapshot = NodeSnapshot(node=None, history=[])
    assert snapshot.node is None


# ── Doc / DocIn ─────────────────────────────────────────────────────────


def test_doc_in_and_doc_fields():
    doc_in = DocIn(
        doc_id="SPEC-STD-CXL-3.2",
        doc_type="standard",
        title="CXL 3.2",
        meta={"spec_id": "SPEC-STD-CXL-3.2"},
        source_ref=None,
    )
    doc = Doc(**doc_in.model_dump(), status="draft", version=1, created_at=NOW, updated_at=NOW)

    assert doc.model_dump(by_alias=True)["sourceRef"] is None
    assert doc.status == "draft"

    with pytest.raises(ValidationError):
        Doc(**doc_in.model_dump(), status="rejected", version=1, created_at=NOW, updated_at=NOW)


def test_doc_in_requires_meta_and_source_ref():
    with pytest.raises(ValidationError):
        DocIn(doc_id="SPEC-X", doc_type="standard", title="X")


# ── Event（§3.0 + §3.5）─────────────────────────────────────────────────


def test_event_accepts_all_entity_and_op_domains():
    for entity in ("doc", "node", "ref", "comment", "schema", "auth"):
        for op in (
            "create",
            "update",
            "delete",
            "status",
            "add",
            "remove",
            "login",
            "logout",
            "fail",
            "user_change",
            "grant_change",
            "key_change",
        ):
            event = Event(
                event_id=uuid4(),
                entity=entity,
                entity_id="SPEC-STD-X",
                op=op,
                payload={},
                actor=str(uuid4()),
                ts=NOW,
            )
            assert event.op == op


def test_event_rejects_unknown_entity_or_op():
    with pytest.raises(ValidationError):
        Event(event_id=uuid4(), entity="user", entity_id="x", op="create", payload={}, actor="a", ts=NOW)
    with pytest.raises(ValidationError):
        Event(event_id=uuid4(), entity="user", entity_id="x", op="upsert", payload={}, actor="a", ts=NOW)
    with pytest.raises(ValidationError):
        Event(event_id=uuid4(), entity="auth", entity_id="x", op="login", payload={}, actor="", ts=NOW)


def test_event_field_diff_payload_shape_is_preserved():
    event = Event(
        event_id=uuid4(),
        entity="node",
        entity_id=str(uuid4()),
        op="update",
        payload={"anchor": {"before": "a", "after": "b"}, "version": {"before": 1, "after": 2}},
        actor="agent-1",
        ts=NOW,
    )

    assert event.payload["anchor"] == {"before": "a", "after": "b"}
    assert event.model_dump(by_alias=True)["eventId"] == str(event.event_id)


# ── WriteContext / Violation ─────────────────────────────────────────────


def test_write_context_requires_actor_and_known_source():
    assert WriteContext(actor="importer", source="importer").source == "importer"

    with pytest.raises(ValidationError):
        WriteContext(actor="", source="cli")
    with pytest.raises(ValidationError):
        WriteContext(actor="x", source="script")


def test_violation_optionality_matches_spec():
    """§3.0 未给 `fix_hint` 默认值 → 必填字段，可显式为 None。"""
    violation = Violation(rule_id="M09A-001", path="content.text", message="空文本", fix_hint=None)

    assert violation.fix_hint is None
    with pytest.raises(ValidationError):
        Violation(rule_id="M09A-001", path="content.text", message="空文本")


# ── 引用 / 批注 / schema / 资产 / 术语 ──────────────────────────────────


def test_ref_nullable_dst_node_for_document_level_edge():
    doc_level = Ref(ref_id=uuid4(), src_node_id=uuid4(), dst_doc_id="EXT:https://x", dst_node_id=None, kind="source_ref")
    node_level = Ref(ref_id=uuid4(), src_node_id=uuid4(), dst_doc_id="SPEC-STD-X", dst_node_id=uuid4(), kind="traces_to")

    assert doc_level.dst_node_id is None
    assert node_level.kind == "traces_to"

    with pytest.raises(ValidationError):
        Ref(ref_id=uuid4(), src_node_id=uuid4(), dst_doc_id="SPEC-STD-X", dst_node_id=None, kind="depends_on")


def test_comment_states_and_version_lock():
    comment = Comment(
        comment_id=uuid4(),
        node_id=uuid4(),
        target_event_id=None,
        body="请确认该时序",
        state="open",
        author="reviewer-1",
        version=1,
        ts=NOW,
    )

    assert comment.state == "open"
    with pytest.raises(ValidationError):
        Comment(
            comment_id=uuid4(),
            node_id=uuid4(),
            target_event_id=None,
            body="x",
            state="closed",
            author="a",
            version=1,
            ts=NOW,
        )


def test_schema_def_asset_and_term():
    definition = SchemaDef(type_name="table.register_field", json_schema={"type": "object"}, version=1)
    asset = Asset(asset_id="a" * 64, mime="image/png", bytes=1024, origin=None, path="images/aa.png")
    term = Term(term="AMBA", definition_node_id=None, kind="normative-keyword")

    assert definition.model_dump(by_alias=True)["jsonSchema"] == {"type": "object"}
    assert asset.bytes == 1024
    with pytest.raises(ValidationError):
        Term(term="AMBA", definition_node_id=None, kind="glossary-term")


# ── M10 身份类型（§3 M10 + S5 + §4 DDL）────────────────────────────────


def test_user_sshkey_grant_and_session():
    user = User(user_id=str(uuid4()), username="alice", role="admin", status="active")
    key = SshKey(
        key_id="SHA256:abc",
        fingerprint="SHA256:abc",
        public_key="ssh-ed25519 AAAA alice@host",
        added_at=NOW,
        revoked_at=None,
    )
    grant = Grant(grant_id=str(uuid4()), user_id=user.user_id, scope="doc_type", value="product", permission="write")
    session = Session(
        session_id=uuid4(),
        user_id=user.user_id,
        token_hash="b" * 64,
        created_at=NOW,
        expires_at=NOW + timedelta(hours=8),
        last_seen_at=NOW,
    )

    assert user.role == "admin"
    assert key.revoked_at is None
    assert session.expires_at - session.created_at == timedelta(hours=8)

    with pytest.raises(ValidationError):
        User(user_id=str(uuid4()), username="bob", role="owner", status="active")
    with pytest.raises(ValidationError):
        Grant(grant_id="g", user_id="u", scope="repo", value="x", permission="write")
    with pytest.raises(ValidationError):
        Grant(grant_id="g", user_id="u", scope="doc", value="x", permission="admin")


# ── 授权目标（S5：repo 已删除）与联合类型判别 ────────────────────────────


def test_grant_target_defaults_and_aliases():
    doc_type_target = DocTypeTarget(value="standard")
    doc_target = DocTarget(value="SPEC-STD-X")

    assert doc_type_target.kind == "doc_type"
    assert doc_target.kind == "doc"
    assert GrantTarget is not None

    from agenticdocer.model import GrantTargetDoc, GrantTargetDocType

    assert GrantTargetDocType is DocTypeTarget
    assert GrantTargetDoc is DocTarget


def test_grant_target_union_discriminates_on_kind():
    from pydantic import TypeAdapter

    adapter = TypeAdapter(GrantTarget)

    assert isinstance(adapter.validate_python({"kind": "doc", "value": "SPEC-1"}), DocTarget)
    assert isinstance(adapter.validate_python({"kind": "doc_type", "value": "standard"}), DocTypeTarget)


# ── 解析提议：NodeIn | RawFallback 判别 ─────────────────────────────────


def test_proposal_union_selects_node_in_or_raw_fallback():
    node_proposal = Proposal(
        proposal_id="p1",
        rule_id="R-HEADING",
        confident=True,
        source_lines=(10, 20),
        atom=node_in_payload(),
    )
    fallback_proposal = Proposal(
        proposal_id="p2",
        rule_id="R-FALLBACK",
        confident=False,
        source_lines=(21, 30),
        atom=RawFallback(atom_type="note", format="html", text="<div>toc</div>", source_lines=(21, 30)),
    )

    assert isinstance(node_proposal.atom, NodeIn)
    assert isinstance(fallback_proposal.atom, RawFallback)


def test_parse_result_nests_and_rejects_negative_stats():
    raw = RawFallback(atom_type="code", format="md", text="x", source_lines=(1, 2))
    result = ParseResult(
        doc_meta={"spec_id": "SPEC-STD-X"},
        proposals=[
            Proposal(
                proposal_id="p1",
                rule_id="R1",
                confident=True,
                source_lines=(1, 2),
                atom=node_in_payload(),
            )
        ],
        unmapped=[UnmappedBlock(source_lines=(3, 4), reason="残余 HTML", fallback=raw)],
        stats=ParseStats(total_blocks=3, rule_covered=1, fallback=1, pending=1),
    )

    assert result.stats.fallback == 1
    assert result.unmapped[0].fallback.atom_type == "code"
    with pytest.raises(ValidationError):
        ParseStats(total_blocks=-1, rule_covered=0, fallback=0, pending=0)


# ── 结果类型 ────────────────────────────────────────────────────────────


def test_result_types_and_quality_scope():
    assert SearchHit(node_id=uuid4(), doc_id="d", anchor="a", score=0.5).score == 0.5
    assert TraversalHit(node_id=uuid4(), doc_id="d", anchor="a", hops=2, via=["traces_to", "see_also"]).hops == 2
    assert RenderResult(doc_id="d", out_path="build/d.md", assets_exported=3).assets_exported == 3
    assert CommitResult(
        doc_id="d", nodes_created=5, refs_created=1, stats=ParseStats(total_blocks=6, rule_covered=6, fallback=0, pending=0)
    ).refs_created == 1
    assert QualityReport(detector_id="broken_refs", violations=[Violation(rule_id="r", path="p", message="m", fix_hint="fix")]).violations[
        0
    ].rule_id == "r"
    assert ExportResult(out_path="build/export", docs=7, nodes=9000).nodes == 9000
    assert AssetSyncReport(fetched=2, missing=["missing.png"], total_refs=3).missing == ["missing.png"]
    assert QualityScope(doc_ids=None, detectors=["terms"]).doc_ids is None
    with pytest.raises(ValidationError):
        ExportResult(out_path="x", docs=-1, nodes=0)
