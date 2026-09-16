"""M09B 质量门（阶段 3；§3 M09 `run_quality_gate` + REQ-M09-F02）。

七个 detector（`detector_id` 即 `QualityReport.detector_id`；声明序 = 报告顺序）：

| detector_id | 判据 | 依赖 |
|---|---|---|
| `broken_refs` | 悬空引用巡检（ADR-009 降级外键兜底：refs src/dst、孤儿 parent、批注 node/event） | M02 |
| `terms` | 术语表校验（`terms` 表 + `TERMS_SEED` 种子；含 `terms.definition_node_id` 兜底） | M02 |
| `assets_missing` | 被引用资产缺失（`sha256` 令牌扫描：片段内源路径 + `figure.asset_ref`） | M02 |
| `render_consistency` | 往返两式（解析保真 / 渲染保真），比较函数只有 M04 `normalize*` 一套 | M04 |
| `events_consistency` | events 重放（M02 `apply_events`）vs 当前态逐字段 | M02 |
| `section_range_consistency` | 章节区间契约（M02 `section_range_diff`：区间法原始结果 vs 递归 CTE，含**漏收**方向） | M02 |
| `perf_health` | 容量巡检（M12 `health()`：分区/膨胀/索引/归档） | M12 |

§3 M09 原定 6 项；`section_range_consistency` 为 Main 批准新增（M02 B-2 优化的反向残余风险
兜底）。声明序**只增不改**——调用方（M11 `quality-gate` 的缺省集合）按子集过滤时相对顺序不变。

`broken_refs` 与 `events_consistency` 是 ADR-009 分区化（6 处外键降级 + `events` 改分区表）
之后**唯一**的完整性兼底，实现在 `broken_refs.py` / `events_consistency.py` 的模块文档里
逐条列明「降级的外键 ↔ 兜底判据」对应关系。

对外入口：

    from agenticdocer.m09 import QualityScope, run_quality_gate
    reports = await run_quality_gate(QualityScope(doc_ids=["SPEC-1"], detectors=None))
"""

from __future__ import annotations

from . import (
    assets_missing,
    broken_refs,
    events_consistency,
    perf_health,
    render_consistency,
    section_range_consistency,
    terms,
)
from .context import GateContext
from .gate import (
    DETECTORS,
    DETECTOR_IDS,
    Detector,
    build_context,
    detector_ids,
    get_detector,
    resolve_detectors,
    run_quality_gate,
    run_quality_gate_sync,
)

__all__ = [
    # 编排
    "DETECTORS",
    "DETECTOR_IDS",
    "Detector",
    "build_context",
    "detector_ids",
    "get_detector",
    "resolve_detectors",
    "run_quality_gate",
    "run_quality_gate_sync",
    # 上下文
    "GateContext",
    # detector 模块（可单独 import 其纯判据函数）
    "assets_missing",
    "broken_refs",
    "events_consistency",
    "perf_health",
    "render_consistency",
    "section_range_consistency",
    "terms",
]
