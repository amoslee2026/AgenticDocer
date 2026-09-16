---
title: 假设与澄清记录 — spec 集中目录
type: composite
purpose: spec
audience: both
direction: input
status: approved
version: "1.0.0"
section_meta: "@meta"
---

# 假设与澄清记录 — spec 集中目录

生成：2026-09-16。it-idea auto 模式（auto_approve=true），未暂停澄清；全部按保守默认推进。输入：`Notes/idea/芯片设计知识库-结构化文档方案-v0.1.md` + 用户指令「集中所有spec到spec目录」。

## 假设清单

| # | 问题/模糊点 | 采用的默认 | 依据 | 影响 | 回退方式 |
|---|---|---|---|---|---|
| A1 | spec 目录建在哪 | `AgenticDocer/spec/`（仓库根） | 用户将 v0.1 方案存于本仓库 Notes/idea；项目名即知识库定位 | — | 目录可整体 `git mv` 迁移 |
| A2 | 「所有 spec」的边界与 spec/ 的层语义 | **分层：spec/ 是知识库型 spec 的物理层 + 工程 spec 的元层（引用视图）**。物理集中 = GigaRAG `corpus/03_reviewed/` 已审核 7 份行业规范（v0.1 §9 首批试点范围「GigaRAG里的规范文档」）；引用登记 = 项目工程 spec（GigaPie/spec、Arion/spec/PRD、nova2026/archExplorer/spec）不迁移。Blast radius 实证（2026-09-16 grep）：`03_reviewed` 在 GigaRAG/scripts 中唯一消费者是 ingest.sh（L14/L53/L139，Task 4 适配）；advisory 点名的 stage_unverified.py/batch_*/merge_best*/split_chapters.py 等转换脚本全部操作 `01_raw/` 与 `02_converted/`——本计划不触碰，5 阶段转换管线与各项目 ingest 契约零影响 | 物理搬走活跃项目流水线产物会破坏工作流；v0.1 §9 划定试点范围；转换管线断链风险经 grep 排除 | 集中语义 = 知识库型 100% 物理持有 + 工程型元层登记 | 若意图为全量物理集中：将 INDEX 表 2 条目逐个 mv 入 spec/（结构不变）；若 GigaRAG 转换脚本未来新增 03_reviewed 消费者，需同步纳入 Task 4 式适配 |
| A3 | 未审核中间产物是否迁移 | 不迁移。`03_unverified/` 551 份分章、`02_converted/` 各转换变体留在 GigaRAG | 违背 GigaRAG「只入库人工转换+人工审核通过文档」核心原则（README L5） | spec/ 只含可信内容 | 审核通过后按移交流程进入 |
| A4 | `01_raw/` 原始 PDF 是否迁移 | 留在 GigaRAG（其定位「仅溯源存档」）；frontmatter `source` 记原路径 | 避免大文件跨仓库重复；PDF 是转换源头，由流水线持有 | `source` 为跨仓库引用路径 | 需要时建 `spec/assets/` 再议 |
| A5 | GigaRAG 角色变化 | 保留转换+审核流水线；`ingest.sh` 读源参数化指向 spec/；权威文件导入成功后**原地标记** `ingested_at`（KEEP_IN_PLACE），不再 mv 至 04_ingested | 单一权威源原则；现有 L134 mv 会搬走知识库本体 | GigaRAG ingest.sh 小改（计划 Task 4） | `KEEP_IN_PLACE=0` 恢复旧行为 |
| A6 | 存量文件是否重命名规范化 | 保持原文件名；命名规范只约束增量 | 文件名与人工审核成果对应稳定；lightRAG 按 basename 核对 | basename 全局唯一成为硬约束（ingest 依赖） | — |
| A7 | 目录类目是否全部预建 | 首批只建 `standards/<org>/`（pcie/amba/cxl/jedec 四个有实物的）；lang/product/safety 在 README 定义、有文档时即建 | YAGNI；空目录无价值 | — | 即用即建 |
| A8 | v0.1 方案文档本身是否入 spec/ | **【修订 2026-09-16 用户指令「所有 spec 文件和 idea 保存在 ./spec」】迁入 `spec/idea/`**；随迁 `idea/assumptions.md`、`idea/.review/`（Task 1 已 git 入库留底）；`docs/plans/`（执行计划）非 spec/idea 类，保留原位 | 用户指令覆盖原保守默认；idea 与 spec 同属知识库内容物 | Notes/ 目录退役；it-idea 后续产物落 `spec/idea/` | mv 可逆（git rename 记录） |
| A9 | 「集中/适当/尽量」等模糊词量化 | K1 集中率 7/7=100%；K2 frontmatter 必填 17 字段 100%（ingested_at 不计入）；K3 ingest DRY_RUN 列出 7 份；K4 INDEX 物理 7 行+引用 ≥3 行、表 1 路径与 spec_id 逐条一致且引用路径存在率 100%；K5 双仓 git 留底；K6 全程零删除；idea 归位完成（Task 3 Step 3 断言） | 量化铁律：不可验收的目标不进入计划 | — | — |
| A10 | 是否执行 LightRAG 重建入 | **【用户指令 2026-09-16：先不要导入 GigaRAG 的文档！！！先开发本项目，再用 GigaRAG 的 markdown 文档做测试】不执行任何 lightRAG 摄入**；`standards/` markdown 先作 AgenticDocer 新系统测试语料；摄入命令当前禁止执行（spec/README 已加 ⛔ 暂缓标注） | 用户明确指令；04_ingested 为空且 LocalServices.md 记录 API key 不一致——摄入前置条件亦未满足 | `ingested_at` 暂缺属预期；ingest.sh 能力（SPEC_SRC_DIR/KEEP_IN_PLACE/DRY_RUN）已就绪待用 | 用户指示后按 spec/README 参考命令执行 |
| A11 | INDEX.md 的 mySkills type/purpose 枚举 | `type: composite, purpose: readme`（登记索引性质，取最接近的合法枚举） | mySkills meta-fields §1.1 无 index 枚举项 | — | — |
| A12 | standards 与 lang 边界细则 | 标准组织正式规范（含 IEEE 1800 LRM、RISC ISA）入 `standards/`；EDA 厂商语法参考/教程手册入 `lang/` | v0.1 §4.1/§4.2 分类精神 | `02_converted/` 待审的 systemverilog/、riscv/ 将来入 standards/ | — |
| A13 | 7 份规范是否都具备 reviewed_by | 迁移脚本按现有 frontmatter 判定：有 `reviewed_by` → `status: approved`；无 → `status: review` 并同步改 INDEX 对应行 | 对抗评审 R9 实证：7/7 均含 reviewed_by（批量导入授权），全为 approved；该分支保留为防御 | 无预期影响（已实证分支不触发） | 补人工审核后改 approved |
