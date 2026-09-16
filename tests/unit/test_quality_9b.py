"""M09B 单测：detector 登记/调度 + 六个 detector 的判据（纯函数层，**不碰数据库**）。

真实缺陷注入在 `tests/integration/test_quality_gate.py`（真库 + 人为破坏数据）；本文件覆盖
「行/报告 → 违规」的判定逻辑、种子解析、往返差异比较与 detector 注册表自证——包括
「登记了但永不触发」的死规则检测（逐模块 `RULES_*` 覆盖测）。
"""

from __future__ import annotations

import datetime as dt
from types import SimpleNamespace
from typing import Any

import pytest

from agenticdocer.m09.quality_9b import (
    DETECTORS,
    DETECTOR_IDS,
    assets_missing,
    broken_refs,
    build_context,
    detector_ids,
    events_consistency,
    get_detector,
    perf_health,
    render_consistency,
    resolve_detectors,
    terms,
)
from agenticdocer.model import Doc, Event, Node, QualityScope, Violation, new_uuid7
from agenticdocer.observability import (
    IndexHealth,
    PartitionHealth,
    PoolHealth,
    TableHealth,
    evaluate_health,
)
from agenticdocer.render import NormalForm, TableNF
from agenticdocer.store import ValidationError, apply_events, field_deltas, now

DOC_ID = "SPEC-STD-AMBA-APB"
STUB_STORAGE = SimpleNamespace(db=SimpleNamespace(url="postgresql+asyncpg://app@db/test"))


# ── 夹具构造器 ────────────────────────────────────────────────────────────


def make_node(**overrides: Any) -> Node:
    fields: dict[str, Any] = {
        "node_id": new_uuid7(),
        "doc_id": DOC_ID,
        "atom_type": "clause",
        "format": "md",
        "ordinal": 1,
        "parent_node_id": None,
        "level": 1,
        "anchor": f"{DOC_ID}#1·overview",
        "content": {"text": "body", "fragment": "## 1 Overview"},
        "status": "active",
        "version": 1,
        "created_at": now(),
        "updated_at": now(),
    }
    fields.update(overrides)
    return Node(**fields)


def make_doc(**overrides: Any) -> Doc:
    fields: dict[str, Any] = {
        "doc_id": DOC_ID,
        "doc_type": "standard",
        "title": "AMBA APB",
        "meta": {"spec_revision": "2.0"},
        "source_ref": "IHI0024",
        "status": "draft",
        "version": 1,
        "created_at": now(),
        "updated_at": now(),
    }
    fields.update(overrides)
    return Doc(**fields)


def create_event(entity: str, record: dict[str, Any], entity_id: str | None = None) -> Event:
    """真实形态的 create 事件（载荷 = M02 `field_deltas` 全量口径）。"""
    return Event(
        event_id=new_uuid7(),
        entity=entity,  # type: ignore[arg-type]
        entity_id=entity_id or str(record.get(f"{entity}_id") or record["node_id"]),
        op="create",
        payload=field_deltas({}, record, include_unchanged=True),
        actor="tester",
        ts=now(),
    )


def ref_row(**overrides: Any) -> dict[str, Any]:
    row = {
        "ref_id": new_uuid7(),
        "src_node_id": new_uuid7(),
        "dst_doc_id": DOC_ID,
        "dst_node_id": None,
        "kind": "see_also",
        "src_found": new_uuid7(),
        "src_status": "active",
        "dst_found": None,
        "dst_status": None,
        "dst_node_doc_id": None,
        "dst_doc_found": DOC_ID,
    }
    row.update(overrides)
    return row


# ── 注册表与作用域（§3 M09 `detector_id` 取值域）──────────────────────────


def test_detector_registry_matches_spec() -> None:
    assert DETECTOR_IDS == (
        "broken_refs",
        "terms",
        "assets_missing",
        "render_consistency",
        "events_consistency",
        "perf_health",
    )
    assert tuple(DETECTORS) == DETECTOR_IDS
    assert detector_ids() == DETECTOR_IDS
    assert all(callable(item) for item in DETECTORS.values())


def test_get_detector_unknown_lists_registered() -> None:
    with pytest.raises(ValidationError) as excinfo:
        get_detector("nope")
    assert "broken_refs" in str(excinfo.value)


def test_resolve_detectors_normalizes_order_and_dedupes() -> None:
    assert resolve_detectors(None) == DETECTOR_IDS
    assert resolve_detectors(["terms", "broken_refs", "terms"]) == ("broken_refs", "terms")
    with pytest.raises(ValidationError):
        resolve_detectors(["broken_refs", "ghost"])


def test_build_context_derives_scope_and_dsn() -> None:
    context, selected = build_context(None, storage=STUB_STORAGE)  # type: ignore[arg-type]
    assert context.doc_ids is None
    assert context.dsn == STUB_STORAGE.db.url
    assert selected == DETECTOR_IDS

    scoped, selected = build_context(
        QualityScope(doc_ids=[DOC_ID], detectors=["perf_health"]),
        storage=STUB_STORAGE,  # type: ignore[arg-type]
        dsn="postgresql://other/db",
    )
    assert scoped.doc_ids == (DOC_ID,)
    assert scoped.dsn == "postgresql://other/db"
    assert selected == ("perf_health",)


def test_quality_scope_requires_scoped_detector_route() -> None:
    """`QualityScope` 只承载 doc_ids/detectors 两字段（§3.0），未知 detector 在执行前被拒。"""
    reports = QualityScope(doc_ids=None, detectors=[])
    assert resolve_detectors(reports.detectors) == ()


# ── terms：种子解析 ───────────────────────────────────────────────────────


def test_repo_seed_is_normative_keywords_only() -> None:
    seeded = terms.load_seed()
    assert len(seeded) >= 11
    assert {item.kind for item in seeded} == {"normative-keyword"}
    assert {"MUST", "MUST NOT", "SHOULD", "MAY"} <= {item.term for item in seeded}


def test_seed_path_precedence(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setenv("TERMS_SEED", str(tmp_path / "env.yaml"))
    assert terms.seed_path() == tmp_path / "env.yaml"
    assert terms.seed_path(tmp_path / "explicit.yaml") == tmp_path / "explicit.yaml"


def test_load_seed_reads_valid_file(tmp_path) -> None:
    path = tmp_path / "seed.yaml"
    path.write_text("version: 1\nterms:\n  - {term: GLOSSARY, kind: glossary}\n", encoding="utf-8")
    assert terms.load_seed(path) == [terms.SeedTerm(term="GLOSSARY", kind="glossary")]


@pytest.mark.parametrize(
    ("body", "label"),
    [
        ("terms:\n  - {term: A, kind: nope}\n", "非法 kind"),
        ("terms:\n  - {kind: glossary}\n", "缺 term"),
        ("terms:\n  - {term: A, kind: glossary}\n  - {term: A, kind: glossary}\n", "重复 term"),
        ("terms: {}\n", "terms 非列表"),
        ("- a\n", "顶层非映射"),
        ("terms: [1,2\n", "YAML 语法错误"),
    ],
)
def test_load_seed_rejects_malformed(tmp_path, body: str, label: str) -> None:
    path = tmp_path / "seed.yaml"
    path.write_text(body, encoding="utf-8")
    with pytest.raises(ValidationError):
        terms.load_seed(path)
    assert label


def test_load_seed_missing_file_raises(tmp_path) -> None:
    with pytest.raises(ValidationError) as excinfo:
        terms.load_seed(tmp_path / "absent.yaml")
    assert "不存在" in str(excinfo.value)


# ── terms：判据 ───────────────────────────────────────────────────────────


def term_row(term: str = "Anchor", **overrides: Any) -> dict[str, Any]:
    row: dict[str, Any] = {"term": term, "definition_node_id": new_uuid7(), "kind": "glossary"}
    row.update(overrides)
    return row


LINKED_RULES: set[str] = set()


@pytest.mark.parametrize(
    ("row", "expected"),
    [
        (
            {
                "term": "Anchor",
                "definition_node_id": new_uuid7(),
                "kind": "glossary",
                "node_found": None,
                "node_status": None,
                "node_atom_type": None,
            },
            terms.RULE_TERMS_DANGLING,
        ),
        (
            {
                "term": "Anchor",
                "definition_node_id": new_uuid7(),
                "kind": "glossary",
                "node_found": new_uuid7(),
                "node_status": "deleted",
                "node_atom_type": "definition",
            },
            terms.RULE_TERMS_DANGLING,
        ),
        (
            {
                "term": "Anchor",
                "definition_node_id": new_uuid7(),
                "kind": "glossary",
                "node_found": new_uuid7(),
                "node_status": "active",
                "node_atom_type": "note",
            },
            terms.RULE_TERMS_NODE_NOT_DEFINITION,
        ),
    ],
)
def test_judge_definition_dangling_and_atom_type(row: dict, expected: str) -> None:
    violations = terms.judge_definition_dangling([row])
    assert [item.rule_id for item in violations] == [expected]
    assert violations[0].fix_hint


def test_judge_definition_dangling_clean() -> None:
    linked = {
        "term": "Anchor",
        "definition_node_id": new_uuid7(),
        "kind": "glossary",
        "node_found": new_uuid7(),
        "node_status": "active",
        "node_atom_type": "definition",
    }
    assert terms.judge_definition_dangling([linked]) == []


def test_judge_kind_requires_glossary_when_bound() -> None:
    bound_keyword = term_row("MUST", kind="normative-keyword")
    unbound_keyword = term_row("MUST", definition_node_id=None, kind="normative-keyword")
    assert [item.rule_id for item in terms.judge_kind([bound_keyword])] == [terms.RULE_TERMS_KIND]
    assert terms.judge_kind([unbound_keyword]) == []
    assert terms.judge_kind([term_row()]) == []


def test_judge_unregistered_flags_definition_without_term_row() -> None:
    definitions = [{"node_id": str(new_uuid7()), "doc_id": DOC_ID, "term": "Anchor"}]
    violations = terms.judge_unregistered(definitions, [term_row("Other")])
    assert [item.rule_id for item in violations] == [terms.RULE_TERMS_UNREGISTERED]
    assert "upsert_term" in violations[0].fix_hint
    assert violations[0].path.endswith("#content.term")
    assert terms.judge_unregistered(definitions, [term_row("Anchor")]) == []
    assert terms.judge_unregistered([{"node_id": "n", "doc_id": DOC_ID, "term": None}], []) == []


def test_judge_seed_reports_missing_and_kind_drift() -> None:
    seeded = [terms.SeedTerm(term="MUST", kind="normative-keyword")]
    missing = terms.judge_seed(seeded, [])
    assert [item.rule_id for item in missing] == [terms.RULE_TERMS_SEED_MISSING]
    assert "TERMS_SEED" in missing[0].message

    drift = terms.judge_seed(seeded, [term_row("MUST", definition_node_id=None, kind="glossary")])
    assert [item.rule_id for item in drift] == [terms.RULE_TERMS_KIND]

    assert terms.judge_seed(seeded, [term_row("MUST", definition_node_id=None)]) == []


def test_terms_rules_are_all_reachable() -> None:
    """死规则检测：`RULES_TERMS` 每条都被上面的用例命中。"""
    detected = {
        terms.RULE_TERMS_DANGLING,
        terms.RULE_TERMS_NODE_NOT_DEFINITION,
        terms.RULE_TERMS_KIND,
        terms.RULE_TERMS_UNREGISTERED,
        terms.RULE_TERMS_SEED_MISSING,
    }
    assert detected == set(terms.RULES_TERMS)


# ── broken_refs：判据（ADR-009 降级外键兜底）──────────────────────────────


def test_judge_refs_source_side() -> None:
    missing = broken_refs.judge_refs([ref_row(src_found=None, src_status=None)])
    assert [item.rule_id for item in missing] == [broken_refs.RULE_REF_SRC_DANGLING]

    deleted = broken_refs.judge_refs([ref_row(src_status="deleted")])
    assert [item.rule_id for item in deleted] == [broken_refs.RULE_REF_SRC_DELETED]

    assert broken_refs.judge_refs([ref_row()]) == []


@pytest.mark.parametrize(
    ("row", "expected"),
    [
        ({"dst_node_id": new_uuid7(), "dst_found": None}, broken_refs.RULE_REF_DST_DANGLING),
        (
            {"dst_node_id": new_uuid7(), "dst_found": new_uuid7(), "dst_status": "deleted"},
            broken_refs.RULE_REF_DST_DELETED,
        ),
        (
            {
                "dst_node_id": new_uuid7(),
                "dst_found": new_uuid7(),
                "dst_node_doc_id": "SPEC-OTHER",
            },
            broken_refs.RULE_REF_DST_DOC_MISMATCH,
        ),
        ({"dst_doc_found": None, "dst_doc_id": "SPEC-MISSING"}, broken_refs.RULE_REF_DST_DOC_MISSING),
    ],
)
def test_judge_refs_target_side(row: dict, expected: str) -> None:
    violations = broken_refs.judge_refs([ref_row(**row)])
    assert [item.rule_id for item in violations] == [expected]
    assert violations[0].fix_hint


def test_judge_refs_accepts_external_leaf_and_internal_doc() -> None:
    external = ref_row(dst_doc_id="EXT:https://example.com/spec", dst_doc_found=None)
    internal = ref_row(dst_node_id=new_uuid7(), dst_found=new_uuid7(), dst_node_doc_id=DOC_ID)
    assert broken_refs.judge_refs([external, internal]) == []


def test_judge_parents() -> None:
    dangling = broken_refs.judge_parents(
        [{"node_id": new_uuid7(), "doc_id": DOC_ID, "parent_node_id": new_uuid7(), "parent_found": None, "parent_status": None}]
    )
    assert [item.rule_id for item in dangling] == [broken_refs.RULE_NODE_PARENT_DANGLING]

    deleted = broken_refs.judge_parents(
        [
            {
                "node_id": new_uuid7(),
                "doc_id": DOC_ID,
                "parent_node_id": new_uuid7(),
                "parent_found": new_uuid7(),
                "parent_status": "deleted",
            }
        ]
    )
    assert [item.rule_id for item in deleted] == [broken_refs.RULE_NODE_PARENT_DELETED]

    ok = broken_refs.judge_parents(
        [
            {
                "node_id": new_uuid7(),
                "doc_id": DOC_ID,
                "parent_node_id": new_uuid7(),
                "parent_found": new_uuid7(),
                "parent_status": "active",
            }
        ]
    )
    assert ok == []


def comment_row(**overrides: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "comment_id": new_uuid7(),
        "node_id": new_uuid7(),
        "state": "open",
        "target_event_id": None,
        "node_found": new_uuid7(),
        "node_status": "active",
        "event_found": None,
    }
    row.update(overrides)
    return row


def test_judge_comments() -> None:
    dangling = broken_refs.judge_comments([comment_row(node_found=None, node_status=None)])
    assert [item.rule_id for item in dangling] == [broken_refs.RULE_COMMENT_NODE_DANGLING]

    deleted_open = broken_refs.judge_comments([comment_row(node_status="deleted")])
    assert [item.rule_id for item in deleted_open] == [broken_refs.RULE_COMMENT_NODE_DELETED]

    # 已 resolve 的批注挂在软删节点上是合法状态（orphan_comments 只处理 open）
    assert broken_refs.judge_comments([comment_row(node_status="deleted", state="resolved")]) == []

    event_gone = broken_refs.judge_comments([comment_row(target_event_id=new_uuid7())])
    assert [item.rule_id for item in event_gone] == [broken_refs.RULE_COMMENT_EVENT_DANGLING]

    assert broken_refs.judge_comments([comment_row(target_event_id=new_uuid7(), event_found=new_uuid7())]) == []


def test_broken_refs_rules_are_all_reachable() -> None:
    rows = [
        ref_row(src_found=None, src_status=None),
        ref_row(src_status="deleted"),
        ref_row(dst_node_id=new_uuid7(), dst_found=None),
        ref_row(dst_node_id=new_uuid7(), dst_found=new_uuid7(), dst_status="deleted"),
        ref_row(dst_doc_found=None),
        ref_row(dst_node_id=new_uuid7(), dst_found=new_uuid7(), dst_node_doc_id="SPEC-OTHER"),
    ]
    detected = {item.rule_id for item in broken_refs.judge_refs(rows)}
    detected |= {
        item.rule_id
        for item in broken_refs.judge_parents(
            [
                {"node_id": new_uuid7(), "doc_id": DOC_ID, "parent_node_id": new_uuid7(), "parent_found": None, "parent_status": None},
                {
                    "node_id": new_uuid7(),
                    "doc_id": DOC_ID,
                    "parent_node_id": new_uuid7(),
                    "parent_found": new_uuid7(),
                    "parent_status": "deleted",
                },
            ]
        )
    }
    detected |= {
        item.rule_id
        for item in broken_refs.judge_comments(
            [
                comment_row(node_found=None, node_status=None),
                comment_row(node_status="deleted"),
                comment_row(target_event_id=new_uuid7()),
            ]
        )
    }
    assert detected == set(broken_refs.RULES_BROKEN_REFS)


# ── assets_missing（判据已委托 M02，测映射与定位）──────────────────────────


def test_judge_missing_sorts_dedupes_and_scopes_path() -> None:
    global_scope = assets_missing.judge_missing(["b" * 64, "a" * 64, "a" * 64])
    assert [item.path for item in global_scope] == [f"assets/{'a' * 64}", f"assets/{'b' * 64}"]
    scoped = assets_missing.judge_missing(["a" * 64], DOC_ID)
    assert scoped[0].path == f"{DOC_ID}#assets/{'a' * 64}"
    assert scoped[0].rule_id == assets_missing.RULE_ASSET_MISSING
    assert scoped[0].fix_hint
    assert assets_missing.judge_missing([]) == []
    assert set(assets_missing.RULES_ASSETS_MISSING) == {assets_missing.RULE_ASSET_MISSING}


# ── render_consistency：两式差异比较 ─────────────────────────────────────


def form(**overrides: Any) -> NormalForm:
    fields: dict[str, Any] = {
        "headings": [(1, "Overview")],
        "tables": [TableNF(rows=1, cols=2, cells=[["a", "b"]])],
        "code_blocks": ["echo"],
        "images": ["assets/" + "a" * 64],
        "lists": [["first", "second"]],
        "inline_markers": ["code"],
    }
    fields.update(overrides)
    return NormalForm(**fields)


def test_diff_forms_identical_is_clean() -> None:
    assert (
        render_consistency.diff_forms(
            form(),
            form(),
            rule_id=render_consistency.RULE_PARSE_DRIFT,
            path_prefix=DOC_ID,
            label="x",
            fix_hint="y",
        )
        == []
    )


@pytest.mark.parametrize("feature", render_consistency.DIFF_FEATURES)
def test_diff_forms_detects_each_feature(feature: str) -> None:
    altered = form(**{feature: [] if feature != "headings" else [(2, "Overview")]})
    violations = render_consistency.diff_forms(
        form(),
        altered,
        rule_id=render_consistency.RULE_PARSE_DRIFT,
        path_prefix=DOC_ID,
        label="解析保真",
        fix_hint="重解析并 commit",
    )
    assert [item.path for item in violations] == [f"{DOC_ID}#{feature}"]
    assert violations[0].rule_id == render_consistency.RULE_PARSE_DRIFT
    assert violations[0].fix_hint


def test_diff_forms_reports_length_mismatch_and_clips() -> None:
    altered = form(headings=[(1, "Overview"), (2, "Extra")])
    violations = render_consistency.diff_forms(
        form(),
        altered,
        rule_id=render_consistency.RULE_ARTIFACT_DRIFT,
        path_prefix=f"{DOC_ID}#artifact",
        label="渲染保真",
        fix_hint="重渲染",
    )
    assert len(violations) == 1
    assert "缺失" in violations[0].message
    assert violations[0].path == f"{DOC_ID}#artifact#headings"


def test_rendered_artifact_path_follows_render_out_dir(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("RENDER_OUT_DIR", str(tmp_path))
    assert render_consistency.rendered_artifact_path(DOC_ID) == tmp_path / f"{DOC_ID}.md"
    assert set(render_consistency.RULES_RENDER_CONSISTENCY) == {
        render_consistency.RULE_PARSE_DRIFT,
        render_consistency.RULE_ARTIFACT_DRIFT,
    }


# ── perf_health：HealthReport → 违规（判据来自 M12 的 verdict）─────────────


def health_report(**overrides: Any):
    fields: dict[str, Any] = {
        "tables": [TableHealth(name="nodes", rows=10, size_bytes=8192, dead_tup=0, last_autovacuum=None)],
        "indexes": [IndexHealth(name="idx_nodes_fts", scans=5, size_bytes=1024)],
        "partitions": PartitionHealth(events_next_missing=False, oldest_event_ts=now()),
        "pool": PoolHealth(size=0, checkedout=0, overflow=0),
    }
    fields.update(overrides)
    return evaluate_health(**fields)


def test_map_health_report_ok_has_no_violations() -> None:
    report = health_report()
    assert report.verdict == "ok"
    assert perf_health.map_health_report(report) == []


def test_map_health_report_partition_missing_and_verdict() -> None:
    report = health_report(
        partitions=PartitionHealth(events_next_missing=True, oldest_event_ts=now())
    )
    assert report.verdict == "fail"
    violations = perf_health.map_health_report(report)
    assert [item.rule_id for item in violations] == [
        perf_health.RULE_PARTITION_MISSING,
        perf_health.RULE_VERDICT,
    ]
    assert "CREATE TABLE" in violations[0].fix_hint
    assert violations[1].fix_hint


def test_map_health_report_degraded_carries_advice() -> None:
    """膨胀/未使用索引起的 degraded 由 M12 判定；fix_hint 原样承载 M12 的建议。"""
    report = health_report(
        tables=[
            TableHealth(
                name="nodes", rows=100_000, size_bytes=10**9, dead_tup=60_000, last_autovacuum=None
            )
        ],
        indexes=[IndexHealth(name="idx_unused", scans=0, size_bytes=20 * 1024 * 1024)],
    )
    assert report.verdict == "degraded"
    violations = perf_health.map_health_report(report)
    assert [item.rule_id for item in violations] == [perf_health.RULE_VERDICT]
    assert "VACUUM" in violations[0].fix_hint
    assert "DROP INDEX" in violations[0].fix_hint
    assert set(perf_health.RULES_PERF_HEALTH) == {
        perf_health.RULE_PARTITION_MISSING,
        perf_health.RULE_VERDICT,
    }


# ── events_consistency：重放 vs 当前态 ────────────────────────────────────


def test_judge_nodes_clean_roundtrip() -> None:
    node = make_node()
    history = {str(node.node_id): [create_event("node", node.model_dump())]}
    assert events_consistency.judge_nodes([node], history) == []


def test_judge_nodes_detects_tampered_current_state() -> None:
    node = make_node()
    history = {str(node.node_id): [create_event("node", node.model_dump())]}
    tampered = node.model_copy(update={"content": {"text": "hand-edited"}, "version": 5})
    violations = events_consistency.judge_nodes([tampered], history)
    fields = {item.path.rsplit("#", 1)[1] for item in violations}
    assert fields == {"content", "version"}
    assert {item.rule_id for item in violations} == {events_consistency.RULE_NODE_DRIFT}
    assert all(item.fix_hint for item in violations)


def test_judge_nodes_detects_tampered_event_history() -> None:
    """篡改事件：追加一条伪造的 update 事件 → 重放结果与当前态不一致即命中。"""
    node = make_node()
    forged = Event(
        event_id=new_uuid7(),
        entity="node",
        entity_id=str(node.node_id),
        op="update",
        payload={"content": {"before": node.content, "after": {"text": "forged"}}},
        actor="tester",
        ts=now(),
    )
    violations = events_consistency.judge_nodes(
        [node], {str(node.node_id): [create_event("node", node.model_dump()), forged]}
    )
    assert [item.path for item in violations] == [f"nodes/{node.node_id}#content"]
    assert violations[0].rule_id == events_consistency.RULE_NODE_DRIFT
    assert "重放" in violations[0].message


def test_judge_nodes_missing_or_incomplete_history() -> None:
    node = make_node()
    no_events = events_consistency.judge_nodes([node], {})
    assert [item.rule_id for item in no_events] == [events_consistency.RULE_NO_CREATE]

    update_only = Event(
        event_id=new_uuid7(),
        entity="node",
        entity_id=str(node.node_id),
        op="update",
        payload={"content": {"before": node.content, "after": {"text": "b"}}},
        actor="tester",
        ts=now(),
    )
    incomplete = events_consistency.judge_nodes([node], {str(node.node_id): [update_only]})
    assert [item.rule_id for item in incomplete] == [events_consistency.RULE_NO_CREATE]
    assert "缺字段" in incomplete[0].message


def test_judge_nodes_invalid_op_is_reported_not_raised() -> None:
    node = make_node()
    bad = Event(
        event_id=new_uuid7(),
        entity="node",
        entity_id=str(node.node_id),
        op="add",
        payload={"content": {"before": None, "after": {"text": "x"}}},
        actor="tester",
        ts=now(),
    )
    violations = events_consistency.judge_nodes([node], {str(node.node_id): [bad]})
    assert [item.rule_id for item in violations] == [events_consistency.RULE_OP_INVALID]
    assert violations[0].fix_hint


def test_judge_docs_clean_drift_and_missing() -> None:
    doc = make_doc()
    history = {doc.doc_id: [create_event("doc", doc.model_dump(), entity_id=doc.doc_id)]}
    assert events_consistency.judge_docs([doc], history) == []

    tampered = doc.model_copy(update={"title": "edited"})
    drift = events_consistency.judge_docs([tampered], history)
    assert [(item.rule_id, item.path) for item in drift] == [
        (events_consistency.RULE_DOC_DRIFT, f"docs/{DOC_ID}#title")
    ]

    assert [item.rule_id for item in events_consistency.judge_docs([doc], {})] == [
        events_consistency.RULE_NO_CREATE
    ]


def test_judge_docs_reports_incomplete_fold() -> None:
    doc = make_doc()
    partial = Event(
        event_id=new_uuid7(),
        entity="doc",
        entity_id=doc.doc_id,
        op="update",
        payload={"title": {"before": "a", "after": "b"}},
        actor="tester",
        ts=now(),
    )
    violations = events_consistency.judge_docs([doc], {doc.doc_id: [partial]})
    assert [item.rule_id for item in violations] == [events_consistency.RULE_NO_CREATE]
    assert "缺字段" in violations[0].message


def test_judge_orphans_and_cap() -> None:
    extra = str(new_uuid7())
    history = {extra: [create_event("node", make_node().model_dump(), entity_id=extra)]}
    violations = events_consistency.judge_orphans(history, set(), entity="node")
    assert [(item.rule_id, item.path) for item in violations] == [
        (events_consistency.RULE_ORPHAN, f"nodes/{extra}")
    ]
    assert events_consistency.judge_orphans(history, {extra}, entity="node") == []

    many = {str(new_uuid7()): [] for _ in range(events_consistency.MAX_ORPHAN_REPORTS + 5)}
    assert len(events_consistency.judge_orphans(many, set(), entity="node")) == (
        events_consistency.MAX_ORPHAN_REPORTS
    )


def test_events_consistency_fold_uses_m02_apply_events() -> None:
    """折叠口径来自 M02（P5：不另写折叠逻辑）——用真实 `apply_events` 交叉验证一次。"""
    node = make_node()
    events = [create_event("node", node.model_dump())]
    snapshot = apply_events("node", events)
    assert snapshot.node is not None
    assert snapshot.node.model_dump() == node.model_dump()


def test_events_rules_are_all_reachable() -> None:
    node = make_node()
    bad = Event(
        event_id=new_uuid7(),
        entity="node",
        entity_id=str(node.node_id),
        op="add",
        payload={},
        actor="tester",
        ts=now(),
    )
    detected = {
        item.rule_id
        for item in events_consistency.judge_nodes(
            [node.model_copy(update={"version": 9})],
            {str(node.node_id): [create_event("node", node.model_dump())]},
        )
    }
    detected |= {item.rule_id for item in events_consistency.judge_nodes([node], {})}
    detected |= {item.rule_id for item in events_consistency.judge_nodes([node], {str(node.node_id): [bad]})}
    detected |= {
        item.rule_id
        for item in events_consistency.judge_orphans({str(new_uuid7()): []}, set(), entity="node")
    }
    assert detected == set(events_consistency.RULES_EVENTS_CONSISTENCY)


def test_violation_shape_is_mechanical() -> None:
    """全部判据产物同形：`rule_id` + 非空 `path` + `message` + `fix_hint`（M06 消费口径）。"""
    samples: list[Violation] = [
        *broken_refs.judge_refs([ref_row(src_found=None, src_status=None)]),
        *terms.judge_seed([terms.SeedTerm(term="MUST", kind="normative-keyword")], []),
        *assets_missing.judge_missing(["a" * 64]),
        *render_consistency.diff_forms(
            form(),
            form(headings=[(2, "x")]),
            rule_id=render_consistency.RULE_PARSE_DRIFT,
            path_prefix=DOC_ID,
            label="解析保真",
            fix_hint="重解析",
        ),
        *perf_health.map_health_report(health_report()),
    ]
    assert samples
    for item in samples:
        assert item.rule_id and "." in item.rule_id
        assert item.path and item.message and item.fix_hint


def test_no_llm_or_network_imports_in_m09() -> None:
    """P6：M09 不引入 LLM/网络客户端（静态断言模块清单）。"""
    import agenticdocer.m09.engine_9a as engine
    import agenticdocer.m09.quality_9b.gate as gate

    banned = {"openai", "anthropic", "httpx", "requests", "urllib.request"}
    for module in (engine, gate):
        source = Path(module.__file__).read_text(encoding="utf-8")  # type: ignore[arg-type]
        assert not any(f"import {name}" in source for name in banned)
    _ = dt.datetime
