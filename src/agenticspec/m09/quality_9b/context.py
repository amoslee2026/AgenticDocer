"""M09B 质量门的执行上下文（各 detector 的共同入参）。

`GateContext` 是 detector 与「作用域/连接面/日志」之间的唯一契约：

* ``doc_ids=None`` → 全库巡检；给定则各 detector 按文档裁剪（引用/批注/事件按
  **源节点所属文档**裁剪，节点按 `doc_id` 裁剪）；
* 词表与容量类判据（`terms` 的种子漂移、`perf_health`）数据面**无 doc 维度**，恒定全表
  执行——`doc_ids` 只影响其中「definition 节点覆盖范围」等有文档维度的部分；
* ``dsn``：`perf_health` 连库串，缺省已在 :func:`agenticspec.m09.quality_9b.gate.build_context`
  解析为 ``storage.db.url``（质量门与巡检必须看**同一个库**）。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - 仅类型
    from agenticspec.observability.logger import ModuleLogger
    from agenticspec.store import Storage

__all__ = ["GateContext"]


@dataclass(slots=True)
class GateContext:
    """一次质量门执行的输入（由 `gate.run_quality_gate` 构造）。"""

    storage: Storage
    logger: ModuleLogger
    doc_ids: tuple[str, ...] | None = None
    dsn: str | None = None
