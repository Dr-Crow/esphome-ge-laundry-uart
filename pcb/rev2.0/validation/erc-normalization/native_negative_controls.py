"""Native-export source-fixture controls, scoped to a temporary copy of Rev2 design."""
from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile,xml.etree.ElementTree as ET
from schematic_parser import parse
R=Path('/workspace/shared/ge-oct4-rev2-erc-normalize');P=Path(__file__).parent;D=R/'pcb/rev2.0/design'
def rows(path):return sorted((n.attrib['ref'],n.attrib['pin'],net.attrib['name'],n.attrib.get('pinfunction',''),n.attrib.get('pintype','')) for net in ET.parse(path).findall('./nets/net') for n in net.findall('node'))
def sourcehash():return {str(p.relative_to(D)):hashlib.sha256(p.read_bytes()).hexdigest() for p in D.rglob('*') if p.is_file()}
initial=sourcehash();baseline=rows(P/'after.net.xml');out=[]
for kind in ['power','uart']:
 with tempfile.TemporaryDirectory(prefix='rev2-negative-native-') as td:
  temp=Path(td)/'design';shutil.copytree(D,temp);sch=temp/'OnionStraws.kicad_sch';s=sch.read_text();a=parse(s);patch=[]
  if kind=='power':
   for n in a.all('symbol'):
    if next(x.items[2] for x in n.all('property') if x.items[1]=='Reference') not in {'#PWR028','#PWR034'}:continue
    raw=s[n.start:n.end];raw=raw.replace('"LegacySymbols:+5V"','"LegacySymbols:+3V3"').replace('(property "Value" "+5V"','(property "Value" "+3V3"');patch.append((n.start,n.end,raw))
  else:
   for n in a.all('global_label'):
    if n.one('at').items[1]!='223.52' or n.items[1] not in {'GEA3_TX','GEA3_RX'}:continue
    raw=s[n.start:n.end];new={'GEA3_TX':'GEA3_RX','GEA3_RX':'GEA3_TX'}[n.items[1]];patch.append((n.start,n.end,raw.replace('"'+n.items[1]+'"','"'+new+'"',1)))
  assert len(patch)==2
  for start,end,val in sorted(patch,reverse=True):s=s[:start]+val+s[end:]
  sch.write_text(s);net=P/(kind+'-negative-native.net.xml');subprocess.run(['kicad-cli','sch','export','netlist','--format','kicadxml','-o',str(net),str(sch)],check=True);fixture=rows(net)
  assert len(fixture)==len(baseline)==186 and baseline!=fixture
  removed=sorted(set(baseline)-set(fixture));added=sorted(set(fixture)-set(baseline));expected=1 if kind=='power' else 2;assert len(removed)==len(added)==expected
  if kind=='power':assert removed==[('U4','5','+5V','VCC','power_in')] and added==[('U4','5','+3V3','VCC','power_in')]
  else:assert {(r,p) for r,p,*_ in removed}=={('U2','11'),('U2','12')}
  out.append({'native_version':'9.0.9','fixture_kind':kind,'mutation':'Temporary copied design only; original explicit +5V annotations -> +3V3' if kind=='power' else 'Temporary copied design only; swap canonical global labels on U2 physical11 and12 processor-side wires','input_source_files_modified':False,'native_export_unique_pin_count':len(fixture),'baseline_unique_pin_count':len(baseline),'detected':True,'removed':removed,'added':added,'pin_names_types_preserved':[(x[0],x[1],x[3],x[4]) for x in baseline]==[(x[0],x[1],x[3],x[4]) for x in fixture]})
assert sourcehash()==initial
(P/'native-negative-controls.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
