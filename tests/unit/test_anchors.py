"""M01 锚规则测试（ADR-006 + A1 修订）：规则 ①②③、219 同父同题去重、幂等、slug 边界。"""

from __future__ import annotations

import re

import pytest

import agenticdocer.model.anchors as anchors
from agenticdocer.model.anchors import (
    EMPTY_SLUG,
    SLUG_MAX_CHARS,
    SectionRef,
    anchor_base,
    assign_anchors,
    body_digest,
    make_anchor,
    normalize_body,
    section_path_str,
    slugify,
)

DOC = "SPEC-STD-CXL-3.2"
DUPLICATE_COUNT = 219  # 实测 CXL「Test Steps:」在同一个无编号父章下的出现次数


# ── 规则 ①②③ 的精确形态 ────────────────────────────────────────────────


def test_rule_1_unique_title_has_no_suffix():
    anchor = make_anchor(DOC, ["11", "2", "3"], "Timing", body_text="unique body", duplicate_title=False)

    assert anchor == f"{DOC}#11.2.3·timing"


def test_rule_2_duplicate_title_appends_body_digest_not_title_digest():
    digest = body_digest("body A")
    other = body_digest("body B")

    first = make_anchor(DOC, ["11", "2"], "Test Steps:", body_text="body A", sibling_index=0, duplicate_title=True)
    second = make_anchor(DOC, ["11", "2"], "Test Steps:", body_text="body B", sibling_index=1, duplicate_title=True)

    assert first == f"{DOC}#11.2·test-steps~{digest[:8]}"
    assert second == f"{DOC}#11.2·test-steps~{other[:8]}"
    assert first != second


def test_rule_3_identical_body_appends_sibling_index():
    digest = body_digest("same body")

    first = make_anchor(DOC, ["11", "2"], "Test Steps:", body_text="same body", sibling_index=0, duplicate_title=True, duplicate_body=True)
    second = make_anchor(DOC, ["11", "2"], "Test Steps:", body_text="same body", sibling_index=1, duplicate_title=True, duplicate_body=True)

    assert first == f"{DOC}#11.2·test-steps~{digest[:8]}~0"
    assert second == f"{DOC}#11.2·test-steps~{digest[:8]}~1"


def test_unnumbered_title_uses_slug_plus_hash():
    anchor = make_anchor(DOC, (), "Chapter A2", body_text="内容")

    assert anchor.startswith(f"{DOC}#chapter-a2~")
    assert anchor.count("~") == 1


def test_make_anchor_spec_style_keywords_equivalent_to_positional():
    digest = body_digest("b")

    positional = make_anchor(DOC, ["1", "2"], "Intro", "b", 3, duplicate_title=True)
    spec_style = make_anchor(DOC, chapter_path=["1", "2"], title="Intro", body_digest=digest, occurrence_index=3)

    assert positional == spec_style
    assert positional.endswith(f"~{digest[:8]}")


def test_make_anchor_requires_body_for_disambiguation():
    with pytest.raises(ValueError):
        make_anchor(DOC, ["1"], "T", sibling_index=1)
    with pytest.raises(ValueError):
        make_anchor(DOC, ["1"], "T", body_text="x", duplicate_body=True)


def test_anchor_base_and_section_path_str():
    assert section_path_str(["11", "2", "3"]) == "11.2.3"
    assert section_path_str("11.2.3") == "11.2.3"
    assert section_path_str(("3.1",)) == "3.1"
    assert section_path_str(None) == ""
    assert section_path_str(["", "  "]) == ""
    assert anchor_base(DOC, ("A", "1"), "Scope") == f"{DOC}#A.1·scope"
    assert anchor_base(DOC, None, "Scope") == f"{DOC}#scope"


# ── slug / 摘要边界 ─────────────────────────────────────────────────────


def test_slugify_collapses_punctuation_and_case():
    assert slugify("Test Steps:") == "test-steps"
    assert slugify("  Test   Steps  ") == "test-steps"
    assert slugify("test__steps") == "test-steps"
    assert slugify("3.1 术语与定义") == "术语与定义"
    assert slugify("ＦＵＬＬ－ＷＩＤＴＨ") == "full-width"


def test_slugify_keeps_cjk_and_accents_but_drops_symbols():
    assert slugify("读写时序（Read/Write）") == "读写时序-read-write"
    assert slugify("Café Résumé") == "café-résumé"


def test_slugify_empty_title_falls_back_to_placeholder():
    assert slugify("") == EMPTY_SLUG
    assert slugify("   ") == EMPTY_SLUG
    assert slugify("***") == EMPTY_SLUG
    assert make_anchor(DOC, ["1", "2"], "") == f"{DOC}#1.2·{EMPTY_SLUG}"


def test_slugify_long_title_truncated_but_still_distinguishable():
    base = "Wrapper Data Register " * 12  # 远超 SLUG_MAX_CHARS
    first = slugify(f"{base} A")
    second = slugify(f"{base} B")

    assert len(first) <= SLUG_MAX_CHARS + 7
    assert first != second  # 截断后追加标题哈希，避免不同标题折叠成同一 slug
    assert slugify(f"{base} A") == first  # 幂等


def test_body_digest_is_whitespace_and_width_insensitive_and_idempotent():
    assert body_digest("a  b\n\tc") == body_digest("a b c")
    assert body_digest("Full\u3000Width") == body_digest("Full Width")
    assert body_digest("同一条款") == body_digest("同一条款")
    assert body_digest("") != body_digest("x")
    assert normalize_body("  x \n y ") == "x y"
    assert len(body_digest("x")) == 64


# ── 219 同父同题：互异 + 幂等（REQ-M01-F02 验收）─────────────────────────


def _duplicate_sections(body_for: "callable[[int], str]", parent: tuple[str, ...]) -> list[SectionRef]:
    return [SectionRef(section_path=parent, title="Test Steps:", body_text=body_for(index)) for index in range(DUPLICATE_COUNT)]


def test_219_same_parent_same_title_distinct_bodies_are_distinct_and_idempotent():
    sections = _duplicate_sections(lambda index: f"Step {index}: 写 0x{index:04x} 到寄存器", parent=())

    first = assign_anchors(DOC, sections)
    second = assign_anchors(DOC, sections)

    assert len(first) == DUPLICATE_COUNT
    assert len(set(first)) == DUPLICATE_COUNT
    assert first == second  # 逐字节一致（同一源文档重复解析不漂移）
    assert all(anchor.startswith(f"{DOC}#test-steps~") for anchor in first)
    assert all(len(anchor.rsplit("~", 1)[1]) == 8 for anchor in first)


def test_219_same_parent_same_title_identical_bodies_use_sibling_index():
    sections = _duplicate_sections(lambda index: "完全相同的正文", parent=())

    first = assign_anchors(DOC, sections)
    second = assign_anchors(DOC, sections)

    assert len(set(first)) == DUPLICATE_COUNT
    assert first == second
    digest = body_digest("完全相同的正文")[:8]
    for index, anchor in enumerate(first):
        assert anchor == f"{DOC}#test-steps~{digest}~{index}"


def test_219_under_numbered_parent_are_distinct():
    sections = _duplicate_sections(lambda index: f"step body {index}", parent=("Power", "Management"))

    anchors_out = assign_anchors(DOC, sections)

    assert len(set(anchors_out)) == DUPLICATE_COUNT
    assert all(anchor.startswith(f"{DOC}#Power.Management·test-steps~") for anchor in anchors_out)


def test_anchors_are_stable_when_other_blocks_are_inserted_elsewhere():
    """稳定性：锚仅依赖文档内容与同级计数——在其他章节插入块不改变既有锚。"""
    body = lambda index: f"step {index}"
    base_sections = _duplicate_sections(body, parent=())
    extended = [SectionRef(section_path=("1",), title="Scope", body_text="scope")] + base_sections

    assert assign_anchors(DOC, extended)[1:] == assign_anchors(DOC, base_sections)


# ── 分组、同级序号与残余冲突升级 ────────────────────────────────────────


def test_unique_sections_get_plain_anchors_and_order_is_preserved():
    sections = [
        SectionRef(section_path=("1",), title="Scope", body_text="a"),
        SectionRef(section_path=("1", "1"), title="Purpose", body_text="b"),
        SectionRef(section_path=("2",), title="Terms", body_text="c"),
    ]

    assert assign_anchors(DOC, sections) == [f"{DOC}#1·scope", f"{DOC}#1.1·purpose", f"{DOC}#2·terms"]


def test_headings_differing_only_in_spelling_share_slug_so_must_not_collide():
    sections = [
        SectionRef(section_path=("1",), title="Test Steps:", body_text="first"),
        SectionRef(section_path=("1",), title="test  steps", body_text="second"),
    ]

    anchors_out = assign_anchors(DOC, sections)

    assert len(set(anchors_out)) == 2
    assert all(anchor.startswith(f"{DOC}#1·test-steps~") for anchor in anchors_out)


def test_assign_anchors_escalates_residual_collisions(monkeypatch):
    monkeypatch.setattr(anchors, "DIGEST_LEN", 1)
    buckets: dict[str, list[str]] = {}
    bodies: list[str] = []
    for index in range(256):
        candidate = f"collision body {index}"
        bucket = buckets.setdefault(body_digest(candidate)[0], [])
        bucket.append(candidate)
        if len(bucket) == 3:
            bodies = list(bucket)
            break
    assert len(bodies) == 3, "未能构造摘要前缀碰撞"

    sections = [SectionRef(section_path=("9",), title="Dup", body_text=body) for body in bodies]
    first = assign_anchors(DOC, sections)
    second = assign_anchors(DOC, sections)

    assert len(set(first)) == 3
    assert first == second
    assert sum(anchor.count("~") == 2 for anchor in first) == 1  # 仅冲突者升级到「摘要~序号」形态


def test_assign_anchors_empty_input():
    assert assign_anchors(DOC, []) == []


def test_assign_anchors_anchor_shape_matches_adr_006():
    pattern = re.compile(r"^SPEC-STD-CXL-3\.2#(?:[0-9A-Za-z.]+·)?[^#~]+(~[0-9a-f]{8}(~\d+)?)?$")
    sections = [
        SectionRef(section_path=("11", "2"), title="Timing", body_text="x"),
        SectionRef(section_path=("11", "2"), title="Timing", body_text="x"),
        SectionRef(section_path=(), title="Chapter A2", body_text="y"),
    ]

    for anchor in assign_anchors(DOC, sections):
        assert pattern.match(anchor), anchor
