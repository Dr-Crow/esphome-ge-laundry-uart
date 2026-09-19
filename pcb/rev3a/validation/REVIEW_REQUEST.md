# Revision 3A review brief

## Suggested title

Review request: ESP32-C3 appliance UART adapter with USB-C and automatic dual-input power

## Purpose

This board connects an ESP32-C3 to the low-voltage GEA serial bus used by compatible
GE appliances and exposes local control through ESPHome/Home Assistant. Its 8P8C
modular connector is **not Ethernet**.

Rev3A is an unqualified prototype. No assembled board has completed electrical or
appliance testing.

## Design summary

- ESP32-C3-WROOM-02-N4 with built-in Wi-Fi antenna.
- USB-C native USB for flashing, logging, and bench power.
- Permanent 2-by-3, 2.54 mm recovery header for 3.3 V UART flashing.
- Automatic appliance power from connector pin 1 or pin 3, with pin-1 priority,
  per-input fuses, reverse-current blocking stages, load switches, and Schottky ORing.
- Populated SMF16A TVS on the protected pin-1 branch, patterned after the published
  FirstBuild design but not yet physically qualified.
- AP63205 switching 5 V regulator and AP2112K 3.3 V regulator.
- Four layers, 88.7 x 40.0 mm, 1.6 mm target thickness.
- 93 fitted components, all on the top side.
- 0.20 mm minimum routed track and ordinary 0.8/0.4 mm through-vias.
- No blind/buried vias, filled vias, controlled-depth drilling, or bottom assembly.

Q3/Q4 are intended to block reverse current and source-to-source backfeed. The
design does not claim protection against a physically reversed supply.

## Review artifacts

- [Schematic](schematic.pdf)
- [Top](top.svg), [mirrored bottom](bottom.svg), [inner 1](inner1.svg), and
  [inner 2](inner2.svg) layer views
- [Top assembly](assembly-top.pdf) and [bottom assembly](assembly-bottom.pdf)
- [Board outline](board-outline.pdf)
- [Top](renders/3d-top.png), [isometric](renders/3d-isometric.png),
  [bottom](renders/3d-bottom.png), and [side](renders/3d-side.png) renders
- [ERC](reports/erc.json) and [DRC](reports/drc.json) reports
- [BOM, CPL, and Gerber package](../manufacturing/README.md)
- [Review checklist](REVIEW_CHECKLIST.md)

## Schematic questions

1. Does the pin-1/pin-3 priority network prevent cross-feed and transition safely
   in both handoff directions?
2. Are the fuses, PMOS reverse-current stages, TPS22810 load switches, Schottky
   diodes, and D18 TVS connected and rated appropriately for a prototype?
3. Is the AP63205 stage appropriate once the actual appliance minimum voltage and
   path loss are measured? The FirstBuild 4.3-15 V label is on downstream
   `V_INPUT`; it is not a measured Rev3A appliance range.
4. Are the USB-C CC, ESD, VBUS isolation/discharge, reset/boot, and J2 recovery
   circuits correct?
5. Are there floating logic inputs, unsafe power-domain interactions, or missing
   bypass/protection parts?

## Layout and BOM questions

1. Are the USB routing, layer transitions, and continuous `In1.Cu` reference
   reasonable for native USB Full Speed without a controlled-impedance claim?
2. Is the short D18 signal branch on otherwise-ground `In2.Cu` acceptable, and are
   its through-via locations appropriate?
3. Are the switching-regulator loops, feedback route, power widths, and returns
   suitable for first prototypes?
4. Are the ESP32 antenna placement and keepout adequate?
5. Do connector, header, button, LED, mounting-hole, and enclosure clearances look sound?
6. Do the exact BOM parts, packages, pin mappings, polarity marks, and rotations
   agree with the schematic and footprints?

## Known findings and limits

- KiCad 9.0.9 reports zero ERC/DRC errors, zero unconnected items, and zero
  schematic-parity findings. The saved reports contain 55 ERC warnings and seven
  DRC warnings with dispositions in [README.md](README.md).
- USB routing has a continuous ground reference, but no controlled-impedance
  fabrication stack is claimed.
- The J1 3D model is a conservative external envelope; final fit requires a real part.
- Supply range, source handoff, reverse current, VBUS decay, D18 behavior,
  temperature, USB reliability, Wi-Fi performance, and enclosure fit remain
  prototype tests.

Please keep schematic and PCB-layout findings separate so each correction can be
reviewed independently.
