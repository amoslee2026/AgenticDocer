"""M09A schema 校验引擎（REQ-M09-F01；阶段 1 随 M01 交付）。

职责：把「原子内容是否合法」变成**可机械验证**的违规清单（`Violation{rule_id, path,
message, fix_hint}`），供两条路径消费：

* M03 导入提议校验（`parse_markdown` → 审核 → `commit_document`，REQ-M03-F03）；
* M06/M07 节点写入校验（`POST/PATCH /api/v1/nodes`，触发 M06 lint 自修复闭环，
  REQ-M06-F02：违规清单含**修复建议**，agent 依 `fix_hint` 修正后重试）。

判定口径单点（P5）
------------------

* schema 一律取自 M01 `ATOM_SCHEMAS`（八类 + 2 变体，与 `schemas` 表种子同源）；
* `content.text` 的**唯一生成口径**是 M01 `derive_text`，故「text 是否等于派生结果」
  是可直接机检的不变量（本模块 `A10.content.text.drift`）；
* 锚形态取自 M01 `assign_anchors`/`make_anchor`（`<doc_id>#…`），本模块只**校验**不构造。

规则集（`rule_id` 与 M03 的规则库口径唯一；同一判据全局只有一个 id）
-------------------------------------------------------------------

| rule_id | 判据 | 适用 |
|---|---|---|
| `M09A.atom.unknown` | `atom_type` 无注册 schema（M01 `ATOM_SCHEMAS`） | 提议 / 写入 |
| `M09A.atom.schema` | `content` 不满足该原子的 JSON Schema（draft 2020-12，额外字段拒绝） | 提议 / 写入 |
| `A10.content.text` | `content.text` 缺失/非字符串/空白（FTS 生成列依赖） | 提议 / 写入 |
| `A10.content.text.drift` | `content.text` ≠ `derive_text(atom_type, content)`（归一后比较） | 提议 / 写入 |
| `A10.content.text.empty` | 派生投影为空（`fragment` 去标签后无文本） | 提议 / 写入 |
| `M09A.anchor.doc_id` | 锚不以 `<doc_id>#` 起首（M01 锚构造口径） | 写入 |
| `M09A.node.parent_self` | `parent_node_id == node_id`（自指；ADR-009 外键降级后无 DB 兜底） | 写入 |
| `M09A.table.format` | 表格原子的 `format` 与 `fragment` 形态不符（E1-a：html `<table>` / md 管道表） | 写入 |
| `M09A.cross_ref.external_node` | `target_doc_id` 为外部叶（`EXT:`）却给了 `target_node_id` | 写入 |
| `M01.doc_type.atom` | `doc_type` 组合规则不允许该原子（调用方提供 `doc_type` 时） | 写入 |

`path` 口径：**相对被校验对象的字段路径**（点号 + 数组下标，落在 `content` 之外用
字段名），如 `content.meta.rows`、`content.fields[0].access`、`anchor`。调用方（M06）
可在响应里自行加锚前缀定位文档内位置。

无 schema 差异的判据不重复上报：schema 已报错时不再叠加 text 派生类判据（避免同一
根因产生多条违规，lint 闭环只应看到需要修的那一刻）。
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from functools import lru_cache
from typing import Any, Final

import jsonschema

from agenticdocer.model import (
    ATOM_SCHEMAS,
    TABLE_ATOMS,
    NodeIn,
    Violation,
    allowed_atom_types,
    derive_text,
    get_atom_schema,
    is_atom_allowed,
    normalize_body,
)

__all__ = [
    "RULE_ANCHOR_DOC_ID",
    "RULE_ATOM_SCHEMA",
    "RULE_ATOM_UNKNOWN",
    "RULE_CONTENT_TEXT",
    "RULE_CONTENT_TEXT_DRIFT",
    "RULE_CONTENT_TEXT_EMPTY",
    "RULE_CROSS_REF_EXTERNAL_NODE",
    "RULE_DOC_TYPE_ATOM",
    "RULE_PARENT_SELF",
    "RULE_TABLE_FORMAT",
    "RULES_9A",
    "validate_proposal",
    "validate_write",
]

# ── 规则 id（唯一登记处；调用方按 id 聚合修复任务，勿在别处再写字面量）────────

RULE_ATOM_UNKNOWN: Final = "M09A.atom.unknown"
RULE_ATOM_SCHEMA: Final = "M09A.atom.schema"
RULE_CONTENT_TEXT: Final = "A10.content.text"
RULE_CONTENT_TEXT_DRIFT: Final = "A10.content.text.drift"
RULE_CONTENT_TEXT_EMPTY: Final = "A10.content.text.empty"
RULE_ANCHOR_DOC_ID: Final = "M09A.anchor.doc_id"
RULE_PARENT_SELF: Final = "M09A.node.parent_self"
RULE_TABLE_FORMAT: Final = "M09A.table.format"
RULE_CROSS_REF_EXTERNAL_NODE: Final = "M09A.cross_ref.external_node"
RULE_DOC_TYPE_ATOM: Final = "M01.doc_type.atom"

RULES_9A: tuple[str, ...] = (
    RULE_ATOM_UNKNOWN,
    RULE_ATOM_SCHEMA,
    RULE_CONTENT_TEXT,
    RULE_CONTENT_TEXT_DRIFT,
    RULE_CONTENT_TEXT_EMPTY,
    RULE_ANCHOR_DOC_ID,
    RULE_PARENT_SELF,
    RULE_TABLE_FORMAT,
    RULE_CROSS_REF_EXTERNAL_NODE,
    RULE_DOC_TYPE_ATOM,
)
"""M09A 全部规则 id（机检清单：测试断言规则集自证）。"""


_TEXT_REQUIRED_MESSAGE: Final = "'text' is a required property"
"""jsonschema 对 `required: ["text"]` 的文案（`A10.content.text` 拥有该判据，故在此剔除）。"""

_EXTERNAL_PREFIX: Final = "EXT:"
_CLIP_CHARS: Final = 120


# ── schema 校验（每 atom_type 编译一次；整档 1 万条提议时避免重复编译）────────


@lru_cache(maxsize=None)
def _validator(atom_type: str) -> jsonschema.Draft202012Validator:
    return jsonschema.Draft202012Validator(get_atom_schema(atom_type))


def _dotted(path: Iterable[Any]) -> str:
    """jsonschema 错误路径 → 字段路径（``content.meta.rows`` / ``content.fields[0]``）。"""
    out = "content"
    for part in path:
        out += f"[{part}]" if isinstance(part, int) else f".{part}"
    return out


def _clip(text: str) -> str:
    flat = " ".join(str(text).split())
    return flat if len(flat) <= _CLIP_CHARS else f"{flat[:_CLIP_CHARS]}…"


def _schema_violations(atom_type: str, content: Mapping[str, Any]) -> list[Violation]:
    """JSON Schema 违规（每条 error 一条违规，路径指向出错字段）。

    schema 的 `'text' is a required property` 由 `A10.content.text` 拥有（见
    `_content_violations`），此处剔除以免同一根因产生两条违规。
    """
    validator = _validator(atom_type)
    violations: list[Violation] = []
    errors = sorted(validator.iter_errors(dict(content)), key=lambda error: list(error.path))
    for error in errors:
        if error.validator == "required" and error.message == _TEXT_REQUIRED_MESSAGE:
            continue
        violations.append(
            Violation(
                rule_id=RULE_ATOM_SCHEMA,
                path=_dotted(error.path),
                message=error.message,
                fix_hint=f"对照 ATOM_SCHEMAS[{atom_type!r}] 修正 content",
            )
        )
    return violations


def _missing_text_violation() -> Violation:
    return Violation(
        rule_id=RULE_CONTENT_TEXT,
        path="content.text",
        message="content.text 缺失或为空（FTS 生成列依赖）",
        fix_hint="由 M01 derive_text 生成后再写入",
    )


def _text_violations(atom_type: str, content: Mapping[str, Any]) -> list[Violation]:
    """`content.text` 判据（A10）：存在性优先，其后判与 `derive_text` 派生结果一致。"""
    text = content.get("text")
    if not isinstance(text, str) or not text.strip():
        return [_missing_text_violation()]
    try:
        derived = derive_text(atom_type, content)
    except ValueError:
        return [
            Violation(
                rule_id=RULE_CONTENT_TEXT_EMPTY,
                path="content.text",
                message=f"{atom_type} 的 text/fragment 派生为空（fragment 去标签后无文本）",
                fix_hint="补 content.fragment 或显式 content.text（A10：text 非空且为纯文本投影）",
            )
        ]
    if normalize_body(text) != normalize_body(derived):
        return [
            Violation(
                rule_id=RULE_CONTENT_TEXT_DRIFT,
                path="content.text",
                message=(
                    f"content.text 与 derive_text 派生结果不一致（P5 唯一口径）："
                    f"text={_clip(text)!r}，派生={_clip(derived)!r}"
                ),
                fix_hint=f"以 derive_text({atom_type!r}, content) 重算结果覆盖 content.text",
            )
        ]
    return []


def _content_violations(atom_type: str, content: Mapping[str, Any]) -> list[Violation]:
    """content 级判据编排（规则优先级见模块文档末段）。

    * `text` 缺失/空白 → 与 schema 违规**并列**报告（不同修复动作：补 schema 字段 vs 生成 text）；
    * `text` 在而 schema 不通过 → 只报 schema（形态未定，派生类判据无意义）；
    * schema 通过 → 判派生一致性（`drift` / `empty`）。
    """
    schema = _schema_violations(atom_type, content)
    text = _text_violations(atom_type, content)
    if text and text[0].rule_id == RULE_CONTENT_TEXT:
        return [*schema, *text]
    if schema:
        return schema
    return text


# ── M09A 对外入口（§3 M09）────────────────────────────────────────────────


def validate_proposal(atom_type: str, content: Mapping[str, Any]) -> list[Violation]:
    """提议级（阶段 1）schema 校验：`(atom_type, content)` → 违规清单。

    空清单 = 通过。违规按 `path` 定序（同一 content 的多次校验结果逐字段一致）。
    """
    if atom_type not in ATOM_SCHEMAS:
        known = ", ".join(sorted(ATOM_SCHEMAS))
        return [
            Violation(
                rule_id=RULE_ATOM_UNKNOWN,
                path="atomType",
                message=f"未注册的 atom_type：{atom_type!r}；已注册：{known}",
                fix_hint="改用已注册的原子类型（八类 + 2 变体；REQ-M01-F01），或先注册 schema",
            )
        ]
    if not isinstance(content, Mapping):
        return [
            Violation(
                rule_id=RULE_ATOM_SCHEMA,
                path="content",
                message=f"content 必须是对象，得到 {type(content).__name__}",
                fix_hint="把 content 改为 JSON 对象（见 ATOM_SCHEMAS）",
            )
        ]
    return _content_violations(atom_type, content)


def validate_write(node: NodeIn, *, doc_type: str | None = None) -> list[Violation]:
    """写入级校验：提议级判据 + 节点字段判据（锚形态/自指父/表格 format/外部引用）。

    ``doc_type`` 可选：给出时叠加 M01 组合规则（`allowed_atom_types`）判据——M06 写入
    路径已知目标文档，M03 提议路径自行按 `result.doc_meta` 判定。
    """
    violations = validate_proposal(node.atom_type, node.content)

    if not node.anchor.startswith(f"{node.doc_id}#"):
        violations.append(
            Violation(
                rule_id=RULE_ANCHOR_DOC_ID,
                path="anchor",
                message=(
                    f"锚 {_clip(node.anchor)!r} 不以 <doc_id># 起首（doc_id={node.doc_id!r}）——"
                    "锚为库内唯一寻址口径，形态由 M01 锚构造单点决定"
                ),
                fix_hint="用 model.anchors.assign_anchors/make_anchor 重算锚（勿手工拼接）",
            )
        )
    if node.node_id is not None and node.parent_node_id == node.node_id:
        violations.append(
            Violation(
                rule_id=RULE_PARENT_SELF,
                path="parent_node_id",
                message=f"parent_node_id 指向自身（{node.node_id}）；ADR-009 外键降级后无 DB 兜底",
                fix_hint="置 parent_node_id 为上级节点 id 或 null",
            )
        )
    violations.extend(_table_violations(node))
    if node.atom_type == "cross_ref":
        target_doc = str(node.content.get("target_doc_id") or "")
        if target_doc.startswith(_EXTERNAL_PREFIX) and node.content.get("target_node_id"):
            violations.append(
                Violation(
                    rule_id=RULE_CROSS_REF_EXTERNAL_NODE,
                    path="content.target_node_id",
                    message=(
                        f"外部叶引用（target_doc_id={_clip(target_doc)!r}）不得带 target_node_id"
                        "（外部文档不在库内，无节点可指）"
                    ),
                    fix_hint="删除 content.target_node_id，仅保留 target_doc_id/target_anchor",
                )
            )
    if doc_type is not None and not is_atom_allowed(doc_type, node.atom_type):
        violations.append(
            Violation(
                rule_id=RULE_DOC_TYPE_ATOM,
                path="atomType",
                message=(
                    f"doc_type={doc_type!r} 不允许原子 {node.atom_type!r}"
                    f"（允许：{list(allowed_atom_types(doc_type))}）"
                ),
                fix_hint="调整规则映射或扩展 doc_type 组合规则（REQ-M01-F03）",
            )
        )
    return sorted(violations, key=lambda item: (item.rule_id, item.path))


def _table_violations(node: NodeIn) -> list[Violation]:
    """表格原子（E1-a）：`format` 与 `fragment` 形态必须一致（md 管道表 / html 片段）。"""
    if node.atom_type not in TABLE_ATOMS:
        return []
    fragment = node.content.get("fragment")
    if not isinstance(fragment, str):
        return []  # schema 已报 required/minLength
    has_html_table = "<table" in fragment.lower()
    if node.format == "html" and has_html_table:
        return []
    if node.format == "md" and not has_html_table:
        return []
    expected = "html" if has_html_table else "md"
    return [
        Violation(
            rule_id=RULE_TABLE_FORMAT,
            path="format",
            message=(
                f"表格原子 format={node.format!r} 与 fragment 形态不符：fragment "
                f"{'含' if has_html_table else '不含'} `<table>`，应为 format={expected!r}"
                "（E1-a：HTML 片段原样直通 / md 管道表原样直通，P4）"
            ),
            fix_hint=f"把 format 改为 {expected!r}（保持 fragment 原样，勿改写片段）",
        )
    ]
