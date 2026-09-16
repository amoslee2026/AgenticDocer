"""M09B `section_range_consistency` detector：大纲区间契约巡检（M02 B-2 缺口兜底）。

背景（M02 的 B-2 优化）：`render_section` 走 **O(子树)** 快路径 `get_section_nodes`
（区间扫 `ordinal ∈ [root, end)`，`end` = 下一个 `level <= root.level` 的标题），该路径
依赖不变量「**`ordinal` 序即大纲序**，且子树在区间内连续」；M02 加了**父链连通性自检 +
不合格自动回退递归 CTE**，但自检只能拦住「**多收**」（区间内出现不属于本子树的节点），
拦不住「**漏收**」——父链声明是后代、却因 `ordinal` 排布落在区间之外。本 detector 就是
这个反向残余风险的**巡检兜底**（Main 批准落地）。

判定口径（P5：区间法真值只有一处）
----------------------------------

判据**完全委托 M02 的诊断接口** `Storage.check_section_range(doc_id, node_id) -> bool|None`：
它比较「`_section_interval` 的**原始**结果（绕开自愈回退）」与「`get_subtree` 的递归 CTE」，
因此**两个方向都会暴露**——若直接比较公开读接口，快路径的自愈回退会让两者恒等而漏报。

* `True` → 区间法与 CTE 一致，干净；
* `False` → 契约破坏（**或节点不存在/已软删**）→ 本 detector 报违规；
* `None` → 该节点 `level` 为空、右边界不可判定 → 跳过（计入 skipped，不报违规）。

**消息里的定位信息**：CTE 侧序列取自 `get_subtree`（权威）；区间侧序列按 M02 docstring
**公开的右边界规则**（`min(ordinal) WHERE ordinal > root.ordinal AND level <= root.level`）
在内存里复原，**仅用于报出「两个行数 + 首个差异位置」**，不参与判定（判定权在
`check_section_range`）。若 M02 后续暴露更富的诊断（原始区间序列），本模块切换到它即可
（见与该模块的接口协调记录）。

抽样（性能）
------------

全量两两比较是 O(n²)，故**按文档抽样**：每文档取 `M09_SECTION_SAMPLE_SIZE`（默认 20）个
代表节点——根、最小 level（顶级章节）、区间边界（ordinal 首尾）、叶子、中间层各取代表，
再按等距填充——**确定性**（同文档同结果，无随机），覆盖大纲的各个结构性位置。
每样本 2 次查询（诊断 + CTE），成本 O(样本数 × 子树)。

**只读巡检**：不改任何数据；角色门槛由调用面（M11 `quality-gate`）决定，本 detector 无
特权要求（至少 reader）。
"""

from __future__ import annotations

import os
from collections.abc import Sequence
from typing import Final
from uuid import UUID

from agenticdocer.model import Doc, Node, Violation

from .context import GateContext

__all__ = [
    "DETECTOR_ID",
    "DEFAULT_SAMPLE_SIZE",
    "RULE_SECTION_RANGE_MISMATCH",
    "RULES_SECTION_RANGE",
    "detect",
    "judge_section_range",
    "sample_nodes",
    "sample_size",
]

DETECTOR_ID: Final = "section_range_consistency"

#: 违规规则 id。**命名说明**：Main 的要求里写作 `DTO_SECTION_RANGE_MISMATCH`，但 `DTO_*` 是
#: M12 的**日志错误码**口径（`error_code_for_rule(rule_id)` 按 rule_id 建键映射），而本模块
#: 的违规 id 一律为 `M09B.<判据>`（六个既有 detector 同口径）。故 rule_id 取
#: `M09B.section_range_mismatch`；日志侧 M12 对未登记 rule_id **原样透传**（其文档明示），
#: 故按规则名聚合仍可用。若需 `DTO_*` 正式登记，属 M12 文件（已同步该建议）。
RULE_SECTION_RANGE_MISMATCH: Final = "M09B.section_range_mismatch"
RULES_SECTION_RANGE: Final = (RULE_SECTION_RANGE_MISMATCH,)

DEFAULT_SAMPLE_SIZE: Final = 20
"""每文档抽样节点数（`M09_SECTION_SAMPLE_SIZE` 可覆盖）。"""

SAMPLE_SIZE_ENV: Final = "M09_SECTION_SAMPLE_SIZE"
_MAX_SAMPLE_SIZE: Final = 1000

FIX_HINT: Final = (
    "检查该节点及其后代的 `ordinal` 与 `parent_node_id` 是否自洽（契约：`ordinal` 序 = 大纲序，"
    "子树在 `[root.ordinal, 下一个 level ≤ root.level 的标题)` 区间内连续）；"
    "重解析入库（M03 commit 按 (level, ordinal) 栈重建 parent）通常即可修复"
)


def sample_size() -> int:
    """每文档抽样数：`M09_SECTION_SAMPLE_SIZE` → 默认 20（非法值回落默认，钳制到 [1, 1000]）。"""
    raw = os.environ.get(SAMPLE_SIZE_ENV)
    try:
        value = int(raw) if raw is not None else DEFAULT_SAMPLE_SIZE
    except ValueError:
        return DEFAULT_SAMPLE_SIZE
    return max(1, min(_MAX_SAMPLE_SIZE, value))


def sample_nodes(nodes: Sequence[Node], size: int) -> list[Node]:
    """**确定性**抽取代表节点（根 / 最小 level / 边界 / 叶子 / 中间层 / 等距填充）。

    只考虑 `level is not None` 的节点（`level` 空则区间右边界不可判定，诊断返回 `None`）。
    同一文档同一 `size` → 同一序列（无随机源）。
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

    parents = {node.node_id for node in candidates if node.parent_node_id is not None}
    child_parents = {node.parent_node_id for node in candidates if node.parent_node_id is not None}
    leaves = [node for node in candidates if node.node_id not in child_parents]
    middles = [node for node in candidates if node.node_id in child_parents and node.node_id in parents]
    roots = [node for node in candidates if node.parent_node_id is None]
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


def interval_ids(doc_nodes: Sequence[Node], root: Node) -> list[UUID]:
    """按 M02 **公开的右边界规则**复原区间 id 序列（**仅供消息定位**，不参与判定）。"""
    barriers = [
        node.ordinal
        for node in doc_nodes
        if node.ordinal > root.ordinal and node.level is not None and node.level <= (root.level or 0)
    ]
    end = min(barriers) if barriers else None
    return [
        node.node_id
        for node in doc_nodes
        if node.ordinal >= root.ordinal and (end is None or node.ordinal < end)
    ]


def _first_diff(left: Sequence[UUID], right: Sequence[UUID]) -> tuple[int, str, str]:
    """首个差异位置 + 两侧取值（长度不同而前缀相同 → 差异在截断点）。

    返回 `(index, 区间侧, CTE 侧)`：一侧缺失时该槽位标注「—（… 无此节点）」，故消息里两侧
    槽位**始终名副其实**（不会把区间侧的元素印到 CTE 槽里）。
    """
    for index in range(min(len(left), len(right))):
        if left[index] != right[index]:
            return index, str(left[index]), str(right[index])
    index = min(len(left), len(right))
    if len(left) > index:
        return index, str(left[index]), "—（CTE 无此节点）"
    if len(right) > index:
        return index, "—（区间无此节点）", str(right[index])
    return index, "—", "—"


def judge_section_range(
    doc_id: str,
    root: Node,
    interval: Sequence[UUID],
    subtree: Sequence[UUID],
) -> Violation | None:
    """区间序列 vs CTE 序列（纯函数）：相等 → `None`；不等 → 违规（含两行数与首个差异）。"""
    if list(interval) == list(subtree):
        return None
    index, interval_side, cte_side = _first_diff(interval, subtree)
    return Violation(
        rule_id=RULE_SECTION_RANGE_MISMATCH,
        path=f"nodes/{root.node_id}",
        message=(
            f"大纲区间契约被破坏（doc_id={doc_id}，节点 anchor={root.anchor!r}，level={root.level}）："
            f"区间法 {len(interval)} 行 vs 递归 CTE {len(subtree)} 行，"
            f"首个差异 @{index}（区间={interval_side}，CTE={cte_side}）"
            "——`ordinal` 序与大纲序不一致"
        ),
        fix_hint=FIX_HINT,
    )


async def _scoped_docs(ctx: GateContext) -> list[Doc]:
    docs = await ctx.storage.list_docs()
    if ctx.doc_ids is None:
        return docs
    wanted = set(ctx.doc_ids)
    return [doc for doc in docs if doc.doc_id in wanted]


async def detect(ctx: GateContext) -> list[Violation]:
    """按文档抽样，逐样本比较区间法与递归 CTE（只读；成环/深链由 M02 的深度上限保证终止）。"""
    size = sample_size()
    violations: list[Violation] = []
    samples = 0
    skipped = 0
    docs = await _scoped_docs(ctx)
    for doc in docs:
        nodes = await ctx.storage.get_doc_nodes(doc.doc_id)
        for root in sample_nodes(nodes, size):
            verdict = await ctx.storage.check_section_range(doc.doc_id, root.node_id)
            if verdict is None:
                skipped += 1
                continue
            if verdict:
                continue
            subtree = await ctx.storage.get_subtree(root.node_id, doc_id=doc.doc_id)
            if not subtree:
                # `False` 也覆盖「节点不存在」：当刻已消失（并发删除）→ 不是契约破坏
                skipped += 1
                continue
            samples += 1
            violation = judge_section_range(
                doc.doc_id, root, interval_ids(nodes, root), [node.node_id for node in subtree]
            )
            if violation is not None:
                violations.append(violation)
    ctx.logger.info(
        "section range scanned",
        docs=len(docs),
        sample_size=size,
        mismatches=samples,
        skipped_undecidable=skipped,
        violations=len(violations),
    )
    return violations
