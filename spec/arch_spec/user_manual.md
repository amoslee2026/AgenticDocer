---
title: 用户手册 — 芯片设计知识库系统
type: narrative
purpose: guide
audience: both
direction: output
status: approved
version: "1.4.0"
section_meta: "@meta"
---

# 用户手册

生成：2026-09-16（it.arch Phase 3/4）。**v1.4 更新**（依批注 B1–B11 与用户要求）——新增鉴权、CLI 工具族、监控与性能评估章节。

面向三类使用者：**Agent 操作者**（coding agent / 工程脚本，经 CLI/HTTP）、**人类评审者**（WebUI）、**管理员**（用户与权限管理）。命令行与界面细节在 it.mas/it.tdd 细化；本手册定义使用路径与预期行为。

> **运行期不依赖 LLM（P6）**：本系统运行路径不调用任何 LLM——`coding agent` 只是**外部调用方**（通过 CLI/HTTP 访问），系统在无 LLM 凭据、断网环境下全功能可用。

## 0. 部署与首次启动（管理员）

```bash
# 环境（uv 管理，Python 3.11）
uv sync                                  # 安装依赖（含 agentic-logger）

# 1) 管理员自举（首次必做，否则系统 fail-closed：所有请求 401）
cp ~/.ssh/id_ed25519.pub data/admin_keys/admin.pub   # 你的公钥
uv run alembic upgrade head              # 建库 + 载入 seed（terms）
uv run agenticdocer auth bootstrap       # 创建首个 admin（幂等）

# 2) 启动服务
uv run agenticdocer-api --host 0.0.0.0 --port 8787   # 鉴权后方可对外监听
```

**注意**：无 `users` 表记录时系统拒绝所有请求（fail-closed 设计）——这是有意为之，避免「忘记配鉴权即裸奔」。

## 1. 快速开始（Agent 操作者）

**前置**：你的 SSH 公钥已在 `users` 表登记（由 admin 执行 `agenticdocer user key add`）。CLI 自动读取 `~/.ssh/` 或 `AGENTICDOCER_SSH_KEY` 私钥签名，无需手工处理鉴权。

```bash
# 身份自检
uv run agenticdocer auth whoami          # 显示 user_id / role / 公钥指纹

# 导入一份规范文档（三步骤：解析 → 审核 → 入库）
uv run agenticdocer import parse spec/standards/amba/IHI0024_AMBA_APB_spec.md
uv run agenticdocer import review IHI0024_AMBA_APB_spec       # 逐条审核
uv run agenticdocer import commit IHI0024_AMBA_APB_spec       # 校验+事务入库

# 读写（需 editor 角色）
uv run agenticdocer node get SPEC-STD-AMBA-APB#3.2.1
uv run agenticdocer node put --file patch.json               # 含 expectedVersion（乐观锁）

# 版本与渲染
uv run agenticdocer doc diff SPEC-STD-AMBA-APB --from 2026-09-01
uv run agenticdocer render SPEC-STD-AMBA-APB                  # 整档（build/rendered/）
uv run agenticdocer render SPEC-STD-AMBA-APB --section 3.2    # 单章节（<1s）

# 调取人类批注（agent 专用 skill 的底层命令）
uv run agenticdocer comment list --doc SPEC-STD-AMBA-APB --state open
```

**Skill 用法**（coding agent 侧，`skills/` 目录）：`docer-import` / `docer-read` / `docer-write` / `docer-render` / `docer-diff` / **`docer-annotations`**（调取人类标注）。

## 2. 导入与审核（半自动流程）

1. **parse**：解析器产出原子提议，逐条带 `rule_id` 与「待确认」标志；同时输出未映射块清单。
2. **review**：人工/agent 逐条处置（通过/拒绝/修正）；「待确认」项必须显式确认；未映射块默认兜底（`note`/`code`）保留。
3. **commit**：经 schema 校验后事务入库；失败则报违规明细，修改提议后重试。

**验收口径**：规则覆盖率（携带 `rule_id` 的源块 ÷ 总源块）≥95%；兜底率与待确认条数在审核输出中报告。

**权限**：`import *` 需 editor 角色。

## 3. 结构化读写（M06 API）

- **鉴权**：所有端点（含读）需 SSH 签名。请求头 `X-SSH-Signature`/`X-SSH-Key-Id`/`X-Timestamp`/`X-Nonce`；签名载荷 = `METHOD\nPATH\nSHA256(body)\nTimestamp\nNonce`。CLI 自动完成（§1）；手写脚本可用 `agenticdocer auth sign` 辅助。
- 读：按 `node_id` / `doc_id` / `anchor`（如 `SPEC-STD-AMBA-APB#3.2.1·transfer`；重复标题带 `~正文摘要` 后缀）取节点。
- 写：提交 JSON Schema 约束的节点变更 + 当前 `version`（乐观锁）。校验失败 → 违规清单+修复建议；冲突（409）→ 重读后重试。
- 每次成功写入自动：写事件（字段级 diff）→ 更新实体 → 触发该文档重渲染。

## 4. 检索

**本系统只提供确定性读写与文档树浏览**；检索能力归属 LightRAG：

| 需求 | 途径 |
|---|---|
| 按 ID/锚直取节点 | `agenticdocer node get`（M06） |
| 浏览文档树/章节树 | `agenticdocer doc get`、`GET /docs/{id}/sections` |
| 关键词/语义检索 | **LightRAG**（本系统经 M-LR 提供导出包：渲染文本 + node_id + 增量事件流） |

> **注**：M05 的图遍历与 FTS 为**内部实现**（供 M-LR 导出与质量门），不暴露端点（ADR-008）。

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
