"""ADR-009 分区几何与 §4 DDL 摘要的单测（纯函数，不需要 PG）。

集成测试在真实库上断言分区存在；本文件补的是**生成逻辑的边界**（月份回卷/命名/数量）——
`events_partition_statements` 也是 §5「新分区由定时任务创建」要复用的公共接口。
"""

from __future__ import annotations

from datetime import datetime, timezone

from agenticdocer.store.db import DEFAULT_DATABASE_URL, DEFAULT_MIGRATION_DATABASE_URL
from agenticdocer.store.schema import (
    EVENTS_DEFAULT_PARTITION,
    NODES_PARTITION_COUNT,
    events_partition_name,
    events_partition_statements,
    metadata,
    nodes_partition_statements,
    privilege_statements,
)

REFERENCE = datetime(2026, 9, 16, 12, 0, tzinfo=timezone.utc)


def _partition_names(statements: list[str]) -> list[str]:
    """`CREATE TABLE IF NOT EXISTS <name> PARTITION OF ...` → `<name>`。"""
    return [statement.split()[5] for statement in statements]


def test_nodes_hash_partition_geometry() -> None:
    statements = nodes_partition_statements()

    assert len(statements) == NODES_PARTITION_COUNT == 64
    assert statements[0] == (
        "CREATE TABLE IF NOT EXISTS nodes_p0 PARTITION OF nodes "
        "FOR VALUES WITH (MODULUS 64, REMAINDER 0)"
    )
    assert _partition_names(statements)[0] == "nodes_p0"
    assert statements[-1].endswith("(MODULUS 64, REMAINDER 63)")
    # 幂等（迁移重跑 / 维护任务可重复执行）
    assert all("IF NOT EXISTS" in statement for statement in statements)


def test_events_partition_names_are_monthly() -> None:
    assert events_partition_name(REFERENCE) == "events_202609"
    assert events_partition_name(datetime(2026, 12, 1, tzinfo=timezone.utc)) == "events_202612"


def test_events_partitions_cover_current_and_next_three_months() -> None:
    statements = events_partition_statements(REFERENCE)

    assert _partition_names(statements) == [
        "events_202609",
        "events_202610",
        "events_202611",
        "events_202612",
        EVENTS_DEFAULT_PARTITION,
    ]
    assert statements[0].endswith(
        "FROM ('2026-09-01T00:00:00+00:00') TO ('2026-10-01T00:00:00+00:00')"
    )
    assert statements[-1].endswith(f"{EVENTS_DEFAULT_PARTITION} PARTITION OF events DEFAULT")


def test_events_partitions_roll_over_the_year_boundary() -> None:
    statements = events_partition_statements(datetime(2026, 12, 31, tzinfo=timezone.utc))

    assert _partition_names(statements)[:4] == [
        "events_202612",
        "events_202701",
        "events_202702",
        "events_202703",
    ]
    assert statements[0].endswith(
        "FROM ('2026-12-01T00:00:00+00:00') TO ('2027-01-01T00:00:00+00:00')"
    )


def test_events_default_partition_can_be_omitted() -> None:
    statements = events_partition_statements(REFERENCE, include_default=False)

    assert len(statements) == 4
    assert all("DEFAULT" not in statement for statement in statements)


def test_metadata_declares_the_thirteen_tables() -> None:
    assert len(metadata.tables) == 13
    assert set(metadata.tables) == {
        "docs",
        "nodes",
        "refs",
        "events",
        "comments",
        "schemas",
        "assets",
        "terms",
        "users",
        "ssh_keys",
        "grants",
        "sessions",
        "nonces",
    }


def test_primary_keys_and_downgraded_foreign_keys() -> None:
    """ADR-009：主键含分区键；分区表上仅保留 `nodes.doc_id → docs` 一处外键。"""
    nodes = metadata.tables["nodes"]
    events = metadata.tables["events"]

    assert [column.name for column in nodes.primary_key] == ["node_id", "doc_id"]
    assert [column.name for column in events.primary_key] == ["event_id", "ts"]
    assert {fk.parent.name for fk in nodes.foreign_keys} == {"doc_id"}
    assert {fk.parent.name for fk in metadata.tables["refs"].foreign_keys} == set()
    assert {fk.parent.name for fk in metadata.tables["comments"].foreign_keys} == set()
    assert {fk.parent.name for fk in metadata.tables["terms"].foreign_keys} == set()
    assert "text_fts" in nodes.c
    assert DEFAULT_DATABASE_URL.endswith("agenticdocer_test")
    assert DEFAULT_MIGRATION_DATABASE_URL.endswith("agenticdocer")


def test_privilege_statements_skip_absent_role() -> None:
    """角色不存在（建库阶段未执行 §4.3 的 CREATE ROLE）时跳过授权并留说明。"""

    class _Connection:
        def execute(self, statement, parameters=None):
            class _Result:
                def first(self):
                    return None

            return _Result()

    statements, notes = privilege_statements(_Connection(), app_role="nobody_here")

    assert statements == []
    assert notes and "nobody_here" in notes[0]
