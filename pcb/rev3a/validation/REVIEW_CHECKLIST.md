# Revision 3A review checklist

This checklist follows the presentation guidance in the r/PrintedCircuitBoard
[schematic](https://www.reddit.com/r/PrintedCircuitBoard/wiki/schematic_review_tips/),
[PCB](https://www.reddit.com/r/PrintedCircuitBoard/wiki/pcb_review_tips/), and
[BOM](https://www.reddit.com/r/PrintedCircuitBoard/wiki/bom_review_tips/) review
guides.

## Package preparation

- [x] Grid-free schematic PDF with revisioned title block.
- [x] Top, mirrored-bottom, and separate inner-layer views.
- [x] Top and bottom assembly drawings with reference designators.
- [x] Straight-down, bottom, side, and isometric populated-board renders.
- [x] Board outline plus PTH and NPTH drill maps.
- [x] Machine-readable ERC and DRC reports.
- [x] Matched Gerber, BOM, and placement files.
- [x] Live five-board quote accepted all 40 BOM groups and 93 placements.

## Source and layout checks

- [x] Schematic-to-PCB parity reports no mismatch.
- [x] PCB reports no unconnected items or error-severity DRC findings.
- [x] BOM contains 40 groups; CPL contains 93 fitted top-side references.
- [x] BOM rows include exact manufacturer and LCSC identifiers.
- [x] D18 and R38 are included in both source and manufacturing outputs.
- [x] Standard 0.8/0.4 mm routed through-vias and 0.30 mm ESP32 thermal drills.
- [x] No blind/buried vias, filled vias, controlled-depth drilling, or bottom-side
  component placement.
- [x] `In1.Cu` is a continuous ground plane; the short D18 signal branch on
  `In2.Cu` is documented.
- [ ] Independent datasheet pinout, polarity, and land-pattern review completed.
- [ ] Fabricator stack-up and USB return path reviewed.
- [ ] Vendor board, drill, part-selection, and placement previews reviewed.

## Physical qualification

- [ ] Small prototype batch assembled and visually inspected.
- [ ] Actual appliance supply range and AP63205 headroom measured.
- [ ] Pin-1-only, pin-3-only, and all eight source combinations pass.
- [ ] Pin 3 to pin 1 and pin 1 removal to pin 3 dynamic handoffs pass.
- [ ] Reverse current into inactive appliance inputs remains within the reviewed
  acceptance limit.
- [ ] USB VBUS falls below 0.8 V within one second after USB removal and no
  appliance-to-host backfeed is observed.
- [ ] D18 stand-off, clamp behavior, and energy margin are consistent with measured
  steady-state and transient conditions.
- [ ] USB enumeration, flashing, reconnect, sustained logging, and Wi-Fi-load tests pass.
- [ ] Enclosure fit, connector insertion, button access, LED visibility, and
  installed antenna performance pass.

Until every physical qualification item passes, Rev3A remains prototype hardware.
