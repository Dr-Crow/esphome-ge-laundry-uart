"""Parametric two-piece printable enclosure for the GEA Adapter Rev3A PCB.

Coordinates follow the PCB: x=0..88.7 mm, y=0..40 mm.  The base and lid
are deliberately separate solids so either can be edited or printed alone.
Run this file with the case virtualenv to regenerate all deliverables::

    python enclosure.py --out case/rev3a

The geometry is intentionally conservative around the two edge connectors.
Connector envelopes and the RF antenna keep-out are parameters below rather
than imported meshes, so this remains editable without KiCad or Fusion.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from build123d import Align, Box, Cylinder, Location, Part, export_step, export_stl


# PCB datum and required fit allowances (millimetres).
PCB_X = 88.7
PCB_Y = 40.0
PCB_T = 1.6
XY_CLEAR = 0.5
Z_CLEAR = 1.0

# Base envelope.  The extra length to x=103.7 is the antenna chamber.
BASE_X0, BASE_X1 = -4.0, 103.7
BASE_Y0, BASE_Y1 = -4.0, 44.0
BASE_Z0, BASE_Z1 = 0.0, 10.0
FLOOR = 2.4

# Lid envelope and its deep, friction-fit skirt.  The skirt overlaps the
# base wall by 1 mm in Z and has 0.25 mm radial clearance per side.
LID_X0, LID_X1 = -5.0, 104.7
LID_Y0, LID_Y1 = -5.0, 45.0
LID_Z0, LID_Z1 = 9.0, 22.0
LID_CEILING = 2.6
LID_INNER_X0, LID_INNER_X1 = -4.25, 103.95
LID_INNER_Y0, LID_INNER_Y1 = -4.25, 44.25

# Board cavity.  It extends into the antenna chamber, but has no internal
# ribs, bosses, or fasteners in x=88.7..103.7, y=3..31.
CAV_X0, CAV_X1 = -XY_CLEAR, 100.2
CAV_Y0, CAV_Y1 = -XY_CLEAR, PCB_Y + XY_CLEAR
ANTENNA_X0, ANTENNA_X1 = PCB_X, PCB_X + 15.0
ANTENNA_Y0, ANTENNA_Y1 = 3.0, 31.0

MOUNT_HOLES = ((4.0, 30.0), (48.0, 4.0))

# C3097717 (EVERCOM 5301-8P8C) is not present in the KiCad assembly STEP.
# The JLCPCB-hosted manufacturer drawing lists 15.20, 11.50, and 18.05 mm
# body dimensions.  Use the largest 11.50 mm body height plus a conservative
# 1.0 mm cable-plug/latch allowance for a 12.50 mm vertical envelope above
# the seated PCB top.  These named values make the missing-3D-model assumption
# visible and are checked in check_geometry.py.
PCB_SEAT_Z = FLOOR + 1.25
PCB_TOP_Z = PCB_SEAT_Z + PCB_T
RJ45_BODY_HEIGHT = 11.50
RJ45_CABLE_LATCH_ALLOWANCE = 1.00
RJ45_VERTICAL_ENVELOPE = RJ45_BODY_HEIGHT + RJ45_CABLE_LATCH_ALLOWANCE
RJ45_ENVELOPE_TOP_Z = PCB_TOP_Z + RJ45_VERTICAL_ENVELOPE
LID_UNDERSIDE_Z = LID_Z1 - LID_CEILING

# The side window crosses the full conservative cable/port opening height.
# The matching lid notch below clears the same insertion envelope.
RJ45_WINDOW_X0, RJ45_WINDOW_X1 = -5.0, 0.7
RJ45_WINDOW_Y0, RJ45_WINDOW_Y1 = 3.5, 25.5
RJ45_WINDOW_Z0, RJ45_WINDOW_Z1 = 2.0, BASE_Z1 + 0.2
RJ45_NOTCH_X0, RJ45_NOTCH_X1 = LID_X0 - 0.2, LID_INNER_X0 + 0.25
RJ45_NOTCH_Y0, RJ45_NOTCH_Y1 = RJ45_WINDOW_Y0 - 0.75, RJ45_WINDOW_Y1 + 0.75
RJ45_NOTCH_Z0, RJ45_NOTCH_Z1 = LID_Z0 - 0.5, RJ45_ENVELOPE_TOP_Z + 1.0

# Printed PCB retention: 1.25 mm locating posts pass through the 3.2 mm
# drills with 0.35 mm radial clearance. Lid-side annular retainers bear on
# the bare mounting annulus only, just above the seated PCB top.
LOCATING_POST_RADIUS = 1.25
LOCATING_POST_TOP_Z = PCB_TOP_Z + 0.30
LID_RETAINER_OUTER_RADIUS = 2.4
LID_RETAINER_INNER_RADIUS = 1.5
LID_RETAINER_BOTTOM_Z = PCB_TOP_Z - 0.05


def _box(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> Part:
    return Box(x1 - x0, y1 - y0, z1 - z0, align=(Align.MIN, Align.MIN, Align.MIN)).locate(
        Location((x0, y0, z0))
    )


def _cylinder(radius: float, z0: float, z1: float, x: float, y: float) -> Part:
    return Cylinder(radius, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).locate(
        Location((x, y, z0))
    )


def make_base() -> Part:
    """Make the open-top base, connector windows, and PCB support rings."""
    base = _box(BASE_X0, BASE_X1, BASE_Y0, BASE_Y1, BASE_Z0, BASE_Z1)
    cavity = _box(CAV_X0, CAV_X1, CAV_Y0, CAV_Y1, FLOOR, BASE_Z1 + 0.2)
    base = base - cavity

    # RJ45 J1: side-entry opening through the left wall.  The generous
    # 22x8.2 mm (Y x Z) window covers the rotated EVERCOM body and cable latch.
    rj45_window = _box(
        RJ45_WINDOW_X0,
        RJ45_WINDOW_X1,
        RJ45_WINDOW_Y0,
        RJ45_WINDOW_Y1,
        RJ45_WINDOW_Z0,
        RJ45_WINDOW_Z1,
    )
    base = base - rj45_window

    # USB-C J4 at (72,36.325), opening through the positive-y/lower edge.
    # Leave a broad flange around the shell for cable insertion.
    usb_window = _box(64.5, 79.5, 39.0, 46.0, 2.0, 6.4)
    base = base - usb_window

    # Two non-hardware bosses support the specified PCB mounting holes.  The
    # 1.9 mm bores leave 0.3 mm radial clearance around the 3.2 mm drills.
    for x, y in MOUNT_HOLES:
        boss = _cylinder(3.0, FLOOR, 3.65, x, y)
        bore = _cylinder(1.9, FLOOR - 0.1, 3.8, x, y)
        locating_post = _cylinder(LOCATING_POST_RADIUS, FLOOR - 0.1, LOCATING_POST_TOP_Z, x, y)
        base = base + (boss - bore) + locating_post

    # Small lead-in ramps at the two long walls make the lid's skirt locate
    # during assembly without intruding into the antenna chamber.
    for x in (18.0, 55.0, 80.0):
        for y in (BASE_Y0 + 0.9, BASE_Y1 - 0.9):
            guide = _box(x - 1.8, x + 1.8, y - 0.55, y + 0.55, 6.6, 8.0)
            base = base + guide
    return base


def make_lid() -> Part:
    """Make the vent-free lid with skirt, snap beads, and service holes."""
    lid = _box(LID_X0, LID_X1, LID_Y0, LID_Y1, LID_Z0, LID_Z1)
    # Open the underside, leaving a 2.6 mm ceiling.
    underside = _box(
        LID_INNER_X0,
        LID_INNER_X1,
        LID_INNER_Y0,
        LID_INNER_Y1,
        LID_Z0 - 0.1,
        LID_Z1 - LID_CEILING,
    )
    lid = lid - underside

    # Clear the complete left lid wall across the conservative RJ45 body and
    # cable/latch insertion envelope. Margins exceed the nominal drawing.
    rj45_notch = _box(
        RJ45_NOTCH_X0,
        RJ45_NOTCH_X1,
        RJ45_NOTCH_Y0,
        RJ45_NOTCH_Y1,
        RJ45_NOTCH_Z0,
        RJ45_NOTCH_Z1,
    )
    lid = lid - rj45_notch

    # Long annular retainers descend from the lid underside to the PCB
    # mounting annulus. They are outside the antenna chamber and stay within
    # 2.4 mm of each hole centre.
    for x, y in MOUNT_HOLES:
        retainer = _cylinder(
            LID_RETAINER_OUTER_RADIUS,
            LID_RETAINER_BOTTOM_Z,
            LID_UNDERSIDE_Z + 0.1,
            x,
            y,
        ) - _cylinder(
            LID_RETAINER_INNER_RADIUS,
            LID_RETAINER_BOTTOM_Z - 0.1,
            LID_UNDERSIDE_Z + 0.2,
            x,
            y,
        )
        lid = lid + retainer

    # Two shallow service holes over SW1 (reset) and SW2 (boot), as present in
    # the Rev3A layout at (5,3.4) and (13,3.4).  They are tool-access holes,
    # not mounting holes, and are outside the antenna keep-out.
    for x in (5.0, 13.0):
        lid = lid - _cylinder(2.0, LID_Z1 - LID_CEILING - 0.1, LID_Z1 + 0.1, x, 3.4)

    # Four inward snap beads.  They are short, rounded-free printable nubs
    # positioned only over the board area; x<=80 keeps the RF chamber empty.
    for x in (24.0, 58.0):
        # Place the nub 0.15 mm inside the skirt edge so the boolean union
        # has a positive overlap (rather than merely touching a face).
        for y in (LID_INNER_Y0 + 0.15, LID_INNER_Y1 - 0.15):
            bead = _box(x - 2.0, x + 2.0, y - 0.45, y + 0.45, LID_Z0 + 0.15, LID_Z0 + 1.0)
            lid = lid + bead
    return lid


def _export(shape: Part, stem: str, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    export_stl(shape, out_dir / f"{stem}.stl")
    export_step(shape, out_dir / f"{stem}.step")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    base = make_base()
    lid = make_lid()
    _export(base, "rev3a_base", args.out)
    _export(lid, "rev3a_lid", args.out)
    print(f"wrote {args.out / 'rev3a_base.stl'} and {args.out / 'rev3a_lid.stl'}")


if __name__ == "__main__":
    main()
