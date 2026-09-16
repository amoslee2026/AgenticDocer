"""`bench_render` — 渲染耗时（ADR-010 §3.2；指标 §1.4：**单章节 <1s、整档 <3s**）。

口径（§1.4「测量口径」列）：

* **整档** = `render.render_document(doc_id)`，取库内**内容体积最大**的文档（语料中为
  `CXL_Specification_rev3p2_ver1p0.md`，3.59MB 级）；
* **单章节** = `render.render_section(doc_id, section_node_id)`，章节取该文档内
  **子树最大的 level-1/2 章节**（§1.4：章节 = level-1/2 子树）。

多次测量取 **中位数**为主判据、**最大值**为保守判据（§1.4 的 <1s/<3s 是上限语义）。

另记录归因数据：`render_section` 内部会整档加载节点（`get_doc_nodes`），本基准单独计时，
以便区分「章节渲染慢」与「整档取数慢」。

运行：

    uv run python tests/perf/bench_render.py --dsn <dsn> [--document-iterations 5] [--compare] [--json]
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
    largest_doc,
    largest_section,
    metric,
    open_storage,
    reachable,
    render_table,
    save,
)

pytestmark = pytest.mark.perf

NAME = "render"
TITLE = "渲染耗时（§1.4：单章节 <1s、整档 <3s）"

_SPEC_ID = re.compile(r"^spec_id:\s*(\S+)\s*$", re.MULTILINE)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="M04 渲染耗时基准（整档 + 单章节）")
    add_common_args(parser)
    parser.add_argument("--document-iterations", type=int, default=5, help="整档渲染重复次数")
    parser.add_argument("--section-iterations", type=int, default=10, help="章节渲染重复次数")
    parser.add_argument("--no-ingest", action="store_true", help="库空时不自动导入语料，直接报错")
    return parser


def corpus_source_bytes() -> dict[str, tuple[str, int]]:
    """`doc_id → (源文件相对路径, 字节数)`（供「最大文档是否即 CXL 3.59MB」的对照）。"""
    mapping: dict[str, tuple[str, int]] = {}
    for path in corpus_paths():
        head = path.read_text(encoding="utf-8")[:4096]
        match = _SPEC_ID.search(head)
        if match:
            mapping[match.group(1)] = (str(path), path.stat().st_size)
    return mapping


async def run_bench(args: argparse.Namespace) -> Bench:
    storage = open_storage(args.dsn)
    db = storage.db
    bench = Bench(name=NAME, title=TITLE, environment=environment())
    try:
        ingested = await ensure_corpus(storage, allow_ingest=not args.no_ingest)
        if ingested:
            bench.note(f"库内无语料，已自动导入 {len(ingested)} 份真实语料")

        doc_id, content_bytes, title = await largest_doc(storage)
        section_node_id, anchor, section_nodes, doc_nodes = await largest_section(storage, doc_id)
        results = await bench_render_set(
            storage,
            doc_id=doc_id,
            section_node_id=section_node_id,
            document_iterations=args.document_iterations,
            section_iterations=args.section_iterations,
        )

        document = results["document"]
        section = results["section"]
        load_nodes = results["section_load_nodes"]
        sources = corpus_source_bytes()
        source_path, source_bytes = sources.get(doc_id, ("(非语料/合成文档)", 0))

        print("\n样本明细：")
        print(render_table(
            ["用例", "对象", "节点数", "产物", "中位ms", "最大ms", "样本数"],
            [
                ["整档", doc_id, doc_nodes, human_bytes(results["document_bytes"]),
                 f"{document['p50_ms']:.1f}", f"{document['max_ms']:.1f}", document["n"]],
                ["单章节", str(anchor), section_nodes, human_bytes(results["section_bytes"]),
                 f"{section['p50_ms']:.1f}", f"{section['max_ms']:.1f}", section["n"]],
            ],
        ))
        print(f"归因：`get_doc_nodes({doc_id})` 中位 {load_nodes['p50_ms']:.1f}ms"
              f"（章节渲染会整档取数，见说明）")

        bench.counters.update({
            "doc_id": doc_id,
            "doc_title": title,
            "doc_nodes": doc_nodes,
            "doc_content_bytes": content_bytes,
            "source_path": source_path,
            "source_bytes": source_bytes,
            "rendered_bytes": results["document_bytes"],
            "section_anchor": str(anchor),
            "section_node_id": str(section_node_id),
            "section_nodes": section_nodes,
            "document_iterations": args.document_iterations,
            "section_iterations": args.section_iterations,
        })

        bench.add(
            metric("render.document.p50_ms", document["p50_ms"], unit="ms",
                   target=TARGET_DOCUMENT_MS, note=f"整档 {doc_id}（{human_bytes(content_bytes)} 内容）"),
            metric("render.document.max_ms", document["max_ms"], unit="ms",
                   target=TARGET_DOCUMENT_MS, note="保守判据：最慢一次仍须 <3s"),
            metric("render.document.p95_ms", document["p95_ms"], unit="ms"),
            metric("render.document.nodes", doc_nodes),
            metric("render.document.rendered_bytes", results["document_bytes"], unit="B"),
            metric("render.section.p50_ms", section["p50_ms"], unit="ms",
                   target=TARGET_SECTION_MS, note=f"最大 level-1/2 章节 {anchor}（{section_nodes} 节点）"),
            metric("render.section.max_ms", section["max_ms"], unit="ms",
                   target=TARGET_SECTION_MS, note="保守判据：最慢一次仍须 <1s"),
            metric("render.section.p95_ms", section["p95_ms"], unit="ms"),
            metric("render.section.nodes", section_nodes),
            metric("render.section.rendered_bytes", results["section_bytes"], unit="B"),
            metric("render.section.load_doc_nodes_p50_ms", load_nodes["p50_ms"], unit="ms",
                   note="归因：章节渲染内部整档取数（render_section 调 get_doc_nodes）"),
        )

        bench.notes.append(
            f"最大文档 = {doc_id}（库内 content 体积 {human_bytes(content_bytes)}；"
            f"源文件 {source_path}，{human_bytes(source_bytes)}）→ 与 §1.4「最大文档 CXL 3.59MB」口径一致"
            if source_bytes else
            f"最大文档 = {doc_id}（{human_bytes(content_bytes)} content；非语料文档，故无源文件对照）"
        )
        bench.notes.append(
            "**瓶颈提示（实现事实，非指标超标）**：`render_section` 内部执行 `get_doc_nodes(doc_id)`"
            "——章节渲染的取数成本是**整档**级的（O(全档节点)），且每次渲染都会重新解析并导出图片资产"
            "（`_resolve_and_export`）。故「单章节」指标随**文档**变大而劣化，而非随章节变大。"
            "若要真正 O(章节)，需 M04 增「按父链/子树查询」的 M02 读接口"
        )
        bench.notes.append(
            f"整档渲染含图片资产导出（P4 唯一例外）；未解析到的资产引用原样保留并计入 WARN"
        )
    finally:
        await db.dispose()
    return bench


def test_render_benchmark() -> None:
    """`pytest -m perf` 路径：跑默认次数，断言测量本身有效（有产物、样本齐全）。

    判定口径说明：目标值达标与否由**报告**（`build/perf.json` 的 verdict）呈现，
    本测试只断言「测量有效」——避免把随机器负载波动的绝对值固化进 CI 断言。
    """
    args = default_args(build_parser())
    if not reachable(args.dsn):
        pytest.skip(f"基准库不可达：{configure_dsn(args.dsn)}")
    bench = asyncio.run(run_bench(args))
    save(bench, args.out)
    assert bench.counters["doc_nodes"] > 0, "最大文档无节点：语料未入库？"
    assert bench.counters["section_nodes"] > 0, "最大章节无节点"
    assert bench.counters["rendered_bytes"] > 0, "整档产物为空"
    for name in ("render.document.p50_ms", "render.section.p50_ms"):
        item = bench.get(name)
        assert item is not None and item.value > 0, f"指标缺失或非正：{name}"


if __name__ == "__main__":
    sys.exit(execute(build_parser(), run_bench))
