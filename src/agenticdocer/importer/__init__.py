"""M03 导入解析（§3 M03）：markdown（+frontmatter）→ 原子提议 → 审核 → 入库。

模块边界：

- :mod:`agenticdocer.importer.rules`——规则库（`rule_id` 可追溯：版本/描述/匹配器）；
- :mod:`agenticdocer.importer.frontmatter`——C5 十七字段 → `DocIn`（`spec_type` 归一在此）；
- :mod:`agenticdocer.importer.doc_type_map`——映射表 §2 的机器可读形式（idea.md 30+ 类型
  → 5 个 `doc_type` + `meta.doc_subtype`）；
- :mod:`agenticdocer.importer.parser`——解析器（源块 → 原子提议 + 未映射块清单 + 统计）；
- :mod:`agenticdocer.importer.assets_sync`——图片资产取件/校验/入库（缺失不阻断）；
- :mod:`agenticdocer.importer.vplan`——vPlan/UCIS XML → `table.coverage_matrix` 原子（§4）；
- :mod:`agenticdocer.importer.cli`——`parse`/`review`/`commit`/`stats` 子命令的**业务函数**
  （CLI 装配由 M11 完成；`python -m agenticdocer.importer` 等价入口见 `__main__.py`）。
"""

from agenticdocer.importer.bulk import BULK_ROWS_PER_TRANSACTION, bulk_insert_nodes
from agenticdocer.importer.assets_sync import (
    AssetRef,
    collect_refs,
    fetch_assets,
    iter_refs,
    ref_counts,
    sync_assets,
)
from agenticdocer.importer.cli import (
    DEFAULT_CTX,
    COMMIT_REPORT_NAME,
    IMPORTER_SOURCE,
    PROPOSALS_NAME,
    REVIEW_STATE_NAME,
    check_proposals,
    commit_document,
    commit_document_bulk,
    decision_summary,
    load_parse_result,
    load_review_state,
    run_commit,
    run_parse,
    run_review,
    run_stats,
    save_parse_result,
    save_review_state,
    selected_proposals,
    stats_report,
    work_dir_for,
)
from agenticdocer.importer.doc_type_map import (
    IDEA_DOC_TYPES,
    PRODUCT_SUBTYPES,
    SPEC_ROWS,
    UnknownDocTypeError,
    resolve_doc_type,
    subtypes_for,
)
from agenticdocer.importer.frontmatter import (
    Frontmatter,
    doc_in_from_meta,
    parse_frontmatter,
    split_frontmatter,
)
from agenticdocer.importer.parser import (
    PROPOSAL_ID_FORMAT,
    Section,
    atom_type_counts,
    build_sections,
    classify,
    coverage,
    fallback_anchors,
    log_parse_stats,
    parse,
    parse_markdown,
    parse_text,
    report,
    rule_counts,
    scan_blocks,
)
from agenticdocer.importer.rules import (
    RULES,
    RULES_BY_KIND,
    RULE_SET_VERSION,
    Block,
    Rule,
)

__all__ = [
    # rules
    "RULES",
    "RULES_BY_KIND",
    "RULE_SET_VERSION",
    "Block",
    "Rule",
    # frontmatter
    "Frontmatter",
    "doc_in_from_meta",
    "parse_frontmatter",
    "split_frontmatter",
    # parser
    "PROPOSAL_ID_FORMAT",
    "Section",
    "atom_type_counts",
    "build_sections",
    "classify",
    "coverage",
    "fallback_anchors",
    "log_parse_stats",
    "parse",
    "parse_markdown",
    "parse_text",
    "report",
    "rule_counts",
    "scan_blocks",
    # bulk（ADR-009 §3）
    "BULK_ROWS_PER_TRANSACTION",
    "bulk_insert_nodes",
    # assets
    "AssetRef",
    "collect_refs",
    "fetch_assets",
    "iter_refs",
    "ref_counts",
    "sync_assets",
    # cli（业务函数）
    "COMMIT_REPORT_NAME",
    "DEFAULT_CTX",
    "IMPORTER_SOURCE",
    "PROPOSALS_NAME",
    "REVIEW_STATE_NAME",
    "atom_content",
    "check_proposals",
    "commit_document",
    "commit_document_bulk",
    "decision_summary",
    "load_parse_result",
    "load_review_state",
    "run_commit",
    "run_parse",
    "run_review",
    "run_stats",
    "save_parse_result",
    "save_review_state",
    "selected_proposals",
    "stats_report",
    "work_dir_for",
]
