"""Add only the verified QFN32 package to pinned partial Seeed derivatives.

Requires OCCT Python bindings and native KiCad CLI 9.0.9. Source input is the
previous producer's immutable derivatives, not the carrier PCB. Run with:
  python augment_xiao_soc_models.py --source-root XIAO_RESEARCH --work-dir OUTPUT
The existing model root is XIAO_RESEARCH/models. No source download or refill.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.Bnd import Bnd_Box
from OCP.GeomAbs import GeomAbs_Circle
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_Reader
from OCP.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS

REV = Path(__file__).resolve().parents[1]
MODEL = REV / 'design/models/xiao-packages/QFN-32-1EP_5x5mm_P0.5mm_EP3.7x3.7mm.step'
MODEL_SHA = '7e77a52b3e261a45529e0df739376ea7cd79204fb1afad81332a50f4f1607000'
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+')
INPUTS = {
    'c3': ('v1.3', 'ee202b11df30ade4d21c983527c5201dd8b0a3eff9f23e7fc4c059b274a5c081',
           [148.4376, 105.0036], -90, [-0.6223, -2.3876], [-2.5223, -0.4876, 2.445]),
    'c6': ('v1.0', '21263d3e4d89f354f719f2bae7bb506a46029ef6b35181b7da86e53ae0e65bd2',
           [108.3977, 72.876], 0, [-1.5627, -2.9314], [-3.4627, -1.0314, 2.445]),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def nodes(text):
    stack, result = [], []
    for match in TOKEN.finditer(text):
        value = match.group()
        if value == '(':
            stack.append([match.start(), None])
        elif value == ')':
            start, name = stack.pop()
            result.append((start, match.end(), name))
        elif stack and stack[-1][1] is None:
            stack[-1][1] = value
    assert not stack
    return result


def non_model_tokens(text):
    for start, end, name in sorted(nodes(text), reverse=True):
        if name == 'model':
            text = text[:start] + text[end:]
    return TOKEN.findall(text)


def read_step(path):
    reader = STEPControl_Reader()
    assert reader.ReadFile(str(path)) == IFSelect_RetDone, path
    assert reader.TransferRoots() > 0
    return reader.OneShape()


def bbox(shape):
    bounds = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape, bounds, False, False)
    return [round(float(n), 9) for n in bounds.Get()]


def parts(shape, kind):
    explorer = TopExp_Explorer(shape, kind)
    while explorer.More():
        yield explorer.Current()
        explorer.Next()


def summary(path):
    shape = read_step(path)
    solids = list(parts(shape, TopAbs_SOLID))
    valid = bool(BRepCheck_Analyzer(shape).IsValid())
    assert valid and all(BRepCheck_Analyzer(s).IsValid() for s in solids), path
    return shape, {'path': path.name, 'bytes': path.stat().st_size,
                   'sha256': sha(path), 'bbox_mm': dict(zip(
                       ['x_min', 'y_min', 'z_min', 'x_max', 'y_max', 'z_max'], bbox(shape))),
                   'solid_count': len(solids),
                   'face_count': sum(1 for _ in parts(shape, TopAbs_FACE)),
                   'occt_shape_valid': valid}


def top_marker_centers(shape):
    centers = set()
    for edge in parts(shape, TopAbs_EDGE):
        curve = BRepAdaptor_Curve(TopoDS.Edge_s(edge))
        if curve.GetType() != GeomAbs_Circle:
            continue
        circle = curve.Circle()
        pt = circle.Location()
        if abs(circle.Radius() - 0.25) < 1e-6 and abs(pt.Z() - 2.445) < 1e-6:
            centers.add(tuple(round(n, 6) for n in [pt.X(), pt.Y(), pt.Z()]))
    return sorted(centers)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', required=True, type=Path)
    parser.add_argument('--work-dir', required=True, type=Path)
    args = parser.parse_args()
    assert subprocess.check_output(['kicad-cli', '--version']).decode().strip() == '9.0.9'
    assert sha(MODEL) == MODEL_SHA
    args.work_dir.mkdir(parents=True, exist_ok=True)
    source_provenance = json.loads((REV/'validation/xiao-model-provenance.json').read_text())
    model_shape, model_summary = summary(MODEL)
    assert bbox(model_shape) == [-2.5, -2.5, 0.0, 2.5, 2.5, 0.85]
    report = {'producer': 'augment_xiao_soc_models.py', 'kicad_version': '9.0.9',
              'source_model': model_summary, 'model_scale': [1, 1, 1], 'modules': {}}
    for key, (revision, input_sha, origin, rotation, center, marker) in INPUTS.items():
        name = f'XIAO_ESP32{key.upper()}_{revision}_vendor_pcb_visual_reference'
        source = args.source_root/(name+'.kicad_pcb')
        assert sha(source) == input_sha, (key, 'wrong previous derivative')
        # Verify the unchanged official PCB from the exact current archive.
        official = args.source_root/source_provenance['modules'][key]['original_pcb_path']
        assert sha(official) == source_provenance['modules'][key]['original_pcb_sha256']
        before = source.read_text()
        footprint = [(s, e) for s, e, tag in nodes(before) if tag == 'footprint' and
                     re.search(r'\(property "Reference" "U4"', before[s:e])]
        assert len(footprint) == 1
        start, end = footprint[0]
        assert not any(tag == 'model' for _, _, tag in nodes(before[start:end]))
        node = ('\n\t\t(model '+json.dumps(str(MODEL))+
                '\n\t\t\t(offset (xyz 0 0 0))\n\t\t\t(scale (xyz 1 1 1))'+
                f'\n\t\t\t(rotate (xyz 0 0 {rotation}))\n\t\t)\n\t')
        after = before[:end-1] + node + before[end-1:]
        assert non_model_tokens(before) == non_model_tokens(after)
        derivative = args.work_dir/(name+'.kicad_pcb')
        derivative.write_text(after)
        output = args.work_dir/(name+'.step')
        common = ['kicad-cli', 'pcb', 'export', 'step', '--force', '-D',
                  'KICAD9_3DMODEL_DIR='+str(args.source_root/'models'),
                  '--user-origin', f'{origin[0]}x{origin[1]}mm']
        command = common + ['--include-tracks', '--include-pads', '--include-zones',
                            '--include-inner-copper', '--min-distance', '0.001mm',
                            '-o', str(output), str(derivative)]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (args.work_dir/(key+'-soc-augmented-export.log')).write_bytes(result.stdout)
        assert result.returncode == 0, result.stdout.decode(errors='replace')
        _, output_summary = summary(output)
        isolated = args.work_dir/(key+'-soc-component-and-board.step')
        result = subprocess.run(common + ['--component-filter', 'U4', '-o', str(isolated),
                                          str(derivative)], stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        assert result.returncode == 0, result.stdout.decode(errors='replace')
        shape, isolated_summary = summary(isolated)
        soc_solids = [s for s in parts(shape, TopAbs_SOLID) if bbox(s)[2] > 1.59]
        assert len(soc_solids) == 1
        soc_bbox = bbox(soc_solids[0])
        assert soc_bbox == [round(center[0]-2.5, 9), round(center[1]-2.5, 9), 1.595,
                            round(center[0]+2.5, 9), round(center[1]+2.5, 9), 2.445]
        markers = top_marker_centers(shape)
        assert markers == [tuple(marker)], (key, markers, marker)
        report['modules'][key] = {'source_derivative_sha256': input_sha,
            'updated_derivative_sha256': sha(derivative),
            'non_model_derivative_tokens_unchanged': True,
            'updated_non_model_token_sha256': hashlib.sha256(json.dumps(
                non_model_tokens(after), separators=(',', ':')).encode()).hexdigest(),
            'model_offset_mm': [0, 0, 0], 'model_rotation_deg': [0, 0, rotation],
            'source_export_origin_mm': origin, 'component_bbox_module_step_mm': soc_bbox,
            'exported_pin1_marker_center_module_step_mm': list(markers[0]),
            'marker_radius_mm': 0.25, 'marker_shape_is_generic_library_detail': True,
            'component_filter_validation': isolated_summary,
            'detailed_visual_reference': output_summary,
            'included_component_count': {'c3': 41, 'c6': 47}[key]}
        print(key, 'verified SoC', soc_bbox, flush=True)
    (args.work_dir/'xiao-soc-export-validation.json').write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
