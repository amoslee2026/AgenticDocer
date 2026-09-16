"""M03 批量写入路径：ADR-009 §3「批量导入：单事务分批（每 5k 行）」的落地。

背景（PerfBench 实测 + Main 裁决 B-1）：逐节点事务下 `commit_document` 吞吐仅
**57–106 节点/s** → 13.4M 节点需 35–40 小时，10k 文档导入无工程可行性。瓶颈在
**每节点一个事务**（含 M02 的「事件 + 实体同事务」往返与逐行索引维护），而非索引本身。

本模块把写入折叠为「**每 5k 行一个事务** + 事务内多条多值语句」：

- 事务边界（P2）：**一个批次 = 一个事务**，批内「节点行 + 其 create 事件」原子写入，
  与逐节点路径同语义（失败整批回滚，重跑幂等）；
- 身份与层级：`node_id` 在**规划期**一次分配（`new_uuid7()`），故父链（`level` + `ordinal`
  栈重建）与 `cross_ref` 目标都能在写入前解析，无需 `RETURNING`，也无需二次扫描；
- 行形状：复用 M02 的 `node_values` / `field_deltas`（**同一口径**，P5）——批量路径造出的
  行与逐节点路径逐字段一致，这是「语义等价」断言的基础；
- 幂等：既有锚且无字段变化 → 不写行、不写事件（与逐节点路径一致）；有变化 → 回落到
  M02 `upsert_node`（罕见路径，保留乐观锁与事件载荷口径）；
- 校验（M09A）与 `WriteContext` 记账仍在 `commit_document` 前置，本模块不绕过任何判据。

**不做**：不推迟/删除任何索引（含 FTS GIN），不跳过事件（P2 硬要求）。
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Final
from uuid import UUID

from sqlalchemy import insert

from agenticdocer.model import WriteContext, new_uuid7
from agenticdocer.observability import get_logger
from agenticdocer.store.db import Database
from agenticdocer.store.nodes import node_values
from agenticdocer.store.rows import field_deltas, jsonable, now, row_to_dict
from agenticdocer.store.schema import events, nodes

__all__ = [
    "BULK_ROWS_PER_STATEMENT",
    "BULK_ROWS_PER_TRANSACTION",
    "BulkWriteResult",
    "bulk_insert_nodes",
]

log = get_logger("m03.bulk")

BULK_ROWS_PER_STATEMENT: Final = 500
"""单条多值 INSERT 的行数（10 列 × 500 = 5,000 参数，远低于 asyncpg 的 32,767 上限）。"""

BULK_ROWS_PER_TRANSACTION: Final = 5000
"""一个事务的行数（ADR-009 §3：每 5k 行一批）。"""


@dataclass
class BulkWriteResult:
    """批量写入结果。"""

    created: int = 0
    node_ids: dict[str, UUID] = field(default_factory=dict)
    """`anchor` → 本次提交使用的 `node_id`（含既有节点复用者）。"""


def _node_record(anchor: str, node_id: UUID, incoming: dict[str, Any], created_at: Any) -> dict[str, Any]:
    return node_values(node_id, incoming, created_at=created_at)


def _event_record(node_id: UUID, record: dict[str, Any], actor: str, ts: Any) -> dict[str, Any]:
    """create 事件行（载荷与 M02 `append_event` 同口径：`field_deltas({}, record, include_unchanged=True)`）。"""
    return {
        "event_id": new_uuid7(),
        "entity": "node",
        "entity_id": str(node_id),
        "op": "create",
        "payload": jsonable(field_deltas({}, record, include_unchanged=True)),
        "actor": actor,
        "ts": ts,
    }


async def bulk_insert_nodes(
    db: Database,
    specs: Sequence[tuple[str, UUID, dict[str, Any]]],
    ctx: WriteContext,
    *,
    rows_per_statement: int = BULK_ROWS_PER_STATEMENT,
    rows_per_transaction: int = BULK_ROWS_PER_TRANSACTION,
) -> BulkWriteResult:
    """批量写入新节点（+ 其 create 事件）：``specs = [(anchor, node_id, incoming), …]``。

    - 每 `rows_per_transaction` 行一个事务，事务内按 `rows_per_statement` 切多条多值语句；
    - 节点行与其事件行**同事务**（P2）：先写节点语句、再写对应事件语句，异常整批回滚；
    - 行形状复用 M02 `node_values`（含 `status='active'`、`version=1`），与逐节点路径同口径。
    """
    result = BulkWriteResult()
    if not specs:
        return result
    for start in range(0, len(specs), rows_per_transaction):
        window = specs[start : start + rows_per_transaction]
        timestamp = now()
        node_rows: list[dict[str, Any]] = []
        event_rows: list[dict[str, Any]] = []
        for anchor, node_id, incoming in window:
            record = _node_record(anchor, node_id, incoming, timestamp)
            node_rows.append(record)
            event_rows.append(_event_record(node_id, record, ctx.actor, timestamp))
            result.node_ids[anchor] = node_id
        async with db.transaction() as session:
            for offset in range(0, len(node_rows), rows_per_statement):
                await session.execute(insert(nodes), node_rows[offset : offset + rows_per_statement])
            for offset in range(0, len(event_rows), rows_per_statement):
                await session.execute(insert(events), event_rows[offset : offset + rows_per_statement])
        result.created += len(node_rows)
        log.info(
            "bulk batch committed",
            batch_rows=len(node_rows),
            batch_index=start // rows_per_transaction,
            doc_id=window[0][2].get("doc_id"),
        )
    return result
