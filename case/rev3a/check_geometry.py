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
