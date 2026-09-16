---
name: docer-import
description: 把一份 markdown 规范/手册导入结构化库时使用（解析 → 提议审核 → 事务入库三步）。产出 doc_id 与入库统计，后续读取/写入/渲染都以该 doc_id 为锚。
role: editor
command: agenticdocer import parse|review|commit
---

# docer-import：导入 markdown → 结构化库

## 何时用

- 库内**尚无**该文档（`agenticdocer doc list` 里找不到），需要首次导入；
- 源 markdown 大幅改版，需要按新快照重建节点（解析幂等，同锚复用）；
- **不适用**：单点修改已有文档 → 用 `docer-write`；只读/渲染 → `docer-read`/`docer-render`。

## 前置角色

**editor**（admin 亦可）。调用链第一步会经 `GET /api/v1/auth/me` 校验身份，再走 M03 导入服务
（`WriteContext(source="importer")`）。

## 底层命令

```bash
# 1) 解析：产出提议（proposals.json）+ 初始化审核状态（review_state.json）
agenticdocer import parse spec/standards/amba/IHI0024_AMBA_APB_spec.md --json

# 2) 审核：逐条处置提议（a 通过 / r 拒绝 / e 修正 / s 跳过 / u 未映射 / A 批量通过非待确认 / q 结束）
agenticdocer import review IHI0024_AMBA_APB_spec --accept-confident --json

# 3) 入库：schema 校验 + 事务写入 docs/nodes/refs/events + 资产同步
agenticdocer import commit IHI0024_AMBA_APB_spec --json
```

工作区默认 `data/import_work/<doc_slug>/`（`IMPORT_WORK_DIR` 可覆盖）；`doc_slug` 缺省取源文件名。
干跑（不写库、不触网）：三步都支持 `--dry-run`。

## 输出解读

- `parse`：`docMeta`（doc_id/doc_type/status）、`proposals`（每个提议带 `ruleId` 与 `needsConfirmation`）、
  `stats`（`totalBlocks`/`coverage`/`fallbackRate`/`pending`）、`unmapped`；
- `review`：`items.<proposalId>.decision` 计数 + `audit` 轨迹；
- `commit`：`docId`、`accepted`/`rejected`/`pending`、`commit`（doc_id/status/stats）、`assets`（`fetched`/`missing`）、
  `violations`（schema 级违规明细与 `fixHint`）。

**验收口径**：规则覆盖率 ≥95%（携带 `ruleId` 的源块 ÷ 总源块）；`coverage` 偏低说明规则库需增补。

## 失败与重试

| 现象 | 处置 |
|---|---|
| `commit` 报 `violations` | 按 `fixHint` 修正提议（`import review` 的 `e` 修正）后重新 commit；**不要**跳过校验 |
| `pending > 0` | 待确认项未显式处置；重跑 `import review`（待确认/兜底项必须逐条确认） |
| `assets.missing` 非空 | 源目录缺图（`assets/<sha256>.<ext>`）；补齐后重跑 `import commit`（可重复执行） |
| 401/403 | 见下节；403 且提示公钥未注册 → 请 admin `agenticdocer user key add` |

## 权限不足补救

CLI 会输出所需角色名与授权命令原文，例如：

```
错误：HTTP 403 ... 需要 editor 角色
补救：agenticdocer user role --username <你的用户名> --role editor
      agenticdocer grant add --username <你的用户名> --scope doc_type --value <doc_type|doc_id> --permission write
```

## 下一步

`docer-annotations`（读人类标注）→ `docer-write`（修订）→ `docer-render` + `docer-diff`（自检）。
