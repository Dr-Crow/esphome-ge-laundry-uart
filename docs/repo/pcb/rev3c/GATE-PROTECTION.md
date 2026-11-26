# Historical Rev3C gate repair at frozen8f95555

This document and its proof describe the frozen80-part gate-repair quote baseline. The current selected higher-rated branch adds the separately documented [rated-switch delta](RATED-SWITCH-OPTION.md); use [rated-switch-proof.json](validation/rated-switch-proof.json) for its current-source evidence. Counts, placements, routes and switch/PPTC statements below are historical for8f95555.

**Current selected-branch clamp:** D16/D17 now select **MCC BZT52C12-TP / C668891**, with the original source/cathode1 and gate-bias/anode2 connections and SOD-123 footprint unchanged. This separately reviewed sourcing correction replaces the former unavailable Nexperia selection in the selected rated candidate. MCC permits25/150 Ω differential impedance at5/1 mA versus Nexperia's10/90 Ω; its temperature coefficient is typical with unspecified test current, and comparable capacitance/surge bounds are absent. The nominal26 V/12 V illustration gives2.745 mA and32.9 mW, below5 mA voltage characterization. Do not apply the historical Nexperia coefficient, capacitance or thermal estimates below to MCC. See the [current primary comparison and package review](RATED-SWITCH-OPTION.md#reviewed-gate-clamp-sourcing-correction); low-current/hot clamp, fast VGS and assembly/thermal qualification remain open. The frozen8f95555 source and existing quote folders retain their original exact parts and bytes.

This review candidate changes only the two original input PMOS orientations and their gate-bias/clamp networks. It starts from restored shared dual-input commit `ade0f40b17ea30bc8b6f70665dd0e3bf4c579644`. Both appliance inputs, original automatic PIN1-presence priority, source-OR diodes and the AP63205 buck remain. **The repair is not complete input protection, an appliance qualification or manufacturing approval.**

## Exact electrical delta

| Position | Restored connection | Corrected connection |
| --- | --- | --- |
| Q3 pin 3 D | PIN1_PROTECTED | PIN1_FUSED |
| Q3 pin 2 S | PIN1_FUSED | PIN1_PROTECTED |
| Q4 pin 3 D | PIN3_PROTECTED | PIN3_FUSED |
| Q4 pin 2 S | PIN3_FUSED | PIN3_PROTECTED |
| D16 pin 1 K | GND, MBR0540-TP Schottky | PIN1_PROTECTED/source, BZT52-C12X 12 V zener |
| D17 pin 1 K | GND, MBR0540-TP Schottky | PIN3_PROTECTED/source, BZT52-C12X 12 V zener |
| R31/R32 pin 1 | respective fused input | GND, retaining 5.1 kΩ |
| C18/C19 pin 1 | respective fused input | respective protected output/source, retaining 100 pF/50 V C0G |

D16/D17 anode pin 2, R31/R32 pin 2 and C18/C19 pin 2 share the respective `PIN*_GATE_CLAMP` bias node. R33/R34 retain 51 Ω between that node and the actual Q3/Q4 gate pin 1. The capacitor therefore bridges source and gate-bias deliberately, not raw input and bias. No gate-source DC pull-up is retained. Native symbols and PCB pad nets use the same mapping.

The corrected PMOS body diode permits positive input to start charging the protected source, then the grounded gate bias turns the channel on. With negative drain input and initially unpowered output, its body diode blocks and VGS remains near zero. This repairs the inherited steady reverse-polarity orientation defect. Drain/source differential, capacitive coupling, hot leakage and changing or precharged outputs still need bounded fault tests. It does not establish reverse-current blocking during every transition.

Below the zener knee, the 5.1 kΩ pull-down brings the gate toward ground through 51 Ω, so nominal 5 V input provides roughly negative source voltage at VGS instead of the inherited source-to-bias resistor and ground Schottky drop. No added series load element or reduced source-voltage window is introduced. Main current routes remain 0.5 mm front copper; five new 0.8/0.4 mm plated vias carry only clamp/capacitor taps. The schematic mirrors Q3/Q4; all 97 PCB footprint positions, rotations, attributes, pad geometry, layers, drills and model references remain unchanged.

## Exact zener, package and sourcing

The [official Nexperia ordering table](https://www.nexperia.com/products/diodes/zener-diodes/serie/bzt52-c-series/) lists **BZT52-C12X**, 12NC **934071127115**, Active, marking **CJ**, package **SOD123**, packing **SOD123_115**. The [primary BZT52-series datasheet](https://assets.nexperia.com/documents/data-sheet/BZT52_SER.pdf) assigns pin 1 cathode and pin 2 anode. This matches the retained native `Diode_SMD:D_SOD-123` footprint's pad 1 cathode bar and pad 2 anode. The BZT52H family uses SOD123F and is not this sourcing/footprint choice.

The [public LCSC listing C550251](https://www.lcsc.com/product-detail/Zener-Diodes_Nexperia-BZT52-C12X_C550251.html) maps exactly Nexperia BZT52-C12X to SOD-123. It showed **Out of Stock** when read October 3, 2026 at 18:31 UTC; the retrieved page was cached from the preceding week. It is sourcing identity evidence, not a live availability guarantee. The exact SKU is recorded in the BOM for review, with procurement held pending availability or a separately proved replacement. Reference price shown was USD 0.0499 at 10+, excluding assembly, tax, shipping and procurement fees.

Primary datasheet bounds are:

- VZ 11.4–12.7 V at IZ = 5 mA, Tj = 25°C
- Differential resistance maximum 90 Ω at 1 mA and 10 Ω at 5 mA
- Temperature coefficient +6…+10 mV/K at 5 mA
- Diode capacitance maximum 85 pF at VR = 0 V, 1 MHz
- 350 mW with the standard footprint, RθJA maximum 350 K/W and Tj maximum 150°C; 590 mW requires the specified 1 cm² cathode area, which this footprint does not provide

## Gate margin is bounded, not transient qualification

At an **illustrative** 26 V source and a 12 V clamp, gate-bias voltage is 14 V. A nominal 5.1 kΩ pull-down carries 2.745 mA and dissipates 38.4 mW; the zener dissipates 32.9 mW. Gate DC current is negligible, so the 51 Ω gate resistor produces no meaningful DC offset. The bias pull-down adds about 0.98 mA at a 5 V source below the zener knee. This modest bias load is not an OEM accessory-current allowance or a complete source-current budget.

The 11.4–12.7 V range is specified at 5 mA, not the illustrative 2.745 mA. It must not be asserted as a guaranteed clamp range at the actual bias current. Extrapolating the 5 mA maximum coefficient from 25°C to Tj = 150°C gives an engineering estimate of 12.7 + 0.010 × 125 = **13.95 V**, approximately **6.05 V** below CJ3407's 20 V magnitude VGS limit. This is a static estimate, not a guaranteed current/temperature/transient corner. At about 33 mW and 350 K/W, the indicative temperature rise is 11.6°C; junction power allowance at 125°C ambient is about 71 mW. Resistor and diode derating must be checked at actual ambient and board thermal conditions.

The clamp anode is on the bias side of the existing 51 Ω resistor. Actual gate VGS can differ during gate-charge/Miller current. C18/C19, diode capacitance, MOSFET capacitance, the retained long gate traces and the source-reference routing determine timing and overshoot. Verify gate/source peaks, turn-on, turn-off, reverse steps and both branches at source and temperature extremes. A “12 V” label and native CAD passes do not bound fast VGS spikes. The illustrative 26 V case is itself beyond TPS22810's 20 V absolute input/enable boundary and is not an allowed applied-board test voltage.

## Preserved functions and independent open gates

PIN1 remains J1.1 → F2 → Q3 → U9 → D14 → V_INPUT. PIN3 remains J1.3 → F1 → Q4 → U10 → D15 → V_INPUT. Q5/R35/R37 still sense PIN1_PROTECTED and pull PIN3_EN low; R36 still enables PIN3 from its own source when PIN1 is absent. This is original PIN1-presence priority, including its weak-PIN1 inhibition limitation. No manual mode, bypass, new converter, switch replacement, new current limit or software dependency is introduced.

U9/U10 TPS22810, D18 SMF16A, both 24 V PPTCs, CJ3407 VDS, D14/D15 current/thermal limits, common AP63205/D11 and the module power paths remain independently unqualified. PIN3 still lacks a coordinated TVS. Nominal-5 V loaded cold start, RF demand, switchover, bus thresholds, source current and thermal gates remain open. See [POWER-QUALIFICATION.md](POWER-QUALIFICATION.md). Powered USB and appliance power must never be connected together under the reviewed module wiring; no battery is included in the load budget.

## Native verification and review package

The [native delta proof](validation/gate-protection-proof.json) records all 221 schematic pin mappings and all 97 native PCB footprints against the restored checkpoint. Exactly **10 pin nets** change as tabulated; **211 remain unchanged**, including all sockets, JP1, pulls, signals, input connector pins, switch/converter/priority pins and test points. Only D16/D17 part fields/values change. The outline stays **99 × 40 mm**, mounts stay at (4.5,33) and (94,35) mm, all 14 socket pads and the C6 antenna rule area stay intact. Filled copper intersection remains **0.0 mm² on all four layers** in the 77.0–80.9 × 11.8–19.2 mm antenna rectangle.

Exactly **33 affected power/gate copper objects** are removed and **39** replacements added, including five clamp-network vias. All retained copper objects, all signal copper, all firmware sources, the project/netclasses/plot policy and every native CPL row are unchanged. The BOM and CPL still contain **80 fitted parts**; only two BOM lines change to the exact zener.

Genuine native KiCad **9.0.9**, pinned symbols/footprints, full error/warning/exclusion ERC and DRC with all track errors and schematic parity report **0 violations, 0 unconnected items and 0 parity differences**. BOM, CPL, four copper SVGs, top/bottom/oblique renders, schematic PDF, source manifest and the **14-member factory Gerber/drill/job ZIP** are regenerated from these sources. Separate PTH/NPTH map PDFs remain validation artifacts. Actual render, schematic, copper and drill-map pixels are inspected; these establish CAD/package review, not electrical or physical qualification.

The source-restoration proof describes the earlier frozen restored checkpoint; the gate-protection proof describes frozen8f95555. Current selected-source verification is [rated-switch-proof.json](validation/rated-switch-proof.json) and the current manifest. No board order, publication, account/login action or physical appliance test was performed by this source repair.
