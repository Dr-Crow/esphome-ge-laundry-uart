"""Verify this bounded Rev2 cleanup using genuine KiCad pcbnew and fresh XML netlist.
Run: kicad-python verify_cleanup.py PATH_TO_CURRENT_NETLIST_XML
The frozen input evidence reflects the UUID-backed reference and pinless-DNP metadata
corrections captured before this cleanup. No power flag is an electrical qualification.
"""
from pathlib import Path
import collections,decimal,hashlib,json,re,subprocess,sys,tempfile,xml.etree.ElementTree as ET
import pcbnew
from kicad_sexpr import Atom,parse,child,children,val
ROOT=Path(__file__).resolve().parent;DESIGN=ROOT.parent.parent/'design'
sha=lambda o:hashlib.sha256(json.dumps(o,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
assert pcbnew.Version()=='9.0.9',pcbnew.Version()
# Generate fresh native geometry with all original routes, pads, footprints and graphics.
with tempfile.TemporaryDirectory() as temp:
 path=Path(temp)/'geometry.json'
 subprocess.run([sys.executable,str(ROOT/'native_snapshot.py'),str(DESIGN/'OnionStraws.kicad_pcb'),str(path)],check=True)
 before=json.loads((ROOT/'input-geometry.json').read_text());current=json.loads(path.read_text())
 authorized={'081246d5-7787-4c04-a448-b62e3ba337a9'}
 for uid in authorized:
  assert before['pads'][uid]['thermal_spoke_angle']==90.0
  assert current['pads'][uid]['thermal_spoke_angle']==45.0
  expected=dict(before['pads'][uid]);expected['thermal_spoke_angle']=45.0
  assert current['pads'][uid]==expected
  before['pads'][uid]=expected
 for uid in ['00d77d43-f542-4542-8700-7511e643f1f0','7a3be8be-71f0-415b-b9dc-8b4bc442a08d']:
  assert before['footprint_graphics'][uid]['reference']=='U2'
  assert before['footprint_graphics'][uid]['layer']==int(pcbnew.F_SilkS)
  del before['footprint_graphics'][uid]
 for uid in ['646b6289-7915-4bf1-b4c3-366890826a55','508c05f0-87b7-4e2e-ad56-0ca055349409']:
  assert before['footprint_graphics'][uid]['reference']=='J1'
  before['footprint_graphics'][uid]['end'][0]=131500000
 assert before==current,'Unexpected component/pad/route/drawing change'
 # Independently compare complete pad source definitions, including custom copper
 # primitives, masks/paste, drills, pinfunction/pintype and all original settings.
 # Numeric spelling and order of the layer-set names are representation only.
 def normalize_pad(node):
  if isinstance(node,list):
   result=[normalize_pad(v) for v in node]
   if result and result[0]=='layers':return [result[0],*sorted(result[1:])]
   return result
  if isinstance(node,Atom) and re.match(r'^-?\d+(\.\d+)?$',str(node)):
   return str(decimal.Decimal(str(node)).normalize())
  return str(node)
 originalpcb=parse(subprocess.check_output(['git','show','d02a00776768ee9a45962089be5a58e84adf5d52:pcb/rev2.0/design/OnionStraws.kicad_pcb'],cwd=DESIGN,text=True))
 currentpcb=parse((DESIGN/'OnionStraws.kicad_pcb').read_text())
 rawpads=lambda source:{str(val(p,'uuid')):normalize_pad(p) for f in children(source,'footprint') for p in children(f,'pad')}
 originalpads=rawpads(originalpcb);currentpads=rawpads(currentpcb)
 thermal=child(currentpads['081246d5-7787-4c04-a448-b62e3ba337a9'],'thermal_bridge_angle')
 assert thermal==['thermal_bridge_angle','45']
 currentpads['081246d5-7787-4c04-a448-b62e3ba337a9'].remove(thermal)
 assert originalpads==currentpads,'Unexpected complete pad definition change'
 # This includes exact native LayerSet.FmtHex equality for every pad, including NPTH.
 assert len(current['footprints'])==73 and len(current['pads'])==222 and len(current['tracks'])==712
 frozen=json.loads((ROOT/'input-schematic-fingerprint.json').read_text());sch=parse((DESIGN/'OnionStraws.kicad_sch').read_text())
 assert sha([n for n in sch if not isinstance(n,list) or n[0] not in ['symbol','lib_symbols']])==frozen['top_level_except_symbols_sha256'],'Original wires/labels/junctions/text/image/sheet data changed'
 smap={n['source_symbol']:n['project_symbol'] for n in json.loads((DESIGN/'symbols/source-map.json').read_text())}
 fmap={n['reference']:n for n in json.loads((DESIGN/'footprints/source-map.json').read_text())}
 symbols={str(val(n,'uuid')):n for n in children(sch,'symbol')}
 for uid,original in frozen['symbols_by_uuid'].items():
  expected=json.loads(json.dumps(original));lib=child(expected,'lib_id');lib[1]=smap[lib[1]]
  ref=next(p[2] for p in children(expected,'property') if p[1]=='Reference')
  if ref in fmap:
   fp=next(p for p in children(expected,'property') if p[1]=='Footprint')
   assert fp[2]==fmap[ref]['source_footprint'];fp[2]=fmap[ref]['project_footprint']
  assert symbols[uid]==expected,(uid,ref,'Unexpected original schematic instance change')
 added=[n for uid,n in symbols.items() if uid not in frozen['symbols_by_uuid']]
 assert len(added)==3 and all(val(n,'lib_id')=='LegacySymbols:PWR_FLAG' and val(n,'in_bom')=='no' and val(n,'on_board')=='no' for n in added)
 embedded={str(n[1]):n for n in children(child(sch,'lib_symbols'),'symbol')}
 library=parse((DESIGN/'symbols/LegacySymbols.kicad_sym').read_text());libs={str(n[1]):n for n in children(library,'symbol')}
 for oldid,digest in frozen['embedded_symbol_definitions'].items():
  local=smap[oldid];name=local.split(':',1)[1];e=embedded[local]
  assert sha([e[0],name,*e[2:]])==digest,(oldid,'Embedded definition changed')
  assert sha(libs[name])==digest,(oldid,'Recovered library definition changed')
 assert len(libs)==25
 # Every project property including original classes, severities and exclusions is unchanged
 # apart from the proven 50mil -> 25mil connection-grid configuration.
 original=json.loads((ROOT/'input-project.json').read_text());project=json.loads((DESIGN/'OnionStraws.kicad_pro').read_text())
 assert original['schematic']['connection_grid_size']==50.0
 assert project['schematic']['connection_grid_size']==25.0
 project['schematic']['connection_grid_size']=50.0;assert project==original
 coords=[]
 for n in parse(subprocess.check_output(['git','show','d02a00776768ee9a45962089be5a58e84adf5d52:pcb/rev2.0/design/OnionStraws.kicad_sch'],cwd=DESIGN,text=True)):
  if not isinstance(n,list) or not n:continue
  if n[0] in ['wire','bus']:
   coords.extend((str(n[0]),float(p[1]),float(p[2])) for p in children(child(n,'pts'),'xy'))
  elif n[0] in ['symbol','label','global_label','junction','no_connect','hierarchical_label']:
   p=child(n,'at');coords.append((str(n[0]),float(p[1]),float(p[2])))
 off=lambda grid:[p for p in coords if any(abs(x/grid-round(x/grid))>1e-5 for x in p[1:])]
 assert len(coords)==725 and not off(.635)
 # Compare complete electrical partitions, including single-pin intentionally unconnected nets.
 def netlist(path):
  root=ET.parse(path).getroot();pins={};groups={};components={c.attrib['ref']:c for c in root.find('components')}
  for net in root.find('nets'):
   group=frozenset((n.attrib['ref'],n.attrib['pin']) for n in net.findall('node'));groups[net.attrib['name']]=group
   for key in group:pins[key]=net.attrib['name']
  return pins,groups,components
 oldpins,oldgroups,oldcomp=netlist(ROOT/'input-netlist.xml');pins,groups,comp=netlist(Path(sys.argv[1]))
 assert len(pins)==186 and pins==oldpins and groups==oldgroups and len(comp)==75
 board=pcbnew.LoadBoard(str(DESIGN/'OnionStraws.kicad_pcb'));boardpins={};boardgroups=collections.defaultdict(set)
 for f in board.GetFootprints():
  for p in f.Pads():
   if p.GetNumber():
    key=(f.GetReference(),p.GetNumber());net=p.GetNetname()
    assert key not in boardpins or boardpins[key]==net
    boardpins[key]=net;boardgroups[net].add(key)
 assert boardpins==pins and {n:frozenset(g) for n,g in boardgroups.items()}==groups
 original_archive=DESIGN.parent/'manufacturing/PCBA-OnionStraws-rev2.0.zip'
 archivehash=hashlib.sha256(original_archive.read_bytes()).hexdigest()
 assert archivehash=='b9c0b397806d3a719c32faa83c08bac2e80aa1c1d4d27d3e6d6a35cd5381445a'
 result={'native_version':pcbnew.Version(),'original_electrical_pin_memberships':len(pins),'electrical_net_partitions':len(groups),'source_component_count_including_pinless_H3_H4':len(comp),'board_footprint_count':73,'pad_definition_count':222,'track_via_item_count':712,'original_schematic_connection_object_coordinates':len(coords),'original_coordinates_off_50mil_grid':len(off(1.27)),'original_coordinates_off_25mil_grid':len(off(.635)),'complete_pad_definition_changes_except_authorized_thermal_angle':0,'pad_layer_set_changes':0,'footprint_placement_changes':0,'route_changes':0,'board_drawing_changes':0,'original_schematic_wire_label_text_image_changes':0,'original_symbol_definition_changes':0,'authorized_pad_setting_changes':['U4.2 thermal spoke angle 90deg -> 45deg'],'authorized_silk_graphics':['remove two U2 overhang graphics','clip two J1 overhang segment ends at x=131.5mm'],'project_changes':['connection_grid_size 50mil -> 25mil only'],'original_pcba_archive_sha256':archivehash}
 (ROOT/'verification-summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
