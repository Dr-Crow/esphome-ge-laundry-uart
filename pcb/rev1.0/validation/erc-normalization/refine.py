from pathlib import Path
from decimal import Decimal as D
import sys,json,uuid
sys.path.insert(0,str(Path(__file__).parent))
from schematic_parser import parse
p=Path('/workspace/shared/ge-oct4-rev1-erc-normalize/pcb/rev1.0/design/OnionStraws.kicad_sch');s=p.read_text();r=parse(s);patch=[];added=[]
def f(x):return format(x.normalize(),'f') if x else '0'
for sym in r.all('symbol'):
 props={x.items[1]:x for x in sym.all('property')};ref=props['Reference'].items[2]
 if ref not in {'#PWR0122','#PWR0135'}:continue
 old=sym.one('at').v()[:2];new=[f(D(old[0])+D('5.08')),old[1]]
 for a in [sym.one('at')]+[x.one('at') for x in sym.all('property')]:
  v=a.v();v[0]=f(D(v[0])+D('5.08'));patch.append((a.start,a.end,'(at '+' '.join(v)+')'))
 added.append(f'  (wire (pts (xy {old[0]} {old[1]}) (xy {new[0]} {new[1]})) (stroke (width 0) (type default) (color 0 0 0 0)) (uuid {uuid.uuid4()}))')
for start,end,new in sorted(patch,reverse=True):s=s[:start]+new+s[end:]
s=s.rstrip();s=s[:-1]+'\n'+'\n'.join(added)+'\n)\n';p.write_text(s)
p=Path(__file__).parent/'presentation-delta.json';d=json.loads(p.read_text());d['new_wire_count']=4
for v in d['moved_existing_power_symbols']:v['to_mm'][0]=f(D(v['to_mm'][0])+D('5.08'));v['wire_bend_mm']=[v['from_mm'][0],v['to_mm'][1]]
d['layout_review_refinement']='Move each +5V arrow 5.08mm right with a right-angle lead to separate it from the visible vertical VCC pin name.'
p.write_text(json.dumps(d,indent=2)+'\n')
