"""M09B `render_consistency` detector：渲染一致性巡检（REQ-M04-F01 两式 / REQ-M09-F02）。

判据就是 §3 M04 的两式（**比较函数只有一套**：M04 `normalize_*` / `NormalForm`）：

* **判据 (a) 解析保真**：`normalize(doc_id) == normalize_markdown(<源文件>)`
  ——库侧节点树镜像 vs 源 Markdown；不等即导入丢结构/改写了本轮不该改的内容；
* **判据 (b) 渲染保真**：`normalize_markdown(<产物文件>) == normalize_markdown(<源文件>)`
  ——产物层（frontmatter 回写、图片 `src` 重写、HTML 直通）的破坏只在这一式里暴露。

源文件取自 `docs.meta['source_path']`（M03 导入期写入）。**无法判定的情形不报违规**：

* 文档无 `source_path` 或源文件已不在盘上 → 跳过（判据无从计算；计入 detector 日志的
  `skipped` 聚合，不制造噪音）；
* 产物文件 `<out_dir>/<doc_id>.md` 不存在 → 只跑判据 (a)（未渲染过的文档不该被质量门判
  「渲染漂移」）。

产物路径口径：M04 `render_document` 产物名为 `<doc_id>.md`（文件名安全化仅替换文件系统
禁用字符；本项目 doc_id 为 `SPEC-*`/`EXT:` 形态，安全化后与 doc_id 相同）。若产物名不同
（含禁用字符的 doc_id），本 detector 判据 (b) 自动跳过并被计入 `skipped`。
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Final

from agenticdocer.model import Doc, Violation
from agenticdocer.render import (
    NormalForm,
    normalize,
    normalize_markdown,
    render_out_dir,
)

from .context import GateContext

__all__ = [
    "DETECTOR_ID",
    "DIFF_FEATURES",
    "RULES_RENDER_CONSISTENCY",
    "detect",
    "diff_forms",
    "rendered_artifact_path",
]

DETECTOR_ID: Final = "render_consistency"

RULE_PARSE_DRIFT: Final = "M09B.render.parse_drift"
RULE_ARTIFACT_DRIFT: Final = "M09B.render.artifact_drift"
RULES_RENDER_CONSISTENCY: tuple[str, ...] = (RULE_PARSE_DRIFT, RULE_ARTIFACT_DRIFT)

_CLIP_CHARS: Final = 160

DIFF_FEATURES: Final[tuple[str, ...]] = (
    "headings",
    "tables",
    "code_blocks",
    "images",
    "lists",
    "inline_markers",
)
"""`NormalForm` 的全部特征维度（逐维比对，任一维不等即该维一条违规）。"""


def _feature_values(form: NormalForm) -> dict[str, list[str]]:
    """各维度 → 可比较/可打印的字符串序列（表格展平为行列文本网格）。"""
    return {
        "headings": [f"h{level}:{text}" for level, text in form.headings],
        "tables": [
            f"{table.rows}x{table.cols}|" + " / ".join(" , ".join(row) for row in table.cells)
            for table in form.tables
        ],
        "code_blocks": list(form.code_blocks),
        "images": list(form.images),
        "lists": [" | ".join(items) for items in form.lists],
        "inline_markers": list(form.inline_markers),
    }


def _clip(value: str) -> str:
    flat = " ".join(value.split())
    return flat if len(flat) <= _CLIP_CHARS else f"{flat[:_CLIP_CHARS]}…"


def _first_mismatch(expected: Sequence[str], actual: Sequence[str]) -> tuple[int, str, str] | None:
    """首个差异位置与其两侧取值；长度不同而前缀相同 → 差异在截断点。"""
    for index in range(min(len(expected), len(actual))):
        if expected[index] != actual[index]:
            return index, expected[index], actual[index]
    if len(expected) != len(actual):
        index = min(len(expected), len(actual))
        return index, "(缺失)" if len(expected) <= index else expected[index], (
            "(缺失)" if len(actual) <= index else actual[index]
        )
    return None


def diff_forms(
    expected: NormalForm,
    actual: NormalForm,
    *,
    rule_id: str,
    path_prefix: str,
    label: str,
    fix_hint: str,
) -> list[Violation]:
    """逐维比较两个 `NormalForm`（纯函数），返回违规清单（逐维定位）。"""
    left = _feature_values(expected)
    right = _feature_values(actual)
    violations: list[Violation] = []
    for feature in DIFF_FEATURES:
        mismatch = _first_mismatch(left[feature], right[feature])
        if mismatch is None:
            continue
        index, want, got = mismatch
        violations.append(
            Violation(
                rule_id=rule_id,
                path=f"{path_prefix}#{feature}",
                message=(
                    f"{label}：{feature} 不一致（源 {len(left[feature])} 项 / 库侧 {len(right[feature])} 项，"
                    f"首个差异 @{index}：源={_clip(want)!r} 库侧={_clip(got)!r}）"
                ),
                fix_hint=fix_hint,
            )
        )
    return violations


def rendered_artifact_path(doc_id: str, out_dir: Path | str | None = None) -> Path:
    """M04 产物路径：`<RENDER_OUT_DIR>/<doc_id>.md`（`render_document` 的命名契约）。"""
    return render_out_dir(out_dir) / f"{doc_id}.md"


async def _scoped_docs(ctx: GateContext) -> list[Doc]:
    docs = await ctx.storage.list_docs()
    if ctx.doc_ids is None:
        return docs
    wanted = set(ctx.doc_ids)
    return [doc for doc in docs if doc.doc_id in wanted]


async def detect(ctx: GateContext) -> list[Violation]:
    """执行两式往返巡检；`skipped` 计数进日志（无源文件/无产物，不代表违规）。"""
    violations: list[Violation] = []
    skipped_no_source = 0
    skipped_no_artifact = 0
    docs = await _scoped_docs(ctx)
    for doc in docs:
        source = _source_path(doc)
        if source is None:
            skipped_no_source += 1
            continue
        expected = normalize_markdown(source)
        actual = await normalize(doc.doc_id, storage=ctx.storage)
        violations.extend(
            diff_forms(
                expected,
                actual,
                rule_id=RULE_PARSE_DRIFT,
                path_prefix=doc.doc_id,
                label="解析保真（判据 a：库侧节点树 vs 源）",
                fix_hint=(
                    "重解析并 commit 该文档（M03 parse_markdown + commit_document），"
                    "或修正被改写的节点 content.fragment（P4：片段原样直通）"
                ),
            )
        )
        artifact = rendered_artifact_path(doc.doc_id)
        if not artifact.is_file():
            skipped_no_artifact += 1
            continue
        violations.extend(
            diff_forms(
                expected,
                normalize_markdown(artifact),
                rule_id=RULE_ARTIFACT_DRIFT,
                path_prefix=f"{doc.doc_id}#artifact",
                label="渲染保真（判据 b：产物 vs 源）",
                fix_hint=(
                    f"重渲染后复跑：render_document({doc.doc_id!r})（M04）；若仍漂移，"
                    "检查渲染层改写（P4 唯一例外仅为图片 src 重写）"
                ),
            )
        )
    ctx.logger.info(
        "render consistency scanned",
        docs=len(docs),
        skipped_no_source=skipped_no_source,
        skipped_no_artifact=skipped_no_artifact,
        violations=len(violations),
    )
    return violations


def _source_path(doc: Doc) -> Path | None:
    """`docs.meta['source_path']`（M03 导入期写入）→ 存在的源文件路径。"""
    raw = doc.meta.get("source_path") if isinstance(doc.meta, dict) else None
    if not isinstance(raw, str) or not raw.strip():
        return None
    path = Path(raw)
    return path if path.is_file() else None
