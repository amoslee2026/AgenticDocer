# 对抗性评审 issues — spec 集中目录建立 执行计划

- 评审对象：`docs/plans/2026-09-16-spec-central-directory.md`（对照 `idea/assumptions.md` A1–A13、`Notes/idea/芯片设计知识库-结构化文档方案-v0.1.md`）
- 评审日期：2026-09-16 · 方式：只读探查（GigaRAG / mySkills / GigaPie / Arion 实地核实，未改动任何既有文件）

---

## R1 · K2 必填字段数三处互斥（18 / 17 / 13），KPI 按字面不可判定

- **Severity**: HIGH
- **位置**: §Header KPI K2（L69）× §Task 5 Step 1（L661–670）× assumptions A9
- **问题描述**: K2「必填字段完整率」存在三个互斥定义：Header K2 = 「7 份 × 18 字段」；Task 5 Step 1 断言脚本实际检查 17 个字段（8 mySkills + 4 spec 专属 + 5 溯源）；A9 记为「13 字段」。「18」在全计划无任何字段清单可对应——唯一可能的第 18 项 `ingested_at` 被 A10 明确排除（本计划不执行摄入）。K2 按字面无法判定绿/不绿，「K1–K6 全绿」的完成定义因此不可签署，直接违反 A9 自定的量化铁律（「不可验收的目标不进入计划」）。
- **修复建议**: 统一为 17 字段——K2 改为「7 份 × 17 字段 = 100%（ingested_at 不计入：A10 本计划不摄入，导入后由脚本幂等追加）」，并同步修正 A9 的「13 字段」表述。

## R2 · `.gitignore`/计划文档/assumptions 全程无人提交，K5 与 Task 5「status 干净」判据自相矛盾

- **Severity**: HIGH
- **位置**: §Task 1 Step 1（L123）+ §Task 3 Step 3（L447）+ K5（L72）+ §Task 5 Step 3 判据（L691）
- **问题描述**: 全计划对 AgenticDocer 只有两笔提交：Task 1 Step 1 `git add Notes`、Task 3 Step 3 `git add spec/ scripts/`。`.gitignore`（Task 1 交付物）、`docs/plans/`（本计划自身）、`idea/assumptions.md`（A1–A13）没有任何 Task 提交，执行完毕后仍为 untracked。后果：(a) K5「AgenticDocer 全程 git 跟踪」不成立；(b) Task 5「status 干净（untracked 仅限本计划外文件）」不可满足——上述三者恰是本计划产物；(c) 计划与假设文档本身无版本兜底，违背 AGENTS.md「项目内文件先 commit 再修改」的可恢复性原则。
- **修复建议**: Task 1 Step 1 改为 `git add Notes docs idea`；Step 2 写完 `.gitignore` 后一并 `git add .gitignore`（或并入 Task 3 提交）；或在 Task 5 增加收尾提交 `git add -A && git commit -m "docs: spec 集中目录计划与假设记录入库"`。

## R3 · Task 1「幂等自证」在 Task 1 时点不可执行（仓库内无任何文件能产出 [skip]）

- **Severity**: MEDIUM
- **位置**: §Task 1 Exit criteria（L365–366）
- **问题描述**: 「脚本幂等自证：对任一文件连跑两次，第二次全部输出 [skip]」在该时点无文件可跑：仓库内 md 仅 3 份——Notes v0.1 无 frontmatter（脚本报 `[err] 无 frontmatter` 退出）；`spec/README.md` 与 `spec/INDEX.md` 有 frontmatter 但文件名不在 REGISTRY、无 spec_id（脚本报 `[err] 未在 REGISTRY 登记` 退出）。任何文件都到不了 `[skip]` 分支，冷启动执行者会卡住或误判脚本有缺陷。幂等自证实际最早在 Task 3 迁入 7 份文件后才能执行（Task 3 Exit criteria 已含「第二遍全部 [skip]」，与此处重复且时序错位）。
- **修复建议**: 删除 Task 1 的幂等自证条目（保留 `py_compile`），幂等判定统一由 Task 3 Exit criteria 承担；如需保留，改为「用 temp 目录下带最小 frontmatter 的 fixture 文件自证后删除」。

## R4 · KEEP_IN_PLACE 模式丢失「防重复入库」机制：收集段不过滤已导入文件

- **Severity**: MEDIUM
- **位置**: §Task 4 Step 2（L507）
- **问题描述**: 默认模式靠 mv 至 04_ingested 让已导入文件离开读源目录（GigaRAG README L14 明言 04_ingested「防重复入库」）。KEEP_IN_PLACE 模式文件原地保留，但新收集段 `find "$SRC_DIR" -name '*.md' …` 不过滤已带 `ingested_at` 的文件——权威源模式下每次运行都会把全部 7 份重新复制、重新 scan、重跑完整 pipeline（单批等待上限 MAX_WAIT=3600s），是否重复入库完全取决于 lightRAG 侧行为，脚本层无防护；`add_ingested_at` 的幂等只保护标记本身，不防止重复摄入。spec/README.md 又把该命令写成标准摄入入口，缺陷在首次实际摄入（A10 之后）即触发。
- **修复建议**: 收集段增加已导入过滤，例如：
  `mapfile -t FILES < <(find "$SRC_DIR" -name '*.md' -type f ! -name 'README.md' | sort | while IFS= read -r f; do grep -q '^ingested_at:' "$f" || printf '%s\n' "$f"; done)`；并在 scripts/README.md 环境变量段注明「已标记 ingested_at 的文件自动跳过」。

## R5 · K4 声称「引用路径存在率 100%」，断言实际只覆盖 2/9+ 条路径

- **Severity**: MEDIUM
- **位置**: §Header KPI K4（L71）+ §Task 5 Step 2
- **问题描述**: Task 5 Step 2 只验证 2 个外部目录（GigaPie/spec、Arion/spec/PRD）存在；表 1 的 7 条物理路径（INDEX 预写文件名与 Task 3 实际迁移结果是否一致）、表 1 spec_id 与各文件 frontmatter spec_id 的一致性、表 1「原始来源（GigaRAG）」列的 01_raw 子目录，均无断言。INDEX 系 Task 1 时点预写，若与迁移实况有任何笔误/漂移，K4 依旧全绿——KPI 声称的覆盖面与实际验证面不符。
- **修复建议**: Task 5 Step 2 补三条机械断言：(1) 逐条 `test -f spec/<表1路径>`；(2) 逐行比对 frontmatter `spec_id` 与表 1；(3) `test -d ~/wrk/GigaRAG/<原始来源列>`。

## R6 · 「双仓 status 干净」在 GigaRAG 侧不可机械判定（现存 42 条计划外未提交记录）

- **Severity**: MEDIUM
- **位置**: §Task 5 Step 3（L690–691）
- **问题描述**: 实测 GigaRAG 工作树当前已有 42 条未提交记录：含 7 个**已跟踪且已修改**的 `corpus/02_converted/**/auto/*.md`，以及大量 untracked（output/、HIPI2025/、.pi/、.skills_local/、logs/、refs/ 等），全部与本计划无关却混在同一 `git status --short` 输出里。「untracked 仅限本计划外文件」需人工逐条分类 40+ 条目，无机械判据，不同执行者会得出不同结论。
- **修复建议**: 把断言限定到本计划作用路径：`git -C ~/wrk/GigaRAG status --short -- scripts README.md corpus/03_reviewed corpus/04_ingested` 输出为空即判干净；AgenticDocer 侧在 R2 修复后可直接 `git status --short` 全量判空。

## R7 · 字段断言 grep 扫全文而非 frontmatter，且 glob 零匹配时空真通过

- **Severity**: LOW
- **位置**: §Task 5 Step 1（L661–670）
- **问题描述**: `grep -q "^${k}:" "$f"` 匹配整个文件：正文若出现行首同名 key（YAML 示例、代码块、语法段）会造成假阳性通过；`for f in spec/standards/*/*.md` 在 glob 零匹配时循环体不执行、直接输出「缺失总数: 0」（空真通过，仅靠 K1 兜底）。已实地核实当前 7 份文件 17 个 key 仅出现于 frontmatter L2–7，无现实误判——属防御性缺口而非现行 bug。
- **修复建议**: 改为先截取 frontmatter 再断言：`fm="$(sed -n '2,/^---$/p' "$f")"; printf '%s' "$fm" | grep -q "^${k}:"`；循环前 `shopt -s nullglob` 并断言实际检查文件数 = 7。

## R8 · INDEX 表 2 预写「3 版本」与实际不符（实测 2 个 md 版本）

- **Severity**: LOW
- **位置**: §Task 1 Step 4 · INDEX 表 2（L267）
- **问题描述**: REF-ARION-PRD 行预写「IO扩展芯粒整体设计方案（3 版本）」；实测 `~/wrk/Arion/spec/PRD/` 仅有 2 个 md 版本（`IO扩展芯粒整体设计方案-260810.md`、`…-260810-v2.md`，另有 .docx/.drawio 源件与 _assets/）。预写登记内容与事实不符，且 K4 不校验表 2 内容描述，错误将长期潜伏在权威索引里。
- **修复建议**: 改为「Arion_IODie_PRD.md、IO扩展芯粒整体设计方案（2 个 md 版本，另 docx/drawio 源件）」，或迁移时以实际盘点为准回填。

## R9 · A13 与计划风险表对降级场景的指令冲突（INDEX 标注 vs 保持不变）

- **Severity**: LOW
- **位置**: §风险与回退表第 3 行（L707）× assumptions A13
- **问题描述**: A13 规定缺 reviewed_by 时「status: review **并在 INDEX 标注**」；计划风险表却规定「INDEX 保持 approved 行不变，如出现 review 状态则人工复核」——降级场景下 INDEX 与文件 frontmatter 状态互相矛盾，且无机器/流程强制调和，两份文档指令冲突。实测 7 份文件 frontmatter 均含 `reviewed_by: lxx(批量导入授权)`（A13 的保守假设实际不成立，7 份全部将为 approved），该分支不会触发，属死分支矛盾。
- **修复建议**: 统一为 A13 语义——风险表缓解措施改为「脚本降级 status=review 时同步将 INDEX 对应行 status 改 review」；A13 可顺带更新为已实证结论（7/7 均有 reviewed_by）。

## R10 · spec/README.md 引用「v0.1 §4.5 公共字段」出处错位且字段非纯落地

- **Severity**: LOW
- **位置**: §Task 1 Step 3 · 字段表（L210）
- **问题描述**: 「spec_id / spec_type / spec_org / spec_revision 是 v0.1 §4.5 公共字段的文件级落地」——v0.1 的公共字段清单实际位于 §4.4 末段（id / version / status / traces_to / source_ref），§4.5 是「逐类型 Schema 字段建议」；且公共字段中并无 spec_org / spec_type 的对应项，二者属计划新增而非「落地」。规范性 README 中的出处引用无法核对到原文。
- **修复建议**: 改为「参考 v0.1 §4.4 公共字段（id / version / status / source_ref）的文件级落地，并新增 spec_org / spec_type」。

---

## 已核实无问题的点（覆盖说明）

- **事实一致性**：7 份文件名与 Task 3 mv 命令、INDEX 表 1 路径、REGISTRY 键逐一相符；01_raw 子目录（pcie/cxl/hbm/amba）与 INDEX「原始来源」列、各文件 `source` 字段一致。
- **脚本可运行性**：7 份文件均合法 UTF-8、无 NUL、LF 行尾——`read_text(encoding="utf-8")` 与 `FM_RE` 匹配无障碍（file(1) 对 IHI0022K 报 "data"，字节级校验通过，非编码问题）；升级脚本对 7 份文件恰补 11 字段、合计 17 字段零缺失（`title` 已存在于全部文件）。
- **元数据合法性**：status 枚举（draft/review/approved）、type=composite 下 purpose=spec/readme、audience=both、direction=input、version 必填——均符合 mySkills meta-fields §1/§1.1；INDEX 取 purpose: readme 与 A11 一致。
- **补丁锚点**：Task 4 五处「原→改」引文与 ingest.sh 实际代码（L2 / L13–16 / L51–59 / L79–88 / L135–139）逐字相符；DRY_RUN 门位于联网检查之前，与 `set -euo pipefail` 无不良交互；`SRC_BY_BASE` 声明先于使用；`wait_and_ingest.sh` / `stage_unverified.py` 确无 03_reviewed 引用（风险表断言成立）。
- **前置条件**：GigaRAG 为 git 仓（03_reviewed/README.md 已跟踪、7 份 md untracked、.gitignore 不拦截 03_reviewed），Task 2 exit criteria 可达成；git user.name/email 已配置；uv 与 python3 在位。
- **可恢复性**：mv 为同文件系统操作、K6 零删除成立；升级失败可从 GigaRAG Task 2 提交恢复（`git show HEAD:路径 > 文件`），回退路径闭合。

## 结论

存在 6 个阻塞问题（R1、R2、R3、R4、R5、R6）
---

## 复核记录（2026-09-16 · 修复后二审）

对 Main 按 R1–R10 修复后的 plan（730 行）与 assumptions.md 逐条复核：

- **R1 部分闭环**：Header K2（L69）与 A9 已统一为 17 字段 ✓，但 Task 3 Exit criteria **L460 仍残留「18 项必填字段零缺失」**——与 17 处口径不一致（K2 可判定性已恢复，残留为验收条目标签错误）。修复：L460 改「17 项必填字段零缺失」。
- **R2–R10 全部闭环**：R2（Step 1 `git add Notes docs idea` + 新增 Step 2b 提交 .gitignore + Exit criteria 2 条提交；`git add idea` 会一并入库本评审目录，.skills_local 已被 ignore，Task 5 判空可达）；R3（幂等自证条目已删，由 Task 3 承担）；R4（收集段 `grep -q '^ingested_at:'` 过滤，grep 处于 `||` 列表无 errexit 风险，spec/README 与 scripts/README 同步说明，「DRY_RUN 列出的即实际待导入集合」语义自洽，默认模式回归不受影响）；R5（awk 解析表 1 `^\| SPEC-` 行取 sid/path、逐条 `test -f`、spec_id 精确字符串匹配断言、01_raw 根目录断言 + 2 外部目录，表 2 REF- 行正确排除，K4/A9 措辞同步）；R6（GigaRAG 断言限定 `-- scripts README.md corpus/03_reviewed corpus/04_ingested`）；R7（nullglob + 文件数=7 守卫 + awk 截取 frontmatter 区断言）；R8（Arion 行改 2 个 md 版本 + docx/drawio 源件，与实测一致）；R9（风险表「同步将 INDEX 对应行 status 改为 review」与 A13 一致，A13 更新为实证 7/7）；R10（改引 §4.4 公共字段，spec_type/spec_org 标注为本目录新增扩展）。
- **两处执行层修正复核无新问题**：awk 精确匹配解析 INDEX（列切分/去空白对表 1 结构正确）、printf 管道断言（guard 放行形式）均正确。
- **新引入问题**：无阻塞项。非阻塞备注：(a) 原始来源断言为根目录粒度（corpus/01_raw/specifications）而非逐行子目录——可接受，INDEX 注明以 frontmatter `source` 为准且 Task 3 保证 source 原样保留；(b) 本 issues.md 的行号锚点对应修复前版本（712 行），修复后 730 行，评审快照性质无需回改。

**二审结论**：R1 残留 1 处（L460「18 项」需改「17 项」），其余全部闭环；该残留为一字修复，修完即无阻塞问题。
