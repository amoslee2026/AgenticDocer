"""`tests/perf/` 共享基准骨架（ADR-010 §3.2；目标值出自 `architecture_specification.md` §1.4）。

五个基准（`bench_{point_query,render,auth,scale,import}.py`）共用本模块：

* **计时与百分位口径**：`timing_stats()` 直接复用在线指标同一实现
  （`agenticdocer.observability.metrics.percentile`，nearest-rank）——P5「口径唯一」；
* **结果落盘**：<repo>/build/perf.json（每基准保留最近 `HISTORY_LIMIT` 次运行 +
  `latest`）+ <repo>/build/perf/<bench>_<ts>.json 归档（ADR-010 §3.2「结果归档」）；
* **历史对比**：`--compare` 打印与上一次运行的同名指标差值（趋势）；
* **人类可读输出**：指标表 + 「达标 / 不达标」判定 + 降级路径独立区块；
* **DSN 解析**：`--dsn` → `PERF_DATABASE_URL` → 内置隔离库 `agenticdocer_perf_test`。
  刻意**不**回落环境里的 `DATABASE_URL`：本套件会灌入上万文档（ADR-009 规模基准），
  误跑在共享库/主库上的代价不可接受（模块本身的默认库即隔离库）。

降级路径（ADR-009 V16「不带 `doc_id` 的点查」）在**指标名、表格、JSON、输出区块**中
一律带 `degraded=True` 标记，不与正常路径混列（用户要求）。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import platform
import random
import re
import shutil
import statistics
import sys
import tempfile
import time
from collections.abc import Awaitable, Callable, Iterable, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "build"
PERF_JSON = BUILD / "perf.json"
PERF_ARCHIVE = BUILD / "perf"
CORPUS_DIR = ROOT / "spec" / "standards"

SCHEMA_VERSION = 1
HISTORY_LIMIT = 20

DEFAULT_DSN = (
    "postgresql+asyncpg://agenticdocer:agenticdocer_dev@127.0.0.1:5432/agenticdocer_perf_test"
)
"""默认隔离库（跑完可 DROP；M02/M09/M11 同款做法）。"""

#: §1.4 目标值（**单一出处**：architecture_specification.md §1.4 表）。
TARGET_POINT_P95_MS = 200.0
TARGET_SECTION_MS = 1_000.0
TARGET_DOCUMENT_MS = 3_000.0
TARGET_AUTH_P95_MS = 10.0
TARGET_COVERAGE = 0.95
TARGET_DOCS = 10_000
TARGET_NODES = 13_400_000
TARGET_NODES_PER_DOC = 1_343
"""§1.4/ADR-009：10,000 文档 ≈13.4M 节点 ⇒ ≈1,343 原子/文档（7 份语料实测校准）。"""

TARGET_PARTITION_COUNT = 64
"""ADR-009 §1：`nodes` HASH(doc_id) 64 分区。"""

TARGET_PARTITION_CV = 0.10
"""分区均衡判据（ADR-009 §1 断言「分区均衡」）：各分区行数的变异系数 ≤10%。"""

SECONDS = 1_000_000  # µs per second


# ───────────────────────────────────────────────────────────── 指标与结果模型


def _verdict(value: Any, target: float | None, comparison: str) -> str:
    if target is None or isinstance(value, bool) or not isinstance(value, (int, float)):
        return "记录"
    if comparison == "<=":
        ok = value <= target
    elif comparison == ">=":
        ok = value >= target
    elif comparison == "==":
        ok = value == target
    else:  # pragma: no cover - 编程错误
        raise ValueError(f"unknown comparison {comparison!r}")
    return "达标" if ok else "不达标"


@dataclass
class Metric:
    """单项指标：实测值 + §1.4 目标值 + 判定。"""

    name: str
    value: Any
    unit: str = ""
    target: float | None = None
    comparison: str = "<="
    degraded: bool = False
    note: str = ""
    verdict: str = field(init=False, default="记录")

    def __post_init__(self) -> None:
        self.verdict = _verdict(self.value, self.target, self.comparison)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "target": self.target,
            "comparison": self.comparison,
            "verdict": self.verdict,
            "degraded": self.degraded,
            "note": self.note,
        }


@dataclass
class Bench:
    """一次基准运行的完整结果。"""

    name: str
    title: str
    metrics: list[Metric] = field(default_factory=list)
    counters: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
    label: str = ""
    started_at: str = ""
    finished_at: str = ""
    duration_s: float = 0.0
    dsn: str = ""
    environment: dict[str, Any] = field(default_factory=dict)

    def add(self, *metrics: Metric) -> Bench:
        self.metrics.extend(metrics)
        return self

    def note(self, text: str) -> Bench:
        self.notes.append(text)
        return self

    def get(self, name: str) -> Metric | None:
        for metric in self.metrics:
            if metric.name == name:
                return metric
        return None

    def failed(self) -> list[Metric]:
        return [m for m in self.metrics if m.verdict == "不达标"]

    def degraded(self) -> list[Metric]:
        return [m for m in self.metrics if m.degraded]

    def to_dict(self) -> dict[str, Any]:
        return {
            "bench": self.name,
            "title": self.title,
            "label": self.label,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_s": self.duration_s,
            "dsn": self.dsn,
            "environment": self.environment,
            "counters": self.counters,
            "metrics": [m.to_dict() for m in self.metrics],
            "notes": self.notes,
        }


def metric(
    name: str,
    value: Any,
    *,
    unit: str = "",
    target: float | None = None,
    comparison: str = "<=",
    degraded: bool = False,
    note: str = "",
) -> Metric:
    return Metric(
        name=name,
        value=value,
        unit=unit,
        target=target,
        comparison=comparison,
        degraded=degraded,
        note=note,
    )


# ──────────────────────────────────────────────────────────────── 计时与统计


class Stopwatch:
    """微秒级计时（`perf_counter`）；`elapsed_us()` 为整数微秒。"""

    __slots__ = ("_start",)

    def __init__(self) -> None:
        self._start = time.perf_counter()

    def restart(self) -> None:
        self._start = time.perf_counter()

    def elapsed_us(self) -> int:
        return int((time.perf_counter() - self._start) * SECONDS)

    def elapsed_ms(self) -> float:
        return (time.perf_counter() - self._start) * 1000.0


def timing_stats(samples_us: Sequence[int]) -> dict[str, float]:
    """样本（µs）→ P50/P95/P99/mean/min/max（ms）。

    百分位与在线指标共用 `observability.metrics.percentile`（nearest-rank，口径唯一）。
    """
    from agenticdocer.observability.metrics import percentile

    if not samples_us:
        return {"n": 0}
    return {
        "n": len(samples_us),
        "p50_ms": round(percentile(list(samples_us), 0.50) / 1000, 3),
        "p95_ms": round(percentile(list(samples_us), 0.95) / 1000, 3),
        "p99_ms": round(percentile(list(samples_us), 0.99) / 1000, 3),
        "mean_ms": round(statistics.fmean(samples_us) / 1000, 3),
        "min_ms": round(min(samples_us) / 1000, 3),
        "max_ms": round(max(samples_us) / 1000, 3),
    }


async def timed(coro: Awaitable[Any]) -> tuple[Any, int]:
    """`await` 一个协程 → `(结果, 耗时 µs)`。"""
    start = time.perf_counter()
    result = await coro
    return result, int((time.perf_counter() - start) * SECONDS)


# ──────────────────────────────────────────────────────────────── 文本与格式化


def human_bytes(size: float) -> str:
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if abs(size) < 1024 or unit == "TiB":
            return f"{size:.1f}{unit}" if unit != "B" else f"{int(size)}B"
        size /= 1024
    return f"{size:.1f}TiB"  # pragma: no cover


def render_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    """定宽纯文本表（人类可读输出；无第三方依赖）。"""
    cells = [[str(cell) for cell in row] for row in rows]
    widths = [len(str(h)) for h in headers]
    for row in cells:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))
    line = "  ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers)).rstrip()
    rule = "  ".join("-" * w for w in widths)
    body = ["  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip() for row in cells]
    return "\n".join([line, rule, *body])


def masked_dsn(dsn: str) -> str:
    try:
        from sqlalchemy.engine import make_url
    except Exception:  # pragma: no cover - sqlalchemy 必在
        return re.sub(r"://[^@]*@", "://***@", dsn)
    try:
        return make_url(dsn).render_as_string(hide_password=True)
    except Exception:
        return re.sub(r"://[^@]*@", "://***@", dsn)


def now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def stamp_compact(iso: str) -> str:
    return re.sub(r"[-:+]", "", iso)[:15]


# ────────────────────────────────────────────────────────────── 结果落盘与对比


def load_store(path: Path | str = PERF_JSON) -> dict[str, Any]:
    """读 `build/perf.json`；缺失返回空骨架，损坏则**先备份**再重建（不静默丢弃）。"""
    target = Path(path)
    if not target.is_file():
        return {"schema": SCHEMA_VERSION, "benchmarks": {}}
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        backup = target.with_suffix(f".corrupt-{stamp_compact(now_iso())}.json")
        shutil.copyfile(target, backup)
        print(f"!! {target} 不是合法 JSON，已备份到 {backup}（本次重建）", file=sys.stderr)
        return {"schema": SCHEMA_VERSION, "benchmarks": {}}
    if not isinstance(data, dict):
        return {"schema": SCHEMA_VERSION, "benchmarks": {}}
    data.setdefault("schema", SCHEMA_VERSION)
    data.setdefault("benchmarks", {})
    return data


def previous_run(name: str, path: Path | str = PERF_JSON) -> dict[str, Any] | None:
    """上一次（最近一次已保存的）该基准运行记录。"""
    entry = load_store(path).get("benchmarks", {}).get(name)
    runs = (entry or {}).get("runs") or []
    return runs[-1] if runs else None


def save(bench: Bench, path: Path | str = PERF_JSON) -> Path:
    """写 `perf.json`（追加历史 + 更新 latest）并归档单次运行 JSON；返回主文件路径。"""
    target = Path(path)
    run = bench.to_dict()
    data = load_store(target)
    entry = data.setdefault("benchmarks", {}).setdefault(bench.name, {})
    entry["title"] = bench.title
    runs = entry.setdefault("runs", [])
    runs.append(run)
    del runs[:-HISTORY_LIMIT]
    entry["latest"] = run
    data["schema"] = SCHEMA_VERSION
    data["updated_at"] = now_iso()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    PERF_ARCHIVE.mkdir(parents=True, exist_ok=True)
    suffix = f"_{bench.label}" if bench.label else ""
    archive = PERF_ARCHIVE / f"{bench.name}_{stamp_compact(bench.started_at)}{suffix}.json"
    archive.write_text(json.dumps(run, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target


def compare_rows(current: Bench, previous: dict[str, Any] | None) -> list[list[str]]:
    """同名指标的上次值/本次值/变化（趋势对比）。"""
    if not previous:
        return []
    before = {m["name"]: m for m in previous.get("metrics", [])}
    rows: list[list[str]] = []
    for item in current.metrics:
        old = before.get(item.name)
        if old is None:
            continue
        old_value, new_value = old.get("value"), item.value
        if not isinstance(old_value, (int, float)) or not isinstance(new_value, (int, float)):
            continue
        if old_value:
            delta = f"{(new_value - old_value) / abs(old_value) * 100:+.1f}%"
        else:
            delta = "n/a"
        rows.append([item.name, f"{old_value:g}", f"{new_value:g}", delta])
    return rows


# ─────────────────────────────────────────────────────────────────────── 输出
def goal_text(item: Metric) -> str:
    """指标目标的可读后缀（无目标值 → 记「记录项」，避免格式化 None）。"""
    if item.target is None:
        return "（记录项）"
    return f"（目标 {item.comparison}{item.target:g} → {item.verdict}）"


def _compact(value: Any, *, text_limit: int = 160, list_limit: int = 8) -> Any:
    """控制台用计数器压缩（长字符串/长列表截断；JSON 落盘仍保留全量）。"""
    if isinstance(value, dict):
        return {key: _compact(item, text_limit=text_limit, list_limit=list_limit)
                for key, item in value.items()}
    if isinstance(value, list):
        head = [_compact(item, text_limit=text_limit, list_limit=list_limit) for item in value[:list_limit]]
        if len(value) > list_limit:
            head.append(f"…（共 {len(value)} 项）")
        return head
    if isinstance(value, str) and len(value) > text_limit:
        return value[:text_limit] + "…"
    return value




def print_report(bench: Bench, previous: dict[str, Any] | None = None) -> None:
    print(f"\n═══ {bench.name} — {bench.title}")
    print(f"label={bench.label or '-'}  dsn={bench.dsn}  started={bench.started_at}  "
          f"duration={bench.duration_s:.1f}s")
    if bench.environment:
        print("environment: " + json.dumps(bench.environment, ensure_ascii=False))
    if bench.counters:
        print("counters:")
        print("\n".join("  " + line for line in
                        json.dumps(_compact(bench.counters), ensure_ascii=False, indent=2).splitlines()))

    rows = []
    for item in bench.metrics:
        target = "" if item.target is None else f"{item.comparison}{item.target:g}"
        rows.append([
            item.name,
            f"{item.value:g}" if isinstance(item.value, (int, float)) and not isinstance(item.value, bool)
            else str(item.value),
            item.unit,
            target,
            item.verdict,
            "降级路径(已知)" if item.degraded else "",
        ])
    if rows:
        print()
        print(render_table(["指标", "实测", "单位", "目标", "判定", "路径"], rows))
    degraded = bench.degraded()
    if degraded:
        print("\n!! 降级路径（`degraded` 标记项，如 ADR-009 V16 的「不带 doc_id」点查）"
              "——结果**不得**与正常路径混为一谈：")
        for item in degraded:
            print(f"   ! {item.name} = {item.value} {item.unit}{goal_text(item)}"
                  f"{('— ' + item.note) if item.note else ''}")

    failed = bench.failed()
    if failed:
        print("\n!! 不达标指标：")
        for item in failed:
            suffix = f"（{item.note}）" if item.note else ""
            print(f"   ✗ {item.name} = {item.value} {item.unit}{goal_text(item)}{suffix}")
    else:
        scored = [m for m in bench.metrics if m.verdict != "记录"]
        if scored:
            print(f"\n✔ 有目标值的 {len(scored)} 项指标全部达标")

    if previous:
        delta_rows = compare_rows(bench, previous)
        header = (f"上次 {previous.get('started_at', '?')}"
                  f"{'，label=' + previous['label'] if previous.get('label') else ''}"
                  f"，dsn={previous.get('dsn', '?')}")
        if delta_rows:
            print(f"\n↔ 与上次运行对比（{header}）：")
            print(render_table(["指标", "上次", "本次", "变化"], delta_rows))
        else:
            print(f"\n↔ 上次运行（{header}）无同名可对比指标")
        if previous.get("dsn") and previous["dsn"] != bench.dsn:
            print("   ⚠ 两次运行的库不同（见上方 dsn）——趋势对比仅供参考，不构成回归判据")
        else:
            print(f"\n↔ 上次运行（{previous.get('started_at', '?')}）无同名可对比指标")

    if bench.notes:
        print("\n说明：")
        for text in bench.notes:
            print(f"  · {text}")


# ─────────────────────────────────────────────────────────────────── 进程脚手架


def add_common_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--dsn", default=None,
                        help=f"基准库 DSN（默认 PERF_DATABASE_URL 或隔离库 {masked_dsn(DEFAULT_DSN)}）")
    parser.add_argument("--out", default=str(PERF_JSON), help="结果文件（默认 build/perf.json）")
    parser.add_argument("--label", default="", help="本次运行标签（写入结果与归档文件名）")
    parser.add_argument("--compare", action="store_true", help="与上一次运行做趋势对比")
    parser.add_argument("--json", action="store_true", help="额外打印本次运行的 JSON")
    parser.add_argument("--strict", action="store_true", help="存在「不达标」指标时以非零码退出")
    return parser


def configure_dsn(dsn: str | None = None) -> str:
    """解析并注入基准库 DSN（赋值覆盖 `.env`，故显式 DSN 始终生效）。"""
    resolved = dsn or os.environ.get("PERF_DATABASE_URL") or DEFAULT_DSN
    os.environ["DATABASE_URL"] = resolved
    os.environ.setdefault("MIGRATION_DATABASE_URL", resolved)
    return resolved


def current_dsn() -> str:
    return os.environ.get("DATABASE_URL", DEFAULT_DSN)


def environment() -> dict[str, Any]:
    return {
        "python": platform.python_version(),
        "platform": f"{platform.system()} {platform.release()}",
        "cpu_count": os.cpu_count(),
        "machine": platform.machine(),
    }


def execute(parser: argparse.ArgumentParser, main_fn: Callable[[argparse.Namespace], Awaitable[Bench]]) -> int:
    """CLI 入口：解析参数 → 跑基准 → 落盘 → 打印（+ 可选对比 / JSON）。"""
    args = parser.parse_args()
    configure_dsn(args.dsn)
    started_at = now_iso()
    wall = time.time()
    bench = asyncio.run(main_fn(args))
    bench.label = args.label or bench.label
    bench.started_at = started_at
    bench.finished_at = now_iso()
    bench.duration_s = round(time.time() - wall, 3)
    bench.dsn = masked_dsn(current_dsn())
    bench.environment.update(environment())
    previous = previous_run(bench.name, args.out)
    path = save(bench, args.out)
    print_report(bench, previous if args.compare else None)
    print(f"\n结果已写入 {path}（归档目录 {PERF_ARCHIVE}）")
    if args.json:
        print(json.dumps(bench.to_dict(), ensure_ascii=False, indent=2))
    failed = bench.failed()
    return 1 if (failed and args.strict) else 0


def default_args(parser: argparse.ArgumentParser) -> argparse.Namespace:
    """pytest 路径用的默认参数（与 `--help` 展示的一致）。"""
    return parser.parse_args([])


def reachable(dsn: str | None = None, *, timeout: float = 5.0) -> bool:
    """基准库是否可连（pytest 路径据此 skip）。"""
    return asyncio.run(_reachable(configure_dsn(dsn), timeout))


async def _reachable(dsn: str, timeout: float) -> bool:
    from sqlalchemy import text

    from agenticdocer.store import Database

    db = Database(dsn)
    try:
        async with asyncio.timeout(timeout):
            async with db.session() as session:
                await session.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
    finally:
        await db.dispose()


# ──────────────────────────────────────────────────────────── 库与语料辅助


def open_storage(dsn: str | None = None) -> Any:
    """构造 `Storage`（显式 DSN，不依赖进程单例）。"""
    from agenticdocer.store import Database, Storage

    return Storage(Database(configure_dsn(dsn)))


async def scalar(db: Any, sql: str, **params: Any) -> Any:
    from sqlalchemy import text

    async with db.session() as session:
        return (await session.execute(text(sql), params)).scalar_one()


async def all_rows(db: Any, sql: str, **params: Any) -> list[Any]:
    from sqlalchemy import text

    async with db.session() as session:
        return list((await session.execute(text(sql), params)).all())


_SIZES_SQL = """
SELECT c.relname, pg_total_relation_size(c.oid) AS bytes
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relkind IN ('r', 'p') AND NOT c.relispartition
ORDER BY bytes DESC
"""


async def pg_info(db: Any) -> dict[str, Any]:
    """库级事实：PG 版本、13 张基表体积（不含分区行，故无重复计数）、`nodes` 分区数。"""
    version = str(await scalar(db, "SHOW server_version"))
    sizes = {str(name): int(size) for name, size in await all_rows(db, _SIZES_SQL)}
    total = sum(sizes.values())
    parts = int(await scalar(db, "SELECT count(*) FROM pg_partition_tree('nodes') WHERE isleaf"))
    return {
        "server_version": version,
        "nodes_partition_count": parts,
        "table_bytes": sizes,
        "total_bytes": total,
        "total_human": human_bytes(total),
    }


async def counts(db: Any) -> dict[str, int]:
    """`docs`/`nodes`/`events` 计数（规模事实）。"""
    from sqlalchemy import text

    async with db.session() as session:
        result = {}
        for table in ("docs", "nodes", "events"):
            result[table] = int(
                (await session.execute(text(f"SELECT count(*) FROM {table}"))).scalar_one()
            )
    return result


def corpus_paths() -> list[Path]:
    """7 份真实语料（`spec/standards/*/*.md`）。"""
    return sorted(CORPUS_DIR.glob("*/*.md"))


async def import_corpus(storage: Any, *, only: Iterable[Path] | None = None) -> list[dict[str, Any]]:
    """真实语料 → 解析 + 入库（in-process，与 M11 `import commit` 同一函数路径）。"""
    from agenticdocer.importer import commit_document, coverage, parse_markdown
    from agenticdocer.model import WriteContext

    ctx = WriteContext(actor="perf-bench", source="importer")
    records: list[dict[str, Any]] = []
    for path in only if only is not None else corpus_paths():
        text = path.read_text(encoding="utf-8")
        watch = Stopwatch()
        result = parse_markdown(path)
        parse_us = watch.elapsed_us()
        watch.restart()
        committed = await commit_document(result, ctx, storage=storage)
        commit_us = watch.elapsed_us()
        records.append({
            "file": str(path.relative_to(ROOT)),
            "doc_slug": path.stem,
            "bytes": len(text.encode("utf-8")),
            "proposals": len(result.proposals),
            "rule_covered": result.stats.rule_covered,
            "blocks": result.stats.total_blocks,
            "fallback": result.stats.fallback,
            "pending": result.stats.pending,
            "coverage": round(coverage(result.stats), 6),
            "unmapped": len(result.unmapped),
            "parse_ms": round(parse_us / 1000, 3),
            "commit_ms": round(commit_us / 1000, 3),
            "nodes_created": committed.nodes_created,
            "refs_created": committed.refs_created,
        })
    return records


async def ensure_corpus(storage: Any, *, allow_ingest: bool = True) -> list[dict[str, Any]] | None:
    """库内无文档时导入真实语料（使基准可独立运行）；已有则返回 `None`（复用）。"""
    existing = int(await scalar(storage.db, "SELECT count(*) FROM docs"))
    if existing:
        return None
    if not allow_ingest:
        raise RuntimeError("库内无文档且已禁用入库（--no-ingest）；请先跑 bench_import.py")
    return await import_corpus(storage)


# ──────────────────────────────────────────────────────── 固定查询集与点查基准


async def sample_points(
    storage: Any, *, count: int, max_docs: int, seed: int
) -> list[tuple[str, str]]:
    """固定（确定性）点查集：随机取样文档 + 文档内 `ordinal` 序前若干节点。

    确定性来源：`seed` 固定 + `ORDER BY doc_id` / `ORDER BY ordinal`。
    """
    db = storage.db
    doc_ids = [str(row[0]) for row in await all_rows(db, "SELECT doc_id FROM docs ORDER BY doc_id")]
    if not doc_ids:
        return []
    rng = random.Random(seed)
    if len(doc_ids) > max_docs:
        doc_ids = sorted(rng.sample(doc_ids, max_docs))
    per_doc = max(1, math.ceil(count / len(doc_ids)))
    points: list[tuple[str, str]] = []
    from sqlalchemy import text

    async with db.session() as session:
        for doc_id in doc_ids:
            rows = (
                await session.execute(
                    text(
                        "SELECT node_id FROM nodes WHERE doc_id = :doc_id AND status = 'active' "
                        "ORDER BY ordinal LIMIT :k"
                    ),
                    {"doc_id": doc_id, "k": per_doc},
                )
            ).scalars()
            points.extend((doc_id, str(node_id)) for node_id in rows)
    rng.shuffle(points)
    return points[:count]


async def bench_point_query_set(
    storage: Any, points: Sequence[tuple[str, str]], *, warmup: int = 10
) -> dict[str, dict[str, float]]:
    """点查两组用例（ADR-009 V16）：带 `doc_id`（分区裁剪）与不带（全 64 分区扇扫）。"""
    for doc_id, node_id in list(points)[:warmup]:
        await storage.get_node(node_id, doc_id=doc_id)
        await storage.get_node(node_id)
    with_doc: list[int] = []
    without_doc: list[int] = []
    for doc_id, node_id in points:
        watch = Stopwatch()
        await storage.get_node(node_id, doc_id=doc_id)
        with_doc.append(watch.elapsed_us())
        watch.restart()
        await storage.get_node(node_id)
        without_doc.append(watch.elapsed_us())
    return {
        "with_doc_id": timing_stats(with_doc),
        "without_doc_id": timing_stats(without_doc),
    }


_EXPLAIN_SQL = (
    "EXPLAIN (FORMAT JSON) SELECT node_id FROM nodes WHERE node_id = '{node}'::uuid "
    "AND status = 'active'{doc}"
)


def _sql_literal(value: str) -> str:
    """SQL 单引号字面量（EXPLAIN 断言用字面量而非参数，避免通用计划干扰裁剪判据）。"""
    return "'" + value.replace("'", "''") + "'"


def _scan_relations(plan: Any) -> list[str]:
    names: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            rel = node.get("Relation Name")
            if isinstance(rel, str):
                names.append(rel)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(plan)
    return names


def _plan_root(plan: Any) -> Any:
    if isinstance(plan, str):
        plan = json.loads(plan)
    if isinstance(plan, list) and plan:
        plan = plan[0]
    if isinstance(plan, dict):
        return plan.get("Plan", plan)
    return {}


async def explain_partitions(
    db: Any, *, node_id: str, doc_id: str | None, force_generic: bool = False
) -> dict[str, Any]:
    """`EXPLAIN (FORMAT JSON)` 的分区命中数（**字面量**，避免自定义/通用计划歧义）。

    `force_generic=True` 时改用参数化查询 + `plan_cache_mode=force_generic_plan`，
    用于探测「应用侧预编译语句在通用计划下是否仍能裁剪」（真实风险点）。
    """
    from uuid import UUID

    from sqlalchemy import text

    safe_node = str(UUID(str(node_id)))
    clause = f" AND doc_id = {_sql_literal(doc_id)}" if doc_id else ""
    sql = _EXPLAIN_SQL.format(node=safe_node, doc=clause)
    async with db.session() as session:
        if force_generic:
            await session.execute(text("SET plan_cache_mode = force_generic_plan"))
            statement = text(
                "EXPLAIN (FORMAT JSON) SELECT node_id FROM nodes WHERE node_id = :node_id "
                "AND status = 'active'" + (" AND doc_id = :doc_id" if doc_id else "")
            )
            params: dict[str, Any] = {"node_id": safe_node}
            if doc_id:
                params["doc_id"] = doc_id
            rows = (await session.execute(statement, params)).all()
        else:
            rows = (await session.execute(text(sql))).all()
    plan = rows[0][0]
    relations = _scan_relations(plan)
    partitions = sum(1 for name in relations if re.fullmatch(r"nodes_p\d+", name))
    root = _plan_root(plan)
    return {
        "partitions": partitions,
        "scanned_relations": relations,
        "plan_node_type": root.get("Node Type"),
        "plan_cache_mode": "force_generic_plan" if force_generic else "default",
        "sql": sql,
    }


# ─────────────────────────────────────────────────────────────── 渲染基准辅助


async def top_docs(storage: Any, limit: int = 2) -> list[tuple[str, int, str]]:
    """库内按**内容体积**降序的文档 → `[(doc_id, content 字节数, title)]`。

    内容体积 = `sum(length(nodes.content::text))`（库内实际载荷），与源文件大小口径不同
    （jsonb 文本化 + 表格/HTML 片段会放大），故渲染基准默认取前 N 份逐一测量，
    避免「最大文档」的选择影响判定（§1.4 举的是 CXL 3.59MB，库内 PCIe 载荷略大）。
    """
    from sqlalchemy import text

    async with storage.db.session() as session:
        rows = (
            await session.execute(
                text(
                    "SELECT n.doc_id, sum(length(n.content::text)) AS bytes, max(d.title) AS title "
                    "FROM nodes n JOIN docs d ON d.doc_id = n.doc_id "
                    "WHERE n.status = 'active' "
                    "GROUP BY n.doc_id ORDER BY bytes DESC NULLS LAST LIMIT :limit"
                ),
                {"limit": max(1, limit)},
            )
        ).all()
    if not rows:
        raise RuntimeError("库内无节点：请先入库语料（bench_import.py）")
    return [(str(row[0]), int(row[1] or 0), str(row[2] or "")) for row in rows]


async def largest_doc(storage: Any) -> tuple[str, int, str]:
    """库内内容体积最大的文档（`top_docs(limit=1)` 的简写形式）。"""
    return (await top_docs(storage, limit=1))[0]


async def largest_section(storage: Any, doc_id: str) -> tuple[Any, str, int, int]:
    """文档内子树最大的 level-1/2 章节 → `(node_id, anchor, node_count, doc_nodes)`。"""
    from agenticdocer.render.sections import list_sections

    nodes = await storage.get_doc_nodes(doc_id)
    sections = list_sections(nodes, max_level=2)
    if not sections:
        raise RuntimeError(f"文档 {doc_id} 无 level-1/2 章节：无法测章节渲染")
    best = max(sections, key=lambda item: item.node_count)
    return best.node_id, best.anchor, best.node_count, len(nodes)


async def bench_render_set(
    storage: Any,
    *,
    doc_id: str,
    section_node_id: Any,
    document_iterations: int,
    section_iterations: int,
    warmup: int = 1,
) -> dict[str, Any]:
    """整档 + 单章节渲染计时（ADR-010 §3.2；指标 §1.4：章节 <1s、整档 <3s）。"""
    from agenticdocer.render import render_document, render_section

    with tempfile.TemporaryDirectory(prefix="perf-render-") as tmp:
        out = Path(tmp)
        for _ in range(warmup):
            await render_document(doc_id, out, storage=storage)
            await render_section(doc_id, section_node_id, out, storage=storage)

        document_samples: list[int] = []
        document_bytes = 0
        for _ in range(max(1, document_iterations)):
            result, micros = await timed(render_document(doc_id, out, storage=storage))
            document_samples.append(micros)
            document_bytes = Path(result.out_path).stat().st_size

        section_samples: list[int] = []
        section_bytes = 0
        for _ in range(max(1, section_iterations)):
            result, micros = await timed(render_section(doc_id, section_node_id, out, storage=storage))
            section_samples.append(micros)
            section_bytes = Path(result.out_path).stat().st_size

        # 归因：章节渲染内部会整档加载节点（`get_doc_nodes`），单独计时以便定位瓶颈
        node_load_samples: list[int] = []
        for _ in range(3):
            _, micros = await timed(storage.get_doc_nodes(doc_id))
            node_load_samples.append(micros)

    return {
        "document": timing_stats(document_samples),
        "section": timing_stats(section_samples),
        "document_bytes": document_bytes,
        "section_bytes": section_bytes,
        "section_load_nodes": timing_stats(node_load_samples),
    }


# ──────────────────────────────────────────────────────────── 合成语料（规模）


def synthetic_markdown(index: int, *, atoms: int, doc_id: str, seed: int = 0) -> str:
    """合成一份 `atoms` 量级的 markdown（结构同真实语料：标题 + 段落 + 表格）。

    每节产出 2 个原子（heading → `clause`，其段落并入 fragment；`<table>` → `table`），
    故节数 = `atoms/2`。内容确定性（同一 `index` 逐字节一致）。
    """
    rng = random.Random(seed * 1_000_003 + index)
    sections = max(1, math.ceil(atoms / 2))
    parts: list[str] = [
        "---",
        f"title: Synthetic Spec {index:06d}",
        "type: composite",
        "purpose: spec",
        "audience: both",
        "direction: input",
        'version: "1.0.0"',
        'section_meta: "@meta"',
        "spec_type: standard",
        f"spec_id: {doc_id}",
        "spec_org: PERF",
        f"spec_revision: SYN-{index:06d}",
        f"source: synthetic/perf/{index:06d}.md",
        "converted_by: perf-bench",
        "converted_at: 2026-09-16",
        "reviewed_by: perf-bench",
        "reviewed_at: 2026-09-16",
        "status: approved",
        "---",
        f"# Synthetic Spec {index:06d}",
    ]
    for number in range(1, sections + 1):
        token = f"{index:06d}-{number:04d}"
        parts.append(f"## 1.{number} Clause {token}")
        parts.append(
            f"This clause describes requirement {token}: the agent shall keep the "
            f"invariant stable across {rng.randint(2, 64)} cycles. "
            f"See Section 1.{max(1, number - 1)} for the preceding requirement."
        )
        parts.append(
            f"<table><tr><td>Parameter</td><td>Value</td></tr>"
            f"<tr><td>id</td><td>{token}</td></tr>"
            f"<tr><td>latency</td><td>{rng.randint(1, 500)}ns</td></tr></table>"
        )
    return "\n\n".join(parts) + "\n"


async def ingest_synthetic(
    storage: Any, *, docs: int, atoms_per_doc: int, seed: int = 7, progress_every: int = 25
) -> dict[str, Any]:
    """合成 `docs` 份文档灌入（**真实 M03 路径**：parse_text → commit_document）。"""
    from agenticdocer.importer import commit_document, parse_text
    from agenticdocer.model import WriteContext

    ctx = WriteContext(actor="perf-bench", source="importer")
    totals = {"docs": 0, "nodes_created": 0, "refs_created": 0, "proposals": 0, "blocks": 0,
              "fallback": 0, "chars": 0}
    watch = Stopwatch()
    for index in range(docs):
        doc_id = f"SPEC-SYN-{index:06d}"
        text = synthetic_markdown(index, atoms=atoms_per_doc, doc_id=doc_id, seed=seed)
        totals["chars"] += len(text)
        result = parse_text(text, doc_slug=f"syn-{index:06d}")
        committed = await commit_document(result, ctx, storage=storage)
        totals["docs"] += 1
        totals["nodes_created"] += committed.nodes_created
        totals["refs_created"] += committed.refs_created
        totals["proposals"] += len(result.proposals)
        totals["blocks"] += result.stats.total_blocks
        totals["fallback"] += result.stats.fallback
        if progress_every and (index + 1) % progress_every == 0:
            print(f"  … 已灌 {index + 1}/{docs} 份（{watch.elapsed_ms() / 1000:.1f}s）", flush=True)
    totals["ingest_ms"] = round(watch.elapsed_ms(), 3)
    totals["nodes_per_s"] = (
        round(totals["nodes_created"] / (totals["ingest_ms"] / 1000), 1) if totals["ingest_ms"] else 0.0
    )
    return totals


def trim_metrics(bench: Bench, *, keep: int = 40) -> Bench:
    """超长指标集（如逐文件/逐分区明细）不截断错误项，只保留前 `keep` 项明细。"""
    if len(bench.metrics) <= keep:
        return bench
    head = bench.metrics[:keep]
    bench.metrics = head
    bench.note(f"指标明细截断：仅保留前 {keep} 项（完整数据见归档 JSON）")
    return bench


__all__ = [
    "BUILD",
    "Bench",
    "CORPUS_DIR",
    "DEFAULT_DSN",
    "HISTORY_LIMIT",
    "Metric",
    "PERF_ARCHIVE",
    "PERF_JSON",
    "ROOT",
    "SCHEMA_VERSION",
    "Stopwatch",
    "TARGET_AUTH_P95_MS",
    "TARGET_COVERAGE",
    "TARGET_DOCUMENT_MS",
    "TARGET_DOCS",
    "TARGET_NODES",
    "TARGET_NODES_PER_DOC",
    "TARGET_PARTITION_COUNT",
    "TARGET_PARTITION_CV",
    "TARGET_POINT_P95_MS",
    "TARGET_SECTION_MS",
    "add_common_args",
    "all_rows",
    "bench_point_query_set",
    "bench_render_set",
    "compare_rows",
    "configure_dsn",
    "corpus_paths",
    "counts",
    "current_dsn",
    "default_args",
    "ensure_corpus",
    "environment",
    "execute",
    "explain_partitions",
    "human_bytes",
    "import_corpus",
    "ingest_synthetic",
    "largest_doc",
    "largest_section",
    "load_store",
    "masked_dsn",
    "metric",
    "now_iso",
    "open_storage",
    "pg_info",
    "previous_run",
    "print_report",
    "reachable",
    "render_table",
    "sample_points",
    "save",
    "scalar",
    "synthetic_markdown",
    "timed",
    "timing_stats",
    "trim_metrics",
]
