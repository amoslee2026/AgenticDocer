"""M04 集成测试：**真实语料 × M03 真实导入**的两式往返 + P4 逐字节证据 + 分章节性能。

数据来源一律为 M03 的真实导入路径（`parse_markdown` + `commit_document`），**不使用任何
测试替身解析器**：节点树、锚、父链、`content.fragment` 全部由 M03 产出，M04 只消费。

断言口径（REQ-M04-F01/F03、P4、§1.4）：

1. **(a) 解析保真**：``await normalize(doc_id) == normalize_markdown(src)``（库侧不经渲染）；
2. **(b) 渲染保真**：``normalize_markdown(<产物文件>) == normalize_markdown(src)``；
3. **P4 逐字节**：``format='html'`` 的 ``<table>`` 片段在产物中逐字节出现；含 ``<img>`` 的片段
   在重写前后**除 ``src`` 外**逐字节一致；正文与源逐字节一致（仅文档首尾空行归一——frontmatter
   分隔与文末换行——以及图片引用这一 P4 明示例外）；
4. **frontmatter 回写**：产物 frontmatter 解析回来 == C5 十七字段映射（§6）；
5. **图片重写与导出**：CAS 资产 → ``assets/<asset_id>.<ext>`` 相对路径 + 字节落 ``out_dir/assets/``；
6. **分章节渲染**：只含该子树、耗时 <1s；整档 <3s（最大文档 CXL 3.59MB）。

语料：``spec/standards/amba/IHI0024_AMBA_APB_spec.md``（整档）、
``spec/standards/cxl/CXL_Specification_rev3p2_ver1p0.md``（最大文档；含 ``<img>`` 表格窗口）。
"""

from __future__ import annotations

import os
import re
import time
from pathlib import Path

import pytest
import yaml
from sqlalchemy import text

from agenticdocer.importer import commit_document, parse_markdown
from agenticdocer.model import DocIn, NodeIn, WriteContext, derive_text, new_uuid7
from agenticdocer.render import (
    body_text,
    grid_to_content,
    list_sections,
    normalize,
    normalize_markdown,
    render_document,
    render_section,
    resolve_table_mode,
    section_subtree,
    table_cells,
    table_meta,
    write_table_edit,
)
from agenticdocer.render.editable import TableEdit, TableGrid, parse_table_fragment
from agenticdocer.store import ConflictError, NotFoundError, Storage

pytestmark = pytest.mark.integration

CORPUS = Path(
    os.environ.get("AGENTICDOCER_CORPUS", Path(__file__).resolve().parents[2] / "spec" / "standards")
)
AMBA = CORPUS / "amba" / "IHI0024_AMBA_APB_spec.md"
CXL = CORPUS / "cxl" / "CXL_Specification_rev3p2_ver1p0.md"

DOC_AMBA = "SPEC-STD-AMBA-APB"  # frontmatter spec_id（M03 由 spec_id 定 doc_id）
DOC_CXL_IMG = "SPEC-M04-CXL-IMG"
DOC_XLINK = "SPEC-M04-XLINK"

CTX = WriteContext(actor="importer", source="importer")

_ENTITY_TABLES = ("comments", "refs", "nodes", "docs", "assets")

_WINDOW_FRONTMATTER = """\
---
title: {title}
type: composite
purpose: spec
audience: both
direction: input
status: approved
version: "1.0.0"
section_meta: "@meta"
spec_id: {doc_id}
spec_type: standard
spec_org: M04 fixture
spec_revision: "r0"
source: corpus/01_raw/specifications/m04-window.md
converted_by: mineru
converted_at: 2026-08-31
reviewed_by: lxx
reviewed_at: 2026-08-31
---
"""


# ── 夹具：真实导入 ────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
async def clean_database(storage: Storage) -> None:
    """每个用例前清空实体表（与 M03 集成测试同口径，保证独立起点）。

    ``events`` 对应用角色是 append-only（A15 库层强制），**不可清**——涉及事件的断言一律按增量。
    """
    async with storage.db.transaction() as session:
        for table in _ENTITY_TABLES:
            await session.execute(text(f"DELETE FROM {table}"))


def _require(path: Path) -> None:
    if not path.is_file():
        pytest.skip(f"语料缺失：{path}（设 AGENTICDOCER_CORPUS 指向语料根）")


def _body(source: Path, result) -> str:
    """源文本基线：M03 ``doc_meta['body_start']``（1 基行号）起的正文（去 frontmatter）。"""
    start = int(result.doc_meta["body_start"])
    return "\n".join(source.read_text(encoding="utf-8").split("\n")[start - 1 :])


async def _import(storage: Storage, source: Path) -> tuple[str, str]:
    """真实 M03 导入：``parse_markdown`` + ``commit_document`` → ``(doc_id, 源正文基线)``。"""
    result = parse_markdown(source)
    committed = await commit_document(result, CTX, storage=storage)
    return committed.doc_id, _body(source, result)


def _write_window(tmp_path: Path, name: str, doc_id: str, body: str) -> Path:
    """把真实语料片段写成带 C5 十七字段 frontmatter 的窗口文件（M03 要求 frontmatter 齐备）。"""
    path = tmp_path / f"{name}.md"
    path.write_text(
        _WINDOW_FRONTMATTER.format(title=f"M04 window {name}", doc_id=doc_id) + body,
        encoding="utf-8",
    )
    return path


def _img_table_slice(source: Path) -> str:
    """真实语料中含 ``<img>`` 的 ``<table>`` 整块原文 + 其上方最近的标题行（含标题以满足
    ``doc_type`` 组合规则要求 clause 原子；MARKDOWN 结构全部取自真实语料，不做重解析）。"""
    lines = source.read_text(encoding="utf-8").split("\n")
    img_at = next(index for index, line in enumerate(lines) if "<img" in line)
    table_at = next(index for index in range(img_at, -1, -1) if lines[index].lstrip().startswith("<table"))
    end = next(index for index in range(img_at, len(lines)) if "</table>" in lines[index])
    heading_at = next(
        (index for index in range(table_at - 1, -1, -1) if re.match(r"^\s{0,3}#{1,6}\s", lines[index])),
        None,
    )
    if heading_at is None:
        return "\n".join(lines[table_at : end + 1])
    head = lines[heading_at]
    return "\n".join([head, "", *lines[table_at : end + 1]])


def _table_fragments(nodes) -> list[str]:
    """含 ``<table>`` 的节点片段（语料中表格常与 OCR 残句同块，故按「包含」判定）。"""
    return [
        str(node.content["fragment"])
        for node in nodes
        if node.content.get("fragment") and "<table" in str(node.content["fragment"])
    ]


def _mask_asset_refs(value: str) -> str:
    """图片引用掩码：源 ``images/<sha>.jpg`` 与产物 ``assets/<sha>.<ext>`` 判为同一占位（P4 例外）。"""
    return re.sub(r"(?:images|assets)/[0-9a-f]{64}(?:\.[A-Za-z0-9]+)?", "@@ASSET@@", value)


def _mask_img_src(fragment: str) -> str:
    """把 ``<img src="…">`` 的值替换为占位符（用于「只有 src 变了」的逐字节比较）。"""
    return re.sub(r'(<img\b[^>]*?\bsrc\s*=\s*")[^"]*(")', r"\1@@\2", fragment)


def _retarget_first_img(fragment: str, asset_id: str) -> str:
    """把片段中第一个图片引用的哈希指向 ``asset_id``（其余字节不动；测试夹具用）。"""
    pattern = re.compile(r"(images/)[0-9a-f]{64}(\.[A-Za-z0-9]+)")
    return pattern.sub(lambda m: f"{m.group(1)}{asset_id}{m.group(2)}", fragment, count=1)


def _body_of_product(text: str) -> str:
    """产物正文（去 frontmatter；产物 frontmatter 由 ``docs.meta`` 回写，非源字节）。"""
    if text.startswith("---\n"):
        return text.split("---\n", 2)[2]
    return text


@pytest.fixture
async def amba(storage: Storage) -> tuple[str, str]:
    """整档 AMBA APB（真实导入；doc_id 取自 frontmatter ``spec_id``）。"""
    _require(AMBA)
    return await _import(storage, AMBA)


@pytest.fixture
async def cxl(storage: Storage) -> tuple[str, str]:
    """整档 CXL（**最大文档** 3.59MB；真实导入）。"""
    _require(CXL)
    return await _import(storage, CXL)


@pytest.fixture
async def cxl_img_window(storage: Storage, tmp_path: Path) -> tuple[str, str]:
    """含 ``<img>`` 的 CXL 表格片段窗口（真实导入）。"""
    _require(CXL)
    window = _write_window(tmp_path, "cxl-img", DOC_CXL_IMG, _img_table_slice(CXL))
    return await _import(storage, window)


# ── 两式往返（REQ-M04-F01）──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_real_corpus_two_way_roundtrip(
    amba: tuple[str, str], storage: Storage, tmp_path: Path
) -> None:
    """真实语料整档：判据 (a) 解析保真 + (b) 渲染保真。"""
    doc_id, source = amba
    source_form = normalize_markdown(source)

    # (a) 解析保真——库侧不经渲染
    assert await normalize(doc_id, storage=storage) == source_form

    result = await render_document(doc_id, tmp_path / "rendered", storage=storage)
    product = Path(result.out_path)
    assert product.is_file()

    # (b) 渲染保真
    assert normalize_markdown(product) == source_form

    # 语料覆盖面自检（防止静默空跑）
    assert len(source_form.headings) == 50
    assert len(source_form.tables) == 7
    assert len(source_form.images) == 8
    assert len(source_form.lists) >= 5


@pytest.mark.asyncio
async def test_two_way_roundtrip_on_largest_document(
    cxl: tuple[str, str], storage: Storage, tmp_path: Path
) -> None:
    """最大文档（CXL 3.59MB）两式往返——真实导入产出的真实节点树。"""
    doc_id, source = cxl
    source_form = normalize_markdown(source)
    assert len(source_form.tables) == 1243

    assert await normalize(doc_id, storage=storage) == source_form
    result = await render_document(doc_id, tmp_path / "rendered", storage=storage)
    product = Path(result.out_path).read_text(encoding="utf-8")
    assert normalize_markdown(Path(result.out_path)) == source_form
    # 逐节点字节覆盖：4,822 个节点的渲染文本全部逐字节出现在产物中（零改写、零转义）
    _assert_node_blocks_verbatim(await storage.get_doc_nodes(doc_id), product)


# ── P4 逐字节证据 ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_html_table_fragments_are_byte_identical(
    amba: tuple[str, str], storage: Storage, tmp_path: Path
) -> None:
    """P4 硬证据：真实语料的 HTML ``<table>`` 片段在产物中逐字节出现。"""
    doc_id, source = amba
    result = await render_document(doc_id, tmp_path / "rendered", storage=storage)
    product = Path(result.out_path).read_text(encoding="utf-8")

    fragments = _table_fragments(await storage.get_doc_nodes(doc_id))
    assert len(fragments) == 7
    for fragment in fragments:
        assert fragment in product, f"HTML 片段被改写：{fragment[:120]!r}"
        assert fragment in source, "片段必须是源文本子串（P4：导入期零改写）"


@pytest.mark.asyncio
async def test_largest_document_table_fragments_are_byte_identical(
    cxl: tuple[str, str], storage: Storage, tmp_path: Path
) -> None:
    """最大文档：1,243 个 ``<table>`` 片段全部逐字节出现（含 80 处 ``<img>`` 的片段）。"""
    doc_id, _ = cxl
    result = await render_document(doc_id, tmp_path / "rendered", storage=storage)
    product = Path(result.out_path).read_text(encoding="utf-8")

    fragments = _table_fragments(await storage.get_doc_nodes(doc_id))
    assert len(fragments) == 1243
    assert all(fragment in product for fragment in fragments)
    assert any("<img" in fragment for fragment in fragments), "应覆盖含 <img> 的表格片段"


@pytest.mark.asyncio
async def test_every_node_block_appears_byte_identical_in_product(
    amba: tuple[str, str], storage: Storage, tmp_path: Path
) -> None:
    """P4（逐节点字节覆盖）：每个节点的渲染文本都**逐字节**出现在产物中——零改写、零转义、零截断。

    **为何不是「整档正文逐字节等于源」**（实测证据，非放宽）：真实导入会按 M03 的原子模型重组块——
    clause 合并「标题行 + 并入段落」、表格/图/代码从 clause 抽离、紧邻行拆成独立节点——故块序与
    块边界**必然**与源不同；且 ``figure``/``cross_ref`` 原子按 M01 schema **没有 fragment**，渲染期
    只能合成（``![](assets/<sha>.ext)``、``[text](target)``）。这些是导入/原子模型的口径，不是渲染层
    改写。渲染层的零改写由三件事共同覆盖：本断言的逐节点字节覆盖、``<table>`` 片段逐字节、
    ``normalize`` 两式往返。
    """
    doc_id, _ = amba
    result = await render_document(doc_id, tmp_path / "rendered", storage=storage)
    product = Path(result.out_path).read_text(encoding="utf-8")
    nodes = await storage.get_doc_nodes(doc_id)

    _assert_node_blocks_verbatim(nodes, product)
    synthesized = [node.anchor for node in nodes if not node.content.get("fragment")]
    assert synthesized, "真实语料应含 fragment-less 原子（figure/cross_ref），用于固定合成口径"


def _assert_node_blocks_verbatim(nodes, product: str) -> None:
    """逐节点断言：``node_block_text`` 的结果是产物正文的逐字节子串（图片重写经掩码吸收）。"""
    masked = _mask_asset_refs(product)
    offenders = [
        node.anchor
        for node in nodes
        if (block := _mask_asset_refs(node_block_text(node))) and block not in masked
    ]
    assert offenders == [], f"节点渲染文本未逐字节出现：{offenders[:3]}（共 {len(offenders)}）"


@pytest.mark.asyncio
async def test_html_img_rewrite_is_the_only_fragment_change(
    cxl_img_window: tuple[str, str], storage: Storage, tmp_path: Path
) -> None:
    """P4 唯一例外：含 ``<img>`` 的片段重写后仅 ``src`` 变化（真实 CXL 片段 + 真实 CAS 资产）。"""
    doc_id, _ = cxl_img_window
    nodes = await storage.get_doc_nodes(doc_id)
    fragments = [fragment for fragment in _table_fragments(nodes) if "<img" in fragment]
    assert fragments, "窗口内应含带 ``<img>`` 的表格片段"
    fragment = fragments[0]

    # 分支 1：语料图片字节不在 CAS → 引用原样直通（片段逐字节不变）
    result = await render_document(doc_id, tmp_path / "rendered", storage=storage)
    assert fragment in Path(result.out_path).read_text(encoding="utf-8")

    # 分支 2：引用指向 CAS 中真实存在的资产 → 仅 src 被重写
    payload = b"\x89PNG\r\n\x1a\nM04-render-fixture"
    asset_id = await storage.put_asset(payload, "image/png", origin="test://m04")
    patched = _retarget_first_img(fragment, asset_id)
    await storage.upsert_doc(
        DocIn(
            doc_id=DOC_XLINK,
            doc_type="standard",
            title="M04 img rewrite fixture",
            meta={"purpose": "spec", "status": "approved"},
            source_ref=None,
        ),
        None,
        CTX,
    )
    content = {"fragment": patched, "meta": table_meta(table_cells(patched))}
    content["text"] = derive_text("table", content)
    await storage.upsert_node(
        NodeIn(
            node_id=new_uuid7(),
            doc_id=DOC_XLINK,
            atom_type="table",
            format="html",
            ordinal=1,
            parent_node_id=None,
            level=None,
            anchor=f"{DOC_XLINK}#sec",
            content=content,
        ),
        None,
        CTX,
    )

    result2 = await render_document(DOC_XLINK, tmp_path / "rendered2", storage=storage)
    product2 = Path(result2.out_path).read_text(encoding="utf-8")
    assert result2.assets_exported == 1
    exported = tmp_path / "rendered2" / "assets" / f"{asset_id}.png"
    assert exported.is_file() and exported.read_bytes() == payload
    assert f'src="assets/{asset_id}.png"' in product2
    assert _mask_img_src(patched) in _mask_img_src(product2), "除 src 外逐字节不变"
    # 判据 (b) 的 images 口径吸收扩展名差异：重写前后为同一 asset_id 集合
    assert normalize_markdown(product2).images == normalize_markdown(patched).images


# ── frontmatter 回写（§6）────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_frontmatter_writeback_matches_c5_mapping(
    amba: tuple[str, str], storage: Storage, tmp_path: Path
) -> None:
    """§6：产物 frontmatter = C5 十七字段（title/spec_id/spec_type/source 由 doc 列回填）。"""
    doc_id, _ = amba
    doc = await storage.get_doc(doc_id)
    result = await render_document(doc_id, tmp_path / "rendered", storage=storage)
    text = Path(result.out_path).read_text(encoding="utf-8")

    assert text.startswith("---\n")
    parsed = yaml.safe_load(text.split("---\n", 2)[1])
    assert parsed["title"] == doc.title
    assert parsed["spec_id"] == doc.doc_id == DOC_AMBA
    assert parsed["spec_type"] == doc.doc_type == "standard"
    assert parsed["source"] == doc.source_ref
    assert parsed["section_meta"] == "@meta"
    assert [f for f in ("spec_org", "spec_revision", "status", "version") if f not in parsed] == []


# ── 图片：合成 + 重写 + 导出 ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_image_assets_exported_and_rewritten(storage: Storage, tmp_path: Path) -> None:
    """figure 由图内资产合成图片引用 → 重写为 ``assets/<sha>.<ext>`` 并导出字节（REQ-M04-F03）。"""
    payload = b"\x89PNG\r\n\x1a\nM04-fixture"
    asset_id = await storage.put_asset(payload, "image/png", origin="test://m04-figure")
    doc_id = "SPEC-M04-FIGURE"
    await storage.upsert_doc(
        DocIn(
            doc_id=doc_id,
            doc_type="standard",
            title="figure fixture",
            meta={"purpose": "spec", "status": "approved"},
            source_ref=None,
        ),
        None,
        CTX,
    )
    await storage.upsert_node(
        NodeIn(
            node_id=new_uuid7(),
            doc_id=doc_id,
            atom_type="figure",
            format="md",
            ordinal=1,
            parent_node_id=None,
            level=None,
            anchor=f"{doc_id}#Figure",
            content={"text": "图 1", "asset_ref": asset_id, "alt": "图 1"},
        ),
        None,
        CTX,
    )
    result = await render_document(doc_id, tmp_path / "rendered", storage=storage)
    text = Path(result.out_path).read_text(encoding="utf-8")
    assert f"![图 1](assets/{asset_id}.png)" in text
    assert (tmp_path / "rendered" / "assets" / f"{asset_id}.png").read_bytes() == payload
    assert result.assets_exported == 1
    # normalize 的 images 口径 = asset_id 集合（重写前哈希路径）
    assert normalize_markdown(text).images == [f"assets/{asset_id}"]
    # (a) 库侧镜像 == 源文本（figure 由 asset_ref 合成，源侧是 images/<sha>.png）
    assert await normalize(doc_id, storage=storage) == normalize_markdown(f"![图 1](images/{asset_id}.png)\n")


# ── 分章节渲染（B10）＋ 性能（§1.4）────────────────────────────────────


@pytest.mark.asyncio
async def test_render_section_scoped_and_fast(
    amba: tuple[str, str], storage: Storage, tmp_path: Path
) -> None:
    """分章节渲染：只含该子树、产物落 ``sections/<anchor>.md``、耗时 <1s。"""
    doc_id, _ = amba
    nodes = await storage.get_doc_nodes(doc_id)
    sections = list_sections(nodes)
    assert sections, "应能识别出 level-1/2 章节"
    target = max(sections, key=lambda section: section.node_count)
    subtree = section_subtree(nodes, target.node_id)

    started = time.perf_counter()
    result = await render_section(doc_id, target.node_id, tmp_path / "rendered", storage=storage)
    elapsed = (time.perf_counter() - started) * 1000
    body = Path(result.out_path).read_text(encoding="utf-8")

    assert Path(result.out_path).parent.name == "sections"
    assert not body.startswith("---"), "章节产物不带 frontmatter"
    # 作用域证明：产物逐字节等于子树块拼接（多一个块就会不等）
    assert body.strip() == body_text(subtree).strip()
    assert len(subtree) < len(nodes), "用例应取真子集章节"
    print(f"[M04] render_section {elapsed:.1f}ms（AMBA 最大章节 {len(subtree)} 节点 / 全档 {len(nodes)} 节点）")
    assert elapsed < 1000, f"分章节渲染超预算：{elapsed:.0f}ms"


@pytest.mark.perf
@pytest.mark.asyncio
async def test_largest_document_render_timing(
    cxl: tuple[str, str], storage: Storage, tmp_path: Path
) -> None:
    """最大文档（CXL 3.59MB）：整档 <3s、最大章节 <1s（§1.4；导入耗时不属于渲染指标）。"""
    doc_id, _ = cxl
    nodes = await storage.get_doc_nodes(doc_id)
    started = time.perf_counter()
    await render_document(doc_id, tmp_path / "rendered", storage=storage)
    document_ms = (time.perf_counter() - started) * 1000

    target = max(list_sections(nodes), key=lambda section: section.node_count)
    started = time.perf_counter()
    await render_section(doc_id, target.node_id, tmp_path / "rendered", storage=storage)
    section_ms = (time.perf_counter() - started) * 1000

    print(
        f"[M04] 全档 CXL（3.59MB / {len(nodes)} 节点）：render_document {document_ms:.0f}ms；"
        f"render_section {section_ms:.0f}ms（最大章节 {target.node_count} 节点）"
    )
    assert section_ms < 1000, f"分章节渲染超预算：{section_ms:.0f}ms"
    assert document_ms < 3000, f"整档渲染超上限：{document_ms:.0f}ms"


# ── 错误路径与表格编辑回写 ───────────────────────────────────────────────


@pytest.mark.asyncio
async def test_render_missing_targets_raise_not_found(
    amba: tuple[str, str], storage: Storage, tmp_path: Path
) -> None:
    """不存在 → ``NotFoundError``（404），不产出半成品文件。"""
    doc_id, _ = amba
    with pytest.raises(NotFoundError):
        await render_document("SPEC-DOES-NOT-EXIST", tmp_path / "rendered", storage=storage)
    with pytest.raises(NotFoundError):
        await render_section(doc_id, new_uuid7(), tmp_path / "rendered", storage=storage)


@pytest.mark.asyncio
async def test_table_edit_roundtrip_writes_content_and_events(storage: Storage, tmp_path: Path) -> None:
    """表格编辑回写（B6/V8）：行列 JSON → content → 乐观锁写入 + node 事件。"""
    doc_id = "SPEC-M04-TABLE-EDIT"
    await storage.upsert_doc(
        DocIn(
            doc_id=doc_id,
            doc_type="standard",
            title="editable table",
            meta={"purpose": "spec", "status": "approved", "editable_tables": True},
            source_ref=None,
        ),
        None,
        CTX,
    )
    node = await storage.upsert_node(
        NodeIn(
            node_id=new_uuid7(),
            doc_id=doc_id,
            atom_type="table",
            format="md",
            ordinal=1,
            parent_node_id=None,
            level=None,
            anchor=f"{doc_id}#Tab",
            content=grid_to_content(TableGrid(rows=[["位域", "访问"], ["D0", "ro"]], header=True)),
        ),
        None,
        CTX,
    )
    mode = resolve_table_mode(await storage.get_doc(doc_id), node, user=None)
    assert mode.editable is False and mode.reason == "role_insufficient"

    edit = TableEdit(
        rows=[["位域", "访问"], ["D0", "rw"], ["D1", "ro"]],
        expected_version=node.version,
        header=True,
    )
    updated = await write_table_edit(node, edit, CTX, storage=storage)
    assert updated.version == node.version + 1
    assert parse_table_fragment(str(updated.content["fragment"])).rows == [
        ["位域", "访问"],
        ["D0", "rw"],
        ["D1", "ro"],
    ]
    assert updated.content["meta"]["rows"] == 3
    assert [event.op for event in await storage.replay("node", node.node_id)] == ["create", "update"]
    with pytest.raises(ConflictError):
        await write_table_edit(node, edit, CTX, storage=storage)  # 版本过期 → 409
