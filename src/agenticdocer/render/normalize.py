"""M04 规范化表示（REQ-M04-F02 / P5 口径唯一）——往返判据的唯一比较函数。

判据（REQ-M04-F01，**两式并列**）：

(a) **解析保真**：``await normalize(doc_id) == normalize_markdown(src)``
    库侧特征直接取自节点（``content.fragment`` 原样拼接，**不经渲染**）：验证「导入未丢结构」。
    其盲区正是只在渲染层才会被破坏的对象——frontmatter 回写、图片 src 重写、块边界拼接；
(b) **渲染保真**：``normalize_markdown(产物文件) == normalize_markdown(src)``
    渲染产物与源逐特征等价：覆盖 HTML 片段直通（P4）、内联标记与块边界。

口径（P5 单一实现 = :func:`extract_features`；源侧与库侧共用）：

* ``headings``：ATX 标题（``#`` 个数 + 文本），**不**取 ``node.level``（M03 的 level 是标题
  编号深度，与源码书写形态不同；本判据要比较的是「写出来的层级」，故两侧都按 ATX 解析）。
  文本经 ``normalize_body`` 归一（NFKC + 折叠空白）。
* ``tables``：HTML ``<table>`` 与 GFM 管道表 都收；单元格文本经 M01 ``html_to_text`` +
  ``normalize_body``（与 ``editable.table_cells`` 同源，P5）。``cols`` = 各行单元格数最大值
  （``colspan`` 不展开；行列断言由 M09B 以 ``content.meta`` 为准）。
* ``code_blocks``：围栏内原文（不含围栏行与语言标识——围栏语言是渲染期合成属性，
  见 ``renderer._synthesize``；原文片段的语言标识随 ``fragment`` 直通，不在本判据口径内）。
* ``images``：**asset_id（sha256）集合**——从引用中抽出 ``<sha256>``（重写前的哈希路径口径）。
  扩展名由渲染期按 ``assets.mime`` 决定，故不入判据（评审 A7-3「口径定为 asset_id 集合」）：
  源 ``![](images/<sha>.jpg)``、库内 figure 合成的 ``assets/<sha>``、产物 ``assets/<sha>.jpg``
  三者判为同一引用。非哈希引用（外链 URL、无法解析的相对路径）原样入集。
* ``lists``：连续的列表项行各成一项组成一个列表；被非列表行/空行隔断即成两个列表
  （缩进续行折入前一项文本，不建模嵌套层级）。
* ``inline_markers``：出现过的**内联标记种类**（排序去重），非出现次数。
"""

from __future__ import annotations

import re
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import Any, Final

from agenticdocer.model import Model, Node, html_to_text, normalize_body
from collections.abc import Sequence
from pathlib import Path
from typing import Final

from agenticdocer.model import Model, normalize_body

__all__ = [
    "NormalForm",
    "TableNF",
    "canonical_image_ref",
    "extract_features",
    "normalize",
    "normalize_markdown",
    "read_source",
]

_FRONTMATTER_OPEN: Final = re.compile(r"^---\s*$")
_FRONTMATTER_CLOSE: Final = re.compile(r"^(---|\.\.\.)\s*$")
_FENCE: Final = re.compile(r"^\s*(```+|~~~+)\s*([^\s`]*)")
_ATX: Final = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)(?:\s+#+)?\s*$")
_BULLET: Final = re.compile(r"^(\s*)([-*+]|\d{1,9}[.)])\s+(.*)$")
_CONTINUATION: Final = re.compile(r"^(\s+)(\S.*)$")
_TABLE_OPEN: Final = re.compile(r"<table\b", re.IGNORECASE)
_TABLE_CLOSE: Final = re.compile(r"</table\s*>", re.IGNORECASE)
_PIPE_ROW: Final = re.compile(r"^\s*\|(.+)\|\s*$")
_PIPE_SEPARATOR: Final = re.compile(r"^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$")
_ASSET_ID: Final = re.compile(r"([0-9a-f]{64})")

_INLINE_MARKERS: Final[tuple[tuple[str, re.Pattern[str]], ...]] = (
    ("bold", re.compile(r"\*\*[\s\S]+?\*\*|__[^_]+__")),
    ("italic", re.compile(r"(?<![*\w])\*(?!\s)[^*\n]+\*(?!\*)|(?<![_\w])_(?!\s)[^_\n]+_(?!_)")),
    ("strike", re.compile(r"~~(?!\s)[^~\n]+~~")),
    ("highlight", re.compile(r"==(?!\s)[^=\n]+==")),
    ("inline_code", re.compile(r"`[^`\n]+`")),
    ("comment", re.compile(r"%%[\s\S]+?%%")),
    ("wikilink", re.compile(r"\[\[[^\]\n]+\]\]")),
    ("footnote", re.compile(r"\[\^[^\]\s]+\]")),
    ("callout", re.compile(r"(?m)^\s*>\s*\[![A-Za-z]+\]")),
)


class TableNF(Model):
    """表格规范化表示（``cells`` 为行列文本网格，是判据的实际载荷）。"""

    rows: int
    cols: int
    cells: list[list[str]]


class NormalForm(Model):
    """§3 M04 的规范化表示（REQ-M04-F02）：往返判据的比较对象。"""

    headings: list[tuple[int, str]]
    tables: list[TableNF]
    code_blocks: list[str]
    images: list[str]
    lists: list[list[str]]
    inline_markers: list[str]


def read_source(source: str | Path) -> str:
    """取源文本：``Path``（或指向已存在文件的 ``str``）读文件，其余 ``str`` 视为文本内容。"""
    if isinstance(source, Path):
        return source.read_text(encoding="utf-8")
    if not isinstance(source, str):
        raise TypeError(f"normalize_markdown 只接受 str（文本）或 Path（文件），得到 {type(source)!r}")
    if "\n" not in source and source.strip() and Path(source).is_file():
        return Path(source).read_text(encoding="utf-8")
    return source


def canonical_image_ref(src: str) -> str:
    """图片引用的比较口径：含 ``<sha256>`` → ``assets/<sha256>``；否则原样（折叠空白）。"""
    match = _ASSET_ID.search(src)
    if match:
        return f"assets/{match.group(1)}"
    return normalize_body(src) or src.strip()


def _skip_frontmatter(lines: Sequence[str]) -> int:
    """跳过文档起始的 YAML frontmatter，返回正文首行下标。"""
    if not lines or not _FRONTMATTER_OPEN.match(lines[0]):
        return 0
    for index in range(1, len(lines)):
        if _FRONTMATTER_CLOSE.match(lines[index]):
            return index + 1
    return 0


def _consume_fence(lines: Sequence[str], start: int, marker: str) -> tuple[str, int]:
    """消费围栏代码块，返回 ``(围栏内原文, 下一行下标)``。"""
    body: list[str] = []
    index = start + 1
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith(marker):
            return "\n".join(body), index + 1
        body.append(lines[index])
        index += 1
    return "\n".join(body), index


def _consume_html_table(lines: Sequence[str], start: int) -> tuple[str, int]:
    """消费整个 ``<table>…</table>``（跨行），返回 ``(片段原文, 下一行下标)``。"""
    fragment: list[str] = []
    index = start
    while index < len(lines):
        fragment.append(lines[index])
        if _TABLE_CLOSE.search(lines[index]):
            return "\n".join(fragment), index + 1
        index += 1
    return "\n".join(fragment), index


def _pipe_row(line: str) -> list[str] | None:
    match = _PIPE_ROW.match(line)
    if match is None:
        return None
    return [normalize_body(cell) for cell in match.group(1).split("|")]


def _consume_pipe_table(lines: Sequence[str], start: int) -> tuple[list[list[str]], int]:
    """消费 GFM 管道表（表头 + 分隔行 + 数据行），返回 ``(网格, 下一行下标)``。"""
    header = _pipe_row(lines[start])
    rows: list[list[str]] = [header] if header else []
    index = start + 2
    while index < len(lines):
        row = _pipe_row(lines[index])
        if row is None:
            break
        rows.append(row)
        index += 1
    return rows, index


def _consume_list(lines: Sequence[str], start: int) -> tuple[list[str], int]:
    """消费连续的列表项行（缩进续行折入前一项），返回 ``(项文本, 下一行下标)``。"""
    items: list[str] = []
    index = start
    while index < len(lines):
        match = _BULLET.match(lines[index])
        if match:
            items.append(normalize_body(match.group(3)))
            index += 1
            continue
        continuation = _CONTINUATION.match(lines[index])
        if continuation and items:
            items[-1] = normalize_body(f"{items[-1]} {continuation.group(2)}")
            index += 1
            continue
        break
    return items, index


def _table_nf(cells: Sequence[Sequence[str]]) -> TableNF:
    meta = table_meta(cells)
    return TableNF(
        rows=meta["rows"],
        cols=meta["cols"],
        cells=[list(row) for row in cells],
    )


def _inline_marker_kinds(text: str) -> list[str]:
    return sorted(name for name, pattern in _INLINE_MARKERS if pattern.search(text))


def extract_features(source: str) -> NormalForm:
    """Markdown 文本 → :class:`NormalForm`（**唯一特征提取实现**，源侧/库侧共用）。"""
    lines = source.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    headings: list[tuple[int, str]] = []
    tables: list[TableNF] = []
    code_blocks: list[str] = []
    lists: list[list[str]] = []
    images: set[str] = set()
    marked: list[str] = []

    index = _skip_frontmatter(lines)
    while index < len(lines):
        line = lines[index]
        fence = _FENCE.match(line)
        if fence:
            block, index = _consume_fence(lines, index, fence.group(1)[:3])
            code_blocks.append(block)
            continue
        if _TABLE_OPEN.search(line):
            fragment, index = _consume_html_table(lines, index)
            cells = table_cells(fragment)
            if cells:
                tables.append(_table_nf(cells))
            images.update(iter_image_srcs(fragment))
            marked.append(fragment)
            continue
        heading = _ATX.match(line)
        if heading:
            headings.append((len(heading.group(1)), normalize_body(heading.group(2))))
            marked.append(heading.group(2))
            index += 1
            continue
        if _pipe_row(line) is not None and index + 1 < len(lines) and _PIPE_SEPARATOR.match(
            lines[index + 1]
        ):
            rows, index = _consume_pipe_table(lines, index)
            tables.append(_table_nf(rows))
            marked.append("\n".join(" | ".join(row) for row in rows))
            continue
        if _BULLET.match(line):
            items, index = _consume_list(lines, index)
            lists.append(items)
            marked.append("\n".join(items))
            continue
        images.update(iter_image_srcs(line))
        marked.append(line)
        index += 1

    return NormalForm(
        headings=headings,
        tables=tables,
        code_blocks=code_blocks,
        images=sorted({canonical_image_ref(src) for src in images}),
        lists=lists,
        inline_markers=_inline_marker_kinds("\n".join(marked)),
    )


def normalize_markdown(source: str | Path) -> NormalForm:
    """源侧规范化：Markdown 文本（或文件路径）→ :class:`NormalForm`。"""
    return extract_features(read_source(source))


async def normalize(doc_id: str, *, storage: Storage | None = None) -> NormalForm:
    """库侧规范化：节点树 → :class:`NormalForm`（**不经渲染**，直接镜像 ``fragment``）。

    镜像文本 = 各节点块（``renderer.node_block_text``，无 fragment 者按原子合成）以空行相连——
    与源的块边界一致，但不含 frontmatter、不做图片重写：故它与源相等即「导入未丢结构」，
    而产物层的破坏只能由 :func:`normalize_markdown` 的渲染产物比较（判据 b）捕获。
    """
    store = storage or get_storage()
    nodes = await store.get_doc_nodes(doc_id)
    return extract_features(body_text(nodes))
