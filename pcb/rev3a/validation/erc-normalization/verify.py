#!/usr/bin/env python3
"""Verify this isolated schematic cleanup against its exact input commit.

Run from any directory with Python 3. This reads committed source and native
exports; it does not replace ERC/DRC. Regenerate reports using README commands.
"""
from pathlib import Path
from decimal import Decimal as D
from collections import Counter
import copy
import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET
from schematic_parser import Node, parse, value

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = '60ccb434ea4bb9c9e0cde7bbac36a15220b23a0e'
SCH = 'pcb/rev3a/design/GEA-Adapter-Rev3A.kicad_sch'
LIB = 'pcb/rev3a/design/symbols/LegacySymbols.kicad_sym'
EDITABLE = {SCH, LIB, 'pcb/rev3a/design/symbols/source-map.json',
            'pcb/rev3a/README.md', 'pcb/rev3a/STANDALONE-REVIEW.md'}


def git_bytes(path):
    return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def memberships(tree):
    return sorted((node.attrib['ref'], node.attrib['pin'], net.attrib['name'],
                   node.attrib.get('pinfunction', ''), node.attrib.get('pintype', ''))
                  for net in tree.findall('./nets/net') for node in net.findall('node'))


def by_uuid(nodes):
    return {node.one('uuid').items[1]: node for node in nodes}


before, after = [ET.parse(HERE / f'{stage}.net.xml') for stage in ('before', 'after')]
old, new = memberships(before), memberships(after)
assert len(old) == len(new) == len({x[:2] for x in new}) == 301
assert old == new
for field in ('components', 'libparts', 'libraries'):
    assert ET.tostring(before.find(field)) == ET.tostring(after.find(field)), field
assert [(n.attrib['code'], n.attrib['name']) for n in before.findall('./nets/net')] == [
    (n.attrib['code'], n.attrib['name']) for n in after.findall('./nets/net')]
negative = copy.deepcopy(new)
i = next(i for i, row in enumerate(negative) if row[:2] == ('U4', '5'))
negative[i] = (*negative[i][:2], '+3V3', *negative[i][3:])
assert negative != old
assert set(old) - set(negative) == {('U4', '5', '+5V', 'VCC', 'power_in')}
assert set(negative) - set(old) == {('U4', '5', '+3V3', 'VCC', 'power_in')}

hashes = json.loads((HERE / 'before-tracked-sha256.json').read_text())
changed = []
for name, expected in hashes.items():
    assert sha(git_bytes(name)) == expected, name
    if sha((ROOT / name).read_bytes()) != expected:
        changed.append(name)
assert set(changed) == EDITABLE, changed

original = parse(git_bytes(SCH).decode())
current = parse((ROOT / SCH).read_text())
orig_lib = original.one('lib_symbols')
now_lib = current.one('lib_symbols')
assert len(orig_lib.all('symbol')) == len(now_lib.all('symbol'))
for a, b in zip(orig_lib.all('symbol'), now_lib.all('symbol')):
    if a.items[1] != 'LegacySymbols:74LVC2G07':
        assert value(a) == value(b), a.items[1]
    else:
        av, bv = value(a), value(b)
        common = next(x for x in av if isinstance(x, list) and x[:2] == ['symbol', '74LVC2G07_0_1'])
        pin = next(x for x in common if isinstance(x, list) and x[:1] == ['pin'] and any(z[:2] == ['number', '5'] for z in x if isinstance(z, list)))
        pin.remove(['hide', 'yes'])
        assert av == bv
        assert ['at', '0', '2.54', '90'] in pin and ['length', '0'] in pin
        assert pin[:3] == ['pin', 'power_in', 'line']
        assert any(x[:2] == ['name', 'VCC'] for x in pin if isinstance(x, list))

old_local = parse(git_bytes(LIB).decode())
new_local = parse((ROOT / LIB).read_text())
for a, b in zip(old_local.all('symbol'), new_local.all('symbol')):
    av, bv = value(a), value(b)
    if a.items[1] == '74LVC2G07':
        common = next(x for x in av if isinstance(x, list) and x[:2] == ['symbol', '74LVC2G07_0_1'])
        pin = next(x for x in common if isinstance(x, list) and x[:1] == ['pin'] and any(z[:2] == ['number', '5'] for z in x if isinstance(z, list)))
        pin.remove(['hide', 'yes'])
    assert av == bv, a.items[1]
# Cached and local modified definition agree, including its original GND hide flag.
embedded = copy.deepcopy(value(next(x for x in now_lib.all('symbol') if x.items[1] == 'LegacySymbols:74LVC2G07')))
embedded[1] = '74LVC2G07'
assert embedded == value(next(x for x in new_local.all('symbol') if x.items[1] == '74LVC2G07'))

remap = json.loads((HERE / 'coordinate-remap.json').read_text())
assert len(remap['symbols']) == 8
assert Counter(x['type'] for x in remap['attachments']) == {'label': 27, 'no_connect': 2}
for move in remap['symbols']:
    for pin in move['pins']:
        assert all(D(v) % D('0.635') == 0 for v in pin['new'])
old_symbols, new_symbols = map(by_uuid, (original.all('symbol'), current.all('symbol')))
assert set(old_symbols) == set(new_symbols)
for uuid, node in old_symbols.items():
    assert node.one('at').v()[2:] == new_symbols[uuid].one('at').v()[2:], uuid
    assert value(node.one('lib_id')) == value(new_symbols[uuid].one('lib_id')), uuid
old_wires, new_wires = map(by_uuid, (original.all('wire'), current.all('wire')))
assert set(old_wires) <= set(new_wires)
assert len(set(new_wires) - set(old_wires)) == 2
for uuid in old_wires:
    assert value(old_wires[uuid]) == value(new_wires[uuid]), uuid
for kind in ('junction', 'global_label', 'hierarchical_label'):
    assert [value(x) for x in original.all(kind)] == [value(x) for x in current.all(kind)], kind
for kind in ('label', 'no_connect'):
    a, b = map(by_uuid, (original.all(kind), current.all(kind)))
    assert set(a) == set(b)
    expected_moves = {x['uuid']: x for x in remap['attachments'] if x['type'] == kind}
    for uuid in a:
        av, bv = value(a[uuid]), value(b[uuid])
        if uuid in expected_moves:
            at = next(x for x in av if isinstance(x, list) and x[:1] == ['at'])
            assert at[1:3] == expected_moves[uuid]['old']
            at[1:3] = expected_moves[uuid]['new']
        assert av == bv, (kind, uuid)

for report in ('after-erc.json', 'after-drc.json', 'after-drc-standard.json'):
    data = json.loads((HERE / report).read_text())
    assert data['kicad_version'] == '9.0.9'
    assert set(data['included_severities']) == {'error', 'warning', 'exclusion'}
    if 'sheets' in data:
        assert not [v for s in data['sheets'] for v in s['violations']]
    else:
        assert not data['violations'] and not data['unconnected_items'] and not data['schematic_parity']
print(json.dumps({'result': 'pass', 'base_commit': BASE, 'pin_memberships': 301,
                  'nets': 72, 'negative_delta_detected': True,
                  'preserved_tracked_files': len(hashes) - len(changed),
                  'changed_existing_paths': sorted(changed),
                  'USB_markers_remapped': 29, 'new_U4_VCC_wires': 2}, indent=2))
