"""M03 vPlan / UCIS 导入器（方案 C §4，idea.md §4.3/§9）。

**对齐目标**：Accellera **UCIS** / Cadence vManager、Siemens Questa 的 **vPlan XML**——
层级 `feature → sub_feature → coverage_item → test → status`，映射到本系统原子变体
`table.coverage_matrix`（schema 单点在 :mod:`agenticdocer.model.atoms`，P5）。

**范围与验证边界（映射表 §5，重要）**：`spec/standards/` 中**不存在真实 vPlan/UCIS 文件**，
故本模块的正确定义为「**导入/导出接口**」，其验证 = **合成 XML 样例**（测试内手写，
注释标注「合成样例，非真实语料」）+ 逐字段断言。**不得**据此声称端到端验证。

**解析子集**（vPlan XML 的可运行子集，非完整 UCIS）：
根元素 `<vPlan>`（接受 `vplan`/`verification_plan`，大小写不敏感；命名空间前缀忽略），
其下 `<feature>` / `<sub_feature>` / `<coverage_item>` / `<test>` 逐层嵌套，元素名经
`name` 属性（缺省取 `<name>`/`<title>` 子元素文本）标识，`status` 属性可选。

**层级缺位与覆盖缺口**（不静默丢弃，与 A10/ADR-006 口径一致）：

- 缺某层元素（如 `feature` 直接挂 `coverage_item`）→ 该列取 :data:`UNNAMED`；
- 覆盖项无测试（覆盖缺口）→ 行的 `test` 记为 :data:`UNASSIGNED_TEST` 哨兵值
  （`matrix` 行的五个字段在 schema 中均要求非空字符串，缺口必须显式留痕），
  原值 ``None`` 保留在 :attr:`CoverageRow.test` 上，可由 :attr:`VPlan.coverage_gaps` 取回；
- `status` 缺省 → :data:`UNKNOWN_STATUS`（覆盖状态取 `coverage_item`，其次取 `test`）。
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from html import escape
from typing import Any, Final
from xml.etree import ElementTree

import jsonschema

from agenticdocer.model import get_atom_schema
from agenticdocer.store import ValidationError

from .parser import atom_content, table_meta

__all__ = [
    "COVERAGE_MATRIX_ATOM",
    "VPLAN_ROOT_TAGS",
    "UNNAMED",
    "UNASSIGNED_TEST",
    "UNKNOWN_STATUS",
    "MATRIX_FIELDS",
    "CoverageRow",
    "VPlan",
    "parse_vplan",
    "matrix_rows",
    "coverage_matrix_content",
    "coverage_matrix_atom",
]

COVERAGE_MATRIX_ATOM: Final = "table.coverage_matrix"
"""vPlan/UCIS 层级落到本系统的原子变体名（schema 见 `model.atoms.ATOM_SCHEMAS`）。"""

VPLAN_ROOT_TAGS: Final = ("vplan", "verification_plan", "ucis")
"""可接受的根元素名（小写比较；`vPlan` 大小写不敏感）。"""

UNNAMED: Final = "(unnamed)"
"""层级缺位哨兵：缺 `feature`/`sub_feature`/`coverage_item` 元素时占位（不丢行）。"""

UNASSIGNED_TEST: Final = "(unassigned)"
"""覆盖缺口哨兵：覆盖项尚无测试（schema 的 `test` 要求非空字符串）。"""

_FORBIDDEN_DECL_MARKERS: Final = ("<!doctype", "<!entity")
UNKNOWN_STATUS: Final = "unknown"
"""`status` 未标注时的取值。"""

MATRIX_FIELDS: Final = ("feature", "sub_feature", "coverage_item", "test", "status")
"""`table.coverage_matrix` 行字段（与 M01 变体 schema 同序；schema 定义仍在 model）。"""

_LEVELS: Final = ("feature", "sub_feature", "coverage_item", "test")
_NAME_CHILD_TAGS: Final = ("name", "title")
_XML_DECL_RE: Final = ("<!doctype", "<!entity")


def _local(tag: str) -> str:
    """去掉命名空间前缀：``{uri}feature`` → ``feature``（小写）。"""
    return tag.rsplit("}", 1)[-1].strip().lower()


def _label(element: ElementTree.Element) -> str:
    """元素名：`name` 属性 → `<name>`/`<title>` 子元素文本 → 空串。"""
    name = element.get("name")
    if name is not None and name.strip():
        return name.strip()
    for child in element:
        if _local(child.tag) in _NAME_CHILD_TAGS and (child.text or "").strip():
            return (child.text or "").strip()
    return ""


def _status(element: ElementTree.Element) -> str:
    return (element.get("status") or "").strip()


@dataclass(frozen=True)
class CoverageRow:
    """一条覆盖矩阵行 = 一个 `coverage_item` × 一个 `test`（无测试则单行缺口）。"""

    feature: str
    sub_feature: str
    coverage_item: str
    test: str | None
    """测试名；``None`` = 该覆盖项尚无测试（覆盖缺口，见 :data:`UNASSIGNED_TEST`）。"""

    status: str
    """覆盖状态：`coverage_item` 的 `status` → 退 `test` 的 `status` → :data:`UNKNOWN_STATUS`。"""

    @property
    def is_gap(self) -> bool:
        return self.test is None

    def as_matrix_row(self) -> dict[str, str]:
        """→ `content.matrix` 的行（缺口以 :data:`UNASSIGNED_TEST` 落位，字段齐备非空）。"""
        return {
            "feature": self.feature,
            "sub_feature": self.sub_feature,
            "coverage_item": self.coverage_item,
            "test": self.test if self.test is not None else UNASSIGNED_TEST,
            "status": self.status,
        }


@dataclass(frozen=True)
class VPlan:
    """一份 vPlan 的解析结果（确定性：同输入 → 同行序）。"""

    name: str
    rows: tuple[CoverageRow, ...]
    format: str = "vplan"
    """来源格式（`vplan`/`ucis`；写入 frontmatter `verification_plan_format`）。"""

    @property
    def coverage_gaps(self) -> tuple[CoverageRow, ...]:
        """无测试的覆盖项（`test is None`）——缺口在矩阵中留痕，此处可取回原值。"""
        return tuple(row for row in self.rows if row.is_gap)

    def matrix_rows(self) -> tuple[dict[str, str], ...]:
        return tuple(row.as_matrix_row() for row in self.rows)

    def to_xml(self) -> str:
        """反向生成 vPlan XML（按行重建层级；`status` 落在唯一可还原的位置）。

        反向生成的 `status` 位置：行有测试 → 落在 `<test>`；行是缺口 → 落在
        `<coverage_item>`。故 ``parse_vplan(plan.to_xml())`` 与原行的五字段逐字段相等
        （存在测试的行不重复写 `coverage_item@status`，避免覆盖逐行状态）。
        """
        groups: dict[tuple[str, str], dict[str, list[CoverageRow]]] = {}
        for row in self.rows:
            groups.setdefault((row.feature, row.sub_feature), {}).setdefault(
                row.coverage_item, []
            ).append(row)
        root = ElementTree.Element("vPlan", {"name": self.name})
        for (feature, sub_feature), items in groups.items():
            feature_el = ElementTree.SubElement(root, "feature", {"name": feature})
            sub_el = ElementTree.SubElement(feature_el, "sub_feature", {"name": sub_feature})
            for item, item_rows in items.items():
                item_el = ElementTree.SubElement(sub_el, "coverage_item", {"name": item})
                tested = [row for row in item_rows if row.test is not None]
                if not tested:
                    item_el.set("status", item_rows[0].status)
                    continue
                for row in tested:
                    ElementTree.SubElement(
                        item_el, "test", {"name": row.test or "", "status": row.status}
                    )
        ElementTree.indent(root, space="  ")
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + ElementTree.tostring(
            root, encoding="unicode"
        )


def _rows_of(
    feature: ElementTree.Element,
) -> Iterator[CoverageRow]:
    """一个 `feature` 元素 → 其下的全部行（逐层展开，层级缺位以 :data:`UNNAMED` 占位）。"""
    feature_name = _label(feature) or UNNAMED
    subs = [child for child in feature if _local(child.tag) == "sub_feature"]
    if not subs:
        yield from _rows_of_scope(feature, feature_name, UNNAMED)
        return
    for sub in subs:
        yield from _rows_of_scope(sub, feature_name, _label(sub) or UNNAMED)


def _rows_of_scope(
    scope: ElementTree.Element, feature_name: str, sub_feature: str
) -> Iterator[CoverageRow]:
    """`feature`/`sub_feature` 作用域 → 行（`coverage_item` 可缺位，测试可缺位）。"""
    items = [child for child in scope if _local(child.tag) == "coverage_item"]
    if not items:
        tests = [child for child in scope if _local(child.tag) == "test"]
        if not tests:
            return
        for test in tests:
            yield CoverageRow(
                feature=feature_name,
                sub_feature=sub_feature,
                coverage_item=UNNAMED,
                test=_label(test) or None,
                status=_status(test) or UNKNOWN_STATUS,
            )
        return
    for item in items:
        item_name = _label(item) or UNNAMED
        item_status = _status(item)
        tests = [child for child in item if _local(child.tag) == "test"]
        if not tests:
            yield CoverageRow(
                feature=feature_name,
                sub_feature=sub_feature,
                coverage_item=item_name,
                test=None,
                status=item_status or UNKNOWN_STATUS,
            )
            continue
        for test in tests:
            yield CoverageRow(
                feature=feature_name,
                sub_feature=sub_feature,
                coverage_item=item_name,
                test=_label(test) or None,
                status=item_status or _status(test) or UNKNOWN_STATUS,
            )


def parse_vplan(xml_text: str, *, name: str | None = None) -> VPlan:
    """vPlan/UCIS XML → :class:`VPlan`（支持子集见模块 docstring）。

    :raises ValidationError: XML 不合法、根元素名不在 :data:`VPLAN_ROOT_TAGS`、
        或文档内不含任何 `feature`（空计划即格式错误，不产出空矩阵）。
    """
    if any(marker in xml_text.lower() for marker in _FORBIDDEN_DECL_MARKERS):
        # 不给外部实体/DTD 留入口（stdlib ElementTree 不解析外部实体，但先拒为快）
        raise ValidationError("vPlan XML 含 DOCTYPE/ENTITY 声明（拒绝解析）", entity="doc")
    try:
        root = ElementTree.fromstring(xml_text)
    except ElementTree.ParseError as exc:
        raise ValidationError(f"vPlan XML 解析失败：{exc}", entity="doc") from exc
    root_tag = _local(root.tag)
    if root_tag not in VPLAN_ROOT_TAGS:
        raise ValidationError(
            f"vPlan 根元素须为 {list(VPLAN_ROOT_TAGS)} 之一，实为 {root.tag!r}", entity="doc"
        )
    features = [child for child in root if _local(child.tag) == "feature"]
    if not features:
        raise ValidationError("vPlan 未含任何 <feature> 元素（空计划）", entity="doc")
    rows: list[CoverageRow] = []
    for feature in features:
        rows.extend(_rows_of(feature))
    return VPlan(
        name=name or (root.get("name") or "").strip() or UNNAMED,
        rows=tuple(rows),
        format="ucis" if root_tag == "ucis" else "vplan",
    )


def matrix_rows(rows: Iterable[CoverageRow]) -> tuple[dict[str, str], ...]:
    """行集合 → `content.matrix`（字段齐备、值非空，符合 M01 变体 schema）。"""
    return tuple(row.as_matrix_row() for row in rows)


def _fragment(rows: Sequence[dict[str, str]]) -> str:
    """矩阵行 → 原样 HTML 表格片段（E1-a：表格原子以 `fragment` 直通渲染）。"""
    header = "".join(f"<th>{escape(field)}</th>" for field in MATRIX_FIELDS)
    body = "".join(
        "<tr>" + "".join(f"<td>{escape(row[field])}</td>" for field in MATRIX_FIELDS) + "</tr>"
        for row in rows
    )
    return f"<table><thead><tr>{header}</tr></thead><tbody>{body}</tbody></table>"


def coverage_matrix_content(rows: Sequence[CoverageRow]) -> dict[str, Any]:
    """行集合 → `table.coverage_matrix` 的 `content`（`text` 由 M01 单点派生）。

    :raises ValidationError: 行集合为空，或 `content` 不合 M01 变体 schema
        （REQ-M01-F01：无 schema/不合 schema 不得写入）。
    """
    if not rows:
        raise ValidationError("coverage_matrix 需至少一行（schema: matrix minItems 1）", entity="doc")
    matrix = [row.as_matrix_row() for row in rows]
    fragment = _fragment(matrix)
    content = atom_content(
        COVERAGE_MATRIX_ATOM, fragment=fragment, meta=table_meta(fragment), matrix=matrix
    )
    _validate(content)
    return content


def coverage_matrix_atom(rows: Sequence[CoverageRow]) -> dict[str, Any]:
    """行集合 → 可写入的原子提议（`atom_type` + `format` + `content`）。

    `format="html"`：片段是真实 `<table>` 标记（E1-a 要求 `format` 与片段形态一致）。
    """
    return {
        "atom_type": COVERAGE_MATRIX_ATOM,
        "format": "html",
        "content": coverage_matrix_content(rows),
    }


def _validate(content: dict[str, Any]) -> None:
    """按 M01 变体 schema 校验 `content`（P5：schema 只在 model 定义，此处只消费）。"""
    try:
        jsonschema.validate(instance=content, schema=get_atom_schema(COVERAGE_MATRIX_ATOM))
    except jsonschema.ValidationError as exc:
        path = "/".join(str(part) for part in exc.absolute_path) or "<root>"
        raise ValidationError(
            f"{COVERAGE_MATRIX_ATOM} content 不合 schema（{path}: {exc.message}）",
            entity="atom",
            entity_id=COVERAGE_MATRIX_ATOM,
        ) from exc
