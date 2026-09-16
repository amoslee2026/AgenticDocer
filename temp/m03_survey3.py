"""临时：M03 语料形态勘察 3——各文档标题层级/编号、CXL Test Steps、列表、代码块。"""

import collections
import pathlib
import re

root = pathlib.Path("/home/lxx/wrk/AgenticDocer/spec/standards")
for f in sorted(root.glob("*/*.md")):
    lines = f.read_text(encoding="utf-8").split("\n")
    hs = [l for l in lines if re.match(r"^#+ ", l)]
    hist = collections.Counter(len(re.match(r"^(#+) ", l).group(1)) for l in hs)
    numbered = sum(1 for l in hs if re.match(r"^#+ \d+(\.\d+)*", l))
    print(f"\n### {f.name} headings={len(hs)} hist={dict(sorted(hist.items()))} numbered={numbered}")
    for l in hs[:12]:
        print("   ", repr(l[:100]))
    for l in hs[-6:]:
        print("   ..", repr(l[:100]))

cxl = (root / "cxl" / "CXL_Specification_rev3p2_ver1p0.md").read_text(encoding="utf-8").split("\n")
print("\n=== CXL 'Test Steps' 上下文 ===")
n = 0
for i, l in enumerate(cxl, 1):
    if l.strip() == "## Test Steps:":
        print(i, repr(l))
        for j in range(i, i + 6):
            print("   ", j, repr(cxl[j - 1][:120]))
        n += 1
        if n >= 2:
            break

print("\n=== CXL 代码块 ===")
for i, l in enumerate(cxl, 1):
    if l.strip().startswith("```"):
        print(i, repr(l[:120]))

pci = (root / "pcie" / "PCI_Express_Base_Specification_Revision_5.0.md").read_text(encoding="utf-8").split("\n")
print("\n=== PCIe 代码块 ===")
for i, l in enumerate(pci, 1):
    if l.strip().startswith("```"):
        print(i, repr(l[:120]))
        for j in range(i + 1, min(i + 6, len(pci) + 1)):
            print("   ", j, repr(pci[j - 1][:100]))
