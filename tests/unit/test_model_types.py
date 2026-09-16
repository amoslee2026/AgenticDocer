"""M01 公共类型测试：字段口径、camelCase 序列化（§6）、边界校验、组合与嵌套。"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID, uuid4

import pytest
from pydantic import BaseModel, ValidationError

from agenticdocer.model import (
    Asset,
    AssetSyncReport,
    Comment,
    CommitResult,
    Doc,
    DocIn,
    DocTypeRule,
    DocTarget,
    DocTypeTarget,
    Event,
    ExportResult,
    Grant,
    GrantTarget,
    Model,
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
    payload = node_in_payload()
    payload.update(node_id=uuid4(), status="active", version=1, created_at=NOW, updated_at=NOW)
    payload.update(overrides)
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
    assert event.model_dump(mode="json", by_alias=True)["eventId"] == str(event.event_id)


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
    owner = uuid4()
    admin = uuid4()
    user = User(
        user_id=str(owner), username="alice", role="admin", status="active", created_at=NOW, updated_at=NOW
    )
    key = SshKey(
        key_id="SHA256:abc",
        fingerprint="SHA256:abc",
        user_id=owner,
        public_key="ssh-ed25519 AAAA alice@host",
        key_type="ssh-ed25519",
        added_at=NOW,
        revoked_at=None,
    )
    grant = Grant(
        grant_id=str(uuid4()),
        user_id=user.user_id,
        scope="doc_type",
        value="product",
        permission="write",
        granted_by=admin,
        granted_at=NOW,
    )
    session = Session(
        session_id=uuid4(),
        user_id=user.user_id,
        token_hash="b" * 64,
        created_at=NOW,
        expires_at=NOW + timedelta(hours=8),
        last_seen_at=NOW,
    )

    assert user.role == "admin"
    assert user.created_at == user.updated_at == NOW
    assert key.revoked_at is None
    assert key.user_id == owner
    assert grant.granted_by == admin
    assert grant.model_dump(by_alias=True)["grantedAt"] == NOW
    assert session.expires_at - session.created_at == timedelta(hours=8)

    with pytest.raises(ValidationError):
        User(user_id=str(uuid4()), username="bob", role="owner", status="active", created_at=NOW, updated_at=NOW)
    with pytest.raises(ValidationError):
        SshKey(
            key_id="k",
            fingerprint="f",
            user_id=owner,
            public_key="ssh-dss AAAA",
            key_type="ssh-dss",
            added_at=NOW,
            revoked_at=None,
        )
    with pytest.raises(ValidationError):
        Grant(grant_id="g", user_id="u", scope="repo", value="x", permission="write", granted_by=None, granted_at=NOW)
    with pytest.raises(ValidationError):
        Grant(grant_id="g", user_id="u", scope="doc", value="x", permission="admin", granted_by=None, granted_at=NOW)


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


# ── §3.0 / §4 DDL 字段契约（逐字一致，防后续漂移）───────────────────────

SPEC_FIELDS: dict[type, set[str]] = {
    # §3.0 公共类型定义（A14）
    WriteContext: {"actor", "source"},
    NodeIn: {"node_id", "doc_id", "atom_type", "format", "ordinal", "parent_node_id", "level", "anchor", "content"},
    Node: {"node_id", "doc_id", "atom_type", "format", "ordinal", "parent_node_id", "level", "anchor", "content", "status", "version", "created_at", "updated_at"},
    RawFallback: {"atom_type", "format", "text", "source_lines"},
    UnmappedBlock: {"source_lines", "reason", "fallback"},
    Proposal: {"proposal_id", "rule_id", "confident", "source_lines", "atom"},
    ParseStats: {"total_blocks", "rule_covered", "fallback", "pending"},
    ParseResult: {"doc_meta", "proposals", "unmapped", "stats"},
    Event: {"event_id", "entity", "entity_id", "op", "payload", "actor", "ts"},
    DocTypeTarget: {"kind", "value"},
    DocTarget: {"kind", "value"},
    Comment: {"comment_id", "node_id", "target_event_id", "body", "state", "author", "version", "ts"},
    NodeSnapshot: {"node", "history"},
    SearchHit: {"node_id", "doc_id", "anchor", "score"},
    TraversalHit: {"node_id", "doc_id", "anchor", "hops", "via"},
    RenderResult: {"doc_id", "out_path", "assets_exported"},
    CommitResult: {"doc_id", "nodes_created", "refs_created", "stats"},
    QualityReport: {"detector_id", "violations"},
    ExportResult: {"out_path", "docs", "nodes"},
    Violation: {"rule_id", "path", "message", "fix_hint"},
    DocIn: {"doc_id", "doc_type", "title", "meta", "source_ref"},
    Doc: {"doc_id", "doc_type", "title", "meta", "source_ref", "status", "version", "created_at", "updated_at"},
    AssetSyncReport: {"fetched", "missing", "total_refs"},
    QualityScope: {"doc_ids", "detectors"},
    # §4 DDL 推导（§3.0 未定义）
    Ref: {"ref_id", "src_node_id", "dst_doc_id", "dst_node_id", "kind"},
    SchemaDef: {"type_name", "json_schema", "version"},
    Asset: {"asset_id", "mime", "bytes", "origin", "path"},
    Term: {"term", "definition_node_id", "kind"},
    Session: {"session_id", "user_id", "token_hash", "created_at", "expires_at", "last_seen_at"},

    # §3 M10 + §4 DDL 补列（Main 裁决：M10/M02 回读三表全列）
    User: {"user_id", "username", "role", "status", "created_at", "updated_at"},
    SshKey: {"key_id", "fingerprint", "user_id", "public_key", "key_type", "added_at", "revoked_at"},
    Grant: {"grant_id", "user_id", "scope", "value", "permission", "granted_by", "granted_at"},

    # 基类与 doc_type 组合规则（REQ-M01-F03）
    Model: set(),
    DocTypeRule: {"doc_type", "allowed_atom_types", "required_atom_types", "required_meta_fields"},
}


def test_required_optionality_follows_spec_section_3_0():
    """§3.0 只在三处给了默认值（Node 继承 NodeIn 的 `format`）；`X | None` 仍为必填。
    例外：内部配置模型 DocTypeRule 的两个可选规则字段（不属 §3.0 传输类型）。"""
    allowed_defaults = {
        ("NodeIn", "format"),
        ("Node", "format"),
        ("DocTypeTarget", "kind"),
        ("DocTarget", "kind"),
        ("DocTypeRule", "required_atom_types"),
        ("DocTypeRule", "required_meta_fields"),
    }
    for model in SPEC_FIELDS:
        for name, field_info in model.model_fields.items():
            if field_info.is_required():
                continue
            assert (model.__name__, name) in allowed_defaults, f"{model.__name__}.{name} 意外有默认值"

    assert NodeIn.model_fields["format"].default == "md"
    assert DocTypeTarget.model_fields["kind"].default == "doc_type"
    assert DocTarget.model_fields["kind"].default == "doc"

    required_but_nullable = (
        (NodeIn, "node_id"),
        (NodeIn, "parent_node_id"),
        (NodeIn, "level"),
        (DocIn, "source_ref"),
        (Ref, "dst_node_id"),
        (Violation, "fix_hint"),
        (SshKey, "revoked_at"),
        (Grant, "granted_by"),
    )
    for model, name in required_but_nullable:
        assert model.model_fields[name].is_required(), f"{model.__name__}.{name} 应为必填"


def test_camel_case_aliases_are_derived_uniformly():
    from pydantic.alias_generators import to_camel

    for model in SPEC_FIELDS:
        for name, field_info in model.model_fields.items():
            assert field_info.alias == to_camel(name)


def test_contract_table_covers_every_public_model():
    """契约表必须与包导出的模型一一对应——防止新增模型或漏改条目导致约束静默失效。"""
    import agenticdocer.model as model_pkg

    public_models = {
        getattr(model_pkg, name)
        for name in model_pkg.__all__
        if isinstance(getattr(model_pkg, name), type) and issubclass(getattr(model_pkg, name), BaseModel)
    }

    assert public_models == set(SPEC_FIELDS)
