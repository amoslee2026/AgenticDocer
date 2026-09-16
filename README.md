# AgenticDocer

芯片设计知识库的结构化文档系统：**结构化库为唯一权威源**，人类可读格式（Markdown/HTML）均为渲染产物；Agent 可通过 API 读写节点、追溯事件、评审批注。

## 目录

| 路径 | 内容 |
|---|---|
| `spec/` | spec 权威源：标准规范语料（`standards/`）+ 分类目录规范（`README.md`、`INDEX.md`） |
| `spec/idea/` | it.idea 产物：设计文档、方案分析、Trade-off 矩阵、澄清台账（E1–E20 已闭环） |
| `spec/arch_spec/` | it.arch 产物：架构规范（主契约）、34 条功能需求、ADR-001..006、数据流/工作流图、需求追溯矩阵 |
| `scripts/` | 工具脚本（frontmatter 升级等） |

## 规格基线

- **架构规范** `spec/arch_spec/architecture_specification.md` v1.2 — 模块接口契约（9 模块 M01–M09 + 边界 M-LR）、DDL 8 表、API/CLI、部署与横切规范
- **功能需求** `spec/arch_spec/functional_specification.md` — 34 条 REQ，P0/P1/P2 分级，验收标准可机械验证
- **评审记录** `spec/arch_spec/.review/issues.md` — 三轮对抗评审（A1–A25 + R1–R10/L1–L9 + N1–N4）全部闭环，终审无阻塞

## 下一步

`spec/arch_spec/` → it.mas（微架构/实现规格）→ it.tdd（实现）

## 授权协议

[PolyForm Noncommercial License 1.0.0](LICENSE) — 与 [AgenticLogger](https://github.com/amoslee2026/AgenticLogger) 同协议。仅限非商业用途；商业使用需另行取得授权。
