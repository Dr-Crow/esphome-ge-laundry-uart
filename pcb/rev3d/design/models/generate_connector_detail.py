"""Drawing-derived connector fallback models, not manufacturer-supplied CAD.

Dimensioned outer geometry, pin pitch and tails follow the cited drawings.
Undimensioned cavities/contact details are illustrative and excluded from fit proof.
Copyright 2026 Dr-Crow. Licensed under the repository MIT license.
"""
from pathlib import Path
from build123d import Align, Box, Cylinder, Color, Compound, Location, export_step

HERE = Path(__file__).resolve().parent
BLACK = Color(0.055, 0.055, 0.065)
METAL = Color(0.72, 0.73, 0.75)
GOLD = Color(0.70, 0.52, 0.16)


def box(x0, x1, y0, y1, z0, z1):
    return Box(x1-x0, y1-y0, z1-z0,
               align=(Align.MIN, Align.MIN, Align.MIN)).locate(Location((x0, y0, z0)))


def socket():
    # HCTL official Rev A PM254-1-N-Z-8.5-XX drawing, N=7:
    # length = 2.54*N+0.40, width 2.50, body height 8.50;
    # 0.64 x 0.40 tails, 3.20 below body. Origin = footprint pad 1.
    body = box(-16.71, 1.47, -1.25, 1.25, 0, 8.5)
    for n in range(7):
        x = -2.54*n
        # Square receiving openings are shown, but their dimensions are not
        # specified. These 0.9mm mouths and 0.25mm recesses are illustrative.
        body -= box(x-.45, x+.45, -.45, .45, 6.7, 8.51)
        body -= box(x-.70, x+.70, -.70, .70, 8.25, 8.51)
    body.color = BLACK
    body.label = 'HCTL PM254 drawing body; illustrative receiving recesses'
    parts = [body]
    for n in range(7):
        tail = box(-2.54*n-.32, -2.54*n+.32, -.20, .20, -3.2, 0)
        tail.color = METAL
        tail.label = f'PM254 nominal tail {n+1}'
        parts.append(tail)
    return Compound(children=parts)


def rj45():
    # EVERCOM official Rev A 2025-09-23 drawing 5301-880XXX:
    # 15.20 width, 18.05 depth, 11.45 height, tails 3.0,
    # round signal contacts diameter 0.46, recommended locating holes 3.20.
    # Pad1 is (0,0); STEP Y mirrors footprint Y. Front opens toward -Y.
    # Contact row1 to peg = 6.35; peg to front = 8.00 -> front -14.35.
    body = box(-3.155, 12.045, -14.35, 3.70, 0, 11.45)
    # Opening/internal wall dimensions are not dimensioned in the drawing.
    # They depict the recognizable connector structure only.
    body -= box(-2.05, 10.94, -14.36, -1.8, 1.1, 10.15)
    body -= box(2.34, 6.55, -14.36, -11.0, 0, 1.1)
    body.color = BLACK
    body.label = 'EVERCOM Rev A drawing body; illustrative internal opening'
    parts = [body]
    for n in range(8):
        x, y = 1.27*n, (0 if n%2==0 else 2.54)
        tail = Cylinder(.23, 3.0, align=(Align.CENTER, Align.CENTER, Align.MIN)).locate(Location((x,y,-3)))
        tail.color = METAL
        tail.label = f'5301 nominal contact tail {n+1}'
        parts.append(tail)
        # Front contact pitch/positions and bending are illustrative; no mating
        # depth or spring profile is asserted by this visual representation.
        spring = box(.875+1.02*n-.11, .875+1.02*n+.11, -13.4, -2.0, 8.75, 8.98)
        spring.color = GOLD
        spring.label = f'5301 illustrative front contact {n+1}'
        parts.append(spring)
    # Locating-post barbs/profile are not fully dimensioned. The recommended
    # drill3.20 is not the true barb diameter, and no insertion depth is known.
    # Omit those solids rather than turn a hole size into a fictitious post.
    # Drawing post centers would be(-1.305,-6.35),(10.195,-6.35), spacing11.50;
    # unchanged source footprint spacing11.43 differs by0.07mm total.
    return Compound(children=parts)


if __name__ == '__main__':
    for filename, model in [
        ('Socket_HCTL_PM254-1-07-Z-8.5-drawing-detail.step', socket()),
        ('RJ45_EVERCOM_5301-8P8C-RevA-drawing-detail.step', rj45()),
    ]:
        export_step(model, HERE / filename)
        b = model.bounding_box()
        print(filename, 'bounds_mm', tuple(b.min), tuple(b.max))
