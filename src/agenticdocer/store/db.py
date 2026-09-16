"""M02 数据库连接与事务（SQLAlchemy 2.0 async + asyncpg）。

池参数按 ADR-009 §3：`pool_size=20, max_overflow=20`（每 worker 上限 40）。
所有写路径经 `Database.transaction()`，保证「事件 + 实体同事务」（§1 P2）。

配置取值顺序（§5「环境变量」）：进程环境变量 → 仓库 `.env` → 本模块默认值。
`.env` 仅作**默认值**注入（`setdefault`），已存在的环境变量永不被覆盖。
"""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Final

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


ENV_FILE: Final = Path(
    os.environ.get("AGENTICDOCER_ENV_FILE") or Path(__file__).resolve().parents[3] / ".env"
)
"""仓库级 `.env`（gitignore；§5 开发期配置）。"""


def _load_env_file(path: Path) -> None:
    """把 `.env` 的键值作为默认值注入 `os.environ`（环境变量优先）。"""
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return
    for raw in content.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.removeprefix("export ").strip()
        if key:
            os.environ.setdefault(key, value.strip().strip('"').strip("'"))


_load_env_file(ENV_FILE)

__all__ = [
    "DEFAULT_DATABASE_URL",
    "DEFAULT_MIGRATION_DATABASE_URL",
    "MAX_OVERFLOW",
    "POOL_SIZE",
    "Database",
    "database_url",
    "get_database",
    "migration_database_url",
]

DEFAULT_DATABASE_URL: Final = "postgresql+asyncpg://agenticdocer_app@127.0.0.1:5432/agenticdocer_test"
"""§5/§3 M02 约定的应用连接串（测试库；无密码，凭据由环境变量提供）。"""

DEFAULT_MIGRATION_DATABASE_URL: Final = "postgresql+asyncpg://agenticdocer@127.0.0.1:5432/agenticdocer"
"""迁移连接串：§4.3 的**属主**角色（建表/GRANT/REVOKE），与应用角色分离（A15 双层防护）。"""

POOL_SIZE: Final = 20
MAX_OVERFLOW: Final = 20


def database_url() -> str:
    """应用连接串（`DATABASE_URL`，最小权限角色 `agenticdocer_app`）。"""
    return os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)


def migration_database_url() -> str:
    """迁移连接串：`MIGRATION_DATABASE_URL` → `DATABASE_URL` → 属主默认（alembic 专用）。"""
    return (
        os.environ.get("MIGRATION_DATABASE_URL")
        or os.environ.get("DATABASE_URL")
        or DEFAULT_MIGRATION_DATABASE_URL
    )


class Database:
    """连接池 + 会话/事务工厂。

    `create_async_engine` 不建立连接，故构造即建引擎（懒连接）。
    """

    def __init__(
        self,
        url: str | None = None,
        *,
        pool_size: int = POOL_SIZE,
        max_overflow: int = MAX_OVERFLOW,
        echo: bool = False,
    ) -> None:
        self.url = url or database_url()
        self.engine: AsyncEngine = create_async_engine(
            self.url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_pre_ping=True,
            pool_recycle=1800,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """只读会话（不自动提交）。"""
        async with self.session_factory() as session:
            yield session

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[AsyncSession]:
        """读写事务：正常退出提交，异常整体回滚（事件与实体同生共死，P2）。"""
        async with self.session_factory() as session:
            async with session.begin():
                yield session

    async def dispose(self) -> None:
        """释放连接池（进程退出 / 测试 teardown）。"""
        await self.engine.dispose()


_database: Database | None = None


def get_database(url: str | None = None) -> Database:
    """进程级单例（未显式给 url 时复用）。"""
    global _database
    if url is not None or _database is None:
        _database = Database(url)
    return _database
