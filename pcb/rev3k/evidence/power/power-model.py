"""DC copper, including layer transitions and both halves of the supply path."""
import json,math,csv,sys
import numpy as np,networkx as nx
from shapely.geometry import LineString,Point,Polygon
from shapely.ops import nearest_points
from scipy import sparse
from scipy.sparse.linalg import spsolve
d=json.load(open(sys.argv[1]));out=[]
for n,gd in d.items():
 ts=[(LineString([a,c]),w,l) for a,c,w,l in gd['tracks']];pos=[{0.,round(line.length,6)} for line,w,l in ts];g=nx.Graph();edges=[];contacts=[]
 def node(i,s):
  s=round(float(s),6);pos[i].add(s);return (i,s)
 def between(i,j,p,q):
  contacts.append((node(i,ts[i][0].project(p)),node(j,ts[j][0].project(q))))
 for i,(a,w,l) in enumerate(ts):
  for j,(c,v,h) in enumerate(ts[:i]):
   if h!=l or a.distance(c)>(w+v)/2+.0001:continue
   pa,pc=nearest_points(a,c);between(i,j,pa,pc)
   for coord in a.coords:
    p=Point(coord)
    if c.distance(p)<=(w+v)/2+.0001:between(i,j,p,p)
   for coord in c.coords:
    p=Point(coord)
    if a.distance(p)<=(w+v)/2+.0001:between(i,j,p,p)
 for p,ls,verts in gd['pads']:
  poly=Polygon(verts).buffer(0)
  for i,(a,w,l) in enumerate(ts):
   if l not in ls or a.distance(poly)>w/2+.0001:continue
   q,c=nearest_points(a,poly);contacts.append((p,node(i,a.project(q))))
   for co in a.coords:
    q=Point(co)
    if poly.distance(q)<=w/2+.0001:contacts.append((p,node(i,a.project(q))))
 for idx,(co,diam,drill) in enumerate(gd['vias']):
  p=Point(co);last=None
  for layer,z in enumerate([0,.22,1.32,1.6]):
   v=('via'+str(idx),layer)
   if last is not None:edges.append((last[0],v,.00001724*(z-last[1])/(math.pi*drill*.020),None))
   for i,(a,w,l) in enumerate(ts):
    if l==layer and a.distance(p)<=(diam+w)/2+.0001:contacts.append((v,node(i,a.project(p))))
   for name,ls,verts in gd['pads']:
    if layer in ls and Polygon(verts).distance(p)<diam/2:contacts.append((name,v))
   last=(v,z)
 for i,(line,w,l) in enumerate(ts):
  pts=sorted(pos[i])
  for a,c in zip(pts,pts[1:]):edges.append(((i,a),(i,c),.01724*(c-a)/w,l))
 uf=nx.utils.UnionFind()
 for a,c in contacts:uf.union(a,c)
 for inner in (30.48,15.2):
  G=nx.Graph()
  for a,c,R,l in edges:
   a,c=uf[a],uf[c]
   if a==c:continue
   res=R if l is None else R/(35 if l in (0,3) else inner)
   if res<=0:continue
   G.add_edge(a,c,w=G.get_edge_data(a,c,{}).get('w',0)+1/res)
  pairs={'VDC':[('J1.1','U9.5')],'/ALT_PWR':[('J1.3','U10.5')],'/V_INPUT':[('U9.6','U8.3'),('U10.6','U8.3')],'/BUCK_5V':[('L1.2','D11.2')],'/D11_K':[('D11.1','JP3.1')],'+5V':[('JP3.2','J6.7')],'+3V3':[('J6.5','U5.5'),('J6.5','C14.2')]}[n]
  for a,c in pairs:
   A,C=uf[a],uf[c]
   if A==C:res=0.
   else:
    nodes=list(nx.node_connected_component(G,A));assert C in nodes,(n,a,c)
    nodes.remove(A);nodes=[A]+nodes;lap=nx.laplacian_matrix(G.subgraph(nodes),nodelist=nodes,weight='w').tocsr()[1:,1:]
    i=nodes.index(C)-1;rhs=np.zeros(len(nodes)-1);rhs[i]=1.;res=float(spsolve(lap,rhs)[i])*1000
   out.append([n,a,c,inner,round(res,3),round(res*.60,3),round(res*1.01,3)])
with open(sys.argv[2],'w') as f:
 w=csv.writer(f);w.writerow(['net','source','sink','inner_um','path_mOhm','drop_at_0p6A_mV','drop_at_1p01A_mV']);w.writerows(out)
