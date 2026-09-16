"""M04 章节清单与可编辑表格判定（B6 / B10 / V8）。

* **章节（B10）**：*章节* = ``level ∈ {1, 2}`` 的节点及其后代子树。``node.level`` 由 M03 按
  **标题编号深度**给出（语料 99.8% 的标题写作 ``##``，真实层级在编号里），故 level-1/2 即
  编号深度 1/2，直接对应用户可读章节；``parent_node_id`` 由 M03 在 commit 阶段重建。
* **可编辑表格模式（B6/V8）**：``editable = (meta.editable_tables is True OR doc_type ∈
  EDITABLE_DOC_TYPES) AND role ∈ {admin, editor} AND format != 'html'``；
  HTML ``<table>`` 片段恒不可编辑（P4 零改写直通）。回写端点见
  :func:`agenticdocer.render.editable.write_table_edit`（M07 ``PATCH /nodes/{id}/table``）。
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Final, Literal
from uuid import UUID

from agenticdocer.model import Doc, Model, Node, User, UUID7, normalize_body
from agenticdocer.store import NotFoundError, as_uuid

__all__ = [
    "EDITABLE_DOC_TYPES",
    "EDITABLE_ROLES",
    "EditableTableMode",
    "SectionInfo",
    "heading_text",
    "list_sections",
    "register_editable_doc_type",
    "resolve_table_mode",
    "section_subtree",
]

EDITABLE_DOC_TYPES: frozenset[str] = frozenset()
"""可编辑表格的 ``doc_type`` 白名单（默认空，由配置经 :func:`register_editable_doc_type` 扩展）。"""

EDITABLE_ROLES: Final = frozenset({"admin", "editor"})
"""可编辑表格的调用方角色（B6：非 editor 一律只读）。"""

_ATX: Final = re.compile(r"^\s{0,3}#{1,6}\s+(.*?)(?:\s+#+)?\s*$")


class SectionInfo(Model):
    """章节清单条目（M07 ``GET /api/v1/docs/{id}/sections`` 的数据源）。"""

    node_id: UUID7
    parent_node_id: UUID7 | None
    anchor: str
    title: str
    level: int
    ordinal: int
    node_count: int
    """子树节点数（含自身，``status='active'``）。"""


class EditableTableMode(Model):
    """表格原子的渲染模式判定结果（B6/V8）。"""

    editable: bool
    reason: Literal["flag_on", "doc_type_whitelist", "role_insufficient", "flag_off", "html_fragment"]


def register_editable_doc_type(doc_type: str) -> None:
    """把 ``doc_type`` 加入可编辑白名单（Q6/B6：白名单由配置扩展，默认空）。

    注意：本函数**重绑定模块属性** ``EDITABLE_DOC_TYPES``；消费方请调用
    :func:`resolve_table_mode`（在调用时读取模块属性），不要 ``from … import EDITABLE_DOC_TYPES``
    后长期持有旧值。
    """
    global EDITABLE_DOC_TYPES
    EDITABLE_DOC_TYPES = EDITABLE_DOC_TYPES | {doc_type}


def heading_text(node: Node) -> str:
    """节点 → 标题文本：优先取 ``fragment`` 首行的 ATX 文本（P4 原文口径），否则取 ``content.text``。"""
    fragment = (node.content or {}).get("fragment")
    if isinstance(fragment, str) and fragment.strip():
        first_line = fragment.lstrip("\n").split("\n", 1)[0]
        match = _ATX.match(first_line)
        if match:
            return normalize_body(match.group(1))
    return normalize_body(str((node.content or {}).get("text") or ""))


def _order_key(node: Node) -> tuple[int, str]:
    return (node.ordinal, str(node.node_id))


def section_subtree(nodes: Sequence[Node], section_node_id: UUID | str) -> list[Node]:
    """章节子树：``section_node_id`` 及其后代，按 ``ordinal`` 序（B10）。

    仅依据文档内节点集（一次查询即可），循环父子链按 visited 截断（脏数据不死循环）。

    :raises NotFoundError: 节点不在给定节点集内（404）。
    """
    target = as_uuid(section_node_id)
    children: dict[UUID | None, list[Node]] = {}
    by_id: dict[UUID, Node] = {}
    for node in nodes:
        by_id[node.node_id] = node
        children.setdefault(node.parent_node_id, []).append(node)
    root = by_id.get(target)
    if root is None:
        raise NotFoundError(
            f"section node {section_node_id} not found in doc {nodes[0].doc_id if nodes else '?'}",
            entity="node",
            entity_id=target,
        )
    reached: set[UUID] = set()
    stack: list[Node] = [root]
    while stack:
        current = stack.pop()
        if current.node_id in reached:
            continue
        reached.add(current.node_id)
        stack.extend(children.get(current.node_id, ()))
    return sorted((node for node in nodes if node.node_id in reached), key=_order_key)


def list_sections(nodes: Sequence[Node], *, max_level: int = 2) -> list[SectionInfo]:
    """章节清单：``level ≤ max_level`` 的节点 + 各自子树节点数（B10，供 M07/M08）。"""
    counts: dict[UUID, int] = {}
    for node in nodes:
        counts[node.node_id] = counts.get(node.node_id, 0) + 1
    # 子树规模：按父链向上累计（O(n)，不做逐章节遍历）
    by_id = {node.node_id: node for node in nodes}
    sizes: dict[UUID, int] = {}
    for node in nodes:
        seen: set[UUID] = set()
        cursor: Node | None = node
        while cursor is not None and cursor.node_id not in seen:
            seen.add(cursor.node_id)
            sizes[cursor.node_id] = sizes.get(cursor.node_id, 0) + 1
            cursor = by_id.get(cursor.parent_node_id) if cursor.parent_node_id else None
    sections: list[SectionInfo] = []
    for node in sorted(nodes, key=_order_key):
        level = node.level
        if level is None or level < 1 or level > max_level:
            continue
        sections.append(
            SectionInfo(
                node_id=node.node_id,
                parent_node_id=node.parent_node_id,
                anchor=node.anchor,
                title=heading_text(node),
                level=level,
                ordinal=node.ordinal,
                node_count=sizes.get(node.node_id, counts.get(node.node_id, 0)),
            )
        )
    return sections


def find_section(nodes: Sequence[Node], anchor: str, *, max_level: int = 2) -> Node | None:
    """按锚定位章节节点（M07 ``?section=<anchor>`` 与 CLI ``--section`` 用）。"""
    for node in sorted(nodes, key=_order_key):
        if node.anchor != anchor:
            continue
        if node.level is not None and 1 <= node.level <= max_level:
            return node
        return None
    return None


def resolve_table_mode(doc: Doc, node: Node, user: User | None) -> EditableTableMode:
    """判定表格原子的渲染模式（B6/V8）：``editable`` + ``reason``。

    判定链（先到先得）：``html`` 片段 → ``html_fragment``；开关与白名单都未命中 → ``flag_off``；
    角色不足（含匿名 ``None``）→ ``role_insufficient``；``meta.editable_tables is True`` →
    ``flag_on``；否则 ``doc_type_whitelist``。

    仅对表格类原子有意义（调用方按 ``atom_type ∈ TABLE_ATOMS`` 过滤）；非表格原子恒
    ``editable=False`` 且按同一链条给出 ``reason``。
    """
    if node.format == "html":
        return EditableTableMode(editable=False, reason="html_fragment")
    by_flag = (doc.meta or {}).get("editable_tables") is True
    by_whitelist = doc.doc_type in EDITABLE_DOC_TYPES
    if not (by_flag or by_whitelist):
        return EditableTableMode(editable=False, reason="flag_off")
    if user is None or user.role not in EDITABLE_ROLES:
        return EditableTableMode(editable=False, reason="role_insufficient")
    return EditableTableMode(
        editable=True,
        reason="flag_on" if by_flag else "doc_type_whitelist",
    )
