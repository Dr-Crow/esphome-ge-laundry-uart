# Rev3B bounded rated-protection backport

This prototype backports the selected Rev3C protection circuit from `fafd3eab5a8a8465697e1557bb075d88f85be9d9` (electrical candidate `7bb455fbc85c748f3125ed091a54375de69fbbcc`) onto frozen Rev3B `0b957ba996e7e7a86f8776c9289b6cfb634421ee`. It is a separate branch. The frozen B/C source and quote folders remain unchanged. It is not appliance-qualified, ready to order, a 40 V carrier specification or a correction for an observed GE field failure.

## Exact bounded change

Both original paths remain: J1.1 → F2 → Q3 → U9 → D14 → V_INPUT, and J1.3 → F1 → Q4 → U10 → D15 → V_INPUT. Original Q5/R35/R37 sense PIN1_PROTECTED and inhibit U10; R36 enables PIN3 from its own source when PIN1 is absent. Presence priority remains, including weak/faulting PIN1's ability to inhibit PIN3. No new fallback behavior or reduced input envelope is asserted.

- Q3/Q4 source/drain orientation is corrected; each drain goes to its fused input and source to its protected node. Source-referenced D16/D17 become exact MCC BZT52C12-TP / C668891. R31/R32 retain 5.1 kΩ but connect to GND; C18/C19 retain 100 pF/50 V C0G across source and bias. R33/R34 retain 51 Ω from bias to actual gate.
- F1/F2 become exact Littelfuse 1812L075/33DR / C151170, 0.75 A hold/1.5 A trip at 20°C, with manufacturer's 1.78 × 3.15 mm pads and 3.45 mm inner gap. Their centers move 1.5 mm right, with only local clearance routes adjusted.
- U9/U10 become exact TI TPS1H200AQDGNRQ1 / C2653785. Pin mapping: VS8, OUT7, IN1, DIAG_EN2, FAULT3, CL4, DELAY5, GND6, EP9. DIAG_EN/GND/EP are GND; FAULT is NC. U9 IN follows its own VS; U10 IN preserves PIN1-presence priority.
- C22/C23 are removed. R38/R39 are UNI-ROYAL 0603WAF3301T5E / C22978, 3.3 kΩ ±1%, from CL to GND. R40/R41 are UNI-ROYAL 0805W8F1003T5E / C149504, 100 kΩ ±1%, from each branch's own VS to DELAY. The former CT ramp is not a drop-in equivalent.
- D20 adds SUNMATE SMF16A / C399290 from PIN3_PROTECTED to GND, matching original D18 upstream of current limiting.

The soldered Seeed XIAO ESP32-C3 U2, its 22 carrier pad functions/geometry, USB behavior, recovery J2/D19, LEDs, JP1, 99 × 40 mm outline, mounting/interface positions, case sources, AP63205 buck, downstream diodes and all firmware remain. No C6 compatibility is claimed for Rev3B. No module, regulator or USB circuitry is substituted.

## Manufacturer lands and local rule

The project-local TI footprint follows [TI TPS1H200A-Q1 Rev E, May 2026](https://www.ti.com/lit/ds/symlink/tps1h200a-q1.pdf), DGN0008K-C01 pp28–29: 1.4 × 0.45 mm lead pads, 0.65 mm pitch and 4.4 mm row spacing. Adjacent copper gap is intrinsically 0.20 mm. EP copper is 2 × 3 mm; mask/paste aperture is 1.57 × 1.89 mm. One full aperture follows TI's 0.125 mm stencil example. Optional under-paste vias are omitted; external 0.8/0.4 mm ground vias remain outside the exposed pad.

Two rules permit 0.20 mm pad-to-pad clearance only within the same U9 or same U10 footprint. All global, Power and Switching class settings, tracks, vias and other footprints retain frozen B constraints. This approved vendor-land exception does not establish universal insulation or environmental compliance. Final stencil/process, ≥85% EP solder coverage, contamination/coating and thermal performance remain gates. New TI/PPTC STEP models are approximate maximum drawing envelopes, not authenticated vendor CAD. Existing connector/module envelopes and case boundaries remain.

## Current and startup bounds

Nominal ICL = 2000/3300 = 0.606 A. TI's conditional ±15% and resistor ±1% give approximately 0.510–0.704 A. Accuracy requires VS−OUT ≥2.5 V and the stated setting range; this is not an OEM allowance or unconditional draw ceiling. ±100 ppm/K resistor drift widens the estimate to about 0.507–0.708 A at 85°C or 0.504–0.713 A at 150°C. CL resistor dissipation at nominal 0.8 V is about 0.194 mW; resistor rating is 100 mW through 70°C, derating to zero at 155°C.

Continued limiting gives 35–45 ms on / 0.8–1.2 s off (40 ms/1 s typical), specified by design rather than production tested. Thermal interruption can change an attempt. The illustrative unloaded minimum charge budget is 0.510 A ×35 ms ≈17.9 mC. Retained switch-output plus buck-input nominal capacitance is about 10.2 µF; buck startup, its 44 µF output, module/carrier capacitors, RF load and source impedance must also be included. Local VS must remain above the maximum 4 V restart threshold. Repeated startup resets remain possible.

At 364 mA, a mixed-condition illustration using PPTC room-temperature R1max, CJ3407's 25°C 0.087 Ω and hot switch limits increases fuse+PMOS+switch drop from about 237 to 323 mV, approximately 86 mV. TPS1H200's 400 mΩ maximum is at 150°C; its 5 mA active-supply maximum uses VS13.5 V/IN5 V/0.5 A load. Neither is a guaranteed complete hot budget. This added loss is upstream of the buck. Both nominal-5 V input branches' loaded startup and module 5V/3V3 margins remain open; see [POWER-QUALIFICATION.md](POWER-QUALIFICATION.md).

## Whole-chain protection gates

Nominal 5/7.5/9/13.6 V intended examples remain; no narrowed envelope is used to force a pass. Source current/tolerance and waveforms are unknown. SMF16A's 26 V maximum clamp is at 7.7 A, 10/1000 µs and 25°C, not all pulse/temperature conditions. TI's 40 V rating addresses the former switch mismatch for that bounded positive-pulse comparison only.

Retained CJ3407 requires |VDS| <30 V and |VGS| <20 V with margin; AP63205 stays within 32 V operating maximum, rather than targeting 35 V absolute maximum. The 33 V PPTCs require their own differential-voltage bound; a downstream clamp does not bound raw connector voltage or voltage across a tripped fuse. A charged 26 V protected node followed by −13.6 V at the PMOS drain creates 39.6 V differential, beyond the retained PMOS. Reverse charged steps remain gated.

Switch CL does not limit upstream TVS current. PPTC maximum 0.20 s trip at 8 A does not prove that a 200 W, 10/1000 µs SMF survives sustained overvoltage until trip. Bound source impedance/current, fault energy/duration, pulse repetition and recovery. Reference PPTC holds of 0.47 A at 70°C/0.36 A at 85°C are not enclosed-board allowances. D14/D15 duty and thermal limits remain independent.

## Source-bound procurement and cost

Exact identities are retained from the selected C source and primary sheets: [Littelfuse 1812L](https://www.littelfuse.com/assetdocs/resettable-ptcs-1812l-datasheet?assetguid=ca5c80cb-504e-4a8a-8e74-0107520a1717), [MCC BZT52](https://www.mouser.com/datasheet/2/258/BZT52C2V4_7eBZT52C75_500mW__SOD_123_-2904721.pdf), [SUNMATE SMF16A](https://jlcpcb.com/api/file/downloadByFileSystemAccessId/8757789523080564736), [Royal Ohm resistors](https://www.royalohm.com/assets/pdf/products/smd/1.pdf), [JLC C22978](https://jlcpcb.com/partdetail/23705-0603WAF3301T5E/C22978), [C149504](https://jlcpcb.com/partdetail/C149504), [C668891](https://jlcpcb.com/partdetail/C668891).

The October 3 C sourcing snapshot reported C149504 Basic, 4,204,330 stock and USD0.0059 at1; C668891 Extended/MSL1, 48,100 stock/47,040 available and USD0.0277 at1. These inherited exact-SKU observations are dated snapshots, not fresh B procurement promises. The C comparison's two-switch/two-fuse/two-TVS selected-part estimate was about +USD0.91 per board at compared small tiers /+USD0.69 at compared100-piece tiers. It excludes CL/retry resistors, zener change, capacitor credits and process fees. It is applicable only to those selected parts, not a complete Rev3B cost.

Rev3B gains three fitted parts net (82 →85). Switches, fuses and MCC zeners are Extended; CL/retry passives are Basic in the cited snapshot. Selected C complete five/ten-carrier quotes do not transfer to B's soldered module, recovery header and assembly. A fresh exact 85-reference B quote, module procurement/antenna installation, stock, assembly fees, shipping and tax remain open. No quotes are changed and no order is placed.

## Native evidence

[Current source proof](validation/rated-protection-proof.json) records 103 schematic items, 102 PCB footprints, 257 pin nets, 222 unchanged original pin nets, 85 matching fitted BOM/CPL references, 109 removed/163 added track/via objects within x39.9125–77.0 / y2.0–33.0099 mm, with all 621 retained objects unchanged. Direct module signal and named GE connector routes retain their original objects and all unaffected pin nets remain identical. Fuse clearance requires enumerated +3V3 and intermediate D9/U4.1 receive-clamp detours; the latter is part of the GE signal path. Native KiCad 9.0.9 all-severity ERC and all-track/parity DRC report zero errors, warnings, exclusions, unconnected items and parity differences. The refreshed factory ZIP has 11 Gerbers, two separate drills and one job file. Separate drill maps, schematic PDF, four copper plots and top/bottom/oblique renders are refreshed and inspected as actual pixels. These are source/assembly review evidence, not electrical, thermal, environmental or physical qualification.

## Independent copper and ground-fill review

The [independent review](validation/INDEPENDENT-BACKPORT-REVIEW.md) confirms the circuit, component identities, interfaces, native results and exact source/BOM/CPL/export hash pairing. Its source binding is electrical implementation commit `5742253a1c95fb51b91638f57c5ae9ecab88c385`; this documentation correction changes no CAD or manufacturing bytes.

The +3V3 detour replaces three F.Cu 0.5 mm segments with a 0.3 mm route and two vias through B.Cu. Four original Net-(D9-K2) segments become six segments and two vias through In2.Cu; this is an intermediate half-duplex receive/clamp connection to U4.1. Their original connected pins are unchanged, but these are actual signal/power routing changes requiring physical return-path and signal review.

All four zone definitions remain identical. Regenerated fill has F.Cu XOR about358.269 mm² (233.259 removed /125.011 added); B.Cu/In1.Cu/In2.Cu XOR about86.875/29.284/48.339 mm². Most substantial change follows the power work, while F.Cu refill also changes1.618 mm² left of x39 and removes24.990 mm² right of x77, reaching x85.467. Other-layer changes outside x39–77 are microscopic coordinate/Boolean residues, not evidence of large edits. Thus filled-copper preservation is narrower than a claim that all physical change stays within the track-object rectangle.

U2’s retained U.FL exclusion is x77.39–80.184 / y10.858–14.922 mm, with zero filled-copper delta inside it on all four layers. This does not establish RF, thermal or return-path performance. Those physical gates remain open alongside loaded-power, source, startup/reset, transient, stencil and environment qualification.

Manufacturer drawing references: Littelfuse1812L page6 specifies1.78 mm pad length ×3.15 mm width and3.45 mm inner gap. TI Rev E page28 specifies2×3 mm copper with1.57×1.89 mm mask-defined exposed opening; the85% coverage criterion applies to the exposed mating/process area, not the entire mask-covered copper extension. Implemented lands match those drawings.
