import sys, xml.etree.ElementTree as ET
def load(f):
    r=ET.parse(f).getroot(); comps={}
    for c in r.find('components'):
        comps[c.get('ref')]=(c.findtext('value'),c.findtext('footprint'),c.findtext('datasheet'),tuple(sorted((p.get('name'),p.get('value')) for p in c.findall('property') if p.get('name')!='Sheetfile')))
    nets={}
    for n in r.find('nets'):
        nets[n.get('name')]=frozenset((x.get('ref'),x.get('pin')) for x in n.findall('node'))
    return comps,nets
ca,na=load(sys.argv[1]); cb,nb=load(sys.argv[2])
print('components added:',sorted(set(cb)-set(ca))); print('components removed:',sorted(set(ca)-set(cb)))
for r in sorted(set(ca)&set(cb)):
    if ca[r]!=cb[r]:
        print('CHANGED',r)
        for i,nm in enumerate(('value','footprint','datasheet')):
            if ca[r][i]!=cb[r][i]: print('   ',nm,ca[r][i],'->',cb[r][i])
        da=dict(ca[r][3]); db=dict(cb[r][3])
        for k in sorted(set(da)|set(db)):
            if da.get(k)!=db.get(k): print('    prop',k,da.get(k),'->',db.get(k))
print('nets added:',sorted(set(nb)-set(na))); print('nets removed:',sorted(set(na)-set(nb)))
for n in sorted(set(na)&set(nb)):
    if na[n]!=nb[n]: print('NET CHANGED',n,'added',sorted(nb[n]-na[n]),'removed',sorted(na[n]-nb[n]))
