# Rev 3F first-article acceptance (Rev 3E control when compared)
Prototype only. These are planned checks, not bench results. Do not attach
to a mains-powered appliance under this plan. Work on a current-limited,
isolated dummy fixture with a qualified operator. Keep USB-only, isolated
dummy-fixture, and any future qualified appliance work separate. Never use a
real USB host alongside an attached appliance. Verify grounding paths before
connecting probes and verify J1 pinout before enabling either rail.

## Evidence record
One row per run: board/assembly ID, actual revision, artwork SHA-256, factory stack ID and inner copper, exact socket and module lot, C3/C6 and
firmware SHA, current limit, harness length and measured source impedance,
voltage at connector and eFuse VIN, temperature, waveform ID, boot/reset
reason, Wi-Fi sustained TX, GE bench emulator transactions, disposition.
Capture raw TP8/9, shared V_INPUT TP3, pre-D11 TP12, post-D11 TP1, module
TP2/+3.3 V, each input current and, on transition runs, TP13/14 and time marks.
Use differential probes and short local returns. For fast transients, probe
hardware near eFuse IN and the buck VIN capacitor, not solely the connector
TPs. For calibrated current use current probes or measured Kelvin shunts;
account for fixture resistance. TP15 is local mux return; TP16 is TVS return.

| Gate | Check on dummy fixture | Decision |
|---|---|---|
| Unpowered | Confirm kit part/lot, pin 1, TVS/D11 polarity, C30 DNP, no shorts, XIAO seating and lid/USB clearance; verify actual solder tails clear enclosure | Stop any short, ambiguity or interference; inspect hidden eFuse joints via X-ray if available |
| Low supply | Both modules, each input independently; screen 4.3, 5 and 15 V at the connector before load, repeat during TX with documented source impedance | Proposed screen: 10 starts per combination; no resets/chatter, sustained TX and bench bus exchange. Verify operating range for exact installed module before applying a provisional 3.0–3.6 V rail bound. Record measured sag and source current margin |
| Dual rail | Test both arrival/removal sequences and weak PIN1 while valid PIN3 is present | Record actual priority, rail minimum, restart and transfer time; scope inactive-rail current against a stated measurement floor. No silent backfeed; don't claim seamless until service survives |
| Controlled hot plug | After stable bench bring-up, scope local eFuse and buck inputs separately with representative cable/source extremes | Target eFuse ≤23 V incl. uncertainty; above that requires justified transient budget; ≥28 V is failure. Check negative ringing and buck bounds separately. Stop at unexplained excursion or heating |
| Fault classification | Bounded dummy-only UVLO/OVLO and load tests | Predicted trip/recovery are planning points, not acceptance limits. 19 V is cutoff characterization, not supported continuous operation. Do not add C30 to hide an unknown failure |

TP17/18 have no onboard pull-up. Use a weak pull-up referenced to DUT
ground only on a reviewed isolated fixture, within ratings and without
back-powering unpowered parts. Verify pull-up supply is valid in the capture.
FLT alone cannot classify: normal reverse-current blocking may assert it,
whereas UVLO/OVLO may deassert it. ILM is nominally 0.601 V/A with 3.3 kΩ,
directional outside specified gain range; do not infer current without
calibration. Keep total node capacitive loading below TI's 50 pF guidance.
 
Sources: [TI TPS25947](https://www.ti.com/lit/ds/symlink/tps25947.pdf),
[Diodes AP63205](https://www.diodes.com/datasheet/download/AP63200-AP63201-AP63203-AP63205.pdf),
[Espressif C6 hardware checklist](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c6/schematic-checklist.html).

## Measure the PIN3 cutoff without disturbing its divider
With Q1 inactive, the nominal 1 MΩ / 68 kΩ divider and 1.20 V threshold
give 18.847 V unloaded. A scope input from TP14 to DUT ground adds a
parallel path: 1 MΩ gives 20.047 V, 10 MΩ gives 18.967 V, and 100 MΩ gives
18.859 V. The added trip error is Vthreshold × Rtop / Rprobe; 10 pF gives
roughly 0.60–0.64 µs of quiet-divider time constant. These are calculations,
not measured values; they omit Q1 switching and part tolerances.
First determine the transition from raw PIN3 (TP9) and switched V_INPUT
(TP3), leaving TP14 untouched. Use characterized high-input-resistance,
low-capacitance probing for the separate control trace, and repeat without
the probe if handoff timing is ambiguous. Never use 50 Ω termination here.

## Review the actual eFuse stencil before releasing assembly

The TI RPW0010A example uses 0.100 mm stencil foil. The nominal Rev 3F
rounded apertures (0.05 mm corner radius) give these geometric area ratios,
using opening area divided by wall area:

| Foil | 0.28 × 1.06 mm split power windows | 0.25 × 0.60 mm side signal windows |
|---|---:|---:|
| 0.100 mm | 1.14 | 0.92 |
| 0.120 mm | 0.95 | 0.76 |
| 0.150 mm | 0.76 | 0.61 |

At 0.150 mm, the side openings fall below the usual 0.66 paste-release
screen even though the split power windows do not. This is not a factory
defect prediction or sign-off. Ask the assembler for the intended foil
thickness and as-cut aperture drawing, including the side and custom
corner openings, the split-pad web, and paste adjustments. Ask what
inspection is available for hidden U9/U10 joints. Confirm on the exact
assembly revision rather than inferring the stencil from the Gerbers.

[TI stencil example, PDF p. 74](https://www.ti.com/lit/ds/symlink/tps25947.pdf#page=74)
· [JLCPCB aperture guidance](https://jlcpcb.com/blog/stencil-aperture-design-geometry-area-ratio-tips).
