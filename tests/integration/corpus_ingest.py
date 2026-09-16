"""真实语料导入替身 + 断言工具（M03 未就绪期的集成测试夹具）。

**M03（``agenticdocer.importer``）尚未交付**，本模块按 M04 渲染契约（见
:mod:`agenticdocer.render.renderer` 模块 docstring）把 ``spec/standards/`` 下的**真实语料**
切成节点：一个空行分隔块 = 一个节点、``content.fragment`` = 源标记逐字节原文、
图片导入期不改写、标题 ``level`` = 编号深度、父链按 level 栈重建。M03 落地后本模块应删除，
改用 ``agenticdocer-import`` 产出真实节点树——测试的两式往返与 P4 逐字节断言不变。

语料路径经 ``AGENTICDOCER_CORPUS`` 覆盖，缺省仓库 ``spec/standards``。
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

import yaml

from agenticdocer.model import (
    DOC_TYPES,
    DocIn,
    NodeIn,
    SectionRef,
    WriteContext,
    assign_anchors,
    derive_text,
    new_uuid7,
)
from agenticdocer.render import table_cells, table_meta
from agenticdocer.store import Storage

CORPUS_ROOT = Path(
    os.environ.get("AGENTICDOCER_CORPUS", Path(__file__).resolve().parents[2] / "spec" / "standards")
)
"""真实语料根目录（默认 ``spec/standards/{pcie,cxl,amba,jedec}``）。"""

CTX = WriteContext(actor="importer", source="importer")

_FENCE = re.compile(r"^\s*(```+|~~~+)\s*([^\s`]*)")
_ATX = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)(?:\s+#+)?\s*$")
_NUMBER = re.compile(r"^(\d+(?:\.\d+)*)(?:[.\s]|$)")
_LETTER_PATH = re.compile(r"^([A-Z](?:\.\d+)+)(?:[.\s]|$)")
_CHAPTER = re.compile(r"^Chapter\s+(\d+)", re.IGNORECASE)
_IMAGE_ONLY = re.compile(r"^!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)\)\s*$")
_ASSET_ID = re.compile(r"([0-9a-f]{64})")
_BULLET = re.compile(r"^\s*([-*+]|\d{1,9}[.)])\s+")
FRONTMATTER_FIELDS = (
    "title",
    "type",
    "purpose",
    "audience",
    "direction",
    "status",
    "version",
    "section_meta",
    "spec_id",
    "spec_type",
    "spec_org",
    "spec_revision",
    "source",
    "converted_by",
    "converted_at",
    "reviewed_by",
    "reviewed_at",
)


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """``(frontmatter dict, 正文)``；无 frontmatter 时返回 ``({}, 原文)``。"""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            meta = yaml.safe_load("\n".join(lines[1:index])) or {}
            return dict(meta), "\n".join(lines[index + 1 :])
    return {}, text


def split_blocks(text: str) -> list[str]:
    """空行分隔块（围栏与 ``<table>…</table>`` 视为不可分割的整体），保留原文。"""
    lines = text.split("\n")
    blocks: list[list[str]] = []
    buffer: list[str] = []
    fence: str | None = None
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if fence is not None:
            buffer.append(line)
            if stripped.startswith(fence):
                fence = None
            index += 1
            continue
        match = _FENCE.match(line)
        if match:
            buffer.append(line)
            fence = match.group(1)[:3]
            index += 1
            continue
        if stripped.startswith("<table"):
            buffer.append(line)
            while "</table>" not in buffer[-1] and index + 1 < len(lines):
                index += 1
                buffer.append(lines[index])
            index += 1
            continue
        if not stripped:
            if buffer:
                blocks.append(buffer)
                buffer = []
            index += 1
            continue
        buffer.append(line)
        index += 1
    if buffer:
        blocks.append(buffer)
    return ["\n".join(block).strip("\n") for block in blocks]


def heading_depth(title: str, fallback_hashes: int) -> tuple[int, tuple[str, ...]]:
    """标题 → ``(编号深度, 章节号路径)``；无编号标题回退 ``#`` 个数（M03 口径）。"""
    number = _NUMBER.match(title)
    if number:
        parts = tuple(number.group(1).split("."))
        return len(parts), parts
    letter = _LETTER_PATH.match(title)
    if letter:
        parts = tuple(letter.group(1).split("."))
        return len(parts), parts
    chapter = _CHAPTER.match(title)
    if chapter:
        return 1, (chapter.group(1),)
    return fallback_hashes, ()


def node_contents(block: str) -> tuple[str, str, dict[str, Any]]:
    """块 → ``(atom_type, format, content)``（含 M03 的 figure/table/code 形态）。"""
    stripped = block.strip()
    if stripped.startswith("<table"):
        content: dict[str, Any] = {
            "fragment": block,
            "meta": table_meta(table_cells(block)),
        }
        content["text"] = derive_text("table", content)
        return "table", "html", content
    fence = _FENCE.match(block)
    if fence:
        body = "\n".join(block.split("\n")[1:-1])
        content = {"fragment": block, "language": fence.group(2), "text": body or stripped}
        return "code", "md", content
    image = _IMAGE_ONLY.match(stripped)
    if image:
        src = image.group("src")
        alt = image.group("alt")
        content = {"text": alt or src, "alt": alt}
        asset_id = _ASSET_ID.search(src)
        if asset_id:
            content["asset_ref"] = asset_id.group(1)
        return "figure", "md", content
    if _BULLET.match(block):
        return "note", "md", {"fragment": block, "text": stripped}
    return "clause", "md", {"fragment": block, "text": stripped}


def blocks_to_nodes(doc_id: str, blocks: list[str]) -> list[NodeIn]:
    """块序列 → 节点序列（ordinal 序；父链按 level 栈重建；锚经 M01 ``assign_anchors``）。"""
    levels: list[int] = []
    paths: list[tuple[str, ...]] = []
    titles: list[str] = []
    parents: list[int | None] = []
    stack: list[tuple[int, int]] = []  # (level, 块下标)

    for index, block in enumerate(blocks):
        heading = _ATX.match(block.split("\n", 1)[0])
        if heading:
            level, path = heading_depth(heading.group(2), len(heading.group(1)))
            title = heading.group(2)
            while stack and stack[-1][0] >= level:
                stack.pop()
            parents.append(stack[-1][1] if stack else None)
            stack.append((level, index))
        else:
            level = 0
            path = paths[stack[-1][1]] if stack else ()
            title = ""
            parents.append(stack[-1][1] if stack else None)
        levels.append(level)
        paths.append(path)
        titles.append(title)

    anchors = assign_anchors(
        doc_id,
        [
            SectionRef(section_path=paths[index], title=titles[index], body_text=blocks[index])
            for index in range(len(blocks))
        ],
    )
    node_ids = [new_uuid7() for _ in blocks]

    nodes: list[NodeIn] = []
    for index, block in enumerate(blocks):
        atom_type, fmt, content = node_contents(block)
        parent_index = parents[index]
        nodes.append(
            NodeIn(
                node_id=node_ids[index],
                doc_id=doc_id,
                atom_type=atom_type,
                format=fmt,
                ordinal=index + 1,
                parent_node_id=node_ids[parent_index] if parent_index is not None else None,
                level=levels[index] or None,
                anchor=anchors[index],
                content=content,
            )
        )
    return nodes


async def ingest_markdown(
    storage: Storage,
    source: Path,
    doc_id: str,
    *,
    window: tuple[int, int] | None = None,
) -> tuple[str, str]:
    """真实语料 → 库（doc + nodes）；返回 ``(doc_id, 用于往返比较的源文本)``。

    ``window``（块下标左闭右开）只入库该窗口，返回的源文本为窗口块的原文拼接
    （= 渲染期的块拼接口径）；``None`` 表示整档，源文本为文件原文（最强证据）。
    """
    raw = source.read_text(encoding="utf-8")
    front, body = split_frontmatter(raw)
    blocks = split_blocks(body)
    if window is not None:
        blocks = blocks[window[0] : window[1]]
        baseline = "\n\n".join(blocks)
    else:
        baseline = body
    meta = {key: value for key, value in front.items() if key in FRONTMATTER_FIELDS}
    meta.pop("title", None)
    meta.pop("spec_id", None)
    meta.pop("spec_type", None)
    doc_type = str(front.get("spec_type") or "standard")
    await storage.upsert_doc(
        DocIn(
            doc_id=doc_id,
            doc_type=doc_type if doc_type in DOC_TYPES else "standard",
            title=str(front.get("title") or source.stem),
            meta=meta,
            source_ref=str(front.get("source") or "") or None,
        ),
        None,
        CTX,
    )
    created: list[Any] = []
    for node in blocks_to_nodes(doc_id, blocks):
        created.append(await storage.upsert_node(node, None, CTX))
    # 第二遍：把父链写回（M03 在 commit 阶段重建 parent，node_id 此时才已知）
    return doc_id, baseline


def window_with_images(blocks: list[str], *, before: int = 12, after: int = 24) -> tuple[int, int]:
    """含 ``<img>`` 的首块的邻域窗口（用于 P4 的 HTML 片段内图片重写证据）。"""
    for index, block in enumerate(blocks):
        if "<img" in block:
            return max(0, index - before), min(len(blocks), index + after)
    raise AssertionError("语料中未找到含 <img> 的块")


__all__ = [
    "CORPUS_ROOT",
    "CTX",
    "FRONTMATTER_FIELDS",
    "blocks_to_nodes",
    "heading_depth",
    "ingest_markdown",
    "node_contents",
    "split_blocks",
    "split_frontmatter",
    "window_with_images",
    "REGISTER_FIELD_COLUMNS",
]
