from pathlib import Path
from decimal import Decimal as D
import json,sys,uuid
sys.path.insert(0,str(Path(__file__).parent))
from schematic_parser import parse
root=Path('/workspace/shared/ge-oct4-rev1-erc-normalize'); sch=root/'pcb/rev1.0/design/OnionStraws.kicad_sch'
def fmt(x):return format(x.normalize(),'f') if x else '0'
def explicit_vcc(s,library):
 r=parse(s);container=r if library else r.one('lib_symbols');lib=next(x for x in container.all('symbol') if x.items[1] in {'74LVC2G07','LegacySymbols:74LVC2G07'})
 common=next(x for x in lib.all('symbol') if x.items[1]=='74LVC2G07_0_1');pin=next(x for x in common.all('pin') if x.one('number').items[1]=='5');old=s[pin.start:pin.end]
 assert '(at 0 2.54 90) (length 0) hide' in old
 new=old.replace('(at 0 2.54 90) (length 0) hide','(at 0 5.715 90) (length 3.175)')
 return s[:pin.start]+new+s[pin.end:]
s=sch.read_text();s=explicit_vcc(s,False);r=parse(s);patch=[];moves=[];wires=[]
for sym in r.all('symbol'):
 props={x.items[1]:x for x in sym.all('property')};ref=props['Reference'].items[2]
 if ref in {'#PWR0122','#PWR0135'}:
  at=sym.one('at').v();old=at[:2]
  for a in [sym.one('at')]+[x.one('at') for x in sym.all('property')]:
   v=a.v();v[1]=fmt(D(v[1])+D('6.35'));patch.append((a.start,a.end,'(at '+' '.join(v)+')'))
  end=(old[0],fmt(D(old[1])+D('6.35')));start=(old[0],fmt(D(old[1])+D('3.175')))
  wires.append(f'  (wire (pts (xy {start[0]} {start[1]}) (xy {end[0]} {end[1]})) (stroke (width 0) (type default) (color 0 0 0 0)) (uuid {uuid.uuid4()}))')
  moves.append({'reference':ref,'from_mm':old,'to_mm':list(end),'rotation_preserved':at[2],'explicit_pin_endpoint_mm':list(start)})
 if ref=='U1':
  for key in ['Reference','Value']:
   a=props[key].one('at');v=a.v();v[0]=fmt(D(v[0])-D('3.81'));patch.append((a.start,a.end,'(at '+' '.join(v)+')'))
for start,end,new in sorted(patch,reverse=True):s=s[:start]+new+s[end:]
s=s.rstrip();assert s[-1]==')';s=s[:-1]+'\n'+ '\n'.join(wires)+'\n)\n';sch.write_text(s)
library=sch.parent/'symbols/LegacySymbols.kicad_sym';library.write_text(explicit_vcc(library.read_text(),True))
proof={'symbol':'LegacySymbols:74LVC2G07','physical_pin':'U1.5','pinfunction_preserved':'VCC','pintype_preserved':'power_in','old_common_pin':{'local_at':['0','2.54','90'],'length_mm':'0','hidden':True},'new_common_pin':{'local_at':['0','5.715','90'],'length_mm':'3.175','hidden':False},'ground_pin_2_unchanged':True,'moved_existing_power_symbols':moves,'new_wire_count':2,'U1_reference_value_shift_x_mm':'-3.81','physical_instance_positions_rotations_pin_uuids_unchanged':True,'new_parts':0}
(Path(__file__).parent/'presentation-delta.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(proof,indent=2))
