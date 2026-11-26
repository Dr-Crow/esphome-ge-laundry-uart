#!/usr/bin/env python3
"""Sanity checks over a built site (default tools/review-hub/site, or the directory given as the first argument or by
HUB_SITE): JSON parses, GLBs load, GLB footprint nodes match parts.json, layer PNGs exist with the
declared size, doc image links resolve, site size. Exit code 1 on any failure."""
import json, os, re, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import hubenv
if __name__ == '__main__':
    hubenv.ensure_env()
    hubenv.ensure_node()
import glbtools
from PIL import Image
import trimesh
from urllib.parse import unquote

SITE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else hubenv.SITE
BUDGET_MB = float(os.environ.get('HUB_BUDGET_MB', 200))  # GitHub Pages: 1 GB per site, 100 MB per file
D = SITE / 'data'
bad = []


def fail(msg):
    bad.append(msg); print('FAIL', msg)

print('validating', SITE)

for p in list(D.rglob('*.json')):
    try: json.load(open(p))
    except Exception as e: fail(f'{p}: {e}')
revs = json.load(open(D / 'revisions.json'))
for r in revs:
    d = D / r['id']
    board = json.load(open(d / 'board.json')); parts = json.load(open(d / 'parts.json'))
    j, _ = glbtools.read_glb(d / 'board.glb')
    lvl, w = glbtools.footprint_nodes(j)
    refs = {p['ref'] for p in parts}
    names = {j['nodes'][i].get('name') for i in lvl}
    footprint_nodes = names & refs
    stray = sorted(n for n in names if n not in refs)
    flagged = {p['ref'] for p in parts if p['glb_node']}
    if flagged != footprint_nodes: fail(f'{r["id"]}: parts glb_node flags {sorted(flagged)} != nodes {sorted(footprint_nodes)}')
    info = json.loads(subprocess.check_output(['node', str(HERE / 'inspect_glb.mjs'), str(d / 'board.glb')], cwd=HERE, text=True))
    loaded = f"{info['meshes']} meshes / {info['triangles']} tris, bounds_mm {info['bounds_mm']}"
    bb = board['bbox_mm']
    if info['triangles'] < 10: fail(f'{r["id"]}: GLB has almost no geometry')
    for l in board['layers']:
        f = d / l['file']
        if not f.exists(): fail(f'{r["id"]}: missing {l["file"]}'); continue
        im = Image.open(f)
        exp = (round((l['bbox_mm'][2] - l['bbox_mm'][0]) * 20), round((l['bbox_mm'][3] - l['bbox_mm'][1]) * 20))
        if im.size != exp: fail(f'{r["id"]}: {l["file"]} size {im.size} != {exp}')
    size = sum(f.stat().st_size for f in d.rglob('*') if f.is_file())
    print(f'{r["id"]}: {size / 1e6:.2f} MB, glb {Path(d / "board.glb").stat().st_size / 1e6:.2f} MB, footprint nodes {sorted(footprint_nodes)}, non-ref root nodes {len(stray)}, trimesh geoms {loaded}')
for c in json.load(open(D / 'cases.json')):
    for p in c['parts']:
        if not (D / p['file']).exists(): fail(f'missing {p["file"]}'); continue
        i = json.loads(subprocess.check_output(['node', str(HERE / 'inspect_glb.mjs'), str(D / p['file'])], cwd=HERE, text=True))
        print(f"  case {c['id']}/{p['name']}: {i['triangles']} tris, bounds_mm {i['bounds_mm']}")
docs = json.load(open(D / 'docs.json'))
miss = 0
for e in docs:
    f = SITE / 'docs' / e['path']
    if not f.exists(): fail(f'doc missing {e["path"]}'); continue
    if f.suffix == '.md':
        for m in re.finditer(r'!\[[^\]]*\]\(\s*<?([^)\s>]+)', f.read_text()):
            t = m.group(1).split('#')[0].split('?')[0]
            if t and not re.match(r'^[a-z]+:', t) and Path(t).suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'):
                if not (f.parent / unquote(t)).exists(): miss += 1; print('  unresolved image', e['path'], '->', t)
print(f'docs: {len(docs)} entries, {miss} unresolved image links')
# A whole line shaped like a Dropbox token makes GitHub push protection refuse the gh-pages push.
TOKEN_LINE = re.compile(r'^[A-Za-z0-9]{11}AAAAAAAAAA[A-Za-z0-9_=\-]{43}$', re.M)
for f in SITE.rglob('*'):
    if f.is_file() and f.suffix in ('.svg', '.json', '.html', '.md', '.txt', '.csv'):
        n = len(TOKEN_LINE.findall(f.read_text(encoding='utf-8', errors='replace')))
        if n: fail(f'{f.relative_to(SITE)}: {n} line(s) shaped like a credential (GitHub push protection); run publish_prep.py')
tot = sum(f.stat().st_size for f in SITE.rglob('*') if f.is_file())
print(f'site total {tot / 1e6:.1f} MB ({sum(1 for f in SITE.rglob("*") if f.is_file())} files, budget {BUDGET_MB:g})')
if tot > BUDGET_MB * 1e6: fail('site over budget')
sys.exit(1 if bad else 0)
