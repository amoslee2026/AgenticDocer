"""临时：P4 零改写保真核查（fragment 是否恒为源文本子串 + 逐块重建差异）。"""

import pathlib
import re

from agenticdocer.importer import parse_markdown

root = pathlib.Path("spec/standards")
for path in sorted(root.glob("*/*.md")):
    text = path.read_text(encoding="utf-8")
    result = parse_markdown(path)
    # frontmatter 之后的正文
    body_start = result.doc_meta["body_start"]
    body = "\n".join(text.split("\n")[body_start - 1 :])
    bad = []
    kept = 0
    for proposal in result.proposals:
        atom = proposal.atom
        fragment = getattr(atom, "content", {}).get("fragment") if hasattr(atom, "content") else None
        if fragment is None:
            continue
        kept += 1
        if fragment not in body:
            bad.append((proposal.proposal_id, proposal.rule_id, proposal.source_lines, fragment[:80]))
    # 重建：按 ordinal 序拼接 fragment（图片/交叉引用节点无 fragment：按 M04 口径另计）
    ordered = sorted(
        (p for p in result.proposals if hasattr(p.atom, "content")),
        key=lambda p: p.atom.ordinal,
    )
    rebuilt = "\n\n".join(
        str(p.atom.content.get("fragment") or f"<{p.atom.atom_type}>") for p in ordered
    )
    src_lines = [line for line in body.split("\n") if line.strip()]
    out_lines = [line for line in rebuilt.split("\n") if line.strip()]
    only_src = [line for line in src_lines if line not in out_lines]
    print(
        f"{path.name}: fragments={kept} 非子串={len(bad)} 正文字段一致={rebuilt.count('##')} 源行缺失={len(only_src)}"
    )
    for item in bad[:3]:
        print("   BAD", item)
    for line in only_src[:5]:
        print("   仅源有:", repr(line[:110]))
