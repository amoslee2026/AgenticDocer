"""M03 导入解析（§3 M03）：markdown（+frontmatter）→ 原子提议 → 审核 → 入库。

模块边界：

- :mod:`agenticdocer.importer.rules`——规则库（`rule_id` 可追溯：版本/描述/匹配器）；
- :mod:`agenticdocer.importer.frontmatter`——C5 十七字段 → `DocIn`；
- :mod:`agenticdocer.importer.parser`——解析器（源块 → 原子提议 + 未映射块清单 + 统计）；
- :mod:`agenticdocer.importer.assets_sync`——图片资产取件/校验/入库（缺失不阻断）；
- :mod:`agenticdocer.importer.cli`——`parse`/`review`/`commit`/`stats` 子命令的**业务函数**
  （CLI 装配由 M11 完成；`python -m agenticdocer.importer` 等价入口见 `__main__.py`）。
"""

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
    load_parse_result,
    load_review_state,
    parse_document,
    review_document,
    run_commit,
    run_parse,
    run_review,
    run_stats,
    save_parse_result,
    stats_report,
    work_dir_for,
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
    "check_proposals",
    "commit_document",
    "load_parse_result",
    "load_review_state",
    "parse_document",
    "review_document",
    "run_commit",
    "run_parse",
    "run_review",
    "run_stats",
    "save_parse_result",
    "stats_report",
    "work_dir_for",
]
