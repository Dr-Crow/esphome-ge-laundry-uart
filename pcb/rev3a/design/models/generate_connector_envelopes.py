"""Generate the simplified Rev3A connector models that lack vendor STEP files."""

from pathlib import Path

from build123d import Align, Box, Location, export_step


HERE = Path(__file__).resolve().parent


def box(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float):
    return Box(x1 - x0, y1 - y0, z1 - z0, align=(Align.MIN, Align.MIN, Align.MIN)).locate(
        Location((x0, y0, z0))
    )


def make_rj45():
    # The outer dimensions come from the EVERCOM 5301-8P8C drawing.  The
    # shallow front cavity is illustrative; the outer solid remains the
    # conservative envelope used for enclosure clearance.  STEP Y is mirrored
    # relative to KiCad's footprint-local Y for this imported model, so mirror
    # the drawing coordinates here.  That places the body over the two locating
    # posts and puts the opening at the PCB edge without changing J1 copper.
    outer = box(-3.205, 12.095, -13.97, 3.77, 0.0, 11.45)
    opening = box(-1.7, 10.6, -14.1, -12.9, 1.2, 9.8)
    return outer - opening


def main() -> None:
    target = HERE / "J1-EVERCOM-5301-8P8C-envelope.step"
    export_step(make_rj45(), target)
    print(f"wrote {target}")


if __name__ == "__main__":
    main()
