from pathlib import Path
import json,hashlib,copy,xml.etree.ElementTree as ET,subprocess,sys
sys.path.insert(0,str(Path(__file__).parent))
from schematic_parser import parse,Node
ROOT=Path('/workspace/shared/ge-oct4-rev1-erc-normalize');PROOF=Path(__file__).parent
SOURCE='2088c3acbe2766541cf4b2daa4a5f45e6ed5e4da'
def digest(b):return hashlib.sha256(b).hexdigest()
def structure(n):return [structure(x) if isinstance(x,Node) else x for x in n.items]
def astsha(n):return digest(json.dumps(structure(n),separators=(',',':')).encode())
def pins(t):return sorted((e.get('ref'),e.get('pin'),n.get('name'),e.get('pinfunction',''),e.get('pintype','')) for n in t.findall('./nets/net') for e in n.findall('node'))
a,b=[ET.parse(PROOF/f'{x}.net.xml') for x in ['before','after']]; ar,br=pins(a),pins(b)
assert ar==br and len(ar)==166 and len(set((x[0],x[1]) for x in ar))==166
assert len(a.findall('./nets/net'))==len(b.findall('./nets/net'))==58
for key in ['components','libparts','libraries']:assert ET.tostring(a.find(key))==ET.tostring(b.find(key)),key
assert [(n.get('code'),n.get('name'),n.get('class')) for n in a.findall('./nets/net')]==[(n.get('code'),n.get('name'),n.get('class')) for n in b.findall('./nets/net')]
negative=ET.parse(PROOF/'negative-control.net.xml'); nr=pins(negative)
assert len(nr)==len(ar)==166 and nr!=ar
assert sorted(set(ar)-set(nr))==[('U1','5','+5V','VCC','power_in')]
assert sorted(set(nr)-set(ar))==[('U1','5','+3V3','VCC','power_in')]
# Current schematic instances are compared in full after discarding only the
# approved display coordinates of U1 Reference/Value and moved +5V annotations.
schpath='pcb/rev1.0/design/OnionStraws.kicad_sch'
oldtext=subprocess.check_output(['git','show',SOURCE+':'+schpath],cwd=ROOT).decode();newtext=(ROOT/schpath).read_text();old,new=parse(oldtext),parse(newtext)
def instancehashes(r):
 d={}
 for n in r.all('symbol'):
  props={x.items[1]:x for x in n.all('property')};ref=props['Reference'].items[2]
  if ref in {'#PWR0122','#PWR0135'}:
   n=copy.deepcopy(n)
   for a in [n.one('at')]+[x.one('at') for x in n.all('property')]:
    a.items[1]='annotation_x';a.items[2]='annotation_y'
  n=copy.deepcopy(n)
  if ref=='U1':
   for p in n.all('property'):
    if p.items[1] in {'Reference','Value'}:p.items=[x for x in p.items if not (isinstance(x,Node) and x.key()=='at')]
  d[n.one('uuid').items[1]]=astsha(n)
 return d
assert instancehashes(old)==instancehashes(new)
delta=json.loads((PROOF/'presentation-delta.json').read_text())
for move in delta['moved_existing_power_symbols']:
 before=next(n for n in old.all('symbol') if next(p.items[2] for p in n.all('property') if p.items[1]=='Reference')==move['reference'])
 after=next(n for n in new.all('symbol') if n.one('uuid').v()==before.one('uuid').v())
 assert before.one('at').v()[:2]==move['from_mm'] and after.one('at').v()[:2]==move['to_mm']
 assert after.one('at').v()[2]==before.one('at').v()[2]
for n in new.all('symbol'):
 ref=next(p.items[2] for p in n.all('property') if p.items[1]=='Reference')
 if ref=='U1':
  before=next(o for o in old.all('symbol') if o.one('uuid').v()==n.one('uuid').v())
  from decimal import Decimal
  for prop in n.all('property'):
   if prop.items[1] in {'Reference','Value'}:
    origin=next(o for o in before.all('property') if o.items[1]==prop.items[1])
    assert Decimal(prop.one('at').v()[0])==Decimal(origin.one('at').v()[0])-Decimal('3.81')
    assert prop.one('at').v()[1:]==origin.one('at').v()[1:]
# Whole original library definition is compared, allowing only the recorded
# visible pin5 presentation. Pin number/function/type remain unchanged.
libpath='pcb/rev1.0/design/symbols/LegacySymbols.kicad_sym'; oldlib=subprocess.check_output(['git','show',SOURCE+':'+libpath],cwd=ROOT).decode();newlib=(ROOT/libpath).read_text()
oldlib=oldlib.replace('(pin power_in line (at 0 2.54 90) (length 0) hide\n          (name "VCC"','(pin power_in line (at 0 5.715 90) (length 3.175)\n          (name "VCC"')
assert astsha(parse(oldlib))==astsha(parse(newlib))
oldembed=oldtext.replace('(pin power_in line (at 0 2.54 90) (length 0) hide\n          (name "VCC"','(pin power_in line (at 0 5.715 90) (length 3.175)\n          (name "VCC"')
assert astsha(parse(oldembed).one('lib_symbols'))==astsha(new.one('lib_symbols'))
for key in ['junction','no_connect','label','global_label','bus','bus_entry','text','sheet']:
 assert [astsha(x) for x in old.all(key)]==[astsha(x) for x in new.all(key)],key
assert {astsha(x) for x in old.all('wire')}.issubset({astsha(x) for x in new.all('wire')})
assert len(new.all('wire'))-len(old.all('wire'))==4
tracked=json.loads((PROOF/'before-tracked-sha256.json').read_text())
assert all(digest(subprocess.check_output(['git','show',SOURCE+':'+n],cwd=ROOT))==d['sha256'] for n,d in tracked.items())
changed=[n for n,d in tracked.items() if digest((ROOT/n).read_bytes())!=d['sha256']]
assert changed==['pcb/rev1.0/design/OnionStraws.kicad_sch','pcb/rev1.0/design/symbols/LegacySymbols.kicad_sym']
protected={n:d for n,d in tracked.items() if (n.startswith('firmware/') or n.endswith('.kicad_pcb') or n.endswith('.kicad_pro') or n.endswith('.kicad_prl') or '/manufacturing/' in n or '/review-manufacturing/' in n or '/footprints/' in n)}
for n,d in protected.items():assert digest((ROOT/n).read_bytes())==d['sha256'],n
cam=json.loads((PROOF/'fresh-cam-comparison.json').read_text());assert len(cam)==11 and all(x['equal_after_only_generation_date_checksum_normalization'] for x in cam)
report={'source_commit':SOURCE,'tool':'KiCad 9.0.9','physical_graph':{'pins_before':166,'pins_after':166,'nets_before':58,'nets_after':58,'membership_sha256':digest(json.dumps(ar,separators=(',',':')).encode()),'removed':[],'added':[],'component_metadata_identical':True,'library_pin_metadata_identical':True,'net_codes_names_classes_identical':True},'physical_metadata':{'all_original_symbol_anchors_rotations_pin_uuids_property_values_and_instance_attributes_identical':True,'approved_display_coordinate_exceptions':'U1 Reference/Value text, #PWR0122/#PWR0135 moved power annotations only','all_original_wires_junctions_labels_no_connects_preserved':True,'new_physical_parts':0,'footprints':61,'native_pad_records':174,'route_segments':351,'vias':26,'pcb_sha256':tracked['pcb/rev1.0/design/OnionStraws.kicad_pcb']['sha256']},'protected_bytes':{'count':len(protected),'all_identical':True,'files':protected},'negative_control':{'kind':'native export of detached schematic fixture replacing both U1-unit +5V annotations with +3V3','candidate_and_source_checkouts_modified':False,'pins_166_and_metadata_still_same':True,'changed_pin_detected':{'removed':sorted(set(ar)-set(nr)),'added':sorted(set(nr)-set(ar))}},'cam_comparison':cam,'no_project_grid_severity_exclusion_or_rule_changes':True,'qualification':{'hardware_qualified':False,'fabrication_approved':False,'ratings_modules_procurement_assembly_rotations_physical_and_appliance_gates_open':True}}
report['candidate_commit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
report['all_tracked_byte_preservation']={'baseline_count':161,'unchanged':159,'changed':changed,'all_physical_CAM_BOM_CPL_firmware_other_revisions_original_artifacts_identical':True}
oldphys=json.loads((PROOF/'before-board-physical.json').read_text());newphys=json.loads((PROOF/'after-board-physical.json').read_text());assert oldphys==newphys
fixture=copy.deepcopy(newphys);key=next(k for k,v in fixture['pads'].items() if v['reference']=='U1' and v['number']=='5');fixture['pads'][key]['net']='+3V3';assert oldphys!=fixture
report['native_board_snapshot']={'before_after_equal':True,'counts':{k:len(v) for k,v in oldphys.items()},'sha256':digest((PROOF/'after-board-physical.json').read_bytes()),'metadata_negative_control':{'kind':'Comparison-only fixture moves U1 pad5 +5V to +3V3 while retaining geometry and pad count','detected':True,'source_or_candidate_files_modified':False}}
erc=json.loads((PROOF/'after-erc.json').read_text());drc=json.loads((PROOF/'after-drc.json').read_text());assert erc['kicad_version']=='9.0.9' and not [v for sh in erc['sheets'] for v in sh['violations']];assert drc['kicad_version']=='9.0.9' and not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity']
(PROOF/'proof.json').write_text(json.dumps(report,indent=2)+'\n')
(PROOF/'physical-pin-memberships.json').write_text(json.dumps(br,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in {'protected_bytes','cam_comparison'}},indent=2));print('Protected byte-exact files:',len(protected))
