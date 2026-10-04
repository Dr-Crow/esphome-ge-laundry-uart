# PCB revisions

This directory keeps every board revision in a separate package so source files, manufacturing files, and review files do not get mixed between revisions.

[Back to the project overview](../README.md) · [PCB ordering guide](ORDERING.md)

> [!IMPORTANT]
> [Rev 3B](rev3b/README.md) is a rated-protection review prototype. Every revision, including Rev 2.2, needs revision-specific electrical and assembly qualification before a new build; no manufacturing release is established here.

## What the folders mean

- `design/` contains the editable KiCad project. A `.pretty` directory under `footprints/` is a KiCad footprint library: it defines the exact copper pads, drill holes, silkscreen, and component outline used on the board. A project `fp-lib-table` maps the library name used by the board to that local directory so footprints resolve from a clean clone. A `models/` directory, when present, contains optional 3D component shapes.
- `manufacturing/` contains files sent to a PCB assembler. Gerbers describe copper, holes, solder mask, and silkscreen; the BOM lists components; the CPL lists component positions and rotations.
- `validation/` contains files used to review the design, such as schematic PDFs, board views, drill maps, and ERC/DRC reports.
- `images/` contains photographs and explanatory renders used by documentation. Images are not manufacturing inputs.

## Revision index

| Revision | Status | Available material |
| --- | --- | --- |
| [Rev 3B](rev3b/README.md) | Soldered C3 prototype; qualification open | Dual-input automatic selection, native checks, source-matched review exports; no C6 claim. |
| [Rev 2.2](rev2.2/README.md) | Historical candidate; qualification open | Corrected KiCad source, matched factory package, and validation exports. |
| [Rev 2.1](rev2.1/README.md) | Built; superseded | KiCad 9 source, JLCPCB package, drill maps, and repair image. |
| [Rev 2.0](rev2.0/README.md) | Built; superseded | PCBA archive, schematic, board model, renders, and photographs. |
| [Rev 1.0](rev1.0/README.md) | Historical | Gerber archive only. |

> [!IMPORTANT]
> Historical RX/TX labels use an endpoint perspective; verify exact ESP GPIO-to-adapter direction. The U1 supervisor has reported boot-loop issues on Rev2.1. Historical manufacturing packages are not qualified corrected sources.

Rev 2.2 addresses those known board-file problems but is not proven until assembled boards pass electrical, appliance, and enclosure testing. Retain its three matched manufacturing files for review; passing digital checks is not manufacturing approval.

Not every revision has the same files. The table lists what is actually available; missing source files, exports, and images were not recreated.

## Historical revisions

- Rev 0.1 had unconnected grounds discovered after ordering.
- Rev 0.2 corrected the grounds but needed a diode orientation bodge and resistor changes.
- Rev 0.3 added test points, an LED, a push button, and protection diodes; three boards were tested.
- Rev 1.0 added configurable resistors for inverted GEA2 serial signaling.
- Rev 2.0 introduced an assembly-oriented ESP32-C3 design.
- Rev 2.1 updated that design and migrated its source to KiCad 9.
