---
title: High Bandwidth Memory (HBM4) DRAM Standard (JESD270-4A)
source: corpus/01_raw/specifications/hbm/JEDEC_JESD270-4A_HBM4_2025.pdf
converted_by: mineru
converted_at: 2026-08-31
reviewed_by: lxx(批量导入授权)
reviewed_at: 2026-08-31
type: composite
purpose: spec
audience: both
direction: input
version: "1.0.0"
section_meta: "@meta"
spec_type: standard
spec_id: SPEC-STD-HBM4-JESD270-4A
spec_org: JEDEC
spec_revision: JESD270-4A
status: approved
---
# JEDEC STANDARD

# High Bandwidth Memory (HBM4) DRAM

JESD270-4A

(Revision of JESD270-4, April 2025)

November 2025

JEDEC SOLID STATE TECHNOLOGY ASSOCIATION

![](images/12a911655f67786fed6a863171690c6e424091316fe50327fc0ca047cea1b679.jpg)

## NOTICE

JEDEC standards and publications contain material that has been prepared, reviewed, and approved through the JEDEC Board of Directors level and subsequently reviewed and approved by the JEDEC legal counsel.

JEDEC standards and publications are designed to serve the public interest through eliminating misunderstandings between manufacturers and purchasers, facilitating interchangeability and improvement of products, and assisting the purchaser in selecting and obtaining with minimum delay the proper product for use by those other than JEDEC members, whether the standard is to be used either domestically or internationally.

JEDEC standards and publications are adopted without regard to whether or not their adoption may involve patents or articles, materials, or processes. By such action JEDEC does not assume any liability to any patent owner, nor does it assume any obligation whatever to parties adopting the JEDEC standards or publications.

The information included in JEDEC standards and publications represents a sound approach to product specification and application, principally from the solid state device manufacturer viewpoint. Within the JEDEC organization there are procedures whereby a JEDEC standard or publication may be further processed and ultimately become an ANSI standard.

No claims to be in conformance with this standard may be made unless all requirements stated in the standard are met.

All risk and liability relating to the use of JEDEC standards is assumed by the user, who agrees to indemnify and hold JEDEC harmless.

Inquiries, comments, and suggestions relative to the content of this JEDEC standard or publication should be addressed to JEDEC at the address below, or refer to www.jedec.org under Standards and Documents for alternative contact information.

Copyright © JEDEC Solid State Technology Association 2025. All rights reserved.

JEDEC retains the copyright on this material. By downloading this file the individual agrees not to charge for or resell the resulting material.

PRICE: Contact JEDEC 3103 10th Street North, Suite 240S, Arlington, VA 22201

DO NOT VIOLATE THE LAW!

This document is copyrighted by JEDEC and may not be reproduced without permission.

For information, contact:

JEDEC Solid State Technology Association

3103 10th Street North

Suite 240S

Arlington, VA 22201

https://www.jedec.org/contact

This page intentionally left blank

## High Bandwidth Memory (HBM4) DRAM

Pages   
Scope   
2 Features..   
3 Organization.   
3.1 Channel Definition.   
3.2 Channel Addressing .   
3.3 Simplified State Diagram . 8   
4 Initialization .... 10   
4.1 HBM4 Power-up and Initialization Sequence 10   
4.2 Initialization Sequence with Stable Power.. 13   
4.3 Controlled Power-off Sequence. . 15   
4.4 Initialization Sequence For Use Of IEEE 1500 Instruction Including Lane Repairs and   
Channel Disable 16   
5 Mode Registers 19   
6 Operation ....... .. 33   
6.1 HBM4 Clocking Overview. .. 33   
6.2 HBM4 Data Bus Inversion (DBIac) . 37   
6.3 Commands .. 41   
6.4 Parity .. . 101   
6.5 Clock Frequency Change Sequence..... . 108   
6.6 Catastrophic Temperature Sensor . . 108   
6.7 Interconnect Redundancy Remapping . 109   
6.8 HBM4 Loopback Test Modes.. . 119   
6.9 On-die DRAM ECC. . 134   
6.10 WOSC. . 146   
6.11 DCA and DCM . . 151   
6.12 Rx Offset Calibration Training . . 157   
6.13 Self Repair . 158   
7 Operating Conditions .... . 163   
7.1 Absolute Maximum DC Rating . 163   
7.2 Recommended DC Operating Condition . 163   
7.3 Operating Temperature . 165   
7.4 Electrostatic Discharge Characteristics. . 165   
8 Electrical Characteristics and DQ/CA Rx . . 166   
8.1 Leakage Current. . 166   
8.2 Capacitance.. . 167   
8.3 DQ Rx Voltage and Timings . 168   
8.4 AWORD Signaling . . 172   
8.5 CK and WDQS Input Signaling. . 172

## High Bandwidth Memory (HBM4) DRAM

## Contents

8.6 Midstack Signaling . . 174   
8.7 Transmit Driver Resistance.. . 174   
8.8 Output Timing Reference Load . . 175   
8.9 Output Voltage Level. . 175   
8.10 Output Rise and Fall Time . 175   
8.11 Overshoot/Undershoot . . 176   
9 IDD Specification .... . 177   
9.1 IDD and IPP Specification Parameters and Test Conditions . . 177   
9.2 IDD and IPP Specifications . 188   
9.3 IDD6 Specification . . 189   
10 AC Timings... . 190   
11 Package (Die) Specification. . 200   
11.1 Signals.. . 200   
11.2 MicroBump Positions . . 202   
11.3 HBM4 Device Dimensions . 203   
11.4 HBM4 Bump Map ... . 204   
12 HBM DRAM Assembly . .. 211   
13 Test and Boundary Scan ... . 212   
13.1 Direct Access (DA) Test Port . 212   
13.2 IEEE Standard 1500. . 213   
13.3 Wrapper Data Register (WDR) Types ..... . 217   
13.4 IEEE1500 Test Access Port Instruction Encodings. . 218   
13.5 Test Instructions.. . 219   
13.6 Interaction with Mission Mode Operation . . 261   
13.7 IEEE1500 Test Port AC Timing Parameters . 262   
13.8 Boundary Scan. . 268   
Annex A — (Informative) Difference between Document Revisions .. .. 269   
A.1 Differences between JESD270-4A and JESD270-4 (April 2025) . 269

## High Bandwidth Memory (HBM4) DRAM

## Tables

## List of Tables

Pages   
Table 1 — Single Channel Signal Count . 3   
Table 2 — Global Signal Count ...   
Table 3 — Array Access Timings Counted Individually Per Pseudo Channel . 5   
Table 4 — HBM4 Channel Addressing . 6   
Table 5 — Bank Group Assignments..   
Table 6 — Command Sequence Affected by Bank Groups.   
Table 7 — Initialization Timing Parameters. ..12   
Table 8 — Power Supply Conditions. .15   
Table 9 — HBM4 Mode Register Overview .20   
Table 10 — Mode Register 0 (MR0) ..21   
Table 11 — Mode Register 1 (MR1) ..21   
Table 12 — Mode Register 2 (MR2) . ..22   
Table 13 — Mode Register 3 (MR3) .22   
Table 14 — Mode Register 4 (MR4) ..22   
Table 15 — Mode Register 5 (MR5) ..23   
Table 16 — Mode Register 6 (MR6) ..23   
Table 17 — Mode Register 7 (MR7) .. ..24   
Table 18 — DWORD MISR Read and Write Operations in Loopback Test Mode (MR7 OP0=1 ..25   
Table 19 — Mode Register 8 (MR8) . ..26   
Table 20 — Mode Register 9 (MR9) ............... ..27   
Table 21 — Mode Register 10 (MR10) ..28   
Table 22 — Mode Register 11 (MR11) ..29   
Table 23 — Mode Register 12 (MR12) .29   
Table 24 — Mode Register 13 (MR13) ..30   
Table 25 — Mode Register 14 (MR14) ..30   
Table 26 — Mode Register 15 (MR15) ..31   
Table 27 — Mode Register 16 (MR16) ..31   
Table 28 — Mode Register 17 (MR17) ..31   
Table 29 — Mode Register 18 (MR18) ..31   
Table 30 — Mode Register 19 (MR19) ..32   
Table 31 — Phase Detector and DERR Signal Behavior.. ..35   
Table 32 — DBI(ac) Truth Table.. ..38   
Table 33 — Row Commands Truth Table.. ..42   
Table 34 — Column Commands Truth Table ..43   
Table 35 — Options for Issuing PREab and PREpb Commands. ..44   
Table 36 — Precharge and Auto Precharge Timings . ..52   
Table 37 — Refresh Counter Increments (Example) ..59   
Table 38 — REFab and REFpb Command Scheduling Requirements. ..60   
Table 39 — Mode Register Definition for Adaptive RFM Levels... ..63

## High Bandwidth Memory (HBM4) DRAM

## Tables (cont'd)

Table 40 — RFM Commands Perceived by HBM4 DRAM . ..64   
Table 41 — Command to Command Timings with DRFM Enabled . ...68   
Table 42 — Bounded Refresh Configuration and tDRFM Timings. ..69   
Table 43 — Signal Groups for Read Data De-Skew . ...80   
Table 44 — Signal Groups for Write Data De-Skew . ....88   
Table 45 — Pin State Description in Power Down ...94   
Table 46 — Pin State Description in Self Refresh.. ..100   
Table 47 — Command/Address Parity Function Table.. ..101   
Table 48 — Data Parity Function Table . ..105   
Table 49 — AWORD - Row Command Bus Remapping. ..110   
Table 50 — AWORD - Column Command Bus Remapping . .111   
Table 51 — Original Lane Assignment - Channel 0 - AWORD Column Repair . ..111   
Table 52 — Remapped Lane Assignment - Channel 0 - AWORD Column Repair ..111   
Table 53 — Original Lane Assignment - Channel 0 - AWORD Row Repair. ..112   
Table 54 — Remapped Lane Assignment - Channel 0 - AWORD Row Repair. ...112   
Table 55 — DWORD Remapping (1 Byte). ..113   
Table 56 — Original DWORD Lane Assignment - Channel 0 – Byte [1:0] . ..114   
Table 57 — Remapped DWORD Lane Assignment - Channel 0 – Byte [1:0] . ..114   
Table 58 — WSO Remapping...... ..117   
Table 59 — Original Lane Assignment – WSO Repair . ..118   
Table 60 — Remapped Lane Assignment – WSO Repair ..118   
Table 61 — MISR Function Table...... ..120   
Table 62 — WDBI, ECC, and SEV Signals during Loopback and Normal Mission Modes ..124   
Table 63 — Mode Registers Associated with Auto ECS ..136   
Table 64 — t per Stack (ECS Independent of SID) ...137   
Table 65 — Error Overwrite Priority Rules to Handle Multiple Error Logging . ..139   
Table 66 — ECS Flag Behavior.. ..140   
Table 67 — Transparency Attributes and Their Access/Control Mechanism ..141   
Table 68 — Severity Encodings on the SEV pins ..141   
Table 69 — Severity Transmission on READ. ..141   
Table 70 — ECC Engine Test Modes. ..142   
Table 71 — Example of Error Vectors and Corresponding Severity... ..144   
Table 72 — WDQS Oscillator Matching Error Specification. ..150   
Table 73 — DCA Maximum Offset and Step Size. ..151   
Table 74 — Read DCA Maximum Offset and Step Size . ...153   
Table 75 — DCM Measurement Result. ..155   
Table 76 — DCM Output Example ..156   
Table 77 — Duty Cycle Monitor Timing. ..156   
Table 78 — MR6 OP[7:6], DCM Control . ..156   
Table 79 — Rx Offset Calibration Training Time Parameter ..157

## High Bandwidth Memory (HBM4) DRAM

## Tables (cont'd)

Table 80 — SELF\_REP Instruction vs Stack Height . ..158   
Table 81 — SELF\_REPAIR Timings. ..159   
Table 82 — SELF\_REP – Expected DRAM Behavior When Resources Shared . ..161   
Table 83 — Absolute Maximum DC Ratings.. ..163   
Table 84 — Recommended DC Operating Condition. ...164   
Table 85 — Operating Temperature. ..165   
Table 86 — Electrostatic Discharge Characteristics. ..165   
Table 87 — Input Leakage Current. ..166   
Table 88 — Input/Output Capacitance. .167   
Table 89 — Input Receiver Voltage Level and Timings Specification ...169   
Table 90 — AWORD Receiver Voltage Level Specification. ..172   
Table 91 — CK and WDQS Input Voltage Level Specification. ..172   
Table 92 — Differential Input Level for WDQS\_t, WDQS\_c... ..173   
Table 93 — Differential Input Slew Rate Definition for WDQS\_t, WDQS\_c. ..173   
Table 94 — Midstack Parameter Specification .... ..174   
Table 95 — Transmit Driver Resistance Specification . ..174   
Table 96 — Output Voltage Level .... ..175   
Table 97 — Overshoot/Undershoot Specification for AWORD and DWORD Signals . ..176   
Table 98 — Basic IDD/IDDQ/IPP/IDDQL Measurement Conditions... ..178   
Table 99 — Example of Timings used for IDD Measurement-Loop Pattern ...180   
Table 100 — IDD0 Measurement-Loop Pattern.. ..181   
Table 101 — IDD4R Measurement-Loop Pattern ..182   
Table 102 — IDD4W Measurement-Loop Pattern. ..184   
Table 103 — IDD5P Measurement-Loop Pattern ..186   
Table 104 — IDD7 Measurement-Loop Pattern... ..187   
Table 105 — IDD and IPP Specification Example. ..188   
Table 106 — IDD6 Specification.. ..189   
Table 107 — Timings Parameters ..190   
Table 108 — Timings Parameters (Part 2). .194   
Table 109 — I/O Signal Description...... ...200   
Table 110 — Geometric Parameters of the Staggered MicroBump Pattern . ..202   
Table 111 — HBM4 Device Dimensions . ..203   
Table 112 — HBM4 Bump Map Footprint A – Geographical Overview (not to scale) ..205   
Table 113 — HBM4 Bump Map Footprint B – Geographical Overview (not to scale) ..206   
Table 114 — HBM4 Footprint A and Footprint B Signal Compatibility ..209   
Table 115 — Direct Access (DA) Pin Allocation. ..212   
Table 116 — Test Access Port Signal Status. ..214   
Table 117 — IEEE1500 Test Port Signal List and Description . ..214   
Table 118 — WIR Channel Selection Definition ..218   
Table 119 — WIR Channel Selection Definition ...218

## High Bandwidth Memory (HBM4) DRAM

## Tables (cont'd)

Table 120 — Instruction Register Encodings .219   
Table 121 — BYPASS Wrapper Data Register. .221   
Table 122 — Wrapper Boundary Register (WBR). .223   
Table 123 — HBM\_RESET Wrapper Data Register . .227   
Table 124 — RESET\_n and HBM\_RESET Truth Table. .228   
Table 125 — MBIST Wrapper Data Register.. .228   
Table 126 — SOFT\_REPAIR Wrapper Data Register .230   
Table 127 — HARD\_REPAIR Wrapper Data Register. .231   
Table 128 — DWORD\_MISR Wrapper Data Register .232   
Table 129 – AWORD\_MISR Wrapper Data Register.. .235   
Table 130 — CHANNEL\_ID Wrapper Data Register . .236   
Table 131 — AWORD\_MISR\_CONFIG Wrapper Data Register . .237   
Table 132 — DEVICE\_ID Wrapper Data Register. .239   
Table 133 — TEMPERATURE Wrapper Data Register ... .243   
Table 134 — MODE\_REGISTER\_DUMP\_SET Wrapper Data Register. ..244   
Table 135 — READ\_LFSR\_COMPARE\_STICKY Wrapper Data Register ... ..247   
Table 136 — LANE\_REPAIR Wrapper Data Register .......... .249   
Table 137 — CHANNEL\_DISABLE Wrapper Data Register .252   
Table 138 — CHANNEL\_TEMPERATURE Wrapper Data Register ..253   
Table 139 — WOSC\_RUN Wrapper Data Register ...... .255   
Table 140 — WOSC\_COUNT Wrapper Data Register. .255   
Table 141 — ECS Error Log Wrapper Data Register . .257   
Table 142 — HS\_REP\_CAP Wrapper Data Register ..258   
Table 143 — SELF\_REP Wrapper Data Register... ..260   
Table 144 — SELF\_REP\_RESULTS Wrapper Data Register . ..260   
Table 145 — IEEE1500 Port Instruction Interactions.. ..261   
Table 146 — IEEE1500 Test Port AC Timings .262

## High Bandwidth Memory (HBM4) DRAM

## Figures

## List of Figures List of Figures

Pages   
Figure 1 — Example Logical Overview of an HBM4 Device .2   
Figure 2 — Pseudo Channel Operation. .5   
Figure 3 — Simplified State Diagram .9   
Figure 4 — Recommended Power-up and Controlled Power-off Sequence 11   
Figure 5 — Power-up and Initialization. ..13   
Figure 6 — HBM4 RESET and Initialization Sequence with Stable Power ..14   
Figure 7 — Initialization Sequence with Lane Repair or Channel Disable . ...17   
Figure 8 — Initialization Sequence with Channel Disable. ..18   
Figure 9 — Aligned WDQS Internal Divider Example . ..33   
Figure 10 — Clocking and Interface Relationship Write to Read Timing ..34   
Figure 11 — High Level Block Diagram Example of Clocking Scheme.... ..34   
Figure 12 — DERR Signal Behavior in WDQS-to-CK Alignment Training. ...36   
Figure 13 — DBIac Algorithm.... ...37   
Figure 14 — Example DBIac Logic for Write and Read ... ...38   
Figure 15 — Internal DBIac State Reset for Write to Read .... ..39   
Figure 16 — Bus Preconditioning and DBI States for Read ... ...40   
Figure 17 — RNOP Command ..... ...45   
Figure 18 — ACTIVATE Command. ..47   
Figure 19 — Bank and Row Activation Command Cycle . ...48   
Figure 20 — Multiple Bank Activations...... ..49   
Figure 21 — PRECHARGE (PREpb) Command ...50   
Figure 22 — PRECHARGE ALL (PREab) Command. ..50   
Figure 23 — REFRESH All-bank Command (REFab). ...55   
Figure 24 — REFab Cycle .... ...56   
Figure 25 — Postponing Refresh Commands (Example) ..56   
Figure 26 — REFRESH per-bank Command (REFpb) . ...57   
Figure 27 — REFpb Command Cycle . ..58   
Figure 28 — Sets of REFpb Commands. ...58   
Figure 29 —RFMab and RFMpb Commands ...61   
Figure 30 — ACTIVATE with DRFM Bit ..65   
Figure 31 — Multiple ACTIVATE with DRFM Bit to Same Bank before DRFM Command. ...66   
Figure 32 — ACTIVATE with DRFM Bit to Open Page (Same Bank and Row Address) ..67   
Figure 33 — CNOP Command .. ..70   
Figure 34 — READ Command . ...71   
Figure 35 — Clock to RDQS and Data Out Timing ..73   
Figure 36 — Single Read Burst with BL = 8.. ..74   
Figure 37 — Seamless Read Bursts with BL = 8 . ..75   
Figure 38 — Non-Seamless Read Bursts with t<sub>CCD</sub> = 3 and BL = 8.. ..76   
Figure 39 — Non-Seamless Read Burst with t = 4 and BL = 8 ... ..77

## High Bandwidth Memory (HBM4) DRAM

## Figures (cont'd)

Figure 40 — Read to Write . ..78   
Figure 41 — Read to Precharge . ..79   
Figure 42 — Write Command.. ..81   
Figure 43 — Clock to WDQS and Data Input Timings ..82   
Figure 44 — Single Write Burst with BL=8 ..... ...83   
Figure 45 — Seamless Write Bursts with BL=8. ..84   
Figure 46 — Non-seamless Write Bursts... ...85   
Figure 47 — Write to Read .. ..86   
Figure 48 — Write to Pre-charge . ..87   
Figure 49 — Mode Register Set Command (MRS).. ...89   
Figure 50 — Mode Register Set Timings . ..90   
Figure 51 — Power-Down Entry Command . ...91   
Figure 52 — Power-Down Entry and Exit. ..93   
Figure 53 — READ or READ with Auto Precharge to Power-Down Entry Timing. ..94   
Figure 54 — WRITE or WRITE with Auto Precharge to Power-Down Entry Timing.. ...95   
Figure 55 — MODE REGISTER SET to Power-Down Entry Timing .. ..95   
Figure 56 — ACTIVATE to Power-Down Entry Timing............ ...96   
Figure 57 — REFab or REFpb to Power-Down Entry Timing. ..96   
Figure 58 — PRECHARGE to Power-Down Entry Timing.... ..96   
Figure 59 — Self-Refresh Entry Command... ...97   
Figure 60 — Self-Refresh Entry and Exit. ..99   
Figure 61 — Enabling and Disabling Command/Address Parity ..101   
Figure 62 — Single Command/Address Parity Error. .102   
Figure 63 — Separated Command/Address Parity Errors.. ..102   
Figure 64 — Consecutive Command/Address Parity Errors.. ..103   
Figure 65 — Write Parity Errors with PL = 2. .105   
Figure 66 — Write Parity Alignment with PL = 2 ..106   
Figure 67 — Write Parity Alignment with PL = 4 ..106   
Figure 68 — Read Parity Alignment with PL = 2 . .107   
Figure 69 — Read Parity Alignment with PL = 4 .... ..107   
Figure 70 — Example Signal Paths with Lane Repair .. .115   
Figure 71 — MISR Features Block Diagram of HBM4. ..119   
Figure 72 — Example of 4 bit MISR-LFSR Implementing $\mathbf { f ( x ) } = \mathbf { X ^ { 4 } } + \mathbf { X ^ { 3 } } + 1$ ..120   
Figure 73 — AWORD MISR Modes Preamble Clock Filter Behavior.. ..126   
Figure 74 — DWORD Write MISR Modes Behavior . ..127   
Figure 75 — DWORD Read LFSR Modes Behavior .131   
Figure 76 — LFSR Compare Mode Block Diagram... ..132   
Figure 77 — On-die ECC Overview Diagram Example . ..134   
Figure 78 — ECS Operation Timing .137   
Figure 79 — tECSint ...... ..138

## High Bandwidth Memory (HBM4) DRAM

## Figures (cont'd)

Figure 80 — REFab with ECS Flag Supported . .140   
Figure 81 — ECS CEs Output Enable Timing for SEV Signaling . .142   
Figure 82 — The Block Diagram of On-die ECC Engine and Path for ECC Engine Test Mode ..143   
Figure 83 — Timing Diagram of ECC Engine Test Mode ..145   
Figure 84 — Oscillator Offset $( \mathrm { W O S C _ { o f f s e t ( V ) } } )$ ..148   
Figure 85 — Oscillator Offset $\mathrm { ( W O S C _ { o f f s e t ( T ) } ) }$ ..149   
Figure 86 — Duty Cycle Adjuster Range . .151   
Figure 87 — Relationship Between WDQS Waveform and DCA Code Change (Example) ..152   
Figure 88 — DCA Training Block Diagram. .153   
Figure 89 — Example of Relationship between WDQS Waveform and RDQS\_t/c and DQ Output ..........154   
Figure 90 — Example Sequence for WDQS Duty Cycle Correction . ..156   
Figure 91 — Rx Offset Calibration Training Timing. ..157   
Figure 92 — Self Repair Flowchart ..162   
Figure 93 — DQ Receiver Mask.. ..168   
Figure 94 — Across DQ V<sub>REFD</sub> Voltage Variation ..168   
Figure 95 — DQ to WDQS Timings (t<sub>WDQS2DQ\_I</sub>, $\mathbf { t } _ { \mathrm { D Q 2 D Q t r a \_ I } }$ and $\mathbf { t } _ { \mathrm { D Q 2 D Q t e r \_ I } } )$ at DRAM Pins Referenced   
from the Internal Latch. ..170   
Figure 96 — Read Data Timing Definitions of t<sub>DQ2DQtra</sub>\_<sub>O</sub>, t<sub>DQ2DQter</sub>\_<sub>O</sub>, and t<sub>DQSQtra</sub>\_ ..171   
Figure 97 — CA Single Pulse Amplitude and Pulse Width.. ..172   
Figure 98 — CK Single Pulse ... ..173   
Figure 99 — Differential Input Slew Rate Definition for WDQS\_t, WDQS\_c ..173   
Figure 100 — Timing Reference Load ........ ..175   
Figure 101 — Output Rise and Fall Definition. ..175   
Figure 102 — Overshoot, Undershoot Definition ..176   
Figure 103 — Measurement Setup for IDD and IPP Measurements . ..178   
Figure 104 — Staggered MicroBump Pattern ..202   
Figure 105 — MicroBump Pillar Diameter ... ...202   
Figure 106 — Figure Overview of HBM4 Bump Map Footprint. ..204   
Figure 107 — Overview of HBM4 Bump Map Footprint A.. ..207   
Figure 108 — Overview of HBM4 Bump Map Footprint B. ..208   
Figure 109 — Overview of HBM4 Bump Map Footprint Compatibility (Overlapping Bumps are   
Highlighted)..... ..210   
Figure 110 — DA Port Connection Diagram For Multiple HBM4 DRAM Devices ..213   
Figure 111 — IEEE Std. 1500 Logic Diagram. ..215   
Figure 112 — WIR Channel Select Logic Diagram ..215   
Figure 113 — IEEE1500 Port Operation . ..216   
Figure 114 — RESET\_n and HBM\_RESET Logic ..227   
Figure 115 — Registers Associated with Lane Repair Instructions. ..250   
Figure 116 — Channel Disable Instruction. ..251   
Figure 117 — Example Channel Configuration 1 ..254   
Figure 118 — Example Channel Configuration 2 ...254

## High Bandwidth Memory (HBM4) DRAM

## Figures (cont'd)

Figure 119 — IEEE1500 Port Input and Output Timings.... .265   
Figure 120 — IEEE1500 EXTEST\_RX and EXTEST\_TX Instruction Related Timings... .265   
Figure 121 — IEEE1500 SOFT\_REPAIR and HARD\_REPAIR Instruction Related Timings. .265   
Figure 122 — IEEE1500 Soft\_Lane\_Repair and Hard\_Lane\_Repair Instruction Related Timings . ......266   
Figure 123 — IEEE1500 DWORD\_MISR / AWORD\_MISR Instruction Related Timings . .266   
Figure 124 — IEEE1500 CHANNEL\_ID Instruction Related Timings.. .266   
Figure 125 — IEEE1500 MODE\_REGISTER\_DUMP\_SET Instruction Related Timings . .267

<table><tr><td>1 Scope</td><td></td></tr></table>

# High Bandwidth Memory (HBM4) DRAM

(From JEDEC Board Ballot JCB-25-75, formulated under the cognizance of the JC-42.2 Subcommittee on High Bandwidth Memory (HBM), item number 1883.98C).

The HBM4 DRAM is tightly coupled to the host compute die with a distributed interface. The interface is divided into independent channels. Each channel is completely independent of one another. Channels are not necessarily synchronous to each other. The HBM4 DRAM uses a wide-interface architecture to achieve high-speed, low power operation. Each channel interface maintains a 64 bit data bus operating at double data rate (DDR).

## 2 Features

• 256 bit prefetch per memory read and write access

• BL = 8

• 64 DQ width + ECC/SEV pins support / channel

• Pseudo Channel (PC) mode operation; 32 DQ width for PC mode

• Differential clock inputs (CK\_t/CK\_c) for command/address

Double data rate (DDR) command/address. Row Activate commands require one-and-a-half-cycle, all other row commands require a half-cycle except for PDE, SRE with one cycle. Column command require only one cycle

• Semi-independent row and column command interfaces allowing Activates/Precharges to be issued in parallel with Read/Writes

Data referenced to unidirectional differential data strobes RDQS\_t/RDQS\_c and WDQS\_t/WDQS\_c. One strobe pair each per DWORD

• Up to 32 channels / device

• Channel density of 3 Gb to 16 Gb

• 16, 32, 48 or 64 banks per channel; varies by device density / channel

• Bank grouping supported

• 1 KB page size per pseudo channel (PC)

• DBIac support configurable via MRS

• Self refresh modes

• Vendor Specific I/O voltage, Tx driver voltage 0.4 V

• DRAM core voltage 1.05 V, independent of I/O voltage

Unterminated data/address/command/clock interfaces

• Unmatched data interfaces

<table><tr><td>3 Organization</td></tr></table>

HBM4 DRAM is optimized for high-bandwidth operation utilizing several independent interfaces called channels (CH). Each channel is further segmented into semi-independent pseudo channels (PC).

Each HBM4 stack will support up to 32 channels. Figure 1 shows an example stack containing 8 DRAM dies, each die supporting 8 independent channels with 2 pseudo channels per channel. Each die contributes additional capacity and additional channels to the stack (up to a maximum of 32 channels per stack or 64 pseudo channels). HBM4 requires 4 DRAM dies to support 32 channels. Additional DRAM dies beyond 4 add additional capacity, SIDs and additional banks per pseudo channel. HBM4 can support stacks of either 4, 8, 12, or 16 DRAM dies. See Channel Addressing clause for more details.

![](images/e46837609914d2d44f91d4f2d35e08ac171edbeee22fd890bd5484ed82f9f8c8.jpg)  
Figure 1 — Example Logical Overview of an HBM4 Device

The DRAM vendor may choose to require an optional interface die that sits at the bottom of the stack and provides signal redistribution and other functions. The vendor may choose to implement many of the logic functions typically found on DRAM die on this logic die. This standard does not explicitly require nor prohibit such a solution.

The division of channels and pseudo channels among the DRAM dies within a stack is left to the vendor.   
Figure 1, with the memory for eight channels implemented on each die, is not a required organization.   
Organizations are permitted where the memory for a single channel is distributed among multiple dies;   
however, all accesses within a single channel must have the same latency for all accesses.

## 3.1 Channel Definition

Each channel consists of an independent command and data interface. RESET\_n, CATTRIP, IEEE1500 test port and power supply signals are common to all channels. Channels are independently clocked, and need not to be synchronous, however the clock is shared between both pseudo channels in a channel.

Since each channel is independent, much of this standard will describe a single channel. Where signal names are involved, families of signals belonging to a given channel will have the suffix 0, 1, …, 31 for channels 0 through 31. If no suffix is present, the signal(s) being described are generic instances of the various per-channel signals.

## 3.1.1 Signal Count

Table 1 — Single Channel Signal Count
<table><tr><td rowspan=1 colspan=1>Function</td><td rowspan=1 colspan=1>Number ofMicrobumps</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Data</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>DQ[63:0]</td></tr><tr><td rowspan=1 colspan=1>Column command/ Address</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>C[7:0]</td></tr><tr><td rowspan=1 colspan=1>Row command/ Address</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>R[9:0]</td></tr><tr><td rowspan=1 colspan=1>DBI</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>1 DBI per 8 DQs</td></tr><tr><td rowspan=1 colspan=1>ECC</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>2 ECC per 32 DQs</td></tr><tr><td rowspan=1 colspan=1>SEV</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>2 SEV per 32 DQs</td></tr><tr><td rowspan=1 colspan=1>DPAR</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>1 PAR per 32 DQs</td></tr><tr><td rowspan=1 colspan=1>APAR</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1 PAR per AWORD</td></tr><tr><td rowspan=1 colspan=1>DERR</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>1 DERR per 32 DQs</td></tr><tr><td rowspan=1 colspan=1>Strobe</td><td rowspan=1 colspan=1>8        1</td><td rowspan=1 colspan=1>1 RDQS_t/RDQS_c, WDQS_t/WDQS_c per 32 DQs</td></tr><tr><td rowspan=1 colspan=1>Clock</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>CK_t/CK_c</td></tr><tr><td rowspan=1 colspan=1>AERR</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>AERR per AWORD</td></tr><tr><td rowspan=1 colspan=1>Redundant Data</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>RD[3:0]</td></tr><tr><td rowspan=1 colspan=1>Redundant Address</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Redundant row / column</td></tr><tr><td rowspan=1 colspan=1>RFU</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1 RFU per AWORD</td></tr><tr><td rowspan=1 colspan=1>Total</td><td rowspan=1 colspan=1>120</td><td rowspan=1 colspan=1></td></tr></table>

## 3.1.1 Signal Count (cont’d)

Table 2 — Global Signal Count
<table><tr><td rowspan=1 colspan=1>Function</td><td rowspan=1 colspan=1>Number ofMicrobumps</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>RESET n</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Global Stack Reset</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>WRCK</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>IEEE1500 Clock</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>WRST_n</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>IEEE1500 only Reset</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>WSI</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>IEEE1500 Serial Input</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>SelectWIR</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>IEEE1500 Select WIR</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>CaptureWR</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>IEEE1500 Capture WR</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>ShiftWR</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>IEEE1500 Shift WR</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>UpdateWR</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>IEEE1500 Update WR</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>WSO</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>1 IEEE1500 Serial Output Per Channel [0:31]</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>RM</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Redundant WSO</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>CATTRIP</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Catastrophic Temperature Sensor</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>MRFU</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Midstack RFU</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Total</td><td rowspan=1 colspan=1>56</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=4>NOTE 1Duplicate microbumps for link redundancy.</td></tr></table>

## 3.1.2 Pseudo Channel Definition

A Pseudo channel (PC) divides a channel into two individual sub-channels of 32 DQ each, providing 256 bit prefetch per memory read and write access for each pseudo channel. Each pseudo-channel provides access to an independent set of DRAM banks of a defined page size. Requests from one pseudo-channel may not access data attached to a different pseudo-channel.

Both pseudo channels operate semi-independent. They share the channel’s row and column command bus as well as CK inputs, but decode and execute commands individually as illustrated in Figure 2. Address PC is used to direct commands to either to pseudo channel 0 (PC = 0) or pseudo channel 1 (PC = 1). Power-down and self refresh are common to both pseudo channels. All I/O signals of DWORD0 are associated with pseudo channel 0, and all I/O signals of DWORD1 with pseudo channel 1.

Array access timings as listed in the table below are applicable for each individual pseudo channel. For example, an ACTIVATE to PC0 can be followed by an ACTIVATE to PC1 as shown in Figure 2. However, a subsequent ACTIVATE to PC0 can only be done after tRRD (PC0). For commands that are common to both pseudo channels (PDE, PDX, SRE, SRX and MRS), it is required that the respective timing conditions are met by both pseudo channels when issuing that command. Both pseudo channels also share the channel’s mode registers.

Table 3 — Array Access Timings Counted Individually Per Pseudo Channel
<table><tr><td rowspan=1 colspan=1>Array Timing Group</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Row Access Timings</td><td rowspan=1 colspan=1>tRC, tRAS, tRCDRD, tRCDWR, tRRDL, tRRDS, tFAW, tRTP, tRP, twR</td></tr><tr><td rowspan=1 colspan=1>Column Access Timings</td><td rowspan=1 colspan=1>tCCDL, tCCDS, tCCDR, twTRL, tWTRS, tRTW</td></tr><tr><td rowspan=1 colspan=1>Refresh Timings</td><td rowspan=1 colspan=1>tRFC, tRFCPB, tRREFD, tREFI, tREFIPB, tRTW</td></tr></table>

![](images/35a8ac68ef18e87d5703f5c0c20044a4b588f3d59a311f979ff0ad9a531e40cd.jpg)  
Figure 2 — Pseudo Channel Operation

## 3.1.3 Dual Command Interfaces

To enable higher performance, HBM4 DRAMs exploit the increase in available signals to provide semiindependent row and column command interfaces for each channel. These interfaces increase command bandwidth and performance by allowing read and write commands to be issued simultaneously with other commands like activates and precharges. See Commands section.

## 3.2 Channel Addressing

Table 4 — HBM4 Channel Addressing
<table><tr><td rowspan=1 colspan=1>Configuration</td><td rowspan=1 colspan=1>24Gb 4H⁸</td><td rowspan=1 colspan=1>24Gb 8H</td><td rowspan=1 colspan=1>24Gb 12H</td><td rowspan=1 colspan=1>24Gb 16H</td><td rowspan=3 colspan=1>Note</td></tr><tr><td rowspan=1 colspan=1>Density per Channel</td><td rowspan=1 colspan=1>3Gb</td><td rowspan=1 colspan=1>6Gb</td><td rowspan=1 colspan=1>9Gb</td><td rowspan=1 colspan=1>12Gb</td></tr><tr><td rowspan=1 colspan=1>Density per PC</td><td rowspan=1 colspan=1>1.5Gb</td><td rowspan=1 colspan=1>3Gb</td><td rowspan=1 colspan=1>4.5Gb</td><td rowspan=1 colspan=1>6Gb</td></tr><tr><td rowspan=1 colspan=1>Prefetch Size per PC (bits)</td><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=1>Row Address</td><td rowspan=1 colspan=1>RA[13:0]5</td><td rowspan=1 colspan=1>RA[13:0]5</td><td rowspan=1 colspan=1>RA[13:0]5</td><td rowspan=1 colspan=1>RA[13:0]5</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Column Address</td><td rowspan=1 colspan=1>CA[4:0]</td><td rowspan=1 colspan=1>CA[4:0]</td><td rowspan=1 colspan=1>CA[4:0]</td><td rowspan=1 colspan=1>CA[4:0]</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Bank Address</td><td rowspan=1 colspan=1>BA[3:0]</td><td rowspan=1 colspan=1>SID[0],BA[3:0]</td><td rowspan=1 colspan=1>SID[1:0] 6,BA[3:0]</td><td rowspan=1 colspan=1>SID[1:0],BA[3:0]</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Page Size per PC</td><td rowspan=1 colspan=1>1KB</td><td rowspan=1 colspan=1>1KB</td><td rowspan=1 colspan=1>1KB</td><td rowspan=1 colspan=1>1KB</td><td rowspan=1 colspan=1>1,3</td></tr><tr><td rowspan=1 colspan=1>Density Code</td><td rowspan=1 colspan=1>0000</td><td rowspan=1 colspan=1>0010</td><td rowspan=1 colspan=1>0100</td><td rowspan=1 colspan=1>0110</td><td rowspan=1 colspan=1>8</td></tr><tr><td rowspan=1 colspan=1>Configuration</td><td rowspan=1 colspan=1>32Gb 4H⁸</td><td rowspan=1 colspan=1>32Gb 8H</td><td rowspan=1 colspan=1>32Gb 12H</td><td rowspan=1 colspan=1>32Gb 16H</td><td rowspan=3 colspan=1>Note</td></tr><tr><td rowspan=1 colspan=1>Density per Channel</td><td rowspan=1 colspan=1>4Gb</td><td rowspan=1 colspan=1>8Gb</td><td rowspan=1 colspan=1>12Gb</td><td rowspan=1 colspan=1>16Gb</td></tr><tr><td rowspan=1 colspan=1>Density per PC</td><td rowspan=1 colspan=1>2Gb</td><td rowspan=1 colspan=1>4Gb</td><td rowspan=1 colspan=1>6Gb</td><td rowspan=1 colspan=1>8Gb</td></tr><tr><td rowspan=1 colspan=1>Prefetch Size per PC (bits)</td><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=1>Row Address</td><td rowspan=1 colspan=1>RA[13:0]</td><td rowspan=1 colspan=1>RA[13:0]</td><td rowspan=1 colspan=1>RA[13:0]</td><td rowspan=1 colspan=1>RA[13:0]</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Column Address</td><td rowspan=1 colspan=1>CA[4:0]</td><td rowspan=1 colspan=1>CA[4:0]</td><td rowspan=1 colspan=1>CA[4:0]</td><td rowspan=1 colspan=1>CA[4:0]</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Bank Address</td><td rowspan=1 colspan=1>BA[3:0]</td><td rowspan=1 colspan=1>SID[0],BA[3:0]</td><td rowspan=1 colspan=1>SID[1:0]6,BA[3:0]</td><td rowspan=1 colspan=1>SID[1:0],BA[3:0]</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Page Size per PC</td><td rowspan=1 colspan=1>1KB</td><td rowspan=1 colspan=1>1KB</td><td rowspan=1 colspan=1>1KB</td><td rowspan=1 colspan=1>1KB</td><td rowspan=1 colspan=1>1,3</td></tr><tr><td rowspan=1 colspan=1>Density Code</td><td rowspan=1 colspan=1>0001</td><td rowspan=1 colspan=1>0011</td><td rowspan=1 colspan=1>0101</td><td rowspan=1 colspan=1>0111</td><td rowspan=1 colspan=1>7</td></tr><tr><td rowspan=1 colspan=6>NOTE 1Prefetch size and page size reflect the effective addressing along with row and column commands.Both do not include the optional ECC bits as described in Channel Definition clause.NOTE 2 The burst order is fixed for Reads and Writes, and the HBM device does not assign column addressbits to distinguish between the eight UI of a BL8 burst. A memory controller may internally assignsuch column address bits but those column address bits are not transmitted to the HBM device.NOTE 3Page Size = 2CoLBITs x (Prefetch Size / 8); where COLBITS is the number of column address bits.Page size and prefetch size per pseudo channel in Pseudo Channel. MSB of RA is used to select halfof open 2 KB page.NOTE 4 SID, SID0, SID1 act as bank address bits in command execution. Specific AC timing parameters orvariations on selected timing parameters may be linked to SID.NOTE 5 RA[13:12] = 11 is invalid.NOTE 6 SID[1:0] = 11 is invalid.NOTE 7 The density code refers to the encoding of per-channel density in DEVICE_ID WDR (Table 132) bits[43:40].NOTE 8 ŠID[0]=1 is invalid in 4Hi configuration.</td></tr></table>

## 3.2.1 Bank Groups

The banks within a device are divided into 2 or 4 or 6 or 8 bank groups. The assignment of banks to bank groups is shown in Table 5.

Different timing parameters are specified depending on whether back-to-back accesses are within the same bank group or across bank groups as shown in Table 6.

Table 5 — Bank Group Assignments
<table><tr><td rowspan=1 colspan=1>Banks</td><td rowspan=1 colspan=1>16 BanksBA[3:0]</td><td rowspan=1 colspan=1>32 BanksSID, BA[3:0]</td><td rowspan=1 colspan=1>48 BanksSID[1:0]1, BA[3:0]</td><td rowspan=1 colspan=1>64 BanksSID[1:0], BA[3:0]</td></tr><tr><td rowspan=1 colspan=1>0 to 7</td><td rowspan=1 colspan=1>Group A</td><td rowspan=1 colspan=1>Group A</td><td rowspan=1 colspan=1>Group A</td><td rowspan=1 colspan=1>Group A</td></tr><tr><td rowspan=1 colspan=1>8 to 15</td><td rowspan=1 colspan=1>Group B</td><td rowspan=1 colspan=1>Group B</td><td rowspan=1 colspan=1>Group B</td><td rowspan=1 colspan=1>Group B</td></tr><tr><td rowspan=1 colspan=1>16 to 23</td><td rowspan=4 colspan=1>N/A</td><td rowspan=1 colspan=1>Group C</td><td rowspan=1 colspan=1>Group C</td><td rowspan=1 colspan=1>Group C</td></tr><tr><td rowspan=1 colspan=1>24 to 31</td><td rowspan=1 colspan=1>Group D</td><td rowspan=1 colspan=1>Group D</td><td rowspan=1 colspan=1>Group D</td></tr><tr><td rowspan=1 colspan=1>32 to 39</td><td rowspan=4 colspan=1>N/A</td><td rowspan=1 colspan=1>Group E</td><td rowspan=1 colspan=1>Group E</td></tr><tr><td rowspan=1 colspan=1>40 to 47</td><td rowspan=1 colspan=1>Group F</td><td rowspan=1 colspan=1>Group F</td></tr><tr><td rowspan=1 colspan=1>48 to 55</td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>N/A</td><td rowspan=1 colspan=1>Group G</td></tr><tr><td rowspan=1 colspan=1>56 to 63</td><td rowspan=1 colspan=1>Group H</td></tr><tr><td rowspan=1 colspan=5>NOTE 1  SID[1:0] = 11 is invalid.</td></tr></table>

Table 6 — Command Sequence Affected by Bank Groups
<table><tr><td rowspan=2 colspan=1>Command Sequence</td><td rowspan=1 colspan=2>Corresponding AC Timing Parameter</td><td rowspan=2 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Accesses ToDifferent Bank Groups</td><td rowspan=1 colspan=1>Accesses WithinSame Bank Group</td></tr><tr><td rowspan=1 colspan=1>ACTIVATE to ACTIVATE</td><td rowspan=1 colspan=1>tRRDS</td><td rowspan=1 colspan=1>tRRDL</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>WRITE to WRITE</td><td rowspan=1 colspan=1>tCCDS</td><td rowspan=1 colspan=1>tcCDL</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>READ to READ</td><td rowspan=1 colspan=1>tccDs or tCCDR</td><td rowspan=1 colspan=1>tcCDL</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Internal WRITE to READ</td><td rowspan=1 colspan=1>tWTRS</td><td rowspan=1 colspan=1>tWTRL</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>READ to PRECHARGE</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>tRTP</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=4>NOTE 1 Parameters tRTP applies only when READ and PRECHARGE go to the same bank.NOTE 2 Parameters tccDR replaces parameter tccDs when consecutive READs go to banks with different stackIDs (SID).</td></tr></table>

## 3.3 Simplified State Diagram

The state diagram provides a simplified illustration of the allowed state transitions and the related commands to control them. The following operations are either not shown or not fully shown in the diagram:

State transitions involving more than one bank;

• Interactions from the use of IEEE1500 instructions to load mode registers or execute test functions;

• the immediate transition from any state to reset state by asserting RESET\_n LOW or by loading the IEEE1500 instructions HBM\_RESET;

The ECS, ECS suppression (ECS flag in REFab/SRE), DRFM, and ECC Engine Test Mode operation;

• DCA and DCM;

• Loopback Test Mode;

• WDQS-to-CK Alignment Training

• Rx Offset Calibration Training

For a complete description of the device behavior, use the information provided in the state diagram along with the command truth tables and AC timing specifications.

## 3.3 Simplified State Diagram (cont’d)

![](images/c1a44f7630d9b3e05be9f2612c8afd4e2535100af3955e108501f853e62c4630.jpg)  
Figure 3 — Simplified State Diagram

<table><tr><td rowspan=1 colspan=1>Code</td><td rowspan=1 colspan=1>Command</td></tr><tr><td rowspan=1 colspan=1>ACT</td><td rowspan=1 colspan=1>Active</td></tr><tr><td rowspan=1 colspan=1>PREab</td><td rowspan=1 colspan=1>Precharge all</td></tr><tr><td rowspan=1 colspan=1>PREpb</td><td rowspan=1 colspan=1>Precharge</td></tr><tr><td rowspan=1 colspan=1>RD</td><td rowspan=1 colspan=1>Read</td></tr><tr><td rowspan=1 colspan=1>RDA</td><td rowspan=1 colspan=1>Read with Auto Precharge</td></tr><tr><td rowspan=1 colspan=1>WR</td><td rowspan=1 colspan=1>Write</td></tr><tr><td rowspan=1 colspan=1>WRA</td><td rowspan=1 colspan=1>Write with Auto Precharge</td></tr><tr><td rowspan=1 colspan=1>REFab</td><td rowspan=1 colspan=1>All bank refresh</td></tr><tr><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>Per bank refresh</td></tr><tr><td rowspan=1 colspan=1>RFMab</td><td rowspan=1 colspan=1>All bank refresh management</td></tr><tr><td rowspan=1 colspan=1>RFMpb</td><td rowspan=1 colspan=1>Per bank refresh management</td></tr><tr><td rowspan=1 colspan=1>PDE</td><td rowspan=1 colspan=1>Power down entry</td></tr><tr><td rowspan=1 colspan=1>PDX</td><td rowspan=1 colspan=1>Power down exit</td></tr><tr><td rowspan=1 colspan=1>SRE</td><td rowspan=1 colspan=1>Self refresh entry</td></tr><tr><td rowspan=1 colspan=1>SRX</td><td rowspan=1 colspan=1>Self refresh exit</td></tr><tr><td rowspan=1 colspan=1>MRS</td><td rowspan=1 colspan=1>More register set</td></tr></table>

<table><tr><td>Initialization 4</td></tr></table>

To power-up and initialize the HBM4 device into functional operation the sequence in clause 4.1 must be followed. At any time after the power-up initialization, the HBM4 device may be reset using the sequence in this section. A limited set of IEEE 1500 port instructions may be used within the initialization sequences, as described in Initialization Sequence with Stable Power clause.

The interactions between HBM4 functional reset and the IEEE 1500 port reset are as follows (also see IEEE Standard 1500 clause):

• Functional reset requires that the IEEE 1500 port also be reset.

• The IEEE 1500 port can be reset at any time without impacting normal operation.

The IEEE 1500 port may be brought out of reset and a limited set of instructions may be used after a minimum time after RESET\_n has been deasserted. See Initialization Sequence with Stable Power clause.

• If not needed, the IEEE 1500 port may be left in reset (WRST $\underline { { \mathbf { n } } } = \mathrm { L O W } )$ during normal operation.

## 4.1 HBM4 Power-up and Initialization Sequence

HBM4 device must be powered up and initialized in a predefined manner. The following sequence and timing must be satisfied for HBM4 power up and initialization sequence.

1. Apply power to the $\mathrm { \Delta V _ { D D C } , V _ { D D Q } , V _ { D D Q L } }$ and $\mathrm { \Delta V _ { P P } }$ supplies following the requirements listed below to prevent latch up from multiple power supplies.

a) V<sub>PP</sub> must ramp at the same time or earlier than V<sub>DDC</sub>

b) V<sub>PP</sub> is required to be greater than Vddc +200 mV after first supply reaches 300mV at time $\mathrm { { T } _ { a } }$ as illustrated in Figure 4.

c) $\mathrm { V _ { D D C } }$ must ramp at the same time or earlier than V<sub>DDQ</sub>

d) As $\mathrm { V _ { D D C } }$ and $\mathrm { V _ { D D Q } }$ levels are vendor specific, $\mathrm { V _ { D D C } }$ must be greater than $\mathrm { V _ { D D Q } + V S P }$ mV after the first supply reaches 300mV. VSP is Vendor Specific and depends on $\mathrm { V _ { D D C } }$ and $\mathrm { V _ { D D Q } }$ levels. See vendor datasheets for more details.

e) $\mathrm { V _ { D D Q } }$ must ramp at same time or earlier than $\mathrm { \Delta V _ { D D Q I } }$

f) $\mathrm { V _ { D D Q } }$ must be greater than $\mathrm { V _ { D D Q L } } { - 2 0 0 }$ mV after the first supply reaches 300mV

All supplies must be withing their normal operating range within t<sub>INIT0</sub> at time T<sub>b</sub>. During power supply ramp time tINT0, RESET\_n WRST\_n and all other input signals may be in an undefined state (driven LOW or HIGH, or Hi-Z).

## 4.1 HBM4 Power-up and Initialization Sequence (cont’d)

It is recommended to power up the supplies in a sequential power-up from highest voltage to lowest voltage. In the recommended example sequence, the power must be applied to each supply without slope reversal in the following sequence as shown in Figure 4.

a) Apply power to $\mathrm { V } _ { \mathrm { P P } }$ at time $\mathrm { T } _ { 0 } .$

b) Apply power to $\mathrm { \Delta V _ { D D C } }$ after $\mathrm { \Delta V _ { P P } }$ is within its defined normal operating range as shown at time $\mathrm { T _ { a l } }$

c) Apply power to $\mathrm { V _ { D D Q } }$ after $\mathrm { V _ { D D C } }$ is within its normal operating range as shown at time $\mathrm { T } _ { \mathfrak { a } 2 } .$

d) Apply power to $\mathrm { V _ { D D Q I } }$ after $\mathrm { V _ { D D Q } }$ is within its normal operating range as shown at time $\mathrm { T } _ { \mathfrak { a } 3 } .$

e) The power-up sequence is complete when $\mathrm { V _ { D D Q I } }$ is within its normal operating range as shown at ${ \mathrm { T } } _ { \mathsf { b } } .$

![](images/68a6fd2baebb622e8ddde1a56cafa294cd66900a65cc23e1c15db4e575790cd2.jpg)  
Figure 4 — Recommended Power-up and Controlled Power-off Sequence

2. RESET\_n and $\mathrm { W R S T \_ n }$ must be driven LOW (below $0 . 2 \times \mathrm { V } _ { \mathrm { D D Q } } )$ before or at the same time when t<sub>INIT0</sub> expires as shown in Figure 5 (time T<sub>b</sub>). All other input signals may be in an undefined state (driven LOW or HIGH, or Hi $- Z )$ at this point. RESET\_n must be maintained LOW for a minimum of t<sub>INIT1</sub> time with stable power. After $\mathrm { \Delta t { } _ { I N I T 6 } }$ time has elapsed, the HBM4 device drives RDQS\_t and RDQS\_c to LOW and HIGH static levels, respectively, and AERR, DERR and CATTRIP signals to LOW.

3. A time t<sub>INIT2</sub> before RESET\_n is pulled HIGH, CK\_t and CK\_c must be driven to static LOW and HIGH levels, respectively.

4. After RESET\_n is driven HIGH, R[3:0] must be driven to PDE state (HIGH, LOW, HIGH, LOW) and C[2:0] must be driven to CNOP state (HIGH, HIGH, HIGH) for a t time before CK clock is toggled. R[9:4] and C[7:3] are allowed to remain in an undefined state. The HBM4 device resets into the precharged power-down state. During $\mathrm { \ t n u T { 3 } } ,$ the HBM4 device will read and apply internal fuse configuration data and perform I/O driver impedance calibration. At the same time the WRST\_n signal may be optionally driven HIGH to enable a subset of the IEEE 1500 instructions (see IEEE Standard 1500 section). In that case, all other IEEE1500 inputs (WRCK, SelectWIR, ShiftWR, CaptureWR, UpdateWR, WSI) must be driven per IEEE1500 Port Input and Output Timings figure at time $\mathrm { \Delta t w m N I T { 2 } }$ before WRST\_n is pulled HIGH (see IEEE1500 Test Port AC Timing Parameters). CATTRIP data must stay LOW from the end of $\mathrm { \ t N I T { 6 } }$ to the end of $\mathrm { \ t r { I T 3 } }$ and valid data must start after t<sub>INIT3</sub>.

## 4.1 HBM4 Power-up and Initialization Sequence (cont’d)

5. While R[3:0] and C[2:0] remain driven to PDE state as defined in step 4, the CK clock shall be started and stable clocks shall be maintained for minimum of t time before driving R[3:0] HIGH. Since R[0] of R[3:0] is a synchronous signal, the corresponding setup time to clock (t<sub>IS</sub>) must be met. Also, RNOP and CNOP commands must be registered (with t<sub>IS</sub> / t<sub>IH</sub> satisfied). After R[3:0] are registered HIGH, a minimum t<sub>INIT5</sub> time must be satisfied before issuing a first MRS command. At or before the time that R[3:0] are driven HIGH, WDQS\_t and WDQS\_c must be driven to LOW and HIGH static levels, respectively. A stable CK clock shall be maintained except when a channel is in power-down or self refresh state. See Power-Down (PDE, PDX) and Self Refresh (SRE, SRX) clauses for conditions about stopping and re-starting the CK clock.

6. Issue all MRS commands to configure the HBM4 device appropriately for the application setting.

7. The HBM4 device is now ready for normal operation.

Table 7 — Initialization Timing Parameters
<table><tr><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Unit</td></tr><tr><td rowspan=1 colspan=1>tINITO</td><td rowspan=1 colspan=1>Power supply ramp time1</td><td rowspan=1 colspan=1>0.01</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>ms</td></tr><tr><td rowspan=1 colspan=1>tINIT1</td><td rowspan=1 colspan=1>RESET_n signal LOW time at power-up (after stable power)</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>μs</td></tr><tr><td rowspan=1 colspan=1>tINIT2</td><td rowspan=1 colspan=1>CK_c and CK_t must be driven to HIGH and LOW before RESET_ndeassertion</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=1 colspan=1>tINIT3</td><td rowspan=1 colspan=1>Precharged power-down state and WRST n LOWtime afterRESET n deassertion</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ms</td></tr><tr><td rowspan=1 colspan=1>tINIT4</td><td rowspan=1 colspan=1>CK clock stable time before R[3:0] HIGH</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td></tr><tr><td rowspan=1 colspan=1>tINIT5</td><td rowspan=1 colspan=1>Idle time before first MRS command</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=1 colspan=1>tINIT6</td><td rowspan=1 colspan=1>RDQS t, RDQS c drivenvalid and AERR, DERR and CATTRIPdriven LOW after RESET_n assertion</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=1 colspan=1>tpW_RESET</td><td rowspan=1 colspan=1>RESET_n signal LOW time with stable power</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>μs</td></tr><tr><td rowspan=1 colspan=1>tINIT7</td><td rowspan=1 colspan=1>R[3:0] and C[2:0] must be driven to PDE and CNOP before CKclock toggling</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td></tr><tr><td rowspan=1 colspan=1>VSP</td><td rowspan=1 colspan=1>Vendor Specific (VSP) voltage for VDDc and VDDQ during ramp(VDDc must be greater than VDDQ + VSP mV)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mV</td></tr></table>

## 4.1 HBM4 Power-up and Initialization Sequence (cont’d)

![](images/6af59a7a54a1de65fde0f0e2ad7800e4fc30c6d7e18d0c6e1a7221ab4f9d1578.jpg)  
NOTE 1 CATTRIP is valid after tINIT3

NOTE 2 Refer to recommended power-up and controlled power-off sequence figure for more details of Ta, divided by Ta1, Ta2, and Ta3.

Figure 5 — Power-up and Initialization

## 4.2 Initialization Sequence with Stable Power

Steps 1 and 2 must be satisfied to perform a functional reset when power is kept stable at the HBM4 DRAM. See Figure 6.

1. RESET\_n must be driven LOW anytime when a functional reset is needed. All other input signals may be in an undefined state (driven LOW or HIGH, or Hi-Z) at this point except WRST\_n and CATTRIP as shown in Figure 6. RESET\_n must be maintained LOW for a minimum of t<sub>PW\_RESET</sub>. R[3:0] must be driven to PDE state (HIGH, LOW, HIGH, LOW) and C[2:0] must be driven to CNOP state (HIGH, HIGH, HIGH) for a t time before CK clock is toggled. R[9:4] and C[7:3] are allowed to remain in an undefined state. Alternately, the IEEE1500 port HBM4\_RESET instruction may be used to perform a re-initialization, with RESET\_n continuing to be driven HIGH. Refer to HBM\_RESET instruction.

2. Follow steps 3 to 6 as described in clause HBM4 Power-up and Initialization Sequence. Note that the CATTRIP output is sticky and not cleared by a functional reset.

A time t<sub>INIT2</sub> before RESET\_n is pulled HIGH, CK\_t and CK\_c must be driven to static LOW and HIGH levels, respectively. See step 3 of the HBM4 Power-up and Initialization Sequence.

## 4.2 Initialization Sequence with Stable Power (cont’d)

![](images/f7859f139907b8085b0f2bcc479b645d950f095066d11087ebf196029cf99c8a.jpg)  
Figure 6 — HBM4 RESET and Initialization Sequence with Stable Power

## 4.3 Controlled Power-off Sequence

For a controlled power-off, the conditions in Table 8 must be met:

While powering off, all input levels must be between $\mathrm { V } _ { \mathrm { S S } }$ and $\operatorname { V } _ { \mathrm { D D Q } }$ or V<sub>DDQL</sub> during voltage ramp to avoid latch-up.

Table 8 — Power Supply Conditions
<table><tr><td rowspan=1 colspan=1>Between</td><td rowspan=1 colspan=1>Application Condition</td></tr><tr><td rowspan=3 colspan=1> $\mathrm { T } _ { \mathrm { X } }$ and $\mathrm { T } _ { \mathrm { Z } }$ </td><td rowspan=1 colspan=1> $\mathrm { \Delta V _ { P P } }$ must be greater than $\mathrm { V _ { D D C } , V _ { D D Q } }$ </td></tr><tr><td rowspan=1 colspan=1>VDDC must be greater than VDDQ + VSP mV</td></tr><tr><td rowspan=1 colspan=1> $\mathrm { V _ { D D Q } }$ must be greater than $\overline { { \mathrm { \Delta V _ { D D Q L } } } }$ - 200 mV</td></tr><tr><td rowspan=1 colspan=2>NOTE 1   $\mathrm { T _ { x } }$ is the point where any power supply drops below the minimum value specified.NOTE 2 Tz is the point where all power supplies are below 300 mV. After Tz, the HBM4 device is powered off.NOTE 3 VSP is Vendor Specific and is the voltage delta for VDDC and VDDQ during power off.</td></tr></table>

The recommended controlled power-off powers off the supplies sequentially from the lowest to highest to avoid latch-up as illustrated in the Recommended Power-up and Controlled Power-off Sequence example figure (Figure 4).

a) The recommended example controlled power-off sequence begins when V<sub>DDQL</sub> supply drops below the minimum operating voltage as shown at time $\mathrm { { T _ { x } } . }$

b) $\mathrm { V _ { D D Q } }$ ramp down can begin once $\mathrm { V _ { D D Q I } }$ drops below 300 mV as shown at time $\mathrm { T _ { y l } }$

c) $\mathrm { V _ { D D C } }$ ramp down can begin once $\mathrm { V _ { D D Q } }$ drops below 300 mV as shown at time $\mathrm { T } _ { \mathrm { y } 2 }$

d) $\mathrm { V } _ { \mathrm { P P } }$ ramp down can begin once V<sub>DDC</sub> drops below 300 mV as shown at time $\mathrm { T _ { y 3 } } .$

e) The power-off completes when all power supplies are below 300 mV and must be completed within tPOFF.

## 4.4 Initialization Sequence For Use Of IEEE 1500 Instruction Including Lane Repairs and Channel Disable

All IEEE 1500 port instructions are allowed after $\mathrm { \ t n u m } 3$ without completing the full initialization sequence. Figure 7 illustrates usage of the EXTEST and SOFT\_LANE\_REPAIR instructions and Figure 8 the usage of the CHANNEL\_DISABLE instruction within the initialization sequence. These sequence may be applied as part of the power-up or stable-power initialization sequence to check for and correct failed connections on the row and column command buses, which must be correctly driven to RNOP and CNOP as part of this initialization sequence. It may also be used to disable a channel before normal operation mode is entered. DWORD lane repairs are also allowed.

1. At time $\mathrm { T _ { a } , }$ RESET\_n and WRST\_n must be driven LOW.

2. After a minimum time $\mathrm { \bf t } _ { \mathrm { I N I T 1 } }$ (if during an initial power-up sequence) or after t<sub>PW\_RESET</sub> (if during a stable power initialization sequence) $\mathrm { R E S E T \_ n }$ shall be driven HIGH. t<sub>INIT2</sub> must also be met.

3. After $\mathrm { \ t N I T { 3 } } ,$ , WRST\_n is driven HIGH. IEEE 1500 port instructions may now be used. (Note that the WRST\_n low pulse width $\mathrm { { \ t w n s r L } }$ is met since t<sub>WRSTL</sub> is less than the t<sub>INIT1</sub> or t<sub>PW\_RESET</sub>). Refer to IEEE1500 Test Port AC Timing Parameters for timing requirements for operating the IEEE 1500 port, including t<sub>SWRST</sub>. At this point, a defective channel may be disabled; also, defective lane detection and soft lane repair may be executed. EXTEST operations may be applied to identify lanes needing repair. If soft lane repair is needed, SOFT\_LANE\_REPAIR and HARD\_LANE\_REPAIR operations can be applied after another RESET\_n toggle, which is required after EXTEST instruction operation. An IEEE 1500 port BYPASS instruction should be applied to return all HBM4 signals to their normal functional mode after SOFT\_LANE\_REPAIR operations. Alternately, WRST\_n may be driven LOW.

4. The initialization sequence may then continue per steps 4 to 6 of HBM4 Power-up and Initialization Sequence, as needed.

During the $\mathrm { \ t n u r { 3 } }$ period before WRST\_n is driven HIGH, the HBM4 device executes various internal configuration operations, including applying hard lane repairs based on previously fused data. Executing soft lane repair instructions after t<sub>INIT3</sub> overwrites any previously programmed hard lane repair data. It is suggested that the hard lane repair data is read from the HBM4 device and merged in any new lane repairs before applying the new soft lane repair operations. Any applicable IEEE 1500 port instructions timings must be met before continuing to time point $\mathrm { T } _ { \mathrm { h } } ,$ such as $\mathbf { t } _ { \mathrm { S L R E P } }$ if a SOFT\_LANE\_REPAIR instruction has been applied.

The EXTEST instructions are not required before applying the soft lane repair(s). Previously determined needed lane repairs may be applied as part of each initialization event.

A time t<sub>INIT2</sub> before RESET\_n is pulled HIGH, CK\_t and CK\_c must be driven to static LOW and HIGH levels, respectively. See step 3 of the HBM4 Power-up and Initialization Sequence.

R[3:0] must be driven PDE state and C[2:0] must be driven CNOP state for a t<sub>INIT7</sub> time.

## 4.4 Initialization Sequence For Use Of IEEE 1500 Instruction Including Lane Repairs and Channel Disable (cont’d)

![](images/7dc88a08fc1db37a6426ee3b8a32d64c02bf56cc26d714242f8a397be1e7f9b4.jpg)  
NOTE 1 After EXTEST operations, another RESET\_n toggle is required.  
NOTE 2 R[9:0] and C[7:0] mean logical pin name because those pin's physical location will be changed after soft or hard lane repair.

Figure 7 — Initialization Sequence with Lane Repair or Channel Disable

## 4.4 Initialization Sequence For Use Of IEEE 1500 Instruction Including Lane Repairs and Channel Disable (cont’d)

![](images/b61813c2147c42844c12665847b11725536240cd2d01a20d3a69e501208e8bb3.jpg)  
NOTE 1 A disabled channel will turn off all AWORD and DWORD input and output buffers including CK\_t/CK\_c and WDQS\_t/WDQS\_c inputs, thus allowing all external signals to float. The CK clock is allowed to be High-Z throughput this initialization sequence.

Figure 8 — Initialization Sequence with Channel Disable

The Mode Registers define the specific mode of operation for the HBM4 DRAM. Twenty 8-bit wide Mode Registers (MR0 to MR19) are defined as in Table 10 through Table 30. MR12 and MR17 are special mode registers and reserved for vendor specific features. Mode Registers are common to both pseudo channels (PC0 and PC1). Reprogramming the Mode Registers does not alter the contents of the memory array.

Mode Registers are programmed via the MODE REGISTER SET (MRS) command and retain the stored information until they are reprogrammed, chip reset, or until the device loses power. Mode Register can also be programmed via the IEEE1500 instruction MODE\_REGISTER\_DUMP\_SET; this instruction can also be used to retrieve the Mode Register content.

Mode Registers must be loaded when all banks are idle and the time t<sub>RDMRS</sub> from a preceding READ command has elapsed. The controller must wait the specified time such as t<sub>MOD</sub>, t<sub>MRD</sub>, t<sub>RDMRS</sub>, and t<sub>WRMRS</sub> (See Mode Register Set (MRS) Command clause) before initiating any subsequent operations. Violating either of these requirements will result in unspecified operation.

No default states are defined for Mode Registers except when otherwise noted. Users therefore must fully initialize all Mode Registers to the desired values upon power-up or after a subsequent chip reset.

When an entire Mode Register is marked as RFU (“Reserved for future use”), then it is considered as not supported by the HBM4 DRAM, and its content is Don’t Care. Reserved states should not be used, as unknown operation or incompatibility with future versions may result. RFU bits in these registers must be programmed to 0.

## 5 Mode Registers (cont’d)

Table 9 — HBM4 Mode Register Overview
<table><tr><td rowspan=1 colspan=2>Mode Register</td><td rowspan=2 colspan=1>OP7</td><td rowspan=2 colspan=1>OP6</td><td rowspan=2 colspan=1>OP5</td><td rowspan=2 colspan=1>OP4</td><td rowspan=2 colspan=1>OP3</td><td rowspan=2 colspan=1>OP2</td><td rowspan=2 colspan=1>OP1</td><td rowspan=2 colspan=1>OP0</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>MA[4:0]</td></tr><tr><td rowspan=1 colspan=1>MR0(Table 10)</td><td rowspan=1 colspan=1>00000</td><td rowspan=1 colspan=1>TestMode(TM)</td><td rowspan=1 colspan=1>CA Parity(CAPAR)</td><td rowspan=1 colspan=1>WriteParity(WPAR)</td><td rowspan=1 colspan=1>ReadParity(RPAR)</td><td rowspan=1 colspan=1>DRFM</td><td rowspan=1 colspan=1>TCSR</td><td rowspan=1 colspan=1>Write DBI(WDBI)</td><td rowspan=1 colspan=1>Read DBI(RDBI)</td></tr><tr><td rowspan=1 colspan=1>MR1(Table 11)</td><td rowspan=1 colspan=1>00001</td><td rowspan=1 colspan=3>Parity Latency (PL)</td><td rowspan=1 colspan=5>Write Latency (WL)</td></tr><tr><td rowspan=1 colspan=1>MR2(Table 12)</td><td rowspan=1 colspan=1>00010</td><td rowspan=1 colspan=8>Read Latency (RL)</td></tr><tr><td rowspan=1 colspan=1>MR3(Table 13)</td><td rowspan=1 colspan=1>00011</td><td rowspan=1 colspan=8>Write Recovery for Auto Pre-charge (WR)</td></tr><tr><td rowspan=1 colspan=1>MR4(Table 14)</td><td rowspan=1 colspan=1>00100</td><td rowspan=1 colspan=8>Activate to Precharge (RAS)</td></tr><tr><td rowspan=1 colspan=1>MR5(Table 15)</td><td rowspan=1 colspan=1>00101</td><td rowspan=1 colspan=4>RFU</td><td rowspan=1 colspan=4>Read to Auto Precharge (RTP)</td></tr><tr><td rowspan=1 colspan=1>MR6(Table 16)</td><td rowspan=1 colspan=1>00110</td><td rowspan=1 colspan=1>DCM Flip</td><td rowspan=1 colspan=1>DCM(Duty CycleMonitor)</td><td rowspan=1 colspan=3>Pullup Driver Strength</td><td rowspan=1 colspan=3>Pulldown Driver Strength</td></tr><tr><td rowspan=1 colspan=1>MR71(Table 17)</td><td rowspan=1 colspan=1>00111</td><td rowspan=1 colspan=1>CATTRIP</td><td rowspan=1 colspan=1>Program-mableRDQSPostamble(tRPST)</td><td rowspan=1 colspan=3>DWORD MISR Control</td><td rowspan=1 colspan=1>RFU</td><td rowspan=1 colspan=1>DWORDRead MuxControl</td><td rowspan=1 colspan=1>DWORDLoopback</td></tr><tr><td rowspan=1 colspan=1>MR81(Table 19)</td><td rowspan=1 colspan=1>01000</td><td rowspan=1 colspan=2>DRFM Bounded RefreshConfiguration (BRC)</td><td rowspan=1 colspan=2>RFM Levels(RFML)</td><td rowspan=1 colspan=1>WDQS-to-CKTraining(WDQS2CK)</td><td rowspan=1 colspan=1>ECS error logauto reset(ECSLOG)</td><td rowspan=1 colspan=1>RxCalibrationOffset</td><td rowspan=1 colspan=1>DA PortLockout</td></tr><tr><td rowspan=1 colspan=1>MR9(Table 20)</td><td rowspan=1 colspan=1>01001</td><td rowspan=1 colspan=1>ECS errorType andAddressReset(ECSRES)</td><td rowspan=1 colspan=1>ECS Multi-bit ErrorCorection(ECSCEM)</td><td rowspan=1 colspan=1>Auto ECSduring SelfRefresh(ECSSRF)</td><td rowspan=1 colspan=1>Auto ECSvia REFab(ECSREF)</td><td rowspan=1 colspan=1>ErrorVectorPattern(ECCVEC)</td><td rowspan=1 colspan=1>ErrorVectorInputMode(ECCTM)</td><td rowspan=1 colspan=1>SeverityReporting(SEVR)</td><td rowspan=1 colspan=1>Meta Data(MD)</td></tr><tr><td rowspan=1 colspan=1>MR101(Table 21)</td><td rowspan=1 colspan=1>01010</td><td rowspan=1 colspan=4>DCA code for RDQS1 (PC1)</td><td rowspan=1 colspan=4>DCA code for RDQS0 (PC0)</td></tr><tr><td rowspan=1 colspan=1>MR11(Table 22)</td><td rowspan=1 colspan=1>01011</td><td rowspan=1 colspan=4>DCA code for WDQS1 (PC1)</td><td rowspan=1 colspan=4>DCA code for WDQS0 (PC0)</td></tr><tr><td rowspan=1 colspan=1>MR12(Table 23)</td><td rowspan=1 colspan=1>01100</td><td rowspan=1 colspan=8>Reserved for Vendor Specific Features</td></tr><tr><td rowspan=1 colspan=1>MR13(Table 24)</td><td rowspan=1 colspan=1>01101</td><td rowspan=1 colspan=1>RFU</td><td rowspan=1 colspan=6>Reference Voltage for AWORD inputs (VREFCA)</td><td rowspan=1 colspan=1>RFU</td></tr><tr><td rowspan=1 colspan=1>MR143(Table 25)</td><td rowspan=1 colspan=1>01110</td><td rowspan=1 colspan=1>RFU</td><td rowspan=1 colspan=6>(PC0) Reference Voltage for DWORD inputs (VREFD)</td><td rowspan=1 colspan=1>RFU</td></tr><tr><td rowspan=1 colspan=1>MR15(Table 26)</td><td rowspan=1 colspan=1>01111</td><td rowspan=1 colspan=4>RFU</td><td rowspan=1 colspan=2>DFE Code (PC1)</td><td rowspan=1 colspan=2>DFE Code (PCO)</td></tr><tr><td rowspan=1 colspan=1>MR162(Table 27)</td><td rowspan=1 colspan=1>10000</td><td rowspan=1 colspan=8>Reserved for Decision Feedback Equalizer (DFE)</td></tr><tr><td rowspan=1 colspan=1>MR172(Table 28)</td><td rowspan=1 colspan=1>10001</td><td rowspan=1 colspan=8>Reserved for Vendor Specific Features</td></tr><tr><td rowspan=1 colspan=1>MR182, 3(Table 29)</td><td rowspan=1 colspan=1>10010</td><td rowspan=1 colspan=1>RFU</td><td rowspan=1 colspan=6>PC1 Reference Voltage for DWORD inputs (VREFD)</td><td rowspan=1 colspan=1>RFU</td></tr><tr><td rowspan=1 colspan=1>MR192(Table 30)</td><td rowspan=1 colspan=1>10011</td><td rowspan=1 colspan=8>RFU</td></tr><tr><td rowspan=1 colspan=10>NOTE 1 Programmable RDQS (MR7 OP6), RxOffC (MR8 OP1), and RDQS DCA (MR10) are vendor optional features.NOTE 2MR16 to MR19 are vendor optional registers.NOTE 3Support is indicated by the PER_PC_VREFD bit field in the DEVICE_ID WDR (see Table 132 for details). If PER_PC_VREFD is 1,then MR14 is utilized for PC0 and MR18 is utilized for PC1. Otherwise, MR14 is utilized for both PC0 and PC1 (see Table 25 andTable 29 for details).</td></tr></table>

Table 10 — Mode Register 0 (MR0)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Test Mode (TM)</td><td rowspan=1 colspan=1>OP[7]</td><td rowspan=1 colspan=1>0 – Normal Operation (Default)1 – Test Mode (Vendor specific): only to be used by theDRAM manufacturer. No functional operation isspecified with test mode enabled.</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Command Address Parity(CAPAR)</td><td rowspan=1 colspan=1>OP[6]</td><td rowspan=1 colspan=1>0 – Disabled (Default)1 – Enabled</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>Write Parity (WPAR)</td><td rowspan=1 colspan=1>OP[5]</td><td rowspan=1 colspan=1>0 – Disabled1 – Enabled</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>Read Parity (RPAR)</td><td rowspan=1 colspan=1>OP[4]</td><td rowspan=1 colspan=1>0 – Disabled1 – Enabled</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>DRFM</td><td rowspan=1 colspan=1>OP[3]</td><td rowspan=1 colspan=1>0 – Disabled (Default)1 – Enabled</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Temperature CompensatedSelf Refresh (TCSR)</td><td rowspan=1 colspan=1>OP[2]</td><td rowspan=1 colspan=1>0 – Disabled1 – Enabled (Default)</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Write DBI (WDBI)</td><td rowspan=1 colspan=1>OP[1]</td><td rowspan=1 colspan=1>0 – Disabled1 – Enabled</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>Read DBI (RDBI)</td><td rowspan=1 colspan=1>OP[0]</td><td rowspan=1 colspan=1>0 – Disabled1 – Enabled</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=4>NOTE 1Refer to the Command/Address Parity clause for details regarding CA Parity.NOTE 2 Refer to the Data Parity clause for details regarding Write Parity and Read Parity.NOTE 3 Refer to the Data Bus Inversion (DBIac) clause for details regarding WDBI and RDBI.</td></tr></table>

Table 11 — Mode Register 1 (MR1)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Parity Latency (PL)</td><td rowspan=1 colspan=1>OP[7:5]</td><td rowspan=1 colspan=1>000 – 0 nCK001 - 1 nCK010 − 2 nCK011 -3 nCK100-4nCKAll others – Reserved</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=1>Write Latency (WL)</td><td rowspan=1 colspan=1>OP[4:0]</td><td rowspan=1 colspan=1>00100-4 nCK00101 -5 nCK00110-6 nCK10010 –18 nCK10011 - 19 nCKAll Others - Reserved</td><td rowspan=1 colspan=1>1,3</td></tr><tr><td rowspan=1 colspan=4>NOTE 1 All PL and WL values are optional, however the supported min-to-max ranges must be contiguous.NOTE 2Refer to the Data Parity clause for details regarding Parity Latency (PL) definition and use with write and readoperations.NOTE 3 Refer to the WRITE command clause for details regarding the Write Latency (WL) definitions and use.</td></tr></table>

## Mode Registers (cont’d)

Table 12 — Mode Register 2 (MR2)
<table><tr><td>Field</td><td>Bits</td><td>Description</td><td>Notes</td></tr><tr><td rowspan="3">Read Latency (RL)</td><td rowspan="3">OP[7:0]</td><td>00010001 - 17 nCK 00010010 - 18 nCK</td><td>1,2</td></tr><tr><td>00010011 - 19 nCK</td><td></td></tr><tr><td>01011001 -89 nCK 01011010 -90 nCK</td><td></td></tr><tr><td colspan="4">NOTE 1 All RL values are optional, however the supported min-to-max ranges must be contiguous. NOTE 2 Refer to the READ command clause for details regarding the Read Latency (RL) definitions and use.</td></tr></table>

Table 13 — Mode Register 3 (MR3)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Write Recovery to AutoPrecharge (WR)</td><td rowspan=1 colspan=1>OP[7:0]</td><td rowspan=1 colspan=1>00000100-4 nCKbal00000101 - 5 nCK00000110 -6 nCK00111110 –62 nCK00111111-63 nCKAll others – Reserved</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=4>NOTE 1 All WR values are optional, however the supported min-to-max range must be contiguous.NOTE 2WR must be programmed with a value greater than or equal to RU{twR/tck}, where RU stands for round up,twR is the analog value from the vendor datasheet and tck is the operating clock cycle time. If an HBM4 DRAMdoes not support the mode register definition of twR in clock cycles, the WR mode register settings will be ignored.</td></tr></table>

Table 14 — Mode Register 4 (MR4)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Activate to Precharge(RAS)</td><td rowspan=1 colspan=1>OP[7:0]</td><td rowspan=1 colspan=1>00000100-4 nCK00000101 -5 nCK00000110 - 6 nCK00111110– 62 nCK00111111-63 nCKAll others – Reserved</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=4>NOTE 1 All RAS values are optional, however the supported min-to-max range must be contiguous.NOTE 2RAS must be programmed with a value greater than or equal to RU{tRAs/tck}, where RU stands for round up,tRAs is the analog value from the vendor datasheet and tck is the operating clock cycle time. If an HBM4 DRAMdoes not support the mode register definition of tRAs in clock cycles, the RAS mode register settings will beignored.</td></tr></table>

Table 15 — Mode Register 5 (MR5)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>RFU</td><td rowspan=1 colspan=1>OP[7:4]</td><td rowspan=1 colspan=1>0000</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Read to Auto Pre-charge(RTP)</td><td rowspan=1 colspan=1>OP[3:0]</td><td rowspan=1 colspan=1>0010 -2 nCK0011-3nCK0100-4nCK1110 – 14 nCK1111 – 15 nCKAll others – Reserved</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=4>NOTE 1 All RTP values are optional, however the supported min-to-max range must be contiguous.NOTE 2RTP must be programmed with a value greater than or equal to RU{tRTP/tCK}, where RU stands for round up,tRTP is the analog value from the vendor datasheet and tCK is the operating clock cycle time. If an HBM4 DRAMdoes not support the mode register definition of tRTP in clock cycles, the RTP mode register settings will beignored.</td></tr></table>

Table 16 — Mode Register 6 (MR6)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Duty Cycle Monitor(DCM) Flip</td><td rowspan=1 colspan=1>OP[7]</td><td rowspan=1 colspan=1>0 – Disabled (Default)1 – Enabled</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Duty Cycle Monitor(DCM)</td><td rowspan=1 colspan=1>OP[6]</td><td rowspan=1 colspan=1>0 – Disabled (Default)1 – Enabled</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Pullup Driver Strength</td><td rowspan=1 colspan=1>OP[5:3]</td><td rowspan=1 colspan=1>000 – 25 Ohm001 -20 Ohm010 – 16.7 Ohm (Default)011 -14.3 OhmAll others – Reserved</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>Pulldown Driver Strength</td><td rowspan=1 colspan=1>OP[2:0]</td><td rowspan=1 colspan=1>000 -25 Ohm001-20 Ohm010 – 16.7 Ohm (Default)011-14.3 OhmAll others – Reserved</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=4>NOTE 1 Refer to the Transmit Driver Resistance (Table 95) table for the details.</td></tr></table>

## Mode Registers (cont’d)

Table 17 — Mode Register 7 (MR7)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>CATTRIP</td><td rowspan=1 colspan=1>OP[7]</td><td rowspan=1 colspan=1>0 – CATTRIP pin drives a LOW or HIGH depending onCATTRIP sensor output (Default)1 – CATTRIP pin drives a static HIGH</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>Programmable RDQSpostamble (tRPST)</td><td rowspan=1 colspan=1>OP[6]</td><td rowspan=1 colspan=1>0 – 2 tWDQS (Default)1 - 4 tWDQS</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>DWORD MISR Control</td><td rowspan=1 colspan=1>OP[5:3]</td><td rowspan=1 colspan=1>The bits are only evaluated if DWORD Loop-back isenabled in OP0000 – Preset: the DWORD MISR is preset as described inthe HBM4 Loopback Test Modes clause, and allDWORD LFSR COMPARE STICKY bits are resetto 0.001 – LFSR mode (READ direction)010 – Register mode (WRITE and READ directions):DWORD writes are captured directly into the MISRwithout compression. The MISR will contain the mostrecent write data.011 – MISR mode (WRITE direction)100 – LFSR Compare mode (WRITE direction)All others - Reserved</td><td rowspan=1 colspan=1>3,4</td></tr><tr><td rowspan=1 colspan=1>RFU</td><td rowspan=1 colspan=1>OP[2]</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>DWORD Read MuxControl</td><td rowspan=1 colspan=1>OP[1]</td><td rowspan=1 colspan=1>The bit is only evaluated with READ commands and ifDWORD Loopback is enabled in OP00 – Return data from DWORD MISR (see OP[5:3])1 – Return LFSR COMPARE STICKY bits (OP[5:3] isignored)</td><td rowspan=1 colspan=1>3,4</td></tr><tr><td rowspan=1 colspan=1>DWORD Loopback</td><td rowspan=1 colspan=1>OP[0]</td><td rowspan=1 colspan=1>0 – Disabled (Default)1 – Enabled: all Writes and Reads will be to/from the MISR.Notes:a) does not require any row activationb) column addresses associated with WRITE and READcommands are ignored</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=4>NOTE 1 The CATTRIP pin can be asserted to “HIGH&quot; from any of the channels [31:0] MR7 OP7 bit (logic OR).NOTE 2Programmable RDQS postamble is an optional feature. A HBM4 device not supporting this feature OP[6] must setto 0 by default.NOTE 3 See Test Method for DWORD Write MISR Mode clause for DWORD MISR mode features and use.NOTE4Refer to Table 18 for details on DWORD MISR operation with WRITE and READ commands.</td></tr></table>

Table 18 — DWORD MISR Read and Write Operations in Loopback Test Mode (MR7 OP0=1)
<table><tr><td rowspan=2 colspan=1>MR7OP[1]</td><td rowspan=2 colspan=1>MR7OP[5:3]</td><td rowspan=1 colspan=2>DWORD MISR Operation1</td><td rowspan=2 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>WRITE</td><td rowspan=1 colspan=1>READ</td></tr><tr><td rowspan=5 colspan=1>0</td><td rowspan=1 colspan=1>000(Preset)</td><td rowspan=1 colspan=1>Write data are ignored</td><td rowspan=1 colspan=1>Read the preset value(clock-like pattern)</td><td rowspan=1 colspan=1>Neither writes nor reads alter theMISR content</td></tr><tr><td rowspan=1 colspan=1>001(LFSR)</td><td rowspan=1 colspan=1>Write data are ignored</td><td rowspan=1 colspan=1>Generate read data fromLFSR</td><td rowspan=1 colspan=1>Writes do not alter the MISRcontent</td></tr><tr><td rowspan=1 colspan=1>010(Register)</td><td rowspan=1 colspan=1>MISR stores the secondhalf (UI 4 to 7) or alldata (UI 0 to 7) of themost recent Write fromregister mode, with only(UI 4 to 7) readable viaWDR(see note 2)</td><td rowspan=3 colspan=1>Read the MISR content(UI 0 to 3 and repeatedfor UI 4 to 7, or all data(UI 0 to 7) of the mostrecent Write (see note 2))_</td><td rowspan=3 colspan=1>Reads do not alter the MISRcontent</td></tr><tr><td rowspan=1 colspan=1>011(MISR)</td><td rowspan=1 colspan=1>Write data areaccumulated in the MISR</td></tr><tr><td rowspan=1 colspan=1>100(LFSRCompare)</td><td rowspan=1 colspan=1>Write data are comparedagainst data generated bythe LFSR</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>XXX</td><td rowspan=1 colspan=1>Write data are ignored</td><td rowspan=1 colspan=1>Read sticky error bits</td><td rowspan=1 colspan=1>Neither writes nor reads alter theMISR content</td></tr><tr><td rowspan=1 colspan=5>NOTE 1 See Loopback Test Modes for DWORD MISR and LFSR features and use.NOTE 2 Depending on implementation, the MISR either stores the second half (UI 4 to 7) or all data (UI 0 to 7) to the mostrecent Write, and subsequent Reads return either the second half (UI 4 to 7) or all data (UI 0 to 7) to that mostrecent Write. If a Read shall send identical data regardless of the actual implementation, users should send thesame write data on UI 0 to 3 and UI 4 to 7 of the most recent write.</td></tr></table>

## Mode Registers (cont’d)

Table 19 — Mode Register 8 (MR8)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>DRFM BoundedRefreshConfiguration (BRC)</td><td rowspan=1 colspan=1>OP[7:6]</td><td rowspan=1 colspan=1>00 − Always ±1, Ratio ±2 (tDRFM = 4 × tRRF)01 − Always ±1, ±2, Ratio ±3 (tDRFM = 6 × tRRF)10 − Always ±1, ±2, ±3, Ratio ±4 (tDRFM = 8 × tRRF)11-RFU</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>RFM Levels(RFML)</td><td rowspan=1 colspan=1>OP[5:4]</td><td rowspan=1 colspan=1>00 – Default Level (RFM may be required or not)01 – Level A (RFM is required)10 – Level B (RFM is required)11 – Level C (RFM is required)</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>WDQS-to-CKTraining(WDQS2CK)</td><td rowspan=1 colspan=1>OP[3]</td><td rowspan=1 colspan=1>0 – Disabled (Default)1 - Enabled</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>ECS error log autoreset (ECSLOG)</td><td rowspan=1 colspan=1>OP[2]</td><td rowspan=1 colspan=1>0 – Disabled (Default)1 – Enabled</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Rx Offset CalibrationStart/Stop</td><td rowspan=1 colspan=1>OP[1]</td><td rowspan=1 colspan=1>0 – Stop (Default)1 - Start</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>DA Port Lockout</td><td rowspan=1 colspan=1>OP[0]</td><td rowspan=1 colspan=1>0 – Access to DA port is enabled (Default)1 – Access to DA port is locked</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=4>NOTE 1 01 and 10 of BRC Configurations are optional features whereas00 is required. Supportability of this optionalfeature should be consulted by vendor datasheets and Table 132 (DEVICE_ID WDR)NOTE 2 The support of Adaptive Refresh Management (ARFM) is optional for the DRAM vendor. HBM4 DRAMs notsupporting (ARFM) will define these bits as RFU. RAAIMT, RAAMMT and RAADEC values for default RFMlevel and RFM levels A to C are set by DRAM vendor and can be read via the IEEE1500 DEVICE ID WDR.NOTE 3 Refer to the WDQS-to-CK Alignment Trainingclause for details.NOTE 4 Rx Offset Calibration is also optional feature and must be set to 0 if it is unavailable. See Table 132 (DEVICE_IDWDR) for details.NOTE 5 DA Port Lockout bit is defined for channels 0 and 4 only. The bit is RFU for all other channels. Once enabled, thebit can only be cleared by powering off the device. The IEEE1500 MODE_REGISTER_DUMP_SET instructioncannot be used to set or clear the bit, but allows reading the bit.</td></tr></table>

Table 20 — Mode Register 9 (MR9)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>ECS Error Type andAddress Reset (ECSRES)</td><td rowspan=1 colspan=1>OP[7]</td><td rowspan=1 colspan=1>0 – Maintain the ECS error type and address log (Default)1 – Reset the ECS error type and address log (self-clearing)</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>ECS multi-bit errorcorrection (ECSCEM)</td><td rowspan=1 colspan=1>OP[6]</td><td rowspan=1 colspan=1>0 – Correction of multi-bit errors during ECS cycles isdisabled1 – Correction of multi-bit errors during ECS cycles isenabled</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Auto ECS during SelfRefresh (ECSSRF)</td><td rowspan=1 colspan=1>OP[5]</td><td rowspan=1 colspan=1>0 – Auto ECS during self refresh mode is disabled (Default)1 – Auto ECS during self refresh mode is Enabled</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>Auto ECS via REFab(ECSREF)</td><td rowspan=1 colspan=1>OP[4]</td><td rowspan=1 colspan=1>0 – Auto ECS via REFab command is disabled (Default)1 – Auto ECS via REFab command is enabled</td><td rowspan=1 colspan=1>2,3</td></tr><tr><td rowspan=1 colspan=1>Error Vector Pattern(ECCVEC)</td><td rowspan=1 colspan=1>OP[3]</td><td rowspan=1 colspan=1>The bit is only evaluated when ECC Vector Input Mode isenabled in OP20 – Codeword 0 (CW0): Data 1’ means error bit and data‘0’ means non-error bit1 – Codeword 1 (CW1): Data ‘0’ means error bit and data1’ means non-error bit  1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Error Vector Input Mode(ECCTM)</td><td rowspan=1 colspan=1>OP[2]</td><td rowspan=1 colspan=1>0 – ECC Engine Test Mode is disabled (default)1 – ECC Engine Test Mode is enabled</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Severity Reporting(SEVR)</td><td rowspan=1 colspan=1>OP[1]</td><td rowspan=1 colspan=1>0 – Error severity reporting is disabled and the SEV signalsare High-Z1 – Error severity reporting is enabled. The SEV signalsdrive error severity information during Reads and other-wise are High-Z.</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>Meta Data (MD)</td><td rowspan=1 colspan=1>OP[0]</td><td rowspan=1 colspan=1>0– ECC signals are disabled. Read and write operations donot include meta data1 – ECC signals are enabled. Read and write operationsinclude meta data transmitted via ECC pins</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=4>NOTE 1 The bit is self-clearing meaning that it automatically returns back to 0 after the reset function has been issued.NOTE 2For ECS operation either ECSSRF or ECSREF (or both) must be enabled.NOTE3When ECS during REFab is enabled, the host must issue REFab commands at an average rate of tEcsint for theDRAM to complete the automatic scrub.NOTE 4 Input data on SEV signals during write operations will be ignored regardless of the SEVR setting.</td></tr></table>

## Mode Registers (cont’d)

Table 21 — Mode Register 10 (MR10)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=2 colspan=1>DCA code for RDQS1(PC1)</td><td rowspan=1 colspan=1>OP[7:4]</td><td rowspan=2 colspan=1>0000 – 0 steps (Default; no correction)0001 --1 step0010 – -2 steps0110 – -6 steps0111 --7 steps1000 – Reserved1001 - +1 step1010 – +2 steps1110 – +6 steps1111 − +7 steps</td><td rowspan=2 colspan=1>1, 2,3,4</td></tr><tr><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>DCA code for RDQS0(PC0)</td><td rowspan=1 colspan=1>OP[3:0]</td><td rowspan=1 colspan=1>0000 – 0 steps (Default; no correction)lobal0001 --1 step0010 – -2 steps0110 – -6 steps0111 - -7 steps1000 – Reserved1001 - +1 step1010 – +2 steps1110 – +6 steps1111 − +7 steps</td><td rowspan=1 colspan=1>1, 2, 3,4</td></tr><tr><td rowspan=1 colspan=4>NOTE10001 to 0111 of bit sets will decrease the internal WDQS duty cycleNOTE 2 1001 to 1111 of bit sets will increase the internal WDQS duty cycle.NOTE 3The step size (in ps) is vendor specific and may be non-linear.NOTE 4 DCA Code for RDQS is optional features configured by 178th bit of DEVICE ID. See Table 132.</td></tr></table>

Table 22 — Mode Register 11 (MR11)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>DCA code for WDQS1(PC1)</td><td rowspan=1 colspan=1>OP[7:4]</td><td rowspan=1 colspan=1>0000 – 0 steps (Default; no correction)0001 - -1 step0010 – -2 steps0110 – -6 steps0111 - -7 steps1000 – Reserved1001 - +1 step1010 – +2 steps1110 – +6 steps1111 - +7 steps</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=1>DCA code for WDQS0(PC0)</td><td rowspan=1 colspan=1>OP[3:0]</td><td rowspan=1 colspan=1>0000 – 0 steps (Default; no correction)lobal0001 - -1 step0010 – -2 steps0110 – -6 steps0111 – -7 steps1000 – Reserved1001 – +1 step1010 – +2 steps1110 – +6 steps1111 - +7 steps</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=4>NOTE 1Values of 0001 to 0111 decrease the internal WDQS duty cycle, and values of 1001 to 1111 increase the internalWDQS duty cycle.NOTE 2The step size (in ps) is vendor specific and may be non-linear.</td></tr></table>

Table 23 — Mode Register 12 (MR12)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Reserved for VendorSpecific Features</td><td rowspan=1 colspan=1>OP[7:0]</td><td rowspan=1 colspan=1>Vendor Specific</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=4>NOTE 1 MR12 is reserved for vendor specific features. Refer to the vendor&#x27;s datasheet for details.</td></tr></table>

## Mode Registers (cont’d)

Table 24 — Mode Register 13 (MR13)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>RFU</td><td rowspan=1 colspan=1>OP[7]</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Reference voltage forAWORD inputs(VREFCA)</td><td rowspan=1 colspan=1>OP[6:1]</td><td rowspan=1 colspan=1> $0 0 0 0 0 0 - 0 . 1 8 \mathrm { ~ x ~ V ~ } _ { \mathrm { D D Q L } }$ 000001 – 0.19 x VDDQL $0 1 1 1 1 1 - 0 . 4 9 \times \mathrm { V _ { D D Q L } }$ 100000 – 0.50 x VDDQL (Default)100001 – 0.51 x VDDQL $1 1 1 1 1 0 - 0 . 8 0 \mathrm { x V _ { D D Q L } }$  $1 1 1 1 1 1 - 0 . 8 1 \mathrm { \ x V _ { D D Q L } }$ </td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>RFU</td><td rowspan=1 colspan=1>OP[0]</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=4>NOTE 1Refer to the AWORD Signaling clause for the AWORD input receiver voltage level specification.</td></tr></table>

Table 25 — Mode Register 14 (MR14)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>RFU</td><td rowspan=1 colspan=1>OP[7]</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Reference voltage for(PC0) DWORD inputs(VREFD)</td><td rowspan=1 colspan=1>OP[6:1]</td><td rowspan=1 colspan=1>000000 – 0.18 x VDDQL000001 – 0.19 x VDDQL $0 1 1 1 1 1 - 0 . 4 9 \times \mathrm { V _ { D D Q L } }$ 100000 – 0.50 x VDDQL (Default)100001 -0.51 x VDDQL111110 – 0.80 x VDDQL111111 – 0.81 x VDDQL</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>RFU</td><td rowspan=1 colspan=1>OP[0]</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=4>NOTE 1 Refer to the DQ Rx Voltage and Timings clause for the DWORD input receiver voltage level specification.NOTE 2Per Pseudo Channel VREFD (PER_PC_VREFD) is an optional feature specified in bit 172 of DEVICE_ID WDR.See Table 132 (DEVICE ID) for details. If PER PC VREFD is 1, MR14 is utilized for PC0 and MR18 is utilizedfor PC1, otherwise MR14 is utilized for both PC0 and PC1.</td></tr></table>

Table 26 — Mode Register 15 (MR15)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>RFU</td><td rowspan=1 colspan=1>OP[7:4]</td><td rowspan=1 colspan=1>0000</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>DFE Code (PC1)</td><td rowspan=1 colspan=1>OP[3:2]</td><td rowspan=1 colspan=1>00 – Disable (Default)01 − Step + 110 − Step + 211 − Step + 3</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>DFE Code (PCO)</td><td rowspan=1 colspan=1>OP[1:0]</td><td rowspan=1 colspan=1>00 – Disable (Default)01 − Step + 110 − Step + 211 − Step + 3</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=4>NOTE 1 Size of each Decision Feedback Equalizer (DFE) steps are vendor specific. Refer to vendor datasheets.</td></tr></table>

Table 27 — Mode Register 16 (MR16)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Reserved for DFE</td><td rowspan=1 colspan=1>OP[7:0]</td><td rowspan=1 colspan=1>TBD</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=4>NOTE 1 MR16 is an optional register. Users shall refer to the vendor datasheet and DEVICE_ID WDR 179th bit.</td></tr></table>

Table 28 — Mode Register 17 (MR17)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Vendor Specific</td><td rowspan=1 colspan=1>OP[7:0]</td><td rowspan=1 colspan=1>Vendor Specific</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=4>NOTE 1 MR17 is reserved for vendor specific features. Refer to the vendor&#x27;s datasheet for details.NOTE 2 MR17 is an optional register. Users shall refer to the vendor datasheet and DEVICE ID WDR 179th bit.</td></tr></table>

Table 29 — Mode Register 18 (MR18)
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>RFU</td><td rowspan=1 colspan=1>OP[7]</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Pseudo Channel 1reference voltage forDWORD inputs(VREFD)</td><td rowspan=1 colspan=1>OP[6:1]</td><td rowspan=1 colspan=1>000000 – 0.18 x VDDQL000001 – 0.19 x VDDQL011111 – 0.49 x VDDQL100000 – 0.50 x VDDQL (Default)100001 – 0.51 x VDDQL111110 – 0.80 x VDDQL111111 – 0.81 x VDDQL</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>RFU</td><td rowspan=1 colspan=1>OP[0]</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=4>NOTE 1 Refer to the DQ Rx Voltage and Timings clause for the DWORD input receiver voltage level specification.NOTE 2 Per Pseudo Channel VREFD (PER_PC_VREFD) is an optional feature specified in bit 172 of DEVICE_ID WDR.See Table 132(DEVICE_ID) for details. If PER_PC_VREFD is 1, MR14 is utilized for PC0 and MR18 is utilizedfor PC1, otherwise MR14 is utilized for both PC0 and PC1.</td></tr></table>

## Mode Registers (cont’d)

Table 30 — Mode Register 19 (MR19)
<table><tr><td>Field</td><td>Bits</td><td>Description</td><td>Notes</td></tr><tr><td>RFU</td><td>OP[7:0]</td><td>00000000</td><td></td></tr><tr><td>NOTE 1 MR19 is an optional register. Users shall refer to the vendor datasheet and DEVICE_ID WDR 179th bit.</td><td></td><td></td><td></td></tr></table>

## 6.1 HBM4 Clocking Overview

The HBM device captures commands and addresses on the row and column buses using a differential clock CK\_t/CK\_c. Both buses operate at double data rate (DDR).

The HBM device has uni-directional differential Write strobes (WDQS\_t/WDQS\_c) and Read strobes (RDQS\_t/RDQS\_c) per 32 DQ (DWORD). The data bus operates at double data rate (DDR).

HBM4 utilizes two types of clock with different frequencies. The strobe frequency is twice the frequency of the command clock, requiring an HBM4 to have reset-type clock-divider in the WDQS clock tree (Figure 11). By dividing the WDQS, the operation speed of DRAM internal circuits in WDQS domain is reduced to half. The direction of the internal WDQS/2 transition may vary depending on vendor’s choice. Command clock and WDQS are generated from the same PLL and RDQS clock is generated from WDQS. WDQS internal divider is initialized to be a pre-defined internal divider state after Self Refresh exit or Power-up or Power down exit sequence. The sum of preamble and postamble for both READ and WRITE operation, as well as the sum of WDQS toggles during the training operation performed before the read and write operations, including DCA and DCM, Read DCA training, WRITE training and other related training functions for unmatched DQ/DQS path, is required to be an even number so that the internal divider’s state, or phase of internal WDQS/2, is maintained. Therefore, HBM4 WDQS does not require a specific sync operation before READ and WRITE operations. WDQS starts toggling before starting WRITE or READ operations to reduce ISI. During inactivity, WDQS/ RDQS are required to be static (WDQS/RDQS\_t is Low, WDQS/RDQS\_c is High). When WRITE training for unmatched DQ/DQS path, DQ should be shifted to align phase to the point where CK and WDQS are in sync.

The following nomenclature is being used throughout this standard:

• a rising CK (or WDQS, RDQS) edge is defined as the crossing of the positive edge of CK\_t (or WDQS\_t, RDQS\_t) and the negative edge of CK\_c (or WDQS\_c, RDQS\_c);

• a falling CK (or WDQS, RDQS) edge is defined as the crossing of the negative edge of CK\_t (or WDQS\_t, RDQS\_t) and the positive edge of CK\_c (or WDQS\_c, RDQS\_c).

![](images/614eb55c5895667adb7ef1ca6b0a12fe5bca3757941020ba32a7617549908ebe.jpg)  
Figure 9 — Aligned WDQS Internal Divider Example

## 6.1 HBM4 Clocking Overview (cont’d)

![](images/ccece099e09b34783a390ea076c49a94cfd1a4a58068515a2fd27f7c16a5599d.jpg)  
NOTE 1 tWPRE1 : Write preamble of WDQS, tWPST1 : Write postamble of WDQS NOTE 2 tWPRE2 : Read preamble of WDQS, tWPST2 : Read postamble of WDQS NOTE 3 tRPRE : Read preamble of RDQS, tRPST : Read postamble of RDQS

Figure 10 — Clocking and Interface Relationship Write to Read Timing  
![](images/2fd410f84f53aa4cef97f7767da9026c5d51f64ebf8fc409d1bf8aa8f6ddcccb.jpg)  
Figure 11 — High Level Block Diagram Example of Clocking Scheme

## 6.1.1 WDQS-to-CK Alignment Training

WDQS-to-CK alignment training allows the host to observe the phase offset between the WDQS strobes in both PCs and the CK clock to aid in keeping the phase relationship within the limits given by the t<sub>DQSS</sub> specification. The WDQS2CK bit in MR8 OP3 (Table 19) is associated with this training mode.

WDQS-to-CK alignment training is required to be performed at least once after device initialization if adherence to the t<sub>DQSS</sub> timing cannot be guaranteed without performing this alignment training. WDQSto-CK alignment training is not required if the t<sub>DQSS</sub> timing is met. An effort to further narrow the WDQSto-CK phase offset by using this training mode will not improve the stable device operation.

Steps 1 through 7 are required for WDQS-to-CK alignment training:

1. Enter WDQS-to-CK alignment training mode by setting the WDQS2CK bit to 1 and wait t<sub>MOD</sub> Commands allowed while in this mode are REFab, REFpb, RFMab, RFMpb, RNOP, CNOP and MRS to exit WDQS-to-CK alignment training. Internal current spikes generated by the use of REFab, REFpb, RFMab and RFMpb commands in this mode may negatively impact the training result. Controllers that cannot account for this impact should avoid use of REFab, REFpb, RFMab and RFMpb commands in this mode.

2. Enable both WDQS0 and WDQS1 strobes; keep both strobes constantly running in order to generate a valid read-out at both phase detectors with each CK clock cycle;

3. Slowly sweep the WDQS0 and WDQS1 phases with respect to the CK clock, and monitor both DERR0 and DERR1 signals for the phase detector's result as shown in Table 31 and Figure 12; each phase detector latches the 0° phase of the internally divided WDQS strobe (0° phase) with each rising CK clock edge and provides the result on the DERR0 signal for WDQS0 and the DERR1 signal for WDQS1 after t<sub>WDQS2PD</sub>;

4. After a minimum of 8 WDQS pulses have been received, the strobes may be halted at any time while WDQS-to-CK alignment training mode is enabled; the phase detector does not provide a valid readout in this case and its result on the DERR signals should be ignored;

5. The ideal alignment is indicated by the phase detector output transitioning from "early" to "late" when the delay of the WDQS phase is continuously increased;

6. When the phase relationship between WDQS and CK meets the t<sub>DQSS</sub> specification, stop both WDQS strobes; ensure that the number of WDQS pulses issued while in this training mode is an even number such that the internal WDQS state is back at its reset state once the training has finished. With that, no specific synchronization between CK and WDQS is required for correct write and read operation;

7. Exit WDQS-to-CK alignment training mode by setting the WDQS2CK bit to 0 and wait t<sub>MOD</sub>.

Table 31 — Phase Detector and DERR Signal Behavior
<table><tr><td rowspan=1 colspan=1>Internal WDQS/2 (0° Phase)Sampled By CK</td><td rowspan=1 colspan=1>WDQS Phase</td><td rowspan=1 colspan=1>DERR0DERR1</td><td rowspan=1 colspan=1>Recommended Action</td></tr><tr><td rowspan=1 colspan=1>HIGH</td><td rowspan=1 colspan=1>Early</td><td rowspan=1 colspan=1>HIGH</td><td rowspan=1 colspan=1>Increase delay on WDQS</td></tr><tr><td rowspan=1 colspan=1>LOW</td><td rowspan=1 colspan=1>Late</td><td rowspan=1 colspan=1>LOW</td><td rowspan=1 colspan=1>Decrease delay on WDQS</td></tr></table>

## 6.1.1 WDQS-to-CK Alignment Training (cont’d)

![](images/c413dab4395c01999f78408e6a80290331de3b05059d0aa0f9c174ff818fc767.jpg)  
Figure 12 — DERR Signal Behavior in WDQS-to-CK Alignment Training

## 6.2 HBM4 Data Bus Inversion (DBIac)

## 6.2.1 Data Bus Inversion (DBIac)

HBM4 DRAMs supports a byte granular Data Bus Inversion (DBIac). The corresponding DBI signal is a DDR I/O and driven or sampled along with the DQs for read and write operations.

The word DBI refers to the internal state of the device unless explicitly noted as DBI signal. The DBIac function can be enabled or disabled independently for writes per MR0 OP1 (WDBI) and for reads per MR0 OP0 (RDBI).

The DBI input is a Don't care and the DBI input receivers are disabled when WDBI is disabled. The DBI output buffers are turned off when RDBI is disabled.

![](images/af964573b6f9e3c9a7b4ff43c6d4d3e84b05888d91e0571a0242d9e0aab6345b.jpg)  
Figure 13 — DBIac Algorithm

Write operation: the HBM4 DRAM inverts write data received on the DQ inputs in case DBI is sampled HIGH, or leaves the write data non-inverted in case DBI is sampled LOW. Note that the ECC inputs are not affected by the DBIac function.

Read operation: the HBM4 DRAM counts the number of DQ signals that are transitioning from the previous state. Note that the ECC and SEV outputs are not affected by DBIac. See Internal DBIac States with Read for bus pre-conditioning. The HBM4 DRAM inverts read data and sets DBI HIGH when the number of transitioning data bits within a byte is greater than 4, or when the number of transitioning data bits within a byte equals 4 and DBI was HIGH; otherwise, the HBM4 DRAM does not invert the read data and sets DBI LOW.

![](images/d5f9b18c70a4e277bc211c3df86ce5f6bc74534c32331564dc6beac976bf225c.jpg)

## 6.2.1 Data Bus Inversion (DBIac) (cont’d)

Table 32 — DBI(ac) Truth Table
<table><tr><td rowspan=1 colspan=1>DQ Charge Count</td><td rowspan=1 colspan=1>Previous DBI State</td><td rowspan=1 colspan=1>New DBI State</td><td rowspan=1 colspan=1>New DQ State</td></tr><tr><td rowspan=1 colspan=1>0 to 3</td><td rowspan=1 colspan=1>X</td><td rowspan=2 colspan=1>LOW</td><td rowspan=2 colspan=1>Not inverted</td></tr><tr><td rowspan=2 colspan=1>4</td><td rowspan=1 colspan=1>LOW</td></tr><tr><td rowspan=1 colspan=1>HIGH</td><td rowspan=2 colspan=1>HIGH</td><td rowspan=2 colspan=1>Inverted</td></tr><tr><td rowspan=1 colspan=1>5 to 8</td><td rowspan=1 colspan=1>X</td></tr></table>

![](images/eb7250bfe23717337f2fc903551bff4131dd172248ed11cd9ffc37df72635d63.jpg)  
Figure 14 — Example DBIac Logic for Write and Read

## 6.2.1.1 Internal DBIac State with Read

The HBM4 DRAM resets the internal DBIac state to LOW whenever any of the following events occur:

• RESET\_n signal de-assertion;

• a MODE REGISTER SET (MRS) command is received;

• a write-to-read bus turnaround;

Self Refresh exit

For all other events or commands, the internal DBIac state is not reset to LOW and the HBM4 DRAM will use its previous state for DBIac calculation.

## First Read Command:

When a first READ command is registered after a DBI reset, the HBM4 DRAM preconditions the bus to LOW prior to read data regardless whether RDBI is enabled or disabled in the mode register, as shown in Figure 15 in case of a write-to-read bus turnaround. The internal state D7 corresponding to the last UI of the read burst is internally stored as a seed value for a subsequent read burst.

The DPAR signal is not included in the DBI calculation and not preconditioned to LOW; its initial state is undefined (LOW or HIGH).

## 6.2.1.1 Internal DBIac State with Read (cont’d)

![](images/05dd1b5ee29677dc6f8f1e1642357b197040c131174b7b672ccee4761ff3acaa.jpg)  
Figure 15 — Internal DBIac State Reset for Write to Read

## 6.2.1.2 Internal DBIac State with Consecutive Read Commands (Seamless and non-seamless)

Once the Read burst is complete, the HBM4 DRAM tri-states all DQ, DBI and ECC output drivers. However, the HBM4 DRAM internally stores the last data-out of the DQ, DBI, ECC and SEV outputs to pre-condition the bus prior to a subsequent read; it also uses the last data-out of the DQ and DBI outputs for DBIac calculation for any subsequent read operation barring a condition to DBI reset. For non-gapless read operations, the HBM4 DRAM pre-conditions all data outputs to the last data-out of the previous burst nominally two WDQS cycles (odd bytes) and one WDQS cycle (even bytes) prior to the first valid data bit as shown in Figure 16.

6.2.1.2 Internal DBIac State with Consecutive Read Commands (Seamless and non-seamless) (cont’d)  
![](images/0e4ff6d2fea7104933d4cf2603f0422b1da7a4815eb7d495f267d49f78c865ad.jpg)  
Figure 16 — Bus Preconditioning and DBI States for Read

## 6.3 Commands

The HBM4 DRAM features DDR commands entered on both rising and falling CK clock edges. Row Activate commands require one-and-a-half-cycle and other row commands require only a half-cycle except for PDE and SRE with one cycle. Column commands require only one cycle.

The command interface includes a reserved DDR input signal ARFU which is omitted from subsequent truth tables but required to be driven to a valid signal level along with the other AWORD inputs.

## 6.3.1 Command Truth Tables

Table 33 — Row Commands Truth Table
<table><tr><td rowspan=1 colspan=1>Command 4</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>ClockCycle</td><td rowspan=1 colspan=1>R0</td><td rowspan=1 colspan=1>R1</td><td rowspan=1 colspan=1>R2</td><td rowspan=1 colspan=1>R3</td><td rowspan=1 colspan=1>R4</td><td rowspan=1 colspan=1>R5</td><td rowspan=1 colspan=1>R6</td><td rowspan=1 colspan=1>R7</td><td rowspan=1 colspan=1>R8</td><td rowspan=1 colspan=1>R9</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Row NoOperation</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>RorF</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1,2,3</td></tr><tr><td rowspan=3 colspan=1>Activate</td><td rowspan=3 colspan=1>ACT</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>PC</td><td rowspan=1 colspan=1>SID0/V</td><td rowspan=1 colspan=1>SID1/V</td><td rowspan=1 colspan=1>BA0</td><td rowspan=1 colspan=1>BA1</td><td rowspan=1 colspan=1>BA2</td><td rowspan=1 colspan=1>BA3</td><td rowspan=1 colspan=1>1,2, 3,5,6</td></tr><tr><td rowspan=1 colspan=1>F</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>RA8</td><td rowspan=1 colspan=1>RA9</td><td rowspan=1 colspan=1>RA10</td><td rowspan=1 colspan=1>RA11</td><td rowspan=1 colspan=1>RA12</td><td rowspan=1 colspan=1>RA13</td><td rowspan=1 colspan=1>RA14/V</td><td rowspan=1 colspan=1>DRFM</td><td rowspan=2 colspan=1></td></tr><tr><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>RA0</td><td rowspan=1 colspan=1>RA1</td><td rowspan=1 colspan=1>RA2</td><td rowspan=1 colspan=1>RA3</td><td rowspan=1 colspan=1>RA4</td><td rowspan=1 colspan=1>RA5</td><td rowspan=1 colspan=1>RA6</td><td rowspan=1 colspan=1>RA7</td></tr><tr><td rowspan=1 colspan=1>Precharge per-bank</td><td rowspan=1 colspan=1>PREpb</td><td rowspan=1 colspan=1>RorF</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>PC</td><td rowspan=1 colspan=1>SID0/V</td><td rowspan=1 colspan=1>SID1/V</td><td rowspan=1 colspan=1>BA0</td><td rowspan=1 colspan=1>BA1</td><td rowspan=1 colspan=1>BA2</td><td rowspan=1 colspan=1>BA3</td><td rowspan=1 colspan=1>1, 2, 3, 5,6</td></tr><tr><td rowspan=1 colspan=1>Prechargeall-bank</td><td rowspan=1 colspan=1>PREab</td><td rowspan=1 colspan=1>R orF</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>PC</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1,2, 3,5,</td></tr><tr><td rowspan=1 colspan=1>RefreshPer-Bank</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>PC</td><td rowspan=1 colspan=1>SID0/V</td><td rowspan=1 colspan=1>SID1/V</td><td rowspan=1 colspan=1>BA0</td><td rowspan=1 colspan=1>BA1</td><td rowspan=1 colspan=1>BA2</td><td rowspan=1 colspan=1>BA3</td><td rowspan=1 colspan=1>1,2, 3, 5,6</td></tr><tr><td rowspan=1 colspan=1>RefreshAll-Bank</td><td rowspan=1 colspan=1>REFab</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>PC</td><td rowspan=1 colspan=1>V/ECS</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1, 2, 3, 5,10</td></tr><tr><td rowspan=1 colspan=1>RefreshManagementPer-Bank</td><td rowspan=1 colspan=1>RFMpb(DRFMpb)</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>PC</td><td rowspan=1 colspan=1>SID0/V</td><td rowspan=1 colspan=1>SID11V</td><td rowspan=1 colspan=1>BA0</td><td rowspan=1 colspan=1>BA1</td><td rowspan=1 colspan=1>BA2</td><td rowspan=1 colspan=1>BA3</td><td rowspan=1 colspan=1>1, 2, 3, 5,6,7,11</td></tr><tr><td rowspan=1 colspan=1>RefreshManagementAll-Bank</td><td rowspan=1 colspan=1>RFMab</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>PC</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>y</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1,2,3,5,7</td></tr><tr><td rowspan=2 colspan=1>Power-DownEntry</td><td rowspan=2 colspan=1>PDE</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1,2,3</td></tr><tr><td rowspan=1 colspan=1>F</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=2 colspan=1>Self RefreshEntry</td><td rowspan=2 colspan=1>SRE</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>V/ECS</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=2 colspan=1>1,2,3,10</td></tr><tr><td rowspan=1 colspan=1>F</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td></tr><tr><td rowspan=1 colspan=1>Power-Downand SelfRefresh Exit</td><td rowspan=1 colspan=1>PDX/ SRX</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1,2,8</td></tr><tr><td rowspan=1 colspan=14>NOTE 1BA = Bank Address; RA = Row Address; PC = Pseudo Channel 0 or 1; SID = Stack ID; V = Valid Signal (either H or L, but not floating)NOTE 2 R[9:0] must be driven to a valid signal level even if a stack ID address (SID) or row address (RA) is not defined for a specific density. APARmust be driven to a valid signal level even if CA parity is disabled in MR0 OP6.NOTE 3 Parity is evaluated on all pins if CA parity is enabled in MR0 OP6.NOTE 4 All other command encodings not shown in the table are reserved for future use.NOTE 5 PC = 0 selects pseudo channel 0 (PC0), and PC = 1 selects pseudo channel 1 (PC1). The pseudo channel not selected by PC performs aRNOP.NOTE 6 The SID bits act as bank address bits in conjunction with ACT, PREpb, REFpb and RFMpb commands, and related timing diagrams shall beinterpreted accordingly. All other row commands do not use SID. Refer to the channel addressing table for HBM4 configurations using SID.NOTE 7 An HBM4 DRAM not requiring refresh management (RFM) will execute an RNOP command instead of RFMabor RFMpb.NOTE 8Parity is not checked at Power-Down Exit or Self Refresh Exit. The HBM4 device requires RNOP andCNOP commands on Row and Column bus respectively with valid parity if CA parity is enabled during the power-down exit period (txp) and self refresh exit period (txs).NOTE 9 ACT is a 1.5 cycle command. Only a RNOP command, a PREpb command to a different bank or a PREab to a different PC areallowed following an ACT command on the falling edge of the second cycle.NOTE 10 See the Auto ECS clause for more details on the optional ECS flag feature.NOTE 11 After the host requested address has been captured by the DRAM the subsequent RFMpb command to that bank is referred to asa DRFMpb command. See the Directed Refresh Management (DRFM) clause for more details.</td></tr></table>

## 6.3.1 Command Truth Tables (cont’d)

Table 34 — Column Commands Truth Table
<table><tr><td rowspan=1 colspan=1>Command 4</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>ClockCycle</td><td rowspan=1 colspan=1>C0</td><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>C2</td><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>C4</td><td rowspan=1 colspan=1>C5</td><td rowspan=1 colspan=1>C6</td><td rowspan=1 colspan=1>C7</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=2 colspan=1>Column NoOperation</td><td rowspan=2 colspan=1>CNOP</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=2 colspan=1>1,2,3</td></tr><tr><td rowspan=1 colspan=1>F</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>V</td></tr><tr><td rowspan=2 colspan=1>Read</td><td rowspan=2 colspan=1>RD</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>PC</td><td rowspan=1 colspan=1>SID0/V</td><td rowspan=1 colspan=1>SID1/V</td><td rowspan=1 colspan=1>BA0</td><td rowspan=2 colspan=1>1, 2, 3, 5,6,7</td></tr><tr><td rowspan=1 colspan=1>F</td><td rowspan=1 colspan=1>BA1</td><td rowspan=1 colspan=1>BA2</td><td rowspan=1 colspan=1>BA3</td><td rowspan=1 colspan=1>CA0</td><td rowspan=1 colspan=1>CA1</td><td rowspan=1 colspan=1>CA2</td><td rowspan=1 colspan=1>CA3</td><td rowspan=1 colspan=1>CA4</td></tr><tr><td rowspan=2 colspan=1>Read w/ AP</td><td rowspan=2 colspan=1>RDA</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>PC</td><td rowspan=1 colspan=1>SID0/V</td><td rowspan=1 colspan=1>SID1/V</td><td rowspan=1 colspan=1>BA0</td><td rowspan=2 colspan=1>1,2, 3, 5,6,7</td></tr><tr><td rowspan=1 colspan=1>F</td><td rowspan=1 colspan=1>BA1</td><td rowspan=1 colspan=1>BA2</td><td rowspan=1 colspan=1>BA3</td><td rowspan=1 colspan=1>CA0</td><td rowspan=1 colspan=1>CA1</td><td rowspan=1 colspan=1>CA2</td><td rowspan=1 colspan=1>CA3</td><td rowspan=1 colspan=1>CA4</td></tr><tr><td rowspan=2 colspan=1>Write</td><td rowspan=2 colspan=1>WR</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>PC</td><td rowspan=1 colspan=1>SID0/V</td><td rowspan=1 colspan=1>SID1/V</td><td rowspan=1 colspan=1>BA0</td><td rowspan=2 colspan=1>1,2, 3, 5,6</td></tr><tr><td rowspan=1 colspan=1>F</td><td rowspan=1 colspan=1>BA1</td><td rowspan=1 colspan=1>BA2</td><td rowspan=1 colspan=1>BA3</td><td rowspan=1 colspan=1>CA0</td><td rowspan=1 colspan=1>CA1</td><td rowspan=1 colspan=1>CA2</td><td rowspan=1 colspan=1>CA3</td><td rowspan=1 colspan=1>CA4</td></tr><tr><td rowspan=2 colspan=1>Write w/ AP</td><td rowspan=2 colspan=1>WRA</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>H</td><td rowspan=1 colspan=1>PC</td><td rowspan=1 colspan=1>SID0/V</td><td rowspan=1 colspan=1>SID1/V</td><td rowspan=1 colspan=1>BA0</td><td rowspan=2 colspan=1>1,2,3,5,6</td></tr><tr><td rowspan=1 colspan=1>F</td><td rowspan=1 colspan=1>BA1</td><td rowspan=1 colspan=1>BA2</td><td rowspan=1 colspan=1>BA3</td><td rowspan=1 colspan=1>CA0</td><td rowspan=1 colspan=1>CA1</td><td rowspan=1 colspan=1>CA2</td><td rowspan=1 colspan=1>CA3</td><td rowspan=1 colspan=1>CA4</td></tr><tr><td rowspan=2 colspan=1>Mode RegisterSet</td><td rowspan=2 colspan=1>MRS</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>L</td><td rowspan=1 colspan=1>MA4</td><td rowspan=1 colspan=1>OP5</td><td rowspan=1 colspan=1>OP6</td><td rowspan=1 colspan=1>OP7</td><td rowspan=1 colspan=1>MA0</td><td rowspan=2 colspan=1>1,3,8,9</td></tr><tr><td rowspan=1 colspan=1>F</td><td rowspan=1 colspan=1>MA1</td><td rowspan=1 colspan=1>MA2I</td><td rowspan=1 colspan=1>MA3</td><td rowspan=1 colspan=1>OP0</td><td rowspan=1 colspan=1>OP1</td><td rowspan=1 colspan=1>OP2</td><td rowspan=1 colspan=1>OP3</td><td rowspan=1 colspan=1>OP4</td></tr><tr><td rowspan=1 colspan=12>NOTE 1 BA = Bank Address; CA = Column Address; PC = Pseudo Channel 0 or 1; SID = Stack ID; MA = Mode RegisterAddress; V = Valid Signal (either H or L, but not floating).NOTE 2 C[7:0] must be driven to a valid signal level even if a stack ID address (SID) is not defined for a specific density, orif parity is disabled in the mode register. APAR must be driven to a valid signal level even if CA parity is disabledin MR0 OP6. C[7:0] are Don&#x27;t Care when the device is in power-down or self refresh.NOTE 3Parity is evaluated on all pins if CA parity is enabled in MR0 OP6.NOTE 4All other command encodings not shown in the table are reserved for future use.NOTE 5PC = 0 selects pseudo channel 0 (PC0), and PC = 1 selects pseudo channel 1 (PC1). The pseudo channel notselected by PC performs a CNOP.NOTE 6 The SID bits act as bank address bits in conjunction with READ and WRITE commands, and related timingdiagrams shall be interpreted accordingly. All other column commands do not use SID. Refer to the channeladdressing table for HBM4 configurations using SID.NOTE 7HBM4 configurations using the SID specify a timing parameter tccDR for consecutive READs to different SID.Vendor datasheets should be consulted for details.NOTE 8All mode registers are write-only by default using the MRS command.NOTE 9 Refer to the HBM4 Mode Register Overview table (Table 9) for MA4 of MRS.</td></tr></table>

## 6.3.1 Command Truth Tables (cont’d)

Table 35 — Options for Issuing PREab and PREpb Commands
<table><tr><td rowspan=2 colspan=1>Command onRisingClock Edge</td><td rowspan=1 colspan=3>Allowed PREab/PREpb Command(s) on Falling Clock Edge (Same Cycle)</td></tr><tr><td rowspan=1 colspan=1>Same PC, Same Bank</td><td rowspan=1 colspan=1>Same PC, Different Bank</td><td rowspan=1 colspan=1>Different PC, Any Bank</td></tr><tr><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=2>PREab, PREpb</td><td rowspan=1 colspan=1>PREab, PREpb</td></tr><tr><td rowspan=1 colspan=1>ACT</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>PREpb</td><td rowspan=1 colspan=1>PREab, PREpb</td></tr><tr><td rowspan=1 colspan=1>PREab</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>PREab, PREpb</td></tr><tr><td rowspan=1 colspan=1>PREpb</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>PREpb</td><td rowspan=1 colspan=1>PREab, PREpb</td></tr><tr><td rowspan=1 colspan=1>REFab</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>--</td><td rowspan=1 colspan=1>PREab, PREpb</td></tr><tr><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>PREpb</td><td rowspan=1 colspan=1>PREab, PREpb</td></tr><tr><td rowspan=1 colspan=1>RFMab</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>PREab, PREpb</td></tr><tr><td rowspan=1 colspan=1>RFMpb</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>PREpb</td><td rowspan=1 colspan=1>PREab, PREpb</td></tr><tr><td rowspan=1 colspan=1>PDE, SRE</td><td rowspan=1 colspan=3></td></tr><tr><td rowspan=1 colspan=1>PDX, SRX</td><td rowspan=1 colspan=3></td></tr></table>

## 6.3.2 Row Commands

## 6.3.2.1 Row No Operation (RNOP) Command

The ROW NO OPERATION (RNOP) command is a half-cycle command received on the row command inputs R[9:0] and latched either with the rising or with the falling CK clock edge (or both edges) as shown in Figure 17. RNOP is used to instruct the HBM4 device to perform a NOP as row command; this prevents unwanted row commands from being registered during idle or wait states. Operations already in progress are not affected.

Row commands other than RNOP are defined either as half-cycle or as one-and-a-half-cycle commands that begin and end on a rising CK clock edge. These commands must be padded with RNOP on the falling CK clock edge of the same cycle. As an alternative, some row commands may be paired with PREpb or PREab commands on the falling CK clock edge instead of RNOP, with the specific conditions for these commands being explicitly described for each row command.

Parity is evaluated with the RNOP command when the parity calculation is enabled in the Mode Register.

RNOP is assumed for the R[9:0] inputs on subsequent timing diagrams unless other row commands are explicitly shown.

![](images/f7f905b027f152306d9a2ac87657f49a4ddc6f0759fb56f272cb3e096b855b30.jpg)  
Figure 17 — RNOP Command

## 6.3.2.2 ACTIVATE (ACT) Command

Before a READ or WRITE command can be issued to a bank, a row in that bank must be opened. This is accomplished via the ACTIVATE command, which selects both the bank and the row to be activated. Once a row is open, a READ or WRITE command could be issued to that row, subject to the t<sub>RCD</sub> specification.

The ACTIVATE command is a one-and-a-half-cycle command received on the row command inputs R[9:0] and latched with the rising and falling CK clock edges as shown in Figure 18. The command must be followed either by RNOP, PREpb or PREab on the falling CK clock edge of the second clock cycle. Note that a PREab in that case must be for the other pseudo channel. A PREpb command could be to any bank in the other pseudo channel as well as to a different bank in the same pseudo channel. In all cases the timing requirements for issuing these commands must be met.

The actual bank and row activation is initiated with the second rising CK clock edge of the ACTIVATE command; therefore all relevant timing parameters refer to this second rising CK clock edge as shown in Figure 19 and Figure 20.

## 6.3.2.2 ACTIVATE (ACT) Command (cont’d)

![](images/0fdec77dde8431119fbb53f2241aac8f565508eb942ce6f374283f54fcaf1520.jpg)  
NOTE 1 BA = Bank Address; PC = Pseudo Channel 0 or 1; RA = Row Address; SID = Stack ID; V = Valid (H or L) Figure 18 — ACTIVATE Command

Parity is evaluated with the ACTIVATE command when the parity calculation is enabled in MR0 OP6.

A subsequent ACTIVATE command to another row in the same bank can only be issued after the previous row has been closed (precharged). A subsequent ACTIVATE can be issued to the same row address without closing the row to capture the address for DRFM. See the DRFM clause for more details. The minimum time interval between successive ACTIVATE commands to the same bank is defined by t<sub>RC</sub>, as shown in Figure 19. A minimum time t<sub>RAS</sub> must have elapsed between opening and closing a row. The figure also shows two cases of t timings and command slots of the PRECHARGE command.

A subsequent ACTIVATE command to another bank can be issued while the first bank is being accessed, which results in a reduction of total row access overhead. The minimum time interval between successive ACTIVATE commands to different banks is defined by tRRD. The row remains active until a PREpb command (or READ or WRITE command with Auto Precharge) is issued to the bank.

## 6.3.2.2 ACTIVATE (ACT) Command (cont’d)

Case1 : tRAS timing met at rising CK clock edge  
![](images/67b53b18897326760cc3d89f471fe12ecb0c95f2b8a6b1a8f42492a80c4078eb.jpg)

Case2 : tRAS timing met at falling CK clock edge  
![](images/c707b0dcdaf8d6ec2e86ae7d3661c6a6f580fc7c9ab8bb68268fbe3b682c084a.jpg)  
NOTE 1 BAx = bank address x; RAy,z = row addresses y,z; CAn = column address n.  
NOTE 2 The PRECHARGE command shown could also be a PRECHARGE ALL command.  
NOTE 4 The reference for tXP and tXS timings is the first clock cycle of an ACTIVATE command, and the reference for tRFC and t timing is the second clock cycle of an ACTIVATE command.  
NOTE 3 tRCD = tRCDRD or tRCDWR, depending on command; tRFC = tRFCab or tRFCpb, depending on command.

Figure 19 — Bank and Row Activation Command Cycle

## 6.3.2.2.1 Bank Restrictions

There is a need to limit the number of bank activations in a rolling window to ensure that the instantaneous current supplying capability of the device is not exceeded. To reflect the short term current supply capability, the parameter tFAW (four activate window) is defined: no more than 4 banks may be activated in a rolling tFAW window. Converting to clocks is done by dividing tFAW (ns) by tCK (ns) and rounding up to next integer value. As an example of the rolling window, if (tFAW/tCK) rounds up to 25 clocks, and an ACTIVATE command is issued at clock T0, no more than three further ACTIVATE commands may be issued at clocks T1 through T24 as illustrated in Figure 20.

![](images/dfa88e0f5228392639be08554059c7bc030043c67acb96771de2af1450cb6aa1.jpg)  
NOTE 1 tRRD = tRRDS or tRRDL, depending on accessed banks.

NOTE 2 Refer to the “REFRESH and PER-BANK REFRESH Command Scheduling Requirements” table for timing restrictions between all combinations of ACTIVATE and PER-BANK REFRESH commands.

Figure 20 — Multiple Bank Activations

## 6.3.2.3 PRECHARGE (PREpb) and PRECHARGE ALL (PREab) Commands

The PRECHARGE (PREpb) and PRECHARGE ALL (PREab) commands are half-cycle commands received on the row command inputs R[9:0] and latched either with the rising or with the falling CK clock edge as shown in Figure 21 and Figure 22. The commands are used to deactivate the open row in a particular bank PREpb or the open rows in all banks PREab. The bank(s) will be in idle state and available for a subsequent row access a specified time t<sub>RP</sub> after the PREpb command is issued.

The fact that both are half-cycle commands and defined on both the rising and the falling CK clock edges allows to issue one PREpb or PREab command on the rising CK clock edge and a second PREpb or PREab command on the falling CK clock edge of the same cycle and thus deactivate the open row in two different banks or even all banks in both pseudo channels within a single clock cycle, provided the t<sub>PPD</sub> timing has been met. It is pointed out that the t<sub>RP</sub> timing is always referenced from the CK clock edge on which the PREpb or PREab command is issued.

Parity is evaluated with the PREpb and PREab commands when the parity calculation is enabled in MR0 OP6.

## 6.3.2.3 PRECHARGE (PREpb) and PRECHARGE ALL (PREab) Commands (cont’d)

![](images/fbe548c34e9ce71e86461a2354f485b3e04c7db703547bbbc3066242e646d687.jpg)  
NOTE 1 BA = Bank Address; PC = Pseudo Channel 0 or 1; SID = Stack ID; V = Valid (H or L)

Figure 21 — PRECHARGE (PREpb) Command  
![](images/c473b0092d9beb0a944e1af597dbbf23bac4ffb39a0dfd00e9bc4862becb71fa.jpg)  
NOTE 1 BA = Bank Address; PC = Pseudo Channel 0 or 1; SID = Stack ID; V = Valid (H or L)  
Figure 22 — PRECHARGE ALL (PREab) Command

Input R2 determines whether one or all banks are to be precharged. In case where only one bank is to be precharged, bank addresses {SID[1:0], BA[3:0]} select the bank. Otherwise, the bank addresses are treated as “Don’t Care”.

Once a bank has been precharged, it is in the idle state and must be activated prior to any READ or WRITE command being issued to that bank. A PREpb command is allowed if there is no open row in that bank (idle state), or if the previously open row is already in the process of precharging. However, the precharge period shall be determined by the most recent PREpb command issued to the bank.

## 6.3.2.3.1 AUTO PRECHARGE

Auto Precharge is a feature which performs the same individual-bank precharge function described in Figure 21 and Figure 22, but without requiring an explicit PREpb command. Auto Precharge is nonpersistent meaning that it is enabled or disabled along for each individual READ or WRITE command.

For read bursts, an auto precharge of the bank and row that is addressed with the READ command begins RTP clock cycles after the READ command was issued or after RAS has been met, with RTP as programmed in clock cycles in MR5 OP[3:0] and RAS as programmed in clock cycles in the RAS field of Mode Register MR4 OP[7:0].

For write bursts, an auto precharge of the bank and row that is addressed with the WRITE command begins (WL + 2 + WR) clock cycles after the WRITE command was issued or after RAS has been met, with WR as programmed in clock cycles in MR3 OP[7:0] and RAS as programmed in clock cycles in MR4 OP[7:0].

Auto Precharge ensures that the precharge is initiated at the earliest valid stage within a burst. The user must not issue another command to the same bank until the precharge (t<sub>RP</sub>) is completed. This is determined as if an explicit PREpb command was issued at the earliest possible time, as described for READ or WRITE commands. A precharge resulting from a READ or WRITE with Auto Precharge may occur in parallel with an explicit PREpb (or PREab) command. It is pointed out that an auto precharge is internally always issued with a rising CK clock edge, while explicit PREpb (or PREab) commands are supported on both clock edges.

## 6.3.2.3.1 AUTO PRECHARGE (cont’d)

Table 36 — Precharge and Auto Precharge Timings
<table><tr><td rowspan=1 colspan=1>FromCommand</td><td rowspan=1 colspan=1>To Command</td><td rowspan=1 colspan=1>Minimum Delay Between“From Command”to “To Command”</td><td rowspan=1 colspan=1>Unit</td><td rowspan=1 colspan=1>Note</td></tr><tr><td rowspan=5 colspan=1>READ</td><td rowspan=1 colspan=1>PRECHARGE (same bank)</td><td rowspan=1 colspan=1>tRTP</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>PRECHARGE (different bank)</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>PRECHARGE ALL</td><td rowspan=1 colspan=1>tRTP</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>WRITE or WRITE w/ AP (any bank)</td><td rowspan=1 colspan=1>tRTW</td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>READ or READ w/ AP (any bank)</td><td rowspan=1 colspan=1>tccD</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=7 colspan=1>READ w/ AP</td><td rowspan=1 colspan=1>PRECHARGE ALL</td><td rowspan=1 colspan=1>tRTP</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>PRECHARGE (different bank)</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>ACTIVATE or PER BANK REFRESH(same bank)</td><td rowspan=1 colspan=1>RTP + RU(tRP/tcK)</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>2,8</td></tr><tr><td rowspan=1 colspan=1>WRITE or WRITE w/ AP (same bank)</td><td rowspan=1 colspan=1>Illegal</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>WRITE or WRITE w/ AP (different bank)</td><td rowspan=1 colspan=1>tRTW</td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>READ or READ w/ AP (same bank)</td><td rowspan=1 colspan=1>Illegal</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>READ or READ w/ AP (different bank)</td><td rowspan=1 colspan=1>tccD</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=7 colspan=1>WRITE</td><td rowspan=1 colspan=1>PRECHARGE (same bank)</td><td rowspan=1 colspan=1>WL + 2 + RU(twR/tck)</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>2,6</td></tr><tr><td rowspan=1 colspan=1>PRECHARGE (different bank)</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>PRECHARGE ALL</td><td rowspan=1 colspan=1>WL + 2 + RU(twR/tck)</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>2,6</td></tr><tr><td rowspan=1 colspan=1>WRITE or WRITE w/ AP (any bank)</td><td rowspan=1 colspan=1>tccD</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=1>READ w/ AP (same bank)              6</td><td rowspan=1 colspan=1>WL + 2 + MAX[RU(twR/tcK) − tRTP,tWTR]</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>2,6,7</td></tr><tr><td rowspan=1 colspan=1>READ (same bank)</td><td rowspan=1 colspan=1>WL + 2 + twTR</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>6,7</td></tr><tr><td rowspan=1 colspan=1>READ or READ w/ AP (different bank)</td><td rowspan=1 colspan=1>WL + 2 + twTR</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>6,7</td></tr><tr><td rowspan=7 colspan=1>WRITE w/ AP</td><td rowspan=1 colspan=1>PRECHARGE ALL</td><td rowspan=1 colspan=1>WL + 2 + RU(twR/tck)</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>2,6</td></tr><tr><td rowspan=1 colspan=1>PRECHARGE (different bank)</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>ACTIVATE or PER BANK REFRESH(same bank)</td><td rowspan=1 colspan=1>WL + 2 + WR + RU(tRp/tcK)</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>2,6,8</td></tr><tr><td rowspan=1 colspan=1>WRITE or WRITE w/ AP (same bank)</td><td rowspan=1 colspan=1>Illegal</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>WRITE or WRITE w/ AP (different bank)</td><td rowspan=1 colspan=1>tccD</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=1>READ or READ w/ AP (same bank)</td><td rowspan=1 colspan=1>Illegal</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>READ or READ w/ AP (different bank)</td><td rowspan=1 colspan=1>WL + 2 + twTR</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>6,7</td></tr><tr><td rowspan=2 colspan=1>PRECHARGE</td><td rowspan=1 colspan=1>PREpb (any bank)</td><td rowspan=1 colspan=1>tpPD</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>PREab</td><td rowspan=1 colspan=1>tPPD</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>PRECHARGEALL</td><td rowspan=1 colspan=1>PREpb or PREab</td><td rowspan=1 colspan=1>tpPD</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=5>NOTE 1 A command issued during the minimum delay time is illegal.NOTE 2 RU = round up to next integer.NOTE 3 A PREpb command is allowed if there is no open row in that bank (idle state), or if the previously open row isalready in the process of precharging. However, the precharge period shall be determined by the most recentPRECHARGE command issued to the bank.NOTE 4 READ or WRITE and PREpb commands may be issued simultaneously.NOTE 5 tccD could either be tccds or tccDL; for READs, tccD could also be tccDR.NOTE 6 WL = write latency.NOTE 7 twTR could either be twTRs or twTRL.NOTE 8 Even if tRp is satisfied from PREab command, tRP generated from previous WRA or RDA (Write or Read with Autoprecharge) should also be satisfied.</td></tr></table>

## 6.3.2.4 Rounding Rules for Row Access Timings

The HBM4 DRAM allows the PREpb and PREab commands to be issued on both rising and falling CK clock edges, as e.g., illustrated in the Bank and Row Activation Command Cycle figure. To let a system take advantage of this flexibility in command scheduling, it is required to adapt the rounding rules for related row access timings.

Traditionally, basic row access timings are converted into clock cycles using the formula nXX = RU(tXX/tCK), with XX representing either RAS, RTP, WR or RP parameters. This formula rounds the analog timings up to the next integer such that the subsequent command can be issued on the next rising clock edge that meets the analog value.

For HBM4 DRAM, this formula is replaced by nXX = 0.5 × RU(2 × tXX/tCK), which rounds analog timings to the next rising or following clock edge that meets the analog value. The result may be the same as with the traditional formula, or 0.5 nCK less. The formula may be applied to row timings tRAS, tRTP, tWR and tRP, only. If rounding the tRP timing results in a falling edge as the command slot for a subsequent row access command, it is required to add 0.5 nCK to the result because all such row commands following a row precharge can be issued on a rising clock edge only.

## Examples:

tR $\mathrm { A S } = 3 3 ~ \mathrm { n s , t C K } = 0 . 7 ~ \mathrm { n s ; n R A S } = 0 . 5 \times \mathrm { R U } ( 2 ~ \mathrm { x ~ t R A S / t C K } ) = 0 . 5 \times \mathrm { R U } ( 2 \times 3 3 / 0 . 7 ) = 0 . 5 \times \mathrm { R U } ( 2 \times 3 3 / 0 . 7 )$ RU(94.29) = 47.5. Conclusion: When the ACTIVATE command was issued at T0, the earliest possible slot for a PRECHARGE command is at T47.5 (falling clock edge).

tR $\mathbf { P } = 1 5 \mathrm { ~ n s , ~ t C K } = 0 . 7 \mathrm { ~ n s ; ~ n R P } = 0 . 5 \times \mathrm { { R U } } ( 2 \times \mathrm { { t R P } / t C K } ) = 0 . 5 \times \mathrm { { R U } } ( 2 \times 1 5 / 0 . 7 ) = 0 . 5 \times \mathrm { { R U } } ( 2 \times 1 5 / 0 . 7 )$ RU(42.85) = 21.5. Conclusion: When the PREpb command was issued at T0 (rising edge), the earliest possible slot for a subsequent ACTIVATE command is at T22, because the falling edge at T21.5 is not supported for an ACTIVATE command and 0.5 nCK must be added to the result. However, when the PREpb command was issued at T0.5 (falling edge), the earliest possible slot for a subsequent ACTIVATE command is again at T2.

## 6.3.2.5 Refresh

The REFRESH command (REF) is used during normal operation of the HBM4 DRAMs. Since “data” is stored as 0s and 1s in capacitors in a DRAM, and the capacitors leak charge over time. A REFRESH command is issued periodically to restore (refresh) the electrical charge in the capacitors. Each REFRESH command results in one or more activate operations to a selected row or rows, followed by a self-timed precharge to close the rows opened during the activate.

REFRESH commands are non-persistent, so they must be issued each time a refresh is required. The HBM4 DRAM requires REFRESH commands to be issued at an average periodic interval of tREFI.

There are several types of refresh operations supported by HBM4 DRAMs.

<sup></sup> REFRESH all-bank (REFab)

<sup></sup> REFRESH per-bank (REFpb)

<sup></sup> REFRESH MANAGEMENT all-bank (RFMab)

<sup></sup> REFRESH MANAGEMENT per-bank (RFMpb)

<sup></sup> DIRECTED REFRESH MANAGEMENT (DRFMpb/RFMpb)

This clause describes the details of the refresh operations and requirements for each of the refresh operation types as well as the transitions between the refresh operation types.

## 6.3.2.5.1 REFRESH Command (REFab)

The REFRESH all-bank command (REFab) is a half-cycle command received on the row command inputs R[9:0] and latched with the rising CK clock edge as shown in Figure 23. The command must be followed either by RNOP, PREpb or PREab on the falling CK clock edge of the same cycle. Note that PREpb and PREab commands in this case must be for the other pseudo channel and the timing requirements for issuing these commands must be met. The REFab command also requires a CNOP command on the column command inputs C[7:0] unless the column command is for the other pseudo channel.

Parity is evaluated with the REFRESH command when the parity calculation is enabled in the Mode Register.

![](images/d3f3c021488104bc5740651b828146297d146c929ca4196a5dbbc8676d11b54f.jpg)  
NOTE 1 PC = Pseudo Channel 0 or 1; V = Valid (H or L)  
Figure 23 — REFRESH All-bank Command (REFab)

The REFab command is nonpersistent, so it must be issued each time a refresh is required. A minimum time t<sub>RFCab</sub> is required between two REFab commands or a REFab command and any subsequent access command after the refresh operation. All banks must be precharged with t<sub>RP</sub> satisfied prior to the REFab command. The banks are in idle state after completion of the REFab command.

The refresh addressing is generated by an internal refresh controller. This makes the address bits “Don’t Care” during a REFab command.

## 6.3.2.5.1 REFRESH Command (REFab) (cont’d)

![](images/278974e58a8085b67d46f5b1a077e2effb6d52ed5b0b10bf73f8f2502b189ba8.jpg)  
NOTE 1 Only RNOP and CNOP commands are allowed after a REFRESH command until tRFCab has expired. NOTE 2 The maximum time interval between two REFRESH commands is $9 \times \operatorname { t } _ { \mathrm { R E F I } } .$  
Figure 24 — REFab Cycle

The HBM4 DRAM requires REFab cycles at an average periodic interval of $\mathbf { t } _ { \mathrm { R E F I } } ( \mathrm { M a x } . )$ . To allow for improved efficiency in scheduling and switching between tasks, some flexibility in the absolute refresh interval is provided. A maximum of eight REFab commands can be postponed during operation of the device, meaning that at no point in time more than a total of eight REFab commands are allowed to be postponed. In case that eight REFab commands are postponed in a row, the resulting maximum interval between the surrounding REFab commands is limited to $9 \times \mathrm { t _ { R E F I } }$ (see Figure 25). At any given time, a maximum of 9 REFab commands can be issued within t<sub>REFI</sub>.

This flexibility to postpone refresh commands also extends to REFpb commands (see REFpb). The maximum interval between refreshes to a particular bank is limited to 9 × t<sub>REFI</sub>. At any given time, a maximum of 9 REFpb commands to a particular bank can be issued within t<sub>REFI</sub>.

![](images/3d3e134e3ef1e395b953fde1d1a70c8e2cab1a823ea46a436f5a82ecdf867477.jpg)  
Figure 25 — Postponing Refresh Commands (Example)

Self refresh mode may be entered with a maximum of eight REFab commands being postponed. After exiting self refresh mode with one or more REFab commands postponed, additional REFab commands may be postponed to the extent that the total number of postponed REFab commands (before and after the self refresh) will never exceed eight. During self refresh mode, the number of postponed REFab commands does not change.

## 6.3.2.5.2 REFRESH per-bank Command (REFpb)

The REFRESH per-bank command (REFpb) provides an alternative solution for the refresh of the HBM4 device. The command initiates a refresh cycle on a single bank while accesses to other banks including writes and reads are not affected. REFpb is a half-cycle command received on the row command inputs R[9:0] and latched with the rising CK clock edge as shown in Figure 26. The command must be followed either by RNOP, PRECHARGE (PREpb) or PRECHARGE ALL (PREab) on the falling CK clock edge of the same cycle. Note that a PREab must be for the other pseudo channel. A PREpb command could be to any bank in the other pseudo channel as well as to a different bank in the same pseudo channel. In all cases the timing requirements for issuing these commands must be met.

Parity is evaluated with the REFpb command when the parity calculation is enabled in the Mode Register.

![](images/f2218af38866d76759b8708561733d084ff7293d30c908d60ecb38367b6b4c73.jpg)  
NOTE 1 BA = Bank Address; PC = Pseudo Channel 0 or 1; SID = Stack ID; V = Valid (H or L)  
Figure 26 — REFRESH per-bank Command (REFpb)

The REFpb command is nonpersistent, so it must be issued each time a refresh is required. A minimum time t<sub>RRD</sub> is required between an ACTIVATE command and a REFpb command to a different bank. A minimum time t is required between any two REFpb commands (see below for an exception requiring t ), and between a REFpb command and an ACTIVATE command to a different bank as shown in Figure 27. A minimum time t<sub>RFCpb</sub> is required between a REFpb command and an access command to the same bank that follows. The bank to be refreshed must be precharged with t<sub>RP</sub> satisfied prior to the REFpb command. The bank is in idle state after completion of the REFpb command.

NOTE 2 tRRD timing must be met between ACTIVATE commands and REFpb commands to different banks. NOTE 3 tRREFD timing must be met between consecutive REFpb commands to different banks, and between a REFpb command followed by an ACTIVATE command to the different bank. NOTE 4 tRFCpb timing must be met between a REFpb command followed by an ACTIVATE command to the same bank.

## 6.3.2.5.2 REFRESH per-bank Command (REFpb) (cont’d)

![](images/c365fe66b8bf1eb52ebc0f1ab23cd6356ba915fd63abb4cc66ab5e9ab15c7333.jpg)  
NOTE 1 BAn,x,y,z = bank address n,x,y,z; RAa,b,c = row address a,b,c.

Figure 27 — REFpb Command Cycle

The row address for each bank is provided by internal refresh counters. This makes the row address bits “Don’t Care” during REFpb commands.

Rules for issuing REFpb commands to the banks apply to each SID individually. A REFpb command to one of the 16 banks per SID can be issued in any order. After all banks within an SID have been refreshed using the REFpb command and after waiting for at least tRFCpb, the controller can issue another set of REFpb commands in the same or different order. However, it is illegal to send another REFpb command to a bank unless all banks within an SID have been refreshed using the REFpb command. The controller must track the bank being refreshed by the REFpb command.

A REFpb command and/or REFRESH MANAGEMENT command must not be issued during t<sub>RFCpb</sub> succeeding the last REFpb (REFpb #N) of a single cycle as shown in   
Figure 28.

The bank count is synchronized between the controller and the HBM4 DRAM by resetting the bank count to zero. Synchronization can occur upon exit from reset state or by issuing a REFab or SELF REFRESH ENTRY command. Both commands may be issued at any time even if a preceding sequence of REFpb commands has not completed cycling through all banks.

![](images/cb8612bb32f8eac4c6254c9ff274936b0b20a8df9a303034a09ed97c45fb4c8d.jpg)  
Figure 28 — Sets of REFpb Commands

## 6.3.2.5.2 REFRESH per-bank Command (REFpb) (cont’d)

The average rate of REFpb commands tREFIpb depends on the bank count N and can be calculated by the following formula:

$$
\mathbf { { t R E F I p b } } = \mathbf { { t R E F I } } / \mathbf { { N } }
$$

The example in Table 37 shows two full sets of REFpb commands with the bank counter reset to 0 and the refresh counter incremented after 16 REFpb commands each. The third set of REFpb commands is interrupted by the REFab command which resets the bank counter to 0 and performs refreshes to all banks indicated by the refresh counter.

Table 37 — Refresh Counter Increments (Example)
<table><tr><td rowspan=1 colspan=1>Count</td><td rowspan=1 colspan=1>Sub-Count</td><td rowspan=1 colspan=1>Command</td><td rowspan=1 colspan=1>Bank Address</td><td rowspan=1 colspan=1>RefreshBank</td><td rowspan=1 colspan=1>BankCounter</td><td rowspan=1 colspan=1>RefreshCounter</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=3>RESET n, REFab, or SELF REFRESH ENTRY command</td><td rowspan=1 colspan=1>To 0</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>000</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0 to 1</td><td rowspan=7 colspan=1>n</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>0001</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1 to 2</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>0010</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>2 to 3</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>0011</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>3 to 4</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=4>…</td></tr><tr><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>1110</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>14 to 15</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>1111</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>15 to 0</td></tr><tr><td rowspan=1 colspan=1>17</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>0100</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>0 to 1</td><td rowspan=7 colspan=1>n + 1</td></tr><tr><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>0111</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>1 to 2</td></tr><tr><td rowspan=1 colspan=1>19</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>1011</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>2 to 3</td></tr><tr><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>0110</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>3 to 4</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=5>…</td></tr><tr><td rowspan=1 colspan=1>31</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>1100</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>14 to 15</td></tr><tr><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>0001</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>15 to 0</td></tr><tr><td rowspan=1 colspan=1>33</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>0010</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>0 to 1</td><td rowspan=3 colspan=1>n+ 2</td></tr><tr><td rowspan=1 colspan=1>34</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>1001</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1 to 2</td></tr><tr><td rowspan=1 colspan=1>35</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>0000</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>2 to 3</td></tr><tr><td rowspan=1 colspan=1>36</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>REFab</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>all</td><td rowspan=1 colspan=1>To 0</td><td rowspan=1 colspan=1>n + 2</td></tr><tr><td rowspan=1 colspan=1>37</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>1010</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>0 to 1</td><td rowspan=2 colspan=1>n + 3</td></tr><tr><td rowspan=1 colspan=1>38</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>0101</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>1 to 2</td></tr><tr><td rowspan=1 colspan=7></td></tr></table>

## 6.3.2.5.2 REFRESH per-bank Command (REFpb) (cont’d)

Table 38 — REFab and REFpb Command Scheduling Requirements
<table><tr><td rowspan=1 colspan=1>From Command</td><td rowspan=1 colspan=1>To Command</td><td rowspan=1 colspan=1>Minimum Delay Between “FromCommand” to“To Command”</td><td rowspan=1 colspan=1>Note</td></tr><tr><td rowspan=5 colspan=1>REFab</td><td rowspan=1 colspan=1>REFab</td><td rowspan=1 colspan=1>tRFCab</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>REFpb (any bank)</td><td rowspan=1 colspan=1>tRFCab</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>REFab</td><td rowspan=1 colspan=1>tRFCab</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>RFMpb (any bank)</td><td rowspan=1 colspan=1>tRFCab</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>ACTIVATE</td><td rowspan=1 colspan=1>tRFCab</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=8 colspan=1>REFpb</td><td rowspan=1 colspan=1>REFab</td><td rowspan=1 colspan=1>tRFCpb</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>REFpb (different bank)</td><td rowspan=1 colspan=1>tRREFD</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>REFpb (any bank)</td><td rowspan=1 colspan=1>tRFCpb</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>RFMFab</td><td rowspan=1 colspan=1>tRFCpb</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>RFMpb (different bank)</td><td rowspan=1 colspan=1>tRREFD</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>RFMpb (any bank)</td><td rowspan=1 colspan=1>tRFCpb</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>ACTIVATE (same bank)</td><td rowspan=1 colspan=1>tRFCpb</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>ACTIVATE (different bank)</td><td rowspan=1 colspan=1>tRREFD</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=5 colspan=1>RFMab</td><td rowspan=1 colspan=1>REFab</td><td rowspan=1 colspan=1>tRFCab</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>REFpb (any bank)</td><td rowspan=1 colspan=1>tRFCab</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>RFMab</td><td rowspan=1 colspan=1>tRFCab</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>RFMpb (any bank)</td><td rowspan=1 colspan=1>tRFCab</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>ACTIVATE</td><td rowspan=1 colspan=1>tRFCab</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=8 colspan=1>RFMpb</td><td rowspan=1 colspan=1>REFab</td><td rowspan=1 colspan=1>tRFCpb</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>REFpb (same bank)</td><td rowspan=1 colspan=1>tRFCpb</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>REFpb (different bank)</td><td rowspan=1 colspan=1>tRREFD</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>RFMab</td><td rowspan=1 colspan=1>tRFCpb</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>RFMpb (same bank)A</td><td rowspan=1 colspan=1>tRFCpb</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>RFMpb (different bank)</td><td rowspan=1 colspan=1>tRREFD</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>ACTIVATE (same bank)</td><td rowspan=1 colspan=1>tRFCpb</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>ACTIVEATE (different bank)</td><td rowspan=1 colspan=1>tRREFD</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=6 colspan=1>ACTIVATE</td><td rowspan=1 colspan=1>REFab</td><td rowspan=1 colspan=1>tRC</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>REFpb (same bank)</td><td rowspan=1 colspan=1>tRC</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>REFpb (different bank)</td><td rowspan=1 colspan=1>tRRD</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>RFMab</td><td rowspan=1 colspan=1>tRC</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>RFMpb (same bank)</td><td rowspan=1 colspan=1>tRC</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>RFMpb (different bank)</td><td rowspan=1 colspan=1>tRRD</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=4>NOTE 1tFAw parameter must be observed as well.NOTE 2A bank must be in an idle state with tRP satisfied before it is refreshed.NOTE 3 tRFCpb parameter must be observed when the first REFpb command completes a set of 16 per-bank refreshoperations within an SID and the second REFpb command initiates the next set of 16 per-bank refresh operationswithin an SID.NOTE 4 tRFCpb parameter must be observed when the REFpb command completes a set of 16 per-bank refresh operationswithin an SID and the following RFMpb command operations.</td></tr></table>

![](images/8fc33a7a856817e985cb1a718d3be0e0f36352edeee9f06f98cd6e5e999bc199.jpg)

## 6.3.2.5.3 Refresh Management (RFM)

Periods of high DRAM activity may require additional refresh commands to protect the integrity of the stored data. The requirement for additional Refresh Management (RFM) is indicated in the RFM field of the DEVICE\_ID WDR (see Table 132): RFM = 0 indicates that no additional refresh is needed beyond the refreshes specified in the REFRESH clause of the standard; RFM = 1 indicates additional DRAM refresh management is required.

A suggested implementation of refresh management by the controller monitors ACTIVATE commands issued per bank to the device. This activity can be monitored as a rolling accumulated ACTIVATE (RAA) count. Each ACTIVATE command will increment the RAA count by 1 for the individual bank receiving the ACTIVATE command.

When the RAA count reaches a DRAM vendor specified Initial Management Threshold (RAAIMT), which is indicated by the HBM4 DRAM in the RAAIMT field of the DEVICE\_ID WDR (see Table 132), additional refresh management is needed. Executing a refresh management command allows additional time for the HBM4 DRAM to manage refresh internally. The RFM operation can be initiated to all banks with the REFRESH MANAGEMENT all-bank (RFMab) command, or to a single bank with the REFRESH MANAGEMENT per-bank (RFMpb) command.

The encoding of RFM related commands RFMab and RFMpb is shown in Figure 29. Both half-cycle commands are received on the R[9:0] inputs and latched with the rising CK clock edge. They must be followed either by RNOP, PREpb or PREab on the falling CK clock edge of the same cycle. Note that a PREab must be for the other pseudo channel. In case of a RFMpb command a PREpb command could be to any bank in the other pseudo channel as well as to a different bank in the same pseudo channel. In all cases the timing requirements for issuing these commands must be met.

An HBM4 DRAM not requiring refresh management will ignore RFMab and RFMpb commands and execute an RNOP command instead.

![](images/ec03028574088c5e82533df9fe3eae9cef7f415e97d92f6f8db636c5c2b5528e.jpg)  
NOTE 1 BA = Bank Address; PC = Pseudo Channel 0 or 1; SID = Stack ID; V = Valid (H or L)  
Figure 29 —RFMab and RFMpb Commands

## 6.3.2.5.3 Refresh Management (RFM) (cont’d)

The RFMab and RFMpb command scheduling shall meet the same minimum separation requirements as those for the REFab and REFpb commands, respectively (see Table 38). The RFMab command period is the same as the REFab command period (t<sub>RFCab</sub>), and the RFMpb command period is the same as the REFpb command period (t<sub>RFCpb</sub>). The requirement for REFpb commands to be issued to all banks in a rolling fashion does not apply to RFMpb commands.

A REFpb command and/or RFMpb command must not be issued during t<sub>RFCpb</sub> succeeding the last PER-BANK REFRESH (REFpb #N) of a single cycle as shown in Figure 27.

When an RFM command is issued to the HBM4 DRAM, the RAA counter in any bank receiving the command can be decremented by the RAAIMT value, down to a minimum RAA value of 0 (no negative or “pull-in” of RFM commands is allowed). Issuing an RFMab command allows the RAA count in all banks to be decremented by the RAAIMT value. Issuing an RFMpb command allows the RAA count only in the bank selected by {SID[1:0], BA[3:0]} to be decremented by the RAAIMT value.

RFM commands are allowed to accumulate or “postpone”, but the RAA counter shall never exceed a vendor specified RAA Maximum Management Threshold (RAAMMT), which is indicated by the HBM4 DRAM in the RAAMMT field of the DEVICE\_ID WDR (see Table 132). If the RAA counter reaches RAAMMT, no additional ACTIVATE commands are allowed to the bank until one or more REF or RFM commands have been issued to reduce the RAA counter below the maximum value.

An RFM command does not replace the requirement for the controller to issue periodic REF commands to the HBM4 DRAM, nor does an RFM command affect internal refresh counters. The RFM commands are bonus time for the HBM4 DRAM to manage refresh internally. However, issuing a REF command also allows decrementing the RAA counter by a value indicated the RAA\_CNT\_DEC field of the DEVICE\_ID WDR (see Table 132). Hence, any periodic REF command issued to the HBM4 DRAM allows the RAA counter of the banks being refreshed to be decremented by that value. Issuing a REFab command allows the RAA count in all banks to be decremented by that value. Issuing an REFpb command allows the RAA count only in the bank selected by {SID[1:0], BA[3:0]} to be decremented by that value.

The per-bank RAA count values may be reset to 0 when the HBM4 DRAM is held in self refresh for at least t<sub>RAASRF</sub> time. No decrement to the per-bank RAA count values is allowed for entering or exiting self refresh and when the HBM4 DRAM is held in self refresh for less than t time.

## 6.3.2.5.4 Adaptive Refresh Management (ARFM)

HBM4 DRAMs optionally support a refresh management mode called Adaptive Refresh Management (ARFM). The HBM4 DRAM indicates the support of ARFM via the ARFM bit in the IEEE1500 DEVICE\_ID WDR. Since RFM related parameters RAAIMT, RAAMMT and RAADEC are read-only, the ARFM mode allows the controller flexibility to choose additional (lower) RFM threshold settings called “RFM Levels”. The RFM levels permit alignment of the controller-issued RFM commands with the DRAM internal management of these commands. MR8 OP[5:4] select the RFM level as shown in Table 39.

Table 39 — Mode Register Definition for Adaptive RFM Levels
<table><tr><td rowspan=1 colspan=1>MR8OP[5:4]</td><td rowspan=1 colspan=1>RFMLevel</td><td rowspan=1 colspan=1>RFMRequirement</td><td rowspan=1 colspan=1>RAAIMT</td><td rowspan=1 colspan=1>RAAMMT</td><td rowspan=1 colspan=1>RAA Decrement perREF Command</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>Default</td><td rowspan=1 colspan=1>Default</td><td rowspan=1 colspan=1>RAAIMT</td><td rowspan=1 colspan=1>RAAMMT</td><td rowspan=1 colspan=1>RAADEC</td><td rowspan=4 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>01</td><td rowspan=1 colspan=1>Level A</td><td rowspan=1 colspan=1>RFM is required</td><td rowspan=1 colspan=1>RAAIMT_A</td><td rowspan=1 colspan=1>RAAMMT A</td><td rowspan=1 colspan=1>RAADEC_A</td></tr><tr><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>Level B</td><td rowspan=1 colspan=1>RFM is required</td><td rowspan=1 colspan=1>RAAIMT B</td><td rowspan=1 colspan=1>RAAMMT B</td><td rowspan=1 colspan=1>RAADEC B</td></tr><tr><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>Level C</td><td rowspan=1 colspan=1>RFM is required</td><td rowspan=1 colspan=1>RAAIMT_C</td><td rowspan=1 colspan=1>RAAMMT_C</td><td rowspan=1 colspan=1>RAADEC_C</td></tr><tr><td rowspan=1 colspan=7>NOTE 1RAAIMT, RAAMMT and RAADEC values are set by DRAM vendor in the IEEE1500 DEVICE_ID WDR.</td></tr></table>

The Adaptive RFM mode inherits the RAA counting and decrement attributes of the standard RFM mode, while using the alternate RAAIMT, RAAMMT and RAADEC values for the selected RFM level. Increasing the RFM level results in increased need for RFM commands. Level C is highest RFM level. The alternate RAAIMT, RAAMMT and RAADEC values for RFM level A to C can be retrieved from the corresponding fields of the IEEE1500 DEVICE\_ID WDR.

Setting the bits in MR8 OP[5:4] to something other than the default "00" will select one of the RFM levels A, B or C. The host shall decrement the Rolling Accumulated ACT (RAA) count to 0, either with RFM or pending REF commands, prior to making a change to the ARFM level.

It is required to set the same RFM level on all channels of the HBM4 DRAM.

Adaptive RFM also allows an HBM4 DRAM shipped with 'RFM not required' (RFM bit in IEEE1500, DEVICE\_ID WDR[128] = 0) to override that initial setting and enable RFM by programming a nondefault ARFM level. The HBM4 DRAM internally manages the change to treat the RFM command as an RFM command in this special override case as shown in Table 40.

## 6.3.2.5.4 Adaptive Refresh Management (ARFM) (cont’d)

Table 40 — RFM Commands Perceived by HBM4 DRAM
<table><tr><td rowspan=2 colspan=1>Command</td><td rowspan=1 colspan=2>Bit in DEVICE ID WDR</td><td rowspan=2 colspan=1>RFM LevelMR8 OP[5:4]</td><td rowspan=2 colspan=1>Command Perceivedby HBM4 DRAM</td><td rowspan=2 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>RFM</td><td rowspan=1 colspan=1>ARFM</td></tr><tr><td rowspan=7 colspan=1>RFMab /RFMpb</td><td rowspan=4 colspan=1>0(RFM not required)</td><td rowspan=2 colspan=1>0(ARFM not supported)</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>01, 10 or 11</td><td rowspan=1 colspan=1>Illegal</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=2 colspan=1>1 (ARFM supported)</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>01, 10 or 11</td><td rowspan=1 colspan=1>RFMab / RFMpb</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=3 colspan=1>1 (RFM required)</td><td rowspan=2 colspan=1>0(ARFM not supported)</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>RFMab / RFMpb</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>01, 10 or 11</td><td rowspan=1 colspan=1>Illegal</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>1 (ARFM supported)</td><td rowspan=1 colspan=1>00, 01, 10 or 11</td><td rowspan=1 colspan=1>RFMab / RFMpb</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=6>NOTE 1 These cases are marked as Illegal&#x27; because HBM4 DRAMs not supporting Adaptive RFM do not support theselection of an ARFM level via MR8 OP[5:4] and therefore define these bits as RFU which implies that the onlysupported setting for these bits is 00.NOTE 2 Adaptive RFM enables an HBM4 DRAM shipped with RFM = 0 (RFM not required) to override the initial settingand enable Adaptive RFM by programming a non-default RFM level.</td></tr></table>

## 6.3.2.5.5 Directed Refresh Management (DRFM)

Directed Refresh Management (DRFM) is a feature that gives the controller additional flexibility for maintaining data integrity within the HBM4 DRAM. The DRFM feature allows the device to capture a host-requested row address, which then is followed by a host-directed RFMpb command allowing the device to refresh physically adjacent neighboring rows of the requested row address. DRFM is disabled by default and can be enabled by setting the DRFM bit in MR0 OP3 to 1b.

HBM4 SDRAM only supports two ways to reset or clear out DRFM sampled addresses, issuing DRFMpb commands by hosts or device reset.

If DRFM is disabled by the host and then re-enabled using MR0 OP3, any sampled row address before disabling DRFM is not guaranteed to be serviced with a DRFMpb command (RFMpb) after DRFM is reenabled. Therefore, the host is required to re-sample any row address to ensure a DRFM address is serviced after disabling and then re-enabling DRFM.

When DRFM is enabled, executing an ACT command with the DRFM bit set to 1<sub>b</sub> will instruct the device to not only open the row but also capture the activated row address for DRFM as shown in Figure 30.

After the DRFM address capture, the host can issue an RFMpb command to the bank (referred to as DRFMpb command) to service the captured DRFM address. This DRFMpb command is supplemental to the device’s RFM requirements and does not allow RAA count to be decremented. A RFMpb command issued to a bank without a valid address sample will be executed as a regular RFMpb command.

![](images/559685f07bfa8930fe733f05147854d1c5246b4eee3642f87947a66478bed3a0.jpg)  
NOTE 1 PRE shown for illustration purposes.

Figure 30 — ACTIVATE with DRFM Bit

## 6.3.2.5.5 Directed Refresh Management (DRFM) (cont’d)

Each bank has an independent DRFM address register for the DRFM row address sample. This DRFM address register is updated with each DRFM address sample to the bank, resulting in the last (most recent) address sample being retained for the host directed DRFMpb command as shown in Figure 31.

![](images/ff605ef4c7af107d87b019b933db25d9f95284610ad8c6fd3b7962fe0241be9f.jpg)  
NOTE 1 PRE shown for illustration purposes.

Figure 31 — Multiple ACTIVATE with DRFM Bit to Same Bank before DRFM Command

## 6.3.2.5.5 Directed Refresh Management (DRFM) (cont’d)

Following a DRFMpb command, the DRFM address register for the bank that received the DRFMpb command will be cleared from further use.

Aside from the DRFMpb command, a chip reset is the only other way to clear DRFM sampled addresses. DRFM capture addresses will be retained during Self Refresh mode, requiring the host to resample prior to issuing a DRFMpb command if the address retained in a bank’s DRFM address register is no longer relevant. Additionally, no RAA credit is given to banks with DRFM sampled addresses, regardless of relevancy.

HBM4 also permits an ACTIVATE to an already open row with the DRFM flag set (DRFM=1) to capture the row. In this case the host must issue the subsequent ACTIVATE to the same row address in the opened bank and must issue the additional ACTIVATE command tRRDL cycles after the initial ACTIVATE command that opened the row.

The HBM4 DRAM will not open the bank as it is already open and simply capture the row address for DRFM. As the bank is already opened, the host may issue a RD/WR/RDA/WRA command without the need for tRCD between the ACTIVATE that only captures a DRFM row address and the RD/WR /RDA/WRA. The timing between an ACTIVATE that only captures a DRFM row address and a PREab/PREpb/WRA/RDA command to close the bank is tDRFM2PRE as shown in Figure 32.

![](images/86c6df9378c9d978c43a87fe48bc23900507313017c19d1612cbe1a1b131e02b.jpg)  
NOTE 1 PRE shown for illustration purposes. tDRFM2PRE applies to the second ACTIVATE to the PREab, PREpb, WRA or RDA.  
Figure 32 — ACTIVATE with DRFM Bit to Open Page (Same Bank and Row Address)

## 6.3.2.5.5 Directed Refresh Management (DRFM) (cont’d)

Any additional ACTIVATE with DRFM flag set to a different row address in the opened bank is illegal. If the initial ACTIVATE command opened the bank and captured the row address for DRFM, then a subsequent ACTIVATE with DRFM flag set to the same bank and row address while the bank is opened will capture the address again and tDRFM2PRE must be met form the most recent ACTIVATE and not the initial ACTIVATE that captured the DRFM row addresses. tRAS is referenced from the ACTIVATE that opens the bank and is not referenced from any ACTIVATE that only captures the DRFM row address.

Table 41 is the timings associated with DRFM row address capture.

Table 41 — Command to Command Timings with DRFM Enabled
<table><tr><td rowspan=1 colspan=1>From Command</td><td rowspan=1 colspan=1>To Command</td><td rowspan=1 colspan=1>min. Delay Between“From Command” to“ToCommand”</td><td rowspan=1 colspan=1>Note</td></tr><tr><td rowspan=1 colspan=1>ACTIVATE (bank closed ,DRFM=0 or 1)</td><td rowspan=1 colspan=1>ACTIVATE (same bank, samerow address, DRFM=1)</td><td rowspan=1 colspan=1>tRRDL</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>REFpb</td><td rowspan=1 colspan=1>ACTIVATE (different bank,bank already open, DRFM=1)</td><td rowspan=1 colspan=1>tRREFD</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>RFMpb</td><td rowspan=1 colspan=1>ACTIVATE (different bank,bank already open, DRFM=1)</td><td rowspan=1 colspan=1>tRREFD</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=11 colspan=1>ACTIVATE (bank alreadyopen, DRFM=1)</td><td rowspan=1 colspan=1>REFab一</td><td rowspan=1 colspan=1>tDRFM2PRE+tRP</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>REFab (same bank)</td><td rowspan=1 colspan=1>tDRFM2PRE+tRP</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>REFpb (different bank)</td><td rowspan=1 colspan=1>tRRDS</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>RFMab</td><td rowspan=1 colspan=1>tDRFM2PRE+tRP</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>RFMpb (same bank)</td><td rowspan=1 colspan=1>tDRFM2PRE+tRP</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>RFMpb (different bank)</td><td rowspan=1 colspan=1>tRRDS</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>PREab</td><td rowspan=1 colspan=1>tDRFM2PRE</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>PREpb (same bank)</td><td rowspan=1 colspan=1>tDRFM2PRE</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>RD or WR (same bank)</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>RD or WR w/ AP (same bank)</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>3,4</td></tr><tr><td rowspan=1 colspan=1>ACTIVATE (different bank,DRFM=0 or 1)</td><td rowspan=1 colspan=1>tRRDS</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=4>NOTE 1 The ACTIVATE (same bank, DRFM=1) to capture the DRFM address is not counted as a part of tFAW.NOTE 2 The bank or all banks must be closed between the ACTIVATE (bank already open, DRFM=1) and the REFab,REFpb (same bank), RFMab, and RFMpb (same bank).NOTE 3 The Read or Write must meet tRCD from the ACTIVATE that opens the bank.NOTE 4 Read and Write with Auto Precharge must meet tDRFM2PRE as illustrated in Figure 32.</td></tr></table>

The DRFMpb command scheduling shall meet the same minimum separation requirements, like tRP, tRRD, or tRREFD as for a RFMpb command (see Refresh Management (RFM) clause). On average, any row/bank address combination is allowed to be sampled once per DRFM command interval, tDRFMI. tDRFMI is 2 × tREFI, resulting in no more than TBD DRFM commands to the same row/bank address combination within tREF.

## 6.3.2.5.5.1 Bounded Refresh Configuration

The DRFMpb command refreshes physically adjacent neighboring rows to the DRFM sampled address, up to the distance specified by the Bounded Refresh Configuration (BRC) as defined by MR8 OP[7:6]. The HBM4 DRAM is responsible for applying a refresh ratio to the outermost rows being refreshed to protect the HBM4 DRAM from excessive refreshes on rows adjacent to the outermost rows.

For example, BRC2 will always refresh the +1 physically adjacent neighboring rows, and the ±2 physically adjacent neighboring rows may be refreshed at a reduced rate as determined by the HBM4 DRAM. Likewise, if BRC4 is programmed, the HBM4 DRAM will always refresh the ±1, ±2 and ± 3 physically adjacent neighboring rows, while applying a ratio to ±4 physically adjacent neighboring rows. The support of BRC3 and BRC4 is optional and indicated in Device ID (Table 132).

The DRFM cycle time per row is tRRF = 60ns. The corresponding DRFMpb command duration tDRFM is determined by the selected BRC option and given as tDRFM = 2 × tRRF × BRC as summarized in Table 42.

Table 42 — Bounded Refresh Configuration and tDRFM Timings
<table><tr><td rowspan=1 colspan=1>BRC</td><td rowspan=1 colspan=1>MR8 OP[7:6]</td><td rowspan=1 colspan=1>Rows RefreshedM</td><td rowspan=1 colspan=1>tDRFM</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>Always ±1, Ratio ±2</td><td rowspan=1 colspan=1>4×tRRF</td></tr><tr><td rowspan=1 colspan=1>3 (Optional)</td><td rowspan=1 colspan=1>01</td><td rowspan=1 colspan=1>Always ±1, ±2, Ratio ±3</td><td rowspan=1 colspan=1>6×tRRF</td></tr><tr><td rowspan=1 colspan=1>4 (Optional)</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>Always ±1, ±2, ±3, Ratio ±4</td><td rowspan=1 colspan=1>8×tRRF</td></tr><tr><td rowspan=1 colspan=1>RFU</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>G         RFU</td><td rowspan=1 colspan=1>RFU</td></tr></table>

## 6.3.3 Column Commands

The column commands consist of CNOP, Read, Read with Auto Precharge, Write, Write with Auto Precharge, MRS. The column commands utilize C[7:0] inputs. All column commands are transmitted in a single clock cycle.

## 6.3.3.1 Column No Operation (CNOP)

The COLUMN NO OPERATION (CNOP) command is a 1-cycle command as shown in Figure 33 and is used to instruct the HBM4 DRAM to perform a NOP as the column command; this prevents unwanted column commands from being registered during idle or wait states. Operations already in progress are not affected.

Parity is evaluated with the CNOP command when the parity calculation is enabled in the Mode Register.

CNOP is assumed for the C[7:0] inputs on subsequent timing diagrams unless other column commands are explicitly shown.

![](images/cfe2675d59d1d2b81437ea6a03abeb79df25914fa0b3e15cb97189f9f47849a0.jpg)  
V = Valid (H or L)  
Don't Care

Figure 33 — CNOP Command

## 6.3.3.2 Read Command (RD, RDA)

A read burst is initiated with a READ command; READ is a one-cycle command received on the column command inputs C[7:0] and latched with the rising and falling CK clock edges as shown in Figure 34. The bank, PC, SID and column addresses are provided with the READ command and auto precharge is either enabled or disabled for that access.

Parity is evaluated with the READ command when CA parity is enabled in the Mode Register.

![](images/e17991c08d54ebe03c6ded0852942a9d7b1f640a5e7756681c46ea48d9934e56.jpg)  
NOTE 1 BA = Bank Address; CA = Column Address; SID = Stack ID; PC = Pseudo Channel 0 or 1; NOTE 2 EN AP = Enable Auto Precharge; DIS AP = Disable Auto Precharge

## Figure 34 — READ Command

The length of the burst initiated with a READ command is eight. The column address is unique for the burst eight. There is no interruption nor truncation of read bursts.

The read latency (RL) is defined from the rising CK edge on which the READ command is issued to the rising CK edge from which the t delay is measured, and the RL field of MR2 OP[7:0] (see Table 12). The first valid data is available RL × t + t + t + t after the rising CK edge when the READ command was issued.

The write strobe (WDQS) is the source to trigger read data (DQ, DBI, ECC, SEV) and the read data strobe. The output drivers are enabled and begin driving either HIGH or LOW nominally two RDQS pulses (odd bytes) or one RDQS pulses (even bytes) prior to the first valid data bit. Bus pre-condition is Low regardless of RDBI enabled and disabled modes on a first READ command.

The output drivers will drive Hi-Z nominally one-half of RDQS pulse or less after the completion of the burst provided no other READ command has been issued.

## 6.3.3.2 Read Command (RD, RDA) (cont’d)

The write data strobe should be provided with a fixed four-pulse preamble and fixed two-pulse postamble before the read data strobe starts to toggle because RDQS is generated from WDQS. The first WDQS edge occurs $( \mathrm { R L } - 2 ) \times \mathrm { t c } \mathrm { + t } _ { \mathrm { D Q S S } }$ . The read data strobe provides a fixed two-pulse preamble and fixed two-pulse postamble; the first RDQS edge occurs $( \mathrm { R L } - 1 ) \times \mathrm { t c } \mathrm { { K } + \mathrm { t D } \mathrm { { Q } \mathrm { { s } \mathrm { { s } } + } } }$ t<sub>WDQS2DQ\_O</sub> after the rising CK edge when the READ command was issued. The first data bit of the read burst is synchronized with the third rising edge of the RDQS strobe. Each subsequent data-out is edge-aligned with the data strobe. Timings for the data strobe are measured relative to the crosspoint of RDQS\_t and its complement, RDQS\_c.

## 6.3.3.2.1 Clock to Write Data Strobe Timings

The Write Data Strobe(WDQS) to Clock(CK) relationship is shown in Figure 35. Related parameters:

<sup></sup> t<sub>DQSS</sub>(min/max) describes the allowed range for rising or falling WDQS edge relative to CK.

<sup></sup> t<sub>DQSS</sub> is the actual position of a WDQS edge relative to CK.

<sup></sup> t<sub>WQSH</sub> describes the WDQS HIGH pulse width

<sup></sup> t<sub>WQSL</sub> describes the WDQS LOW pulse width

## 6.3.3.2.2 Write Data Strobe and Data Out Timings

The Write Data Strobe to Read Data Strobe (RDQS) relationship is shown in Figure 35. Related parameters:

t<sub>WDQS2DQ\_O</sub>(min/max) describes the allowed range for a rising or falling RDQS edge relative to WDQS.

<sup></sup> t<sub>WDQS2DQ\_O</sub> is the actual position of a RDQS edge relative to WDQS.

<sup></sup> t<sub>QSH</sub> describes the RDQS HIGH pulse width.

<sup></sup> t<sub>QSL</sub> describes the RDQS LOW pulse width.

t<sub>LZ</sub>(min/max) describe the allowed range for the data output Hi-Z to low impedance transition relative to WDQS.

t<sub>HZ</sub>(min/max) describe the allowed range for the data output low impedance to Hi-Z transition relative to WDQS.

## 6.3.3.2.3 Read Data Strobe and Data Out Timings

The Read Data Strobe (RDQS) to Data Out (DQ, ECC, SEV, DBI) relationship is shown in Figure 35. Related parameters:

<sup></sup> tDQSQ describes the latest valid transition of any associated DQ or ECC or SEV or DBI pin for both rising and falling RDQS edges.

tQH describes the earliest invalid transition of any associated DQ or ECC or SEV or DBI pin for both rising and falling RDQS edges.

<sup></sup> tQW describes the valid data output window of any associated DQ or ECC or SEV or DBI pin for both rising and falling RDQS edges.

<sup></sup> tDQ2DQ describes Read DQ to DQ skew of any associated DQ or ECC or SEV or DBI pin for both rising and falling RDQS edges.

6.3.3.2.3 Read Data Strobe and Data Out Timings (cont’d)  
![](images/bd5093770427e19a791fafe93ef6d656c3320094083386ded84e5f4eed450828.jpg)  
NOTE 1 tWDQS2DQ\_O may span multiple clock periods.  
NOTE 2 A burst length of 8 is shown.  
NOTE 3 Early/late data transition of a DQ or SEV or ECC or DBI can vary within a burst.  
NOTE 4 Da...a+7 = data-out for READ command a.  
D = last data-out from previous READ command (not if first READ after reset, MRS, self refresh or write-to-read).  
NOTE 5 tWPRE2 = Read preamble for WDQS, tWPST2 = Read postamble for WDQS  
NOTE 6 tRPRE = Read preamble for RDQS, tRPST = Read postamble for RDQS

Figure 35 — Clock to RDQS and Data Out Timings

## 6.3.3.2.4 Read Operation

Single read bursts are shown in Figure 36 for BL=8.

![](images/702c7e87321339266a7c00b1edd684461739b4a0257c6dbb9e15ac67cf621e93.jpg)  
NOTE 1 BAx = bank address x; CAa = column address a.  
NOTE 2 RL = 6 is shown as an example.  
NOTE 3 DATA = DQ[31:0]. DBI[3:0], ECC[1:0]. SEV[1:0] for P C0, and DQ[63:32], DBI[7:4],ECC[3:2]. SEV[3:2] for PC1. WDQS\_t/\_c is ${ \mathrm { W D Q S 0 } } .$ $\underline { { \boldsymbol { \mathsf { t } } } } / \underline { { \boldsymbol { \mathsf { c } } } }$ for PC0, and WDQS1\_t/\_c for PC1. RDQS\_t/\_c is RDQS0 $\underline { { \boldsymbol { \mathsf { t } } } } / \underline { { \boldsymbol { \mathsf { c } } } }$ for PC0, and RDQS1 $\underline { { \boldsymbol { \mathsf { t } } } } / \underline { { \boldsymbol { \mathsf { c } } } }$ for PC1.  
NOTE 4 Da...a+7 = data-out for READ command a.  
D = last data-out from previous READ command (not if first REA D after reset, MRS, self refresh or write-to-read). NOTE 5 tWDQS2DQ ${ \underline { { \mathbf { \Pi } } } } _ { 0 } = 0$ and nominal tQW is shown for illustration purposes.  
NOTE 6 RDBI could be on or off and is controlled with MR0 OP0.

Figure 36 — Single Read Burst with $\mathbf { B L } = \mathbf { 8 }$

## 6.3.3.2.4 Read Operation (cont’d)

Data from any read burst may be concatenated with data from a subsequent READ command. A continuous flow of data can be maintained as shown in Figure 37. The first data element from the new burst follows the last element of a completed burst. The new READ command should be issued after the previous READ command according to the t<sub>CCD</sub> timing. If that READ command is to another idle bank then an ACTIVATE command must precede the READ command and t<sub>RCDRD</sub> also must be met.

![](images/4073c6fcda9fa4c0af81d7d3feaa3a6ee50ef4cb57103631568b9670835f9642.jpg)  
NOTE 1 BAx = bank address x; CAa,b = column address a,b.  
NOTE 2 RL = 6 is shown as an example.  
NOTE 3 DATA = DQ[31:0]. DBI[3:0], ECC[1:0]. SEV[1:0] for PC0, and DQ[63:32], DBI[7:4],ECC[3:2]. SEV[3:2] for PC1. WDQS\_t/\_c is WDQS0\_t/\_c for PC0, and WDQS1\_t/\_c for PC1. RDQS\_t/\_c is RDQS0\_t/\_c for PC0, and RDQS1\_t/\_c for PC1.  
NOTE 4 Da,Da+1..Da+7,Db,Db+1..Db+7 = output data for READ commands a,b.  
D = last data-out from previous READ command (not if first READ after reset, MRS, self refresh or write-to-read). NOTE 5 tWDQS2DQ\_O = 0 and nominal tQW is shown for illustration purposes. NOTE 6 RDBI could be on or off and is controlled with MR0 OP0.

Figure 37 — Seamless Read Bursts with BL = 8

## 6.3.3.2.4 Read Operation (cont’d)

Examples of non-seamless read bursts are shown in Figure 38 for $\mathrm { t } _ { \mathrm { C C D } } = 3$ and Figure 39 for $\mathrm { t _ { C C D } } = 4$ . The RDQS pulse at clock edge T8 in Figure 38 represents the read postamble of the first read burst as well as the read preamble of the second read burst. The chosen t<sub>CCD</sub> value leads to a continuous series of RDQS pulses over both read bursts, and the data bus does not return to Hi-Z between the read bursts (for odd bytes), and the last data out of the first read burst (Da + 7) is re-driven at the RDQS at clock edge $\mathrm { T } 8 + \mathbf { a }$ half (for even bytes) preceding the second read burst.

With $\mathrm { t _ { C C D } } = 4$ as shown in Figure 39 the timing of each of the two read bursts is identical to a single read burst as shown in Figure 36. The data bus returns to Hi-Z between the read bursts, and the last data out of the first read burst $( \mathrm { D a } + 7 )$ is re-driven at the RDQS pulse at clock edge T9 (for odd bytes) and $\mathrm { T } 9 + \mathbf { a }$ half (for even bytes) preceding the second read burst.

![](images/6ad1f88d1641d3729f3aba058987fe730bc0133f8e4349532b047309332b7bb6.jpg)  
NOTE 1 BAx = bank address x; CAa,b = column address a,b.  
NOTE 2 RL = 6, tCCD = 3 are shown as an example.  
NOTE 3 DATA = DQ[31:0]. DBI[3:0], ECC[1:0]. SEV[1:0] for P C0, and DQ[63:32], DBI[7:4],ECC[3:2]. SEV[3:2] for P C1. WDQS\_t/\_c is WDQS0\_t/\_c for PC0, and WDQS1\_t/\_c for PC1. RDQS\_t/\_c is RDQS0\_t/\_c for PC0, and RDQS1\_t/\_c for PC1.  
NOTE 4 Da,Da+1..Da+7,Db,Db+1..Db+7 = output data for READ commands a,b.  
NOTE 5 tWDQS2DQ\_O = 0 and nominal tQW is shown for illustration purposes.  
NOTE 6 RDBI could be on or off and is controlled with MR0 OP0.

Figure 38 — Non-Seamless Read Bursts with $\mathbf { t } _ { \mathrm { C C D } } = 3$ and $\mathbf { B L } = \mathbf { 8 }$

## 6.3.3.2.4 Read Operation (cont’d)

![](images/92b6783d23878a94a277802eff12af21d904f642843418d9c4e51821d18bd9ed.jpg)  
NOTE 1 BAx = bank address x; CAa,b = column address a,b.  
NOTE 2 RL = 6, tCCD =4 are shown as an example.  
NOTE 3 DATA = DQ[31:0]. DBI[3:0], ECC[1:0]. SEV[1:0] for PC0, and DQ[63:32], DBI[7:4],ECC[3:2]. SEV[3:2] for PC1. WDQS\_t/\_c is WDQS0\_t/\_c for PC0, and WDQS1\_t/\_c for PC1. RDQS\_t/\_c is RDQS0\_t/\_c for PC0, and RDQS1\_t/\_c for PC1.  
NOTE 4 Da,Da+1..Da+7,Db,Db+1..Db+7 = output data for READ commands a,b.  
NOTE 5 tWDQS2DQ\_O = 0 and nominal tQW is shown for illustration purposes.  
D = last data-out from previous READ command (not if first READ after reset, MRS, self refresh or write-to-read).  
NOTE 6 RDBI could be on or off and is controlled with MR0 OP0.

Figure 39 — Non-Seamless Read Burst with $\mathbf { t } _ { \mathbf { C C D } } = 4$ and $\mathbf { B L } = \mathbf { 8 }$

## 6.3.3.2.4 Read Operation (cont’d)

A WRITE can be issued any time after a READ command as long as the bus turnaround time $\mathrm { \bf t _ { \mathrm { R T W } } }$ is met as shown in Figure 40. If that WRITE command is to another idle bank, then an ACTIVATE command must precede the WRITE command and t<sub>RCDWR</sub> also must be met.

![](images/58f22891065e406082fce01cf933e231cec88ff3c4aa0ff3f520a04d6a9a06d4.jpg)  
Don't Care  
NOTE 1 BAx = bank address x; CAa = column address a.  
NOTE 2 RL=6 and WL=5 are shown as examples.  
NOTE 3 DATA = DQ[31:0]. DBI[3:0], ECC[1:0]. SEV[1:0] for PC0, and DQ[63:32], DBI[7:4],ECC[3:2]. SEV[3:2] for PC1. WDQS\_t/\_c is WDQS0\_t/\_c for PC0, and WDQS1\_t/\_c for PC1. RDQS\_t/\_c is RDQS0\_t/\_c for PC0, and RDQS1\_t/\_c for PC1.  
NOTE 4 Da...a+7 = data-out for READ command a.  
D = last data-out from previous READ command (not if first READ after re set, MRS, self refresh or write-to-read). NOTE 5 Db...b+7 = data-in for WRITE command b.  
NOTE 6 tWDQS2DQ\_O = 0 and nominal tQW is shown for illustration purposes.  
NOTE 7 tRTW is not a device limit but determined by the system bus turnaround time.  
NOTE 8 RDBI and WDBI could be on or off. RDBI is controlled with MR0 OP0, and WDBI is controlled with MR0 OP1.

Figure 40 — Read to Write

## 6.3.3.2.4 Read Operation (cont’d)

A PRECHARGE can be issued $\mathbf { t } _ { \mathrm { R T P } }$ after the READ command as shown in Figure 41. After the PRECHARGE command, a subsequent ACTIVATE command to the same bank cannot be issued until $\mathbf { t } _ { \mathrm { R P } }$ is met.

![](images/4c831e1d2150a305076b2ac5cb4edc4fb5fe7615208782d55fa0edd0c0cf3d20.jpg)  
NOTE 1 BAx = bank address x; CAa = column address a.  
NOTE 2 RL = 6 is shown as an example.  
NOTE 3 DATA = DQ[31:0]. DBI[3:0], ECC[1:0]. SEV[1:0] for P C0, and DQ[63:32], DBI[7:4],ECC[3:2]. SEV[3:2] for PC1. WDQS\_t/\_c is WDQS0\_t/\_c for PC0, and WDQS1\_t/\_c for PC1. RDQS\_t/\_c is RDQS0\_t/\_c for PC0, and RDQS1\_t/\_c for PC1.  
NOTE 4 Da...a+7 = data-out for READ command a.  
D = last data-out from previous READ command (not if first READ after reset, MRS, self refresh or write-to-read). NOTE 5 tWDQS2DQ\_O = 0 and nominal tQW is shown for illustration purposes.  
NOTE 6 $\mathrm { t R T P } = 1$ nCK is shown as an example. tRTP = tRTPL when the PRECHARGE command accesses the same bank; otherwise tRTP = tRTPS.  
NOTE 7 RDBI could be on or off and is controlled with MR0 OP0.

Figure 41 — Read to Precharge

## 6.3.3.2.5 Per-Signal-Group for Read De-Skew

The internal WDQS clock tree is optimized for lowest signal skew among signals within a group as outlined in Table 43. The grouping is aligned with the physical location of signals in a DWORD (see HBM4 Bump Map) with no lane being repaired.

Each group contains 6 to 8 signals. The internal WDQS clock tree, however, compensates the different loading by e.g., adding dummy loads. The per-group de-skew is also deterministic and not frequency dependent. A larger signal skew should be expected between different groups. A per-group de-skew is recommended to achieve the largest signaling margin for read data.

In this context, RDQS\_t and RDQS\_c are treated as regular out signals within group T4.

Table 43 — Signal Groups for Read Data De-Skew
<table><tr><td rowspan=1 colspan=1>Group</td><td rowspan=1 colspan=1>Signal List (DWORD0)</td><td rowspan=1 colspan=1>Signal List (DWORD1)</td></tr><tr><td rowspan=1 colspan=1>T0</td><td rowspan=1 colspan=1>DQ0, DQ1, DQ2, DQ8, DQ9, DQ10,ECC0, ECC1</td><td rowspan=1 colspan=1>DQ32, DQ33, DQ34, DQ40, DQ41,DQ42, ECC2, ECC3</td></tr><tr><td rowspan=1 colspan=1>T1</td><td rowspan=1 colspan=1>DQ3, DQ4, DQ11, DQ12, RD0, DPAR0</td><td rowspan=1 colspan=1>DQ35, DQ36, DQ43, DQ44, RD2,DPAR1</td></tr><tr><td rowspan=1 colspan=1>T2</td><td rowspan=1 colspan=1>DQ5, DQ6, DQ7, DQ13, DQ14, DQ15,DBI0, DBI1</td><td rowspan=1 colspan=1>DQ37, DQ38, DQ39, DQ45, DQ46,DQ47, DBI4, DBI5</td></tr><tr><td rowspan=1 colspan=1>T3</td><td rowspan=1 colspan=1>DQ16, DQ17, DQ18, DQ24, DQ25,DQ26, SEV0, SEV1                  1</td><td rowspan=1 colspan=1>DQ48, DQ49, DQ50, DQ56, DQ57,DQ58, SEV2, SEV3</td></tr><tr><td rowspan=1 colspan=1>T4</td><td rowspan=1 colspan=1>RDQS0_t, RDQS0_c</td><td rowspan=1 colspan=1>DQ51, DQ52, DQ59, DQ60, RD3,RDQS1_t, RDQS1_c</td></tr><tr><td rowspan=1 colspan=1>T5</td><td rowspan=1 colspan=1>DQ21, DQ22, DQ23, DQ29, DQ30,DQ31, DBI2, DBI3</td><td rowspan=1 colspan=1>DQ53, DQ54, DQ55, DQ61, DQ62,DQ63, DBI6, DBI7</td></tr></table>

## 6.3.3.3 Write Command (WR, WRA)

A Write burst is initiated with a WRITE command. WRITE is a one-cycle command received on the column command inputs C[7:0] and latched with the rising and falling CK clock edges as shown in Figure 42. The bank, PC, SID and column addresses are provided with the WRITE command and auto precharge is either enabled or disabled for that access.

Parity is evaluated with the WRITE command when CA parity is enabled in MR0 OP5 (Table 10).

![](images/fc50e3b0da555620caa009ae4144751899d512a40d225acd6f212862aeafdafe.jpg)  
NOTE 1 BA = Bank Address; CA = Column Address; SID = Stack ID; PC = Pseudo Channel 0 or 1; NOTE 2 EN AP = Enable Auto Precharge; DIS AP = Disable Auto Precharge

## Figure 42 — Write Command

The length of the burst initiated with a WRITE command is eight. The column address is unique for this burst of eight. There is no interruption nor truncation of write bursts.

The write latency (WL) is defined from the rising CK edge on which the WRITE command is issued to the rising CK edge from which the t delay is measured, and the WL field of MR1 OP[4:0]. The first valid data must be driven $\mathrm { W L } \times \mathrm { t _ { C K } } + \mathrm { t _ { D Q S S } }$ after the rising CK edge when the WRITE command was issued.

The write data strobe provides a fixed two-pulse preamble and two-pulse postamble; the first WDQS edge must be driven $\mathrm { ( W L - 1 ) } \times \mathrm { t _ { C K } } + \mathrm { t _ { D Q S S } }$ after the rising CK edge when the WRITE command was issued.

The HBM4 uses an un-matched WDQS-DQ path, so WDQS must stay within t<sub>DQSS</sub> and the DQ can be trained to stay center aligned to the WDQS with satisfying t<sub>DIVW</sub>. The DQ-data must be held for t<sub>DIVW</sub> (data input valid window) and the WDQS can be periodically trained to stay center aligned to DQ in the t<sub>DIVW</sub> window to compensate for timing changes due to temperature and voltage variation. Burst data is captured by the HBM on successive edges of WDQS until the burst length is complete. Pin timings for the data strobe are measured relative to the crosspoint of WDQS\_t and its complement, WDQS\_c.

## 6.3.3.3.1 Clock to Write Data Strobe Timings

The clock to write data strobe (WDQS) relationship is shown in Figure 43. Related parameters:

<sup></sup> t<sub>DQSS</sub>(min/max) describes the allowed range for a rising or falling WDQS edge relative to CK.

<sup></sup> t<sub>DQSS</sub> is the actual position of a WDQS edge relative to CK.

<sup></sup> t<sub>WQSH</sub> describes the WDQS HIGH pulse width.

<sup></sup> t<sub>WQSL</sub> describes the WDQS LOW pulse width.

## 6.3.3.3.2 Write Data Strobe and Data In Timings

The write data strobe (WDQS) to data in relationship is shown in Figure 43. Related parameters:

<sup></sup> t<sub>WDQS2DQ\_I</sub> describes the allowed range for a DQ to a rising or falling WDQS edge.

<sup></sup> t<sub>DIVW</sub> describes allowed range for receiver minimum setup/hold time for sampling at DQ.

<sup></sup> V<sub>DIVW</sub> describes allowed range for receiver voltage peak to peak size.

![](images/760bafbb155e521e79c83399c2c70cf6559ad9e139781a398535d21f95c15aa6.jpg)  
NOTE 4 tWPST1 = Write postamble for WDQS

Figure 43 — Clock to WDQS and Data Input Timings

## 6.3.3.3.3 Write Operation

Single write bursts are shown in Figure 44.

![](images/f91ce4aa02854818e7cd2efbe42fa2e83a20dd73dd396906f378f1e11a530188.jpg)  
NOTE 1 BAx = bank address x; CAa = column address a.  
NOTE 2 WL = 4 is shown as an example.  
NOTE 3 DATA = DQ[31:0]. DBI[3:0], ECC[1:0] for PC0, and DQ[63:32], DBI[7:4],ECC[3:2] for PC1. DPAR = DPAR 0 for PC0 and DPAR1 for PC1 (if applicable). WDQS\_t/\_c is WDQS0\_t/\_c for PC0, and WDQS1\_t/\_c for PC1.  
NOTE 4 Da...Da+7 = data-in for WRITE command a.  
NOTE 5 tDQSS = 0 is shown for illustration purposes.  
NOTE 6 WDBI could be on or off and is controlled with MR0 OP1.

Figure 44 — Single Write Burst with BL=8

## 6.3.3.3.3 Write Operation (cont’d)

Data from any write burst may be concatenated with data from a subsequent WRITE command. A continuous flow of data can be maintained as shown in Figure 45. The first data element from the new burst follows the last element of a completed burst. The new WRITE command should be issued after the previous WRITE command according to the t<sub>CCD</sub> timing. If that WRITE command is to another idle bank then an ACTIVE command must precede the WRITE command and t<sub>RCDWR</sub> also must be met.

![](images/615f5e4b8be7bb71b68bdbd93696505b95f101c9e596ee0171e271d5d316909a.jpg)  
NOTE 1 BAx = bank address x; CAa = column address a.  
NOTE 2 WL = 4 is shown as an example.  
NOTE 3 tCCD = tCCDS when the second WRITE is to a different bank group, otherwise tCCD=tCCDL.  
NOTE 4 DATA = DQ[31:0], DBI[3:0], ECC[1:0] for PC0 and DQ[63:32], DBI[7:4], ECC[3:2] for PC1.  
DPAR = DPAR0 for PC0 and DPAR1 for PC1 (if applicable).  
WDQS\_t/\_c is WDQS0\_t/\_c for PC0 and WDQS1\_t/\_c for PC1.  
NOTE 5 Da...Da+7 = data-in for WRITE command a, Db...Db+7 = data-in for WRITE command b.  
NOTE 6 tDQSS = 0 And tCCDS = 2 are shown for illustration purposes.  
NOTE 7 WDBI could be on or off and is controlled with MR0 OP1.

Figure 45 — Seamless Write Bursts with BL=8

## 6.3.3.3.3 Write Operation (cont’d)

Examples of non-seamless write bursts are shown in Figure 46.

![](images/96c70ae80f59906992b6fe2e96ac75594297d3fb288d148b1420749e380784e0.jpg)  
Don't Care  
NOTE 1 BAx = bank address x; CAa = column address a.  
NOTE 2 WL = 4 is shown as an example.  
WDQS\_t/\_c is WDQS0\_t/\_c for PC0, and WDQS1\_t/\_c for PC1.  
NOTE 4 DATA = DQ[31:0], DBI[3:0], ECC[1:0] for PC0 and DQ[63:32], DBI[7:4], ECC[3:2] for PC1.  
NOTE 3 tCCD = tCCDS when the second WRITE is to a different bank group, otherwise tCCD=tCCDL.  
NOTE 5 Da...Da+7 = data-in for WRITE command a, Db...Db+7 = data-in for WRITE command b.  
NOTE 6 tDQSS = 0 And tCCDS = 3 are shown for illustration purposes.  
NOTE 7 WDBI could be on or off and is controlled with MR0 OP1.

Figure 46 — Non-seamless Write Bursts

DPAR = DPAR0 for PC0 and DPAR1 for PC1 (if applicable).

## 6.3.3.3.3 Write Operation (cont’d)

A READ can be issued any time after a WRITE command as long as the bus turnaround time $\mathrm { \Delta t w T R }$ is met as shown in Figure 47. If that READ command is to another idle bank, then an ACTIVATE command must precede the READ command and t<sub>RCDRD</sub> also must be met. The bus is preconditioned for the first read burst by being driven LOW two RDQS pulses (Odd bytes) and one RDQS pulse (Even bytes) prior to the first valid data element of the read burst regardless whether RDBI is enabled in MR0 OP0 or not.

![](images/d037ec874864c1bf4b9e666c833f46fff1bdbfffa5e45eca25de648754f615df.jpg)  
NOTE 1 BAx = bank address x; CAa,b = column address a,b.  
NOTE 2 WL = 4 and RL = 6 are shown as examples.  
NOTE 3 DATA = DQ[31:0], DBI[3:0], ECC[1:0], SEV[1:0] for PC0, and DQ[63:32], DBI[7:4], ECC[3:2], SEV[3:2] for PC1.  
WDQS\_t/\_c is WDQS0\_t/\_c for PC0 and WDQS1\_t/\_c for PC1.  
RDQS\_t/\_c is RDQS0\_t/\_c for PC0 and RDQS1\_t/\_c for PC1.  
NOTE 4 Da...Da+7 = data-in for WRITE command b. Db...Db+7 = data-out for READ command a.  
NOTE 5 tWDQS2DQ\_O, tDQSS = 0 and nominal tQW is shown for illustration purposes.  
NOTE 6 tWTR = tWTRL when both WRITE and READ access banks in the same bank group, otherwise t.  
NOTE 7 WDBI could be on or off and is controlled with MR0 OP1.  
NOTE 8 READ operation shown with RDBI enabled. RDBI is enabled/disabled with MR0 OP0.

Figure 47 — Write to Read

## 6.3.3.3.3 Write Operation (cont’d)

The write recovery time t<sub>WR</sub> must have elapsed before a PRECHARGE command can be issued to that bank as shown in Figure 48; the $\mathrm { { t w R } }$ interval begins with the completion of the write burst at WL + BL/4 clock cycles after the WRITE command was issued. Also, t<sub>RAS</sub> must be met when the PRECHARGE is issued. After the PRECHARGE command, a subsequent ACTIVATE command to the same bank cannot be issued until t<sub>RP</sub> is met.

![](images/8457c95190564fad265aa6e9c3d4e3b94b0d7b307a0750545b7a93bf124ceac7.jpg)  
NOTE 1 BAx = bank address x; CAa = column address a.  
NOTE 2 WL = 4 is shown as an example.  
NOTE 3 DATA = DQ[31:0], DBI[3:0], ECC[1:0] for PC0, and DQ[63:32], DBI[7:4], ECC[3:2] for PC1. DPAR = DPAR0 for PC0 and DPAR1 for PC1 (if applicable). WDQS\_t/\_c is WDQS0\_t/\_c for PC0 and WDQS1\_t/\_c for PC1  
NOTE 4 Da...Da+7 = data-in for WRITE command a.  
NOTE 5 tDQSS = 0 is shown for illustration purposes.  
NOTE 6 WDBI could be on or off and is controlled with MR0 OP1.

Figure 48 — Write to Pre-charge

## 6.3.3.3.4 Per-Signal-Group for Write De-Skew

The internal WDQS clock tree is optimized for lowest signal skew among signals within a group as outlined in Table 44. The grouping is aligned with the physical location of signals in a DWORD (see HBM4 Bump map) with no lane being repaired.

Each group contains 5 to 8 signals. The internal WDQS clock tree, however, compensates the different loading by e.g., adding dummy loads. The per-group de-skew is also deterministic and not frequency dependent. A larger signal skew should be expected between different groups. A per-group de-skew is recommended to achieve the largest signaling margin for write data.

Table 44 — Signal Groups for Write Data De-Skew
<table><tr><td rowspan=1 colspan=1>Group</td><td rowspan=1 colspan=1>Signal List (DWORD0)</td><td rowspan=1 colspan=1>Signal List (DWORD1)</td></tr><tr><td rowspan=1 colspan=1>TO</td><td rowspan=1 colspan=1>DQ0, DQ1, DQ2, DQ8, DQ9, DQ10,ECC0, ECC1</td><td rowspan=1 colspan=1>DQ32, DQ33, DQ34, DQ40, DQ41, DQ42,ECC2, ECC3</td></tr><tr><td rowspan=1 colspan=1>T1</td><td rowspan=1 colspan=1>DQ3, DQ4, DQ11, DQ12,RD0, DPAR0</td><td rowspan=1 colspan=1>DQ35, DQ36, DQ43, DQ44,RD2, DPAR1</td></tr><tr><td rowspan=1 colspan=1>T2</td><td rowspan=1 colspan=1>DQ5, DQ6, DQ7, DQ13, DQ14, DQ15,DBI0, DBI1</td><td rowspan=1 colspan=1>DQ37, DQ38, DQ39, DQ45, DQ46, DQ47DBI4, DBI5</td></tr><tr><td rowspan=1 colspan=1>T3</td><td rowspan=1 colspan=1>DQ16, DQ17, DQ18, DQ24, DQ25, DQ267</td><td rowspan=1 colspan=1>DQ48, DQ49, DQ50, DQ56, DQ57, DQ58</td></tr><tr><td rowspan=1 colspan=1>T4</td><td rowspan=1 colspan=1>DQ19, DQ20, DQ27, DQ28,RD1</td><td rowspan=1 colspan=1>DQ51, DQ52, DQ59, DQ60,RD3</td></tr><tr><td rowspan=1 colspan=1>T5</td><td rowspan=1 colspan=1>DQ21, DQ22, DQ23, DQ29, DQ30, DQ31,DBI2, DBI3                    1</td><td rowspan=1 colspan=1>DQ53, DQ54, DQ55, DQ61, DQ62, DQ63,DBI6, DBI7</td></tr></table>

## 6.3.3.4 Mode Register Set (MRS) Command

The MODE REGISTER SET (MRS) command is a 1-cycle command as shown in Figure 49 and is used to load the Mode Registers of the HBM4 DRAM. The command is received on the column command inputs C[7:0] and requires an RNOP command on the row command inputs R[9:0].

Inputs MA[4:0] select one of the twenty Mode Registers, and inputs OP[7:0] determine the opcode to be loaded. Refer to the Mode Registers clause for the register definition.

![](images/eebd9d48a1866bc0af41aac640690b8709a676dc781b99f59a4250c761a31b28.jpg)  
NOTE 1 MA = Mode Register Address; OP = Opcode; V = Valid (H or L)  
Figure 49 — Mode Register Set Command (MRS)

The MODE REGISTER SET (MRS) command can only be issued when all banks are idle, the time t<sub>RDMRS</sub> from a preceding READ command has elapsed and the time t<sub>WRMRS</sub> from a preceding WRITE command has elapsed. The MRS command cycle time t<sub>MRD</sub> is required to complete the write operation to the Mode Register and is the minimum time required between two MRS commands. The MRS command to Non-MRS command delay, t<sub>MOD</sub>, is required by the HBM4 DRAM to update the features, and is the minimum time required from an MRS command to a non-MRS command excluding RNOP and CNOP.

Parity is evaluated with the MODE REGISTER SET command when CA parity has already been enabled in the Mode Register prior to this MODE REGISTER SET command. When CA parity is enabled by a MODE REGISTER SET command, the HBM4 DRAM requires all subsequent commands including RNOP and CNOP to be issued with correct parity until t<sub>MOD</sub> has expired for the MODE REGISTER SET command that disables CA parity.

## 6.3.3.4 Mode Register Set (MRS) Command (cont’d)

![](images/8d5d9e7939a6a18a4b386ad77bad02d44b40a2ea3046ecc321aa69a97e1c14e9.jpg)  
Valid = Any row command allowed in bank idle state  
NOTE 1 Valid shown as half cycle for illustration purposes.

Figure 50 — Mode Register Set Timings

## 6.3.4 Power-Mode Commands

## 6.3.4.1 Power-Down (PDE, PDX)

HBM4 devices enter Power-down with a Power-down Entry command as shown in Figure 51.

![](images/15b5314b48dc6a760207f8f240707214e9ca8bae8c2ec01c98448f5f70e2218c.jpg)  
Figure 51 — Power-Down Entry Command

Power-down Entry must not be issued when read or write operations are in progress on either PC. A read operation is completed when the last data element including parity (when enabled) and RDQS postamble has been transmitted on the outputs. A write operation is completed when the last data element including parity (when enabled) has been written to the memory array with t<sub>WR</sub> satisfied; for writes with autoprecharge, the number of clock cycles programmed in the mode register for WR must have elapsed instead.

Power-down Entry can be issued while any other operations such as row activation, precharge, auto precharge, or refresh are in progress, but the power-down IDD specification will not apply until such operations are complete.

If power-down occurs when all banks are idle, this mode is referred to as precharge power-down; if power-down occurs when there is a row active in any bank, this mode is referred to as active powerdown.

To ensure that there is enough time to internally process the power-down entry, POWER DOWN ENTRY and CNOP commands have to be maintained for t<sub>CPDED</sub> period. Also, the CK clock must be held stable for t<sub>CKPDE</sub> cycle.

## 6.3.4.1 Power-Down (PDE, PDX) (cont’d)

Once t<sub>CPDED</sub> and t<sub>CKPDE</sub> have been met, the pins shall have the following states (see Table 45):

The RESET\_n and R0 receiver remains active; RESET\_n = HIGH and R0 = LOW must be maintained to keep the HBM4 DRAM in power-down;

The CK clock receiver remains active. The clock may be stopped with CK\_t and CK\_c being driven to static LOW and HIGH levels, respectively; in that case the clock must be stable again with t<sub>CH</sub>(min) and t<sub>CL</sub>(min) satisfied at least t<sub>CKPDX</sub> cycles prior to power-down exit;

<sup></sup> WDQS\_t = static LOW and WDQS\_c = static HIGH levels must be maintained, respectively;

<sup></sup> RDQS\_t and RDQS\_c continue driving static LOW and HIGH levels, respectively;

<sup></sup> AERR, DERR continue driving static LOW levels;

<sup></sup> CATTRIP continues driving valid HIGH or LOW levels;

<sup></sup> All other input and output buffers are deactivated.

No refresh operations are performed in power-down mode. The maximum duration in power-down mode is limited by the refresh requirements of the device.

While in power-down the device will maintain the internal DBI state for the DBI(ac) calculation when DBI is enabled in the Mode Register. The device will also continue driving RDQS\_t and RDQS\_c to LOW and HIGH static levels, respectively, and CATTRIP to valid HIGH or LOW levels.

Power-down is synchronously exited when R0 is registered HIGH (in conjunction with CNOP commands). A valid executable command may be applied t<sub>XP</sub> cycles later. The minimum power-down duration is specified by t<sub>PD</sub>.

If CA parity is enabled, parity is evaluated for the POWER-DOWN ENTRY command. The HBM4 device requires PDE and CNOP commands with valid parity for the entire t<sub>CPDED</sub> period, while it will suspend parity checking after power-down entry and drive AERR to a static LOW. DERR remains LOW as there are no data bursts in progress at this time.

Parity is not evaluated for the POWER-DOWN EXIT command. The HBM4 device requires RNOP and CNOP commands with valid parity for the entire t<sub>XP</sub> period, while within t<sub>XP</sub> period it will resume parity checking and indicating parity errors on AERR. DERR remains LOW as there are no data bursts in progress at this time.

Power-down is entered when R[3:0] are registered HIGH, LOW, HIGH, LOW along with CNOP commands as shown in Figure 52. PDE and CNOP commands are required for t<sub>CPDED</sub> period after powerdown entry.

## 6.3.4.1 Power-Down (PDE, PDX) (cont’d)

![](images/9cb0eb2a4adf4515df107cd599a2ca6c0e16f6f948d52abaac0b3cdcaa77f574.jpg)  
NOTE 1 Only PDE and CNOP commands are allowed during tCPDED period. PDX, RNOP and CNOP commands are allowed during tXP periods.  
prior to power-down entry.  
NOTE 3 Read bursts must have been completed with tRDPDE satisfied prior to power-down entry.  
NOTE 4 Address inputs are "Don't Care" for power-down entry and exit.  
NOTE 5 AERR, DERR are driven LOW when parity check is suspended during power-down. Signals are shown with tPARAC=0 and tPARDQ=0 for illustration purpose.  
NOTE 6 The CK clock may be stopped during power-down as shown, or toggling.  
NOTE 7 tCKPDE means valid CK clocks required after first power-down entry.  
NOTE 8 tCKPDX means valid CK clocks required before power-down exit.  
NOTE 9 Second PDE and third PDE after first PDE are treated as a RNOP and do not issue a power down entry.

Figure 52 — Power-Down Entry and Exit

## 6.3.4.1 Power-Down (PDE, PDX) (cont’d)

Table 45 — Pin State Description in Power Down
<table><tr><td rowspan=1 colspan=1>Pin Group</td><td rowspan=1 colspan=1>Pin State</td></tr><tr><td rowspan=1 colspan=1>RESET_n</td><td rowspan=1 colspan=1>H</td></tr><tr><td rowspan=1 colspan=1>CK_t, CK_c</td><td rowspan=1 colspan=1>L/H or Toggling</td></tr><tr><td rowspan=1 colspan=1>R0</td><td rowspan=1 colspan=1>L</td></tr><tr><td rowspan=1 colspan=1>R[9:1]</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>C[7:0]</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>APAR, ARFU</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>AERR</td><td rowspan=1 colspan=1>L</td></tr><tr><td rowspan=1 colspan=1>DQ, DBI, ECC, SEV, DPAR</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>WDQS_t, WDQS_c</td><td rowspan=1 colspan=1>L/H</td></tr><tr><td rowspan=1 colspan=1>RDQS_t, RDQS_c</td><td rowspan=1 colspan=1>L/H</td></tr><tr><td rowspan=1 colspan=1>DERR</td><td rowspan=1 colspan=1>L</td></tr><tr><td rowspan=1 colspan=1>CATTRIP</td><td rowspan=1 colspan=1>7   V</td></tr><tr><td rowspan=1 colspan=2>NOTE 1 For the pin state description, the following definitions apply:a) &quot;L” is defined as “LOW”, and “H&quot; is defined as “HIGH”b) “X&quot; is defined as “Don&#x27;t Care&quot;, and “V” is defined as “Valid&quot;</td></tr></table>

![](images/fed10b958005db60d1f8795b11f741d63653a8b4209154cf3e07e4038f339315.jpg)  
NOTE 1 PRE indicates the internal auto-precharge for RDA commands.  
NOTE 2 BL = 8, RL = 6, and PL =1 are shown as examples.  
NOTE 3 R0 must be used for command except for PDE or address until the end of the read burst operation.

Figure 53 — READ or READ with Auto Precharge to Power-Down Entry Timing

## 6.3.4.1 Power-Down (PDE, PDX) (cont’d)

![](images/6142b07889cef81ebdb7d99e21a5393a41cdb28289a1cefc8fe4c7a113045496.jpg)  
NOTE 1 PRE indicates the internal auto-precharge for WRA commands.  
NOTE 2 BL = 8, WL = 4 and PL = 1 are shown as examples.  
NOTE 3 R0 must be used for address until the end of the write burst operation.  
NOTE 4 tWR is the analog value used with WR commands.  
NOTE 5 nWR is the number of clock cycles programmed for WR in the Mode Register and used with WRA commands.

Figure 54 — WRITE or WRITE with Auto Precharge to Power-Down Entry Timing  
![](images/d99eeb6d374e9a483173597b91fbf323cc4fa4f61d9d4d487a8ba2f9c06bcf92.jpg)  
Figure 55 — MODE REGISTER SET to Power-Down Entry Timing

## 6.3.4.1 Power-Down (PDE, PDX) (cont’d)

![](images/4fc6ba915627ce4d5ac0f7d207821e07e2a03c02898319200fdb531105af2bbe.jpg)

NOTE 1 In the case of a PDE command following an ACTIVATE command that opens a bank, the clocks must continue to run from the ACTIVATE until the number of cycles programmed in the RAS register in MR4 and tCKPDE have been met. In the case of an ACTIVATE to capture a DRFM row address, tCKPDE must be met before the clocks are stopped in addition to RAS from the ACTIVATE that opened the bank.

Figure 56 — ACTIVATE to Power-Down Entry Timing

![](images/5a9c5f25d28412f2d44717652e6990ebfbb487d082a9be3f12ff7c1861911d01.jpg)  
NOTE 1 Upon power-down entry the clock must be kept active for the number of clock cycles programmed in the RAS register in MR4 and tCKPDE has been met, referenced to the REFRESH or PER BANK REFRESH command.

Figure 57 — REFab or REFpb to Power-Down Entry Timing  
![](images/831d111e6477fcb4e9b5b44118a7f008abf2c5d452fdcc1c3109e453660f6570.jpg)  
Figure 58 — PRECHARGE to Power-Down Entry Timing

## 6.3.4.2 Self Refresh (SRE, SRX)

Self refresh can be used to retain data in the HBM4 device, even if the rest of the system is powered down. When in the self refresh mode, the HBM4 device retains data without external clocking. The command is received on the row command inputs R[9:0] as shown in Figure 59 and requires a CNOP command on the column command inputs C[7:0].

![](images/93e42856c3312e450720b9cec682291a4de1de586aa9d2fca77802bd188cd63e.jpg)  
Figure 59 — Self-Refresh Entry Command

Self refresh entry is only allowed when all banks in both pseudo channels are precharged with tRP satisfied, the last data elements from a preceding READ command have been pushed out (t<sub>RDSRE</sub>), or t<sub>MOD</sub> from a preceding MODE REGISTER SET command is met. PDE and CNOP commands are required after entering self refresh mode until t<sub>CPDED</sub> is met.

Once the SELF REFRESH-ENTRY command is registered, R0 must be held LOW to keep the device in self refresh mode. For proper self refresh operation, all power supply pins (V<sub>DDC</sub>, V<sub>DDQ</sub>, V<sub>PP</sub>, V<sub>DDQL</sub>) must be at valid levels. The HBM4 device initiates a minimum of one internal refresh within t<sub>CKSR</sub> period once it enters self refresh mode.

The clocks are internally disabled during self refresh operation to save power. The minimum time that the HBM4 device must remain in self refresh mode is t<sub>CKSR</sub>. The user may halt the external clock or change the external clock frequency t<sub>CKSRE</sub> after self refresh entry is registered. However, the clock must be restarted and stable $\mathrm { \ t { _ { C K S R X } } }$ before the device can exit self refresh operation.

To ensure that there is enough time to internally process the self refresh entry, POWER DOWN ENTRY and CNOP commands have to be maintained for t<sub>CPDED</sub> period following the SELF REFRESH ENTRY command. Also, the CK clock must be held stable for t<sub>CKSRE</sub> cycle.

## 6.3.4.2 Self Refresh (SRE, SRX) (cont’d)

Once t<sub>CPDED</sub> and t<sub>CKSRE</sub> have been met, the pins shall have the following states (see Table 46):

The RESET\_n and R0 receiver remains active; RESET\_n = HIGH and R0 = LOW must be maintained to keep the HBM4 DRAM in self refresh;

The CK clock receiver is disabled; the clock may be stopped, or the clock frequency may be changed; MRS required to set after t<sub>XSMRSF</sub> in case of frequency changed; the clock must be stable again with t<sub>CH</sub>(min) and t<sub>CL</sub>(min) satisfied at least t<sub>CKSRX</sub> cycles prior to self refresh exit;

<sup></sup> WDQS\_t = static LOW and WDQS\_c = static HIGH levels must be maintained, respectively;

<sup></sup> RDQS\_t and RDQS\_c continue driving static LOW and HIGH levels, respectively;

<sup></sup> AERR, DERR continue driving static LOW levels;

<sup></sup> CATTRIP continues driving valid HIGH or LOW levels;

<sup></sup> All other input and output buffers are deactivated.

If CA parity is enabled, parity is evaluated for the SELF REFRESH ENTRY command. The HBM4 device requires PDE and CNOP commands with valid parity for the entire t period, while it will suspend parity checking after self refresh entry and drive AERR to a static LOW. DERR remains LOW as there are no data bursts in progress at this time.

Parity is not evaluated for the SELF REFRESH EXIT command. The HBM4 device requires RNOP and CNOP commands with valid parity for the entire t<sub>XS</sub> period, while within t<sub>XS</sub> period it will resume parity checking and indicating parity errors on AERR. DERR remains LOW as there are no data bursts in progress at this time.

The procedure for exiting self refresh requires a sequence of events. First, the CK clock must be stable prior to R0 going back HIGH. A delay of at least t<sub>XS</sub> must be satisfied before a valid command can be issued to the device to allow for completion of any internal refresh in progress.

Upon exit from self refresh, the HBM4 device can be put back into self refresh mode after waiting at least t<sub>XS</sub> period.

## 6.3.4.2 Self Refresh (SRE, SRX) (cont’d)

![](images/ff3890df14ca2bd222fad0be89be626383409667dc74e0d15b33ed22548ff7a2.jpg)  
NOTE 1 Only PDE and CNOP commands are allowed during t period. Only RNOP and CNOP commands are allowed during tXS periods, except for MRS commands which are allowed tXSMRS(or tXSMRSF when in case of frequency changed, tXSMRSF can be required longer than tXS) after self-refresh exit.  
NOTE 2 Write bursts must have been completed with tRP satisfied prior to self-refresh entry.  
NOTE 3 Read bursts must have been completed with tRDSRE satisfied prior to self-refresh entry.  
NOTE 4 Address inputs are "Don't Care" for self-refresh entry and exit.  
NOTE 5 AERR, DERR are driven LOW when parity check is suspended during self-refresh. Signals are shown with $\scriptstyle \mathrm { t p } _ { \mathrm { A R A C } } = 0$ and tPARDQ=0 for illustration purpose.  
NOTE 6 PDE commands after SRE are treated as a RNOP and does not issue a power down entry.

Figure 60 — Self-Refresh Entry and Exit

## 6.3.4.2 Self Refresh (SRE, SRX) (cont’d)

Table 46 — Pin State Description in Self Refresh
<table><tr><td rowspan=1 colspan=1>Pin Group</td><td rowspan=1 colspan=1>Pin State</td></tr><tr><td rowspan=1 colspan=1>RESET_n</td><td rowspan=1 colspan=1>H</td></tr><tr><td rowspan=1 colspan=1>CK_t, CK_c</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>R0</td><td rowspan=1 colspan=1>L</td></tr><tr><td rowspan=1 colspan=1>R[9:1]</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>C[7:0]</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>APAR, ARFU</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>AERR</td><td rowspan=1 colspan=1>L</td></tr><tr><td rowspan=1 colspan=1>DQ, DBI, ECC, SEV, DPAR</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>WDQS_t, WDQS_c</td><td rowspan=1 colspan=1>L/H</td></tr><tr><td rowspan=1 colspan=1>RDQS_t, RDQS_c</td><td rowspan=1 colspan=1>L/H</td></tr><tr><td rowspan=1 colspan=1>DERR</td><td rowspan=1 colspan=1>L</td></tr><tr><td rowspan=1 colspan=1>CATTRIP</td><td rowspan=1 colspan=1>    V</td></tr><tr><td rowspan=1 colspan=2>NOTE 1 For the pin state description, the following definitions apply:a) “L” is defined as “LOW”, and “H” is defined as “HIGH”b) “X” is defined as “Don&#x27;t Care&quot;, and “V” is defined as “Valid&quot;</td></tr></table>

## 6.4 Parity

## 6.4.1 Command/Address Parity

The HBM4 DRAM includes a command/address parity checking function controlled by the CAPAR bit in MR0 OP6. The function is disabled by default. The APAR input and AERR output are associated with the function. APAR is enabled only when the function is enabled.

If enabled, the parity is calculated every CK clock cycle separately on both the rising and falling CK clock edges over input signals R[9:0], C[7:0], ARFU and APAR as summarized in Table 47. The AERR output indicates whether a parity error has occurred or not on either the rising or falling CK clock edge (or both edges). The HBM4 DRAM executes commands regardless of command/address parity errors.

Table 47 — Command/Address Parity Function Table
<table><tr><td rowspan=1 colspan=1>INPUTS</td><td rowspan=1 colspan=1>Sum of Inputs Received HIGH</td><td rowspan=1 colspan=1>AERR</td></tr><tr><td rowspan=2 colspan=1>R[9:0], C[7:0], ARFU, APAR</td><td rowspan=1 colspan=1>Even</td><td rowspan=1 colspan=1>LOW</td></tr><tr><td rowspan=1 colspan=1>Odd</td><td rowspan=1 colspan=1>HIGH</td></tr><tr><td rowspan=1 colspan=3>NOTE 1 See Command Truth Tables for command and device state exceptions.</td></tr></table>

The HBM4 DRAM may begin to check parity on the next clock cycle following the MODE REGISTER SET command that enables the parity checking function; it will have the parity check enabled latest when t<sub>MOD</sub> has expired after that MODE REGISTER SET command. The HBM4 DRAM therefore requires all subsequent commands including RNOP and CNOP to be issued with correct parity until when t<sub>MOD</sub> has expired for the MODE REGISTER SET command that disables the parity calculation. See also the Power-Down and Self Refresh clauses. AERR is driven LOW by the HBM4 DRAM at reset.

For every parity error, AERR is driven HIGH for 1 t<sub>CK</sub>, t<sub>PARAC</sub> after the corresponding cycle of the error inputs. In the case of consecutive errors, the AERR signal will stay HIGH during the next cycle. The parity function should not be disabled within t<sub>PARAC</sub> after an access command.

![](images/2e2235e68d1050e0f138a7c228133b40a2c9000f400c306979c6fbefb4784a3d.jpg)  
NOTE 1 For illustration purpose, tPARAC is shown with 0 tCK digital and 0 ns analog output delay.

NOTE 2 See Power-Down and Self Refresh clauses for details on disabling and enabling parity check in conjunction with power-down and self refresh entry and exit.

Figure 61 — Enabling and Disabling Command/Address Parity

## 6.4.1 Command/Address Parity (cont’d)

Figure 62 illustrates a single parity error occurrence on the R inputs. In this case, the error occurs at the rising edge of the first cycle of the ACTIVATE command at time T0. After $\mathrm { t } _ { \mathrm { P A R A C } } ,$ AERR is driven HIGH for 1 t<sub>CK</sub> and then LOW since no subsequent errors occur.

![](images/a86bd2217a708c5465f61fd01d961fdd0cc925a7ba56364ff35a28cbe7d5aab3.jpg)  
NOTE 1 For illustration purpose, tPARAC is shown with 2 tCK digital and 0 ns analog output delay. NOTE 2 MR0 OP6 shall be maintained as 1 for at least tPARAC after the access command.  
Figure 62 — Single Command/Address Parity Error

Figure 63 illustrates parity error occurrences on the R and the C inputs. In this case, the error occurs at the falling edge of the first cycle of the ACTIVATE command at time T0. After $\mathrm { \ t p { \scriptstyle A R A C } } ,$ AERR is driven HIGH for 1 t<sub>CK</sub> and then LOW for 1 t<sub>CK</sub>. Since an error also occurs in T2 at both the rising and the falling edges of the READ or WRITE command, the AERR is again driven HIGH for 1 t<sub>CK</sub> and then LOW since no subsequent errors occur.

![](images/9fe73dbd9bb90cefa3224d3f21bd5d1ceaedc22823b58ed8314464b113ae4b09.jpg)  
NOTE 1 For illustration purpose, tPARAC is shown with 2 tCK digital and 0 ns analog output delay. NOTE 2 MR0 OP6 shall be maintained as 1 for at least tPARAC after the access command.  
Figure 63 — Separated Command/Address Parity Errors

## 6.4.1 Command/Address Parity (cont’d)

Figure 64 illustrates consecutive parity error occurrences on the R and the C inputs during the T0, T1, and T2 cycles and either the rising, the falling or both clock edges. Due to the common AERR output, parity error occurrences on both interfaces are indistinguishable.

![](images/2f715c41824c3993aeda97aaae1d3de8f4961796a7dec8f04524da3a45ca3949.jpg)  
NOTE 1 For illustration purpose, tPARAC is shown with 2 tCK digital and 0 ns analog output delay. NOTE 2 MR0 OP6 shall be maintained as 1 for at least tPARAC after the access command.  
Figure 64 — Consecutive Command/Address Parity Errors

## 6.4.2 Data Parity

The HBM4 DRAM includes a data parity checking function for writes controlled by the WPAR bit in MR0 OP5, and a data parity generation function for reads controlled by the RPAR bit in MR0 OP4. Both WPAR and RPAR functions are disabled by default. There is one DPAR bidirectional DDR I/O and one DERR output signal per DWORD associated with the function. The DPAR input is enabled with WPAR during writes, and the DPAR output is enabled with RPAR during reads, otherwise DPAR is disabled.

The data parity function includes a programmable parity latency PL between the corresponding data and the DPAR signal. PL is programmed in MR1 OP[7:5], and is the same for writes and reads. The corresponding DPAR signal will be received and sent PL cycles later. The WDQS and RDQS strobes will have additional strobe cycles with the same preamble and postambles to accommodate the latching of the delayed DPAR signal at both ends. Examples of reads and writes with DQ parity enabled can be found in the Write Command and Read Command clauses. The DRAM vendor’s datasheet shall be consulted for the range of supported PL values.

On read transactions, the HBM4 DRAM generates parity and transmits the parity on the DPAR signal along with the corresponding data on DQ, DBI and ECC.

On write transactions, the HBM4 DRAM compares the DPAR input with the corresponding data received on DQ, DBI and ECC inputs as summarized in Table 48. The parity calculation is performed separately for each UI of a write burst.

If an error occurs in any single or in multiple UIs within one clock cycle of a write burst (D0 ... D3 or D4 ... D7), DERR is driven HIGH for 1 t<sub>CK</sub>, t<sub>PARDQ</sub> after the corresponding cycle of error inputs. The t<sub>PARDQ</sub> interval for errors occurring during the first clock cycle of a write burst begins (WL + PL) clock cycles after the WRITE command was issued. In case of errors within the first and the second clock cycle of a write burst, DERR will stay HIGH during the next cycle. DERR is driven LOW by the HBM4 DRAM at reset.

When an error occurs, the HBM4 DRAM does not block the write data. The HBM4 DRAM completes the write transaction to the array as normal.

WPAR should not be disabled within (WL + PL + t<sub>PARDQ</sub> + 2 t<sub>CK</sub>) after the WRITE command in order to not create a conflict with any ongoing parity operation. For the same reason RPAR should not be disabled within t after the READ command.

As outlined in Table 48, metadata received and sent via the ECC signals are included in the parity check and parity generation only when these signals are enabled by the MD bit in MR9 OP0. Similarly, the DBI signals are included in the parity check and parity generation only when these signals are enabled by the WDBI and RDBI bits in MR0 OP[1:0]. The SEV signals are not included in the parity check or parity generation.

## 6.4.2 Data Parity (cont’d)

Table 48 — Data Parity Function Table
<table><tr><td rowspan=1 colspan=2>CONFIGURATION</td><td rowspan=1 colspan=2>INPUTS</td><td rowspan=2 colspan=1>Sum of InputsReceivedHIGH</td><td rowspan=2 colspan=1>DERR</td></tr><tr><td rowspan=1 colspan=1>MD(MR9 OP0)</td><td rowspan=1 colspan=1>WDBI or RDBI(MR0 OP[1:0])</td><td rowspan=1 colspan=1>DWORD0</td><td rowspan=1 colspan=1>DWORD1</td></tr><tr><td rowspan=4 colspan=1>Enabled</td><td rowspan=2 colspan=1>Enabled</td><td rowspan=2 colspan=1>DQ[31:0], ECC[1:0],DBI[3:0], DPAR0</td><td rowspan=2 colspan=1>DQ[63:32], ECC[3:2],DBI[7:4], DPAR1</td><td rowspan=1 colspan=1>Even</td><td rowspan=1 colspan=1>LOW</td></tr><tr><td rowspan=1 colspan=1>Odd</td><td rowspan=1 colspan=1>HIGH</td></tr><tr><td rowspan=2 colspan=1>Disabled</td><td rowspan=2 colspan=1>DQ[31:0], ECC[1:0],DPAR0</td><td rowspan=2 colspan=1>DQ[63:32], ECC[3:2],DPAR1</td><td rowspan=1 colspan=1>Even</td><td rowspan=1 colspan=1>LOW</td></tr><tr><td rowspan=1 colspan=1>Odd</td><td rowspan=1 colspan=1>HIGH</td></tr><tr><td rowspan=4 colspan=1>Disabled</td><td rowspan=2 colspan=1>Enabled</td><td rowspan=2 colspan=1>DQ[31:0], DBI[3:0],DPARO</td><td rowspan=2 colspan=1>DQ[63:32], DBI[7:4],DPAR1</td><td rowspan=1 colspan=1>Even</td><td rowspan=1 colspan=1>LOW</td></tr><tr><td rowspan=1 colspan=1>Odd</td><td rowspan=1 colspan=1>HIGH</td></tr><tr><td rowspan=2 colspan=1>Disabled</td><td rowspan=2 colspan=1>DQ[31:0], DPAR0</td><td rowspan=2 colspan=1>DQ[63:32], DPAR1</td><td rowspan=1 colspan=1>Even</td><td rowspan=1 colspan=1>LOW</td></tr><tr><td rowspan=1 colspan=1>Odd</td><td rowspan=1 colspan=1>HIGH</td></tr><tr><td rowspan=1 colspan=6>NOTE 1 The DBI inputs are disabled and excluded from the parity check when WDBI is disabled in MR0 OP1.The DBI outputs are disabled and excluded from the parity generation when RDBI is disabled in MR0 OP0. TheECC I/Os are disabled and excluded from the parity check and parity generation when MD is disabled in MR9 OP0.</td></tr></table>

Figure 65 illustrates data parity error occurrences on two seamless write bursts. In this example errors occur in the second (D1), third (D2), sixth (D5) and seventh (D6) UI of the first write burst, and in the fifth (P4) and sixth (P5) UI of the DPAR input of the second write burst. After $\mathrm { t } _ { \mathrm { P A R D Q } } ,$ , DERR is driven HIGH for 2 t<sub>CK</sub> at T5 and T6, then driven LOW for 1 t<sub>CK</sub> and again driven HIGH for 1 t<sub>CK</sub> at T8.

![](images/10d775cbe41f92eb47acc68f4fc95a5f37e0b962c0e590e0b0b1fdb485135c44.jpg)  
NOTE 1 D0 … D7 = data-in for WRITE command (BL8 burst). P0 … P7 = parity-in for WRITE command.  
NOTE 2 DATA = DQ[31:0], DBI[3:0], ECC[1:0] for PC0, and DQ[63:32], DBI[7:4], ECC[3:2] for PC1. WDQS\_t/\_c is WDQS0\_t/\_c for PC0, and WDQS1\_t/\_c for PC1.  
NOTE 3 Two seamless bursts are shown, with parity errors in the second (D1), third (D2), sixth (D5) and seventh (D6) UI of the first write burst, and in the fifth (P4) and sixth (P5) UI of the DPAR input of the second write burst. NOTE 4 PL=2 is assumed.  
NOTE 5 The parity check is performed separately for the first clock cycle (UI = D0 … D3) and the second clock cycle (UI = D4 … D7) of a BL8 burst.  
NOTE 6 tPARDQ is shown with 2 tCK digital and 0 ns analog output delay.  
NOTE 7 WDBI could be on or off and is controlled with MR0 OP1. WDBI shall be maintained enabled for at least tPARDQ after the access command.

Figure 65 — Write Parity Errors with PL = 2

## 6.4.2 Data Parity (cont’d)

Examples of single write bursts with write data parity enabled are shown in Figure 66 and Figure 67.   
With PL= 2 four additional WDQS pulses are received at cycles T8 and T9 to latch the DPAR input.

![](images/a276d6fc75e7b9a01d6dea08ce2d27d7e3ae884e475d65decbfca723831a19ed.jpg)  
NOTE 1 D0 … D7 = data-in for WRITE command (BL8 burst). P0 … P7 = parity-in for WRITE command.  
NOTE 3 WL = 6 and PL=2 is assumed.  
NOTE 4 WDBI could be on or off and is controlled with MR0 OP1.

Figure 66 — Write Parity Alignment with PL = 2

With PL = 4, the WDQS postamble for the write data at cycle T8 is immediately followed by the WDQS preamble for the write parity data at cycle T9, resulting in continuous WDQS pulses over the write data and data parity bursts.

![](images/56405a26b77797aceaad6c79470d16271c230823ebb867c948fdf23a215bea46.jpg)  
NOTE 1 D0 … D7 = data-in for WRITE command (BL8 burst). P0 … P7 = parity-in for WRITE command. NOTE 2 DATA = DQ[31:0], DBI[3:0], ECC[1:0] for PC0, and DQ[63:32], DBI[7:4], ECC[3:2] for PC1. WDQS\_t/\_c is WDQS0\_t/\_c for PC0, and WDQS1\_t/\_c for PC1.  
NOTE 3 WL = 6 and PL=4 is assumed.  
NOTE 4 WDBI could be on or off and is controlled with MR0 OP1.

Figure 67 — Write Parity Alignment with PL = 4

Examples of a single read bursts with read data parity enabled are shown in Figure 68 and Figure 69. The DPAR output is preconditioned over half a clock cycle like for the even data bytes. With PL = 2 four additional WDQS and RDQS pulses for DPAR are received and returned at cycles T12 and T13.

6.4.2 Data Parity (cont’d)  
![](images/b988c457c556d47682055734f1b9e3b6fa52be39947faebf3c1f853846842796.jpg)  
NOTE 1 D0 … D7 = data-out for READ command (BL8 burst). P0 … P7 = parity-out for READ command.  
NOTE 4 RDBI could be on or off and is controlled with MR0 OP0.

Figure 68 — Read Parity Alignment with PL = 2

With PL = 4, the WDQS postamble for the read data at cycle T12 overlaps with the WDQS preamble for the read parity data. The RDQS postamble for the read data at cycle T12 is immediately followed by the RDQS preamble for the read parity data at cycle T13, both resulting in continuous WDQS and RDQS pulses over the read data and data parity bursts.

![](images/afae28812edef23f2ef4e64e769e2f5abcdbcc7ddf46e647cad23aea3d124882.jpg)  
NOTE 1 D0 … D7 = data-out for READ command (BL8 burst). P0 … P7 = parity-out for READ command. NOTE 2 DATA = DQ[31:0], DBI[3:0], ECC[1:0] for PC0, and DQ[63:32], DBI[7:4], ECC[3:2] for PC1. RDQS\_t/\_c is RDQS0\_t/\_c for PC0, and RDQS1\_t/\_c for PC1. WDQS\_t/\_c is WDQS0\_t/\_c for PC0, and WDQS1\_t/\_c for PC1. NOTE 3 RL = 10 and PL=4 is assumed.  
NOTE 4 RDBI could be on or off and is controlled with MR0 OP0.

Figure 69 — Read Parity Alignment with PL = 4

## 6.5 Clock Frequency Change Sequence

Clock Frequency changes can occur during self refresh mode only. When the CK clock is stopped after self refresh entry, it can be restarted at a different frequency. If the change in clock-rate requires changes to configuration parameters, MRS commands immediately prior to or after self refresh mode may be required.

## 6.6 Catastrophic Temperature Sensor

The CATTRIP sensor logic detects if the junction temperature of any die in the HBM4 stack exceeds a catastrophic trip-point level. The level is set by the DRAM vendor to a value below the temperature that would result in permanent damage to the device. If the junction temperature anywhere in the stack exceeds that catastrophic trip-point level, the HBM4 device will drive the CATTRIP pin to HIGH.

The CATTRIP output is sticky in that device power-off is required to clear the CATTRIP output to LOW. Sufficient time should be allowed for the device to cool after a CATTRIP event. See HBM4 Power-Up and Initialization Sequence for the initialization of the CATTRIP pin.

The circuits associated with the CATTRIP pin will operate correctly even if the catastrophic trip-point level has been exceeded, and regardless of whether the external or internal clocks have stopped. The functionality of CATTRIP can be verified by writing a “1” to MR7 OP7 to force CATTRIP to HIGH, and “0” to set CATTRIP back to LOW.

## 6.7 Interconnect Redundancy Remapping

The HBM4 DRAM supports interconnect lane remapping to help improve SIP assembly yield and recover functionality of the HBM4 stack. The SOFT\_LANE\_REPAIR and HARD\_LANE\_REPAIR instructions are used to perform lane remapping. AWORD and DWORD lane remapping are independent for each channel. WSO remapping is associated with Channel 1 for WSO0 through WSO15 and Channel 17 for WSO16 through WSO31. When WIR[13:8] is $0 1 _ { \mathrm { h } }$ (Channel 1) or $1 1 _ { \mathrm { h } }$ (Channel 17) the WDR length is 45, otherwise the WDR length is 40. See the Test Instructions clause for more details.

SOFT\_LANE\_REPAIR and HARD\_LANE\_REPAIR instructions can only be issued as a part of the device initialization and before normal memory operation has commenced, e.g., before the CK clock has started to toggle.

The HBM4 DRAM can be programmed to retain the remapped lane information even when power is completely removed from the HBM4 stack.

Only a single broken lane in a single channel or WSO can be repaired at a time, in order to limit the current constraint of the associated circuits. If multiple lanes are to be repaired, it is required to shift in the repair vectors for each broken lane sequentially, with all other lane repair setting = F<sub>h</sub>, and initiate each actual lane repair with a separate UpdateWR event.

## 6.7.1 AWORD Remapping

There is one redundant AWORD lane per channel to either repair one lane in the row command bus or one lane in the column command bus. APAR and ARFU are associated with the column command bus repair as shown in Table 50. $\mathrm { C K \_ c , C K \_ t , }$ and AERR signals cannot be remapped. After a lane is remapped, the input buffer associated with the broken lane is turned off and the input buffer associated with the redundant bump (RA) is turned on. All functionalities are preserved with row or column bus lane remapping.

## 6.7.1.1 Row Command Bus – Remapping Table

Table 49 — AWORD - Row Command Bus Remapping
<table><tr><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>RegisterEncoding</td><td rowspan=1 colspan=1>R1</td><td rowspan=1 colspan=1>R2</td><td rowspan=1 colspan=1>R3</td><td rowspan=1 colspan=1>R0</td><td rowspan=1 colspan=1>R4</td><td rowspan=1 colspan=1>R5</td><td rowspan=1 colspan=1>R6</td><td rowspan=1 colspan=1>R7</td><td rowspan=1 colspan=1>R8</td><td rowspan=1 colspan=1>R9</td><td rowspan=1 colspan=1>RA</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 0</td><td rowspan=1 colspan=1>0001</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>R1</td><td rowspan=1 colspan=1>R2</td><td rowspan=1 colspan=1>R3</td><td rowspan=1 colspan=1>R0</td><td rowspan=1 colspan=1>R4</td><td rowspan=1 colspan=1>R5</td><td rowspan=1 colspan=1>R6</td><td rowspan=1 colspan=1>R7</td><td rowspan=1 colspan=1>R8</td><td rowspan=1 colspan=1>R9</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 1</td><td rowspan=1 colspan=1>0010</td><td rowspan=1 colspan=1>R1</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>R2</td><td rowspan=1 colspan=1>R3</td><td rowspan=1 colspan=1>R0</td><td rowspan=1 colspan=1>R4</td><td rowspan=1 colspan=1>R5</td><td rowspan=1 colspan=1>R6</td><td rowspan=1 colspan=1>R7</td><td rowspan=1 colspan=1>R8</td><td rowspan=1 colspan=1>R9</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 2</td><td rowspan=1 colspan=1>0011</td><td rowspan=1 colspan=1>R1</td><td rowspan=1 colspan=1>R2</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>R3</td><td rowspan=1 colspan=1>R0</td><td rowspan=1 colspan=1>R4</td><td rowspan=1 colspan=1>R5</td><td rowspan=1 colspan=1>R6</td><td rowspan=1 colspan=1>R7</td><td rowspan=1 colspan=1>R8</td><td rowspan=1 colspan=1>R9</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 3</td><td rowspan=1 colspan=1>0000</td><td rowspan=1 colspan=1>R1</td><td rowspan=1 colspan=1>R2</td><td rowspan=1 colspan=1>R3</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>R0</td><td rowspan=1 colspan=1>R4</td><td rowspan=1 colspan=1>R5</td><td rowspan=1 colspan=1>R6</td><td rowspan=1 colspan=1>R7</td><td rowspan=1 colspan=1>R8</td><td rowspan=1 colspan=1>R9</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 4</td><td rowspan=1 colspan=1>0100</td><td rowspan=1 colspan=1>R1</td><td rowspan=1 colspan=1>R2</td><td rowspan=1 colspan=1>R3</td><td rowspan=1 colspan=1>R0</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>R4</td><td rowspan=1 colspan=1>R5</td><td rowspan=1 colspan=1>R6</td><td rowspan=1 colspan=1>R7</td><td rowspan=1 colspan=1>R8</td><td rowspan=1 colspan=1>R9</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 5</td><td rowspan=1 colspan=1>0101</td><td rowspan=1 colspan=1>R1</td><td rowspan=1 colspan=1>R2</td><td rowspan=1 colspan=1>R3</td><td rowspan=1 colspan=1>R0</td><td rowspan=1 colspan=1>R4</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>R5</td><td rowspan=1 colspan=1>R6</td><td rowspan=1 colspan=1>R7</td><td rowspan=1 colspan=1>R8</td><td rowspan=1 colspan=1>R9</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 6</td><td rowspan=1 colspan=1>0110</td><td rowspan=1 colspan=1>R1</td><td rowspan=1 colspan=1>R2</td><td rowspan=1 colspan=1>R3</td><td rowspan=1 colspan=1>R0</td><td rowspan=1 colspan=1>R4</td><td rowspan=1 colspan=1>R5</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>R6</td><td rowspan=1 colspan=1>R7</td><td rowspan=1 colspan=1>R8</td><td rowspan=1 colspan=1>R9</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 7</td><td rowspan=1 colspan=1>0111</td><td rowspan=1 colspan=1>R1</td><td rowspan=1 colspan=1>R2</td><td rowspan=1 colspan=1>R3</td><td rowspan=1 colspan=1>R0</td><td rowspan=1 colspan=1>R4</td><td rowspan=1 colspan=1>R5</td><td rowspan=1 colspan=1>R6</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>R7</td><td rowspan=1 colspan=1>R8</td><td rowspan=1 colspan=1>R9</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 8</td><td rowspan=1 colspan=1>1000</td><td rowspan=1 colspan=1>R1</td><td rowspan=1 colspan=1>R2</td><td rowspan=1 colspan=1>R3</td><td rowspan=1 colspan=1>R0</td><td rowspan=1 colspan=1>R4</td><td rowspan=1 colspan=1>R5</td><td rowspan=1 colspan=1>R6</td><td rowspan=1 colspan=1>R7</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>R8</td><td rowspan=1 colspan=1>R9</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 9</td><td rowspan=1 colspan=1>1001</td><td rowspan=1 colspan=1>R1</td><td rowspan=1 colspan=1>R2</td><td rowspan=1 colspan=1>R3</td><td rowspan=1 colspan=1>R0</td><td rowspan=1 colspan=1>R4</td><td rowspan=1 colspan=1>R5</td><td rowspan=1 colspan=1>R6</td><td rowspan=1 colspan=1>R7</td><td rowspan=1 colspan=1>R8</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>R9</td></tr><tr><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=1>1010to1110</td><td rowspan=1 colspan=1>R1</td><td rowspan=1 colspan=1>R2</td><td rowspan=1 colspan=1>R3</td><td rowspan=1 colspan=1>R0</td><td rowspan=1 colspan=1>R4</td><td rowspan=1 colspan=1>R5</td><td rowspan=1 colspan=1>R6</td><td rowspan=1 colspan=1>R7</td><td rowspan=1 colspan=1>R8</td><td rowspan=1 colspan=1>R9</td><td rowspan=1 colspan=1>RA</td></tr><tr><td rowspan=1 colspan=1>DefaultNo Repair</td><td rowspan=1 colspan=1>1111</td><td rowspan=1 colspan=1>R1</td><td rowspan=1 colspan=1>R2</td><td rowspan=1 colspan=1>R3</td><td rowspan=1 colspan=1>R0</td><td rowspan=1 colspan=1>R4</td><td rowspan=1 colspan=1>R5</td><td rowspan=1 colspan=1>R6</td><td rowspan=1 colspan=1>R7</td><td rowspan=1 colspan=1>R8</td><td rowspan=1 colspan=1>R9</td><td rowspan=1 colspan=1>RA</td></tr><tr><td rowspan=1 colspan=13>NOTE 1 XX = Lane is remapped</td></tr></table>

6.7.1.2 Column Command Bus – Remapping Table  
Table 50 — AWORD - Column Command Bus Remapping
<table><tr><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>RegisterEncoding</td><td rowspan=1 colspan=1>Co</td><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>C2</td><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>C4</td><td rowspan=1 colspan=1>C5</td><td rowspan=1 colspan=1>C6</td><td rowspan=1 colspan=1>C7</td><td rowspan=1 colspan=1>APAR</td><td rowspan=1 colspan=1>ARFU</td><td rowspan=1 colspan=1>RA</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 0</td><td rowspan=1 colspan=1>0000</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>C0</td><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>C2</td><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>C4</td><td rowspan=1 colspan=1>C5</td><td rowspan=1 colspan=1>C6</td><td rowspan=1 colspan=1>C7</td><td rowspan=1 colspan=1>APAR</td><td rowspan=1 colspan=1>ARFU</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 1</td><td rowspan=1 colspan=1>0001</td><td rowspan=1 colspan=1>C0</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>C2</td><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>C4</td><td rowspan=1 colspan=1>C5</td><td rowspan=1 colspan=1>C6</td><td rowspan=1 colspan=1>C7</td><td rowspan=1 colspan=1>APAR</td><td rowspan=1 colspan=1>ARFU</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 2</td><td rowspan=1 colspan=1>0010</td><td rowspan=1 colspan=1>C0</td><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>C2</td><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>C4</td><td rowspan=1 colspan=1>C5</td><td rowspan=1 colspan=1>C6</td><td rowspan=1 colspan=1>C7</td><td rowspan=1 colspan=1>APAR</td><td rowspan=1 colspan=1>ARFU</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 3</td><td rowspan=1 colspan=1>0011</td><td rowspan=1 colspan=1>C0</td><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>C2</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>C4</td><td rowspan=1 colspan=1>C5</td><td rowspan=1 colspan=1>C6</td><td rowspan=1 colspan=1>C7</td><td rowspan=1 colspan=1>APAR</td><td rowspan=1 colspan=1>ARFU</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 4</td><td rowspan=1 colspan=1>0100</td><td rowspan=1 colspan=1>C0</td><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>C2</td><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>C4</td><td rowspan=1 colspan=1>C5</td><td rowspan=1 colspan=1>C6</td><td rowspan=1 colspan=1>C7</td><td rowspan=1 colspan=1>APAR</td><td rowspan=1 colspan=1>ARFU</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 5</td><td rowspan=1 colspan=1>0101</td><td rowspan=1 colspan=1>C0</td><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>C2</td><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>C4</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>C5</td><td rowspan=1 colspan=1>C6</td><td rowspan=1 colspan=1>C7</td><td rowspan=1 colspan=1>APAR</td><td rowspan=1 colspan=1>ARFU</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 6</td><td rowspan=1 colspan=1>0110</td><td rowspan=1 colspan=1>C0</td><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>C2</td><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>C4</td><td rowspan=1 colspan=1>C5</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>C6</td><td rowspan=1 colspan=1>C7</td><td rowspan=1 colspan=1>APAR</td><td rowspan=1 colspan=1>ARFU</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 7</td><td rowspan=1 colspan=1>0111</td><td rowspan=1 colspan=1>C0</td><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>C2</td><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>C4</td><td rowspan=1 colspan=1>C5</td><td rowspan=1 colspan=1>C6</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>C7</td><td rowspan=1 colspan=1>APAR</td><td rowspan=1 colspan=1>ARFU</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 8</td><td rowspan=1 colspan=1>1000</td><td rowspan=1 colspan=1>C0</td><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>C2</td><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>C4</td><td rowspan=1 colspan=1>C5</td><td rowspan=1 colspan=1>C6</td><td rowspan=1 colspan=1>C7</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>APAR</td><td rowspan=1 colspan=1>ARFU</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 9</td><td rowspan=1 colspan=1>1001</td><td rowspan=1 colspan=1>C0</td><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>C2</td><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>C4</td><td rowspan=1 colspan=1>C5</td><td rowspan=1 colspan=1>C6</td><td rowspan=1 colspan=1>C7</td><td rowspan=1 colspan=1>APAR</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>ARFU</td></tr><tr><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=1>1010to1110</td><td rowspan=1 colspan=1>C0</td><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>C2</td><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>C4</td><td rowspan=1 colspan=1>C5</td><td rowspan=1 colspan=1>C6</td><td rowspan=1 colspan=1>C7</td><td rowspan=1 colspan=1>APAR</td><td rowspan=1 colspan=1>ARFU</td><td rowspan=1 colspan=1>RA</td></tr><tr><td rowspan=1 colspan=1>Default –No Repair</td><td rowspan=1 colspan=1>1111</td><td rowspan=1 colspan=1>C0</td><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>C2</td><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>C4</td><td rowspan=1 colspan=1>C5</td><td rowspan=1 colspan=1>C6</td><td rowspan=1 colspan=1>C7</td><td rowspan=1 colspan=1>APAR</td><td rowspan=1 colspan=1>ARFU</td><td rowspan=1 colspan=1>RA</td></tr><tr><td rowspan=1 colspan=13>NOTE 1XX = Lane is remapped</td></tr></table>

## 6.7.1.3 AWORD Remapping Examples

As an example, C0\_4 is the broken lane in the Column Command bus with no broken lanes on the Row Command bus. The lane is remapped by programming Channel $0 ^ { \circ } \mathrm { s }$ LANE REPAIR WDR bits AWORD\_CA[3:0] to $4 _ { \mathrm { h } }$ and AWORD\_RA[3:0] to $\mathrm { F _ { h } } .$

Table 51 — Original Lane Assignment - Channel 0 - AWORD Column Repair
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ARFU0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_7</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>co_0</td></tr><tr><td rowspan=1 colspan=1>RA0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>APAR0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_6</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>CK0_t</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_9</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_7</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>CK0_c</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_1</td></tr><tr><td rowspan=1 colspan=1>AERRO</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_8</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_6</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_2</td><td rowspan=1 colspan=1></td></tr></table>

Table 52 — Remapped Lane Assignment - Channel 0 - AWORD Column Repair
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>APAR0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_6</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_0</td></tr><tr><td rowspan=1 colspan=1>ARFU0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_7</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>CK0_t</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_9</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_7</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>CK0_c</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_1</td></tr><tr><td rowspan=1 colspan=1>AERRO</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_8</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_6</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_2</td><td rowspan=1 colspan=1></td></tr></table>

In a second example, R0\_0 is the broken lane in the Row Command bus with no broken lanes on the Column Command bus. The lane is remapped by programming Channel 0’s LANE REPAIR WDR bits AWORD\_RA[3:0] to $0 _ { \mathrm { h } }$ and AWORD\_CA[3:0] to F<sub>h</sub>.

## 6.7.1.3 AWORD Remapping Examples (cont’d)

Table 53 — Original Lane Assignment - Channel 0 - AWORD Row Repair
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ARFU0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_7</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_0</td></tr><tr><td rowspan=1 colspan=1>RA0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>APARO</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_6</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>CK0_t</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_9</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_7</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>CK0_c</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_1</td></tr><tr><td rowspan=1 colspan=1>AERRO</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_8</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_6</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_2</td><td rowspan=1 colspan=1></td></tr></table>

Table 54 — Remapped Lane Assignment - Channel 0 - AWORD Row Repair
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ARFU0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_7</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>co_0</td></tr><tr><td rowspan=1 colspan=1>R0_9</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>APARO</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_6</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>CK0_t</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>C0_1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_8</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_6</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>CK0_c</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_1</td></tr><tr><td rowspan=1 colspan=1>AERRO</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_7</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R0_2</td><td rowspan=1 colspan=1></td></tr></table>

## 6.7.2 DWORD Remapping

HBM4 supports remapping of one broken data bus lane per double byte. Two adjacent bytes (e.g., DQ[15:0], DQ[31:16], DQ[47:32], DQ[63:48]) are treated as a pair (double byte), but each double byte is treated independently.

After a lane is remapped, the input buffer associated with the broken lane is turned off and the output driver is tri-stated; the input buffer associated with the redundant lane (RD) is additionally turned on and the output driver is activated.

It is required to program “1111<sub>b</sub>” for the intact byte within the double byte while the remapping for the broken lane in the other byte is encoded according to the table.

DBI functionality is preserved as long as the Mode Register setting for DBI function is enabled. There is no impact on the Data Parity function. WDQS\_c, WDQS\_t, RDQS\_c, RDQS\_t, PAR and DERR signals cannot be remapped.

During Reads, the RD output drivers are enabled along with the DQ, DBI and ECC/SEV lanes of the physical byte the lane is located in: RD0 and RD2 are located within even bytes and thus enabled one WDQS cycle prior to the first valid data bit, and RD1 and RD3 are located within odd bytes and thus enabled two WDQS cycles prior to the first valid data bit.

## 6.7.2.1 DWORD Remapping Table

Table 55 — DWORD Remapping (1 Byte)
<table><tr><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>RegisterEncoding</td><td rowspan=1 colspan=1>ECC0(ECC1/SEVO/SEVI)</td><td rowspan=1 colspan=1>DQ0(DQ8/DQ16/DQ24)</td><td rowspan=1 colspan=1>DQ1(DQ9/DQ17/DQ25)</td><td rowspan=1 colspan=1>DQ2(DQ10/DQ18/DQ26)</td><td rowspan=1 colspan=1>DQ3(DQ11/DQ19/DQ27)</td><td rowspan=1 colspan=1>DQ4(DQ12/DQ20/DQ28)</td><td rowspan=1 colspan=1>DQ5(DQ13/DQ21/DQ29)</td><td rowspan=1 colspan=1>DQ6(DQ14/DQ22/DQ30)</td><td rowspan=1 colspan=1>DQ7(DQ15/DQ23/DQ31)</td><td rowspan=1 colspan=1>DBI0(DBI1/DBI2/DBI3)</td><td rowspan=1 colspan=1>RD0(RD0/RD1/RD1)</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 0</td><td rowspan=1 colspan=1>0000</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>ECC0</td><td rowspan=1 colspan=1>DQ0</td><td rowspan=1 colspan=1>DQ1</td><td rowspan=1 colspan=1>DQ2</td><td rowspan=1 colspan=1>DQ3</td><td rowspan=1 colspan=1>DQ4</td><td rowspan=1 colspan=1>DQ5</td><td rowspan=1 colspan=1>DQ6</td><td rowspan=1 colspan=1>DQ7</td><td rowspan=1 colspan=1>DBI0</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 1</td><td rowspan=1 colspan=1>0001</td><td rowspan=1 colspan=1>ECC0</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>DQ0</td><td rowspan=1 colspan=1>DQ1</td><td rowspan=1 colspan=1>DQ2</td><td rowspan=1 colspan=1>DQ3</td><td rowspan=1 colspan=1>DQ4</td><td rowspan=1 colspan=1>DQ5</td><td rowspan=1 colspan=1>DQ6</td><td rowspan=1 colspan=1>DQ7</td><td rowspan=1 colspan=1>DBI0</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 2</td><td rowspan=1 colspan=1>0010</td><td rowspan=1 colspan=1>ECC0</td><td rowspan=1 colspan=1>DQ0</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>DQ1</td><td rowspan=1 colspan=1>DQ2</td><td rowspan=1 colspan=1>DQ3</td><td rowspan=1 colspan=1>DQ4</td><td rowspan=1 colspan=1>DQ5</td><td rowspan=1 colspan=1>DQ6</td><td rowspan=1 colspan=1>DQ7</td><td rowspan=1 colspan=1>DBI0</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 3</td><td rowspan=1 colspan=1>0011</td><td rowspan=1 colspan=1>ECC0</td><td rowspan=1 colspan=1>DQ0</td><td rowspan=1 colspan=1>DQ1</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>DQ2</td><td rowspan=1 colspan=1>DQ3</td><td rowspan=1 colspan=1>DQ4</td><td rowspan=1 colspan=1>DQ5</td><td rowspan=1 colspan=1>DQ6</td><td rowspan=1 colspan=1>DQ7</td><td rowspan=1 colspan=1>DBI0</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 4</td><td rowspan=1 colspan=1>0100</td><td rowspan=1 colspan=1>ECC0</td><td rowspan=1 colspan=1>DQ0</td><td rowspan=1 colspan=1>DQ1</td><td rowspan=1 colspan=1>DQ2</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>DQ3</td><td rowspan=1 colspan=1>DQ4</td><td rowspan=1 colspan=1>DQ5</td><td rowspan=1 colspan=1>DQ6</td><td rowspan=1 colspan=1>DQ7</td><td rowspan=1 colspan=1>DBI0</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 5</td><td rowspan=1 colspan=1>0101</td><td rowspan=1 colspan=1>ECC0</td><td rowspan=1 colspan=1>DQ0</td><td rowspan=1 colspan=1>DQ1</td><td rowspan=1 colspan=1>DQ2</td><td rowspan=1 colspan=1>DQ3</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>DQ4</td><td rowspan=1 colspan=1>DQ5</td><td rowspan=1 colspan=1>DQ6</td><td rowspan=1 colspan=1>DQ7</td><td rowspan=1 colspan=1>DBI0</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 6</td><td rowspan=1 colspan=1>0110</td><td rowspan=1 colspan=1>ECC0</td><td rowspan=1 colspan=1>DQ0</td><td rowspan=1 colspan=1>DQ1</td><td rowspan=1 colspan=1>DQ2</td><td rowspan=1 colspan=1>DQ3</td><td rowspan=1 colspan=1>DQ4</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>DQ5</td><td rowspan=1 colspan=1>DQ6</td><td rowspan=1 colspan=1>DQ7</td><td rowspan=1 colspan=1>DBI0</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 7</td><td rowspan=1 colspan=1>0111</td><td rowspan=1 colspan=1>ECC0</td><td rowspan=1 colspan=1>DQ0</td><td rowspan=1 colspan=1>DQ1</td><td rowspan=1 colspan=1>DQ2</td><td rowspan=1 colspan=1>DQ3</td><td rowspan=1 colspan=1>DQ4</td><td rowspan=1 colspan=1>DQ5</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>DQ6</td><td rowspan=1 colspan=1>DQ7</td><td rowspan=1 colspan=1>DBI0</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 8</td><td rowspan=1 colspan=1>1000</td><td rowspan=1 colspan=1>ECC0</td><td rowspan=1 colspan=1>DQ0</td><td rowspan=1 colspan=1>DQ1</td><td rowspan=1 colspan=1>DQ2</td><td rowspan=1 colspan=1>DQ3</td><td rowspan=1 colspan=1>DQ4</td><td rowspan=1 colspan=1>DQ5</td><td rowspan=1 colspan=1>DQ6</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>DQ7</td><td rowspan=1 colspan=1>DBI0</td></tr><tr><td rowspan=1 colspan=1>Repair Lane 9</td><td rowspan=1 colspan=1>1001</td><td rowspan=1 colspan=1>ECC0</td><td rowspan=1 colspan=1>DQ0</td><td rowspan=1 colspan=1>DQ1</td><td rowspan=1 colspan=1>DQ2</td><td rowspan=1 colspan=1>DQ3</td><td rowspan=1 colspan=1>DQ4</td><td rowspan=1 colspan=1>DQ5</td><td rowspan=1 colspan=1>DQ6</td><td rowspan=1 colspan=1>DQ7</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>DBI0</td></tr><tr><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=1>1010to1110</td><td rowspan=1 colspan=1>ECC0</td><td rowspan=1 colspan=1>DQ0</td><td rowspan=1 colspan=1>DQ1</td><td rowspan=1 colspan=1>DQ2</td><td rowspan=1 colspan=1>DQ3</td><td rowspan=1 colspan=1>DQ4</td><td rowspan=1 colspan=1>DQ5</td><td rowspan=1 colspan=1>DQ6</td><td rowspan=1 colspan=1>DQ7</td><td rowspan=1 colspan=1>DBI0</td><td rowspan=1 colspan=1>RD0</td></tr><tr><td rowspan=1 colspan=1>Default -No Repair</td><td rowspan=1 colspan=1>1111</td><td rowspan=1 colspan=1>ECC0</td><td rowspan=1 colspan=1>DQ0</td><td rowspan=1 colspan=1>DQ1</td><td rowspan=1 colspan=1>DQ2</td><td rowspan=1 colspan=1>DQ3</td><td rowspan=1 colspan=1>DQ4</td><td rowspan=1 colspan=1>DQ5</td><td rowspan=1 colspan=1>DQ6</td><td rowspan=1 colspan=1>DQ7</td><td rowspan=1 colspan=1>DBI0</td><td rowspan=1 colspan=1>RD0</td></tr><tr><td rowspan=1 colspan=13>NOTE 1XX = Lane is remappedNOTE 2 DWORD0 and DWÓRD0_BYTE1 are shown as an exampleNOTE 3 ECC is associated with DWORD0_BYTE0,DWORD0_BYTE1, DWORD1_BYTE0 and DWORD1_BYTE1NOTE 4 SEV is associated with DWORD0_BYTE2,DWORD0_BYTE3, DWORD1_BYTE2 and DWORD1_BYTE3</td></tr></table>

## 6.7.2.2 DWORD Remapping Example

As an example, ECC0\_0 is a broken lane for byte 0 while all lanes for byte 1 are intact. The lane is remapped as illustrated in Table 57 by programming channel 0’s LANE REPAIR WDR bits DWORD0\_BYTE0[3:0] to 0<sub>h</sub> and bits DWORD0\_BYTE1[3:0] to F<sub>h</sub>.

Table 56 — Original DWORD Lane Assignment - Channel 0 – Byte [1:0]
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_7</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0 5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>RD0_0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ECCO_0</td></tr><tr><td rowspan=1 colspan=1>DBI0_0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_6</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DPARO_0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_0</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>VDDQL</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>VDDQL</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>VDDQL</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>VDDQL</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>VDDQL</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>VDDQL</td></tr><tr><td rowspan=1 colspan=1>DBI0_1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_14</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_12</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WDQS00t</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_10</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_8</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_15</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_13</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WDQS00c</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_11</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_9</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ECCO_1</td></tr></table>

Table 57 — Remapped DWORD Lane Assignment - Channel 0 – Byte [1:0]
<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_6</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DBI0_0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>XX</td></tr><tr><td rowspan=1 colspan=1>DQ0_7</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0 5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DPARO_0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ECCO_0</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>VDDQL</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>VDDQL</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>VDDQL</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>VDDQL</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>VDDQL</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>VDDQL</td></tr><tr><td rowspan=1 colspan=1>DBI0_1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_14</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_12</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WDQSO0t</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_10</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_8</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_15</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_13</td><td rowspan=1 colspan=1>C</td><td rowspan=1 colspan=1>WDQS00c</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_11</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DQ0_9</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ECCO_1</td></tr></table>

## 6.7.2.2 DWORD Remapping Example (cont’d)

The circuit diagram in Figure 70 illustrates the DQ lane remapping in more detail. Physical micro-bump DQ3 will be connected to internal logical DQ3 input and output paths when the DQ3 lane is not remapped; with remapping the internal DQ3 input and output paths would be routed to the physical DQ4 micro-bump.

![](images/3e5aef049dfd8ad56b3d4156f10b629ab849142dbbea28d6bd81694e34bef39f.jpg)  
Figure 70 — Example Signal Paths with Lane Repair

## 6.7.3 WSO Remapping

Unlike AWORD and DWORD repair, WSO remapping does not operate on an individual channel. There are two redundant WSO lanes (RM0 and RM1) in the IEEE 1500 interface to allow repair per Table 58.

RM0 is associated with the lower channel group which includes WSO[15:0]. RM1 is associated with the upper channel group which includes WSO[31:16]. After a lane is remapped, the output buffer associated with the broken lane is tristated and the output buffer associated with the redundant bump (RM) is activated. All functionalities are preserved with WSO lane remapping.

To repair a broken lane in the lower channel group, the host must program WIR[13:8] to $0 1 _ { \mathrm { h } }$ (Channel 1) and WIR[7:0] to either $1 2 _ { \mathrm { h } }$ or $1 3 _ { \mathrm { h } }$ depending on whether a hard or soft lane repair. To repair a broken lane in the upper channel group, the host must program WIR[13:8] to 11<sub>h</sub> (Channel 17) and WIR[7:0] to either $1 2 _ { \mathrm { h } }$ or1 $3 _ { \mathrm { h } }$ depending on whether a hard or soft repair. In either case, the WDR is then loaded using UpdateWR and the repair is completed after tSLREP/tHLREP as shown in Table 146.

Only one WSO can be repaired in each group. For example, RM0 and RM1 cannot be used to repair 2 WSO lanes in the lower channel group. If there is one broken WSO in both the upper and lower channel groups, they must be repaired one at a time in series using a separate Update WR event after tSLREP/tHLREP has expired.

For WSO hard lane repair, it is not permitted to repair a WSO lane using Channel 1 or 17 and another lane in the AWORD or DWORD on the same channel at the same time. The WDR loaded with UpdateWR to repair WSO must set the AWORD and DWORD bit fields to $\operatorname { F _ { h } }$ and the WSO[4:0] bit field to the lane to be repaired. Additional lanes in the AWORD or DWORD can be repaired using a separate UpdateWR event after tHLREP has expired. When the current instruction is a lane repair in Channel 1 or Channel 17’s AWORD or DWORD the WSO[4:0] WDR bit field must be programmed to $1 \mathrm { F _ { h } }$

For WSO soft lane repair, the bit field(s) for any AWORD or DWORD lane repair done prior to the W SO lane repair must be included in the WDR loaded with UpdateWR. The bit fields for any AWORD or DWORD not previously repaired must be set to $\operatorname { F } _ { \mathrm { h } } .$ . Conversely, any subsequent AWORD or DWORD soft lane repair initiated on Channel 1 or 17 using a separate UpdateWR event after tSLREP has expired must include the WSO lane repair bit fields with the previous repair. Failure to include previous repairs in subsequent soft lane repair WDR’s bit fields will result in the previous repairs being reverted or a new lane repaired.

6.7.3 WSO Remapping (cont’d)  
Table 58 — WSO Remapping
<table><tr><td rowspan=1 colspan=1>RepairLane #</td><td rowspan=1 colspan=1>RegisterEncoding</td><td rowspan=1 colspan=1>WS016(WSO0)</td><td rowspan=1 colspan=1>WSO17(WS01)</td><td rowspan=1 colspan=1>WSO18(WSO2)</td><td rowspan=1 colspan=1>WSO19(WSO3)</td><td rowspan=1 colspan=1>WSO20(WSO4)</td><td rowspan=1 colspan=1>WSO21(WSO5)</td><td rowspan=1 colspan=1>WSO22(WSO6)</td><td rowspan=1 colspan=1>WSO23(WSO7)</td><td rowspan=1 colspan=1>WSO24(WSO8)</td><td rowspan=1 colspan=1>WSO25(WSO9)</td><td rowspan=1 colspan=1>WS026(WS010)</td><td rowspan=1 colspan=1>WS027[(ws011)</td><td rowspan=1 colspan=1>WSO28(WS012)</td><td rowspan=1 colspan=1>WSO29(WS013)</td><td rowspan=1 colspan=1>WSO30(WSO14)</td><td rowspan=1 colspan=1>WSO31(WS015)</td><td rowspan=1 colspan=1>RM1(RM0)</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>00000</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>WS016</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>WSO18</td><td rowspan=1 colspan=1>WSO19</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>WSO25</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>WSO31</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>00001</td><td rowspan=1 colspan=1>WS016</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>WSO18</td><td rowspan=1 colspan=1>WSO19</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>WSO25</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>WSO31</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>00010</td><td rowspan=1 colspan=1>WSO16</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>WSO18</td><td rowspan=1 colspan=1>WSO19</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>WSO25</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>WSO31</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>00011</td><td rowspan=1 colspan=1>WS016</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>WSO18</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>WS019</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>WSO25</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>WSO31</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>00100</td><td rowspan=1 colspan=1>WS016</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>WSO18</td><td rowspan=1 colspan=1>WSO19</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>WSO25</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>WSO31</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>00101</td><td rowspan=1 colspan=1>WSO16</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>WS018</td><td rowspan=1 colspan=1>WSO19</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>WSO25</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>WSO31</td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>00110</td><td rowspan=1 colspan=1>WSO16</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>WSO18</td><td rowspan=1 colspan=1>WSO19</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>WSO25</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>WSO31</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>00111</td><td rowspan=1 colspan=1>WS016</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>WSO18</td><td rowspan=1 colspan=1>WSO19</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>WSO25</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>WSO31</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>01000</td><td rowspan=1 colspan=1>WSO16</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>WSO18</td><td rowspan=1 colspan=1>WSO19</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>WSO25</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>WSO31</td></tr><tr><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>01001</td><td rowspan=1 colspan=1>WS016</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>WSO18</td><td rowspan=1 colspan=1>WSO19</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>WSO25</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>WSO31</td></tr><tr><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>01010</td><td rowspan=1 colspan=1>WSO16</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>WSO18</td><td rowspan=1 colspan=1>WSO19</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>WSO25</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>WSO31</td></tr><tr><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>01011</td><td rowspan=1 colspan=1>WS016</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>WSO18</td><td rowspan=1 colspan=1>WSO19</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>WSO25</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>WSO31</td></tr><tr><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>01100</td><td rowspan=1 colspan=1>WS016</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>WSO18</td><td rowspan=1 colspan=1>WSO19</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>WSO25</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>WSO31</td></tr><tr><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>01101</td><td rowspan=1 colspan=1>WSO16</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>WSO18</td><td rowspan=1 colspan=1>WSO19</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>WSO25</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>WSO31</td></tr><tr><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>01110</td><td rowspan=1 colspan=1>WSO16</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>WSO18</td><td rowspan=1 colspan=1>WSO19</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>WSO25</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>WSO31</td></tr><tr><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>01111</td><td rowspan=1 colspan=1>WS016</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>WS018</td><td rowspan=1 colspan=1>WSO19</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>WS025</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1>WSO31</td></tr><tr><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=1>10000to11110</td><td rowspan=1 colspan=1>WSO16</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>WSO18</td><td rowspan=1 colspan=1>WS019</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>WSO25</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>WSO31</td><td rowspan=1 colspan=1>RM1</td></tr><tr><td rowspan=1 colspan=1>Default No Repair</td><td rowspan=1 colspan=1>11111</td><td rowspan=1 colspan=1>WS016</td><td rowspan=1 colspan=1>WS017</td><td rowspan=1 colspan=1>WS018</td><td rowspan=1 colspan=1>WSO19</td><td rowspan=1 colspan=1>WSO20</td><td rowspan=1 colspan=1>WSO21</td><td rowspan=1 colspan=1>WSO22</td><td rowspan=1 colspan=1>WSO23</td><td rowspan=1 colspan=1>WSO24</td><td rowspan=1 colspan=1>WSO25</td><td rowspan=1 colspan=1>WSO26</td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1>WSO31</td><td rowspan=1 colspan=1>RM1</td></tr><tr><td rowspan=1 colspan=19>NOTE 1 XX = Lane is remapped</td></tr></table>

## 6.7.3 WSO Remapping (cont’d)

As an example, WSO29 is the broken lane in the midstack. The lane is remapped by programming Channel 17’s LANE\_REPAIR\_WDR bits WSO[4:0] to D<sub>h</sub>.

Table 59 — Original Lane Assignment – WSO Repair
<table><tr><td rowspan=1 colspan=1>RM1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WSO31</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WSO26</td></tr></table>

Table 60 — Remapped Lane Assignment – WSO Repair
<table><tr><td rowspan=1 colspan=1>WSO31</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WSO30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WSO29</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>XX</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WSO28</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WSO27</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WSO26</td></tr></table>

A Multiple-input Shift Register (MISR) / Linear Feedback Shift Register (LFSR) circuit is defined within the HBM4 AWORD and DWORD I/O blocks. These circuits are intended for testing and training the link between the Host and the HBM4 device. Referring to Figure 71, each byte within a DWORD implements a 40-bit MISR/LFSR circuit, comprised of WDQS 2-cycles Rise and Fall 4-bits for each of the eight DQs plus DBI and ECC/SEV signals. Respective Q0, Q1, Q2, Q3 indicate half WDQS cycle for each one signal within each byte of a DWORD implement. The BL0 to BL3 of HBM4 are matched with the Q0 to Q3 in the front two WDQS cycles and the BL4 to BL7 of HBM4 are matched with the Q0 to Q3 in the next two WDQS cycles. In operation, the MISR/LFSR circuits operate independently across the bytes. The AWORD implements a 38-bit MISR/LFSR circuit comprised of CK DDR Rise and Fall bits for the 18 row and column command bits, plus ARFU. When the MISR registers are read via the IEEE 1500 port DWORD\_MISR instruction, the four bytes per DWORD (160-bits) for the two DWORDs within a channel are serially shifted out, for a total of 320-bits. The 38-bit AWORD MISR content is read via the AWORD\_MISR instruction. See Table 128 and Table 129 for the bit-orders for these MISR registers.

The term MISR modes collectively refers to all of the modes - LFSR mode, Register mode, MISR mode, and LFSR Compare mode. AWORD MISR modes and DWORD MISR modes refer to all of the modes defined for the specific bus.

![](images/50687642d32735de924e236882023d887865d020d9dc6ac82378b3e5910c6f22.jpg)  
Figure 71 — MISR Features Block Diagram of HBM4

## 6.8.1 HBM4 Polynomial Structure

Figure 72 provides an example of a 4-bit Galois type MISR/LFSR structure that implements the following polynomial:

$$
\mathbf { f ( x ) } = \mathbf { X ^ { 4 } } + \mathbf { X ^ { 3 } } + 1
$$

The example circuit and function table are for illustration only, and this circuit's modes are not fully representative of the actual DWORD and AWORD MISR definitions as outlined below. For example, the circuit shown in Figure 72 implements a reset function, while the AWORD and DWORD MISRs instead implement a preset function, where specific bits are set to logic 1.

![](images/28116631342e2079ee371fc80271fdeb116ee023f79db1a93a05bada794d7c00.jpg)  
Figure 72 — Example of 4 bit MISR-LFSR Implementing ${ \bf f ( x ) } = { \bf X ^ { 4 } } + { \bf X ^ { 3 } } + { \bf 1 }$

Table 61 — MISR Function Table
<table><tr><td rowspan=1 colspan=1>M1</td><td rowspan=1 colspan=1>MO</td><td rowspan=1 colspan=1>Function</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Reset</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>LFSR</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Register</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>MISR</td></tr></table>

## 6.8.1.1 AWORD MISR Polynomial

The HBM4 AWORD MISR structure is a 38-bit MISR/LFSR with the following polynomial:

$$
\mathbf { f } ( \mathbf { x } ) = \mathbf { X } ^ { 3 8 } + \mathbf { X } ^ { 6 } + \mathbf { X } ^ { 5 } + \mathbf { X } + 1
$$

The AWORD MISR may be serially accessed via the AWORD\_MISR IEEE 1500 port instruction. See Table 129 for the AWORD MISR wrapper data register bit order.

## 6.8.1.2 DWORD MISR Polynomial

The DWORD MISR structure is a 40-bit MISR/LFSR per byte with the following polynomial:

$$
\mathrm { f ( x ) } = \mathrm { X } ^ { 4 0 } + \mathrm { X } ^ { 3 8 } + \mathrm { X } ^ { 2 1 } + \mathrm { X } ^ { 1 9 } + 1
$$

Note that when the DWORD MISRs are accessed via the DWORD\_MISR IEEE 1500 port instructions that all of the individual byte MISRs within a channel are concatenated into a 320-bit wrapper data register. See Table 128 for the DWORD MISR bit order.

## 6.8.2 General Loopback Modes Features and Behavior

This clause addresses features and behaviors that generally apply to all of the MISR modes.

a) Entering the MISR modes – MISR modes may be enabled after tINIT3 within the initialization sequence; they may also be entered any time after completing the initialization (see Initialization section). DWORD MISR modes are controlled via MR7 OP[5:3] (see Table 17), while AWORD MISR modes are controlled via the IEEE 1500 port AWORD MISR CONFIG instruction. AWORD and DWORD MISR modes cannot be used simultaneously since the DWORD MISR modes are driven via READ and WRITE commands on the AWORD bus.

b) Entering and exiting AWORD MISR modes – HBM4 allows the AWORD MISR modes to be utilized on one or more channels while the other channels continue to operate normally. After normal initialization, to enter the AWORD MISR modes on a given channel the host must put the HBM4 channel into either precharge power-down or self refresh modes. Self refresh mode may be used in order to retain memory content while using the AWORD MISR modes, as needed. AWORD MISR modes may also be enabled after tINIT4 within the initialization sequence. Enabling the AWORD MISR modes re-enables the AWORD I/O buffers that are normally disabled in power-down and self refresh modes, which may result in increased current draw over the IDD2P, IDD2P0 and IDD6x specifications. If returning to normal operation is not required, the host may assert an initialization sequence per section Initialization after operating the AWORD MISR modes. The sequence for entering AWORD MISR modes, and then exiting back to normal operation is as follows:

1) At any time after initializing, the HBM4 enters the all banks idle state.

2) Enter either the precharge power-down state or the self refresh state. R0 = LOW while in these states.

3) Stop toggling CK (CK\_t = LOW, CK\_c = HIGH).

4) Enable/enter and operate the AWORD MISR modes (AWORD\_MISR\_CONFIG Enable = 1 - On). Finish these operations with CK stopped (CK\_t = LOW, CK\_c = HIGH) and R0 = LOW.

5) Disable the AWORD MISR modes and follow the Power-Down (PDE, PDX) or Self Refresh (SRE, SRX) exit procedures.

6) When using the AWORD MISR modes after t<sub>INIT3</sub> within the initialization sequence, powerdown or self refresh entry and exit do not apply.

If the DRAM is not required to continue with mission mode operation after AWORD MISR test, there is no requirement on row/column command bus and the precharge power-down state or the self refresh state after loopback test. The AWORD MISR modes (AWORD\_MISR\_CONFIG Enable bit) can be reset by WRST\_n during a subsequent initialization sequence.

c) Entering and exiting DWORD MISR modes – HBM4 allows the DWORD MISR modes to be utilized on one or more channels while the other channels continue to operate normally. After normal initialization (see Initialization), to enter the DWORD MISR modes on a given channel the host must put the HBM4 channel into the all banks idle, enable the DWORD MISR modes (MR7 Loopback Enable = 1 - Enable; see Table 17), and then enter precharge power-down or self refresh. Self refresh may be used in order to retain memory content while using the DWORD MISR modes, as needed. Enabling the DWORD MISR modes before entering precharge power-down or self refresh keeps the AWORD and DWORD I/O buffers enabled, and may result in increased current draw over the IDD2P, IDD2P0 and IDD6x specifications. DWORD MISR modes may also be enabled after t<sub>INIT3</sub> within the initialization sequence. Also see items f) and h) for related DWORD MISR modes configuration setting. On the column command bus only READ (RD), WRITE (WR), and Column No Operation (CNOP) commands may be issued which operate the DWORD MISR modes, MR6 MRS commands may be issued to set the DWORD driver strengths, MR10 MRS commands may be issued to set the DWORD DCA codes for RDQS, MR11 MRS commands may be issued to set the DWORD DCA codes for WDQS, MR14 MRS commands may be issued to set the DWORD VREF (VREFD), optionally (see DEVICE\_ID[172]) MR18 MRS commands may be issued to set the PC1 DWORD VREF (VREFD), MR15 MRS commands may be issued to set the DWORD DFE codes, and MR7 MRS commands may be issued to select the DWORD MISR modes. On the row command bus only R0 = static LOW may be issued. The sequence for entering DWORD MISR modes, and then exiting back to normal operation is as follows:

1) At any time after initializing, the HBM4 enters the all banks idle state.

2) Set all configuration mode registers as needed for use in the DWORD MISR modes (see items h), k), and n)).

3) Set MR7 DWORD Loopback Enable = 1 - Enable, and then wait t<sub>MOD</sub>.

4) Enter either precharge power-down or self refresh. R0 = LOW while in these states.

5) Select and operate the DWORD MISR modes via MR7 settings (Row command input requires RNOP with R0 = L to keep power-down or self refresh status during MR7 setting) and sending RD, WR, and CNOP commands. After completing DWORD MISR operations, send CNOP commands.

6) Follow the power-down exit (PDX) or self refresh exit (SRX) procedures.

7) Set MR7 DWORD Loopback Enable = 0 - Disable, and then wait t<sub>MOD</sub> before continuing normal operation.

MRS commands are not supported until after t<sub>INIT5</sub> in the initialization sequences; therefore, to configure and control the mode registers for DWORD MISR modes usage after t<sub>INIT3</sub> the MODE\_REGISTER\_DUMP\_SET instruction must be used. The sequence for entering and operating the DWORD MISR modes after t in the initialization sequence is as follows:

1) Start CK with PD and CNOP on the command buses.

2) Using MODE\_REGISTER\_DUMP\_SET sets all configuration mode registers as needed for use in the DWORD MISR modes (see items f) and h)), set MR7 DWORD Loopback Enable = 1 - Enable, and then wait t .

3) Select and operate the DWORD MISR modes via MR7 settings (using MODE\_REGISTER\_- DUMP\_SET) and sending RD, WR, and CNOP commands.

4) After completing DWORD MISR operations, send CNOP commands, set MR7 DWORD Loopback Enable = 0 - Disable using MODE\_REGISTER\_DUMP\_SET, then wait t<sub>MOD</sub>.

5) CK clocking may be stopped if desired.

## 6.8.2 General Loopback Modes Features and Behavior (cont’d)

6) Proceed to other IEEE 1500 instructions, or proceed with the initialization sequence from Figure 7 time Td.

If the DRAM is not required to continue with mission mode operation after DWORD MISR test, there is no requirement to follow the power-down or self refresh procedures and set MR7 DWORD Loopback Enable = 0 - Disable. The Loopback Enable bit can be reset by a subsequent initialization sequence with RESET\_n = LOW.

d) Command decode is disabled in AWORD MISR modes - When AWORD MISR modes are enabled the traffic sent on the AWORD bus is not limited to valid commands. To prevent undefined states and operations, when AWORD MISR modes are enabled (AWORD MISR CONFIG Enable = 1 - On), command decoding is disabled.

e) With lane repairs the MISR bit positions remain with their logical signals - The MISR bits are associated with their logic signals, not the physical microbumps (see Figure 70). For example, if DQ3 has been repaired (which routes the DQ3 data to the DQ4 microbump) the data received on the DQ4 microbump is routed to the DQ3 MISR bits. Effectively, the behaviors for all MISR modes are unchanged - all 10 bits of the byte are captured in the MISR in the same bit locations, as if no lane repair were active.

f) HBM4 DBI, and ECC/SEV logic circuits are not functional in the DWORD MISR modes - The DBI and ECC/SEV signals are treated as pure data signals. Their raw values are captured, compared, or sent without regard to their normal bus inversion or ECC functional meaning.

• It is required to enable Write DBIac and Read DBIac in MR0 in order to enable the I/O buffers on the DBI signals. A value of 0 is internally assumed for all DBI write data in case WDBI is disabled.

Regardless whether meta data and severity reporting are enabled in MR9 or not, setting MR7 DWORD Loopback Enable = 1 will enable the ECC/SEV signal’s I/O buffers. Note that the SEV signals are bidirectional I/Os in loopback test mode only.

If Write Parity (WPAR) is enabled by MR0 OP5 (Table 10), then the Write DBIac (MR0 OP1) and Meta Data (MP9 OP0) shall also be enabled to ensure ECC and Write DBI inputs are correctly evaluated during parity checking. (Table 62)

## 6.8.2 General Loopback Modes Features and Behavior (cont’d)

Table 62 — WDBI, ECC, and SEV Signals during Loopback and Normal Mission Modes
<table><tr><td rowspan=2 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>WPAR Off (MR0 OP5=0)</td><td rowspan=1 colspan=2>WPAR On (MR0 OP5=1)</td></tr><tr><td rowspan=1 colspan=1>MR0 OP1</td><td rowspan=1 colspan=1>WDBIReceiver State</td><td rowspan=1 colspan=1>WR Parity</td><td rowspan=1 colspan=1>WDBIReceiver State</td><td rowspan=1 colspan=1>WR Parity</td></tr><tr><td rowspan=2 colspan=1>MissionMode</td><td rowspan=1 colspan=1>WDBI On</td><td rowspan=1 colspan=1>ON (0 or 1)</td><td rowspan=1 colspan=1>No ParityChecking</td><td rowspan=1 colspan=1>ON (0 or 1)</td><td rowspan=1 colspan=1>Includedin Parity Check</td></tr><tr><td rowspan=1 colspan=1>WDBI Off</td><td rowspan=1 colspan=1>OFF</td><td rowspan=1 colspan=1>No ParityChecking</td><td rowspan=1 colspan=1>OFF</td><td rowspan=1 colspan=1>Not Includedin Parity Check</td></tr><tr><td rowspan=2 colspan=1>LoopbackMode</td><td rowspan=1 colspan=1>WDBI On</td><td rowspan=1 colspan=1>ON (0 or 1)</td><td rowspan=1 colspan=1>No ParityChecking</td><td rowspan=1 colspan=1>ON (0 or 1)</td><td rowspan=1 colspan=1>Includedin Parity Check</td></tr><tr><td rowspan=1 colspan=1>WDBI Off</td><td rowspan=1 colspan=1>OFF</td><td rowspan=1 colspan=1>No ParityChecking</td><td rowspan=1 colspan=1>Not Allowed</td><td rowspan=1 colspan=1>Not Allowed</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>MR9 OP0</td><td rowspan=1 colspan=1>ECCReceiver State</td><td rowspan=1 colspan=1>WR Parity</td><td rowspan=1 colspan=1>ECCReceiver State</td><td rowspan=1 colspan=1>WR Parity</td></tr><tr><td rowspan=2 colspan=1>MissionMode</td><td rowspan=1 colspan=1>ECC On</td><td rowspan=1 colspan=1>ON (0 or 1)</td><td rowspan=1 colspan=1>No ParityChecking</td><td rowspan=1 colspan=1>ON (0 or 1)</td><td rowspan=1 colspan=1>Includedin Parity Check</td></tr><tr><td rowspan=1 colspan=1>ECC Off</td><td rowspan=1 colspan=1>OFF</td><td rowspan=1 colspan=1>No ParityChecking</td><td rowspan=1 colspan=1>OFF</td><td rowspan=1 colspan=1>Not Includedin Parity Check</td></tr><tr><td rowspan=2 colspan=1>LoopbackMode</td><td rowspan=1 colspan=1>ECC On</td><td rowspan=1 colspan=1>ON (0 or 1)</td><td rowspan=1 colspan=1>No ParityChecking</td><td rowspan=1 colspan=1>ON (0 or 1)</td><td rowspan=1 colspan=1>Includedin Parity Check</td></tr><tr><td rowspan=1 colspan=1>ECC Off</td><td rowspan=1 colspan=1>ON (0 or 1)</td><td rowspan=1 colspan=1>No ParityChecking</td><td rowspan=1 colspan=1>Not Allowed</td><td rowspan=1 colspan=1>Not Allowed</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>MR9 OP1</td><td rowspan=1 colspan=1>SEVReceiver State</td><td rowspan=1 colspan=1>WR Parity</td><td rowspan=1 colspan=1>SEVReceiver State</td><td rowspan=1 colspan=1>WR Parity</td></tr><tr><td rowspan=2 colspan=1>MissionMode</td><td rowspan=1 colspan=1>SEV On</td><td rowspan=1 colspan=1>OFF</td><td rowspan=1 colspan=1>No ParityChecking</td><td rowspan=1 colspan=1>OFF</td><td rowspan=1 colspan=1>Not Includedin Parity Check</td></tr><tr><td rowspan=1 colspan=1>SEV Off</td><td rowspan=1 colspan=1>OFF</td><td rowspan=1 colspan=1>No ParityChecking</td><td rowspan=1 colspan=1>OFF</td><td rowspan=1 colspan=1>Not Includedin Parity Check</td></tr><tr><td rowspan=2 colspan=1>LoopbackMode</td><td rowspan=1 colspan=1>SEV On</td><td rowspan=1 colspan=1>ON (0 or 1)</td><td rowspan=1 colspan=1>No ParityChecking</td><td rowspan=1 colspan=1>ON (0 or 1)</td><td rowspan=1 colspan=1>Not Includedin Parity Check</td></tr><tr><td rowspan=1 colspan=1>SEV Off</td><td rowspan=1 colspan=1>ON (0 or 1)</td><td rowspan=1 colspan=1>No ParityChecking</td><td rowspan=1 colspan=1>ON (0 or 1)</td><td rowspan=1 colspan=1>Not Includedin Parity Check</td></tr></table>

• The host may write DBI encoded or non-encoded data to the HBM4. In MISR mode or Register mode, the raw data received from the host will be directly captured (not DBI decoded) to the MISR register.

• For LFSR Compare mode to match, the host must send the LFSR generated raw data on all 10 signals of the byte without write DBI encoding. The HBM4 will not DBI decode the received data, and thus the host must send the raw LFSR data in order for LFSR Compare to match.

• For LFSR mode, the HBM4 will generate non-DBI encoded read data.

## 6.8.2 General Loopback Modes Features and Behavior (cont’d)

g) DWORD read path parity traffic generation - In DWORD LFSR mode (Read direction) and Read Register mode, the HBM4 parity logic is not active and the MR0 DQ Bus Read Parity settings have no effect. To generate traffic on the DWORD parity signal a copy of a nearby DQ signal is produced on the Parity signal. Logical signals DQ2, DQ34 are sent on the respective DWORD block parity DPAR0, DPAR1 signals, irrespective of any lane repairs. The parity signals are driven with the DQ data without any additional cycle delay - effectively with Parity Latency = 0. A suggested host-side implementation is to use signature register circuits for checking the validity of the received parity signal. When reading back the LFSR\_COMPARE\_STICKY error bits, the parity signal output is unspecified.

h) AWORD and DWORD write parity checking - In AWORD and DWORD Register mode, MISR mode, and LFSR Compare mode the HBM4 parity evaluation logic is active and outputs results on AERR after t<sub>PARAC</sub> and DERR after t<sub>PARDQ</sub>, respectively (if enabled in MR0, see Table 10). The MR1 Parity Latency setting (see Table 11) must be set to a vendor implementation-specific supported PL value, which may be interface speed specific. The HBM4 device will process write parity per the PL setting and protocol, including any required additional WDQS cycles. A suggested host-side implementation is to use signature register circuits for checking the correctness of the AERR and DERR signals. It is also suggested that the host generates data on the DWORD Parity signals in order to exercise these signal paths and logic.

i) Preset state AAAAAAAAAA and 2AAAAAAAAA - The Preset state for the DWORD MISR registers is AAAAAAAAAA , which initializes the Rise bit for each signal to 1'b1 and the Fall bit to 1'b0. This is a useful state for producing an alternating 0/1/0/1/0/1/0/1 pattern on all 10 bits associated with a DWORD byte when put into DWORD read Register mode (burst length 8). This basic pattern may be used by the host for RDQS eye centering. READ commands from the DWORD\_MISR are supported in Preset state. WRITE and READ commands to and from the DWORD\_MISR do not change the DWORD\_MISR content in this mode. The AWORD MISR register is also preset to the same 0/1 pattern (0x2AAAAAAAAA<sub>h</sub> for the 38-bit polynomial) for implementation consistency; although the AWORD cannot be enabled to drive this data pattern back to the host. Any non-zero initialization pattern is sufficient for all of the MISR modes; however, an initial pattern of all zeroes is a stuck-at-zero state for the DWORD LFSR mode. The Preset state may be overridden using the Write Register modes (see AWORD and DWORD Write Register Modes).

j) DWORD MISR registers are writeable via IEEE 1500 - The normal intended method for writing the DWORD MISR registers are through the functional interface (see Test Method for DWORD Write MISR mode). The values of the DWORD MISR registers may also be written using the DWORD\_MISR IEEE 1500 port instruction. This feature enables setting alternate seed values.

k) DWORD read and write latencies must be set properly - READ and WRITE commands are used to generate DWORD MISR modes traffic. Normal mode DWORD read and write protocol is followed using the latency settings, as supported by the operating frequency being used.

l) DWORD Write preamble and post-amble clocks adhere to the normal protocol - For DWORD write MISR modes (Register mode, MISR mode, and LFSR Compare mode), the host is expected to send WDQS preamble and postamble clocks, and the HBM4 samples the DWORD data, consistent with the write protocols defined in the clause entitled Write Command (WR, WRA).

![](images/89180df0c57a1a26f6e1a88bb23ccfffacf17532d2f53cbd47d594ab9cae3214.jpg)  
Figure 73 — AWORD MISR Modes Preamble Clock Filter Behavior

## 6.8.2 General Loopback Modes Features and Behavior (cont’d)

m) DWORD Read preamble and post-amble clocks adhere to the normal protocol - For DWORD Read Register mode, LFSR mode (Read direction), and when returning the LFSR\_COMPARE STICKY bits, the HBM4 will produce RDQS preamble and postamble clocks, and send DWORD data, consistent with the read protocols defined in the clause entitled Read Command (RD, RDA).

n) AWORD MISR modes preamble clock filter - In the AWORD MISR modes, the host is expected to stop CK toggling, enable the desired AWORD MISR mode, and then start sending CK toggles and AWORD data. To avoid timing impairment on the CK startup cycle, the HBM4 will treat the first received CK cycle as a preamble clock cycle and not process the data on the AWORD signals in MISR or Register mode, nor compare them in LFSR Compare mode. The MISR block will keep its state unchanged during filter cycle. The first clock cycle filter circuit is enabled by setting AWORD\_MISR\_CONFIG MODE = 2’b00 - Preset. The first data sampled by the HBM4 is on the second CK clock cycle. Only the very first CK clock cycle will be filtered - if the host were to stop and restart CK clocking while remaining in an AWORD MISR mode (without applying another Preset), the AWORD data will be sampled on the startup clock cycle, with possible CK edge timing impairment.

o) Cycles processed in the MISR modes - AWORD MISR modes rely on stopping CK clocks before and after the test sequence. All AWORD cycles sent to the HBM4 after the filtered preamble clock cycle are processed into the MISR (MISR mode and Register mode) or compared (LFSR Compare mode), including the last cycle before CK is stopped. An even number of AWORD cycles – not counting the filtered preamble cycle – provides that the test results is the same regardless of the specific AWORD MISR implementation. For DWORD MISR modes, all valid data cycles written to the HBM4 are processed into the MISR (MISR mode and Register mode) or compared (LFSR Compare mode) while the DWORD MISR modes are enabled, consistent with the DWORD write protocol and write latency setting. Data pin signal states during preamble and post-amble cycles are not processed into the MISR. For example, if 10 non-seamless Burst Length = 8 write operations are sent to the HBM4 in DWORD MISR mode a total of 80 data bit times (UI) will be processed into the MISR.

## 6.8.3 AWORD and DWORD Write MISR Modes

When the AWORD or DWORD MISR modes are active, the data on the AWORD or DWORD data signals is received based on the CK or WDQS clocks respectively, and compressed in the MISR circuits. The host is in complete control of the number of data cycles that are sent, and if successfully received by the HBM4 the values captured in the respective MISRs will be repeatable and deterministic. Figure 74 illustrates the behavior for DWORD MISR mode (Write direction).

![](images/3ca6deeab1ad6c1fbba89b51a3bce2a3f66518a2ef7ddfd54e7819954d3377a8.jpg)  
Figure 74 — DWORD Write MISR Modes Behavior

## 6.8.3.1 Test Method for AWORD (Write) MISR Mode

a) After the required HBM4 initialization, the host issues either precharge power-down or self refresh mode (R0 = LOW) and stops sending CK clocks to the HBM4 (CK\_t = LOW, CK\_c = HIGH).

b) Initialize the AWORD MISR by setting the AWORD\_MISR\_CONFIG Enable = 1'b1 - On and AWORD\_MISR\_CONFIG MODE = 2’b00 - Preset. The Preset operation also enables the preamble clock filter circuit.

c) Enable the AWORD MISR mode by setting AWORD\_MISR\_CONFIG Mode = 2'b11 - MISR mode.

d) The host sends three or more CK clock cycles and data on the AWORD signals. The first received CK clock cycle is discarded as a preamble clock by the HBM4 and shall be followed by an even number of clock cycles. The HBM4 clocks the received data into the AWORD MISR and evaluates parity, if enabled. The ending clock state applied by the host is CK\_t = LOW, CK\_c = HIGH.

e) The host reads the MISR content via the IEEE 1500 AWORD\_MISR instruction.

## 6.8.3.2 Test Method for DWORD Write MISR Mode

a) Initialize the test sequence by setting MR7 DWORD Loopback Enable = 1'b1 - Enable and presetting the MISR registers by setting the DWORD MISR Control = 3'b000 - Preset. The controller can load the DWORD MISR registers with an alternate seed value via the functional interface or IEEE 1500 (see AWORD and DWORD Write Register Modes and DWORD\_MISR IEEE1500 port instruction).

b) The host issues either precharge power-down or self refresh mode (R0=Low).

c) Enable DWORD MISR mode by setting MR7 DWORD MISR Control = 3'b011 - MISR mode.

d) The host sends one or more DWORD write cycles following the write latency and burst length setting and following the normal write protocol. The HBM4 clocks the received data into the DWORD MISRs and evaluates parity, if enabled.

e) The host reads the MISR content via the IEEE 1500 DWORD\_MISR instruction. The MISR content is also readable via the functional interface (see DWORD Read Register Mode).

## 6.8.4 AWORD and DWORD Write Register Modes

When the AWORD or DWORD Register modes are active, the data on the AWORD or DWORD data signals are received based on the CK or WDQS clocks respectively, and stored directly into the respective MISR registers without compression. Effectively the MISR register operates as a 2-bit storage register for AWORD and as a 4-bit storage register for DWORD. On rising CK or WDQS edges the signal states on the AWORD or DWORD bus respectively are stored in the Rising bits within the MISR registers, and on falling CK or WDQS edges the bus signal states are stored in the Falling bits within the MISR registers. If the host sends multiple DDR cycles to the HBM4, the MISRs will contain the last 2-bit per AWORD MISR cycle and 4-bit per DWORD MISR cycle, if successfully received by the HBM4.

The Register modes are intended for basic, quick link testing and training, and for initializing the DWORD MISR seed values.

## 6.8.4.1 Test Method for AWORD (Write) Register Mode

a) After the required HBM4 initialization, the host issues either precharge power-down or self refresh mode (R0 = LOW) and stops sending CK clocks to the HBM4 (CK\_t = LOW, CK\_c = HIGH).

b) Initialize the AWORD MISR by setting the AWORD\_MISR\_CONFIG Enable = 1'b1 - On and AWORD\_MISR\_CONFIG MODE = 2’b00 - Preset. The Preset operation enables the preamble clock filter circuit.

c) Enable the AWORD Register mode by setting AWORD\_MISR\_CONFIG MODE = 2’b10 – Register mode.

d) The host sends two or more CK clock cycles and data on the AWORD signals. The first received CK clock cycle is discarded as a preamble clock by the HBM4. The HBM4 clocks the raw received data into the AWORD MISR register without MISR compression and evaluates parity, if enabled. The ending clock state applied by the host is CK\_t = LOW, CK\_c = HIGH. The last clocked DDR cycle data is retained in the AWORD MISR register.

e) The host reads the MISR content via the IEEE 1500 AWORD\_MISR instruction.

## 6.8.4.1 Test Method for AWORD (Write) Register Mode (cont’d)

Note that the AWORD write register mode cannot practically be used to apply an alternate seed value into the AWORD MISR register. In clause Test Method for AWORD (Write) Register Mode step d, the preamble clock filter circuit is exercised and cleared. At this point while it is allowed for the host to then stop sending AWORD cycles, set the AWORD\_MISR\_CONFIG MODE to MISR mode or LFSR Compare mode, and then send additional AWORD cycles, there may be timing impairment for the beginning of the second set of AWORD cycles.

The preamble clock filter circuit cannot be re-enabled for these additional AWORD cycles without applying the AWORD MISR Preset function, which would also overwrite the alternate seed value applied by the AWORD write register operation. There is no expected application value for using an alternate MISR seed value for the AWORD MISR functions since the AWORD bus is receive-only.

## 6.8.4.2 Test Method for DWORD Write Register Mode

a) Enable DWORD Register mode by setting MR7 DWORD Loopback Enable = 1'b1 - Enable and DWORD MISR Control = 3'b010 - Register mode. A Preset is not required prior to using Register mode.

b) The host issues either precharge power-down or self refresh mode (R0=Low).

c) The host sends one or more DWORD write cycles following the write latency and burst length setting and following the normal write protocol. The HBM4 clocks the raw received data into the DWORD MISR registers without MISR compression and evaluates parity, if enabled. The last clocked DDR cycle data is retained in the DWORD MISR registers.

d) The host reads the MISR content via the IEEE 1500 DWORD\_MISR instruction. The MISR content is also readable via the functional interface (see DWORD Read Register Mode).

## 6.8.5 DWORD Read Register Mode

The content of various DWORD MISR mode related registers may be read over the functional interface, assuming that the read path with the host is properly trained (or used for read path training). The MR7 DWORD Read Mux Control bit field is used to select the data source. The host issues read commands and the HBM4 responds following the read command protocol (such as read latency and burst length) and timing (such as pre and post-amble clocks) per Read Command (RD, RDA).

Intended uses for the various read data sources include the following:

Reading the sticky error bits after an LFSR Compare mode test sequence (DWORD Read Mux Control = 1'b1 - Return LFSR\_COMPARE\_STICKY) - Sticky error data is a single data bit per signal and is output as static values on the interface for the full read burst length.

• NOTE: When using the LFSR mode (see DWORD Read LFSR Mode) set the DWORD Read Mux Control = 1'b0 - Return data from DWORD MISR registers.

Reading a basic clock pattern on all or select signals for DWORD read link training (DWORD Read Mux Control = 1'b0 - Return data from DWORD MISR registers) - Which signals toggle may be set with the Preset mode or a DWORD Register write (see AWORD and DWORD Write Register Modes).

Reading the MISR registers final values at the end of a MISR mode test sequence (DWORD Read Mux Control = 1'b0 - Return data from DWORD MISR registers) - The results of a MISR mode test sequence may be read back on the functional interface, or via the IEEE 1500 port DWORD\_MISR instruction. The MISR content is sent on UI 0 - 3 and then repeated on UI 4 – 7, or all data(UI 0 to 7) of the most recent Write depending on vendor’s implementation (see Table 18 — DWORD MISR Read and Write Operations in Loopback Test Mode (MR7 OP0=1)).

## 6.8.5.1 Test Method for DWORD Read Register Mode

a) Enable the test mode and select the desired read-back register by setting MR7 DWORD Loopback Enable = 1'b1 - Enable, DWORD MISR Control = 3'b010 - Register mode, and DWORD Read Mux Control = 0.

b) The host issues either precharge power-down or self refresh mode (R0=Low).

c) The host sends one or more DWORD read commands. The HBM4 responds following the read latency and burst length setting and following the normal read protocol.

## 6.8.6 DWORD LFSR Mode (Read direction)

When in DWORD LFSR mode (Read direction), the HBM4 generates DWORD data from the LFSR in response to read commands issued by the host. LFSR data is generated, consistent with only the valid UIs of the read protocol. Read Preamble and post-amble RDQS clocks are generated consistent with the read protocol. The first data cycle generated will be the LFSR initial state, based on Preset or an alternate seed value if loaded.

Figure 75 illustrates the behavior of DWORD LFSR mode (Read direction).

NOTE: There is no AWORD LFSR mode since the AWORD bus cannot source data to the host.  
![](images/aa5cf1efaf7012621121d1f061638bbc308fe66a69b04f8a6f908e31742dfcec.jpg)  
Figure 75 — DWORD Read LFSR Modes Behavior

## 6.8.6.1 Test Method for DWORD LFSR Mode (Read direction)

a) Initialize the test sequence by setting MR7 DWORD Loopback Enable = 1'b1 - Enable and presetting the MISR registers by setting the DWORD MISR Control = 3'b000 - Preset. The controller can load the DWORD MISR registers with an alternate seed value via the functional interface or IEEE 1500 (see AWORD and DWORD Write Register Modes and DWORD\_MISR IEEE 1500 port instruction).

b) The host issues either precharge power-down or self refresh mode (R0=Low).

c) Enable DWORD LFSR mode by setting MR7 DWORD MISR Control = 3'b001 - LFSR mode and DWORD Read Mux Control = 1'b0 - Return data from DWORD MISR registers.

d) The host sends one or more DWORD read commands. The HBM4 responds following the read latency and burst length setting and following the normal read protocol, with data produced from the LFSR. A suggested host-side implementation is to use signature register circuits for checking the validity of the data received.

## 6.8.7 AWORD and DWORD Write LFSR Compare Modes

The LFSR Compare modes enable direct identification of failing signal connections between the Host and HBM4. It is assumed that the Host implements LFSR data generators that match the lengths and polynomials of the HBM4 LFSRs, and that the Host and HBM4 LFSRs start and run in synch. The LFSRs generate data on each signal, and the compare circuitry checks for matching data for each data unit interval (UI). Any mismatch between the data received at the HBM4 inputs (based on the respective CK or WDQS clocking) and the data predicted by the HBM4 LFSR will set the sticky error bit for the respective signals. The first data cycle expected from the host and compared by the HBM4 will be the LFSR initial state, based on Preset or an alternate seed value if loaded.

Once a miscompare is found on a signal, its sticky error bit is set (1'b1) for the remainder of the test sequence. The sticky error bits may be read via the IEEE 1500 port READ\_LFSR\_COMPARE\_STICKY instruction or via the functional interface (see DWORD Read Register Mode). AWORD sticky error bits are only readable via the IEEE 1500 port. The sticky error bits are reset (1'b0) via the MR7 DWORD MISR Control = 3'b000 - Preset, or IEEE 1500 AWORD\_MISR\_CONFIG MODE = 2'b00 - Preset.

Figure 76 illustrates the system-level configuration for LFSR Compare mode.

![](images/06cb489548499c82566762df47cc0a116a94f840af92c022d34dbeb6af2d597c.jpg)  
Figure 76 — LFSR Compare Mode Block Diagram

Note that data produced on the DWORD Parity signals from the host to the HBM4 is an implementation suggestion for exercising the parity signal paths and HBM4 input timing and logic. The host-side implementation for parity signal generation is not specified. This figure also illustrates that a host-driven logical signal is compared with the matching logical signal data by the HBM4 compare circuit, regardless of any active lane repairs which may shift the physical signal routing. The AWORD LFSR Compare circuit matches the DWORD circuit except for the non-existent Parity signals.

## 6.8.7.1 Test method for AWORD (Write) LFSR Compare Mode

a) After the required HBM4 initialization, the host issues either precharge power-down or self refresh mode (R0 = LOW) and stops sending CK clocks to the HBM4 (CK\_t = LOW, CK\_c = HIGH).

b) Initialize the AWORD MISR (LFSR) register by setting the AWORD\_MISR\_CONFIG Enable = 1'b1 - On and AWORD\_MISR\_CONFIG MODE = 2'b00 - Preset. The Preset operation also clears the AWORD per-signal sticky error bits and enables the preamble clock filter circuit. The host-side LFSR data generator should also be initialized to the same value.

c) Enable the AWORD LFSR Compare mode by setting AWORD\_MISR\_CONFIG MODE = 2'b01 - LFSR Compare mode.

d) The host sends two or more CK clock cycles with LFSR-generated data on the AWORD signals. The first received CK clock cycle is discarded as a preamble clock by the HBM4. The HBM4 LFSR predicts expected AWORD data per cycle from the host, based on matching LFSR polynomials and starting seeds in the host and HBM4. Any mismatches set sticky error for the respective signal. Parity is evaluated, if enabled. The ending clock state applied by the host is CK\_t = LOW, CK\_c = HIGH.

e) The host reads the Sticky error bits to determine which signals failed. The bits are readable via the IEEE 1500 port READ\_LFSR\_COMPARE\_STICKY instruction.

## 6.8.7.2 Test Method for DWORD Write LFSR Compare mode

a) Initialize the DWORD LFSR (MISR) registers by setting MR7 DWORD Loopback Enable = 1'b1 - Enable and DWORD MISR Control = 3'b000 - Preset. The Preset operation also clears the DWORD per-signal sticky error bits. The controller can load the DWORD MISR registers with an alternate seed value via the functional interface or IEEE 1500 (see AWORD and DWORD Write Register Modes and DWORD\_MISR IEEE1500 port instruction). The host-side LFSR data generator should also be preset/initialized to the same value.

b) The host issues either precharge power-down or self refresh mode (R0=Low).

c) Enable DWORD LFSR Compare mode by setting MR7 DWORD MISR Control = 3'b100 – LFSR Compare mode.

d) The host sends one or more DWORD write cycles with LFSR-generated data on the DWORD signals following the write latency and burst length setting and following the normal write protocol. The HBM4 LFSRs predict expected DWORD data per cycle from the host, based on matching LFSR polynomials and starting seeds in the host and HBM4. Any mismatches set sticky error for the respective signal. Parity is evaluated, if enabled.

e) The host reads the sticky error bits to determine which signals failed. The bits are readable via the IEEE 1500 port READ\_LFSR\_COMPARE\_STICKY instruction. The sticky error bits are also readable via the functional interface (see DWORD Read Register Mode).

## 6.9 On-die DRAM ECC

## 6.9.1 ECC Overview

The HBM4 device uses a symbol-based on-die ECC, read/write meta-data (MD) bits, an error scrubbing mechanism, an error transparency protocol, interface transmission parity, and fault isolation limits to achieve a high level of system RAS.

## HBM4 ECC features:

• Minimum 304b codeword

<sup></sup> 256b+16b user data access size

<sup></sup> Symbol-based on-die ECC

<sup></sup> Symbol size is implementation specific

• On-die ECC real-time transparency

<sup></sup> Two pins per PC transmit error severity

<sup></sup> SBE signaled only after SBE threshold exceeded

• Automated on-die error scrubbing mechanism

<sup></sup> Auto-ECS during REFab operation has MR for enable/disable

<sup></sup> Auto-ECS during SRF has MR for enable/disable

<sup></sup> MR bit to enable correction of CEm during ECS

<sup></sup> Errors are only logged during ECS

• Single bit READ and WRITE data interface parity

<sup></sup> DQ, DBI, and ECC bits included in parity calculation

SEV transparency bits not included in parity calculation

An overview of an example HBM4 on-die ECC engine is shown in Figure 77.

![](images/ca91a906910c80a84a5998729dcab8ba57d76dea34d51fa16980a0e4aa2f9deb.jpg)  
Figure 77 — On-die ECC Overview Diagram Example

## 6.9.2 HBM4 On-die ECC Requirements

## On-die ECC Engine:

HBM4 devices shall implement on-die symbol-based ECC.

HBM4 on-die ECC has a codeword size dependent on symbol size error correction capability. The dataword and example check-bits of the codeword are as follows:

• Data-word: 272b (256b data per PC + 16b meta data per PC)

• On-die ECC check-bits: Implementation specific (e.g., 32b assuming 16b single symbol correction)

The 272b user data consists of 256b transmitted over 32 DQ pins times BL8 and 16b transmitted over 2 ECC pins times BL8.

On reads the DRAM corrects all errors that are less than or equal to a single symbol size and within the symbol boundary before returning the data to the memory controller. The DRAM shall not write the corrected data back to the array during a read cycle.

On writes, the DRAM computes the check bits and writes the data and check bits to the array.

In the case of interface MD bits being disabled via MR9 OP0, the DRAM may assume any value for the 16b of the ECC data-word corresponding to the MD bits. The DRAM can only guarantee valid array MD bits if written while interface MD function is enabled. The ECC engine treatment of the MD bits is not affected by the disabling of the interface MD setting.

The specific ECC H-matrix used, the symbol size, and the number of codewords are implementation specific.

## 6.9.3 DRAM Fault Isolation Requirements

Fault isolation is the management of errors caused by various faults to be isolated within certain boundaries regardless of the od-ECC operation.

The fault isolation boundaries will be chosen in accordance with the ECC symbol size to maximize the correction capability of multi-bit faults. The design must guarantee that the most common multi-bit fault modes will create errors constrained to a correctable symbol-size or fewer bits.

## 6.9.4 Error Check and Scrub (ECS)

The HBM4 device implements an Auto ECS function. Auto ECS will use on-die ECC and operate in the background during REFab and SRF periods. The ECS mode allows the DRAM to internally read, detect errors, correct errors, and write back corrected data bits to the array (scrub errors) while providing transparency. Any errors corrected by on-die ECC during Auto ECS must be logged in the transparency registers according to the rules described in this clause.

## 6.9.4 Error Check and Scrub (ECS) (cont’d)

During Auto ECS, the internal Read-Modify-Write cycle will:

1. Read the entire code-word(s) from the DRAM array.

2. If the ECC engine detects a single-bit error, the error will be corrected, and code-word(s) will be written back to DRAM.

3. If the ECC engine detects a correctable multi-bit error, the error will be corrected, and code-word(s) will be written back to DRAM. CEm during ECS can be enabled/disabled by MR9 OP6.

4. If an error is detected in the code-word(s) and is uncorrectable, the bits in the code-word(s) will not be modified. The code-word(s) must not be written back to DRAM.

5. If the ECC engine detects no error, the DRAM may choose to write the resultant code-word(s) back to DRAM or not.

## ECS related MR control:

Table 63 — Mode Registers Associated with Auto ECS
<table><tr><td rowspan=1 colspan=1>Auto ECS Mode Registers</td><td rowspan=1 colspan=1>Mode Register Value (Default All Disabled)</td></tr><tr><td rowspan=1 colspan=1>Auto ECS via REFab (ECSREF)</td><td rowspan=1 colspan=1>MR9 OP4, 1 = Enabled, 0 = Disabled</td></tr><tr><td rowspan=1 colspan=1>Auto ECS during Self Refresh (ECSSRF)</td><td rowspan=1 colspan=1>MR9 OP5, 1 = Enabled, 0 = Disabled</td></tr><tr><td rowspan=1 colspan=1>CEm during ECS (ECSCEM)</td><td rowspan=1 colspan=1>MR9 OP6, 1 = Enabled, 0 = Disabled</td></tr><tr><td rowspan=1 colspan=1>ECS Error Type and Address Log Reset (ECSRES)</td><td rowspan=1 colspan=1>MR9 OP7, 1 = Reset (Self Clearing), 0 = Maintain</td></tr><tr><td rowspan=1 colspan=1>ECS Error Log Reset with Log Read-out (ECSLOG)</td><td rowspan=1 colspan=1>MR8 OP2 1 = Enabled, 0 = Disabled</td></tr></table>

Auto ECS modes MR9 OP[6:4] defined in Table 63 shall be programmed during DRAM initialization, ECSCEM (MR9 OP6) must be programmed either before or at the same time as ECSREF and ECSSRF (OP[5:4]) and shall not be changed once the first ECS operation occurs, otherwise an unknown operation could result during subsequent ECS operations.

ECS operations are considered to have begun once one of Auto ECS modes (ECSREF or ECSSRF) or both modes are enabled and the first required REFab or SRE command is issued.

The DRAM can only guarantee valid ECS operations if array bits are written prior to executing ECS operations, thus enabling the DRAM to calculate the proper parity bits.

Once ECS operations begin the only way to reset the Auto ECS is a device RESET. Disabling either ECSREF (MR9 OP4) or ECSSRF (MR9 OP5) or both after enabled just disables ECS operations in that mode and does not reset the ECS address counters or ECS logs.

## 6.9.4 Error Check and Scrub (ECS) (cont’d)

## ECS related timing parameters:

The ECS operation timing is shown in Figure 78.

![](images/d625cc3d46c54d9b57a9bb33d56d19e46c4ed3a656e9d72439ae1d0d91e48157.jpg)  
Figure 78 — ECS Operation Timing

• t<sub>ECSC</sub>: Max time for HBM4 to complete ECS operation

• t<sub>ECSint</sub>: Average ECS interval to cover all codewords in a specified period of t<sub>ECS</sub> (e.g., 24h)

• t<sub>ECS</sub>: Period of time to complete ECS on all codeword

• ERRTH: Vendor specific filter threshold of ERRCNT used for transparency. No CEs will be logged or transmitted on SEV pins until ERRCNT > ERRTH

In order to complete a full Error Check and Scrub within the recommended $\operatorname { t } _ { \mathrm { E C S } }$ (e.g., 24 hours), the average periodic interval of ECS operations (t<sub>ECSint</sub>) is 86,400 seconds divided by the total number of codewords as described in Table 64. The number if ECS operations is configuration dependent.

Table 64 — t<sub>ECSint</sub> per Stack (ECS Independent of SID)
<table><tr><td rowspan=1 colspan=1>Configuration</td><td rowspan=1 colspan=1>24 Gb x 4/ 8/ 12/ 16</td><td rowspan=1 colspan=1>32 Gb x 4/ 8/ 12/ 16</td></tr><tr><td rowspan=1 colspan=1>GB per device</td><td rowspan=1 colspan=1>12/24/36/48 GB</td><td rowspan=1 colspan=1>16/ 32/ 48/ 64 GB</td></tr><tr><td rowspan=1 colspan=1>Gb per PC</td><td rowspan=1 colspan=1>1.5 Gb</td><td rowspan=1 colspan=1>2 Gb</td></tr><tr><td rowspan=1 colspan=1>304b code-words per PC per SID</td><td rowspan=1 colspan=1>222 × 1.5</td><td rowspan=1 colspan=1>223</td></tr><tr><td rowspan=1 colspan=1>tECSint [ms] per PC</td><td rowspan=1 colspan=1>13.733</td><td rowspan=1 colspan=1>10.300</td></tr><tr><td rowspan=1 colspan=3>NOTE 1  $\underline { { \mathrm { t } _ { \mathrm { E C S i n t } } } }$ values are based on the recommended 24hr $\mathrm { \Delta t _ { E C S } }$ period.</td></tr></table>

## ECS operations in REFab:

If ECSREF is enabled (MR9 OP4=1) and ECSSRF is disabled (MR9 OP5=0), the maximum average spacing between REFab commands for the DRAM to complete the automatic scrub within the recommended t<sub>ECS</sub>(e.g., 24 hours) is $\mathrm { \Delta t { _ { E C S i n t } } }$ as shown in Figure 79.

## 6.9.4 Error Check and Scrub (ECS) (cont’d)

![](images/f9f1f02355a03c3c8684e40ff3de19d6889a6245307a6ff9adc6b02435e5ec24.jpg)

REFab may be issued at a higher rate than tECSint to meet refresh requirements (tREFI). The host is required to meet the requirements for refresh, while at the same time ensuring tECSint is met. The managing of the refresh and ECS operations on the DRAM is vendor implementation specific.

## For example:

i) On one extreme, the host may issue only REFab (no REFpb) commands every 3.9 µs (tREFI) to meet refresh requirements. This equates to approximately 22.1 billion REFab per SID in the recommended 24 hr tECS period (24 hrs/3.9 µs). In this case, the DRAM will use a fraction of the 11.05 billion REFab per SID to perform ECS operations since $2 ^ { 2 3 }$ codewords in the case of 32G bit density is approximately 16.8M REFab per SID.

ii) On the other extreme, the host can issue 11.05 billion REFpb sets per SID and no REFab to meet the refresh requirements. With ECS enabled, the host will need to convert at least 2<sup>23</sup> REFpb sets per SID to REFab to meet both the refresh and ECS requirements for a 32Gbit DRAM. tECSint must be met for the REFab.

In both examples, the host has the option to send an additional $2 ^ { 2 3 }$ REFab per SID for a 32G bit on top of the approximately 11.05 billion REFpb sets or REFab required for refresh operations. In either case the DRAM will manage the refresh and ECS operations.

## ECS operations in only Self Refresh mode:

When ECSSRF is enabled (MR9 OP5=1) and ECSREF is disabled (MR9 OP4=0), the DRAM will perform ECS operations only in Self Refresh. The management of the refresh and ECS operations while in Self Refresh is vendor implementation specific. As an ECS operation may still be in progress when the SRX command is issued, the log is not guaranteed to be updated until tXS has expired after the SRX command.

## ECS operations in both REFab and Self Refresh mode:

When both ECSSRF (MR9 OP5=1) and ECSREF (MR9 OP4=1) are enabled, the DRAM will perform ECS operation in both modes when REFab or SRE commands.

## 6.9.4 Error Check and Scrub (ECS) (cont’d)

ECS related logging: The registers are allocated per PC and SID accessible via the IEEE1500 interface.

1. When the on-die ECC detects an error, the DRAM address of the error must be logged in the form of Bank, Row, Column, Error Type

2. The error is logged within t<sub>ECSC</sub> and accessible via IEEE1500

The priority of error logging is defined in Table 65.

Table 65 — Error Overwrite Priority Rules to Handle Multiple Error Logging
<table><tr><td rowspan=2 colspan=1>Previous Error</td><td rowspan=1 colspan=4>Current Error</td></tr><tr><td rowspan=1 colspan=1>NE</td><td rowspan=1 colspan=1>CEs</td><td rowspan=1 colspan=1>CEm</td><td rowspan=1 colspan=1>UE</td></tr><tr><td rowspan=1 colspan=1>NE (No error)</td><td rowspan=1 colspan=1>None</td><td rowspan=1 colspan=1>Update</td><td rowspan=1 colspan=1>Update</td><td rowspan=1 colspan=1>Update</td></tr><tr><td rowspan=1 colspan=1>CEs (Corrected single-bit error)</td><td rowspan=1 colspan=1>Maintain</td><td rowspan=1 colspan=1>Update</td><td rowspan=1 colspan=1>Update</td><td rowspan=1 colspan=1>Update</td></tr><tr><td rowspan=1 colspan=1>CEm (Corrected multi-bit error)</td><td rowspan=1 colspan=1>Maintain</td><td rowspan=1 colspan=1>Maintain</td><td rowspan=1 colspan=1>Update</td><td rowspan=1 colspan=1>Update</td></tr><tr><td rowspan=1 colspan=1>UE (Uncorrectable error)</td><td rowspan=1 colspan=1>Maintain</td><td rowspan=1 colspan=1>Maintain</td><td rowspan=1 colspan=1>Maintain</td><td rowspan=1 colspan=1>Update</td></tr><tr><td rowspan=1 colspan=5>NOTE 1 Logging of newest error may be lost in case of a simultaneous reset and new ECS errorNOTE 2In the case of MR8 OP2 = 1, reset of ECS error log can only be guaranteed when captured WDR of ECS errorlog is valid</td></tr></table>

## Reset of ECS error log:

A reset of the ECS error log clears all VALID bits of the ECS\_ERROR\_LOG WDR to $0 _ { \mathrm { b } }$ and the Error Type log to “NE” (no error). There are three independent methods for clearing the error log:

1. The host may issue device RESET.

2. The host may issue a manual log reset by programming ECSRES (MR9 OP7 = 1). In this case the register is self clearing and the reset of the log is completed no later than tMOD. Logging will resume after tMOD expires and the first ECS operation starts and the log is updated based on the rules in Table 65.

3. The host may configure MR8 OP2 ECS error log auto-reset (ECSLOG), in which case the error log will be reset upon read out of the error log.

## Error counting:

The number of CEs are counted during ECS in order to control whether the severity information of CEs is conveyed on the SEV pins during READ operations. Error counting assumes one codeword covering each access.

• ERRCNT == number of error events accumulated during ECS

• ERRCNT is independently maintained per PC and SID

• CEs count as one event toward ERRCNT

• CEm and UE do not count toward ERRCNT

• If more than one codeword is used, a CEs in both codewords counts as a CEm

• ERRCNT will be incremented a maximum of one for any codeword size

## Reset of ERRCNT:

Automatic reset internally by HBM4 after each t<sub>ECS</sub>

## 6.9.4 Error Check and Scrub (ECS) (cont’d)

## ECS Flag feature (optional feature):

HBM4 Auto ECS supports an optional ECS Flag. The host can read out the Device ID to determine if ECS flag feature is supported. The ECS flag is included in the REFab and SRE commands. ECS operations are considered to have begun once with the first REFab or SRE with ECS flag = ‘L’ in the respective command is issued as ECS operations are only initiated when the ECS flag is set to ‘L’ per the rules in Table 66.

Table 66 — ECS Flag Behavior
<table><tr><td rowspan=1 colspan=1>Command</td><td rowspan=1 colspan=1>R4</td><td rowspan=1 colspan=1>DRAM Behavior</td></tr><tr><td rowspan=2 colspan=1>SRE(ECSSRF enabled)</td><td rowspan=1 colspan=1>ECS=H</td><td rowspan=1 colspan=1>ECS operations suppressed, DRAM manages refresh operations in SelfRefresh mode</td></tr><tr><td rowspan=1 colspan=1>ECS=L</td><td rowspan=1 colspan=1>DRAM manages ECS and Refresh operations in Self Refresh mode</td></tr><tr><td rowspan=2 colspan=1>REFab(ECSREF enabled)</td><td rowspan=1 colspan=1>ECS=H</td><td rowspan=1 colspan=1>ECS operations suppressed, DRAM manages refresh operation with theREFab command</td></tr><tr><td rowspan=1 colspan=1>ECS=L</td><td rowspan=1 colspan=1>DRAM manages ECS and Refresh operations with the REFab command</td></tr></table>

As shown in Figure 80, the host must ensure REFab ECS=L are issued at tECSint to properly complete ECS operations. Regardless of ECS flag, t must be met. If Auto ECS is not enabled, a REFab ECS=L will perform a refresh operation.

![](images/5bf2b87d6c281166a9f2adb676591dbe29cfb1d4f89620b7ca78382e373f01ae.jpg)

When ECSSRF is enabled (MR9 OP5=1) and ECSREF is disabled (MR9 OP4=0), the DRAM will perform ECS operations only in Self Refresh when SRE (ECS=L) command is issued. If Auto ECS operation are not enabled in Self Refresh, a SRE (ECS=L) will result in the DRAM managing refresh operations only.

When both ECSSRF (MR9 OP5=1) and ECSREF (MR9 OP4=1) are enabled, the DRAM will perform ECS operation in both modes when either REFab (ECS=L) or SRE (ECS=L) commands are issued.

## 6.9.5 On-die ECC Transparency Protocol

An HBM4 device must provide transparency of actions by the on-die ECC engine. The specific information to be conveyed and the method of conveyance is given in Table 67.

Table 67 — Transparency Attributes and Their Access/Control Mechanism
<table><tr><td rowspan=1 colspan=1>Attribute</td><td rowspan=1 colspan=1>Operation</td><td rowspan=1 colspan=1>Transparency Mechanism</td></tr><tr><td rowspan=1 colspan=1>Real-time severity metadata</td><td rowspan=1 colspan=1>RD/RDA</td><td rowspan=1 colspan=1>Two SEV pins per PC</td></tr><tr><td rowspan=1 colspan=1>Logging address and severity of an error</td><td rowspan=1 colspan=1>ECS</td><td rowspan=1 colspan=1>IEEE1500 register</td></tr></table>

Severity Metadata: The severity of an error denotes the outcome of the on-die ECC processing over a codeword(s) during a READ operation. The severity information is conveyed on the SEV pins together with the data transfer on the DQ pins. Severity transmission will use the encoding shown in the Table 68 for each BL8 transaction.

Table 68 — Severity Encodings on the SEV pins
<table><tr><td rowspan=3 colspan=1>Severity</td><td rowspan=3 colspan=1>Pin</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan=1 colspan=8>Burst Position</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>7</td></tr><tr><td rowspan=2 colspan=1>NE</td><td rowspan=1 colspan=1>SEV[0]</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>SEV[1]</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=2 colspan=1>CEs</td><td rowspan=1 colspan=1>SEV[0]</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>SEV[1]</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=2 colspan=1>CEm</td><td rowspan=1 colspan=1>SEV[0]</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>SEV[1]</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=2 colspan=1>UE</td><td rowspan=1 colspan=1>SEV[0]</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>SEV[1]</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td></tr></table>

Severity Metadata Signaling Control: The HBM4 device includes a mode register MR9 OP1 to enable or disable the severity metadata signaling by the HBM4 device.

Table 69 — Severity Transmission on READ
<table><tr><td rowspan=1 colspan=1>On-die ECC Severity</td><td rowspan=1 colspan=1>NE</td><td rowspan=1 colspan=1>CEs</td><td rowspan=1 colspan=1>CEm</td><td rowspan=1 colspan=1>UE</td></tr><tr><td rowspan=1 colspan=1>Severity on SEV[1:0]</td><td rowspan=1 colspan=1>NE</td><td rowspan=1 colspan=1>NE if ERRCNT &lt;= ERRTHCEs if previous or currentERRCNT &gt; ERRTH</td><td rowspan=1 colspan=1>CEm</td><td rowspan=1 colspan=1>UE</td></tr></table>

## 6.9.5 On-die ECC Transparency Protocol (cont’d)

The CEs output enables timing for SEV is shown in Figure 81.

![](images/fa830fc2e1f0875ac665ec0061d10042ac5cdcf6b85d4ab76f9a4e5c3a9eeaf8.jpg)  
Figure 81 — ECS CEs Output Enable Timing for SEV Signaling

## 6.9.6 ECC Engine Test Mode

HBM4 devices provide ECC engine testing method of the on-die ECC engine only, not error access into the core. The outcome of the error injection is reported according to the transparency protocol.

Table 70 — ECC Engine Test Modes
<table><tr><td rowspan=1 colspan=1>Selection by MRS</td><td rowspan=1 colspan=1>ECC Engine Test Mode</td></tr><tr><td rowspan=1 colspan=1>ECC Engine Test Mode(MR9 OP2)</td><td rowspan=1 colspan=1>0 – Normal Operation (Default)1 – ECC Engine Test Mode</td></tr><tr><td rowspan=1 colspan=1>Error Vector Patterns(MR9 OP3)</td><td rowspan=1 colspan=1>0 – CW0 (Codeword0)Data 1’ means error bit and Data0&#x27;means non-error bit1 – CW1 (Codeword1)Data 0’ means error bit and Data 1’ means non-error bit</td></tr></table>

While in the ECC engine test mode in Table 70,

1. WR will function as an error injection command, Write DQ data is error injection pattern (CW0 or CW1 by MR9 OP3)

2. RD will function as an outcome output command, Read DQ/ECC/SEV data is the outcome of ECC engine test

## 6.9.6 ECC Engine Test Mode (cont’d)

The following sequence must be satisfied to perform a functional On-die ECC engine test mode of HBM4 DRAM. See Figure 82 and Table 71.

1. The HBM4 device registers Mode Register Set command (MRS) by MR9 OP[3:2] for the entry of On-die ECC engine test mode in Table 70. Error severity reporting must be enabled via the SEVR bit in MR9 OP1. The MD bit in MR9 OP0 must be set according to the user’s desire to include the ECC signals in this test or not.

2. As an example in Table 71 — Example of Error Vectors and Corresponding Severity for the engine test, write “1” as Error and “0” as NE(No Error) in the case of CW0 mode. The symbol boundary is vendor specific, and output and severity information are determined according to the error type injected by the host.

3. To check the result of engine test, read the output after t<sub>WTR</sub>.

A. The DQs will show the correction data as ALL “0” when the DATA is CEs or CEm in the case of CW0. Also, the output will show the values as written data when the DATA is UE case.

B. The BL[7:4] of SEV[1:0] pins will indicate NE, CEs, CEm and UE. CEs severity information can be real-time signaling via SEV[1:0]. During ECC engine test, #ERRTH value is ignored.

4. Repeat the 2, 3, 4 sequence and the operation for the engine test after t<sub>RTW</sub>.

A. E.g.) Mode entry - WR-RD - WR-RD - WR-RD - … In this case, a single WR must be followed by a single RD.

The mapping between DQ/ECC and DATA[271:0] is vendor specific. When the MRS bit is enabled, the core is not accessed, and the data pattern is interpreted as an error vector. When HBM4 is in the ECC Engine Test Mode, it does not guarantee data retention and the only allowed commands are CNOP, WR, RD and MRS to disable this test mode.

![](images/4515ea4b7987dc36378eb3bd0fead7fa58c90e3320284909709b805181251467.jpg)  
Figure 82 — The Block Diagram of On-die ECC Engine and Path for ECC Engine Test Mode

## 6.9.6 ECC Engine Test Mode (cont’d)

Table 71 — Example of Error Vectors and Corresponding Severity
<table><tr><td rowspan=1 colspan=1>Severity</td><td rowspan=1 colspan=1>Error Vector Pattern(MR9 OP3)</td><td rowspan=1 colspan=1>Error VectorInput[271:0](Write data)</td><td rowspan=1 colspan=1>Error VectorOutput[271:0](Read data)</td><td rowspan=1 colspan=1>Severity(SEV[1:0])</td><td rowspan=1 colspan=1>Note</td></tr><tr><td rowspan=2 colspan=1>NE</td><td rowspan=1 colspan=1>CW0</td><td rowspan=1 colspan=1>0000...00000000</td><td rowspan=1 colspan=1>0000...00000000</td><td rowspan=2 colspan=1>NE</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>CW1</td><td rowspan=1 colspan=1>1111...11111111</td><td rowspan=1 colspan=1>1111...11111111</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=2 colspan=1>CEs</td><td rowspan=1 colspan=1>CW0</td><td rowspan=1 colspan=1>1000...000000000000...00000001</td><td rowspan=1 colspan=1>0000...000000000000...00000000</td><td rowspan=2 colspan=1>CEs</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>CW1</td><td rowspan=1 colspan=1>0111...111111111111...11111110</td><td rowspan=1 colspan=1>1111...111111111111...11111111</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=2 colspan=1>CEm</td><td rowspan=1 colspan=1>CW0</td><td rowspan=1 colspan=1>0000...000011111111...00000000</td><td rowspan=1 colspan=1>0000...000000000000...00000000</td><td rowspan=2 colspan=1>CEm</td><td rowspan=1 colspan=1>1,3</td></tr><tr><td rowspan=1 colspan=1>CW1</td><td rowspan=1 colspan=1>1111...111100000000...11111111</td><td rowspan=1 colspan=1>1111...111111111111...11111111</td><td rowspan=1 colspan=1>2,3</td></tr><tr><td rowspan=1 colspan=1>UE</td><td rowspan=1 colspan=1>CW0 or 1</td><td rowspan=1 colspan=1>None of the above</td><td rowspan=1 colspan=1>Not specified</td><td rowspan=1 colspan=1>UE</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=6>NOTE 1 CW0 indicates that 1 means the error bit and 0 means normal bitNOTE 2 CW1 indicates that 0 means the error bit and 1 means normal bit.NOTE 3 CEm is limited to a symbol.</td></tr></table>

6.9.6 ECC Engine Test Mode (cont’d)  
![](images/d17f70d5f1b2f8ebcb5a7065efdadf0b4392b9cb4780df8bd6d84964932771b1.jpg)  
NOTE 1 WRITE and READ address must be the same for ECC Engine Test Mode.  
NOTE 2 WRITE and READ commands do not require a preceding ACT command for ECC Engine Test Mode.  
NOTE 3 No other commands are allowed except CNOP and MRS to disable ECC Engine Test mode.  
NOTE 4 WL = 4 and RL = 6 are shown as an example.  
NOTE 5 DATA = DQ[31:0], DBI[3:0], ECC[1:0], SEV[1:0] for PC0 and DATA = DQ[63:32], DBI[7:4], ECC[3:2], SEV[3:2] for PC1.  
NOTE 6 Da, ..., Da+7 = data-in for WRITE command. Db, ..., Db+7 = data-out for READ command.  
NOTE 7 tWDQS2DQ\_O, tDQSS = 0 and nominal tQW are shown for illustration purposes.  
NOTE 8 tWTR should be tWTRL by both WRITE and READ access banks in the same bank group for ECC Engine Test Mode.  
NOTE 9 WDBI and RDBI could be on or off. WDBI is controlled with MR0 OP1 and RDBI is controlled with MR0 OP0.  
NOTE 10 WDBI and RDBI off are recommend for output of ECC Engine Test Mode. (See Table 71 — Example of Error Vectors and Corresponding Severity) NOTE 11 SEVR on is mandatory to verify on-die ECC transparency.

Figure 83 — Timing Diagram of ECC Engine Test Mode

## 6.10 WOSC

## 6.10.1 WDQS Interval Oscillator

As voltage and temperature change on the HBM4 DRAM, the WDQS clock tree delay will shift and may require re-training. The HBM4 DRAM includes an internal WDQS clock-tree oscillators to measure the amount of delay over a given time interval (determined by the controller), allowing the controller to compare the trained delay value to the delay value seen at a later time. The WDQS Interval Oscillator (“oscillator”) will provide the controller with important information regarding the need to re-train, and the magnitude of potential error. The oscillator is not associated with any channel and operates fully independent of any channel’s operating frequency or state (e.g., bank active, bank idle, power-down or self refresh). Also, no CK, WDQS or WRCK clock is required while the oscillator is counting. The oscillator is disabled by default upon power-up.

The IEEE1500 instructions WOSC\_RUN and WOSC\_COUNT are associated with the oscillator. Setting the WOSC\_START\_STOP bit in the WOSC\_RUN Wrapper Data Register to 1 will start an internal ring oscillator that counts the number of times a signal propagates through a copy of the WDQS clock tree. The oscillator is stopped by setting the WOSC\_START\_STOP bit back to 0. The maximum count is $2 ^ { 2 4 }$ 1, and the longest run time for the oscillator to not overflow the counter can be calculated as follows:

## Longest Run Time Interval = 2<sup>24</sup> × t<sub>RX\_DQS2DQ</sub>(min)

The validity of the clock count is indicated by the WOSC\_COUNT\_VALID bit in the WOSC\_COUNT Wrapper Data Register. The default state of 0 indicates an invalid count. The state is also set to 0 when the oscillator is started. When the oscillator stops, the WOSC\_COUNT\_VALID bit is set to 1 to indicate a valid count, and the result of the counter is stored in the WOSC\_COUNT\_VALUE field of the WOSC\_COUNT WDR. The WOSC\_COUNT\_VALID bit will remain 0 (invalid) if the counter overflows $( 2 ^ { 2 4 }$ or more cycles) or if the oscillator is interrupted by pulling RESET\_n to LOW. On the other hand, pulling WRST\_n to LOW does not impact the oscillator's operation. After the oscillator stops the host may issue the WOSC\_COUNT instruction to read out the count.

The controller may adjust the accuracy of the result by running the oscillator for shorter (less accurate) or longer (more accurate) duration. The accuracy of the result for a given temperature and voltage is determined by the following equation:

## WDQS Oscillator Granularity Error = 2 × (WDQS delay) / (Run Time)

Where:

<sup></sup> Run Time = total time between the oscillator starting and automatically stopping

<sup></sup> WDQS delay = the value of the WDQS clock tree delay [t<sub>RX\_DQS2DQ</sub>(min/max)]

Additional matching error must be included, which is the difference between WDQS training circuit and the actual WDQS clock tree across voltage and temperature. The matching error is vendor specific.

Therefore, the total accuracy of the WDQS Oscillator counter is given by:

WDQS Oscillator Accuracy = 1 - Granularity Error - Matching Error

## 6.10.1 WDQS Interval Oscillator (cont’d)

Example: If the total time between start and stop is 100 ns, and the maximum WDQS clock tree delay is 400 ps [t<sub>RX\_DQS2DQ</sub>(max)], then the WDQS Oscillator Granularity Error is:

WDQS Oscillator Granularity Error = 2 × (0.4 ns) = 0.8% 100 ns

This equates to a granularity timing error of 3.2ps.

Assuming a circuit Matching Error of 5.5ps across voltage and temperature, then the accuracy is:

WDQS Oscillator Accuracy = 1 - 3.2 + 5.5 = 97.8% 400

Example: Running the WDQS Oscillator for a longer period improves the accuracy. If the total time between start and stop is 250ns, and the maximum WDQS clock tree delay is 400ps [t<sub>RX\_DQS2DQ</sub>(max)], then the WDQS Oscillator Granularity Error is:

$$
\mathbf { W D Q S ~ O s c i l l a t o r ~ G r a n u l a r i t y ~ E r r o r } = \frac { 2 \times ( 0 . 4 ~ \mathrm { n s } ) } { 2 5 0 ~ \mathrm { n s } } = 0 . 3 2 \%
$$

This equates to a granularity timing error or 1.28ps.

$$
\mathrm { W D Q S ~ O s c i l l a t o r ~ A c c u r a c y } = 1 - \frac { 1 . 2 8 + 5 . 5 } { 4 0 0 } = 9 8 . 3 \%
$$

Assuming a circuit Matching Error of 5.5ps across voltage and temperature, then the accuracy is:

## 6.10.1 WDQS Interval Oscillator (cont’d)

The WDQS Interval Oscillator matching error is defined as the difference between the WDQS training circuit (interval oscillator) and the actual WDQS clock tree across voltage and temperature.

## Parameters:

<sup></sup> t<sub>RX\_DQS2DQ</sub>: Actual WDQS clock tree delay

<sup></sup> t<sub>WDQSosc</sub>: Training circuit (interval oscillator) delay

$\operatorname { W O S C } _ { \mathrm { O f f s e t ( V ) } } { \mathrm { : } }$ Average delay difference over voltage

$\operatorname { W O S C } _ { \mathrm { O f f s e t ( T ) } } \colon$ Average delay difference over temp

$\mathrm { W O S C _ { M a t c h ( V ) : } }$ WDQS oscillator matching error over voltage

$\mathrm { W O S C _ { M a t c h ( T ) } } \mathrm { : }$ WDQS oscillator matching error over temp

![](images/795ed716b2999cbc81f794e2cb62a5bece3d37d1e80a936e1928ccf8dd6cfe14.jpg)  
Figure 84 — Oscillator Offset $\mathbf { ( W O S C _ { o f f s e t ( V ) } ) }$

WOSC<sub>Match(V)</sub>:

$$
\mathbf { W O S C } _ { \mathrm { M a t c h ( V ) } } = \left[ \mathbf { t } _ { \mathrm { R X \_ D Q S 2 D Q ( V ) } } - \mathbf { t } _ { \mathrm { W D Q S o s c ( V ) } } - \mathbf { W O S C } _ { \mathrm { o f f s e t ( V ) } } \right]
$$

t<sub>DQSosc(V)</sub>:

$$
\begin{array} { c } { \mathbf { t } _ { \mathrm { W D Q S o s c ( V ) } } = \underline { { \mathbf { R u n t i m e } } } } \\ { 2 \times \mathbf { C o u n t } } \end{array}
$$

t<sub>WDQSosc(T)</sub>:

## 6.10.1 WDQS Interval Oscillator (cont’d)

![](images/1bd218b5aaa0ce12ddd9d7aa47a4c243eff240cc9142a5d29e48888174d4a03f.jpg)  
Figure 85 — Oscillator Offset (WOSC<sub>offset(T)</sub>)

$$
\mathbf { W O S C } _ { \mathrm { M a t c h ( T ) } } = \left[ \mathbf { t } _ { \mathrm { R X \_ D Q S 2 D Q ( T ) } } - \mathbf { t } _ { \mathrm { W D Q S o s c ( T ) } } - \mathbf { W O S C } _ { \mathrm { o f f s e t ( T ) } } \right]
$$

$$
\mathbf { t } _ { \mathrm { W D Q S o s c ( T ) } } = \underbrace { \mathbf { R u n t i m e } } _ { 2 \times \mathrm { C o u n t } }
$$

## 6.10.1 WDQS Interval Oscillator (cont’d)

Table 72 — WDQS Oscillator Matching Error Specification
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Unit</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>WDQS Oscillator Matching Error:voltage variation</td><td rowspan=1 colspan=1> $\mathrm { W O S C _ { M a t c h ( V ) } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ps</td><td rowspan=1 colspan=1>1,2,3,5</td></tr><tr><td rowspan=1 colspan=1>WDQS Oscillator Matching Error:temperature variation</td><td rowspan=1 colspan=1> $\mathrm { W O S C _ { M a t c h ( T ) } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ps</td><td rowspan=1 colspan=1> $1 , 2 , 3 , 5$ </td></tr><tr><td rowspan=1 colspan=1>WDQS Oscillator Offset for voltagevariation</td><td rowspan=1 colspan=1> $\mathrm { W O S C _ { o f f s e t ( V ) } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ps</td><td rowspan=1 colspan=1>2,5</td></tr><tr><td rowspan=1 colspan=1>WDQS Oscillator Offset for temperaturevariation</td><td rowspan=1 colspan=1> $\mathrm { W O S C _ { o f f s e t ( T ) } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ps</td><td rowspan=1 colspan=1> $2 , 5$ </td></tr><tr><td rowspan=1 colspan=6>NOTE 1 The $\mathrm { W O S C _ { M a t c h } }$ is the matching error between the actual WDQS and WDQS interval oscillator over voltage ortemp.NOTE 2 This parameter will be characterized or guaranteed by design.NOTE 3 The input stimulus for tRx_DQs2DQ will be consistent over voltage and temp conditions.NOTE 4 tRx_DQs2DQ(V, or T) delay will be the average of WDQS to DQ delay over the runtime period.NOTE 5 The matching error and offset of the oscillator came from WDQS Interval oscillator.NOTE 6 These parameters are defined per device.</td></tr></table>

## 6.10.2 tWDQS2DQ\_I Offset due to Temperature and Voltage Variation

As temperature and voltage change on the HBM4 DRAM, the WDQS clock tree will shift and may require retraining. The oscillator is usually used to measure the amount of delay over a given time interval (determined by the controller), allowing the controller to compare the trained delay value to the delay value seen at a later time. The t<sub>WDQS2DQ\_I</sub> offset due to temperature and voltage variation specification can be used for instances when the oscillator cannot be used to control the t<sub>WDQS2DQ\_I</sub>.

## 6.11 DCA and DCM

## 6.11.1 Duty Cycle Adjuster (DCA)

HBM4 DRAMs support a Duty Cycle Adjuster (DCA) that allows the memory controller to adjust the DRAM internally generated WDQS to compensate for a systemic duty cycle error on WDQS. The DCA is located before the WDQS divider or equivalent (see High Level Block Diagram Example of Clocking Scheme Figure 11). The DCA will affect the WDQS duty cycle for both Write and Read operations.

A separate DCA is provided for each WDQS (See Table 22):

<sup></sup> the DCA for WDQS0 (PC0) is controlled via MR11 OP[3:0];

<sup></sup> the DCA for WDQS1 (PC1) is controlled via MR11 OP[7:4];

A range of -7 steps to +7 steps is supported as shown in Figure 86 and changes the effective internal WDQS duty cycle as follows:

<sup></sup> a positive value increases the effective t<sub>WQSH</sub> time and decreases the effective t<sub>WQSL</sub> time.

<sup></sup> a negative value decreases the effective t<sub>WQSH</sub> time and increases the effective t<sub>WQSL</sub> time.

The use of the DCA is optional for the memory controller and is not supported at CK clock frequencies lower than f<sub>CKDCA</sub>; at those frequencies it is required to disable the DCA by setting the DCA code to the default value (0000).

A duty cycle adjustment, with or without a duty cycle monitor sequence, shall be performed prior to WDQS-to-CK Alignment Training.

An example of the effect of a DCA code change to the WDQS duty cycle is shown in Figure 87. The maximum offset and step are given in Table 73.

![](images/84f57e995b9b1c16bf3e0e54369e8d2cb52d70c10df66217d16071ef7359fc24.jpg)  
Figure 86 — Duty Cycle Adjuster Range

Table 73 — DCA Maximum Offset and Step Size
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Unit</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Duty cycle adjuster maximum offset</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>35</td><td rowspan=1 colspan=1>ps</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=1>Duty cycle adjuster single step size</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>ps</td><td rowspan=1 colspan=1>1,3</td></tr><tr><td rowspan=1 colspan=5>NOTE 1 The values are guaranteed by design.NOTE 2 The parameter describes the absolute maximum offset from step 0 to step +7 or from step0 to step -7.NOTE 3 The single step size reflects the non-linearity of each step.</td></tr></table>

6.11.1 Duty Cycle Adjuster (DCA) (cont’d)  
![](images/60179bac82f887efe789dfc71c3b2deee324f9b68939a4d3456b9e59ff8934e3.jpg)  
NOTE 1 Refer to the AC Timings section for the definition of tWQSH, tWQSL, and tWDQS.

Figure 87 — Relationship Between WDQS Waveform and DCA Code Change (Example)

## 6.11.2 Read Duty Cycle Adjuster (DCA)

HBM4 SDRAM supports read DCA function (as optional feature). Read DCA is mode- registeradjustable DCA to allow the memory controller to adjust DRAM read data duty to compensate duty distortion dedicated to read DQ. A separate read DCA is provided for each byte, RDCAL is for the lower Byte read adjustment and RDCAU is for upper byte read adjustment. Read DCA is located on adjusted WCK clock tree to provide dedicated read duty adjustment.

The host can adjust the read duty cycle by MR10 OP[3:0] for RDCA0 and MR10 OP[7:4] for RDCA1 setting and can determine the optimal Mode Register setting for DCA in multiple different ways. Since Read DCA might affect WDQS DCA, read DCA training shall be after WDQS DCA training as shown in Figure 88. DRAM read data duty is monitored by the host. To get proper duty distortion adjustment, HBM4 DRAM WDQS adjustment and sync need to be performed in proper way.

The following training sequence shall be followed for WDQS and RDQS duty cycle adjustment. (See Figure 88)

1. Write DCA training (w/ or w/o DCM);

2. Write Leveling (WDQS to CK alignment training);

3. Read DCA training (w/o DCM);

![](images/003c232b46cb99999031ad8e54389acc14b0ab935b623edc09791a6e5556bc47.jpg)  
Figure 88 — DCA Training Block Diagram

## 6.11.2.1 Read Duty Cycle Adjuster Range

The maximum offset and step are as follows. The difference of actual value between step N and step N+1 cannot be defined, since the variation of duty cycle by changing Read DCA code is not linear. Refer to Table 21 for adjusting RDQS DCA codes via MR10, along with $1 7 8 ^ { \mathrm { t h } }$ bits of DEVICE\_ID WDR fields (Table 132).

Table 74 — Read DCA Maximum Offset and Step Size
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Unit</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Read duty cycle adjuster maximum offset</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>35</td><td rowspan=1 colspan=1>ps</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=1>Read duty cycle adjuster single step size</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>ps</td><td rowspan=1 colspan=1>1,3</td></tr><tr><td rowspan=1 colspan=5>NOTE 1 The values are guaranteed by design.NOTE 2 The parameter describes the absolute maximum offset from step 0 to step +7 or from step 0 to step -7.NOTE 3 The single step size reflects the non-linearity of each step.</td></tr></table>

## 6.11.2.2 Relationship between Read DCA Code Change and DQ Output/RDQS Timing

The Read DCA code change effect to DQ Output and RDQS are as follows. The rising edge of WCK\_t affects to the rising edge of RDQS\_t and the even data output. The falling edge of WCK\_t affects to the falling edge of RDQS\_t and the odd data output. The complimentary signal (WCK\_c and RDQS\_c) is the same as the true signal.

The relationship between the Read DCA code change and delay time variation (Delay\_R/F) only can define in a qualitative manner. See Figure 89.

![](images/37b4b9811dae96eaa6123e8aad28bde23840526efd9d504626cf3af7e89284a3.jpg)  
Figure 89 — Example of Relationship between WDQS Waveform and RDQS\_t/c and DQ Output

## 6.11.3 Duty Cycle Monitor (DCM)

The HBM4 DRAM includes a Duty Cycle Monitor (DCM) that allows the memory controller to observe the DRAM internal WDQS clock tree duty cycle distortion.

The DCM is controlled via MR6 OP[7:6] (see Table 16). Once DCM is enabled by setting MR6 OP6 to 1, the DCM will start the WDQS duty cycle distortion measurement and provide the result on DERR0 for DWORD0 (PC0) and on DERR1 for DWORD1 (PC1) after waiting at least t<sub>DCMM</sub> time. An even number of continuous WDQS pulses will be required for the complete duration of the measurement cycle, from the MRS command that initiates the measurement until the t<sub>DCMM</sub> timing has been met. The result will remain valid until the DCM is disabled by setting MR6 OP6 back to 0. The DERR outputs will then return to their default state latest after t<sub>MOD</sub> has elapsed.

DCM results may be inaccurate if DCM circuit hysteresis is present. To increase the accuracy of this function, the DCM supports flipping the input by setting MR6 OP[7] to the opposite state and then repeating the measurement after the tDCMM timing.

Commands allowed while in this mode are REFab, REFpb, RFMab, RFMpb, RNOP, CNOP and MRS to disable the duty cycle monitor. Internal current spikes generated by the use of REFab, REFpb, RFMab and RFMpb commands in this mode may negatively impact the training result. Controllers that cannot account for this impact should avoid use of REFab, REFpb, RFMab, and RFMpb commands in this mode.

The DCM is not supported at CK clock frequencies lower than fCKDCA, as in the case of DCA.

Table 75 — DCM Measurement Result
<table><tr><td rowspan=1 colspan=1>WDQS Duty Cycle</td><td rowspan=1 colspan=1>Result (DERR0, DERR1)</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>&lt; 50%</td><td rowspan=1 colspan=1>LOW</td><td rowspan=2 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>≥50%</td><td rowspan=1 colspan=1>HIGH</td></tr><tr><td rowspan=1 colspan=3>NOTE 1 The result is valid a time tDcmm after enabling DCM</td></tr></table>

The following example command sequence may be used for WDQS duty cycle adjustment (see also Figure 90):

1. Enable both WDQS strobes;

2. Enable no flip DCM and wait for t<sub>DCMM</sub>;

3. Observe the measurement result via DERR0 and DERR1 outputs (No flip);

4. Enable DCM and wait for tDCMM;

5. Observe the measurement result via DERR0 and DERR1 outputs (Flip);

6. Disable DCM and wait for t<sub>MOD</sub>; DERR0 and DERR1 outputs return to their default state;

7. Issue an MRS command to set an appropriate DCA codes for both WDQS strobes and wait for t<sub>MOD</sub>;

8. Repeat steps 2 to 7 as needed;

9. Perform WDQS-to-CK alignment training.

6.11.3 Duty Cycle Monitor (DCM) (cont’d)  
![](images/1765e98962246cbc8d9dc0650ec41e0612df16b9e07243f7a42c49b258f50c43.jpg)  
NOTE 1 The host may send continuous WDQS pulses throughout the whole duty cycle adjustment procedure, in addition to the required WDQS pulses as shown in the figure.  
Figure 90 — Example Sequence for WDQS Duty Cycle Correction

Table 76 explains the relationship between MR6 OP[7] and DERR. For the accurate duty cycle adjustment, apply the DCA code corresponding to the averaged value of no flip result and flip result. Table 78 shows Mode Register for the DCM flip operation.

Table 76 — DCM Output Example
<table><tr><td rowspan=1 colspan=1>DCACode</td><td rowspan=1 colspan=1>-7</td><td rowspan=1 colspan=1>-6</td><td rowspan=1 colspan=1>-5</td><td rowspan=1 colspan=1>-4</td><td rowspan=1 colspan=1>-3</td><td rowspan=1 colspan=1>-2</td><td rowspan=1 colspan=1>-1</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>+1</td><td rowspan=1 colspan=1>+2</td><td rowspan=1 colspan=1>+3</td><td rowspan=1 colspan=1>+4</td><td rowspan=1 colspan=1>+5</td><td rowspan=1 colspan=1>+6</td><td rowspan=1 colspan=1>+7</td></tr><tr><td rowspan=1 colspan=1>No Flip</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>Flip</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td></tr></table>

Table 77 — Duty Cycle Monitor Timing
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Unit</td></tr><tr><td rowspan=1 colspan=1>Duty Cycle MonitorMeasurement time</td><td rowspan=1 colspan=1>tDCMM</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>μs</td></tr></table>

Table 78 — MR6 OP[7:6], DCM Control
<table><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Note</td></tr><tr><td rowspan=1 colspan=1>Flip inputs to cancel offset (DCM_Flip)</td><td rowspan=1 colspan=1>[7]</td><td rowspan=1 colspan=1>0 - No flip (default)1 - Flip</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>DCM_Start/Stop</td><td rowspan=1 colspan=1>[6]</td><td rowspan=1 colspan=1>0 - Stop (default)1 - Start</td><td rowspan=1 colspan=1></td></tr></table>

## 6.12 Rx Offset Calibration Training

## 6.12.1 Offset Calibration Training Description

HBM4 DRAM supports Rx offset calibration (RXoffC) training for adjusting DQ Rx as an optional feature. Support for the feature is indicated in the Device ID RXoffC bit field, which is started/stopped using MR8 OP1.

If supported, it is recommended to perform Rx offset calibration whenever training is performed whether as part of the power-up initialization process or during normal operation to cope with operating condition changes. Since Rx offset calibration affects DRAM write calibration training, Rx offset calibration training must be performed before VREFD training and WDQS-to-CK alignment.

Before the DRAM starts the training, the DQ channel should be floated by the host. If the DRAM requires other features for this training, the device shall automatically enable those features after the MRS is issued to start the training and shall be automatically disabled within tMOD after the MRS to disable the training is issued. See vendor datasheets for more details.

## 6.12.2 Offset Calibration Training Sequence

The following sequence must be satisfied for offset calibration training.

1. Issue MRS command for starting an offset calibration training. At this time, DQ channel should be floated by the Host.

2. Wait tOSCAL until the HBM4 DRAM completes the offset calibration.

3. Issue MRS command for exiting the offset calibration training.

![](images/6cd890d6b34adbab33f206d120a7c938c623532d49de45d498689c2442f8d2ac.jpg)  
Figure 91 — Rx Offset Calibration Training Timing

Table 79 — Rx Offset Calibration Training Time Parameter
<table><tr><td rowspan=1 colspan=1>Item</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Min.</td><td rowspan=1 colspan=1>Max.</td><td rowspan=1 colspan=1>Unit</td></tr><tr><td rowspan=1 colspan=1>Rx Offset Calibration Training Time</td><td rowspan=1 colspan=1>tOSCAL</td><td rowspan=1 colspan=1>–</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>μs</td></tr></table>

MR8 (Table 19) shows Mode Register for the Rx offset calibration. Rx Offset Calibration supportability defined in 177<sup>th</sup> bit of DEVICE\_ID WDR tells it is optional features and must be set to 0 if it is unavailable. See Table 132 for details.

## 6.13 Self Repair

The HBM4 DRAM supports self repair to help improve SiP (System in Package) assembly yields or to achieve a high level of system reliability by scanning for and repairing failures in the DRAM during the initialization process.

The IEEE1500 instructions SELF\_REP and SELF\_REP\_RESULTS are associated with the HBM4 self repair functionality. Self repair is initiated by setting WIR [7:0] to $^ { \bullet } 1 \mathbf { A } \mathbf { h } ^ { \bullet }$ which loads the SELF\_REP instruction. Since the instruction works on 8 or 16 channels at a time, WIR [13:8] must be set to $^ { 6 } 3 8 _ { \mathrm { h } } { \mathrm { \Omega } } ^ { , }$ or $\cdot 3 9 _ { \mathrm { h } } \cdot$ to select one half of the channels to run on, or must be set to $\mathrm { ^ { * } 3 \mathrm { A _ { h } ^ { * } , \ ^ { * } 3 \mathrm { B _ { h } ^ { * } , \ ^ { * } 3 \mathrm { C _ { h } ^ { * } , \mathrm { o r } \ ^ { * } 3 \mathrm { D _ { h } ^ { * } } } } } }$ to select one quarter of the channels to run on. A parallel operation of Self Repair on all groups of 8 or 16 channels are not supported. SELF\_REP clock source can be WRCK as a direct clock source or reference clock source or an internal clocked mode independent of WRCK and independent of any I/O functional clocks.

Setting REP\_TYPE field, bits[3:2], of the SELF\_REP instruction to $\cdot _ { 1 } \vert _ { \mathrm { b } } \ '$ will instruct the DRAM to start the first phase of the self repair process which is ‘self-test’ to identify any hard failures. The SELF\_REP instruction works on one SID at a time and must be run on each SID separately by using the SID\_SELECT field, bits [5:4]. The number of SELF\_REP instructions required to check all channels and SIDs is listed in Table 80. The SELFR\_REF\_RATE field, bits [7:6], must be set by the host to control temperature compensated refresh rate.

Table 80 — SELF\_REP Instruction vs Stack Height
<table><tr><td rowspan=1 colspan=1>StackHeight</td><td rowspan=1 colspan=1>SID</td><td rowspan=1 colspan=1>Min # SELF REP on 8 ChannelGroups to cover all 32 Channels</td><td rowspan=1 colspan=1>Min # SELF REP on 16 ChannelGroups to cover all 32 Channels</td></tr><tr><td rowspan=1 colspan=1>4H</td><td rowspan=1 colspan=1>SID0</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>8H</td><td rowspan=1 colspan=1>SID0, SID1</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>12H</td><td rowspan=1 colspan=1>SID0, SID1, SID2</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>6</td></tr><tr><td rowspan=1 colspan=1>16H</td><td rowspan=1 colspan=1>SID0, SID1, SID2, SID3</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>12</td></tr><tr><td rowspan=1 colspan=4>NOTE 1 This table only shows minimum number of channels to cover all channels by SELF_REP.HBM4 4/8/12/16Hi configuration supports both 8 and 16 channel grouping.</td></tr></table>

The ‘self-test’ will use vendor specific pattern(s) that detect hard failures in the HBM4 DRAM. Once the ‘self-test’ phase is complete the DRAM will proceed to the ‘auto-repair’ phase. The ‘auto-repair’ automatically repairs failed address(es) from the ‘self-test’ phase with the number of failed addresses repaired vendor specific.

SELF\_REP may be issued any time after the device has been properly initialized, specifically $\mathrm { t } _ { \mathrm { I N I T } 3 }$ has been met and the DRAM is in the all banks idle state. Since the SELF\_REP instruction operates on 8 channels at a time as selected by WIR[13:8], the 8 channels identified in $3 \mathrm { A _ { h } } , 3 \mathrm { B _ { h } } , 3 \mathrm { C _ { h } }$ or $3 \mathrm { D } _ { \mathrm { h } }$ or the 16 channels identified in $3 8 _ { \mathrm { h } }$ or $3 9 _ { \mathrm { h } }$ must be in the all banks idle state. See the vendor specification for the mapping of channels for $3 8 _ { \mathrm { h } }$ and $3 \mathrm { D } _ { \mathrm { h } } .$

During the self repair process the host can poll the DRAM for status using the SR\_PROGRESS field of the SELF\_REP instruction. The DRAM will report whether the “self-test” is in progress, the “auto-repair” is in progress or the self repair process has completed or not running. The SELF\_REP instruction must be kept in the WIR during this time.

## 6.13 Self Repair (cont’d)

Once the self repair process is complete, the SELF\_REP\_RESULTS instruction can be issued to read out the results. The DRAM will report the results for each SID and will indicate whether; i) fails remain, ii) unrepairable fails remain; iii) SELF\_REP should be run again; or iv) Self Repair has not run since INIT or no fails remain after most recent run.

If after running both the ‘self-test’ and ‘auto-repair’ phases the results indicate that fails remain, the SELF REP instruction can be issued to run only the ‘auto-repair’ phase to repair additional fails by setting the $\mathrm { R E P \_ T Y P E } : 0 \ ^ { \cdot } 1 0 _ { \mathrm { b } } ^ { \ }$ . With REP\_TYPE set to $\cdot _ { 1 0 _ { \mathrm { b } } } ,$ the DRAM will repair additional row addresses from the previous ‘self-test’. If additional fails remain, the host can continue to issue SELF\_REP instructions with REP $\mathrm { { T Y P E } = \cdot 1 0 _ { b } \cdot }$ , followed by SELF\_REP\_RESULTS, until the DRAM reports $\cdot _ { 0 0 _ { \mathrm { b } } } ,$ to indicate that there are no fails remaining. If the DRAM reports ‘11<sub>b</sub>’, this is an indication to the host to run SELF\_REP again with either REP\_TYPE set to ‘01<sub>b</sub>’ (‘self-test only) or $\cdot _ { 1 } \vert _ { \mathrm { b } } \ '$ (self-test and auto-repair) to load internal fail addresses from the ‘self -test’ phase.

With REP\_TYPE set to $\cdot 0 1 _ { \mathrm { b } } \cdot$ , the SELF\_REPAIR instruction will only run the ‘self-test’ phase and the host can check the results after completion to decide next steps.

If the host runs the ‘auto-repair’ only without previously having run the ‘self-test’ phase, then the SELF\_REP\_RESULTS instruction will report ‘00<sub>b</sub>’as there are no failing address(es).

If the DRAM reports “Unrepairable fails remain” on a channel, this indicates that there are not enough repair elements remaining to repair failed addresses latched during the ‘self-test’ phase. The host can decide whether to run self repair again to repair other channels or complete the repair process.

Once the self repair process is complete, the host must issue a reset of the DRAM by driving RESET\_n to low and then following the Initialization Sequence with Stable power.

The host is able to cancel the self repair in progress by using the SELF\_REP instruction with REP\_TYPE set to $\cdot _ { 0 0 _ { \mathrm { b } } } ,$ , however only the “self-test” phase can be cancelled. The SR\_PROGRESS field of the SELF\_REP will be set to ‘00<sub>b</sub>’ and the host must wait t<sub>SELF\_CANCEL</sub> before any additional SELF repair. If no further repair is needed, the host must reset the DRAM.

If the host does not use the polling to determine completion then the following timing parameters will indicate the completion of the REP\_TYPE.

Table 81 — SELF\_REPAIR Timings
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>REP_TYPE</td><td rowspan=1 colspan=1>Phase</td><td rowspan=1 colspan=1>Min/Max</td><td rowspan=1 colspan=1>Unit</td></tr><tr><td rowspan=1 colspan=1>tSELF_HEAL</td><td rowspan=1 colspan=1> $1 1 _ { \mathrm { b } }$ </td><td rowspan=1 colspan=1>Self-test and Auto-repair</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>S</td></tr><tr><td rowspan=1 colspan=1>tsELF_REP</td><td rowspan=1 colspan=1> $1 0 _ { \mathrm { b } }$ </td><td rowspan=1 colspan=1>Auto-repair</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>S</td></tr><tr><td rowspan=1 colspan=1>tsELF_NR</td><td rowspan=1 colspan=1> $0 1 _ { \mathrm { b } }$ </td><td rowspan=1 colspan=1>Self-test</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>S</td></tr><tr><td rowspan=1 colspan=1>tSELF_CANCEL</td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { b } }$ </td><td rowspan=1 colspan=1>Self-test cancel time</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>μs</td></tr></table>

## 6.13 Self Repair (cont’d)

Self repair resources are vendor specific. The Self repair resources can be shared with the hard/soft repair resources if the DRAM supports two or more resources per bank. The SHARED\_REP\_RES field of the DEVICE\_ID indicates whether the DRAM supports separate or shared resources. If the DRAM shares the resources the host can use the HS\_REP\_CAP instruction to tell how many resources are available for self repair. When resources shared, any repairs done by self repair will update the resources per bank. The number of repair done by the DRAM per SELF\_REP instruction is vendor specific.

If the DRAM shares resources with self repair, the DRAM must not use all the available resources in a bank. One resource per bank must be left for the host to perform soft repair. If the host desires to allow self repair to use all of the shared resources then the SHARED\_OVERRIDE (Table 143) field can be set to $^ { \circ } 1 \boldsymbol { \mathbf { \mathit { b } } } ^ { \prime }$ . If the resources are not shared the SHARED\_OVERRIDE field will be ignored. Before any self repair, the host is recommended to clear any soft repairs using the undo function on the channels the host plans to run self repair, or a chip reset. Failure to do so could result in the DRAM using the shared resources and operation is then not guaranteed, including loss of data. After the self repair is complete the host can perform soft repairs after checking if resources are available. Table 82 illustrates the expected behavior of the DRAM and the expected SEL\_REP\_RESULTS when SHARED\_OVERRIDE is set to $^ { \bullet } 0 ^ { \bullet }$ and ‘1’.

## 6.13 Self Repair (cont’d)

Table 82 — SELF\_REP – Expected DRAM Behavior When Resources Shared
<table><tr><td rowspan=2 colspan=1>Case</td><td rowspan=2 colspan=1>ResourceVSFails</td><td rowspan=1 colspan=7>Examples</td></tr><tr><td rowspan=1 colspan=1>Resource(s)beforeSELF_REP</td><td rowspan=1 colspan=1>Fails</td><td rowspan=1 colspan=1>Override(0 = default)</td><td rowspan=1 colspan=1>DRAMbehavior</td><td rowspan=1 colspan=1>Results</td><td rowspan=1 colspan=1>Resource(s)afterSELF_REP</td><td rowspan=1 colspan=1>SubsequentHard/Softrepair</td></tr><tr><td rowspan=2 colspan=1>1</td><td rowspan=2 colspan=1>Resources&lt; Fails</td><td rowspan=2 colspan=1>1</td><td rowspan=2 colspan=1>2</td><td rowspan=1 colspan=1>0 (No)</td><td rowspan=1 colspan=1>Norepair</td><td rowspan=1 colspan=1>Unrepairablefailsremain</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>1 (Yes)</td><td rowspan=1 colspan=1>Auto-repair</td><td rowspan=1 colspan=1>Unrepairablefailsremain</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=5></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2></td></tr><tr><td rowspan=2 colspan=1>2</td><td rowspan=2 colspan=1>Resources= Fails</td><td rowspan=2 colspan=1>2</td><td rowspan=2 colspan=1>2</td><td rowspan=1 colspan=1>0 (No)</td><td rowspan=1 colspan=1>Norepair</td><td rowspan=1 colspan=1>Unrepairablefailsremain</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>1 (Yes)</td><td rowspan=1 colspan=1>Auto-repair(s)1</td><td rowspan=1 colspan=1>No failsremain(Fails remain)²</td><td rowspan=1 colspan=1>0 (1)3</td><td rowspan=1 colspan=1>No (Yes)3</td></tr><tr><td rowspan=1 colspan=6></td><td rowspan=1 colspan=3></td></tr><tr><td rowspan=2 colspan=1>3</td><td rowspan=2 colspan=1>Resources&gt; Fails</td><td rowspan=2 colspan=1>3</td><td rowspan=2 colspan=1>2</td><td rowspan=1 colspan=1>0 (No)</td><td rowspan=1 colspan=1>Auto-repair(s)1</td><td rowspan=1 colspan=1>No failsremain(Fails remain)²</td><td rowspan=1 colspan=1>1 (2)4</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>1 (Yes)口</td><td rowspan=1 colspan=1>Auto-repair(s)1</td><td rowspan=1 colspan=1>No failsremain(Fails remain)²</td><td rowspan=1 colspan=1>1 (2)4</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=9>NOTE 1 The number of repairs per SELF_REP instruction is vendor specific.NOTE 2 If the DRAM does 1 repair per SELF REP then after the initial SELF REP the DRAM will report &#x27;fails remain&#x27; andthe host will need to issue a second SELF_REP to repair the other fail so that the results are &#x27;no fails remain&#x27;. If theDRAM repairs both fails in one SELF REP instruction then the results will be &#x27;no fails remain.NOTE 3 If the DRAM only does 1 repair per SELF_REP, the host has the option to do no further repair and leave theremaining resource for soft repair or use up the one remaining resource with an additional SELF REP. If the DRAMdoes more than 1 repair per SELF_REP then the host cannot do subsequent soft repair.NOTE 4For Case 3 the number of resources repaired depends on whether the initial SELF_REP repairs 1 fail or both.</td></tr></table>

## 6.13 Self Repair (cont’d)

Figure 92 provides a flow chart showing three flows for REP\_TYPE field of the SELF\_REP instruction.

![](images/7fb43d9004fa28920310e4b6c14433bcc8b1012f65b91b36552d77a8e39211f8.jpg)  
Figure 92 — Self Repair Flowchart

## 7.1 Absolute Maximum DC Rating

Table 83 — Absolute Maximum DC Ratings
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Rating</td><td rowspan=1 colspan=1>Unit</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Voltage on VDDc relative to Vss</td><td rowspan=1 colspan=1>VDDC</td><td rowspan=1 colspan=1>-0.3 to 1.4</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=1>Voltage on VDpo relative to Vss</td><td rowspan=1 colspan=1>VDDQ</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1,2,4</td></tr><tr><td rowspan=1 colspan=1>Voltage on VDDQL relative to Vss</td><td rowspan=1 colspan=1>VDDQL</td><td rowspan=1 colspan=1>-0.3 to 0.8</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=1>Voltage on Vpp relative to Vss</td><td rowspan=1 colspan=1>Vpp</td><td rowspan=1 colspan=1>-0.3 to 2.1</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=1>Voltage on any signal pin relative to Vss</td><td rowspan=1 colspan=1>VIN, VOUT</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1,2,4</td></tr><tr><td rowspan=1 colspan=1>Storage Temperature</td><td rowspan=1 colspan=1>TSTORAGE</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>℃</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=5>NOTE 1 Stresses greater than those listed under “Absolute Maximum Ratings&quot; may cause permanent damage to the device.This is a stress rating only and functional operation of the device at these or any other conditions above thoseindicated in the operational sections of this standard is not implied. Exposure to absolute maximum ratingconditions for extended periods may affect reliability.NOTE 2 See HBM4 Power-up and Initialization Sequence for the relationship between the power supplies.NOTE 3Storage temperature is the case surface temperature on the center/top side of the HBM4 device. For theMeasurement conditions, please refer to JESD51-2 standard.NOTE 4The vendor&#x27;s datasheet shall be consulted for the rating values.</td></tr></table>

## 7.2 Recommended DC Operating Condition

For HBM4, the need arose to define more than one VDDQ range due to the requirements of the HBM4 specification and device designs envisioned in the lifetime of HBM4. The typical levels listed in Table 84 represent the known values at the time of publication.

Vendor datasheets should be consulted for actual VDDQ voltage(s) supported, as factors such as process technology and supported system voltage(s) may require typical operating voltages to be added, dropped or maintained over time.

## 7.2 Recommended DC Operating Condition (cont’d)

Table 84 — Recommended DC Operating Condition
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Minimum</td><td rowspan=1 colspan=1>Typical</td><td rowspan=1 colspan=1>Maximum</td><td rowspan=1 colspan=1>Unit</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=3 colspan=1>Core Supply Voltage</td><td rowspan=3 colspan=1> $\mathrm { V _ { D D C } }$ </td><td rowspan=1 colspan=1>1.018</td><td rowspan=1 colspan=1>1.05</td><td rowspan=1 colspan=1>1.124</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=4>And / or</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0.97</td><td rowspan=1 colspan=1>1.00</td><td rowspan=1 colspan=1>1.07</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=7 colspan=1>I/O Supply Voltage</td><td rowspan=7 colspan=1> $\mathrm { V _ { D D Q } }$ </td><td rowspan=1 colspan=1>0.873</td><td rowspan=1 colspan=1>0.9</td><td rowspan=1 colspan=1>0.963</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=4>And / or</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>0.776</td><td rowspan=1 colspan=1>0.8</td><td rowspan=1 colspan=1>0.856</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=4>And / or</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>0.7275</td><td rowspan=1 colspan=1>0.75</td><td rowspan=1 colspan=1>0.8025</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=4>And / or</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>0.679</td><td rowspan=1 colspan=1>0.7</td><td rowspan=1 colspan=1>0.749</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>Supply Voltage forTX Driver Output Stage</td><td rowspan=1 colspan=1>VDDQL</td><td rowspan=1 colspan=1>0.38</td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1>0.44</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>Pump Voltage</td><td rowspan=1 colspan=1> $\mathrm { \Delta V _ { P P } }$ </td><td rowspan=1 colspan=1>1.746</td><td rowspan=1 colspan=1>1.8</td><td rowspan=1 colspan=1>1.95</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=7>NOTE 1 The voltage ranges are defined at the HBM4 DRAM micropillars. DC bandwidth is limited to 20MHz.NOTE 2 HBM4 must support at least one typical VDDQ voltage and the following tolerances must be supported. Theminimum value of VDDQ = 0.97 × typical VDDQ and the maximum value of VDDQ = 1.07 × typical VDDQ.Vendor datasheet must be consulted for actual VDDQ voltage.NOTE 3  HBM4 must support at least one typical VDDQ voltage and the following tolerances must be supported. Theminimum value of VDDC = 0.97 × typical VDDQ and the maximum value of VDDC = 1.07 × typical VDDC.</td></tr></table>

Table 85 — Operating Temperature
<table><tr><td rowspan=1 colspan=2>Parameter</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>JESD402-1OperatingJunction TempRange</td><td rowspan=1 colspan=1>Minimum</td><td rowspan=1 colspan=1>Maximum</td><td rowspan=1 colspan=1>Unit</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>OperatingTemperature</td><td rowspan=1 colspan=1>Standard</td><td rowspan=1 colspan=1> $\mathrm { T _ { N } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> $^ \mathrm { { \circ } } C$ </td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>OperatingTemperature(Optional)</td><td rowspan=1 colspan=1>Extended</td><td rowspan=1 colspan=1> $\mathrm { T _ { E } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> $\overline { { ^ \circ \mathrm { C } } }$ </td><td rowspan=1 colspan=1>1,2,3</td></tr><tr><td rowspan=1 colspan=8>NOTE 1 The operating temperature refers to the junction temperature of all memory die(s) and the optional logic die of theHBM4 DRAM. The host is required to monitor the operating temperature via the IEEE1500 test port instructionsTEMPERATURE and CHANÑEL_TEMPERATURE. The host is also required to monitor the CATTRIP outputthat signals if the junction temperature of any die in the HBM4 DRAM exceeds a catastrophic trip-point level thatcould result in permanent damage to the device.NOTE 2 HBM DRAM may require additional Refresh cycle. Refer to vendor datasheet.NOTE 3 HBM4 operating temperatures are vendor specific. Please see JESD402-1B or later for the TJopr ranges that can besupported and vendor specifications for the specific ranges supported.</td></tr></table>

## 7.4 Electrostatic Discharge Characteristics

Table 86 — Electrostatic Discharge Characteristics
<table><tr><td rowspan=2 colspan=1>Parameter</td><td rowspan=2 colspan=1>Symbol</td><td rowspan=1 colspan=1>Values</td><td rowspan=2 colspan=1>Unit</td><td rowspan=2 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>min.</td></tr><tr><td rowspan=1 colspan=1>PHY Human Body Model (HBM PHY)</td><td rowspan=1 colspan=1>ESDHBM_PHY</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>PHY Charged Device Model (CDM PHY)     I</td><td rowspan=1 colspan=1>ESDcDM_PHY</td><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>DA Human Body Model (HBM DA)</td><td rowspan=1 colspan=1>ESDHBM_DA</td><td rowspan=1 colspan=1>1000</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>DA Charged Device Model (CDM DA)</td><td rowspan=1 colspan=1>ESDcDM_DA</td><td rowspan=1 colspan=1>250</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=5>NOTE1PHY Human Body Model (HBM PHY), or ESDHBM_PHY, is not applicable for HBM DRAM.NOTE 2 Refer to JEP157A or later for more details.NOTE3Refer to ESDA/JEDEC Joint Standard JS-001 for measurement procedures.NOTE 4 Refer to ESDA/JEDEC Joint Standard JS-002 for measurement procedures.</td></tr></table>

## 8.1 Leakage Current

Table 87 — Input Leakage Current
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Minimum</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Unit</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Input leakage current for AWORD and DWORD inputs</td><td rowspan=1 colspan=1>IL</td><td rowspan=1 colspan=1>-50</td><td rowspan=1 colspan=1>50</td><td rowspan=1 colspan=1>μA</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=6>NOTE 1 Any input 0V ≤ VIN ≤ VDDQL. (All inputs pins including IEEE1500 not under test = 0V)</td></tr></table>

Table 88 — Input/Output Capacitance
<table><tr><td rowspan=3 colspan=1>Parameter</td><td rowspan=3 colspan=1>Symbol</td><td rowspan=1 colspan=16>Speed Bin (Gbps)</td><td rowspan=3 colspan=1>Unit</td></tr><tr><td rowspan=1 colspan=2>4.8</td><td rowspan=1 colspan=2>5.2</td><td rowspan=1 colspan=2>5.6</td><td rowspan=1 colspan=1>6.</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=2>6.4</td><td rowspan=1 colspan=2>6.8</td><td rowspan=1 colspan=2>7.2</td><td rowspan=1 colspan=2>8.0</td></tr><tr><td rowspan=1 colspan=1>Min.</td><td rowspan=1 colspan=1>Max.</td><td rowspan=1 colspan=1>Min.</td><td rowspan=1 colspan=1>Max.</td><td rowspan=1 colspan=1>Min.</td><td rowspan=1 colspan=1>Max.</td><td rowspan=1 colspan=1>Min.</td><td rowspan=1 colspan=1>Max.</td><td rowspan=1 colspan=1>Min.</td><td rowspan=1 colspan=1>Max.</td><td rowspan=1 colspan=1>Min.</td><td rowspan=1 colspan=1>Max.</td><td rowspan=1 colspan=1>Min.</td><td rowspan=1 colspan=1>Max.</td><td rowspan=1 colspan=1>Min.</td><td rowspan=1 colspan=1>Max.</td></tr><tr><td rowspan=1 colspan=1>Input/OutputCapacitance – DQs,DBI, DPAR, ECC, SEV</td><td rowspan=1 colspan=1>Cio</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1>pF</td></tr><tr><td rowspan=1 colspan=1>Input CapacitanceRow and pFColumn Address</td><td rowspan=1 colspan=1>CADDR</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1>pF</td></tr><tr><td rowspan=1 colspan=1>Input/OutputCapacitance – ReadStrobe</td><td rowspan=1 colspan=1>CRDQS</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1>pF</td></tr><tr><td rowspan=1 colspan=1>Input CapacitanceWrite Strobe</td><td rowspan=1 colspan=1>CWDQS</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1>pF</td></tr><tr><td rowspan=1 colspan=1>Input CapacitanceClock</td><td rowspan=1 colspan=1>Cck</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1>pF</td></tr><tr><td rowspan=1 colspan=1>Capacitance – DERR,AERR</td><td rowspan=1 colspan=1>CERROR</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1>pF</td></tr><tr><td rowspan=1 colspan=19>NOTE 1 This parameter is not subject to production test.</td></tr></table>

## 8.3 DQ Rx Voltage and Timings

![](images/bef45c29cb49e24ed47433584a51e19cfc20b27ffbfa1997305ed9fb8a05c6a4.jpg)  
Figure 93 — DQ Receiver Mask

The DQ input receiver mask for voltage and timing is shown in Figure 93 is applied per pin. The DQ Rx mask $\left( \mathrm { V } _ { \mathrm { D I V W } } , \mathrm { t } _ { \mathrm { D I V W } } \right)$ defines the area the input signal must not encroach in order for the DQ input receiver to successfully capture an input signal with a BER of lower than TBD. The mask is a receiver property.

$\mathrm { V _ { c e n t \_ D Q ( m i d ) } }$ is defined as the midpoint between the largest $\mathrm { V _ { c e n t \_ D Q } }$ voltage level and the smallest $\mathrm { V _ { c e n t \_ D Q } }$ voltage level across all DQ pins for a given DRAM TBD (Determined by DRAM $\mathrm { V } _ { \mathrm { R E F D } }$ training granularity, $\mathrm { i . e . , }$ component/channel/DWORD) level. Each DQ $\mathrm { V _ { c e n t } }$ is defined by the center, i.e., widest opening, of the cumulative data input eye as depicted in Figure 94. This clarifies that any DRAM TBD level variation must be accounted for within the DQ Rx mask.

![](images/112fd5ec5ad97206bacc53aa80b1e11d72bd2cf234edf9a0f7b6a052b92bb870.jpg)  
Figure 94 — Across DQ V<sub>REFD</sub> Voltage Variation

Table 89 — Input Receiver Voltage Level and Timings Specification
<table><tr><td rowspan=3 colspan=1>Parameter</td><td rowspan=3 colspan=1>Symbol</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=16>Speed Bin (Gbps)</td><td rowspan=3 colspan=1>Unit</td><td rowspan=3 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=2>4.8</td><td rowspan=1 colspan=2>5.2</td><td rowspan=1 colspan=2>5.6</td><td rowspan=1 colspan=2>6.0</td><td rowspan=1 colspan=2>6.4</td><td rowspan=1 colspan=2>6.8</td><td rowspan=1 colspan=2>7.2</td><td rowspan=1 colspan=2>7.6</td><td rowspan=1 colspan=2>8.0</td></tr><tr><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td></tr><tr><td rowspan=1 colspan=1>DQ RxMaskvoltage p-p</td><td rowspan=1 colspan=1>VDIVW</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>mV</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=1>Rx TimingWindowwith PSIJ</td><td rowspan=1 colspan=1>tDIVW</td><td rowspan=1 colspan=1>0.30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>UI</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Input SlewRate overVDIVW</td><td rowspan=1 colspan=1>SRIN_DIVW</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>V/ns</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>Rx singlepulseamplitude</td><td rowspan=1 colspan=1>VIHLDQ AC</td><td rowspan=1 colspan=1>190</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>190</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>190</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>190</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>190</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>190</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>190</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>190</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>190</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mV</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=22>NOTE 1 DQ Rx mask voltage and timing parameters are applied per lane and includes DRAM DQ to WDQS voltage AC noise impact for frequencies &gt;20 MHz at a fixed temperature on a die.NOTE 2 DQ Rx mask voltage $\mathrm { \Delta V _ { D I V W } }$ has to be centered around $\mathrm { V _ { c e n t \_ D Q ( m i d ) } } ,$ and is after RX offset calibration training if supported, as indicated in the RxoffCfield of the Device ID.NOTE 3 Input slew rate over $\mathrm { \Delta V _ { D I V W } }$ mask centered at $\mathrm { V _ { c e n t \_ D Q ( m i d ) } } .$ The input slew rate is for DRAM design only and is valid at the micro bump.The slew rate is an informative parameter.NOTE 4DQ single input pulse amplitude into the receiver has to meet or exceed $\mathrm { V _ { I H L D Q \_ A C } }$ at any point over the total UI. No timing requirementabove level. $\mathrm { V _ { I H L D Q \_ A C } }$ is the peak to peak voltage centered around $\mathrm { V _ { c e n t \_ D Q ( m i d ) } }$ such that $\mathrm { V _ { I H L \_ A C } } / 2$ min has to be met both above andbelow $\mathrm { V _ { c e n t \_ D Q ( m i d ) } . }$ </td></tr></table>

## 8.3 DQ Rx Voltage and Timings (cont’d)

DQ, WDQS Data-in at DRAM Latch

Center aligned to WDQS inter De-skew group

![](images/5952df69f9c3280b3e6462f9249f426cead8448fda5d1525b0189ab21a57462d.jpg)  
Center aligned to WDQS inter De-skew group  
All DQ signal groups center aligned to the strobe at the DRAM internal latch

![](images/efe84a58a2eb5ea8dc3eef38b917c6b6d30150275ed5950c1594773039917ba4.jpg)

DQ, WDQS Data-in at DRAM Bump  
![](images/b0db979992c0570aaa7900b4bb4f50799bed224026f0d7e65854cb3ae0a71f9e.jpg)

![](images/462c376e1c1d199b29649ee470ac7b77040992d3be6610d23082649b01851925.jpg)  
tWDQS2DQ\_I is measured at the center (midpoint) of the tDIVW window  
NOTE 1 DQx and DQy are in the same data de-skewing group (Ta) in a DWORD.  
NOTE 2 DQx represents the max tWDQS2DQx\_I in group Ta, and DQy represents the min tWDQS2DQy\_I in group Ta, in this example.  
NOTE 3 tWDQS2DQc\_I represents the max tWDQS2DQ\_I and tWDQS2DQb\_I represents the min tWDQS2DQ\_I in a DWORD, where Ta, Tb, and Tc are signals in each de-skewing group in this example. tWDQS2DQa\_I represents the reference of tWDQS2DQ\_I for comparison in this example.  
NOTE 4 Timing different between tWDQS2DQx\_I and tWDQS2DQy\_I represents the max tDQ2DQtra\_I, in this example.  
NOTE 5 Timing different between tWDQS2DQb\_I and tWDQS2DQc\_I represents the max tDQ2DQter\_I, in this example.  
NOTE 6 Refer to Table 44 for the signals that belong to each signal group.  
NOTE 7 The skew between the earliest and latest data input within a DWORD is defined by tDQ2DQter\_I(MAX). The skew among data inputs within a byte group is limited to tDQ2DQtra\_I(MAX), and tDQ2DQtra\_I is included in tDQ2DQter\_I.

Figure 95 — DQ to WDQS Timings (t<sub>WDQS2DQ\_I</sub>, t<sub>DQ2DQtra\_I</sub> and t<sub>DQ2DQter\_I</sub>) at DRAM Pins Referenced from the Internal Latch

## 8.3 DQ Rx Voltage and Timings (cont’d)

All of the timing terms in DQ to WDQS\_t are measured from the WDQS\_t/WDQS\_c to the center midpoint of the t<sub>DIVW</sub> window taken at the V<sub>DIVW</sub> voltage levels centered around $\mathrm { V _ { c e n t \_ D Q ( m i d ) } } .$ In Figure 95 the timings at the pins are referenced with respect to all DQ signal groups center aligned to the DRAM internal latch. The data to data offset in write de-skew group, t<sub>DQ2DQtra\_I</sub>, is defined as the difference between the min and max t<sub>WDQS2DQ\_I</sub> for a given de-skew group. The data to data offset in different write de-skew group, t<sub>DQ2DQter\_I</sub>, is defined as the difference between the min and max t<sub>WDQS2DQ\_I</sub> for a given DWORD. t<sub>WDQS2DQ\_O</sub> is defined as the WDQS to read data and RDQS offset.

![](images/671679d2c29e4cb9a570bc662a273440dc688e2be0e9b3fba6c957259eb06d2e.jpg)  
NOTE 1 tDQ2DQtra\_O is defined at the same input pattern for all DQ in the same de-skew group signals.

NOTE 2 tDQ2DQter\_O is defined at the skew between de-skew group signals (Ta, Tb in this example) at the latest valid transition of the associated DQ pins. tWDQS2DQx\_O represents the min tWDQS2DQ\_O and tWDQS2Dqy\_O represents the max tWDQS2DQ\_O, in this example.

NOTE 3 t<sub>DQSQtra</sub> is defined at the skew between RDQS to the last valid transition of the DQ pins in de-skew group T4.

NOTE 4 The skew between the earliest and latest data output within a DWORD including RDQS\_t/\_c is defined by tDQ2DQter\_O(max). The skew among data outputs within a byte group is limited to tDQ2DQtra\_O(MAX), and tDQ2DQtra\_O is included in tDQ2DQter\_O.

Figure 96 — Read Data Timing Definitions of t<sub>DQ2DQtra</sub>\_<sub>O</sub>, t<sub>DQ2DQter</sub>\_<sub>O</sub>, and t<sub>DQSQtra</sub>\_<sub>O</sub>

## 8.4 AWORD Signaling

Table 90 — AWORD Receiver Voltage Level Specification
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Unit</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Input HIGH Voltage</td><td rowspan=1 colspan=1> $\mathrm { \Delta V _ { I H C A } }$ </td><td rowspan=1 colspan=1> $\mathrm { V _ { R E F C A } } + 0 . 1$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1,3</td></tr><tr><td rowspan=1 colspan=1>Input LOW Voltage</td><td rowspan=1 colspan=1> $\mathrm { \Delta V _ { I L C A } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> $\overline { { \mathrm { V } _ { \mathrm { R E F C A } } - 0 . 1 } }$ </td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1,3</td></tr><tr><td rowspan=1 colspan=1>Command/Address Rx single pulse amplitude</td><td rowspan=1 colspan=1> $\mathrm { V _ { I H L C A \_ A C } }$ </td><td rowspan=1 colspan=1>240</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mV</td><td rowspan=1 colspan=1>2,3</td></tr><tr><td rowspan=1 colspan=6>NOTE 1VREFCA based input receiver enabled (see MR13, Table 24). For C, R, ARFU and APAR inputs.NOTE 2CA single input pulse amplitude into the receiver has to meet or exceed $\mathrm { V _ { I H L \_ A C } }$ at any point over the total UI.No timing requirement above level. $\mathrm { V _ { I H L C A \_ A C } }$ is the peak to peak voltage centered around VDDQL/2 such that $\mathrm { V } _ { \mathrm { I H L C A \_ A C } } / 2$ min has to be met both above and below ${ \dot { \mathrm {  ~ \cal ~ V ~ } } } _ { \mathrm { \scriptsize { D D Q L } } } / { \dot { 2 } } .$ NOTE 3 Parameter is applied to all speed bins.</td></tr></table>

![](images/e46a869316d86b09d80798103ba8f1843e3ac0b39f3352825667b20b19505c56.jpg)  
Figure 97 — CA Single Pulse Amplitude and Pulse Width

## 8.5 CK and WDQS Input Signaling

Table 91 — CK and WDQS Input Voltage Level Specification
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Unit</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>CK clock Input Differential InputVoltage</td><td rowspan=1 colspan=1>VIDCK</td><td rowspan=1 colspan=1>160</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mV</td><td rowspan=1 colspan=1>1,7</td></tr><tr><td rowspan=1 colspan=1>CK clock Differential InputCross-point Voltage</td><td rowspan=1 colspan=1> $\mathrm { V } _ { \mathrm { I X C K } }$ </td><td rowspan=1 colspan=1> $\mathrm { V } _ { \mathrm { D D Q L } } / 2 - 4 0 \mathrm { m V }$ </td><td rowspan=1 colspan=1> $\mathrm { V } _ { \mathrm { D D Q L } } / 2 + 4 0 \mathrm { m V }$ </td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>2,7</td></tr><tr><td rowspan=1 colspan=1>WDQS Differential InputVoltage</td><td rowspan=1 colspan=1>VIDWDQS</td><td rowspan=1 colspan=1>150</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mV</td><td rowspan=1 colspan=1>3,7</td></tr><tr><td rowspan=1 colspan=1>WDQS Differential InputCross-point Voltage</td><td rowspan=1 colspan=1> $\mathrm { V _ { I X W D Q S } }$ </td><td rowspan=1 colspan=1> $\overline { { \mathrm { V } _ { \mathrm { D D Q L } } / 2 - 3 0 \mathrm { m V } } }$ </td><td rowspan=1 colspan=1> $\overline { { \mathrm { V } _ { \mathrm { D D Q L } } / 2 + 3 0 \mathrm { m V } } }$ </td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>4,7</td></tr><tr><td rowspan=1 colspan=1>RDQS Differential OutputCross-point Voltage</td><td rowspan=1 colspan=1>VOXRDQS</td><td rowspan=1 colspan=1> $\mathrm { V } _ { \mathrm { D D Q L } } / 2 - \mathrm { T B D }$ </td><td rowspan=1 colspan=1> $\overline { { \mathrm { V } _ { \mathrm { D D Q L } } / 2 + \mathrm { T B D } } }$ </td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>5,6,7</td></tr><tr><td rowspan=1 colspan=1>WDQS Differential InputSlew Rate</td><td rowspan=1 colspan=1>SR_WDQS</td><td rowspan=1 colspan=1>TBD</td><td rowspan=1 colspan=1>TBD</td><td rowspan=1 colspan=1>V/ns</td><td rowspan=1 colspan=1>7</td></tr><tr><td rowspan=1 colspan=6>NOTE 1 Vıdck is the magnitude of the difference between the input level on CK_t and the input level on CK_c.NOTE 2The input reference level for timings referenced to CK is the point at which CK_t and CK_c cross.NOTE3 VıDwDQs is the magnitude of the difference between the input level on WDQS_t and the input level on WDQS_c.NOTE4The input reference level for timings referenced to WDQS is the point at which WDQS_t and WDQS_c cross.NOTE 5 Includes VDDQL, VDDQ AC noise impact of TBD mV (pk-pk) at the DRAM supply microbumps; AC noiseincludes system PDN impact.NOTE 6 This parameter is guaranteed by design at the DRAM micropillars with Output Timing reference load and ReadDBI enabled.NOTE 7Parameter is applied to all speed bins.</td></tr></table>

![](images/c3a6b0be79e794e289507d968085699be400a30c9325586c456919a3c23b7f2f.jpg)  
Figure 98 — CK Single Pulse

Table 92 — Differential Input Level for WDQS\_t, WDQS\_c
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>min</td><td rowspan=1 colspan=1>Max.</td><td rowspan=1 colspan=1>Unit</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>WDQS Differential Input High</td><td rowspan=1 colspan=1> $\mathrm { V _ { I H d i f f \_ W D Q S } }$ </td><td rowspan=1 colspan=1>TBD</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mV</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>WDQS Differential Input Low</td><td rowspan=1 colspan=1> $\mathrm { V _ { I L d i f f \_ W D Q S } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TBD</td><td rowspan=1 colspan=1>mV</td><td rowspan=1 colspan=1></td></tr></table>

Table 93 — Differential Input Slew Rate Definition for WDQS\_t, WDQS\_c
<table><tr><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>From</td><td rowspan=1 colspan=1>To</td><td rowspan=1 colspan=1>Defined by</td></tr><tr><td rowspan=1 colspan=1>WDQS Differential Input Slew Rate forRising Edge (WDQS_t – WDQS_c)</td><td rowspan=1 colspan=1> $\mathrm { V _ { I L d i f f \_ W D Q S } }$ </td><td rowspan=1 colspan=1>VIHdiff_WDQS</td><td rowspan=1 colspan=1> $| \mathrm { V } _ { \mathrm { I L d i f f \_ W D Q S } } - \mathrm { V } _ { \mathrm { I H d i f f \_ W D Q S } } |$  $/ \operatorname { T } _ { \mathrm { R d i f f } }$ </td></tr><tr><td rowspan=1 colspan=1>WDQS Differential Input Slew Rate forFalling Edge $( \mathrm { W D Q S } \_ { \mathrm { 1 } } ^ { \mathrm { ~ \cdot ~ } } \mathrm { W D Q S } \_ { \mathrm { c } } )$ </td><td rowspan=1 colspan=1> $\mathrm { V _ { I H d i f f \_ W D Q S } }$ </td><td rowspan=1 colspan=1> $\mathrm { V _ { I L d i f f \_ W D Q S } }$ </td><td rowspan=1 colspan=1> $| \mathrm { V } _ { \mathrm { I L d i f f \_ W D Q S } } - \mathrm { V } _ { \mathrm { I H d i f f \_ W D Q S } } |$  $/ \operatorname { T } _ { \mathrm { F d i f f } }$ </td></tr></table>

![](images/003be4412c49a2814ca3d7822a7d2b464af44b475abf80f6d7352146dbe182b7.jpg)  
Figure 99 — Differential Input Slew Rate Definition for WDQS\_t, WDQS\_c

## 8.6 Midstack Signaling

Table 94 — Midstack Parameter Specification
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Unit</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Input HIGH Voltage for RESET_n and WRST_n,WRCK, SELECTWIR, SHIFTWR,CAPTUREWR, UPDATEWR and WSI inputs</td><td rowspan=1 colspan=1> $\mathrm { V } _ { \mathrm { I H R } }$ </td><td rowspan=1 colspan=1> $\overline { { 0 . 7 \times \mathrm { V _ { D D Q } } } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>Input LOW Voltage for RESET n and WRST n,WRCK, SELECTWIR, SHIFTWR,CAPTUREWR, UPDATEWR and WSI inputs</td><td rowspan=1 colspan=1> $\operatorname { V } _ { \mathrm { I L R } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> $0 . 2 \times \mathrm { V } _ { \mathrm { D D Q } }$ </td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>Output HIGH Voltage for CATTRIP and WSOoutputs</td><td rowspan=1 colspan=1> $\mathrm { V } _ { \mathrm { O H R } }$ </td><td rowspan=1 colspan=1> $0 . 7 \times \mathrm { V } _ { \mathrm { D D Q } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Output LOW Voltage for CATTRIP and WSOoutputs</td><td rowspan=1 colspan=1> $\mathrm { V _ { O L R } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> $0 . 3 \times \mathrm { V } _ { \mathrm { D D Q } }$ </td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=6>NOTE 1 CMOS input receivers. For RESET_n, WRST_n, WRCK, SELECTWIR, SHIFTWR, CAPTUREWR,UPDATEWR and WSI inputs.</td></tr></table>

## 8.7 Transmit Driver Resistance

HBM4 drivers have programmable resistance settings with 20% accuracy. Driver targets (in Ohm) are shown in Table 95.

Table 95 — Transmit Driver Resistance Specification
<table><tr><td rowspan=1 colspan=1>Nominal (Ohm)</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=1>16.7</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=1>14.3</td><td rowspan=1 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=2>NOTE 1Transmit driver resistance have -20% of min. lower and +20% of upper tolerances,respect to each corresponding nominal valuesNOTE2Nominal values in this table follow corresponding Vddq1 × 0.5 level. SeeRecommended DC Operating Condition clauses.</td></tr></table>

![](images/73eacb69c128275c66e70ae2800e95b58d7312844827cd05c06e66e95c67d161.jpg)  
Figure 100 — Timing Reference Load

## 8.9 Output Voltage Level

Table 96 — Output Voltage Level
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Unit</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Output HIGH Voltage</td><td rowspan=1 colspan=1> $\overline { { \mathrm { { V } _ { O H } } } }$ </td><td rowspan=1 colspan=1> $\overline { { \mathrm { V _ { D D Q L } } / 2 + } }$ 60mV</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Output LOW Voltage</td><td rowspan=1 colspan=1> $\mathrm { \Delta V _ { O L } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> $\overline { { \mathrm { V } _ { \mathrm { D D Q L } } / 2 - 6 0 \mathrm { m V } } }$ </td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1></td></tr></table>

## 8.10 Output Rise and Fall Time

![](images/21daae1f9641d29cbff6d7118f1858bcd4a66f8879c18d309a639d1935287ab0.jpg)  
NOTE $\mathrm { T _ { R } = \left\{ \ C _ { T O T A L } \times ( \Delta V _ { O H } - V _ { O L } ) \right\} / \mathrm { I } ; T _ { F } = \left\{ \ C _ { T O T A L } \times ( \Delta V _ { O H } - V _ { O L } ) \right\} / \mathrm { I } } ,$ where I = Transmit Drive Current in mA.  
Figure 101 — Output Rise and Fall Definition

## 8.11 Overshoot/Undershoot

Table 97 — Overshoot/Undershoot Specification for AWORD and DWORD Signals
<table><tr><td rowspan=2 colspan=1>Parameter</td><td rowspan=1 colspan=9>Speed Bin (Gbps)</td><td rowspan=2 colspan=1>Unit</td><td rowspan=2 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>4.8</td><td rowspan=1 colspan=1>5.2</td><td rowspan=1 colspan=1>5.6</td><td rowspan=1 colspan=1>6.0</td><td rowspan=1 colspan=1>6.4</td><td rowspan=1 colspan=1>6.8</td><td rowspan=1 colspan=1>7.2</td><td rowspan=1 colspan=1>7.6</td><td rowspan=1 colspan=1>8.0</td></tr><tr><td rowspan=1 colspan=1>Maximum peakamplitudeallowed forovershoot area</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Maximum peakamplitudeallowed forundershoot area</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>0.12</td><td rowspan=1 colspan=1>V</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Maximumovershoot areaabove $\underline { { \mathrm { \Delta V _ { D D Q L } } } }$ </td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>mV-ns</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Maximumundershoot areabelow $\underline { { \mathrm { V } _ { \mathrm { S S } } } }$ </td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>mV-ns</td><td rowspan=1 colspan=1></td></tr></table>

![](images/50fbace5411048b2413bdfff40819b6c19beac138b99f65f3eeab0012d92c35c.jpg)  
Figure 102 — Overshoot, Undershoot Definition

## 9 IDD Specification

## 9.1 IDD and IPP Specification Parameters and Test Conditions

This clause defines operating current measurement conditions and loop pattern.

• I<sub>DD</sub> currents are measured as time-averaged currents with all $\mathrm { V _ { D D C } }$ microbumps of the HBM4 device under test tied together.

• I<sub>PP</sub> currents use the same definitions as I<sub>DD</sub> except that the current on the V<sub>PP</sub> supply is measured. All $\mathrm { \Delta V _ { P P } }$ microbumps of the HBM4 device under test are tied together for I<sub>PP</sub> current measurements.

I<sub>DDQ</sub> currents are measured as time-averaged currents with all V<sub>DDQ</sub> microbumps of the HBM4 device under test tied together are not included in the measurements. Instead, DRAM vendors shall provide simulated values using the I measurement-loop pattern as defined in Table 101.

I<sub>DDQL</sub> currents are measured as time-averaged currents with all V<sub>DDQL</sub> microbumps of the HBM4 device under test tied together. Output reference load $\mathrm { C _ { T O T A L } }$ is $2 . 5 \mathrm { p F } _ { \mathrm { : } }$ , and the simulated load driving current can be added to the IDDQL if vendor uses no load for this measurement.

• I , I , I and I measurements are taken with all channels of the HBM4 device simultaneously executing the same pattern. However, values in the vendor’s datasheet shall be given per channel.

For IDD measurements, the following definitions apply:

$\mathbf { \bar { \theta } } ^ { 6 } 0 ^ { 9 }$ and $^ { 6 6 } \mathrm { L O W } ^ { 5 }$ are defined as $\mathrm { { V } _ { I N } \leq \mathrm { { V } _ { I L } ( m a x ) ; } }$

$^ { 6 6 } 1 ^ { , 5 }$ and ${ } ^ { 6 6 } \mathrm { H I G H } '$ are defined as $\mathrm { { V } _ { I N } \geq \mathrm { { V } _ { I H } ( m i n ) ; } }$

• WL, RL, RAS and RTP are programmed to appropriate values;

• DBIac is enabled for Reads and Writes;

• SEV and parity are disabled;

• MD is enabled in MR9;

• CNOP/RNOP commands and all address inputs are stable during idle command cycles;

• Some I<sub>DD</sub> Measurement-Loop pattern use high order address bits RA13 which are not defined for all densities. In those cases, the respective undefined address bit(s) shall be kept LOW.

Basic $\mathrm { I _ { D D } }$ Measurement Conditions are described in Table 98.

• I<sub>DD</sub> Measurements are done after properly initializing the HBM4 device. This includes the pre-load of the memory array with data pattern used with I<sub>DD4R</sub> measurements.

• The I<sub>DD</sub> Measurement-Loop patterns shall be executed at least once before actual $\mathrm { I _ { D D } }$ measurement is started.

• For timing parameters used with I<sub>DD</sub> Measurement-Loop pattern: $\mathsf { n R C } = \mathsf { t R C / t _ { C K } } ; \mathsf { n R A S } = \mathsf { t _ { R A S } / t _ { C K } }$ n $\mathrm { { 3 P = t _ { R P } / t _ { C K } } }$ , and $\mathrm { n R F C } = \mathrm { t _ { R F C } / t _ { C K } }$ <sub>.</sub> If not already an integer, round up to the next integer.

## 9.1 IDD and IPP Specification Parameters and Test Conditions (cont’d)

![](images/de419c0f17792e5aef3831f5b6932c51ad8eea302f2f3e606de5b5c65aac9cdc.jpg)  
Figure 103 — Measurement Setup for IDD and IPP Measurements

Table 98 — Basic IDD/IDDQ/IPP/IDDQL Measurement Conditions
<table><tr><td colspan="1" rowspan="1">Parameter/Condition</td><td colspan="1" rowspan="1">Symbol</td></tr><tr><td colspan="1" rowspan="1">One Bank Activate Precharge Current:tck = tck(min); tRc, tRAs and tRp as defined in Table 99; R and C inputs are HIGH between validcommands; DQ, ECC and DBI inputs are LOW; bank and row addresses with ACT and PREcommands as defined in Table 100.</td><td colspan="1" rowspan="1">IDD0, IDDQ0,IPP0, IDDQL0</td></tr><tr><td colspan="1" rowspan="1">Precharge Power-down Current:Device in Precharge Power-Down is issued; $\mathrm { t _ { C K } = t _ { C K } ( m i n ) } ;$ all banks are idle; R0 input is LOW;R[9:1] and C inputs are HIGH; DQ, ECC and DBI inputs are LOW</td><td colspan="1" rowspan="1">IDD2P, IDDQ2P,IPP2P, IDDQL2P</td></tr><tr><td colspan="1" rowspan="1">Precharge Power-down Current with clock stop:Device in Precharge Power-Down is issued; CK t is LOW; CK c is HIGH; all banks are idle; R0input is LOW; R[9:1] and C inputs are HIGH; DQ, ECC and DBI inputs are LOW</td><td colspan="1" rowspan="1">IDD2P0,IDDQ2P0,IPP2P0,IDDQL2P0</td></tr><tr><td colspan="1" rowspan="1">Precharge Standby Current:tck = tck(min); all banks are idle; R and C inputs are HIGH; DQ, ECC and DBI inputs are LOW</td><td colspan="1" rowspan="1">IDD2N,IDDQ2N, IPP2N,IDDQL2N</td></tr><tr><td colspan="1" rowspan="1">Active Power-down Current:Device in Active Power-Down is issued; tck = tck(min); one bank is active; R0 input is LOW;R[9:1] and C inputs are HIGH; DQ, ECC and DBI inputs are LOW</td><td colspan="1" rowspan="1">IDD3P, IDDQ3P,IPP3P, IDDQL3P</td></tr><tr><td colspan="1" rowspan="1">Active Power-down Current with clock stop:Device in Active Power-Down is issued; CK t is LOW; CK c is HIGH; one bank is active; R0input is LOW; R[9:1] and C inputs are HIGH; DQ, ECC and DBI inputs are LOW</td><td colspan="1" rowspan="1">IDD3P0,IDDQ3P0,IPP3P0,IDDQL3P0</td></tr><tr><td colspan="1" rowspan="1">Active Standby Current:tck = tck(min); one bank is active; R and C inputs are HIGH; DQ, ECC and DBI inputs are LOW</td><td colspan="1" rowspan="1">IDD3N,IDDQ3N, IPP3N,IDDQL3N</td></tr><tr><td colspan="1" rowspan="1">Read Burst Current:tck = tck(min); all banks activated; continuous read burst across bank groups as defined in Table101; IOUT = 0 mA; Ctotal = 2.5 pF</td><td colspan="1" rowspan="1">IDD4R,IDDQ4R,IPP4R,IDDQL4R</td></tr><tr><td colspan="1" rowspan="1">Write Burst Current:tck = tck(min); all banks activated; continuous write burst across bank groups as defined in Table102.</td><td colspan="1" rowspan="1">IDD4W,IDDQ4W,IPP4w,IDDQL4W</td></tr><tr><td colspan="1" rowspan="1">All-bank Refresh Burst Current:tck = tck(min); tRFCab as defined Table 99; R and C inputs are HIGH between valid commands; DQ,ECC and DBI inputs are LOW</td><td colspan="1" rowspan="1">IDD5B,IDDQ5B,IPP5B,IDDQL5B</td></tr><tr><td colspan="1" rowspan="1">Per-bank Refresh Burst Current:tck = tck(min); Use tRFCpb and tRREFD as defined in Table 99; R and C inputs are HIGHbetween valid commands; DQ, ECC and DBI inputs are LOW; The order of bank is sequentialfrom BK0 to BK15 with sequential SID.</td><td colspan="1" rowspan="1">IDD5P,IDDQ5P,IPP5P,IDDQL5P</td></tr><tr><td colspan="1" rowspan="1">Self Refresh Current:                                         baR0 input is LOW; R[9:1] and C inputs are LOW; DQ, ECC and DBI inputs are LOW</td><td colspan="1" rowspan="1">IDD6, IDDQ6,IPP6, IDDQL6</td></tr><tr><td colspan="1" rowspan="1">All-Bank Interleave Read Current:One bank in each of the 4 bank groups activated and precharged at tRc(min) as defined in Table 99;continuous read burst across bank groups; Ctotal = 2.5 pF1</td><td colspan="1" rowspan="1">IDD7, IDDQ7,IPP7, IDDQL7</td></tr><tr><td colspan="1" rowspan="1">Reset Low Current:                              RESET_n is LOW; CK_t, CK_c, WDQS_t, WDQS_c are LOW; R and C inputs are LOW; DQ,ECC and DBI inputs are LOW; Note: Reset low current reading is valid once power is stable andRESET_n has been LOW for at least 1ms</td><td colspan="1" rowspan="1">IDD8, IDDQ8,IpP8, IDDQL8</td></tr></table>

## 9.1 IDD and IPP Specification Parameters and Test Conditions (cont’d)

Table 99 — Example of Timings used for IDD Measurement-Loop Pattern
<table><tr><td rowspan=1 colspan=4>Parameter</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Unit</td></tr><tr><td rowspan=1 colspan=4>tRC</td><td rowspan=1 colspan=1>48</td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=1 colspan=4>tRAS</td><td rowspan=1 colspan=1>33</td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=1 colspan=4>tRP</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=1 colspan=4>tRREFD</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=2 colspan=2>tRFCpb</td><td rowspan=1 colspan=2>24 Gb/die</td><td rowspan=1 colspan=1>240</td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=1 colspan=2>32 Gb/die</td><td rowspan=1 colspan=1>280</td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=8 colspan=1>tRFCab</td><td rowspan=4 colspan=1>24 Gb/die</td><td rowspan=1 colspan=1>4-High</td><td rowspan=1 colspan=1>3 Gb / channel</td><td rowspan=1 colspan=1>360</td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=1 colspan=1>8-High</td><td rowspan=1 colspan=1>6 Gb / channel</td><td rowspan=1 colspan=1>410</td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=1 colspan=1>12-High</td><td rowspan=1 colspan=1>9 Gb / channel</td><td rowspan=1 colspan=1>1        450</td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=1 colspan=1>16-High</td><td rowspan=1 colspan=1>12 Gb / channel</td><td rowspan=1 colspan=1>490</td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=4 colspan=1>32 Gb/die</td><td rowspan=1 colspan=1>4-High</td><td rowspan=1 colspan=1>4 Gb / channel</td><td rowspan=1 colspan=1>400</td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=1 colspan=1>8-High</td><td rowspan=1 colspan=1>8 Gb / channel</td><td rowspan=1 colspan=1>450</td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=1 colspan=1>12-High</td><td rowspan=1 colspan=1>12 Gb / channel</td><td rowspan=1 colspan=1>490</td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=1 colspan=1>16-High</td><td rowspan=1 colspan=1>16 Gb / channel</td><td rowspan=1 colspan=1>530</td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=1 colspan=6>NOTE 1 DRAM vendors may decide to use different values for tRAs and tRP; however, nRAS + nRP = nRCmust be achieved. nRAS = RU(tRAS/tCK), nRP = RU(tRP/tCK), nRFCpb = RU(tRFCpb/tCK),nRREFD = RU(tRREFD/tCK). If not already an integer, round up to the next integer.</td></tr></table>

## 9.1 IDD and IPP Specification Parameters and Test Conditions (cont’d)

Table 100 — IDD0 Measurement-Loop Pattern
<table><tr><td rowspan=1 colspan=1>Sub-Loop</td><td rowspan=1 colspan=1>CycleNumber</td><td rowspan=1 colspan=1>RowCommand</td><td rowspan=1 colspan=1>ColumnCommand</td><td rowspan=1 colspan=1>BankAddress(BA[3:0])</td><td rowspan=1 colspan=1>RowAddress(RA[13:0])</td><td rowspan=1 colspan=1>Col.Address(CA[4:0])</td></tr><tr><td rowspan=11 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>ACT - PC0</td><td rowspan=1 colspan=1>CNOP</td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>CNOP</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td></tr><tr><td rowspan=1 colspan=1> $^ 2$ </td><td rowspan=1 colspan=1>ACT - PC1</td><td rowspan=1 colspan=1>CNOP</td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td></tr><tr><td rowspan=1 colspan=1> $^ 3$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>CNOP</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td></tr><tr><td rowspan=1 colspan=1> $4$ </td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>CNOP</td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=5>Repeat pattern until cycle (nRAS)</td></tr><tr><td rowspan=1 colspan=1>nRAS + 1</td><td rowspan=1 colspan=1>PRE – PCO</td><td rowspan=1 colspan=1>CNOP</td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td></tr><tr><td rowspan=1 colspan=1>nRAS + 2</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>CNOP</td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td></tr><tr><td rowspan=1 colspan=1>nRAS + 3</td><td rowspan=1 colspan=1>PRE-PC1</td><td rowspan=1 colspan=1>CNOP</td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td></tr><tr><td rowspan=1 colspan=1>nRAS + 4</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>CNOP</td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=5>Repeat pattern until cycle (nRC</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>nRC</td><td rowspan=1 colspan=5>repeat sub-loop 0 pattern until cycle $( 2 \times \mathrm { n R C } - 1 ) ; \mathrm { u s e \ B A } = 0 5 _ { \mathrm { h \ a n d \ R A } } = 0 2 \mathrm { A A A _ { h } }$ instead</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>2×nRC</td><td rowspan=1 colspan=5>repeat sub-loop 0 pattern until cycle (3 × nRC - 1); use BA = 02h and RA = 01555hinstead</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>3×nRC</td><td rowspan=1 colspan=5>repeat sub-loop 0 pattern until cycle (4 × nRC - 1); use BA = 07h and RA = 02AAAhinstead</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>4×nRC</td><td rowspan=1 colspan=5>repeat sub-loop 0 pattern until cycle (5 × nRC - 1); use BA = 01h and RA = 01555hinstead</td></tr><tr><td rowspan=1 colspan=1> $5$ </td><td rowspan=1 colspan=1>5×nRC</td><td rowspan=1 colspan=5>repeat sub-loop 0 pattern until cycle $( 6 \times \mathrm { n R C } - 1 ) ; \mathrm { u s e \ B A } = 0 6 _ { \mathrm { h } } \mathrm { a n d \ R A } = 0 2 \mathrm { A A A _ { h } }$ instead</td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>6×nRC</td><td rowspan=1 colspan=5>repeat sub-loop 0 pattern until cycle (7 × nRC - 1); use BA = 03h and RA = 01555hinstead</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>7×nRC</td><td rowspan=1 colspan=5>repeat sub-loop 0 pattern until cycle (8 × nRC - 1); use BA = 04h and RA = 02AAAhinstead</td></tr><tr><td rowspan=1 colspan=1>8 to 15</td><td rowspan=1 colspan=6>for 16-bank devices: repeat sub-loops 0 to 7 pattern; use BA3 = 1 instead, maintain SID[1:0] = 00</td></tr><tr><td rowspan=1 colspan=1>16 to 31</td><td rowspan=1 colspan=6>for 8-High,12-High and 16-High devices: repeat sub-loops 0, 1, and 2 patterns; use SID[1:0] = 01instead</td></tr><tr><td rowspan=1 colspan=1>32 to 47</td><td rowspan=1 colspan=6>for 12-High and 16-High devices: repeat sub-loops 0, 1, and 2 pattern; use SID[1:0] = 10 instead</td></tr><tr><td rowspan=1 colspan=1>48 to 63</td><td rowspan=1 colspan=6>for 16-High devices: repeat sub-loops 0, 1, and 2 patterns; use SID[1:0] = 11 instead</td></tr><tr><td rowspan=1 colspan=7>NOTE 1 ACT is a 1.5 cycle command. The falling edge of the second cycle is a RNOP</td></tr></table>

## 9.1 IDD and IPP Specification Parameters and Test Conditions (cont’d)

Table 101 — IDD4R Measurement-Loop Pattern
<table><tr><td rowspan=1 colspan=1>Sub-Loop</td><td rowspan=1 colspan=1>CycleNumber</td><td rowspan=1 colspan=1>RowCommand</td><td rowspan=1 colspan=1>ColumnCommand</td><td rowspan=1 colspan=1>Row BankAddress(BA[3:0])</td><td rowspan=1 colspan=1>Col.BankAddress(BA[3:0])</td><td rowspan=1 colspan=1>RowAddress(RA[13:0])</td><td rowspan=1 colspan=1>Col.Address(CA[4:0])</td><td rowspan=1 colspan=1>DataPattern(1 Byte)</td></tr><tr><td rowspan=32 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC0</td><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC1</td><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ - PC0</td><td rowspan=1 colspan=1> $0  { 2 _ { \mathrm { h } } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ - PC1</td><td rowspan=1 colspan=1> $0  { 2 _ { \mathrm { h } } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC0</td><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC1</td><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC0</td><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC1</td><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC0</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC1</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ - PC0</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC1</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC0</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ -PC1</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ - PC0</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC1</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC0</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>17</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC1</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ - PC0</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>19</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ - PC1</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ - PC0</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>21</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ - PC1</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>22</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC0</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>23</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC1</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC0</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC1</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>26</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ - PC0</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>27</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC1</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>28</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ - PC0</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>29</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ - PC1</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC0</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>31</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ - PC1</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>repeat sub-</td><td rowspan=1 colspan=1>loop 0 pattern; us</td><td rowspan=1 colspan=2>e RBA0 = 1 and CBA0 = 1 in</td><td rowspan=1 colspan=3>stead, maintain SID[1:0]=00</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=7>repeat sub-loop 0 and 1 pattern; use RBA1 = 0 and CBA1 = 1 instead, maintain SID[1:0]=00RNOP, CNOP 2-cycle before SID change to meet tCCDR</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=7>for 8-High,12-High and 16-High devices: repeat sub-loops 0,1 and 2 pattern; use SID[1:0] = 01instead</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=7>for 12-High and 16-High devices: repeat sub-loops 0,1 and 2 pattern; use SID[1:0] = 10 instead</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=7>for 16-High devices: repeat sub-loops 0,1 and 2 pattern; use SID[1:0] = 11 instead</td></tr></table>

## 9.1 IDD and IPP Specification Parameters and Test Conditions (cont’d)

Table 101 — IDD4R Measurement-Loop Pattern (cont’d)
<table><tr><td>NOTE 1</td><td>Pattern A for a Byte (BL0 to BL7)  $: 0 0 _ { \mathrm { h } } , 3 \mathrm { C _ { h } , F 0 _ { h } , 6 9 _ { h } , A A _ { h } , F F _ { h } , C 3 _ { h } , 5 5 _ { h } }$ </td></tr><tr><td>NOTE 2</td><td>Pattern B for a Byte (BL0 to BL7) :  $\mathrm { F O _ { h } , C C _ { h } , O O _ { h } , 9 9 _ { h } , 5 A _ { h } , O F _ { h } , 3 3 _ { h } , A 5 _ { h } }$ </td></tr><tr><td>NOTE3</td><td>Pattern C for a Byte (BL0 to BL7)  $\mathrm { : 3 3 _ { h } , 0 F _ { h } , C 3 _ { h } , 5 A _ { h } , 9 9 _ { h } , C C _ { h } , F O _ { h } , 6 6 _ { h } }$ </td></tr><tr><td>NOTE4</td><td>Pattern D for a Byte (BL0 to BL7) :  $\mathrm { C 3 _ { h } , F F _ { h } , 3 3 _ { h } , A A _ { h } , 6 9 _ { h } , 3 C _ { h } , 0 0 _ { h } , 9 6 _ { h } }$ </td></tr><tr><td></td><td>NOTE 5 Vendors may provide IDD4/7 values based on worse toggle patterns reflecting internal bus architecture.</td></tr></table>

## 9.1 IDD and IPP Specification Parameters and Test Conditions (cont’d)

Table 102 — IDD4W Measurement-Loop Pattern
<table><tr><td rowspan=1 colspan=1>Sub-Loop</td><td rowspan=1 colspan=1>CycleNumber</td><td rowspan=1 colspan=1>RowCommand</td><td rowspan=1 colspan=1>ColumnCommand</td><td rowspan=1 colspan=1>Row BankAddress(BA[3:0])</td><td rowspan=1 colspan=1>Col.BankAddress(BA[3:0])</td><td rowspan=1 colspan=1>RowAddress(RA[13:0])</td><td rowspan=1 colspan=1>Col.Address(CA[4:0])</td><td rowspan=1 colspan=1>DataPattern(1 Byte)</td></tr><tr><td rowspan=32 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC0</td><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC1</td><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC0</td><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE - PC1</td><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE - PC0</td><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE - PC1</td><td rowspan=1 colspan=1> $0  { 2 _ { \mathrm { h } } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $1 \mathrm { A } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC0</td><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE - PC1</td><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC0</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE –PC1</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC0</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE - PC1</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC0</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC1</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC0</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC1</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC0</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>17</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE - PC1</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC0</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>19</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE -PC1</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC0</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>21</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE –PC1</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>22</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC0</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>23</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE –PC1</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC0</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE - PC1</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>26</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC0</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>27</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE - PC1</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>28</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE - PC0</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>29</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC1</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC0</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>31</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>WRITE – PC1</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=7>repeat sub-loop 0 pattern; use RBA0 = 1 and $\mathrm { C B A } 0 = 1$ instead, maintain SID[1:0]=00</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=7>repeat sub-loop 0 and 1 pattern; use RBA1 = 0 and CBA1 = 1 instead, maintain SID[1:0]=00</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=7>for 8-High,12-High and 16-High devices: repeat sub-loops 0,1 and 2 pattern; use SID[1:0] = 01instead</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=7>for 12-High and 16-High devices: repeat sub-loops 0,1 and 2 pattern; use SID[1:0] = 10 instead</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=7>for 16-High devices: repeat sub-loops 0,1 and 2 pattern; use SID[1:0] = 11 instead</td></tr></table>

## 9.1 IDD and IPP Specification Parameters and Test Conditions (cont’d)

Table 102 — IDD4W Measurement-Loop Pattern (cont’d)
<table><tr><td>NOTE 1</td><td>Pattern A for a Byte (BL0 to BL7  $) : 0 0 \mathrm { { h } , 3 C \mathrm { { h } , F 0 _ { h } , 6 9 \mathrm { { h } , A A _ { h } , F F _ { h } , C 3 _ { h } , 5 5 _ { h } } } }$ </td></tr><tr><td>NOTE 2</td><td>Pattern B for a Byte (BL0 to BL7) :  $\mathrm { F O _ { h } , C C _ { h } , O O _ { h } , 9 9 _ { h } , 5 A _ { h } , 0 F _ { h } , 3 3 _ { h } , A 5 _ { h } }$ </td></tr><tr><td>NOTE3</td><td>Pattern C for a Byte (BL0 to BL7) :  $3 3 _ { \mathrm { h } } , 0 \mathrm { F _ { h } , C 3 _ { \mathrm { h } } , 5 A _ { \mathrm { h } } , 9 9 _ { \mathrm { h } } , C C _ { h } , F 0 _ { h } , 6 6 _ { h } }$ </td></tr><tr><td>NOTE 41</td><td>Pattern D for a Byte (BL0 to BL7) :  $\mathrm { C 3 _ { h } , F F _ { h } , 3 3 _ { h } , A A _ { h } , 6 9 _ { h } , 3 C _ { h } , 0 0 _ { h } , 9 6 _ { h } }$ </td></tr><tr><td></td><td>NOTE 5 Vendors may provide IDD4/7 values based on worse toggle patterns reflecting internal bus architecture.</td></tr></table>

## 9.1 IDD and IPP Specification Parameters and Test Conditions (cont’d)

Table 103 — IDD5P Measurement-Loop Pattern
<table><tr><td rowspan=1 colspan=1>Sub-Loop</td><td rowspan=1 colspan=1>CycleNumber</td><td rowspan=1 colspan=1>Row Command</td><td rowspan=1 colspan=1>Column Command</td><td rowspan=1 colspan=1>Row Bank Address $( \mathbf { S I D } [ 1 { : } 0 ] , \mathbf { B A } [ 3 { : } 0 ] )$ </td></tr><tr><td rowspan=5 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>PER-BANK REFRESH – PC0</td><td rowspan=1 colspan=1>CNOP</td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } } , 0 0 _ { \mathrm { h } }$ </td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>CNOP</td><td rowspan=1 colspan=1> $\mathrm { N } / \mathrm { A }$ </td></tr><tr><td rowspan=1 colspan=1> $^ 2$ </td><td rowspan=1 colspan=1>PER-BANK REFRESH – PC1</td><td rowspan=1 colspan=1>CNOP</td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } } , 0 0 _ { \mathrm { h } }$ </td></tr><tr><td rowspan=1 colspan=1> $^ 3$ </td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>CNOP</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>repeat RNOP until cycle (nRREFD-1)</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>nRREFD</td><td rowspan=1 colspan=3>repeat sub-loop 0 pattern until cycle $( 2 \times \mathrm { n R R E F D - 1 } ) ;$ use $\mathrm { B A } { = } 0 5 _ { \mathrm { h } }$ instead</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>2×nRREFD</td><td rowspan=1 colspan=3>repeat sub-loop 0 pattern until cycle $( 3 \times \mathrm { n R R E F D - 1 } ) ;$ use $\mathrm { B A } { = } 0 2 _ { \mathrm { h } }$ instead</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>3×nRREFD</td><td rowspan=1 colspan=3>repeat sub-loop 0 pattern until cycle $( 4 \times \mathrm { n R R E F D - 1 } ) ;$ use $\mathrm { B A } { = } 0 7 _ { \mathrm { h } }$ instead</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>4×nRREFD</td><td rowspan=1 colspan=3>repeat sub-loop 0 pattern until cycle $( 5 \times \mathrm { n R R E F D - 1 } ) ;$ use $\mathrm { B A } { = } 0 1 _ { \mathrm { h } }$ instead</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>5×nRREFD</td><td rowspan=1 colspan=3>repeat sub-loop 0 pattern until cycle $( 6 \times \mathrm { n R R E F D - 1 } ) ;$ use $\mathrm { B A } { = } 0 6 _ { \mathrm { h } }$ insteadV</td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>6×nRREFD</td><td rowspan=1 colspan=3>repeat sub-loop 0 pattern until cycle $( 7 \times \mathrm { n R R E F D - 1 } ) ;$ use $\mathrm { B A } { = } 0 3 _ { \mathrm { h } }$ instead</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>7×nRREFD</td><td rowspan=1 colspan=3>repeat sub-loop 0 pattern until cycle $( { 8 \times \mathrm { n R R E F D - 1 } } ) ;$ use $B { \mathrm { A } } { = } 0 4 _ { \mathrm { h } }$ instead</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=4>repeat sub-loops 0 to 7 pattern; use $\mathrm { B A } 3 { = } 1$ instead</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=4>for 4-High devices: wait for nRFCpbfor all other devices: repeat sub-loops 0 to 15 pattern; use SID[1:0] = 01h instead</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=4>for 8-High devices: wait for (nRFCpb – 15 × nRREFD)for 12-High and 16-High devices: repeat sub-loops 0 to 15 pattern; use SID[ $1 { : } 0 ] = 0 2 _ { \mathrm { h } }$ instead</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=4>for 12-High 32Gb devices: wait for (nRFCpb – 31 × nRREFD)for 16-High devices: repeat sub-loops 0 to 15 pattern; use $\mathrm { S I D } [ 1 { : } 0 ] = 0 3 _ { \mathrm { h } }$ instead</td></tr><tr><td rowspan=1 colspan=5>NOTE 1 nRFCpb = RU(tRFCpb/tCK), nRREFD = RU(tRREFD/tCK). If not already an integer, round up to thenext integer.</td></tr></table>

## 9.1 IDD and IPP Specification Parameters and Test Conditions (cont’d)

Table 104 — IDD7 Measurement-Loop Pattern
<table><tr><td rowspan=1 colspan=1>Sub-Loop</td><td rowspan=1 colspan=1>CycleNumber</td><td rowspan=1 colspan=1>RowCommand</td><td rowspan=1 colspan=1>ColumnCommand</td><td rowspan=1 colspan=1>RowBankAddress(BA[3:0])</td><td rowspan=1 colspan=1>Col. BankAddress(BA[3:0])</td><td rowspan=1 colspan=1>RowAddress(RA[13:0])</td><td rowspan=1 colspan=1>Col.Address(CA[4:0])</td><td rowspan=1 colspan=1>DataPattern(1 Byte)</td></tr><tr><td rowspan=32 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=2 colspan=1>ACT–PC0</td><td rowspan=1 colspan=1>READ-PC0</td><td rowspan=2 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=2 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>READ –PC1</td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=2 colspan=1>ACT–PC1</td><td rowspan=1 colspan=1>READ – PC0</td><td rowspan=2 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=2 colspan=1>01555h</td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>READ - PC1</td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ - PC0</td><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $1 \mathrm { A } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ –PC1</td><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC0</td><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ –PC1</td><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=2 colspan=1>ACT-PC0</td><td rowspan=1 colspan=1>READ – PC0</td><td rowspan=2 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=2 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>READ-PC1</td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>10</td><td rowspan=2 colspan=1>ACT-PC1</td><td rowspan=1 colspan=1>READ -PC0</td><td rowspan=2 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=2 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>READ –PC1</td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ –PC0</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC1</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ – PC0</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ - PC1</td><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=2 colspan=1>ACT -PC0</td><td rowspan=1 colspan=1>READ -PC0</td><td rowspan=2 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=2 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>17</td><td rowspan=1 colspan=1>READ - PC1</td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>18</td><td rowspan=2 colspan=1>ACT-PC1</td><td rowspan=1 colspan=1>READ -PC0</td><td rowspan=2 colspan=1>X   $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=2 colspan=1>01555h</td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>19</td><td rowspan=1 colspan=1>READ -PC1</td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ-PCO</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>21</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ -PC1</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 1 5 5 5 \mathrm { s } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>22</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ - PC0</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>23</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READ - PC1</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>01555h</td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>24</td><td rowspan=2 colspan=1>ACT – PC0</td><td rowspan=1 colspan=1>READA – PC0</td><td rowspan=2 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=2 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>READA- PC1</td><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern A</td></tr><tr><td rowspan=1 colspan=1>26</td><td rowspan=2 colspan=1>ACT-PC1</td><td rowspan=1 colspan=1>READA – PC0</td><td rowspan=2 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=2 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>27</td><td rowspan=1 colspan=1>READA- PC1</td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern B</td></tr><tr><td rowspan=1 colspan=1>28</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READA – PC0</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>29</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READA–PC1</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Pattern C</td></tr><tr><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READA – PC0</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>31</td><td rowspan=1 colspan=1>RNOP</td><td rowspan=1 colspan=1>READA - PC1</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1> $0 2 \mathrm { A A A _ { h } }$ </td><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Pattern D</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=7>repeat sub-loop 0 pattern; use $\mathrm { R B A } 0 = 1$ and $\mathrm { C B A } 0 = 1$ instead, maintain SID[1:0]=00</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=7>repeat sub-loop 0 and 1 pattern; use $\mathrm { R B A l } = 0$ and CBA1 = 1 instead, maintain SID[1:0]=00RNOP, CNOP 2-cycle before SID change to meet tCCDR</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=7>for 8-High,12-High and 16-High devices: repeat sub-loops 0,1 and 2 pattern; use SID[1:0] = 01instead</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=7>for 12-High and 16-High devices: repeat sub-loops 0,1 and 2 pattern; use SID[1:0] = 10 instead</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=7>for 16-High devices: repeat sub-loops 0,1 and 2 pattern; use SID[1:0] = 11 instead</td></tr></table>

## 9.1 IDD and IPP Specification Parameters and Test Conditions (cont’d)

Table 104 — IDD7 Measurement-Loop Pattern (cont’d)
<table><tr><td>NOTE 1</td><td>Pattern A for a Byte (BL0 to BL7) :  $0 0 _ { \mathrm { h } } , 3 C _ { \mathrm { h } } , \mathrm { F } 0 _ { \mathrm { h } } , 6 9 _ { \mathrm { h } } , \mathrm { A A _ { \mathrm { h } } , F F _ { \mathrm { h } } , C 3 _ { \mathrm { h } } , 5 5 _ { \mathrm { h } } }$ </td></tr><tr><td>NOTE 2</td><td>Pattern B for a Byte (BL0 to BL7) :  $\mathrm { F O _ { h } , C C _ { h } , O O _ { h } , 9 9 _ { h } , 5 A _ { h } , O F _ { h } , 3 3 _ { h } , A 5 _ { h } }$ </td></tr><tr><td>NOTE 3</td><td>Pattern C for a Byte (BL0 to BL7) :  $3 3 _ { \mathrm { h } } , 0 \mathrm { F _ { h } , C 3 h , 5 A _ { h } , 9 9 _ { h } , C C _ { h } , F 0 _ { h } , 6 6 _ { h } }$ </td></tr><tr><td>NOTE 4</td><td>Pattern D for a Byte (BL0 to BL7) :  $\mathrm { C 3 _ { h } , F F _ { h } , 3 3 _ { h } , A A _ { h } , 6 9 _ { h } , 3 C _ { h } , 0 0 _ { h } , 9 6 _ { h } }$ </td></tr><tr><td>NOTE 5</td><td>Vendors may provide IDD4/7 values based on worse toggle patterns reflecting internal bus architecture.</td></tr><tr><td>NOTE 6</td><td>ACT is a 1.5 cycle command. The falling edge of the second cycle is a RNOP.</td></tr></table>

## 9.2 IDD and IPP Specifications

IDD and IPP values are valid for the full operating range of voltage and temperature unless otherwise noted.

Table 105 — IDD and IPP Specification Example
<table><tr><td rowspan=2 colspan=1>Symbol</td><td rowspan=1 colspan=2>Speed Bin</td><td rowspan=2 colspan=1>Unit</td><td rowspan=2 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>IDD (Max)</td><td rowspan=1 colspan=1>IPP (Max)</td></tr><tr><td rowspan=1 colspan=1>IDD0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mA</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>IDD2P</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mA</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>IDD2P0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mA</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>IDD2N</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mA</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>IDD3P</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mA</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>IDD3P0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mA</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>IDD3N</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mA</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>IDD4R</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mA</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>IDD4W</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mA</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>IDD5B</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mA</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>IDD5P</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mA</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>IDD6x</td><td rowspan=1 colspan=2>See Separate Table</td><td rowspan=1 colspan=1>mA</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>IDD7</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mA</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>IDD8</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>mA</td><td rowspan=1 colspan=1></td></tr></table>

## 9.3 IDD6 Specification

Table 106 — IDD6 Specification
<table><tr><td colspan="2">Symbol</td><td>Temperature Range</td><td>Value</td><td>Unit</td><td>Notes</td></tr><tr><td colspan="2">IDD6N</td><td> $\overline { { 0 ^ { \circ } C \cdot \mathrm { T _ { N } } } }$ </td><td></td><td>mA</td><td>2,3,7</td></tr><tr><td colspan="2">IDD6E (Optional)</td><td> $0 ^ { \circ } C - \mathrm { T } _ { \mathrm { E } }$ </td><td></td><td>mA</td><td>1,3,4,7</td></tr><tr><td colspan="2">IDD6R (Optional)</td><td> $0 ^ { \circ } \mathrm { C } \cdot \mathrm { T } _ { \mathrm { R } }$ </td><td></td><td>mA</td><td>3,5,7</td></tr><tr><td colspan="2" rowspan="3">IDD6A (Optional)</td><td> $\overline { { 0 ^ { \circ } C \cdot \mathrm { T } _ { a } } }$ </td><td></td><td>mA</td><td>3,5,5,6</td></tr><tr><td> $\mathrm { T _ { b } - T _ { y } ( o p t i o n a l ) }$ </td><td></td><td> $\mathrm { m A }$ </td><td>3,5,5,6</td></tr><tr><td> $\mathrm { T _ { z } - T _ { O P E R m a x } }$ </td><td></td><td> $\mathrm { m A }$ </td><td>3,5, 5, 6,8</td></tr><tr><td>NOTE1 NOTE 2 NOTE3 NOTE4 NOTE5 NOTE 6 are supplier/design specific. Temperature ranges are intended to denote the nominal trip points for the internal temperature sensor to bracket discrete self refresh rates internal to the DRAM. Refer to</td><td colspan="4">Max. values for IDD currents considering worst case conditions of process, temperature and voltage. Applicable for MR0 settings OP2=0. Supplier data sheets include a max value. IDD6E is only specified for devices which support the Extended Temperature Range feature. IDD6A is only specified for devices which support the Temperature Controlled Self Refresh feature enabled by MR0 with OP2=1. The number of discrete temperature ranges supported and the associated  $\mathrm { T } _ { \mathrm { a } } - \mathrm { T } _ { \mathrm { z } } ,$  and  $\mathrm { T _ { O P E R m a x } }$  values</td></tr></table>

10 AC Timings

Table 107 — Timings Parameters
<table><tr><td rowspan=3 colspan=1>Parameter</td><td rowspan=3 colspan=1>Symbol</td><td rowspan=1 colspan=11>Speed Bin²</td><td rowspan=2 colspan=1>Unit</td><td rowspan=2 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=2>4.8 Gbps/pin</td><td rowspan=1 colspan=2>5.2 Gbps/pin</td><td></td><td rowspan=1 colspan=1>5.6 Gbp</td><td rowspan=1 colspan=1>s/pin</td><td rowspan=1 colspan=2>6.0 Gbps/pin</td><td rowspan=1 colspan=2>6.4 Gbps/pin</td></tr><tr><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td></td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=13>CK Timings</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>CK clock frequency</td><td rowspan=1 colspan=1>fcK</td><td rowspan=1 colspan=1>50</td><td rowspan=1 colspan=1>1200</td><td rowspan=1 colspan=1>50</td><td rowspan=1 colspan=1>1300</td><td rowspan=1 colspan=2>50</td><td rowspan=1 colspan=1>1400</td><td rowspan=1 colspan=1>50</td><td rowspan=1 colspan=1>1500</td><td rowspan=1 colspan=1>50</td><td rowspan=1 colspan=1>1600</td><td rowspan=1 colspan=1>MHz</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>CK clock period</td><td rowspan=1 colspan=1>tcK</td><td rowspan=1 colspan=1>0.833</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>0.769</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=2>0.714</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>0.667</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>0.625</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>Absolute CK clock differentialHIGH-level width</td><td rowspan=1 colspan=1>tCH</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=2>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1>tck</td><td rowspan=1 colspan=1>40</td></tr><tr><td rowspan=1 colspan=1>Absolute CK clock differentialLOW-level width</td><td rowspan=1 colspan=1>tcL</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=2>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1>tck</td><td rowspan=1 colspan=1>40</td></tr><tr><td rowspan=1 colspan=9>Command and Address Input Timings</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Command and address input setuptime based on VIH/VIL</td><td rowspan=1 colspan=1>tis</td><td rowspan=1 colspan=1>92</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>85</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>79</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>73</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>69</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ps</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=1>Command and address input holdtime based on VIH/VIL</td><td rowspan=1 colspan=1>tIH</td><td rowspan=1 colspan=1>92</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>85</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>79</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>73</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>69</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ps</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=1>Command and address single pulsewidth</td><td rowspan=1 colspan=1>tCIPW</td><td rowspan=1 colspan=1>292</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>269口</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>250</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>233</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>219</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ps</td><td rowspan=1 colspan=1>27</td></tr><tr><td rowspan=1 colspan=8>Data Input Timings</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>WDQS clock period</td><td rowspan=1 colspan=1>twDQS</td><td rowspan=1 colspan=1>0.416</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>0.385</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=2>0.357</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>0.333</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>0.312</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>41</td></tr><tr><td rowspan=1 colspan=1>Average WDQS differential inputHIGH pulse width</td><td rowspan=1 colspan=1>twQSH(avg)</td><td rowspan=1 colspan=1>0.47</td><td rowspan=1 colspan=1>0.53</td><td rowspan=1 colspan=1>0.47</td><td rowspan=1 colspan=1>0.53</td><td rowspan=1 colspan=2>0.47</td><td rowspan=1 colspan=1>0.53</td><td rowspan=1 colspan=1>0.47</td><td rowspan=1 colspan=1>0.53</td><td rowspan=1 colspan=1>0.47</td><td rowspan=1 colspan=1>0.53</td><td rowspan=1 colspan=1>twDQS</td><td rowspan=1 colspan=1>42</td></tr><tr><td rowspan=1 colspan=1>Average WDQS differential inputLOW pulse width</td><td rowspan=1 colspan=1>twQSL(avg)</td><td rowspan=1 colspan=1>0.47</td><td rowspan=1 colspan=1>0.53</td><td rowspan=1 colspan=1>0.47</td><td rowspan=1 colspan=1>0.53</td><td rowspan=1 colspan=2>0.47</td><td rowspan=1 colspan=1>0.53</td><td rowspan=1 colspan=1>0.47</td><td rowspan=1 colspan=1>0.53</td><td rowspan=1 colspan=1>0.47</td><td rowspan=1 colspan=1>0.53</td><td rowspan=1 colspan=1>twDQS</td><td rowspan=1 colspan=1>42</td></tr><tr><td rowspan=1 colspan=1>Absolute WDQS differential inputHIGH pulse width</td><td rowspan=1 colspan=1>twQSH(abs)</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=2>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1>twDQS</td><td rowspan=1 colspan=1>43</td></tr><tr><td rowspan=1 colspan=1>Absolute WDQS differential inputLOW pulse width</td><td rowspan=1 colspan=1>twQSL(abs)</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=2>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1>twDQS</td><td rowspan=1 colspan=1>43</td></tr><tr><td rowspan=1 colspan=1>Rx single pulse width</td><td rowspan=1 colspan=1>tDIPW</td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>0.55</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.55</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>UI</td><td rowspan=1 colspan=1>27</td></tr><tr><td rowspan=1 colspan=1>Rx Timing Window with PSIJ</td><td rowspan=1 colspan=1>tDIVW</td><td rowspan=1 colspan=1>0.30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>0.30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>UI</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>WDQS to write data offset</td><td rowspan=1 colspan=1>twDQS2DQ_I</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>650</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>650</td><td rowspan=1 colspan=2>100</td><td rowspan=1 colspan=1>650</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>650</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>650</td><td rowspan=1 colspan=1>ps</td><td rowspan=1 colspan=1>33,34,45</td></tr><tr><td rowspan=1 colspan=1>WDQS to write data offset voltagevariation for write</td><td rowspan=1 colspan=1>twDQS2DQ_IVOLT</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.8</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.8</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>0.8</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.8</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.8</td><td rowspan=1 colspan=1>ps/mV</td><td rowspan=1 colspan=1>34,46</td></tr><tr><td rowspan=1 colspan=1>WDQS to write data offsettemperature variation for write</td><td rowspan=1 colspan=1>tWDQS2DQ_ITEMP</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1>ps/C</td><td rowspan=1 colspan=1>34,46,47</td></tr></table>

Table 107 — Timings Parameters (cont’d)
<table><tr><td rowspan=3 colspan=1>Parameter</td><td rowspan=3 colspan=1>Symbol</td><td rowspan=1 colspan=10>Speed Bin²</td><td rowspan=3 colspan=1>Unit</td><td rowspan=3 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=2>4.8 Gbps/pin</td><td rowspan=1 colspan=2>5.2 Gbps/pin</td><td rowspan=1 colspan=2>5.6 Gbps/pin</td><td rowspan=1 colspan=2>6.0 Gbps/pin</td><td rowspan=1 colspan=2>6.4 Gbps/pin</td></tr><tr><td rowspan=1 colspan=1>min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>min</td><td rowspan=1 colspan=1>Max</td><td rowspan=1 colspan=1>min</td><td rowspan=1 colspan=1>Max</td></tr><tr><td rowspan=1 colspan=14>Data Input Timings (cont&#x27;d)</td></tr><tr><td rowspan=1 colspan=1>DQ to DQ skew (intra-byte) forwrite</td><td rowspan=1 colspan=1>tDQ2DQtra_I</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>ps</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>DQ to DQ skew (inter-byte) forwrite</td><td rowspan=1 colspan=1>tDQ2DQter_I</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>40</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>40</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>40</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>40</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>40</td><td rowspan=1 colspan=1>ps</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=14>Data Output Timings</td></tr><tr><td rowspan=1 colspan=1>RDQS differential output HIGH</td><td rowspan=1 colspan=1>tQSH</td><td rowspan=1 colspan=1>twQSH(abs)- 0.08</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>twQSH(abs)- 0.08</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>twQSH(abs)- 0.08</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>twQSH(abs)- 0.08</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>twQSH(abs)- 0.08</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>twDQS</td><td rowspan=1 colspan=1>6,38</td></tr><tr><td rowspan=1 colspan=1>RDQS differential output LOW</td><td rowspan=1 colspan=1>tQSL</td><td rowspan=1 colspan=1>twQSL(abs)- 0.08</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>twQSL(abs)- 0.08</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>twQSL(abs)-0.08</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>twQSL(abs)- 0.08</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>twQSL(abs)- 0.08</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>twDQS</td><td rowspan=1 colspan=1>6,39</td></tr><tr><td rowspan=1 colspan=1>DQ output hold time from DQS</td><td rowspan=1 colspan=1>tQH</td><td rowspan=1 colspan=1>Min(tQsH, tQsl)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Min(tQsH, tosl)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Min(tosH, tQsl)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Min(tQsH, tQsL)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Min(tQsH, tQsL)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>twDQS</td><td rowspan=1 colspan=1>6</td></tr><tr><td rowspan=1 colspan=1>DQ output window per pin</td><td rowspan=1 colspan=1>tQw</td><td rowspan=1 colspan=1>Min(tQsH, tosl) -0.07</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Min(tQsH, tosl) -0.07</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Min(tosH, tQsl) -0.07</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Min(tQsH, tosl) -0.07</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Min(tQsH, tQsl) -0.07</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>UI</td><td rowspan=1 colspan=1>6</td></tr><tr><td rowspan=1 colspan=1>RDQS to DQ skew in Byte T4</td><td rowspan=1 colspan=1>tDQSQtra</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>ps</td><td rowspan=1 colspan=1>6</td></tr><tr><td rowspan=1 colspan=1>DQ to DQ skew (intra-byte) for read</td><td rowspan=1 colspan=1>tDQ2DQtra_O</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>ps</td><td rowspan=1 colspan=1>6</td></tr><tr><td rowspan=1 colspan=1>DQ to DQ skew (inter-byte) for read</td><td rowspan=1 colspan=1>tDQ2DQter_0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1>ps</td><td rowspan=1 colspan=1>6</td></tr><tr><td rowspan=1 colspan=1>WDQS to read data and RDQSoffset</td><td rowspan=1 colspan=1>tWDQS2DQ_0</td><td rowspan=1 colspan=1>0.2</td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1>0.2</td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1>0.2</td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1>0.2</td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1>0.2</td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>6,33,35</td></tr><tr><td rowspan=1 colspan=1>WDQS to read data offset voltagevariation for read</td><td rowspan=1 colspan=1>tWDQS2DQ_0_VOLT</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1>ps/mV</td><td rowspan=1 colspan=1>35,46</td></tr><tr><td rowspan=1 colspan=1>WDQS to read data offsettemperature variation for read</td><td rowspan=1 colspan=1>tWDQS2DQ_0TEMP</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>1.0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>1.0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>1.0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>1.0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>1.0</td><td rowspan=1 colspan=1>ps/C</td><td rowspan=1 colspan=1>35,46,47</td></tr><tr><td rowspan=1 colspan=1>DQ, DBI high impedance to lowimpedance time from WDQS</td><td rowspan=1 colspan=1>tLZ</td><td rowspan=1 colspan=10>Min: twDQS2DQ_o(min) – tQH(min)Max: twDQS2DQ_o(max) + tDQSQtra(max)</td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>6</td></tr><tr><td rowspan=1 colspan=1>DQ, DBI low impedance to highimpedance time from WDQS</td><td rowspan=1 colspan=1>tHZ</td><td rowspan=1 colspan=10>Min: twDQS2DQ_o(min)Max: twDQS2DQ_o(max) + tDQSQtra(max)</td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>6</td></tr></table>

Table 107 — Timings Parameters (cont’d)
<table><tr><td colspan="1" rowspan="3">Parameter</td><td colspan="1" rowspan="3">Symbol</td><td colspan="8" rowspan="1">Speed Bin²</td><td colspan="1" rowspan="2">Unit</td><td colspan="1" rowspan="2">Notes</td></tr><tr><td colspan="2" rowspan="1">6.8 Gbps/pin</td><td colspan="2" rowspan="1">7.2 Gbps/pin</td><td colspan="2" rowspan="1">7.6 Gbps/pin</td><td colspan="2" rowspan="1">8.0 Gbps/pin</td></tr><tr><td colspan="1" rowspan="1">min</td><td colspan="1" rowspan="1">Max</td><td colspan="1" rowspan="1">min</td><td colspan="1" rowspan="1">Max</td><td colspan="1" rowspan="1">min</td><td colspan="1" rowspan="1">Max</td><td colspan="1" rowspan="1">min</td><td colspan="1" rowspan="1">Max</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="4" rowspan="1"></td><td colspan="2" rowspan="1">CK Timings</td><td colspan="1" rowspan="1"></td><td colspan="2" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">CK clock frequency</td><td colspan="1" rowspan="1">fcK</td><td colspan="1" rowspan="1">50</td><td colspan="1" rowspan="1">1700</td><td colspan="1" rowspan="1">50</td><td colspan="1" rowspan="1">1800</td><td colspan="1" rowspan="1">50</td><td colspan="1" rowspan="1">1900</td><td colspan="1" rowspan="1">50</td><td colspan="1" rowspan="1">2000</td><td colspan="1" rowspan="1">MHz</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">CK clock period</td><td colspan="1" rowspan="1">tck</td><td colspan="1" rowspan="1">0.588</td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">0.556</td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">0.526</td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">0.500</td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">ns</td><td colspan="1" rowspan="1">4</td></tr><tr><td colspan="1" rowspan="1">Absolute CK clock differentialHIGH-level width</td><td colspan="1" rowspan="1">tCH</td><td colspan="1" rowspan="1">0.45</td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1">0.45</td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1">0.45</td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1">0.45</td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1">tcK</td><td colspan="1" rowspan="1">40</td></tr><tr><td colspan="1" rowspan="1">Absolute CK clock differentialLOW-level width</td><td colspan="1" rowspan="1">tcL</td><td colspan="1" rowspan="1">0.45</td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1">0.45</td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1">0.45</td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1">0.45</td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1">tck</td><td colspan="1" rowspan="1">40</td></tr><tr><td colspan="10" rowspan="1">Command and Address Input Timings</td><td colspan="2" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">Command and address input setuptime based on VIH/VIL</td><td colspan="1" rowspan="1">tis</td><td colspan="1" rowspan="1">65</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">61</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">58</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">55</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">ps</td><td colspan="1" rowspan="1">5</td></tr><tr><td colspan="1" rowspan="1">Command and address input holdtime based on VIH/VIL</td><td colspan="1" rowspan="1">tIH</td><td colspan="1" rowspan="1">65</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">61</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">58</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">55</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">ps</td><td colspan="1" rowspan="1">5</td></tr><tr><td colspan="1" rowspan="1">Command and address single pulsewidth</td><td colspan="1" rowspan="1">tcIPw</td><td colspan="1" rowspan="1">206</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">195</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">184</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">175</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">ps</td><td colspan="1" rowspan="1">27</td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="4" rowspan="1">Data Input T</td><td colspan="7" rowspan="1">imings</td></tr><tr><td colspan="1" rowspan="1">WDQS clock period</td><td colspan="1" rowspan="1">twDQS</td><td colspan="1" rowspan="1">0.295</td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1">0.278</td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1">0.263</td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1">0.250</td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1">ns</td><td colspan="1" rowspan="1">41</td></tr><tr><td colspan="1" rowspan="1">Average WDQS differential inputHIGH pulse width</td><td colspan="1" rowspan="1">twQSH(avg)</td><td colspan="1" rowspan="1">0.47</td><td colspan="1" rowspan="1">0.53</td><td colspan="1" rowspan="1">0.47</td><td colspan="1" rowspan="1">0.53</td><td colspan="1" rowspan="1">0.47</td><td colspan="1" rowspan="1">0.53</td><td colspan="1" rowspan="1">0.47</td><td colspan="1" rowspan="1">0.53</td><td colspan="1" rowspan="1">twDQS</td><td colspan="1" rowspan="1">42</td></tr><tr><td colspan="1" rowspan="1">Average WDQS differential inputLOW pulse width</td><td colspan="1" rowspan="1">twQSL(avg)</td><td colspan="1" rowspan="1">0.47</td><td colspan="1" rowspan="1">0.53</td><td colspan="1" rowspan="1">0.47</td><td colspan="1" rowspan="1">0.53</td><td colspan="1" rowspan="1">0.47</td><td colspan="1" rowspan="1">0.53</td><td colspan="1" rowspan="1">0.47</td><td colspan="1" rowspan="1">0.53</td><td colspan="1" rowspan="1">twDQS</td><td colspan="1" rowspan="1">42</td></tr><tr><td colspan="1" rowspan="1">Absolute WDQS differential inputHIGH pulse width</td><td colspan="1" rowspan="1">twQSH(abs)</td><td colspan="1" rowspan="1">0.45</td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1">0.45</td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1">0.45</td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1">0.45</td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1">twDQS</td><td colspan="1" rowspan="1">43</td></tr><tr><td colspan="1" rowspan="1">Absolute WDQS differential inputLOW pulse width</td><td colspan="1" rowspan="1">twQSL(abs)</td><td colspan="1" rowspan="1">0.45</td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1">0.45</td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1">0.45</td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1">0.45</td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1">twDQS</td><td colspan="1" rowspan="1">43</td></tr><tr><td colspan="1" rowspan="1">Rx single pulse width</td><td colspan="1" rowspan="1">tDIPW</td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">0.55</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">UI</td><td colspan="1" rowspan="1">27</td></tr><tr><td colspan="1" rowspan="1">Rx Timing Window with PSIJ</td><td colspan="1" rowspan="1">tDIVW</td><td colspan="1" rowspan="1">0.30</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">0.30</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">0.30</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">0.30</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">UI</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">WDQS to write data offset</td><td colspan="1" rowspan="1">tWDQS2DQ_I</td><td colspan="1" rowspan="1">100</td><td colspan="1" rowspan="1">650</td><td colspan="1" rowspan="1">100</td><td colspan="1" rowspan="1">650</td><td colspan="1" rowspan="1">100</td><td colspan="1" rowspan="1">650</td><td colspan="1" rowspan="1">100</td><td colspan="1" rowspan="1">650</td><td colspan="1" rowspan="1">ps</td><td colspan="1" rowspan="1">33,34,45</td></tr><tr><td colspan="1" rowspan="1">WDQS to write data offset voltagevariation for write</td><td colspan="1" rowspan="1">twDQS2DQ_IVOLT</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">0.8</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">0.8</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">0.8</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">0.8</td><td colspan="1" rowspan="1">ps/mV</td><td colspan="1" rowspan="1">34,46</td></tr><tr><td colspan="1" rowspan="1">WDQS to write data offsettemperature variation for write</td><td colspan="1" rowspan="1">tWDQS2DQ_ITEMP</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">0.4</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">0.4</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">0.4</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">0.4</td><td colspan="1" rowspan="1">ps/C</td><td colspan="1" rowspan="1">34,46,47</td></tr><tr><td colspan="12" rowspan="1">Data Input Timings (cont'd)</td></tr><tr><td colspan="1" rowspan="1">DQ to DQ skew (intra-byte) forwrite</td><td colspan="1" rowspan="1">tDQ2DQtra_I</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1">ps</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">DQ to DQ skew (inter-byte) forwrite</td><td colspan="1" rowspan="1">tDQ2DQter_I</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">40</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">40</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">40</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">40</td><td colspan="1" rowspan="1">ps</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="12" rowspan="1">Data Output Timings</td></tr><tr><td colspan="1" rowspan="1">RDQS differential output HIGH</td><td colspan="1" rowspan="1">tQSH</td><td colspan="1" rowspan="1">twQSH(abs) -0.08</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">twQSH(abs) -0.08</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">twQSH(abs) -0.08</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">twQSH(abs) -0.08</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">twDQS</td><td colspan="1" rowspan="1">6,38</td></tr><tr><td colspan="1" rowspan="1">RDQS differential output LOW</td><td colspan="1" rowspan="1">tQSL</td><td colspan="1" rowspan="1">twQSL(abs) -0.08</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">twQSL(abs) -0.08</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">twQSL(abs) -0.08</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">twQSL(abs) -0.08</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">twDQS</td><td colspan="1" rowspan="1">6,39</td></tr><tr><td colspan="1" rowspan="1">DQ output hold time from DQS</td><td colspan="1" rowspan="1">tQH</td><td colspan="1" rowspan="1">min(tQsH,tQSL)</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">min(tQSH,tQSL)</td><td colspan="1" rowspan="1">60</td><td colspan="1" rowspan="1">min(tQsH,tQSL)</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">min(tQsH,tQSL)</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">twDQS</td><td colspan="1" rowspan="1">6</td></tr><tr><td colspan="1" rowspan="1">DQ output window per pin</td><td colspan="1" rowspan="1">tQw</td><td colspan="1" rowspan="1">min(tQsH,tQSL) - 0.07</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">min(tQsH,tQsL) - 0.07</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">min(tQSH,tQSL) - 0.07</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">min(tosH,tQSL) - 0.07</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">UI</td><td colspan="1" rowspan="1">6</td></tr><tr><td colspan="1" rowspan="1">RDQS to DQ skew in Byte T4</td><td colspan="1" rowspan="1">tDQSQtra</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">ps</td><td colspan="1" rowspan="1">6</td></tr><tr><td colspan="1" rowspan="1">DQ to DQ skew (intra-byte) for read</td><td colspan="1" rowspan="1">tDQ2DQtra_O</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1">ps</td><td colspan="1" rowspan="1">6</td></tr><tr><td colspan="1" rowspan="1">DQ to DQ skew (inter-byte) for read</td><td colspan="1" rowspan="1">tDQ2DQter_0</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">30</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">30</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">30</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">30</td><td colspan="1" rowspan="1">ps</td><td colspan="1" rowspan="1">6</td></tr><tr><td colspan="1" rowspan="1">WDQS to read data and RDQSoffset</td><td colspan="1" rowspan="1">twDQS2DQ_0</td><td colspan="1" rowspan="1">0.2</td><td colspan="1" rowspan="1">2.5</td><td colspan="1" rowspan="1">0.2</td><td colspan="1" rowspan="1">2.5</td><td colspan="1" rowspan="1">0.2</td><td colspan="1" rowspan="1">2.5</td><td colspan="1" rowspan="1">0.2</td><td colspan="1" rowspan="1">2.5</td><td colspan="1" rowspan="1">ns</td><td colspan="1" rowspan="1">6,33,35</td></tr><tr><td colspan="1" rowspan="1">WDQS to read data offset voltagevariation for read</td><td colspan="1" rowspan="1">tWDQS2DQ_0VOLT</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">2.5</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">2.5</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">2.5</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">2.5</td><td colspan="1" rowspan="1">ps/mV</td><td colspan="1" rowspan="1">35,46</td></tr><tr><td colspan="1" rowspan="1">WDQS to read data offsettemperature variation for read</td><td colspan="1" rowspan="1">tWDQS2DQ_0TEMP</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">1.0</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">1.0</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">1.0</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">1.0</td><td colspan="1" rowspan="1">ps/C</td><td colspan="1" rowspan="1">35,46,47</td></tr><tr><td colspan="1" rowspan="1">DQ, DBI high impedance to lowimpedance time from WDQS</td><td colspan="1" rowspan="1">tLZ</td><td colspan="8" rowspan="1">min: twDQS2DQ_o(min) − tQH(min)Max: twDQS2DQ_o(max) + tDQsQtra(max)</td><td colspan="1" rowspan="1">ns</td><td colspan="1" rowspan="1">6</td></tr><tr><td colspan="1" rowspan="1">DQ, DBI low impedance to highimpedance time from WDQS</td><td colspan="1" rowspan="1">tHZ</td><td colspan="8" rowspan="1">min: twDQS2DQ_o(min)Max: twDQS2DQ_o(max) + tDQSQtra(max)</td><td colspan="1" rowspan="1">ns</td><td colspan="1" rowspan="1">6</td></tr></table>

Table 108 — Timings Parameters (Part 2)
<table><tr><td rowspan=2 colspan=1>Parameter1,3</td><td rowspan=2 colspan=1>Symbol</td><td rowspan=1 colspan=2>Values</td><td rowspan=2 colspan=1>Unit</td><td rowspan=2 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>min</td><td rowspan=1 colspan=1>MAX</td></tr><tr><td rowspan=1 colspan=6>Row Access Timings</td></tr><tr><td rowspan=1 colspan=1>ACTIVATE to ACTIVATE command period</td><td rowspan=1 colspan=1>tRC</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>ACTIVATE to PREab, PREab, WRA, RDA commandperiod</td><td rowspan=1 colspan=1>tRAS</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>9 × tREFI</td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>7</td></tr><tr><td rowspan=1 colspan=1>ACTIVATE to READ command delay</td><td rowspan=1 colspan=1>tRCDRD</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>ACTIVATE to WRITE command delay</td><td rowspan=1 colspan=1>tRCDWR</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>ACTIVATE to ACTIVATE or PER BANK REFRESH bankB command delay same bank group</td><td rowspan=1 colspan=1>tRRDL</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>8</td></tr><tr><td rowspan=1 colspan=1>ACTIVATE to ACTIVATE or PER BANK REFRESH bankB command delay different bank group</td><td rowspan=1 colspan=1>tRRDS</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>9</td></tr><tr><td rowspan=1 colspan=1>Four bank activate window</td><td rowspan=1 colspan=1>tFAW</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>10</td></tr><tr><td rowspan=1 colspan=1>READ to PRECHARGE command delay same bank</td><td rowspan=1 colspan=1>tRTP</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>11,32</td></tr><tr><td rowspan=1 colspan=1>PRECHARGE command period</td><td rowspan=1 colspan=1>tRP</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>WRITE recovery time</td><td rowspan=1 colspan=1>twR</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>32</td></tr><tr><td rowspan=1 colspan=1>Auto precharge write recovery + precharge time</td><td rowspan=1 colspan=1>tDAL</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>12</td></tr><tr><td rowspan=1 colspan=1>PRECHARGE to PRECHARGE delay same pseudo channel</td><td rowspan=1 colspan=1>tpPD</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Rolling Accumulated ACTIVATE count</td><td rowspan=1 colspan=1>RAA</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=6>Column Access Timings</td></tr><tr><td rowspan=1 colspan=1>RD/WR bank A to RD/WR bank B command delay samebank group</td><td rowspan=1 colspan=1>tcCDL</td><td rowspan=1 colspan=1>Max(4, 2.5 ns/tck)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>13,14</td></tr><tr><td rowspan=1 colspan=1>RD/WR bank A to RD/WR bank B command delay differentbank group</td><td rowspan=1 colspan=1>tcCDS</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>15,16</td></tr><tr><td rowspan=1 colspan=1>RD SID A to RD SID B command delay</td><td rowspan=1 colspan=1>tcCDR</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>17</td></tr><tr><td rowspan=1 colspan=1>Internal WRITE to READ command delay same bank group</td><td rowspan=1 colspan=1>tWTRL</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>13</td></tr><tr><td rowspan=1 colspan=1>Internal WRITE to READ command delay different bankgroup</td><td rowspan=1 colspan=1>tWTRS</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>15</td></tr><tr><td rowspan=1 colspan=1>READ to WRITE command delay</td><td rowspan=1 colspan=1>tRTW</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>18</td></tr><tr><td rowspan=1 colspan=6>Power-Down Timings</td></tr><tr><td rowspan=1 colspan=1>POWER-DOWN ENTRY to EXIT time</td><td rowspan=1 colspan=1>tPD</td><td rowspan=1 colspan=1>tcPDED + 6 × tcK</td><td rowspan=1 colspan=1>9× tREFI</td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>POWER-DOWN EXIT time</td><td rowspan=1 colspan=1>txP</td><td rowspan=1 colspan=1>MAX(10× tcK,7.5)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Valid CK clocks required after POWER-DOWN ENTRY</td><td rowspan=1 colspan=1>tCKPDE</td><td rowspan=1 colspan=1>RU(tCPDED / tCcK)+1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Valid CK clocks required before POWER-DOWN EXIT</td><td rowspan=1 colspan=1>tCKPDX</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Command path disable delay</td><td rowspan=1 colspan=1>tCPDED</td><td rowspan=1 colspan=1>MAX(10 × tcK,7.5)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>ACTIVATE to POWER-DOWN ENTRY command delay</td><td rowspan=1 colspan=1>tACTPDE</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>19</td></tr><tr><td rowspan=1 colspan=1>PRECHARGE(rising CK edge) to POWER-DOWN ENTRYcommand delay</td><td rowspan=1 colspan=1>tPRPDER</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>PRECHARGE(falling CK edge) to POWER-DOWNENTRY command delay</td><td rowspan=1 colspan=1>tPRPDEF</td><td rowspan=1 colspan=1>1.5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>REFRESH to POWER-DOWN ENTRY command delay</td><td rowspan=1 colspan=1>tREFPDE</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>19</td></tr><tr><td rowspan=1 colspan=1>PER BANK REFRESH to POWER-DOWN ENTRYcommand delay</td><td rowspan=1 colspan=1>tREFPBPDE</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>19</td></tr></table>

Table 108 — Timings Parameters (Part 2) (cont’d)
<table><tr><td rowspan=2 colspan=4>Parameter1,3</td><td rowspan=2 colspan=1>Symbol</td><td rowspan=1 colspan=2>Values</td><td rowspan=2 colspan=1>Unit</td><td rowspan=2 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=2>min          MAX</td></tr><tr><td rowspan=1 colspan=9>Power-Down Timings (cont&#x27;d)</td></tr><tr><td rowspan=1 colspan=4>MODE REGISTER SET to POWER-DOWN ENTRYcommand delay</td><td rowspan=1 colspan=1>tMRSPDE</td><td rowspan=1 colspan=1>tMOD(min)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=4>READ or READ w/ AP to POWER-DOWN ENTRYcommand delay</td><td rowspan=1 colspan=1>tRDPDE</td><td rowspan=1 colspan=1> $\overline { { \mathrm { R L + P L } + 2 + } }$  $\mathrm { R U } ( \mathrm { t _ { D Q S S } } ( \mathrm { m a x } ) +$  $\mathrm { t _ { W D Q S 2 D Q \_ O } ( m a x ) / }$ tck)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=4>WRITE to POWER-DOWN ENTRY command delay</td><td rowspan=1 colspan=1>tWRPDE</td><td rowspan=1 colspan=1> $\overline { { \mathrm { \mathbf { W L } } + \mathrm { \mathbf { P L } } + 3 } }$  $+ \ : \mathrm { R U } ( \mathrm { t _ { W R } / t _ { C K } } )$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>20</td></tr><tr><td rowspan=1 colspan=4>WRITE w/ AP to POWER-DOWN ENTRY command delay</td><td rowspan=1 colspan=1>tWRAPDE</td><td rowspan=1 colspan=1>WL + PL + 3+ WR</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1>21</td></tr><tr><td rowspan=1 colspan=9>Self Refresh Timings</td></tr><tr><td rowspan=1 colspan=4>SELF REFRESH ENTRY to EXIT time</td><td rowspan=1 colspan=1>tCKSR</td><td rowspan=1 colspan=1> $\mathrm { t } _ { \mathrm { C P D E D } } + 6 \times \mathrm { t } _ { \mathrm { C K } }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=4>Valid CK clocks required after SELF REFRESH ENTRY</td><td rowspan=1 colspan=1>tCKSRE</td><td rowspan=1 colspan=1> $\overline { { \mathrm { R U } ( \mathrm { t } _ { \mathrm { C P D E D } } / \mathrm { t } _ { \mathrm { C K } } ) } }$ +1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=4>Valid CK clocks required before SELF REFRESH orPOWER-DOWN EXIT</td><td rowspan=1 colspan=1>tCKSRX</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=4>READ or READ w/ AP to SELF REFRESH ENTRYcommand delay</td><td rowspan=1 colspan=1>tRDSRE</td><td rowspan=1 colspan=1> RL + PL + 3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>nCK</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=4>Exit self refresh command delay</td><td rowspan=1 colspan=1>txs</td><td rowspan=1 colspan=1> $\mathrm { M A X } ( 1 0 \times \mathrm { t } _ { \mathrm { C K } } ,$  $\mathbf { t } _ { \mathrm { R F C } } ( \operatorname* { m i n } ) + 1 0 )$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=4>Exit self refresh to MODE REGISTER SET command delay</td><td rowspan=1 colspan=1>txsMRS</td><td rowspan=1 colspan=1> $\overline { { \mathbf { M A X } ( 1 0 \times \mathbf { t } _ { \mathrm { C K } } } } ,$ 15)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=4>Exit self refresh to MODE REGISTER SET command delayafter frequency change</td><td rowspan=1 colspan=1>txsMRSF</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=4>WRITE to SELF REFRESH ENTRY command delay</td><td rowspan=1 colspan=1>tWRSRE</td><td rowspan=1 colspan=1> $\overline { { \mathrm { W L } + \mathrm { P L } + 3 } }$  $+ \ : \mathrm { R U } ( \mathrm { t w r } \ : / \ : \mathrm { t c } \times )$  $+ \mathrm { R U } ( \mathrm { t _ { R P } / t _ { C K } } )$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>20</td></tr><tr><td rowspan=1 colspan=4>WRITE w/ AP to SELF REFRESH ENTRY command delay</td><td rowspan=1 colspan=1>tWRASRE</td><td rowspan=1 colspan=1>WL + PL + 3 + $\mathrm { W R + R U ( t _ { R P } / t _ { C K } ) }$ </td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>21</td></tr><tr><td rowspan=1 colspan=9>Refresh Timings</td></tr><tr><td rowspan=1 colspan=4>Minimum time in self refresh for per-bank RAA count to bereset to 0</td><td rowspan=1 colspan=1>tRAASRF</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>29</td></tr><tr><td rowspan=8 colspan=1>REFRESHcommand period</td><td rowspan=4 colspan=1>24 Gb/die</td><td rowspan=1 colspan=1>4-High</td><td rowspan=1 colspan=1>3 Gb / channel</td><td rowspan=8 colspan=1>tRFCab</td><td rowspan=1 colspan=1>360</td><td rowspan=1 colspan=1></td><td rowspan=8 colspan=1>ns</td><td rowspan=8 colspan=1>22</td></tr><tr><td rowspan=1 colspan=1>8-High</td><td rowspan=1 colspan=1>6 Gb / channel</td><td rowspan=1 colspan=1>410</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>12-High</td><td rowspan=1 colspan=1>9 Gb / channel</td><td rowspan=1 colspan=1>450</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>16-High</td><td rowspan=1 colspan=1>12 Gb / channel</td><td rowspan=1 colspan=1>490</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=4 colspan=1>32 Gb/die</td><td rowspan=1 colspan=1>4-High</td><td rowspan=1 colspan=1>4 Gb / channel</td><td rowspan=1 colspan=1>400</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>8-High</td><td rowspan=1 colspan=1>8 Gb / channel</td><td rowspan=1 colspan=1>450</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>12-High</td><td rowspan=1 colspan=1>12 Gb / channel</td><td rowspan=1 colspan=1>490</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>16-High</td><td rowspan=1 colspan=1>16 Gb / channel</td><td rowspan=1 colspan=1>530</td><td rowspan=1 colspan=1></td></tr></table>

Table 108 — Timings Parameters (Part 2) (cont’d)
<table><tr><td colspan="2" rowspan="2">Parameter1,3</td><td colspan="2" rowspan="2">Symbol</td><td colspan="2" rowspan="1">Values</td><td colspan="1" rowspan="2">Unit</td><td colspan="1" rowspan="2">Notes</td></tr><tr><td colspan="2" rowspan="1">min          MAX</td></tr><tr><td colspan="8" rowspan="1">Refresh Timings (cont'd)</td></tr><tr><td colspan="1" rowspan="2">PER BANK REFRESH command period(same bank)</td><td colspan="1" rowspan="1">24 Gb / die</td><td colspan="2" rowspan="1">tRFCpb</td><td colspan="1" rowspan="1">240</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="2">ns</td><td colspan="1" rowspan="2">28</td></tr><tr><td colspan="1" rowspan="1">32 Gb / die</td><td colspan="2" rowspan="1"></td><td colspan="1" rowspan="1">280</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">PER BANK REFRESH command period (different bank)and PER BANK REFRESH to ACTIVATÈ (different bank)command delay</td><td colspan="2" rowspan="1">tRREFD</td><td colspan="1" rowspan="1">MAX(3 × tck, 8)</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">ns</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">Average periodic refresh interval for REFRESH command</td><td colspan="2" rowspan="1">tREFI</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">3.9</td><td colspan="1" rowspan="1">μs</td><td colspan="1" rowspan="1">23</td></tr><tr><td colspan="2" rowspan="1">Half rate of periodic refresh commands interval forREFRESH command by temperature trip points</td><td colspan="2" rowspan="1">0.5×tREFI</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">0.5 × 3.9</td><td colspan="1" rowspan="1">μs</td><td colspan="1" rowspan="1">23</td></tr><tr><td colspan="2" rowspan="1">Quarter rate of periodic refresh commands interval forREFRESH command by temperature trip points</td><td colspan="2" rowspan="1">0.25 ×tREFI</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">0.25 × 3.9</td><td colspan="1" rowspan="1">μs</td><td colspan="1" rowspan="1">23</td></tr><tr><td colspan="1" rowspan="5">Average periodic refresh interval forPER BANK REFRESH command</td><td colspan="1" rowspan="1">8-High</td><td colspan="2" rowspan="1">tREFIpb</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">tREFI / 32</td><td colspan="1" rowspan="1">μs</td><td colspan="1" rowspan="5">22,24</td></tr><tr><td colspan="1" rowspan="3">12-High</td><td colspan="1" rowspan="3"></td><td></td><td></td><td></td><td></td></tr><tr><td colspan="2" rowspan="3"></td><td></td><td></td><td></td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">tREFI / 48</td><td colspan="1" rowspan="1">μs</td></tr><tr><td colspan="1" rowspan="1">16-High</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">tREFI / 64</td><td colspan="1" rowspan="1">μs</td></tr><tr><td colspan="1" rowspan="1">Secondary ACTIVATE command withDRFM flag to PREab, PREab, WRA,RDA command delay</td><td colspan="1" rowspan="1"></td><td colspan="2" rowspan="1">tDRFM2PRE</td><td colspan="1" rowspan="1">TBD</td><td colspan="1" rowspan="1">tRAS(Max.) -tRRDL</td><td colspan="1" rowspan="1">ns</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">Time interval during which anyRow/Bank address combination may besampled for DRFM</td><td colspan="1" rowspan="1"></td><td colspan="2" rowspan="1">tDRFMi</td><td colspan="1" rowspan="1">a</td><td colspan="1" rowspan="1">2× tREFI</td><td colspan="1" rowspan="1">μs</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="8" rowspan="1">WDQS-to-CK Timings</td></tr><tr><td colspan="2" rowspan="1">WDQS/2 (0° phase) rising edge to CK rising edge delay</td><td colspan="2" rowspan="1">tDQSS</td><td colspan="1" rowspan="1">Max(-200ps,-0.2tCK)</td><td colspan="1" rowspan="1">min(200ps,0.2tCK)</td><td colspan="1" rowspan="1">ps/tCK</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">WDQS-to-CK phase search range during WDQS-to-CKalignment training</td><td colspan="2" rowspan="1">twDQS2CK</td><td colspan="1" rowspan="1">-0.4</td><td colspan="1" rowspan="1">0.4</td><td colspan="1" rowspan="1">tCK</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">CK clock to phase detector output delay in WDQS-to-CKalignment training mode</td><td colspan="2" rowspan="1">twDQS2PD</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">ns</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="8" rowspan="1">Miscellaneous Timings</td></tr><tr><td colspan="2" rowspan="1">MODE REGISTER SET command update delay</td><td colspan="2" rowspan="1">tMOD</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">nCK</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">MODE REGISTER SET command cycle time</td><td colspan="2" rowspan="1">tMRD</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">nCK</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">MODE REGISTER SET command from a preceding READcommand</td><td colspan="2" rowspan="1">tRDMRS</td><td colspan="1" rowspan="1">RL + PL + 2 +RU(tDQss(MAX)+ twDQS2DQ_0(MAX)/tck)</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">nCK</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">Internal WRITE to MODE REGISTER SET command delay</td><td colspan="2" rowspan="1">tWRMRS</td><td colspan="1" rowspan="1">MAX(RU(twR +tRP)/tcK), (PL +RU(tPARDQ/tCK),6)</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">nCK</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">Interval VREFD offset single step settling time</td><td colspan="2" rowspan="1">tVREFD</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">ns</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">Interval VREFD offset full range settling time</td><td colspan="2" rowspan="1">tFVREFD</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">ns</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">ADD/CMD parity error output delay</td><td colspan="2" rowspan="1">tPARAC</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">ns</td><td colspan="1" rowspan="1">25</td></tr><tr><td colspan="2" rowspan="1">Write data parity error output delay</td><td colspan="2" rowspan="1">tPARDQ</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">ns</td><td colspan="1" rowspan="1">26</td></tr><tr><td colspan="2" rowspan="1">Write preamble for WDQS</td><td colspan="2" rowspan="1">tWPRE1</td><td colspan="2" rowspan="1">4</td><td colspan="1" rowspan="1">tWDQS</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">Read preamble for WDQS</td><td colspan="2" rowspan="1">tWPRE2</td><td colspan="2" rowspan="1">16</td><td colspan="1" rowspan="1">tWDQS</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">Write postamble for WDQS</td><td colspan="2" rowspan="1">twPST1</td><td colspan="2" rowspan="1">2</td><td colspan="1" rowspan="1">tWDQS</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">Read postamble for WDQS</td><td colspan="2" rowspan="1">tWPST2</td><td colspan="2" rowspan="1">4</td><td colspan="1" rowspan="1">tWDQS</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">Read preamble for RDQS</td><td colspan="2" rowspan="1">tRPRE</td><td colspan="2" rowspan="1">2</td><td colspan="1" rowspan="1">tWDQS</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="2">Read postamble for RDQS</td><td colspan="1" rowspan="1">MR7 OP6 = 0</td><td colspan="1" rowspan="2">tRPST</td><td colspan="3" rowspan="1">2</td><td colspan="1" rowspan="2">tWDQS</td><td colspan="3" rowspan="2">48</td></tr><tr><td colspan="1" rowspan="1">MR7 OP6 = 1</td><td colspan="5" rowspan="1">4</td></tr><tr><td colspan="2" rowspan="1">CK clock frequency with DCA enabled</td><td colspan="1" rowspan="1">fCKDCA</td><td colspan="2" rowspan="1">1200</td><td colspan="1" rowspan="1">-</td><td colspan="1" rowspan="1">MHz</td><td colspan="3" rowspan="1">36</td></tr><tr><td colspan="2" rowspan="1">Duty Cycle Monitor Measurement time</td><td colspan="1" rowspan="1">tDCMM</td><td colspan="2" rowspan="1">1</td><td colspan="1" rowspan="1">-</td><td colspan="1" rowspan="1">μs</td><td colspan="3" rowspan="1">37</td></tr></table>

Table 108 — Timings Parameters (Part 2) (cont’d)
<table><tr><td></td><td>NOTE 1 AC timing parameters apply to each channel of the HBM4 device independently. No timing parameters are specified across channels, and all channels operate independently of each other.</td></tr><tr><td></td><td>NOTE 2 Speed bins are shown as examples. Vendors may define different speed bins; in this case it is recommended to</td></tr><tr><td></td><td>scale the values for the related timing parameters. NOTE 3 All parameters assume proper device initialization.</td></tr><tr><td></td><td>NOTE 4 Parameter tck is calculated as the average clock period across any consecutive 1,000 cycle window, where each</td></tr><tr><td></td><td>clock period is calculated both from rising CK edge to rising CK edge, and falling CK edge to falling CK edge.</td></tr><tr><td></td><td>NOTE 5 Parameter is based on VIHCA and VILCA.</td></tr><tr><td></td><td>NOTE 6 Parameter is measured with Output Timing reference load and Read DBI enabled.</td></tr><tr><td></td><td>NOTE 7 For Reads and Writes with auto precharge enabled, the device will hold off the internal precharge until tRAs(min) has been satisfied or the number of clock cycles as programmed for RAS in MR4 have elapsed.</td></tr><tr><td></td><td>NOTE 8 Parameter applies when consecutive commands access the same bank group.</td></tr><tr><td></td><td>NOTE 9 Parameter applies when consecutive commands access different bank groups.</td></tr><tr><td></td><td>NOTE 10 No more than 4 ACTIVATE or PER BANK REFRESH commands are allowed within tFAw period.</td></tr><tr><td></td><td></td></tr><tr><td></td><td>NOTE 11 Parameter applies when READ and PRECHARGE commands access the same bank.</td></tr><tr><td></td><td>NOTE 12 tDAL = (twR/tck) + (tRp/tck). For each of the terms, if not already an integer, round up to the next integer.</td></tr><tr><td></td><td>NOTE 13 Parameter applies consecutive commands access the same bank group. NOTE 14 tccDL parameter is applied when seamless consecutive Write or Read commands access to the banks in the same bank</td></tr><tr><td></td><td>group. 1</td></tr><tr><td></td><td>NOTE 15 Parameter applies when consecutive commands access different bank groups. NOTE 16 tccds is either for seamless consecutive READ or seamless consecutive WRITE commands.</td></tr><tr><td></td><td>NOTE 17 tccDR is a parameter for 8, 12, 16-High HBM devices that is used for seamless consecutive READ commands between different stack IDs (SID) instead of tccDs. The tccDR(min) value is vendor specific and a range of tccDs + 1 to 2nCK is</td></tr><tr><td></td><td>supported. The tccDR(min) is dependent on the operation frequency. The vendor datasheet should be consulted for details. For seamless WRITE commands the normal tccDs parameter applies. tccDR does not apply to DWORD MISR operations when DWORD Loopback is enabled in MR7.</td></tr><tr><td></td><td>tRTw is not a DRAM device limit but determined by the system bus turnaround time. Avoid bus contention by setting tRTw (min) = (RL + BL/4 - WL + 0.5) × tcK + twDQs2DQ_o(max) - twDQs2DQ_(min) , and round up to the next integer.</td></tr><tr><td>NOTE 19</td><td>Upon entering power-down the CK clock may be stopped after the number of clock cycles programmed</td></tr><tr><td></td><td>in the RAS register in MR4, referenced to the ACTIVATE that opened the bank, the REFRESH or the PER BANK REFRESH command</td></tr><tr><td>NOTE 20</td><td>twR is defined in ns. For calculation of twRPDE round up twR/tck to the next integer. For calculation of tWRPDE or</td></tr><tr><td></td><td>tWRSRE round up tWR/tCK to the next integer. NOTE 21 WR in clock cycles as programmed in MR3.</td></tr><tr><td>NOTE 22 Density is given per channel.</td><td></td></tr><tr><td></td><td>NOTE 23 A maximum of 8 consecutive REFRESH commands can be posted to an HBM4 device, meaning that the</td></tr><tr><td></td><td>maximum absolute interval between any REFRESH command and the next REFRESH command is 9 × tREFI. All temperatures are able to be measured by CHANNEL_TEMPERATURE instructions issued after proper</td></tr><tr><td></td><td>initialization sequences. Host must ensure tREFI period by predefined Min. and Max. ranges specified in vendors</td></tr><tr><td>NOTE 24</td><td>datasheets. Each corresponding refresh trip points and temperature measurement frequencies are vendor specific. tREFIPB = tREFI / N; N = no. of banks.</td></tr><tr><td>NOTE 25</td><td>tpARAc may be specified as an analog delay or as a combination of n clock cycles and an analog delay. The nominal</td></tr><tr><td></td><td>AERR HIGH time in case of a parity error is 1 nCK.</td></tr><tr><td></td><td></td></tr><tr><td>NOTE 26</td><td>tpArDQ may be specified as an analog delay or as a combination of n clock cycles and an analog delay. The nominal</td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td>DERR HIGH time in case of a parity error is 1 nCK.</td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td>NOTE 27 tcIPw is based on VREFCA level, and tDIPw is based on VREFDQ level.</td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr></table>

Table 108 — Timings Parameters (Part 2) (cont’d)
<table><tr><td colspan="2">Parameter1,3</td><td rowspan="2">Symbol</td><td rowspan="2">MIN</td><td colspan="2">Values MAX</td><td rowspan="2">Unit</td><td rowspan="2">Notes</td></tr><tr><td colspan="2">Density is given per die.</td></tr><tr><td>NOTE 28 NOTE 29</td><td colspan="4">Parameter applies only to HBM4 DRAMs that require the use of Refresh Management (RFM).</td><td colspan="2"></td></tr><tr><td></td><td colspan="4" rowspan="3">PRECHARGE and PRECHARGE ALL commands can be issued on a rising or a falling CK edge. For corresponds to the internal WR or RTP, add 0.5 tck to the number of clock cycles defined for RTP with</td><td rowspan="3"></td></tr><tr><td>NOTE 32</td></tr><tr><td></td></tr><tr><td>NOTE 33</td><td colspan="2">PVT variation is included.</td></tr><tr><td>NOTE 34</td><td colspan="4">The minimum-to-maximum range does not exceed 400ps. The vendor's datasheet shall be consulted for the minimum and maximum values.</td><td colspan="3"></td></tr><tr><td>NOTE 35</td><td colspan="4">The minimum-to-maximum range does not exceed 1.5ns. The vendor's datasheet shall be consulted for the</td><td colspan="2"></td></tr><tr><td>NOTE 36</td><td colspan="4">minimum and maximum values. Parameter fckDcA applies when a duty correction code other than the default 0000 is programmed in the mode</td><td colspan="2"></td></tr><tr><td>NOTE 37</td><td colspan="4">register. tpcmm is measured from the MRS command that enables the duty cycle measurement until the measurement result</td><td colspan="2"></td></tr><tr><td>NOTE 38</td><td colspan="8">in valid. tQsH describes the instantaneous differential output high pulse width on RDQS t – RDQS c as it measures the</td></tr><tr><td>NOTE 39</td><td colspan="7" rowspan="10">next falling edge from an arbitrary rising edge. tQsí edge measurement is based on zero voltage. tosı describes the instantaneous differential output low pulse width on RDQS t – RDQS c as it measures the next rising edge from an arbitrary falling edge. tQsL edge measurement is based on zero voltage.</td></tr><tr><td></td></tr><tr><td></td><td rowspan="4"></td><td colspan="3"></td></tr><tr><td></td><td colspan="3"></td></tr><tr><td></td><td><img src="images/3eb5efeb8003255765b419af0ce5df995de556e6c5159ec6c63c193090f944e5.jpg"/></td><td colspan="2"></td></tr><tr><td></td><td colspan="3"></td></tr><tr><td>NOTE 40</td><td colspan="3">tcH(abs) is the absolute instantaneous clock high pulse width, as measured from one rising edge to the following falling edge. tcL(abs) is the absolute instantaneous clock low pulse width, as measured from one falling edge to the following rising edge.</td><td colspan="2"></td></tr><tr><td>NOTE 41</td><td colspan="5">Parameter twdos is calculated as the average write clock period across any consecutive 200 cycle window, where each clock period is calculated both from rising CK edge to rising CK edge, and falling CK edge to falling CK</td></tr><tr><td>NOTE 42</td><td colspan="5">edge. twQsH(avg) is defined as the average high pulse width, as calculated across any consecutive 200 high pulses.</td></tr><tr><td></td><td colspan="5">twQsL(avg) is defined as the average low pulse width, as calculated across any consecutive 200 low pulses. twQsH(abs) is the absolute instantaneous write clock high pulse width, as measured from one rising edge to the</td></tr><tr><td>NOTE 43</td><td colspan="5">following falling edge. twQsL(abs) is the absolute instantaneous write clock low pulse width, as measured from one falling edge to the following rising edge. twDQs2DQ 1 max delay variation as a function of the DC voltage variation for VDDQ. It includes VDDQ AC noise</td></tr><tr><td>NOTE 45</td><td colspan="5">impact for frequencies &gt; 20MHz and max voltage of TBD mVpk-pk from DC to 20 MHz at a fixed temperature on the package.</td></tr><tr><td>NOTE 46</td><td colspan="5">Actual values could be positive or negative numbers depending on design implementation and process. The parameter is referenced to IEEE1500 TEMPERATURE readout. See TEMPERATURE clauses.</td></tr><tr><td>NOTE 47</td><td colspan="5"></td></tr><tr><td>NOTE 48</td><td colspan="5">HBM4 supports a programmable tRPST as an optional feature. Support for this feature is indicated in the PROG RDQS PST bit field in the Device ID. See 13.5.11 DEVICE ID</td></tr><tr><td>11 Package (Die) Specification</td><td colspan="5"></td></tr></table>

## 11.1 Signals

Table 109 — I/O Signal Description
<table><tr><td colspan="1" rowspan="1">Signals</td><td colspan="1" rowspan="1">Type</td><td colspan="1" rowspan="1">Description</td></tr><tr><td colspan="1" rowspan="1">CK[31:0]_t, CK[31:0]_c</td><td colspan="1" rowspan="1">Input</td><td colspan="1" rowspan="1">Clock: CK t and CK c are differential clock inputs. Row and columncommand and address inputs are latched on the rising and falling edgesof CK.</td></tr><tr><td colspan="1" rowspan="1">C[31:0]_[7:0]</td><td colspan="1" rowspan="1">Input</td><td colspan="1" rowspan="1">Column command and address: the command code, bank and columnaddress for Write and Read operations and the mode register addressand code to be loaded with MODE REGISTER SET commands arereceived on the C[7:0] inputs.</td></tr><tr><td colspan="1" rowspan="1">R[31:0]_[9:0]</td><td colspan="1" rowspan="1">Input</td><td colspan="1" rowspan="1">Row command and address: the command code, bank and row addressfor Activate, Precharge and Refresh commands are received on theR[9:0] inputs.</td></tr><tr><td colspan="1" rowspan="1">ARFU[31:0]</td><td colspan="1" rowspan="1">Input</td><td colspan="1" rowspan="1">Reserved for future use: unused microbumps in AWORD.</td></tr><tr><td colspan="1" rowspan="1">APAR[31:0]</td><td colspan="1" rowspan="1">Input</td><td colspan="1" rowspan="1">Command / address parity: one parity signal per AWORD. APAR isassociated with C[7:0], R[9:0] and ARFU.</td></tr><tr><td colspan="1" rowspan="1">DQ[31:0] [63:0]</td><td colspan="1" rowspan="1">I/O</td><td colspan="1" rowspan="1">Data Input/Output: 64-bit data bus. DQ[31:0] represents the 32-bit databus of PC0 and DQ[63:32] represents the 32-bit data bus of PC1.</td></tr><tr><td colspan="1" rowspan="1">DBI[31:0]_[7:0]</td><td colspan="1" rowspan="1">I/O</td><td colspan="1" rowspan="1">Data Bus Inversion: DBI0 is associated with DQ[7:0], DBI1 isassociated with DQ[15:8], ... , and DBI7 is associated with DQ[63:56].</td></tr><tr><td colspan="1" rowspan="1">ECC[31:0]_[3:0]</td><td colspan="1" rowspan="1">I/O</td><td colspan="1" rowspan="1">ECC: ECC0, ECC1 are associated with DQ[31:0]. ECC2, ECC3 areassociated with DQ[63:32]</td></tr><tr><td colspan="1" rowspan="1">SEV[31:0]_[3:0]</td><td colspan="1" rowspan="1">I/O</td><td colspan="1" rowspan="1">SEV: SEV0, SEV1 are associated with DQ[31:0]. SEV2, SEV3 areassociated with DQ[63:32].</td></tr><tr><td colspan="1" rowspan="1">DPAR[31:0]_[1:0]</td><td colspan="1" rowspan="1">I/O</td><td colspan="1" rowspan="1">Data Parity: one data parity signal per DWORD. DPAR0 is associatedwith DQ[31:0] and DPAR1 is associated with DQ[63:32].</td></tr><tr><td colspan="1" rowspan="1">DERR[31:0]_[1:0]</td><td colspan="1" rowspan="1">Output</td><td colspan="1" rowspan="1">Data parity error: one data parity error bit per DWORD. DERR0 isassociated with DQ[31:0] and DERR1 is associated with DQ[63:32].</td></tr><tr><td colspan="1" rowspan="1">AERR[31:0]</td><td colspan="1" rowspan="1">Output</td><td colspan="1" rowspan="1">Address parity error. One address parity error bit for row and columnaddress and command per AWORD.</td></tr><tr><td colspan="1" rowspan="1">WDQS[31:0]_[1:0]_t,WDQS[31:0]_[1:0]_c</td><td colspan="1" rowspan="1">Input</td><td colspan="1" rowspan="1">Write Data Strobe: WDQS t and WDQS c are differential strobeinputs. One WDQS pair per DWORD. WDQS0 is associated withDQ[31:0] and WDQS1 is associated with DQ[63:32]</td></tr><tr><td colspan="1" rowspan="1">RDQS[31:0]_[1:0]_t,RDQS[31:0]_[1:0]_c</td><td colspan="1" rowspan="1">Output</td><td colspan="1" rowspan="1">Read Data Strobe: RDQS t and RDQS c are differential strobeoutputs. Read output data are sent on the rising and falling edges ofRDQS. One RDQS pair per DWORD. RDQS0 is associated withDQ[31:0] and RDQS1 is associated with DQ[63:32].</td></tr><tr><td colspan="1" rowspan="1">DA[39:0]</td><td colspan="1" rowspan="1">I/O</td><td colspan="1" rowspan="1">Direct Access Input/Output: These pins are provided for direct accesstest. They must be routed directly to an external package I/O pin. Thefunction is defined by the memory vendor</td></tr><tr><td colspan="1" rowspan="1">RESET_n</td><td colspan="1" rowspan="1">Input</td><td colspan="1" rowspan="1">Reset: RESET n LOW asynchronously initiates a full chip reset of theHBM4 device.</td></tr><tr><td colspan="1" rowspan="1">NC</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">No connect pad: electrically isolated</td></tr><tr><td colspan="1" rowspan="1">WRCK</td><td colspan="1" rowspan="1">Input</td><td colspan="1" rowspan="1">IEEE-1500 Wrapper Serial Port Clock</td></tr><tr><td colspan="1" rowspan="1">WRST_n</td><td colspan="1" rowspan="1">Input</td><td colspan="1" rowspan="1">IEEE-1500 Wrapper Serial Port Reset</td></tr><tr><td colspan="1" rowspan="1">SelectWIR</td><td colspan="1" rowspan="1">Input</td><td colspan="1" rowspan="1">IEEE-1500 Wrapper Serial Port Instruction Register Select</td></tr><tr><td colspan="1" rowspan="1">ShiftWR</td><td colspan="1" rowspan="1">Input</td><td colspan="1" rowspan="1">IEEE-1500 Wrapper Serial Port Shift</td></tr><tr><td colspan="1" rowspan="1">CaptureWR</td><td colspan="1" rowspan="1">Input</td><td colspan="1" rowspan="1">IEEE-1500 Wrapper Serial Port Capture</td></tr><tr><td colspan="1" rowspan="1">UpdateWR</td><td colspan="1" rowspan="1">Input</td><td colspan="1" rowspan="1">IEEE-1500 Wrapper Serial Port Update</td></tr><tr><td colspan="1" rowspan="1">WSI</td><td colspan="1" rowspan="1">Input</td><td colspan="1" rowspan="1">IEEE-1500 Wrapper Serial Port Data</td></tr><tr><td colspan="1" rowspan="1">WSO[31:0]</td><td colspan="1" rowspan="1">Output</td><td colspan="1" rowspan="1">IEEE-1500 Wrapper Serial Port Data Out</td></tr><tr><td colspan="1" rowspan="1">RD[31:0]_[3:0]</td><td colspan="1" rowspan="1">I/O</td><td colspan="1" rowspan="1">Redundant microbumps in DWORD</td></tr><tr><td colspan="1" rowspan="1">RA[31:0]</td><td colspan="1" rowspan="1">Input</td><td colspan="1" rowspan="1">Redundant command and address microbump in AWORD</td></tr><tr><td colspan="1" rowspan="1">RM[1:0]</td><td colspan="1" rowspan="1">Output</td><td colspan="1" rowspan="1">Redundant WSO microbump in MIDSTACK</td></tr><tr><td colspan="1" rowspan="1">MRFU[3:0]</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">Reserved for future use, unused microbumps in mid-stack region1</td></tr><tr><td colspan="1" rowspan="1">NOBUMP</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">Depopulated pad: reserved as test pad for probing</td></tr><tr><td colspan="1" rowspan="1">CATTRIP</td><td colspan="1" rowspan="1">Output</td><td colspan="1" rowspan="1">DRAM Catastrophic Temperature Report</td></tr><tr><td colspan="1" rowspan="1">VSS</td><td colspan="1" rowspan="1">Supply</td><td colspan="1" rowspan="1">Ground</td></tr><tr><td colspan="1" rowspan="1">VDDC, VDDQ, VPP,VDDQL</td><td colspan="1" rowspan="1">Supply</td><td colspan="1" rowspan="1">Power supply</td></tr><tr><td colspan="3" rowspan="1">NOTE 1Index [31:0] represents the channel indicator “0" to “31" of the HBM device. Signal names including the channelindicators are used whenever more than one channel and/or pseudo channel is referenced, as e.g., with the HBM4Bump Map. The channel indicators are omitted whenever features and functions common to all channels and/or allpseudo channels are described.NOTE 2HBM4 devices supporting less than 32 channels are allowed to have input/output buffers physically present at thepins associated with the unavailable channels, however these input/output buffers will be disabled. The host shallleave those pins floating. The availability of each channel [31:0] has to be coded in IEEE1500 DEVICE_IDWrapper Data Register bits [39:8]NOTE 3All power supply microbumps defined in Table 112 must be present and connected with their respective power netseven if the related channel is not present or marked non-working.</td></tr></table>

## 11.2 MicroBump Positions

The MicroBump array of the DRAM stack employs a staggered pattern as depicted in Figure 104 where a ‘staggered’ bump is located halfway between major row and column, hence its location is determined by X/2 and Y/2. Table 110 shows geometric parameters of the Staggered MicroBump pattern. Parameter $\mathrm { P } _ { \mathrm { m i n } }$ is the minimum bump pitch anywhere in the MicroBump field; for chosen X and Y parameters.

![](images/c888cda7106648cddb72333d48853d6d09f2fed4a53ac9a695cf43995d0aee4e.jpg)  
Figure 104 — Staggered MicroBump Pattern

Table 110 — Geometric Parameters of the Staggered MicroBump Pattern
<table><tr><td rowspan=1 colspan=1>Label</td><td rowspan=1 colspan=1>Nominal Value</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1> $7 0 \mu \mathrm { m }$ </td><td rowspan=1 colspan=1>Horizontal pitch of two adjacent MicroBumps</td></tr><tr><td rowspan=1 colspan=1>Y</td><td rowspan=1 colspan=1> $1 1 0 \mu \mathrm { m }$ </td><td rowspan=1 colspan=1>Vertical pitch of two adjacent MicroBumps</td></tr><tr><td rowspan=1 colspan=1> $\mathrm { P } _ { \mathrm { m i n } }$ </td><td rowspan=1 colspan=1> $6 5 ~ { \mu \mathrm { m } }$ </td><td rowspan=1 colspan=1>Minimum pitch of the bump field</td></tr><tr><td rowspan=1 colspan=1>D</td><td rowspan=1 colspan=1> $2 8 \mu \mathrm { m }$ </td><td rowspan=1 colspan=1>MicroBump diameter</td></tr><tr><td rowspan=1 colspan=1>S</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Bump-to-bump air gap; $ { \mathbf { S } } =  { \mathbf { P } } _ { \mathrm { M i n } } -  { \mathbf { D } }$ </td></tr></table>

The HBM4 bump map is defined as shown in subsequent tables. Please refer to MO-362 for device dimensions.

![](images/517520447420ce0e5510d9994b5c130520922a83cf5fe8dc0b4ac223380c955d.jpg)  
Figure 105 — MicroBump Pillar Diameter

## 11.2 MicroBump Positions (cont’d)

Two HBM bump maps are defined as shown in the subsequent tables and are referred to as Footprint A and Footprint B. Footprint A is specified for the 24 Gb/die configuration and Footprint B is specified for the 32 Gb/die configuration as in Table 111.

Footprint A consists of 161 rows with a pitch of Y/2 and 308 columns with a pitch of X/2. The overall array size is $( 3 0 7 \times \mathrm { X } / 2 + \mathrm { D } ) \times ( 1 6 0 \times \mathrm { Y } / 2 + \mathrm { D } ) = 1 0 7 7 3 . 0 ~ \mathrm { { \mu m } \times 8 8 2 8 . 0 }$ μm. The bump map is center aligned with the die. The bump map center is the origin of the bump location coordinates. Bump A1 is located at the top left at $\mathrm { X } = - 5 3 7 2 . 5 \mu \mathrm { m } , \mathrm { Y } = + 4 4 0 0 . 0 \mu \mathrm { m } .$

Footprint B consists of 161 rows with a pitch of Y/2 and 348 columns with a pitch of X/2. The overall array size is $( 3 4 7 \times \mathrm { X } / 2 + \mathrm { D } ) \times ( \bar { 1 } 6 0 \times \mathrm { Y } / 2 + \mathrm { D } ) = 1 2 1 7 3 . 0 ~ \mathrm { \textmu m } \times 8 8 2 8 . 0 ~ \mathrm { \textmu m }$ . The bump map is center aligned with the die. The bump map center is the origin of the bump location coordinates. Bump A1 is located at the top left at X = -6072.5 μm, Y = +4400.0 μm.

## 11.3 HBM4 Device Dimensions

Table 111 — HBM4 Device Dimensions
<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Configuration</td><td rowspan=1 colspan=1>Minimum</td><td rowspan=1 colspan=1>Nominal</td><td rowspan=1 colspan=1>Maximum</td><td rowspan=1 colspan=1>Unit</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=2 colspan=1>Width</td><td rowspan=2 colspan=1>X</td><td rowspan=1 colspan=1>24Gb/die</td><td rowspan=1 colspan=1>12.75</td><td rowspan=1 colspan=1>12.775</td><td rowspan=1 colspan=1>12.8</td><td rowspan=1 colspan=1>mm</td><td rowspan=3 colspan=1>3,4,5</td></tr><tr><td rowspan=1 colspan=1>32Gb/die</td><td rowspan=1 colspan=1>14.15</td><td rowspan=1 colspan=1>14.175</td><td rowspan=1 colspan=1>14.2</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Length</td><td rowspan=1 colspan=1>Y</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>10.95</td><td rowspan=1 colspan=1>10.975</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>mm</td></tr><tr><td rowspan=4 colspan=1>Height</td><td rowspan=4 colspan=1>Z</td><td rowspan=1 colspan=1>4-High</td><td rowspan=1 colspan=1>750</td><td rowspan=1 colspan=1>775</td><td rowspan=1 colspan=1>800</td><td rowspan=1 colspan=1>μm</td><td rowspan=4 colspan=1>1,2</td></tr><tr><td rowspan=1 colspan=1>8-High</td><td rowspan=1 colspan=1>750</td><td rowspan=1 colspan=1>775</td><td rowspan=1 colspan=1>800</td><td rowspan=1 colspan=1>μm</td></tr><tr><td rowspan=1 colspan=1>12-High</td><td rowspan=1 colspan=1>750</td><td rowspan=1 colspan=1>775</td><td rowspan=1 colspan=1>800</td><td rowspan=1 colspan=1>μm</td></tr><tr><td rowspan=1 colspan=1>16-High</td><td rowspan=1 colspan=1>750</td><td rowspan=1 colspan=1>775</td><td rowspan=1 colspan=1>800</td><td rowspan=1 colspan=1>μm</td></tr><tr><td rowspan=1 colspan=8>NOTE 1 The configuration refers to the number of memory dies in the stack. The stack may include an additional base(interface) die.NOTE 2 Refer to MO-362 for related package drawings.NOTE 3 Refer to MO-362 for X and Y dimension min/Max tolerances and related package drawings.NOTE 4 Refer to Footprint A in JESD271-4 &quot;High Bandwidth Memory (HBM4) DRAM Bump Map Spreadsheet&quot; fordetails on the 24 Gb/die footprint.NOTE 5 Refer to Footprint B in JESD271-4 &quot;High Bandwidth Memory (HBM4) DRAM Bump Map Spreadsheet&quot; fordetails on the 32 Gb/die footprint.</td></tr></table>

## 11.4 HBM4 Bump Map

A geographical overview of the HBM4 bump maps is provided in Table 112 for Footprint A and Table 113 for Footprint B. An overview of the Footprint A and B bump maps are shown in Figure 107 and Figure 108, respectively, and the detailed bump map is provided in JESD271-4 "High Bandwidth Memory (HBM4) DRAM Bump Map Spreadsheet". Bump maps for both footprints follow orientations defined by MO-362 as well as Figure 107 and Figure 108, which are represented with the user perspective as detailed in Figure 106. Refer to the JEDEC website for the latest version of JESD271-4.

![](images/61df85a53842cdbe8e8578d63292e709e78cc35cf7d643dff42cc4202143ed0d.jpg)  
Figure 106 — Figure Overview of HBM4 Bump Map Footprint

Table 112 — HBM4 Bump Map Footprint A – Geographical Overview (not to scale)
<table><tr><td rowspan=1 colspan=2>Columns</td><td rowspan=1 colspan=1>1, 2</td><td rowspan=1 colspan=2>3 ... 62</td><td rowspan=1 colspan=1>63 .. 85</td><td rowspan=1 colspan=3>86 ... 94</td><td rowspan=1 colspan=1>95 ... 177</td><td rowspan=1 colspan=1>178 ... 188</td><td rowspan=1 colspan=1>189 .. 202</td><td rowspan=1 colspan=1>203 . 216</td><td rowspan=1 colspan=1>217 . 230</td><td rowspan=1 colspan=1>231 .…. 244</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>251 .. 264</td><td rowspan=1 colspan=1>265 . 278</td><td rowspan=1 colspan=1>279 . 292</td><td rowspan=1 colspan=1>293 ... 306</td><td rowspan=1 colspan=1>3030</td></tr><tr><td rowspan=18 colspan=1></td><td rowspan=1 colspan=1>A ... K</td><td rowspan=1 colspan=4>Upper Left EdgePower Supply Region</td><td rowspan=1 colspan=5>Upper Center EdgePower Supply Region</td><td rowspan=1 colspan=9>Upper Right EdgePower Supply Region</td><td rowspan=18 colspan=1>enpl Bampas</td></tr><tr><td rowspan=1 colspan=1>L ... AD</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD0Channel 28</td><td rowspan=1 colspan=1>DWORD0Channel 24</td><td rowspan=1 colspan=1>DWORD0Channel 20</td><td rowspan=1 colspan=1>DWORD0Channel 16</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD0Channel 12</td><td rowspan=1 colspan=1>DWORD0Channel 8</td><td rowspan=1 colspan=1>DWORD0Channel 4</td><td rowspan=1 colspan=1>DWORD0Channel 0</td></tr><tr><td rowspan=2 colspan=1>AE ... AK</td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=2></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=2></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>AWORDChannel 28</td><td rowspan=2 colspan=1>AWORDChannel 24</td><td rowspan=2 colspan=1>AWORDChannel 20</td><td rowspan=2 colspan=2>AWORDChannel 16</td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>AWORDChannel 12</td><td rowspan=2 colspan=1>AWORDChannel 8</td><td rowspan=2 colspan=1>AWORDChannel 4</td></tr><tr><td rowspan=1 colspan=3></td><td></td></tr><tr><td rowspan=1 colspan=1>AL ... BD</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3></td><td rowspan=9 colspan=1>DirectAccessTestPort</td><td rowspan=9 colspan=1>Center SupplyRegion</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD1Channel 28</td><td rowspan=1 colspan=1>DWORD1Channel 24</td><td rowspan=1 colspan=1>DWORD1Channel 20</td><td rowspan=1 colspan=1>DWORD1Channel 16</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD1Channel 12</td><td rowspan=1 colspan=1>DWORD1Channel 8</td><td rowspan=1 colspan=1>DWORD1Channel 4</td><td rowspan=1 colspan=1>DWORD1Channel 0</td></tr><tr><td rowspan=1 colspan=1>BE ... BV</td><td rowspan=4 colspan=1></td><td rowspan=7 colspan=2>PowerSupply</td><td rowspan=7 colspan=1>LeftDepopu-latedMicropillarAreaDedicatedfor(Optional)</td><td></td><td></td><td rowspan=2 colspan=1></td><td rowspan=1 colspan=1>DWORD0Channel 29</td><td rowspan=1 colspan=1>DWORD0Channel 25</td><td rowspan=1 colspan=1>DWORD0Channel 21</td><td rowspan=1 colspan=1>DWORD0Channel 17</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD0Channel 13</td><td rowspan=1 colspan=1>DWORD0Channel 9</td><td rowspan=1 colspan=1>DWORD0Channel 5</td><td rowspan=1 colspan=1>DWORD0Channel 1</td></tr><tr><td rowspan=1 colspan=1>BW ... CDCD</td><td></td><td></td><td rowspan=1 colspan=1>AWORDChannel 29</td><td rowspan=1 colspan=1>AWORDChannel 25</td><td rowspan=1 colspan=1>AWORDChannel 21</td><td rowspan=1 colspan=1>AWORDChannel 17</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>AWORDChannel 13</td><td rowspan=1 colspan=1>AWORDChannel 9</td><td rowspan=1 colspan=1>AWORDChannel 5</td><td rowspan=1 colspan=1>AWORDChannel 1</td></tr><tr><td rowspan=1 colspan=1>CE ... CT</td><td></td><td></td><td rowspan=6 colspan=1>RightDepoplua-ted Area</td><td rowspan=2 colspan=1>DWORD1Channel 29</td><td rowspan=2 colspan=1>DWORD1Channel 25</td><td rowspan=2 colspan=1>DWORD1Channel 21</td><td rowspan=2 colspan=1>DWORD1Channel 17</td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>DWORD1Channel 13</td><td rowspan=2 colspan=1>DWORD1Channel 9</td><td rowspan=2 colspan=1>DWORD1Channel 5</td><td rowspan=2 colspan=1>DWORD1Channel 1</td></tr><tr><td rowspan=1 colspan=1>CU, CV</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>CW ... DC</td><td rowspan=1 colspan=1></td><td></td><td></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Reset, IEEE15</td><td rowspan=1 colspan=1>00 Port, etc..</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>VD</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Reset, IEEE15</td><td rowspan=1 colspan=1>00 Port, etc...</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>DD, DE</td><td rowspan=3 colspan=1></td><td rowspan=3 colspan=2>Re</td><td></td><td></td><td rowspan=2 colspan=1>DWORD1Channel 30</td><td rowspan=2 colspan=1>DWORD1Channel 26</td><td rowspan=2 colspan=1>DWORDIChannel 22</td><td rowspan=2 colspan=1>DWORD1Channel 18</td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>DWORD1Channel 14</td><td rowspan=2 colspan=1>DWORD1Channel 10</td><td rowspan=2 colspan=1>DWORDIChannel 6</td><td rowspan=2 colspan=1>DWORD1Channel 2</td></tr><tr><td rowspan=1 colspan=1>DF ... DU</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>DW ... EC</td><td rowspan=1 colspan=1>ProbePads</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1>AWORDChannel 30</td><td rowspan=1 colspan=1>AWORDChannel 26</td><td rowspan=1 colspan=1>AWORDChannel 22</td><td rowspan=1 colspan=1>AWORDChannel 18</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>AWORDChannel 14</td><td rowspan=1 colspan=1>AWORDChannel 10</td><td rowspan=1 colspan=1>AWORDChannel 6</td><td rowspan=1 colspan=1>AWORDChannel 2</td></tr><tr><td rowspan=1 colspan=1>ED ... EU</td><td rowspan=1 colspan=1></td><td rowspan=4 colspan=2></td><td rowspan=4 colspan=1></td><td rowspan=4 colspan=3></td><td rowspan=4 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD0Channel 30</td><td rowspan=1 colspan=1>DWORD0Channel 26</td><td rowspan=1 colspan=1>DWORD0Channel 22</td><td rowspan=1 colspan=1>DWORD0Channel 18</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD0Channel 14</td><td rowspan=1 colspan=1>DWORD0Channel 10</td><td rowspan=1 colspan=1>DWORD0Channel 6</td><td rowspan=1 colspan=1>DWORD0Channel 2</td></tr><tr><td rowspan=1 colspan=1>EV ... FL</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD1Channel 31</td><td rowspan=1 colspan=1>DWORD1Channel 27</td><td rowspan=1 colspan=1>DWORD1Channel 23</td><td rowspan=1 colspan=1>DWORD1Channel 19</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD1Channel 15</td><td rowspan=1 colspan=1>DWORD1Channel 11</td><td rowspan=1 colspan=1>DWORD1Channel 7</td><td rowspan=1 colspan=1>DWORD1Channel 3</td></tr><tr><td rowspan=1 colspan=1>FM ... FU</td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=1 colspan=1>AWORDChannel 31</td><td rowspan=1 colspan=1>AWORDChannel 27</td><td rowspan=1 colspan=1>AWORDChannel 23</td><td rowspan=1 colspan=1>AWORDChannel 19</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>AWORDChannel 15</td><td rowspan=1 colspan=1>AWORDChannel 11</td><td rowspan=1 colspan=1>AWORDChannel 7</td><td rowspan=1 colspan=1>AWORDChannel 3</td></tr><tr><td rowspan=1 colspan=1>FV ... GL</td><td rowspan=1 colspan=1>DWORD0Channel 31</td><td rowspan=1 colspan=1>DWORD0Channel 27</td><td rowspan=1 colspan=1>DWORD0Channel 23</td><td rowspan=1 colspan=1>DWORD0Channel 19</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD0Channel 15</td><td rowspan=1 colspan=1>DWORD0Channel 11</td><td rowspan=1 colspan=1>DWORD0Channel 7</td><td rowspan=1 colspan=1>DWORD0Channel 3</td></tr><tr><td rowspan=1 colspan=1>GM ... HA</td><td rowspan=1 colspan=4>Lower Left EdgePower Supply Region</td><td rowspan=1 colspan=5>Lower Center EdgePower Supply Region</td><td rowspan=1 colspan=9>Lower Right EdgePower Supply Region</td></tr></table>

## 11.4 HBM4 Bump Map (cont’d)

Table 113 — HBM4 Bump Map Footprint B – Geographical Overview (not to scale)
<table><tr><td rowspan=1 colspan=2>Columns</td><td rowspan=1 colspan=2>1,2</td><td rowspan=1 colspan=2>3 ... 102</td><td rowspan=1 colspan=1>103 .. 125</td><td rowspan=1 colspan=1>126 ...134</td><td rowspan=1 colspan=1>135 ... 217</td><td rowspan=1 colspan=1>218 .. 228</td><td rowspan=1 colspan=1>229 .. 242</td><td rowspan=1 colspan=1>243 ... 2256</td><td rowspan=1 colspan=1>257 . 270</td><td rowspan=1 colspan=1>271 .. 284</td><td rowspan=1 colspan=1>....</td><td rowspan=1 colspan=1>291 ... 304</td><td rowspan=1 colspan=1>305 ...3118</td><td rowspan=1 colspan=1>319 ..332</td><td rowspan=1 colspan=1>333 . 346</td><td rowspan=1 colspan=1>34</td></tr><tr><td rowspan=7 colspan=1></td><td rowspan=1 colspan=1>A ... K</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2>UpperLeftPower Suppl</td><td rowspan=1 colspan=1>Edgey Region</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>UpperCenterE dgePower Supply Re gion</td><td rowspan=1 colspan=9>UpperRight EdgePower Supply Region</td><td rowspan=21 colspan=1>ena Bapds</td></tr><tr><td rowspan=1 colspan=1>L ... AD</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORDOChanne128</td><td rowspan=1 colspan=1>DWORD0Cha nnel 24</td><td rowspan=1 colspan=1>DWORD0Channel 20</td><td rowspan=1 colspan=1>DWORDOChannel 16</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD0Channel 12</td><td rowspan=1 colspan=1>DWORD0Channe18</td><td rowspan=1 colspan=1>DWORD0Channe14</td><td rowspan=1 colspan=1>DWORD0Cha nne 10</td></tr><tr><td rowspan=1 colspan=1>AE ... AK</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>AWORDChanne128</td><td rowspan=1 colspan=1>AWORDChannel 24</td><td rowspan=1 colspan=1>AWORDChanne1 20</td><td rowspan=1 colspan=1>AWORDChannel 16</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>AWORDChannel 12</td><td rowspan=1 colspan=1>AWORDChannel8</td><td rowspan=1 colspan=1>AWORDChannel 4</td><td rowspan=1 colspan=1>AWORDChannel0</td></tr><tr><td rowspan=1 colspan=1>AL ... BD</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=1 colspan=1>DWORD1Channe1 28</td><td rowspan=1 colspan=1>DWORD1Channel 24</td><td rowspan=1 colspan=1>DWORD1Channe120</td><td rowspan=1 colspan=1>DWORD1Channel 16</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD1Channel 12</td><td rowspan=1 colspan=1>DWORD1Channe18</td><td rowspan=1 colspan=1>DWORD1Channe14</td><td rowspan=1 colspan=1>DWORD1Channe10</td></tr><tr><td rowspan=1 colspan=1>BE ... BV</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=16 colspan=1>RightDepoplua-ted Area</td><td rowspan=1 colspan=1>DWORD0Channe1 29</td><td rowspan=1 colspan=1>DWORD0Channel 25</td><td rowspan=1 colspan=1>DWORD0Channel 21</td><td rowspan=1 colspan=1>DWORDOChannel 17</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD0Channel 13</td><td rowspan=1 colspan=1>DWORD0Channe19</td><td rowspan=1 colspan=1>DWORD0Channe15</td><td rowspan=1 colspan=1>DWORD0Channel1</td></tr><tr><td rowspan=1 colspan=1>BW ... CD</td><td rowspan=7 colspan=2>ea Banps</td><td rowspan=8 colspan=2>PowerSupplyRegion</td><td rowspan=1 colspan=1>Left Depopu-lated</td><td rowspan=1 colspan=1></td><td rowspan=3 colspan=1>Center Supply</td><td rowspan=1 colspan=1>AWORDChanne1 29</td><td rowspan=1 colspan=1>AWORDChannel 25</td><td rowspan=1 colspan=1>AWORDChannel 21</td><td rowspan=1 colspan=1>AWORDChannel 17</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>AWORDChannel 13</td><td rowspan=1 colspan=1>AWORDChannel9</td><td rowspan=1 colspan=1>AWORDChannel 5</td><td rowspan=1 colspan=1>AWORDChannel 1</td></tr><tr><td rowspan=1 colspan=1>CE ... CT</td><td rowspan=2 colspan=1>MicropillarArea</td><td rowspan=2 colspan=1>Direct</td><td rowspan=2 colspan=1>DWORD1Channe129</td><td rowspan=2 colspan=1>DWORD1Channel 25</td><td rowspan=2 colspan=1>DWORDIChannel 21</td><td rowspan=2 colspan=1>DWORDIChannel 17</td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>DWORD1Channel 13</td><td rowspan=2 colspan=1>DWORD1Channe19</td><td rowspan=2 colspan=1>DWORD1Channe15</td><td rowspan=2 colspan=1>DWORD1Channe11</td></tr><tr><td rowspan=14 colspan=1></td><td rowspan=1 colspan=1>Cu, CV</td></tr><tr><td rowspan=1 colspan=1>CW... DC</td><td rowspan=5 colspan=1>Dedicatedfor(Optional)</td><td rowspan=7 colspan=1>TestPort</td><td rowspan=7 colspan=1>Region</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Reset, EEE150</td><td rowspan=1 colspan=1>0 Port, etc...</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>VD</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Reset, EEE150</td><td rowspan=1 colspan=1>0 Port, etc.</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>DD, DE</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td rowspan=3 colspan=2></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td rowspan=2 colspan=1>DWORDIChanne130</td><td rowspan=2 colspan=1>DWORD1Channel 26</td><td rowspan=2 colspan=1>DWORD1Channel 22</td><td rowspan=2 colspan=1>DWORD1Channel 18</td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>DWORD1Channel 14</td><td rowspan=2 colspan=1>DWORD1Channel 10</td><td rowspan=2 colspan=1>DWORD1Channe16</td><td rowspan=2 colspan=1>DWORD1Channe12</td></tr><tr><td rowspan=1 colspan=1>DF ... DU</td></tr><tr><td rowspan=2 colspan=1>DW... EC</td><td rowspan=2 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=2 colspan=2></td><td rowspan=2 colspan=1>Pads</td><td rowspan=2 colspan=1>AWORDChanne130</td><td rowspan=2 colspan=1>AWORDChamnel 26</td><td rowspan=2 colspan=1>AWORDChannel22</td><td rowspan=2 colspan=1>AWORDChannel 18</td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>AWORDChannel 14</td><td rowspan=2 colspan=1>AWORDChannel 10</td><td rowspan=2 colspan=1>AWORDChannel6</td><td rowspan=2 colspan=1>AWORDChannel 2</td></tr><tr><td rowspan=1 colspan=2></td></tr><tr><td rowspan=1 colspan=1>ED ... EU</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=5 colspan=1></td><td rowspan=1 colspan=1>DWORDOChame130</td><td rowspan=1 colspan=1>DWORD0Channel 26</td><td rowspan=1 colspan=1>DWORD0Channel 22</td><td rowspan=1 colspan=1>DWORD0Channel 18</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD0Channel 14</td><td rowspan=1 colspan=1>DWORD0Channel 10</td><td rowspan=1 colspan=1>DWORD0Channe16</td><td rowspan=1 colspan=1>DWORD0Channe12</td></tr><tr><td rowspan=1 colspan=1>EV ... FL</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD1Channe131</td><td rowspan=1 colspan=1>DWORD1Channel 27</td><td rowspan=1 colspan=1>DWORD1Channel 23</td><td rowspan=1 colspan=1>DWORD1Channel 19</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD1Channel 15</td><td rowspan=1 colspan=1>DWORD1Channel 11</td><td rowspan=1 colspan=1>DWORD1Channe1 7</td><td rowspan=1 colspan=1>DWORD1Channe13</td></tr><tr><td rowspan=2 colspan=1>FM ...FU</td><td rowspan=2 colspan=2></td><td rowspan=3 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=3 colspan=1></td><td rowspan=2 colspan=1>AWORDChanne131</td><td rowspan=2 colspan=1>AWORDChannel 27</td><td rowspan=2 colspan=1>AWORDChannel23</td><td rowspan=2 colspan=1>AWORDChannel 19</td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>AWORDChannel 15</td><td rowspan=2 colspan=1>AWORDChannel 11</td><td rowspan=2 colspan=1>AWORDChannel 7</td><td rowspan=2 colspan=1>AWORDChannel3</td></tr><tr><td rowspan=2 colspan=2></td></tr><tr><td rowspan=1 colspan=1>FV ..GL</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD0Channe131</td><td rowspan=1 colspan=1>DWORD0Channel 27</td><td rowspan=1 colspan=1>DWORD0Channel 23</td><td rowspan=1 colspan=1>DWORD0Channel 19</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DWORD0Channel 15</td><td rowspan=1 colspan=1>DWORD0Channel 11</td><td rowspan=1 colspan=1>DWORD0Channe17</td><td rowspan=1 colspan=1>DWORD0Channe13</td></tr><tr><td rowspan=1 colspan=1>GM .. HA</td><td rowspan=1 colspan=5>LowerLeft EdgePower Supply Region</td><td rowspan=1 colspan=3>LowerCenterEdgePower Supply Re gion</td><td rowspan=1 colspan=9>Lower Right EdgePower Supply Re gion</td></tr></table>

![](images/9a8ba63d8402d0005ee58ed0831b2a5f30c15b6e34311f9c17a1022ecf71e216.jpg)  
Figure 107 — Overview of HBM4 Bump Map Footprint A

## 11.4 HBM4 Bump Map (cont’d)

![](images/207752bcd34a001de2864fe975dec78895bfa11143036f9c4351dd9200e0a3f2.jpg)  
Figure 108 — Overview of HBM4 Bump Map Footprint B

## 11.4.1 HBM4 Bump Map Footprint Compatibility

The HBM4 bump map Footprint B is a superset of Footprint A allowing for compatibility between the two bump map footprints enabling users to re-use the 32 Gb/die interposer and package designs for the 24 Gb/die configuration. Using the 24 Gb/die configuration on an interposer designed for Footprint B will require NC bumps on the left edges of Footprint A to be connected to V<sub>DDC</sub>, V<sub>DDQ</sub>, V<sub>PP</sub>, and V<sub>SS</sub> bumps of the respective edge locations on Footprint B as shown in Table 114 and Figure 109.

Table 114 — HBM4 Footprint A and Footprint B Signal Compatibility
<table><tr><td rowspan=1 colspan=1>Footprint BPin Number</td><td rowspan=1 colspan=1>Footprint ASignal</td><td rowspan=1 colspan=1>Footprint BSignal</td><td rowspan=1 colspan=1>Footprint BPin Number</td><td rowspan=1 colspan=1>Footprint ASignal</td><td rowspan=1 colspan=1>Footprint BSignal</td></tr><tr><td rowspan=1 colspan=1>A41</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VDDC</td><td rowspan=1 colspan=1>GR41</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VPP</td></tr><tr><td rowspan=1 colspan=1>C41</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VDDC</td><td rowspan=1 colspan=1>GT42</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VPP</td></tr><tr><td rowspan=1 colspan=1>GW41</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VDDC</td><td rowspan=1 colspan=1>A43</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VSS</td></tr><tr><td rowspan=1 colspan=1>HA41</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VDDC</td><td rowspan=1 colspan=1>B44</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VSS</td></tr><tr><td rowspan=1 colspan=1>A7</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VDDQ</td><td rowspan=1 colspan=1>C43</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VSS</td></tr><tr><td rowspan=1 colspan=1>B6</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VDDQ</td><td rowspan=1 colspan=1>D44</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VSS</td></tr><tr><td rowspan=1 colspan=1>GY46</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VDDQ</td><td rowspan=1 colspan=1>GV44</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VSS</td></tr><tr><td rowspan=1 colspan=1>HA47</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VDDQ</td><td rowspan=1 colspan=1>GW43</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VSS</td></tr><tr><td rowspan=1 colspan=1>F42</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VPP</td><td rowspan=1 colspan=1>GY44</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VSS</td></tr><tr><td rowspan=1 colspan=1>G41</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VPP</td><td rowspan=1 colspan=1>HA43</td><td rowspan=1 colspan=1>NC</td><td rowspan=1 colspan=1>VSS</td></tr></table>

## 11.4.1 HBM4 Bump Map Footprint Compatibility (cont’d)

Top Corner  
![](images/88ae517c229fc5c07f478a3df62854039680a4ffcd47488101b222345cd04efa.jpg)  
Figure 109 — Overview of HBM4 Bump Map Footprint Compatibility (Overlapping Bumps are Highlighted)

The HBM4 DRAM assembly is not defined by this standard. The shape and materials of the die to die interfaces between the die in the HBM4 DRAM are not defined in this standard and the shape (annular, cone, cylinder, etc.) and materials (Cu, W) are not defined or restricted in this standard. However, these interfaces must fit within the electrical requirements of the channel interface.

HBM4 DRAMs provide two separate test interfaces as described below:

<sup></sup> A direct access(DA) test port intended for the vendor to access the HBM4 device independent of the host;

<sup></sup> An IEEE 1500 Standard test port, to be controlled by the host.

## 13.1 Direct Access (DA) Test Port

A direct access (DA) test port is available via DA[39:0] for vendor specific test implementations. Two microbumps are associated with each DA pin. A depopulated area for probing is located close to the DA port region in columns 86 to 94 of the HBM4 bump map (See HBM4 Bump Map clause).

Access to the DA test port is controlled via pin DA12. When DA12 = LOW, DA[39:13][11:0] drivers are in Hi-Z and input receivers are disabled allowing the bus to float. When DA12 = HIGH, DA[39:13][11:0] are enabled for vendor specific test features and the IEEE 1500 port is disabled. CATTRIP output remains active but their state may not be valid and shall be ignored. The DA12 input is equipped with an internal pull-down resistor which ensures that DA12 is held LOW and the test port remains inactive even if the pin is left floating.

The DA test port may be enabled at any time after the power ramp has been completed and all supply voltages are within their defined ranges (t<sub>INIT0</sub>), and after waiting for at least t<sub>INIT1</sub> time. The level of the RESET\_n pin shall be irrelevant for DA test port enabling.

The DA test port may be disabled at any time by pulling DA12 to LOW. The HBM4 DRAM may then resume normal operation after performing a device initialization as described in the Initialization Sequence with Stable Power clauses.

8 DA pins are designated to connect point-to-point to each HBM4 DRAM. 32 pins are designated to connect in parallel to up to four HBM4 DRAM devices on a multi drop bus as shown in Figure 110. The function of each of these pins is vendor specific. Table 115 defines which DA pins are allocated for point to-point and for multi drop.

Table 115 — Direct Access (DA) Pin Allocation
<table><tr><td rowspan=1 colspan=1>Pin Group</td><td rowspan=1 colspan=1>DA Pin List</td><td rowspan=1 colspan=1>Pin Count</td></tr><tr><td rowspan=1 colspan=1>Point to Point</td><td rowspan=1 colspan=1>DA[19:12]</td><td rowspan=1 colspan=1>8</td></tr><tr><td rowspan=1 colspan=1>Multi Drop</td><td rowspan=1 colspan=1>DA[39:20][11:0]</td><td rowspan=1 colspan=1>32</td></tr></table>

## 13.1 Direct Access (DA) Test Port (cont’d)

![](images/9bea9df53ff80227131d0d2db72d7625805d9a0da7566e66c77f0e9a27340f64.jpg)  
Figure 110 — DA Port Connection Diagram For Multiple HBM4 DRAM Devices

## 13.1.1 DA Test Port Lockout

The DA test port can be disabled (locked) by setting MR8 OP0 bit to 1. The bit is defined for channels 0 or 4 only. Once the bit is set to 1, the DA test port will remain disabled unless power is removed from the HBM4 DRAM. Any chip reset through pulling RESET\_n LOW or via IEEE1500 HBM\_RESET instruction, or writing a 0 via an MRS command or IEEE1500 instruction   
MODE\_REGISTER\_DUMP\_SET will not clear the locked state.

## 13.2 IEEE Standard 1500

The IEEE Standard 1500 compliant test access port provides a direct test connection between a host and the HBM4 DRAM. The HBM4 DRAM’s test port extends the standard specification and replicates the WSO output per channel. This allows some instructions to be executed in parallel across channels, and eliminates the need for cross-channel arbitration for WSO.

IEEE 1500 operations may be asserted at any time after device initialization and during normal memory operation including when the HBM4 DRAM is in power-down or self refresh mode. See an Interaction with Mission Mode Operation clause for how the various instructions interact with normal operation, and requirements for returning to normal operation. See also clause on Initialization Sequence For Use Of IEEE 1500 Instruction Including Lane Repairs and Channel Disable for a subset of operations that are allowed before the device initialization has been completed.

Please refer to ieee.org for more details about the IEEE1500 standard.

## 13.2.1 Interaction Between DA Test Port and IEEE1500 Test Access Port

DA12 = LOW selects the IEEE1500 test access port and DA12 = HIGH selects the DA test port. It is possible to operate the HBM4 DRAM without using the test ports. In this case the internal pull-down resistor on DA12 or pulling DA12 LOW in the system will keep the DA test port disabled, and pulling WRST\_n LOW in the system will keep the IEEE1500 test port disabled.

## 13.2.1 Interaction Between DA Test Port and IEEE1500 Test Access Port (cont’d)

Table 116 summarizes the status of the test access port signals.

Table 116 — Test Access Port Signal Status
<table><tr><td rowspan=1 colspan=1>WRST_n</td><td rowspan=1 colspan=1>DA12, MR8 OP0</td><td rowspan=1 colspan=1>Signal Name</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Status</td></tr><tr><td rowspan=3 colspan=1>LOW</td><td rowspan=3 colspan=1>DA12 = LOW or MR8 OP0 = 1</td><td rowspan=1 colspan=1>Other IEEE1500 inputs1</td><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>X (Don&#x27;t Care)</td></tr><tr><td rowspan=1 colspan=1>WSO</td><td rowspan=1 colspan=1>Output</td><td rowspan=1 colspan=1>V (Valid)2</td></tr><tr><td rowspan=1 colspan=1>DA[39:13][11:0]</td><td rowspan=1 colspan=1>I/O</td><td rowspan=1 colspan=1>X (Don&#x27;t Care)</td></tr><tr><td rowspan=3 colspan=1>HIGH</td><td rowspan=3 colspan=1>DA12 = LOW or MR8 OP0 = 1</td><td rowspan=1 colspan=1>Other IEEE1500 inputs1</td><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>Active</td></tr><tr><td rowspan=1 colspan=1>WSO</td><td rowspan=1 colspan=1>Output</td><td rowspan=1 colspan=1>V (Valid)2</td></tr><tr><td rowspan=1 colspan=1>DA[39:13][11:0]</td><td rowspan=1 colspan=1>I/O</td><td rowspan=1 colspan=1>X (Don&#x27;t Care)</td></tr><tr><td rowspan=3 colspan=1>Don&#x27;t Care</td><td rowspan=3 colspan=1>DA12 = HIGH and MR8 OP0 = 0</td><td rowspan=1 colspan=1>Other IEEE1500 inputs1</td><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>X (Don&#x27;t Care)</td></tr><tr><td rowspan=1 colspan=1>WSO</td><td rowspan=1 colspan=1>Output</td><td rowspan=1 colspan=1>V (Valid)²</td></tr><tr><td rowspan=1 colspan=1>DA[39:13][11:0]</td><td rowspan=1 colspan=1>I/O</td><td rowspan=1 colspan=1>Vendor specific³</td></tr><tr><td rowspan=1 colspan=5>NOTE 1 WRCK, SelectWIR, ShiftWR, CaptureWR, UpdateWR, WSINOTE 2 V = Valid Signal (either HIGH or LOW, but not floating).NOTE 3 Please refer to vendor&#x27;s datasheet.</td></tr></table>

## 13.2.2 IEEE1500 Test Access Port I/O Signals

Table 117 — IEEE1500 Test Port Signal List and Description
<table><tr><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>WRCK</td><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>Dedicated clock used to operate IEEE Std 1500 functions.</td></tr><tr><td rowspan=1 colspan=1>WRST_n</td><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>When pulled LOW, WRST n asynchronously puts the IEEE1500 test port intoits normal system mode. No WRCK clocks are required when WRST n isLOW. See WDR Reset State</td></tr><tr><td rowspan=1 colspan=1>WSI</td><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>IEEE1500 test port serial input</td></tr><tr><td rowspan=1 colspan=1>SelectWIR</td><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>SelectWIR determines whether the instruction register (WIR) or a wrapper dataregister is being accessed.</td></tr><tr><td rowspan=1 colspan=1>CaptureWR</td><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>Controls a Capture operation in the selected wrapper register (WR)</td></tr><tr><td rowspan=1 colspan=1>ShiftWR</td><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>Controls a Shift operation in the selected wrapper register (WR)</td></tr><tr><td rowspan=1 colspan=1>UpdateWR</td><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>Controls an Update operation in the selected wrapper register (WR)</td></tr><tr><td rowspan=1 colspan=1>WSO[31:0]</td><td rowspan=1 colspan=1>Output</td><td rowspan=1 colspan=1>IEEE1500 test port per-channel serial output</td></tr></table>

## 13.2.3 IEEE1500 Test Access Port Functional Description

Figure 111 shows the HBM4 DRAM’s IEEE1500 compliant architecture that uses an asymmetrical WSP (Wrapper Serial Port) with a single WSI and thirty-two per channel WSOs. The standard compliant register stack is shown in the figure, including the Wrapper Bypass Register (WBY), Wrapper Boundary Register (WBR), and Wrapper Data Registers (WDR). The C, S and U notation for the registers refer to Capture, Shift and Update respectively, and indicate for each of the registers which functions are supported by that register. For example, the WBY only provides a Shift stage, whereas the WDRs provide Shift/Capture and Update stages.

## 13.2.3 IEEE1500 Test Access Port Functional Description (cont’d)

![](images/191b5dca699fedf2db0336aa8b1e0f07f46b243d034c185b0250c913d74a889f.jpg)  
Figure 111 — IEEE Std. 1500 Logic Diagram

The WSO[31:0] output drivers are permanently enabled, with their drive state being LOW, HIGH, or undefined based on the current instruction loaded into the WIR. For example, if BYPASS is the current instruction, then WSO output data is defined only after one or more WRCK clock cycles have been applied. A WSO output will drive a LOW when a channel is disabled via the CHANNEL\_DISABLE instruction or marked as “not present / not working” in the DEVICE\_ID WDR.

The Wrapper Instruction Register (WIR) logic is included in Figure 111, and Figure 112 shows further details of the WIR implementation. The WIR and instruction opcodes are described in IEEE1500 Test Access Port Instruction Register clause, and the instructions supported by IEEE1500 Test Instructions. The five channel select bits of the WIR shift stage in Figure 112 are decoded to generate the CHSelect[31:0] outputs which control the per channel operation of the instructions. When a channel is not selected for an active instruction, then the CaptureWDR[31:0], ShiftWDR[31:0] and UpdateWDR[31:0] enables of the WSP are gated off. This will disable the WDRs of unselected channels for the decoded instruction. This gating is shown by the logic AND gates at the output of the de-multiplexer in Figure 111.

![](images/9489fe4469eeca72bac4a4202860d29a75b2a829c5beb3e4afa92e50f5e87b49.jpg)  
Figure 112 — WIR Channel Select Logic Diagram

## 13.2.3 IEEE1500 Test Access Port Functional Description (cont’d)

HBM4 DRAMs are allowed to support less than 32 channels. The availability of each channel is coded in the DEVICE\_ID WDR bits [39:8]. Unavailable channels do not respond to IEEE1500 instructions.

Figure 113 illustrates an IEEE1500 port operation sequence with a minimum number of WRCK cycles:

Signal SelectWIR is set at clock edge T0. Control signals CaptureWR, ShiftWR and UpdateWR are all inactive as they are not allowed to change coincident with SelectWIR. SelectWIR must be kept stable until after completion of the complete sequence which spans until clock edge T4.

<sup></sup> A WDR capture operation is performed at clock edge T1 with CaptureWR sampled High at T1.

<sup></sup> A single WDR shift operation is performed at clock edge T2 with ShiftWR sampled High at T2.

A WDR update operation is performed at clock edge T3b with UpdateWR sampled High at T3b.   
Please note that the update operation occurs on the falling WRCK clock edge.

<sup></sup> For some IEEE1500 port instructions a capture, shift or update event may not be specified; please refer to the description of each instruction for details.

![](images/8ce0739f9dd6de532a55e2e21b98b624f474f536bf141cc0e79115e51706d0b9.jpg)  
Figure 113 — IEEE1500 Port Operation

## 13.3 Wrapper Data Register (WDR) Types

## 13.3.1 Read Only (R) Wrapper Data Registers

WDR bit fields that are specified as read-only capture data into the shift stage register when a CaptureWR event is performed. The read-only WDRs keep their state during an UpdateWR event and do not have an update stage register. Read-only WDRs shift out their content during a ShiftWR event. Data shifted into WSI during the ShiftWR event is ignored.

## 13.3.2 Write Only (W) Wrapper Data Registers

WDR bit fields that are specified as write-only copy all data bits into the update stage register when an UpdateWR event is performed. When a write-only WDR is connected between WSI and WSO, any CaptureWR event has no effect on the WDR. Write-only WDRs shift out their content during the ShiftWR event.

## 13.3.3 Read and Write (R/W) Wrapper Data Registers

R/W WDRs operate as merged function of write-only and read-only WDRs. They capture data bits into the shift stage register during a CaptureWR event and copy bits from the shift stage into the update stage simultaneously when the UpdateWR event is performed.

## 13.3.4 WDR Reset State

Asserting WRST\_n to LOW asynchronously asserts these states on the HBM4 DRAM’s IEEE1500 test port logic:

All WDRs place their update and / or shift stages (where applicable) into a state that ensures that the HBM4 DRAM returns to mission mode operation and all test modes are disabled;

The WIR is set to BYPASS, effectively clearing any prior EXTEST\_RX, EXTEST\_TX, or CHANNEL\_ID instruction, thus returning all functional pins to their normal functional mode. Boundary scan chain content is undefined;

<sup></sup> No change to any previously loaded SOFT\_REPAIR, HARD\_REPAIR, SOFT\_LANE\_REPAIR, or HARD\_LANE\_REPAIR register content;

<sup></sup> The content of the DWORD\_MISR and AWORD\_MISR registers is undefined;

<sup></sup> The AWORD MISR is disabled by setting bit 2 in the AWORD\_MISR\_CONFIG WDR to 0;

The CHANNEL\_DISABLE WDR is reset (refer to the CHANNEL\_DISABLE instruction for conditions to re-enable a disabled channel);

<sup></sup> Any ongoing MBIST operation will be terminated.

## 13.4 IEEE1500 Test Access Port Instruction Encodings

The HBM4 DRAM supports a 14-bit Wrapper Instruction Register (WIR). Bits WIR[13:8] select the channel and bits WIR[7:0] encode the test instruction. When SelectWIR is asserted, the WIR will not respond to the CaptureWR event and nothing will be captured into the WIR.

The WIR channel selection definition applies only to instructions defined in Table 120 (WIR[7:0] = 00<sub>h</sub> to $1 \mathrm { F _ { h } } )$ . The definition does not apply to vendor specific instructions, and vendors may use bits WIR[13:8] for different purposes.

Table 118 — WIR Channel Selection Definition
<table><tr><td rowspan=1 colspan=1>WIR[13:8]</td><td rowspan=1 colspan=1>Channel Select</td><td rowspan=1 colspan=1>WIR[13:8]</td><td rowspan=1 colspan=1>Channel Select</td><td rowspan=1 colspan=1>WIR[13:8]</td><td rowspan=1 colspan=1>Channel Select</td><td rowspan=1 colspan=1>WIR[13:8]</td><td rowspan=1 colspan=1>Channel Select</td></tr><tr><td rowspan=1 colspan=1> $0 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 0</td><td rowspan=1 colspan=1> $0 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 8</td><td rowspan=1 colspan=1> $1 0 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 16</td><td rowspan=1 colspan=1> $1 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 24</td></tr><tr><td rowspan=1 colspan=1> $0 1 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 1</td><td rowspan=1 colspan=1> $0 9 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 9</td><td rowspan=1 colspan=1> $1 1 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 17</td><td rowspan=1 colspan=1> $1 9 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 25</td></tr><tr><td rowspan=1 colspan=1> $0 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 2</td><td rowspan=1 colspan=1> $0 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Channel 10</td><td rowspan=1 colspan=1> $1 2 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 18</td><td rowspan=1 colspan=1> $1 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>Channel 26</td></tr><tr><td rowspan=1 colspan=1> $0 3 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 3</td><td rowspan=1 colspan=1> $0 \mathrm { B _ { h } }$ </td><td rowspan=1 colspan=1>Channel 11</td><td rowspan=1 colspan=1> $1 3 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 19</td><td rowspan=1 colspan=1> $1 \mathrm { B _ { h } }$ </td><td rowspan=1 colspan=1>Channel 27</td></tr><tr><td rowspan=1 colspan=1> $0 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 4</td><td rowspan=1 colspan=1> $0 \mathrm { C _ { h } }$ </td><td rowspan=1 colspan=1>Channel 12</td><td rowspan=1 colspan=1> $1 4 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 20</td><td rowspan=1 colspan=1> $1 \mathrm { C } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 28</td></tr><tr><td rowspan=1 colspan=1> $0 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 5</td><td rowspan=1 colspan=1> $0 \mathrm { D _ { h } }$ </td><td rowspan=1 colspan=1>Channel 13</td><td rowspan=1 colspan=1> $1 5 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 21</td><td rowspan=1 colspan=1> $1 \mathrm { D _ { h } }$ </td><td rowspan=1 colspan=1>Channel 29</td></tr><tr><td rowspan=1 colspan=1> $0 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 6</td><td rowspan=1 colspan=1> $0 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1>Channel 14</td><td rowspan=1 colspan=1> $1 6 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 22</td><td rowspan=1 colspan=1> $1 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1>Channel 30</td></tr><tr><td rowspan=1 colspan=1> $0 7 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 7</td><td rowspan=1 colspan=1> $0 \mathrm { F _ { h } }$ </td><td rowspan=1 colspan=1>Channel 15</td><td rowspan=1 colspan=1> $1 7 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>Channel 23</td><td rowspan=1 colspan=1> $1 \mathrm { F _ { h } }$ </td><td rowspan=1 colspan=1>Channel 31</td></tr></table>

Table 119 — WIR Channel Selection Definition
<table><tr><td rowspan=1 colspan=1>WIR[13:8]</td><td rowspan=1 colspan=1>1            Channel Select</td></tr><tr><td rowspan=1 colspan=1> $3 8 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>16 Channels – 1st group</td></tr><tr><td rowspan=1 colspan=1> $3 9 _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>16 Channels – 2ⁿd group</td></tr><tr><td rowspan=1 colspan=1> $3 \mathrm { A _ { h } }$ </td><td rowspan=1 colspan=1>8 Channels - 1st group</td></tr><tr><td rowspan=1 colspan=1> $3 \mathrm { B _ { h } }$ </td><td rowspan=1 colspan=1>8 Channels - 2nd group</td></tr><tr><td rowspan=1 colspan=1> $3 C _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>8 Channels - 3rd group</td></tr><tr><td rowspan=1 colspan=1> $3 \mathrm { D } _ { \mathrm { h } }$ </td><td rowspan=1 colspan=1>8 Channels - 4th group</td></tr><tr><td rowspan=1 colspan=1> $3 \mathrm { E _ { h } }$ </td><td rowspan=1 colspan=1>Not used. (all channels selected)</td></tr><tr><td rowspan=1 colspan=1> $3 \mathrm { F _ { h } }$ </td><td rowspan=1 colspan=1>All channels - 32 channels</td></tr><tr><td rowspan=1 colspan=1> $\mathrm { X _ { h } }$ </td><td rowspan=1 colspan=1>Ignored(all channels selected)</td></tr><tr><td rowspan=1 colspan=2>NOTE 1 See the vendor datasheets for the mapping of channels for $3 \mathrm { A } _ { \mathrm { h } } ,$ 3Bh, $3 C _ { \mathrm { h } }$ and 3Dh</td></tr></table>

## 13.5 Test Instructions

Test instructions supported by the HBM4 DRAM are listed in Table 120 and subsequently described in detail.

Table 120 — Instruction Register Encodings
<table><tr><td colspan="1" rowspan="1">WIR[13:8]</td><td colspan="1" rowspan="1">WIR[7:0]</td><td colspan="1" rowspan="1">Instruction</td><td colspan="1" rowspan="1">Description</td><td colspan="1" rowspan="1">RegisterType</td><td colspan="1" rowspan="1">WDRLength</td></tr><tr><td colspan="1" rowspan="1"> $\mathrm { X _ { h } }$ </td><td colspan="1" rowspan="1"> $0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">BYPASS</td><td colspan="1" rowspan="1">Bypass</td><td colspan="1" rowspan="1">R/W</td><td colspan="1" rowspan="1">1</td></tr><tr><td colspan="1" rowspan="1"> $3 \mathrm { F _ { h } , }$  $1 \mathrm { F _ { h } } – 0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1"> $0 1 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">EXTEST RX</td><td colspan="1" rowspan="1">Microbump boundary scan Rx test(open/ short)</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">120</td></tr><tr><td colspan="1" rowspan="1"> $3 \mathrm { F _ { h } , }$  $1 \mathrm { F _ { h } } – 0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1"> $0 2 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">EXTEST TX</td><td colspan="1" rowspan="1">Microbump boundary scan Tx test(open/ short)</td><td colspan="1" rowspan="1">W</td><td colspan="1" rowspan="1">120</td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"> $0 3 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">RFU</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"> $0 4 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">RFU</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1"> $\mathrm { X _ { h } }$ </td><td colspan="1" rowspan="1"> $0 5 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">HBM RESET</td><td colspan="1" rowspan="1">Functional reset excluding Wrapper DataRegisters (WDRs) and any IEEE1500test port logic or I/Os</td><td colspan="1" rowspan="1">W</td><td colspan="1" rowspan="1">1</td></tr><tr><td colspan="1" rowspan="1"> $3 \mathrm { F _ { h } , }$  $1 \mathrm { F _ { h } } – 0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1"> $0 6 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">MBIST</td><td colspan="1" rowspan="1">HBM4 DRAM resident Memory BISTengine test           1</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">Vendorspecific</td></tr><tr><td colspan="1" rowspan="1"> $1 \mathrm { F _ { h } } – 0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1"> $0 7 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">SOFT REPAIR</td><td colspan="1" rowspan="1">Soft repair of failing memory array bitcell</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">25</td></tr><tr><td colspan="1" rowspan="1"> $1 \mathrm { F _ { h } } – 0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1"> $0 8 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">HARD REPAIR</td><td colspan="1" rowspan="1">Hard repair of DRAM failing memoryarray bit cell</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">25</td></tr><tr><td colspan="1" rowspan="1"> $3 \mathrm { F _ { h } , }$  $1 \mathrm { F _ { h } } – 0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1"> $0 9 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">DWORD MISR</td><td colspan="1" rowspan="1">Read back for DWORD MISR and writeof a seed value</td><td colspan="1" rowspan="1">R/W</td><td colspan="1" rowspan="1">320</td></tr><tr><td colspan="1" rowspan="1"> $3 \mathrm { F _ { h } , }$  $1 \mathrm { F _ { h } } \mathrm { - } 0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1"> $0 \mathrm { A _ { h } }$ </td><td colspan="1" rowspan="1">AWORD MISRS7</td><td colspan="1" rowspan="1">Read back for AWORD MISR</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">38</td></tr><tr><td colspan="1" rowspan="1"> $3 \mathrm { F _ { h } , }$  $1 \mathrm { F _ { h } } – 0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1"> $0 \mathrm { B _ { h } }$ </td><td colspan="1" rowspan="1">CHANNEL ID</td><td colspan="1" rowspan="1">All TX I/Os go HIGH(except I/Os in MIDSTACK region)</td><td colspan="1" rowspan="1">W</td><td colspan="1" rowspan="1">1</td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"> $0 \mathrm { C _ { h } }$ </td><td colspan="1" rowspan="1">RFU</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1"> $3 \mathrm { F _ { h } , }$  $1 \mathrm { F _ { h } } – 0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1"> $0 \mathrm { D _ { h } }$ </td><td colspan="1" rowspan="1">AWORD MISRCONFIG</td><td colspan="1" rowspan="1">Allows IEEE1500 test port access toconfigure the AWORD MISR testfeature</td><td colspan="1" rowspan="1">W</td><td colspan="1" rowspan="1">8</td></tr><tr><td colspan="1" rowspan="1"> $3 \mathrm { F _ { h } , }$  $1 \mathrm { F _ { h } } – 0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1"> $0 \mathrm { E _ { h } }$ </td><td colspan="1" rowspan="1">DEVICE_ID</td><td colspan="1" rowspan="1">Returns the HBM4 DRAM's uniqueidentification code</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">182</td></tr><tr><td colspan="1" rowspan="1"> $\mathrm { X _ { h } }$ </td><td colspan="1" rowspan="1"> $0 \mathrm { F _ { h } }$ </td><td colspan="1" rowspan="1">TEMPERATURE</td><td colspan="1" rowspan="1">Returns a 9-bit binary temperature code</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">9</td></tr><tr><td colspan="1" rowspan="1"> $3 \mathrm { F _ { h } , }$  $1 \mathrm { F _ { h } } – 0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1"> $1 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">MODE REGISTERDUMP_SET</td><td colspan="1" rowspan="1">Returns and set the HBM4 DRAM'sMode Register values</td><td colspan="1" rowspan="1">R/W</td><td colspan="1" rowspan="1">1607</td></tr><tr><td colspan="1" rowspan="1"> $3 \mathrm { F _ { h } , }$  $1 \mathrm { F _ { h } } – 0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1"> $1 1 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">READ LFSRCOMPARE STICKY</td><td colspan="1" rowspan="1">Reads the sticky bit error forLFSR Compare feature</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">99</td></tr><tr><td colspan="1" rowspan="1"> $1 \mathrm { F _ { h } } \mathrm { - } 0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1"> $1 2 \mathrm { { h } }$ </td><td colspan="1" rowspan="1">SOFT_LANE_REPAIR</td><td colspan="1" rowspan="1">Soft Lane Remapping</td><td colspan="1" rowspan="1">R/W</td><td colspan="1" rowspan="1">40 or 458</td></tr><tr><td colspan="1" rowspan="1"> $1 \mathrm { F _ { h } } – 0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1"> $1 3 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">HARD LANE REPAIR</td><td colspan="1" rowspan="1">Hard Lane Remapping</td><td colspan="1" rowspan="1">R/W</td><td colspan="1" rowspan="1">40 or 458</td></tr><tr><td colspan="1" rowspan="1"> $3 \mathrm { F _ { h } , }$  $\underline { { 1 \mathrm { F _ { h } } . 0 0 _ { h } } }$ </td><td colspan="1" rowspan="1"> $1 4 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">CHANNEL DISABLE</td><td colspan="1" rowspan="1">Disables a channel(All-channel disable is optional)</td><td colspan="1" rowspan="1">W</td><td colspan="1" rowspan="1">1</td></tr><tr><td colspan="1" rowspan="1"> $3 \mathrm { F _ { h } , }$  $1 \mathrm { F _ { h } } – 0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1"> $1 5 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">CHANNELTEMPERATURE</td><td colspan="1" rowspan="1">Returns a 9-bit binary channeltemperature code per SID</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">36</td></tr><tr><td colspan="1" rowspan="1"> $\mathrm { X _ { h } }$ </td><td colspan="1" rowspan="1"> $1 6 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">WOSC RUN</td><td colspan="1" rowspan="1">WDQS Interval Oscillator</td><td colspan="1" rowspan="1">W</td><td colspan="1" rowspan="1">1</td></tr><tr><td colspan="1" rowspan="1"> $\mathrm { X _ { h } }$ </td><td colspan="1" rowspan="1"> $1 7 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">WOSC COUNT</td><td colspan="1" rowspan="1">WDQS Interval Oscillator Count</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">25</td></tr><tr><td colspan="1" rowspan="1"> $1 \mathrm { F _ { h } } – 0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1"> $1 8 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">ECS ERROR LOG</td><td colspan="1" rowspan="1">Error Check and Scrub (ECS) ErrorLog Information</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">216</td></tr><tr><td colspan="1" rowspan="1"> $1 \mathrm { F _ { h } } – 0 0 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1"> $1 9 _ { \mathrm { h } }$ </td><td colspan="1" rowspan="1">HS REP CAP</td><td colspan="1" rowspan="1">Returns whether banks have repairresources or not</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">256</td></tr><tr><td colspan="1" rowspan="1"> $3 8 _ { \mathrm { h } } , 3 9 _ { \mathrm { h } } , ^ { 4 }$  $3 \mathrm { A } _ { \mathrm { h } ^ { - 3 } } \mathrm { D } _ { \mathrm { h } } ^ { 5 }$ </td><td colspan="1" rowspan="1"> $1 \mathrm { A _ { h } }$ </td><td colspan="1" rowspan="1">SELF REP</td><td colspan="1" rowspan="1">Self repair</td><td colspan="1" rowspan="1">R/W</td><td colspan="1" rowspan="1">9</td></tr><tr><td colspan="1" rowspan="1"> $3 8 _ { \mathrm { h } } , 3 9 _ { \mathrm { h } } , ^ { 4 }$  $3 \mathrm { A } _ { \mathrm { h } ^ { - 3 } } \mathrm { D } _ { \mathrm { h } } ^ { 5 }$ </td><td colspan="1" rowspan="1"> $1 \mathrm { B _ { h } }$ </td><td colspan="1" rowspan="1">SELF REP RESULTS</td><td colspan="1" rowspan="1">Self repair results</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">8</td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"> $1 \mathrm { C } _ { \mathrm { h } ^ { - } }$  $3 \mathrm { F _ { h } }$ </td><td colspan="1" rowspan="1">RFU</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">Vendorspecific</td><td colspan="1" rowspan="1"> $4 0 _ { \mathrm { h } ^ { - } }$  $\mathrm { F F _ { h } }$ </td><td colspan="1" rowspan="1">Vendor specific</td><td colspan="1" rowspan="1">V</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="6" rowspan="1">NOTE 1 Unsupported instruction codes will default to the BYPASSinstruction when the WIR is updated with theunsupported encodingNOTE 2 Channels that are not selected by WIR[13:8] do not respond to the instruction and ignore any Update, Captureand Shift events.NOTE 3 WDRs shift out the least significant bit on the WSO port at the first WRCK of the shift sequence. WSO outputtiming and valid data window are defined in Table 146 (IEEE1500 Test Port AC Timings).NOTE 4 WIR[13:8] value of $3 8 _ { \mathrm { h } }$ or $3 9 _ { \mathrm { h } }$ is for enabling self repair or self repair results on groups of 16 channels. Thechannels associated with 38h and $3 9 _ { \mathrm { h } }$ are vendor specific.NOTE 5 WIR[13:8] value of $3 \mathrm { A _ { h } } , 3 \mathrm { B _ { h } } , 3 \mathrm { C _ { h } } ,$ and $3 \mathrm { D } _ { \mathrm { h } }$ is for enabling self repair or self repair results on groups of 8channels. The channels associated with $3 \mathrm { A h } , 3 \mathrm { B h } , 3 \mathrm { C _ { h } } ,$ and $3 \mathrm { D } _ { \mathrm { h } }$ are vendor specificNOTE 6 Global test instructions $( \mathrm { W I R } [ 1 3 { : } 8 ] = \mathrm { X } _ { \mathrm { h } } )$ drive the same data on the WSO outputs of all active channels duringShiftWR events. Inactive channels (channels that are marked as “not present / not working" in the DEVICE_IDWDR and channels that have been disabled using the CHANNEL_DISABLE instruction) drive a static LOWon their WSO outputs.NOTE 7 The maximum WDR length for MODE_REGISTER_DUMP_SET is 160 bits but is vendor specific and willdepend on whether MR16-MR19 are supported, which is indicated by the EXTENDED_MR field of theDEVICE_ID WDR (see Table 132) Refer to supplier datasheet for more information.NOTE 8Channels 1 and 17 WDR length is 45, while the WDR length for Channels 0, 2 through 15 and 16, 18 through31 is 40.</td></tr></table>

## 13.5.1 BYPASS

The BYPASS instruction places a single bit WDR between WSI and each channel’s WSO and RM. Data is shifted from WSI to WSO and RM through the one bit WDR by WRCK.

BYPASS is the default instruction after asserting WRST\_n to LOW.

## Wrapper Data Register

When BYPASS is the current instruction, the 1-bit shift register as shown in Table 121 is connected between WSI, RM[1:0], and WSO[31:0], and the WSO and RM outputs of all active channels drive the same data during ShiftWR events.

## CaptureWR

When BYPASS is the current instruction, the CaptureWR event will have no effect.

## UpdateWR

When BYPASS is the current instruction, the UpdateWR event will have no effect.

Table 121 — BYPASS Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>BYPASS</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Single bit bypass shift register per IEEE1500 Standard</td></tr></table>

## 13.5.2 EXTEST\_RX and EXTEST\_TX

EXTEST\_RX and EXTEST\_TX are both intended for DC I/O connectivity testing similar to board level boundary scan. The receive notation in EXTEST\_RX designates that the HBM4 I/O will sample the logic value and capture into the data register the value that is present at the micro bump interface. The transmit notation in EXTEST\_TX designates that the HBM4 I/O will drive the logic value shifted into the data register at the micro bump interface. All HBM4 bidirectional I/O, inputs and outputs support both instructions. Differential inputs and outputs (CK\_t/CK\_c, WDQS\_t/WDQS\_c and RDQS\_t/RDQS\_c) also support both instructions on both the true and complement pins.

While EXTEST\_RX is the current instruction, all functional pins of the selected channel(s) enter a High-Z state, including the output-only pins AERR, DERR, RDQS\_t/RDQS\_c. See also the Boundary Scan section.

I/O signals power up in input mode by default. The host will put all AWORD and DWORD drivers into High-Z state prior to loading the EXTEST\_TX instruction into the WIR. As soon as EXTEST\_TX becomes the current instruction, all AWORD and DWORD signals will change to output mode and remain in output mode until reset of the test logic or until a different instruction is updated on the channel.

A channel disabled either via the corresponding CHANNEL\_AVAILABLE bit in the DEVICE ID WDR or via the CHANNEL\_DISABLE instruction will not respond to the EXTEST\_TX or EXTEST\_RX instructions.

## Wrapper Data Register

When EXTEST\_RX or EXTEST\_TX is the current instruction, the Wrapper Boundary Register (WBR) as shown in Table 122 is connected between WSI and WSO.

## CaptureWR

When EXTEST\_RX is the current instruction, the CaptureWR event will capture the input values into the shift stage of the WDR. The captured data is shifted out on WSO during a subsequent ShiftWR event. Inputs must be stable for the setup and hold times t<sub>SEXT</sub> and t<sub>HEXT</sub>.

When EXTEST\_TX is the current instruction, the CaptureWR event will have no effect.

## ShiftWR

The Wrapper Boundary Register (WBR) does not provide an update stage. When EXTEST\_TX is the current instruction, the value driven on the outputs is directly derived from the WDR’s shift stage and will update with each ShiftWR event. The new data will be stable after t<sub>OVEXT</sub> time.

## UpdateWR

When EXTEST\_RX or EXTEST\_TX is the current instruction, the UpdateWR event will have no effect.

## 13.5.2 EXTEST\_RX and EXTEST\_TX (cont’d)

Table 122 — Wrapper Boundary Register (WBR)
<table><tr><td colspan="1" rowspan="1">BitPosition</td><td colspan="1" rowspan="1">Bit Field</td><td colspan="1" rowspan="1">Type</td><td colspan="5" rowspan="1">Description</td></tr><tr><td colspan="1" rowspan="1">119</td><td colspan="1" rowspan="1">DBI7</td><td colspan="1" rowspan="1">I/O</td><td colspan="5" rowspan="34">DWORD1 (PC1)Yobal</td></tr><tr><td colspan="1" rowspan="1">118</td><td colspan="1" rowspan="1">DQ63</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">117</td><td colspan="1" rowspan="1">DQ62</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">116</td><td colspan="1" rowspan="1">DQ61</td><td colspan="1" rowspan="1">I/O</td><td colspan="4" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">115</td><td colspan="1" rowspan="1">DQ60</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">114</td><td colspan="1" rowspan="1">RD3</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">113</td><td colspan="1" rowspan="1">DERR1</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">112</td><td colspan="1" rowspan="1">DQ59</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">111</td><td colspan="1" rowspan="1">DQ58</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">110</td><td colspan="1" rowspan="1">DQ57</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">109</td><td colspan="1" rowspan="1">DQ56</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">108</td><td colspan="1" rowspan="1">SEV3</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">107</td><td colspan="1" rowspan="1">DBI6</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">106</td><td colspan="1" rowspan="1">DQ55</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">105</td><td colspan="1" rowspan="1">DQ54</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">104</td><td colspan="1" rowspan="1">DQ53</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">103</td><td colspan="1" rowspan="1">DQ52</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">102</td><td colspan="1" rowspan="1">RDQS1_c</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">101</td><td colspan="1" rowspan="1">RDQS1_t</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">100</td><td colspan="1" rowspan="1">DQ51</td><td colspan="5" rowspan="1">1/O</td></tr><tr><td colspan="1" rowspan="1">99</td><td colspan="1" rowspan="1">DQ50</td><td colspan="5" rowspan="1">01O</td></tr><tr><td colspan="1" rowspan="1">98</td><td colspan="1" rowspan="1">DQ49</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">97</td><td colspan="1" rowspan="1">DQ48</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">96</td><td colspan="1" rowspan="1">SEV2</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">95</td><td colspan="1" rowspan="1">DBI5</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">94</td><td colspan="1" rowspan="1">DQ47</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">93</td><td colspan="1" rowspan="1">DQ46</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">92</td><td colspan="1" rowspan="1">DQ45</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">91</td><td colspan="1" rowspan="1">DQ44</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">90</td><td colspan="1" rowspan="1">WDQS1_c</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">89</td><td colspan="1" rowspan="1">WDQS1_t</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">88</td><td colspan="1" rowspan="1">DQ43</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">87</td><td colspan="1" rowspan="1">DQ42</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">86</td><td colspan="1" rowspan="1">DQ41</td><td colspan="5" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">85</td><td colspan="1" rowspan="1">DQ40</td><td colspan="1" rowspan="1">I/O</td><td colspan="1" rowspan="14">DWORD1 (PC1) (cont'd)</td></tr><tr><td colspan="1" rowspan="1">84</td><td colspan="1" rowspan="1">ECC3</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">83</td><td colspan="1" rowspan="1">DBI4</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">82</td><td colspan="1" rowspan="1">DQ39</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">81</td><td colspan="1" rowspan="1">DQ38</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">80</td><td colspan="1" rowspan="1">DQ37</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">79</td><td colspan="1" rowspan="1">DQ36</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">78</td><td colspan="1" rowspan="1">RD2</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">77</td><td colspan="1" rowspan="1">DPAR1</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">76</td><td colspan="1" rowspan="1">DQ35</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">75</td><td colspan="1" rowspan="1">DQ34</td><td colspan="1" rowspan="1">I/O</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">74</td><td colspan="1" rowspan="1">DQ33</td><td colspan="1" rowspan="1">I/O</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">73</td><td colspan="1" rowspan="1">DQ32</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">72</td><td colspan="1" rowspan="1">ECC2</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">71</td><td colspan="1" rowspan="1">AERR</td><td colspan="1" rowspan="1">I/O</td><td colspan="1" rowspan="25">AWORDYobal</td></tr><tr><td colspan="1" rowspan="1">70</td><td colspan="1" rowspan="1">R9</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">69</td><td colspan="1" rowspan="1">R8</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">68</td><td colspan="1" rowspan="1">R7</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">67</td><td colspan="1" rowspan="1">R6</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">66</td><td colspan="1" rowspan="1">CK_c</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">65</td><td colspan="1" rowspan="1">R5</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">64</td><td colspan="1" rowspan="1">R4</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">63</td><td colspan="1" rowspan="1">R0</td><td colspan="1" rowspan="1">1/O</td></tr><tr><td colspan="1" rowspan="1">62</td><td colspan="1" rowspan="1">R3</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">61</td><td colspan="1" rowspan="1">SR2</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">60</td><td colspan="1" rowspan="1">R1</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">59</td><td colspan="1" rowspan="1">RA</td><td colspan="1" rowspan="1">I/O</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">58</td><td colspan="1" rowspan="1">ARFU</td><td colspan="1" rowspan="1">I/O</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="2">57</td><td colspan="1" rowspan="2">APAR</td><td colspan="1" rowspan="2">I/O</td><td colspan="1" rowspan="2"></td></tr><tr><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">56</td><td colspan="1" rowspan="1">C7</td><td colspan="1" rowspan="1">I/O</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">55</td><td colspan="1" rowspan="1">C6</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">54</td><td colspan="1" rowspan="1">C5</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">53</td><td colspan="1" rowspan="1">CK_t</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">52</td><td colspan="1" rowspan="1">C4</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">51</td><td colspan="1" rowspan="1">C3</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">50</td><td colspan="1" rowspan="1">C2</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">49</td><td colspan="1" rowspan="1">C1</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">48</td><td colspan="1" rowspan="1">C0</td><td colspan="1" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">47</td><td colspan="1" rowspan="1">DBI3</td><td colspan="1" rowspan="1">I/O</td><td colspan="3" rowspan="39">DWORD0 (PC0)Yobal</td></tr><tr><td colspan="1" rowspan="1">46</td><td colspan="1" rowspan="1">DQ31</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">45</td><td colspan="1" rowspan="1">DQ30</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">44</td><td colspan="1" rowspan="1">DQ29</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">43</td><td colspan="1" rowspan="1">DQ28</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">42</td><td colspan="1" rowspan="1">RD1</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">41</td><td colspan="1" rowspan="1">DERR0</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">40</td><td colspan="1" rowspan="1">DQ27</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">39</td><td colspan="1" rowspan="1">DQ26</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">38</td><td colspan="1" rowspan="1">DQ25</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">37</td><td colspan="1" rowspan="1">DQ24</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">36</td><td colspan="1" rowspan="1">SEV1</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">35</td><td colspan="1" rowspan="1">DBI2</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">34</td><td colspan="1" rowspan="1">DQ23</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">33</td><td colspan="1" rowspan="1">DQ22</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">32</td><td colspan="1" rowspan="1">DQ21</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">31</td><td colspan="1" rowspan="1">DQ20</td><td colspan="1" rowspan="1">I/O</td><td colspan="2" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">30</td><td colspan="1" rowspan="1">RDQS0_c</td><td colspan="1" rowspan="1">I/O</td><td colspan="2" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">29</td><td colspan="1" rowspan="1">RDQS0_t</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">28</td><td colspan="1" rowspan="1">DQ19</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">27</td><td colspan="1" rowspan="1">DQ18</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">26</td><td colspan="1" rowspan="1">DQ17</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">25</td><td colspan="1" rowspan="1">DQ16</td><td colspan="1" rowspan="1">0I/O</td><td colspan="2" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">24</td><td colspan="1" rowspan="1">SEV0</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">23</td><td colspan="1" rowspan="1">DBI1</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">22</td><td colspan="1" rowspan="1">DQ15</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">21</td><td colspan="1" rowspan="1">DQ14</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">DQ13</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">19</td><td colspan="1" rowspan="1">DQ12</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">18</td><td colspan="1" rowspan="1">WDQS0_c</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">17</td><td colspan="1" rowspan="1">WDQS0_t</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">16</td><td colspan="1" rowspan="1">DQ11</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">15</td><td colspan="1" rowspan="1">DQ10</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">14</td><td colspan="1" rowspan="1">DQ9</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">13</td><td colspan="1" rowspan="1">DQ8</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">12</td><td colspan="1" rowspan="1">ECC1</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">11</td><td colspan="1" rowspan="1">DBI0</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1">DQ7</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">DQ6</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">8</td><td colspan="1" rowspan="1">DQ5</td><td colspan="1" rowspan="1">I/O</td><td colspan="3" rowspan="9">DWORD0 (PC0) (cont'd)</td></tr><tr><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">DQ4</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">RD0</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">DPAR0</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">DQ3</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">DQ2</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">DQ1</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">DQ0</td><td colspan="3" rowspan="1">I/O</td></tr><tr><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">ECCO</td><td colspan="3" rowspan="1">I/O</td></tr></table>

## 13.5.3 HBM\_RESET

The HBM\_RESET instruction initiates an asynchronous functional reset of the HBM4 DRAM, equivalent to asserting RESET\_n to LOW.

The HBM\_RESET condition is not self-clearing. Instead, the reset state must explicitly be set and cleared. To accomplish an HBM4 reset, the HBM\_RESET bit must be held as 1 for a minimum duration of t<sub>RES</sub> which equals t<sub>PW\_RESET</sub> (see Initialization Sequence with Stable Power).

It is pointed out that the Wrapper Serial Port (WSP) itself including the associated control logic and WDRs is not reset by the HBM\_RESET instruction. The DA port signal pins are also not affected by the HBM\_RESET instruction.

## Wrapper Data Register

When HBM\_RESET is the current instruction, the data register as shown in Table 123 is connected between WSI and WSO[31:0], and the WSO outputs of all active channels drive the same data during ShiftWR events.

## CaptureWR

When HBM\_RESET is the current instruction, the CaptureWR event will have no effect.

## UpdateWR

When HBM\_RESET is the current instruction, the UpdateWR event will load the value from the shift stage into the update stage and initiate or clear the functional reset.

Table 123 — HBM\_RESET Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>HBM RESET</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>0 - Clear the functional reset1 - Initiate the functional reset</td></tr></table>

Internally, the RESET\_n pin and the HBM\_RESET instruction are logically combined such that when either is true then the internal reset state is true. During power-up it is required that WRST\_n be driven LOW, thus ensuring that the uninitialized IEEE1500 test port logic does not interfere with the power-up initialization sequence.

![](images/f4c2dc253c86cfa8870217403d3f37233210e8c2cc3fd566e128213a3ca5f499.jpg)  
Figure 114 — RESET\_n and HBM\_RESET Logic

## 13.5.3 HBM4\_RESET (cont’d)

After the power-up initialization, the RESET\_n input is HIGH, and subsequent stable power resets may be asserted by either driving the RESET\_n input LOW, or by using the HBM\_RESET instruction. Note that the HBM\_RESET instruction does not bring the HBM4 DRAM out of reset while the external RESET\_n input is driven LOW. Similarly, the HBM4 DRAM cannot be brought out of reset using the RESET\_n input while reset is asserted using the HBM\_RESET instruction.

Table 124 — RESET\_n and HBM\_RESET Truth Table
<table><tr><td rowspan=1 colspan=1>RESET_n</td><td rowspan=1 colspan=1>HBM_RESET</td><td rowspan=1 colspan=1>Internal Reset State</td></tr><tr><td rowspan=1 colspan=1>LOW</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Reset asserted by RESET_n</td></tr><tr><td rowspan=1 colspan=1>LOW</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Reset asserted by both RESET_n pin and HBM_RESET instruction</td></tr><tr><td rowspan=1 colspan=1>HIGH</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Exit reset state</td></tr><tr><td rowspan=1 colspan=1>HIGH</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Reset asserted by HBM_RESET instruction</td></tr></table>

## 13.5.4 MBIST

The MBIST instruction is used for HBM4 DRAM hosted memory built in self-test. HBM devices must support memory MBIST. This instruction format and data register field configuration is required for IEEE Std 1500 access to the test feature. MBIST engine clock source can be WRCK as a direct clock source or reference clock source or an internal clocked mode independent of WRCK and independent of any I/O functional clocks is also acceptable.

## Wrapper Data Register

When MBIST is the current instruction, the vendor specific data register as shown in Table 125 is connected between WSI and WSO.

## CaptureWR

When MBIST is the current instruction, the CaptureWR event will capture R or R/W bit fields into the shift stage of the WDR.

## UpdateWR

When MBIST is the current instruction, the UpdateWR event will load the W and R/W bit fields from the shift stage to the update stage of the WDR simultaneously.

Table 125 — MBIST Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>Vendorspecific</td><td rowspan=1 colspan=1>Vendor specific</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Vendor specific</td></tr></table>

## 13.5.5 SOFT\_REPAIR

The SOFT\_REPAIR instruction allows the user to temporarily repair bit cells in the HBM4 DRAM without using permanent fusing mechanism to initiate the repair. This feature is intended to enable validation that the intended repair works as expected. Once a soft repair is validated, the user may choose to perform a fused hard repair via the HARD\_REPAIR instruction. If DRAM power is removed or the DRAM is RESET, the SOFT\_REPAIR will revert to the un-repaired state.

Repair resources (redundant rows) are provided per PC and per bank. The actual number of repair resources are vendor specific. The number and availability of repair resources are provided via the HS\_REP\_CAP instruction. The use of SOFT\_REPAIR will not decrement the HS\_REP\_CAP register so the host controller must track the resources used. If there is no repair resource available in a certain bank then the host controller should not issue a SOFT\_REPAIR to that bank. However, if a SOFT\_REPAIR sequence is issued to a bank with no repair resource available, the DRAM will ignore the programming sequence.

The SOFT\_REPAIR granularity indicating the number of repaired rows per SOFT\_REPAIR is vendor specific. The address bits associated with the granularity are also vendor specific and indicated in the PPR\_RA[13:0] field of the DEVICE\_ID WDR. See Table 132 for more details.

The SOFT\_REPAIR supports an Undo and Lock function. The SOFT\_REPAIR Undo will restore a previously used repair resource back to its unused state and the same time reactivate the original (unrepaired) row instead. The complete address information comprising the PC, SID, bank and row address must be provided with the SOFT\_REPAIR instruction as described in Table 126, and the SOFT\_REPAIR\_UNDO and SOFT\_REPAIR\_START fields must set to “1”.

The host controller can lock down a used soft repair resource by issuing the SOFT\_REPAIR instruction with the SOFT\_REPAIR\_LOCK and SOFT\_REPAIR\_START bits as “1”. Each SOFT\_REPAIR resource supports the Lock feature. For both UNDO/LOCK cases, the HBM4 DRAM may ignore the row address bit if it so chooses, as the SID, PC, BK are enough to uniquely identify the SOFT\_REPAIR resource. The row address may be ignored if there is only single repair resource. If a host issues a SOFT\_REPAIR on an already repaired but unlocked row then HBM4 DRAM will allocate another repair resource in response to a host request if an available resource exists. Support for the feature is vendor specific. A locked repair resource cannot be used to replace another row or being set back to the unused state using the Undo function. Only a chip reset (RESET\_n pulled LOW) or power-cycling can unlock a locked repair resource.

When using soft repair specifically with the Undo function, the host controller must manage and schedule the refresh operation properly on the valid data of a row address. If a row has been repaired, all refresh commands will exclude the original row from being refreshed and refresh the repair row instead. Similarly, unused repair resources will not be refreshed which includes those resources that had been allocated but were then set back to the unused state using the Undo operation. Especially when switching back and forth between an original and a repair row, regular refresh commands may not hit both rows within the required refresh interval. A possible method to prevent a potential data loss is to explicitly issue ACTIVATE and PRECHARGE commands to the mapped-out rows before and after the SOFT\_REPAIR operations.

The SOFT\_REPAIR UNDO and LOCK are mutually exclusive. So, in the case of any SOFT\_REPAIR instruction issued, the SOFT\_REPAIR UNDO and LOCK must not be set “1” at the same time.

A channel must be in bank idle state, as long as the SOFT\_REPAIR instruction is loaded in the WIR.

## 13.5.5 SOFT\_REPAIR (cont’d)

## Wrapper Data Register

When the SOFT\_REPAIR instruction is updated the data register as shown in Table 126 is connected between WSI and WSO.

## CaptureWR

When SOFT\_REPAIR is the current instruction, the CaptureWR event will have no effect.

## UpdateWR

When SOFT\_REPAIR is the current instruction, the UpdateWR event will load the write only bit field from the shift stage into the update stage simultaneously. Completion of the update event will initiate the soft repair sequence.

Table 126 — SOFT\_REPAIR Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>[24]</td><td rowspan=1 colspan=1>SOFT REPAIR LOCK</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1> $0 _ { \mathsf { b } } - { \mathsf { S O F T } }$ REPAIR is open1b − SOFT REPAIR is hard-locked</td></tr><tr><td rowspan=1 colspan=1>[23]</td><td rowspan=1 colspan=1>SOFT REPAIR UNDO</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>0b − Do SOFT REPAIR (SOFT REPAIR enabled)1b − Undo SOFT_REPAIR (SOFT_REPAIR not enabled)</td></tr><tr><td rowspan=1 colspan=1>[22]</td><td rowspan=1 colspan=1>SOFT_PC</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>PC</td></tr><tr><td rowspan=1 colspan=1>[21:20]</td><td rowspan=1 colspan=1>SOFT_SID</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>SID[1:0]</td></tr><tr><td rowspan=1 colspan=1>[19:16]</td><td rowspan=1 colspan=1>SOFT_BK</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>BA[3:0]</td></tr><tr><td rowspan=1 colspan=1>[15:1]</td><td rowspan=1 colspan=1>SOFT ROW</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>RFU, RA[13:0]1</td></tr><tr><td rowspan=1 colspan=1>[0]</td><td rowspan=1 colspan=1>SOFT REPAIR START</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>Ob − Disabled (Default)1b− Enabled</td></tr><tr><td rowspan=1 colspan=4>NOTE 1 SOFT_ROW includes an additional bit to support future row addressing, i.e., RA14.</td></tr></table>

## 13.5.6 HARD\_REPAIR

The HARD\_REPAIR instruction is used to permanently repair failing bit cells detected in the HBM4 DRAM. A fuse rupture scheme is used to implement the repair. The repair sequence will be initiated on update of the data register. After some vendor specified time period fuse rupture automatically completes and repair is affected. Hard repair will be permanent. Completion of HARD\_REPAIR requires a subsequent chip reset (RESET\_n pulled LOW) as described in Interaction with Mission Mode Operation. The HBM vendor is required to specify the time to wait after updating the HARD\_REPAIR WDR as well as any requirements for WRCK clocking if required to perform the repair.

All channels of the HBM4 DRAM must be in bank idle state as long as the HARD\_REPAIR instruction is loaded in the WIR.

## Wrapper Data Register

When HARD\_REPAIR is the current instruction, the data register as shown in Table 127 is connected between WSI and WSO.

## CaptureWR

When HARD\_REPAIR is the current instruction, the CaptureWR event will have no effect.

## UpdateWR

When HARD\_REPAIR is the current instruction, the UpdateWR event will load the write-only bit fields from the shift stage into the update stage and initiate the hard repair sequence. The hard repair is completed after a waiting time of t<sub>HREP</sub>.

Table 127 — HARD\_REPAIR Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>[24:23]</td><td rowspan=1 colspan=3>RESERVED</td></tr><tr><td rowspan=1 colspan=1>[22]</td><td rowspan=1 colspan=1>HARD_PC</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>PC</td></tr><tr><td rowspan=1 colspan=1>[21:20]</td><td rowspan=1 colspan=1>HARD_SID</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>SID[1:0]</td></tr><tr><td rowspan=1 colspan=1>[19:16]</td><td rowspan=1 colspan=1>HARD_BK</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>BA[3:0]</td></tr><tr><td rowspan=1 colspan=1>[15:1]</td><td rowspan=1 colspan=1>HARD_ROW</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>RFU, RA[13:0]1</td></tr><tr><td rowspan=1 colspan=1>[0]</td><td rowspan=1 colspan=1>HARD_REPAIR_START</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>Ob: Disabled (default)1b: Enabled</td></tr><tr><td rowspan=1 colspan=4>NOTE 1 HARD_ROW includes an additional bit to support future row addressing, i.e., RA14.</td></tr></table>

## 13.5.7 DWORD\_MISR

This instruction captures and shifts out the DWORD MISR value on the WSO output. The instruction may also be used to preload data for use in LFSR mode. The DWORD MISR is associated with the DWORD IO test feature.

Note that the MISR content is not specified after shifting out the MISR content. The host should reinitialize the MISR before continuing with additional testing, e.g., by using the MISR Preset function in Mode Register 7 (Table 17). See clause HBM4 Loopback Test Modes features and usage.

## Wrapper Data Register

When DWORD\_MISR is the current instruction, the data register as shown in Table 128 is connected between WSI and WSO. The notation is "…\_Q0" to "…\_Q3" for the 4 UI per CK clock cycle latched by WDQS in MISR mode or driven along with RDQS in LFSR mode.

## CaptureWR

When DWORD\_MISR is the current instruction, the CaptureWR event will load the respective MISR values into the shift stage of the WDR. A minimum waiting time of tSMISR between the last data capture into the DWORD MISR and this CaptureWR event must be observed.

## UpdateWR

When DWORD\_MISR is the current instruction, the UpdateWR event will load the bits from the shift stage of the WDR into the DWORD MISR.

Table 128 — DWORD\_MISR Wrapper Data Register
<table><tr><td colspan="1" rowspan="1">BitPosition</td><td colspan="1" rowspan="1">Bit Field</td><td colspan="1" rowspan="1">Type</td><td colspan="1" rowspan="1">Description</td></tr><tr><td colspan="1" rowspan="1">[319:160]</td><td colspan="1" rowspan="1">DWORD1</td><td colspan="1" rowspan="1">R/W</td><td colspan="1" rowspan="1">DWORD1: DQ[63:32], DBI[7:4], ECC[3:2] and SEV[3:2](Same bit ordering as DWORD0)</td></tr><tr><td colspan="1" rowspan="1">[159:120]</td><td colspan="1" rowspan="1">DWORD0 BYTE3</td><td colspan="1" rowspan="1">R/W</td><td colspan="1" rowspan="1">Byte 3 of DWORD0: DQ[31:24], DBI3 and SEV1(Same ordering as Byte 0)</td></tr><tr><td colspan="1" rowspan="1">[119:80]</td><td colspan="1" rowspan="1">DWORD0 BYTE2</td><td colspan="1" rowspan="1">R/W</td><td colspan="1" rowspan="1">Byte 2 of DWORD0: DQ[23:16], DBI2 and SEV0(Same ordering as Byte 0)</td></tr><tr><td colspan="1" rowspan="1">[79:40]</td><td colspan="1" rowspan="1">DWORD0 BYTE1</td><td colspan="1" rowspan="1">R/W</td><td colspan="1" rowspan="1">Byte 1 of DWORD0: DQ[15:8], DBI1 and ECC1(Same ordering as Byte 0)</td></tr><tr><td colspan="1" rowspan="1">[39]</td><td colspan="1" rowspan="1">DWORD0_DBI0_Q0</td><td colspan="1" rowspan="1">R/W</td><td colspan="1" rowspan="7">Byte 0 of DWORD0</td></tr><tr><td colspan="1" rowspan="1">[38]</td><td colspan="1" rowspan="1">DWORD0 DBI0 Q1</td><td colspan="1" rowspan="1">R/W</td></tr><tr><td colspan="1" rowspan="1">[37]</td><td colspan="1" rowspan="1">DWORD0_DBI0_Q2</td><td colspan="1" rowspan="1">R/W</td></tr><tr><td colspan="1" rowspan="1">[36]</td><td colspan="1" rowspan="1">DWORD0_DBI0_Q3</td><td colspan="1" rowspan="1">R/W</td></tr><tr><td colspan="1" rowspan="1">[35]</td><td colspan="1" rowspan="1">DWORD0_DQ7_Q0</td><td colspan="1" rowspan="1">R/W</td></tr><tr><td colspan="1" rowspan="1">[34]</td><td colspan="1" rowspan="1">DWORD0_DQ7_Q1</td><td colspan="1" rowspan="1">R/W</td></tr><tr><td colspan="1" rowspan="1">[33]</td><td colspan="1" rowspan="1">DWORD0_DQ7_Q2</td><td colspan="1" rowspan="1">R/W</td></tr><tr><td colspan="1" rowspan="1">[32]</td><td colspan="1" rowspan="1">DWORD0_DQ7_Q3</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[31]</td><td colspan="1" rowspan="1">DWORD0_DQ6_Q0</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[30]</td><td colspan="1" rowspan="1">DWORD0_DQ6_Q1</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[29]</td><td colspan="1" rowspan="1">DWORD0_DQ6_Q2</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[28]</td><td colspan="1" rowspan="1">DWORD0_DQ6_Q3</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[27]</td><td colspan="1" rowspan="1">DWORD0_DQ5_Q0</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[26]</td><td colspan="1" rowspan="1">DWORD0_DQ5_Q1</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[25]</td><td colspan="1" rowspan="1">DWORD0_DQ5_Q2</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[24]</td><td colspan="1" rowspan="1">DWORD0_DQ5_Q3</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[23]</td><td colspan="1" rowspan="1">DWORD0_DQ4_Q0</td><td colspan="1" rowspan="1">R/W</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">[22]</td><td colspan="1" rowspan="1">DWORD0_DQ4_Q1</td><td colspan="1" rowspan="1">R/W</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">[21]</td><td colspan="1" rowspan="1">DWORD0_DQ4_Q2</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[20]</td><td colspan="1" rowspan="1">DWORD0_DQ4_Q3</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[19]</td><td colspan="1" rowspan="1">DWORD0_DQ3_Q0</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[18]</td><td colspan="1" rowspan="1">DWORD0_DQ3_Q1</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[17]</td><td colspan="1" rowspan="1">DWORD0_DQ3_Q2</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[16]</td><td colspan="1" rowspan="1">DWORD0_DQ3_Q3</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[15]</td><td colspan="1" rowspan="1">DWORD0_DQ2_Q0</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[14]</td><td colspan="1" rowspan="1">DWORD0_DQ2_Q1</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[13]</td><td colspan="1" rowspan="1">DWORD0_DQ2_Q2</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[12]</td><td colspan="1" rowspan="1">DWORD0_DQ2_Q3</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[11]</td><td colspan="1" rowspan="1">DWORD0_DQ1_Q0</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[10]</td><td colspan="1" rowspan="1">DWORD0_DQ1_Q1</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[9]</td><td colspan="1" rowspan="1">DWORD0_DQ1_Q2</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[8]</td><td colspan="1" rowspan="1">DWORD0_DQ1_Q3</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[7]</td><td colspan="1" rowspan="1">DWORD0_DQ0_Q0</td><td colspan="1" rowspan="1">R/W</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">[6]</td><td colspan="1" rowspan="1">DWORD0_DQ0_Q1</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[5]</td><td colspan="1" rowspan="1">DWORD0_DQ0_Q2</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[4]</td><td colspan="1" rowspan="1">DWORD0_DQ0_Q3</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[3]</td><td colspan="1" rowspan="1">DWORD0_ECC0_Q0</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[2]</td><td colspan="1" rowspan="1">DWORD0_ECC0_Q1</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[1]</td><td colspan="1" rowspan="1">DWORD0_ECC0_Q2</td><td colspan="1" rowspan="1">R/W</td><td></td></tr><tr><td colspan="1" rowspan="1">[0]</td><td colspan="1" rowspan="1">DWORD0_ECC0_Q3</td><td colspan="1" rowspan="1">R/W</td><td></td></tr></table>

## 13.5.8 AWORD\_MISR

This instruction captures and shifts out the AWORD MISR value on the WSO output. The MISR in this instruction is associated with the AWORD loopback test feature. The data register bit positions are specified in Table 129.

Note that the content of the MISR is not specified after shifting out the MISR content. The host should reinitialize the MISR using the AWORD\_MISR\_CONFIG instruction before continuing with additional testing. See HBM4 Loopback Test Modes clauses for MISR mode features and usage.

## Wrapper Data Register

When AWORD\_MISR is the current instruction, the data register as shown in Table 129 is connected between WSI and WSO. The notation is "…\_R" for bits latched on the rising CK clock edge and "…\_F" for bits latched on the falling CK clock edge.

## CaptureWR

When AWORD\_MISR is the current instruction, the CaptureWR event will load the respective MISR values into the shift stage of the WDR. A minimum waiting time of tSMISR between the last data capture into the AWORD MISR and this CaptureWR event must be observed.

## UpdateWR

When AWORD\_MISR is the current instruction, the UpdateWR event will have no effect.

## 13.5.8 AWORD\_MISR (cont’d)

Table 129 – AWORD\_MISR Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=2>Description</td></tr><tr><td rowspan=1 colspan=1>[37]</td><td rowspan=1 colspan=1>R1_R</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[36]</td><td rowspan=1 colspan=1>R1_F</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[35]</td><td rowspan=1 colspan=1>R2_R</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[34]</td><td rowspan=1 colspan=1>R2_F</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[33]</td><td rowspan=1 colspan=1>R3_R</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[32]</td><td rowspan=1 colspan=1>R3_F</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[31]</td><td rowspan=1 colspan=1>R0_R</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[30]</td><td rowspan=1 colspan=1>R0_F</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[29]</td><td rowspan=1 colspan=1>R4_R</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[28]</td><td rowspan=1 colspan=1>R4_F</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[27]</td><td rowspan=1 colspan=1>R5_R</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[26]</td><td rowspan=1 colspan=1>R5_F</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[25]</td><td rowspan=1 colspan=1>R6_R</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[24]</td><td rowspan=1 colspan=1>R6_F</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[23]</td><td rowspan=1 colspan=1>R7_R</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[22]</td><td rowspan=1 colspan=1>R7_F</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[21]</td><td rowspan=1 colspan=1>R8_R</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[20]</td><td rowspan=1 colspan=1>R8_F</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[19]</td><td rowspan=1 colspan=1>R9_R</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[18]</td><td rowspan=1 colspan=1>R9_F</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[17]</td><td rowspan=1 colspan=1>ARFU_R</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[16]</td><td rowspan=1 colspan=1>ARFU_F       C</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[15]</td><td rowspan=1 colspan=1>C7_R</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[14]</td><td rowspan=1 colspan=1>C7_F</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[13]</td><td rowspan=1 colspan=1>C6_R</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[12]</td><td rowspan=1 colspan=1>C6_F</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>[11]</td><td rowspan=1 colspan=1>C5_R</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[10]</td><td rowspan=1 colspan=1>C5_F</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[9]</td><td rowspan=1 colspan=1>C4_R</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[8]</td><td rowspan=1 colspan=1>C4_F</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[7]</td><td rowspan=1 colspan=1>C3_R</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[6]</td><td rowspan=1 colspan=1>C3_F</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1></td><td></td></tr><tr><td rowspan=1 colspan=1>[5]</td><td rowspan=1 colspan=1>C2_R</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1></td><td></td></tr><tr><td rowspan=1 colspan=1>[4]</td><td rowspan=1 colspan=1>C2_F</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[3]</td><td rowspan=1 colspan=1>C1_R</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[2]</td><td rowspan=1 colspan=1>C1_F</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>[1]</td><td rowspan=1 colspan=1>C0_R</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1></td><td></td></tr><tr><td rowspan=1 colspan=1>[0]</td><td rowspan=1 colspan=1>C0_F</td><td rowspan=1 colspan=1>R</td><td></td><td></td></tr></table>

## 13.5.9 CHANNEL\_ID

This instruction enables the HBM4 channel identification by driving all bidirectional DWORD I/Os to HIGH, unless a channel is disabled either via the corresponding CHANNEL\_AVAILABLE bit in the DEVICE ID WDR or via the CHANNEL\_DISABLE instruction. In these cases, a channel will not respond to the CHANNEL\_ID instruction.

## Wrapper Data Register

When CHANNEL\_ID is the current instruction, the data register as shown in Table 130 is connected between WSI and WSO.

## CaptureWR

When CHANNEL\_ID is the current instruction, the CaptureWR event will have no effect.

## UpdateWR

When CHANNEL\_ID is the current instruction, the UpdateWR event will load the enable bit from the shift stage into the update stage of the WDR. All DWORD bidirectional I/Os (DQ, DBI, RD, ECC/SEV and DPAR) will drive a HIGH latest after t when the enable bit is 1, and return to their default state latest after t<sub>OZCHN</sub> when the enable bit is 0 or a different instruction has been loaded in the WIR. Output pins (RDQS\_t/c, DERR) maintain the default state regardless of the CHANNEL\_ID instruction. DBI, ECC and DPAR will drive a HIGH even if the respective function is disabled in the Mode Register.

Table 130 — CHANNEL\_ID Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>[0]</td><td rowspan=1 colspan=1>ENABLE</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>0 - TX return to their default state1 - TX drive a HIGH</td></tr></table>

## 13.5.10 AWORD\_MISR\_CONFIG

This instruction configures the AWORD MISR for subsequent tests. See HBM4 Loopback Test Modes clauses for MISR mode features and usage.

## Wrapper Data Register

When AWORD\_MISR\_CONFIG is the current instruction, the data register as shown in Table 131 is connected between WSI and WSO.

## CaptureWR

When AWORD\_MISR\_CONFIG is the current instruction, the CaptureWR event will have no effect.

## UpdateWR

When AWORD\_MISR\_CONFIG is the current instruction, the UpdateWR event will load the configuration bits from the shift stage into the update stage of the WDR and configures the AWORD MISR into the desired mode. The new configuration is valid for subsequent AWORD MISR operation once the t<sub>CMISR</sub> timing has elapsed.

Table 131 — AWORD\_MISR\_CONFIG Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>[7:3]</td><td rowspan=1 colspan=1>VENDOR_SPECIFIC [4:0]</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>00000 - No action (default)All others - Reserved for vendor specific the AWORD MISRConfiguration</td></tr><tr><td rowspan=1 colspan=1>[2]</td><td rowspan=1 colspan=1>ENABLE</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>0 - Off1 - On</td></tr><tr><td rowspan=1 colspan=1>[1:0]</td><td rowspan=1 colspan=1>MODE[1:0]</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>00 - Preseta) The 38-bit AWORD MISR is preset to0x2AAAAAAAAAh;b) the AWORD LFSR COMPARE STICKY bits are allcleared to 0;c) the AWORD preamble clock filter circuit is enabled.01 - LFSR Compare mode10 - Register mode: AWORD transfers are captured directly tothe MISR register. Note that Register mode cannot be usedto set an alternate seed value (see Test method for AWORD(Write) Register Mode)11 - MISR mode</td></tr></table>

## 13.5.11 DEVICE\_ID

This instruction allows shift out of the DEVICE\_ID that provides various information about the HBM4 DRAM including a device specific unique serial number. The per channel ID data registers are intended to support vendors who require additional resolution for identifying the device.

## Wrapper Data Register

When the DEVICE\_ID instruction is updated the data register as shown in Table 132 is connected between WSI and WSO.

## CaptureWR

When DEVICE\_ID is the current instruction, the CaptureWR event will load the respective identification field values into the shift stage of the WDR.

## UpdateWR

When DEVICE\_ID is the current instruction, the UpdateWR event will have no effect.

## 13.5.11 DEVICE\_ID (cont’d)

Table 132 — DEVICE\_ID Wrapper Data Register
<table><tr><td colspan="1" rowspan="1">BitPosition</td><td colspan="1" rowspan="1">Bit Field</td><td colspan="1" rowspan="1">Type</td><td colspan="1" rowspan="1">Description</td></tr><tr><td colspan="1" rowspan="1">[181]</td><td colspan="1" rowspan="1">PROG RDQS PST</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Indicates the support of programmable RDQS Postamble(tRPST).0 – Programmable tRPST is not supported.1 – Programmable tRPST is supported.</td></tr><tr><td colspan="1" rowspan="1">[180]</td><td colspan="1" rowspan="1">SRE ECS FLAG</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Indicates the support of the ECSflag in SRE or PREabcommands.0 – SRE ECS Flag is not supported1 – SRE ECS Flag is supported</td></tr><tr><td colspan="1" rowspan="1">[179]</td><td colspan="1" rowspan="1">EXTENDED MR</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Indicates the support of an extended Mode Registeraddress space.0 – Mode registers MR0 thru MR15 are supported1 – Mode registers MR0 thru MR19 are supported</td></tr><tr><td colspan="1" rowspan="1">[178]</td><td colspan="1" rowspan="1">READ DCA</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Indicates the support of Read Duty Cycle Adjuster.0 – Read DCA is not supported, and MR10 is not utilized1 – Read DCA is supported, and adjustment is controlledvia MR10</td></tr><tr><td colspan="1" rowspan="1">[177]</td><td colspan="1" rowspan="1">RXoffC</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Indicates the support of Rx Offset Calibration.0 – Rx Offset Calibration is not supported1 – Rx Offset Calibration is supported</td></tr><tr><td colspan="1" rowspan="1">[176]</td><td colspan="1" rowspan="1">LOW TEMP</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">New temperature code supports for low temperatureoperating limits in TEMPERATURE WDR0 – LOW TEMP code is not supported1 – LOW TEMP code is supported</td></tr><tr><td colspan="1" rowspan="1">[175:173]</td><td colspan="1" rowspan="1">OPT_FEATURES[2:0]</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">Reserved to indicate the support of optional features thatmay be added in a future revision of this standard.000 – default0 – optional feature is not supported1 – optional feature is supported</td></tr><tr><td colspan="1" rowspan="1">[172]</td><td colspan="1" rowspan="1">PER PC VREFD4</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Indicates the support of Per Pseudo Channel VREFD.0 – Per Pseudo Channel VREFD is not supported andMR18 is not utilized1 – Per Pseudo Channel VREFD is supported. MR14 isutilized for PC0 and MR18 is utilized for PC1</td></tr><tr><td colspan="1" rowspan="1">[171]</td><td colspan="1" rowspan="1">SHARED REP RES</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Sharing of HS REP CAP with self repair0: Self repair resources are separate from hard/softresources1: Self repair resources are shared with hard/softresources</td></tr><tr><td colspan="1" rowspan="1">[170]</td><td colspan="1" rowspan="1">PPR RSVD²</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Reserved row addresses associated with a single soft orhard repair.0 - default</td></tr><tr><td colspan="1" rowspan="1">[169:156]</td><td colspan="1" rowspan="1">PPR_RA[13:0]</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Row addresses associated with a single soft or hardrepair.Encoding:0 - row address is evaluated1 - row address is ignoredbit 0: RA0bit 1: RA1bit 12: RA13bit 13: RFU</td></tr><tr><td colspan="1" rowspan="1">[155]</td><td colspan="1" rowspan="1">RAADEC C</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">RAA Counter Decrement per REF Command for RFMlevel C(MR8 OP[5:4] = 11).The field shall be ignored when the ARFM bit is 0Same encoding as in RAADEC</td></tr><tr><td colspan="1" rowspan="1">[154:153]</td><td colspan="1" rowspan="1">RAAMMT C[1:0]</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">RAA Maximum Management Threshold (RAAMMT) forRFM1evel C (MR8 OP[5:4] = 11).The field shall be ignored when the ARFM bit is 0Same encoding as in RAAMMT</td></tr><tr><td colspan="1" rowspan="1">[152:150]</td><td colspan="1" rowspan="1">RAAIMT_C[2:0]</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">RAA Initial Management Threshold (RAAIMT) for RFMlevel C(MR8 OP[5:4] = 11)The field shall be ignored when the ARFM bit is 0.Same encoding as in RAAIMT</td></tr><tr><td colspan="1" rowspan="1">[149]</td><td colspan="1" rowspan="1">RAADEC B      Sa</td><td colspan="1" rowspan="1">Ri</td><td colspan="1" rowspan="1">RAA Counter Decrement per REF Command for RFMlevel B(MR8 OP[5:4] = 10).The field shall be ignored when the ARFM bit is 0Same encoding as in RAADEC</td></tr><tr><td colspan="1" rowspan="1">[148:147]</td><td colspan="1" rowspan="1">RAAMMT_B[1:0]</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">RAA Maximum Management Threshold (RAAMMT) forRFMlevel B (MR8 OP[5:4] = 10).The field shall be ignored when the ARFM bit is 0Same encoding as in RAAMMT</td></tr><tr><td colspan="1" rowspan="1">[146:144]</td><td colspan="1" rowspan="1">RAAIMT B[2:0]</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">RAA Initial Management Threshold (RAAIMT) for RFMlevel B(MR8 OP[5:4] = 10).The field shall be ignored when the ARFM bit is 0Same encoding as in RAAIMT</td></tr><tr><td colspan="1" rowspan="1">[143]</td><td colspan="1" rowspan="1">RAADEC A</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">RAA Counter Decrement per REF Command for RFMlevel A(MR8 OP[5:4] = 01).The field shall be ignored when the ARFM bit is 0Same encoding as in RAADEC</td></tr><tr><td colspan="1" rowspan="1">[142:141]</td><td colspan="1" rowspan="1">RAAMMT A[1:0]</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">RAA Maximum Management Threshold (RAAMMT) forRFMlevel A (MR8 OP[5:4] = 01).The field shall be ignored when the ARFM bit is 0Same encoding as in RAAMMT</td></tr><tr><td colspan="1" rowspan="1">[140:138]</td><td colspan="1" rowspan="1">RAAIMT_A[2:0]</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">RAA Initial Management Threshold (RAAIMT) for RFMlevel A(MR8 OP[5:4] = 01).The field shall be ignored when the ARFM bit is 0Same encoding as in RAAIMT</td></tr><tr><td colspan="1" rowspan="1">[137]</td><td colspan="1" rowspan="1">RAADEC</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Default RAA Counter Decrement per REF Command.The field shall be ignored when the RFM bit is 0.0 - 1.0 ×RAAIMT1 - 0.5 × RAAIMT</td></tr><tr><td colspan="1" rowspan="1">[136:135]</td><td colspan="1" rowspan="1">RAAMMT[1:0]</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Default RAA Maximum Management Threshold(RAAMMT)The field shall be ignored when the RFM bit is 0.00 - 3×RAAIMT01 - 4 × RAAIMT10 - 5×RAAIMT11 - 6×RAAIMT</td></tr><tr><td colspan="1" rowspan="1">[134:132]</td><td colspan="1" rowspan="1">RAAIMT[2:0]</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Default RAA Initial Management Threshold (RAAIMT)alThe field shall be ignored when the RFM bit is 0.000 - 32001 - 40010 - 48011 -56100 - 64101 - 72110 - 80111 – Reserved</td></tr><tr><td colspan="1" rowspan="1">[131:130]</td><td colspan="1" rowspan="1">DRFM_BRC[1:0]</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">Directed Refresh Management (DRFM) - SupportedBounded Refresh Configuration (BRC) Settings00 – BRC = 2 is supported (default)01 – BRC = 2 and 3 are supported10 – BRC = 2, 3 and 4 are supported</td></tr><tr><td colspan="1" rowspan="1">[129]</td><td colspan="1" rowspan="1">ARFM</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Adaptive Refresh Management (ARFM)0 – Adaptive Refresh Management is not supported1 – Adaptive Refresh Management is supported</td></tr><tr><td colspan="1" rowspan="1">[128]</td><td colspan="1" rowspan="1">RFM</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Refresh Management (RFM)0 - Refresh Management not required1 - Refresh Management required</td></tr><tr><td colspan="1" rowspan="1">[127:120]</td><td colspan="1" rowspan="1">MANUFACTURINGYEAR[7:0]</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Binary encoded year:2020 = 00000000; 2024 = 00000100</td></tr><tr><td colspan="1" rowspan="1">[119:112]</td><td colspan="1" rowspan="1">MANUFACTURINGWEEK[7:0]</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Binary encoded week:WW52 = 00110100</td></tr><tr><td colspan="1" rowspan="1">[111:48]</td><td colspan="1" rowspan="1">SERIAL_NO[63:0]</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Unique device ID</td></tr><tr><td colspan="1" rowspan="1">[47:44]</td><td colspan="1" rowspan="1">MANUFACTURERID[3:0]</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">0001 - Samsung0110 - SK Hynix1100 - CXMT1111 - MicronAll others – Reserved</td></tr><tr><td colspan="1" rowspan="1">[43:40]</td><td colspan="1" rowspan="1">DENSITY[3:0]</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Memory density per channel (see 3.2 ChannelAddressing)0000 - 3 Gb (24Gb 4 High)0010 - 6 Gb (24Gb 8-High)0100 - 9 Gb (24Gb 12-High)0110 - 12 Gb (24Gb 16-High)0001 - 4 Gb (32Gb 4 High)0011 - 8 Gb (32Gb 8-High)0101 - 12 Gb (32Gb 12-High)0111 - 16 Gb (32Gb 16-High)</td></tr><tr><td colspan="1" rowspan="1">[39:8]</td><td colspan="1" rowspan="1">CHANNELAVAILABLE[31:0]1</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Channel Available0 - Channel not present / not working1 - Channel present / workingChannel encoding (1 bit per channel):bit 0: channel 0bit 1: channel 1bit 30: channel 30bit 31: channel 31</td></tr><tr><td colspan="1" rowspan="1">[7:0]</td><td colspan="1" rowspan="1">MODEL PARTNUMBER[7:0]</td><td colspan="1" rowspan="1">R</td><td colspan="1" rowspan="1">Vendor reserved</td></tr><tr><td colspan="4" rowspan="1">NOTE 1 A channel marked as “not present / not working" keeps all AWORD and DWORD input and output bufferspermanently disabled and drives that channel's WSO to LOW.NOTE 2 The PPR_RVSD field will only be used in the future if additions to the addressing table increase the row address toinclude RA15. If future additions to the addressing table increase the bank, column, or pseudo channel address thenthe PPR RSVD will remain at the default.NOTE 3 HBM4 devices must output bits [175:173] even if the optional features are not used.NOTE 4 Allocating EXTENDED MR to 0 and PER PC VREF to 1 in DEVICE ID at the same time is not permitted.</td></tr></table>

## 13.5.12 TEMPERATURE

This instruction captures the HBM4 DRAM’s junction temperature. Temperature reporting is specified as a 9-bit field: bit 0 or LSB indicates the validity of the temperature sensor read-out, and the remaining 8 bits indicate the temperature in degrees Celsius.

## Wrapper Data Register

When TEMPERATURE is the current instruction, the data register as shown in Table 133 is connected between WSI and WSO[31:0], and the WSO outputs of all active channels drive the same data during ShiftWR events.

## CaptureWR

When TEMPERATURE is the current instruction, the CaptureWR event will load the temperature field values into the shift stage of the WDR.

## UpdateWR

When TEMPERATURE is the current instruction, the UpdateWR event will have no effect.

Table 133 — TEMPERATURE Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Note</td></tr><tr><td rowspan=1 colspan=1>[8:1]</td><td rowspan=1 colspan=1>TEMP[7:0]</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>Temperature in degrees Celsius. Examples:8&#x27;b 0000 0000 = − 40 ℃8&#x27;b 0010 1000 = 0 ℃8&#x27;b 0100 0001 = 25 ℃8&#x27;b 1010 0111 = 127 ℃8&#x27;b 1111 1111 = SDRAM Low temperature operating limitexceeded (optional)</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>[0]</td><td rowspan=1 colspan=1>VALID</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>Temperature sensor output valid0 – Invalid1 − Valid</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=5>NOTE 1 8’b 1111 1111 is vendor optional code. Refer to the vendor&#x27;s datasheet for details.</td></tr></table>

## 13.5.13 MODE\_REGISTER\_DUMP\_SET

The MODE\_REGISTER\_DUMP\_SET instruction provides read (dump) and write (set) access to the HBM4 Mode Registers.

## Wrapper Data Register

When MODE\_REGISTER\_DUMP\_SET is the current instruction, the data register as shown in Table 134 is connected between WSI and WSO.

## CaptureWR

When MODE\_REGISTER\_DUMP\_SET is the current instruction, the CaptureWR event will capture the Mode Register content into the shift stage of the WDR. Reserved Mode Registers and bit fields marked as “RFU” capture an ‘X’ value. The Mode Register content itself does not change with the CaptureWR event. A minimum waiting time of t<sub>MRSS</sub> = t<sub>MOD</sub> must be observed between an MRS command and this Capture WR event.

## UpdateWR

When MODE\_REGISTER\_DUMP\_SET is the current instruction, the UpdateWR event will simultaneously load the bits from the shift stage to the mode registers. The updated mode register content will be valid for subsequent mission mode operation after t<sub>UPDMRS</sub>.

Table 134 — MODE\_REGISTER\_DUMP\_SET Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition¹</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>[159:152]</td><td rowspan=1 colspan=1>MR19</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>MR19[7:0]</td></tr><tr><td rowspan=1 colspan=1>[151:144]</td><td rowspan=1 colspan=1>MR18</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR18[7:0]</td></tr><tr><td rowspan=1 colspan=1>[143:136]</td><td rowspan=1 colspan=1>MR17</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR17[7:0]</td></tr><tr><td rowspan=1 colspan=1>[135:128]</td><td rowspan=1 colspan=1>MR16</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR16[7:0]</td></tr><tr><td rowspan=1 colspan=1>[127:120]</td><td rowspan=1 colspan=1>MR15</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR15[7:0]</td></tr><tr><td rowspan=1 colspan=1>[119:112]</td><td rowspan=1 colspan=1>MR14</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR14[7:0]</td></tr><tr><td rowspan=1 colspan=1>[111:104]</td><td rowspan=1 colspan=1>MR13</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR13[7:0]</td></tr><tr><td rowspan=1 colspan=1>[103:96]</td><td rowspan=1 colspan=1>MR12</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR12[7:0]</td></tr><tr><td rowspan=1 colspan=1>[95:88]</td><td rowspan=1 colspan=1>MR11</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR11[7:0]</td></tr><tr><td rowspan=1 colspan=1>[87:80]</td><td rowspan=1 colspan=1>MR10</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR10[7:0]</td></tr><tr><td rowspan=1 colspan=1>[79:72]</td><td rowspan=1 colspan=1>MR9</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR9[7:0]</td></tr><tr><td rowspan=1 colspan=1>[71:64]</td><td rowspan=1 colspan=1>MR8</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR8[7:0]</td></tr><tr><td rowspan=1 colspan=1>[63:56]</td><td rowspan=1 colspan=1>MR7</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR7[7:0]</td></tr><tr><td rowspan=1 colspan=1>[55:48]</td><td rowspan=1 colspan=1>MR6</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR6[7:0]</td></tr><tr><td rowspan=1 colspan=1>[47:40]</td><td rowspan=1 colspan=1>MR5</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR5[7:0]</td></tr><tr><td rowspan=1 colspan=1>[39:32]</td><td rowspan=1 colspan=1>MR4</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR4[7:0]</td></tr></table>

## 13.5.13 MODE\_REGISTER\_DUMP\_SET (cont’d)

Table 134 — MODE\_REGISTER\_DUMP\_SET Wrapper Data Register (cont’d)
<table><tr><td rowspan=1 colspan=1>BitPosition¹</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>[31:24]</td><td rowspan=1 colspan=1>MR3</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR3[7:0]</td></tr><tr><td rowspan=1 colspan=1>[23:16]</td><td rowspan=1 colspan=1>MR2</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR2[7:0]</td></tr><tr><td rowspan=1 colspan=1>[15:8]</td><td rowspan=1 colspan=1>MR1</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR1[7:0]</td></tr><tr><td rowspan=1 colspan=1>[7:0]</td><td rowspan=1 colspan=1>MR0</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>MR0[7:0]</td></tr><tr><td rowspan=1 colspan=4>NOTE1The maximum bit position for MODE_REGISTER_DUMP_SET is 160 bits but is vendor specific andwill depend on whether MR16-MR19 are supported, which is indicated by the EXTENDED_MR field of theDEVICE_ID WDR (see Table 132). Refer to supplier datasheet for more information.</td></tr></table>

## 13.5.14 READ\_LFSR\_COMPARE\_STICKY

This instruction is used to capture the LFSR Compare Sticky error data to be shifted out on the WSO output. The instruction is associated with the AWORD and DWORD I/O loopback test features. Data register bit positions are specified in the Data Register clause of this instruction in Table 135. Note that the content of the MISR and LFSR Compare Sticky error data registers is not specified after shifting out the sticky error content. The host should reinitialize the MISR registers, such as with MR7 Preset (Table 17) and AWORD\_MISR\_CONFIG preset, before continuing with additional testing. See clause HBM4 Loopback Test Modes for MISR mode features and usage.

While both the AWORD and DWORD sticky error bits share a common WDR, the bits are set and cleared only by their respective AWORD or DWORD Preset and LFSR Compare operations. For example, an AWORD\_MISR\_CONFIG preset operation clears the AWORD sticky error bits, and the state of the DWORD sticky error bits is undefined; therefore, the host should ignore the DWORD sticky error bits when operating the AWORD LFSR Compare mode. Conversely, the DWORD\_MISR\_CONFIG preset operation clears the DWORD sticky error bits, and the state of the AWORD sticky error bits is undefined; therefore, the host should ignore the AWORD sticky error bits when operating the DWORD LFSR Compare mode.

## Wrapper Data Register

When READ\_LFSR\_COMPARE\_STICKY is the current instruction, the data register as shown in Table 135 is connected between WSI and WSO.

## CaptureWR

When READ\_LFSR\_COMPARE\_STICKY is the current instruction, the CaptureWR event will load the sticky error values into the shift stage of the WDR.

## UpdateWR

When READ\_LFSR\_COMPARE\_STICKY is the current instruction, the UpdateWR event will have no effect.

## 13.5.14 READ\_LFSR\_COMPARE\_STICKY (cont’d)

Table 135 — READ\_LFSR\_COMPARE\_STICKY Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>[98:59]</td><td rowspan=1 colspan=1>DWORD1</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>DWORD1: DQ[63:32], DBI[7:4], ECC[3:2] and SEV[3:2](same ordering as DWORD0)</td></tr><tr><td rowspan=1 colspan=1>[58]</td><td rowspan=1 colspan=1>AWORD_R1</td><td rowspan=1 colspan=1>R</td><td rowspan=19 colspan=1>AWORDGlobalX</td></tr><tr><td rowspan=1 colspan=1>[57]</td><td rowspan=1 colspan=1>AWORD_R2</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[56]</td><td rowspan=1 colspan=1>AWORD R3</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[55]</td><td rowspan=1 colspan=1>AWORD_R0</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[54]</td><td rowspan=1 colspan=1>AWORD_R4</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[53]</td><td rowspan=1 colspan=1>AWORD_R5</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[52]</td><td rowspan=1 colspan=1>AWORD_R6</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[51]</td><td rowspan=1 colspan=1>AWORD_R7</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[50]</td><td rowspan=1 colspan=1>AWORD_R8</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[49]</td><td rowspan=1 colspan=1>AWORD_R9</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[48]</td><td rowspan=1 colspan=1>AWORD_ARFU</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[47]</td><td rowspan=1 colspan=1>AWORD_C7</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[46]</td><td rowspan=1 colspan=1>AWORD_C6</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[45]</td><td rowspan=1 colspan=1>AWORD_C5</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[44]</td><td rowspan=1 colspan=1>AWORD_C4</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[43]</td><td rowspan=1 colspan=1>AWORD_C3</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[42]</td><td rowspan=1 colspan=1>AWORD C2</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[41]</td><td rowspan=1 colspan=1>AWORD_C1</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[40]</td><td rowspan=1 colspan=1>AWORD_CO</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[39:30]</td><td rowspan=1 colspan=1>DWORD0_BYTE_3</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>Byte 3 of DWORD0: DQ[31:24], DBI3 and SEV1(same ordering as Byte 0)</td></tr><tr><td rowspan=1 colspan=1>[29:20]</td><td rowspan=1 colspan=1>DWORD0 BYTE 2</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>Byte 2 of DWORD0: DQ[23:16], DBI2 and SEV0(same ordering as Byte 0)</td></tr><tr><td rowspan=1 colspan=1>[19:10]</td><td rowspan=1 colspan=1>DWORD0 BYTE 1</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>Byte 1 of DWORD0: DQ[15:8], DBI1 and ECC1(same ordering as Byte 0)</td></tr><tr><td rowspan=1 colspan=1>[9]</td><td rowspan=1 colspan=1>DWORD0_DBI0</td><td rowspan=1 colspan=1>R</td><td rowspan=10 colspan=1>Byte 0 of DWORD0 (PC0)</td></tr><tr><td rowspan=1 colspan=1>[8]</td><td rowspan=1 colspan=1>DWORD0_DQ7</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[7]</td><td rowspan=1 colspan=1>DWORD0_DQ6</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[6]</td><td rowspan=1 colspan=1>DWORD0_DQ5</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[5]</td><td rowspan=1 colspan=1>DWORD0_DQ4</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[4]</td><td rowspan=1 colspan=1>DWORD0_DQ3</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[3]</td><td rowspan=1 colspan=1>DWORD0_DQ2</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[2]</td><td rowspan=1 colspan=1>DWORD0 DQ1</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[1]</td><td rowspan=1 colspan=1>DWORD0 DQ0</td><td rowspan=1 colspan=1>R</td></tr><tr><td rowspan=1 colspan=1>[0]</td><td rowspan=1 colspan=1>DWORD0 ECC0</td><td rowspan=1 colspan=1>R</td></tr></table>

## 13.5.15 SOFT\_LANE\_REPAIR and HARD\_LANE\_REPAIR

SOFT\_LANE\_REPAIR and HARD\_LANE\_REPAIR instructions can only be issued as part of the device initialization and before normal memory operation has commenced, e.g., before the CK clock has started to toggle.

## Wrapper Data Register

When either SOFT\_LANE\_REPAIR or HARD\_LANE\_REPAIR is the current instruction, the LANE\_REPAIR wrapper data register as shown in Table 136 is connected between WSI and WSO.

Figure 115 illustrates the interaction between SOFT\_LANE\_REPAIR and HARD\_LANE\_REPAIR instructions and the associated registers. It is pointed out that the actual I/O lane remapping is derived from the content of the lane repair shadow register.

## CaptureWR

When either SOFT\_LANE\_REPAIR or HARD\_LANE\_REPAIR is the current instruction, the CaptureWR event will load the lane remapping data from the lane repair shadow register into the shift stage of the WDR. This internal lane repair shadow register is pre-loaded with the repair data from a preceding HARD $\_ { \mathrm { L A N E } }$ REPAIR operation upon HBM4 DRAM initialization (RESET\_n pulled Low). or the default value of $\operatorname { F _ { h } }$ for DWORD and AWORD lanes, or $1 \mathrm { F _ { h } }$ for WSO lanes if no previous repairs have occurred. The memory controller shall use these data to configure the lane repair accordingly at the host for subsequent SOFT\_LANE\_REPAIRS.

## UpdateWR

When SOFT\_LANE\_REPAIR is the current instruction, the UpdateWR event will load the lane remapping data from the shift stage of the WDR into the lane repair shadow register and force the I/O lanes to be remapped accordingly. The bit field(s) for any previous AWORD, DWORD or WSO lane repairs must be included in the WDR loaded with UpdateWR, and bit fields for any lane not previously repaired must be set to $\operatorname { F _ { h } }$ for DWORD and AWORD lanes, or $1 \mathrm { F _ { h } }$ for WSO lanes (see Interconnect Redundancy Remapping clause for details). This remapping is non-persistent; it will be lost when RESET\_n is pulled low or the device loses power. Pulling WRST\_n low does not reset the lane repair shadow register.

When HARD\_LANE\_REPAIR is the current instruction, the UpdateWR event will load the lane remapping data from the shift stage of the WDR into the hard lane repair register. The controller must wait $\mathbf { t } _ { \mathrm { H L R E P } }$ to allow the HBM4 DRAM to complete this operation and permanently store the repair vector.

Only a single broken lane can be repaired at a time, in order to limit the current constraint of the associated circuits. If multiple lanes are to be repaired, it is required to shift in the repair vectors for each broken lane sequentially, with all other lane repair setting = Fh for AWORD or DWORD lanes, or setting $= 1 \mathrm { F _ { h } }$ for WSO lanes, and initiate each actual lane repair with a separate UpdateWR event.

The HARD\_LANE\_REPAIR UpdateWR event itself does not lead to an actual re-mapping of the I/O lanes. For such re-mapping to get effective it is required to initiate a chip reset by pulling RESET\_n LOW for at least t , which copies the repair vector from the hard lane repair register into the lane repair shadow register as shown in Figure 115.

## 13.5.15 SOFT\_LANE\_REPAIR and HARD\_LANE\_REPAIR (cont’d)

Table 136 — LANE\_REPAIR Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>[44:40]</td><td rowspan=1 colspan=1>WSO[4:0]</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>Lane remapping applied to WSO $0 _ { \mathrm { h } } - \mathrm { F _ { h } } \mathrm { : } \mathrm { W } \mathrm { \bar { S } O 0 } \mathrm { ~ - } \mathrm { W } \mathrm { \bar { S } O 1 } 5 \mathrm { ~ o r } \mathrm { W } \mathrm { S O } 1 6 \mathrm { - } \mathrm { W } \mathrm { S O } 3 1$  $1 0 _ { \mathrm { h } } - 1 \mathrm { E } _ { \mathrm { h } } \colon$ Reserved $1 \mathrm { F _ { h } } \mathrm { : }$ No lane remapping (default)WSO[4:0] bit field is only supported in Channels 1 and 17.Channel 1 for repair of WSO0 - WSO15Channel 17 for repair of WSO16 - WSO31</td></tr><tr><td rowspan=1 colspan=1>[39:36]</td><td rowspan=1 colspan=1>DWORD1 BYTE3[3:0]</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>Lane remapping applied to DWORD1 byte 3 $0 _ { \mathrm { h } } \mathrm { { : } } \operatorname { S E V } 3$  $1 _ { \mathrm { h } } - 8 _ { \mathrm { h } } \colon { \mathrm { D Q } } 5 6 - { \mathrm { D Q } } 6 3$  $9 _ { \mathrm { h } } ; \mathrm { D B I } 7$  $\mathbf { A } _ { \mathrm { h } } - \mathrm { E h } \colon \mathrm { R e s e r v e d }$  $\mathrm { F _ { h } } \mathrm { : }$ No lane remapping (default)</td></tr><tr><td rowspan=1 colspan=1>[35:32]</td><td rowspan=1 colspan=1>DWORD1 BYTE2[3:0]</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>Lane remapping applied to DWORD1 byte 2 $0 _ { \mathrm { h } } \mathrm { { : } } \operatorname { S E V } 2$       1 $1 _ { \mathrm { h } } - 8 _ { \mathrm { h } } \colon \mathrm { D Q } 4 8 \textrm { - D Q } 5 5$  $9 _ { \mathrm { h } } \colon \mathrm { D B I } 6$  O $\mathbf { A } _ { \mathrm { h } } - \mathrm { E h } \colon \mathrm { R e s e r v e d }$  $\mathrm { F _ { h } } \mathrm { : N o }$ lane remapping (default)</td></tr><tr><td rowspan=1 colspan=1>[31:28]</td><td rowspan=1 colspan=1>DWORD1_BYTE1[3:0]</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>Lane remapping applied to DWORD1 byte 1Oh: ECC3 $1 _ { \mathrm { h } } - 8 _ { \mathrm { h } } \colon \mathrm { D Q } 4 0 \mathbin { - } \mathrm { D Q } 4 7$  $9 _ { \mathrm { h } } ; \mathrm { D B I } 5$  $\mathrm { A _ { h } } - \mathrm { E _ { h } } \mathrm { : R e s e r v e d }$  $\mathrm { F _ { h } } \mathrm { : N o }$ lane remapping (default)</td></tr><tr><td rowspan=1 colspan=1>[27:24]</td><td rowspan=1 colspan=1>DWORD1 BYTE0[3:0]</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>Lane remapping applied to DWORD1 byte 0 $0 _ { \mathrm { h } } \colon \mathrm { E C C } 2$  $1 _ { \mathrm { h } } - 8 _ { \mathrm { h } } \colon \mathrm { D Q } 3 2 \AA - \mathrm { D Q } 3 9$  $9 _ { \mathrm { h } } ; \mathrm { D B I } 4$  $\mathrm { A _ { h } } - \mathrm { E _ { h } } \mathrm { : R e s e r v e d }$  $\mathrm { F _ { h } } \mathrm { : N o }$ lane remapping (default)</td></tr><tr><td rowspan=1 colspan=1>[23:20]</td><td rowspan=1 colspan=1>AWORD_RA[3:0]</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>Lane remapping applied to AWORD. $0 _ { \mathrm { h } } - 9 _ { \mathrm { h } } \colon \mathrm { R } 0 - \mathrm { R } 9$  $\mathbf { A } _ { \mathrm { h } } - \mathrm { E } _ { \mathrm { h } } \colon \mathrm { R e s e r v e d }$  $\mathrm { F _ { h } } \mathrm { : }$ No lane remapping (default)</td></tr><tr><td rowspan=1 colspan=1>[19:16]</td><td rowspan=1 colspan=1>AWORD_CA[3:0]</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>Lane remapping applied to AWORD. $0 _ { \mathrm { h } } - 7 _ { \mathrm { h } } \mathrm { : C } 0 - \mathrm { C } 7$  $8 _ { \mathrm { h } } { : } \mathrm { A P A R }$ 9h: ARFU $\mathbf { A } _ { \mathrm { h } }$    $\operatorname { E } _ { \mathrm { h } } .$ Reserved $\mathrm { F _ { h } } \mathrm { : }$ No lane remapping (default)</td></tr></table>

## 13.5.15 SOFT\_LANE\_REPAIR and HARD\_LANE\_REPAIR (cont’d)

Table 136 — LANE\_REPAIR Wrapper Data Register (cont’d)
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>[15:12]</td><td rowspan=1 colspan=1>DWORD0_BYTE3[3:0]</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>Lane remapping applied to DWORD 0 byte 3 $0 _ { \mathrm { h } } \mathrm { { : S E V 1 } }$  $1 _ { \mathrm { h } } - 8 _ { \mathrm { h } } \colon \mathrm { D Q } 2 4 - \mathrm { D Q } 3 1$  $9 _ { \mathrm { h } } ; \mathrm { D B I } 3$  $\mathbf { A } _ { \mathrm { h } } - \mathrm { E } _ { \mathrm { h } } \colon \mathrm { R e s e r v e d }$  $\mathrm { F _ { h } } \mathrm { : N o }$ lane remapping (default)</td></tr><tr><td rowspan=1 colspan=1>[11:8]</td><td rowspan=1 colspan=1>DWORD0_BYTE2[3:0]</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>Lane remapping applied to DWORD0 byte 2 $0 _ { \mathrm { h } } \mathrm { { : S E V 0 } }$  $1 _ { \mathrm { h } } - 8 _ { \mathrm { h } } \colon \mathrm { D Q } 1 6 - \mathrm { D Q } 2 3$  $9 _ { \mathrm { h } } ; \mathrm { D B I } 2$  $\mathrm { A _ { h } } - \mathrm { E _ { h } } \mathrm { : R e s e r v e d }$  $\mathrm { F _ { h } } \mathrm { : N o }$ lane remapping (default)</td></tr><tr><td rowspan=1 colspan=1>[7:4]</td><td rowspan=1 colspan=1>DWORD0_BYTE1[3:0]</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>Lane remapping applied to DWORD0 byte 1 $0 _ { \mathrm { h } } \mathrm { { : E C C 1 } }$  $1 _ { \mathrm { h } } - 8 _ { \mathrm { h } } \colon { \mathrm { D Q } } 8 \AA - { \mathrm { D Q } } 1 5$  $9 _ { \mathrm { h } } ; \mathrm { D B I } 1$  $\mathrm { A _ { h } } - \mathrm { E _ { h } } \mathrm { : R e s e r v e d }$  $\mathrm { F _ { h } } \mathrm { : }$ No lane remapping (default)</td></tr><tr><td rowspan=1 colspan=1>[3:0]</td><td rowspan=1 colspan=1>DWORD0_BYTE0[3:0]</td><td rowspan=1 colspan=1>R/W</td><td rowspan=1 colspan=1>Lane remapping applied to DWORD0 byte 0 $0 _ { \mathrm { h } } \colon \mathrm { E C C } 0$  $1 _ { \mathrm { h } } - 8 _ { \mathrm { h } } \colon { \mathrm { D Q 0 } } - { \mathrm { D Q 7 } }$  $9 _ { \mathrm { h } } ; \mathrm { D B I 0 }$  $\mathrm { A _ { h } } - \mathrm { E _ { h } } \mathrm { : R e s e r v e d }$  $\mathrm { F _ { h } } \mathrm { : N o }$ lane remapping (default)</td></tr></table>

![](images/9e779ded17e9d2a8b6a52738304dfa6ef016f10799d23c8ff7a470a999a5e972.jpg)  
Figure 115 — Registers Associated with Lane Repair Instructions

## 13.5.16 CHANNEL\_DISABLE

This instruction disables one channel or all channels specified in WIR[13:8]. The instruction may only be issued after t timing has been met and only before the CK clock is started for the first time. The disabled channel will transition into a safe low-power state where they do not respond to commands. All AWORD and DWORD input and output buffers will be turned off, thus allowing all external signals to float. It will also not respond to EXTEST\_RX, EXTEST\_TX and CHANNEL\_ID instructions. Both RESET\_n and WRST\_n must be maintained HIGH during the all-channel disable state. The channel’s WSO output will remain active and drive a LOW.

The all-channel disable option shall be used during host-side HTOL and/or other reliability tests to prevent unintentional degradation of the HBM4 DRAM. This option may only be issued after tINIT3 timing has been met, before the CK clock is started for the first time after exit from reset state and only if no other IEEE1500 instruction other than BYPASS or DEVICE\_ID has been loaded before.

A disabled channel can be enabled again by pulling both RESET\_n and WRST\_n to LOW and following the procedure described in the Initialization Sequence with Stable Power clause.

## Wrapper Data Register

When CHANNEL\_DISABLE is the current instruction, the data register as shown in Figure 116.   
Table 137 is connected between WSI and WSO.

## CaptureWR

When CHANNEL\_DISABLE is the current instruction, the CaptureWR event will have no effect.

## UpdateWR

When CHANNEL\_DISABLE is the current instruction, the UpdateWR event will load the disable bit from the shift stage into the update stage of the WDR and asynchronously transition into a safe low power state when the bit is 1. Input and output buffers will be disabled latest after t<sub>CHDIS</sub>.

![](images/8871d572ade7aa8788810dd10d5a5e507a825d416800e48f96a27c69c1177368.jpg)  
Figure 116 — Channel Disable Instruction

## 13.5.16 CHANNEL\_DISABLE (cont’d)

Table 137 — CHANNEL\_DISABLE Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>[0]</td><td rowspan=1 colspan=1>CH_DIS</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>0 – Channel is enabled (default).Clearing the bit to 0 does not re-enable a channel.1 – Channel is disabled</td></tr></table>

## 13.5.17 CHANNEL TEMPERATURE

This instruction captures the channel’s junction temperature. Temperature reporting is specified as a 9-bit field per SID: the LSB indicates the validity of the temperature sensor read-out, and the remaining 8 bits indicate the temperature in degrees Celsius.

## Wrapper Data Register

When CHANNEL\_TEMPERATURE is the current instruction, the data register as shown in Table 138 is connected between WSI and WSO.

## CaptureWR

When CHANNEL\_TEMPERATURE is the current instruction, the CaptureWR event load the temperature field values into the shift stage of the WDR.

## UpdateWR

When CHANNEL TEMPERATURE is the current instruction, the UpdateWR event will have no effect.

## 13.5.17 CHANNEL TEMPERATURE (cont’d)

Table 138 — CHANNEL\_TEMPERATURE Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>[35:28]</td><td rowspan=1 colspan=1>CHANNEL SID3TEMP[7:0]</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>Maximum temperature per channel for SID3 in Degrees Celsius.Same encoding as in CHANNEL_SID0_TEMP[7:0]</td></tr><tr><td rowspan=1 colspan=1>[27]</td><td rowspan=1 colspan=1>CHANNEL_ SID3VALID</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>Channel Temperature sensor output valid for SID30 – Invalid1 - Valid</td></tr><tr><td rowspan=1 colspan=1>[26:19]</td><td rowspan=1 colspan=1>CHANNEL SID2TEMP[7:0]</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>Maximum temperature per channel for SID2 in Degrees Celsius.Same encoding as in CHANNEL SID0 TEMP[7:0]</td></tr><tr><td rowspan=1 colspan=1>[18]</td><td rowspan=1 colspan=1>CHANNEL_SID2VALID</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>Channel Temperature sensor output valid for SID20 – Invalid1 - Valid</td></tr><tr><td rowspan=1 colspan=1>[17:10]</td><td rowspan=1 colspan=1>CHANNEL SID1TEMP[7:0]</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>Maximum temperature per channel for SID1 in Degrees Celsius.Same encoding as in CHANNEL SID0 TEMP[7:0]</td></tr><tr><td rowspan=1 colspan=1>[9]</td><td rowspan=1 colspan=1>CHANNEL_SID1VALID</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>Channel Temperature sensor output valid for SID10 – Invalid1 – Valid</td></tr><tr><td rowspan=1 colspan=1>[8:1]</td><td rowspan=1 colspan=1>CHANNEL_SID0TEMP[7:0]</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>Maximum temperature per channel for SID0 in Degree Celsius.Examples:8&#x27;b $0 \bar { 0 } 0 0 0 0 0 0 0 = - 4 0 { } ^ { \circ } \mathrm { C }$ 8&#x27;b 0010 1000 = 0 ℃ $8 ^ { \bullet } \mathbf { b } 0 1 0 0 0 0 0 1 = 2 5 ^ { \circ } \mathbf { C }$  $8 ^ { \circ } \mathbf { b } \ 1 0 1 0 \ 0 1 1 1 = 1 2 7 ^ { \circ } \mathbf { C }$ </td></tr><tr><td rowspan=1 colspan=1>[0]</td><td rowspan=1 colspan=1>CHANNEL SID0VALID</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>Channel Temperature sensor output valid for SID00- Invalid1-Valid</td></tr><tr><td rowspan=1 colspan=4>NOTE 1For unsupported SID fields the HBM4 DRAM will report the sensor output as invalid and the temperature as allzeros.NOTE 2 Device may report the same maximum temperature value for all the channels within the same core-die orindividual channel temperatures based on number of unique temperature sensors (Figure 117).NOTE 3 If a channel is distributed across multiple dies (within the same ŠID), as shown in Figure 118, the device reportsthe maximum channel temperature value between the core-dies across which the channel is distributed.</td></tr></table>

## 13.5.17 CHANNEL TEMPERATURE (cont’d)

![](images/aa293eddbddd14b2d8aa12a6429155cbd49f0e8f8985c492c05677d17d6a77aa.jpg)  
Figure 117 — Example Channel Configuration 1

![](images/768466577ce10212e6807a99c5cb34a0841aec5836e7eb71b74804c3ae1a075d.jpg)  
Figure 118 — Example Channel Configuration 2

## 13.5.18 WOSC\_RUN and WOSC\_COUNT

The WOSC\_RUN and WOSC\_COUNT instructions are associated with the WDQS Interval Oscillator in the HBM4 DRAM.

## Wrapper Data Register

When WOSC\_RUN is the current instruction, the WOSC\_RUN wrapper data register as shown in Table 139 is connected between WSI and WSO[31:0], and the WSO outputs of all active channels drive the same data during ShiftWR events.

When WOSC\_COUNT is the current instruction, the WOSC\_COUNT wrapper data register as shown in Table 140 is connected between WSI and WSO[31:0], and the WSO outputs of all active channels drive the same data during ShiftWR events.

## CaptureWR

When WOSC\_RUN is the current instruction, the CaptureWR event will have no effect.

When WOSC\_COUNT is the current instruction, the CaptureWR event will load the WDQS oscillator count value into the shift stage of the WDR and update the WOSC\_COUNT\_VALID field of the WDR.

## UpdateWR

When WOSC\_RUN is the current instruction, the UpdateWR event will load the value from the shift stage into the update stage and start or stop the WDQS Interval Oscillator.

When WOSC\_COUNT is the current instruction, the UpdateWR event will have no effect.

Table 139 — WOSC\_RUN Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>[0]</td><td rowspan=1 colspan=1>WOSC START STOP</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>0 – Stop WDQS Interval Oscillator (default)1 – Start WDQS Interval Oscillator</td></tr></table>

Table 140 — WOSC\_COUNT Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>[24:1]</td><td rowspan=1 colspan=1>WOSC COUNT VALUE</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>Oscillator count value.Range 0 to 224-1</td></tr><tr><td rowspan=1 colspan=1>[0]</td><td rowspan=1 colspan=1>WOSC COUNT VALID</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>0 – Count is invalid (default)1 – Count is valid</td></tr><tr><td rowspan=1 colspan=4>NOTE 1The WDQS oscillator count value is used to train WDQS to the data valid window. The value reported in thisWDR can be used by the memory controller to periodically adjust the phase of WDQS relative to data.NOTE2The contents of bits [23:0] is reset by starting the oscillator.</td></tr></table>

## 13.5.19 ECS Error Log

This instruction is used to capture ECS Error Log information reading from the WDR. The registers in this instruction are associated with the Error type and Error address (position) as the ECS operation result during ECS period. The error types are NE, CE<sub>S</sub>, CE<sub>M</sub>, UE. The encoding of error types is the same as burst position 4\~7 of severity transmission in Table 68. See clause on Error Check and Scrub (ECS). HBM4 device will store detailed information about errors detected during ECS operation period. The latest logging information will follow priority update rule in the following order such as UE, CE<sub>M</sub>, CE<sub>S</sub>, NE of Table 65. In case of CE<sub>S</sub>, error information would be logged in HBM4 for host-polling when #ERRECS during current or previous ECS period is larger than the #ERRTH, where the #ERRECS means accumulated the number of errors events detected during previous ECS period, not the number of error bits. At this time the error address will be logged and readout through IEEE1500 WSO. The logged ECS error information is either cleared manually by the host using ECSRES mode register (MR9 OP7) or if ECSLOG mode register (MR8 OP2) is enabled when the log is read out. See the ECS clause for more details.

## Wrapper Data Register

When the ECS Error Log instruction is updated the data register as shown in Table 141 is connected between WSI and WSO.

## CaptureWR

When ECS Error Log is the current instruction, the CaptureWR event will load the respective error log field values into the shift stage of the WDR.

## UpdateWR

When ECS Error Log is the current instruction, the UpdateWR event will have no effect.

## 13.5.19 ECS Error Log (cont’d)

Table 141 — ECS Error Log Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>[215:190]</td><td rowspan=1 colspan=1>SID3 PC1 ECS[25:0]</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>ECS error log for SID3, PC1Same encoding as in SID0_PC0_ECS</td></tr><tr><td rowspan=1 colspan=1>[189]</td><td rowspan=1 colspan=1>SID3 PC1 ECS VALID</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>ECS error log valid of SID3, PC1Same encoding as in SID0 PC0 ECS VALID</td></tr><tr><td rowspan=1 colspan=1>[188:163]</td><td rowspan=1 colspan=1>SID3 PC0 ECS[25:0]</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>ECS error log for SID3, PC0Same encoding as in SID0 PCO ECS</td></tr><tr><td rowspan=1 colspan=1>[162]</td><td rowspan=1 colspan=1>SID3 PC0 ECS VALID</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>ECS error log valid of SID3, PC0Same encoding as in SID0_PC0_ECS_VALID</td></tr><tr><td rowspan=1 colspan=1>[161:136]</td><td rowspan=1 colspan=1>SID2_PC1_ECS[25:0]</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>ECS error log for SID2, PC1Same encoding as in SID0 PCO ECS</td></tr><tr><td rowspan=1 colspan=1>[135]</td><td rowspan=1 colspan=1>SID2 PC1 ECS VALID</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>ECS error log valid of SID2, PC1Same encoding as in SID0_PC0_ECS_VALID</td></tr><tr><td rowspan=1 colspan=1>[134:109]</td><td rowspan=1 colspan=1>SID2_PC0_ECS[25:0]</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>ECS error log for SID2, PC0Same encoding as in SID0_PC0_ECS</td></tr><tr><td rowspan=1 colspan=1>[108]</td><td rowspan=1 colspan=1>SID2 PC0 ECS VALID</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>ECS error log valid of SID2, PC0Same encoding as in SID0 PC0 ECS VALID</td></tr><tr><td rowspan=1 colspan=1>[107:82]</td><td rowspan=1 colspan=1>SID1 PC1 ECS[25:0]</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>ECS error log for SID1, PC1Same encoding as in SID0_PC0_ECS</td></tr><tr><td rowspan=1 colspan=1>[81]</td><td rowspan=1 colspan=1>SID1 PC1 ECS VALID</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>ECS error log valid of SID1, PC1Same encoding as in SID0 PC0 ECS VALID</td></tr><tr><td rowspan=1 colspan=1>[80:55]</td><td rowspan=1 colspan=1>SID1 PC0 ECS[25:0]</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>ECS error log for SID1, PC0Same encoding as in SID0 PCO ECS</td></tr><tr><td rowspan=1 colspan=1>[54]</td><td rowspan=1 colspan=1>SID1 PC0 ECS VALID</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>ECS error log valid of SID1, PC0Same encoding as in SID0 PC0 ECS VALID</td></tr><tr><td rowspan=1 colspan=1>[53:28]</td><td rowspan=1 colspan=1>SID0 PC1 ECS[25:0]</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>ECS error log for SID0, PC1Same encoding as in SID0 PC0 ECS</td></tr><tr><td rowspan=1 colspan=1>[27]</td><td rowspan=1 colspan=1>SID0 PC1 ECS VALID</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>ECS error log valid of SID0, PC1Same encoding as in SID0_PC0_ECS_VALID</td></tr><tr><td rowspan=1 colspan=1>[26:1]</td><td rowspan=1 colspan=1>SID0 PC0 ECS[25:0]</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>ECS error log for SID0, PC0[25:22] – Bank address BA[3:0][21:7] – Row address RFU, RA[13:0]1[6:2] – Column address CA[4:0][1:0] – Error Type[1:0]00b: NE01b: CEs10b: UE11b: CEm</td></tr><tr><td rowspan=1 colspan=1>[0]</td><td rowspan=1 colspan=1>SID0 PC0 ECS VALID</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>ECS error log valid for SID0, PC00 – Invalid (default)1 – Valid</td></tr><tr><td rowspan=1 colspan=4>NOTE 1 ECS error log includes an additional bit to support future row addressing, i.e., RA14.</td></tr></table>

## 13.5.20 HS\_REP\_CAP

The HS\_REP\_CAP instruction tells the host whether a bank(s) has resources for either hard repair or soft repair. For each bank of the DRAM, the Gray-coded encoding indicates whether there are no resources, 1 resource or 2 or more resources.

This instruction shall be used by the host before performing any hard of soft repair. This register will be updated with the completion of a hard repair only. The DRAM may also share resources with self repair. In this case the completion of self repair will also update this register. The sharing of resources between hard/soft repair and self repair is vendor specific and identified in the SHARED\_REP\_RES field of the DEVICE\_ID.

## Wrapper Data Register

When HS\_REP\_CAP is the current instruction, the wrapper data register as shown in Table 142 is connected between WSI and WSO.

## CaptureWR

When HS\_REP\_CAP is the current instruction, the CaptureWR event will load the resource field value into the shift stage register.

## UpdateWR

When HS\_REP\_CAP is the current instruction, the UpdateWR event will have no effect.

Table 142 — HS\_REP\_CAP Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=2>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>[255:192]</td><td rowspan=1 colspan=2>HS REPAIR RES SID3</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>SID3 PC0 Banks [15:0] and PC1 Banks [15:0]</td></tr><tr><td rowspan=1 colspan=1>[191:128]</td><td rowspan=1 colspan=2>HS REPAIR RES SID2</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>SID2 PC0 Banks [15:0] and PC1 Banks [15:0]</td></tr><tr><td rowspan=1 colspan=1>[127:64]</td><td rowspan=1 colspan=2>HS REPAIR RES SID1</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>SID1 PC0 Banks [15:0] and PC1 Banks [15:0]</td></tr><tr><td rowspan=1 colspan=1>[63:32]</td><td rowspan=3 colspan=2>HS REPAIR RES SID0</td><td rowspan=3 colspan=1>R</td><td rowspan=1 colspan=1>SID0 PC1 Banks [15:0]</td></tr><tr><td rowspan=1 colspan=1>[31:2]</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>SID0 PC0 Banks [15:1]</td></tr><tr><td rowspan=1 colspan=1>[1:0]</td><td rowspan=1 colspan=1>Resources available for SID0 PC0 Bank 000b: No resource available01b: 1 resource10: Reserved11: 2 or more resources</td></tr></table>

## 13.5.21 SELF\_REP and SELF\_REP\_RESULTS

The SELF\_REP and SELF\_REP\_RESULTS instructions are associated with HBM4 self repair.

## Wrapper Data Register

When SELF\_REP is the current instruction, the SELF\_REP wrapper data register as shown in Table 143 is connected between WSI and WSO.

When SELF\_REP\_RESULTS is the current instruction, the SELF\_REP\_RESULTS wrapper data register as shown in Table 144 is connected between WSI and WSO.

## CaptureWR

When SELF\_REP is the current instruction, the CaptureWR event will capture the SR\_PROGRESS to the shift stage register.

When SELF\_REP\_RESULTS is the current instruction, the CaptureWR event will capture the SID[3:0]\_RESULTS to the shift stage register.

## UpdateWR

When SELF\_REP is the current instruction, the UpdateWR event will copy the SELFR\_REF\_RATE, SID-SELECT and REP\_TYPE into the update stage register.

When SELF\_REP\_RESULTS is the current instruction, the UpdateWR event will have no effect.

## 13.5.21 SELF\_REP and SELF\_REP\_RESULTS (cont’d)

Table 143 — SELF\_REP Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>[8]</td><td rowspan=1 colspan=1>SHARED OVERRIDE²</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1> $0 _ { \mathrm { b } } \mathrm { : }$ DRAM must leave 1 resource when resources shared(default)1b: DRAM can use all resources for Self-repair whenshared</td></tr><tr><td rowspan=1 colspan=1>[7:6]</td><td rowspan=1 colspan=1>SELFR REP RATE</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { { b } } } \colon$ 1 x tREFI $0 1 _ { \mathrm { b } } \mathrm { : }$ 0.5 x tREFI $1 0 _ { \mathrm { b } } \mathrm { : }$ 0.25 x tREFI $1 1 _ { \mathrm { b } } \mathrm { : }$ Reserved</td></tr><tr><td rowspan=1 colspan=1>[5:4]</td><td rowspan=1 colspan=1>SID SELECT</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1> $0 0 \mathrm { { b } ; }$ SID0 $0 1 _ { \mathrm { b } } \mathrm { : }$ SID1 $1 0 _ { \mathrm { b } } \mathrm { : }$ SID2 $1 1 _ { \mathrm { b } } \mathrm { : }$ SID3</td></tr><tr><td rowspan=1 colspan=1>[3:2]</td><td rowspan=1 colspan=1>REP TYPE</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1> $1 1 _ { \mathrm { b } } \mathrm { : }$ Run self-test and auto-repair $1 0 _ { \mathrm { b } } \mathrm { : }$ Auto-repair only $0 1 _ { \mathrm { b } } \mathrm { : }$ Run self-test only and no auto-repair $0 0 \mathrm { { b } ; }$ Disabled/Cancel¹</td></tr><tr><td rowspan=1 colspan=1>[1:0]</td><td rowspan=1 colspan=1>SR PROGRESS</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1> $0 0 _ { \mathrm { { b } } } \colon$ Not running (default) $0 1 _ { \mathrm { b } } \mathrm { : }$ Self-test in progress $1 0 _ { \mathrm { b } } \mathrm { : }$ Auto-repair in progress $1 1 _ { \mathrm { b } } \mathrm { : }$ Complete</td></tr><tr><td rowspan=1 colspan=4>NOTE 1 Cancel will only stop the SELF_REPAIR when the self-test is in progress (SR_PROGRESS = 01b) andSR_PROGRESS is set to 00b (not running) after cancel.NOTE 2 When resources are shared between self and hard/soft repair the SHARED_OVERRIDE field allows the DRAM touse all the resources for self repair. When the resources are not shared the field is do not care.</td></tr></table>

Table 144 — SELF\_REP\_RESULTS Wrapper Data Register
<table><tr><td rowspan=1 colspan=1>BitPosition</td><td rowspan=1 colspan=1>Bit Field</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>[7:6]</td><td rowspan=1 colspan=1>SID3 RESULTS</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>SID3 SELF REP results</td></tr><tr><td rowspan=1 colspan=1>[5:4]</td><td rowspan=1 colspan=1>SID2 RESULTS</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>SID2 SELF REP results</td></tr><tr><td rowspan=1 colspan=1>[3:2]</td><td rowspan=1 colspan=1>SID1 RESULTS</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>SID1 SELF REP results</td></tr><tr><td rowspan=1 colspan=1>[1:0]</td><td rowspan=1 colspan=1>SID0 RESULTS</td><td rowspan=1 colspan=1>R</td><td rowspan=1 colspan=1>SID0 SELF REP results00: SELF REP test has not run since INIT or Nofails remain after most recent run $0 1 \mathrm { { b } \mathrm { { : } } }$ Fail(s) remain $1 0 _ { \mathrm { b } } \mathrm { : }$ Unrepairable fail(s) remain $1 1 { \mathrm { _ { b } } } { \mathrm { : } }$ SELF REP should be run again</td></tr><tr><td rowspan=1 colspan=4>NOTE 1 For unsupported SID fields, the DRAM will report the results as 00b (SELF-REPAIR test has not run).NOTE 2 DRAM may report the same SELF_REP_RESULTS value for up to 16 channels, 8 channels or individual channelresults as defined in Table 118 — WIR Channel Selection Definition.</td></tr></table>

## 13.6 Interaction with Mission Mode Operation

Table 145 defines the interaction of the various IEEE1500 instructions with mission mode operation, and any instruction exit requirements (see also Table 120 for all IEEE1500 instructions).

Table 145 — IEEE1500 Port Instruction Interactions
<table><tr><td rowspan=1 colspan=1>Instruction</td><td rowspan=1 colspan=1>Interaction withMission Mode</td><td rowspan=1 colspan=1>Post InstructionRequirements</td></tr><tr><td rowspan=1 colspan=1>BYPASSDWORD MISRAWORD MISRREAD LFSR COMPARE STICKY1DEVICE IDTEMPERATUREMODE REGISTER DUMP SET (dump)CHANNEL TEMPERATUREWOSC RUNWOSC COUNTECS ERROR LOGSELF REP RESULTSHS REP CAP</td><td rowspan=1 colspan=1>Instructions may be used at anytime.Core memory content is retainedif refresh specifications are met.1</td><td rowspan=1 colspan=1>None</td></tr><tr><td rowspan=1 colspan=1>SOFT REPAIR2, 5SOFT LANE REPAIR²MODE REGISTER_DUMP_SET (set)AWORD MISR CONFIG³</td><td rowspan=1 colspan=1>Core memory content is retainedif refresh specifications are met.</td><td rowspan=1 colspan=1>Meet IEEE1500 Port ACTimings(see Table 146)</td></tr><tr><td rowspan=1 colspan=1>EXTEST RX, EXTEST TXMBISTCHANNEL IDHARD REPAIR⁴HARD LANE REPAIR⁴CHANNEL DISABLE⁶SELF REP⁴4</td><td rowspan=1 colspan=1>HBM4 interface state and corememory content are not defined.</td><td rowspan=1 colspan=1>Reset</td></tr><tr><td rowspan=1 colspan=3>NOTE 1While accessing these MISR-related registers has no interaction with mission mode, operating the AWORD andDWORD MISR modes may result in memory content loss unless the channel is put into self refresh mode. SeeHBM4 Loopback Test Modes clause.NOTE 2Soft memory array and lane repairs imply that memory content is at least partially incorrect. While the HBM4DRAM imposes no restrictions on the interface state and memory content, the host should consider the health ofThe memory content based on the repair(s) being applied.NOTE 3 See HBM4 Loopback Test Modes for proper sequencing of the AWORD MISR test modes.NOTE 4Self/Hard memory array and hard lane repairs involve blowing fuses. Normal operation on any channel is notsupported when the self/hard repair operations are used. A chip reset with RESET_n pulled LOW is required afterself/hard repair operations before returning the HBM4 DRAM to normal operation.NOTE 5For SOFT_REPAIR it is required that the channel is held in bank idle state from the time when the SOFT_REPAIRinstruction is loaded in the WIR until the SOFT REPAIR instruction is unloaded.NOTE 6 In case of all channel operation, refer to CHANNEL_DISABLE instruction for conditions to re-enable a disabledchannel.</td></tr></table>

## 13.7 IEEE1500 Test Port AC Timing Parameters

Table 146 — IEEE1500 Test Port AC Timings
<table><tr><td rowspan=2 colspan=1>Parameter</td><td rowspan=2 colspan=1>Symbol</td><td rowspan=1 colspan=2>Values</td><td rowspan=2 colspan=1>Unit</td><td rowspan=2 colspan=1>Notes</td></tr><tr><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td></tr><tr><td rowspan=1 colspan=6>IEEE1500 Port I/O Timings</td></tr><tr><td rowspan=1 colspan=1>WRCK clock period</td><td rowspan=1 colspan=1>tcKTP</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>–</td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>WRCK clock high pulse width</td><td rowspan=1 colspan=1>tCKTPH</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>一</td><td rowspan=1 colspan=1>tCKTP</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>WRCK clock low pulse width</td><td rowspan=1 colspan=1>tCKTPL</td><td rowspan=1 colspan=1>0.45</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>tcKTP</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>WRST_n pulse width low</td><td rowspan=1 colspan=1>twRSTL</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>IEEE1500 port operation after WRST_n deassertion</td><td rowspan=1 colspan=1>tWINIT1</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>tcKTP</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Rising WRST_n edge to WRCK setup time</td><td rowspan=1 colspan=1>tsWRST</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>WSP input setup time to WRCK rising edge</td><td rowspan=1 colspan=1>tsR</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>WSP input hold time from WRCK rising edge</td><td rowspan=1 colspan=1>tHR</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>WSP input setup time to WRCK falling edge</td><td rowspan=1 colspan=1>tsF</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>WSP input hold time from WRCK falling edge</td><td rowspan=1 colspan=1>tHF</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>WSO output valid time from WRCK falling edge</td><td rowspan=1 colspan=1>tovwso</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=3>EXTEST_RX Instruction Related Timings</td><td rowspan=1 colspan=3></td></tr><tr><td rowspan=1 colspan=1>Input setup time to WRCK rising edge         ■</td><td rowspan=1 colspan=1>tsEXT</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>6</td></tr><tr><td rowspan=1 colspan=1>Input hold time from WRCK rising edge</td><td rowspan=1 colspan=1>tHEXT</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>6</td></tr><tr><td rowspan=1 colspan=6>EXTEST_TX Instruction Related Timings</td></tr><tr><td rowspan=1 colspan=1>Output valid time from WRCK rising edge</td><td rowspan=1 colspan=1>tOVEXT</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>7</td></tr><tr><td rowspan=1 colspan=6>HBM4_RESET Instruction Related Timings</td></tr><tr><td rowspan=1 colspan=1>HBM_RESET instruction minimum active time</td><td rowspan=1 colspan=1>tRES</td><td rowspan=1 colspan=1>tpW_RESET</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>8</td></tr><tr><td rowspan=1 colspan=6>SOFT_REPAIR and HARD_REPAIR Instruction Related Timings</td></tr><tr><td rowspan=1 colspan=1>SOFT_REPAIR minimum waiting time</td><td rowspan=1 colspan=1>tsREP</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>–</td><td rowspan=1 colspan=1>ns, µs ornWRCK</td><td rowspan=1 colspan=1>9</td></tr><tr><td rowspan=1 colspan=1>HARD_REPAIR minimum waiting time</td><td rowspan=1 colspan=1>tHREP</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns, µs ornWRCK</td><td rowspan=1 colspan=1>10</td></tr><tr><td rowspan=1 colspan=6>DWORD_MISR and AWORD_MISR Instruction Related Timings</td></tr><tr><td rowspan=1 colspan=1>DWORD and AWORD MISR data capture to WDRdata capture delay</td><td rowspan=1 colspan=1>tsMISR</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>11</td></tr><tr><td rowspan=1 colspan=6>CHANNEL_ID Instruction Related Timings</td></tr><tr><td rowspan=1 colspan=1>Output high time from WRCK falling edge</td><td rowspan=1 colspan=1>tOVCHN</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>12</td></tr><tr><td rowspan=1 colspan=1>Output return to default state delay</td><td rowspan=1 colspan=1>tOZCHN</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>ns</td><td rowspan=1 colspan=1>13</td></tr></table>

Table 146 — IEEE1500 Test Port AC Timings (cont’d)
<table><tr><td rowspan="2">Parameter</td><td rowspan="2">Symbol</td><td colspan="2">Values</td><td rowspan="2">Unit</td><td rowspan="2">Notes</td></tr><tr><td>Min</td><td>Max</td></tr><tr><td colspan="7">Mode_Register_Dump_Set Instruction Related Timings</td></tr><tr><td>WDR update to Mode Register valid delay</td><td>tUPDMRS</td><td></td><td></td><td>ns</td><td>14</td></tr><tr><td>MRS command to WDR data capture delay</td><td>tMRSS</td><td>tMOD</td><td></td><td>nCK</td><td>15</td></tr><tr><td colspan="6">AWORD_MISR_CONFIG Instruction Related Timings</td></tr><tr><td>AWORD MISR configuration to MISR operation delay</td><td>tCMISR</td><td></td><td></td><td>ns</td><td>16</td></tr><tr><td colspan="6">SOFT_LANE_REPAIR and HARD_LANE_REPAIR Instruction Related Timings</td></tr><tr><td>SOFT_LANE_REPAIR minimum waiting time</td><td>tsLREP</td><td></td><td></td><td>ns or μs</td><td>17</td></tr><tr><td>HARD LANE REPAIR minimum waiting time</td><td>tHLREP</td><td></td><td></td><td>ns or µs</td><td>18</td></tr><tr><td colspan="6">CHANNEL_DISABLE Instruction Related Timing</td></tr><tr><td>Channel disable to input and output buffer disable delay</td><td>tCHDIS</td><td></td><td></td><td>ns or µs</td><td>19</td></tr><tr><td colspan="6">SELF_REPAIR Instruction Related Timings</td></tr><tr><td colspan="2">Self-test and Auto-repair test time</td><td colspan="2">tsELF_HEAL</td><td>S</td><td>20</td></tr><tr><td colspan="2">Auto-repair test time</td><td colspan="2">tsELF REP 1</td><td>S</td><td>20</td></tr><tr><td colspan="2">Self-test test time</td><td colspan="2">tsELF_NR</td><td>S</td><td>20</td></tr><tr><td colspan="2">Self-test cancel time</td><td colspan="2">tsELF_CANCEL –</td><td>μs</td><td>20</td></tr><tr><td colspan="6">AC timing parameters apply to each channel of the HBM4 device independently except for timings related to IEEE1500 input pins that are common to all channels. No timing parameters are specified across channels, and all</td></tr><tr><td>NOTE 1 channels operate independently of each other. NOTE 2 All parameters assume proper device initialization. Parameter applies to WSI, SelectWIR, ShiftWR, and CaptureWR inputs. Parameter applies to Update WR input.</td><td colspan="5">Parameter applies to WSO output changes resulting from Wrapper Instruction Register (WIR), Wrapper Bypass</td></tr><tr><td>NOTE 3 NOTE 4 NOTE 5</td><td colspan="5"></td></tr><tr><td>NOTE 6</td><td colspan="5">Register (WBY) or any Wrapper Data Register (WDR) shift operation. Parameter applies to all HBM4 inputs and bidirectional IOs in the CaptureWR cycle when the active instruction is EXTEST_RX.</td></tr><tr><td>NOTE 7 NOTE 8</td><td colspan="3">Parameter applies to all HBM outputs and bidirectional IOs in the ShiftWR cycle when the active instruction is EXTEST_TX. Parameter applies when the active instruction is HBM_RESET; it is measured from either the falling WRCK edge that loads the HBM_RESET instruction in the UpdateWIR cycle (in case no WDR is associated with the</td><td></td><td></td></tr><tr><td></td><td colspan="5">instruction) or the falling WRCK edge that sets the WDR bit to 1’ in the UpdateWR cycle (in case a WDR is associated with the instruction) until either the HBM_RESET instruction is invalidated or the WDR bit is set back</td></tr><tr><td>NOTE 9</td><td colspan="3">to 0’. The minimum value equals the RESET_n minimum low time with stable power (tPw_REsET). Parameter applies when the active instruction is SOFT_REPAIR; it describes the minimum time for the HBM4</td><td></td><td></td></tr><tr><td>NOTE 10</td><td colspan="3">device to perform the internal soft repair; it is measured from the falling WRCK edge that loads the repair vector and repair start bit in the UpdateWR cycle until the instruction is invalidated. Parameter applies when the active instruction is HARD_REPAIR; it describes the minimum time for the HBM4</td><td></td><td></td></tr><tr><td></td><td colspan="3">device to perform the internal hard repair; it is measured from the falling WRCK edge that loads the repair vector</td><td></td><td></td></tr><tr><td>NOTE 11</td><td colspan="3">and repair start bit in the UpdateWR cycle until the instruction is invalidated. Parameter applies when the active instruction is DWORD_MISR or AWORD_MISR; it is measured from the last CK clock that updates the data in the respective MISR until the rising WRCK edge associated with the CaptureWR</td><td></td><td></td></tr></table>

<table><tr><td>NOTE 12</td><td>Parameter applies when the active instruction is CHANNEL_ID; it describes the maximum duration from either the falling WRCK edge that sets the CHANNEL ID instruction in the UpdateWIR cycle (when no WDR is associated with the instruction) or the falling WRCK edge in the UpdateWR cycle that sets the enable bit in the WDR to 1’ (when a WDR is associated with the instruction) until the bidirectional IOs drive a High.</td></tr><tr><td>NOTE 13</td><td>Parameter applies when the active instruction is CHANNEL_ID; it describes the maximum duration from either the falling WRCK edge that sets any instruction other than CHANNEL_ID instruction in the UpdateWIR cycle (when no WDR is associated with the instruction) or the falling WRCK edge in the UpdateWR cycle that sets the enable bit in the WDR to 0’ (when a WDR is associated with the instruction) until the bidirectional IOs return to their default state.</td></tr><tr><td></td><td>NOTE 14 Parameter applies when the active instruction is MODE_REGISTER_DUMP_SET; it describes the minimum required delay between the falling WRCK edge in the UpdateWR cycle that loads the Mode Registers from the WDR shift register until any valid command other than RNOP and CNOP can be issued at the command interface.</td></tr><tr><td>NOTE 15 NOTE 16</td><td>Parameter applies when the active instruction is MODE REGISTER DUMP SET; it describes the minimum required delay between the last MRS command that loads any Mode Register and the rising WRCK edge in the CaptureWR cycle that copies the Mode Register content into the WDR shift register. Parameter applies when the active instruction is AWORD_MISR_CONFIG; it describes the minimum required</td></tr><tr><td></td><td>delay between the falling WRCK edges in the UpdateWR cycle that loads the AWORD MISR configuration until the MISR configuration is valid for any subsequent AWORD or DWORD MISR operation in the CK clock domain.</td></tr><tr><td>NOTE 17</td><td>Parameter applies when the active instruction is SOFT_LANE_REPAIR; it describes the minimum time for the HBM4 device to perform the internal soft lane repair; it is measured from the falling WRCK edge that loads the repair vector in the UpdateWR cycle until the instruction is invalidated. 3 Parameter applies when the active instruction is HARD LANE_REPAIR; it describes the minimum time for the</td></tr><tr><td>NOTE 18</td><td>HBM4 device to perform the internal hard lane repair; it is measured from the falling WRCK edge that loads the repair vector in the UpdateWR cycle until the instruction is invalidated.</td></tr><tr><td>NOTE 19</td><td>Parameter applies when the active instruction is CHANNEL DISABLE; it describes the minimum waiting time for disabling the channel&#x27;s input and output buffers after the UpdateWR event that sets the CHANNEL_DISABLE</td></tr><tr><td>NOTE 20</td><td>WDR to 1. Parameter represents the maximum time the operation will take to complete and therefore the minimum time the host must wait.</td></tr></table>

## 13.7 IEEE1500 Test Port AC Timing Parameters (cont’d)

![](images/b11a88f8b4d07fd14426376a8844884cf6aa33b852332adde3fa5ccd0e211c65.jpg)  
Figure 119 — IEEE1500 Port Input and Output Timings

![](images/88ba5fe2c293def65138664ada6377dcf517a5d33b0bee889ce38cbd7e4069c0.jpg)

![](images/70b92b1fd0c3a19f89f9e39285a881fe9bf8aed81bad2b1f0183ebbbbd8cafd6.jpg)  
Figure 120 — IEEE1500 EXTEST\_RX and EXTEST\_TX Instruction Related Timings

![](images/a1306343327b046718caace3494e35a85c59a22fc0aa45b83b2cc2ec6e518638.jpg)  
Figure 121 — IEEE1500 SOFT\_REPAIR and HARD\_REPAIR Instruction Related Timings

## 13.7 IEEE1500 Test Port AC Timing Parameters (cont’d)

![](images/9727b66dad3343c7a748725d354c8f07d629c6917723cd79b0ea81099e80c4c3.jpg)  
Figure 122 — IEEE1500 Soft\_Lane\_Repair and Hard\_Lane\_Repair Instruction Related Timings

![](images/39eb6885163ebcbbce8be2a49f52758a5a1bb727036bb8d2ae76585898d86b35.jpg)  
NOTE 1 Same timings for data inputs and DWORD MISR with DWORD\_MISR instruction. NOTE 2 tOVWSO = 0 for illustration purpose.

Figure 123 — IEEE1500 DWORD\_MISR / AWORD\_MISR Instruction Related Timings  
![](images/72d7d98acc8441450cd271a380a6ba87a370b41a0b4666d8e8b5c6c01e556580.jpg)  
NOTE 1 tOVCHN and tOZCHN refer to set/reset of the Enable bit in the WDR.  
Figure 124 — IEEE1500 CHANNEL\_ID Instruction Related Timings

![](images/b45937a8f01d4fc5c0f09fe3bf18640d86130c5269798ae94329b38d2871af6d.jpg)  
A.C. = any command allowed in bank idle state.

Figure 125 — IEEE1500 MODE\_REGISTER\_DUMP\_SET Instruction Related Timings

## 13.8 Boundary Scan

The HBM4 DRAM supports a boundary scan chain per channel via the IEEE1500 test port. The boundary scan operation is associated with IEEE1500 test port instructions EXTEST\_RX and EXTEST\_TX.

Scan data is shifted in through WSI and out through the respective WSO, based on the active channel selections in the WIR (see Table 118). All functional pins are included in the boundary scan chains. Table 122 lists the micro-bump boundary scan chain order. Bit position 0 is the first bit shifted in on WSI and out on the WSOs.

The boundary scan chain length for all channels is 120 bits (see Table 122), with dummy WDR bit padding as needed on the MSB end of the chains. Matched length boundary scan chains allow all channel chains to be loaded with matching data with one shift operation when WIR[13:8] =3F<sub>h</sub>.

All input-only and output-only pins are implemented as bi-directionals to aid in SIP package level testing and fault isolation. Effectively, all pins support both EXTEST\_RX and EXTEST\_TX instructions.

I/O signals power up in input mode by default. As soon as EXTEST\_TX becomes the current instruction, the I/Os will change to output mode, and the outputs will drive the values shifted into the WDR shift stage.

When EXTEST\_RX is the current instruction, all functional pins of the selected channel(s) enter a High-Z state, including the output-only pins AERR, DERR, and RDQS\_t/RDQS\_c. On a subsequent CaptureWR event, the pins will capture the input values into the WDR shift stage.

Boundary scan mode entry may be asserted at any time after device initialization and before normal memory operation has commenced, e.g., before the CK clock has started to toggle. Upon exiting the scan mode, the state of the HBM4 DRAM is unknown and the integrity of the data content of the memory array is not guaranteed and therefore the reset initialization sequence is required before returning to normal operation.

## Annex A — (Informative) Difference between Document Revisions

This table briefly describes the changes from JESD270-4 to JESD270-4A. If the change to a concept involves any words added or deleted (excluding deletion of accidentally repeated words), it is included. Some punctuation changes are not included.

## A.1 Differences between JESD270-4A and JESD270-4 (April 2025)

<table><tr><td rowspan=1 colspan=1>Page(s)</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Corrections: Figure 2</td></tr><tr><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>Table 9: Add per-PC VrefD feature, relevant notes on describing per-PC VrefD</td></tr><tr><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1>Table 25: Add notes to represents per-PC VrefD on MR14, Add (PC0)’ to tell itis dependant to supporting optional features</td></tr><tr><td rowspan=1 colspan=1>31</td><td rowspan=1 colspan=1>Table 29: Add per-PC VrefD on MR18, Adjust RFU, add hyperlink</td></tr><tr><td rowspan=1 colspan=1>45</td><td rowspan=1 colspan=1>Corrections: Figure 17</td></tr><tr><td rowspan=1 colspan=1>65, 67, 68</td><td rowspan=1 colspan=1>Clause 6.3.2.5.5: Add a text to add a clarity of enable/disable DRFM, its timingrelationships                                   1Table 41 added: to deliver timing relationships between regular commands andsubsequent activate commands</td></tr><tr><td rowspan=1 colspan=1>79</td><td rowspan=1 colspan=1>Figure 41: Note 6 revised to remove bank group disabling</td></tr><tr><td rowspan=1 colspan=1>96</td><td rowspan=1 colspan=1>Corrections: Figure 56 and 57, Add notes</td></tr><tr><td rowspan=1 colspan=1>122</td><td rowspan=1 colspan=1>6.8.2.(c) Add a text to support per-PC VrefD while DWORD MISR training</td></tr><tr><td rowspan=1 colspan=1>153,154</td><td rowspan=1 colspan=1>6.11.2.1 Add a text on an optional feature (Read DCA)Table 74: Removed (redundant contents)</td></tr><tr><td rowspan=1 colspan=1>158</td><td rowspan=1 colspan=1>6.12.2 Add a text on an optional feature (RxOffCal)Table 80 and 81: Removed (redundant contents)</td></tr><tr><td rowspan=1 colspan=1>181, 182, 184,186, 187</td><td rowspan=1 colspan=1>Corrections: Table 100, 101, 102, 104 (RA pattern)</td></tr><tr><td rowspan=1 colspan=1>194</td><td rowspan=1 colspan=1>Table 108: Revise Note 19 (how to count RAS cycles)</td></tr><tr><td rowspan=1 colspan=1>204</td><td rowspan=1 colspan=1>Clear typos and hyperlinks on Figure 107 and Figure 108</td></tr><tr><td rowspan=1 colspan=1>204</td><td rowspan=1 colspan=1>11.4 Revise a text: add a dead bug view perspective on how to see bump matrixorientationsAddition: Figure 106</td></tr><tr><td rowspan=1 colspan=1>214</td><td rowspan=1 colspan=1>Clause 13.2.3: corrections: 16 to 32 WSO signals</td></tr><tr><td rowspan=1 colspan=1>239</td><td rowspan=1 colspan=1>Table 132: Add options feature supports (LOW TEMP, PER PC VREFD),adjust OPT FEATURES bits, Add note 4</td></tr><tr><td rowspan=1 colspan=1>243</td><td rowspan=1 colspan=1>Table 133: Add optional a low temperature code, add note 1</td></tr></table>

This page intentionally left blank

## Standard Improvement Form

JEDEC Standard JESD270-4A

The purpose of this form is to provide the Technical Committees of JEDEC with input from the industry regarding usage of the subject standard. Individuals or companies are invited to submit comments to JEDEC. All comments will be collected and dispersed to the appropriate committee(s).

If you can provide input, please complete this form and return to:

JEDEC

Attn: Publications Department

Email: angies@jedec.org

3103 10th Street North

Suite 240S

Arlington, VA 22201

1. I recommend changes to the following:

Requirement, section number

Test method number Section number

The referenced section number has proven to be:

Unclear Too Rigid In Error

Other

2. Recommendations for correction:

3. Other suggestions for document improvement:

Submitted by

Name:

Phone:

Company:

E-mail:

Address:

City/State/Zip: Date:

# JEDEC