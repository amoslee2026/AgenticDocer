"""`Storage`：§3 M02 契约的单一装配点（组合各实体仓储，共享同一 `Database`）。"""

from __future__ import annotations

from pathlib import Path

from .assets import AssetRepository, asset_store_dir
from .comments import CommentRepository
from .db import Database
from .docs import DocRepository
from .events import EventRepository
from .nodes import NodeRepository
from .refs import RefRepository
from .repository import Repository

__all__ = ["Storage", "get_storage"]


class Storage(
    NodeRepository,
    DocRepository,
    RefRepository,
    CommentRepository,
    AssetRepository,
    EventRepository,
):
    """M02 完整读写面。

    写方法一律携带 `ctx: WriteContext`，并在单事务内写「事件 + 实体」（P2）。
    各仓储共享同一连接池；`db=None` 取进程级单例（`DATABASE_URL`）。
    """
    def __init__(self, db: Database | None = None, *, store_dir: Path | str | None = None) -> None:
        Repository.__init__(self, db)
        self.store_dir = Path(store_dir) if store_dir is not None else asset_store_dir()
        self.store_dir = Path(asset_store_dir) if asset_store_dir is not None else asset_store_dir()


def get_storage() -> Storage:
    """进程级装配（M06/M07 应用启动用）。"""
    return Storage()
