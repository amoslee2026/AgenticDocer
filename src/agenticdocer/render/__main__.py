"""M04 渲染 CLI：``python -m agenticdocer.render <doc_id> [--section <anchor>]``（§3 M04 / A12）。

用法::

    python -m agenticdocer.render SPEC-STD-AMBA-APB              # 整档 → <out>/SPEC-….md
    python -m agenticdocer.render SPEC-STD-AMBA-APB --sections   # 章节清单（anchor/title/level）
    python -m agenticdocer.render SPEC-STD-AMBA-APB --section 'SPEC…#3·术语'
    python -m agenticdocer.render SPEC-STD-AMBA-APB --out-dir build/rendered

呈现层约定：stdout 只承载用户可见结果（路径/清单/错误）；运行日志一律经 ``m04.*`` logger
（ADR-010 禁止业务代码 ``print``/``logging``）。退出码：0 成功、1 文档/章节不存在。

对应 M11 的 console script 名 ``agenticdocer-render``（§3 M04）；本模块是等价入口。
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from agenticdocer.observability import get_logger
from agenticdocer.store import NotFoundError, Storage

from .renderer import render_document, render_section
from .sections import find_section, list_sections

log = get_logger("m04.cli")


def _emit(text: str) -> None:
    """stdout 单行输出（CLI 呈现层；非日志）。"""
    sys.stdout.write(f"{text}\n")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m agenticdocer.render",
        description="渲染文档/章节为 Markdown（HTML 片段零改写直通，P4）",
    )
    parser.add_argument("doc_id", help="文档 ID（= 源 frontmatter 的 spec_id）")
    parser.add_argument("--section", metavar="ANCHOR", help="只渲染该锚对应的 level-1/2 章节子树")
    parser.add_argument("--sections", action="store_true", help="列出章节清单，不渲染")
    parser.add_argument("--out-dir", metavar="DIR", help="产物根目录（缺省取 RENDER_OUT_DIR）")
    return parser


async def _run(args: argparse.Namespace) -> int:
    storage = Storage()
    out_dir = Path(args.out_dir) if args.out_dir else None
    try:
        if args.sections:
            nodes = await storage.get_doc_nodes(args.doc_id)
            for section in list_sections(nodes):
                _emit(f"{'  ' * (section.level - 1)}{section.level}\t{section.anchor}\t{section.title}\t{section.node_count}")
            return 0
        if args.section:
            nodes = await storage.get_doc_nodes(args.doc_id)
            node = find_section(nodes, args.section)
            if node is None:
                _emit(f"section not found: {args.section}（用 --sections 查看可用锚）")
                return 1
            result = await render_section(args.doc_id, node.node_id, out_dir, storage=storage)
        else:
            result = await render_document(args.doc_id, out_dir, storage=storage)
    except NotFoundError as exc:
        log.error("render target not found", error_code="NOT_FOUND", detail=str(exc))
        _emit(f"not found: {exc.message}")
        return 1
    _emit(f"{result.out_path}\tassets={result.assets_exported}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI 入口：``python -m agenticdocer.render …``；返回进程退出码。"""
    args = _parser().parse_args(argv)
    return asyncio.run(_run(args))


if __name__ == "__main__":  # pragma: no cover - 进程入口
    raise SystemExit(main())
