"""Small GLB JSON-chunk helpers (no geometry work; geometry is handled by gltf-transform / trimesh)."""
import json, struct


def read_glb(path):
    b = open(path, 'rb').read()
    magic, ver, total = struct.unpack('<4sII', b[:12])
    assert magic == b'glTF'
    off = 12
    chunks = []
    while off < total:
        ln, typ = struct.unpack('<I4s', b[off:off + 8])
        chunks.append((typ, b[off + 8:off + 8 + ln]))
        off += 8 + ln
    j = json.loads(chunks[0][1])
    return j, chunks[1:]


def write_glb(path, j, rest):
    js = json.dumps(j, separators=(',', ':')).encode()
    js += b' ' * ((4 - len(js) % 4) % 4)
    body = struct.pack('<I4s', len(js), b'JSON') + js
    for typ, data in rest:
        data = data + (b'\0' * ((4 - len(data) % 4) % 4))
        body += struct.pack('<I4s', len(data), typ) + data
    open(path, 'wb').write(struct.pack('<4sII', b'glTF', 2, 12 + len(body)) + body)


def wrap_named_mesh_nodes(src, dst):
    """Footprint nodes that carry a mesh directly get the mesh moved to a child node, so later
    quantization (which rewrites the transform of mesh-bearing nodes) cannot move the footprint origin."""
    j, rest = read_glb(src)
    n0 = len(j['nodes'])
    for i in range(n0):
        nd = j['nodes'][i]
        if nd.get('name') and 'mesh' in nd and i in (j['scenes'][0]['nodes'] + [c for x in j['nodes'] for c in x.get('children', [])]):
            child = {'mesh': nd.pop('mesh'), 'name': nd['name'] + '__mesh'}
            if 'skin' in nd: child['skin'] = nd.pop('skin')
            j['nodes'].append(child)
            nd.setdefault('children', []).append(len(j['nodes']) - 1)
    write_glb(dst, j, rest)


def world_nodes(j):
    """name -> (4x4 world matrix as nested lists) for every named node, via simple TRS composition."""
    import numpy as np
    def local(n):
        if 'matrix' in n:
            return np.array(n['matrix']).reshape(4, 4).T
        t = np.array(n.get('translation', [0, 0, 0]), float)
        q = n.get('rotation', [0, 0, 0, 1]); s = n.get('scale', [1, 1, 1])
        x, y, z, w = q
        R = np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
                      [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)],
                      [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
        M = np.eye(4); M[:3, :3] = R * np.array(s); M[:3, 3] = t
        return M
    out = {}
    def walk(i, P):
        n = j['nodes'][i]; M = P @ local(n)
        if n.get('name'): out.setdefault(n['name'], []).append(M)
        for c in n.get('children', []): walk(c, M)
    for r in j['scenes'][0]['nodes']: walk(r, np.eye(4))
    return out


def footprint_nodes(j):
    """Nodes that sit directly under the scene root (KiCad puts one unnamed wrapper node under the scene, whose
    children are the per-footprint nodes). Returns (level_node_indices, {name: world 4x4})."""
    import numpy as np
    roots = j['scenes'][0]['nodes']
    lvl = roots
    P = np.eye(4)
    if len(roots) == 1 and not j['nodes'][roots[0]].get('name'):
        w = world_nodes_idx(j, roots[0], np.eye(4))
        P = w
        lvl = j['nodes'][roots[0]].get('children', [])
    out = {}
    for i in lvl:
        M = P @ _local(j['nodes'][i])
        n = j['nodes'][i].get('name')
        if n: out.setdefault(n, M)
    return lvl, out


def _local(n):
    import numpy as np
    if 'matrix' in n:
        return np.array(n['matrix']).reshape(4, 4).T
    t = np.array(n.get('translation', [0, 0, 0]), float)
    x, y, z, w = n.get('rotation', [0, 0, 0, 1]); s = n.get('scale', [1, 1, 1])
    R = np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
                  [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)],
                  [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
    M = np.eye(4); M[:3, :3] = R * np.array(s); M[:3, 3] = t
    return M


def world_nodes_idx(j, i, P):
    return P @ _local(j['nodes'][i])
