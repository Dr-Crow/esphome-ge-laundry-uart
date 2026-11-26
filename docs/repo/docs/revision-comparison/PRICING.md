# Recorded assembly quotes

Latest October5 pre-order analysis and committed fixes: [all-revision review](preorder-2026-10-05/README.md). Earlier checkpoint/quote/source boundaries below remain explicit.

[Comparison](README.md) · [Validation](VALIDATION.md) · [Finish plan](FINISH-PLAN.md)

All prices are USD. The selected exact Rev3C quotes refreshed October 5, 2026 at 02:47 UTC and the historical October 3 baseline quotes are complete PCB plus Economic top-side assembly for **all five or all ten carriers**, with exact reference/part-code matching at both quantities. Shipping, tax, XIAO modules and module-side headers/installation, programming, functional tests, enclosures and appliance cables are excluded. No order has been placed.

## Current STPS140Z Rev3C quote

Fresh October 5 quotes at 17:53/17:55 UTC match the three files from published `bf5c2318b4c9ee775c19f7b9327cd1a8fea02d27`, including STPS140Z/C155662 D14/D15. All 83 references/34 codes match, with no shortage warnings, substitutions or omissions. [Source/hash receipt](../../pcb/rev3c/validation/JLCPCB-ST-QUOTE-2026-10-05.json) and [illustrated ordering guide](../../pcb/rev3c/ORDERING.md) preserve the exact files/settings.

| USD subtotal | Five assembled carriers | Ten assembled carriers |
| --- | ---: | ---: |
| PCB | 29.81 | 36.07 |
| Economic PCBA | 106.00 | 135.13 |
| **Complete carrier total** | **135.81** | **171.20** |
| Difference from pre-ST quote | +1.17 | +2.28 |

The diode repair adds about $0.23 per carrier under these settings. Modules, module headers, case, programming/tests, shipping and tax are excluded. Stock is not reserved; a quote does not approve new-part pose, solder joints, process or electrical/physical readiness. Current-ST A/B outcomes are recorded below; their earlier snapshots remain historical.

## Historical pre-ST Rev3C and original baseline

| Matched factory source | References / unique purchasing groups | Five carriers | Ten carriers |
| --- | ---: | ---: | ---: |
| Historical pre-ST corrected trio, integration `2d5a42cc7a9440aef784fe827d0e25690bb74bfd` | 83 / 34 | **$134.64** | **$168.92** |
| Historical baseline `ca1fdb1261af8b32a1bf353d37f40439ead5c3b0` | 80 / 33 | $130.39 | $160.37 |
| Difference from historical baseline | | **$4.25** | **$8.55** |

The premium is approximately $0.85 per carrier. Restored source `5542734` adds source-preserving partial C3/C6 models and quote documentation. Current selected source `b87d3e8` additionally disables unwanted drill-marker plotting and regenerates the Gerber ZIP; BOM/CPL are unchanged. The October 5, 02:47 UTC [fresh quote receipt](../../pcb/rev3c/validation/JLCPCB-QUOTE-2026-10-05.json) verifies this corrected ZIP and matching BOM/CPL. All 83 references/34 parts matched without shortage warnings or substitutions; stock is not reserved. This pre-ST quote is compared with an October 3 baseline snapshot, rather than a new simultaneous baseline quote. The previously quoted factory trio is the corrected J1 body-datum package at `b53cfca`; all 83 exact codes matched and were stocked at both quantities in the 04:16 refresh. The earlier `7bb455f` CPL is historical; do not use it as the current placement file. The 80-reference baseline changed only D16/D17 sourcing to reviewed MCC C668891; its original TPS22810 switches, fuses and topology remain. It is a historical price comparison, not the selected design.

| Included subtotal | Selected, five | Selected, ten | Baseline, five | Baseline, ten |
| --- | ---: | ---: | ---: | ---: |
| PCB | 29.81 | 36.07 | 29.81 | 36.07 |
| PCBA | 104.83 | 132.85 | 100.58 | 124.30 |
| Components within PCBA | 34.18 | 58.71 | 30.02 | 50.36 |
| Extended-part fees within PCBA | 52.53 | 52.53 | 52.53 | 52.53 |

PCBA also includes setup, stencil, SMT, hand-soldering, manual assembly and nitrogen reflow. Rounded lines are not substitutes for the supplier's total. The quote includes J1 RJ45 and J5/J6 female sockets with no unapproved omissions or substitutions.

Observed settings were FR-4 TG135, four layers, 99 × 40 mm, 1.6 mm, green mask, white silkscreen, lead-free HASL and 1 oz copper on both inner and outer layers. The native export job reports 35 µm on all layers; that metadata has not established a mandatory electrical stackup. A 0.5 oz inner comparison needs a separately evaluated variant. Supplier 2D and 3D placeholders did not establish actual body/pad/pin 1 alignment or physical approval, even with the corrected CPL. Rev3B's exact 85-reference quote is blocked by U2 C18212168 stock at both quantities; no omission was approved.

The illustrated `pcb/rev3c/ORDERING.md` in the selected candidate records the actual screenshots, steps and SHA-256 hashes of each matched Gerber/BOM/CPL trio. Familiar filenames alone are insufficient. Keep the 83-reference trio together; never mix it with the 80-reference baseline. Refresh exact stock, process review, shipping/tax and total after qualification and before any later order approval.

## Current ST-parts Rev3A/B outcomes

| Published bf5c231 factory scope | References / codes | Five | Ten | Result |
| --- | ---: | ---: | ---: | --- |
| Rev3A, 88.7 × 40 mm, integrated WROOM and connectors included | 97 / 42 | **$180.08** | **$230.15** | All exact refs available; no omissions/substitutions |
| Rev3B, 99 × 40 mm, soldered XIAO C3 required | 85 / 35 | Full assembly unavailable | Full assembly unavailable | Sole shortage U2 C18212168/113991054: zero stock, short five/ten |

A's PCB/PCBA split is $29.79/$150.29 at five and $36.03/$194.12 at ten. [A source-hash receipt](../../pcb/rev3a/validation/JLCPCB-ST-QUOTE-2026-10-05.json) preserves the actual detected outline and 97 code matches. Its J4 solder delivery/inspection/retention, supplier pose and all electrical/physical gates remain open.

B's other 84 refs are available and selected, with all 85 source codes matching. [B stock-blocked receipt](../../pcb/rev3b/validation/JLCPCB-ST-QUOTE-2026-10-05.json) records bare PCB $29.81/five and $36.07/ten; these are **not assembled totals**. No required module was omitted. External exact-module vendors remain an option subject to lot, consignment and assembly review; C6 is not a soldered B drop-in. All values are USD before shipping/tax, stock is not reserved, and no order or release approval follows.

## Earlier Rev3A/B snapshots before ST repair

| Historical exact source | References / priced groups | Five | Ten | Scope |
| --- | ---: | ---: | ---: | --- |
| Rev3A factory trio `a5ab243` | 97 /42 | **$178.90** | **$227.86** | Includes integrated C3 and connectors; shipping, tax, case/programming/tests excluded |
| Rev3B October 4 snapshot | 85 | Unavailable | Unavailable | Exact U2 C18212168 shortage; no omission accepted |

A's one-reference-per-row BOM is component-equivalent to its native 49-row grouping and clears the supplier import warning. Its schematic-only0-warning cleanup preserves the quoted factory trio. J4's recessed shell legs/no paste aperture still require assembler-approved solder delivery, inspection and retention. Placeholder supplier views do not approve placement. The C carrier quotes exclude XIAO modules; compare that scope before comparing totals.

## Historical architecture quotes

These earlier snapshots price the original source architectures, not the current repairs or the new Rev3A/B protection sources. Each is a batch of five, with all five quoted carriers assembled.

| Revision / scope | Quote date | Historical total | Per carrier |
| --- | --- | ---: | ---: |
| Rev2.2 assembled board | September 19, 2026 | $78.07 | $15.61 |
| Original Rev3A, including integrated processor | October 1, 2026 | $154.44 | $30.89 |
| Original Rev3B carrier, XIAO/installation excluded | October 1, 2026 | $112.08 | $22.42, incomplete |
| Original Rev3C carrier, sockets included | October 1, 2026 | $114.65 | $22.93 |
| Original Rev3C plus five $5.99 retail C3 modules | October 1, 2026 | $144.60 | $28.92 |

Original Rev3C's quote came from `163c98f`; public head `38d94d3` added case-alignment/quote documentation. Its 82-reference/33-group scope differs from the selected 83-reference source. Rev3A's original quote included 93 placements/40 purchasing groups. Rev3B deliberately excluded module, antenna and soldering because a complete module batch was unavailable at that time. Adding a retail module price does not establish an installed factory quote.

The October 1 retail snapshots were $5.99 for [pre-headered C3, SKU 102010633](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32C3-Pre-Soldered-p-6331.html) and $6.20 for [pre-headered C6, SKU 102010636](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32C6-Pre-Soldered-p-6328.html). They are historical module-only prices, not current stock or complete adapter quotes. No delivered cost, printed case cost or appliance compatibility has been established against the $39.99 FirstBuild comparison target.
