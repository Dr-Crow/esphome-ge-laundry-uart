# PCB revisions

This directory keeps every board revision in a separate package so source files, manufacturing files, and review files do not get mixed between revisions.

[Back to the project overview](../README.md) · [PCB ordering guide](ORDERING.md)

> [!IMPORTANT]
> Every revision needs its own source, electrical, assembly and physical qualification before a new build. Rev2.2 retains unresolved regulator/current and protection limits; it is not a released fallback. Older packages remain for review and project history.

## What the folders mean

- `design/` contains the editable KiCad project. A `.pretty` directory under `footprints/` is a KiCad footprint library: it defines the exact copper pads, drill holes, silkscreen, and component outline used on the board. A project `fp-lib-table` maps the library name used by the board to that local directory so footprints resolve from a clean clone. A `models/` directory, when present, contains optional 3D component shapes.
- `manufacturing/` contains files sent to a PCB assembler. Gerbers describe copper, holes, solder mask, and silkscreen; the BOM lists components; the CPL lists component positions and rotations.
- `validation/` contains files used to review the design, such as schematic PDFs, board views, drill maps, and ERC/DRC reports.
- `images/` contains photographs and explanatory renders used by documentation. Images are not manufacturing inputs.

## Revision index

| Revision | Status | Available material |
| --- | --- | --- |
| [Rev 3H](rev3h/README.md) | Review candidate; qualification open | Rev 3G plus the J7 3.3 V listen-only GEA bus monitor header (R48–R50) and C16/C17 moved to a JLC basic part. Base with J7/JP3 tail pockets in `rev3h/case`. |
| [Rev 3G](rev3g/OPEN-FIRST.html) | Service prototype for review (ChatGPT); qualification open | Rev 3F with the cuttable JP3 5 V link (replaces R47), JP4 GEA3-TX mute link, plated TP4–TP7 probe holes and closed-USB lids. |
| [Rev 3F](rev3f/README.md) | Cost-down review (ChatGPT); qualification open | Rev 3E with 8 bypass caps moved to 0603 C14663, widened In2 power traces and split eFuse paste. |
| [Rev 3E](rev3e/README.md) | As-quoted probe-pad prototype; qualification open | The board of the 2026-11-25 JLC quote ($94.22 for 5): PIN3 overvoltage lockout, SRV05-4 ESD, TP12–TP18. Quote and cost review in `rev3e/`. |
| [Rev 3D](rev3d/README.md) | Candidate; qualification open | TPS259470A eFuse priority mux, PIN1 overvoltage lockout, SMF17A input TVS. |
| [Rev 3C](rev3c/README.md) | Selected socketed C3/C6 prototype; qualification open | Rated dual-input source, four firmware profiles, corrected stencils, factory trio, partial component previews and illustrated ordering guide. |
| [Rev 3B](rev3b/README.md) | Rated soldered-C3 alternative; qualification open | Native source, matched factory package, typed placement evidence and partial C3 previews; exact module stock remains a gate. |
| [Rev 3A](rev3a/README.md) | Rated integrated-C3 alternative; qualification open | Native source, matched factory package, reviewed USB shell slots/lands and placement evidence; assembler solder/retention review remains open. |
| [Rev 2.2](rev2.2/README.md) | Historical candidate; qualification open | Corrected KiCad source, matched factory package, and validation exports. |
| [Rev 2.1](rev2.1/README.md) | Historical; superseded; qualification open | Corrected KiCad source, source-bound supplier files, drill maps and explicit placement conventions. |
| [Rev 2.0](rev2.0/README.md) | Historical; qualification open | Restored editable source, regenerated current CAM and preserved original PCBA archive; current supplier BOM/CPL and rotations remain unqualified. |
| [Rev 1.0](rev1.0/README.md) | Historical; qualification open | Restored editable source, regenerated current CAM and preserved original Gerber archive; original purchasing/module/buck identity remains missing. |

> [!IMPORTANT]
> Historical RX/TX labels use an endpoint perspective; verify the exact ESP GPIO-to-adapter direction rather than inferring a hardware swap. The U1 supervisor has reported boot-loop issues on Rev2.1. Historical manufacturing packages are not qualified corrected sources.

Rev 2.2 addresses those known board-file problems but is not proven until assembled boards pass electrical, appliance, and enclosure testing. Keep the three matched files together for review; qualification and exact supplier process approval are still required before ordering.

All seven revisions have fresh full-severity native ERC/DRC and intended-rule checks with no findings. Source/CAM parity passes for all seven; complete source-bound BOM/CPL checks pass Rev2.1/2.2/3A/3B/3C. Rev1/Rev2's missing current supplier inputs remain explicit CI failures. All release gates remain open. See [validation](../docs/revision-comparison/VALIDATION.md) and the [finish plan](../docs/revision-comparison/FINISH-PLAN.md).

## Historical revisions

- Rev 0.1 had unconnected grounds discovered after ordering.
- Rev 0.2 corrected the grounds but needed a diode orientation bodge and resistor changes.
- Rev 0.3 added test points, an LED, a push button, and protection diodes; three boards were tested.
- Rev 1.0 added configurable resistors for inverted GEA2 serial signaling.
- Rev 2.0 introduced an assembly-oriented ESP32-C3 design.
- Rev 2.1 updated that design and migrated its source to KiCad 9.
