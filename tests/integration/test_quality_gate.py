"""M09B 集成测试：真库 + **人为制造缺陷**，验证 detector 真实检出（REQ-M09-F02 / ADR-009）。

每个用例先建一份「干净样本」（源 md + 文档 + 节点，全部经 M02 正规写入路径），断言质量门
零违规，然后**破坏数据**再断言命中——「能检出」与「不误报」两侧都被验证。

覆盖的注入手法（与生产故障形态对应）：

| detector | 注入 | 对应真实故障 |
|---|---|---|
| `broken_refs` | 软删引用目标 / 建悬空目标边 / 软删源节点 | ADR-009 外键降级（DB 不再兜底） |
| `events_consistency` | 直接 INSERT 伪造事件 / 直接 UPDATE 绕过事件写节点 | P2「事件与实体同事务」被绕过 |
| `terms` | definition 原子的术语未登记 / 词条绑定悬空节点 | R10 词表与内容模型脱钩 |
| `assets_missing` | figure 引用无 `assets` 行与字节的 sha256 | A6 取件缺失（M03 漏件） |
| `render_consistency` | 软删表格节点（判据 a）/ 篡改渲染产物（判据 b） | 导入丢结构 / 产物层破坏 |
| `perf_health` | 无法在应用角色下制造（分区属 DDL）→ 用实时 `health()` 交叉校验判据一致性 | ADR-010 容量巡检 |
| `doc_type_schema_conformance` | 直接写 `docs` 行（绕过 M03 frontmatter 校验）使 `meta` 缺该 `doc_type` 必填字段 | 规则细化后既有文档未回溯（Q6/B7 裁剪的沉淀） |

样本一律用唯一 `doc_id`（`SPEC-QG<n>`），按 doc_ids 作用域断言，故可与其他 agent 的数据共存；
但**本文件依赖 `conftest.migrated_schema`**（会 drop/recreate schema），仍须独占运行。
"""

from __future__ import annotations

import asyncio
import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
from sqlalchemy import delete, insert, update
from sqlalchemy.dialects.postgresql import insert as pg_insert

from agenticdocer.m09 import DETECTOR_IDS, run_quality_gate, run_quality_gate_sync
from agenticdocer.m09.quality_9b import (
    assets_missing,
    broken_refs,
    doc_type_conformance,
    events_consistency,
    perf_health,
    render_consistency,
    section_range_consistency,
    terms,
)
from agenticdocer.model import (
    C5_META_FIELDS,
    DocIn,
    Node,
    NodeIn,
    QualityScope,
    Violation,
    WriteContext,
    derive_text,
    new_uuid7,
)
from agenticdocer.observability import health
from agenticdocer.render import render_document, table_meta
from agenticdocer.store import Storage, ValidationError, now
from agenticdocer.store.schema import events as events_table
from agenticdocer.store.schema import nodes as nodes_table
from agenticdocer.store.schema import terms as terms_table

pytestmark = pytest.mark.integration

CTX = WriteContext(actor="m09-tester", source="cli")
_SEQ = itertools.count(1)
_RUN = new_uuid7().hex[:12]
"""本次测试运行的唯一后缀：`doc_id` 跨**运行**唯一（锚唯一约束 `(doc_id, anchor)` 要求如此——
库不清空时，仅按进程内计数会与上一轮运行冲突）。"""

CLAUSE_FRAGMENT = "## 1 Overview\n\nThis is the overview body."
TABLE_FRAGMENT = "| a | b |\n| --- | --- |\n| 1 | 2 |"
TABLE_CELLS = [["a", "b"], ["1", "2"]]


@dataclass(frozen=True)
class Sample:
    """干净样本：源 md（判据 a/b 的源侧）、文档、两个节点。"""

    doc_id: str
    source: Path
    clause: Node
    table: Node


# ── 夹具 ─────────────────────────────────────────────────────────────────


@pytest.fixture
async def seeded_terms(storage: Storage) -> int:
    """把 `TERMS_SEED` 载入 `terms` 表（模拟 §5「种子随 migrate 载入」的写入路径），
    并清掉**本测试自己**在上一轮运行留下的 `Ghost-Term*` 残行。

    `terms` 数据面无 doc 维度（判据恒定全表），故「干净样本」断言要求本测试拥有自己的
    命名空间：`Ghost-Term*` 只由本文件写入。
    """
    rows = [
        {"term": item.term, "definition_node_id": None, "kind": item.kind}
        for item in terms.load_seed()
    ]
    async with storage.db.transaction() as session:
        await session.execute(delete(terms_table).where(terms_table.c.term.like("Ghost-Term%")))
        await session.execute(
            pg_insert(terms_table).values(rows).on_conflict_do_nothing(index_elements=["term"])
        )
    return len(rows)


@pytest.fixture
async def sample(storage: Storage, tmp_path: Path, seeded_terms: int) -> Sample:
    return await make_sample(storage, tmp_path)


async def make_sample(storage: Storage, tmp_path: Path) -> Sample:
    """建一份干净样本：源 md 与库内节点树**逐块镜像**（判据 a 应当成立）。"""
    index = next(_SEQ)
    doc_id = f"SPEC-QG-{_RUN}-{index}"
    source = tmp_path / f"qg-{_RUN}-{index}.md"
    source.write_text(
        "---\n"
        f"doc_id: {doc_id}\n"
        "doc_type: standard\n"
        "title: M09 Quality Gate Sample\n"
        "---\n\n"
        f"{CLAUSE_FRAGMENT}\n\n{TABLE_FRAGMENT}\n",
        encoding="utf-8",
    )
    doc = await storage.upsert_doc(
        DocIn(
            doc_id=doc_id,
            doc_type="standard",
            title="M09 Quality Gate Sample",
            meta={"source_path": str(source), "doc_slug": f"qg-{_RUN}-{index}"},
            source_ref=None,
        ),
        None,
        CTX,
    )
    clause = await add_node(
        storage,
        doc_id=doc.doc_id,
        atom_type="clause",
        ordinal=1,
        level=1,
        anchor=f"{doc_id}#1·overview",
        content={"fragment": CLAUSE_FRAGMENT},
    )
    table = await add_node(
        storage,
        doc_id=doc.doc_id,
        atom_type="table",
        ordinal=2,
        level=None,
        anchor=f"{doc_id}#2·table",
        content={"fragment": TABLE_FRAGMENT, "meta": table_meta(TABLE_CELLS)},
    )
    return Sample(doc_id=doc.doc_id, source=source, clause=clause, table=table)


async def add_node(
    storage: Storage,
    *,
    doc_id: str,
    atom_type: str,
    ordinal: int,
    level: int | None,
    anchor: str,
    content: dict[str, Any],
    fmt: str = "md",
    parent: Node | None = None,
) -> Node:
    """经 M02 正规写入路径加节点（`content.text` 由 M01 `derive_text` 单点生成）。`parent` 供大纲用例建层级。"""
    payload = {**content, "text": derive_text(atom_type, content)}
    return await storage.upsert_node(
        NodeIn(
            node_id=None,
            doc_id=doc_id,
            atom_type=atom_type,
            format=fmt,  # type: ignore[arg-type]
            ordinal=ordinal,
            parent_node_id=parent.node_id if parent is not None else None,
            level=level,
            anchor=anchor,
            content=payload,
        ),
        None,
        CTX,
    )


async def gate(
    storage: Storage,
    doc_id: str,
    detectors: list[str] | None = None,
    *,
    dsn: str | None = None,
) -> dict[str, list[Violation]]:
    """跑质量门（按 doc_id 作用域），返回 `detector_id → violations`；`dsn` 供 perf_health 注入。"""
    reports = await run_quality_gate(
        QualityScope(doc_ids=[doc_id], detectors=detectors), storage=storage, dsn=dsn
    )
    return {report.detector_id: report.violations for report in reports}


def rules(violations: list[Violation]) -> set[str]:
    return {item.rule_id for item in violations}


DATA_DETECTORS = ["broken_refs", "terms", "assets_missing", "render_consistency", "events_consistency"]


# ── 基线：干净样本零违规（不误报）────────────────────────────────────────


async def test_clean_sample_passes_gate(storage: Storage, sample: Sample) -> None:
    """干净样本：五个数据面 detector 全空（`perf_health` 见下一用例）。

    四个 doc 维度的 detector 断言**绝对零违规**；`terms` 因词表无 doc 维度（种子/绑定悬空
    是**全局**判据），只断言「种子已载入（夹具负责）且无指向本样本的违规」——共享库里他人
    数据不属于本用例的断言范围（否则等于断言一个本用例不拥有的全局不变量）。
    """
    result = await gate(storage, sample.doc_id, DATA_DETECTORS)
    assert set(result) == set(DATA_DETECTORS)
    for detector_id, violations in result.items():
        if detector_id == "terms":
            assert terms.RULE_TERMS_SEED_MISSING not in rules(violations), violations
            assert not [item for item in violations if sample.doc_id in item.path], violations
            continue
        assert violations == [], f"{detector_id}: {violations}"


async def test_perf_health_matches_live_verdict(storage: Storage, sample: Sample) -> None:
    """`perf_health` 判据 = M12 `health()` 的实时 verdict（同一实现，ADR-010）。"""
    report = await health(dsn=storage.db.url)
    result = await gate(storage, sample.doc_id, ["perf_health"])
    violations = result["perf_health"]
    assert report.partitions.events_next_missing is False  # migrate 已建次月分区
    assert bool(violations) == (report.verdict != "ok")
    if violations:
        assert rules(violations) <= set(perf_health.RULES_PERF_HEALTH)


async def test_report_shape_is_mechanical(storage: Storage, sample: Sample) -> None:
    """报告结构：`QualityReport.detector_id` + 违规四要素（rule_id/path/message/fix_hint）。"""
    reports = await run_quality_gate(
        QualityScope(doc_ids=[sample.doc_id], detectors=DATA_DETECTORS), storage=storage
    )
    assert [report.detector_id for report in reports] == DATA_DETECTORS
    assert all(report.violations == [] for report in reports)


# ── broken_refs：ADR-009 降级外键兜底 ────────────────────────────────────


async def test_broken_refs_detects_deleted_target(storage: Storage, sample: Sample) -> None:
    """删引用目标（软删）→ `M09B.ref.dst_deleted`；删除前为干净对照。"""
    await storage.add_ref(sample.clause.node_id, sample.doc_id, sample.table.node_id, "see_also", CTX)
    assert (await gate(storage, sample.doc_id, ["broken_refs"]))["broken_refs"] == []

    await storage.delete_node(sample.table.node_id, sample.table.version, CTX)
    violations = (await gate(storage, sample.doc_id, ["broken_refs"]))["broken_refs"]
    assert broken_refs.RULE_REF_DST_DELETED in rules(violations)
    hit = next(item for item in violations if item.rule_id == broken_refs.RULE_REF_DST_DELETED)
    assert hit.path.startswith("refs/") and hit.fix_hint


async def test_broken_refs_detects_dangling_target_and_source(
    storage: Storage, sample: Sample
) -> None:
    """悬空目标节点（DB 无外键）与已软删的源节点都要命中。"""
    ghost = new_uuid7()
    await storage.add_ref(sample.clause.node_id, sample.doc_id, ghost, "traces_to", CTX)
    src_node = await add_node(
        storage,
        doc_id=sample.doc_id,
        atom_type="note",
        ordinal=3,
        level=None,
        anchor=f"{sample.doc_id}#3·note",
        content={"fragment": "- note"},
    )
    await storage.add_ref(src_node.node_id, sample.doc_id, sample.table.node_id, "see_also", CTX)
    await storage.delete_node(src_node.node_id, src_node.version, CTX)

    violations = (await gate(storage, sample.doc_id, ["broken_refs"]))["broken_refs"]
    assert {broken_refs.RULE_REF_DST_DANGLING, broken_refs.RULE_REF_SRC_DELETED} <= rules(violations)
    dangling = next(item for item in violations if item.rule_id == broken_refs.RULE_REF_DST_DANGLING)
    assert str(ghost) in dangling.message


async def test_broken_refs_detects_target_doc_mismatch(storage: Storage, sample: Sample) -> None:
    """`dst_doc_id` 与目标节点实际所属文档不符（边自相矛盾）。"""
    await storage.add_ref(sample.clause.node_id, "SPEC-OTHER-DOC", sample.table.node_id, "see_also", CTX)
    violations = (await gate(storage, sample.doc_id, ["broken_refs"]))["broken_refs"]
    assert broken_refs.RULE_REF_DST_DOC_MISMATCH in rules(violations)


# ── events_consistency：events 重放 vs 当前态（P2 兼底）──────────────────


async def test_events_consistency_detects_forged_event(storage: Storage, sample: Sample) -> None:
    """**篡改事件**：直接 INSERT 一条伪造 update 事件 → 重放与当前态不一致即命中。"""
    assert (await gate(storage, sample.doc_id, ["events_consistency"]))["events_consistency"] == []

    async with storage.db.transaction() as session:
        await session.execute(
            insert(events_table).values(
                event_id=new_uuid7(),
                entity="node",
                entity_id=str(sample.clause.node_id),
                op="update",
                payload={"content": {"before": sample.clause.content, "after": {"text": "forged"}}},
                actor="tester",
                ts=now(),
            )
        )
    violations = (await gate(storage, sample.doc_id, ["events_consistency"]))["events_consistency"]
    assert events_consistency.RULE_NODE_DRIFT in rules(violations)
    hit = next(item for item in violations if item.rule_id == events_consistency.RULE_NODE_DRIFT)
    assert hit.path == f"nodes/{sample.clause.node_id}#content"
    assert "重放" in hit.message and hit.fix_hint


async def test_events_consistency_detects_write_bypassing_events(
    storage: Storage, sample: Sample
) -> None:
    """绕过 M02 直接 UPDATE 节点（事件与实体不同事务）→ 重放漂移。"""
    async with storage.db.transaction() as session:
        await session.execute(
            update(nodes_table)
            .where(nodes_table.c.node_id == sample.table.node_id, nodes_table.c.doc_id == sample.doc_id)
            .values(content={**sample.table.content, "fragment": "tampered"})
        )
    violations = (await gate(storage, sample.doc_id, ["events_consistency"]))["events_consistency"]
    assert rules(violations) == {events_consistency.RULE_NODE_DRIFT}
    assert any(item.path.endswith("#content") for item in violations)


# ── terms：词表校验（R10）────────────────────────────────────────────────


async def test_terms_detects_unregistered_and_dangling(storage: Storage, sample: Sample) -> None:
    """未登记术语 + 绑定悬空节点的词条各命中一条判据。"""
    assert (await gate(storage, sample.doc_id, ["terms"]))["terms"] == []

    definition = await add_node(
        storage,
        doc_id=sample.doc_id,
        atom_type="definition",
        ordinal=4,
        level=None,
        anchor=f"{sample.doc_id}#4·term",
        content={"term": "Unseeded-Term", "fragment": "Unseeded-Term: a term without a row."},
    )
    violations = (await gate(storage, sample.doc_id, ["terms"]))["terms"]
    assert [item.rule_id for item in violations] == [terms.RULE_TERMS_UNREGISTERED]
    assert violations[0].path == f"nodes/{definition.node_id}#content.term"
    assert "upsert_term" in violations[0].fix_hint

    async with storage.db.transaction() as session:
        await session.execute(
            insert(terms_table).values(
                term="Ghost-Term", definition_node_id=new_uuid7(), kind="glossary"
            )
        )
    violations = (await gate(storage, sample.doc_id, ["terms"]))["terms"]
    assert terms.RULE_TERMS_DANGLING in rules(violations)


# ── assets_missing：A6 取件缺失 ──────────────────────────────────────────


async def test_assets_missing_detects_unbacked_sha(storage: Storage, sample: Sample) -> None:
    """figure 引用的 sha256 无 `assets` 行与字节 → 命中；换成真实资产后为干净对照。"""
    absent = "c" * 64
    await add_node(
        storage,
        doc_id=sample.doc_id,
        atom_type="figure",
        ordinal=5,
        level=None,
        anchor=f"{sample.doc_id}#5·fig",
        content={"asset_ref": absent, "text": "Figure: timing", "caption": "timing"},
    )
    violations = (await gate(storage, sample.doc_id, ["assets_missing"]))["assets_missing"]
    assert rules(violations) == {assets_missing.RULE_ASSET_MISSING}
    assert violations[0].path == f"{sample.doc_id}#assets/{absent}"

    stored = await storage.put_asset(b"\x89PNG\r\n\x1a\ntest-bytes", "image/png", "M09 集成测试")
    await add_node(
        storage,
        doc_id=sample.doc_id,
        atom_type="figure",
        ordinal=6,
        level=None,
        anchor=f"{sample.doc_id}#6·fig",
        content={"asset_ref": stored, "text": "Figure: stored", "caption": "stored"},
    )
    remaining = (await gate(storage, sample.doc_id, ["assets_missing"]))["assets_missing"]
    assert [item.path for item in remaining] == [f"{sample.doc_id}#assets/{absent}"]


# ── render_consistency：两式（判据 a / b）───────────────────────────────


async def test_render_consistency_detects_parse_drift(storage: Storage, sample: Sample) -> None:
    """判据 a：库侧节点树与源不一致（软删表格节点）→ `M09B.render.parse_drift#tables`。"""
    assert (await gate(storage, sample.doc_id, ["render_consistency"]))["render_consistency"] == []

    await storage.delete_node(sample.table.node_id, sample.table.version, CTX)
    violations = (await gate(storage, sample.doc_id, ["render_consistency"]))["render_consistency"]
    assert render_consistency.RULE_PARSE_DRIFT in rules(violations)
    assert [item.path for item in violations if item.rule_id == render_consistency.RULE_PARSE_DRIFT] == [
        f"{sample.doc_id}#tables"
    ]


async def test_render_consistency_detects_artifact_drift(
    storage: Storage, sample: Sample, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """判据 b：产物文件与源不一致（篡改产物）→ `M09B.render.artifact_drift#headings`。"""
    monkeypatch.setenv("RENDER_OUT_DIR", str(tmp_path / "rendered"))
    await render_document(sample.doc_id, storage=storage)
    artifact = render_consistency.rendered_artifact_path(sample.doc_id)
    assert artifact.is_file()
    assert (await gate(storage, sample.doc_id, ["render_consistency"]))["render_consistency"] == []

    artifact.write_text(artifact.read_text(encoding="utf-8") + "\n## 9 Extra\n", encoding="utf-8")
    violations = (await gate(storage, sample.doc_id, ["render_consistency"]))["render_consistency"]
    assert render_consistency.RULE_ARTIFACT_DRIFT in rules(violations)
    assert [
        item.path for item in violations if item.rule_id == render_consistency.RULE_ARTIFACT_DRIFT
    ] == [f"{sample.doc_id}#artifact#headings"]


# ── detector 选择、作用域隔离与入口约束 ──────────────────────────────────


async def test_detector_selection_runs_only_selected(storage: Storage, sample: Sample) -> None:
    """`QualityScope.detectors` 可选过滤：只跑选定 detector（其余面即便有缺陷也不出现）。"""
    await storage.add_ref(sample.clause.node_id, sample.doc_id, new_uuid7(), "see_also", CTX)
    await add_node(
        storage,
        doc_id=sample.doc_id,
        atom_type="figure",
        ordinal=7,
        level=None,
        anchor=f"{sample.doc_id}#7·fig",
        content={"asset_ref": "d" * 64, "text": "Figure: missing"},
    )
    result = await gate(storage, sample.doc_id, ["broken_refs"])
    assert set(result) == {"broken_refs"}
    assert rules(result["broken_refs"]) == {broken_refs.RULE_REF_DST_DANGLING}
    full = await gate(storage, sample.doc_id, ["broken_refs", "assets_missing"])
    assert rules(full["broken_refs"]) == {broken_refs.RULE_REF_DST_DANGLING}
    assert rules(full["assets_missing"]) == {assets_missing.RULE_ASSET_MISSING}


async def test_scope_isolates_defects_between_documents(
    storage: Storage, sample: Sample, tmp_path: Path
) -> None:
    """缺陷在 A 文档，作用域到 B 文档 → 不报（按 doc_ids 裁剪生效）。"""
    other = await make_sample(storage, tmp_path)
    await storage.add_ref(sample.clause.node_id, sample.doc_id, new_uuid7(), "see_also", CTX)

    scoped = await gate(storage, other.doc_id, ["broken_refs", "assets_missing"])
    assert scoped == {"broken_refs": [], "assets_missing": []}

    unfiltered = (await gate(storage, sample.doc_id, ["broken_refs"]))["broken_refs"]
    assert rules(unfiltered) == {broken_refs.RULE_REF_DST_DANGLING}


async def test_unknown_detector_id_is_rejected(storage: Storage, sample: Sample) -> None:
    with pytest.raises(ValidationError) as excinfo:
        await run_quality_gate(
            QualityScope(doc_ids=[sample.doc_id], detectors=["ghost"]), storage=storage
        )
    assert "broken_refs" in str(excinfo.value)


async def test_sync_wrapper_refuses_running_loop(storage: Storage, sample: Sample) -> None:
    """事件循环内调用同步入口 → 明确报错（与 M12 `health_sync` 同口径）。"""
    with pytest.raises(RuntimeError):
        run_quality_gate_sync(
            QualityScope(doc_ids=[sample.doc_id], detectors=["broken_refs"]), storage=storage
        )


def test_sync_entry_is_repeatable_in_process(
    database_urls: tuple[str, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """同一进程内**多次**调用同步入口都必须成功（回归：进程级单例池绑定旧事件循环）。

    每次 `asyncio.run` 新建循环，故同步入口必须**自建自弃**连接池；依赖 `database_urls`
    以沿用 conftest 的「无 PG 即整体 skip」语义。

    此处只断言**结构与可重复性**：种子是否已入库取决于 M06 lifespan 或本文件其它用例是否
    先跑（`seeded_terms` 夹具），属**跨用例状态**，不在此处断言——「terms 面零违规」由
    `test_clean_sample_passes_gate`（显式载入种子）与人工交叉验证（M06 载入器）承担。
    """
    _, app_url = database_urls
    monkeypatch.setenv("DATABASE_URL", app_url)
    scope = QualityScope(doc_ids=[], detectors=["broken_refs", "terms"])

    first = run_quality_gate_sync(scope)
    second = run_quality_gate_sync(scope)

    assert [report.detector_id for report in first] == ["broken_refs", "terms"]
    assert [report.detector_id for report in second] == ["broken_refs", "terms"]
    # 两次调用结果逐字段一致（同一库状态下确定性；不断言违规数，避免依赖跨用例状态）
    assert [report.model_dump() for report in first] == [report.model_dump() for report in second]


async def test_global_scope_runs_all_detectors_and_finds_defects(
    storage: Storage, sample: Sample
) -> None:
    """全库作用域（`doc_ids=None`，CLI/`stats` 形态）：六个 detector 都要跑通并给出报告。"""
    ghost = new_uuid7()
    await storage.add_ref(sample.clause.node_id, sample.doc_id, ghost, "see_also", CTX)

    reports = await run_quality_gate(QualityScope(doc_ids=None, detectors=None), storage=storage)
    assert [report.detector_id for report in reports] == list(DETECTOR_IDS)

    refs = next(report for report in reports if report.detector_id == "broken_refs")
    assert broken_refs.RULE_REF_DST_DANGLING in {item.rule_id for item in refs.violations}
    assert any(str(ghost) in item.message for item in refs.violations)
    # 全库巡检不得因孤儿事件/未登记术语等历史数据而崩溃（有结论即合格）
    assert all(isinstance(report.violations, list) for report in reports)


async def test_perf_health_detects_failing_target(storage: Storage, sample: Sample) -> None:
    """`perf_health` 缺陷注入：把巡检指向**不可达库** → `verdict=fail` 必须变成违规。

    容量面的真缺陷（分区缺失/膨胀）属 DDL，应用角色无法制造；但「巡检目标不可达/未迁移」是
    等价且可注入的容量故障，且判据完全来自 M12 `health()`（本 detector 不做二次解读）。
    关键语义：`fail` **绝不静默通过**——这正是质量门接入容量巡检的意义（ADR-010）。
    """
    absent = "postgresql+asyncpg://agenticdocer_app:agenticdocer_app_dev@127.0.0.1:5432/agenticdocer_m09_absent_test"
    report = await health(dsn=absent)
    assert report.verdict == "fail", report.advice

    violations = (await gate(storage, sample.doc_id, ["perf_health"], dsn=absent))["perf_health"]
    assert bool(violations) == (report.verdict != "ok")
    assert perf_health.RULE_VERDICT in rules(violations)
    assert rules(violations) <= set(perf_health.RULES_PERF_HEALTH)
    assert all(item.fix_hint for item in violations)
    assert "失败" in violations[0].fix_hint  # 建议原样来自 M12 的 advice


# ── section_range_consistency：区间契约（M02 B-2 兜底）────────────────────


@dataclass(frozen=True)
class Outline:
    """三层大纲样本：a(l1) / a1,a2(l2, a 的子) / b(l1 同级)。"""

    doc_id: str
    root: Node
    child_a1: Node
    child_a2: Node
    sibling: Node


async def make_outline(storage: Storage) -> Outline:
    """建一份**契约成立**的大纲：ordinal 序 = 大纲序（子树在区间内连续）。"""
    index = next(_SEQ)
    doc_id = f"SPEC-QG-OUT-{_RUN}-{index}"
    await storage.upsert_doc(
        DocIn(
            doc_id=doc_id,
            doc_type="standard",
            title="Outline sample",
            meta={"doc_slug": f"outline-{_RUN}-{index}"},
            source_ref=None,
        ),
        None,
        CTX,
    )
    root = await add_node(
        storage,
        doc_id=doc_id,
        atom_type="clause",
        ordinal=1,
        level=1,
        anchor=f"{doc_id}#1·a",
        content={"fragment": "## 1 a"},
    )
    child_a1 = await add_node(
        storage,
        doc_id=doc_id,
        atom_type="clause",
        ordinal=2,
        level=2,
        anchor=f"{doc_id}#1.1·a1",
        content={"fragment": "### 1.1 a1"},
        parent=root,
    )
    child_a2 = await add_node(
        storage,
        doc_id=doc_id,
        atom_type="clause",
        ordinal=3,
        level=2,
        anchor=f"{doc_id}#1.2·a2",
        content={"fragment": "### 1.2 a2"},
        parent=root,
    )
    sibling = await add_node(
        storage,
        doc_id=doc_id,
        atom_type="clause",
        ordinal=4,
        level=1,
        anchor=f"{doc_id}#2·b",
        content={"fragment": "## 2 b"},
    )
    return Outline(
        doc_id=doc_id, root=root, child_a1=child_a1, child_a2=child_a2, sibling=sibling
    )


async def _patch_node(storage: Storage, node: Node, **values: Any) -> None:
    """直改节点字段（绕过事件）：**故意制造**只可能来自脏数据的契约破坏。"""
    async with storage.db.transaction() as session:
        await session.execute(
            update(nodes_table)
            .where(nodes_table.c.node_id == node.node_id, nodes_table.c.doc_id == node.doc_id)
            .values(**values)
        )


async def test_section_range_clean_outline_reports_nothing(storage: Storage) -> None:
    """契约成立的大纲：区间法与递归 CTE 一致 → 零违规（不误报）。"""
    outline = await make_outline(storage)
    result = await gate(storage, outline.doc_id, ["section_range_consistency"])
    assert result == {"section_range_consistency": []}


async def test_section_range_detects_missing_in_interval(storage: Storage) -> None:
    """**漏收**方向（原方案的自检盲区）：子节点的父声明在区间内、但 ordinal 排到区间之外。"""
    outline = await make_outline(storage)
    # a1 仍是 a 的子节点，但 ordinal 排到同级 b(4) 之后 → a 的区间 [1, 4) 收不到 a1
    await _patch_node(storage, outline.child_a1, ordinal=9)

    violations = (await gate(storage, outline.doc_id, ["section_range_consistency"]))[
        "section_range_consistency"
    ]
    assert rules(violations) == {section_range_consistency.RULE_SECTION_RANGE_MISMATCH}
    hit = violations[0]
    assert hit.path == f"nodes/{outline.root.node_id}"
    assert "区间缺" in hit.message and str(outline.child_a1.node_id) in hit.message
    assert "首个差异" in hit.message and hit.fix_hint


async def test_section_range_detects_extra_in_interval(storage: Storage) -> None:
    """**多收/断链**方向：区间内出现父链落在区间外的节点（自检未通过 → 区间不可用）。"""
    outline = await make_outline(storage)
    # a1 的父改成同级 b（b 的 ordinal 在 a 的区间之外），a1 自身仍在 a 的区间内
    await _patch_node(storage, outline.child_a1, parent_node_id=outline.sibling.node_id)

    violations = (await gate(storage, outline.doc_id, ["section_range_consistency"]))[
        "section_range_consistency"
    ]
    assert rules(violations) == {section_range_consistency.RULE_SECTION_RANGE_MISMATCH}
    assert any("多收/断链" in item.message for item in violations)


async def test_section_range_cycle_does_not_hang(storage: Storage) -> None:
    """成环（a1⇄a2）必须**有结论**：M02 的深度上限保证终止，detector 不得挂死或抛异常。"""
    outline = await make_outline(storage)
    await _patch_node(storage, outline.child_a1, parent_node_id=outline.child_a2.node_id)
    await _patch_node(storage, outline.child_a2, parent_node_id=outline.child_a1.node_id)

    reports = await asyncio.wait_for(
        run_quality_gate(
            QualityScope(doc_ids=[outline.doc_id], detectors=["section_range_consistency"]),
            storage=storage,
        ),
        timeout=60,
    )
    assert [report.detector_id for report in reports] == ["section_range_consistency"]
    assert all(item.path and item.fix_hint for item in reports[0].violations)


# ── doc_type_schema_conformance：组合规则的历史数据兜底 ────────────────────


async def _make_bare_doc(storage: Storage, *, doc_type: str, meta: dict[str, Any]) -> str:
    """只写 `docs` 行（**绕过 M03 frontmatter 校验**）：模拟「规则细化前入库 / 手工写入」的历史数据。"""
    index = next(_SEQ)
    doc_id = f"SPEC-QG-{_RUN}-{index}"
    await storage.upsert_doc(
        DocIn(
            doc_id=doc_id,
            doc_type=doc_type,
            title="M09 doc_type conformance sample",
            meta=meta,
            source_ref=None,
        ),
        None,
        CTX,
    )
    return doc_id


async def test_doc_type_conformance_detects_historical_missing_meta(storage: Storage) -> None:
    """规则细化后的历史行：`safety` 必填 `standard_ref`/`audit_trail` 缺失 → 逐字段命中。

    **合成样例，非真实语料**：`safety`（FMEA/FTA）无语料（`doc_type_mapping.md` §5）。本用例
    证明的是「差异化规则 + 判据在真库上连通」，**不是**端到端导入验证。
    """
    doc_id = await _make_bare_doc(storage, doc_type="safety", meta={})

    violations = (await gate(storage, doc_id, ["doc_type_schema_conformance"]))[
        "doc_type_schema_conformance"
    ]
    assert rules(violations) == {doc_type_conformance.RULE_META_MISSING}
    # 质量门出口按 `(rule_id, path)` 定序（`gate.run_quality_gate`），故此处按 path 字典序
    assert [item.path for item in violations] == [
        f"{doc_id}:meta.audit_trail",
        f"{doc_id}:meta.standard_ref",
    ]
    assert all(item.fix_hint for item in violations)


async def test_doc_type_conformance_passes_conformant_doc(storage: Storage) -> None:
    """符合现时规则的行零违规（`standard` 的 C5 十七字段齐备）——不误报。"""
    doc_id = await _make_bare_doc(
        storage, doc_type="standard", meta={field: "x" for field in C5_META_FIELDS}
    )
    result = await gate(storage, doc_id, ["doc_type_schema_conformance"])
    assert result == {"doc_type_schema_conformance": []}


async def test_doc_type_conformance_is_scoped_by_doc_ids(storage: Storage) -> None:
    """作用域收窄：只报本 `doc_ids` 内的文档（全库巡检时分摊到各文档，互不牵连）。"""
    bad = await _make_bare_doc(storage, doc_type="safety", meta={})
    good = await _make_bare_doc(
        storage, doc_type="safety", meta={"standard_ref": "IEC 61508", "audit_trail": "rev-1"}
    )
    reports = await run_quality_gate(
        QualityScope(doc_ids=[good], detectors=["doc_type_schema_conformance"]), storage=storage
    )
    assert [report.violations for report in reports] == [[]]
    scoped_bad = await gate(storage, bad, ["doc_type_schema_conformance"])
    assert scoped_bad["doc_type_schema_conformance"]


async def test_unknown_doc_type_is_blocked_by_ddl_not_by_detector(storage: Storage) -> None:
    """取值域由 **DDL** 兜底：模型层未登记的 `doc_type` 写不进 `docs`（CHECK → 422）。

    故 detector 的 `M09B.doc_type.unknown` 分支在真库**不可达**（它是 DDL/模型漂移的护栏，
    只由单测的合成行覆盖）——本用例把该边界钉死：DDL 与 `DOC_TYPES` 同域时，未知值在
    写入侧即被拒。
    """
    with pytest.raises(ValidationError):
        await _make_bare_doc(storage, doc_type="register-map", meta={})
