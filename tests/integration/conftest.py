"""集成测试夹具：需要真实 PG（`TEST_DATABASE_URL`，默认测试库）。

PG 不可用（连不上 / 无凭据）时**整体 skip**，不 fail——无库环境仍应全绿。

连接串（`.env` 由 `agenticdocer.store.db` 作为默认值注入）：
- 应用角色：`TEST_DATABASE_URL` → `DATABASE_URL` → `...agenticdocer_app@.../agenticdocer_test`
- 迁移（属主）：应用连接串的**同一库** + `MIGRATION_DATABASE_URL` 的属主凭据。

安全闸：夹具会 `DROP SCHEMA public CASCADE`，故库名必须以 `_test` 结尾，否则直接报错
（避免误清生产/开发库）。
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
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from agenticdocer.store import Database, Storage

ROOT = Path(__file__).resolve().parents[2]
APP_URL_DEFAULT = "postgresql+asyncpg://agenticdocer_app@127.0.0.1:5432/agenticdocer_test"
OWNER_URL_DEFAULT = "postgresql+asyncpg://agenticdocer@127.0.0.1:5432/agenticdocer_test"


def _app_url() -> str:
    return os.environ.get("TEST_DATABASE_URL") or os.environ.get("DATABASE_URL") or APP_URL_DEFAULT


def _owner_url(app_url: str) -> str:
    """属主凭据 + **同一个（测试）库**。

    只替换用户名/口令，不采用 `MIGRATION_DATABASE_URL` 的库名——那指向 `agenticdocer`
    （开发/生产库），而本夹具会 `DROP SCHEMA public CASCADE`。
    """
    application = make_url(app_url)
    owner = make_url(os.environ.get("MIGRATION_DATABASE_URL") or OWNER_URL_DEFAULT)
    # 注意：`str(URL)` 会掩码口令（hide_password=True），连接串必须显式 render。
    return application.set(username=owner.username, password=owner.password).render_as_string(
        hide_password=False
    )


def _masked(url: str) -> str:
    return make_url(url).render_as_string(hide_password=True)


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
    app = _app_url()
    database = make_url(app).database or ""
    if not database.endswith("_test"):
        raise pytest.UsageError(
            f"集成测试会 DROP SCHEMA public，仅允许 *_test 库；当前库为 {database!r}（{_masked(app)}）"
        )
    owner = _owner_url(app)
    for label, url in (("migration/owner", owner), ("application", app)):
        error = asyncio.run(_probe(url))
        if error is not None:
            pytest.skip(f"PostgreSQL {label} 连接不可用（{_masked(url)}）：{error}")
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
    """`Storage`（资产字节落 tmp_path，不污染仓库 `data/`）。"""
    return Storage(database, store_dir=tmp_path / "assets")
