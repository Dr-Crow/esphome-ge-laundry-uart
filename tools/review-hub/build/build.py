#!/usr/bin/env python3
"""Design-review hub asset pipeline.

    python3 build/build.py                  # everything
    python3 build/build.py --rev rev3d      # one revision (pcb assets + cost + index)
    python3 build/build.py --cases | --docs | --cost
    python3 build/build.py --cost --refresh # re-query JLCPCB instead of using build/cache/jlc

Real work is done by kicad-cli / pcbnew (pinned Docker image), gltf-transform (pinned npm libs),
trimesh and rsvg-convert. This file is the glue. See ../README.md.
"""
import argparse, csv, datetime, hashlib, io, json, os, re, shutil, subprocess, sys, time, zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import hubenv

if __name__ == '__main__':
    hubenv.ensure_env()  # re-exec inside build/.venv (Pillow/numpy/trimesh); created on first run

import numpy as np
from PIL import Image, ImageDraw
import glbtools
import sexp

CFG = hubenv.load_config()
REPO = Path(CFG['repo'])
IMAGE = CFG['kicad_image']
PPM = CFG['px_per_mm']
SITE = hubenv.SITE          # --out / HUB_SITE; default tools/review-hub/site
DATA = SITE / 'data'
CACHE = hubenv.CACHE        # --cache / HUB_CACHE; default build/cache
PKG3D = CACHE / 'packages3D'  # KiCad standard 3D models (build/models.py --fetch-models), mounted read-only into the container
REVS = {r['id']: r for r in CFG['revisions']}
GLTF_CLI = '@gltf-transform/cli@4.3.0'


def log(rev, msg):
    print(f'[{rev}] {msg}', flush=True)


def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(f'command failed ({r.returncode}): {" ".join(map(str, cmd))[:300]}\n{r.stdout[-1500:]}\n{r.stderr[-1500:]}')
    return r.stdout


def docker(argv):
    """Run a command in the pinned KiCad image (repo read-only, build/ and site/ writable)."""
    mounts = [(REPO, 'ro'), (HERE, 'rw'), (SITE, 'rw'), (CACHE, 'rw'), (PKG3D, 'ro')]
    seen, vols = set(), []
    for p, mode in mounts:
        if p not in seen:
            seen.add(p)
            vols += ['-v', f'{p}:{p}:{mode}']
    return sh(['docker', 'run', '--rm', '--platform', 'linux/amd64'] + vols
              + sum((['-e', f'KICAD{n}_3DMODEL_DIR={PKG3D}'] for n in (6, 7, 8, 9)), []) + [IMAGE] + [str(a) for a in argv])


def kicad_cli(*argv):
    return docker(['kicad-cli'] + list(argv))


def jwrite(path, obj, indent=None):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, indent=indent, separators=(',', ':') if indent is None else None) + '\n')


def sha(*paths_or_bytes):
    h = hashlib.sha1()
    for p in paths_or_bytes:
        h.update(p if isinstance(p, bytes) else Path(p).read_bytes() if Path(p).exists() else b'')
    return h.hexdigest()[:12]


def fresh(stamp_file, key, force):
    """Stage cache: true if stamp_file holds `key` (inputs unchanged) and --force not given."""
    if not force and stamp_file.exists() and stamp_file.read_text().strip() == key:
        return True
    return False


# --------------------------------------------------------------------------- BOM / netlist
def read_bom(rev):
    """-> list of {ref, lcsc, comment, footprint, dnp}. Handles the JLC format and rev2.0's KiCad-BOM-in-zip format."""
    spec = REVS[rev]['bom']
    if not spec:
        return None
    if isinstance(spec, dict):
        text = zipfile.ZipFile(REPO / spec['zip']).read(spec['member']).decode('utf-8-sig')
    else:
        text = (REPO / spec).read_text(encoding='utf-8-sig')
    rows = []
    for r in csv.DictReader(io.StringIO(text)):
        refs = r.get('Designator') or r.get('Reference') or ''
        lcsc = (r.get('LCSC Part #') or '').strip()
        if not lcsc:  # rev2.0 puts the LCSC code in the Description column
            d = (r.get('Description') or '').strip()
            lcsc = d if re.fullmatch(r'C\d+', d) else ''
        for ref in re.split(r'[,\s]+', refs.strip()):
            if ref:
                rows.append({'ref': ref, 'lcsc': lcsc, 'comment': r.get('Comment') or r.get('Value') or '',
                             'footprint': r.get('Footprint') or '', 'dnp': (r.get('DNP') or '').strip() not in ('', '0')})
    return rows


def netlist_fields(rev, cdir):
    """Schematic netlist (kicad-cli sch export netlist) -> {ref: {field: value, '_description':..}}. {} if no schematic."""
    sch = REVS[rev].get('sch')
    if not sch or not (REPO / sch).exists():
        return {}
    out = cdir / 'netlist.net'
    kicad_cli('sch', 'export', 'netlist', '--format', 'kicadsexpr', '-o', out, REPO / sch)
    tree = sexp.parse(out.read_text())
    res = {}
    for comp in sexp.find_all(tree, 'comp'):
        ref = sexp.get(comp, 'ref')
        f = {}
        fl = sexp.child(comp, 'fields')
        if fl:
            for fld in sexp.find_all(fl, 'field'):
                f[sexp.get(fld, 'name')] = fld[-1] if isinstance(fld[-1], str) else ''
        f['_value'] = sexp.get(comp, 'value') or ''
        f['_datasheet'] = sexp.get(comp, 'datasheet') or ''
        f['_description'] = sexp.get(comp, 'description') or ''
        ls = sexp.child(comp, 'libsource')
        if ls and not f['_description']:
            f['_description'] = sexp.get(ls, 'description') or ''
        res[ref] = f
    return res


# --------------------------------------------------------------------------- per-revision stages
def stage_extract(rev, force):
    cdir = CACHE / rev
    cdir.mkdir(parents=True, exist_ok=True)
    pcb = REPO / REVS[rev]['pcb']
    out = cdir / 'extract.json'
    key = sha(pcb, HERE / 'kicad_extract.py', PKG3D / 'MANIFEST.json')
    if not fresh(cdir / 'extract.stamp', key, force) or not out.exists():
        log(rev, 'pcbnew extract')
        docker(['python3', HERE / 'kicad_extract.py', pcb, out])
        (cdir / 'extract.stamp').write_text(key)
    return json.load(open(out))


def pad_probe_candidates(ex):
    return ex.get('pad_probes', [])


def export_compact_model(rev, pcb, origin, raw, final):
    """Only fitted components are rendered. Repair empty STEP meshes under their native transforms."""
    direct = raw.with_name('direct.glb')
    cx, cy = origin
    kicad_cli('pcb', 'export', 'glb', '--subst-models', '--no-dnp', '--include-silkscreen', '--include-soldermask',
              '--user-origin', f'{cx}x{cy}mm', '-o', direct, pcb)
    refs = [p['ref'] for p in read_bom(rev) if not p['dnp']]
    sh([hubenv.cad_python(CFG), HERE / 'compact_fitted.py', direct, raw, PKG3D, *refs])
    sh(['node', HERE / 'optimize_glb.mjs', raw, final, '--wrap'], cwd=HERE)


def stage_glb(rev, ex, force):
    cdir = CACHE / rev
    pcb = REPO / REVS[rev]['pcb']
    bb = ex['bbox_mm']
    cx, cy = round((bb['x0'] + bb['x1']) / 2, 4), round((bb['y0'] + bb['y1']) / 2, 4)
    raw = cdir / 'raw.glb'
    outdir = DATA / rev
    outdir.mkdir(parents=True, exist_ok=True)
    final = outdir / 'board.glb'
    key = sha(pcb, HERE / 'optimize_glb.mjs', HERE / 'glbtools.py', PKG3D / 'MANIFEST.json', f'{cx},{cy}'.encode())
    compact = rev in ('rev3i', 'rev3j', 'rev3k', 'rev3l', 'rev3m')
    if compact:
        key = sha(key.encode(), HERE / 'compact_fitted.py', REPO / REVS[rev]['bom'])
    if not fresh(cdir / 'glb.stamp', key, force) or not final.exists() or not raw.exists():
        log(rev, f'kicad-cli export glb (origin {cx},{cy})')
        if compact:
            export_compact_model(rev, pcb, (cx, cy), raw, final)
        else:
            kicad_cli('pcb', 'export', 'glb', '--subst-models', '--include-silkscreen', '--include-soldermask',
                      '--user-origin', f'{cx}x{cy}mm', '-o', raw, pcb)
            log(rev, 'optimize (join primitives / dedup / meshopt)')
            sh(['node', HERE / 'optimize_glb.mjs', raw, final, '--wrap'], cwd=HERE)
        (cdir / 'glb.stamp').write_text(key)
    return verify_glb(rev, ex, raw, final, cx, cy)


def verify_glb(rev, ex, raw, final, cx, cy):
    """Compare every footprint's pcbnew position/rotation with its glTF node, in raw and compressed GLB."""
    import trimesh
    j_raw, _ = glbtools.read_glb(raw)
    j_fin, _ = glbtools.read_glb(final)
    lvl_raw, w_raw = glbtools.footprint_nodes(j_raw)
    raw_nodes = {j_raw['nodes'][i].get('name'): j_raw['nodes'][i] for i in lvl_raw}
    lvl_fin, w_fin = glbtools.footprint_nodes(j_fin)
    root_names = {j_fin['nodes'][i].get('name') for i in lvl_fin}
    res, seat_top, seat_bot = [], [], []
    for p in ex['parts']:
        for tag, w in (('raw', w_raw), ('final', w_fin)):
            if p['ref'] in w and tag == 'raw':
                M = w[p['ref']]
                gx, gy, gz = M[0, 3] * 1000, M[1, 3] * 1000, M[2, 3] * 1000
                yaw = np.degrees(np.arctan2(-M[2, 0], M[0, 0]))  # rotation about +Y
                res.append({'ref': p['ref'], 'side': p['side'], 'dx': gx - (p['x'] - cx), 'dz': gz - (p['y'] - cy),
                            'gy': gy, 'kx': p['x'], 'ky': p['y'], 'rot': p['rot'], 'yaw': float(yaw),
                            'in_final': p['ref'] in w_fin, 'group': 'mesh' not in raw_nodes[p['ref']],
                            'final_dx': float((w_fin[p['ref']][0, 3] * 1000) - (p['x'] - cx)) if p['ref'] in w_fin else 0.0,
                            'final_dz': float((w_fin[p['ref']][2, 3] * 1000) - (p['y'] - cy)) if p['ref'] in w_fin else 0.0,
                            'final_dy': float(w_fin[p['ref']][1, 3] * 1000 - gy) if p['ref'] in w_fin else 0.0})
                (seat_top if p['side'] == 'top' else seat_bot).append(gy)
    # board body extents (exclude silkscreen, which floats above the surface)
    scene = trimesh.load(str(raw), force='scene')
    stem = (REPO / REVS[rev]['pcb']).stem
    ext = [m.bounds[:, 1] * 1000 for n, m in scene.geometry.items() if n.startswith(stem + '_') and 'silkscreen' not in n.lower()]
    ymin = float(min(e[0] for e in ext)) if ext else None
    ymax = float(max(e[1] for e in ext)) if ext else None
    # rotation: which sign convention relates KiCad rot to glTF yaw (top side)
    def wrap(a): return (a + 180) % 360 - 180
    def mz(ref):
        ms = pm0[ref].get('models', [])
        return ms[0]['rotation_deg'][2] if len(ms) == 1 else None
    pm0 = {p['ref']: p for p in ex['parts']}
    cand = [r for r in res if mz(r['ref']) is not None and not (r['side'] == 'bottom')]
    rot_res = [abs(wrap(r['yaw'] - (r['rot'] - mz(r['ref'])))) for r in res if r['side'] == 'top' and mz(r['ref']) is not None]
    rot_res_neg = [abs(wrap(r['yaw'] + (r['rot'] - mz(r['ref'])))) for r in res if r['side'] == 'top' and mz(r['ref']) is not None]
    rot_bot = [abs(wrap(r['yaw'] - (r['rot'] - mz(r['ref'])))) for r in res if r['side'] == 'bottom' and mz(r['ref']) is not None]
    rot_bot_neg = [abs(wrap(r['yaw'] + (r['rot'] - mz(r['ref'])))) for r in res if r['side'] == 'bottom' and mz(r['ref']) is not None]
    named = {p['ref'] for p in ex['parts']}
    pm = {p['ref']: p for p in ex['parts']}
    exact = [r for r in res if abs(r['dx']) < 1e-3 and abs(r['dz']) < 1e-3]
    offset_nodes = []
    for r in res:
        if r in exact: continue
        offs = [np.hypot(m['offset_mm'][0], m['offset_mm'][1]) for m in pm[r['ref']].get('models', [])]
        mag = float(np.hypot(r['dx'], r['dz']))
        offset_nodes.append({'ref': r['ref'], 'resid_mm': [round(r['dx'], 4), round(r['dz'], 4)], 'resid_magnitude_mm': round(mag, 4),
                             'model_offset_xy_magnitudes_mm': [round(float(o), 4) for o in offs],
                             'explained_by_model_offset': any(abs(mag - o) < 0.01 for o in offs)})
    res_all = res
    res = exact  # map statistics use footprints whose node origin is the footprint origin
    hole_check = check_holes(ex, scene, stem, cx, cy)
    info = {
        'hole_check': hole_check,
        'origin_mm': [cx, cy],
        'matched_footprints': len(res_all), 'exact_origin_footprints': len(res), 'nodes_with_model_offset': offset_nodes,
        'footprints_with_glb_node': sorted(r['ref'] for r in res_all if r['in_final']),
        'footprints_nodes_dropped_empty': sorted(r['ref'] for r in res_all if not r['in_final']),
        'max_abs_dx_mm': max((abs(r['dx']) for r in res), default=0.0),
        'max_abs_dz_mm': max((abs(r['dz']) for r in res), default=0.0),
        'max_abs_final_dxz_mm': max((max(abs(r['final_dx']), abs(r['final_dz'])) for r in res), default=0.0),
        'max_abs_final_dy_mm': max((abs(r['final_dy']) for r in res), default=0.0),
        'top_seat_y_mm': float(np.median(seat_top)) if seat_top else None,
        'bottom_seat_y_mm': float(np.median(seat_bot)) if seat_bot else None,
        'body_min_y_mm': ymin, 'body_max_y_mm': ymax,
        'rot_top_resid_deg': max(rot_res, default=None), 'rot_top_resid_if_negated_deg': max(rot_res_neg, default=None),
        'rot_bottom_resid_deg': max(rot_bot, default=None), 'rot_bottom_resid_if_negated_deg': max(rot_bot_neg, default=None),
        'samples': sorted(res, key=lambda r: -abs(r['dx']) - abs(r['dz']))[:0] or
                   [{k: (round(v, 5) if isinstance(v, float) else v) for k, v in r.items() if k in ('ref', 'side', 'kx', 'ky', 'rot', 'dx', 'dz', 'yaw', 'gy')}
                    for r in sorted(res, key=lambda r: r['ref'])[:0]],
        'footprint_nodes_at_scene_root': sorted(n for n in root_names if n in named),
        'size_bytes': Path(final).stat().st_size,
    }
    # pick explicit verification samples: J1 (rotated), a top-side IC, a bottom-side part if any, plus extremes
    pick = []
    by = {r['ref']: r for r in res}
    for ref in ('J1', 'U9', 'J5'):
        if ref in by: pick.append(by[ref])
    pick += [r for r in res if r['side'] == 'bottom'][:2]
    pick += sorted(res, key=lambda r: -(abs(r['dx']) + abs(r['dz'])))[:1]
    seen = set()
    info['samples'] = []
    for r in pick:
        if r['ref'] in seen: continue
        seen.add(r['ref'])
        info['samples'].append({'ref': r['ref'], 'side': r['side'], 'kicad_xy': [r['kx'], r['ky']], 'kicad_rot': r['rot'],
                                'gltf_x_mm': round(r['dx'] + (r['kx'] - cx), 4), 'gltf_z_mm': round(r['dz'] + (r['ky'] - cy), 4),
                                'gltf_y_mm': round(r['gy'], 4), 'resid_x_mm': round(r['dx'], 5), 'resid_z_mm': round(r['dz'], 5),
                                'gltf_yaw_deg': round(r['yaw'], 3)})
    return info


def check_holes(ex, scene, stem, cx, cy):
    """Independent map check that needs no 3D parts: board-body vertices must lie on the circle of each drilled hole
    when KiCad (x,y) is mapped to glTF (X=(x-cx), Z=(y-cy)); the mirrored-Z mapping is tested as a control."""
    V = []
    for n, g in scene.geometry.items():
        if n.startswith(stem + '_') and 'silkscreen' not in n.lower():
            V.append(np.asarray(g.vertices)[:, [0, 2]] * 1000)
    if not V: return None
    V = np.vstack(V)
    holes = [h for h in ex['holes'] if h['d'] >= 0.7 and h.get('kind') == 'pad' and 'slot' not in h]
    holes += [h for h in ex['holes'] if h['d'] >= 0.7 and h.get('kind') == 'via'][:0]
    chosen = []
    for h in sorted(holes, key=lambda h: (h['x'], h['y'])):
        if not chosen or min(np.hypot(h['x'] - c['x'], h['y'] - c['y']) for c in chosen) > 8:
            chosen.append(h)
        if len(chosen) >= 8: break
    out = []
    for h in chosen:
        r = h['d'] / 2
        def hits(zsign):
            c = np.array([h['x'] - cx, zsign * (h['y'] - cy)])
            d = np.hypot(*(V - c).T)
            return int((abs(d - r) < 0.03).sum())
        out.append({'x': h['x'], 'y': h['y'], 'd': h['d'], 'vertices_on_circle': hits(1), 'vertices_on_circle_if_Z_mirrored': hits(-1)})
    return {'holes_tested': len(out), 'all_match': all(o['vertices_on_circle'] >= 6 for o in out) if out else None, 'detail': out}


def glb_node_check(rev, ex):
    """Every footprint node in the compressed GLB must be a direct child of the scene root (or scene root's single wrapper)."""
    j, _ = glbtools.read_glb(DATA / rev / 'board.glb')
    names = {n.get('name') for n in j['nodes']}
    return names


# ---- layers
LAYER_DEFS = [  # (kicad layer, svg file suffix, kind, side)
    ('F.Cu', 'F_Cu', 'copper', 'top'), ('In1.Cu', 'In1_Cu', 'copper', 'inner'), ('In2.Cu', 'In2_Cu', 'copper', 'inner'),
    ('B.Cu', 'B_Cu', 'copper', 'bottom'),
    ('F.SilkS', 'F_Silkscreen', 'silk', 'top'), ('B.SilkS', 'B_Silkscreen', 'silk', 'bottom'),
    ('F.Mask', 'F_Mask', 'mask', 'top'), ('B.Mask', 'B_Mask', 'mask', 'bottom'),
    ('F.Paste', 'F_Paste', 'paste', 'top'), ('B.Paste', 'B_Paste', 'paste', 'bottom'),
    ('F.Fab', 'F_Fab', 'fab', 'top'), ('B.Fab', 'B_Fab', 'fab', 'bottom'),
    ('Edge.Cuts', 'Edge_Cuts', 'edge', 'top'),
]


def raster_svg(svg_text, vb, w_px, h_px, tmp):
    """Rasterise svg with a replaced viewBox/size to RGBA via rsvg-convert."""
    s = re.sub(r'width="[^"]*mm"\s+height="[^"]*mm"\s+viewBox="[^"]*"',
               f'width="{w_px}px" height="{h_px}px" viewBox="{vb[0]:.4f} {vb[1]:.4f} {vb[2]:.4f} {vb[3]:.4f}" preserveAspectRatio="none"',
               svg_text, count=1)
    tmp.with_suffix('.svg').write_text(s)
    sh(['rsvg-convert', '-f', 'png', '-o', str(tmp.with_suffix('.png')), str(tmp.with_suffix('.svg'))])
    return Image.open(tmp.with_suffix('.png')).convert('RGBA')


def save_la(img, path):
    """Layer PNGs are white with alpha = coverage; store as grey+alpha (L=255), ~18% smaller than RGBA, decodes to white RGBA."""
    a = np.array(img)[..., 3]
    Image.fromarray(np.stack([np.full_like(a, 255), a], -1), 'LA').save(path, optimize=True)


def to_white_alpha(im):
    a = np.array(im)
    alpha = a[..., 3].astype(np.float32)
    if alpha.min() >= 250:  # opaque background: derive coverage from darkness
        alpha = 255 - a[..., :3].mean(axis=2)
    out = np.zeros(a.shape, np.uint8)
    out[..., :3] = 255
    out[..., 3] = np.clip(alpha, 0, 255).astype(np.uint8)
    return Image.fromarray(out, 'RGBA')


def stage_layers(rev, ex, force):
    cdir = CACHE / rev
    pcb = REPO / REVS[rev]['pcb']
    ldir = DATA / rev / 'layers'
    key = sha(pcb, HERE / 'build.py', f'{PPM}'.encode())
    svgdir = cdir / 'svg'
    meta_f = cdir / 'layers.json'
    if fresh(cdir / 'layers.stamp', key, force) and meta_f.exists():
        meta = json.load(open(meta_f))
        # The cache is keyed on the inputs only; a cache reused with a new --out has no PNGs there yet.
        if all((DATA / rev / l['file']).exists() for l in meta['layers']):
            return meta
    log(rev, 'svg export + rasterise layers')
    if svgdir.exists(): shutil.rmtree(svgdir)
    svgdir.mkdir(parents=True)
    names = [d[0] for d in LAYER_DEFS if d[2] != 'copper' or d[0] in ex['copper_layers']]
    kicad_cli('pcb', 'export', 'svg', '--mode-multi', '--layers', ','.join(names), '--page-size-mode', '2',
              '--exclude-drawing-sheet', '--black-and-white',
              *(['--drill-shape-opt', '0'] if rev in ('rev3i', 'rev3j', 'rev3k', 'rev3l', 'rev3m') else []), '-o', svgdir, pcb)
    stem = pcb.stem
    bb = ex['bbox_mm']
    W, H = bb['x1'] - bb['x0'], bb['y1'] - bb['y0']
    wpx, hpx = round(W * PPM), round(H * PPM)
    ppm_x, ppm_y = wpx / W, hpx / H
    # --- calibrate the svg page offset using Edge.Cuts: its outer extent must equal the pcbnew edge bbox
    edge_svg = (svgdir / f'{stem}-Edge_Cuts.svg').read_text()
    m = re.search(r'viewBox="([\d.\-]+) ([\d.\-]+) ([\d.\-]+) ([\d.\-]+)"', edge_svg)
    pw, ph = float(m.group(3)), float(m.group(4))
    CAL = 50  # px/mm for calibration raster
    im = raster_svg(edge_svg, (0, 0, pw, ph), round(pw * CAL), round(ph * CAL), cdir / 'cal')
    al = np.array(im)[..., 3]
    ys, xs = np.nonzero(al > 20)
    ex0, ex1, ey0, ey1 = xs.min() / CAL, (xs.max() + 1) / CAL, ys.min() / CAL, (ys.max() + 1) / CAL
    offx, offy = ex0 - bb['x0'], ey0 - bb['y0']
    cal = {'svg_page_mm': [pw, ph], 'edge_outer_in_svg_mm': [round(ex0, 3), round(ey0, 3), round(ex1, 3), round(ey1, 3)],
           'svg_offset_mm': [round(offx, 3), round(offy, 3)],
           'edge_extent_vs_pcbnew_bbox_mm': [round((ex1 - ex0) - W, 3), round((ey1 - ey0) - H, 3)]}
    vb = (bb['x0'] + offx, bb['y0'] + offy, W, H)
    ldir.mkdir(parents=True, exist_ok=True)
    for f in ldir.glob('*.png'): f.unlink()
    layers = []
    copper = ex['copper_layers']  # bottom-up order via CuStack is top->bottom
    T = ex['thickness_mm']
    ncu = len(copper)
    def z_of(name, kind, side):
        if kind == 'copper':
            i = copper.index(name)  # 0 = F.Cu
            return round(T * (1 - i / (ncu - 1)), 4) if ncu > 1 else T
        if kind in ('edge',): return round(T / 2, 4)
        return T if side == 'top' else 0.0
    order_seq = ['B.Fab', 'B.SilkS', 'B.Mask', 'B.Paste', 'B.Cu'] + list(reversed(copper[1:-1])) + ['F.Cu', 'F.Paste', 'F.Mask', 'F.SilkS', 'F.Fab', 'Edge.Cuts']
    for name, suf, kind, side in LAYER_DEFS:
        f = svgdir / f'{stem}-{suf}.svg'
        if not f.exists(): continue
        img = to_white_alpha(raster_svg(f.read_text(), vb, wpx, hpx, cdir / 'tmp'))
        if np.array(img)[..., 3].max() == 0:
            log(rev, f'  layer {name} is empty, skipped')
            continue
        save_la(img, ldir / f'{name}.png')
        layers.append({'name': name, 'file': f'layers/{name}.png', 'kind': kind, 'side': side, 'px_per_mm': round(ppm_x, 4),
                       'bbox_mm': [bb['x0'], bb['y0'], bb['x1'], bb['y1']], 'z_mm': z_of(name, kind, side), '_o': order_seq.index(name)})
    # drills drawn from pcbnew geometry (same frame)
    for plated, nm in ((True, 'Drill_PTH'), (False, 'Drill_NPTH')):
        hs = [h for h in ex['holes'] if h['plated'] == plated]
        if not hs: continue
        big = Image.new('L', (wpx * 4, hpx * 4), 0)
        dr = ImageDraw.Draw(big)
        for h in hs:
            px, py = (h['x'] - bb['x0']) * ppm_x * 4, (h['y'] - bb['y0']) * ppm_y * 4
            sx, sy = h.get('slot', [h['d'], h['d']])
            if h.get('orient', 0) % 180 == 90: sx, sy = sy, sx
            rx, ry = sx / 2 * ppm_x * 4, sy / 2 * ppm_y * 4
            if abs(sx - sy) < 1e-3:
                dr.ellipse([px - rx, py - ry, px + rx, py + ry], fill=255)
            else:
                dr.rounded_rectangle([px - rx, py - ry, px + rx, py + ry], radius=min(rx, ry), fill=255)
        a = np.array(big.resize((wpx, hpx), Image.LANCZOS))
        out = np.zeros((hpx, wpx, 4), np.uint8); out[..., :3] = 255; out[..., 3] = a
        save_la(Image.fromarray(out, 'RGBA'), ldir / f'{nm}.png')
        layers.append({'name': nm, 'file': f'layers/{nm}.png', 'kind': 'drill', 'side': 'top', 'px_per_mm': round(ppm_x, 4),
                       'bbox_mm': [bb['x0'], bb['y0'], bb['x1'], bb['y1']], 'z_mm': round(T / 2, 4), '_o': len(order_seq)})
    layers.sort(key=lambda l: l['_o'])
    for i, l in enumerate(layers):
        l['order'] = i
        del l['_o']
    meta = {'layers': layers, 'calibration': cal, 'size_px': [wpx, hpx]}
    meta['alignment'] = check_alignment(rev, ex, layers, ldir, bb, ppm_x, ppm_y, wpx, hpx)
    jwrite(meta_f, meta)
    (cdir / 'layers.stamp').write_text(key)
    return meta


def check_alignment(rev, ex, layers, ldir, bb, ppm_x, ppm_y, wpx, hpx):
    res = {}
    edge = np.array(Image.open(ldir / 'Edge.Cuts.png').convert('RGBA'))[..., 3] > 20
    ys, xs = np.nonzero(edge)
    res['edge_px_bbox'] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
    res['edge_touches_all_borders'] = bool(xs.min() <= 1 and ys.min() <= 1 and xs.max() >= wpx - 2 and ys.max() >= hpx - 2)
    # pad probes: find best shift of a synthetic pad-shaped mask against F.Mask openings
    probes, results = ex.get('pad_probes', []), []
    mask_f = ldir / 'F.Mask.png'
    if mask_f.exists():
        mk = np.array(Image.open(mask_f).convert('RGBA'))[..., 3] > 127
        for pr in probes:
            if pr['side'] != 'top': continue
            cxp, cyp = (pr['x'] - bb['x0']) * ppm_x, (pr['y'] - bb['y0']) * ppm_y
            sx, sy = pr['w'] * ppm_x, pr['h'] * ppm_y
            R = 8
            x0, y0 = int(cxp) - int(sx / 2) - R - 3, int(cyp) - int(sy / 2) - R - 3
            x1, y1 = int(cxp) + int(sx / 2) + R + 4, int(cyp) + int(sy / 2) + R + 4
            if x0 < 0 or y0 < 0 or x1 >= wpx or y1 >= hpx: continue
            win = mk[y0:y1, x0:x1]
            yy, xx = np.mgrid[y0:y1, x0:x1]
            best = None
            for dy in range(-R, R + 1):
                for dx in range(-R, R + 1):
                    px, py = cxp + dx + 0.5, cyp + dy + 0.5
                    if pr['shape'] == 'circle':
                        syn = ((xx + 0.5 - px) / (sx / 2)) ** 2 + ((yy + 0.5 - py) / (sy / 2)) ** 2 <= 1
                    else:
                        syn = (abs(xx + 0.5 - px) <= sx / 2) & (abs(yy + 0.5 - py) <= sy / 2)
                    inter = (syn & win).sum(); uni = (syn | win).sum()
                    score = inter / uni if uni else 0
                    if best is None or score > best[0]: best = (score, dx, dy)
            results.append({'ref': pr['ref'], 'pad': pr['pad'], 'expected_px': [round(cxp, 1), round(cyp, 1)], 'best_shift_px': [best[1], best[2]], 'iou': round(best[0], 3)})
    res['pad_probes'] = results
    res['max_abs_shift_px'] = max((max(abs(r['best_shift_px'][0]), abs(r['best_shift_px'][1])) for r in results), default=None)
    return res


def stage_renders(rev, ex, force):
    cdir = CACHE / rev
    pcb = REPO / REVS[rev]['pcb']
    rdir = DATA / rev / 'renders'
    key = sha(pcb)
    if fresh(cdir / 'render.stamp', key, force) and (rdir / 'top.png').exists():
        return True
    log(rev, 'kicad-cli pcb render (basic quality, top+bottom)')
    rdir.mkdir(parents=True, exist_ok=True)
    bb = ex['bbox_mm']
    w, h = bb['x1'] - bb['x0'], bb['y1'] - bb['y0']
    H = int(1600 * h / w) + 200
    def render(side, zoom, raw):
        kicad_cli('pcb', 'render', '--side', side, '--width', 1600, '--height', H, '--quality', 'basic',
                  '--background', 'transparent', '--zoom', zoom, '-o', raw, pcb)
        return Image.open(raw).convert('RGBA')
    for side in ('top', 'bottom'):
        raw = cdir / f'render-{side}.png'
        # zoom 1 render only to measure how big the board is in frame, then re-render so it fills ~94% of the canvas
        im0 = render(side, 1, raw)
        b0 = im0.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
        zoom = round(min(0.94 * im0.width / (b0[2] - b0[0]), 0.94 * im0.height / (b0[3] - b0[1])), 3) if b0 else 1
        im = render(side, zoom, raw)
        box = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
        if box:
            pad = 16
            im = im.crop((max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad)))
        im.save(rdir / f'{side}.png', optimize=True)
    (cdir / 'render.stamp').write_text(key)
    return True


def stage_sch(rev, force):
    sch = REVS[rev].get('sch')
    sdir = DATA / rev / 'sch'
    if not sch or not (REPO / sch).exists():
        return None
    cdir = CACHE / rev
    key = sha(REPO / sch)
    if fresh(cdir / 'sch.stamp', key, force) and (sdir / 'index.json').exists():
        return json.load(open(sdir / 'index.json'))
    log(rev, 'sch export svg')
    tmp = cdir / 'schsvg'
    if tmp.exists(): shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    kicad_cli('sch', 'export', 'svg', '--black-and-white', '--no-background-color', '--exclude-drawing-sheet', '-o', tmp, REPO / sch)
    files = sorted(tmp.glob('*.svg'))
    root_stem = (REPO / sch).stem
    files.sort(key=lambda f: (f.stem != root_stem, f.name))
    if sdir.exists(): shutil.rmtree(sdir)
    sdir.mkdir(parents=True)
    idx = []
    for i, f in enumerate(files, 1):
        shutil.copy(f, sdir / f'sheet-{i}.svg')
        t = f.stem[len(root_stem) + 1:] if f.stem.startswith(root_stem + '-') else ('Root sheet' if f.stem == root_stem else f.stem)
        idx.append({'file': f'sheet-{i}.svg', 'title': t.replace('_', ' ')})
    jwrite(sdir / 'index.json', idx)
    (cdir / 'sch.stamp').write_text(key)
    return idx


def stage_parts(rev, ex, glb_info, force):
    cdir = CACHE / rev
    bom = read_bom(rev)
    bom_by_ref = {r['ref']: r for r in bom} if bom else {}
    nl = netlist_fields(rev, cdir)
    nodes = set(glb_info['footprints_with_glb_node']) if glb_info else set()
    parts = []
    consumed = {'Reference', 'Value', 'Footprint', 'Datasheet', 'Description', 'LCSC', 'LCSC Part #', 'LCSC Part', 'MPN',
                'Manufacturer', 'Manufacturer_Part_Number', 'Mfr. Part #'}
    for p in ex['parts']:
        f = {}
        n = nl.get(p['ref'], {})
        for k, v in n.items():
            if not k.startswith('_') and v not in ('', None): f[k] = v
        for k, v in p['fields'].items():
            if v not in ('', None): f[k] = v
        b = bom_by_ref.get(p['ref'])
        def pick(*keys):
            for k in keys:
                if f.get(k): return f[k]
            return ''
        lcsc, lsrc = pick('LCSC', 'LCSC Part #', 'LCSC Part'), 'pcb/schematic field'
        if not lcsc and b and b['lcsc']: lcsc, lsrc = b['lcsc'], 'manufacturing BOM'
        if not lcsc: lsrc = None
        desc = pick('Description') or n.get('_description', '')
        ds = pick('Datasheet') or n.get('_datasheet', '')
        parts.append({
            'ref': p['ref'], 'value': p['value'] or n.get('_value', ''), 'footprint': p['footprint'], 'side': p['side'],
            'x': p['x'], 'y': p['y'], 'rot': p['rot'], 'bbox_mm': p['bbox_mm'], 'bbox_source': p['bbox_source'],
            'lcsc': lcsc or None, 'lcsc_source': lsrc, 'mpn': pick('MPN', 'Manufacturer_Part_Number', 'Mfr. Part #') or None,
            'manufacturer': pick('Manufacturer') or None, 'description': desc, 'datasheet': '' if ds == '~' else ds,
            'dnp': p['dnp'] or bool(b and b.get('dnp')), 'in_bom': p['in_bom'],
            'assembled': bool(b) and p['ref'] in bom_by_ref,
            'has_3d_model_ref': p['has_3d_model'], 'glb_node': p['ref'] in nodes,
            'fields': {k: v for k, v in f.items() if k not in consumed},
            'pads': p['pads'],
        })
    parts.sort(key=lambda q: (re.sub(r'\d+', '', q['ref']), int(re.sub(r'\D', '', q['ref']) or 0)))
    jwrite(DATA / rev / 'parts.json', parts)
    return parts


def write_board_json(rev, ex, glb_info, layer_meta):
    bb = ex['bbox_mm']
    cx, cy = glb_info['origin_mm']
    T = ex['thickness_mm']
    holes = [{k: v for k, v in h.items() if k != 'orient' or True} for h in ex['holes']]
    glb = {
        'file': 'board.glb', 'scale_to_mm': 1000, 'origin_mm': [cx, cy], 'kicad_y_to': '+Z',
        'board_bottom_y_mm': 0.0, 'board_top_y_mm': T,
        'parts_seat_top_y_mm': round(glb_info['top_seat_y_mm'], 4) if glb_info['top_seat_y_mm'] is not None else None,
        'parts_seat_bottom_y_mm': round(glb_info['bottom_seat_y_mm'], 4) if glb_info['bottom_seat_y_mm'] is not None else None,
        'body_extent_y_mm': [round(glb_info['body_min_y_mm'], 4), round(glb_info['body_max_y_mm'], 4)] if glb_info['body_min_y_mm'] is not None else None,
        'map': (f'glTF units are metres (scale_to_mm=1000). X = (kx - {cx})/1000, Z = (ky - {cy})/1000 (KiCad +Y, which points down the '
                f'board when viewed from the top, maps to +Z), Y is up: 0 at the board bottom face, {T} mm at the top face (top-side parts '
                f'seat at about {round(glb_info["top_seat_y_mm"], 3) if glb_info["top_seat_y_mm"] is not None else T} mm, bottom-side parts hang below 0). '
                f'Footprint nodes sit directly under the scene root node; node translation = footprint origin; rotation is about +Y '
                f'(yaw = {"KiCad rot" if (glb_info["rot_top_resid_deg"] or 0) <= (glb_info["rot_top_resid_if_negated_deg"] or 0) else "-KiCad rot"} for top-side parts).'),
        'rotation_sign_top': 1 if (glb_info['rot_top_resid_deg'] or 0) <= (glb_info['rot_top_resid_if_negated_deg'] or 0) else -1,
        'verification': {k: glb_info[k] for k in ('matched_footprints', 'exact_origin_footprints', 'nodes_with_model_offset', 'max_abs_dx_mm', 'max_abs_dz_mm', 'max_abs_final_dxz_mm',
                                                  'max_abs_final_dy_mm', 'rot_top_resid_deg', 'rot_bottom_resid_deg', 'samples', 'hole_check')},
    }
    board = {'id': rev, 'bbox_mm': bb, 'thickness_mm': T, 'copper_layers': ex['copper_layers'], 'outline': ex['outline'],
             'holes': holes, 'glb': glb, 'layers': layer_meta['layers'],
             'png_alignment': {'calibration': layer_meta['calibration'], 'check': layer_meta['alignment']}}
    jwrite(DATA / rev / 'board.json', board)
    return board


# --------------------------------------------------------------------------- cost
JLC_API = 'https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList'


def jlc_lookup(code, refresh):
    import urllib.request
    cf = CACHE / 'jlc' / f'{code}.json'
    if cf.exists() and not refresh:
        return json.load(open(cf))
    req = urllib.request.Request(JLC_API, data=json.dumps({"keyword": code, "currentPage": 1, "pageSize": 5}).encode(),
                                 headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
    found = None
    for attempt in range(3):
        try:
            data = json.load(urllib.request.urlopen(req, timeout=30))
            for x in (data['data']['componentPageInfo']['list'] or []):
                if x['componentCode'] == code:
                    found = x
            break
        except Exception as e:  # noqa
            if attempt == 2: raise
            time.sleep(2)
    rec = {'captured': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), 'item': found}
    cf.parent.mkdir(parents=True, exist_ok=True)
    cf.write_text(json.dumps(rec))
    time.sleep(0.3)
    return rec


def unit_price(x, qty):
    best = None
    for p in x.get('componentPrices') or []:
        if qty >= p['startNumber']: best = p['productPrice']
    return best if best is not None else ((x.get('componentPrices') or [{}])[0].get('productPrice') or 0)


def stage_cost(rev, refresh, parts=None):
    spec = REVS[rev]
    out = DATA / rev / 'cost.json'
    boards = [5, 10]
    quotes = spec.get('documented_quotes', [])
    bom = read_bom(rev)
    if bom is None:
        cost = {'captured': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), 'source': None, 'boards': boards,
                'lines': [], 'totals': {'parts': {'5': None, '10': None}, 'unique': 0, 'extended': 0, 'assembled_refs': 0},
                'documented_quotes': quotes,
                'note': 'No BOM/CPL exists for this revision (only a Gerber archive is in the repo), so no priced lines can be produced.'}
        jwrite(out, cost)
        return cost
    log(rev, f'cost: JLC lookups for {len({r["lcsc"] for r in bom if r["lcsc"]})} codes')
    by = {}
    for r in bom:
        by.setdefault(r['lcsc'], []).append(r)
    lines, captured = [], []
    for code, rows in by.items():
        refs = [r['ref'] for r in rows]
        n = len(refs)
        line = {'lcsc': code or None, 'mpn': None, 'class': None, 'stock': None, 'qty_per_board': n, 'refs': refs,
                'unit_price': {'5': None, '10': None}, 'line_total': {'5': None, '10': None}, 'problem': None,
                'comment': rows[0]['comment'], 'footprint': rows[0]['footprint'], 'description': None}
        if not code:
            line['problem'] = 'no LCSC part number in BOM'
            lines.append(line); continue
        rec = jlc_lookup(code, refresh)
        captured.append(rec['captured'])
        x = rec['item']
        if not x:
            line['problem'] = 'NOT FOUND in JLCPCB parts search'
            lines.append(line); continue
        lib = x.get('componentLibraryType')
        line['mpn'] = x.get('componentModelEn')
        line['description'] = x.get('describe') or x.get('componentSpecificationEn')
        line['class'] = 'basic' if lib == 'base' else ('preferred' if x.get('preferredComponentFlag') else 'extended')
        line['stock'] = x.get('stockCount') or 0
        for b in boards:
            up = unit_price(x, n * b)
            line['unit_price'][str(b)] = round(up, 5)
            line['line_total'][str(b)] = round(up * n * b, 4)
        need = n * max(boards)
        if line['stock'] == 0: line['problem'] = 'out of stock'
        elif line['stock'] < max(200, need): line['problem'] = f'low stock ({line["stock"]}, need {need} for 10 boards)'
        lines.append(line)
    lines.sort(key=lambda l: (l['refs'][0][0], int(re.sub(r'\D', '', l['refs'][0]) or 0)))
    cost = {'captured': max(captured) if captured else None, 'source': 'JLCPCB public parts search (selectSmtComponentList), list-price tier for boards x qty_per_board; price cache in build/cache/jlc',
            'boards': boards, 'lines': lines,
            'totals': {'parts': {str(b): round(sum(l['line_total'][str(b)] or 0 for l in lines), 2) for b in boards},
                       'unique': len([l for l in lines if l['lcsc']]),
                       'extended': len([l for l in lines if l['class'] in ('extended', 'preferred')]),
                       'extended_fee_applies': len([l for l in lines if l['class'] == 'extended']),
                       'preferred': len([l for l in lines if l['class'] == 'preferred']),
                       'assembled_refs': len(bom), 'problems': len([l for l in lines if l['problem']])},
            'documented_quotes': quotes,
            'notes': ['totals.extended counts every non-basic unique code (same definition as tools/jlc_bom_check.py); totals.extended_fee_applies excludes JLC "preferred" parts.',
                      'Line prices are list-price tiers; JLCPCB buys extras for small parts, so real quotes differ (see documented_quotes).']}
    jwrite(out, cost)
    return cost


# --------------------------------------------------------------------------- index
def build_index(revs):
    out = []
    for r in CFG['revisions']:
        rid = r['id']
        d = DATA / rid
        if not (d / 'board.json').exists():
            continue
        board = json.load(open(d / 'board.json'))
        parts = json.load(open(d / 'parts.json'))
        cost = json.load(open(d / 'cost.json')) if (d / 'cost.json').exists() else None
        bb = board['bbox_mm']
        commit = subprocess.run(['git', '-C', str(REPO), 'log', '-1', '--format=%h', '--', str(Path(r['pcb']).parent)], capture_output=True, text=True).stdout.strip()
        uniq = cost['totals']['unique'] if cost and cost['lines'] else None
        size_mm = [round(bb['x1'] - bb['x0'], 2), round(bb['y1'] - bb['y0'], 2)]
        if rid in ('rev3i', 'rev3j', 'rev3k', 'rev3l', 'rev3m'):
            # Drawing strokes extend beyond the nominal mechanical profile.
            size_mm = np.ptp(np.asarray(board['outline'][0]), axis=0).round(4).tolist()
            uniq = len({p['lcsc'] for p in parts if p['assembled'] and p['lcsc']})
        out.append({
            'id': rid, 'label': r['label'], 'status': r['status'], 'date': r['date'], 'date_basis': r.get('date_basis'),
            'summary': r['summary'], 'commit': commit,
            **({'source_url': r['source_url']} if r.get('source_url') else {}),
            **({'asset_revision': hashlib.sha256((REPO / r['pcb']).read_bytes()).hexdigest()[:12]}
               if rid in ('rev3l', 'rev3m') else {}),
            'commit_basis': 'last commit touching the revision design/ folder',
            'layers': board['copper_layers'].__len__(), 'size_mm': size_mm,
            'thickness_mm': board['thickness_mm'], 'parts_total': len(parts), 'parts_assembled': sum(1 for p in parts if p['assembled']),
            'unique_lcsc': uniq, 'extended': cost['totals']['extended'] if cost and cost['lines'] else None,
            'case': r['case'], 'readme': r['readme'] and f'repo/{r["readme"]}',
            'has': {'glb': (d / 'board.glb').exists(), 'layers': (d / 'layers').exists(), 'sch': (d / 'sch' / 'index.json').exists(),
                    'cost': bool(cost and cost['lines']), 'renders': (d / 'renders' / 'top.png').exists()},
        })
    jwrite(DATA / 'revisions.json', out, indent=1)
    return out


def do_rev(rev, args):
    """pcb assets for one revision (a single failure should not stop the others)."""
    t0 = time.time()
    force = args.force
    ex = stage_extract(rev, force)
    info = stage_glb(rev, ex, force)
    lm = stage_layers(rev, ex, force)
    write_board_json(rev, ex, info, lm)
    stage_parts(rev, ex, info, force)
    stage_sch(rev, force)
    stage_renders(rev, ex, force)
    log(rev, f'done in {time.time() - t0:.0f}s: {info["matched_footprints"]} glb footprints, max resid {info["max_abs_dx_mm"]:.4f}/{info["max_abs_dz_mm"]:.4f} mm, '
             f'glb {info["size_bytes"] / 1e6:.2f} MB, png shift {lm["alignment"]["max_abs_shift_px"]} px')
    return info


def assemble_site():
    """Make SITE a complete static site: the viewer and the two hand-edited data files come from tools/review-hub/site."""
    src = hubenv.HUB / 'site'
    (DATA).mkdir(parents=True, exist_ok=True)
    if SITE.resolve() == src.resolve():
        return
    shutil.copy2(src / 'index.html', SITE / 'index.html')
    for name in ('pricing.json', 'updates.json'):
        shutil.copy2(src / 'data' / name, DATA / name)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--rev', action='append', help='only this revision id (repeatable)')
    ap.add_argument('--cases', action='store_true', help='build case GLBs only')
    ap.add_argument('--docs', action='store_true', help='mirror docs only')
    ap.add_argument('--cost', action='store_true', help='cost.json only')
    ap.add_argument('--refresh', action='store_true', help='re-query JLCPCB (otherwise cached responses are reused)')
    ap.add_argument('--fetch-models', action='store_true', help='download missing KiCad 3D models (kicad-packages3D 9.0.0) into build/cache/packages3D')
    ap.add_argument('--force', action='store_true', help='ignore stage caches')
    ap.add_argument('--jobs', type=int, default=3)
    ap.add_argument('--out', help=f'site directory to build into (default {hubenv.HUB / "site"}); index.html and the hand-edited data files are copied in')
    ap.add_argument('--cache', help=f'build cache directory (default {HERE / "cache"})')
    args = ap.parse_args()
    hubenv.require_tools('docker', 'node', 'rsvg-convert')
    hubenv.ensure_node()
    only = (args.cases or args.docs or args.cost)
    revs = args.rev or [r['id'] for r in CFG['revisions']]
    for r in revs:
        if r not in REVS: sys.exit(f'unknown revision {r}')
    assemble_site()
    CACHE.mkdir(parents=True, exist_ok=True)
    if args.fetch_models or not (PKG3D / 'MANIFEST.json').exists():
        if not args.fetch_models:
            print('note: build/cache/packages3D is empty; GLBs will only contain project-local models. Use --fetch-models.')
            PKG3D.mkdir(parents=True, exist_ok=True)
        else:
            import models
            mf = models.fetch(REPO, [r['pcb'] for r in CFG['revisions']], PKG3D, CFG.get('ca_bundle'))
            print(f"models: {mf['total_files']} files, {mf['total_bytes']} bytes, missing upstream: {mf['missing_upstream']}")
    if not only:
        from concurrent.futures import ThreadPoolExecutor
        infos = {}
        with ThreadPoolExecutor(max_workers=args.jobs) as ex_:
            futs = {r: ex_.submit(do_rev, r, args) for r in revs}
            for r, f in futs.items():
                try: infos[r] = f.result()
                except Exception as e:  # noqa
                    print(f'[{r}] FAILED: {e}', file=sys.stderr)
    if not args.cases and not args.docs:
        for r in revs:
            if (DATA / r).exists():
                stage_cost(r, args.refresh)
    full = not only and not args.rev
    if args.docs or full:
        import docs_mirror
        docs_mirror.run(CFG, SITE)
    if args.cases or full:
        import cases_build
        cases_build.run(CFG, SITE, DATA, sys.modules[__name__])
    build_index(revs)
    print('revisions.json written')
    import publish_prep  # artifacts don't serve .glb or SVGs with a DOCTYPE
    g, s = publish_prep.run(SITE)
    print(f'{g} .glb mirrored to .gltf.json, {s} SVG DOCTYPEs stripped')


if __name__ == '__main__':
    main()
