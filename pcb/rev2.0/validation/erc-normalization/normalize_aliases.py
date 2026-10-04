from pathlib import Path
from decimal import Decimal as D
import json,uuid
from schematic_parser import parse
r=Path('/workspace/shared/ge-oct4-rev2-erc-normalize');p=r/'pcb/rev2.0/design/OnionStraws.kicad_sch';s=p.read_text();a=parse(s);patch=[];labels=[];moves=[]
fmt=lambda v:format(v.normalize(),'f') if v else '0'
ref=lambda n:next(x.items[2] for x in n.all('property') if x.items[1]=='Reference')
for n in a.all('label'):
 if n.items[1] not in {'GLITCHES','RXD','TXD'}:continue
 old=n.items[1];new={'GLITCHES':'DBG_LED','RXD':'GEA3_TX','TXD':'GEA3_RX'}[old]
 raw=s[n.start:n.end];patch.append((n.start,n.end,raw.replace('"'+old+'"','"'+new+'"',1)))
 labels.append({'uuid':n.one('uuid').items[1],'old':old,'new':new,'at':n.one('at').v()})
lib=next(n for n in a.one('lib_symbols').all('symbol') if n.items[1]=='LegacySymbols:74LVC2G07');common=next(n for n in lib.all('symbol') if n.items[1]=='74LVC2G07_0_1');pin=next(n for n in common.all('pin') if n.one('number').items[1]=='5');assert pin.items[2]=='line' and 'hide' in pin.items
raw=s[pin.start:pin.end];assert '(length 0) hide' in raw;patch.append((pin.start,pin.end,raw.replace('(length 0) hide','(length 0)',1)))
for n in a.all('symbol'):
 if ref(n) in {'#PWR028','#PWR034'}:
  old=n.one('at').v()
  for at in [n.one('at')]+[x.one('at') for x in n.all('property')]:
   v=at.v();v[1]=fmt(D(v[1])+D('3.175'));patch.append((at.start,at.end,'(at '+' '.join(v)+')'))
  x,y=D(old[0]),D(old[1]);wire_uuid=str(uuid.uuid5(uuid.NAMESPACE_URL,'ge-rev2-erc-normalize:'+n.one('uuid').items[1]))
  wire=f'\n\t(wire\n\t\t(pts (xy {fmt(x)} {fmt(y)}) (xy {fmt(x)} {fmt(y+D("3.175"))}))\n\t\t(stroke (width 0) (type default))\n\t\t(uuid "{wire_uuid}")\n\t)\n'
  patch.append((a.end-1,a.end-1,wire));moves.append({'reference':ref(n),'uuid':n.one('uuid').items[1],'old_at':old,'new_at':[old[0],fmt(y+D('3.175')),old[2]],'wire_uuid':wire_uuid,'pin':'U4.5','net':'+5V'})
 if ref(n)=='U4':
  for prop in n.all('property'):
   if prop.items[1] not in {'Reference','Value'}:continue
   at=prop.one('at');v=at.v();v[0]=fmt(D(v[0])-D('3.81'));patch.append((at.start,at.end,'(at '+' '.join(v)+')'))
for start,end,value in sorted(patch,reverse=True):s=s[:start]+value+s[end:]
p.write_text(s)
p=p.parent/'symbols/LegacySymbols.kicad_sym';s=p.read_text();a=parse(s);lib=next(n for n in a.all('symbol') if n.items[1]=='74LVC2G07');common=next(n for n in lib.all('symbol') if n.items[1]=='74LVC2G07_0_1');pin=next(n for n in common.all('pin') if n.one('number').items[1]=='5');raw=s[pin.start:pin.end];assert '(length 0) hide' in raw;s=s[:pin.start]+raw.replace('(length 0) hide','(length 0)',1)+s[pin.end:];p.write_text(s)
(Path(__file__).parent/'annotation-delta.json').write_text(json.dumps({'label_changes':labels,'power_annotation_moves':moves,'symbol_definition_change':'74LVC2G07 physical pin 5 VCC/power_in/length 0/original coordinates preserved; remove hidden presentation in embedded and local library definition only','u4_reference_value_text_x_translation_mm':'-3.81','hardware_pins_changed':0,'ground_pin_2_hidden_presentation_unchanged':True,'power_flags_changed':0},indent=2)+'\n')
print('Canonicalized',len(labels),'labels; made U4.5 visible; extended',len(moves),'original +5V annotations')
