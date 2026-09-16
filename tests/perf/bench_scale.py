"""`bench_scale` — 10k 文档规模验收（ADR-010 §3.2；ADR-009 规模策略的验收手段）。

§1.4/ADR-009 的目标规模是 **10,000 份文档 ≈13.4M 节点 ≈20–54GB**（≈1,343 原子/文档，
按 7 份真实语料实测校准）。本基准合成语料灌入后测：

| 测项 | 手段 | 判据 |
|---|---|---|
| 点查延迟 | 复用 `bench_point_query` 的双用例查询集 | §1.4 P95 <200ms（含 ADR-009 V16 降级路径） |
| 渲染 | 复用 `bench_render`（最大文档 + 最大章节） | §1.4 章节 <1s / 整档 <3s |
| 存储量 | `pg_total_relation_size` 汇总（13 张基表，不含分区行重复计数） | §1.4 20–54GB（按真实语料密度外推） |
| 分区有效性 | `pg_partition_tree` 分区数 + 各分区行数分布 + `EXPLAIN` 裁剪 | 64 分区、均衡、带 doc_id 裁剪到 1 |

**合成语料走真实 M03 路径**（`parse_text` → `commit_document`），不另造写库旁路；
节点总数按**实测原子/文档**计数，不外推假设。

规模可调：`--docs`（默认 100，冒烟）/ `--atoms-per-doc`（默认 1343，即 §1.4 口径）。
未跑到 10k 时，结果中 `scale.docs` 与 10k 目标的差距、以及线性外推的存储/节点量
会**显式标注**，不做静默替代。

运行：

    uv run python tests/perf/bench_scale.py --dsn <dsn> --docs 100          # 冒烟
    uv run python tests/perf/bench_scale.py --dsn <dsn> --docs 10000 --compare
"""

from __future__ import annotations

import argparse
import asyncio
import statistics
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import pytest  # noqa: E402

from _common import (  # noqa: E402
    TARGET_DOCS,
    TARGET_DOCUMENT_MS,
    TARGET_NODES,
    TARGET_NODES_PER_DOC,
    TARGET_PARTITION_COUNT,
    TARGET_PARTITION_CV,
    TARGET_POINT_P95_MS,
    TARGET_SECTION_MS,
    Bench,
    add_common_args,
    all_rows,
    bench_point_query_set,
    bench_render_set,
    configure_dsn,
    counts,
    default_args,
    environment,
    execute,
    explain_partitions,
    human_bytes,
    ingest_synthetic,
    largest_doc,
    largest_section,
    metric,
    open_storage,
    pg_info,
    reachable,
    render_table,
    sample_points,
    save,
    scalar,
)

pytestmark = pytest.mark.perf

NAME = "scale"
TITLE = "10k 文档规模验收（ADR-009 规模 + §1.4 点查/渲染/存储/分区有效性）"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="规模验收基准（合成 10k 文档灌入 + 指标复测）")
    add_common_args(parser)
    parser.add_argument("--docs", type=int, default=100, help="合成文档数（§1.4 目标 10000）")
    parser.add_argument("--atoms-per-doc", type=int, default=TARGET_NODES_PER_DOC,
                        help=f"每文档原子数（§1.4 口径 {TARGET_NODES_PER_DOC}）")
    parser.add_argument("--seed", type=int, default=7, help="合成语料种子（内容确定性）")
    parser.add_argument("--queries", type=int, default=200, help="点查查询集大小（§1.4 ≥100）")
    parser.add_argument("--warmup", type=int, default=10, help="点查预热次数")
    parser.add_argument("--docs-sample", type=int, default=50, help="点查取样文档数上限")
    parser.add_argument("--document-iterations", type=int, default=3, help="整档渲染重复次数")
    parser.add_argument("--section-iterations", type=int, default=5, help="章节渲染重复次数")
    parser.add_argument("--skip-render", action="store_true", help="跳过渲染段（先只验规模/点查）")
    parser.add_argument("--fresh", action="store_true",
                        help="灌入前清空实体表（否则按 `SPEC-SYN-*` 幂等续灌，用于分批跑）")
    return parser


async def truncate_entities(db) -> None:
    from sqlalchemy import text

    async with db.engine.begin() as connection:
        await connection.execute(
            text("TRUNCATE TABLE comments, refs, nodes, docs, assets CASCADE")
        )


async def partition_rows(db) -> list[tuple[str, int]]:
    """各 `nodes` 分区行数（单次 Append 扫描，比逐分区 count 快得多）。"""
    rows = await all_rows(
        db, "SELECT tableoid::regclass::text AS part, count(*) AS rows FROM nodes GROUP BY 1 ORDER BY 1"
    )
    return [(str(name), int(count)) for name, count in rows]


async def events_partition_rows(db) -> list[tuple[str, int]]:
    rows = await all_rows(
        db,
        "SELECT tableoid::regclass::text AS part, count(*) AS rows FROM events GROUP BY 1 ORDER BY 1",
    )
    return [(str(name), int(count)) for name, count in rows]


async def run_bench(args: argparse.Namespace) -> Bench:
    storage = open_storage(args.dsn)
    db = storage.db
    bench = Bench(name=NAME, title=TITLE, environment=environment())
    try:
        if args.fresh:
            await truncate_entities(db)

        before = await counts(db)
        existing_syn = int(await scalar(
            db, "SELECT count(*) FROM docs WHERE doc_id LIKE 'SPEC-SYN-%'"
        ))
        print(f"灌入前：docs={before['docs']}（其中合成 {existing_syn}）nodes={before['nodes']}")
        ingest = await ingest_synthetic(
            storage, docs=args.docs, atoms_per_doc=args.atoms_per_doc, seed=args.seed
        )
        after = await counts(db)
        print(f"灌入后：docs={after['docs']} nodes={after['nodes']} events={after['events']}"
              f"（{ingest['ingest_ms'] / 1000:.1f}s，{ingest['nodes_per_s']:.0f} 节点/s）")

        info = await pg_info(db)
        parts = await partition_rows(db)
        events_parts = await events_partition_rows(db)
        syn_docs = int(await scalar(db, "SELECT count(*) FROM docs WHERE doc_id LIKE 'SPEC-SYN-%'"))
        syn_nodes = int(await scalar(
            db, "SELECT count(*) FROM nodes WHERE doc_id LIKE 'SPEC-SYN-%'"
        ))
        nodes_per_doc = syn_nodes / syn_docs if syn_docs else 0.0
        bytes_per_node = info["total_bytes"] / after["nodes"] if after["nodes"] else 0.0
        rows_per_part = [count for _, count in parts]
        cv = (
            statistics.pstdev(rows_per_part) / statistics.fmean(rows_per_part)
            if len(rows_per_part) > 1 and statistics.fmean(rows_per_part)
            else 0.0
        )

        # 分区行数分布（只打印头部/尾部，完整数据落 JSON）
        ordered = sorted(parts, key=lambda item: item[1])
        print(f"\n分区行数分布（{len(parts)} 分区）：min={ordered[0][1]} "
              f"max={ordered[-1][1]} mean={statistics.fmean(rows_per_part):.0f} "
              f"CV={cv:.3f}")
        print(render_table(
            ["分区", "行数"],
            [[name, count] for name, count in ordered[:3] + ordered[-3:]],
        ))

        # ── 点查（复用 bench_point_query 的口径）──────────────────────────
        points = await sample_points(
            storage, count=args.queries, max_docs=args.docs_sample, seed=20260916
        )
        if not points:
            raise RuntimeError("查询集为空：库内无节点")
        point_results = await bench_point_query_set(storage, points, warmup=args.warmup)
        sample_doc, sample_node = points[0]
        explain_pruned = await explain_partitions(db, node_id=sample_node, doc_id=sample_doc)
        explain_scan = await explain_partitions(db, node_id=sample_node, doc_id=None)

        bench.add(
            metric("scale.docs", after["docs"],
                   note=f"库内文档总数（含语料）；本次合成 {args.docs} 份（§1.4 目标 {TARGET_DOCS}）"),
            metric("scale.synthetic_docs", syn_docs),
            metric("scale.nodes", after["nodes"],
                   note=f"库内节点总数（§1.4 目标 ≈{TARGET_NODES:,}）"),
            metric("scale.synthetic_nodes", syn_nodes),
            metric("scale.nodes_per_doc", round(nodes_per_doc, 1),
                   note=f"实测原子/文档（§1.4 校准值 {TARGET_NODES_PER_DOC}）"),
            metric("scale.target_docs_ratio", round(after["docs"] / TARGET_DOCS, 4),
                   note="实际跑到的规模 ÷ 10k 目标（**如实记录未跑满**）"),
            metric("scale.ingest_nodes_per_s", ingest["nodes_per_s"]),
            metric("scale.ingest_wall_s", round(ingest["ingest_ms"] / 1000, 3), unit="s"),
            metric("scale.storage_total_gib", round(info["total_bytes"] / 1024**3, 4), unit="GiB",
                   note="13 张基表 pg_total_relation_size 汇总（表+索引+TOAST）"),
            metric("scale.bytes_per_node", round(bytes_per_node, 1), unit="B",
                   note="含索引放大；合成语料内容密度低于真实规范，故偏小"),
            metric("scale.partition_count", len(parts),
                   target=float(TARGET_PARTITION_COUNT), comparison="==",
                   note="ADR-009 §1：nodes HASH(doc_id) 64 分区"),
            metric("scale.partition_row_cv", round(cv, 4),
                   target=TARGET_PARTITION_CV,
                   note="各分区行数变异系数（ADR-009 §1「分区均衡」；样本文档数小时受抽样支配）"),
            metric("scale.partition_rows_min", min(rows_per_part) if rows_per_part else 0),
            metric("scale.partition_rows_max", max(rows_per_part) if rows_per_part else 0),
            metric("scale.events_partition_count", len(events_parts),
                   note="events RANGE(ts) 按月 + DEFAULT"),
            metric("scale.point_query.with_doc_id.p95_ms", point_results["with_doc_id"]["p95_ms"],
                   unit="ms", target=TARGET_POINT_P95_MS,
                   note="规模下复测（§1.4 P95 <200ms）"),
            metric("scale.point_query.with_doc_id.p50_ms", point_results["with_doc_id"]["p50_ms"],
                   unit="ms"),
            metric("scale.point_query.without_doc_id.p95_ms", point_results["without_doc_id"]["p95_ms"],
                   unit="ms", target=TARGET_POINT_P95_MS, degraded=True,
                   note="ADR-009 V16 已知降级路径（无 doc_id → 扇扫全部 64 分区）"),
            metric("scale.point_query.without_doc_id.p50_ms", point_results["without_doc_id"]["p50_ms"],
                   unit="ms", degraded=True),
            metric("scale.explain.with_doc_id.partitions", explain_pruned["partitions"],
                   target=1.0, comparison="==", note="规模下分区裁剪仍须成立"),
            metric("scale.explain.without_doc_id.partitions", explain_scan["partitions"],
                   target=float(TARGET_PARTITION_COUNT), comparison="==", degraded=True),
        )

        # ── 渲染（复用 bench_render 的口径）───────────────────────────────
        if not args.skip_render:
            doc_id, content_bytes, title = await largest_doc(storage)
            section_node_id, anchor, section_nodes, doc_nodes = await largest_section(storage, doc_id)
            render = await bench_render_set(
                storage, doc_id=doc_id, section_node_id=section_node_id,
                document_iterations=args.document_iterations,
                section_iterations=args.section_iterations,
            )
            bench.counters.update({
                "render_doc_id": doc_id,
                "render_doc_title": title,
                "render_doc_nodes": doc_nodes,
                "render_doc_content_bytes": content_bytes,
                "render_section_anchor": str(anchor),
                "render_section_nodes": section_nodes,
            })
            bench.add(
                metric("scale.render.document.p50_ms", render["document"]["p50_ms"], unit="ms",
                       target=TARGET_DOCUMENT_MS),
                metric("scale.render.document.max_ms", render["document"]["max_ms"], unit="ms",
                       target=TARGET_DOCUMENT_MS),
                metric("scale.render.section.p50_ms", render["section"]["p50_ms"], unit="ms",
                       target=TARGET_SECTION_MS),
                metric("scale.render.section.max_ms", render["section"]["max_ms"], unit="ms",
                       target=TARGET_SECTION_MS),
                metric("scale.render.document.nodes", doc_nodes),
                metric("scale.render.section.nodes", section_nodes),
                metric("scale.render.section.load_doc_nodes_p50_ms",
                       render["section_load_nodes"]["p50_ms"], unit="ms",
                       note="归因：章节渲染内部整档取数"),
            )

        # ── 外推（10k 文档口径）──────────────────────────────────────────
        bench.counters.update({
            "synthetic_docs": syn_docs,
            "synthetic_nodes": syn_nodes,
            "nodes_per_doc": round(nodes_per_doc, 1),
            "ingest": ingest,
            "pg": info,
            "partition_rows": dict(parts),
            "events_partition_rows": dict(events_parts),
            "query_set": len(points),
            "atoms_per_doc_requested": args.atoms_per_doc,
            "docs_requested": args.docs,
            "fresh": bool(args.fresh),
        })
        projected_nodes = nodes_per_doc * TARGET_DOCS
        projected_bytes = bytes_per_node * projected_nodes
        bench.counters["extrapolation"] = {
            "basis_docs": syn_docs,
            "basis_nodes": syn_nodes,
            "projected_nodes_at_10k_docs": round(projected_nodes, 1),
            "projected_storage_gib_at_10k_docs": round(projected_bytes / 1024**3, 3),
        }
        if syn_docs and nodes_per_doc:
            bench.add(
                metric("scale.projected_nodes_at_10k_docs", round(projected_nodes, 1),
                       note=f"按实测 {nodes_per_doc:.1f} 节点/文档线性外推（§1.4 预期 ≈13.4M）"),
                metric("scale.projected_storage_gib_at_10k_docs",
                       round(projected_bytes / 1024**3, 3), unit="GiB",
                       note="线性外推（**合成语料密度低于真实规范，故低于 §1.4 的 20–54GB 预期**）"),
            )
            bench.note(
                f"**规模未跑满（如实记录）**：本次灌入 {syn_docs} 份合成文档 / {syn_nodes} 节点，"
                f"为 §1.4 目标（{TARGET_DOCS} 文档 / ≈{TARGET_NODES:,} 节点）的 "
                f"{syn_docs / TARGET_DOCS:.2%}；按 {nodes_per_doc:.1f} 节点/文档线性外推，"
                f"10k 文档 ≈{projected_nodes / 1e6:.1f}M 节点、≈{projected_bytes / 1024**3:.1f}GiB"
            )
        bench.note(
            f"灌入吞吐 {ingest['nodes_per_s']:.0f} 节点/s（{ingest['ingest_ms'] / 1000:.1f}s / "
            f"{syn_docs} 份）。按此吞吐，10k 文档 ≈{projected_hours(ingest, nodes_per_doc)}，"
            "这是**逐节点事务**（M02「事件+实体同事务」）的必然代价；"
            "ADR-009 §3 规定批量导入走 `COPY` + 每 5k 行一批，本基准刻意不启用该旁路"
            "（in-process 与 M11 `import commit` 同一路径）"
        )
        bench.note(
            "合成语料结构为「标题 clause（段落并入 fragment）+ 表格」，与真实语料同构；"
            "解析走真实 `parse_text`（非直接造 NodeIn），故计数器是实测值"
        )
    finally:
        await db.dispose()
    return bench


def projected_hours(ingest: dict, nodes_per_doc: float) -> str:
    rate = ingest["nodes_per_s"] or 0
    if not rate:
        return "n/a"
    seconds = nodes_per_doc * TARGET_DOCS / rate
    return f"{seconds / 3600:.1f}h（{seconds / 60:.0f} 分钟）"


def test_scale_benchmark() -> None:
    """`pytest -m perf` 路径：小规模冒烟（默认 `--docs 100`），断言分区与裁剪事实。

    10k 全量**不在** pytest 路径触发（小时级）；要跑全量请显式
    `uv run python tests/perf/bench_scale.py --docs 10000`。
    """
    args = default_args(build_parser())
    if not reachable(args.dsn):
        pytest.skip(f"基准库不可达：{configure_dsn(args.dsn)}")
    bench = asyncio.run(run_bench(args))
    save(bench, args.out)
    assert bench.get("scale.partition_count").value == TARGET_PARTITION_COUNT, "分区数不是 64"
    assert bench.get("scale.explain.with_doc_id.partitions").value == 1, "带 doc_id 未裁剪到单分区"
    assert bench.counters["synthetic_docs"] >= args.docs, "合成文档数不足"
    assert bench.counters["query_set"] >= 100, "点查查询集不足 100 次"


if __name__ == "__main__":
    sys.exit(execute(build_parser(), run_bench))
