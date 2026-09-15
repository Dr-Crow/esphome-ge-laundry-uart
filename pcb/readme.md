> [!IMPORTANT]
>
> Rev 2.0 and 2.1 PCBs have two known issues.
>
> * The printed RX and TX labels are swapped.
> * `U1`, an optional voltage-monitor chip, can repeatedly reset the ESP32. Order those revisions without U1 installed. On an existing board, removing U1 or cutting the small trace between U1 pin 2 and the nearby via removes it from the circuit.

## Hardware revision guide

| Revision | Status | Summary |
| --- | --- | --- |
| 0.1 | Superseded | First PCB attempt. Some ground connections were missing. |
| 0.2 | Superseded | First built revision. D4 required a physical rework and two resistors needed to be removed or changed. |
| 0.3 | Tested | Added test points, an LED, a push button, and protection diodes. Three boards were tested with a washer and dryer. |
| 1.0 | Superseded | Added resistor options for inverted GEA2 serial signaling. |
| 2.0 | Built with known issues | Changed to the ESP32-C3 module and redesigned the board for factory assembly. RX/TX are mislabeled and U1 can cause boot loops. |
| 2.1 | Built with known issues | Refined the Rev 2 layout, protection-diode footprint, power/test connections, and manufacturing files. It retains the Rev 2.0 RX/TX and U1 problems. |
| 2.2 | Manufacturing candidate | Corrects the two Rev 2.x problems without redesigning the circuit. Its files pass package-consistency checks, but known legacy ERC/DRC findings remain and no physical Rev 2.2 board has been tested. See the [Rev 2.2 ordering and validation guide](rev2.2/README.md). |
| 3A | Review-ready prototype design | Keeps the ESP32-C3 module while adding USB-C, automatic pin-1/pin-3 appliance-power selection, dedicated reset/boot buttons, three status LEDs, and a populated recovery header. It remains unqualified until independent review, vendor previews, and prototype bring-up pass. See the [Rev 3A board guide](rev3/BOARD_GUIDE.md). |

## Manufacturing file guide

- A **Gerber ZIP** describes the board shape, copper, holes, solder mask, and printed labels.
- A **BOM** (bill of materials) is the factory shopping list. It says which part belongs at each reference such as `U2` or `J1`.
- A **CPL**, centroid, or pick-and-place file tells the assembler where each part goes and how it is rotated.
- **SMT** parts sit on surface pads and are normally placed by machine. **Through-hole** parts have pins that pass through drilled holes and are wave- or manually soldered by the assembler.
- `J1` is the through-hole appliance cable connector. It belongs in both the Rev 2.2 BOM and CPL so an assembler has its part number, location, and orientation. A no-hand-solder order is possible only when the vendor's parts review and assembly preview explicitly show J1 as installed.
- `J2` is an unpopulated row of six standard through-holes for service access. Revision 2.2 leaves it unchanged and adds no connector or enclosure cost.
- `J3` is a second six-signal service connection made only from flat copper contacts and alignment holes. A compatible Tag-Connect cable or reusable pogo fixture can contact it without soldering or adding a factory-installed part.

The older files under `gerber5/` and `jlcpcb/` describe Rev 2.1. For a Rev 2.2 quote, use only the three matching files under `rev2.2/production/`.

### Rev 2.2

Rev 2.2 makes the smallest practical correction to Rev 2.1:

- The factory no longer installs `U1`, an optional chip that monitors voltage and resets the ESP32. Existing boards showed that it can repeatedly reset the ESP32 instead, so the footprint remains available for experiments but the normal assembly leaves it empty.
- The printed RX and TX connector labels are corrected.
- `Q1` now has the same supplier catalog number as the identical `Q2`. This changes only the factory shopping data; it does not change the circuit or silkscreen.
- `J1` retains the original low-cost EVERCOM `5301-8P8C` (`C3097717`). Its eight signal holes now use the manufacturer's recommended 0.90 mm diameter; the connector position and two 3.20 mm locating holes are unchanged. Confirm the connector orientation and drill pattern in the vendor preview and prototype batch before production use.
- Two existing bottom-side solder selectors choose the appliance wiring. `JP1` selects the FirstBuild-compatible signal mapping. `JP2` selects the normal or alternate appliance power input; both are manufactured with pads 1-2 connected by default. Changing either requires cutting the existing copper bridge and soldering the other pair.
- The existing `J2` through-holes and flat `J3` Tag-Connect pads remain available for debugging. Neither is populated by the factory in this minimal revision.
- A new Gerber, BOM, and CPL set is kept in its own directory so it cannot be mixed with Rev 2.1 files.

### Rev 2.1

Rev 2.1 enlarged the D8 protection-diode footprint, added a ground test point, moved the appliance connector farther inside the board edge, adjusted the 5 V regulator footprint, and refreshed the manufacturing files. It retained the Rev 2.0 RX/TX label and U1 reset problems.

### Rev 2.0

Rev 2.0 redesigned the board for factory assembly, replaced the DC/DC converter with a linear regulator, and changed to an ESP32-C3 module compatible with the FirstBuild adapter pinout. Historical manufacturing files are included, but Rev 2.0 is not recommended for new orders because of the known RX/TX label and U1 reset problems.

![v2 Render](https://github.com/user-attachments/assets/77eab417-817f-48a1-bfa4-fbe587ed5843)

Existing Rev 2.0/2.1 U1 rework:

![v2 fix.png](https://github.com/mulcmu/esphome-ge-laundry-uart/blob/main/pcb/v2%20fix.png?raw=true)


### Rev 1.0

Added 3 resistors in case GEA2 is inverted serial.  The full duplex serial line can now be configured with either pull up or pull down resistors as needed.

### Rev 0.3

Added test points, LED, Push button and two more protection diodes.  Built and tested 3 boards with both washer and dryer.  No issues.

![OnionStraws](https://user-images.githubusercontent.com/10102873/151646053-841ecb00-9c4c-4cec-b6ba-a1de453bc428.png)

### Rev 0.2

Built and tested.  D4 diode wrong way for the half duplex GEA1.  Mounted upside down for bodge fix.  R7 and R3 need removed or changed to pull down instead of pull up.

![2022-01-28 22 47 21](https://user-images.githubusercontent.com/10102873/151646299-4b15c27d-1e0b-475f-a76f-1d3a9e918ef6.jpg)

### Rev 0.1

Ran DRC, didn't see the unconnected nets tab.  Some of the grounds were not connected.  At least Rev 0.2 placed on order before Rev 0.1 shipped.
