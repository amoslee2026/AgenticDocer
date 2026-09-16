"""`scripts/upgrade_frontmatter.py` 的契约守卫（方案 C 语料接入，2026-09-17）。

三条不可回退的契约：
① 脚本镜像的「导入必填 meta」与 `model/doc_types.py` **单源一致**（C5 ∪ 规则表专属项；防漂移）；
② 已有 frontmatter 的语料**零改写**——只追加缺失字段，字段齐全恒 `[skip]`（既有 7 份语料的安全网）；
③ 无 frontmatter 的语料**新建** frontmatter，正文逐字节保留，且结果能被 M03 `parse_frontmatter` 接受
（`doc_type` = 登记表的 `spec_type`，非 `standard`）。
另覆盖：非 markdown 语料 / 许可文件跳过；登记不全或 `spec_type` 冲突时报错且**不改写**该文件；批量失败隔离。
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys

import pytest
import yaml

from agenticdocer.importer import parse_frontmatter
from agenticdocer.model import C5_META_FIELDS, DOC_TYPES, DOC_TYPE_RULES, missing_required_meta

ROOT = pathlib.Path(__file__).resolve().parents[2]

BODY = "# Demo FMEA\n\n| failure mode | effect | RPN |\n|---|---|---|\n| stuck-high | no reset | 12 |\n"

_PROVENANCE = {  # 与脚本 `_DOWNLOADED` 同形：网络下载语料共用的溯源四项
    "converted_by": '"download（原样下载，未转换）"',
    "converted_at": "2026-09-17",
    "reviewed_by": '"lxx(下载授权)"',
    "reviewed_at": "2026-09-17",
}

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

LANG_ENTRY = {
    "spec_id": "SPEC-LANG-DEMO",
    "spec_org": "demo/org",
    "spec_revision": "v1",
    "spec_type": "lang",
    "source": "https://example.invalid/demo.md",
    **_PROVENANCE,
    "command_name": '"demo"',
    "syntax": '"demo <arg>"',
    "tool_context": '"demo tool 1.0"',
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


def _registered(monkeypatch, path: pathlib.Path, entry: dict) -> None:
    """把临时文件登记进脚本 `REGISTRY`（键 = basename，与生产路径同一机制）。"""
    monkeypatch.setitem(uf.REGISTRY, path.name, entry)


# ── ① 单源一致性（脚本镜像表 vs 模型规则表）────────────────────────────────


def test_required_meta_mirrors_model_rule_table():
    """`DOC_TYPE_REQUIRED_META` == C5 十七字段 ∪ `DOC_TYPE_RULES[*].required_meta_fields`（逐 doc_type）。"""
    mirror = {
        doc_type: C5_META_FIELDS + tuple(f for f in rule.required_meta_fields if f not in C5_META_FIELDS)
        for doc_type, rule in DOC_TYPE_RULES.items()
    }
    assert set(uf.DOC_TYPE_REQUIRED_META) == set(DOC_TYPES)
    assert uf.DOC_TYPE_REQUIRED_META == mirror


def test_field_order_covers_all_c5_fields():
    """新建块按 `FIELD_ORDER` 写出：C5 十七字段须都在顺序表内（否则新语料行序漂移）。"""
    assert set(C5_META_FIELDS) <= set(uf.FIELD_ORDER)
    assert uf.FIELD_ORDER[-1] == "status"  # 与既有 7 份语料同形：status 收尾


# ── ② 已有 frontmatter：只增不改 + 幂等 ─────────────────────────────────────


def test_existing_frontmatter_is_only_appended(monkeypatch, tmp_path, capsys):
    path = tmp_path / "demo-lang.md"
    head = "---\ntitle: Demo Lang\ncustom_field: keep-me\nspec_type: lang\n"
    path.write_text(head + "---\n" + BODY, encoding="utf-8")
    _registered(monkeypatch, path, dict(LANG_ENTRY))

    uf.upgrade(path)
    text = path.read_text(encoding="utf-8")

    assert text.startswith(head)  # 已有行原样保留（内容与顺序均不变）
    assert text[len(head) :].startswith("type: composite\n")  # 缺失字段追加在已有行之后
    fm = parse_frontmatter(text, doc_slug="demo-lang")
    assert fm.body == BODY  # 正文逐字节保留
    assert fm.doc_type == "lang"
    assert fm.body_start > 1  # frontmatter 仍在文件顶部
    assert "custom_field: keep-me" in text  # 非本脚本管辖的字段同样不动

    first_pass = text
    uf.upgrade(path)  # 幂等：第二遍无缺失字段
    assert path.read_text(encoding="utf-8") == first_pass
    assert "[skip]" in capsys.readouterr().out


def test_legacy_corpus_files_are_complete_readonly():
    """既有 7 份语料（`standards/{pcie,cxl,jedec,amba}`）**只读**核对：C5 十七字段齐全。

    不执行脚本（避免测试写坏真实语料）；这是「对它们跑脚本必 `[skip]`」的前置条件。
    """
    files = sorted(
        p
        for sub in ("pcie", "cxl", "jedec", "amba")
        for p in (ROOT / "spec" / "standards" / sub).glob("*.md")
    )
    assert len(files) == 7
    for path in files:
        m = uf.FM_RE.match(path.read_text(encoding="utf-8"))
        assert m is not None, path.name
        fields = yaml.safe_load(m.group(1))
        assert fields["spec_type"] == "standard", path.name
        assert missing_required_meta("standard", fields) == [], path.name


# ── ③ 无 frontmatter：新建 + 可被 M03 解析 ─────────────────────────────────


def test_creates_frontmatter_when_absent(monkeypatch, tmp_path, capsys):
    path = tmp_path / "demo-FMEA.md"
    path.write_text(BODY, encoding="utf-8")
    _registered(monkeypatch, path, dict(SAFETY_ENTRY))

    uf.upgrade(path)
    text = path.read_text(encoding="utf-8")

    assert text.startswith("---\ntitle: ")
    fm = parse_frontmatter(text, doc_slug="demo-FMEA")
    assert fm.body == BODY  # 原正文逐字节保留
    assert fm.doc_type == "safety"  # spec_type=safety -> doc_type=safety（非 standard）
    assert fm.fields["spec_id"] == "SPEC-SAFE-DEMO"
    assert fm.fields["status"] == "approved"  # A13：追加后已有 reviewed_by -> approved
    assert missing_required_meta("safety", fm.meta) == []
    assert "[new]" in capsys.readouterr().out


def test_title_falls_back_to_first_heading(monkeypatch, tmp_path):
    """无 frontmatter 且登记表未给 title -> 取首个 `# ` 标题（此处为正文首行）。"""
    path = tmp_path / "no-heading-doc.md"
    path.write_text(BODY, encoding="utf-8")
    _registered(monkeypatch, path, dict(SAFETY_ENTRY))
    uf.upgrade(path)
    assert 'title: "Demo FMEA"' in path.read_text(encoding="utf-8")


def test_status_is_review_without_reviewed_by(monkeypatch, tmp_path):
    """无 `reviewed_by` 的登记 -> `status: review`（A13 的保守分支，不是静默 approved）。"""
    path = tmp_path / "demo-raw.md"
    path.write_text(BODY, encoding="utf-8")
    entry = {k: v for k, v in SAFETY_ENTRY.items() if k not in ("reviewed_by", "reviewed_at")}
    entry["reviewed_by"] = '""'  # 占位空值仍算「有该字段」
    _registered(monkeypatch, path, entry)
    uf.upgrade(path)
    assert "status: approved" in path.read_text(encoding="utf-8")  # reviewed_by 存在 -> approved

    entry2 = {k: v for k, v in SAFETY_ENTRY.items() if k != "reviewed_by"}
    path2 = tmp_path / "demo-no-review.md"
    path2.write_text(BODY, encoding="utf-8")
    _registered(monkeypatch, path2, entry2)
    uf.upgrade(path2)
    assert "status: review" in path2.read_text(encoding="utf-8")


# ── 不猜测：类型冲突 / 登记不全 -> 报错且不写入 ───────────────────────────────


def test_spec_type_conflict_is_refused(monkeypatch, tmp_path):
    path = tmp_path / "demo-FMEA.md"
    original = "---\ntitle: Demo\nspec_type: standard\n---\n" + BODY
    path.write_text(original, encoding="utf-8")
    _registered(monkeypatch, path, dict(SAFETY_ENTRY))

    with pytest.raises(uf.UpgradeError, match="冲突"):
        uf.upgrade(path)
    assert path.read_text(encoding="utf-8") == original


@pytest.mark.parametrize("drop", ["audit_trail", "converted_by", "spec_id"])
def test_incomplete_registry_entry_is_refused(monkeypatch, tmp_path, drop):
    """登记表缺该 doc_type 必填 meta（含 C5 溯源项）-> 报错而不是写出半份 frontmatter。"""
    path = tmp_path / "demo-FMEA.md"
    path.write_text(BODY, encoding="utf-8")
    entry = {k: v for k, v in SAFETY_ENTRY.items() if k != drop}
    _registered(monkeypatch, path, entry)

    with pytest.raises(uf.UpgradeError, match="必填 meta 缺"):
        uf.upgrade(path)
    assert path.read_text(encoding="utf-8") == BODY


def test_unregistered_file_raises(tmp_path):
    path = tmp_path / "unknown-doc.md"
    path.write_text(BODY, encoding="utf-8")
    with pytest.raises(uf.UpgradeError, match="未在 REGISTRY 登记"):
        uf.upgrade(path)
    assert path.read_text(encoding="utf-8") == BODY


# ── 跳过类：非 markdown 语料 / 许可文件 ─────────────────────────────────────


def test_non_markdown_corpus_is_skipped(monkeypatch, tmp_path, capsys):
    """`.rst`/`.n`/`.hjson`/`.adoc`/`.xml` 不得当 markdown 处理（须前置转换）。"""
    path = tmp_path / "demo.rst"
    path.write_text("Options\n=======\n", encoding="utf-8")
    _registered(monkeypatch, path, {"spec_id": "SPEC-TOOL-DEMO", "spec_type": "tool-manual"})

    uf.upgrade(path)
    assert path.read_text(encoding="utf-8") == "Options\n=======\n"
    assert "[skip-nonmd]" in capsys.readouterr().out


def test_license_file_is_skipped_without_registry(tmp_path, capsys):
    """许可文件（`*-LICENSE`/`*-license.terms`）不是文档语料：跳过且无需登记。"""
    path = tmp_path / "demo-LICENSE"
    path.write_text("Apache License 2.0\n", encoding="utf-8")
    uf.upgrade(path)
    assert path.read_text(encoding="utf-8") == "Apache License 2.0\n"
    assert "[skip-license]" in capsys.readouterr().out


# ── 批量：失败隔离 + 退出码 ──────────────────────────────────────────────────


def test_main_isolates_failures_and_reports_exit_code(monkeypatch, tmp_path, capsys):
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

    assert uf.main([]) == 2  # 无参数 = 用法错误
