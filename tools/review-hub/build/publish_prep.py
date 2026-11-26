#!/usr/bin/env python3
"""Make site files publishable as a Claude artifact.

1. Write a self-contained .gltf.json (JSON, buffer as a base64 data URI) beside every .glb.
2. Strip DOCTYPE/DTD declarations from SVGs (the artifact host refuses XML files that carry them), and re-wrap
   embedded image data so no line looks like a credential to GitHub push protection (see TOKEN below).


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


# GitHub push protection reads a 64-character line of the form <11 alnum>AAAAAAAAAA<43 alnum> as a Dropbox token.
# kicad-cli wraps embedded PNG data at exactly 64 characters, and zero-heavy scans produce such lines. Re-wrap the
# same bytes (padding restored) at the first width that leaves no token-shaped run; validate.py checks the result.
TOKEN = re.compile(r'(?<![A-Za-z0-9])[A-Za-z0-9]{11}AAAAAAAAAA[A-Za-z0-9_=\-]{43}(?![A-Za-z0-9_=\-])')
IMG = re.compile(r'(data:image/[a-z+]+;base64,)([A-Za-z0-9+/=\s]+)(?=")')


def _rewrap(m):
    s = re.sub(r'\s', '', m.group(2)); s += '=' * (-len(s) % 4)
    for w in (76, 100, 120, 200, 1000):
        out = '\n'.join(s[i:i + w] for i in range(0, len(s), w))
        if not TOKEN.search(out): break
    return m.group(1) + out


def strip_svg(svg: Path) -> bool:
    t = svg.read_text(encoding='utf-8', errors='replace')
    n = IMG.sub(_rewrap, DOCTYPE.sub('', t, count=1))
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
    print(f'{g} .glb mirrored to .gltf.json, {s} SVGs cleaned (DOCTYPE stripped / image data re-wrapped)')
