# Current Rev2 source review

The earlier review below is frozen to its original input. Current schematic-only
normalization resolves all four aliases; fresh native ERC/DRC/unconnected/parity
are zero. [Source-bound delta and native negative controls](../validation/erc-normalization/DELTA-AND-INTEGRATION.md) prove 186 physical memberships and all PCB/CAM/firmware bytes unchanged.
Power/module/assembly/physical gates remain open.

## Frozen prior review

# Rev 2.0 bounded native cleanup review

Genuine KiCad **9.0.9** validates the cleaned source with **ERC: 0 errors / 4
intentional warnings; DRC: 0 errors / 0 warnings; 0 unconnected items; 0 schematic
parity issues**. DRC includes `--all-track-errors --schematic-parity --severity-all`;
ERC includes `--severity-all`. No rule was disabled, downgraded or excluded.
This is a source cleanup and current export review, not a manufacturing release,
power qualification, appliance safety assessment or supplier rotation approval.

## Source and exact preserved circuit

Restored historical source: `af1f2c40029ef67c56910fb2c55feac835553525`. Cleanup base:
`d02a00776768ee9a45962089be5a58e84adf5d52`, branch `fix/rev2-native-source-review`.
The intentional input patch was snapshotted before the cleanup. It corrects
board `Power Pin` to schematic JP2 and `INPUT POWER` to TP3 using their original
source UUIDs; pinless DNP H3/H4 are excluded from the board, with no new holes.

`proof/verify_cleanup.py` checks the current native board against the immutable
input geometry and fresh native XML netlist. The proof retains **all 186 original
electrical pin memberships / 45 net partitions**, including single-pin unconnected
nets, and verifies original schematic connections and labels, every component
identity, **73 board footprints, 222 physical pad definitions and 712 tracks/vias**.
All placement coordinates, pad layer sets (including NPTH), route geometry,
board drawings/outline, mounting geometry, drills and interfaces are unchanged.
There are 75 source component records, including the two absent pinless DNP
mechanical placeholders. UART direction text remains historical and unchanged.

The independently fused pin-1 VDC and pin-3 ALT_PWR paths and original **manual
JP2 selector** are retained. Q1/Q2, D7, U3 L7805, U6 and all ratings/values remain
historical. No automatic source priority, ORing, regulator substitution, 40 V
propagation or firmware change is introduced. U6 retains the original
AP2205-3.3 value and AP2204R-3.3 symbol identity discrepancy.

## Native library and grid recovery

All 24 original embedded symbol definitions are recovered exactly into
`LegacySymbols`, plus the pinned upstream PWR_FLAG definition. Pin numbers, names,
types, hidden pins, symbol graphics and existing aliases are unchanged. All 73
embedded board footprints are stored individually in `LegacyBoard`, retaining
original geometry and board-specific settings with only the explicitly listed
thermal/silk exceptions. Maps retain every prior library identifier; a clean
library comparison means agreement with these recovered definitions, not with
newer library substitutions.

The original 50 mil connection-grid setting reports 115 native off-grid endpoint
warnings. Every one of the **725 original connection-bearing object coordinates**
is exactly on the 25 mil grid (199 of those object coordinates are off 50 mil).
Changing only the project connection grid to 25 mil clears those warnings without
snapping or moving any source item. The original native rules, severities,
exclusions, net classes and every other project setting are retained.

Three power flags model the intended externally supplied VDC net, GND return and
passive selected/protected `/p1` output feeding U3.IN. They resolve the original
power-input-not-driven model findings at VDC/#PWR013, U1.1 and U3.1. They do not
establish available voltage/current, selector state, regulator headroom or physical
protection performance. The four remaining ERC warnings are classified in
`reports/warning-classification.json`: DBG_LED/GLITCHES, GEA3_TX/RXD,
GEA3_RX/TXD and +5V/VCC. All remain visible at their original warning severity.

## Authorized physical cleanup and regenerated zone fill

U4.2 GND (pad UUID `081246d5-7787-4c04-a448-b62e3ba337a9`) originally has one thermal
spoke where the zone requires two. Its **thermal spoke angle alone changes from
90 to 45 degrees**. The original two-spoke minimum, 0.5 mm thermal gap/width,
pad position/size/layers and existing 0.4064 mm GND route remain. A fresh native
DRC reports no starved relief after the refill; reducing the required spoke count
or replacing the thermal with a solid connection was unnecessary.

Compared against an **untouched source refilled by the same KiCad 9.0.9 engine**,
the angle edit changes **0.575544686049 mm²** of F.Cu fill in one polygon, bounded
by x=83.0875–84.25 / y=90.139802–90.9255 mm around U4.2. B.Cu is exactly unchanged
against that control. KiCad 9 regeneration itself retessellates small cached zone
edges across the historical board: XOR areas are 1.6160023714 mm² on F.Cu and
0.365273824683 mm² on B.Cu, comparing historical cached fill to the untouched
native9 refill. Those separate engine-regeneration differences are quantified in
`proof/copper-refill-difference.json`; they are not attributed to the thermal edit
and are not claimed as CAD-to-original-CAM identity.

Only four silkscreen graphics change: remove U2 overhang UUIDs
`00d77d43-f542-4542-8700-7511e643f1f0` and
`7a3be8be-71f0-415b-b9dc-8b4bc442a08d`; clip the ends of J1 segment UUIDs
`646b6289-7915-4bf1-b4c3-366890826a55` and
`508c05f0-87b7-4e2e-ad56-0ca055349409` to x=131.5 mm. All other graphics and text,
including every original UART label, are retained.


### Exact UART label meanings

The unchanged printed test-point text is `Full RX (5)` and `Full TX (4)`.
J1.5 (`GEA_FullRx`) is the **ESP transmit / appliance receive** path:
U2.12 IO21/TXD → R12 → U5.3 input / U5.4 output → R24 → J1.5.
J1.4 (`GEA_FullTx`) is the **appliance transmit / ESP receive** path:
J1.4 → R25 → U4.3 input / U4.4 output → R13 → U2.11 IO20/RXD.

J2 prints `EN / RX / TX / BOOT / GND / 3v3`; its RX label is at J2.5
(`GEA3_RX`, U2.12 IO21/TXD) and TX is at J2.4 (`GEA3_TX`, U2.11 IO20/RXD).
J3 prints `3v3 GND BOOT` and `EN  RX  TX`: RX at J3.3 connects U2.12
IO21/TXD; TX at J3.5 connects U2.11 IO20/RXD. These header labels are consistent
with the **attached programmer's** receive/transmit perspective, an interpretation
because the source does not print an explicit viewpoint legend. The source net
aliases TXD/RXD and native pin functions establish the ESP direction exactly.

The inherited historical README described RX/TX labels as swapped. A blanket
semantic mismatch is not established when the appliance and attached-programmer
perspectives above are used. No UART text was changed. Verify the viewpoint of
both endpoints when wiring; `proof/uart-direction-map.json` records exact strings,
pins and native paths. This review does not establish which external programming
cable or appliance connector is physically wired to those endpoints.

## Current review exports and historical supplier artifacts

This directory contains the **current** readable schematic PDF, front/back
assembly PDFs and native SVG/PNG board views, two-page copper PDF, drill reports
and maps, native netlist/BOM/placement exports, current Gerbers/drills and a packaged
copy of the current editable design. Assembly PDF pages hide value text and are
cropped for readability; this affects presentation only, not native CAD geometry.
The embedded board screenshot inside the schematic is an original historical
image retained without replacement; use the current board/copper plots for the
actual cleaned board. `reports/source-hashes.json` pairs reports/exports to inputs.

The historical archive `../manufacturing/PCBA-OnionStraws-rev2.0.zip` remains byte
identical, SHA-256 **b9c0b397806d3a719c32faa83c08bac2e80aa1c1d4d27d3e6d6a35cd5381445a**.
All original validation PDF/STEP/render files also remain unchanged. They must not
be presented as exports of the cleaned source. Current CAM is separately labeled
`CURRENT-CAM-REVIEW-rev2.0.zip`; it does not overwrite the original package.

The additional [flat native review CAM](CI-CAM-REVIEW-rev2.0.zip) is retained from
source integration `7df3567e2785f3937ca9884a226c557eda3318e0`. It contains eight
Gerbers, separate PTH/NPTH drills and the native job, with no presentation PDFs.
The flat native archive omits the empty backside paste layer; its exact member
inventory is distinct from the retained presentation package.
Its independently verified native CAM parity applies to these unchanged CAD
bytes. This additional archive does not qualify the historical BOM/CPL or supplier
rotations. The original PCBA and current presentation archives remain separate.

The original archived supplier CPL has nine diode rotations differing by 180°
from native PCB rotations. The standalone historical CPL also has six additional
semiconductor 180° offsets. No supplier convention or approved polarity review
has been established. `native-positions-all.csv` contains the 62 footprints eligible under their original
native placement attributes; `native-positions-top-smd.csv` contains 59 top-side
SMD footprints after native DNP exclusions. `native-footprints-all-73.csv` separately
records all 73 physical footprint placements, native angles, side, attributes and
DNP status. These are fresh **native placement exports with native rotations**,
explicitly **not supplier approved**. They must not be combined with
or substituted into an order using the old package without an assembly review.
Original archive bytes, matching outline bounds and clean native checks do not
prove complete original CAD-to-Gerber/drill geometry parity.

## Reproduce verification

Activate the pinned genuine tools, then run `proof/validate_native.py` with
`kicad-python`. It copies the final design into a temporary directory and runs
ERC, DRC and netlist export sequentially. The temporary copy prevents KiCad 9
project-format migration from rewriting the source project configuration. It
checks the final source/geometry and records fresh all-severity native reports.
`proof/verify_cleanup.py` can also be run with the path to a fresh native XML netlist.
