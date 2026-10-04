"""Create native KiCad C3/C6 previews and matched-camera baseline comparisons."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
REV = ROOT / 'pcb/rev3c'
PCB = REV / 'design/GEA-Adapter-Rev3C.kicad_pcb'
BASE = '409dc0118dce37eb6bdd3f4507da134994e1333e'
CURRENT_C3 = 'XIAO_ESP32C3_v1.3_vendor_pcb_visual_reference.step'
ALTERNATE_C6 = 'XIAO_ESP32C6_v1.0_vendor_pcb_visual_reference.step'


def run_view(job):
    board, image, view = job
    args = ['kicad-cli', 'pcb', 'render', '-D',
            'KICAD9_3DMODEL_DIR=' + os.environ['KICAD9_3DMODEL_DIR'],
            '--width', '1800', '--height', '1000', '--quality', 'high',
            '--background', 'opaque', '--side', 'bottom' if view == 'bottom' else 'top']
    if view == 'oblique':
        args += ['--rotate', '315,0,25']
    args += ['-o', str(image), str(board)]
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode or not image.is_file():
        raise RuntimeError(f'Render failed: {image.name}; ' + result.stdout.decode(errors='replace')[-2000:])
    print('Rendered', image.name, flush=True)
    return {'image': str(image.relative_to(REV)),
            'sha256': hashlib.sha256(image.read_bytes()).hexdigest(),
            'bytes': image.stat().st_size, 'side': view,
            'source_sha256': hashlib.sha256(board.read_bytes()).hexdigest(),
            'rotate_deg': [315,0,25] if view == 'oblique' else [0,0,0]}


if __name__ == '__main__':
    assert subprocess.check_output(['kicad-cli', '--version']).decode().strip() == '9.0.9'
    (REV/'images/model-comparison').mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='gea-model-render-') as td:
        scratch = Path(td)
        (scratch/'models').symlink_to(REV/'design/models', target_is_directory=True)
        # Board-only transient variants carry identical electrical source.
        old = scratch/'baseline.kicad_pcb'
        source_old = subprocess.check_output(['git','-C',str(ROOT),'show',f'{BASE}:pcb/rev3c/design/GEA-Adapter-Rev3C.kicad_pcb']).decode()
        # Native standalone boards without a matching project may leave
        # KIPRJMOD unresolved. Resolve only transient model paths explicitly.
        local_models = str(REV/'design/models') + '/'
        old.write_text(source_old.replace('${KIPRJMOD}/models/',local_models))
        c6 = scratch/'c6-visual-only.kicad_pcb'
        alternate = PCB.read_text().replace(CURRENT_C3,ALTERNATE_C6)
        assert alternate.count('(xyz -16.637 -7.62 12.6)') == 1
        # C6's verified U.FL body datum differs from C3's.
        alternate = alternate.replace('(xyz -16.637 -7.62 12.6)',
                                      '(xyz -16.6275 -3.324 12.6)')
        c6.write_text(alternate.replace('${KIPRJMOD}/models/',local_models))
        jobs = []
        for view in ['top','bottom','oblique']:
            jobs.append((PCB, REV/f'images/rev3c-render-{view}.png', view))
            jobs.append((old, REV/f'images/model-comparison/before-{view}.png', view))
        for view in ['top','bottom','oblique']:
            jobs.append((c6, REV/f'images/rev3c-render-c6-{view}.png', view))
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(run_view,jobs))
    receipt = {'renderer':'native KiCad CLI 9.0.9','render_quality':'high',
               'dimensions_pixels':[1800,1000], 'baseline_commit':BASE,
               'matched_camera_before_after':True,
               'c6_variant_is_transient_3d_model_swap_only':True,
               'pixel_review':'Pending explicit image inspection', 'renders':results}
    (REV/'validation/component-model-render-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
