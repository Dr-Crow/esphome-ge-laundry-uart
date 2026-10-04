"""Independently compare all original STEP solids against the SoC additions."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_Reader
from OCP.TopAbs import TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer

REV = Path(__file__).resolve().parents[1]
PREVIOUS_SHA = {
    'c3': 'ce94f33287391d085e1cab8886d803a4e3822b638902346ca5a8ecb020f55055',
    'c6': '81efa7c7c0e1d811a9d34c3eb9ff03c09ee8861f5cb627265f05abbf8824f992'}


def signature(shape):
    bounds = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape, bounds, False, False)
    volume, area = GProp_GProps(), GProp_GProps()
    BRepGProp.VolumeProperties_s(shape, volume)
    BRepGProp.SurfaceProperties_s(shape, area)
    center = volume.CentreOfMass()
    return tuple(round(x, 6) for x in [*bounds.Get(), volume.Mass(), area.Mass(),
                                      center.X(), center.Y(), center.Z()])


def signatures(path):
    reader = STEPControl_Reader()
    assert reader.ReadFile(str(path)) == IFSelect_RetDone
    assert reader.TransferRoots() > 0
    explorer = TopExp_Explorer(reader.OneShape(), TopAbs_SOLID)
    result = []
    while explorer.More():
        result.append(signature(explorer.Current()))
        explorer.Next()
    return Counter(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', required=True, type=Path)
    args = parser.parse_args()
    package = json.loads((REV/'validation/xiao-soc-package-provenance.json').read_text())
    rows = {}
    for key, revision in [('c3', 'v1.3'), ('c6', 'v1.0')]:
        name = f'XIAO_ESP32{key.upper()}_{revision}_vendor_pcb_visual_reference.step'
        old, new = args.source_root/name, REV/'design/models'/name
        assert hashlib.sha256(old.read_bytes()).hexdigest() == PREVIOUS_SHA[key]
        before, after = signatures(old), signatures(new)
        missing, additions = before-after, after-before
        assert not missing, (key, 'previous solids changed', missing)
        assert sum(additions.values()) == 1, (key, additions)
        added = next(iter(additions))
        assert list(added[:6]) == package['modules'][key]['component_bbox_module_step_mm']
        rows[key] = {'before_step_sha256': PREVIOUS_SHA[key],
                     'after_step_sha256': hashlib.sha256(new.read_bytes()).hexdigest(),
                     'before_solid_count': sum(before.values()),
                     'after_solid_count': sum(after.values()),
                     'all_previous_solid_geometry_signatures_preserved': True,
                     'new_solid_count': 1, 'new_solid_signature': list(added)}
        print(key, 'all previous solids preserved; one verified SoC added', flush=True)
    report = {'comparison': 'Multiset of every solid: optimal bbox, volume, surface area and center of mass, rounded to 0.000001 mm / corresponding geometry units. This independently checks exports in addition to the exact source non-model token proof.',
              'signature_fields': ['x_min','y_min','z_min','x_max','y_max','z_max',
                                   'volume_mm3','surface_area_mm2','center_x_mm',
                                   'center_y_mm','center_z_mm'], 'modules': rows}
    (REV/'validation/xiao-soc-export-geometry-preservation.json').write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
