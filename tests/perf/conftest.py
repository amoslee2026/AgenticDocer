"""`tests/perf/` 的 pytest 接线（ADR-010 §3.2 的运行口径）。

两件事，都是为了不动 `pyproject.toml` 的全局配置：

1. **收集**：`bench_*.py` 不符合 pytest 默认的 `python_files`（`test_*.py`/`*_test.py`），
   但 ADR-010 §3.2 规定的文件名就是 `bench_*.py`。本 conftest 用 `pytest_collect_file`
   钩子在**本目录内**把它们当测试模块收集，不改全局 ini。
2. **默认跳过**：ADR-010/§1.4 的基准是分钟级（`bench_scale` 更慢），故**默认跳过**，
   仅当 `-m` 表达式显式含 `perf` 时才运行：`uv run pytest tests/perf/ -m perf`。
   （标记 `@pytest.mark.perf` 由各基准模块用 `pytestmark` 声明；此处补「未选中即跳过」，
   使 `pytest tests/` 全量跑不会误触基准。）
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from pathlib import Path

import pytest

PERF_SELECTION = re.compile(r"\bperf\b")
SKIP_REASON = "性能基准默认跳过（分钟级）；显式运行：`uv run pytest tests/perf/ -m perf`"


def pytest_collect_file(file_path: Path, parent: pytest.Collector) -> pytest.Module | None:
    """把 `bench_*.py` 作为测试模块收集（仅限本目录）。"""
    if file_path.suffix == ".py" and file_path.name.startswith("bench_"):
        return pytest.Module.from_parent(parent, path=file_path)
    return None


def pytest_collection_modifyitems(
    config: pytest.Config, items: Iterable[pytest.Item]
) -> None:
    """未用 `-m perf` 显式选中时，把基准标记为 skip（而非静默不跑）。"""
    expression = config.getoption("-m") or ""
    if PERF_SELECTION.search(str(expression)):
        return
    skip = pytest.mark.skip(reason=SKIP_REASON)
    for item in items:
        item.add_marker(skip)
