---
title: AMBA AHB Protocol Specification (IHI0033C)
source: corpus/01_raw/specifications/amba/IHI0033C_AMBA_AHB_spec.pdf
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
spec_id: SPEC-STD-AMBA-AHB-C
spec_org: ARM
spec_revision: IHI0033C
status: approved
---
AMBA<sup>®</sup> AHB

Protocol Specification

Copyright © 2001, 2006, 2010, 2015, 2021 Arm Limited or its affiliates. All rights reserved.

Release Information

Change history
<table><tr><td>Date</td><td>Issue</td><td>Confidentiality</td><td>Change</td></tr><tr><td>06 June 2006</td><td>A</td><td>Non-Confidential</td><td>First release for v1.0</td></tr><tr><td>25 June 2015</td><td>B.a</td><td>Confidential</td><td>Update for AMBA 5 AHB Protocol Specification</td></tr><tr><td>30 October 2015</td><td>B.b</td><td>Non-Confidential</td><td>Confidential to Non-Confidential Release</td></tr><tr><td>15 September 2021</td><td>C</td><td>Non-confidential</td><td>New features and enhancements: Signal width properties, Write strobes, User signaling update, Signal validity rules, and interface protection using parity. Regularized terminology to be Manager and</td></tr></table>

## Proprietary Notice

This document is NON-CONFIDENTIAL and any use by you is subject to the terms of this notice and the Arm AMBA Specification Licence set about below.

This document is protected by copyright and other related rights and the practice or implementation of the information contained in this document may be protected by one or more patents or pending patent applications. No part of this document may be reproduced in any form by any means without the express prior written permission of Arm. No license, express or implied, b estoppel or otherwise to any intellectual property rights is granted by this document unless specifically stated.

Your access to the information in this document is conditional upon your acceptance that you will not use or permit others to use the information for the purposes of determining whether implementations infringe any third party patents.

THIS DOCUMENT IS PROVIDED "AS IS". ARM PROVIDES NO REPRESENTATIONS AND NO WARRANTIES, EXPRESS, IMPLIED OR STATUTORY, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTIES OF MERCHANTABILITY, SATISFACTORY QUALITY, NON-INFRINGEMENT OR FITNESS FOR A PARTICULAR PURPOSE WITH RESPECT TO THE DOCUMENT. For the avoidance of doubt, Arm makes no representation with respect to, and has undertaken no analysis to identify or understand the scope and content of, patents, copyrights, trade secrets, or other rights.

This document may include technical inaccuracies or typographical errors.

TO THE EXTENT NOT PROHIBITED BY LAW, IN NO EVENT WILL ARM BE LIABLE FOR ANY DAMAGES, INCLUDING WITHOUT LIMITATION ANY DIRECT, INDIRECT, SPECIAL, INCIDENTAL, PUNITIVE, OR CONSEQUENTIAL DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY, ARISING OUT OF ANY USE OF THIS DOCUMENT, EVEN IF ARM HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

This document consists solely of commercial items. You shall be responsible for ensuring that any use, duplication or disclosure of this document complies fully with any relevant export laws and regulations to assure that this document or any portion thereof is not exported, directly or indirectly, in violation of such export laws. Use of the word "partner" in reference to Arm's customers is not intended to create or refer to any partnership relationship with any other company. Arm may make changes to this document at any time and without notice.

This document may be translated into other languages for convenience, and you agree that if there is any conflict between the English version of this document and any translation, the terms of the English version of the Agreement shall prevail.

The Arm corporate logo and words marked with <sup>®</sup> or <sup>™</sup> are registered trademarks or trademarks of Arm Limited (or its subsidiaries) in the US and/or elsewhere. All rights reserved. Other brands and names mentioned in this document may be the trademarks of their respective owners. Please follow Arm's trademark usage guidelines at http://www.arm.com/company/policies/trademarks.

Copyright © 2001, 2006, 2010, 2015, 2021 Arm Limited (or its affiliates). All rights reserved. Arm Limited. Company 02557590 registered in England.   
110 Fulbourn Road, Cambridge, England CB1 9NJ.   
LES-PRE-21451 version 2.2

## AMBA SPECIFICATION LICENCE

THIS END USER LICENCE AGREEMENT ("LICENCE") IS A LEGAL AGREEMENT BETWEEN YOU (EITHER A SINGLE INDIVIDUAL, OR SINGLE LEGAL ENTITY) AND ARM LIMITED ("ARM") FOR THE USE OF ARM'S INTELLECTUAL PROPERTY (INCLUDING, WITHOUT LIMITATION, ANY COPYRIGHT) IN THE RELEVANT AMBA SPECIFICATION ACCOMPANYING THIS LICENCE. ARM LICENSES THE RELEVANT AMBA SPECIFICATION TO YOU ON CONDITION THAT YOU ACCEPT ALL OF THE TERMS IN THIS LICENCE. BY CLICKING "I AGREE" OR OTHERWISE USING OR COPYING THE RELEVANT AMBA SPECIFICATION YOU INDICATE THAT YOU AGREE TO BE BOUND BY ALL THE TERMS OF THIS LICENCE.

"LICENSEE" means You and your Subsidiaries.

"Subsidiary" means, if You are a single entity, any company the majority of whose voting shares is now or hereafter owned or controlled, directly or indirectly, by You. A company shall be a Subsidiary only for the period during which such control exists.

1. Subject to the provisions of Clauses 2, 3 and 4, Arm hereby grants to LICENSEE a perpetual, non-exclusive, non-transferable, royalty free, worldwide licence to:

(i) use and copy the relevant AMBA Specification for the purpose of developing and having developed products that comply with the relevant AMBA Specification;

(ii) manufacture and have manufactured products which either: (a) have been created by or for LICENSEE under the licence granted in Clause 1(i); or (b) incorporate a product(s) which has been created by a third party(s) under a licence granted by Arm in Clause 1(i) of such third party's AMBA Specification Licence; and

(iii) offer to sell, sell, supply or otherwise distribute products which have either been (a) created by or for LICENSEE under the licence granted in Clause 1(i); or (b) manufactured by or for LICENSEE under the licence granted in Clause 1(ii).

2. LICENSEE hereby agrees that the licence granted in Clause 1 is subject to the following restrictions:

(i) where a product created under Clause 1(i) is an integrated circuit which includes a CPU then either: (a) such CPU shall only be manufactured under licence from Arm; or (b) such CPU is neither substantially compliant with nor marketed as being compliant with the Arm instruction sets licensed by Arm from time to time;

(ii) the licences granted in Clause 1(iii) shall not extend to any portion or function of a product that is not itself compliant with part of the relevant AMBA Specification; and

(iii) no right is granted to LICENSEE to sublicense the rights granted to LICENSEE under this Agreement.

3. Except as specifically licensed in accordance with Clause 1, LICENSEE acquires no right, title or interest in any Arm technology or any intellectual property embodied therein. In no event shall the licences granted in accordance with Clause 1 be construed as granting LICENSEE, expressly or by implication, estoppel or otherwise, a licence to use any Arm technology except the relevant AMBA Specification.

4. THE RELEVANT AMBA SPECIFICATION IS PROVIDED "AS IS" WITH NO REPRESENTATION OR WARRANTIES EXPRESS, IMPLIED OR STATUTORY, INCLUDING BUT NOT LIMITED TO ANY WARRANTY OF SATISFACTORY QUALITY, MERCHANTABILITY, NON-INFRINGEMENT OR FITNESS FOR A PARTICULAR PURPOSE, OR THAT ANY USE OR IMPLEMENTATION OF SUCH ARM TECHNOLOGY WILL NOT INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADE SECRETS OR OTHER INTELLECTUAL PROPERTY RIGHTS.

5. NOTWITHSTANDING ANYTHING TO THE CONTRARY CONTAINED IN THIS AGREEMENT, TO THE FULLEST EXTENT PETMITTED BY LAW, THE MAXIMUM LIABILITY OF ARM IN AGGREGATE FOR ALL CLAIMS MADE AGAINST ARM, IN CONTRACT, TORT OR OTHERWISE, IN CONNECTION WITH THE SUBJECT MATTER OF THIS AGREEMENT (INCLUDING WITHOUT LIMITATION (I) LICENSEE'S USE OF THE ARM TECHNOLOGY; AND (II) THE IMPLEMENTATION OF THE ARM TECHNOLOGY IN ANY PRODUCT CREATED BY LICENSEE UNDER THIS AGREEMENT) SHALL NOT EXCEED THE FEES PAID (IF ANY) BY LICENSEE TO ARM UNDER THIS AGREEMENT. THE EXISTENCE OF MORE THAN ONE CLAIM OR SUIT WILL NOT ENLARGE OR EXTEND THE LIMIT. LICENSEE RELEASES ARM FROM ALL OBLIGATIONS, LIABILITY, CLAIMS OR DEMANDS IN EXCESS OF THIS LIMITATION.

6. No licence, express, implied or otherwise, is granted to LICENSEE, under the provisions of Clause 1, to use the Arm tradename, or AMBA trademark in connection with the relevant AMBA Specification or any products based thereon. Nothing in Clause 1 shall be construed as authority for LICENSEE to make any representations on behalf of Arm in respect of the relevant AMBA Specification.

7. This Licence shall remain in force until terminated by you or by Arm. Without prejudice to any of its other rights if LICENSEE is in breach of any of the terms and conditions of this Licence then Arm may terminate this Licence immediately upon giving written notice to You. You may terminate this Licence at any time. Upon expiry or termination of this Licence by You or by Arm LICENSEE shall stop using the relevant AMBA Specification and destroy all copies of the relevant AMBA Specification in your possession together with all documentation and related materials. Upon expiry or termination of this Licence, the provisions of clauses 6 and 7 shall survive.

8. The validity, construction and performance of this Agreement shall be governed by English Law.

## Confidentiality Status

This document is Non-Confidential. The right to use, copy and disclose this document may be subject to license restrictions in accordance with the terms of the agreement entered into by Arm and the party that Arm delivered this document to.

## Product Status

The information in this document is final, that is for a developed product.

## Web Address

http://www.arm.com

## Contents AMBA AHB Protocol Specification

Preface   
About this specification viii   
Feedback xii   
Chapter 1 Introduction   
1.1 About the protocol . 1-14   
1.2 AMBA AHB revisions 1-17   
1.3 Operation 1-18   
Chapter 2 Signal Descriptions   
2.1 Global signals . 2-20   
2.2 Manager signals 2-21   
2.3 Subordinate signals 2-23   
2.4 Decoder signals 2-24   
2.5 Multiplexor signals 2-25   
Chapter 3 Transfers   
3.1 Basic transfers 3-28   
3.2 Transfer types 3-30   
3.3 Locked transfers 3-32   
3.4 Transfer size 3-33   
3.5 Write strobes 3-34   
3.6 Burst operation 3-35   
3.7 Waited transfers 3-40   
3.8 Protection control 3-45   
3.9 Memory types . 3-46   
3.10 Secure transfers 3-51   
Chapter 4 Bus Interconnection   
4.1 Interconnect 4-54   
4.2 Address decoding 4-55   
4.3 Read data and response multiplexor 4-56   
4.4 Interconnect with AHB interfaces 4-57   
Chapter 5 Subordinate Response Signaling   
5.1 Subordinate transfer responses 5-60   
Chapter 6 Data Buses   
6.1 Data buses 6-64   
6.2 Endianness 6-65   
6.3 Data bus width 6-69   
Chapter 7 Clock and Reset   
7.1 Clock and reset requirements 7-72   
Chapter 8 Signal validity   
8.1 Signal validity in AMBA AHB 8-74   
8.2 Signal validity rules 8-75   
Chapter 9 Atomicity   
9.1 Single-copy atomicity size 9-78   
9.2 Multi-copy atomicity 9-79   
Chapter 10 Exclusive Transfers   
10.1 Introduction 10-82   
10.2 Exclusive Access Monitor 10-83   
10.3 Exclusive access signaling 10-84   
10.4 Exclusive Transfer restrictions 10-85   
Chapter 11 User Signaling   
11.1 User signal description 11-88   
11.2 User signal interconnect recommendations 11-89   
Chapter 12 Interface protection using parity   
12.1 Parity use in AMBA AHB 12-92   
12.2 Configuration of interface protection 12-93   
12.3 Byte parity check signals 12-94   
12.4 Error detection behavior 12-95   
12.5 Parity check signals 12-96   
Appendix A Signal matrix   
A.1 Signal matrix . A-98   
A.2 Check signal matrix A-100   
Appendix B Revisions

## Glossary

## Preface

This preface introduces the AMBA AHB Protocol Specification. It contains the following sections:

About this specification on page viii

Feedback on page xii

## About this specification

This specification describes the AMBA AHB protocol.

## Intended audience

This specification is written for hardware and software engineers who want to become familiar with the AMBA AHB protocol and design systems and modules that are compatible with the AMBA AHB protocol.

## Using this specification

This specification is organized into the following chapters:

Chapter 1 Introduction Read this chapter for an overview of the AMBA AHB protocol.

Chapter 2 Signal Descriptions Read this chapter for descriptions of the signals.

Chapter 3 Transfers

Read this chapter for information about the different types of transfer initiated by a Manager.

Chapter 4 Bus Interconnection Read this chapter for information about the interconnect logic required for AMBA AHB systems.

Chapter 5 Subordinate Response Signaling Read this chapter for information about the Subordinate response signaling.

Read this chapter for information about the read and write data buses and how to interface to different data bus widths.

Chapter 7 Clock and Reset Read this chapter for information about the clock and reset signals.

Chapter 8 Signal validity Read this chapter for information on the rules when signals must be valid.

Chapter 9 Atomicity Read this chapter for information on the atomic properties that this specification defines.

Chapter 10 Exclusive Transfers Read this chapter for information about Exclusive transfers, the Exclusive Access Monitor, and the additional signals associated with Exclusive transfers.

Chapter 11 User Signaling Read this chapter for a description of the set of optional user defined signals, on each channel, called User signals.

Chapter 12 Interface protection using parity Read this chapter for a description of interface protection using parity and the parity check signals used in AMBA AHB.

This appendix defines the required and optional signals for the AMBA AHB interfaces.

## Appendix B Revisions

Read this appendix for a description of the technical changes between released issues of this specification.

Read the Glossary for definitions of terms used in this specification.

## Conventions

This section describes the conventions that this specification uses:

Typographical

Timing diagrams

• Signals on page xi

## Typographical

The typographical conventions are:

italic Highlights important notes, introduces special terminology, and denotes internal cross-references and citations.

bold Denotes signal names, and is used for terms in descriptive lists, where appropriate.

monospace Used for assembler syntax descriptions, pseudocode, and source code examples. Also used in the main text for instruction mnemonics and for references to other items appearing in assembler syntax descriptions, pseudocode, and source code examples.

SMALL CAPITALS Used for a few terms that have specific technical meanings.

## Timing diagrams

The components used in timing diagrams are explained in the figure Key to timing diagram conventions. Variations have clear labels, when they occur. Do not assume any timing information that is not explicit in the diagrams.

Shaded bus and signal areas are undefined, so the bus or signal can assume any value within the shaded area at that time. The actual level is unimportant and does not affect normal operation.

Clock

HIGH to LOW

Transient

HIGH/LOW to HIGH

Bus stable

Bus to high impedance

Bus change

High impedance to stable bus

## Key to timing diagram conventions

Timing diagrams sometimes show single-bit signals as HIGH and LOW at the same time and they look similar to the bus change shown in Key to timing diagram conventions. If a timing diagram shows a single-bit signal in this way, then its value does not affect the accompanying description.

## Signals

The signal conventions are:

Signal level

The level of an asserted signal depends on whether the signal is active-HIGH or active-LOW. Asserted means:

HIGH for active-HIGH signals.

LOW for active-LOW signals.

Lower-case n At the start or end of a signal name denotes an active-LOW signal.

Prefix H Denotes an Advanced High-performance Bus (AHB) signal.

Prefix P Denotes an Advanced Peripheral Bus (APB) signal.

## Numbers

Numbers are normally written in decimal. Binary numbers are preceded by 0b, and hexadecimal numbers by 0x.   
Both are written in a monospace font.

## Additional reading

This section lists relevant publications from Arm.

See Arm Developer, https://developer.arm.com/docs, for access to Arm documentation.

## Arm publications

ARM<sup>®</sup> AMBA<sup>®</sup> APB Protocol Specification (ARM IHI 0024)

ARM<sup>®</sup> AMBA<sup>®</sup> AXI and ACE Protocol Specification (ARM IHI 0022)

Multi-layer AHB Technical Overview (ARM DVI 0045)

## Feedback

Arm welcomes feedback on its documentation.

## Feedback on this specification

If you have any comments on this specification, send an e-mail to errata@arm.com. Give:

The title, AMBA<sup>®</sup> AHB Protocol Specification.

The number, ARM IHI 0033C.

The page numbers to which your comments apply.

• A concise explanation of your comments.

Arm also welcomes general suggestions for additions and improvements.

## Progressive terminology commitment

Arm values inclusive communities. Arm recognizes that we and our industry have used terms that can be offensive. Arm strives to lead the industry and create change. Previous issues of this document included terms that can be offensive. We have replaced these terms.

If you find offensive terms in this document, please contact terms@arm.com.

## Chapter 1 Introduction

This chapter provides an overview of the AMBA AHB protocol. It contains the following sections:

About the protocol on page 1-14

AMBA AHB revisions on page 1-17

Operation on page 1-18

Note

For illustrative purposes, a 32-bit data bus is used in this specification. Additional data bus widths are permitted, as Data bus width on page 6-69 shows.

## 1.1 About the protocol

AMBA AHB is a bus interface suitable for high-performance synthesizable designs.

It defines the interface between components, such as Managers, interconnects, and Subordinates.

AMBA AHB implements the features required for high-performance, high clock frequency systems including:

Burst transfers

Single clock-edge operation

Non-tristate implementation

Configurable data bus widths

Configurable address bus widths

The most common AHB Subordinates are internal memory devices, external memory interfaces, and high-bandwidth peripherals. Although low-bandwidth peripherals can be included as AHB Subordinates, for system performance reasons, they typically reside on the AMBA Advanced Peripheral Bus (APB). Bridging between the higher performance AHB and APB is done using an AHB Subordinate, known as an APB bridge.

Figure 1-1 shows a single Manager AHB system design with the AHB Manager and three AHB Subordinates. The bus interconnect logic consists of one address decoder and a Subordinate-to-Manager multiplexor. The decoder monitors the address from the Manager during the address phase so that the appropriate Subordinate is selected during the data phase of a transfer. The multiplexor routes the corresponding Subordinate output data back to the Manager.

AHB also supports multi-Manager designs by the use of an interconnect component that provides arbitration and routing signals from different Managers to the appropriate Subordinates.

Note

Figure 1-1 shows only the main address and data buses and typical data routing. Not all signals are shown.

![](images/a643a3d7c340b3e668ec3e434e0c9c546a8465f8d50efe881bf955057cba08b0.jpg)  
Figure 1-1 AHB block diagram

The main component types of an AHB system are described in:

Manager on page 1-15

Subordinate on page 1-15

Interconnect on page 1-16

## 1.1.1 Manager

A Manager provides address and control information to initiate read and write operations. Figure 1-2 shows a Manager interface.

Note

The diagram in Figure 1-2 does not include the additional signals defined in AHB5.

![](images/10c2e7048866ddaed33e1525fa662ac8b7ff52899b235b0903a7bfaa2bbd408f.jpg)  
Figure 1-2 Manager interface

## 1.1.2 Subordinate

A Subordinate responds to transfers initiated by Managers in the system. The Subordinate uses the HSELx select signal from the decoder to control when it responds to a bus transfer.

The Subordinate signals back to the Manager:

The completion or extension of the bus transfer.

The success or failure of the bus transfer.

Figure 1-3 shows a Subordinate interface.

Note

The diagram in Figure 1-3 does not include the additional signals defined in AHB5.

![](images/4728c0775a49d7691ca4b068188646ae43628ac398ee4d9889b05c95d1c47ccf.jpg)  
Figure 1-3 Subordinate interface

## 1.1.3 Interconnect

An interconnect component provides the connection between Managers and Subordinates in a system.

A single Manager system only requires the use of a Decoder and Multiplexor, as described in the following sections.

A multi-Manager system requires the use of an interconnect that provides arbitration and the routing of signals from different Managers to the appropriate Subordinates. This routing is required for address, control, and write data signaling. Further details of the different approaches used for multi-Manager systems, such as single layer or multi-layer interconnects, are not provided within this specification.

See Multi-layer AHB Technical Overview (ARM DVI 0045) for more information about implementing a multi-layer AHB-Lite interconnect.

## Decoder

This component decodes the address of each transfer and provides a select signal for the Subordinate that is involved in the transfer. It also provides a control signal to the multiplexor.

A single centralized decoder is required in all implementations that use two or more Subordinates. See Address decoding on page 4-55 for more information.

## Multiplexor

A Subordinate-to-Manager multiplexor is required to multiplex the read data bus and response signals from the Subordinates to the Manager. The decoder provides control for the multiplexor.

A single centralized multiplexor is required in all implementations that use two or more Subordinates. See Read data and response multiplexor on page 4-56 for more information.

## 1.2 AMBA AHB revisions

Issue A of this specification describes the AHB-Lite interface. Issue B introduced AHB5, which is based on AHB-Lite with some added capabilities.

This issue of the document is Issue C and adds the following topics:

Signal width properties. See Manager signals on page 2-21.

Write strobes. See Write strobes on page 3-34.

User signaling update. See User signal description on page 11-88.

Interface protection using parity. See Parity use in AMBA AHB on page 12-92.

In this specification, the term AHB is used to refer to both AHB-Lite and AHB5.

Unless stated, signals are common to both AHB-Lite and AHB5.

## 1.3 Operation

The Manager starts a transfer by driving the address and control signals. These signals provide information about the address, direction, width of the transfer, and indicate if the transfer forms part of a burst. Transfers can be:

Single.

Incrementing bursts that do not wrap at address boundaries.

Wrapping bursts that wrap at particular address boundaries.

The write data bus moves data from the Manager to a Subordinate, and the read data bus moves data from a Subordinate to the Manager.

Every transfer consists of:

Address phase One address and control cycle.

Data phase One or more cycles for the data.

A Subordinate cannot request that the address phase is extended and therefore all Subordinates must be capable of sampling the address during this time. However, a Subordinate can request that the Manager extends the data phase by using HREADY. This signal, when LOW, causes wait states to be inserted into the transfer and enables the Subordinate to have extra time to provide or sample data.

The Subordinate uses HRESP to indicate the success or failure of a transfer.

## Chapter 2 Signal Descriptions

This chapter describes the protocol signals. It contains the following sections:

Global signals on page 2-20

Manager signals on page 2-21

Subordinate signals on page 2-23

Decoder signals on page 2-24

Multiplexor signals on page 2-25

Note

All AHB-Lite and AHB5 signals are prefixed with the letter H to differentiate them from other similarly named signals in a system design.

Some signals can have a variety of widths, described by a property. These properties can be used to describe a fixed configuration or to control the configuration of an interface. Signals with a width of 0 are not present on the interface.

## 2.1 Global signals

Table 2-1 lists the protocol global signals.  
Table 2-1 Global signals
<table><tr><td>Name</td><td>Source</td><td>Width</td><td>Description</td></tr><tr><td>HCLK</td><td>Clock source</td><td>1</td><td>The bus clock times all bus transfers. All signal timings are related to the rising edge of HCLK.</td></tr><tr><td>HRESETn</td><td>Reset controller</td><td>1</td><td>See Clock on page 7-72. The bus reset signal is active LOW and resets the</td></tr><tr><td></td><td></td><td></td><td>system and the bus. This is the only active LOW signal. See Reset on page 7-72.</td></tr></table>

## 2.2 Manager signals

Table 2-2 lists the protocol signals generated by a Manager. A signal width property defines the width of a signal. For example, ADDR\_WIDTH defines the width of HADDR. The properties can be used to describe a fixed configuration or to control the configuration of an interface.

Table 2-2 Manager signals
<table><tr><td>Name</td><td>Destination</td><td>Width</td><td>Description</td></tr><tr><td>HADDR</td><td>Subordinate and decoder</td><td>ADDR WIDTH</td><td>The byte address of the transfer. ADDRWIDTH is recommended to be between 10 and 64. In the issues A and B of this specification, the address width was fixed at 32.</td></tr><tr><td>HBURST</td><td>Subordinate</td><td>HBURST WIDTH</td><td>Indicates how many transfers are in the burst and how the address increments. HBURST WIDTH must be 0 or 3. See Burst operation on page 3-35.</td></tr><tr><td>HMASTLOCK</td><td>Subordinate</td><td>1</td><td>Indicates that the current transfer is part of a locked sequence. It has the same timing as the address and control signals. See Locked transfers on page 3-32.</td></tr><tr><td>HPROT</td><td>Subordinate</td><td>HPROT WIDTH</td><td>Protection control signal, which provides information about the access type. HPROT_WIDTH must be 0, 4, or 7, depending on the Extended_Memory_Types property. See Protection control on page 3-45.</td></tr><tr><td>HSIZE</td><td>Subordinate</td><td>3</td><td>See Memory types on page 3-46. Indicates the size of the transfer. See Transfer size on page 3-33.</td></tr><tr><td>HNONSEC</td><td>Subordinate and decoder 1</td><td></td><td>Indicates whether the transfer is Non-secure or Secure. This signal is supported if the AHB5 Secure Transfers property is True.</td></tr><tr><td>HEXCL</td><td>Exclusive Access Monitor</td><td>1</td><td>See Secure transfers on page 3-51. Indicates whether the transfer is part of an Exclusive Access sequence. This signal is supported if the AHB5 Exclusive Transfers property is True.</td></tr><tr><td>HMASTER</td><td>Exclusive Access Monitor and Subordinate</td><td>HMASTER WIDTH</td><td>See Exclusive access signaling on page 10-84. Manager identifier. Generated by a Manager if it has multiple Exclusive capable threads. Modified by an interconnect to ensure each Manager is uniquely identified.</td></tr><tr><td>HTRANS</td><td>Subordinate</td><td>2</td><td>Indicates the transfer type. This can be: IDLE BUSY NONSEQUENTIAL SEQUENTIAL.</td></tr><tr><td>HWDATA</td><td>Subordinate</td><td>DATA WIDTH</td><td>See Transfer types on page 3-30. Transfers data from the Manager to the Subordinates during write operations. DATA WIDTH can be 8, 16, 32, 64, 128, 256, 512, or 1024. However, any value smaller than 32 or larger than 256 is not recommended. See Data buses on page 6-64.</td></tr><tr><td>HWSTRB</td><td>Subordinate</td><td>DATA WIDTH/8</td><td>Write strobes. Deasserted to indicate when active write data byte lanes do not contain valid data. There is 1 bit for each 8 bits of HWDATA. HWSTRB[n] corresponds to HWDATA[(8n)+7:(8n)]. HWSTRB is a data-phase signal and has the same validity rules as HWDATA.</td></tr><tr><td>HWRITE</td><td>Subordinate</td><td>1</td><td>See Write strobes on page 3-34. Indicates the transfer direction. When HIGH this signal indicates a write transfer and when LOW a read transfer. It has the same timing as the address signals, however, it must remain constant throughout a burst transfer. See Basic transfers on page 3-28.</td></tr></table>

## 2.3 Subordinate signals

Table 2-3 lists the protocol signals generated by a Subordinate.  
Table 2-3 Subordinate signals
<table><tr><td>Name</td><td>Destination</td><td>Width</td><td>Description</td></tr><tr><td>HRDATA</td><td>Multiplexor</td><td>DATA WIDTH</td><td>During read operations, the read data bus transfers data from the selected Subordinate to the multiplexor. The multiplexor then transfers the data to the Manager. DATA WIDTH can be 8, 16, 32, 64, 128, 256, 512, or 1024. However, any value smaller than 32 or larger than 256 is not recommended.</td></tr><tr><td>HREADYOUT</td><td>Multiplexor</td><td>1</td><td>When HIGH, the HREADYOUT signal indicates that a transfer has finished on the bus. This signal can be driven LOW to extend a transfer. See Read data and response multiplexor on</td></tr><tr><td>HRESP</td><td>Multiplexor</td><td>1</td><td>page 4-56. The transfer response provides the Manager with additional information on the status of a transfer. When LOW, the HRESP signal indicates that the transfer status is OKAY. When HIGH, the HRESP signal indicates that the transfer status is ERROR. See Subordinate transfer responses on</td></tr><tr><td></td><td></td><td>1</td><td>Exclusive Okay. Indicates the success or failure of an Exclusive Transfer. This signal is supported if the AHB5 Exclusive Transfers property is True. See Exclusive access signaling on page 10-84.</td></tr></table>

## 2.4 Decoder signals

Table 2-4 lists the protocol signals generated by the decoder.  
Table 2-4 Decoder signals
<table><tr><td>Name</td><td>Destination</td><td>Width</td><td>Description</td></tr><tr><td>HSELxª</td><td>Subordinate</td><td>1</td><td>Each Subordinate has its own select signal HSELx and this signal indicates that the current transfer is intended for the selected Subordinate. When the Subordinate is initially selected, it must also monitor the status of HREADY to ensure that the previous bus transfer has completed,</td></tr><tr><td></td><td></td><td></td><td>before it responds to the current transfer. When a Subordinate is selected for a non-IDLE transfer, HSELx must be</td></tr><tr><td></td><td></td><td></td><td>asserted in the same cycle as the address and other control signals. HSELx can be asserted or deasserted for IDLE transfers. See Address decoding on page 4-55.</td></tr></table>

a. The letter x used in HSELx must be changed to a unique identifier for each Subordinate in a system. For example, HSEL\_S1, HSEL\_S2, and HSEL\_Memory.

Usually the decoder also provides the multiplexor with the HSELx signals, or a signal or bus derived from the HSELx signals, to enable the multiplexor to route the appropriate signals, from the selected Subordinate to the Manager. It is important that these additional multiplexor control signals are retimed to the data phase.

## 2.5 Multiplexor signals

Table 2-5 lists the protocol signals generated by the multiplexor.  
Table 2-5 Multiplexor signals
<table><tr><td>Name</td><td>Destination</td><td>Width</td><td>Description</td></tr><tr><td>HRDATA</td><td>Manager</td><td>DATA_WIDTH</td><td>Read data bus, selected by the decoder.a</td></tr><tr><td>HREADY</td><td>Manager and Subordinate</td><td>1</td><td>When HIGH, the HREADY signal indicates to the Manager and all Subordinates, that the previous transfer is complete. See Read data and response multiplexor on</td></tr><tr><td>HRESP</td><td>Manager</td><td>1</td><td>page 4-56. Transfer response, selected by the decoder.a</td></tr><tr><td>HEXOKAY</td><td>Manager</td><td>1</td><td>Exclusive okay, selected by the decoder.a</td></tr></table>

a. Because the HRDATA, HRESP, and HEXOKAY signals pass through the multiplexor and retain the same signal naming, the full signal descriptions for these three signals are provided in Table 2-3 on page 2-23.

2 Signal Descriptions

2.5 Multiplexor signals

## Chapter 3 Transfers

This chapter describes read and write transfers. It contains the following sections:

Basic transfers on page 3-28

Transfer types on page 3-30

Locked transfers on page 3-32

Transfer size on page 3-33

Write strobes on page 3-34

Burst operation on page 3-35

Waited transfers on page 3-40

Protection control on page 3-45

Memory types on page 3-46

Secure transfers on page 3-51

## 3.1 Basic transfers

A transfer consists of two phases:

Address Lasts for a single HCLK cycle unless it is extended by the previous bus transfer.

Data Might require several HCLK cycles. Use the HREADY signal to control the number of clock cycles required to complete the transfer.

HWRITE controls the direction of data transfer to or from the Manager. Therefore, when:

HWRITE is HIGH, it indicates a write transfer and the Manager broadcasts data on the write data bus, HWDATA.

HWRITE is LOW, a read transfer is performed, and the Subordinate must generate the data on the read data bus, HRDATA.

The simplest transfer is one with no wait states, so the transfer consists of one address cycle and one data cycle.   
Figure 3-1 shows a simple read transfer and Figure 3-2 shows a simple write transfer.

![](images/dec4548a649ed9c6fb3e150ed587c45cafd2d122b8e58292fb98bc5911ba2603.jpg)  
Figure 3-1 Read transfer

![](images/ee7b11cd24ac5e47a7b4f5b9c7de3744af41e451898ee4cc8e7dddb8e3cbe689.jpg)  
Figure 3-2 Write transfer

In a simple transfer with no wait states:

1. The Manager drives the address and control signals onto the bus after the rising edge of HCLK.

2. The Subordinate then samples the address and control information on the next rising edge of HCLK.

3. After the Subordinate has sampled the address and control it can start to drive the appropriate HREADYOUT response. This response is sampled by the Manager on the third rising edge of HCLK.

This simple example demonstrates how the address and data phases of the transfer occur during different clock cycles. The address phase of any transfer occurs during the data phase of the previous transfer. This overlapping of address and data is fundamental to the pipelined nature of the bus and enables high-performance operation while still providing adequate time for a Subordinate to provide the response to a transfer.

A Subordinate can insert wait states into any transfer to enable additional time for completion. Each Subordinate has an HREADYOUT signal that it drives during the data phase of a transfer. The interconnect is responsible for combining the HREADYOUT signals from all Subordinates to generate a single HREADY signal that is used to control the overall progress.

Figure 3-3 shows a read transfer with two wait states.  
![](images/bb09d4f4058cc091cf6165bcc13430cbe23942d8d5f253b047d38613b94c9d14.jpg)  
Figure 3-3 Read transfer with two wait states

Figure 3-4 shows a write transfer with one wait state.  
![](images/7cbfdb7100fa3bb175a8541e611026f56a443f235a21df4c133390ecbbe7f510.jpg)  
Figure 3-4 Write transfer with one wait state

Note

For write operations the Manager holds the data stable throughout the extended cycles. For read transfers, the Subordinate does not have to provide valid data until the transfer is about to complete. For further information on the use of stable data, see Clock on page 7-72.

When a transfer is extended in this way, it has the side-effect of extending the address phase of the next transfer.   
Figure 3-5 shows three transfers to unrelated addresses, A, B, and C with an extended address phase for address C.

![](images/539c6806f5e8845776ed194a87350793ece6cba31ed719d03e24e8f3e83f9d18.jpg)  
Figure 3-5 Multiple transfers  
In Figure 3-5:

The transfers to addresses A and C are zero wait state

The transfer to address B is one wait state

Extending the data phase of the transfer to address B has the effect of extending the address phase of the transfer to address C.

## 3.2 Transfer types

Table 3-1 lists the transfers that can be classified into one of four types, as controlled by HTRANS[1:0].  
Table 3-1 Transfer type encoding
<table><tr><td>HTRANS[1:0]</td><td>Type</td><td>Description</td></tr><tr><td>0b00</td><td>IDLE</td><td>Indicates that no data transfer is required. A Manager uses an IDLE transfer when it does not want to perform a data transfer. It is recommended that the Manager terminates a locked transfer with an IDLE transfer.</td></tr><tr><td>0b01</td><td>BUSY</td><td>Subordinates must always provide a zero wait state OKAY response to IDLE transfers and the transfer must be ignored by the Subordinate. The BUSY transfer type enables Managers to insert idle cycles in the middle of a burst. This transfer</td></tr><tr><td rowspan="5"></td><td rowspan="5"></td><td>type indicates that the Manager is continuing with a burst but the next transfer cannot take place immediately.</td></tr><tr><td>When a Manager uses the BUSY transfer type, the address and control signals must reflect the next transfer in the burst.</td></tr><tr><td>Only undefined length bursts can have a BUSY transfer as the last cycle of a burst. See Burst termination after a BUSY transfer on page 3-35.</td></tr><tr><td>Subordinates must always provide a zero wait state OKAY response to BUSY transfers and the transfer must be ignored by the Subordinate.</td></tr><tr><td>Indicates a single transfer or the first transfer of a burst</td></tr><tr><td rowspan="3">0b10</td><td rowspan="3">NONSEQ</td><td>The address and control signals are unrelated to the previous transfer.</td></tr><tr><td>Single transfers on the bus are treated as bursts of length one and therefore the transfer type is</td></tr><tr><td>NONSEQUENTIAL. The remaining transfers in a burst are SEQUENTIAL and the address is related to the previous</td></tr><tr><td rowspan="3">0b11</td><td rowspan="3">SEQ</td><td>transfer.</td></tr><tr><td>The control information is identical to the previous transfer. The address is equal to the address of the previous transfer plus the transfer size, in bytes, with the</td></tr><tr><td>transfer size being signaled by the HSIZE[2:0] signals. In the case of a wrapping burst, the address of the transfer wraps at the address boundary.</td></tr></table>

Figure 3-6 shows the use of the NONSEQ, BUSY, and SEQ transfer types.  
![](images/393282bd16eeda1fa1f23dd8a825df09300b8a77323eff00193e6075a53311d0.jpg)  
Figure 3-6 Transfer type examples

In Figure 3-6:

T0-T1 The 4-beat read starts with a NONSEQ transfer.

T1-T2 The Manager is unable to perform the second beat and inserts a BUSY transfer to delay the start of the second beat. The Subordinate provides the read data for the first beat.

T2-T3 The Manager is now ready to start the second beat, so a SEQ transfer is signaled. The Manager ignores any data that the Subordinate provides on the read data bus.

T3-T4 The Manager performs the third beat. The Subordinate provides the read data for the second beat.

T4-T5 The Manager performs the last beat. The Subordinate is unable to complete the transfer and uses HREADYOUT to insert a single wait state.

T5-T6 The Subordinate provides the read data for the third beat.

T6-T7 The Subordinate provides the read data for the last beat.

## 3.3 Locked transfers

If the Manager requires locked accesses, then it must also assert the HMASTLOCK signal. This signal indicates to any Subordinate that the current transfer sequence is indivisible and must therefore be processed before any other transfers are processed.

Typically the locked transfer is used to maintain the integrity of a semaphore, by ensuring that the Subordinate does not perform other operations between the read and write phases of a microprocessor SWP instruction.

In a locked sequence:

The bus is locked after a cycle with HMASTLOCK asserted, HSEL asserted if present, and HREADY is HIGH.

The bus is unlocked after a cycle with HMASTLOCK deasserted and HREADY is HIGH.

Figure 3-7 shows the HMASTLOCK signal with a microprocessor SWP instruction.

![](images/a7e25cef84c4dc5ddea863d4b8f9a51a3abb9bb4aeb3cb274459d5ecc6bd5237.jpg)  
Figure 3-7 Locked transfer

Note

After a locked transfer, it is recommended that the Manager inserts an IDLE transfer.

Most Subordinates have no requirement to implement HMASTLOCK because they are only capable of performing transfers in the order they are received. Subordinates that can be accessed by more than one Manager, for example, a Multi-Port Memory Controller (MPMC) must implement the HMASTLOCK signal.

It is permitted for a Manager to assert HMASTLOCK for IDLE transfers at the beginning, in the middle, or at the end of a sequence of locked transfers. Using locked IDLE transfers at the start or end of a locked transfer sequence is permitted, but not recommended, as this behavior can adversely affect the arbitration of the system.

It is also permitted, but not recommended, for a Manager to assert HMASTLOCK for a number of IDLE transfers and then deassert HMASTLOCK without performing a non-IDLE transfer. This behavior can adversely affect the arbitration of the system.

It is required that all transfers in a locked sequence are to the same Subordinate address region.

## 3.4 Transfer size

HSIZE[2:0] indicates the size of a data transfer. Table 3-2 lists the possible transfer sizes.

Table 3-2 Transfer size encoding
<table><tr><td>HSIZE[2]</td><td>HSIZE[1]</td><td>HSIZE[0]</td><td>Size (bits)</td><td>Description</td></tr><tr><td>0</td><td>0</td><td>0</td><td>8</td><td>Byte</td></tr><tr><td>0</td><td>0</td><td>1</td><td>16</td><td>Halfword</td></tr><tr><td>0</td><td>1</td><td>0</td><td>32</td><td>Word</td></tr><tr><td>0</td><td>1</td><td>1</td><td>64</td><td>Doubleword</td></tr><tr><td>1</td><td>0</td><td>0</td><td>128</td><td>4-word line</td></tr><tr><td>1</td><td>0</td><td>1</td><td>256</td><td>8-word line</td></tr><tr><td>1</td><td>1</td><td>0</td><td>512</td><td></td></tr><tr><td>1</td><td>1</td><td>1</td><td>1024</td><td></td></tr></table>

## 3.5 Write strobes

Write strobes is an optional feature, which enables a Manager to issue a write that updates only a subset of active write data bytes. The Write\_Strobes property indicates if an interface supports write strobes.

True Write strobes are supported and HWSTRB is included on the interface.

False Write strobes are not supported and HWSTRB is not included on the interface.

Note

If Write\_Strobes is not declared, it is considered as False.

## 3.5.1 Write strobes signaling

Table 2-2 on page 2-21 provides the information on HWSTRB signal for write strobes.

## 3.5.2 Write strobes rules

The following rules are applicable to write strobes in AHB:

For the transfers, which are narrower than the data bus, HSIZE and HADDR determine which byte lanes are active.

Write strobes which correspond to an active byte lane can be HIGH or LOW. A transfer with LOW strobe bits for active byte lanes is known as a sparse write.

Write strobes which correspond to an inactive byte lane can be HIGH or LOW. An interface must use HSIZE and HADDR to determine which byte lanes are inactive.

A transfer with all write strobes deasserted is permitted, no bytes are written in that transfer.

The mapping of write strobes to write data lanes is not dependent on endianness.

For read transfers, it is recommended that write strobes are deasserted.

Write strobes are permitted to change between beats of a write burst.

## 3.5.3 Interoperability

Table 3-3 describes how to connect interfaces based on their Write\_Strobes property:

Table 3-3 Write\_Strobes property
<table><tr><td>Write_Strobes Subordinate: False</td><td></td><td>Subordinate: True</td></tr><tr><td>Manager: False Compatible.</td><td></td><td>Compatible. Tie the HWSTRB input HIGH on the Subordinate</td></tr><tr><td></td><td></td><td>interface.</td></tr><tr><td>Manager: True</td><td>Compatible if the Manager does not generate sparse writes.</td><td>Compatible.</td></tr></table>

## 3.6 Burst operation

Bursts of 4, 8, and 16-beats, undefined length bursts, and single transfers are defined in this protocol. It supports incrementing and wrapping bursts:

Incrementing bursts access sequential locations and the address of each transfer in the burst is an increment of the previous address.

Wrapping bursts wrap when they cross an address boundary. The address boundary is calculated as the product of the number of beats in a burst and the size of the transfer. The number of beats are controlled by HBURST and the transfer size is controlled by HSIZE.

For example, a four-beat wrapping burst of word (4-byte) accesses wraps at 16-byte boundaries. Therefore, if the start address of the burst is 0x34, then it consists of four transfers to addresses 0x34, 0x38, 0x3C, and 0x30.

HBURST[2:0] controls the burst type. Table 3-4 lists the possible burst types.

Table 3-4 Burst signal encoding
<table><tr><td>HBURST[2:0]</td><td>Type</td><td>Description</td></tr><tr><td>0b000</td><td>SINGLE</td><td>Single transfer burst</td></tr><tr><td>0b001</td><td>INCR</td><td>Incrementing burst of undefined length</td></tr><tr><td>0b010</td><td>WRAP4</td><td>4-beat wrapping burst</td></tr><tr><td>0b011</td><td>INCR4</td><td>4-beat incrementing burst</td></tr><tr><td>0b100</td><td>WRAP8</td><td>8-beat wrapping burst</td></tr><tr><td>0b101</td><td>INCR8</td><td>8-beat incrementing burst</td></tr><tr><td>0b110</td><td>WRAP16</td><td>16-beat wrapping burst</td></tr><tr><td>0b111</td><td>INCR16</td><td>16-beat incrementing burst</td></tr></table>

Managers must not attempt to start an incrementing burst that crosses a 1KB address boundary.

Managers can perform single transfers using either:

SINGLE transfer burst.

Undefined length burst that has a burst of length one.

Note

The burst size indicates the number of beats in the burst and not the number of bytes transferred. Calculate the total amount of data transferred in a burst by multiplying the number of beats by the amount of data in each beat, as indicated by HSIZE[2:0].

All transfers in a burst must be aligned to the address boundary equal to the size of the transfer. For example, word transfers must align to word address boundaries (HADDR[1:0] = 0b00), and halfword transfers to halfword address boundaries (HADDR[0] = 0). It is recommended that the address for IDLE transfers is aligned, to avoid spurious warnings in simulation. In Issues A and B of this specification, this was a rule rather than a recommendation.

## 3.6.1 Burst termination after a BUSY transfer

After a burst has started, the Manager uses BUSY transfers if it requires more time before continuing with the next transfer in the burst.

During an undefined length burst, INCR, the Manager might insert BUSY transfers and then decide that no more data transfers are required. Under these circumstances, it is acceptable for the Manager to then perform a NONSEQ or IDLE transfer that then effectively terminates the undefined length burst.

The protocol does not permit a Manager to end a burst with a BUSY transfer for fixed-length bursts of type:

Incrementing INCR4, INCR8, and INCR16.

Wrapping WRAP4, WRAP8, and WRAP16.

These fixed-length burst types must terminate with a SEQ transfer.

The Manager is not permitted to perform a BUSY transfer immediately after a SINGLE burst. SINGLE bursts must be followed by an IDLE transfer or a NONSEQ transfer.

## 3.6.2 Early burst termination

Bursts can be terminated by either:

Subordinate error response

Multi-layer interconnect termination

## Subordinate error response

If a Subordinate provides an ERROR response, then the Manager can cancel the remaining transfers in the burst. However, this is not a strict requirement and it is also acceptable for the Manager to continue the remaining transfers in the burst.

If the Manager cancels the remaining transfers in the burst, then it must change HTRANS to indicate IDLE during the two-cycle Error response.

If the Manager does not complete that burst, then there is no requirement for it to rebuild the burst when it next accesses that Subordinate. For example, if a Manager only completes three beats of an eight-beat burst, then it does not have to complete the remaining five transfers when it next accesses that Subordinate.

## Multi-layer interconnect termination

Although Managers are not permitted to terminate a burst request early, Subordinates must be designed to work correctly if the burst is not completed.

When a multi-layer interconnect component is used in a multi-Manager system, then it can terminate a burst so that another Manager can gain access to the Subordinate. The Subordinate must terminate the burst from the original Manager and then respond appropriately to the new Manager if this occurs.

## 3.6.3 Burst examples

Examples of various bursts are shown in the following sections:

Four-beat wrapping burst, WRAP4

Four-beat incrementing burst, INCR4 on page 3-38

Eight-beat wrapping burst, WRAP8 on page 3-38

Eight-beat incrementing burst, INCR8 on page 3-39

Undefined length bursts, INCR on page 3-39

## Four-beat wrapping burst, WRAP4

Figure 3-8 shows a write transfer using a four-beat wrapping burst, with a wait state added for the first transfer.  
![](images/fd03a0ac4ef00496150ca1f09f23a17d2cd98583b91d768305851966e16751f1.jpg)  
Figure 3-8 Four-beat wrapping burst  
Because the burst is a four-beat burst of word transfers, the address wraps at 16-byte boundaries, and the transfer to address 0x3C is followed by a transfer to address 0x30.

## Four-beat incrementing burst, INCR4

Figure 3-9 shows a read transfer using a four-beat incrementing burst, with a wait state added for the first transfer. In this case, the address does not wrap at a 16-byte boundary and the address 0x3C is followed by a transfer to address 0x40.

![](images/1c9caf42fd24ac81b64d2238188e5992c1d324673a3f6939fc1a84ff1371fa4c.jpg)  
Figure 3-9 Four-beat incrementing burst

Eight-beat wrapping burst, WRAP8  
Figure 3-10 shows a read transfer using an eight-beat wrapping burst.  
![](images/921f1855151ff34aab7c3a711f51d790784596847e2cd331b27471aa202a781e.jpg)  
Figure 3-10 Eight-beat wrapping burst

Because the burst is an eight-beat burst of word transfers, the address wraps at 32-byte boundaries, and the transfer to address 0x3C is followed by a transfer to address 0x20.

## Eight-beat incrementing burst, INCR8

Figure 3-11 shows a write transfer using an eight-beat incrementing burst.  
![](images/6dc17f50241cdd159ab460d143d5f53c2d3ce7bf25ca5e9f67f5654b202a4d7c.jpg)  
Figure 3-11 Eight-beat incrementing burst

This burst uses halfword transfers, therefore the addresses increase by two. Because the burst is incrementing, the addresses continue to increment beyond the 16-byte address boundary.

## Undefined length bursts, INCR

Figure 3-12 shows incrementing bursts of undefined length.  
![](images/557a0ab7e3bb24ec9f96340254ee2ab8e1c4b2d2b066abf047ef84c389d5a866.jpg)  
Figure 3-12 Undefined length bursts  
Figure 3-12 shows two bursts:

The first burst is a write consisting of two halfword transfers starting at address 0x20. These transfer addresses increment by two.

The second burst is a read consisting of three word transfers starting at address 0x5C. These transfer addresses increment by four.

## 3.7 Waited transfers

Subordinates use HREADYOUT to insert wait states if they require more time to provide or sample the data. During a waited transfer, the Manager is restricted to what changes it can make to the transfer type and address. These restrictions are described in the following sections:

Transfer type changes during wait states

Address changes during wait states on page 3-43

## 3.7.1 Transfer type changes during wait states

When the Subordinate is requesting wait states, the Manager must not change the transfer type, except as described in:

IDLE transfer

BUSY transfer, fixed-length burst on page 3-41

BUSY transfer, undefined length burst on page 3-42

## IDLE transfer

During a waited transfer, the Manager is permitted to change the transfer type from IDLE to NONSEQ. When the HTRANS transfer type changes to NONSEQ the Manager must keep HTRANS constant, until HREADY is HIGH.

Figure 3-13 shows a waited transfer for a SINGLE burst, with a transfer type change from IDLE to NONSEQ.  
![](images/bd786774d691208262af0d2b80f44575afb3d76137b92efd19c7e9369879c601.jpg)  
Figure 3-13 Waited transfer, IDLE to NONSEQ

In Figure 3-13:

T0-T1 The Manager initiates a SINGLE burst to address A.

T1-T2 The Manager inserts one IDLE transfer to address Y. The Subordinate inserts a wait state with HREADYOUT = LOW.

T2-T3 The Manager inserts one IDLE transfer to address Z.

T3-T4 The Manager changes the transfer type to NONSEQ and initiates an INCR4 transfer to address B.

T4-T6 With HREADY LOW, the Manager must keep HTRANS constant.

T5-T6 SINGLE burst to address A completes with HREADY HIGH and the Manager starts the first beat to address B.

T6-T7 First beat of the INCR4 transfer to address B completes and the Manager starts the next beat to address B+4.

## BUSY transfer, fixed-length burst

During a waited transfer for a fixed-length burst, the Manager is permitted to change the transfer type from BUSY to SEQ. When the HTRANS transfer type changes to SEQ the Manager must keep HTRANS constant, until HREADY is HIGH.

Note

Because BUSY transfers must only be inserted between successive beats of a burst, this does not apply to SINGLE bursts. Therefore this situation applies to the following burst types:

INCR4, INCR8, and INCR16.

WRAP4, WRAP8, and WRAP16.

Figure 3-14 shows a waited transfer in a fixed-length burst, with a transfer type change from BUSY to SEQ.
<table><tr><td rowspan="2">HCLK</td><td colspan="2">TO</td><td colspan="2">T1</td><td colspan="2">T2</td><td colspan="2">T3</td><td colspan="2">T4 T5</td><td colspan="2">T6</td><td colspan="2">T7</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="2">HTRANS[1:0]</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td>SEQ</td><td></td><td>BUSY</td><td></td><td></td><td></td><td>SEQ</td><td></td><td></td><td>SEQ</td><td></td></tr><tr><td rowspan="2">HADDR[31:0]</td><td></td><td>0x24</td><td></td><td>0x28</td><td></td><td></td><td></td><td>0x28</td><td></td><td></td><td>0x2C</td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="2">HBURST[2:0] HREADY</td><td></td><td>INCR4</td><td></td><td></td><td>INCR4</td><td></td><td></td><td>INCR4</td><td></td><td></td><td>INCR4</td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="2">HRDATA[31:0]</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>Data (0x28)</td><td></td><td></td></tr><tr><td rowspan="2"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>4</td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>Data (0x24)</td><td></td><td></td><td></td></tr></table>

Figure 3-14 Waited transfer, BUSY to SEQ for a fixed-length burst

In Figure 3-14:

T0-T1 The Manager initiates the next beat of the INCR4 burst to address 0x24.

T1-T3 The Manager inserts a BUSY transfer to address 0x28.

T3-T4 The Manager changes the transfer type to SEQ and initiates the next beat of the burst to address 0x28.

T4-T6 With HREADY LOW, the Manager must keep HTRANS constant.

T5-T6 Beat to address 0x24 completes with HREADY HIGH.

T6-T7 Third beat of the INCR4 transfer to address 0x28 completes and the Manager starts the final beat to address 0x2C.

## BUSY transfer, undefined length burst

During a waited transfer for an undefined length burst, INCR, the Manager is permitted to change from BUSY to any other transfer type, when HREADY is LOW. The burst continues if a SEQ transfer is performed but terminates if an IDLE or NONSEQ transfer is performed.

Figure 3-15 shows a waited transfer during an undefined length burst, with a transfer type change from BUSY to NONSEQ.  
![](images/b26476c04d7ead93483baa5b5391675eb8c279cd0b9ae26231babc5204dce5ae.jpg)  
Figure 3-15 Waited transfer, BUSY to NONSEQ for an undefined length burst

In Figure 3-15:

T0-T1 The Manager initiates the next beat of the INCR burst to address 0x64.

T1-T3 The Manager inserts a BUSY transfer to address 0x68. The Subordinate inserts wait states with HREADYOUT = LOW.

T3-T4 The Manager changes the transfer type to NONSEQ and initiates a new burst to address 0x10.

T4-T6 With HREADY LOW, the Manager must keep HTRANS constant.

T5-T6 Undefined length burst completes with HREADY HIGH and the Manager starts the first beat to address 0x10.

T6-T7 First beat of the INCR4 transfer to address 0x10 completes and the Manager starts the next beat to address 0x14.

## 3.7.2 Address changes during wait states

When the Subordinate is requesting wait states, the Manager can only change the address once, except as described in:

During an IDLE transfer

After an ERROR response on page 3-44

## During an IDLE transfer

During a waited transfer, the Manager is permitted to change the address for IDLE transfers. When the HTRANS transfer type changes to NONSEQ, the Manager must keep the address constant until HREADY is HIGH.

Figure 3-16 shows a waited transfer for a SINGLE burst, with the address changing during the IDLE transfers.  
![](images/13f90c9657dfb2c7dee087c1c124cd79f5d7a3bb2576d3c30b6ebab9820c87a1.jpg)  
Figure 3-16 Address changes during a waited transfer, with an IDLE transfer

In Figure 3-16:

T0-T1 The Manager initiates a SINGLE burst to address A.

T1-T2 The Manager inserts one IDLE transfer to address Y. The Subordinate inserts a wait state with HREADYOUT = LOW.

T2-T3 The Manager inserts one IDLE transfer to address Z.

T3-T4 The Manager changes the transfer type to NONSEQ and initiates an INCR4 transfer to address B. Until HREADY goes HIGH, no more address changes are permitted.

T5-T6 SINGLE burst to address A completes with HREADY HIGH and the Manager starts the first beat to address B.

T6-T7 First beat of the INCR4 transfer to address B completes and the Manager starts the next beat to address B+4.

## After an ERROR response

During a waited transfer, if the Subordinate responds with an ERROR response, then the Manager is permitted to change the address when HREADY is LOW. See ERROR response on page 5-61 for more information about the ERROR response.

Figure 3-17 shows a waited transfer, with the address changing following an ERROR response from the Subordinate.  
![](images/80943e9edc89a9d1ef793a94c0b33ae369f09c2545e82daee7826cc721ac556b.jpg)  
Figure 3-17 Address changes during a waited transfer, after an ERROR

In Figure 3-17:

T0-T1 The Manager initiates the next beat of the burst to address 0x24.

T1-T3 The Manager initiates the next beat of the burst to address 0x28. The Subordinate responds with OKAY.

T3-T4 The Subordinate responds with ERROR.

T4-T5 The Manager changes the transfer type to IDLE and is permitted to change the address while HREADY is LOW. The Subordinate completes the ERROR response.

T5-T6 The Subordinate at address 0xC0 responds with OKAY.

## 3.8 Protection control

Issue A of this specification defined a 4-bit HPROT signal, which is described in this section.

Issue B of this specification adds extended memory types and this is described in more detail in Memory types on page 3-46.

Note

The name of HPROT[3] is changed between Issue A and Issue B of this specification, but the definition remains the same. In Issue A HPROT[3] was designated Cacheable, in Issue B it is designated Modifiable.

The protection control signals, HPROT[3:0], provide additional information about a bus access and are primarily intended for use by any module that implements some level of protection.

The signals indicate if the transfer is:

An opcode fetch or data access.

A privileged mode access or user mode access.

For Managers with a Memory Management Unit, these signals also indicate if the current access is Cacheable or Bufferable. Table 3-5 lists the HPROT signal encoding.

Table 3-5 Protection signal encoding
<table><tr><td>HPROT[3] Modifiable</td><td>HPROT[2] Bufferable</td><td>HPROT[1] Privileged</td><td>HPROT[0] Data/Opcode</td><td>Description</td></tr><tr><td></td><td></td><td></td><td>0</td><td>Opcode fetch</td></tr><tr><td></td><td></td><td></td><td>1</td><td>Data access</td></tr><tr><td></td><td></td><td>0</td><td></td><td>User access</td></tr><tr><td></td><td></td><td>1</td><td></td><td>Privileged access</td></tr><tr><td></td><td>0</td><td></td><td></td><td>Non-bufferable</td></tr><tr><td></td><td>1</td><td></td><td></td><td>Bufferable</td></tr><tr><td>0</td><td></td><td></td><td></td><td>Non-cacheable</td></tr><tr><td>1</td><td></td><td></td><td></td><td>Cacheable</td></tr></table>

Note

Many Managers are not capable of generating accurate protection information. If a Manager is not capable of generating accurate protection information, it is recommended that:

The Manager sets HPROT to 0b0011 to correspond to a Non-cacheable, Non-bufferable, privileged, data access.

Subordinates do not use HPROT unless necessary.

The HPROT control signals have the same timing as the address bus. However, they must remain constant throughout a burst transfer.

## 3.9 Memory types

AHB5 defines the Extended\_Memory\_Types property. This property defines whether an interface supports the extended memory types described in this section. If this property is not defined, then the interface does not support the extended memory types.

This issue of the specification adds additional HPROT signaling and provides a more detailed list of requirements for each of the memory types.

Table 3-6 shows the meaning of each HPROT bit and Table 3-7 on page 3-47 provides a mapping between HPROT[6:2] and the memory type.

Table 3-6 Meaning of the HPROT bits
<table><tr><td>Bit</td><td>Name</td><td>Description</td></tr><tr><td>HPROT[0]</td><td>Data/Inst</td><td>When asserted, this bit indicates the transfer is a data access. When deasserted this bit indicates the transfer is an instruction fetch.</td></tr><tr><td>HPROT[1]</td><td>Privileged</td><td>When asserted, this bit indicates the transfer is a privileged access. When deasserted this bit indicates the transfer is an unprivileged access.</td></tr><tr><td>HPROT[2]</td><td>Bufferable</td><td>If both of HPROT[4:3] are deasserted, then when this bit is: Deasserted, the write response must be given from the final destination.</td></tr><tr><td></td><td>Modifiable</td><td>the write transfer is required to be made visible at the final destination in a timely manner. When asserted, the characteristics of the transfer can be modified.</td></tr><tr><td>HPROT[4] Lookup</td><td></td><td>When deasserted the characteristics of the transfer must not be modified. When asserted, the transfer must be looked up in a cache. When deasserted, the transfer does not need to be looked up in a cache and the</td></tr><tr><td>HPROT[5]</td><td>Allocate</td><td>transfer must propagate to the final destination. When asserted, for performance reasons, it is recommended that this transfer is allocated in the cache.</td></tr><tr><td>HPROT[6]</td><td>Shareable</td><td>not allocated in the cache. When asserted, indicates that this transfer is to a region of memory that is shared with other Managers in the system. A response for the transfer must not be</td></tr><tr><td></td><td></td><td>provided until the transfer is visible to other Managers. When deasserted, indicates that this transfer is Non-shareable and the region of</td></tr></table>

## 3.9.1 Data or Instruction

All transfers include the Data or Instruction protection bit HPROT[0]:

When asserted, this bit indicates the transfer is a data access.

When deasserted this bit indicates the transfer is an instruction fetch.

The protocol defines this indication as a hint. It is not accurate in all cases, for example, where a transaction contains a mix of instruction and data items.

It is recommended that a Manager sets HPROT[0] HIGH, to indicate a data access unless the access is specifically known to be an instruction access.

## 3.9.2 Unprivileged or Privileged

All transfers include the Privileged or Unprivileged protection bit, HPROT[1]:

When asserted, this bit indicates the transfer is a Privileged access.

When deasserted this bit indicates the transfer is an Unprivileged access.

Note

Some processors support multiple levels of privilege, see the documentation for the selected processor to determine the mapping to AHB privilege levels. The only distinction provided is between Privileged and Unprivileged access.

## 3.9.3 Memory type

This section provides additional information on the HPROT Protection Control signals and how these signals relate to different memory types.

The Device memory type E suffix indicates that an early write response is permitted.

The Device memory type nE suffix indicates that an early write response is not permitted and that the write response must come from the final destination.

Table 3-7 shows the mapping between HPROT[6:2] signaling and the memory type. The bit combinations that Table 3-7 does not show, are not permitted.

Table 3-7 Permitted combinations of HPROT bits
<table><tr><td>HPROT[6]</td><td>HPROT[5]</td><td>HPROT[4]</td><td>HPROT[3]</td><td>HPROT[2]</td><td>Memory Type</td></tr><tr><td>Shareable</td><td>Allocate</td><td>Lookup</td><td>Modifiable</td><td>Bufferable</td><td></td></tr><tr><td>0a</td><td>0</td><td>0</td><td>0</td><td>0</td><td>Device-nE</td></tr><tr><td>0a</td><td>0</td><td>0</td><td>0</td><td>1</td><td>Device-E</td></tr><tr><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>Normal Non-cacheable, Non-shareable</td></tr><tr><td>0</td><td>0 or 1</td><td>1</td><td>1</td><td>0</td><td>Write-through, Non-shareable</td></tr><tr><td>0</td><td>0 or 1</td><td>1</td><td>1</td><td>1</td><td>Write-back, Non-shareable</td></tr><tr><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>Normal Non-cacheable, Shareable</td></tr><tr><td>1</td><td>0 or 1</td><td>1</td><td>1</td><td>0</td><td>Write-through, Shareable</td></tr><tr><td>1</td><td>0 or 1</td><td>1</td><td>1</td><td>1</td><td>Write-back, Shareable</td></tr></table>

a. Not applicable and must be zero for Device memory.

The following sections detail the requirements for each memory type.

## 3.9.4 Device memory requirements

For all Device memory, that is Device-nE and Device-E, the required behavior is:

Read data must be obtained from the final destination.

Transfers must not be split into multiple transfers or merged with other transfers.

Reads must not be prefetched or performed speculatively.

Writes must not be merged.

All read and write transfers from the same Manager to the same Subordinate must remain ordered.

The size of the transfer, as indicated by HSIZE, must not be changed.

A burst of transfers is permitted to be broken into a number of smaller bursts. However, the total number of NONSEQ and SEQ transfers in the original burst must be the same as the total number of NONSEQ and SEQ transfers in the resultant smaller bursts.

The only change permitted to HPROT is to convert a transfer from Bufferable to Non-bufferable.

For Device-nE:

Write response must be obtained from the final destination.

## For Device-E:

The write response can be obtained from an intermediate point.

Write transfers must be observable to all other Managers at the point that a write response is given.

Write transfers must arrive at the final destination in a timely manner.

## 3.9.5 Normal memory requirements

Normal memory can be Normal Non-cacheable, Write-through, or Write-back. For Normal memory, the required behavior is:

Reads can be speculative.

Reads can fetch more data than required.

Writes can be merged.

The characteristics of the transfer, as indicated by HBURST and HSIZE can be changed.

Read and write transfers from the same Manager to addresses that overlap must remain ordered.

• For Shareable transactions, the response must only be given when the transfer is visible to all other Managers.

Additionally, for Normal Non-cacheable memory:

Write transfers must be made visible at the final destination in a timely manner.

Note

There is no mechanism to determine when a write transfer has reached its final destination.

Read data must be obtained either from:

The final destination.

A write transfer that is progressing to its final destination.

If read data is obtained from a write transfer:

It must be obtained from the most recent version of the write.

The data must not be cached to service a later read.

Reads must not cache the data obtained for later use.

For a Normal Non-cacheable Memory, read data can be obtained from a write transfer that is still progressing to its final destination, this is indistinguishable from the read and write transfers propagating to arrive at the final destination at the same time. Read data returned in this manner does not indicate that the write transfer is visible at the final destination.

Additionally, for Write-through:

The write response can be obtained from an intermediate cache or buffer.

Read data can be cached in an intermediate cache or buffer.

A cache lookup is required for read and write transfers.

Write transactions must be made visible at the final destination in a timely manner.

Note

There is no mechanism to determine when a write transaction is visible at the final destination.

Additionally, for Write-back:

The write response can be obtained from an intermediate cache or buffer.

Read data can be cached in an intermediate cache or buffer.

A cache lookup is required for read and write transfers.

Write transactions are not required to be made visible at the final destination.

## 3.9.6 Allocate attribute

Write-through and Write-back transfers include an Allocate attribute, HPROT[5]. For performance reasons, it is recommended that:

When asserted, this transfer is allocated in the cache.

When deasserted, this transfer is not allocated in the cache.

## 3.9.7 Legacy Considerations

Table 3-8 shows the recommended mapping to provide HPROT[6:0] signaling for a component that only includes HPROT[3:0] signaling.

Table 3-8 Mapping of an HPROT[3:0] signaling component to provide HPROT[6:0] signaling
<table><tr><td colspan="4">Original Signaling</td><td colspan="4">Mapping for extended memory type</td><td rowspan="2">Maps to memory type</td></tr><tr><td>HPROT</td><td></td><td>Definition</td><td>Expected use</td><td>HPROT</td><td></td><td></td><td></td></tr><tr><td>[3]</td><td>[2]</td><td></td><td></td><td>[6]</td><td>[4]</td><td>[3]</td><td>[2]</td><td></td></tr><tr><td>0</td><td>0</td><td>Non-cacheable, Non-bufferable</td><td>Strongly ordered</td><td>0</td><td>0</td><td>0</td><td>0</td><td>Device-nE</td></tr><tr><td>0</td><td>1</td><td>Non-cacheable, Bufferable</td><td>Device</td><td>0</td><td>0</td><td>0</td><td>1</td><td>Device-E</td></tr><tr><td>1</td><td>0</td><td>Cacheable, Non-bufferable</td><td>Write-through</td><td>1</td><td>1</td><td>1</td><td>0</td><td>Write-through, Shareable</td></tr><tr><td>1</td><td>1</td><td>Cacheable, Bufferable</td><td>Write-back</td><td>1</td><td>1</td><td>1</td><td>1</td><td>Write-back, Shareable</td></tr></table>

When using components that support HPROT[6:0] in a system that only includes HPROT[3:0], then the higher order HPROT bits can be removed.

Note

This approach results in the mapping of Write-through to Non-cacheable memory. However, an alternative scheme can be used, in particular, if additional information is provided to determine a more appropriate mapping.

## 3.10 Secure transfers

AHB5 defines the Secure\_Transfers property. This property defines whether an interface supports the concept of Secure and Non-secure transfers. If this property is not defined, then the interface does not support Secure transfers.

An interface that supports Secure transfers has an additional signal, HNONSEC. This signal is asserted for a Non-secure transfer and deasserted for a Secure transfer.

HNONSEC is an address phase signal and must be constant throughout a burst.

Care must be taken when interfacing between components that do not support Secure transfers.

Note

This signal is defined so that when it is asserted the transfer is identified as Non-secure. This is consistent with other signaling in implementations of the Arm Security Extensions.

3.10 Secure transfers

## Chapter 4 Bus Interconnection

This chapter describes the additional interconnect logic required for AMBA AHB systems. It contains the following sections:

Interconnect on page 4-54

Address decoding on page 4-55

Read data and response multiplexor on page 4-56

## 4.1 Interconnect

An interconnect component provides the connection between Managers and Subordinates in a system.

A single Manager system only requires the use of a Decoder and Multiplexor, as described in the following sections.

A multi-Manager system requires the use of an interconnect that provides arbitration and the routing of signals from different Managers to the appropriate Subordinates. This routing is required for address, control, and write data signaling. Further details of the different approaches used for multi-Manager systems, such as single layer or multi-layer interconnects, are not provided within this specification.

See Multi-layer AHB Technical Overview (ARM DVI 0045) for more information about implementing a multi-layer AHB-Lite interconnect.

## 4.2 Address decoding

An address decoder provides a select signal, HSELx, for each Subordinate on the bus. Simple address decoding schemes are encouraged to avoid complex decode logic and to ensure high-speed operation.

A Subordinate must only sample the HSELx, address, and control signals when HREADY is HIGH, indicating that the current transfer is completing. Under certain circumstances, it is possible that HSELx is asserted when HREADY is LOW, but the selected Subordinate has changed by the time the current transfer completes. See Address changes during wait states on page 3-43.

The minimum address space that can be allocated to a single Subordinate is 1KB, and the start and the end of the address region must exist on a 1KB boundary. All Managers are designed so that they do not perform incrementing transfers over a 1KB address boundary. This ensures that a burst never crosses an address decode boundary.

Figure 4-1 shows the HSELx Subordinate select signals generated by the decoder.

![](images/3b964cfe44c4c01b5e3632a1f784779b712567a8f5485314140dffadb86443f9.jpg)  
Figure 4-1 Subordinate select signals

## 4.2.1 Default Subordinate

If a system design does not contain a completely filled memory map, then an additional default Subordinate must be implemented to provide a response when any of the nonexistent address locations are accessed.

If a NONSEQUENTIAL or SEQUENTIAL transfer is attempted to a nonexistent address location, then the default Subordinate provides an ERROR response.

IDLE or BUSY transfers to nonexistent locations result in a zero wait state OKAY response.

## 4.2.2 Multiple Subordinate select

A single Subordinate interface is permitted to support multiple Subordinate select, HSELx, signals. Each HSELx signal corresponds to a different decode of the higher-order address bits.

This permits a single Subordinate interface to provide multiple logical interfaces, each with a different location in the system address map. The minimum address space that can be allocated to a logical interface is 1KB. This approach removes the need for a Subordinate to support the address decode to differentiate between the logical interfaces.

A typical use case for multiple HSELx signals is a peripheral that has its main data path and control registers at different locations in the address map. Both locations can be accessed through a single interface without the need for the Subordinate to perform an address decode.

## 4.3 Read data and response multiplexor

The AHB protocol is used with a read data multiplexor interconnection scheme. The Manager drives out the address and control signals to all the Subordinates, with the decoder selecting the appropriate Subordinate during the data phase of the transfer. Any response data from the selected Subordinate, passes through the read data multiplexor to the Manager.

Figure 4-2 shows the multiplexor interconnection structure required to implement a design with three Subordinates.  
![](images/0216c9ebdf8b6859bbd9dbe7107e8c9ce7363b56ac44dd4e248ebe39fc9171de.jpg)  
Figure 4-2 Multiplexor interconnection

## 4.4 Interconnect with AHB interfaces

Generic interconnect products can offer AHB as an interface option, among others such as AMBA AXI or AMBA APB. Figure 4-3 shows how a generic interconnect might implement HTRANS, HREADY, and HSEL

![](images/cf7b28ee5fb66aa628e081b6b562ec7aa72ad5146bcbda9fb3b6aa168216adfd.jpg)  
Figure 4-3 Interconnect with AHB interfaces

In this example, the Manager side of the interconnect uses HTRANS to indicate valid transfers and has a single HREADY signal. HREADY is used to stall a transfer when the Subordinate has inserted wait states or when the Manager is waiting for arbitration from within the interconnect.

The Subordinate side of the interconnect also includes an HSEL output and two HREADY signals. HREADYOUT from the Subordinate is passed to the Managers to insert wait states. The HREADY output from the interconnect can be used to stall a Subordinate if the data phase of the previous transfer is stalled.

An alternative implementation would be for HSEL to be tied HIGH on the Subordinates and the interconnect to override HTRANS to IDLE for unselected Subordinates.

4.4 Interconnect with AHB interfaces

## Chapter 5 Subordinate Response Signaling

This chapter describes the Subordinate response signaling. It contains the following section:

Subordinate transfer responses on page 5-60

## 5.1 Subordinate transfer responses

After a Manager has started a transfer, the Subordinate controls how the transfer progresses. A Manager cannot cancel a transfer after it has commenced.

For components that support the AHB5 Exclusive\_Transfers property, see Exclusive access signaling on page 10-84 for details of the additional HEXOKAY transfer response signal.

A Subordinate must provide a response that indicates the status of the transfer when it is accessed. The transfer status is provided by the HRESP signal. Table 5-1 lists the HRESP states.

Table 5-1 shows that the complete transfer response is a combination of the HRESP and HREADYOUT signals.

Table 5-1 HRESP signal response
<table><tr><td>HRESP</td><td>Response Description</td><td></td></tr><tr><td>0</td><td>OKAY</td><td>The transfer has either completed successfully or additional cycles are required for the Subordinate to complete the request.</td></tr><tr><td rowspan="2">1</td><td rowspan="2">ERROR</td><td>The HREADYOUT signal indicates whether the transfer is pending or complete.</td></tr><tr><td>An error has occurred during the transfer. The error condition must be signaled to the Manager so that it is aware the transfer has been unsuccessful.</td></tr></table>

Table 5-2 lists the complete transfer response based on the status of the HRESP and HREADYOUT signals.

Table 5-2 Combined HRESP and HREADYOUT signal response
<table><tr><td></td><td colspan="2">HREADYOUT</td></tr><tr><td>HRESP</td><td>0 1</td><td></td></tr><tr><td>0</td><td>Transfer pending</td><td>Successful transfer completed</td></tr><tr><td>1</td><td>ERROR response, first cycle</td><td>ERROR response, second cycle</td></tr></table>

This means the Subordinate can complete the transfer in the following three ways:

Immediately complete the transfer.

Signal an error to indicate that the transfer has failed.

Insert one or more wait states to enable time to complete the transfer.

These three Subordinate transfer responses are described in:

Transfer done

Transfer pending

ERROR response on page 5-61

## 5.1.1 Transfer done

A successful completed transfer is signaled when HREADY is HIGH and HRESP is OKAY.

## 5.1.2 Transfer pending

A typical Subordinate uses HREADYOUT to insert the appropriate number of wait states into the data phase of the transfer. The transfer then completes with HREADYOUT HIGH and an OKAY response to indicate the successful completion of the transfer.

When a Subordinate inserts a number of wait states prior to completing the response, it must drive HRESP to OKAY.

Note

In general, every Subordinate must have a predetermined maximum number of wait states that it inserts before it completes a transfer. This enables the maximum latency for accessing the bus to be calculated. Inserting wait states stalls the entire AHB interface, so long periods of wait states can have a negative impact on the system performance.

## 5.1.3 ERROR response

A Subordinate uses the ERROR response to indicate some form of error condition with the associated transfer.   
Usually this denotes a protection error such as an attempt to write to a read-only memory location.

Although an OKAY response can be given in a single cycle, the ERROR response requires two cycles. To start the ERROR response, the Subordinate drives HRESP HIGH to indicate ERROR while driving HREADYOUT LOW to extend the transfer for one extra cycle. In the next cycle HREADYOUT is driven HIGH to end the transfer and HRESP remains driven HIGH to indicate ERROR.

The two-cycle response is required because of the pipelined nature of the bus. By the time a Subordinate starts to issue an ERROR response, then the address for the following transfer has already been broadcast onto the bus. The two-cycle response provides sufficient time for the Manager to cancel this next access and drive HTRANS[1:0] to IDLE before the start of the next transfer.

If the Subordinate requires more than two cycles to provide the ERROR response, then additional wait states can be inserted at the start of the transfer. During this time HREADY is LOW and the response must be set to OKAY.

Figure 5-1 shows a transfer with an ERROR response.
<table><tr><td rowspan="2">HCLK</td><td rowspan="2">TO</td><td rowspan="2"></td><td rowspan="2">T1</td><td colspan="2">T2</td><td colspan="2">T3</td><td colspan="2">T4</td><td colspan="2">T5</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="2">HTRANS[1:0]</td><td></td><td>NONSEQ</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>IDLE</td><td></td><td></td><td></td></tr><tr><td rowspan="2">HADDR[31:0]</td><td></td><td>A</td><td></td><td></td><td>B</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="2">HWRITE</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="2">HWDATA[31:0] HREADY</td><td></td><td></td><td></td><td></td><td>Data (A)</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="2">HRESP</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td>OKAY</td><td></td><td>OKAY</td><td></td><td>ERROR</td><td></td><td>ERROR</td><td></td><td>OKAY</td><td></td></tr></table>

Figure 5-1 ERROR response  
In Figure 5-1:

T1-T2 The Subordinate inserts a wait state and provides an OKAY response.

T2-T3 The Subordinate issues an ERROR response. This is the first cycle of the ERROR response because HREADY is LOW.

T3-T4 The Subordinate issues an ERROR response. This is the last cycle of the ERROR response because HREADY is now HIGH.

The Manager changes the transfer type to IDLE. This cancels the intended transaction to address B, that was registered by a Subordinate at time T2.

T4-T5 Subordinate responds with an OKAY response.

If a Subordinate provides an ERROR response, then the Manager can cancel the remaining transfers in the burst. However, this is not a strict requirement and it is acceptable for the Manager to continue the remaining transfers in the burst. A Manager, which receives an ERROR response to a read transfer might still use the data. A Subordinate cannot rely on the ERROR response to prevent the reading of a value on HRDATA. It is recommended that HRDATA is driven to zero when an ERROR response is given to a read transfer.

5 Subordinate Response Signaling

5.1 Subordinate transfer responses

# Chapter 6 Data Buses

This chapter describes the data buses. It contains the following sections:

Data buses on page 6-64

Endianness on page 6-65

Data bus width on page 6-69

## 6.1 Data buses

Separate read and write data buses are required to implement an AHB system. Although the recommended minimum data bus width is specified as 32-bits, this can be changed as described in Data bus width on page 6-69. The data buses are described in:

HWDATA

HRDATA

Endianness on page 6-65

## 6.1.1 HWDATA

The Manager drives the write data bus during write transfers. If the transfer is extended, then the Manager must hold the data valid until the transfer completes, as indicated by HREADY HIGH. See Clock on page 7-72 for details on holding signals valid across multiple cycles.

For transfers that are narrower than the width of the bus, for example a 16-bit transfer on a 32-bit bus, the Manager only has to drive the appropriate byte lanes. The Subordinate selects the write data from the correct byte lanes. See Endianness on page 6-65 for details of the byte lanes that are active for a little-endian and big-endian system.

## 6.1.2 HRDATA

The appropriate Subordinate drives the read data bus during read transfers. If the Subordinate extends the read transfer by holding HREADY LOW, then the Subordinate only has to provide valid data in the final cycle of the transfer, as indicated by HREADY HIGH.

For transfers that are narrower than the width of the bus, the Subordinate is only required to provide valid data on the active byte lanes. The Manager selects the data from the correct byte lanes.

A Subordinate only has to provide valid data when a transfer completes with an OKAY response. ERROR responses do not require valid read data.

## 6.2 Endianness

AHB supports both big-endian and little-endian systems. Two approaches to big-endian data storage are supported.

AHB5 introduces the Endian property to define which form of big-endian data access is supported.

BE8 Byte-invariant big-endian. The term, byte-invariant big-endian, is derived from the fact that a byte access (8-bit) uses the same data bus bits as a little-endian access to the same address.

BE32 Word-invariant big-endian. The term, word-invariant big-endian, is derived from the fact that a word access (32-bit) uses the same data bus bits for the Most Significant (MS) and the Least Significant (LS) bytes as a little-endian access to the same address.

Additional information on byte-invariant big-endian can be found in the section Byte invariance on page 6-67.

The following set of equations defines which data bits are used for little-endian, byte-invariant big-endian, and word-invariant big-endian accesses.

The equations use the following variables:

address The address of the transfer.

Data\_Bus\_Bytes The number of 8-bit data bus byte lanes.

INT(x) Rounded down integer value of x.

## 6.2.1 Little-endian

When a little-endian component accesses a byte, the following equation shows which data bus bits are used:

Byte\_Lane = Address –(INT(Address / Data\_bus\_Bytes)) × Data\_Bus\_Bytes

Data is transferred on DATA[(8 × Byte\_Lane) + 7 : (8 × Byte\_Lane)]

When larger little-endian transfers occur, data is transferred such that:

The LS byte is transferred to the transfer address.

Increasingly significant bytes are transferred to sequentially incrementing addresses.

## 6.2.2 Byte-invariant big-endian

When a byte-invariant big-endian component accesses a byte, the following equation shows which data bus bits are used:

Byte\_Lane = Address –(INT(Address / Data\_bus\_Bytes)) × Data\_Bus\_Bytes

Data is transferred on DATA[(8 × Byte\_lane) + 7 : (8 × Byte\_lane)]

Note

These equations are identical to those for little-endian. Because big-endian and little-endian accesses are identical for byte transfers, the term byte-invariant is used for these transfers.

When larger byte-invariant big-endian transfers occur, data is transferred such that:

The MS byte is transferred to the transfer address.

Decreasingly significant bytes are transferred to sequentially incrementing addresses.

Note

This is the key difference between byte-invariant big-endian and little-endian components.

## 6.2.3 Word-invariant big-endian

When a word-invariant big-endian component accesses a byte, the following equation shows which data bus bits are used:

Address\_Offset = Address –(INT(Address / Data\_Bus\_Bytes)) × Data\_bus\_Bytes

Word\_Offset = (INT(Address\_Offset / 4)) × 4

Byte\_Offset = Address\_Offset – Word\_Offset

Data is transferred on DATA[(8 × (Word\_Offset + 3 – Byte\_Offset)) + 7 : 8 × (Word\_Offset + 3 – Byte\_Offset)]

For a 32-bit bus, the Word\_Offset will always be zero and therefore the equation simplifies to:

DATA[(8 × (3 – Byte\_Offset)) + 7 : 8 × (3 – Byte\_Offset)]

This shows a key difference between word-invariant big-endian and little-endian components. A word-invariant big-endian component transfers a byte quantity using different data bus bits compared to both little-endian and byte-invariant big-endian components.

For halfword and word transfers using word-invariant big-endian, data is transferred such that:

The most significant byte is transferred to the transfer address.

Decreasingly significant bytes are transferred to sequentially incrementing addresses.

For transfers larger than a word using word-invariant big-endian, data is split into word size blocks:

The least significant word is transferred to the transfer address.

Increasingly significant words are transferred to incrementing addresses.

The 32-bit data bus in Table 6-1, Table 6-2 on page 6-67, and Table 6-3 on page 6-67 can be extended for wider data bus implementations.

Burst transfers that have a transfer size less than the width of the data bus have different active byte lanes for each beat of the burst.

Table 6-1 and Table 6-2 on page 6-67 show the byte lanes on a 32-bit bus that are active in a little-endian or byte-invariant big-endian system. The active byte lanes are identical in both cases, but the locations of the most significant and least significant bytes differ.

Table 6-1 Active byte lanes for a 32-bit little-endian data bus
<table><tr><td>Transfer size</td><td>Address offset</td><td>DATA[31:24]</td><td>DATA[23:16]</td><td>DATA[15:8]</td><td>DATA[7:0]</td></tr><tr><td>Word</td><td>0</td><td>Active[MS]</td><td>Active</td><td>Active</td><td>Active[LS]</td></tr><tr><td>Halfword</td><td>0</td><td>1</td><td>1</td><td>Active[MS]</td><td>Active[LS]</td></tr><tr><td>Halfword</td><td>2</td><td>Active[MS]</td><td>Active[LS]</td><td></td><td>1</td></tr><tr><td>Byte</td><td>0</td><td></td><td></td><td></td><td>Active</td></tr><tr><td>Byte</td><td>1</td><td></td><td>1</td><td>Active</td><td>I</td></tr><tr><td>Byte</td><td>2</td><td>1</td><td>Active</td><td></td><td></td></tr><tr><td>Byte</td><td>3</td><td>Active</td><td>1</td><td></td><td></td></tr></table>

Table 6-2 Active byte lanes for a 32-bit byte-invariant big-endian data bus
<table><tr><td>Transfer size</td><td>Address offset</td><td>DATA[31:24]</td><td>DATA[23:16]</td><td>DATA[15:8]</td><td>DATA[7:0]</td></tr><tr><td>Word</td><td>0</td><td>Active[LS]</td><td>Active</td><td>Active</td><td>Active[MS]</td></tr><tr><td>Halfword</td><td>0</td><td>1</td><td>-</td><td>Active[LS]</td><td>Active[MS]</td></tr><tr><td>Halfword</td><td>2</td><td>Active[LS]</td><td>Active[MS]</td><td>1</td><td>1</td></tr><tr><td>Byte</td><td>0</td><td></td><td></td><td>1</td><td>Active</td></tr><tr><td>Byte</td><td>1</td><td>1</td><td>1</td><td>Active</td><td>1</td></tr><tr><td>Byte</td><td>2</td><td>-</td><td>Active</td><td></td><td></td></tr><tr><td>Byte</td><td>3</td><td>Active</td><td>一</td><td>一</td><td>一</td></tr></table>

Table 6-3 shows the byte lanes on a 32-bit bus that are active in a word-invariant big-endian system.

Table 6-3 Active byte lanes for a 32-bit word-invariant big-endian data bus
<table><tr><td>Transfer size</td><td>Address offset</td><td>DATA[31:24]</td><td>DATA[23:16]</td><td>DATA[15:8]</td><td>DATA[7:0]</td></tr><tr><td>Word</td><td>0</td><td>Active[MS]</td><td>Active</td><td>Active</td><td>Active[LS]</td></tr><tr><td>Halfword</td><td>0</td><td>Active[MS]</td><td>Active[LS]</td><td></td><td>1</td></tr><tr><td>Halfword</td><td>2</td><td>1</td><td>1</td><td>Active[MS]</td><td>Active[LS]</td></tr><tr><td>Byte</td><td>0</td><td>Active</td><td></td><td></td><td></td></tr><tr><td>Byte</td><td>1</td><td>1</td><td>Active</td><td>1</td><td>1</td></tr><tr><td>Byte</td><td>2</td><td></td><td></td><td>Active</td><td>I</td></tr><tr><td>Byte</td><td>3</td><td>一</td><td>1</td><td>1</td><td>Active</td></tr></table>

## 6.2.4 Byte invariance

The use of byte-invariant big-endian data structures simplifies accessing a mixed-endian data structure in a single memory space.

Using byte-invariant big-endian and little-endian means that, for any multi-byte element in a data structure:

The element uses the same continuous bytes of memory, regardless of the endianness of the data.

The endianness determines the order of those bytes in memory, meaning it determines whether the first byte in memory is the MS byte or the LS byte of the element.

Any byte transfer to a given address passes the eight bits of data on the same data bus wires to the same address location, regardless of the endianness of any data element of which the byte is a part.

Figure 6-1 shows an example of a data structure that requires byte-invariant access. In this example, the header fields use little-endian ordering, and the data payload uses big-endian ordering.

![](images/07f716760a5fb3a724ed48560b9acc5c394ff2ad3290a78f26de2a0207ba8eca.jpg)  
Figure 6-1 Example mixed-endian data structure

In this structure, for example, Count is a two-byte little-endian element, meaning its lowest address is its LS byte.   
The use of byte invariance ensures that a big-endian access to the payload does not corrupt the little-endian element.

## 6.3 Data bus width

One method to improve bus bandwidth without increasing the frequency of operation is to make the data path of the on-chip bus wider.

Specifying a fixed width of bus means that, in many cases, the width of the bus is not optimal for the application. Therefore an approach has been adopted that enables flexibility of the width of bus but still ensures that modules are highly portable between designs.

The protocol allows the data bus to be 8, 16, 32, 64, 128, 256, 512, or 1024-bits wide. However, it is recommended that a minimum bus width of 32 bits is used. A maximum bus width of 256 bits is adequate for almost all applications.

For read and write transfers, the receiving module must select the data from the correct byte lane on the bus.   
Replication of data across all byte lanes is not required.

The following sections describe:

Implementing a narrow Subordinate on a wide bus

Implementing a wide Subordinate on a narrow bus on page 6-70

Implementing a Manager on a wide bus on page 6-70

## 6.3.1 Implementing a narrow Subordinate on a wide bus

Figure 6-2 shows how a Subordinate module that has been originally designed to operate with a 32-bit data bus can be converted to operate on a 64-bit bus. This only requires the addition of external logic, rather than any internal design changes, the technique is therefore applicable to hard macrocells.

![](images/1cac9304b4442f3a776519d41eb929a7a8a24539598bdc35aa93052f81e10fd8.jpg)  
Figure 6-2 Narrow Subordinate on a wide bus

For the output, when converting a narrow bus to a wider bus, do one of the following:

Replicate the data on both halves of the wide bus as Figure 6-2 shows.

Use additional logic to ensure that only the appropriate half of the bus is changed. This results in a reduction of power consumption.

A Subordinate can only accept transfers that are as wide as its natural interface. If a Manager attempts a transfer that is wider than the Subordinate can support, then the Subordinate can use the ERROR transfer response.

## 6.3.2 Implementing a wide Subordinate on a narrow bus

Predesigned or imported Subordinates can be adapted to work with a narrower data bus by using external logic.   
Figure 6-3 shows a wide Subordinate being implemented on a narrow bus.

![](images/7c21b17c155f45af4c56ddf316e40755dff77b6d5c49c6fc0d7bc6d5885d916e.jpg)  
Figure 6-3 Wide Subordinate on a narrow bus

## 6.3.3 Implementing a Manager on a wide bus

Managers can be modified to work on a wider bus than originally intended in the same way that the Subordinate is modified to work on a wider bus. Do this by:

Multiplexing the input bus.

Replicating the output bus.

Managers cannot work on a narrower bus than originally intended unless some mechanism is included in the Manager to limit the width of transfers that the Manager attempts. The Manager must never attempt a transfer where the width, as indicated by HSIZE, is wider than the data bus that it connects to.

# Chapter 7 Clock and Reset

This chapter describes the timing of the protocol clock and reset signals. It contains the following section: Clock and reset requirements on page 7-72

## 7.1 Clock and reset requirements

This section describes the requirements for implementing the HCLK and HRESETn signals.

## 7.1.1 Clock

Each component uses a single clock signal, HCLK. All input signals are sampled on the rising edge of HCLK. All output signal changes must occur after the rising edge of HCLK.

Signals that are described as being stable are required to remain at the same value when sampled at different rising clock edges in an extended transfer. However, it is possible that these signals can glitch after clock edges, returning to the same value as previously driven.

Note

It is possible to observe this behavior when using a typical synthesis design flow, where the control signals for an output multiplexor can change during an extended transfer, but they result in the same output value being used.

It is IMPLEMENTATION DEFINED whether an interface is glitch free between rising clock edges.

AHB5 defines the Stable\_Between\_Clock property. This property is defined to determine if an interface guarantees that signals that are required to be stable remain stable between rising clock edges.

If this property is True, it is guaranteed that signals that are required to be stable remain stable and glitch free between rising clock edges.

If this property is False, or is not defined, signals can glitch between rising clock edges.

## 7.1.2 Reset

The reset signal, HRESETn, is the only active LOW signal in the protocol and is the primary reset for all bus elements. The reset can be asserted asynchronously, but is deasserted synchronously after the rising edge of HCLK.

A component must define a minimum number of cycles for which the reset signal must be asserted to ensure that the component is fully reset and the outputs are at the required reset values.

During reset all Managers must ensure the address and control signals are at valid levels and that HTRANS[1:0] indicates IDLE.

During reset all Subordinates must ensure that HREADYOUT is HIGH.

# Chapter 8 Signal validity

This chapter describes the rules when signals must be valid in AMBA AHB. It contains the following sections:

Signal validity in AMBA AHB on page 8-74

Signal validity rules on page 8-75

## 8.1 Signal validity in AMBA AHB

When signals are not required to be valid they can take any value, but 0 or X is recommended. When a data transfer has invalid byte lanes, it is recommended that they are driven to 0. This ensures that there can be no leaking of data between transactions when invalid byte lanes are sampled.

## 8.2 Signal validity rules

The following signals must always be valid:

HTRANS

HADDR

HSEL

HMASTLOCK

HREADY

HREADYOUT

HRESP

The following signals must be valid when HTRANS is not IDLE:

HBURST

HPROT

HSIZE

HNONSEC

HEXCL

HMASTER

HWRITE

HAUSER

The following signals must be valid during the data phase of a write transaction:

HWDATA

HWSTRB

HWUSER

The following signals must be valid in the data phase of a write transaction when HREADY is HIGH and HRESP is LOW:

HEXOKAY

HBUSER

The following signals must be valid in the data phase of a read transaction when HREADY is HIGH and HRESP is LOW:

HRDATA

HEXOKAY

HRUSER

HBUSER

## Chapter 9 Atomicity

This chapter defines two atomic properties. It contains the following sections:

Single-copy atomicity size on page 9-78

Multi-copy atomicity on page 9-79

## 9.1 Single-copy atomicity size

The single-copy atomicity size defines the number of data bytes that a transfer is guaranteed to update atomically.

The single-copy atomicity size is defined for a group of components that are communicating. For example:

• A processor, DSP, and DRAM controller are in a 64-bit single-copy atomic group.

A larger group, including a processor, DSP, DMA, DRAM, SRAM, and peripherals are in a 32-bit single-copy atomic group.

A transfer never has a single-copy atomicity guarantee greater than the alignment of its start address. For example, a burst in a 64-bit single-copy atomic group that is not aligned to an 8-byte boundary does not have any 64-bit single-copy atomicity guarantee.

When a write transfer updates a memory location, it must be guaranteed that an observer will see either:

No update to the location.

An update to at least a single-copy atomicity size amount of data.

It is not permitted for another observer to see some data bytes updated within the single-copy atomicity size at one point in time, and then other data bytes within the same single-copy atomicity size at a later point in time.

Byte strobes associated with a transfer do not affect the single-copy atomicity size.

It is required that a transfer that is larger than the single-copy atomicity size must update memory in blocks of at least the single-copy atomicity size.

When determining the single-copy atomicity size, the exact instant when the data value is updated is not considered.   
What must be ensured is that no Manager can ever observe a partially updated form of the atomic data.

For example, in many systems data structures such as linked lists are made up of 32-bit atomic elements. An atomic update of one of these elements requires that the entire 32-bit value is updated at the same time. It is not acceptable for any Manager to observe an update of only 16-bits at one point in time, and then the update of the other 16-bits at a later point in time.

## 9.2 Multi-copy atomicity

AHB5 defines the Multi\_Copy\_Atomicity property. This property is defined to specify that a system provides multi-copy atomicity.

A system is defined as having this property if the Multi\_Copy\_Atomicity property is set to True.

A system that does not support the Multi\_Copy\_Atomicity property has the default value of False.

A system is defined as being multi-copy atomic if:

Writes to the same location are observed in the same order by all agents.

A write to a location that is observable by an agent, other than the issuer, is observable by all agents.

Multi-copy atomicity can be ensured by avoiding the use of forwarding buffers, which can make a transfer visible to some agents in a system, but not visible to all.

Additional requirements exist to ensure multi-copy atomicity in systems that include some form of hardware cache coherency. These additional requirements are not discussed in further detail in this specification.

# Chapter 10 Exclusive Transfers

This chapter describes the concept of Exclusive Transfers. It contains the following sections:

Introduction on page 10-82

Exclusive Access Monitor on page 10-83

Exclusive access signaling on page 10-84

Exclusive Transfer restrictions on page 10-85

## 10.1 Introduction

AHB5 defines the Exclusive\_Transfers property. This property defines whether an interface supports the concept of Exclusive Transfers. If this property is not defined, then the interface does not support Exclusive Transfers.

Exclusive Transfers provide a mechanism to support semaphore-type operations.

An Exclusive access sequence is a sequence of Exclusive Transfers from a single Manager that operate using the following steps:

1. Perform an Exclusive Read transfer from an address.

2. Calculate a new data value to store to that address that is based on the data value obtained from the Exclusive Read.

3. Between the Exclusive Read and the Exclusive Write, there can be other Non-exclusive transfers.

4. Perform an Exclusive Write transfer to the same address, with the new data value:

If no other Manager has written to that location since the Exclusive Read transfer, the Exclusive Write transfer is successful and updates memory.

If another Manager has written to that location since the Exclusive Read transfer, the Exclusive Write transfer is failed and the memory location is not updated.

5. The response to the Exclusive Write transfer indicates if the transfer was successful or if it failed.

This sequence ensures that the memory location is only updated if, at the point of the store to memory, the location still holds the same value that was used to calculate the new value to be written to the location.

If the Exclusive Write transfer fails, it is expected that the Manager will repeat the entire Exclusive access sequence.

It is IMPLEMENTATION DEFINED whether an update of the same, or overlapping, location by the same Manager after an Exclusive Read transfer will cause the associated Exclusive Write transfer to succeed or fail.

## 10.2 Exclusive Access Monitor

An Exclusive Access Monitor is required to support an Exclusive access sequence and this monitor must determine if an Exclusive Write transfer succeeds or fails.

The Exclusive Access Monitor must be capable of concurrently monitoring at least one address location for each Exclusive access capable Manager in the system.

The position of the Exclusive Access Monitor in the system is not defined. However, it must be positioned such that it can observe accesses to all address locations that are used for Exclusive access sequences. For example, if a system includes multiple memory controllers, either all accesses are routed through a central point that contains the Exclusive Access Monitor or a separate Exclusive Access Monitor is required at each memory controller.

It is not required that a system supports an Exclusive access sequence to all address locations. A fail-safe mechanism is provided for accesses to locations that do not support an Exclusive access sequence. Typically, it would be expected that a system would support Exclusive access sequences to main memory, but not to any peripheral device.

## 10.3 Exclusive access signaling

The additional signals associated with Exclusive Transfers are:

HEXCL Exclusive Transfer. Indicates that the transfer is part of an Exclusive access sequence. This signal is an address phase signal and has the same validity constraints as HADDR.

HMASTER[m:0] Manager Identifier. A Manager that has multiple Exclusive capable threads must generate this signal to differentiate between the threads.

The HMASTER value generated by the Manager will be combined with an interconnect generated value to ensure the resultant HMASTER value presented to the Exclusive Access Monitor is unique.

This signal is an address phase signal and has the same validity constraints as HADDR.

HEXOKAY Exclusive Okay. An additional response signal is added to indicate the success or failure of an Exclusive Transfer.

The width of the HMASTER[m:0] signal is IMPLEMENTATION DEFINED. However, the following widths are recommended:

For Manager components, implement the number of bits required for the number of Exclusive capable threads supported.

For an interconnect port where a Manager connects, implement 4-bits. Optionally, an interconnect can support a configuration of a larger bit width.

For a Subordinate or monitor component, implement 8-bits. Optionally, a Subordinate or monitor component can support a configuration of a larger bit width.

HMASTER signaling is permitted to be used for purposes other than Exclusive Transfers. It is permitted for the interconnect and Subordinate components in a system to use this signaling to distinguish between different Managers in the system and adapt their behavior appropriately. Therefore, a valid HMASTER indication must be provided for all transfers, not only Exclusive Transfers.

## 10.3.1 Response signaling

The HEXOKAY signal is used to indicate the success or failure of an Exclusive Transfer:

When asserted, HEXOKAY indicates that the Exclusive Transfer has been successful and for an Exclusive Write transfer the memory location has been updated.

When deasserted HEXOKAY indicates that the Exclusive Transfer has failed. This can be because either:

An Exclusive Transfer has been attempted to an address location that does not support Exclusive Transfers.

An Exclusive Write transfer has failed because the memory location has not remained unchanged since a matching Exclusive Read transfer. In this scenario, the memory location is not updated.

A Manager can ensure that it does not attempt to perform an Exclusive Write transfer to an address location that does not support Exclusive Transfers by ensuring that it always performs an Exclusive Read transfer to that location first.

The following constraints apply to HEXOKAY:

HEXOKAY must only be asserted in the same cycle as HREADY is asserted.

HEXOKAY can only be asserted in response to an Exclusive Transfer.

HEXOKAY must not be asserted in the same cycle as HRESP is asserted.

In a system where it can be determined that the location of an Exclusive Transfer will only be accessed by a single Manager, it is permitted for the Subordinate to always indicate that an Exclusive Transfer is successful, without the need to monitor whether another Manager has accessed the location.

## 10.4 Exclusive Transfer restrictions

The following restrictions apply to an Exclusive Transfer:

Must be a single beat transfer.

Must be indicated as burst type SINGLE or burst type INCR.

Must not include a BUSY transfer.

The address must be aligned to data size as indicated by HSIZE.

The value of the HPROT signals must guarantee that the Exclusive Access Monitor has visibility of the transfer.

Note

The HPROT signals must guarantee that the Exclusive Access Monitor has visibility of the transfer. If the Exclusive Access Monitor is located downstream of a system cache, then the transfer must be Non-cacheable. If the Exclusive Access Monitor is located upstream of a system cache, then it is permitted for the transfer to be Cacheable. If the Exclusive Access Monitor is downstream of a write buffer that might give an early write response, then the Exclusive transfer must be Non-bufferable.

For an Exclusive Read transfer and an Exclusive Write transfer to be considered part of the same Exclusive access sequence, the following signals must be the same for both transfers:

HADDR, Address

HSIZE, Data Size

HPROT, Protection Control

HBURST, Burst Type

HMASTER, Manager Identifier

HNONSEC, Non-secure, if applicable

It is permitted for a Manager to issue an Exclusive Read transfer and never follow it with an Exclusive Write transfer in the same Exclusive access sequence.

It is permitted for a Manager to issue an Exclusive Write transfer, which has not been preceded by an Exclusive Read transfer in the same Exclusive access sequence. In this case, the Exclusive Write transfer must fail and the HEXOKAY response signal must be deasserted.

A Manager must not have two Exclusive Transfers outstanding at the same point in time. The address phase of an Exclusive Transfer must not be issued while the data phase of an earlier Exclusive Transfer is in progress. This applies whether the transfers are part of the same Exclusive access sequence or not.

It is permitted for the address phase of an Exclusive Transfer with a particular HMASTER value to be issued while the data phase of an earlier Exclusive Transfer with a different HMASTER value is in progress.

The address phase of an Exclusive Transfer is defined as being when HEXCL is asserted and HTRANS indicates NONSEQ. The assertion of HEXCL when HTRANS indicates IDLE is not defined as the address phase of an Exclusive Transfer.

# Chapter 11 User Signaling

This chapter describes the set of optional user defined signals, on each channel, called the User signals. It contains the following sections:

User signal description on page 11-88

User signal interconnect recommendations on page 11-89

Note

Generally, it is recommended that the User signals are not used. The AHB protocol does not define the function of these signals and this can lead to interoperability issues if two components use the same User signals in an incompatible way.

## 11.1 User signal description

Table 11-1 lists the User signal names defined for each channel. Each User signal can have a different width.  
Table 11-1 User signal description
<table><tr><td>Signal</td><td>Source</td><td>Width</td><td>Description</td></tr><tr><td>HAUSER</td><td>Manager</td><td>USER REQ WIDTH</td><td>User-defined request attribute. USER REQWIDTH defines the width of HAUSER in bits. Recommended to be between 0 and 128 bits.</td></tr><tr><td>HWUSER</td><td>Manager</td><td>USER DATA WIDTH</td><td>User-defined write data attribute. USER DATA WIDTH defines the width of HWUSER in bits. Recommended to be between 0 and DATA WIDTH/2.</td></tr><tr><td>HRUSER</td><td>Subordinate</td><td>USER_DATA_WIDTH</td><td>User-defined read data attribute. USER DATA WIDTH defines the width of HRUSER in bits. Recommended to be between 0 and DATAWIDTH/2.</td></tr><tr><td>HBUSER</td><td>Subordinate</td><td>USER_RESP_WIDTH</td><td>User-defined response attribute. Used for both read and write transfers. USER RESP WIDTH defines the width of HBUSER in bits. Recommended to be between 0 and 16.</td></tr></table>

These signals have the same timing and validity requirements as the associated channel.

For data channel User signals, it is recommended that:

The number of User bits is an integer multiple of the width of the interface in bytes.

The User bits for each byte are packed together in adjacent bits.

The location of the User bits for a data channel is defined as:

Each data byte has m User signals associated with it.

The data bus width is n bytes.

The total number of User bits is u where u = m × n.

The User signals for byte y, where y = 0 ... (n – 1), are located at:

HWUSER[((y × m) + (m – 1)):(y × m)]

HRUSER[((y × m) + (m – 1)):(y × m)]

It is recommended to include User signals on an interconnect, however, there is no requirement to include them on Managers or Subordinates.

## 11.2 User signal interconnect recommendations

For transfers that are not modified by the interconnect, the User signals associated with the transfer can be transported across the interconnect unmodified.

For transfers that are modified by the interconnect, the information in this section provides guidelines for the generation of User signals associated with generated transfers.

The User signals protocol rules are:

The HAUSER signal must be valid during the address phase of a transfer.

The HAUSER signal must not change between cycles when HREADY is LOW, unless HRESP signal is ERROR.

The HWUSER signal must be valid during the data phase of a write transfer.

The HWUSER signal must not change between cycles of a write transfer when HREADY signal is LOW, unless HRESP signal is ERROR

The HRUSER signal must be valid during the data phase of a read transfer when HREADY signal is HIGH, unless HRESP signal is ERROR

The HBUSER signal must be valid during the data phase of a read or write transfer when HREADY signal is HIGH, unless HRESP signal is ERROR.

Where a single transfer is converted to multiple transfers:

The HAUSER signal of the original transfer is replicated into each generated transfer.

For each generated transfer that contains some of the data bytes of the original transfer, the HWUSER and HRUSER signals of the generated transfer use the User bits for the data bytes contained in the transfer.

Where multiple transfers are converted to a single transfer:

The HAUSER signal of the first transfer is used to generate the HAUSER signal of the generated transfer. The HAUSER signals of subsequent transfers are discarded.

The HWUSER and HRUSER signals for the generated transfer use the combined User bits for the associated data bytes in the original transfers.

## 11 User Signaling

11.2 User signal interconnect recommendations

# Chapter 12 Interface protection using parity

This chapter describes interface protection using parity and the parity check signals used in AMBA AHB. It contains the following sections:

Parity use in AMBA AHB on page 12-92

Configuration of interface protection on page 12-93

Byte parity check signals on page 12-94

Error detection behavior on page 12-95

Parity check signals on page 12-96

## 12.1 Parity use in AMBA AHB

For safety-critical applications, it is necessary to detect and possibly correct, transient, and functional errors on individual wires within an SoC.

An error in a system component can propagate and cause multiple errors within connected components. Error detection and correction (EDC) is required to operate end-to-end, covering all logic and wires from source to destination.

One way to implement end-to-end protection, is to employ customized EDC schemes in components and implement a simple error detection scheme between components.

Between these components there is no logic and single bit errors do not propagate to multi-bit errors. This section describes a parity scheme for detecting single-bit errors on the AMBA interface between components. Multi-bit errors can be detected if they occur in different parity signal groups. Figure 12-1 shows locations where parity can be used in AMBA AHB.

![](images/bef5263b187b2cd39674e2cc9509e67974c82cbf439544a0303cbca295255db9.jpg)  
Figure 12-1 Parity use in AMBA AHB

## 12.2 Configuration of interface protection

The protection scheme employed on an interface is defined by the property Check\_Type. The following Check\_Type values are defined:

False

No checking signals on the interface. If the Check\_Type property is not declared, it is considered to be False.

Odd\_Parity\_Byte\_All

Odd parity checking included for all signals. Each bit of the parity signal generally covers up to 8 bits.

## 12.3 Byte parity check signals

The following attributes are common to all the check signals added for byte parity interface protection:

Odd parity is used. Odd parity means that check signals are added to groups of signals on the interface and driven such that there is always an odd number of asserted bits in that group.

Parity signals covering data and payload are defined such that in most cases there are no more than 8 bits per group. This limitation assumes that there is a maximum of 3 logic levels available in the timing budget for generating each parity bit.

Parity signals covering critical control signals, which are likely to have a smaller timing budget available, are defined with a single parity bit. This single odd parity bit is the inversion of the original critical control signal.

For a check signal that is wider than 1 bit:

Check bit [n] corresponds to bits $[ ( 8 \mathrm { n } + 7 ) { : } 8 \mathrm { n } ]$ in the payload.

If the payload is not an integer number of bytes, the most significant bit of the check signal covers fewer than 8-bits in the most significant portion of the payload.

Check signals must be driven correctly in every cycle that the Check Enable term is True. For more information on parity check signals, see Table 12-1 on page 12-96.

Parity signals must be driven appropriate to all the bits in the associated payload, irrespective of whether those bits are actively used in the transfer. For example, all bits of HWDATACHK must be driven correctly, even if some byte lanes are not used on the transfer.

If none of the signals covered by a check signal are present on an interface, then the check signal is omitted from the interface.

If some of the signals covered by a check signal are not present on an interface, then the missing signals are assumed to be LOW.

## 12.4 Error detection behavior

This specification is not prescriptive regarding component or system behavior when a parity error is detected.   
Depending on the system and affected signals, a flipped bit can have a wide range of effects.

It might be harmless, cause performance issues, cause data corruption, cause security violations, or deadlock. The transaction response is independent of parity error detection.

When an error is detected, the receiver can do any of the following:

Terminate or propagate the transaction.

Correct the parity check signal or propagate the error.

• Update its memory or leave untouched.

Signal an error response through other means, for example with an interrupt.

## 12.5 Parity check signals

All of the following check signals are synchronous to HCLK and must be driven correctly in every cycle in which the Check Enable term is True.

Table 12-1 Parity check signals
<table><tr><td>Check signal</td><td>Signals covered</td><td>Check signal width</td><td>Granularity</td><td>Check enable</td></tr><tr><td>HTRANSCHK</td><td>HTRANS</td><td>1</td><td>2</td><td>HRESETn</td></tr><tr><td>HADDRCHK</td><td>HADDR</td><td>ceil(ADDR_WIDTH/8)</td><td>1-8</td><td>HRESETn</td></tr><tr><td>HCTRLCHK1</td><td>HBURST</td><td>1</td><td>4-9</td><td>HTRANS != IDLE</td></tr><tr><td></td><td>HMASTLOCK HWRITE HSIZE</td><td></td><td></td><td></td></tr><tr><td></td><td>HNONSEC</td><td></td><td></td><td></td></tr><tr><td>HCTRLCHK2</td><td>HEXCL HMASTER</td><td>1</td><td>2-9</td><td>HTRANS != IDLE</td></tr><tr><td>HPROTCHK</td><td>HPROT</td><td>1</td><td>4-7</td><td>HTRANS != IDLE</td></tr><tr><td>HWSTRBCHK</td><td>HWSTRB</td><td>ceil(DATA WIDTH/64)</td><td>1-8</td><td>Write data phase</td></tr><tr><td>HWDATACHK</td><td>HWDATA</td><td>DATA_WIDTH/8</td><td>8</td><td>Write data phase</td></tr><tr><td>HRDATACHK</td><td></td><td></td><td>8</td><td></td></tr><tr><td>HREADYOUTCHK</td><td>HRDATA</td><td>DATA WIDTH/8</td><td></td><td>Read data phase &amp; HREADY</td></tr><tr><td></td><td>HREADYOUT</td><td>1</td><td>1</td><td>HRESETn</td></tr><tr><td>HREADYCHK HRESPCHK</td><td>HREADY</td><td>1</td><td>1</td><td>HRESETn</td></tr><tr><td></td><td>HRESP HEXOKAY</td><td>1</td><td>1-2</td><td>Data phase</td></tr><tr><td>HSELxCHK</td><td>HSELx</td><td>1</td><td>1a</td><td>HRESETn</td></tr><tr><td>HAUSERCHK</td><td>HAUSER</td><td>ceil(USER_REQ_WIDTH/8)</td><td>1-8</td><td>HTRANS != IDLE</td></tr><tr><td>HRUSERCHK</td><td>HRUSER</td><td>ceil(USER_DATA_WIDTH/8)</td><td>1-8</td><td>Read data phase &amp; HREADY</td></tr><tr><td>HWUSERCHK</td><td>HWUSER</td><td>ceil(USER_DATA_WIDTH/8)</td><td>1-8</td><td>Write data phase</td></tr><tr><td>HBUSERCHK</td><td>HBUSER</td><td>ceil(USER_RESP_WIDTH/8)</td><td>1-8</td><td>Data phase &amp; HREADY</td></tr></table>

a. If a Subordinate has multiple HSEL inputs, there is a single HSELxCHK signal and the check granularity is greater than 1.

Note

The function ceil() returns the lowest integer value that is equal to or greater than the input to the function.

## Appendix A Signal matrix

This appendix lists all signals for AMBA AHB5 interfaces. This Appendix contains:

Signal matrix on page A-98

Check signal matrix on page A-100

## A.1 Signal matrix

The optional signals have a default value that should be used for any undriven inputs. The Manager column applies to an AHB Manager interface and interconnect Manager mirror interfaces. The Subordinate column applies to an AHB Subordinate interface and interconnect Subordinate mirror interfaces.

Table A-1 Key for Table A-2 and Table A-3
<table><tr><td>Code</td><td>Meaning</td></tr><tr><td>Y</td><td>Mandatory for inputs and outputs</td></tr><tr><td>N</td><td>Must not be present</td></tr><tr><td>0</td><td>Optional for inputs and outputs</td></tr><tr><td>C</td><td>Conditional, must be present if property is True</td></tr><tr><td>OC</td><td>Optional conditional, optional but can only be present if property is True</td></tr></table>

Table A-2 lists all AMBA AHB signals:

Table A-2 AMBA AHB signals
<table><tr><td>Signal</td><td>Width</td><td>Default</td><td>Presence Property</td><td>Manager</td><td>Subordinate</td></tr><tr><td>HCLK</td><td>1</td><td></td><td></td><td>Y</td><td>Y</td></tr><tr><td>HRESET</td><td>1</td><td></td><td></td><td>Y</td><td>Y</td></tr><tr><td>HADDR</td><td>ADDR_WIDTH</td><td>1</td><td></td><td>Y</td><td>Y</td></tr><tr><td>HBURST</td><td>3</td><td>0x1</td><td></td><td>0</td><td>0</td></tr><tr><td>HMASTLOCK</td><td>1</td><td>0b0</td><td></td><td>0</td><td>0</td></tr><tr><td>HPROT</td><td>HPROT_WIDTH</td><td>0x03</td><td></td><td>0</td><td>0</td></tr><tr><td>HSIZE</td><td>3</td><td>1</td><td></td><td>Y</td><td>Y</td></tr><tr><td>HNONSEC</td><td>1</td><td>0b0</td><td>Secure_Transfers</td><td>C</td><td>C</td></tr><tr><td>HEXCL</td><td>1</td><td>0b0</td><td>Exclusive_Transfers</td><td>C</td><td>C</td></tr><tr><td>HMASTER</td><td>HMASTER_WIDTH</td><td>0</td><td>Exclusive_Transfers</td><td>C</td><td>C</td></tr><tr><td>HTRANS</td><td>2</td><td></td><td></td><td>Y</td><td>Y</td></tr><tr><td>HWDATA</td><td>DATA_WIDTH</td><td></td><td></td><td>Y</td><td>Y</td></tr><tr><td>HWSTRB</td><td>DATA_WIDTH/8</td><td>All ones</td><td>Write_Strobes</td><td>C</td><td>C</td></tr><tr><td>HWRITE</td><td>1</td><td></td><td></td><td>Y</td><td>Y</td></tr><tr><td>HRDATA</td><td>DATA_WIDTH</td><td></td><td></td><td>Y</td><td>Y</td></tr><tr><td>HREADY</td><td>1</td><td></td><td></td><td>Y</td><td>Y</td></tr><tr><td>HREADYOUT</td><td>1</td><td></td><td></td><td>N</td><td>Y</td></tr><tr><td>HRESP</td><td>1</td><td></td><td></td><td>Y</td><td>Y</td></tr><tr><td>HEXOKAY</td><td>1</td><td></td><td>Exclusive_Transfers</td><td>C</td><td>C</td></tr><tr><td>HSELx</td><td>1</td><td>一</td><td>一</td><td>N</td><td>Y</td></tr><tr><td>HAUSER</td><td>USER_REQ_WIDTH</td><td></td><td>USER_REQ_WIDTH</td><td>OC</td><td>OC</td></tr><tr><td>HWUSER</td><td>USER DATA WIDTH</td><td></td><td>USER DATA WIDTH</td><td>OC</td><td>OC</td></tr><tr><td>HRUSER</td><td>USER DATA WIDTH</td><td>一</td><td>USER DATA WIDTH</td><td>OC</td><td>OC</td></tr><tr><td>HBUSER</td><td>USER_RESP_WIDTH</td><td>-</td><td>USER_RESP_WIDTH</td><td>OC</td><td>OC</td></tr></table>

## A.2 Check signal matrix

Table A-3 shows the protection signals that can be present on an interface, based on the value of the Check\_Type property. The Presence Property column indicates the property, which defines the presence of the signal, in addition to the Check\_Type property.

Table A-3 Check signal matrix
<table><tr><td>Signal</td><td>Width</td><td>Presence Property</td><td>Default</td><td>Manager</td><td>Subordinate</td></tr><tr><td>HTRANSCHK</td><td>1</td><td></td><td></td><td>C</td><td>C</td></tr><tr><td>HADDRCHK</td><td>ceil(ADDR_WIDTH/8)</td><td></td><td>一</td><td>C</td><td>C</td></tr><tr><td>HCTRLCHK1</td><td>1</td><td></td><td></td><td>C</td><td>C</td></tr><tr><td>HCTRLCHK2</td><td>1</td><td>Exclusive_Transfers</td><td>1</td><td>C</td><td>C</td></tr><tr><td>HPROTCHK</td><td>1</td><td>HPROT_WIDTH</td><td>1</td><td>OC</td><td>OC</td></tr><tr><td>HWSTRBCHK</td><td>ceil(DATA_WIDTH/64)</td><td>Write_Strobes</td><td></td><td>C</td><td>C</td></tr><tr><td>HWDATACHK</td><td>DATA WIDTH/8</td><td></td><td></td><td>C</td><td>C</td></tr><tr><td>HRDATACHK</td><td>DATA WIDTH/8</td><td></td><td></td><td>C</td><td>C</td></tr><tr><td>HREADYOUTCHK</td><td>1</td><td></td><td></td><td>N</td><td>C</td></tr><tr><td>HREADYCHK</td><td>1</td><td></td><td></td><td>C</td><td>C</td></tr><tr><td>HRESPCHK</td><td>1</td><td></td><td></td><td>C</td><td>C</td></tr><tr><td>HSELxCHK</td><td>1</td><td></td><td></td><td>N</td><td>C</td></tr><tr><td>HAUSERCHK</td><td>ceil(USER_REQ_WIDTH/8)</td><td>USER_REQ_WIDTH</td><td></td><td>C</td><td>C</td></tr><tr><td>HRUSERCHK</td><td>ceil(USER_DATA_WIDTH/8)</td><td>USER_DATA_WIDTH</td><td></td><td>C</td><td>C</td></tr><tr><td>HWUSERCHK</td><td>ceil(USER_DATA_WIDTH/8)</td><td>USER_DATA_WIDTH</td><td></td><td>C</td><td>C</td></tr><tr><td>HBUSERCHK</td><td>ceil(USER_RESP_WIDTH/8)</td><td>USER RESP WIDTH</td><td></td><td>C</td><td>C</td></tr></table>

Appendix B Revisions

This appendix describes the technical changes between released issues of this specification.

Table B-1 Issue A
<table><tr><td>Change</td><td>Location Affects</td><td></td></tr><tr><td>First release.</td><td></td><td></td></tr></table>

Table B-2 Differences between issue A and issue B
<table><tr><td>Change</td><td>Location</td><td>Affects</td></tr><tr><td>Additional section describing revisions, which include new properties, clarifications and recommendations.</td><td>AMBA AHB revisions on page 1-17.</td><td>All revisions</td></tr><tr><td>Clarification of the HPROT[3:0] protection control signal.</td><td>Manager signals on page 2-21.</td><td>All revisions</td></tr><tr><td>Additional table entry for the HPROT[6:4] signal that adds extended memory types. Applicable only to Issue B of this specification.</td><td>Manager signals on page 2-21.</td><td>All revisions</td></tr><tr><td>Additional table entry for the HNONSEC signal required for Secure transfers.</td><td>Manager signals on page 2-21.</td><td>All revisions</td></tr><tr><td>Additional table entries for the HEXCL and HMASTER[3:0] signals required for Exclusive Transfers.</td><td>Manager signals on page 2-21</td><td>All revisions</td></tr><tr><td>Additional table entry describing the HEXOKAY signal required for Exclusive Transfers.</td><td>Subordinate signals on page 2-23.</td><td>All revisions</td></tr><tr><td>Additional details on the use of HMASTLOCK for IDLE transfers.</td><td>Locked transfers on page 3-32.</td><td>All revisions</td></tr><tr><td>Additional section that describes AHB5 Extended Memory Types.</td><td>Memory types on page 3-46.</td><td>All revisions</td></tr><tr><td>Additional section that describes AHB5 Secure Transfers.</td><td>Secure transfers on page 3-51.</td><td>All revisions</td></tr><tr><td>Additional section that describes AHB5 Multiple Subordinate Select.</td><td>Multiple Subordinate select on page 4-55.</td><td>All revisions</td></tr><tr><td>Additional section that describes the AHB5 Endian property.</td><td>Endianness on page 6-65.</td><td>All revisions</td></tr><tr><td>Additional chapter that describes AHB5 Exclusive Transfers.</td><td>Chapter 10 Exclusive Transfers.</td><td>All revisions</td></tr><tr><td>Additional section that describes the AHB5 Stable_Between_Clock property.</td><td>Clock on page 7-72.</td><td>All revisions</td></tr><tr><td>Additional chapter that describes AHB5 Atomicity.</td><td>Chapter 9 Atomicity.</td><td>All revisions</td></tr><tr><td>Additional chapter that describes the optional user defined signals on each channel called the User signals.</td><td>Chapter 11 User Signaling.</td><td>All revisions</td></tr></table>

Table B-3 Differences between issue B and issue C
<table><tr><td>Change</td><td>Location</td></tr><tr><td>Additional details describing new signal width properties, including clarifications and recommendations.</td><td>Manager signals on page 2-21. Subordinate signals on page 2-23.</td></tr><tr><td></td><td>Decoder signals on page 2-24. Multiplexor signals on page 2-25.</td></tr><tr><td>Additional details for locked sequence. New section describing Write strobes feature, including information on</td><td>Locked transfers on page 3-32. Write strobes signaling on page 3-34.</td></tr><tr><td>Write strobe signaling, rules, and interoperability Additional chapter that describes the signal validity rules in AMBA</td><td></td></tr><tr><td>AHB5.</td><td>Chapter 8 Signal validity.</td></tr><tr><td>Additional details on response signaling. New table for User signals describing signal width properties,</td><td>Response signaling on page 10-84. User signal description on page 11-88</td></tr><tr><td>clarification, and recommendations.</td><td></td></tr><tr><td>Additional details on User signals rules Additional chapter that describes interface protection using parity and</td><td>User signal interconnect recommendations on page 11-89. Chapter 12 Interface protection using parity.</td></tr><tr><td>the parity check signals used in AMBA AHB, including configuration of interface protection and error detection behavior.</td><td></td></tr><tr><td>Additional appendix that lists all signals for AMBA AHB5 interfaces.</td><td>Appendix A Signal matrix.</td></tr><tr><td>Terminology update. Regularized terminology to use Manager to indicate the agent that initiates transactions and Subordinate to indicate</td><td>Throughout the specification.</td></tr></table>

## Glossary

This glossary describes some of the technical terms used in AMBA AHB documentation.

AHB An AMBA bus protocol that defines the interface between system components, including Managers, interconnects, and Subordinates. AMBA AHB supports high clock frequency, single clock-edge operation, burst transfers, and non-tristate implementation. It can support wide data bus configurations.

See also AHB-Lite.

AHB-Lite A subset of the full AMBA AHB protocol specification. It provides all of the basic functions required by the majority of AMBA AHB Subordinate and Manager designs, particularly when used with a multi-layer AMBA interconnect.

Aligned A data item stored at an address that is exactly divisible by the highest power of 2 that divides exactly into its size in bytes. Aligned halfwords, words, and doublewords therefore have addresses that are divisible by 2, 4, and 8 respectively.

APB An AMBA bus protocol for ancillary or general-purpose peripherals such as timers, interrupt controllers, UARTs, and I/O ports. Using APB to connect to the main system bus through a system-to-peripheral bus bridge can help reduce system power consumption.

AXI An AMBA bus protocol that supports:

Separate phases for address or control and data.

Unaligned data transfers using byte lane strobes.

Burst-based transactions with only the start address issued.

Separate read and write data channels.

Issuing multiple outstanding addresses.

Out-of-order transaction completion.

• Optional addition of register stages to meet timing or repropagation requirements.

The AXI protocol includes optional signaling extensions for low-power operation.

<table><tr><td>Beat</td><td>An alternative term for an individual transfer within a burst. For example, in AMBA AHB, an INCR4 burst comprises four beats.</td></tr><tr><td></td><td>See also Burst.</td></tr><tr><td rowspan="3">Burst</td><td>A group of transfers to consecutive addresses. In an AMBA protocol, a burst is controlled by signals that indicate</td></tr><tr><td>the length of the burst and how the address is incremented.</td></tr><tr><td>See also Beat.</td></tr><tr><td>Doubleword Endianness</td><td>A 64-bit data item. Doublewords are normally at least word-aligned in Arm systems. The scheme that determines the order of successive bytes of data in a data structure when that structure is stored in</td></tr><tr><td rowspan="2"></td><td>memory.</td></tr><tr><td>See also Little-endian and Big-endian.</td></tr><tr><td>Halfword</td><td>A 16-bit data item. Halfwords are normally halfword-aligned in Arm systems.</td></tr><tr><td>Processor</td><td>A general term for an entity that performs processing.</td></tr><tr><td>Word</td><td>A 32-bit data item. Words are normally word-aligned in Arm systems.</td></tr></table>