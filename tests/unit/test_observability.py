"""M12 可观测性横切层单元测试（ADR-010 / REQ-M12-F01..F05）。

覆盖：rid 生成与 ContextVar 传播、DTO_* 错误码、AgenticLogger 适配层
（结构化 JSONL / per-entry rid / timer / 阈值分级）、指标聚合、健康巡检判定、
FastAPI 埋点中间件。**不依赖 PG**（取数层用假连接；不可达分支用 loopback 拒连验证）。
"""

from __future__ import annotations

import asyncio
import datetime as dt
import importlib
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from agenticdocer.observability import (
    DTO_ANCHOR_CONFLICT,
    DTO_AUTH_REJECTED,
    DTO_PARTITION_MISSING,
    DTO_PERF_EXCEEDED,
    DTO_REF_BROKEN,
    HealthReport,
    IndexHealth,
    MetricsSnapshot,
    ModuleLogger,
    ObservabilityMiddleware,
    PartitionHealth,
    PoolHealth,
    RenderMetric,
    TableHealth,
    EndpointMetric,
    classify_duration,
    current_rid,
    error_code_for_rule,
    evaluate_health,
    get_logger,
    health,
    install,
    new_rid,
    normalize_dsn,
    percentile,
    perf_budget_ms,
    pool_health,
    reset_loggers,
    reset_rid,
    rid_scope,
    set_rid,
    slow_query_ms,
    snapshot,
)

_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"

# ----------------------------------------------------------------------
# fixtures / helpers
# ----------------------------------------------------------------------


@pytest.fixture()
def logs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """把 LOG_DIR 指向临时目录并清空 logger 缓存（回退时同样清空）。"""
    d = tmp_path / "logs"
    monkeypatch.setenv("LOG_DIR", str(d))
    reset_loggers()
    yield d
    reset_loggers()


def _entries(log_dir: Path, module: str | None = None) -> list[dict]:
    """读取目录下全部 JSONL 数据行（跳过 __GLOBAL_CTX__ 头）。"""
    out: list[dict] = []
    for path in sorted(log_dir.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            entry = json.loads(line)
            if entry.get("level") == "__GLOBAL_CTX__":
                continue
            if module is not None and entry.get("module") != module:
                continue
            out.append(entry)
    return out


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _since() -> dt.datetime:
    return _now() - dt.timedelta(seconds=60)


# ----------------------------------------------------------------------
# rid：生成与传播
# ----------------------------------------------------------------------


def test_new_rid_shape() -> None:
    rid = new_rid()
    assert len(rid) == 8
    assert all(c in "0123456789abcdef" for c in rid)


def test_new_rid_unique_in_burst() -> None:
    assert len({new_rid() for _ in range(50_000)}) == 50_000


def test_new_rid_leading_bytes_track_clock() -> None:
    def circular_distance(a: int, b: int) -> int:
        return min((a - b) % 256, (b - a) % 256)

    prefix = int(new_rid()[:2], 16)
    now_ms = int(time.time() * 1000) & 0xFF
    assert circular_distance(prefix, now_ms) <= 8


def test_new_rid_unique_across_processes() -> None:
    code = (
        "from agenticdocer.observability.rid import new_rid\n"
        "for _ in range(2000):\n"
        "    print(new_rid())\n"
    )
    env = {**os.environ, "PYTHONPATH": str(_SRC)}
    proc = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(_ROOT),
        check=True,
    )
    other = set(proc.stdout.split())
    assert len(other) == 2000
    assert not (other & {new_rid() for _ in range(2000)})


def test_current_rid_defaults_to_none() -> None:
    assert current_rid() is None


def test_set_rid_then_reset() -> None:
    token = set_rid("deadbeef")
    try:
        assert current_rid() == "deadbeef"
    finally:
        reset_rid(token)
    assert current_rid() is None


def test_set_rid_generates_when_omitted() -> None:
    token = set_rid()
    try:
        rid = current_rid()
    finally:
        reset_rid(token)
    assert rid is not None and len(rid) == 8


def test_rid_scope_restores_previous_value() -> None:
    token = set_rid("aaaaaaaa")
    try:
        with rid_scope() as generated:
            assert current_rid() == generated
            assert generated != "aaaaaaaa"
        assert current_rid() == "aaaaaaaa"
    finally:
        reset_rid(token)


def test_rid_scope_accepts_explicit_value() -> None:
    with rid_scope("00112233") as rid:
        assert rid == "00112233" and current_rid() == "00112233"
    assert current_rid() is None


def test_rid_propagates_into_child_async_task() -> None:
    async def main() -> str | None:
        token = set_rid("cafebabe")
        seen: dict[str, str | None] = {}

        async def child() -> None:
            seen["rid"] = current_rid()

        try:
            await asyncio.create_task(child())
        finally:
            reset_rid(token)
        return seen["rid"]

    assert asyncio.run(main()) == "cafebabe"


def test_concurrent_async_tasks_do_not_leak_rid() -> None:
    async def main() -> dict[str, set[str | None]]:
        results: dict[str, set[str | None]] = {}

        async def worker(name: str, rid: str) -> None:
            token = set_rid(rid)
            try:
                for _ in range(3):
                    await asyncio.sleep(0)
                    results.setdefault(name, set()).add(current_rid())
            finally:
                reset_rid(token)

        await asyncio.gather(worker("a", "11111111"), worker("b", "22222222"))
        return results

    assert asyncio.run(main()) == {"a": {"11111111"}, "b": {"22222222"}}


def test_thread_does_not_inherit_rid() -> None:
    """ContextVar 不跨线程传播（中间件须在请求任务内 set_rid）。"""
    token = set_rid("abcd1234")
    try:
        seen: list[str | None] = []
        worker = threading.Thread(target=lambda: seen.append(current_rid()))
        worker.start()
        worker.join()
        assert seen == [None]
        assert current_rid() == "abcd1234"
    finally:
        reset_rid(token)


# ----------------------------------------------------------------------
# 错误码
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "code",
    [DTO_PERF_EXCEEDED, DTO_ANCHOR_CONFLICT, DTO_AUTH_REJECTED, DTO_REF_BROKEN, DTO_PARTITION_MISSING],
)
def test_dto_error_code_is_plain_string(code: str) -> None:
    assert str(code) == code.value
    assert str(code).startswith("DTO_")


def test_error_code_for_rule_maps_known_rule() -> None:
    assert error_code_for_rule("RULE_ANCHOR_DUP") == DTO_ANCHOR_CONFLICT


def test_error_code_for_rule_passes_unknown_rule_through() -> None:
    assert error_code_for_rule("RULE_SOMETHING_ELSE") == "RULE_SOMETHING_ELSE"


# ----------------------------------------------------------------------
# 适配层：阈值分级 / logger
# ----------------------------------------------------------------------


def test_classify_duration_boundaries() -> None:
    assert classify_duration(5, None) == ("INFO", None)
    assert classify_duration(0, 100) == ("INFO", None)
    assert classify_duration(80, 100) == ("INFO", None)  # 恰好 0.8× → 不告警
    assert classify_duration(81, 100) == ("WARN", None)
    assert classify_duration(100, 100) == ("WARN", None)  # 恰好等于指标 → 未超
    level, code = classify_duration(101, 100)
    assert level == "ERROR"
    assert str(code) == "DTO_PERF_EXCEEDED"


def test_perf_budget_reads_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SLOW_QUERY_MS", "77")
    assert perf_budget_ms("point_query") == 77
    assert slow_query_ms() == 77
    assert perf_budget_ms("unknown_op") is None


def test_perf_budget_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SLOW_QUERY_MS", raising=False)
    assert slow_query_ms() == 200
    assert perf_budget_ms("render_section") == 1000
    assert perf_budget_ms("render_document") == 3000
    assert perf_budget_ms("auth_verify") == 10


def test_get_logger_returns_module_view(logs: Path) -> None:
    logger = get_logger("m12.test")
    assert isinstance(logger, ModuleLogger)
    assert logger.module == "m12.test"


def test_command_derived_from_module_prefix(logs: Path) -> None:
    assert get_logger("m02.nodes").file_path.name.startswith("agenticdocer_store")
    assert get_logger("m06.router").file_path.name.startswith("agenticdocer_api")
    assert get_logger("m07.router").file_path.name.startswith("agenticdocer_api")
    assert get_logger("mlr.export").file_path.name.startswith("agenticdocer_export")
    assert get_logger("custom.thing").file_path.name.startswith("agenticdocer_custom")


def test_logger_writes_structured_jsonl(logs: Path) -> None:
    token = set_rid("1234abcd")
    try:
        logger = get_logger("m02.nodes", doc_id="SPEC-CXL")
        logger.info("hello", msg="x", count=2)
    finally:
        reset_rid(token)

    entries = _entries(logs)
    assert len(entries) == 1
    entry = entries[0]
    assert entry["level"] == "INFO"
    assert entry["module"] == "m02.nodes"
    assert entry["rid"] == "1234abcd"
    assert entry["msg"] == "hello"
    assert entry["ctx"] == {"doc_id": "SPEC-CXL", "msg": "x", "count": 2}
    assert {"ts", "pid", "seq"} <= set(entry)


def test_rid_is_resolved_per_entry(logs: Path) -> None:
    logger = get_logger("m12.test")
    for rid in ("aaaaaaaa", "bbbbbbbb"):
        token = set_rid(rid)
        try:
            logger.info("x")
        finally:
            reset_rid(token)
    assert [e["rid"] for e in _entries(logs)] == ["aaaaaaaa", "bbbbbbbb"]


def test_entry_without_context_falls_back_to_run_rid(logs: Path) -> None:
    get_logger("m12.test").info("x")
    rid = _entries(logs)[0]["rid"]
    assert len(rid) == 8 and rid != ""


def test_error_without_code_defaults_to_unknown(logs: Path) -> None:
    get_logger("m12.test").error("boom")
    assert _entries(logs)[0]["error_code"] == "UNKNOWN"


def test_debug_writes_debug_level(logs: Path) -> None:
    get_logger("m12.test").debug("trace detail", step=1)
    entry = _entries(logs)[0]
    assert entry["level"] == "DEBUG"
    assert entry["ctx"]["step"] == 1


def test_exception_records_traceback_sidecar(logs: Path) -> None:
    logger = get_logger("m10.verify")
    try:
        raise ValueError("bad signature")
    except ValueError as exc:
        logger.exception("verify failed", exc)

    entry = _entries(logs)[0]
    assert entry["level"] == "ERROR"
    assert entry["error_code"] == "INTERNAL_UNEXPECTED"
    assert entry["tid"].startswith("tb_")

    sidecars = list(logs.glob("*.tracebacks"))
    assert sidecars
    assert "bad signature" in sidecars[0].read_text(encoding="utf-8")


def test_child_binds_extra_context(logs: Path) -> None:
    logger = get_logger("m04.render").child(doc_id="SPEC-1", section="3.0")
    logger.info("rendered")
    assert _entries(logs)[0]["ctx"] == {"doc_id": "SPEC-1", "section": "3.0"}


def test_tool_call_logs_command_with_error_code(logs: Path) -> None:
    get_logger("m11.cli").tool_call("agenticdocer", "import --doc SPEC-1", 2, 42)
    entry = _entries(logs)[0]
    assert entry["level"] == "TOOL"
    assert entry["module"] == "m11.cli"
    assert entry["tool"] == "agenticdocer"
    assert entry["cmd"] == "import --doc SPEC-1"
    assert entry["exit"] == 2
    assert entry["dur"] == 42
    assert entry["error_code"] == "EXEC_NON_ZERO"


def test_tool_call_success_has_no_error_code(logs: Path) -> None:
    get_logger("m11.cli").tool_call("agenticdocer", "stats", 0, 5)
    entry = _entries(logs)[0]
    assert entry["exit"] == 0
    assert "error_code" not in entry


# ----------------------------------------------------------------------
# 适配层：timer
# ----------------------------------------------------------------------


def test_timer_records_duration(logs: Path) -> None:
    with get_logger("m02.nodes").timer("point_query"):
        time.sleep(0.01)
    entry = _entries(logs)[0]
    assert entry["level"] == "INFO"
    assert entry["dur"] >= 10
    assert entry["ctx"]["op"] == "point_query"


def test_timer_merges_extra_fields(logs: Path) -> None:
    with get_logger("m02.nodes").timer("point_query", doc_id="SPEC-1"):
        pass
    ctx = _entries(logs)[0]["ctx"]
    assert ctx["op"] == "point_query" and ctx["doc_id"] == "SPEC-1"


def test_timer_error_path_logs_and_reraises(logs: Path) -> None:
    with pytest.raises(ValueError):
        with get_logger("m02.nodes").timer("point_query", error_code=DTO_REF_BROKEN):
            raise ValueError("boom")

    entry = _entries(logs)[0]
    assert entry["level"] == "ERROR"
    assert entry["error_code"] == "DTO_REF_BROKEN"
    assert entry["dur"] >= 0
    assert entry["ctx"]["op"] == "point_query"
    assert entry["tid"].startswith("tb_")


def test_timer_exceeding_budget_emits_perf_error_code(logs: Path) -> None:
    with get_logger("m02.nodes").timer("point_query", budget_ms=1):
        time.sleep(0.005)
    entry = _entries(logs)[0]
    assert entry["level"] == "ERROR"
    assert entry["error_code"] == "DTO_PERF_EXCEEDED"


def test_timer_within_budget_is_info(logs: Path) -> None:
    with get_logger("m04.render").timer("render_section", budget_ms=10_000):
        pass
    assert _entries(logs)[0]["level"] == "INFO"


def test_timer_uses_env_budget_for_point_query(logs: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SLOW_QUERY_MS", "1")
    with get_logger("m02.nodes").timer("point_query"):
        time.sleep(0.005)
    assert _entries(logs)[0]["error_code"] == "DTO_PERF_EXCEEDED"


def test_logger_file_is_readable_by_sdk_query_layer(logs: Path) -> None:
    from agentic_logger.storage.jsonl import JSONLBackend

    logger = get_logger("m09a.engine")
    token = set_rid("feedf00d")
    try:
        logger.info("validated", dur=12, doc_id="SPEC-1")
    finally:
        reset_rid(token)

    backend = JSONLBackend(file_path=logger.file_path)
    assert backend.stats("module")["m09a.engine"] == 1
    hits = backend.query(rid="feedf00d", level="INFO")
    assert len(hits) == 1 and hits[0]["dur"] == 12


# ----------------------------------------------------------------------
# 指标聚合
# ----------------------------------------------------------------------


def test_percentile_nearest_rank() -> None:
    values = [10, 20, 30, 40, 100]
    assert percentile(values, 50) == 30
    assert percentile(values, 95) == 100
    assert percentile(values, 99) == 100
    assert percentile(values, 0) == 10
    assert percentile([], 95) == 0


def test_snapshot_on_empty_dir_is_zeroed(logs: Path) -> None:
    snap = snapshot(since=_since(), window=600, log_dir=logs)
    assert snap.window_seconds == 600
    assert snap.endpoints == []
    assert snap.slow_queries == []
    assert snap.auth_failures == 0
    assert snap.render.count == 0


def test_snapshot_aggregates_endpoints(logs: Path) -> None:
    logger = get_logger("m06.router")
    for dur in (10, 20, 30, 40, 100):
        logger.info("GET /api/v1/docs/{doc_id} 200", dur=dur, route="/api/v1/docs/{doc_id}", method="GET", status=200)
    logger.info("GET /api/v1/docs/{doc_id} 500", dur=7, route="/api/v1/docs/{doc_id}", method="GET", status=500)

    snap = snapshot(since=_since(), window=600, log_dir=logs)
    assert len(snap.endpoints) == 1
    metric = snap.endpoints[0]
    assert metric.route == "/api/v1/docs/{doc_id}"
    assert metric.count == 6
    assert (metric.p50, metric.p95, metric.p99) == (20, 100, 100)
    assert metric.error_rate == pytest.approx(1 / 6)


def test_snapshot_ignores_entries_outside_window(logs: Path) -> None:
    logger = get_logger("m06.router")
    logger.info("fresh", dur=5, route="/x", status=200)

    stale = {
        "ts": (_now() - dt.timedelta(hours=2)).isoformat(timespec="milliseconds"),
        "level": "INFO",
        "msg": "stale",
        "module": "m06.router",
        "rid": "deadbeef",
        "pid": "1",
        "seq": 99,
        "dur": 5,
        "ctx": {"route": "/x", "status": 200},
    }
    with logger.file_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(stale) + "\n")

    snap = snapshot(since=_since(), window=600, log_dir=logs)
    assert snap.endpoints[0].count == 1


def test_snapshot_collects_slow_queries(logs: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SLOW_QUERY_MS", "50")
    logger = get_logger("m02.nodes")
    logger.warn("slow query", dur=500, op="point_query", sql_hash="abc123", table="nodes")
    logger.info("fast query", dur=5, op="point_query", sql_hash="abc123", table="nodes")

    snap = snapshot(since=_since(), window=600, log_dir=logs)
    assert len(snap.slow_queries) == 1
    slow = snap.slow_queries[0]
    assert (slow.sql_hash, slow.count, slow.max_dur, slow.table) == ("abc123", 1, 500, "nodes")


def test_snapshot_counts_auth_failures(logs: Path) -> None:
    logger = get_logger("m10.verify")
    logger.error("signature rejected", error_code=DTO_AUTH_REJECTED)
    logger.error("broken ref", error_code=DTO_REF_BROKEN)

    snap = snapshot(since=_since(), window=600, log_dir=logs)
    assert snap.auth_failures == 1


def test_snapshot_render_metrics(logs: Path) -> None:
    logger = get_logger("m04.render")
    logger.info("section", dur=100, op="render_section")
    logger.info("section", dur=200, op="render_section")
    logger.info("document", dur=500, op="render_document")

    snap = snapshot(since=_since(), window=600, log_dir=logs)
    assert snap.render.count == 3
    assert snap.render.section_p95 == 200
    assert snap.render.document_p95 == 500


def test_metrics_types_serialise_camel_case() -> None:
    snap = MetricsSnapshot(
        window_seconds=60,
        endpoints=[EndpointMetric(route="/x", count=1, p50=1, p95=2, p99=3, error_rate=0.0)],
        slow_queries=[],
        auth_failures=0,
        render=RenderMetric(section_p95=0, document_p95=0, count=0),
    )
    dumped = snap.model_dump(by_alias=True)
    assert set(dumped) == {"windowSeconds", "endpoints", "slowQueries", "authFailures", "render"}
    assert set(dumped["endpoints"][0]) == {"route", "count", "p50", "p95", "p99", "errorRate"}
    assert set(dumped["render"]) == {"sectionP95", "documentP95", "count"}

    parsed = MetricsSnapshot.model_validate(
        {
            "windowSeconds": 60,
            "endpoints": [],
            "slowQueries": [],
            "authFailures": 3,
            "render": {"sectionP95": 1, "documentP95": 2, "count": 3},
        }
    )
    assert parsed.auth_failures == 3
    assert parsed.render.section_p95 == 1


def test_health_types_serialise_camel_case() -> None:
    report = HealthReport(
        tables=[TableHealth(name="nodes", rows=1, size_bytes=2, dead_tup=3, last_autovacuum=None)],
        indexes=[IndexHealth(name="idx_nodes_doc_ordinal", scans=0, size_bytes=4)],
        partitions=PartitionHealth(events_next_missing=False, oldest_event_ts=None),
        pool=PoolHealth(size=20, checkedout=1, overflow=0),
        verdict="ok",
        advice=[],
    )
    dumped = report.model_dump(by_alias=True)
    assert set(dumped) == {"tables", "indexes", "partitions", "pool", "verdict", "advice"}
    assert set(dumped["tables"][0]) == {"name", "rows", "sizeBytes", "deadTup", "lastAutovacuum"}
    assert set(dumped["partitions"]) == {"eventsNextMissing", "oldestEventTs"}
    assert set(dumped["pool"]) == {"size", "checkedout", "overflow"}




# ----------------------------------------------------------------------
# 健康巡检
# ----------------------------------------------------------------------


def _ok_tables() -> list[TableHealth]:
    return [
        TableHealth(
            name="nodes",
            rows=1_000,
            size_bytes=1 << 20,
            dead_tup=10,
            last_autovacuum=_now(),
        )
    ]


def _ok_indexes() -> list[IndexHealth]:
    return [IndexHealth(name="idx_nodes_doc_ordinal", scans=42, size_bytes=1 << 20)]


def _ok_partitions() -> PartitionHealth:
    return PartitionHealth(events_next_missing=False, oldest_event_ts=_now() - dt.timedelta(days=30))


def test_evaluate_health_ok() -> None:
    report = evaluate_health(
        tables=_ok_tables(),
        indexes=_ok_indexes(),
        partitions=_ok_partitions(),
        pool=PoolHealth(size=20, checkedout=1, overflow=0),
    )
    assert report.verdict == "ok"
    assert report.advice == []


def test_evaluate_health_missing_partition_is_fail() -> None:
    report = evaluate_health(
        tables=_ok_tables(),
        indexes=_ok_indexes(),
        partitions=PartitionHealth(events_next_missing=True, oldest_event_ts=_now() - dt.timedelta(days=30)),
        pool=PoolHealth(size=20, checkedout=1, overflow=0),
    )
    assert report.verdict == "fail"
    assert any("分区" in advice for advice in report.advice)


def test_evaluate_health_dead_tuples_degrade() -> None:
    report = evaluate_health(
        tables=[TableHealth(name="nodes", rows=100_000, size_bytes=1 << 30, dead_tup=40_000, last_autovacuum=_now())],
        indexes=_ok_indexes(),
        partitions=_ok_partitions(),
        pool=PoolHealth(size=20, checkedout=1, overflow=0),
    )
    assert report.verdict == "degraded"
    assert any("vacuum" in advice.lower() or "膨胀" in advice for advice in report.advice)


def test_evaluate_health_stale_autovacuum_degrades() -> None:
    report = evaluate_health(
        tables=[
            TableHealth(
                name="events",
                rows=1_000_000,
                size_bytes=1 << 30,
                dead_tup=50_000,
                last_autovacuum=_now() - dt.timedelta(days=30),
            )
        ],
        indexes=_ok_indexes(),
        partitions=_ok_partitions(),
        pool=PoolHealth(size=20, checkedout=1, overflow=0),
    )
    assert report.verdict == "degraded"
    assert any("autovacuum" in advice for advice in report.advice)


def test_evaluate_health_unused_index_advice() -> None:
    report = evaluate_health(
        tables=_ok_tables(),
        indexes=[IndexHealth(name="idx_dead", scans=0, size_bytes=64 << 20)],
        partitions=_ok_partitions(),
        pool=PoolHealth(size=20, checkedout=1, overflow=0),
    )
    assert report.verdict == "degraded"
    assert any("idx_dead" in advice for advice in report.advice)


def test_evaluate_health_small_unused_index_is_ignored() -> None:
    report = evaluate_health(
        tables=_ok_tables(),
        indexes=[IndexHealth(name="idx_tiny", scans=0, size_bytes=1024)],
        partitions=_ok_partitions(),
        pool=PoolHealth(size=20, checkedout=1, overflow=0),
    )
    assert report.verdict == "ok"


def test_evaluate_health_pool_saturation_degrades() -> None:
    report = evaluate_health(
        tables=_ok_tables(),
        indexes=_ok_indexes(),
        partitions=_ok_partitions(),
        pool=PoolHealth(size=20, checkedout=24, overflow=10),
    )
    assert report.verdict == "degraded"
    assert any("连接池" in advice for advice in report.advice)


def test_evaluate_health_pool_untouched_when_unavailable() -> None:
    report = evaluate_health(
        tables=_ok_tables(),
        indexes=_ok_indexes(),
        partitions=_ok_partitions(),
        pool=PoolHealth(size=0, checkedout=0, overflow=0),
    )
    assert report.verdict == "ok"
    assert report.advice == []


def test_evaluate_health_archive_overdue_degrades() -> None:
    report = evaluate_health(
        tables=_ok_tables(),
        indexes=_ok_indexes(),
        partitions=PartitionHealth(
            events_next_missing=False,
            oldest_event_ts=_now() - dt.timedelta(days=900),
        ),
        pool=PoolHealth(size=20, checkedout=1, overflow=0),
    )
    assert report.verdict == "degraded"
    assert any("归档" in advice for advice in report.advice)


def test_normalize_dsn_strips_driver_suffix() -> None:
    assert normalize_dsn("postgresql+asyncpg://u:p@h:5432/db") == "postgresql://u:p@h:5432/db"
    assert normalize_dsn("postgresql://u:p@h:5432/db") == "postgresql://u:p@h:5432/db"


def test_pool_health_from_sqlalchemy_like_pool() -> None:
    class _Engine:
        class pool:  # noqa: N801
            @staticmethod
            def size() -> int:
                return 20

            @staticmethod
            def checkedout() -> int:
                return 3

            @staticmethod
            def overflow() -> int:
                return 1

    assert pool_health(_Engine()) == PoolHealth(size=20, checkedout=3, overflow=1)
    assert pool_health(None) == PoolHealth(size=0, checkedout=0, overflow=0)


def test_health_reports_fail_when_db_unreachable(logs: Path) -> None:
    report = asyncio.run(health(dsn="postgresql://nobody:nobody@127.0.0.1:1/agenticdocer", timeout=0.5))
    assert report.verdict == "fail"
    assert report.advice and any("数据库" in advice for advice in report.advice)
    assert _entries(logs, module="m12.health")


# ----------------------------------------------------------------------
# FastAPI 中间件
# ----------------------------------------------------------------------


def _make_app() -> FastAPI:
    app = FastAPI()

    @app.get("/ping")
    async def ping() -> dict[str, str | None]:
        return {"rid": current_rid()}

    @app.get("/boom")
    async def boom() -> None:
        raise HTTPException(status_code=403, detail="nope")

    @app.get("/crash")
    async def crash() -> None:
        raise RuntimeError("kaput")

    install(app)
    return app


def test_middleware_generates_rid_and_logs_request(logs: Path) -> None:
    with TestClient(_make_app()) as client:
        response = client.get("/ping")

    assert response.status_code == 200
    rid = response.headers["x-request-id"]
    assert len(rid) == 8
    assert response.json()["rid"] == rid

    entry = _entries(logs, module="m12.middleware")[0]
    assert entry["rid"] == rid
    assert entry["level"] == "INFO"
    assert entry["ctx"]["route"] == "/ping"
    assert entry["ctx"]["method"] == "GET"
    assert entry["ctx"]["status"] == 200
    assert entry["dur"] >= 0


def test_middleware_uses_route_template_for_parameterised_path(logs: Path) -> None:
    app = FastAPI()

    @app.get("/docs/{doc_id}")
    async def doc(doc_id: str) -> dict[str, str]:
        return {"doc_id": doc_id}

    install(app)
    with TestClient(app) as client:
        assert client.get("/docs/SPEC-1").status_code == 200

    assert _entries(logs, module="m12.middleware")[0]["ctx"]["route"] == "/docs/{doc_id}"


def test_middleware_logs_client_error_as_warn(logs: Path) -> None:
    with TestClient(_make_app()) as client:
        response = client.get("/boom")

    assert response.status_code == 403
    entry = _entries(logs, module="m12.middleware")[0]
    assert entry["level"] == "WARN"
    assert entry["error_code"] == "DTO_AUTH_REJECTED"
    assert entry["ctx"]["status"] == 403


def test_middleware_logs_unhandled_exception_as_error(logs: Path) -> None:
    with TestClient(_make_app(), raise_server_exceptions=False) as client:
        response = client.get("/crash")

    assert response.status_code == 500
    entry = _entries(logs, module="m12.middleware")[0]
    assert entry["level"] == "ERROR"
    assert entry["error_code"] == "INTERNAL_UNEXPECTED"
    assert entry["ctx"]["status"] == 500
    assert entry["tid"].startswith("tb_")
    assert logs.glob("*.tracebacks")


def test_middleware_is_asgi_middleware_subclass() -> None:
    from starlette.middleware.base import BaseHTTPMiddleware

    assert issubclass(ObservabilityMiddleware, BaseHTTPMiddleware)


# ----------------------------------------------------------------------
# 健康巡检取数（假连接：验证 SQL 结果 → HealthReport 的映射与分区覆盖判定）
# ----------------------------------------------------------------------


class _FakeConn:
    """按 SQL 关键字分派的 asyncpg 连接替身。"""

    def __init__(self, tables: list[dict], indexes: list[dict], relkind: str | None, bounds: list[str]) -> None:
        self._tables = tables
        self._indexes = indexes
        self._relkind = relkind
        self._bounds = [{"relname": f"events_p{i}", "bound": b} for i, b in enumerate(bounds)]
        self.closed = False

    async def fetch(self, sql: str) -> list[dict]:
        if "pg_stat_user_tables" in sql:
            return self._tables
        if "pg_stat_user_indexes" in sql:
            return self._indexes
        return self._bounds

    async def fetchval(self, sql: str) -> str | None:
        return self._relkind

    async def close(self) -> None:
        self.closed = True


def _patch_pg(monkeypatch: pytest.MonkeyPatch, conn: _FakeConn) -> None:
    # 注意：包级 `health` 是函数名，取子模块须走 importlib。
    health_module = importlib.import_module("agenticdocer.observability.health")

    async def fake_connect(dsn: str, timeout: float = 5.0) -> _FakeConn:
        return conn

    monkeypatch.setattr(health_module.asyncpg, "connect", fake_connect)


def _month_bounds(*months: str) -> list[str]:
    """生成 `FOR VALUES FROM (…) TO (…)` 边界文本。"""
    out = []
    for month in months:
        year, mon = (int(part) for part in month.split("-"))
        start = dt.datetime(year, mon, 1, tzinfo=dt.timezone.utc)
        end = dt.datetime(year + (mon // 12), mon % 12 + 1, 1, tzinfo=dt.timezone.utc)
        out.append(f"FOR VALUES FROM ('{start:%Y-%m-%d %H:%M:%S+00}') TO ('{end:%Y-%m-%d %H:%M:%S+00}')")
    return out


def _this_month() -> str:
    now = _now()
    return f"{now.year:04d}-{now.month:02d}"


def test_probe_detects_missing_next_month_partition(
    logs: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    conn = _FakeConn(
        tables=[],
        indexes=[],
        relkind="p",
        bounds=_month_bounds(_this_month()),
    )
    _patch_pg(monkeypatch, conn)

    report = asyncio.run(health(dsn="postgresql://u:p@127.0.0.1:5432/agenticdocer"))
    assert conn.closed  # 连接必须被关闭
    assert report.partitions.events_next_missing is True
    assert report.verdict == "fail"
    assert any("分区" in advice for advice in report.advice)
    entry = _entries(logs, module="m12.health")
    assert any(e.get("error_code") == "DTO_PARTITION_MISSING" for e in entry)


def test_probe_accepts_covered_next_month(logs: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    now = _now()
    nxt = dt.datetime(now.year + (now.month // 12), now.month % 12 + 1, 1)
    conn = _FakeConn(
        tables=[
            {
                "relname": "nodes",
                "n_live_tup": 10,
                "size_bytes": 1024,
                "n_dead_tup": 0,
                "last_autovacuum": now,
            }
        ],
        indexes=[{"indexrelname": "idx_nodes_doc_ordinal", "idx_scan": 7, "size_bytes": 1024}],
        relkind="p",
        bounds=_month_bounds(_this_month(), f"{nxt.year:04d}-{nxt.month:02d}"),
    )
    _patch_pg(monkeypatch, conn)

    report = asyncio.run(health(dsn="postgresql://u:p@127.0.0.1:5432/agenticdocer"))
    assert report.partitions.events_next_missing is False
    assert report.verdict == "ok"
    assert [t.name for t in report.tables] == ["nodes"]
    assert report.partitions.oldest_event_ts is not None


def test_probe_flags_unpartitioned_events_table(logs: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    conn = _FakeConn(tables=[], indexes=[], relkind="r", bounds=[])
    _patch_pg(monkeypatch, conn)

    report = asyncio.run(health(dsn="postgresql://u:p@127.0.0.1:5432/agenticdocer"))
    assert report.partitions.events_next_missing is False
    assert report.verdict == "degraded"
    assert any("分区" in advice for advice in report.advice)


def test_probe_fails_when_events_table_missing(logs: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    conn = _FakeConn(tables=[], indexes=[], relkind=None, bounds=[])
    _patch_pg(monkeypatch, conn)

    report = asyncio.run(health(dsn="postgresql://u:p@127.0.0.1:5432/agenticdocer"))
    assert report.verdict == "fail"
    assert any("迁移" in advice for advice in report.advice)


def test_probe_ignores_unparseable_bounds(logs: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    conn = _FakeConn(
        tables=[],
        indexes=[],
        relkind="p",
        bounds=["DEFAULT"],
    )
    _patch_pg(monkeypatch, conn)

    report = asyncio.run(health(dsn="postgresql://u:p@127.0.0.1:5432/agenticdocer"))
    assert report.partitions.oldest_event_ts is None
    assert report.partitions.events_next_missing is True

def test_health_reports_fail_without_dsn(logs: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    report = asyncio.run(health())
    assert report.verdict == "fail"
    assert any("DATABASE_URL" in advice for advice in report.advice)
