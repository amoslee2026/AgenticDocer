"""M09B `section_range_consistency` detector：大纲区间契约巡检（M02 B-2 缺口兜底）。

背景（M02 的 B-2 优化）：`render_section` 走 **O(子树)** 快路径 `get_section_nodes`
（区间扫 `ordinal ∈ [root, end)`，`end` = 下一个 `level <= root.level` 的标题），依赖不变量
「**`ordinal` 序即大纲序**，且子树在区间内连续」。M02 加了「父链连通性自检 + 不合格自动回退
递归 CTE」，但自检只能拦住**多收**方向；**漏收**（父链声明是后代、却因 `ordinal` 排布落在
区间之外）在区间内无法自检 —— 本 detector 即该残余风险的**巡检兜底**（Main 批准落地）。

判定口径（P5：区间法真值只有一处）
----------------------------------

判据**完全委托 M02 的诊断接口** `Storage.section_range_diff(doc_id, node_id)`
（`check_section_range` 是它的布尔投影），其比较对象是「区间法**原始**结果（绕开自愈回退）」
与「`get_subtree` 的递归 CTE」——若改比公开读接口，快路径的自愈回退会让两者恒等而**漏报**：

* 返回 `None` → 不可判定（节点不在该文档 / `level` 为空）→ 跳过并计入 skipped；
* `first_diff_index is None` 且两侧等长 → 一致，干净；
* 否则 → 契约破坏，报 `M09B.section_range_mismatch`：
  - `interval_self_check=False` → 区间**不可用**（空哨兵）→ 定性为**多收/断链**，按 CTE 定位；
  - 自检通过 → 用 `missing_in_interval`/`extra_in_interval` 给出「区间缺 X / 区间多 Y」。

本模块**不复制**右边界/区间规则（那会成第二口径）：定位数据全部来自 M02 的 diff。

抽样（性能）
------------

全量两两比较是 O(n²)，故**按文档抽样** `M09_SECTION_SAMPLE_SIZE`（默认 20）个代表节点：
根、最小 level、区间边界（ordinal 首尾）、叶子、中间层各取代表，再等距填充 —— **确定性**
（同文档同结果，无随机）。每样本 2 次查询（区间 + CTE），成本 O(样本数 × 子树)。

**只读巡检**：不改任何数据；角色门槛由调用面（M11 `quality-gate`）决定（至少 reader）。
"""

from __future__ import annotations

import os
from collections.abc import Mapping, Sequence
from typing import Any, Final
from uuid import UUID

from agenticspec.model import Doc, Node, Violation

from .context import GateContext

__all__ = [
    "DETECTOR_ID",
    "DEFAULT_SAMPLE_SIZE",
    "RULE_SECTION_RANGE_MISMATCH",
    "RULES_SECTION_RANGE",
    "SAMPLE_SIZE_ENV",
    "detect",
    "judge_section_diff",
    "sample_nodes",
    "sample_size",
]

DETECTOR_ID: Final = "section_range_consistency"

#: 违规规则 id。**命名说明**：任务书写作 `DTO_SECTION_RANGE_MISMATCH`，但 `DTO_*` 是 M12 的
#: **日志错误码**口径（`error_code_for_rule(rule_id)` 按 rule_id 建键），而 M09B 的违规 id
#: 一律为 `M09B.<判据>`（既有六个 detector 同口径）。故取 `M09B.section_range_mismatch`；
#: M12 对未登记 rule_id **原样透传**（其模块文档明示），按规则名聚合仍可用。
RULE_SECTION_RANGE_MISMATCH: Final = "M09B.section_range_mismatch"
RULES_SECTION_RANGE: Final = (RULE_SECTION_RANGE_MISMATCH,)

DEFAULT_SAMPLE_SIZE: Final = 20
"""每文档抽样节点数（`M09_SECTION_SAMPLE_SIZE` 可覆盖）。"""

SAMPLE_SIZE_ENV: Final = "M09_SECTION_SAMPLE_SIZE"
_MAX_SAMPLE_SIZE: Final = 1000
_ID_LIST_LIMIT: Final = 3
"""消息里逐条列出的差异节点上限（超出只报计数，避免长文档刷屏）。"""

FIX_HINT: Final = (
    "检查该节点及其后代的 `ordinal` 与 `parent_node_id` 是否自洽（契约：`ordinal` 序 = 大纲序，"
    "子树在 [root.ordinal, 下一个 level ≤ root.level 的标题) 区间内连续）；"
    "重解析入库（M03 commit 按 (level, ordinal) 栈重建 parent）通常即可修复"
)


def sample_size() -> int:
    """每文档抽样数：`M09_SECTION_SAMPLE_SIZE` → 默认 20（非法值回落默认，钳制 [1, 1000]）。"""
    raw = os.environ.get(SAMPLE_SIZE_ENV)
    try:
        value = int(raw) if raw is not None else DEFAULT_SAMPLE_SIZE
    except ValueError:
        return DEFAULT_SAMPLE_SIZE
    return max(1, min(_MAX_SAMPLE_SIZE, value))


def sample_nodes(nodes: Sequence[Node], size: int) -> list[Node]:
    """**确定性**抽取代表节点（根 / 最小 level / 边界 / 叶子 / 中间层 / 等距填充）。

    只考虑 `level is not None` 的节点（`level` 空 → 区间右边界不可定义，`section_range_diff`
    返回 `None`）。同文档同 `size` → 同序列（无随机源，便于复现与快照断言）。
    """
    candidates = [node for node in nodes if node.level is not None]
    if size <= 0 or not candidates:
        return []
    if size >= len(candidates):
        return list(candidates)

    picked: list[Node] = []
    seen: set[UUID] = set()

    def take(node: Node) -> None:
        if len(picked) < size and node.node_id not in seen:
            seen.add(node.node_id)
            picked.append(node)

    child_parents = {node.parent_node_id for node in candidates if node.parent_node_id is not None}
    roots = [node for node in candidates if node.parent_node_id is None]
    leaves = [node for node in candidates if node.node_id not in child_parents]
    middles = [
        node
        for node in candidates
        if node.parent_node_id is not None and node.node_id in child_parents
    ]
    top_level = min(node.level for node in candidates if node.level is not None)

    for node in (
        *(roots[:1]),
        *[node for node in candidates if node.level == top_level][:1],
        candidates[0],
        candidates[-1],
        *(leaves[:1]),
        *(middles[len(middles) // 2 : len(middles) // 2 + 1]),
    ):
        take(node)

    stride = max(1, len(candidates) // size)
    for node in candidates[::stride]:
        take(node)
    for node in candidates:  # 兜底补足（去重后可能不足 size）
        take(node)
    return picked


def _listed(values: Sequence[Any]) -> str:
    """差异节点列表 → 可读文本（超过 `_ID_LIST_LIMIT` 只报计数）。"""
    if not values:
        return "无"
    shown = "、".join(str(item) for item in values[:_ID_LIST_LIMIT])
    return shown if len(values) <= _ID_LIST_LIMIT else f"{shown} 等 {len(values)} 个"


def judge_section_diff(doc_id: str, root: Node, diff: Mapping[str, Any]) -> Violation | None:
    """M02 的 diff → 违规（纯函数）：一致 → `None`；不一致 → `M09B.section_range_mismatch`。"""
    interval = list(diff["interval_ids"])
    subtree = list(diff["subtree_ids"])
    index = diff["first_diff_index"]
    self_check = bool(diff["interval_self_check"])
    if index is None and len(interval) == len(subtree):
        return None

    head = (
        f"大纲区间契约被破坏（doc_id={doc_id}，节点 anchor={root.anchor!r}，level={root.level}）："
    )
    if not self_check:
        detail = (
            f"区间法**不可用**（父链连通性/区间连续自检未通过，空哨兵）vs 递归 CTE "
            f"{len(subtree)} 行 —— 定性为**多收/断链**（区间行数无意义），按语义权威 CTE 定位"
        )
    else:
        detail = (
            f"区间法 {len(interval)} 行 vs 递归 CTE {len(subtree)} 行，首个差异 @{index}："
            f"区间缺 {_listed(diff['missing_in_interval'])} / 区间多 {_listed(diff['extra_in_interval'])}"
        )
    return Violation(
        rule_id=RULE_SECTION_RANGE_MISMATCH,
        path=f"nodes/{root.node_id}",
        message=head + detail,
        fix_hint=FIX_HINT,
    )


async def _scoped_docs(ctx: GateContext) -> list[Doc]:
    docs = await ctx.storage.list_docs()
    if ctx.doc_ids is None:
        return docs
    wanted = set(ctx.doc_ids)
    return [doc for doc in docs if doc.doc_id in wanted]


async def detect(ctx: GateContext) -> list[Violation]:
    """按文档抽样，逐样本取 M02 的区间/CTE 差异（只读；成环/深链由 M02 的深度上限保证终止）。"""
    size = sample_size()
    violations: list[Violation] = []
    mismatches = 0
    skipped = 0
    docs = await _scoped_docs(ctx)
    for doc in docs:
        nodes = await ctx.storage.get_doc_nodes(doc.doc_id)
        for root in sample_nodes(nodes, size):
            diff = await ctx.storage.section_range_diff(doc.doc_id, root.node_id)
            if diff is None:
                # 不可判定：节点不在该文档或 level 为空（M02 的三态语义，不与契约破坏混用）
                skipped += 1
                continue
            violation = judge_section_diff(doc.doc_id, root, diff)
            if violation is None:
                continue
            if not diff["subtree_ids"]:
                # 并发防护：抽样后节点被删/无可达子树 → 不作为契约破坏上报
                skipped += 1
                continue
            mismatches += 1
            violations.append(violation)
    ctx.logger.info(
        "section range scanned",
        docs=len(docs),
        sample_size=size,
        mismatches=mismatches,
        skipped_undecidable=skipped,
        violations=len(violations),
    )
    return violations
