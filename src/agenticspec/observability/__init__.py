"""M12 可观测性横切层（ADR-010）——全模块唯一日志出口 + 性能指标 + 健康巡检。

对外契约（architecture_specification §3 M12）：

* :func:`get_logger` / :class:`ModuleLogger`——业务代码唯一的日志入口（禁止 `print`/`logging`）；
* :func:`new_rid` / :func:`current_rid` / :func:`set_rid` / :func:`rid_scope`——请求级追踪；
* :class:`MetricsSnapshot` / :func:`snapshot`——`GET /api/v1/admin/metrics` 的聚合；
* :class:`HealthReport` / :func:`health`——`agenticspec stats --health` 与 M09B `perf_health`；
* :class:`ObservabilityMiddleware` / :func:`install`——FastAPI 埋点中间件（`app.py` 装配）；
* `DTO_*` 业务错误码（`DTO_PERF_EXCEEDED` 等）。

**审计分离**：日志是运行态（可轮转可丢弃）；审计权威源是 PG `events` 表（P2）。
"""

from __future__ import annotations

from agenticspec.observability.error_codes import (
    DTO_ANCHOR_CONFLICT,
    DTO_AUTH_REJECTED,
    DTO_PARTITION_MISSING,
    DTO_PERF_EXCEEDED,
    DTO_REF_BROKEN,
    DtoErrorCode,
    error_code_for_rule,
)
from agenticspec.observability.health import (
    HealthReport,
    IndexHealth,
    PartitionHealth,
    PoolHealth,
    TableHealth,
    evaluate_health,
    health,
    health_sync,
    normalize_dsn,
    pool_health,
)
from agenticspec.observability.logger import (
    PROGRAM,
    ModuleLogger,
    classify_duration,
    command_for,
    get_logger,
    log_dir,
    perf_budget_ms,
    reset_loggers,
    slow_query_ms,
)
from agenticspec.observability.metrics import (
    EndpointMetric,
    MetricsSnapshot,
    RenderMetric,
    SlowQuery,
    percentile,
    snapshot,
)
from agenticspec.observability.middleware import (
    REQUEST_ID_HEADER,
    UNROUTED,
    ObservabilityMiddleware,
    install,
)
from agenticspec.observability.rid import (
    current_rid,
    new_rid,
    reset_rid,
    rid_scope,
    set_rid,
)

__all__ = [
    "DTO_ANCHOR_CONFLICT",
    "DTO_PARTITION_MISSING",
    "DTO_PERF_EXCEEDED",
    "DTO_REF_BROKEN",
    "PROGRAM",
    "REQUEST_ID_HEADER",
    "UNROUTED",
    "DtoErrorCode",
    "EndpointMetric",
    "HealthReport",
    "IndexHealth",
    "MetricsSnapshot",
    "ModuleLogger",
    "ObservabilityMiddleware",
    "PartitionHealth",
    "PoolHealth",
    "RenderMetric",
    "SlowQuery",
    "TableHealth",
    "classify_duration",
    "command_for",
    "current_rid",
    "error_code_for_rule",
    "evaluate_health",
    "get_logger",
    "health",
    "health_sync",
    "install",
    "log_dir",
    "new_rid",
    "normalize_dsn",
    "perf_budget_ms",
    "percentile",
    "pool_health",
    "reset_loggers",
    "reset_rid",
    "rid_scope",
    "set_rid",
    "slow_query_ms",
    "snapshot",
]
