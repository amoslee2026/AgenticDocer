"""仓储基类：统一持有 `Database`（缺省取进程级单例）。"""

from __future__ import annotations

from .db import Database, get_database

__all__ = ["Repository"]


class Repository:
    """各实体仓储的公共基类。

    `db` 为 `None` 时使用 `get_database()`（`DATABASE_URL` 单例）——便于 M06/M07
    在应用启动时直接装配 `Storage()`；测试注入独立 `Database`。
    """

    def __init__(self, db: Database | None = None) -> None:
        self.db: Database = db if db is not None else get_database()
