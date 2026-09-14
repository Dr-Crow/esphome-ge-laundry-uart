# Revision 3A PCB

## Automatic power front end

Revision 3A is a no-jumper design. Each appliance input is protected independently:

```text
J1 pin 1 (VDC)  -> F2 -> CJ3407 reverse-protection PMOS -> TPS22810DBVR ->+
J1 pin 3 (ALT)  -> F1 -> CJ3407 reverse-protection PMOS -> TPS22810DBVR ->+-> V_INPUT
                                                                            |
                                                                            +-> AP63205 input
```

Each TPS22810 uses CT = 0.022 uF, a local 1 uF input capacitor, a 0.1 uF output
capacitor, and a small 100 pF/5.1 k/51 ohm PMOS gate network derived from the
published FirstBuild design. An MMBT3904 transistor and two resistors give pin 1
priority when both inputs are present. MBR0540 diodes combine the two protected
outputs without feeding one appliance pin from the other. USB power remains on its
separate F3/D10 path, and the existing buck-side D11 isolation is retained. There is
no JP2 or user-selectable power control.

The AP63205 remains the prototype regulator. A measured 4.3 V source cannot produce a
regulated 5 V output; source headroom and the reverse-protection/load-switch drops are
physical release gates, not software assumptions.

### Eight-state power truth table

| VDC (pin 1) | ALT_PWR (pin 3) | USB VBUS | Selected appliance path | V_INPUT / board behavior |
| --- | --- | --- | --- | --- |
| absent | absent | absent | none | unpowered |
| present | absent | absent | pin 1 | V_INPUT from pin 1 |
| absent | present | absent | pin 3 | V_INPUT from pin 3 |
| present | present | absent | pin 1 priority | pin 3 isolated |
| absent | absent | present | USB | USB path only |
| present | absent | present | pin 1 + USB isolation | no appliance-to-USB backfeed |
| absent | present | present | pin 3 + USB isolation | no appliance-to-USB backfeed |
| present | present | present | pin 1 priority + USB isolation | both isolated; test current sharing |

The schematic includes diagnostic pads at the fused, reverse-protected, and switched
output of each appliance input, plus V_INPUT, USB VBUS, +5V and +3V3. J2 remains a
schematic-only, do-not-install header option and is not placed on the PCB. J3 is the
existing do-not-install Tag-Connect programming footprint. Validate all eight states
with current-limited supplies before any appliance connection.

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
| Board | 88.7 mm by 30.1 mm, two layers | Current draft is about 88.7 mm by 40.0 mm, two layers |

The blocking diodes are one-way valves for electricity. They let either the appliance or USB power the board while preventing appliance power from being pushed back into the computer's USB port. That behavior still needs to be measured on prototypes in every source combination.

## Current state

- The schematic is complete enough for design review and opens in KiCad 9.0.9.
- The board outline, component placement, antenna keepout, and bottom ground zone are present.
- The automatic pin-1/pin-3 power paths now reach the regulator input, and the
  lower-edge buck-converter input, switching, output, bootstrap, and feedback
  connections are routed. The feedback sense trace uses the bottom layer briefly
  and returns to the output capacitor through two standard through-vias.
- The USB-C connector is placed on the lower board edge. The ESP32-to-series-resistor
  section of the USB pair is routed on the top layer at 5.225 mm and 6.025 mm
  (0.800 mm skew), with no vias. The ESD protector has a local ground via, and both
  connector ground contacts are tied to the grounded shell pads.
- The connector-to-ESD and ESD-to-series-resistor data sections, additional ground
  returns, and the remaining signal and rail connections still need routing and a
  final zone refill. The board is not a manufacturing candidate.
- No Gerber, BOM, or placement package is released for ordering.

The next routing slices should finish and measure the two remaining USB data sections,
add short ground returns into the bottom plane, then complete the remaining appliance
and control nets. Every slice must preserve the bottom ground return and ESP32 antenna
keepout.

The KiCad files are the source of truth.

## Two-layer versus four-layer USB

The current file remains a two-layer board because cost matters. Espressif permits a two-layer ESP32-C3 design when the bottom layer stays substantially continuous ground, but USB still needs a closely spaced, equal-length 90-ohm pair over uninterrupted ground.

The published FirstBuild manufacturing archive is also two-layer: it contains one
top and one bottom copper image and no inner copper layers. A JLCPCB calculator check
on 2026-09-14 priced five 88.7 mm by 34 mm bare boards at $4 total for two layers and
$7 total for four layers before shipping. That quote is a planning snapshot, not the
final assembled Revision 3A price.

FirstBuild's Gerber outline measures about 59.94 mm by 27.43 mm. It achieves that
density with a Seeed XIAO ESP32-C3 daughterboard, which already includes USB-C and the
radio subsystem, plus carrier components placed on both sides and extensive use of
0402/0603 packages. Revision 3A keeps the native ESP32-C3-WROOM-02, larger passives,
and single-sided component placement. Its 40 mm height provides a dedicated lower-edge
buck-converter corridor without using the USB routing area. Changing to four copper
layers alone would not reduce it to FirstBuild's footprint.

The USB component placement must leave a direct corridor for the pair while preserving
the ground plane and antenna keepout. The release design remains two layers. Trace
width and spacing use JLCPCB's published calculator model for its nominal stack-up:
17 mil traces, an 8 mil pair gap, and 8 mil clearance to top-layer ground produce a
calculated result near 90 ohms. JLCPCB does not advertise impedance certification for
its normal two-layer FR-4 service, so this is a design target rather than a TDR-backed
fabrication guarantee. If that geometry does not fit over uninterrupted bottom
ground, the two-layer layout must be revised and reviewed again; moving to four layers
is outside the current Revision 3A decision unless separately approved.

See [DESIGN_NOTES.md](DESIGN_NOTES.md) for the decision gates and unresolved items.
Use [BRINGUP.md](BRINGUP.md) to record current-limited prototype validation before
any appliance connection.

## Before an order can be released

1. Finish every required connection and obtain a clean schematic/PCB parity check.
2. Resolve or formally exclude every ERC and DRC finding in KiCad rather than matching a saved warning count.
3. Verify the documented two-layer USB geometry, pair-length match, and uninterrupted ground return.
4. Verify exact manufacturer part numbers, footprints, availability, and assembly type for all populated parts.
5. Review the vendor's board, drill, parts, and placement previews.
6. Test a small prototype batch with current-limited power before connecting an appliance.
7. Record all eight pin-1, pin-3, and USB source combinations in the bring-up matrix.
8. Confirm USB enumeration/flashing, repeated booting, Wi-Fi load, temperatures, and no voltage backfeed.
