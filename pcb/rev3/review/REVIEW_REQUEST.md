# Revision 3A review brief

## Suggested review title

Review Request: ESP32-C3 Wi-Fi appliance UART adapter with USB-C and automatic dual-input power

## Purpose

This board is a local-control adapter for compatible GE appliance service ports.
It connects an ESP32-C3 to the appliance's low-voltage GEA serial bus and exposes
the device to ESPHome/Home Assistant over Wi-Fi. The appliance connector is an
8P8C modular connector, but it is **not Ethernet**.

Revision 3A is an unqualified prototype. No assembled board has been electrically
tested, and no appliance connection should be attempted until the current-limited
bring-up sequence passes.

## Design summary

- ESP32-C3-WROOM-02-N4 with built-in Wi-Fi antenna.
- USB-C for normal native-USB flashing, logging, and bench power.
- Permanent 2-by-3, 2.54 mm recovery header for 3.3 V UART flashing.
- Automatic acceptance of appliance power on either connector pin 1 or pin 3,
  with pin-1 priority, per-input resettable fuses, reverse-polarity protection,
  controlled switches, and blocking diodes.
- AP63205 switching regulator followed by an AP2112K 3.3 V regulator.
- Four layers, 88.70 mm by 40.00 mm, 1.6 mm target thickness.
- All 91 fitted components are on the top side.
- `In1.Cu` and `In2.Cu` are intended as continuous ground-reference planes.
- 0.20 mm minimum routed track; standard signal vias are 0.8/0.4 mm through-vias.
- No blind/buried vias, via-in-pad, controlled-depth drilling, or bottom-side assembly.

## Review artifacts

- [Schematic PDF](schematic.pdf) and [schematic PNG](schematic.png)
- [Top outer layer](top.png) and [mirrored bottom outer layer](bottom.png)
- [Inner ground plane 1](inner1.png) and [inner ground plane 2](inner2.png)
- [Top assembly drawing](assembly-top.pdf) and [bottom assembly drawing](assembly-bottom.pdf)
- [Dimensioned outline](dimensions.pdf)
- [Straight-down 3D view](3d-top.png), [isometric view](3d-isometric.png),
  [bottom view](3d-bottom.png), and [side view](3d-side.png)
- [DRC report](drc.rpt), [ERC report](erc.rpt), and [drill report](drill.rpt)
- [BOM and manufacturing-package guide](../production/README.md)
- [Review-readiness checklist](REVIEW_CHECKLIST.md)

## Schematic-review questions

1. Does the pin-1/pin-3 priority and isolation network prevent cross-feed and
   behave safely for all source combinations?
2. Are the resettable fuses, PMOS reverse-protection stages, load switches, and
   blocking diodes appropriately connected and rated for a prototype?
3. Does the AP63205 stage have a defensible path to 5 V, subject to measuring the
   appliance's actual minimum voltage and available headroom?
4. Are the USB-C CC, ESD, VBUS isolation, reset/boot, and recovery-header circuits correct?
5. Are there any floating or incorrectly terminated logic inputs, unsafe power
   domains, or missing bypass components?

## PCB-layout and BOM review questions

1. Are the USB differential routing, layer transitions, and continuous ground
   reference reasonable for native USB Full Speed without a controlled-impedance claim?
2. Are the switching-regulator loops, feedback route, power widths, and return
   paths suitable for first prototypes?
3. Are the ESP32 antenna placement and keepout adequate?
4. Do connector, button, LED, J2-header, mounting-hole, and enclosure clearances
   appear mechanically sound?
5. Do the exact BOM parts, packages, pin mappings, polarity marks, and placement
   rotations agree with the schematic and land patterns?

## Known findings and limits

- KiCad 9.0.9 reports zero DRC errors, zero unconnected items, and zero
  schematic-parity issues. Seven reviewed warnings are documented in this directory.
- ERC reports zero errors and 55 reviewed embedded-library/grid warnings.
- The RJ45 model is a conservative external envelope; internal contact and latch
  geometry are not modeled.
- USB routing dimensions are documented, but no controlled-impedance stack-up is claimed.
- Part availability, assembly rotation, and all vendor previews must be refreshed
  against the current package immediately before ordering.
- Electrical behavior, backfeed protection, temperatures, USB reliability,
  enclosure fit, and appliance compatibility remain unverified until prototype bring-up.

Please keep schematic and PCB-layout feedback separate so each finding can be
addressed and re-reviewed without changing posted review images in place.
