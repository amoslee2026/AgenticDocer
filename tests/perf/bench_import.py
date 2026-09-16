"""`bench_import` — 7 份真实语料的导入吞吐与解析覆盖率（ADR-010 §3.2）。

对应指标（`architecture_specification.md` §1.4）：**解析规则覆盖率 ≥95%；零静默丢弃**。
口径出自 REQ-M03-F01/F04 与 design_doc §10：

* 覆盖率 = 携带 `rule_id` 的**源块**数 ÷ 总源块数（`importer.parser.coverage`，唯一口径）；
* 零静默丢弃 = 每个源块要么被规则覆盖、要么进兜底（`total_blocks == rule_covered + fallback`），
  兜底块也 100% 入库。

导入走 **in-process 真实路径**（`parse_markdown` → `commit_document`），与 M11
`import commit` 同一函数（§1.3 调用路径裁决），不另造旁路。

运行：

    uv run python tests/perf/bench_import.py --dsn <dsn> [--truncate] [--compare] [--json]
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import pytest  # noqa: E402

from _common import (  # noqa: E402
    TARGET_COVERAGE,
    Bench,
    Stopwatch,
    add_common_args,
    configure_dsn,
    counts,
    default_args,
    ensure_corpus,
    environment,
    execute,
    import_corpus,
    metric,
    open_storage,
    reachable,
    render_table,
    save,
)

pytestmark = pytest.mark.perf

NAME = "import"
TITLE = "导入吞吐与解析覆盖率（§1.4：覆盖率 ≥95%、零静默丢弃）"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="M03 导入吞吐与解析覆盖率基准")
    add_common_args(parser)
    parser.add_argument("--truncate", action="store_true",
                        help="入库前清空实体表（nodes/docs/refs/comments/assets），得到纯净的首次导入耗时")
    parser.add_argument("--file", action="append", default=None,
                        help="只导入指定语料（可重复；默认全部 7 份）")
    return parser


async def truncate_entities(db) -> None:
    """清空实体表（`events` 是 append-only 权威审计，**不动**；P2）。"""
    from sqlalchemy import text

    async with db.engine.begin() as connection:
        await connection.execute(
            text("TRUNCATE TABLE comments, refs, nodes, docs, assets CASCADE")
        )


async def run_bench(args: argparse.Namespace) -> Bench:
    storage = open_storage(args.dsn)
    db = storage.db
    bench = Bench(name=NAME, title=TITLE, environment=environment())
    try:
        if args.truncate:
            await truncate_entities(db)
        bench.counters["truncated"] = bool(args.truncate)
        before = await counts(db)
        if before["docs"] and not args.truncate:
            bench.note(
                f"库内已有 {before['docs']} 份文档：`commit_document` 幂等（同锚复用节点），"
                "`nodes_created` 会是 0——要测首次导入吞吐请加 `--truncate`"
            )

        only = [Path(item).resolve() for item in args.file] if args.file else None
        watch = Stopwatch()
        records = await import_corpus(storage, only=only)
        wall_ms = watch.elapsed_ms()
        after = await counts(db)

        blocks = sum(int(r["blocks"]) for r in records)
        covered = sum(int(r["rule_covered"]) for r in records)
        fallback = sum(int(r["fallback"]) for r in records)
        nodes_created = sum(int(r["nodes_created"]) for r in records)
        refs_created = sum(int(r["refs_created"]) for r in records)
        parse_ms = sum(float(r["parse_ms"]) for r in records)
        commit_ms = sum(float(r["commit_ms"]) for r in records)
        payload = sum(int(r["bytes"]) for r in records)
        coverage = covered / blocks if blocks else 0.0
        accounting_ok = blocks == covered + fallback

        print(f"\n逐文件明细（{len(records)} 份语料）：")
        print(render_table(
            ["语料", "字节", "源块", "规则覆盖", "兜底", "待确认", "节点", "解析ms", "入库ms"],
            [
                [
                    Path(r["file"]).name,
                    r["bytes"],
                    r["blocks"],
                    r["rule_covered"],
                    r["fallback"],
                    r["pending"],
                    r["nodes_created"],
                    f"{r['parse_ms']:.1f}",
                    f"{r['commit_ms']:.1f}",
                ]
                for r in records
            ],
        ))

        bench.counters.update({
            "files": len(records),
            "blocks": blocks,
            "rule_covered": covered,
            "fallback": fallback,
            "zero_silent_drop": accounting_ok,
            "nodes_created": nodes_created,
            "nodes_after": after["nodes"],
            "docs_after": after["docs"],
            "refs_created": refs_created,
            "payload_bytes": payload,
            "wall_ms": round(wall_ms, 3),
        })

        bench.add(
            metric("import.coverage", round(coverage, 6), target=TARGET_COVERAGE,
                   comparison=">=", unit="ratio",
                   note="携带 rule_id 的源块 ÷ 总源块（REQ-M03-F01；M03 实测 0.9993）"),
            metric("import.min_file_coverage",
                   round(min(float(r["coverage"]) for r in records), 6), unit="ratio",
                   note="单份语料最低覆盖率（判据仍以聚合值 `import.coverage` 为准）"),
            metric("import.fallback_ratio",
                   round(fallback / blocks, 6) if blocks else 0.0, unit="ratio",
                   note="兜底块占比（兜底块亦 100% 入库，非丢弃）"),
            metric("import.pending_blocks", sum(int(r["pending"]) for r in records),
                   note="待确认块（低置信规则命中）"),
            metric("import.docs", len(records)),
            metric("import.payload_mib", round(payload / 1024 / 1024, 3), unit="MiB"),
            metric("import.parse_total_s", round(parse_ms / 1000, 3), unit="s"),
            metric("import.commit_total_s", round(commit_ms / 1000, 3), unit="s"),
            metric("import.wall_s", round(wall_ms / 1000, 3), unit="s"),
            metric("import.docs_per_min",
                   round(len(records) / (wall_ms / 60000), 2) if wall_ms else 0.0),
            metric("import.nodes_per_s",
                   round(nodes_created / (wall_ms / 1000), 1) if wall_ms else 0.0),
            metric("import.mib_per_s",
                   round(payload / 1024 / 1024 / (wall_ms / 1000), 3) if wall_ms else 0.0),
        )
        for record in records:
            slug = record["doc_slug"]
            bench.add(
                metric(f"import.{slug}.coverage", round(float(record["coverage"]), 6), unit="ratio"),
                metric(f"import.{slug}.blocks", int(record["blocks"])),
                metric(f"import.{slug}.parse_ms", round(float(record["parse_ms"]), 3), unit="ms"),
                metric(f"import.{slug}.commit_ms", round(float(record["commit_ms"]), 3), unit="ms"),
                metric(f"import.{slug}.nodes_created", int(record["nodes_created"])),
            )

        bench.note(
            f"零静默丢弃对账：total_blocks {blocks} == rule_covered {covered} + fallback {fallback}"
            f" → {'成立' if accounting_ok else '**不成立**'}"
        )
        bench.note(
            "`nodes_created` 以 `CommitResult` 计（新增节点）；`nodes_after` 为库内总数，"
            "幂等重跑时前者为 0 属预期"
        )
        bench.note(
            "解析为确定性纯函数（无 LLM/网络，P6）；入库为逐节点事务（M02「事件+实体同事务」），"
            "故 commit 远慢于 parse——批量导入优化见 ADR-009 §3（COPY + 分批）"
        )
    finally:
        await db.dispose()
    return bench


def test_import_benchmark() -> None:
    """`pytest -m perf` 路径：跑默认规模并断言覆盖率/零静默丢弃（§1.4 硬指标）。"""
    args = default_args(build_parser())
    if not reachable(args.dsn):
        pytest.skip(f"基准库不可达：{configure_dsn(args.dsn)}")
    bench = asyncio.run(run_bench(args))
    save(bench, args.out)
    coverage = bench.get("import.coverage")
    assert coverage is not None and coverage.value >= TARGET_COVERAGE, f"覆盖率不达标：{coverage}"
    assert bench.counters["zero_silent_drop"] is True, "零静默丢弃对账不成立"
    assert bench.counters["files"] == 7, f"语料份数不是 7：{bench.counters['files']}"


def test_corpus_ingest_is_idempotent() -> None:
    """幂等复核（M02「无变化不写事件」）：语料二次 commit 不新增节点。"""
    args = default_args(build_parser())
    if not reachable(args.dsn):
        pytest.skip(f"基准库不可达：{configure_dsn(args.dsn)}")
    asyncio.run(_idempotency_probe(args))


async def _idempotency_probe(args: argparse.Namespace) -> None:
    storage = open_storage(args.dsn)
    try:
        await ensure_corpus(storage)
        records = await import_corpus(storage)
        created = sum(int(r["nodes_created"]) for r in records)
        assert created == 0, f"幂等性被破坏：二次导入新增了 {created} 个节点"
    finally:
        await storage.db.dispose()


if __name__ == "__main__":
    sys.exit(execute(build_parser(), run_bench))
