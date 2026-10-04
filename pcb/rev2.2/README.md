# PCB Rev 2.2: unqualified source review

Rev 2.2 is a historical correction of the Rev 2.1 source. Its original architecture is retained for review; it is not a qualified manufacturing release or approved appliance fallback.

> [!WARNING]
> Power/source/current ratings and physical qualification are unresolved. Native KiCad ERC/DRC is clean after a local C10 move and reroute. Neither manual JP2 configuration provides the requested automatic selection between appliance pin 1 and pin 3. Do not order or power this board on the strength of clean ERC, the old quote, or the archived manufacturing files.

## Architecture and source differences

- U1 remains on the source board but is Do Not Populate in Rev 2.2 because it caused ESP32 boot loops on existing Rev 2 boards. R3 retains EN pull-up. Neither board button is a reset button.
- Both original appliance power-input paths remain present through F1/F2. JP2 is a manual three-pad selector, with its original pads-1/2 copper bridge. It does not automatically select, isolate or combine the two sources.
- JP1 retains its original FirstBuild-compatible signal selector. No new user jumper, USB connector or automatic power-selection circuit has been added.
- J1 retains the original EVERCOM `5301-8P8C` catalog intent (`C3097717`) and the inherited Rev 2.2 0.90 mm signal holes / 3.20 mm locating holes. Connector orientation, drill fit and enclosure clearance are unqualified.
- Q1/Q2 retain the matching `C10493` catalog metadata. The historical Rev 2.2 BOM retains R22 `C17673`, R18/R21 `C104108` and U6 `C19268131`. Catalog entries do not establish circuit ratings or availability.

The source cleanup recovers embedded symbol and footprint definitions into local project libraries, aligns the connection-grid metadata with the existing 25 mil drawing, removes contradictory net aliases and clips silkscreen that lay beyond the board edge. U4 pad 2 now makes a solid contact with its GND zone while retaining the existing routed ground connection and via. All 74 component identities and 223 pad definitions remain unchanged. C10 alone moves upward 0.30 mm; seven local track endpoints change and two local segments are added (713 track/via items total). Full source preservation evidence is in the [native review report](validation/REVIEW.md).

## Adapter-perspective signal mapping

- J1 pin 5: adapter/ESP TX to appliance RX
- J1 pin 4: appliance TX to adapter/ESP RX
- J2 pin 4: adapter/ESP RX (`GPIO20`); connect UART TX only under a qualified power arrangement
- J2 pin 5: adapter/ESP TX (`GPIO21`); connect UART RX only under a qualified power arrangement
- J3 pin 3: adapter/ESP TX; pin 5: adapter/ESP RX

J2/J3 are unpopulated service interfaces. They are not USB. Programmer VCC leads must remain disconnected; directly injecting 3.3 V on their regulator-output rail is not a qualified power method. See the [service interface and power boundary](STANDALONE-REVIEW.md#service-interface-and-power-boundary).

## Review package

- [KiCad project](design/OnionStraws.kicad_pro), [schematic source](design/OnionStraws.kicad_sch) and [PCB source](design/OnionStraws.kicad_pcb)
- [Source-library provenance](design/README.md) and [native validation report](validation/REVIEW.md)
- [Schematic PDF](validation/schematic.pdf), [top view](validation/board-top.png) and [bottom view](validation/board-bottom.png)
- [Source-matched Gerber ZIP](manufacturing/GERBER-OnionStraws-rev2.2.zip), [BOM](manufacturing/BOM-OnionStraws-rev2.2.csv) and [CPL](manufacturing/CPL-OnionStraws-rev2.2.csv), for review only

The views are native 2D source plots. They do not prove component-body, connector or enclosure fit and are not photographs or verified 3D assemblies. DNP crosses in the schematic mark intentionally unassembled parts.

A September 19, 2026 quote was $78.07 before shipping and tax for five assembled boards. It is historical pricing, not current availability or authorization to manufacture. No order or appliance test was performed in this source review.

The review BOM now uses each complete native project-footprint identifier (`LegacyBoard:<reference>_<source-name>`). Grouped rows are split where those identifiers differ. All supplier LCSC IDs, component values, per-reference selections and aggregate purchasing quantities are unchanged; this naming change does not alter pads, routes or the power circuit.

[PCB revision index](../README.md) · [Release status](STANDALONE-REVIEW.md#release-status) · [Rev 2 enclosure](../../case/rev2/README.md)

[Standalone candidate scope and release boundaries](STANDALONE-REVIEW.md).
