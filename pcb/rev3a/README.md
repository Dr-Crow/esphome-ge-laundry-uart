# Revision 3A PCB

Revision 3A keeps the ESP32-C3-WROOM-02 module from Revision 2.x and adds native
USB-C, automatic appliance-power selection, a switching 5 V supply, a stronger
3.3 V rail, and a permanent recovery header.

> [!WARNING]
> Revision 3A is an untested prototype design. The KiCad checks pass, but no
> assembled board has completed the electrical and appliance tests in
> [BRINGUP.md](BRINGUP.md). Do not connect an unqualified board to an appliance.

![Revision 3A populated-board render](validation/renders/3d-top.png)

## What changes from Revision 2.2

| Area | Revision 2.2 | Revision 3A |
| --- | --- | --- |
| ESP32 | ESP32-C3-WROOM-02 | Same module and built-in antenna |
| Programming | External programming connection | USB-C native USB plus J2 recovery header |
| Appliance power | One fixed appliance-power pin | Automatic pin 1 / pin 3 selection with pin-1 priority |
| 5 V supply | L7805 linear regulator | AP63205 switching regulator |
| 3.3 V supply | AP2205, 200 mA | AP2112K, up to 600 mA |
| USB and appliance power | Not intended for simultaneous use | Diode-isolated paths, pending prototype verification |
| Board | 88.7 x 30.1 mm, two layers | 88.7 x 40.0 mm, four layers |

## Power architecture

No user jumper is required. Each appliance input has its own resettable fuse,
CJ3407 reverse-current blocking stage, and TPS22810 controlled load switch. The
two switched outputs feed `V_INPUT` through Schottky diodes. A transistor network
gives pin 1 priority when both inputs are present.

```text
J1 pin 1 -> fuse -> reverse-current block -> load switch -> diode --+
                                                                  +-> V_INPUT -> AP63205 -> +5V
J1 pin 3 -> fuse -> reverse-current block -> load switch -> diode --+

USB-C VBUS -> fuse -> diode -----------------------------------------> +5V
```

The CJ3407 stages are intended to limit reverse current and backfeed between
sources. They are not claimed as protection against a physically reversed supply.
D18 is a populated SMF16A TVS from `PIN1_PROTECTED` to ground, following the
single-TVS placement used by the published FirstBuild reference design. Its
orientation, stand-off voltage, clamp behavior, and energy margin remain prototype
qualification items.

The FirstBuild schematic labels its downstream `V_INPUT` rail as 4.3-15 V. That is
not a measured Rev3A appliance-input range. Rev3A's actual minimum appliance
voltage, voltage drop, regulator headroom, and transient environment must be
measured before the input range is approved.

## Programming and controls

- `J4` is the normal USB-C flashing, logging, and bench-power connection.
- `J2 RECOVERY` is a populated 2-by-3, 2.54 mm header for 3.3 V UART recovery.
- `SW1 RESET` resets the ESP32-C3.
- `SW2 BOOT` selects the ROM downloader when held during reset.
- The green LED reports Wi-Fi status, yellow reports GEA-bus status, and red is a
  user-controlled diagnostic LED.

The ESP32 antenna overhangs the right edge. Keep at least 15 mm beyond that edge
clear of metal, wiring, fasteners, and enclosure ribs.

## Design and manufacturing status

- KiCad 9.0.9 ERC: zero errors and 55 reviewed warnings.
- KiCad 9.0.9 DRC: zero errors, zero unconnected items, zero schematic-parity
  findings, and seven reviewed warnings.
- Manufacturing package: 44 BOM groups and 93 fitted top-side placements.
- Board construction: four copper layers, 1.6 mm target thickness, 0.20 mm minimum
  routed track, ordinary 0.8/0.4 mm through-vias, and 0.30 mm ESP32 thermal drills.
- `In1.Cu` is a continuous ground-reference plane. `In2.Cu` is a ground plane
  except for one short D18 TVS branch; native USB remains referenced to `In1.Cu`.
- No blind or buried vias, filled vias, controlled-depth drilling, or bottom-side
  assembly is required.

These checks establish file consistency, not electrical safety or appliance
compatibility. The source files are authoritative; generated files must be
regenerated after a source change.

## Directory map

- [`design/`](design/) - editable KiCad source, local footprints, and 3D models
- [`manufacturing/`](manufacturing/) - matched Gerber, BOM, and placement files
- [`validation/`](validation/) - schematic, layer views, reports, renders, and
  community-review material
- [Rev3A enclosure](../../case/rev3a/README.md) - printable case source and exports

## Release gates

Before ordering more than a small prototype batch or connecting an appliance:

1. Complete an independent schematic, layout, BOM, and mechanical review.
2. Review the fabricator's board, drill, part-selection, and placement previews.
3. Measure the actual appliance supply range and AP63205 headroom.
4. Pass all eight steady-state source combinations and both dynamic pin-1/pin-3
   handoff directions without dropout, cross-feed, or unsafe heating.
5. Pass USB VBUS decay and appliance-to-USB no-backfeed tests.
6. Qualify D18 against measured steady-state and transient conditions, or revise
   the protection design before assembly.
7. Pass USB enumeration, flashing, sustained logging, Wi-Fi load, enclosure fit,
   connector access, and antenna-performance tests on at least two boards.

Use [BOARD_GUIDE.md](BOARD_GUIDE.md) for the user-facing board map,
[DESIGN_NOTES.md](DESIGN_NOTES.md) for engineering decisions, and
[BRINGUP.md](BRINGUP.md) for the bench procedure.
