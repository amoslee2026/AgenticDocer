"""临时：M03 语料形态勘察 5——目录区/残余 HTML/列表与段落规模。"""

import pathlib
import re

root = pathlib.Path("/home/lxx/wrk/AgenticDocer/spec/standards")


def show(name, lo, hi):
    f = root / name
    lines = f.read_text(encoding="utf-8").split("\n")
    print(f"\n=== {name} [{lo}-{hi}] ===")
    for i in range(lo, min(hi, len(lines)) + 1):
        print(i, repr(lines[i - 1][:130]))


show("pcie/PCI_Express_Base_Specification_Revision_5.0.md", 1259, 1275)
show("pcie/PCI_Express_Base_Specification_Revision_5.0.md", 1882, 1898)
show("cxl/CXL_Specification_rev3p2_ver1p0.md", 30, 70)
show("jedec/JEDEC_JESD270-4A_HBM4_2025.md", 30, 60)
show("jedec/JEDEC_JESD270-4A_HBM4_2025.md", 150, 175)

print("\n=== 残余 HTML 行（非 <table/<img）===")
for f in sorted(root.glob("*/*.md")):
    lines = f.read_text(encoding="utf-8").split("\n")
    n = 0
    for i, l in enumerate(lines, 1):
        s = l.lstrip()
        if s.startswith("<") and not s.startswith(("<table", "<img")):
            n += 1
            if n <= 6:
                print(f.name, i, repr(l[:130]))
    print("  ->", f.name, "residual lines:", n)

print("\n=== 列表块规模 ===")
LIST = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\S")
for f in sorted(root.glob("*/*.md")):
    lines = f.read_text(encoding="utf-8").split("\n")
    blocks = 0
    items = 0
    i = 0
    while i < len(lines):
        if LIST.match(lines[i]):
            blocks += 1
            while i < len(lines):
                if LIST.match(lines[i]):
                    items += 1
                    i += 1
                elif lines[i].strip() == "" and i + 1 < len(lines) and LIST.match(lines[i + 1]):
                    i += 1
                else:
                    break
        else:
            i += 1
    print(f.name, "list_blocks", blocks, "items", items)
