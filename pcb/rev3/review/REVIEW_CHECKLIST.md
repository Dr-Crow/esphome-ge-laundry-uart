# Revision 3A review-readiness checklist

This checklist adapts the presentation and review practices in the
[schematic](https://www.reddit.com/r/PrintedCircuitBoard/wiki/schematic_review_tips/),
[PCB](https://www.reddit.com/r/PrintedCircuitBoard/wiki/pcb_review_tips/), and
[BOM](https://www.reddit.com/r/PrintedCircuitBoard/wiki/bom_review_tips/)
guides from r/PrintedCircuitBoard. The linked pages remain the authoritative
community guidance.

## Review package

- [x] Schematic supplied as a light-background, grid-free PDF and lossless PNG.
- [x] Schematic is in normal reading orientation and includes board name, date,
  revision, and project identity in its title block.
- [x] Lossless top, bottom, and individual inner-copper views are supplied.
- [x] Clean top and bottom assembly drawings show reference designators without
  the overlapping value text from the earlier assembly image.
- [x] A straight-down populated-board render is supplied in the same orientation
  as the top PCB view; optional isometric and side renders are separate.
- [x] A dimensioned outline drawing states the 88.70 mm by 40.00 mm board size.
- [x] PTH and NPTH drill maps and the drill report are included.
- [x] ERC and DRC machine-readable and text reports are included with dispositions.
- [x] Gerbers have been regenerated and inspected one layer at a time locally.

## Schematic and component checks

- [x] Power and ground pins are visible in the schematic.
- [x] Connector pins, USB-C CC resistors, ESD protection, reset/boot controls,
  bypass capacitors, and power-source isolation are shown.
- [x] Schematic-to-PCB parity reports no mismatch and the PCB reports no
  unconnected items.
- [x] Every fitted BOM reference appears exactly once in the CPL.
- [x] Every one of the 91 fitted references resolves to a 3D model. Repository-
  local exact-part models are used where the KiCad 9 library does not contain the
  required connector, switch, or fuse model.
- [ ] Datasheet pinout and land-pattern checks still require an independent
  human review before ordering.

## Layout and fabrication checks

- [x] Board dimensions remain below the common 100 mm by 100 mm prototype tier.
- [x] All fitted components are on the top side, simplifying assembly and keeping
  the enclosure floor flat.
- [x] Pin-1 and polarity indicators are present for user-facing and polarized parts.
- [x] The antenna overhang and keepout are documented.
- [x] Minimum routed track width is 0.20 mm and standard signal vias are
  0.8/0.4 mm through-vias. ESP32 thermal vias are 0.6/0.3 mm.
- [x] The functional layer order is documented below.
- [ ] Final dielectric thicknesses and finished copper weights must match the
  selected fabricator's reviewed stack-up before fabrication.
- [ ] Board, drill, parts, and placement previews must be reviewed in the vendor
  portal using the current manufacturing package.

### Intended four-layer function

| Layer | Intended use |
| --- | --- |
| `F.Cu` | Components, local power, and signal routing |
| `In1.Cu` | Continuous ground reference plane |
| `In2.Cu` | Continuous ground reference plane |
| `B.Cu` | Signal routing and short feedback/USB transitions |

Target finished thickness is 1.6 mm. This table describes electrical function,
not an impedance-controlled fabrication stack. Native USB must be tested on the
assembled prototype.

## BOM and assembly checks

- [x] BOM records exact manufacturer, manufacturer part number, LCSC identifier,
  footprint, and relevant electrical ratings.
- [x] BOM contains 43 purchasing groups and 91 fitted references; CPL contains
  the same 91 references.
- [x] Components use standard values and assembly-compatible packages; no BGA,
  WLCSP, blind/buried via, via-in-pad, or bottom-side placement is used.
- [x] Known quote-time sourcing gates and no-substitution-sensitive parts are
  documented in [../DESIGN_NOTES.md](../DESIGN_NOTES.md).
- [ ] Availability, substitutes, extended-part fees, and placement rotations
  must be refreshed in the vendor portal immediately before ordering.
- [ ] The current 43-group package needs a new assembled-board quote because the
  recorded quote predates the populated J2 recovery header.

## Physical release gates

- [ ] Independent schematic, layout, BOM, and mechanical review completed.
- [ ] Small prototype batch assembled and visually inspected.
- [ ] Current-limited USB-only and appliance-input tests completed.
- [ ] All eight source combinations pass without backfeed or unsafe heating.
- [ ] USB enumeration, flashing, repeated reconnects, and sustained logging pass.
- [ ] Enclosure fit, button access, LED visibility, J1/J4 cable insertion, and
  antenna clearance pass with physical hardware.

Until every physical release gate passes, Rev3A is a review and prototype design,
not production hardware.
