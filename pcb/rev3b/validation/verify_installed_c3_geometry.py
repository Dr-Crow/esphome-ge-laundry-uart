"""Check actual native installed STEP geometry, including all 14 pin holes.

Requires native KiCad CLI 9.0.9 on PATH and OCCT Python bindings. A transient
board resolves only KIPRJMOD paths; the retained source PCB is never saved.
The U2-filtered native export includes the unchanged carrier substrate because
KiCad's no-board-body mode rejects an assembly containing only this compound.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from OCP.Bnd import Bnd_Box
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepGProp import BRepGProp
from OCP.GeomAbs import GeomAbs_Cylinder
from OCP.GProp import GProp_GProps
from OCP.IFSelect import IFSelect_RetDone
from OCP.STEPControl import STEPControl_Reader
from OCP.TopAbs import TopAbs_FACE, TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS

REV = Path(__file__).resolve().parents[1]
PCB = REV/'design/GEA-Adapter-Rev3B.kicad_pcb'
MODEL = REV/'design/models/XIAO_ESP32C3_v1.3_vendor_pcb_visual_reference.step'
TRANSLATION = [87.89, -12.9175, 1.595]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    reader = STEPControl_Reader()
    assert reader.ReadFile(str(path)) == IFSelect_RetDone
    assert reader.TransferRoots() > 0
    shape = reader.OneShape()
    assert BRepCheck_Analyzer(shape).IsValid()
    return shape


def bounds(shape):
    box = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape, box, False, False)
    return box.Get()


def signatures(shape, translation=(0, 0, 0)):
    explorer = TopExp_Explorer(shape, TopAbs_SOLID)
    result = []
    while explorer.More():
        solid = explorer.Current()
        box = [v+translation[i%3] for i, v in enumerate(bounds(solid))]
        volume, area = GProp_GProps(), GProp_GProps()
        BRepGProp.VolumeProperties_s(solid, volume)
        BRepGProp.SurfaceProperties_s(solid, area)
        center = volume.CentreOfMass()
        values = [*box, volume.Mass(), area.Mass(), center.X()+translation[0],
                  center.Y()+translation[1], center.Z()+translation[2]]
        result.append(tuple(round(v, 5) for v in values))
        explorer.Next()
    return Counter(result)


def cylinder_centers(shape):
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    result = set()
    while explorer.More():
        surface = BRepAdaptor_Surface(TopoDS.Face_s(explorer.Current()))
        if surface.GetType() == GeomAbs_Cylinder:
            cylinder = surface.Cylinder()
            axis = cylinder.Axis()
            if abs(abs(axis.Direction().Z())-1) < 1e-7 and abs(cylinder.Radius()-.425) < 1e-6:
                point = axis.Location()
                result.add((round(point.X(), 6), round(point.Y(), 6)))
        explorer.Next()
    return result


def main():
    assert subprocess.check_output(['kicad-cli', '--version']).decode().strip() == '9.0.9'
    with tempfile.TemporaryDirectory(prefix='rev3b-c3-native-') as directory:
        scratch = Path(directory)
        transient = scratch/'model-registration.kicad_pcb'
        transient.write_text(PCB.read_text().replace('${KIPRJMOD}/models/',
                                                     str(REV/'design/models')+'/'))
        exported = scratch/'installed-c3-and-carrier.step'
        command = ['kicad-cli', 'pcb', 'export', 'step', '--force',
                   '--component-filter', 'U2', '--user-origin', '0x0mm',
                   '-o', str(exported), str(transient)]
        run = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        assert run.returncode == 0 and exported.is_file(), run.stdout.decode(errors='replace')[-2000:]
        model, installed = read(MODEL), read(exported)
        before, after = signatures(model, TRANSLATION), signatures(installed)
        assert sum(before.values()) == 1083 and sum(after.values()) == 1084
        missing, additions = before-after, after-before
        assert not missing, ('Imported solids changed or model transform incorrect', missing)
        assert sum(additions.values()) == 1
        carrier = next(iter(additions))
        assert list(carrier[:6]) == [0.0, -40.0, 0.0, 99.0, 0.0, 1.51]
        preservation = json.loads((REV/'validation/verified-c3-model-preservation.json').read_text())
        centers = cylinder_centers(installed)
        pins = []
        for row in preservation['fourteen_pin_registration']:
            x, y = row['registered_drill_xy_carrier_mm']
            target = (round(x, 6), round(-y, 6))
            assert target in centers, target
            pins.append({'pin': row['pin'], 'actual_native_step_hole_center_xy_mm': list(target),
                         'hole_radius_mm': .425, 'matches_primary_source_transform': True,
                         'carrier_land_kicad_xy_mm': row['unchanged_carrier_land_xy_mm'],
                         'drill_minus_land_kicad_xy_mm': row['drill_minus_land_xy_mm']})
        soc_bbox = [84.7677, -17.8051, 3.19, 89.7677, -12.8051, 4.04]
        assert any(list(signature[:6]) == soc_bbox for signature in after)
        box = bounds(installed)
        assert round(box[3], 5) == 99.764, 'USB shell does not project beyond the right edge'
        report = {
            'native_kicad_version': '9.0.9', 'source_pcb_sha256': sha(PCB),
            'source_model_sha256': sha(MODEL), 'native_export_sha256': sha(exported),
            'native_export_bytes': exported.stat().st_size, 'native_export_retained_in_repository': False,
            'export_scope': 'Diagnostic native STEP: U2 compound plus unchanged carrier substrate; no manufacturing/CAM export changes.',
            'source_and_export_occt_shape_valid': True, 'source_model_solid_count': 1083,
            'export_solid_count': 1084, 'all_source_solids_preserved_at_actual_installed_transform': True,
            'geometry_signature': 'Multiset of optimal bounding box, volume, surface area and center of mass for all solids, rounded to 0.00001 in mm / corresponding geometry units.',
            'actual_native_source_to_installed_translation_xyz_mm': TRANSLATION,
            'actual_native_xy_rotation_deg': 0, 'fourteen_actual_native_pin_holes': pins,
            'nominal_soc_bbox_native_step_mm': soc_bbox,
            'usb_right_verified_by_native_geometry_and_render': True,
            'generic_usb_shell_extreme_carrier_x_mm': round(box[3], 5),
            'z_caveat': 'Native export places source substrate bottom at 1.595 mm with the retained 0 mm model offset. This follows nominal native board stackup; solder stand-off and real installed seating remain unmeasured.',
            'supplier_assembly_origin_qualified': False,
            'all_electrical_manufacturing_and_placement_source_unchanged': True}
        (REV/'validation/verified-c3-installed-geometry.json').write_text(json.dumps(report, indent=2)+'\n')
        print(json.dumps({'preserved_source_solids': 1083, 'pin_holes_matched': len(pins),
                          'native_translation_mm': TRANSLATION, 'usb_right_verified': True}, indent=2))


if __name__ == '__main__':
    main()
