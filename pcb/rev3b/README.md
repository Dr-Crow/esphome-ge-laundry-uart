# PCB Rev 3B review candidate

Rev 3B is a design in progress under review: PCB routing is unfinished, and there is no final case or assembled-board quote. It is not orderable. The [PCB revision index](../README.md) still points to [Rev 2.2](../rev2.2/README.md).

[Back to the PCB revision index](../README.md) · [Ordering guide](../ORDERING.md) · [Firmware examples](../../firmware/README.md)

## What Rev 3B is

Rev 3B uses a Seeed XIAO ESP32-C3 module with built-in USB-C, BOOT/RESET buttons, and an external antenna. It follows the approach of the [FirstBuild GE appliance adapter](https://github.com/geappliances/home-assistant-adapter). Rev 3A instead uses an ESP32-C3-WROOM-02 module and a separate USB connector on the carrier.

The antenna comes with the XIAO module; factory installation still needs confirmation. The carrier footprint follows Seeed's official 22-pad drawing.

The [KiCad 9 project](design/GEA-Adapter-Rev3B.kicad_pro), [schematic source](design/GEA-Adapter-Rev3B.kicad_sch), and [PCB source](design/GEA-Adapter-Rev3B.kicad_pcb) are available for design review. The provisional PCB uses four copper layers and measures 99 x 40 mm, with USB-C extending about 1 mm beyond the edge. This is 10.3 mm longer than Rev 3A's PCB; the extra space accommodates the XIAO while retaining much of the input circuitry's placement.

Routing, enclosure fit, manufacturing files and assembled-board pricing are still pending. The board has unconnected nets and must not be fabricated from this source. The J2 3D model's seating position also needs verification before enclosure clearances are finalized. These files are not a fabrication release.

## One power source at a time

Rev 3B adds circuitry to automatically select between GE appliance pin 1 and pin 3 power, so the same board works with either wiring without a solder-selector change. Only one external supply may be physically connected to the board at a time: USB, appliance power, or a regulated 5 V supply on `J2`. There is no simultaneous-source protection circuit, and appliance power energizes the same rail as USB VBUS — connecting both at once can back-feed a computer through the USB cable. Rev 3B also does not support battery operation.

## Module power pins

On the XIAO ESP32-C3 module:

- Pad 14 (`5V`) is an input/output pin.
- Pad 12 (`3V3`) is output only from the module's onboard regulator. Never drive or inject power into it.
- Pad 21 (`VBAT`) is unused on this board.

## Connection and recovery

| Interface | Purpose | Appliance | USB | Notes |
| --- | --- | --- | --- | --- |
| USB-C | Native flashing and USB logging | Unplugged | Connected | Hold BOOT while connecting, release when the bootloader port appears. |
| Appliance service port | Normal operation and Wi-Fi diagnostics | Connected | Unplugged | See the [firmware guide](../../firmware/README.md) for the connection steps. |
| `J2` | Backup programming when USB access is impractical | Unplugged | Unplugged | Requires its own regulated 5 V supply; see below. |

`J2` is a permanent, factory-populated, SMD 2x3 header. Its design-candidate pinout, not yet confirmed on assembled hardware:

| J2 pin | Signal |
| --- | --- |
| 1 | Regulated 5 V in, through an isolation diode |
| 2 | Ground |
| 3 | Boot (GPIO9) |
| 4 | Module RX (GPIO20) |
| 5 | Module TX (GPIO21) |
| 6 | Enable |

Use a **3.3 V logic** USB-to-UART adapter: adapter TX connects to J2 pin 4, and adapter RX to pin 5. Pin 1 accepts a regulated 5 V supply; never feed that voltage into a signal pin or the module's `3V3` output. If the supply and UART adapter are separate devices, join their grounds at J2 pin 2. Some UART adapters cannot supply enough current, so check the adapter's rating. The [firmware guide](../../firmware/README.md#j2-backup-programming-design-candidate) explains the boot sequence. J2 can bypass a damaged USB connector, but not a damaged processor or regulator.

The board also has two mounting points and three status LEDs on GPIO2, GPIO3, and GPIO4, alongside the module's onboard BOOT and RESET buttons.

## GE bus connections

| Bus | TX | RX |
| --- | --- | --- |
| GEA2 | GPIO5 | GPIO10 |
| GEA3 | GPIO21 | GPIO20 |

See the [firmware guide](../../firmware/README.md) for the matching ESPHome configuration and the `seeed_xiao_esp32c3` board substitution.

## Case and ordering status

Rev 3B is not orderable. See [Rev 2.2](../rev2.2/README.md) and its [ordering guide](../ORDERING.md), which is the current manufacturing candidate with physical bring-up testing still pending.

## Sources

- [Seeed XIAO ESP32-C3 getting started guide](https://wiki.seeedstudio.com/XIAO_ESP32C3_Getting_Started/)
- [GE Appliances home-assistant-adapter getting-started guide](https://github.com/geappliances/home-assistant-adapter/blob/main/doc/getting-started.md)
- [XIAO module footprint source](design/footprints/SOURCE.md) and [3D clearance model notes](design/models/README.md)
