"""M09B `perf_health` detector：容量巡检接入质量门（ADR-010 / REQ-M12-F05 验收 (c)）。

巡检本体**就是** M12 `health()`（`agenticspec stats --health` 的同一实现，ADR-010 §3.3：
「`health()` 与 M09B `perf_health` detector 共用」），本模块只做两件事：

1. 以**质量门所在库**的 DSN 调用 `health()`（`GateContext.dsn`，见 `gate.build_context`）；
2. 把 `HealthReport` 机械映射为违规项——判据不做二次解读：

* `M09B.perf.partition_missing` — `events` 未来月份分区缺失（`verdict='fail'` 的硬原因之一，
  伴随 `DTO_PARTITION_MISSING`）；`fix_hint` 给出建分区的具体语句；
* `M09B.perf.verdict` — `verdict != 'ok'`（degraded/fail）：膨胀、autovacuum 滞后、零扫描索引、
  连接池饱和、归档逾期等，逐条建议（`HealthReport.advice`）原样进 `fix_hint`。

`verdict='ok'` 时零违规（`advice` 非空 ⟺ verdict 非 ok，见 M12 `evaluate_health`）。

**连接池采样不参与判定**：`health(engine=…)` 会把应用连接池占用计入告警，而池占用是
**运行态**信号（随请求波动），不是数据面缺陷；质量门是离线巡检，故不传 engine（`pool` 全 0
= 未知，M12 对容量 0 不做判定）。运行态池饱和由 M12 的 `/admin/health` 与指标快照负责。

容量类数据面无 doc 维度：`doc_ids` 不影响本 detector。
"""

from __future__ import annotations

from typing import Final

from agenticspec.model import Violation
from agenticspec.observability import HealthReport, health

from .context import GateContext

__all__ = [
    "DETECTOR_ID",
    "RULES_PERF_HEALTH",
    "detect",
    "map_health_report",
]

DETECTOR_ID: Final = "perf_health"

RULE_PARTITION_MISSING: Final = "M09B.perf.partition_missing"
RULE_VERDICT: Final = "M09B.perf.verdict"
RULES_PERF_HEALTH: Final = (RULE_PARTITION_MISSING, RULE_VERDICT)

_PARTITION_FIX: Final = (
    "按 ADR-009 §4.2 预建下月分区："
    "CREATE TABLE events_<YYYYMM> PARTITION OF events FOR VALUES FROM ('<月首>') TO ('<次月首>')"
    "；并把预建任务挂到定时器（当前仅 migrated 时建历史/未来三个月）"
)
_MAX_ADVICE_CHARS: Final = 600


def map_health_report(report: HealthReport, *, path: str = "db") -> list[Violation]:
    """`HealthReport` → 违规清单（纯函数，无 IO；供单测直接构造报告验证映射）。"""
    violations: list[Violation] = []
    if report.partitions.events_next_missing:
        violations.append(
            Violation(
                rule_id=RULE_PARTITION_MISSING,
                path=f"{path}#partitions.events_next_missing",
                message=(
                    "events 未来月份分区缺失：下月事件写入将失败（ADR-009 §4.2；"
                    f"oldest_event_ts={report.partitions.oldest_event_ts}）"
                ),
                fix_hint=_PARTITION_FIX,
            )
        )
    if report.verdict != "ok":
        advice = " | ".join(report.advice)[:_MAX_ADVICE_CHARS]
        violations.append(
            Violation(
                rule_id=RULE_VERDICT,
                path=f"{path}#verdict",
                message=(
                    f"容量巡检 verdict={report.verdict}"
                    f"（表 {len(report.tables)} 张 / 索引 {len(report.indexes)} 个 / "
                    f"建议 {len(report.advice)} 条）"
                ),
                fix_hint=advice
                or "运行 `agenticspec stats --health` 查看明细（M12 ADR-010 §3.3）",
            )
        )
    return violations


async def detect(ctx: GateContext) -> list[Violation]:
    """调用 M12 `health()` 并映射为违规项（DSN 缺省 = 质量门所用库）。"""
    report = await health(dsn=ctx.dsn)
    violations = map_health_report(report)
    ctx.logger.info(
        "perf health probed",
        verdict=report.verdict,
        advice=len(report.advice),
        violations=len(violations),
    )
    return violations
