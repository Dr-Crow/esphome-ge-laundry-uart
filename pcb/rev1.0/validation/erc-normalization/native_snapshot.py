import pcbnew,json,sys
from pathlib import Path
b=pcbnew.LoadBoard(sys.argv[1]);out={'footprints':{},'pads':{},'tracks':{},'drawings':{},'footprint_graphics':{}}
xy=lambda p:[p.x,p.y]
def graphic(g):
 d={'class':g.GetClass(),'layer':int(g.GetLayer())}
 if g.GetClass() in ['PCB_TEXT','PCB_FIELD','FP_TEXT']:
  d.update(text=g.GetText(),position=xy(g.GetPosition()),angle=g.GetTextAngleDegrees(),size=xy(g.GetTextSize()),thickness=g.GetTextThickness(),visible=g.IsVisible(),mirrored=g.IsMirrored())
 elif g.GetClass()=='PCB_SHAPE':
  d.update(shape=int(g.GetShape()),start=xy(g.GetStart()),end=xy(g.GetEnd()),width=g.GetWidth())
  if g.GetShape()==pcbnew.SHAPE_T_POLY:
   p=g.GetPolyShape();d['polygons']=[[[o.CPoint(i).x,o.CPoint(i).y] for i in range(o.PointCount())] for o in [p.COutline(j) for j in range(p.OutlineCount())]]
  if g.GetShape()==pcbnew.SHAPE_T_ARC:d.update(center=xy(g.GetCenter()),arc_mid=xy(g.GetArcMid()))
 return d
for f in b.GetFootprints():
 out['footprints'][f.m_Uuid.AsString()]={'reference':f.GetReference(),'value':f.GetValue(),'position':xy(f.GetPosition()),'angle':f.GetOrientationDegrees(),'layer':int(f.GetLayer()),'source_path':f.GetPath().AsString(),'attribute':int(f.GetAttributes()),'dnp':f.IsDNP()}
 for p in f.Pads():
  out['pads'][p.m_Uuid.AsString()]={'reference':f.GetReference(),'number':p.GetNumber(),'net':p.GetNetname(),'pinfunction':p.GetPinFunction(),'pintype':p.GetPinType(),'position':xy(p.GetPosition()),'size':xy(p.GetSize()),'drill':xy(p.GetDrillSize()),'shape':int(p.GetShape()),'attribute':int(p.GetAttribute()),'angle':p.GetOrientationDegrees(),'layers':p.GetLayerSet().FmtHex(),'offset':xy(p.GetOffset()),'zone_connection':int(p.GetLocalZoneConnection()),'thermal_spoke_angle':p.GetThermalSpokeAngleDegrees(),'thermal_gap_override':p.GetLocalThermalGapOverride(),'thermal_width_override':p.GetLocalThermalSpokeWidthOverride(),'roundrect_ratio':p.GetRoundRectRadiusRatio(),'chamfer_ratio':p.GetChamferRectRatio(),'solder_mask_margin':p.GetLocalSolderMaskMargin(),'solder_paste_margin':p.GetLocalSolderPasteMargin(),'solder_paste_ratio':p.GetLocalSolderPasteMarginRatio()}
 for g in f.GraphicalItems():out['footprint_graphics'][g.m_Uuid.AsString()]={'reference':f.GetReference(),**graphic(g)}
for t in b.GetTracks():
 d={'class':t.GetClass(),'net':t.GetNetname(),'start':xy(t.GetStart()),'end':xy(t.GetEnd()),'layer':int(t.GetLayer())}
 if t.GetClass()=='PCB_VIA':d.update(diameter=t.GetWidth(pcbnew.F_Cu),drill=t.GetDrill(),type=int(t.GetViaType()),layers=t.GetLayerSet().FmtHex())
 else:d['width']=t.GetWidth()
 out['tracks'][t.m_Uuid.AsString()]=d
for g in b.GetDrawings():out['drawings'][g.m_Uuid.AsString()]=graphic(g)
json.dump(out,open(sys.argv[2],'w'),indent=2);print({k:len(v) for k,v in out.items()})
