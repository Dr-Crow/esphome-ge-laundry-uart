# PCB revisions

This directory keeps every board revision in a separate package so source files, manufacturing files, and review files do not get mixed between revisions.

[Back to the project overview](../README.md) · [PCB ordering guide](ORDERING.md)

> [!IMPORTANT]
> [Rev3C](rev3c/README.md) is the selected development focus, with both appliance inputs and automatic PIN1 priority. All revisions remain subject to their electrical and physical qualification gates before ordering or appliance connection.

## What the folders mean

- `design/` contains the editable KiCad project. A `.pretty` directory under `footprints/` is a KiCad footprint library: it defines the exact copper pads, drill holes, silkscreen, and component outline used on the board. A project `fp-lib-table` maps the library name used by the board to that local directory so footprints resolve from a clean clone. A `models/` directory, when present, contains optional 3D component shapes.
- `manufacturing/` contains files sent to a PCB assembler. Gerbers describe copper, holes, solder mask, and silkscreen; the BOM lists components; the CPL lists component positions and rotations.
- `validation/` contains files used to review the design, such as schematic PDFs, board views, drill maps, and ERC/DRC reports.
- `images/` contains photographs and explanatory renders used by documentation. Images are not manufacturing inputs.

## Revision index

| Revision | Status | Available material |
| --- | --- | --- |
| [Rev3C](rev3c/README.md) | Selected prototype; unqualified | Socketed C3/C6 source, matched 83-reference package, native review and illustrated quote guide. |
| [Rev 2.2](rev2.2/README.md) | Legacy review; unqualified | KiCad source, factory package and validation exports; power/current/thermal review remains. |
| [Rev 2.1](rev2.1/README.md) | Built; superseded | KiCad 9 source, JLCPCB package, drill maps, and repair image. |
| [Rev 2.0](rev2.0/README.md) | Built; superseded | PCBA archive, schematic, board model, renders, and photographs. |
| [Rev 1.0](rev1.0/README.md) | Historical | Gerber archive only. |

> [!IMPORTANT]
> UART RX/TX labels must be interpreted from the appliance or module perspective using the exact schematic. The Rev2-era U1 reset supervisor has reported ESP32 boot-loop issues. Original manufacturing archives are historical, not qualification evidence.

Rev2.2 omits that supervisor, but its input protection, regulator current capability and thermal limits still require review. No older revision is an established safe fallback. The [selected Rev3C guide](rev3c/ORDERING.md) describes its exact matched file trio and release gates.

Not every revision has the same files. The table lists what is actually available; missing source files, exports, and images were not recreated.

## Historical revisions

- Rev 0.1 had unconnected grounds discovered after ordering.
- Rev 0.2 corrected the grounds but needed a diode orientation bodge and resistor changes.
- Rev 0.3 added test points, an LED, a push button, and protection diodes; three boards were tested.
- Rev 1.0 added configurable resistors for inverted GEA2 serial signaling.
- Rev 2.0 introduced an assembly-oriented ESP32-C3 design.
- Rev 2.1 updated that design and migrated its source to KiCad 9.
