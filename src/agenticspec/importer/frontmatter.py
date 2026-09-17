"""M03 frontmatter 解析：C5 十七字段 → :class:`~agenticspec.model.DocIn`。

权威来源：`architecture_specification.md` §3 M03、§6「frontmatter → docs 映射（A22，C5 十七字段）」；
`spec/README.md`「frontmatter 规范（v2）」（**语料真实形态**：17 字段，含 spec 专属 4 项与
GigaRAG 流水线溯源 5 项；`ingested_at` 由摄入脚本幂等追加，不属必填）。

映射（§6 原样落地）：

======================  ==================================================
frontmatter             目标
======================  ==================================================
``title``               ``docs.title``
``spec_id``             ``docs.doc_id``（`SPEC-*`）
``spec_type``           ``docs.doc_type``（`standard`/`lang`/`tool-manual`/`product`/`safety`，
                        或映射表 §2 的类型别名——经 :func:`doc_type_map.resolve_doc_type` 归一）
``source``              ``docs.source_ref``（原始 PDF 路径）
``status``              ``docs.status``（`approved`→approved、`review`→reviewed、`draft`→draft）
其余 12 字段            ``docs.meta`` JSONB **全量保真**（+ 稳定派生键 `doc_slug`/`doc_subtype`）
======================  ==================================================

必填校验口径 = `model.doc_types.C5_META_FIELDS`（P5 单点：M01 定义、M03 消费、M09A 复用），
缺字段即 `ValidationError`（→ 422），不落地半份元数据。
`doc_type` 的细粒度判定（idea.md 30+ 类型 → 5 个 `doc_type`）与 `product` 大类的细分
（`meta.doc_subtype`）单点在 :mod:`agenticspec.importer.doc_type_map`（映射表 §2 的机器可读
形式）；`verification-plan` 子类型另需 `verification_plan_format`（映射表 §4）。
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

import yaml

from agenticspec.model import C5_META_FIELDS, DOC_TYPES, DocIn, DocStatus, missing_required_meta
from agenticspec.store import ValidationError

from .doc_type_map import (
    RESOLVABLE_KEYS,
    VERIFICATION_PLAN_FORMATS,
    VERIFICATION_PLAN_SUBTYPE,
    UnknownDocTypeError,
    invalid_verification_plan_format,
    missing_verification_plan_meta,
    resolve_doc_type,
    subtypes_for,
)

__all__ = [
    "FRONTMATTER_DELIMITER",
    "STATUS_MAP",
    "Frontmatter",
    "split_frontmatter",
    "parse_frontmatter",
    "doc_in_from_meta",
    "frontmatter_field_names",
]

FRONTMATTER_DELIMITER: Final = "---"

STATUS_MAP: dict[str, DocStatus] = {
    "approved": "approved",
    "review": "reviewed",
    "reviewed": "reviewed",
    "draft": "draft",
}
"""mySkills `status` → `docs.status`（§6「approved→approved 等」）。"""


@dataclass(frozen=True)
class Frontmatter:
    """解析结果：全量字段 + 正文 + 定位信息。"""

    fields: dict[str, Any]
    """JSON 安全的全量 frontmatter（YAML 日期等已转 ISO 字符串）。"""

    body: str
    """frontmatter 之后的正文（含结尾换行，逐字节与源一致）。"""

    body_start: int
    """正文首行的**源文件行号**（1 基）——块行号的基准。"""

    doc_slug: str
    source_path: Path | None

    resolved_doc_type: str = "standard"
    """`spec_type` 归一后的 `doc_type`（`model.DOC_TYPES` 之一；映射表 §2）。"""

    resolved_doc_subtype: str | None = None
    """`meta.doc_subtype`：`product` 大类等的细分；无细分为 ``None``（映射表 §2 收敛原则）。"""

    # ---------------------------------------------------------------- 映射

    @property
    def doc_id(self) -> str:
        return str(self.fields["spec_id"])

    @property
    def doc_type(self) -> str:
        return self.resolved_doc_type

    @property
    def doc_subtype(self) -> str | None:
        """细分（`meta.doc_subtype`）：`product` 大类靠它区分架构/MAS/寄存器手册等。"""
        return self.resolved_doc_subtype

    @property
    def title(self) -> str:
        return str(self.fields["title"])

    @property
    def source_ref(self) -> str | None:
        value = self.fields.get("source")
        return None if value is None else str(value)

    @property
    def doc_status(self) -> DocStatus:
        return STATUS_MAP[str(self.fields.get("status", "draft")).strip().lower()]

    @property
    def meta(self) -> dict[str, Any]:
        """`docs.meta`：frontmatter 全量保真 + 稳定派生键（不含时间戳，保证重复导入幂等）。

        派生键：`doc_slug`（恒有）；`doc_subtype`（判定/声明出细分时）——后者同时是
        `product` 组合规则的必填项（映射表 §3）。
        """
        meta = {**self.fields, "doc_slug": self.doc_slug}
        if self.resolved_doc_subtype is not None:
            meta["doc_subtype"] = self.resolved_doc_subtype
        return meta

    @property
    def doc_meta(self) -> dict[str, Any]:
        """`ParseResult.doc_meta`：`meta` + 映射出的文档级字段（供提交期重建 `DocIn`）。"""
        return {
            "doc_slug": self.doc_slug,
            "doc_subtype": self.resolved_doc_subtype,
            "doc_id": self.doc_id,
            "doc_type": self.doc_type,
            "title": self.title,
            "source_ref": self.source_ref,
            "source_path": None if self.source_path is None else str(self.source_path),
            "doc_status": self.doc_status,
            "frontmatter": dict(self.fields),
        }

    def doc_in(self) -> DocIn:
        """→ :class:`DocIn`（`meta` 全量保真，`source_ref` 来自 `source`）。"""
        return DocIn(
            doc_id=self.doc_id,
            doc_type=self.doc_type,
            title=self.title,
            meta=self.meta,
            source_ref=self.source_ref,
        )


def frontmatter_field_names(fields: dict[str, Any]) -> list[str]:
    """字段名清单（诊断/报告用）。"""
    return sorted(fields)


def _jsonable(value: Any) -> Any:
    """YAML 标量 → JSON 安全值（`datetime.date` 等转 ISO 字符串，保真不丢信息）。"""
    if isinstance(value, (_dt.datetime, _dt.date, _dt.time)):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def split_frontmatter(text: str) -> tuple[dict[str, Any], str, int]:
    """切出 frontmatter → ``(fields, body, body_start_line)``。

    `body_start_line` 为正文首行的源文件行号（1 基）；无 frontmatter 时抛
    :class:`ValidationError`（REQ-M03-F01：frontmatter 字段按 C5 规范校验——缺失即无法校验）。
    """
    lines = text.split("\n")
    opening = 0
    while opening < len(lines) and not lines[opening].strip():
        opening += 1
    if opening >= len(lines) or lines[opening].strip() != FRONTMATTER_DELIMITER:
        raise ValidationError(
            "缺少 frontmatter（首行须为 '---'）；C5 十七字段无从校验",
            entity="doc",
        )
    closing = None
    for index in range(opening + 1, len(lines)):
        if lines[index].strip() == FRONTMATTER_DELIMITER:
            closing = index
            break
    if closing is None:
        raise ValidationError("frontmatter 未闭合（缺结尾 '---'）", entity="doc")
    raw = "\n".join(lines[opening + 1 : closing])
    try:
        loaded = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise ValidationError(f"frontmatter YAML 解析失败：{exc}", entity="doc") from exc
    if loaded is None:
        loaded = {}
    if not isinstance(loaded, dict):
        raise ValidationError(f"frontmatter 须为映射（key: value），实为 {type(loaded).__name__}", entity="doc")
    fields = {str(key): _jsonable(value) for key, value in loaded.items()}
    body = "\n".join(lines[closing + 1 :])
    return fields, body, closing + 2


def parse_frontmatter(
    text: str,
    *,
    doc_slug: str,
    source_path: Path | None = None,
) -> Frontmatter:
    """解析 + 校验 frontmatter（C5 十七字段 + `spec_type` 归一 + 组合规则必填字段）。

    `spec_type` 先经 :func:`doc_type_map.resolve_doc_type` 归一（5 个 `doc_type` 值、映射表 §2
    的 slug 与别名均可写）；`product` 大类的细分入 `meta.doc_subtype`（不新增 `doc_type`）。

    :raises ValidationError: 缺必填字段、`spec_type` 无法归一、`doc_subtype` 非法、
        组合规则（`missing_required_meta`）缺字段、`verification_plan_format` 缺失/非法、
        `status` 非法。
    """
    fields, body, body_start = split_frontmatter(text)
    missing = [name for name in C5_META_FIELDS if name not in fields]
    if missing:
        raise ValidationError(
            f"frontmatter 缺 C5 必填字段 {missing}（§6 十七字段；doc_slug={doc_slug}）",
            entity="doc",
            entity_id=str(fields.get("spec_id") or doc_slug),
        )
    raw_spec_type = str(fields["spec_type"])
    try:
        resolved = resolve_doc_type(raw_spec_type)
    except UnknownDocTypeError:
        raise ValidationError(
            f"spec_type={raw_spec_type!r} 不在取值域 {list(DOC_TYPES)}（A22），"
            f"亦非映射表 §2 的已知类型 slug/别名（合法写法共 {len(RESOLVABLE_KEYS)} 个）",
            entity="doc",
            entity_id=str(fields["spec_id"]),
        ) from None
    doc_type = resolved.doc_type
    declared_subtype = fields.get("doc_subtype")
    if declared_subtype is not None:
        doc_subtype: str | None = str(declared_subtype).strip()
        known_subtypes = subtypes_for(doc_type)
        if doc_subtype not in known_subtypes:
            raise ValidationError(
                f"doc_subtype={declared_subtype!r} 不在 doc_type={doc_type!r} 的细分取值域"
                f" {list(known_subtypes)}（映射表 §2 收敛原则：细分只加 `meta`，不新增 `doc_type`）",
                entity="doc",
                entity_id=str(fields["spec_id"]),
            )
    else:
        doc_subtype = resolved.doc_subtype
    frontmatter = Frontmatter(
        fields=fields,
        body=body,
        body_start=body_start,
        doc_slug=doc_slug,
        source_path=source_path,
        resolved_doc_type=doc_type,
        resolved_doc_subtype=doc_subtype,
    )
    meta = frontmatter.meta
    extra_missing = missing_required_meta(doc_type, meta)
    if extra_missing:
        raise ValidationError(
            f"doc_type={doc_type!r} 的组合规则另需字段 {extra_missing}（REQ-M01-F03）",
            entity="doc",
            entity_id=str(fields["spec_id"]),
        )
    if doc_subtype == VERIFICATION_PLAN_SUBTYPE:
        plan_missing = missing_verification_plan_meta(meta)
        if plan_missing:
            raise ValidationError(
                f"doc_subtype={VERIFICATION_PLAN_SUBTYPE!r} 另需字段 {plan_missing}"
                f"（映射表 §4：UCIS/vPlan 对齐）",
                entity="doc",
                entity_id=str(fields["spec_id"]),
            )
        bad_format = invalid_verification_plan_format(meta)
        if bad_format is not None:
            raise ValidationError(
                f"verification_plan_format={bad_format!r} 非法"
                f"（合法值 {list(VERIFICATION_PLAN_FORMATS)}；映射表 §4）",
                entity="doc",
                entity_id=str(fields["spec_id"]),
            )
    status_key = str(fields.get("status", "")).strip().lower()
    if status_key not in STATUS_MAP:
        raise ValidationError(
            f"frontmatter status={fields.get('status')!r} 无法映射到 docs.status"
            f"（合法值：{sorted(STATUS_MAP)}）",
            entity="doc",
            entity_id=str(fields["spec_id"]),
        )
    return frontmatter


def doc_in_from_meta(doc_meta: dict[str, Any]) -> DocIn:
    """`ParseResult.doc_meta` → :class:`DocIn`（提交期重建，proposals.json 往返用）。

    派生键 `doc_slug`/`doc_subtype` 与 :meth:`Frontmatter.meta` 逐键一致（往返不丢细分）。
    """
    frontmatter = doc_meta.get("frontmatter")
    if not isinstance(frontmatter, dict):
        raise ValidationError("doc_meta 缺少 frontmatter 全量字段（无法重建 DocIn）", entity="doc")
    meta = {**frontmatter, "doc_slug": str(doc_meta.get("doc_slug", ""))}
    if doc_meta.get("doc_subtype") is not None:
        meta["doc_subtype"] = str(doc_meta["doc_subtype"])
    return DocIn(
        doc_id=str(doc_meta["doc_id"]),
        doc_type=str(doc_meta["doc_type"]),
        title=str(doc_meta["title"]),
        meta=meta,
        source_ref=None if doc_meta.get("source_ref") is None else str(doc_meta["source_ref"]),
    )
