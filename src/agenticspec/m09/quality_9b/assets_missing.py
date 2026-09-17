"""M09B `assets_missing` detector：被引用资产缺失巡检（REQ-M03-F05 验收 / REQ-M09-F02）。

**取数完全委托 M02** `Storage.list_missing_assets`（P5 口径唯一）：库内资产引用只有一条口径
——`ASSET_HASH_PATTERN`（任意 sha256 令牌），它同时覆盖两种承载：

* `figure.content.asset_ref`（M03 从源图文件名提取的裸 sha256）；
* HTML/markdown 片段里**原样保留的源路径** `images/<sha256>.jpg`（P4 零改写直通）。

（`assets/<sha256>.<ext>` 是 **M04 渲染产物**里的重写形态，不是库内形态——故判据不能只认
它，否则「刚导入、未渲染」的文档会漏报全部缺失；M02 已按此口径统一扫描。）

判据：引用存在 ∧（`assets` 元数据行存在 ∧ CAS 字节文件存在）（A6：行在表、字节在
`ASSET_STORE_DIR`）。缺任一 → `M09B.asset.missing`。`assets` 不是 §3.5 的事件实体，故缺失
无法从 events 侧发现，只能靠本巡检。

作用域：全库 → 一次扫描；`doc_ids` 给定 → 逐文档扫描（吃 `nodes` 分区裁剪，且违规 `path`
带 `doc_id#` 前缀便于定位）。
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Final

from agenticspec.model import Violation

from .context import GateContext

__all__ = [
    "DETECTOR_ID",
    "RULES_ASSETS_MISSING",
    "detect",
    "judge_missing",
]

DETECTOR_ID: Final = "assets_missing"

RULE_ASSET_MISSING: Final = "M09B.asset.missing"
RULES_ASSETS_MISSING: Final = (RULE_ASSET_MISSING,)

FIX_HINT: Final = (
    "重新取件入库：M03 assets_sync.fetch_assets / M02 put_asset（内容寻址，asset_id=sha256），"
    "或修正 content 中的引用指向真实资产（源图缺失时按缺失清单补件后重导入）"
)


def judge_missing(asset_ids: Iterable[str], doc_id: str | None = None) -> list[Violation]:
    """缺失资产 id 序列 → 违规清单（纯函数；`path` 按文档定位，排序确定）。"""
    prefix = f"{doc_id}#" if doc_id is not None else ""
    scope = f"（doc_id={doc_id}）" if doc_id is not None else ""
    return [
        Violation(
            rule_id=RULE_ASSET_MISSING,
            path=f"{prefix}assets/{asset_id}",
            message=(
                f"节点 content 引用的资产缺失（assets 元数据行或 CAS 字节文件不存在）{scope}"
                f"：assets/{asset_id}"
            ),
            fix_hint=FIX_HINT,
        )
        for asset_id in sorted(set(asset_ids))
    ]


async def detect(ctx: GateContext) -> list[Violation]:
    """执行资产缺失巡检（全库一次扫描；按 `doc_ids` 作用域时逐文档扫描）。"""
    targets: Sequence[str | None] = ctx.doc_ids if ctx.doc_ids is not None else (None,)
    violations: list[Violation] = []
    for doc_id in targets:
        violations.extend(judge_missing(await ctx.storage.list_missing_assets(doc_id), doc_id))
    return violations
