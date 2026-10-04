"""Verify the Rev3B visual lane against its exact selected electrical source.

Run with native KiCad 9.0.9 Python, --primary-source-pcb pointing to the
unmodified Seeed v1.3 PCB, and --stock-model-root pointing to KiCad 9.0.9 models.
No source board is saved, refilled, or exported by this verifier.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import pcbnew

BASE = '1db7a80f38a05c0c85023c01df63db22d81281c4'
ROOT = Path(__file__).resolve().parents[3]
REV = ROOT / 'pcb/rev3b'
PCB = 'pcb/rev3b/design/GEA-Adapter-Rev3B.kicad_pcb'
SOURCE_SHA = 'a761393935ff261a58fee3e3d7ecfb65152eaba8620de64ff7758fb0c043d1db'
STEP_SHA = '8ba2b9fd52c2a292f9fb0f3c2214738c83b830287490eef49d0962ddfbd56c80'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def non_model_tokens(data):
    text = data.decode()
    stack, cuts = [], []
    pattern = r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+'
    for match in re.finditer(pattern, text):
        token = match.group()
        if token == '(':
            stack.append([match.start(), None])
        elif token == ')':
            start, name = stack.pop()
            if name == 'model':
                cuts.append((start, match.end()))
        elif stack and stack[-1][1] is None:
            stack[-1][1] = token
    assert not stack
    for start, end in reversed(cuts):
        text = text[:start] + text[end:]
    return json.dumps(re.findall(pattern, text), ensure_ascii=False,
                      separators=(',', ':')).encode()


def baseline(path):
    return subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{BASE}:{path}'])


def xy(point):
    return [round(pcbnew.ToMM(point.x), 7), round(pcbnew.ToMM(point.y), 7)]


def vec(value):
    return [value.x, value.y, value.z]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--primary-source-pcb', type=Path, required=True)
    parser.add_argument('--stock-model-root', type=Path, required=True)
    args = parser.parse_args()
    assert pcbnew.Version() == '9.0.9'
    source_bytes = args.primary_source_pcb.read_bytes()
    assert sha(source_bytes) == SOURCE_SHA
    before, after = baseline(PCB), (ROOT/PCB).read_bytes()
    token_before, token_after = non_model_tokens(before), non_model_tokens(after)
    assert token_before == token_after, 'A non-model PCB token changed'
    files = subprocess.check_output(['git', '-C', str(ROOT), 'ls-tree', '-r',
                                     '--name-only', BASE]).decode().splitlines()
    protected = [p for p in files if (
        p.startswith(('firmware/', 'case/')) or '/manufacturing/' in p or
        p.endswith(('.kicad_sch', '.kicad_sym', '.kicad_mod', '.kicad_pro', '.kicad_dru')) or
        ('/design/' in p and p.endswith('.kicad_pcb') and p != PCB) or
        p.rsplit('/', 1)[-1] in ('fp-lib-table', 'sym-lib-table'))]
    protected_rows = []
    for path in protected:
        current = (ROOT/path).read_bytes()
        assert current == baseline(path), path
        protected_rows.append({'path': path, 'sha256': sha(current),
                               'matches_selected_baseline': True})

    board = pcbnew.LoadBoard(str(ROOT/PCB))
    u2 = next(f for f in board.GetFootprints() if f.GetReference() == 'U2')
    assert xy(u2.GetPosition()) == [77.39, 4.0]
    assert u2.GetOrientationDegrees() == -90
    installed = list(u2.Models())
    assert len(installed) == 1
    model = installed[0]
    assert model.m_Filename == '${KIPRJMOD}/models/XIAO_ESP32C3_v1.3_vendor_pcb_visual_reference.step'
    assert vec(model.m_Offset) == [8.9175, 10.5, 0.0]
    assert vec(model.m_Rotation) == [0.0, 0.0, -90.0]
    assert vec(model.m_Scale) == [1.0, 1.0, 1.0]
    source = pcbnew.LoadBoard(str(args.primary_source_pcb))
    rows = []
    carrier_pads = {p.GetNumber(): xy(p.GetPosition()) for p in u2.Pads()}
    for footprint in source.GetFootprints():
        if footprint.GetReference() not in ('J1', 'J2'):
            continue
        for pad in footprint.Pads():
            if pad.GetNumber() not in [str(i) for i in range(1, 8)]:
                continue
            number = int(pad.GetNumber()) + (7 if footprint.GetReference() == 'J1' else 0)
            native = xy(pad.GetPosition())
            step = [round(native[0]-148.4376, 7), round(105.0036-native[1], 7)]
            carrier = [round(87.89+step[0], 7), round(12.9175-step[1], 7)]
            land = carrier_pads[str(number)]
            delta = [round(carrier[i]-land[i], 7) for i in range(2)]
            assert delta == [0.0, 0.4625 if number <= 7 else -0.4625]
            rows.append({'pin': number, 'source_reference': footprint.GetReference(),
                         'source_pad': pad.GetNumber(), 'source_net': pad.GetNetname(),
                         'source_xy_mm': native, 'step_xy_mm': step,
                         'registered_drill_xy_carrier_mm': carrier,
                         'unchanged_carrier_land_xy_mm': land,
                         'drill_minus_land_xy_mm': delta})
    assert len(rows) == 14
    usb = next(f for f in source.GetFootprints() if f.GetReference() == 'USB0')
    usb_xy = xy(usb.GetPosition())
    registered_usb = [round(usb_xy[0]-60.5476, 7), round(usb_xy[1]-92.0861, 7)]
    assert registered_usb == [92.589, 12.9175]
    resolutions = []
    for footprint in board.GetFootprints():
        for item in footprint.Models():
            resolved = item.m_Filename.replace('${KIPRJMOD}', str(REV/'design'))
            resolved = resolved.replace('${KICAD9_3DMODEL_DIR}', str(args.stock_model_root))
            data = Path(resolved).read_bytes()
            resolutions.append({'reference': footprint.GetReference(), 'path': item.m_Filename,
                                'sha256': sha(data), 'bytes': len(data),
                                'scale': vec(item.m_Scale), 'resolved': True})
    assert len(resolutions) == sum(len(list(f.Models())) for f in board.GetFootprints())
    assert all(r['scale'] == [1.0, 1.0, 1.0] for r in resolutions)
    assets = []
    for path in [REV/'design/models/XIAO_ESP32C3_v1.3_vendor_pcb_visual_reference.step',
                 REV/'design/models/XIAO-ASSET-LICENSE.md',
                 REV/'design/models/KICAD-LIBRARY-LICENSE.md',
                 REV/'design/models/xiao-packages/QFN-32-1EP_5x5mm_P0.5mm_EP3.7x3.7mm.step',
                 REV/'validation/xiao-c3-model-source.json',
                 REV/'validation/xiao-soc-package-source.json']:
        assets.append({'path': str(path.relative_to(ROOT)), 'sha256': sha(path.read_bytes()),
                       'bytes': path.stat().st_size})
    assert assets[0]['sha256'] == STEP_SHA
    receipt = {
        'selected_baseline_commit': BASE, 'native_kicad_version': pcbnew.Version(),
        'scope': 'Only U2 placed 3D association and visual assets/docs/receipts/renders changed; no manufacturing export regeneration.',
        'pcb_before_sha256': sha(before), 'pcb_after_sha256': sha(after),
        'pcb_non_model_tokens_before_sha256': sha(token_before),
        'pcb_non_model_tokens_after_sha256': sha(token_after),
        'all_non_model_pcb_tokens_identical': True,
        'protected_files': protected_rows, 'all_protected_files_byte_identical': True,
        'source_pcb_sha256': SOURCE_SHA,
        'primary_source_url': 'https://files.seeedstudio.com/wiki/XIAO_WiFi/Resources/XIAO_ESP32C3_v1.3_KiCad_260116.zip',
        'assembly_transform': {'reference': 'U2', 'footprint_xy_mm': [77.39, 4.0],
            'footprint_rotation_deg': -90, 'model_offset_mm': vec(model.m_Offset),
            'model_rotation_deg': vec(model.m_Rotation), 'model_scale': vec(model.m_Scale),
            'grid_datum_carrier_xy_mm': [87.89, 12.9175],
            'old_nominal_fab_body_center_carrier_xy_mm': [87.89, 12.9],
            'primary_substrate_body_center_carrier_xy_mm': [87.9535, 12.9175],
            'primary_substrate_bbox_carrier_xy_mm': [77.476, 4.0275, 98.431, 21.8075],
            'unchanged_nominal_fab_body_bbox_carrier_xy_mm': [77.39, 4.0, 98.39, 21.8],
            'unchanged_typed_nominal_body_datum_cpl_xy_mm': [87.89, -12.90],
            'primary_substrate_cad_center_cpl_xy_mm': [87.9535, -12.9175],
            'cad_center_minus_typed_nominal_body_cpl_xy_mm': [0.0635, -0.0175],
            'nominal_body_vs_cad_caveat': 'Sub-0.1 mm CAD/nominal discrepancy; not evidence of a wrong typed datum basis. Existing CPL and its nominal-body placement proof remain untouched; visual asset does not reinterpret electrical source or placement.',
            'body_bounds_exclude': ['copper', 'solder mask', 'edge stroke thickness', 'all components', 'USB shell'],
            'drilled_grid_average_excludes': ['source J1/J2 extra edge castellations', 'test points', 'underside contacts', 'component coordinates'],
            'supplier_assembly_origin_qualified': False,
            'source_grid_datum_xy_mm': [148.4376, 105.0036],
            'source_to_carrier_translation_mm': [-60.5476, -92.0861],
            'registered_usb_footprint_xy_mm': registered_usb,
            'zero_z_is_retained_unmeasured_nominal': True,
            'z_caveat': 'Retained existing 0 mm model offset; no measured solder seating or stand-off and no Rev3C 11 mm socket stack copied. The source compound contains lower copper as low as -0.04 mm; zero offset is not physical fit proof.'},
        'fourteen_pin_registration': sorted(rows, key=lambda row: row['pin']),
        'land_fit_caveat': 'Drilled module pin centers differ from carrier SMD land rows by 0.4625 mm. Datum/axis registration does not qualify solder contact, pad overlap or underside-clearance fit.',
        'bound_visual_assets': assets, 'native_model_resolution': resolutions,
        'all_native_models_resolve': True, 'native_registration_scale_percent': 100,
        'actual_installed_native_geometry_receipt': 'verified-c3-installed-geometry.json',
        'qualification': 'Partial C3 visual reference; no enclosure, mating, RF, electrical, thermal, appliance or manufacturing qualification.'}
    (REV/'validation/verified-c3-model-preservation.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({'non_model_tokens_identical': True, 'protected_file_count': len(protected_rows),
                      'native_models_resolved': len(resolutions), 'scale_percent': 100,
                      'module_model_sha256': STEP_SHA}, indent=2))


if __name__ == '__main__':
    main()
