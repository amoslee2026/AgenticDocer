"""M-LR LightRAG 边界（L6；架构规范 §3 M-LR；ADR-002/ADR-008）。

对外契约：

* :func:`~agenticspec.mlr.export.export_package`——生成导出包（渲染文本 + ``node_id``
  映射 + 图结构上下文），**不依赖 lightRAG 在线**（REQ-MLR-F01）；
* :func:`~agenticspec.mlr.stream.change_stream`——基于 ``events`` 的增量游标流
  （REQ-MLR-F02），:func:`~agenticspec.mlr.stream.cursor_token` 给出可持久化的续拉游标。

依赖（§1.3 矩阵：M-LR → M02/M04/M05 内部）：M02 读库、M04 渲染口径、M05 ``traverse``
构造图结构（ADR-008：M05 降级后的主要消费方）。

**C7（摄入暂缓）/ P6（无 LLM）**：本包只生成导出包与事件流——不导入 lightRAG、
不调用其 API、不访问网络。
"""

from __future__ import annotations

from .export import (
    DEFAULT_GRAPH_HOPS,
    EXPORT_GRAPH_FILE,
    EXPORT_MANIFEST_FILE,
    EXPORT_NODES_FILE,
    FORMAT_VERSION,
    export_package,
    node_record,
)
from .stream import (
    CURSOR_SEPARATOR,
    DEFAULT_BATCH_SIZE,
    DEFAULT_POLL_INTERVAL,
    change_stream,
    cursor_token,
)

__all__ = [
    "CURSOR_SEPARATOR",
    "DEFAULT_BATCH_SIZE",
    "DEFAULT_GRAPH_HOPS",
    "DEFAULT_POLL_INTERVAL",
    "EXPORT_GRAPH_FILE",
    "EXPORT_MANIFEST_FILE",
    "EXPORT_NODES_FILE",
    "FORMAT_VERSION",
    "change_stream",
    "cursor_token",
    "export_package",
    "node_record",
]
