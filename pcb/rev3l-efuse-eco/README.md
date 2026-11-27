# Rev 3L-E shared eFuse output bypass study

Experimental 65 × 30 mm carrier for isolated prototype evaluation. The underside is marked **3L-E / PROTOTYPE**. Use 3L-E to evaluate one relatively inexpensive change on the full-diagnostics carrier. The shared capacitor still has two vias in each output path. Electrical qualification, factory review and a 3L-E quote remain open.

[Native KiCad project](design/GEA-Adapter-Rev3L-ECO.kicad_pro) · [Schematic](design/GEA-Adapter-Rev3L-ECO.kicad_sch) · [Board](design/GEA-Adapter-Rev3L-ECO.kicad_pcb) · [Top CAM](evidence/cam-top.png) · [Bottom CAM](evidence/cam-bottom.png)

## What changed

C31 adds a 10 µF, 50 V, 1206 Samsung CL31A106KBHNNNE between the common protected input and ground. It uses C9’s existing C13585 SKU. C9 and C10 remain at the buck. R18 and R33 moved, with their original values. The board retains all 3L probe points, J7, signal selectors, both power inputs, front-only placement and the original outline. The two probe labels affected by placement moved with no reduction in text size.

| Center-to-center PCB route | U9 | U10 |
| --- | ---: | ---: |
| Previous closest fitted output capacitor C9, straight-line lower bound | 24.74 mm | 18.24 mm |
| New route from OUT pin 6 to C31 positive, horizontal copper including travel in end lands | 8.29 mm | 7.73 mm |
| Vias in this route | 2 | 2 |
| GND pin 8 to its nearest connected ground via | 1.94 mm | 2.43 mm |
| Plane-path straight-line lower bound between that via and C31’s ground via | 4.37 mm | 5.91 mm |

C31’s ground land reaches its ground via in 1.27 mm. Horizontal lengths exclude barrel depth. Ground current spreads through filled copper. These geometrical measurements establish proximity only. TI recommends local transient suppression at OUT. The residual two-via loop on each channel makes a separate capacitor per output preferable if the shared part does not keep both pins within their transient limits. [TI TPS25947, sections 5.1 and 8.3.1](https://www.ti.com/lit/ds/symlink/tps25947.pdf)

The +5 V detour adds 0.205 mm at the original 0.90 mm width on In2. This adds about 0.26 mΩ at 15.2 µm finished copper and 20 °C, or 0.16 mV at 0.60 A, using 1.724×10⁻⁸ Ω·m. The existing BOOT trace adds 0.027 mm at its original 0.205 mm width. Small sections of the receiver, input-overvoltage sense and priority-control signals were rerouted. The inner ground pours were refilled. The original rail-screen and mesh results belong to their original boards.

## Capacitance and qualification

Samsung’s 25 °C, 1 kHz, 1 V measurement curve gives typical effective capacitance of 3.386 µF at 12 V, 2.548 µF at 15 V, 1.898 µF at 18.85 V and 1.794 µF at 19.673 V by linear interpolation. The last voltage is a divider screen using the 1.223 V maximum rising OVLO threshold, 1.01 MΩ upper resistor, 67.32 kΩ lower resistor and 100 nA pin leakage. Handover, Q1 on the auxiliary divider and input-step overshoot require separate checks. Temperature, tolerance, aging and measurement amplitude can affect the installed capacitance. [Samsung characteristics](https://product.samsungsem.com/mlcc/CL31A106KBHNNN.do) · [TI electrical characteristics](https://www.ti.com/lit/ds/symlink/tps25947.pdf#page=9)

- On an isolated, current-limited fixture, measure the effective capacitance at operating bias and temperature. Capture each OUT at its IC ground with low-inductance probing during short-circuit interruption and hot-plug, including cable impedance and the highest enabled input. Record amplitude and duration. Design for margin to the continuous and transient absolute limits. TI’s −0.8 V OUT exception applies only below 1 µs.
- Check PIN1-only and PIN3-only start, priority transfer in both directions, a weak input still inside the voltage window, converter startup and module resets with both XIAO variants. Include the added charge taken by C31. R34/R41 set approximately 1.01 A nominal ILIM. The 0.60 A scenario is a load screen. AUXOFF indicates valid priority input after startup and can remain asserted during load overcurrent or thermal shutdown.
- Keep the entire appliance harness disconnected during USB programming. JP3 opens the D11 buck feed. The data steering paths and common ground remain. U11 is **ProTek SRV05-4-P-T7, C85364**. Its native datasheet link was corrected. J1 pins 4, 5 and 7 reach its steering diodes before the external series resistors. A powered data line can raise the module 5 V rail even with JP3 cut. Characterize each signal alone and together using representative source impedances and an initially unpowered carrier. Measure rail rise and injection current before any connector or protection redesign. See the separate data-line options for the residual pull-up paths and unqualified floating-REF proposal. [ProTek datasheet](https://www.lcsc.com/datasheet/C85364.pdf) · [Data-line protection choices](../compact-review/DATA-LINE-PROTECTION.md)
- Check USB-only cold attach on both modules. C11 and the five 100 nF capacitors contribute 10.5 µF nominal before the module’s load. D18 and D20 protect raw inputs upstream of the eFuses. A shorted TVS or sustained reversed harness depends on source-side current limiting. Check enclosed temperature, C3 antenna-lead routing, C6 antenna clearance and printed-case fit on both builds.

## Assembly evidence

Compared with combined commit `c7e102aaa9c85a485478ee5c403a945064977d56`, the bill goes from 72 to 73 fitted references and stays at 32 distinct LCSC codes. All 73 placements are on top. Only R18 and R33 change amongst previously fitted placements. Five fully assembled boards add five capacitor placements, with no additional distinct feeder SKU at these substitutions. No vendor fee or price is established for this ECO.

KiCad 9.0.9 reports zero ERC and DRC violations, zero unconnected items and zero schematic parity differences. Geometry editing used pcbnew 9.0.2. The corrected placement generator checks each fitted body center within 0.10 mm, including the rotated jack and headers. C31, R18 and R33 have body-edge distances of 9.05, 7.23 and 6.34 mm respectively. The 18 inherited bodies under JLC’s 2.5 mm guideline include the jack. Factory handling, tooling, copper tolerances and placement rotation still need the supplier’s review. [Body-edge audit](evidence/component-body-edge.csv) · [ERC](evidence/ERC.json) · [DRC and parity](evidence/DRC.json)

The CAM package contains four copper layers, 180 front paste objects and zero rear paste objects. The outline and nonplated holes match the parent. Rear QR artwork decoded from the new CAM rendering to the project repository. Physical scanning, powered testing and factory acceptance remain open. Board SHA-256 is `a03f99733d337c358b6f3299e666f42263c3d8cb844dea6cbb286324a991fa12`. [CAM and placement comparison](evidence/manufacturing-comparison.json) · [Review exports](manufacturing)
