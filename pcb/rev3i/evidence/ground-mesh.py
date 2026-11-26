"""Four-layer resistive mesh of the actual GND fills, with plated GND vias and connector pins.
Run using /usr/bin/python3 with KiCad 9 pcbnew, NumPy and SciPy. Input is a board filename.
Mesh width is in mm. Contact snapping and the treatment of thermal spokes are approximations."""
import sys,csv
from pathlib import Path
import pcbnew as k,numpy as np
from scipy.sparse import coo_matrix,csgraph
from scipy.sparse.linalg import spsolve
b=k.LoadBoard(sys.argv[1]);step=float(sys.argv[2]);ofile=sys.argv[3];nx=int(99/step);ny=int(40/step)
zones={z.GetLayer():z for z in b.Zones() if z.GetNetname()=='GND'}
layers=[k.F_Cu,k.In1_Cu,k.In2_Cu,k.B_Cu];edges=[];nn=0;indexes=[]
def vec(x,y):return k.VECTOR2I(round(x*1e6),round(y*1e6))
import collections,math
metal=collections.defaultdict(list)
def register(obj,layers):
 bb=obj.GetBoundingBox();a,c=bb.GetOrigin(),bb.GetEnd()
 for layer in layers:
  for i in range(math.floor(a.x/3e6),math.floor(c.x/3e6)+1):
   for j in range(math.floor(a.y/3e6),math.floor(c.y/3e6)+1):metal[layer,i,j].append(obj)
for f in b.GetFootprints():
 for p in f.Pads():
  if p.GetNetname()=='GND':register(p,[ly for ly in layers if p.IsOnLayer(ly)])
for t in b.GetTracks():
 if t.GetNetname()=='GND':register(t,layers if t.GetClass()=='PCB_VIA' else [t.GetLayer()])
def filled(x,y):
 pt=vec(x,y);return polys.Collide(pt) or any(o.HitTest(pt) for o in metal.get((layer,math.floor(x/3),math.floor(y/3)),[]))
for layer,num in zip(layers,range(4)):
 polys=zones[layer].GetFilledPolysList(layer)
 grid=np.full((nx,ny),-1,dtype=int)
 for i in range(nx):
  for j in range(ny):
   x=(i+.5)*step;y=(j+.5)*step
   if not filled(x,y):continue
   grid[i,j]=nn
   if i>0 and grid[i-1,j]>=0 and filled(x-step/2,y):edges.append((grid[i-1,j],nn,num,0))
   if j>0 and grid[i,j-1]>=0 and filled(x,y-step/2):edges.append((grid[i,j-1],nn,num,0))
   nn+=1
 indexes.append(grid)
contacts=[]
for t in b.GetTracks():
 if t.GetClass()=='PCB_VIA' and t.GetNetname()=='GND':
  p=t.GetStart();contacts.append((None,p.x/1e6,p.y/1e6,t.GetDrillValue()/1e6))
for f in b.GetFootprints():
 for pad in f.Pads():
  if pad.GetNetname()=='GND' and pad.GetDrillSize().x>0:
   p=pad.GetPosition();contacts.append((f.GetReference()+'.'+pad.GetNumber(),p.x/1e6,p.y/1e6,pad.GetDrillSize().x/1e6))
pins={}
for name,x,y,diam in contacts:
 last=None
 for l,g in enumerate(indexes):
  i,j=int(x/step),int(y/step);span=int(.85/step)+1
  opts=[(((ii+.5)*step-x)**2+((jj+.5)*step-y)**2,g[ii,jj]) for ii in range(max(0,i-span),min(i+span+1,nx)) for jj in range(max(0,j-span),min(j+span+1,ny)) if g[ii,jj]>=0]
  if not opts:continue
  ds,node=min(opts)
  if ds>.85**2:continue
  if last:
   z=[0,.22,1.32,1.6];R=.00001724*(z[l]-z[last[0]])/(np.pi*diam*.020)
   edges.append((last[1],node,4,R))
  if name and l==0:pins[name]=node
  last=(l,node)
a,c,ly,r=np.array(edges).T;a=a.astype(int);c=c.astype(int);rows=[]
for inner in [30.48,15.2]:
 gs=np.divide(1,r,out=np.ones_like(r),where=r>0);gs[ly==0]=gs[ly==3]=35/.01724;gs[ly==1]=gs[ly==2]=inner/.01724
 rr=np.r_[a,c,a,c];cc=np.r_[a,c,c,a]
 M=coo_matrix((np.r_[gs,gs,-gs,-gs],(rr,cc)),shape=(nn,nn)).tocsr()
 _,labels=csgraph.connected_components(M);src=pins['J1.8'];dst=pins['J6.6'];active=np.where((labels==labels[src])&(np.arange(nn)!=src))[0]
 assert dst in active
 rhs=(active==dst).astype(float);sol=spsolve(M[active][:,active],rhs);res=float(sol[np.where(active==dst)[0][0]])
 rows.append([step,inner,res*1000,.60*res*1000,len(active),len(contacts)])
print(rows)
with open(ofile,'a') as f:csv.writer(f).writerows(rows)
