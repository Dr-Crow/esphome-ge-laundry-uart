"""Case GLBs: the Rev3D case (Rev3C enclosure, flush USB-C port) in four lid variants via export_review.py, plus rev2 (STLs).

STL -> GLB with trimesh (mm -> m, case CAD axes kept untouched), then meshopt via optimize_glb.mjs.
Board placement for the Rev3C case is derived from interface_baseline.py and verified geometrically."""
import hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

import numpy as np
import trimesh

import hubenv

HERE = Path(__file__).resolve().parent
CACHE = hubenv.CACHE


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sh(cmd, **kw):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if r.returncode:
        raise RuntimeError(f'{cmd}\n{r.stdout[-1200:]}\n{r.stderr[-1200:]}')
    return r.stdout


def stl_to_glb(stl, out, name):
    m = trimesh.load(str(stl), force='mesh')
    m.merge_vertices()
    m.apply_scale(0.001)  # mm -> m, same unit as the board GLB
    tmp = CACHE / 'case-tmp'
    tmp.mkdir(exist_ok=True)
    raw = tmp / f'{name}.glb'
    sc = trimesh.Scene()
    sc.add_geometry(m, node_name=name, geom_name=name)
    raw.write_bytes(sc.export(file_type='glb'))
    out.parent.mkdir(parents=True, exist_ok=True)
    sh(['node', HERE / 'optimize_glb.mjs', raw, out], cwd=HERE)
    return trimesh.load(str(stl), force='mesh')  # mm mesh for checks


def gcode_info(g, repo=None):
    if not Path(g).exists():
        return None
    t = Path(g).read_text(errors='ignore')
    def grab(pat):
        m = re.search(pat, t)
        return m.group(1).strip() if m else None
    mm = grab(r'; filament used \[mm\] = ([\d.]+)')
    return {'time': grab(r'; estimated printing time \(normal mode\) = (.+)'),
            'filament_m': round(float(mm) / 1000, 3) if mm else None,
            'filament_cm3': float(grab(r'; filament used \[cm3\] = ([\d.]+)') or 0) or None,
            'grams': (lambda v: round(float(v), 1) if v and float(v) > 0 else None)(grab(r'; (?:total )?filament used \[g\] = ([\d.]+)')),
            'source': hubenv.display_path(g, repo or hubenv.HUB.parent.parent)}


# Optional: without a slicer the case parts simply carry no print estimate. Set HUB_PRUSASLICER to override.
SLICER = Path(os.environ.get('HUB_PRUSASLICER') or shutil.which('prusa-slicer') or '/Applications/PrusaSlicer.app/Contents/MacOS/PrusaSlicer')
SLICE_ARGS = ['--layer-height', '0.2', '--first-layer-height', '0.35', '--perimeters', '3', '--top-solid-layers', '3',
              '--bottom-solid-layers', '3', '--fill-density', '20%', '--fill-pattern', 'stars', '--support-material',
              '--support-material-auto', '--nozzle-diameter', '0.4', '--filament-diameter', '1.75', '--filament-type', 'PLA',
              '--filament-density', '1.24']  # same settings as the 2026-11-22 slices, plus PLA density so grams are reported


def slice_stl(stl, gcode):
    """PrusaSlicer CLI (generic 0.4 mm nozzle, PLA 20% stars, auto supports). Returns gcode_info or None if no slicer."""
    if not SLICER.exists():
        return None
    gcode.parent.mkdir(parents=True, exist_ok=True)
    stamp = gcode.with_suffix('.stamp')
    key = hashlib.sha256(Path(stl).read_bytes() + ' '.join(SLICE_ARGS).encode()).hexdigest()
    if not (gcode.exists() and stamp.exists() and stamp.read_text() == key):  # the slicer is slow; reuse unchanged STLs
        sh([SLICER, '--export-gcode', *SLICE_ARGS, '--output', gcode, stl])
        stamp.write_text(key)
    return gcode_info(gcode)


def run_c6(cfg, src):
    """Run the documented export_review.py for C6. Parameter provenance is recorded in the returned dict."""
    work = CACHE / 'case-src' / 'analytical'
    if work.exists(): shutil.rmtree(work)
    work.mkdir(parents=True)
    for f in list(src.glob('*.py')) + list(src.glob('*.json')):
        shutil.copy2(f, work / f.name)
    out = CACHE / 'exports-review-c6'
    if out.exists(): shutil.rmtree(out)
    params = dict(module='c6', antenna='internal', stack=11.325, boot_height=0.53, reset_height=0.53, boot_stop=0.36,
                  reset_stop=0.36, gap=0.25, leaf_offset=16.6, relieved_guides=True)
    cmd = [hubenv.cad_python(cfg), 'export_review.py', '--module', 'c6', '--antenna', 'internal', '--stack', '11.325',
           '--boot-height', '0.53', '--reset-height', '0.53', '--boot-stop', '0.36', '--reset-stop', '0.36',
           '--leaf-offset', '16.6', '--relieved-guides', '--output', out]
    sh(cmd, cwd=work)
    return out, params, cmd


def run_export(cfg, src, module, antenna, argv, tag):
    """Run the repo's export_review.py (from a copy, so the repo stays untouched) with explicit arguments."""
    work = CACHE / 'case-src' / 'analytical'
    if work.exists(): shutil.rmtree(work)
    work.mkdir(parents=True)
    for f in list(src.glob('*.py')) + list(src.glob('*.json')):
        shutil.copy2(f, work / f.name)
    out = CACHE / f'exports-review-{tag}'
    if out.exists(): shutil.rmtree(out)
    cmd = [hubenv.cad_python(cfg), 'export_review.py', '--module', module, '--antenna', antenna, *argv, '--output', out]
    sh(cmd, cwd=work)
    return out, cmd


def rpsma_proxies(out_dir):
    """Reference hardware for the external lid, in the physical case frame (mm, z up), from CASE-ANALYSIS.md:
    D-flat hole 6.5 mm at x 56 / z 15.5 through a 1.5 mm land (physical y -4.4..-2.9), 12 mm nut recess outside.
    RP-SMA bulkhead jack (1/4-36 thread), AF8 x 1.6 nut, 10.2 x 0.5 washer, and a 120 mm half-wave dipole
    (max 10.7 mm) screwed on straight out, as in the original concept render. Not printed parts."""
    def cyl_y(r, y0, y1, sections=40):
        m = trimesh.creation.cylinder(radius=r, height=abs(y1 - y0), sections=sections)
        m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
        m.apply_translation([56.0, (y0 + y1) / 2, 15.5]); return m
    hw = trimesh.util.concatenate([cyl_y(3.175, 1.4, -11.0),          # jack body + thread through the land
                                   cyl_y(5.1, -4.4, -4.9),            # washer OD 10.2 x 0.5 on the land
                                   cyl_y(4.62, -4.9, -6.5, sections=6)])  # AF8 hex nut (circumradius 4.62) x 1.6
    whip = trimesh.util.concatenate([cyl_y(4.6, -6.5, -16.5),          # knurled RP-SMA coupling
                                     cyl_y(5.35, -16.5, -34.0),        # knuckle / base, 10.7 mm max
                                     cyl_y(4.2, -34.0, -124.0),        # radome
                                     cyl_y(3.2, -124.0, -126.5)])      # tip
    # Tilt-swivel version: same coupling, a hinge 8 mm past it, then the radome turned 90 deg to point straight up
    # (typical 2.4 GHz RP-SMA swivel dipole, ~120 mm overall). Hinge axis is parallel to x.
    HINGE_Y, HINGE_Z, UP = -24.0, 15.5, 92.0
    def cyl_z(r, z0, z1, y, sections=40):
        m = trimesh.creation.cylinder(radius=r, height=z1 - z0, sections=sections)
        m.apply_translation([56.0, y, (z0 + z1) / 2]); return m
    knuckle = trimesh.creation.icosphere(subdivisions=3, radius=5.6); knuckle.apply_translation([56.0, HINGE_Y, HINGE_Z])
    swivel = trimesh.util.concatenate([cyl_y(4.6, -6.5, -16.5), cyl_y(5.35, -16.5, HINGE_Y), knuckle,
                                       cyl_z(5.0, HINGE_Z, HINGE_Z + 12.0, HINGE_Y), cyl_z(4.2, HINGE_Z + 12.0, HINGE_Z + UP, HINGE_Y),
                                       cyl_z(3.2, HINGE_Z + UP, HINGE_Z + UP + 2.5, HINGE_Y)])
    files = {}
    for name, mesh in (('proxy_rpsma_bulkhead', hw), ('proxy_dipole_120mm', whip), ('proxy_dipole_swivel_up', swivel)):
        stl = CACHE / 'case-tmp' / f'{name}.stl'; stl.parent.mkdir(exist_ok=True); mesh.export(stl)
        # same physical frame as the exported case STLs
        files[name] = stl
    return files


def point_in(mesh, pts):
    return mesh.contains(np.asarray(pts, float))


CASE_CY = 20.0  # enclosure.py CY: the mirror line between KiCad (y down) and physical case coordinates


def placement_check(base, lid, ex_rev3d, seat_z, pcb_t, cx, cy):
    """Does the board, placed by case=(kx, ky, z), fit the cavity? Counts sample points that fall inside printed solid."""
    parts = {p['ref']: p for p in ex_rev3d['parts']}
    def box_pts(b, z0, z1, n=5):
        xs = np.linspace(b[0] + 0.3, b[2] - 0.3, n); ys = np.linspace(b[1] + 0.3, b[3] - 0.3, n); zs = np.linspace(z0, z1, 3)
        return np.array([[x, y, z] for x in xs for y in ys for z in zs])
    top = seat_z + pcb_t
    groups = {
        'J1 RJ45 body (z top+0.5..top+8)': box_pts(parts['J1']['bbox_mm'], top + 0.5, top + 8),
        'J5 socket row (z top+0.5..top+7)': box_pts(parts['J5']['bbox_mm'], top + 0.5, top + 7),
        'J6 socket row (z top+0.5..top+7)': box_pts(parts['J6']['bbox_mm'], top + 0.5, top + 7),
    }
    # board plate interior (between standoffs): coarse grid over the outline, mid-board height
    bb = ex_rev3d['bbox_mm']
    xs = np.linspace(bb['x0'] + 2, bb['x1'] - 2, 40); ys = np.linspace(bb['y0'] + 2, bb['y1'] - 2, 16)
    groups['board plate (z mid-board, grid 40x16)'] = np.array([[x, y, seat_z + pcb_t / 2] for x in xs for y in ys])
    res = {}
    def count(ymap):
        out = {}
        for k, pts in groups.items():
            p2 = pts.copy(); p2[:, 1] = ymap(p2[:, 1])
            inside = point_in(base, p2) | point_in(lid, p2)
            out[k] = {'points': len(pts), 'inside_solid': int(inside.sum())}
        return out
    # Since the 2026-11-23 frame fix, exports are physical: case y = 2*CY - KiCad y (CY = 20, board centreline).
    res['placement_y_equals_40_minus_ky'] = count(lambda y: 2 * CASE_CY - y)
    res['control_old_convention_y_equals_ky'] = count(lambda y: y)
    allb = trimesh.util.concatenate([base, lid]).bounds
    res['case_bounds_mm'] = allb.round(3).tolist()
    corners = np.array([[bb['x0'], bb['y0']], [bb['x1'], bb['y1']]])
    res['board_bbox_inside_case_xy'] = bool(allb[0][0] < bb['x0'] and allb[1][0] > bb['x1'] and allb[0][1] < bb['y0'] and allb[1][1] > bb['y1'])
    res['board_z_range_mm'] = [seat_z, top]
    return res


def run(CFG, SITE, DATA, exporter=None):
    repo = Path(CFG['repo'])
    ana = repo / 'case' / 'rev3c' / 'analytical'
    cases_dir = DATA / 'cases'
    if cases_dir.exists(): shutil.rmtree(cases_dir)
    cases = []

    # ---- board frame facts (from the rev3d build; rev3c shares the outline/origin)
    board = {r: json.load(open(DATA / r / 'board.json')) for r in ('rev3c', 'rev3d') if (DATA / r / 'board.json').exists()}
    ex = json.load(open(CACHE / 'rev3d' / 'extract.json')) if (CACHE / 'rev3d' / 'extract.json').exists() else None
    ib = (ana / 'interface_baseline.py').read_text()
    floor = float(re.search(r'^FLOOR = ([\d.]+)', ib, re.M).group(1))
    standoff = float(re.search(r'^PCB_STANDOFF = ([\d.]+)', ib, re.M).group(1))
    pcb_t = float(re.search(r'^PCB_T = ([\d.]+)', ib, re.M).group(1))
    seat_z = floor + standoff

    def mat(rev):
        cx, cy = board[rev]['glb']['origin_mm']
        yb = board[rev]['glb']['board_bottom_y_mm']
        # case (x, y, z) mm -> board GLB mm: X = x - cx, Y = z - seat_z + yb, Z = ky - cy with ky = 2*CASE_CY - y
        return [[1, 0, 0, round(-cx, 4)],
                [0, 0, 1, round(yb - seat_z, 4)],
                [0, -1, 0, round(2 * CASE_CY - cy, 4)],
                [0, 0, 0, 1]]

    # ---------------- Rev3D case (shared with Rev3C): four lids, flush USB-C port ----------------
    C3_ARGS = ['--stack', '11.325', '--boot-height', '1.5', '--reset-height', '1.5', '--boot-stop', '0.4', '--reset-stop', '0.4',
               '--leaf-offset', '17.3', '--relieved-guides', '--usb-style', 'flush', '--rj45-style', 'flush', '--label-inlay']
    C6_ARGS = ['--stack', '11.325', '--boot-height', '0.53', '--reset-height', '0.53', '--boot-stop', '0.36', '--reset-stop', '0.36',
               '--leaf-offset', '16.6', '--relieved-guides', '--usb-style', 'flush', '--rj45-style', 'flush', '--label-inlay']
    ANTENNA = {'fpc': 'Flat antenna holder', 'smooth': 'Smooth top', 'external': 'External SMA'}
    VARIANTS = [(m, a, args) for m, args in (('c3', C3_ARGS), ('c6', C6_ARGS)) for a in ('fpc', 'smooth', 'external')]
    built = []
    for mod, ant, argv in VARIANTS:
        outx, cmdx = run_export(CFG, ana, mod, ant, argv, f'{mod}-{ant}-flush')
        cid = f'rev3d-{mod}-{ant}'
        lidstem = f'review_lid_{mod}_{ant}'
        pieces = [('review_base', 'base', 'Base (common)', '#8d98a5'), (lidstem, 'lid', f'{mod.upper()} lid, {ANTENNA[ant].lower()}', '#c5ccd4'),
                  ('review_guide_wifi', 'guide', 'Light guide: Wi-Fi', '#ffd24a'), ('review_guide_bus', 'guide', 'Light guide: bus', '#ffd24a'),
                  ('review_guide_aux', 'guide', 'Light guide: aux', '#ffd24a')]
        pieces.append((f'review_label_inlay_{mod}', 'inlay', 'Label inlay, second colour (multi-material printers)', '#3c4249'))
        if ant == 'fpc':
            pieces.append(('proxy_fpc_antenna_40x20', 'proxy', 'Flat antenna 40 x 20 mm (reference, not printed)', '#c8742c'))
        extra_src = {}
        if ant == 'external':
            extra_src = rpsma_proxies(cases_dir / cid)
            pieces += [('proxy_rpsma_bulkhead', 'proxy', 'RP-SMA bulkhead, nut and washer (reference)', '#c9a24a'),
                       ('proxy_dipole_120mm', 'proxy', '120 mm half-wave dipole, straight (reference)', '#2b2f34'),
                       ('proxy_dipole_swivel_up', 'proxy', '120 mm tilt-swivel dipole, turned upright (reference)', '#2b2f34')]
        partsx, meshx = [], {}
        for stem, role, label, color in pieces:
            out = cases_dir / cid / f'{stem}.glb'
            meshx[stem] = stl_to_glb(extra_src.get(stem, outx / f'{stem}.stl'), out, stem)
            pr = slice_stl(outx / f'{stem}.stl', CACHE / 'slice' / cid / f'{stem}.gcode') if role in ('base', 'lid') else None
            partsx.append({'name': label, 'role': role, 'file': f'cases/{cid}/{stem}.glb', 'color_hint': color, 'print': pr, 'bytes': out.stat().st_size,
                           **({'metal': True} if stem == 'proxy_rpsma_bulkhead' else {}),
                           **({'whip_pose': 'straight', 'whip_label': 'Straight out'} if stem == 'proxy_dipole_120mm' else {}),
                           **({'whip_pose': 'swivel', 'whip_label': 'Swivel, upright'} if stem == 'proxy_dipole_swivel_up' else {})})
        px = json.load(open(outx / 'REVIEW-PARAMETERS.json'))
        built.append((mod, ant, cid, partsx, meshx, lidstem, outx, cmdx, px))

    # ---------------- magnet bases (same for every lid): four 8 x 2 mm N52 disc pockets, three mounting styles ----------------
    MAG_STYLES = {'glue': 'Glue-in (open pocket, flush)', 'press': 'Press-fit (crush ribs)', 'embedded': 'Embedded (pause print, sealed)'}
    mag_parts = []
    for style, label in MAG_STYLES.items():
        outm, cmdm = run_export(CFG, ana, 'c3', 'fpc', C3_ARGS + ['--magnets', '8x2', '--magnet-style', style], f'magnets-8x2-{style}-flush')
        rm = json.load(open(outm / 'REVIEW-PARAMETERS.json'))['magnets']
        pr = slice_stl(outm / 'review_base.stl', CACHE / 'slice' / 'magnets' / f'review_base_magnets_8x2_{style}.gcode')
        # magnet discs in the physical case frame (export mirrors y about 20): [x, y, z_bottom, diameter, thickness]
        zb = (lambda z0: -1.0 if style != 'embedded' else z0)
        discs = [[x, round(40 - y, 3), round(zb(z0), 3), 8.0, 2.0] for x, y, r, z0, z1 in rm['pockets']]
        note = {'glue': 'Open-bottom pockets; glue N52 8 x 2 mm discs flush (CA or epoxy). Strongest hold. 1.3 mm skin to the cavity floor.',
                'press': 'Open-bottom pockets with three 0.6 mm crush ribs (0.25 mm into the pocket); press the discs in, no glue. Hold as glue-in.',
                'embedded': f"Sealed pockets 0.55 mm above the bottom face. Pause BEFORE print height {rm['pause_before_print_z_mm']} mm (0.35 mm first layer, 0.2 mm layers), drop the discs in (all the same pole up), resume. Invisible; roughly a third less hold through the skin."}[style]
        mag_parts.append((style, label, outm, pr, discs, note))
    for mod, ant, cid, partsx, meshx, lidstem, outx, cmdx, px in built:
        for i, (style, label, outm, pr, discs, note) in enumerate(mag_parts):
            out = cases_dir / cid / f'review_base_magnets_8x2_{style}.glb'
            stl_to_glb(outm / 'review_base.stl', out, f'review_base_magnets_8x2_{style}')
            partsx.insert(1 + i, {'name': f'Base, magnets: {label}', 'role': 'base', 'variant': f'magnets-{style}', 'magnet_style': style,
                                  'magnet_label': label, 'magnet_discs': discs, 'file': f'cases/{cid}/review_base_magnets_8x2_{style}.glb',
                                  'color_hint': '#8d98a5', 'print': pr, 'bytes': out.stat().st_size, 'note': note})

    # ---------------- placement verification (Rev3C/3D board in the Rev3C case) ----------------
    checks = {cid: (placement_check(meshx['review_base'], meshx[lidstem], ex, seat_z, pcb_t, *board['rev3d']['glb']['origin_mm']) if ex and board else None)
              for mod, ant, cid, partsx, meshx, lidstem, outx, cmdx, px in built}
    def verdict(chk):
        if not chk: return False
        good = all(v['inside_solid'] == 0 for k, v in chk['placement_y_equals_40_minus_ky'].items() if not k.startswith('board plate'))
        plate = chk['placement_y_equals_40_minus_ky']['board plate (z mid-board, grid 40x16)']
        return bool(good and chk['board_bbox_inside_case_xy'] and plate['inside_solid'] <= 0.1 * plate['points'])
    frame_note = ('Case export frame (physical, right-handed) = (x, y, z) mm with x = KiCad x, y = 40 - KiCad y (mirror about the '
                  'board centreline, applied by enclosure.export() since the 2026-11-23 frame fix), z up with the board bottom at '
                  f'z = {seat_z} (FLOOR {floor} + PCB_STANDOFF {standoff}) and the board top at z = {round(seat_z + pcb_t, 3)} (interface_baseline.py). '
                  'Case GLBs keep these CAD axes (z up) scaled to metres; matrix_mm maps case mm -> board-GLB mm: '
                  'X = x - cx, Y = z - seat_z + board_bottom_y, Z = (40 - y) - cy. Determinant +1: a proper rotation, so the board '
                  'needs no mirroring to sit in the case. Before the fix the exports used y = KiCad y (determinant -1, a mirror-image case).')
    def placement(chk, revs):
        ok = verdict(chk)
        mats = {r: mat(r) for r in revs if r in board}
        base_m = mats.get('rev3d') or next(iter(mats.values()), None)
        return {'map': frame_note, 'verified': ok, 'matrix_mm': base_m if ok else None,
                'matrix_mm_by_revision': mats if ok else {},
                'matrix_determinant': round(float(np.linalg.det(np.array(base_m, float)[:3, :3])), 6) if base_m else None,
                'note': ('Verified by sampling: points inside the J1 body, the J5/J6 socket rows and a grid over the board plate '
                         'are not inside printed solid (except mounting posts/standoffs) with y = 40 - ky, while the old y = ky convention '
                         'collides at J1 and J5. See checks.') if ok else 'Placement checks did not pass; see checks.',
                'checks': chk}

    # ---------------- rev2 ----------------
    r2dir = repo / 'case' / 'rev2' / 'exports'
    r2_parts, r2m = [], {}
    for stem, role, label, color in (('v2-case-base', 'base', 'Base', '#8d98a5'), ('v2-case-lid', 'lid', 'Lid', '#c5ccd4')):
        out = cases_dir / 'rev2' / f'{stem}.glb'
        r2m[stem] = stl_to_glb(r2dir / f'{stem}.stl', out, stem)
        r2_parts.append({'name': label, 'role': role, 'file': f'cases/rev2/{stem}.glb', 'color_hint': color, 'print': None, 'bytes': out.stat().st_size})
    r2b = trimesh.util.concatenate(list(r2m.values())).bounds
    r2ex = json.load(open(CACHE / 'rev2.2' / 'extract.json'))['bbox_mm'] if (CACHE / 'rev2.2' / 'extract.json').exists() else None
    r2_note = (f'Rev2 STL bounds (mm): x {r2b[0][0]:.2f}..{r2b[1][0]:.2f}, y {r2b[0][1]:.2f}..{r2b[1][1]:.2f}, z {r2b[0][2]:.2f}..{r2b[1][2]:.2f}. ')
    if r2ex:
        r2_note += (f'Rev2.x board bbox in KiCad: x {r2ex["x0"]}..{r2ex["x1"]}, y {r2ex["y0"]}..{r2ex["y1"]}. The case y range equals the NEGATED board y range with equal '
                    f'{(-r2ex["y1"] - r2b[0][1]):.2f}/{(r2b[1][1] + r2ex["y0"]):.2f} mm margins and x lies in the same numeric range (J1 overhangs the board to x 136.94 vs case x max {r2b[1][0]:.2f}), '
                    'so the working hypothesis is case x = KiCad x, case y = -KiCad y (a proper rotation, unlike the Rev3C case). ')
    r2_note += ('The board z level could not be established: only 2 of the 4 board holes (J1 locating holes) coincide with printed solid, so no '
                'placement was verified and no matrix is given.')

    def sources(files):
        return [{'path': hubenv.display_path(p, repo), 'sha256': sha256(p)} for p in files]
    cases += [
        *[{'id': cid, 'label': f'Rev3D case · {mod.upper()} · {ANTENNA[ant]}', 'module': mod, 'antenna': ant, 'antenna_label': ANTENNA[ant],
           'revisions': ['rev3d', 'rev3c'], 'parts': partsx,
           'board_placement': placement(checks[cid], ['rev3d', 'rev3c']),
           'params': {k: v for k, v in px['parameters'].items() if k != 'output'} | {'qualification': px['qualification'],
                      'command': 'python ' + ' '.join(str(c) for c in cmdx[1:-1]) + ' <dir>', 'usb_flush': px.get('usb_flush')},
           'source_files': sources([ana / 'enclosure.py', ana / 'interface_baseline.py', ana / 'export_review.py', outx / 'REVIEW-PARAMETERS.json']),
           'status_note': ('Shared by Rev3D and Rev3C (same outline, holes, J1 and sockets); every Rev3D 3D model checked clear of printed solid. '
                           'Flush USB-C port (0.5 mm in front of the module mouth, 9.64 x 4.36 mm opening); mouth position and shell are unmeasured, '
                           'so print the USB-end coupon first. '
                           + {'fpc': 'Flat antenna holder: keeper rails and two cable keepers under the roof for the 40 x 20 mm FPC antenna that ships with the XIAO (plugs into its U.FL). ',
                              'smooth': 'Smooth top: plain roof with no antenna features, for the C6 onboard ceramic antenna or your own mounting (tape, other antennas). The C3 has no onboard antenna, so it needs an FPC or external antenna. ',
                              'external': 'External SMA: 12 mm bulkhead bore in the long side wall at x 56 mm for an SMA/RP-SMA pigtail from the module U.FL, plus a printed cable keeper; hardware, bend room and RF unverified. '}[ant]
                           + ('C6 switch values are composed from documented nominals. ' if mod == 'c6' else '')
                           + 'Unqualified review geometry.')}
          for mod, ant, cid, partsx, meshx, lidstem, outx, cmdx, px in built],
        {'id': 'rev2', 'label': 'Rev 2 case (Fusion export)', 'revisions': ['rev2.0', 'rev2.1', 'rev2.2'], 'parts': r2_parts,
         'board_placement': {'map': 'Not established: ' + r2_note, 'verified': False, 'matrix_mm': None, 'matrix_mm_by_revision': {}, 'note': r2_note, 'checks': None},
         'params': {'format': 'STL exported from v2-case.f3z (Fusion 360)', 'units_assumed': 'mm'},
         'source_files': sources([r2dir / 'v2-case-base.stl', r2dir / 'v2-case-lid.stl']),
         'status_note': 'Designed around the Rev 2.x outline (case/rev2/README.md). Units assumed to be mm; not verified against a board.'},
    ]
    import compact_cases
    if exporter is None:
        import build as exporter
    cases = compact_cases.build(CFG, DATA, exporter) + cases
    (DATA / 'cases.json').write_text(json.dumps(cases, indent=1) + '\n')
    print('cases:', [(c['id'], c['board_placement']['verified']) for c in cases])
