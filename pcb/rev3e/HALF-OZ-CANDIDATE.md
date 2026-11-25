# Rev 3E half-ounce inner copper candidate

**Status: quote and engineering review only.** Candidate E-LC-A changes only the fabrication stackup request. No CAD, routing, drill, paste, protection, firmware, BOM, CPL, or enclosure change. An independently qualified assembly file set is required before ordering. Do not reuse the current quote as evidence for a different stencil or artifact set.

| Parameter | Reference | E-LC-A |
| --- | --- | --- |
| Outline and thickness | 99 × 40 mm; nominal 1.6 mm | Same |
| Layer count, finished exterior copper | Four; 1 oz outer | Same |
| Inner copper | 1 oz in reference quote | 0.5 oz both inner layers, subject to exact JLCPCB build option |
| All other quote options | Five boards, top-side Economic; compare same finish, lead time, and shipping | Same |
| Manufacturing subtotal | $94.22 verified | $77.51 if the $16.71 option is the only change; not yet requoted |

The inspected Rev 3E CAD board has no explicit stackup block. Four copper layers and 1.6 mm board thickness are in CAD, but the quoted 1 oz inner thickness is a fabrication option, not a component requirement inferred from the board file. Confirm actual finished copper, dielectric stack, and finished thickness with the fabricator. Do not change to two layers or thin the outer copper in this experiment. [JLCPCB copper weights](https://jlcpcb.com/help/article/jlcpcb-copper-weight).

## Route audit, not a thermal qualification

Inspected the retained Rev 3E preflight board, SHA-256 `af5ac25f2d90386e9839136fdb6057eabe55a13371bffb57a84a7091d8325ffc`. Ground pours exist on all four layers. The protected `/V_INPUT` path and buck switch node route on the front. The VDC entry has a measurable inner-layer series run: J1 pin 1 to the front-layer transition near (40.377, 8.4902), length 29.758 mm at 0.50 mm on In2. At nominal 20 °C bulk copper this one span is roughly 29 mΩ with 35 µm foil or 59 mΩ with 17.5 µm foil; sensitivity at 0.40 A is roughly 12 mV additional drop. This is not measured current, a full path model, or a low-voltage pass. Actual copper, temperature, vias, neckdowns and the port harness can change the result. The board also has 0.50 mm inner routes on +5 V and +3.3 V; trace them to loads before assuming they carry full module current. The conspicuous 14.8 mm × 0.20 mm `/BUCK_5V` inner run connects U8 pad 1 (FB) to the output-capacitor node; do not count it as a series power bottleneck or widen it blindly.

[TI TPS25947 §8.4](https://www.ti.com/lit/ds/symlink/tps25947.pdf) calls for short, adequately sized current paths, quiet local ground, and top/bottom heat-spreading copper with vias; no specific 1 oz inner requirement was found in that section. [Diodes AP63205 layout guidance](https://www.diodes.com/assets/Datasheets/AP63200-AP63201-AP63203-AP63205.pdf) recommends 2 oz **top and bottom** for its 2 A thermal case, plus bottom ground and capacitor ground vias. The current quote already uses 1 oz exterior; don't claim this board is qualified at the converter rating. Retain outer copper and ground coverage. Validate low-input headroom and temperature at the **actual adapter load**, not the headline IC ratings.

## Acceptance and second lever

1. Quote the exact stackup A/B with identical manufacturing inputs, confirm fee and factory CAM stack. Start with unchanged geometry so the comparison is attributable to foil thickness.
2. Review the input and rail paths layer by layer, including the other input, returns, via neckdowns and actual output loading. If needed, widen the J1 VDC run toward 1.0 mm where clearance permits (roughly restores the nominal width × thickness of the current 0.50 mm at 1 oz) or route a short equivalent outer/parallel path. Preserve clearance, antenna cutouts and quiet/switching return geometry. Re-run native ERC and DRC/parity plus fabrication comparison after layout edits.
3. Compare first articles on isolated current-limited fixture: loaded PIN1 and PIN3 cold boot, input handoff and rail sag, C3/C6 radio bursts, and eFuse/buck heating at intended hottest ambient. Keep the 1 oz reference until the lower-cost build shows sufficient margin.
4. Separately try fee-free component changes as E-LC-B only after a live fee/stock check and datasheet/footprint review. Screen L1 and other discrete passives first; existing C9 and U4/U5 sourced alternates are also Extended. Do not silently change the eFuses, TVSs, buck, and sockets. See [quote cost review](QUOTE-AND-COST-REVIEW.md) for the fee ledger.
