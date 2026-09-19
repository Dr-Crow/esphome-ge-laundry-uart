# Revision 3A board guide

Revision 3A uses the same ESP32-C3-WROOM-02 module as Revision 2.x while adding
USB-C, automatic appliance-power selection, separate RESET and BOOT buttons,
three status LEDs, and a permanent recovery header.

> [!WARNING]
> This board is an untested prototype. Follow [BRINGUP.md](BRINGUP.md) before
> connecting it to an appliance.

![Revision 3A populated-board render](validation/renders/3d-top.png)

The appliance connector is on the left, USB-C is along the lower edge, and the
ESP32 antenna overhangs the right edge.

## Connectors, controls, and indicators

| Marking | Function | Normal use |
| --- | --- | --- |
| `J1` | Appliance 8P8C connector | Power and GEA serial bus after prototype qualification |
| `J4` | USB-C | Normal flashing, logging, and bench power |
| `J2 RECOVERY` | 2-by-3 recovery header | Backup 3.3 V UART flashing with the enclosure open |
| `SW1 RESET` | Reset button | Restart the ESP32-C3 |
| `SW2 BOOT` | Boot-mode button | Hold during reset to enter the ROM downloader |
| `D4` green | Wi-Fi status | Firmware-controlled Wi-Fi-connected indication |
| `D5` red | Diagnostic | User-controlled diagnostic indication |
| `D6` yellow | GEA status | Firmware-controlled appliance-bus indication |

Keep at least 15 mm beyond the antenna edge clear of metal and wiring.

## Automatic appliance power

Different appliance harnesses can supply power on J1 pin 1 or pin 3. Rev3A does
not use a selection jumper:

- each input has a resettable fuse and reverse-current blocking stage;
- controlled load switches select the source and give pin 1 priority;
- Schottky diodes are intended to keep the two appliance inputs isolated; and
- the USB power path is diode-isolated before it joins the 5 V rail.

This circuit is intended to prevent source-to-source backfeed. It is not claimed
to tolerate a physically reversed appliance supply. All source combinations and
handoff transitions must be tested with current-limited bench supplies.

## Normal flashing

1. Leave J1 disconnected for initial bench work.
2. Connect J4 to a computer with a USB-C data cable.
3. Flash using the ESP32-C3 native USB interface.
4. If automatic download mode does not start, hold `SW2 BOOT`, tap and release
   `SW1 RESET`, then release BOOT after the downloader starts.

## Recovery flashing

J2 is a backup for an unavailable USB data path. Use a 3.3 V logic USB-to-UART
adapter and female Dupont leads. Never apply 5 V logic, and never drive J2's 3.3 V
pin while USB-C or the appliance is powering the board. The exact pin map and
sequence are in [BRINGUP.md](BRINGUP.md#recovery-flashing-through-j2).

The matching enclosure keeps J2 inside the case. Remove the lid before attaching
recovery leads, then disconnect them before closing the enclosure or connecting an
appliance.

## More information

- [Revision overview](README.md)
- [Design decisions](DESIGN_NOTES.md)
- [Prototype bring-up](BRINGUP.md)
- [Review package](validation/README.md)
- [Manufacturing package](manufacturing/README.md)
- [Printable enclosure](../../case/rev3a/README.md)
