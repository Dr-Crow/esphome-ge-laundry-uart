# Rev3 follow-up defect and decision map

Updated October 5, 2026. Starting source: `77f4c8893db6c018640e25c55a3af624a3eb06b3`. New engineering covers Rev3A/B/C; Rev3C is the preferred carrier. Historical Rev1/Rev2.x and already-upstreamed Rev2.2 receive no new redesign. Existing history is preserved.

## Applicable electrical work

| Finding | Rev3A | Rev3B | Rev3C | Next action and boundary |
| --- | --- | --- | --- | --- |
| D14/D15 input OR diodes rated 0.5 A/125 °C, below approximately 606 mA nominal switch limit | STPS140Z applied | STPS140Z applied | STPS140Z applied | Exact STPS140Z/C155662 repair applied; numerical nets, pads, placements and routes retained. New native/CAM/quote checks remain required. Preserve numbered nets, both inputs and priority. A part rating repair cannot establish enclosed thermal capability. |
| Downstream PMEG2010ER | D10/D11 already 1 A/20 V/150 °C | D11 already 1 A/20 V/150 °C | D11 already 1 A/20 V/150 °C | Retain unless a separate demonstrated issue justifies change. Input CL does not impose the same output-current limit after a buck. |
| Actual input, fault-energy and hot-load envelope | Unknown | Unknown | Unknown | Complete bounded datasheet calculations; obtain the target appliance/model and reviewed limits before powered qualification. 40 V switch rating is not 40 V carrier capability. |
| Module/regulator/USB implementation | WROOM/AP2112 and separate USB branch | Soldered XIAO C3 | Socketed XIAO C3/C6 | Assess each separately; do not copy carrier-specific assumptions. Disconnect appliance before powered USB on XIAO carriers. |

## Rev3C enclosure work

| Finding | Feasible now | Remaining input or choice |
| --- | --- | --- |
| Accepted stack range 11.0–11.65 mm excludes part of the source's assumed socket/spacer range | Extend the analytical envelope to 10.35–11.65 mm and test new endpoints; retain explicit parameterization | Actual factory header and seated stack remain unmeasured. Assumed envelopes are not supplier guarantees. |
| C6 source switch identity changed between manufacturer archives | Keep named conditional profiles and explicit source/date/MPN evidence | Current schematic identifies TS-1001S while the PCB retains SKTAAAE010. Authenticate fitted lot before physical button calibration. |
| Generic USB gauges do not identify a purchased cable | Use a primary StarTech USB2CC2M drawing for a candidate-specific body/shank screen | Authenticate the module's receptacle mating plane and final insertion relationship; no universal-cable fit claim. |
| Common closure permits the wrong module lid | Prepare plastic-only keying options and measure first contact/closure | A base/lid key does not automatically identify the installed module. Common-base, extra-insert and keyed-base tradeoffs need a deliberate choice. |
| Printed mechanisms, guide relief and antenna routes | Complete source-bound geometry/tolerance screens with exact selected part maxima | Electrical make/overtravel, material/print/fatigue, optical/RF and full cable-route behavior remain physical gates. |

## Reproduction already complete

The [pinned checkpoint](../../../case/rev3c/analytical/review/pinned-reproduction/GE-Pinned-CAD-Reproduction-2026-10-05.md) records build123d 0.11.1/trimesh 5.1.0 reproduction of the frozen 77f4c88 case source. All 43 recovered-prototype and eight analytical STEP/STL pairs pass readback. Across 20 shape comparisons and 12 stack cases, prior 0.10 and pinned 0.11.1 results agree within the stated tolerances. The known wrong-lid interference remains. That checkpoint is historical evidence for the stated source, not a pass for future edits.

Stage focused commits, refresh affected manufacturing/geometry evidence, verify the exact remote commit and preserve a complete backup at each substantive milestone. No order, upstream submission or physical equipment test follows from this map.

[Independent Rev3 repair review](rev3-power-refinement/GE-Rev3-Remaining-Power-Defects-and-Bounded-Repairs.md) records the datasheet/pad/thermal decision and separate source-node correction.
