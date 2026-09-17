"""initial schema：§4 DDL 13 表 + ADR-009 分区 + §4.3 角色授权

Revision ID: 0001_initial
Revises:
Create Date: 2026-09-16

本 revision 的表结构由 `agenticspec.store.schema.metadata` 直接落地——**单一来源**：
`store/schema.py` 是 DDL 的权威定义，此处不复制一份会漂移的字面 DDL。
约束：后续任何结构变更都必须（a）改 `schema.py` 并（b）新增一个 revision 用
`op.*` 显式写出增量（不要依赖本文件重新生成），否则「新建库」与「升级库」会分叉。

ADR-009 落地项：
- `nodes` HASH(doc_id) 64 分区、`events` RANGE(ts) 按月 + DEFAULT 兜底（V3）；
- 主键含分区键：`nodes(node_id, doc_id)`、`events(event_id, ts)`；
- 6 处外键降级为应用层校验（不建 REFERENCES，见 `schema.py` 注释）；
- §4.3 授权口径：`events` 及其分区只授 SELECT/INSERT（P2 append-only）。
"""

from __future__ import annotations

from alembic import op
from sqlalchemy import text

from agenticspec.store import schema

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def _notice(message: str) -> None:
    """把迁移期的跳过原因以 PG NOTICE 输出（不引入 logging）。"""
    op.execute(text(f"DO $do$ BEGIN RAISE NOTICE '{message}'; END $do$"))


def upgrade() -> None:
    bind = op.get_bind()

    schema.metadata.create_all(bind=bind)

    for statement in schema.nodes_partition_statements():
        op.execute(statement)
    for statement in schema.events_partition_statements():
        op.execute(statement)

    statements, notes = schema.privilege_statements(bind)
    for statement in statements:
        op.execute(statement)
    for note in notes:
        _notice(note)


def downgrade() -> None:
    schema.metadata.drop_all(bind=op.get_bind())
    # 注：GRANT/REVOKE 与 ALTER DEFAULT PRIVILEGES 不随本 revision 回滚（角色级设置，
    # 由运维按 §4.3 显式管理）。
