"""Export five explicitly parameterized review pieces, without a release claim."""
import argparse
import hashlib
import json
from pathlib import Path

import enclosure as case

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--module', required=True, choices=['c3', 'c6'])
parser.add_argument('--antenna', default='internal', choices=['internal', 'external'])
parser.add_argument('--stack', required=True, type=float)
for name in ['boot-height', 'reset-height', 'boot-stop', 'reset-stop']:
    parser.add_argument('--' + name, required=True, type=float)
parser.add_argument('--gap', default=0.25, type=float)
parser.add_argument('--leaf-offset', default=16.6, type=float)
parser.add_argument('--relieved-guides', action='store_true')
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
case.configure(args.stack, 'per_assembly', 'per_assembly', heights, gaps, stops, args.leaf_offset)
case.OUT = args.output.resolve()
case.OUT.mkdir(parents=True, exist_ok=True)
pieces = {'review_base': case.base(),
          f'review_lid_{args.module}_{args.antenna}': case.shell(args.module, args.antenna)}
for name, (bottom, roof) in case.PIPES.items():
    pieces['review_guide_' + name.lower()] = (case.pipe_with_cap_relief(name)
        if args.relieved_guides else case.pipe_shape(bottom, roof, 1.43))
receipt = {'qualification': 'Unqualified review geometry; no measured assembly or switch-travel proof',
           'parameters': {key: str(value) if isinstance(value, Path) else value
                          for key, value in vars(args).items()},
           'source_sha256': {name: hashlib.sha256((case.ROOT / name).read_bytes()).hexdigest()
                             for name in ['enclosure.py', 'interface_baseline.py',
                                          'component_envelopes.py', 'current_carrier_bounds.json']},
           'parts': {name: case.export(shape, name) for name, shape in pieces.items()}}
(case.OUT / 'REVIEW-PARAMETERS.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('Exported five review pieces. Switch, print, optical, RF and physical qualification remain open.')
