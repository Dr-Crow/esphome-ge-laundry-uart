"""Mirror the repository's markdown into site/docs and write data/docs.json.

Private working notes are NOT part of the public build. They are mirrored only when a notes folder is configured
explicitly (HUB_NOTES or "notes" in build/config.local.json); the repo-only build has no "Plan & findings",
"Research" or "Reddit drafts" groups.

Never copies certs/, logs/, venvs/, ci-local*/, scratch-repo/, esphome-cache/, or anything under a dotfile path.
Candidates are scanned for credential-like patterns first; a file with any hit is NOT copied and is listed in
build/cache/docs-skipped.json (path + pattern name + hit count only, never the matched text)."""
import json, re, shutil
from pathlib import Path
from urllib.parse import unquote

import hubenv

IMG_EXT = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}
BLOCK_DIRS = ('certs', 'logs', 'venvs', 'scratch-repo', 'esphome-cache')
MAX_IMG = 4 * 1024 * 1024  # GitHub Pages has no tight per-site budget; one 2.5 MB comparison image is linked from two docs

SECRET_PATTERNS = {
    'aws-access-key': r'AKIA[0-9A-Z]{16}',
    'github-token': r'\b(?:ghp|gho|ghu|ghs|ghr|github_pat)_[A-Za-z0-9_]{20,}',
    'slack-token': r'\bxox[abprs]-[A-Za-z0-9-]{10,}',
    'openai-style-key': r'\bsk-[A-Za-z0-9_-]{20,}',
    'private-key-block': r'-----BEGIN [A-Z ]*PRIVATE KEY-----',
    'credential-assignment': r'(?i)\b(?:api[_-]?key|secret|access[_-]?token|auth[_-]?token|passwd|password)\b["\']?\s*[:=]\s*["\']?[A-Za-z0-9/_\-.+]{8,}',
    'email-address': r'(?<![\w.+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}',
}


def blocked(rel: Path):
    parts = rel.parts
    return any(p.startswith('.') or p in BLOCK_DIRS or p.startswith('ci-local') for p in parts)


def scan(text):
    hits = {}
    for name, pat in SECRET_PATTERNS.items():
        n = len(re.findall(pat, text))
        if n: hits[name] = n
    return hits


def title_of(text, fallback):
    for line in text.splitlines():
        m = re.match(r'#\s+(.+?)\s*#*\s*$', line)
        if m: return re.sub(r'[`*_]', '', m.group(1)).strip()
    return fallback


def linked_images(md_text):
    out = set()
    for m in re.finditer(r'!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+"[^"]*")?\s*\)', md_text):
        out.add(m.group(1))
    for m in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', md_text):
        out.add(m.group(1))
    res = []
    for t in out:
        t = t.split('#')[0].split('?')[0]
        if not t or re.match(r'^[a-z]+:', t) or t.startswith('/'): continue
        if Path(t).suffix.lower() in IMG_EXT:
            res.append(unquote(t))
    return res


def run(CFG, SITE):
    repo = Path(CFG['repo'])
    notes = Path(CFG['notes']) if CFG.get('notes') else None
    docs_root = SITE / 'docs'
    if docs_root.exists(): shutil.rmtree(docs_root)
    docs_root.mkdir(parents=True)
    entries, skipped, copied_assets = [], [], []

    revids = {r['id'] for r in CFG['revisions']}

    def add_doc(src: Path, root: Path, dest_prefix: str, group, rev, source_label):
        rel = src.relative_to(root)
        if blocked(rel):
            return
        text = src.read_text(errors='replace')
        hits = scan(text)
        if hits:
            skipped.append({'file': source_label, 'reason': 'credential-like pattern', 'patterns': hits})
            return
        dest = docs_root / dest_prefix / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        entries.append({'id': f'{dest_prefix}/{rel}'.replace('/', '-').replace('.', '_'),
                        'title': title_of(text, src.name) if src.suffix == '.md' else src.name,
                        'group': group, 'rev': rev, 'path': f'{dest_prefix}/{rel}', 'source': source_label,
                        'bytes': dest.stat().st_size})
        if src.suffix == '.md':
            for t in linked_images(text):
                img = (src.parent / t).resolve()
                try:
                    irel = img.relative_to(root.resolve())
                except ValueError:
                    continue
                if blocked(irel) or not img.is_file(): continue
                if img.stat().st_size >= MAX_IMG:
                    skipped.append({'file': f'{source_label} -> {t}', 'reason': 'linked image >= 2 MB'}); continue
                d = docs_root / dest_prefix / irel
                if d.exists(): continue
                d.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(img, d)
                copied_assets.append(str(d.relative_to(docs_root)))

    # (a) private notes: only when a notes folder is configured explicitly
    if notes:
        for name, group in (('PLAN.md', 'Plan & findings'), ('FINDINGS.md', 'Plan & findings')):
            add_doc(notes / name, notes, 'notes', group, None, f'notes/{name}')
        for f in sorted((notes / 'research').glob('*')):
            if f.suffix in ('.md', '.txt'):
                add_doc(f, notes, 'notes', 'Research', None, f'notes/{f.relative_to(notes)}')
        add_doc(notes / 'reddit' / 'DRAFTS.md', notes, 'notes', 'Reddit drafts', None, 'notes/reddit/DRAFTS.md')
        for f in sorted((notes / 'reddit' / 'assets').glob('*')):
            if f.suffix.lower() in IMG_EXT | {'.pdf'} and f.is_file():
                d = docs_root / 'notes' / 'reddit' / 'assets' / f.name
                d.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, d)
                copied_assets.append(str(d.relative_to(docs_root)))

    # (b) repo
    singles = ['README.md', 'CONTRIBUTING.md', 'pcb/README.md', 'pcb/ORDERING.md', 'case/README.md',
               'case/rev3c/analytical/README.md', 'case/rev3c/analytical/MECHANICAL-DIMENSIONS.md']
    cand = [(repo / s) for s in singles]
    cand += sorted((repo / 'pcb').glob('rev*/*.md'))
    cand += sorted((repo / 'case').glob('*/README.md'))
    cand += sorted((repo / 'docs').rglob('*.md')) if (repo / 'docs').exists() else []
    seen = set()
    for f in cand:
        if not f.exists() or f in seen: continue
        seen.add(f)
        rel = f.relative_to(repo)
        top = rel.parts[0]
        rev = rel.parts[1] if top == 'pcb' and len(rel.parts) > 2 and rel.parts[1] in revids else None
        group = 'Revision docs' if rev else ('Case docs' if top == 'case' else 'Repo')
        add_doc(f, repo, 'repo', group, rev, str(rel))

    order = {'Plan & findings': 0, 'Research': 1, 'Reddit drafts': 2, 'Revision docs': 3, 'Case docs': 4, 'Repo': 5}
    entries.sort(key=lambda e: (order[e['group']], e['rev'] or '', e['path']))
    (SITE / 'data').mkdir(parents=True, exist_ok=True)
    (SITE / 'data' / 'docs.json').write_text(json.dumps(entries, indent=1) + '\n')
    hubenv.CACHE.mkdir(parents=True, exist_ok=True)
    (hubenv.CACHE / 'docs-skipped.json').write_text(json.dumps({'skipped': skipped, 'assets_copied': len(copied_assets)}, indent=1))
    print(f'docs: {len(entries)} documents, {len(copied_assets)} images/pdfs, {len(skipped)} skipped')
    for s in skipped:
        print('  skipped:', s['file'], s.get('patterns') or s['reason'])
