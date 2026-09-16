---
title: it.idea 五份产物对抗评审问题清单
type: composite
purpose: review
audience: both
direction: input
status: review
version: "1.0.0"
section_meta: "@meta"
---

# it.idea 产物对抗评审 · issues.md

评审对象（`spec/idea/`）：`design_doc.md`、`approach_analysis.md`、`trade_off_matrix.md`、`clarifications.md`、`summary.md`；对照源：`芯片设计知识库-结构化文档方案-v0.1.md`（含 §4.4 原子表、§5.1 不做清单、§9 已定事项）。

严重度：**CRITICAL** = 阻塞 it.arch 交接、且对 100% 试点语料成立；**HIGH** = 模块契约/数据完整性高影响；**MEDIUM** = 真实缺陷，需修但不改变总体方案；**LOW** = 文档准确性/信息项。阻塞 = CRITICAL + HIGH + MEDIUM。

## 证据基线（本机实测 2026-09-16，只读核实）

- 语料 `spec/standards/` 7 文件合计 **8,812,225 B（≈8.8MB）**、75,694 行；标题行合计 5,954（CXL 2,666 / PCIe 2,097 / AMBA-AXI 506 / HBM4 389 / AHB-C 131 / AHB-Lite-B 115 / APB 50）。
- 表格形态：以 `|` 开头的行 **0**（无 GFM 竖线表格）；`<table>` **2,440**、`<tr>` **19,763**、`<td>` **79,817**，其中 **57,005** 个单元格带 `colspan/rowspan/bgcolor/align` 属性；含 `<sup>` 的行 239 行。
- 图片：`images/<sha256>.jpg` 形式引用 **1,019 处**（去重后仍 1,019 个）；AgenticDocer 仓库内 `*.jpg` 文件 **0** 个；同批图片实物在 GigaRAG `corpus/02_converted/specifications/*/auto/images/`。
- 标题重复（锚冲突实证）：CXL 单文件内 219×「Test Steps:」、217×「Fail Conditions:」、214×「Pass Criteria:」、170×「Prerequisites:」、59×「IMPLEMENTATION NOTE」；PCIe 154×「IMPLEMENTATION NOTE」；HBM4 21×「Wrapper Data Register」等；AMBA-AXI 存在 2×「Part C Glossary」。
- lightRAG：`lightrag-hku` 安装于 `/home/lxx/.local/share/uv/tools/lightrag-hku/lib/python3.11/site-packages/lightrag/kg/{postgres_impl.py,pgtable_impl.py}`（Q1 引用属实）；现运行形态为 JSON 文件模式（`/home/lxx/lightrag/rag_storage`）。
- GigaRAG：`scripts/ingest.sh` L9 默认 `LIGHTRAG_INPUT_DIR=/mnt/big10T/lxx/lightrag/inputs`；摄入源对 `$SRC_DIR` 做**递归 `*.md` 扫描**（仅排除 README.md；命中 `^ingested_at:` 即跳过；basename 重复直接 ERROR 退出）。GigaRAG README L5 原文为「只入库人工转换 + 人工审核通过的文档。自动解析（PDF/Word 直转）质量不可控，禁止直接入库」。
- AGENTS.md：`~/.pi/agent/AGENTS.md` L26「不保留向后兼容」、L108「测试覆盖率 99%」；`~/.omp/agent/AGENTS.md` L20/L78 同义（C6 与 §8 引用属实）。
- `spec/README.md`（移交流程、frontmatter v2 17 字段、⛔ 摄入暂缓）、`spec/INDEX.md`（表 1 七条）与五份产物陈述一致；`AgenticDocer/docs/` 为空目录。

---

## E1 HTML 表格与内联标记无原子/渲染策略，§10 断言在指定语料上不可实现

- **Severity**: CRITICAL
- **位置**: `design_doc.md` §5 数据模型 nodes 行（L124）、§10 测试策略（L226）
- **问题描述**: 语料中表格 **100% 为 HTML 标记**（0 行竖线表格；`<table>` 2,440、`<tr>` 19,763、`<td>` 79,817，57,005 个单元格带 `colspan/rowspan/bgcolor/align`），另有内联 `<sup>/<br>` 等。而 §5 的八类原子（`clause`/`definition`/`table`〔+`register_field`〕/`figure`/`code`/`example`/`note`/`cross_ref`）与 M03 解析提议、M06 结构化写入、M09 lint、M04 渲染全链路都没有「HTML 表格 / 内联标记」的表达位；§10 却断言「表格行列数还原」。执行者两条路都走不通：结构化拆解（属性、嵌套标记、`<sup>` 序列无处安放）或原文透传（无 raw 原子类型）。触发条件 = 解析任一试点的表格（100% 命中），影响阶段 1 里程碑「7 份语料全链路往返」不可达，P1「格式合规由渲染层确定性保证」在此类内容上失效。
- **修复建议**: 二选一并写死在 design_doc：(a) 增 `table.html` 子类型——`content` 存原样 HTML 片段 + 解析出的行列数元数据，规定 M04 原样回写、M09 按 HTML 结构断言行列数；(b) 定义 HTML→结构化单元格字段映射（含 `colspan/rowspan/align` 字段）与渲染还原规则。无论哪种，§10 断言应改为「行列数与单元格文本保真（非字节）」，并覆盖 `<sup>/<br>` 等内联标记。

## E2 图片/附件资产策略缺失（1,019 处引用、权威源内 0 个实物）

- **Severity**: HIGH
- **位置**: `design_doc.md` §5 数据模型（L122-124）、§7 集成边界（L199）
- **问题描述**: 语料含 1,019 处 `images/<sha256>.jpg` 引用，而 `spec/standards/` 及整个 AgenticDocer 仓库内图片文件数为 **0**（实物留在 GigaRAG `corpus/02_converted/.../auto/images/`）。数据模型既无资产表/文件存储，`figure` 原子也无 asset/path 字段；§7 只定义导出格式、不定义渲染产物落盘位置与图片链接重写/复制规则；§10 断言不含图。触发条件 = 解析/渲染任一含图文档（7 份中 6 份命中）：M03 对 1,019 处引用无处置依据，M04 渲染产物必然含死链，「结构化库=唯一权威源、渲染产物可读」不成立。
- **修复建议**: §5 增补资产模型（`assets` 表或 content-addressed 文件存储 + `figure.content.asset_ref`）；§7 增一行「渲染产物落盘目录 + 图片相对路径重写/复制规则（含 source-of-truth 与 GigaRAG images 目录的同步策略）」；§10 增加「图片引用保真」断言。

## E3 refs / schemas 写入无事件覆盖，违反「一切写入走 events」

- **Severity**: HIGH
- **位置**: `design_doc.md` §5 数据模型 refs/events 行（L125-126）、版本与 diff 段（L132）
- **问题描述**: L132 声明「一切写入走 M06/M07 → 先写 `events`」，但 `events.entity` 枚举仅 `doc/node/comment`：`refs`（引用边）与 `schemas` 的创建/删除没有任何事件形态。跨边界后果：引用边是 S2（版本与结构化 diff）与 M-LR（「增量由 events 驱动」，§7 L198）的输入之一，refs 变更既不会出现在 M07 的历史/结构化 diff 中，也不会触发 M-LR 增量——属静默丢弃。触发条件 = 任何引用边新增/删除（M03 导入 `source_ref`/`cross_ref`、agent 维护 `traces_to` 均命中）。
- **修复建议**: 二选一：(a) `entity` 扩为 `doc/node/ref/comment/schema`，并定义 ref 事件 payload（`src/dst/kind` 增删）；(b) 明确 refs 为 nodes.content 的派生表（`traces_to`/`see_also` 等字段写在节点 JSONB 内），并规定节点事件 payload 覆盖 refs 重建所需字段。同时修正 L132 的「一切写入」表述或补齐 schemas 事件语义。

## E4 模块依赖与实施顺序自相矛盾（M03/M06 依赖 M09；M09 输入定义无法服务入库前校验）

- **Severity**: HIGH
- **位置**: `design_doc.md` §4 模块表（L84-93，M09 行 L96）、§12 实施顺序
- **问题描述**: 三处定义互斥：(1) L84 不变量「依赖只许向下（后编依赖前编）」；(2) 模块表把 M03（L90）、M06（L93）的依赖列为含 M09；(3) §12、`clarifications.md` B14（L64）、`approach_analysis.md`（L79-81）一致把 M09 排到最后的「增值」阶段。且 M09 边界定义为「节点/文档 → 违规清单」（已落库实体），无法服务 M03 声明的「入库前」提议校验——即 M03 声明的依赖对象在时序与语义上都不存在。后果：it.mas 无法据同一份 design_doc 生成自洽的依赖序与接口。
- **修复建议**: 把「提议级 schema 校验（入库前）」写入 M03 边界（复用 M01 的 schema 定义），M09 仅对已落库实体做 lint；同步修正 L84 不变量措辞、模块表依赖列、§4 依赖图（现缺 M03 的 M01/M09 入边）与 §12/B14 顺序，或明示 M09 分两阶段交付（校验规则库随 M01/M03 先行）。

## E5 events 与当前态的一致性机制缺失（事务/并发/快照/校验）

- **Severity**: MEDIUM
- **位置**: `design_doc.md` §5 版本与 diff 段（L130-132）、§4 M09 行（L96）
- **问题描述**: 「先写 events 再更新实体当前态」（L132）未定义事务边界与失败恢复，实体表（L122-128）无 version/乐观锁列，「快照」无表/策略定义，M09 的校验类别（L96：schema/断链/术语/渲染）也不含 events↔当前态一致性。触发条件：M06（agent 自修复闭环重写）与 M07（WebUI 编辑）并发写同一节点——后写者基于陈旧读取计算字段级 diff，造成当前态丢失更新且事件日志无法自证；或进程在两次写入之间中断留下撕裂状态且无检测/修复路径。
- **修复建议**: 明确「事件+实体同事务提交」；实体表增 `version` 列并在写入路径做乐观锁（冲突返回可重试错误）；定义快照策略（写时或周期）与启动期/巡检式一致性校验，把「events↔当前态差异」纳入 M09 违规清单。

## E6 批注与版本历史无锚定关系，节点删除后批注悬空

- **Severity**: MEDIUM
- **位置**: `design_doc.md` §5 comments 行（L127）、§6.3 评审流
- **问题描述**: `comments` 仅有 `node_id`+`state`，无 revision/event 锚。节点被更新 N 次后，「该批注针对哪一版正文」不可知；`clarifications.md` S6（L30）同时要求「版本历史」与「批注」，但历史版本视图如何呈现对应批注无定义；`events.op=delete` 后 `comments.node_id` 的处置（级联/孤儿/冻结）未定义。触发条件 = 任一被批注节点发生第二次更新或删除（P3 的常态路径）。
- **修复建议**: `comments` 增 `target_event_id`（或 node revision）字段，规定批注锚定创建时的节点版本；规定节点删除时批注保留并标记 `orphaned`；在 WebUI 功能规格中定义历史视图的批注呈现规则。

## E7 条款层级未建模、锚唯一性与稳定性规则不足

- **Severity**: MEDIUM
- **位置**: `design_doc.md` §5 nodes 行（L124）、ID 方案（L130）
- **问题描述**: nodes 无 parent/path/level 字段，层级只隐含在 anchor 字符串内，而 §10 断言「条款标题/层级还原」——层级还原无数据依据。锚规则「按章节路径生成，冲突时加序号后缀」（L130）在语料上不可靠：CXL 单文件内 219×「Test Steps:」（另 217/214/170/59 组重复）、PCIe 154×「IMPLEMENTATION NOTE」、HBM4 21×「Wrapper Data Register」，且存在无编号标题（AMBA「Chapter A2」「Part C Glossary」「AMBA SPECIFICATION LICENCE」）。序号后缀会随章节插入/删除漂移，而 B8（L58）把 (uuid, alias) 作为引用表达 → alias 不稳定即人工引用与追溯展示不稳定。
- **修复建议**: 增 `parent_node_id`（或 level+path）字段；把 anchor 定义为与插入位置无关的确定性构造（章节号 + 重复项内容哈希消歧）；写明源文档改版重解析后 anchor 的稳定性承诺与迁移规则。

## E8 M02/M05 边界重叠、检索语义未定义

- **Severity**: MEDIUM
- **位置**: `design_doc.md` §4 模块表（L89、L92）、§6.4 检索流（L189）
- **问题描述**: M02 边界已含「查询结果」，M05 又输出「查询（ID/关键词/多跳 refs）→ 结果集」，两者仅以「依赖 M02」相连——多跳递归查询（SQL CTE）、关键词检索（PG FTS / trigram / LIKE 未定，索引未定）的实现归属无定义。§6.4 仅给「默认 ≤2 跳」，未定义：哪些 `refs.kind`（`traces_to`/`see_also`/`composes_from`/`source_ref`）参与扩展及其方向（上游/下游/双向）、环与重复节点处理、命中排序与证据截断规则。D1「多跳 ≤2 跳可纯 SQL 递归 CTE」的结论因此没有承接方。
- **修复建议**: 在 §4 划定 M02=原子 CRUD+点查、M05=图遍历与检索语义；§6.4 写明每种 kind 的遍历方向与是否参与多跳、跳数语义、去重/排序规则、关键词检索实现选型与索引。

## E9 M04/M09 渲染校验职责重叠；术语与 schema 版本来源缺失

- **Severity**: MEDIUM
- **位置**: `design_doc.md` §4 模块表（L96）、§10（L228）
- **问题描述**: M04 边界自带「（往返一致）」属性、§10 又给 M04 配往返测试，而 M09 职责亦含「渲染一致性」——同一保证有两个执行者，谁是对外门禁未定义。M09 的「术语」校验无术语表/规则来源（数据模型无 glossary/terms 资产，`definition` 原子未规定可被 M09 消费的字段）。schemas 表（L128）的 `version` 与 nodes 无绑定：schema 演进后旧节点用哪版 schema 复审无规定（C6 允许直接演进，但复审口径缺失）。
- **修复建议**: 明确 M09 违规类别与判定来源（schema 违规 ← M01 schemas；断链 ← refs；术语 ← 新增术语/规范性关键词表；渲染一致性 ← 消费 M04 的往返比对结果，不重复计算）；nodes 增 `schema_version` 或写明「一律按当前 schema 复审」。

## E10 M03 半自动流程定义缺口（置信度、审核载体、未映射内容兜底）

- **Severity**: MEDIUM
- **位置**: `design_doc.md` §6.1 导入流（L146-148）、§4 M03 行（L90）
- **问题描述**: 流程给出「提议清单（逐原子 + 置信度）」「高置信段可批量自动通过」（B11 回退）「拒绝/修正 → 回退提议」，但全文未定义：置信度如何产生与阈值（解析器是确定性规则，无概率来源）；审核交互载体——只有 `trade_off_matrix.md` D7 提到「CLI 先行」，设计正文与模块表没有任何 CLI 组件或接口；解析器无法映射到八类原子的内容（HTML 表格、内联标记、目录/许可/免责声明等 boilerplate）如何处置（丢弃/降级/原文残留）——而这一处置直接决定 §10「零丢失率」的分母。it.mas 无法据此实现 M03。
- **修复建议**: 在 design_doc 增设 M03 小节：置信度定义与阈值（或明确取消该字段）、审核载体（CLI 命令面或复用 M07 API）与批量通过规则、未映射内容的兜底策略（建议 raw/note 降级并计数），并与 §10 断言对齐。

## E11 B10 规模量化与指定语料规模相互否定

- **Severity**: MEDIUM
- **位置**: `clarifications.md` B10（L60）、§1 S7；`design_doc.md` §1（L30）
- **问题描述**: B10 量化「单库 ≤10k 节点、≤200 份文档」，但指定 fixture 仅 7 份文档的最小原子数已 ≈9.4k（标题 5,954 + 表格 2,440 + 图 1,019），再计入 definition/note/cross_ref 必然超限——验收目标被自身 fixture 否定；Q4/D6（条款级 vs 段落级）未裁决，取段落级将成倍放大。同一量级还是 D1「纯 PG 足够、无需分区/缓存」的依据，失真会连带影响存储结论的论证链。
- **修复建议**: 按实测上修 B10（并注明粒度前提「以条款级为基线」），给出节点数估算式（标题 + 表格 + 图 + 定义/注释 + 预留系数），并与 Q4/D6 联动；同步修正 summary/design 中引用 B10 的表述。

## E12 渲染产物落盘/双权威源未定义，且与 GigaRAG ingest 递归扫描冲突

- **Severity**: MEDIUM
- **位置**: `design_doc.md` §7 集成边界（L197-199）、§9 部署
- **问题描述**: 设计未定义渲染产物的落盘目录与写回策略，而 `spec/standards/` 已被既有 `ingest.sh` 约定为摄入源且**递归扫描**（仅跳过 README.md 与带 `ingested_at` 者，basename 重复直接报错退出）。后果二选一皆不自洽：(a) 渲染产物落回 `spec/` 下 → C7 解禁后会被 ingest 递归拾取，与 §7「增量由 events 驱动」的 M-LR 通道形成双入口，重复/冲突入库（且同名文件会令 ingest 直接失败）；(b) 落在别处 → `spec/standards/` 原 markdown 与 DB 成为双权威源，P1「唯一权威源」不成立。
- **修复建议**: 在 §7/§9 明确渲染产物输出目录（置于 ingest 扫描范围之外，或声明渲染产物为只读派生、不落 spec/），并写明 C7 解禁后 ingest 与 M-LR 的唯一入口约定与去重口径。

## E13 §10 关键断言不可机械执行、覆盖不全

- **Severity**: MEDIUM
- **位置**: `design_doc.md` §10 测试策略（L226-230）
- **问题描述**: (a)「零丢失率 ≥ 目标值（量化于 it.test-plan）」——目标值后置且「丢失」无定义（对 HTML 表格/图片/boilerplate 无法判定），当前不可验收；(b)「渲染产物与源 markdown 的语义一致性（结构断言，非字节 diff）」——未定义可比对的规范化中间表示与判定规则，「语义一致」无执行者口径；(c) 断言清单不含 figure/图片与内联 HTML（见 E1/E2）；端到端仅「一次结构化修改 + 一次评审动作」，未覆盖 S2/S6 的 events 重放/历史视图、批注生命周期、断链检测等可观测结果。
- **修复建议**: 用可执行判据替换：(a)「解析提议覆盖率 = 被原子承接的源块数 ÷ 总源块数」并给目标值；(b) 定义 `render(parse(src))` 与 `src` 的规范化表示（标题序列 / 表格行列与单元格文本 / 代码块 / 图片引用 / 列表）等价；(c) 补 figure/内联标记与 events、批注路径的断言项。

## E14 M01「文档类型组合规则」与 schema 版本绑定无模型

- **Severity**: LOW
- **位置**: `design_doc.md` §4 M01 行（L88）、§5 schemas 行（L128）
- **问题描述**: M01 边界承诺输出「文档类型组合规则」，但持久化仅 `schemas(type_name/json_schema/version)`，无「doc_type → 允许的原子类型/必填字段」模型；M03 校验与 M09 lint 若要按文档类型判定合法性则无处取数。C6 允许直接演进，但文档未声明该能力是否延后。
- **修复建议**: 在 schemas 增 `doc_type` 组合定义（或新增 doc_types 表），或明示「组合规则随首个非 standard 类型引入时定义」并标注开放问题编号。

## E15 trade_off 加权总分算术错误

- **Severity**: LOW
- **位置**: `trade_off_matrix.md` §1（L27-29）；`summary.md`（L24）
- **问题描述**: 按表内权重与分值复算，A = (100+100+75+75+30+50+15)/100 = **4.45**（文档写 4.55）、B = 300/100 = **3.00**（写 2.90）、C = 325/100 = **3.25**（写 3.30）；summary 引用了同一组数字。结论（A 胜出）不变，但决策矩阵不可复算。
- **修复建议**: 按行分值重算并统一 §1 表格、计算行与 summary 引用（A 4.45 / B 3.00 / C 3.25）；或删除计算式、在表内注明分值仅作相对比较。

## E16 语料体积陈述与实测不符（11.4MB vs 8.8MB）

- **Severity**: LOW
- **位置**: `design_doc.md` §1（L30）；`summary.md`（L48）
- **问题描述**: 两处称语料「≈11.4MB」，实测 7 文件合计 8,812,225 B ≈ 8.8MB（du 8.5MiB）。该数字是规模/存储估算与 B10 讨论的输入，重复出现在两份产物中。
- **修复建议**: 统一改为实测值（≈8.8MB / 7 文件），或注明口径（例如是否含图片资产；图片实物在 GigaRAG 侧，若纳入需另计）。

## E17 v0.1 §5.1 引用不准确（「全自动 PDF 直转」不在该清单）

- **Severity**: LOW
- **位置**: `design_doc.md` §2 范围（L35）；`clarifications.md` §1 out of scope（L33）
- **问题描述**: 「范围外（v0.1 §5.1 明示不做）」列了 5 项，其中前 4 项与 v0.1 §5.1 一致，但「全自动 PDF 直转」不在 §5.1 不做清单内（其依据实为 GigaRAG README L5 原则与 B11）。下游 it.arch 会把该条当作 v0.1 已声明边界继承，来源错标会掩盖真实依据。
- **修复建议**: 拆开引用：4 项标 v0.1 §5.1；「全自动 PDF/markdown 直转」改标 B11 + GigaRAG README L5。

## E18 v0.1 §9 已定决策（verification plan 对齐 UCIS/vPlan）未继承且未声明延后

- **Severity**: LOW
- **位置**: `clarifications.md` B7（L57）、§1 out of scope（L33）；`design_doc.md` §2
- **问题描述**: v0.1 §9 将「verification plan 对齐 Accellera UCIS / vPlan 格式导入导出」列为已确定事项；五份产物全文检索无 UCIS/vPlan 匹配，亦未声明「随 product/verification 类型延后」。属未声明偏离，交接给 it.arch 时该决策将静默丢失。
- **修复建议**: 在 clarifications 范围外或 design_doc §2 增一行：「v0.1 §9 的 UCIS/vPlan 对齐适用于 verification plan 类型，随 B7 逐类型扩展时落地（当前不实现）」。

## E19 clarifications §0 悬空引用（docs/plans 计划文件不存在）

- **Severity**: LOW
- **位置**: `clarifications.md` §0（L18）；`design_doc.md` §9（L217）
- **问题描述**: 引用 `../..//docs/plans/2026-09-16-spec-central-directory.md`，该路径不存在——`AgenticDocer/docs/` 为空目录，全仓库无 `*central-directory*` 匹配文件；同句 `assumptions.md` 存在。design_doc §9 亦把「docs/ 计划」列为既有布局。执行者按图索骥会落空。
- **修复建议**: 改为指向实际留底位置（如 `spec/idea/.review/archive/` 或 git 历史 commit）或删除该引用；同步修正 design_doc §9 布局描述。

## E20 LightRAG 运行形态表述与实测不一致

- **Severity**: LOW
- **位置**: `design_doc.md` §3 架构图（L46）；`summary.md`（L35）
- **问题描述**: 架构图把 LightRAG 直接标注为「同 PG 实例，`LIGHTRAG_*` 表」，实测为 JSON 文件模式（storage=`/home/lxx/lightrag/rag_storage`），PG 后端仅为代码能力、尚未迁移；summary 的正确表述（「运行中（JSON 文件模式）…迁移为后期配置变更」）与图不一致。若 it.arch 继承图述现状，会误判联调前置条件（需先完成存储迁移与双写/重建策略）。
- **修复建议**: 图注改为「LightRAG 语义索引（现为 JSON 文件模式；迁移后：同 PG 实例、`LIGHTRAG_*` 表）」，并在 §7 补一行迁移前置条件。

---

## 结论

阻塞项 13 个（CRITICAL 1 + HIGH 3 + MEDIUM 9）；另有 7 个 LOW 信息项不计入阻塞。最高优先级：E1（HTML 表格无原子/渲染策略，阶段 1 往返里程碑不可达）、E2（图片资产策略缺失）、E3（refs 无事件覆盖）、E4（模块依赖/顺序自相矛盾）。

存在 13 个阻塞问题（E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13）

---

# 复核（闭环验证，2026-09-16）

复核对象：`design_doc.md` v1.1.0、`clarifications.md`、`trade_off_matrix.md`、`summary.md`（均已修订）、`approach_analysis.md`（未修订）、`plan-spec-central-directory.md`（新增，745 行/34,573 B，已核验为原计划文档）。

## 逐项结论（E1–E20）

| 原 issue | 结论 | 核验点（改后文档位置） |
|---|---|---|
| E1 | 闭环 | §5.1 选定方案(a)：`table.format=html` + `content.fragment` 原样 + `content.meta{rows,cols,cells,max_colspan}`；M04 零改写回写；M09A 仅校验片段闭合与元数据一致；§10 断言改为「行列数与单元格文本保真」 |
| E2 | 闭环（残留 N3） | §5 `assets` 表（sha256 寻址）+ §5.2 取件/校验/缺失不阻断；§7 渲染产物图片路径；§10 图片引用集断言 |
| E3 | 闭环 | `events.entity` 扩为 doc/node/ref/comment/schema；§5.3 定义 ref 事件 payload `{op:add\|remove, src, dst, kind}` 与 M-LR 消费 |
| E4 | 闭环（残留 N7） | M09A（随 M01 交付，服务 M03 提议校验/M06 写入校验）/M09B（质量门）拆分；§4 模块表、依赖图、§12、B14、summary 阶段同步 |
| E5 | 闭环 | §5.3：事件+实体同事务、乐观锁 409、不建快照（重放视图）、M09B events↔当前态巡检 |
| E6 | 闭环 | `comments.target_event_id`；`state` 增 `orphaned`（不级联）；§6.3 历史视图批注呈现规则 |
| E7 | 闭环 | `nodes.parent_node_id`+`level`；§5.4 锚构造与位置无关（章节号+标题哈希消歧，覆盖重复/无编号标题）+ 重解析迁移规则 |
| E8 | 闭环 | §4「边界细则」消歧（M02 不含图遍历）；§6.4 kind×方向×跳数表 + 去重/环/排序 + FTS/pg_trgm 与索引 |
| E9 | 闭环（残留 N4） | §5.3 schema 复审口径（一律按当前 schema）+ 术语数据源（glossary + 规范性关键词） |
| E10 | 闭环 | §6.1 取消概率置信度→`rule_id`+待确认标志；审核载体 CLI（阶段 1）→M07（阶段 2）；未映射块 note/code 兜底且计入覆盖率分母 |
| E11 | 部分闭环（残留 N2） | B10 上修 ≤100k 节点/≤500 文档（含粒度前提与实测依据）；summary/design 已同步，**trade_off_matrix 未同步** |
| E12 | 闭环 | §7 新增「渲染产物」行（`build/rendered/`，不在 spec/、不被 ingest 扫描）+「入库唯一入口」（初始快照 + 增量仅走 events→M-LR） |
| E13 | 部分闭环（残余构成 N1） | §10 重写为 `normalize()` + 覆盖率 + 图片/HTML/事件/批注/断链断言；**覆盖率口径与 §6.1 兜底保证冲突（见 N1）** |
| E14 | 闭环 | §5 `schemas` 行注明 doc_type 组合规则随首个非 standard 类型引入；clarifications 新增 Q6 |
| E15 | 闭环 | 矩阵与计算式改为 A 4.45 / B 3.00 / C 3.25（含 B/C 完整算式）；summary 同步 |
| E16 | 闭环 | design §1 与 summary 均改为「实测 8,812,225 B ≈8.8MB、75,694 行」 |
| E17 | 闭环 | design §2 与 clarifications §1 均改为：4 项标 v0.1 §5.1；「全自动直转」标 B11 + GigaRAG 核心原则（非 §5.1） |
| E18 | 闭环 | design §2 增「延后声明」：UCIS/vPlan 适用于 verification 类型，随 B7 逐类型扩展落地 |
| E19 | 闭环 | 计划文档恢复至 `spec/idea/plan-spec-central-directory.md`（已核验 745 行）；clarifications §0 与 design §9 引用同步修正（docs/plans 已废弃） |
| E20 | 闭环 | §3 图注「现状：JSON 文件模式；迁移后：同 PG 实例 LIGHTRAG_* 表」；§7 增迁移前置条件；§11 增迁移风险行 |

## 新引入 / 残留问题

### N1 解析提议覆盖率口径与兜底保证冲突（原 E13 残余）

- **Severity**: MEDIUM
- **位置**: `design_doc.md` §10（解析器行）、§6.1（未映射内容兜底）
- **问题描述**: §10 定义「解析提议覆盖率 = 被原子承接的源块数 ÷ 总源块数」并给出阶段 1 目标 ≥95%；§6.1 又保证「规则未覆盖块 100% 有兜底原子（note/code）」。按字面实现，兜底块同样「被原子承接」→ 覆盖率恒为 100%，≥95% 门禁不可否证（无法发现解析规则退化），阶段 1 里程碑的量化判据形同虚设。若原意为「规则命中率」，则分子应限定为 `rule_id` 命中的块。
- **修复建议**: 将指标改写为「**规则覆盖率 = 携带 rule_id 的源块数 ÷ 总源块数（≥95%）**」，兜底块单列为「**兜底率/待确认清单条数**」独立指标并纳入回归基线；两处口径在 §6.1 与 §10 保持一致。

### N2 trade_off_matrix 未随 B10 上修同步（≤10k 残留）

- **Severity**: LOW
- **位置**: `trade_off_matrix.md` D1 行、§3「已被否决的选项」行
- **问题描述**: B10 已上修 ≤100k 节点，但 D1 仍写「节点量级 ≤10k（B10）」，否决项仍写「≤10k 节点纯 PG 足够」——陈旧引用与 B10 v1.1 及其他文档不一致（结论不受影响）。
- **修复建议**: 两处改为「≤100k 节点（B10 v1.1）」。

### N3 `assets.missing` 未纳入 M09B 职责声明

- **Severity**: LOW
- **位置**: `design_doc.md` §5.2、§4 M09B 描述、§5 `assets` 表
- **问题描述**: §5.2 规定缺失资产记为 `assets.missing` 违规项（由 M09B 呈现），但 §4 的 M09B 职责枚举仍为「断链/术语/渲染一致性/events↔当前态一致性」，未含资产缺失；`assets` 表列（asset_id/mime/bytes/origin/path）亦无 missing 状态承载位。
- **修复建议**: §4 M09B 职责补「资产缺失」；§5.2 明确缺失记录的落点（独立违例表或 `assets.state` 列）。

### N4 glossary/terms 表未进入 §5 数据模型清单

- **Severity**: LOW
- **位置**: `design_doc.md` §5.3、§5 表清单
- **问题描述**: §5.3 声明术语校验数据源为「terms 词汇表（glossary 表，随 M09B 引入）」，但 §5 的表清单（docs/nodes/refs/events/comments/schemas/assets）未列该表。
- **修复建议**: 在 §5 增 `glossary` 表行（或注明「M09B 引入时补登记」）。

### N5 approach_analysis.md 未同步 M09A/M09B 与阶段口径

- **Severity**: LOW
- **位置**: `approach_analysis.md` 实施顺序建议节
- **问题描述**: 阶段 1 仍写「M01 → M02 → M03 → M04」（缺 M09A）；阶段 3 仍写「M09 质量门」；并行可能性仍写「M05 与 M09 在 M04 后可并行」——与 design §12、B14、summary 的新口径不一致。
- **修复建议**: 同步为「M01（+M09A）→ M02 → M03 → M04」「阶段 3：M05 → M09B → M-LR」「M05 与 M09B 可并行」。

### N6 版本号未同步

- **Severity**: LOW
- **位置**: 四份文档 frontmatter
- **问题描述**: design_doc 升为 1.1.0 并附修订说明，clarifications / trade_off_matrix / summary 内容已改仍为 1.0.0，变更可追溯性不一致。
- **修复建议**: 三份同步至 1.1.0（或按各自修订记录递增）。

### N7 §4 依赖原则措辞与依赖图小口径冲突

- **Severity**: LOW
- **位置**: `design_doc.md` §4 原则句与依赖图
- **问题描述**: 原则句「只依赖低编号模块（编号序即实现序）」与 M03/M06 依赖 M09A 字面冲突（M09A 交付序靠前但编号为 9）；依赖图仍缺 M01→M03、M02→M06、M01→M07 等表中有、图中未绘的边。
- **修复建议**: 原则句改为「只依赖已交付模块，交付序见 §12（M09A 随 M01 交付）」；图边按模块表补齐或注明「图仅示主链」。

### N8 §11 大文件参数未用实测最大值

- **Severity**: LOW
- **位置**: `design_doc.md` §11 风险表（解析质量行）
- **问题描述**: 该行仍引用「3.4MB/2.7 万行」，实测最大规模为 CXL 3,594,622 B / 31,072 行（PCIe 3,531,270 B / 27,850 行）。
- **修复建议**: 改为「最大单文档 3.6MB / 3.1 万行（CXL）」以与 §1 实测口径一致。

## 复核结论

19/20 项完全闭环（E1–E12、E14–E20）；E13 部分闭环，其残余（N1）构成新的阻塞项。其余 N2–N8 为 LOW 信息项。

存在 1 个阻塞问题（N1）

---

# 最终确认（N1–N8 闭环，2026-09-16）

| 项 | 结论 | 核验位置（改后） |
|---|---|---|
| N1 | 闭环 | `design_doc.md` §10 L292「规则覆盖率 = 携带 `rule_id` 的源块数 ÷ 总源块数（≥95%）」+ 单列「兜底率/待确认条数」；§6.1 L196 兜底 bullet 注「不计入规则覆盖率」 |
| N2 | 闭环 | `trade_off_matrix.md` D1（L35）与否决表（L48）均改为 ≤100k（B10 v1.1） |
| N3 | 闭环 | `design_doc.md` §4 M09B 职责（L99）增「assets 缺失」；`assets` 表（L136）注「缺失引用以 `assets.missing` 违规项记录（不建空行）」 |
| N4 | 闭环 | `design_doc.md` §5 新增 `terms` 表行（L137：term / definition_node_id / kind=glossary\|normative-keyword） |
| N5 | 闭环 | `approach_analysis.md` 阶段 1（L78 含 M09A + 规则覆盖率）、阶段 3（L80 M09B）、并行行（L82 M09B） |
| N6 | 闭环（3 份） | `clarifications.md`/`trade_off_matrix.md`/`summary.md` version → 1.1.0（各 L8） |
| N7 | 闭环 | `design_doc.md` §4 原则句（L87）改为「依赖以交付序约束（§12）：模块只可依赖已交付模块；模块表列完备依赖，依赖图仅示关键路径」 |
| N8 | 闭环 | `design_doc.md` §11（L303）改为「实测最大 CXL 3,594,622 B / 31,072 行」 |

## 残留（全部非阻塞，措辞/版本级）

- C1（LOW）：`summary.md` L42 里程碑仍写「解析提议覆盖率 ≥95%」，与 design §10/§6.1 新口径「规则覆盖率」术语不一致（改一个词）。
- C2（LOW）：`design_doc.md` L166 仍称「`terms` 词汇表（glossary 表）」——§5（L137）已定名 `terms`（kind 含 glossary），括号内旧别名建议删去。
- C3（LOW）：`approach_analysis.md` 已按 N5 修改但版本仍为 1.0.0（L8），建议随其余文档一并升 1.1.0。

## 最终结论

N1–N8 全部闭环；残留 C1–C3 为措辞/版本级、不影响 it.arch 交接。E1–E13 原阻塞项与其后残余均已闭环。

无阻塞问题
