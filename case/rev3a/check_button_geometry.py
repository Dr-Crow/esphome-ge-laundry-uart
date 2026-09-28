"""Focused geometry checks for the optional Rev3A captive-button assembly."""

from __future__ import annotations

import argparse
from pathlib import Path

import trimesh
from build123d import Location, import_step

from button_case import (
    BUTTON_CENTERS, BUTTON_SPACING, FLANGE_CLEAR_RADIUS, FLANGE_RADIUS,
    FLANGE_REST_BOTTOM_Z, FLANGE_REST_TOP_Z, FULL_PRESS_TIP_Z,
    GUIDE_OUTER_RADIUS, KEEPER_BOTTOM_Z, KEEPER_HOLE_RADIUS, KEEPER_TOP_Z,
    NOMINAL_STROKE, PAD_RADIUS, REST_TIP_Z, SLIDER_RADIUS, SWITCH_HEIGHT,
    SWITCH_MODEL, SWITCH_TOP_Z, THROAT_RADIUS, UPPER_THROAT_BOTTOM_Z,
    _cylinder, make_button_lid, make_keeper, make_plunger,
)
from enclosure import ANTENNA_X0, J2_HALF_X, J2_HALF_Y, J2_X, J2_Y, PCB_TOP_Z, RJ45_NOTCH_X1, _box


EPS = 0.01


def _volume(shape) -> float:
    if shape is None:
        return 0.0
    if hasattr(shape, "volume"):
        return float(shape.volume)
    return sum(float(item.volume) for item in shape if hasattr(item, "volume"))


def _export_check(path: Path, name: str) -> None:
    mesh = trimesh.load_mesh(path, process=True)
    assert isinstance(mesh, trimesh.Trimesh), name
    assert mesh.is_watertight and mesh.is_volume, f"{name} STL is not a watertight volume"
    step = import_step(path.with_suffix(".step"))
    assert step.is_valid and len(step.solids()) == 1, f"{name} STEP is not one valid solid"
    print(f"{name}: STL watertight=True bounds={mesh.bounds.tolist()}; STEP solid=True")


def _placed_switch(x: float, y: float):
    # Fresh STEP solids for every pose: Location mutates build123d objects.
    raw = import_step(SWITCH_MODEL).solids()
    body = [i for i, s in enumerate(raw) if float(s.bounding_box().max.Z) <= 1.20 + 1e-6]
    actuator = [i for i, s in enumerate(raw) if float(s.bounding_box().min.Z) >= 1.0 - 1e-6]
    assert body and actuator and not set(body).intersection(actuator)
    placed = [s.locate(Location((x, y, PCB_TOP_Z))) for s in raw]
    return placed, body, actuator


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()

    lid = make_button_lid()
    keeper = make_keeper()
    assert lid.is_valid and keeper.is_valid
    assert BUTTON_SPACING == 8.0
    assert 2.0 * GUIDE_OUTER_RADIUS < BUTTON_SPACING
    assert THROAT_RADIUS > PAD_RADIUS > SLIDER_RADIUS
    assert FLANGE_CLEAR_RADIUS > FLANGE_RADIUS > THROAT_RADIUS
    assert FLANGE_CLEAR_RADIUS - FLANGE_RADIUS >= 0.10
    assert GUIDE_OUTER_RADIUS - FLANGE_CLEAR_RADIUS >= 0.80
    assert KEEPER_HOLE_RADIUS > SLIDER_RADIUS
    assert abs((FLANGE_REST_BOTTOM_Z - KEEPER_TOP_Z) - NOMINAL_STROKE) < 1e-9
    assert abs((REST_TIP_Z - FULL_PRESS_TIP_Z) - NOMINAL_STROKE) < 1e-9
    assert abs(FLANGE_REST_TOP_Z - UPPER_THROAT_BOTTOM_Z) < 1e-9

    for stem in ("rev3a_button_lid", "rev3a_button_plunger", "rev3a_button_keeper"):
        _export_check(args.dir / f"{stem}.stl", stem)

    raw_switch = import_step(SWITCH_MODEL)
    assert raw_switch.is_valid and len(raw_switch.solids()) == 3
    assert abs(max(float(s.bounding_box().max.Z) for s in raw_switch.solids()) - SWITCH_HEIGHT) < 1e-6

    # Keeper latch final pose is clear of the lid before it carries any load.
    assert _volume(keeper.intersect(lid)) < 1e-7, "keeper is not assembleable at its snap pose"
    keeper_down = make_keeper().locate(Location((0.0, 0.0, -EPS)))
    assert _volume(keeper_down.intersect(lid)) > 1e-5, "keeper hooks do not restrain downward load"

    for x, y in BUTTON_CENTERS:
        rest = make_plunger().locate(Location((x, y, 0.0)))
        pressed = make_plunger().locate(Location((x, y, -NOMINAL_STROKE)))
        too_far_up = make_plunger().locate(Location((x, y, EPS)))
        too_far_down = make_plunger().locate(Location((x, y, -NOMINAL_STROKE - EPS)))
        placed_switch, body, actuator = _placed_switch(x, y)

        # Before the keeper is installed, an underside-loaded slider has a
        # clear axial corridor through the cavity and throat into its rest
        # position. These samples cover its flange entering the cavity.
        for insertion_offset in (-0.50, -0.30, -0.10, 0.0):
            inserting = make_plunger().locate(Location((x, y, insertion_offset)))
            assert _volume(inserting.intersect(lid)) < 1e-7, f"underside insertion blocked at {(x, y)}"

        # The normal rest and lower-stop poses have only face contact. A
        # 0.01 mm move beyond each stop must penetrate its real mating solid.
        assert _volume(rest.intersect(lid)) < 1e-7, f"rest lid interference at {(x, y)}"
        assert _volume(pressed.intersect(lid)) < 1e-7, f"pressed lid interference at {(x, y)}"
        assert _volume(pressed.intersect(keeper)) < 1e-7, f"lower stop is not zero-gap at {(x, y)}"
        assert _volume(too_far_up.intersect(lid)) > 1e-5, f"upper capture missing at {(x, y)}"
        assert _volume(too_far_down.intersect(keeper)) > 1e-5, f"lower stop missing at {(x, y)}"

        # Rest is light actuator contact, not a claimed air gap. At lower
        # stop only the moving actuator has the intentional static-envelope
        # intersection; the switch package/cover remains clear.
        assert sum(_volume(rest.intersect(s)) for s in placed_switch) < 1e-7
        assert sum(_volume(pressed.intersect(placed_switch[i])) for i in body) < 1e-7
        assert sum(_volume(pressed.intersect(placed_switch[i])) for i in actuator) > 1e-5
        print(f"button {(x, y)}: upper-capture=True lower-stop=True stroke={NOMINAL_STROKE:.2f} mm")

    # New parts remain in the front-left service area, clear of J1, J2, RF.
    assert -1.50 > RJ45_NOTCH_X1
    j2 = _box(J2_X - J2_HALF_X, J2_X + J2_HALF_X, J2_Y - J2_HALF_Y, J2_Y + J2_HALF_Y, KEEPER_BOTTOM_Z, 20.0)
    assert _volume(keeper.intersect(j2)) < 1e-7
    assert 19.50 < ANTENNA_X0
    print("optional captive-button geometry checks: PASS")


if __name__ == "__main__":
    main()
