"""Shared setup for the hub build scripts: configuration, output/cache locations and tool environments.

Everything machine-specific is optional. The defaults work on a fresh clone:

  repo        the repository this file lives in (tools/review-hub/build -> three levels up)
  notes       unset: no private notes are mirrored (see docs_mirror.py)
  cad_python  unset: build/.venv-cad is created from build/requirements-cad.txt the first time cases are built
  ca_bundle   unset: the system trust store is used

Override with environment variables HUB_REPO, HUB_NOTES, HUB_CAD_PYTHON, HUB_CA_BUNDLE or with a git-ignored
build/config.local.json holding the same four keys ("repo", "notes", "cad_python", "ca_bundle").
Output and cache locations: --out DIR / HUB_SITE (default tools/review-hub/site) and --cache DIR / HUB_CACHE
(default build/cache).
"""
import json, os, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent           # tools/review-hub/build
HUB = HERE.parent                                 # tools/review-hub
VENV = HERE / '.venv'
CAD_VENV = HERE / '.venv-cad'
OVERRIDE_KEYS = ('repo', 'notes', 'cad_python', 'ca_bundle')
ENV_KEYS = {'repo': 'HUB_REPO', 'notes': 'HUB_NOTES', 'cad_python': 'HUB_CAD_PYTHON', 'ca_bundle': 'HUB_CA_BUNDLE'}


def _argv_opt(name):
    """Value of --name X / --name=X on the command line, read before argparse so module-level paths can use it."""
    a = sys.argv
    for i, x in enumerate(a):
        if x == name and i + 1 < len(a):
            return a[i + 1]
        if x.startswith(name + '='):
            return x.split('=', 1)[1]
    return None


def _path(value):
    return Path(value).expanduser().resolve()


SITE = _path(_argv_opt('--out') or os.environ.get('HUB_SITE') or HUB / 'site')
CACHE = _path(_argv_opt('--cache') or os.environ.get('HUB_CACHE') or HERE / 'cache')


def load_config():
    cfg = json.load(open(HERE / 'revisions.config.json'))
    local = HERE / 'config.local.json'
    if local.exists():
        extra = json.load(open(local))
        unknown = sorted(set(extra) - set(OVERRIDE_KEYS))
        if unknown:
            sys.exit(f'{local}: unknown keys {unknown}; allowed: {list(OVERRIDE_KEYS)}')
        cfg.update({k: v for k, v in extra.items() if v})
    for k, env in ENV_KEYS.items():
        if os.environ.get(env):
            cfg[k] = os.environ[env]
    cfg['repo'] = str(_path(cfg.get('repo') or HUB.parent.parent))
    if not (Path(cfg['repo']) / 'pcb').is_dir():
        sys.exit(f'repo {cfg["repo"]} has no pcb/ folder; set HUB_REPO or "repo" in build/config.local.json')
    for k in ('notes', 'cad_python', 'ca_bundle'):
        cfg[k] = str(_path(cfg[k])) if cfg.get(k) else None
    if cfg['notes'] and not Path(cfg['notes']).is_dir():
        sys.exit(f'notes folder {cfg["notes"]} does not exist')
    return cfg


def ensure_env():
    """Re-exec inside build/.venv (Pillow/numpy/trimesh); create it on first run."""
    if Path(sys.prefix).resolve() == VENV.resolve():
        return
    py = VENV / 'bin' / 'python'
    if not py.exists():
        make_venv(VENV, HERE / 'requirements.txt')
    os.execv(str(py), [str(py)] + sys.argv)


def make_venv(venv, requirements):
    print(f'creating {venv} from {requirements.name} ...', flush=True)
    if shutil.which('uv'):
        subprocess.check_call(['uv', 'venv', '--python', '3.12', str(venv)])
        subprocess.check_call(['uv', 'pip', 'install', '--python', str(venv / 'bin' / 'python'), '-r', str(requirements)])
    else:
        subprocess.check_call([sys.executable, '-m', 'venv', str(venv)])
        subprocess.check_call([str(venv / 'bin' / 'python'), '-m', 'pip', 'install', '-r', str(requirements)])


def ensure_node():
    """npm ci in build/ on a fresh clone (versions and hashes come from package-lock.json)."""
    if (HERE / 'node_modules' / '@gltf-transform' / 'core').exists():
        return
    if not shutil.which('npm'):
        sys.exit('node/npm not found; install Node 18+ and re-run')
    print('npm ci in build/ ...', flush=True)
    subprocess.check_call(['npm', 'ci', '--ignore-scripts'], cwd=HERE)


def require_tools(*names):
    missing = [n for n in names if not shutil.which(n)]
    if missing:
        sys.exit('missing required tools on PATH: ' + ', '.join(missing))


def cad_python(cfg):
    """Interpreter with build123d (the case CAD). Configured one, else build/.venv-cad (created on first use)."""
    if cfg.get('cad_python'):
        if not Path(cfg['cad_python']).exists():
            sys.exit(f'cad_python {cfg["cad_python"]} does not exist')
        return cfg['cad_python']
    py = CAD_VENV / 'bin' / 'python'
    if not py.exists():
        make_venv(CAD_VENV, HERE / 'requirements-cad.txt')
    return str(py)


def display_path(p, repo):
    """Path for published JSON: relative to the repo, or "cache/..." for build products; never absolute."""
    p = Path(p).resolve()
    if p.is_relative_to(CACHE):
        return 'cache/' + str(p.relative_to(CACHE))
    if p.is_relative_to(Path(repo).resolve()):
        return str(p.relative_to(Path(repo).resolve()))
    return p.name
