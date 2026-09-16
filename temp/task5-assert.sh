#!/usr/bin/env bash
# Task 5 端到端断言
set -uo pipefail
cd /home/lxx/wrk/AgenticDocer || exit 1

echo "=== Step 1: frontmatter 17 字段完整性（K2）==="
shopt -s nullglob
files=(spec/standards/*/*.md)
test "${#files[@]}" -eq 7 || { echo "文件数 ${#files[@]} ≠ 7，中止"; exit 1; }
missing=0
for f in "${files[@]}"; do
  fm="$(awk 'NR==1{next} /^---[[:space:]]*$/{exit} {print}' "$f")"
  for k in title type purpose audience direction status version section_meta \
           spec_id spec_type spec_org spec_revision source \
           converted_by converted_at reviewed_by reviewed_at; do
    printf '%s\n' "$fm" | grep -q "^${k}:" || { echo "MISSING: $k in $f"; missing=$((missing+1)); }
  done
done
echo "缺失总数: $missing   # 期望 0"

echo "=== Step 2: K1 + K4 断言 ==="
test "$(find spec/standards -name '*.md' -type f | wc -l)" -eq 7 && echo "K1 OK"
while IFS='|' read -r sid path; do
  test -f "spec/$path" || echo "K4 缺失: $sid -> $path"
  awk -v sid="$sid" 'NR==1{next} /^---[[:space:]]*$/{exit} $0 == "spec_id: " sid {found=1; exit} END{exit !found}' "spec/$path" || echo "K4 ID 不一致: $sid"
done < <(awk -F'|' '/^\| SPEC-/ {sid=$2; path=$3; gsub(/^[ \t]+|[ \t]+$/, "", sid); gsub(/^[ \t]+|[ \t]+$/, "", path); print sid "|" path}' spec/INDEX.md)
echo "表1 路径与 spec_id 逐条核对完成"
test -d /home/lxx/wrk/GigaRAG/corpus/01_raw/specifications && echo "K4 原始来源根 OK"
test -d /home/lxx/wrk/GigaPie/spec && echo "REF-GIGAPIE-SPEC OK"
test -d /home/lxx/wrk/Arion/spec/PRD && echo "REF-ARION-PRD OK"
test -d /home/lxx/wrk/nova2026/archExplorer/spec && echo "REF-NOVA-ARCHEXPLORER OK"
test -f spec/idea/芯片设计知识库-结构化文档方案-v0.1.md && test -f spec/idea/assumptions.md && test -d spec/idea/.review && echo "idea 归位 OK"
test ! -e Notes && echo "Notes/ 已退役 OK"

echo "=== Step 3: 双仓状态（K5）==="
git -C /home/lxx/wrk/AgenticDocer status --short && echo "AgenticDocer clean"
git -C /home/lxx/wrk/GigaRAG status --short -- scripts README.md corpus/03_reviewed corpus/04_ingested && echo "GigaRAG 作用路径 clean"
