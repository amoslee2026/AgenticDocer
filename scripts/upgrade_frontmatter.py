#!/usr/bin/env python3
"""为 spec frontmatter 补全 mySkills 与 spec 专属字段（幂等）。

用法: uv run --no-project python3 scripts/upgrade_frontmatter.py <md文件...>
行为: 仅追加缺失字段，绝不改写已有字段；无 frontmatter 的文件报错退出。
status 判定（假设 A13）: frontmatter 已有 reviewed_by -> approved，否则 review。
新文档接入: 在 REGISTRY 登记其 spec_id/spec_org/spec_revision 三专属字段。
"""
import re
import sys
from pathlib import Path

COMMON_FIELDS = [
    ("type", "composite"),
    ("purpose", "spec"),
    ("audience", "both"),
    ("direction", "input"),
    ("version", '"1.0.0"'),
    ("section_meta", '"@meta"'),
    ("spec_type", "standard"),
]

# spec 专属字段登记表（首批 7 份；增量文档在此追加）
REGISTRY = {
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
}

FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def upgrade(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        sys.exit(f"[err] 无 frontmatter: {path}")
    fm = m.group(1)
    existing = {ln.split(":", 1)[0].strip() for ln in fm.splitlines() if ":" in ln}
    add = list(COMMON_FIELDS) + [
        (k, v) for k, v in REGISTRY.get(path.name, {}).items()
        if k not in existing
    ]
    # spec_id 缺失且未登记 -> 报错（不猜测）
    if "spec_id" not in existing and "spec_id" not in {k for k, _ in add}:
        sys.exit(f"[err] {path.name} 未在 REGISTRY 登记 spec_id/spec_org/spec_revision")
    # status 按溯源判定（A13）：已有字段则跳过，缺失时按 reviewed_by 推导
    if "status" not in existing:
        add.append(("status", "approved" if "reviewed_by" in existing else "review"))
    missing = [(k, v) for k, v in add if k not in existing]
    if not missing:
        print(f"[skip] {path.name}: 字段齐全")
        return
    new_fm = fm + "\n" + "\n".join(f"{k}: {v}" for k, v in missing)
    new_text = "---\n" + new_fm + "\n---\n" + text[m.end():]
    path.write_text(new_text, encoding="utf-8")
    print(f"[ok] {path.name}: +{len(missing)} 字段 ({', '.join(k for k, _ in missing)})")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for arg in sys.argv[1:]:
        upgrade(Path(arg))
