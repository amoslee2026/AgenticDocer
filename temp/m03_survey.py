"""临时：M03 语料形态勘察（不入库，仅统计）。"""

import collections
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/home/lxx/wrk/AgenticDocer/spec/standards")
files = sorted(root.glob("*/*.md"))
tot = collections.Counter()
for f in files:
    t = f.read_text(encoding="utf-8")
    lines = t.split("\n")
    c = collections.Counter()
    c["lines"] = len(lines)
    c["headings"] = sum(1 for l in lines if re.match(r"^#{1,6} ", l))
    c["md_table_sep"] = sum(
        1 for l in lines if re.match(r"^\s*\|[\s:|-]*-{3,}[\s:|-]*\|\s*$", l)
    )
    c["html_table"] = len(re.findall(r"<table[ >]", t))
    c["code_fence_open"] = sum(1 for l in lines if l.strip().startswith("```"))
    c["md_img"] = len(re.findall(r"!\[[^\]]*\]\(", t))
    c["html_img"] = len(re.findall(r"<img\b", t))
    c["list_items"] = sum(1 for l in lines if re.match(r"^\s*([-*+]|\d+[.)])\s+\S", l))
    c["html_block_lines"] = sum(1 for l in lines if l.lstrip().startswith("<"))
    tot.update(c)
    print(f.name, dict(c))
print("TOTAL", dict(tot))

# 标题形态抽样
print("\n=== heading samples (PCIe) ===")
pci = root / "pcie" / "PCI_Express_Base_Specification_Revision_5.0.md"
for i, l in enumerate(pci.read_text(encoding="utf-8").split("\n"), 1):
    if re.match(r"^#{1,6} ", l):
        print(i, l[:100])
        if i > 4000:
            break
