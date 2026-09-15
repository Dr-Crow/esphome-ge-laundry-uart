# Revision 3A PCB

## Automatic power front end

Revision 3A is a no-jumper design. The proposed front end gives each appliance input an independent fuse, reverse-protection stage, and controlled switch:

```text
J1 pin 1 (VDC)  -> F2 -> CJ3407 reverse-protection PMOS -> TPS22810DBVR ->+
J1 pin 3 (ALT)  -> F1 -> CJ3407 reverse-protection PMOS -> TPS22810DBVR ->+-> V_INPUT
                                                                            |
                                                                            +-> AP63205 input
```

Each TPS22810 uses CT = 0.022 uF, a local 1 uF input capacitor, a 0.1 uF output
capacitor, and a small 100 pF/5.1 k/51 ohm PMOS gate network derived from the
published FirstBuild design. An MMBT3904 transistor and two resistors give pin 1
priority when both inputs are present. MBR0540 diodes are intended to combine the two switched
outputs without feeding one appliance pin from the other. USB power remains on its
separate F3/D10 path, and the existing buck-side D11 isolation is retained. There is
no JP2 or user-selectable power control.

Pin-1 priority, reverse protection, and source isolation are design objectives, not
qualified safety properties. Verify them with current-limited supplies in all eight
source combinations before connecting an appliance.

The AP63205 remains the prototype regulator. A measured 4.3 V source cannot produce a
regulated 5 V output; source headroom and the reverse-protection/load-switch drops are
physical release gates, not software assumptions.

### Eight-state design expectation — unverified until bring-up

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
schematic-only, do-not-install header option and is not placed on the PCB. J3 is a
top-side, no-component Tag-Connect recovery footprint carrying EN, +3V3, ESP UART TX,
GND, ESP UART RX, and BOOT. It permits 3.3 V UART flashing if the USB connector or
USB data path is unavailable without adding a per-board connector or assembly step.
SW1 is connected to `EN` and labelled `RESET`; SW2 is connected to GPIO9 and labelled
`BOOT`. Hold BOOT, tap RESET, release RESET, then release BOOT to enter the ESP32-C3
ROM downloader. A permanent 2.54 mm J2 header was evaluated, but both through-hole
and surface-mount 2-by-3 footprints conflicted with the completed routing or nearby
component courtyards at every practical top-side location. It remains omitted rather
than increasing board size or destabilizing the validated route.
JP1 is unrelated to power:
it is the inherited signal-mapping solder selector. Its manufactured copper defaults
to pads 1-2 for FirstBuild-compatible mapping; changing it is an engineering rework
that requires cutting that bridge and joining pads 2-3. Validate all eight power states
with current-limited supplies before any appliance connection.

### Buttons and indicators

- `SW1 RESET` resets the ESP32-C3. `SW2 BOOT` is only needed to force the ROM
  downloader when automatic USB flashing cannot start. Before the reset/boot cleanup,
  both switches acted on boot-strapping pins and the board had no dedicated reset
  button.
- The green LED is the Wi-Fi-connected indicator.
- The yellow LED is the GEA-bus-connected indicator.
- The red LED is currently exposed to ESPHome/Home Assistant as a user-controlled
  diagnostic light. It is reserved for a future fault pattern rather than adding a
  fourth LED or silently changing an existing entity's behavior.

USB-C is the normal programming and logging interface. The six gold pads and three
alignment holes at J3 form a reusable Tag-Connect `TC2030-IDC-NL` service interface;
they are contacted by spring pins, so the production board needs no soldered header.
The recovery cable terminates in a 2-by-3, 0.1-inch IDC socket and must be broken out
or rewired to the documented J3 pinout before connecting a 3.3 V USB-to-UART adapter.
Do not attach a generic Tag-Connect USB/FTDI cable directly: its standard pin order
does not match J3. See [BRINGUP.md](BRINGUP.md#recovery-flashing-when-usb-is-unavailable)
for the exact pin map and power precautions.

Status: digitally complete for review and quoting, but not electrically qualified. Do not order or connect this board to an appliance until the vendor previews and prototype gates below pass.

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
| Board | 88.7 mm by 30.1 mm, two layers | 88.7 mm by 40.0 mm, four layers |

The blocking diodes are one-way valves for electricity. They let either the appliance or USB power the board while preventing appliance power from being pushed back into the computer's USB port. That behavior still needs to be measured on prototypes in every source combination.

## Current state

- The schematic is complete enough for design review and opens in KiCad 9.0.9.
- The 88.7 mm by 40.0 mm board, component placement, antenna keepout, and four-layer stack are complete. `In1.Cu` and `In2.Cu` are uninterrupted ground-reference planes.
- The automatic pin-1/pin-3 power paths now reach the regulator input, and the
  lower-edge buck-converter input, switching, output, bootstrap, and feedback
  connections are routed. The feedback sense trace uses the bottom layer briefly
  and returns to the output capacitor through two standard through-vias.
- The USB-C connector is placed on the lower board edge. The complete connector-to-
  ESP32 paths measure 24.314 mm for D+ and 25.357 mm for D- (1.043 mm skew). Both
  use 0.20 mm tracks. Each crosses from `F.Cu` to `B.Cu` and back through two standard
  0.8/0.4 mm through-vias while remaining referenced to an uninterrupted internal
  ground plane. The ESD protector has a local ground via, and both connector ground
  contacts are tied to the grounded shell pads. The dimensions are manufacturing
  evidence, not a 90-ohm impedance claim; fabricator and physical USB tests remain gates.
- The ESP32 module is shifted to the right so its antenna overhangs the PCB and its
  keepout begins at the board edge. The PCB remains 88.7 mm by 40.0 mm; the enclosure
  must preserve 15 mm of antenna-side clearance outside that edge.
- Native KiCad 9.0.9 DRC reports zero errors and zero unconnected items. Five local
  footprint-copy mismatches and four intentional connector/antenna silkscreen edge
  warnings are documented in the review package. ERC reports zero errors and 55
  reviewed legacy/grid warnings; see `review/README.md` for their dispositions.
- The schematic BOM contains 42 purchasing groups / 90 fitted parts and every group
  has an exact LCSC identifier. A complete JLCPCB Economic Assembly match on
  2026-09-15 selected every group and placement and quoted five boards at $141.24
  before shipping and tax ($28.25 each). Stock and pricing must be refreshed at
  order time.
- The generated Gerber, BOM, and placement package is a review/quote artifact. Do not
  order it until the vendor previews are reviewed and the owner approves a prototype batch.

J4 uses SHOU HAN `TYPE-C 16PIN 2MD(073)` (`C2765186`) with KiCad 9's
`Connector_USB:USB_C_Receptacle_HCTL_HC-TYPE-C-16P-01A` land pattern. The
selected connector drawing matches the footprint's contact row, locating holes,
four shell slots, and body envelope. Revalidate the complete USB cluster against
the manufacturer drawing after any footprint or routing change. This match is
not manufacturing approval.

The KiCad files are the source of truth.

## Four-layer routing decision

Rev3A uses four copper layers. A complete two-layer route was tested first, but the
signal routing split the ground fill into 18 disconnected fragments and left the USB
pair without a defensible continuous return path. Adding solid `In1.Cu` and `In2.Cu`
ground planes closed every ground connection without changing component placement,
outline size, or the automatic-power and USB circuits. This is a signal-integrity and
return-current correction, not a board-size optimization.

The published FirstBuild manufacturing archive is also two-layer: it contains one
top and one bottom copper image and no inner copper layers. A JLCPCB calculator check
on 2026-09-14 priced five 88.7 mm by 34 mm bare boards at $4 total for two layers and
$7 total for four layers before shipping. That historical snapshot did not use the
current 88.7 mm by 40.0 mm outline and is not a Revision 3A price. The live assembled
quote recorded for this revision supersedes that historical comparison.

FirstBuild's Gerber outline measures about 59.94 mm by 27.43 mm. It achieves that
density with a Seeed XIAO ESP32-C3 daughterboard, which already includes USB-C and the
radio subsystem, plus carrier components placed on both sides and extensive use of
0402/0603 packages. Revision 3A keeps the native ESP32-C3-WROOM-02, larger passives,
and single-sided component placement. Its 40 mm height provides a dedicated lower-edge
buck-converter corridor without using the USB routing area. Changing to four copper
layers alone would not reduce it to FirstBuild's footprint.

The release candidate uses 0.20 mm minimum tracks. Each USB data path uses two
standard 0.8/0.4 mm through-vias, and every other routed via uses the same standard
size. U2's center pad uses twelve 0.6/0.3 mm plated thermal-ground holes, matching
Revision 2.2 and JLCPCB's standard 0.3 mm minimum-drill option. An earlier 0.2 mm
version invoked small-hole material and test charges without providing a routing or
thermal requirement. These are manufacturing limits rather than a controlled-impedance guarantee. USB enumeration,
flashing, sustained logging, and reconnect testing on the physical prototype remain
release gates even though the pair is referenced to continuous internal ground.

See [DESIGN_NOTES.md](DESIGN_NOTES.md) for the decision gates and unresolved items.
Use [BRINGUP.md](BRINGUP.md) to record current-limited prototype validation before
any appliance connection.

## Before an order can be released

1. Finish every required connection and obtain a clean schematic/PCB parity check.
2. Resolve or formally exclude every ERC and DRC finding in KiCad rather than matching a saved warning count.
3. Verify the documented four-layer USB geometry, pair-length match, stack-up, and uninterrupted ground return.
4. Verify exact manufacturer part numbers, footprints, availability, and assembly type for all populated parts.
5. Review the vendor's board, drill, parts, and placement previews.
6. Test a small prototype batch with current-limited power before connecting an appliance.
7. Record all eight pin-1, pin-3, and USB source combinations in the bring-up matrix.
8. Confirm USB enumeration/flashing, repeated booting, Wi-Fi load, temperatures, and no voltage backfeed.
