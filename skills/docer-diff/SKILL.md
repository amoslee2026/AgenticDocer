---
name: docer-diff
description: 动手修改前感知他方（人类或其他 agent）对文档的改动，或需要向人汇报本次改了什么时使用。输出字段级结构化 diff（events 重放口径，与 WebUI 版本历史同源）。
role: reader
command: agenticdocer doc diff
---

# docer-diff：变更感知

## 何时用

- **写前必查**：确认自己手上的 `version`/内容没有过期（时序纪律：`docer-diff` → `docer-write`）；
- 需要交付「本次改动摘要」（节点数/字段数/操作类型分布）；
- 需要解释某节点为何是当前这个值（版本历史）。

## 前置角色

**reader**。

## 底层命令

```bash
agenticdocer doc diff SPEC-STD-AMBA-APB --json                        # 当前 vs 上一次变更（缺省区间）
agenticdocer doc diff SPEC-STD-AMBA-APB --from 2026-09-01 --json      # 指定时间区间
agenticdocer doc diff SPEC-STD-AMBA-APB --from 12 --to 18 --json      # 指定版本区间
```

> 全部命令都支持 `--json`（结构化输出，camelCase，与 M06/M07 DTO 同形）与 `--dry-run`
> （干跑：只回放将要发出的请求，不触网/不写库；用于参数自检与固定 prompt 演练）。

## 输出解读

```json
{"docId": "…", "fromTs": "…", "toTs": "…",
 "changes": [{"nodeId": "…", "anchor": "…#3.2.1·transfer", "op": "added|modified|deleted",
              "field": "content.text", "before": "旧值", "after": "新值"}],
 "summary": {"added": 2, "modified": 5, "deleted": 0, "refs": 1}}
```

- 与 `apply_events` 折叠口径一致（P5）：同一份数据，API/WebUI/CLI 三处结果相同；
- **无变更时 `changes` 为空且退出码 0**（不是错误）。

## 失败与重试

| 现象 | 处置 |
|---|---|
| `changes` 为空但预期有改动 | 确认 `--from/--to` 区间；确认改动发生在**本库**（外部直接改 spec/ 快照不会产生事件） |
| 404 | doc_id 不存在 → `agenticdocer doc list` |
| 403 | 见下节（需 reader） |

## 权限不足补救

```
agenticdocer user role --username <你的用户名> --role reader
agenticdocer grant add --username <你的用户名> --scope doc_type --value <doc_type|doc_id> --permission read
```

## 建议工作流

`docer-diff`（看别人改了什么）→ `docer-read`（取最新 `version`）→ `docer-write`（写）→ `docer-diff`（确认改动范围）。
