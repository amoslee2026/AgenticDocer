"""M03 导入解析：markdown（+frontmatter）→ 原子提议（规则 + 待确认标志 + 未映射块清单）。

权威来源：`architecture_specification.md` §3 M03、§6（frontmatter 映射）、
`functional_specification.md` REQ-M03-F01/F04/F05、`ADR-006`（结构化粒度与锚策略）、
`design_doc.md` §5.1（内容原子与格式策略）、§6.1（导入流）、§10（覆盖率口径）。

解析流水线（全部确定性，无 LLM/P6）：

1. **frontmatter** → :class:`~agenticdocer.importer.frontmatter.Frontmatter`
   （C5 十七字段校验；`spec_id`→doc_id、`spec_type`→doc_type、`source`→source_ref）；
2. **块切分**（`scan_blocks`）：按语法形态切出**源块**——口径 = design_doc §10
   「标题/表格/图/代码块/列表/段落」（+ 块级 HTML 残余）；行号为**源文件行号**（1 基闭区间）；
3. **上下文归类**（`classify`）：目录区（`Contents`/`List of Tables`…）内的块 → 兜底规则，
   术语区（`Glossary`/`Terms and Acronyms`…）内的词条 → `definition`；其余按形态规则；
4. **章节树**（`build_sections`）：层级取**标题编号深度**（语料 99.8% 用 `##`，真实层级在编号里：
   `1.3.2.1`、`A5.3.6`、`A.1`、`Chapter 10`、`Annex A`），无编号标题回退 `#` 个数；
5. **原子提议**（`_Pending` → :class:`Proposal`）：ADR-006 的条款级粒度——标题成 `clause`
   节点，其**正文段落并入该节点 `content.fragment`**（不单独成节点）；表格/图/代码/列表/引用
   成为**同级独立原子**；未映射块走兜底（`note`，零静默丢弃）；
6. **定锚**：整档一次 :func:`agenticdocer.model.assign_anchors`（P5：锚逻辑单点，
   已处理「同父同题 ×219」等重复场景）——非标题原子用「所属章节号路径 + `<类型>-<序号>`」，
   与标题节点同处一个分组空间，天然互不冲突。

`content` 契约（与 M04 渲染对齐，P4 零改写）：

- `format` ∈ {md, html}；`content.fragment` = **源标记逐字节原文**（标题行含 `##`、表格含
  整个 `<table>…</table>`、代码含整段围栏）；渲染期原样拼接（`ordinal` 序、`\\n\\n` 连接）；
- `content.text` 一律由 :func:`agenticdocer.model.derive_text` 生成（A10：FTS 唯一来源，非空）；
- `figure` 无 `fragment`（M01 schema 为 `additionalProperties: false`）：`asset_ref` = 文件名里的
  sha256，渲染期由 M04 合成图片语法；`cross_ref` 同样以 `text` 承载可见引用文本。

`doc_meta` 除 frontmatter 映射外还携带两份**解析期事实**（提交/审核期消费，不影响 `docs.meta`）：

- `asset_refs`：全部图片引用出现（`total`/`md`/`html`/`unique`/`refs`），提交期据此取件；
- `fallback`：兜底提议 `proposal_id` → 锚（`RawFallback` 结构无锚字段，故由解析期单点定锚）。
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final

from agenticdocer.model import (
    NodeIn,
    ParseResult,
    ParseStats,
    Proposal,
    RawFallback,
    SectionRef,
    UnmappedBlock,
    assign_anchors,
    derive_text,
)
from agenticdocer.model.anchors import section_path_str
from agenticdocer.observability import get_logger

from . import rules
from .assets_sync import collect_refs, ref_counts, unique_refs
from .frontmatter import Frontmatter, parse_frontmatter
from .rules import Block, Rule

__all__ = [
    "PROPOSAL_ID_FORMAT",
    "Section",
    "parse_markdown",
    "parse",
    "parse_text",
    "scan_blocks",
    "classify",
    "build_sections",
    "coverage",
    "atom_type_counts",
    "rule_counts",
    "report",
    "log_parse_stats",
    "fallback_anchors",
]

log = get_logger("m03.parser")

PROPOSAL_ID_FORMAT: Final = "p{:04d}"
"""提议 ID 形态（稳定、有序：同一源文件重复解析逐字节一致）。"""

_ATX_PREFIX_RE: Final = re.compile(r"(?m)^#{1,6}[ \t]+")
_XREF_TARGET_RE: Final = re.compile(
    r"\b(?:Section|Chapter|Clause|Annex|Appendix|Part|Sub-section|subsection)[ \t]+"
    r"([A-Z]?\d+(?:\.\d+)*)",
    re.IGNORECASE,
)
_HEADING_HASHES_RE: Final = re.compile(r"^(?P<hashes>#{1,6})")


# ── 章节树 ───────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Section:
    """一个标题（ADR-006：条款级最小节点的载体）。"""

    index: int
    """文档序（0 基）。"""

    block_index: int
    """标题块在块序列中的下标。"""

    rank: int
    """层级 = 编号深度（无编号标题取 `#` 个数）——即节点 `level`。"""

    path: tuple[str, ...]
    """章节号路径（无编号标题为 `()`）。"""

    title: str
    """归一标题（去 HTML 标签、折空白；用于锚 slug 与词条名）。"""

    raw_title: str
    """标题原文（`#` 之后的部分；进 content.fragment）。"""

    parent: int | None
    """父章节的 `index`（无父为 ``None``）。"""


def _is_path_prefix(parent: tuple[str, ...], child: tuple[str, ...]) -> bool:
    return len(parent) < len(child) and child[: len(parent)] == parent


def build_sections(blocks: Sequence[Block]) -> tuple[list[Section], list[int | None]]:
    """标题块 → 章节树；同时返回「每个块所属的最近标题章节」（无则 ``None``）。"""
    sections: list[Section] = []
    owner: list[int | None] = [None] * len(blocks)
    stack: list[int] = []
    current: int | None = None
    for index, block in enumerate(blocks):
        if block.kind != rules.HEADING:
            owner[index] = current
            continue
        heading = rules.match_heading(block.lines[0])
        assert heading is not None  # scan_blocks 只把标题行判为 HEADING
        raw_title = heading.group("title")
        numbered = rules.parse_numbering(raw_title)
        rank = len(numbered[0]) if numbered else len(_HEADING_HASHES_RE.match(block.lines[0]).group("hashes"))  # type: ignore[union-attr]
        path = numbered[0] if numbered else ()
        while stack:
            top = sections[stack[-1]]
            if top.rank >= rank:
                stack.pop()
                continue
            if path and top.path and not _is_path_prefix(top.path, path):
                stack.pop()
                continue
            break
        sections.append(
            Section(
                index=len(sections),
                block_index=index,
                rank=rank,
                path=path,
                title=rules.clean_text(raw_title),
                raw_title=raw_title,
                parent=stack[-1] if stack else None,
            )
        )
        stack.append(len(sections) - 1)
        current = len(sections) - 1
        owner[index] = current
    return sections, owner


# ── 块切分（形态）───────────────────────────────────────────────────────


def _shape_of(lines: Sequence[str], index: int) -> str:
    """块形态判定（纯语法，无文档级上下文）。"""
    line = lines[index]
    if rules.match_heading(line):
        return rules.HEADING
    if rules.match_fence(line):
        return rules.CODE
    if rules.match_html_table_open(line):
        return rules.TABLE_HTML
    if rules.match_md_table(lines, index):
        return rules.TABLE_MARKDOWN
    if rules.match_md_image(line) or rules.match_html_image(line):
        return rules.FIGURE
    if rules.match_list_item(line):
        return rules.LIST
    if rules.match_block_html(line):
        return rules.HTML_RESIDUE
    return rules.PARAGRAPH


def _skip_blanks(lines: Sequence[str], index: int) -> int:
    while index < len(lines) and not lines[index].strip():
        index += 1
    return index


def _consume_fence(lines: Sequence[str], index: int) -> int:
    opening = rules.match_fence(lines[index])
    assert opening is not None
    marker = opening.group("fence")[0]
    width = len(opening.group("fence"))
    index += 1
    while index < len(lines):
        closing = rules.match_fence(lines[index])
        if closing is not None and closing.group("fence")[0] == marker and len(closing.group("fence")) >= width:
            return index + 1
        index += 1
    return index  # 未闭合：整体成块（零丢弃）


def _consume_table_html(lines: Sequence[str], index: int) -> int:
    depth = 0
    while index < len(lines):
        opens, closes = rules.count_html_table_markers(lines[index])
        depth += opens - closes
        index += 1
        if depth <= 0:
            break
    return index


def _consume_table_markdown(lines: Sequence[str], index: int) -> int:
    index += 1  # 分隔行
    while index < len(lines) and lines[index].strip() and "|" in lines[index]:
        index += 1
    return index


def _consume_list(lines: Sequence[str], index: int) -> int:
    """列表块：列表项 + 其续行；松散列表（空行分隔的同类项）合并为一块。"""
    while index < len(lines):
        if rules.match_list_item(lines[index]):
            index += 1
            continue
        if not lines[index].strip():
            following = _skip_blanks(lines, index)
            if following < len(lines) and rules.match_list_item(lines[following]):
                index = following
                continue
            break
        # 续行：非特殊块起首的行属于上一个列表项（markdown lazy continuation）
        if _shape_of(lines, index) == rules.PARAGRAPH:
            index += 1
            continue
        break
    return index


def _consume_html_residue(lines: Sequence[str], index: int) -> int:
    while index < len(lines):
        if rules.match_block_html(lines[index]):
            index += 1
            continue
        if not lines[index].strip():
            following = _skip_blanks(lines, index)
            if following < len(lines) and rules.match_block_html(lines[following]):
                index = following
                continue
        break
    return index


def _consume_paragraph(lines: Sequence[str], index: int) -> int:
    while index < len(lines):
        if not lines[index].strip():
            break
        if index > 0 and _shape_of(lines, index) != rules.PARAGRAPH:
            break
        index += 1
    return index


_CONSUMERS: dict[str, Callable[[Sequence[str], int], int]] = {
    rules.HEADING: lambda lines, index: index + 1,
    rules.CODE: _consume_fence,
    rules.TABLE_HTML: _consume_table_html,
    rules.TABLE_MARKDOWN: _consume_table_markdown,
    rules.FIGURE: lambda lines, index: index + 1,
    rules.LIST: _consume_list,
    rules.HTML_RESIDUE: _consume_html_residue,
    rules.PARAGRAPH: _consume_paragraph,
}


def scan_blocks(lines: Sequence[str], *, first_line: int = 1) -> list[Block]:
    """按语法形态切块（行号 1 基闭区间，指向源文件行）。"""
    blocks: list[Block] = []
    total = len(lines)
    index = 0
    while index < total:
        if not lines[index].strip():
            index += 1
            continue
        start = index
        kind = _shape_of(lines, index)
        index = _CONSUMERS[kind](lines, index)
        end = index
        while end > start + 1 and not lines[end - 1].strip():  # 去尾空行（fragment 无首尾空行）
            end -= 1
        rule = rules.RULES[rules.RULES_BY_KIND[kind]]
        blocks.append(
            Block(
                kind=kind,
                rule_id=rule.rule_id,
                confident=rule.confident,
                start=first_line + start,
                end=first_line + end - 1,
                lines=tuple(lines[start:end]),
            )
        )
        index = max(index, end)
    return blocks


def _toc_continues(blocks: Sequence[Block], position: int) -> bool:
    """目录区延续判据：本标题之后、下一个标题之前的内容是否仍是目录条目。"""
    following: list[Block] = []
    for block in blocks[position + 1 :]:
        if block.kind == rules.HEADING:
            break
        following.append(block)
    lines = [line for block in following for line in block.lines if line.strip()]
    if not lines:
        return False
    hits = sum(1 for line in lines if rules.match_toc_line(line))
    return hits / len(lines) >= rules.TOC_CONTINUATION_RATIO


def _is_definition_entry(blocks: Sequence[Block], position: int) -> bool:
    """词条标题判据：其后到下一个标题之间**恰有一个**段落块（术语区上下文内）。"""
    following: list[Block] = []
    for block in blocks[position + 1 :]:
        if block.kind == rules.HEADING:
            break
        following.append(block)
    if len(following) != 1 or following[0].kind != rules.PARAGRAPH:
        return False
    heading = rules.match_heading(blocks[position].lines[0])
    assert heading is not None
    title = rules.clean_text(heading.group("title"))
    if not title or len(title) > 80 or rules.match_cross_ref(title):
        return False
    return len(following[0].text) >= 20


def classify(blocks: Sequence[Block]) -> list[Block]:
    """应用文档级上下文（目录区 / 术语区）→ 最终规则（`rule_id` + 待确认标志）。"""
    out: list[Block] = []
    toc_mode = False
    glossary_mode = False
    for position, block in enumerate(blocks):
        rule_id = block.rule_id
        if block.kind == rules.HEADING:
            title = block.lines[0]
            if rules.match_toc_marker(title):
                toc_mode, glossary_mode = True, False
                rule_id = rules.RULES_BY_KIND[rules.HEADING]
            elif toc_mode and _toc_continues(blocks, position):
                rule_id = rules.RULES_BY_KIND[rules.HEADING]  # 目录页眉伪标题，仍在目录区
            else:
                toc_mode = False
                if rules.match_glossary_marker(title):
                    glossary_mode = True
                elif rules.match_glossary_exit(title) or rules.parse_numbering(title):
                    glossary_mode = False
                if glossary_mode and _is_definition_entry(blocks, position):
                    rule_id = rules.DEFINITION_RULE_ID
                else:
                    rule_id = rules.RULES_BY_KIND[rules.HEADING]
        elif toc_mode:
            rule_id = rules.TOC_RULE_ID
        elif (
            glossary_mode
            and block.kind == rules.PARAGRAPH
            and rules.match_definition_paragraph(block.text)
        ):
            rule_id = rules.DEFINITION_BODY_RULE_ID
        rule = rules.RULES[rule_id]
        out.append(
            Block(
                kind=block.kind,
                rule_id=rule_id,
                confident=rule.confident,
                start=block.start,
                end=block.end,
                lines=block.lines,
            )
        )
    return out


# ── 原子构造 ─────────────────────────────────────────────────────────────


@dataclass
class _Pending:
    """待定锚的原子提议（第二遍统一定锚前的中间态）。"""

    block: Block
    atom_type: str
    format: str
    content: dict[str, Any] | None
    level: int | None
    section_path: tuple[str, ...]
    anchor_title: str
    body_text: str
    fallback: bool = False
    extra: dict[str, Any] = field(default_factory=dict)


def _strip_heading_markers(text: str) -> str:
    return _ATX_PREFIX_RE.sub("", text)


def _content(
    atom_type: str,
    *,
    fragment: str | None = None,
    text: str | None = None,
    raw: str = "",
    **extra: Any,
) -> dict[str, Any]:
    """构造原子 `content`：`fragment` 原样 + `text` 由 M01 `derive_text` 单点生成（A10）。"""
    content: dict[str, Any] = {key: value for key, value in extra.items() if value is not None}
    if fragment is not None:
        content["fragment"] = fragment
    if text is not None:
        content["text"] = text
    try:
        content["text"] = derive_text(atom_type, content)
    except ValueError:
        # 退化路径（内容为空）：仍保证 A10 的 content.text 非空，并留痕
        content["text"] = fragment or raw or atom_type
        log.warn("empty text projection", atom_type=atom_type, source_lines=list(...) if False else None)
    return content


class _TableMeta(HTMLParser := __import__("html.parser", fromlist=["HTMLParser"]).HTMLParser):  # type: ignore[misc]
    """HTML 表格结构统计（E1-a：rows/cols/cells/max_colspan，供 M09B 行列断言）。

    口径：`rows` = `<tr>` 个数；`cells` = `<td>`/`<th>` 个数；`max_colspan` = colspan 最大值；
    `cols` = 各逻辑行 colspan 之和的最大值（即最大逻辑列数）。
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows = 0
        self.cells = 0
        self.max_colspan = 1
        self.cols = 0
        self._row_span = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tr":
            self.rows += 1
            self._row_span = 0
        elif tag in ("td", "th"):
            self.cells += 1
            colspan = 1
            for name, value in attrs:
                if name == "colspan" and value:
                    try:
                        colspan = max(1, int(str(value).strip()))
                    except ValueError:
                        colspan = 1
            self.max_colspan = max(self.max_colspan, colspan)
            self._row_span += colspan
            self.cols = max(self.cols, self._row_span)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def table_meta(fragment: str, *, markdown: bool) -> dict[str, int]:
    """表格结构元数据（HTML 片段用 HTMLParser 统计；md 表格按行/单元格切分统计）。"""
    if not markdown:
        parser = _TableMeta()
        parser.feed(fragment)
        parser.close()
        return {"rows": parser.rows, "cols": parser.cols, "cells": parser.cells, "max_colspan": parser.max_colspan}
    rows = [line for line in fragment.split("\n") if line.strip()]
    data_rows = [line for line in rows if not re.fullmatch(r"[ \t]*\|?[\s:|-]+\|?[ \t]*", line)]
    columns = 0
    cells = 0
    for line in data_rows:
        count = len([cell for cell in line.strip().strip("|").split("|")])
        columns = max(columns, count)
        cells += count
    return {"rows": len(data_rows), "cols": columns, "cells": cells, "max_colspan": 1}
