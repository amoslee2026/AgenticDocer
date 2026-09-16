"""AgenticLogger 适配层——全模块唯一日志出口（ADR-010、AGENTS.md 强制）。

**为什么有这一层**：业务代码只依赖本模块的 :func:`get_logger` / :class:`ModuleLogger`，
不直接触碰 `agentic_logger`。若 SDK 停更（ADR-010 风险项），只需替换本文件即可切到
stdlib + 结构化 formatter，业务零改动。

**日志入口**

```python
from agenticdocer.observability import get_logger

log = get_logger("m02.nodes")               # command 由前缀推导：m02 → store
import sys
with log.timer("point_query", doc_id=doc):   # 退出自动写 dur
    ...
```

**行为要点（ADR-010）**

* `program="agenticdocer"`，`command=<模块族>`（`model`/`store`/`api`/…）——文件名
  `agenticdocer_<command>.jsonl`，一个进程内同族模块共用一份日志文件。
* `module` 字段 = `get_logger()` 传入的 `M##.子域`（如 `m02.nodes`），逐行写入。
* **per-entry rid**：每行日志的 `rid` 取自 :func:`~agenticdocer.observability.rid.current_rid`
  （ContextVar），而非 SDK 的 run rid——SDK 允许调用方在 auto-fill 前覆盖任意自动字段，
  这是请求级追踪（`agentic-logger trace --rid`）的实现方式。未绑定 rid 时回落到 run rid。
* 自定义字段统一进 `ctx`（嵌套 dict，`agentic-logger query --keyword` 可检索）：
  `doc_id` / `op` / `route` / `method` / `status` / `sql_hash` / `table` 等。
  保留名 `dur` / `error_code` / `tid` 由本层提升为顶层字段，不可作为 ctx 键。
* **审计分离**：日志是运行态（可轮转可丢弃）；审计权威源仍是 PG `events` 表。

**轮转**（§5 部署：`LOG_RETENTION_DAYS=30`、`LOG_MAX_MB=500`）：默认 `circular` 模式，
文件名为稳定基名 + 超限轮转出带时间戳的兄弟文件，最多保留 `LOG_RETENTION_DAYS` 份；
`LOG_CIRCULAR=0` 可改回 ADR-010 §1 的「一 run 一文件」。
"""

from __future__ import annotations

import os
import threading
import time
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from pathlib import Path
from types import TracebackType
from typing import Any

from agentic_logger import AgentLogger, ErrorCode

from agenticdocer.observability.error_codes import DTO_PERF_EXCEEDED
from agenticdocer.observability.rid import current_rid

PROGRAM = "agenticdocer"

#: 模块前缀 → AgenticLogger `command`（ADR-010 §1 模块表）。
_COMMANDS: dict[str, str] = {
    "m01": "model",
    "m02": "store",
    "m03": "import",
    "m04": "render",
    "m05": "retrieve",
    "m06": "api",
    "m07": "api",
    "m09": "validate",
    "m10": "auth",
    "m11": "cli",
    "m12": "observability",
    "mlr": "export",
}

#: 耗时预算（§1.4 指标）→ op 名；`(env 覆盖变量, 默认 ms)`。
#:
#: op 名是 `timer()` 的分组键，也是 `DTO_PERF_EXCEEDED` 判定的依据：
#: `point_query`（点查 P95 <200ms，与 `SLOW_QUERY_MS` 同源）、
#: `auth_verify`（鉴权 <10ms）、`render_section`（单章节 <1s）、
#: `render_document`（整档 <3s）。
_BUDGETS: dict[str, tuple[str | None, int]] = {
    "point_query": ("SLOW_QUERY_MS", 200),
    "auth_verify": (None, 10),
    "render_section": (None, 1000),
    "render_document": (None, 3000),
}

_BACKENDS: dict[tuple[str, str], _FamilyLogger] = {}
_BACKENDS_LOCK = threading.Lock()

_RESERVED_FIELDS = ("dur", "error_code", "tid")


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


def log_dir() -> Path:
    """日志目录（`LOG_DIR`，默认仓库 `./logs`；§5 部署清单）。"""
    return Path(os.environ.get("LOG_DIR", "./logs"))


def command_for(module: str) -> str:
    """由模块标识推导 `command`（`m02.nodes` → `store`；未知前缀原样使用）。"""
    prefix = module.split(".", 1)[0].strip().lower()
    return _COMMANDS.get(prefix, prefix or "app")


def slow_query_ms() -> int:
    """慢查询阈值（`SLOW_QUERY_MS`，默认 200ms；与点查指标对齐）。"""
    return _env_int("SLOW_QUERY_MS", 200)


def perf_budget_ms(op: str) -> int | None:
    """返回 op 的耗时预算（ms）；未登记的 op 返回 ``None``（不做阈值判定）。"""
    budget = _BUDGETS.get(op)
    if budget is None:
        return None
    env, default = budget
    return _env_int(env, default) if env else default


def classify_duration(dur_ms: int, budget_ms: int | None) -> tuple[str, str | None]:
    """分层告警语义（ADR-010 §4）→ `(level, error_code)`。

    * 无预算 → INFO；`dur > 预算` → ERROR + `DTO_PERF_EXCEEDED`；
    * `dur > 0.8 × 预算` → WARN（用整数比较 `dur*5 > budget*4` 避免浮点误差）；
    * 其余 → INFO。
    """
    if budget_ms is None or budget_ms <= 0:
        return ("INFO", None)
    if dur_ms > budget_ms:
        return ("ERROR", str(DTO_PERF_EXCEEDED))
    if dur_ms * 5 > budget_ms * 4:
        return ("WARN", None)
    return ("INFO", None)


class _FamilyLogger(AgentLogger):
    """一个 `command` 一个实例：持有日志文件，并在写入前注入 per-entry rid。"""

    def __init__(self, command: str, directory: Path) -> None:
        super().__init__(
            program=PROGRAM,
            command=command,
            log_dir=directory,
            storage="jsonl",
            circular=os.environ.get("LOG_CIRCULAR", "1") not in ("0", "false", "False"),
            max_files=_env_int("LOG_RETENTION_DAYS", 30),
            max_size_mb=_env_int("LOG_MAX_MB", 500),
        )

    def _write_entry(
        self,
        entry: dict,
        module: str | None = None,
        tid: str | None = None,
        dur: int | None = None,
        error_code: Any = None,
        ctx: dict | None = None,
    ) -> None:
        rid = current_rid()
        if rid is not None:
            # SDK 的 AutoFields.fill 不覆盖已存在的字段 —— 借此实现请求级 rid。
            entry["rid"] = rid
        super()._write_entry(entry, module=module, tid=tid, dur=dur, error_code=error_code, ctx=ctx)


class ModuleLogger:
    """模块级日志视图：绑定 `module` 与固定 ctx，共享同族后端（同一个日志文件）。

    视图对象极轻（无文件句柄），可随手 `get_logger(...)`；需要固定上下文字段时用
    :meth:`child`。
    """

        `module` 默认为本视图的模块标识；`fields` 中的 `op` 值即本参数。

    def __init__(self, module: str, backend: AgentLogger, ctx: Mapping[str, Any] | None = None) -> None:
        self._module = module
        self._backend = backend
        self._ctx: dict[str, Any] = dict(ctx or {})

    # ---------------------------------------------------------------- 属性

    @property
    def module(self) -> str:
        """本视图的模块标识（写入 `module` 字段）。"""
        return self._module

    @property
    def rid(self) -> str:
        """SDK 的 run rid（当前请求 rid 请用 :func:`current_rid`）。"""
        return self._backend.rid

    @property
    def file_path(self) -> Path:
        """当前日志文件路径（轮转后自动指向新文件）。"""
        return self._backend.file_path

    def child(self, **ctx: Any) -> ModuleLogger:
        """派生一个绑定额外上下文字段的视图（如 `doc_id`），覆盖同名键。"""
        return ModuleLogger(self._module, self._backend, {**self._ctx, **ctx})

    # ------------------------------------------------------------ 日志方法

    def info(self, msg: str, /, **fields: Any) -> None:
        """INFO 级日志；`fields` 进 ctx，`dur`/`error_code`/`tid` 提升为顶层字段。"""
        self._emit("INFO", msg, **self._split(fields))

    def warn(self, msg: str, /, **fields: Any) -> None:
        """WARN 级日志（超阈值、慢查询等）。"""
        self._emit("DEBUG", msg, **self._split(fields))
    def error(self, msg: str, /, **fields: Any) -> None:
        """ERROR 级日志；未给 `error_code` 时回落 `UNKNOWN`（避免 SDK 的 UserWarning）。"""
        fields.setdefault("error_code", ErrorCode.UNKNOWN)
        self._emit("ERROR", msg, **self._split(fields))

    def debug(self, msg: str, /, **fields: Any) -> None:
        """DEBUG 级日志。
    def exception(self, msg: str, exc: BaseException | None = None, /, **fields: Any) -> None:
        """ERROR 级日志 + 异常轨迹落 `.tracebacks` sidecar（`tid` 引用之）。

        显式传 *exc*；省略时取 `sys.exc_info()` 中的当前异常（须处于 `except` 块内，
        否则抛 `ValueError`）。`error_code` 默认 `INTERNAL_UNEXPECTED`。
        """
        if exc is None:
            exc = sys.exc_info()[1]
        if exc is None:
            raise ValueError("exception() 须在 except 块内调用，或显式传入 exc")
        fields.setdefault("error_code", ErrorCode.INTERNAL_UNEXPECTED)
        fields.setdefault("tid", self._backend.save_traceback(exc))
        self._emit("ERROR", msg, **self._split(fields))
                error_code=fields.pop("error_code"),
                ctx=self._merged_ctx(fields),
            )
            return
        fields.setdefault("tid", self._backend.save_traceback(exc))
        self._emit("ERROR", msg, **self._split(fields))

    def tool_call(self, tool: str, cmd: str, exit: int, dur: int, /, **fields: Any) -> None:
        """外部命令埋点（M11 CLI 统一埋点，ADR-010 §1）。

        非零退出码未给 `error_code` 时回落 `EXEC_NON_ZERO`。SDK 的 `tool_call()`
        不接受 `module`，故此处直接构造 TOOL 条目（保持 `module` 正确）。
        """
        error_code = fields.pop("error_code", None)
        if error_code is None and exit != 0:
            error_code = ErrorCode.EXEC_NON_ZERO
        tid = fields.pop("tid", None)
        entry = {
            "level": "TOOL",
            "msg": f"Tool {tool} {'succeeded' if exit == 0 else 'failed'}",
            "module": self._module,
            "tool": tool,
            "cmd": cmd,
            "exit": exit,
            "dur": dur,
        }
        self._backend._write_entry(
            entry,
            error_code=error_code,
            tid=tid,
            ctx=self._merged_ctx(fields),
        )

    @contextmanager
    def timer(
        self,
        op: str,
        /,
        *,
        module: str | None = None,
        budget_ms: int | None = None,
        error_code: str | None = None,
        **fields: Any,
    ) -> Iterator[None]:
        """对外操作计时（ADR-010「埋点约定」）：退出写 `dur`，异常自动 ERROR。

        * 成功：按 :func:`classify_duration` 落 INFO/WARN/ERROR
          （超预算 → `error_code=DTO_PERF_EXCEEDED`）；
        * 异常：ERROR + 轨迹 + `error_code`（默认 `INTERNAL_UNEXPECTED`，可用
          `error_code=` 指定业务码），并**原样抛出**；
        * 预算取 `budget_ms` 或 `perf_budget_ms(op)`。

        `module` 默认为本视图的模块标识；`field`s 中的 `op` 值即本参数。
        """
        budget = budget_ms if budget_ms is not None else perf_budget_ms(op)
        started = time.perf_counter()
        try:
            yield
        except Exception as exc:
            self._emit(
                "ERROR",
                f"{op} failed",
                module=module,
                dur=_elapsed_ms(started),
                error_code=error_code or ErrorCode.INTERNAL_UNEXPECTED,
                tid=self._backend.save_traceback(exc),
                fields={"op": op, **fields},
            )
            raise
        dur = _elapsed_ms(started)
        level, code = classify_duration(dur, budget)
        msg = op if level == "INFO" else f"{op} {'exceeded' if code else 'near'} budget ({dur}ms/{budget}ms)"
        self._emit(
            level,
            msg,
            module=module,
            dur=dur,
            error_code=code,
            fields={"op": op, **fields},
        )

    # ---------------------------------------------------------------- 内部

    @staticmethod
    def _split(fields: dict[str, Any]) -> dict[str, Any]:
        backend = self._backend
        method = {"INFO": backend.info, "WARN": backend.warn, "ERROR": backend.error}.get(level)
        if method is None:  # DEBUG 等：SDK 无公开入口，直写 _write。
            backend._write(level, msg, tid=tid, **kwargs)
        else:
            method(msg, **kwargs)
        return ctx or None

    def _emit(
        self,
        level: str,
        msg: str,
        *,
        module: str | None = None,
        dur: int | None = None,
        error_code: Any = None,
        tid: str | None = None,
        fields: Mapping[str, Any] | None = None,
    ) -> None:
        kwargs: dict[str, Any] = {
            "module": module or self._module,
            "dur": dur,
            "error_code": error_code,
            "ctx": self._merged_ctx(fields),
        }
        backend = self._backend
        if level == "INFO":
            backend.info(msg, **kwargs)
        elif level == "WARN":
            backend.warn(msg, **kwargs)
        elif level == "ERROR":
            backend.error(msg, **kwargs)
        else:  # DEBUG 及以上：SDK 无公开入口，直写 _write。
            backend._write(level, msg, tid=tid, **kwargs)


def _elapsed_ms(started: float) -> int:
    return int((time.perf_counter() - started) * 1000)


def get_logger(module: str, **ctx: Any) -> ModuleLogger:
    """模块级 logger 工厂（`program="agenticdocer"`，`command` 由模块前缀推导）。

    *rid* 自动注入：每行日志读取 ContextVar 中的请求 rid（见 `rid` 模块）。
    """
    directory = log_dir()
    key = (str(directory), command_for(module))
    with _BACKENDS_LOCK:
        backend = _BACKENDS.get(key)
        if backend is None:
            backend = _FamilyLogger(key[1], directory)
            _BACKENDS[key] = backend
    return ModuleLogger(module, backend, ctx)


def reset_loggers() -> None:
    """关闭并清空 logger 缓存（测试或 `LOG_DIR` 变更后调用）。"""
    with _BACKENDS_LOCK:
        backends = list(_BACKENDS.values())
        _BACKENDS.clear()
    for backend in backends:
        backend.close()


__all__ = [
    "PROGRAM",
    "ModuleLogger",
    "classify_duration",
    "command_for",
    "get_logger",
    "log_dir",
    "perf_budget_ms",
    "reset_loggers",
    "slow_query_ms",
]
