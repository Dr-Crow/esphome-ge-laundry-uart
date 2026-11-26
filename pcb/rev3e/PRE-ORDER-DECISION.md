# Rev 3E pre-order engineering decision

**Recommendation: do not release five boards solely on a clean layout report.** Retain the 1 oz inner Rev 3E as the first-article reference if there is no time for an A/B. Prefer the recovered-margin half-ounce candidate only if the shop confirms the intended stack and assembly controls and we can accept the first-article uncertainty. A five-board order is still prototyping, not a guarantee of compatibility. No order or quote mutation occurred during this desk review.

## Tested routing option, not a production change

Starting with the frozen preflight board, uniformly widening the five In2 VDC segments failed clearance against two GEA vias even at 0.65 mm. A separate working copy widens them to 1.0 mm and shifts the upper section 0.60 mm away from the vias, leaving the endpoints unchanged. After refilling the ground zones, native KiCad 9.0.2 showed zero ERC violations and zero DRC errors, unconnected items or schematic parity discrepancies. The original and candidate each had 88 library warnings under this isolated configuration. Comparing track UUIDs and geometry confirms that exactly five tracks changed, all VDC on In2; no via or other track changed. The ground fills were recalculated and are not asserted identical. No approved release Gerber, vendor DFM or pinned KiCad 9.0.9 result yet.

| PIN1 inner trace option | Room-temperature nominal | Sensitivity case: 85 °C, foil 20% below nominal | Drop at assumed 0.60 A in that case | Trace loss in that case |
| --- | ---: | ---: | ---: | ---: |
| 1 oz / 0.50 mm / 29.76 mm | 29.3 mΩ | 46.0 mΩ | 27.6 mV | 16.6 mW |
| 0.5 oz / 0.50 mm / 29.76 mm | 58.6 mΩ | 92.0 mΩ | 55.2 mV | 33.1 mW |
| 0.5 oz / shifted 1.0 mm / 30.65 mm | 30.2 mΩ | 47.4 mΩ | 28.4 mV | 17.1 mW |

Bulk copper model: 1.724e-8 Ω·m at 20 °C, temperature coefficient 0.00393/°C. 0.60 A, 85 °C and minus 20% foil are sensitivity assumptions, not a specified load, requirement, JLCPCB tolerance or a comprehensive worst-case. The table models only one trace. It cannot establish board temperature, ground rise or appliance compatibility.

## Functional gates the $17 cannot buy

- **Startup:** The PIN1 eFuse turn-on is set by R31 360 kΩ / R32 150 kΩ on U9 EN/UVLO. With the typical 1.2 V threshold and nominal resistors it is about 4.08 V, 220 mV below a 4.3 V input. The stacked corner (maximum threshold, 1% resistors at their worst, EN leakage through R31) reaches about 4.254 V, leaving 46 mV. Plan for the corner, but it is not the expected value. That threshold senses the input; do not mechanically subtract the entire downstream drop from that 46 mV. Upstream harness/return sag and downstream voltage delivered to the buck are separate. The full path budget includes source and harness, PIN1 VDC copper/via and eFuse drop, common V_INPUT copper, buck dropout, D11, distribution and XIAO regulator. PIN3 has different enable circuitry; characterize independently. The buck cannot boost to a regulated 5 V at 4.3 V input. Don't call either copper option a low-voltage pass.
- **Heat and protection:** Record actual rail sag and hot spots using an isolated, current-limited dummy source on each input individually, then handoff, with both intended modules and Wi-Fi bursts. Check the source current limit, startup transients, input protection behavior and repeat at intended ambient; never connect an unverified appliance and host USB simultaneously. Keep protection parts and sockets. Thicker foil does not resolve a low source voltage, if present.
- **Manufacturing:** Confirm exact stack and factory tooling/placement on the release files. Check post-CAM GND return continuity and clearances, factory-added tooling, U9/U10 rotation and stencil apertures/thickness, and targeted inspection availability. The separate stencil trial has not been merged into this routing variant. Perform pinned 9.0.9 DRC/ERC and compare fresh CAM, drill, BOM/CPL before release.
- **Cost:** Original five-board $94.22 fabrication + assembly and earlier $25.99 freight preview are the dated reference. $77.51 before freight and tax is a projection if only the inner-copper surcharge disappears. No live lower-copper or landed quote yet. No verified fee-free drop-in so far; keep passive screening separate to avoid hiding a regression. See [quote and sourcing review](QUOTE-AND-COST-REVIEW.md).

Candidate trace-board SHA-256 `492e7bb754593afdce91e6417ed3f8b3c4a826cc75b57f169f8e2ddd20f83711`. This is an identity for the working-copy check, not an orderable artifact.
