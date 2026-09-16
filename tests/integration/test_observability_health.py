"""M12 健康巡检的真实 PG 回归（REQ-M12-F05）。

**为什么必须连真实库**：本模块的 `_probe()` 是「SQL 结果 → `HealthReport`」的映射层，
其缺陷几乎全部来自**驱动类型假设与真实不一致**，而 mock 会自我印证该假设：

* `pg_class.relkind` 是 PG 内部类型 `"char"`，asyncpg 返回 **`bytes`**（实测 `b'p'`）。
  此前 fake 连接返回 `"p"`（str），使 `relkind == "p"` 的恒假缺陷在全绿单测下存活；
* 分区边界文本 `pg_get_expr(relpartbound, …)` 的真实形状也需在真库上校验。

因此本文件用**独立 oracle**（不复用被测的解析/判定代码）取真值，再与被测结果比对。
夹具复用 `tests/integration/conftest.py` 的 `database_urls`/`migrated_schema`
（`*_test` 库；PG 不可用则整体 skip）。
"""

from __future__ import annotations

import asyncio
import datetime as dt
import re

import asyncpg
import pytest

from agenticdocer.observability import health_sync, normalize_dsn

pytestmark = pytest.mark.integration

# 独立写法（故意不复用被测模块的正则/函数）。
_BOUND_LO = re.compile(r"FROM \('([^']+)'\)")
_BOUND_HI = re.compile(r"TO \('([^']+)'\)")


def _next_month_start(now: dt.datetime) -> dt.datetime:
    year, month = (now.year + 1, 1) if now.month == 12 else (now.year, now.month + 1)
    return now.replace(year=year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)


async def _oracle(app_url: str) -> tuple[str | None, list[dt.datetime], bool]:
    """直接查目录取真值：`(relkind 归一, events 各分区下界, 下一月是否已覆盖)`。"""
    connection = await asyncpg.connect(normalize_dsn(app_url), timeout=5)
    try:
        raw = await connection.fetchval("SELECT relkind FROM pg_class WHERE relname = 'events' LIMIT 1")
        rows = await connection.fetch(
            """
            SELECT pg_get_expr(c.relpartbound, c.oid) AS bound
            FROM pg_class c
            JOIN pg_inherits i ON i.inhrelid = c.oid
            JOIN pg_class p ON p.oid = i.inhparent
            WHERE p.relname = 'events'
            """
        )
    finally:
        await connection.close()

    relkind = raw.decode() if isinstance(raw, (bytes, bytearray)) else raw
    lowers: list[dt.datetime] = []
    spans: list[tuple[dt.datetime, dt.datetime | None]] = []
    for row in rows:
        bound = row["bound"] or ""
        lo = _BOUND_LO.search(bound)
        hi = _BOUND_HI.search(bound)
        if lo is None:
            continue  # MINVALUE / DEFAULT 分区无下界
        lower = dt.datetime.fromisoformat(lo.group(1))
        lowers.append(lower)
        spans.append((lower, dt.datetime.fromisoformat(hi.group(1)) if hi else None))

    target = _next_month_start(dt.datetime.now(dt.timezone.utc))
    covered = any(lower <= target and (upper is None or target < upper) for lower, upper in spans)
    return relkind, lowers, covered


def test_health_matches_independent_oracle_on_real_db(
    database_urls: tuple[str, str], migrated_schema: str
) -> None:
    """已迁移库上：relkind 不得被误判，分区覆盖/最老分区须与独立 oracle 逐项一致。"""
    _, app_url = database_urls
    relkind, lowers, covered = asyncio.run(_oracle(app_url))
    assert relkind == "p", "本用例假设迁移后的 events 为分区表（ADR-009 §4.2）"

    report = health_sync(dsn=app_url, timeout=5.0)

    # 1) relkind 归一：已分区表不得落入「普通表」分支（缺陷签名 = 该建议出现）
    assert not any("尚未按 ts RANGE 分区" in advice for advice in report.advice)
    assert not any("events 表缺失" in advice for advice in report.advice)

    # 2) 分区覆盖判定与独立 oracle 一致；缺下月分区 → missing 且 fail
    assert report.partitions.events_next_missing is (not covered)
    assert (report.verdict == "fail") is (not covered)

    # 3) 最老分区起点与 oracle 逐值一致（验证边界文本解析）
    expected_oldest = min(lowers) if lowers else None
    assert report.partitions.oldest_event_ts == expected_oldest
    if expected_oldest is not None:
        assert report.partitions.oldest_event_ts.tzinfo is not None


def test_health_probe_reads_real_table_and_index_stats(
    database_urls: tuple[str, str], migrated_schema: str
) -> None:
    """表/索引巡检项须反映真实目录（行数、条目存在性、类型可运算）。"""
    _, app_url = database_urls
    report = health_sync(dsn=app_url, timeout=5.0)

    assert report.tables, "已迁移库应至少含 docs/nodes/events 等用户表"
    assert {table.name for table in report.tables} >= {"nodes", "events"}
    for table in report.tables:
        assert table.rows >= 0 and table.size_bytes > 0
        assert isinstance(table.dead_tup, int)
        assert table.last_autovacuum is None or isinstance(table.last_autovacuum, dt.datetime)

    assert report.indexes, "已迁移库应有索引"
    assert all(isinstance(index.scans, int) for index in report.indexes)
    assert all(index.size_bytes > 0 for index in report.indexes)

    # 未注入 engine/pool 时连接池采样为 0，不得据此告警
    assert report.pool.size == 0
    assert not any("连接池" in advice for advice in report.advice)
