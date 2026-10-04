"""Run sequential, all-severity genuine-native checks without rewriting source .pro."""
from pathlib import Path
import collections,hashlib,json,shutil,subprocess,sys,tempfile
import pcbnew
ROOT=Path(__file__).resolve().parent;REVIEW=ROOT.parent;DESIGN=REVIEW.parent/'design';REPORTS=REVIEW/'reports'
assert pcbnew.Version()=='9.0.9',pcbnew.Version()
def source_hashes():return {str(p.relative_to(DESIGN)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(DESIGN.rglob('*')) if p.is_file() and p.suffix not in ['.lck','.bak']}
initial=source_hashes()
with tempfile.TemporaryDirectory(prefix='rev2-native-validation-') as temp:
 work=Path(temp)/'design';shutil.copytree(DESIGN,work)
 sch=work/'OnionStraws.kicad_sch';pcb=work/'OnionStraws.kicad_pcb'
 commands=[['kicad-cli','sch','erc','--severity-all','--format','json','-o',str(REPORTS/'erc.json'),str(sch)],['kicad-cli','pcb','drc','--severity-all','--all-track-errors','--schematic-parity','--format','json','-o',str(REPORTS/'drc.json'),str(pcb)],['kicad-cli','sch','export','netlist','--format','kicadxml','-o',str(REVIEW/'netlist.xml'),str(sch)],['kicad-cli','sch','export','bom','--fields','Reference,Value,Footprint,${DNP},Description,LCSC','--labels','Reference,Value,Recovered Footprint,DNP,Description,LCSC','-o',str(REVIEW/'native-bom.csv'),str(sch)]]
 for command in commands:subprocess.run(command,check=True)
 erc=json.loads((REPORTS/'erc.json').read_text());events=[v for s in erc['sheets'] for v in s['violations']]
 drc=json.loads((REPORTS/'drc.json').read_text())
 assert len(events)==4 and all(v['severity']=='warning' and v['type']=='multiple_net_names' for v in events),events
 assert not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity'],drc
 meanings={'DBG_LED and GLITCHES':'Original debug LED label alias; DBG_LED stays canonical','GEA3_TX and RXD':'Original appliance-perspective GEA3_TX / ESP receive RXD alias; GEA3_TX stays canonical','GEA3_RX and TXD':'Original appliance-perspective GEA3_RX / ESP transmit TXD alias; GEA3_RX stays canonical','+5V and VCC':'Original +5V supply / hidden U4 VCC pin alias; original pin name and +5V net retained'}
 classifications=[]
 for event in events:
  record=dict(event);record['classification']=next(value for key,value in meanings.items() if key in event['description']);record['disposition']='Intentional source alias retained; original warning severity visible';classifications.append(record)
 (REPORTS/'warning-classification.json').write_text(json.dumps(classifications,indent=2)+'\n')
 summary={'native_version':pcbnew.Version(),'erc_errors':0,'erc_warnings':4,'drc_errors':0,'drc_warnings':0,'drc_unconnected_items':0,'schematic_parity_issues':0,'erc_arguments':['--severity-all','--format','json'],'drc_arguments':['--severity-all','--all-track-errors','--schematic-parity','--format','json'],'execution':'Byte-exact source copy; KiCad project-format migration confined to temporary directory','no_source_changes_during_validation':source_hashes()==initial}
 assert summary['no_source_changes_during_validation']
 (REPORTS/'native-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 (REPORTS/'source-hashes.json').write_text(json.dumps({'native_version':pcbnew.Version(),'source_sha256':initial,'reports_generated_from_byte_exact_source_copy':True},indent=2)+'\n')
 subprocess.run([sys.executable,str(ROOT/'verify_cleanup.py'),str(REVIEW/'netlist.xml')],check=True)
 print(json.dumps(summary,indent=2))
