"""M03 frontmatter 解析：C5 十七字段 → :class:`~agenticdocer.model.DocIn`。

权威来源：`architecture_specification.md` §3 M03、§6「frontmatter → docs 映射（A22，C5 十七字段）」；
`spec/README.md`「frontmatter 规范（v2）」（**语料真实形态**：17 字段，含 spec 专属 4 项与
GigaRAG 流水线溯源 5 项；`ingested_at` 由摄入脚本幂等追加，不属必填）。

映射（§6 原样落地）：

======================  ==================================================
frontmatter             目标
======================  ==================================================
``title``               ``docs.title``
``spec_id``             ``docs.doc_id``（`SPEC-*`）
``spec_type``           ``docs.doc_type``（`standard`/`lang`/`tool-manual`/`product`/`safety`）
``source``              ``docs.source_ref``（原始 PDF 路径）
``status``              ``docs.status``（`approved`→approved、`review`→reviewed、`draft`→draft）
其余 12 字段            ``docs.meta`` JSONB **全量保真**（+ 稳定派生键 `doc_slug`）
======================  ==================================================

必填校验口径 = `model.doc_types.C5_META_FIELDS`（P5 单点：M01 定义、M03 消费、M09A 复用），
缺字段即 `ValidationError`（→ 422），不落地半份元数据。
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

import yaml

from agenticdocer.model import C5_META_FIELDS, DOC_TYPES, DocIn, DocStatus, missing_required_meta
from agenticdocer.store import ValidationError

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

    # ---------------------------------------------------------------- 映射

    @property
    def doc_id(self) -> str:
        return str(self.fields["spec_id"])

    @property
    def doc_type(self) -> str:
        return str(self.fields["spec_type"])

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
        """`docs.meta`：frontmatter 全量保真 + 稳定派生键（不含时间戳，保证重复导入幂等）。"""
        return {**self.fields, "doc_slug": self.doc_slug}

    @property
    def doc_meta(self) -> dict[str, Any]:
        """`ParseResult.doc_meta`：`meta` + 映射出的文档级字段（供提交期重建 `DocIn`）。"""
        return {
            "doc_slug": self.doc_slug,
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
    """解析 + 校验 frontmatter（C5 十七字段 + `spec_type`/`status` 取值域）。

    :raises ValidationError: 缺必填字段、`spec_type` 不在 `DOC_TYPES`、`status` 非法。
    """
    fields, body, body_start = split_frontmatter(text)
    missing = [name for name in C5_META_FIELDS if name not in fields]
    if missing:
        raise ValidationError(
            f"frontmatter 缺 C5 必填字段 {missing}（§6 十七字段；doc_slug={doc_slug}）",
            entity="doc",
            entity_id=str(fields.get("spec_id") or doc_slug),
        )
    doc_type = str(fields["spec_type"])
    if doc_type not in DOC_TYPES:
        raise ValidationError(
            f"spec_type={doc_type!r} 不在取值域 {list(DOC_TYPES)}（A22）",
            entity="doc",
            entity_id=str(fields["spec_id"]),
        )
    extra_missing = missing_required_meta(doc_type, fields)
    if extra_missing:
        raise ValidationError(
            f"doc_type={doc_type!r} 的组合规则另需字段 {extra_missing}（REQ-M01-F03）",
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
    return Frontmatter(
        fields=fields,
        body=body,
        body_start=body_start,
        doc_slug=doc_slug,
        source_path=source_path,
    )


def doc_in_from_meta(doc_meta: dict[str, Any]) -> DocIn:
    """`ParseResult.doc_meta` → :class:`DocIn`（提交期重建，proposals.json 往返用）。"""
    frontmatter = doc_meta.get("frontmatter")
    if not isinstance(frontmatter, dict):
        raise ValidationError("doc_meta 缺少 frontmatter 全量字段（无法重建 DocIn）", entity="doc")
    return DocIn(
        doc_id=str(doc_meta["doc_id"]),
        doc_type=str(doc_meta["doc_type"]),
        title=str(doc_meta["title"]),
        meta={**frontmatter, "doc_slug": str(doc_meta.get("doc_slug", ""))},
        source_ref=None if doc_meta.get("source_ref") is None else str(doc_meta["source_ref"]),
    )
