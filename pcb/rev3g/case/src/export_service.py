from pathlib import Path
import json
import build123d as b
import enclosure as e
e.OUT=Path(__file__).resolve().parents[1]/'parts';e.OUT.mkdir(exist_ok=True)
e.configure(stack_mm=11.0,reach_mode='per_assembly',usb_mode='per_assembly',usb_style='original',rj45_style='original')
record={}
for mod in ('c3','c6'):
 s=e.shell(mod,'internal',closed_usb=True)
 # In the maker's KiCad frame, cast axial rays across the entire connector mouth,
 # over the documented socket-height range. A usable USB plug needs a clear corridor.
 thickness=[]
 for y in (8.10,10.5,12.92,15.0,17.75):
  for z in (18.4,19.3,20.3,21.4):
   edge=b.Edge.make_line((100.004,y,z),(110,y,z))
   hit=s.intersect(edge)
   lengths=[v.length for v in hit.edges()] if hit is not None else []
   assert sum(lengths)>1,(mod,y,z,lengths)
   thickness.append(sum(lengths))
 probe=e.B(91.939,100.003,8.041,17.794,16.8,22.7)
 common=s.intersect(probe)
 vol=sum(o.volume for o in common.solids()) if common else 0
 if vol>=.0001:
  print(mod, [(str(v.bounding_box()),v.volume) for v in common.solids()],flush=True)
  # Compare with the open-port parent to distinguish inherited proxy overlaps.
  parent=e.shell(mod,'internal',closed_usb=False)
  added=s-parent
  intrusion=added.intersect(probe)
  new_overlap=sum(o.volume for o in intrusion.solids()) if intrusion else 0
  assert new_overlap < .0001, (mod,new_overlap)
 else:
  new_overlap=0
 record[mod]={'min_sampled_axial_wall_mm':round(min(thickness),3),'max_sampled_axial_wall_mm':round(max(thickness),3),'plug_corridor_rays':len(thickness),'socket_mouth_box_overlap_mm3':vol,'added_material_box_overlap_mm3':new_overlap,'lid':e.export(s,'closed-usb-lid-'+mod)}
record['base']=e.export(e.base(),'matching-base')
for n,(a,z) in e.PIPES.items():record[n]=e.export(e.pipe_with_cap_relief(n),'lightpipe-'+n.lower())
(Path(__file__).resolve().parents[1]/'case-checks.json').write_text(json.dumps(record,indent=2))
print(record)
