"""M04 normalize 单测（REQ-M04-F02、P4/P5 口径）。

口径要点在此固定（P5「各自单测固定」）：六个特征族的口径、frontmatter 跳过、
图片 asset_id 口径（扩展名不入判据）、代码块与表格的边界隔离、以及**渲染无关的
等价性**（把 ``images/<sha>.jpg`` 改写成 ``assets/<sha>.jpg`` 不改变 images 集合——
这正是 P4「唯一例外」能与往返判据共存的原因）。
"""

from __future__ import annotations

from pathlib import Path

import pytest

from agenticspec.render import (
    NormalForm,
    canonical_image_ref,
    extract_features,
    normalize_markdown,
    read_source,
)

SHA_A = "a" * 64
SHA_B = "b" * 64

SOURCE = f"""---
title: 示例规范
spec_id: SPEC-DEMO
status: approved
---
# 概览

正文段落，含 `内联代码`、**粗体**、==高亮== 与 %%批注%%。

> [!TODO] 待办事项

## 1.1 术语

- 术语 A
- 术语 B
  续行文本

- 另一列表项

| 列一 | 列二 |
|---|---|
| a | b |

```sv
module m;  # 代码里的 # 与 <table> 不应被解析
<table><tr><td>x</td></tr></table>
```

![](images/{SHA_A}.jpg)

<table><tr><td>位域</td><td><img src="images/{SHA_B}.jpg"/></td></tr></table>
"""


def test_frontmatter_is_skipped_not_parsed_as_content() -> None:
    form = extract_features(SOURCE)
    assert ("title: 示例规范" in [text for _, text in form.headings]) is False
    assert form.headings[0] == (1, "概览")


def test_headings_use_atx_level_and_normalized_text() -> None:
    form = extract_features(SOURCE)
    assert form.headings == [
        (1, "概览"),
        (2, "1.1 术语"),
    ]


def test_tables_include_html_and_pipe_tables_in_document_order() -> None:
    form = extract_features(SOURCE)
    assert len(form.tables) == 2
    pipe, html = form.tables
    assert pipe.cells == [["列一", "列二"], ["a", "b"]]
    assert (pipe.rows, pipe.cols) == (2, 2)
    assert html.cells == [["位域", ""]]
    assert (html.rows, html.cols) == (1, 2)


def test_code_fence_content_extracted_and_isolated_from_other_features() -> None:
    form = extract_features(SOURCE)
    assert len(form.code_blocks) == 1
    assert "# 代码里的 # 与 <table> 不应被解析" in form.code_blocks[0]
    assert "<table><tr><td>x</td></tr></table>" in form.code_blocks[0]
    # 围栏内的 <table> 不得计入 tables（1 个管道表 + 1 个真实 HTML 表）
    assert len(form.tables) == 2


def test_lists_grouped_by_continuity_and_continuation_lines_folded() -> None:
    form = extract_features(SOURCE)
    assert form.lists == [["术语 A", "术语 B 续行文本"], ["另一列表项"]]


def test_inline_marker_kinds_are_deduplicated_and_sorted() -> None:
    form = extract_features(SOURCE)
    assert form.inline_markers == ["bold", "callout", "comment", "highlight", "inline_code"]


def test_images_use_asset_id_key_regardless_of_prefix_and_extension() -> None:
    form = extract_features(SOURCE)
    assert form.images == [f"assets/{SHA_A}", f"assets/{SHA_B}"]


@pytest.mark.parametrize(
    "before,after",
    [
        (f"![](images/{SHA_A}.jpg)", f"![](assets/{SHA_A}.jpg)"),
        (f"![](images/{SHA_A}.jpeg)", f"![](assets/{SHA_A}.png)"),
        (f'<img src="images/{SHA_A}.jpg"/>', f'<img src="assets/{SHA_A}.jpg"/>'),
        (f"![](assets/{SHA_A})", f"![](assets/{SHA_A}.jpg)"),
    ],
)
def test_image_rewrite_does_not_change_normal_form(before: str, after: str) -> None:
    """P4「图片 src 重写是唯一例外」与往返判据共存的原因：重写被 images 口径吸收。"""
    assert extract_features(before) == extract_features(after)


def test_canonical_image_ref_keeps_non_asset_refs_verbatim() -> None:
    assert canonical_image_ref(f"images/{SHA_A}.jpg") == f"assets/{SHA_A}"
    assert canonical_image_ref("https://example.com/a.png") == "https://example.com/a.png"
    assert canonical_image_ref("  ../figs/a.png  ") == "../figs/a.png"


def test_extract_features_is_deterministic_and_idempotent() -> None:
    once = extract_features(SOURCE)
    twice = extract_features(SOURCE)
    assert once == twice
    assert isinstance(once, NormalForm)


def test_product_like_text_with_frontmatter_is_equivalent_to_source_body() -> None:
    product = "---\ntitle: 示例规范\nspec_id: SPEC-DEMO\nstatus: approved\n---\n\n" + SOURCE.split(
        "---\n", 2
    )[2].lstrip("\n")
    assert extract_features(product) == extract_features(SOURCE)


def test_normalize_markdown_reads_path_and_text_forms(tmp_path: Path) -> None:
    path = tmp_path / "doc.md"
    path.write_text(SOURCE, encoding="utf-8")
    assert normalize_markdown(path) == normalize_markdown(SOURCE)
    assert normalize_markdown(str(path)) == normalize_markdown(SOURCE)
    assert read_source(path) == SOURCE


def test_read_source_rejects_other_types() -> None:
    with pytest.raises(TypeError):
        read_source(123)  # type: ignore[arg-type]


def test_unterminated_fence_still_captures_body() -> None:
    # 未闭合围栏：其后全文即代码块内容（逐字节，含行尾换行）
    form = extract_features("```py\nprint(1)\n")
    assert form.code_blocks == ["print(1)\n"]


def test_html_table_without_rows_is_ignored() -> None:
    assert extract_features("<table></table>").tables == []
