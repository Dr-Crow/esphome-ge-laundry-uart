"""Geometry checks for the Rev3C enclosure: manifold STL/STEP exports, plus
solid-vs-solid collision checks between the case and PCB/socket/module
envelopes (J1, J2, the two sockets, and the plugged-in module).

    pip install -r requirements.txt
    python enclosure.py --out .
    python enclosure.py --out . --antenna internal
    python enclosure.py --out . --magnets
    python check_geometry.py

All default checks here are portable: pure build123d/trimesh geometry
against this file's own constants, no private paths and no external KiCad
dependency. Two checks are optional and off by default:

    python check_geometry.py --kicad-python /path/to/kicad/python3 \\
        --official-module /path/to/XIAO-ESP32-C3-v1.3.kicad_pcb \\
        --carrier-board /path/to/GEA-Adapter-Rev3C.kicad_pcb

``--official-module`` re-derives BOOT0/RST0/ANT0/USB0 from Seeed's
officially published XIAO ESP32-C3 v1.3 KiCad hardware files with native
pcbnew and compares them against this file's BUTTON_POSITIONS/ANT0_POSITION/
USB0_POSITION constants. ``--carrier-board`` compares the two socket
footprints' actual placement on a real Rev3C carrier board file (once one
exists) against SOCKET_ROW_Y/SOCKET_PIN_X0/SOCKET_PIN_X1. Both need
``--kicad-python`` (KiCad's bundled Python interpreter, which ships
``pcbnew``; the project's own venv does not). Any check whose required file
is omitted or missing is reported as skipped, not failed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import trimesh
from build123d import Align, Box, Cylinder, Location, Part, import_step

import enclosure as e

OUT = Path(__file__).parent / "exports"

# Expected positions for the optional native-pcbnew cross-check below --
# these alias enclosure.py's own BUTTON_POSITIONS/ANT0_POSITION/
# USB0_POSITION constants, they are not a separately recorded copy. The
# independence in check_official_module() comes from the LEFT side of that
# comparison: it loads Seeed's officially published XIAO ESP32-C3 v1.3
# KiCad hardware files directly with native pcbnew (module product page:
# https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32C3-Pre-Soldered-p-6331.html)
# and re-applies the documented offset, so the check still catches
# enclosure.py drifting from the official source -- it just isn't a
# second, independently-typed copy of the expected numbers.
EXPECTED_OFFICIAL_POSITIONS = {
    "BOOT0": e.BUTTON_POSITIONS["BOOT0"],
    "RST0": e.BUTTON_POSITIONS["RST0"],
    "ANT0": e.ANT0_POSITION,
    "USB0": e.USB0_POSITION,
}
OFFICIAL_TRANSFORM_DX, OFFICIAL_TRANSFORM_DY = -60.5476, -92.0861

# Axis-aligned proxy solids. Each uses a documented board-frame bounding box
# (never tighter than the real/candidate envelope) and a Z range above the
# seated PCB top, so "zero intersection with case material" is a necessary,
# conservative pass/fail signal.
COMPONENTS = {
    "J1 (RJ45)": (e.J1_BBOX, e.PCB_TOP_Z, e.RJ45_ENVELOPE_TOP_Z),
    "J2 (recovery header)": (e.J2_BBOX, e.PCB_TOP_Z, e.J2_ENVELOPE_TOP_Z),
    "Socket row A (y=5.2975)": (e.SOCKET_BBOX[0], e.PCB_TOP_Z, e.SOCKET_TOP_Z_MAX),
    "Socket row B (y=20.5375)": (e.SOCKET_BBOX[1], e.PCB_TOP_Z, e.SOCKET_TOP_Z_MAX),
    "Module, max stack (plugged-in XIAO)": (
        e.MODULE_BBOX, e.MODULE_PCB_BOTTOM_Z_MAX, e.MODULE_ENVELOPE_TOP_Z,
    ),
    "Module, min stack (plugged-in XIAO)": (
        e.MODULE_BBOX,
        e.MODULE_PCB_BOTTOM_Z_MIN,
        e.MODULE_PCB_BOTTOM_Z_MIN + e.MODULE_ENVELOPE_HEIGHT_MAX,
    ),
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
    """Every component envelope -- including both the min-stack and
    max-stack module proxies -- must have zero solid-material intersection
    with both the base and the lid.
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

    # Under-board tail proxies: J1's (unchanged from Rev3B) plus the two
    # socket rows.
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

    for idx, bbox in enumerate(e.SOCKET_BBOX):
        socket_tail_proxy = _box(
            {
                "x_min": bbox["x_min"] - 0.75,
                "x_max": bbox["x_max"] + 0.75,
                "y_min": bbox["y_min"] - 0.75,
                "y_max": bbox["y_max"] + 0.75,
            },
            e.PCB_SEAT_Z - e.SOCKET_TAIL_CLEARANCE_DEPTH,
            e.PCB_SEAT_Z,
        )
        if (socket_tail_proxy & base).volume > 1e-6:
            problems.append(f"Socket row {idx} under-board tail-clearance proxy intersects the base")
        remaining_skin = e.PCB_SEAT_Z - e.SOCKET_TAIL_CLEARANCE_DEPTH
        if remaining_skin < e.SOCKET_TAIL_FLOOR_SKIN - 1e-9:
            problems.append(
                f"Socket row {idx} tail pocket leaves only {remaining_skin:.3f} mm of floor "
                f"skin, below the documented {e.SOCKET_TAIL_FLOOR_SKIN} mm minimum"
            )

    return problems


def check_usb_window_stack_coverage() -> list[str]:
    """The USB window's Z-span must cover the full plausible assembled
    range, from the shortest plausible stack's connector height to the
    tallest plausible envelope top -- not only the tallest-case figure.
    """
    problems = []
    if e.USB_WINDOW_Z0 > e.MODULE_PCB_BOTTOM_Z_MIN - 1e-9:
        problems.append(
            "USB_WINDOW_Z0 does not clear the minimum plausible stack's module-PCB-bottom height"
        )
    if e.USB_WINDOW_Z1 < e.MODULE_ENVELOPE_TOP_Z - 1e-9:
        problems.append(
            "USB_WINDOW_Z1 does not clear the maximum plausible stack's envelope top"
        )
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
    """BOOT0/RST0 tool apertures must be genuinely open, and must sit over
    the module's own footprint (not off in empty case space).
    """
    problems = []
    for ref, (x, y) in e.BUTTON_POSITIONS.items():
        if not (e.MODULE_BBOX["x_min"] <= x <= e.MODULE_BBOX["x_max"]):
            problems.append(f"{ref} x={x} falls outside the module's own board-edge bbox")
        if not (e.MODULE_BBOX["y_min"] <= y <= e.MODULE_BBOX["y_max"]):
            problems.append(f"{ref} y={y} falls outside the module's own board-edge bbox")
        probe = e._cylinder(
            e.BUTTON_ACCESS_RADIUS * 0.8,
            e.LID_Z1 - e.LID_CEILING - 0.2,
            e.LID_Z1 + 0.2,
            x,
            y,
        )
        if (probe & lid).volume > 1e-6:
            problems.append(f"{ref} tool aperture is obstructed")
    xs = {round(x, 4) for x, _ in e.BUTTON_POSITIONS.values()}
    ys = {round(y, 4) for _, y in e.BUTTON_POSITIONS.values()}
    if len(xs) != 1 or len(ys) != 2:
        problems.append(
            "BUTTON_POSITIONS topology regressed: expected BOOT0/RST0 to share X and differ in Y"
        )
    return problems


def check_mount_hole_access() -> list[str]:
    problems = []
    for name, (bbox, z0, z1) in COMPONENTS.items():
        for hole_name, (hx, hy) in (("H1", e.H1), ("H2", e.H2)):
            if bbox["x_min"] <= hx <= bbox["x_max"] and bbox["y_min"] <= hy <= bbox["y_max"]:
                problems.append(f"{hole_name} falls inside {name}'s footprint bbox")
    return problems


def check_magnet_pockets(base_magnets: Part) -> list[str]:
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


def check_socket_height_budget() -> list[str]:
    """Sanity-check the Z-stack arithmetic itself (independent of boolean
    geometry), so a future edit to one term can't silently drop another.
    """
    problems = []
    expected_max_top = (
        e.PCB_TOP_Z
        + e.SOCKET_BODY_HEIGHT_MAX
        + e.MALE_HEADER_SPACER_HEIGHT_MAX
        + e.MODULE_ENVELOPE_HEIGHT_MAX
    )
    if abs(expected_max_top - e.MODULE_ENVELOPE_TOP_Z) > 1e-9:
        problems.append(
            "MODULE_ENVELOPE_TOP_Z does not equal the sum of its documented max-stack terms: "
            f"got {e.MODULE_ENVELOPE_TOP_Z}, expected {expected_max_top}"
        )
    expected_min_bottom = (
        e.PCB_TOP_Z + e.SOCKET_BODY_HEIGHT_MIN + e.MALE_HEADER_SPACER_HEIGHT_MIN
    )
    if abs(expected_min_bottom - e.MODULE_PCB_BOTTOM_Z_MIN) > 1e-9:
        problems.append(
            "MODULE_PCB_BOTTOM_Z_MIN does not equal the sum of its documented min-stack terms: "
            f"got {e.MODULE_PCB_BOTTOM_Z_MIN}, expected {expected_min_bottom}"
        )
    if e.LID_UNDERSIDE_Z < e.MODULE_ENVELOPE_TOP_Z:
        problems.append("LID_UNDERSIDE_Z sits below the module's own max-stack envelope top")
    return problems


def _run_pcbnew(kicad_python: Path, script: str) -> tuple[int, str, str]:
    import subprocess

    result = subprocess.run(
        [str(kicad_python), "-c", script], capture_output=True, text=True, timeout=60
    )
    return result.returncode, result.stdout, result.stderr


def check_official_module(kicad_python: Path | None, official_module: Path | None) -> list[str]:
    """Optional: re-derive BOOT0/RST0/ANT0/USB0 from Seeed's officially
    published KiCad hardware files with native pcbnew, independent of this
    file's own constants, and compare against EXPECTED_OFFICIAL_POSITIONS.
    """
    if kicad_python is None or official_module is None:
        print("skipped: --official-module cross-check (no --kicad-python/--official-module given)")
        return []
    if not kicad_python.exists():
        return [f"--kicad-python {kicad_python} does not exist"]
    if not official_module.exists():
        return [f"--official-module {official_module} does not exist"]

    script = f'''
import pcbnew
b = pcbnew.LoadBoard(r"{official_module}")
for fp in b.GetFootprints():
    ref = fp.GetReference()
    if ref in ("BOOT0", "RST0", "ANT0", "USB0"):
        pos = fp.GetPosition()
        print(ref, pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y))
'''
    returncode, stdout, stderr = _run_pcbnew(kicad_python, script)
    if returncode != 0 or not stdout.strip():
        return [f"native pcbnew cross-check (official module) produced no output: {stderr.strip()[:500]}"]

    native = {}
    for line in stdout.strip().splitlines():
        ref, ox, oy = line.split()
        native[ref] = (float(ox), float(oy))

    if set(native) != set(EXPECTED_OFFICIAL_POSITIONS):
        return [
            f"native pcbnew cross-check found refs {sorted(native)}, "
            f"expected {sorted(EXPECTED_OFFICIAL_POSITIONS)}"
        ]

    problems = []
    for ref, (ex, ey) in EXPECTED_OFFICIAL_POSITIONS.items():
        ox, oy = native[ref]
        cx, cy = ox + OFFICIAL_TRANSFORM_DX, oy + OFFICIAL_TRANSFORM_DY
        if abs(cx - ex) > 0.01 or abs(cy - ey) > 0.01:
            problems.append(
                f"{ref}: native pcbnew + documented offset gives ({cx:.4f}, {cy:.4f}), "
                f"enclosure.py has ({ex}, {ey})"
            )
    return problems


def check_carrier_board(kicad_python: Path | None, carrier_board: Path | None) -> list[str]:
    """Optional: compare the two socket footprints' actual placement on a
    real Rev3C carrier board file against SOCKET_ROW_Y/SOCKET_PIN_X0/
    SOCKET_PIN_X1, when such a board file is available.
    """
    if kicad_python is None or carrier_board is None:
        print("skipped: --carrier-board cross-check (no --kicad-python/--carrier-board given)")
        return []
    if not kicad_python.exists():
        return [f"--kicad-python {kicad_python} does not exist"]
    if not carrier_board.exists():
        return [f"--carrier-board {carrier_board} does not exist"]

    script = f'''
import pcbnew
b = pcbnew.LoadBoard(r"{carrier_board}")
for fp in b.GetFootprints():
    name = str(fp.GetFPID().GetLibItemName())
    if "Socket" in name and "HCTL" in name:
        pos = fp.GetPosition()
        print(fp.GetReference(), pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y))
'''
    returncode, stdout, stderr = _run_pcbnew(kicad_python, script)
    if returncode != 0 or not stdout.strip():
        return [f"native pcbnew cross-check (carrier board) produced no output: {stderr.strip()[:500]}"]

    found_x = set()
    found_y = set()
    for line in stdout.strip().splitlines():
        _ref, ox, oy = line.split()
        found_x.add(round(float(ox), 4))
        found_y.add(round(float(oy), 4))

    problems = []
    expected_y = {round(y, 4) for y in e.SOCKET_ROW_Y}
    expected_x = {round(e.SOCKET_PIN_X0, 4), round(e.SOCKET_PIN_X1, 4)}
    if found_y != expected_y:
        problems.append(f"carrier board socket row Y positions {found_y} != expected {expected_y}")
    if not expected_x.issubset(found_x):
        problems.append(f"carrier board socket pin-row X positions {found_x} do not include expected {expected_x}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kicad-python", type=Path, default=None, help="KiCad's bundled python3 (ships pcbnew)")
    parser.add_argument("--official-module", type=Path, default=None, help="Seeed official XIAO ESP32-C3 v1.3 .kicad_pcb")
    parser.add_argument("--carrier-board", type=Path, default=None, help="Rev3C carrier .kicad_pcb, once one exists")
    args = parser.parse_args()

    problems: list[str] = []

    problems += check_socket_height_budget()
    problems += check_usb_window_stack_coverage()
    problems += check_official_module(args.kicad_python, args.official_module)
    problems += check_carrier_board(args.kicad_python, args.carrier_board)

    base = e.make_base()
    lid = e.make_lid()
    problems += check_component_clearance(base, lid)
    problems += check_connector_corridors(base, lid)
    problems += check_led_sightlines(lid)
    problems += check_button_sightlines(lid)
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
        "rev3c_base", "rev3c_lid",
        "rev3c_base_ant-internal", "rev3c_lid_ant-internal",
        "rev3c_base_ant-external", "rev3c_lid_ant-external",
        "rev3c_base_magnets", "rev3c_lid_magnets",
    ):
        problems += check_variant_mesh(stem)

    for base_stem, lid_stem in (
        ("rev3c_base", "rev3c_lid"),
        ("rev3c_base_ant-internal", "rev3c_lid_ant-internal"),
        ("rev3c_base_ant-external", "rev3c_lid_ant-external"),
        ("rev3c_base_magnets", "rev3c_lid_magnets"),
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
