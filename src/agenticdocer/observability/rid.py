"""请求级追踪 ID（rid）——ADR-010 §2「rid 贯穿」。

一次 HTTP 请求或 CLI 调用生成一个 rid，贯穿 M10 鉴权 → M06/M07 路由 → M02 存储
→ M04 渲染；AgenticLogger 的每行日志都带同一个 rid，`agentic-logger trace --rid`
即可拉出全链路。

**8 hex 的构成**（ADR-010：uuid7 短形态、时间有序）

```
  rid = "a1b2c3d4"
         ││ └─────┴─ 低 24 位：进程内随机起点 + 单调递增计数（唯一性来源）
         └┴──────── 高 8 位：当前毫秒的低 8 位（时间局部性，256ms 回绕）
```

* **为什么不是 `uuid7().hex[:8]`**：UUIDv7 的前 8 个 hex 位是时间戳高位，同一
  ~65 秒窗口内完全不变——批量请求会拿到大量重复 rid，丧失追踪价值。因此取
  「时间前缀 + 单调计数」而非字面位截断（见交付说明的偏差声明）。
* **进程内唯一**：计数器严格递增（mod 2^24）；两条 rid 相同当且仅当毫秒低字节
  相同且相距恰好 2^24 次调用——实际不可达。
* **跨进程**：计数器起点由 `secrets.randbits(24)` 随机化，两进程撞同一 rid 的
  概率上界约 2^-24（且还需毫秒低字节对齐）。

传播：`contextvars.ContextVar`。新建 asyncio 任务会拷贝当前上下文（子任务可见父
rid，且并发任务互不串号）；**线程不继承**——HTTP 中间件在请求任务内 `set_rid()`，
CLI 在入口处 `set_rid()`。
"""

from __future__ import annotations

import contextvars
import secrets
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager
from typing import cast

_RID_NAME = "agenticdocer_rid"

#: 计数器位宽：24 位 → 与 8 位毫秒前缀拼成 32 位（8 hex）。
_SEQ_BITS = 24
_SEQ_MASK = (1 << _SEQ_BITS) - 1
_TS_MASK = 0xFF

#: 进程内随机起点（跨进程去重的唯一随机源）。
_seq: int = secrets.randbits(_SEQ_BITS)
_seq_lock = threading.Lock()

_rid_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(_RID_NAME, default=None)


def new_rid() -> str:
    """生成一个 8 hex 的请求/调用追踪 id（进程内唯一，时间前缀有序）。"""
    global _seq
    with _seq_lock:
        _seq = (_seq + 1) & _SEQ_MASK
        seq = _seq
    ts_ms = int(time.time() * 1000) & _TS_MASK
    return f"{ts_ms:02x}{seq:06x}"


def current_rid() -> str | None:
    """返回当前上下文的 rid；未设置时返回 ``None``。"""
    return _rid_var.get()


def set_rid(rid: str | None = None) -> contextvars.Token[str | None]:
    """把 *rid* 写入当前上下文（``None`` 则新生成一个），返回可用于回退的 token。"""
    return _rid_var.set(rid if rid is not None else new_rid())


def reset_rid(token: contextvars.Token[str | None]) -> None:
    """回退 :func:`set_rid` 返回的 token。"""
    _rid_var.reset(token)


@contextmanager
def rid_scope(rid: str | None = None) -> Iterator[str]:
    """作用域内绑定 rid（未给出则新生成），退出时恢复原值。"""
    token = set_rid(rid)
    try:
        yield cast("str", _rid_var.get())  # set_rid 保证非 None
    finally:
        reset_rid(token)
