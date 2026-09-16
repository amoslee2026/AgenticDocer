"""M09B 质量门编排（REQ-M09-F02；§3 M09 `run_quality_gate`）。

`run_quality_gate(scope)` 是质量门的**唯一入口**：解析作用域 → 选定 detector → 逐个执行
→ 每个 detector 一份 `QualityReport`（**含零违规的报告**，detector 全集可见，便于机检
「6 项都跑过」而非「只看到坏的那些」）。

* 作用域 `QualityScope{doc_ids, detectors}`：`doc_ids=None` = 全库；`detectors=None` = 全选，
  否则只跑指定项（**detector 可单独调用**），未登记的 id → `ValidationError`（422）；
* 报告顺序恒定（`DETECTOR_IDS` 声明序），同输入同输出；
* 每项 detector 一个 `timer` 埋点（`op="quality_gate_detector"`，ctx 带 `detector_id`），
  汇总一条 `quality_gate` 日志；无 LLM、无网络（P6）。

同步入口 :func:`run_quality_gate_sync` 供 CLI/脚本消费（与 M12 `health_sync` 同口径：事件
循环内调用即报错，不静默另起循环）。
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Sequence
from typing import Final

from agenticdocer.model import QualityReport, QualityScope, Violation
from agenticdocer.observability import ModuleLogger, get_logger
from agenticdocer.store import (
    Database,
    Storage,
    ValidationError,
    database_url,
    get_storage,
)

from . import (
    assets_missing,
    broken_refs,
    doc_type_conformance,
    events_consistency,
    perf_health,
    render_consistency,
    section_range_consistency,
    terms,
)
from .context import GateContext

__all__ = [
    "DETECTORS",
    "DETECTOR_IDS",
    "build_context",
    "detector_ids",
    "get_detector",
    "resolve_detectors",
    "run_quality_gate",
    "run_quality_gate_sync",
]

Detector = Callable[[GateContext], Awaitable[list[Violation]]]

log: ModuleLogger = get_logger("m09.quality")

DETECTORS: Final[dict[str, Detector]] = {
    broken_refs.DETECTOR_ID: broken_refs.detect,
    terms.DETECTOR_ID: terms.detect,
    assets_missing.DETECTOR_ID: assets_missing.detect,
    render_consistency.DETECTOR_ID: render_consistency.detect,
    events_consistency.DETECTOR_ID: events_consistency.detect,
    section_range_consistency.DETECTOR_ID: section_range_consistency.detect,
    perf_health.DETECTOR_ID: perf_health.detect,
    doc_type_conformance.DETECTOR_ID: doc_type_conformance.detect,
}
"""detector 登记表（key = `QualityReport.detector_id`）：§3 M09 声明的 6 项 + 两项后加——
`section_range_consistency`（M02 B-2 区间契约兜底）、`doc_type_schema_conformance`（方案 C
的 doc_type 组合规则历史数据兜底，`doc_type_mapping.md` §3）。声明序即报告顺序，
**只增不改序**——调用方（M11 `quality-gate` 的缺省集合）按各自子集过滤时，相对顺序不变。"""

DETECTOR_IDS: Final[tuple[str, ...]] = tuple(DETECTORS)
"""声明序 = 报告顺序（常量，便于机检与快照）。"""


def detector_ids() -> tuple[str, ...]:
    """全部 detector id（声明序）。"""
    return DETECTOR_IDS


def get_detector(detector_id: str) -> Detector:
    """取单个 detector（可单独调用）；未登记 → `ValidationError`。"""
    try:
        return DETECTORS[detector_id]
    except KeyError:
        raise ValidationError(
            f"未知 detector_id={detector_id!r}；已登记：{list(DETECTOR_IDS)}",
            entity="quality_gate",
        ) from None


def resolve_detectors(detectors: Sequence[str] | None) -> tuple[str, ...]:
    """`QualityScope.detectors` → 待执行 id 序列（去重 + 声明序归一；未登记即报错）。"""
    if detectors is None:
        return DETECTOR_IDS
    for detector_id in detectors:
        get_detector(detector_id)
    selected = set(detectors)
    return tuple(item for item in DETECTOR_IDS if item in selected)


def build_context(
    scope: QualityScope | None,
    *,
    storage: Storage | None = None,
    dsn: str | None = None,
) -> tuple[GateContext, tuple[str, ...]]:
    """构造执行上下文；返回 `(ctx, 待执行 detector id 序列)`。"""
    store = storage or get_storage()
    doc_ids = None if scope is None or scope.doc_ids is None else tuple(scope.doc_ids)
    context = GateContext(
        storage=store,
        logger=log,
        doc_ids=doc_ids,
        dsn=dsn or store.db.url,
    )
    return context, resolve_detectors(None if scope is None else scope.detectors)


async def run_quality_gate(
    scope: QualityScope | None = None,
    *,
    storage: Storage | None = None,
    dsn: str | None = None,
) -> list[QualityReport]:
    """执行质量门，返回每个选定 detector 一份报告（含零违规者）。

    :param scope: `QualityScope{doc_ids, detectors}`；`None` = 全库 + 全选。
    :param storage: M02 装配面（缺省进程单例）。
    :param dsn: `perf_health` 巡检连库串（缺省 = `storage.db.url`，即质量门同一库）。
    :raises ValidationError: `scope.detectors` 含未登记的 detector id（422）。
    """
    context, selected = build_context(scope, storage=storage, dsn=dsn)
    reports: list[QualityReport] = []
    with context.logger.timer(
        "quality_gate",
        detectors=len(selected),
        docs=len(context.doc_ids) if context.doc_ids is not None else -1,
    ):
        for detector_id in selected:
            detector = get_detector(detector_id)
            with context.logger.child(detector_id=detector_id).timer("quality_gate_detector"):
                violations = await detector(context)
            violations.sort(key=lambda item: (item.rule_id, item.path))
            reports.append(QualityReport(detector_id=detector_id, violations=violations))
            if violations:
                context.logger.warn(
                    "quality gate violations", detector_id=detector_id, count=len(violations)
                )
    total = sum(len(report.violations) for report in reports)
    context.logger.info(
        "quality gate finished",
        detectors=len(reports),
        violations=total,
        failed_detectors=[report.detector_id for report in reports if report.violations],
    )
    return reports


def run_quality_gate_sync(
    scope: QualityScope | None = None,
    *,
    storage: Storage | None = None,
    dsn: str | None = None,
) -> list[QualityReport]:
    """`run_quality_gate` 的同步包装（CLI/脚本）；事件循环内调用 → `RuntimeError`。

    **资源归属**：未显式给 `storage` 时，本入口自建并自弃连接池（`Database(database_url())`），
    故**同一进程内可重复调用**——每次 `asyncio.run` 都会新建事件循环，若复用进程级单例
    （`get_storage()`），池中连接仍绑定在已关闭的上一个循环上，第二次调用即报
    `Future attached to a different loop`。显式传入 `storage` 的调用方自行负责循环一致性。
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(_run_sync_once(scope, storage=storage, dsn=dsn))
    raise RuntimeError("run_quality_gate_sync() 不能在事件循环内调用；请 await run_quality_gate()")


async def _run_sync_once(
    scope: QualityScope | None,
    *,
    storage: Storage | None,
    dsn: str | None,
) -> list[QualityReport]:
    """同步入口的单次执行体（自建池在一轮内用完即弃）。"""
    if storage is not None:
        return await run_quality_gate(scope, storage=storage, dsn=dsn)
    owned = Storage(Database(database_url()))
    try:
        return await run_quality_gate(scope, storage=owned, dsn=dsn)
    finally:
        await owned.db.dispose()
