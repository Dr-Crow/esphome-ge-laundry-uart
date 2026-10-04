# Rev 2.2 native source review — 2026-10-03

**Status: source review only; not ready to manufacture, power or connect to an appliance.**

Recovered public source: `bc0d52495bd97ed1504bd0ca0775e47feb01a648`.
Reviewed source head: `78ca806c0225fdab5c5a5f3a61c1085dce92581e` (the source cleanup, readability and local capacitor-clearance commits).
The power topology and assembly population are preserved. Both original input paths remain, but JP2 selects them manually. This legacy architecture does not provide automatic pin-1/pin-3 power selection.

## Actual native checks

Native KiCad **9.0.9** was used, including its matching `pcbnew` Python API for board save/zone refill. Checks include error, warning and exclusion severities. PCB checks use all-track-error reporting and schematic parity. No ERC/DRC exclusions were added; inherited rule severities, board design settings and net classes are unchanged.

| Check | Original source | Reviewed source |
| --- | ---: | ---: |
| ERC errors | 3 | 0 |
| ERC warnings | 164 | 0 |
| ERC total | 167 | 0 |
| DRC errors | 2 | 0 |
| DRC warnings | 62 | 0 |
| DRC total | 64 | 0 |
| Unconnected items | 0 | 0 |
| Schematic-parity issues | 0 | 0 |

The exact retained native reports are [ERC before](erc-before.json), [ERC after](erc-after.json), [DRC before](drc-before.json) and [DRC after](drc-after.json). Counts are report findings, not evidence of electrical or mechanical qualification.

## Classification and bounded changes

| Original category | Count | Treatment |
| --- | ---: | --- |
| Power pin not driven | 3 errors | Add power flags at the intended external input, GND and passive-switch output feeding U3. These describe the source topology; they do not validate ratings. |
| Endpoint off connection grid | 111 warnings | Set the project connection grid to the source's existing 25 mil grid. No wire, pin or junction moved. |
| Symbol-library mismatch | 44 warnings | Recover exact embedded definitions into a project-local library; do not replace them with newer library pin geometry. |
| Missing/obsolete symbol definitions | 5 warnings | Recover the inherited APX803L, 3.3-V buffer and obsolete PMOS definitions locally. |
| Multiple net names | 4 warnings | Align redundant DBG_LED/GLITCHES and historical UART aliases; name U4's hidden pin +5V to agree with its actual source net. |
| Footprint-library mismatch | 58 warnings | Recover the source-specific embedded footprints locally; keep copper, drills and component placement. |
| Starved thermal, U4 pad 2 | 1 error | Use a local solid GND-zone contact on this pad, retaining its existing 0.4064 mm hard route and via. Global thermal-spoke and clearance rules remain unchanged. |
| Silkscreen clipped by edge | 4 warnings | Clip/remove only overhanging U2/J1 silk primitives. Connector/module copper, holes, outlines and positions remain unchanged. |
| C9/C10 courtyard overlap | 1 error | Move C10 upward 0.30 mm and adjust only its local GND/input links and the adjacent 3.3-V route. Native courtyard boundary separation is now 0.05 mm. |

The final bounded fix moves C10 from (84.025, 99.050) mm to (84.025, 98.750) mm without changing its orientation or either pad definition. It adjusts seven existing F.Cu tracks and adds two 0.4064-mm F.Cu +3V3 segments; the remainder of the board retains its original placement and routing. C9 and C11 remain in place. [Immediate-before DRC](drc-capacitor-before.json) has exactly one courtyard error; the final native DRC has zero errors, warnings, unconnected or parity findings. [Before](capacitor-before.png) and [after](capacitor-after.png) are actual native copper/fabrication/courtyard plot pixels. They show the shared capacitor area in both revisions. No courtyard, severity, exclusion or clearance rule was changed. Physical component fit remains unqualified.

Rev 2.1's title block now agrees with its 2.1 board identity. UART silk and service documentation use the adapter/ESP perspective. The schematic annotations no longer claim a qualified input range, inrush current or successful U1 brownout behavior. Release notes are clear of the title block and the inherited illustration.

## Source preservation evidence

[Preservation proof](preservation-proof.json) records the complete cleanup exceptions; [capacitor-clearance proof](capacitor-clearance-proof.json) records every local change against source head `7b3201de09d19bec6a10d9e90b4b02792bda6972`. Each revision retains:

- 45 physical net memberships, checked from native KiCad XML netlists
- 74 footprint identities, values and assembly properties; C10 alone moves 0.30 mm and all orientations are unchanged
- 223 pads, with all sizes, shapes, numbers, nets and drills unchanged; only the two C10 pad positions move with its footprint
- All 711 original track/via items: 704 retain exact endpoints, seven local track endpoints change, and two local track segments are added (713 total); widths, layers, nets and via positions/drills are unchanged
- All component values and assembly properties

The only pad setting changed from recovered source is U4 pin 2's local zone connection from inherited (`−1`) to solid (`2`). The board is refilled by native KiCad. Zone definitions, outlines and global settings remain identical. All meaningful local copper changes fit within X 80.5–86.2 / Y 96.3–100.9 mm; native refill can re-express collinear vertices elsewhere with at most a 1.414-nm boundary rounding displacement, recorded explicitly in the proof. Bottom zone geometry is unchanged. [Source-map metadata](../design/footprints/source-map.json) identifies each project-local footprint's former library identifier. [Recovered-library notes](../design/README.md) explain the provenance and license.

The adapter-perspective UART proof is U2 pad 11 `IO20/RXD` → J2 pin 4 / J3 pin 5, and U2 pad 12 `IO21/TXD` → J2 pin 5 / J3 pin 3. Historical `GEA3_TX` is the GPIO20 receive net; historical `GEA3_RX` is the GPIO21 transmit net. J1 pin 5 is adapter TX, while pin 4 is adapter RX. Those historical net names are retained and explicitly explained.

## Matched review exports

- [Schematic PDF](schematic.pdf), [top PNG](board-top.png), [bottom PNG](board-bottom.png), and native [top SVG](board-top.svg) / [bottom SVG](board-bottom.svg)
- [Native netlist](native-netlist.xml) and [raw native component positions](native-positions.csv)
- [Gerber archive](../manufacturing/GERBER-OnionStraws-rev2.2.zip), [BOM](../manufacturing/BOM-OnionStraws-rev2.2.csv) and [CPL](../manufacturing/CPL-OnionStraws-rev2.2.csv)
- [PTH drill map](pth-drill-map.pdf) and [NPTH drill map](npth-drill-map.pdf)
- [Assembly centroid metadata](assembly-centroid-offsets.json)

Rev 2.2 retains 59 assembled references; U1 and J2 remain DNP. Native source positions and rotations match the historical CPL except C10’s explicit 0.30-mm move. BOM and regenerated CPL membership match at 59 references.

The review BOM now uses each complete native project-footprint identifier (`LegacyBoard:<reference>_<source-name>`). Grouped rows are split where those identifiers differ. All supplier LCSC IDs, component values, per-reference selections and aggregate purchasing quantities are unchanged; this naming change does not alter pads, routes or the power circuit.

The stored native PCB plot policy selects exactly F.Cu, B.Cu, F.Mask, B.Mask, F.Paste, B.Paste, F.SilkS, B.SilkS and Edge.Cuts, uses Protel extensions and subtracts mask from silk. The matching Gerber ZIP was regenerated with `kicad-cli pcb export gerbers --board-plot-params`. The front copper, paste, mask and silkscreen exports reflect the local C10 change; all five remaining layers and both drill tool/hit lists match the previous review exports apart from timestamps. Both BOMs use the JLCPCB `LCSC Part #` header.

The Gerber ZIP contains the nine native copper/paste/silk/mask/edge layer outputs, separate PTH/NPTH drills and a native Gerber job file; its ZIP integrity check passed. The original Gerber/BOM/CPL files are retained byte-for-byte under [manufacturing/original](../manufacturing/original/) and must not be mixed with the regenerated review files.

Native SVG trailing whitespace is normalized without changing rendered geometry. Both updated board-side PNGs and the capacitor before/after pixels were visually inspected. The schematic source and its previously inspected native PDF remain byte-identical; the fresh native netlist confirms the same named connections. Top/bottom board images are native 2D copper/silkscreen plots, without editor grid/chrome or displayed net names. The inherited schematic illustration is an unqualified historical rendering. These assets are not photographs, a verified 3D assembly, a component-fit test or a physical hardware test.

## Open qualification decisions

- Actual appliance pin-1 and pin-3 voltage ranges, transients, available source current and reference-ground behavior
- Automatic source selection and isolation while preserving both original appliance inputs; this manual-selector source does not implement that requirement
- U3/U6 current and thermal margins, dropout, reverse feeding, and the exact populated regulator part's input/output differential limits
- Fuse, PMOS, TVS, clamp, capacitor and resistor voltage/current/power/temperature stress under all supported conditions
- UART threshold, clamp current and back-powering behavior on the specific appliance interface
- Physical capacitor-body fit despite the cleared native courtyards; J1 footprint, drill/orientation, supplier centroid alignment and enclosure fit
- Repeatable hardware bring-up under an approved power arrangement, followed by appliance-specific qualification

Rev 2.1 additionally retains its known U1 boot-loop issue and is retired. Rev 2.2's U1 DNP status does not close any other gate. The current Rev 2.0 package holds only manufacturing/review assets, but a public historical editable snapshot exists at `af1f2c40029ef67c56910fb2c55feac835553525`. Source/export pairing and native ERC/DRC/parity for that snapshot are outside this Rev 2.1/2.2 pass and remain pending. No CAD was fabricated from manufacturing assets.

Direct 3.3-V programmer VCC injection into J2/J3 is not an approved power arrangement. No input range, current limit, fallback board or test recipe is approved by this review. See the [service interface and power boundary](../STANDALONE-REVIEW.md#service-interface-and-power-boundary).

## Tool provenance and reproduction

- KiCad CLI / native Python API: `9.0.9`
- Official symbol-library 9.0.9 head: `ad36cd14bcd1b1cd0484f629ccdd3481366f74f3`
- Official footprint-library 9.0.9 head: `2b941bf1d97862be429793b46fd52a5add09a2fc`
- Verified KiCad AppImage SHA-256: `212181f4a3c105f200c363992ff6437666869a0169a97e9129110d20a0d8312a`

The review used the pinned official install activated by `/workspace/shared/ge-oct3-tools/activate.sh`; project-local source libraries are part of the checkout. With native KiCad 9.0.9 and its official 9.0.9 libraries configured, run from this revision's `design/` directory:

```sh
kicad-cli sch erc --severity-all --format json --output erc.json OnionStraws.kicad_sch
kicad-cli pcb drc --severity-all --all-track-errors --schematic-parity --format json --output drc.json OnionStraws.kicad_pcb
```

[Export provenance and hashes](export-provenance.json) identifies the exact input bytes and output files. No remote write, PR, order, live appliance test or electrical energization was performed.
