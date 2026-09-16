"""M03 CLI 业务函数：`parse` / `review` / `commit` / `stats`（CLI 装配由 M11 完成）。

权威来源：`architecture_specification.md` §3 M03（含 A13 提议持久化）、§9.2 CLI 工具族、
`functional_specification.md` REQ-M03-F02（审核器）/F03（入库）/F04（兜底统计）。

**工作区契约（A13）**：`IMPORT_WORK_DIR/<doc_slug>/`（默认仓库 `data/import_work/`）

- `proposals.json`——解析输出（`ParseResult` + 解析报告 + 规则集版本）；
- `review_state.json`——逐提议审核状态（`pending`/`accepted`/`rejected`/`amended`，
  含修正后的原子与审核轨迹）；
- `commit_report.json`——入库结果（写入行数、引用边数、资产同步报告、违规明细）。

**审核口径（§6.1）**：解析器确定性、无概率置信度；人工只需复核**待确认项与未映射清单**——
故 `review` 默认只走「未决 + 待确认/兜底」，`A`（批量通过）**仅作用于非待确认项**，
其余需逐条显式处置（REQ-M03-F02 验收）。

**入库口径（REQ-M03-F03）**：先经 :func:`check_proposals`（M09A 等价 schema 级校验，
用 M01 `ATOM_SCHEMAS` + jsonschema 本地实施），再经 M02 逐写（每次写入 = 事件 + 实体同事务）；
整个导入**幂等**（同锚复用既有节点、无变化不写事件），故部分失败可安全重跑。
`parent_node_id` 由 `level` + `ordinal` 在提交期重建（node_id 到提交期才产生）。
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import sys
from collections.abc import Callable, Iterable, Iterator, Sequence
from pathlib import Path
from typing import Any, Final, Literal
from uuid import UUID

import jsonschema

from agenticdocer.model import (
    AssetSyncReport,
    CommitResult,
    Model,
    NodeIn,
    ParseResult,
    Proposal,
    RawFallback,
    Violation,
    WriteContext,
    allowed_atom_types,
    get_atom_schema,
    get_doc_type_rule,
    is_atom_allowed,
)
from agenticdocer.observability import get_logger
from agenticdocer.store import Storage, ValidationError, get_storage

from .assets_sync import source_root_for, sync_assets
from .frontmatter import doc_in_from_meta
from .parser import atom_content, fallback_anchors, log_parse_stats, parse_markdown, report
from .rules import RULE_SET_VERSION

__all__ = [
    "COMMIT_REPORT_NAME",
    "DEFAULT_ACTOR",
    "DEFAULT_CTX",
    "IMPORT_WORK_DIR_ENV",
    "PROPOSALS_NAME",
    "REVIEW_STATE_NAME",
    "CommitReport",
    "ReviewItem",
    "ReviewState",
    "atom_content",
    "check_proposals",
    "commit_document",
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

log = get_logger("m03.cli")

PROPOSALS_NAME: Final = "proposals.json"
REVIEW_STATE_NAME: Final = "review_state.json"
COMMIT_REPORT_NAME: Final = "commit_report.json"
IMPORT_WORK_DIR_ENV: Final = "IMPORT_WORK_DIR"
_REPO_ROOT: Final = Path(__file__).resolve().parents[3]

IMPORTER_SOURCE: Final = "importer"
DEFAULT_ACTOR: Final = "importer"

DEFAULT_CTX: Final = WriteContext(actor=DEFAULT_ACTOR, source="importer")
"""导入写入上下文（§6 A3：`source` 由凭据/路径判定，M03 导入器恒为 `importer`）。"""

Decision = Literal["pending", "accepted", "rejected", "amended"]


# ── 持久化类型（A13；工作区文件专用，非 §3.0 领域类型）────────────────────


class ReviewItem(Model):
    """单个提议的审核状态（A13：`pending`/`accepted`/`rejected`/`amended(含修正 JSON)`）。"""

    proposal_id: str
    rule_id: str
    confident: bool
    source_lines: tuple[int, int]
    decision: Decision = "pending"
    amended_atom: dict[str, Any] | None = None
    reviewed_at: str | None = None


class ReviewState(Model):
    """`review_state.json`：逐提议审核状态 + 审核轨迹（REQ-M03-F02「审核动作落审计输出」）。"""

    doc_slug: str
    doc_id: str
    rule_set_version: str
    updated_at: str
    items: dict[str, ReviewItem]
    audit: list[dict[str, Any]] = []


class CommitReport(Model):
    """`commit_report.json`：入库结果 + 资产同步 + 违规明细。"""

    doc_slug: str
    doc_id: str
    doc_type: str
    doc_status: str
    accepted: int
    rejected: int
    pending: int
    commit: CommitResult
    assets: AssetSyncReport | None
    violations: list[Violation] = []
    work_dir: str


def _now() -> str:
    return _dt.datetime.now(_dt.UTC).replace(microsecond=0).isoformat()


def work_dir_for(doc_slug: str, work_dir: Path | str | None = None) -> Path:
    """导入工作区目录（`IMPORT_WORK_DIR/<doc_slug>/`，§5 环境变量）。"""
    root = Path(work_dir) if work_dir is not None else Path(os.environ.get(IMPORT_WORK_DIR_ENV, _REPO_ROOT / "data" / "import_work"))
    return root / doc_slug


def save_parse_result(
    result: ParseResult,
    *,
    doc_slug: str | None = None,
    work_dir: Path | str | None = None,
) -> Path:
    """落 `proposals.json`（`ParseResult` + 解析报告 + 规则集版本）；返回文件路径。"""
    slug = doc_slug or str(result.doc_meta.get("doc_slug") or "")
    if not slug:
        raise ValidationError("doc_slug 缺失：无法定位导入工作区", entity="doc")
    directory = work_dir_for(slug, work_dir)
    directory.mkdir(parents=True, exist_ok=True)
    payload = {
        "doc_slug": slug,
        "rule_set_version": RULE_SET_VERSION,
        "report": report(result),
        "result": result.model_dump(by_alias=True, mode="json"),
    }
    path = directory / PROPOSALS_NAME
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info(
        "import parse persisted",
        doc_slug=slug,
        doc_id=result.doc_meta.get("doc_id"),
        proposals=len(result.proposals),
        path=str(path),
    )
    return path


def load_parse_result(doc_slug: str, *, work_dir: Path | str | None = None) -> ParseResult:
    """读 `proposals.json` → :class:`ParseResult`（`commit`/`stats` 的输入）。"""
    path = work_dir_for(doc_slug, work_dir) / PROPOSALS_NAME
    if not path.is_file():
        raise ValidationError(f"提议文件不存在：{path}（先跑 import parse）", entity="doc", entity_id=doc_slug)
    payload = json.loads(path.read_text(encoding="utf-8"))
    return ParseResult.model_validate(payload["result"])


def save_review_state(state: ReviewState, *, work_dir: Path | str | None = None) -> Path:
    """落 `review_state.json`；返回文件路径。"""
    directory = work_dir_for(state.doc_slug, work_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / REVIEW_STATE_NAME
    path.write_text(
        json.dumps(state.model_dump(by_alias=True, mode="json"), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    log.info("import review persisted", doc_slug=state.doc_slug, path=str(path))
    return path


def load_review_state(doc_slug: str, *, work_dir: Path | str | None = None) -> ReviewState:
    """读 `review_state.json`；不存在时按 `ParseResult` 初始化（全部 `pending`）。"""
    directory = work_dir_for(doc_slug, work_dir)
    path = directory / REVIEW_STATE_NAME
    if path.is_file():
        return ReviewState.model_validate(json.loads(path.read_text(encoding="utf-8")))
    result = load_parse_result(doc_slug, work_dir=work_dir)
    state = ReviewState(
        doc_slug=doc_slug,
        doc_id=str(result.doc_meta.get("doc_id") or ""),
        rule_set_version=RULE_SET_VERSION,
        updated_at=_now(),
        items={
            proposal.proposal_id: ReviewItem(
                proposal_id=proposal.proposal_id,
                rule_id=proposal.rule_id,
                confident=proposal.confident,
                source_lines=proposal.source_lines,
            )
            for proposal in result.proposals
        },
        audit=[],
    )
    save_review_state(state, work_dir=work_dir)
    return state


# ── parse ────────────────────────────────────────────────────────────────


def run_parse(
    src: Path | str,
    doc_slug: str | None = None,
    *,
    work_dir: Path | str | None = None,
) -> ParseResult:
    """`parse <src.md> [--doc-slug S]`：解析 → 落 `proposals.json` + 初始化 `review_state.json`。"""
    result = parse_markdown(src, doc_slug)
    slug = doc_slug or Path(src).stem
    save_parse_result(result, doc_slug=slug, work_dir=work_dir)
    load_review_state(slug, work_dir=work_dir)  # 初始化（已存在则原样保留）
    log_parse_stats(result, doc_slug=slug)
    return result


# ── review ───────────────────────────────────────────────────────────────


def _preview(proposal: Proposal, width: int = 160) -> str:
    atom = proposal.atom
    if isinstance(atom, RawFallback):
        body = atom.text
        kind = f"fallback:{atom.atom_type}({atom.format})"
    else:
        body = str(atom.content.get("text", ""))
        kind = f"{atom.atom_type}({atom.format})"
    flat = " ".join(body.split())
    return f"{kind}  {flat[:width]}{'…' if len(flat) > width else ''}"


def _stdio() -> tuple[Callable[[str], None], Callable[[str], str]]:
    """交互默认通道（终端 UI，非日志；禁止 print/`logging` 的纪律由本函数收敛）。"""

    def write(line: str) -> None:
        sys.stdout.write(line + "\n")
        sys.stdout.flush()

    def ask(prompt: str) -> str:
        sys.stdout.write(prompt)
        sys.stdout.flush()
        return sys.stdin.readline().strip()

    return write, ask


def _audit(state: ReviewState, action: str, actor: str, **fields: Any) -> None:
    state.audit.append({"at": _now(), "action": action, "actor": actor, **fields})


def run_review(
    doc_slug: str,
    *,
    work_dir: Path | str | None = None,
    answers: Iterable[str] | None = None,
    out: Callable[[str], None] | None = None,
    ask: Callable[[str], str] | None = None,
    actor: str = "anonymous",
    accept_confident: bool = False,
    pending_only: bool = True,
) -> ReviewState:
    """`review <doc_slug>`：逐条审核提议 → 更新 `review_state.json`（REQ-M03-F02）。

    命令：`a` 通过、`r` 拒绝、`e` 修正（下一行给 JSON 补丁）、`s` 跳过、`u` 查看未映射清单、
    `A` 批量通过**非待确认**项、`q` 结束。`accept_confident=True` 时先自动通过全部
    非待确认项（批量通过不触及待确认/兜底件，见 §6.1）。
    """
    if out is None or ask is None:
        default_out, default_ask = _stdio()
        out = out or default_out
        ask = ask or default_ask
    stream: Iterator[str] = iter(answers) if answers is not None else iter(())
    interactive = answers is None

    def next_answer(prompt: str) -> str:
        if interactive:
            return ask(prompt)
        try:
            return next(stream)
        except StopIteration:
            return "q"

    result = load_parse_result(doc_slug, work_dir=work_dir)
    state = load_review_state(doc_slug, work_dir=work_dir)
    unmapped = {item.source_lines: item for item in result.unmapped}

    if accept_confident:
        auto = 0
        for item in state.items.values():
            if item.decision == "pending" and item.confident:
                item.decision, item.reviewed_at = "accepted", _now()
                auto += 1
        if auto:
            _audit(state, "batch_accept", actor, count=auto, scope="confident")

    queue = [
        proposal
        for proposal in result.proposals
        if state.items[proposal.proposal_id].decision == "pending"
        and (not pending_only or not proposal.confident)
    ]
    out(f"[review] {doc_slug}：待审 {len(queue)} 条（待确认/兜底）；共 {len(result.proposals)} 条提议")
    for index, proposal in enumerate(queue, 1):
        item = state.items[proposal.proposal_id]
        flag = "" if proposal.confident else "  ⚠待确认"
        out(f"[{index}/{len(queue)}] {proposal.proposal_id} {proposal.rule_id}{flag} 行 {proposal.source_lines[0]}-{proposal.source_lines[1]}")
        out(f"      {_preview(proposal)}")
        while True:
            answer = next_answer("  [a]通过 [r]拒绝 [e]修正 [s]跳过 [u]未映射 [A]批量通过非待确认 [q]结束 > ").strip()
            if answer in ("a", "r", "s", "q", "u", "A"):
                break
            if answer == "e":
                patch = next_answer("  修正 JSON（对 content 打补丁）> ")
                try:
                    parsed = json.loads(patch)
                except json.JSONDecodeError as exc:
                    out(f"  ! JSON 非法：{exc}")
                    continue
                if not isinstance(parsed, dict) or isinstance(proposal.atom, RawFallback):
                    out("  ! 仅结构化原子支持修正（兜底件请改用拒绝/接受）")
                    continue
                proposal.atom.content.update(parsed)
                item.amended_atom = dict(parsed)
                item.decision, item.reviewed_at = "amended", _now()
                _audit(state, "amend", actor, proposal_id=proposal.proposal_id, patch=parsed)
                break
            out("  ? 未识别的命令")
        if answer == "a":
            item.decision, item.reviewed_at = "accepted", _now()
            _audit(state, "accept", actor, proposal_id=proposal.proposal_id)
        elif answer == "r":
            item.decision, item.reviewed_at = "rejected", _now()
            _audit(state, "reject", actor, proposal_id=proposal.proposal_id)
        elif answer == "s":
            _audit(state, "skip", actor, proposal_id=proposal.proposal_id)
        elif answer == "u":
            out(f"[未映射清单] {len(unmapped)} 条（不丢弃，随 commit 落库为兜底原子）")
            for entry in list(unmapped.values())[:20]:
                out(f"    - 行 {entry.source_lines[0]}-{entry.source_lines[1]}：{entry.reason}")
            _audit(state, "view_unmapped", actor, count=len(unmapped))
        elif answer == "A":
            auto = 0
            for candidate in result.proposals:
                entry = state.items[candidate.proposal_id]
                if entry.decision == "pending" and entry.confident:
                    entry.decision, entry.reviewed_at = "accepted", _now()
                    auto += 1
            _audit(state, "batch_accept", actor, count=auto, scope="confident")
            out(f"  [批量通过非待确认项] {auto} 条")
        elif answer == "q":
            _audit(state, "quit", actor, at_proposal=proposal.proposal_id)
            break

    state.updated_at = _now()
    save_review_state(state, work_dir=work_dir)
    summary = decision_summary(state)
    log.info(
        "import review done",
        doc_slug=doc_slug,
        actor=actor,
        **summary,
    )
    out(f"[review] 完成：{summary}")
    return state


def decision_summary(state: ReviewState) -> dict[str, int]:
    """审核状态计数（`pending`/`accepted`/`rejected`/`amended`）。"""
    summary = {"pending": 0, "accepted": 0, "rejected": 0, "amended": 0}
    for item in state.items.values():
        summary[item.decision] += 1
    return summary


# ── 校验（M09A 等价：schema 级）──────────────────────────────────────────


def selected_proposals(result: ParseResult, accepted: Iterable[str] | None = None) -> list[Proposal]:
    """审核结论筛选：`accepted=None` → 全部提议；否则只取给定 `proposal_id` 集合。"""
    if accepted is None:
        return list(result.proposals)
    wanted = set(accepted)
    return [proposal for proposal in result.proposals if proposal.proposal_id in wanted]


_VALIDATORS: dict[str, jsonschema.Draft202012Validator] = {}
"""`atom_type` → 已编译的 schema validator（缓存：整档 1 万条提议时避免重复编译）。"""


def _validator(atom_type: str) -> jsonschema.Draft202012Validator:
    validator = _VALIDATORS.get(atom_type)
    if validator is None:
        validator = _VALIDATORS[atom_type] = jsonschema.Draft202012Validator(get_atom_schema(atom_type))
    return validator


def check_proposals(
    result: ParseResult,
    *,
    accepted: Iterable[str] | None = None,
) -> list[Violation]:
    """提议级校验（REQ-M03-F03：非法提议被拒且报出违规明细）。

    判据（M09A schema 级 + M03 结构完整性）：
    ① 原子类型已注册且被该 `doc_type` 放行（REQ-M01-F03）；
    ② `content` 满足 M01 `ATOM_SCHEMAS`（jsonschema draft 2020-12，额外字段拒绝）；
    ③ `content.text` 非空（A10：FTS 生成列的唯一来源）；
    ④ 锚非空、同文档内唯一（DB 约束 `UNIQUE (doc_id, anchor)` 的前置校验）；
    ⑤ 兜底提议必须有解析期定下的锚（`doc_meta.fallback`）；
    ⑥ `doc_type` 组合规则的必备原子（`clause`）在场。
    """
    doc_type = str(result.doc_meta.get("doc_type") or "")
    proposals = selected_proposals(result, accepted)
    violations: list[Violation] = []
    fallbacks = fallback_anchors(result)
    seen_anchors: dict[str, str] = {}
    clause_seen = False
    for proposal in proposals:
        atom = proposal.atom
        if isinstance(atom, RawFallback):
            if not atom.text.strip():
                violations.append(
                    Violation(
                        rule_id="M03.fallback.empty",
                        path=proposal.proposal_id,
                        message="兜底原子文本为空（零静默丢弃要求原样保留源块）",
                        fix_hint="检查块切分是否产生空块",
                    )
                )
            if proposal.proposal_id not in fallbacks:
                violations.append(
                    Violation(
                        rule_id="M03.fallback.anchor",
                        path=proposal.proposal_id,
                        message="兜底提议缺锚（doc_meta.fallback 未登记）",
                        fix_hint="重新解析（F01/F02/F03 的锚由解析期单点确定）",
                    )
                )
            continue
        if not is_atom_allowed(doc_type, atom.atom_type):
            violations.append(
                Violation(
                    rule_id="M01.doc_type.atom",
                    path=f"{atom.anchor}",
                    message=f"doc_type={doc_type!r} 不允许原子 {atom.atom_type!r}（允许：{list(allowed_atom_types(doc_type))}）",
                    fix_hint="调整规则映射或扩展 doc_type 组合规则（REQ-M01-F03）",
                )
            )
            continue
        if atom.atom_type.split(".", 1)[0] == "clause":
            clause_seen = True
        for error in sorted(_validator(atom.atom_type).iter_errors(atom.content), key=lambda err: list(err.path)):
            location = "/".join(str(part) for part in error.path) or "(root)"
            violations.append(
                Violation(
                    rule_id="M09A.atom.schema",
                    path=f"{atom.anchor}#{location}",
                    message=error.message,
                    fix_hint=f"对照 ATOM_SCHEMAS[{atom.atom_type!r}] 修正 content",
                )
            )
        text = atom.content.get("text")
        if not isinstance(text, str) or not text.strip():
            violations.append(
                Violation(
                    rule_id="A10.content.text",
                    path=str(atom.anchor),
                    message="content.text 缺失或为空（FTS 生成列依赖）",
                    fix_hint="由 M01 derive_text 生成后再写入",
                )
            )
        if not atom.anchor.strip():
            violations.append(
                Violation(rule_id="M03.anchor.empty", path=proposal.proposal_id, message="锚为空", fix_hint=None)
            )
        elif atom.anchor in seen_anchors:
            violations.append(
                Violation(
                    rule_id="M03.anchor.duplicate",
                    path=str(atom.anchor),
                    message=f"锚重复（另一提议 {seen_anchors[atom.anchor]}；DB 约束 UNIQUE(doc_id, anchor)）",
                    fix_hint="锚消歧由 model.anchors.assign_anchors 统一处理（P5）",
                )
            )
        else:
            seen_anchors[atom.anchor] = proposal.proposal_id
    required = get_doc_type_rule(doc_type).required_atom_types if doc_type else ()
    if "clause" in required and not clause_seen:
        violations.append(
            Violation(
                rule_id="M01.doc_type.required",
                path=str(result.doc_meta.get("doc_id")),
                message="缺少必备原子 clause（doc_type 组合规则）",
                fix_hint="检查标题规则是否命中（R01.heading.clause）",
            )
        )
    return violations


# ── commit ───────────────────────────────────────────────────────────────


def _node_spec(
    proposal: Proposal,
    fallbacks: dict[str, str],
) -> tuple[str, int | None, str, str, dict[str, Any]]:
    """提议 → `(anchor, level, atom_type, format, content)`。"""
    atom = proposal.atom
    if isinstance(atom, RawFallback):
        anchor = fallbacks.get(proposal.proposal_id, "")
        return anchor, None, atom.atom_type, atom.format, atom_content("note", fragment=atom.text)
    return atom.anchor, atom.level, atom.atom_type, atom.format, atom.content


async def commit_document(
    result: ParseResult,
    ctx: WriteContext | None = None,
    *,
    storage: Storage | None = None,
    accepted: Iterable[str] | None = None,
) -> CommitResult:
    """审核通过的提议 → 校验 → 事务写入 `docs`/`nodes`/`refs`（REQ-M03-F03）。

    - 校验不通过 → `ValidationError`（带违规明细，调用方经 §6 映射为 422）；
    - 幂等：同锚复用既有节点（`node_id` 复用 → M02 的「无变化不写事件」生效），
      引用边按 `(src, dst_doc, dst_node, kind)` 去重，故重跑不产生重复节点/边；
    - `parent_node_id` 由 `(level, ordinal)` 栈重建（node_id 提交期才产生）；
    - 每次节点写入由 M02 保证「事件 + 实体同事务」；整档导入的原子性由**幂等重跑**兜底。
    """
    context = ctx or DEFAULT_CTX
    if context.source != "importer":
        log.warn("unexpected write source", source=context.source, actor=context.actor)
    violations = check_proposals(result, accepted=accepted)
    if violations:
        raise ValidationError(
            "提议未通过 schema 级校验：" + "；".join(f"{item.path}: {item.message}" for item in violations[:5]),
            entity="node",
            entity_id=str(result.doc_meta.get("doc_id")),
        )
    store = storage or get_storage()
    doc_meta = result.doc_meta
    doc = await store.upsert_doc(doc_in_from_meta(doc_meta), None, context)
    status = str(doc_meta.get("doc_status") or "draft")
    if doc.status != status:
        doc = await store.update_doc_status(doc.doc_id, status, doc.version, context)  # type: ignore[arg-type]
    existing = {node.anchor: node.node_id for node in await store.get_doc_nodes(doc.doc_id)}
    selected = selected_proposals(result, accepted)
    fallbacks = fallback_anchors(result)
    nodes_created = 0
    stack: list[tuple[int, UUID]] = []
    committed: list[tuple[Proposal, UUID]] = []
    for proposal in selected:
        anchor, level, atom_type, fmt, content = _node_spec(proposal, fallbacks)
        if not anchor:
            raise ValidationError(f"提议 {proposal.proposal_id} 无锚（无法入库）", entity="node")
        if level is not None:
            while stack and stack[-1][0] >= level:
                stack.pop()
        parent = stack[-1][1] if stack else None
        node_in = NodeIn(
            node_id=existing.get(anchor),
            doc_id=doc.doc_id,
            atom_type=atom_type,
            format=fmt,  # type: ignore[arg-type]
            ordinal=proposal.source_lines[0],  # 文档序：源行号即稳定 ordinal（重解析不漂移）
            parent_node_id=parent,
            level=level,
            anchor=anchor,
            content=content,
        )
        node = await store.upsert_node(node_in, None, context)
        if anchor not in existing:
            nodes_created += 1
        existing[anchor] = node.node_id
        if level is not None:
            stack.append((level, node.node_id))
        committed.append((proposal, node.node_id))

    refs_created = 0
    for proposal, node_id in committed:
        atom = proposal.atom
        if isinstance(atom, RawFallback) or atom.atom_type != "cross_ref":
            continue
        target_anchor = atom.content.get("target_anchor")
        kind = str(atom.content.get("ref_kind") or "see_also")
        dst_node = existing.get(str(target_anchor)) if target_anchor else None
        known = {
            (ref.dst_doc_id, ref.dst_node_id, ref.kind)
            for ref in await store.list_refs(node_id)
        }
        if (doc.doc_id, dst_node, kind) in known:
            continue
        await store.add_ref(node_id, doc.doc_id, dst_node, kind, context)  # type: ignore[arg-type]
        refs_created += 1

    log.info(
        "import committed",
        doc_id=doc.doc_id,
        doc_slug=doc_meta.get("doc_slug"),
        doc_status=doc.status,
        nodes_created=nodes_created,
        nodes_total=len(committed),
        refs_created=refs_created,
        accepted=len(selected),
        proposals=len(result.proposals),
    )
    return CommitResult(
        doc_id=doc.doc_id,
        nodes_created=nodes_created,
        refs_created=refs_created,
        stats=result.stats,
    )


async def run_commit(
    doc_slug: str,
    *,
    work_dir: Path | str | None = None,
    ctx: WriteContext | None = None,
    storage: Storage | None = None,
    sync_assets_too: bool = True,
    source_root: Path | str | None = None,
) -> CommitReport:
    """`commit <doc_slug>`：读提议 + 审核结论 → 校验 → 入库 → 资产同步 → 落 `commit_report.json`。"""
    context = ctx or DEFAULT_CTX
    result = load_parse_result(doc_slug, work_dir=work_dir)
    state = load_review_state(doc_slug, work_dir=work_dir)
    accepted = {item.proposal_id for item in state.items.values() if item.decision in ("accepted", "amended")}
    rejected = sum(1 for item in state.items.values() if item.decision == "rejected")
    summary = decision_summary(state)
    if summary["pending"]:
        log.warn("import commit with pending items", doc_slug=doc_slug, pending=summary["pending"])
    store = storage or get_storage()
    with log.timer("commit_import", module="m03.cli", doc_slug=doc_slug):
        commit = await commit_document(result, context, storage=store, accepted=accepted)
        assets: AssetSyncReport | None = None
        if sync_assets_too:
            refs = result.doc_meta.get("asset_refs", {}) or {}
            source = Path(source_root) if source_root is not None else _source_root_of(result)
            assets = await sync_assets(list(refs.get("refs") or []), source, store)
    violations = check_proposals(result, accepted=accepted)
    report_path = work_dir_for(doc_slug, work_dir) / COMMIT_REPORT_NAME
    payload = CommitReport(
        doc_slug=doc_slug,
        doc_id=commit.doc_id,
        doc_type=str(result.doc_meta.get("doc_type") or ""),
        doc_status=str(result.doc_meta.get("doc_status") or "draft"),
        accepted=len(accepted),
        rejected=rejected,
        pending=summary["pending"],
        commit=commit,
        assets=assets,
        violations=violations,
        work_dir=str(report_path.parent),
    )
    report_path.write_text(
        json.dumps(payload.model_dump(by_alias=True, mode="json"), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return payload


def _source_root_of(result: ParseResult) -> Path:
    """资产取件根：源 md 所在目录（`IMPORT_SOURCE_ROOT` 可覆盖，见 assets_sync）。"""
    return source_root_for(result.doc_meta.get("source_path"))

# ── stats ────────────────────────────────────────────────────────────────


def stats_report(
    *,
    src: Path | str | None = None,
    doc_slug: str | None = None,
    work_dir: Path | str | None = None,
) -> dict[str, Any]:
    """规则覆盖率/兜底率/待确认条数报告（`stats <doc_slug>`；也可直接给源文件现算）。"""
    if src is not None:
        result = parse_markdown(src, doc_slug)
        summary = report(result)
        log_parse_stats(result, doc_slug=doc_slug or Path(src).stem)
        return summary
    if not doc_slug:
        raise ValidationError("stats 需要 src 或 doc_slug 之一", entity="doc")
    path = work_dir_for(doc_slug, work_dir) / PROPOSALS_NAME
    if path.is_file():
        stored = json.loads(path.read_text(encoding="utf-8"))
        summary = stored.get("report")
        if isinstance(summary, dict):
            summary = {**summary, "rule_set_version": stored.get("rule_set_version"), "source": str(path)}
            log.info("import stats read", doc_slug=doc_slug, coverage=summary.get("coverage"), path=str(path))
            return summary
    result = load_parse_result(doc_slug, work_dir=work_dir)
    log_parse_stats(result, doc_slug=doc_slug)
    return report(result)


def run_stats(
    *,
    src: Path | str | None = None,
    doc_slug: str | None = None,
    work_dir: Path | str | None = None,
) -> dict[str, Any]:
    """`stats` 子命令业务函数（alias of :func:`stats_report`）。"""
    return stats_report(src=src, doc_slug=doc_slug, work_dir=work_dir)
