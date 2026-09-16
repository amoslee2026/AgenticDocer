"""容量健康巡检（ADR-010 §3.3、REQ-M12-F05）——`agenticdocer stats --health`。

巡检项（全部只读）：

| 项 | 数据源 |
|---|---|
| 表行数与膨胀 | `pg_stat_user_tables`（`n_live_tup`/`n_dead_tup`）+ `pg_total_relation_size` |
| autovacuum 滞后 | `pg_stat_user_tables.last_autovacuum` |
| 索引使用率 | `pg_stat_user_indexes`（`idx_scan = 0` → 建议清理） |
| 分区完整性 | `events` 分区边界（`pg_get_expr(relpartbound)`）→ 下一月分区是否已建 |
| 归档逾期 | 最老 `events` 分区起点 vs 24 个月保留策略（ADR-009） |
| 连接池饱和度 | 应用侧 `pool.checkedout()/size()` 采样（注入 engine/pool） |

判定分三档（`HealthReport.verdict`）：`ok` / `degraded`（有建议） / `fail`（分区缺失、
库不可达、连接池打满）。`evaluate_health()` 是纯函数，便于单测；`health()` 负责取数。
"""

from __future__ import annotations

import asyncio
import datetime as dt
import os
import re
import time
from dataclasses import dataclass, field
from typing import Any, Literal

import asyncpg
from agentic_logger import ErrorCode
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from agenticdocer.observability.error_codes import DTO_PARTITION_MISSING
from agenticdocer.observability.logger import get_logger

# ---------------------------------------------------------------- 阈值

#: 死元组占比超过该值且绝对量超过 `_DEAD_TUP_MIN` → 膨胀告警。
_DEAD_TUP_RATIO = 0.2
_DEAD_TUP_MIN = 10_000
#: 行数低于该值的表不参与膨胀判定（统计噪声）。
_MIN_ROWS_FOR_BLOAT = 1_000
#: autovacuum 距上次超过该时长且死元组偏多 → 滞后告警。
_AUTOVACUUM_STALE = dt.timedelta(days=7)
#: 小于该体积的零扫描索引不提示（新建库/统计重置期的噪声）。
_UNUSED_INDEX_MIN_BYTES = 10 * 1024 * 1024
#: 连接池占用率达到该比例 → 降级；≥100% → 失败。
_POOL_SATURATION_RATIO = 0.8
#: `events` 保留策略（ADR-009：>24 个月归档）。
_EVENT_RETENTION_DAYS = 24 * 30

# ---------------------------------------------------------------- SQL

_SQL_TABLES = """
SELECT relname,
       n_live_tup,
       pg_total_relation_size(relid) AS size_bytes,
       n_dead_tup,
       last_autovacuum
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC
"""

_SQL_INDEXES = """
SELECT indexrelname, idx_scan, pg_relation_size(indexrelid) AS size_bytes
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC, pg_relation_size(indexrelid) DESC
"""

#: 'p' = 分区表，'r' = 普通表，None = 不存在。
_SQL_EVENTS_RELKIND = "SELECT relkind FROM pg_class WHERE relname = 'events' LIMIT 1"

_SQL_EVENTS_PARTITIONS = """
SELECT c.relname, pg_get_expr(c.relpartbound, c.oid) AS bound
FROM pg_class c
JOIN pg_inherits i ON i.inhrelid = c.oid
JOIN pg_class p ON p.oid = i.inhparent
WHERE p.relname = 'events'
ORDER BY c.relname
"""

_BOUND_FROM = re.compile(r"FROM \('([^']+)'\)")
_BOUND_TO = re.compile(r"TO \('([^']+)'\)")


class _CamelModel(BaseModel):
    """HTTP 序列化统一 camelCase（§6 横切）。"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class TableHealth(_CamelModel):
    """表的容量与膨胀状态。"""

    name: str
    rows: int
    size_bytes: int
    dead_tup: int
    last_autovacuum: dt.datetime | None


class IndexHealth(_CamelModel):
    """索引使用率（`scans == 0` → 建议清理）。"""

    name: str
    scans: int
    size_bytes: int


class PartitionHealth(_CamelModel):
    """`events` 分区完整性（下一月是否已建）与最老分区起点。"""

    events_next_missing: bool
    oldest_event_ts: dt.datetime | None


class PoolHealth(_CamelModel):
    """应用连接池采样（未注入 engine 时全 0 = 未知）。"""

    size: int
    checkedout: int
    overflow: int


class HealthReport(_CamelModel):
    """巡检报告（`agenticdocer stats --health` 与 M09B `perf_health` detector 共用）。"""

    tables: list[TableHealth]
    indexes: list[IndexHealth]
    partitions: PartitionHealth
    pool: PoolHealth
    verdict: Literal["ok", "degraded", "fail"]
    advice: list[str]


# ---------------------------------------------------------------- 工具


def normalize_dsn(dsn: str) -> str:
    """把 SQLAlchemy 风格 DSN 还原为 asyncpg 可用的纯 DSN。"""
    return re.sub(r"^postgresql\+\w+://", "postgresql://", dsn.strip())


def pool_health(engine: Any | None) -> PoolHealth:
    """从 SQLAlchemy Engine/AsyncEngine（或裸 pool）采样连接池；失败/缺省返回全 0。"""
    if engine is None:
        return PoolHealth(size=0, checkedout=0, overflow=0)
    pool = getattr(engine, "pool", engine)
    try:
        return PoolHealth(
            size=int(pool.size()),
            checkedout=int(pool.checkedout()),
            overflow=int(pool.overflow()),
        )
    except Exception:  # noqa: BLE001 — 采样失败等价于「未知」，不应影响巡检结论
        return PoolHealth(size=0, checkedout=0, overflow=0)


def _aware(value: dt.datetime | None) -> dt.datetime | None:
    if value is None:
        return None
    return value if value.tzinfo is not None else value.replace(tzinfo=dt.timezone.utc)


def _human_mib(size_bytes: int) -> str:
    return f"{size_bytes / (1024 * 1024):.1f} MiB"


# ---------------------------------------------------------------- 判定


def evaluate_health(
    *,
    tables: list[TableHealth],
    indexes: list[IndexHealth],
    partitions: PartitionHealth,
    pool: PoolHealth,
) -> HealthReport:
    """由巡检数据推导 `verdict` 与可执行建议（纯函数）。"""
    advice: list[str] = []
    verdict: Literal["ok", "degraded", "fail"] = "ok"

    def degrade(message: str) -> None:
        nonlocal verdict
        if verdict == "ok":
            verdict = "degraded"
        advice.append(message)

    def fail(message: str) -> None:
        nonlocal verdict
        verdict = "fail"
        advice.append(message)

    if partitions.events_next_missing:
        fail("events 未来月份分区缺失：事件写入将失败；请创建下月分区（CREATE TABLE ... PARTITION OF events FOR VALUES FROM (...) TO (...)，见 ADR-009 §4.2）")

    now = dt.datetime.now(dt.timezone.utc)
    for table in tables:
        dead_ratio = table.dead_tup / table.rows if table.rows else 0.0
        if (
            table.rows >= _MIN_ROWS_FOR_BLOAT
            and table.dead_tup >= _DEAD_TUP_MIN
            and dead_ratio > _DEAD_TUP_RATIO
        ):
            degrade(
                f"表 {table.name} 膨胀：dead_tup={table.dead_tup}/{table.rows}（{dead_ratio:.0%}）；"
                f"建议 VACUUM (ANALYZE) {table.name} 并调低该表 autovacuum scale_factor"
            )
        last = _aware(table.last_autovacuum)
        if table.dead_tup >= _DEAD_TUP_MIN and (last is None or now - last > _AUTOVACUUM_STALE):
            stale_for = "从未执行" if last is None else f"{(now - last).days} 天未执行"
            degrade(
                f"表 {table.name} autovacuum 滞后（{stale_for}，n_dead_tup={table.dead_tup}）；"
                "检查 autovacuum 参数与长事务"
            )

    for index in indexes:
        if index.scans == 0 and index.size_bytes >= _UNUSED_INDEX_MIN_BYTES:
            degrade(
                f"未使用索引 {index.name}（{_human_mib(index.size_bytes)}，idx_scan=0）："
                f"确认无查询依赖后 DROP INDEX {index.name}"
            )

    capacity = pool.size + pool.overflow
    if capacity > 0:
        ratio = pool.checkedout / capacity
        if ratio >= 1.0:
            fail(
                f"连接池已打满（checkedout={pool.checkedout}/容量 {capacity}）；"
                "扩容 pool_size/max_overflow 或排查连接泄漏"
            )
        elif ratio >= _POOL_SATURATION_RATIO:
            degrade(
                f"连接池接近饱和（checkedout={pool.checkedout}/容量 {capacity}，{ratio:.0%}）；"
                "建议提高 pool_size 或减少长事务"
            )

    oldest = _aware(partitions.oldest_event_ts)
    if oldest is not None and now - oldest > dt.timedelta(days=_EVENT_RETENTION_DAYS):
        degrade(
            f"events 最老分区起点 {oldest.date()} 超过 24 个月保留策略（ADR-009）；"
            "请归档并 DROP 逾期分区"
        )

    return HealthReport(
        tables=tables,
        indexes=indexes,
        partitions=partitions,
        pool=pool,
        verdict=verdict,
        advice=advice,
    )


# ---------------------------------------------------------------- 取数


@dataclass
class _Probe:
    """`health()` 的取数结果（含目录级异常提示）。"""

    tables: list[TableHealth] = field(default_factory=list)
    indexes: list[IndexHealth] = field(default_factory=list)
    partitions: PartitionHealth = field(
        default_factory=lambda: PartitionHealth(events_next_missing=False, oldest_event_ts=None)
    )
    advice: list[str] = field(default_factory=list)
    hard_fail: bool = False
    degraded: bool = False


def _next_month_start(now: dt.datetime) -> dt.datetime:
    year, month = (now.year + 1, 1) if now.month == 12 else (now.year, now.month + 1)
    return now.replace(
        year=year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0
    )


def _bound_ts(pattern: re.Pattern[str], bound: str) -> dt.datetime | None:
    match = pattern.search(bound or "")
    if match is None:
        return None  # MINVALUE / MAXVALUE / DEFAULT
    try:
        return _aware(dt.datetime.fromisoformat(match.group(1)))
    except ValueError:
        return None


async def _probe(dsn: str, timeout: float) -> _Probe:
    """连库取巡检数据；对空库/未迁移库给出目录级提示。"""
    connection = await asyncpg.connect(normalize_dsn(dsn), timeout=timeout)
    try:
        table_rows = await connection.fetch(_SQL_TABLES)
        index_rows = await connection.fetch(_SQL_INDEXES)
        relkind = await connection.fetchval(_SQL_EVENTS_RELKIND)
        bound_rows = await connection.fetch(_SQL_EVENTS_PARTITIONS)
    finally:
        await connection.close()

    probe = _Probe(
        tables=[
            TableHealth(
                name=row["relname"],
                rows=int(row["n_live_tup"] or 0),
                size_bytes=int(row["size_bytes"] or 0),
                dead_tup=int(row["n_dead_tup"] or 0),
                last_autovacuum=row["last_autovacuum"],
            )
            for row in table_rows
        ],
        indexes=[
            IndexHealth(
                name=row["indexrelname"],
                scans=int(row["idx_scan"] or 0),
                size_bytes=int(row["size_bytes"] or 0),
            )
            for row in index_rows
        ],
    )

    bounds = [(_bound_ts(_BOUND_FROM, row["bound"]), _bound_ts(_BOUND_TO, row["bound"])) for row in bound_rows]
    oldest = min((lower for lower, _ in bounds if lower is not None), default=None)

    if relkind is None:
        probe.partitions = PartitionHealth(events_next_missing=True, oldest_event_ts=None)
        probe.advice.append("events 表缺失：迁移未执行（alembic upgrade head）")
        probe.hard_fail = True
        return probe

    if relkind == "p":
        next_start = _next_month_start(dt.datetime.now(dt.timezone.utc))
        covered = any(
            lower is not None and lower <= next_start and (upper is None or next_start < upper)
            for lower, upper in bounds
        )
        probe.partitions = PartitionHealth(events_next_missing=not covered, oldest_event_ts=oldest)
    else:
        # 普通表（尚未分区）：写入不会失败，但失去分区维护与归档检查能力。
        probe.partitions = PartitionHealth(events_next_missing=False, oldest_event_ts=oldest)
        probe.advice.append(
            "events 尚未按 ts RANGE 分区（ADR-009 §4.2）：月初写入前请完成分区化，"
            "否则归档逾期检查不可用"
        )
        probe.degraded = True
    return probe


async def health(
    *,
    dsn: str | None = None,
    engine: Any | None = None,
    timeout: float = 5.0,
) -> HealthReport:
    """执行巡检并返回报告；结果同时写入 `m12.health` 日志（含 `DTO_PARTITION_MISSING`）。"""
    logger = get_logger("m12.health")
    target = dsn or os.environ.get("DATABASE_URL") or ""
    started = time.perf_counter()

    if not target:
        report = HealthReport(
            tables=[],
            indexes=[],
            partitions=PartitionHealth(events_next_missing=False, oldest_event_ts=None),
            pool=pool_health(engine),
            verdict="fail",
            advice=["未配置 DATABASE_URL：无法巡检数据库"],
        )
        logger.error("健康巡检失败：缺少 DATABASE_URL", error_code=ErrorCode.IO_NOT_FOUND)
        return report

    try:
        probe = await _probe(target, timeout)
    except Exception as exc:  # noqa: BLE001 — 巡检必须给出结论而非抛出
        report = HealthReport(
            tables=[],
            indexes=[],
            partitions=PartitionHealth(events_next_missing=False, oldest_event_ts=None),
            pool=pool_health(engine),
            verdict="fail",
            advice=[f"数据库连接失败（{type(exc).__name__}: {exc}）；检查 DATABASE_URL、PG 状态与凭据"],
        )
        logger.error(
            "健康巡检失败：数据库连接失败",
            error_code=ErrorCode.NET_CONN_REFUSED,
            reason=f"{type(exc).__name__}: {exc}",
        )
        return report

    report = evaluate_health(
        tables=probe.tables,
        indexes=probe.indexes,
        partitions=probe.partitions,
        pool=pool_health(engine),
    )
    if probe.advice:
        verdict: Literal["ok", "degraded", "fail"] = report.verdict
        if probe.hard_fail:
            verdict = "fail"
        elif probe.degraded and verdict == "ok":
            verdict = "degraded"
        report = report.model_copy(
            update={"advice": [*probe.advice, *report.advice], "verdict": verdict}
        )

    logger.info(
        "健康巡检完成",
        dur=int((time.perf_counter() - started) * 1000),
        verdict=report.verdict,
        tables=len(report.tables),
        indexes=len(report.indexes),
    )
    if report.partitions.events_next_missing:
        logger.error(
            "events 下一月分区缺失",
            error_code=DTO_PARTITION_MISSING,
            oldest_event_ts=str(report.partitions.oldest_event_ts),
        )
    for line in report.advice:
        logger.warn("巡检建议", advice=line)
    return report


def health_sync(**kwargs: Any) -> HealthReport:
    """`health()` 的同步包装（CLI/M09B 同步路径）；事件循环内请改用 `await health()`。"""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(health(**kwargs))
    raise RuntimeError("health_sync() 不能在事件循环内调用；请 await health()")


__all__ = [
    "HealthReport",
    "IndexHealth",
    "PartitionHealth",
    "PoolHealth",
    "TableHealth",
    "evaluate_health",
    "health",
    "health_sync",
    "normalize_dsn",
    "pool_health",
]
