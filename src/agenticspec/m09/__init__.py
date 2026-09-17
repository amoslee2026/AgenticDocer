"""M09 校验与质量门（L3；architecture_specification §3 M09）。

两个子域，签名与规范一致：

* **M09A** :mod:`agenticspec.m09.engine_9a` —— schema 校验引擎（REQ-M09-F01，阶段 1）：
  `validate_proposal(atom_type, content)` / `validate_write(node, doc_type=None)` →
  `list[Violation]`（含 `fix_hint`，M06 lint 自修复闭环 REQ-M06-F02 依赖）；
* **M09B** :mod:`agenticspec.m09.quality_9b` —— 质量门（REQ-M09-F02，阶段 3）：
  `run_quality_gate(scope)` → `list[QualityReport]`，八个 detector（§3 M09 的 6 项 + Main 批准
  新增的 `section_range_consistency` + 方案 C 的 `doc_type_schema_conformance`）可经
  `QualityScope.detectors` 单独调用。

    from agenticspec.m09 import QualityScope, run_quality_gate, validate_write

    violations = validate_write(node, doc_type="standard")
    reports = await run_quality_gate(QualityScope(doc_ids=None, detectors=["broken_refs"]))

依赖方向（§3 依赖矩阵）：M09 → M01（模型/schema）、M02（存储/事件折叠）、M04（渲染规范化）、
M12（日志/健康巡检）。无 LLM、无网络（P6）。
"""

from __future__ import annotations

from agenticspec.model import QualityReport, QualityScope, Violation

from . import engine_9a, quality_9b
from .engine_9a import (
    RULES_9A,
    RULE_ANCHOR_DOC_ID,
    RULE_ATOM_SCHEMA,
    RULE_ATOM_UNKNOWN,
    RULE_CONTENT_TEXT,
    RULE_CONTENT_TEXT_DRIFT,
    RULE_CONTENT_TEXT_EMPTY,
    RULE_CROSS_REF_EXTERNAL_NODE,
    RULE_DOC_TYPE_ATOM,
    RULE_DOC_TYPE_VARIANT,
    RULE_PARENT_SELF,
    RULE_TABLE_FORMAT,
    validate_proposal,
    validate_write,
)
from .quality_9b import (
    DETECTORS,
    DETECTOR_IDS,
    GateContext,
    detector_ids,
    get_detector,
    resolve_detectors,
    run_quality_gate,
    run_quality_gate_sync,
)

__all__ = [
    # 子域模块
    "engine_9a",
    "quality_9b",
    # M09A（REQ-M09-F01）
    "RULES_9A",
    "RULE_ANCHOR_DOC_ID",
    "RULE_ATOM_SCHEMA",
    "RULE_ATOM_UNKNOWN",
    "RULE_CONTENT_TEXT",
    "RULE_CONTENT_TEXT_DRIFT",
    "RULE_CONTENT_TEXT_EMPTY",
    "RULE_CROSS_REF_EXTERNAL_NODE",
    "RULE_DOC_TYPE_ATOM",
    "RULE_DOC_TYPE_VARIANT",
    "RULE_PARENT_SELF",
    "RULE_TABLE_FORMAT",
    "validate_proposal",
    "validate_write",
    # M09B（REQ-M09-F02）
    "DETECTORS",
    "DETECTOR_IDS",
    "GateContext",
    "detector_ids",
    "get_detector",
    "resolve_detectors",
    "run_quality_gate",
    "run_quality_gate_sync",
    # 公共类型（M01 直出，供调用方一次 import 即得 M09 契约）
    "QualityReport",
    "QualityScope",
    "Violation",
]
