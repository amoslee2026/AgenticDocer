---
title: AMBA AXI and ACE Protocol Specification (IHI0022K)
source: corpus/01_raw/specifications/amba/IHI0022K_AMBA_AXI_ACE_protocol_spec.pdf
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
spec_id: SPEC-STD-AMBA-AXI-K
spec_org: ARM
spec_revision: IHI0022K
status: approved
---
![](images/e09076dbde85e643607bd91b9212f7531b3c0c0cee06658aa701e66f8191e425.jpg)

Document number

ARM IHI 0022

Document quality

Released

Document version

Issue L

Document confidentiality

Non-confidential

Date of issue

27 Aug 2025

Copyright © 2003-2025 Arm Limited or its affiliates. All rights reserved.

## AMBA® AXI Protocol Specification

## Release information

<table><tr><td>Date</td><td>Version</td><td>Changes</td></tr><tr><td>2025/Aug/27 L</td><td></td><td>• EAC-0 release of Issue L.</td></tr><tr><td></td><td></td><td>• Credited transport option.</td></tr><tr><td></td><td></td><td>• Arm Compression Technology.</td></tr><tr><td></td><td></td><td>• New option for protection signaling.</td></tr><tr><td></td><td></td><td>• RME - Granular Data Isolation.</td></tr><tr><td></td><td></td><td>• Untranslated transactions v4.</td></tr><tr><td></td><td></td><td>• CMO to the Point of Physical Storage.</td></tr><tr><td></td><td></td><td>• Other minor additions, corrections, and clarifications.</td></tr><tr><td>2023/Sep/29 K</td><td></td><td>• EAC-0 release of Issue K.</td></tr><tr><td></td><td></td><td>• Memory Encryption Contexts (MEC).</td></tr><tr><td></td><td></td><td>• Memory System Resource Partitioning and Monitoring (MPAM) extension.</td></tr><tr><td></td><td></td><td>• Memory Tagging Extension (MTE) Simplified option.</td></tr><tr><td></td><td></td><td>• Other minor additions, corrections, and clarifications.</td></tr><tr><td>2023/Mar/01 J</td><td></td><td>• EAC-0 release of Issue J.</td></tr><tr><td></td><td></td><td>• Simplified document structure.</td></tr><tr><td></td><td></td><td>• AXI3, AXI4, AXI4-Lite, ACE, and ACE5 content removed.</td></tr><tr><td></td><td></td><td>• New content added for AXI5, AXI5-Lite, ACE5-Lite, ACE5-LiteDVM, and</td></tr><tr><td>2021/Jan/26</td><td></td><td>ACE5-LiteACP interface classes • Corrected error in table D13-22 for AxADDR[15].</td></tr><tr><td>2021/Jan/11</td><td>H.c</td><td>• Regularized terminology to use Manager to indicate the agent that initiates read and</td></tr><tr><td></td><td>H.b</td><td>write requests and Subordinate to indicate the agent that responds to read and write</td></tr><tr><td></td><td></td><td>requests.</td></tr><tr><td>2020/Mar/31 H</td><td></td><td>• EAC-0 release of Issue H.</td></tr><tr><td></td><td></td><td>• New optional features defined for AMBA 5 interface variants.</td></tr><tr><td>2019/Jul/30</td><td>G</td><td>• EAC-0 release of Issue G.</td></tr><tr><td></td><td></td><td>• New optional features defined for AMBA 5 interface variants.</td></tr><tr><td>2017/Dec/21</td><td>F.b</td><td>• EAC-1 release to address issues found with the EAC-0 release of release F.</td></tr><tr><td>2017/Dec/18</td><td></td><td>• EAC-0 release of Issue F.</td></tr><tr><td></td><td></td><td>• New interfaces defined for AMBA protocol: AXI5, AXI5-Lite, ACE5, ACE5-Lite,</td></tr><tr><td>2013/Feb/22</td><td>E</td><td>ACE5-LiteDVM, and ACE5-LiteACP. • Second release of AMBA AXI and ACE Protocol specification.</td></tr><tr><td>2011/Oct/28</td><td>D</td><td>• First release of AMBA AXI and ACE Protocol specification.</td></tr><tr><td>2011/Jun/03</td><td></td><td>• Public beta draft of AMBA AXI and ACE Protocol specification.</td></tr><tr><td></td><td>D-2c</td><td></td></tr><tr><td>2010/Mar/03</td><td>C</td><td>• First release of AXI specification v2.0.</td></tr><tr><td>2004/Mar/19</td><td>B</td><td>• First release of AXI specification v1.0.</td></tr><tr><td>2003/Jun/16</td><td>A</td><td>• First release.</td></tr></table>

## Non-Confidential Proprietary Notice

This document is protected by copyright and other related rights and the use or implementation of the information contained in this document may be protected by one or more patents or pending patent applications. No part of this document may be reproduced in any form by any means without the express prior written permission of Arm Limited (“Arm”). No license, express or implied, by estoppel or otherwise to any intellectual property rights is granted by this document unless specifically stated.

Your access to the information in this document is conditional upon your acceptance that you will not use or permit others to use the information for the purposes of determining whether the subject matter of this document infringes any third party patents.

The content of this document is informational only. Any solutions presented herein are subject to changing conditions, information, scope, and data. This document was produced using reasonable efforts based on information available as of the date of issue of this document. The scope of information in this document may exceed that which Arm is required to provide, and such additional information is merely intended to further assist the recipient and does not represent Arm’s view of the scope of its obligations. You acknowledge and agree that you possess the necessary expertise in system security and functional safety and that you shall be solely responsible for compliance with all legal, regulatory, safety and security related requirements concerning your products, notwithstanding any information or support that may be provided by Arm herein. In addition, you are responsible for any applications which are used in conjunction with any Arm technology described in this document, and to minimize risks, adequate design and operating safeguards should be provided for by you.

This document may include technical inaccuracies or typographical errors. THIS DOCUMENT IS PROVIDED “AS IS”. ARM PROVIDES NO REPRESENTATIONS AND NO WARRANTIES, EXPRESS, IMPLIED OR STATUTORY, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTIES OF MERCHANTABILITY, SATISFACTORY QUALITY, NON-INFRINGEMENT OR FITNESS FOR A PARTICULAR PURPOSE WITH RESPECT TO THE DOCUMENT. For the avoidance of doubt, Arm makes no representation with respect to, and has undertaken no analysis to identify or understand the scope and content of, any patents, copyrights, trade secrets, trademarks, or other rights.

TO THE EXTENT NOT PROHIBITED BY LAW, IN NO EVENT WILL ARM BE LIABLE FOR ANY DAMAGES, INCLUDING WITHOUT LIMITATION ANY DIRECT, INDIRECT, SPECIAL, INCIDENTAL, PUNITIVE, OR CONSEQUENTIAL DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY, ARISING OUT OF ANY USE OF THIS DOCUMENT, EVEN IF ARM HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

Reference by Arm to any third party’s products or services within this document is not an express or implied approval or endorsement of the use thereof.

This document consists solely of commercial items. You shall be responsible for ensuring that any permitted use, duplication, or disclosure of this document complies fully with any relevant export laws and regulations to assure that this document or any portion thereof is not exported, directly or indirectly, in violation of such export laws. Use of the word “partner” in reference to Arm’s customers is not intended to create or refer to any partnership relationship with any other company. Arm may make changes to this document at any time and without notice.

This document may be translated into other languages for convenience, and you agree that if there is any conflict between the English version of this document and any translation, the terms of the English version of this document shall prevail.

The validity, construction and performance of this notice shall be governed by English Law.

The Arm corporate logo and words marked with ® or ™ are registered trademarks or trademarks of Arm Limited (or its affiliates) in the US and/or elsewhere. Please follow Arm’s trademark usage guidelines at http://www.arm.com/company/policies/trademarks. All rights reserved. Other brands and names mentioned in this document may be the trademarks of their respective owners.

Copyright © 2003-2025 Arm Limited or its affiliates. All rights reserved.

Arm Limited. Company 02557590 registered in England.

110 Fulbourn Road, Cambridge, England CB1 9NJ.

PRE-21451 version 3

# AMBA SPECIFICATION LICENCE

THIS END USER LICENCE AGREEMENT (“LICENCE”) IS A LEGAL AGREEMENT BETWEEN YOU (EITHER A SINGLE INDIVIDUAL, OR SINGLE LEGAL ENTITY) AND ARM LIMITED (“ARM”) FOR THE USE OF ARM’S INTELLECTUAL PROPERTY (INCLUDING, WITHOUT LIMITATION, ANY COPYRIGHT) IN THE RELEVANT AMBA SPECIFICATION ACCOMPANYING THIS LICENCE. ARM LICENSES THE RELEVANT AMBA SPECIFICATION TO YOU ON CONDITION THAT YOU ACCEPT ALL OF THE TERMS IN THIS LICENCE. BY CLICKING “I AGREE” OR OTHERWISE USING OR COPYING THE RELEVANT AMBA SPECIFICATION YOU INDICATE THAT YOU AGREE TO BE BOUND BY ALL THE TERMS OF THIS LICENCE.

“LICENSEE” means You and your Subsidiaries. “Subsidiary” means, if You are a single entity, any company the majority of whose voting shares is now or hereafter owned or controlled, directly or indirectly, by You. A company shall be a Subsidiary only for the period during which such control exists.

1. Subject to the provisions of Clauses 2, 3 and 4, Arm hereby grants to LICENSEE a perpetual, non-exclusive, non-transferable, royalty free, worldwide licence to:

(i) use and copy the relevant AMBA Specification for the purpose of developing and having developed products that comply with the relevant AMBA Specification;

(ii) manufacture and have manufactured products which either: (a) have been created by or for LICENSEE under the licence granted in Clause 1(i); or (b) incorporate a product(s) which has been created by a third party(s) under a licence granted by Arm in Clause 1(i) of such third party’s AMBA Specification Licence; and

(iii) offer to sell, sell, supply or otherwise distribute products which have either been (a) created by or for LICENSEE under the licence granted in Clause 1(i); or (b) manufactured by or for LICENSEE under the licence granted in Clause 1(ii).

2. LICENSEE hereby agrees that the licence granted in Clause 1 is subject to the following restrictions:

(i) where a product created under Clause 1(i) is an integrated circuit which includes a CPU then either: (a) such CPU shall only be manufactured under licence from Arm; or (b) such CPU is neither substantially compliant with nor marketed as being compliant with the Arm instruction sets licensed by Arm from time to time;

(ii) the licences granted in Clause 1(iii) shall not extend to any portion or function of a product that is not itself compliant with part of the relevant AMBA Specification; and

(iii) no right is granted to LICENSEE to sublicense the rights granted to LICENSEE under this Agreement.

3. Except as specifically licensed in accordance with Clause 1, LICENSEE acquires no right, title or interest in any Arm technology or any intellectual property embodied therein. In no event shall the licences granted in accordance with Clause 1 be construed as granting LICENSEE, expressly or by implication, estoppel or otherwise, a licence to use any Arm technology except the relevant AMBA Specification.

4. THE RELEVANT AMBA SPECIFICATION IS PROVIDED “AS IS” WITH NO REPRESENTATION OR WARRANTIES EXPRESS, IMPLIED OR STATUTORY, INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF SATISFACTORY QUALITY, MERCHANTABILITY, NON-INFRINGEMENT OR FITNESS FOR A PARTICULAR PURPOSE, OR THAT ANY USE OR IMPLEMENTATION OF SUCH ARM TECHNOLOGY WILL NOT INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADE SECRETS OR OTHER INTELLECTUAL PROPERTY RIGHTS.

5. NOTWITHSTANDING ANYTHING TO THE CONTRARY CONTAINED IN THIS AGREEMENT, TO THE FULLEST EXTENT PETMITTED BY LAW, THE MAXIMUM LIABILITY OF ARM IN AGGREGATE FOR ALL CLAIMS MADE AGAINST ARM, IN CONTRACT, TORT OR OTHERWISE, IN CONNECTION WITH THE SUBJECT MATTER OF THIS AGREEMENT (INCLUDING WITHOUT LIMITATION (I) LICENSEE’S USE OF THE ARM TECHNOLOGY; AND (II) THE IMPLEMENTATION OF THE ARM TECHNOLOGY IN ANY PRODUCT CREATED BY LICENSEE UNDER THIS AGREEMENT) SHALL NOT EXCEED THE FEES PAID (IF ANY) BY LICENSEE TO ARM UNDER THIS AGREEMENT. THE EXISTENCE OF MORE THAN ONE CLAIM OR SUIT WILL NOT ENLARGE OR EXTEND THE LIMIT. LICENSEE RELEASES ARM FROM ALL OBLIGATIONS, LIABILITY, CLAIMS OR DEMANDS IN EXCESS OF THIS LIMITATION.

6. No licence, express, implied or otherwise, is granted to LICENSEE, under the provisions of Clause 1, to use the Arm tradename, or AMBA trademark in connection with the relevant AMBA Specification or any products based thereon. Nothing in Clause 1 shall be construed as authority for LICENSEE to make any representations on behalf of Arm in respect of the relevant AMBA Specification.

7. This Licence shall remain in force until terminated by you or by Arm. Without prejudice to any of its other rights if LICENSEE is in breach of any of the terms and conditions of this Licence then Arm may terminate this Licence immediately upon giving written notice to You. You may terminate this Licence at any time. Upon expiry or termination of this Licence by You or by Arm LICENSEE shall stop using the relevant AMBA Specification and destroy all copies of the relevant AMBA Specification in your possession together with all documentation and related materials. Upon expiry or termination of this Licence, the provisions of clauses 6 and 7 shall survive.

8. The validity, construction and performance of this Agreement shall be governed by English Law.

PRE-21451 version 3

## Confidentiality Status

This document is Non-Confidential. The right to use, copy and disclose this document may be subject to license restrictions in accordance with the terms of the agreement entered into by Arm and the party that Arm delivered this document to.

## Product Status

The information in this document is final, that is for a developed product.

## Web Address

http://www.arm.com

## Contents AMBA<sup>®</sup> AXI Protocol Specification

AMBA® AXI Protocol Specification ii   
Release information ii   
Non-Confidential Proprietary Notice iii   
AMBA SPECIFICATION LICENCE iv   
Confidentiality Status v   
Product Status v   
Web Address v   
Intended audience xiii   
Using this specification . xiii   
Conventions xv   
Typographical conventions xv   
Timing diagrams xv   
Signals xvi   
Numbers xvi   
Pseudocode descriptions xvi   
Additional reading xvii   
Feedback . xviii   
Feedback on this specification . xviii   
Inclusive terminology commitment xviii   
ation   
Introduction   
A1.1 About the AXI protocol 21   
A1.2 AXI Architecture . . 22   
A1.2.1 Interface and interconnect 24   
A1.3 Terminology 25   
A1.3.1 AXI components and topology 25   
A1.3.2 AXI transactions and transfers 25   
A1.3.3 Caches and cache operation 25   
A1.3.4 Temporal description 25   
AXI transport   
A2.1 Clock and reset 27   
A2.1.1 Clock . 27   
A2.1.2 Reset . 27   
A2.2 AXI transport options 28   
A2.3 Valid-Ready transport 29   
A2.3.1 Valid-Ready signals 30   
A2.3.2 Dependencies between channel handshake signals 31   
A2.4 Credited transport 33   
A2.4.1 Credited flow control 34   
A2.4.2 Resource Planes 35   
A2.4.3 Shared credits . 36   
A2.4.4 Transfer-level clock gating 38   
A2.4.5 Credited transport signals 39   
A2.5 Pipelining and register stages 40   
A2.6 AXI transactions and transfers 41   
AXI transactions   
A3.1 Transaction request . 43   
A3.1.1 Size attribute 43   
A3.1.2 Length attribute 44   
A3.1.3 Maximum number of bytes in a transaction 45   
A3.1.4 Burst attribute 46   
A3.1.5 Transfer address 49   
A3.1.6 Transaction equations 49   
A3.1.7 Pseudocode description of the transfers . 51   
A3.1.8 Regular transactions 52   
A3.2 Write and read data . 53   
A3.2.1 Write data channel (W) 53   
A3.2.2 Read data channel (R) 55   
A3.2.3 Narrow transfers 55   
A3.2.4 Byte invariance 56   
A3.2.5 Unaligned transfers 58   
A3.3 Transaction response 61   
A3.3.1 Write response 61   
A3.3.2 Read response 62   
A3.3.3 Subordinate Busy indicator . 64   
Request attributes   
A4.1 Subordinate types 67   
A4.2 Memory attributes 68   
A4.2.1 Bufferable, AxCACHE[0] 68   
A4.2.2 Modifiable, AxCACHE[1] 69   
A4.2.3 Allocate and Other Allocate, AxCACHE[2], and AxCACHE[3] 70   
A4.3 Memory types 71   
A4.3.1 Memory type requirements 71   
A4.3.2 Mismatched memory attributes 74   
A4.3.3 Changing memory attributes 74   
A4.3.4 Transaction buffering 74   
A4.3.5 Example use of Device memory types 75   
A4.4 Protocol errors 76   
A4.4.1 Software protocol error 76   
A4.4.2 Hardware protocol error 76   
A4.5 Protection attributes 77   
A4.5.1 Signaling for protection attributes 77   
A4.5.2 Privileged and Instruction attributes 78   
A4.5.3 Physical address space (PAS) 79   
A4.5.4 Realm Management Extension . 79   
A4.5.5 Granular Data Isolation 79   
A4.6 Memory Encryption Contexts 81   
A4.6.1 MEC signaling 81   
A4.6.2 MECID usage 82   
A4.6.3 MEC and GDI 83   
A4.7 Multiple region interfaces . 84   
A4.7.1 Region identifier signaling 84   
A4.7.2 Using the region identifier 84   
A4.8 QoS signaling 86   
A4.8.1 QoS identifiers . 86   
A4.8.2 QoS acceptance indicators 87   
Transaction identifiers and ordering   
A5.1 Transaction identifiers 90   
A5.1.1 Transaction ID signals . 90   
A5.2 Unique ID indicator 91   
A5.3 Request ordering 93   
A5.3.1 Memory locations and Peripheral regions 93   
A5.3.2 Device and Normal requests 94   
A5.3.3 Observation and completion definitions 94   
A5.3.4 Manager ordering guarantees 94   
A5.3.5 Subordinate ordering requirements 95   
A5.3.6 Interconnect ordering requirements 96   
A5.3.7 Response before the endpoint 96   
A5.3.8 Ordering between requests with different memory types 97   
A5.3.9 Ordered write observation 97   
A5.4 Interconnect use of transaction identifiers 99   
A5.5 Write data and response ordering 100   
A5.6 Read data ordering 101   
A5.6.1 Read data interleaving 101   
A5.6.2 Read data chunking . 102   
Atomic accesses   
A6.1 Single-copy atomicity size 108   
A6.2 Multi-copy write atomicity . 109   
A6.3 Exclusive accesses 110   
A6.3.1 Exclusive access sequence 110   
A6.3.2 Exclusive access from the perspective of the Manager . 111   
A6.3.3 Exclusive access restrictions 111   
A6.3.4 Exclusive access from the perspective of the Subordinate 112   
A6.4 Atomic transactions 113   
A6.4.1 Overview 113   
A6.4.2 Atomic transaction operations 114   
A6.4.3 Atomic transactions attributes 114   
A6.4.4 ID use for Atomic transactions 116   
A6.4.5 Request attribute restrictions for Atomic transactions 117   
A6.4.6 Atomic transaction signaling 117   
A6.4.7 Transaction structure 118   
A6.4.8 Response signaling 119   
A6.4.9 Atomic transaction dependencies 120   
A6.4.10 Support for Atomic transactions 121   
Request Opcodes   
A7.1 Opcode signaling 124   
A7.2 AWSNOOP encodings 126   
A7.3 ARSNOOP encodings 129   
Caches   
A8.1 Caching in AXI 132   
A8.2 Cache line size 133   
A8.3 Cache coherency and Domains 134   
A8.3.1 System Domain 134   
A8.3.2 Non-shareable Domain 134   
A8.3.3 Shareable Domain 134   
A8.3.4 Domain signaling 135   
A8.3.5 Domain consistency . 136   
A8.3.6 Domains and memory types 136   
A8.4 I/O coherency 137   
A8.5 Caching Shareable lines 138   
A8.5.1 Opcodes to support reading and writing full cache lines 139   
A8.5.2 Configuration of Shareable cache support 140   
A8.6 Prefetch transaction 142   
A8.6.1 Rules for the prefetch transaction 142   
A8.6.2 Response for prefetched data 143   
A8.7 Cache Stashing 144   
A8.7.1 Stash transaction Opcodes 144   
A8.7.2 Stash transaction signaling 145   
A8.7.3 Stash request Domain 145   
A8.7.4 Stash target identifiers 146   
A8.7.5 Transaction ID for stash transactions 147   
A8.7.6 Support for stash transactions 148   
A8.8 Deallocating read transactions 149   
A8.8.1 Deallocating read Opcodes . 149   
A8.8.2 Rules and recommendations 149   
A8.9 Invalidate hint 151   
A8.9.1 Invalidate Hint signaling 151   
A8.9.2 Invalidate Hint support 152   
Cache maintenance   
A9.1 Cache Maintenance Operations 154   
A9.2 Actions on receiving a CMO 155   
A9.3 CMO request attributes . 156   
A9.4 CMO propagation . 157   
A9.5 CMOs on the write channels 158   
A9.6 Write with CMO 160   
A9.6.1 Attributes for write with CMO 161   
A9.6.2 Propagation of write with CMO 161   
A9.6.3 Response to write with CMOs 161   
A9.6.4 Example flow with a write plus CMO 162   
A9.7 CMOs on the read channels 163   
A9.8 CMOs for Persistence 164   
A9.8.1 Point of Persistence and Deep Persistence 164   
A9.8.2 Persistent CMO (PCMO) transactions 164   
A9.8.3 PCMO propagation 165   
A9.8.4 PCMOs on write channels 165   
A9.8.5 PCMOs on read channels 167   
A9.9 Cache maintenance and Realm Management Extension 168   
A9.9.1 CMO to PoPA 168   
A9.9.2 CMO to PoPA propagation 169   
A9.10 Cache maintenance to the Point of Physical Storage 170   
A9.11 Processor cache maintenance instructions 172   
A9.11.1 Unpredictable behavior with software cache maintenance 172   
Additional request qualifiers   
A10.1 Non-secure Access Identifiers (NSAID) 175   
A10.1.1 NSAID signaling 175   
A10.1.2 Caching and NSAID 176   
A10.2 Page-based Hardware Attributes (PBHA) 177   
A10.2.1 PBHA values 177   
A10.3 Subsystem Identifier 178   
A10.3.1 Subsystem ID usage 178   
A10.4 Arm Compression Technology (ACT) 179   
A10.4.1 ACT signaling 180   
A10.4.2 ACT requests 180   
A10.4.3 Modifying ACT transactions 181   
Other write transactions   
A11.1 WriteZero Transaction 183   
A11.2 WriteDeferrable Transaction 184   
A11.2.1 WriteDeferrable transaction support 184   
A11.2.2 WriteDeferrable signaling 184   
A11.2.3 Response to a WriteDeferrable request 185   
System monitoring, debug, and user extensions   
A12.1 Memory System Resource Partitioning and Monitoring (MPAM) 187   
A12.1.1 MPAM signaling 187   
A12.1.2 MPAM fields 188   
A12.1.3 MPAM component interactions 189   
A12.2 Memory Tagging Extension (MTE) 190   
A12.2.1 MTE support . 190   
A12.2.2 MTE signaling 191   
A12.2.3 Caching tags 191   
A12.2.4 Transporting tags 192   
A12.2.5 Reads with tags 193   
A12.2.6 Writes with tags 194   
A12.2.7 Memory tagging interoperability 197   
A12.2.8 MTE and Atomic transactions 197   
A12.2.9 MTE and Prefetch transactions 198   
A12.2.10 MTE and Poison . 198   
A12.3 Trace signals 199   
A12.4 User Loopback signaling 200   
A12.5 User defined signaling 202   
A12.5.1 Configuration 202   
A12.5.2 User signals 202   
A12.5.3 Usage considerations 203   
Untranslated Transactions   
A13.1 Introduction to Distributed Virtual Memory 205   
A13.2 Support for untranslated transactions 206   
A13.3 Untranslated transaction signaling . 207   
A13.4 Translation identifiers 209   
A13.4.1 Secure Stream Identifier (SECSID) 209   
A13.4.2 StreamID (SID) 210   
A13.4.3 SubstreamID (SSID) 210   
A13.4.4 Untranslated Transactions and GDI 211   
A13.5 PCIe considerations 212   
A13.5.1 PCIe XT mode 212   
A13.6 Translation fault flows 214   
A13.6.1 Stall flow 215   
A13.6.2 ATST flow 215   
A13.6.3 NoStall flow 215   
A13.6.4 PRI flow 216   
A13.7 Untranslated transaction qualifier 217   
A13.8 Permitted combinations of MMU signals and PAS 218   
A13.9 StashTranslation Opcode . 219   
A13.10 UnstashTranslation Opcode 220   
Interface clock and power gating   
A14.1 Interface gating with Valid-Ready transport . 223   
A14.1.1 AWAKEUP rules and recommendations 223   
A14.1.2 AWAKEUP and Coherency Connection signaling 224   
A14.1.3 ACWAKEUP rules and recommendations 224   
A14.2 Interface gating with credited transport 225   
A14.2.1 Channel states 226   
A14.2.2 Stop request signal, ASKSTOP 227   
A14.2.3 Credit control signal rules . 227   
A14.2.4 Pipelining channels 227   
A14.2.5 Clock and power gating 228   
A14.3 Sequence diagram 229   
A14.4 Example waveform 230   
A14.4.1 Transmitting one read transaction 230   
Distributed Virtual Memory messages   
A15.1 Introduction to DVM transactions 232   
A15.2 Support for DVM messages 233   
A15.3 DVM messages 234   
A15.3.1 DVM message fields 234   
A15.3.2 TLB Invalidate messages 239   
A15.3.3 Branch Predictor Invalidate messages 243   
A15.3.4 Instruction cache invalidations 244   
A15.3.5 Synchronization message 247   
A15.3.6 Hint message 247   
A15.4 Transporting DVM messages 248   
A15.4.1 Signaling for DVM messages 249   
A15.4.2 Snoop channels using Valid-Ready transport 250   
A15.4.3 Snoop channels using credited transport 250   
A15.4.4 Address widths in DVM messages 250   
A15.4.5 Mapping message fields to signals 251   
A15.5 DVM Sync and Complete . 258   
A15.6 Coherency Connection signaling 260   
A15.6.1 Coherency Connection Handshake 260   
A15.7 Snoop channels credit control 263   
Interface and data protection   
A16.1 Data protection using Poison 265   
A16.2 Parity protection for data and interface signals 266   
A16.2.1 Configuration of parity protection . 266   
A16.2.2 Error detection behavior 266   
A16.2.3 Parity check signals 267   
ices   
Signal list   
B1.1 Write channels 275   
B1.1.1 Write request channel . 275   
B1.1.2 Write data channel 277   
B1.1.3 Write response channel . 278   
B1.2 Read channels 279   
B1.2.1 Read request channel 279   
B1.2.2 Read data channel 281   
B1.3 Snoop channels . 282   
B1.3.1 Snoop request channel . 282   
B1.3.2 Snoop response channel 282   
B1.4 Interface level signals . 283   
B1.4.1 Clock and reset signals 283   
B1.4.2 Credit control signals 283   
B1.4.3 Wakeup signals 283   
B1.4.4 QoS Accept signals . 284   
B1.4.5 Coherency Connection signals . 284   
B1.4.6 Interface control signals . 284   
Chapter B2 Interface classes   
B2.1 Summary of interface classes 286   
B2.1.1 AXI5 287   
B2.1.2 ACE5-Lite 287   
B2.1.3 ACE5-LiteDVM 287   
B2.1.4 ACE5-LiteACP 287   
B2.1.5 AXI5-Lite . 288   
B2.2 Signal matrix 289   
B2.3 Parity check signal matrix 296   
B2.4 Property matrix 300   
Chapter B3 Summary of ID constraints   
Chapter B4 Revisions   
B4.1 Differences between Issue H.c and Issue J . 307   
B4.2 Differences between Issue J and Issue K 309   
B4.3 Differences between Issue K and Issue L 311

## Part C Glossary

## Preface

This preface describes the content organization and documentation conventions used in this specification.

## Intended audience

This specification is written for hardware and software engineers who want to become familiar with the AMBA protocol and design systems and modules that are compatible with the AXI protocol.

## Using this specification

The information in this specification is organized into parts, as described in this section:

## Part A Specification

Chapter A1 Introduction

Introduces the AXI protocol architecture and terminology used in this specification.

## Chapter A2 AXI transport

Describes the AXI transport layer, with two options for flow control.

## Chapter A3 AXI transactions

Contains information on the AXI protocol transactions, such as transaction request, transaction response, and read and write data.

## Chapter A4 Request attributes

Describes memory attributes, memory types, memory protection, and multiple region interfaces.

## Chapter A5 Transaction identifiers and ordering

Describes transaction ID signals, request ordering, write data and response ordering, and read data ordering.

## Chapter A6 Atomic accesses

Contains information on Atomic accesses, single and multi-copy atomicity, and exclusive accesses.

## Chapter A7 Request Opcodes

Provides information on the opcode field that describes the function of a request and indicates how it must be processed by a Subordinate.

## Chapter A8 Caches

Describes caching in the AXI protocol, including I/O coherency, caching shareable lines, and managing cache allocation using specific transactions.

## Chapter A9 Cache maintenance

Provides information on using cache maintenance operations to control cache content ensuring visibility of data.

## Chapter A10 Additional request qualifiers

Describes additional request qualifiers in the AXI protocol, such as Non-secure Access Identifier (NSAID), Page-based Hardware Attributes (PBHA), and Subsystem Identifier.

Chapter A11 Other write transactions

Contains information on other write transactions in the AXI protocol, such as WriteDeferrable and WriteZero.

## Chapter A12 System monitoring, debug, and user extensions

Describes system debug, trace, and monitoring features of the AXI protocol, such as Memory System Resource Partitioning and Monitoring (MPAM), Memory Tagging Extension (MTE), and User Loopback and User defined signaling.

Chapter A13 Untranslated Transactions

Describes how AXI supports the use of virtual addresses and translation stash hints for components upstream of a System Memory Management Unit (SMMU).

Chapter A14 Interface clock and power gating

Describes how to stop and start interfaces for clock or power gating.

Chapter A15 Distributed Virtual Memory messages

Describes how AXI supports distributed system MMUs using Distributed Virtual Memory (DVM) messages to maintain all MMUs in a virtual memory system.

## Chapter A16 Interface and data protection

Explains how to protect data or interfaces using poison and parity check signals.

## Part B Appendices

Chapter B1 Signal list

A list of all the signals that are defined in the AXI protocol.

Chapter B2 Interface classes

Descriptions of all the AMBA 5 AXI interface classes, including signal and property tables.

Chapter B3 Summary ofID constraints

A summary of ID constraints in the AXI protocol.

Chapter B4 Revisions

Details of the changes between this issue and the previous issue of this specification.

## Part C Glossary

Chapter C1 Glossary

Learn about the AXI protocol terms and concepts.

## Conventions

## Typographical conventions

The typographical conventions are:

italic

Highlights important notes, introduces special terminology, and denotes internal cross-references and citations.

## bold

Denotes signal names, and is used for terms in descriptive lists, where appropriate.

monospace

Used for assembler syntax descriptions, pseudocode, and source code examples.

Also used in the main text for instruction mnemonics and for references to other items appearing in assembler syntax descriptions, pseudocode, and source code examples.

## SMALL CAPITALS

Used in body text for a few terms that have specific technical meanings.

Colored text

Indicates a link. This can be:

• A cross-reference that includes the page number of the referenced information if it is not on the current page.

• A URL, for example http://developer.arm.com.

• A link, to a chapter or appendix, or to a glossary entry, or to the section of the document that defines the colored term.

## Timing diagrams

The components used in timing diagrams are explained in Figure 1. Variations have clear labels when they occur.   
Do not assume any timing information that is not explicit in the diagrams.

![](images/78163f0f048decb6dd42e6769759078376fff9e7fd4dfdd1df8eb73cd74a16a5.jpg)  
Figure 1: Key to timing diagram conventions

Timing diagrams sometimes show single-bit signals as HIGH and LOW at the same time and they look similar to the bus change shown in Figure 1. If a timing diagram shows a single-bit signal in this way, then its value does not affect the accompanying description.

## Signals

The signal conventions are:

• Signal level - The level of an asserted signal depends on whether the signal is active-HIGH or active-LOW. Asserted means:

– HIGH for active-HIGH signals.

– LOW for active-LOW signals.

• Lowercase n - At the start or end of a signal name denotes an active-LOW signal.

• Lowercase x - At the second letter of a signal name denotes a collective term for both Read and Write. For example, AxCACHE refers to both the ARCACHE and AWCACHE signals.

## Numbers

Numbers are normally written in decimal. Binary numbers are preceded by 0b, and hexadecimal numbers by 0x. In both cases, the prefix and the associated value are written in a monospace font, for example 0xFFFF0000. To improve readability, long numbers can be written with an underscore separator between every four characters, for example 0xFFFF\_0000\_0000\_0000. Ignore any underscores when interpreting the value of a number.

## Pseudocode descriptions

This specification uses a form of pseudocode to provide precise descriptions of the specified functionality. This pseudocode is written in a monospace font. The pseudocode language is described in the Arm® Architecture Reference Manualfor A-profile architecture.

## Additional reading

This section lists publications by Arm and by third parties.

See Arm Developer, http://developer.arm.com for access to Arm documentation.

[1] AMBA® AXI and ACE Protocol Specification. (ARM IHI 0022 H.c)

[2] AMBA® AXI Protocol Specification. (ARM IHI 0022 K)

[3] Arm® Architecture Reference Manual for A-profile architecture. (ARM DDI 0487)

[4] Arm® Realm Management Extension (RME) System Architecture. (ARM DEN 0129)

[5] AMBA® 5 CHI Architecture Specification. (ARM IHI 0050)

[6] Arm® Architecture Reference Manual Supplement, Memory System Resource Partitioning and Monitoring (MPAM),for A-profile architecture. (ARM DDI 0598)

[7] Arm® System Memory Management Unit Architecture Specification, SMMU architecture version 3. (ARM IHI 0070)

## Feedback

Arm welcomes feedback on its documentation.

## Feedback on this specification

If you have any comments or suggestions for additions and improvements, create a ticket at https://support.developer.arm.com. As part of the ticket, please include:

• The title (AMBA® AXI Protocol Specification).

• The number (ARM IHI 0022 Issue L).

• The page numbers to which your comments apply.

• A concise explanation of your comments.

Arm also welcomes general suggestions for additions and improvements.

## Note

Arm tests PDFs only in Adobe Acrobat and Acrobat Reader, and cannot guarantee the appearance or behavior of any document when viewed with any other PDF reader.

## Inclusive terminology commitment

Arm values inclusive communities. Arm recognizes that we and our industry have used terms that can be offensive.

Arm strives to lead the industry and create change.

Previous issues of this document included terms that can be offensive. We have replaced these terms. If you find offensive terms in this document, please contact terms@arm.com.

Part A Specification

## Chapter A1 Introduction

This chapter introduces the architecture of the AXI protocol and the terminology used in this specification.

It contains the following sections:

• A1.1 About the AXIprotocol

• A1.2 AXI Architecture

• A1.3 Terminology

## A1.1 About the AXI protocol

The AXI protocol supports high-performance, high-frequency system designs for communication between Manager and Subordinate components.

The AXI protocol features are:

• Suitable for high-bandwidth and low-latency designs.

• High-frequency operation is provided without using complex bridges.

• The protocol meets the interface requirements of a wide range of components.

• Suitable for memory controllers with high initial access latency.

• Flexibility in the implementation of interconnect architectures is provided.

• Backward-compatible with AHB and APB interfaces.

The key features of the AXI protocol are:

• Separate address/control and data phases.

• Support for unaligned data transfers using byte strobes.

• Uses burst-based transactions with only the start address issued.

• Separate write and read data channels that can provide low-cost Direct Memory Access (DMA).

• Support for issuing multiple outstanding addresses.

• Support for out-of-order transaction completion.

• Permits easy addition of register stages to provide timing closure.

For the previous issues of this specification, see [1] and [2].

## A1.2 AXI Architecture

The AXI protocol defines transactions that are used to read and write data, or control the caching of data and translations. Transactions are performed by sending transfers on the channels:

• Write request, which has signal names beginning with AW.

• Write data, which has signal names beginning with W.

• Write response, which has signal names beginning with B.

• Read request, which has signal names beginning with AR.

• Read data, which has signal names beginning with R.

A request channel carries control information that describes the nature of the data to be transferred. This is known as a request.

The data is transferred between Manager and Subordinate using either:

• A write data channel to transfer data from the Manager to the Subordinate. In a write transaction, the Subordinate uses the write response channel to signal the completion of the transfer to the Manager.

• A read data channel to transfer data from the Subordinate to the Manager.

## The AXI protocol:

• Permits address information to be issued ahead of the actual data transfer.

• Supports multiple outstanding transactions.

• Supports out-of-order completion of transactions.

Figure A1.1 shows how a write transaction uses the write request, write data, and write response channels.

![](images/5b4821f13ff092b48ddfa56d3033c87f3a307fa29556cfba0774886027e47770.jpg)  
Figure A1.1: Channel architecture of writes  
Figure A1.2 shows how a read transaction uses the read request and read data channels.

![](images/5376344452ed9e4bdeca5578f78af8ed666cd1838df75977bba3e9b2ba9e1424.jpg)  
Figure A1.2: Channel architecture of reads

## Write and read request channels

There are separate write and read request channels. The appropriate request channel carries all the required address and control information for a transaction.

## Write data channel

The write data channel carries the write data from the Manager to the Subordinate. Write data can be up to 1024 bits wide and there is a byte lane strobe signal for every eight data bits, indicating the bytes of the data that are valid.

Write data channel information is always treated as buffered, so that the Manager can perform write transactions without Subordinate acknowledgment of previous write transactions.

## Write response channel

A Subordinate uses the write response channel to respond to write transactions. All write transactions require completion signaling on the write response channel.

As Figure A1.1 shows, completion is signaled only for a complete transaction, not for each data transfer in a transaction.

## Read data channel

The read data channel carries both the read data and the read response information from the Subordinate to the Manager. Read data can be up to 1024 bits wide.

## A1.2.1 Interface and interconnect

A typical system consists of several Manager and Subordinate devices that are connected together through some form of interconnect, as Figure A1.3 shows.

![](images/7a275cd086b533ada6584416ac3e48a2c354d9391c45714218c658c74e88cc87.jpg)  
Figure A1.3: Interface and interconnect

The AXI protocol provides a single interface definition for the interfaces between:

• A Manager and the interconnect

• A Subordinate and the interconnect

• A Manager and a Subordinate

This interface definition supports many different interconnect implementations.

An interconnect between devices is equivalent to another device with symmetrical Manager and Subordinate ports that the real Manager and Subordinate devices can be connected.

## A1.2.1.1 Typical system topologies

Most systems use one of three interconnect topologies:

• Shared request and data channels

• Shared request channel and multiple data channels

• Multilayer, with multiple request and data channels

In most systems, the request channel bandwidth requirement is significantly less than the data channel bandwidth requirement. Such systems can achieve a good balance between system performance and interconnect complexity by using a shared request channel with multiple data channels to enable parallel data transfers.

## A1.3 Terminology

This section summarizes terms that are used in this specification, and are defined in Chapter C1 Glossary, or elsewhere. Where appropriate, terms that are listed in this section link to the corresponding glossary definition.

## A1.3.1 AXI components and topology

The following terms describe AXI components:

• Component

• Manager Component

• Subordinate Component, which includes Memory Subordinate component and Peripheral Subordinate component

• Interconnect Component

For a particular AXI transaction, Upstream and Downstream refer to the relative positions of AXI components within the AXI topology.

## A1.3.2 AXI transactions and transfers

A channel is a unidirectional connection, capable of carrying transfers between a transmitter (Tx) and receiver (Rx).

An interface is a set of channel transmitters and receivers on a component, where the channels have a defined use.   
AXI interfaces are defined as Manager or Subordinate.

An AXI transfer is the communication in one cycle on an AXI channel.

An AXI transaction is the set of transfers required for an AXI Manager to communicate with an AXI Subordinate.   
For example, a read transaction consists of a request transfer and one or more read data transfers.

## A1.3.3 Caches and cache operation

This specification does not define standard cache terminology that is defined in any reference work on caching.   
However, the glossary entries for Cache and Cache line clarify how these terms are used in this document.

## A1.3.4 Temporal description

The AXI specification uses the term in a timely manner.

## Chapter A2 AXI transport

AXI uses channels to transport request, data and response transfers between components.

This chapter describes the AXI transport with options for either a VALID-READY handshake or credited channels. It contains the following sections:

• A2.1 Clock and reset

• A2.2 AXI transport options

• A2.3 Valid-Ready transport

• A2.4 Credited transport

• A2.5 Pipelining and register stages

• A2.6 AXI transactions and transfers

## A2.1 Clock and reset

This section describes the requirements for implementing the AXI global clock and reset signals ACLK and ARESETn.

## A2.1.1 Clock

Each AXI interface has a single clock signal, ACLK. All input signals are sampled on the rising edge of ACLK.   
All output signal changes can only occur after the rising edge of ACLK.

There must be no combinatorial paths between input and output signals on an interface.

## A2.1.2 Reset

The AXI protocol uses a single active-LOW reset signal, ARESETn. The reset signal can be asserted asynchronously, but deassertion can only be synchronous with a rising edge of ACLK.

Signals that are required to be deasserted during reset must remain deasserted at least until the rising ACLK edge after ARESETn is HIGH. The earliest point these signals can be asserted is at a rising ACLK edge after ARESETn is HIGH.

Other signals can take any value during reset.

For example, for VALID, this is point b in Figure A2.1.

![](images/d006160569fad2d2f4180b64ccc74eeb23c6c064ab37b9a81e5219c1600b16a9.jpg)  
Figure A2.1: Exit from reset

## A2.2 AXI transport options

Two options are available for AXI transport:

• Ready, where every channel includes VALID and READY signals. The transmitter asserts VALID when it has a transfer to send. A transfer occurs when VALID and READY are both HIGH.

• Credited, where every channel includes VALID and CRDT signals. The receiver uses CRDT signals to give credits to the transmitter. The transmitter can assert VALID to send a transfer if it has an appropriate credit. This transport is good for high frequency operation and enables the use of Resource Planes on a link.

All AXI channels on an interface use the same type of transport, Table A2.1 shows how this is configured using the AXI\_Transport property.

Table A2.1: AXI\_Transport property
<table><tr><td></td><td>AXI_Transport Default Description</td><td></td></tr><tr><td>Credited</td><td></td><td>AXI channels use CRDT flow control signals.</td></tr><tr><td>Ready</td><td>Y</td><td>AXI channels use READY flow control signals.</td></tr></table>

The following rules apply to transport configuration:

• Connected Manager and Subordinate interfaces must have the same value for the AXI\_Transport property.

• Credited transport can be used with AXI5 interfaces only.

## A2.3 Valid-Ready transport

When using a Valid-Ready transport, all AXI channels use the same VALID-READY handshake process to transfer address, data, and control information. This two-way flow control mechanism means both the Manager and Subordinate can control the rate that the information moves between Manager and Subordinate. The transmitter generates the VALID signal to indicate when the address, data, or control information is available. The receiver generates the READY signal to indicate that it can accept the information. Transfer occurs only when both the VALID and READY signals are HIGH.

VALID signals must be LOW during reset.

Figure A2.2, Figure A2.3 and Figure A2.4 show examples of the handshake process.

The transmitter presents information after edge 1 and asserts the VALID signal as shown in Figure A2.2. The receiver asserts the READY signal after edge 2. The transmitter must keep its information stable until the transfer occurs at edge 3, when this assertion is recognized.

![](images/4cb443d8c39c95fb84850b9d179fffef2681849d7cc9e0ceac02a122284ae699.jpg)  
Figure A2.2: VALID before READY handshake

A transmitter is not permitted to wait until READY is asserted before asserting VALID.

When VALID is asserted, it must remain asserted until the handshake occurs, at a rising clock edge when VALID and READY are both asserted.

In Figure A2.3, the receiver asserts READY after edge 1, before the address, data, or control information is valid. This assertion indicates that it can accept the information. The transmitter presents the information and asserts VALID after edge 2, then the transfer occurs at edge 3, when this assertion is recognized. In this case, transfer occurs in a single cycle.

![](images/a133abaeb4e035fe8a51341a74e5bb0bb14db6519911c8934ea09a4ec7425f19.jpg)  
Figure A2.3: READY before VALID handshake

A receiver is permitted to wait for VALID to be asserted before asserting the corresponding READY.

If READY is asserted, it is permitted to deassert READY before VALID is asserted.

In Figure A2.4, both the transmitter and receiver happen to indicate that they can transfer the address, data, or control information after edge 1. In this case, the transfer occurs at the rising clock edge when the assertion of both VALID and READY can be recognized. These assertions mean that the transfer occurs at edge 2.

![](images/67af5f90038e5934f1649272e3f6c6c5270f9905a8317d6c58470d26c5ac5ca6.jpg)  
Figure A2.4: VALID with READY handshake

The default state of READY signals can be either HIGH or LOW.

For request channels, it is recommended to use HIGH as the default state to minimize latency. In that case, the Subordinate must be able to accept any valid request that is presented to it.

## A2.3.1 Valid-Ready signals

Table A2.2 shows the VALID and READY signals. VALID signals are present whether using Valid-Ready transport or credited transport.

Table A2.2: Valid and Ready signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWVALID</td><td>1</td><td></td><td>Asserted high to indicate that the signals on the AW channel are valid.</td></tr><tr><td>AWREADY</td><td>1</td><td></td><td>Asserted high to indicate that a transfer on the AW channel can be accepted.</td></tr><tr><td>WVALID</td><td>1</td><td>一</td><td>Asserted high to indicate that the signals on the W channel are valid.</td></tr><tr><td>WREADY</td><td>1</td><td></td><td>Asserted high to indicate that a transfer on the W channel can be accepted.</td></tr><tr><td>BVALID</td><td>1</td><td></td><td>Asserted high to indicate that the signals on the B channel are valid.</td></tr><tr><td>BREADY</td><td>1</td><td></td><td>Asserted high to indicate that a transfer on the B channel can be accepted.</td></tr><tr><td>ARVALID</td><td>1</td><td></td><td>Asserted high to indicate that the signals on the AR channel are valid.</td></tr><tr><td>ARREADY</td><td>1</td><td></td><td>Asserted high to indicate that a transfer on the AR channel can be accepted.</td></tr><tr><td>RVALID</td><td>1</td><td></td><td>Asserted high to indicate that the signals on the R channel are valid.</td></tr><tr><td>RREADY</td><td>1</td><td></td><td>Asserted high to indicate that a transfer on the R channel can be accepted.</td></tr></table>

## A2.3.2 Dependencies between channel handshake signals

There are dependencies between channels for write, read, and snoop transactions. These are described in the sections below and include dependency diagrams, where:

• Single-headed arrows point to signals that can be asserted before or after the signal at the start of the arrow.

• Double-headed arrows point to signals that must be asserted only after assertion of the signal at the start of the arrow.

## A2.3.2.1 Write transaction dependencies

For transactions on the write channels, Figure A2.5 shows the handshake signal dependencies. The rules are:

• The Manager must not wait for the Subordinate to assert AWREADY or WREADY before asserting AWVALID or WVALID. This applies to every write data transfer in a transaction.

• The Subordinate can wait for AWVALID or WVALID, or both, before asserting AWREADY.

• The Subordinate can assert AWREADY before AWVALID or WVALID, or both, are asserted.

• The Subordinate can wait for AWVALID or WVALID, or both, before asserting WREADY.

• The Subordinate can assert WREADY before AWVALID or WVALID, or both, are asserted.

• The Subordinate must wait for AWVALID, AWREADY, WVALID, and WREADY to be asserted before asserting BVALID.

• The Subordinate must wait for the last write data transfer before asserting BVALID. The last write data transfer has WLAST asserted, see A3.2.1 Write data channel (W).

• The Subordinate must not wait for the Manager to assert BREADY before asserting BVALID.

• The Manager can wait for BVALID before asserting BREADY.

• The Manager can assert BREADY before BVALID is asserted.

![](images/9417a6c72577a9cd7d59aa3105a92cf58fcfc44e03864405378b03ac1851f0c4.jpg)  
Figure A2.5: Write transaction handshake dependencies

For transactions on the write channels that do not include data, WVALID and WREADY are not included in the dependencies.

## A2.3.2.2 Read transaction dependencies

For transactions on the read channels, Figure A2.6 shows the handshake signal dependencies. The rules are:

• The Manager must not wait for the Subordinate to assert ARREADY before asserting ARVALID.

• The Subordinate can wait for ARVALID to be asserted before it asserts ARREADY.

• The Subordinate can assert ARREADY before ARVALID is asserted.

• The Subordinate must wait for both ARVALID and ARREADY to be asserted before it asserts RVALID to indicate that valid data is available.

• The Subordinate must not wait for the Manager to assert RREADY before asserting RVALID.

• The Manager can wait for RVALID to be asserted before it asserts RREADY.

• The Manager can assert RREADY before RVALID is asserted.

![](images/3ea24c9cb8349a51721f6e420ab6e48f78bd82c2aa2e99ac168046ed7f0e8a1b.jpg)  
Figure A2.6: Read transaction handshake dependencies

## A2.4 Credited transport

When the AXI\_Transport property is Credited, AXI channels use a credited transport.

Table A2.3 shows a list of all signals that can be added to a channel when credited transport is used. Signal names are the base name, when instantiated each includes a prefix to indicate which channel they belong.

A channel has a transmitter (Tx) and a receiver (Rx).

Table A2.3: Credited channel signals
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Presence</td><td>Description</td></tr><tr><td>VALID</td><td>1</td><td>Tx</td><td></td><td>When asserted HIGH, there is one transfer from Tx to Rx.</td></tr><tr><td>PENDING</td><td>1</td><td>Tx</td><td>AXI_Transport == Credited</td><td>Asserted HIGH to indicate that a transfer might occur in the following cycle. See A2.4.4 Transfer-level clock gating.</td></tr><tr><td>RP</td><td>clog2(Num_RP)</td><td>Tx</td><td>Num_RP &gt; 1</td><td>Encoded indicator of the Resource Plane number for a transfer. See A2.4.2 Resource Planes.</td></tr><tr><td>SHAREDCRD</td><td>1</td><td>Tx</td><td>Shared_Credits == True</td><td>Asserted HIGH to indicate that the transfer is using a shared credit. See A2.4.3 Shared credits.</td></tr><tr><td>CRDT</td><td>Num_RP</td><td>Rx</td><td>AXI_Transport == Credited</td><td>Asserted HIGH to give one credit on the respective resource plane.</td></tr><tr><td>CRDTSH</td><td>1</td><td>Rx</td><td>Shared_Credits == True</td><td>Asserted HIGH to give one shared credit. See A2.4.3 Shared credits.</td></tr></table>

## A2.4.1 Credited flow control

The following rules apply to a credited channel:

• During reset the channel transmitter has no credits, the receiver has all available credits. All CRDT and CRDTSH signals must be LOW.

• Each cycle that CRDT or CRDTSH is asserted gives one credit per bit asserted, to the channel transmitter.

• The channel transmitter uses a credit each cycle that VALID is asserted.

• VALID must not be asserted when the channel transmitter has zero credits.

• The minimum number of credits that the receiver can give is 1 per resource plane.

• The maximum number of credits that the receiver can give is 15 per resource plane and 15 shared credits. There must not be combinatorial paths between credit signals and other signals on a channel in either direction. This restriction has the following consequences:

• A credit cannot be used for a transfer in the same cycle that it is given.

• A credit cannot be given in the same cycle that it is used by a transfer.

An example of transfers on a channel is shown in Figure A2.7. In this example, the receiver has two credits available.

![](images/ea965417c9d7f8d97cbef04a0cd7af10cd1e395b2228b85e0f55d79e7be95cd3.jpg)  
Figure A2.7: Example Transfers

Cycle 0 At reset the Tx has no credits.

Cycle 3 One credit is given by the Rx.

Cycle 4 The Tx uses the credit for a transfer. Another credit is given by the Rx.

Cycle 5 The Tx uses the second credit for a transfer.

Cycle 7 The credit used in cycle 4 is given back to the Tx.

Cycle 8 The Tx uses the credit for a transfer.

## A2.4.2 Resource Planes

Resource Planes (RP) are used to enable independence between traffic sharing a channel. This could be to avoid deadlock scenarios or to improve quality-of-service. Each RP has dedicated credits so it is possible to give credits for one RP, allowing it to make progress when another RP is blocked waiting for credit.

• Transfers using different Resource Planes must not block one another between transmitter and receiver.

If transfers remain on separate Resource Planes across multiple links, then the non-blocking guarantee can be extended.

The parameter Num\_RP specifies how many RPs are supported on a channel.

The RP signal indicates the Resource Plane number for each transfer, from 0 to Num\_RP-1.

The width of RP is clog2(Num\_RP). For example, if Num\_RP is 5 the width of RP is 3. If Num\_RP is 1, there is no RP signal.

Credits are given per Resource Plane. The CRDT signal has one bit per Resource Plane, therefore the receiver can give up to one credit per RP per cycle. The number of credits for each RP is permitted to be different.

• The transmitter can issue a transfer on a specific RP only if it has at least one credit for that RP.

• The receiver must be able to give at least one dedicated credit per RP supported.

• The AR, AW and W channels can have multiple RPs.

• The AW and W transfers in the same transaction must use the same RP number.

There are no ordering guarantees between transfers using different RPs. This means:

• A Manager must not issue a request transfer that has the same ID as an outstanding transaction on the same channel but a different RP.

• A Manager can interleave write data transfers for different transactions if they are using different RPs. See A5.5 Write data and response ordering.

The B and R channels have one RP.

Table A2.5 shows the properties that define the number of RPs.

Table A2.5: Resource plane number properties
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>Num_RP_AWW</td><td>1-8</td><td>1</td><td>Number of resource planes on the AW and W channels.</td></tr><tr><td>Num_RP_AR</td><td>1-8</td><td>1</td><td>Number of resource planes on the AR channel.</td></tr></table>

Connected interfaces can be configured to have a different number of RPs, but a Manager must not require the use of more RPs than can be provided by the attached Subordinate.

If the AXI\_Transport property is Ready: Num\_RP\_AWW and Num\_RP\_AR must be 1.

## A2.4.3 Shared credits

Any channel that includes multiple RPs can optionally include shared credits to improve buffer utilization when throughput varies on different RPs. A receiver supporting shared credits can allocate its buffers between those dedicated to one RP and those for any RP.

Table A2.6 shows the properties that define whether shared credits are supported.

Table A2.6: Shared credit properties
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>Shared_Credits_AW</td><td>True, False</td><td>False</td><td>If True, Shared credits are supported on the AW channel and the AWCRDTSH and AWSHAREDCRD signals are included.</td></tr><tr><td>Shared_Credits_W</td><td>True, False</td><td>False</td><td>If True, Shared credits are supported on the W channel and the WCRDTSH and WSHAREDCRD signals are included.</td></tr><tr><td>Shared_Credits_AR</td><td>True, False</td><td>False</td><td>If True, Shared credits are supported on the AR channel and the ARCRDTSH and ARSHAREDCRD signals are included.</td></tr></table>

The following rules apply:

• If the AXI\_Transport property is Ready: Shared\_Credits\_AW, Shared\_Credits\_W and Shared\_Credits\_AR must be False.

• If Num\_RP\_AWW is 1: Shared\_Credits\_AW and Shared\_Credits\_W must be False.

• If Num\_RP\_AR is 1: Shared\_Credits\_AR must be False.

• The CRDTSH signal is asserted by the receiver to give one shared credit to the transmitter. CRDTSH can be asserted without asserting CRDT.

• A transmitter can use a shared credit to send a transfer on any RP.

• A receiver must give independence guarantees between RPs, whether the transmitter is using a shared or dedicated credit.

• The SHAREDCRD signal is asserted by the transmitter alongside VALID to indicate that the transfer is using a shared credit.

It is recommended that a transmitter uses a dedicated rather than shared credit for a transfer if it has both. This is because shared credits are more flexible so could be retained for a transfer that does not have a dedicated credit.

The compatibility between Manager and Subordinate interfaces according to the values of the Shared\_Credits properties is shown in Table A2.7.

Table A2.7: Shared credits compatibility
<table><tr><td>Shared_Credits Subordinate: False</td><td></td><td>Subordinate: True</td></tr><tr><td>Manager: False Compatible.</td><td></td><td>Compatible.</td></tr><tr><td></td><td></td><td>SHAREDCRD inputs tied LOW, CRDTSH outputs unconnected.</td></tr><tr><td></td><td></td><td>Functional, but available shared credits are</td></tr><tr><td></td><td></td><td>unused.</td></tr></table>

<table><tr><td>Manager: True Compatible.</td><td></td></tr><tr><td>SHAREDCRD outputs unconnected,</td><td>Compatible.</td></tr><tr><td>CRDTSH inputs tied LOW.</td><td></td></tr><tr><td></td><td>Manager does not receive any shared credits.</td></tr></table>

An example of the use of a channel with 3 Resource Planes and shared credits is shown in Figure A2.8.  
![](images/5e3aeffcbe32e44f87fcbe1b3d20c0a13847c5007d7c489e6992c9242f8a124c.jpg)  
Figure A2.8: Example of a channel with 3 Resource Planes

Cycle 0 The Transmitter has no credits.

Cycle 1 The Receiver gives one credit for each RP and one shared credit.

Cycle 2 The Transmitter sends a transfer on RP1 using a dedicated credit.

Cycle 3 The Receiver gives a dedicated credit back to the Transmitter for RP1.

Cycle 5 The Transmitter sends a transfer on RP2 using a dedicated credit.

Cycle 6 The Transmitter sends a transfer on RP2 using a shared credit, as no dedicated credits are available.

Cycle 7 The Receiver gives a shared credit, and a dedicated credit for RP2 back to the Transmitter.

Cycle 8 The Transmitter sends a transfer on RP0 using a dedicated credit

Cycle 9 The Receiver gives a dedicated credit back to the Transmitter for RP0, along with an additional shared credit.

## A2.4.4 Transfer-level clock gating

The PENDING signal associated with a channel is guaranteed to be asserted the cycle before a transfer is sent, so can be used to gate the clock of the receiver circuitry.

The following rules apply:

• There is one PENDING signal per channel.

• It is required that PENDING is asserted in the cycle before VALID is asserted.

• When PENDING is deasserted, it is required that VALID is deasserted in the next cycle.

• When PENDING is asserted, it is permitted but not required that VALID is asserted in the next cycle.

The PENDING signal is independent of credits and credit control. For example, a transmitter is permitted to do any of the following:

• Keep PENDING permanently asserted, including during reset. It might do this if it is unable to determine in advance when a transfer is to be sent.

• Assert PENDING when it does not have a credit.

• Assert and then deassert PENDING without sending a transfer.

An example of the use of PENDING is shown in Figure A2.9.

![](images/ce29b8caff3916b8b91704351acde30aaaef90d12b291b2197775b83addf892b.jpg)  
Figure A2.9: Example usage of the PENDING signal

See A14.2 Interface gating with credited transport for information regarding gating of interfaces using credited channels.

## A2.4.5 Credited transport signals

Table A2.9 shows the signals that can be included when AXI\_Transport is Credited. Each channel also has a VALID signal, as shown in Table A2.2.

Table A2.9: Signals when using credited transport
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWPENDING</td><td>1</td><td>0b1</td><td>Asserted HIGH to indicate that a transfer might occur in the following cycle.</td></tr><tr><td>AWCRDT</td><td>Num_RP_AWW</td><td>All zeros</td><td>Asserted HIGH to give one AW credit on the respective RP.</td></tr><tr><td>AWCRDTSH</td><td>1</td><td>0b0</td><td>Asserted HIGH to give one shared AW credit, supports up to one shared credit per cycle.</td></tr><tr><td>AWRP</td><td>clog2(Num_RP_AWW)</td><td>All zeros</td><td>Encoded indicator of the Resource Plane number for an AW transfer.</td></tr><tr><td>AWSHAREDCRD</td><td>1</td><td>0b0</td><td>Asserted HIGH to indicate that an AW transfer is using a shared credit</td></tr><tr><td>WPENDING</td><td>1</td><td>0b1</td><td>Asserted HIGH to indicate that a transfer might occur in the following cycle.</td></tr><tr><td>WCRDT</td><td>Num_RP_AWW</td><td>All zeros</td><td>Asserted HIGH to give one W credit on the respective RP.</td></tr><tr><td>WCRDTSH</td><td>1</td><td>0b0</td><td>Asserted HIGH to give one shared W credit, supports up to one shared credit per cycle.</td></tr><tr><td>WRP</td><td>clog2(Num_RP_AWW)</td><td>All zeros</td><td>Encoded indicator of the Resource Plane number for a W transfer.</td></tr><tr><td>WSHAREDCRD</td><td>1</td><td>0b0</td><td>Asserted HIGH to indicate that a W transfer is using a shared credit</td></tr><tr><td>BPENDING</td><td>1</td><td>0b1</td><td>Asserted HIGH to indicate that a transfer might occur in the following cycle.</td></tr><tr><td>BCRDT</td><td>1</td><td>0b0</td><td>Asserted HIGH to give one B credit</td></tr><tr><td>ARPENDING</td><td>1</td><td>0b1</td><td>Asserted HIGH to indicate that a transfer might occur in the following cycle.</td></tr><tr><td>ARCRDT</td><td>Num_RP_AR</td><td>All zeros</td><td>Asserted HIGH to give one AR credit on the respective RP.</td></tr><tr><td>ARCRDTSH</td><td>1</td><td>0b0</td><td>Asserted HIGH to give one shared AR credit, supports up to one shared credit per cycle.</td></tr><tr><td>ARRP</td><td>clog2(Num_RP_AR)</td><td>All zeros</td><td>Encoded indicator of the Resource Plane number for an AR transfer.</td></tr><tr><td>ARSHAREDCRD</td><td>1</td><td>0b0</td><td>Asserted HIGH to indicate that an AR transfer is using a shared credit</td></tr><tr><td>RPENDING</td><td>1</td><td>0b1</td><td>Asserted HIGH to indicate that a transfer might occur in the following cycle.</td></tr><tr><td>RCRDT</td><td>1</td><td>0b0</td><td>Asserted HIGH to give one R credit.</td></tr></table>

## A2.5 Pipelining and register stages

Each AXI channel transfers information in only one direction, and the architecture does not require any fixed relationship between the channels. This means that a register stage can be inserted at any point in any channel at the cost of an additional cycle of latency.

These qualities make the following possible:

• Trade-off between cycles of latency and maximum frequency of operation.

• Direct, fast connection between a processor and high-performance memory, while using simple register slices to isolate longer paths to less performance critical peripherals.

The following rules apply to the registering of channels:

• There can be any number of register stages on VALID, READY, and CRDT paths between components.

• Different channels can have a different number of register stages, depending on their timing requirements.

• VALID signals must be pipelined by the same number of cycles as the payload signals of that channel including RP and SHAREDCRD signals, if present.

• PENDING signals must retain the relationship that they are HIGH in the cycle before VALID is HIGH.

## A2.6 AXI transactions and transfers

The AXI protocol requires the following relationships to be maintained:

• A write response must always follow the last write transfer in a write transaction.

• Read data and responses must always follow the read request.

• When a Manager issues a write request, it must be able to provide all write data for that transaction, without dependency on other transactions from that Manager.

• When a Manager has issued a write request and all write data, it must be able to accept all responses for that transaction, without dependency on other transactions from that Manager.

• When a Manager has issued a read request, it must be able to accept all read data for that transaction, without dependency on other transactions from that Manager.

– Note that a Manager can rely on read data returning in order from transactions that use the same ID, so the Manager only needs enough storage for read data from transactions with different IDs.

• A Manager is permitted to wait for one transaction to complete before issuing another transaction request.

• A Subordinate is permitted to wait for one transaction to complete before accepting another request, giving credits or sending transfers for another transaction.

• A Subordinate must not block acceptance of data-less write requests due to transactions with leading write data.

The protocol does not define any other relationship between the channels.

The lack of relationship means, for example, that the write data can appear at an interface before the write request for the transaction. This can occur if the write request channel contains more register stages than the write data channel. Similarly, the write data might appear in the same cycle as the request.

When the interconnect is required to determine the destination address space or Subordinate space, it must realign the request and write data. This realignment is required to assure that the write data is signaled as being valid only to the Subordinate for which it is destined.

## Chapter A3 AXI transactions

The AXI protocol uses transactions for communication between Managers and Subordinates. All transactions include a request and a response. Write and read transactions also include one or more data transfers.

This chapter describes the transaction requests, responses, and data transfers.

It contains the following sections:

• A3.1 Transaction request

• A3.2 Write and read data

• A3.3 Transaction response

## A3.1 Transaction request

An AXI Manager initiates a transaction by issuing a request to a Subordinate. A request includes transaction attributes and the address of the first data transfer. If the transaction includes more than one data transfer, the Subordinate must calculate the addresses of subsequent transfers.

A transaction must not cross a 4KB address boundary. This prevents a transaction from crossing a boundary between two Subordinates. It also limits the number of address increments that a Subordinate must support.

## A3.1.1 Size attribute

Size indicates the maximum number of bytes in each data transfer.

For read transactions, Size indicates how many data bytes must be valid in each read data transfer.

For write transactions, Size indicates how many data byte lanes are permitted to be active. The write strobes indicate which of those bytes are valid in each transfer.

Size must not exceed the data width of an interface, as determined by the DATA\_WIDTH property.

If Size is smaller than DATA\_WIDTH, a subset of byte lanes is used for each transfer.

Size is communicated using the AWSIZE and ARSIZE signals on the write request and read request channels, respectively. In this specification, AxSIZE indicates AWSIZE and ARSIZE.

Table A3.1: AxSIZE signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWSIZE, ARSIZE</td><td>3</td><td>log2(DATA_WIDTH/8)</td><td>Indicates the maximum number of bytes in each data transfer within a transaction.</td></tr></table>

Size is encoded on the AxSIZE signals as shown in Table A3.2.

Table A3.2: AxSIZE encodings
<table><tr><td>AxSIZE</td><td>Label Meaning</td><td></td></tr><tr><td>0b000</td><td>1</td><td>1 byte per transfer</td></tr><tr><td>0b001</td><td>2</td><td>2 bytes per transfer</td></tr><tr><td>0b010</td><td>4</td><td>4 bytes per transfer</td></tr><tr><td>0b011</td><td>8</td><td>8 bytes per transfer</td></tr><tr><td>0b100</td><td>16</td><td>16 bytes per transfer</td></tr><tr><td>0b101</td><td>32</td><td>32 bytes per transfer</td></tr><tr><td>0b110</td><td>64</td><td>64 bytes per transfer</td></tr><tr><td>0b111</td><td>128</td><td>128 bytes per transfer</td></tr></table>

The property SIZE\_Present is used to determine if the AxSIZE signals are present.

Table A3.3: SIZE\_Present property
<table><tr><td>SIZE_Present Default Description</td><td></td><td></td></tr><tr><td>True</td><td>Y</td><td>AWSIZE and ARSIZE are present.</td></tr><tr><td>False</td><td></td><td>AWSIZE and ARSIZE are not present.</td></tr></table>

A Manager that only issues requests of full data width can omit the AxSIZE outputs from its interface. An attached Subordinate must have its AxSIZE input tied according to the data width.

## A3.1.2 Length attribute

The Length attribute defines the number of data transfers in a transaction.

Size x Length is the maximum number of bytes that can be transferred in a transaction. If the address is unaligned or there are deasserted write strobes, the actual number of bytes transferred can be lower than Size x Length.

A Manager must issue the number of write data transfers according to Length.

A Subordinate must issue the number of read data transfers according to Length.

Length is communicated using the AWLEN and ARLEN signals on the write request and read request channels, respectively. In this specification, AxLEN indicates AWLEN and ARLEN.

Table A3.4: AxLEN signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWLEN, ARLEN</td><td>8</td><td>0x00</td><td>The total number of transfers in a transaction, encoded as: Length = AxLEN + 1.</td></tr></table>

The property LEN\_Present is used to determine if the signals are present. Table A3.5 shows the legal values of LEN\_Present.

Table A3.5: LEN\_Present property
<table><tr><td></td><td>LEN_Present Default Description</td><td></td></tr><tr><td>True</td><td>Y</td><td>AWLEN and ARLEN are present.</td></tr><tr><td>False</td><td></td><td>AWLEN and ARLEN are not present.</td></tr></table>

A Manager that only issues requests of Length 1 can omit the AxLEN outputs from its interface. An attached Subordinate must have its AxLEN input tied to 0x00.

The following rules apply to transaction Length:

• For wrapping bursts, Length can be 2, 4, 8, or 16.

• For fixed bursts, Length can be up to 16.

• A transaction must not cross a 4KB address boundary.

• Early termination of transactions is not supported.

No component can terminate a transaction early. However, to reduce the number of data transfers in a write transaction, the Manager can disable further writing by deasserting all the write strobes. In this case, the Manager must complete the remaining transfers in the transaction. In a read transaction, the Manager can discard read data, but it must complete all transfers in the transaction.

## A3.1.3 Maximum number of bytes in a transaction

The maximum number of bytes in a transaction is 4KB and transactions are not permitted to cross a 4KB boundary.   
However, many Managers generate transactions which are always smaller than this.

A Subordinate or interconnect might benefit from this information. For example, a Subordinate might be able to optimize away some decode logic. An interconnect striping at a granule smaller than 4KB might be able to avoid burst splitting if it knows that transactions will not cross the stripe boundary.

The property Max\_Transaction\_Bytes defines the maximum size of a transaction in bytes as shown in Table A3.6.

Table A3.6: Max\_Transaction\_Bytes property
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>Max_Transaction_Bytes</td><td>64, 128, 256, 512, 1024,</td><td>4096</td><td>A Manager issues transactions where Size x Length is Max_Transaction_Bytes or smaller and do not cross a</td></tr><tr><td></td><td>2048, 4096</td><td></td><td>Max_Transaction_Bytes boundary. cross a Max_Transaction_Bytes boundary.</td></tr><tr><td></td><td></td><td></td><td>A Subordinate can only accept transactions where Size x Length is Max_Transaction_Bytes or smaller and do not</td></tr></table>

When connecting Manager and Subordinate interfaces, Table A3.7 indicates combinations of Max\_Transaction\_Bytes that are compatible.

Table A3.7: Max\_Transaction\_Bytes interoperability
<table><tr><td></td><td>Manager &lt; Subordinate Manager == Subordinate Manager &gt; Subordinate</td><td></td></tr><tr><td>Compatible.</td><td>Compatible.</td><td>Not compatible.</td></tr></table>

## A3.1.4 Burst attribute

The Burst attribute describes how the address increments between transfers in a transaction.

Burst is communicated using the AWBURST and ARBURST signals on the write request and read request channels, respectively. In this specification, AxBURST indicates AWBURST and ARBURST.

Table A3.8: AxBURST signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWBURST, ARBURST</td><td>2</td><td>0b01 (INCR)</td><td>Describes how the address increments between transfers in a transaction.</td></tr></table>

Burst is encoded on the AxBURST signals as shown in Table A3.9.

Table A3.9: AxBURST encodings
<table><tr><td>AxBURST</td><td>Label</td><td>Meaning</td></tr><tr><td>0b00</td><td>FIXED</td><td>Fixed burst</td></tr><tr><td>0b01</td><td>INCR</td><td>Incrementing burst</td></tr><tr><td>0b10</td><td>WRAP</td><td>Wrapping burst</td></tr><tr><td>0b11</td><td>RESERVED</td><td></td></tr></table>

The property BURST\_Present is used to determine if the AxBURST signals are present.

A Manager that only issues requests with a Burst type of INCR can omit the AxBURST outputs from its interface.   
An attached Subordinate must have its AxBURST input tied to 0b01.

Table A3.10: BURST\_Present property
<table><tr><td>BURST_Present Default Description</td><td></td><td></td></tr><tr><td>True</td><td>Y</td><td>AWBURST and ARBURST are present.</td></tr><tr><td>False</td><td></td><td>AWBURST and ARBURST are not present.</td></tr></table>

There are three different Burst types:

## Incrementing address (INCR)

With this Burst type, the address for each transfer is an increment of the address for the previous transfer. The increment value depends on the transaction Size. For example, for an aligned start address, the address for each transfer in a transaction with a Size of 4 bytes is the previous address plus 4. This Burst type is used for accesses to normal sequential memory.

## Wrapping address (WRAP)

This Burst type is similar to INCR except that the address wraps around to a lower address if an upper address limit is reached. The following restrictions apply:

• The start address must be aligned to the size of each transfer.

• The Length of the burst must be 2, 4, 8, or 16 transfers.

The behavior of a wrapping transaction is:

• The lowest address accessed by the transaction is the start address aligned to the total size of the data to be transferred, that is Size <sub>\*</sub> Length. This address is defined as the wrap boundary.

• After each transfer, the address increments in the same way as for an INCR burst. However, if this incremented address is ((wrap boundary)+ (Size <sub>\*</sub> Length)), then the address wraps round to the wrap boundary.

• The first transfer in the transaction can use an address that is higher than the wrap boundary, subject to the restrictions that apply to wrapping transactions. The address wraps when the first address is higher than the wrap boundary. This Burst type is used for cache line accesses.

Wrapping bursts are primarily intended for reading and writing cache lines. The property Wrap\_CLS\_Modifiable can be used to limit wrapping bursts to being cache line sized and Modifiable (AxCACHE[1] is 0b1). Constraining wrapping bursts using this property can simplify the design of decoders and bridges converting between protocols or data widths.

Table A3.11 describes the Wrap\_CLS\_Modifiable property.

Table A3.11: Wrap\_CLS\_Modifiable property
<table><tr><td></td><td>Wrap_CLS_Modifiable Default Description</td><td></td></tr><tr><td>True</td><td></td><td>When Burst type is WRAP, the transaction must be cache line sized and Modifiable.</td></tr><tr><td>False</td><td>Y</td><td>When Burst type is WRAP, the transaction is not required to be cache line sized and can be Non-modifiable.</td></tr></table>

Note that a wrapping AtomicCompare is not affected by this property, see A6.4 Atomic transactions.

Table A3.12 shows compatibility for the Wrap\_CLS\_Modifiable property.

Table A3.12: Wrap\_CLS\_Modifiable compatibility
<table><tr><td>Wrap_CLS_Modifiable</td><td>Subordinate: False</td><td>Subordinate: True</td></tr><tr><td>Manager: False</td><td>Compatible.</td><td>Not compatible.</td></tr><tr><td>Manager: True</td><td>Compatible.</td><td>Compatible.</td></tr></table>

## Fixed address (FIXED)

This Burst type is used for repeated accesses to the same location such as when loading or emptying a FIFO.

• The address is the same for every transfer in the burst.

• The byte lanes that are valid are constant for all transfers. However, within those byte lanes, the actual bytes that have WSTRB asserted can differ for each transfer.

• The Length of the burst can be up to 16 transfers.

• The FIXED burst type can only be used with WriteNoSnoop or ReadNoSnoop Opcodes. See Chapter A7 Request Opcodes for more information.

A Burst type of FIXED is not commonly used, and a property Fixed\_Burst\_Disable is defined in Table A3.13 to indicate if a component supports it.

Table A3.13: Fixed\_Burst\_Disable property
<table><tr><td>Fixed_Burst_Disable Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>Requests with Burst type FIXED are not supported by a Subordinate interface and not generated by a Manager interface.</td></tr><tr><td>False</td><td>Y</td><td>Requests with Burst type FIXED are supported by a Subordinate interface and might be generated by a Manager interface.</td></tr></table>

Compatibility between Manager and Subordinate interfaces, according to the values of the Fixed\_Burst\_Disable property is shown in Table A3.14.

Table A3.14: Fixed\_Burst\_Disable compatibility
<table><tr><td>Fixed_Burst_Disable</td><td>Subordinate: False</td><td>Subordinate: True</td></tr><tr><td>Manager: False</td><td>Compatible.</td><td>Not compatible.</td></tr><tr><td>Manager: True</td><td>Compatible.</td><td>Compatible.</td></tr></table>

## A3.1.5 Transfer address

This section provides methods for determining the address and byte lanes of transfers within a transaction.

The start address for a transaction is indicated using the AxADDR signals.

Table A3.15: AxADDR signals
<table><tr><td>Name</td><td>Width</td><td>Default Description</td><td></td></tr><tr><td>AWADDR, ARADDR</td><td>ADDR_WIDTH</td><td></td><td>Address of first transfer in a transaction.</td></tr></table>

## Address width

The property ADDR\_WIDTH is used to define the address width.

Table A3.16: ADDR\_WIDTH property
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>ADDR_WIDTH</td><td>1..64</td><td>32</td><td>Width of AWADDR, ARADDR, and ACADDR in bits.</td></tr></table>

The protocol supports communication between components that have different physical address space sizes. Components with different physical address space sizes must communicate as follows:

• The component with the smaller physical address space must be positioned within an aligned window in the larger physical address space. Typically, the window is located at the bottom of the larger physical address space. However, it is acceptable for the component with the smaller physical address space to be positioned in an offset window within the larger physical address space.

• An outgoing transaction must have the required additional higher-order bits added to the transaction address.

• An incoming transaction must be examined so that:

– A transaction that is within the address window has the higher-order address bits removed and is passed through.

– A transaction that does not have the required higher-order address bits is suppressed.

It is the responsibility of the interconnect to provide the required functionality.

## A3.1.6 Transaction equations

The equations listed here are used to determine the address and active data byte lanes for each transfer in a transaction. The equations use the following additional variables:

• Start\_Addr: The start address that is issued by the Manager.

• Data\_Bytes: The width of the data channels in bytes (DATA\_WIDTH/8).

• Aligned\_Addr: The aligned version of the start address.

• Address\_N: The address of transfer N in a transaction. N is 1 for the first transfer in a transaction.

• Wrap\_Boundary: The lowest address within a wrapping transaction.

• Lower\_Byte\_Lane: The byte lane of the lowest addressed byte of a transfer.

• Upper\_Byte\_Lane: The byte lane of the highest addressed byte of a transfer.

• INT(x): The rounded-down integer value of x.

These equations determine addresses of transfers within a burst:

```python
Start_Addr = AxADDR
```

Aligned\_Addr = INT(Start\_Addr / Size)<sub>\*</sub> Size

This equation determines the address of the first transfer in a burst:

Address\_1 = Start\_Addr

For an INCR burst and for a WRAP burst for which the address has not wrapped, this equation determines the address of any transfer after the first transfer in a burst:

Address\_N = Aligned\_Addr + (N - 1)<sub>\*</sub> Size

For a WRAP burst, the Wrap\_Boundary variable defines the wrapping boundary:

Wrap\_Boundary = INT(Start\_Addr / (Size <sub>\*</sub> Length))<sub>\*</sub> Size <sub>\*</sub> Length

For a WRAP burst, if Address\_N = Wrap\_Boundary + Size <sub>\*</sub> Length, then:

• Use this equation for the current transfer:

Address\_N = Wrap\_Boundary

• Use this equation for any subsequent transfers:

Address\_N = Aligned\_Addr + ((N - 1)<sub>\*</sub> Size)- (Size <sub>\*</sub> Length)

These equations determine the byte lanes to use for the first transfer in a burst:

```c
Lower_Byte_Lane = Start_Addr - (INT(Start_Addr/Data_Bytes)<sub>*</sub> Data_Bytes)
```

Upper\_Byte\_Lane = Aligned\_Addr + (Size-1)- (INT(Start\_Addr/Data\_Bytes)<sub>\*</sub> Data\_Bytes)

These equations determine the byte lanes to use for all transfers after the first transfer in a burst:

Lower\_Byte\_Lane = Address\_N - (INT(Address\_N / Data\_Bytes)<sub>\*</sub> Data\_Bytes)

Upper\_Byte\_Lane = Lower\_Byte\_Lane + Size - 1

Data is transferred on:

DATA((8 <sub>\*</sub> Upper\_Byte\_Lane)+ 7: (8 <sub>\*</sub> Lower\_Byte\_Lane))

The transaction container describes all the bytes that could be accessed in that transaction, if the address is aligned and strobes are asserted:

Container\_Size = Size <sub>\*</sub> Length

For INCR bursts:

Container\_Lower = Aligned\_Addr

Container\_Upper = Aligned\_Addr + Container\_Size

For WRAP bursts:

Container\_Lower = Wrap\_Boundary

Container\_Upper = Wrap\_Boundary + Container\_Size

## A3.1.7 Pseudocode description of the transfers

```c
// DataTransfer()
DataTransfer(Start_Addr, Size, Length, Data_Bytes, Burst, IsWrite)
// IsWrite is TRUE for a write, and FALSE for a read
addr = Start_Addr; // Variable for current address
Aligned_Addr = (INT(addr/Size) Size);
aligned = (Aligned_Addr == addr); // Check whether addr aligned to Size
Container_Size = Size <sub>*</sub> Length;
if Burst == WRAP then
Lower_Wrap_Boundary = (INT(addr/Container_Size) <sub>*</sub> Container_Size);
// addr must be aligned for a wrapping burst
Upper_Wrap_Boundary = Lower_Wrap_Boundary + Container_Size;
for n = 1 to Length
Lower_Byte_Lane = addr - (INT(addr/Data_Bytes) <sub>*</sub> Data_Bytes);
if aligned then
Upper_Byte_Lane = Lower_Byte_Lane + Size - 1
else
Upper_Byte_Lane = Aligned_Addr + Size - 1
- (INT(addr/Data_Bytes) <sub>*</sub> Data_Bytes);
// Perform data transfer
if IsWrite then
dwrite(addr, Lower_Byte_Lane, Upper_Byte_Lane)
else
dread(addr, Lower_Byte_Lane, Upper_Byte_Lane);
// Increment address if necessary
if Burst != FIXED then
if aligned then
addr = addr + Size;
if Burst == WRAP then
if addr >= Upper_Wrap_Boundary then addr = Lower_Wrap_Boundary;
else
addr = Aligned_Addr + Size;
aligned = TRUE; // All transfers after the first are aligned
return;
```

## A3.1.8 Regular transactions

There are many options of burst, size, and length for a transaction. However, some interfaces and transaction types might only use a subset of these options. If a Subordinate component is attached to a Manager which uses only a subset of transaction options, it can be designed with simplified decode logic.

The Regular attribute is defined, to identify transactions which meet the following criteria:

• Length is 1, 2, 4, 8, or 16 transfers.

• Size is the same as the data channel width if Length is greater than 1.

• Burst is INCR or WRAP, not FIXED.

• Address is aligned to the transaction container for INCR transactions.

• Address is aligned to Size for WRAP transactions.

The Regular\_Transactions\_Only property is used to define whether a Manager issues only Regular type transactions and if a Subordinate only supports Regular transactions.

Table A3.17: Regular\_Transactions\_Only property
<table><tr><td>Regular_Transactions_Only Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>Only Regular transactions are issued/supported.</td></tr><tr><td>False</td><td>Y</td><td>All legal combinations of Burst, Size, and Length are issued/supported.</td></tr></table>

Interoperability rules for Regular transactions are shown in Table A3.18.

Table A3.18: Regular\_Transactions\_Only interoperability
<table><tr><td></td><td>Subordinate: False Subordinate: True</td><td></td></tr><tr><td>Manager: False Compatible.</td><td></td><td>Not compatible. If the Manager issues a transaction that is not Regular,</td></tr><tr><td></td><td></td><td>then data corruption or deadlock might occur.</td></tr><tr><td>Manager: True Compatible.</td><td></td><td>Compatible.</td></tr></table>

## A3.2 Write and read data

This section describes the AXI write and read data channels and how the interface performs mixed-endian and unaligned transfers.

Write and read data signals have the same width, specified using the DATA\_WIDTH property.

Table A3.19: DATA\_WIDTH property
<table><tr><td>Name</td><td>Values</td><td>Default Description</td><td></td></tr><tr><td>DATA_WIDTH</td><td>I 8, 16, 32, 64, 128, 256, 512, 1024</td><td></td><td>Data width in bits, applies to RDATA and WDATA.</td></tr></table>

## A3.2.1 Write data channel (W)

The data and last signals for the write data channel are shown in Table A3.20.

Table A3.20: Write data signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>WDATA</td><td>DATA_WIDTH</td><td></td><td>The write data signal carries data between a Manager and Subordinate in a write transaction.</td></tr><tr><td>WLAST</td><td>1</td><td></td><td>Indicates the last write data transfer of a transaction.</td></tr></table>

The following rules apply:

• The Manager must assert the WLAST signal while it is driving the final write transfer in the transaction.

• It is recommended that WDATA is driven to zero for inactive byte lanes.

• A Subordinate that does not use WLAST can omit the input from its interface.

The property WLAST\_Present is used to determine if the WLAST signal is present.

Table A3.21: WLAST\_Present property
<table><tr><td>WLAST_Present</td><td>Default</td><td>Description</td></tr><tr><td>True</td><td>Y</td><td>WLAST is present.</td></tr><tr><td>False</td><td></td><td>WLAST is not present.</td></tr></table>

## A3.2.1.1 Write strobes

The WSTRB signal carries write strobes that specify which byte lanes of the write data channel contain valid information.

Table A3.22: WSTRB signal
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>WSTRB</td><td>DATA_WIDTH / 8</td><td>All ones</td><td>Indicates which byte lanes of WDATA contain valid data in a write transaction.</td></tr></table>

There is one write strobe for each 8 bits of the write data channel, therefore WSTRB[n] corresponds to WDATA[(8n)+7:(8n)].

## When WVALID is HIGH:

• Data bytes to be written have a corresponding write strobe set HIGH.

• Inside of the transaction container any number of write strobes can be HIGH. If all write strobes are LOW, no data is written from that transfer.

• Outside of the transaction container all write strobes must be LOW.

## When WVALID is LOW:

• Write strobes can take any value, although it is recommended that they are either driven LOW or held at their previous value.

• It is recommended that WDATA is driven to zero for byte lanes where the strobe is LOW.

The property WSTRB\_Present is used to indicate if the WSTRB signal is present on an interface.

Table A3.23: WSTRB\_Present property
<table><tr><td>WSTRB_Present Default</td><td></td><td>Description</td></tr><tr><td>True</td><td>Y</td><td>WSTRB is present.</td></tr><tr><td>False</td><td></td><td>WSTRB is not present.</td></tr></table>

A Manager that only issues transactions where all write strobes are asserted can omit the WSTRB output from its interface. An attached Subordinate must have its WSTRB input tied HIGH.

## A3.2.2 Read data channel (R)

The read data and last signals are shown in Table A3.24.

Table A3.24: Read data channel control signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>RDATA</td><td>DATA_WIDTH</td><td></td><td>The read data signal carries data between a Subordinate and Manager in a read transaction.</td></tr><tr><td>RLAST</td><td>1</td><td></td><td>Indicates the last read data transfer of a transaction.</td></tr></table>

The following rules apply:

• Even if a Subordinate has only one source of read data, it must assert the RVALID signal only in response to a request.

• The Subordinate must assert the RLAST signal when it is driving the final read transfer in the transaction.

• It is recommended that RDATA is driven to zero for inactive byte lanes.

• A Manager that does not use RLAST can omit the input from its interface.

The property RLAST\_Present is used to determine if the RLAST signal is present.

Table A3.25: RLAST\_Present property
<table><tr><td>RLAST_Present</td><td> Default</td><td>Description</td></tr><tr><td>True</td><td>Y</td><td>RLAST is present.</td></tr><tr><td>False</td><td></td><td>RLAST is not present.</td></tr></table>

## A3.2.3 Narrow transfers

When a Manager generates a transfer that is narrower than its data channel, the address and control information determine the byte lanes that the transfer uses:

• When Burst is INCR or WRAP, different byte lanes are used for each data transfer in the transaction.

• When Burst is FIXED, the same byte lanes are used for each data transfer in the transaction.

Two examples of byte lane use are shown in Figure A3.1 and Figure A3.2. The shaded cells indicate bytes that are not transferred.

In Figure A3.1:

• The transaction has five data transfers.

• The starting address is 0.

• Each transfer is 8 bits.

• The transfers are on a 32-bit data channel.

• The burst type is INCR.

<table><tr><td>31</td><td>2423</td><td>1615</td><td>8 17</td><td>0</td><td></td></tr><tr><td></td><td></td><td></td><td></td><td>D[7:0]</td><td>1st transfer</td></tr><tr><td></td><td></td><td>D[15:8]</td><td></td><td></td><td>2nd transfer</td></tr><tr><td></td><td>D[23:16]</td><td></td><td></td><td></td><td>3rd transfer</td></tr><tr><td>D[31:24]</td><td></td><td></td><td></td><td></td><td>4th transfer</td></tr><tr><td></td><td></td><td></td><td></td><td>D[7:0]</td><td>5th transfer</td></tr><tr><td colspan="6"></td></tr></table>

Figure A3.1: Narrow transfer example with 8-bit transfers

In Figure A3.2:

• The transaction has three data transfers.

• The starting address is 4.

• Each transfer is 32 bits.

• The transfers are on a 64-bit data channel.

<table><tr><td rowspan=1 colspan=1>63       565</td><td rowspan=1 colspan=1>5       48</td><td rowspan=1 colspan=1>47       40</td><td rowspan=1 colspan=1>39       323</td><td rowspan=1 colspan=1>1       242</td><td rowspan=1 colspan=1>3        16</td><td rowspan=1 colspan=1>15        8</td><td rowspan=1 colspan=1>7        0</td><td rowspan=5 colspan=1>1st transfer2nd transfer3rd transfer</td></tr><tr><td rowspan=1 colspan=1>D[63:56]</td><td rowspan=1 colspan=1>D[55:48]</td><td rowspan=1 colspan=1>D[47:40]</td><td rowspan=1 colspan=1>D[39:32]</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>D[31:24]</td><td rowspan=1 colspan=1>D[23:16]</td><td rowspan=1 colspan=1>D[15:8]</td><td rowspan=1 colspan=1>D[7:0]</td></tr><tr><td rowspan=1 colspan=1>D[63:56]</td><td rowspan=1 colspan=1>D[55:48]</td><td rowspan=1 colspan=1>D[47:40]</td><td rowspan=1 colspan=1>D[39:32]</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=9></td></tr></table>

WDATA[63:0]

Figure A3.2: Narrow transfer example with 32-bit transfers

## A3.2.4 Byte invariance

To access mixed-endian data structures in a single memory space, the AXI protocol uses a byte-invariant endianness scheme.

Byte-invariant endianness means that for any multi-byte element in a data structure:

• The element uses the same continuous bytes of memory, regardless of the endianness of the data.

• The endianness determines the order of those bytes in memory, meaning it determines whether the first byte in memory is the most significant byte (MSB) or the least significant byte (LSB) of the element.

• Any byte transfer to an address passes the 8 bits of data on the same data channel wires to the same address location, regardless of the endianness of any larger data element that it is a constituent of.

Components that have only one transfer width must have their byte lanes connected to the appropriate byte lanes of the data channel. Components that support multiple transfer widths might require a more complex interface to convert an interface that is not naturally byte-invariant.

Most little-endian components can connect directly to a byte-invariant interface. Components that support only big-endian transfers require a conversion function for byte-invariant operation.

The examples in Figure A3.3 and Figure A3.4 show a 32-bit number 0x0A0B0C0D, stored in a register and in a memory.

In Figure A3.3 there is an example of the big-endian, byte-invariant data structure. In this structure:

• The MSB of the data, which is $0 \times 0 \mathbb { A } .$ is stored in the MSB position in the register.

• The MSB of the data is stored in the memory location with the lowest address.

• The other data bytes are positioned in decreasing order of significance.

![](images/7385ec3cfdea9d976aa708649f907d784d79d77a52fc141026e16d28199bad1a.jpg)  
Figure A3.3: Example big-endian byte-invariant data structure

In Figure A3.4 there is an example of a little-endian, byte-invariant data structure. In this structure:

• The LSB of the data, which is $0 \times 0 \mathrm { D } ,$ is stored in the LSB position in the register.

• The LSB of the data is stored in the memory location with the lowest address.

• The other data bytes are positioned in increasing order of significance.

![](images/7d919b0a9aa48fbfcbc504b4ea78005303327bbf5630baf40580b13184a16b3a.jpg)  
Figure A3.4: Example little-endian byte-invariant data structure

The examples in Figure A3.3 and Figure A3.4 show that byte invariance ensures that big-endian and little-endian structures can coexist in a single memory space without corruption.

In Figure A3.5 there is an example of a data structure that requires byte-invariant access. In this example, the header fields use little-endian ordering, and the payload uses big-endian ordering.

![](images/6b1f3d21f87b2f6d32309187fd8776a0477c5ba74f926d90c46e107c0765fed1.jpg)  
† 16-bit continuous Destination field  
Figure A3.5: Example mixed-endian data structure

In this example structure, Data items is a two-byte little-endian element, meaning its lowest address is its LSB. The use of byte invariance ensures that a big-endian access to the payload does not corrupt the little-endian element.

## A3.2.5 Unaligned transfers

AXI supports unaligned transfers. For any transaction that is made up of data transfers wider than 1 byte, the first bytes accessed might be unaligned with the natural address boundary. For example, a 32-bit data packet that starts at a byte address of 0x1002 is not aligned to the natural 32-bit address boundary.

A Manager can:

• Use the low-order address lines to signal an unaligned start address.

• Provide an aligned address and use the byte lane strobes to signal the unaligned start address.

The information on the low-order address lines must be consistent with the information on the byte lane strobes.

The Subordinate is not required to take special action based on any alignment information from the Manager.

In Figure A3.6 there are examples of aligned and unaligned 32-bit transactions on a 32-bit data channel. Each row in the figure represents a transfer and the shaded cells indicate bytes that are not transferred.

Address: 0x00   
Transfer size: 32-bits   
Burst type: incrementing   
Burst length: 4 transfers   
Address: 0x01   
Transfer size: 32-bits   
Burst type: incrementing   
Burst length: 4 transfers

Address: 0x01 Transfer size: 32-bits Burst type: incrementing Burst length: 5 transfers

Address: 0x07 Transfer size: 32-bits Burst type: incrementing Burst length: 5 transfers

<table><tr><td rowspan=2 colspan=1>31    242</td><td></td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>3    161</td><td rowspan=1 colspan=1>5     83I</td><td rowspan=1 colspan=1>17       o</td></tr><tr><td rowspan=1 colspan=1>0x03</td><td rowspan=1 colspan=1>0x02</td><td rowspan=1 colspan=1>0x01</td><td rowspan=1 colspan=1>0x00</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x07</td><td rowspan=1 colspan=1>0x06</td><td rowspan=1 colspan=1>0x05</td><td rowspan=1 colspan=1>0x04</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x0B</td><td rowspan=1 colspan=1>0x0A</td><td rowspan=1 colspan=1>0x09</td><td rowspan=1 colspan=1>0x08</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x0F</td><td rowspan=1 colspan=1>0x0E</td><td rowspan=1 colspan=1>0x0D</td><td rowspan=1 colspan=1>0x0C</td></tr></table>

WDATA[31:0]

<table><tr><td rowspan=1 colspan=1>31    242</td><td rowspan=1 colspan=1>3    161</td><td rowspan=1 colspan=1>5     8</td><td rowspan=1 colspan=1>7      0</td></tr><tr><td rowspan=1 colspan=1>0x03</td><td rowspan=1 colspan=1>0x02</td><td rowspan=1 colspan=1>0x01</td><td rowspan=1 colspan=1>0x00</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x07</td><td rowspan=1 colspan=1>0x06</td><td rowspan=1 colspan=1>0x05</td><td rowspan=1 colspan=1>0x04</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x0B</td><td rowspan=1 colspan=1>0x0A</td><td rowspan=1 colspan=1>0x09</td><td rowspan=1 colspan=1>0x08</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x0F</td><td rowspan=1 colspan=1>0x0E</td><td rowspan=1 colspan=1>0x0D</td><td rowspan=1 colspan=1>0x0C</td></tr></table>

WDATA[31:0]

<table><tr><td rowspan=1 colspan=1>31    242</td><td rowspan=1 colspan=1>3    16</td><td rowspan=1 colspan=1>15    8</td><td rowspan=1 colspan=1>7     0</td><td rowspan=11 colspan=1>1st transfer2nd transfer3rd transfer4th transfer5th transfer</td></tr><tr><td rowspan=1 colspan=1>0x03</td><td rowspan=1 colspan=1>0x02</td><td rowspan=1 colspan=1>0x01</td><td rowspan=1 colspan=1>0x00</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x07</td><td rowspan=1 colspan=1>0x06</td><td rowspan=1 colspan=1>0x05</td><td rowspan=1 colspan=1>0x04</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x0B</td><td rowspan=1 colspan=1>0x0A</td><td rowspan=1 colspan=1>0x09</td><td rowspan=1 colspan=1>0x08</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x0F</td><td rowspan=1 colspan=1>0x0E</td><td rowspan=1 colspan=1>0x0D</td><td rowspan=1 colspan=1>0x0C</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x13</td><td rowspan=1 colspan=1>0x12</td><td rowspan=1 colspan=1>0x11</td><td rowspan=1 colspan=1>0x10</td></tr><tr><td rowspan=1 colspan=4></td></tr></table>

WDATA[31:0]

<table><tr><td rowspan=1 colspan=1>31    242</td><td rowspan=1 colspan=1>3    161</td><td rowspan=1 colspan=1>5    8</td><td rowspan=1 colspan=1>7     0</td></tr><tr><td rowspan=1 colspan=1>0x07</td><td rowspan=1 colspan=1>0x06</td><td rowspan=1 colspan=1>0x05</td><td rowspan=1 colspan=1>0x04</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x0B</td><td rowspan=1 colspan=1>0x0A</td><td rowspan=1 colspan=1>0x09</td><td rowspan=1 colspan=1>0x08</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x0F</td><td rowspan=1 colspan=1>0x0E</td><td rowspan=1 colspan=1>0x0D</td><td rowspan=1 colspan=1>0x0C</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x13</td><td rowspan=1 colspan=1>0x12</td><td rowspan=1 colspan=1>0x11</td><td rowspan=1 colspan=1>0x10</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x17</td><td rowspan=1 colspan=1>0x16</td><td rowspan=1 colspan=1>0x15</td><td rowspan=1 colspan=1>0x14</td></tr></table>

Figure A3.6: Aligned and unaligned transfers on a 32-bit data channel

In Figure A3.7 there are examples of aligned and unaligned 32-bit transactions on a 64-bit data channel. Each row

Address: 0x00   
Transfer size: 32-bits   
Burst type: incrementing   
Burst length: 4 transfers   
Address: 0x07   
Transfer size: 32-bits   
Burst type: incrementing   
Burst length: 4 transfers

in the figure represents a transfer and the shaded cells indicate bytes that are not transferred.
<table><tr><td rowspan=1 colspan=1>63   565</td><td rowspan=1 colspan=1>5   484</td><td rowspan=1 colspan=1>7   403</td><td rowspan=1 colspan=1>9   323</td><td rowspan=1 colspan=1>1   242</td><td rowspan=1 colspan=1>3   161</td><td rowspan=1 colspan=1>5    8</td><td rowspan=1 colspan=1>7     0</td></tr><tr><td rowspan=1 colspan=1>0x07</td><td rowspan=1 colspan=1>0x06</td><td rowspan=1 colspan=1>0x05</td><td rowspan=1 colspan=1>0x04</td><td rowspan=1 colspan=1>0x03</td><td rowspan=1 colspan=1>0x02</td><td rowspan=1 colspan=1>0x01</td><td rowspan=1 colspan=1>0x00</td></tr><tr><td rowspan=1 colspan=1>]</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x07</td><td rowspan=1 colspan=1>0x06</td><td rowspan=1 colspan=1>0x05</td><td rowspan=1 colspan=1>0x04</td><td rowspan=1 colspan=1>0x03</td><td rowspan=1 colspan=1>0x02</td><td rowspan=1 colspan=1>0x01</td><td rowspan=1 colspan=1>0x00</td></tr><tr><td rowspan=1 colspan=1>0x0F</td><td rowspan=1 colspan=1>0x0E</td><td rowspan=1 colspan=1>0x0D</td><td rowspan=1 colspan=1>0x0C</td><td rowspan=1 colspan=1>0x0B</td><td rowspan=1 colspan=1>0x0A</td><td rowspan=1 colspan=1>0x09</td><td rowspan=1 colspan=1>0x08</td></tr><tr><td rowspan=1 colspan=1>0x0F</td><td rowspan=1 colspan=1>0x0E</td><td rowspan=1 colspan=1>0x0D</td><td rowspan=1 colspan=1>0x0C</td><td rowspan=1 colspan=1>0x0B</td><td rowspan=1 colspan=1>0x0A</td><td rowspan=1 colspan=1>0x09</td><td rowspan=1 colspan=1>0x08</td></tr></table>

<table><tr><td rowspan=1 colspan=1>63   56</td><td rowspan=1 colspan=1>55   48</td><td rowspan=1 colspan=1>47   403</td><td rowspan=1 colspan=1>9   323</td><td rowspan=1 colspan=1>1   24</td><td rowspan=1 colspan=1>23   16</td><td rowspan=1 colspan=1>15    8</td><td rowspan=1 colspan=1>7     0</td></tr><tr><td rowspan=1 colspan=1>0x07</td><td rowspan=1 colspan=1>0x06</td><td rowspan=1 colspan=1>0x05</td><td rowspan=1 colspan=1>0x04</td><td rowspan=1 colspan=1>0x03</td><td rowspan=1 colspan=1>0x02</td><td rowspan=1 colspan=1>0x01</td><td rowspan=1 colspan=1>0x00</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x0F</td><td rowspan=1 colspan=1>0x0E</td><td rowspan=1 colspan=1>0x0D</td><td rowspan=1 colspan=1>0x0C</td><td rowspan=1 colspan=1>0x0B</td><td rowspan=1 colspan=1>0x0A</td><td rowspan=1 colspan=1>0x09</td><td rowspan=1 colspan=1>0x08</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x0F</td><td rowspan=1 colspan=1>0x0E</td><td rowspan=1 colspan=1>0x0D</td><td rowspan=1 colspan=1>0x0C</td><td rowspan=1 colspan=1>0x0B</td><td rowspan=1 colspan=1>0x0A</td><td rowspan=1 colspan=1>0x09</td><td rowspan=1 colspan=1>0x08</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x17</td><td rowspan=1 colspan=1>0x16</td><td rowspan=1 colspan=1>0x15</td><td rowspan=1 colspan=1>0x14</td><td rowspan=1 colspan=1>0x13</td><td rowspan=1 colspan=1>0x12</td><td rowspan=1 colspan=1>0x11</td><td rowspan=1 colspan=1>0x10</td></tr></table>

Address: 0x07 Transfer size: 32-bits Burst type: incrementing Burst length: 5 transfers

<table><tr><td rowspan=1 colspan=1>63   565</td><td rowspan=1 colspan=1>5   48</td><td rowspan=1 colspan=1>47   403</td><td rowspan=1 colspan=1>9   323</td><td rowspan=1 colspan=1>1   242</td><td rowspan=1 colspan=1>3   161</td><td rowspan=1 colspan=2>5    817      0</td></tr><tr><td rowspan=1 colspan=1>0x07</td><td rowspan=1 colspan=1>0x06</td><td rowspan=1 colspan=1>0x05</td><td rowspan=1 colspan=1>0x04</td><td rowspan=1 colspan=1>0x03</td><td rowspan=1 colspan=1>0x02</td><td rowspan=1 colspan=1>0x01</td><td rowspan=1 colspan=1>0x00</td></tr><tr><td rowspan=1 colspan=1>0x0F</td><td rowspan=1 colspan=1>0x0E</td><td rowspan=1 colspan=1>0x0D</td><td rowspan=1 colspan=1>0x0C</td><td rowspan=1 colspan=1>0x0B</td><td rowspan=1 colspan=1>0x0A</td><td rowspan=1 colspan=1>0x09</td><td rowspan=1 colspan=1>0x08</td></tr><tr><td rowspan=1 colspan=1>0x0F</td><td rowspan=1 colspan=1>0x0E</td><td rowspan=1 colspan=1>0x0D</td><td rowspan=1 colspan=1>0x0C</td><td rowspan=1 colspan=1>0x0B</td><td rowspan=1 colspan=1>0x0A</td><td rowspan=1 colspan=1>0x09</td><td rowspan=1 colspan=1>0x08</td></tr><tr><td rowspan=1 colspan=1>0x17</td><td rowspan=1 colspan=1>0x16</td><td rowspan=1 colspan=1>0x15</td><td rowspan=1 colspan=1>0x14</td><td rowspan=1 colspan=1>0x13</td><td rowspan=1 colspan=1>0x12</td><td rowspan=1 colspan=1>0x11</td><td rowspan=1 colspan=1>0x10</td></tr><tr><td rowspan=1 colspan=1>0x17</td><td rowspan=1 colspan=1>0x16</td><td rowspan=1 colspan=1>0x15</td><td rowspan=1 colspan=1>0x14</td><td rowspan=1 colspan=1>0x13</td><td rowspan=1 colspan=1>0x12</td><td rowspan=1 colspan=1>0x11</td><td rowspan=1 colspan=1>0x10</td></tr></table>

Figure A3.7: Aligned and unaligned transfers on a 64-bit data channel

In Figure A3.8 there is an example of an aligned 32-bit wrapping transaction on a 64-bit data channel. Each row in the figure represents a transfer and the shaded cells indicate bytes that are not transferred.

Address: 0x04   
Transfer size: 32-bits   
Burst type: wrapping   
Burst length: 4 transfers

<table><tr><td rowspan=1 colspan=2>63   5655</td><td rowspan=1 colspan=1>5548</td><td rowspan=1 colspan=1>47   403</td><td rowspan=1 colspan=1>9   323</td><td rowspan=1 colspan=1>1   242</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>1615    87     0</td></tr><tr><td rowspan=1 colspan=1>0x07</td><td rowspan=1 colspan=1>0x06</td><td rowspan=1 colspan=1>0x05</td><td rowspan=1 colspan=1>0x04</td><td rowspan=1 colspan=1>0x03</td><td rowspan=1 colspan=1>0x02</td><td></td><td rowspan=1 colspan=1>0x00</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0x0F</td><td rowspan=1 colspan=1>0x0E</td><td rowspan=1 colspan=1>0x0D</td><td rowspan=1 colspan=1>0x0C</td><td rowspan=1 colspan=1>0x0B</td><td rowspan=1 colspan=1>0x0A</td><td></td><td rowspan=1 colspan=1>0x08</td></tr><tr><td rowspan=1 colspan=1>0x0F</td><td rowspan=1 colspan=1>0x0E</td><td rowspan=1 colspan=1>0x0D</td><td rowspan=1 colspan=1>0x0C</td><td rowspan=1 colspan=1>0x0B</td><td rowspan=1 colspan=1>0x0A</td><td></td><td rowspan=1 colspan=1>0x08</td></tr><tr><td rowspan=1 colspan=1>0x07</td><td rowspan=1 colspan=1>0x06</td><td rowspan=1 colspan=1>0x05</td><td rowspan=1 colspan=1>0x04</td><td rowspan=1 colspan=1>0x03</td><td rowspan=1 colspan=1>0x02</td><td></td><td rowspan=1 colspan=1>0x00</td></tr><tr><td rowspan=1 colspan=8></td></tr></table>

Figure A3.8: Aligned wrapping transfers on a 64-bit channel

## A3.3 Transaction response

Every AXI transaction includes one or more response transfers sent by the Subordinate to indicate the result of the transaction.

Transactions on the write channels have one or more write responses.

Transactions on the read channels have one or more read responses.

Atomic transactions have write and read responses, see A6.4 Atomic transactions.

## A3.3.1 Write response

Write responses are transported using the BRESP signal on the write response channel. All transactions on the write channels have one Completion response which indicates the result of the transaction. Some transactions also have a second write response, for example to indicate Persistence, see A9.8.4 PCMO response on the B channel.

The BRESP and BCOMP signals are used to send write responses.

Table A3.26: BRESP and BCOMP signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>BRESP</td><td>BRESP_WIDTH</td><td>0b000 (OKAY)</td><td>Indicates the result of a transaction that uses the write channels.</td></tr><tr><td>BCOMP</td><td>1</td><td>0b1</td><td>Asserted HIGH to indicate a Completion response.</td></tr></table>

The BRESP\_WIDTH property is defined in Table A3.27.

Table A3.27: BRESP\_WIDTH property
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>BRESP_WIDTH</td><td>0,2,3</td><td>2</td><td>Width of BRESP in bits.</td></tr><tr><td></td><td></td><td></td><td>Must be 3 if:</td></tr><tr><td></td><td></td><td></td><td>Untranslated_Transactions = v2 OR</td></tr><tr><td></td><td></td><td></td><td>Untranslated_Transactions = v3 OR</td></tr><tr><td></td><td></td><td></td><td>WriteDeferrable_Transaction = True</td></tr></table>

BRESP is an optional signal. If the BRESP\_WIDTH property is 0, it is not present and assumed to be 0b000 (OKAY).

BCOMP is only present if an interface is using a feature that can have two write responses, these are:

• Cache maintenance for Persistence, see A9.8 CMOsfor Persistence.

• Memory Tagging, see A12.2 Memory Tagging Extension (MTE).

If BCOMP is present, it must be asserted for one response transfer of every transaction on the write channels.   
The BRESP encodings are shown in Table A3.28.

Table A3.28: BRESP encodings
<table><tr><td>BRESP</td><td>Label</td><td>Meaning</td></tr><tr><td>0b000</td><td>OKAY</td><td>Non-exclusive write: The transaction was successful. If the transaction includes write data, the updated value is observable. Exclusive write: Failed to update the location.</td></tr><tr><td>0b001</td><td>EXOKAY</td><td>Exclusive write succeeded. This response is only permitted for an exclusive write.</td></tr><tr><td>0b010</td><td>SLVERR</td><td>The request has reached an end point but has not completed successfully. The location might not be fully updated. Typically used when there is a problem within a Subordinate such as trying to access a read-only or powered-down function.</td></tr><tr><td>0b011</td><td>DECERR</td><td>The request has not reached a point where data can be written. The location might not be fully updated. Typically used when the address decodes to an invalid address.</td></tr><tr><td>0b100</td><td>DEFER</td><td>Write was unsuccessful because it cannot be serviced at this time. The location is not updated. This response is only permitted for a WriteDeferrable transaction.</td></tr><tr><td>0b101</td><td>TRANSFAULT</td><td>Write was terminated because of a translation fault which might be resolved by a PRI request. Only permitted for requests using the PRI flow.</td></tr><tr><td>0b110</td><td>RESERVED</td><td></td></tr><tr><td>0b111</td><td>UNSUPPORTED</td><td>Write was unsuccessful because the transaction type is not supported by the target. The location is not updated. This response is only permitted for a WriteDeferrable transaction.</td></tr></table>

## A3.3.2 Read response

The read response indicates if the read was successful and whether the data in that transfer is valid.

Read responses are transported using the RRESP signal on the read data channel. There is a read response with every read data transfer in a transaction. The response value is not required to be the same for every read data transfer in a transaction.

It is required that all data transfers as indicated by Length are always completed irrespective of the response. For some responses, the data in that transfer is not required to be valid.

The RRESP signal is defined in Table A3.29.

Table A3.29: RRESP signal

<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>RRESP</td><td>RRESP_WIDTH</td><td>0b000</td><td>Response for transactions on the read channels.</td></tr><tr><td colspan="2"></td><td>(OKAY)</td><td>Must be valid when RVALID is asserted.</td></tr></table>

The RRESP\_WIDTH property is defined in Table A3.30.

Table A3.30: RRESP\_WIDTH property
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>RRESP_WIDTH</td><td>0,2,3</td><td>2</td><td>Width of RRESP in bits.</td></tr><tr><td></td><td></td><td></td><td>Must be 3 if Prefetch_Transaction = True OR</td></tr><tr><td></td><td></td><td></td><td>Untranslated_Transactions = v2 OR</td></tr><tr><td></td><td></td><td></td><td>Untranslated_Transactions = v3 OR</td></tr><tr><td></td><td></td><td></td><td>Shareable_Cache_Support = True</td></tr></table>

RRESP is an optional signal. If the RRESP\_WIDTH property is 0, it is not present and assumed to be 0b000 (OKAY).

The RRESP encodings are shown in Table A3.31.

For responses where data is not required to be valid, the Manager might still sample the RDATA value so the Subordinate should not rely on the response to hide sensitive data.

Table A3.31: RRESP encodings

<table><tr><td>RRESP</td><td>Label</td><td>Meaning</td></tr><tr><td>0b000</td><td>OKAY</td><td>Non-exclusive read: Transaction has completed successfully, read data is valid. Exclusive read: Subordinate does not support exclusive accesses.</td></tr><tr><td>0b001</td><td>EXOKAY</td><td>Exclusive read succeeded. This response is only permitted for an exclusive read.</td></tr><tr><td>0b010</td><td>SLVERR</td><td>Transaction has encountered a contained error; only this location is affected. Typically used when there is a problem within a Subordinate such as a FIFO overrun, unsupported transfer size or trying to access a powered-down function. Read data is not valid.</td></tr><tr><td>0b011</td><td>DECERR</td><td>Transaction has encountered a non-contained error; other locations may be affected. Typically used when the address decodes to an invalid address. Read data is not valid.</td></tr><tr><td>0b100</td><td>PREFETCHED</td><td>Read data is valid and has been sourced from a prefetched value.</td></tr><tr><td>0b101</td><td>TRANSFAULT</td><td>Transaction was terminated because of a translation fault which might be resolved by a PRI request. Read data is not valid. Only permitted for requests using the PRI flow.</td></tr><tr><td>0b110</td><td>OKAYDIRTY</td><td>Read data is valid and is Dirty with respect to the value in memory. Only permitted for a response to a ReadShared request.</td></tr><tr><td>0b111</td><td>RESERVED</td><td></td></tr></table>

The value of RRESP is not constrained to be the same for every transfer in a transaction. A response of DECERR is generally used when there is a problem accessing a Subordinate, and in this case DECERR is signaled consistently in every transfer of read data. There may be a benefit if a Manager can inspect just one read data transfer to determine whether a DECERR has occurred.

The Consistent\_DECERR property is used to define whether a Subordinate signals DECERR consistently within a transaction as shown in Table A3.32.

Table A3.32: Consistent\_DECERR property
<table><tr><td>Consistent_DECERR Default Description</td><td></td></tr><tr><td>True</td><td>DECERR is signaled for every read data transfer, or no read data transfers in each cache line of data. For example, a transaction which crosses a cache line boundary can receive a DECERR response for every read data transfer on one cache</td></tr><tr><td></td><td>line and no data transfers on the next cache line.</td></tr><tr><td>False Y</td><td>DECERR may be signaled on any number of read data transfers.</td></tr></table>

A Subordinate interface that does not use the DECERR response can set the Consistent\_DECERR property to True.

A Manager with Consistent\_DECERR set True can inspect a single data transfer to determine whether a DECERR has occurred.

Setting this property to True can be helpful when bridging between AXI and CHI where DECERR translates to a Non-data Error.

When connecting Manager and Subordinate interfaces, Table A3.33 indicates combinations of Consistent\_DECERR that are compatible.

Table A3.33: Consistent\_DECERR interoperability
<table><tr><td></td><td>Subordinate: False</td><td>Subordinate: True</td></tr><tr><td>Manager: False</td><td>Compatible.</td><td>Compatible.</td></tr><tr><td>Manager: True</td><td>Not compatible. A DECERR response might be</td><td>Compatible.</td></tr></table>

## A3.3.3 Subordinate Busy indicator

When providing a response, a Subordinate can indicate its current level of activity using the Busy indicator. This information can be used to control the issue rate of a Manager or how many speculative transactions it produces.

The Busy indication is useful for components with a shared resource, such as a memory controller or system cache. For example, the Busy indication can indicate:

• The level of a shared queue.

• The level of a read or write request queue, depending on the direction of the transaction.

• When the resource usage by a component is more or less than its allocated value.

The Busy\_Support property as shown in Table A3.34 is used to define whether an interface includes the Busy indicator signals.

Table A3.34: Busy\_Support property
<table><tr><td>Busy_Support Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>Subordinate busy is supported.</td></tr><tr><td>False</td><td>Y</td><td>Subordinate busy is not supported.</td></tr></table>

When Busy\_Support is True, the following signals are included on an interface.

Table A3.35: Busy indicator signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>BBUSY,</td><td>2</td><td>0b00</td><td>Indicates the current level of Subordinate activity</td></tr><tr><td>RBUSY</td><td></td><td></td><td>in a transaction response. The value increases as</td></tr><tr><td></td><td></td><td></td><td>the Subordinate becomes busier.</td></tr></table>

For transactions with multiple read data transfers, Busy must be valid but can take a different value for every transfer.

For transactions with multiple write responses, Busy must be valid in the response with BCOMP asserted. For other write responses, Busy is not applicable and can take any value.

For Atomic transactions with write and read responses, BBUSY and RBUSY are expected, but not required to have the same value.

The exact usage of Busy indicator values is IMPLEMENTATION DEFINED, in Table A3.36 there is an example of how it can be used. In this example, a default value of 0b01 would be appropriate if a Subordinate was not able to generate a dynamic busy indicator.

Table A3.36: Example usage of the Busy indicator
<table><tr><td>Busy indicator value Meaning</td><td></td><td>Manager behavior</td></tr><tr><td>0b00</td><td>Not busy</td><td>Increase speculative requests.</td></tr><tr><td>0b01</td><td>Optimally busy</td><td>No change.</td></tr><tr><td>0b10</td><td>Quite busy</td><td>Decrease speculative requests.</td></tr><tr><td>0b11</td><td>Very busy</td><td>Heavily decrease speculative requests.</td></tr></table>

When connecting Manager and Subordinate interfaces, Table A3.37 indicates combinations of Busy\_Support that are compatible.

Table A3.37: Busy\_Support interoperability
<table><tr><td></td><td>Subordinate: False</td><td>Subordinate: True</td></tr><tr><td>Manager: False</td><td>Compatible.</td><td>Compatible, BUSY outputs are left unconnected.</td></tr><tr><td>Manager: True</td><td>Compatible, BUSY inputs are tied to the default value.</td><td>Compatible.</td></tr></table>

## Chapter A4 Request attributes

This chapter describes request attributes that indicate how the request should be handled by downstream components. It contains the following sections:

• A4.1 Subordinate types

• A4.2 Memory attributes

• A4.3 Memory types

• A4.4 Protocol errors

• A4.5 Protection attributes

• A4.6 Memory Encryption Contexts

• A4.7 Multiple region interfaces

• A4.8 QoS signaling

## A4.1 Subordinate types

Subordinates are classified as either a Memory Subordinate or a Peripheral Subordinate.

## Memory Subordinate

A Memory Subordinate is required to handle all transaction types correctly.

## Peripheral Subordinate

A Peripheral Subordinate has an IMPLEMENTATION DEFINED method of access. Typically, the method of access is defined in the component data sheet that describes the transaction types that the Subordinate handles correctly.

Any access to the Peripheral Subordinate that is not part of the IMPLEMENTATION DEFINED method of access must complete, in compliance with the protocol. However, when such an access has been made, there is no requirement that the Peripheral Subordinate continues to operate correctly. The Subordinate is only required to continue to complete further transactions in a protocol compliant manner.

## A4.2 Memory attributes

This section describes the attributes that determine how a request should be treated by system components such as caches, buffers, and memory controllers.

The AWCACHE and ARCACHE signals specify the memory attributes of a request. They control:

• How a transaction progresses through the system.

• How any system-level buffers and caches handle the transaction.

In this specification, the term AxCACHE refers collectively to the AWCACHE and ARCACHE signals. Table A4.1 describes the AWCACHE and ARCACHE signals.

Table A4.1: AxCACHE signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWCACHE, ARCACHE</td><td>4</td><td>0x0</td><td>The memory attributes of a request control how a transaction progresses through the system and how caches and buffers handle the request.</td></tr></table>

The CACHE\_Present property is used to determine if the AxCACHE signals are present on an interface.

Table A4.2: CACHE\_Present property
<table><tr><td>CACHE_Present Default Description</td><td></td><td></td></tr><tr><td>True</td><td>Y</td><td>AWCACHE and ARCACHE are present.</td></tr><tr><td>False</td><td></td><td>AWCACHE and ARCACHE are not present.</td></tr></table>

AWCACHE bits are encoded as:

• [0] Bufferable

• [1] Modifiable

• [2] Other Allocate

• [3] Allocate

ARCACHE bits are encoded as:

• [0] Bufferable

• [1] Modifiable

• [2] Allocate

• [3] Other Allocate

Note that the Allocate and Other Allocate bits are in different positions for read and write requests.

## A4.2.1 Bufferable, AxCACHE[0]

For write transactions:

• If the Bufferable bit is deasserted and AWCACHE[3:2] are both deasserted, the write response indicates that the data has reached its final destination.

• If the Bufferable bit is asserted, the write response can be sent from an intermediate point, when the observability requirements have been met.

For read transactions where ARCACHE[3:2] are deasserted (Non-cacheable) and ARCACHE[1] is asserted (Modifiable):

• If the Bufferable bit is deasserted, the read data must be obtained from the final destination.

• If the Bufferable bit is asserted, the read data can be obtained from the final destination or from a write that is progressing to the final destination.

For other combinations of ARCACHE[3:1], the Bufferable bit has no effect.

## A4.2.2 Modifiable, AxCACHE[1]

When AxCACHE[1] is asserted, the transaction is Modifiable which indicates that the characteristics of the transaction can be modified. When AxCACHE[1] is deasserted, the transaction is Non-modifiable.

The following sections describe the properties of Non-modifiable and Modifiable transactions.

## Non-modifiable transactions

A Non-modifiable transaction must not be split into multiple transactions or merged with other transactions.

In a Non-modifiable transaction, the parameters that are shown in Table A4.3 must not be changed.

Table A4.3: Parameters fixed as Non-modifiable
<table><tr><td>Parameter</td><td>Signals</td></tr><tr><td>Address</td><td>AxADDR, and therefore AxREGION</td></tr><tr><td>Size</td><td>AxSIZE</td></tr><tr><td>Length</td><td>AxLEN</td></tr><tr><td>Burst type</td><td>AxBURST</td></tr><tr><td>Protection attributes</td><td>AxPROT, AxNSE, AxPAS, AxINST, AxPRIV</td></tr></table>

The AxCACHE attribute can only be modified to convert a transaction from being Bufferable to Non-bufferable.   
No other change to AxCACHE is permitted.

The transaction ID and the QoS values can be modified.

A Non-modifiable transaction with Length greater than 16 can be split into multiple transactions. Each resulting transaction must meet the requirements that are given in this subsection, except that:

• The Length is reduced.

• The address of the generated transactions is adapted appropriately.

A Non-modifiable transaction that is an exclusive access, as indicated by AxLOCK asserted, is permitted to have the Size, AxSIZE, and Length, AxLEN, modified if the total number of bytes accessed remains the same.

There are circumstances where it is not possible to meet the requirements of Non-modifiable transactions. For example, when downsizing to a data width narrower than required by Size, the transaction must be modified.

A component that performs such an operation can optionally include an IMPLEMENTATION DEFINED mechanism to indicate that a modification has occurred. This mechanism can assist with software debug.

## Modifiable transactions

A Modifiable transaction can be modified in the following ways:

• A transaction can be broken into multiple transactions.

• Multiple transactions can be merged into a single transaction.

• A read transaction can fetch more data than required.

• A write transaction can access a larger address range than required using the WSTRB signals to ensure that only the appropriate locations are updated.

• In each generated transaction, the following attributes can be modified:

– Address, AxADDR

– Size, AxSIZE

– Length, AxLEN

– Burst type, AxBURST

The following must not be changed:

• Exclusive access indicator: AxLOCK

• The access and address space attributes: AxPROT, AxINST, AxPRIV, AxNSE, AxPAS, AxMMUPASUNKNOWN.

AxCACHE can be modified, but any modification must ensure that the visibility of transactions by other components is not reduced, either by preventing propagation of transactions to the required point, or by changing the need to look up a transaction in a cache. Any modification to the memory attributes must be consistent for all transactions to the same address range.

The transaction ID and QoS values can be modified.

No transaction modification is permitted that:

• Causes accesses to a different 4KB address space than that of the original transaction.

• Causes a single access to a single-copy atomicity sized region to be performed as multiple accesses. See A6.1 Single-copy atomicity size.

## A4.2.3 Allocate and Other Allocate, AxCACHE[2], and AxCACHE[3]

If the Allocate bit is asserted:

• The data might have been previously allocated, so the line must be looked up in a cache.

• It is recommended that the data is allocated into a cache for future use.

If the Other Allocate bit is asserted:

• The data might have been previously allocated, so the line must be looked up in a cache.

• It is not recommended that the data is allocated as it is not expected to be accessed again.

If Allocate and Other Allocate are both deasserted, the request is not required to look up in any cache.

## A4.3 Memory types

The combination of AxCACHE signals indicates a memory type. Table A4.4 shows the memory type encodings.   
Values in brackets are permitted but not preferred. Values that are not shown in the table are reserved.

Table A4.4: Memory type encoding
<table><tr><td>ARCACHE[3:0]</td><td>AWCACHE[3:0]</td><td>Memory type</td></tr><tr><td>0b0000</td><td>0b0000</td><td>Device Non-bufferable</td></tr><tr><td>0b0001</td><td>0b0001</td><td>Device Bufferable</td></tr><tr><td>0b0010</td><td>0b0010</td><td>Normal Non-cacheable Non-bufferable</td></tr><tr><td>0b0011</td><td>0b0011</td><td>Normal Non-cacheable Bufferable</td></tr><tr><td>0b1010</td><td>0b0110</td><td>Write-Through No-Allocate</td></tr><tr><td>0b1110 (0b0110)</td><td>0b0110</td><td>Write-Through Read-Allocate</td></tr><tr><td>0b1010</td><td>0b1110 (0b1010)</td><td>Write-Through Write-Allocate</td></tr><tr><td>0b1110</td><td>0b1110</td><td>Write-Through Read and Write-Allocate</td></tr><tr><td>0b1011</td><td>0b0111</td><td>Write-Back No-Allocate</td></tr><tr><td>0b1111 (0b0111)</td><td>0b0111</td><td>Write-Back Read-Allocate</td></tr><tr><td>0b1011</td><td>0b1111 (0b1011)</td><td>Write-Back Write-Allocate</td></tr><tr><td>0b1111</td><td>0b1111</td><td>Write-Back Read and Write-Allocate</td></tr></table>

## A4.3.1 Memory type requirements

This section specifies the required behavior for each of the memory types.

## Device Non-bufferable

The required behavior for Device Non-bufferable memory is:

• The write response must be obtained from the final destination.

• Read data must be obtained from the final destination.

• Transactions are Non-modifiable, see A4.2.2 Non-modifiable transactions.

• Read data must not be prefetched.

• Write transactions must not be merged.

## Device Bufferable

The required behavior for the Device Bufferable memory type is:

• The write response can be obtained from an intermediate point.

• Write transactions must be made visible at the final destination in a timely manner.

• Read data must be obtained from the final destination.

• Transactions are Non-modifiable, see A4.2.2 Non-modifiable transactions.

• Read data must not be prefetched.

• Write transactions must not be merged.

Both Device memory types are Non-modifiable. In this specification, the terms Device memory and Non-modifiable memory are interchangeable.

For read transactions, there is no difference in the required behavior for Device Non-bufferable and Device Bufferable memory types.

## Normal Non-cacheable Non-bufferable

The required behavior for the Normal Non-cacheable Non-bufferable memory type is:

• The write response must be obtained from the final destination.

• Read data must be obtained from the final destination.

• Transactions are Modifiable, see A4.2.2 Modifiable transactions.

• Write transactions can be merged.

## Normal Non-cacheable Bufferable

The required behavior for the Normal Non-cacheable Bufferable memory type is:

• The write response can be obtained from an intermediate point.

• Write transactions must be made visible at the final destination in a timely manner, as defined in the glossary. There is no mechanism to determine when a write transaction is visible at its final destination.

• Read data must be obtained from either:

– The final destination.

– A write transaction that is progressing to its final destination.

• If read data is obtained from a write transaction:

– It must be obtained from the most recent version of the write.

– The data must not be cached to service a later read.

• Transactions are Modifiable, see A4.2.2 Modifiable transactions.

• Write transactions can be merged.

For a Normal Non-cacheable Bufferable read, data can be obtained from a write transaction that is still progressing to its final destination. This data is indistinguishable from the read and write transactions propagating to arrive at the final destination at the same time. Read data that is returned in this manner does not indicate that the write transaction is visible at the final destination.

## Write-Through No-Allocate

The required behavior for the Write-Through No-Allocate memory type is:

• The write response can be obtained from an intermediate point.

• Write transactions must be made visible at the final destination in a timely manner, as defined in the glossary. There is no mechanism to determine when a write transaction is visible at the final destination.

• Read data can be obtained from an intermediately cached copy.

• Transactions are Modifiable, see A4.2.2 Modifiable transactions.

• Read data can be prefetched.

• Write transactions can be merged.

• A cache lookup is required for read and write transactions.

• The No-Allocate attribute is an allocation hint, that is, it is a recommendation to the memory system that for performance reasons, these transactions are not allocated. However, the allocation of read and write transactions is not prohibited.

## Write-Through Read-Allocate

The required behavior for the Write-Through Read-Allocate memory type is the same as for Write-Through No-Allocate memory. For performance reasons:

• Allocation of read transactions is recommended.

• Allocation of write transactions is not recommended.

## Write-Through Write-Allocate

The required behavior for the Write-Through Write-Allocate memory type is the same as for Write-Through No-Allocate memory. For performance reasons:

• Allocation of read transactions is not recommended.

• Allocation of write transactions is recommended.

## Write-Through Read and Write-Allocate

The required behavior for the Write-Through Read and Write-Allocate memory type is the same as for Write-Through No-Allocate memory. For performance reasons:

• Allocation of read transactions is recommended.

• Allocation of write transactions is recommended.

## Write-Back No-Allocate

The required behavior for the Write-Back No-Allocate memory type is:

• The write response can be obtained from an intermediate point.

• Write transactions are not required to be made visible at the final destination.

• Read data can be obtained from an intermediately cached copy.

• Transactions are Modifiable, see A4.2.2 Modifiable transactions.

• Read data can be prefetched.

• Write transactions can be merged.

• A cache lookup is required for read and write transactions.

• The No-Allocate attribute is an allocation hint, that is, it is a recommendation to the memory system that for performance reasons, these transactions are not allocated. However, the allocation of read and write transactions is not prohibited.

## Write-Back Read-Allocate

The required behavior for the Write-Back Read-Allocate memory type is the same as for Write-Back No-Allocate memory. For performance reasons:

• Allocation of read transactions is recommended.

• Allocation of write transactions is not recommended.

## Write-Back Write-Allocate

The required behavior for the Write-Back Write-Allocate memory type is the same as for Write-Back No-Allocate memory. For performance reasons:

• Allocation of read transactions is not recommended.

• Allocation of write transactions is recommended.

## Write-Back Read and Write-Allocate

The required behavior for the Write-Back Read and Write-Allocate memory type is the same as for Write-Back No-Allocate memory. For performance reasons:

• Allocation of read transactions is recommended.

• Allocation of write transactions is recommended.

## A4.3.2 Mismatched memory attributes

Multiple agents that are accessing the same area of memory, can use mismatched memory attributes. However, for functional correctness, the following rules must be obeyed:

• All Managers accessing the same area of memory must have a consistent view of the cacheability of that area of memory at any level of hierarchy. The rules to be applied are:

– If the address region is Non-cacheable, all Managers must use transactions with both AxCACHE[3:2] deasserted.

– If the address region is Cacheable, all Managers must use transactions with either of AxCACHE[3:2] asserted.

• Different Managers can use different allocation hints.

• If an addressed region is Normal Non-cacheable, any Manager can access it using a Device memory transaction.

• If an addressed region has the Bufferable attribute, any Manager can access it using transactions that do not permit Bufferable behavior. For example, a transaction that requires the response from the final destination does not permit Bufferable behavior.

## A4.3.3 Changing memory attributes

The attributes for a particular memory region can be changed from one type to another incompatible type. For example, the attribute can be changed from Write-Through Cacheable to Normal Non-cacheable. This change requires a suitable process to perform the change.

Typically, the following process is performed:

1. All Managers stop accessing the region.

2. A single Manager performs any required cache maintenance operations.

3. All Managers restart accessing the memory region, using the new attributes.

## A4.3.4 Transaction buffering

Write access to the following memory types do not require a transaction response from the final destination, but do require that write transactions are made visible at the final destination in a timely manner:

• Device Bufferable

• Normal Non-cacheable Bufferable

• Write-Through

For write transactions, all three memory types require the same behavior.

For read transactions, the required behavior is as follows:

• For Device Bufferable memory, read data must be obtained from the final destination.

• For Normal Non-cacheable Bufferable memory, read data must be obtained either from the final destination or from a write transaction that is progressing to its final destination.

• For Write-Through memory, read data can be obtained from an intermediately cached copy.

In addition to ensuring that write transactions progress towards their final destination in a timely manner, intermediate buffers must behave as follows:

• An intermediate buffer that can respond to a transaction must ensure that over time, any read transaction to Normal Non-cacheable Bufferable propagates towards its destination. This propagation means that when forwarding a read transaction, the attempted forwarding must not continue indefinitely, and any data that is used for forwarding must not persist indefinitely. The protocol does not define a mechanism to determine the duration for which data used in forwarding a read transaction, can be retained. However, in such a mechanism, the act of reading the data must not reset the data timeout period.

Without this requirement, continued polling of the same location can prevent the timeout of a read that is held in the buffer, preventing the read progressing towards its destination.

• An intermediate buffer that can hold and merge write transactions must ensure that transactions do not remain in its buffer indefinitely. For example, merging write transactions must not reset the mechanism that determines when a write is drained towards its final destination.

Without this requirement, continued writes to the same location can prevent the timeout of a write held in the buffer, preventing the write progressing towards its destination.

For information about the required behavior of read accesses to these memory types, see:

• A4.3.1 Device Bufferable

• A4.3.1 Normal Non-cacheable Bufferable

• A4.3.1 Write-Through No-Allocate

## A4.3.5 Example use of Device memory types

The specification supports the combined use of Device Non-bufferable and Device Bufferable memory types to force write transactions to reach their final destination and ensure that the issuing Manager knows when the transaction is visible to all other Managers.

A write transaction that is marked as Device Bufferable is required to reach its final destination in a timely manner. However, the write response for the transaction can be signaled by an intermediate buffer. Therefore, the issuing Manager cannot know when the write is visible to all other Managers.

If a Manager issues a Device Bufferable write transaction, or stream of write transactions, followed by a Device Non-bufferable write transaction, and all transactions use the same AXI ID, then the AXI ordering requirements force all of the Device Bufferable write transactions to reach the final destination before a response is given to the Device Non-bufferable transaction. Therefore, the response to the Device Non-bufferable transaction indicates that all the transactions are visible to all Managers.

A Device Non-bufferable transaction can only guarantee the completion of Device Bufferable transactions that are issued with the same ID, and are to the same Subordinate device.

## A4.4 Protocol errors

The AXI protocol defines two categories of protocol errors, a software protocol error and a hardware protocol error.

## A4.4.1 Software protocol error

A software protocol error occurs when multiple accesses to the same location are made with mismatched shareability or cacheability attributes. A software protocol error can cause a loss of coherency and result in the corruption of data values. The protocol requires that the system does not deadlock for a software protocol error, and that transactions always progress through a system.

A software protocol error for an access in one 4KB memory region must not cause data corruption in a different 4KB memory region. For locations held in Normal memory, the use of appropriate software barriers and cache maintenance can be used to return memory locations to a defined state.

When accessing a peripheral device, if Modifiable transactions are used (AxCACHE[1] is asserted), then the correct operation of the peripheral cannot be guaranteed. The only requirement is that the peripheral continues to respond to transactions in a protocol compliant manner. To restore a peripheral device that has been accessed incorrectly, to a known operational state, involves a sequence of events that are IMPLEMENTATION DEFINED.

## A4.4.2 Hardware protocol error

A hardware protocol error is defined as any protocol error that is not a software protocol error. No support is required for hardware protocol errors.

If a hardware protocol error occurs, then recovery from the error is not guaranteed. The system might crash, lock up, or suffer some other non-recoverable failure.

## A4.5 Protection attributes

AXI requests can have attributes that can be used to protect memory from unexpected accesses. These attributes are physical address space (PAS), Privileged, and Instruction.

## A4.5.1 Signaling for protection attributes

Table A4.5 shows the signals that can be used to indicate protection attributes.

Table A4.5: Protection signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Presence</td><td>Description</td></tr><tr><td>AWPROT, ARPROT</td><td>3</td><td>0b000</td><td>PROT_Present</td><td>The protection attributes for a request.</td></tr><tr><td>AWNSE, ARNSE</td><td>1</td><td>0b0</td><td>RME_Support == True and PROT_Present == True</td><td>Extends AxPROT[1] to include Root and Realm address spaces.</td></tr><tr><td>AWPRIV, ARPRIV</td><td>1</td><td>0b0</td><td>INSTPRIV_Present</td><td>LOW to indicate this is an unprivileged access, HIGH for a privileged access. Equivalent to AxPROT[0].</td></tr><tr><td>AWINST, ARINST</td><td>1</td><td>0b0</td><td>INSTPRIV_Present</td><td>LOW to indicate this is a data access, HIGH for an instruction access. Equivalent to AxPROT[2].</td></tr><tr><td>AWPAS, ARPAS</td><td>PAS WIDTH</td><td>All zeros (Secure)</td><td>PAS_WIDTH &gt; 0</td><td>Physical address space (PAS) of a transaction.</td></tr></table>

Table A4.6 shows the properties used to define the protection signaling.

Table A4.6: Protection properties
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>PROT_Present</td><td>True, False</td><td>True</td><td>Indicates if AxPROT signals are present on an interface. True AWPROT and ARPROT are present. False</td></tr><tr><td>INSTPRIV_Present</td><td>True, False</td><td>False</td><td>AWPROT and ARPROT are not present. Indicates if AxINST and AxPRIV signals are present on an interface. True AWPRIV, ARPRIV, AWINST and ARINST are present. False</td></tr><tr><td></td><td>0..3</td><td>0</td><td>Width of the AWPAS and ARPAS signals in bits.</td></tr><tr><td></td><td></td><td></td><td>AWPRIV, ARPRIV, AWINST and ARINST are not</td></tr><tr><td>PAS_WIDTH</td><td></td><td></td><td>present.</td></tr></table>

AxPROT and AxNSE signals have been superseded by AxPRIV, AxINST and AxPAS for signaling protection attributes. An interface must not include both sets of signals, the following rules apply:

• If PROT\_Present is True, PAS\_WIDTH must be 0.

• If PROT\_Present is True, INSTPRIV\_Present must be False.

## A4.5.2 Privileged and Instruction attributes

An AXI Manager might support more than one level of operating privilege, and can optionally extend this concept of privilege to memory access. Some processors support multiple levels of privilege, see the documentation for the selected processor to determine the mapping to AXI privilege levels. The only distinction AXI can provide is between privileged and unprivileged access.

Access privilege can be signaled using either AxPROT[0] or AxPRIV:

• 0b0: Unprivileged

• 0b1: Privileged

An access can be labeled as an instruction access or a data access, using either AxPROT[2] or AxINST:

• 0b0: Data access

• 0b1: Instruction access

The AXI protocol defines this indication as a hint. It is not accurate in all cases, for example, where a transaction contains a mix of instruction and data items. It is recommended that a Manager indicates a data access unless the access is known to be an instruction access.

## A4.5.3 Physical address space (PAS)

An AXI request can include a physical address space identifier. Requests with the same address but to different physical address spaces can decode to different memory locations. Some memory locations might have access restrictions based on the PAS.

Table A4.7 shows the physical address spaces with signal encodings and property that must be True to enable a Manager to use that encoding. An interface can include AxPAS or AxPROT/AxNSE signals, not both.

Table A4.7: Physical address space encodings
<table><tr><td>Physical address space</td><td>AxPAS</td><td>AxPROT[1]</td><td>AxNSE</td><td>Property</td></tr><tr><td>Secure</td><td>0b000</td><td>0b0</td><td>0b0</td><td>-</td></tr><tr><td>Non-secure (NS)</td><td>0b001</td><td>0b1</td><td>0b0</td><td>-</td></tr><tr><td>Root</td><td>0b010</td><td>0b0</td><td>0b1</td><td>RME_Support</td></tr><tr><td>Realm</td><td>0b011</td><td>0b1</td><td>0b1</td><td>RME_Support</td></tr><tr><td>System Agent (SA)</td><td>0b100</td><td>-</td><td></td><td>GDI_Support</td></tr><tr><td>Non-secure Protected (NSP)</td><td>0b101</td><td>-</td><td>一</td><td>GDI_Support</td></tr></table>

Other values of AxPAS are reserved.

## A4.5.4 Realm Management Extension

Memory protection can be extended using the Realm Management Extension (RME) [3]. This provides hardware-based isolation that allows execution contexts to run in different Security states and share resources in the system.

When RME is used, it adds the Root and Realm physical address spaces, affects the operation of cache maintenance operations and extends the MPAM signals.

RME support is defined using the RME\_Support property.

Table A4.8: RME\_Support property
<table><tr><td></td><td>RME_Support Default Description</td><td></td></tr><tr><td>True</td><td></td><td>RME is supported.</td></tr><tr><td>False</td><td>Y</td><td>RME is not supported.</td></tr></table>

## A4.5.5 Granular Data Isolation

Granular Data Isolation (GDI) is an extension to the Arm Realm Management Extension (RME).

The GDI feature is designed to enable memory isolation between data flows from Processing Elements (PEs) and non-Processing Elements, within an RME system. To achieve this, two physical address spaces (PAS) are defined for specific use cases:

• Non-secure Protected (NSP)

– Intended for media pipelines, with flexible Non-secure software management and strong data confidentiality.

– Memory is managed by a Processing Element (PE), using the SMMU, on behalf of a Non-secure device in protected mode.

• System Agent (SA)

– Intended for use by higher security on chip sub-systems that require memory allocation on request.

– Fully isolated from PEs, and any additional memory management is independent from the PEs.

– Requests to the System Agent PAS are physically addressed but might require access checks.

PEs are not permitted to directly access either of these new PAS, except for performing Cache Maintenance through to the Point ofPhysical Aliasing (PoPA).

Both new physical address spaces are permitted to make use of the RME Memory Encryption Contexts (MEC) feature, see A4.6 Memory Encryption Contexts.

For more information on the GDI architecture, see [3].

See Table A4.7 for the NSP and SA physical address space encodings.

The property GDI\_Support determines whether an interface supports Granular Data Isolation.

Table A4.9: GDI\_Support property
<table><tr><td>GDI_Support Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>GDI is supported. NSP and SA address spaces can be used.</td></tr><tr><td>False</td><td>Y</td><td>GDI is not supported.</td></tr></table>

The following rules apply to the GDI\_Support property:

• When RME\_Support is False, GDI\_Support must be False.

• When GDI\_Support is True, PAS\_WIDTH must be 3.

• When GDI\_Support is True, Untranslated\_Transactions must be False or v4.

## A4.6 Memory Encryption Contexts

Memory Encryption Contexts (MEC) is an extension to the Arm Realm Management Extension (RME) that allows each Realm to have its own unique encryption context. The MEC extension assigns memory encryption contexts to all memory accesses within the Realm physical address space. All memory transactions are associated with a MECID, which is determined by the Security state, translation regime, translation tables and the MEC system registers. The MECID is used by a memory encryption engine as an index into a table of encryption contexts, either keys or tweaks, that contribute to the external memory encryption.

Use of MEC can help protect Realm data in memory, by enabling each set of Realm data to be encrypted in a different way. This means that a malicious agent that has access to the physical memory device and is able to decipher one set of Realm data, cannot use the same decryption method to access other sets of Realm data. Before the Point ofEncryption (PoE) the data that moves between components is in plaintext form.

Realm management software at R-EL2 controls MECID policy and assignment to Realms.

For more information on MEC, see [3] and [4].

Note that the MEC architecture specification [3] details several implementation options for when a MECID value mismatch occurs. This MEC implementation assumes that Managers and caches do not perform any MECID checks. For example, if a read access associated with a MECID targets a location that has a copy present in a cache and is associated with a different MECID, the read access succeeds as though the MECID values did not mismatch. Additional protection is not needed here as Realm management software at R-EL2 ensures that one context can be prevented from accessing locations that belong to a different context, thus ensuring plaintext leakages do not occur.

## A4.6.1 MEC signaling

The MEC\_Support property determines whether an interface supports Memory Encryption Contexts.

Table A4.10: MEC\_Support property
<table><tr><td>MEC_Support Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>MEC is supported, AxMECID signals are present.</td></tr><tr><td>False</td><td>Y</td><td>MEC is not supported, AxMECID signals are not present.</td></tr></table>

MEC is an extension of RME, so if the RME\_Support property is False, MEC\_Support must be False.   
The following signals are required to support MEC.

Table A4.11: MECID signals

<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWMECID, ARMECID</td><td>MECID_WIDTH All zeros</td><td></td><td>RME Memory Encryption Context identifier (MECID).</td></tr></table>

The parameter MECID\_WIDTH defines the width of the AxMECID signals.

Table A4.12: MECID\_WIDTH property
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>MECID_WIDTH</td><td>0,16</td><td>0</td><td>Width of AWMECID and ARMECID in bits.</td></tr></table>

The following rules apply to the MECID\_WIDTH property:

• If MECID\_WIDTH is 0, AWMECID and ARMECID are not present on the interface.

• If MEC\_Support is False, MECID\_WIDTH must be 0.

• If MEC\_Support is True, MECID\_WIDTH must not be 0.

Note that the width of MECID does not indicate how many different values are used by a component. It might be possible to reduce the storage requirements of MECID by using a narrower internal width.

The compatibility between Manager and Subordinate interfaces according to the values of the MEC\_Support property is shown in Table A4.13.

Table A4.13: MEC\_Support compatibility
<table><tr><td>MEC_Support</td><td>Subordinate: False</td><td>Subordinate: True</td></tr><tr><td>Manager: False</td><td>Compatible.</td><td>Compatible. AxMECID inputs are tied LOW.</td></tr><tr><td>Manager: True</td><td>Compatible. Downstream memory is not encrypted using MEC.</td><td>Compatible.</td></tr></table>

## A4.6.2 MECID usage

The MECID value range is bounded, dependent on the physical address space being accessed.

Table A4.14: MECID constraints
<table><tr><td>Physical address space</td><td>MECID constraints</td></tr><tr><td>Secure</td><td>Must be zero</td></tr><tr><td>Non-secure</td><td>Must be zero</td></tr><tr><td>Root</td><td>Must be zero</td></tr><tr><td>Realm</td><td>Can take any valueª</td></tr><tr><td>System Agent</td><td>Can take any valueª</td></tr><tr><td>Non-Secure Protected</td><td>Can take any valueª</td></tr></table>

<sup>a</sup> Depends on the MEC\_Support and MECID\_Width properties.

MECID is inapplicable and can take any value for the following request Opcodes:

• CMO

• CleanInvalid

## Chapter A4. Request attributes A4.6. Memory Encryption Contexts

• MakeInvalid

• CleanShared

• CleanSharedPersist

• InvalidateHint

• StashTranslation

• UnstashTranslation

MECID is inapplicable and must be 0 for the following request Opcodes:

• DVM Complete

Components that propagate transactions and support MECID on their Subordinate and Manager interfaces must preserve the MECID on requests where it is applicable. Components that perform address translation might change the MECID.

A cache that stores data which has an associated MECID must also store the MECID and provide it with the data during a write-back.

A CleanInvalidPoPA operation can be used to ensure that a cache line is cleaned and invalidated from all caches upstream of the Point of Encryption. See A9.9 Cache maintenance and Realm Management Extension for more information on CleanInvalidPoPA.

## A4.6.3 MEC and GDI

When using MEC and GDI, MECID must be valid for all accesses to Non-secure Protected or System Agent physical address spaces. MECID mismatches must not result in a loss of confidentiality of data between Memory Encryption Contexts.

A cache must enforce the following rules for the System Agent and Non-secure Protected physical address spaces when there is a difference between the incoming request MECID and the previously cached MECID value.

• For a read transaction:

– Any returned data must be masked to an IMPLEMENTATION SPECIFIC value. Arm recommends, but does not require, that this value is all ones.

– The cache is permitted to retain the line.

• For a partial write transaction:

– Cached data must be masked to an IMPLEMENTATION SPECIFIC value. Arm recommends, but does not require, that this value is all ones.

– The partial write data is then merged into this masked value.

– The cached MECID for the location must be updated to the MECID of the incoming write.

• For a full cache line write transaction:

– The write data overwrites the previously cached value.

– The cached MECID must be updated to the MECID of the incoming write.

For more information on GDI, see A4.5.5 Granular Data Isolation.

## A4.7 Multiple region interfaces

This section describes the use of a region identifier with a request, to support interfaces with multiple address regions within a single interface.

## A4.7.1 Region identifier signaling

The property REGION\_Present determines whether an interface supports region identifier signaling.

Table A4.15: REGION\_Present property
<table><tr><td>REGION_Present Default</td><td></td><td>Description</td></tr><tr><td>True</td><td>Y</td><td>AWREGION and ARREGION are present.</td></tr><tr><td>False</td><td></td><td>AWREGION and ARREGION are not present.</td></tr></table>

The signals to indicate a region are shown in Table A4.16.

Table A4.16: Region signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWREGION, ARREGION</td><td>4</td><td>0x0</td><td>A 4-bit region identifier which can be used to identify different address regions.</td></tr></table>

## A4.7.2 Using the region identifier

The 4-bit region identifier can be used to uniquely identify up to 16 different regions. The region identifier can provide a decode of higher-order address bits. The region identifier must remain constant within any 4K-byte address space.

The use of region identifiers means that a single physical interface on a Subordinate can provide multiple logical interfaces, each with a different location in the system address map. The use of the region identifier means that the Subordinate does not have to support the address decode between the different logical interfaces.

This specification expects an interconnect to produce AxREGION signals when performing the address decode function for a single Subordinate that has multiple logical interfaces. If a Subordinate only has a single physical interface in the system address map, the interconnect must use the default AxREGION values.

There are several usage models for the region identifier including, but not limited to, the following:

• A peripheral can have its main data path and control registers at different locations in the address map, and be accessed through a single interface without the need for the Subordinate to perform an address decode.

• A Subordinate can exhibit different behaviors in different memory regions. For example, a Subordinate might provide read and write access in one region, but read-only access in another region.

A Subordinate must ensure that the correct protocol signaling and the correct ordering of transactions are maintained. A Subordinate must ensure that it provides the responses to two requests to different regions with the same transaction ID in the correct order.

A Subordinate must also ensure the correct protocol signaling for any values of AxREGION. If a Subordinate implements fewer than sixteen regions, then the Subordinate must ensure the correct protocol signaling on any attempted access to an unsupported region. How this is achieved is IMPLEMENTATION DEFINED. For example, the Subordinate might ensure this by:

• Providing an error response for any transaction that accesses an unsupported region.

• Aliasing supported regions across all unsupported regions, to ensure that a protocol compliant response is given for all accesses.

The AxREGION signals only provide an address decode of the existing address space that can be used by Subordinates to remove the need for an address decode function. The signals do not create new independent address spaces. AxREGION must only be present on an interface that is downstream of an address decode function.

## A4.8 QoS signaling

AXI supports Quality of Service (QoS) schemes through the features of:

• A4.8.1 QoS identifiers

• A4.8.2 QoS acceptance indicators

## A4.8.1 QoS identifiers

An AXI request has an optional identifier which can be used to distinguish between different traffic streams as shown in Table A4.17.

Table A4.17: QoS signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWQOS,</td><td>4</td><td>0x0</td><td>Quality of Service identifier used to distinguish</td></tr><tr><td>ARQOS</td><td></td><td></td><td>between different traffic streams.</td></tr></table>

The QOS\_Present property is used to define whether an interface includes the AxQOS signals.

Table A4.18: QOS\_Present property
<table><tr><td>QOS_Present Default</td><td></td><td>Description</td></tr><tr><td>True</td><td>Y</td><td>AWQOS and ARQOS are present.</td></tr><tr><td>False</td><td></td><td>AWQOS and ARQOS are not present.</td></tr></table>

The protocol does not specify the exact use of the QoS identifier. It is recommended to use AxQOS as a priority indicator for the associated write or read request, where a higher value indicates a higher priority request.

## Using the QoS identifiers

A Manager can produce its own AxQOS values, and if it can produce multiple streams of traffic, it can choose different QoS values for the different streams.

Support for QoS requires a system-level understanding of the QoS scheme in use, and collaboration between all participating components. For this reason, it is recommended that a Manager component includes some programmability that can be used to control the exact QoS values that are used for any given scenario.

If a Manager component does not support a programmable QoS scheme, it can use QoS values that represent the relative priorities of the transactions it generates. These values can then be mapped to alternative system level QoS values if appropriate.

This specification expects that many interconnect component implementations will support programmable registers that can be used to assign QoS values to connected Managers. These values replace the QoS values, either programmed or default, supplied by the Managers.

The default system-level implementation of QoS is that any component with a choice of more than one transaction to process selects the request with the higher QoS value to process first. This selection only occurs when there is no other AXI constraint that requires the requests to be processed in a particular order. This means that the AXI ordering rules take precedence over ordering for QoS purposes.

## A4.8.2 QoS acceptance indicators

The QoS acceptance indicators as shown in Table A4.19 are output signals from a Subordinate interface that indicate the minimum QoS value it will accept without delay.

The signals are synchronous to ACLK but are unrelated to any other AXI channel.

Table A4.19: QoS acceptance signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>VAWQOSACCEPT</td><td>4</td><td>0x0</td><td>An output from a Subordinate that indicates the QoS value for which it accepts requests from the AW channel.</td></tr><tr><td>VARQOSACCEPT</td><td>4</td><td>0x0</td><td>An output from a Subordinate that indicates the</td></tr><tr><td></td><td></td><td></td><td>QoS value for which it accepts requests from the AR channel.</td></tr></table>

QoS Accept signaling is intended for Subordinate components that have different resources available for different QoS values, which is typically the case with memory controllers. The Subordinate can indicate that it only accepts requests at a certain QoS value or above when the resources available to lower QoS values are in use.

QoS Accept signaling can be used as an input to a Manager interface that might have several different requests to select from. This permits the Manager interface to only issue requests that are likely to be accepted, which avoids unnecessary blocking of the interface. By preventing the issue of requests that might be stalled for a significant period, the interface remains available for the issue of higher priority requests that might arrive at a later point in time.

In this specification, the term VAxQOSACCEPT refers collectively to the VAWQOSACCEPT and VARQOSACCEPT signals.

The rules and recommendations for the VAxQOSACCEPT signals are:

• Any requests with QoS level equal to or higher than VAxQOSACCEPT are accepted by the Subordinate.

• Any request with QoS level below VAxQOSACCEPT might be stalled for a significant time.

This specification does not define a time period during which the Subordinate is required to accept a request at, or above, the QoS level indicated. However, it is expected that for a given Subordinate there will be a deterministic maximum number of clock cycles taken to accept a transaction, after taking into account implementation aspects such as clock domain crossing ratios.

• It is permitted for a Subordinate interface to accept a request that is below the QoS level indicated by the VAxQOSACCEPT signal, but it is expected that the request might be subject to a significant delay.

While it is acceptable for a Subordinate to delay a request that has a lower priority than the QoS acceptance level, it is recommended that such a transaction is not delayed indefinitely.

There are several reasons for a lower-priority transaction to be issued on the interface, for example:

• A delay between a change in the QoS acceptance value and the ability of the component to adapt to that change.

• A requirement to make progress on a transaction that is Head-of-line blocking a higher priority request.

• A requirement to make progress on a transaction for reasons of starvation prevention.

The QoS\_Accept property as shown in Table A4.20 is used to define whether an interface includes the QoS accept indicator signals.

Table A4.20: QoS\_Accept property
<table><tr><td>QoS_Accept Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>The interface includes VAWQOSACCEPT and VARQOSACCEPT signals.</td></tr><tr><td>False</td><td>Y</td><td>The interface does not include VAWQOSACCEPT or VARQOSACCEPT signals.</td></tr></table>

# Chapter A5 Transaction identifiers and ordering

This chapter describes transaction identifiers and how they can be used to control the ordering of transactions.

It contains the following sections:

• A5.1 Transaction identifiers

• A5.2 Unique ID indicator

• A5.3 Request ordering

• A5.4 Interconnect use oftransaction identifiers

• A5.5 Write data and response ordering

• A5.6 Read data ordering

## A5.1 Transaction identifiers

The AXI protocol includes a transaction identifier (AXI ID). A Manager can use the AXI ID to identify transactions that must be returned in order.

All transactions with a given AXI ID value must remain ordered, but there is no restriction on the ordering of transactions with different ID values. A single physical port can support out-of-order transactions by acting as several logical ports, each handling its transactions in order.

By using AXI IDs, a Manager can issue transactions without waiting for earlier transactions to complete. This can improve system performance because it enables parallel processing of transactions.

## A5.1.1 Transaction ID signals

The read and write request, read data, and write response channels include a transaction ID signal.

Table A5.1: ID signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWID</td><td>ID_W_WIDTH</td><td>All zeros</td><td>Transaction identifier used for the ordering of write requests.</td></tr><tr><td>BID</td><td>ID_W_WIDTH</td><td>All zeros</td><td>Transaction identifier used for the ordering of write responses.</td></tr><tr><td>ARID</td><td>ID_R_WIDTH</td><td>All zeros</td><td>Transaction identifier used for the ordering of read requests.</td></tr><tr><td>RID</td><td>ID_R_WIDTH</td><td>All zeros</td><td>Transaction identifier used for the ordering of read data.</td></tr></table>

The ID width properties are described in Table A5.2.

Table A5.2: ID width properties
<table><tr><td>Name</td><td>Values</td><td>Default Description</td><td></td></tr><tr><td>ID_W_WIDTH</td><td>0..32</td><td></td><td>ID width on write channels in bits, applies to AWID and BID.</td></tr><tr><td>ID_R_WIDTH</td><td>0..32</td><td></td><td>ID width on read channels in bits, applies to ARID and RID.</td></tr></table>

If a width property is zero, the associated signal is not present.

A Manager that does not support reordering of its requests and responses, or has only one outstanding transaction, can omit the ID signals from its interface. An attached Subordinate must have its AxID inputs tied LOW.

A Subordinate that does not reorder requests or responses does not need to use ID values.

If a Subordinate does not include ID signals, it cannot be connected to a Manager that does have ID signals, because the Manager requires BID and RID to be reflected from AWID and ARID.

## A5.2 Unique ID indicator

The unique ID indicator is an optional flag that indicates when a request on the read or write address channels is using an AXI identifier that is unique for in-flight transactions. A corresponding signal is also on the read and write response channels to indicate that a transaction is using a unique ID.

The unique ID indicator can be used downstream of the AXI Manager to determine when a request needs to be ordered with respect to other requests from that Manager. Requests that do not require ordering might not require tracking in downstream components.

The Unique\_ID\_Support property is used to indicate whether an interface supports unique ID indication.

Table A5.3: Unique\_ID\_Support property
<table><tr><td>Unique_ID_Support Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>Unique ID indicator signals are present on the interface.</td></tr><tr><td>False</td><td>Y</td><td>Unique ID indicator signals are not present on the interface.</td></tr></table>

When Unique\_ID\_Support is True, the following signals are included on the read request, read data, write request, and write response channels.

Table A5.4: Unique ID indicator signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWIDUNQ,</td><td>1</td><td>0b0</td><td>If asserted high, the ID for this transfer is</td></tr><tr><td>BIDUNQ, ARIDUNQ,</td><td></td><td></td><td>unique-in-flight.</td></tr><tr><td>RIDUNQ</td><td></td><td></td><td></td></tr></table>

The following rules apply to the unique ID indicators:

• When AWIDUNQ is asserted, there must be no outstanding write transactions from this Manager with the same AWID value.

• A Manager must not issue a write request with the same AWID as an outstanding write transaction that had AWIDUNQ asserted.

• If AWIDUNQ is deasserted for a request, the corresponding BIDUNQ signal must be deasserted in a single transfer response or the Completion part of a multi-transfer response.

• If AWIDUNQ is asserted for a request, the corresponding BIDUNQ signal must be asserted in a single transfer response or the Completion part of a multi-transfer response.

• When ARIDUNQ is asserted, there must be no outstanding read transactions from this Manager with the same ARID value.

• A Manager must not issue a read request with the same ARID as an outstanding read transaction that had ARIDUNQ asserted.

• If ARIDUNQ is deasserted for a request, the corresponding RIDUNQ signal must be deasserted for all response transfers for that transaction.

• If ARIDUNQ is asserted for a request, the corresponding RIDUNQ signal must be asserted for all response transfers for that transaction.

• For an Atomic transaction that includes read and write responses, additional rules apply:

– If AWIDUNQ is deasserted for an Atomic request, the corresponding RIDUNQ signal must be deasserted for all response transfers for that transaction.

– If AWIDUNQ is asserted for an Atomic request, the corresponding RIDUNQ signal must be asserted for all response transfers for that transaction.

A transaction is outstanding from the cycle that had AxVALID asserted until the cycle when the final response transfer is accepted by the Manager. If an interface includes BCOMP, the transaction is considered to be outstanding until a response is received with BCOMP asserted.

An Atomic transaction is outstanding until both write and read responses are accepted by the Manager, see A6.4 Atomic transactions.

Some transaction types specify that AxIDUNQ is required to be asserted, if present. If not specified, asserting AxIDUNQ is optional, even if there are no outstanding transactions using the same ID.

## A5.3 Request ordering

The AXI request ordering model is based on the use of the transaction identifier, which is signaled on ARID or AWID.

Transaction requests on the same channel, with the same ID and destination are guaranteed to remain in order.   
Transaction responses with the same ID are returned in the same order as the requests were issued.

The ordering model does not give any ordering guarantees between:

• Transactions from different Managers

• Read and write transactions

• Transactions with different IDs

• Transactions to different Peripheral regions

• Transactions to different Memory locations

If a Manager requires ordering between transactions that have no ordering guarantee, the Manager must wait to receive a response to the first transaction before issuing the second transaction.

## A5.3.1 Memory locations and Peripheral regions

The address map in AMBA is made up of Memory locations and Peripheral regions.

A Memory location has all of the following properties:

• A read of a byte from a Memory location returns the last value that was written to that byte location.

• A write to a byte of a Memory location updates the value at that location to a new value that is obtained by a subsequent read of that location.

• Reading or writing to a Memory location has no side-effects on any other Memory location.

• Observation guarantees for Memory are given for each location.

• The size of a Memory location is equal to the single-copy atomicity size for that component.

A Peripheral region has all of the following properties:

• A read from an address in a Peripheral region does not necessarily return the last value that was written to that address.

• A write to a byte address in a Peripheral region does not necessarily update the value at that address to a new value that is obtained by subsequent reads.

• Accessing an address within a Peripheral region might have side-effects on other addresses within that region.

• Observation guarantees for Peripherals are given per region.

• The size of a Peripheral region is IMPLEMENTATION DEFINED but it must be contained within a single Subordinate component.

A transaction can be to one or more address locations. The locations are determined by AxADDR and any relevant qualifiers such as the address space.

• Ordering guarantees are given only between accesses to the same Memory location or Peripheral region.

• A transaction to a Peripheral region must be entirely contained within that region.

• A transaction that spans multiple Memory locations has multiple ordering guarantees.

## A5.3.2 Device and Normal requests

Transactions can be either of type Device or Normal.

## Device

A read or write where the request has AxCACHE[1] deasserted.

Device transactions can be used to access Peripheral regions or Memory locations.

## Normal

A read or write where the request has AxCACHE[1] asserted.

Normal transactions are used to access Memory locations and are not expected to be used to access Peripheral regions.

A Normal access to a Peripheral region must complete in a protocol compliant manner, but the result is IMPLEMENTATION DEFINED.

## A5.3.3 Observation and completion definitions

For accesses to Peripheral regions, a Device read or write access DRW1 is observed by a Device read or write access DRW2, when DRW1 arrives at the Subordinate component before DRW2.

For accesses to Memory locations, all of the following apply:

• A write W1 is observed by a write W2, if W2 takes effect after W1.

• A read R1 is observed by a write W2, if R1 returns data from a write W3, when W2 is after W3.

• A write W1 is observed by a read R2, if R2 returns data from either W1 or from write W3, when W3 is after W1.

Read R1 or write W1 can be of type Device or Normal.

The definitions of write and read completions are:

## Write completion response

The cycle when the associated BRESP handshake is given, when BVALID, BREADY and BCOMP (if present) are asserted.

## Read completion response

The cycle when the last associated RDATA handshake is given, when RVALID, RLAST and RREADY are asserted.

## A5.3.4 Manager ordering guarantees

There are three types of ordering model guarantees:

• Observability guarantees before a completion response is received.

• Observability guarantees from a completion response.

• Response ordering guarantees.

## Observability guarantees before a completion response is received

All of the following guarantees apply to transactions from the same Manager using the same ID:

• A Device write DW1 is guaranteed to arrive at the destination before Device write DW2, where DW2 is issued after DW1 and to the same Peripheral region.

• A Device read DR1 is guaranteed to arrive at the destination before Device read DR2, where DR2 is issued after DR1 and to the same Peripheral region.

• A write W1 is guaranteed to be observed by a write W2, where W2 is issued after W1 and both have the same cacheability and Memory location.

• A write W1 that has been observed by a read R2 is guaranteed to be observed by a read R3, where R3 is issued after R2 and have the same cacheability and Memory location.

## Observability guarantees from a completion response

The guarantees from a completion response are as follows:

• For a read request, the completion response guarantees that it is observable to a subsequent read or write request from any Manager.

• For a Non-bufferable write request, the completion response guarantees that it is observable to a subsequent read or write request from any Manager.

• For a Bufferable write request, the completion response can be sent from an intermediate point. It does not guarantee that the write has completed at the endpoint but does guarantee observability, depending on the Domain of the request:

– Non-shareable: observable to the issuing Manager only.

– Shareable: observable to all other Managers in the Shareable Domain.

– System: observable to all other Managers.

For more information on Domains, see A8.3 Cache coherency and Domains.

## Response ordering guarantees

Transaction responses have all the following ordering guarantees:

• A read R1 is guaranteed to receive a response before the response to a read R2, where R2 is issued from the same Manager after R1 with the same ID.

• A write W1 is guaranteed to receive a response before the response to a write W2, where W2 is issued from the same Manager after W1 with the same ID.

## A5.3.5 Subordinate ordering requirements

To meet the Manager ordering guarantees, Subordinate interfaces must meet the following requirements.

## Peripheral locations

For Peripheral locations, the execution order of transactions to Peripheral locations is IMPLEMENTATION DEFINED. This execution order is typically expected to match the arrival order but that is not a requirement.

## Memory locations

For transactions with the same cacheability and Memory location:

• A write W1 must be ordered before a write W2 with the same ID, where W2 is received after W1 is received.

• A write W1 must be ordered before a write W2, where W2 is received after the completion response for W1 is given.

• A write W1 must be ordered before a read R2, where R2 is received after the completion response for W1 is given.

• A read R1 must be ordered before a write W2, where W2 is received after the completion response for R1 is given.

## Response ordering requirements

• The response to read R1 must be returned before the response to a read R2, where R2 is received after R1 with the same ID.

• The response to write W1 must be returned before the response to a write W2, where W2 is received after W1 with the same ID.

## A5.3.6 Interconnect ordering requirements

An interconnect component has the following attributes:

• A request is received on one port and is either issued on a different port or responded to.

• A response is received on one port and is either issued on a different port or consumed.

When the interconnect issues requests or responses, it must adhere to the following requirements:

• A read R1 request must be issued before a read R2 request, where R2 is received after R1, with the same ID and to the same or overlapping locations.

• A write W1 request must be issued before a write W2 request, where W2 is received after W1, with the same ID, to the same or overlapping locations.

• A Device read DR1 request must be issued before a Device read DR2 request, where DR2 is received after DR1, with the same ID and to the same Peripheral region.

• A Device write DW1 request must be issued before a Device write DW2 request, where DW2 is received after DW1, with the same ID and to the same Peripheral region.

• A read R1 response must be issued before a read R2 response, where R2 is received after R1, with the same ID.

• A write W1 response must be issued before a write W2 response, where W2 is received after W1, with the same ID.

When the interconnect is acting as a Subordinate component, it must also adhere to the Subordinate requirements.

Any manipulation of the AXI ID values that are associated with a transaction must ensure that the ordering requirements of the original ID values are maintained.

## A5.3.7 Response before the endpoint

To improve system performance, it is possible for an intermediate component to issue a response to some transactions. This action is known as an early response. The intermediate component issuing an early response must ensure that visibility and ordering guarantees are met.

## Early read response

For Normal read transactions, an intermediate component can respond with read data from a local memory if it is up to date with respect to all earlier writes to the same or overlapping address. In this case, the request is not required to propagate beyond the intermediate component.

An intermediate component must observe ID ordering rules, which means a read response can only be sent if all earlier reads with the same ID have already had a response.

## Early write response

For Bufferable write transactions (AWCACHE[0] is asserted), an intermediate component can send an early write response for transactions that have no downstream observers. If the intermediate component sends an early write response, the intermediate component can store a local copy of the data, but must propagate the transaction downstream, before discarding that data.

An intermediate component must observe ID ordering rules, which means a write response can only be sent if all earlier writes with the same ID have already had a response.

After sending an early write response, the component must be responsible for ordering and observability of that transaction until the write has been propagated downstream, and a write response is received. During the period between sending the early write response and receiving a response from downstream, the component must ensure that:

• If an early write response was given for a Normal transaction, all subsequent transactions to the same or overlapping Memory locations are ordered after the write that has had an early response.

• If an early write response was given for a Device transaction, then all subsequent transactions to the same Peripheral region are ordered after the write that has had an early response.

When giving an early write response for a Device Bufferable transaction, the intermediate component is expected to propagate the write transaction without dependency on other transactions. The intermediate component cannot wait for another read or write to arrive before propagating a previous Device write.

## A5.3.8 Ordering between requests with different memory types

There are no ordering requirements between Cacheable requests and Device or Non-cacheable Normal requests.   
Responses must be in order for transactions with the same AXI ID, irrespective of cacheability.

Ordering requirements between Device and Normal Non-cacheable requests depends on the Device\_Normal\_Independence property.

Table A5.5: Device\_Normal\_Independence property
<table><tr><td>Device_Normal_Independence Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>A Device request is permitted to overtake, or be overtaken by, a Normal Non-cacheable request with the same ID to the same location.</td></tr><tr><td>False</td><td>Y</td><td>Device and Normal Non-cacheable requests with the same ID, to the same location must be observed in issue order.</td></tr></table>

Guidance for connecting Manager and Subordinate interfaces with different values of Device\_Normal\_Independence is shown in Table A5.6.

Table A5.6: Device\_Normal\_Independence interoperability
<table><tr><td></td><td>Subordinate: False</td><td>Subordinate: True</td></tr><tr><td>Manager: False</td><td>Compatible.</td><td>Incompatible. The Subordinate might not meet the ordering requirements of the Manager.</td></tr><tr><td>Manager: True</td><td>Compatible. The Subordinate might enforce stricter ordering than required.</td><td>Compatible.</td></tr></table>

## A5.3.9 Ordered write observation

To improve compatibility with interface protocols that support a different ordering model, a Subordinate interface can give stronger ordering guarantees for write transactions, known as Ordered Write Observation.

The Ordered\_Write\_Observation property is used to define whether an interface has Ordered Write Observation.

Table A5.7: Ordered\_Write\_Observation property
<table><tr><td>Ordered_Write_Observation Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>The interface exhibits Ordered Write Observation</td></tr><tr><td>False</td><td>Y</td><td>The interface does not exhibit Ordered Write Observation.</td></tr></table>

An interface that exhibits Ordered Write Observation gives guarantees for write transactions that are not dependent on the destination or address:

• A write W1 is guaranteed to be observed by a write W2, where W2 is issued after W1, from the same Manager, with the same ID.

When using Ordered Write Observation, a Manager can issue multiple write requests without waiting for write responses, and they are observed in issue order. This can result in improved performance when using the Producer-Consumer ordering model.

## A5.4 Interconnect use of transaction identifiers

When a Manager is connected to an interconnect, the interconnect appends additional bits to the AWID and ARID identifiers that are unique to that Manager port. This has two effects:

• Managers do not have to know what ID values are used by other Managers because the interconnect makes the ID values used by each Manager unique by appending the Manager number to the original identifier.

• The ID identifier at a Subordinate interface is wider than the ID identifier at a Manager interface.

For write responses, the interconnect uses the additional bits of the BID identifier to determine which Manager port the write response is destined for. The interconnect removes these bits of the BID identifier before passing the BID value to the correct Manager port.

For read data, the interconnect uses the additional bits of the RID identifier to determine which Manager port the read data is destined for. The interconnect removes these bits of the RID identifier before passing the RID value to the correct Manager port.

## A5.5 Write data and response ordering

A Manager must issue write data in the same order that it issues the transaction requests.

When using credited transport, this rule applies to each Resource Plane. Therefore, it is permitted to send data out of order with respect to requests if they are using different Resource Planes. Interleaving data transfers for different transactions is permitted if they are on different Resource Planes. See A2.4.2 Resource Planes for more information on Resource Planes.

Figure A5.1 shows an example of write data ordering and interleaving when using two Resource Planes, it shows:

• Data for the transaction with ID1 is permitted to be issued before data for ID0 as they are using different RPs.

• Data transfers for ID1 can be interleaved between transfers for ID0 or ID2, as they are using different RPs.

![](images/7c6114915a2f78be52169aaabeda46b678d49c14e5f1840e09f0056277d01ad6.jpg)  
Figure A5.1: Example of a write data ordering with two Resource Planes

A Subordinate must ensure that the BID value of a write response matches the AWID value of the request to which it is responding.

An interconnect must ensure that write responses from a sequence of transactions with the same AWID value targeting different Subordinates are received by the Manager in request order.

## A5.6 Read data ordering

The Subordinate must ensure that the RID value of any returned data matches the ARID value of the request to which it is responding.

The interconnect must ensure that read data from a sequence of transactions with the same ARID value targeting different Subordinates are received by the Manager in request order.

The read data reordering depth is the maximum number of accepted requests for which a Subordinate might send read data. A Subordinate that sends read data in the same order as the requests were received has a read data reordering depth of one.

The read data reordering depth is a static value that can be specified by the designer of the Subordinate.

There is no mechanism for a Manager to dynamically determine the read data reordering depth of a Subordinate.

## A5.6.1 Read data interleaving

AXI ordering permits read data transfers with different ID values to be interleaved. This applies to all transactions that can have multiple read data transfers, including Atomic transactions.

Some AXI Manager and interconnect components can be more efficiently designed if it is determined at design-time whether the attached Subordinate interface will interleave read data from different transactions.

The property Read\_Interleaving\_Disabled is used to indicate whether an interface supports the interleaving of read data transfers from different transactions.

Table A5.8: Read\_Interleaving\_Disabled property
<table><tr><td>Read_Interleaving_Disabled Default</td><td>Description</td></tr><tr><td>True</td><td>A Manager interface is not capable of receiving read data that is interleaved. A Subordinate interface is guaranteed not to interleave read data.</td></tr><tr><td>False Y</td><td>A Manager interface is capable of receiving read data that is interleaved.</td></tr><tr><td></td><td>A Subordinate interface might interleave data from read transactions with different ARID values.</td></tr></table>

For some interfaces, this property can be used as a configuration control, for others it is a capability indicator. All Managers that issue transactions with different IDs must be designed to accept interleaved data. Managers might use the configuration option to disable interleaving as an optimization when the attached Subordinate supports the disabling of interleaving.

## A5.6.2 Read data chunking

The read data chunking option enables a Subordinate interface to reorder read data within a transaction using a 128b granule. The start address might be used as a hint to determine which chunk to send first, but the Subordinate is permitted to return chunks of data in any order.

The property Read\_Data\_Chunking is used to indicate whether an interface supports the return of read data in reorderable chunks.

Table A5.9: Read\_Data\_Chunking property
<table><tr><td>Read_Data_Chunking Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>Read data chunking is supported.</td></tr><tr><td>False</td><td>Y</td><td>Read data chunking is not supported, no chunking signals are present.</td></tr></table>

## A5.6.2.1 Read data chunking signaling

When read data chunking is supported, the following signals as shown in Table A5.10 are added to the read request and data channel.

Table A5.10: Read data chunking signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>ARCHUNKEN</td><td>1</td><td>0b0</td><td>If asserted in a read request, the Subordinate can send read data in 128b chunks.</td></tr><tr><td>RCHUNKV</td><td>1</td><td>0b0</td><td>Asserted high to indicate that RCHUNKNUM and RCHUNKSTRB are valid. It must be the same for every response of the transaction.</td></tr><tr><td>RCHUNKNUM</td><td>RCHUNKNUM WIDTH</td><td>All zeros</td><td>Indicates the chunk number being transferred. Chunks are numbered incrementally from zero, according to the data width and base address of the transaction.</td></tr><tr><td>RCHUNKSTRB</td><td>RCHUNKSTRB_WIDTH</td><td>All ones</td><td>Indicates the read data chunks that are valid for this transfer. Each bit corresponds to 128 bits of data. The least significant bit of RCHUNKSTRB corresponds to the least significant 128 bits of RDATA.</td></tr></table>

The RCHUNKNUM\_WIDTH property defines the width of the RCHUNKNUM signal.

Table A5.11: RCHUNKNUM\_WIDTH property
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>RCHUNKNUM_WIDTH</td><td>10,1,5,6,7,8</td><td>0</td><td>Width of RCHUNKNUM in bits.</td></tr><tr><td></td><td></td><td></td><td>Must be 0 if Read_Data_Chunking == False else</td></tr><tr><td></td><td></td><td></td><td>0 or 1 if DATA WIDTH &lt; 128</td></tr><tr><td></td><td></td><td></td><td>8 if DATA_WIDTH == 128</td></tr><tr><td></td><td></td><td></td><td>7 if DATA_WIDTH == 256</td></tr><tr><td></td><td></td><td></td><td>6 if DATA_WIDTH == 512</td></tr><tr><td></td><td></td><td></td><td>5 if DATA_WIDTH == 1024</td></tr></table>

The RCHUNKSTRB\_WIDTH property defines the width of the RCHUNKSTRB signal.

Table A5.12: RCHUNKSTRB\_WIDTH property
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>RCHUNKSTRB_WIDTH</td><td>I0,1, 2,4,8</td><td>0</td><td>Width of RCHUNKSTRB in bits.</td></tr><tr><td></td><td></td><td></td><td>Must be 0 if Read_Data_Chunking == False else</td></tr><tr><td></td><td></td><td></td><td>0 or 1 if DATA_WIDTH &lt; 256</td></tr><tr><td></td><td></td><td></td><td>2 if DATA_WIDTH == 256</td></tr><tr><td></td><td></td><td></td><td>4 if DATA_WIDTH == 512</td></tr><tr><td></td><td></td><td></td><td>8 if DATA_WIDTH == 1024</td></tr></table>

Interfaces with a small DATA\_WIDTH can include RCHUNKNUM and RCHUNKSTRB signals as 1-bit wide or omit them from the interface. When using interface protection, the RCHUNKCHK signal covers both of these signals, so RCHUNKNUM and RCHUNKSTRB must be the same width for connected components.

It is recommended that RCHUNKNUM and RCHUNKSTRB are omitted if not required by the interface.

## A5.6.2.2 Read data chunking protocol rules

In the read data chunking protocol, all the following rules apply:

• ARCHUNKEN must only be asserted for transactions with the following attributes:

– Size is equal to the data channel width, or Length is one transfer.

– Size is 128 bits or larger.

– Addr is aligned to 16 bytes.

– Burst is INCR or WRAP.

– Opcode is ReadNoSnoop, ReadOnce, ReadOnceCleanInvalid, or ReadOnceMakeInvalid.

• The ID value must be unique-in-flight, which means:

– ARCHUNKEN can only be asserted if there are no outstanding read transactions using the same ARID value.

– The Manager must not issue a request on the read channel with the same ARID as an outstanding request that had ARCHUNKEN asserted.

– If present on the interface, ARIDUNQ must be asserted if ARCHUNKEN is asserted.

• If ARCHUNKEN is deasserted, RCHUNKV must be deasserted for all response transfers of the transaction.

• If ARCHUNKEN is asserted, RCHUNKV can be asserted for response transfers of the transaction.

• RCHUNKV must be the same for every response transfer of a transaction.

• When RVALID and RCHUNKV are asserted, RCHUNKNUM must be between zero and ARLEN.

• When RVALID and RCHUNKV are asserted, RCHUNKSTRB must not be zero.

• When RVALID and RCHUNKV are asserted, RLAST must only be asserted for the final response transfer of the transaction, irrespective of RCHUNKNUM and RCHUNKSTRB.

• When RVALID is asserted and RCHUNKV is deasserted, RCHUNKNUM and RCHUNKSTRB can take any value.

The number of data chunks transferred must be consistent with ARLEN and ARSIZE, so the number of bytes transferred in a transaction is the same whether chunking is enabled or not. Note that when using read data chunking, a transaction might have more read data transfers than indicated by ARLEN.

For unaligned transactions, chunks at addresses lower than ARADDR are not transferred and must have RCHUNKSTRB deasserted.

## A5.6.2.3 Interoperability

If a Manager supports read data chunking, then downstream interconnect and Subordinates can reduce their buffering if they also support chunking. An interconnect which connects to components with a mixture of chunking support can drive ARCHUNKEN and RCHUNKV according to the capabilities of the attached components.

When connecting interfaces with different values for the Read\_Data\_Chunking property, the following rules apply as shown in Table A5.13.

Table A5.13: Read\_Data\_Chunking interoperability
<table><tr><td></td><td>Subordinate: False</td><td>Subordinate: True</td></tr><tr><td rowspan="5">Manager: False</td><td>ARCHUNKEN is not present.</td><td>Subordinate ARCHUNKEN input is tied low.</td></tr><tr><td>RCHUNKV is not present.</td><td>Subordinate RCHUNKV output is unconnected.</td></tr><tr><td>RCHUNKNUM is not present.</td><td>Subordinate RCHUNKNUM output is unconnected.</td></tr><tr><td>RCHUNKSTRB is not present</td><td>Subordinate RCHUNKSTRB output is unconnected.</td></tr><tr><td>Full data transfers are sent in natural order. Full data transfers are sent in natural order.</td><td></td></tr><tr><td rowspan="5">Manager: True</td><td>Manager ARCHUNKEN output is unconnected.</td><td>Chunking signals are connected.</td></tr><tr><td>Manager RCHUNKV input is tied low.</td><td>Read data can be reordered and sent in chunks.</td></tr><tr><td>Manager RCHUNKNUM input is tied.</td><td></td></tr><tr><td>Manager RCHUNKSTRB input is tied.</td><td></td></tr><tr><td>Full data transfers are sent in natural order.</td><td></td></tr></table>

## A5.6.2.4 Chunking examples

In these examples, each row in the figure represents a transfer and the shaded cells indicate bytes that are not transferred.

![](images/775a6638c7b7b17494f0d1d93aba7c8a6b1afdb9d087935c16c97dd118cf28c9.jpg)  
Figure A5.2: Example of read data returned in 128-bit chunks  
Figure A5.3: Example with an unaligned address and a mixture of 128-bit and 256-bit chunks

Figure A5.2 shows a transaction on a 256-bit width read data channel where:

• Addr is 0x00.

• Length is 2 transfers.

• Size is 256 bits.

• Burst is INCR.

$$
\mathsf { R C H U N K N U M } = 1 ; \mathsf { R C H U N K S T R B } = 0 . 0 0 1 ; \mathsf { R L A S T } = 0
$$

$$
{ \mathsf { R C H U N K N U M } } = 0 ; { \mathsf { R C H U N K S T R B } } = 0 { \mathsf { b } } 1 0 ; { \mathsf { R L A S T } } = 0
$$

$$
\mathsf { R C H U N K N U M } = 1 ; \mathsf { R C H U N K S T R B } = 0 \mathsf { b } 1 0 ; \mathsf { R L A S T } = 0
$$

$$
{ \mathsf { R C H U N K N U M } } = 0 ; { \mathsf { R C H U N K S T R B } } = 0 { \mathsf { b } } 0 1 ; { \mathsf { R L A S T } } = 1
$$

Figure A5.3 shows a transaction on a 256-bit width read data channel, where:

• Addr is 0x10.

• Length is 2 transfers.

• Size is 256 bits.

• Burst is INCR.

$$
{ \mathsf { R C H U N K N U M } } = 0 ; { \mathsf { R C H U N K S T R B } } = 0 { \mathsf { b } } 1 0 ; { \mathsf { R L A S T } } = 0
$$

$$
\mathsf { R C H U N K N U M } = 1 ; \mathsf { R C H U N K S T R B } = 0 . 0 1 1 ; \mathsf { R L A S T } = 1
$$

Figure A5.4 shows a transaction on a 128-bit width read data channel, where:

• Addr is 0x10.

• Length is 4 transfers.

• Size is 128 bits.

• Burst is WRAP.

• RCHUNKSTRB is not present.

The Subordinate uses the start address as a hint and sends the chunk at 0x10 first.

Chapter A5. Transaction identifiers and ordering A5.6. Read data ordering

![](images/e8791c3a9fe773f10b00e71c54e8959b81e32f532d7671b6e39d68a220ba0a8f.jpg)  
Figure A5.4: Example of a wrapping transaction

# Chapter A6 Atomic accesses

This chapter describes single-copy and multi-copy atomicity and how to perform exclusive accesses and atomic transactions.

It contains the following sections:

• A6.1 Single-copy atomicity size

• A6.2 Multi-copy write atomicity

• A6.3 Exclusive accesses

• A6.4 Atomic transactions

## A6.1 Single-copy atomicity size

The single-copy atomicity size is the minimum number of bytes that a transaction updates atomically. The AXI protocol requires a transaction that is larger than the single-copy atomicity size to update memory in blocks of at least the single-copy atomicity size.

Atomicity does not define the exact instant when the data is updated. What must be ensured is that no Manager can ever observe a partially updated form of the atomic data. For example, in many systems, data structures such as linked lists are made up of 32-bit atomic elements. An atomic update of one of these elements requires that the entire 32-bit value is updated at the same time. It is not acceptable for any Manager to observe an update of only 16 bits at one time, and then the update of the other 16 bits later.

More complex systems require support for larger atomic elements, in particular 64-bit atomic elements, so that Managers can communicate using data structures that are based on these larger atomic elements.

The single-copy atomicity sizes that are supported in a system are important because all the components involved in a given communication must support the required size of atomic element. If two Managers are communicating through an interconnect and a single Subordinate, then all the components involved must ensure that transactions of the required size are treated atomically.

The AXI protocol does not require a specific single-copy atomicity size and systems can be designed to support different single-copy atomicity sizes.

In AXI the term single-copy atomic group describes a group of components that can communicate at a particular atomicity. For example, Figure A6.1 shows a system in which:

• The CPU, DSP, DRAM controller, DMA controller, peripherals, SRAM memory and associated interconnect, are in a 32-bit single-copy atomic group.

• The CPU, DSP, DRAM controller, and associated interconnect are also in a 64-bit single-copy atomic group.

![](images/c23c58d6f99c71e1193f0108ea6d3293829d2782bc611cdea6ea4ff71b348a42.jpg)  
Figure A6.1: Example system with different single-copy atomic groups

A transaction never has an atomicity guarantee greater than the alignment of its start address. For example, a transaction in a 64-bit single-copy atomic group that is not aligned to an 8-byte boundary does not have any 64-bit single-copy atomic guarantee.

Byte strobes associated with a transaction do not affect the single-copy atomicity size.

## A6.2 Multi-copy write atomicity

A system is defined as being multi-copy atomic if:

• Writes to the same location are observed in the same order by all agents.

• A write to a location that is observable by an agent, is observable by all agents.

To specify that a system provides multi-copy atomicity, a Multi\_Copy\_Atomicity property is defined.

Table A6.1: Multi\_Copy\_Atomicity property
<table><tr><td>Multi_Copy_Atomicity Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>Multi_Copy_Atomicity is supported.</td></tr><tr><td>False</td><td>Y</td><td>Multi_Copy_Atomicity is not supported.</td></tr></table>

Multi-copy atomicity can be ensured by:

• Using a single Point of Serialization (PoS) for a given address, so that all accesses to the same location are ordered. This must ensure that all coherent cached copies of a location are invalidated before the new value of the location is made visible to any agents.

• Avoiding the use of forwarding buffers that are upstream of any agents. This prevents a buffered write of a location becoming visible to some agents before it is visible to all agents.

It is required that the Multi\_Copy\_Atomicity property is True for Issue G and later of this specification.

## A6.3 Exclusive accesses

The exclusive access mechanism can provide semaphore-type operations without requiring the connection to remain dedicated to a particular Manager during the operation.

The AxLOCK signals are used to indicate an exclusive access, and the BRESP and RRESP signals indicate the success or failure of the exclusive access write or read respectively.

Table A6.2: AxLOCK signals

<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWLOCK, ARLOCK</td><td>1</td><td>0b0</td><td>Asserted high to indicate that an exclusive access is required.</td></tr></table>

The Exclusive\_Accesses property is used to define whether a Manager issues exclusive accesses or whether a Subordinate supports them:

Table A6.3: Exclusive\_Accesses property
<table><tr><td>Exclusive_Accesses</td><td>Default</td><td>Description</td></tr><tr><td>True</td><td>Y</td><td>Exclusive accesses are supported. AWLOCK and ARLOCK are present on the interface.</td></tr><tr><td>False</td><td></td><td>Exclusive accesses are not supported. AWLOCK and ARLOCK are not present on the interface.</td></tr></table>

Table A6.4 provides guidance that applies when connecting Manager and Subordinate components with different property values:

Table A6.4: Exclusive Accesses Interoperability
<table><tr><td></td><td>Subordinate: False</td><td>Subordinate: True</td></tr><tr><td>Manager: False</td><td>Compatible.</td><td>Compatible. AWLOCK and ARLOCK are tied LOW.</td></tr><tr><td>Manager: True</td><td>Not compatible. Exclusive accesses will continually fail, but the interface will not deadlock.</td><td>Compatible.</td></tr></table>

## A6.3.1 Exclusive access sequence

The mechanism of an exclusive access sequence is:

1. A Manager issues an exclusive read request from an address.

2. At some later time, the Manager attempts to complete the exclusive operation by issuing an exclusive write request to the same address, with an AWID that matches the ARID used for the exclusive read.

3. This exclusive write access is signaled as either:

• Successful, if no other Manager has written to that location since the exclusive read access. In this case, the exclusive write updates memory.

• Failed, if another Manager has written to that location since the exclusive read access. In this case, the memory location is not updated.

A Manager might not complete the write portion of an exclusive operation. The exclusive access monitoring hardware monitors only one address for each transaction ID. If a Manager does not complete the write portion of an exclusive operation, a subsequent exclusive read by that Manager using the same transaction ID changes the address that is being monitored for exclusive accesses.

## A6.3.2 Exclusive access from the perspective of the Manager

A Manager starts an exclusive operation by performing an exclusive read. If the transaction is successful, the Subordinate returns the EXOKAY response, indicating that the Subordinate recorded the address to be monitored for exclusive accesses.

If the Manager attempts an exclusive read from a Subordinate that does not support exclusive accesses, the Subordinate returns the OKAY response instead of the EXOKAY response. In this case, the read data is valid, but the location is not being monitored for exclusivity.

The Manager can treat the OKAY response as an error condition indicating that the exclusive access is not supported. It is recommended that the Manager does not perform the write portion of this exclusive operation.

At some time after the exclusive read, the Manager tries an exclusive write to the same location. If the contents of the addressed location have not been updated since the exclusive read, the exclusive write operation succeeds. The Subordinate returns the EXOKAY response, and updates the memory location.

If the contents of the addressed location have been updated since the exclusive read, the exclusive write attempt fails, and the Subordinate returns the OKAY response instead of the EXOKAY response. The exclusive write attempt does not update the memory location.

A Manager might not complete the write portion of an exclusive operation. If this happens, the Subordinate continues to monitor the address for exclusive accesses until another exclusive read starts a new exclusive access sequence.

A Manager must not start the write part of an exclusive access sequence until the read part is complete.

## A6.3.3 Exclusive access restrictions

The following restrictions apply to exclusive accesses:

• The address of an exclusive access must be aligned to the total number of bytes in the transaction, that is, the product of Size and Length

• The number of bytes to be transferred in an exclusive access transaction must be a power-of-2, that is, 1, 2, 4, 8, 16, 32, 64, or 128 bytes.

• The Length of an exclusive access must not exceed 16 transfers.

• The Domain must not be Shareable, see A8.3.3 Shareable Domain.

• The Opcode must be ReadExclusive or WriteExclusive. See Chapter A7 Request Opcodes.

• AWTAGOP must not be Match, see A12.2 Memory Tagging Extension (MTE).

Failure to observe these restrictions causes UNPREDICTABLE behavior.

For an exclusive sequence to be successful, the AxCACHE values must be appropriate to ensure that the read and write requests reach the exclusive access monitor.

The minimum number of bytes to be monitored during an exclusive operation is the product of Size and Length.

The Subordinate can monitor a larger number of bytes, up to 128, which is the maximum number of bytes in an exclusive access. However, this can result in a successful exclusive access being indicated as failing because a neighboring byte was updated.

If any of the signals shown in Table A6.5 are different between the read and write requests in an exclusive sequence, the exclusive write might fail even if the location has not been updated by another agent.

Table A6.5: Signals that should be the same in an exclusive sequence
<table><tr><td>AxID</td><td>AxADDR</td><td>AxREGION</td><td>AxSUBSYSID</td><td>AxDOMAIN</td></tr><tr><td>AxLEN</td><td>AxSIZE</td><td>AxBURST</td><td>AxLOCK</td><td>AxCACHE[1:0]</td></tr><tr><td>AxPROT</td><td>AxNSE</td><td>AxPAS</td><td>AxINST</td><td>AxPRIV</td></tr><tr><td>AxSNOOP</td><td>AxMMUVALID</td><td>AxMMUATST</td><td>AxMMUFLOW</td><td>AxMMUPASUNKNOWN</td></tr><tr><td>AxMMUPM</td><td>AxMMUSECSID</td><td>AxMMUSID</td><td>AxMMUSSID</td><td>AxMMUSSIDV</td></tr></table>

## A6.3.4 Exclusive access from the perspective of the Subordinate

A Subordinate that supports exclusive access must have monitor hardware. It is recommended that such a Subordinate has a monitor unit for each exclusive-capable Manager ID that can access it.

When a Subordinate receives an exclusive read request, it records the address and ARID value of any exclusive read operation. Then it monitors that location until either a write occurs to that location or until another exclusive read with the same ARID value resets the monitor to a different address.

If the Subordinate can successfully process the exclusive read, it responds with EXOKAY for every read data transfer.

If the Subordinate cannot process the exclusive read, it responds with a response which is not EXOKAY. An exclusive read can have more than one response transfers. It is not permitted to have a mix of OKAY and EXOKAY responses for a single transaction.

When the Subordinate receives an exclusive write with a given AWID value, the monitor checks to see if that address is being monitored for exclusive access with that AWID. If it is, then this indicates that no write has occurred to that location since the exclusive read access, and the exclusive write proceeds, completing the exclusive access. The Subordinate returns the EXOKAY response to the Manager and updates the addressed memory location.

If the address is not being monitored with the same AWID value at the time of an exclusive write, this indicates one of the following:

• The location has been updated since the exclusive read access.

• The monitor has been reset to another location.

• The Manager did not issue an exclusive read with the same attributes as the exclusive write.

If the monitor deems the sequence to have failed, the exclusive write must not update the addressed location, and the Subordinate must return the OKAY response instead of the EXOKAY response.

If a Subordinate that does not support exclusive accesses receives an exclusive write, it responds with an OKAY response and the location is updated.

## A6.4 Atomic transactions

Atomic transactions perform more than just a single access and have an operation that is associated with the transaction. Atomic transactions enable sending the operation to the data, permitting the operation to be performed closer to where the data is located. Atomic transactions are suited to situations where the data is located a significant distance from the agent that must perform the operation.

Compared with using exclusive accesses, this approach reduces the amount of time during which the data must be made inaccessible to other agents in the system.

Atomic transactions update the entire written location atomically, irrespective of the single-copy atomicity size of the component.

## A6.4.1 Overview

In an atomic transaction, the Manager sends an address, control information, and outbound data. The Subordinate sends inbound data (except for AtomicStore) and a response. This specification supports four forms of Atomic transaction:

## AtomicStore

• The Manager sends a single data value with an address and the atomic operation to be performed.

• The Subordinate performs the operation using the sent data and value at the addressed location as operands.

• The result is stored in the address location.

• A single response is given without data.

• Outbound data size is 1, 2, 4, or 8 bytes.

## AtomicLoad

• The Manager sends a single data value with an address and the atomic operation to be performed.

• The Subordinate returns the original data value at the addressed location.

• The Subordinate performs the operation using the sent data and value at the addressed location as operands.

• The result is stored in the address location.

• Outbound data size is 1, 2, 4, or 8 bytes.

• Inbound data size is the same as the outbound data size.

## AtomicSwap

• The Manager sends a single data value with an address.

• The Subordinate swaps the value at the addressed location with the data value that is supplied in the transaction.

• The Subordinate returns the original data value at the addressed location.

• Outbound data size is 1, 2, 4, or 8 bytes.

• Inbound data size is the same as the outbound data size.

## AtomicCompare

• The Manager sends two data values, the compare value and the swap value, to the addressed location. The compare and swap values are of equal size.

• The Subordinate checks the data value at the addressed location against the compare value:

– If the values match, the swap value is written to the addressed location.

– If the values do not match, the swap value is not written to the addressed location.

• The Subordinate returns the original data value at the addressed location.

• Outbound data size is 2, 4, 8, 16, or 32 bytes.

• Inbound data size is half of the outbound data size because the outbound data contains both compare and swap values, whereas the inbound data has only the original data value.

## A6.4.2 Atomic transaction operations

This specification supports eight different operations that can be used with AtomicStore and AtomicLoad transactions as shown in Table A6.6.

Table A6.6: Atomic transaction operators
<table><tr><td>Operator</td><td>Description</td></tr><tr><td>ADD</td><td>The value in memory is added to the sent data and the result stored in memory.</td></tr><tr><td>CLR</td><td>Every set bit in the sent data clears the corresponding bit of the data in memory.</td></tr><tr><td>EOR</td><td>Bitwise exclusive OR of the sent data and value in memory.</td></tr><tr><td>SET</td><td>Every set bit in the sent data sets the corresponding bit of the data in memory.</td></tr><tr><td>SMAX</td><td>The value stored in memory is the maximum of the existing value and sent data. This operation assumes signed data.</td></tr><tr><td>SMIN</td><td>The value stored in memory is the minimum of the existing value and sent data. This operation assumes signed data.</td></tr><tr><td>UMAX</td><td>The value stored in memory is the maximum of the existing value and sent data. This operation assumes unsigned data.</td></tr><tr><td>UMIN</td><td>The value stored in memory is the minimum of the existing value and sent data. This operation assumes unsigned data.</td></tr></table>

## A6.4.3 Atomic transactions attributes

The rules for atomic transactions are as follows:

• AWLEN and AWSIZE specify the number of bytes of write data in the transaction. For AtomicCompare, the number of bytes must include both the compare and swap values.

• If AWLEN indicates a transaction length greater than one, AWSIZE is required to be the full data channel width.

• Write strobes that are not within the data window, as specified by AWADDR and AWSIZE, must be deasserted.

• Write strobes within the data window must be asserted.

• All atomic transactions are considered to be Regular.

## For AtomicStore, AtomicLoad, and AtomicSwap

• The write data is 1, 2, 4, or 8 bytes and read data is 1, 2, 4, or 8 bytes respectively.

• AWADDR must be aligned to the total write data size.

• AWBURST must be INCR.

## For AtomicCompare

• The write data is 2, 4, 8, 16, or 32 bytes and read data is 1, 2, 4, 8, or 16 bytes.

• AWADDR must be aligned to half the total write data size.

• If AWADDR points to the lower half of the transaction:

– The compare value is sent first. The compare value is in the lower bytes of a single-transfer transaction, or in the first transfers of a multi-transfer transaction.

– AWBURST must be INCR.

• If AWADDR points to the upper half of the transaction:

– The swap value is sent first. The swap value is in the lower bytes of a single-transfer transaction, or in the first transfers of a multi-transfer transaction.

– AWBURST must be WRAP.

• There are relaxations to the usual rules for transactions of type WRAP:

– A Length of 1 is permitted.

– AWADDR is not required to be aligned to the transfer size.

– The property Wrap\_CLS\_Modifiable does not affect AtomicCompare. See A3.1.4 Wrapping address (WRAP) for more information.

Examples of AtomicCompare transactions with a 64-bit data channel are shown in Figure A6.2.

<table><tr><td>AWADDR</td><td>AWSIZE</td><td>AWLEN</td><td>AWBURST</td><td>7 6 5</td><td></td><td>4</td><td>3</td><td></td><td>2 1 0</td><td></td><td></td><td></td></tr><tr><td>0x00</td><td>1 (2B)</td><td>0</td><td>INCR</td><td>一</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>S</td><td>C</td><td></td></tr><tr><td>0x01</td><td></td><td>0</td><td>WRAP</td><td></td><td>1 1</td><td></td><td>–</td><td>1</td><td>-</td><td>C</td><td>S</td><td></td></tr><tr><td></td><td>1 (2B)</td><td></td><td></td><td>1</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>0x04</td><td>2 (4B)</td><td>0</td><td>INCR</td><td>S</td><td>S C</td><td>C</td><td></td><td>-</td><td>-</td><td>-</td><td>一</td><td></td></tr><tr><td>0x06</td><td>2 (4B)</td><td>0</td><td>WRAP</td><td>C</td><td>C S</td><td></td><td>S</td><td>–</td><td>-</td><td></td><td>一 1</td><td></td></tr><tr><td>0x00</td><td>3 (8B)</td><td>0</td><td>INCR</td><td>S</td><td>S</td><td>S</td><td>S</td><td>C</td><td>C</td><td></td><td>C C</td><td></td></tr><tr><td>0x04</td><td>3 (8B)</td><td>0</td><td>WRAP</td><td>C</td><td>C</td><td>C</td><td>C</td><td>S</td><td>S</td><td></td><td>S S</td><td></td></tr><tr><td>0x00</td><td>3 (8B)</td><td>1</td><td>INCR</td><td>C S</td><td>C S</td><td>C S S</td><td>C</td><td>C S S</td><td>C</td><td>C</td><td>C S</td><td>1st Transfer S 2ⁿd Transfer</td></tr><tr><td>0x08</td><td></td><td></td><td></td><td>S</td><td>S</td><td>S</td><td>S</td><td>S</td><td>S</td><td>S</td><td>S</td><td>1st Transfer</td></tr><tr><td></td><td>3 (8B)</td><td>1</td><td>WRAP</td><td>C</td><td>C</td><td>C</td><td>C</td><td>C</td><td>C</td><td>C</td><td>C</td><td>2ⁿd Transfer</td></tr></table>

Figure A6.2: Examples showing the location of the Compare and Swap values for an AtomicCompare

Note that the compare and swap values are sent in a different order in the last two examples.

## A6.4.4 ID use for Atomic transactions

A single AXI ID is used for an Atomic transaction. The same AXI ID is used for the request, write response, and the read data. This requirement means that the Manager must only use ID values that can be signaled on both AWID and RID signals.

The ID must be unique-in-flight for Atomic transactions, which means:

• An AtomicStore request can only be issued if there are no outstanding transactions on the write channels using the same ID value.

• A Manager must not issue a request on the write channel with the same ID value as an outstanding AtomicStore request.

• An AtomicLoad, AtomicSwap or AtomicCompare request can only be issued if there are no outstanding transactions on the read or write channels using the same ID value.

• A Manager must not issue a request on the read or write channels with the same ID value as an outstanding AtomicLoad, AtomicSwap or AtomicCompare request.

• For Atomic transactions that use the read data channel, if the interface includes Unique ID signaling then RIDUNQ must be asserted if AWIDUNQ was asserted. See A5.2 Unique ID indicator for more details.

These rules ensure there are no ordering requirements between Atomic transactions and other transactions.

## A6.4.5 Request attribute restrictions for Atomic transactions

For Atomic transactions, the following restrictions apply for request attributes:

• AWCACHE and AWDOMAIN are permitted to be any combination valid for the interface type. See Table A8.7.

• AWSNOOP must be set to all zeros. If AWSNOOP has any other value, AWATOP must be all zeros.

• AWLOCK must be deasserted, not exclusive access.

## A6.4.6 Atomic transaction signaling

To support Atomic transactions AWATOP is added to an interface.

Table A6.7: AWATOP signal
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWATOP</td><td>6</td><td>0x00</td><td>Indicates the type and endianness of an atomic transaction.</td></tr></table>

The encodings for AWATOP are shown in Table A6.8 and Table A6.9.

Table A6.8: AWATOP encodings
<table><tr><td>AWATOP[5:0]</td><td>Description</td></tr><tr><td>0b000000</td><td>Non-atomic operation</td></tr><tr><td>0b01exxx</td><td>AtomicStore</td></tr><tr><td>0b10exxx</td><td>AtomicLoad</td></tr><tr><td>0b110000</td><td>AtomicSwap</td></tr><tr><td>0b110001</td><td>AtomicCompare</td></tr></table>

For AtomicStore and AtomicLoad transactions AWATOP[3] indicates the endianness that is required for the atomic operation:

• When deasserted, this bit indicates that the operation is little-endian.

• When asserted, this bit indicates that the operation is big-endian.

The value of AWATOP[3] applies to arithmetic operations only and is ignored for bitwise logical operations.

For AtomicStore and AtomicLoad transactions, Table A6.9 shows the encodings for the operations on the lower-order AWATOP[2:0] signals.

Table A6.9: Lower order AWATOP[2:0] encodings
<table><tr><td>AWATOP[2:0]</td><td>Operation</td><td>Description</td></tr><tr><td>0b000</td><td>ADD</td><td>Add</td></tr><tr><td>0b001</td><td>CLR</td><td>Bit clear</td></tr><tr><td>0b010</td><td>EOR</td><td>Exclusive OR</td></tr><tr><td>0b011</td><td>SET</td><td>Bit set</td></tr><tr><td>0b100</td><td>SMAX</td><td>Signed maximum</td></tr><tr><td>0b101</td><td>SMIN</td><td>Signed minimum</td></tr><tr><td>0b110</td><td>UMAX</td><td>Unsigned maximum</td></tr><tr><td>0b111</td><td>UMIN</td><td>Unsigned minimum</td></tr></table>

## A6.4.7 Transaction structure

For AtomicLoad, AtomicSwap, and AtomicCompare transactions, the transaction structure is as follows:

• The request is issued on the AW channel.

• The associated transaction data is sent on the W channel.

• The number of write data transfers required on the W channel is determined by the AWLEN signal.

• The relative timing of the Atomic transaction request and the Atomic transaction write data is not specified.

• The Subordinate returns the original data value using the R channel.

• The number of read data transfers is determined from both AWLEN and the AWATOP signals. For the AtomicCompare operation, if AWLEN indicates a transaction length greater than 1, then the number of read data transfers is half that specified by AWLEN.

• A Subordinate is permitted to wait for all write data before sending read data. A Manager must be able to send all write data without receiving any read data.

• A Subordinate is permitted to send all read data before accepting any write data. A Manager must be able to accept all read data without any write data being accepted.

• A single write response is returned on the B channel. The write response must be given by the Subordinate only after it has received all write data transfers and the result of the atomic transaction is observable.

The transfers involved in AtomicLoad, AtomicSwap, and AtomicCompare transactions are shown in Figure A6.3.

![](images/79b120a58b6d9a8c950d6604a503719186b0d197362949db36087a45165cd2a8.jpg)  
Figure A6.3: AtomicLoad, AtomicSwap, or AtomicCompare transaction

For AtomicStore transactions, the transaction structure is as follows:

• The request is issued on the AW channel.

• The associated transaction data is sent on the W channel.

• The number of write data transfers required on the W channel is determined by the AWLEN signal.

• The relative timing of the Atomic transaction request and the Atomic transaction write data is not specified.

• A single write response is returned on the B channel. The write response must be given only by the Subordinate after it has received all write data transfers and the result of the atomic transaction is observable.

The transfers involved in AtomicStore transactions are shown in Figure A6.4.

![](images/4567eb0a5fdf15553040b31f866050e8276b569e494b195386f575418317fca0.jpg)  
Figure A6.4: AtomicStore transaction

## A6.4.8 Response signaling

The write response to an Atomic transaction indicates that the transaction is visible to all required observers.

Atomic transactions that include a read response are visible to all required observers from the point of receiving the first item of read data.

A Manager is permitted to use either a read or write response as an indication that a transaction is visible to all required observers.

There is no concept of an error that is associated with the operation, such as overflow. An operation is fully specified for all input combinations.

For transactions, such as AtomicCompare, where there are multiple outcomes for the transaction, no indication is provided on the outcome of the transaction. To determine if a Compare and Swap instruction has updated the memory location, it is necessary to inspect the original data value that is returned as part of the transaction.

It is permitted to give an error response to an Atomic transaction when the transaction reaches a component that does not support Atomic transactions.

For AtomicLoad, AtomicSwap, and AtomicCompare transactions:

• A Subordinate must send the correct number of read data transfers, even if the write response is DECERR or SLVERR.

• A Manager might ignore the write response and only use the response that comes with read data.

• If there is an error with the write part of the transaction, it is highly recommended that a DECERR or SLVERR response is signaled on the read and write responses, so it is not missed by the Manager.

• If there is an error on the write but not on the read, a Manager ignoring the write response must read the location again to determine whether it was updated.

## A6.4.9 Atomic transaction dependencies

For AtomicLoad, AtomicSwap, and AtomicCompare transactions, Figure A6.5 shows the following Atomic transaction handshake signal dependencies:

• The Manager must not wait for the Subordinate to assert AWREADY or WREADY before asserting AWVALID or WVALID.

• The Subordinate can wait for AWVALID or WVALID, or both, before asserting AWREADY.

• The Subordinate can assert AWREADY before AWVALID or WVALID, or both, are asserted.

• The Subordinate can wait for AWVALID or WVALID, or both, before asserting WREADY.

• The Subordinate can assert WREADY before AWVALID or WVALID, or both, are asserted.

• The Subordinate must wait for AWVALID, AWREADY, WVALID, and WREADY to be asserted before asserting BVALID.

• The Subordinate must also wait for WLAST to be asserted before asserting BVALID because the write response BRESP, must be signaled only after the last data transfer of a write transaction.

• The Subordinate must not wait for the Manager to assert BREADY before asserting BVALID.

• The Manager can wait for BVALID before asserting BREADY.

• The Manager can assert BREADY before BVALID is asserted.

• The Subordinate must wait for both AWVALID and AWREADY to be asserted before it asserts RVALID to indicate that valid data is available.

• The Subordinate must not wait for the Manager to assert RREADY before asserting RVALID.

• The Manager can wait for RVALID to be asserted before it asserts RREADY.

• The Manager can assert RREADY before RVALID is asserted.

• The Manager must not wait for the Subordinate to assert RVALID before asserting WVALID.

• The Subordinate can wait for WVALID to be asserted, for all write data transfers, before it asserts RVALID.

• The Manager can assert WVALID before RVALID is asserted.

In the dependency diagram that Figure A6.5 shows:

• A single-headed arrow points to a signal that can be asserted before or after the signal at the start of the arrow.

• A double-headed arrow points to a signal that must be asserted only after assertion of the signal at the start of the arrow.

![](images/e6afbae34d9820f7e6b68599d72fa9806b079092400afddc45d422ef3c44c80e.jpg)  
Figure A6.5: Atomic transaction handshake dependencies

## A6.4.10 Support for Atomic transactions

The Atomic\_Transactions property is used to indicate whether a component supports Atomic transactions.

Table A6.10: Atomic\_Transactions property
<table><tr><td></td><td>Atomic_Transactions Default Description</td><td></td></tr><tr><td>True</td><td></td><td>Atomic Transactions are supported.</td></tr><tr><td>False</td><td>Y</td><td>Atomic Transactions are not supported.</td></tr></table>

In some implementations this will be a fixed interface attribute, other implementations might enable the design-time setting of the property.

If a Subordinate or interconnect component declares that it supports Atomic transactions, then it must support all operation types, sizes, and endianness.

## Manager support

A Manager component that supports Atomic transactions can also include a mechanism to suppress the generation of Atomic transactions to ensure compatibility in systems where Atomic transactions are not supported.

An optional BROADCASTATOMIC pin is specified. When present and deasserted, Atomic transactions are not issued by the Manager.

Table A6.11: BROADCASTATOMIC tie-off input
<table><tr><td>Name</td><td>Width</td><td>Default</td><td> Description</td></tr><tr><td>BROADCASTATOMIC</td><td>1</td><td>0b1</td><td>Manager tie-off input, used to control the issuing of</td></tr><tr><td></td><td></td><td></td><td>Atomic transactions from an interface.</td></tr><tr><td></td><td></td><td></td><td></td></tr></table>

## Subordinate support

It is optional for a Subordinate component to support Atomic transactions.

If a Subordinate component only supports Atomic transactions for particular memory types, or for particular address regions, then the Subordinate must give an appropriate error response for the Atomic transactions that i does not support.

## Interconnect support

It is optional for an interconnect to support Atomic transactions.

If an interconnect does not support Atomic transactions, all attached Manager components must be configured to not generate Atomic transactions.

Atomic transactions can be supported at any point within an interconnect that supports them, including passing Atomic transactions downstream to Subordinate components.

Atomic transactions are not required to be supported for every address location. If Atomic transactions are not supported for a given address location, then an appropriate error response can be given for the transaction. See A3.3 Transaction response.

For Device transactions, the Atomic transaction must be passed to the endpoint Subordinate. If the Subordinate is configured to indicate that it does not support Atomic transactions, then the interconnect must give an error response for the transaction. An Atomic transaction must not be passed to a component that does not support Atomic transactions.

For Cacheable transactions, the interconnect can either:

• Perform the atomic operation within the interconnect. This method requires that the interconnect performs the appropriate read, write, and snoop transactions to complete the operation.

• If the appropriate endpoint Subordinate is configured to indicate that it does support atomic operations, then the interconnect can pass the atomic operation to the Subordinate.

# Chapter A7 Request Opcodes

The request Opcode indicates the function of a request and how it must be processed by a Subordinate.

This chapter summarizes all Opcodes that are available with links in the tables to detailed descriptions of how they work.

It contains the following sections:

• A7.1 Opcode signaling

• A7.2 AWSNOOP encodings

• A7.3 ARSNOOP encodings

## A7.1 Opcode signaling

The request Opcode is communicated using the AWSNOOP and ARSNOOP signals.

Table A7.1: AxSNOOP signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWSNOOP</td><td>AWSNOOP_WIDTH</td><td>0x00 (WriteNoSnoop / WriteUniquePtl / Atomic / WriteExclusive /</td><td>Opcode for requests using the write channels.</td></tr><tr><td>ARSNOOP</td><td>ARSNOOP_WIDTH</td><td>WriteACT) 0x0 (ReadNoSnoop / ReadOnce / ReadExclusive / ReadACT)</td><td>Opcode for requests using the read channels.</td></tr></table>

WriteNoSnoop, WriteUniquePtl, ReadNoSnoop and ReadOnce are default Opcodes and are used for generic requests.

The AxSNOOP width properties are defined in Table A7.2.

Table A7.2: AxSNOOP width properties
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>AWSNOOP_WIDTH</td><td>0,4,5</td><td>4</td><td>Width of AWSNOOP in bits.</td></tr><tr><td>ARSNOOP_WIDTH</td><td>0,4</td><td>4</td><td>Width of ARSNOOP in bits.</td></tr></table>

If any of the following properties are not False, AWSNOOP\_WIDTH must be 5:

• WriteDeferrable\_Transaction

• UnstashTranslation\_Transaction

• InvalidateHint\_Transaction

If any of the following properties are not False, AWSNOOP\_WIDTH must be 4 or 5:

• Shareable\_Cache\_Support

• WriteNoSnoopFull\_Transaction

• CMO\_On\_Write

• WriteZero\_Transaction

• Cache\_Stash\_Transactions

• Untranslated\_Transactions

• Prefetch\_Transaction

If any of the following properties are not False, ARSNOOP\_WIDTH must be 4:

• Shareable\_Cache\_Support

• DeAllocation\_Transactions

• CMO\_On\_Read

• DVM\_Message\_Support

Any AxSNOOP bits not driven by an interface are assumed to be LOW.

A Manager that only uses Opcodes where AWSNOOP is LOW can set AWSNOOP\_WIDTH to 0 which omits the AWSNOOP output from its interface. An attached Subordinate must have its AWSNOOP input tied LOW.

A Manager that only uses Opcodes where ARSNOOP is LOW can set ARSNOOP\_WIDTH to 0 which omits the ARSNOOP output from its interface. An attached Subordinate must have its ARSNOOP input tied LOW.

## A7.2 AWSNOOP encodings

The encodings for AWSNOOP are shown in Table A7.3. Some Opcodes depend on the Domain of the request. The Enable column lists the property expression that determines whether a Manager interface is permitted to use the Opcode and a Subordinate interface supports it.

Unlisted combinations of AWSNOOP and AWDOMAIN are illegal.

Table A7.3: AWSNOOP encodings
<table><tr><td>AWSNOOP</td><td>AWDOMAIN1</td><td>Opcode</td><td>Enable</td><td>Description</td></tr><tr><td rowspan="5">0b00000</td><td>NSH, SYS</td><td>WriteNoSnoop</td><td>-</td><td>Write to a Non-shareable or System location.</td></tr><tr><td>SH</td><td>WriteUniquePtl</td><td>Shareable_Transactions</td><td>Write to a Shareable location.</td></tr><tr><td>NSH, SH, SYS</td><td>Atomic</td><td>Atomic_Transactions</td><td>Atomic transaction, indicated by nonzero AWATOP signal.</td></tr><tr><td>NSH, SYS</td><td>WriteExclusive</td><td>Exclusive_Accesses</td><td>Exclusive write access, indicated by AWLOCK asserted.</td></tr><tr><td>SYS</td><td>WriteACT</td><td>ACT_Support</td><td>ACT write access, indicated by AWACTV asserted.</td></tr><tr><td>0b00001</td><td>NSH, SYS</td><td>WriteNoSnoopFull</td><td>WriteNoSnoopFull Transaction or Shareable_Cache_Support</td><td>Cache line sized and Regular write to a Non-shareable location.</td></tr><tr><td></td><td>SH</td><td>WriteUniqueFull</td><td>Shareable_Transactions</td><td>Cache line sized and Regular write to a Shareable location.</td></tr><tr><td>0b00010 0b00011</td><td></td><td>RESERVED</td><td></td><td>Cache line sized and Regular write</td></tr><tr><td></td><td>SH</td><td>WriteBackFull</td><td>Shareable_Transactions and Shareable_Cache_Support</td><td>to a Shareable location. The line was held in a coherent cache and is Dirty.</td></tr><tr><td>0b00100</td><td></td><td>RESERVED</td><td></td><td>Cache line sized and Regular write</td></tr><tr><td>0b00101</td><td>SH</td><td>WriteEvictFull</td><td>Shareable_Transactions and Shareable_Cache_Support</td><td>to a Shareable location. The line was held in a coherent cache and is Clean.</td></tr><tr><td>0b00110</td><td>NSH, SH</td><td>CMO</td><td>CMO_On_Write</td><td>A data-less request which indicates that a cache maintenance operation must be performed. The specific operation is encoded on the AWCMO signal. Cache line sized and Regular.</td></tr><tr><td>0b00111</td><td>NSH, SH, SYS</td><td>WriteZero</td><td>WriteZero_Transaction</td><td>Cache line sized and Regular write, where the value of every byte is zero.</td></tr></table>

Continued on next page

Table A7.3 – Continued from previous page
<table><tr><td>AWSNOOP</td><td>AWDOMAIN1</td><td>Opcode</td><td>Enable</td><td>Description</td></tr><tr><td>0b01000</td><td>SH</td><td>WriteUniquePtlStash</td><td>Shareable Transactions and Cache_Stash_Transactions</td><td>Write to a Shareable location with an indication that the data should be allocated into a cache. Cache line sized or smaller.</td></tr><tr><td>0b01001</td><td>SH</td><td>WriteUniqueFullStash</td><td>Shareable_Transactions and Cache Stash Transactions</td><td>Cache line sized and Regular write to a Shareable location with an indication that the data should be allocated into a cache.</td></tr><tr><td>0b01010</td><td>NSH, SH</td><td>WritePtlCMO</td><td>Write_Plus_CMO</td><td>Write where any cached copies of the line must be cleaned and/or invalidated according to the AWCMO signal. Cache line sized</td></tr><tr><td>0b01011</td><td>NSH, SH</td><td>WriteFullCMO</td><td>Write_Plus_CMO</td><td>Cache line sized and Regular write where any cached copies of the line must be cleaned and/or invalidated according to the</td></tr><tr><td>0b01100</td><td>NSH, SH</td><td>StashOnceShared</td><td>Cache_Stash_Transactions</td><td>A data-less request which indicates that a cache line should be fetched into a cache. Other copies of the line are not required to be invalidated. Cache line sized</td></tr><tr><td>0b01101</td><td>NSH, SH</td><td>StashOnceUnique</td><td>Cache_Stash_Transactions</td><td>A data-less request which indicates that a cache line should be fetched into a cache. It is recommended that all other copies are invalidated. Cache line sized</td></tr><tr><td>0b01110</td><td>NSH, SH, SYS</td><td>StashTranslation</td><td>Untranslated Transactions and Cache_Stash_Transactions</td><td>A data-less request which indicates that a translation should be cached in an MMU.</td></tr><tr><td>0b01111</td><td>NSH, SH</td><td>Prefetch</td><td>Prefetch_Transaction</td><td>A data-less request which indicates that a Manager might read the addressed cache line at a later time. Cache line sized and Regular.</td></tr><tr><td>0b10000</td><td>SYS</td><td>WriteDeferrable</td><td>WriteDeferrable_Transaction</td><td>A 64-byte atomic write where the Subordinate can give a DEFER or UNSUPPORTED response.</td></tr><tr><td>0b10001</td><td>NSH, SH, SYS</td><td>UnstashTranslation</td><td>UnstashTranslation_Transaction</td><td>A data-less request which is a hint that a translation is not likely to be used again.</td></tr></table>

Continued on next page

Table A7.3 – Continued from previous page
<table><tr><td>AWSNOOP</td><td>AWDOMAIN1</td><td>Opcode</td><td>Enable</td><td>Description</td></tr><tr><td>0b10010</td><td>NSH, SH</td><td>InvalidateHint</td><td>InvalidateHint_Transaction</td><td>A data-less request which indicates that a cache line is no longer required and can be invalidated. A write-back is permitted but not required. Cache</td></tr><tr><td>0b10011 to 0b11111</td><td></td><td>RESERVED</td><td></td><td>line sized and Regular.</td></tr></table>

<sup>1</sup> NSH is Non-shareable (0b00), SH is Shareable (0b01 or 0b10), SYS is System (0b11).

## A7.3 ARSNOOP encodings

The encodings for ARSNOOP are shown in Table A7.4. Some Opcodes depend on the Domain of the request. The Enable column lists the property expression that determines whether a Manager interface is permitted to use the Opcode and a Subordinate interface supports it.

Unlisted combinations of ARSNOOP and ARDOMAIN are illegal.

Table A7.4: ARSNOOP encodings
<table><tr><td>ARSNOOP</td><td>ARDOMAIN1</td><td>Opcode</td><td>Enable</td><td>Description</td></tr><tr><td rowspan="4">0b0000</td><td>NSH, SYS</td><td>ReadNoSnoop</td><td></td><td>Read from a Non-shareable or System location.</td></tr><tr><td>SH</td><td>ReadOnce</td><td>Shareable_Transactions</td><td>Read from a Shareable location which the Manager will not cache.</td></tr><tr><td>NSH, SYS</td><td>ReadExclusive</td><td>Exclusive_Accesses</td><td>Exclusive read access, indicated by ARLOCK asserted.</td></tr><tr><td>SYS</td><td>ReadACT</td><td>ACT_Support</td><td>ACT read access, indicated by ARACTV asserted.</td></tr><tr><td>0b0001</td><td>SH</td><td>ReadShared</td><td>Shareable_Transactions and Shareable_Cache_Support</td><td>Cache line sized and Regular read from a Shareable location which the Manager might cache. Data can be Dirty</td></tr><tr><td>0b0010</td><td>SH</td><td>ReadClean</td><td>Shareable_Transactions and Shareable_Cache_Support</td><td>Cache line sized and Regular read from Shareable location which the Manager might cache. Data must not be Dirty.</td></tr><tr><td>0b0011</td><td></td><td>RESERVED</td><td></td><td>Read from a Shareable location</td></tr><tr><td>0b0100</td><td>SH</td><td>ReadOnceCleanInvalid</td><td>Shareable_Transactions and DeAllocation_Transactions</td><td>which the Manager will not cache. Cached copies are recommended to be cleaned and invalidated. Cache line sized or smaller.</td></tr><tr><td>0b0101</td><td>SH</td><td>ReadOnceMakeInvalid</td><td>Shareable_Transactions and DeAllocation_Transactions</td><td>Read from a Shareable location which the Manager will not cache. Cached copies are recommended to be invalidated without a write-back. Cache line</td></tr><tr><td>0b0110</td><td></td><td>RESERVED</td><td></td><td>sized or smaller.</td></tr><tr><td>0b0111</td><td></td><td>RESERVED</td><td></td><td></td></tr><tr><td>0b1000</td><td>NSH, SH</td><td>CleanShared</td><td>CMO_On_Read</td><td>A request to clean all copies of a cache line. Cache line sized and Regular.</td></tr></table>

Continued on next page

Chapter A7. Request Opcodes A7.3. ARSNOOP encodings  
Table A7.4 – Continued from previous page
<table><tr><td>ARSNOOP</td><td>ARDOMAIN1</td><td>Opcode</td><td>Enable</td><td>Description</td></tr><tr><td>0b1001</td><td>NSH, SH</td><td>CleanInvalid</td><td>CMO_On_Read</td><td>A request to clean and invalidate all copies of a cache line. Cache line sized and Regular.</td></tr><tr><td>0b1010</td><td>NSH, SH</td><td>CleanSharedPersist</td><td>CMO On Read and Persist CMO</td><td>A request to clean all copies of a cache line. Cleaned data must pass the Point of Persistence or Point of Deep Persistence. Cache line sized and Regular.</td></tr><tr><td>0b1011</td><td></td><td>RESERVED</td><td></td><td></td></tr><tr><td>0b1100</td><td></td><td>RESERVED</td><td></td><td></td></tr><tr><td>0b1101</td><td>NSH, SH</td><td>MakeInvalid</td><td>CMO_On_Read</td><td>A request to clean and invalidate all copies of a cache line. Dirty data is not required to be written to memory. Cache line sized</td></tr><tr><td>0b1110</td><td>SH</td><td>DVM Complete</td><td>DVM_Message_Support</td><td>and Regular. Indicates completion of a DVM synchronization message.</td></tr><tr><td>0b1111</td><td></td><td>RESERVED</td><td></td><td></td></tr></table>

<sup>1</sup> NSH is Non-shareable (0b00), SH is Shareable (0b01 or 0b10), SYS is System (0b11).

## Chapter A8 Caches

This chapter describes caching in the AXI protocol.

It contains the following sections:

• A8.1 Caching in AXI

• A8.2 Cache line size

• A8.3 Cache coherency and Domains

• A8.4 I/O coherency

• A8.5 Caching Shareable lines

• A8.6 Prefetch transaction

• A8.7 Cache Stashing

• A8.8 Deallocating read transactions

• A8.9 Invalidate hint

## A8.1 Caching in AXI

In this specification, the term cache is used for any storage structure, including caches, buffers, or other intermediate storage elements. Data can be cached at various points in a system. An example topology is shown in Figure A8.1. In the example, there is a system cache which is visible to all agents, local Shareable caches which are visible to all coherent agents and local Non-shareable caches which are visible to a single agent.

Fully coherent agents use hardware coherency with data snooping to keep their caches coherent. These will typically use an AMBA CHI interface [5].

I/O coherent agents can share data with fully coherent agents but any data that is cached locally to them must be manually maintained to ensure coherency.

Non-coherent agents must use manual cache maintenance on any data that is shared with other agents and cached locally.

![](images/42703198b09faa1221b39739c7bc32185c80c2323a37a686e05d27b960ed251e.jpg)  
Figure A8.1: Example system topology showing possible cache locations and type

## A8.2 Cache line size

A cache line is defined as a cached copy of sequentially byte addressed memory locations, with the first address aligned to the total size of the cache line. A system which employs cache sharing must have a common cache line size. Some transactions only operate on entire cache lines and must be cache line sized.

The cache line size is fixed at design time and defined using the Cache\_Line\_Size property.

<table><tr><td>Name Values</td><td>Default</td><td>Description</td></tr><tr><td>Cache_Line_Size</td><td>16, 32, 64, 128, 256, 512, 1024, 2048 64</td><td>Cache line size in bytes.</td></tr></table>

For any interfaces carrying cache line sized transactions, the data width must be wide enough to transport a cache line using 16 transfers or fewer.

To be compatible with AMBA CHI, cache line size must be 64 bytes.

Opcodes where the transaction must be cache line sized and Regular are shown in Table A8.2. For more information on Regular transactions, see A3.1.8 Regular transactions.

Table A8.2: Opcodes which must be cache line sized and Regular
<table><tr><td>Transactions on the read channels</td><td>Transactions on the write channels</td></tr><tr><td>ReadShared</td><td>WriteNoSnoopFull</td></tr><tr><td>ReadClean</td><td>WriteUniqueFull</td></tr><tr><td>CleanShared</td><td>WriteBackFull</td></tr><tr><td>CleanInvalid</td><td>WriteEvictFull</td></tr><tr><td>MakeInvalid</td><td>CMO</td></tr><tr><td>CleanSharedPersist</td><td>WriteZero</td></tr><tr><td>ReadNoSnoop with MTE Fetch</td><td>WriteUniqueFullStash</td></tr><tr><td></td><td>WriteFullCMO</td></tr><tr><td></td><td>StashOnceShared</td></tr><tr><td></td><td>StashOnceUnique</td></tr><tr><td></td><td>Prefetch</td></tr><tr><td></td><td>InvalidateHint</td></tr></table>

Cache line sized transactions have the following constraints:

• Size x Length must be equal to the cache line size.

• Transactions with write data must have all byte strobes asserted within the cache line container.

## A8.3 Cache coherency and Domains

When multiple Managers share data, writes from those Managers must be coherent. This means writes to the same address location by two Managers are observable in the same order by all participating Managers.

If a system contains caches, measures must be taken to ensure that cached values do not become stale.

In AMBA, this can be achieved in three ways:

• Using Non-cacheable transactions.

• Software coherency with manual cache maintenance.

• Hardware coherency with snooping and automatic cache maintenance.

AXI supports these by attributing a Domain to every address location, this can be System, Non-shareable or Shareable. There must be a consistent definition of:

• Which address locations are in each Domain.

• Which Domain an address location is attributed.

## A8.3.1 System Domain

Address locations in the System Domain must be visible to all Managers that are able to access them. This is achieved by ensuring that all System Domain requests are Non-cacheable and therefore not stored in any local caches. Using the System Domain makes coherency simple but is generally not high performance.

Requests to Device type memory are required to use the System Domain.

## A8.3.2 Non-shareable Domain

Address locations in the Non-shareable Domain are not required to be visible to other Managers. Transactions to Non-shareable locations do not need to trigger hardware coherency mechanisms to ensure visibility.

If Non-shareable data is to be shared between Managers, then transactions known as Cache Maintenance Operations (CMOs) must be issued to clean and invalidate the data from any local caches before it is read. See Chapter A9 Cache maintenance for more details.

Data sharing using CMOs is known as software coherency and can be an efficient approach if the sharing behavior between Managers is known. For example, if there are predictable data sets that are written by one agent then read by another. The main disadvantage of this approach is that it relies on software being correct. Coherency bugs in software can be easy to introduce and difficult to debug.

To avoid a loss of coherency, there are some rules when caching Non-shareable lines:

• The eviction and write-back of Clean Non-shareable data is not permitted. This is to avoid a Clean line from overwriting a Dirty line in a downstream cache that was written by another Manager.

• The passing of Dirty data on a read of a Non-shareable line from one cache to another is not permitted. The line must be passed as Clean and responsibility for writing back the line remains with the downstream cache. This avoids a subsequent write-back of the line from overwriting a later update from another Manager.

## A8.3.3 Shareable Domain

Address locations in the Shareable Domain must be visible to all other Managers that also have those locations marked as Shareable. Requests with the Shareable attribute must snoop local caches and lookup in caches that might contain Shareable data from other Managers.

There are two reasons why an AXI component may need to support the Shareable Domain: to enable I/O coherency and to support the movement of Shareable cache lines between upstream and downstream caches. These cases are covered in A8.4 I/O coherency and A8.5 Caching Shareable lines.

Requests in the Shareable domain can use a Burst type of INCR or WRAP, not FIXED.

## A8.3.4 Domain signaling

Domain signaling is optional, if an interface does not have Domain signaling then Non-cacheable requests are assumed to be in the System Domain and Cacheable requests are assumed to be in the Non-shareable Domain.

If a component is required to support the Shareable Domain, it must include the Domain signaling.

The Shareable\_Transactions property is used to describe whether an interface supports the Shareable Domain and therefore has Domain signaling.

Table A8.3: Shareable\_Transactions property
<table><tr><td>Shareable_Transactions Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>Shareable domain supported, AxDOMAIN signals are on the interface.</td></tr><tr><td>False</td><td>Y</td><td>Shareable domain not supported, AxDOMAIN signals are not on the interface.</td></tr></table>

When Shareable\_Transactions is True, the following signals are included on the interface.

Table A8.4: AxDOMAIN signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWDOMAIN, ARDOMAIN</td><td>2</td><td></td><td>Shareability domain of a request.</td></tr></table>

Shareable\_Transactions is encoded on the AxDOMAIN signals as shown in Table A8.5.

Table A8.5: AxDOMAIN encodings
<table><tr><td>AxDOMAIN</td><td>Label</td><td>Meaning</td></tr><tr><td>0b00</td><td>Non-shareable</td><td>Non-shareable domain</td></tr><tr><td>0b01</td><td>Shareable</td><td>Shareable domain</td></tr><tr><td>0b10</td><td>Shareable</td><td>Shareable domain</td></tr><tr><td>0b11</td><td>System</td><td>System domain</td></tr></table>

If AxDOMAIN signals are not present:

• Non-cacheable requests are assumed to be in the System domain.

• Cacheable requests are assumed to be in the Shareable domain.

In previous versions of this specification, AxDOMAIN values of 0b01 and 0b10 indicated Inner Shareable and Outer Shareable respectively. In this version, it is recommended that 0b10 is used to indicate the Shareable domain.

Guidance for connecting Manager and Subordinate interfaces with different values of Shareable\_Transactions is shown in Table A8.6.

Table A8.6: Shareable\_Transactions interoperability
<table><tr><td></td><td>Subordinate: False</td><td>Subordinate: True</td></tr><tr><td>Manager: False</td><td>Compatible.</td><td>Compatible if logic is added to generate default AxDOMAIN values from AxCACHE.</td></tr><tr><td>Manager: True</td><td>Compatible. AxDOMAIN outputs are unconnected.</td><td>Compatible.</td></tr></table>

## A8.3.5 Domain consistency

An address location can be marked as Shareable for one agent and Non-shareable for another. To avoid a loss of coherency, data cached as Non-shareable must be made visible using CMOs before being accessed by an agent that has the location marked as Shareable.

## A8.3.6 Domains and memory types

The combination of Domain and memory type determines which caches must be accessed to complete the transactions.

Legal combinations of memory type and Domain are shown in Table A8.7. The table also indicates which caches must be accessed when processing a request.

• Peer caches are those which are accessed using snoop requests, this requires a coherent protocol such as AMBA CHI [5].

• Inline caches are those which requests pass through while progressing towards memory.

Table A8.7: Legal combinations of memory type and Domain
<table><tr><td>Memory type</td><td>Domain</td><td>Caches accessed</td></tr><tr><td>Device (AxCACHE[3:1] == 0b000)</td><td>System</td><td>None</td></tr><tr><td rowspan="3">Normal Non-cacheable (AxCACHE[3:1] == 0b001)</td><td>Non-shareable</td><td>None</td></tr><tr><td>Shareable</td><td>Peer caches</td></tr><tr><td>System (recommended)</td><td>None</td></tr><tr><td rowspan="2">Normal Cacheable (AxCACHE[3:2] != 0b00)</td><td>Non-shareable</td><td>Inline caches</td></tr><tr><td>Shareable</td><td>Inline and peer caches</td></tr></table>

Note that Normal Non-cacheable Shareable is permitted but not expected. Some implementations might not look up in peer caches for Non-cacheable accesses.

## A8.4 I/O coherency

An I/O coherent Manager can read and write data in the Sharable Domain through use of a coherent interconnect but it cannot be snooped, so it must not cache Shareable data. AXI does not support data snooping, so the coherent interconnect will typically be based on the AMBA CHI protocol [5] with AXI interfaces for connecting I/O coherent Managers.

![](images/403ef626bbb3b2fa4c3a288b574f0db58e762680c3d5c328fd30bd86759e18bf.jpg)  
Figure A8.2: Example use of I/O coherency

When an I/O coherent Manager issues a Shareable read request, the coherent interconnect tries to find the data by snooping appropriate coherent caches and checking Shareable lines within its caches. If the data cannot be found, a request is sent downstream towards memory. When the data is returned, it must not be cached by the I/O coherent Manager because the data can become stale.

When an I/O coherent Manager issues a Shareable write request (WriteUniquePtl or WriteUniqueFull), the coherent interconnect issues clean and invalidation requests to the coherent caches to ensure that there are no local copies. It then writes the data into a cache or towards memory. For a partial cache line write, any Dirty data found in coherent caches can be merged with the write.

The Shareable\_Cache\_Support property must be False for an I/O coherent interface.

## A8.5 Caching Shareable lines

An AXI-based cache that is downstream of a coherent interconnect has the option to store Shareable lines in addition to Non-shareable cache lines. This has the advantages that:

• Clean evictions of Shareable lines can be cached but must not be written back to memory.

• Dirty data from Shareable lines can be passed to upstream Shareable caches.

To enable this, additional Opcodes and responses are required. The cache must also track which lines are Shareable if it also stores lines from the Non-shareable Domain. In this case, a valid cache line can have one of four states:

• Clean

• Dirty

• Shareable Clean

• Shareable Dirty

The rules regarding which Opcodes can hit which cache lines are shown in Table A8.8.

Table A8.8: Rules for caching Shareable lines
<table><tr><td rowspan="2">Opcode</td><td rowspan="2">Domain</td><td colspan="4">Cache state</td></tr><tr><td>Clean</td><td>Dirty</td><td>Shareable Clean</td><td>Shareable Dirty</td></tr><tr><td rowspan="2">Read*</td><td>Non-shareable</td><td>Permitted to hit</td><td>Permitted to hit</td><td>Must not hit</td><td>Permitted to hit1</td></tr><tr><td>Shareable</td><td>Permitted to hit</td><td>Must hit</td><td>Permitted to hit</td><td>Must hit²</td></tr><tr><td rowspan="2">Write*</td><td>Non-shareable</td><td>Must hit</td><td>Must hit</td><td>Must not hit</td><td>Permitted to hit1</td></tr><tr><td>Shareable</td><td>Must hit</td><td>Must hit</td><td>Must hit</td><td>Must hit</td></tr><tr><td rowspan="2">CleanShared*</td><td>Non-shareable</td><td>Permitted to hit</td><td>Must hit</td><td>Permitted to hit</td><td>Permitted to hit³</td></tr><tr><td>Shareable</td><td>Permitted to hit</td><td>Must hit</td><td>Permitted to hit</td><td>Must hit</td></tr><tr><td rowspan="2">CleanInvalid* / MakeInvalid</td><td>Non-shareable</td><td>Must hit</td><td>Must hit</td><td>Permitted to hit³</td><td>Permitted to hit3</td></tr><tr><td>Shareable</td><td>Must hit</td><td>Must hit</td><td>Must hit</td><td>Must hit</td></tr><tr><td rowspan="2">InvalidateHint / Prefetch</td><td>Non-shareable</td><td>Permitted to hit</td><td>Permitted to hit</td><td>Permitted to hit</td><td>Permitted to hit</td></tr><tr><td>Shareable</td><td>Permitted to hit</td><td>Permitted to hit</td><td>Permitted to hit</td><td>Permitted to hit</td></tr><tr><td rowspan="2">StashOnce*</td><td>Non-shareable</td><td>Permitted to hit</td><td>Permitted to hit</td><td>Must not hit</td><td>Permitted to hit</td></tr><tr><td>Shareable</td><td>Permitted to hit</td><td>Permitted to hit</td><td>Permitted to hit</td><td>Permitted to hit</td></tr></table>

∗ Includes all variants of the Opcode.  
<sup>1</sup> The line must no longer be marked as Shareable.

<sup>2</sup> Dirty data can be provided upstream if the request was ReadShared.

<sup>3</sup> Must hit if RME\_Support is True.

If Outer Cacheable mode is used by attached CPUs, transactions marked in the page tables as Inner Non-cacheable, Outer Cacheable will not use shareable read and write transactions and it is not expected that cache lines will be allocated as Shareable.

## A8.5.1 Opcodes to support reading and writing full cache lines

The following Opcodes can be used to read and write full cache lines of data.

Transactions using these Opcodes must be Modifiable, cache line sized and Regular. See A4.2.2 Modifiable transactions, A8.2 Cache line size and A3.1.8 Regular transactions.

For write transactions all write strobes must be asserted.

## ReadClean

A full cache line read from a Shareable location, where the data is likely to be allocated in an upstream cache. The read data must be Clean.

This Opcode can be used if the Shareable\_Cache\_Support and Shareable\_Transactions properties are both True.

## ReadShared

A full cache line read from a Shareable location, where the data is likely to be allocated in an upstream cache. The read data can be Clean or Dirty. If the data is Dirty, the line must be allocated upstream, and the response for all transfers of read data must be OKAYDIRTY instead of OKAY.

This Opcode can be used if the Shareable\_Cache\_Support and Shareable\_Transactions properties are both True.

## WriteNoSnoopFull

A Non-shareable write of a full cache line where the data is Dirty and not allocated upstream.

An upstream cache can issue a WriteNoSnoopFull transaction when it evicts a Non-shareable Dirty cache line or when streaming write data which is cache line sized. If a downstream cache receives a WriteNoSnoopFull request, it can allocate the line knowing that the line is not allocated upstream.

This Opcode can be used if the WriteNoSnoopFull\_Transaction or Shareable\_Cache\_Support property is True.

Table A8.9: WriteNoSnoopFull\_Transaction property
<table><tr><td>WriteNoSnoopFull_Transaction Default</td><td></td><td>Description</td></tr><tr><td>True</td><td></td><td>WriteNoSnoopFull is supported.</td></tr><tr><td>False</td><td>Y</td><td>WriteNoSnoopFull is not supported unless Shareable_Cache_Support is True.</td></tr></table>

## WriteUniqueFull

A Shareable write of a full cache line where the data is Dirty but was not allocated upstream. This transaction is used by an I/O coherent Manager to write to a cache line that might be stored in a cache within the coherent domain. A system cache can allocate the line as Shareable Dirty.

This Opcode can be used if the Shareable\_Transactions property is True.

## WriteBackFull

A WriteBackFull transaction can be used when a Shareable Dirty line is evicted from a coherent cache. This transaction enables a system cache to allocate the line as Shareable Dirty.

This Opcode can be used if the Shareable\_Cache\_Support and Shareable\_Transactions properties are both True.

## WriteEvictFull

A WriteEvictFull transaction can be used when a Shareable Clean line is evicted from a coherent cache. This transaction enables a system cache to allocate the line as Shareable Clean.

A Shareable Clean line must not be exposed to any agents outside of the Shareable Domain because the line might become stale within caches in the Shareable Domain. For the same reason, data from a WriteEvictFull must not update memory.

This Opcode can be used if the Shareable\_Cache\_Support and Shareable\_Transactions properties are both True.

## A8.5.2 Configuration of Shareable cache support

The Shareable\_Cache\_Support property is used to indicate whether an interface supports the additional transaction Opcodes required for the storage of coherent cache lines.

Table A8.10: Shareable\_Cache\_Support property
<table><tr><td>Shareable_Cache_Support Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>Additional Opcodes for Shareable cache lines are supported.</td></tr><tr><td>False</td><td>Y</td><td>Additional Opcodes for Shareable cache lines are not supported.</td></tr></table>

The compatibility between Manager and Subordinate interfaces according to the values of the Shareable\_Cache\_Support property is shown in Table A8.11.

Table A8.11: Shareable\_Cache\_Support compatibility
<table><tr><td>Shareable_Cache_Support</td><td>Subordinate: False</td><td>Subordinate: True</td></tr><tr><td>Manager: False</td><td>Compatible.</td><td>Compatible.</td></tr><tr><td rowspan="2">Manager: True</td><td>Incompatible.</td><td>Compatible.</td></tr><tr><td>Alternative Opcodes must be used.</td><td></td></tr></table>

Shareable requests can also be controlled at reset-time using an optional Manager input signal, BROADCASTSHAREABLE.

Table A8.12: BROADCASTSHAREABLE signal
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>BROADCASTSHAREABLE</td><td>1</td><td>0b1</td><td>Manager tie-off input, used to control the issuing of</td></tr><tr><td></td><td></td><td></td><td>Shareable transactions from an interface.</td></tr><tr><td></td><td></td><td></td><td></td></tr></table>

When BROADCASTSHAREABLE is present and deasserted, all transactions are converted to Non-shareable equivalents before they are sent, as shown in Table A8.13.

Table A8.13: Opcode alternatives
<table><tr><td>Opcode</td><td>BROADCASTSHAREABLE is LOW</td></tr><tr><td>WriteUniquePtl</td><td>WriteNoSnoop</td></tr><tr><td>WriteUniqueFull</td><td>WriteNoSnoop or WriteNoSnoopFull</td></tr><tr><td>WriteBackFull</td><td>WriteNoSnoop or WriteNoSnoopFull</td></tr><tr><td>WriteEvictFull</td><td>- (request must be dropped)</td></tr><tr><td>CMO (Shareable)</td><td>CMO (Non-shareable)</td></tr><tr><td>WriteUniquePtlStash</td><td>WriteNoSnoop</td></tr><tr><td>WriteUniqueFullStash</td><td>WriteNoSnoop or WriteNoSnoopFull</td></tr><tr><td>WritePtlCMO (Shareable)</td><td>WritePtlCMO (Non-shareable)</td></tr><tr><td>StashOnceShared (Shareable)</td><td>StashOnceShared (Non-shareable)</td></tr><tr><td>StashOnceUnique (Shareable)</td><td>StashOnceUnique (Non-shareable)</td></tr><tr><td>Prefetch (Shareable)</td><td>Prefetch (Non-shareable)</td></tr><tr><td>ReadOnce</td><td>ReadNoSnoop</td></tr><tr><td>ReadShared</td><td>ReadNoSnoop</td></tr><tr><td>ReadClean</td><td>ReadNoSnoop</td></tr><tr><td>ReadOnceCleanInvalid</td><td>ReadNoSnoop</td></tr><tr><td>ReadOnceMakeInvalid</td><td>ReadNoSnoop</td></tr></table>

## A8.6 Prefetch transaction

When a Manager has indication that it might need data for an address but does not want to commit to reading it yet, it can send a Prefetch request to the system that it might be advantageous to prepare the location for reading. This request to the system can cause the allocation of data into a downstream cache or from off-chip memory before the Manager makes the actual read request.

The Prefetch request is not required to be ordered with respect to other requests such as CMOs, therefore a Prefetch must not be used to signal that a line can be fetched into a managed or visible cache.

The PREFETCHED response to a read request indicates that the transaction has hit upon prefetched data. The Manager can use this as part of a heuristic to determine if it continues issuing Prefetch requests.

In AMBA CHI [5], the equivalent of a Prefetch request is PrefetchTgt which can be issued alongside a coherent request to the same address. The PrefetchTgt can bypass any coherency checks and cause the memory controller to prefetch the data in case the coherent request does not find the data in any shared caches. If the memory controller uses an AXI interface, the CHI PrefetchTgt request can be converted to an AXI Prefetch.

## A8.6.1 Rules for the prefetch transaction

A Prefetch is a data-less transaction, the rules are:

• The Prefetch transaction consists of a request on the AW channel and a single response transfer on the B channel, there is no data transfer.

• A Prefetch request is signaled using the AWSNOOP Opcode of 0b01111.

• A Prefetch request must be cache line sized with the following constraints:

– The transaction is Regular, see A3.1.8 Regular transactions.

– AWCACHE[1] is asserted, that is a Normal transaction.

– AWDOMAIN is Non-shareable or Shareable.

– AWLOCK is deasserted, not exclusive access.

• The ID value must be unique-in-flight, which means:

– A Prefetch request can only be issued if there are no outstanding write transactions using the same AWID.

– The Manager must not issue a request on the write channel with the same AWID as an outstanding Prefetch request.

– If present on the interface, AWIDUNQ must be asserted for Prefetch transactions.

• The Manager may or may not follow a Prefetch request with a non-Prefetch request to the same address.

• A Subordinate interface at any level can chose to propagate or respond to a Prefetch request.

• It is permitted to respond to a Prefetch request with OKAY, DECERR, SLVERR, or TRANSFAULT (only if AWMMUFLOW is PRI).

• An OKAY response can be sent irrespective of whether the Subordinate acts on the Prefetch request.

The Prefetch\_Transaction property is used to indicate whether a component supports the Prefetch Opcode as shown in Table A8.14.

Table A8.14: Prefetch\_Transaction property
<table><tr><td>Prefetch_Transaction</td><td>Default Description</td><td></td></tr><tr><td>True</td><td></td><td>Prefetch is supported.</td></tr><tr><td>False</td><td>Y</td><td>Prefetch is not supported.</td></tr></table>

## A8.6.2 Response for prefetched data

If a read request hits on data which has been prepared due to a previous Prefetch request, the Subordinate may return a PREFETCHED response. This can be used by the Manager to determine the success rate of its Prefetch requests.

The PREFETCHED response has the following rules and recommendations:

• The PREFETCHED response is signaled using RRESP encoding of 0b100.

• When Prefetch\_Transaction is True, RRESP\_WIDTH must be 3 to enable the signaling of the PREFETCHED response.

• PREFETCHED indicates that read data is valid and has come from a prefetched source.

• PREFETCHED can be used for a response to the following Opcodes:

– ReadNoSnoop

– ReadOnce

– ReadClean

– ReadShared

– ReadOnceCleanInvalid

– ReadOnceMakeInvalid

• A PREFETCHED response cannot be sent for an exclusive read.

• It is recommended that within a cache line, the PREFETCHED response is used for all data transfers or no data transfers. If a transaction spans cache lines, there can be a mixture of PREFETCHED and other responses for each cache line accessed.

• A PREFETCHED response can only be sent if the Prefetch\_Transaction property is True for the interface.

• A PREFETCHED response can be sent to a Manager even if the Manager has not sent a Prefetch request to that location. For example, if a Manager happens to read data which was prefetched by another Manager.

## A8.7 Cache Stashing

Cache stashing enables one component to indicate that data should be placed in another cache in the system. This technique can be used to ensure that data is located close to its point of use, potentially improving the performance of the overall system. The AXI protocol supports cache stashing requests with or without a stash target identifier.

Cache stashing is a hint. A cache, or system component can choose to ignore the stash part of a request.

I/O coherent AXI Managers can request that data is stashed in fully coherent Managers with AMBA CHI interfaces [5].

## A8.7.1 Stash transaction Opcodes

There are four Opcodes that can be used for cache stashing.

## WriteUniquePtlStash

Write to a Shareable location with an indication that the data should be allocated into a cache. Any number of bytes within the cache line can be written, including all bytes or zero bytes.

## WriteUniqueFullStash

Write a full cache line of data to a Shareable location with an indication that the data should be allocated into a cache. The transaction must be cache line sized and Regular. All write strobes must be asserted.

## StashOnceShared

A data-less transaction which indicates that a cache line should be fetched into a particular cache. Other copies of the line are not required to be invalidated.

## StashOnceUnique

A data-less transaction which indicates that a cache line should be fetched into a particular cache. It is recommended that all other copies are invalidated.

A StashOnceUnique transaction can cause the invalidation of a cached copy of a cache line and care must be taken to ensure that such transactions do not interfere with exclusive access sequences.

For an interface that supports the Untranslated Transactions feature, an extra stash transaction is supported. The StashTranslation transaction is used to indicate to a System Memory Management Unit (SMMU) that a translation should be obtained for the address that is supplied with the StashTranslation transaction. See A13.9 StashTranslation Opcode.

## A8.7.2 Stash transaction signaling

Stash requests are signaled on the write request channel and have a single response transfer on the write response channel. Write with stash transactions also include write data.

A stash request has constraints on Domain, Size, and Length shown in Table A8.15. Cache stash transactions are not permitted to cross a cache line boundary.

Table A8.15: Domain, Size, and Length constraints for stash requests
<table><tr><td>Opcode</td><td>AWSNOOP</td><td>Domain</td><td>Size, Length</td></tr><tr><td>WriteUniquePtlStash</td><td>0b1000</td><td>Shareable</td><td>Cache size or smaller</td></tr><tr><td>WriteUniqueFullStash</td><td>0b1001</td><td>Shareable</td><td>Cache line sized and Regular</td></tr><tr><td>StashOnceShared</td><td>0b1100</td><td>Non-shareable, Shareable</td><td>Cache line sized and Regular</td></tr><tr><td>StashOnceUnique</td><td>0b1101</td><td>Non-shareable, Shareable</td><td>Cache line sized and Regular</td></tr></table>

The following constraints also apply to all stash request Opcodes:

• AWCACHE[1] is 0b1 (Modifiable)

• AWLOCK is 0b0 (not exclusive access)

• AWTAGOP is 0b00 (Invalid)

• AWATOP is 0b000000 (Non-atomic operation)

## A8.7.3 Stash request Domain

The Domain of a stash request determines which caches are checked for the cache line and how the line should be fetched and stored.

A stash request to a Shareable location implies that the line can be stored in a peer or inline cache. If the stash request causes a cache to issue a downstream request, it should be Shareable if possible. Writes with stash must always be to a Shareable location.

A stash request to a Non-shareable location implies that the line can be stored in an inline cache. If the stash request causes a cache to issue a downstream request, it must be Non-shareable. StashOnceShared and StashOnceUnique Opcodes can be to Shareable or Non-shareable locations.

## A8.7.4 Stash target identifiers

A stash request can optionally include target identifiers to indicate a specific cache that is preferred for the data to be stored. This specification does not define the precise details of this identification mechanism. It is expected that any agent that is performing a stash operation knows the identifier to use for a given stash transaction.

This specification defines two levels of identification:

• A Node ID (NID) to identify the physical interface that the cache stash should be sent to.

• A Logical Processor ID (LPID) to identify a functional unit that is associated with that physical interface. For example, a stash transaction can specify a processor cluster interface and specific cache within that cluster. The signals used to indicate stash targets are shown in Table A8.16.

Table A8.16: Signals used to indicate stash targets
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWSTASHNID</td><td>11</td><td>0x000</td><td>Node Identifier of the target for a stash operation.</td></tr><tr><td>AWSTASHNIDEN</td><td>1</td><td>0b0</td><td>HIGH to indicate that the AWSTASHNID signal is valid.</td></tr><tr><td>AWSTASHLPID</td><td>5</td><td>0x00</td><td>Logical Processor Identifier within the target for a stash operation.</td></tr><tr><td>AWSTASHLPIDEN</td><td>1</td><td>0b0</td><td>HIGH to indicate that the AWSTASHLPID signal is valid.</td></tr></table>

The NID and LPID signals are optional on an interface, controlled using the STASHNID\_Present and STASHLPID\_Present properties, respectively.

Table A8.17: STASHNID\_Present property
<table><tr><td>STASHNID_Present Default</td><td>Description</td><td></td></tr><tr><td>True</td><td></td><td>AWSTASHNID and AWSTASHNIDEN are present.</td></tr><tr><td>False</td><td>Y</td><td>AWSTASHNID and AWSTASHNIDEN are not present.</td></tr></table>

Table A8.18: STASHLPID\_Present property
<table><tr><td></td><td>STASHLPID_Present Default Description</td><td></td></tr><tr><td>True</td><td></td><td>AWSTASHLPID and AWSTASHLPIDEN are present.</td></tr><tr><td>False</td><td>Y</td><td>AWSTASHLPID and AWSTASHLPIDEN are not present.</td></tr></table>

Each stash target identifier has an enable signal so NID and LPID can be controlled independently.

• For stash transactions, any combination of target enables is permitted.

• For non-stash transactions, AWSTASHLPIDEN and AWSTASHNIDEN must be LOW.

• When AWSTASHNIDEN is LOW, AWSTASHNID is invalid and must be zero.

• When AWSTASHLPIDEN is LOW, AWSTASHLPID is invalid and must be zero.

• It is permitted, but not recommended to send a stash transaction with a stash target that indicates a component that does not support cache stashing. The indication of a stash target within a stash transaction does not affect which components are permitted to access and cache a given cache line.

For WriteUniquePtlStash and WriteUniqueFullStash requests without a target, the following is recommended:

• If the interconnect can determine that the line is held in a single cache before the write occurs, then stash the cache line back to that cache.

• If the cache line is not held in any cache before the write occurs, then stash the cache line in a shared system cache.

For StashOnceShared and StashOnceUnique requests without a target:

• If the interconnect can determine that the cache line is not in any cache, then it is recommended to stash the cache line in a shared system cache.

• A component can use this to prefetch a cache line to a downstream cache for its own use.

## A8.7.5 Transaction ID for stash transactions

There are no constraints on the use of AXI ID values for WriteUniquePtlStash and WriteUniqueFullStash transactions.

StashOnceShared and StashOnceUnique can be referred to as StashOnce transactions.

StashOnce transactions must not use the same AXI ID values that are used by non-StashOnce transactions on the write channels that are outstanding at the same time. This rule ensures that there are no ordering constraints between StashOnce transactions and other transactions. Therefore, a component that discards a StashOnce request can give an immediate response without checking ID ordering requirements.

StashOnce transactions and non-StashOnce transactions are permitted to use the same AXI ID value, provided that the same ID value is not used by both a StashOnce transaction and a non-StashOnce at the same time.

There can be multiple outstanding StashOnce transactions with the same ID.

There can be multiple outstanding non-StashOnce transactions with the same ID.

The use of a unique ID value for a StashOnce transaction ensures that these transactions can be given an immediate response if they are not supported.

## A8.7.6 Support for stash transactions

The Cache\_Stash\_Transactions property is used to indicate whether an interface supports cache stashing, as shown in Table A8.19.

Table A8.19: Cache\_Stash\_Transactions property
<table><tr><td>Cache_Stash_Transactions Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>All cache stashing Opcodes are supported. There may or may not be a stash target.</td></tr><tr><td>Basic</td><td></td><td>Only the StashOnceShared Opcode is supported. A stash target is not permitted, STASHLPID_Present and STASHNID_Present must be False.</td></tr><tr><td>False</td><td>Y</td><td>Cache stashing is not supported and associated signals are omitted.</td></tr></table>

When Cache\_Stash\_Transactions is False, STASHNID\_Present and STASHLPID\_Present must both be False. The compatibility between Manager and Subordinate interfaces according to the values of the Cache\_Stash\_Transactions property is shown in Table A8.20.

Table A8.20: Stash transactions compatibility
<table><tr><td>Cache_Stash_Transactions</td><td>Subordinate: False</td><td>Subordinate: Basic</td><td>Subordinate: True</td></tr><tr><td>Manager: False</td><td>Compatible.</td><td>Compatible.</td><td>Compatible.</td></tr><tr><td>Manager: Basic</td><td>Incompatible, action must be taken.</td><td>Compatible.</td><td>Compatible.</td></tr><tr><td>Manager: True</td><td>Incompatible, action must be taken.</td><td>Incompatible, action must be taken.</td><td>Compatible.</td></tr></table>

If a Manager issues stash requests to a target that does not support them, action can be taken in the Manager or interconnect as shown in Table A8.21.

Table A8.21: Action needed if the target does not support stash transactions
<table><tr><td>Stash transaction</td><td>Action</td></tr><tr><td>WriteUniquePtlStash</td><td>Convert to WriteUniquePtl.</td></tr><tr><td>WriteUniqueFullStash</td><td>Convert to WriteUniqueFull.</td></tr><tr><td>StashOnceShared</td><td>Do not propagate and give an immediate response.</td></tr><tr><td>StashOnceUnique</td><td>Do not propagate and give an immediate response.</td></tr></table>

## A8.8 Deallocating read transactions

Deallocating read transactions can be used when a Manager requires data which is not likely to be used again by any Manager. A cache can use this as a hint to evict the line and make the resource available for other data.

The DeAllocation\_Transactions property is used to indicate whether a component supports deallocating transactions as shown in Table A8.22.

Interoperability between a component that issues deallocating transactions and a component that does not support them can be performed by converting the Opcode to ReadOnce.

Table A8.22: DeAllocation\_Transactions property
<table><tr><td>DeAllocation_Transactions Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>Deallocating transactions are supported.</td></tr><tr><td>False</td><td>Y</td><td>Deallocating transactions are not supported.</td></tr></table>

## A8.8.1 Deallocating read Opcodes

This specification defines two deallocating transaction Opcodes on the read request channel:

## ReadOnceCleanInvalid (ROCI)

This request reads a snapshot of the current value of the cache line. It is recommended, but not required that any cached copy of the cache line is deallocated. If a Dirty copy of the cache line exists, and the cache line is deallocated, then the Dirty copy must be written back to main memory.

ReadOnceCleanInvalid is signaled using an ARSNOOP value of 0b0100.

## ReadOnceMakeInvalid (ROMI)

This request reads a snapshot of the current value of the cache line. It is recommended, but not required that any cached copy of the cache line is deallocated. It is permitted, but not required that a Dirty copy of the cache line is discarded. The Dirty copy of the cache line does not need to be written back to main memory.

ReadOnceMakeInvalid is signaled using an ARSNOOP value of 0b0101.

## A8.8.2 Rules and recommendations

Deallocating transactions are only permitted to access one cache line at a time and are not permitted to cross a cache line boundary. Size must be cache line sized or smaller.

A ROMI request to part of a cache line can result in the invalidation of the entire cache line. Some implementations might not support the deallocation behavior for transactions that are less than a cache line and instead convert the transaction to ReadOnce in such cases.

ROCI and ROMI are only supported in the Shareable Domain, so the Shareable\_Transactions property must be True if DeAllocation\_Transactions is True.

For a ROMI transaction, it is required that the invalidation of the cache line is committed before the return of the first item of read data for the transaction. The invalidation of the cache line is not required to have completed at this point. However, it must be ensured that any later write transaction from any agent that starts after this point, is guaranteed not to be invalidated by this transaction.

The following considerations apply to the use of deallocating transactions:

• Caution is needed when deallocating transactions are issued to the same cache line that other agents are using for exclusive accesses. This is because the deallocation can cause an exclusive sequence to fail.

• Apart from the interaction with exclusive accesses, the ROCI transaction only provides a hint for deallocation of a cache line and has no other impact on the correctness of a system.

• The use of the ROMI transaction can cause the loss of a Dirty cache line. The use of this transaction must be strictly limited to scenarios when it is known that it is safe to do so.

• Deallocating transactions do not guarantee that a cache line will be cleaned or invalidated, so cannot be used to ensure that data is visible to all observers.

## A8.9 Invalidate hint

The InvalidateHint transaction is a data-less deallocation hint. It can be used when a Manager has finished working with a data set and that data might be allocated in a downstream cache. An InvalidateHint request informs the cache that the line is no longer required and can be invalidated. A write-back of the line is permitted but not required.

InvalidateHint is not required to be executed for functional correctness, so can be terminated at any point in the system by responding with BRESP of OKAY.

Care is needed when using an InvalidateHint transaction to avoid exposure of previously overwritten values. This can be achieved either by:

• Ensuring that a clean operation following a scrubbing write ensures that the write has been propagated sufficiently far that it is not removed by the Invalidate Hint transaction.

• Ensuring the use of the InvalidateHint transaction is limited to address ranges that will not contain sensitive information.

## A8.9.1 Invalidate Hint signaling

InvalidateHint is a data-less transaction using AW and B channels.

The following constraints apply to an InvalidateHint request:

• AWSNOOP is 0b10010.

– AWSNOOP must be 5b wide if the InvalidateHint\_Transaction property is True.

• AWDOMAIN can be Non-shareable or Shareable.

• AWBURST is INCR.

• AWSIZE and AWLEN must be cache line sized and Regular.

• AWCACHE is Normal Cacheable.

• AWID is unique-in-flight, which means:

– An InvalidateHint request can only be issued if there are no outstanding transactions on the write channels using the same ID value.

– A Manager must not issue a request on the write channels with the same ID as an outstanding InvalidateHint transaction.

– If present, AWIDUNQ must be asserted for an InvalidateHint request.

• AWLOCK is deasserted, not an exclusive access.

• AWTAGOP is Invalid.

• AWATOP is Non-atomic operation.

## A8.9.2 Invalidate Hint support

The InvalidateHint\_Transaction property is used to indicate whether an interface supports the InvalidateHint transaction, as shown in Table A8.23.

Table A8.23: InvalidateHint\_Transaction property
<table><tr><td>InvalidateHint_Transaction Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>InvalidateHint is supported.</td></tr><tr><td>False</td><td>Y</td><td>InvalidateHint is not supported.</td></tr></table>

The compatibility between Manager and Subordinate interfaces according to the values of the InvalidateHint\_Transaction property is shown in Table A8.24.

Table A8.24: InvalidateHint\_Transaction compatibility
<table><tr><td>InvalidateHint_Transaction</td><td>Subordinate: False</td><td>Subordinate: True</td></tr><tr><td>Manager: False</td><td>Compatible.</td><td>Compatible.</td></tr><tr><td>Manager: True</td><td>Not compatible. An adapter that responds OKAY to InvalidateHint could be used to make it compatible.</td><td>Compatible.</td></tr></table>

## Chapter A9 Cache maintenance

This chapter describes cache maintenance operations (CMOs) that assist with software cache management. It contains the following sections:

• A9.1 Cache Maintenance Operations

• A9.2 Actions on receiving a CMO

• A9.3 CMO request attributes

• A9.4 CMO propagation

• A9.5 CMOs on the write channels

• A9.6 Write with CMO

• A9.7 CMOs on the read channels

• A9.8 CMOs for Persistence

• A9.9 Cache maintenance and Realm Management Extension

• A9.10 Cache maintenance to the Point of Physical Storage

• A9.11 Processor cache maintenance instructions

## A9.1 Cache Maintenance Operations

Cache maintenance operations are requests that instruct caches to clean and invalidate cache lines. Unlike the allocation and deallocation hints, it is mandatory that a cache actions a CMO that targets a line it has cached.

CMOs can be transported on either the read or write channels.

Transporting CMOs on read channels is included in this specification to support legacy components. It is recommended that the new designs transmit CMOs on the write channels.

The specification supports the following cache maintenance operations.

## CleanShared (CS)

When completed, all cached copies of the addressed line are Clean and any associated writes are observable.

## CleanSharedPersist (CSP)

When completed, all cached copies of the addressed line are Clean and any associated writes are observable and have reached the Point of Persistence (PoP). See A9.8 CMOs for Persistence.

## CleanSharedDeepPersist (CSDP)

When completed, all cached copies of the addressed line are Clean and any associated writes are observable and have reached the Point of Deep Persistence (PoDP). See A9.8 CMOsfor Persistence.

## CleanInvalid (CI)

When completed, all cached copies of the addressed line are invalidated, having been written to memory if they were Dirty. Any associated writes are observable.

## CleanInvalidPoPA (CIPA)

When completed, all cached copies of the addressed line are invalidated, and any Dirty cached copy is written past the Point of Physical Aliasing (PoPA). See A9.9 Cache maintenance and Realm Management Extension.

## CleanInvalidStorage (CIS)

When completed, all cached copies of the addressed line are invalidated, and any Dirty cached copy is written past the Point of Physical Storage (PoPS). See A9.10 Cache maintenance to the Point ofPhysical Storage.

## MakeInvalid (MI)

When completed, all cached copies of the addressed line are invalidated, and any Dirty cached copy might have been discarded.

## A9.2 Actions on receiving a CMO

When a component receives a CMO, it must do the following:

1. If the component is a cache and the CMO is cacheable, it must look up the line.

2. If the component is a coherent interconnect and the CMO is Shareable, a CMO snoop must be sent to any cache that might have the line:

• Allocated, for an Invalidate CMO.

• Dirty, for a Clean CMO.

Note that a coherent protocol such as AMBA CHI [5] is required to send CMO snoop requests.

3. For a Clean CMO, write back any dirty data that is found in the cache or peer caches.

It is recommended that Write-Through No-Allocate is used for writes to memory which will be followed by a CMO to the same line. This ensures that the line will be looked up in any downstream cache but will not be allocated.

4. Wait for all snoops and associated writes to receive a response.

5. If the CMO does not need to be sent downstream, the component can issue a response to the CMO.

6. If the CMO does need to be sent downstream, the CMO must be sent and the response that is returned must be propagated when it is received from downstream.

## A9.3 CMO request attributes

The following rules apply to CMO transactions:

• The request must be cache line sized and Regular. See A3.1.8 Regular transactions for more details.

• The Domain can be Non-shareable or Shareable.

– System Domain is not permitted, which means that CMO transactions must be Normal rather than Device.

– If AxDOMAIN is omitted from the interface, CMO transactions are assumed to be Non-shareable.

The AxCACHE and AxDOMAIN attributes indicate which caches must action a CMO, as shown in Table A9.1.

Table A9.1: CMO applicability
<table><tr><td>AxCACHE</td><td>AxDOMAIN</td><td>CMO applies to</td></tr><tr><td>Device</td><td>System</td><td>N/A (not legal for CMOs)</td></tr><tr><td rowspan="2">Non-cacheable</td><td>Non-shareable</td><td>No caches</td></tr><tr><td>Shareable</td><td>Peer caches</td></tr><tr><td rowspan="2">Cacheable</td><td>Non-shareable</td><td>In-line caches</td></tr><tr><td>Shareable</td><td>Peer caches and in-line caches</td></tr></table>

To maintain coherency, the following recommendations apply to CMOs and non-CMOs:

• If a location is cacheable for non-CMO transactions, it should be cacheable for CMO transactions.

• If a location is in the Shareable Domain for non-CMO transactions, it should be in the Shareable Domain for CMO transactions.

• If a location is in the Non-shareable Domain for non-CMO transactions, it can be in the Non-shareable or Shareable Domain for CMO transactions.

• A Manager should not issue a read request that permits it to allocate a line, while there is an outstanding CMO to that line.

• Allocation hints, such as AxCACHE[3:2], are not required to match between CMO and non-CMO transactions to the same cache line.

## A9.4 CMO propagation

The propagation of CMOs downstream of components depends on the system topology. A CMO must be propagated downstream if the CMO is cacheable and there is a downstream cache which might have allocated the line and there is an observer downstream of that cache.

Two mechanisms are defined for controlling whether CMOs are propagated from a Manager interface.

• At design-time, using the properties CMO\_On\_Write or CMO\_On\_Read.

• At run-time, using the optional BROADCASTCACHEMAINT and BROADCASTSHAREABLE tie-off inputs to a Manager interface.

Table A9.2: BROADCASTCACHEMAINT signal
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>BROADCASTCACHEMAINT</td><td>1</td><td>0b1</td><td>Manager tie-off input, used to control the issuing of CMOs from an interface.</td></tr></table>

## When BROADCASTCACHEMAINT and BROADCASTSHAREABLE are both present and deasserted:

• CleanShared, CleanInvalid and MakeInvalid requests are not issued.

• WritePtlCMO with CleanShared or CleanInvalid is converted to WriteNoSnoop.

• WriteFullCMO with CleanShared or CleanInvalid is converted to WriteNoSnoop or WriteNoSnoopFull.

## A9.5 CMOs on the write channels

The CMO\_On\_Write property is used to indicate whether an interface supports CMOs on the write channels.

Table A9.3: CMO\_On\_Write property
<table><tr><td></td><td>CMO_On_Write Default Description</td><td></td></tr><tr><td>True</td><td></td><td>CMOs are supported on the AW and B channels.</td></tr><tr><td>False</td><td>Y</td><td>CMOs are not supported on the AW and B channels. They are either signaled on the read channels or not used by this interface.</td></tr></table>

On the write channels, CMOs can be sent as a stand-alone operation or combined with a data write. The AWSNOOP encodings that can be used to signal CMO requests on the AW channel are shown in Table A9.4. For more information on the combined write with CMO operations see A9.6 Write with CMO.

Table A9.4: AWSNOOP encodings

<table><tr><td>AWSNOOP</td><td>Operation</td><td>Enable property</td><td>Description</td></tr><tr><td>0b0110</td><td>CMO</td><td>CMO_On_Write</td><td>Stand-alone CMO.</td></tr><tr><td>0b1010</td><td>WritePtlCMO</td><td>Write_Plus_CMO</td><td>CMO combined with a write which is less than or equal to one cache line.</td></tr><tr><td>0b1011</td><td>WriteFullCMO</td><td>Write_Plus_CMO</td><td>CMO combined with a write which is exactly one cache line.</td></tr></table>

The AWCMO signal indicates the type of CMO that is requested, it is present on the AW channel when CMO\_On\_Write is True.

Table A9.5: AWCMO signal

<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWCMO</td><td>AWCMO_WIDTH</td><td>0b000</td><td>Indicates the CMO type for write opcodes that</td></tr><tr><td rowspan="2"></td><td rowspan="2"></td><td>(CleanInvalid)</td><td>include a cache maintenance operation.</td></tr><tr><td></td><td></td></tr></table>

The width of AWCMO is determined by the property AWCMO\_WIDTH.

Table A9.6: AWCMO\_WIDTH property
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>AWCMO_WIDTH</td><td>0,2,3</td><td>0</td><td>Width of AWCMO in bits.</td></tr></table>

The rules for AWCMO\_WIDTH are:

• Must be 0 if CMO\_On\_Write is False. This means that AWCMO is not on the interface.

• Must be 2 if CMO\_On\_Write is True and RME\_Support is False.

• Must be 3 if CMO\_On\_Write is True and

– RME\_Support is True or

– Storage\_CMO is True.

The encodings for AWCMO are shown in Table A9.7. An encoding cannot be used if the associated enable property is False.

Table A9.7: AWCMO encodings
<table><tr><td>AWCMO</td><td>Label</td><td>Enable property</td><td>Meaning</td></tr><tr><td>0b000</td><td>CleanInvalid</td><td></td><td>Clean and invalidate</td></tr><tr><td>0b001</td><td>CleanShared</td><td></td><td>Clean only</td></tr><tr><td>0b010</td><td>CleanSharedPersist</td><td>Persist_CMO</td><td>Clean to the Point of Persistence</td></tr><tr><td>0b011</td><td>CleanSharedDeepPersist</td><td>Persist_CMO</td><td>Clean to the Point of Deep Persistence</td></tr><tr><td>0b100</td><td>CleanInvalidPoPA</td><td>RME_Support</td><td>Clean and invalidate to the Point of Physical Aliasing</td></tr><tr><td>0b101</td><td>CleanInvalidStorage</td><td>Storage_CMO</td><td>Clean and invalidate to the Point of Physical Storage</td></tr><tr><td>0b110</td><td>RESERVED</td><td></td><td>一</td></tr><tr><td>0b111</td><td>RESERVED</td><td></td><td>=</td></tr></table>

Note that MakeInvalid is not supported on the write channels.

When AWSNOOP is not CMO, WritePtlCMO or WriteFullCMO, AWCMO must be 0b000.

A CMO transaction on the write channels consists of a request on the AW channel and a response on the B channel. There are no transfers on the W channel in a CMO transaction.

The write response to the CMOs CleanInvalid and CleanShared have a single response transfer on the B channel. This indicates that all caches are Clean and/or invalid within the specified Domain and any associated writes are observable.

Other CMOs are described in:

• A9.8 CMOs for Persistence

• A9.9 Cache maintenance and Realm Management Extension

• A9.10 Cache maintenance to the Point of Physical Storage

## A9.6 Write with CMO

Cache maintenance operations are often used with a write to memory. For example:

• A write from an I/O agent which must be made visible to observers which are downstream of caches.

• A write to persistent memory that must ensure that all copies of the line are also cleaned to the point of persistence.

• A CMO that causes a write back of dirty data, which must be followed by the CMO.

A write with CMO combines a write with a CMO to improve the efficiency of this type of scenario. It is expected that some Managers will natively generate a write with CMO. In other cases, a cache or interconnect will combine a CMO with a write before propagating them downstream.

The Write\_Plus\_CMO property is used to indicate whether a component supports combined write and CMOs on the write channels.

Table A9.8: Write\_Plus\_CMO property
<table><tr><td>Write_Plus_CMO Default Description</td><td></td></tr><tr><td>True</td><td>Combined write and cache maintenance operations are supported.</td></tr><tr><td>False Y</td><td>Combined write and cache maintenance operations are not supported.</td></tr></table>

If the Write\_Plus\_CMO property is True, the CMO\_On\_Write property must also be True.

When Write\_Plus\_CMO is True, the WritePtlCMO and WriteFullCMO Opcodes can be used to indicate a write with CMO.

A write with CMO can use any of the CMO types as indicated by AWCMO.

Some example uses of write with CMO are shown in the Table A9.9.

Table A9.9: Examples of write with CMO transactions
<table><tr><td>Operation</td><td>Primary use-case</td><td>Action</td></tr><tr><td>Shareable WritePtlCMO with CleanShared</td><td>An I/O agent writing less than a cache line to a Shareable region, where the data must be visible to observers downstream of a cache.</td><td>All in-line and peer caches must look up the line and write back any dirty data. Data from a Dirty cache line can be merged with the partial write to form a WriteFullCMO with CleanShared to go downstream.</td></tr><tr><td>Shareable WriteFullCMO with CleadSharedPersist</td><td>An I/O agent writing a cache line to a Shareable region, where the data must reach the Point of Persistence.</td><td>The coherent interconnect issues a MakeInvalid snoop to coherent peer caches. In-line caches look up the line and either update or invalidate any copies. The write and CleanSharedPersist must be propagated if there is a Point of Persistence downstream.</td></tr><tr><td>Non-shareable WriteFullCMO with CleanInvalid</td><td>Issued by a cache when a CleanInvalid CMO has hit a Dirty line and caused a write to memory.</td><td>All in-line and peer cache entries must be cleaned and invalidated. The write and CleanInvalid must be propagated if there are observers downstream.</td></tr></table>

## A9.6.1 Attributes for write with CMO

A write with CMO has the following attribute constraints:

• AWSNOOP is 0b1010 to indicate WritePtlCMO and 0b1011 to indicate WriteFullCMO.

• AWLOCK is deasserted, not an exclusive access.

A WriteFullCMO must be cache line sized and Regular, see A8.2 Cache line size and A3.1.8 Regular transactions.

A WritePtlCMO must be cache line sized or smaller and not cross a cache line boundary. The associated CMO applies to the whole of the addressed cache line. AWBURST must not be FIXED.

The cache maintenance part of the write with CMO is always treated as cacheable and Shareable, irrespective of AWCACHE and AWDOMAIN.

## A9.6.2 Propagation of write with CMO

Propagation of a write with CMO follows the same rules as the propagation of a CMO. It is possible to split a write with CMO into separate write and CMO transactions for propagation downstream. In that case, either:

• The write is issued first, followed by the CMO on the write request channel with the same ID as the write.

• The write is issued first. When the write response is received, the CMO can be issued on the write or read channel.

When splitting a write and CMO, if AWDOMAIN is Shareable, then:

• WritePtlCMO becomes WriteUniquePtl.

• WriteFullCMO becomes WriteUniqueFull.

If AWDOMAIN is Non-shareable, then the write becomes WriteNoSnoop or WriteNoSnoopFull.

The CMO is sent as cacheable. If there is a downstream cache in the Shareable Domain, the CMO is sent as Shareable.

If there is no cache downstream that requires management by cache maintenance, the CMO part of the transaction can be discarded. If the discarded CMO is a CleanSharedPersist or CleanSharedDeepPersist, the BCOMP and BPERSIST signals must be set on the write response. See A9.8 CMOsfor Persistence for more details.

## A9.6.3 Response to write with CMOs

Responses to writes with CMOs follow the same rules as CMOs on the write channel.

A write with CI or CS has a single response transfer which indicates that the write and CMO are both observable.

A write with a CSP or CSDP, has one response that indicates that the write is observable and one response that indicates that the write has reached the PoP / PoDP.

As with a standalone CSP/CSDP, a Subordinate can optionally combine the two responses into a single transfer.

A write with CMO is not permitted to use the MTE Match opcode, so a write response that is combined with Persist and Match responses is not necessary. See A12.2 Memory Tagging Extension (MTE) for more details

## A9.6.4 Example flow with a write plus CMO

As an example of a flow using a write with CMO, Figure A9.1 shows an I/O Coherent Manager issuing a Shareable CleanShared request on the AW channel into a CHI interconnect.

• The snoop generated by the coherent interconnect hits dirty data in the coherent cache.

• The interconnect then issues a Non-shareable WriteFullCMO with CleanShared.

• The system cache looks up the line, overwrites any existing copies and forwards the write request to the memory. The memory does not need to receive CMOs because its data is observable to all agents.

• The memory controller returns an OKAY response when the data is observable, which is propagated back to the Manager.

![](images/74cf8a115b036f9889d4f475ada4ff65f7e7db2bd0824c6d083ae4a954c7acb7.jpg)  
Figure A9.1: Example write with CMO

## A9.7 CMOs on the read channels

The CMO\_On\_Read property is used to indicate whether an interface supports CMOs on the read channels.

Table A9.10: CMO\_On\_Read property
<table><tr><td>CMO_On_Read Default Description</td><td></td><td></td></tr><tr><td>True</td><td>Y</td><td>CMOs are supported on the AR and R channels.</td></tr><tr><td>False</td><td></td><td>CMOs are not supported on the AR and R channels. They are either signaled on the write channels or not used by this interface.</td></tr></table>

A CMO transaction on the read channels consists of a request on the AR channel and a single transfer response on the R channel. The response indicates that the CMO is observed, and all cache lines have been cleaned and invalidated if necessary.

Table A9.11: ARSNOOP encodings
<table><tr><td>ARSNOOP</td><td>Operation</td></tr><tr><td>0b1000</td><td>CleanShared</td></tr><tr><td>0b1001</td><td>CleanInvalid</td></tr><tr><td>0b1010</td><td>CleanSharedPersist</td></tr><tr><td>0b1101</td><td>MakeInvalid</td></tr></table>

The ARSNOOP encodings used to signal CMO requests on the AR channel are shown in Table A9.11.

## A9.8 CMOs for Persistence

Cache maintenance operations for Persistence are used to provide a cache clean to the Point of Persistence or Point of Deep Persistence. These operations are used to ensure that a store operation, which might be held in a Dirty cache line, is moved downstream to persistent memory.

The Persist\_CMO property is used to indicate whether a component supports cache maintenance for Persistence.

Table A9.12: Persist\_CMO property
<table><tr><td>Persist_CMO</td><td>Default Description</td><td></td></tr><tr><td>True</td><td></td><td>Persistent CMOs are supported.</td></tr><tr><td>False</td><td>Y</td><td>Persistent CMOs are not supported.</td></tr></table>

Persistent CMOs can be transmitted on either read or write channels, according to the CMO\_On\_Write and CMO\_On\_Read properties.

If CMO\_On\_Write and CMO\_On\_Read are both False, Persist\_CMO must be False.

## A9.8.1 Point of Persistence and Deep Persistence

In systems with non-volatile memory, each memory location has a point in the hierarchy at which data can be relied upon to be persistent when power is removed. This is known as the Point of Persistence (PoP).

Some systems require multiple levels of guarantee regarding the persistence of data. For example, some data might need the guarantee that it is preserved on power failure and also backup battery failure. To support such a requirement, this specification also defines the Point of Deep Persistence (PoDP).

Systems might have different points for the PoP and PoDP, or they might be the same.

## A9.8.2 Persistent CMO (PCMO) transactions

The specification supports the following PCMO transactions.

## CleanSharedPersist (CSP)

When this completes, all cached copies of the addressed line in the specified Domain are Clean and any associated writes are observable and have reached the Point of Persistence (PoP).

## CleanSharedDeepPersist (CSDP)

When this completes, all cached copies of the addressed line in the specified Domain are Clean and any associated writes are observable and have reached the Point of Deep Persistence (PoDP).

When a component receives a PCMO, it is processed in the same way as a CleanShared transaction. If a snoop is required, a CleanShared snoop transaction is used.

## A9.8.3 PCMO propagation

The propagation of PCMOs downstream of components depends on the system topology. A PCMO must be propagated downstream in the following circumstances:

1. If the PCMO is cacheable and there is a downstream cache which might have allocated the cache line and there is an observer downstream of that cache.

2. If there is a PoP downstream of the component.

3. If the PCMO is a CleanSharedDeepPersist and there is a PoDP downstream of the component.

If (1) applies, but not (2) or (3), then a CleanSharedPersist or CleanSharedDeepPersist can be changed to a CleanShared before being sent downstream.

If the PCMO is changed to a CleanShared, the Persist response must be sent by the component doing the transformation.

The propagation of PCMOs can be controlled at reset-time using the optional Manager input BROADCASTPERSIST.

Table A9.13: BROADCASTPERSIST signal
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>BROADCASTPERSIST</td><td>1</td><td>0b1</td><td>Manager tie-off input, used to control the issuing of CleanSharedPersist and</td></tr></table>

When BROADCASTPERSIST is present and deasserted, CleanSharedPersist and CleanSharedDeepPersist are converted to CleanShared. This applies to standalone CMOs and write with CMOs.

Note that the issuing of the CleanShared is controlled by the BROADCASTSHAREABLE and BROADCASTCACHEMAINT signals.

## A9.8.4 PCMOs on write channels

When using write channels to transport cache maintenance operations, CleanSharedPersist and CleanSharedDeepPersist are both supported.

## PCMO request on the AWchannel

A PCMO request on the write channels is signaled by setting AWSNOOP to CMO, WritePtlCMO or WriteFullCMO. See Table A9.4 for encodings.

The AWCMO signal then indicates CleanSharedPersist or CleanSharedDeepPersist, see Table A9.7.

When Persist\_CMO is False, AWCMO must not indicate CleanSharedPersist or CleanSharedDeepPersist.

## PCMO response on the B channel

CleanSharedPersist and CleanSharedDeepPersist transactions on the AW channel have two responses: a Completion response and a Persist response.

Having separate responses enables system tracking resources to be freed up early, in the case that committing data to the PoP/PoDP takes a long time. The Completion and Persist responses can occur in any order and can be separated by responses from other transactions.

The Completion and Persist responses are signaled using two signals that are included on the write response (B) channel when CMO\_On\_Write and Persist\_CMO are both True.

Table A9.14: Signals for responding to a PCMO
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>BCOMP</td><td>1</td><td>0b1</td><td>Asserted HIGH to indicate a Completion response.</td></tr><tr><td>BPERSIST</td><td>1</td><td>0b0</td><td>Asserted HIGH to indicate a Persist response.</td></tr></table>

The Completion response indicates that all caches are Clean, and any associated writes are observable. It has the following rules:

• BCOMP is asserted and BPERSIST is deasserted.

• BID is driven with the same value as AWID.

• If loopback signaling is supported, BLOOP is driven from AWLOOP.

• If AWIDUNQ was asserted, the ID can be reused when this response is received.

• BRESP can take any value that is legal for a PCMO request.

• The Completion response must follow normal response ordering rules.

• If BCOMP is present on an interface, it must be asserted for one response transfer in all transactions on the write channels.

The Persist response indicates that the data has reached the PoP or PoDP. It has the following rules:

• BCOMP is deasserted and BPERSIST is asserted.

• BID is driven from AWID.

• BIDUNQ can take any value, it is not required to have the same value as AWIDUNQ.

• BLOOP can take any value, it is not required to be driven from AWLOOP.

• BRESP can take any value that is legal for a PCMO request.

• The Persist response has no ordering requirements, it can overtake or be overtaken by other response transfers.

• If BPERSIST is present on an interface, it must be asserted for one transfer of a response to a CSP or CSDP. It must be deasserted for all other responses.

A Subordinate can optionally combine the two responses into a single transfer. The following rules apply:

• BCOMP and BPERSIST are both asserted.

• BID is driven from AWID.

• If loopback signaling is supported, BLOOP is driven from AWLOOP.

• BRESP can take any value that is legal for a PCMO request.

• The combined response must follow normal response ordering rules.

• If AWIDUNQ was asserted, the ID can be reused when this response is received.

A Manager can count the number of responses returned with BPERSIST asserted, allowing it to determine when it has no outstanding persistent operations.

## Example PCMO using write channels

An example of a CleanSharedPersist transaction on the write channels is shown in Figure A9.2.

In this example, the write is observable to all other agents in the last-level cache, so the Completion response can be sent when the request has been hazarded at that point. The Non-volatile Memory sends a combined Completion and Persist response, so the cache must deassert BCOMP when it propagates the response upstream.

![](images/7a98680a9cd126fb6123217f2eeb0fc215312afb5b83dc79f2d5269a8b791ee4.jpg)  
Figure A9.2: Example PCMO transaction

## A9.8.5 PCMOs on read channels

If using read channels to transport cache maintenance operations, only the CleanSharedPersist transaction is supported. CleanSharedDeepPersist can only be used on the write channels.

A CleanSharedPersist is signaled by setting ARSNOOP to 0b1010.

When Persist\_CMO is False, ARSNOOP must not indicate CleanSharedPersist.

There is a single response transfer on the R channel which indicates that the request is observed, and all cache lines have been cleaned to the PoP.

## A9.9 Cache maintenance and Realm Management Extension

When using the Realm Management Extensions (RME), it is required that cache maintenance operations apply to all lines with the same address and physical address space as the CMO, irrespective of other attributes. Table A9.15 illustrates which cache lines must be operated on by a CMO with and without RME support. See A4.5 Protection attributes and [4] for more information.

Table A9.15: Cache lines operated on by a CMO
<table><tr><td>Attribute</td><td>RME_Support is False</td><td>RME_Support is True</td></tr><tr><td>Address</td><td>Same cache line</td><td>Same cache line</td></tr><tr><td>Physical Address Space</td><td>Same</td><td>Same</td></tr><tr><td>Memory attributes</td><td>Any AxCACHE</td><td>Any AxCACHE</td></tr><tr><td>Shareability Domain</td><td>Same Domain</td><td>Any Domain</td></tr></table>

When acted upon by a CleanInvalid or CleanShared CMO, data must propagate to a point where it is observable to all agents using the same physical address space as the CMO.

## A9.9.1 CMO to PoPA

RME defines the Point of Physical Aliasing (PoPA), which is the point in a system where data is observable to accesses from all agents, irrespective of physical address space.

There is a CMO named CleanInvalidPoPA, which helps transitioning ownership of a physical granule from one Security state to another.

The response to a CleanInvalidPoPA indicates that all cached copies are invalidated, and any Dirty cached copy is written past the PoPA.

CleanInvalidPoPA has the same rules as other CMOs, regarding lines that are acted upon and transaction attribute restrictions.

When RME\_Support is True, the AWCMO signal is extended to 3b to enable the signaling of a CleanInvalidPoPA, encodings are:

• 0b000: CleanInvalid

• 0b001: CleanShared

• 0b010: CleanSharedPersist

• 0b011: CleanSharedDeepPersist

• 0b100: CleanInvalidPoPA

A CleanInvalidPoPA can be used stand-alone or combined with a write transaction, so can be used with the following values of AWSNOOP:

• 0b0110: CMO

• 0b1010: WritePtlCMO

• 0b1011: WriteFullCMO

The CMO\_On\_Write property must be True to use a CleanInvalidPoPA.

The Write\_Plus\_CMO property must be True to use a write with CleanInvalidPoPA.

When using Memory Encryption Contexts, a CleanInvalidPoPA CMO can be used to ensure that data is cleaned and invalidated in all caches upstream of the Point of Encryption. See A4.6 Memory Encryption Contexts for more information.

## A9.9.2 CMO to PoPA propagation

An optional input signal, BROADCASTCMOPOPA can be used to control the propagation of CleanInvalidPoPA at reset-time.

Table A9.16: BROADCASTCMOPOPA signal
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>BROADCASTCMOPOPA</td><td>1</td><td>0b1</td><td>Manager tie-off input, used to control the issuing of a CleanInvalidPoPA CMO.</td></tr></table>

When BROADCASTCMOPOPA is present and deasserted, then CleanInvalidPoPA is converted to CleanInvalid.   
This applies to standalone CMOs and write with CMOs.

Note that the issuing of the CleanInvalid is controlled by the BROADCASTSHAREABLE and BROADCASTCACHEMAINT signals.

## A9.10 Cache maintenance to the Point of Physical Storage

For systems with long uptimes, such as server and HPC, software needs a mechanism to efficiently remove poison and detect which locations have persistent errors.

In order to remove poison from a location, it can be overwritten by a known good value and the value read back to check that the poison has been removed and the error is not persistent.

However, if the location is cached, this mechanism might not work. The write could be allocated into a local cache and only the cached copy modified. A subsequent read of the location would return the value from a cache and the test would show that the poison is removed. The cached copy might later be written back to memory where it could fail to remove poison if the fault is persistent.

To avoid this scenario, it is necessary to define the Point ofPhysical Storage (PoPS), which is the furthest point in the memory system to which a write transaction can propagate. This is expected to be at the memory interface, after all buffers and caches.

A CleanInvalidStorage can be used to clean and invalidate data from all caches and buffers between the requester and PoPS. After this completes, a read from the same cache line is guaranteed to return data from memory rather than a cache.

A programmer can issue a write to clear the poison, then a CleanInvalidStorage CMO to push the value to memory.   
A read of the location can be used to check that the poison is cleared.

The property Storage\_CMO indicates if an interface supports the CleanInvalidStorage operation.

Table A9.17: Storage\_CMO property
<table><tr><td>Storage_CMO Default</td><td>Description</td><td></td></tr><tr><td>True</td><td></td><td>CleanInvalidStorage CMO is supported.</td></tr><tr><td>False</td><td>Y</td><td>CleanInvalidStorage CMO is not supported.</td></tr></table>

Storage\_CMO can only be True when CMO\_On\_Write is True.

CleanInvalidStorage can be used as a stand-alone CMO or as part of a full line write with CMO, using the AWCMO signal. That means the Opcode can be CMO or WriteFullCMO, but not WritePtlCMO.

Table A9.18 shows compatibility between Manager and Subordinate interfaces, according to the values of the Storage\_CMO property.

Table A9.18: Storage\_CMO compatibility
<table><tr><td>Storage_CMO</td><td>Subordinate: False</td><td>Subordinate: True</td></tr><tr><td>Manager: False</td><td>Compatible.</td><td>Compatible.</td></tr><tr><td>Manager: True</td><td>Not compatible.</td><td>Compatible.</td></tr></table>

The propagation of CleanInvalidStorage can be controlled at reset-time using the optional Manager input BROADCASTSTORAGE.

Table A9.19: BROADCASTSTORAGE signal
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>BROADCASTSTORAGE</td><td>1</td><td>0b1</td><td>Manager tie-off input, used to control the issuing of a CleanInvalidStorage CMO.</td></tr></table>

When BROADCASTSTORAGE is present and deasserted, CleanInvalidStorage is converted to CleanInvalid.   
This applies to standalone CMOs and write with CMOs.

## A9.11 Processor cache maintenance instructions

The cache maintenance protocol requires that the cache maintenance operations use the AxCACHE and AxDOMAIN signals to identify the caches on which the cache maintenance operations must operate.

For a processor that has cache maintenance instructions that are required to operate on a different number of caches than are defined by the AxCACHE and AxDOMAIN values, the cacheability and shareability of the transaction must be adapted to meet the requirements of the processor.

For example, if a processor instruction performing a cache maintenance operation on a location with Device memory attributes is required to operate on all caches within the system, then the Manager must issue a cache maintenance transaction as Normal Cacheable, Shareable, since this is the most pervasive of the cache maintenance operations and operates on all the required caches.

## A9.11.1 Unpredictable behavior with software cache maintenance

Cache maintenance can be used to reliably communicate shared memory data structures between a coherent group of Managers and non-coherent agents. This process must follow a particular sequence to reliably make the data structures visible as required.

When using cache maintenance to make the writes of a non-coherent agent visible to a coherent group of Managers, there are periods of time when writing and reading the data structures gives UNPREDICTABLE results and can cause a loss of coherency.

The observation of a line that is being updated by a non-coherent agent is UNPREDICTABLE during the period between the clean transaction that starts the sequence and the invalidate transaction that completes it. During this period, it is permissible to see multiple transitions of a cache line that is being updated by a non-coherent agent.

![](images/91f4e010cfd15fdc4a61e875ba80a03046fb122fff99da77e75655c84c593b66.jpg)  
Figure A9.3: Required sequence of communication between coherent and non-coherent domains

There are five stages of communication between a coherent domain and a non-coherent agent, shown in Figure A9.3. The five-stage sequence is:

1. The coherent domain has access. The coherent domain has full read and write access to the appropriate memory locations during this stage. This stage finishes when all required writes from the coherent domain are complete within the coherent domain.

2. The coherent domain is cleaned. A cache clean operation is required for all the address locations that are undergoing software cache maintenance during this stage. The coherent domain clean forces all previous writes to be visible to the non-coherent agent. This stage finishes when all required writes are complete and therefore visible to the non-coherent agent.

3. The non-coherent agent has access. The non-coherent agent has both read and write access to the defined memory locations during this stage. This stage finishes when all required writes from the non-coherent agent are complete.

4. The coherent domain is invalidated. A cache invalidate operation is required for all the address locations that are undergoing software cache maintenance during this stage. This coherent domain invalidate stage removes all cached copies of the defined locations ensuring that any subsequent access from the coherent domain observes the writes from the non-coherent agent. This stage finishes when all the required invalidations are complete.

5. The coherent domain has full access to the defined memory locations.

The following table shows when accesses from the coherent domain or the non-coherent agent are permitted. The remaining accesses can have UNPREDICTABLE results, with possible loss of coherency.

Table A9.20: Permitted accesses from the Coherent domain and Non-coherent agent
<table><tr><td>Phase</td><td>Description</td><td colspan="2">Coherent domain</td><td colspan="2">External agent</td></tr><tr><td></td><td></td><td>Read</td><td>Write</td><td>Read</td><td>Write</td></tr><tr><td>1</td><td>Coherent domain access</td><td>Permitted</td><td>Permitted</td><td>一</td><td>一</td></tr><tr><td>2</td><td>Coherent domain clean</td><td>一</td><td>一</td><td>一</td><td>一</td></tr><tr><td>3</td><td>External agent access</td><td>一</td><td></td><td>Permitted</td><td>Permitted</td></tr><tr><td>4</td><td>Coherent domain invalidate</td><td></td><td></td><td>一</td><td>一</td></tr><tr><td>5</td><td>Coherent domain access</td><td>Permitted</td><td>Permitted</td><td>一</td><td>一</td></tr></table>

## Chapter A10 Additional request qualifiers

This chapter describes some additional request qualifiers for the AXI protocol.

It contains the following sections:

• A10.1 Non-secure Access Identifiers (NSAID)

• A10.2 Page-based Hardware Attributes (PBHA)

• A10.3 Subsystem Identifier

• A10.4 Arm Compression Technology (ACT)

## A10.1 Non-secure Access Identifiers (NSAID)

To support the storage and processing of protected data, a set of signals can be added that enable access to particular Non-secure memory locations to be controlled. The signals supply a Non-secure Access Identifier (NSAID) alongside the transaction request. The NSAID can be checked to permit or deny access to a memory location.

The NSAccess\_Identifiers property is used to indicate whether a component supports these additional signals.

Table A10.1: NSAccess\_Identifiers property
<table><tr><td>NSAccess_Identifiers</td><td>Default Description</td><td></td></tr><tr><td>True</td><td></td><td>NSAID signaling is present on the interface.</td></tr><tr><td>False</td><td>Y</td><td>NSAID signaling is not present on the interface.</td></tr></table>

## A10.1.1 NSAID signaling

If the NSAccess\_Identifiers property is True, the following signals are added to the read and write request channels.

Table A10.2: AxNSAID signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWNSAID, ARNSAID</td><td>4</td><td>0x0</td><td>Non-secure access identifier, can be checked to permit or deny access to a memory location.</td></tr></table>

A 4-bit NSAID value supports up to 16 unique identifiers. For each NSAID, there is a set of access permission that is defined which determine how locations in memory are permitted to be accessed. The access permissions can be:

• No access

• Read-only access

• Write-only access

• Read/write access

The mechanism that is used to define the access permissions for each NSAID is IMPLEMENTATION DEFINED.   
However, this mechanism is typically implemented using some form of Memory Protection Unit (MPU).

The following rules and recommendations apply to NSAID values:

• Requests to the Non-secure physical address space can use any NSAID value.

• Requests other address spaces must use an NSAID value of zero.

• It is permitted for transactions with different NSAID values to have access to overlapping memory locations.

• It is permitted for transactions with different NSAID values to have any combination of access permissions for a given memory location.

• It is recommended that Managers use the default NSAID value of zero when accessing data that is not protected, or when they do not have an assigned NSAID value.

• If a Manager is required to use a single NSAID value, then it is permitted for NSAID signals to be tied to a fixed value.

## A10.1.2 Caching and NSAID

Where caching and system coherency is performed upstream of permission checking, accesses with different NSAID values that pass data between them must be subjected to permission checks.

The rules that are associated with NSAID use and coherency are as follows:

• When an agent caches a line of data that has been fetched using a particular NSAID value, it must ensure that any subsequent write to main memory or any response to a snoop uses the same NSAID value. This rule ensures that a Manager cannot move a cache line of data from one protected region to another.

• For a read request with a given NSAID value, if a snoop is used to obtain the data:

– If the NSAID value of the snoop response matches the read request, then data can be provided directly.

– If the NSAID value of the snoop response does not match the read request, then the cache line must first be written to memory using the NSAID value obtained through the snoop response, and then read from memory using the NSAID value of the original request. The write and subsequent read are only required to reach a point at which permission checking has occurred.

• Snoop transactions that invalidate cached copies, such as MakeInvalid, must not be used if memory protection is used. All such snoop transactions must be replaced with transactions that also clean the cache line to main memory, such as CleanInvalid.

• Any interconnect-generated write to main memory that occurs as the result of a snoop must use the NSAID value that is obtained from the snoop response.

• If a single Manager can issue transactions with multiple NSAID values, it must ensure that internal accesses to cached copies use the NSAID value that was used to fetch the cache line initially:

– An access that has a cache line hit with the same address, but a different NSAID value, must clean and invalidate the cache line before refetching the cache line with the appropriate NSAID value. This process ensures that a protection check is performed.

– If it is guaranteed that the Manager never accesses the same cache line with a different NSAID value, clean and invalidation operations are not necessary. This guarantee can be by design or be assured by using appropriate cache maintenance operations.

• Appropriate cache maintenance must be performed when changing the access permissions for NSAID values.

It is permitted for a Manager to write to a cache line when that agent does not have write permission to the location. It is also permitted for the updated cache line to be passed to other Managers using the same NSAID value. However, it is not permitted for the update to propagate to main memory or to an access using a different NSAID value.

## A10.2 Page-based Hardware Attributes (PBHA)

Page-based hardware attributes (PBHA) are 4-bit descriptors associated with a translation table entry that can be annotated onto a transaction request.

This specification describes how they can be transported but their use is IMPLEMENTATION DEFINED.

The following signals are used on the read and write request channels to transfer PBHA values.

Table A10.3: AxPBHA signals
<table><tr><td>Name</td><td>Width</td><td>Default Description</td><td></td></tr><tr><td>AWPBHA, ARPBHA</td><td>4</td><td></td><td>A 4b user-defined descriptor associated with a translation table entry that can be annotated onto a transaction request.</td></tr></table>

The PBHA\_Support property is used to indicate whether an interface supports PBHA.

Table A10.4: PBHA\_Support property
<table><tr><td>PBHA_Support Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>PBHA is supported. AWPBHA and ARPBHA are present on the interface.</td></tr><tr><td>False</td><td>Y</td><td>PBHA is not supported.</td></tr></table>

## A10.2.1 PBHA values

PBHA values can be added to the request during address translation and propagated through a system if they are supported by downstream components. At the MMU, all transactions to the same page and physical address space are likely to have the same value but accuracy of PBHA values might be degraded as they pass through the system.

Examples of where PBHA values might become inaccurate are:

• When an interconnect is combining transactions from different sources, some might have PBHA values attached, and others might take a fixed value.

• In a downstream cache, PBHA values might not be cached along with the data in all cases.

• In the case that PBHA values in translation tables are changed, values on in-flight transactions or cached data could become inconsistent. Appropriate TLB Invalidate or cache maintenance operations could be used to achieve consistency.

This list is not exhaustive, designers are encouraged to document situations where PBHA can become inaccurate within their component. A system integrator wanting to use PBHA must consider every component between the source and target to determine the requirements of the target can be met.

## A10.3 Subsystem Identifier

The Subsystem Identifier (ID) is a field that can be added to transaction requests to indicate from which subsystem they originate. The Subsystem ID can be used to qualify the transaction address and provide isolation between parts of a system when they share memory or devices.

The signals used to transfer the Subsystem ID are shown in Table A10.5.

Table A10.5: AxSUBSYSID signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWSUBSYSID,</td><td>SUBSYSID_WIDTH</td><td></td><td>Subsystem identifier that indicates from which</td></tr><tr><td>ARSUBSYSID</td><td></td><td></td><td>subsystem a request originates.</td></tr></table>

The SUBSYSID\_WIDTH property is used to define the width and presence of the Subsystem ID signals. If the property is zero, the signals are not present.

Table A10.6: SUBSYSID\_WIDTH property
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>SUBSYSID_WIDTH</td><td>0..8</td><td>0</td><td>Width of AWSUBSYSID and ARSUBSYSID in bits.</td></tr></table>

## A10.3.1 Subsystem ID usage

This specification does not define the usage of Subsystem IDs.

Example implementations include:

• A Manager or group of Managers using a single Subsystem ID where they have common access rights to shared memory or peripherals.

• An interconnect combining requests from Managers in different subsystems. In this case, the interconnect Manager interface therefore uses different Subsystem IDs for different requests.

• Using the Subsystem ID as a look-up in a firewall or Memory Protection Unit (MPU) to isolate subsystems for safety or security reasons.

• Requiring that all Managers within a coherent domain use the same Subsystem ID, so it can be used in snoop filtering.

• Using Subsystem ID for performance profiling or monitoring.

• An interconnect that propagates Subsystem ID through some interfaces and not others.

## A10.4 Arm Compression Technology (ACT)

Arm Compression Technology (ACT) is a block-based compression technology that allows data compression and decompression with a minimum of state. This enables the codec hardware to be separate from the components using the data, and a single codec to be shared between multiple agents.

When using ACT, a Manager generates loads and stores of uncompressed data that are routed by the interconnect to the ACT codec. The ACT codec performs the compression/decompression and generates any required memory transactions to the compressed data in memory. The codec uses information carried in the ACT payload of the request to perform the correct compression or decompression.

This feature extends AXI5 interfaces with signals to indicate ACT transactions and carry the ACT payload between a Manager and external codec.

The ACT\_Support property determines whether an interface supports Arm Compression Technology signaling.

Table A10.7: ACT\_Support property
<table><tr><td>ACT_Support Default Description</td><td></td><td></td></tr><tr><td>v1</td><td></td><td>ACT is supported, ACT signals are present</td></tr><tr><td>False</td><td>Y</td><td>ACT is not supported, ACT signals are not present.</td></tr></table>

The ACT\_Support property can be True for the following interface classes:

• AXI5

When ACT\_Support is v1:

• The ACT signals are present, see Table A10.9.

• WriteACT and ReadACT transactions are supported.

• The data bus width (DATA\_WIDTH) must be 128b or larger.

• Untranslated\_Transactions must not be False, because ACT transactions are to virtual addresses.

When connecting Manager and Subordinate interfaces, the ACT\_Support property must be compatible as shown in Table A10.8.

Table A10.8: ACT\_Support property compatibility
<table><tr><td></td><td>Subordinate: False</td><td>Subordinate: v1</td></tr><tr><td>Manager: False</td><td>Compatible</td><td>Compatible. AxACTV inputs tied LOW.</td></tr><tr><td>Manager: v1</td><td>Not compatible</td><td>Compatible</td></tr></table>

## A10.4.1 ACT signaling

The following signals are required to support ACT.

Table A10.9: ACT signals
<table><tr><td>Signal</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWACTV</td><td>1</td><td>0b0</td><td>Asserted HIGH to indicate that this is a WriteACT request and AWACT contains a valid payload.</td></tr><tr><td>AWACT</td><td>ACT_W_WIDTH</td><td>All zeros</td><td>ACT payload on the write request channel.</td></tr><tr><td>ARACTV</td><td>1</td><td>0b0</td><td>Asserted HIGH to indicate that this is a ReadACT request and ARACT contains a valid payload.</td></tr><tr><td>ARACT</td><td>ACT_R_WIDTH</td><td>All zeros</td><td>ACT payload on the read request channel.</td></tr></table>

The properties that define the width of the ACT payload are shown in Table A10.10.

Table A10.10: ACT width properties
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>ACT_W_WIDTH</td><td>0,16..32</td><td>0</td><td>Width of AWACT in bits.</td></tr><tr><td>ACT_R_WIDTH</td><td>0,16..32</td><td>0</td><td>Width of ARACT in bits.</td></tr></table>

The following rules apply to the ACT signal widths:

• If ACT\_W\_WIDTH is 0, AWACT and AWACTV are not present.

• If ACT\_R\_WIDTH is 0, ARACT and ARACTV are not present.

• If ACT\_Support is False, ACT\_W\_WIDTH and ACT\_R\_WIDTH must be 0.

## A10.4.2 ACT requests

A WriteACT request is signaled by setting AWSNOOP to 0x0 and AWACTV to 0b1.

• When AWACTV is HIGH, AWSNOOP must be 0x0.

A ReadACT request is signaled by setting ARSNOOP to 0x0 and ARACTV to 0b1.

• When ARACTV is HIGH, ARSNOOP must be 0x0.

WriteACT and ReadACT requests have the following constraints:

• Burst is INCR.

• AxCACHE is Device transaction.

• Domain is System.

• Size is the same as the data bus width if Length is greater than 1 transfer.

• AxADDR[13:0] is zero.

• For writes, all write strobes within the transaction container must be asserted.

• AxLOCK is Normal.

• TagOp is Invalid.

• ID is unique-in-flight, which means:

– An ACT read request can only be issued if there are no outstanding transactions on the read channels with the same ID.

– An ACT write request can only be issued if there are no outstanding transactions on the write channels with the same ID.

– A request must not be issued on the read channels with the same ID as an outstanding ACT read request.

– A request must not be issued on the write channels with the same ID as an outstanding ACT write request.

– If present, AxIDUNQ must be asserted.

## A10.4.3 Modifying ACT transactions

Transactions using ACT have a Non-modifiable memory attribute, which means there are limitations regarding which signals can be modified as the transaction progresses through a system.

The AXI specification permits Non-modifiable transactions to have their Size and Length changed in the following circumstances:

• If Length is greater than 16, but that is not supported by a Subordinate interface. In this case, a transaction is split into multiple smaller transactions.

• If the transaction is transported across an interconnect link with data width smaller than that of the request.

The ACT payload associated with a transaction is specific to the Size and Length of that transaction, so an ACT transaction must never have its Size or Length changed. This might limit the topology of subsystems transporting ACT transactions.

# Chapter A11 Other write transactions

This chapter describes additional write transactions supported in the AXI protocol.

It contains the following sections:

• A11.1 WriteZero Transaction

• A11.2 WriteDeferrable Transaction

## A11.1 WriteZero Transaction

Many writes in a system, particularly from a CPU, have data set to zero. For example, while initializing or allocating memory. These writes with a zero value consume write data bandwidth and interconnect power that can be saved by using a data-less request.

The WriteZero transaction is used to write zero values to a cache line sized data location. The transaction consists of a write request and write response but has no associated write data transfer. It is functionally equivalent to a regular write to the same location with fully populated data lanes where all data has a value of zero.

The WriteZero\_Transaction property is used to indicate whether an interface supports the WriteZero transaction.

Table A11.1: WriteZero\_Transaction property
<table><tr><td>WriteZero_Transaction Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>WriteZero is supported.</td></tr><tr><td>False</td><td>Y</td><td>WriteZero is not supported.</td></tr></table>

The rules for a WriteZero transaction are:

• A WriteZero request indicates that the data at the locations indicated by address, size, and length attributes must be set to zero.

• A WriteZero transaction consists of a request on the AW channel and a single response on the B channel.

• A WriteZero transaction is cache line sized and Regular, see A3.1.8 Regular transactions

• AWSNOOP must be 0b0111 or 0b00111.

• AWLOCK must be 0b0, not exclusive access.

• AWTAGOP must be Invalid.

• AWID must be unique-in-flight, which means:

– A WriteZero transaction can only be issued if there are no outstanding write transactions using the same AWID value.

– A Manager must not issue a request on the write channel with the same AWID as an outstanding WriteZero transaction.

– If present, AWIDUNQ must be asserted for a WriteZero transaction.

• AWDOMAIN can take any value. If the Domain is Shareable, a WriteZero acts as a WriteUniqueFull with zero as data.

• A Manager that issues WriteZero requests cannot be connected to a Subordinate that does not support WriteZero.

## A11.2 WriteDeferrable Transaction

In enterprise systems, accelerators are commonly used that are accessed across chip-to-chip connections using a 64-byte atomic store operation. These store operations are performed to shared queues within the accelerator. In some cases, it is possible that the store will not be accepted because the queue is full but might be accepted if retried later. This type of transaction is known as a WriteDeferrable.

PCIe Gen5 includes support for a deferrable write through the Deferrable Memory Write (DMWr) transaction. This requires a write response, so the DMWr is a non-posted Write. It is expected that a WriteDeferrable transaction in AXI translates to a PCIe DMWr transaction.

## A11.2.1 WriteDeferrable transaction support

The WriteDeferrable\_Transaction property is used to indicate whether an interface supports the WriteDeferrable transaction.

Table A11.2: WriteDeferrable\_Transaction property
<table><tr><td>WriteDeferrable_Transaction Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>WriteDeferrable is supported.</td></tr><tr><td>False</td><td>Y</td><td>WriteDeferrable is not supported.</td></tr></table>

A Manager that issues WriteDeferrable requests cannot be connected to a Subordinate that does not support WriteDeferrable.

## A11.2.2 WriteDeferrable signaling

When the WriteDeferrable\_Transaction property is True, AWSNOOP and BRESP must be wide enough to accommodate additional encodings:

• AWSNOOP\_WIDTH must be 5.

• BRESP\_WIDTH must be 3.

A WriteDeferrable transaction consists of a request, 64-bytes of write data and a write response.

The rules for a WriteDeferrable transaction are:

• AWSNOOP is 0b10000.

• AWDOMAIN is 0b11 (System shareable).

• AWCACHE is Device or Normal Non-cacheable.

• Legal combinations of Length x Size are:

– 1 x 64-bytes

– 2 x 32-bytes

– 4 x 16-bytes

– 8 x 8-bytes

– 16 x 4-bytes

• All bits of WSTRB must be set within the 64-byte container.

• AWADDR is aligned to 64-bytes.

• AWBURST is INCR.

• AWLOCK is deasserted, not exclusive access.

• AWATOP is Non-atomic transaction.

• AWTAGOP is Invalid.

• The ID is unique-in-flight for all transactions, which means:

– A WriteDeferrable transaction can only be issued if there are no outstanding transactions on the write channels with the same ID value.

– A Manager must not issue a request on the write channels with the same ID as an outstanding WriteDeferrable transaction.

– If present, AWIDUNQ must be asserted for a WriteDeferrable transaction.

• A WriteDeferrable transaction must be treated as 64-byte atomic, therefore:

– It must only be to locations which have a single-copy atomicity size of 64-bytes or greater.

– The request must not be split or merged with other transactions.

## A11.2.3 Response to a WriteDeferrable request

Table A11.3 shows the meanings for the response to a WriteDeferrable request.

Table A11.3: WriteDeferrable response meanings
<table><tr><td>BRESP[2:0]</td><td>Response</td><td>Indication</td></tr><tr><td>0b000</td><td>OKAY</td><td>The write was accepted by a Subordinate that supports WriteDeferrable transactions and was successful.</td></tr><tr><td>0b001</td><td>EXOKAY</td><td>Not a permitted response to WriteDeferrable.</td></tr><tr><td>0b010</td><td>SLVERR</td><td>Write has reached an end point but has been unsuccessful.</td></tr><tr><td>0b011</td><td>DECERR</td><td>Write has not reached a point where data can be written.</td></tr><tr><td>0b100</td><td>DEFER</td><td>Write was unsuccessful because it cannot be serviced at this time but might be successful if resent later. The location is not updated. This response is only permitted for a WriteDeferrable transaction.</td></tr><tr><td>0b101</td><td>TRANSFAULT</td><td>Write was terminated because of a translation fault which might be resolved by a PRI request. This response is only permitted if AWMMUFLOW is PRI.</td></tr><tr><td>0b110</td><td>RESERVED</td><td></td></tr><tr><td>0b111</td><td>UNSUPPORTED</td><td>Write was unsuccessful because the transaction type is not supported by the target. The location is not updated. This response is only permitted for a WriteDeferrable transaction.</td></tr></table>

If an interconnect detects that a WriteDeferrable is targeting a Subordinate that does not support WriteDeferrable transactions, it must not propagate the request.

In this case, it is expected that an UNSUPPORTED response is sent, but SLVERR or DECERR are also permitted.

A Subordinate interface that can recognize a WriteDeferrable but cannot process it, has the WriteDeferrable\_Transaction property True but is expected to respond with UNSUPPORTED.

# Chapter A12 System monitoring, debug, and user extensions

This chapter describes the AXI features for system monitoring and debug. It also describes how to add user-defined extensions to each channel.

It contains the following sections:

• A12.1 Memory System Resource Partitioning and Monitoring (MPAM)

• A12.2 Memory Tagging Extension (MTE)

• A12.3 Trace signals

• A12.4 User Loopback signaling

• A12.5 User defined signaling

## A12.1 Memory System Resource Partitioning and Monitoring (MPAM)

Memory System Resource Partitioning and Monitoring (MPAM) is a technology for partitioning and monitoring memory system resources for physical and virtual machines. The full MPAM architecture is described in the Armv8.4 extensions [6].

Each MPAM-enabled Manager adds MPAM information to its requests. The MPAM information is propagated through the system to memory components where it can be used to influence resource allocation decisions. Monitoring memory usage based on MPAM information can also enable the tuning of performance and accurate costing between machines.

## A12.1.1 MPAM signaling

The MPAM\_Support property as shown in Table A12.1 is used to indicate whether an interface supports MPAM.

Table A12.1: MPAM\_Support property
<table><tr><td>MPAM_Support</td><td>Default</td><td>Description</td></tr><tr><td>MPAM_12_1</td><td></td><td>The interface is enabled for MPAM and includes the MPAM signals on AW and AR channels. The width of PARTID is 12 and PMG is 1.</td></tr><tr><td>MPAM_9_1</td><td></td><td>The interface is enabled for MPAM and includes the MPAM signals on AW and AR channels. The width of PARTID is 9 and PMG is 1.</td></tr><tr><td>False</td><td>Y</td><td>MPAM is not supported, the interface is not MPAM enabled and no MPAM signals are present on the interface.</td></tr></table>

The signals used to support MPAM are shown in Table A12.2.

Table A12.2: AxMPAM signals

<table><tr><td>Name</td><td>Width</td><td>Default </td><td>Description</td></tr><tr><td>AWMPAM,</td><td>MPAM_WIDTH</td><td></td><td>Memory System Resource Partitioning and</td></tr><tr><td>ARMPAM</td><td></td><td></td><td>Monitoring (MPAM) information for a request.</td></tr><tr><td></td><td></td><td></td><td></td></tr></table>

The value of MPAM\_WIDTH is determined by the MPAM\_Support and RME\_Support properties.   
When MPAM\_Support is False, MPAM\_WIDTH must be zero.

## A12.1.2 MPAM fields

MPAM fields are encoded within the AxMPAM signals depending on the MPAM\_Support and RME\_Support properties.

When MPAM\_Support is MPAM\_9\_1 and RME\_Support is False, MPAM\_WIDTH must be 11 and the mapping is shown in Table A12.3.

Table A12.3: MPAM\_9\_1 fields when RME\_Support is False
<table><tr><td>Field</td><td>Description</td><td>Width</td><td>Mapping</td></tr><tr><td>MPAM_NS</td><td>Security indicator</td><td>1</td><td>AxMPAM[0]</td></tr><tr><td>PARTID</td><td>Partition identifier</td><td>9</td><td>AxMPAM[9:1]</td></tr><tr><td>PMG</td><td>Performance monitor group</td><td>1</td><td>AxMPAM[10]</td></tr></table>

When MPAM\_Support is MPAM\_9\_1 and RME\_Support is True, MPAM\_WIDTH must be 12 and the mapping is shown in Table A12.4.

Table A12.4: MPAM\_9\_1 fields when RME\_Support is True
<table><tr><td>Field</td><td>Description</td><td>Width</td><td>Mapping</td></tr><tr><td>MPAM_SP</td><td>Physical address space indicator</td><td>2</td><td>AxMPAM[1:0]</td></tr><tr><td>PARTID</td><td>Partition identifier</td><td>9</td><td>AxMPAM[10:2]</td></tr><tr><td>PMG</td><td>Performance monitor group</td><td>1</td><td>AxMPAM[11]</td></tr></table>

When MPAM\_Support is MPAM\_12\_1 and RME\_Support is False, MPAM\_WIDTH must be 14 and the mapping is shown in Table A12.5.

Table A12.5: MPAM\_12\_1 fields when RME\_Support is False
<table><tr><td>Field</td><td>Description</td><td>Width</td><td>Mapping</td></tr><tr><td>MPAM_NS</td><td>Security indicator</td><td>1</td><td>AxMPAM[0]</td></tr><tr><td>PARTID</td><td>Partition identifier</td><td>12</td><td>AxMPAM[12:1]</td></tr><tr><td>PMG</td><td>Performance monitor group</td><td>1</td><td>AxMPAM[13]</td></tr></table>

When MPAM\_Support is MPAM\_12\_1 and RME\_Support is True, MPAM\_WIDTH must be 15 and the mapping is shown in Table A12.6.

Table A12.6: MPAM\_12\_1 fields when RME\_Support is True
<table><tr><td>Field</td><td>Description</td><td>Width</td><td>Mapping</td></tr><tr><td>MPAM_SP</td><td>Physical address space indicator</td><td>2</td><td>AxMPAM[1:0]</td></tr><tr><td>PARTID</td><td>Partition identifier</td><td>12</td><td>AxMPAM[13:2]</td></tr><tr><td>PMG</td><td>Performance monitor group</td><td>1</td><td>AxMPAM[14]</td></tr></table>

## A12.1.3 MPAM component interactions

Implementation of MPAM technology has impacts on Manager, Interconnect, and Subordinate components.

If a Manager component is included in an MPAM-enabled system, but does not support MPAM signaling, then the system must add the MPAM information. The default behavior is IMPLEMENTATION DEFINED; one possible approach is to copy the physical address space of the request onto the least significant MPAM bits and zero-extend the remaining higher bits.

## Manager components

Manager components that are MPAM-enabled must drive MPAM signals when the corresponding AxVALID is asserted. Values used are IMPLEMENTATION DEFINED for all transaction types. It is expected, but not required, that a Manager uses the same sets of values for read and write requests. A Manager might not use all the PARTID or PMG values that can be signaled on the interface.

## Interconnect components

MPAM identifiers have global scope. There is no requirement for interconnect components to make MPAM identifiers unique. When an interconnect Manager interface is connected to an MPAM-enabled Subordinate, it can use propagated values or IMPLEMENTATION DEFINED values.

## Subordinate components

A Subordinate component that is MPAM-enabled can use the MPAM information for memory partitioning and monitoring. MPAM signals are sampled when the corresponding AxVALID is asserted.

## A12.2 Memory Tagging Extension (MTE)

The Memory Tagging Extension (MTE) provides a mechanism that can be used to detect memory safety violations.

When a region of memory is allocated for a particular use, it is given an Allocation Tag value. When the memory is subsequently accessed, a Physical Tag value is provided that corresponds to the physical address of the access. If the Physical Tag does not match with the Allocation Tag, a warning is generated.

Allocation Tags are stored in the memory system and can be cached in the same way as data. Each tag is 4 bits and is associated with a 16-byte aligned address location.

The following operations are supported:

• Updating the Allocation Tag value using a write transaction, with or without updating the associated data value.

• Reading of data with associated Allocation tag. The Requestor can then perform the check of Physical Tag against the Allocation Tag.

• Writing to memory with a Physical Tag to be compared with the Allocation Tag. The result is indicated in the transaction response.

When memory tagging is supported in a system, it is not required that every transaction uses memory tagging. It is also not required that every component in the system supports memory tagging.

The Memory Tagging Extension is supported on Arm A-profile architecture v8.5 onwards and is described in the Arm® Architecture Reference Manualfor A-profile architecture [3].

## A12.2.1 MTE support

The MTE\_Support property of an interface is used to indicate the level of support for MTE. There are different levels of support that can be used, depending on the use-case.

Table A12.7: MTE\_Support property
<table><tr><td></td><td>MTE_Support Default Description</td><td></td></tr><tr><td>Standard</td><td></td><td>Memory tagging is fully supported on the interface, all MTE signals are present.</td></tr><tr><td>Simplified</td><td></td><td>All memory tagging operations are supported except MTE Match. Partial tag writes are not permitted, so when AWTAGOP is Update, all WTAGUPDATE bits that correspond to the tags inside the transaction container must be asserted. BTAGMATCH is not present. BCOMP is not required.</td></tr><tr><td>Basic</td><td></td><td>Memory tagging is supported on the interface at a basic level. A limited set of tag operations are permitted. BTAGMATCH is not present. BCOMP is not required.</td></tr><tr><td>False</td><td>Y</td><td>Memory tagging is not supported on the interface and no MTE signals are present.</td></tr></table>

MTE\_Support must be False when:

• DATA\_WIDTH is 32 or smaller.

• Untranslated\_Transactions is True, v1 or v2.

The compatibility between Manager and Subordinate interfaces, according to the values of the MTE\_Support property is shown in Table A12.8.

Table A12.8: MTE\_Support
<table><tr><td></td><td>Subordinate: False</td><td>Subordinate: Basic</td><td>Subordinate: Simplified</td><td>Subordinate: Standard</td></tr><tr><td>Manager: False</td><td>Compatible.</td><td>Compatible.</td><td>Compatible.</td><td>Compatible.</td></tr><tr><td>Manager: Basic</td><td>Protocol compliant. The Subordinate ignores AxTAGOP, so write tags are lost and read tag values are static.</td><td>Compatible.</td><td>Compatible.</td><td>Compatible.</td></tr><tr><td>Manager: Simplified</td><td>Protocol compliant. The Subordinate ignores AxTAGOP, so write tags are lost and read tag values are static.</td><td>Not compatible.</td><td>Compatible.</td><td>Compatible.</td></tr><tr><td>Manager: Standard</td><td>Not compatible.</td><td>Not compatible.</td><td>Not compatible.</td><td>Compatible.</td></tr></table>

## A12.2.2 MTE signaling

The signals required to support MTE are shown in Table A12.9.

Table A12.9: MTE signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWTAGOP</td><td>2</td><td>0b00 (Invalid)</td><td>Indicates if MTE tags are associated with a write transaction.</td></tr><tr><td>ARTAGOP</td><td>2</td><td>0b00 (Invalid)</td><td>Indicates if MTE tags are requested with a read transaction.</td></tr><tr><td>WTAG, RTAG</td><td>ceil(DATA WIDTH/128)*4</td><td></td><td>Memory tag associated with data. There is a 4-bit tag per 128-bits of data, with a minimum of 4-bits. It has the same validity rules as the associated data. It is recommended that invalid tags are driven to zero</td></tr><tr><td>WTAGUPDATE</td><td>ceil(DATA_WIDTH/128)</td><td></td><td>Indicates which tags must be written to memory when AWTAGOP is Update. There is 1 bit per 4 bits of tag.</td></tr><tr><td>BTAGMATCH</td><td>2</td><td></td><td>Indicates the result of a tag comparison on a write transaction.</td></tr><tr><td>BCOMP</td><td>1</td><td>0b1</td><td>Asserted HIGH to indicate a Completion response.</td></tr></table>

## A12.2.3 Caching tags

Allocation Tags that are cached must be kept hardware-coherent. The coherence mechanism is the same as for data. Applicable tag cache states are: Invalid, Clean, and Dirty. A line that is either Clean or Dirty is Valid.

Constraints on the combination of data cache state and tag cache state are:

• Tags can be Valid only when data is Valid.

• Tags can be Invalid when data is Valid.

• When a cached line is evicted and tags are Dirty, then it is permitted to treat clean data that is evicted as dirty.

• When Dirty tags are evicted from a cache, they must be either written back to memory or passed dirty to another cache.

• When Clean tags are evicted from a cache, they can be sent to other caches or dropped silently.

• A CMO which hits a line with Valid tags applies to the data and the tag.

• When a MakeInvalid or ROMI transaction hits a line with dirty tags, the tags must be written back to memory.

## A12.2.4 Transporting tags

Tag values are transported using the WTAG signal when AWTAGOP is not Invalid.

Tag values are transported using the RTAG signal when ARTAGOP is not Invalid.

When transporting tags, the following rules apply in addition to other constraints based on the transaction type:

• The transaction must be cache line sized or smaller and not cross a cache line boundary.

• AxADDR must be a physical address, therefore AxMMUVALID must be LOW if present.

• AxBURST must be INCR or WRAP, not FIXED.

• The transaction must be to Normal Write-Back memory, which means:

– The CACHE\_Present property must be True.

– AxCACHE[3:2] is not 0b00.

– AxCACHE[1:0] is 0b11.

• The ID value must be unique-in-flight, which means:

– A read with tag Transfer or Fetch can only be issued if there are no outstanding read transactions using the same ARID value.

– A Manager must not issue a request on the read channel with the same ARID as an outstanding read with tag Transfer or Fetch.

– If present, ARIDUNQ must be asserted for a read with tag Transfer or Fetch.

– A write with tag Transfer, Update or Match can only be issued if there are no outstanding write transactions using the same AWID value.

– A Manager must not issue a request on the write channel with the same AWID as an outstanding write with tag Transfer, Update, or Match.

– If present, AWIDUNQ must be asserted for a write with tag operations Transfer, Update, or Match.

• The memory tag is transported on RTAG or WTAG, where TAG[4n-1:4(n-1)] corresponds to DATA[128n-1:128(n-1)].

• For data widths wider than 128 bits, the tag signal carries multiple tags. The tags are driven appropriate to the data being transported, with the least significant tag bits used to transport the tag for the least significant 128 bits of data.

• For read transactions that use read data chunking, only tags which correspond to valid chunk strobes are required to be valid.

• For write transactions where multiple transfers address the same tag, WTAG and WTAGUPDATE values must be consistent for each 4-bit tag that is accessed by the transaction.

## A12.2.5 Reads with tags

A read can request that Allocation Tags are returned along with data, which is determined by the value of ARTAGOP, as shown in Table A12.10.

Table A12.10: ARTAGOP encodings
<table><tr><td>ARTAGOP</td><td>Operation Meaning</td><td></td></tr><tr><td>0b00</td><td>Invalid</td><td>Tags are not required to be returned with the data. In the response to this request, RTAG is invalid and must be zero.</td></tr><tr><td>0b01</td><td>Transfer</td><td>Each transfer of read data must have a valid tag value. Tags must be sent for every 16-byte granule that is accessed, even if the address is not aligned to 16 bytes.</td></tr><tr><td>0b10</td><td>RESERVED</td><td></td></tr><tr><td>0b11</td><td>Fetch</td><td>Only tags are required to be fetched. Data is not required to be valid and must not be used by the Manager. Transactions using Fetch must be cache line sized and Regular. Tags must be sent for every 16-byte granule that is accessed.</td></tr></table>

There are limitations on which read channel Opcodes can be used with MTE tag transfer. Table A12.11 shows the combinations of Opcode and TagOp that are legal for each configuration of MTE\_Support.

A TagOp encoding of Invalid is legal for all Opcodes.

An asterisk (\*) indicates all variants of the Opcode.

Table A12.11: Legal tag operations for read transactions
<table><tr><td rowspan="2">Opcode</td><td colspan="2">MTE_Support = Basic</td><td colspan="2">MTE_Support = Simplified</td><td colspan="2">MTE_Support = Standard</td></tr><tr><td>Transfer</td><td>Fetch</td><td>Transfer</td><td>Fetch</td><td>Transfer</td><td>Fetch</td></tr><tr><td>ReadNoSnoop</td><td>Y</td><td></td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>ReadOnce</td><td>Y</td><td>1</td><td>Y</td><td>1</td><td>Y</td><td>1</td></tr><tr><td>ReadShared</td><td>Y</td><td>1</td><td>Y</td><td>1</td><td>Y</td><td>1</td></tr><tr><td>ReadClean</td><td>Y</td><td></td><td>Y</td><td>-</td><td>Y</td><td>1</td></tr><tr><td>ReadOnceCleanInvalid</td><td>1</td><td></td><td>1</td><td></td><td>1</td><td></td></tr><tr><td>ReadOnceMakeInvalid</td><td>1</td><td></td><td>1</td><td>1</td><td>1</td><td></td></tr><tr><td>CleanInvalid*</td><td>I</td><td>1</td><td>1</td><td>I</td><td>1</td><td></td></tr><tr><td>CleanShared*</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>MakeInvalid</td><td>I</td><td></td><td>1</td><td>1</td><td>-</td><td>1</td></tr><tr><td>DVM Complete</td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>

## A12.2.6 Writes with tags

A write can request that Allocation Tags are written along with data or that the write includes a Physical Tag which is compared with the Allocation Tag already stored in memory. The signal AWTAGOP indicates the tag operation to be performed.

Table A12.12: AWTAGOP encodings
<table><tr><td>AWTAGOP</td><td>Operation</td><td>Meaning</td></tr><tr><td rowspan="2">0b00</td><td>Invalid</td><td>The tags are not valid; no tag updating or checking is required.</td></tr><tr><td></td><td>WTAGUPDATE must be deasserted. WTAG must be zero.</td></tr><tr><td rowspan="2">0b01</td><td rowspan="2">Transfer</td><td>The tags are Clean. Tag check does not need to be performed. The completer of the write can cache the tags if it is allocating the data.</td></tr><tr><td>WTAGUPDATE must be deasserted. WTAG bits must be valid for every byte in the transaction container.</td></tr><tr><td rowspan="4">0b10</td><td>Update</td><td>Tag values have been updated and are dirty; the tags in memory must be updated, according to WTAGUPDATE. WTAGUPDATE can have any number of bits asserted, including none.</td></tr><tr><td></td><td>Tags that are only partially addressed in the transaction must have WTAGUPDATE deasserted. Write*Full* Opcodes must have all associated WTAGUPDATE bits asserted.</td></tr><tr><td></td><td>WTAG must be valid for every associated WTAGUPDATE bit that is asserted.</td></tr><tr><td>Match</td><td>The tags in the write must be checked against the Allocation Tag values that are obtained from memory. The Match operation must be performed for all tags where any corresponding write data strobes are asserted. It is required to update memory with the data, even if the match fails.</td></tr></table>

For a write with tag Update, WTAGUPDATE indicates which tags must be written. It has the following rules:

• WTAGUPDATE[n] corresponds to WTAG[4n+3:4n].

• If a bit is asserted, then the corresponding tags must be written to memory.

• If a bit is deasserted, then the corresponding tags are invalid.

• WTAGUPDATE bits outside of the transaction container must be deasserted.

• For operations other than Update, WTAGUPDATE must be deasserted.

• A tag-only write can be achieved by asserting WTAGUPDATE and deasserting WSTRB.

There are limitations on which write channel Opcodes can be used with MTE tag transfer. Table A12.13 shows the combinations of Opcode and TagOp that are legal for each configuration of MTE\_Support.

A TagOp encoding of Invalid is legal for all Opcodes.

An asterisk (\*) indicates all variants of the Opcode.

Table A12.13: Legal tag operations for write transactions
<table><tr><td rowspan="2">Opcode</td><td colspan="2">MTE_Support = Basic</td><td rowspan="2"></td><td colspan="2">MTE_Support = Simplified</td><td colspan="3">MTE_Support = Standard</td></tr><tr><td></td><td>Transfer Update Match</td><td>Transfer Update1</td><td>Match</td><td>Transfer</td><td>Update Match</td><td></td></tr><tr><td>WriteNoSnoop</td><td></td><td>Y</td><td></td><td>Y</td><td></td><td>Y</td><td>Y</td><td>Y2</td></tr><tr><td>WriteUnique*</td><td></td><td>Y</td><td>=</td><td>Y -</td><td></td><td>-</td><td>Y</td><td></td></tr><tr><td>WriteNoSnoopFull</td><td></td><td>Y</td><td>1</td><td>Y Y</td><td></td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>WriteBackFull</td><td></td><td>Y</td><td>一</td><td>Y Y</td><td></td><td>Y</td><td>Y</td><td></td></tr><tr><td>WriteEvictFull</td><td>Y</td><td></td><td></td><td>Y</td><td></td><td>Y</td><td></td><td></td></tr><tr><td>Atomic</td><td></td><td></td><td>一</td><td>1</td><td></td><td>一</td><td></td><td>Y</td></tr><tr><td>CMO</td><td></td><td></td><td></td><td>-</td><td></td><td>-</td><td></td><td></td></tr><tr><td>Write*CMO</td><td></td><td></td><td></td><td>Y3 Y</td><td></td><td>Y3</td><td>Y</td><td></td></tr><tr><td>WriteZero</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>WriteUnique*Stash</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>StashOnce*</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>StashTranslation</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Prefetch</td><td></td><td></td><td>I</td><td>Y</td><td></td><td>Y</td><td></td><td></td></tr><tr><td>WriteDeferrable</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>UnstashTranslation</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>InvalidateHint</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>

<sup>1</sup> Partial tag updates are not supported.

<sup>2</sup> Not Exclusive write.

<sup>3</sup> Domain must be Non-shareable.

Write transactions with a tag Match operation (AWTAGOP is 0b11) have two parts to the response:

• A Completion response, which indicates that the write is observable.

• A Match response, which indicates whether the tag comparison passes or fails.

A two-part response enables components with separate data and tag storage parts to respond independently. Response transfers can be sent in any order. The two parts can be optionally combined into a single response transfer.

The responses are signaled using BCOMP and BTAGMATCH. Table A12.14 shows the encodings for BTAGMATCH.

Table A12.14: BTAGMATCH encodings
<table><tr><td>BTAGMATCH</td><td>Operation</td><td>Meaning</td></tr><tr><td>0b00</td><td>None</td><td>No match result because not a match transaction</td></tr><tr><td>0b01</td><td>Separate</td><td>Match result is in a separate response transfer</td></tr><tr><td>0b10</td><td>Fail</td><td>Tags do not match</td></tr><tr><td>0b11</td><td>Pass</td><td>Tags match</td></tr></table>

## Completion response

The Completion response indicates that the write is observable. It has the following rules:

• BCOMP must be asserted.

• BTAGMATCH must be 0b01 (Match result in separate response).

• BID must have the same value as AWID.

• If Loopback signaling is supported, BLOOP must have the same value as AWLOOP.

• BRESP can take any value that is legal for the request Opcode.

• The Completion response must follow normal response ordering rules.

• The ID value can be reused when this response is received.

## Match response

The Match response indicates the result of the tag comparison on a write.

• If the tags match for every transfer of the entire transaction, then the response is Pass.

• If any tags associated with active write data byte lanes do not match those already stored, then the response is Fail.

A Match response has the following rules:

• BCOMP must be deasserted.

• BTAGMATCH must be 0b11 (Pass) or 0b10 (Fail).

• BID must have the same value as AWID.

• BIDUNQ can take any value, it is not required to have the same value as AWIDUNQ.

• BLOOP can take any value, it is not required to have the same value as AWLOOP.

• BRESP can take any value that is legal for the request Opcode.

• The Match response has no ordering requirements, it can overtake or be overtaken by any other response transfers.

## Combined response

A Subordinate can optionally combine the two responses into a single transfer. The following rules apply:

• BCOMP must be asserted.

• BTAGMATCH must be 0b11 (Pass) or 0b10 (Fail).

• BID must have the same value as AWID.

• If Loopback signaling is supported, BLOOP must have the same value as AWLOOP.

• BRESP can take any value that is legal for the request Opcode.

• The combined response must follow normal response ordering rules.

• The ID value can be reused when this response is received.

Possible responses to a Match operation are shown in Table A12.15.

Table A12.15: Possible responses to a Match operation
<table><tr><td>BTAGMATCH</td><td>BCOMP</td><td>Description</td></tr><tr><td>0b00</td><td>0b0</td><td>Not legal for a response to a request with tag Match.</td></tr><tr><td>0b00</td><td>0b1</td><td>Not legal for a response to a request with tag Match.</td></tr><tr><td>0b01</td><td>0b0</td><td>Not legal.</td></tr><tr><td>0b01</td><td>0b1</td><td>Completion response, part of a two-part response.</td></tr><tr><td>0b10</td><td>0b0</td><td>Match Fail, part of a two-part response.</td></tr><tr><td>0b10</td><td>0b1</td><td>Match Fail or MTE Match not supported, one-part response.</td></tr><tr><td>0b11</td><td>0b0</td><td>Match Pass, part of a two-part response.</td></tr><tr><td>0b11</td><td>0b1</td><td>Match Pass, one-part response.</td></tr></table>

## A12.2.7 Memory tagging interoperability

When an MTE operation is performed to a memory location that does not support memory tagging, the resultant data must be identical to that produced by a non-MTE operation to the same location.

• For a read with Transfer or Fetch, RTAG is recommended to be zero.

• For a write with Transfer or Update, the data must be written normally. The tag is discarded.

• For a write with Match, the data must be written normally and a single Combined response is given. BTAGMATCH must be 0b10 (Fail).

A Subordinate is expected to give an OKAY response to an MTE operation unless it would have given a different response to an equivalent non-MTE operation.

## A12.2.8 MTE and Atomic transactions

An Atomic transaction to a location that is protected with memory tagging can use a write Match operation.   
Atomic transactions cannot be used with Transfer or Update operations.

AtomicCompare transactions with Match can be 16 bytes or 32 bytes. If the transaction is 32 bytes, the same tag value must be used for tag bits associated with the compare and swap bytes.

Read data that is returned within an Atomic Transaction does not have valid RTAG values, so RTAG is recommended to be zero.

## A12.2.9 MTE and Prefetch transactions

A Prefetch transaction with AWTAGOP of Transfer indicates that the data should be prefetched with tags if possible. A Prefetch transaction has no write data, so no tag Transfer operation occurs within the transaction.

## A12.2.10 MTE and Poison

Section A16.1 Data protection using Poison discusses the concept of Poison associated with read and write data. There is no poison signaling directly associated with Allocation Tags. When writing a tag with poisoned data, the stored tag might be marked as poisoned.

The exact mechanism for this is IMPLEMENTATION DEFINED. Implementations might choose to do one of the following, but other implementations are possible.

• Poison associated with the data results in the tag being poisoned. Depending on the granularity of the poison associated with the tag, it may not be possible to clear the poison using the same techniques that would be used to clear poison associated with data.

• Poison associated with the data does not result in the tag being poisoned. This means that a corrupted tag might subsequently be used in an MTE Match operation, which could fail incorrectly. The rate at which this occurs should be significantly lower than the rate at which data corruption occurs.

• A combination of approaches may be employed, depending on the caching or storage structures in use.

## A12.3 Trace signals

An optional Trace signal can be associated with each channel to support the debugging, tracing, and performance measurement of systems.

The Trace\_Signals property is used to indicate whether a component supports Trace signals.

Table A12.16: Trace\_Signals property
<table><tr><td></td><td>Trace_Signals Default Description</td><td></td></tr><tr><td>True</td><td></td><td>Trace signals are included on all channels.</td></tr><tr><td>False</td><td>Y</td><td>Trace signals are not present.</td></tr></table>

The Trace signals associated with each channel are shown in Table A12.17. If the Trace\_Signals property is True, then the appropriate Trace signal must be present for all channels that are present.

Table A12.17: Trace signals

<table><tr><td>Name</td><td>Width Default</td><td>Description</td></tr><tr><td>AWTRACE</td><td>1</td><td>Trace signal associated with the write request channel.</td></tr><tr><td>WTRACE</td><td>1</td><td>Trace signal associated with the write data channel.</td></tr><tr><td>BTRACE</td><td>1</td><td>Trace signal associated with the write response channel.</td></tr><tr><td>ARTRACE</td><td>1</td><td>Trace signal associated with the read request channel.</td></tr><tr><td>RTRACE</td><td>1 一</td><td>Trace signal associated with the read data channel.</td></tr></table>

The exact use for Trace signals is not detailed in this specification, but it is expected that the use of Trace signaling is coordinated across the system and only one use of the Trace signaling occurs at a given time. Trace signal behavior is IMPLEMENTATION DEFINED, but the following recommendations are given:

• A Manager interface can assert the Trace signal along with the address of a transaction that should be tracked through the system.

• A component that provides a response to a transaction with the Trace signal asserted in the request provides a response with the Trace signal asserted.

• A component that provides a response to a transaction with the Trace signal deasserted in the request provides a response with the Trace signal deasserted.

• Components that pass-through transactions, preserve the Trace attribute of requests and responses.

• If a downstream component does not support Trace signals, an interconnect can assert Trace on the appropriate transfers.

• A Subordinate that receives a request with AWTRACE asserted should assert the BTRACE signal alongside the response.

• If an interface includes BCOMP, then BTRACE can take any value for responses with BCOMP deasserted.

• WTRACE should be propagated through interconnect components.

• A Subordinate that receives a request with the ARTRACE signal asserted should assert the RTRACE signal alongside every transfer of the read response.

• For Atomic transactions that require a response on the read channel, the RTRACE signal should be asserted if AWTRACE was asserted.

## A12.4 User Loopback signaling

User Loopback signaling permits an agent that is issuing requests to store information that is related to the transaction in an indexed table.

The transaction response can then use a fast table index to obtain the required information, rather than requiring a more complex lookup that uses the transaction ID.

The Loopback\_Signals property is used to indicate whether a component supports Loopback signals.

Table A12.18: Loopback\_Signals property
<table><tr><td>Loopback_Signals Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>Loopback signaling is supported.</td></tr><tr><td>False</td><td>Y</td><td>Loopback signaling is not supported.</td></tr></table>

The Loopback signals associated with each channel are shown in Table A12.19.

Table A12.19: Loopback signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWLOOP</td><td>LOOP_W_WIDTH</td><td>All zeros</td><td>A user-defined value that must be reflected from a write request to response transfers.</td></tr><tr><td>BLOOP</td><td>LOOP_W_WIDTH</td><td>All zeros</td><td>A user-defined value that is copied from the write request to write responses.</td></tr><tr><td>ARLOOP</td><td>LOOP_R_WIDTH</td><td>All zeros</td><td>A user-defined value that must be reflected from a read request to response and data transfers.</td></tr><tr><td>RLOOP</td><td>LOOP_R_WIDTH</td><td>All zeros</td><td>A user-defined value that is copied from the read request to response and data transfers.</td></tr></table>

The width of the Loopback signals is determined by the properties shown in Table A12.20. The maximum width is a recommendation.

Table A12.20: Loopback signal width properties
<table><tr><td>Name</td><td>Values</td><td>Default Description</td><td></td></tr><tr><td>LOOP_W_WIDTH</td><td>0..8</td><td></td><td>Loop signal width on write channels in bits, applies to AWLOOP and BLOOP.</td></tr><tr><td>LOOP_R_WIDTH</td><td>0..8</td><td></td><td>Loop signal width on read channels in bits, applies to ARLOOP and RLOOP.</td></tr></table>

The rules for the Loopback width properties are:

• If LOOP\_W\_WIDTH is 0, AWLOOP and BLOOP are not present.

• If LOOP\_R\_WIDTH is 0, ARLOOP and RLOOP are not present.

• If Loopback\_Signals is False, LOOP\_R\_WIDTH and LOOP\_W\_WIDTH must be 0.

• If Loopback\_Signals is True, LOOP\_W\_WIDTH or LOOP\_R\_WIDTH must be greater than 0.

The usage rules are:

• The value of BLOOP must be identical to the value that was on AWLOOP.

• If an interface includes BCOMP, then BLOOP can take any value for responses with BCOMP deasserted.

• The value of RLOOP must be identical to the value that was on ARLOOP for all read data transfers.

• For Atomic transactions that require a response on the read channel, the value of RLOOP must be identical to the value that was presented on AWLOOP. This means that the Manager must use loop values that can be signaled on both AWLOOP and RLOOP.

Loopback values are not required to be unique. Multiple outstanding transactions from the same Manager are permitted to use the same value.

It is not required that the Loopback value is preserved as a transaction progresses through a system. An intermediate component is permitted to store the Loopback value of a request it receives and use its own value for a request that it propagates downstream. When the component receives a response to the downstream transaction, it can retrieve the Loopback value for the original transaction.

## A12.5 User defined signaling

An AXI interface can include a set of user-defined signals, called User signals. The signals can be used to augment information to a transaction, where there is a requirement that is not covered by the existing AMBA specification. Information can be added to:

• A transaction request

• A transaction response

• Each transfer of read or write data within a transaction

Generally, it is recommended to avoid using User signals. The AXI protocol does not define the functions of these signals, which can lead to interoperability issues if two components use the same User signals in an incompatible manner.

## A12.5.1 Configuration

The presence and width of User signals is specified by the properties in Table A12.21:

Table A12.21: User signal properties
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>USER_REQ_WIDTH</td><td>0..128</td><td>0</td><td>Width of user extensions to a request in bits, applies to AWUSER and ARUSER.</td></tr><tr><td>USER_DATA_WIDTH</td><td>0..512</td><td>0</td><td>Width of user extensions to data in bits, applies to WUSER and RUSER.</td></tr><tr><td>USER_RESP_WIDTH</td><td>0..16</td><td>0</td><td>Width of user extensions to responses in bits, applies to BUSER and RUSER.</td></tr></table>

If a property has a value of zero, then the associated signals are not present on the interface.

The maximum signal widths are for guidance only, to set a reasonable maximum for configurable interfaces.

## A12.5.2 User signals

The user signals that can be added to each channel are shown in Table A12.22.

Table A12.22: User signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWUSER, ARUSER</td><td>USER_REQ_WIDTH</td><td>All zeros</td><td>User-defined extension to a request.</td></tr><tr><td>WUSER</td><td>USER_DATA_WIDTH</td><td>All zeros</td><td>User-defined extension to write data.</td></tr><tr><td>BUSER</td><td>USER_RESP_WIDTH</td><td>All zeros</td><td>User-defined extension to a write response.</td></tr><tr><td>RUSER</td><td>USER_DATA_WIDTH + USER_RESP_WIDTH</td><td>All zeros</td><td>User-defined extension to read data and response.</td></tr></table>

## A12.5.3 Usage considerations

Where User signals are implemented:

• The design decision regarding presence and width of User signals is made independently for request, data, and response channels.

• It is not required that values on request User signals are reflected on response User signals.

To assist with data width and protocol conversion, it is recommended that:

• USER\_DATA\_WIDTH is an integer multiple of the width of the data channels in bytes.

• User response bits are the same value for every transfer of a read or write response.

• The lower bits of RUSER are used to transport per-transaction response information.

• The upper bits of RUSER are used to transport per-transfer read data information.

# Chapter A13 Untranslated Transactions

This chapter describes how AXI supports the use of virtual addresses and translation stash hints for components upstream of a System Memory Management Unit (SMMU). It contains the following sections:

• A13.1 Introduction to Distributed Virtual Memory

• A13.2 Supportfor untranslated transactions

• A13.3 Untranslated transaction signaling

• A13.4 Translation identifiers

• A13.5 PCIe considerations

• A13.6 Translation fault flows

• A13.7 Untranslated transaction qualifier

• A13.8 Permitted combinations ofMMU signals and PAS

• A13.9 StashTranslation Opcode

• A13.10 UnstashTranslation Opcode

## A13.1 Introduction to Distributed Virtual Memory

An example system using Distributed Virtual Memory (DVM) is shown in Figure A13.1.

![](images/fa17af9df4332850379f91c44fa0018592041bf983411d759e35f430bc2475d1.jpg)  
Figure A13.1: Virtual memory system

In Figure A13.1, the System Memory Management Units (SMMUs) translate addresses in the virtual address space to addresses in the physical address space. Although all components in the system must use a single physical address space, SMMU components enable different Manager components to operate in their own independent virtual address or intermediate physical address space.

A typical process in the virtual memory system shown in Figure A13.1 might operate as follows:

1. A Manager component operating in a virtual address (VA) space issues a transaction that uses a VA.

2. The SMMU receives the VA for translation to a physical address (PA):

• If the SMMU has recently performed the requested translation, then it might obtain a cached copy of the translation from its TLB.

• Otherwise, the SMMU must perform a translation table walk, accessing translation table in memory to obtain the required VA to PA translation.

3. The SMMU uses the PA to issue the transaction for the requesting component.

At step 2 of this process, the translation for the required VA might not exist. In this case, the translation table walk generates a fault that must be notified to the agent that maintains the translation tables. For the required access to proceed, that agent must then provide the required VA to PA translation. Typically, it updates the translation tables with the required information.

Maintaining the translation tables can require changes to translation table entries that are cached in TLBs. To prevent the use of these entries, a DVM message can be used to issue a TLB invalidate operation.

After the translation tables have been updated and the necessary TLB invalidations have been performed, a DVM Sync transaction is used to ensure that all required transactions have completed.

Details of DVM messages used to maintain SMMUs can be found in Chapter A15 Distributed Virtual Memory messages.

## A13.2 Support for untranslated transactions

AXI supports the use of virtual addresses through the untranslated transactions extension.

The Untranslated\_Transactions property is used to indicate which version of untranslated transactions is supported by an interface.

Table A13.1: Untranslated\_Transactions property
<table><tr><td>Untranslated_Transactions Default Description</td><td></td><td></td></tr><tr><td>v4</td><td></td><td>Untranslated transactions version 4 is supported.</td></tr><tr><td>v3</td><td></td><td>Untranslated transactions version 3 is supported.</td></tr><tr><td>v2</td><td></td><td>Untranslated transactions version 2 is supported.</td></tr><tr><td>v1</td><td></td><td>Untranslated transactions version 1 is supported.</td></tr><tr><td>True</td><td></td><td>Untranslated transactions version 1 is supported.</td></tr><tr><td>False</td><td>Y</td><td>Untranslated transactions are not supported.</td></tr></table>

Address translation is the process of translating an input address to an output address based on address mapping and memory attribute information that is held in translation tables. This process permits agents in the system to use their own virtual address space, but ensures that the addresses for all transactions are eventually translated to a single physical address space for the entire system.

The use of a single physical address space is required for the correct operation of hardware coherency and therefore the SMMU functionality is typically located before a coherent interconnect.

The additional signals that are specified in this section provide sufficient information for an SMMU to determine the translation that is required for a particular transaction and permit different transactions on the same interface to use different translation schemes.

All signals in the Untranslated Transactions extension are prefixed with AWMMU for write transactions and ARMMU for read transactions.

In this specification, AxMMU indicates AWMMU or ARMMU.

## A13.3 Untranslated transaction signaling

The signals to support untranslated transactions are shown in Table A13.2. Each signal is described in following sections, including the property values which determine whether they are present.

Table A13.2: Signals for Untranslated Transactions
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWMMUSECSID, ARMMUSECSID</td><td>SECSID_WIDTH</td><td>0b00 (Non-secure)</td><td>Secure Stream Identifier for untranslated transactions.</td></tr><tr><td>AWMMUSID, ARMMUSID</td><td>SID_WIDTH</td><td>All zeros</td><td>Stream Identifier for untranslated transactions.</td></tr><tr><td>AWMMUSSIDV, ARMMUSSIDV</td><td>1</td><td>0b0</td><td>Asserted HIGH to indicate that a transaction has a valid substream identifier.</td></tr><tr><td>AWMMUSSID, ARMMUSSID</td><td>SSID_WIDTH</td><td>All zeros</td><td>Substream identifier for untranslated transactions.</td></tr><tr><td>AWMMUATST, ARMMUATST</td><td>1</td><td>0b0</td><td>Indicates that the transaction has already undergone PCIe ATS translation.</td></tr><tr><td>AWMMUFLOW, ARMMUFLOW</td><td>2</td><td>0b00 (Stall)</td><td>Indicates the SMMU flow for managing translation faults for this transaction.</td></tr><tr><td>AWMMUVALID, ARMMUVALID</td><td>1</td><td>0b1</td><td>MMU qualifier signal. When deasserted, the transaction address is a physical</td></tr><tr><td>AWMMUPM, ARMMUPM</td><td>1</td><td>0b0</td><td>address and does not require translation. Protected Mode indicator</td></tr><tr><td>AWMMUPASUNKNOWN, ARMMUPASUNKNOWN</td><td>1</td><td>0b0</td><td>HIGH to indicate that there is no PAS expectation</td></tr></table>

When Untranslated\_Transactions is v2 or higher, RRESP and BRESP are extended to 3-bits to accommodate the signaling of the TRANSFAULT response. See A3.3 Transaction response for encodings.

In Table A13.3 there is a summary of which MMU signals are present for which version of untranslated transactions.

• ‘Y’ indicates that the signal is mandatory.

• ‘C’ indicates that the presence is configurable.

• ‘-’ indicates that the signal must not be present.

Table A13.3: Signals in each version of untranslated transactions
<table><tr><td>Signals</td><td>Version 1</td><td>Version 2</td><td>Version 3</td><td>Version 4</td></tr><tr><td>AxMMUSECSID</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>AxMMUSID</td><td>C</td><td>C</td><td>C</td><td>C</td></tr><tr><td>AxMMUSSIDV</td><td>C</td><td>C</td><td>C</td><td>C</td></tr><tr><td>AxMMUSSID</td><td>C</td><td>C</td><td>C</td><td>C</td></tr><tr><td>AxMMUATST</td><td>C</td><td>-</td><td>1</td><td>1</td></tr><tr><td>AxMMUFLOW</td><td>1</td><td>C</td><td>C</td><td>C</td></tr><tr><td>AxMMUVALID</td><td>1</td><td>1</td><td>Y</td><td>Y</td></tr><tr><td>AxMMUPM</td><td>1</td><td>1</td><td>1</td><td>C</td></tr><tr><td>AxMMUPASUNKNOWN</td><td>I</td><td>-</td><td>-</td><td>C</td></tr></table>

## A13.4 Translation identifiers

Requests using virtual addressing can have up to three identifiers that are used during address translation:

• Secure Stream Identifier A13.4.1 Secure Stream Identifier (SECSID)

• Stream Identifier A13.4.2 StreamID (SID)

• Substream Identifier A13.4.3 SubstreamID (SSID)

During the building of a system, it is possible that the stream identifiers for a given component have some ID bits provided by the component and some ID bits that are tied off for that component. This fixes the range of values in the stream identifier name space that can be used by that component. Typically, the low-order bits are provided by the component and the high-order bits are tied off.

Any additional identifier field bits for AxMMUSID or AxMMUSSID, that are not supplied by the component or hard coded by the interconnect, must be tied LOW.

## A13.4.1 Secure Stream Identifier (SECSID)

The Secure Stream Identifier is used to indicate the virtual address space of the request. It is transported using the AxMMUSECSID signal, Table A13.4 shows the encodings.

Table A13.4: AxMMUSECSID encodings
<table><tr><td>AxMMUSECSID</td><td>Label</td><td>Meaning</td></tr><tr><td>0b00</td><td>Non-secure</td><td>Non-secure address space</td></tr><tr><td>0b01</td><td>Secure</td><td>Secure address space</td></tr><tr><td>0b10</td><td>Realm</td><td>Realm address space</td></tr><tr><td>0b11</td><td>RESERVED</td><td></td></tr></table>

The width of AxMMUSECSID is determined by the property SECSID\_WIDTH.

Table A13.5: SECSID\_WIDTH property
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>SECSID_WIDTH</td><td>0,1,2</td><td>0</td><td>Width of AWMMUSECSID and</td></tr><tr><td></td><td></td><td></td><td>ARMMUSECSID in bits.</td></tr></table>

The following rules apply:

• SECSID\_WIDTH must be 0 when Untranslated\_Transactions is False. AxMMUSECSID signals are not present.

• SECSID\_WIDTH must be 1 when Untranslated\_Transactions is not False and RME\_Support is False. Only Non-secure and Secure address spaces can be used.

• SECSID\_WIDTH must be 2 when Untranslated\_Transactions is not False and RME\_Support is True.

• When AxMMUSECSID is Non-secure, the physical address space must be Non-secure.

• When AxMMUSECSID is Secure, the physical address space must be Non-secure or Secure.

• When AxMMUSECSID is Realm, the physical address space must be Non-secure or Realm.

## A13.4.2 StreamID (SID)

The StreamID can be used to map a request to a translation context in the MMU. Each address space uses a different namespace, so they can have the same Stream Identifier values.

The width of AxMMUSID is determined by the property SID\_WIDTH.

Table A13.6: SID\_WIDTH property
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>SID_WIDTH</td><td>0..32</td><td>0</td><td>StreamID width in bits, applies to</td></tr><tr><td></td><td></td><td></td><td>AWMMUSID and ARMMUSID.</td></tr></table>

If SID\_WIDTH is 0, AxMMUSID signals are not present and the default value is used.

## A13.4.3 SubstreamID (SSID)

The SubstreamID can be used with requests that have the same StreamID to associate different application address translations to different logical blocks.

There is a separate enable signal AxMMUSSIDV for the SubstreamID, so a Manager can issue requests with or without a SubstreamID.

• When AxMMUSSIDV is deasserted, AxMMUSSID must be 0.

Note that a stream with a SubstreamID of 0 is different from a stream with no valid substream (AxMMUSSIDV is deasserted).

The width of AxMMUSSID is determined by the property SSID\_WIDTH.

Table A13.7: SSID\_WIDTH property
<table><tr><td>Name</td><td>Values</td><td>Default</td><td>Description</td></tr><tr><td>SSID_WIDTH</td><td>0..20</td><td>0</td><td>SubstreamID width in bits, applies to</td></tr><tr><td></td><td></td><td></td><td>AWMMUSSID and ARMMUSSID.</td></tr></table>

When SSID\_WIDTH is 0, AxMMUSSID and AxMMUSSIDV are not present on the interface and there are no valid SubstreamIDs.

## A13.4.4 Untranslated Transactions and GDI

When using untranslated transactions and GDI, the Untranslated\_Transactions property must be v4 and the following signals are included.

Table A13.8: AxMMUPM signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Presence</td><td>Description</td></tr><tr><td>AWMMUPM,</td><td>1</td><td>0</td><td>GDI_Support == True and</td><td>Protected Mode indicator</td></tr><tr><td>ARMMUPM</td><td></td><td></td><td>Untranslated_Transactions == v4</td><td></td></tr></table>

The Protected Mode (PM) indicator is used to indicate which address spaces the request is permitted to access. The following rules apply:

• AxMMUPM can only be asserted for requests with a Non-secure context.

• When ARMMUPM is asserted, it means that the request can read from both NS and NSP address spaces.

• When AWMMUPM is asserted, it means that the request can write to the NSP address space but is not permitted to write to the NS address space.

• Requests to the Non-secure Protected or System Agent physical address space must be physically addressed, that means:

– When AxPAS is NSP or SA, AxMMUVALID must be LOW.

• When AxMMUPM is asserted, AxMMUFLOW must not be Stall.

## A13.5 PCIe considerations

When the Untranslated\_Transactions signaling is used for interfacing to PCIe Root Complex, the following considerations apply:

• AxMMUSECSID must be Non-secure or Realm.

• AxMMUSID corresponds to the PCIe Requester ID.

• AxMMUSSID corresponds to the PCIe PASID.

• AxMMUSSIDV is asserted if the transaction had a PASID prefix, otherwise it is deasserted.

## A13.5.1 PCIe XT mode

PCIe eXtended TEE (XT) extends the access modes available for PCIe requests.

To support PCIe XT mode, AxMMUPASUNKNOWN signals are included, present when Untranslated\_Transactions is v4, RME\_Support is True and PAS\_WIDTH is not 0.

Table A13.9: AxMMUPASUNKNOWN signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWMMUPASUNKNOWN,</td><td>1</td><td>0b0</td><td>HIGH to indicate that there is no</td></tr><tr><td>ARMMUPASUNKNOWN</td><td></td><td></td><td>PAS expectation</td></tr></table>

The following rules apply when AxMMUVALID and AxMMUPASUNKNOWN are asserted:

• AxMMUSECSID must be Realm.

• AxPAS is inapplicable and must be Realm.

A PCIe device in eXtended TEE (XT) mode provides XT and T bits which should map to AXI as shown in Table A13.10.

Table A13.10: Mapping PCIe T and XT to AXI
<table><tr><td>XT T</td><td>AxMMUSECSID</td><td>AxPAS</td><td>AxMMUPASUNKNOWN</td><td>Meaning</td></tr><tr><td>0 0</td><td>Non-secure</td><td>Non-secure</td><td>0</td><td>Non-trusted request that must target a Non-secure PAS.</td></tr><tr><td>0 1</td><td>Realm</td><td>Realm</td><td>1</td><td>Trusted request that can target a Realm or Non-secure PAS.</td></tr><tr><td>1 0</td><td>Realm</td><td>Non-secure</td><td>0</td><td>Trusted request that must target a Non-secure PAS.</td></tr><tr><td>1 1</td><td>Realm</td><td>Realm</td><td>0</td><td>Trusted request that must target a Realm PAS.</td></tr></table>

When PCIe XT mode is not used, the T bit should map to AXI as shown in Table A13.11.

Table A13.11: Mapping PCIe T bit to AXI
<table><tr><td>T</td><td>AxMMUSECSID</td><td>AxMMUPASUNKNOWN</td><td>AxPAS</td><td>Meaning</td></tr><tr><td>0</td><td>Non-secure</td><td>0</td><td>Non-secure</td><td>Non-trusted request that must target a Non-secure PAS.</td></tr><tr><td>1</td><td>Realm</td><td>0</td><td>Realm</td><td>Trusted request that must target a Realm PAS.</td></tr></table>

## A13.6 Translation fault flows

An untranslated transaction can indicate which flow can be used when an SMMU encounters a translation fault. If no flow is indicated, a Stall flow is assumed. The property MMUFLOW\_Present is used to indicate whether other SMMU flows are supported.

Table A13.12: MMUFLOW\_Present property
<table><tr><td>MMUFLOW_Present</td><td>Default Description</td><td></td></tr><tr><td>True</td><td></td><td>AxMMUFLOW or AxMMUATST are present.</td></tr><tr><td>False</td><td>Y</td><td>AxMMUFLOW and AxMMUATST are not present.</td></tr></table>

MMUFLOW\_Present must be False if Untranslated\_Transactions is False.

If MMUFLOW\_Present is True, then:

• If Untranslated\_Transactions is True or v1, ARMMUATST and AWMMUATST are present on the interface.

• If Untranslated\_Transactions is v2 or higher, ARMMUFLOW and AWMMUFLOW are present on the interface.

Version 1 of the specification for untranslated transactions supports the Stall and ATST flows, using the AxMMUATST signals.

• When AxMMUATST is deasserted LOW, the Stall flow is used.

• When AxMMUATST is asserted HIGH, the ATST flow is used.

For version 2 and above, the AxMMUFLOW signals are used to indicate which flow can be used.

Table A13.13: AxMMUFLOW encodings
<table><tr><td>AxMMUFLOW</td><td>Flow type</td><td>Meaning</td></tr><tr><td>0b00</td><td>Stall</td><td>The SMMU Stall flow can be used.</td></tr><tr><td>0b01</td><td>ATST</td><td>The SMMU ATST flow must be used.</td></tr><tr><td>0b10</td><td>NoStall</td><td>The SMMU NoStall flow must be used.</td></tr><tr><td>0b11</td><td>PRI</td><td>The SMMU PRI flow can be used.</td></tr></table>

The following sections describe each flow in turn.

## A13.6.1 Stall flow

When the Stall flow is used, software can configure the SMMU to take one of the following actions when a translation fault occurs:

• Terminate the transaction with an SLVERR response.

• Terminate the transaction with an OKAY response, data is RAZ/WI.

• Stall the translation and inform software that the translation is stalled. Software can then instruct the SMMU to terminate the transaction or update the translation tables and retry the translation. The Manager is not aware of the stall.

This flow enables software to manage translation faults and demand paging without the Manager being aware. However, it has the following limitations:

• The Manager can see very long transaction latency, potentially triggering timeouts.

• Due to the dependence of software activity, the Stall flow can cause deadlocks in some systems.

For example, it is not recommended for use with PCIe because of dependencies between outgoing transactions to PCIe from a CPU, and incoming transactions from PCIe through the SMMU.

Enabling the Stall flow does not necessarily cause a stall when a translation fault occurs. Stalls only occur when enabled by software. Software does not normally enable stalling for PCIe endpoints.

## A13.6.2 ATST flow

The Address Translation Service Translated (ATST) flow indicates that the transaction has already been translated by Address Translation Services (ATS). It is only used by PCIe Root Ports.

When the flow is ATST, the transaction might still undergo some translation, depending on the configuration of the SMMU. For more information, see Arm® System Memory Management Unit Architecture Specification [7].

If a translation fault occurs, the transaction must be terminated with an SLVERR response.

When the flow is ATST, the following constraints apply:

• AxMMUSECSID must be Non-secure or Realm.

• If Untranslated\_Transactions is True, v1 or v2 then AxMMUSSIDV must be LOW.

When Untranslated\_Transactions is v3 or higher, it is permitted to assert AxMMUSSIDV when AxMMUFLOW indicates ATST. This is to enable the transport of PASID and other attributes from a PCIe transaction using the AxMMUSSID signal.

## A13.6.3 NoStall flow

The NoStall flow is used by a Manager that is not able to be stalled.

If a translation fault occurs when using this flow, the Subordinate must terminate the transaction with an SLVERR or OKAY response, even if software has configured the device to be stalled when a translation fault occurs.

This flow is recommended for Managers such as PCIe Root Ports which might deadlock if stalling is enabled by software.

## A13.6.4 PRI flow

The PRI flow is designed for use with a PCIe integrated endpoint. The Manager uses the PRI flow to enable software to respond to translation faults without risking deadlock.

When the flow is PRI and a translation fault occurs, the transaction is terminated with a TRANSFAULT response. The Manager can then use a separate mechanism to request that the page is made available, before retrying the transaction. This mechanism is normally PCIe PRI.

When this flow is used, software enables ATS but no ATS features are required in hardware.

A transaction that uses this flow might still be terminated by the SMMU with an SLVERR, if the translation failed for a reason which cannot be resolved by a PRI request, for example because the SMMU is incorrectly configured.

The following rules apply to a TRANSFAULT response:

• TRANSFAULT is indicated by setting RRESP or BRESP to 0b101. See A3.3 Transaction response for all encodings.

• A TRANSFAULT response is only permitted for requests using the PRI flow.

• If TRANSFAULT is used for one response transfer, it must be used for all response transfers of a transaction.

• If RRESP is TRANSFAULT, the read data in that transfer is not valid.

## A13.7 Untranslated transaction qualifier

When the Untranslated\_Transactions property is v3 or higher, a qualifier signal AxMMUVALID is added to the read and write request channels.

When AxMMUVALID is deasserted, the transaction address is a physical address and does not require translation.   
This enables a Manager to issue a mixture of translated and untranslated transactions.

The rules for using these signals are:

• When AxMMUVALID is asserted, the following signals are constrained:

– AxTAGOP must be 0b00 (Invalid)

• When AxMMUVALID is deasserted, the following signals are not applicable and can take any value:

– AxMMUSECSID

– AxMMUSID

– AxMMUSSIDV

– AxMMUSSID

– AxMMUFLOW

– AxMMUPM

– AxMMUPASUNKNOWN

• Translated and untranslated transactions must not use the same ID for in-flight transactions, and this applies to the following:

– Transactions with AWMMUVALID asserted and others with AWMMUVALID deasserted.

– Transactions with ARMMUVALID asserted and others with ARMMUVALID deasserted.

## A13.8 Permitted combinations of MMU signals and PAS

Table A13.14 shows the legal combinations of AxMMU signals and PAS. Other combinations are not permitted.

Table A13.14: Legal combinations of MMU signals and PAS
<table><tr><td>AXSSID AXID</td><td>AMOW</td><td></td><td>AUWN AXPPM</td><td></td><td></td></tr><tr><td>0</td><td>1</td><td></td><td></td><td>Secure</td><td>Meaning NoStreamID, Secure PAS</td></tr><tr><td>0</td><td>-</td><td></td><td></td><td>Non-secure</td><td>NoStreamID, Non-secure PAS</td></tr><tr><td>0</td><td>-</td><td></td><td></td><td>Root</td><td>NoStreamID, Root PAS</td></tr><tr><td>0</td><td></td><td></td><td></td><td>Realm</td><td>NoStreamID, Realm PAS</td></tr><tr><td>0</td><td>=</td><td></td><td></td><td>SA</td><td>NoStreamID, System Agent PAS</td></tr><tr><td>0</td><td>-</td><td></td><td></td><td>NSP</td><td>NoStreamID, Non-secure Protected PAS</td></tr><tr><td>1</td><td>Non-secure</td><td>Stall, NoStall, PRI</td><td>0 0</td><td>Non-secure</td><td>Untranslated, Non-secure context</td></tr><tr><td>1</td><td>Non-secure</td><td>NoStall, PRI</td><td>1 0</td><td>Non-secure</td><td>Untranslated, Non-secure context, Protected Mode</td></tr><tr><td>1</td><td>Non-secure</td><td>ATST</td><td>0 0</td><td>Non-secure</td><td>Translated, Non-secure context</td></tr><tr><td>1</td><td>Non-secure</td><td>ATST</td><td>1 0</td><td>Non-secure</td><td>Translated, Non-secure context, Protected Mode</td></tr><tr><td>1</td><td>Secure</td><td>Stall, NoStall, PRI</td><td>0 0</td><td>Secure</td><td>Untranslated, Secure context, Secure PAS</td></tr><tr><td>1</td><td>Secure</td><td>Stall, NoStall, PRI</td><td>0 0</td><td>Non-secure</td><td>Untranslated, Secure context, Non-secure PAS</td></tr><tr><td>1</td><td>Realm</td><td>Stall, NoStall, PRI</td><td>0 0</td><td>Non-secure</td><td>Untranslated, Realm context, Non-secure PAS</td></tr><tr><td>1</td><td>Realm</td><td>Stall, NoStall, PRI</td><td>0 0</td><td>Realm</td><td>Untranslated, Realm context, Realm PAS</td></tr><tr><td>1</td><td>Realm</td><td>Stall, NoStall, PRI</td><td>0 1</td><td>Realm</td><td>Untranslated, Realm context, no PAS expectation</td></tr><tr><td>1</td><td>Realm</td><td>ATST</td><td>0 0</td><td>Non-secure</td><td>Translated, Realm context, Non-secure PAS</td></tr><tr><td>1</td><td>Realm</td><td>ATST</td><td>0 0</td><td>Realm</td><td>Translated, Realm context, Realm PAS</td></tr><tr><td>1</td><td>Realm</td><td>ATST</td><td>0</td><td>1 Realm</td><td>Translated, Realm context, no PAS expectation</td></tr></table>

## A13.9 StashTranslation Opcode

The StashTranslation Opcode is a hint that an MMU should cache the table entry required to process the given address, to reduce the latency for any future transactions using that table entry.

The requirements on the MMU depend on whether the address is virtual or physical, and if the Realm Management Extension is being used:

• If AWMMUVALID is asserted or not present, the StashTranslation request has a virtual address and the MMU should cache the relevant page table entry.

• If AWMMUVALID is deasserted, the StashTranslation request has a physical address and the MMU should cache the relevant Granule Protection Table entry.

If RME\_Support is False, AWMMUVALID must be asserted for a StashTranslation request.

The StashTranslation Opcode can be used by a Manager and supported by a Subordinate if the following property conditions apply:

• Untranslated\_Transactions is v1 or higher.

• Untranslated\_Transactions is True and Cache\_Stash\_Transactions is True.

The rules for a StashTranslation operation are:

• The StashTranslation transaction consists of a request on the AW channel and a single response transfer on the B channel. There are no write data transfers.

• AWSNOOP is 0b01110 to indicate StashTranslation, AWSNOOP\_WIDTH can be 4 or 5.

• No stash target is supported. If present, AWSTASHNID, AWSTASHNIDEN, AWSTASHLPID, and AWSTASHLPIDEN must be LOW.

• Any legal combination of AWCACHE and AWDOMAIN values is permitted. See Table A8.7.

• AWATOP is 0b000000 (Non-atomic transaction).

• AWTAGOP is 0b00 (Invalid).

• StashTranslation requests must not use the same AXI ID values that are used by non-StashTranslation transactions on the write channels that are outstanding at the same time. This rule ensures that there are no ordering constraints between StashTranslation transactions and other transactions, so a Subordinate that does not stash translations can respond immediately.

• An OKAY response indicates that the StashTranslation request has been accepted, not that the translation is stashed. The request is a hint and is not guaranteed to be acted upon by a Completer.

## A13.10 UnstashTranslation Opcode

The UnstashTranslation Opcode is a hint that the page table or granule table entry that corresponds to the given transaction address and StreamID is not likely to be used again.

The requirements on the MMU depend on whether the address is virtual or physical, and if the Realm Management Extension is being used:

• If AWMMUVALID is asserted or not present, the UnstashTranslation request has a virtual address and the MMU should deallocate the relevant page table entry.

• If AWMMUVALID is deasserted, the StashTranslation request has a physical address and the MMU should deallocate the relevant Granule Protection Table entry.

If RME\_Support is False, AWMMUVALID must be asserted for an UnstashTranslation request.

The UnstashTranslation\_Transaction property is used to indicate whether an interface supports the UnstashTranslation Opcode.

Table A13.15: UnstashTranslation\_Transaction property
<table><tr><td>UnstashTranslation_Transaction Default</td><td></td><td>Description</td></tr><tr><td>True</td><td></td><td>UnstashTranslation is supported.</td></tr><tr><td>False</td><td>Y</td><td>UnstashTranslation is not supported.</td></tr></table>

The following table shows compatibility between Manager and Subordinate interfaces, according to the values of the UnstashTranslation\_Transaction property.

Table A13.16: UnstashTranslation\_Transaction compatibility
<table><tr><td>UnstashTranslation_Transaction Subordinate: False</td><td></td><td>Subordinate: True</td></tr><tr><td>Manager: False</td><td>Compatible.</td><td>Compatible.</td></tr><tr><td>Manager: True</td><td>Not compatible.</td><td>Compatible.</td></tr></table>

The rules for an UnstashTranslation operation are:

• The UnstashTranslation transaction consists of a request on the AW channel and a single response transfer on the B channel. There are no write data transfers.

• AWSNOOP is 0b10001 to indicate UnstashTranslation, AWSNOOP\_WIDTH must be 5.

• No stash target is supported. If present, AWSTASHNID, AWSTASHNIDEN, AWSTASHLPID, and AWSTASHLPIDEN must be LOW.

• Any legal combination of AWCACHE and AWDOMAIN values is permitted. See Table A8.7.

• AWATOP is 0b000000 (Non-atomic transaction).

• AWTAGOP is 0b00 (Invalid).

• AWID is unique-in-flight, which means:

– An UnstashTranslation request can only be issued if there are no outstanding transactions on the write channels using the same ID value.

– A Manager must not issue a request on the write channels with the same ID as an outstanding UnstashTranslation transaction.

– If present, AWIDUNQ must be asserted for an UnstashTranslation request.

• An OKAY response indicates that the UnstashTranslation request has been accepted, not that the translation is deallocated. The request is a hint and is not guaranteed to be acted upon by a Completer.

# Chapter A14 Interface clock and power gating

This chapter describes stopping and starting interfaces for the purposes of clock and power control. It contains the following sections:

• A14.1 Interface gating with Valid-Ready transport

• A14.2 Interface gating with credited transport

## A14.1 Interface gating with Valid-Ready transport

When using a Valid-Ready transport, wake-up signals can be used to indicate when there is activity associated with the interface.

Table A14.1: Wake-up signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>AWAKEUP</td><td>1</td><td></td><td>Manager output, asserted HIGH to indicate there might be activity on the read and write request channels.</td></tr><tr><td>ACWAKEUP</td><td>1</td><td></td><td>Subordinate output, asserted HIGH to indicate there might be activity on the snoop request channel.</td></tr></table>

The signals can be routed to a clock controller or similar component to enable power and clocks to the connected components.

The wake-up signals are synchronous and must also be suitable for sampling asynchronously in a different clock domain. This requires the wake-up signals to be glitch-free, which can be achieved by for example being generated directly from a register, or from a glitch-free OR tree.

The wake-up signals must be asserted to guarantee that a transaction can be accepted, but once the transaction is in progress the assertion or deassertion of the wake-up signal is IMPLEMENTATION DEFINED.

It is recommended, but not required that a wake-up signal is deasserted when no further transactions are required.   
The Wakeup\_Signals property is used to indicate whether a component includes wake-up signaling.

Table A14.2: Wakeup\_Signals property
<table><tr><td>Wakeup_Signals Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>AWAKEUP is present. ACWAKEUP is present if the interface has an AC channel.</td></tr><tr><td>False</td><td>Y</td><td>No wake-up signals are present.</td></tr></table>

Wakeup signals can only be used with Valid-Ready transport, which implies the following:

• When AXI\_Transport is Credited, Wakeup\_Signals must be False.

## A14.1.1 AWAKEUP rules and recommendations

AWAKEUP is an output signal from a Manager interface and is asserted at the start of a transaction to indicate that there is a transaction to be processed. It has the following rules:

• It is recommended that AWAKEUP is asserted at least one cycle before the assertion of ARVALID, AWVALID, or WVALID to prevent the acceptance of a transaction request being delayed.

• It is permitted for AWAKEUP to be asserted at any point before or after the assertion of ARVALID, AWVALID, or WVALID.

• A Subordinate is permitted to wait for AWAKEUP to be asserted before asserting ARREADY, AWREADY, or WREADY.

• If AWAKEUP is asserted in a cycle where AWVALID is asserted and AWREADY is deasserted, then AWAKEUP must remain asserted until AWREADY is asserted.

• If AWAKEUP is asserted in a cycle when ARVALID is asserted and ARREADY is deasserted, then AWAKEUP must remain asserted until ARREADY is asserted.

• After the ARVALID, ARREADY handshake, or the AWVALID, AWREADY handshake, the interconnect must remain active until the transaction has completed.

• It is permitted, but not recommended, to assert AWAKEUP then deassert it without a transaction taking place.

There is no requirement relating to the assertion of AWAKEUP relative to WVALID. However, for components that can assert WVALID before AWVALID, the assertion of AWAKEUP at least one cycle before WVALID can prevent the acceptance of a new transaction being delayed.

If a Subordinate has an AWAKEUP input but the attached Manager does not have an AWAKEUP output, then either:

• Tie AWAKEUP high, however this might prevent the Subordinate interface from using low power states.

• Derive AWAKEUP from AxVALID and SYSCOREQ/ACK. This method allows the Subordinate to enter low power states, but it may introduce latency while the clock is enabled.

## A14.1.2 AWAKEUP and Coherency Connection signaling

If wake-up and Coherency Connection signals are both present on an interface, there are additional considerations.

• It is required that the AWAKEUP signal is asserted to guarantee progress of a transition on the Coherency Connection signaling.

• It is permitted for AWAKEUP to be asserted at any point before or after the assertion of SYSCOREQ. However, it is required to be asserted to guarantee the corresponding assertion of SYSCOACK. When AWAKEUP is asserted with SYSCOREQ asserted and SYSCOACK deasserted, it must remain asserted until SYSCOACK is asserted.

• It is permitted for AWAKEUP to be asserted at any point before or after the deassertion of SYSCOREQ. However, it is required to be asserted to guarantee the corresponding deassertion of SYSCOACK. When AWAKEUP is asserted with SYSCOREQ deasserted and SYSCOACK asserted, it must remain asserted until SYSCOACK is deasserted.

See A15.6 Coherency Connection signaling for more details.

## A14.1.3 ACWAKEUP rules and recommendations

ACWAKEUP is an output signal from a Subordinate interface, usually on an interconnect, and is asserted at the start of a DVM message transaction to indicate that there is a transaction to be processed. It has the following rules:

• It is recommended that ACWAKEUP is asserted at least one cycle before the assertion of ACVALID to prevent the acceptance of a DVM request being delayed.

• ACWAKEUP must remain asserted until the associated ACVALID / ACREADY handshake to ensure progress of the DVM transaction.

• After the ACVALID / ACREADY handshake, the Manager must remain active until the DVM transaction has completed.

• It is permitted for ACWAKEUP to be asserted at any point before or after the assertion of ACVALID.

• It is permitted, but not recommended, to assert ACWAKEUP and then deassert it without ACVALID being asserted.

## A14.2 Interface gating with credited transport

When using credited transport, an interface can include control signals to determine when channel receivers can give credits. This can be used to clock or power gate interfaces when they are idle.

The property Credit\_Control is used to indicate whether credit control signals are included on an interface. If credit control signals are not included, the interface is assumed to be running when not in reset.

Credits are implicitly returned during the STOP state and on exit from the STOP state all credits are with the receiver. Transmitters are not required to explicitly return all credits to the receiver before it stops.

Table A14.3: Credit\_Control property
<table><tr><td>Credit_Control</td><td>Default Description</td><td></td></tr><tr><td>False</td><td>Y</td><td>Credit control signals are not included. Credit exchange starts from reset and does not stop.</td></tr><tr><td>Implicit_Return_Uni</td><td></td><td>Credit control signals are included. Credits are implicitly returned to the receiver when exiting the STOP state. Control is unidirectional because only a Manager can initiate the move to ACTIVATE or DEACTIVATE.</td></tr></table>

The following rules apply to the Credit\_Control property:

• Credit\_Control must be False if the AXI\_Transport property is Ready.

• Connected interfaces must have the same value for Credit\_Control.

Table A14.4 shows the signals that are included when Credit\_Control is Implicit\_Return\_Uni.

Table A14.4: Credit control signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>ACTIVATEREQ</td><td>1</td><td>0b1</td><td>Activation / deactivation request from a Manager.</td></tr><tr><td>ACTIVATEACK</td><td>1</td><td>0b1</td><td>Activation / deactivation acknowledge from a Subordinate.</td></tr><tr><td>ASKSTOP</td><td>1</td><td>0b0</td><td>Asserted HIGH to indicate that the Subordinate wants the Manager to stop the interface.</td></tr></table>

Figure A14.1 shows connected AXI5 interfaces using credit control signaling.  
![](images/d7dc892387984782007f17cb8ef3c29c637ab6a93424d4e5942b703a882d720a.jpg)  
Figure A14.1: AXI5 interfaces using credit control signaling

## A14.2.1 Channel states

When using credit control, an interface can be in one of four states: STOP, ACTIVATE, RUN, DEACTIVATE.

• RUN and STOP are stable states. An interface can remain in this state for an indefinite period.

• DEACTIVATE and ACTIVATE are transient states. It is expected that an interface moves to the next stable state in a relatively short period.

![](images/47b0fcedb64e20c20e5d4bdbb735c5d4abe7e70fcf9e22ee668ff6dcb06f0f9f.jpg)  
Figure A14.2: Interface states

## A14.2.1.1 STOP state

• There are no outstanding transactions, the interface is idle and can be clock gated or powered down.

• Managers and Subordinates have no credits and cannot send any transfers or credits.

• The Subordinate might receive credits after entering this state if there is a race between credits and ACTIVATEREQ deassertion, they must be discarded.

• If the Manager wants to start a transaction, it can assert ACTIVATEREQ.

• When ACTIVATEREQ is asserted, the interface moves into the ACTIVATE state.

## A14.2.1.2 ACTIVATE state

• This is a transient state, and the interface is expected to transition to RUN within a relatively short period.

• When the Subordinate is ready to start, it asserts ACTIVATEACK and starts to send credits.

• The Manager might receive credits due to a potential race between ACTIVATEACK and credit signals, these can be used to send transfers.

• When ACTIVATEACK is asserted, the interface moves into the RUN state.

## A14.2.1.3 RUN state

• The Manager and Subordinate can send credits and transfers.

• If the Manager wants to stop the interface and there are no outstanding transactions, it can stop sending credits and deassert ACTIVATEREQ.

• If the Subordinate wants the interface to stop, it can assert ASKSTOP.

• When ACTIVATEREQ is deasserted, the interface moves into the DEACTIVATE state.

## A14.2.1.4 DEACTIVATE state

• This is a transient state, and the interface is expected to transition to STOP within a relatively short period.

• The Manager must not send transfers or credits.

• The Subordinate will have no transfers to send because all outstanding transactions must be complete.

• The Subordinate stops sending credits and deasserts ACTIVATEACK.

• When ACTIVATEACK is deasserted, the interface moves into the STOP state.

## A14.2.2 Stop request signal, ASKSTOP

The Manager controls the move from RUN to DEACTIVATE, but the Subordinate can use the ASKSTOP signal to ask the Manager to initiate the move to DEACTIVATE. This might be because the Subordinate is idle or because it is required to reconfigure or reset when all outstanding transactions are complete.

The following rules apply to ASKSTOP:

• ASKSTOP can only be HIGH when ACTIVATEACK is HIGH, that means in the RUN or DEACTIVATE states.

• If ASKSTOP is asserted, it must remain HIGH until ACTIVATEACK is LOW.

• ASKSTOP must be LOW when ACTIVATEACK is LOW.

• When ASKSTOP is HIGH, the Manager must deassert ACTIVATEREQ when there are no outstanding transactions.

• It is recommended that the Manager does not issue any new transaction requests when ASKSTOP is HIGH.

## A14.2.3 Credit control signal rules

The following rules apply to the credit control signals:

• When ACTIVATEREQ is LOW there must be no outstanding transactions and the Manager must not send transfers.

• When ACTIVATEREQ is LOW or ACTIVATEACK is LOW, the Manager must not send credits.

• When ACTIVATEACK is LOW, the Subordinate must not send transfers or credits.

• ACTIVATEREQ, ACTIVATEACK and ASKSTOP must be LOW during reset.

## A14.2.4 Pipelining channels

It can sometimes be required to add pipeline stages to channels to meet timing between interfaces. The following rules and notes apply:

• Register pipeline stages can be added to VALID, CRDT or CRDTSH paths of any channel independently.

• The Manager must not receive any credits in the STOP state.

– If credit signals from the Subordinate have a longer transport delay than ACTIVATEACK, there must be a delay between sending the last credits and deasserting ACTIVATEACK.

• If credit signals from the Manager have a longer transport delay than ACTIVATEREQ, the Subordinate might receive credits in the STOP state. These credits must be discarded.

• If ACTIVATEACK has a longer transport delay than credit signals, the Manager might receive and use credits in the ACTIVATE state.

• ASKSTOP must be pipelined the same as ACTIVATEACK so the rules regarding ASKSTOP can be applied on both sides of the connection.

• When registering the VALID signals, the logic must ensure that associated payload signals remain aligned to VALID and the PENDING signals are HIGH in the cycle before VALID is HIGH.

## A14.2.5 Clock and power gating

When an interface is in the STOP state, the transport logic can be clock or power gated. The following rules apply:

• Transfers will not be sent or received.

• Credits will not be sent.

• If credits are received, they are discarded.

A Subordinate interface can use the ACTIVATEREQ input to activate its clocks or power, therefore:

• ACTIVATEREQ must be glitch free and suitable for sampling in a different clock domain.

## A14.3 Sequence diagram

Figure A14.3 shows the sequence diagram for credit control in an AXI5 interface.

![](images/f004bd11b368c818d44b6da5a0af42b51f6853d9d8f555cc552399d1a24c9687.jpg)  
Figure A14.3: Sequence diagram of an AXI5 connection using credit control signaling

The following behavior is not shown in the sequence diagram:

• A Manager might receive credits in the DEACTIVATE state due to the opposite direction race.

• A Manager might receive credits in the ACTIVATE state due to pipelining, these can be used immediately.

• Due to pipelining, a Subordinate might receive credits during the STOP state, which must be discarded.

## A14.4 Example waveform

An example interface control waveform is included to demonstrate a common case but does not indicate all permitted behavior. Not all signals are shown, for example PENDING signals must be included on all credited channels.

## A14.4.1 Transmitting one read transaction

In this example, the Manager sends one read request, waits for the two data transfers then stops the interface.

![](images/c22d0e53459590d9ecf232a4d42f0821736f7b6c3a51dac846aeb23f26218cba.jpg)  
Figure A14.4: Starting and stopping an interface after one read transaction

Cycle 0 The link is inactive, both interfaces are in STOP.

Cycle 2 The Manager has a request to send, so asserts ACTIVATEREQ to wake the Subordinate.

Cycle 4 The Subordinate asserts ACTIVATEACK. It sends a credit by asserting ARCRDT.

Cycle 5 The Manager sends a transfer on AR and the Subordinate sends another AR credit.

Cycle 6 The Manager starts sending credits on the R channel.

Cycle 10, 12 The Subordinate sends two read data transfers and the transaction is complete.

Cycle 13 The Subordinate wants the interface to stop so asserts ASKSTOP.

Cycle 29 There are no outstanding transactions so the Manager deasserts ACTIVATEREQ.

Cycle 31 The Subordinate deasserts ACTIVATEACK and ASKSTOP and moves into STOP. This must be at least N cycles after the Subordinate sent a credit, where N is the maximum number of cycles that any credit signal is delayed by pipelining.

# Chapter A15 Distributed Virtual Memory messages

This chapter describes how AXI supports distributed system MMUs using Distributed Virtual Memory (DVM) messages to maintain all MMUs in a virtual memory system.

It contains the following sections:

• A15.1 Introduction to DVM transactions

• A15.2 Support for DVM messages

• A15.3 DVM messages

• A15.4 Transporting DVM messages

• A15.5 DVM Sync and Complete

• A15.6 Coherency Connection signaling

## A15.1 Introduction to DVM transactions

DVM transactions are an optional feature used to pass messages that support the maintenance of a virtual memory system. There are two types of DVM transactions: DVM message and DVM Complete.

A DVM message supports the following operations:

• TLB Invalidate

• Branch Predictor Invalidate

• Physical Instruction Cache Invalidate

• Virtual Instruction Cache Invalidate

• Synchronization

• Hint

DVM message requests are sent from a Subordinate interface, usually on an interconnect, to a Manager interface using the snoop request (AC) channel.

DVM message responses are sent from a Manager to Subordinate interface using the snoop response (CR) channel.

A DVM Complete transaction is issued on the read request channel (AR) in response to a DVM Synchronization (Sync) message, to indicate that all required operations and any associated transactions have completed.

## A15.2 Support for DVM messages

The DVM\_Message\_Support property is used to indicate if an interface supports DVM messages.

Table A15.1: DVM\_Message\_Support property
<table><tr><td>DVM_Message_Support Default Description</td><td></td><td></td></tr><tr><td>Receiver</td><td></td><td>DVM message and Synchronization transactions are supported from Subordinate to Manager interfaces on the AC/CR channels. DVM Complete transactions are supported from Manager to Subordinate interfaces on the</td></tr><tr><td>False</td><td>Y</td><td>AR/R channels. DVM message transactions are not supported.</td></tr></table>

Note that the Bidirectional option for DVM\_Message\_Support in previous issues of this specification is deprecated in this specification.

DVM Complete messages require that ARDOMAIN is set to Shareable. Therefore, when DVM\_Message\_Support is Receiver the Shareable\_Transactions property must be True.

DVM messages were introduced in the Armv7 architecture and were extended in Armv8, Armv8.1, Armv8.4, and Armv9.2 architectures. It is essential that interfaces initiating and receiving DVM messages support the same architecture versions.

The following properties define the version that is supported by an interface:

• DVM\_v8

• DVM\_v8.1

• DVM\_v8.4

• DVM\_v9.2

Each property can take the values: True or False. If a property is not declared, then it is considered False.

In Table A15.2 there is an indication of which message versions are supported, depending on the property values.   
A component that supports DVM messages from a specific version must also support earlier architecture versions.

Table A15.2: DVM message versions
<table><tr><td colspan="4">DVM property</td><td colspan="5">Architecture support</td></tr><tr><td>DVM_v9.2</td><td>DVM_v8.4</td><td>DVM_v8.1</td><td>DVM_v8</td><td>Armv9.2</td><td>Armv8.4</td><td>Armv8.1</td><td>Armv8</td><td>Armv7</td></tr><tr><td>True</td><td>True or False</td><td>True or False</td><td>True or False</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>False</td><td>True</td><td>True or False</td><td>True or False</td><td>一</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>False</td><td>False</td><td>True</td><td>True or False</td><td>-</td><td></td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>False</td><td>False</td><td>False</td><td>True</td><td>-</td><td>-</td><td>1</td><td>Y</td><td>Y</td></tr><tr><td>False</td><td>False</td><td>False</td><td>False</td><td>-</td><td></td><td></td><td>-</td><td>Y</td></tr></table>

## A15.3 DVM messages

The following DVM messages are supported by the protocol:

• TLB Invalidate

• Branch Predictor Invalidate

• Physical Instruction Cache Invalidate

• Virtual Instruction Cache Invalidate

• Synchronization

• Hint

DVM transactions only operate on read-only structures, such as Instruction cache, Branch Predictor, and TLB, and therefore only invalidation operations are required. The concept of cleaning does not apply to a read-only structure. This means that it is functionally correct to invalidate more entries than the DVM message requires, although the extra invalidations can affect performance.

## A15.3.1 DVM message fields

The fields in DVM messages are shown in Table A15.3.

Table A15.3: DVM message fields
<table><tr><td>Name</td><td>Width</td><td colspan="2">Description</td></tr><tr><td>VA</td><td>32-57</td><td colspan="2">Virtual Address or Intermediate Physical Address (IPA)</td></tr><tr><td>PA</td><td>32-52</td><td colspan="2">Physical Address</td></tr><tr><td>ASID</td><td>8 or 16</td><td colspan="2">Address Space ID</td></tr><tr><td>ASIDV</td><td>1</td><td colspan="2">Asserted HIGH to indicate that the ASID field is valid.</td></tr><tr><td></td><td></td><td colspan="2">When deasserted, ASID must be zero.</td></tr><tr><td>VMID</td><td>8 or 16</td><td colspan="2">Virtual Machine ID</td></tr><tr><td>VMIDV</td><td>1</td><td colspan="2">Asserted HIGH to indicate that the VMID field is valid. When deasserted, VMID must be zero.</td></tr><tr><td>DVMType</td><td>3</td><td colspan="2">DVM message type:</td></tr><tr><td></td><td>0b000</td><td>TLB Invalidate (TLBI)</td><td></td></tr><tr><td></td><td></td><td>0b001</td><td>Branch Predictor Invalidate (BPI)</td></tr><tr><td></td><td></td><td>0b010</td><td>Physical Instruction Cache Invalidate (PICI)</td></tr><tr><td></td><td></td><td>0b011</td><td>Virtual Instruction Cache Invalidate (VICI)</td></tr><tr><td></td><td></td><td>0b100</td><td>Synchronization (Sync)</td></tr><tr><td></td><td></td><td>0b101 Reserved</td><td></td></tr><tr><td></td><td></td><td>0b110 Hint</td><td></td></tr><tr><td></td><td></td><td>0b111 Reserved</td><td></td></tr></table>

Continued on next page

Table A15.3 – Continued from previous page
<table><tr><td>Name</td><td>Width</td><td colspan="2">Description</td></tr><tr><td>Exception</td><td>2</td><td colspan="2">Indicates the Exception level that the transaction applies to:</td></tr><tr><td></td><td></td><td>0b00</td><td>Hypervisor and all Guest OS</td></tr><tr><td></td><td></td><td>0b01</td><td>EL3</td></tr><tr><td></td><td></td><td>0b10</td><td>Guest OS</td></tr><tr><td></td><td></td><td>0b11</td><td>Hypervisor</td></tr><tr><td>Security</td><td>2</td><td colspan="2">Indicates which Security state the invalidation applies to. See Table A15.6 for encodings.</td></tr><tr><td>Leaf</td><td>1</td><td>Indicates whether only leaf entries are invalidated:</td><td></td></tr><tr><td></td><td></td><td>0b0</td><td>Invalidate all associated translations.</td></tr><tr><td></td><td></td><td>0b1</td><td>Invalidate Leaf Entry only</td></tr><tr><td>Stage</td><td>2</td><td colspan="2">Indicates which stages are invalidated:</td></tr><tr><td></td><td></td><td>0b00</td><td>Armv7: Stage of invalidation varies with invalidation type. Armv8 and later: Stage 1 and Stage 2 invalidation.</td></tr><tr><td></td><td></td><td>0b01</td><td>Stage 1 only invalidation.</td></tr><tr><td></td><td></td><td>0b10</td><td>Stage 2 only invalidation.</td></tr><tr><td></td><td></td><td>0b11</td><td>GPT</td></tr><tr><td>Num</td><td>5</td><td colspan="2">Used as a constant multiplication factor in the range calculation. All binary values are valid.</td></tr><tr><td>Scale</td><td>2</td><td colspan="2">Used as a constant in address range exponent calculation.</td></tr><tr><td>TTL</td><td></td><td colspan="2">All binary values are valid. Hint of Translation Table Level (TTL) which includes the addresses to be</td></tr><tr><td>TG</td><td></td><td colspan="2">invalidated. See Table A15.4 and Table A15.5 for details.</td></tr><tr><td></td><td>2</td><td colspan="2">Translation Granule (TG). For TLB Invalidations by range, TG indicates the granule size:</td></tr><tr><td></td><td></td><td>0b00 Reserved.</td><td></td></tr><tr><td></td><td></td><td>0b01</td><td>4KB</td></tr><tr><td></td><td></td><td>0b10</td><td>16KB</td></tr><tr><td></td><td></td><td>0b11</td><td>64KB</td></tr><tr><td></td><td></td><td></td><td>For non-range TLB Invalidations, TG and TTL indicate the table level hint, see</td></tr><tr><td></td><td></td><td colspan="2">Table A15.5.</td></tr><tr><td>VI</td><td>16</td><td colspan="2">Virtual Index, used for PICI messages.</td></tr><tr><td>VIV</td><td>2</td><td>Virtual Index Valid:</td><td>Virtual Index not valid</td></tr><tr><td></td><td></td><td>0b00</td><td></td></tr><tr><td></td><td></td><td>0b01</td><td>Reserved</td></tr><tr><td></td><td></td><td>0b10</td><td>Reserved</td></tr><tr><td></td><td></td><td>0b11</td><td>Virtual Index valid</td></tr></table>

Continued on next page

Table A15.3 – Continued from previous page
<table><tr><td>Name</td><td>Width</td><td colspan="2">Description</td></tr><tr><td>IS</td><td>4</td><td></td><td>Invalidation Size encoding for GPT TLBI by PA operations:</td></tr><tr><td></td><td></td><td>0b0000</td><td>4KB</td></tr><tr><td></td><td></td><td>0b0001</td><td>16KB</td></tr><tr><td></td><td></td><td>0b0010</td><td>64KB</td></tr><tr><td></td><td></td><td>0b0011</td><td>2MB</td></tr><tr><td></td><td></td><td>0b0100</td><td>32MB</td></tr><tr><td></td><td></td><td>0b0101</td><td>512MB</td></tr><tr><td></td><td></td><td>0b0110</td><td>1GB</td></tr><tr><td></td><td></td><td>0b0111</td><td>16GB</td></tr><tr><td></td><td></td><td>0b1000</td><td>64GB</td></tr><tr><td></td><td></td><td>0b1001</td><td>512GB</td></tr><tr><td></td><td></td><td>0b1010- 0b1111</td><td>Reserved</td></tr><tr><td>Addr</td><td>1</td><td colspan="2">Indicates if the message includes an address.</td></tr><tr><td></td><td></td><td></td><td>No address information.</td></tr><tr><td></td><td></td><td>0b0 0b1</td><td>Address included, this is a two-part message.</td></tr><tr><td>Range</td><td></td><td colspan="2"></td></tr><tr><td></td><td>1</td><td colspan="2">Asserted HIGH to indicate that the 2nd part indicates an address range.</td></tr><tr><td>Completion</td><td>1</td><td colspan="2">Asserted HIGH to indicate that a Completion message is required.</td></tr></table>

## TLB Invalidate level hint

For TLB Invalidations by address range, the TTL field indicates which level of translation table walk holds the leaf entry for the address being invalidated. The encodings are shown in Table A15.4.

Table A15.4: Leaf entry hint for range-based TLB Invalidations
<table><tr><td>TTL</td><td>Meaning</td></tr><tr><td>0b00</td><td>No level hint information.</td></tr><tr><td>0b01</td><td>The leaf entry is on level 1 of the translation table walk.</td></tr><tr><td>0b10</td><td>The leaf entry is on level 2 of the translation table walk.</td></tr><tr><td>0b11</td><td>The leaf entry is on level 3 of the translation table walk.</td></tr></table>

For TLB Invalidations by non-range address, the TTL and TG fields indicate which level of translation table walk holds the leaf entry for the address being invalidated. The encodings are shown in Table A15.5.

Table A15.5: Leaf entry hint for non-range TLB Invalidations
<table><tr><td>TG</td><td>TTL</td><td>Meaning</td></tr><tr><td rowspan="5">0b00</td><td>0b00</td><td>No level hint</td></tr><tr><td>0b01</td><td>Reserved</td></tr><tr><td>0b10</td><td>Reserved</td></tr><tr><td>0b11</td><td>Reserved</td></tr><tr><td>0b00</td><td>No level hint</td></tr><tr><td rowspan="3">0b01</td><td>0b01</td><td>The leaf entry is on level 1 of the translation table walk.</td></tr><tr><td>0b10</td><td>The leaf entry is on level 2 of the translation table walk.</td></tr><tr><td>0b11</td><td>The leaf entry is on level 3 of the translation table walk.</td></tr><tr><td rowspan="4">0b10</td><td>0b00</td><td>No level hint</td></tr><tr><td>0b01</td><td>No level hint</td></tr><tr><td>0b10</td><td>The leaf entry is on level 2 of the translation table walk.</td></tr><tr><td>0b11</td><td>The leaf entry is on level 3 of the translation table walk.</td></tr><tr><td rowspan="4">0b11</td><td>0b00</td><td>No level hint</td></tr><tr><td>0b01</td><td>The leaf entry is on level 1 of the translation table walk.</td></tr><tr><td>0b10</td><td>The leaf entry is on level 2 of the translation table walk.</td></tr><tr><td>0b11</td><td>The leaf entry is on level 3 of the translation table walk.</td></tr></table>

## Security field

The Security field has different meanings depending on the DVM Type, as shown in Table A15.6.

Table A15.6: Security field encodings per DVM Type
<table><tr><td>Security</td><td>TLBI</td><td>BPI</td><td>PICI All</td><td>PICI by PA</td><td>VICI</td></tr><tr><td>0b00</td><td>Realm</td><td>Secure and Non-secure</td><td>Root, Realm, Secure, and Non-secure</td><td>Root</td><td>Secure and Non-secure</td></tr><tr><td>0b01</td><td>Non-secure address from a Secure context</td><td>Reserved</td><td>Realm and Non-secure</td><td>Realm</td><td>Reserved</td></tr><tr><td>0b10</td><td>Secure</td><td>Reserved</td><td>Secure and Non-secure</td><td>Secure</td><td>Secure</td></tr><tr><td>0b11</td><td>Non-secure</td><td>Reserved</td><td>Non-secure</td><td>Non-secure</td><td>Non-secure</td></tr></table>

## ASID field

The ASID field contains an 8-bit or 16-bit Address Space ID.

• Armv7 supports only an 8-bit ASID.

• Armv8 and above support both 8-bit and 16-bit ASID.

It cannot be determined from a DVM message whether the message uses an 8-bit or 16-bit ASID. All 8-bit ASID messages are required to set the ASID[15:8] bits to zero.

It is expected that most systems will use a single ASID size across the entire system, either 8-bit ASID or 16-bit ASID.

In a system that contains a mix of 8-bit ASID and 16-bit ASID components, it is expected that all maintenance is done by an agent that uses 16-bit ASID. This ensures that the agent can perform maintenance on both the 8-bit ASID and 16-bit ASID components.

The interoperability requirements are:

• For an 8-bit ASID agent sending a message to a 16-bit ASID agent, a message appears as a 16-bit ASID with the upper 8 bits set to zero.

• For a 16-bit ASID agent sending a message to an 8-bit ASID agent:

– If the upper 8 bits are zero, the message was received correctly.

– If the upper 8 bits are non-zero, then over-invalidation will occur, since the 8-bit ASID agent ignores the upper 8 bits.

## VMID field

The VMID field contains an 8-bit or 16-bit Virtual Machine ID.

• Armv7 and Armv8 support only 8-bit VMIDs.

• Armv8.1 and above support both 8-bit and 16-bit VMIDs.

It cannot be determined from a DVM message whether the message uses an 8-bit or 16-bit VMID. All 8-bit VMID messages are required to set the VMID[15:8] field to zero.

It is expected that most systems use a single VMID size across the entire system, either 8-bit VMID or 16-bit VMID.

In a system that contains a mix of 8-bit VMID and 16-bit VMID components, it is expected that all maintenance is done by an agent that uses 16-bit VMID. This ensures that the agent can perform maintenance on both the 8-bit VMID and 16-bit VMID components.

The interoperability requirements are:

• For an 8-bit VMID agent sending a message to a 16-bit VMID agent, a message appears as a 16-bit VMID with the upper 8 bits set to zero.

• For a 16-bit VMID agent sending a message to an 8-bit VMID agent:

– If the upper 8 bits are zero, the message was received correctly.

– If the upper 8 bits are nonzero, then over-invalidation will occur, since the 8-bit VMID agent ignores the upper 8 bits.

When Armv8.1 and above is supported, ACVMIDEXT is included on the AC channel to transport the upper byte of 16-bit VMIDs. See A15.4 Transporting DVM messages for more details.

## A15.3.2 TLB Invalidate messages

This section details the TLB Invalidate (TLBI) message.

For a TLBI message some fields have a fixed value, as shown in Table A15.7.

Table A15.7: Fixed field values for a TLBI message
<table><tr><td>Name</td><td>Value</td><td>Meaning</td></tr><tr><td>DVMType</td><td>0b000</td><td>TLB Invalidate opcode.</td></tr><tr><td>Completion</td><td>0b0</td><td>Completion not required.</td></tr></table>

The entries on which the TLBI must operate depends on the fields in the message. All supported TLBI operations are shown in Table A15.8.

The Arm column indicates the minimum Arm architecture version required to support the message.

The field to signal mappings for TLBI messages are detailed in Table A15.20.

Table A15.8: TLBI messages
<table><tr><td>Operation</td><td>Arm</td><td>Exception</td><td>Security</td><td>VMIDV</td><td>ASIDV</td><td>Leaf</td><td>Stage</td><td>Addr</td></tr><tr><td>EL3 TLBI all</td><td>v8</td><td>0b01</td><td>0b10</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b0</td></tr><tr><td>EL3 TLBI by VA</td><td>v8</td><td>0b01</td><td>0b10</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b1</td></tr><tr><td>EL3 TLBI by VA, Leaf only</td><td>v8</td><td>0b01</td><td>0b10</td><td>0b0</td><td>0b0</td><td>0b1</td><td>0b00</td><td>0b1</td></tr><tr><td>Secure Guest OS TLBI by Non-secure IPA</td><td>v8.4</td><td>0b10</td><td>0b01</td><td>0b1</td><td>0b0</td><td>0b0</td><td>0b10</td><td>0b1</td></tr><tr><td>Secure Guest OS TLBI by Non-secure IPA, Leaf only</td><td>v8.4</td><td>0b10</td><td>0b01</td><td>0b1</td><td>0b0</td><td>0b1</td><td>0b10</td><td>0b1</td></tr><tr><td>Secure TLBI all</td><td>v7</td><td>0b10</td><td>0b10</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b0</td></tr><tr><td>Secure TLBI by VA</td><td>v7</td><td>0b10</td><td>0b10</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b1</td></tr><tr><td>Secure TLBI by VA, Leaf only</td><td>v8</td><td>0b10</td><td>0b10</td><td>0b0</td><td>0b0</td><td>0b1</td><td>0b00</td><td>0b1</td></tr></table>

Continued on next page

Table A15.8 – Continuedfrom previous page
<table><tr><td>Operation</td><td>Arm</td><td>Exception</td><td>Security</td><td>VMIDV</td><td>ASIDV</td><td>Leaf</td><td>Stage</td><td>Addr</td></tr><tr><td>Secure TLBI by ASID</td><td>v7</td><td>0b10</td><td>0b10</td><td>0b0</td><td>0b1</td><td>0b0</td><td>0b00</td><td>0b0</td></tr><tr><td>Secure TLBI by ASID and VA</td><td>v7</td><td>0b10</td><td>0b10</td><td>0b0</td><td>0b1</td><td>0b0</td><td>0b00</td><td>0b1</td></tr><tr><td>Secure TLBI by ASID and VA, Leaf only</td><td>v8</td><td>0b10</td><td>0b10</td><td>0b0</td><td>0b1</td><td>0b1</td><td>0b00</td><td>0b1</td></tr><tr><td>Secure Guest OS TLBI all</td><td>v8.4</td><td>0b10</td><td>0b10</td><td>0b1</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b0</td></tr><tr><td>Secure Guest OS TLBI by VA</td><td>v8.4</td><td>0b10</td><td>0b10</td><td>0b1</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b1</td></tr><tr><td>Secure Guest OS TLBI all, Stage 1 only</td><td>v8.4</td><td>0b10</td><td>0b10</td><td>0b1</td><td>0b0</td><td>0b0</td><td>0b01</td><td>0b0</td></tr><tr><td>Secure Guest OS TLBI by Secure IPA</td><td>v8.4</td><td>0b10</td><td>0b10</td><td>0b1</td><td>0b0</td><td>0b0</td><td>0b10</td><td>0b1</td></tr><tr><td>Secure Guest OS TLBI by VA, Leaf only</td><td>v8.4</td><td>0b10</td><td>0b10</td><td>0b1</td><td>0b0</td><td>0b1</td><td>0b00</td><td>0b1</td></tr><tr><td>Secure Guest OS TLBI by Secure IPA, Leaf only</td><td>v8.4</td><td>0b10</td><td>0b10</td><td>0b1</td><td>0b0</td><td>0b1</td><td>0b10</td><td>0b1</td></tr><tr><td>Secure Guest OS TLBI by ASID</td><td>v8.4</td><td>0b10</td><td>0b10</td><td>0b1</td><td>0b1</td><td>0b0</td><td>0b00</td><td>0b0</td></tr><tr><td>Secure Guest OS TLBI by ASID and VA</td><td>v8.4</td><td>0b10</td><td>0b10</td><td>0b1</td><td>0b1</td><td>0b0</td><td>0b00</td><td>0b1</td></tr><tr><td>Secure Guest OS TLBI by ASID and VA, Leaf only</td><td>v8.4</td><td>0b10</td><td>0b10</td><td>0b1</td><td>0b1</td><td>0b1</td><td>0b00</td><td>0b1</td></tr><tr><td>All OS TLBI all</td><td>v7</td><td>0b10</td><td>0b11</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b0</td></tr><tr><td>Guest OS TLBI all, Stage 1 and 2</td><td>v7</td><td>0b10</td><td>0b11</td><td>0b1</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b0</td></tr><tr><td>Guest OS TLBI by VA</td><td>v7</td><td>0b10</td><td>0b11</td><td>0b1</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b1</td></tr><tr><td>Guest OS TLBI all, Stage 1 only</td><td>v8</td><td>0b10</td><td>0b11</td><td>0b1</td><td>0b0</td><td>0b0</td><td>0b01</td><td>0b0</td></tr><tr><td>Guest OS TLBI by IPA</td><td>v8</td><td>0b10</td><td>0b11</td><td>0b1</td><td>0b0</td><td>0b0</td><td>0b10</td><td>0b1</td></tr><tr><td>Guest OS TLBI by VA, Leaf only</td><td>v8</td><td>0b10</td><td>0b11</td><td>0b1</td><td>0b0</td><td>0b1</td><td>0b00</td><td>0b1</td></tr><tr><td>Guest OS TLBI by IPA, Leaf only</td><td>v8</td><td>0b10</td><td>0b11</td><td>0b1</td><td>0b0</td><td>0b1</td><td>0b10</td><td>0b1</td></tr><tr><td>Guest OS TLBI by ASID</td><td>v7</td><td>0b10</td><td>0b11</td><td>0b1</td><td>0b1</td><td>0b0</td><td>0b00</td><td>0b0</td></tr><tr><td>Guest OS TLBI by ASID and VA</td><td>v7</td><td>0b10</td><td>0b11</td><td>0b1</td><td>0b1</td><td>0b0</td><td>0b00</td><td>0b1</td></tr><tr><td>Guest OS TLBI by ASID and VA, Leaf only</td><td>v8</td><td>0b10</td><td>0b11</td><td>0b1</td><td>0b1</td><td>0b1</td><td>0b00</td><td>0b1</td></tr><tr><td>Secure Hypervisor TLBI all</td><td>v8.4</td><td>0b11</td><td>0b10</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b0</td></tr><tr><td>Secure Hypervisor TLBI by VA</td><td>v8.4</td><td>0b11</td><td>0b10</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b1</td></tr><tr><td>Secure Hypervisor TLBI by VA, Leaf only</td><td>v8.4</td><td>0b11</td><td>0b10</td><td>0b0</td><td>0b0</td><td>0b1</td><td>0b00</td><td>0b1</td></tr><tr><td>Secure Hypervisor TLBI by ASID</td><td>v8.4</td><td>0b11</td><td>0b10</td><td>0b0</td><td>0b1</td><td>0b0</td><td>0b00</td><td>0b0</td></tr><tr><td>Secure Hypervisor TLBI by ASID and VA</td><td>v8.4</td><td>0b11</td><td>0b10</td><td>0b0</td><td>0b1</td><td>0b0</td><td>0b00</td><td>0b1</td></tr><tr><td>Secure Hypervisor TLBI by ASID and VA, Leaf only</td><td>v8.4</td><td>0b11</td><td>0b10</td><td>0b0</td><td>0b1</td><td>0b1</td><td>0b00</td><td>0b1</td></tr><tr><td>Hypervisor TLBI all</td><td>v7</td><td>0b11</td><td>0b11</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b0</td></tr><tr><td>Hypervisor TLBI by VA</td><td>v7</td><td>0b11</td><td>0b11</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b1</td></tr></table>

Continued on next page

Table A15.8 – Continuedfrom previous page
<table><tr><td>Operation</td><td>Arm</td><td>Exception</td><td>Security</td><td>VMIDV</td><td>ASIDV</td><td>Leaf</td><td>Stage</td><td>Addr</td></tr><tr><td>Hypervisor TLBI by VA, Leaf only</td><td>v8</td><td>0b11</td><td>0b11</td><td>0b0</td><td>0b0</td><td>0b1</td><td>0b00</td><td>0b1</td></tr><tr><td>Hypervisor TLBI by ASID</td><td>v8.1</td><td>0b11</td><td>0b11</td><td>0b0</td><td>0b1</td><td>0b0</td><td>0b00</td><td>0b0</td></tr><tr><td>Hypervisor TLBI by ASID and VA</td><td>v8.1</td><td>0b11</td><td>0b11</td><td>0b0</td><td>0b1</td><td>0b0</td><td>0b00</td><td>0b1</td></tr><tr><td>Hypervisor TLBI by ASID and VA, Leaf only</td><td>v8.1</td><td>0b11</td><td>0b11</td><td>0b0</td><td>0b1</td><td>0b1</td><td>0b00</td><td>0b1</td></tr><tr><td>Realm TLBI all</td><td>v9.2</td><td>0b10</td><td>0b00</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b0</td></tr><tr><td>Realm Guest OS TLBI all, Stage 1 only</td><td>v9.2</td><td>0b10</td><td>0b00</td><td>0b1</td><td>0b0</td><td>0b0</td><td>0b01</td><td>0b0</td></tr><tr><td>Realm Guest OS TLBI all, Stage 1 and 2</td><td>v9.2</td><td>0b10</td><td>0b00</td><td>0b1</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b0</td></tr><tr><td>Realm Guest OS TLBI by VA</td><td>v9.2</td><td>0b10</td><td>0b00</td><td>0b1</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b1</td></tr><tr><td>Realm Guest OS TLBI by VA, Leaf only</td><td>v9.2</td><td>0b10</td><td>0b00</td><td>0b1</td><td>0b0</td><td>0b1</td><td>0b00</td><td>0b1</td></tr><tr><td>Realm Guest OS TLBI by ASID</td><td>v9.2</td><td>0b10</td><td>0b00</td><td>0b1</td><td>0b1</td><td>0b0</td><td>0b00</td><td>0b0</td></tr><tr><td>Realm Guest OS TLBI by ASID and VA</td><td>v9.2</td><td>0b10</td><td>0b00</td><td>0b1</td><td>0b1</td><td>0b0</td><td>0b00</td><td>0b1</td></tr><tr><td>Realm Guest OS TLBI by ASID and VA, Leaf only</td><td>v9.2</td><td>0b10</td><td>0b00</td><td>0b1</td><td>0b1</td><td>0b1</td><td>0b00</td><td>0b1</td></tr><tr><td>Realm Guest OS TLBI by IPA</td><td>v9.2</td><td>0b10</td><td>0b00</td><td>0b1</td><td>0b0</td><td>0b0</td><td>0b10</td><td>0b1</td></tr><tr><td>Realm Guest OS TLBI by IPA, Leaf only</td><td>v9.2</td><td>0b10</td><td>0b00</td><td>0b1</td><td>0b0</td><td>0b1</td><td>0b10</td><td>0b1</td></tr><tr><td>Realm Hypervisor TLBI all</td><td>v9.2</td><td>0b11</td><td>0b00</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b0</td></tr><tr><td>Realm Hypervisor TLBI by VA</td><td>v9.2</td><td>0b11</td><td>0b00</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b00</td><td>0b1</td></tr><tr><td>Realm Hypervisor TLBI by VA, Leaf only</td><td>v9.2</td><td>0b11</td><td>0b00</td><td>0b0</td><td>0b0</td><td>0b1</td><td>0b00</td><td>0b1</td></tr><tr><td>Realm Hypervisor TLBI by ASID</td><td>v9.2</td><td>0b11</td><td>0b00</td><td>0b0</td><td>0b1</td><td>0b0</td><td>0b00</td><td>0b0</td></tr><tr><td>Realm Hypervisor TLBI by ASID and VA</td><td>v9.2</td><td>0b11</td><td>0b00</td><td>0b0</td><td>0b1</td><td>0b0</td><td>0b00</td><td>0b1</td></tr><tr><td>Realm Hypervisor TLBI by ASID and VA, Leaf only</td><td>v9.2</td><td>0b11</td><td>0b00</td><td>0b0</td><td>0b1</td><td>0b1</td><td>0b00</td><td>0b1</td></tr><tr><td>GPT TLBI by PA</td><td>v9.2</td><td>0b01</td><td>0b10</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b11</td><td>0b1</td></tr><tr><td>GPT TLBI by PA, Leaf only</td><td>v9.2</td><td>0b01</td><td>0b10</td><td>0b0</td><td>0b0</td><td>0b1</td><td>0b11</td><td>0b1</td></tr><tr><td>GPT TLBI all</td><td>v9.2</td><td>0b01</td><td>0b10</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b11</td><td>0b0</td></tr></table>

## Range field

The Range field indicates that an invalidation operates on a range of addresses.

Range can be 0b1 for messages where both of the following apply:

• Arm is v8.4 or later.

• The Addr bit is 0b1, so the message includes an address.

## Range based TLB Invalidate by IPA or VA

When the Range field is 0b1 for a TLBI by VA or IPA, the address range to invalidate is calculated using the following formula:

BaseAddr ≤ AddressRange < BaseAddr+(Num + 1) × 2<sup>(5×Scale+1)</sup> × T ranslation\_Granule\_Size

Where:

• Translation\_Granule\_Size in bytes is determined from the TG value provided in the message. See Table A15.3 for encodings.

• Scale is provided in the message, it can take any value from 0-3.

• Num is provided in the message, it can take any value from 0-31.

• BaseAddr is the base address of the range, based on TG:

– 4K: BaseAddr is VA[MaxVA:12].

– 16K: BaseAddr is VA[MaxVA:14], VA[13:12] must be zero.

– 64K: BaseAddr is VA[MaxVA:16], VA[15:12] must be zero.

A TLBI by Range is a 2-part message with field mappings described in Table A15.20.

## GPT TLB Invalidate

Granule Protection Table (GPT) TLBI by PA operations perform range-based invalidation and invalidate TLB entries starting from the PA, within the range as specified in the Invalidation Size (IS) field. See Table A15.3 for encodings.

If the PA is not aligned to the IS value, no TLB entries are required to be invalidated.

The IS field is applicable only in GPT TLBI by PA operations.

• A GPT TLBI all message is signaled using a 1-part message with the Range field set to 0b0.

• A GPT TLBI by PA message is signaled using a 2-part message with the Range field set to 0b1.

The field to signal mappings for GPT TLBI messages are shown in Table A15.20.

## A15.3.3 Branch Predictor Invalidate messages

The Branch Predictor Invalidate (BPI) message is used to invalidate virtual addresses from branch predictors.   
A BPI message is signaled using a 1-part or 2-part message with field to signal mappings detailed in Table A15.21.   
The fixed field values for a BPI message are shown in Table A15.9.

Table A15.9: Fixed field values for a BPI message
<table><tr><td>Name</td><td>Value</td><td>Meaning</td></tr><tr><td>DVMType</td><td>0b001</td><td>Branch Predictor Invalidate opcode</td></tr><tr><td>Completion</td><td>0b0</td><td>Completion not required</td></tr><tr><td>Range</td><td>0b0</td><td>Address is not a range</td></tr><tr><td>VMIDV</td><td>0b0</td><td>VMID field not valid</td></tr><tr><td>ASIDV</td><td>0b0</td><td>ASID field not valid</td></tr><tr><td>Exception</td><td>0b00</td><td>Hypervisor and all Guest OS</td></tr><tr><td>Security</td><td>0b00</td><td>Secure and Non-secure</td></tr><tr><td>Leaf</td><td>0b0</td><td>Leaf information is N/A</td></tr><tr><td>Stage</td><td>0b00</td><td>Stage information is N/A</td></tr></table>

All supported BPI operations are shown in Table A15.10.

The Arm column indicates the minimum Arm architecture version required to support the message.

Table A15.10: BPI messages
<table><tr><td>Operation</td><td>Arm</td><td>Addr</td></tr><tr><td>Branch Predictor Invalidate all</td><td>v7</td><td>0b0</td></tr><tr><td>Branch Predictor Invalidate by VA</td><td>v7</td><td>0b1</td></tr></table>

## A15.3.4 Instruction cache invalidations

Instruction caches can use either a physical address or a virtual address to tag the data they contain. A system might contain a mixture of both forms of cache.

The DVM protocol includes instruction cache invalidation operations that use physical addresses and operations that use virtual addresses. A component that receives DVM messages must support both forms of message, independent of the style of instruction cache implemented. It might be necessary to over-invalidate in the case where a message is received in a format that is not native to the cache type.

## Physical Instruction Cache Invalidate

This section lists the Physical Instruction Cache Invalidate (PICI) operations that the DVM message supports.   
This message type is also used for Instruction Caches which are Virtually Indexed Physically Tagged (VIPT).

A PICI message is signaled using a 1-part or 2-part message with field to signal mappings detailed in Table A15.22. The fixed field values for a PICI message are shown in Table A15.11.

Table A15.11: Fixed field values for a PICI message
<table><tr><td>Name</td><td>Value</td><td>Meaning</td></tr><tr><td>DVMType</td><td>0b010</td><td>Physical Instruction Cache Invalidate opcode</td></tr><tr><td>Completion</td><td>0b0</td><td>Completion not required</td></tr><tr><td>Range</td><td>0b0</td><td>Address is not a range</td></tr><tr><td>Exception</td><td>0b00</td><td>Hypervisor and all Guest OS</td></tr><tr><td>Leaf</td><td>0b0</td><td>Leaf information is N/A</td></tr><tr><td>Stage</td><td>0b00</td><td>Stage information is N/A</td></tr></table>

All supported PICI operations are shown in Table A15.12.

Table A15.12: PICI messages
<table><tr><td>Operation</td><td>Arm</td><td>Security</td><td>VIV</td><td>Addr</td></tr><tr><td>PICI all Root, Realm, Secure and Non-secure</td><td>v9.2</td><td>0b00</td><td>0b00</td><td>0b0</td></tr><tr><td>PICI by PA without Virtual Index, Root only</td><td>v9.2</td><td>0b00</td><td>0b00</td><td>0b1</td></tr><tr><td>PICI by PA with Virtual Index, Root only</td><td>v9.2</td><td>0b00</td><td>0b11</td><td>0b1</td></tr><tr><td>PICI all Realm and Non-secure</td><td>v9.2</td><td>0b01</td><td>0b00</td><td>0b0</td></tr><tr><td>PICI by PA without Virtual Index, Realm only</td><td>v9.2</td><td>0b01</td><td>0b00</td><td>0b1</td></tr><tr><td>PICI by PA with Virtual Index, Realm only</td><td>v9.2</td><td>0b01</td><td>0b11</td><td>0b1</td></tr><tr><td>PICI all Secure and Non-secure</td><td>v7</td><td>0b10</td><td>0b00</td><td>0b0</td></tr><tr><td>PICI by PA without Virtual Index, Secure only</td><td>v7</td><td>0b10</td><td>0b00</td><td>0b1</td></tr><tr><td>PICI by PA with Virtual Index, Secure only</td><td>v7</td><td>0b10</td><td>0b11</td><td>0b1</td></tr><tr><td>PICI all, Non-secure only</td><td>v7</td><td>0b11</td><td>0b00</td><td>0b0</td></tr><tr><td>PICI by PA without Virtual Index, Non-secure only</td><td>v7</td><td>0b11</td><td>0b00</td><td>0b1</td></tr><tr><td>PICI by PA with Virtual Index, Non-secure only</td><td>v7</td><td>0b11</td><td>0b11</td><td>0b1</td></tr></table>

When the Virtual Index Valid (VIV) field is 0b11, then VI[27:12] is used as part of the Physical Address. Note that in previous issues of this specification, a PICI all with Security value of 0b10 was incorrectly labeled as Secure only when it should have been Secure and Non-secure.

## Virtual Instruction Cache Invalidate

This section lists the Virtual Instruction Cache Invalidate (VICI) operations that the DVM message supports. A VICI message is signaled using a 1-part or 2-part message with field to signal mappings detailed in Table A15.22.

The fixed field values for a VICI message are shown in Table A15.13.

Table A15.13: Fixed field values for a VICI message
<table><tr><td>Name</td><td>Value</td><td>Meaning</td></tr><tr><td>DVMType</td><td>0b011</td><td>Virtual Instruction Cache Invalidate opcode</td></tr><tr><td>Completion</td><td>0b0</td><td>Completion not required</td></tr><tr><td>Range</td><td>0b0</td><td>Address is not a range</td></tr><tr><td>Leaf</td><td>0b0</td><td>Leaf information is N/A</td></tr><tr><td>Stage</td><td>0b00</td><td>Stage information is N/A</td></tr></table>

All supported VICI operations are shown in Table A15.14.

The Arm column indicates the minimum Arm architecture version required to support the message.

Table A15.14: VICI messages
<table><tr><td>Operation</td><td>Arm</td><td>Exception</td><td>Security</td><td>VMIDV</td><td>ASIDV</td><td>Addr</td></tr><tr><td>Hypervisor and all Guest OS VICI all, Secure and Non-secure</td><td>v7</td><td>0b00</td><td>0b00</td><td>0b0</td><td>0b0</td><td>0b0</td></tr><tr><td>Hypervisor and all Guest OS VICI all, Non-secure only</td><td>v7</td><td>0b00</td><td>0b11</td><td>0b0</td><td>0b0</td><td>0b0</td></tr><tr><td>All Guest OS VICI by ASID and VA, Secure only</td><td>v7</td><td>0b10</td><td>0b10</td><td>0b0</td><td>0b1</td><td>0b1</td></tr><tr><td>All Guest OS VICI by VMID, Secure only</td><td>v8.4</td><td>0b10</td><td>0b10</td><td>0b1</td><td>0b0</td><td>0b0</td></tr><tr><td>All Guest OS VICI by ASID, VA and VMID, Secure only</td><td>v8.4</td><td>0b10</td><td>0b10</td><td>0b1</td><td>0b1</td><td>0b1</td></tr><tr><td>All Guest OS VICI by VMID, Non-secure only</td><td>v7</td><td>0b10</td><td>0b11</td><td>0b1</td><td>0b0</td><td>0b0</td></tr><tr><td>All Guest OS VICI by ASID, VA and VMID, Non-secure only</td><td>v7</td><td>0b10</td><td>0b11</td><td>0b1</td><td>0b1</td><td>0b1</td></tr><tr><td>Hypervisor VICI by VA, Non-secure only</td><td>v7</td><td>0b11</td><td>0b11</td><td>0b0</td><td>0b0</td><td>0b1</td></tr><tr><td>Hypervisor VICI by ASID and VA, Non-secure only</td><td>v8.1</td><td>0b11</td><td>0b11</td><td>0b0</td><td>0b1</td><td>0b1</td></tr></table>

## A15.3.5 Synchronization message

A Synchronization (Sync) message is used when the requester needs to know when all previous invalidations are complete. For more information on how to use the Sync message, see A15.5 DVM Sync and Complete

A Sync message is signaled using a 1-part message with field to signal mappings detailed in Table A15.21.

The fixed field values for a Sync message are shown in Table A15.15.

Table A15.15: Fixed field values for a Sync message
<table><tr><td>Name</td><td>Value</td><td>Meaning</td></tr><tr><td>DVMType</td><td>0b100</td><td>Sync opcode</td></tr><tr><td>Completion</td><td>0b1</td><td>Completion required</td></tr><tr><td>ASIDV</td><td>0b0</td><td>No ASID information</td></tr><tr><td>VMIDV</td><td>0b0</td><td>No VMID information</td></tr><tr><td>Addr</td><td>0b0</td><td>No address information</td></tr><tr><td>Range</td><td>0b0</td><td>No address range</td></tr><tr><td>Exception</td><td>0b00</td><td>Exception information is N/A</td></tr><tr><td>Security</td><td>0b00</td><td>Security information is N/A</td></tr><tr><td>Leaf</td><td>0b0</td><td>Leaf information is N/A</td></tr><tr><td>Stage</td><td>0b00</td><td>Stage information is N/A</td></tr></table>

## A15.3.6 Hint message

A reserved message address space is provided for future Hint messages.

The fixed field values for a Hint message are shown in Table A15.16.

Table A15.16: Fixed field values for a Hint message
<table><tr><td>Name</td><td>Value</td><td>Meaning</td></tr><tr><td>DVMType</td><td>0b110</td><td>Hint opcode</td></tr><tr><td>Completion</td><td>0b0</td><td>Completion not required</td></tr></table>

## A15.4 Transporting DVM messages

To transport DVM messages, two channels are added to an interface:

• Snoop request channel, used to transfer DVM message requests. Signals on this channel have the prefix AC.

• Snoop response channel, used to transfer DVM message responses. Signals on this channel have the prefix CR.

A DVM message transaction consists of one request transfer on the snoop request channel and one response on the snoop response channel. There can be one or two transactions per message, the Addr field in the first request indicates if another transaction is required.

DVM messages that do not include an address are sent using one transaction.

DVM messages that include an address are sent using two transactions.

An interconnect is usually used to replicate and distribute DVM message requests to participating Manager components. Managers can use the Coherency Connection signaling to opt into receiving messages at runtime, see A15.6 Coherency Connection signaling.

Flows for one-part and two-part messages are shown in Figure A15.1.

![](images/009868cc79ad12e71ceb79b4d9462aa0991557b1f1d7e36a696cfacd7cc97538.jpg)  
Figure A15.1: DVM message flows

The following rules apply to two-part DVM messages:

• The requests are always sent as successive transfers, with no other message requests between them.

• A component issuing a two-part DVM message must be able to issue the second part of the message without requiring a response to the first part of the message.

## A15.4.1 Signaling for DVM messages

Snoop channels for DVM messages use the same transport as the other AXI channels as determined by the AXI\_Transport property. See A2.2 AXI transport options for more details on transport.

DVM message requests use the snoop request channel from a Subordinate to a Manager interface. Table A15.17 shows the signals that can be included in the snoop request channel.

Table A15.17: Snoop request channel
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Presence</td><td>Description</td></tr><tr><td>ACVALID</td><td>1</td><td>Subordinate</td><td>DVM_Message_Support</td><td>DVM message request valid indicator.</td></tr><tr><td>ACREADY</td><td>1</td><td>Manager</td><td>DVM_Message_Support and AXI_Transport == Ready</td><td>DVM message request ready indicator.</td></tr><tr><td>ACPENDING</td><td>1</td><td>Subordinate</td><td>DVM_Message_Support and AXI_Transport == Credited</td><td>Pending signal for the AC channel.</td></tr><tr><td>ACCRDT</td><td>1</td><td>Manager</td><td>DVM_Message_Support and AXI_Transport == Credited</td><td>Asserted high to give one DVM message request credit.</td></tr><tr><td>ACADDR</td><td>ADDR_WIDTH</td><td>Subordinate</td><td>DVM_Message_Support</td><td>Used to carry the payload for DVM message requests.</td></tr><tr><td>ACVMIDEXT</td><td>4</td><td>Subordinate</td><td>DVM_Message_Support and (DVM_v8.1 or DVM_v8.4 or DVM_v9.2)</td><td>Extension to support 16-bit VMID in DVM messages.</td></tr><tr><td>ACTRACE</td><td>1</td><td>Subordinate</td><td>DVM_Message_Support and Trace_Signals</td><td>Trace signal for the AC channel.</td></tr></table>

The response to a DVM request is transported on the snoop response channel from a Manager to a Subordinate interface. Table A15.18 shows the signals that can be included in the snoop response channel.

Table A15.18: Snoop response channel
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Presence</td><td>Description</td></tr><tr><td>CRVALID</td><td>1</td><td>Manager</td><td>DVM_Message_Support</td><td>DVM message response valid indicator.</td></tr><tr><td>CRREADY</td><td>1</td><td>Subordinate</td><td>DVM_Message_Support and AXI_Transport == Ready</td><td>DVM message response ready indicator.</td></tr><tr><td>CRPENDING</td><td>1</td><td>Manager</td><td>DVM_Message_Support and AXI_Transport == Credited</td><td>Pending signal for the CR channel.</td></tr><tr><td>CRCRDT</td><td>1</td><td>Subordinate</td><td>DVM_Message_Support and AXI_Transport == Credited</td><td>Asserted high to give one DVM message response credit.</td></tr><tr><td>CRTRACE</td><td>1</td><td>Manager</td><td>DVM_Message_Support and Trace_Signals</td><td>Trace signal for the CR channel.</td></tr></table>

A DVM response acknowledges that the request has been received but does not indicate the success or failure of a

DVM message. Reordering is not supported on the AC or CR channels, so responses are returned in the same order as the AC requests were issued.

The ACTRACE and CRTRACE signals act the same as trace signals on other channels, see A12.3 Trace signals for more information.

## A15.4.2 Snoop channels using Valid-Ready transport

When using a Valid-Ready transport, the following rules apply:

• ACVALID must only be asserted by a Subordinate when there is valid address and control information.

• When asserted, ACVALID must remain asserted until the rising clock edge after the Manager asserts the ACREADY signal.

• CRVALID is asserted to indicate that the Manager has acknowledged the DVM message.

• When asserted, CRVALID must remain asserted until the rising clock edge after the Subordinate asserts the CRREADY signal.

The rules for dependencies between the snoop request and response channels are listed below and illustrated in Figure A15.2.

• The Subordinate must not wait for the Manager to assert ACREADY before asserting ACVALID.

• The Manager can wait for ACVALID to be asserted before it asserts ACREADY.

• The Manager can assert ACREADY before ACVALID is asserted.

• The Manager must wait for both ACVALID and ACREADY to be asserted before it asserts CRVALID to indicate that a valid response is available.

• The Manager must not wait for the Subordinate to assert CRREADY before asserting CRVALID.

• The Subordinate can wait for CRVALID to be asserted before it asserts CRREADY.

• The Subordinate can assert CRREADY before CRVALID is asserted.

![](images/3c537cb9a48ad7e84cb54a53f149615917a789191b50d11aecebedcec1868c39.jpg)  
Figure A15.2: Snoop transaction handshake dependencies

## A15.4.3 Snoop channels using credited transport

When using credited transport, the rules of A2.4 Credited transport and A2.4.4 Transfer-level clock gating apply to the snoop channels. In addition:

• The Manager must wait for a DVM message request before sending a DVM message response.

• Multiple Resource Planes and shared credits are not supported on the snoop channels.

## A15.4.4 Address widths in DVM messages

The property ADDR\_WIDTH is used to specify the width of ARADDR, AWADDR, and ACADDR. This sets the physical address width used by an interface.

The ACADDR signal is also used to transport the Virtual Address (VA), so the required VA width also sets a minimum constraint on ADDR\_WIDTH. Table A15.19 shows some common VA widths and the minimum ADDR\_WIDTH required.

Table A15.19: Common VA widths and minimum ADDR\_WIDTH
<table><tr><td>VA width</td><td>Minimum ADDR_WIDTH</td></tr><tr><td>32</td><td>32</td></tr><tr><td>41</td><td>40</td></tr><tr><td>49</td><td>44</td></tr><tr><td>53</td><td>48</td></tr><tr><td>57</td><td>48</td></tr></table>

VA widths greater than 57-bits are not supported.

If the PA width exceeds the VA width, then virtual address operations might receive additional address information in a DVM message. In this case, any additional address information must be ignored and operations performed using only the supported address bits.

If a component supports a larger VA width than its PA width, the component must take appropriate action regarding the additional physical address bits. See A3.1.5 Transfer address for more details on mismatched address widths.

## A15.4.5 Mapping message fields to signals

The fields in DVM messages are transported using bits of the ACADDR and ACVMIDEXT signals.

There are different mappings for each message type, shown in the tables below. The bit position allocation might appear irregular but is used to ease the translation between implementations with different address widths.

For Hint messages, the Completion (0b0) and DVMType (0b110) fields are at ACADDR[15] and ACADDR[14:12] respectively, other mappings are IMPLEMENTATION DEFINED.

The mappings for TLB Invalidate messages are shown in Table A15.20.

Table A15.20: Field mappings for TLB Invalidate messages
<table><tr><td>Signal</td><td>TLBI 1-part</td><td>TLBI 1st of 2-part</td><td>TLBI 2nd part by VA or IPA</td><td>TLBI 2nd part by range</td><td>GPT TLBI 1st part</td><td>GPT TLBI 2nd part</td></tr><tr><td>ACADDR[51]</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b0</td><td>PA[51]</td></tr><tr><td>ACADDR[50]</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b0</td><td>PA[50]</td></tr><tr><td>ACADDR[49]</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b0</td><td>PA[49]</td></tr><tr><td>ACADDR[48]</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b0</td><td>PA[48]</td></tr><tr><td>ACADDR[47]</td><td>0b0</td><td>VA[56]</td><td>VA[52]</td><td>VA[52]</td><td>0b0</td><td>PA[47]</td></tr><tr><td>ACADDR[46]</td><td>0b0</td><td>VA[55]</td><td>VA[51]</td><td>VA[51]</td><td>0b0</td><td>PA[46]</td></tr><tr><td>ACADDR[45]</td><td>0b0</td><td>VA[54]</td><td>VA[50]</td><td>VA[50]</td><td>0b0</td><td>PA[45]</td></tr><tr><td>ACADDR[44]</td><td>0b0</td><td>VA[53]</td><td>VA[49]</td><td>VA[49]</td><td>0b0</td><td>PA[44]</td></tr><tr><td>ACADDR[43]</td><td>VMID[15]</td><td>VA[48]</td><td>VA[44]</td><td>VA[44]</td><td>0b0</td><td>PA[43]</td></tr><tr><td>ACADDR[42]</td><td>VMID[14]</td><td>VA[47]</td><td>VA[43]</td><td>VA[43]</td><td>0b0</td><td>PA[42]</td></tr><tr><td>ACADDR[41]</td><td>VMID[13]</td><td>VA[46]</td><td>VA[42]</td><td>VA[42]</td><td>0b0</td><td>PA[41]</td></tr><tr><td>ACADDR[40]</td><td>VMID[12]</td><td>VA[45]</td><td>VA[41]</td><td>VA[41]</td><td>0b0</td><td>PA[40]</td></tr><tr><td>ACADDR[39]</td><td>ASID[15]</td><td>ASID[15]</td><td>VA[39]</td><td>VA[39]</td><td>0b0</td><td>PA[39]</td></tr><tr><td>ACADDR[38]</td><td>ASID[14]</td><td>ASID[14]</td><td>VA[38]</td><td>VA[38]</td><td>0b0</td><td>PA[38]</td></tr><tr><td>ACADDR[37]</td><td>ASID[13]</td><td>ASID[13]</td><td>VA[37]</td><td>VA[37]</td><td>0b0</td><td>PA[37]</td></tr><tr><td>ACADDR[36]</td><td>ASID[12]</td><td>ASID[12]</td><td>VA[36]</td><td>VA[36]</td><td>0b0</td><td>PA[36]</td></tr><tr><td>ACADDR[35]</td><td>ASID[11]</td><td>ASID[11]</td><td>VA[35]</td><td>VA[35]</td><td>0b0</td><td>PA[35]</td></tr><tr><td>ACADDR[34]</td><td>ASID[10]</td><td>ASID[10]</td><td>VA[34]</td><td>VA[34]</td><td>0b0</td><td>PA[34]</td></tr><tr><td>ACADDR[33]</td><td>ASID[9]</td><td>ASID[9]</td><td>VA[33]</td><td>VA[33]</td><td>0b0</td><td>PA[33]</td></tr><tr><td>ACADDR[32]</td><td>ASID[8]</td><td>ASID[8]</td><td>VA[32]</td><td>VA[32]</td><td>0b0</td><td>PA[32]</td></tr><tr><td>ACADDR[31]</td><td>VMID[7]</td><td>VMID[7]</td><td>VA[31]</td><td>VA[31]</td><td>0b0</td><td>PA[31]</td></tr><tr><td>ACADDR[30]</td><td>VMID[6]</td><td>VMID[6]</td><td>VA[30]</td><td>VA[30]</td><td>0b0</td><td>PA[30]</td></tr><tr><td>ACADDR[29]</td><td>VMID[5]</td><td>VMID[5]</td><td>VA[29]</td><td>VA[29]</td><td>0b0</td><td>PA[29]</td></tr><tr><td>ACADDR[28]</td><td>VMID[4]</td><td>VMID[4]</td><td>VA[28]</td><td>VA[28]</td><td>0b0</td><td>PA[28]</td></tr><tr><td>ACADDR[27]</td><td>VMID[3]</td><td>VMID[3]</td><td>VA[27]</td><td>VA[27]</td><td>0b0</td><td>PA[27]</td></tr><tr><td>ACADDR[26]</td><td>VMID[2]</td><td>VMID[2]</td><td>VA[26]</td><td>VA[26]</td><td>0b0</td><td>PA[26]</td></tr><tr><td>ACADDR[25]</td><td>VMID[1]</td><td>VMID[1]</td><td>VA[25]</td><td>VA[25]</td><td>0b0</td><td>PA[25]</td></tr><tr><td>ACADDR[24]</td><td>VMID[0]</td><td>VMID[0]</td><td>VA[24]</td><td>VA[24]</td><td>0b0</td><td>PA[24]</td></tr><tr><td>ACADDR[23]</td><td>ASID[7]</td><td>ASID[7]</td><td>VA[23]</td><td>VA[23]</td><td>0b0</td><td>PA[23]</td></tr><tr><td>ACADDR[22]</td><td>ASID[6]</td><td>ASID[6]</td><td>VA[22]</td><td>VA[22]</td><td>0b0</td><td>PA[22]</td></tr><tr><td>ACADDR[21]</td><td>ASID[5]</td><td>ASID[5]</td><td>VA[21]</td><td>VA[21]</td><td>0b0</td><td>PA[21]</td></tr></table>

Continued on next page

Chapter A15. Distributed Virtual Memory messages A15.4. Transporting DVM messages  
Table A15.20 – Continued from previous page
<table><tr><td>Signal</td><td>TLBI 1-part</td><td>TLBI 1st of 2-part</td><td>TLBI 2nd part by VA or IPA</td><td>TLBI 2nd part by range</td><td>GPT TLBI 1st part</td><td>GPT TLBI 2nd part</td></tr><tr><td>ACADDR[20]</td><td>ASID[4]</td><td>ASID[4]</td><td>VA[20]</td><td>VA[20]</td><td>0b0</td><td>PA[20]</td></tr><tr><td>ACADDR[19]</td><td>ASID[3]</td><td>ASID[3]</td><td>VA[19]</td><td>VA[19]</td><td>0b0</td><td>PA[19]</td></tr><tr><td>ACADDR[18]</td><td>ASID[2]</td><td>ASID[2]</td><td>VA[18]</td><td>VA[18]</td><td>0b0</td><td>PA[18]</td></tr><tr><td>ACADDR[17]</td><td>ASID[1]</td><td>ASID[1]</td><td>VA[17]</td><td>VA[17]</td><td>0b0</td><td>PA[17]</td></tr><tr><td>ACADDR[16]</td><td>ASID[0]</td><td>ASID[0]</td><td>VA[16]</td><td>VA[16]</td><td>0b0</td><td>PA[16]</td></tr><tr><td>ACADDR[15]</td><td>0b0 (Completion)</td><td>0b0 (Completion)</td><td>VA[15]</td><td>VA[15]</td><td>0b0 (Completion)</td><td>PA[15]</td></tr><tr><td>ACADDR[14]</td><td>0b0 (DVMType[2])</td><td>0b0 (DVMType[2])</td><td>VA[14]</td><td>VA[14]</td><td>0b0 (DVMType[2])</td><td>PA[14]</td></tr><tr><td>ACADDR[13]</td><td>0b0 (DVMType[1])</td><td>0b0 (DVMType[1])</td><td>VA[13]</td><td>VA[13]</td><td>0b0 (DVMType[1])</td><td>PA[13]</td></tr><tr><td>ACADDR[12]</td><td>0b0 (DVMType[0])</td><td>0b0 (DVMType[0])</td><td>VA[12]</td><td>VA[12]</td><td>0b0 (DVMType[0])</td><td>PA[12]</td></tr><tr><td>ACADDR[11]</td><td>Exception[1]</td><td>Exception[1]</td><td>TG[1]</td><td>TG[1]</td><td>Exception[1]</td><td>IS[3]</td></tr><tr><td>ACADDR[10]</td><td>Exception[0]</td><td>Exception[0]</td><td>TG[0]</td><td>TG[0]</td><td>Exception[0]</td><td>IS[2]</td></tr><tr><td>ACADDR[9]</td><td>Security[1]</td><td>Security[1]</td><td>TTL[1]</td><td>TTL[1]</td><td>Security[1]</td><td>IS[1]</td></tr><tr><td>ACADDR[8]</td><td>Security[0]</td><td>Security[0]</td><td>TTL[0]</td><td>TTL[0]</td><td>Security[0]</td><td>IS[0]</td></tr><tr><td>ACADDR[7]</td><td>0b0 (Range)</td><td>Range</td><td>0b0</td><td>Scale[1]</td><td>Range</td><td>0b0</td></tr><tr><td>ACADDR[6]</td><td>VMIDV</td><td>VMIDV</td><td>0b0</td><td>Scale[0]</td><td>0b0 (VMIDV)</td><td>0b0</td></tr><tr><td>ACADDR[5]</td><td>ASIDV</td><td>ASIDV</td><td>0b0</td><td>Num[4]</td><td>0b0 (ASIDV)</td><td>0b0</td></tr><tr><td>ACADDR[4]</td><td>0b0</td><td>Leaf</td><td>0b0</td><td>Num[3]</td><td>Leaf</td><td>0b0</td></tr><tr><td>ACADDR[3]</td><td>Stage[1]</td><td>Stage[1]</td><td>VA[40]</td><td>VA[40]</td><td>Stage[1]</td><td>0b0</td></tr><tr><td>ACADDR[2]</td><td>Stage[0]</td><td>Stage[0]</td><td>0b0</td><td>Num[2]</td><td>Stage[0]</td><td>0b0</td></tr><tr><td>ACADDR[1]</td><td>0b0</td><td>0b0</td><td>0b0</td><td>Num[1]</td><td>0b0</td><td>0b0</td></tr><tr><td>ACADDR[0]</td><td>0b0 (Addr)</td><td>0b1 (Addr)</td><td>0b0</td><td>Num[0]</td><td>Addr</td><td>0b0</td></tr><tr><td>ACVMIDEXT[3]</td><td>VMID[11]</td><td>VMID[11]</td><td>VMID[15]</td><td>VMID[15]</td><td>0b0</td><td>0b0</td></tr><tr><td>ACVMIDEXT[2]</td><td>VMID[10]</td><td>VMID[10]</td><td>VMID[14]</td><td>VMID[14]</td><td>0b0</td><td>0b0</td></tr><tr><td>ACVMIDEXT[1]</td><td>VMID[9]</td><td>VMID[9]</td><td>VMID[13]</td><td>VMID[13]</td><td>0b0</td><td>0b0</td></tr><tr><td>ACVMIDEXT[0]</td><td>VMID[8]</td><td>VMID[8]</td><td>VMID[12]</td><td>VMID[12]</td><td>0b0</td><td>0b0</td></tr></table>

The mappings for Branch Predictor Invalidate and Sync messages are shown in Table A15.21.

Table A15.21: Field mappings for BPI and Sync messages
<table><tr><td>Signal</td><td>BPI all or Sync</td><td>BPI by VA 1st part</td><td>BPI by VA 2nd part</td></tr><tr><td>ACADDR[51]</td><td>0b0</td><td>0b0</td><td>0b0</td></tr><tr><td>ACADDR[50]</td><td>0b0</td><td>0b0</td><td>0b0</td></tr><tr><td>ACADDR[49]</td><td>0b0</td><td>0b0</td><td>0b0</td></tr><tr><td>ACADDR[48]</td><td>0b0</td><td>0b0</td><td>0b0</td></tr><tr><td>ACADDR[47]</td><td>0b0</td><td>VA[56]</td><td>VA[52]</td></tr><tr><td>ACADDR[46]</td><td>0b0</td><td>VA[55]</td><td>VA[51]</td></tr><tr><td>ACADDR[45]</td><td>0b0</td><td>VA[54]</td><td>VA[50]</td></tr><tr><td>ACADDR[44]</td><td>0b0</td><td>VA[53]</td><td>VA[49]</td></tr><tr><td>ACADDR[43]</td><td>0b0</td><td>VA[48]</td><td>VA[44]</td></tr><tr><td>ACADDR[42]</td><td>0b0</td><td>VA[47]</td><td>VA[43]</td></tr><tr><td>ACADDR[41]</td><td>0b0</td><td>VA[46]</td><td>VA[42]</td></tr><tr><td>ACADDR[40]</td><td>0b0</td><td>VA[45]</td><td>VA[41]</td></tr><tr><td>ACADDR[39]</td><td>0b0</td><td>0b0</td><td>VA[39]</td></tr><tr><td>ACADDR[38]</td><td>0b0</td><td>0b0</td><td>VA[38]</td></tr><tr><td>ACADDR[37]</td><td>0b0</td><td>0b0</td><td>VA[37]</td></tr><tr><td>ACADDR[36]</td><td>0b0</td><td>0b0</td><td>VA[36]</td></tr><tr><td>ACADDR[35]</td><td>0b0</td><td>0b0</td><td>VA[35]</td></tr><tr><td>ACADDR[34]</td><td>0b0</td><td>0b0</td><td>VA[34]</td></tr><tr><td>ACADDR[33]</td><td>0b0</td><td>0b0</td><td>VA[33]</td></tr><tr><td>ACADDR[32]</td><td>0b0</td><td>0b0</td><td>VA[32]</td></tr><tr><td>ACADDR[31]</td><td>0b0</td><td>0b0</td><td>VA[31]</td></tr><tr><td>ACADDR[30]</td><td>0b0</td><td>0b0</td><td>VA[30]</td></tr><tr><td>ACADDR[29]</td><td>0b0</td><td>0b0</td><td>VA[29]</td></tr><tr><td>ACADDR[28]</td><td>0b0</td><td>0b0</td><td>VA[28]</td></tr><tr><td>ACADDR[27]</td><td>0b0</td><td>0b0</td><td>VA[27]</td></tr><tr><td>ACADDR[26]</td><td>0b0</td><td>0b0</td><td>VA[26]</td></tr><tr><td>ACADDR[25]</td><td>0b0</td><td>0b0</td><td>VA[25]</td></tr><tr><td>ACADDR[24]</td><td>0b0</td><td>0b0</td><td>VA[24]</td></tr><tr><td>ACADDR[23]</td><td>0b0</td><td>0b0</td><td>VA[23]</td></tr><tr><td>ACADDR[22]</td><td>0b0</td><td>0b0</td><td>VA[22]</td></tr><tr><td>ACADDR[21]</td><td>0b0</td><td>0b0</td><td>VA[21]</td></tr></table>

Continued on next page

Table A15.21 – Continued from previous page
<table><tr><td>Signal</td><td>BPI all or Sync</td><td>BPI by VA 1st part</td><td>BPI by VA 2nd part</td></tr><tr><td>ACADDR[20]</td><td>0b0</td><td>0b0</td><td>VA[20]</td></tr><tr><td>ACADDR[19]</td><td>0b0</td><td>0b0</td><td>VA[19]</td></tr><tr><td>ACADDR[18]</td><td>0b0</td><td>0b0</td><td>VA[18]</td></tr><tr><td>ACADDR[17]</td><td>0b0</td><td>0b0</td><td>VA[17]</td></tr><tr><td>ACADDR[16]</td><td>0b0</td><td>0b0</td><td>VA[16]</td></tr><tr><td>ACADDR[15]</td><td>Completion</td><td>0b0 (Completion)</td><td>VA[15]</td></tr><tr><td>ACADDR[14]</td><td>DVMType[2]</td><td>0b0 (DVMType[2])</td><td>VA[14]</td></tr><tr><td>ACADDR[13]</td><td>DVMType[1]</td><td>0b0 (DVMType[1])</td><td>VA[13]</td></tr><tr><td>ACADDR[12]</td><td>DVMType[0]</td><td>0b1 (DVMType[0])</td><td>VA[12]</td></tr><tr><td>ACADDR[11]</td><td>0b0 (Exception[1])</td><td>0b0 (Exception[1])</td><td>VA[11]</td></tr><tr><td>ACADDR[10]</td><td>0b0 (Exception[0])</td><td>0b0 (Exception[0])</td><td>VA[10]</td></tr><tr><td>ACADDR[9]</td><td>0b0 (Security[1])</td><td>0b0 (Security[1])</td><td>VA[9]</td></tr><tr><td>ACADDR[8]</td><td>0b0 (Security[0])</td><td>0b0 (Security[0])</td><td>VA[8]</td></tr><tr><td>ACADDR[7]</td><td>Ob0 (Range)</td><td>Ob0 (Range)</td><td>VA[7]</td></tr><tr><td>ACADDR[6]</td><td>0b0 (VMIDV)</td><td>0b0 (VMIDV)</td><td>VA[6]</td></tr><tr><td>ACADDR[5]</td><td>0b0 (ASIDV)</td><td>0b0 (ASIDV)</td><td>VA[5]</td></tr><tr><td>ACADDR[4]</td><td>0b0 (Leaf)</td><td>0b0 (Leaf)</td><td>VA[4]</td></tr><tr><td>ACADDR[3]</td><td>0b0 (Stage[1])</td><td>0b0 (Stage[1])</td><td>VA[40]</td></tr><tr><td>ACADDR[2]</td><td>0b0 (Stage[0])</td><td>0b0 (Stage[0])</td><td>0b0</td></tr><tr><td>ACADDR[1]</td><td>0b0</td><td>0b0</td><td>0b0</td></tr><tr><td>ACADDR[0]</td><td>0b0 (Addr)</td><td>0b1 (Addr)</td><td>0b0</td></tr><tr><td>ACVMIDEXT[3]</td><td>0b0</td><td>0b0</td><td>0b0</td></tr><tr><td>ACVMIDEXT[2]</td><td>0b0</td><td>0b0</td><td>0b0</td></tr><tr><td>ACVMIDEXT[1]</td><td>0b0</td><td>0b0</td><td>0b0</td></tr><tr><td>ACVMIDEXT[0]</td><td>0b0</td><td>0b0</td><td>0b0</td></tr></table>

The mappings for Instruction Cache Invalidation messages are shown in Table A15.22.

Table A15.22: Field mappings for VICI and PICI messages
<table><tr><td>Signal</td><td>VICI all</td><td>VICI by VA 1st part</td><td>VICI by VA 2nd part</td><td>PICI 1st part</td><td>PICI 2nd part</td></tr><tr><td>ACADDR[51]</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b0</td><td>PA[51]</td></tr><tr><td>ACADDR[50]</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b0</td><td>PA[50]</td></tr><tr><td>ACADDR[49]</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b0</td><td>PA[49]</td></tr><tr><td>ACADDR[48]</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b0</td><td>PA[48]</td></tr><tr><td>ACADDR[47]</td><td>0b0</td><td>VA[56]</td><td>VA[52]</td><td>0b0</td><td>PA[47]</td></tr><tr><td>ACADDR[46]</td><td>0b0</td><td>VA[55]</td><td>VA[51]</td><td>0b0</td><td>PA[46]</td></tr><tr><td>ACADDR[45]</td><td>0b0</td><td>VA[54]</td><td>VA[50]</td><td>0b0</td><td>PA[45]</td></tr><tr><td>ACADDR[44]</td><td>0b0</td><td>VA[53]</td><td>VA[49]</td><td>0b0</td><td>PA[44]</td></tr><tr><td>ACADDR[43]</td><td>VMID[15]</td><td>VA[48]</td><td>VA[44]</td><td>0b0</td><td>PA[43]</td></tr><tr><td>ACADDR[42]</td><td>VMID[14]</td><td>VA[47]</td><td>VA[43]</td><td>0b0</td><td>PA[42]</td></tr><tr><td>ACADDR[41]</td><td>VMID[13]</td><td>VA[46]</td><td>VA[42]</td><td>0b0</td><td>PA[41]</td></tr><tr><td>ACADDR[40]</td><td>VMID[12]</td><td>VA[45]</td><td>VA[41]</td><td>0b0</td><td>PA[40]</td></tr><tr><td>ACADDR[39]</td><td>ASID[15]</td><td>ASID[15]</td><td>VA[39]</td><td>0b0</td><td>PA[39]</td></tr><tr><td>ACADDR[38]</td><td>ASID[14]</td><td>ASID[14]</td><td>VA[38]</td><td>0b0</td><td>PA[38]</td></tr><tr><td>ACADDR[37]</td><td>ASID[13]</td><td>ASID[13]</td><td>VA[37]</td><td>0b0</td><td>PA[37]</td></tr><tr><td>ACADDR[36]</td><td>ASID[12]</td><td>ASID[12]</td><td>VA[36]</td><td>0b0</td><td>PA[36]</td></tr><tr><td>ACADDR[35]</td><td>ASID[11]</td><td>ASID[11]</td><td>VA[35]</td><td>0b0</td><td>PA[35]</td></tr><tr><td>ACADDR[34]</td><td>ASID[10]</td><td>ASID[10]</td><td>VA[34]</td><td>0b0</td><td>PA[34]</td></tr><tr><td>ACADDR[33]</td><td>ASID[9]</td><td>ASID[9]</td><td>VA[33]</td><td>0b0</td><td>PA[33]</td></tr><tr><td>ACADDR[32]</td><td>ASID[8]</td><td>ASID[8]</td><td>VA[32]</td><td>0b0</td><td>PA[32]</td></tr><tr><td>ACADDR[31]</td><td>VMID[7]</td><td>VMID[7]</td><td>VA[31]</td><td>VI[27]</td><td>PA[31]</td></tr><tr><td>ACADDR[30]</td><td>VMID[6]</td><td>VMID[6]</td><td>VA[30]</td><td>VI[26]</td><td>PA[30]</td></tr><tr><td>ACADDR[29]</td><td>VMID[5]</td><td>VMID[5]</td><td>VA[29]</td><td>VI[25]</td><td>PA[29]</td></tr><tr><td>ACADDR[28]</td><td>VMID[4]</td><td>VMID[4]</td><td>VA[28]</td><td>VI[24]</td><td>PA[28]</td></tr><tr><td>ACADDR[27]</td><td>VMID[3]</td><td>VMID[3]</td><td>VA[27]</td><td>VI[23]</td><td>PA[27]</td></tr><tr><td>ACADDR[26]</td><td>VMID[2]</td><td>VMID[2]</td><td>VA[26]</td><td>VI[22]</td><td>PA[26]</td></tr><tr><td>ACADDR[25]</td><td>VMID[1]</td><td>VMID[1]</td><td>VA[25]</td><td>VI[21]</td><td>PA[25]</td></tr><tr><td>ACADDR[24]</td><td>VMID[0]</td><td>VMID[0]</td><td>VA[24]</td><td>VI[20]</td><td>PA[24]</td></tr><tr><td>ACADDR[23]</td><td>ASID[7]</td><td>ASID[7]</td><td>VA[23]</td><td>VI[19]</td><td>PA[23]</td></tr><tr><td>ACADDR[22]</td><td>ASID[6]</td><td>ASID[6]</td><td>VA[22]</td><td>VI[18]</td><td>PA[22]</td></tr></table>

Continued on next page

Chapter A15. Distributed Virtual Memory messages A15.4. Transporting DVM messages  
Table A15.22 – Continued from previous page
<table><tr><td>Signal</td><td>VICI all</td><td>VICI by VA 1st part</td><td>VICI by VA 2nd part</td><td>PICI 1st part</td><td>PICI 2nd part</td></tr><tr><td>ACADDR[21]</td><td>ASID[5]</td><td>ASID[5]</td><td>VA[21]</td><td>VI[17]</td><td>PA[21]</td></tr><tr><td>ACADDR[20]</td><td>ASID[4]</td><td>ASID[4]</td><td>VA[20]</td><td>VI[16]</td><td>PA[20]</td></tr><tr><td>ACADDR[19]</td><td>ASID[3]</td><td>ASID[3]</td><td>VA[19]</td><td>VI[15]</td><td>PA[19]</td></tr><tr><td>ACADDR[18]</td><td>ASID[2]</td><td>ASID[2]</td><td>VA[18]</td><td>VI[14]</td><td>PA[18]</td></tr><tr><td>ACADDR[17]</td><td>ASID[1]</td><td>ASID[1]</td><td>VA[17]</td><td>VI[13]</td><td>PA[17]</td></tr><tr><td>ACADDR[16]</td><td>ASID[0]</td><td>ASID[0]</td><td>VA[16]</td><td>VI[12]</td><td>PA[16]</td></tr><tr><td>ACADDR[15]</td><td>0b0 (Completion)</td><td>0b0 (Completion)</td><td>VA[15]</td><td>0b0 (Completion)</td><td>PA[15]</td></tr><tr><td>ACADDR[14]</td><td>0b0 (DVMType[2])</td><td>0b0 (DVMType[2])</td><td>VA[14]</td><td>0b0 (DVMType[2])</td><td>PA[14]</td></tr><tr><td>ACADDR[13]</td><td>0b1 (DVMType[1])</td><td>0b1 (DVMType[1])</td><td>VA[13]</td><td>0b1 (DVMType[1])</td><td>PA[13]</td></tr><tr><td>ACADDR[12]</td><td>0b1 (DVMType[0])</td><td>0b1 (DVMType[0])</td><td>VA[12]</td><td>0b0 (DVMType[0])</td><td>PA[12]</td></tr><tr><td>ACADDR[11]</td><td>Exception[1]</td><td>Exception[1]</td><td>VA[11]</td><td>0b0 (Exception[1])</td><td>PA[11]</td></tr><tr><td>ACADDR[10]</td><td>Exception[0]</td><td>Exception[0]</td><td>VA[10]</td><td>0b0 (Exception[0])</td><td>PA[10]</td></tr><tr><td>ACADDR[9]</td><td>Security[1]</td><td>Security[1]</td><td>VA[9]</td><td>Security[1]</td><td>PA[9]</td></tr><tr><td>ACADDR[8]</td><td>Security[0]</td><td>Security[0]</td><td>VA[8]</td><td>Security[0]</td><td>PA[8]</td></tr><tr><td>ACADDR[7]</td><td>Ob0 (Range)</td><td>Ob0 (Range)</td><td>VA[7]</td><td>Ob0 (Range)</td><td>PA[7]</td></tr><tr><td>ACADDR[6]</td><td>VMIDV</td><td>VMIDV</td><td>VA[6]</td><td>VIV[1]</td><td>PA[6]</td></tr><tr><td>ACADDR[5]</td><td>ASIDV</td><td>ASIDV</td><td>VA[5]</td><td>VIV[0]</td><td>PA[5]</td></tr><tr><td>ACADDR[4]</td><td>0b0 (Leaf)</td><td>Ob0 (Leaf)</td><td>VA[4]</td><td>0b0</td><td>PA[4]</td></tr><tr><td>ACADDR[3]</td><td>0b0 (Stage[1])</td><td>0b0 (Stage[1])</td><td>VA[40]</td><td>0b0</td><td>0b0</td></tr><tr><td>ACADDR[2]</td><td>0b0 (Stage[0])</td><td>0b0 (Stage[0])</td><td>0b0</td><td>0b0</td><td>0b0</td></tr><tr><td>ACADDR[1]</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b0</td><td>0b0</td></tr><tr><td>ACADDR[0]</td><td>0b0 (Addr)</td><td>0b1 (Addr)</td><td>0b0</td><td>Addr</td><td>0b0</td></tr><tr><td>ACVMIDEXT[3]</td><td>VMID[11]</td><td>VMID[11]</td><td>VMID[15]</td><td>0b0</td><td>0b0</td></tr><tr><td>ACVMIDEXT[2]</td><td>VMID[10]</td><td>VMID[10]</td><td>VMID[14]</td><td>0b0</td><td>0b0</td></tr><tr><td>ACVMIDEXT[1]</td><td>VMID[9]</td><td>VMID[9]</td><td>VMID[13]</td><td>0b0</td><td>0b0</td></tr><tr><td>ACVMIDEXT[0]</td><td>VMID[8]</td><td>VMID[8]</td><td>VMID[12]</td><td>0b0</td><td>0b0</td></tr></table>

## A15.5 DVM Sync and Complete

A DVM Sync message is used when the requester needs to know when all previous invalidations are complete.

A DVM Complete request is sent when a component has received a DVM Sync message and all preceding invalidation operations are complete. The following rules apply in determining when an operation is complete:

## TLB Invalidate

Complete when a Manager can no longer use an invalidated translation and all previous transactions that could have used an invalidated translation are complete

## Branch Predictor Invalidate

Complete when cached copies of predicted instruction fetches have been invalidated and can no longer be accessed by the associated Manager. The invalidated cached copies might be from any virtual address or from a specified virtual address.

## Instruction Cache Invalidate

Complete when cached instructions have been invalidated and can no longer be accessed by the associated Manager.

The synchronization flow between an interconnect and one receiving Manager is shown in Figure A15.3.

## The process is:

1. The Manager acknowledges receipt of the DVM Sync message using the snoop response (CR) channel. This response must not be dependent on the forward progress of any transactions on the AR or AW channels.

2. The Manager must issue a DVM Complete request on the AR channel when it has completed all the necessary actions. This must be after the handshake of the associated DVM Sync on the snoop request channel of the same Manager. The Manager must send a DVM Complete in a timely manner, even if it continues to receive more DVM invalidation operations and more DVM Sync messages.

3. The interconnect component responds to the DVM Complete request using the read data (R) channel of the component that issued the DVM Complete. Read data is not valid in this response.

![](images/812f7f2c363fe19bbf9331cfcd906c67a0b270fe32227e76a937043638d8696a.jpg)  
Figure A15.3: DVM Synchronization flow

Every DVM Sync message must have one corresponding DVM Complete request.

A DVM Complete request can only be sent if there is a corresponding DVM Sync message.

A DVM Complete request is signaled on the AR channel, Table A15.23 shows the constraints on other AR channel signals if they are present.

Table A15.23: DVM Complete request constraints
<table><tr><td>Signal</td><td>Constraint</td></tr><tr><td>ARSNOOP</td><td>Must be 0b1110.</td></tr><tr><td>ARADDR</td><td>Must be zero.</td></tr><tr><td>ARID</td><td>Must be different from that of any outstanding, non-DVM Complete transaction on the read channels.</td></tr><tr><td>ARBURST</td><td>Must be INCR (0b01).</td></tr><tr><td>ARLEN</td><td>Must be 1 transfer (0x00).</td></tr><tr><td>ARSIZE</td><td>Must be equal to the data channel width or Max_Transaction_Bytes if that is smaller than the data width.</td></tr><tr><td>ARDOMAIN</td><td>Must be Shareable (0b01 or 0b10).</td></tr><tr><td>ARCACHE</td><td>Must be Modifiable, Non-cacheable (0b0 01 0).</td></tr><tr><td>ARCHUNKEN</td><td>Must be 0b0.</td></tr><tr><td>ARMMUVALID</td><td>Must be 0b0. If not present, ARMMUVALID is assumed to be 0b0 for a DVM Complete request.</td></tr><tr><td>ARMMUATST</td><td>Must be 0b0.</td></tr><tr><td>ARMMUFLOW</td><td>Must be 0b00.</td></tr><tr><td>ARTAGOP</td><td>Must be 0b00.</td></tr><tr><td>ARLOCK</td><td>Must be 0b0.</td></tr></table>

When using credited transport, a DVM Complete message can use any value for ARRP, but all DVM Complete messages on an interface must use the same RP.

## A15.6 Coherency Connection signaling

DVM message requests are transferred from a Subordinate to a Manager interface, which is the opposite direction to other requests. A Manager which is idle might be powered down and unable to accept any DVM requests. Coherency Connection signaling can be used to enable a Manager to control whether it receives DVM message requests.

The Coherency\_Connection\_Signals property is used to indicate whether a component supports the Coherency Connection signals.

Table A15.24: Coherency\_Connection\_Signals property
<table><tr><td>Coherency_Connection_Signals Default Description</td><td></td><td></td></tr><tr><td>True</td><td></td><td>Coherency Connection signaling is supported.</td></tr><tr><td>False</td><td>Y</td><td>Coherency Connection signaling is not supported.</td></tr></table>

When Coherency\_Connection\_Signals is True, the following signals are included on an interface.

Table A15.25: Coherency Connection signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>SYSCOREQ</td><td>1</td><td></td><td>Output from a Manager, asserted HIGH to request that it receives DVM messages on the AC channel.</td></tr><tr><td>SYSCOACK</td><td>1</td><td></td><td>Output from a Subordinate, asserted HIGH to acknowledge that the attached Manager might receive DVM messages on the AC channel.</td></tr></table>

Coherency Connection signals do not have default values, so connected interfaces must both support or not support Coherency Connection signaling.

The Coherency Connection signals use a four-phase scheme which can safely cross clock domains.

Disconnecting from DVM messages is typically used before entering a low-power state in which DVM requests cannot be processed.

## A15.6.1 Coherency Connection Handshake

SYSCOREQ and SYSCOACK must be deasserted when ARESETn is asserted. When not in reset, the following requests are permitted:

• A Manager requests to receive DVM messages by asserting SYSCOREQ HIGH. The interconnect indicates that DVM messages are enabled by asserting SYSCOACK HIGH.

• The Manager requests to stop receiving DVM messages by deasserting SYSCOREQ LOW. The interconnect indicates that DVM messages is disabled by deasserting SYSCOACK LOW.

The handshake timing is shown in Figure A15.4.

Chapter A15. Distributed Virtual Memory messages A15.6. Coherency Connection signaling  
![](images/a3ae74a0f6f170a42af186ac1d2e12b352e78f7051445f76b8b0c1d8be855a57.jpg)  
Figure A15.4: Coherency Connection handshake timing

The connection signaling obeys the four-phase handshake rules:

• A Manager can only change SYSCOREQ when SYSCOACK is at the same level.

• A Subordinate can only change SYSCOACK when SYSCOREQ is at the opposite level.

The rules for Managers and Subordinate components in each state are shown in Table A15.26.

Table A15.26: Coherency Connection signaling states
<table><tr><td>State</td><td>SYSCOREQ</td><td>SYSCOACK</td><td>Rules</td></tr><tr><td>Disabled</td><td>0</td><td>0</td><td>Manager: • Must not fetch and use DVM-managed translation table data to perform translations. • Asserts SYSCOREQ if it needs to perform DVM-managed translations. Subordinate:</td></tr><tr><td>Connect</td><td>1</td><td>0</td><td>to complete immediately. Manager: • Must not fetch and use DVM-managed translation table data to perform translations. • Must be able to receive and respond to DVM message requests. • Waiting for SYSCOACK to be asserted before using DVM-managed translations.</td></tr><tr><td>Enabled</td><td>1</td><td>1</td><td>Manager: • Can fetch and use DVM-managed translation table data. • Must be able to receive and respond to DVM message requests. • Deasserts SYSCOREQ if it has finished using DVM-managed translation table data and wants to enter a</td></tr></table>

Continued on next page

Chapter A15. Distributed Virtual Memory messages A15.6. Coherency Connection signaling  
Table A15.26 – Continued from previous page
<table><tr><td>State</td><td></td><td>SYSCOREQ SYSCOACK Rules</td><td></td></tr><tr><td>Disconnect</td><td>0</td><td>1</td><td>Manager: • Must not fetch or use any DVM-managed translation table data.</td></tr><tr><td rowspan="4"></td><td></td><td></td><td>• Must be able to receive and respond to DVM message requests.</td></tr><tr><td></td><td></td><td>• Waiting for SYSCOACK to be deasserted before disabling DVM-managed logic.</td></tr><tr><td></td><td></td><td>Subordinate: • Must wait for all outstanding DVM messages to receive a</td></tr><tr><td></td><td></td><td>response before deasserting SYSCOACK. • Must stop issuing DVM messages in a timely manner. • Must issue the second part of a 2-part DVM message if the first part has already been issued.</td></tr></table>

Note that a Subordinate is not permitted to send DVM messages in the Connect state, but a Manager must be able to receive DVM messages in the Connect state. This is because there might be a race between the assertion of SYSCOACK and ACVALID.

If an interconnect has sent a DVM Sync message that requires a DVM Complete message on the AR channel, then the interconnect is permitted to deassert SYSCOACK before the DVM Complete request is received. The Manager is required to send the DVM Complete request on the AR channel, even when DVM messages are disabled.

Transitions on the Coherency Connection signals might rely on AWAKEUP being asserted, see A14.1.2 AWAKEUP and Coherency Connection signaling for details.

## A15.7 Snoop channels credit control

When using credited transport, the snoop channels can include control signals to determine when channel receivers can give credits. This can be used to clock or power gate snoop channels when they are idle.

The following rules apply:

• Credit control is independent of the other channels on the interface. For example, the DVM channels can be in RUN when other channels are in STOP.

• All of the rules in A14.2 Interface gating with credited transport apply to the DVM credit control signals, but the Manager and Subordinate terms are swapped.

• A DVM transaction is considered to be complete when the response is received on CR. For a DVM Sync, the DVM channels can be stopped once the CR response is received. The Manager must start the main channels to send a DVM Complete request on the AR channel.

• Credit control is independent of the coherency connection state. For example, DVM messages might be enabled by setting SYSCOREQ and SYSCOACK HIGH, but the AC and CR channels remain in STOP until a DVM message needs to be sent.

Table A15.27 shows the signals that are included when DVM\_Message\_Support is Receiver and Credit\_Control is Implicit\_Return\_Uni.

Table A15.27: Credit control signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>ACTIVATEREQD</td><td>1</td><td>0b1</td><td>Activation / deactivation request from a Subordinate for the snoop channels.</td></tr><tr><td>ACTIVATEACKD</td><td>1</td><td>0b1</td><td>Activation / deactivation acknowledge from a Manager for the snoop channels.</td></tr><tr><td>ASKSTOPD</td><td>1</td><td>0b0</td><td>Asserted HIGH to indicate that the Manager wants the Subordinate to stop the snoop channels.</td></tr></table>

# Chapter A16 Interface and data protection

This chapter specifies schemes for the protection of data and interfaces using poison and parity signaling. It contains the following sections:

• A16.1 Data protection using Poison

• A16.2 Parity protectionfor data and interface signals

## A16.1 Data protection using Poison

Poison signaling is used to indicate that a set of data bytes has been previously corrupted. Passing the Poison signaling alongside the data permits any future user of the data to be notified that the data might be corrupt. Poison signaling is supported at the granularity of 1 bit for every 64 bits of data.

Table A16.1: Poison signals
<table><tr><td>Name</td><td>Width</td><td>Default</td><td>Description</td></tr><tr><td>WPOISON,</td><td>ceil(DATA_WIDTH / 64)</td><td></td><td>Asserted high to indicate that the data in this transfer</td></tr><tr><td>RPOISON</td><td></td><td></td><td>is corrupted. There is one bit per 64-bits of data.</td></tr><tr><td></td><td></td><td></td><td></td></tr></table>

The presence of Poison signals is configured using the Poison property.

Table A16.2: Poison property
<table><tr><td>Poison</td><td>Default 1</td><td>Description</td></tr><tr><td>True</td><td></td><td>Poison signaling is supported.</td></tr><tr><td>False</td><td>Y</td><td>Poison signaling is not supported.</td></tr></table>

The validity of the Poison signaling is identical to the validity of the associated data.

Poison signaling is independent of error response signaling:

• It is permitted to signal an error with no Poison violation.

• It is permitted to signal a Poison violation without signaling an error response.

A 64-bit granule is defined as an 8-byte address range that is aligned to an 8-byte boundary.

Where the transaction size, as indicated by AxSIZE, is less than 64-bits then it is permitted for the Poison bit to be different on each data transfer. In this situation the receiving component must examine all data transfers to determine if the 64-bit granule is poisoned.

Poison bits can be set for data lanes that are invalid for a transfer. For example, a 64-bit transfer on a 128-bit channel can have both Poison bits set.

For implications of Poison with MTE Tags, see A12.2.10 MTE and Poison.

## A16.2 Parity protection for data and interface signals

For safety-critical applications it is necessary to detect and possibly correct, transient and functional errors on individual wires within an SoC.

An error in a system component can propagate and cause multiple errors within connected components. Error detection and correction (EDC) is required to operate end-to-end, covering all logic and wires from source to destination.

One way to implement end-to-end protection, is to employ customized EDC schemes in components and implement a simple error detection scheme between components. Between these components there is no logic and single bit errors do not propagate to multi-bit errors. This section describes a parity scheme for detecting single-bit errors on the AMBA interface between components. Multi-bit errors can be detected if they occur in different parity signal groups. Figure A16.1 shows locations where parity can be used in AMBA.

![](images/6bbbe6f7ff9aaf747450812d820d45f677fc61285fc89fc2695ff6be4f80a30d.jpg)  
Figure A16.1: Parity use in AMBA

## A16.2.1 Configuration of parity protection

The protection scheme employed on an interface is defined by the property Check\_Type.

Table A16.3: Check\_Type property
<table><tr><td>Check_Type</td><td>Default Description</td><td></td></tr><tr><td>Odd_Parity_Byte_All</td><td></td><td>Odd parity checking included for all signals. Each bit of the parity signal generally covers up to 8 bits. However, a parity bit can cover more than 8 bits if the configuration requires it.</td></tr><tr><td>Odd_Parity_Byte_Data</td><td></td><td>Odd parity checking included for data signals with names that end in DATA. Each bit of the parity signal covers exactly 8 bits.</td></tr><tr><td>False</td><td>Y</td><td>No checking signals on the interface.</td></tr></table>

## A16.2.2 Error detection behavior

This specification is not prescriptive regarding component or system behavior when a parity error is detected. Depending on the system and affected signals, a flipped bit can have a wide range of effects. It might be harmless,

cause performance issues, data corruption, security violations, or deadlock. The transaction response is independent of parity error detection.

When an error is detected, the receiver can do any of the following:

• Terminate or propagate the transaction. Termination might or might not be protocol compliant.

• Correct the parity check signal or propagate the signal in error.

• Update its memory or leave untouched. The location might be marked as poisoned.

• Signal an error response through other means, for example with an interrupt.

## A16.2.3 Parity check signals

The parity check signals are listed in Table A16.4. They have the following attributes and rules:

• Odd parity is used.

Odd parity means that check signals are added to groups of signals on the interface and driven such that there is always an odd number of asserted bits in that group.

• Parity signals covering data and payload are defined such that in most cases there are no more than 8 bits per group.

This limitation assumes that there is a maximum of 3 logic levels available in the timing budget for generating each parity bit.

• Parity signals covering critical control signals, which are likely to have a smaller timing budget available, are defined with a single odd parity bit. This single odd parity bit is the inversion of the original critical control signal.

• Check signals are synchronous to ACLK and must be driven correctly in every cycle that the signal in the Check enable column is HIGH, see Table A16.4.

• Control signals have ARESETn as the Check enable.

– If the check signal for a control signal is wider than 1 bit, check bit [n] corresponds to bit [n] in the control signal.

• Payload signals have xVALID as the Check enable.

– If the check signal for a payload signal is wider than 1 bit:

<sub>\*</sub> Where a check signal covers multiple signals, parity is calculated by concatenating the signals in the order they are listed in Table A16.4, with the first signal listed at the LSB.

<sub>\*</sub> Check bit [n] corresponds to bits [(8n+7):8n] in the payload, with the following exceptions:

· WTAGCHK[n] is the parity of {WTAGUPDATE[n],WTAG[4n+3:4n]}.

· RTAGCHK[n] is the parity of RTAG[4n+3:4n].

<sub>\*</sub> If the payload is not an integer number of bytes, the most significant bit of the check signal covers fewer than 8-bits in the most significant portion of the payload.

• Parity signals must be driven appropriately to all the bits in the associated payload, irrespective of whether those bits are actively used in the transfer. For example, all bits of WDATACHK must be driven correctly when WVALID is asserted, even if some byte lanes are not being used.

• If none of the signals covered by a check signal are present on an interface, then the check signal is omitted from the interface.

The following rules apply for CHK signals which cover multiple signals where one or more of the inputs or outputs are missing:

• If there is a missing signal output, the value is assumed to be the default for that signal. Signals with a non-zero default must be considered when calculating parity, for example BCOMP which has a default value of 0b1.

• If there is an output signal with no corresponding input, the missing input cannot be assumed to take a fixed value. Therefore, the CHK signal cannot be used reliably.

• It is recommended that input signals that are part of a CHK group are either all present or all not present.

Table A16.4: Parity check signals
<table><tr><td>Name</td><td>Signals covered</td><td>Width</td><td>Check enable</td></tr><tr><td>AWVALIDCHK</td><td>AWVALID</td><td>1</td><td>ARESETn</td></tr><tr><td>AWREADYCHK</td><td>AWREADY</td><td>1</td><td>ARESETn</td></tr><tr><td>AWPENDINGCHK</td><td>AWPENDING</td><td>1</td><td>ARESETn</td></tr><tr><td>AWCRDTCHK</td><td>AWCRDT</td><td>Num_RP_AWW</td><td>ARESETn</td></tr><tr><td>AWCRDTSHCHK</td><td>AWCRDTSH</td><td>1</td><td>ARESETn</td></tr><tr><td>AWRPCHK</td><td>AWRP</td><td>1</td><td>AWVALID</td></tr><tr><td>AWSHAREDCRDCHK</td><td>AWSHAREDCRD</td><td>1</td><td>AWVALID</td></tr><tr><td>AWIDCHK</td><td>AWID AWIDUNQ</td><td>ceil((ID_W_WIDTH + int(Unique_ID_Support))/8)</td><td>AWVALID</td></tr><tr><td>AWADDRCHK</td><td>AWADDR</td><td>ceil(ADDR_WIDTH/8)</td><td>AWVALID</td></tr><tr><td>AWLENCHK</td><td>AWLEN</td><td>1</td><td>AWVALID</td></tr><tr><td>AWCTLCHK0</td><td>AWSIZE AWBURST AWLOCK AWPROT</td><td>1</td><td>AWVALID</td></tr><tr><td>AWCTLCHK1</td><td>AWREGION AWCACHE AWQOS</td><td>1</td><td>AWVALID</td></tr><tr><td>AWCTLCHK2</td><td>AWDOMAIN AWSNOOP</td><td>1</td><td>AWVALID</td></tr><tr><td>AWCTLCHK3</td><td>AWATOP AWCMO</td><td>1</td><td>AWVALID</td></tr><tr><td>AWPASCHK</td><td>AWTAGOP AWPAS</td><td>1</td><td>AWVALID</td></tr><tr><td>AWINSTPRIVCHK</td><td>AWINST</td><td>1</td><td>AWVALID</td></tr><tr><td>AWUSERCHK</td><td>AWPRIV AWUSER</td><td>ceil(USER_REQ_WIDTH/8)</td><td>AWVALID</td></tr><tr><td>AWSTASHNIDCHK</td><td>AWSTASHNID AWSTASHNIDEN</td><td>1</td><td>AWVALID</td></tr><tr><td>AWSTASHLPIDCHK</td><td>AWSTASHLPID AWSTASHLPIDEN</td><td>1</td><td>AWVALID</td></tr></table>

Continued on next page

Chapter A16. Interface and data protection A16.2. Parity protection for data and interface signals  
Table A16.4 – Continued from previous page
<table><tr><td>Name</td><td>Signals covered</td><td>Width</td><td>Check enable</td></tr><tr><td>AWTRACECHK</td><td>AWTRACE</td><td>1</td><td>AWVALID</td></tr><tr><td>AWLOOPCHK</td><td>AWLOOP</td><td>ceil(LOOP_W_WIDTH/8)</td><td>AWVALID</td></tr><tr><td>AWMMUCHK</td><td>AWMMUATST AWMMUFLOW AWMMUSECSID AWMMUSSIDV</td><td>1</td><td>AWVALID</td></tr><tr><td>AWMMUSIDCHK</td><td>AWMMUVALID AWMMUSID</td><td>ceil(SID_WIDTH/8)</td><td>AWVALID</td></tr><tr><td>AWMMUSSIDCHK</td><td>AWMMUSSID</td><td>ceil(SSID_WIDTH/8)</td><td>AWVALID</td></tr><tr><td>AWMMUPASUNKNOWNCHK</td><td></td><td></td><td>AWVALID</td></tr><tr><td>AWMMUPMCHK</td><td>AWMMUPASUNKNOWN</td><td>1</td><td></td></tr><tr><td>AWPBHACHK</td><td>AWMMUPM</td><td>1</td><td>AWVALID</td></tr><tr><td>AWMECIDCHK</td><td>AWPBHA</td><td>1</td><td>AWVALID</td></tr><tr><td>AWNSAIDCHK</td><td>AWMECID</td><td>ceil(MECID_WIDTH/8)</td><td>AWVALID</td></tr><tr><td>AWMPAMCHK</td><td>AWNSAID</td><td>1</td><td>AWVALID</td></tr><tr><td>AWSUBSYSIDCHK</td><td>AWMPAM</td><td>1</td><td>AWVALID</td></tr><tr><td>AWACTCHK</td><td>AWSUBSYSID AWACTV</td><td>1 ceil((ACT_W_WIDTH+1)/8)</td><td>AWVALID AWVALID</td></tr><tr><td>WVALIDCHK</td><td>AWACT</td><td></td><td></td></tr><tr><td>WREADYCHK</td><td>WVALID</td><td>1</td><td>ARESETn</td></tr><tr><td>WPENDINGCHK</td><td>WREADY</td><td>1</td><td>ARESETn</td></tr><tr><td>WCRDTCHK</td><td>WPENDING</td><td>1</td><td>ARESETn</td></tr><tr><td>WCRDTSHCHK</td><td>WCRDT</td><td>Num_RP_AWW</td><td>ARESETn</td></tr><tr><td>WRPCHK</td><td>WCRDTSH</td><td>1</td><td>ARESETn</td></tr><tr><td>WSHAREDCRDCHK</td><td>WRP</td><td>1</td><td>WVALID</td></tr><tr><td>WDATACHK</td><td>WSHAREDCRD</td><td>1</td><td>WVALID</td></tr><tr><td>WSTRBCHK</td><td>WDATA</td><td>DATA_WIDTH/8</td><td>WVALID</td></tr><tr><td>WTAGCHK</td><td>WSTRB WTAG</td><td>ceil(DATA_WIDTH/64) ceil(DATA_WIDTH/128)</td><td>WVALID WVALID</td></tr><tr><td></td><td>WTAGUPDATE</td><td></td><td></td></tr><tr><td>WLASTCHK WUSERCHK</td><td>WLAST</td><td>1</td><td>WVALID</td></tr><tr><td>WPOISONCHK</td><td>WUSER</td><td>ceil(USER_DATA_WIDTH/8)</td><td>WVALID</td></tr><tr><td></td><td>WPOISON</td><td>ceil(DATA_WIDTH/512)</td><td>WVALID</td></tr><tr><td>WTRACECHK</td><td>WTRACE</td><td>1</td><td>WVALID</td></tr><tr><td>BVALIDCHK</td><td>BVALID</td><td>1</td><td>ARESETn</td></tr><tr><td>BREADYCHK</td><td>BREADY</td><td>1</td><td>ARESETn</td></tr></table>

Continued on next page

Chapter A16. Interface and data protection A16.2. Parity protection for data and interface signals  
Table A16.4 – Continued from previous page
<table><tr><td>Name</td><td>Signals covered</td><td>Width</td><td>Check enable</td></tr><tr><td>BPENDINGCHK</td><td>BPENDING</td><td>1</td><td>ARESETn</td></tr><tr><td>BCRDTCHK</td><td>BCRDT</td><td>1</td><td>ARESETn</td></tr><tr><td>BIDCHK</td><td>BID BIDUNQ</td><td>ceil((ID_W_WIDTH + int(Unique_ID_Support))/8)</td><td>BVALID</td></tr><tr><td>BRESPCHK</td><td>BRESP BCOMP BPERSIST BTAGMATCH BBUSY</td><td>1</td><td>BVALID</td></tr><tr><td>BUSERCHK</td><td>BUSER</td><td>ceil(USER_RESP_WIDTH/8)</td><td>BVALID</td></tr><tr><td>BTRACECHK</td><td>BTRACE</td><td>1</td><td>BVALID</td></tr><tr><td>BLOOPCHK</td><td>BLOOP</td><td>ceil(LOOP_W_WIDTH/8)</td><td>BVALID</td></tr><tr><td>ARVALIDCHK</td><td>ARVALID</td><td>1</td><td>ARESETn</td></tr><tr><td>ARREADYCHK</td><td>ARREADY</td><td>1</td><td>ARESETn</td></tr><tr><td>ARPENDINGCHK</td><td>ARPENDING</td><td>1</td><td>ARESETn</td></tr><tr><td>ARCRDTCHK</td><td>ARCRDT</td><td>Num_RP_AR</td><td>ARESETn</td></tr><tr><td>ARCRDTSHCHK</td><td>ARCRDTSH</td><td>1</td><td>ARESETn</td></tr><tr><td>ARRPCHK</td><td>ARRP</td><td>1</td><td>ARVALID</td></tr><tr><td>ARSHAREDCRDCHK</td><td>ARSHAREDCRD</td><td>1</td><td>ARVALID</td></tr><tr><td>ARIDCHK</td><td>ARID ARIDUNQ</td><td>ceil((ID_R_WIDTH + int(Unique_ID_Support))/8)</td><td>ARVALID</td></tr><tr><td>ARADDRCHK</td><td>ARADDR</td><td>ceil(ADDR_WIDTH/8)</td><td>ARVALID</td></tr><tr><td>ARLENCHK ARCTLCHKO</td><td>ARLEN</td><td>1 1</td><td>ARVALID</td></tr><tr><td>ARNSE</td><td>ARSIZE ARBURST ARLOCK ARPROT</td><td></td><td>ARVALID</td></tr><tr><td>ARCTLCHK1</td><td>ARREGION ARCACHE ARQOS</td><td>1</td><td>ARVALID</td></tr><tr><td>ARCTLCHK2</td><td>ARDOMAIN ARSNOOP</td><td>1</td><td>ARVALID</td></tr><tr><td>ARCTLCHK3</td><td>ARCHUNKEN ARTAGOP</td><td>1</td><td>ARVALID</td></tr><tr><td>ARPASCHK</td><td>ARPAS</td><td>1</td><td>ARVALID</td></tr><tr><td>ARINSTPRIVCHK</td><td>ARINST ARPRIV</td><td>1</td><td>ARVALID</td></tr></table>

Continued on next page

A16.2. Parity protection for data and interface signals  
Table A16.4 – Continued from previous page
<table><tr><td>Name</td><td>Signals covered</td><td>Width</td><td>Check enable</td></tr><tr><td>ARUSERCHK</td><td>ARUSER</td><td>ceil(USER_REQ_WIDTH/8)</td><td>ARVALID</td></tr><tr><td>ARTRACECHK</td><td>ARTRACE</td><td>1</td><td>ARVALID</td></tr><tr><td>ARLOOPCHK</td><td>ARLOOP</td><td>ceil(LOOP_R_WIDTH/8)</td><td>ARVALID</td></tr><tr><td>ARMMUCHK</td><td>ARMMUATST ARMMUFLOW ARMMUSECSID ARMMUSSIDV ARMMUVALID</td><td>1</td><td>ARVALID</td></tr><tr><td>ARMMUSIDCHK</td><td>ARMMUSID</td><td>ceil(SID_WIDTH/8)</td><td>ARVALID</td></tr><tr><td>ARMMUSSIDCHK</td><td>ARMMUSSID</td><td>ceil(SSID_WIDTH/8)</td><td>ARVALID</td></tr><tr><td>ARMMUPASUNKNOWNCHK</td><td>ARMMUPASUNKNOWN</td><td>1</td><td>ARVALID</td></tr><tr><td>ARMMUPMCHK</td><td>ARMMUPM</td><td>1</td><td>ARVALID</td></tr><tr><td>ARNSAIDCHK</td><td>ARNSAID</td><td>1</td><td>ARVALID</td></tr><tr><td>ARMPAMCHK</td><td>ARMPAM</td><td>1</td><td>ARVALID</td></tr><tr><td>ARPBHACHK</td><td>ARPBHA</td><td>1</td><td>ARVALID</td></tr><tr><td>ARMECIDCHK</td><td>ARMECID</td><td>ceil(MECID_WIDTH/8)</td><td>ARVALID</td></tr><tr><td>ARSUBSYSIDCHK</td><td>ARSUBSYSID</td><td>1</td><td>ARVALID</td></tr><tr><td>ARACTCHK</td><td>ARACTV ARACT</td><td>ceil((ACT_R_WIDTH+1)/8)</td><td>ARVALID</td></tr><tr><td>RVALIDCHK</td><td>RVALID</td><td>1</td><td>ARESETn</td></tr><tr><td>RREADYCHK</td><td>RREADY</td><td>1</td><td>ARESETn</td></tr><tr><td>RPENDINGCHK</td><td>RPENDING</td><td>1</td><td>ARESETn</td></tr><tr><td>RCRDTCHK</td><td>RCRDT</td><td>1</td><td>ARESETn</td></tr><tr><td>RIDCHK</td><td>RID RIDUNQ</td><td>ceil((ID_R_WIDTH + int(Unique_ID_Support))/8)</td><td>RVALID</td></tr><tr><td>RDATACHK</td><td>RDATA</td><td>DATA_WIDTH/8</td><td>RVALID</td></tr><tr><td>RTAGCHK</td><td>RTAG</td><td>ceil(DATA_WIDTH/128)</td><td>RVALID</td></tr><tr><td>RRESPCHK</td><td>RRESP RBUSY</td><td>1</td><td>RVALID</td></tr><tr><td>RLASTCHK</td><td>RLAST</td><td>1</td><td>RVALID</td></tr><tr><td>RCHUNKCHK</td><td>RCHUNKV RCHUNKNUM RCHUNKSTRB</td><td>1</td><td>RVALID</td></tr><tr><td>RUSERCHK</td><td>RUSER</td><td>ceil((USER_DATA_WIDTH + USER_RESP_WIDTH)/8)</td><td>RVALID</td></tr><tr><td>RPOISONCHK</td><td>RPOISON</td><td>ceil(DATA_WIDTH/512)</td><td>RVALID</td></tr></table>

Continued on next page

Table A16.4 – Continued from previous page
<table><tr><td>Name</td><td>Signals covered</td><td>Width</td><td>Check enable</td></tr><tr><td>RTRACECHK</td><td>RTRACE</td><td>1</td><td>RVALID</td></tr><tr><td>RLOOPCHK</td><td>RLOOP</td><td>ceil(LOOP_R_WIDTH/8)</td><td>RVALID</td></tr><tr><td>ACVALIDCHK</td><td>ACVALID</td><td>1</td><td>ARESETn</td></tr><tr><td>ACREADYCHK</td><td>ACREADY</td><td>1</td><td>ARESETn</td></tr><tr><td>ACPENDINGCHK</td><td>ACPENDING</td><td>1</td><td>ARESETn</td></tr><tr><td>ACCRDTCHK</td><td>ACCRDT</td><td>1</td><td>ARESETn</td></tr><tr><td>ACADDRCHK</td><td>ACADDR</td><td>ceil(ADDR_WIDTH/8)</td><td>ACVALID</td></tr><tr><td>ACVMIDEXTCHK</td><td>ACVMIDEXT</td><td>1</td><td>ACVALID</td></tr><tr><td>ACTRACECHK</td><td>ACTRACE</td><td>1</td><td>ACVALID</td></tr><tr><td>CRVALIDCHK</td><td>CRVALID</td><td>1</td><td>ARESETn</td></tr><tr><td>CRREADYCHK</td><td>CRREADY</td><td>1</td><td>ARESETn</td></tr><tr><td>CRPENDINGCHK</td><td>CRPENDING</td><td>1</td><td>ARESETn</td></tr><tr><td>CRCRDTCHK</td><td>CRCRDT</td><td>1</td><td>ARESETn</td></tr><tr><td>CRTRACECHK</td><td>CRTRACE</td><td>1</td><td>CRVALID</td></tr><tr><td>VAWQOSACCEPTCHK</td><td>VAWQOSACCEPT</td><td>1</td><td>ARESETn</td></tr><tr><td>VARQOSACCEPTCHK</td><td>VARQOSACCEPT</td><td>1</td><td>ARESETn</td></tr><tr><td>AWAKEUPCHK</td><td>AWAKEUP</td><td>1</td><td>ARESETn</td></tr><tr><td>ACWAKEUPCHK</td><td>ACWAKEUP</td><td>1</td><td>ARESETn</td></tr><tr><td>ACTIVATEREQCHK</td><td>ACTIVATEREQ</td><td>1</td><td>ARESETn</td></tr><tr><td>ACTIVATEACKCHK</td><td>ACTIVATEACK</td><td>1</td><td>ARESETn</td></tr><tr><td>ASKSTOPCHK</td><td>ASKSTOP</td><td>1</td><td>ARESETn</td></tr><tr><td>ACTIVATEREQDCHK</td><td>ACTIVATEREQD</td><td>1</td><td>ARESETn</td></tr><tr><td>ACTIVATEACKDCHK</td><td>ACTIVATEACKD</td><td>1</td><td>ARESETn</td></tr><tr><td>ASKSTOPDCHK</td><td>ASKSTOPD</td><td>1</td><td>ARESETn</td></tr><tr><td>SYSCOREQCHK</td><td>SYSCOREQ</td><td>1</td><td>None</td></tr><tr><td>SYSCOACKCHK</td><td>SYSCOACK</td><td>1</td><td>None</td></tr></table>

Part B Appendices

## Chapter B1 Signal list

This appendix lists all the signals described within this specification. Some channels and signals are optional, so are not included on every interface. Each signal name contains a hyperlink to the section in which the signal is defined.

Parity check signals are not included in this chapter but are listed in A16.2.3 Parity check signals.

Signals are grouped based on channel and category as described in the following sections:

• B1.1 Write channels

• B1.2 Read channels

• B1.3 Snoop channels

• B1.4 Interface level signals

## B1.1 Write channels

The write channels are used to transfer requests, data, and responses for write transactions and some other data-less transactions.

## B1.1.1 Write request channel

The write request channel carries all the required address and control information for transactions that use the write channels. Signals on this channel have the prefix AW.

Table B1.1: Write request channel signals
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Description</td></tr><tr><td>AWVALID</td><td>1</td><td>Manager</td><td>Valid indicator</td></tr><tr><td>AWREADY</td><td>1</td><td>Subordinate</td><td>Ready indicator</td></tr><tr><td>AWPENDING</td><td>1</td><td>Manager</td><td>Pending indicator</td></tr><tr><td>AWCRDT</td><td>Num_RP_AWW</td><td>Subordinate</td><td>Credit grant</td></tr><tr><td>AWCRDTSH</td><td>1</td><td>Subordinate</td><td>Shared credit grant</td></tr><tr><td>AWRP</td><td>clog2(Num_RP_AWW)</td><td>Manager</td><td>Resource Plane indicator</td></tr><tr><td>AWSHAREDCRD</td><td>1</td><td>Manager</td><td>Shared credit indicator</td></tr><tr><td>AWID</td><td>ID_W_WIDTH</td><td>Manager</td><td>Transaction identifier for a write request</td></tr><tr><td>AWADDR</td><td>ADDR_WIDTH</td><td>Manager</td><td>Transaction address</td></tr><tr><td>AWREGION</td><td>4</td><td>Manager</td><td>Region identifier</td></tr><tr><td>AWLEN</td><td>8</td><td>Manager</td><td>Transaction length</td></tr><tr><td>AWSIZE</td><td>3</td><td>Manager</td><td>Transaction size</td></tr><tr><td>AWBURST</td><td>2</td><td>Manager</td><td>Burst attribute</td></tr><tr><td>AWLOCK</td><td>1</td><td>Manager</td><td>Exclusive access indicator</td></tr><tr><td>AWCACHE</td><td>4</td><td>Manager</td><td>Memory attributes</td></tr><tr><td>AWPROT</td><td>3</td><td>Manager</td><td>Protection attributes</td></tr><tr><td>AWNSE</td><td>1</td><td>Manager</td><td>Non-secure extension bit for RME</td></tr><tr><td>AWPAS</td><td>PAS_WIDTH</td><td>Manager</td><td>Physical Address Space</td></tr><tr><td>AWINST</td><td>1</td><td>Manager</td><td>Data or instruction request indicator</td></tr><tr><td>AWPRIV</td><td>1</td><td>Manager</td><td>Privileged request indicator</td></tr><tr><td>AWQOS</td><td>4</td><td>Manager</td><td>QoS identifier</td></tr><tr><td>AWUSER</td><td>USER_REQ_WIDTH</td><td>Manager</td><td>User-defined extension to a request</td></tr><tr><td>AWDOMAIN</td><td>2</td><td>Manager</td><td>Shareability domain of a request</td></tr><tr><td>AWSNOOP</td><td>AWSNOOP WIDTH</td><td>Manager</td><td>Write request opcode</td></tr><tr><td>AWSTASHNID</td><td>11</td><td>Manager</td><td>Stash Node ID</td></tr><tr><td>AWSTASHNIDEN</td><td>1</td><td>Manager</td><td>Stash Node ID enable</td></tr></table>

Continued on next page

Table B1.1 – Continued from previous page
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Description</td></tr><tr><td>AWSTASHLPID</td><td>5</td><td>Manager</td><td>Stash Logical Processor ID</td></tr><tr><td>AWSTASHLPIDEN</td><td>1</td><td>Manager</td><td>Stash Logical Processor ID enable</td></tr><tr><td>AWTRACE</td><td>1</td><td>Manager</td><td>Trace signal</td></tr><tr><td>AWLOOP</td><td>LOOP_W_WIDTH</td><td>Manager</td><td>Loopback signals on the write channels</td></tr><tr><td>AWMMUVALID</td><td>1</td><td>Manager</td><td>MMU signal qualifier</td></tr><tr><td>AWMMUSECSID</td><td>SECSID_WIDTH</td><td>Manager</td><td>Secure Stream ID</td></tr><tr><td>AWMMUSID</td><td>SID_WIDTH</td><td>Manager</td><td>StreamID</td></tr><tr><td>AWMMUSSIDV</td><td>1</td><td>Manager</td><td>SubstreamID valid</td></tr><tr><td>AWMMUSSID</td><td>SSID_WIDTH</td><td>Manager</td><td>SubstreamID</td></tr><tr><td>AWMMUATST</td><td>1</td><td>Manager</td><td>Address translated indicator</td></tr><tr><td>AWMMUFLOW</td><td>2</td><td>Manager</td><td>SMMU flow type</td></tr><tr><td>AWMMUPASUNKNOWN</td><td>1</td><td>Manager</td><td>PAS unknown indicator</td></tr><tr><td>AWMMUPM</td><td>1</td><td>Manager</td><td>Protected Mode indicator</td></tr><tr><td>AWPBHA</td><td>4</td><td>Manager</td><td>Page-based Hardware Attributes</td></tr><tr><td>AWMECID</td><td>MECID_WIDTH</td><td>Manager</td><td>Memory Encryption Context identifier</td></tr><tr><td>AWNSAID</td><td>4</td><td>Manager</td><td>Non-secure Access ID</td></tr><tr><td>AWSUBSYSID</td><td>SUBSYSID_WIDTH</td><td>Manager</td><td>Subsystem ID</td></tr><tr><td>AWATOP</td><td>6</td><td>Manager</td><td>Atomic transaction opcode</td></tr><tr><td>AWMPAM</td><td>MPAM_WIDTH</td><td>Manager</td><td>MPAM information with a request</td></tr><tr><td>AWIDUNQ</td><td>1</td><td>Manager</td><td>Unique ID indicator</td></tr><tr><td>AWCMO</td><td>AWCMO_WIDTH</td><td>Manager</td><td>CMO type</td></tr><tr><td>AWTAGOP</td><td>2</td><td>Manager</td><td>Memory Tag operation for write requests</td></tr><tr><td>AWACT</td><td>ACT_W_WIDTH</td><td>Manager</td><td>ACT payload</td></tr><tr><td>AWACTV</td><td>1</td><td>Manager</td><td>ACT valid indicator</td></tr></table>

## B1.1.2 Write data channel

The write data channel carries write data and control information from a Manager to a Subordinate. Signals on this channel have the prefix W.

Table B1.2: Write data channel signals
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Description</td></tr><tr><td>WVALID</td><td>1</td><td>Manager</td><td>Valid indicator</td></tr><tr><td>WREADY</td><td>1</td><td>Subordinate</td><td>Ready indicator</td></tr><tr><td>WPENDING</td><td>1</td><td>Manager</td><td>Pending indicator</td></tr><tr><td>WCRDT</td><td>Num_RP_AWW</td><td>Subordinate</td><td>Credit grant</td></tr><tr><td>WCRDTSH</td><td>1</td><td>Subordinate</td><td>Shared credit grant</td></tr><tr><td>WRP</td><td>clog2(Num_RP_AWW)</td><td>Manager</td><td>Resource Plane indicator for the W channel</td></tr><tr><td>WSHAREDCRD</td><td>1</td><td>Manager</td><td>Shared credit indicator</td></tr><tr><td>WDATA</td><td>DATA_WIDTH</td><td>Manager</td><td>Write data</td></tr><tr><td>WSTRB</td><td>DATA_WIDTH / 8</td><td>Manager</td><td>Write data strobes</td></tr><tr><td>WTAG</td><td>ceil(DATA_WIDTH/128)*4</td><td>Manager</td><td>Memory Tag</td></tr><tr><td>WTAGUPDATE</td><td>ceil(DATA_WIDTH/128)</td><td>Manager</td><td>Memory Tag update</td></tr><tr><td>WLAST</td><td>1</td><td>Manager</td><td>Last write data</td></tr><tr><td>WUSER</td><td>USER_DATA_WIDTH</td><td>Manager</td><td>User-defined extension to write data</td></tr><tr><td>WPOISON</td><td>ceil(DATA_WIDTH / 64)</td><td>Manager</td><td>Poison indicator</td></tr><tr><td>WTRACE</td><td>1</td><td>Manager</td><td>Trace signal</td></tr></table>

## B1.1.3 Write response channel

The write response channel carries responses from Subordinate to Manager for transactions using the write data channels. Signals on this channel have the prefix B.

Table B1.3: Write response channel signals
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Description</td></tr><tr><td>BVALID</td><td>1</td><td>Subordinate</td><td>Valid indicator</td></tr><tr><td>BREADY</td><td>1</td><td>Manager</td><td>Ready indicator</td></tr><tr><td>BPENDING</td><td>1</td><td>Subordinate</td><td>Pending indicator</td></tr><tr><td>BCRDT</td><td>1</td><td>Manager</td><td>Credit grant</td></tr><tr><td>BID</td><td>ID_W_WIDTH</td><td>Subordinate</td><td>Transaction identifier for a write response</td></tr><tr><td>BIDUNQ</td><td>1</td><td>Subordinate</td><td>Unique ID indicator</td></tr><tr><td>BRESP</td><td>BRESP_WIDTH</td><td>Subordinate</td><td>Write response</td></tr><tr><td>BCOMP</td><td>1</td><td>Subordinate</td><td>Completion response indicator</td></tr><tr><td>BPERSIST</td><td>1</td><td>Subordinate</td><td>Persist response</td></tr><tr><td>BTAGMATCH</td><td>2</td><td>Subordinate</td><td>Memory Tag Match response</td></tr><tr><td>BUSER</td><td>USER_RESP_WIDTH</td><td>Subordinate</td><td>User-defined extension to a write response</td></tr><tr><td>BTRACE</td><td>1</td><td>Subordinate</td><td>Trace signal</td></tr><tr><td>BLOOP</td><td>LOOP_W_WIDTH</td><td>Subordinate</td><td>Loopback signal on the write response channel</td></tr><tr><td>BBUSY</td><td>2</td><td>Subordinate</td><td>Busy indicator</td></tr></table>

## B1.2 Read channels

The read channels are used to transfer requests, data, and responses for read transactions, cache maintenance operations, and DVM Complete messages.

## B1.2.1 Read request channel

The read request channel carries all the required address and control information for transactions that use the read channels. Signals on this channel have the prefix AR.

Table B1.4: Read request channel signals
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Description</td></tr><tr><td>ARVALID</td><td>1</td><td>Manager</td><td>Valid indicator</td></tr><tr><td>ARREADY</td><td>1</td><td>Subordinate</td><td>Ready indicator</td></tr><tr><td>ARPENDING</td><td>1</td><td>Manager</td><td>Pending indicator</td></tr><tr><td>ARCRDT</td><td>Num_RP_AR</td><td>Subordinate</td><td>Credit grant</td></tr><tr><td>ARCRDTSH</td><td>1</td><td>Subordinate</td><td>Shared credit grant</td></tr><tr><td>ARRP</td><td>clog2(Num_RP_AR)</td><td>Manager</td><td>Resource Plane indicator</td></tr><tr><td>ARSHAREDCRD</td><td>1</td><td>Manager</td><td>Shared credit indicator</td></tr><tr><td>ARID</td><td>ID_R_WIDTH</td><td>Manager</td><td>Transaction identifier for a read request</td></tr><tr><td>ARADDR</td><td>ADDR_WIDTH</td><td>Manager</td><td>Transaction address</td></tr><tr><td>ARREGION</td><td>4</td><td>Manager</td><td>Region identifier</td></tr><tr><td>ARLEN</td><td>8</td><td>Manager</td><td>Transaction length</td></tr><tr><td>ARSIZE</td><td>3</td><td>Manager</td><td>Transaction size</td></tr><tr><td>ARBURST</td><td>2</td><td>Manager</td><td>Burst attribute</td></tr><tr><td>ARLOCK</td><td>1</td><td>Manager</td><td>Exclusive access indicator</td></tr><tr><td>ARCACHE</td><td>4</td><td>Manager</td><td>Memory attributes</td></tr><tr><td>ARPROT</td><td>3</td><td>Manager</td><td>Protection attributes</td></tr><tr><td>ARNSE</td><td>1</td><td>Manager</td><td>Non-secure extension bit for RME</td></tr><tr><td>ARPAS</td><td>PAS_WIDTH</td><td>Manager</td><td>Physical Address Space</td></tr><tr><td>ARINST</td><td>1</td><td>Manager</td><td>Data or instruction request indicator</td></tr><tr><td>ARPRIV</td><td>1</td><td>Manager</td><td>Privileged request indicator</td></tr><tr><td>ARQOS</td><td>4</td><td>Manager</td><td>QoS identifier</td></tr><tr><td>ARUSER</td><td>USER_REQ_WIDTH</td><td>Manager</td><td>User-defined extension to a request</td></tr><tr><td>ARDOMAIN</td><td>2</td><td>Manager</td><td>Shareability domain of a request</td></tr><tr><td>ARSNOOP</td><td>ARSNOOP_WIDTH</td><td>Manager</td><td>Read request opcode</td></tr><tr><td>ARTRACE</td><td>1</td><td>Manager</td><td>Trace signal</td></tr><tr><td>ARLOOP</td><td>LOOP_R_WIDTH</td><td>Manager</td><td>Loopback signal on the read request channel</td></tr></table>

Continued on next page

Table B1.4 – Continued from previous page
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Description</td></tr><tr><td>ARMMUVALID</td><td>1</td><td>Manager</td><td>MMU signal qualifier</td></tr><tr><td>ARMMUSECSID</td><td>SECSID_WIDTH</td><td>Manager</td><td>Secure Stream ID</td></tr><tr><td>ARMMUSID</td><td>SID_WIDTH</td><td>Manager</td><td>StreamID</td></tr><tr><td>ARMMUSSIDV</td><td>1</td><td>Manager</td><td>SubstreamID valid</td></tr><tr><td>ARMMUSSID</td><td>SSID_WIDTH</td><td>Manager</td><td>SubstreamID</td></tr><tr><td>ARMMUATST</td><td>1</td><td>Manager</td><td>Address translated indicator</td></tr><tr><td>ARMMUFLOW</td><td>2</td><td>Manager</td><td>SMMU flow type</td></tr><tr><td>ARMMUPASUNKNOWN</td><td>1</td><td>Manager</td><td>PAS unknown indicator</td></tr><tr><td>ARMMUPM</td><td>1</td><td>Manager</td><td>Protected Mode indicator</td></tr><tr><td>ARPBHA</td><td>4</td><td>Manager</td><td>Page-based Hardware Attributes</td></tr><tr><td>ARMECID</td><td>MECID_WIDTH</td><td>Manager</td><td>Memory Encryption Context identifier</td></tr><tr><td>ARNSAID</td><td>4</td><td>Manager</td><td>Non-secure Access ID</td></tr><tr><td>ARSUBSYSID</td><td>SUBSYSID_WIDTH</td><td>Manager</td><td>Subsystem ID</td></tr><tr><td>ARMPAM</td><td>MPAM_WIDTH</td><td>Manager</td><td>MPAM information with a request</td></tr><tr><td>ARCHUNKEN</td><td>1</td><td>Manager</td><td>Read data chunking enable</td></tr><tr><td>ARIDUNQ</td><td>1</td><td>Manager</td><td>Unique ID indicator</td></tr><tr><td>ARTAGOP</td><td>2</td><td>Manager</td><td>Memory Tag operation for read requests</td></tr><tr><td>ARACT</td><td>ACT_R_WIDTH</td><td>Manager</td><td>ACT payload</td></tr><tr><td>ARACTV</td><td>1</td><td>Manager</td><td>ACT valid indicator</td></tr></table>

## B1.2.2 Read data channel

The read data channel carries read data and responses from a Subordinate to a Manager. Signals on this channel have the prefix R.

Table B1.5: Read data channel signals
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Description</td></tr><tr><td>RVALID</td><td>1</td><td>Subordinate</td><td>Valid indicator</td></tr><tr><td>RREADY</td><td>1</td><td>Manager</td><td>Ready indicator</td></tr><tr><td>RPENDING</td><td>1</td><td>Subordinate</td><td>Pending indicator</td></tr><tr><td>RCRDT</td><td>1</td><td>Manager</td><td>Credit grant</td></tr><tr><td>RID</td><td>ID_R_WIDTH</td><td>Subordinate</td><td>Transaction identifier for read data</td></tr><tr><td>RIDUNQ</td><td>1</td><td>Subordinate</td><td>Unique ID indicator</td></tr><tr><td>RDATA</td><td>DATA_WIDTH</td><td>Subordinate</td><td>Read data</td></tr><tr><td>RTAG</td><td>ceil(DATA WIDTH/128)*4</td><td>Subordinate</td><td>Memory Tag</td></tr><tr><td>RRESP</td><td>RRESP_WIDTH</td><td>Subordinate</td><td>Read response</td></tr><tr><td>RLAST</td><td>1</td><td>Subordinate</td><td>Last read data</td></tr><tr><td>RUSER</td><td>USER_DATA_WIDTH + USER_RESP_WIDTH</td><td>Subordinate</td><td>User-defined extension to read data and response</td></tr><tr><td>RPOISON</td><td>ceil(DATA_WIDTH / 64)</td><td>Subordinate</td><td>Poison indicator</td></tr><tr><td>RTRACE</td><td>1</td><td>Subordinate</td><td>Trace signal</td></tr><tr><td>RLOOP</td><td>LOOP_R_WIDTH</td><td>Subordinate</td><td>Loopback signal on the read data channel</td></tr><tr><td>RCHUNKV</td><td>1</td><td>Subordinate</td><td>Read data chunking valid</td></tr><tr><td>RCHUNKNUM</td><td>RCHUNKNUM WIDTH</td><td>Subordinate</td><td>Read data chunk number</td></tr><tr><td>RCHUNKSTRB</td><td>RCHUNKSTRB_WIDTH</td><td>Subordinate</td><td>Read data chunk strobe</td></tr><tr><td>RBUSY</td><td>2</td><td>Subordinate</td><td>Busy indicator</td></tr></table>

## B1.3 Snoop channels

In this specification, the snoop channels are only used to transport DVM messages.

## B1.3.1 Snoop request channel

The snoop request channel carries address and control information for DVM message requests. Signals on this channel have the prefix AC.

Table B1.6: Snoop request channel signals
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Description</td></tr><tr><td>ACVALID</td><td>1</td><td>Subordinate</td><td>Valid indicator</td></tr><tr><td>ACREADY</td><td>1</td><td>Manager</td><td>Ready indicator</td></tr><tr><td>ACPENDING</td><td>1</td><td>Subordinate</td><td>Pending indicator</td></tr><tr><td>ACCRDT</td><td>1</td><td>Manager</td><td>Credit grant</td></tr><tr><td>ACADDR</td><td>ADDR_WIDTH</td><td>Subordinate</td><td>DVM message payload</td></tr><tr><td>ACVMIDEXT</td><td>4</td><td>Subordinate</td><td>VMID extension for DVM messages</td></tr><tr><td>ACTRACE</td><td>1</td><td>Subordinate</td><td>Trace signal</td></tr></table>

## B1.3.2 Snoop response channel

The snoop response channel carries responses to DVM messages. Signals on this channel have the prefix CR.

Table B1.7: Snoop response channel signals
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Description</td></tr><tr><td>CRVALID</td><td>1</td><td>Manager</td><td>Valid indicator</td></tr><tr><td>CRREADY</td><td>1</td><td>Subordinate</td><td>Ready indicator</td></tr><tr><td>CRPENDING</td><td>1</td><td>Manager</td><td>Pending indicator</td></tr><tr><td>CRCRDT</td><td>1</td><td>Subordinate</td><td>Credit grant</td></tr><tr><td>CRTRACE</td><td>1</td><td>Manager</td><td>Trace signal</td></tr></table>

## B1.4 Interface level signals

Interface level signals are non-channel signals. There can be up to one set of each per interface.

## B1.4.1 Clock and reset signals

All signals on an interface are synchronous to a global clock and are reset using a global reset signal.

Table B1.8: Clock and reset signals
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Description</td></tr><tr><td>ACLK</td><td>1</td><td>External</td><td>Global clock signal</td></tr><tr><td>ARESETn</td><td>1</td><td>External</td><td>Global reset signal</td></tr></table>

## B1.4.2 Credit control signals

Credit control signals are used with a credited link layer, to determine when channel receivers can give credits and therefore when transmitters can send transfers.

Table B1.9: Credit control signals
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Description</td></tr><tr><td>ACTIVATEREQ</td><td>1</td><td>Manager</td><td>Activation request</td></tr><tr><td>ACTIVATEACK</td><td>1</td><td>Subordinate</td><td>Activation acknowledge</td></tr><tr><td>ASKSTOP</td><td>1</td><td>Subordinate</td><td>Stop request</td></tr><tr><td>ACTIVATEREQD</td><td>1</td><td>Subordinate</td><td>Activation request for snoop channels</td></tr><tr><td>ACTIVATEACKD</td><td>1</td><td>Manager</td><td>Activation acknowledge for snoop channels</td></tr><tr><td>ASKSTOPD</td><td>1</td><td>Manager</td><td>Stop request for snoop channels</td></tr></table>

## B1.4.3 Wakeup signals

The wake-up signals are used to indicate that there is activity associated with the interface.

Table B1.10: Wake-up signals
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Description</td></tr><tr><td>AWAKEUP</td><td>1</td><td>Manager</td><td>Wake-up signal associated with read and write channels</td></tr><tr><td>ACWAKEUP</td><td>1</td><td>Subordinate</td><td>Wake-up signal associated with snoop channels</td></tr></table>

## B1.4.4 QoS Accept signals

QoS Accept signals can be used by a Subordinate interface to indicate the minimum QoS value of requests that it accepts.

Table B1.11: QoS Accept signals
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Description</td></tr><tr><td>VAWQOSACCEPT</td><td>4</td><td>Subordinate</td><td>QoS acceptance level for write requests</td></tr><tr><td>VARQOSACCEPT</td><td>4</td><td>Subordinate</td><td>QoS acceptance level for read requests</td></tr></table>

## B1.4.5 Coherency Connection signals

The coherency connection signals are used by a Manager to control whether it receives DVM messages on the AC channel.

Table B1.12: Coherency connection signals
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Description</td></tr><tr><td>SYSCOREQ</td><td>1</td><td>Manager</td><td>Coherency connect request</td></tr><tr><td>SYSCOACK</td><td>1</td><td>Subordinate</td><td>Coherency connect acknowledge</td></tr></table>

## B1.4.6 Interface control signals

The interface control signals are static inputs to a Manager interface that can be used to configure interface behavior.

Table B1.13: Interface control signals
<table><tr><td>Name</td><td>Width</td><td>Source</td><td>Description</td></tr><tr><td>BROADCASTATOMIC</td><td>1</td><td>Tie-off</td><td>Control input for Atomic transactions</td></tr><tr><td>BROADCASTSHAREABLE</td><td>1</td><td>Tie-off</td><td>Control input for Shareable transactions</td></tr><tr><td>BROADCASTCACHEMAINT</td><td>1</td><td>Tie-off</td><td>Control input for cache maintenance operations</td></tr><tr><td>BROADCASTCMOPOPA</td><td>1</td><td>Tie-off</td><td>Control input for the CleanInvalidPoPA CMO</td></tr><tr><td>BROADCASTPERSIST</td><td>1</td><td>Tie-off</td><td>Control input for CleanSharedPersist and CleanSharedDeepPersist</td></tr><tr><td>BROADCASTSTORAGE</td><td>1</td><td>Tie-off</td><td>Control input for CleanInvalidStorage CMO</td></tr></table>

# Chapter B2 Interface classes

The specification part in this document describes a generic fully-featured protocol, with some features being mandatory and others optional, based on properties. Previous issues of this specification defined a number of interface classes for different use-cases. These can all now be described by constraining certain properties to limit the functionality and signaling on that interface.

This chapter describes the following interface classes:

• B2.1.1 AXI5

• B2.1.2 ACE5-Lite

• B2.1.3 ACE5-LiteDVM

• B2.1.4 ACE5-LiteACP

• B2.1.5 AXI5-Lite

There are also signal and property tables with columns for each interface class:

• B2.2 Signal matrix

• B2.3 Parity check signal matrix

• B2.4 Property matrix

Note that ACE, ACE5, AXI3, AXI4, and AXI4-Lite interface classes are not described in this specification. See [1] for more information on these interfaces.

## B2.1 Summary of interface classes

An example of where different interface classes might be used is shown in Figure B2.1. Note that an AXI5 interface can be configured to meet all of the use-cases.

![](images/cfd8c6ac362b021169cc694bf59ac8e18736c2a2d5d8af157cdc51ed0b0ef926.jpg)  
Figure B2.1: Example system topology showing possible interface classes

## B2.1.1 AXI5

The AXI5 interface class is a generic interface with no property constraints.

Compared with Issue H of this specification, the following properties are now permitted to be enabled for an AXI5 interface:

• Shareable\_Transactions

• CMO\_On\_Read

• CMO\_On\_Write

• Write\_Plus\_CMO

• WriteZero\_Transaction

• Prefetch\_Transaction

• Cache\_Stash\_Transactions

• DVM\_Message\_Support (Receiver only)

• DVM\_v8, DVM\_v8.1, DVM\_v8.4, DVM\_v9.2

• Coherency\_Connection\_Signals

• DeAllocation\_Transactions

• Persist\_CMO

## B2.1.2 ACE5-Lite

An ACE5-Lite interface was previously needed if an AXI interface included any functionality that required AxSNOOP signals. With this version of the specification, an AXI5 interface is recommended for new designs as it now supports all functionality.

## B2.1.3 ACE5-LiteDVM

An ACE5-LiteDVM interface was previously needed if an interface was required to send or receive DVM messages. With this version of the specification, an AXI5 interface is recommended for new designs as it now supports all functionality.

The most common use-case for an ACE5-LiteDVM interface is for a system MMU to receive invalidation messages on the AC channel. The issuing of DVM messages on the AR channel is mostly done by fully coherent CPUs, so is beyond the scope of this specification.

Note that there are some differences between the definition of ACE5-LiteDVM in this specification, compared with Issue H [1].

In this specification, snoop data transfer and bidirectional DVM messages are not supported. Therefore, the following signals described in earlier issues of this specification are no longer required on an ACE5-LiteDVM interface:

• ACSNOOP, all requests on the AC channel can be assumed to be DVM messages.

• ACPROT, not required for DVM messages.

• CRRESP, not required for DVM messages.

## B2.1.4 ACE5-LiteACP

ACE5-LiteACP, which is a subset of ACE5-Lite, is intended for tightly coupling accelerator components to a processor cluster. The interface is optimized for coherent cache line accesses and is less complex than an ACE5-Lite interface.

The following constraints apply to ACE5-LiteACP in order to reduce complexity.

• Data width must be 128b (DATA\_WIDTH = 128).

• Size must be 128b (SIZE\_Present = False).

• Length must be 1 or 4 transfers.

• Burst must be INCR (BURST\_Present = False).

• Memory type must be Write-back, that is AxCACHE[1:0] is 0b11 and AxCACHE[3:2] is not 0b00.

• Cache line size must be 64.

• Some other optional features are not permitted, as Table B2.4 describes.

## B2.1.5 AXI5-Lite

AXI5-Lite is a subset of AXI5 where all transactions have one data transfer. It is intended for communication with register-based components and simple memories when bursts of data transfer are not advantageous.

The key functionality of AXI5-Lite is:

• All transactions have burst length 1.

• Supported Opcodes are WriteNoSnoop and ReadNoSnoop.

• Reordering of responses is permitted when requests have different IDs.

• All accesses are considered Device Non-bufferable.

• Exclusive accesses are not supported.

Note that the burst type is assumed to be INCR, this must be taken into account when calculating a parity value for the AxCTLCHK0 signal.

## B2.2 Signal matrix

In Table B2.2, there is a list of all signals with codes that describe the presence requirements for each interface class. The Presence column describes the property condition used to specify the presence of the signal.

The list of codes that are used is shown in Table B2.1.

Table B2.1: Key to signals table
<table><tr><td>Code</td><td>Manager interfaces</td><td>Subordinate interfaces</td></tr><tr><td>Y</td><td>Mandatory</td><td>Mandatory</td></tr><tr><td>YM</td><td>Mandatory</td><td>Optional</td></tr><tr><td>YS</td><td>Optional</td><td>Mandatory</td></tr><tr><td>0</td><td>Optional</td><td>Optional</td></tr><tr><td>NS</td><td>Optional</td><td>Not present</td></tr><tr><td>N</td><td>Not present</td><td>Not present</td></tr></table>

Table B2.2: Summary of signal presence for each interface class
<table><tr><td>Signal</td><td>Presence</td><td>AXI5</td><td>ACE5- Lite</td><td>ACE5-</td><td>ACE5- LiteDVM LiteACP</td><td>AXI5- Lite</td></tr><tr><td>ACLK</td><td>1</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>ARESETn</td><td>-</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>AWVALID</td><td></td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>AWREADY</td><td>AXI_Transport == Ready</td><td>0</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>AWPENDING</td><td>AXI_Transport == Credited</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWCRDT</td><td>AXI_Transport == Credited</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWCRDTSH</td><td>Shared_Credits_AW == True</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWRP</td><td>Num_RP_AWW &gt; 1</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWSHAREDCRD</td><td>Shared_Credits_AW == True</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWID</td><td>ID_W_WIDTH &gt; 0</td><td>YS</td><td>YS</td><td>YS</td><td>YS</td><td>YS</td></tr><tr><td>AWADDR</td><td>-</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>AWREGION</td><td>REGION_Present</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>AWLEN</td><td>LEN_Present</td><td>YS</td><td>YS</td><td>YS</td><td>YS</td><td>N</td></tr><tr><td>AWSIZE</td><td>SIZE_Present</td><td>YS</td><td>YS</td><td>YS</td><td>N</td><td>0</td></tr><tr><td>AWBURST</td><td>BURST_Present</td><td>YS</td><td>YS</td><td>YS</td><td>N</td><td>N</td></tr><tr><td>AWLOCK</td><td>Exclusive_Accesses</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>AWCACHE</td><td>CACHE_Present</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr></table>

Continued on next page

Chapter B2. Interface classes B2.2. Signal matrix  
Table B2.2 – Continued from previous page
<table><tr><td>Signal</td><td>Presence</td><td>AXI5</td><td>ACE5- Lite</td><td>ACE5- LiteDVM</td><td>ACE5- LiteACP</td><td>AXI5- Lite</td></tr><tr><td>AWPROT</td><td>PROT_Present</td><td>0</td><td>YM</td><td>YM</td><td>YM</td><td>YM</td></tr><tr><td>AWNSE</td><td>RME_Support</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>AWPAS</td><td>PAS_WIDTH &gt; 0</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWINST</td><td>INSTPRIV_Present</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWPRIV</td><td>INSTPRIV_Present</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWQOS</td><td>QOS_Present</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>AWUSER</td><td>USER_REQ_WIDTH &gt; 0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>AWDOMAIN</td><td>Shareable_Transactions</td><td>0</td><td>Y</td><td>Y</td><td>Y</td><td>N</td></tr><tr><td>AWSNOOP</td><td>AWSNOOP_WIDTH &gt; 0</td><td>0</td><td>YS</td><td>YS</td><td>YS</td><td>N</td></tr><tr><td>AWSTASHNID</td><td>STASHNID_Present</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>AWSTASHNIDEN</td><td>STASHNID_Present</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>AWSTASHLPID</td><td>STASHLPID_Present</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>AWSTASHLPIDEN</td><td>STASHLPID_Present</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>AWTRACE</td><td>Trace_Signals</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>AWLOOP</td><td>Loopback_Signals</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>AWMMUVALID</td><td>Untranslated_Transactions == v3 or Untranslated_Transactions == v4</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWMMUSECSID</td><td>SECSID_WIDTH &gt; 0</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWMMUSID</td><td>SID_WIDTH &gt; 0</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWMMUSSIDV</td><td>SSID_WIDTH &gt; 0</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWMMUSSID</td><td>SSID_WIDTH &gt; 0</td><td>0</td><td>0</td><td>N N</td><td>N</td><td>N</td></tr><tr><td>AWMMUATST AWMMUFLOW</td><td>MMUFLOW_Present and (Untranslated_Transactions == v1 or Untranslated_Transactions == True) MMUFLOW_Present and</td><td>0</td><td>0</td><td></td><td>N</td><td>N</td></tr><tr><td></td><td>(Untranslated_Transactions == v2 or Untranslated_Transactions == v3 or Untranslated_Transactions == v4)</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWMMUPASUNKNOWN</td><td>Untranslated_Transactions == v4 and RME_Support and PAS_WIDTH &gt; 0</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWMMUPM</td><td>GDI_Support and Untranslated_Transactions == v4</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWPBHA</td><td>PBHA_Support</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>AWMECID</td><td>MEC_Support</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>AWNSAID</td><td>NSAccess_Identifiers</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr></table>

Continued on next page

Chapter B2. Interface classes B2.2. Signal matrix  
Table B2.2 – Continued from previous page
<table><tr><td>Signal</td><td>Presence</td><td>AXI5</td><td>ACE5- Lite</td><td>ACE5- LiteDVM LiteACP</td><td>ACE5-</td><td>AXI5- Lite</td></tr><tr><td>AWSUBSYSID</td><td>SUBSYSID_WIDTH &gt; 0</td><td>0</td><td>0</td><td>0</td><td>N</td><td>0</td></tr><tr><td>AWATOP</td><td>Atomic_Transactions</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>AWMPAM</td><td>MPAM_Support != False</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>AWIDUNQ</td><td>Unique_ID_Support</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>AWCMO</td><td>CMO_On_Write</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>AWTAGOP</td><td>MTE_Support != False</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>AWACT</td><td>ACT_Support != False</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWACTV</td><td>ACT_Support != False</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>WVALID</td><td>-</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>WREADY</td><td>AXI_Transport == Ready</td><td>0</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>WPENDING</td><td>AXI_Transport == Credited</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>WCRDT</td><td>AXI_Transport == Credited</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>WCRDTSH</td><td>Shared_Credits_W == True</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>WRP</td><td>Num_RP_AWW &gt; 1</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>WSHAREDCRD</td><td>Shared_Credits_W == True</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>WDATA</td><td></td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>WSTRB</td><td>WSTRB_Present</td><td>YS</td><td>YS</td><td>YS</td><td>YS</td><td>YS</td></tr><tr><td>WTAG</td><td>MTE_Support != False</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>WTAGUPDATE</td><td>MTE_Support != False</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>WLAST</td><td>WLAST_Present</td><td>YM</td><td>YM</td><td>YM</td><td>YM</td><td>N</td></tr><tr><td>WUSER</td><td>USER_DATA_WIDTH &gt; 0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>WPOISON</td><td>Poison</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>WTRACE</td><td>Trace_Signals</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>BVALID</td><td>-</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>BREADY</td><td>AXI_Transport == Ready</td><td>0</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>BPENDING</td><td>AXI_Transport == Credited</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>BCRDT</td><td>AXI_Transport == Credited</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>BID</td><td>ID_W_WIDTH &gt; 0</td><td>YS</td><td>YS</td><td>YS</td><td>YS</td><td>YS</td></tr><tr><td>BIDUNQ</td><td>Unique_ID_Support</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>BRESP</td><td>BRESP_WIDTH &gt; 0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>BCOMP</td><td>(Persist_CMO and CMO_On_Write) or MTE_Support == Standard</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr></table>

Continued on next page

Chapter B2. Interface classes B2.2. Signal matrix  
Table B2.2 – Continued from previous page
<table><tr><td>Signal</td><td>Presence</td><td>AXI5</td><td>ACE5- Lite</td><td>ACE5- LiteDVM</td><td>ACE5- LiteACP</td><td>AXI5- Lite</td></tr><tr><td>BPERSIST</td><td>Persist_CMO and CMO_On_Write</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>BTAGMATCH</td><td>MTE_Support == Standard</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>BUSER</td><td>USER_RESP_WIDTH &gt; 0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>BTRACE</td><td>Trace_Signals</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>BLOOP</td><td>Loopback_Signals</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>BBUSY</td><td>Busy_Support</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ARVALID</td><td></td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>ARREADY</td><td>AXI_Transport == Ready</td><td>0</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>ARPENDING</td><td>AXI_Transport == Credited</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARCRDT</td><td>AXI_Transport == Credited</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARCRDTSH</td><td>Shared_Credits_AR == True</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARRP</td><td>Num_RP_AR &gt; 1</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARSHAREDCRD</td><td>Shared_Credits_AR == True</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARID</td><td>ID_R_WIDTH &gt; 0</td><td>YS</td><td>YS</td><td>YS</td><td>YS</td><td>YS</td></tr><tr><td>ARADDR</td><td>-</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>ARREGION</td><td>REGION_Present</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ARLEN</td><td>LEN_Present</td><td>YS</td><td>YS</td><td>YS</td><td>YS</td><td>N</td></tr><tr><td>ARSIZE</td><td>SIZE_Present</td><td>YS</td><td>YS</td><td>YS</td><td>N</td><td>0</td></tr><tr><td>ARBURST</td><td>BURST_Present</td><td>YS</td><td>YS</td><td>YS</td><td>N</td><td>N</td></tr><tr><td>ARLOCK</td><td>Exclusive_Accesses</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ARCACHE</td><td>CACHE_Present</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>ARPROT</td><td>PROT_Present</td><td>0</td><td>YM</td><td>YM</td><td>YM</td><td>YM</td></tr><tr><td>ARNSE</td><td>RME_Support</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ARPAS</td><td>PAS_WIDTH &gt; 0</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARINST</td><td>INSTPRIV_Present</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARPRIV</td><td>INSTPRIV_Present</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARQOS</td><td>QOS_Present</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ARUSER</td><td>USER_REQ_WIDTH &gt; 0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>ARDOMAIN</td><td>Shareable_Transactions</td><td>0</td><td>Y</td><td>Y</td><td>Y</td><td>N</td></tr><tr><td>ARSNOOP</td><td>ARSNOOP_WIDTH &gt; 0</td><td>0</td><td>YS</td><td>YS</td><td>0</td><td>N</td></tr><tr><td>ARTRACE</td><td>Trace_Signals</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>ARLOOP</td><td>Loopback_Signals</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr></table>

Continued on next page

Table B2.2 – Continued from previous page
<table><tr><td>Signal</td><td>Presence</td><td>AXI5</td><td>ACE5- Lite</td><td>ACE5- LiteDVM</td><td>ACE5- LiteACP</td><td>AXI5- Lite</td></tr><tr><td>ARMMUVALID</td><td>Untranslated_Transactions == v3 or Untranslated_Transactions == v4</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARMMUSECSID</td><td>SECSID_WIDTH &gt; 0</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARMMUSID</td><td>SID_WIDTH &gt; 0</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARMMUSSIDV</td><td>SSID_WIDTH &gt; 0</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARMMUSSID</td><td>SSID_WIDTH &gt; 0</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARMMUATST</td><td>MMUFLOW_Present and (Untranslated_Transactions == v1 or Untranslated_Transactions == True)</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARMMUFLOW</td><td>MMUFLOW_Present and (Untranslated_Transactions == v2 or Untranslated_Transactions == v3 or Untranslated_Transactions == v4)</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARMMUPASUNKNOWN</td><td>Untranslated_Transactions == v4 and RME_Support and PAS_WIDTH &gt; 0</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARMMUPM</td><td>GDI_Support and Untranslated_Transactions == v4</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARPBHA</td><td>PBHA_Support</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ARMECID</td><td>MEC_Support</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ARNSAID</td><td>NSAccess_Identifiers</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ARSUBSYSID</td><td>SUBSYSID_WIDTH &gt; 0</td><td>0</td><td>0</td><td>0</td><td>N</td><td>0</td></tr><tr><td>ARMPAM</td><td>MPAM_Support != False</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>ARCHUNKEN</td><td>Read_Data_Chunking</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>ARIDUNQ</td><td>Unique_ID_Support</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>ARTAGOP</td><td>MTE_Support != False</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ARACT</td><td>ACT_Support != False</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARACTV</td><td>ACT_Support != False</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>RVALID</td><td></td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>RREADY</td><td>AXI_Transport == Ready</td><td>0</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>RPENDING</td><td>AXI_Transport == Credited</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>RCRDT</td><td>AXI_Transport == Credited</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>RID</td><td>ID_R_WIDTH &gt; 0</td><td>YS</td><td>YS</td><td>YS</td><td>YS</td><td>YS</td></tr><tr><td>RIDUNQ</td><td>Unique_ID_Support</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>RDATA</td><td>-</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td><td>Y</td></tr><tr><td>RTAG</td><td>MTE_Support != False</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr></table>

Continued on next page

Chapter B2. Interface classes B2.2. Signal matrix  
Table B2.2 – Continued from previous page
<table><tr><td>Signal</td><td>Presence</td><td>AXI5</td><td>ACE5- Lite</td><td>ACE5- LiteDVM LiteACP</td><td>ACE5-</td><td>AXI5- Lite</td></tr><tr><td>RRESP</td><td>RRESP_WIDTH &gt; 0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>RLAST</td><td>RLAST_Present</td><td>YS</td><td>YS</td><td>YS</td><td>YS</td><td>N</td></tr><tr><td>RUSER</td><td>USER_DATA_WIDTH &gt; 0 or USER_RESP_WIDTH &gt; 0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>RPOISON</td><td>Poison</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>RTRACE</td><td>Trace_Signals</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>RLOOP</td><td>Loopback_Signals</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>RCHUNKV</td><td>Read_Data_Chunking</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>RCHUNKNUM</td><td>RCHUNKNUM_WIDTH &gt; 0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>RCHUNKSTRB</td><td>RCHUNKSTRB_WIDTH &gt; 0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>RBUSY</td><td>Busy_Support</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ACVALID</td><td>DVM_Message_Support</td><td>0</td><td>N</td><td>Y</td><td>N</td><td>N</td></tr><tr><td>ACREADY</td><td>DVM_Message_Support and AXI_Transport == Ready</td><td>0</td><td>N</td><td>Y</td><td>N</td><td>N</td></tr><tr><td>ACPENDING</td><td>DVM_Message_Support and AXI_Transport == Credited</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ACCRDT</td><td>DVM_Message_Support and AXI_Transport == Credited</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ACADDR</td><td>DVM_Message_Support and AXI_Transport == Credited</td><td>0</td><td>N</td><td>Y</td><td>N</td><td>N</td></tr><tr><td>ACVMIDEXT</td><td>DVM_Message_Support and (DVM_v8.1 or DVM_v8.4 or DVM_v9.2)</td><td>0</td><td>N</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ACTRACE</td><td>DVM_Message_Support and Trace_Signals</td><td>0</td><td>N</td><td>0</td><td>N</td><td>N</td></tr><tr><td>CRVALID</td><td>DVM_Message_Support</td><td>0</td><td>N</td><td>Y</td><td>N</td><td>N</td></tr><tr><td>CRREADY</td><td>DVM_Message_Support and AXI_Transport == Ready</td><td>0</td><td>N</td><td>Y</td><td>N</td><td>N</td></tr><tr><td>CRPENDING</td><td>DVM_Message_Support and AXI_Transport == Credited</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>CRCRDT</td><td>DVM_Message_Support and AXI_Transport == Credited</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>CRTRACE</td><td>DVM_Message_Support and Trace_Signals</td><td>0</td><td>N</td><td>0</td><td>N</td><td>N</td></tr><tr><td>AWAKEUP</td><td>Wakeup_Signals</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></table>

Continued on next page

Table B2.2 – Continued from previous page
<table><tr><td>Signal</td><td>Presence</td><td>AXI5</td><td>ACE5- Lite</td><td>ACE5-</td><td>ACE5- LiteDVM LiteACP</td><td>AXI5- Lite</td></tr><tr><td>ACWAKEUP</td><td>Wakeup_Signals and DVM_Message_Support</td><td>0</td><td>N</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ACTIVATEREQ</td><td>Credit_Control == Implicit_Return_Uni</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ACTIVATEACK</td><td>Credit_Control == Implicit_Return_Uni</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ASKSTOP</td><td>Credit_Control == Implicit_Return_Uni</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ACTIVATEREQD</td><td>DVM_Message_Support and Credit_Control == Implicit_Return_Uni</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ACTIVATEACKD</td><td>DVM_Message_Support and Credit_Control == Implicit_Return_Uni</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ASKSTOPD</td><td>DVM_Message_Support and Credit_Control == Implicit_Return_Uni</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>VARQOSACCEPT</td><td>QoS_Accept</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>VAWQOSACCEPT</td><td>QoS_Accept</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>SYSCOREQ</td><td>Coherency_Connection_Signals</td><td>0</td><td>N</td><td>0</td><td>N</td><td>N</td></tr><tr><td>SYSCOACK</td><td>Coherency_Connection_Signals</td><td>0</td><td>N</td><td>0</td><td>N</td><td>N</td></tr><tr><td>BROADCASTATOMIC</td><td>-</td><td>NS</td><td>NS</td><td>NS</td><td>N</td><td>N</td></tr><tr><td>BROADCASTSHAREABLE</td><td></td><td>NS</td><td>NS</td><td>NS</td><td>NS</td><td>N</td></tr><tr><td>BROADCASTCACHEMAINT</td><td></td><td>NS</td><td>NS</td><td>NS</td><td>N</td><td>N</td></tr><tr><td>BROADCASTCMOPOPA -</td><td></td><td>NS</td><td>NS</td><td>NS</td><td>N</td><td>N</td></tr><tr><td>BROADCASTPERSIST -</td><td></td><td>NS</td><td>NS</td><td>NS</td><td>N</td><td>N</td></tr><tr><td>BROADCASTSTORAGE 1</td><td></td><td>NS</td><td>N</td><td>N</td><td>N</td><td>N</td></tr></table>

## B2.3 Parity check signal matrix

Parity check signals for each interface type are shown in Table B2.3, using the codes defined in Table B2.1. Parity check signals are described in A16.2.3 Parity check signals.

Table B2.3: Summary of check signal presence for each interface class
<table><tr><td>Signal</td><td>AXI5</td><td>ACE5- Lite</td><td>ACE5- LiteDVM</td><td>ACE5- LiteACP</td><td>AXI5- Lite</td></tr><tr><td>AWVALIDCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>AWREADYCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>AWPENDINGCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWCRDTCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWCRDTSHCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWRPCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWSHAREDCRDCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWIDCHK</td><td>0</td><td>0</td><td>O</td><td>0</td><td>O</td></tr><tr><td>AWADDRCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>AWLENCHK</td><td>0</td><td>0</td><td>O</td><td>0</td><td>N</td></tr><tr><td>AWCTLCHK0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>AWCTLCHK1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>AWCTLCHK2</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>AWCTLCHK3</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>AWPASCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWINSTPRIVCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWUSERCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>AWSTASHNIDCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>AWSTASHLPIDCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>AWTRACECHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>AWLOOPCHK</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>AWMMUCHK</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWMMUSIDCHK</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWMMUSSIDCHK</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWMMUPASUNKNOWNCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWMMUPMCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>AWPBHACHK</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>AWNSAIDCHK</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr></table>

Continued on next page

Table B2.3 – Continued from previous page
<table><tr><td>Signal</td><td>AXI5</td><td>ACE5- Lite</td><td>ACE5- LiteDVM</td><td>ACE5- LiteACP</td><td>AXI5- Lite</td></tr><tr><td>AWMPAMCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>AWSUBSYSIDCHK</td><td>0</td><td>0</td><td>0</td><td>N</td><td>0</td></tr><tr><td>AWMECIDCHK</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>AWACTCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>WVALIDCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>WREADYCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>WPENDINGCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>WCRDTCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>WCRDTSHCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>WRPCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>WSHAREDCRDCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>WDATACHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>WSTRBCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>WTAGCHK</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>WLASTCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>WUSERCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>WPOISONCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>WTRACECHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>BVALIDCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>BREADYCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>BPENDINGCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>BCRDTCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>BIDCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>BRESPCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>BUSERCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>BTRACECHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>BLOOPCHK</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ARVALIDCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>ARREADYCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>ARPENDINGCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARCRDTCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARCRDTSHCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr></table>

Continued on next page

Table B2.3 – Continued from previous page
<table><tr><td>Signal</td><td>AXI5</td><td>ACE5- Lite</td><td>ACE5- LiteDVM</td><td>ACE5- LiteACP</td><td>AXI5- Lite</td></tr><tr><td>ARRPCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARSHAREDCRDCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARIDCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>ARADDRCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>ARLENCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>ARCTLCHK0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>ARCTLCHK1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>ARCTLCHK2</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>ARCTLCHK3</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>ARPASCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARINSTPRIVCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARUSERCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>ARTRACECHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>ARLOOPCHK</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ARMMUCHK</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARMMUSIDCHK</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARMMUSSIDCHK</td><td>0</td><td>0</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARMMUPASUNKNOWNCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARMMUPMCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ARNSAIDCHK</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ARMPAMCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>ARPBHACHK</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ARSUBSYSIDCHK</td><td>0</td><td>0</td><td>0</td><td>N</td><td>0</td></tr><tr><td>ARMECIDCHK</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ARACTCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>RVALIDCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>RREADYCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>RPENDINGCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>RCRDTCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>RIDCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>RDATACHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>RTAGCHK</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr></table>

Continued on next page

Table B2.3 – Continued from previous page
<table><tr><td>Signal</td><td>AXI5</td><td>ACE5- Lite</td><td>ACE5- LiteDVM</td><td>ACE5- LiteACP</td><td>AXI5- Lite</td></tr><tr><td>RRESPCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>RLASTCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>RCHUNKCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>N</td></tr><tr><td>RUSERCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>RPOISONCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>RTRACECHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>RLOOPCHK</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ACVALIDCHK</td><td>0</td><td>N</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ACREADYCHK</td><td>0</td><td>N</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ACPENDINGCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ACCRDTCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ACADDRCHK</td><td>0</td><td>N</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ACVMIDEXTCHK</td><td>0</td><td>N</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ACTRACECHK</td><td>0</td><td>N</td><td>0</td><td>N</td><td>N</td></tr><tr><td>CRVALIDCHK</td><td>0</td><td>N</td><td>0</td><td>N</td><td>N</td></tr><tr><td>CRREADYCHK</td><td>0</td><td>N</td><td>0</td><td>N</td><td>N</td></tr><tr><td>CRPENDINGCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>CRCRDTCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>CRTRACECHK</td><td>0</td><td>N</td><td>0</td><td>N</td><td>N</td></tr><tr><td>VAWQOSACCEPTCHK</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>VARQOSACCEPTCHK</td><td>0</td><td>0</td><td>0</td><td>N</td><td>N</td></tr><tr><td>AWAKEUPCHK</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>ACWAKEUPCHK</td><td>0</td><td>N</td><td>0</td><td>N</td><td>N</td></tr><tr><td>ACTIVATEREQCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ACTIVATEACKCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ASKSTOPCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ACTIVATEREQDCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ACTIVATEACKDCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>ASKSTOPDCHK</td><td>0</td><td>N</td><td>N</td><td>N</td><td>N</td></tr><tr><td>SYSCOREQCHK</td><td>0</td><td>N</td><td>0</td><td>N</td><td>N</td></tr><tr><td>SYSCOACKCHK</td><td>0</td><td>N</td><td>0</td><td>N</td><td>N</td></tr></table>

## B2.4 Property matrix

A list of all properties is shown in Table B2.4.

The table shows the document issue in which the property was introduced and all legal values for the property. There is a column for each interface class which shows the legal values of that property for that interface class. A dash means there are no constraints on the property value.

Note that for User signals and User Loopback signals, the maximum width values are a recommendation rather than a rule. See A12.5 User defined signaling and A12.4 User Loopback signaling for more information.

Table B2.4: Summary of interface property constraints
<table><tr><td>Property</td><td>Issue</td><td>Values</td><td>AXI5</td><td>ACE5- Lite</td><td>ACE5- LiteDVM</td><td>ACE5- LiteACP</td><td>AXI5- Lite</td></tr><tr><td>ACT_Support</td><td>L</td><td>v1, False</td><td></td><td>False</td><td>False</td><td>False</td><td>False</td></tr><tr><td>ACT_R_WIDTH</td><td>L</td><td>0,16..32</td><td></td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>ACT_W_WIDTH</td><td>L</td><td>0,16..32</td><td></td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>ADDR_WIDTH</td><td>H</td><td>1..64</td><td></td><td></td><td>-</td><td>1</td><td>-</td></tr><tr><td>ARSNOOP_WIDTH</td><td>J</td><td>0,4</td><td></td><td>-</td><td>-</td><td>-</td><td>0</td></tr><tr><td>Atomic_Transactions</td><td>F</td><td>True, False</td><td></td><td>1</td><td>-</td><td>False</td><td>False</td></tr><tr><td>AWCMO_WIDTH</td><td>J</td><td>0,2,3</td><td>一</td><td></td><td>-</td><td>0</td><td>0</td></tr><tr><td>AWSNOOP_WIDTH</td><td>J</td><td>0,4,5</td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>AXI_Transport</td><td>L</td><td>Ready, Credited</td><td></td><td>Ready</td><td>Ready</td><td>Ready</td><td>Ready</td></tr><tr><td>BRESP_WIDTH</td><td>J</td><td>0,2,3</td><td></td><td></td><td>-</td><td>-</td><td>-</td></tr><tr><td>BURST_Present</td><td>J</td><td>True, False</td><td></td><td></td><td>-</td><td>False</td><td>False</td></tr><tr><td>Busy_Support</td><td>J</td><td>True, False</td><td></td><td></td><td>-</td><td>False</td><td>False</td></tr><tr><td>Cache_Line_Size</td><td>K</td><td>16, 32, 64, 128, 256, 512, 1024, 2048</td><td></td><td></td><td></td><td>64</td><td>I</td></tr><tr><td>CACHE_Present</td><td>J</td><td>True, False</td><td></td><td></td><td></td><td></td><td>False</td></tr><tr><td>Cache_Stash_Transactions</td><td>F</td><td>True, Basic, False</td><td></td><td></td><td></td><td></td><td>False</td></tr><tr><td>Check_Type</td><td>F</td><td>Odd_Parity_Byte_All, Odd_Parity_Byte_Data, False</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>CMO_On_Read</td><td>G</td><td>True, False</td><td></td><td></td><td></td><td>False</td><td>False</td></tr><tr><td>CMO_On_Write</td><td>G</td><td>True, False</td><td></td><td></td><td></td><td>False</td><td>False</td></tr><tr><td>Coherency_Connection_Signals</td><td>F</td><td>True, False</td><td></td><td>False</td><td>=</td><td>False</td><td>False</td></tr><tr><td>Consistent_DECERR</td><td>H</td><td>True, False</td><td></td><td>1</td><td>-</td><td>-</td><td>True</td></tr><tr><td>Credit_Control</td><td>L</td><td>False, Implicit_Return_Uni</td><td></td><td>False</td><td>False</td><td>False</td><td>False</td></tr><tr><td>DATA_WIDTH</td><td>H</td><td>8, 16, 32, 64, 128, 256, 512, 1024</td><td></td><td></td><td></td><td>128</td><td></td></tr></table>

Continued on next page

Chapter B2. Interface classes B2.4. Property matrix  
Table B2.4 – Continued from previous page
<table><tr><td>Property</td><td>Issue</td><td>Values</td><td>AXI5</td><td>ACE5- Lite</td><td>ACE5- LiteDVM</td><td>ACE5- LiteACP</td><td>AXI5- Lite</td></tr><tr><td>DeAllocation_Transactions</td><td>F</td><td>True, False</td><td></td><td></td><td>I</td><td>False</td><td>False</td></tr><tr><td>Device_Normal_Independence</td><td>K</td><td>True, False</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>DVM_Message_Support</td><td>H</td><td>Receiver, False</td><td></td><td>False</td><td>Receiver</td><td>False</td><td>False</td></tr><tr><td>DVM_v8</td><td>E</td><td>True, False</td><td></td><td>False</td><td></td><td>False</td><td>False</td></tr><tr><td>DVM_v8.1</td><td>F</td><td>True, False</td><td></td><td>False</td><td></td><td>False</td><td>False</td></tr><tr><td>DVM_v8.4</td><td>H</td><td>True, False</td><td></td><td>False</td><td></td><td>False</td><td>False</td></tr><tr><td>DVM_v9.2</td><td>J</td><td>True, False</td><td></td><td>False</td><td></td><td>False</td><td>False</td></tr><tr><td>Exclusive_Accesses</td><td>H</td><td>True, False</td><td></td><td>-</td><td></td><td>False</td><td>False</td></tr><tr><td>Fixed_Burst_Disable</td><td>K</td><td>True, False</td><td></td><td>-</td><td></td><td>False</td><td>False</td></tr><tr><td>GDI_Support</td><td>L</td><td>True, False</td><td></td><td>False</td><td>False</td><td>False</td><td>False</td></tr><tr><td>ID_R_WIDTH</td><td>H</td><td>0..32</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>ID_W_WIDTH</td><td>H</td><td>0..32</td><td></td><td></td><td></td><td>-</td><td>-</td></tr><tr><td>INSTPRIV_Present</td><td>L</td><td>True, False</td><td></td><td>False</td><td>False</td><td>False</td><td>False</td></tr><tr><td>InvalidateHint_Transaction</td><td>J</td><td>True, False</td><td></td><td></td><td></td><td>False</td><td>False</td></tr><tr><td>LEN_Present</td><td>J</td><td>True, False</td><td></td><td></td><td></td><td>-</td><td>False</td></tr><tr><td>LOOP_R_WIDTH</td><td>H</td><td>0..8</td><td></td><td></td><td></td><td>0</td><td>0</td></tr><tr><td>LOOP_W_WIDTH</td><td>H</td><td>0..8</td><td></td><td></td><td></td><td>0</td><td>0</td></tr><tr><td>Loopback_Signals</td><td>F</td><td>True, False</td><td></td><td></td><td></td><td>False</td><td>False</td></tr><tr><td>Max_Transaction_Bytes</td><td>H</td><td>64, 128, 256, 512, 1024, 2048, 4096</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>MMUFLOW_Present</td><td>J</td><td>True, False</td><td></td><td></td><td>False</td><td>False</td><td>False</td></tr><tr><td>MEC_Support</td><td>K</td><td>True, False</td><td></td><td></td><td></td><td>False</td><td>False</td></tr><tr><td>MECID_WIDTH</td><td>K</td><td>0,16</td><td></td><td></td><td></td><td>0</td><td>0</td></tr><tr><td>MPAM_Support</td><td>K</td><td>MPAM_9_1, MPAM_12_1, False</td><td></td><td></td><td></td><td></td><td>False</td></tr><tr><td>MPAM_WIDTH</td><td>K</td><td>0, 11, 12, 14, 15</td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>MTE_Support</td><td>K</td><td>Standard, Simplified Basic, False</td><td></td><td></td><td>Basic, False</td><td>False</td><td>False</td></tr><tr><td>Multi_Copy_Atomicity</td><td>E</td><td>True, False</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>NSAccess_Identifiers</td><td>F</td><td>True, False</td><td></td><td>一</td><td>1</td><td>False</td><td>False</td></tr><tr><td>Num_RP_AR</td><td>L</td><td>1..8</td><td></td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>Num_RP_AWW</td><td>L</td><td>1..8</td><td></td><td>1</td><td>1</td><td>1</td><td>1</td></tr><tr><td>Ordered_Write_Observation</td><td>E</td><td>True, False</td><td></td><td></td><td></td><td></td><td>1</td></tr></table>

Continued on next page

Chapter B2. Interface classes B2.4. Property matrix  
Table B2.4 – Continued from previous page
<table><tr><td>Property</td><td>Issue</td><td>Values</td><td>AXI5</td><td>ACE5- Lite</td><td>ACE5- LiteDVM</td><td>ACE5- LiteACP</td><td>AXI5- Lite</td></tr><tr><td>PAS_WIDTH</td><td>L</td><td>0..3</td><td></td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>PBHA_Support</td><td>J</td><td>True, False</td><td></td><td></td><td></td><td>False</td><td>False</td></tr><tr><td>PROT_Present</td><td>J</td><td>True, False</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Persist_CMO</td><td>F</td><td>True, False</td><td></td><td></td><td></td><td>False</td><td>False</td></tr><tr><td>Poison</td><td>F</td><td>True, False</td><td></td><td></td><td></td><td></td><td>1</td></tr><tr><td>Prefetch_Transaction</td><td>H</td><td>True, False</td><td></td><td></td><td></td><td>False</td><td>False</td></tr><tr><td>QoS_Accept</td><td>F</td><td>True, False</td><td></td><td></td><td></td><td>False</td><td>False</td></tr><tr><td>QOS_Present</td><td>J</td><td>True, False</td><td></td><td></td><td></td><td>False</td><td>False</td></tr><tr><td>RCHUNKNUM_WIDTH</td><td>J</td><td>0, 1, 5, 6, 7, 8</td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>RCHUNKSTRB_WIDTH</td><td>J</td><td>0,1, 2, 4,8</td><td></td><td></td><td></td><td></td><td>0</td></tr><tr><td>Read_Data_Chunking</td><td>G</td><td>True, False</td><td></td><td></td><td></td><td></td><td>False</td></tr><tr><td>Read_Interleaving_Disabled</td><td>G</td><td>True, False</td><td></td><td></td><td></td><td></td><td>False</td></tr><tr><td>REGION_Present</td><td>J</td><td>True, False</td><td></td><td></td><td></td><td>False</td><td>False</td></tr><tr><td>Regular_Transactions_Only</td><td>H</td><td>True, False</td><td></td><td></td><td></td><td>False</td><td>False</td></tr><tr><td>RLAST_Present</td><td>J</td><td>True, False</td><td></td><td></td><td></td><td></td><td>False</td></tr><tr><td>RME_Support</td><td>J</td><td>True, False</td><td></td><td></td><td></td><td>False</td><td>False</td></tr><tr><td>RRESP_WIDTH</td><td>J</td><td>0,2,3</td><td></td><td></td><td>-</td><td>-</td><td>-</td></tr><tr><td>SECSID_WIDTH</td><td>J</td><td>0,1,2</td><td></td><td></td><td>0</td><td>0</td><td>0</td></tr><tr><td>Shareable_Cache_Support</td><td>J</td><td>True, False</td><td></td><td></td><td>False</td><td>False</td><td>False</td></tr><tr><td>Shareable_Transactions</td><td>H</td><td>True, False</td><td></td><td>True</td><td>True</td><td>True</td><td>False</td></tr><tr><td>Shared_Credits_AR</td><td>L</td><td>True, False</td><td></td><td>False</td><td>False</td><td>False</td><td>False</td></tr><tr><td>Shared_Credits_AW</td><td>L</td><td>True, False</td><td></td><td>False</td><td>False</td><td>False</td><td>False</td></tr><tr><td>Shared_Credits_W</td><td>L</td><td>True, False</td><td></td><td>False</td><td>False</td><td>False</td><td>False</td></tr><tr><td>SID_WIDTH</td><td>H</td><td>0..32</td><td></td><td></td><td>0</td><td>0</td><td>0</td></tr><tr><td>SIZE_Present</td><td>J</td><td>True, False</td><td></td><td></td><td>-</td><td>False</td><td>-</td></tr><tr><td>SSID_WIDTH</td><td>H</td><td>0..20</td><td></td><td></td><td>0</td><td>0</td><td>0</td></tr><tr><td>STASHLPID_Present</td><td>J</td><td>True, False</td><td></td><td></td><td>1</td><td>-</td><td>False</td></tr><tr><td>STASHNID_Present</td><td>J</td><td>True, False</td><td></td><td></td><td></td><td></td><td>False</td></tr><tr><td>Storage_CMO</td><td>L</td><td>True, False</td><td></td><td>False</td><td>False</td><td>False</td><td>False</td></tr><tr><td>SUBSYSID_WIDTH</td><td>J</td><td>0..8</td><td></td><td></td><td></td><td>0</td><td></td></tr><tr><td>Trace_Signals</td><td>F</td><td>True, False</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Unique_ID_Support</td><td>G</td><td>True, False</td><td></td><td></td><td></td><td></td><td></td></tr></table>

Continued on next page

Chapter B2. Interface classes B2.4. Property matrix  
Table B2.4 – Continued from previous page
<table><tr><td>Property</td><td>Issue</td><td>Values</td><td>AXI5</td><td>ACE5- Lite</td><td>ACE5- LiteDVM</td><td>ACE5- LiteACP</td><td>AXI5- Lite</td></tr><tr><td>UnstashTranslation_Transaction J</td><td></td><td>True, False</td><td></td><td></td><td>False</td><td>False</td><td>False</td></tr><tr><td>Untranslated_Transactions</td><td>F</td><td>v4, v3, v2, v1, True, False</td><td></td><td></td><td>False</td><td>False</td><td>False</td></tr><tr><td>USER_DATA_WIDTH</td><td>H</td><td>0..DATA_WIDTH/2</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>USER_REQ_WIDTH</td><td>H</td><td>0..128</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>USER_RESP_WIDTH</td><td>H</td><td>0..16</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Wrap_CLS_Modifiable</td><td>L</td><td>True, False</td><td></td><td></td><td></td><td></td><td>False</td></tr><tr><td>WLAST_Present</td><td>J</td><td>True, False</td><td></td><td></td><td></td><td></td><td>False</td></tr><tr><td>WSTRB_Present</td><td>J</td><td>True, False</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Wakeup_Signals</td><td>F</td><td>True, False</td><td></td><td></td><td></td><td>一</td><td>–</td></tr><tr><td>Write_Plus_CMO</td><td>H</td><td>True, False</td><td></td><td></td><td></td><td>False</td><td>False</td></tr><tr><td>WriteDeferrable_Transaction</td><td>J</td><td>True, False</td><td></td><td></td><td></td><td>False</td><td>False</td></tr><tr><td>WriteZero_Transaction</td><td>H</td><td>True, False</td><td></td><td></td><td></td><td>False</td><td>False</td></tr><tr><td>WriteNoSnoopFull_Transaction</td><td>K</td><td>True, False</td><td></td><td></td><td></td><td>False</td><td>False</td></tr></table>

Chapter B3 Summary of ID constraints

This appendix is a summary of ID usage constraints in this document.

Must use an ID that is unique in-flight on the same channels:

• Atomic transactions

• Prefetch transactions

• WriteZero transactions

• WriteDeferrable transactions

• InvalidateHint transactions

• Read transactions with data chunking enabled

• Transactions which transport MTE tags

• UnstashTranslation transactions

• ACT transactions

Must not use the same ID for in-flight transactions on the same channels:

• DVM Complete and non-DVM Complete transactions

• StashOnce and non-StashOnce transactions

• Translated and untranslated transactions

• StashTranslation and non-StashTranslation transactions

Must use the same ID:

• Multiple outstanding requests that require ordering between them.

• Transactions in an exclusive access pair.

## Chapter B4 Revisions

This appendix describes the technical changes between released issues of this specification.

It contains the following sections:

• B4.1 Differences between Issue H.c and Issue J

• B4.2 Differences between Issue J and Issue K

• B4.3 Differences between Issue K and Issue L

## B4.1 Differences between Issue H.c and Issue J

<table><tr><td>Feature</td><td>Change</td><td>Detail</td></tr><tr><td>AXI3, AXI4, AXI4-Lite interfaces</td><td>Removal</td><td>AXI3, AXI4, and AXI4-Lite content is removed from the specification. These interface types are not recommended for new designs and have been superseded by the AXI5 interface. Removed content can be accessed by downloading earlier versions of this specification.</td></tr><tr><td>ACE and ACE5 interfaces</td><td>Removal</td><td>ACE and ACE5 content is removed from the specification. AMBA CHI is recommended for fully coherent agents and is actively supported.</td></tr><tr><td>ACE5-Lite, ACE5-LiteDVM, ACE5-LiteACP, and AXI5-Lite interfaces</td><td>Update</td><td>ACE5-Lite, ACE5-LiteDVM, ACE5-LiteACP, and AXI5-Lite interfaces are described through constraints on property values and signal presence.</td></tr><tr><td>AXI5 interface</td><td>New feature</td><td>All optional features in this specification are now applicable to AXI5 class interfaces. AXI5 is expected to be used for general-purpose interfaces.</td></tr><tr><td>Caching shareable lines</td><td>New feature</td><td>Support for storing shareable lines in a system cache.</td></tr><tr><td>Cache stashing</td><td>New feature</td><td>There is an additional Basic option for cache stashing to support interfaces which use only a sub-set of the cache stashing protocol.</td></tr><tr><td>Invalidate hint</td><td>New feature</td><td>InvalidateHint transaction, which can be used by an agent when it is finished working with a data set and that data might be allocated in a downstream cache.</td></tr><tr><td>WriteDeferrable transaction</td><td>New feature</td><td>A 64-byte atomic store operation that might not be accepted by the Subordinate.</td></tr><tr><td>Realm Management Extension (RME)</td><td>New feature</td><td>Enhanced memory protection.</td></tr><tr><td>DVM v9.2</td><td>New feature</td><td>New messages to support the Armv9.2 architecture.</td></tr><tr><td>Untranslated transactions</td><td>New feature</td><td>Version 3 adds support for mixing translated and untranslated transactions.</td></tr><tr><td></td><td>New feature</td><td>UnstashTranslation transaction, used as a deallocation hint for an address translation cache.</td></tr><tr><td>Page-based Hardware Attributes (PBHA)</td><td>New feature</td><td>4-bit descriptors associated with a translation table entry that can be annotated onto a transaction request.</td></tr><tr><td>Subsystem Identifier</td><td>New feature</td><td>An additional identifier that can be added to transaction requests to indicate from which subsystem they originate.</td></tr><tr><td>Subordinate busy</td><td>New feature</td><td>Response signal that indicates the level of activity of a Subordinate.</td></tr><tr><td>Unique ID indicator</td><td>Clarification</td><td>Added rules for the Unique ID Indicator and Atomic transactions that include read and write responses.</td></tr><tr><td></td><td>Correction</td><td>BIDUNQ is not required to follow AWIDUNQ for non-Completion write responses such as Persist and MTE Match.</td></tr><tr><td>Memory Tagging Extension (MTE)</td><td>Clarification</td><td>A WritePtlCMO or WriteFullCMO with AWTAGOP Transfer must be Non-shareable. This is because a WriteUnique with AWTAGOP of</td></tr></table>

Continued on next page

Table B4.1 – Continued from previous page
<table><tr><td>Feature</td><td>Change</td><td>Detail</td></tr><tr><td rowspan="3"></td><td>Clarification</td><td>Transactions that carry MTE tags must not cross a cache line boundary.</td></tr><tr><td>Additional requirement</td><td>Read transactions with the MTE opcode of Fetch must be Regular.</td></tr><tr><td>Enhancement</td><td>The text describing MTE and Poison is enhanced with additional guidance.</td></tr><tr><td>Prefetch transaction</td><td>Clarification</td><td>A Prefetch request must not be used to signal that a line can be fetched into a managed or visible cache.</td></tr><tr><td>Wakeup signals</td><td>Clarification</td><td>It is permitted for Wakeup signals to be driven from a glitch-free OR tree if that implementation is safe for asynchronous sampling.</td></tr><tr><td>Multi-copy atomicity</td><td>Update</td><td>The requirements for multi-copy atomicity are updated for the Armv8 architecture.</td></tr><tr><td rowspan="2">Exclusive accesses</td><td>Update</td><td>New signals are added to the rules for an exclusive sequence.</td></tr><tr><td>Clarification</td><td>The requirements for AxCACHE in an exclusive access have been redefined to be easier to understand.</td></tr><tr><td>Read response</td><td>Clarification</td><td>For read responses where data is not required to be valid, the Manager might still sample the RDATA value so the Subordinate should not rely on the response to hide sensitive data.</td></tr><tr><td>Interface parity</td><td>Enhancement</td><td>The description regarding how to handle missing signals in CHK groups is enhanced to cover the case where either the input or output is missing.</td></tr><tr><td>Signal matrix</td><td>Correction</td><td>The ARDOMAIN and AWDOMAIN entries in the signal matrix are corrected to be dependent on the Shareable_Transactions property and marked as Configurable rather than Mandatory.</td></tr><tr><td>Cache stashing</td><td>Correction</td><td>&quot;AWSTASHLPIDEN must be driven to all zeros when AWSTASHLPIDEN is deasserted&quot; is corrected to: &quot;When AWSTASHLPIDEN is LOW, AWSTASHLPID is invalid and must</td></tr></table>

B4.2 Differences between Issue J and Issue K
<table><tr><td>Feature</td><td>Change</td><td>Detail</td></tr><tr><td>Memory Encryption Contexts (MEC)</td><td>New feature</td><td>The Memory Encryption Contexts (MEC) feature is added to the Realm Management Extension (RME).</td></tr><tr><td>MPAM extension</td><td>Enhancement</td><td>A new configuration option is defined for MPAM to support a wider PartID field.</td></tr><tr><td>MTE extension</td><td>Enhancement</td><td>A new configuration option is defined for MTE to support components which transport tags but do not support the Match operation.</td></tr><tr><td>Fixed_Burst_Disable</td><td>Enhancement</td><td>A new property is defined that allows components to not support a Burst type of FIXED.</td></tr><tr><td>Cache_Line_Size</td><td>Enhancement</td><td>A new property is defined to capture the cache line size of an interface.</td></tr><tr><td>WriteNoSnoopFull Transaction</td><td>Enhancement</td><td>A new WriteNoSnoopFull_Transaction property is defined to enable an interface to support WriteNoSnoopFull without having to support all transactions related to caching shareable lines.</td></tr><tr><td>Write channel dependency</td><td>Clarification</td><td>It is clarified that a Subordinate must not block acceptance of data-less write requests due to transactions with leading write data.</td></tr><tr><td>Length attribute</td><td>Clarification</td><td>It is clarified that Size x Length defines that maximum number of bytes in a transaction rather than the actual number in all cases.</td></tr><tr><td>Transaction equations</td><td>Correction</td><td>The Data_Bytes variable is corrected to be DATA_WIDTH/8.</td></tr><tr><td>Transaction pseudocode</td><td>Clarification</td><td>Variable names changed to align with earlier sections.</td></tr><tr><td>Ordering between Device and Normal Non-cacheable</td><td>Enhancement</td><td>A property Device_Normal_Independence is added to control whether Device and Normal Non-cacheable requests are required to be ordered against each other.</td></tr><tr><td>CACHE_Present</td><td>Clarification</td><td>It is clarified that the CACHE_Present property determines whether AxCACHE signals are present on an interface.</td></tr><tr><td>Cache stash property</td><td>Correction</td><td>In the paragraph text and Table A8.19, the Cache_Stash_Transactions property was incorrectly referred to as Stash_Transactions.</td></tr><tr><td>Max_Transaction_Bytes</td><td>Clarification</td><td>Clarification on the meaning of the Max_Transaction_Bytes property.</td></tr><tr><td>Write data strobes</td><td>Clarification</td><td>Clarification of the rules for WSTRB.</td></tr><tr><td>Read data interleaving</td><td>Clarification</td><td>It is clarified that read data transfers in Atomic transactions can be interleaved.</td></tr><tr><td>Modifiable transactions</td><td>Clarification</td><td>It is clarified that AxNSE must not be modified, along with AxPROT.</td></tr><tr><td>Exclusive accesses</td><td>Clarification</td><td>It is clarified that AWATOP must not be Match for exclusive writes.</td></tr><tr><td>PREFETCHED response</td><td>Change</td><td>The recommendation for PREFETCHED response is changed to be: within a cache line, the PREFETCHED response is used for all data transfers or no data transfers. This aligns better with the CHI</td></tr><tr><td>Caching shareable lines</td><td>Clarification</td><td>DataSource response. It is clarified that clean evictions of Shareable lines must not be written</td></tr><tr><td></td><td>Clarification</td><td>back to memory. In Table A8.8, CacheStash* is replaced with StashOnce*.</td></tr></table>

Continued on next page

Table B4.2 – Continued from previous page
<table><tr><td>Feature</td><td>Change</td><td>Detail</td></tr><tr><td>Memory Tagging</td><td>Clarification</td><td>A footnote is added to Table A12.13 to clarify that a WriteNoSnoop with tag Match must not be Exclusive.</td></tr><tr><td></td><td>Correction</td><td>In Table A12.12, the value for Tags match is corrected to be 0b11, not 0b10.</td></tr><tr><td>User Loopback signaling</td><td>Clarification</td><td>Clarification of the rules for LOOP_x_WIDTH properties.</td></tr><tr><td>MMUFLOW_Present property default</td><td>Correction</td><td>The default value for MMUFLOW_Present is corrected to be False to make it compatible with the default for the Untranslated_Transactions property.</td></tr><tr><td>StashTranslation and UnstashTranslation</td><td>Enhancement</td><td>StashTranslation and UnstashTranslation are enhanced to enable the stash or unstash of Granule Protection Table entries.</td></tr><tr><td rowspan="2">DVM messages</td><td>Clarification</td><td>It is clarified that the AC and CR channels are ordered.</td></tr><tr><td>Correction</td><td>The mapping for the 2nd part of a PICI message was incorrect in Table A15.22. ACADDR[11:4] should be PA[11:4].</td></tr><tr><td>Poison</td><td>Correction</td><td>The width of WPOISON and RPOISON is corrected to be ceil(DATA_WIDTH/64) rather than DATA_WIDTH/64.</td></tr><tr><td>Interface parity for CRTRACE</td><td>Correction</td><td>In Table A16.4, the enable signal for CRTRACECHK was indicated as ACVALID when it should be CRVALID.</td></tr><tr><td>Loopback check signal width</td><td>Change</td><td>In Table A16.4, the width of check signals for Loopback signals is changed from 1 to ceil(LOOP_x_WIDTH) to cover cases where the maximum recommendation of 8 for loopback width is exceeded.</td></tr><tr><td rowspan="2">ACE5-LiteDVM interface</td><td>Correction</td><td>The list of signals no longer supported in ACE5-LiteDVM is corrected to ACSNOOP, ACPROT and CRRESP</td></tr><tr><td>Correction</td><td>DVM_Message_Support must be Receiver for ACE5-LiteDVM interfaces. Therefore, the snoop channels are mandatory rather than optional.</td></tr><tr><td>BROADCAST* signals</td><td>Correction</td><td>In the signal matrix Table B2.2, the BROADCAST* signal presence was listed as dependent on a Broadcast_Signals property which was not defined. Presence conditions for these signals have now been removed.</td></tr><tr><td>Parity check signal matrix</td><td>Clarification</td><td>A matrix of parity check signals vs interface type is added for clarity.</td></tr><tr><td>Read Interleaving Disabled and AXI5-Lite</td><td>Correction</td><td>Read_Interleaving_Disabled was incorrectly constrained to True for AXI5-Lite interfaces, it should be False.</td></tr></table>

B4.3 Differences between Issue K and Issue L
<table><tr><td>Feature</td><td>Change</td><td>Detail</td></tr><tr><td>Credited transport</td><td>New feature</td><td>New credited transport option for all channels.</td></tr><tr><td>Arm Compression Technology</td><td>New feature</td><td>Added support for Arm Compression Technology.</td></tr><tr><td>Protection attributes</td><td>New feature</td><td>New options for signaling physical address space and other protection attributes.</td></tr><tr><td>RME - Granular Data Isolation</td><td>New feature</td><td>Added support for the GDI extension to RME.</td></tr><tr><td>Reset</td><td>Clarification</td><td>It is clarified that all signals that are required to be deasserted during reset must wait until at least the rising ACLK edge after ARESETn is HIGH.</td></tr><tr><td>Memory Encryption Contexts (MEC)</td><td>Correction</td><td>In Table B2.4, the MECID_WIDTH row has been corrected to say values can be 0,16 (two values) rather than 0..16 (range).</td></tr><tr><td></td><td>Clarification</td><td>It is clarified that the constraint for zero MECID only applies to requests where MECID is applicable.</td></tr><tr><td></td><td>Clarification</td><td>Removed misleading paragraph regarding mismatched widths of AxMECID.</td></tr><tr><td>Untranslated Transactions</td><td>Correction</td><td>The default value for AWMMUVALID and ARMMUVALID is corrected to be Ob1 rather than Ob0.</td></tr><tr><td></td><td>Correction</td><td>When the AxMMUVALID signals were added to the specification, it was expected that translated and untranslated transactions would use different AXI ID values, but these rules were missing from the</td></tr><tr><td></td><td>New feature</td><td>specification. New v4 option for Untranslated Transactions supports address translation with GDI and PCIe XT mode.</td></tr><tr><td>Transaction address calculation</td><td>Correction</td><td>The expression to determine the address states for a wrap transaction has been corrected to:  $\begin{array} { l } { { \tt A d c e s s \_ N \ = \ \tt A l i g n e d \_ A d d r \ + \ ( \tt ( N \mathrm { ~ - ~ } 1 ) \tt \ \star \ S i z e ) - \tt A d m e d \_ B d d r \ = } } \\ { { \tt ( S i z e \ \star \ L e n g t h ) } } \end{array}$ </td></tr><tr><td>Wrapping bursts</td><td>New feature</td><td>New property Wrap_CLS_Modifiable, used to determine whether</td></tr><tr><td>Exclusive accesses</td><td>Clarification</td><td>WRAP transactions must be cache line sized and Modifiable. It is clarified that mismatched attributes do not always cause a failure.</td></tr><tr><td>Atomic Transactions</td><td>Clarification</td><td>It is clarified that Atomic transactions must update the entire written location atomically.</td></tr><tr><td></td><td>Clarification</td><td>AtomicCompare transactions count as a Regular Transaction, even though the address might not be aligned to Size.</td></tr><tr><td></td><td>Clarification</td><td>Clarification of ID rules for Atomic transactions.</td></tr><tr><td>Memory Tagging Extension (MTE)</td><td>Clarification</td><td>If is clarified that transactions that carry tags must be physically addressed.</td></tr></table>

Continued on next page

Table B4.3 – Continued from previous page
<table><tr><td>Feature</td><td>Change</td><td>Detail</td></tr><tr><td>Cache line sized transactions</td><td>Change</td><td>The following Opcodes can now be Non-modifiable or Modifiable: WriteZero, WriteNoSnoopFull, WritePtlCMO, WriteFullCMO.</td></tr><tr><td>Caching Shareable lines</td><td>Correction</td><td>In Table A8.8, the entry for a Non-shareable CleanShared CMO has a footnote added that it must hit a Shareable Dirty line if RME_Support is True.</td></tr><tr><td></td><td>Enhancement</td><td>Added a statement regarding Outer Cacheable mode in attached CPUs.</td></tr><tr><td>Cache maintenance operations</td><td>Clarification</td><td>It is clarified that if the AxDOMAIN signals are missing, a CMO is assumed to be Non-shareable.</td></tr><tr><td></td><td>Correction</td><td>In the example of a Non-shareable WriteFullCMO with CleanInvalid, all in-line and peer caches must be cleaned and invalidated because the CMO is considered to be shareable</td></tr><tr><td></td><td>New feature</td><td>New cache maintenance operation, CleanInvalidStorage.</td></tr><tr><td>DVM Messages</td><td>Correction</td><td>In the ASID field section, the statement “For a 16-bit ASID agent sending a message to an 8-bit VMID agent&quot; has been corrected to “For a</td></tr><tr><td></td><td>Clarification</td><td>16-bit ASID agent sending a message to an 8-bit ASID agent&quot;. The use of the Range field in DVM TLBI messages is clarified.</td></tr><tr><td></td><td>Clarification</td><td>It is clarified that the range calculation uses the Translation Granule size in bytes, derived from TG.</td></tr><tr><td>DVM Complete transaction</td><td>Clarification</td><td>When DATA_WIDTH is 1024 and Max_Transaction_Bytes is 64 bytes, it is not possible that a DVM Complete can have ARSIZE equal to data channel width. It is clarified that for a DVM Complete, ARSIZE must be equal to the data channel width or Max_Transaction_Bytes if that is</td></tr><tr><td>DVM connection</td><td>Clarification</td><td>smaller than the data width. It is clarified that there might be a race between the assertion of SYSCOACK and ACVALID.</td></tr><tr><td>AWCACHE meanings</td><td>Correction</td><td>The meaning of the Bufferable bit (AWCACHE[0]) is corrected to say that the write response indicates that the data has reached its final destination only if AWCACHE[3:2] are both deasserted.</td></tr><tr><td>ACE-LiteACP cache line size</td><td>Clarification</td><td>It is clarified that the constraints on ACE5-LiteACP interfaces include a cache line size of 64 bytes.</td></tr><tr><td>Trace signals</td><td>Clarification</td><td>Added recommendation that a component that provides a response to a transaction with the Trace signal deasserted in the request provides a response with the Trace signal deasserted.</td></tr><tr><td>Loopback signals</td><td>Clarification</td><td>It is clarified that Loopback signals can be used on only read or only write channels.</td></tr><tr><td>Cache line sized and Regular</td><td>Clarification</td><td>ReadNoSnoop with MTE Fetch is added to the list of Opcodes that must be cache line sized and Regular.</td></tr><tr><td>ID constraints</td><td>Clarification</td><td>It is clarified that transactions with unique ID constraints are only constrained against other transactions on the same channels.</td></tr></table>

Part C Glossary

Chapter C1 Glossary

## Aligned

A data item stored at an address that is divisible by the highest power of 2 that divides into its size in bytes.   
Aligned halfwords, words and doublewords therefore have addresses that are divisible by 2, 4 and 8 respectively.

An aligned access is one where the address of the access is aligned to the size of each element of the access.

## At approximately the same time

Two events occur at approximately the same time if a remote observer might not be able to determine the order in which they occurred.

## Barrier

An operation that forces a defined ordering of other actions.

## Big-endian memory

Means that the most significant byte (MSB) of the data is stored in the memory location with the lowest address.

## Blocking

Describes an operation that prevents following actions from continuing until the operation completes.

## Branch prediction

Is where a processor selects a future execution path to fetch along. For example, after a branch instruction, the processor can choose to speculatively fetch either the instruction following the branch or the instruction at the branch target.

## Byte

An 8-bit data item.

## Cache

Any cache, buffer, or other storage structure in a caching Manager that can hold a copy of the data value for a particular address location.

## Cache hit

A memory access that can be processed at high speed because the data it addresses is already in the cache.

## Cache line

The basic unit of storage in a cache. Its size in words is always a power of two. A cache line must be aligned to the size of the cache line.

## Cache miss

A memory access that cannot be processed at high speed because the data it addresses is not in the cache.

## ceil()

A function that returns the lowest integer value that is equal to or greater than the input to the function.

## Coherent

Data accesses from a set of observers to a memory location are coherent accesses to that memory location by the members of the set of observers are consistent with there being a single total order of all writes to that memory location by all members of the set of observers.

## Component

A distinct functional unit that has at least one AMBA interface. Component can be used as a general term for Manager, Subordinate, peripheral, and interconnect components.

## Deprecated

Something that is present in the specification for backwards compatibility. Whenever possible you must avoid using deprecated features. These features might not be present in future versions of the specification.

## Downstream

An AXI transaction operates between a Manager component and one or more Subordinate components, and can pass through one or more intermediate components. At any intermediate component, for a given transaction, downstream means between that component and a destination Subordinate component, and includes the destination Subordinate component.

Downstream and upstream are defined relative to the transaction as a whole, not relative to individual data flows within the transaction.

## Downstream cache

A downstream cache is defined from the perspective of an initiating Manager. A downstream cache for a Manager is one that it accesses using the fundamental AXI transaction channels. An initiating Manager can allocate cache lines into a downstream cache.

## Endianness

An aspect of the system memory mapping.

## Full coherency

A fully coherent Manager can share data with other Managers and allocate that data in its local caches; it can snoop and be snooped.

## I/O coherency

An I/O coherent Manager can share data with other Managers but cannot allocate that data in its local caches; it can snoop but not be snooped.

## IMPLEMENTATION DEFINED

Means that the behavior is not defined by this specification, but must be defined and documented by individual implementations.

## in a timely manner

The protocol cannot define an absolute time within which something must occur. However, in a sufficiently idle system, it will make progress and complete without requiring any explicit action.

## Initiating Manager

A Manager that issues a transaction that starts a sequence of events. When describing a sequence of transactions, the term initiating Manager distinguishes the Manager that triggers the sequence of events from any snooped Manager that is accessed as a result of the action of the initiating Manager.

Initiating Manager is a temporal definition, meaning it applies at particular points in time, and typically is used when describing sequences of events. A Manager that is an initiating Manager for one sequence of events can be a snooped Manager for another sequence of events.

## Interconnect component

A component with more than one AMBA interface that connects one or more Manager components to one or more Subordinate components.

An interconnect component can be used to group together either:

• A set of Managers so that they appear as a single Manager interface.

• A set of Subordinates so that they appear as a single Subordinate interface.

## Little-endian memory

Means that the least significant byte (LSB) of the data is stored in the memory location with the lowest address.

## Load

The action of a Manager component reading the value held at a particular address location. For a processor, a load occurs as the result of executing a particular instruction. Whether the load results in the Manager issuing a read transaction depends on whether the accessed cache line is held in the local cache.

## Local cache

A local cache is defined from the perspective of an initiating Manager. A local cache is one that is internal to the Manager. Any access to the local cache is performed within the Manager.

## Main memory

The memory that holds the data value of an address location when no cached copies of that location exist. For any location, main memory can be out of date with respect to the cached copies of the location, but main memory is updated with the most recent data value when no cached copies exist.

Main memory can be referred to as memory when the context makes the intended meaning clear.

## Manager

An agent that initiates transactions.

## Manager component

A component that initiates transactions.

It is possible that a single component can act as both a Manager component and as a Subordinate component. For example, a Direct Memory Access (DMA) component can be a Manager component when it is initiating transactions to move data, and a Subordinate component when it is being programmed.

## Memory Encryption Contexts (MEC)

Memory Encryption Contexts are configurations of encryption that are associated with areas of memory, assigned by the MMU.

MEC is an extension to the Arm Realm Management Extension (RME). The RME system architecture requires that the Realm, Secure, and Root Physical Address Spaces (PAS) are encrypted. The encryption key or encryption context, used with each of these PASs is global within that PAS. For example, for the Realm PAS, all Realm memory uses the same encryption context. With MEC this concept is broadened, and for the Realm PAS specifically, each Realm is allowed to have a unique encryption context. This provides additional defense in depth to the isolation already provided in RME. MECIDs are identifying tags that are associated with different Memory Encryption Contexts.

## Memory Management Unit (MMU)

Provides detailed control of the part of a memory system that provides address translation. Most of the control is provided using translation tables that are held in memory, and define the attributes of different regions of the physical memory map.

## Memory Subordinate component

A Memory Subordinate component, or Memory Subordinate, is a Subordinate component with the following properties:

• A read of a byte from a Memory Subordinate returns the last value written to that byte location.

• A write to a byte location in a Memory Subordinate updates the value at that location to a new value that is obtained by subsequent reads.

• Reading a location multiple times has no side-effects on any other byte location.

• Reading or writing one byte location has no side-effects on any other byte location.

## Observer

A processor or other Manager component, such as a peripheral device, that can generate reads from or writes to memory.

## Page-based Hardware Attributes (PBHA)

Page Based Hardware Attributes (PBHA) is an optional, implementation defined feature. It allows software to set up to 4 bits in the translation tables, which are then propagated though the memory system with transactions, and can be used in the system to control system components. The meaning of the bits is specific to the system design.

## Peer cache

A peer cache is defined from the perspective of an initiating Manager. A peer cache for that Manager is one that is accessed using snoop channels. An initiating Manager cannot allocate cache lines into a peer cache.

## Peripheral Subordinate component

A Peripheral Subordinate component is also described as a Peripheral Subordinate. A Peripheral Subordinate typically has an IMPLEMENTATION DEFINED method of access that is described in the data sheet for the component. Any access that is not defined as permitted might cause the Peripheral Subordinate to fail, but must complete in a protocol-correct manner to prevent system deadlock. The protocol does not require continued correct operation of the peripheral.

In the context of the descriptions in this specification, Peripheral Subordinate is synonymous with peripheral, peripheral component, peripheral device, and device.

## PoS

Point of Serialization. The point through which all transactions to a given address must pass and the order in which the transactions are processed is determined.

## Prefetching

Prefetching refers to speculatively fetching instructions or data from the memory system. In particular, instruction prefetching is the process of fetching instructions from memory before the instructions that precede them, in simple sequential execution of the program, have finished executing. Prefetching an instruction does not mean that the instruction has to be executed.

In this specification, references to instruction or data fetching apply also to prefetching, unless the context explicitly indicates otherwise.

## RAZ/WI, Read-As-Zero, Writes Ignored

Hardware must implement the field as Read-as-Zero, and must ignore writes to the field. Software can rely on the field reading as all 0s, and on writes being ignored. This description can apply to a single bit that reads as 0, or to a field that reads as all 0s.

## Realm Management Extensions (RME)

The Realm Management Extension (RME) is an extension to the Armv9 A-profile architecture. RME is one component of the Arm Confidential Compute Architecture (Arm CCA). Together with the other components of the Arm CCA, RME enables support for dynamic, attestable and trusted execution environments (Realms) to be run on an Arm PE. RME adds two additional Security states (Root and Realm) and two physical address spaces (Root and Realm), and provides hardware-based isolation that allows execution contexts to run in different Securit states and share resources in the system.

## Snoop filter

A precise snoop filter that is able to track precisely the cache lines that might be allocated within a Manager.

## Snooped cache

A hardware-coherent cache on a snooped Manager. That is, it is a hardware-coherent cache that receives snoop transactions.

The term snooped cache is used in preference to the term snooped Manager when the sequence of events being described only involves the cache and does not involve any actions or events on the associated Manager.

## Snooped Manager

A caching Manager that receives snoop transactions.

Snooped Manager is a temporal definition, meaning it applies at particular points in time, and typically is used when describing sequences of events. A Manager that is a snooped Manager for one sequence of events can be an initiating Manager for another sequence of events.

## Speculative read

A transaction that a Manager issues when it might not need the transaction to be performed because it already has a copy of the accessed cache line in its local cache. Typically, a Manager issues a speculative read in parallel with a local cache lookup. This gives lower latency than looking in the local cache first, and then issuing a read transaction only if the required cache line is not found in the local cache.

## Store

The action of a Manager component changing the value held at a particular address location. For a processor, a store occurs as the result of executing a particular instruction. Whether the store results in the Manager issuing a read or write transaction depends on whether the accessed cache line is held in the local cache, and if it is in the local cache, the state it is in.

## Subordinate

An agent that receives and responds to requests.

## Subordinate component

A component that receives transactions and responds to them.

It is possible that a single component can act as both a Subordinate component and as a Manager component. For example, a Direct Memory Access (DMA) component can be a Subordinate component when it is being programmed and a Manager component when it is initiating transactions to move data.

## System Memory Management Unit (SMMU)

A system-level MMU. That is, a system component that provides address translation from one address space to another. An SMMU provides one or more of:

• virtual address (VA) to physical address (PA) translation.

• VA to intermediate physical address (IPA) translation.

• IPA to PA translation.

When using the Realm Management Extension (RME), an SMMU can also perform the Granule Protection Check.

## Transaction

An AXI Manager initiates an AXI transaction to communicate with an AXI Subordinate. Typically, the transaction requires information to be exchanged between the Manager and Subordinate on multiple channels. The complete set of required information exchanges form the AXI transaction.

## Translation Lookaside Buffer (TLB)

A memory structure containing the results of translation table walks. TLBs help to reduce the average cost of a memory access.

## Translation table

A table held in memory that defines the properties of memory areas of various sizes from 1KB.

## Translation table walk

The process of doing a full translation table lookup.

## Unaligned

An unaligned access is an access where the address of the access is not aligned to the size of an element of the access.

## Unaligned memory accesses

Are memory accesses that are not, or might not be, appropriately halfword-aligned, word-aligned, or doubleword-aligned.

## UNPREDICTABLE

In the AMBA AXI Architecture means that the behavior cannot be relied upon.

UNPREDICTABLE behavior must not be documented or promoted as having a defined effect.

## Upstream

An AXI transaction operates between a Manager component and one or more Subordinate components, and can pass through one or more intermediate components. At any intermediate component, for a given transaction, upstream means between that component and the originating Manager component, and includes the originating Manager component.

Downstream and upstream are defined relative to the transaction as a whole, not relative to individual data flows within the transaction.

## Write-Back cache

A cache in which when a cache hit occurs on a store access, the data is only written to the cache. Data in the cache can therefore be more up-to-date than data in main memory. Any such data is written back to main memory when the cache line is cleaned or re-allocated. Another common term for a Write-Back cache is a copy-back cache.

## Write-Through cache

A cache in which when a cache hit occurs on a store access, the data is written both to the cache and to main memory. This is normally done via a write buffer to avoid slowing down the processor.