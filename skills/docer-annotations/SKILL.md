---
name: docer-annotations
description: 需要知道「人类评审者说了什么」时使用：读取 WebUI 里留下的批注（正文、作者、状态、锚定节点与版本），并取回批注锚定版本处的节点快照。只读，不改批注状态。
role: reader
command: agenticdocer comment list
---

# docer-annotations：调取人类标注（B11 专项）

## 何时用

- 人类在 WebUI 留了批注，agent 需要据此修订（B11：**专用 skill 调取人类用户的标注**）；
- 需要「批注所指的历史版本内容」来理解人类当时看到的是什么；
- 需要清点仍未处置的开放批注（`state=open`）或节点已删的遗留批注（`state=orphaned`）。

## 前置角色

**reader**（本 skill **只读**；批注状态流转属 reviewer 职责，走 `agenticdocer comment resolve`）。

## 底层命令

```bash
# 某文档的全部开放批注（含锚定节点与版本）
agenticdocer comment list --doc SPEC-STD-AMBA-APB --state open --json

# 带上「锚定版本处的节点快照」——agent 据此理解人类在说什么
agenticdocer comment list --doc SPEC-STD-AMBA-APB --state open --with-context --json

# 单节点批注 / 节点已软删的遗留批注
agenticdocer comment list --node <node_id> --json
agenticdocer comment list --doc SPEC-STD-AMBA-APB --state orphaned --json
```

`--doc` 与 `--node` **二选一**（同时给或不给都会被拒）；`--state` 可取 `open|resolved|orphaned`，缺省为全部。

> 全部命令都支持 `--json`（结构化输出，camelCase，与 M06/M07 DTO 同形）与 `--dry-run`
> （干跑：只回放将要发出的请求，不触网/不写库；用于参数自检与固定 prompt 演练）。

## 输出解读

```json
[{"commentId": "…", "nodeId": "…", "targetEventId": "…", "body": "人类批注正文",
  "state": "open|resolved|orphaned", "author": "<人类 user_id>", "version": 1, "ts": "…",
  "context": {"anchorEventId": "…", "historyCount": 4, "nodeMissing": false, "node": {"anchor": "…", "content": {…}}}}]
```

- `targetEventId`：批注**锚定的版本**（人类写批注时的节点状态）；
- `--with-context` 时逐条调 `GET /api/v1/events/replay?node_id=&upto=<targetEventId>` 取该版本快照，
  于是「人类当时看到的内容」与「当前内容」可并排比较（当前内容用 `docer-read`）；
- `state=orphaned`：节点已软删、批注按规范保留（REQ-M02-F05）——**不要**据此删批注。

## 失败与重试

| 现象 | 处置 |
|---|---|
| 空列表 | 该文档/节点确实没有匹配批注（退出码 0）；确认 `--state` 与 `--doc` 是否写错 |
| 403 | 见下节（需 reader） |
| `--doc`/`--node` 报用法错误 | 二选一，不能同时给；批量按文档查用 `--doc` |

## 权限不足补救

```
agenticdocer user role --username <你的用户名> --role reader
agenticdocer grant add --username <你的用户名> --scope doc_type --value <doc_type|doc_id> --permission read
```

## 典型闭环（B11）

1. `docer-annotations --state open --with-context` → 逐条读懂人类意图与当时的上下文；
2. `docer-diff` / `docer-read` → 确认当前 `version` 与最新内容；
3. `docer-write` → 按批注修订节点；
4. reviewer 在 WebUI（或 `agenticdocer comment resolve <comment_id> --expected-version N`）置 `resolved`。
