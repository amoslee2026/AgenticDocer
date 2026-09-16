"""M04 渲染引擎（L3 领域服务层）：节点树 → Markdown、规范化表示、章节与表格编辑支持。

对外契约（architecture_specification §3 M04）：

* :func:`render_document` / :func:`render_section`——渲染入口（``format='html'`` 片段零改写直通，P4）；
* :func:`normalize` / :func:`normalize_markdown`——往返判据的两侧（REQ-M04-F01 两式并列）；
* :class:`EditableTableMode` / :func:`resolve_table_mode`——表格渲染模式判定（B6/V8）；
* :func:`write_table_edit`——行列 JSON ↔ ``content`` 转换（M07 ``PATCH /nodes/{id}/table``）。

CLI 等价入口：``python -m agenticdocer.render <doc_id> [--section <anchor>]``。
"""

from __future__ import annotations

from .editable import (
    REGISTER_FIELD_COLUMNS,
    TableEdit,
    TableGrid,
    build_table_fragment,
    content_to_grid,
    grid_to_content,
    parse_table_fragment,
    table_cells,
    table_meta,
    validate_table_content,
    write_table_edit,
)
from .normalize import (
    NormalForm,
    TableNF,
    canonical_image_ref,
    extract_features,
    normalize,
    normalize_markdown,
    read_source,
)
from .renderer import (
    DEFAULT_RENDER_OUT_DIR,
    body_text,
    collect_image_srcs,
    document_frontmatter,
    frontmatter_text,
    iter_image_srcs,
    node_block_text,
    render_document,
    render_out_dir,
    render_section,
    rewrite_image_srcs,
)
from .sections import (
    EDITABLE_DOC_TYPES,
    EDITABLE_ROLES,
    EditableTableMode,
    SectionInfo,
    find_section,
    heading_text,
    list_sections,
    register_editable_doc_type,
    resolve_table_mode,
    section_subtree,
)

__all__ = [
    # renderer（§3 M04 渲染入口）
    "DEFAULT_RENDER_OUT_DIR",
    "body_text",
    "collect_image_srcs",
    "document_frontmatter",
    "frontmatter_text",
    "iter_image_srcs",
    "node_block_text",
    "render_document",
    "render_out_dir",
    "render_section",
    "rewrite_image_srcs",
    # normalize（REQ-M04-F02；往返判据）
    "NormalForm",
    "TableNF",
    "canonical_image_ref",
    "extract_features",
    "normalize",
    "normalize_markdown",
    "read_source",
    # sections（B6/B10）
    "EDITABLE_DOC_TYPES",
    "EDITABLE_ROLES",
    "EditableTableMode",
    "SectionInfo",
    "find_section",
    "heading_text",
    "list_sections",
    "register_editable_doc_type",
    "resolve_table_mode",
    "section_subtree",
    # editable（B6/V8 回写）
    "REGISTER_FIELD_COLUMNS",
    "TableEdit",
    "TableGrid",
    "build_table_fragment",
    "content_to_grid",
    "grid_to_content",
    "parse_table_fragment",
    "table_cells",
    "table_meta",
    "validate_table_content",
    "write_table_edit",
]
