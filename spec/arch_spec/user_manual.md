---
title: 用户手册 — 芯片设计知识库系统
type: narrative
purpose: guide
audience: both
direction: output
status: approved
version: "1.2.0"
section_meta: "@meta"
---

# 用户手册

生成：2026-09-16（it.arch Phase 3）。面向两类使用者：**Agent 操作者**（coding agent / 工程脚本）与**人类评审者**（WebUI）。命令行与界面细节在 it.mas/it.tdd 细化；本手册定义使用路径与预期行为。

## 1. 快速开始（Agent 操作者）

```bash
# 环境（uv 管理，Python 3.11）
uv sync                             # 安装依赖
uv run alembic upgrade head         # 建库（database: agenticdocer）
uv run agenticdocer-api             # 启动服务（默认 127.0.0.1:8787）

# 导入一份规范文档（三步骤：解析 → 审核 → 入库）
uv run agenticdocer-import parse spec/standards/amba/IHI0024_AMBA_APB_spec.md   # 生成提议清单（在仓库根目录执行）
uv run agenticdocer-import review IHI0024_AMBA_APB_spec                         # 逐条审核（CLI，状态落 data/import_work/）
uv run agenticdocer-import commit IHI0024_AMBA_APB_spec --actor importer        # 校验+事务入库

# 渲染（产物落 build/rendered/，不动 spec/）
uv run agenticdocer-render SPEC-STD-AMBA-APB    # 入参为 doc_id（= frontmatter spec_id；doc_slug 仅导入工作区标识）
```

## 2. 导入与审核（半自动流程）

1. **parse**：解析器产出原子提议，逐条带 `rule_id` 与「待确认」标志；同时输出未映射块清单。
2. **review**：人工/agent 逐条处置（通过/拒绝/修正）；「待确认」项必须显式确认；未映射块默认兜底（`note`/`code`）保留。
3. **commit**：经 schema 校验后事务入库；失败则报违规明细，修改提议后重试。

**验收口径**：规则覆盖率（携带 `rule_id` 的源块 ÷ 总源块）≥95%；兜底率与待确认条数在审核输出中报告。

## 3. 结构化读写（Agent 通过 M06 API）

- 读：按 `node_id` / `doc_id` / `anchor`（如 `SPEC-STD-AMBA-APB#3.2.1·transfer`；重复标题带 `~正文摘要` 后缀）取节点（含 content 与元数据）。
- 写：提交 JSON Schema 约束的节点变更 + 当前 `version`（乐观锁）。校验失败 → 返回违规清单与修复建议；冲突（409）→ 重读后重试。
- 每次成功写入自动：写事件（字段级 diff）→ 更新实体 → 触发该文档重渲染。

## 4. 检索（阶段 3）

- 精确：`node_id`/`anchor`/`doc_id` 直取。
- 多跳：按 `traces_to`（上游 1–2 跳）、`composes_from`、`see_also` 遍历（结果含证据链与跳数）。
- 关键词：全文检索（FTS）；命中携带 node_id 可回查权威记录。
- 语义（联调后）：LightRAG 召回回查结构化库；正确性始终以结构化库为准。

## 5. 评审（人类评审者，WebUI）

| 操作 | 说明 |
|---|---|
| 浏览 | 按文档/节点树浏览；表单由 schema 自动生成 |
| 结构化 diff | 每次变更按字段级并排展示新旧值（非行级 diff） |
| 批注 | 针对 node_id 留言（open）；解决后置 resolved；节点删除后批注保留并标 orphaned |
| 状态流转 | draft → reviewed → approved（记录到事件日志） |
| 版本历史 | 按事件重放查看任意版本；批注显示于其锚定版本旁 |

## 6. 常见问题

| 问题 | 处置 |
|---|---|
| 解析出现大量「待确认」 | 正常——按批复核；高频模式可增补解析规则（rule_id 可追溯到规则） |
| 图片渲染缺失 | 查 M09B `assets.missing` 清单；确认 GigaRAG `corpus/02_converted/.../auto/images/` 有实物 |
| 写入返回 409 | 乐观锁冲突：重读节点（含最新 version）后重试 |
| 渲染产物在哪 | `build/rendered/`（可重建，不入库）；`spec/` 内的 markdown 是导入快照，勿直接编辑 |
| 为何不能向 lightRAG 导入 | 用户指令暂缓（C7）；系统就绪后按 §4 的导出包接口联调 |

## 7. 数据与恢复

- 权威源 = PostgreSQL（database `agenticdocer`）；一切变更可凭 `events` 重放。
- 备份：`pg_dump agenticdocer`（纳入 sys-backup 惯例）+ git（代码与 spec/ 文档）。
- 迁移：Alembic 管理 DDL 版本（`uv run alembic upgrade head`）。
