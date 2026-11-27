"""Supply two missing OCC meshes from the referenced STEP solids, preserving footprint transforms."""
import sys
from pathlib import Path

import build123d as cad
import numpy as np

import glbtools


def solids(shape):
    if shape.children:
        for child in shape.children:
            yield from solids(child)
    elif len(shape.solids()):
        yield shape


def solid_meshes(node, nodes):
    if 'mesh' in node:
        yield node['mesh']
    for index in node.get('children', []):
        yield from solid_meshes(nodes[index], nodes)


def repair(input_glb, output_glb, models, fitted):
    scene, chunks = glbtools.read_glb(input_glb)
    data = bytearray(chunks[0][1][:scene['buffers'][0]['byteLength']])
    nodes = scene['nodes']
    root = nodes[scene['scenes'][0]['nodes'][0]]
    indices = {nodes[i].get('name'): i for i in root['children']}

    def accessor(vectors):
        vectors = np.ascontiguousarray(vectors, dtype='<f4')
        data.extend(bytes(-len(data) % 4))
        view = len(scene['bufferViews'])
        scene['bufferViews'].append({'buffer': 0, 'byteOffset': len(data), 'byteLength': vectors.nbytes, 'target': 34962})
        data.extend(vectors.tobytes())
        index = len(scene['accessors'])
        scene['accessors'].append({'bufferView': view, 'componentType': 5126, 'count': len(vectors), 'type': 'VEC3',
                                   'min': vectors.min(0).tolist(), 'max': vectors.max(0).tolist()})
        return index

    for reference in ('C30', 'D8'):
        if reference in indices and reference not in fitted:
            root['children'].remove(indices[reference])
    for reference, stem in [('D11', 'Nexperia_CFP3_SOD-123W'), ('L1', 'L_Sunlord_SWPA5040S')]:
        node = nodes[indices[reference]]
        if reference not in fitted or any(True for _ in solid_meshes(node, nodes)):
            continue
        step = next(models.rglob(stem + '.step'))
        primitives = []
        for solid in solids(cad.import_step(step)):
            vertices, faces = solid.tessellate(.012)
            # STEP uses millimetres with Z up. GLTF uses metres with Y up.
            positions = np.array([tuple(v) for v in vertices])[:, [0, 2, 1]] / 1000
            positions[:, 2] *= -1
            triangles = positions[np.array(faces)]
            normals = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
            lengths = np.linalg.norm(normals, axis=1)
            valid = lengths > 1e-16
            color = list(solid.color) if solid.color else [.62, .63, .64, 1.]
            material = len(scene['materials'])
            scene['materials'].append({'name': stem + ' finish', 'pbrMetallicRoughness': {
                'baseColorFactor': color, 'metallicFactor': .1, 'roughnessFactor': .55}})
            primitives.append({'attributes': {'POSITION': accessor(triangles[valid].reshape(-1, 3)),
                                               'NORMAL': accessor(np.repeat(normals[valid] / lengths[valid, None], 3, axis=0))},
                               'mode': 4, 'material': material})
        if not primitives:
            raise ValueError(f'{reference}: no tessellated solids in {step}')
        node.pop('children', None)
        node['mesh'] = len(scene['meshes'])
        scene['meshes'].append({'name': stem, 'primitives': primitives})
    scene['buffers'][0]['byteLength'] = len(data)
    glbtools.write_glb(output_glb, scene, [(b'BIN\0', bytes(data))])


if __name__ == '__main__':
    repair(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), set(sys.argv[4:]))
