"""M-LR 增量事件流（REQ-MLR-F02；架构规范 §3 M-LR、§3.5；ADR-009 §1/§4）。

:func:`change_stream` 是**基于 `events` 的游标流**（只读、无 LLM、无网络，P6/C7），
供 lightRAG 增量消费。

**定序与游标语义**（与 M02 :meth:`~agenticdocer.store.events.EventRepository.changes_since`
同一口径，是本模块的权威定义）：

* 全序键 = ``(ts, event_id)``。``ts`` 为 UTC timestamptz；同一毫秒内的多条事件由
  ``event_id``（UUIDv7，时间有序）定序。**只看 `ts` 会在同毫秒边界上跳过事件**，
  故续拉游标一律携带 ``event_id``。
* 区间取**半开**：``(ts, event_id) > 游标`` → 不重不漏。
* 分区（ADR-009 §1：``events`` 按 ``ts`` RANGE 月分区）对调用方透明：查询走父表，
  PG 自动合并各分区；``event_id`` 内嵌毫秒时间戳（``uuid7_timestamp_ms``）用于**定位游标**。
  归档分区（ADR-009 §4：``DETACH`` 到 ``events_archive``）改走 ``events_all`` 视图的动作
  在 M02 内完成，本模块不受影响。

**`since` 三形态**（:func:`cursor_token` 是官方产出形态）：

1. ``None`` / ``""``——从头（最早事件）开始；
2. ``"<ts_iso>@<event_id>"``——:func:`cursor_token` 的产物，**精确**续拉；
3. ``"<event_id>"``（裸 UUIDv7）——精确续拉，但 `ts` 需先从库里解析（:func:`_resolve_exact`；
   按 `event_id` 内嵌毫秒起扫，窗口与批数有界）；
4. ``"<ts_iso>"``——**粗粒度**时间游标：``ts > 该时刻``。同一时刻的其余事件会被跳过，
   仅用于「拉某时刻之后的变更」这类场景；续拉请用形态 2。

游标字符串由消费方自己持久化——流的每个 :class:`~agenticdocer.model.Event` 都可用
:func:`cursor_token` 转成续拉 token。
"""

from __future__ import annotations

import asyncio
import re
from contextlib import nullcontext
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Final
from uuid import UUID

from agenticdocer.model import Event, is_uuid7, uuid7_timestamp_ms
from agenticdocer.observability import get_logger
from agenticdocer.store import Storage, ValidationError

__all__ = [
    "CURSOR_SEPARATOR",
    "DEFAULT_BATCH_SIZE",
    "DEFAULT_POLL_INTERVAL",
    "change_stream",
    "cursor_token",
]

log = get_logger("mlr.stream")

DEFAULT_BATCH_SIZE: Final = 1000
"""单批事件数（keyset 分页；13.4M 事件规模下不整表入内存）。"""

DEFAULT_POLL_INTERVAL: Final = 1.0
"""`follow=True` 时的空批轮询间隔（秒）。"""

CURSOR_SEPARATOR: Final = "@"
"""游标内 `ts` 与 `event_id` 的分隔符（ISO-8601 时间戳不含 `@`，可安全 `rpartition`）。"""

_TS_WINDOW: Final = timedelta(seconds=5)
"""裸 `event_id` 游标解析窗口：事件的落库 `ts` ≥ `event_id` 内嵌毫秒（`append_event` 先取
`event_id` 后取 `now()`），偏移量为亚毫秒级；5s 窗口用于兜住时钟抖动。"""

_TS_WINDOW_BATCHES: Final = 5
"""裸 `event_id` 解析的最大批数（`5000` 条事件/窗口内找不到即判失败，避免无界扫描）。"""

_UUID_TEXT: Final = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)


@dataclass(frozen=True, slots=True)
class _Cursor:
    """流的定位游标（`(ts, event_id)` 行值比较；`ts=None` → 从头）。

    `pending_id` 仅用于裸 `event_id` 形态：`ts` 待从库中解析（:func:`_resolve_exact`）。
    """

    ts: datetime | None = None
    event_id: UUID | None = None
    pending_id: UUID | None = None


def cursor_token(event: Event) -> str:
    """事件 → 可持久化的精确续拉游标（``"<ts_iso>@<event_id>"``）。

    消费方把最后一条已处理事件的 token 存下来，下次作 `since` 传入即可从其后继续
    （半开区间，不重不漏）。
    """
    return _token(event.ts, event.event_id)


async def change_stream(
    since: str | None = None,
    *,
    storage: Storage | None = None,
    entity: str | None = None,
    batch_size: int = DEFAULT_BATCH_SIZE,
    follow: bool = False,
    poll_interval: float = DEFAULT_POLL_INTERVAL,
) -> AsyncIterator[Event]:
    """从 `since` 游标起按 `(ts, event_id)` 序产出事件（§3 M-LR / REQ-MLR-F02）。

    :param since: 游标字符串（形态见模块文档；`None` = 从头）。
    :param storage: 注入 `Storage`（缺省进程级单例）。
    :param entity: 可选实体过滤（``doc`` / ``node`` / ``ref`` / ``comment`` / ``schema`` / ``auth``）。
    :param batch_size: 单批拉取条数（≥1）。
    :param follow: ``False``（缺省）为**有界拉取**——拉空即结束，便于重放式消费；
      ``True`` 为追尾——无新事件时按 `poll_interval` 轮询，直到消费方中断（`break`/关闭生成器）。
    """
    if batch_size < 1:
        raise ValidationError(f"batch_size must be >= 1, got {batch_size}", entity="event")
    store = storage if storage is not None else Storage()
    cursor = _parse_cursor(since)
    if cursor.pending_id is not None:
        cursor = await _resolve_exact(store, cursor.pending_id)
    emitted = 0
    while True:
        # 追尾模式的空轮询不计指标：空闲期会按 poll_interval 每秒写一行日志
        timer = (
            nullcontext()
            if follow
            else log.timer("change_stream_batch", module="mlr.stream", limit=batch_size)
        )
        with timer:
            batch = await store.changes_since(
                since_ts=cursor.ts,
                since_event_id=cursor.event_id,
                entity=entity,
                limit=batch_size,
            )
        if not batch:
            if not follow:
                _log_drained(since, entity, emitted, cursor)
                return
            await asyncio.sleep(poll_interval)
            continue
        for event in batch:
            cursor = _Cursor(ts=event.ts, event_id=event.event_id)
            emitted += 1
            yield event
        if len(batch) < batch_size and not follow:
            _log_drained(since, entity, emitted, cursor)
            return


def _log_drained(since: str | None, entity: str | None, emitted: int, cursor: _Cursor) -> None:
    """有界拉取结束时的口径记录（`cursor` 即可供下次续拉的 token）。"""
    token = (
        None if cursor.ts is None or cursor.event_id is None else _token(cursor.ts, cursor.event_id)
    )
    log.info("change_stream drained", since=since, entity=entity, events=emitted, cursor=token)


def _token(ts: datetime, event_id: UUID) -> str:
    return f"{ts.isoformat()}{CURSOR_SEPARATOR}{event_id}"


def _parse_cursor(since: str | None) -> _Cursor:
    """`since` 文本 → :class:`_Cursor`（纯函数；非法游标 → :class:`ValidationError`）。"""
    if since is None or not since.strip():
        return _Cursor()
    text = since.strip()
    if CURSOR_SEPARATOR in text:
        ts_text, _, id_text = text.rpartition(CURSOR_SEPARATOR)
        return _Cursor(ts=_parse_ts(ts_text), event_id=_parse_event_id(id_text))
    if _UUID_TEXT.match(text):
        return _Cursor(pending_id=_parse_event_id(text))
    return _Cursor(ts=_parse_ts(text))


async def _resolve_exact(store: Storage, event_id: UUID) -> _Cursor:
    """裸 `event_id` 游标 → 精确 `(ts, event_id)`（有界扫描，见 `_TS_WINDOW*`）。"""
    start = datetime.fromtimestamp(uuid7_timestamp_ms(event_id) / 1000, tz=timezone.utc)
    horizon = start + _TS_WINDOW
    # `ts >= start`（游标事件自身的 ts 可能略晚于其内嵌毫秒，故下界回退 1ms）
    cursor = _Cursor(ts=start - timedelta(milliseconds=1))
    for _ in range(_TS_WINDOW_BATCHES):
        batch = await store.changes_since(
            since_ts=cursor.ts,
            since_event_id=cursor.event_id,
            limit=DEFAULT_BATCH_SIZE,
        )
        for event in batch:
            if event.event_id == event_id:
                return _Cursor(ts=event.ts, event_id=event.event_id)
            if event.ts > horizon:
                break
        if not batch or batch[-1].ts > horizon:
            break
        cursor = _Cursor(ts=batch[-1].ts, event_id=batch[-1].event_id)
    raise ValidationError(
        f"since cursor {event_id} not found in events within "
        f"{_TS_WINDOW.total_seconds()}s of its embedded timestamp; "
        f"use cursor_token(event) ('<ts_iso>@<event_id>') for exact resumption",
        entity="event",
        entity_id=event_id,
    )


def _parse_ts(text: str) -> datetime:
    """ISO-8601 → aware datetime（naive 按 UTC 处理，与 M02/M12 的 `ts` 口径一致）。"""
    try:
        ts = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValidationError(
            f"invalid since cursor timestamp {text!r}; expected ISO-8601 "
            f"(e.g. 2026-09-16T10:00:00+00:00)",
            entity="event",
        ) from exc
    return ts if ts.tzinfo is not None else ts.replace(tzinfo=timezone.utc)


def _parse_event_id(text: str) -> UUID:
    """事件 ID 文本 → UUIDv7（`event_id` 一律为 UUIDv7，非 v7 → 非法游标）。"""
    try:
        value = UUID(text)
    except ValueError as exc:
        raise ValidationError(
            f"invalid since cursor event id {text!r}; expected a UUID", entity="event"
        ) from exc
    if not is_uuid7(value):
        raise ValidationError(
            f"since cursor event id {text} is not a UUIDv7 (event ids are UUIDv7)",
            entity="event",
            entity_id=value,
        )
    return value
