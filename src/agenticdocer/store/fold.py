"""事件折叠（`apply_events`）——严格按 §3.5「事件载荷与折叠规范」表实现。

纯函数：不触库、不读环境，同一事件序列恒得同一结果（REQ-M02-F03 重放、M09B
`events_consistency` 巡检的可判定基础）。

| entity | op | 折叠 |
|---|---|---|
| doc | create/update/status | 逐字段覆盖到 doc 行快照 |
| node | create/update/delete | create 建快照；update 逐字段覆盖；delete 置 `status=deleted` |
| ref | add/remove | add 追加 refs 行；remove 移除对应行 |
| comment | create/update | 逐字段覆盖批注快照 |
| schema | create/update | 记录 schema 版本历史 |
| auth | login/logout/fail/user_change/grant_change/key_change | 追加（不参与实体折叠，仅审计） |

载荷口径（写入侧见 `events.py`，与本模块互为契约）：

- doc/node/comment/schema：`{field: {"before": x, "after": y}}`；
  `create` 时 before 恒为 `None`，`delete` 时 after 恒为 `None` 且覆盖**全字段**
  （即 §3.5 的「delete 含 before 全量」）；
- ref：扁平 `{src, dst_doc, dst_node, kind}`；
- auth：扁平 `{user_id, key_fingerprint?, ip?, reason?}`。

为兼容「整行形态」的历史/外部载荷，`{"before": {...}}` 亦被接受；扁平字段值按
`after` 解释。
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Final

from agenticdocer.model import Comment, Doc, Event, Node, NodeSnapshot
from .errors import ValidationError
from .rows import build_model, jsonable

__all__ = ["ENTITY_OPS", "apply_events", "entity_ops"]

ENTITY_OPS: Final[dict[str, tuple[str, ...]]] = {
    "doc": ("create", "update", "status"),
    "node": ("create", "update", "delete"),
    "ref": ("add", "remove"),
    "comment": ("create", "update"),
    "schema": ("create", "update"),
    "auth": ("login", "logout", "fail", "user_change", "grant_change", "key_change"),
}
"""§3.5 表的 (entity, op) 取值域；`events.op` 在 DDL 层为自由文本，取值域由本表约束。"""


def entity_ops(entity: str) -> tuple[str, ...]:
    """实体的合法 op 集合（未知实体 → ValidationError）。"""
    try:
        return ENTITY_OPS[entity]
    except KeyError:
        raise ValidationError(
            f"unknown event entity {entity!r}; expected one of {sorted(ENTITY_OPS)}",
            entity=entity,
        ) from None


def _normalize_payload(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """载荷 → `{field: {"before": x, "after": y}}` 的统一形态。"""
    if not payload:
        return {}
    if set(payload) <= {"before", "after"} and isinstance(payload.get("before"), dict):
        before = payload.get("before") or {}
        after = payload.get("after") or {}
        keys = list(before) + [k for k in after if k not in before]
        return {k: {"before": before.get(k), "after": after.get(k)} for k in keys}
    deltas: dict[str, dict[str, Any]] = {}
    for field, value in payload.items():
        if isinstance(value, dict) and ("before" in value or "after" in value):
            deltas[field] = {"before": value.get("before"), "after": value.get("after")}
        else:
            deltas[field] = {"before": None, "after": value}
    return deltas


def _check_op(entity: str, ev: Event) -> None:
    ops = entity_ops(entity)
    if ev.op not in ops:
        raise ValidationError(
            f"op {ev.op!r} is not valid for entity {entity!r}; expected one of {list(ops)}",
            entity=entity,
            entity_id=ev.entity_id,
        )


def _apply_deltas(state: dict[str, Any], payload: dict[str, Any]) -> None:
    for field, delta in _normalize_payload(payload).items():
        state[field] = delta["after"]


def _apply_delete(state: dict[str, Any], payload: dict[str, Any]) -> None:
    """delete：以 before 全量复原（`after` 为 None 的字段取 `before`）。"""
    for field, delta in _normalize_payload(payload).items():
        state[field] = delta["before"] if delta["after"] is None else delta["after"]
    state["status"] = "deleted"


def _fold_node(events: Sequence[Event]) -> NodeSnapshot:
    state: dict[str, Any] = {}
    for ev in events:
        _check_op("node", ev)
        payload = ev.payload or {}
        if ev.op == "create":
            _apply_deltas(state, payload)
            state.setdefault("node_id", ev.entity_id)
            state.setdefault("status", "active")
            state.setdefault("version", 1)
        elif ev.op == "update":
            _apply_deltas(state, payload)
        else:  # delete
            _apply_delete(state, payload)
    node = build_model(Node, state) if state else None
    return NodeSnapshot(node=node, history=list(events))


def _fold_record(events: Sequence[Event], entity: str, cls: Any) -> dict[str, Any]:
    state: dict[str, Any] = {}
    for ev in events:
        _check_op(entity, ev)
        _apply_deltas(state, ev.payload or {})
        state.setdefault(_ID_FIELD[entity], ev.entity_id)
    return build_model(cls, state).model_dump()


_ID_FIELD: Final[dict[str, str]] = {"doc": "doc_id", "comment": "comment_id"}


def _ref_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (row.get("src_node_id"), row.get("dst_doc_id"), row.get("dst_node_id"), row.get("kind"))


def _fold_ref(events: Sequence[Event]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for ev in events:
        _check_op("ref", ev)
        payload = ev.payload or {}
        row = {
            "src_node_id": payload.get("src"),
            "dst_doc_id": payload.get("dst_doc"),
            "dst_node_id": payload.get("dst_node"),
            "kind": payload.get("kind"),
        }
        if ev.op == "add":
            if _ref_key(row) not in {_ref_key(r) for r in rows}:
                rows.append(row)
        elif _ref_key(row) in {_ref_key(r) for r in rows}:
            rows = [r for r in rows if _ref_key(r) != _ref_key(row)]
    return {"refs": rows}


def _fold_schema(events: Sequence[Event]) -> dict[str, Any]:
    versions: list[dict[str, Any]] = []
    type_name: str | None = None
    for ev in events:
        _check_op("schema", ev)
        payload = ev.payload or {}
        type_name = payload.get("type_name", type_name or ev.entity_id)
        versions.append(
            {
                "type_name": type_name,
                "version": payload.get("version"),
                "diff": jsonable(payload.get("diff")),
                "event_id": ev.event_id,
                "ts": ev.ts,
            }
        )
    return {
        "type_name": type_name,
        "versions": versions,
        "current_version": versions[-1]["version"] if versions else None,
    }


def _fold_auth(events: Sequence[Event]) -> dict[str, Any]:
    for ev in events:
        _check_op("auth", ev)
    return {"audit": [ev.model_dump() for ev in events]}


def apply_events(entity: str, events: Sequence[Event]) -> NodeSnapshot | dict[str, Any]:
    """按 §3.5 折叠事件序列。

    - `node` → `NodeSnapshot`（`node=None` 表示序列未含任何可重建状态的事件）；
    - `doc`/`comment` → 行快照 dict；
    - `ref` → `{"refs": [...]}`（行集重建）；
    - `schema` → 版本历史 dict；
    - `auth` → `{"audit": [...]}`（仅审计，不折叠）。
    """
    entity_ops(entity)
    if entity == "node":
        return _fold_node(events)
    if entity == "doc":
        return _fold_record(events, "doc", Doc)
    if entity == "comment":
        return _fold_record(events, "comment", Comment)
    if entity == "ref":
        return _fold_ref(events)
    if entity == "schema":
        return _fold_schema(events)
    return _fold_auth(events)
