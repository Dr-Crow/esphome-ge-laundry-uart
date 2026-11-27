"""Build the compact board legend views from the revision's final manufacturing files."""
from io import BytesIO
from pathlib import Path
import shutil
import zipfile

import cairosvg
from gerbonara import GerberFile
from PIL import Image, ImageOps


def render_layer(gerber, bbox_mm, size):
    x0, y0, x1, y1 = (bbox_mm[k] for k in ('x0', 'y0', 'x1', 'y1'))
    # Explorer overlays all layers in the top-view coordinate frame. Gerber +Y is up.
    bounds = ((x0, -y1), (x1, -y0))
    drawing = GerberFile.from_string(gerber.decode()).to_svg(
        force_bounds=bounds, bg='white', fg='black')
    png = cairosvg.svg2png(bytestring=str(drawing).encode(), output_width=size[0] * 3,
                           output_height=size[1] * 3)
    with Image.open(BytesIO(png)).convert('RGBA') as pixels:
        sheet = Image.new('RGBA', pixels.size, 'white')
        sheet.alpha_composite(pixels)
        ink = ImageOps.invert(sheet.convert('L')).resize(size, Image.Resampling.LANCZOS)
    return Image.merge('LA', (Image.new('L', size, 255), ink))


def stage(revision_dir, out, bbox_mm):
    revision_dir = Path(revision_dir)
    evidence = revision_dir / 'evidence/silkscreen'
    cam, = (revision_dir / 'manufacturing').glob('CAM*.zip')
    render_dir = out / 'renders'
    render_dir.mkdir(exist_ok=True)
    with zipfile.ZipFile(cam) as archive:
        for side, layer, suffix in [('top', 'F.SilkS', '.gto'), ('bottom', 'B.SilkS', '.gbo')]:
            member, = [name for name in archive.namelist() if name.lower().endswith(suffix)]
            path = out / 'layers' / (layer + '.png')
            with Image.open(out / 'layers/Edge.Cuts.png') as edge:
                image = render_layer(archive.read(member), bbox_mm, edge.size)
            image.save(path, optimize=True)
            # These reviewed composites are already in physical viewing orientation.
            shutil.copyfile(evidence / (side + '.png'), render_dir / (side + '.png'))
