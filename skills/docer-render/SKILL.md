---
name: docer-render
description: 需要文档的可读 markdown 产物时使用（整档或单章节，HTML 片段零改写直通）。写入后用来自检产物；人类评审者看的是 WebUI，agent 侧看这个。
role: reader
command: agenticdocer render
---

# docer-render：渲染为 Markdown

## 何时用

- 需要**完整可读文本**（交给 LLM 阅读/比对、生成导出包、人工抽查）；
- 写入后自检：渲染产物与源文档应往返一致（REQ-M04-F01）；
- 大文档只关心一节 → `--section` 单章节渲染（目标 <1s，避免整档开销）。

## 前置角色

**reader**。

## 底层命令

```bash
agenticdocer render SPEC-STD-AMBA-APB --json                  # 整档（服务端落 build/rendered/）
agenticdocer render SPEC-STD-AMBA-APB --section 'SPEC-STD-AMBA-APB#3.2' --json
agenticdocer render SPEC-STD-AMBA-APB --markdown               # markdown 直接打到 stdout
agenticdocer render SPEC-STD-AMBA-APB --out build/local.md     # 另存一份到本地路径
```

章节锚从 `GET /api/v1/docs/{doc_id}/sections`（`docer-read` 的 sections 清单口径）取得。

> 全部命令都支持 `--json`（结构化输出，camelCase，与 M06/M07 DTO 同形）与 `--dry-run`
> （干跑：只回放将要发出的请求，不触网/不写库；用于参数自检与固定 prompt 演练）。

## 输出解读

`{docId, outPath, assetsExported, section, markdown}`：

- `outPath`：服务端产物路径（`build/rendered/`，可重建、不入库）；
- `markdown`：渲染正文（`--json` 时随结果返回；人可读模式下用 `--markdown` 打印）；
- `assetsExported`：随产物导出的图片数量（缺图由 M09B `assets.missing` 报告）。

## 失败与重试

| 现象 | 处置 |
|---|---|
| 404 | doc_id 不存在 → `agenticdocer doc list` 复核 |
| 渲染缺图 | 查导入期 `assets.missing` 清单，补齐源图后重跑 `import commit`（渲染是只读的，可反复重跑） |
| 403 | 见下节（需 reader） |

## 权限不足补救

```
agenticdocer user role --username <你的用户名> --role reader
agenticdocer grant add --username <你的用户名> --scope doc_type --value <doc_type|doc_id> --permission read
```
