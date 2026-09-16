#!/usr/bin/env bash
# fixture 验证：T3 ingested_at 过滤 + T2 INDEX 表解析（guard 兼容形式）
set -uo pipefail
cd /tmp/spec_plan_test

echo "=== T3: mapfile ingested_at 过滤 ==="
SRC_DIR=standards
mapfile -t FILES < <(find "$SRC_DIR" -name '*.md' -type f ! -name 'README.md' | sort | while IFS= read -r f; do grep -q '^ingested_at:' "$f" || printf '%s\n' "$f"; done)
echo "过滤后 count=${#FILES[@]}（预期 1：done.md 已带 ingested_at 被跳过）"
printf '  %s\n' "${FILES[@]##*/}"

echo "=== T2: INDEX 表 1 解析（awk + rg，guard 兼容）==="
mkdir -p spec/standards/pcie
cp standards/pcie/PCI_Express_Base_Specification_Revision_5.0.md spec/standards/pcie/
while IFS='|' read -r sid path; do
  test -f "spec/$path" || echo "K4 缺失: $sid -> $path"
  awk -v sid="$sid" 'NR==1{next} /^---[[:space:]]*$/{exit} $0 == "spec_id: " sid {found=1; exit} END{exit !found}' "spec/$path" || echo "K4 ID 不一致: $sid"
done < <(awk -F'|' '/^\| SPEC-/ {sid=$2; path=$3; gsub(/^[ \t]+|[ \t]+$/, "", sid); gsub(/^[ \t]+|[ \t]+$/, "", path); print sid "|" path}' INDEX.md)
echo "T2 完成（预期：真实文件无输出，不存在文件报两条 K4 缺失+ID 不一致）"
rm -rf spec
