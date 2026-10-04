"""Render the model-only Rev3B checkpoint and its exact historical baseline."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
REV = ROOT/'pcb/rev3b'
PCB = REV/'design/GEA-Adapter-Rev3B.kicad_pcb'
BASE = '1db7a80f38a05c0c85023c01df63db22d81281c4'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render(job):
    board, dest, view, source_hash = job
    command = ['kicad-cli', 'pcb', 'render', '-D',
               'KICAD9_3DMODEL_DIR='+os.environ['KICAD9_3DMODEL_DIR'],
               '--width', '1800', '--height', '1000', '--quality', 'high',
               '--background', 'opaque', '--side', 'bottom' if view == 'bottom' else 'top']
    rotation = [315, 0, 25] if view == 'oblique' else [0, 0, 0]
    if view == 'oblique':
        command += ['--rotate', ','.join(map(str, rotation))]
    command += ['-o', str(dest), str(board)]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert result.returncode == 0 and dest.is_file(), result.stdout.decode(errors='replace')[-2000:]
    print('Rendered', dest.name, flush=True)
    return {'image': str(dest.relative_to(REV)), 'sha256': sha(dest),
            'bytes': dest.stat().st_size, 'view': view, 'rotation_deg': rotation,
            'pcb_source_sha256': source_hash}


def main():
    assert subprocess.check_output(['kicad-cli', '--version']).decode().strip() == '9.0.9'
    (REV/'images/model-comparison').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='rev3b-c3-visual-') as directory:
        scratch = Path(directory)
        baseline = subprocess.check_output(['git', '-C', str(ROOT), 'show',
            f'{BASE}:pcb/rev3b/design/GEA-Adapter-Rev3B.kicad_pcb'])
        jobs = []
        for name, data, before in [('current', PCB.read_bytes(), False),
                                   ('baseline', baseline, True)]:
            transient = scratch/f'{name}.kicad_pcb'
            # Standalone transient boards resolve KIPRJMOD explicitly. Only
            # model paths change in these diagnostic copies, never source.
            transient.write_text(data.decode().replace('${KIPRJMOD}/models/',
                                                       str(REV/'design/models')+'/'))
            for view in ['top', 'bottom', 'oblique']:
                dest = REV/(f'images/model-comparison/before-{view}.png' if before else
                            f'images/rev3b-render-{view}.png')
                jobs.append((transient, dest, view, hashlib.sha256(data).hexdigest()))
        with ThreadPoolExecutor(max_workers=2) as pool:
            rows = list(pool.map(render, jobs))
    receipt = {'native_renderer': 'KiCad CLI 9.0.9', 'quality': 'high',
               'dimensions_px': [1800, 1000], 'baseline_commit': BASE,
               'matched_camera_before_after': True,
               'pixel_review': 'Pending explicit inspection', 'renders': rows}
    (REV/'validation/verified-c3-render-receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')


if __name__ == '__main__':
    main()
