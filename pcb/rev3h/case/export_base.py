"""Rev 3H case base: the Rev 3G matching base plus the J7 / JP3 tail pockets.

Run with the build123d environment from this folder:  python export_base.py

Uses case/rev3c/analytical/enclosure.py (one source for every variant) with exactly the settings
pcb/rev3g/case/src/export_service.py used for matching-base: recessed-end envelope (original USB and
RJ45 styles), 11.0 mm stack, per-assembly reach. Writes parts/matching-base-rev3h.{step,stl} and
case-checks.json, which records the checks below so a rerun shows any drift:
  * the base with tail_pockets=False has Rev 3G's recorded volume (28171.03 mm3);
  * Rev 3G's matching-base.step minus this base is the pockets and nothing else, and this base
    minus Rev 3G's adds no material;
  * a vertical line down from the board bottom (z 3.65) under every J7 / JP3 pin finds >= 3.5 mm free.
"""
import json
import sys
from pathlib import Path

import build123d as b

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'case' / 'rev3c' / 'analytical'))
import enclosure as e  # noqa: E402

SEAT = e.e.PCB_SEAT_Z   # board bottom, 3.65
e.OUT = HERE / 'parts'
e.OUT.mkdir(exist_ok=True)
e.configure(stack_mm=11.0, reach_mode='per_assembly', usb_mode='per_assembly',
            usb_style='original', rj45_style='original')

record = {'settings': {'stack_mm': 11.0, 'reach_mode': 'per_assembly', 'usb_mode': 'per_assembly',
                       'usb_style': 'original', 'rj45_style': 'original', 'magnets': None,
                       'tail_pockets': True}}

# Same geometry without the pockets must be Rev 3G's matching base.
plain = e.base(tail_pockets=False)
record['without_pockets_volume_mm3'] = round(plain.volume, 3)
assert abs(plain.volume - 28171.03) < 0.05, plain.volume

base = e.base()
record['base'] = e.export(base, 'matching-base-rev3h')
record['pockets_mm'] = {n: {'x': [round(x0, 3), round(x1, 3)], 'y_kicad': [round(y0, 3), round(y1, 3)],
                            'bottom_z': round(e.TAIL_BOTTOM_Z, 3), 'floor_under_mm': round(e.TAIL_BOTTOM_Z + 1.0, 3)}
                        for n, x0, x1, y0, y1 in e.tail_pocket_boxes()}

# Difference against Rev 3G's matching base (exact solids).
g = b.import_step(ROOT / 'pcb' / 'rev3g' / 'case' / 'parts' / 'matching-base.step')
new = b.import_step(HERE / 'parts' / 'matching-base-rev3h.step')
removed = g - new
added = new - g
expected = 0.0
for n, x0, x1, y0, y1 in e.tail_pocket_boxes():
    expected += (g & e.B(x0, x1, 40 - y1, 40 - y0, e.TAIL_BOTTOM_Z, 2.45)).volume
record['difference_vs_rev3g'] = {
    'rev3g_volume_mm3': round(g.volume, 3), 'rev3h_volume_mm3': round(new.volume, 3),
    'removed_mm3': round(sum(s.volume for s in removed.solids()), 3),
    'expected_pocket_mm3': round(expected, 3),
    'added_mm3': round(sum(s.volume for s in added.solids()), 3) if added else 0.0}

# Free depth under each pin, physical frame (y = 40 - y_kicad), line from the board bottom to the base bottom.
free = {}
for name, pins in e.TAIL_PINS.items():
    out = []
    for x, y in pins:
        line = b.Edge.make_line((x, 40 - y, SEAT), (x, 40 - y, -1.0))
        hit = new.intersect(line)
        solid = sum(v.length for v in hit.edges()) if hit is not None else 0.0
        out.append(round((SEAT + 1.0) - solid, 3))
    free[name] = out
record['free_depth_under_board_mm'] = free
assert min(min(v) for v in free.values()) >= 3.5 - 1e-6, free
assert record['difference_vs_rev3g']['added_mm3'] < 1e-3
assert abs(record['difference_vs_rev3g']['removed_mm3'] - expected) < 0.01

(HERE / 'case-checks.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
