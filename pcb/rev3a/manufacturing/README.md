# Revision 3A manufacturing package

Upload these three matched files together:

- [`GERBER-GEA-Adapter-Rev3A.zip`](GERBER-GEA-Adapter-Rev3A.zip)
- [`BOM-GEA-Adapter-Rev3A.csv`](BOM-GEA-Adapter-Rev3A.csv)
- [`CPL-GEA-Adapter-Rev3A.csv`](CPL-GEA-Adapter-Rev3A.csv)

The package describes an 88.7 x 40.0 mm, four-layer, 1.6 mm board with all 93
fitted components on the top side. The BOM contains 44 purchasing groups and an
exact LCSC identifier for every group.

The Gerber archive contains 14 files: four copper layers, top/bottom paste,
top/bottom solder mask, top/bottom silkscreen, board outline, separate plated and
non-plated drill files, and the Gerber job file. The minimum plated drill is
0.30 mm; ordinary routed vias use 0.40 mm drills. The design does not require
blind/buried vias, filled vias, controlled-depth drilling, or four-wire Kelvin
testing.

J1 is a through-hole EVERCOM 5301-8P8C appliance connector. J2 is a populated
top-side 2-by-3 recovery header. J4 is the USB-C receptacle. Confirm all three are
present and correctly oriented in the vendor preview.

> [!WARNING]
> This package is suitable for quoting and a small prototype batch only. Do not
> order production quantities or connect a board to an appliance until the
> [review checklist](../validation/REVIEW_CHECKLIST.md) and
> [bring-up procedure](../BRINGUP.md) pass.

Supplier stock, substitutions, assembly classifications, and pricing change. Stop
if any BOM row is unselected or marked do-not-place, or if the quote adds a process
not listed above. Review the board, drill, parts, and placement previews before
payment.
