# Rev 3L · 65 × 30 mm engineering prototype

**Incomplete electrical layout. Do not fabricate.** Open design/GEA-Adapter-Rev3L.kicad_pro for the editable board. [Top probe guide](evidence/probes.svg) · [Top copper](evidence/rev3l-top.svg) · [Bottom copper](evidence/rev3l-bottom.svg) · [DRC and schematic parity](evidence/routing-DRC.json) · [ERC](evidence/ERC.json). Keep the routed 70 × 32 mm [Rev 3K](../rev3k/) as the prototype-review baseline.

## Electrical status

The first 65 mm checkpoint had 32 opens and 94 other DRC findings. The present KiCad 9.0.9 all-severity, all-track-errors run has **13 open connections, zero additional DRC findings, zero ERC findings and zero schematic-parity differences**. There are no reported copper-clearance violations. The main supply and ground nets have no open connections in this report.

Remaining open nets are /DBG_LED, GEA_HalfDplx, Net-(D5-A), Net-(D9-K2) × 2, Net-(R12-Pad2), Net-(R21-Pad1), /GEA3_TX_D6, /PIN1_ILM × 2, /PIN1_UV, /PIN1_OV, /PIN1_FLT_N. An open current-limit, voltage-threshold, fault or appliance-data connection can change behavior even when the supply rails show continuity. The current layout needs a local placement and routing pass for the protection control and interface networks. Keep the eFuse thresholds, input priority, clamp, USB isolation parts, XIAO pin mapping and debug series resistors intact.

The previous checkpoint rerouted interconnects on all four layers, separated the input/output escapes of the two eFuses, added local ground vias and joined sections of the ground reference. The regulator switching and bootstrap copper retain the prior local geometry. The board keeps all 98 footprints and the 232 reference/pad/net records of 3K. The schematic and fitted component selection are unchanged. Footprint geometry work used KiCad pcbnew 9.0.2. The board SHA-256 is `350d8b584832cdfd5ba15cd5963fd1e350280ad6a8d1cf80e9e64bdd16007e5e`.

The current update removes the orphaned debug-LED copper and the dangling branch. The anode and cathode of D5 each still have one electrical open. Moving the series resistor, changing LED orientation and global rerouting were evaluated. The tested alternatives failed to improve complete-net connectivity while retaining the other design rules. No indicator or safeguard was deleted. All footprint coordinates and orientations match the previous 3L.

This version adds 27 ground stitching vias, widens existing ground tracks where clearances allow and widens portions of the module 5 V feed on F.Cu, In1.Cu and In2.Cu. Widening the feed on B.Cu as well produced a lower feed drop but cut into a return corridor. The selected trial retained the existing B.Cu feed width. See the [copper comparison](evidence/power-trials.csv).

## Probe access and isolation

The three 2 mm exposed top pads are TP1 for module 5 V, TP2 for module 3.3 V and TP3 for the protected input. TP12 exposes the buck output on a 1 mm top pad. Use TP16 at the buck or the TP15 plated ground near TP1. The ground connection at TP15 is solid for probing. TP7 is under the module in the populated XY assembly and should be approached from the back or with the module removed. The other service points and the top J7 monitor remain available. The [pad map](evidence/debug-pad-map.csv) distinguishes a footprint's nominal placement side from the actual copper faces of plated holes.

The [probe reach check](evidence/probe-clearance.json) registered both partial Seeed C3 and C6 STEP models to J5 and screened a straight 2 mm diameter probe at each of the six named top landmarks. All six clear the modeled module and fitted bodies with the carrier out of its enclosure. The tightest modeled body-to-probe-edge clearance is 0.44 mm. Confirm the real probe barrel, installed module, C3 antenna lead and cable access before adoption. Use the guide to identify the 3.3 V pad. The compact top legend has limited space.

J7 is a 3.3 V monitor for an isolated fixture. Pin 1 is shared ground. Pins 2–4 are the protected monitor taps with series resistors. Keep the external transmitter and its supply disconnected. Unplug the appliance cable before using USB. Neither the J7 resistors nor the carrier diode provides galvanic isolation. Use the designated service links to isolate their documented sections. Keep the eFuses and transient protection in circuit.

## Size, assembly and cost

FirstBuild measures 59.944 × 27.432 mm across its outline artwork, approximately 1,644.4 mm². The 65 × 30 mm Rev 3L is 5.056 mm longer, 2.568 mm wider and 18.6% larger by area. Its 1,950 mm² footprint saves 290 mm² (12.95%) versus the 70 × 32 mm Rev 3K. These are board dimensions. The 3K case is 77.2 × 40 × 31.9 mm externally and does not fit 3L. The matching [3L case study](case/) measures 72.2 × 38 × 31.9 mm externally and has a common friction-fit base and separate C3/C6 printed-button lids. Both require a physical fit check. [FirstBuild outline Gerber](https://github.com/geappliances/home-assistant-adapter/blob/4888a7df56e8ce6382ed91e4b95bd5020f1802f6/doc/pcb/HA%20Adapter%20Gerbers%2011-15-24.zip)

The fitted BOM comparison gives 72 references and 32 distinct LCSC codes, all top-side. No TP reference is fitted. Review Gerbers contain 178 top paste objects and zero bottom paste objects. The unpopulated underside pads use copper and a mask opening. They require no bottom stencil, placement, solder joint or second reflow. A physical probe fixture or paid functional test is a separate service. There is no new assembly quote or independently verified dollar saving from the smaller outline. Use five fully assembled, single-board, single-sided, lead-free Economic assemblies as the pricing basis. The prior part and fee review is in [3K sourcing](../rev3k/PARTS-AND-COST.md). [JLC assembly pricing](https://jlcpcb.com/help/article/pcb-assembly-price) · [JLC functional test](https://jlcpcb.com/help/article/functional-test-service)

Twenty-nine fitted component bodies screen within JLC's 2.5 mm edge distance, including the intentional 0.38 mm jack overhang. Obtain tooling, removal and insertion approval and price any tooling separately. The body screen uses the jack drawing, maximum socket body dimensions and other package fabrication outlines. The [via audit](evidence/via-to-land.csv) records close mask/copper geometry. No drilled via overlaps a surface land. At TP12 a same-net via annulus reaches the exposed probe copper. Verify tenting, mask registration and finished drill clearances. [JLC assembly capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities) · [JLC assembly terms](https://jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-assembly-service)

## Gates before fabrication

Review the complete routed design, ground return continuity, buck and eFuse loop geometry, stackup and minimum finished copper and plating. The proposed four-layer stack uses 1 oz outers and 0.5 oz inners. The 0.60 A load screen and roughly 1.01 A nominal input current limit are distinct. Compare any completed layout with the 1 oz alternative. Confirm all 72 placements, QFN aperture and angle, connector body origins and through-hole insertion with the factory. Test both XIAO variants on an isolated current-limited bench for startup and load steps, current limiting, source priority, reverse leakage, fault behavior and USB backfeed in both directions. Dry-fit both modules, the actual antenna and a latched plug before finalizing a case. No powered test or order was made.

The earlier all-rear probe placement and its placement-only DRC are retained in evidence/unrouted-placement and evidence/placement-DRC.json. The routed file and its evidence are the current review material.

## Copper-only screening

The inherited Rev 3K model uses 35 µm outer copper, 15.2 versus 30.48 µm finished inner copper and 20 µm via-wall plating. Rail endpoints, both stack assumptions and the 0.60 A and 1.01 A sensitivity cases are in [rail paths](evidence/rail-paths.csv). The resistive model excludes component and connector losses. Remaining opens prevent functional qualification.

- J1.1 to U9.5 (VDC) models 42.313 mV of copper drop at 0.60 A on the thinner stack.
- J1.3 to U10.5 (/ALT_PWR) models 12.05 mV of copper drop at 0.60 A on the thinner stack.
- JP3.2 to J6.7 (+5V) models 40.512 mV of copper drop at 0.60 A on the thinner stack.
- J6.5 to U5.5 (+3V3) models 23.015 mV of copper drop at 0.60 A on the thinner stack.

The [ground return mesh](evidence/ground-return.csv) samples the actual fills, tracks and through connections on a 0.25 mm grid. Ground continuity in this model does not establish transient or RF behavior.

At 0.60 A and 15.2 µm modeled inner copper, the module 5 V feed drops 40.5 mV, down from 49.0 mV on the preceding 3L. The J1.8–J6.6 ground return drops 16.6 mV, down from 17.3 mV. The corresponding Rev 3K values are 32.3 and 3.3 mV. On 3L with 30.48 µm inners the revised values are 29.4 and 9.3 mV. The gap in the return path still warrants a placement and routing redesign before adopting the thinner inner stack. The feed and return calculations use different endpoint pairs. Each is a copper-only estimate. A working 0.5 oz design, factory pricing, temperature rise, regulator stability and backfeed behavior remain unverified.
