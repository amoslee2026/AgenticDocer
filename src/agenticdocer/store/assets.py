"""资产仓储（REQ-M02-F06、A6）：元数据落 `assets` 表，字节落文件系统 CAS。

- 路径：`ASSET_STORE_DIR/<sha256[:2]>/<sha256>.<ext>`（A6），`assets.path` 记相对路径；
- 幂等去重：同 sha256 不重复落盘、不重复插行；
- 无事件：`assets` 不是 §3.5 的事件实体域（不在 `ENTITY_OPS` 中）；
- 引用口径：库内引用是 **sha256 令牌**（非渲染产物形态），见 `ASSET_HASH_PATTERN`。
"""

from __future__ import annotations

import asyncio
import hashlib
import mimetypes
import os
import re
from pathlib import Path
from typing import Any, Final

from sqlalchemy import insert, select, text

from agenticdocer.model import Asset
from .errors import NotFoundError
from .repository import Repository
from .rows import build_model, row_to_dict
from .schema import assets

__all__ = [
    "ASSET_HASH_PATTERN",
    "ASSET_REF_PATTERN",
    "AssetRepository",
    "asset_store_dir",
]

_REPO_ROOT: Final = Path(__file__).resolve().parents[3]
"""`src/agenticdocer/store/assets.py` → 仓库根。"""

DEFAULT_ASSET_STORE_DIR: Final = _REPO_ROOT / "data" / "assets"

ASSET_HASH_PATTERN: Final = re.compile(r"[0-9a-f]{64}")
"""**库内引用口径**：任意出现的 sha256 令牌即资产引用（P5 口径唯一）。

库内（`nodes.content`）有两种承载：`figure.content.asset_ref`（裸 sha256，M03 解析器写入）
与 HTML/markdown 片段里保留的**源路径**（`images/<sha256>.jpg`，P4 零改写直通）。
`assets/<sha256>.<ext>` 只出现在 **M04 渲染产物**里，不是库内形态——故不能只认后者。
M04 的解析器用同一规则（其 `_HASH_TOKEN`），M02 不依赖 M04（P3 单向依赖），故规则定义在此层。
"""

ASSET_REF_PATTERN: Final = re.compile(r"assets/([0-9a-f]{64})\.[A-Za-z0-9]+")
"""渲染产物形态 `assets/<sha256>.<ext>`（§3 M04，M04 渲染器按此解析）。"""


def asset_store_dir() -> Path:
    """`ASSET_STORE_DIR`（§5 环境变量），默认仓库 `data/assets`。"""
    return Path(os.environ.get("ASSET_STORE_DIR", DEFAULT_ASSET_STORE_DIR))


def _extension(mime: str) -> str:
    extension = mimetypes.guess_extension(mime) or ".bin"
    return "jpg" if extension == ".jpe" else extension.lstrip(".")


class AssetRepository(Repository):
    """§3 M02 的资产读写面。"""

    def __init__(self, db: Any = None, *, store_dir: Path | None = None) -> None:
        super().__init__(db)
        self.store_dir = Path(store_dir) if store_dir is not None else asset_store_dir()

    def _relative_path(self, asset_id: str, mime: str) -> Path:
        return Path(asset_id[:2]) / f"{asset_id}.{_extension(mime)}"

    async def put_asset(self, data: bytes, mime: str, origin: str | None = None) -> str:
        """写入资产，返回 `asset_id`（sha256 hex）；同内容幂等。

        顺序：先落文件（内容寻址，重写等价）→ 再插元数据行，避免留下「有行无字节」的
        悬空记录；反向残留（有字节无行）无害，重跑会补齐。
        """
        asset_id = hashlib.sha256(data).hexdigest()
        relative = self._relative_path(asset_id, mime)
        destination = self.store_dir / relative

        def _write() -> None:
            destination.parent.mkdir(parents=True, exist_ok=True)
            if not destination.exists():
                destination.write_bytes(data)

        await asyncio.to_thread(_write)
        async with self.db.transaction() as session:
            existing = (
                await session.execute(select(assets.c.asset_id).where(assets.c.asset_id == asset_id))
            ).first()
            if existing is None:
                await session.execute(
                    insert(assets).values(
                        asset_id=asset_id,
                        mime=mime,
                        bytes=len(data),
                        origin=origin,
                        path=str(relative),
                    )
                )
        return asset_id

    async def get_asset(self, asset_id: str) -> Asset:
        async with self.db.session() as session:
            row = (
                await session.execute(select(*tuple(assets.c)).where(assets.c.asset_id == asset_id))
            ).first()
        if row is None:
            raise NotFoundError(f"asset {asset_id} not found", entity="asset", entity_id=asset_id)
        return build_model(Asset, row_to_dict(row))

    async def get_asset_path(self, asset_id: str) -> Path:
        """资产字节路径（校验行与文件同时存在）。"""
        record = await self.get_asset(asset_id)
        path = self.store_dir / record.path
        if not await asyncio.to_thread(path.exists):
            raise NotFoundError(
                f"asset {asset_id} metadata exists but bytes are missing at {path}",
                entity="asset",
                entity_id=asset_id,
            )
        return path

    async def get_asset_paths(self, asset_ids: Iterable[str]) -> dict[str, Path]:
        """批量取资产字节路径（PERF B-2：消 N+1）。

        单条 `WHERE asset_id = ANY(...)` 取回全部元数据行，再一次线程内 `stat` 校验字节
        存在性——M04 章节渲染对 1,099 处图片引用逐个 `get_asset_path` 的顺序往返由此消除。

        **缺失项不出现在返回值里**（元数据缺行或字节缺失），调用方按「解析不到 → 原样直通
        （P4）」处置；需要报缺失时用 `list_missing_assets`。
        """
        wanted = [asset_id for asset_id in dict.fromkeys(asset_ids) if asset_id]
        if not wanted:
            return {}
        async with self.db.session() as session:
            rows = (
                await session.execute(
                    select(assets.c.asset_id, assets.c.path).where(
                        assets.c.asset_id.in_(wanted)
                    )
                )
            ).all()
        candidates = {row.asset_id: self.store_dir / row.path for row in rows}

        def _existing() -> dict[str, Path]:
            return {asset_id: path for asset_id, path in candidates.items() if path.exists()}

        return await asyncio.to_thread(_existing)

    async def list_missing_assets(self, doc_id: str | None = None) -> list[str]:
        """被节点引用但**元数据或字节缺失**的 asset_id 列表（M09B `assets_missing` 判据）。

        引用口径 = `ASSET_HASH_PATTERN`（任意 sha256 令牌）：覆盖 `figure.content.asset_ref`
        的裸 sha、HTML/markdown 片段里原样保留的源路径（`images/<sha256>.jpg`）与渲染产物的
        `assets/<sha256>.<ext>` —— 只认后者会在「刚导入、未渲染」的文档上漏报全部缺失。
        扫描在 PG 侧用 `regexp_matches(..., 'g')` 完成，不把 13M 行拉进 Python。
        """
        # 两种形态分别成句：`:doc_id IS NULL` 这类「裸 NULL 参数」在 asyncpg 下无法
        # 推断类型（AmbiguousParameterError），且按 doc_id 过滤还能吃分区裁剪。
        # 捕获组来自同一个常量（P5 口径唯一）；PG 的 regexp_matches 需要显式分组。
        pattern = f"({ASSET_HASH_PATTERN.pattern})"
        if doc_id is None:
            statement = text(
                "SELECT DISTINCT m[1] AS asset_id FROM ("
                "  SELECT regexp_matches(content::text, :pattern, 'g') AS m FROM nodes"
                "  WHERE status = 'active'"
                ") AS matched"
            )
            params: dict[str, Any] = {"pattern": pattern}
        else:
            statement = text(
                "SELECT DISTINCT m[1] AS asset_id FROM ("
                "  SELECT regexp_matches(content::text, :pattern, 'g') AS m FROM nodes"
                "  WHERE status = 'active' AND doc_id = :doc_id"
                ") AS matched"
            )
            params = {"pattern": pattern, "doc_id": doc_id}
        async with self.db.session() as session:
            referenced = list((await session.execute(statement, params)).scalars())
            known = {
                row.asset_id: Path(row.path)
                for row in (
                    await session.execute(
                        select(assets.c.asset_id, assets.c.path).where(
                            assets.c.asset_id.in_(referenced or [""])
                        )
                    )
                )
            }
        missing: list[str] = []
        for asset_id in sorted(referenced):
            relative = known.get(asset_id)
            if relative is None or not await asyncio.to_thread(
                (self.store_dir / relative).exists
            ):
                missing.append(asset_id)
        return missing
