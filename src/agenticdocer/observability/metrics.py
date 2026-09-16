"""在线性能指标聚合（ADR-010 §3.1、REQ-M12-F03）。

从 **AgenticLogger 查询层**（`agentic_logger.storage.jsonl.JSONLBackend`）读取 `logs/`
下的 JSONL 原始日志并聚合——不引入 Prometheus/Grafana/时序库（ADR-010 明确否决），
也不重复实现查询逻辑。

**日志契约（埋点方 ↔ 本聚合层的接口）**

| 指标 | 采集点（写入方） | 本层识别方式 |
|---|---|---|
| 端点耗时/错误率 | `m12.middleware`、`m06/m07.router` | ctx 含 `route`；`status >= 400` 计入错误率 |
| 慢查询 Top-N | M02 查询包装器（`> SLOW_QUERY_MS`） | ctx 含 `table` 且 `dur > slow_query_ms()` |
| 鉴权失败率 | M10 `verify_signature` | `error_code == DTO_AUTH_REJECTED`（或 `AUTH_*`） |
| 渲染耗时（整档/章节） | M04（`op = render_section` / `render_document`） | ctx 的 `op` |

百分位用 **nearest-rank** 法（确定性、无需 numpy）：`k = ceil(q/100 × n)`，取升序第 k 个。
"""

from __future__ import annotations

import datetime as dt
import math
import os
from collections import defaultdict
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any

from agentic_logger.storage.jsonl import JSONLBackend
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from agenticdocer.observability.error_codes import DTO_AUTH_REJECTED
from agenticdocer.observability.logger import PROGRAM, log_dir as log_directory, slow_query_ms

#: 单文件最多读取的日志行数（内存上界；超限时截断，快照计数偏低）。
_MAX_ENTRIES_PER_FILE = int(os.environ.get("METRICS_MAX_ENTRIES", "200000"))

#: 鉴权失败码的兼容前缀（SDK 自带 `AUTH_*` 与本文 `DTO_AUTH_*` 并存）。
_AUTH_FAILURE_PREFIXES = ("AUTH_",)

#: 渲染类 op 名（M04 埋点约定）。
RENDER_SECTION_OP = "render_section"
RENDER_DOCUMENT_OP = "render_document"


class _CamelModel(BaseModel):
    """HTTP 序列化统一 camelCase（§6 横切：`alias_generator=to_camel`）。"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class EndpointMetric(_CamelModel):
    """单个路由的耗时与错误率。"""

    route: str
    count: int
    p50: int
    p95: int
    p99: int
    error_rate: float


class SlowQuery(_CamelModel):
    """慢查询聚合（M02 包装器上报）。"""

    sql_hash: str
    count: int
    max_dur: int
    table: str


class RenderMetric(_CamelModel):
    """渲染耗时（整档 vs 章节，§1.4 指标）。"""

    section_p95: int
    document_p95: int
    count: int


class MetricsSnapshot(_CamelModel):
    """窗口内的指标快照（`GET /api/v1/admin/metrics` 的响应体）。"""

    window_seconds: int
    endpoints: list[EndpointMetric]
    slow_queries: list[SlowQuery]
    auth_failures: int
    render: RenderMetric


def percentile(values: Sequence[int], q: float) -> int:
    """nearest-rank 百分位；空序列返回 0。"""
    if not values:
        return 0
    ordered = sorted(values)
    rank = max(1, math.ceil(q / 100 * len(ordered)))
    return ordered[rank - 1]


def snapshot(
    since: dt.datetime,
    window: int = 3600,
    *,
    log_dir: str | Path | None = None,
) -> MetricsSnapshot:
    """聚合 `[since, since+window)` 窗口内的指标快照。

    `since` 为 naive 时按 UTC 处理（与 SDK 写入的 `ts` 口径一致）。
    """
    if since.tzinfo is None:
        since = since.replace(tzinfo=dt.timezone.utc)
    until = since + dt.timedelta(seconds=window)
    directory = Path(log_dir) if log_dir is not None else log_directory()
    entries = _collect(since, until, directory)
    return MetricsSnapshot(
        window_seconds=window,
        endpoints=_endpoint_metrics(entries),
        slow_queries=_slow_queries(entries),
        auth_failures=sum(1 for entry in entries if _is_auth_failure(entry)),
        render=_render_metric(entries),
    )


# ----------------------------------------------------------------------
# 读取层
# ----------------------------------------------------------------------


def _log_files(directory: Path) -> list[Path]:
    files = sorted(directory.glob(f"{PROGRAM}_*.jsonl"))
    archive = directory / "archive"
    if archive.is_dir():
        files.extend(sorted(archive.glob(f"{PROGRAM}_*.jsonl")))
    return files


def _collect(since: dt.datetime, until: dt.datetime, directory: Path) -> list[dict[str, Any]]:
    """读取窗口内的日志条目（跳过 `__GLOBAL_CTX__` 头；非重叠文件按时间范围跳过）。"""
    since_text = since.isoformat(timespec="milliseconds")
    until_text = until.isoformat(timespec="milliseconds")

    entries: list[dict[str, Any]] = []
    for path in _log_files(directory):
        if not path.exists() or path.stat().st_size == 0:
            continue
        backend = JSONLBackend(file_path=path)
        span = backend.get_time_range()
        if span is not None and (span["max_ts"] < since_text or span["min_ts"] > until_text):
            continue
        for entry in backend.query(since=since_text, until=until_text, limit=_MAX_ENTRIES_PER_FILE):
            if entry.get("level") == "__GLOBAL_CTX__":
                continue
            entries.append(entry)
    return entries


def _ctx(entry: dict[str, Any]) -> dict[str, Any]:
    ctx = entry.get("ctx")
    return ctx if isinstance(ctx, dict) else {}


def _dur(entry: dict[str, Any]) -> int | None:
    dur = entry.get("dur")
    return dur if isinstance(dur, int) else None


def _status(entry: dict[str, Any]) -> int:
    status = _ctx(entry).get("status")
    if isinstance(status, int):
        return status
    # 无 status 字段时退化为 level 判定（ERROR 视为失败请求）。
    return 500 if entry.get("level") == "ERROR" else 200


# ----------------------------------------------------------------------
# 聚合
# ----------------------------------------------------------------------


def _endpoint_metrics(entries: Iterable[dict[str, Any]]) -> list[EndpointMetric]:
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        route = _ctx(entry).get("route")
        if isinstance(route, str) and route:
            buckets[route].append(entry)

    metrics: list[EndpointMetric] = []
    for route, group in buckets.items():
        durs = [dur for entry in group if (dur := _dur(entry)) is not None]
        errors = sum(1 for entry in group if _status(entry) >= 400)
        metrics.append(
            EndpointMetric(
                route=route,
                count=len(group),
                p50=percentile(durs, 50),
                p95=percentile(durs, 95),
                p99=percentile(durs, 99),
                error_rate=errors / len(group),
            )
        )
    metrics.sort(key=lambda metric: metric.count, reverse=True)
    return metrics


def _slow_queries(entries: Iterable[dict[str, Any]]) -> list[SlowQuery]:
    threshold = slow_query_ms()
    buckets: dict[tuple[str, str], list[int]] = defaultdict(list)
    for entry in entries:
        ctx = _ctx(entry)
        table = ctx.get("table")
        dur = _dur(entry)
        if not isinstance(table, str) or dur is None or dur <= threshold:
            continue
        sql_hash = ctx.get("sql_hash")
        buckets[(sql_hash if isinstance(sql_hash, str) else "unknown", table)].append(dur)

    queries = [
        SlowQuery(sql_hash=sql_hash, count=len(durs), max_dur=max(durs), table=table)
        for (sql_hash, table), durs in buckets.items()
    ]
    queries.sort(key=lambda query: query.max_dur, reverse=True)
    return queries


def _is_auth_failure(entry: dict[str, Any]) -> bool:
    code = str(entry.get("error_code") or "")
    return code == str(DTO_AUTH_REJECTED) or code.startswith(_AUTH_FAILURE_PREFIXES)


def _render_metric(entries: Iterable[dict[str, Any]]) -> RenderMetric:
    sections: list[int] = []
    documents: list[int] = []
    for entry in entries:
        op = _ctx(entry).get("op")
        dur = _dur(entry)
        if dur is None:
            continue
        if op == RENDER_SECTION_OP:
            sections.append(dur)
        elif op == RENDER_DOCUMENT_OP:
            documents.append(dur)
    return RenderMetric(
        section_p95=percentile(sections, 95),
        document_p95=percentile(documents, 95),
        count=len(sections) + len(documents),
    )


__all__ = [
    "RENDER_DOCUMENT_OP",
    "RENDER_SECTION_OP",
    "EndpointMetric",
    "MetricsSnapshot",
    "RenderMetric",
    "SlowQuery",
    "percentile",
    "snapshot",
]
