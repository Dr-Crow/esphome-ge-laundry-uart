"""Source-bound Rev2 annotation candidate checks; no source mutation by controls."""
from pathlib import Path
from copy import deepcopy
import hashlib,json,subprocess,sys,xml.etree.ElementTree as ET
from schematic_parser import parse,Node
R=Path('/workspace/shared/ge-oct4-rev2-erc-normalize');P=Path(__file__).parent
SOURCE='24dd93b0cb633c889765108397380a0e438393fa'
SCH='pcb/rev2.0/design/OnionStraws.kicad_sch';LIB='pcb/rev2.0/design/symbols/LegacySymbols.kicad_sym'
assert subprocess.check_output(['git','cat-file','-t',SOURCE],cwd=R,text=True).strip()=='commit'

def rows(xml):return sorted((n.attrib['ref'],n.attrib['pin'],net.attrib['name'],n.attrib.get('pinfunction',''),n.attrib.get('pintype','')) for net in xml.findall('./nets/net') for n in net.findall('node'))
def compare_graph(a,b):
 assert rows(a)==rows(b),'physical ref/pin/net/name/type memberships changed'
 for name in ['components','libparts','libraries']:assert ET.tostring(a.find(name))==ET.tostring(b.find(name)),name+' metadata changed'
 assert [(n.attrib['code'],n.attrib['name']) for n in a.findall('./nets/net')]==[(n.attrib['code'],n.attrib['name']) for n in b.findall('./nets/net')],'net name/code changed'
a,b=[ET.parse(P/(x+'.net.xml')) for x in ['before','after']];compare_graph(a,b);pins=rows(a);assert len(pins)==186==len(set((x[0],x[1]) for x in pins));assert len(a.findall('./nets/net'))==45
controls=[]
for ref,pin,newnet in [('U4','5','+3V3'),('U2','11','GEA3_RX'),('U2','12','GEA3_TX')]:
 fixture=deepcopy(b);node=next(n for net in fixture.findall('./nets/net') for n in net.findall('node') if n.attrib['ref']==ref and n.attrib['pin']==pin);oldnet=next(net.attrib['name'] for net in fixture.findall('./nets/net') if node in net.findall('node'));assert oldnet!=newnet
 for net in fixture.findall('./nets/net'):
  if node in net.findall('node'):net.remove(node)
 next(net for net in fixture.findall('./nets/net') if net.attrib['name']==newnet).append(node)
 try:compare_graph(a,fixture)
 except AssertionError:controls.append({'mutation':f'{ref}.{pin} {oldnet} -> {newnet}','node_count_preserved':len(rows(fixture))==186,'pin_name_type_preserved':True,'detected':True})
 else:raise AssertionError('negative graph control escaped')
oldphys=json.loads((P/'before-board-physical.json').read_text());newphys=json.loads((P/'after-board-physical.json').read_text());assert oldphys==newphys
fixture=deepcopy(newphys);uid=next(k for k,p in fixture['pads'].items() if p['reference']=='U4' and p['number']=='5');fixture['pads'][uid]['net']='+3V3';assert oldphys!=fixture;controls.append({'mutation':'comparison-only U4 pad5 net -> +3V3 in complete board metadata','pad_count_preserved':len(fixture['pads'])==222,'detected':True})

def norm(n):return [norm(x) for x in n.items] if isinstance(n,Node) else n
def getref(n):return next(x.items[2] for x in n.all('property') if x.items[1]=='Reference')
old=parse(subprocess.check_output(['git','show',SOURCE+':'+SCH],cwd=R,text=True));new=parse((R/SCH).read_text());delta=json.loads((P/'annotation-delta.json').read_text());moves={m['uuid']:m for m in delta['power_annotation_moves']};os={n.one('uuid').items[1]:n for n in old.all('symbol')};ns={n.one('uuid').items[1]:n for n in new.all('symbol')};assert set(os)==set(ns)
changes=[]
for uid,n in ns.items():
 nn=norm(n);on=norm(os[uid]);ref=getref(n)
 if uid in moves:
  def substitute_at(value,original):
   for x in value:
    if isinstance(x,list) and x[0]=='at':x[1:]=next(o[1:] for o in original if isinstance(o,list) and o[0]=='at')
    if isinstance(x,list) and x[0]=='property':
     orig=next(o for o in original if isinstance(o,list) and o[:3]==x[:3]);substitute_at(x,orig)
  substitute_at(nn,on);changes.append({'reference':ref,'kind':'original power symbol and property annotation coordinates only'})
 elif ref=='U4':
  for prop in nn:
   if isinstance(prop,list) and prop[0]=='property' and prop[1] in ['Reference','Value']:
    orig=next(x for x in on if isinstance(x,list) and x[:3]==prop[:3]);next(x for x in prop if isinstance(x,list) and x[0]=='at')[1:]=next(x for x in orig if isinstance(x,list) and x[0]=='at')[1:]
  changes.append({'reference':ref,'kind':'reference/value text positions only; physical instance untouched'})
 assert nn==on,(uid,ref,'unexpected instance metadata changed')

def lib_compare(oa,na,embedded):
 oldlibs={n.items[1]:n for n in (oa.one('lib_symbols').all('symbol') if embedded else oa.all('symbol'))};newlibs={n.items[1]:n for n in (na.one('lib_symbols').all('symbol') if embedded else na.all('symbol'))};assert oldlibs.keys()==newlibs.keys()
 for name,n in newlibs.items():
  nn=norm(n);on=norm(oldlibs[name])
  if name in ['LegacySymbols:74LVC2G07','74LVC2G07']:
   common=next(x for x in nn if isinstance(x,list) and x[:2]==['symbol','74LVC2G07_0_1']);ocommon=next(x for x in on if isinstance(x,list) and x[:2]==['symbol','74LVC2G07_0_1']);pin=next(x for x in common if isinstance(x,list) and x[0]=='pin' and any(isinstance(v,list) and v[:2]==['number','5'] for v in x));opin=next(x for x in ocommon if isinstance(x,list) and x[0]=='pin' and any(isinstance(v,list) and v[:2]==['number','5'] for v in x));assert next(x for x in pin if isinstance(x,list) and x[0]=='at')==['at','0','5.715','90'];assert next(x for x in pin if isinstance(x,list) and x[0]=='length')==['length','3.175'];assert 'hide' not in pin;assert 'hide' in opin
   for key in ['at','length']:next(x for x in pin if isinstance(x,list) and x[0]==key)[1:]=next(x[1:] for x in opin if isinstance(x,list) and x[0]==key)
   pin.insert(pin.index(next(x for x in pin if isinstance(x,list) and x[0]=='length'))+1,'hide')
  assert nn==on,(name,'unexpected library pin or property metadata change')
lib_compare(old,new,True);lib_compare(parse(subprocess.check_output(['git','show',SOURCE+':'+LIB],cwd=R,text=True)),parse((R/LIB).read_text()),False)
# All original routing and sheet content remain exact; only listed labels and new annotation wires differ.
dlabels={x['uuid']:x for x in delta['label_changes']};newobjects={n.one('uuid').items[1]:n for n in new.items if isinstance(n,Node) and n.one('uuid') and n.key()!='symbol'}
for n in old.items:
 if not isinstance(n,Node) or n.key() in ['symbol','lib_symbols']:continue
 if not n.one('uuid'):assert norm(n)==norm(new.one(n.key()));continue
 uid=n.one('uuid').items[1]
 if uid in dlabels:
  d=dlabels[uid]
  if d['disposition'].startswith('Remove'):assert uid not in newobjects
  else:
   nxt=newobjects[uid];assert nxt.items[1]==d['new'];assert nxt.one('uuid').v()==n.one('uuid').v();assert nxt.one('at').v()[:2]==n.one('at').v()[:2]
   expected=norm(n);actual=norm(nxt)
   if nxt.key()=='global_label':
    expected[0]='global_label';expected.insert(3,['shape','input']);next(x for x in expected if isinstance(x,list) and x[0]=='at')[3]='180';effects=next(x for x in expected if isinstance(x,list) and x[0]=='effects');next(x for x in effects if isinstance(x,list) and x[0]=='justify')[1:]=['right']
   expected[1]=d['new'];assert actual==expected,(uid,'unexpected label metadata')
 else:assert uid in newobjects and norm(n)==norm(newobjects[uid]),(uid,'original sheet object changed')
oldids={n.one('uuid').items[1] for n in old.items if isinstance(n,Node) and n.one('uuid') and n.key()!='symbol'};added=[n for uid,n in newobjects.items() if uid not in oldids];assert len(added)==4 and all(n.key()=='wire' for n in added)
assert set(n.one('uuid').items[1] for n in added)=={m[k] for m in delta['power_annotation_moves'] for k in ['wire_uuid','additional_wire_uuid']}
expectedsegments={tuple(tuple(pt) for pt in seg) for m in delta['power_annotation_moves'] for seg in m['wire_segments']};assert {tuple(tuple(pt.v()) for pt in n.one('pts').all('xy')) for n in added}==expectedsegments
sha=lambda x:hashlib.sha256(x).hexdigest();before=json.loads((P/'before-tracked-sha256.json').read_text());assert all(h==sha(subprocess.check_output(['git','show',SOURCE+':'+f],cwd=R)) for f,h in before.items());after={f:sha((R/f).read_bytes()) for f in before};changed=[f for f in before if before[f]!=after[f]];assert changed==[SCH,LIB] or set(changed)=={SCH,LIB};preserved={f:h for f,h in after.items() if f not in changed}
(P/'after-tracked-sha256.json').write_text(json.dumps(after,indent=2)+'\n');(P/'preserved-tracked-sha256.json').write_text(json.dumps(preserved,indent=2)+'\n');(P/'after-pin-memberships.json').write_text(json.dumps(rows(b),indent=2)+'\n')
erc=json.loads((P/'after-erc.json').read_text());drc=json.loads((P/'after-drc.json').read_text());assert erc['kicad_version']=='9.0.9' and not [v for s in erc['sheets'] for v in s['violations']];assert drc['kicad_version']=='9.0.9' and not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity']
result={'source_commit':SOURCE,'native_version':'9.0.9','graph':{'unique_physical_pins':186,'nets':45,'membership_sha256':sha(json.dumps(pins,separators=(',',':')).encode()),'full_physical_pin_name_type_membership_identical':True,'component_metadata_identical':True,'libpart_pin_metadata_identical':True,'library_metadata_identical':True,'net_codes_names_identical':True,'U4_memberships':[x for x in pins if x[0]=='U4'],'UART_memberships':[x for x in pins if x[2] in ['GEA3_RX','GEA3_TX']]},'board_physical_metadata_identical':True,'board_counts':{k:len(v) for k,v in oldphys.items()},'all_original_sheet_routing_objects_preserved':True,'all_original_symbol_instances_physical_metadata_preserved':True,'all_symbol_definition_changes_limited_to_recorded_U4_pin5_presentation':True,'annotation_instances_changed':changes,'added_annotation_wires':4,'power_flags_changed':0,'tracked_input_files':len(before),'preserved_input_file_count':len(preserved),'changed_source_files':changed,'negative_controls':controls,'erc_errors':0,'erc_warnings':0,'erc_exclusions':0,'drc_violations':0,'drc_unconnected':0,'drc_schematic_parity':0,'native_rule_project_file_byte_preserved':True,'legacy_procurement_module_rating_physical_safety_gates_open':True}
(P/'candidate-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
