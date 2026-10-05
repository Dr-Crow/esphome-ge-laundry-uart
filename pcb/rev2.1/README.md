# PCB Rev 2.1: retired, source review only

> **Current purchasing correction:** R18/R21 now select C104108 (220k) and R22 selects C17673 (4.7k), matching the declared values and the later Rev2.2 intended-part correction. The [review and exact delta](validation/RESISTOR-CATALOG-CORRECTION.md) preserve the original conflicting archives and unchanged circuit/placement/CAM. Loaded-interface, power, supplier and physical qualification remain open.

Rev 2.1 retains its original architecture and assembly population, including U1. It is the last built Rev 2.x source before the historical Rev 2.2 corrections.

> [!WARNING]
> U1 is known to cause ESP32 boot loops. This cleanup does not qualify the power circuit or repair that architecture. Rev 2.1 is retired, has clean native ERC/DRC after the local capacitor fix, and is not an approved board to order or an appliance fallback. Existing manufactured boards retain historical UART silkscreen; verify its endpoint perspective before interpreting the labels.

## Recovered and reviewed files

- [KiCad project](design/OnionStraws.kicad_pro), [schematic](design/OnionStraws.kicad_sch) and [PCB](design/OnionStraws.kicad_pcb)
- [Source-library provenance](design/README.md)
- [Native validation report](validation/REVIEW.md)
- [Readable schematic PDF](validation/schematic.pdf)
- [Top board view](validation/board-top.png) and [bottom board view](validation/board-bottom.png)
- [Source-matched Gerber archive](manufacturing/GERBER-OnionStraws-rev2.1.zip), [BOM](manufacturing/BOM-OnionStraws-rev2.1.csv) and [CPL](manufacturing/CPL-OnionStraws-rev2.1.csv), retained for review only
- [Plated-hole drill map](validation/pth-drill-map.pdf), [non-plated-hole drill map](validation/npth-drill-map.pdf) and [historical U1 illustration](images/u1-trace-fix.png)

The inherited schematic title said 2.0. It now agrees with the board's 2.1 identity. Net memberships, component identities and assembly population are preserved. C10 alone moves 0.30 mm with a bounded local reroute; all other placements and routes are preserved. Local source libraries make obsolete or missing definitions recoverable without adopting a newer library's pad geometry. No rule severity or global clearance was lowered.

J1 pin 5 is adapter TX to appliance RX; pin 4 is appliance TX to adapter RX. J2 pin 4 is adapter RX and pin 5 is adapter TX. J3 pin 3 is adapter TX and pin 5 is adapter RX. This source's silkscreen is corrected to that perspective; older fabrication archives and physical boards must not be assumed to match. [Service interface and power boundary](STANDALONE-REVIEW.md#service-interface-and-power-boundary).

Both original appliance power inputs remain present through F1/F2 and manual JP2 selection. Automatic pin-1/pin-3 power selection is absent. Input/source/current ratings, component stress, regulator heat/reverse feeding and connector/enclosure fit require separate qualification. Do not power the board through a programmer's VCC lead.

The review BOM now uses each complete native project-footprint identifier (`LegacyBoard:<reference>_<source-name>`). Grouped rows are split where those identifiers differ. All supplier LCSC IDs, component values, per-reference selections and aggregate purchasing quantities are unchanged; this naming change does not alter pads, routes or the power circuit.

The existing CPL uses reviewed pad-bounding-box centers for J1/U3/U6 and native footprint anchors for all other assembled references. See the [placement convention proof](validation/PLACEMENT-REVIEW.md). This export-parity result is separate from supplier package/alignment approval.

[PCB revision index](../README.md) · [Release status](STANDALONE-REVIEW.md#release-status) · [Rev 2 enclosure](../../case/rev2/README.md)

[Standalone candidate scope and release boundaries](STANDALONE-REVIEW.md).
