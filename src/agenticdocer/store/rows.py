"""行 ↔ 模型 / 事件载荷的转换助手（M02 内部）。"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Final
from uuid import UUID

__all__ = ["UTC", "build_model", "field_deltas", "jsonable", "now", "row_to_dict"]

UTC: Final = timezone.utc


def now() -> datetime:
    """统一时间源（UTC，timestamptz）。"""
    return datetime.now(UTC)


def row_to_dict(row: Any) -> dict[str, Any]:
    """SQLAlchemy Core 行 → 普通 dict（列名 → 值）。"""
    return dict(row._mapping)


def build_model(cls: Any, data: Mapping[str, Any]) -> Any:
    """按列名字典构造 pydantic 模型。

    先按字段名校验（要求模型 `populate_by_name=True`，见 `_compat` 约定）；模型
    若因别名/额外字段拒绝，退回 `model_construct`——行数据来自本库自身，正确性由
    DB 约束保证，此处不应因序列化口径差异导致读路径失败。
    """
    fields = {k: v for k, v in data.items() if k in cls.model_fields}
    try:
        return cls(**fields)
    except Exception:  # noqa: BLE001 - 见 docstring：退回无校验构造
        return cls.model_construct(**fields)


def jsonable(value: Any) -> Any:
    """转为 JSONB 可序列化值（事件 payload 落库前必经）。"""
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Mapping):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [jsonable(v) for v in value]
    return value


def field_deltas(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    *,
    include_unchanged: bool = False,
) -> dict[str, dict[str, Any]]:
    """字段级 diff，形如 ``{field: {"before": x, "after": y}}``（§3.5 载荷口径）。

    - `create`：`field_deltas({}, row, include_unchanged=True)` → before 全为 `None`；
    - `delete`：`field_deltas(row, {}, include_unchanged=True)` → after 全为 `None`，即 before 全量；
    - `update`：`field_deltas(before_row, after_row)` → 仅变更字段。
    """
    keys: list[str] = [str(k) for k in before]
    keys += [str(k) for k in after if str(k) not in before]
    out: dict[str, dict[str, Any]] = {}
    for key in keys:
        old = before.get(key)
        new = after.get(key)
        if not include_unchanged and old == new:
            continue
        out[key] = {"before": jsonable(old), "after": jsonable(new)}
    return out
