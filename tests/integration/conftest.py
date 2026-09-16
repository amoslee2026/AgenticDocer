"""集成测试夹具：需要真实 PG（`DATABASE_URL`，默认测试库）。

PG 不可用（连不上/无凭据）时**整体 skip**，不 fail——CI 无库环境仍应全绿。

连接串：
- 应用角色：`TEST_DATABASE_URL` → `DATABASE_URL` → `...agenticdocer_app@.../agenticdocer_test`
- 属主角色（迁移用）：`MIGRATION_DATABASE_URL` → `...agenticdocer@.../agenticdocer_test`
"""

from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncIterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from agenticdocer.store import Database, Storage

ROOT = Path(__file__).resolve().parents[2]
APP_URL_DEFAULT = "postgresql+asyncpg://agenticdocer_app@127.0.0.1:5432/agenticdocer_test"
OWNER_URL_DEFAULT = "postgresql+asyncpg://agenticdocer@127.0.0.1:5432/agenticdocer_test"


def _app_url() -> str:
    return os.environ.get("TEST_DATABASE_URL") or os.environ.get("DATABASE_URL") or APP_URL_DEFAULT


def _owner_url() -> str:
    return os.environ.get("MIGRATION_DATABASE_URL") or OWNER_URL_DEFAULT


async def _probe(url: str) -> str | None:
    engine = create_async_engine(url, poolclass=NullPool)
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return None
    except Exception as exc:  # noqa: BLE001 - 任何连接问题都降级为 skip
        return f"{type(exc).__name__}: {exc}"
    finally:
        await engine.dispose()


async def _drop_and_recreate_public_schema(owner_url: str) -> None:
    engine = create_async_engine(owner_url, isolation_level="AUTOCOMMIT", poolclass=NullPool)
    try:
        async with engine.connect() as connection:
            await connection.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
            await connection.execute(text("CREATE SCHEMA public"))
            await connection.execute(text("GRANT USAGE ON SCHEMA public TO PUBLIC"))
    finally:
        await engine.dispose()


@pytest.fixture(scope="session")
def database_urls() -> tuple[str, str]:
    """`(owner_url, app_url)`；任一不可用 → skip 全部集成测试。"""
    owner, app = _owner_url(), _app_url()
    for label, url in (("migration/owner", owner), ("application", app)):
        error = asyncio.run(_probe(url))
        if error is not None:
            pytest.skip(f"PostgreSQL {label} URL 不可用（{url}）：{error}")
    return owner, app


@pytest.fixture(scope="session")
def migrated_schema(database_urls: tuple[str, str]) -> str:
    """重建 public schema 并 `alembic upgrade head`（会话一次）。"""
    owner, _ = database_urls
    asyncio.run(_drop_and_recreate_public_schema(owner))
    config = Config(str(ROOT / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", owner)
    command.upgrade(config, "head")
    return owner


@pytest.fixture
async def database(database_urls: tuple[str, str], migrated_schema: str) -> AsyncIterator[Database]:
    """应用角色的连接池（小池：测试并发低）。"""
    _, app = database_urls
    db = Database(app, pool_size=4, max_overflow=2)
    try:
        yield db
    finally:
        await db.dispose()


@pytest.fixture
def storage(database: Database, tmp_path: Path) -> Storage:
    """`Storage`（资产字节落 tmp_path，不污染仓库 data/） 。"""
    return Storage(database, store_dir=tmp_path / "assets")
