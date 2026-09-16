"""M01 UUIDv7 测试：时间有序（字节序单调）、唯一位布局、时钟回拨与线程安全。"""

from __future__ import annotations

import threading
import time
import uuid as uuid_mod

import agenticdocer.model.uuid7 as uuid7_mod
from agenticdocer.model.uuid7 import is_uuid7, new_uuid7, uuid7_timestamp_ms


def test_consecutive_ids_are_byte_order_monotonic():
    ids = [new_uuid7() for _ in range(2000)]
    assert all(left.bytes < right.bytes for left, right in zip(ids, ids[1:]))


def test_ids_are_unique():
    ids = {new_uuid7() for _ in range(5000)}
    assert len(ids) == 5000


def test_version_and_variant_bits():
    for _ in range(64):
        value = new_uuid7()
        assert value.version == 7
        assert value.variant == uuid_mod.RFC_4122
        assert is_uuid7(value)


def test_embedded_timestamp_tracks_now():
    before = time.time_ns() // 1_000_000
    stamp = uuid7_timestamp_ms(new_uuid7())
    after = time.time_ns() // 1_000_000
    assert before - 1000 <= stamp <= after + 1000


def test_null_uuid_is_not_uuid7():
    assert not is_uuid7(uuid_mod.UUID(int=0))


def test_clock_regression_keeps_monotonic(monkeypatch):
    readings = iter([10_000, 10_000, 9_000, 9_000, 9_000])
    monkeypatch.setattr(uuid7_mod.time, "time_ns", lambda: next(readings) * 1_000_000)
    monkeypatch.setattr(uuid7_mod, "_last_ms", -1)
    monkeypatch.setattr(uuid7_mod, "_seq", 0)

    ids = [new_uuid7() for _ in range(5)]

    assert all(left.bytes < right.bytes for left, right in zip(ids, ids[1:]))
    # 回拨后沿用最后时间戳（10_000），不产生小于前值的 UUID
    assert {uuid7_timestamp_ms(value) for value in ids} == {10_000}


def test_sequence_exhaustion_borrows_next_millisecond(monkeypatch):
    monkeypatch.setattr(uuid7_mod.time, "time_ns", lambda: 5_000 * 1_000_000)
    monkeypatch.setattr(uuid7_mod, "_last_ms", 5_000)
    monkeypatch.setattr(uuid7_mod, "_seq", uuid7_mod._SEQ_MAX)

    first = new_uuid7()
    second = new_uuid7()

    assert uuid7_timestamp_ms(first) == 5_001
    assert uuid7_timestamp_ms(second) == 5_001
    assert first.bytes < second.bytes


def test_thread_safety_produces_unique_ids():
    collected: list[uuid_mod.UUID] = []
    lock = threading.Lock()

    def worker() -> None:
        local = [new_uuid7() for _ in range(300)]
        with lock:
            collected.extend(local)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(collected) == 2400
    assert len(set(collected)) == 2400


def test_new_uuid7_returns_uuid_instance():
    assert isinstance(new_uuid7(), uuid_mod.UUID)
