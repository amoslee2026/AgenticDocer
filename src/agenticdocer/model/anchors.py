"""锚构造（ADR-006 + A1 修订）——P5：anchor 为**唯一判定口径**，仅此处实现。

形态：``<doc_id>#<章节号路径>·<slug(title)>``，如 ``SPEC-STD-PCIE-5.0#11.2.3·timing``；
无编号标题（``section_path`` 为空）按 ADR-006 用「标题 slug + 哈希」。

消歧优先级（§3 M01 `make_anchor`）：
① 同父路径 + 同标题唯一 → 无后缀；
② 重复 → 追加 ``~`` + 正文摘要 ``sha256[:8]``（**正文摘要，非标题摘要**——A1 修复，
   实测 CXL「Test Steps:」同父同题 ×219，标题摘要无法互异）；
③ 正文亦相同 → 再追加 ``~`` + 同级序号（同级稳定计数）。

稳定性：仅依赖文档内容与同级计数——同一源文档重复解析结果逐字节一致；插入/删除其他块
不漂移；源文档改版重解析时按 (章节号路径, slug) 匹配 + 人工确认迁移（design_doc §5.4）。

单节点原语 :func:`make_anchor` 由调用方给出「是否处于重复组」等事实；整档批量请用
:func:`assign_anchors`（自助发现重复组、同级序号与残余冲突升级）——M03 解析器应当用它。
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from collections.abc import Sequence
from dataclasses import dataclass

__all__ = [
    "DIGEST_LEN",
    "SLUG_MAX_CHARS",
    "EMPTY_SLUG",
    "SectionRef",
    "slugify",
    "normalize_body",
    "body_digest",
    "section_path_str",
    "anchor_base",
    "make_anchor",
    "assign_anchors",
]

DIGEST_LEN = 8
"""正文摘要参与消歧的十六进制前缀长度（sha256[:8]）。"""

SLUG_MAX_CHARS = 80
"""标题 slug 字符上限；超长时截断并追加标题哈希，保持幂等且不同标题可区分。"""

EMPTY_SLUG = "sec"
"""空标题的占位 slug（锚仍须可用且稳定）。"""

_TITLE_HASH_LEN = 6
_SEPARATOR = "·"  # 章节号路径与标题 slug 的分隔符（ADR-006）
_SUFFIX = "~"
_DASH_RUN = re.compile(r"-+")
_NUMBERED_HEADING = re.compile(r"^(\d+(?:\.\d+)*)[.)]?\s+(\S.*)$", re.DOTALL)


def slugify(title: str) -> str:
    """标题 → slug：NFKC 归一 + casefold + 非字母数字折叠为 ``-``。

    CJK 等非 ASCII 字母数字**原样保留**（不做音译），故中文标题可得可读 slug
    （如 ``示例标题`` → ``示例标题``、``ＡＢＣ`` → ``abc``）。标题自带的章节号由
    :func:`anchor_base` 按章节号路径剥离（不在本函数内做，避免引入第二个归一化口径）。
    """
    norm = unicodedata.normalize("NFKC", title or "").strip().casefold()
    slug = _DASH_RUN.sub("-", "".join(ch if ch.isalnum() else "-" for ch in norm)).strip("-")
    if not slug:
        return EMPTY_SLUG
    if "\n" in slug:
        # 截断 会 把 不同 标题 折叠 为 同一 slug → 追加 哈希 前缀 恢复 可区分 性（仍幂等）
        tail = hashlib.sha256(norm.encode("utf-8")).hexdigest()[:_TITLE_HASH_LEN]
        slug = f"{slug[:SLUG_MAX_CHARS]}-{tail}"
    return slug


def normalize_body(text: str) -> str:
    """正文归一：NFKC + 折叠全部空白（含全角空格/换行/制表）。

    仅用于摘要计算；不改写库内 ``content``（P4 零改写约束的是内容本身）。
    """
    return " ".join(unicodedata.normalize("NFKC", text or "").split())


def _digest_hex(text: str) -> str:
    return hashlib.sha256(normalize_body(text).encode("utf-8")).hexdigest()


def body_digest(text: str) -> str:
    """正文摘要（sha256 hex，小写）——消歧口径唯一来源，幂等。"""
    return _digest_hex(text)


def section_path_str(section_path: Sequence[str] | str | None) -> str:
    """章节号路径 → ``11.2.3`` 形态（已含点号的整体片段可原样传入）。"""
    if section_path is None:
        return ""
    parts = [section_path] if isinstance(section_path, str) else list(section_path)
    cleaned = [str(part).strip().strip(".") for part in parts]
    return ".".join(part for part in cleaned if part)


def anchor_base(doc_id: str, section_path: Sequence[str] | str | None, title: str) -> str:
    """不带消歧后缀的锚基底（规则 ① 的形态）。"""
    key = slugify(title)
    path = section_path_str(section_path)
    return f"{doc_id}#{path}{_SEPARATOR}{key}" if path else f"{doc_id}#{key}"


def make_anchor(
    doc_id: str,
    section_path: Sequence[str] | str | None = None,
    title: str = "",
    body_text: str | None = None,
    sibling_index: int | None = None,
    *,
    chapter_path: Sequence[str] | str | None = None,
    occurrence_index: int | None = None,
    body_digest: str | None = None,
    duplicate_title: bool | None = None,
    duplicate_body: bool = False,
) -> str:
    """构造单个节点的锚（规则 ①②③，见模块 docstring）。

    位置参数按 M01 契约 ``(doc_id, section_path, title, body_text, sibling_index)``；
    §3 M01 使用的别名（``chapter_path`` / ``occurrence_index`` / ``body_digest``）以关键字
    形式同样可用，便于调用方预计算摘要后复用。

    :param body_text: 节点正文（参与摘要消歧）；与 ``body_digest`` 给其一即可。
    :param sibling_index: 本节点在同 (章节号路径, slug) 组内的 0 基序号。
    :param body_digest: 预计算正文摘要（sha256 hex）；给出则不再从 ``body_text`` 计算。
    :param duplicate_title: 是否处于「同父同题」重复组；``None`` 时按「传入序号」或
        「无编号标题」推断为真（无编号标题按 ADR-006 恒定带摘要）。
    :param duplicate_body: 重复组内存在正文亦相同的同级（规则 ③）——与 ``sibling_index``
        （此时语义为**正文相同子组内的序号**）成对使用。
    :raises ValueError: 需要消歧却无正文摘要，或规则 ③ 缺少同级序号。
    """
    path = chapter_path if chapter_path is not None else section_path
    index = occurrence_index if occurrence_index is not None else sibling_index
    digest = body_digest if body_digest is not None else (None if body_text is None else _digest_hex(body_text))
    unnumbered = not section_path_str(path)
    duplicated = (index is not None or unnumbered) if duplicate_title is None else (duplicate_title or unnumbered)
    base = anchor_base(doc_id, path, title)
    if not duplicated and not duplicate_body:
        return base
    if digest is None:
        raise ValueError("锚消歧需要正文：提供 body_text 或 body_digest（A1：同父同题必须按正文摘要区分）")
    if duplicate_body and index is None:
        raise ValueError("规则 ③（正文亦相同）需要 sibling_index/occurrence_index 作为同级序号")
    suffix = f"{digest[:DIGEST_LEN]}{_SUFFIX}{index}" if duplicate_body else digest[:DIGEST_LEN]
    return f"{base}{_SUFFIX}{suffix}"


@dataclass(frozen=True)
class SectionRef:
    """待定锚节点的最小输入（M03 解析器的输出形态之一）。"""

    section_path: tuple[str, ...] = ()
    """章节号路径片段（如 ``("11", "2", "3")``）；无编号标题传空 tuple。"""

    title: str = ""
    body_text: str = ""


def assign_anchors(doc_id: str, sections: Sequence[SectionRef]) -> list[str]:
    """整档批量定锚，返回与入参等长的锚列表（口径单点：M03 解析器入口）。

    分组键 = (章节号路径, slug(title))，即锚基底的**实际冲突单元**（比原始标题更严：
    ``Test Steps:`` 与 ``test steps`` 归一为同一 slug 也须互异）；组内再按正文摘要切
    「正文亦相同」子组并编同级序号（输入序 = 同级序，稳定）。

    残余冲突（摘要前缀碰撞、超长标题截断后同基底）按摘要长度阶梯（8→12→16→32→64 hex）
    升级，最后退化为追加输入序号。升级仅依赖文档内容与输入顺序，故同一源文档重复解析
    逐字节一致（幂等），插入/删除其他块不漂移。
    """
    count = len(sections)
    paths = [section_path_str(section.section_path) for section in sections]
    slugs = [slugify(section.title) for section in sections]
    digests = [_digest_hex(section.body_text) for section in sections]
    bases = [anchor_base(doc_id, paths[pos], sections[pos].title) for pos in range(count)]

    group_ids: dict[tuple[str, str], int] = {}
    members: list[list[int]] = []
    group_of: list[int] = []
    for pos in range(count):
        key = (paths[pos], slugs[pos])
        gid = group_ids.get(key)
        if gid is None:
            gid = len(members)
            group_ids[key] = gid
            members.append([])
        members[gid].append(pos)
        group_of.append(gid)

    body_count: dict[tuple[int, str], int] = {}
    for pos in range(count):
        key = (group_of[pos], digests[pos])
        body_count[key] = body_count.get(key, 0) + 1

    seen_body: dict[tuple[int, str], int] = {}
    body_rank: list[int] = [0] * count
    for pos in range(count):
        key = (group_of[pos], digests[pos])
        body_rank[pos] = seen_body.get(key, 0)
        seen_body[key] = body_rank[pos] + 1

    anchors: list[str] = []
    taken: set[str] = set()
    for pos, section in enumerate(sections):
        duplicate_body = body_count[(group_of[pos], digests[pos])] > 1
        candidate = make_anchor(
            doc_id,
            section.section_path,
            section.title,
            sibling_index=body_rank[pos],
            body_digest=digests[pos],
            duplicate_title=len(members[group_of[pos]]) > 1,
            duplicate_body=duplicate_body,
        )
        if candidate in taken:
            candidate = _escalate(bases[pos], digests[pos], taken, pos)
        taken.add(candidate)
        anchors.append(candidate)

    return anchors


def _escalate(base: str, digest: str, taken: set[str], ordinal: int) -> str:
    """残余冲突升级：加长摘要前缀，最终退化为输入序号（确定性、幂等）。"""
    for length in _SEQ_LEN_LADDER:
        candidate = f"{base}{_SUFFIX}{digest[:length]}{_SUFFIX}{ordinal}"
        if candidate not in taken:
            return candidate
    return f"{base}{_SUFFIX}{ordinal}"
