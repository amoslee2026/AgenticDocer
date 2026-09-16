"""M04 render 单测：节点渲染分派、P4 零改写、frontmatter 回写、图片重写、章节与表格编辑。

P4（HTML 片段零改写）在此以**逐字节**断言固定：片段原样出现在块文本里；唯一例外
（图片 ``src`` 重写）与「片段其余部分逐字节不变」分别断言。
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from uuid import uuid4

import pytest
import yaml

from agenticdocer.model import Doc, Node, User, new_uuid7
from agenticdocer.render import (
    EDITABLE_DOC_TYPES,
    TableEdit,
    TableGrid,
    body_text,
    build_table_fragment,
    collect_image_srcs,
    content_to_grid,
    document_frontmatter,
    find_section,
    frontmatter_text,
    grid_to_content,
    heading_text,
    iter_image_srcs,
    list_sections,
    node_block_text,
    parse_table_fragment,
    register_editable_doc_type,
    resolve_table_mode,
    rewrite_image_srcs,
    section_subtree,
    table_cells,
    table_meta,
    validate_table_content,
)
from agenticdocer.store import NotFoundError, ValidationError

SHA_A = "c" * 64
SHA_B = "d" * 64
NOW = datetime(2026, 9, 16, tzinfo=UTC)

HTML_TABLE = (
    '<table><tr><td colspan="2">位域</td></tr>'
    '<tr><td>0</td><td><img src="images/%s.jpg"/></td></tr></table>' % SHA_A
)


def make_node(
    *,
    atom_type: str = "clause",
    fmt: str = "md",
    level: int | None = None,
    ordinal: int = 1,
    anchor: str = "DOC#sec",
    content: dict | None = None,
    parent=None,
    node_id=None,
) -> Node:
    return Node(
        node_id=node_id or new_uuid7(),
        doc_id="DOC",
        atom_type=atom_type,
        format=fmt,
        ordinal=ordinal,
        parent_node_id=parent,
        level=level,
        anchor=anchor,
        content=content if content is not None else {"text": "正文", "fragment": "正文"},
        status="active",
        version=1,
        created_at=NOW,
        updated_at=NOW,
    )


def make_doc(*, doc_type: str = "standard", meta: dict | None = None) -> Doc:
    return Doc(
        doc_id="SPEC-DEMO",
        doc_type=doc_type,
        title="示例",
        meta=meta or {},
        source_ref="corpus/x.md",
        status="approved",
        version=1,
        created_at=NOW,
        updated_at=NOW,
    )


def make_user(role: str) -> User:
    return User(
        user_id=uuid4(),
        username="tester",
        role=role,
        status="active",
        created_at=NOW,
        updated_at=NOW,
    )


# ── P4：零改写直通 ───────────────────────────────────────────────────────


def test_html_fragment_is_emitted_byte_identically() -> None:
    node = make_node(atom_type="table", fmt="html", content={"fragment": HTML_TABLE, "text": "t"})
    assert node_block_text(node) == HTML_TABLE


def test_md_fragment_is_emitted_byte_identically() -> None:
    fragment = "## 3.1 术语\n\n正文含 `code`、%%批注%% 与 &amp; 实体。"
    node = make_node(content={"fragment": fragment, "text": fragment})
    assert node_block_text(node) == fragment


def test_block_text_strips_only_outer_newlines() -> None:
    fragment = "\n\n<table><tr><td>x</td></tr></table>\n"
    node = make_node(atom_type="table", fmt="html", content={"fragment": fragment, "text": "x"})
    assert node_block_text(node) == "<table><tr><td>x</td></tr></table>"


def test_body_text_separates_blocks_with_single_blank_line() -> None:
    nodes = [
        make_node(ordinal=1, content={"fragment": "# 标题", "text": "标题"}, level=1),
        make_node(ordinal=2, content={"fragment": "正文", "text": "正文"}),
        make_node(ordinal=3, content={"text": "   "}),  # 无 fragment、text 全空白 → 丢弃
    ]
    assert body_text(nodes) == "# 标题\n\n正文"


# ── 无 fragment 时的合成 ────────────────────────────────────────────────


def test_synthesized_heading_uses_level() -> None:
    node = make_node(level=3, content={"text": "3.1.2 规则"})
    assert node_block_text(node) == "### 3.1.2 规则"


def test_synthesized_code_uses_language_fence() -> None:
    node = make_node(atom_type="code", content={"text": "module m;\nendmodule", "language": "sv"})
    assert node_block_text(node) == "```sv\nmodule m;\nendmodule\n```"


def test_synthesized_figure_uses_asset_ref_and_caption() -> None:
    node = make_node(
        atom_type="figure",
        content={"text": "图 1", "asset_ref": SHA_A, "caption": "图 1 结构", "alt": "结构图"},
    )
    assert node_block_text(node) == f"![结构图](assets/{SHA_A})\n\n图 1 结构"


def test_synthesized_cross_ref_targets_anchor_doc_and_external_uri() -> None:
    node = make_node(
        atom_type="cross_ref",
        content={"text": "见 3.1", "ref_kind": "see_also", "target_doc_id": "DOC", "target_anchor": "DOC#3.1·术语"},
    )
    assert node_block_text(node) == "[见 3.1](#DOC#3.1·术语)"
    external = make_node(
        atom_type="cross_ref",
        content={"text": "RFC", "ref_kind": "source_ref", "target_doc_id": "EXT:https://x/y"},
    )
    assert node_block_text(external) == "[RFC](https://x/y)"


def test_synthesized_register_field_table_is_html() -> None:
    node = make_node(
        atom_type="table.register_field",
        fmt="md",
        content={
            "text": "CTRL",
            "register": "CTRL",
            "fields": [{"field": "EN", "bits": "0", "access": "rw"}],
        },
    )
    block = node_block_text(node)
    assert block.startswith("<table>") and block.endswith("</table>")
    assert table_cells(block) == [["EN", "0", "rw", "", ""]]


def test_synthesized_state_machine_prefers_mermaid_source() -> None:
    node = make_node(
        atom_type="figure.state_machine",
        content={"text": "sm", "states": ["A", "B"], "mermaid": "stateDiagram-v2\n  A --> B"},
    )
    assert node_block_text(node) == "```mermaid\nstateDiagram-v2\n  A --> B\n```"


def test_iter_image_srcs_covers_md_and_html_forms() -> None:
    text = f'![](images/{SHA_A}.jpg) ![alt](assets/{SHA_B}.png "t") <img src="images/{SHA_A}.jpg"/>'
    assert list(iter_image_srcs(text)) == [
        f"images/{SHA_A}.jpg",
        f"assets/{SHA_B}.png",
        f"images/{SHA_A}.jpg",
    ]
    assert collect_image_srcs([text, text]) == [f"images/{SHA_A}.jpg", f"assets/{SHA_B}.png"]


def test_rewrite_image_srcs_preserves_quotes_and_untouched_bytes() -> None:
    mapping = {f"images/{SHA_A}.jpg": f"assets/{SHA_A}.jpg"}
    text = f'<table><tr><td><img src="images/{SHA_A}.jpg"/></td>' f"<td><img src='images/{SHA_A}.jpg'></td></tr></table>"
    rewritten = rewrite_image_srcs(text, mapping)
    assert f'src="assets/{SHA_A}.jpg"' in rewritten
    assert f"src='assets/{SHA_A}.jpg'" in rewritten
    assert rewritten.replace("assets/", "images/") == text


def test_rewrite_image_srcs_leaves_unknown_refs_and_md_titles_alone() -> None:
    text = '![a](images/x.png "标题") ![](https://example.com/y.png)'
    assert rewrite_image_srcs(text, {}) == text
    assert rewrite_image_srcs(text, {"images/x.png": "assets/x.png"}) == '![a](assets/x.png "标题") ![](https://example.com/y.png)'


def test_html_img_rewrite_is_the_only_change_inside_table_fragment() -> None:
    node = make_node(atom_type="table", fmt="html", content={"fragment": HTML_TABLE, "text": "t"})
    rewritten = node_block_text(node, {f"images/{SHA_A}.jpg": f"assets/{SHA_A}.jpg"})
    assert rewritten.count("assets/") == 1
    masked = re.sub(r'(src=")[^"]*(")', r"\1@@\2", rewritten)
    assert masked == re.sub(r'(src=")[^"]*(")', r"\1@@\2", HTML_TABLE)
    assert rewritten != HTML_TABLE  # 差异仅限 src


# ── frontmatter（§6 C5 十七字段）────────────────────────────────────────


def test_document_frontmatter_maps_c5_fields_and_preserves_extras() -> None:
    doc = make_doc(
        meta={
            "type": "composite",
            "purpose": "spec",
            "spec_org": "ARM",
            "spec_revision": "IHI0024",
            "version": "1.0.0",
            "section_meta": "@meta",
            "status": "approved",
            "extra_field": "keep-me",
        }
    )
    data = document_frontmatter(doc)
    assert list(data) == [
        "title",
        "type",
        "purpose",
        "status",
        "version",
        "section_meta",
        "spec_id",
        "spec_type",
        "spec_org",
        "spec_revision",
        "source",
        "extra_field",
    ]
    assert data["title"] == "示例"
    assert data["spec_id"] == "SPEC-DEMO"
    assert data["spec_type"] == "standard"
    assert data["source"] == "corpus/x.md"
    assert data["status"] == "approved"
    assert data["extra_field"] == "keep-me"
    assert data["type"] == "composite"


def test_frontmatter_text_is_valid_yaml_and_ordered() -> None:
    doc = make_doc(meta={"spec_org": "ARM", "version": "1.0.0"})
    text = frontmatter_text(doc)
    assert text.startswith("---\n") and text.endswith("---\n")
    parsed = yaml.safe_load(text.split("---\n")[1])
    assert parsed["title"] == "示例"
    assert parsed["version"] == "1.0.0"
    assert list(parsed)[0] == "title"


def test_frontmatter_source_prefers_meta_over_source_ref() -> None:
    doc = make_doc(meta={"source": "corpus/meta.md"})
    assert document_frontmatter(doc)["source"] == "corpus/meta.md"


# ── 章节（B10）─────────────────────────────────────────────────────────


def test_section_subtree_returns_root_and_descendants_in_ordinal_order() -> None:
    root = make_node(level=1, ordinal=1, anchor="DOC#1·root", content={"fragment": "# Root", "text": "Root"})
    child = make_node(level=2, ordinal=3, anchor="DOC#1.1·c", parent=root.node_id, content={"fragment": "## C", "text": "C"})
    leaf = make_node(level=None, ordinal=2, anchor="DOC#1·p", parent=root.node_id, content={"fragment": "P", "text": "P"})
    other = make_node(level=1, ordinal=9, anchor="DOC#2·o", content={"fragment": "# O", "text": "O"})
    nodes = [root, child, leaf, other]
    assert section_subtree(nodes, root.node_id) == [root, leaf, child]
    assert section_subtree(nodes, other.node_id) == [other]
    with pytest.raises(NotFoundError):
        section_subtree(nodes, new_uuid7())


def test_section_subtree_tolerates_parent_cycles() -> None:
    first = make_node(level=1, ordinal=1, anchor="A", content={"fragment": "# A", "text": "A"})
    second = make_node(level=2, ordinal=2, anchor="B", parent=first.node_id, content={"fragment": "## B", "text": "B"})
    first = first.model_copy(update={"parent_node_id": second.node_id})
    assert len(section_subtree([first, second], first.node_id)) == 2


def test_heading_text_prefers_atx_fragment_over_content_text() -> None:
    node = make_node(level=3, content={"fragment": "## 1.3.2.1 Legacy Rules\n\n正文", "text": "1.3.2.1 Legacy Rules"})
    assert heading_text(node) == "1.3.2.1 Legacy Rules"
    plain = make_node(level=2, content={"text": "  无 fragment 的标题  "})
    assert heading_text(plain) == "无 fragment 的标题"


def test_list_sections_filters_levels_and_counts_subtree() -> None:
    root = make_node(level=1, ordinal=1, anchor="DOC#1·r", content={"fragment": "# R", "text": "R"})
    mid = make_node(level=2, ordinal=2, anchor="DOC#1.1·m", parent=root.node_id, content={"fragment": "## M", "text": "M"})
    deep = make_node(level=3, ordinal=3, anchor="DOC#1.1.1·d", parent=mid.node_id, content={"fragment": "### D", "text": "D"})
    sections = list_sections([root, mid, deep])
    assert [(s.anchor, s.level, s.title, s.node_count) for s in sections] == [
        ("DOC#1·r", 1, "R", 3),
        ("DOC#1.1·m", 2, "M", 2),
    ]
    assert find_section([root, mid, deep], "DOC#1.1·m") is mid
    assert find_section([root, mid, deep], "DOC#1.1.1·d") is None  # level>2 非章节


# ── 可编辑表格模式（B6/V8）────────────────────────────────────────────


def test_resolve_table_mode_reason_chain() -> None:
    doc = make_doc()
    node = make_node(atom_type="table", content={"fragment": "<table></table>", "text": "t"})
    html = make_node(atom_type="table", fmt="html", content={"fragment": "<table></table>", "text": "t"})
    editor = make_user("editor")
    reader = make_user("reader")

    assert resolve_table_mode(doc, html, editor).reason == "html_fragment"
    assert resolve_table_mode(doc, node, editor).reason == "flag_off"
    flagged = make_doc(meta={"editable_tables": True})
    assert resolve_table_mode(flagged, node, reader).reason == "role_insufficient"
    assert resolve_table_mode(flagged, node, None).reason == "role_insufficient"
    assert resolve_table_mode(flagged, node, editor) == resolve_table_mode(flagged, node, editor)
    assert resolve_table_mode(flagged, node, editor).editable is True
    assert resolve_table_mode(flagged, node, editor).reason == "flag_on"
    doc_admin = make_doc(meta={"editable_tables": False})
    assert resolve_table_mode(doc_admin, node, make_user("admin")).reason == "flag_off"


def test_resolve_table_mode_doc_type_whitelist() -> None:
    register_editable_doc_type("language-reference")
    try:
        doc = make_doc(doc_type="language-reference")
        node = make_node(atom_type="table", content={"fragment": "<table></table>", "text": "t"})
        mode = resolve_table_mode(doc, node, make_user("editor"))
        assert mode.editable is True and mode.reason == "doc_type_whitelist"
    finally:
        import agenticdocer.render.sections as sections

        sections.EDITABLE_DOC_TYPES = EDITABLE_DOC_TYPES


# ── 表格编辑（B6/V8）────────────────────────────────────────────────────


def test_table_cells_and_meta_handle_colspan_and_entities() -> None:
    fragment = '<table><tr><td colspan="2">a&amp;b</td></tr><tr><td>c</td><td>d</td></tr></table>'
    assert table_cells(fragment) == [["a&b"], ["c", "d"]]
    assert table_meta(table_cells(fragment)) == {"rows": 2, "cols": 2, "cells": 3, "max_colspan": 1}


def test_parse_and_build_table_fragment_roundtrip() -> None:
    fragment = "<table><tr><th>位域</th><th>访问</th></tr><tr><td>D0</td><td>ro</td></tr></table>"
    grid = parse_table_fragment(fragment)
    assert grid.header is True and grid.rows == [["位域", "访问"], ["D0", "ro"]]
    assert table_cells(build_table_fragment(grid)) == grid.rows


def test_build_table_fragment_escapes_cell_text() -> None:
    grid = TableGrid(rows=[["a<b"], ["x&y"], ["q\"z"]], header=False)
    built = build_table_fragment(grid)
    assert "<td>a&lt;b</td>" in built and "<td>x&amp;y</td>" in built
    assert table_cells(built) == [["a<b"], ["x&y"], ["q\"z"]]


def test_grid_to_content_and_back_is_stable() -> None:
    grid = TableGrid(rows=[["位域", "访问"], ["D0", "ro"]], header=True)
    content = grid_to_content(grid)
    assert set(content) == {"fragment", "meta", "text"}
    assert content["meta"]["rows"] == 2
    assert content["text"].startswith("位域")
    assert content_to_grid(content).rows == grid.rows
    validate_table_content("table", content)


def test_register_field_grid_maps_columns_and_requires_register() -> None:
    grid = TableGrid(
        rows=[["EN", "0", "rw"], ["MODE", "2:1", "ro"]],
        header=False,
        header_names=["field", "bits", "access"],
        register_name="CTRL",
    )
    content = grid_to_content(grid, atom_type="table.register_field")
    assert content["register"] == "CTRL"
    assert content["fields"] == [
        {"field": "EN", "bits": "0", "access": "rw"},
        {"field": "MODE", "bits": "2:1", "access": "ro"},
    ]
    back = content_to_grid(content)
    assert back.rows == [["EN", "0", "rw", "", ""], ["MODE", "2:1", "ro", "", ""]]
    assert back.register_name == "CTRL"
    with pytest.raises(ValidationError):  # 缺 register
        grid_to_content(
            TableGrid(rows=[["EN"]], header=False, header_names=["field"]),
            atom_type="table.register_field",
        )
    with pytest.raises(ValidationError):  # 无非空 field 列
        grid_to_content(
            TableGrid(rows=[["EN"]], header=False, header_names=["bits"]),
            atom_type="table.register_field",
        )


def test_grid_to_content_rejects_non_table_atom_and_bad_schema() -> None:
    with pytest.raises(ValidationError):
        grid_to_content(TableGrid(rows=[["a"]], header=True), atom_type="clause")
    with pytest.raises(ValidationError):
        validate_table_content("table", {"fragment": "<table></table>"})


def test_table_edit_model_defaults() -> None:
    edit = TableEdit(rows=[["a"]], expected_version=3)
    assert edit.header is True and edit.atom_type is None and edit.register_name is None
