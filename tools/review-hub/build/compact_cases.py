"""Rebuild the verified CAD views from the compact enclosure STLs and module-specific carrier."""
import hashlib
import json
import struct
import shutil
from pathlib import Path

import numpy as np

import glbtools
import compact_base_preview


def save_case_mesh(stl, out):
    """Reindex the source triangles in assembled CAD axes and convert millimetres to metres."""
    source = stl.read_bytes()
    count, = struct.unpack_from('<I', source, 80)
    if len(source) != 84 + 50 * count:
        raise ValueError(f'{stl}: expected a binary STL')
    dtype = np.dtype([('normal', '<f4', 3), ('vertices', '<f4', (3, 3)), ('attribute', '<u2')])
    triangles = np.frombuffer(source, dtype=dtype, offset=84)['vertices']
    verts, order = np.unique(triangles.reshape(-1, 3), axis=0, return_inverse=True)
    verts = np.ascontiguousarray(verts / 1000, dtype='<f4')
    indices = np.ascontiguousarray(order, dtype='<u2' if len(verts) < 65536 else '<u4')
    geometry = verts.tobytes() + indices.tobytes()
    gltf = {'asset': {'version': '2.0', 'generator': 'Native enclosure STL'}, 'scene': 0,
            'scenes': [{'nodes': [0]}], 'nodes': [{'name': stl.stem, 'mesh': 0}],
            'meshes': [{'primitives': [{'attributes': {'POSITION': 0}, 'indices': 1, 'mode': 4}]}],
            'buffers': [{'byteLength': len(geometry)}],
            'bufferViews': [{'buffer': 0, 'byteLength': verts.nbytes, 'target': 34962},
                            {'buffer': 0, 'byteOffset': verts.nbytes, 'byteLength': indices.nbytes, 'target': 34963}],
            'accessors': [{'bufferView': 0, 'componentType': 5126, 'count': len(verts), 'type': 'VEC3',
                           'min': verts.min(0).tolist(), 'max': verts.max(0).tolist()},
                          {'bufferView': 1, 'componentType': 5123 if indices.itemsize == 2 else 5125,
                           'count': indices.size, 'type': 'SCALAR'}]}
    glbtools.write_glb(out, gltf, [(b'BIN\0', geometry)])


def build(cfg, data, exporter):
    here = Path(__file__).resolve().parent
    repo = Path(cfg['repo'])
    records = json.loads((here / 'compact-cases.config.json').read_text())
    generated = set()
    for record in records:
        rev = record['compact_revision']
        dest = data / 'cases' / rev
        dest.mkdir(parents=True, exist_ok=True)
        for part, filename in zip(record['parts'], record['source_files'], strict=True):
            stl = repo / filename
            if hashlib.sha256(stl.read_bytes()).hexdigest() != record['source_sha256'][stl.name]:
                raise ValueError(f'{stl}: enclosure CAD changed; regenerate its preview and check the board registration')
            glb = data / part['file']
            if glb not in generated:
                save_case_mesh(stl, glb)
                generated.add(glb)
                if part['role'] == 'base':
                    compact_base_preview.render(stl, data / record['open_base_preview'])
            part['bytes'] = glb.stat().st_size
        del record['source_sha256']
        source = (repo / record['source_files'][0]).parent
        facts = json.loads((source / 'case-checks.json').read_text())
        params = record['params']
        if params['pcb_mm'] != facts['pcb_mm'] or params['enclosure_exterior_mm'] != facts['assembled_outer_mm']:
            raise ValueError(f'{rev}: recorded dimensions differ from native case checks')
        shutil.copyfile(here / 'compact-previews' / (record['id'] + '.png'), data / record['preview'])
        pcb = repo / exporter.REVS[rev]['pcb']
        width, height, _ = facts['pcb_mm']
        origin = [width / 2, height / 2]
        board_json = data / rev / 'board.json'
        if board_json.is_file():
            board = json.loads(board_json.read_text())
            origin = board['glb']['origin_mm']
            bottom = board['glb']['board_bottom_y_mm']
        else:
            bottom = 0
        matrix = [[1, 0, 0, -origin[0]], [0, 0, 1, bottom - facts['floor_to_pcb_underside_mm']],
                  [0, -1, 0, height - origin[1]], [0, 0, 0, 1]]
        bp = record['board_placement']
        if not np.allclose(matrix, bp['matrix_mm'], atol=.01):
            raise ValueError(f'{rev}: carrier origin no longer matches the validated enclosure datum')
        if record['module_variant'] != 'c6':
            continue
        # Exchange only the visual model. Both modules mount on the same socket pin datum.
        work = exporter.CACHE / rev / 'case-c6'
        work.mkdir(parents=True, exist_ok=True)
        original = pcb.read_text()
        c3 = 'XIAO_ESP32C3_v1.3_vendor_pcb_visual_reference.step'
        c6 = 'XIAO_ESP32C6_v1.0_vendor_pcb_visual_reference.step'
        if original.count(c3) != 1 or original.count(c6):
            raise ValueError(f'{rev}: expected exactly one fitted C3 visual model')
        board = work / pcb.name
        board.write_text(original.replace(c3, c6).replace('${KIPRJMOD}', str(pcb.parent)))
        exporter.export_compact_model(rev, board, origin, work / 'raw.glb', data / record['board_asset'])
    return records
