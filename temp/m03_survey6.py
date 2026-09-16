"""临时：AMBA AXI/JEDEC 标题形态细查。"""

import pathlib
import re

root = pathlib.Path("/home/lxx/wrk/AgenticDocer/spec/standards")
for rel, lo, hi in [
    ("amba/IHI0022K_AMBA_AXI_ACE_protocol_spec.md", 1, 8111),
    ("amba/IHI0033C_AMBA_AHB_spec.md", 1, 2125),
    ("jedec/JEDEC_JESD270-4A_HBM4_2025.md", 1, 4098),
]:
    lines = (root / rel).read_text(encoding="utf-8").split("\n")
    hs = [(i, l) for i, l in enumerate(lines, 1) if re.match(r"^#+ ", l)]
    print(f"\n### {rel} 共 {len(hs)} 标题；中段样本：")
    mid = len(hs) // 3
    for i, l in hs[mid : mid + 18]:
        print("  ", i, repr(l[:100]))
