# AgenticDocer skills（agent 侧语义封装，架构 §9.3）

本目录是给**外部 coding agent** 消费的 skill 定义（运行期不依赖、不安装，P6）：每个 skill 把
`agenticdocer` CLI 的若干子命令封装成「何时用 / 需要什么角色 / 怎么读输出 / 失败怎么重试」的语义单元，
**不重复实现任何逻辑**。

| Skill | 用途 | 前置角色 | 底层命令 |
|---|---|---|---|
| [`docer-import`](docer-import/SKILL.md) | 导入 markdown → 结构化库（解析 → 提议审核 → 事务入库） | editor | `agenticdocer import parse\|review\|commit` |
| [`docer-read`](docer-read/SKILL.md) | 按 doc_id/anchor/node_id 读取文档树与节点（含 `version`） | reader | `agenticdocer doc list\|get`、`node get` |
| [`docer-write`](docer-write/SKILL.md) | 结构化写入/更新/软删（乐观锁，409 重读重试） | editor | `agenticdocer node put\|delete` |
| [`docer-render`](docer-render/SKILL.md) | 渲染整档或章节为 Markdown | reader | `agenticdocer render` |
| [`docer-diff`](docer-diff/SKILL.md) | 查看文档版本 diff（了解他方改动） | reader | `agenticdocer doc diff` |
| [`docer-annotations`](docer-annotations/SKILL.md) | **调取人类标注**（含锚定版本上下文） | reader | `agenticdocer comment list` |

## skill 与 CLI 的关系

- **skill 是 CLI 的语义封装**：声明「何时用哪个命令、如何解读输出、失败如何重试、需要何种角色」；
  实现只有一处——`src/agenticdocer/cli.py`；
- **鉴权由 CLI 自动完成**：skill 不感知密码学细节，只要求运行环境有可用 SSH 私钥且公钥已在 `users` 表登记
  （`AGENTICDOCER_SSH_KEY` 可指定私钥；`agenticdocer auth whoami` 自检身份）；
- **面向 agent 的输出**：所有命令支持 `--json`（camelCase，与 M06/M07 DTO 同形），便于机读；
- **干跑**：`--dry-run` 只回放将要发出的请求（不触网/不写库），用于参数自检与固定 prompt 演练。

## 四字段契约（V17 判据）

每个 `skills/<name>/SKILL.md` 的 YAML frontmatter 必须含且仅含四个字段：`name` / `description`
（何时用）/ `role`（前置角色）/ `command`（底层命令）。机检：

```bash
uv run pytest tests/unit/test_skills_schema.py -q      # jsonschema 校验 + 四字段 + 命令可达性
```

契约本体见 [`skill.schema.json`](skill.schema.json)（JSON Schema 2020-12）。

## 典型 agent 工作流（§9.3）

```
docer-import（首次导入：parse → review → commit）
  → docer-annotations（读取人类标注，定位待修正点，含锚定版本上下文）
  → docer-diff（先感知他方改动）
  → docer-read（取最新 version）
  → docer-write（按标注修订节点，乐观锁）
  → docer-render + docer-diff（自检产物与变更范围）
```

**时序纪律**：任何写入前先 `docer-diff` + `docer-read` 取最新 `version`，避免基于过期版本写入
（否则 409；重读后重试）。

## 权限模型（M10 四角色）

`reader < reviewer < editor < admin`；grant 只能在角色上限内**收窄**范围（`--scope doc_type|doc`，
`--permission read|write|review`）。权限不足时 CLI 输出所需角色名与授权命令原文，例如：

```
错误：HTTP 403 ...
补救：agenticdocer user role --username <你的用户名> --role editor
      agenticdocer grant add --username <你的用户名> --scope doc_type --value <doc_type|doc_id> --permission write
```

> **注**：`agenticdocer import commit` 与 `auth bootstrap` 不经 HTTP（前者是 M03 批量导入服务的事务写路径，
> 后者建立鉴权本身）。其余用户级操作一律经 M06/M07 HTTP，与 WebUI 共享同一套鉴权/RBAC 判定（P5）。
