import glob,json,sys,pcbnew as k
b=k.LoadBoard(sys.argv[1]);nets=['VDC','/ALT_PWR','/V_INPUT','/BUCK_5V','/D11_K','+5V','+3V3'];d={n:{'pads':[],'vias':[],'tracks':[]} for n in nets};layers=[k.F_Cu,k.In1_Cu,k.In2_Cu,k.B_Cu]
def xy(a):return [i/1e6 for i in a]
for f in b.GetFootprints():
 for pad in f.Pads():
  n=pad.GetNetname()
  if n not in d:continue
  ly=[i for i,l in enumerate(layers) if pad.IsOnLayer(l)]
  poly=pad.GetEffectivePolygon(layers[ly[0]]);o=poly.COutline(0);d[n]['pads'].append([f.GetReference()+'.'+pad.GetNumber(),ly,[xy(o.CPoint(i)) for i in range(o.PointCount())]])
for t in b.GetTracks():
 n=t.GetNetname()
 if n not in d:continue
 if isinstance(t,k.PCB_VIA):d[n]['vias'].append([xy(t.GetPosition()),t.GetWidth(k.F_Cu)/1e6,t.GetDrillValue()/1e6])
 else:d[n]['tracks'].append([xy(t.GetStart()),xy(t.GetEnd()),t.GetWidth()/1e6,layers.index(t.GetLayer())])
json.dump(d,open(sys.argv[2],'w'))
