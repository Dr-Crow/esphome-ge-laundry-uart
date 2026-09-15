# Rev3A printable enclosure

This directory contains an editable [build123d](https://build123d.readthedocs.io/) source model and regenerated two-piece exports for the Rev3A GEA Adapter.

These STEP/STL files are fit-check deliverables, not enclosure qualification. The
KiCad assembly now includes a deliberately simplified J1 visualization envelope made
from the linked manufacturer drawing; it is not manufacturer CAD. Preserve that
drawing revision and validate the populated board, both cable insertions, retention,
temperature, and installed Wi-Fi behavior before release.

## Dimensions and fit

- PCB datum: **88.7 × 40.0 × 1.6 mm**; the base cavity has at least 0.5 mm XY clearance on the board's left, top, and bottom edges.
- Base envelope: x=-4..103.7, y=-4..44, z=0..10 mm. Lid envelope: x=-5..104.7, y=-5..45, z=9..22 mm; total assembled height is 22 mm.
- The board sits on printed annular bosses at (4,30) and (48,4), aligned with the 3.2 mm PCB drills. 1.25 mm locating posts pass through both holes (0.35 mm radial clearance), and matching 2.4 mm OD / 1.5 mm ID annular lid retainers lightly contact only the bare mounting annuli. No screws or purchased hardware are required; verify the retainer contact on the first populated-board print.
- The lid is a friction/snap fit: its 7 mm deep skirt overlaps the base wall by 1 mm, with two pairs of shallow snap beads. Expect to tune bead clearance for the printer and filament.

## Connector and service clearances

J1 (RJ45) is treated as a left-side entry connector and has a 22 × 8.2 mm base window spanning y=3.5..25.5 and z=2..10.2 mm. The lid has a matching y=2.75..26.25, z=8.5..18.75 left-wall notch with 0.75 mm lateral and 1.0 mm vertical margin, so the lid wall cannot block the full conservative body/cable insertion envelope. The JLCPCB page identifies C3097717 as EVERCOM 5301-8P8C and links the one-page manufacturer drawing, which lists 15.20, 11.50, and 18.05 mm connector body dimensions: [JLCPCB C3097717](https://jlcpcb.com/partdetail/EVERCOM-53018P8C/C3097717). The simplified KiCad model is aligned to the connector's actual pin and locating-hole pattern and uses the 11.50 mm body height; the enclosure adds a 1.00 mm conservative cable/latch allowance above the seated PCB top (12.50 mm envelope). The lid underside is z=19.4 mm, leaving 1.65 mm above that envelope.

J4 (USB-C) is at (72,36.325) near the lower (+Y) edge and has a 15 × 7 mm cable window. J2 is a populated top-side 2-by-3 recovery header at (11.7,32.5). Its supplier STEP reaches 11.06 mm above the PCB datum, leaving 3.09 mm below the lid underside. There is intentionally no external J2 opening: remove the lid before attaching a 3.3 V USB-to-UART adapter, then disconnect the adapter before closing the enclosure or connecting the appliance. Service holes are provided above SW1/SW2 at (5,3.4) and (13,3.4). SW1 is hardware `RESET`/`EN`; SW2 is GPIO9/`BOOT`. Hold BOOT while tapping RESET to force recovery download mode. Three 2.5 mm-diameter lid apertures expose D4 (green/Wi-Fi), D5 (red/user diagnostic), and D6 (yellow/GEA bus) without adding PCB parts. Connector bodies and cable plugs vary, so prototype-fit both plugs, J2 with Dupont leads, and the populated board before committing to a final print.

## Antenna gate

The volume x=88.7..103.7, y=3..31 is intentionally a clear chamber: no bosses, ribs, snap beads, or fasteners are placed there. The only material at that boundary is the enclosure perimeter wall. Keep this chamber free of metal inserts, foil, or wiring loops during assembly; verify Wi-Fi RSSI and reconnect behavior in the installed appliance position.

## Print and prototype gate

Print base and lid separately with the flat floor/ceiling on the build plate, no supports, 0.2 mm layers, 3+ perimeters, 20–30% infill, and a 0.4 mm nozzle. PETG or ABS is preferred for appliance heat; PLA is suitable only for a bench fit. Deburr the connector windows and test the lid on an unpowered populated PCB first. Confirm J1/J4 plug insertion, the full RJ45 plug/latch sweep, J2 lead access with the lid removed, button reach, board seating, and antenna behavior before any live appliance connection.

## Files

- `requirements.txt` — pinned Python dependencies for regeneration and checks.
- `enclosure.py` — parametric source; rerun with `python enclosure.py --out case/rev3a`.
- `rev3a_base.stl`, `rev3a_lid.stl` — print meshes.
- `rev3a_base.step`, `rev3a_lid.step` — editable CAD exchange solids.
- `check_geometry.py` — regenerates the shapes and checks exported STLs with trimesh.

The checked-in exports pass `check_geometry.py` with build123d 0.11.1 and trimesh
4.12.2: each STL is a watertight volume and each STEP file imports as one valid solid.
This is a geometry check only; it does not replace a populated-board fit test.
