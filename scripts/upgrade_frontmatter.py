#!/usr/bin/env python3
"""为 spec frontmatter 补全 mySkills 与 spec 专属字段（幂等，只增不改）。

用法: uv run --no-project python3 scripts/upgrade_frontmatter.py <文件...>

行为（`.md` / `.markdown`）:
- **已有 frontmatter**：只追加缺失字段，绝不改写已有行（既有 7 份语料恒 `[skip]`）；
- **无 frontmatter**：**新建**一个完整 frontmatter 块置顶，原正文逐字节保留在其后
  （`title` 取首个 `# ` 标题；登记表 `title` 优先）。
- **非 markdown 语料**（`.n` nroff / `.rst` / `.hjson` / `.adoc` / …）：跳过并提示需前置转换——
  方案 C 的 47 份真实语料里只有 `safety/*.md` 与 `lang/opensta-commands.md` 是 markdown；
  其余**不得当 markdown 处理**，须先转换为 markdown 再跑本脚本。
  UCIS `.xml` 走 `agenticdocer.importer.vplan`（UCIS 解析器），不经本脚本。

`status` 判定（假设 A13）: 追加后已有 `reviewed_by` -> `approved`，否则 `review`。
`spec_type` 取值域（单源 `agenticdocer/model/doc_types.py`；本脚本零依赖故镜像）:
`standard` | `lang` | `tool-manual` | `product` | `safety`（缺省 `standard`，向后兼容首批 7 份）。

新文档接入: 在 `REGISTRY` 登记 `spec_id`/`spec_org`/`spec_revision`/`spec_type`，**外加**该
doc_type 的必填 meta（见 `DOC_TYPE_REQUIRED_META`；来自 `spec/arch_spec/doc_type_mapping.md` §3）
与溯源五项（`source` 逐文件给，`_DOWNLOADED` 供同批复用）。登记不全 / `spec_type` 非法 /
已有 `spec_type` 与登记冲突 -> **报错退出，不猜测**。

`REGISTRY` 的值按 YAML 字面量书写（含 `: `/`#`/空格/中文等标量的自行加引号）；脚本原样写入。
漂移守卫: `DOC_TYPE_REQUIRED_META` 与 `DOC_TYPE_RULES[*].required_meta_fields` 的对照由
`tests/unit/test_upgrade_frontmatter.py` 承担——改模型规则表须同步改本表。
"""
import re
import sys
from pathlib import Path

MARKDOWN_SUFFIXES = (".markdown", ".md")

# doc 元数据固定字段（`title` 见 `_title_for`；`spec_type` 逐文件取登记表；`status` 按 A13 判定）
COMMON_FIELDS = [
    ("type", "composite"),
    ("purpose", "spec"),
    ("audience", "both"),
    ("direction", "input"),
    ("version", '"1.0.0"'),
    ("section_meta", '"@meta"'),
]

DEFAULT_SPEC_TYPE = "standard"

# 各 doc_type 的必填 meta（镜像 `model/doc_types.py::DOC_TYPE_RULES[*].required_meta_fields`；
# `standard` 即 C5 十七字段）。缺项 = 该文件导入必 422（`importer/frontmatter.py`），故在此前置拦截。
DOC_TYPE_REQUIRED_META = {
    "standard": (
        "title",
        "type",
        "purpose",
        "audience",
        "direction",
        "status",
        "version",
        "section_meta",
        "spec_id",
        "spec_type",
        "spec_org",
        "spec_revision",
        "source",
        "converted_by",
        "converted_at",
        "reviewed_by",
        "reviewed_at",
    ),
    "lang": ("command_name", "syntax", "tool_context"),
    "tool-manual": ("command_name", "syntax", "tool_context"),
    "product": ("doc_subtype", "traces_to", "owner"),
    "safety": ("standard_ref", "audit_trail"),
}

# frontmatter 写出顺序（与 `spec/README.md`「frontmatter 规范（v2）」及既有 7 份语料同形；
# 未列字段按登记表顺序缀后）
FIELD_ORDER = (
    "title",
    "type",
    "purpose",
    "audience",
    "direction",
    "version",
    "section_meta",
    "spec_id",
    "spec_type",
    "spec_org",
    "spec_revision",
    "source",
    "converted_by",
    "converted_at",
    "reviewed_by",
    "reviewed_at",
    "status",
)

# 方案 C 网络下载语料共用的溯源四项（`source` 逐文件给；清单/许可/字节数见 spec/standards/DOWNLOADED.md）
_DOWNLOADED = {
    "converted_by": '"download（原样下载，未转换）"',
    "converted_at": "2026-09-17",
    "reviewed_by": '"lxx(下载授权)"',
    "reviewed_at": "2026-09-17",
}

# spec 专属字段登记表（逐文件；`spec_type` 省略 = standard）
REGISTRY = {
    # ── 首批 7 份（2026-09-16 自 GigaRAG 迁入；frontmatter 已含 C5 十七字段，恒 [skip]）──
    "PCI_Express_Base_Specification_Revision_5.0.md": {
        "spec_id": "SPEC-STD-PCIE-5.0", "spec_org": "PCI-SIG", "spec_revision": '"5.0 v1.0"',
    },
    "CXL_Specification_rev3p2_ver1p0.md": {
        "spec_id": "SPEC-STD-CXL-3.2", "spec_org": "CXL Consortium", "spec_revision": '"r3.2 v1.0"',
    },
    "JEDEC_JESD270-4A_HBM4_2025.md": {
        "spec_id": "SPEC-STD-HBM4-JESD270-4A", "spec_org": "JEDEC", "spec_revision": "JESD270-4A",
    },
    "IHI0033C_AMBA_AHB_spec.md": {
        "spec_id": "SPEC-STD-AMBA-AHB-C", "spec_org": "ARM", "spec_revision": "IHI0033C",
    },
    "IHI0033B_AMBA5_AHB_AHB-Lite_spec.md": {
        "spec_id": "SPEC-STD-AMBA-AHB-LITE-B", "spec_org": "ARM", "spec_revision": "IHI0033B",
    },
    "IHI0024_AMBA_APB_spec.md": {
        "spec_id": "SPEC-STD-AMBA-APB", "spec_org": "ARM", "spec_revision": "IHI0024",
    },
    "IHI0022K_AMBA_AXI_ACE_protocol_spec.md": {
        "spec_id": "SPEC-STD-AMBA-AXI-K", "spec_org": "ARM", "spec_revision": "IHI0022K",
    },
    # ── 方案 C 新增：真实语料（2026-09-17 网络下载，HTTP 200 实测 + 许可核查）──
    #
    # `.md`：可直接入库（本脚本补 frontmatter 后即能被 M03 解析）
    "neqsim-FMEA.md": {
        "spec_id": "SPEC-SAFE-NEQSIM-FMEA",
        "spec_org": "Equinor/neqsim",
        "spec_revision": "IEC-60812",
        "spec_type": "safety",
        **_DOWNLOADED,
        "source": "https://raw.githubusercontent.com/equinor/neqsim/master/docs/safety/FMEA.md",
        "standard_ref": '"IEC 60812（2018）"',
        "audit_trail": (
            '"spec/standards/DOWNLOADED.md §2.4；Apache-2.0；'
            '2026-09-17 下载自 equinor/neqsim@master:docs/safety/FMEA.md"'
        ),
    },
    "protective-stop-FMEDA.md": {
        "spec_id": "SPEC-SAFE-PROTECTIVE-STOP-FMEDA",
        "spec_org": "polymathrobotics/protective-stop",
        "spec_revision": "main",
        "spec_type": "safety",
        **_DOWNLOADED,
        "source": (
            "https://raw.githubusercontent.com/polymathrobotics/protective-stop/main/docs/safety/FMEDA.md"
        ),
        "standard_ref": '"IEC 61508-2／IEC 61508-6 + ISO 13849-1"',
        "audit_trail": (
            '"spec/standards/DOWNLOADED.md §2.4；Apache-2.0；'
            '2026-09-17 下载自 polymathrobotics/protective-stop@main:docs/safety/FMEDA.md"'
        ),
    },
    "cdriscv-FMEDA.md": {
        "spec_id": "SPEC-SAFE-CDRISCV-FMEDA",
        "spec_org": "ChipDesign-BV/cdriscv-32s-10",
        "spec_revision": "main",
        "spec_type": "safety",
        **_DOWNLOADED,
        "source": "https://raw.githubusercontent.com/ChipDesign-BV/cdriscv-32s-10/main/doc/fmeda.md",
        "standard_ref": (
            '"ISO 26262-5（ASIL D：SPFM≥99%、LFM≥90% 阈值判据；原文未指名标准，按所引阈值反推）"'
        ),
        "audit_trail": (
            '"spec/standards/DOWNLOADED.md §2.4；Apache-2.0；'
            '2026-09-17 下载自 ChipDesign-BV/cdriscv-32s-10@main:doc/fmeda.md"'
        ),
    },
    "opensta-commands.md": {
        "spec_id": "SPEC-LANG-OPENSTA-CMD",
        "spec_org": "Parallax/OpenSTA",
        "spec_revision": "master",
        "spec_type": "lang",
        **_DOWNLOADED,
        "source": "https://raw.githubusercontent.com/parallaxsw/OpenSTA/master/doc/Commands.md",
        "command_name": '"OpenSTA Tcl 命令参考（283 个命令节）"',
        "syntax": '"逐命令 `<pre><code>` 语法块（见正文各节）"',
        "tool_context": '"OpenSTA（Parallax）master"',
    },
    # 以下为**非 markdown 语料**：登记的是 `spec_id` 预分配与类型判定；脚本按后缀跳过，
    # 须先转换为 markdown（转换后文件名若变化，同步改本表键名）并补齐该 doc_type 的必填 meta。
    #
    # `lang/`：Tcl 内置命令 man pages（nroff，DocBook RefEntry 原型；此处登记代表 3 份）
    "set.n": {
        "spec_id": "SPEC-LANG-TCL-SET",
        "spec_org": "Tcl Core Team",
        "spec_revision": '"8.7"',
        "spec_type": "lang",
        **_DOWNLOADED,
        "source": "https://raw.githubusercontent.com/tcltk/tcl/main/doc/set.n",
    },
    "proc.n": {
        "spec_id": "SPEC-LANG-TCL-PROC",
        "spec_org": "Tcl Core Team",
        "spec_revision": '"8.7"',
        "spec_type": "lang",
        **_DOWNLOADED,
        "source": "https://raw.githubusercontent.com/tcltk/tcl/main/doc/proc.n",
    },
    "expr.n": {
        "spec_id": "SPEC-LANG-TCL-EXPR",
        "spec_org": "Tcl Core Team",
        "spec_revision": '"8.7"',
        "spec_type": "lang",
        **_DOWNLOADED,
        "source": "https://raw.githubusercontent.com/tcltk/tcl/main/doc/expr.n",
    },
    # `tool-manual/`：Verilator 用户指南（rst）
    "verilator-exe.rst": {
        "spec_id": "SPEC-TOOL-VERILATOR-EXE",
        "spec_org": "Verilator",
        "spec_revision": "master",
        "spec_type": "tool-manual",
        **_DOWNLOADED,
        "source": "https://raw.githubusercontent.com/verilator/verilator/master/docs/guide/exe_verilator.rst",
    },
    "verilator-warnings.rst": {
        "spec_id": "SPEC-TOOL-VERILATOR-WARN",
        "spec_org": "Verilator",
        "spec_revision": "master",
        "spec_type": "tool-manual",
        **_DOWNLOADED,
        "source": "https://raw.githubusercontent.com/verilator/verilator/master/docs/guide/warnings.rst",
    },
    # `product/`：OpenTitan AES（hjson）+ RISC-V ISA Manual（adoc）
    "opentitan-aes.hjson": {
        "spec_id": "SPEC-PROD-OPENTITAN-AES-IP",
        "spec_org": "lowRISC/OpenTitan",
        "spec_revision": "master",
        "spec_type": "product",
        **_DOWNLOADED,
        "source": "https://raw.githubusercontent.com/lowRISC/opentitan/master/hw/ip/aes/data/aes.hjson",
    },
    "opentitan-aes_testplan.hjson": {
        "spec_id": "SPEC-PROD-OPENTITAN-AES-TESTPLAN",
        "spec_org": "lowRISC/OpenTitan",
        "spec_revision": "master",
        "spec_type": "product",
        **_DOWNLOADED,
        "source": "https://raw.githubusercontent.com/lowRISC/opentitan/master/hw/ip/aes/data/aes_testplan.hjson",
    },
    "opentitan-aes_sec_cm_testplan.hjson": {
        "spec_id": "SPEC-PROD-OPENTITAN-AES-SEC-CM-TESTPLAN",
        "spec_org": "lowRISC/OpenTitan",
        "spec_revision": "master",
        "spec_type": "product",
        **_DOWNLOADED,
        "source": (
            "https://raw.githubusercontent.com/lowRISC/opentitan/master/hw/ip/aes/data/"
            "aes_sec_cm_testplan.hjson"
        ),
    },
    "riscv-isa-csrs.adoc": {
        "spec_id": "SPEC-PROD-RISCV-ISA-CSRS",
        "spec_org": "RISC-V International",
        "spec_revision": "main",
        "spec_type": "product",
        **_DOWNLOADED,
        "source": "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/priv/csrs.adoc",
    },
    "riscv-isa-machine.adoc": {
        "spec_id": "SPEC-PROD-RISCV-ISA-MACHINE",
        "spec_org": "RISC-V International",
        "spec_revision": "main",
        "spec_type": "product",
        **_DOWNLOADED,
        "source": "https://raw.githubusercontent.com/riscv/riscv-isa-manual/main/src/priv/machine.adoc",
    },
    # `ucis/`：UCIS XML 结构化数据（走 `importer/vplan.py`，不经本脚本；此处仅登记身份）
    "pyucis-toggle_2state.xml": {
        "spec_id": "SPEC-UCIS-PYUCIS-TOGGLE-2STATE",
        "spec_org": "fvutils/pyucis",
        "spec_revision": '"1.0"',
        "spec_type": "standard",
        **_DOWNLOADED,
        "source": (
            "https://raw.githubusercontent.com/fvutils/pyucis/master/tests/conversion/fixtures/xml/"
            "toggle_2state.xml"
        ),
    },
    "pyucis-fsm_example.xml": {
        "spec_id": "SPEC-UCIS-PYUCIS-FSM-EXAMPLE",
        "spec_org": "fvutils/pyucis",
        "spec_revision": '"1.0"',
        "spec_type": "standard",
        **_DOWNLOADED,
        "source": (
            "https://raw.githubusercontent.com/fvutils/pyucis/master/tests/conversion/fixtures/xml/"
            "fsm_example.xml"
        ),
    },
    "pyucis-block_statement.xml": {
        "spec_id": "SPEC-UCIS-PYUCIS-BLOCK-STATEMENT",
        "spec_org": "fvutils/pyucis",
        "spec_revision": '"1.0"',
        "spec_type": "standard",
        **_DOWNLOADED,
        "source": (
            "https://raw.githubusercontent.com/fvutils/pyucis/master/tests/conversion/fixtures/xml/"
            "block_statement.xml"
        ),
    },
    "pyucis-branch_nested.xml": {
        "spec_id": "SPEC-UCIS-PYUCIS-BRANCH-NESTED",
        "spec_org": "fvutils/pyucis",
        "spec_revision": '"1.0"',
        "spec_type": "standard",
        **_DOWNLOADED,
        "source": (
            "https://raw.githubusercontent.com/fvutils/pyucis/master/tests/conversion/fixtures/xml/"
            "branch_nested.xml"
        ),
    },
    "pyucis-assertion_cover.xml": {
        "spec_id": "SPEC-UCIS-PYUCIS-ASSERTION-COVER",
        "spec_org": "fvutils/pyucis",
        "spec_revision": '"1.0"',
        "spec_type": "standard",
        **_DOWNLOADED,
        "source": (
            "https://raw.githubusercontent.com/fvutils/pyucis/master/tests/conversion/fixtures/xml/"
            "assertion_cover.xml"
        ),
    },
    "fc4sc-coverage-results-gold.xml": {
        "spec_id": "SPEC-UCIS-FC4SC-COVERAGE-GOLD",
        "spec_org": "amiq-consulting/fc4sc",
        "spec_revision": '"1.0"',
        "spec_type": "standard",
        **_DOWNLOADED,
        "source": (
            "https://raw.githubusercontent.com/amiq-consulting/fc4sc/master/examples/fir/"
            "coverage_results_gold.xml"
        ),
    },
}

FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

# 许可文件（`LICENSE` / `neqsim-LICENSE` / `riscv-isa-LICENSE.adoc` / `tcl-license.terms`…）不是
# 文档语料 -> 不登记、不改写（见 spec/standards/DOWNLOADED.md 的 47 份清单）
LICENSE_NAME_RE = re.compile(r"(^|[-_.])licen[cs]e([-_.]|$)", re.IGNORECASE)


class UpgradeError(Exception):
    """该文件无法安全处理（未登记 / `spec_type` 非法 / 必填 meta 缺 / 类型冲突）——报错但不猜测。"""


def _yaml_quote(value: str) -> str:
    """双引号 YAML 标量（转义 `\\` 与 `"`）——用于从正文推导的 `title`。"""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _title_for(path: Path, text: str, entry: dict) -> str:
    """新建 frontmatter 的 `title`：登记表优先，其次首个 `# ` 标题，最后文件名主干。"""
    if "title" in entry:
        return entry["title"]
    for line in text.splitlines():
        if line.startswith("# "):
            return _yaml_quote(line[2:].strip())
    return _yaml_quote(path.stem)


def _ordered(pairs: list) -> list:
    """按 `FIELD_ORDER` 排（未列字段保持登记表顺序——`sorted` 稳定）。"""
    return sorted(
        pairs, key=lambda kv: FIELD_ORDER.index(kv[0]) if kv[0] in FIELD_ORDER else len(FIELD_ORDER)
    )


def upgrade(path: Path) -> None:
    """处理单份文件；不可安全处理 -> :class:`UpgradeError`（调用方决定是否继续）。"""
    if LICENSE_NAME_RE.search(path.name):
        print(f"[skip-license] {path.name}: 许可文件（非文档语料，不登记）")
        return
    entry = REGISTRY.get(path.name)
    if entry is None:
        raise UpgradeError(
            f"{path.name} 未在 REGISTRY 登记（spec_id/spec_org/spec_revision/spec_type + 该类型必填 meta）"
        )
    spec_type = entry.get("spec_type", DEFAULT_SPEC_TYPE)
    if spec_type not in DOC_TYPE_REQUIRED_META:
        raise UpgradeError(f"{path.name}: spec_type={spec_type!r} 不在取值域 {sorted(DOC_TYPE_REQUIRED_META)}")
    if path.suffix.lower() not in MARKDOWN_SUFFIXES:
        print(f"[skip-nonmd] {path.name}: {path.suffix} 非 markdown 语料，需前置转换后才能补 frontmatter")
        return

    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    fm = m.group(1) if m else None
    body_start = m.end() if m else 0
    existing = {}
    if fm is not None:
        existing = {ln.split(":", 1)[0].strip(): ln.split(":", 1)[1] for ln in fm.splitlines() if ":" in ln}
    declared = existing.get("spec_type", "").strip().strip("\"'")
    if declared and declared != spec_type:
        raise UpgradeError(f"{path.name}: 已有 spec_type={declared!r} 与登记表 {spec_type!r} 冲突（不改写已有字段）")

    add = []
    if "title" not in existing:
        add.append(("title", _title_for(path, text, entry)))
    add += [(k, v) for k, v in COMMON_FIELDS if k not in existing]
    add.append(("spec_type", spec_type))
    add += [(k, v) for k, v in entry.items() if k != "spec_type"]
    # status 按溯源判定（A13）：追加后已有 reviewed_by -> approved，否则 review
    have = set(existing) | {k for k, _ in add}
    if "status" not in have:
        add.append(("status", "approved" if "reviewed_by" in have else "review"))
    lack = [k for k in DOC_TYPE_REQUIRED_META[spec_type] if k not in have and k != "status"]
    if lack:
        raise UpgradeError(f"{path.name}: spec_type={spec_type} 必填 meta 缺 {lack}——请在 REGISTRY 补登记（不猜测）")

    missing = _ordered([(k, v) for k, v in add if k not in existing])
    if not missing:
        print(f"[skip] {path.name}: 字段齐全")
        return
    block = "\n".join(f"{k}: {v}" for k, v in missing)
    if fm is None:
        path.write_text(f"---\n{block}\n---\n{text}", encoding="utf-8")
        print(f"[new] {path.name}: 新建 frontmatter +{len(missing)} 字段 ({', '.join(k for k, _ in missing)})")
    else:
        path.write_text("---\n" + fm + "\n" + block + "\n---\n" + text[body_start:], encoding="utf-8")
        print(f"[ok] {path.name}: +{len(missing)} 字段 ({', '.join(k for k, _ in missing)})")


def main(argv: list) -> int:
    """批量处理（逐个隔离失败：单个文件报错不阻断其余，最后以退出码汇总）。"""
    if not argv:
        print(__doc__)
        return 2
    failures = 0
    for arg in argv:
        try:
            upgrade(Path(arg))
        except UpgradeError as exc:
            print(f"[err] {exc}")
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
