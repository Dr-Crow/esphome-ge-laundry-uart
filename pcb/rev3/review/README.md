# Rev3A review package

The KiCad schematic and PCB are authoritative. The files in this directory are
derived review artifacts and must be regenerated after either source changes.

The package includes a one-page schematic PDF/PNG, top and mirrored-bottom copper
plots, both internal-plane plots, clean top and bottom assembly drawings, a
dimensioned outline, straight-down and isometric 3D views, ERC/DRC reports, and
plated/non-plated drill maps and reports. The bottom assembly drawing is
intentionally sparse because every fitted component is on the top side.

| Artifact | Purpose |
| --- | --- |
| `schematic.pdf` / `schematic.png` | Light-background, grid-free schematic with revisioned title block |
| `top.png` / `bottom.png` | Fabricated outer-layer views; bottom is mirrored for inspection |
| `inner1.png` / `inner2.png` | Individual internal ground-plane views |
| `assembly-top.pdf` / `assembly-top.png` | Top fabrication outlines and reference designators without value-text clutter |
| `assembly-bottom.pdf` / `assembly-bottom.png` | Bottom fabrication and hole view; no fitted bottom components |
| `dimensions.pdf` / `dimensions.png` | 88.70 mm by 40.00 mm outline and hole locations |
| `3d-top.png` | Mandatory straight-down populated-board view in top-layer orientation |
| `3d-isometric.png` | Optional angled view for component-height and connector inspection |
| `3d-bottom.png` / `3d-side.png` | Underside and connector-height inspection |
| `drc.*` / `erc.*` | Current KiCad 9.0.9 report outputs and reviewed warning counts |
| `*-drl_map.pdf` / `drill.rpt` | Plated and non-plated drill review |

All 91 fitted references resolve to a 3D model. SW1/SW2 and F1/F2 use repository-
local exact-part models because their old KiCad-library filenames are not present
in the current KiCad 9 installation. J1 uses a deliberately simplified STEP
envelope derived from its
manufacturer drawing because the catalog part has no official 3D model. Its socket
opening is oriented at the left board edge and its envelope matches the drawing's
outer dimensions, but internal latch/contact geometry is not modeled; use the
drawing and a physical connector for final mechanical qualification.

Use [REVIEW_CHECKLIST.md](REVIEW_CHECKLIST.md) to track the remaining human,
vendor-preview, and physical-prototype gates. Before publishing the package to a
community, confirm that community's current posting rules and use separate direct
links for each artifact rather than expecting reviewers to navigate the repository.
The vendor-neutral [review brief](REVIEW_REQUEST.md) separates schematic questions
from layout/BOM questions and summarizes all known untested claims.

## Review order

1. Review connector pinout, power-source priority and isolation, USB-C wiring,
   test points, and DNP items in the schematic.
2. Compare the PCB against the schematic. Check connector orientation, antenna
   keepout, USB geometry and return path, power switching loops, silkscreen, and
   drills.
3. Run ERC and DRC from the current KiCad project. A saved report or image is not
   proof that the source still matches it.
4. Check every fitted BOM row for value, package, rating, exact manufacturer part
   number, and sourcing identifier. Confirm that the CPL covers the same 91 fitted
   parts.
5. Use `dimensions.png` and the enclosure models to check the outline, mounting
   holes, connector openings, button height, J2 clearance, and antenna keepout.
6. Separately inspect the vendor's board, drill, parts, and placement previews.

The schematic review follows the presentation guidance from the
[r/PrintedCircuitBoard schematic](https://www.reddit.com/r/PrintedCircuitBoard/wiki/schematic_review_tips/),
[PCB](https://www.reddit.com/r/PrintedCircuitBoard/wiki/pcb_review_tips/), and
[BOM](https://www.reddit.com/r/PrintedCircuitBoard/wiki/bom_review_tips/) review
checklists: light-background schematic, lossless top/bottom views, readable
silkscreen, visible orientation marks, and exact purchasing data.

## ERC dispositions

KiCad 9.0.9 reports zero error-severity findings and 55 reviewed warnings:

| Finding | Count | Disposition |
| --- | ---: | --- |
| Embedded symbols differ from current KiCad libraries | 44 | Retained to avoid silently changing a legacy design. Exact fitted parts and PCB footprints remain independently review-required. |
| Legacy U5 library lookup | 2 | U5 is a required 74LVC2G07 level interface. Substitution with the current library symbol changed pin/net mapping, so the self-contained embedded symbol is retained. |
| USB-section endpoints off the preferred grid | 8 | Each displayed wire endpoint is electrically joined in the exported netlist; high-zoom inspection and netlist parity found no orphan. Retained because moving the compact connector symbols changed connectivity during trial cleanup. |
| `+5V` and hidden `VCC` alias | 1 | Intentional: U4's hidden supply pin resolves to the board `+5V` rail. |

These dispositions are not physical qualification. Rev3A remains quote-only and
prototype-only until the vendor previews and the bring-up plan pass.

## PCB DRC dispositions

KiCad 9.0.9 reports zero error-severity findings, zero unconnected items, zero
schematic-parity issues, and seven reviewed warnings:

| Finding | Count | Disposition |
| --- | ---: | --- |
| Local footprint differs from current library copy | 5 | D2, C5, SW2, TP13, and U2 are intentionally retained project copies. D2/C5/SW2/U2 predate the final route; TP13 differs only because its crowded silkscreen circle was moved to fabrication documentation. Exact fitted parts and pads remain unchanged. |
| Silkscreen reaches board edge | 2 | U2's antenna intentionally overhangs the board edge. The warnings affect outline graphics only; copper, mask, pads, and fabrication clearances pass. |

The board uses four copper layers. Both internal layers are solid GND reference
planes. The complete connector-to-ESP32 paths measure 24.314 mm (D+) and 25.357 mm
(D-), for 1.043 mm skew. Both use 0.20 mm tracks and two standard 0.8/0.4 mm
through-vias to cross from `F.Cu` to `B.Cu` and back. The minimum board trace is
0.20 mm and every routed via is a standard 0.8/0.4 mm through-via. U2 additionally
uses twelve 0.6/0.3 mm plated thermal-ground holes in its center pad, matching the
Revision 2.2 module footprint and standard 0.3 mm fabrication capability. These
checks do not replace fabricator stack-up review or physical USB testing.
