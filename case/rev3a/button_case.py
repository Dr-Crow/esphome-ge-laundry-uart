"""Optional captive finger-button lid for the Rev3A enclosure.

This is deliberately an alternate assembly: the original tool-access lid is
not modified. Each button is a one-piece slider loaded from the underside of
the lid. A shared keeper then snaps into the underside of the lid. The
slider's wide flange is caught between the lid's upper throat and the keeper,
so it has positive stops in both axial directions without a printed spring.

The XKB switch's own return spring raises the slider to its upper stop. The
model is a prototype-fit aid only: the data sheet gives no over-travel limit.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from build123d import Part, export_step, export_stl

from enclosure import LID_UNDERSIDE_Z, LID_Z1, PCB_TOP_Z, _box, _cylinder, make_lid


SWITCH_MODEL = Path(__file__).parents[2] / "pcb/rev3a/design/models/SW1-SW2-XKB-TS-1187A-B-A-B.step"
BUTTON_CENTERS = ((5.0, 3.4), (13.0, 3.4))
BUTTON_SPACING = 8.0

# C318884 geometry measured from the seated PCB datum used by enclosure.py.
SWITCH_HEIGHT = 1.5
SWITCH_TOP_Z = PCB_TOP_Z + SWITCH_HEIGHT
ACTUATOR_RADIUS = 1.0

# This is the actual axial motion from the flange's upper-throat stop to its
# keeper stop. It begins with the tip just touching the switch actuator; the
# switch return spring supplies return force. A physical release/continuity
# test is mandatory because the data sheet does not state a safe over-travel
# or crush-force limit.
NOMINAL_STROKE = 0.20
REST_TIP_Z = SWITCH_TOP_Z
FULL_PRESS_TIP_Z = REST_TIP_Z - NOMINAL_STROKE

# Lid guide. The original 4 mm tool hole is enlarged only in this optional
# lid. The 4.3 mm finger pad passes the 4.7 mm throat during underside
# insertion. The 5.4 mm flange cannot pass it once installed.
GUIDE_OUTER_RADIUS = 3.70
THROAT_RADIUS = 2.35
FLANGE_RADIUS = 2.70
FLANGE_CLEAR_RADIUS = 2.82
SLIDER_RADIUS = 0.80
PAD_RADIUS = 2.15
FLANGE_HEIGHT = 0.80
KEEPER_HOLE_RADIUS = 1.05
RADIAL_CLEARANCE = FLANGE_CLEAR_RADIUS - FLANGE_RADIUS

# At rest the flange top touches the upper throat. At full press its bottom
# touches the keeper top. These faces, not an arbitrary translated pose, set
# the 0.20 mm nominal stroke.
UPPER_THROAT_BOTTOM_Z = 16.00
FLANGE_REST_TOP_Z = UPPER_THROAT_BOTTOM_Z
FLANGE_REST_BOTTOM_Z = FLANGE_REST_TOP_Z - FLANGE_HEIGHT
KEEPER_TOP_Z = FLANGE_REST_BOTTOM_Z - NOMINAL_STROKE
KEEPER_BOTTOM_Z = 13.60
GUIDE_CAVITY_BOTTOM_Z = KEEPER_TOP_Z
GUIDE_CAVITY_TOP_Z = UPPER_THROAT_BOTTOM_Z
GUIDE_TOP_Z = LID_UNDERSIDE_Z + 0.10

# The shared keeper is fitted from below after both sliders. Its side latches
# hook over the *top* faces of the lid-side rails. The keeper plate is 1.4 mm
# thick; each arm is an 0.80 mm X-thickness cantilever after its 0.05 mm union
# overlap. PETG/ABS prototype fitting verifies the one-time retention fit.
KEEPER_X0, KEEPER_X1 = -1.50, 19.50
KEEPER_Y0, KEEPER_Y1 = 0.40, 6.40
LATCH_WEB = 0.75
# The arm flexes in its 0.80 mm actual X thickness. Its free length from the
# keeper top to the hook underside is 3.50 mm; the rail engagement is 0.10 mm.
# Gently spread both arms outward while fitting the keeper--this is not a
# push-through snap-force claim.
LATCH_RISE = 4.30
LATCH_HOOK = 0.90
RAIL_Z0, RAIL_Z1 = KEEPER_TOP_Z + 2.30, KEEPER_TOP_Z + 3.50


def _annulus(outer: float, inner: float, z0: float, z1: float, x: float, y: float) -> Part:
    return _cylinder(outer, z0, z1, x, y) - _cylinder(inner, z0 - 0.05, z1 + 0.05, x, y)


def make_button_lid() -> Part:
    """Return the optional lid with two flange cavities and keeper rails."""
    lid = make_lid()
    for x, y in BUTTON_CENTERS:
        # Widen only this variant's original r=2.0 service hole so the
        # underside-loaded 4.3 mm pad can traverse the 4.7 mm throat.
        lid = lid - _cylinder(THROAT_RADIUS, LID_UNDERSIDE_Z - 0.10, LID_Z1 + 0.10, x, y)
        # The guide overlaps the existing ceiling at z=19.4..19.5, making a
        # single lid solid while keeping the existing service-hole location.
        throat = _annulus(GUIDE_OUTER_RADIUS, THROAT_RADIUS, UPPER_THROAT_BOTTOM_Z, GUIDE_TOP_Z, x, y)
        cavity_wall = _annulus(
            GUIDE_OUTER_RADIUS, FLANGE_CLEAR_RADIUS, GUIDE_CAVITY_BOTTOM_Z, GUIDE_CAVITY_TOP_Z, x, y
        )
        lid = lid + throat + cavity_wall
    # The keeper's latches flex in X while it is pushed upward. The rails are
    # outside both guide envelopes and remain clear of the RJ45 opening.
    for x0, x1 in ((-1.35, -0.15), (18.15, 19.35)):
        rail = _box(x0, x1, KEEPER_Y0, KEEPER_Y1, RAIL_Z0, RAIL_Z1)
        # A rear brace joins each short latch rail to the original ceiling;
        # it is deliberately outside the two guide envelopes.
        brace = _box(x0, x1, KEEPER_Y0, KEEPER_Y0 + 1.20, RAIL_Z1 - 0.05, GUIDE_TOP_Z)
        lid = lid + rail + brace
    return lid


def make_plunger() -> Part:
    """Return one underside-loaded slider; print two identical copies."""
    stem = _cylinder(SLIDER_RADIUS, REST_TIP_Z, FLANGE_REST_BOTTOM_Z, 0.0, 0.0)
    lead_in = _cylinder(FLANGE_RADIUS - 0.40, FLANGE_REST_BOTTOM_Z, FLANGE_REST_BOTTOM_Z + 0.40, 0.0, 0.0)
    flange = _cylinder(FLANGE_RADIUS, FLANGE_REST_BOTTOM_Z + 0.40, FLANGE_REST_TOP_Z, 0.0, 0.0)
    pad = _cylinder(PAD_RADIUS, FLANGE_REST_TOP_Z, LID_Z1 + 0.70, 0.0, 0.0)
    return stem + lead_in + flange + pad


def make_keeper() -> Part:
    """Return the common two-button lower stop and snap-retained keeper."""
    keeper = _box(KEEPER_X0, KEEPER_X1, KEEPER_Y0, KEEPER_Y1, KEEPER_BOTTOM_Z, KEEPER_TOP_Z)
    for x, y in BUTTON_CENTERS:
        keeper = keeper - _cylinder(KEEPER_HOLE_RADIUS, KEEPER_BOTTOM_Z - 0.05, KEEPER_TOP_Z + 0.05, x, y)
    # Side latches sit outside the guide envelopes. Their inward hook noses
    # finish above the rail tops and restrain keeper downward motion.
    left_arm = _box(KEEPER_X0 - LATCH_WEB, KEEPER_X0 + 0.05, KEEPER_Y0, KEEPER_Y1, KEEPER_BOTTOM_Z, KEEPER_TOP_Z + LATCH_RISE)
    left_hook = _box(KEEPER_X0 - 0.55, KEEPER_X0 + 0.25, KEEPER_Y0 + 1.20, KEEPER_Y1 - 1.20, RAIL_Z1, RAIL_Z1 + 0.80)
    right_arm = _box(KEEPER_X1 - 0.05, KEEPER_X1 + LATCH_WEB, KEEPER_Y0, KEEPER_Y1, KEEPER_BOTTOM_Z, KEEPER_TOP_Z + LATCH_RISE)
    right_hook = _box(KEEPER_X1 - 0.25, KEEPER_X1 + 0.55, KEEPER_Y0 + 1.20, KEEPER_Y1 - 1.20, RAIL_Z1, RAIL_Z1 + 0.80)
    return keeper + left_arm + left_hook + right_arm + right_hook


def _export(shape: Part, stem: str, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    export_stl(shape, out_dir / f"{stem}.stl")
    export_step(shape, out_dir / f"{stem}.step")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    _export(make_button_lid(), "rev3a_button_lid", args.out)
    _export(make_plunger(), "rev3a_button_plunger", args.out)
    _export(make_keeper(), "rev3a_button_keeper", args.out)
    print(f"wrote optional button lid, two plungers, and shared keeper to {args.out}")


if __name__ == "__main__":
    main()
