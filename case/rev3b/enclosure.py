"""Parametric two-piece printable enclosure for the GEA Adapter Rev3B PCB.

Coordinates follow the frozen Rev3B PCB: x=0..99 mm, y=0..40 mm, 1.6 mm
thick, four copper layers (see ../../pcb/rev3b/README.md). The base and lid
are separate solids so either can be edited or printed alone, using a small
build123d parametric model.

Component transforms (H1, H2, J1, J2, U2, D4, D5, D6) are read directly from
the frozen Rev3B board file (pcb/rev3b/design/GEA-Adapter-Rev3B.kicad_pcb)
via KiCad 9's bundled pcbnew Python module; see the per-constant comments
below for each value and its source footprint/property.

Run with the build123d/trimesh versions pinned in requirements.txt::

    python enclosure.py --out case/rev3b
    python enclosure.py --out case/rev3b --antenna internal
    python enclosure.py --out case/rev3b --magnets

The optional external-bulkhead variant is dimensioned only for the named
TE/Linx CSB-RGFB-102-UFFR RP-SMA bulkhead-to-U.FL cable assembly. It is not a
generic SMA/RP-SMA opening; see README.md "Antenna variants".
"""

from __future__ import annotations

import argparse
from pathlib import Path

from build123d import Align, Box, Cylinder, Location, Part, export_step, export_stl


# ---------------------------------------------------------------------------
# PCB datum (from pcbnew extraction, 2026-10-01; see module docstring above)
# ---------------------------------------------------------------------------
PCB_X0, PCB_X1 = 0.0, 99.0   # nominal Edge.Cuts rectangle; measured bbox is
PCB_Y0, PCB_Y1 = 0.0, 40.0   # -0.05..99.05 / -0.05..40.05 (0.1 mm line stroke)
PCB_T = 1.6                  # board.GetDesignSettings().GetBoardThickness()

XY_CLEAR = 0.5   # board-to-cavity-wall clearance
Z_CLEAR = 1.0    # clearance from the tallest populated envelope to the lid

# Two board supports at the factory M3 (3.2 mm drill) mounting holes, one per
# board end, under bare carrier mounting areas, not under XIAO edge pads,
# underside contacts, U.FL, antenna chamber, or connector shells. Both are clear of
# every footprint bbox below by construction and by check_geometry.py.
H1 = (4.5, 33.0)
H2 = (94.0, 35.0)
MOUNT_HOLES = (H1, H2)
MOUNT_DRILL_RADIUS = 1.6  # 3.2 mm MountingHole_3.2mm_M3_DIN965

# J1 (RJ45, OnionStraws:RJ45_EVERCOM_5301-8P8C_Horizontal), at (13.97, 12.55)
# rotated -90 deg. Envelope from models/J1-EVERCOM-5301-8P8C-envelope.step,
# board-frame bbox from pcbnew: x=-0.525..18.265, y=8.49..25.175. The body
# protrudes 0.525 mm past the PCB left edge (x=0), so the jack/cable exits
# through the case LEFT wall. This is a conservative clearance envelope, not
# manufacturer CAD (see pcb/rev3b/design/models/README.md); it is also not
# yet confirmed against the mating cable's plug/latch geometry.
J1_BBOX = {"x_min": -0.525, "x_max": 18.265, "y_min": 8.49, "y_max": 25.175}
RJ45_BODY_HEIGHT = 11.45  # Z range of the envelope STEP, parsed 2026-10-01
RJ45_CABLE_LATCH_ALLOWANCE = 1.00  # unverified conservative plug/latch margin
RJ45_VERTICAL_ENVELOPE = RJ45_BODY_HEIGHT + RJ45_CABLE_LATCH_ALLOWANCE
# The checked-in J1 STEP/footprint does not specify assembled tail length.
# Reserve a conservative 3.0 mm below the seated board with a 0.6 mm floor
# skin, and keep the assumption explicit for physical confirmation.
J1_TAIL_CLEARANCE_DEPTH = 3.0
J1_TAIL_FLOOR_SKIN = 0.6

# U2 (XIAO ESP32-C3 v1.3 carrier, GEA_XIAO:XIAO-ESP32-C3-v1.3-SMD), at
# (77.39, 4.0) rotated -90 deg. Board-frame bbox from pcbnew:
# x=77.14..99.987, y=3.286..22.375. The envelope protrudes 0.987 mm past the
# PCB right edge (x=99), matching pcb/rev3b/README.md's "USB-C extending
# about 1 mm beyond the edge" note, so USB-C exits through the case RIGHT
# wall -- the opposite end from J1. The STEP envelope
# (XIAO-ESP32-C3-v1.3-envelope.step, z=0..4.5 mm)
# is a conservative build123d clearance solid, not measured component CAD;
# it folds in the USB shell, both buttons, and the U.FL connector estimate.
U2_BBOX = {"x_min": 77.14, "x_max": 99.987, "y_min": 3.286, "y_max": 22.375}
XIAO_ENVELOPE_HEIGHT = 4.5
USB_CABLE_MARGIN = 2.5  # unverified plug/strain-relief + finger-access margin

# J2 (recovery header, OnionStraws:Recovery_Header_2x3_P2.54mm_Vertical), at
# (20.0, 32.0), 0 deg. Board-frame bbox from pcbnew: x=15.215..24.785,
# y=27.865..36.135. models/README.md documents a 9.20 mm nominal / 9.60 mm
# stacked pre-assembly maximum height; use the 9.60 mm figure as the case
# keep-clear envelope. J2 gets no case opening and is lid-removal-only.
J2_BBOX = {"x_min": 15.215, "x_max": 24.785, "y_min": 27.865, "y_max": 36.135}
J2_HEIGHT_MAX = 9.60

# D4/D5/D6 status LEDs (LED_SMD:LED_0805_2012Metric), 0 deg, from pcbnew.
# No LED part/envelope STEP exists in this project; the 2.5 mm viewing-hole
# diameter below is a conservative viewing aperture, not a measured LED lens.
LED_POSITIONS = {"D4": (84.0, 26.0), "D5": (84.0, 30.0), "D6": (88.0, 26.0)}
LED_VIEW_RADIUS = 1.25

# BOOT/RESET centers are derived from the official Seeed v1.3 KiCad project
# and transformed through the current U2 footprint's carrier mapping. These
# are center coordinates, not a promise about actuator height or tool fit; the
# conservative lid apertures below still require a physical press/return check.
BUTTON_POSITIONS = {"BOOT0": (90.725, 5.524), "RST0": (81.835, 5.524)}
BUTTON_ACCESS_RADIUS = 1.75

# ---------------------------------------------------------------------------
# Derived Z stack-up. The 3.2 mm-drill mounting footprints get a short
# annular boss seats the board 1.25 mm above the floor, which doubles as the
# documented, estimated (not measured) under-board clearance for J1's
# through-hole solder tails; the local footprint gives drill diameter but not
# assembled tail length (J2 is SMD and has no tail).
# ---------------------------------------------------------------------------
FLOOR = 2.4
PCB_STANDOFF = 1.25
PCB_SEAT_Z = FLOOR + PCB_STANDOFF
PCB_TOP_Z = PCB_SEAT_Z + PCB_T

XIAO_ENVELOPE_TOP_Z = PCB_TOP_Z + XIAO_ENVELOPE_HEIGHT
RJ45_ENVELOPE_TOP_Z = PCB_TOP_Z + RJ45_VERTICAL_ENVELOPE
J2_ENVELOPE_TOP_Z = PCB_TOP_Z + J2_HEIGHT_MAX

TALLEST_ENVELOPE_TOP_Z = max(XIAO_ENVELOPE_TOP_Z, RJ45_ENVELOPE_TOP_Z, J2_ENVELOPE_TOP_Z)
LID_UNDERSIDE_Z = TALLEST_ENVELOPE_TOP_Z + Z_CLEAR

LOCATING_POST_RADIUS = 1.25
LID_RETAINER_OUTER_RADIUS = 2.4
LID_RETAINER_INNER_RADIUS = 1.5

# ---------------------------------------------------------------------------
# Case envelope. The magnet
# variant (see the "if magnets:" block in make_base()) widens it to leave
# room for captive corner pockets outside the PCB cavity; this is a
# deliberate, documented size trade-off, not a change to the default
# (nonmagnetic) candidate.
# ---------------------------------------------------------------------------
DEFAULT_MARGIN = 4.0
MAGNET_MARGIN = 12.0  # wide enough for one captive pocket per side margin;
                       # see the asserts in make_base() for the arithmetic

CAV_X0, CAV_X1 = PCB_X0 - XY_CLEAR, PCB_X1 + XY_CLEAR
CAV_Y0, CAV_Y1 = PCB_Y0 - XY_CLEAR, PCB_Y1 + XY_CLEAR

BASE_Z0 = 0.0
BASE_Z1 = PCB_TOP_Z + 3.75  # wall rises partway; lid skirt covers the rest
LID_CEILING = 2.2
LID_Z0 = BASE_Z1 - 1.0      # 1 mm skirt overlap
LID_Z1 = LID_UNDERSIDE_Z + LID_CEILING

RJ45_WINDOW_Y0, RJ45_WINDOW_Y1 = J1_BBOX["y_min"] - 0.75, J1_BBOX["y_max"] + 0.75
RJ45_WINDOW_Z0, RJ45_WINDOW_Z1 = PCB_TOP_Z - 0.5, RJ45_ENVELOPE_TOP_Z + 0.5

USB_WINDOW_Y0, USB_WINDOW_Y1 = U2_BBOX["y_min"] - 0.75, U2_BBOX["y_max"] + 0.75
USB_WINDOW_Z0 = PCB_TOP_Z - 0.5
USB_WINDOW_Z1 = XIAO_ENVELOPE_TOP_Z + USB_CABLE_MARGIN

# Internal antenna alignment lip for the candidate 40 x 20 mm FPC (see
# README.md "Antenna variants"). It sits on the lid underside, away from the
# LED apertures; it is placement guidance, not a verified antenna keepout.
ANTENNA_FPC_WIDTH = 20.0   # along X, against the wall
ANTENNA_FPC_LENGTH = 40.0  # along Y
ANTENNA_FPC_X0 = 52.0

# Optional external bulkhead datum, taken from the primary TE/Linx drawing:
# CSB-RGFB-102-UFFR, RP-SMA bulkhead jack (male pin) to U.FL/MHF1 female
# socket, 102 mm RG-178. The drawing recommends a 6.5 mm mounting hole and
# limits the local enclosure panel to 1.5 mm. Its 6.0 mm flat/key datum is
# documented in README.md; without an orientation datum in the PCB/case
# coordinate system it is intentionally not guessed as a keyed cutout.
EXTERNAL_PART = "TE/Linx CSB-RGFB-102-UFFR"
EXTERNAL_HOLE_DIAMETER = 6.5
EXTERNAL_HOLE_RADIUS = EXTERNAL_HOLE_DIAMETER / 2
EXTERNAL_FLAT_DATUM_MM = 6.0
EXTERNAL_MAX_PANEL_THICKNESS = 1.5
EXTERNAL_CABLE_LENGTH = 102.0
EXTERNAL_MIN_BEND_RADIUS = 10.0
EXTERNAL_HOLE_X = 93.0
EXTERNAL_HOLE_Z = 13.5

# Magnet pockets: captive, fully enclosed, printed-in-place via a pause
# print. Each pocket is bored directly out of the already-solid side margin
# wall block (x < CAV_X0 or x > CAV_X1, full height, since the cavity cut
# never reaches there -- see the "if magnets:" block in make_base()), so it
# is isolated from the PCB cavity and has solid material above and below by
# construction, not a separate printed pedestal. Sized for a placeholder
# 4 x 2 mm disc magnet with running clearance; not a measured or qualified
# magnet selection, and RF/holding-force/thermal behavior are explicitly
# untested -- see README.md. Off by default (nonmagnetic).
MAGNET_DIAMETER = 4.0
MAGNET_RADIUS = MAGNET_DIAMETER / 2 + 0.3
MAGNET_THICKNESS = 2.0
MAGNET_BASE_MARGIN = 0.8   # solid material kept below the magnet pocket
MAGNET_PEDESTAL_RADIUS = MAGNET_RADIUS + 1.5  # min. solid radius around each pocket
MAGNET_PAUSE_Z = FLOOR + MAGNET_BASE_MARGIN + MAGNET_THICKNESS  # slicer pause height
MAGNET_WALL_CLEARANCE = 1.5   # pocket-to-exterior-wall gap
MAGNET_CAVITY_CLEARANCE = 0.5  # pocket-to-PCB-cavity gap


def _box(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> Part:
    return Box(x1 - x0, y1 - y0, z1 - z0, align=(Align.MIN, Align.MIN, Align.MIN)).locate(
        Location((x0, y0, z0))
    )


def _cylinder(radius: float, z0: float, z1: float, x: float, y: float) -> Part:
    return Cylinder(radius, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).locate(
        Location((x, y, z0))
    )


def _margin(magnets: bool) -> float:
    return MAGNET_MARGIN if magnets else DEFAULT_MARGIN


def make_base(antenna: str = "none", magnets: bool = False) -> Part:
    """Open-top base: cavity, connector windows, and two board supports.

    ``antenna`` selects "none", "internal", or "external". The external
    choice is a matching base variant for the named bulkhead cable; its
    opening is cut in make_lid(), where the local panel seat is defined.
    """
    if antenna not in ("none", "internal", "external"):
        raise ValueError(f"unsupported antenna variant: {antenna!r}")
    margin = _margin(magnets)
    base_x0, base_x1 = CAV_X0 - margin, CAV_X1 + margin
    base_y0, base_y1 = CAV_Y0 - margin, CAV_Y1 + margin
    wall_top = BASE_Z1

    base = _box(base_x0, base_x1, base_y0, base_y1, BASE_Z0, wall_top)
    cavity = _box(CAV_X0, CAV_X1, CAV_Y0, CAV_Y1, FLOOR, wall_top + 0.2)
    base = base - cavity

    # Under-board relief below the through-hole RJ45 tails. The local model
    # contains no verified tail length, so this is a conservative clearance
    # pocket rather than a claim about the assembled connector.
    j1_tail_pocket = _box(
        PCB_X0,
        J1_BBOX["x_max"] + 0.75,
        J1_BBOX["y_min"] - 0.75,
        J1_BBOX["y_max"] + 0.75,
        J1_TAIL_FLOOR_SKIN,
        FLOOR + 0.05,
    )
    base = base - j1_tail_pocket

    # J1 RJ45: left-wall opening (x=0 side).
    rj45_window = _box(
        base_x0 - 0.2, 1.0,
        RJ45_WINDOW_Y0, RJ45_WINDOW_Y1,
        RJ45_WINDOW_Z0, RJ45_WINDOW_Z1,
    )
    base = base - rj45_window

    # U2 USB-C: right-wall opening (x=99 side). Deliberately generous in Y
    # so it also exposes BOOT/RESET for finger/tool press -- see the
    # "UNRESOLVED" note above J2_BBOX for why there are no separate button
    # holes.
    usb_window = _box(
        98.0, base_x1 + 0.2,
        USB_WINDOW_Y0, USB_WINDOW_Y1,
        USB_WINDOW_Z0, USB_WINDOW_Z1,
    )
    base = base - usb_window

    # Two annular board-support bosses with locating posts at the current
    # 3.2 mm mounting drills.
    for x, y in MOUNT_HOLES:
        boss = _cylinder(3.0, FLOOR, PCB_SEAT_Z, x, y) - _cylinder(1.9, FLOOR - 0.1, PCB_SEAT_Z + 0.15, x, y)
        locating_post = _cylinder(LOCATING_POST_RADIUS, FLOOR - 0.1, PCB_TOP_Z + 0.30, x, y)
        base = base + boss + locating_post

    if magnets:
        # One pocket in the left margin strip, one in the right, offset in Y
        # for a stable two-point hold. x < CAV_X0 (and x > CAV_X1) is
        # already solid, full-height wall material there -- the cavity cut
        # above only touches x in [CAV_X0, CAV_X1] -- so each pocket is
        # simply bored out of that existing solid block. MAGNET_PEDESTAL_
        # RADIUS is the minimum solid-material radius kept around each
        # pocket (checked against both the exterior wall and the PCB
        # cavity by the asserts below), not a separately printed feature.
        left_x = base_x0 + MAGNET_WALL_CLEARANCE + MAGNET_PEDESTAL_RADIUS
        right_x = base_x1 - MAGNET_WALL_CLEARANCE - MAGNET_PEDESTAL_RADIUS
        assert left_x - MAGNET_PEDESTAL_RADIUS >= base_x0, "magnet pocket breaks the exterior wall"
        assert left_x + MAGNET_PEDESTAL_RADIUS <= CAV_X0 - MAGNET_CAVITY_CLEARANCE, (
            "magnet pocket intrudes on the PCB cavity"
        )
        assert right_x + MAGNET_PEDESTAL_RADIUS <= base_x1, "magnet pocket breaks the exterior wall"
        assert right_x - MAGNET_PEDESTAL_RADIUS >= CAV_X1 + MAGNET_CAVITY_CLEARANCE, (
            "magnet pocket intrudes on the PCB cavity"
        )
        # y=33 (left) sits above the J1/RJ45 window (y<=25.925); y=30
        # (right) sits above the U2/USB window (y<=23.125). Both wall
        # windows are cut from ``base`` earlier in this function, so a
        # pocket placed inside either window's (x, y) footprint would
        # reopen/obstruct that connector opening -- keep them disjoint.
        pocket_sites = ((left_x, 33.0), (right_x, 30.0))
        for x, y in pocket_sites:
            pocket = _cylinder(
                MAGNET_RADIUS,
                FLOOR + MAGNET_BASE_MARGIN,
                FLOOR + MAGNET_BASE_MARGIN + MAGNET_THICKNESS,
                x, y,
            )
            base = base - pocket

    return base


def _cylinder_y(radius: float, y0: float, y1: float, x: float, z: float) -> Part:
    """Cylinder along Y, used for the optional bulkhead opening."""
    return Cylinder(
        radius,
        y1 - y0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).locate(Location((x, y1, z), (90, 0, 0)))


def make_lid(magnets: bool = False, antenna: str = "none") -> Part:
    """Vent-free lid with skirt, snap beads, and LED apertures.

    The ``magnets`` flag must match the value passed to make_base() so the
    lid's skirt footprint lines up with the (possibly widened) base.
    """
    if antenna not in ("none", "internal", "external"):
        raise ValueError(f"unsupported antenna variant: {antenna!r}")
    margin = _margin(magnets)
    lid_z0 = LID_Z0
    lid_z1 = LID_Z1
    lid_x0, lid_x1 = CAV_X0 - margin - 1.0, CAV_X1 + margin + 1.0
    lid_y0, lid_y1 = CAV_Y0 - margin - 1.0, CAV_Y1 + margin + 1.0
    lid_inner_x0, lid_inner_x1 = lid_x0 + 0.75, lid_x1 - 0.75
    lid_inner_y0, lid_inner_y1 = lid_y0 + 0.75, lid_y1 - 0.75

    lid = _box(lid_x0, lid_x1, lid_y0, lid_y1, lid_z0, lid_z1)
    underside = _box(
        lid_inner_x0, lid_inner_x1, lid_inner_y0, lid_inner_y1,
        lid_z0 - 0.1, lid_z1 - LID_CEILING,
    )
    lid = lid - underside

    for ref, (x, y) in LED_POSITIONS.items():
        lid = lid - _cylinder(LED_VIEW_RADIUS, lid_z1 - LID_CEILING - 0.1, lid_z1 + 0.1, x, y)

    # Tool access to the factory XIAO buttons. The centers come from the
    # official module project mapping above; actuator force/return is a
    # physical check, not inferred from this clearance hole.
    for x, y in BUTTON_POSITIONS.values():
        lid = lid - _cylinder(
            BUTTON_ACCESS_RADIUS,
            lid_z1 - LID_CEILING - 0.1,
            lid_z1 + 0.1,
            x,
            y,
        )

    # The lid skirt overlaps the base, so both connector corridors must be
    # opened in the lid as well as in the base. These are deliberately the
    # same conservative windows used for the base walls.
    lid = lid - _box(
        lid_x0 - 0.2,
        1.0,
        RJ45_WINDOW_Y0,
        RJ45_WINDOW_Y1,
        RJ45_WINDOW_Z0,
        RJ45_WINDOW_Z1,
    )
    lid = lid - _box(
        98.0,
        lid_x1 + 0.2,
        USB_WINDOW_Y0,
        USB_WINDOW_Y1,
        USB_WINDOW_Z0,
        USB_WINDOW_Z1,
    )

    for x, y in MOUNT_HOLES:
        retainer = _cylinder(
            LID_RETAINER_OUTER_RADIUS, PCB_TOP_Z - 0.05, lid_z1 - LID_CEILING + 0.1, x, y
        ) - _cylinder(LID_RETAINER_INNER_RADIUS, PCB_TOP_Z - 0.15, lid_z1 - LID_CEILING + 0.2, x, y)
        lid = lid + retainer

    for x in (24.0, 70.0):
        for y in (lid_inner_y0 + 0.15, lid_inner_y1 - 0.15):
            bead = _box(x - 2.0, x + 2.0, y - 0.45, y + 0.45, lid_z0 + 0.15, lid_z0 + 1.0)
            lid = lid + bead

    if antenna == "external":
        # The ordinary lid wall is 0.75 mm. Add only 0.75 mm locally so the
        # connector's panel seat is 1.5 mm total (the TE/Linx maximum), while
        # leaving the rest of the inexpensive lid unchanged. The pad is
        # outside the PCB cavity and is the mechanical load path for the
        # bulkhead nut; no force is routed through the U.FL snap connection.
        pad_x0 = EXTERNAL_HOLE_X - 5.0
        pad_x1 = EXTERNAL_HOLE_X + 5.0
        pad_z0 = EXTERNAL_HOLE_Z - 5.0
        pad_z1 = EXTERNAL_HOLE_Z + 5.0
        pad = _box(
            pad_x0,
            pad_x1,
            lid_y1 - 1.5,
            lid_y1 - 0.75,
            pad_z0,
            pad_z1,
        )
        lid = lid + pad
        # Bore through the complete local seat. The hole is deliberately
        # circular; the drawing's 6.0 mm flat/key datum is retained as a
        # documented orientation datum, not an invented keyed orientation.
        hole = _cylinder_y(
            EXTERNAL_HOLE_RADIUS,
            lid_y1 - 1.7,
            lid_y1 + 0.2,
            EXTERNAL_HOLE_X,
            EXTERNAL_HOLE_Z,
        )
        lid = lid - hole

    if antenna == "internal":
        # Keep the candidate FPC flat against the lid underside. This is a
        # coherent 40 x 20 mm placement inside the available case height and
        # avoids masking the three LED apertures at x=84..88. The ring is a
        # shallow placement guide only; the antenna adhesive supplies actual
        # retention and its identity/clearance remain unverified.
        lid = lid + make_internal_antenna_ledge()

    return lid


def make_internal_antenna_ledge() -> Part:
    """Shallow alignment lip for an adhesive-backed external FPC antenna.

    Outlines a 40 x 20 mm rectangle against the interior of the right end
    wall for visual placement guidance only; it provides no mechanical
    retention (the antenna's own adhesive backing retains it) and is not a
    verified antenna keepout. See README.md "Antenna variants".
    """
    x0 = ANTENNA_FPC_X0
    y0 = (PCB_Y0 + PCB_Y1) / 2 - ANTENNA_FPC_LENGTH / 2
    y1 = y0 + ANTENNA_FPC_LENGTH
    outline = _box(
        x0,
        x0 + ANTENNA_FPC_WIDTH,
        y0,
        y1,
        LID_UNDERSIDE_Z - 0.7,
        LID_UNDERSIDE_Z + 0.1,
    )
    inner = _box(
        x0 + 1.0,
        x0 + ANTENNA_FPC_WIDTH - 1.0,
        y0 + 1.0,
        y1 - 1.0,
        LID_UNDERSIDE_Z - 0.8,
        LID_UNDERSIDE_Z + 0.2,
    )
    return outline - inner


def _export(shape: Part, stem: str, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    export_stl(shape, out_dir / f"{stem}.stl")
    export_step(shape, out_dir / f"{stem}.step")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "exports")
    parser.add_argument("--antenna", choices=("none", "internal", "external"), default="none")
    parser.add_argument("--magnets", action="store_true")
    args = parser.parse_args()

    base = make_base(antenna=args.antenna, magnets=args.magnets)
    lid = make_lid(magnets=args.magnets, antenna=args.antenna)

    suffix = ""
    if args.antenna != "none":
        suffix += f"_ant-{args.antenna}"
    if args.magnets:
        suffix += "_magnets"

    _export(base, f"rev3b_base{suffix}", args.out)
    _export(lid, f"rev3b_lid{suffix}", args.out)

    print(f"wrote {args.out / f'rev3b_base{suffix}.stl'} and {args.out / f'rev3b_lid{suffix}.stl'}")


if __name__ == "__main__":
    main()

