from pathlib import Path
import hashlib,json,subprocess,xml.etree.ElementTree as ET
r=Path('/workspace/shared/ge-oct4-rev2-erc-normalize'); p=Path('/workspace/shared/ge-oct4-rev2-erc-normalize-proof')
paths=subprocess.check_output(['git','ls-files','-z'],cwd=r).decode().split('\0'); paths=[x for x in paths if x]
h={x:hashlib.sha256((r/x).read_bytes()).hexdigest() for x in paths}
(p/'before-tracked-sha256.json').write_text(json.dumps(h,indent=2)+'\n')
n=ET.parse(p/'before.net.xml'); rows=sorted((e.attrib['ref'],e.attrib['pin'],net.attrib['name'],e.attrib.get('pinfunction',''),e.attrib.get('pintype','')) for net in n.findall('./nets/net') for e in net.findall('node'))
(p/'before-pin-memberships.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Tracked files',len(h),'Memberships',len(rows),'Nets',len(n.findall('./nets/net')))
print('U4',[x for x in rows if x[0]=='U4'])
