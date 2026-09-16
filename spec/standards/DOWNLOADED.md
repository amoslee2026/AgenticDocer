---
title: 真实语料清单（非 standard doc_type 验证用）
type: composite
purpose: spec
audience: both
direction: input
status: approved
version: "1.0.0"
section_meta: "@meta"
---

# 真实语料清单

> **目的**：为 AgenticDocer 的非 `standard` 文档类型（`lang`/`tool-manual`/`product`/`safety`/UCIS）提供**真实语料**用于端到端验证。
>
> **来源**：用户指示「部分真实语料可以从网络搜索获得」（2026-09-17）→ 调研（`agent://IndividualTick`，全部 URL 实测 HTTP 状态码 + 许可核查）→ 下载。
>
> **下载日期**：2026-09-17。全部 **HTTP 200**，首行抽查确认为真实文档（非错误页）。

## 1. 目录结构

```
spec/standards/
├── {pcie,cxl,jedec,amba}/   # 既有：standard 类型（7 份，已审核）
├── lang/          # 语言/脚本语法手册（→ doc_type=lang）
├── tool-manual/   # EDA 工具手册（→ doc_type=tool-manual）
├── product/       # 项目规格/验证计划（→ doc_type=product）
├── safety/        # 功能安全 FMEA/FMEDA（→ doc_type=safety）
└── ucis/          # UCIS XML 结构化数据（→ table.coverage_matrix）
```

## 2. 语料清单（47 文件，约 1.04 MB）

### 2.1 `lang/` — 语言/脚本语法手册（23 文件，372 KB）

| 文件 | 字节 | 说明 |
|---|---|---|
| `set.n`／`proc.n`／`expr.n`／`if.n`／`for.n`／`while.n`／`list.n`／`string.n`／`puts.n`／`open.n`／`close.n`／`read.n`／`format.n`／`regexp.n`／`regsub.n`／`switch.n`／`catch.n`／`error.n`／`source.n`／`array.n`／`dict.n` | 728–22,982 | **Tcl 内置命令 man pages**（21 份）——**DocBook RefEntry 的原型形态**：NAME / SYNOPSIS / DESCRIPTION / OPTIONS / EXAMPLES / SEE ALSO |
| `opensta-commands.md` | 174,472 | **OpenSTA 命令参考**（283 个 `##` 命令节，含 SDC 命令：create_clock / set_false_path / set_input_delay 等） |
| `tcl-license.terms` | 2,255 | Tcl 许可（BSD 式，**明确许可 documentation 的 use/copy/distribute**） |

**来源**：`raw.githubusercontent.com/tcltk/tcl/main/doc/*.n`、`.../parallaxsw/OpenSTA/master/doc/Commands.md`
**许可**：BSD 式（Tcl）／ GPL-3.0（OpenSTA，仅作测试 fixture，不派生作品）

### 2.2 `tool-manual/` — EDA 工具手册（3 文件，220 KB）

| 文件 | 字节 | 说明 |
|---|---|---|
| `verilator-exe.rst` | 89,373 | Verilator 命令行选项参考（逐选项语法/参数/说明） |
| `verilator-warnings.rst` | 89,764 | Verilator 诊断码表（逐码含义） |
| `verilator-LICENSE` | 42,098 | LGPL-3.0 / Artistic-2.0 双许可 |

**来源**：`.../verilator/verilator/master/docs/guide/{exe_verilator,warnings}.rst`
**`tool_context` 验证点**：工具名 + 版本（Verilator 在文档构建期由 `conf.py::get_vlt_version()` 注入；此处为源文件）

### 2.3 `product/` — 项目规格/验证计划（7 文件，308 KB）

| 文件 | 字节 | 说明 |
|---|---|---|
| `opentitan-aes_testplan.hjson` | 10,641 | **OpenTitan AES 验证计划**：`name`/`desc`/`stage`(V1,V2,V3,V2S)/`tests[]` |
| `opentitan-aes_sec_cm_testplan.hjson` | 12,428 | 安全对策→测试的**追溯映射**（countermeasure → test） |
| `opentitan-aes.hjson` | 45,920 | AES IP 规格：`features`、**27 处 `bits:` 位域定义**、`registers`（resval/swaccess/hwaccess）、`countermeasures` |
| `riscv-isa-csrs.adoc` | 38,308 | RISC-V CSR 规格（**位域语义章节**：WLRL/WARL） |
| `riscv-isa-machine.adoc` | 173,630 | RISC-V Machine-level ISA（条款 + 规范性关键词） |
| `opentitan-LICENSE`／`riscv-isa-LICENSE.adoc` | 11,358／860 | Apache-2.0 ／ CC-BY-4.0 |

**来源**：`.../lowRISC/opentitan/master/hw/ip/aes/data/*.hjson`、`.../riscv/riscv-isa-manual/main/src/{priv/csrs,priv/machine,license}.adoc`
**追溯链验证点**：`traces_to`（testplan → IP spec）、`feature → test → stage`

### 2.4 `safety/` — 功能安全 FMEA/FMEDA（6 文件，80 KB）

| 文件 | 字节 | 说明 |
|---|---|---|
| `neqsim-FMEA.md` | 1,671 | **IEC 60812 对齐**：S/O/D 三维评分 + `RPN = S·O·D` + 阈值分级（**RPN 字段最直接**） |
| `protective-stop-FMEDA.md` | 30,675 | 芯片/器件级 FMEDA：逐元件 λ(FIT)、失效模式、安全机制、诊断覆盖率、PFH |
| `cdriscv-FMEDA.md` | 7,582 | 由综合网表计算：SPFM/LFM/残留 FIT，逐 block λ/safe/SPF，MEASURED/ASSUMED/DERIVED 标注 |
| 三份 LICENSE | 11,324–11,353 | 均 Apache-2.0 |

**来源**：`.../equinor/neqsim/master/docs/safety/FMEA.md`、`.../polymathrobotics/protective-stop/main/docs/safety/FMEDA.md`、`.../ChipDesign-BV/cdriscv-32s-10/main/doc/fmeda.md`
**`table.failure_mode` 验证点**：失败模式/影响/严重度/检测方法/RPN

### 2.5 `ucis/` — UCIS XML 结构化数据（8 文件，64 KB）

| 文件 | 字节 | 说明 |
|---|---|---|
| `pyucis-toggle_2state.xml`／`pyucis-fsm_example.xml`／`pyucis-block_statement.xml`／`pyucis-branch_nested.xml`／`pyucis-assertion_cover.xml` | 858–1,618 | **真实 UCIS XML**（5 种覆盖类型：toggle/fsm/block/branch/assertion），形如 `<UCIS ucisVersion="1.0">` + `sourceFiles`/`historyNodes`/`instanceCoverages` |
| `fc4sc-coverage-results-gold.xml` | 12,431 | AMIQ fc4sc 金标准 UCIS XML（带 `ucis:` 命名空间，与规范示例同形） |
| `pyucis-LICENSE`／`fc4sc-LICENSE` | 11,357／11,358 | 均 Apache-2.0 |

**来源**：`.../fvutils/pyucis/master/tests/conversion/fixtures/xml/*.xml`、`.../amiq-consulting/fc4sc/master/examples/fir/coverage_results_gold.xml`
**`table.coverage_matrix` 验证点**：`feature`/`coverage_item`/`bin`/`status(hits, coverageCount)` 层级

## 3. 未获取的语料与原因

| 缺口 | 原因（实测） | 替代方案 |
|---|---|---|
| **vPlan XML**（Cadence/Siemens 专有导出格式） | 社区唯一样本（`kei-seu/I2C/.../questa_vplan.xml`）**仓库无 LICENSE** → 高风险，**不下载** | 用 **OpenTitan testplan**（`feature→test→stage` 结构等价）作许可清晰替身 |
| UPF 命令参考 | Accellera `/downloads/standards/upf` → **404**（已由 IEEE 1801 接管）；IEEE 付费墙 | 用 OpenSTA Commands.md（SDC 方向）替代 |
| SystemVerilog/VHDL 官方 LRM | Accellera 路径 404；IEEE 1800/1076 付费墙 | Verilator 文档（实现子集） |
| 官方 ISO 26262 / DO-254 / IEC 61508 原文 | 均为付费标准 | ECSS-Q-ST-30-02C（免费官方）+ NASA FMECA + 三份 Apache-2.0 真实 FMEDA |

## 4. 许可与合规

| 许可 | 语料 | 用途边界 |
|---|---|---|
| **BSD 式** | Tcl man pages | 明确许可 documentation 的 use/copy/distribute |
| **Apache-2.0** | OpenTitan、pyucis、fc4sc、neqsim、protective-stop、cdriscv | 可自由使用（含派生） |
| **CC-BY-4.0** | RISC-V ISA Manual | 署名即可 |
| **GPL-3.0** | OpenSTA Commands.md | **仅作测试 fixture**（不修改、不链接、不派生作品） |
| **LGPL-3.0/Artistic-2.0** | Verilator 文档 | 同上 |

> **合规声明**：GPL/LGPL 语料**仅用于本系统的导入/渲染测试**，不修改原文件、不与代码链接、不构成派生作品。若未来需分发含此语料的产物，需重新评估。

## 5. 验证边界（更新）

| doc_type | 真实语料 | 端到端验证 |
|---|---|---|
| `standard` | ✅ 7 份 | ✅ 已交付 |
| `lang` | ✅ 21 份 Tcl man + OpenSTA | **可达**（原始格式 `.n`/`.md`，需 importer 支持或转换） |
| `tool-manual` | ✅ Verilator 2 份 | **可达**（`.rst` 需转换） |
| `product` | ✅ OpenTitan 3 份 + RISC-V 2 份 | **可达**（`.hjson`/`.adoc` 需转换） |
| `safety` | ✅ 3 份 FMEA/FMEDA | **可达**（`.md`，可直接导入） |
| UCIS | ✅ 6 份 XML | **可达**（`importer/vplan.py` 可解析 UCIS XML） |
| **vPlan XML** | ❌ 无许可源 | **不可达**（仅接口 + 合成样例） |

**格式现实**：`safety/`（md）与 `ucis/`（xml）可**直接导入**；`lang`（nroff `.n`）、`tool-manual`（rst）、`product`（hjson/adoc）**需格式转换**才能进现有 markdown 解析器——这是后续工作项。

## 相关

- `doc_type_mapping.md`（类型映射与行业标准对齐）
- `../../../agent://IndividualTick`（完整调研报告，含全部候选与实测状态码）
