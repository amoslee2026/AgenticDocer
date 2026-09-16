"""M09B `assets_missing` detector：被引用资产缺失巡检（REQ-M03-F05 验收 / REQ-M09-F02）。

两条引用口径都查（P5：库内引用只有这两种形态）：

1. **渲染期重写口径** `assets/<sha256>.<ext>`——M04 渲染时把图片 `src` 重写成的库内相对
   路径（§3 M02 `ASSET_REF_PATTERN`）。取数直接委托 M02 `list_missing_assets`（PG 侧正则
   去重，避免把大 `content` 拉进 Python）；
2. **原子字段口径** `figure.content.asset_ref`（sha256 hex，M01 schema）——M03 从源图文件名
   提取、不经字符串扫描，是 M02 那条扫描**看不到**的引用面；本 detector 补上它。

两条口径都判「元数据行存在 ∧ 字节文件存在」（A6：字节落 CAS 目录，行在 `assets` 表），
缺任一 → `M09B.asset.missing`。`assets` 表本身不是事件实体（§3.5 无 asset 事件），故缺失
只能靠巡检发现，不会体现在 events 里。
"""

from __future__ import annotations

import asyncio
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Final

from sqlalchemy import Select, select

from agenticdocer.model import Violation
from agenticdocer.store.schema import assets, nodes

from .context import GateContext

__all__ = [
    "DETECTOR_ID",
    "RULES_ASSETS_MISSING",
    "detect",
    "judge_figure_refs",
]

DETECTOR_ID: Final = "assets_missing"

RULE_ASSET_MISSING: Final = "M09B.asset.missing"
RULES_ASSETS_MISSING: tuple[str, ...] = (RULE_ASSET_MISSING,)

FIGURE_ATOMS: Final[tuple[str, ...]] = ("figure", "figure.state_machine")
"""带 `content.asset_ref` 的原子（M01 schema）。"""

_MISSING_FIX: Final = (
    "重新取件入库：M03 assets_sync.fetch_assets / M02 put_asset（内容寻址，asset_id=sha256），"
    "或修正 content 中的引用指向真实资产"
)


def judge_figure_refs(
    rows: Sequence[Mapping[str, Any]],
    stored_paths: Mapping[str, str],
    *,
    present: Sequence[str],
) -> list[Violation]:
    """`figure.asset_ref` 判据（纯函数）。

    :param rows: `{node_id, doc_id, asset_ref}`（`asset_ref` 非空）
    :param stored_paths: `assets.asset_id → assets.path`（已查得行）
    :param present: 实际存在于 CAS 目录的 `asset_id` 列表
    """
    on_disk = set(present)
    violations: list[Violation] = []
    for row in rows:
        asset_id = str(row["asset_ref"])
        path = f"nodes/{row['node_id']}#content.asset_ref"
        if asset_id not in stored_paths:
            violations.append(
                Violation(
                    rule_id=RULE_ASSET_MISSING,
                    path=path,
                    message=(
                        f"figure 原子引用的资产无元数据行：asset_ref={asset_id}"
                        f"（doc_id={row['doc_id']}）"
                    ),
                    fix_hint=_MISSING_FIX,
                )
            )
        elif asset_id not in on_disk:
            violations.append(
                Violation(
                    rule_id=RULE_ASSET_MISSING,
                    path=path,
                    message=(
                        f"figure 原子引用的资产字节缺失：asset_ref={asset_id}，"
                        f"assets.path={stored_paths[asset_id]!r}（doc_id={row['doc_id']}）"
                    ),
                    fix_hint=_MISSING_FIX,
                )
            )
    return violations


def _figure_statement(doc_ids: Sequence[str] | None) -> Select[Any]:
    statement = (
        select(
            nodes.c.node_id,
            nodes.c.doc_id,
            nodes.c.content.op("->>")("asset_ref").label("asset_ref"),
        )
        .where(
            nodes.c.atom_type.in_(FIGURE_ATOMS),
            nodes.c.status == "active",
            nodes.c.content.op("->>")("asset_ref").is_not(None),
        )
        .order_by(nodes.c.doc_id, nodes.c.ordinal)
    )
    if doc_ids is not None:
        statement = statement.where(nodes.c.doc_id.in_(tuple(doc_ids)))
    return statement


async def _figure_violations(ctx: GateContext) -> list[Violation]:
    """`asset_ref` 口径：一条查行 + 一次存在性判定（CAS 目录 IO 用线程池，避免阻塞循环）。"""
    async with ctx.storage.db.session() as session:
        rows = (await session.execute(_figure_statement(ctx.doc_ids))).mappings().all()
        if not rows:
            return []
        referenced = sorted({str(row["asset_ref"]) for row in rows})
        stored = {
            row.asset_id: row.path
            for row in (
                await session.execute(
                    select(assets.c.asset_id, assets.c.path).where(
                        assets.c.asset_id.in_(referenced)
                    )
                )
            )
        }
    store_dir = Path(ctx.storage.store_dir)
    present = await asyncio.gather(
        *(
            asyncio.to_thread((store_dir / relative).is_file)
            for relative in (stored[asset_id] for asset_id in stored)
        )
    )
    on_disk = [asset_id for asset_id, exists in zip(stored, present, strict=True) if exists]
    return judge_figure_refs(rows, stored, present=on_disk)


async def detect(ctx: GateContext) -> list[Violation]:
    """执行资产缺失巡检（渲染期重写口径 + `asset_ref` 字段口径）。"""
    violations: list[Violation] = []
    targets: tuple[str | None, ...] = ctx.doc_ids if ctx.doc_ids is not None else (None,)
    for doc_id in targets:
        for asset_id in await ctx.storage.list_missing_assets(doc_id):
            scope = f"{doc_id}#" if doc_id is not None else ""
            violations.append(
                Violation(
                    rule_id=RULE_ASSET_MISSING,
                    path=f"{scope}assets/{asset_id}",
                    message=(
                        f"节点 content 引用的资产缺失（元数据或字节）：assets/{asset_id}"
                        + (f"（doc_id={doc_id}）" if doc_id is not None else "")
                    ),
                    fix_hint=_MISSING_FIX,
                )
            )
    violations.extend(await _figure_violations(ctx))
    return violations
