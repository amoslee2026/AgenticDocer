---
name: docer-write
description: 需要新增/修改/软删结构化节点时使用（乐观锁写入，409 冲突需重读后重试）。写入前先 docer-diff 感知他方改动，写后 docer-render 自检产物。
role: editor
command: agenticdocer node put|node delete
---

# docer-write：结构化写入

## 何时用

- 按人类标注（`docer-annotations`）或评审意见修订既有节点；
- 补充/修订定义、条款、表格等原子；
- 软删过时节点（写 delete 事件，关联批注自动置 `orphaned`，**不级联删除批注**）。

## 前置角色

**editor**（表格编辑同此权限；reviewer 只能批注与审批，不能改正文）。

## 底层命令

```bash
# 更新：载荷 = NodeIn（camelCase）+ expectedVersion（乐观锁）
agenticdocer node put --file patch.json --json

# 内联新建（最短路径）
agenticdocer node put --doc SPEC-STD-AMBA-APB --atom-type clause --anchor 'SPEC-STD-AMBA-APB#3.2.1·transfer' \
  --content '{"text":"…"}' --json

# 软删（必须给当前 version）
agenticdocer node delete <node_id> --expected-version 3 --json
```

`patch.json` 示例（字段口径见 `agenticdocer node get --json` 输出）：

```json
{"docId": "SPEC-STD-AMBA-APB", "nodeId": "<uuid7>", "atomType": "clause", "anchor": "…#3.2.1·transfer",
 "format": "md", "ordinal": 42, "level": 3, "content": {"text": "修订后的正文"}, "expectedVersion": 3}
```

## 输出解读

返回写入后的 `NodeDTO`：`version` 已 +1（**下次更新要用这个新值**）；服务端同时落 `node` 事件
（字段级 diff），该文档重渲染由服务端触发。

## 失败与重试

| 现象 | 处置 |
|---|---|
| **409** | 乐观锁冲突：`agenticdocer node get <node_id>` 重取 `version`（并 `docer-diff` 看谁改了什么）后重试；**不要**盲目重放旧载荷 |
| **422** | schema 校验失败：按 `detail.violations[].fixHint` 修正 `content`（八类原子 schema 见 M01） |
| 404 | 节点已软删或 doc_id/anchor 错 → 转 `docer-read` 复核 |
| 403 | 见下节（需 editor） |

## 权限不足补救

```
agenticdocer user role --username <你的用户名> --role editor
agenticdocer grant add --username <你的用户名> --scope doc_type --value <doc_type|doc_id> --permission write
```

## 纪律

- 一次只改一个语义单元；`anchor` 尽量保持不变（锚是跨文档引用与批注的定位键）；
- 修改后必跑 `docer-render`（自检往返一致）+ `docer-diff`（确认改动范围符合预期）。
