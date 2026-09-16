"""M04 表格编辑回写支持（B6/V8）：行列 JSON ↔ 节点 ``content`` 转换。

口径（P5 单一判定口径）：

* 表格原子的**权威形态是 ``content.fragment``**（原样 HTML，P4）。本模块是
  「该 HTML ↔ 行列网格」的**唯一转换实现**：``normalize`` 的表格特征、``render`` 的
  合成表格、M07 的编辑回写全部经此，故三者同源、不会互相漂移。
* 编辑回写**只作用于 ``format != 'html'`` 的表格原子**（B6）；HTML ``<table>`` 片段恒只读
  （``sections.resolve_table_mode`` 的 ``html_fragment``，P4 零改写）。
* 回写端点统一为 M07 ``PATCH /api/v1/nodes/{node_id}/table``（body = 行列 JSON +
  ``expectedVersion``），乐观锁用 ``nodes.version``：不匹配 → ``ConflictError``(409)。
  本模块的 :func:`write_table_edit` 是该端点「转 ``content`` + 写 ``node`` 事件」的服务端实现。
* ``meta``（rows/cols/cells/max_colspan）与 ``text``（A10 检索投影）按 M01 口径派生，
  生成结果经 ``ATOM_SCHEMAS`` 校验后才允许写入（REQ-M01-F01）。

限制（显式声明）：``<table>`` 解析不处理嵌套表格与未闭合单元格（语料实测无此形态）；
``colspan``/``rowspan`` 不展开，故 ``meta.cols`` = 各行单元格数的最大值。
"""

from __future__ import annotations

import html as _html
import re
from collections.abc import Mapping, Sequence
from typing import Any, Final

import jsonschema

from agenticdocer.model import (
    TABLE_ATOMS,
    Model,
    Node,
    NodeIn,
    WriteContext,
    derive_text,
    get_atom_schema,
    html_to_text,
    normalize_body,
)
from agenticdocer.store import Storage, ValidationError

__all__ = [
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

REGISTER_FIELD_COLUMNS: Final = ("field", "bits", "access", "reset", "description")
"""``table.register_field`` 的行列名（= ATOM_SCHEMAS 中 ``fields[].properties`` 的键序）。"""

_ROW_RE: Final = re.compile(r"<tr\b[^>]*>(.*?)</tr>", re.IGNORECASE | re.DOTALL)
_CELL_RE: Final = re.compile(r"<t([dh])\b[^>]*>(.*?)</t\1>", re.IGNORECASE | re.DOTALL)
_TH_RE: Final = re.compile(r"<th\b", re.IGNORECASE)


class TableGrid(Model):
    """表格的行列网格（M07 请求体与 ``content`` 之间的中间表示）。"""

    rows: list[list[str]]
    header: bool = True
    """首行渲染为 ``<th>``（HTML 表格以 ``<th>`` 表头的形态亦靠此还原）。"""

    header_names: list[str] = []
    """可选列名（``table.register_field`` 靠它把行映射回 ``fields[]``）。"""

    register_name: str | None = None
    """``table.register_field`` 的寄存器名（对应 ``content['register']``，M01 schema 键名）。"""


class TableEdit(Model):
    """M07 ``PATCH /nodes/{node_id}/table`` 的请求体（行列 JSON + ``expectedVersion``）。"""

    rows: list[list[str]]
    expected_version: int
    header: bool = True
    header_names: list[str] = []
    register_name: str | None = None
    atom_type: str | None = None
    """缺省沿用节点既有 ``atom_type``；给定时必须是表格类原子。"""


def table_cells(fragment: str) -> list[list[str]]:
    """HTML 表格片段 → 单元格文本网格（**唯一解析口径**）。

    单元格文本经 M01 ``html_to_text`` 去标签 + ``normalize_body`` 折叠空白（NFKC）。
    """
    grid: list[list[str]] = []
    for row_html in _ROW_RE.findall(fragment or ""):
        grid.append([normalize_body(html_to_text(cell)) for _, cell in _CELL_RE.findall(row_html)])
    return grid


def table_meta(cells: Sequence[Sequence[str]]) -> dict[str, int]:
    """网格 → ``content.meta``（``colspan``/``rowspan`` 不展开，``cols`` 取各行最大值）。"""
    return {
        "rows": len(cells),
        "cols": max((len(row) for row in cells), default=0),
        "cells": sum(len(row) for row in cells),
        "max_colspan": 1,
    }


def parse_table_fragment(fragment: str) -> TableGrid:
    """HTML 表格片段 → :class:`TableGrid`（表头由首行是否 ``<th>`` 判定）。"""
    cells = table_cells(fragment)
    has_header = bool(_TH_RE.search(fragment or ""))
    return TableGrid(rows=cells, header=has_header)


def build_table_fragment(grid: TableGrid) -> str:
    """网格 → 规范 HTML 表格片段（单元格文本转义；供编辑回写与合成渲染共用）。"""
    lines = ["<table>"]
    for index, row in enumerate(grid.rows):
        tag = "th" if (grid.header and index == 0) else "td"
        body = "".join(
            f"<{tag}>{_html.escape(str(cell), quote=False)}</{tag}>" for cell in row
        )
        lines.append(f"<tr>{body}</tr>")
    lines.append("</table>")
    return "\n".join(lines)


def content_to_grid(content: Mapping[str, Any]) -> TableGrid:
    """节点 ``content`` → :class:`TableGrid`（``fields`` 优先，其次 ``fragment``）。"""
    fields = content.get("fields")
    if isinstance(fields, Sequence) and fields:
        rows = [
            [str((item or {}).get(name) or "") for name in REGISTER_FIELD_COLUMNS]
            for item in fields
            if isinstance(item, Mapping)
        ]
        register = content.get("register")
        return TableGrid(
            rows=rows,
            header=True,
            header_names=list(REGISTER_FIELD_COLUMNS),
            register=str(register) if register else None,
        )
    fragment = content.get("fragment")
    if isinstance(fragment, str) and fragment:
        register = content.get("register")
        grid = parse_table_fragment(fragment)
        return grid.model_copy(update={"register": str(register) if register else None})
    return TableGrid(rows=[], header=False)


def validate_table_content(atom_type: str, content: Mapping[str, Any]) -> None:
    """按 ``ATOM_SCHEMAS`` 校验待写入的 ``content``；失败 → ``ValidationError``(422)。"""
    try:
        jsonschema.validate(instance=dict(content), schema=get_atom_schema(atom_type))
    except jsonschema.ValidationError as exc:
        path = "/".join(str(part) for part in exc.absolute_path) or "<root>"
        raise ValidationError(
            f"{atom_type} content 不合 schema（{path}: {exc.message}）",
            entity="node",
        ) from exc


def grid_to_content(grid: TableGrid, *, atom_type: str = "table") -> dict[str, Any]:
    """网格 → 节点 ``content``（``fragment`` + ``meta`` + ``text``，表格变体另给 ``register``/``fields``）。

    :raises ValidationError: 原子非表格类，或生成的 ``content`` 不合 schema（422）。
    """
    if atom_type not in TABLE_ATOMS:
        raise ValidationError(
            f"{atom_type} 不是表格类原子（{sorted(TABLE_ATOMS)}），不可用行列编辑",
            entity="node",
        )
    fragment = build_table_fragment(grid)
    content: dict[str, Any] = {"fragment": fragment, "meta": table_meta(table_cells(fragment))}
    if atom_type == "table.register_field":
        names = list(grid.header_names or REGISTER_FIELD_COLUMNS)
        allowed = REGISTER_FIELD_COLUMNS
        fields: list[dict[str, str]] = []
        for row in grid.rows:
            item = {
                name: value
                for name, value in zip(names, row)
                if name in allowed and str(value).strip()
            }
            if item.get("field"):
                fields.append(item)
        if not fields:
            raise ValidationError("table.register_field 需要至少一行含 field 的字段行", entity="node")
        if not (grid.register or "").strip():
            raise ValidationError("table.register_field 需要 register（寄存器名）", entity="node")
        content["register"] = grid.register
        content["fields"] = fields
    content["text"] = derive_text(atom_type, content)
    validate_table_content(atom_type, content)
    return content


async def write_table_edit(
    node: Node,
    edit: TableEdit,
    ctx: WriteContext,
    *,
    storage: Storage,
) -> Node:
    """行列编辑 → ``content`` 转换 → 乐观锁写入（M07 ``PATCH /nodes/{id}/table`` 的服务端实现）。

    :raises NotFoundError: 节点不存在（404）。
    :raises ConflictError: ``expected_version`` 与 ``nodes.version`` 不匹配（409）。
    :raises ValidationError: 原子不可编辑 / ``content`` 不合 schema（422）。
    """
    atom_type = edit.atom_type or node.atom_type
    if atom_type not in TABLE_ATOMS:
        raise ValidationError(
            f"node {node.node_id} 的原子 {atom_type!r} 不是表格类，不可用行列编辑（B6）",
            entity="node",
            entity_id=node.node_id,
        )
    grid = TableGrid(
        rows=edit.rows,
        header=edit.header,
        header_names=list(edit.header_names),
        register=edit.register,
    )
    content = grid_to_content(grid, atom_type=atom_type)
    updated = NodeIn(
        node_id=node.node_id,
        doc_id=node.doc_id,
        atom_type=atom_type,
        format=node.format,
        ordinal=node.ordinal,
        parent_node_id=node.parent_node_id,
        level=node.level,
        anchor=node.anchor,
        content=content,
    )
    return await storage.upsert_node(updated, edit.expected_version, ctx)
