"""`scripts/upgrade_frontmatter.py` 的契约守卫（方案 C 语料接入，2026-09-17）。

三条不可回退的契约：
① 脚本镜像的 doc_type 必填 meta 与 `model/doc_types.py` **单源一致**（防漂移：改规则表须同改脚本）；
② 已有 frontmatter 的语料**零改写**——只追加缺失字段，字段齐全恒 `[skip]`（既有 7 份语料的安全网）；
③ 无 frontmatter 的语料**新建** frontmatter，正文逐字节保留，且新建结果能被 M03 `parse_frontmatter` 接受。
另覆盖：非 markdown 语料 / 许可文件跳过；未登记文件报错而不猜测（且不改写该文件）；批量失败隔离。
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys

import pytest
import yaml

from agenticdocer.importer import parse_frontmatter
from agenticdocer.model import DOC_TYPES, DOC_TYPE_RULES, missing_required_meta

ROOT = pathlib.Path(__file__).resolve().parents[2]


_PROVENANCE = {  # 与脚本 `_DOWNLOADED` 同形：下载语料共用的溯源四项
    "converted_by": '"download（原样下载，未转换）"',
    "converted_at": "2026-09-17",
    "reviewed_by": '"lxx(下载授权)"',
    "reviewed_at": "2026-09-17",
}


def _load_script():
    """按文件路径载入脚本（`scripts/` 非包）——返回模块对象。"""
    path = ROOT / "scripts" / "upgrade_frontmatter.py"
    spec = importlib.util.spec_from_file_location("upgrade_frontmatter_under_test", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


uf = _load_script()

BODY = "# Demo FMEA\n\n| failure mode | effect | RPN |\n|---|---|---|\n| stuck-high | no reset | 12 |\n"

SAFETY_ENTRY = {
    "spec_id": "SPEC-SAFE-DEMO",
    "spec_org": "demo/org",
    "spec_revision": "IEC-60812",
    "spec_type": "safety",
    "source": "https://example.invalid/demo-FMEA.md",
    **_PROVENANCE,
    "standard_ref": '"IEC 60812"',
    "audit_trail": '"spec/standards/DOWNLOADED.md；demo"',
}
    "spec_revision": "IEC-60812",
    "spec_type": "safety",
    "source": "https://example.invalid/demo-FMEA.md",
    "standard_ref": '"IEC 60812"',
    "audit_trail": '"spec/standards/DOWNLOADED.md；demo"',
}


def _registered(monkeypatch, path: pathlib.Path, entry: dict) -> None:
    monkeypatch.setitem(uf.REGISTRY, path.name, entry)


# ── ① 单源一致性（镜像表 vs 模型规则表）──────────────────────────────────────


def test_required_meta_mirrors_model_rule_table():
    """脚本 `DOC_TYPE_REQUIRED_META` 必须逐 doc_type 等于 `DOC_TYPE_RULES[*].required_meta_fields`。"""
    mirror = {doc_type: tuple(rule.required_meta_fields) for doc_type, rule in DOC_TYPE_RULES.items()}
    assert set(uf.DOC_TYPE_REQUIRED_META) == set(DOC_TYPES)
    assert uf.DOC_TYPE_REQUIRED_META == mirror


def test_field_order_covers_all_c5_fields():
    """新建块按 `FIELD_ORDER` 写出，C5 十七字段必须都在该顺序表内（否则新语料行序漂移）。"""
    assert set(DOC_TYPE_RULES["standard"].required_meta_fields) <= set(uf.FIELD_ORDER)


# ── ② 已有 frontmatter：只增不改 + 幂等 ─────────────────────────────────────


def test_existing_frontmatter_is_only_appended(monkeypatch, tmp_path, capsys):
    path = tmp_path / "demo-lang.md"
    original_fm = "---\ntitle: Demo Lang\ncustom_field: keep-me\nspec_type: lang\n---\n"
    path.write_text(original_fm + BODY, encoding="utf-8")
    _registered(
        monkeypatch,
        path,
        {
            "spec_id": "SPEC-LANG-DEMO",
            "spec_org": "demo/org",
            "spec_revision": "v1",
            "spec_type": "lang",
            "source": "https://example.invalid/demo.md",
            "command_name": '"demo"',
            "syntax": '"demo <arg>"',
def test_required_meta_mirrors_model_rule_table():
    """脚本 `DOC_TYPE_REQUIRED_META` = C5 十七字段 ∪ `DOC_TYPE_RULES[*].required_meta_fields`（逐 doc_type 相符）。"""
    mirror = {
        doc_type: C5_META_FIELDS + tuple(f for f in rule.required_meta_fields if f not in C5_META_FIELDS)
        for doc_type, rule in DOC_TYPE_RULES.items()
    }
    assert set(uf.DOC_TYPE_REQUIRED_META) == set(DOC_TYPES)
    assert uf.DOC_TYPE_REQUIRED_META == mirror
    assert text.startswith(original_fm)  # 已有的行原样保留（顺序与内容均不变）
    assert "custom_field: keep-me" in text
    assert text[len(original_fm) :].startswith("type: composite\n")  # 缺失字段追加在已有块之后
    fm = parse_frontmatter(text, doc_slug="demo-lang")
    assert fm.body == BODY  # 正文逐字节保留
    assert fm.doc_type == "lang"
    assert fm.body_start > 1  # frontmatter 仍在文件顶部

    first_pass = path.read_text(encoding="utf-8")
    uf.upgrade(path)  # 幂等：第二遍无缺失字段
    assert path.read_text(encoding="utf-8") == first_pass
    assert "[skip]" in capsys.readouterr().out


def test_legacy_corpus_files_are_complete_readonly():
    """既有 7 份语料（`standards/{pcie,cxl,jedec,amba}`）**只读**核对：C5 十七字段齐全。

    不执行脚本（避免测试写坏真实语料）；这是「跑脚本必 `[skip]`」的前置条件。
    """

    files = sorted(
        p
        for sub in ("pcie", "cxl", "jedec", "amba")
        for p in (ROOT / "spec" / "standards" / sub).glob("*.md")
    )
    assert len(files) == 7
    for path in files:
        text = path.read_text(encoding="utf-8")
        m = uf.FM_RE.match(text)
        assert m is not None, path.name
        fields = yaml.safe_load(m.group(1))
        assert missing_required_meta("standard", fields) == [], path.name
        assert fields["spec_type"] == "standard", path.name


# ── ③ 无 frontmatter：新建 + 可被 M03 解析 ─────────────────────────────────


def test_creates_frontmatter_when_absent(monkeypatch, tmp_path, capsys):
    path = tmp_path / "demo-FMEA.md"
    path.write_text(BODY, encoding="utf-8")
    _registered(monkeypatch, path, dict(SAFETY_ENTRY))

    uf.upgrade(path)
    text = path.read_text(encoding="utf-8")

    assert text.startswith("---\ntitle: ")
    fm = parse_frontmatter(text, doc_slug="demo-FMEA")
    assert fm.body == BODY
    assert fm.doc_type == "safety"  # spec_type=safety -> doc_type=safety（非 standard）
    assert fm.fields["spec_id"] == "SPEC-SAFE-DEMO"
    assert fm.fields["status"] == "approved"  # A13：有 reviewed_by -> approved
    assert missing_required_meta("safety", fm.meta) == []
    assert "[new]" in capsys.readouterr().out


def test_title_falls_back_to_first_heading(monkeypatch, tmp_path):
    path = tmp_path / "no-heading.docx.md"
    path.write_text(BODY, encoding="utf-8")
    _registered(monkeypatch, path, dict(SAFETY_ENTRY))
    uf.upgrade(path)
    assert 'title: "Demo FMEA"' in path.read_text(encoding="utf-8")


def test_spec_type_conflict_is_refused(monkeypatch, tmp_path):
    """已有 `spec_type` 与登记表冲突 -> 报错，且**不改写**该文件（绝不猜测/改已有字段）。"""
    path = tmp_path / "demo-FMEA.md"
    original = "---\ntitle: Demo\nspec_type: standard\n---\n" + BODY
    path.write_text(original, encoding="utf-8")
    _registered(monkeypatch, path, dict(SAFETY_ENTRY))

    with pytest.raises(uf.UpgradeError, match="冲突"):
        uf.upgrade(path)
    assert path.read_text(encoding="utf-8") == original


# ── 跳过 / 报错 / 批量隔离 ────────────────────────────────────────────────


def test_non_markdown_corpus_is_skipped(monkeypatch, tmp_path, capsys):
    path = tmp_path / "demo.rst"
    path.write_text("Options\n=======\n", encoding="utf-8")
    _registered(monkeypatch, path, {"spec_id": "SPEC-TOOL-DEMO", "spec_type": "tool-manual"})

    uf.upgrade(path)
    assert path.read_text(encoding="utf-8") == "Options\n=======\n"  # 未被当 markdown 处理
    assert "[skip-nonmd]" in capsys.readouterr().out


def test_license_file_is_skipped_without_registry(tmp_path, capsys):
    path = tmp_path / "demo-LICENSE"
    path.write_text("Apache License 2.0\n", encoding="utf-8")
    uf.upgrade(path)
    assert path.read_text(encoding="utf-8") == "Apache License 2.0\n"
    assert "[skip-license]" in capsys.readouterr().out


def test_unregistered_file_raises(tmp_path):
    path = tmp_path / "unknown.md"
    path.write_text(BODY, encoding="utf-8")
    with pytest.raises(uf.UpgradeError, match="未在 REGISTRY 登记"):
        uf.upgrade(path)
    assert path.read_text(encoding="utf-8") == BODY


def test_main_isolates_failures_and_reports_exit_code(monkeypatch, tmp_path, capsys):
    """批量：单个文件失败不阻断其余，退出码 1 汇总；无参数 -> 2。"""
    bad = tmp_path / "unregistered.md"
    bad.write_text(BODY, encoding="utf-8")
    good = tmp_path / "demo-FMEA.md"
    good.write_text(BODY, encoding="utf-8")
    _registered(monkeypatch, good, dict(SAFETY_ENTRY))

    assert uf.main([str(bad), str(good)]) == 1
    out = capsys.readouterr().out
    assert "[err] unregistered.md 未在 REGISTRY 登记" in out
    assert good.read_text(encoding="utf-8").startswith("---\n")  # 失败隔离：后续文件仍处理
    assert bad.read_text(encoding="utf-8") == BODY
    assert uf.main([]) == 2
