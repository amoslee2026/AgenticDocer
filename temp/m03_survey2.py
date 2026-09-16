"""临时：M03 语料形态勘察 2——标题/定义/HTML 残片/列表样本。"""

import pathlib
import re
import sys

root = pathlib.Path("/home/lxx/wrk/AgenticDocer/spec/standards")
text = (root / "pcie" / "PCI_Express_Base_Specification_Revision_5.0.md").read_text(encoding="utf-8")
lines = text.split("\n")

print("=== numbered headings (PCIe, 采样) ===")
seen = 0
for i, l in enumerate(lines, 1):
    if re.match(r"^#{1,6} ", l) and re.search(r"\d", l.split(" ", 1)[1][:12]):
        print(i, repr(l[:110]))
        seen += 1
        if seen > 25:
            break

print("\n=== heading level histogram ===")
import collections

h = collections.Counter(len(re.match(r"^(#+) ", l).group(1)) for l in lines if re.match(r"^#+ ", l))
print(dict(sorted(h.items())))

print("\n=== TOC 段样本 (PCIe 38-60) ===")
for i in range(38, 60):
    print(i, repr(lines[i - 1][:110]))

print("\n=== 非 table/img 的 < 行 (PCIe) ===")
n = 0
for i, l in enumerate(lines, 1):
    s = l.lstrip()
    if s.startswith("<") and not s.startswith("<table") and not s.startswith("<img"):
        print(i, repr(l[:150]))
        n += 1
        if n > 25:
            break

print("\n=== 定义形态（PCIe 术语表附近 2433-2450） ===")
for i in range(2433, 2452):
    print(i, repr(lines[i - 1][:150]))
