"""Linear switched-current input-network screen; run with Python + numpy/scipy."""
import csv,itertools
from pathlib import Path
import numpy as np
from scipy.linalg import expm
out=Path(__file__).resolve().parent
rows=[]
# Effective source-L/R at connector; input TVS/eFuse regulation are outside this on-state model.
# State vector is cable current, pre-eFuse capacitor voltage, post-eFuse capacitor voltage, constant.
def screen(v,cap,freq,L,R,trace,ilow=.10,ihigh=.60):
    cf=.80e-6  # assumed biased effective C20 or C21 at the connector
    cb=(cap+.10)*1e-6  # C9 plus fitted C10
    resistance=.028+trace
    A=np.zeros((4,4))
    A[0]=[-R/L,-1/L,0,v/L]
    A[1]=[1/cf,-1/(cf*resistance),1/(cf*resistance),0]
    A[2]=[0,1/(cb*resistance),-1/(cb*resistance),0]
    period=1/freq; duty=min(1.,5/v)
    def phase(load,dt):
        h=A.copy();h[2,3]=-load/cb
        return expm(h*dt)
    def seq(I):
        return [phase(I,period*duty/4)]*4+[phase(0,period*(1-duty)/4)]*4
    def composite(steps):
        t=np.eye(4)
        for m in steps:t=m@t
        return t
    pre=seq(ilow);post=seq(ihigh);cycle=composite(pre)
    x=np.r_[np.linalg.solve(np.eye(3)-cycle[:3,:3],cycle[:3,3]),1.]
    trace_v=[];src_v=[]
    for _ in range(int(np.ceil(100e-6*freq))):
        for m in post:
            x=m@x;trace_v.append(x[2]);src_v.append(x[1])
    return (min(trace_v),max(trace_v),1000*np.ptp(trace_v[-8:]),min(src_v))
for v,nom in [(12.,3.386),(15.,2.548)]:
 for scale,L,R,hz,stack in itertools.product([.65,1.,1.2],[.25,1.,3.],[.15,.50,1.0],[.9,1.1],['1oz','half']):
    trace={'1oz':.015301,'half':.030683}[stack] # compact candidate J1 pin-1 inner trace, room temperature
    a=screen(v,nom*scale,hz*1e6,L*1e-6,R,trace)
    rows.append([v,scale,L,R,hz,stack,*[round(x,6) for x in a]])
with (out/'input-transient.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['source_V','C9_curve_multiplier','cable_uH','source_ohm','switch_MHz','inner_copper','min_buck_in_V','max_buck_in_V','settled_ripple_mVpp','min_pre_efuse_V']);w.writerows(rows)
for v in [12,15]:
 r=[i for i in rows if i[0]==v and i[5]=='half']
 print(v,'nominal examples',[i for i in r if i[1:5]==[1.,1.,.5,1.1]],'sweep Vmin and max ripple',min(i[6] for i in r),max(i[8] for i in r))

# Dropout sensitivity: assume the high-side switch stays on. This is a cable/input
# voltage calculation only; it cannot prove either module's 3.3 V rail or UVLO timing.
low=[]
for R,L,I,stack in itertools.product([.15,.50,1.],[.25,1.,3.],[.35,.60],['1oz','half']):
 trace={'1oz':.015301,'half':.030683}[stack]
 vmin,vmax,_,pre=screen(4.3,7.276,1.1e6,L*1e-6,R,trace,ihigh=I)
 low.append([R,L,I,stack,round(vmin,5),round(pre,5),round(4.3-I*(R+trace+.028),5)])
with (out/'low-line.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['source_ohm','cable_uH','load_A','inner','min_buck_in_V','min_pre_efuse_V','settled_buck_in_V']);w.writerows(low)
print('low-line', [r for r in low if r[1]==1 and r[2]==.60 and r[3]=='half'])
