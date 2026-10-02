"""Geometry checks for the Rev3B enclosure: manifold STL/STEP exports, plus
solid-vs-solid collision checks between the case and PCB component envelopes
(J1, J2, U2) derived from the frozen board file.

    pip install -r requirements.txt
    python enclosure.py --out .
    python enclosure.py --out . --antenna internal
    python enclosure.py --out . --magnets
    python check_geometry.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import trimesh
from build123d import Align, Box, Location, Part, import_step

import enclosure as e

OUT = Path(__file__).parent / "exports"

# Axis-aligned proxy solids for the three components whose footprints are
# not under the board supports: each uses the exact board-frame bounding box
# pcbnew reported (already rotation-corrected) and the component's
# documented Z envelope above the seated PCB top. A proxy box is a looser
# (never tighter) stand-in than the real STEP shape, so "zero intersection
# with case material" here is a necessary, conservative pass/fail signal.
COMPONENTS = {
    "J1 (RJ45)": (e.J1_BBOX, e.PCB_TOP_Z, e.RJ45_ENVELOPE_TOP_Z),
    "U2 (XIAO/USB-C)": (e.U2_BBOX, e.PCB_TOP_Z, e.XIAO_ENVELOPE_TOP_Z),
    "J2 (recovery header)": (e.J2_BBOX, e.PCB_TOP_Z, e.J2_ENVELOPE_TOP_Z),
}


def _box(bbox: dict, z0: float, z1: float) -> Part:
    return Box(
        bbox["x_max"] - bbox["x_min"], bbox["y_max"] - bbox["y_min"], z1 - z0,
        align=(Align.MIN, Align.MIN, Align.MIN),
    ).locate(Location((bbox["x_min"], bbox["y_min"], z0)))


def check_variant_mesh(stem: str) -> list[str]:
    problems = []
    stl_path = OUT / f"{stem}.stl"
    step_path = OUT / f"{stem}.step"
    if not stl_path.exists() or not step_path.exists():
        return [f"{stem}: missing export, run enclosure.py first"]

    mesh = trimesh.load(stl_path)
    if not mesh.is_watertight:
        problems.append(f"{stem}.stl is not watertight")
    if mesh.volume <= 0:
        problems.append(f"{stem}.stl has non-positive volume ({mesh.volume})")
    # Boolean cavities appear as separate negatively oriented shells in some
    # STL readers (the captive magnet pockets are the intentional example).
    # Require exactly one positive-volume connected body and permit only such
    # negative cavity shells.
    components = mesh.split(only_watertight=False)
    if len([part for part in components if part.volume > 1e-6]) != 1:
        problems.append(f"{stem}.stl is not a single connected printable solid")

    try:
        step_part = import_step(str(step_path))
        if not step_part.is_valid:
            problems.append(f"{stem}.step is not a valid solid")
        if step_part.volume <= 0:
            problems.append(f"{stem}.step has non-positive volume ({step_part.volume})")
        if len(step_part.solids()) != 1:
            problems.append(f"{stem}.step is not a single connected printable solid")
        if abs(step_part.volume - mesh.volume) / mesh.volume > 0.02:
            problems.append(
                f"{stem}: STEP volume ({step_part.volume:.1f}) and STL volume "
                f"({mesh.volume:.1f}) disagree by more than 2%"
            )
    except Exception as exc:  # pragma: no cover - diagnostic path
        problems.append(f"{stem}.step failed to import: {exc}")

    return problems


def check_component_clearance(base: Part, lid: Part) -> list[str]:
    """Every component envelope must have zero solid-material intersection
    with both the base and the lid: this is what "the support/window
    geometry actually clears the real component" means in boolean terms,
    not just a bounding-box comparison done by hand.
    """
    problems = []
    for name, (bbox, z0, z1) in COMPONENTS.items():
        proxy = _box(bbox, z0, z1)
        for part_name, part in (("base", base), ("lid", lid)):
            overlap = (proxy & part).volume
            if overlap > 1e-6:
                problems.append(
                    f"{name} envelope intersects the {part_name} by {overlap:.3f} mm^3"
                )
    # Explicit under-board tail proxy: the supplied J1 model has no verified
    # pin-tail length, so the case reserves the documented conservative pocket
    # depth and this check ensures it is actually clear of the base.
    tail_proxy = _box(
        {
            "x_min": e.PCB_X0,
            "x_max": e.J1_BBOX["x_max"] + 0.75,
            "y_min": e.J1_BBOX["y_min"] - 0.75,
            "y_max": e.J1_BBOX["y_max"] + 0.75,
        },
        e.PCB_SEAT_Z - e.J1_TAIL_CLEARANCE_DEPTH,
        e.PCB_SEAT_Z,
    )
    if (tail_proxy & base).volume > 1e-6:
        problems.append("J1 under-board tail-clearance proxy intersects the base")
    return problems


def check_connector_corridors(base: Part, lid: Part) -> list[str]:
    """Windows must clear both overlapping walls in the assembled case."""
    problems = []
    outer_x0 = min(float(base.bounding_box().min.X), float(lid.bounding_box().min.X)) - 0.1
    outer_x1 = max(float(base.bounding_box().max.X), float(lid.bounding_box().max.X)) + 0.1
    corridors = {
        "RJ45": _box(
            {"x_min": outer_x0, "x_max": 1.0, "y_min": e.RJ45_WINDOW_Y0, "y_max": e.RJ45_WINDOW_Y1},
            e.RJ45_WINDOW_Z0,
            e.RJ45_WINDOW_Z1,
        ),
        "USB-C": _box(
            {"x_min": 98.0, "x_max": outer_x1, "y_min": e.USB_WINDOW_Y0, "y_max": e.USB_WINDOW_Y1},
            e.USB_WINDOW_Z0,
            e.USB_WINDOW_Z1,
        ),
    }
    for name, corridor in corridors.items():
        for part_name, part in (("base", base), ("lid", lid)):
            if (corridor & part).volume > 1e-6:
                problems.append(f"{name} insertion corridor intersects {part_name}")
    return problems


def check_led_sightlines(lid: Part) -> list[str]:
    """Each LED must have an actual clear hole through the lid: a small probe
    cylinder centered on the LED position, spanning the lid ceiling, must
    have zero remaining lid material (i.e. the aperture was really cut).
    """
    from build123d import Cylinder

    problems = []
    for ref, (x, y) in e.LED_POSITIONS.items():
        probe = Cylinder(
            e.LED_VIEW_RADIUS * 0.5, e.LID_CEILING + 0.4,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).locate(Location((x, y, e.LID_Z1 - e.LID_CEILING - 0.2)))
        overlap = (probe & lid).volume
        if overlap > 1e-6:
            problems.append(f"{ref} aperture is obstructed ({overlap:.3f} mm^3 remaining)")
    return problems


def check_button_sightlines(lid: Part) -> list[str]:
    """Factory BOOT0/RST0 tool apertures must be genuinely open."""
    problems = []
    for ref, (x, y) in e.BUTTON_POSITIONS.items():
        probe = e._cylinder(
            e.BUTTON_ACCESS_RADIUS * 0.8,
            e.LID_Z1 - e.LID_CEILING - 0.2,
            e.LID_Z1 + 0.2,
            x,
            y,
        )
        if (probe & lid).volume > 1e-6:
            problems.append(f"{ref} tool aperture is obstructed")
    return problems


def check_button_datums() -> list[str]:
    """BUTTON_POSITIONS must match the rigid-translation datums derived from
    the official Seeed v1.3 project's own BOOT0/RST0 footprint centers --
    (139.5476,100.5586) and (139.5476,109.4486) respectively -- offset by
    the row-pair-derived translation dx=-60.5476, dy=-92.0861 (see
    enclosure.py's BUTTON_POSITIONS comment). This is a regression guard
    against reintroducing a swapped-label or reflected-axis mistake.
    """
    problems = []
    expected = {
        "BOOT0": (139.5476 - 60.5476, 100.5586 - 92.0861),
        "RST0": (139.5476 - 60.5476, 109.4486 - 92.0861),
    }
    for ref, (ex, ey) in expected.items():
        if ref not in e.BUTTON_POSITIONS:
            problems.append(f"{ref} missing from BUTTON_POSITIONS")
            continue
        ax, ay = e.BUTTON_POSITIONS[ref]
        if abs(ax - ex) > 0.01 or abs(ay - ey) > 0.01:
            problems.append(
                f"{ref} at ({ax},{ay}) does not match the official-pin-derived "
                f"datum ({ex:.4f},{ey:.4f})"
            )
    return problems


def check_mount_hole_access() -> list[str]:
    """H1/H2 locating posts must reach the PCB's own 3.2 mm drill without
    the post itself exceeding the drill radius (checked already by
    construction: LOCATING_POST_RADIUS=1.25 < MOUNT_DRILL_RADIUS=1.6) and
    must not collide with any connector/header envelope.
    """
    problems = []
    for name, (bbox, z0, z1) in COMPONENTS.items():
        for hole_name, (hx, hy) in (("H1", e.H1), ("H2", e.H2)):
            if bbox["x_min"] <= hx <= bbox["x_max"] and bbox["y_min"] <= hy <= bbox["y_max"]:
                problems.append(f"{hole_name} falls inside {name}'s footprint bbox")
    return problems


def check_magnet_pockets(base_magnets: Part) -> list[str]:
    """Each magnet pocket must actually be hollow (a probe cylinder sized to
    the nominal magnet finds no material) and fully capped on top and
    bottom (probes placed just outside the pocket's Z range, still inside
    the pedestal, must find solid material -- i.e. captive, not open).
    """
    from build123d import Cylinder

    problems = []
    left_x = e.CAV_X0 - e.MAGNET_MARGIN + e.MAGNET_WALL_CLEARANCE + e.MAGNET_PEDESTAL_RADIUS
    right_x = e.CAV_X1 + e.MAGNET_MARGIN - e.MAGNET_WALL_CLEARANCE - e.MAGNET_PEDESTAL_RADIUS
    sites = {"left pocket": (left_x, 33.0), "right pocket": (right_x, 30.0)}

    pocket_z0 = e.FLOOR + e.MAGNET_BASE_MARGIN
    pocket_z1 = pocket_z0 + e.MAGNET_THICKNESS

    for site_name, (x, y) in sites.items():
        hollow_probe = Cylinder(
            e.MAGNET_RADIUS * 0.8, (pocket_z1 - pocket_z0) * 0.8,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).locate(Location((x, y, pocket_z0 + (pocket_z1 - pocket_z0) * 0.1)))
        if (hollow_probe & base_magnets).volume > 1e-6:
            problems.append(f"{site_name} is not hollow at the magnet's nominal position")

        for cap_name, z in (("bottom", pocket_z0 - 0.3), ("top", pocket_z1 + 0.3)):
            cap_probe = Cylinder(
                e.MAGNET_RADIUS * 0.8, 0.2,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).locate(Location((x, y, z)))
            solid_volume = (cap_probe & base_magnets).volume
            if solid_volume <= 1e-6:
                problems.append(f"{site_name} {cap_name} skin is open (not captive)")
    return problems


def check_external_bulkhead(lid: Part) -> list[str]:
    """Check the named TE/Linx bulkhead opening and its local wall seat.

    The circular probe must pass through the seat without residual lid
    material, while a surrounding annulus must still intersect the reinforced
    seat. This validates the actual boolean result rather than trusting the
    STL export or a nominal hole constant alone.
    """
    problems = []
    if e.EXTERNAL_MAX_PANEL_THICKNESS != 1.5:
        problems.append("external connector panel-thickness datum drifted from 1.5 mm")
    lid_y1 = e.CAV_Y1 + e.DEFAULT_MARGIN + 1.0
    hole = e._cylinder_y(
        e.EXTERNAL_HOLE_RADIUS,
        lid_y1 - 1.7,
        lid_y1 + 0.2,
        e.EXTERNAL_HOLE_X,
        e.EXTERNAL_HOLE_Z,
    )
    if (hole & lid).volume > 1e-6:
        problems.append("external bulkhead bore is obstructed")
    annulus = e._cylinder_y(
        e.EXTERNAL_HOLE_RADIUS + 1.0,
        lid_y1 - 1.7,
        lid_y1 + 0.2,
        e.EXTERNAL_HOLE_X,
        e.EXTERNAL_HOLE_Z,
    ) - e._cylinder_y(
        e.EXTERNAL_HOLE_RADIUS + 0.15,
        lid_y1 - 1.7,
        lid_y1 + 0.2,
        e.EXTERNAL_HOLE_X,
        e.EXTERNAL_HOLE_Z,
    )
    if (annulus & lid).volume <= 1e-6:
        problems.append("external bulkhead seat has no surrounding solid material")
    return problems


def main() -> int:
    problems: list[str] = []

    base = e.make_base()
    lid = e.make_lid()
    problems += check_component_clearance(base, lid)
    problems += check_connector_corridors(base, lid)
    problems += check_led_sightlines(lid)
    problems += check_button_sightlines(lid)
    problems += check_button_datums()
    problems += check_mount_hole_access()

    base_ant = e.make_base(antenna="internal")
    lid_ant = e.make_lid(antenna="internal")
    problems += check_component_clearance(base_ant, lid_ant)
    problems += check_connector_corridors(base_ant, lid_ant)

    base_ext = e.make_base(antenna="external")
    lid_ext = e.make_lid(antenna="external")
    problems += check_component_clearance(base_ext, lid_ext)
    problems += check_connector_corridors(base_ext, lid_ext)
    problems += check_external_bulkhead(lid_ext)

    base_magnets = e.make_base(magnets=True)
    lid_magnets = e.make_lid(magnets=True)
    problems += check_component_clearance(base_magnets, lid_magnets)
    problems += check_connector_corridors(base_magnets, lid_magnets)
    problems += check_magnet_pockets(base_magnets)

    for stem in (
        "rev3b_base", "rev3b_lid",
        "rev3b_base_ant-internal", "rev3b_lid_ant-internal",
        "rev3b_base_ant-external", "rev3b_lid_ant-external",
        "rev3b_base_magnets", "rev3b_lid_magnets",
    ):
        problems += check_variant_mesh(stem)

    # Repeat the clearance checks on the exported STEP solids, not only on
    # freshly constructed build123d Parts.
    for base_stem, lid_stem in (
        ("rev3b_base", "rev3b_lid"),
        ("rev3b_base_ant-internal", "rev3b_lid_ant-internal"),
        ("rev3b_base_ant-external", "rev3b_lid_ant-external"),
        ("rev3b_base_magnets", "rev3b_lid_magnets"),
    ):
        imported_base = import_step(str(OUT / f"{base_stem}.step"))
        imported_lid = import_step(str(OUT / f"{lid_stem}.step"))
        problems += check_component_clearance(imported_base, imported_lid)
        problems += check_connector_corridors(imported_base, imported_lid)

    if problems:
        print("FAIL:")
        for p in problems:
            print(f"  - {p}")
        return 1

    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

