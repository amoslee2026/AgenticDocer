"""`bench_render` — 渲染耗时（ADR-010 §3.2；指标 §1.4：**单章节 <1s、整档 <3s**）。

口径（§1.4「测量口径」列）：

* **整档** = `render.render_document(doc_id)`；
* **单章节** = `render.render_section(doc_id, section_node_id)`，章节 = 该文档内
  **子树最大的 level-1/2 章节**（§1.4：章节 = level-1/2 子树）。

默认测**内容体积最大的前 2 份文档**（`--docs N` 可调，`--doc-id` 可强制指定）：
§1.4 举的「最大文档 CXL 3.59MB」与库内**实际载荷最大**的文档（PCIe 5.0）相差 3%，
两者都测可消除「选哪份」对判定的影响。**保守判据**取各文档的最坏值（`render.*.max_ms`）。

多次测量取 **中位数**为主判据、**最大值**为保守判据（§1.4 的 <1s/<3s 是上限语义）。

另记录**同轮次分量对照**（实测，不做跨方法/跨窗口相减）：

* 章节读路径：`get_section_nodes`（当前实现，O(子树)）vs `get_doc_nodes`（**历史对照**，O(全档)）；
* 资产取路径：N+1（逐 src `get_asset_path`，B-2 前实现）vs 批量 `get_asset_paths`（B-2 后）。

**口径纪律**：本基准只报**自己直接测得的**数值；引用他人/其它窗口的数值时必须标注来源与方法。

运行：

    uv run python tests/perf/bench_render.py --dsn <dsn> [--docs 2] [--compare] [--json]
"""

from __future__ import annotations

import argparse
import asyncio
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import pytest  # noqa: E402

from _common import (  # noqa: E402
    TARGET_DOCUMENT_MS,
    TARGET_SECTION_MS,
    Bench,
    add_common_args,
    bench_render_set,
    configure_dsn,
    corpus_paths,
    default_args,
    ensure_corpus,
    environment,
    execute,
    human_bytes,
    largest_section,
    metric,
    open_storage,
    reachable,
    render_table,
    save,
    scalar,
    top_docs,
)

pytestmark = pytest.mark.perf

NAME = "render"
TITLE = "渲染耗时（§1.4：单章节 <1s、整档 <3s）"

_SPEC_ID = re.compile(r"^spec_id:\s*(\S+)\s*$", re.MULTILINE)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="M04 渲染耗时基准（整档 + 单章节）")
    add_common_args(parser)
    parser.add_argument("--docs", type=int, default=2,
                        help="测量内容体积最大的前 N 份文档（默认 2：覆盖 §1.4 的 CXL 与库内最大载荷）")
    parser.add_argument("--doc-id", action="append", default=None,
                        help="强制指定文档（可重复；覆盖 --docs）")
    parser.add_argument("--document-iterations", type=int, default=5, help="整档渲染重复次数")
    parser.add_argument("--section-iterations", type=int, default=10, help="章节渲染重复次数")
    parser.add_argument("--no-ingest", action="store_true", help="库空时不自动导入语料，直接报错")
    return parser


def corpus_source_bytes() -> dict[str, tuple[str, int]]:
    """`doc_id → (源文件路径, 字节数)`（用于对照 §1.4「最大文档 CXL 3.59MB」）。"""
    mapping: dict[str, tuple[str, int]] = {}
    for path in corpus_paths():
        head = path.read_text(encoding="utf-8")[:4096]
        match = _SPEC_ID.search(head)
        if match:
            mapping[match.group(1)] = (str(path), path.stat().st_size)
    return mapping


async def select_documents(args: argparse.Namespace, storage) -> list[tuple[str, int, str]]:
    """待测文档：显式 `--doc-id` → 逐个解析；否则取内容体积最大的前 N 份。"""
    if not args.doc_id:
        return await top_docs(storage, limit=max(1, args.docs))
    selected: list[tuple[str, int, str]] = []
    for doc_id in args.doc_id:
        doc = await storage.get_doc(doc_id)  # 不存在 → NotFoundError（不静默跳过）
        content_bytes = int(await scalar(
            storage.db,
            "SELECT coalesce(sum(length(content::text)), 0) FROM nodes "
            "WHERE doc_id = :doc_id AND status = 'active'",
            doc_id=doc_id,
        ))
        selected.append((doc.doc_id, content_bytes, doc.title))
    return selected


async def run_bench(args: argparse.Namespace) -> Bench:
    storage = open_storage(args.dsn)
    db = storage.db
    bench = Bench(name=NAME, title=TITLE, environment=environment())
    try:
        ingested = await ensure_corpus(storage, allow_ingest=not args.no_ingest)
        if ingested:
            bench.note(f"库内无语料，已自动导入 {len(ingested)} 份真实语料")

        sources = corpus_source_bytes()
        documents = await select_documents(args, storage)
        reports: list[dict] = []
        for doc_id, content_bytes, title in documents:
            section_node_id, anchor, section_nodes, doc_nodes = await largest_section(storage, doc_id)
            results = await bench_render_set(
                storage,
                doc_id=doc_id,
                section_node_id=section_node_id,
                document_iterations=args.document_iterations,
                section_iterations=args.section_iterations,
            )
            source_path, source_bytes = sources.get(doc_id, ("(非语料/合成文档)", 0))
            reports.append({
                "doc_id": doc_id,
                "title": title,
                "doc_nodes": doc_nodes,
                "content_bytes": content_bytes,
                "source_path": source_path,
                "source_bytes": source_bytes,
                "section_anchor": str(anchor),
                "section_node_id": str(section_node_id),
                "section_nodes": section_nodes,
                "document": results["document"],
                "section": results["section"],
                "document_bytes": results["document_bytes"],
                "section_bytes": results["section_bytes"],
                "load_section_nodes": results["load_section_nodes"],
                "load_doc_nodes": results["load_doc_nodes"],
                "assets_n_plus_one": results["assets_n_plus_one"],
                "assets_batched": results["assets_batched"],
                "asset_refs": results["asset_refs"],
            })

        print("\n样本明细（各文档的整档 / 最大 level-1/2 章节）：")
        print(render_table(
            ["文档", "节点", "源文件", "用例", "章节节点", "产物", "中位ms", "最大ms"],
            [
                [
                    r["doc_id"],
                    r["doc_nodes"],
                    human_bytes(r["source_bytes"]) if r["source_bytes"] else "-",
                    "整档",
                    "-",
                    human_bytes(r["document_bytes"]),
                    f"{r['document']['p50_ms']:.1f}",
                    f"{r['document']['max_ms']:.1f}",
                ]
                for r in reports
            ]
            + [
                [
                    r["doc_id"],
                    r["doc_nodes"],
                    human_bytes(r["source_bytes"]) if r["source_bytes"] else "-",
                    "章节",
                    r["section_nodes"],
                    human_bytes(r["section_bytes"]),
                    f"{r['section']['p50_ms']:.1f}",
                    f"{r['section']['max_ms']:.1f}",
                ]
                for r in reports
            ],
        ))
        for report in reports:
            print(f"  · {report['doc_id']} 最大章节 = {report['section_anchor']}"
                  f"（{report['section_nodes']} 节点）；读路径中位 "
                  f"{report['load_section_nodes']['p50_ms']:.1f}ms（get_section_nodes，O(子树)），"
                  f"历史对照 get_doc_nodes {report['load_doc_nodes']['p50_ms']:.1f}ms；"
                  f"资产 {report['asset_refs']} 处：N+1 {report['assets_n_plus_one']['p50_ms']:.1f}ms vs "
                  f"批量 {report['assets_batched']['p50_ms']:.1f}ms")

        worst_doc_p50 = max(r["document"]["p50_ms"] for r in reports)
        worst_doc_max = max(r["document"]["max_ms"] for r in reports)
        worst_sec_p50 = max(r["section"]["p50_ms"] for r in reports)
        worst_sec_max = max(r["section"]["max_ms"] for r in reports)
        worst_section_load = max(r["load_section_nodes"]["p50_ms"] for r in reports)
        worst_doc_load = max(r["load_doc_nodes"]["p50_ms"] for r in reports)
        worst_assets_n1 = max(r["assets_n_plus_one"]["p50_ms"] for r in reports)
        worst_assets_batch = max(r["assets_batched"]["p50_ms"] for r in reports)
        asset_refs_max = max(r["asset_refs"] for r in reports)

        for report in reports:
            suffix = report["doc_id"]
            source = human_bytes(report["source_bytes"]) if report["source_bytes"] else "n/a"
            bench.add(
                metric(f"render.document.{suffix}.p50_ms", report["document"]["p50_ms"], unit="ms",
                       target=TARGET_DOCUMENT_MS,
                       note=f"{report['title']}（源文件 {source}，{report['doc_nodes']} 节点）"),
                metric(f"render.document.{suffix}.max_ms", report["document"]["max_ms"], unit="ms",
                       target=TARGET_DOCUMENT_MS),
                metric(f"render.section.{suffix}.p50_ms", report["section"]["p50_ms"], unit="ms",
                       target=TARGET_SECTION_MS,
                       note=f"最大 level-1/2 章节 {report['section_anchor']}"
                            f"（{report['section_nodes']} 节点）"),
                metric(f"render.section.{suffix}.max_ms", report["section"]["max_ms"], unit="ms",
                       target=TARGET_SECTION_MS),
                metric(f"render.section.{suffix}.load_section_nodes_p50_ms",
                       report["load_section_nodes"]["p50_ms"], unit="ms",
                       note="**当前实现**的章节读取（`get_section_nodes`，O(子树) 区间快路径）"),
                metric(f"render.section.{suffix}.load_doc_nodes_p50_ms",
                       report["load_doc_nodes"]["p50_ms"], unit="ms",
                       note="**历史对照**：整档读取（`get_doc_nodes`）——自 M04 PERF B-2 起 "
                            "`render_section` 已不再调用，仅作分量比照，**不代表当前章节渲染成本**"),
                metric(f"render.section.{suffix}.assets_n_plus_one_p50_ms",
                       report["assets_n_plus_one"]["p50_ms"], unit="ms",
                       note=f"**历史实现**的资产取路径（N+1：逐 src `get_asset_path`，"
                            f"{report['asset_refs']} 处引用）"),
                metric(f"render.section.{suffix}.assets_batched_p50_ms",
                       report["assets_batched"]["p50_ms"], unit="ms",
                       note=f"**当前实现**的资产取路径（`get_asset_paths` 单条 ANY，消 N+1）"),
            )
        bench.add(
            metric("render.document.p50_ms", worst_doc_p50, unit="ms", target=TARGET_DOCUMENT_MS,
                   note="**保守判据**：各文档整档中位数的最坏值"),
            metric("render.document.max_ms", worst_doc_max, unit="ms", target=TARGET_DOCUMENT_MS,
                   note="**保守判据**：各文档最慢一次的全局最坏值"),
            metric("render.document.p95_ms", max(r["document"]["p95_ms"] for r in reports),
                   unit="ms"),
            metric("render.section.p50_ms", worst_sec_p50, unit="ms", target=TARGET_SECTION_MS,
                   note="**保守判据**：各文档章节中位数的最坏值"),
            metric("render.section.max_ms", worst_sec_max, unit="ms", target=TARGET_SECTION_MS,
                   note="**保守判据**：各文档最慢一次的全局最坏值"),
            metric("render.section.p95_ms", max(r["section"]["p95_ms"] for r in reports), unit="ms"),
            metric("render.section.load_section_nodes_p50_ms",
                   max(r["load_section_nodes"]["p50_ms"] for r in reports), unit="ms",
                   note="**当前实现**章节读取中位耗时（`get_section_nodes`，O(子树)）"),
            metric("render.section.load_doc_nodes_p50_ms",
                   max(r["load_doc_nodes"]["p50_ms"] for r in reports), unit="ms",
                   note="**历史对照**整档读取中位耗时（`get_doc_nodes`；非当前章节渲染成本）"),
            metric("render.section.assets_n_plus_one_p50_ms",
                   max(r["assets_n_plus_one"]["p50_ms"] for r in reports), unit="ms",
                   note="**历史实现**资产 N+1 取路径中位耗时"),
            metric("render.section.assets_batched_p50_ms",
                   max(r["assets_batched"]["p50_ms"] for r in reports), unit="ms",
                   note="**当前实现**资产批量取路径中位耗时"),

            metric("render.docs_measured", len(reports)),
        )

        bench.counters.update({
            "docs": reports,
            "document_iterations": args.document_iterations,
            "section_iterations": args.section_iterations,
        })

        corpus_largest = max(sources.items(), key=lambda item: item[1][1]) if sources else None
        bench.notes.append(
            "本次实测文档：" + "；".join(
                f"{r['doc_id']}（载荷 {human_bytes(r['content_bytes'])}，源文件 "
                f"{human_bytes(r['source_bytes']) if r['source_bytes'] else 'n/a'}）" for r in reports
            )
            + (f"；语料中**源文件**最大者为 {corpus_largest[0]}"
               f"（{human_bytes(corpus_largest[1][1])}，即 §1.4 所述「CXL 3.59MB」）"
               if corpus_largest else "")
        )
        bench.notes.append(
            "判定取各文档的最坏值（`render.document.p50_ms` / `render.section.p50_ms`），"
            "故「载荷最大」与「源文件最大」的选择差异不影响达标结论"
        )
        bench.notes.append(
            f"**已被 M04 PERF B-2 消除**（原归因：`render_section` 走 `get_doc_nodes` 整档取数 ⇒ 章节成本 "
            f"O(全档)）：`render_section` 现走 `get_section_nodes`（O(子树) 区间快路径 + CTE 安全网）。"
            f"同轮次分量实测：`get_doc_nodes`（历史对照）{worst_doc_load:.1f}ms vs `get_section_nodes`（当前）"
            f"{worst_section_load:.1f}ms ⇒ 章节读路径不再随**文档**大小劣化"
        )
        bench.notes.append(
            f"**资产取路径 N+1 曾是最大单项成本**（B-2 前的逐 src `get_asset_path`）：本基准同轮次分量实测"
            f"（最多引用 {asset_refs_max} 处）：N+1 {worst_assets_n1:.1f}ms vs 批量 `get_asset_paths`"
            f"{worst_assets_batch:.1f}ms。与 M04Render 在其隔离库的同机同轮次 A/B"
            f"（全档读 86.5→35.3ms、资产取路径 188.8→1.6ms / 302 处引用）**方向与量级一致**"
            f"——**引用值已标注来源与方法，不与本基准数值相减**"
        )
        bench.notes.append(
            "整档渲染含图片资产导出（P4 唯一例外）；未解析到的资产引用原样保留并计入 WARN"
        )
    finally:
        await db.dispose()
    return bench


def test_render_benchmark() -> None:
    """`pytest -m perf` 路径：跑默认文档集，断言测量本身有效（有产物、指标齐全）。

    判定口径说明：目标达标与否由**报告**（`build/perf.json` 的 verdict）呈现，
    本测试只断言「测量有效」——避免把随机器负载波动的绝对值固化进 CI 断言。
    """
    args = default_args(build_parser())
    if not reachable(args.dsn):
        pytest.skip(f"基准库不可达：{configure_dsn(args.dsn)}")
    bench = asyncio.run(run_bench(args))
    save(bench, args.out)
    docs = bench.counters["docs"]
    assert docs, "未测到任何文档：语料未入库？"
    for report in docs:
        assert report["doc_nodes"] > 0, f"{report['doc_id']} 无节点"
        assert report["section_nodes"] > 0, f"{report['doc_id']} 最大章节无节点"
        assert report["document_bytes"] > 0, f"{report['doc_id']} 整档产物为空"
        assert report["section_bytes"] > 0, f"{report['doc_id']} 章节产物为空"
    for name in ("render.document.p50_ms", "render.section.p50_ms"):
        item = bench.get(name)
        assert item is not None and item.value > 0, f"指标缺失或非正：{name}"


if __name__ == "__main__":
    sys.exit(execute(build_parser(), run_bench))
