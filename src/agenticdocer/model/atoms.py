"""M01 原子定义：八类原子的 JSON Schema、2 变体与 ``content.text`` 派生（A10/R5）。

- 权威来源：§3 M01（`ATOM_TYPES` / `ATOM_VARIANTS` / `get_json_schema` / `derive_text`）、
  design_doc §5.1（内容原子与格式策略 E1）、functional REQ-M01-F01（schema 注册与加载）。
- `ATOM_SCHEMAS` 即 `schemas` 表（§4）的种子内容：key = `type_name`（八类 + 2 变体），
  value = JSON Schema（draft 2020-12）；M02 落库、M09A 加载校验，两侧同一份定义（P5）。
- `extra="forbid"` 的等价物是 ``additionalProperties: false``：拼错字段即违规，
  schema 变更必须显式升版并产生 `schema` 事件（REQ-M01-F01）。
- ``text`` 为**一切原子的必填字段**：FTS 生成列 `nodes.text_fts` 只读 `content->>'text'`
  （§4 DDL / A10），故 M01 提供 :func:`derive_text` 作为该字段的唯一生成口径，写入前调用。
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from html.parser import HTMLParser
from typing import Any

__all__ = [
    "ATOM_TYPES",
    "ATOM_VARIANTS",
    "ATOM_SCHEMAS",
    "TABLE_ATOMS",
    "UnknownAtomTypeError",
    "get_atom_schema",
    "derive_text",
    "html_to_text",
]

ATOM_TYPES: tuple[str, ...] = ("clause", "definition", "table", "figure", "code", "example", "note", "cross_ref")
ATOM_VARIANTS: tuple[str, ...] = ("table.register_field", "figure.state_machine")

TABLE_ATOMS: frozenset[str] = frozenset({"table", "table.register_field"})
"""表格类原子：`content.fragment` 必为原样 HTML 片段（design_doc §5.1，E1-a）。"""

_DIALECT = "https://json-schema.org/draft/2020-12/schema"
_SHA256_HEX = r"^[0-9a-f]{64}$"

_TEXT_PROP: dict[str, Any] = {
    "type": "string",
    "minLength": 1,
    "description": "纯文本投影（A10：FTS 与检索的唯一来源，非空；由 M01.derive_text 生成）",
}
_FRAGMENT_PROP: dict[str, Any] = {
    "type": "string",
    "description": "源标记原样片段（`format` 为 md/html 时随渲染直通，P4 零改写）",
}
_TABLE_META_PROP: dict[str, Any] = {
    "type": "object",
    "description": "解析器统计的表格结构元数据（E1-a：供 M09B 行列断言）",
    "properties": {
        "rows": {"type": "integer", "minimum": 0},
        "cols": {"type": "integer", "minimum": 0},
        "cells": {"type": "integer", "minimum": 0},
        "max_colspan": {"type": "integer", "minimum": 1},
    },
    "required": ["rows", "cols", "cells", "max_colspan"],
    "additionalProperties": False,
}
_REGISTER_FIELD_PROP: dict[str, Any] = {
    "type": "object",
    "description": "寄存器字段行",
    "properties": {
        "field": {"type": "string", "minLength": 1},
        "bits": {"type": "string", "description": "位区间，如 '7:0' 或单个位号"},
        "access": {"enum": ["ro", "rw", "wo", "rw1c", "w1c", "reserved"]},
        "reset": {"type": "string"},
        "description": {"type": "string"},
    },
    "required": ["field"],
    "additionalProperties": False,
}
_TRANSITION_PROP: dict[str, Any] = {
    "type": "object",
    "properties": {
        "from": {"type": "string", "minLength": 1},
        "to": {"type": "string", "minLength": 1},
        "event": {"type": "string"},
        "condition": {"type": "string"},
    },
    "required": ["from", "to"],
    "additionalProperties": False,
}


def _schema(title: str, description: str, props: dict[str, Any], required: Sequence[str]) -> dict[str, Any]:
    return {
        "$schema": _DIALECT,
        "title": title,
        "description": description,
        "type": "object",
        "properties": {"text": _TEXT_PROP, **props},
        "required": ["text", *required],
        "additionalProperties": False,
    }


_CLAUDE_BODY = "条款正文的段落/列表/内联标记（ADR-006：clause 为最小节点，子结构不单独成节点）"

ATOM_SCHEMAS: dict[str, dict[str, Any]] = {
    "clause": _schema("clause", f"条款：{_CLAUDE_BODY}", {"fragment": _FRAGMENT_PROP}, ()),
    "definition": _schema(
        "definition",
        "术语定义（M03 导入时写入 terms 词表，R10）",
        {
            "term": {"type": "string", "minLength": 1, "description": "被定义术语"},
            "fragment": _FRAGMENT_PROP,
        },
        ("term",),
    ),
    "table": _schema(
        "table",
        "表格：`fragment` 为原样 HTML 片段（不允许拆解再还原，E1-a）",
        {"fragment": {**_FRAGMENT_PROP, "minLength": 1}, "meta": _TABLE_META_PROP},
        ("fragment", "meta"),
    ),
    "table.register_field": _schema(
        "table.register_field",
        "表格变体：寄存器字段表（寄存器名 + 字段行集合）",
        {
            "fragment": {**_FRAGMENT_PROP, "minLength": 1},
            "meta": _TABLE_META_PROP,
            "register": {"type": "string", "minLength": 1, "description": "寄存器名/偏移标识"},
            "fields": {"type": "array", "items": _REGISTER_FIELD_PROP, "minItems": 1},
        },
        ("fragment", "meta", "register", "fields"),
    ),
    "figure": _schema(
        "figure",
        "图：`asset_ref` 指向内容寻址资产（E2）；内联示意可仅给 `text`",
        {
            "asset_ref": {"type": "string", "pattern": _SHA256_HEX, "description": "assets.asset_id（sha256 hex）"},
            "caption": {"type": "string"},
            "alt": {"type": "string", "description": "HTML <img alt> 原文（P4 直通）"},
        },
        (),
    ),
    "figure.state_machine": _schema(
        "figure.state_machine",
        "图变体：状态机（状态集合 + 迁移集合）",
        {
            "asset_ref": {"type": "string", "pattern": _SHA256_HEX},
            "states": {"type": "array", "items": {"type": "string", "minLength": 1}, "minItems": 1},
            "transitions": {"type": "array", "items": _TRANSITION_PROP},
            "mermaid": {"type": "string", "description": "等价 stateDiagram-v2 源（可选，渲染辅助）"},
        },
        ("states",),
    ),
    "code": _schema(
        "code",
        "代码块：`text` 即代码原文（md/文本类原样，不做去标签）",
        {
            "language": {"type": "string", "description": "围栏语言标识（如 sv, c, json）"},
            "fragment": _FRAGMENT_PROP,
        },
        (),
    ),
    "example": _schema("example", "示例（非规范性但可追溯）", {"fragment": _FRAGMENT_PROP}, ()),
    "note": _schema(
        "note",
        "注释/说明；亦为未映射块的兜底原子（design_doc §6.1：降级保留，不丢弃）",
        {"fragment": _FRAGMENT_PROP},
        (),
    ),
    "cross_ref": _schema(
        "cross_ref",
        "交叉引用原子：指向本文档节点或外部文档节点（refs 边的原子形态）",
        {
            "ref_kind": {"enum": ["traces_to", "see_also", "composes_from", "source_ref"]},
            "target_doc_id": {"type": "string", "minLength": 1, "description": "目标 doc_id；外部叶引用为 'EXT:<uri>'"},
            "target_node_id": {"type": "string", "format": "uuid"},
            "target_anchor": {"type": "string"},
        },
        ("ref_kind", "target_doc_id"),
    ),
}
"""八类原子 + 2 变体的 JSON Schema（key = `schemas.type_name`，§4）。"""


class UnknownAtomTypeError(ValueError):
    """请求的 atom_type 无注册 schema（REQ-M01-F01：无 schema 的写入被拒）。"""


def get_atom_schema(atom_type: str) -> dict[str, Any]:
    """取 atom_type 的 JSON Schema；未注册（含拼错）→ :class:`UnknownAtomTypeError`。

    变体以 ``"<atom>.<variant>"`` 形式独立注册（``table.register_field``）。
    """
    try:
        return ATOM_SCHEMAS[atom_type]
    except KeyError:
        known = ", ".join(sorted(ATOM_SCHEMAS))
        raise UnknownAtomTypeError(f"未注册的 atom_type：{atom_type!r}；已注册：{known}") from None


# ── content.text 派生（A10/R5：M01 保证一切节点 content.text 非空）────────

_TAG_RE = re.compile(r"<[a-zA-Z!/][^>]*>")
_ROW_SEPARATORS = ("tr",)
_BLOCK_SEPARATORS = ("p", "div", "li", "table", "section", "blockquote")
_CELL_SEPARATORS = ("td", "th")


class _HtmlTextExtractor(HTMLParser):
    """HTML 片段 → 纯文本：按文档序收集文本，单元格以空格、行以换行分隔。"""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("br", "hr"):
            self._parts.append(" ")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag in _CELL_SEPARATORS:
            self._parts.append(" ")
        elif tag in _ROW_SEPARATORS or tag in _BLOCK_SEPARATORS:
            self._parts.append("\n")

    def handle_data(self, data: str) -> None:
        self._parts.append(data)

    def text(self) -> str:
        lines = [" ".join(line.split()) for line in "".join(self._parts).split("\n")]
        return "\n".join(line for line in lines if line)


def html_to_text(fragment: str) -> str:
    """HTML 片段 → 纯文本（去标签；单元格按行列序以空格拼接，行间换行）。"""
    parser = _HtmlTextExtractor()
    parser.feed(fragment)
    parser.close()
    return parser.text()


def _looks_like_html(text: str) -> bool:
    return bool(_TAG_RE.search(text))


def derive_text(atom_type: str, content: Mapping[str, Any]) -> str:
    """生成 ``content.text``（A10/R5）——该字段的**唯一生成口径**，写入前必调。

    - 表格类（``table`` / ``table.register_field``）：由 ``fragment``（原样 HTML）去标签，
      单元格按行列序拼接；
    - ``cross_ref``：取可见引用文本，缺省退化为 ``target_anchor`` / ``target_doc_id``；
    - ``figure.state_machine``：无 ``text``/``fragment`` 时由状态集合与迁移集合拼接；
    - 其余原子：``text`` 原样返回；缺 ``text`` 时用 ``fragment``（HTML 则去标签，md/文本原样）。

    :raises UnknownAtomTypeError: ``atom_type`` 无注册 schema（REQ-M01-F01）。
    :raises ValueError: 派生结果为空——M01 保证 `content.text` 非空，空值即写入错误。
    """
    if atom_type not in ATOM_SCHEMAS:
        raise UnknownAtomTypeError(f"未注册的 atom_type：{atom_type!r}；无 schema 的类型不得写入")

    if atom_type in TABLE_ATOMS:
        fragment = content.get("fragment")
        derived = html_to_text(str(fragment)) if fragment else ""
    elif atom_type == "cross_ref":
        derived = str(content.get("text") or content.get("target_anchor") or content.get("target_doc_id") or "")
    else:
        text = content.get("text")
        fragment = content.get("fragment")
        if text:
            derived = str(text)
        elif atom_type == "figure.state_machine" and not fragment:
            states = [str(state) for state in content.get("states") or ()]
            transitions = [
                f"{item.get('from')}->{item.get('to')}"
                for item in content.get("transitions") or ()
                if isinstance(item, Mapping)
            ]
            derived = " ".join([*states, *transitions])
        elif fragment:
            raw = str(fragment)
            derived = html_to_text(raw) if _looks_like_html(raw) else raw
        else:
            derived = ""

    if not derived.strip():
        raise ValueError(f"{atom_type} 的 content.text 派生为空：请提供 text/fragment（A10：content.text 非空）")
    return derived
