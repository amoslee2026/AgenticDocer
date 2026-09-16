"""M04 渲染引擎（ADR-004：程序化渲染管线，不使用模板）。

渲染契约（P4 + §3 M04，即 M03 与 M04 之间的跨模块约定）：

1. ``content.fragment`` = 块的**源标记逐字节原文**（含标题行的 ``##``、含整个
   ``<table>…</table>`` 片段）。有 fragment 的节点**原样输出**——HTML 片段零改写（P4）；
2. 无 fragment 才按 ``atom_type`` 合成（``code`` / ``figure*`` / ``cross_ref`` / 表格类，
   见 :func:`_synthesize`）；
3. 块边界：节点之间**单个空行**（``\\n\\n``），文档以**单个 ``\\n``** 结尾；
4. **唯一例外**（P4）：图片 ``src`` 重写为 ``assets/<sha256>.<ext>`` 相对路径
   （含 HTML 片段内的 ``<img>``，A7），资产字节由 CAS 导出到 ``<out_dir>/assets/``
   （REQ-M04-F03）。解析不出 asset_id 的引用（外链、未入库相对路径）**原样保留**并计入
   ``unresolved``（日志 WARN）——库内引用的权威形态由 M03 ``assets_sync`` 保证；
5. frontmatter 由 ``docs.meta`` 按 **C5 十七字段**回写（§6 映射），``meta`` 其余键按名序追加
   （「meta 全量保真」）；
6. ``format='html'`` 的 ``<table>`` 片段除图片 ``src`` 外**逐字节不变**（P4 硬约束），
   这使 ``normalize_markdown(产物) == normalize_markdown(源)``（REQ-M04-F01(b)）成立。

产物落盘（REQ-M04-F03）：整档 ``<out_dir>/<doc_id>.md``；章节 ``<out_dir>/sections/<anchor>.md``
（章节产物**不带 frontmatter**——它是 WebUI/M08 按需加载的片段，frontmatter 属文档级）；
资产 ``<out_dir>/assets/<sha256>.<ext>``。``out_dir`` 默认取 ``RENDER_OUT_DIR``（§5）。

接口为 ``async``：存储层（M02）全异步，渲染需读节点树与资产行。
"""

from __future__ import annotations

import asyncio
import os
import re
import shutil
from collections.abc import Iterable, Iterator, Mapping, Sequence
from pathlib import Path
from typing import Any, Final
from uuid import UUID

import yaml

from agenticdocer.model import C5_META_FIELDS, TABLE_ATOMS, Doc, Node, RenderResult
from agenticdocer.observability import get_logger
from agenticdocer.store import ASSET_REF_PATTERN, NotFoundError, Storage, get_storage

from .editable import REGISTER_FIELD_COLUMNS, TableGrid, build_table_fragment
from .sections import section_subtree

__all__ = [
    "DEFAULT_RENDER_OUT_DIR",
    "body_text",
    "document_frontmatter",
    "frontmatter_text",
    "iter_image_srcs",
    "node_block_text",
    "render_document",
    "render_out_dir",
    "render_section",
    "rewrite_image_srcs",
]

log = get_logger("m04.renderer")

_REPO_ROOT: Final = Path(__file__).resolve().parents[3]
"""``src/agenticdocer/render/renderer.py`` → 仓库根。"""

DEFAULT_RENDER_OUT_DIR: Final = _REPO_ROOT / "build" / "rendered"
"""``build/rendered/``（REQ-M04-F03：产物不入 ``spec/``、不被 ingest 扫描）。"""

_HASH_TOKEN: Final = re.compile(r"([0-9a-f]{64})(?:\.([A-Za-z0-9]+))?")
"""从任意引用路径中抽 ``asset_id``（+可选扩展名）：``images/<sha>.jpg``、``assets/<sha>.png``、裸 sha。"""

_MD_IMAGE: Final = re.compile(r"(!\[[^\]]*\]\(\s*)([^)\s<>]+)")
_HTML_IMAGE: Final = re.compile(
    r"(<img\b[^>]*?\bsrc\s*=\s*)(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))",
    re.IGNORECASE,
)

_UNSAFE_NAME: Final = re.compile(r"[\\/:*\?\"<>|\x00]")


# ── 位置与命名 ────────────────────────────────────────────────────────────


def render_out_dir(out_dir: str | Path | None = None) -> Path:
    """渲染产物根目录：显式入参 → ``RENDER_OUT_DIR`` → 仓库 ``build/rendered``（§5）。"""
    if out_dir is not None:
        return Path(out_dir)
    return Path(os.environ.get("RENDER_OUT_DIR", DEFAULT_RENDER_OUT_DIR))


def _safe_name(value: str) -> str:
    """文件名安全化（锚含 ``#``/``·``，doc_id 可能含 ``:``；仅替换文件系统分隔类字符）。"""
    return _UNSAFE_NAME.sub("_", str(value)) or "unnamed"


# ── 单节点渲染（纯函数；ADR-004）──────────────────────────────────────────


def node_block_text(node: Node, image_map: Mapping[str, str] | None = None) -> str:
    """节点 → Markdown 块文本（**唯一节点渲染口径**；``normalize`` 的库侧镜像亦经此）。

    ``image_map`` 给出 ``src → 重写后 src`` 时执行图片重写（P4 唯一例外）；缺省则纯直通。
    """
    content = node.content or {}
    fragment = content.get("fragment")
    text = fragment if isinstance(fragment, str) and fragment.strip() else _synthesize(node)
    if image_map:
        text = rewrite_image_srcs(text, image_map)
    return text.strip("\n")


def _synthesize(node: Node) -> str:
    """无 fragment 的节点按 ``atom_type`` 合成 Markdown（结构化字段 → 源标记）。"""
    content = node.content or {}
    text = str(content.get("text") or "").strip()
    if node.level is not None:
        return f"{'#' * int(node.level)} {text}".rstrip()
    atom_type = node.atom_type
    if atom_type == "code":
        language = str(content.get("language") or "").strip()
        return f"```{language}\n{text}\n```"
    if atom_type in TABLE_ATOMS:
        if atom_type == "table.register_field":
            return build_table_fragment(_register_grid(content))
        return build_table_fragment(TableGrid(rows=[], header=False))
    if atom_type == "figure":
        return _figure_block(content, text)
    if atom_type == "figure.state_machine":
        return _state_machine_block(content)
    if atom_type == "cross_ref":
        return f"[{text}]({_cross_ref_target(content)})"
    return text


def _register_grid(content: Mapping[str, Any]) -> TableGrid:
    fields = [item for item in content.get("fields") or () if isinstance(item, Mapping)]
    rows = [
        [str(item.get(name) or "") for name in REGISTER_FIELD_COLUMNS] for item in fields
    ]
    register_name = content.get("register")
    return TableGrid(
        rows=rows,
        header=False,  # 字段行即数据行，合成表格无表头行
        header_names=list(REGISTER_FIELD_COLUMNS),
        register_name=str(register_name) if register_name else None,
    )


def _figure_block(content: Mapping[str, Any], text: str) -> str:
    alt = str(content.get("alt") or "").strip()
    asset_ref = str(content.get("asset_ref") or "").strip()
    caption = str(content.get("caption") or "").strip()
    if not asset_ref:
        line = f"![{alt}]({text})" if text else f"![{alt}]()"
        return f"{line}\n\n{caption}" if caption else line
    src = f"assets/{asset_ref}"
    line = f"![{alt}]({src})"
    return f"{line}\n\n{caption}" if caption else line


def _state_machine_block(content: Mapping[str, Any]) -> str:
    mermaid = str(content.get("mermaid") or "").strip()
    if mermaid:
        return f"```mermaid\n{mermaid}\n```"
    lines = ["```mermaid", "stateDiagram-v2"]
    for item in content.get("transitions") or ():
        if not isinstance(item, Mapping):
            continue
        arrow = f"  {item.get('from')} --> {item.get('to')}"
        if item.get("condition"):
            arrow += f" : {item['condition']}"
        elif item.get("event"):
            arrow += f" : {item['event']}"
        lines.append(arrow)
    lines.append("```")
    return "\n".join(lines)


def _cross_ref_target(content: Mapping[str, Any]) -> str:
    anchor = str(content.get("target_anchor") or "").strip()
    if anchor:
        return f"#{anchor}"
    node_id = str(content.get("target_node_id") or "").strip()
    if node_id:
        return f"#{node_id}"
    target = str(content.get("target_doc_id") or "").strip()
    return target[4:] if target.startswith("EXT:") else target


def body_text(nodes: Sequence[Node], image_map: Mapping[str, str] | None = None) -> str:
    """节点序列 → Markdown 正文（ordinal 序由调用方保证；块间单个空行）。"""
    return "\n\n".join(
        block
        for block in (node_block_text(node, image_map) for node in nodes)
        if block
    )


# ── 图片引用（P4 唯一例外；收集与重写共用同一对正则）──────────────────────


def iter_image_srcs(text: str) -> Iterator[str]:
    """文本中的所有图片引用：Markdown ``![](src)`` + HTML ``<img src=…>``（A7）。"""
    if not text:
        return
    for match in _MD_IMAGE.finditer(text):
        yield match.group(2)
    for match in _HTML_IMAGE.finditer(text):
        yield _html_img_src(match)


def _html_img_src(match: re.Match[str]) -> str:
    return next(group for group in match.groups()[1:] if group is not None)


def rewrite_image_srcs(text: str, mapping: Mapping[str, str]) -> str:
    """按 ``mapping`` 重写图片 ``src``（片段其余部分**逐字节不变**）。"""

    def _md(match: re.Match[str]) -> str:
        new = mapping.get(match.group(2))
        return match.group(0) if new is None else f"{match.group(1)}{new}"

    def _html(match: re.Match[str]) -> str:
        new = mapping.get(_html_img_src(match))
        if new is None:
            return match.group(0)
        prefix = match.group(1)
        if match.group(2) is not None:
            return f'{prefix}"{new}"'
        if match.group(3) is not None:
            return f"{prefix}'{new}'"
        return f"{prefix}{new}"

    return _HTML_IMAGE.sub(_html, _MD_IMAGE.sub(_md, text))


def collect_image_srcs(texts: Iterable[str]) -> list[str]:
    """按出现序去重的图片 ``src`` 清单（供一次性解析/导出，避免重复 IO）。"""
    seen: dict[str, None] = {}
    for text in texts:
        for src in iter_image_srcs(text):
            seen.setdefault(src, None)
    return list(seen)


async def _resolve_and_export(
    storage: Storage,
    srcs: Sequence[str],
    out_dir: Path,
) -> tuple[dict[str, str], int, list[str]]:
    """图片 ``src`` → 产物相对路径；并把资产字节从 CAS 导出到 ``<out_dir>/assets/``。

    返回 ``(src→新 src 映射, 导出资产数, 未能解析的 src 清单)``。无法解析的引用原样保留
    （P4 直通），交由 M09B ``assets_missing`` 与 M03 ``assets_sync`` 处置。
    """
    mapping: dict[str, str] = {}
    exported: dict[str, str] = {}
    unresolved: list[str] = []
    for src in srcs:
        asset_id, ext = await _identify_asset(storage, src)
        if asset_id is None:
            unresolved.append(src)
            continue
        if asset_id not in exported:
            try:
                source_path = await storage.get_asset_path(asset_id)
            except NotFoundError:
                unresolved.append(src)
                continue
            suffix = ext or source_path.suffix.lstrip(".")
            name = f"{asset_id}.{suffix}" if suffix else asset_id
            destination = out_dir / "assets" / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            await asyncio.to_thread(shutil.copyfile, source_path, destination)
            exported[asset_id] = name
        mapping[src] = f"assets/{exported[asset_id]}"
    if unresolved:
        log.warn(
            "image refs unresolved (kept verbatim)",
            count=len(unresolved),
            sample=unresolved[:3],
        )
    return mapping, len(exported), unresolved


async def _identify_asset(storage: Storage, src: str) -> tuple[str | None, str | None]:
    """引用 → ``(asset_id, ext)``；解析不出 ``asset_id`` 时返回 ``(None, None)``。

    库内形态（``assets/<sha>.<ext>``，``ASSET_REF_PATTERN``）优先；其次从任意路径抽
    ``<sha256>``（``images/<sha>.jpg``、裸 sha），扩展名缺失时回查 ``assets.path``。
    """
    match = ASSET_REF_PATTERN.search(src)
    if match:
        return match.group(1), match.group(2).lower()
    token = _HASH_TOKEN.search(src)
    if token is None:
        return None, None
    asset_id, ext = token.group(1), (token.group(2) or "").lower() or None
    if ext is None:
        ext = await _asset_extension(storage, asset_id)
    return asset_id, ext


async def _asset_extension(storage: Storage, asset_id: str) -> str | None:
    try:
        asset = await storage.get_asset(asset_id)
    except NotFoundError:
        return None
    return Path(asset.path).suffix.lstrip(".").lower() or None


# ── frontmatter（§6 C5 十七字段）─────────────────────────────────────────


def document_frontmatter(doc: Doc) -> dict[str, Any]:
    """``Doc`` → frontmatter 映射（C5 十七字段定序 + ``meta`` 其余键按名序追加）。"""
    meta = dict(doc.meta or {})
    resolved: dict[str, Any] = {}
    for name in C5_META_FIELDS:
        value = _frontmatter_value(doc, meta, name)
        if value is None or value == "":
            continue
        resolved[name] = value
    for name in sorted(meta):
        if name not in resolved and meta[name] not in (None, ""):
            resolved[name] = meta[name]
    return resolved


def _frontmatter_value(doc: Doc, meta: Mapping[str, Any], name: str) -> Any:
    if name == "title":
        return doc.title
    if name == "spec_id":
        return doc.doc_id
    if name == "spec_type":
        return doc.doc_type
    if name == "status":
        return meta.get("status", doc.status)
    if name == "source":
        return meta.get("source") or doc.source_ref
    return meta.get(name)


def frontmatter_text(doc: Doc) -> str:
    """frontmatter 序列化（``---\\n<yaml>---\\n``；宽度放开以免长值折行）。"""
    data = document_frontmatter(doc)
    dump = yaml.safe_dump(
        data,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=4096,
    )
    return f"---\n{dump}---\n"


def _assemble(doc: Doc, blocks: Sequence[str], mapping: Mapping[str, str]) -> str:
    body = "\n\n".join(
        rewrite_image_srcs(block, mapping) for block in blocks if block
    )
    head = frontmatter_text(doc)
    return f"{head}\n{body}\n" if body else f"{head}\n"


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


# ── 对外渲染入口 ─────────────────────────────────────────────────────────


async def render_document(
    doc_id: str,
    out_dir: str | Path | None = None,
    *,
    storage: Storage | None = None,
) -> RenderResult:
    """整档渲染：节点树（``status='active'``、``ordinal`` 序）→ Markdown。

    产物 ``<out_dir>/<doc_id>.md``（frontmatter + 正文）；图片重写并导出 ``<out_dir>/assets/``。

    :raises NotFoundError: 文档不存在（404）。
    """
    store = storage or get_storage()
    target = render_out_dir(out_dir)
    scoped = log.child(doc_id=doc_id)
    with scoped.timer("render_document"):
        doc = await store.get_doc(doc_id)
        nodes = await store.get_doc_nodes(doc_id)
        blocks = [node_block_text(node) for node in nodes]
        mapping, exported, unresolved = await _resolve_and_export(
            store, collect_image_srcs(blocks), target
        )
        text = _assemble(doc, blocks, mapping)
        path = target / f"{_safe_name(doc.doc_id)}.md"
        await asyncio.to_thread(_write_text, path, text)
    scoped.info(
        "document rendered",
        nodes=len(nodes),
        images_rewritten=len(mapping),
        assets_exported=exported,
        unresolved=len(unresolved),
        out_path=str(path),
    )
    return RenderResult(doc_id=doc.doc_id, out_path=str(path), assets_exported=exported)


async def render_section(
    doc_id: str,
    section_node_id: UUID | str,
    out_dir: str | Path | None = None,
    *,
    storage: Storage | None = None,
) -> RenderResult:
    """章节渲染（B10）：``section_node_id`` 及其后代（``ordinal`` 序、``status='active'``）→ Markdown。

    产物 ``<out_dir>/sections/<anchor>.md``（**不带 frontmatter**；图片规则与整档一致）。
    仅遍历该章节子树（不渲染其余节点），指标：单章节 <1s（§1.4）。

    :raises NotFoundError: 章节节点不在该文档的 active 节点中（404）。
    """
    store = storage or get_storage()
    target = render_out_dir(out_dir)
    scoped = log.child(doc_id=doc_id, section=str(section_node_id))
    with scoped.timer("render_section"):
        nodes = await store.get_doc_nodes(doc_id)
        subtree = section_subtree(nodes, section_node_id)
        blocks = [node_block_text(node) for node in subtree]
        mapping, exported, unresolved = await _resolve_and_export(
            store, collect_image_srcs(blocks), target
        )
        text = "\n\n".join(rewrite_image_srcs(block, mapping) for block in blocks if block)
        path = target / "sections" / f"{_safe_name(subtree[0].anchor)}.md"
        await asyncio.to_thread(_write_text, path, f"{text}\n")
    scoped.info(
        "section rendered",
        nodes=len(subtree),
        images_rewritten=len(mapping),
        assets_exported=exported,
        unresolved=len(unresolved),
        out_path=str(path),
    )
    return RenderResult(doc_id=doc_id, out_path=str(path), assets_exported=exported)
