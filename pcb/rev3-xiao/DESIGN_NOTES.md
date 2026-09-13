# Revision 3B design notes

## Plain-English comparison

| Question | Revision 3A bare module | Revision 3B XIAO |
| --- | --- | --- |
| USB connector | Designed on the carrier | Built into the XIAO |
| Wi-Fi antenna | Built into the ESP32 module | Separate antenna connected to the XIAO U.FL socket |
| USB trace difficulty | Carrier must route a controlled pair | Handled inside the XIAO |
| Carrier layer target | Two layers if rerouting works; four-layer fallback | Two layers |
| MCU/module cost | Lower | Higher, currently about $5 retail |
| Carrier part count | Higher | Lower |
| Dual-source power | Carrier has explicit blocking paths | Requires a new policy/circuit and proof |
| Assembly | One assembled PCB | Carrier plus an assembled XIAO module |

The XIAO can still be competitive because its module premium replaces the USB connector, USB protection, configuration resistors, series resistors, boot/reset support, flash, RF layout, and 3.3 V supply. Only matched assembled quotes can determine the real winner.

## Power facts and implications

- Seeed documents `BAT` for a 3.7 V lithium battery and allows USB while that battery is attached.
- Seeed's maintained guidance describes the XIAO 5 V/VBUS pad as USB-derived. An external supply may feed that pad through a diode.
- The XIAO 3V3 pin is an onboard regulator output, not the preferred carrier power input.
- The published schematic connects USB VBUS to the onboard charger and connects the charger to the battery node.

Therefore a regulated supply on `VBAT` is not equivalent to a battery. With USB present, the charger can try to charge that regulated node. A regulator with reverse-current protection toward its own input does not by itself prove that the shared node is safe.

## Safe development directions

### Mutually exclusive sources

Feed regulated appliance-derived 5 V into the XIAO 5 V pad through the vendor-required diode and prohibit simultaneous USB. This has the fewest carrier parts, but the operating rule must be physically enforceable or very clear because firmware cannot prevent electrical backfeed.

### Simultaneous appliance and USB power

Use a dedicated source selector, ideal-diode controller, or load switch whose data sheet explicitly covers reverse blocking and the required voltage/current range. Validate source-only, USB-only, both, neither, and both insertion orders. No appliance-derived voltage may reach the host VBUS.

This circuit is not selected yet. It should not be added to a production carrier until a schematic review and bench fixture establish the current paths, handoff behavior, voltage drop, startup, thermal margin, and fault behavior.

## Mechanical and assembly gates

- Confirm the exact XIAO hardware revision and fitted charger before testing.
- Compare the project footprint with the official pad drawing and a physical module.
- Confirm the assembler supports turnkey placement of the XIAO underside pads; do not assume the user will solder the module.
- Keep carrier copper away from the U.FL connector and provide a safe antenna/cable location in the enclosure.
- Verify the USB-C opening, buttons, antenna lead, appliance connector, and mounting holes with a printed enclosure sample.

## Cost gate

The finished-unit goal is below the former $39.99 FirstBuild retail price, not merely a cheap bare PCB. Compare JLCPCB and PCBWay at 5, 10, and 30 complete units using the same board finish, parts, through-hole assembly, XIAO sourcing, enclosure, shipping, and expected yield. Do not publish a per-board price until the live parts review and assembly quote are complete.

## Primary references

- [Seeed XIAO ESP32-C3 getting-started and battery guidance](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/)
- [Seeed XIAO ESP32-C3 source repository](https://github.com/Seeed-Studio/OSHW-XIAO-Series/tree/main/XIAO-ESP32C3)
- [Seeed XIAO ESP32-C3 schematic](https://files.seeedstudio.com/wiki/XIAO_WiFi/Resources/XIAO_ESP32C3_v1.3_SCH_260116.pdf)
