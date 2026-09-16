"""临时：行级覆盖核查（零静默丢弃）+ fragment 行级保真（P4）。"""

import pathlib

from agenticdocer.importer import parse_markdown

root = pathlib.Path("spec/standards")
totals = {"lines": 0, "uncovered": 0, "frag_lines": 0, "bad_lines": 0, "nodes": 0}
for path in sorted(root.glob("*/*.md")):
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    result = parse_markdown(path)
    body_start = result.doc_meta["body_start"]
    body_lines = lines[body_start - 1 :]
    covered: set[int] = set()
    for proposal in result.proposals:
        start, end = proposal.source_lines
        covered.update(range(start, end + 1))
    uncovered = [
        (index + body_start, line)
        for index, line in enumerate(body_lines)
        if line.strip() and (index + body_start) not in covered
    ]
    # fragment 行级保真：每个 fragment 的每一行都应在源文本里逐字节出现
    body = "\n".join(body_lines)
    bad = []
    frag_lines = 0
    for proposal in result.proposals:
        atom = proposal.atom
        text_value = atom.content.get("fragment") if hasattr(atom, "content") else atom.text
        if not text_value:
            continue
        for line in str(text_value).split("\n"):
            frag_lines += 1
            if line.strip() and line not in body:
                bad.append((proposal.proposal_id, line[:80]))
    totals["lines"] += len(body_lines)
    totals["uncovered"] += len(uncovered)
    totals["frag_lines"] += frag_lines
    totals["bad_lines"] += len(bad)
    totals["nodes"] += len(result.proposals)
    print(
        f"{path.name}: 正文行={len(body_lines)} 未覆盖非空行={len(uncovered)} "
        f"fragment 行={frag_lines} 非保真行={len(bad)} 节点={len(result.proposals)}"
    )
    for item in uncovered[:4]:
        print("    未覆盖:", item)
    for item in bad[:4]:
        print("    非保真:", item)
print("TOTAL", totals)
