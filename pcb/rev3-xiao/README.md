# Revision 3B XIAO carrier

Status: mechanical and architecture study. This is not a complete circuit or an orderable board.

Revision 3B explores replacing the bare ESP32 module and carrier USB circuit with a Seeed Studio XIAO ESP32-C3 module. The XIAO supplies the ESP32, flash memory, USB-C connector, boot/reset controls, 3.3 V regulator, and a U.FL connector for its external Wi-Fi antenna.

## Why consider it

- USB flashing is already implemented on the module.
- The carrier can remain a normal low-cost two-layer board because it does not route USB data or design the ESP32 RF section.
- It removes several small USB and 3.3 V parts from the carrier.
- It resembles the FirstBuild approach and may be easier for new contributors to understand.

## Tradeoffs

- The XIAO costs more than a bare ESP32-C3-WROOM-02.
- Its separate antenna and cable need protected space in the enclosure.
- The underside pads require an assembler that can place and reflow the module; the target remains a no-hand-solder order.
- The module's USB, charger, battery input, and 5 V pad are not a general-purpose dual-source power system. Safely using appliance power while USB is attached needs an explicit, tested power policy.
- Availability and board-revision changes are controlled by the module vendor rather than this project.

## Current files

- `GEA-Adapter-Rev3B-XIAO-Placement.kicad_pcb` is a two-layer mechanical placement study using the Revision 3 outline. It has no complete circuit or routing and must not be fabricated.
- `footprints/GEA_XIAO.pretty/XIAO-ESP32-C3-v1.3-SMD.kicad_mod` is the project-local 22-pad XIAO footprint derived from Seeed's published source. Its source and license are recorded beside it.

The KiCad files are the source of truth. Only the reviewable design files and supporting documentation belong in this branch.

## Power decision

The previously studied idea of feeding regulated 4.0 V into the XIAO `VBAT` pad is not approved. Seeed documents that pad for a 3.7 V lithium cell. When USB is attached, the onboard charger can source current into the same node, so a normal regulator connected there may be driven from its output side or contend with the charger.

The remaining choices are:

1. Use appliance power and USB only one at a time, feeding external 5 V through the diode arrangement documented by Seeed. This is simple but makes live USB debugging while installed unavailable.
2. Add a qualified source-selection or reverse-blocking power circuit and prove it in all four source states. This preserves live USB use but adds parts and validation work.
3. Keep Revision 3A as the production design when simultaneous appliance and USB power is a requirement.

See [DESIGN_NOTES.md](DESIGN_NOTES.md) for the decision gates.
