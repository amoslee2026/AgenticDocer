"""M03 导入解析：markdown（+frontmatter）→ 原子提议（规则 + 待确认标志 + 未映射块清单）。

权威来源：`architecture_specification.md` §3 M03、§6（frontmatter 映射）、
`functional_specification.md` REQ-M03-F01/F04/F05、`ADR-006`（结构化粒度与锚策略）、
`design_doc.md` §5.1（内容原子与格式策略）、§6.1（导入流）、§10（覆盖率口径）。

解析流水线（全部确定性，无 LLM/P6）：

1. **frontmatter** → :class:`~agenticspec.importer.frontmatter.Frontmatter`
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
6. **定锚**：整档一次 :func:`agenticspec.model.assign_anchors`（P5：锚逻辑单点，
   已处理「同父同题 ×219」等重复场景）——非标题原子用「所属章节号路径 + `<类型>-<序号>`」，
   与标题节点同处一个分组空间，天然互不冲突。

`content` 契约（与 M04 渲染对齐，P4 零改写）：

- `format` ∈ {md, html}；`content.fragment` = **源标记逐字节原文**（标题行含 `##`、表格含
  整个 `<table>…</table>`、代码含整段围栏）；渲染期原样拼接（`ordinal` 序、`\\n\\n` 连接）；
- `content.text` 一律由 :func:`agenticspec.model.derive_text` 生成（A10：FTS 唯一来源，非空）；
- `figure` 无 `fragment`（M01 schema 为 `additionalProperties: false`）：`asset_ref` = 文件名里的
  sha256，渲染期由 M04 合成图片语法；`cross_ref` 同样以 `text` 承载可见引用文本。

`doc_meta` 除 frontmatter 映射外还携带两份**解析期事实**（提交/审核期消费，不影响 `docs.meta`）：

- `asset_refs`：全部图片引用出现（`total`/`md`/`html`/`unique`/`refs`），提交期据此取件；
- `fallback`：兜底提议 `proposal_id` → 锚（`RawFallback` 结构无锚字段，故由解析期单点定锚）。
"""

from __future__ import annotations

import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Final

from agenticspec.model import (
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
from agenticspec.model.anchors import section_path_str
from agenticspec.model import html_to_text
from agenticspec.observability import get_logger

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
    "atom_content",
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


_DEFINITION_ENTRY_MAX_CHARS: Final = 2000
"""词条正文长度上限：超过即视为普通小节（防止把术语区内的长小节并成定义）。"""


def _is_definition_entry(blocks: Sequence[Block], position: int) -> bool:
    """词条标题判据（术语区上下文内）：其后到下一个标题之间**全是段落**且正文不长。

    语料实测：PCIe 词条 = 标题 + 单段落；AMBA AXI 词条（`## Aligned`）常为「标题 + 2 段」，
    故允许**多段**，但要求无非段落块（表格/图/代码/列表会退出判据）且总长 ≤ 2000 字符。
    区域标记标题本身（`Glossary`/`Terms and Acronyms`…）与终止标题不判为词条。
    """
    following: list[Block] = []
    for block in blocks[position + 1 :]:
        if block.kind == rules.HEADING:
            break
        following.append(block)
    if not following or any(item.kind != rules.PARAGRAPH for item in following):
        return False
    if sum(len(item.text) for item in following) > _DEFINITION_ENTRY_MAX_CHARS:
        return False
    heading = rules.match_heading(blocks[position].lines[0])
    assert heading is not None
    title = heading.group("title")
    if rules.match_glossary_marker(title) or rules.match_glossary_exit(title):
        return False
    cleaned = rules.clean_text(title)
    if not cleaned or len(cleaned) > 80 or rules.match_cross_ref(cleaned):
        return False
    return len(following[0].text) >= 20


def classify(blocks: Sequence[Block]) -> list[Block]:
    """应用文档级上下文（目录区 / 术语区）与文本线索规则 → 最终规则（+ 待确认标志）。

    顺序（先结构、后上下文、再线索）：
    ① 结构性原子（表格/图片/代码/块级 HTML）**不受上下文影响**——形态即结论；
    ② 标题块永远不成兜底——是 `definition`（术语区内词条）还是 `clause`；
    ③ 目录区内（Contents/List of Tables…）的其余块 → 兜底规则（F01，不计覆盖率）；
    ④ 术语区内的「术语 释义…」段落 → `definition`（R12，启发式）；
    ⑤ 其余段落按线索判 `cross_ref`（R09）/`example`（R10），都不中才并入条款（R11）。

    术语区/目录区也可由**纯文本标记行**开启（mineru 常丢标题层级，实测 AMBA AXI
    `Part C Glossary` 就是一整行普通文本），标记行本身仍按段落规则归属条款。
    """
    out: list[Block] = []
    toc_mode = False
    glossary_mode = False
    for position, block in enumerate(blocks):
        rule_id = block.rule_id
        if block.kind == rules.HEADING:
            rule_id, (toc_mode, glossary_mode) = _classify_heading(
                blocks, position, toc_mode, glossary_mode
            )
        elif block.rule_id in _STRUCTURAL_RULES:
            if block.rule_id == "R03.table.html" and rules.match_empty_table_fragment(block.text):
                rule_id = "F04.table.text-empty"  # A10 无从派生 text → 兜底保留（REQ-M03-F04）
            elif block.rule_id == "F02.html.residue" and rules.match_html_pre_code(block.text):
                rule_id = "R13.code.html-pre"  # HTML 形态的代码块 → code（format=html，P4 直通）
        elif toc_mode:
            rule_id = rules.TOC_RULE_ID
        elif block.kind == rules.PARAGRAPH:
            if _is_marker_line(block.text, rules.match_glossary_marker):
                glossary_mode = True
            if glossary_mode and rules.match_definition_paragraph(block.text):
                rule_id = rules.DEFINITION_BODY_RULE_ID
            elif rules.match_cross_ref(block.text):
                rule_id = "R09.cross_ref.sentence"
            elif rules.match_example(block.text):
                rule_id = "R10.example.callout"
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


_STRUCTURAL_RULES: Final[frozenset[str]] = frozenset(
    {
        "R03.table.html",
        "R04.table.markdown",
        "R05.code.fenced",
        "R06.figure.image",
        "R07.figure.html-img",
        "F02.html.residue",
    }
)
"""形态即结论的规则：表格/图片/代码/块级 HTML 残余——**不**被目录区上下文改写。"""

_MARKER_MAX_CHARS: Final = 80


def _is_marker_line(text: str, matcher: Callable[[str], Any]) -> bool:
    """纯文本区域标记行（短、无目录点引导）——如 `Part C Glossary`。"""
    flattened = " ".join(text.split())
    if not flattened or len(flattened) > _MARKER_MAX_CHARS:
        return False
    if rules.match_toc_line(flattened):
        return False
    return matcher(flattened) is not None


def _classify_heading(
    blocks: Sequence[Block],
    position: int,
    toc_mode: bool,
    glossary_mode: bool,
) -> tuple[str, tuple[bool, bool]]:
    """标题块的规则与（更新后的）上下文状态：``(rule_id, (toc_mode, glossary_mode))``。"""
    heading = rules.match_heading(blocks[position].lines[0])
    assert heading is not None
    title = heading.group("title")
    if rules.match_toc_marker(title):
        return rules.RULES_BY_KIND[rules.HEADING], (True, False)
    if toc_mode and _toc_continues(blocks, position):
        return rules.RULES_BY_KIND[rules.HEADING], (True, glossary_mode)  # 目录页眉伪标题
    if rules.match_glossary_marker(title):
        glossary_mode = True
    elif rules.match_glossary_exit(title) or rules.parse_numbering(title):
        glossary_mode = False
    if glossary_mode and _is_definition_entry(blocks, position):
        return rules.DEFINITION_RULE_ID, (False, glossary_mode)
    return rules.RULES_BY_KIND[rules.HEADING], (False, glossary_mode)


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
    heading: bool = False
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def source_lines(self) -> tuple[int, int]:
        """来源行区间（clause 节点含并入的正文段落范围，见 `extra["source_lines"]`）。"""
        value = self.extra.get("source_lines")
        return value if isinstance(value, tuple) else self.block.source_lines


def _strip_heading_markers(text: str) -> str:
    return _ATX_PREFIX_RE.sub("", text)


def atom_content(
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
        # 退化路径（投影为空）：仍保证 A10 的 content.text 非空，并留痕（便于发现解析退化）
        content["text"] = fragment or raw or atom_type
        log.warn("empty text projection", atom_type=atom_type)
    return content


class _TableMeta(HTMLParser):
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


def table_meta(fragment: str, *, markdown: bool = False) -> dict[str, int]:
    """表格结构元数据（HTML 片段用 :class:`_TableMeta` 统计；md 表格按行/单元格统计）。"""
    if not markdown:
        parser = _TableMeta()
        parser.feed(fragment)
        parser.close()
        return {
            "rows": parser.rows,
            "cols": parser.cols,
            "cells": parser.cells,
            "max_colspan": parser.max_colspan,
        }
    rows = [line for line in fragment.split("\n") if line.strip()]
    data_rows = [line for line in rows if not _MD_TABLE_DELIMITER_RE.fullmatch(line)]
    columns = 0
    cells = 0
    for line in data_rows:
        count = len(line.strip().strip("|").split("|"))
        columns = max(columns, count)
        cells += count
    return {"rows": len(data_rows), "cols": columns, "cells": cells, "max_colspan": 1}


_MD_TABLE_DELIMITER_RE: Final = re.compile(r"^[ \t]*\|?[\s:|-]+\|?[ \t]*$")


# ── 原子提议构造（规则 → 原子）──────────────────────────────────────────


def _absorbed_by_heading(
    blocks: Sequence[Block], sections: Sequence[Section], owner: Sequence[int | None]
) -> tuple[dict[int, list[Block]], list[Block]]:
    """→ (标题块下标 → 并入该条款的正文段落, 序言段落)。

    序言段落 = 首个标题之前的段落（无归属）；它们并入一个 `preamble` 条款节点，
    保证「零静默丢弃」（源块数 = 承接 + 兜底，见 :func:`report`）。
    """
    absorbed: dict[int, list[Block]] = {section.block_index: [] for section in sections}
    preamble: list[Block] = []
    for index, block in enumerate(blocks):
        if block.kind == rules.HEADING or block.rule_id != "R11.paragraph.clause-body":
            continue
        section_index = owner[index]
        if section_index is None:
            preamble.append(block)
        else:
            absorbed[sections[section_index].block_index].append(block)
    return absorbed, preamble


def _join_blocks(items: Sequence[Block]) -> str:
    """按源序拼接块原文（单空行分隔）——clause/definition 节点把并入的正文段落合成一段。

    **P4 零改写口径**：每个块的原文逐字节保留（不重排、不改写）；块被抽成独立原子
    （表格/图/代码/列表/引用）时其内容不并入，故合成结果不保证是源文本的**连续子串**，
    但恒为「源块的原文按源序的拼接」。渲染期按 `ordinal` 拼回时以单空行分隔，
    与 M04 的 normalize 口径（标题/表格/图/列表/内联标记，不含空行数）一致。
    """
    return "\n\n".join(item.text for item in items)

def _term_of(section: Section) -> str:
    """词条名：标题去编号后的余下文本（无编号标题即标题本身）。"""
    numbered = rules.parse_numbering(section.raw_title)
    if numbered is not None and numbered[1]:
        return numbered[1]
    return section.title or section.raw_title


def _clause_pending(
    section: Section | None,
    block: Block,
    prose: Sequence[Block],
) -> _Pending:
    """标题 → clause 节点（正文段落并入 `content.fragment`，ADR-006）。"""
    fragment = _join_blocks([block, *prose])
    end = prose[-1].end if prose else block.end
    return _Pending(
        block=block,
        atom_type="clause",
        format="md",
        content=atom_content(
            "clause",
            fragment=fragment,
            text=_strip_heading_markers(fragment),
            raw=fragment,
        ),
        level=section.rank if section is not None else 1,
        section_path=section.path if section is not None else (),
        anchor_title=section.title if section is not None else "preamble",
        body_text=fragment,
        heading=True,
        extra={"source_lines": (block.start, end)},
    )


def _definition_heading_pending(section: Section, block: Block, prose: Sequence[Block]) -> _Pending:
    """术语区词条标题 → definition 节点（fragment 含标题行，渲染零改写）。"""
    fragment = _join_blocks([block, *prose])
    end = prose[-1].end if prose else block.end
    return _Pending(
        block=block,
        atom_type="definition",
        format="md",
        content=atom_content(
            "definition",
            fragment=fragment,
            text=_strip_heading_markers(fragment),
            term=_term_of(section),
        ),
        level=section.rank,
        section_path=section.path,
        anchor_title=section.title,
        body_text=fragment,
        heading=True,
        extra={"source_lines": (block.start, end)},
    )


def _definition_paragraph_pending(block: Block, match: re.Match[str]) -> _Pending:
    """术语区 `术语 释义…` 段落 → definition 节点。"""
    return _Pending(
        block=block,
        atom_type="definition",
        format="md",
        content=atom_content("definition", fragment=block.text, text=block.text, term=match.group("term")),
        level=None,
        section_path=(),
        anchor_title="",
        body_text=block.text,
    )


def _table_pending(block: Block) -> _Pending:
    """表格块 → table 节点（`fragment` 原样直通；`meta` 为结构统计，E1-a）。"""
    markdown = block.rule_id == "R04.table.markdown"
    return _Pending(
        block=block,
        atom_type="table",
        format="md" if markdown else "html",
        content=atom_content("table", fragment=block.text, meta=table_meta(block.text, markdown=markdown)),
        level=None,
        section_path=(),
        anchor_title="",
        body_text=block.text,
    )


def _code_pending(block: Block) -> _Pending:
    """围栏代码块 → code 节点（整段围栏进 `fragment`；`text` 为围栏内原文）。"""
    opening = rules.match_fence(block.lines[0])
    language = opening.group("lang") if opening is not None else ""
    closed = len(block.lines) > 1 and rules.match_fence(block.lines[-1]) is not None
    inner = "\n".join(block.lines[1:-1] if closed else block.lines[1:])
    return _Pending(
        block=block,
        atom_type="code",
        format="md",
        content=atom_content(
            "code",
            fragment=block.text,
            text=inner.strip() or block.text,
            language=language or None,
        ),
        level=None,
        section_path=(),
        anchor_title="",
        body_text=block.text,
    )


_HTML_ALT_RE: Final = re.compile(r"\balt\s*=\s*[\"']?(?P<alt>[^\"'>]*)", re.IGNORECASE)


def _code_html_pending(block: Block) -> _Pending:
    """块级 `<pre>`（HTML 形态代码块）→ code 节点（`format=html`，fragment 逐字节原样）。"""
    return _Pending(
        block=block,
        atom_type="code",
        format="html",
        content=atom_content("code", fragment=block.text, text=html_to_text(block.text) or block.text),
        level=None,
        section_path=(),
        anchor_title="",
        body_text=block.text,
    )


def _figure_pending(block: Block) -> _Pending:
    """图片块 → figure 节点（`asset_ref` = 文件名 sha256；无 `fragment`，渲染期由 M04 合成）。"""
    if block.rule_id == "R06.figure.image":
        match = rules.match_md_image(block.text)
        alt = match.group("alt") if match is not None else ""
        source = match.group("src") if match is not None else block.text
    else:
        match = rules.match_html_image(block.text)
        source = match.group("src") if match is not None else block.text
        alt_match = _HTML_ALT_RE.search(block.text)
        alt = alt_match.group("alt") if alt_match is not None else ""
    ref = collect_refs(f'![{alt}]({source})')[0]
    return _Pending(
        block=block,
        atom_type="figure",
        format="html" if block.rule_id == "R07.figure.html-img" else "md",
        content=atom_content(
            "figure",
            text=alt.strip() or source,
            alt=alt.strip() or None,
            asset_ref=ref.sha256,
        ),
        level=None,
        section_path=(),
        anchor_title="",
        body_text=block.text,
    )


def _note_pending(block: Block) -> _Pending:
    """列表块 → note 节点（原样 `fragment`，渲染期直通）。"""
    return _Pending(
        block=block,
        atom_type="note",
        format="md",
        content=atom_content("note", fragment=block.text, text=block.text),
        level=None,
        section_path=(),
        anchor_title="",
        body_text=block.text,
    )


def _cross_ref_pending(block: Block, doc_id: str) -> _Pending:
    """交叉引用块 → cross_ref 节点（+ 提交期 refs 边）。"""
    return _Pending(
        block=block,
        atom_type="cross_ref",
        format="md",
        content=atom_content("cross_ref", text=block.text, ref_kind="see_also", target_doc_id=doc_id),
        level=None,
        section_path=(),
        anchor_title="",
        body_text=block.text,
    )


def _example_pending(block: Block) -> _Pending:
    """示例块 → example 节点。"""
    return _Pending(
        block=block,
        atom_type="example",
        format="md",
        content=atom_content("example", fragment=block.text, text=block.text),
        level=None,
        section_path=(),
        anchor_title="",
        body_text=block.text,
    )


def _plan(
    blocks: Sequence[Block],
    sections: Sequence[Section],
    owner: Sequence[int | None],
    doc_id: str,
) -> list[_Pending]:
    """块序列 → 待定锚原子序列（**文档序**，即最终 `ordinal` 序）。"""
    absorbed, preamble = _absorbed_by_heading(blocks, sections, owner)
    preamble_at = preamble[0].start if preamble else None
    pending: list[_Pending] = []
    counters: dict[tuple[int | None, str], int] = {}
    for index, block in enumerate(blocks):
        rule = rules.RULES[block.rule_id]
        section_index = owner[index]
        section = sections[section_index] if section_index is not None else None
        if block.kind == rules.HEADING:
            assert section is not None
            prose = absorbed.get(section.block_index, [])
            if block.rule_id == rules.DEFINITION_RULE_ID:
                pending.append(_definition_heading_pending(section, block, prose))
            else:
                pending.append(_clause_pending(section, block, prose))
            continue
        if block.rule_id == "R11.paragraph.clause-body":
            if block.start == preamble_at:  # 序言：首个括号外段落起，整段并入单个 preamble 节点
                pending.append(_clause_pending(None, block, preamble[1:]))
            continue
        key = (section_index, rule.atom_type)
        counters[key] = counters.get(key, 0) + 1
        title = f"{rule.atom_type}-{counters[key]}"
        if block.rule_id == rules.DEFINITION_BODY_RULE_ID:
            match = rules.match_definition_paragraph(block.text)
            assert match is not None  # 规则命中即已匹配
            item = _definition_paragraph_pending(block, match)
        elif block.rule_id in ("R03.table.html", "R04.table.markdown"):
            item = _table_pending(block)
        elif block.rule_id == "R05.code.fenced":
            item = _code_pending(block)
        elif block.rule_id == "R13.code.html-pre":
            item = _code_html_pending(block)
        elif block.rule_id in ("R06.figure.image", "R07.figure.html-img"):
            item = _figure_pending(block)
        elif block.rule_id == "R08.list.note":
            item = _note_pending(block)
        elif block.rule_id == "R09.cross_ref.sentence":
            item = _cross_ref_pending(block, doc_id)
        elif block.rule_id == "R10.example.callout":
            item = _example_pending(block)
        else:  # 兜底规则：F01/F02/F03（结构无锚字段，锚由解析期单点定，见 doc_meta["fallback"]）
            item = _Pending(
                block=block,
                atom_type=rule.atom_type,
                format="html" if block.kind in (rules.HTML_RESIDUE, rules.TABLE_HTML) else "md",
                content=None,
                level=None,
                section_path=section.path if section is not None else (),
                anchor_title=title,
                body_text=block.text,
                fallback=True,
            )
        if not item.heading:  # 非标题原子：锚取所属章节号路径 +「<类型>-<章节内序号>」
            if section is not None:
                item.section_path = section.path
            item.anchor_title = title
        pending.append(item)
    return pending


def _resolve_cross_refs(pending: Sequence[_Pending]) -> dict[str, int]:
    """把 `See Section 1.2.3` 解析到**本档内**已定锚的章节（同一文档内可解析者）。

    未解析的引用保留为「文档级 see_also 边」（`dst_node_id IS NULL`）——M09B
    `broken_refs` 巡检的口径来源（ADR-009：dst 不校验，悬空目标由巡检报告）。
    """
    by_path = {
        section_path_str(item.section_path): item.extra["anchor"]
        for item in pending
        if item.heading and item.section_path and "anchor" in item.extra
    }
    total = resolved = 0
    unresolved: list[str] = []
    for item in pending:
        if item.atom_type != "cross_ref" or item.content is None:
            continue
        total += 1
        match = _XREF_TARGET_RE.search(str(item.content.get("text", "")))
        target = by_path.get(match.group(1)) if match is not None else None
        if target is None:
            unresolved.append(str(item.content.get("text", ""))[:160])
            continue
        item.content["target_anchor"] = target
        resolved += 1
    return {"total": total, "resolved": resolved, "unresolved": unresolved}


def fallback_anchors(result: ParseResult) -> dict[str, str]:
    """兜底提议 `proposal_id` → 锚（`RawFallback` 无锚字段，锚在解析期定于 `doc_meta`）。"""
    mapping = result.doc_meta.get("fallback")
    return dict(mapping) if isinstance(mapping, dict) else {}


# ── 统计与报告 ───────────────────────────────────────────────────────────


def coverage(stats: ParseStats) -> float:
    """规则覆盖率 = 携带 `rule_id` 的源块数 ÷ 总源块数（design_doc §10；目标 ≥95%）。"""
    return stats.rule_covered / stats.total_blocks if stats.total_blocks else 0.0


def atom_type_counts(result: ParseResult) -> dict[str, int]:
    """各原子类型计数（含兜底原子；变体按基底名计数）。"""
    counts: dict[str, int] = {}
    for proposal in result.proposals:
        kind = proposal.atom.atom_type.split(".", 1)[0]
        counts[kind] = counts.get(kind, 0) + 1
    return dict(sorted(counts.items()))


def rule_counts(result: ParseResult) -> dict[str, int]:
    """各规则命中计数（`rule_id` → 提议数）。"""
    counts: dict[str, int] = {}
    for proposal in result.proposals:
        counts[proposal.rule_id] = counts.get(proposal.rule_id, 0) + 1
    return dict(sorted(counts.items()))


def report(result: ParseResult) -> dict[str, Any]:
    """解析统计报告（`stats` CLI 的输出口径；coverage/兜底率/待确认条数/未映射清单）。"""
    stats = result.stats
    blocks = result.doc_meta.get("blocks") if isinstance(result.doc_meta.get("blocks"), dict) else {}
    unmapped_reasons: dict[str, int] = {}
    for item in result.unmapped:
        unmapped_reasons[item.reason] = unmapped_reasons.get(item.reason, 0) + 1
    return {
        "doc_id": result.doc_meta.get("doc_id"),
        "doc_slug": result.doc_meta.get("doc_slug"),
        "total_blocks": stats.total_blocks,
        "rule_covered": stats.rule_covered,
        "fallback": stats.fallback,
        "pending": stats.pending,
        "coverage": round(coverage(stats), 6),
        "fallback_ratio": round(stats.fallback / stats.total_blocks, 6) if stats.total_blocks else 0.0,
        "proposals": len(result.proposals),
        "absorbed": blocks.get("absorbed"),
        "blocks_by_kind": blocks.get("by_kind", {}),
        "atom_types": atom_type_counts(result),
        "rules": rule_counts(result),
        "unmapped": {"count": len(result.unmapped), "reasons": unmapped_reasons},
        "asset_refs": result.doc_meta.get("asset_refs", {}),
        "cross_ref": {
            key: value
            for key, value in (result.doc_meta.get("cross_ref") or {}).items()
            if key != "unresolved"
        },
    }


COVERAGE_TARGET: Final = 0.95
"""规则覆盖率目标（§1.4 指标：规则覆盖率 ≥95%；低于目标记 WARN）。"""


def log_parse_stats(result: ParseResult, *, module: str = "m03.parser", **extra: Any) -> dict[str, Any]:
    """落解析统计（M12 度量：覆盖率/兜底率/待确认条数；低于目标记 WARN）并返回报告。"""
    summary = report(result)
    fields: dict[str, Any] = {
        "doc_id": summary["doc_id"],
        "doc_slug": summary["doc_slug"],
        "total_blocks": summary["total_blocks"],
        "rule_covered": summary["rule_covered"],
        "coverage": summary["coverage"],
        "fallback": summary["fallback"],
        "fallback_ratio": summary["fallback_ratio"],
        "pending": summary["pending"],
        "atom_types": summary["atom_types"],
        **extra,
    }
    emit = log.info if summary["coverage"] >= COVERAGE_TARGET else log.warn
    emit("import parse stats", module=module, **fields)
    return summary


# ── 入口 ─────────────────────────────────────────────────────────────────


def parse_text(
    text: str,
    *,
    doc_slug: str,
    source_path: Path | None = None,
) -> ParseResult:
    """解析 markdown 文本 → :class:`ParseResult`（确定性：同一输入逐字节一致）。"""
    frontmatter: Frontmatter = parse_frontmatter(text, doc_slug=doc_slug, source_path=source_path)
    doc_id = frontmatter.doc_id
    lines = frontmatter.body.split("\n")
    blocks = classify(scan_blocks(lines, first_line=frontmatter.body_start))
    sections, owner = build_sections(blocks)
    pending = _plan(blocks, sections, owner, doc_id)
    anchors = assign_anchors(
        doc_id,
        [SectionRef(item.section_path, item.anchor_title, item.body_text) for item in pending],
    )
    for item, anchor in zip(pending, anchors):
        item.extra["anchor"] = anchor
    # 引用解析必须在建 NodeIn 之前：pydantic 校验会复制 content，
    # 之后再改 `item.content` 不会影响已构造的原子（跨引用目标锚因此需先落定）。
    cross_ref = _resolve_cross_refs(pending)
    proposals: list[Proposal] = []
    unmapped: list[UnmappedBlock] = []
    fallback_map: dict[str, str] = {}
    for position, (item, anchor) in enumerate(zip(pending, anchors)):
        proposal_id = PROPOSAL_ID_FORMAT.format(position + 1)
        if item.fallback:
            fallback = RawFallback(
                atom_type=item.atom_type,
                format=item.format,
                text=item.block.text,
                source_lines=item.source_lines,
            )
            proposals.append(
                Proposal(
                    proposal_id=proposal_id,
                    rule_id=item.block.rule_id,
                    confident=item.block.confident,
                    source_lines=item.source_lines,
                    atom=fallback,
                )
            )
            unmapped.append(
                UnmappedBlock(
                    source_lines=item.source_lines,
                    reason=rules.RULES[item.block.rule_id].description,
                    fallback=fallback,
                )
            )
            fallback_map[proposal_id] = anchor
            continue
        proposals.append(
            Proposal(
                proposal_id=proposal_id,
                rule_id=item.block.rule_id,
                confident=item.block.confident,
                source_lines=item.source_lines,
                atom=NodeIn(
                    node_id=None,
                    doc_id=doc_id,
                    atom_type=item.atom_type,
                    format=item.format,  # type: ignore[arg-type]
                    # ordinal = 源行号（稳定：与 proposal.source_lines[0] 恒等，
                    # 重解析/审核筛选都不改变块序；M04 按 ordinal 拼接即还原源序）
                    ordinal=item.source_lines[0],
                    parent_node_id=None,  # 层级由 (level, ordinal) 在提交期重建（node_id 提交期才产生）
                    level=item.level,
                    anchor=anchor,
                    content=item.content or {},
                ),
            )
        )

    by_kind: dict[str, int] = {}
    for block in blocks:
        by_kind[block.kind] = by_kind.get(block.kind, 0) + 1
    rule_covered = sum(1 for block in blocks if rules.RULES[block.rule_id].category == "mapped")
    stats = ParseStats(
        total_blocks=len(blocks),
        rule_covered=rule_covered,
        fallback=len(blocks) - rule_covered,
        pending=sum(1 for proposal in proposals if not proposal.confident),
    )
    if stats.total_blocks != stats.rule_covered + stats.fallback:  # 零静默丢弃（不变量）
        log.error(
            "block accounting mismatch",
            total_blocks=stats.total_blocks,
            rule_covered=stats.rule_covered,
            fallback=stats.fallback,
            error_code="DTO_PARSE_ACCOUNTING",
        )
    asset_refs = collect_refs(text)
    doc_meta: dict[str, Any] = {
        **frontmatter.doc_meta,
        "body_start": frontmatter.body_start,
        "blocks": {
            "total": len(blocks),
            "absorbed": sum(
                1
                for block in blocks
                if rules.RULES[block.rule_id].category == "mapped"
                and block.kind in (rules.PARAGRAPH,)
                and block.rule_id == "R11.paragraph.clause-body"
            ),
            "by_kind": by_kind,
        },
        "asset_refs": {**ref_counts(asset_refs), "refs": unique_refs(asset_refs)},
        "cross_ref": cross_ref,
        "fallback": fallback_map,
    }
    return ParseResult(
        doc_meta=doc_meta,
        proposals=proposals,
        unmapped=unmapped,
        stats=stats,
    )


def parse_markdown(path: Path | str, doc_slug: str | None = None) -> ParseResult:
    """解析 markdown 文件（§3 M03 接口）。

    `doc_slug` 缺省 = 源文件名去 `.md`（§3 M03：「如 `IHI0024_AMBA_APB_spec`」），
    仅用于导入工作区（`data/import_work/<doc_slug>/`）；`doc_id` 一律取 frontmatter `spec_id`。
    """
    source = Path(path)
    slug = doc_slug or source.stem
    text = source.read_text(encoding="utf-8")
    with log.timer("parse_markdown", module="m03.parser", doc_slug=slug, bytes=len(text)):
        return parse_text(text, doc_slug=slug, source_path=source)


def parse(path: Path | str, doc_slug: str | None = None) -> ParseResult:
    """`parse_markdown` 的别名（§3 M03 接口名与 CLI 子命令同名）。"""
    return parse_markdown(path, doc_slug)
