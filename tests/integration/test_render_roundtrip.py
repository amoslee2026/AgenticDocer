"""M04 集成测试：**真实语料**两式往返 + P4 逐字节证据 + 分章节性能（REQ-M04-F01/F03）。

覆盖：

1. **(a) 解析保真**：``await normalize(doc_id) == normalize_markdown(src)``（真实语料）；
2. **(b) 渲染保真**：``normalize_markdown(<产物文件>) == normalize_markdown(src)``；
3. **P4 硬证据**：HTML ``<table>`` 片段在产物中**逐字节出现**；含 ``<img>`` 的片段仅 ``src``
   属性被重写（重写前后哈希路径集合一致）；
4. **frontmatter 回写**：产物 frontmatter 解析回来 == C5 十七字段映射；
5. **图片重写与导出**：CAS 资产 → ``assets/<asset_id>.<ext>`` 相对路径 + 字节落 ``out_dir/assets/``；
6. **分章节渲染**：只含该子树、耗时 <1s（§1.4）。

语料：``spec/standards/amba/IHI0024_AMBA_APB_spec.md``（整档 263 块，含 7 个 HTML 表格、8 张图）
与 ``spec/standards/cxl/…``（含 ``<img>`` 的 HTML 表格窗口）。节点树由
``corpus_ingest``（M03 替身）产出；M03 落地后改用真实导入，断言不变。
"""

from __future__ import annotations

import itertools
import re
import time
from pathlib import Path

import pytest
import yaml

from agenticdocer.model import DocIn, NodeIn, derive_text, new_uuid7
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

from corpus_ingest import (
    CORPUS_ROOT,
    CTX,
    bulk_ingest_markdown,
    ingest_markdown,
    split_blocks,
    split_frontmatter,
    window_with_images,
)

pytestmark = pytest.mark.integration

AMBA = CORPUS_ROOT / "amba" / "IHI0024_AMBA_APB_spec.md"
CXL = CORPUS_ROOT / "cxl" / "CXL_Specification_rev3p2_ver1p0.md"

AMBA_DOC = "SPEC-STD-AMBA-APB"
CXL_DOC = "SPEC-CXL-3P2-WINDOW"

_SEQ = itertools.count(1)


def _require(path: Path) -> None:
    if not path.is_file():
        pytest.skip(f"语料缺失：{path}（设 AGENTICDOCER_CORPUS 指向语料根）")


def _table_fragments(nodes) -> list[str]:
    """含 ``<table>`` 的节点片段（语料中表格常与 OCR 残句同块，故按「包含」而非「起始」判定）。"""
    return [
        str(node.content["fragment"])
        for node in nodes
        if node.content.get("fragment") and "<table" in str(node.content["fragment"])
    ]


@pytest.fixture
async def amba(storage: Storage) -> tuple[str, str]:
    """整档入库 AMBA APB（每次用唯一 doc_id，避免跨测试锚唯一约束冲突）。"""
    _require(AMBA)
    return await ingest_markdown(storage, AMBA, f"{AMBA_DOC}-{next(_SEQ)}")


@pytest.fixture
async def cxl_window(storage: Storage) -> tuple[str, str]:
    """CXL 含 ``<img>`` 表格的窗口入库（真实片段 + 真实引用）。"""
    _require(CXL)
    _, body = split_frontmatter(CXL.read_text(encoding="utf-8"))
    window = window_with_images(split_blocks(body))
    return await ingest_markdown(storage, CXL, f"{CXL_DOC}-{next(_SEQ)}", window=window)


@pytest.mark.asyncio
async def test_real_corpus_two_way_roundtrip(amba: tuple[str, str], storage: Storage, tmp_path: Path) -> None:
    """真实语料整档：判据 (a) 解析保真 + (b) 渲染保真。"""
    doc_id, source = amba
    source_form = normalize_markdown(source)

    # (a) 解析保真——不经渲染
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
async def test_html_table_fragments_are_byte_identical(
    amba: tuple[str, str], storage: Storage, tmp_path: Path
) -> None:
    """P4 硬证据：真实语料的 HTML ``<table>`` 片段在产物中逐字节出现。"""
    doc_id, source = amba
    result = await render_document(doc_id, tmp_path / "rendered", storage=storage)
    text = Path(result.out_path).read_text(encoding="utf-8")

    nodes = await storage.get_doc_nodes(doc_id)
    fragments = _table_fragments(nodes)
    assert len(fragments) == 7
    for fragment in fragments:
        assert fragment in text, f"HTML 片段被改写：{fragment[:120]!r}"
        assert source.count(fragment) >= 1


@pytest.mark.asyncio
async def test_html_img_rewrite_is_the_only_fragment_change(
    cxl_window: tuple[str, str], storage: Storage, tmp_path: Path
) -> None:
    """P4 唯一例外：含 ``<img>`` 的片段重写后仅 ``src`` 变化（真实 CXL 片段 + 真实 CAS 资产）。"""
    doc_id, _ = cxl_window
    nodes = await storage.get_doc_nodes(doc_id)
    with_img = [fragment for fragment in _table_fragments(nodes) if "<img" in fragment]
    assert with_img, "窗口内应至少有一个含 <img> 的 HTML 表格片段"

    # 语料图片字节不在本机（引用解析不到资产行）→ 先断言「不可解析即原样直通」（P4 直通分支）
    result = await render_document(doc_id, tmp_path / "rendered", storage=storage)
    text = Path(result.out_path).read_text(encoding="utf-8")
    for fragment in with_img:
        assert fragment in text, "不可解析的图片引用必须原样保留（P4 直通）"

    # 解析得动的分支：把片段的 <img> src 换成 CAS 中真实存在的 asset_id，重渲染
    sample = with_img[0]
    payload = b"\x89PNG\r\n\x1a\nM04-render-fixture"
    asset_id = await storage.put_asset(payload, "image/png", origin="test://m04")
    patched = _retarget_first_img(sample, asset_id)
    doc2 = f"SPEC-CXL-IMG-REWRITE-{next(_SEQ)}"
    await _store_single_table_doc(storage, doc2, patched)

    result2 = await render_document(doc2, tmp_path / "rendered2", storage=storage)
    text2 = Path(result2.out_path).read_text(encoding="utf-8")
    assert result2.assets_exported == 1
    exported = tmp_path / "rendered2" / "assets" / f"{asset_id}.png"
    assert exported.is_file() and exported.read_bytes() == payload
    assert f'src="assets/{asset_id}.png"' in text2
    # 除 src 之外的字节完全一致（P4：片段本体零改写）
    assert _mask_img_src(patched) in _mask_img_src(text2)
    # 判据 (b) 的 images 口径吸收扩展名差异：重写前后为同一 asset_id 集合
    assert normalize_markdown(text2).images == normalize_markdown(patched).images


def _retarget_first_img(fragment: str, asset_id: str) -> str:
    """把片段中第一个 ``<img>`` 引用指向 ``asset_id``（其余结构/字节不动；测试夹具用）。"""
    pattern = re.compile(r"(images/)[0-9a-f]{64}(\.[A-Za-z0-9]+)")
    return pattern.sub(lambda match: f"{match.group(1)}{asset_id}{match.group(2)}", fragment, count=1)


def _mask_img_src(fragment: str) -> str:
    """把 ``<img src="…">`` 的值替换为占位符（用于「只有 src 变了」的逐字节比较）。"""
    return re.sub(
        r'(<img\b[^>]*?\bsrc\s*=\s*")[^"]*(")',
        r"\1@@\2",
        fragment,
    )


async def _store_single_table_doc(storage: Storage, doc_id: str, fragment: str) -> None:
    """单节点文档：一个 ``format='html'`` 的表格节点（图片重写路径的最小复现）。"""
    await storage.upsert_doc(
        DocIn(
            doc_id=doc_id,
            doc_type="standard",
            title="M04 image rewrite fixture",
            meta={"purpose": "spec", "status": "approved"},
            source_ref=None,
        ),
        None,
        CTX,
    )

    content = {"fragment": fragment, "meta": table_meta(table_cells(fragment))}
    content["text"] = derive_text("table", content)
    await storage.upsert_node(
        NodeIn(
            node_id=new_uuid7(),
            doc_id=doc_id,
            atom_type="table",
            format="html",
            ordinal=1,
            parent_node_id=None,
            level=None,
            anchor=f"{doc_id}#sec",
            content=content,
        ),
        None,
        CTX,
    )


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
    head = text.split("---\n", 2)[1]
    parsed = yaml.safe_load(head)
    assert parsed["title"] == doc.title
    assert parsed["spec_id"] == doc.doc_id == doc_id
    assert parsed["spec_type"] == doc.doc_type == "standard"
    assert parsed["source"] == doc.source_ref
    missing = [field for field in ("spec_org", "spec_revision", "status", "version") if field not in parsed]
    assert missing == []
    assert parsed["section_meta"] == "@meta"


@pytest.mark.asyncio
async def test_image_assets_exported_and_rewritten(storage: Storage, tmp_path: Path) -> None:
    """图片重写为 ``assets/<sha>.<ext>`` 相对路径，且字节导出到 ``out_dir/assets/``（REQ-M04-F03）。"""
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
            content={"text": "images/placeholder.png", "asset_ref": asset_id, "alt": "图 1"},
        ),
        None,
        CTX,
    )
    result = await render_document(doc_id, tmp_path / "rendered", storage=storage)
    text = Path(result.out_path).read_text(encoding="utf-8")
    assert f"![图 1](assets/{asset_id}.png)" in text
    exported = tmp_path / "rendered" / "assets" / f"{asset_id}.png"
    assert exported.read_bytes() == payload
    assert result.assets_exported == 1
    # normalize 的 images 口径 = asset_id 集合（重写前哈希路径）
    assert normalize_markdown(text).images == [f"assets/{asset_id}"]
    # (a) 库侧镜像 == 源文本（figure 由 asset_ref 合成，源侧是 images/<sha>.png）
    source = f"![图 1](images/{asset_id}.png)\n"
    assert await normalize(doc_id, storage=storage) == normalize_markdown(source)


@pytest.mark.asyncio
async def test_render_section_scoped_and_fast(
    amba: tuple[str, str], storage: Storage, tmp_path: Path
) -> None:
    """分章节渲染（B10）：只含该子树、产物落 ``sections/<anchor>.md``、耗时 <1s（§1.4）。"""
    doc_id, _ = amba
    nodes = await storage.get_doc_nodes(doc_id)
    sections = list_sections(nodes)
    assert sections, "应能识别出 level-1/2 章节"
    target = max(sections, key=lambda section: section.node_count)
    subtree = section_subtree(nodes, target.node_id)
    assert len(subtree) >= 1

    started = time.perf_counter()
    result = await render_section(doc_id, target.node_id, tmp_path / "rendered", storage=storage)
    elapsed = time.perf_counter() - started
    body = Path(result.out_path).read_text(encoding="utf-8")
    assert Path(result.out_path).parent.name == "sections"
    assert not body.startswith("---"), "章节产物不带 frontmatter"
    # 作用域证明：产物 **逐字节等于** 子树块拼接（多一个块就会不等）
    assert body.strip() == body_text(subtree).strip()
    assert len(subtree) < len(nodes), "用例应取真子集章节"
    print(
        f"[M04] render_section {elapsed * 1000:.1f}ms"
        f"（AMBA 最大章节：{len(subtree)} 节点 / 全档 {len(nodes)} 节点）"
    )
    assert elapsed < 1.0, f"分章节渲染超预算：{elapsed:.3f}s"


@pytest.mark.perf
@pytest.mark.asyncio
async def test_full_cxl_document_roundtrip_and_timing(storage: Storage, tmp_path: Path) -> None:
    """**最大文档**（CXL 3.59MB / 13,835 块）：两式往返 + P4 片段证据 + 渲染耗时（§1.4）。

    入库走 ``bulk_ingest_markdown``（基准夹具，见其 docstring）：本测试测量的是读取与渲染成本。
    """
    _require(CXL)
    doc_id = f"SPEC-CXL-FULL-{next(_SEQ)}"
    _doc_id, source = await bulk_ingest_markdown(storage, CXL, doc_id)
    # (a) 解析保真
    source_form = normalize_markdown(source)

    started = time.perf_counter()
    result = await render_document(doc_id, tmp_path / "full", storage=storage)
    document_ms = (time.perf_counter() - started) * 1000
    product = Path(result.out_path).read_text(encoding="utf-8")

    # (b) 渲染保真
    assert normalize_markdown(product) == source_form
    # P4：全部 HTML 表格片段逐字节出现（含 <img> 者：引用未落库 → 原样直通）
    nodes = await storage.get_doc_nodes(doc_id)
    fragments = _table_fragments(nodes)
    assert len(fragments) == 1243
    assert all(fragment in product for fragment in fragments)

    sections = list_sections(nodes)
    target = max(sections, key=lambda section: section.node_count)
    started = time.perf_counter()
    await render_section(doc_id, target.node_id, tmp_path / "full", storage=storage)
    section_ms = (time.perf_counter() - started) * 1000

    print(
        f"[M04] 全档（CXL 3.59MB/{len(nodes)} 节点）：render_document {document_ms:.0f}ms；"
        f"render_section {section_ms:.0f}ms（最大章节 {target.node_count} 节点）"
    )
    assert section_ms < 1000, f"分章节渲染超预算：{section_ms:.0f}ms"
    assert document_ms < 3000, f"整档渲染超上限：{document_ms:.0f}ms"

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
async def test_table_edit_roundtrip_writes_content_and_events(
    storage: Storage, tmp_path: Path
) -> None:
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
            content=grid_to_content(
                TableGrid(rows=[["位域", "访问"], ["D0", "ro"]], header=True)
            ),
        ),
        None,
        CTX,
    )
    doc = await storage.get_doc(doc_id)
    mode = resolve_table_mode(doc, node, user=None)
    assert mode.editable is False and mode.reason == "role_insufficient"

    edit = TableEdit(
        rows=[["位域", "访问"], ["D0", "rw"], ["D1", "ro"]],
        expected_version=node.version,
        header=True,
    )
    updated = await write_table_edit(node, edit, CTX, storage=storage)
    assert updated.version == node.version + 1
    grid = parse_table_fragment(str(updated.content["fragment"]))
    assert grid.rows == [["位域", "访问"], ["D0", "rw"], ["D1", "ro"]]
    assert updated.content["meta"]["rows"] == 3

    events = await storage.replay("node", node.node_id)
    assert [event.op for event in events] == ["create", "update"]
    with pytest.raises(ConflictError):
        await write_table_edit(node, edit, CTX, storage=storage)  # 版本过期 → 409
