"""M05 图遍历与关键词检索（**内部实现：无公开端点**，ADR-008）。

对外检索能力由 LightRAG 承担；本模块的两个函数仅由 M-LR 导出（主要）与 M09B 质量门
（次要）以 Python 内部调用消费：

- :func:`traverse`——refs 多跳遍历（`KIND_RULES` 方向/跳数截断/去重/环截断/软删过滤）；
- :func:`search_text`——PG FTS 关键词检索（ADR-005，结果含 `score`）。

**不提供 router**：M06/M07 不得把二者暴露为端点（ADR-008 边界表）。
"""

from __future__ import annotations

from .search import FTS_CONFIG, search_text
from .traverse import KIND_RULES, MAX_HOPS, Direction, expandable_kinds, traverse

__all__ = [
    "FTS_CONFIG",
    "KIND_RULES",
    "MAX_HOPS",
    "Direction",
    "expandable_kinds",
    "search_text",
    "traverse",
]
