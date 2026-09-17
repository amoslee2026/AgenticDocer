"""M09B `broken_refs` detector：外键降级后的**悬空引用巡检**（ADR-009 §1/§3）。

ADR-009 为分区化把 6 处外键降级为应用层校验，DB 不再兜底（`events` 分区 + `nodes`
HASH 分区使级联外键不可用）：

| 降级的外键 | 兜底位置 |
|---|---|
| `nodes.parent_node_id → nodes(node_id)` | 本模块（孤儿 parent） |
| `refs.src_node_id → nodes(node_id)` | 本模块 |
| `refs.dst_node_id → nodes(node_id)` | 本模块 |
| `comments.node_id → nodes(node_id)` | 本模块 |
| `comments.target_event_id → events(event_id)` | 本模块 |
| `terms.definition_node_id → nodes(node_id)` | :mod:`agenticspec.m09.quality_9b.terms`（术语面同表读取） |

判据（全部机械可验，`path` = 出错行）：

* `refs.src_node_id` 不存在 → `M09B.ref.src_dangling`；存在但软删（A2）→ `M09B.ref.src_deleted`
  （边仍在，遍历会命中已删节点）；
* `refs.dst_node_id` 非空时：节点不存在 → `M09B.ref.dst_dangling`；软删 → `M09B.ref.dst_deleted`；
* `refs.dst_doc_id` 既非库内文档、也不以 ``EXT:`` 起首（外部叶引用）→ `M09B.ref.dst_doc_missing`
  （`refs.dst_doc_id` 无 DB 外键，ADR-009 亦未给应用层校验）；
* `dst_node_id` 非空但该节点 `doc_id` ≠ `dst_doc_id` → `M09B.ref.dst_doc_mismatch`（边自相矛盾）；
* 节点 `parent_node_id` 指向不存在 → `M09B.node.parent_dangling`；指向软删节点 → `M09B.node.parent_deleted`
  （M02 `_assert_parent_exists` 只校验「写入当刻存在」，软删后无兜底）；
* 批注 `node_id` 不存在 → `M09B.comment.node_dangling`；批注 `state='open'` 而节点已软删 →
  `M09B.comment.node_deleted`（`delete_node` 应已 `orphan_comments`，缺失即数据不一致）；
* 批注 `target_event_id` 非空而事件不存在 → `M09B.comment.event_dangling`。

`judge_*` 为纯函数（行 → 违规），供单测直接造缺陷验证；`detect` 只负责取数与裁剪。
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Final

from sqlalchemy import Select, select

from agenticspec.model import Violation
from agenticspec.store.schema import comments, docs, events, nodes, refs

from .context import GateContext

__all__ = [
    "DETECTOR_ID",
    "RULES_BROKEN_REFS",
    "detect",
    "judge_comments",
    "judge_parents",
    "judge_refs",
]

DETECTOR_ID: Final = "broken_refs"

RULE_REF_SRC_DANGLING: Final = "M09B.ref.src_dangling"
RULE_REF_SRC_DELETED: Final = "M09B.ref.src_deleted"
RULE_REF_DST_DANGLING: Final = "M09B.ref.dst_dangling"
RULE_REF_DST_DELETED: Final = "M09B.ref.dst_deleted"
RULE_REF_DST_DOC_MISSING: Final = "M09B.ref.dst_doc_missing"
RULE_REF_DST_DOC_MISMATCH: Final = "M09B.ref.dst_doc_mismatch"
RULE_NODE_PARENT_DANGLING: Final = "M09B.node.parent_dangling"
RULE_NODE_PARENT_DELETED: Final = "M09B.node.parent_deleted"
RULE_COMMENT_NODE_DANGLING: Final = "M09B.comment.node_dangling"
RULE_COMMENT_NODE_DELETED: Final = "M09B.comment.node_deleted"
RULE_COMMENT_EVENT_DANGLING: Final = "M09B.comment.event_dangling"

RULES_BROKEN_REFS: tuple[str, ...] = (
    RULE_REF_SRC_DANGLING,
    RULE_REF_SRC_DELETED,
    RULE_REF_DST_DANGLING,
    RULE_REF_DST_DELETED,
    RULE_REF_DST_DOC_MISSING,
    RULE_REF_DST_DOC_MISMATCH,
    RULE_NODE_PARENT_DANGLING,
    RULE_NODE_PARENT_DELETED,
    RULE_COMMENT_NODE_DANGLING,
    RULE_COMMENT_NODE_DELETED,
    RULE_COMMENT_EVENT_DANGLING,
)

EXTERNAL_DOC_PREFIX: Final = "EXT:"
"""外部叶引用（设计文档 §4：`dst_doc_id='EXT:<uri>'`，合法且不参与库内存在性判定）。"""

_MISSING_FIX: Final = "重新导入/补建目标节点（M03 重解析 + commit），或改用 remove_ref 摘除该边"


# ── 纯判据（行 → 违规）────────────────────────────────────────────────────


def judge_refs(rows: Sequence[Mapping[str, Any]]) -> list[Violation]:
    """引用边判据（行键见 `_refs_statement`）。"""
    violations: list[Violation] = []
    for row in rows:
        ref_id = str(row["ref_id"])
        path = f"refs/{ref_id}"
        edge = f"{row['kind']} {row['src_node_id']} → {row['dst_doc_id']}/{row['dst_node_id']}"
        if row["src_found"] is None:
            violations.append(
                Violation(
                    rule_id=RULE_REF_SRC_DANGLING,
                    path=path,
                    message=f"引用边的源节点不存在：{edge}（ADR-009：refs.src_node_id 无外键）",
                    fix_hint=f"恢复源节点或删除该边：remove_ref({row['src_node_id']!r}, …, ctx)",
                )
            )
        elif row["src_status"] != "active":
            violations.append(
                Violation(
                    rule_id=RULE_REF_SRC_DELETED,
                    path=path,
                    message=f"引用边的源节点已软删（status={row['src_status']}）：{edge}",
                    fix_hint="删除该边（remove_ref）或恢复源节点（恢复后重跑 M09B）",
                )
            )
        dst_node_id = row["dst_node_id"]
        if dst_node_id is not None:
            if row["dst_found"] is None:
                violations.append(
                    Violation(
                        rule_id=RULE_REF_DST_DANGLING,
                        path=path,
                        message=f"引用边的目标节点不存在：{edge}（M09B broken_refs 即为此兜底，ADR-009）",
                        fix_hint=_MISSING_FIX,
                    )
                )
            elif row["dst_status"] != "active":
                violations.append(
                    Violation(
                        rule_id=RULE_REF_DST_DELETED,
                        path=path,
                        message=f"引用边的目标节点已软删（status={row['dst_status']}）：{edge}",
                        fix_hint="删除该边（remove_ref）或恢复目标节点",
                    )
                )
            elif row["dst_node_doc_id"] != row["dst_doc_id"]:
                violations.append(
                    Violation(
                        rule_id=RULE_REF_DST_DOC_MISMATCH,
                        path=path,
                        message=(
                            f"引用边自相矛盾：dst_doc_id={row['dst_doc_id']!r} 但 dst_node_id "
                            f"属于文档 {row['dst_node_doc_id']!r}：{edge}"
                        ),
                        fix_hint="以目标节点实际 doc_id 修正 refs.dst_doc_id（重写边：remove_ref + add_ref）",
                    )
                )
        dst_doc_id = str(row["dst_doc_id"])
        if row["dst_doc_found"] is None and not dst_doc_id.startswith(EXTERNAL_DOC_PREFIX):
            violations.append(
                Violation(
                    rule_id=RULE_REF_DST_DOC_MISSING,
                    path=path,
                    message=(
                        f"引用边的目标文档不存在：dst_doc_id={dst_doc_id!r}（外部叶引用须以 "
                        f"{EXTERNAL_DOC_PREFIX!r} 起首）：{edge}"
                    ),
                    fix_hint="改为库内 doc_id，或按外部叶引用口径写 'EXT:<uri>'（先确认源块确实引用外部文档）",
                )
            )
    return violations


def judge_parents(rows: Sequence[Mapping[str, Any]]) -> list[Violation]:
    """节点父子关系判据（行键：`node_id/doc_id/parent_node_id/parent_found/parent_status`）。"""
    violations: list[Violation] = []
    for row in rows:
        path = f"nodes/{row['node_id']}"
        parent = row["parent_node_id"]
        if row["parent_found"] is None:
            violations.append(
                Violation(
                    rule_id=RULE_NODE_PARENT_DANGLING,
                    path=path,
                    message=(
                        f"节点 {row['doc_id']} 的父节点不存在：parent_node_id={parent}"
                        "（ADR-009：nodes.parent_node_id 无外键，M02 仅校验写入当刻）"
                    ),
                    fix_hint="重解析入库（M03 commit 按 (level, ordinal) 栈重建 parent），或置 parent_node_id=null",
                )
            )
        elif row["parent_status"] != "active":
            violations.append(
                Violation(
                    rule_id=RULE_NODE_PARENT_DELETED,
                    path=path,
                    message=(
                        f"节点的父节点已软删（status={row['parent_status']}）：parent_node_id={parent}"
                        "——层级树出现悬挂分支"
                    ),
                    fix_hint="恢复父节点，或把该节点的 parent_node_id 上提到最近的存活祖先",
                )
            )
    return violations


def judge_comments(rows: Sequence[Mapping[str, Any]]) -> list[Violation]:
    """批注判据（行键：`comment_id/node_id/state/target_event_id/node_found/node_status/event_found`）。"""
    violations: list[Violation] = []
    for row in rows:
        path = f"comments/{row['comment_id']}"
        if row["node_found"] is None:
            violations.append(
                Violation(
                    rule_id=RULE_COMMENT_NODE_DANGLING,
                    path=path,
                    message=(
                        f"批注指向的节点不存在：node_id={row['node_id']}"
                        "（ADR-009：comments.node_id 无外键；A2 软删方案下无级联）"
                    ),
                    fix_hint="把批注置 orphaned（M02 orphan_comments 口径），或恢复节点",
                )
            )
        elif row["node_status"] != "active" and row["state"] == "open":
            violations.append(
                Violation(
                    rule_id=RULE_COMMENT_NODE_DELETED,
                    path=path,
                    message=(
                        f"批注仍为 open 而节点已软删（node_id={row['node_id']}）——"
                        "delete_node 应同事务 orphan_comments（A2）"
                    ),
                    fix_hint="PATCH 该批注 state='orphaned'（M07 /api/v1/comments/{id}），或恢复节点",
                )
            )
        if row["target_event_id"] is not None and not row["event_found"]:
            violations.append(
                Violation(
                    rule_id=RULE_COMMENT_EVENT_DANGLING,
                    path=path,
                    message=(
                        f"批注锚定的事件不存在：target_event_id={row['target_event_id']}"
                        "（ADR-009：comments.target_event_id 无外键）"
                    ),
                    fix_hint="重锚到该节点的最新事件（M02 _latest_node_event_id 口径），或置 target_event_id=null",
                )
            )
    return violations


# ── 取数（分区分片裁剪：作用域按源节点所属文档）────────────────────────────


def _scoped_node_ids(doc_ids: Sequence[str]) -> Select[Any]:
    """作用域内的节点 id 子查询（`nodes` 按 doc_id HASH 分区 → 子查询可吃分区裁剪）。"""
    return select(nodes.c.node_id).where(nodes.c.doc_id.in_(tuple(doc_ids)))


def _refs_statement(doc_ids: Sequence[str] | None) -> Select[Any]:
    src = nodes.alias("src")
    dst = nodes.alias("dst")
    statement = (
        select(
            refs.c.ref_id,
            refs.c.src_node_id,
            refs.c.dst_doc_id,
            refs.c.dst_node_id,
            refs.c.kind,
            src.c.node_id.label("src_found"),
            src.c.status.label("src_status"),
            dst.c.node_id.label("dst_found"),
            dst.c.status.label("dst_status"),
            dst.c.doc_id.label("dst_node_doc_id"),
            docs.c.doc_id.label("dst_doc_found"),
        )
        .select_from(
            refs.join(src, src.c.node_id == refs.c.src_node_id, isouter=True)
            .join(dst, dst.c.node_id == refs.c.dst_node_id, isouter=True)
            .join(docs, docs.c.doc_id == refs.c.dst_doc_id, isouter=True)
        )
        .order_by(refs.c.ref_id)
    )
    if doc_ids is not None:
        statement = statement.where(refs.c.src_node_id.in_(_scoped_node_ids(doc_ids)))
    return statement


def _parents_statement(doc_ids: Sequence[str] | None) -> Select[Any]:
    parent = nodes.alias("parent")
    statement = (
        select(
            nodes.c.node_id,
            nodes.c.doc_id,
            nodes.c.parent_node_id,
            parent.c.node_id.label("parent_found"),
            parent.c.status.label("parent_status"),
        )
        .select_from(
            nodes.join(parent, parent.c.node_id == nodes.c.parent_node_id, isouter=True)
        )
        .where(nodes.c.parent_node_id.is_not(None))
        .order_by(nodes.c.node_id)
    )
    if doc_ids is not None:
        statement = statement.where(nodes.c.doc_id.in_(tuple(doc_ids)))
    return statement


def _comments_statement(doc_ids: Sequence[str] | None) -> Select[Any]:
    statement = (
        select(
            comments.c.comment_id,
            comments.c.node_id,
            comments.c.state,
            comments.c.target_event_id,
            nodes.c.node_id.label("node_found"),
            nodes.c.status.label("node_status"),
            events.c.event_id.label("event_found"),
        )
        .select_from(
            comments.join(nodes, nodes.c.node_id == comments.c.node_id, isouter=True).join(
                events, events.c.event_id == comments.c.target_event_id, isouter=True
            )
        )
        .order_by(comments.c.comment_id)
    )
    if doc_ids is not None:
        statement = statement.where(comments.c.node_id.in_(_scoped_node_ids(doc_ids)))
    return statement


async def detect(ctx: GateContext) -> list[Violation]:
    """执行悬空引用巡检（一次会话内三条查询；均为左连接，故缺失行也可被观测到）。"""
    doc_ids = ctx.doc_ids
    async with ctx.storage.db.session() as session:
        ref_rows = (await session.execute(_refs_statement(doc_ids))).mappings().all()
        parent_rows = (await session.execute(_parents_statement(doc_ids))).mappings().all()
        comment_rows = (await session.execute(_comments_statement(doc_ids))).mappings().all()
    return [
        *judge_refs(ref_rows),
        *judge_parents(parent_rows),
        *judge_comments(comment_rows),
    ]
