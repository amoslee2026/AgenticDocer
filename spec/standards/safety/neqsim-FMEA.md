---
title: "FMEA / FMECA Worksheet (IEC 60812)"
description: "Failure Modes and Effects Analysis using FMEAWorksheet — Severity, Occurrence and Detection scoring, RPN = S·O·D criticality ranking, and configurable threshold for hot-list filtering per IEC 60812."
type: composite
purpose: spec
audience: both
direction: input
version: "1.0.0"
section_meta: "@meta"
spec_id: SPEC-SAFE-NEQSIM-FMEA
spec_type: safety
spec_org: Equinor/neqsim
spec_revision: IEC-60812
source: https://raw.githubusercontent.com/equinor/neqsim/master/docs/safety/FMEA.md
converted_by: "download（原样下载，未转换）"
converted_at: 2026-09-17
reviewed_by: "lxx(下载授权)"
reviewed_at: 2026-09-17
status: approved
standard_ref: "IEC 60812（2018）"
audit_trail: "spec/standards/DOWNLOADED.md §2.4；Apache-2.0；2026-09-17 下载自 equinor/neqsim@master:docs/safety/FMEA.md"
---

# FMEA / FMECA Worksheet (IEC 60812)

`neqsim.process.safety.hazid.FMEAWorksheet` provides a Failure Modes, Effects
and Criticality Analysis worksheet aligned with IEC 60812 (2018). Each entry
captures the failure mode of a tagged component and its three risk dimensions.

## Risk Priority Number

$$
\mathrm{RPN} = S \cdot O \cdot D
$$

where each factor is on a 1–10 scale:

- **S** (Severity) — consequence severity if the mode occurs
- **O** (Occurrence) — likelihood of the mode
- **D** (Detection) — inverse detectability (10 = undetectable)

## Code pattern

```java
FMEAWorksheet fm = new FMEAWorksheet("Subsea Tree — XT-001");
fm.addEntry("PT-101", "Transmitter", "Drift high",
    "Sensor degradation",
    "Spurious ESD trip, lost production",
    4, 5, 3);    // S, O, D — RPN = 60
fm.addEntry("BDV-202", "Blowdown valve", "Fail to open",
    "Solenoid coil failure",
    "Cannot depressurize during fire — vessel rupture risk",
    9, 2, 6);    // RPN = 108

List<FMEAWorksheet.Entry> hotList = fm.criticalEntries(100); // RPN > 100
```

## Common thresholds

| Threshold | Action |
|-----------|--------|
| RPN > 200 | Mandatory mitigation — design change |
| RPN 100–200 | Mitigation recommended — added safeguard or inspection |
| RPN < 100 | Monitor in operating phase |

## See also

- [HAZOP Worksheet](HAZOP.md)
- [Event and Fault Trees](event_fault_trees.md)
