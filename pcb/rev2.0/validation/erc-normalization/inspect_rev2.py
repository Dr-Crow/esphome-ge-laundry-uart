from pathlib import Path
from schematic_parser import parse
r=Path('/workspace/shared/ge-oct4-rev2-erc-normalize');p=r/'pcb/rev2.0/design/OnionStraws.kicad_sch';s=p.read_text();a=parse(s)
def ref(n):return next(z.items[2] for z in n.all('property') if z.items[1]=='Reference')
for n in a.all('symbol'):
 if ref(n)=='U4':print(s[n.start:n.end])
libs={x.items[1]:x for x in a.one('lib_symbols').all('symbol')}
for n in a.all('symbol'):
 if ref(n)=='U4':print('LIB',s[libs[n.one('lib_id').items[1]].start:libs[n.one('lib_id').items[1]].end])
print('POWER')
for n in a.all('symbol'):
 if ref(n).startswith('#PWR') and 3.1<float(n.one('at').items[1])<3.4:print(ref(n),n.one('lib_id').v(),n.one('at').v())
print('WIRES')
for n in a.all('wire'):
 if any(3.1<float(pt.items[1])<3.4 and 1.1<float(pt.items[2])<2 for pt in n.one('pts').all('xy')):print(s[n.start:n.end])
print('LABELS')
for n in a.all('label')+a.all('global_label'):
 if n.items[1] in {'RXD','TXD','GLITCHES','DBG_LED','GEA3_RX','GEA3_TX'}:print(n.key(),n.items[1],n.one('at').v(),n.one('uuid').v())
