"""M05 关键词检索（PG FTS，ADR-005；**内部实现，无公开端点**——ADR-008）。

- 选型：`tsvector`（`english` 配置）全文检索 + `websearch_to_tsquery` 查询语法
  （词/短语/布尔），相关度用 `ts_rank`（ADR-005「Decision」）；
- 索引：`nodes.text_fts` STORED 生成列 + GIN（`idx_nodes_fts`，M02 已建；ADR-009 V23
  裁决保留）——生成列表达式锁定为 `to_tsvector('english', coalesce(content->>'text',''))`，
  故**查询必须用同一配置** `english` 才能命中该索引（:data:`FTS_CONFIG`）；
- 消费方：M-LR 导出、M09B 质量门（次要）；对外检索由 LightRAG 承担（ADR-008 边界表）；
- 默认过滤 `status='deleted'`（L5）；空间上 `nodes` 按 `doc_id` HASH 64 分区，FTS 是
  **跨全部分区**的索引扫描（查询不带 `doc_id`，无裁剪面——这与 traverse 的分区约束不同）；
- 无 LLM、无网络：确定性 FTS（P6）。
"""

from __future__ import annotations

from typing import Final

from sqlalchemy import cast, desc, func, literal, select
from sqlalchemy.dialects.postgresql import REGCONFIG

from sqlalchemy import cast, desc, func, literal, select, true
from agenticdocer.observability import get_logger, slow_query_ms
from agenticdocer.store import Storage, ValidationError, get_storage
from agenticdocer.store.schema import nodes

__all__ = ["FTS_CONFIG", "search_text"]

log = get_logger("m05.search")

FTS_CONFIG: Final = "english"
"""`nodes.text_fts` 生成列所用配置（ADR-005）；改配置需同时改迁移里的生成列。"""


async def search_text(
    q: str,
    limit: int = 50,
    *,
    storage: Storage | None = None,
    include_deleted: bool = False,
) -> list[SearchHit]:
    """关键词全文检索（REQ-M05-F02；内部接口，ADR-008）。

    参数：
        q: 检索串（`websearch_to_tsquery` 语法：词、`"短语"`、`or`、`-词`）。
           空串/纯空白 → `[]`（不查库）。
        limit: 命中上限（默认 50，§3 M05 契约）；须 ≥1。
        storage: `Storage` 注入（缺省取进程级单例）。
        include_deleted: 同时纳入 `status='deleted'` 节点（默认过滤，L5）。

    返回：`SearchHit[]`（`node_id`/`doc_id`/`anchor`/`score`），按 `score` 降序 →
    `doc_id` → `ordinal` 排序；`q` 只含停用词/操作符时不报错，返回 `[]`
    （`websearch_to_tsquery` 产出空 tsquery，`@@` 无命中）。
    """
    if not isinstance(q, str):
        raise ValidationError(f"query must be a str, got {type(q).__name__}", entity="node")
    if limit < 1:
        raise ValidationError(f"limit must be >= 1, got {limit}", entity="node")
    query_text = q.strip()
    if not query_text:
        return []
    store = get_storage() if storage is None else storage
    with log.timer("search_text", budget_ms=slow_query_ms(), limit=limit):
        # tsquery CTE 只算一次（`ts_rank` 需按行求值，重复求值会在命中集大时放大开销）；
        # 单行 CTE 与 `nodes` 的显式 `JOIN ... ON true` —— 与隐式逗号交叉连接等价，但不触发
        # SQLAlchemy 的 cartesian-product 警告。
        match = select(
            func.websearch_to_tsquery(cast(literal(FTS_CONFIG), REGCONFIG), query_text).label(
                "query"
            )
        ).cte("tsq")
        statement = (
            select(
                nodes.c.node_id,
                nodes.c.doc_id,
                nodes.c.anchor,
                func.ts_rank(nodes.c.text_fts, match.c.query).label("score"),
            )
            .select_from(nodes.join(match, true()))
            .where(nodes.c.text_fts.op("@@")(match.c.query))
            .order_by(desc("score"), nodes.c.doc_id, nodes.c.ordinal, nodes.c.node_id)
            .limit(limit)
        )
        if not include_deleted:
            statement = statement.where(nodes.c.status == "active")
        async with store.db.session() as session:
            rows = (await session.execute(statement)).all()
    log.info("search_text", limit=limit, hits=len(rows), query_chars=len(query_text))
    return [
        SearchHit(node_id=row.node_id, doc_id=row.doc_id, anchor=row.anchor, score=row.score)
        for row in rows
    ]
