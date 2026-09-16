"""M09B `terms` detector：术语表校验（R10 / REQ-M09-F02 数据面）。

数据源两处，缺一不可（P5：判据口径来自 R10 与 §5 环境清单）：

* `terms` 表——`{term, definition_node_id, kind}`，`kind ∈ {glossary, normative-keyword}`；
* 种子文件——`TERMS_SEED`（默认 `<repo>/data/terms_seed.yaml`），§5 声明「随 migrate 载入」；
  本 detector 只**读**不写（写入路径属 M01 `upsert_term` / M07 `POST /api/v1/terms`）。

判据：

* `M09B.terms.definition_dangling` — `terms.definition_node_id` 指向不存在或已软删的节点。
  ADR-009 把该外键降级（6 处之一），此处即其兜底；
* `M09B.terms.node_not_definition` — `definition_node_id` 指向的节点不是 `definition` 原子
  （词表与内容模型脱钩：R10 要求指向 definition 节点）；
* `M09B.terms.kind` — 绑定了 definition 节点的词条 `kind` 必须是 `glossary`
  （`normative-keyword` 是规范性关键词，不对应文档节点）；
* `M09B.terms.unregistered` — 作用域内 `definition` 原子的 `content.term` 在 `terms` 表中
  **完全无行**（该术语未被词表登记，检索与术语一致性无从建立）；
* `M09B.terms.seed_missing` — 种子中声明的词条未入库或 `kind` 与种子不符（种子随 migrate
  载入；未载入即部署不完整）。

**盲区声明**：同名术语的多个 definition 节点只可能有一个绑定 `definition_node_id`
（`terms.term` 是主键），故 `unregistered` 只在「该 term 一行都没有」时报出——这是刻意的
低误报取舍，绑定关系漂移由 `definition_dangling` / `node_not_definition` 覆盖。

`terms` 数据面无 doc 维度：`doc_ids` 只影响 `unregistered`（按 definition 节点所属文档裁剪），
其余判据恒定全表执行。
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

import yaml
from sqlalchemy import Select, select

from agenticdocer.model import TermKind, Violation
from agenticdocer.store import ValidationError
from agenticdocer.store.schema import nodes, terms

from .context import GateContext

__all__ = [
    "DETECTOR_ID",
    "RULES_TERMS",
    "SEED_TERM_KINDS",
    "SeedTerm",
    "detect",
    "judge_definition_dangling",
    "judge_kind",
    "judge_seed",
    "judge_unregistered",
    "load_seed",
    "seed_path",
]

DETECTOR_ID: Final = "terms"

RULE_TERMS_DANGLING: Final = "M09B.terms.definition_dangling"
RULE_TERMS_NODE_NOT_DEFINITION: Final = "M09B.terms.node_not_definition"
RULE_TERMS_KIND: Final = "M09B.terms.kind"
RULE_TERMS_UNREGISTERED: Final = "M09B.terms.unregistered"
RULE_TERMS_SEED_MISSING: Final = "M09B.terms.seed_missing"

RULES_TERMS: tuple[str, ...] = (
    RULE_TERMS_DANGLING,
    RULE_TERMS_NODE_NOT_DEFINITION,
    RULE_TERMS_KIND,
    RULE_TERMS_UNREGISTERED,
    RULE_TERMS_SEED_MISSING,
)

SEED_TERM_KINDS: Final[tuple[str, ...]] = ("glossary", "normative-keyword")
"""种子文件允许的 `kind`（与 M01 `TermKind` / DDL CHECK 同源）。"""

_REPO_ROOT: Final = Path(__file__).resolve().parents[4]
"""`src/agenticdocer/m09/quality_9b/terms.py` → 仓库根（parents: quality_9b, m09, agenticdocer, src）。"""

DEFAULT_SEED_PATH: Final = _REPO_ROOT / "data" / "terms_seed.yaml"


@dataclass(frozen=True, slots=True)
class SeedTerm:
    """种子文件中的一条词条声明。"""

    term: str
    kind: TermKind


def seed_path(path: Path | str | None = None) -> Path:
    """种子文件路径：显式入参 → `TERMS_SEED`（§5）→ 仓库 `data/terms_seed.yaml`。"""
    if path is not None:
        return Path(path)
    import os

    configured = os.environ.get("TERMS_SEED")
    return Path(configured) if configured else DEFAULT_SEED_PATH


def load_seed(path: Path | str | None = None) -> list[SeedTerm]:
    """读种子词表（严格解析：结构/取值域错误 → `ValidationError`，不静默降级）。

    文件形式（`data/terms_seed.yaml`）::

        version: 1
        terms:
          - term: MUST
            kind: normative-keyword
    """
    target = seed_path(path)
    if not target.is_file():
        raise ValidationError(
            f"术语种子文件不存在：{target}（TERMS_SEED 见 §5；本仓库默认 data/terms_seed.yaml）",
            entity="term",
        )
    try:
        raw = yaml.safe_load(target.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValidationError(f"术语种子文件解析失败：{target}（{exc}）", entity="term") from exc

    if not isinstance(raw, Mapping) or not isinstance(raw.get("terms"), list):
        raise ValidationError(
            f"术语种子文件结构非法：{target} 顶层须为映射且含 `terms` 列表（见模块文档）",
            entity="term",
        )
    seeded: list[SeedTerm] = []
    seen: set[str] = set()
    for index, item in enumerate(raw["terms"]):
        if not isinstance(item, Mapping):
            raise ValidationError(f"术语种子第 {index} 项不是映射：{item!r}", entity="term")
        term = str(item.get("term") or "").strip()
        kind = str(item.get("kind") or "")
        if not term:
            raise ValidationError(f"术语种子第 {index} 项缺 `term`", entity="term")
        if kind not in SEED_TERM_KINDS:
            raise ValidationError(
                f"术语种子第 {index} 项 kind={kind!r} 非法；期望 {list(SEED_TERM_KINDS)}",
                entity="term",
            )
        if term in seen:
            raise ValidationError(f"术语种子第 {index} 项 term={term!r} 重复", entity="term")
        seen.add(term)
        seeded.append(SeedTerm(term=term, kind=kind))  # type: ignore[arg-type]
    return seeded


# ── 纯判据（行 → 违规）────────────────────────────────────────────────────


def judge_definition_dangling(rows: Sequence[Mapping[str, Any]]) -> list[Violation]:
    """词条绑定的节点不存在/已软删/非 definition 原子（行键见 `_linked_statement`）。"""
    violations: list[Violation] = []
    for row in rows:
        term = str(row["term"])
        path = f"terms/{term}"
        bound = row["definition_node_id"]
        if row["node_found"] is None:
            violations.append(
                Violation(
                    rule_id=RULE_TERMS_DANGLING,
                    path=path,
                    message=(
                        f"词条绑定的定义节点不存在：definition_node_id={bound}"
                        "（ADR-009：terms.definition_node_id 无外键，本项为其兜底）"
                    ),
                    fix_hint="重新导入该 definition 原子并 upsert_term 重绑，或置 definition_node_id=null",
                )
            )
        elif row["node_status"] != "active":
            violations.append(
                Violation(
                    rule_id=RULE_TERMS_DANGLING,
                    path=path,
                    message=(
                        f"词条绑定的定义节点已软删（status={row['node_status']}）："
                        f"definition_node_id={bound}"
                    ),
                    fix_hint="恢复该节点，或把 definition_node_id 重绑到存活的 definition 节点",
                )
            )
        elif row["node_atom_type"] != "definition":
            violations.append(
                Violation(
                    rule_id=RULE_TERMS_NODE_NOT_DEFINITION,
                    path=path,
                    message=(
                        f"词条绑定的节点不是 definition 原子（atom_type={row['node_atom_type']!r}）："
                        f"definition_node_id={bound}（R10）"
                    ),
                    fix_hint="重绑到该术语的 definition 节点（或置 null 表示仅词表登记）",
                )
            )
    return violations


def judge_kind(rows: Sequence[Mapping[str, Any]]) -> list[Violation]:
    """绑定节点的词条 `kind` 必须为 `glossary`（行键：`term/definition_node_id/kind`）。"""
    violations: list[Violation] = []
    for row in rows:
        if row["definition_node_id"] is None or row["kind"] == "glossary":
            continue
        term = str(row["term"])
        violations.append(
            Violation(
                rule_id=RULE_TERMS_KIND,
                path=f"terms/{term}",
                message=(
                    f"词条 {term!r} 绑定了 definition 节点却 kind={row['kind']!r}；"
                    "规范性关键词（normative-keyword）不对应文档节点（R10）"
                ),
                fix_hint="改 kind='glossary'，或清空 definition_node_id 保留为规范性关键词",
            )
        )
    return violations


def judge_unregistered(
    definition_rows: Sequence[Mapping[str, Any]], term_rows: Sequence[Mapping[str, Any]]
) -> list[Violation]:
    """作用域内 definition 原子的 `content.term` 是否被词表登记（行键：`node_id/doc_id/term`）。"""
    registered = {str(row["term"]) for row in term_rows}
    violations: list[Violation] = []
    for row in definition_rows:
        term = str(row["term"] or "").strip()
        if not term or term in registered:
            continue
        violations.append(
            Violation(
                rule_id=RULE_TERMS_UNREGISTERED,
                path=f"nodes/{row['node_id']}#content.term",
                message=(
                    f"definition 原子的术语 {term!r}（doc_id={row['doc_id']}）未登记到 terms 词表"
                    "——术语一致性校验失去数据源（R10）"
                ),
                fix_hint=(
                    f"upsert_term({term!r}, definition_node_id={row['node_id']!r}, "
                    "kind='glossary', ctx)（M01 写入路径）"
                ),
            )
        )
    return violations


def judge_seed(
    seeded: Sequence[SeedTerm], term_rows: Sequence[Mapping[str, Any]]
) -> list[Violation]:
    """种子词条是否已载入 `terms` 表且 `kind` 一致（§5：种子随 migrate 载入）。"""
    stored = {str(row["term"]): str(row["kind"]) for row in term_rows}
    violations: list[Violation] = []
    for item in seeded:
        if item.term not in stored:
            violations.append(
                Violation(
                    rule_id=RULE_TERMS_SEED_MISSING,
                    path=f"terms/{item.term}",
                    message=(
                        f"种子词条 {item.term!r}（kind={item.kind}）未入库——TERMS_SEED 未载入，"
                        "词表数据面缺失"
                    ),
                    fix_hint=(
                        f"upsert_term({item.term!r}, None, {item.kind!r}, ctx)，"
                        "或核对 migrate 的 TERMS_SEED 载入步骤（§5）"
                    ),
                )
            )
        elif stored[item.term] != item.kind:
            violations.append(
                Violation(
                    rule_id=RULE_TERMS_KIND,
                    path=f"terms/{item.term}",
                    message=(
                        f"词条 {item.term!r} 的 kind={stored[item.term]!r} 与种子声明的 "
                        f"{item.kind!r} 不一致"
                    ),
                    fix_hint=f"以种子为准改 kind={item.kind!r}（种子是规范性关键词的权威清单）",
                )
            )
    return violations


# ── 取数 ─────────────────────────────────────────────────────────────────


def _term_columns() -> list[Any]:
    return [terms.c.term, terms.c.definition_node_id, terms.c.kind]


def _all_terms_statement() -> Select[Any]:
    return select(*_term_columns()).order_by(terms.c.term)


def _linked_statement() -> Select[Any]:
    """词条 → 绑定节点（左连接：节点缺失/软删/原子类型都可观测）。"""
    return (
        select(
            *_term_columns(),
            nodes.c.node_id.label("node_found"),
            nodes.c.status.label("node_status"),
            nodes.c.atom_type.label("node_atom_type"),
        )
        .select_from(terms.join(nodes, nodes.c.node_id == terms.c.definition_node_id, isouter=True))
        .where(terms.c.definition_node_id.is_not(None))
        .order_by(terms.c.term)
    )


def _definitions_statement(doc_ids: Sequence[str] | None) -> Select[Any]:
    statement = (
        select(
            nodes.c.node_id,
            nodes.c.doc_id,
            nodes.c.content.op("->>")("term").label("term"),
        )
        .where(nodes.c.atom_type == "definition", nodes.c.status == "active")
        .order_by(nodes.c.doc_id, nodes.c.ordinal)
    )
    if doc_ids is not None:
        statement = statement.where(nodes.c.doc_id.in_(tuple(doc_ids)))
    return statement


async def detect(ctx: GateContext) -> list[Violation]:
    """执行术语表校验（3 条查询 + 1 次种子读取）。"""
    seeded = load_seed()
    async with ctx.storage.db.session() as session:
        term_rows = (await session.execute(_all_terms_statement())).mappings().all()
        linked_rows = (await session.execute(_linked_statement())).mappings().all()
        definition_rows = (await session.execute(_definitions_statement(ctx.doc_ids))).mappings().all()
    return [
        *judge_definition_dangling(linked_rows),
        *judge_kind(term_rows),
        *judge_unregistered(definition_rows, term_rows),
        *judge_seed(seeded, term_rows),
    ]
