"""M03 批量写入路径：ADR-009 §3「批量导入：`COPY` + 单事务分批（每 5k 行）」的落地。

背景（PerfBench 实测 + Main 裁决 B-1）：逐节点事务下 `commit_document` 吞吐仅
**57–106 节点/s** → 13.4M 节点需 35–40 小时，10k 文档导入无工程可行性。瓶颈在
**每节点一个事务**（事件 + 实体同事务的逐次往返与逐行索引维护），而非索引本身。

本模块把写入折叠为「**每 5k 行一个事务**（ADR-009 §3 原文）+ 事务内 `COPY`」：

- 传输用 `asyncpg.copy_records_to_table`（消除逐行参数编解码与逐行 round-trip）；
- **P2 硬要求**：一个批次 = 一个事务，批内「节点行 + 其 create 事件行」原子写入；
  失败整批回滚，重跑幂等（既有锚且无变化 → 不写行、不写事件）；
- **身份在规划期分配**：`node_id` 由 `new_uuid7()` 提前生成，故父链（`level`+`ordinal`
  栈重建）与 `cross_ref` 目标可在写入前解析，无需 `RETURNING`，也无需二次扫描；
- **行形状同口径（P5）**：复用 M02 `node_values` / `field_deltas`，批量路径造出的行与
  逐节点路径逐字段一致——这是「语义等价」断言的基础；
- 列清单由 `nodes.c` / `events.c` 中 **`computed is None`** 的列推出（跳过 `text_fts` 等生成列）；
- **不**推迟/删除任何索引（含 FTS GIN），**不**跳过事件。

M02Store 未提供 `Storage.bulk_*` 原语（已协调），故此处 asyncpg 直连实现——Main 批准的
兜底路径（「若他不做你可用 asyncpg 直连实现，但要说明」）。
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Final
from uuid import UUID

from agenticspec.model import WriteContext, new_uuid7
from agenticspec.observability import get_logger
from agenticspec.store.db import Database
from agenticspec.store.nodes import node_values
from agenticspec.store.rows import field_deltas, jsonable, now
from agenticspec.store.schema import events, nodes

__all__ = [
    "BULK_ROWS_PER_TRANSACTION",
    "BulkWriteResult",
    "bulk_insert_nodes",
    "copy_columns",
]

log = get_logger("m03.bulk")

BULK_ROWS_PER_TRANSACTION: Final = 5000
"""一个事务的行数（ADR-009 §3：每 5k 行一批）。"""


def copy_columns(table: Any) -> tuple[str, ...]:
    """`COPY` 可写的列（跳过生成列，如 `nodes.text_fts`）。"""
    return tuple(column.name for column in table.c if column.computed is None)


NODE_COPY_COLUMNS: Final = copy_columns(nodes)
EVENT_COPY_COLUMNS: Final = copy_columns(events)
_JSON_COLUMNS: Final = frozenset({"content", "payload"})


@dataclass
class BulkWriteResult:
    """批量写入结果。"""

    created: int = 0
    node_ids: dict[str, UUID] = field(default_factory=dict)
    """`anchor` → 本次提交使用的 `node_id`（含复用既有节点者）。"""


def _cell(column: str, value: Any) -> Any:
    """单元格取值：jsonb 列须为 JSON 文本（asyncpg 的 COPY 不做对象编解码）。"""
    if column in _JSON_COLUMNS and not isinstance(value, str):
        return json.dumps(jsonable(value), ensure_ascii=False)
    return value


def _row(columns: Sequence[str], record: dict[str, Any]) -> list[Any]:
    return [_cell(column, record.get(column)) for column in columns]


async def _copy(session: Any, table: Any, columns: Sequence[str], records: list[dict[str, Any]]) -> None:
    """在会话当前事务内执行一次 `COPY`（asyncpg 直连：与 SQLAlchemy 会话同连接同事务）。"""
    connection = await session.connection()
    raw = await connection.get_raw_connection()
    driver = raw.driver_connection
    await driver.copy_records_to_table(
        table.name,
        records=[_row(columns, record) for record in records],
        columns=list(columns),
    )


async def bulk_insert_nodes(
    db: Database,
    specs: Sequence[tuple[str, UUID, dict[str, Any]]],
    ctx: WriteContext,
    *,
    rows_per_transaction: int = BULK_ROWS_PER_TRANSACTION,
) -> BulkWriteResult:
    """批量写入新节点 + 其 create 事件：``specs = [(anchor, node_id, incoming), …]``。

    - 每 `rows_per_transaction` 行**一个事务**；事务内先 `COPY` 节点行、再 `COPY` 事件行（P2）；
    - 节点行形状复用 M02 `node_values`（`status='active'`、`version=1`、批内时间戳一致）；
    - create 事件载荷复用 M02 `field_deltas({}, record, include_unchanged=True)`（口径单一）。
    """
    result = BulkWriteResult()
    if not specs:
        return result
    total = len(specs)
    for start in range(0, total, rows_per_transaction):
        window = specs[start : start + rows_per_transaction]
        timestamp = now()
        node_rows: list[dict[str, Any]] = []
        event_rows: list[dict[str, Any]] = []
        for anchor, node_id, incoming in window:
            record = node_values(node_id, incoming, created_at=timestamp)
            node_rows.append(record)
            event_rows.append(
                {
                    "event_id": new_uuid7(),
                    "entity": "node",
                    "entity_id": str(node_id),
                    "op": "create",
                    "payload": field_deltas({}, record, include_unchanged=True),
                    "actor": ctx.actor,
                    "ts": timestamp,
                }
            )
            result.node_ids[anchor] = node_id
        async with db.transaction() as session:
            await _copy(session, nodes, NODE_COPY_COLUMNS, node_rows)
            await _copy(session, events, EVENT_COPY_COLUMNS, event_rows)
        result.created += len(node_rows)
        log.info(
            "bulk batch committed",
            batch_rows=len(node_rows),
            batch_index=start // rows_per_transaction,
            doc_id=window[0][2].get("doc_id"),
        )
    log.info(
        "bulk insert done",
        created=result.created,
        batches=(total + rows_per_transaction - 1) // rows_per_transaction,
    )
    return result
