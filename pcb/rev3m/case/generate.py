"""Rev 3M enclosure, millimetres. Rebuild with build123d 0.10."""
from pathlib import Path
import sys, json, math
import build123d as b
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root.parent.parent/'rev3k'/'case'/'support'))
import enclosure as e
from antenna_clearance import check_c3_reservations
e.configure(stack_mm=11.,reach_mode='per_assembly',usb_mode='per_assembly')
def box(x0,x1,y0,y1,z0,z1):
    return b.Pos(x0,y0,z0)*b.Box(x1-x0,y1-y0,z1-z0,align=(b.Align.MIN,)*3)
def cyl(x,y,r,z0,z1):
    return b.Pos(x,y,z0)*b.Cylinder(r,z1-z0,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
def shell(z0,z1,x0=-2.4,x1=64.744000,y0=-5.,y1=30.432000,t=1.8):
    return box(x0,x1,y0,y1,z0,z1)-box(x0+t,x1-t,y0+t,y1-t,z0-.1,z1+.1)
def vol(s):
    return sum(v.volume for v in s.solids()) if s is not None else 0.
def save(s,name):
    assert s.is_valid and len(s.solids())==1,(name,len(s.solids()),s.is_valid)
    b.export_step(s,root/(name+'.step'));b.export_stl(s,root/(name+'.stl'),tolerance=.03,angular_tolerance=.22)
def module(s):
    return b.Pos(-39.33935000,-9.21799800,0)*e.to_physical(s)
def point(x,y):
    return [x+(-39.33935000),30.78200200-y]
seat=3.65
posts=[(3.091446, 3.086239), (54.374195, 3.087)]
base=box(-2.4,64.744000,-5,30.432000,-1.4,0)+shell(-.1,6.8)
# The tongue under the C3 antenna stays below its lower edge (z = 8 mm).
# The three other tongues keep their full height for both module lids.
for x0,x1 in [(4,17),(44.944,57.944)]:
    for y0,y1 in [(-3.35,-2.15),(27.581999999999997,28.782)]:
        tongue_top = 7.65 if x0 == 4 and y0 < 0 else 8.9
        base+=box(x0,x1,y0,y1,6.35,tongue_top)
        by=-3.18 if y0<0 else 28.612
        base+=cyl((x0+x1)/2,by,.13,7.3,min(8.23, tongue_top))
for x,y in posts:base+=cyl(x,y,2.6,-.03,seat)+cyl(x,y,1.23,seat-.05,5.55)
# Jack external body extends to x=-0.38. Allow both connector insertion and plug latch.
window=box(-4,1,7.082817999999999,25.582818,4.65,18.45);base-=window
carrier=box(0,59.944,0,27.432,seat,seat+1.6)
for x,y in posts:carrier-=cyl(x,y,1.6,seat-.1,seat+1.7)
assert vol(base & carrier)<1e-5
save(base,'common-base')
checks={'pcb_mm':[59.944,27.432,1.6],'assembled_outer_mm':[67.144,35.432,31.9],'floor_to_pcb_underside_mm':seat,'board_to_base_mm3':vol(carrier & base),'stack_assumption_mm':11,'case_frame':'x=PCB x, y=27.432 - PCB y, PCB underside z=3.65','posts_xy':posts,'c3_ufl_xy':point(78.873,12.9175)}
led=[('D4', 44.696867, 5.360356), ('D5', 47.341867, 5.732469), ('D6', 51.298334, 6.9745)]
fpc=box(4.5,44.5,-2.95,-1.15,8.,28.)
# Side-mounted FPC leaves the roof leaves free. Feed exits the upper half near the right end.
# Radius 5 mm elbow leading from antenna toward socket; z fixed above regulator.
z=21.8;cx,cy=34.53365000,12.86450200
path=[(39.53365000,17.86450200,20.),(39.53365000,17.86450200,z),(cx,17.86450200,z)]
for i in range(1,11):
    a=math.radians(90+9*i);path.append((cx+5*math.cos(a),cy+5*math.sin(a),z))
path.extend([(cx-5,1,z),(cx-5,-.8,z)])
tube=None
for a,c in zip(path,path[1:]):
    v=b.Vector(c)-b.Vector(a)
    seg=b.Solid.make_cylinder(1.0,v.length,b.Plane(origin=a,z_dir=v))
    tube=seg if tube is None else tube+seg
checks.update(check_c3_reservations('base', base, fpc, tube))
for name,x,y in led:
    oy=y
    pipe=cyl(x,y,.88,6.9,30.52)
    pipe+=cyl(x,oy,1.18,27.95,28.5)
    save(pipe,'lightpipe-'+name)
for m in ['c3','c6']:
    lid=shell(6.8,30.5)+box(-2.4,64.744000,-5,30.432000,28.5,30.5)
    lid-=window
    # Relief the tongue strip to a 0.08 mm nominal interference only near each raised bump.
    for x0,x1 in [(3.75,17.25),(44.694,58.194)]:
        lid-=box(x0,x1,-3.45,-2.0,6.79,9.12)
        lid-=box(x0,x1,27.432,28.881999999999998,6.79,9.12)
        for ya,yb in [(-3.5,-3.25),(28.682,28.932)]:
            lid+=box((x0+x1)/2-.5,(x0+x1)/2+.5,ya,yb,7.25,8.3)
    for x,y in posts:
        # Carrier retention sleeve stops 0.37 mm above the mounted PCB at rest.
        lid+=cyl(x,y,2.0,5.62,28.6)-cyl(x,y,1.53,5.61,8.3)
    for name in ['BOOT','RESET']:
        lid-=module(e.flexure_void(m,name));lid+=module(e.flexure(m,name));lid+=module(e.button_stop(m,name))
    for ref,x,y in led:lid-=cyl(x,y,.99,28.35,30.65)
    if m=='c3':
        # Short upper/lower side-wall rails at both ends. Open installation face.
        for x0,x1 in [(18.0,20.4),(42.2,44.8)]:
            lid+=box(x0,x1,-3.8,-.7,7.3,7.85);lid+=box(x0,x1,-1.02,-.55,7.6,9.5)
            lid+=box(x0,x1,-3.3,-.7,28.12,28.65)
        lid=lid.solids()[0].fuse(*lid.solids()[1:]) if len(lid.solids())>1 else lid.solids()[0]
        checks['c3_lead_path_mm']=round(sum(math.dist(a,c) for a,c in zip(path,path[1:])),2)
        checks['c3_coax_points_case_xyz']=path
    else:
        ceramic=module(e.B(77.5285,79.7285,13.3415,18.7415,17.85,19.05))
        checks['c6_ceramic_to_lid_min_mm']=round(lid.distance_to(ceramic),4)
    # Engrave the fixed roof outside the compliant leaves and cable reservation.
    for txt,x,y,size in [('UNPLUG RJ45 BEFORE USB',19.,26.631999999999998,1.6),('GEA 3M  '+m.upper(),18.,4.2,1.8)]+[(name,*[point(*xy)[0],point(*xy)[1]+4.65],1.35) for name,xy in e.SW[m].items()]:
        letters=b.Text(txt,font_size=size,font='DejaVu Sans')
        lid-=b.Pos(x,y,30.15)*b.extrude(letters,amount=.45)
    if m == 'c3':
        checks.update(check_c3_reservations('lid', lid, fpc, tube))
    checks[m+'_board_overlap_mm3']=round(vol(lid & carrier),6)
    checks[m+'_closure_interference_mm3']=round(vol(lid & base),6)
    checks[m+'_switches_case_xy']={name:point(*xy) for name,xy in e.SW[m].items()}
    checks[m+'_lid_pipe_overlap_mm3']={ref:round(vol(lid & b.import_step(root/('lightpipe-'+ref+'.step'))),6) for ref,_,_ in led}
    assert checks[m+'_board_overlap_mm3']<.001
    assert all(x<.001 for x in checks[m+'_lid_pipe_overlap_mm3'].values()),checks
    save(lid,'closed-usb-lid-'+m)
checks['light_guides_case_xy']={ref:[x,y] for ref,x,y in led}
checks['nominal_board_to_sleeve_gap_mm']=0.37
(root/'case-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(checks)
