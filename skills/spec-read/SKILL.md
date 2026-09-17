---
name: spec-read
description: 需要按 doc_id / anchor / node_id 读取文档树或节点内容时使用（含节点 version，供后续写入做乐观锁）。只想看渲染后的 markdown 请改用 spec-render。
role: reader
command: agenticspec doc list|agenticspec doc get|agenticspec node get
---

# spec-read：结构化读取

## 何时用

- 动手修改前先取**当前态**（含 `version`），避免基于过期版本写入（配合 `spec-diff`）；
- 按锚定位章节（锚形态：`<doc_id>#<章节号路径>·<标题 slug>`，同父同题靠正文摘要消歧）；
- 浏览文档清单，确认目标文档是否已导入。

## 前置角色

**reader**（reviewer/editor/admin 亦可）。

## 底层命令

```bash
agenticspec doc list --json                       # 文档清单（docId/docType/title/status/version）
agenticspec doc get SPEC-STD-AMBA-APB --json      # 文档详情 + frontmatter meta
agenticspec node get <node_id> --doc <doc_id> --json   # 单节点（含 version）
agenticspec render <doc_id> --json                # 需要整档内容树 → 见 spec-render
```

`--doc` 传入可让服务端按 `doc_id` 分区裁剪（ADR-009 V16）；缺省为全分区扫（降级，慢但正确）。

> 全部命令都支持 `--json`（结构化输出，camelCase，与 M06/M07 DTO 同形）与 `--dry-run`
> （干跑：只回放将要发出的请求，不触网/不写库；用于参数自检与固定 prompt 演练）。

## 输出解读

- `NodeDTO`：`nodeId`/`docId`/`atomType`（八类原子之一）/`format`（md|html|text）/`level`/`anchor`/
  `content`（schema 约束的结构化内容）/`version`/`status`；
- `DocDTO`：`docId`/`docType`/`title`/`meta`/`status`(draft|reviewed|approved)/`version`/`updatedAt`；
- **`version` 是写入门票**：把它原样交给 `node put --expected-version`。

## 失败与重试

| 现象 | 处置 |
|---|---|
| 404 | 标识符不存在或已软删：`doc list` 复核 doc_id；节点已删则看 `comment list --state orphaned` |
| 401/403 | 见下节；读操作失败**不影响库状态**（可安全重试） |
| 输出为空/截断 | 用 `--json` 取完整结构化结果，勿解析人可读表格 |

## 权限不足补救

403 时 CLI 给出所需角色与授权命令原文：

```
agenticspec user role --username <你的用户名> --role reader
agenticspec grant add --username <你的用户名> --scope doc_type --value <doc_type|doc_id> --permission read
```
