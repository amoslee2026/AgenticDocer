"""临时：对 7 份真实语料跑解析并汇总裁决数据。"""

import pathlib
import time

from agenticdocer.importer import parse_markdown, report

root = pathlib.Path("spec/standards")
total_blocks = covered = fallback = proposals = 0
atom_totals: dict[str, int] = {}
rows = []
for path in sorted(root.glob("*/*.md")):
    started = time.perf_counter()
    result = parse_markdown(path)
    summary = report(result)
    elapsed = time.perf_counter() - started
    stats = result.stats
    total_blocks += stats.total_blocks
    covered += stats.rule_covered
    fallback += stats.fallback
    proposals += len(result.proposals)
    for kind, count in summary["atom_types"].items():
        atom_totals[kind] = atom_totals.get(kind, 0) + count
    rows.append((path.name, stats.total_blocks, stats.rule_covered, stats.fallback, len(result.proposals), summary["coverage"], elapsed, summary["asset_refs"]))

print(f"{'file':50s} {'blocks':>7s} {'covered':>7s} {'fallback':>8s} {'props':>6s} {'cov':>7s} {'sec':>5s}")
for name, blocks, cov, fb, props, ratio, sec, assets in rows:
    print(f"{name:50s} {blocks:7d} {cov:7d} {fb:8d} {props:6d} {ratio:7.4f} {sec:5.2f}  refs={assets.get('total')}(md={assets.get('md')},html={assets.get('html')},uniq={assets.get('unique')})")
print()
print(f"TOTAL blocks={total_blocks} covered={covered} fallback={fallback} proposals={proposals} "
      f"coverage={covered / total_blocks:.4f} fallback_ratio={fallback / total_blocks:.4f}")
print("atom_types:", atom_totals)
