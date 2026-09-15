"""Small regression checks for the Rev3A enclosure deliverables."""

from __future__ import annotations

import argparse
from pathlib import Path

import trimesh
from build123d import import_step

from enclosure import (
    ANTENNA_X0,
    ANTENNA_X1,
    ANTENNA_Y0,
    ANTENNA_Y1,
    BASE_X0,
    BASE_X1,
    BASE_Y0,
    BASE_Y1,
    PCB_X,
    PCB_Y,
    LED_VIEW_HOLES,
    LED_VIEW_RADIUS,
    LID_CEILING,
    LID_Z1,
    LID_UNDERSIDE_Z,
    RJ45_ENVELOPE_TOP_Z,
    RJ45_WINDOW_Y0,
    RJ45_WINDOW_Y1,
    RJ45_WINDOW_Z0,
    RJ45_WINDOW_Z1,
    RJ45_NOTCH_X0,
    RJ45_NOTCH_X1,
    RJ45_NOTCH_Y0,
    RJ45_NOTCH_Y1,
    RJ45_NOTCH_Z0,
    RJ45_NOTCH_Z1,
    LOCATING_POST_RADIUS,
    LID_RETAINER_OUTER_RADIUS,
    LID_RETAINER_INNER_RADIUS,
    _box,
    _cylinder,
    make_base,
    make_lid,
)


def _bounds(shape):
    box = shape.bounding_box()
    return tuple(float(v) for v in (*box.min, *box.max))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()

    base = make_base()
    lid = make_lid()
    bx = _bounds(base)
    lx = _bounds(lid)
    assert bx[0] <= BASE_X0 + 1e-6 and bx[3] >= BASE_X1 - 1e-6
    assert bx[1] <= BASE_Y0 + 1e-6 and bx[4] >= BASE_Y1 - 1e-6
    assert lx[0] < bx[0] and lx[3] > bx[3], (lx, bx)
    assert PCB_X + 15.0 == ANTENNA_X1
    assert ANTENNA_X0 >= PCB_X and ANTENNA_Y0 >= 0 and ANTENNA_Y1 <= PCB_Y
    assert LID_UNDERSIDE_Z - RJ45_ENVELOPE_TOP_Z >= 1.0
    assert RJ45_WINDOW_Y1 - RJ45_WINDOW_Y0 >= 18.0
    assert RJ45_WINDOW_Z1 - RJ45_WINDOW_Z0 >= 8.0
    assert RJ45_NOTCH_Y0 < RJ45_WINDOW_Y0 and RJ45_NOTCH_Y1 > RJ45_WINDOW_Y1
    assert RJ45_NOTCH_Z0 <= 9.0 and RJ45_NOTCH_Z1 >= RJ45_ENVELOPE_TOP_Z + 0.99
    insertion = _box(
        RJ45_NOTCH_X0,
        RJ45_NOTCH_X1,
        RJ45_NOTCH_Y0,
        RJ45_NOTCH_Y1,
        RJ45_NOTCH_Z0,
        RJ45_NOTCH_Z1,
    )
    overlap = lid.intersect(insertion)
    assert overlap is None or overlap.volume < 1e-6, "lid blocks RJ45 insertion envelope"
    assert LOCATING_POST_RADIUS < 1.6
    assert LID_RETAINER_INNER_RADIUS < 1.6 < LID_RETAINER_OUTER_RADIUS
    for x, y in LED_VIEW_HOLES:
        viewing_hole = _cylinder(
            LED_VIEW_RADIUS,
            LID_Z1 - LID_CEILING - 0.1,
            LID_Z1 + 0.1,
            x,
            y,
        )
        blocked = lid.intersect(viewing_hole)
        assert blocked is None or blocked.volume < 1e-6, f"lid blocks LED view at {(x, y)}"
    print(f"RJ45 envelope: top_z={RJ45_ENVELOPE_TOP_Z:.2f} lid_underside={LID_UNDERSIDE_Z:.2f} clearance={LID_UNDERSIDE_Z - RJ45_ENVELOPE_TOP_Z:.2f} mm")
    print(f"RJ45 window: y={RJ45_WINDOW_Y0}..{RJ45_WINDOW_Y1} z={RJ45_WINDOW_Z0}..{RJ45_WINDOW_Z1} mm")

    for name in ("rev3a_base", "rev3a_lid"):
        # STL stores each triangle's vertices independently by design;
        # process=True welds coincident vertices before topology checks.
        mesh = trimesh.load_mesh(args.dir / f"{name}.stl", process=True)
        assert isinstance(mesh, trimesh.Trimesh), name
        assert mesh.is_watertight, f"{name} STL is not watertight"
        assert mesh.is_volume, f"{name} STL is not a volume"
        print(f"{name}: watertight={mesh.is_watertight} manifold={mesh.is_watertight} bounds={mesh.bounds.tolist()}")
        step_shape = import_step(args.dir / f"{name}.step")
        assert step_shape.is_valid, f"{name} STEP failed build123d validity"
        assert len(step_shape.solids()) >= 1, f"{name} STEP has no solid"
        print(f"{name}: STEP import valid=True solids={len(step_shape.solids())}")
    print("geometry checks: PASS")


if __name__ == "__main__":
    main()
