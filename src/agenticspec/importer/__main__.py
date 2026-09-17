"""`python -m agenticspec.importer`：M03 导入器等价入口（§3 M03：A12 CLI 统一）。

CLI 装配由 M11 统一负责（Typer app / `agenticspec import`）；本入口只做参数解析与
结果输出，业务逻辑全部在 :mod:`agenticspec.importer.cli`——两处入口共用同一组业务函数。

子命令与 §3 M03 一致：

    parse  <src.md> [--doc-slug S] [--work-dir D]   → data/import_work/<slug>/proposals.json
    review <doc_slug> [--accept-confident] [--actor A]
    commit <doc_slug> [--actor A] [--no-assets] [--source-root R]
    stats  [<doc_slug> | --src <src.md>]
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from agenticspec.importer.bulk import BULK_ROWS_PER_TRANSACTION
from agenticspec.importer.cli import (
    DEFAULT_ACTOR,
    run_commit,
    run_parse,
    run_review,
    run_stats,
)

__all__ = ["build_parser", "main"]


def _emit(payload: object) -> None:
    """输出（终端 UI，非日志；日志一律走 M12 适配层）。"""
    text = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False, indent=2, default=str)
    sys.stdout.write(text + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agenticspec-import", description="M03 导入解析（parse/review/commit/stats）")
    sub = parser.add_subparsers(dest="command", required=True)

    parse_cmd = sub.add_parser("parse", help="解析 markdown → 提议（proposals.json）")
    parse_cmd.add_argument("src", type=Path)
    parse_cmd.add_argument("--doc-slug", default=None)
    parse_cmd.add_argument("--work-dir", default=None, type=Path)

    review_cmd = sub.add_parser("review", help="交互审核提议（更新 review_state.json）")
    review_cmd.add_argument("doc_slug")
    review_cmd.add_argument("--work-dir", default=None, type=Path)
    review_cmd.add_argument("--actor", default="anonymous")
    review_cmd.add_argument(
        "--accept-confident",
        action="store_true",
        help="先批量通过全部非待确认项（待确认/兜底仍需逐条处置）",
    )

    commit_cmd = sub.add_parser("commit", help="校验 + 入库 + 资产同步")
    commit_cmd.add_argument("doc_slug")
    commit_cmd.add_argument("--work-dir", default=None, type=Path)
    commit_cmd.add_argument("--actor", default=DEFAULT_ACTOR)
    commit_cmd.add_argument("--source-root", default=None, type=Path)
    commit_cmd.add_argument("--no-assets", action="store_true", help="跳过图片资产同步")
    commit_cmd.add_argument(
        "--bulk",
        action="store_true",
        help="批量路径（ADR-009 §3：COPY + 每 5k 行一事务）",
    )
    commit_cmd.add_argument(
        "--bulk-mode",
        choices=("online", "initial_load"),
        default="online",
        help="online=在线增量（默认）；initial_load=仅空文档全量装载",
    )
    commit_cmd.add_argument("--batch-size", type=int, default=BULK_ROWS_PER_TRANSACTION, help="每批行数")

    stats_cmd = sub.add_parser("stats", help="规则覆盖率/兜底率/待确认条数")
    stats_cmd.add_argument("doc_slug", nargs="?", default=None)
    stats_cmd.add_argument("--src", default=None, type=Path)
    stats_cmd.add_argument("--work-dir", default=None, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "parse":
        result = run_parse(args.src, args.doc_slug, work_dir=args.work_dir)
        _emit(result.model_dump(by_alias=True, mode="json", exclude={"proposals", "unmapped"}))
        return 0
    if args.command == "review":
        state = run_review(
            args.doc_slug,
            work_dir=args.work_dir,
            actor=args.actor,
            accept_confident=args.accept_confident,
        )
        _emit({"doc_slug": state.doc_slug, "items": len(state.items), "audit": len(state.audit)})
        return 0
    if args.command == "commit":
        report = asyncio.run(
            run_commit(
                args.doc_slug,
                work_dir=args.work_dir,
                ctx=None if args.actor == DEFAULT_ACTOR else _ctx(args.actor),
                sync_assets_too=not args.no_assets,
                source_root=args.source_root,
                bulk=args.bulk,
                bulk_mode=args.bulk_mode,
                batch_size=args.batch_size,
            )
        )
        _emit(report.model_dump(by_alias=True, mode="json", exclude={"violations"}))
        return 0
    summary = run_stats(doc_slug=args.doc_slug, src=args.src, work_dir=args.work_dir)
    _emit(summary)
    return 0


def _ctx(actor: str):
    from agenticspec.model import WriteContext

    return WriteContext(actor=actor, source="importer")


if __name__ == "__main__":  # pragma: no cover - 入口
    raise SystemExit(main())
