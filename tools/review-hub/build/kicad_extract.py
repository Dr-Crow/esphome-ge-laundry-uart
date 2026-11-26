"""Runs INSIDE the pinned kicad image (pcbnew python). Usage: kicad_extract.py in.kicad_pcb out.json
Dumps board geometry (bbox, Edge.Cuts polygons, holes) and every footprint with fields/pads."""
import json, os, sys
import pcbnew

MM = 1e6  # KiCad internal units are nm


def mm(v):
    return round(v / MM, 4)


def poly_rings(ps):
    out = []
    for i in range(ps.OutlineCount()):
        o = ps.Outline(i)
        out.append([[mm(o.CPoint(k).x), mm(o.CPoint(k).y)] for k in range(o.PointCount())])
        for j in range(ps.HoleCount(i)):
            h = ps.Hole(i, j)
            out.append([[mm(h.CPoint(k).x), mm(h.CPoint(k).y)] for k in range(h.PointCount())])
    return out


board = pcbnew.LoadBoard(sys.argv[1])
PROJ = os.path.dirname(os.path.abspath(sys.argv[1]))


def model_resolves(name):
    p = name.replace('${KIPRJMOD}', PROJ)
    for n in (6, 7, 8, 9):
        p = p.replace('${KICAD%d_3DMODEL_DIR}' % n, os.environ.get('KICAD%d_3DMODEL_DIR' % n, '/nonexistent'))
    return any(os.path.exists(x) for x in (p, os.path.splitext(p)[0] + '.step'))

res = {}
bb = board.GetBoardEdgesBoundingBox()
res['bbox_mm'] = {'x0': mm(bb.GetX()), 'y0': mm(bb.GetY()), 'x1': mm(bb.GetRight()), 'y1': mm(bb.GetBottom())}
res['thickness_mm'] = mm(board.GetDesignSettings().GetBoardThickness())
res['copper_layer_count'] = board.GetCopperLayerCount()
res['copper_layers'] = [board.GetLayerName(l) for l in board.GetEnabledLayers().CuStack()]

ps = pcbnew.SHAPE_POLY_SET()
board.GetBoardPolygonOutlines(ps)
res['outline'] = poly_rings(ps)

holes = []
for fp in board.GetFootprints():
    for p in fp.Pads():
        d = p.GetDrillSize()
        if d.x > 0 and d.y > 0:
            c = p.GetPosition()
            holes.append({'x': mm(c.x), 'y': mm(c.y), 'd': mm(min(d.x, d.y)),
                          'plated': p.GetAttribute() != pcbnew.PAD_ATTRIB_NPTH, 'kind': 'pad',
                          **({'slot': [mm(d.x), mm(d.y)], 'orient': round(p.GetOrientationDegrees(), 1)} if d.x != d.y else {})})
for t in board.GetTracks():
    if t.Type() == pcbnew.PCB_VIA_T:
        c = t.GetPosition()
        holes.append({'x': mm(c.x), 'y': mm(c.y), 'd': mm(t.GetDrillValue()), 'plated': True, 'kind': 'via'})
res['holes'] = holes

parts = []
for fp in board.GetFootprints():
    side = 'bottom' if fp.IsFlipped() else 'top'
    crt = fp.GetCourtyard(pcbnew.B_CrtYd if fp.IsFlipped() else pcbnew.F_CrtYd)
    if crt is not None and crt.OutlineCount() > 0:
        b = crt.BBox()
        box = [mm(b.GetX()), mm(b.GetY()), mm(b.GetRight()), mm(b.GetBottom())]
        src = 'courtyard'
    else:
        b = fp.GetBoundingBox(False)
        box = [mm(b.GetX()), mm(b.GetY()), mm(b.GetRight()), mm(b.GetBottom())]
        src = 'pads+body'
    fields = {}
    for f in fp.GetFields():
        fields[f.GetName()] = f.GetText()
    pos = fp.GetPosition()
    fid = fp.GetFPID()
    attrs = fp.GetAttributes()
    pads = [{'num': p.GetNumber(), 'net': p.GetNetname()} for p in fp.Pads()]
    parts.append({
        'ref': fp.GetReference(), 'value': fp.GetValue(),
        'footprint': str(fid.GetUniStringLibId()),
        'side': side, 'x': mm(pos.x), 'y': mm(pos.y), 'rot': round(fp.GetOrientationDegrees(), 3),
        'bbox_mm': box, 'bbox_source': src,
        'dnp': bool(fp.IsDNP()), 'in_bom': not fp.IsExcludedFromBOM(),
        'on_board': not fp.IsExcludedFromBoard() if hasattr(fp, 'IsExcludedFromBoard') else True,
        'fields': fields, 'pads': pads,
        'has_3d_model': any(model_resolves(m.m_Filename) for m in fp.Models()),
        'models_declared': len(fp.Models()),
        'models': [{'offset_mm': [round(m.m_Offset.x, 4), round(m.m_Offset.y, 4), round(m.m_Offset.z, 4)],
                    'rotation_deg': [m.m_Rotation.x, m.m_Rotation.y, m.m_Rotation.z], 'file': m.m_Filename} for m in fp.Models()],
    })
res['parts'] = parts

# pad probes for PNG alignment checks: isolated top-side circular/rectangular pads, spread over the board
import math
cands, allc = [], []
for fp in board.GetFootprints():
    for p in fp.Pads():
        c = p.GetPosition()
        allc.append((c.x / MM, c.y / MM))
for fp in board.GetFootprints():
    for p in fp.Pads():
        if not p.IsOnLayer(pcbnew.F_Cu) or not p.IsOnLayer(pcbnew.F_Mask):
            continue
        shp = p.GetShape()
        if shp not in (pcbnew.PAD_SHAPE_CIRCLE, pcbnew.PAD_SHAPE_RECT, pcbnew.PAD_SHAPE_ROUNDRECT):
            continue
        ang = p.GetOrientationDegrees() % 360
        if round(ang) % 90 != 0 or abs(ang - round(ang)) > 0.01:
            continue
        sz = p.GetSize(); w, h = sz.x / MM, sz.y / MM
        if round(ang) % 180 == 90:
            w, h = h, w
        if min(w, h) < 0.9 or max(w, h) > 5:
            continue
        c = p.GetPosition(); cx_, cy_ = c.x / MM, c.y / MM
        near = min((math.hypot(cx_ - x, cy_ - y) for x, y in allc if (x, y) != (cx_, cy_)), default=99)
        if near < max(w, h) / 2 + 1.2:
            continue
        cands.append({'ref': fp.GetReference(), 'pad': p.GetNumber(), 'x': round(cx_, 4), 'y': round(cy_, 4),
                      'w': round(w, 4), 'h': round(h, 4), 'shape': 'circle' if shp == pcbnew.PAD_SHAPE_CIRCLE else 'rect', 'side': 'top'})
chosen = []
for _ in range(8):
    if not cands:
        break
    if not chosen:
        chosen.append(cands.pop(0)); continue
    best = max(cands, key=lambda q: min(math.hypot(q['x'] - c['x'], q['y'] - c['y']) for c in chosen))
    cands.remove(best); chosen.append(best)
res['pad_probes'] = chosen
json.dump(res, open(sys.argv[2], 'w'))
print('ok', len(parts), 'footprints', len(holes), 'holes')
