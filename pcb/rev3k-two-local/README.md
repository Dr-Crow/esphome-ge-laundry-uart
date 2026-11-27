# 3K-C2 experimental eFuse output bypass

**Prototype for factory review and isolated bench evaluation.** This is a 70 × 32 × 1.6 mm Rev 3K electrical variant derived from [c7e102a](https://github.com/Dr-Crow/esphome-ge-laundry-uart/tree/c7e102aaa9c85a485478ee5c403a945064977d56/pcb/rev3k). Its underside reads **GEA 3K-C2 / PROTO**. Use the project, board and schematic together in [design](design). The native filenames retain the 3K project name for KiCad sheet-instance and library resolution. [Top CAM](evidence/CAM-top.png) · [Bottom CAM](evidence/CAM-bottom.png)

## Electrical change

C31 connects U9 OUT to ground locally and C32 does the same for U10. Both are the existing C9 SKU, Samsung CL31A106KBHNNNE, 10 µF nominal, 50 V, X5R, 1206 (JLC C13585). C9 and C10 still bypass the buck input. Each capacitor adds a short top copper branch and a dedicated through-via into the ground planes. TI recommends low-ESR ceramic capacitance greater than 1 µF close to the eFuse output to help absorb negative transients. [TI TPS25947, §§8.3.1 and 8.4.1](https://www.ti.com/lit/ds/symlink/tps25947.pdf)

| Measurement | U9 / C31 | U10 / C32 |
| --- | ---: | ---: |
| OUT land to capacitor positive land, nominal edge gap | 1.656 mm | 0.709 mm |
| Top copper centerline from capacitor positive center to near edge of OUT land, approximately | 2.94 mm | 1.97 mm |
| Capacitor ground-pad center to its new plane via, along copper | 1.87 mm | 1.61 mm |
| New ground via to existing eFuse ground via, center to center | 4.903 mm | 6.521 mm |

These measurements describe copper geometry. The planes support multiple return paths. High-frequency loop impedance and turn-off overshoot still need measurement. R18 and R33 moved to make room. R33's ground land now has a direct top connection to U9's existing ground via. Both current-limit resistors and all their traces/vias retain their parent locations. Local portions of the two GEA signals, primary OV/fault, BOOT and a level-shift control net were rerouted. All 18 bare probe lands remain top-side at their original coordinates. The TP17 label is now upright when read from the board's short edge. J7, selectors, module footprint/keepout, LED centers and mounting holes retain the 3K geometry. The matching 3K case still needs a populated dry fit. [Measured pad and via coordinates](evidence/layout-change.json) · [Probe map](evidence/debug-pad-map.csv) · [3K case](../rev3k/case/)

U11 retains C85364. Its schematic and footprint now link to the distributor's datasheet for the fitted ProTek SRV05-4. The rail-steering topology still allows a signal to feed the module rail. Disconnect the appliance cable before connecting USB. [ProTek SRV05-4](https://protekdevices.com/products/series-details/?id=5150)

## Capacitance, startup and bench gates

Samsung's typical room-temperature bias curve gives 3.386 µF per capacitor at 12 V, 2.548 µF at 15 V and approximately 1.794 µF at 19.67 V. The last point screens the high end of the nominal OV-divider range with threshold, resistor and input-leakage tolerances. Actual shutdown can differ with auxiliary leakage, delay and transients. Installed minimum capacitance across lot, temperature, tolerance and aging has yet to be established. The two added capacitors are on the shared post-eFuse rail, adding 20 µF nominal or roughly 6.77 µF of incremental small-signal capacitance at 12 V on the typical curve. Check startup on the actual source and harness because charging current depends on the voltage-dependent capacitance and output slew. [Samsung characteristic data](https://product.samsungsem.com/mlcc/CL31A106KBHNNN.do)

On an isolated current-limited fixture, scope each eFuse OUT against its local ground using a short ground spring. Check startup/restart at the source extremes, current limit, primary-to-alternate changeover and backfeed for each input alone and together. Check positive input and negative output excursions during switching/load steps and controlled overload/fault, followed by rail margin and heating under wireless bursts. Verify the returned module-side rail and UART pin voltages with USB/appliance cable sequencing on the isolated fixture before any appliance use.

The same rail-conductance model and 0.25 mm ground-mesh model used for 3K were rerun. All modeled rail drops match at the published precision. The J1.8 to J6.6 ground drop at 0.60 A changes from 3.332 to 3.405 mV at 15.2 µm inner copper and from 1.894 to 1.949 mV at 30.48 µm. Each model assumes 35 µm outer copper. Confirm the finished stack and transient performance before choosing it. [Rail paths](evidence/rail-paths.csv) · [Ground return](evidence/ground-return.csv) · [Model assumptions](../rev3k/evidence/power/README.md)

## Assembly, cost and verification

KiCad 9.0.9 reports zero ERC violations, zero DRC violations at all severities with all track errors enabled, zero unconnected items and zero schematic parity issues. The editing API was pcbnew 9.0.2. The project rules were retained. Four copper layers, four nonplated holes and 226 plated holes were present in the exported CAM. Front paste objects increase from 178 to 182. Rear paste is empty. [ERC](evidence/ERC.json) · [DRC and parity](evidence/DRC.json) · [Parsed Gerber comparison](evidence/cam-comparison.json)

Five fully assembled single-side boards now need ten additional placements in total. Each board has 74 fitted top-side references and 32 distinct LCSC codes. There is no additional distinct-SKU feeder in the historical fee model. Actual parts, incremental assembly and final price require a configured factory quote. The CPL generator applies the same corrected connector body centers as 3K and checks all 74 output centers against the body table within 0.10 mm. [BOM](manufacturing/BOM-3K-C2-review.csv) · [CPL](manufacturing/CPL-3K-C2-review.csv) · [Connector datums](manufacturing/placement-origin-review.json) · [Review CAM archive](manufacturing/CAM-3K-C2-review.zip)

The fabrication-outline body screen gives C31, C32, R18 and R33 minimum board-edge clearances of 7.90, 10.40, 7.70 and 5.90 mm. Fifteen inherited fitted bodies remain within the factory's 2.5 mm guide, including the intentionally overhanging jack. Ask for tooling/depanelization pricing and placement review before manufacturing. [All fitted body edges](evidence/component-body-edge.csv)

A native outward-polygon screen included same-net copper at every surface land and bare test pad. No through-via bore or annulus overlaps a land. The smallest annulus-to-land gap is about 0.089 mm on inherited R19.2 on both boards. The new same-net GEA_FullRx via near U11.3 measures 0.103 mm annulus-to-land and 0.233 mm from bore to land. Confirm finished registration, solder-mask tenting and stencil coverage with the actual production process. Among just the four altered component positions, the smallest annulus-to-land gap is 0.223 mm at R33. [Via-to-land results](evidence/via-to-land.json)

The trial has no factory quote, factory acceptance, powered fixture data or appliance validation. The two local capacitors are a defensible protection experiment. Choose between this board and a smaller candidate after comparing their measured power-up, turn-off and changeover behavior.
