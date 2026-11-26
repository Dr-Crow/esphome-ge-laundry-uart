"""Generate the Rev 3J enclosure from its verified 3I parent. Units are mm."""
from pathlib import Path
import json, math
import build123d as b

here = Path(__file__).resolve().parent
parent = here.parents[1] / "rev3i/case"
data = json.loads((here / "board-datums.json").read_text())
seat = 3.65
def center(rev, ref):
    x,y = data[rev][ref]["center"]
    return x,(40 if rev=="3I" else 39.45)-y
def pins(ref):
    return [(x,39.45-y) for x,y in data["3J"][ref]["pads"].values()]
def box(x0,x1,y0,y1,z0,z1):
    return b.Pos(x0,y0,z0)*b.Box(x1-x0,y1-y0,z1-z0,align=(b.Align.MIN,)*3)
def cyl(r, z0, z1, xy):
    return b.Pos(*xy,z0)*b.Cylinder(r,z1-z0,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
def volume(s):
    return sum(v.volume for v in s.solids()) if s is not None else 0
def line_depth(s,x,y):
    ray=b.Edge.make_line((x,y,seat),(x,y,-1))
    hit=s.intersect(ray)
    return min([seat-v.Z for e in hit.edges() for v in e.vertices() if v.Z<=seat+1e-5],default=4.65) if hit else 4.65
def write(s,name):
    assert s.is_valid and len(s.solids())==1,name
    b.export_step(s,here/(name+".step"));b.export_stl(s,here/(name+".stl"))
def shift(ref):
    i,j=center("3I",ref),center("3J",ref)
    return tuple(j[k]-i[k] for k in (0,1))
records={"case_frame":"physical y = 39.45 - PCB y, x unchanged; board bottom z = 3.65","units":"mm"}
for ref in ["J5","J6","D4","D5","D6"]:
    assert math.dist(center("3I",ref),center("3J",ref))<.00001,ref
base=b.import_step(parent/"matching-base.step")
for r in ["H1","H2"]:
    # The base floor is 2.4 high. Rebuild only the locating posts above it.
    base-=cyl(3.02,2.4,5.56,center("3I",r))
    base+=cyl(3,2.38,seat,center("3J",r))+cyl(1.25,seat-.02,5.55,center("3J",r))
jx,jy=shift("J1")
# Preserve both the shifted jack window and clearance to the existing wall.
window=box(-10,1,40-25.925+jy,40-7.74+jy,4.75,18.2)
base-=window
base-=box(-.2,19,40-26+jy,40-7.7+jy,.65,2.46)
for ref in ["J7","JP3"]:
    pp=pins(ref);xs,ys=zip(*pp)
    base-=box(min(xs)-1.4,max(xs)+1.4,min(ys)-1.4,max(ys)+1.4,.15,2.46)
records['post_centers']={r:center("3J",r) for r in ["H1","H2"]}
records['tail_free_depth']={r:[round(line_depth(base,*p),3) for p in pins(r)] for r in ["J7","JP3","J5","J6","J1"]}
assert min(records['tail_free_depth']['JP3']+records['tail_free_depth']['J7'])>=3.499
write(base,"matching-base")
outline=box(0,90.13165,39.45-37.94012,39.45,seat,seat+1.6)
for r in ["H1","H2"]:outline-=cyl(1.6,seat-.1,seat+1.7,center('3J',r))
assert volume(base & outline)<.00001
records['pcb_to_base_intersection_mm3']=round(volume(base & outline),6)
for m in ["c3","c6"]:
    name="closed-usb-lid-"+m
    lid=b.import_step(parent/(name+".step"))-window
    for ref in ["H1","H2"]:
        # Recenter only the lower bore on the new post; 0.25 mm nominal radial fit.
        lid-=cyl(1.5,5.5,9,center("3J",ref))
    records[m]={}
    for name2,obj in [('base',base),('carrier',outline),('RJ45_window',window)]:
        v=volume(lid & obj);assert v<.00001,(m,name2,v);records[m][name2+'_overlap_mm3']=round(v,6)
    wall=[]
    for y in (8.10,10.5,12.92,15.0,17.75):
        for z in (18.4,19.3,20.3,21.4):
            ray=b.Edge.make_line((91.136,40-y,z),(101.2,40-y,z))
            hit=lid.intersect(ray);wall.append(sum(v.length for v in hit.edges()) if hit else 0)
    assert min(wall)>1,(m,wall);records[m]['min_usb_wall_over_20_rays']=round(min(wall),3)
    write(lid,name)
caps=json.loads((here.parents[1]/"rev3g/case/src/current_carrier_bounds.json").read_text())
for n in ["wifi","bus","aux"]:
    pipe=b.import_step(parent/("lightpipe-"+n+".step"))
    for rec in caps['records']:
        if 'body_max_dimensions_mm' not in rec:continue
        ref=rec['reference'];x,y=center("3J",ref);x0,x1,y0,y1,z0,z1=rec['bounds_mm']
        sx=(x1-x0)/2+.25;sy=(y1-y0)/2+.25
        envelope=box(x-sx,x+sx,y-sy,y+sy,z0,z1+.4)
        pipe-=envelope;assert volume(pipe & envelope)<1e-5
    write(pipe,'lightpipe-'+n)
records['outside_xyz_mm']=[round(s,4) for s in base.bounding_box().size]
(here/'case-checks.json').write_text(json.dumps(records,indent=2)+'\n')
print(records,flush=True)
