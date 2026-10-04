"""Prove the render/model lane preserves the selected electrical candidate."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

BASE = '409dc0118dce37eb6bdd3f4507da134994e1333e'
ROOT = Path(__file__).resolve().parents[3]
PCB = 'pcb/rev3c/design/GEA-Adapter-Rev3C.kicad_pcb'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def baseline(path):
    return subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{BASE}:{path}'])


def remove_models(data):
    # Match balanced S-expressions while respecting escaped quoted strings.
    # Removing whole model nodes proves every other source token unchanged.
    text = data.decode()
    stack, cuts = [], []
    for m in re.finditer(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+', text):
        t = m.group()
        if t == '(':
            stack.append([m.start(), None])
        elif t == ')':
            start, name = stack.pop()
            if name == 'model':
                cuts.append((start, m.end()))
        elif stack and stack[-1][1] is None:
            stack[-1][1] = t
    for start, end in reversed(cuts):
        text = text[:start] + text[end:]
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+', text)
    return json.dumps(tokens, ensure_ascii=False, separators=(',', ':')).encode()


if __name__ == '__main__':
    before = baseline(PCB)
    after = (ROOT / PCB).read_bytes()
    before_tokens, after_tokens = remove_models(before), remove_models(after)
    paths = subprocess.check_output(['git', '-C', str(ROOT), 'ls-tree', '-r', '--name-only', BASE]).decode().splitlines()
    protected = [p for p in paths if (
        p.startswith('firmware/') or '/manufacturing/' in p or
        p.endswith(('.kicad_sch', '.kicad_sym', '.kicad_mod', '.kicad_pro', '.kicad_dru')) or
        ('/design/' in p and p.endswith('.kicad_pcb') and p != PCB)
    )]
    unchanged = [{ 'path':p, 'sha256':digest((ROOT/p).read_bytes()),
                   'matches_selected_baseline':baseline(p)==(ROOT/p).read_bytes()}
                 for p in protected]
    result = {
        'selected_baseline_commit': BASE,
        'comparison': 'Entire PCB S-expression token stream identical after removing only model nodes; all non-model data including pads, nets, tracks, vias, zones, outline, placement and properties retained.',
        'pcb_before_sha256': digest(before), 'pcb_after_sha256': digest(after),
        'pcb_without_models_before_sha256': digest(before_tokens),
        'pcb_without_models_after_sha256': digest(after_tokens),
        'non_model_pcb_tokens_identical': before_tokens == after_tokens,
        'protected_files': unchanged,
        'all_protected_files_byte_identical': all(x['matches_selected_baseline'] for x in unchanged),
    }
    dest = Path(__file__).with_name('component-model-electrical-preservation.json')
    dest.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='protected_files'}, indent=2))
    if not result['non_model_pcb_tokens_identical'] or not result['all_protected_files_byte_identical']:
        raise SystemExit('Model lane altered protected electrical/manufacturing source')
