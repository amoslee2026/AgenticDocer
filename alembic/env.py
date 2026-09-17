"""Alembic 环境（async engine，asyncpg）。

- `target_metadata` = `agenticspec.store.schema.metadata`（§4 DDL 的单一来源）；
- 连接串取 `MIGRATION_DATABASE_URL`（属主角色，§4.3）→ `DATABASE_URL` → 默认；
- 迁移用 `NullPool`：一次性进程，不复用连接池。
"""

from __future__ import annotations

import asyncio

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from agenticspec.store import schema
from agenticspec.store.db import migration_database_url

config = context.config

target_metadata = schema.metadata


def _url() -> str:
    configured = (config.get_main_option("sqlalchemy.url") or "").strip()
    return configured or migration_database_url()


def run_migrations_offline() -> None:
    """离线模式：只生成 SQL（`alembic upgrade head --sql`）。"""
    context.configure(
        url=_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        {"sqlalchemy.url": _url()},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
