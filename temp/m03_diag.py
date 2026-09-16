"""临时：诊断 fallback 区块 / definition 分布 / 被误判的表。"""

import collections
import pathlib

from agenticdocer.importer import parse_markdown, report

root = pathlib.Path("spec/standards")
for path in sorted(root.glob("*/*.md")):
    result = parse_markdown(path)
    defs = [p for p in result.proposals if p.atom.atom_type == "definition"]
    rules_of_defs = collections.Counter(p.rule_id for p in defs)
    print(f"\n### {path.name}: definitions={len(defs)} {dict(rules_of_defs)}")
    print("   未映射：")
    for item in result.unmapped:
        block = None
        for p in result.proposals:
            if p.source_lines == item.source_lines:
                block = p
        preview = ""
        if block is not None:
            preview = " ".join(str(getattr(block.atom, "text", ""))[:90].split())
        print(f"   行 {item.source_lines[0]}-{item.source_lines[1]} {item.fallback.atom_type}/{item.fallback.format} :: {preview}")
    print("   definition 样例：")
    for p in defs[:3]:
        print("   ", p.rule_id, p.atom.atom_type, "|", " ".join(str(p.atom.content.get("text", ""))[:70].split()))
    for p in defs[-3:]:
        print("   ..", p.rule_id, p.atom.atom_type, "|", " ".join(str(p.atom.content.get("text", ""))[:70].split()))
