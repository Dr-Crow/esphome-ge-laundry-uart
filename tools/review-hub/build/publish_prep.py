#!/usr/bin/env python3
"""Make site files publishable as a Claude artifact.

1. Write a self-contained .gltf.json (JSON, buffer as a base64 data URI) beside every .glb.
2. Strip DOCTYPE/DTD declarations from SVGs (the artifact host refuses XML files that carry them).


Claude artifacts do not serve .glb, but they serve .json-like text, and three.js GLTFLoader reads
.gltf with embedded buffers, including EXT_meshopt_compression data. Geometry is byte-identical.
Usage: publish_prep.py SITE_DIR
"""
import base64, json, struct, sys
from pathlib import Path


def convert(glb: Path) -> Path:
    b = glb.read_bytes()
    magic, version, length = struct.unpack_from('<4sII', b, 0)
    if magic != b'glTF' or version != 2:
        raise SystemExit(f'{glb}: not a glTF 2.0 binary')
    off, js, binchunk = 12, None, b''
    while off < length:
        clen, ctype = struct.unpack_from('<I4s', b, off)
        data = b[off + 8: off + 8 + clen]
        if ctype == b'JSON': js = json.loads(data)
        elif ctype == b'BIN\x00': binchunk = data
        off += 8 + clen
    bufs = js.get('buffers', [])
    # The GLB BIN chunk is the buffer without a uri (buffer 0); meshopt fallback buffers stay uri-less.
    for i, buf in enumerate(bufs):
        if 'uri' not in buf and not (buf.get('extensions', {}).get('EXT_meshopt_compression', {}).get('fallback')):
            buf['uri'] = 'data:application/octet-stream;base64,' + base64.b64encode(binchunk[:buf['byteLength']]).decode()
            break
    out = glb.with_suffix('.gltf.json')  # .json is a served type; GLTFLoader sniffs content, not the name
    out.write_text(json.dumps(js, separators=(',', ':')))
    return out


import re
DOCTYPE = re.compile(r'<!DOCTYPE[^>\[]*(\[[^\]]*\])?\s*>', re.S)


def strip_svg(svg: Path) -> bool:
    t = svg.read_text(encoding='utf-8', errors='replace')
    n = DOCTYPE.sub('', t, count=1)
    if n != t:
        svg.write_text(n, encoding='utf-8'); return True
    return False


def run(root):
    root = Path(root)
    g = sum(1 for glb in sorted(root.rglob('*.glb')) if convert(glb))
    s = sum(1 for svg in sorted(root.rglob('*.svg')) if strip_svg(svg))
    return g, s


if __name__ == '__main__':
    g, s = run(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'site')
    print(f'{g} .glb mirrored to .gltf.json, {s} SVG DOCTYPEs stripped')
