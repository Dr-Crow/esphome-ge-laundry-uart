# Revision 3A PCB

Status: design in progress. Do not fabricate or connect this board to an appliance yet.

Revision 3A keeps the ESP32-C3-WROOM-02 module used by Revision 2. The module includes its Wi-Fi antenna. The board adds easier USB-C programming and replaces the older power regulators with parts better suited to appliance power and Wi-Fi current peaks.

## What changes from Revision 2.2

| Area | Revision 2.2 | Revision 3A |
| --- | --- | --- |
| ESP32 | ESP32-C3-WROOM-02 | Same module and built-in antenna |
| Programming | External programming connection | USB-C using the ESP32-C3's built-in USB interface |
| Appliance-to-5 V power | L7805 linear regulator | AP63205 switching regulator for less heat and a wider input range |
| 3.3 V power | AP2205, rated for 200 mA | AP2112K, rated for up to 600 mA |
| USB/appliance power sharing | Not supported | Each source passes through a blocking diode before the 5 V rails join |
| Reset monitor | U1 footprint left empty | Removed from the design |
| Board | 88.7 mm by 30.1 mm, two layers | Current draft is about 72.1 mm by 34.1 mm, two layers |

The blocking diodes are one-way valves for electricity. They let either the appliance or USB power the board while preventing appliance power from being pushed back into the computer's USB port. That behavior still needs to be measured on prototypes in every source combination.

## Current state

- The schematic is complete enough for design review and opens in KiCad 9.0.9.
- The board outline, component placement, antenna keepout, ground plane, and part of the power routing are present.
- The GEA3 receiver path from U5 through R12 to ESP32-C3 U2 pad 12, and the transmitter path from U4 through R13 to U2 pad 11, are routed. The DNP J3 debug-header branches on those nets remain open.
- The USB connector and protection parts are placed, but the USB data pair is not routed.
- Many ordinary signal and power connections remain unrouted. The board is not a manufacturing candidate.
- No Gerber, BOM, or placement package is released for ordering.

The next routing slice should distribute +3V3 locally and complete the remaining appliance/control nets. It must continue to leave the USB differential-pair corridor and the ESP32 antenna keepout untouched.

The KiCad files are the source of truth. This branch intentionally does not include custom board-generator scripts, checksum manifests, or per-routing-step validation programs.

## Two-layer versus four-layer USB

The current file remains a two-layer board because cost matters. Espressif permits a two-layer ESP32-C3 design when the bottom layer stays substantially continuous ground, but USB still needs a closely spaced, equal-length 90-ohm pair over uninterrupted ground.

The present USB component placement leaves too little room for a compliant pair on a normal 1.6 mm two-layer stack-up. The next layout step is therefore to try a wider USB corridor while preserving the ground plane and antenna keepout. If a fabricator cannot approve a practical two-layer width and gap after that placement change, the USB-capable board will move to four layers. A two-layer board with USB removed remains a fallback for appliance-power and GEA testing, but it would not meet the browser-flashing goal.

See [DESIGN_NOTES.md](DESIGN_NOTES.md) for the decision gates and unresolved items.

## Before an order can be released

1. Finish every required connection and obtain a clean schematic/PCB parity check.
2. Resolve or formally exclude every ERC and DRC finding in KiCad rather than matching a saved warning count.
3. Obtain a fabricator-approved USB stack-up and 90-ohm routing geometry.
4. Verify exact manufacturer part numbers, footprints, availability, and assembly type for all populated parts.
5. Review the vendor's board, drill, parts, and placement previews.
6. Test a small prototype batch with current-limited power before connecting an appliance.
7. Prove all four power states: appliance only, USB only, both connected, and neither connected.
8. Confirm USB enumeration/flashing, repeated booting, Wi-Fi load, temperatures, and no voltage backfeed.
