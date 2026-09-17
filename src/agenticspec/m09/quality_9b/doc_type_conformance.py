"""M09B `doc_type_schema_conformance` detector：文档类型组合规则的历史数据巡检。

**为什么需要**：`doc_type` 的**差异化组合规则**（`allowed_atom_types` / `required_meta_fields`，
REQ-M01-F03，见 `doc_type_mapping.md` §3）只在**写入路径**（M03 导入 `frontmatter.validate`、
M06/M07 写入 `M09A`）生效。规则本身是代码常量（`model/doc_types.py`，Q6 可扩展），**细化或
收紧之后，库内既有文档不会被回溯检查**——历史行可能缺该 `doc_type` 现时必填的 `meta` 字段。
本巡检即该缺口的兜底：**只读**扫描 `docs` 行，逐行按现时规则判定。

判据（两条，均取自 M01 单点口径，P5）：

* `M09B.doc_type.meta_missing` ← `M01.missing_required_meta(doc_type, meta)`：缺失字段**逐字段**
  一条违规（与 M09A 的 `fix_hint` 粒度一致：agent 依建议补哪个字段就补哪个）；
* `M09B.doc_type.unknown` ← `doc_type ∉ M01.DOC_TYPES`：`docs.doc_type` 受 DDL CHECK 约束
  （`docs_doc_type_check`），正常库内不可达；**判据仍必要**——DDL 与模型层若发生漂移
  （迁移先行/模型未同步），`missing_required_meta` 会抛 `KeyError` 并让**整轮质量门**崩掉。
  本判据把该情形降级为一条违规，使漂移可见而非致命。

作用域：`doc_ids=None` → 全库（`Storage.list_docs` 一次取全；`docs` 表无分区，行数即文档数，
量级远小于 `nodes`）；给定 `doc_ids` → 裁剪到该子集。

已知限制（如实标注）：本判据**不做端到端验证**——`lang`/`tool-manual`/`product`/`safety` 四类
当前无真实语料（`doc_type_mapping.md` §5），其规则正确性只有单元 + 合成样例背书；本巡检对
这四类的实际命中率在语料入库前**无法测量**。
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Final

from agenticspec.model import DOC_TYPES, Doc, Violation, missing_required_meta

from .context import GateContext

__all__ = [
    "DETECTOR_ID",
    "RULES_DOC_TYPE_CONFORMANCE",
    "RULE_DOC_TYPE_UNKNOWN",
    "RULE_META_MISSING",
    "detect",
    "judge_docs",
]

DETECTOR_ID: Final = "doc_type_schema_conformance"

RULE_META_MISSING: Final = "M09B.doc_type.meta_missing"
RULE_DOC_TYPE_UNKNOWN: Final = "M09B.doc_type.unknown"
RULES_DOC_TYPE_CONFORMANCE: Final = (RULE_DOC_TYPE_UNKNOWN, RULE_META_MISSING)

_META_FIX_HINT: Final = (
    "补齐 docs.meta 的该字段（M03 重导：源 frontmatter 补该键 → parse_markdown → commit_document），"
    "或修正该 doc_type 的 required_meta_fields（M01 register_doc_type_rule，须同步文档化依据）"
)
_UNKNOWN_FIX_HINT: Final = (
    "把 doc_type 改为 M01.DOC_TYPES 之一（§4 DDL docs_doc_type_check 同步），"
    "或经 M01 register_doc_type_rule 登记该类型的组合规则后再放宽 CHECK"
)


def judge_docs(docs: Iterable[Doc]) -> list[Violation]:
    """文档行 → 违规清单（纯函数；按 `doc_id` 定序，同文档内按字段名定序）。"""
    violations: list[Violation] = []
    for doc in sorted(docs, key=lambda item: item.doc_id):
        if doc.doc_type not in DOC_TYPES:
            violations.append(
                Violation(
                    rule_id=RULE_DOC_TYPE_UNKNOWN,
                    path=f"{doc.doc_id}:doc_type",
                    message=(
                        f"文档 {doc.doc_id} 的 doc_type={doc.doc_type!r} 无组合规则"
                        f"（已注册：{list(DOC_TYPES)}）——DDL CHECK 与模型层取值域不一致"
                    ),
                    fix_hint=_UNKNOWN_FIX_HINT,
                )
            )
            continue
        for field_name in missing_required_meta(doc.doc_type, doc.meta):
            violations.append(
                Violation(
                    rule_id=RULE_META_MISSING,
                    path=f"{doc.doc_id}:meta.{field_name}",
                    message=(
                        f"文档 {doc.doc_id}（doc_type={doc.doc_type!r}）的 meta 缺必填字段"
                        f" {field_name!r}——该类型组合规则的必填口径（REQ-M01-F03）"
                    ),
                    fix_hint=_META_FIX_HINT,
                )
            )
    return violations


async def detect(ctx: GateContext) -> list[Violation]:
    """执行 doc_type 组合规则巡检（全库或按 `doc_ids` 裁剪）。"""
    docs: Sequence[Doc] = await ctx.storage.list_docs()
    if ctx.doc_ids is not None:
        wanted = set(ctx.doc_ids)
        docs = [doc for doc in docs if doc.doc_id in wanted]
    violations = judge_docs(docs)
    ctx.logger.info(
        "doc_type conformance scanned",
        docs=len(docs),
        violations=len(violations),
    )
    return violations
