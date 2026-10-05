"""Parametric two-piece printable enclosure for the Rev3C socketed-XIAO carrier.

Reuses Rev3B's enclosure shape/code (see ../rev3b/enclosure.py): same 99 x 40
x 1.6 mm board envelope, same J1/J2/LED/mount-hole positions, same antenna/
magnet variants. The only mechanical change from Rev3B is U2: Rev3C sockets
a factory pre-soldered, pre-headered retail XIAO ESP32-C3 module onto two
1x7 female headers (HCTL PM254-1-07-Z-8.5, LCSC C2897370 --
https://www.lcsc.com/product-detail/C2897370.html) instead of soldering the
module down flush as an SMD part. Both the carrier (with sockets) and the
module (with its male header) ship fully assembled; no user soldering is
required or implied anywhere in this file.

The Rev3C carrier layout is a routed review candidate. The
socket/button/USB/antenna positions below are a candidate transform: the
official Seeed XIAO ESP32-C3 v1.3 published
KiCad hardware files give the module's own pad/switch/connector geometry,
translated by a fixed offset onto this carrier's socket-row layout. See the
per-constant comments for the values and what each one is sourced from.
Rev3B (../rev3b/) is unmodified by this file.

The height stack above the carrier board is a conservative, explicitly
provisional envelope, not a measured assembly, except where noted as
manufacturer-confirmed (the socket body height). No physical fit, mating
retention, or electrical qualification is claimed.

Run with the build123d/trimesh versions pinned in requirements.txt::

    python enclosure.py --out case/rev3c
    python enclosure.py --out case/rev3c --antenna internal
    python enclosure.py --out case/rev3c --magnets

See ../rev3b/enclosure.py's docstring for the external-bulkhead variant's
scope (unchanged here).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from build123d import Align, Box, Cylinder, Location, Part, export_step, export_stl


# ---------------------------------------------------------------------------
# PCB datum. The Rev3C carrier keeps the same 99 x 40 x 1.6 mm envelope as
# Rev3B. J1/J2/LED/mount-hole positions are reused verbatim from Rev3B
# (unchanged region of the board); only the U2 (XIAO) area, derived below,
# is new.
# ---------------------------------------------------------------------------
PCB_X0, PCB_X1 = 0.0, 99.0
PCB_Y0, PCB_Y1 = 0.0, 40.0
PCB_T = 1.6  # unchanged from Rev3B

XY_CLEAR = 0.5
Z_CLEAR = 1.0

# Unchanged from Rev3B; H1/H2 sit under bare carrier mounting areas, clear
# of the new socket footprint by construction and by check_geometry.py.
H1 = (4.5, 33.0)
H2 = (94.0, 35.0)
MOUNT_HOLES = (H1, H2)
MOUNT_DRILL_RADIUS = 1.6

# J1 (RJ45) -- unchanged from Rev3B.
J1_BBOX = {"x_min": -0.525, "x_max": 18.265, "y_min": 8.49, "y_max": 25.175}
RJ45_BODY_HEIGHT = 11.45
RJ45_CABLE_LATCH_ALLOWANCE = 1.00
RJ45_VERTICAL_ENVELOPE = RJ45_BODY_HEIGHT + RJ45_CABLE_LATCH_ALLOWANCE
J1_TAIL_CLEARANCE_DEPTH = 3.0
J1_TAIL_FLOOR_SKIN = 0.6

# ---------------------------------------------------------------------------
# U2 area -- socketed XIAO ESP32-C3 module (Rev3C's only mechanical change
# from Rev3B). Socket row Y centers and the shared pin X span below match
# the in-progress Rev3C carrier layout's own socket footprint placement;
# the button/U.FL/USB-C positions are the official module's own pad/switch/
# connector layout translated by the same fixed offset onto those rows (a
# pure translation, independently verified identical from both rows).
# ---------------------------------------------------------------------------

# Two HCTL PM254-1-07-Z-8.5 (LCSC C2897370) 1x7 female headers, 2.54 mm
# pitch. Body envelope (18.18 long x 2.5 wide x 8.5 high) and the height
# tolerance (+/-0.15) are manufacturer-confirmed from the part's published
# drawing (LCSC product page above). The mating pin insertion-depth limit is
# not dimensioned on that drawing.
SOCKET_ROW_Y = (5.2975, 20.5375)
SOCKET_PIN_X0, SOCKET_PIN_X1 = 80.27, 95.51
SOCKET_BODY_LENGTH = 18.18   # 2.54 * 7 pins + 0.40, per drawing formula
SOCKET_BODY_WIDTH = 2.5
SOCKET_LENGTH_TOL = 0.30
SOCKET_WIDTH_TOL = 0.15
SOCKET_CENTER_X = (SOCKET_PIN_X0 + SOCKET_PIN_X1) / 2  # 87.89
SOCKET_BODY_HEIGHT = 8.5     # manufacturer-confirmed nominal
SOCKET_HEIGHT_TOL = 0.15     # manufacturer-confirmed tolerance
SOCKET_BODY_HEIGHT_MIN = SOCKET_BODY_HEIGHT - SOCKET_HEIGHT_TOL  # 8.35
SOCKET_BODY_HEIGHT_MAX = SOCKET_BODY_HEIGHT + SOCKET_HEIGHT_TOL  # 8.65
SOCKET_BBOX = tuple(
    {
        "x_min": SOCKET_CENTER_X - SOCKET_BODY_LENGTH / 2,
        "x_max": SOCKET_CENTER_X + SOCKET_BODY_LENGTH / 2,
        "y_min": y - SOCKET_BODY_WIDTH / 2,
        "y_max": y + SOCKET_BODY_WIDTH / 2,
    }
    for y in SOCKET_ROW_Y
)
# Published maximum body, centred on the nominal row datum. The drawing does
# not specify body-to-pin registration or assembled seating tolerances.
SOCKET_MAX_BBOX = tuple(
    {
        "x_min": SOCKET_CENTER_X - (SOCKET_BODY_LENGTH + SOCKET_LENGTH_TOL) / 2,
        "x_max": SOCKET_CENTER_X + (SOCKET_BODY_LENGTH + SOCKET_LENGTH_TOL) / 2,
        "y_min": y - (SOCKET_BODY_WIDTH + SOCKET_WIDTH_TOL) / 2,
        "y_max": y + (SOCKET_BODY_WIDTH + SOCKET_WIDTH_TOL) / 2,
    }
    for y in SOCKET_ROW_Y
)
# Through-hole solder tails: 3.2 +/-0.25 mm from the seating plane
# (manufacturer-confirmed), i.e. up to 3.45 mm max below the socket body.
# Below the 1.6 mm carrier that leaves a conservative ~2.4 mm clearance need
# from the carrier underside with a 0.6 mm minimum floor skin retained.
SOCKET_TAIL_CLEARANCE_DEPTH = 2.4
SOCKET_TAIL_FLOOR_SKIN = 0.6

# Male pin-header plastic spacer base on the pre-headered retail module:
# sits on top of the female socket when mated. Not manufacturer-dimensioned
# for this specific module SKU -- modeled as a provisional, adjustable
# envelope spanning a plausible 2.0-3.0 mm range (typical 2.54 mm
# breakaway-header insulator-base heights), not a measured figure.
MALE_HEADER_SPACER_HEIGHT_MIN = 2.0
MALE_HEADER_SPACER_HEIGHT_MAX = 3.0
REVIEW_STACK_MIN = SOCKET_BODY_HEIGHT_MIN + MALE_HEADER_SPACER_HEIGHT_MIN
REVIEW_STACK_MAX = SOCKET_BODY_HEIGHT_MAX + MALE_HEADER_SPACER_HEIGHT_MAX

# Complete plugged-in module envelope, measured from the module's OWN PCB
# underside (where it rests on the male header) to its tallest top-side
# feature (USB-C shell / buttons / onboard antenna). The official module's
# own PCB is 1.6 mm thick (from its published KiCad hardware files) and is
# already folded into this 5.5 mm provisional maximum -- do not add module
# PCB thickness again on top of this. Not confirmed for the pre-soldered
# SKU's actual top-side components.
MODULE_ENVELOPE_HEIGHT_MAX = 5.5

# Plugged-in module's own board-edge footprint (candidate). This is the X/Y
# space the module itself occupies once seated -- used for the insertion-
# clearance/collision check, not for any case cutout.
MODULE_BBOX = {"x_min": 77.463, "x_max": 98.444, "y_min": 4.015, "y_max": 21.820}

# USB-C connector on the plugged-in module (candidate). Like Rev3B's U2,
# this overhangs the PCB_X1=99 edge by about 1 mm, so the window still exits
# through the case RIGHT wall.
USB_BBOX = {"x_min": 91.939, "x_max": 100.003, "y_min": 8.041, "y_max": 17.794}
USB0_POSITION = (92.589, 12.9175)  # USB-C connector center
USB_CABLE_MARGIN = 2.5  # unverified plug/strain-relief + finger-access margin, same as Rev3B

# U.FL (ANT0) center on the plugged-in module (candidate). No separate case
# feature -- it falls inside MODULE_BBOX and is covered by the module
# collision check; recorded here only as a documented keep-clear reference.
ANT0_POSITION = (78.873, 12.9175)

# BOOT0/RST0 switch centers (candidate, independently re-derived from the
# official module layout). These supersede Rev3B's hardcoded button
# positions, which do not apply to this socketed layout: this module's two
# buttons sit at the SAME X and differ only in Y (stacked along the short
# axis), not spread along X at the same Y the way Rev3B's flush-mounted
# footprint used.
#
# Pin-1 orientation note: on the y=5.2975 row, pin 1 is at the HIGH-x end
# (nearer USB-C); on the y=20.5375 row, pin 1 is at the LOW-x end (nearer
# BOOT0/RST0). Both the carrier's sockets and the module's male header are
# factory-assembled; this note is for engineering reference, not a build
# step. The sockets are not keyed: reversed insertion is possible and can
# damage the board. Match the module's USB-C end to the case USB opening.
BUTTON_POSITIONS = {"BOOT0": (79.0, 8.4725), "RST0": (79.0, 17.3625)}
BUTTON_ACCESS_RADIUS = 1.75

# Current selected carrier has no J2 or D19. Historical original is retained
# separately; only this isolated analytical proxy removes the stale envelope.
J2_PRESENT = False

# D4/D5/D6 status LEDs -- unchanged from Rev3B.
LED_POSITIONS = {"D4": (84.0, 26.0), "D5": (84.0, 30.0), "D6": (88.0, 26.0)}
LED_VIEW_RADIUS = 1.25

# ---------------------------------------------------------------------------
# Derived Z stack-up. Floor/standoff are unchanged from Rev3B (same carrier
# board); the existing 1.25 mm general standoff is less than the 2.4 mm
# socket-tail clearance need, so the tail relief is a local pocket cut
# deeper into the floor slab, the same pattern Rev3B already used for J1's
# RJ45 tails, not a change to the general standoff.
#
# The USB-C window must cover the full plausible range of assembled
# heights, not just the tallest case: _MIN uses the shortest plausible
# socket+spacer stack (its lower bound), _MAX uses the tallest plausible
# full stack including the module's own top-side envelope (its upper
# bound, and the figure that drives lid clearance).
# ---------------------------------------------------------------------------
FLOOR = 2.4
PCB_STANDOFF = 1.25
PCB_SEAT_Z = FLOOR + PCB_STANDOFF
PCB_TOP_Z = PCB_SEAT_Z + PCB_T

SOCKET_TOP_Z_MIN = PCB_TOP_Z + SOCKET_BODY_HEIGHT_MIN
SOCKET_TOP_Z_MAX = PCB_TOP_Z + SOCKET_BODY_HEIGHT_MAX
MODULE_PCB_BOTTOM_Z_MIN = SOCKET_TOP_Z_MIN + MALE_HEADER_SPACER_HEIGHT_MIN
MODULE_PCB_BOTTOM_Z_MAX = SOCKET_TOP_Z_MAX + MALE_HEADER_SPACER_HEIGHT_MAX
MODULE_ENVELOPE_TOP_Z = MODULE_PCB_BOTTOM_Z_MAX + MODULE_ENVELOPE_HEIGHT_MAX

# Used by check_geometry.py's component-clearance proxy for the normal
# (tallest-case) module envelope.
SOCKET_TOP_Z = SOCKET_TOP_Z_MAX
MODULE_PCB_BOTTOM_Z = MODULE_PCB_BOTTOM_Z_MAX

RJ45_ENVELOPE_TOP_Z = PCB_TOP_Z + RJ45_VERTICAL_ENVELOPE
TALLEST_ENVELOPE_TOP_Z = max(MODULE_ENVELOPE_TOP_Z, RJ45_ENVELOPE_TOP_Z)
LID_UNDERSIDE_Z = TALLEST_ENVELOPE_TOP_Z + Z_CLEAR

LOCATING_POST_RADIUS = 1.25
LID_RETAINER_OUTER_RADIUS = 2.4
LID_RETAINER_INNER_RADIUS = 1.5

# ---------------------------------------------------------------------------
# Case envelope -- unchanged shape/margins from Rev3B.
# ---------------------------------------------------------------------------
DEFAULT_MARGIN = 4.0
MAGNET_MARGIN = 12.0

CAV_X0, CAV_X1 = PCB_X0 - XY_CLEAR, PCB_X1 + XY_CLEAR
CAV_Y0, CAV_Y1 = PCB_Y0 - XY_CLEAR, PCB_Y1 + XY_CLEAR

BASE_Z0 = 0.0
BASE_Z1 = PCB_TOP_Z + 3.75
LID_CEILING = 2.2
LID_Z0 = BASE_Z1 - 1.0
LID_Z1 = LID_UNDERSIDE_Z + LID_CEILING

RJ45_WINDOW_Y0, RJ45_WINDOW_Y1 = J1_BBOX["y_min"] - 0.75, J1_BBOX["y_max"] + 0.75
RJ45_WINDOW_Z0, RJ45_WINDOW_Z1 = PCB_TOP_Z - 0.5, RJ45_ENVELOPE_TOP_Z + 0.5

# USB window Y-range is the socketed module's USB_BBOX. Z-range spans from
# the shortest plausible stack's connector height (Z0, using the MIN socket
# + MIN spacer bound) to the tallest plausible envelope top plus cable
# margin (Z1, using the MAX bound) -- see the Z stack-up comment above.
USB_WINDOW_Y0, USB_WINDOW_Y1 = USB_BBOX["y_min"] - 0.75, USB_BBOX["y_max"] + 0.75
USB_WINDOW_Z0 = MODULE_PCB_BOTTOM_Z_MIN - 0.5
USB_WINDOW_Z1 = MODULE_ENVELOPE_TOP_Z + USB_CABLE_MARGIN

# Internal antenna ledge -- unchanged from Rev3B (independent of the U2
# socket change; placed relative to LID_UNDERSIDE_Z, which already
# recomputes with the new stack).
ANTENNA_FPC_WIDTH = 20.0
ANTENNA_FPC_LENGTH = 40.0
ANTENNA_FPC_X0 = 52.0

# External bulkhead datum -- unchanged from Rev3B.
EXTERNAL_PART = "TE/Linx CSB-RGFB-102-UFFR"
EXTERNAL_HOLE_DIAMETER = 6.5
EXTERNAL_HOLE_RADIUS = EXTERNAL_HOLE_DIAMETER / 2
EXTERNAL_FLAT_DATUM_MM = 6.0
EXTERNAL_MAX_PANEL_THICKNESS = 1.5
EXTERNAL_CABLE_LENGTH = 102.0
EXTERNAL_MIN_BEND_RADIUS = 10.0
EXTERNAL_HOLE_X = 93.0
EXTERNAL_HOLE_Z = 13.5

# Magnet pockets -- unchanged from Rev3B.
MAGNET_DIAMETER = 4.0
MAGNET_RADIUS = MAGNET_DIAMETER / 2 + 0.3
MAGNET_THICKNESS = 2.0
MAGNET_BASE_MARGIN = 0.8
MAGNET_PEDESTAL_RADIUS = MAGNET_RADIUS + 1.5
MAGNET_PAUSE_Z = FLOOR + MAGNET_BASE_MARGIN + MAGNET_THICKNESS
MAGNET_WALL_CLEARANCE = 1.5
MAGNET_CAVITY_CLEARANCE = 0.5


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
    """Open-top base: cavity, connector windows, board supports, and the two
    socket under-board tail-relief pockets.

    ``antenna`` selects "none", "internal", or "external" -- unchanged from
    Rev3B. The module is pressed into both sockets before the assembled
    board is placed into this base (the carrier and the module both arrive
    factory-assembled; nothing is soldered during installation) -- see
    README.md "Installation". That ordering is why no extra vertical
    insertion clearance needs to be reserved inside the case walls beyond
    the normal open-top cavity and the Z-stack above.
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

    # Under-board relief below the through-hole RJ45 tails -- unchanged from Rev3B.
    j1_tail_pocket = _box(
        PCB_X0,
        J1_BBOX["x_max"] + 0.75,
        J1_BBOX["y_min"] - 0.75,
        J1_BBOX["y_max"] + 0.75,
        J1_TAIL_FLOOR_SKIN,
        FLOOR + 0.05,
    )
    base = base - j1_tail_pocket

    # Under-board relief below each socket row's through-hole tails. Same
    # pattern as J1's pocket (cut connects into the already-open cavity at
    # FLOOR + 0.05 so it isn't a sealed internal void), sized from
    # SOCKET_TAIL_CLEARANCE_DEPTH/SOCKET_TAIL_FLOOR_SKIN.
    for bbox in SOCKET_BBOX:
        socket_tail_pocket = _box(
            bbox["x_min"] - 0.75,
            bbox["x_max"] + 0.75,
            bbox["y_min"] - 0.75,
            bbox["y_max"] + 0.75,
            PCB_SEAT_Z - SOCKET_TAIL_CLEARANCE_DEPTH,
            FLOOR + 0.05,
        )
        base = base - socket_tail_pocket

    # J1 RJ45: left-wall opening (x=0 side) -- unchanged from Rev3B.
    rj45_window = _box(
        base_x0 - 0.2, 1.0,
        RJ45_WINDOW_Y0, RJ45_WINDOW_Y1,
        RJ45_WINDOW_Z0, RJ45_WINDOW_Z1,
    )
    base = base - rj45_window

    # USB-C: right-wall opening (x=99 side). Y-range and Z-range are the
    # recomputed socketed-module values (USB_WINDOW_* above) -- deliberately
    # NOT widened to also expose BOOT0/RST0 the way Rev3B's single window
    # did, because the re-derived button centers (x=79.0) sit far from the
    # USB-C window (x>=91.2), on the opposite side of the module. See the
    # separate button bores in make_lid().
    usb_window = _box(
        98.0, base_x1 + 0.2,
        USB_WINDOW_Y0, USB_WINDOW_Y1,
        USB_WINDOW_Z0, USB_WINDOW_Z1,
    )
    base = base - usb_window

    for x, y in MOUNT_HOLES:
        boss = _cylinder(3.0, FLOOR, PCB_SEAT_Z, x, y) - _cylinder(1.9, FLOOR - 0.1, PCB_SEAT_Z + 0.15, x, y)
        locating_post = _cylinder(LOCATING_POST_RADIUS, FLOOR - 0.1, PCB_TOP_Z + 0.30, x, y)
        base = base + boss + locating_post

    if magnets:
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
    return Cylinder(
        radius,
        y1 - y0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).locate(Location((x, y1, z), (90, 0, 0)))


def make_lid(magnets: bool = False, antenna: str = "none") -> Part:
    """Vent-free lid with skirt, snap beads, LED apertures, and button bores.

    The ``magnets`` flag must match the value passed to make_base().

    No lid-underside retention rib is added over the module: the module's
    own board-edge footprint is a candidate, not a verified bare-laminate
    zone distinct from BOOT0/RST0/ANT0/USB0, so there is no verified landing
    spot for a non-contact rib. Retention instead relies on the female
    sockets' own pin friction/engagement, same as any 2.54 mm header socket.
    README.md calls for a physical vibration and cable-tug check on a
    bench; passing this file's geometry checks is not proof of header
    engagement under load.
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

    # Tool access to the re-derived BOOT0/RST0 centers. Non-contact by
    # construction (bored the full lid thickness), same pattern as Rev3B --
    # the lid never presses a plunger against either switch.
    for x, y in BUTTON_POSITIONS.values():
        lid = lid - _cylinder(
            BUTTON_ACCESS_RADIUS,
            lid_z1 - LID_CEILING - 0.1,
            lid_z1 + 0.1,
            x,
            y,
        )

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
        hole = _cylinder_y(
            EXTERNAL_HOLE_RADIUS,
            lid_y1 - 1.7,
            lid_y1 + 0.2,
            EXTERNAL_HOLE_X,
            EXTERNAL_HOLE_Z,
        )
        lid = lid - hole

    if antenna == "internal":
        lid = lid + make_internal_antenna_ledge()

    return lid


def make_internal_antenna_ledge() -> Part:
    """Shallow alignment lip for an adhesive-backed external FPC antenna --
    unchanged from Rev3B (see that module's docstring); only its Z position
    changes, automatically, via the recomputed LID_UNDERSIDE_Z.
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

    _export(base, f"rev3c_base{suffix}", args.out)
    _export(lid, f"rev3c_lid{suffix}", args.out)

    print(f"wrote {args.out / f'rev3c_base{suffix}.stl'} and {args.out / f'rev3c_lid{suffix}.stl'}")


if __name__ == "__main__":
    main()
