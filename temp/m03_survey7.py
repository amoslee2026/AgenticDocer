"""临时：glossary 区形态细查。"""

import pathlib

root = pathlib.Path("/home/lxx/wrk/AgenticDocer/spec/standards")


def show(rel, lo, hi):
    lines = (root / rel).read_text(encoding="utf-8").split("\n")
    print(f"\n=== {rel} [{lo}-{hi}] ===")
    for i in range(lo, min(hi, len(lines)) + 1):
        print(i, repr(lines[i - 1][:110]))


show("amba/IHI0033C_AMBA_AHB_spec.md", 160, 200)
show("amba/IHI0033B_AMBA5_AHB_AHB-Lite_spec.md", 1812, 1852)
show("amba/IHI0033C_AMBA_AHB_spec.md", 2088, 2125)
show("pcie/PCI_Express_Base_Specification_Revision_5.0.md", 3320, 3340)
