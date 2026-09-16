"""M03 规则库：源块 → 原子提议的**可追溯**规则（rule_id / 版本 / 描述 / 匹配器）。

权威来源：`architecture_specification.md` §3 M03、`functional_specification.md`
REQ-M03-F01/F04、`design_doc.md` §5.1（内容原子与格式策略 E1）、§6.1（未映射兜底）、
§10（规则覆盖率口径 = 携带 rule_id 的源块数 ÷ 总源块数）。

三件事在本模块单点定义，其余模块只引用：

1. **源块（:class:`Block`）**：markdown 按其**语法形态**切分出的最小可计数单元——
   口径见 design_doc §10「源块 = 标题/表格/图/代码块/列表/段落」；
2. **规则（:class:`Rule`）**：`rule_id` 可追溯四元组（版本、描述、匹配器、原子映射）。
   `category="mapped"` 的规则计入规则覆盖率分子；`category="fallback"` 的规则是
   **兜底**（REQ-M03-F04：降级为 `note`/`code` 保留，不计入覆盖率、单列兜底率），
   二者都**不丢弃**源内容（零静默丢弃）；
3. **匹配器（matcher）**：纯函数（行文本/行序列 → 判定），名字登记在 :data:`MATCHERS`，
   `Rule.matcher` 必须能在其中解析到——规则库可自证（测试断言无悬空匹配器）。

匹配器**只做形态判定**，不做文档级上下文判定（目录区/术语区是上下文口径，由
:mod:`agenticdocer.importer.parser` 的 `classify()` 应用，见 :data:`TOC_RULE_ID`、
:data:`DEFINITION_RULE_ID`）。
"""

from __future__ import annotations

import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, Final, Literal

from agenticdocer.model import html_to_text

__all__ = [
    "RULE_SET_VERSION",
    "Rule",
    "RuleCategory",
    "Block",
    "RULES",
    "RULES_BY_KIND",
    "MATCHERS",
    "TOC_RULE_ID",
    "DEFINITION_RULE_ID",
    "DEFINITION_BODY_RULE_ID",
    "TOC_CONTINUATION_RATIO",
    "DEFINITION_STOPWORDS",
    "clean_text",
    "parse_numbering",
    "count_html_table_markers",
    "match_heading",
    "match_fence",
    "match_html_table_open",
    "match_html_table_close",
    "match_md_table",
    "match_md_image",
    "match_html_image",
    "match_list_item",
    "match_block_html",
    "match_toc_marker",
    "match_toc_line",
    "match_glossary_marker",
    "match_glossary_exit",
    "match_cross_ref",
    "match_example",
    "match_definition_paragraph",
]

RULE_SET_VERSION: Final = "1.0.0"
"""规则集版本；`rule_id` 的语义（匹配器/原子映射）变更时递增（可追溯性要求）。"""

RuleCategory = Literal["mapped", "fallback"]

# ── 源块种类（§10 口径：标题/表格/图/代码块/列表/段落 + 残余 HTML）──────────

HEADING: Final = "heading"
TABLE_HTML: Final = "table.html"
TABLE_MARKDOWN: Final = "table.markdown"
CODE: Final = "code"
FIGURE: Final = "figure"
LIST: Final = "list"
PARAGRAPH: Final = "paragraph"
HTML_RESIDUE: Final = "html.residue"


@dataclass(frozen=True)
class Block:
    """一个源块（语法形态切分的最小单元；行号 1 基、闭区间、指向**源文件**行）。"""

    kind: str
    rule_id: str
    confident: bool
    start: int
    end: int
    lines: tuple[str, ...]

    @property
    def text(self) -> str:
        """块原文（行以 ``\\n`` 连接，**不含**首尾空行——P4 零改写的搬运单位）。"""
        return "\n".join(self.lines)

    @property
    def source_lines(self) -> tuple[int, int]:
        """来源定位（闭区间，1 基）——REQ-M03-F01「提议含来源定位」。"""
        return (self.start, self.end)


@dataclass(frozen=True)
class Rule:
    """一条可追溯规则。"""

    rule_id: str
    version: str
    description: str
    atom_type: str
    category: RuleCategory
    confident: bool
    matcher: str
    """匹配器名（:data:`MATCHERS` 的键）；规则库自证用。"""


_TABLE_META_DOC = "（meta 由解析器统计：rows/cols/cells/max_colspan，E1-a）"

RULES: dict[str, Rule] = {
    rule.rule_id: rule
    for rule in (
        Rule(
            "R01.heading.clause",
            RULE_SET_VERSION,
            "ATX 标题行 → clause（ADR-006：条款为最小节点；其正文段落并入 content.fragment）",
            "clause",
            "mapped",
            True,
            "match_heading",
        ),
        Rule(
            "R02.heading.definition",
            RULE_SET_VERSION,
            "术语区内的标题行（词条标题 + 单段落正文）→ definition",
            "definition",
            "mapped",
            True,
            "match_glossary_marker",
        ),
        Rule(
            "R03.table.html",
            RULE_SET_VERSION,
            f"HTML `<table>…</table>` 片段 → table（format=html，原样直通，P4）{_TABLE_META_DOC}",
            "table",
            "mapped",
            True,
            "match_html_table_open",
        ),
        Rule(
            "R04.table.markdown",
            RULE_SET_VERSION,
            f"markdown 管道表格 → table（format=md，原样直通）{_TABLE_META_DOC}",
            "table",
            "mapped",
            True,
            "match_md_table",
        ),
        Rule(
            "R05.code.fenced",
            RULE_SET_VERSION,
            "围栏代码块（```/~~~）→ code（含围栏原样保留）",
            "code",
            "mapped",
            True,
            "match_fence",
        ),
        Rule(
            "R06.figure.image",
            RULE_SET_VERSION,
            "独占一行的 markdown 图片引用 `![alt](images/<sha256>.jpg)` → figure（asset_ref=sha256）",
            "figure",
            "mapped",
            True,
            "match_md_image",
        ),
        Rule(
            "R07.figure.html-img",
            RULE_SET_VERSION,
            "独占一行的 HTML `<img src=…>` → figure（启发式：语料内 <img> 均在 <table> 片段内）",
            "figure",
            "mapped",
            False,
            "match_html_image",
        ),
        Rule(
            "R08.list.note",
            RULE_SET_VERSION,
            "列表块（无序/有序，含跨空行的松散列表）→ note",
            "note",
            "mapped",
            True,
            "match_list_item",
        ),
        Rule(
            "R09.cross_ref.sentence",
            RULE_SET_VERSION,
            "整块即交叉引用（`See Section 1.2.3` 等）→ cross_ref（启发式：文本线索判定）",
            "cross_ref",
            "mapped",
            False,
            "match_cross_ref",
        ),
        Rule(
            "R10.example.callout",
            RULE_SET_VERSION,
            "`Example …` 起首的段落 → example（启发式：文本线索判定）",
            "example",
            "mapped",
            False,
            "match_example",
        ),
        Rule(
            "R11.paragraph.clause-body",
            RULE_SET_VERSION,
            "正文段落 → 并入所属 clause 的 content.fragment（ADR-006：段落不单独成节点）",
            "clause",
            "mapped",
            True,
            "match_paragraph",
        ),
        Rule(
            "R12.paragraph.definition",
            RULE_SET_VERSION,
            "术语区内的 `术语 释义…` 段落 → definition（启发式：术语区 + 首词大写形态）",
            "definition",
            "mapped",
            False,
            "match_definition_paragraph",
        ),
        Rule(
            "F01.toc.entry",
            RULE_SET_VERSION,
            "目录区（Contents/Table of Contents/List of Tables|Figures 等）内的块 → 兜底 note（不计覆盖率）",
            "note",
            "fallback",
            False,
            "match_toc_line",
        ),
        Rule(
            "F02.html.residue",
            RULE_SET_VERSION,
            "块级 HTML 残余（转换残留的非表格/非图片标签块）→ 兜底 note(format=html，不计覆盖率）",
            "note",
            "fallback",
            False,
            "match_block_html",
        ),
        Rule(
            "F03.unmapped.catch-all",
            RULE_SET_VERSION,
            "未匹配任何形态规则的块 → 兜底 note（零静默丢弃的最后一道闸）",
            "note",
            "fallback",
            False,
            "match_never",
        ),
    )
}
"""全部规则（key = `rule_id`）。"""

RULES_BY_KIND: dict[str, str] = {
    HEADING: "R01.heading.clause",
    TABLE_HTML: "R03.table.html",
    TABLE_MARKDOWN: "R04.table.markdown",
    CODE: "R05.code.fenced",
    FIGURE: "R06.figure.image",
    LIST: "R08.list.note",
    PARAGRAPH: "R11.paragraph.clause-body",
    HTML_RESIDUE: "F02.html.residue",
}
"""块形态 → 默认规则（目录区/术语区的上下文覆盖见 :data:`TOC_RULE_ID`/:data:`DEFINITION_RULE_ID`）。"""

TOC_RULE_ID: Final = "F01.toc.entry"
"""目录区覆盖规则（上下文口径：只在 TOC 区内的非标题块生效）。"""

DEFINITION_RULE_ID: Final = "R02.heading.definition"
DEFINITION_BODY_RULE_ID: Final = "R12.paragraph.definition"

TOC_CONTINUATION_RATIO: Final = 0.6
"""目录区延续判据：标题后首块区域内 TOC 形态行占比 ≥ 该值时仍在目录区（页眉伪标题场景）。"""


# ── 匹配器（纯函数；形态判定）────────────────────────────────────────────

_HEADING_RE = re.compile(r"^(?P<hashes>#{1,6})[ \t]+(?P<title>.*?)[ \t]*$")
_FENCE_RE = re.compile(r"^[ \t]*(?P<fence>```+|~~~+)[ \t]*(?P<lang>[A-Za-z0-9_+#.-]*)[ \t]*$")
_HTML_TABLE_OPEN_RE = re.compile(r"<table\b", re.IGNORECASE)
_HTML_TABLE_CLOSE_RE = re.compile(r"</table\s*>", re.IGNORECASE)
_MD_TABLE_DELIM_RE = re.compile(r"^[ \t]*\|?(?:[ \t]*:?-{3,}:?[ \t]*\|)+[ \t]*:?-{3,}:?[ \t]*\|?[ \t]*$")
_MD_IMAGE_RE = re.compile(
    r"^!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)(?:[ \t]+\"[^\"]*\")?\)[ \t]*$"
)
_HTML_IMAGE_RE = re.compile(
    r"^<img\b(?=[^>]*\bsrc\s*=)[^>]*\bsrc\s*=\s*[\"']?(?P<src>[^\"'\s>]+)[\"']?[^>]*>[ \t]*$",
    re.IGNORECASE,
)
_LIST_ITEM_RE = re.compile(r"^(?P<indent>[ \t]*)(?:[-*+]|\d{1,9}[.)])[ \t]+(?P<body>\S.*)$")
_BLOCK_HTML_RE = re.compile(
    r"^[ \t]*</?(?P<tag>"
    r"div|p|ul|ol|li|dl|dt|dd|hr|center|font|pre|blockquote|section|article|"
    r"h[1-6]|caption|colgroup|col|thead|tbody|tfoot|tr|td|th|caption|figure"
    r")\b[^>]*>",
    re.IGNORECASE,
)
_TOC_MARKER_RE = re.compile(
    r"^(?:table of contents|contents|table of figures|table of tables|"
    r"list of tables|list of figures|list of figures and tables|figures|tables|index)\b",
    re.IGNORECASE,
)
_TOC_LINE_RE = re.compile(r"\.{2,}|\s\.\s?\d{1,4}[ \t]*$")
_TOC_NUMBERED_RE = re.compile(
    r"^[ \t]*(?:\d+(?:\.\d+)*|[A-Z](?:\.\d+)*|Figure\s+[\dA-Z][\w.\-]*|Table\s+[\dA-Z][\w.\-]*|"
    r"Chapter\s+\d+|Appendix\s+[A-Z]|Annex\s+[A-Z]|Part\s+[A-Z])\b.*?[\s.]\d{1,4}[ \t]*$"
)
_GLOSSARY_MARKER_RE = re.compile(
    r"^(?:glossary|terms and acronyms|terms and definitions|terms|definitions|"
    r"abbreviations|acronyms|definitions and abbreviations|list of abbreviations|"
    r"terminology)\b",
    re.IGNORECASE,
)
_GLOSSARY_EXIT_RE = re.compile(
    r"^(?:contents|table of contents|list of tables|list of figures|figures|tables|preface|index|"
    r"revision history|change history|introduction|notice|disclaimer|legal|about|using this|"
    r"intended audience|feedback|objective|overview|standard improvement form|acknowledge?ments|"
    r"copyright|proprietary)\b",
    re.IGNORECASE,
)
_CROSS_REF_RE = re.compile(
    r"^(?:See|Refer to|see|refer to)\b[^.!?]{0,160}?\b"
    r"(?:Section|Chapter|Clause|Table|Figure|Annex|Appendix|Part|sub-section|subsection|"
    r"specification|document)\b",
)
_EXAMPLE_RE = re.compile(r"^(?:Example|EXAMPLE|Examples)\b\s*(?:\d+(?:\.\d+)*)?\s*[:.—–-]?\s*\S", re.UNICODE)
_DEFINITION_TERM_RE = re.compile(r"^(?P<term>[A-Z][\w./()+-]*(?:[ \t]+[A-Z][\w./()+-]*){0,3})[ \t]+(?P<body>[A-Z]\S.*)$")

_CROSS_REF_MAX_CHARS: Final = 300
_DEFINITION_MAX_TERM_CHARS: Final = 60
_DEFINITION_MIN_BODY_CHARS: Final = 20


def clean_text(raw: str) -> str:
    """形态判定用的归一文本：去 HTML 标签（复用 :func:`agenticdocer.model.html_to_text`）+ 折空白。

    只用于**匹配与锚标题**，不改写块原文（P4 零改写约束的是 `content`）。
    """
    return html_to_text(raw).strip()


def match_heading(line: str) -> re.Match[str] | None:
    """ATX 标题（`#`…`######` + 空格 + 标题）。"""
    return _HEADING_RE.match(line)


def match_fence(line: str) -> re.Match[str] | None:
    """围栏代码块起始行（``` / ~~~，可带语言标识）。"""
    return _FENCE_RE.match(line)


def match_html_table_open(line: str) -> re.Match[str] | None:
    """HTML 表格起始（`<table…`）。"""
    return _HTML_TABLE_OPEN_RE.search(line)


def match_html_table_close(line: str) -> re.Match[str] | None:
    """HTML 表格闭合（`</table>`）。"""
    return _HTML_TABLE_CLOSE_RE.search(line)


def match_md_table(lines: Sequence[str], index: int = 0) -> re.Match[str] | None:
    """markdown 管道表格：本行含 `|` 且下一行是分隔行（`|---|:--:|`）。"""
    if index + 1 >= len(lines):
        return None
    if "|" not in lines[index]:
        return None
    return _MD_TABLE_DELIM_RE.match(lines[index + 1])


def match_md_image(line: str) -> re.Match[str] | None:
    """独占一行的 markdown 图片引用。"""
    return _MD_IMAGE_RE.match(line)


def match_html_image(line: str) -> re.Match[str] | None:
    """独占一行的 HTML `<img src=…>`。"""
    return _HTML_IMAGE_RE.match(line)


def match_list_item(line: str) -> re.Match[str] | None:
    """列表项（`-`/`*`/`+`/`1.`/`1)` 起首）。"""
    return _LIST_ITEM_RE.match(line)


def match_block_html(line: str) -> re.Match[str] | None:
    """块级 HTML 标签起首的行（内联标签如 `<sup>` 不属此列——随段落原样保留）。"""
    return _BLOCK_HTML_RE.match(line)


def match_toc_marker(title: str) -> re.Match[str] | None:
    """目录类标题（Contents / Table of Figures / List of Tables / Index …）。"""
    return _TOC_MARKER_RE.match(clean_text(title))


def match_toc_line(line: str) -> re.Match[str] | None:
    """目录条目行（点引导或「编号/图表题 + 页码」收尾）。"""
    stripped = line.rstrip()
    if not stripped.strip():
        return None
    return _TOC_LINE_RE.search(stripped) or _TOC_NUMBERED_RE.match(stripped)


def match_glossary_marker(title: str) -> re.Match[str] | None:
    """术语区标题（Glossary / Terms and Acronyms / Abbreviations …）。"""
    return _GLOSSARY_MARKER_RE.match(clean_text(title))


def match_glossary_exit(title: str) -> re.Match[str] | None:
    """术语区终止标题（Preface / Contents / Introduction / Index …）。"""
    return _GLOSSARY_EXIT_RE.match(clean_text(title))


def match_cross_ref(text: str) -> re.Match[str] | None:
    """整块即交叉引用（短、以 See/Refer to 起首、含 Section/Table/Figure 等引用对象）。"""
    flattened = " ".join(text.split())
    if len(flattened) > _CROSS_REF_MAX_CHARS:
        return None
    return _CROSS_REF_RE.match(flattened)


def match_example(text: str) -> re.Match[str] | None:
    """`Example …` 起首的块。"""
    return _EXAMPLE_RE.match(" ".join(text.split()))


def match_definition_paragraph(text: str) -> re.Match[str] | None:
    """术语区内 `术语 释义…` 段落（术语 ≤ 4 词、≤60 字符；释义以大写字母起首）。

    语料实测（AMBA `## Glossary` 区）：词条是「术语 + 空格 + 释义」的段落（如
    `AHB An AMBA bus protocol that defines…`）。故要求术语首词不在
    :data:`DEFINITION_STOPWORDS`（虚词/连接词），避免把普通句子首词误当术语。
    """
    flattened = " ".join(text.split())
    match = _DEFINITION_TERM_RE.match(flattened)
    if match is None:
        return None
    term = match.group("term")
    if len(term) > _DEFINITION_MAX_TERM_CHARS:
        return None
    if term.split(" ", 1)[0].casefold() in DEFINITION_STOPWORDS:
        return None
    if len(match.group("body")) < _DEFINITION_MIN_BODY_CHARS:
        return None
    return match


def count_html_table_markers(line: str) -> tuple[int, int]:
    """本行的 `(<table` 个数, `</table>` 个数)——表格块的嵌套闭合判定。"""
    return len(_HTML_TABLE_OPEN_RE.findall(line)), len(_HTML_TABLE_CLOSE_RE.findall(line))


def match_never(line: str) -> None:
    """兜底规则的匹配器：永不命中（仅由 `classify()` 在无规则可命中时指派）。"""
    return None


MATCHERS: dict[str, Callable[..., Any]] = {
    "match_heading": match_heading,
    "match_fence": match_fence,
    "match_html_table_open": match_html_table_open,
    "match_html_table_close": match_html_table_close,
    "match_md_table": match_md_table,
    "match_md_image": match_md_image,
    "match_html_image": match_html_image,
    "match_list_item": match_list_item,
    "match_block_html": match_block_html,
    "match_toc_marker": match_toc_marker,
    "match_toc_line": match_toc_line,
    "match_glossary_marker": match_glossary_marker,
    "match_glossary_exit": match_glossary_exit,
    "match_cross_ref": match_cross_ref,
    "match_example": match_example,
    "match_definition_paragraph": match_definition_paragraph,
    "match_never": match_never,
    "match_paragraph": match_never,  # 段落是「其余皆非」的补集，见 parser.scan_blocks
}
"""匹配器登记表：`Rule.matcher` 必须命中此表（规则库自证，测试断言）。"""


_NUMBERING_RE = re.compile(
    r"^(?P<num>\d+(?:\.\d+)*|[A-Z]\d+(?:\.\d+)*|[A-Z]\.\d+(?:\.\d+)*)\.?(?=[ \t])[ \t]+(?P<rest>\S.*)$"
)
_WORD_NUMBERING_RE = re.compile(
    r"^(?P<word>Chapter|Appendix|Annex|Part|Section|Clause)[ \t]+(?P<num>[A-Z]|\d+(?:\.\d+)*)\b"
    r"[ \t]*[.:—–-]?[ \t]*(?P<rest>.*)$",
    re.IGNORECASE,
)


def parse_numbering(title: str) -> tuple[tuple[str, ...], str] | None:
    """标题编号 → ``(章节号路径, 标题余下文本)``；无编号返回 ``None``。

    语料实测（ADR-006）：标题层级在**编号**里而非 `#` 个数里（`##` 占 99.8%），
    编号形态含 ``1.3.2``、``A5.3.6``、``A.1``、``Appendix B``、``Annex A``、``Chapter 10``。
    形态判定用 :func:`clean_text` 去标签后的文本（CXL 标题含 `<sub>` 残片）。
    """
    cleaned = clean_text(title)
    if not cleaned:
        return None
    match = _NUMBERING_RE.match(cleaned)
    if match is not None:
        return tuple(match.group("num").split(".")), match.group("rest").strip()
    match = _WORD_NUMBERING_RE.match(cleaned)
    if match is not None:
        return (match.group("num"),), match.group("rest").strip()
    return None
