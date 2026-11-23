"""Export five explicitly parameterized review pieces, without a release claim."""
import argparse
import hashlib
import json
from pathlib import Path

import enclosure as case

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--module', required=True, choices=['c3', 'c6'])
parser.add_argument('--antenna', default='internal', choices=['internal', 'fpc', 'smooth', 'external'],
                    help="fpc: flat-antenna keeper rails; smooth: plain roof; external: SMA bulkhead; "
                         "internal: original pairing (C3 fpc, C6 smooth)")
parser.add_argument('--stack', required=True, type=float)
for name in ['boot-height', 'reset-height', 'boot-stop', 'reset-stop']:
    parser.add_argument('--' + name, required=True, type=float)
parser.add_argument('--gap', default=0.25, type=float)
parser.add_argument('--leaf-offset', default=16.6, type=float)
parser.add_argument('--relieved-guides', action='store_true')
parser.add_argument('--magnets', default='none', choices=['none', '6x2', '8x2', '10x2'],
                    help='four open-bottom pockets in the base for N52 disc magnets (diameter x thickness, mm)')
parser.add_argument('--usb-style', default='original', choices=['original', 'flush'],
                    help='flush: end wall at the USB-C port with a snug opening (adds a USB-end fit coupon)')
parser.add_argument('--output', required=True, type=Path)
args = parser.parse_args()
if min(args.boot_height, args.reset_height, args.boot_stop, args.reset_stop, args.gap) <= 0:
    parser.error('Switch heights, stops and release gap must be positive review dimensions')
heights = {module: dict(case.SW_HEIGHT[module]) for module in case.SW}
stops = {module: dict(case.BUTTON_TRAVEL[module]) for module in case.SW}
gaps = {module: dict(case.CONTACT_GAP[module]) for module in case.SW}
heights[args.module] = {'BOOT': args.boot_height, 'RESET': args.reset_height}
stops[args.module] = {'BOOT': args.boot_stop, 'RESET': args.reset_stop}
gaps[args.module] = {'BOOT': args.gap, 'RESET': args.gap}
case.configure(args.stack, 'per_assembly', 'per_assembly', heights, gaps, stops, args.leaf_offset, args.usb_style)
case.OUT = args.output.resolve()
case.OUT.mkdir(parents=True, exist_ok=True)
MAG = False if args.magnets == 'none' else args.magnets
pieces = {'review_base': case.base(MAG),
          f'review_lid_{args.module}_{args.antenna}': case.shell(args.module, args.antenna)}
for name, (bottom, roof) in case.PIPES.items():
    pieces['review_guide_' + name.lower()] = (case.pipe_with_cap_relief(name)
        if args.relieved_guides else case.pipe_shape(bottom, roof, 1.43))
coupons = {}
if args.usb_style == 'flush':
    # Short USB-end slice of both halves: print it, seat a real module + cable, and measure the mouth
    # recess and plug seating before printing a full case. Not an extra piece of the assembly.
    end = case.B(86., 110., -10., 50., -2., 40.)
    # Keep the largest solid: the cut can free a slice of a button leaf, which is not part of the USB fit test.
    biggest = lambda s: max(s.solids(), key=lambda p: p.volume)
    coupons = {'coupon_usb_end_base': biggest(case.base(MAG) & end),
               f'coupon_usb_end_lid_{args.module}': biggest(case.shell(args.module, args.antenna) & end)}
if args.antenna == 'fpc' or (args.antenna == 'internal' and args.module == 'c3'):
    # Reference body for the 40 x 20 mm flat antenna in its keeper (viewing and clearance only; do not print).
    coupons['proxy_fpc_antenna_40x20'] = case.B(*case.FPC_BOX)
receipt = {'qualification': 'Unqualified review geometry; no measured assembly or switch-travel proof',
           'parameters': {key: str(value) if isinstance(value, Path) else value
                          for key, value in vars(args).items()},
           'source_sha256': {name: hashlib.sha256((case.ROOT / name).read_bytes()).hexdigest()
                             for name in ['enclosure.py', 'interface_baseline.py',
                                          'component_envelopes.py', 'current_carrier_bounds.json']},
           'parts': {name: case.export(shape, name) for name, shape in pieces.items()},
           'coupons': {name: case.export(shape, name) for name, shape in coupons.items()}}
if args.usb_style == 'flush':
    z0, z1 = case.usb_port_z()
    receipt['usb_flush'] = {'face_x_kicad': round(case.usb_face_x(), 3), 'mouth_x_kicad': case.USB_MOUTH_X,
                            'recess_mm': case.USB_RECESS, 'plate_mm': case.USB_PLATE_T,
                            'opening_mm': [round(case.USB_SHELL_W + 2 * case.USB_CLEAR, 3), round(z1 - z0, 3)],
                            'opening_z': [round(z0, 3), round(z1, 3)],
                            'upper_step': [round(v, 3) for v in case.usb_step(args.module)],
                            'assumptions': 'Mouth x from the official module KiCad files; Type-C shell 8.94 x 3.26 top-mounted; '
                                           'module PCB 1.2-1.6 mm. Unmeasured: print the coupon first.'}
(case.OUT / 'REVIEW-PARAMETERS.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('Exported five review pieces. Switch, print, optical, RF and physical qualification remain open.')
