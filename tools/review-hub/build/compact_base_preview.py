"""Orthographic preview of the open compact base, highlighting the C3 pocket tongue."""
import struct

import numpy as np
from PIL import Image


def render(stl, destination):
    raw = stl.read_bytes()
    count, = struct.unpack_from('<I', raw, 80)
    if len(raw) != 84 + 50 * count:
        raise ValueError(f'{stl}: expected binary STL')
    dt = np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')])
    triangles = np.frombuffer(raw, dt, offset=84)['v'].astype(float)
    camera = np.array([-.45, .7, 1.1])
    camera /= np.linalg.norm(camera)
    right = np.cross([0, 0, 1], camera)
    right /= np.linalg.norm(right)
    up = np.cross(camera, right)
    proj = triangles @ np.array([right, -up, camera]).T
    lo, hi = proj[:, :, :2].min((0, 1)), proj[:, :, :2].max((0, 1))
    w, h = 1350, 900
    scale = min((w - 80) / (hi[0] - lo[0]), (h - 80) / (hi[1] - lo[1]))
    proj[:, :, :2] = (proj[:, :, :2] - (hi + lo) / 2) * scale + [w / 2, h / 2]
    rgb = np.full((h, w, 3), [234, 240, 237], dtype=np.uint8)
    depth = np.full((h, w), -np.inf)
    light = np.array([-.4, -.3, .86]); light /= np.linalg.norm(light)
    highlighted = 0
    for model, tri in zip(triangles, proj):
        normal = np.cross(model[1] - model[0], model[2] - model[0])
        length = np.linalg.norm(normal)
        if length < 1e-10 or normal @ camera <= 0:
            continue
        normal /= length
        x, y, z = model.mean(0)
        # Face coordinates are in the generator's assembled case datum (mm).
        tongue = 3.99 < x < 17.01 and -3.5 < y < -2.1 and z > 6.8
        highlighted += int(tongue)
        colour = np.array([233, 154, 52] if tongue else [83, 126, 119])
        colour = np.minimum(255, colour * (.68 + .36 * max(0, normal @ light)))
        points = tri[:, :2]
        x0, y0 = np.floor(points.min(0)).astype(int)
        x1, y1 = np.ceil(points.max(0)).astype(int) + 1
        gy, gx = np.ogrid[y0:y1, x0:x1]
        a, b, c = tri
        den = (b[1]-c[1])*(a[0]-c[0]) + (c[0]-b[0])*(a[1]-c[1])
        if abs(den) < 1e-10:
            continue
        u = ((b[1]-c[1])*(gx+.5-c[0]) + (c[0]-b[0])*(gy+.5-c[1])) / den
        v = ((c[1]-a[1])*(gx+.5-c[0]) + (a[0]-c[0])*(gy+.5-c[1])) / den
        z = u*a[2] + v*b[2] + (1-u-v)*c[2]
        region = depth[y0:y1, x0:x1]
        visible = (u >= 0) & (v >= 0) & (u+v <= 1) & (z > region)
        region[visible] = z[visible]
        rgb[y0:y1, x0:x1][visible] = colour
    if not highlighted:
        raise ValueError(f'{stl}: corrected tongue not found at its expected location')
    Image.fromarray(rgb).resize((900, 600), Image.Resampling.LANCZOS).save(destination, optimize=True)
