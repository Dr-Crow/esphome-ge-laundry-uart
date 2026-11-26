"""KiCad standard 3D models (kicad-packages3D @ tag 9.0.0), fetched file-by-file into build/cache/packages3D/.

Only files referenced by footprints in the configured PCBs via ${KICAD6..9_3DMODEL_DIR} are fetched. STEP is fetched for every
referenced path (kicad-cli --subst-models swaps .wrl -> .step); the .wrl itself only when no STEP exists upstream.
MANIFEST.json records url, size and sha256 for each file (and files that do not exist upstream)."""
import hashlib, json, re, ssl, time, urllib.error, urllib.request
from pathlib import Path

TAG = '9.0.0'
BASE = f'https://gitlab.com/kicad/libraries/kicad-packages3D/-/raw/{TAG}/'
RX = re.compile(r'\(model "\$\{KICAD\d_3DMODEL_DIR\}/([^"]+)"')


def wanted(repo, pcbs):
    out = set()
    for p in pcbs:
        for m in RX.finditer((Path(repo) / p).read_text()):
            out.add(m.group(1))
    return sorted(out)


def _get(url, ctx):
    req = urllib.request.Request(url, headers={'User-Agent': 'design-review-hub-build'})
    for attempt in range(3):
        try:
            return urllib.request.urlopen(req, timeout=60, context=ctx).read()
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            if attempt == 2: raise
        except Exception:
            if attempt == 2: raise
        time.sleep(2)


def fetch(repo, pcbs, pkg_dir, ca_bundle=None):
    pkg = Path(pkg_dir); pkg.mkdir(parents=True, exist_ok=True)
    mf_path = pkg / 'MANIFEST.json'
    mf = json.load(open(mf_path)) if mf_path.exists() else {'source': BASE, 'tag': TAG, 'files': {}, 'missing_upstream': []}
    try:
        ctx = ssl.create_default_context()
        _ = ctx
    except Exception:
        ctx = None
    def get(url):
        try:
            return _get(url, ctx)
        except ssl.SSLError:
            return _get(url, ssl.create_default_context(cafile=ca_bundle))
        except urllib.error.URLError as e:
            if isinstance(e.reason, ssl.SSLError) and ca_bundle:
                return _get(url, ssl.create_default_context(cafile=ca_bundle))
            raise
    for rel in wanted(repo, pcbs):
        stem = rel.rsplit('.', 1)[0]
        # kicad-cli --subst-models resolves the referenced path first and only then swaps in the .step, so a referenced .wrl is fetched too
        if rel.endswith('.wrl') and not (rel in mf['files'] and (pkg / rel).exists()):
            wd = get(BASE + rel)
            time.sleep(0.2)
            if wd is not None:
                (pkg / rel).parent.mkdir(parents=True, exist_ok=True); (pkg / rel).write_bytes(wd)
                mf['files'][rel] = {'url': BASE + rel, 'bytes': len(wd), 'sha256': hashlib.sha256(wd).hexdigest(), 'note': 'referenced path; the STEP twin is used by --subst-models'}
        for ext in ('.step',):
            r = stem + ext
            if r in mf['files'] and (pkg / r).exists(): continue
            data = get(BASE + r)
            time.sleep(0.2)
            if data is None:
                # no STEP upstream: fall back to the referenced WRL (or the path as written)
                w = stem + '.wrl'
                if w in mf['files'] and (pkg / w).exists(): continue
                wd = get(BASE + w)
                if wd is None:
                    if rel not in mf['missing_upstream']: mf['missing_upstream'].append(rel)
                    continue
                (pkg / w).parent.mkdir(parents=True, exist_ok=True); (pkg / w).write_bytes(wd)
                mf['files'][w] = {'url': BASE + w, 'bytes': len(wd), 'sha256': hashlib.sha256(wd).hexdigest()}
                continue
            (pkg / r).parent.mkdir(parents=True, exist_ok=True); (pkg / r).write_bytes(data)
            mf['files'][r] = {'url': BASE + r, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    mf['total_files'] = len(mf['files']); mf['total_bytes'] = sum(f['bytes'] for f in mf['files'].values())
    mf_path.write_text(json.dumps(mf, indent=1, sort_keys=True) + '\n')
    return mf
