"""`bench_point_query` — 点查延迟 P50/P95/P99（ADR-010 §3.2；指标 §1.4：P95 <200ms）。

**两个用例（ADR-009 V16「读路径约束」硬要求）**：

1. **带 `doc_id`** → `nodes` 按 `doc_id` HASH 分区，命中单分区（**索引级**）；
2. **不带 `doc_id`** → 需探测全部 64 分区（**已知降级路径**，本基准记录的基线）。

结果中降级路径带 `degraded=True` 标记，独立成块输出，不与正常路径混列。
并断言 `EXPLAIN` 的分区数（带 → 1，不带 → 64）——使「分区裁剪是否生效」成为可复算事实，
而非阅读 DDL 的推断。

另含一项**风险探针**：`plan_cache_mode=force_generic_plan` 下带 `doc_id` 的点查是否仍裁剪
（应用侧 asyncpg 预编译语句在通用计划下可能丢失参数化裁剪，ADR-009 §风险）。

运行：

    uv run python tests/perf/bench_point_query.py --dsn <dsn> [--queries 200] [--compare] [--json]
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
    TARGET_PARTITION_COUNT,
    TARGET_POINT_P95_MS,
    Bench,
    add_common_args,
    bench_point_query_set,
    configure_dsn,
    counts,
    default_args,
    ensure_corpus,
    environment,
    execute,
    explain_partitions,
    metric,
    open_storage,
    reachable,
    render_table,
    sample_points,
    save,
)

pytestmark = pytest.mark.perf

NAME = "point_query"
TITLE = "点查延迟 P95（§1.4 <200ms；ADR-009 V16 双用例）"

DEGRADED_NOTE = "ADR-009 V16 已知降级路径：无 doc_id 时无法分区裁剪，需扇扫全部 64 分区"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="点查延迟基准（含分区裁剪断言）")
    add_common_args(parser)
    parser.add_argument("--queries", type=int, default=200, help="固定查询集大小（§1.4 要求 ≥100）")
    parser.add_argument("--warmup", type=int, default=10, help="预热次数（不计入统计）")
    parser.add_argument("--docs-sample", type=int, default=50,
                        help="取样文档数上限（大规模库下控制准备耗时）")
    parser.add_argument("--seed", type=int, default=20260916, help="查询集抽样种子（固定即固定查询集）")
    parser.add_argument("--no-ingest", action="store_true", help="库空时不自动导入语料，直接报错")
    return parser


async def run_bench(args: argparse.Namespace) -> Bench:
    storage = open_storage(args.dsn)
    db = storage.db
    bench = Bench(name=NAME, title=TITLE, environment=environment())
    try:
        ingested = await ensure_corpus(storage, allow_ingest=not args.no_ingest)
        if ingested:
            nodes = sum(int(r["nodes_created"]) for r in ingested)
            bench.note(f"库内无语料，已自动导入 {len(ingested)} 份真实语料（新增 {nodes} 节点）")

        facts = await counts(db)
        points = await sample_points(storage, count=args.queries, max_docs=args.docs_sample, seed=args.seed)
        if not points:
            raise RuntimeError("查询集为空：库内无节点，请先跑 bench_import.py（或去掉 --no-ingest）")

        results = await bench_point_query_set(storage, points, warmup=args.warmup)

        sample_doc, sample_node = points[0]
        explain_pruned = await explain_partitions(db, node_id=sample_node, doc_id=sample_doc)
        explain_scan = await explain_partitions(db, node_id=sample_node, doc_id=None)
        try:
            explain_generic = await explain_partitions(
                db, node_id=sample_node, doc_id=sample_doc, force_generic=True
            )
        except Exception as exc:  # pragma: no cover - 老版本 PG 无 plan_cache_mode
            explain_generic = {"partitions": None, "plan_node_type": f"probe failed: {exc}"}

        print("\nEXPLAIN 分区裁剪证据（字面量 SQL，基于查询集首点）：")
        print(render_table(
            ["用例", "计划根节点", "扫描分区数", "SQL"],
            [
                ["带 doc_id", str(explain_pruned["plan_node_type"]),
                 explain_pruned["partitions"], explain_pruned["sql"]],
                ["不带 doc_id", str(explain_scan["plan_node_type"]),
                 explain_scan["partitions"], explain_scan["sql"]],
            ],
        ))
        print(f"风险探针（plan_cache_mode=force_generic_plan，带 doc_id）："
              f"扫描 {explain_generic['partitions']} 分区 / 根节点 {explain_generic['plan_node_type']}")

        bench.counters.update({
            "queries": len(points),
            "requested_queries": args.queries,
            "warmup": args.warmup,
            "seed": args.seed,
            "docs_sample": args.docs_sample,
            "docs_in_db": facts["docs"],
            "nodes_in_db": facts["nodes"],
            "explain_with_doc_id": explain_pruned,
            "explain_without_doc_id": explain_scan,
            "explain_force_generic_with_doc_id": {
                "partitions": explain_generic.get("partitions"),
                "plan_node_type": explain_generic.get("plan_node_type"),
            },
        })

        pruned = results["with_doc_id"]
        scanned = results["without_doc_id"]
        bench.add(
            metric("point_query.with_doc_id.p50_ms", pruned["p50_ms"], unit="ms"),
            metric("point_query.with_doc_id.p95_ms", pruned["p95_ms"], unit="ms",
                   target=TARGET_POINT_P95_MS, note="§1.4 点查延迟 P95（分区裁剪路径）"),
            metric("point_query.with_doc_id.p99_ms", pruned["p99_ms"], unit="ms"),
            metric("point_query.with_doc_id.mean_ms", pruned["mean_ms"], unit="ms"),
            metric("point_query.with_doc_id.max_ms", pruned["max_ms"], unit="ms"),
            metric("point_query.without_doc_id.p50_ms", scanned["p50_ms"], unit="ms", degraded=True),
            metric("point_query.without_doc_id.p95_ms", scanned["p95_ms"], unit="ms",
                   target=TARGET_POINT_P95_MS, degraded=True, note=DEGRADED_NOTE),
            metric("point_query.without_doc_id.p99_ms", scanned["p99_ms"], unit="ms", degraded=True),
            metric("point_query.without_doc_id.mean_ms", scanned["mean_ms"], unit="ms", degraded=True),
            metric("point_query.without_doc_id.max_ms", scanned["max_ms"], unit="ms", degraded=True),
            metric("explain.with_doc_id.partitions", explain_pruned["partitions"],
                   target=1.0, comparison="==",
                   note="ADR-009 V16：带 doc_id 必须裁剪到单一分区"),
            metric("explain.without_doc_id.partitions", explain_scan["partitions"],
                   target=float(TARGET_PARTITION_COUNT), comparison="==", degraded=True,
                   note="ADR-009 V16：不带 doc_id 扇扫全部 64 分区（预期行为，非缺陷）"),
            metric("explain.with_doc_id.partitions_force_generic",
                   explain_generic.get("partitions"), degraded=True,
                   note="风险探针：通用计划下是否仍裁剪（None = 该 PG 不支持 plan_cache_mode）"),
        )

        bench.notes.append(
            f"固定查询集：{len(points)} 点（seed={args.seed}，取样文档 "
            f"{min(args.docs_sample, facts['docs'])}/{facts['docs']} 份；库内 {facts['nodes']} 节点）"
        )
        if len(points) < 100:
            bench.notes.append(f"**警告**：查询集仅 {len(points)} 次，低于 §1.4 要求的 100 次")
        bench.notes.append(
            "带 doc_id 的 P95 若超 §1.4 指标 → 触发 ADR-009 V16.5 升级条件（建 node_id→doc_id "
            "映射表或调整分区键，单开 migration revision）"
        )
        bench.notes.append(
            "降级路径与正常路径的差值即「分区裁剪」的净收益；该比值应随库规模增长而扩大"
        )
    finally:
        await db.dispose()
    return bench


def test_point_query_benchmark() -> None:
    """`pytest -m perf` 路径：断言分区裁剪事实（架构不变量）与查询集规模。"""
    args = default_args(build_parser())
    if not reachable(args.dsn):
        pytest.skip(f"基准库不可达：{configure_dsn(args.dsn)}")
    bench = asyncio.run(run_bench(args))
    save(bench, args.out)
    pruned = bench.get("explain.with_doc_id.partitions")
    scanned = bench.get("explain.without_doc_id.partitions")
    assert pruned is not None and pruned.value == 1, f"带 doc_id 未裁剪到单分区：{pruned}"
    assert scanned is not None and scanned.value == TARGET_PARTITION_COUNT, (
        f"不带 doc_id 未扇扫全部 {TARGET_PARTITION_COUNT} 分区：{scanned}"
    )
    assert bench.counters["queries"] >= 100, f"查询集不足 100 次：{bench.counters['queries']}"


if __name__ == "__main__":
    sys.exit(execute(build_parser(), run_bench))
