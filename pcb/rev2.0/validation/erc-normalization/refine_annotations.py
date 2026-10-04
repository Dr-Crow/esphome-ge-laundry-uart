from pathlib import Path
import json,uuid
from decimal import Decimal as D
from schematic_parser import parse
r=Path('/workspace/shared/ge-oct4-rev2-erc-normalize');p=r/'pcb/rev2.0/design/OnionStraws.kicad_sch';s=p.read_text();a=parse(s);patch=[]
fmt=lambda v:format(v.normalize(),'f') if v else '0'
ref=lambda n:next(x.items[2] for x in n.all('property') if x.items[1]=='Reference')
dp=Path(__file__).parent/'annotation-delta.json';d=json.loads(dp.read_text())
for n in a.all('label'):
 if n.items[1] not in {'GEA3_TX','GEA3_RX'}:continue
 uid=n.one('uuid').items[1];raw=s[n.start:n.end]
 if n.one('at').items[1]=='207.01':
  patch.append((n.start,n.end,''));next(x for x in d['label_changes'] if x['uuid']==uid)['disposition']='Remove redundant local alias already wired to original same-net global label; physical wiring unchanged'
 else:
  raw=raw.replace('(label ','(global_label ',1).replace('(at '+ ' '.join(n.one('at').v())+')','(at '+n.one('at').items[1]+' '+n.one('at').items[2]+' 180)',1).replace('(fields_autoplaced yes)','(shape input)\n\t\t(fields_autoplaced yes)',1).replace('(justify left bottom)','(justify right)',1)
  patch.append((n.start,n.end,raw));next(x for x in d['label_changes'] if x['uuid']==uid)['disposition']='Use original canonical global net name on unchanged connector attachment coordinate, matching original global shape input'
lib=next(n for n in a.one('lib_symbols').all('symbol') if n.items[1]=='LegacySymbols:74LVC2G07');pin=next(n for n in next(n for n in lib.all('symbol') if n.items[1]=='74LVC2G07_0_1').all('pin') if n.one('number').items[1]=='5')
for node,val in [(pin.one('at'),'(at 0 5.715 90)'),(pin.one('length'),'(length 3.175)')]:patch.append((node.start,node.end,val))
for n in a.all('symbol'):
 if ref(n) not in {'#PWR028','#PWR034'}:continue
 for at in [n.one('at')]+[x.one('at') for x in n.all('property')]:
  v=at.v();v[0]=fmt(D(v[0])+D('5.08'));v[1]=fmt(D(v[1])+D('3.175'));patch.append((at.start,at.end,'(at '+' '.join(v)+')'))
 move=next(x for x in d['power_annotation_moves'] if x['reference']==ref(n));old=move['old_at'];x,y=D(old[0]),D(old[1]);endpoint=y+D('3.175');ay=y+D('6.35');ax=x+D('5.08');move['new_at']=[fmt(ax),fmt(ay),old[2]];move['explicit_pin_endpoint']=[fmt(x),fmt(endpoint)];move['additional_wire_uuid']=str(uuid.uuid5(uuid.NAMESPACE_URL,'ge-rev2-erc-normalize:bend:'+n.one('uuid').items[1]));move['wire_segments']=[[[fmt(x),fmt(endpoint)],[fmt(x),fmt(ay)]],[[fmt(x),fmt(ay)],[fmt(ax),fmt(ay)]]]
 wire=next(w for w in a.all('wire') if w.one('uuid').items[1]==move['wire_uuid']);raw=f'\t(wire\n\t\t(pts (xy {fmt(x)} {fmt(endpoint)}) (xy {fmt(x)} {fmt(ay)}))\n\t\t(stroke (width 0) (type default))\n\t\t(uuid "{move["wire_uuid"]}")\n\t)';patch.append((wire.start,wire.end,raw))
 extra=f'\n\t(wire\n\t\t(pts (xy {fmt(x)} {fmt(ay)}) (xy {fmt(ax)} {fmt(ay)}))\n\t\t(stroke (width 0) (type default))\n\t\t(uuid "{move["additional_wire_uuid"]}")\n\t)\n';patch.append((a.end-1,a.end-1,extra))
for start,end,val in sorted(patch,reverse=True):s=s[:start]+val+s[end:]
p.write_text(s)
p=p.parent/'symbols/LegacySymbols.kicad_sym';s=p.read_text();a=parse(s);lib=next(n for n in a.all('symbol') if n.items[1]=='74LVC2G07');pin=next(n for n in next(n for n in lib.all('symbol') if n.items[1]=='74LVC2G07_0_1').all('pin') if n.one('number').items[1]=='5');patch=[(pin.one('at').start,pin.one('at').end,'(at 0 5.715 90)'),(pin.one('length').start,pin.one('length').end,'(length 3.175)')]
for start,end,val in sorted(patch,reverse=True):s=s[:start]+val+s[end:]
p.write_text(s)
d['symbol_definition_change']='74LVC2G07 pin 5 VCC/power_in/name/number/angle preserved; visible explicit length 3.175mm lead from original body contact at local (0,2.54) to endpoint (0,5.715), mirrored in embedded and local library definitions; GND pin2 unchanged'
dp.write_text(json.dumps(d,indent=2)+'\n')
