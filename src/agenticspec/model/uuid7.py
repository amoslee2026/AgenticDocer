"""UUIDv7 生成器（RFC 9562 §5.7）：时间有序，仅用标准库。

位布局（128 位，大端）：

    | 48 bit unix_ts_ms | 4 bit ver=7 | 12 bit rand_a | 2 bit var=10 | 62 bit rand_b |

实现选择：``rand_a`` + ``rand_b`` 合并为一个 74 位**单调计数器**。新毫秒到来时以
``secrets`` 随机播种该计数器，同一毫秒内逐次自增；时钟回拨视作「同毫秒」继续自增，
计数耗尽时借位到下一毫秒。由此保证：

- 连续生成的两个 UUID 满足 ``a.bytes < b.bytes``（字节序单调递增，§6「ID：应用侧
  UUIDv7（时间有序）」）；
- 每个 UUID 唯一（同毫秒内计数不重复，跨毫秒时间戳不同）；
- 计数器初值随机，ID 不可由前一个 UUID 预测。
"""

from __future__ import annotations

import secrets
import threading
import time
from uuid import UUID

__all__ = ["new_uuid7", "is_uuid7", "uuid7_timestamp_ms"]

_NS_PER_MS = 1_000_000
_TS_BITS = 48
_TS_MASK = (1 << _TS_BITS) - 1
_VERSION = 0x7
_VARIANT = 0b10  # RFC 4122/9562 变体（10x）

_RAND_BITS = 62
_SEQ_BITS = 12 + _RAND_BITS  # rand_a(12) + rand_b(62)
_SEQ_MAX = (1 << _SEQ_BITS) - 1

_lock = threading.Lock()
_last_ms = -1
_seq = 0


def _pack(ts_ms: int, seq: int) -> UUID:
    rand_a = (seq >> _RAND_BITS) & 0xFFF
    rand_b = seq & ((1 << _RAND_BITS) - 1)
    value = (
        ((ts_ms & _TS_MASK) << (_TS_BITS + 32))
        | (_VERSION << 76)
        | (rand_a << 64)
        | (_VARIANT << 62)
        | rand_b
    )
    return UUID(int=value)


def new_uuid7() -> UUID:
    """生成一个 UUIDv7（时间有序、全局唯一、线程安全）。"""
    global _last_ms, _seq
    with _lock:
        now_ms = time.time_ns() // _NS_PER_MS
        if now_ms > _last_ms:
            _last_ms = now_ms
            _seq = secrets.randbits(_SEQ_BITS)
        elif _seq >= _SEQ_MAX:
            # 同毫秒内 74 位计数耗尽（或长时间时钟回拨）：借位到下一毫秒
            _last_ms += 1
            _seq = 0
        else:
            _seq += 1
        return _pack(_last_ms, _seq)


def is_uuid7(value: UUID) -> bool:
    """是否为 UUIDv7（版本位 = 7 且变体位 = 10x）。"""
    return (value.int >> 76) & 0xF == _VERSION and (value.int >> 62) & 0b11 == _VARIANT


def uuid7_timestamp_ms(value: UUID) -> int:
    """取 UUIDv7 内嵌的 unix 毫秒时间戳（用于排序/分区断言）。"""
    return value.int >> (_TS_BITS + 32)
