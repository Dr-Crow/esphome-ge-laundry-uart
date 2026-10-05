"""Screen a named cable at explicit supplied coordinates; no physical fit claim."""
import argparse
import hashlib
import json
import math
from pathlib import Path

import enclosure as case
from review_dimensions import USB_CANDIDATES

def intersection(a, b):
    x, y = a.bounding_box(), b.bounding_box()
    if not all(min(list(x.max)[i], list(y.max)[i])-max(list(x.min)[i], list(y.min)[i]) > 1e-6 for i in range(3)):
        return 0.0
    result = a.intersect(b)
    if result is None:
        return 0.0
    return abs(float(result.volume)) if hasattr(result, 'volume') else sum(abs(float(s.volume)) for s in result)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--module', required=True, choices=['c3', 'c6'])
    parser.add_argument('--antenna', required=True, choices=['internal', 'external'])
    parser.add_argument('--cable', choices=USB_CANDIDATES, default='startech_usb2cc2m')
    for name in ['stack', 'boot-height', 'reset-height', 'boot-stop', 'reset-stop', 'axis-y', 'axis-z']:
        parser.add_argument('--' + name, required=True, type=float)
    parser.add_argument('--shoulder-x', required=True, type=float, action='append', help='Repeat for a conditional coordinate sensitivity sweep')
    parser.add_argument('--datum-note', required=True, help='Describe whether coordinates are measured, manufacturer supplied or hypothetical')
    parser.add_argument('--clearance', type=float, default=.25, help='Chosen geometric reserve, not a manufacturer tolerance')
    parser.add_argument('--gap', type=float, default=.25)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if not all(math.isfinite(x) for x in [args.stack, args.boot_height, args.reset_height, args.boot_stop, args.reset_stop, args.axis_y, args.axis_z, args.clearance, args.gap, *args.shoulder_x]):
        parser.error('All geometric parameters must be finite')
    if min(args.boot_height, args.reset_height, args.boot_stop, args.reset_stop, args.gap) <= 0 or args.clearance < 0:
        parser.error('Positive switch/gap dimensions and nonnegative clearance required')
    heights = {m: dict(case.SW_HEIGHT[m]) for m in case.SW}
    stops = {m: dict(case.BUTTON_TRAVEL[m]) for m in case.SW}
    gaps = {m: dict(case.CONTACT_GAP[m]) for m in case.SW}
    heights[args.module] = {'BOOT': args.boot_height, 'RESET': args.reset_height}
    stops[args.module] = {'BOOT': args.boot_stop, 'RESET': args.reset_stop}
    gaps[args.module] = {'BOOT': args.gap, 'RESET': args.gap}
    case.configure(args.stack, 'per_assembly', 'per_assembly', heights, gaps, stops, 17.3 if args.module == 'c3' else 16.6)
    base, lid = case.base(), case.shell(args.module, args.antenna)
    profile = USB_CANDIDATES[args.cable]
    reserve, y, z = args.clearance, args.axis_y, args.axis_z
    half_y, half_z = profile['body_width_max_mm']/2, profile['body_height_max_mm']/2
    rows = []
    for x in args.shoulder_x:
        # Published maximum overmold; rectangular corners deliberately overfill
        # unmeasured rounding. The native metal shank/insertion is not modelled.
        body = case.B(x-reserve, x+profile['body_length_max_mm']+reserve,
                      y-half_y-reserve, y+half_y+reserve, z-half_z-reserve, z+half_z+reserve)
        hits = {'base_mm3': intersection(base, body), 'lid_mm3': intersection(lid, body)}
        rows.append({'shoulder_x_mm': x, 'overmold_intersections_mm3': hits,
                     'conditional_body_clear': max(hits.values()) < 1e-5})
    receipt = {'physical_qualification': False, 'parameters': {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
               'candidate': profile, 'source_sha256': {n: hashlib.sha256((case.ROOT/n).read_bytes()).hexdigest() for n in ['enclosure.py', 'interface_baseline.py', 'component_envelopes.py', 'current_carrier_bounds.json', 'review_dimensions.py', 'review_usb_corridor.py']},
               'results': rows, 'limits': ['Conditional rectangular overmold screen only; no insertion, metal-shank, finger, strain-relief bend, retention or printed-tolerance proof.',
                                         'Supplied axis and shoulder coordinates are not authenticated by this program.',
                                         'Switch heights/stops remain explicitly supplied review parameters; electrical make/overtravel are unverified.']}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2)+'\n')
    for row in rows:
        print('Shoulder X', row['shoulder_x_mm'], 'conditional overmold clear', row['conditional_body_clear'], row['overmold_intersections_mm3'])

if __name__ == '__main__':
    main()
