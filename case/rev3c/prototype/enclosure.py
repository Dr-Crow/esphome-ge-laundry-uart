"""Tapered universal Rev3C enclosure, source-backed review concept (millimetres).

Common snap-fit base; chip-specific tops with direct printed compliant buttons.
PCB/firmware are not modified. Heights and moving fits remain prototypes.
"""
from pathlib import Path
import json, math
from build123d import *
import interface_baseline as e

ROOT=Path(__file__).parent
OUT=ROOT/'exports'
CX,CY=49.5,20.0
SEAM=6.8
ROOF=30.5
UNDER=28.5
BTN={} # button coordinates are module-specific, exactly above the switches
SW={'c3':{'BOOT':(79.0,8.4725),'RESET':(79.0,17.3625)},
    'c6':{'BOOT':(97.3483,19.4927),'RESET':(97.3483,6.3355)}}
# C6 switch height is conditional on Alps SKTAAAE010 being the fitted part.
# C3 height is provisional. Final foot length is set from a measured assembly.
SW_TOP={'c3':20.00,'c6':19.03}
REST_GAP=.25
STROKE=.40
SCREWS=((-2.4,3.8),(-2.4,36.2),(101.4,3.8),(101.4,36.2))
PIPES={'WIFI':((84.,26.),(70.,32.)),
       'AUX':((84.,30.),(80.25,32.)),
       'BUS':((88.,26.),(90.5,32.))}
B=e._box
C=e._cylinder
def rr(w,h,r,z):
    return Pos(CX,CY,z)*RectangleRounded(w,h,r)
def rrsolid(w,h,r,z0,z1):
    return extrude(rr(w,h,r,z0),amount=z1-z0)
def cy(r,y0,y1,x,z):
    return Cylinder(r,y1-y0,align=(Align.CENTER,Align.CENTER,Align.MIN)).locate(Location((x,y1,z),(90,0,0)))
def xopening(width,height,r,y,z):
    # Rounded aperture through the X end wall, sized to a USB plug envelope.
    sk=Plane.YZ.offset(-10)*Pos(y,z)*RectangleRounded(width,height,r)
    return extrude(sk,amount=122)
def rib_between(a,b,z0,z1,width=2.2):
    dx,dy=b[0]-a[0],b[1]-a[1]
    angle=math.degrees(math.atan2(dy,dx)); length=math.hypot(dx,dy)
    box=Box(length,width,z1-z0,align=(Align.CENTER,Align.CENTER,Align.MIN))
    box=Pos((a[0]+b[0])/2,(a[1]+b[1])/2,z0)*Rot(Z=angle)*box
    return box+C(width/2,z0,z1,*a)+C(width/2,z0,z1,*b)
def pipe_shape(bottom,top,r,z0=6.75,z1=30.48):
    # Actual CAD, not a renderer-only light streak. Optical function untested.
    x0,y0=bottom; x1,y1=top
    return loft([Pos(x0,y0,z0)*Circle(r),Pos(x0,y0,9.0)*Circle(r),
                 Pos(x1,y1,26.8)*Circle(r),Pos(x1,y1,z1)*Circle(r)],ruled=True)
def legend(text,x,y,size=1.7):
    sk=Pos(x,y,ROOF-.26)*Text(text,size,font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    return extrude(sk,amount=.28)


# Nominal prototype dimensions, not measured or material-qualified.
FLEX_T=.80
FLEX_W=1.20
FLEX_L=14.0
HEAD_R=2.60
FLEX_BOTTOM=29.60
TRAVEL={'c3':.40,'c6':.36}
# Two opposed horizontal leaf latches. Their longitudinal fibers can be
# printed in the XY plane, avoiding a deliberately Z-oriented flexure arm.
LATCH_ROOT_X=22.0
LATCH_TIP_X=40.0
LATCH_DEFLECT=.80  # conservative insertion envelope, must be coupon-tested
FPC_BOX=(22.,62.,4.,24.,26.4,28.2) # conservative 40x20 footprint / 1.8 tall

def labels(module):
    common=[('WIFI',70.,36.8,1.6),('AUX',80.25,36.8,1.6),('BUS',90.5,36.8,1.6),
            ('GEA',28.,20.,5.2),('LOCAL APPLIANCE LINK',29.,14.4,1.45)]
    if module=='c3': return common+[('BOOT',79.,3.50,1.6),('RESET',79.,22.10,1.6),('C3',96.,25.5,1.4)]
    return common+[('RESET',89.,1.75,1.6),('BOOT',91.,24.3,1.6),('C6',96.,27.,1.4)]

def latch(side=1, deflection=0):
    # Deflection is a diagnostic rigid-envelope translation, not elastic CAD.
    y0,y1=43.20,44.20
    s=B(22.,40.,y0,y1,7.0,9.4)
    # Ramp above retention shoulder; a finger/tool can press it via a small
    # visible seam-level release aperture, avoiding a sealed non-serviceable latch.
    ramp=Plane.YZ.offset(37.)*Polygon((44.05,8.05),(45.40,8.05),(45.40,8.65),(44.15,9.40),align=None)
    s+=extrude(ramp,amount=3.)
    if side==-1: s=s.mirror(Plane.XZ.offset(-20.))
    if deflection: s=Pos(0,-side*deflection,0)*s
    return s

def base(magnets=False):
    s=rrsolid(114,54,6,-1.,SEAM)
    s-=rrsolid(101,42,3,2.4,SEAM+.2)
    s-=B(-.2,19.,7.7,26.,.65,2.45)
    for p in e.SOCKET_BBOX:
        s-=B(p['x_min']-.75,p['x_max']+.75,p['y_min']-.75,p['y_max']+.75,1.25,2.45)
    for x,y in e.MOUNT_HOLES:
        s+=C(3.,2.35,3.65,x,y)+C(1.25,2.35,5.55,x,y)
    tongue=loft([rr(109.6,49.6,4.3,SEAM-.1),rr(109.1,49.1,4.3,8.15)],ruled=True)
    tongue-=loft([rr(105.6,45.6,3.3,SEAM-.2),rr(105.1,45.1,3.3,8.3)],ruled=True)
    s+=tongue
    s-=B(-10,1,7.74,25.925,4.75,18.2)
    # Preserve a stable closed-height datum without any tightening operation.
    for x,y in SCREWS:
        s-=C(3.3,SEAM,8.3,x,y)
        s+=C(2.85,SEAM-.1,SEAM+.2,x,y)
    for side in [-1,1]:
        pocket=B(21.6,41.,42.2,47.2,2.4,10.2)
        anchor=B(20.8,23.0,42.6,44.9,2.3,9.4)
        if side==-1:
            pocket=pocket.mirror(Plane.XZ.offset(-20.))
            anchor=anchor.mirror(Plane.XZ.offset(-20.))
        s-=pocket
        s+=anchor+latch(side)
        stop=B(37.,40.,41.4,42.35,2.3,9.4)
        roots=C(.45,7.,9.4,23.,43.2)+C(.45,7.,9.4,23.,44.2)
        if side==-1:
            stop=stop.mirror(Plane.XZ.offset(-20.))
            roots=roots.mirror(Plane.XZ.offset(-20.))
        s+=stop+roots
    if magnets:
        for x,y in [(33.,34.),(60.,34.)]: s-=C(2.3,-1.1,1.3,x,y)
    return s

def flexure(module,name):
    x,y=SW[module][name]
    # A twin leaf directly over each switch. Foot is narrow only at its
    # distal end; no offset transfer lever or separate return spring.
    s=C(HEAD_R,FLEX_BOTTOM,FLEX_BOTTOM+FLEX_T,x,y)
    for dy in [-1.65,1.65]:
        beam=B(x-16.6,x-.8,y+dy-FLEX_W/2,y+dy+FLEX_W/2,FLEX_BOTTOM,FLEX_BOTTOM+FLEX_T)
        s+=beam
    s+=C(1.05,22.5,FLEX_BOTTOM+.05,x,y)
    s+=C(.52,SW_TOP[module]+REST_GAP,22.55,x,y)
    return s

def flexure_void(module,name):
    x,y=SW[module][name]
    # 0.60+ mm release slots. The roof bridges around the leaf root only.
    return B(x-15.6,x+.4,y-3.1,y+3.1,UNDER-.1,ROOF+.2)+C(3.20,UNDER-.1,ROOF+.2,x,y)

def button_stop(module,name):
    x,y=SW[module][name]
    top=FLEX_BOTTOM-TRAVEL[module]
    collar=C(3.45,22.5,top,x,y)-C(1.22,22.4,top+.1,x,y)
    # Attach outside the moving/slot envelope. The ring catches cap underside
    # after nominal travel, while the foot moves through its central bore.
    collar+=B(x+3.1,x+4.05,y-.65,y+.65,22.5,ROOF)
    return collar

def fpc_retention():
    # FPC slides under two shallow edge keeper rails; a printed spring finger
    # retains its entry edge. Flexure and RF effectiveness remain test gates.
    s=B(20.6,21.4,3.3,24.7,25.95,UNDER+.1)+B(62.6,63.4,3.3,24.7,25.95,UNDER+.1)
    s+=B(20.8,23.1,3.3,24.7,25.95,26.25)+B(60.9,63.2,3.3,24.7,25.95,26.25)
    s+=B(21.0,63.0,24.4,25.2,25.95,UNDER+.1)
    # Entry stop is outside final nominal FPC y4.0 edge: not a forced RF-pad overlap.
    s+=B(20.9,25.,3.0,3.7,26.3,UNDER+.1)
    s+=B(24.9,42.,3.0,3.6,26.3,27.3)
    s+=B(40.,42.,3.5,3.70,26.3,27.3)
    # Two snap-under cable keepers, above electronics, away from the C3 foot.
    for x,y in [(66.,12.9),(71.5,12.9)]:
        # Inverted-U bore is open sideways for installation; no tight cable tie.
        s+=B(x-1,x+1,y-2.,y-1.1,24.5,UNDER+.1)
        s+=B(x-1,x+1,y-1.3,y+1.8,24.5,25.3)
    return s

def shell(module='c3',antenna='internal'):
    outer=loft([rr(114,54,6,SEAM+.2),rr(107,47,6,28.7),rr(107,47,6,ROOF)],ruled=True)
    try:
        outer=outer.fillet(1.05,[a for a in outer.edges() if a.bounding_box().min.Z>ROOF-.01])
    except Exception: pass
    cavity=loft([rr(110,50,4.5,SEAM),rr(103,43,4.3,UNDER)],ruled=True)
    s=outer-cavity
    s-=B(-10,1,7.74,25.925,4.75,18.2)
    s-=xopening(14.8,9.0,2.2,12.9175,20.7)&B(98,110,-10,50,10,30)
    # Four small plastic datum lands stay outside PCB, set seam closure height.
    for x,y in SCREWS:
        s+=C(3.1,7.0,12.,x,y)+loft([Pos(x,y,11.9)*Circle(3.1),Pos(x,y,20.)*Circle(1.3),Pos(x,y,UNDER+.1)*Circle(1.3)],ruled=True)
    for x,y in e.MOUNT_HOLES:
        s+=C(2.4,5.65,UNDER+.1,x,y)-C(1.5,5.5,9.,x,y)
    for side in [-1,1]:
        relief=B(20.3,24.0,42.4,45.3,6.8,10.1)
        window=B(36.5,40.5,44.4,49.,7.90,9.65)
        if side==-1:
            relief=relief.mirror(Plane.XZ.offset(-20.))
            window=window.mirror(Plane.XZ.offset(-20.))
        s-=relief+window
    for name in SW[module]:
        s-=flexure_void(module,name)
        s+=button_stop(module,name)+flexure(module,name)
    for name,(bottom,top) in PIPES.items():
        tx,ty=top
        # Short STRAIGHT roof collar only. Lower angled cradles were removed
        # because they obstructed vertical assembly of the bent rigid pipes.
        s+=C(2.12,26.90,UNDER+.12,tx,ty)
        s-=C(1.60,26.8,ROOF+.2,tx,ty)
        # Nominal 0.12 mm diametral press-fit band, coupon-specific.
        s+=C(2.12,28.65,29.25,tx,ty)-C(1.37,28.55,29.35,tx,ty)
    for name,x,y,size in labels(module): s-=legend(name,x,y,size)
    if module=='c3' and antenna=='internal': s+=fpc_retention()
    if antenna=='external':
        s-=cy(6.,44.4,48.,56.,15.5)
        s+=cy(7.,42.9,44.4,56.,15.5)
        s-=cy(3.25,42.7,44.6,56.,15.5)&B(52.7,58.75,42.5,44.8,12.2,18.8)
        # Printed cable sleeve keeper replaces the former cable-tie anchor.
        anchor=B(51.5,60.5,36.0,38.2,12.7,UNDER+.1)
        anchor-=B(53.0,59.0,35.8,38.4,13.2,17.8)
        s+=anchor
    return s

def component_proxies(module):
    import component_envelopes as p
    q=p.proxies(module)
    if module=='c6':
        q['ufl']=C(1.2,18.50,19.40,78.8825,8.6215)
        q['ceramic']=B(77.6285,79.6285,13.4415,18.6415,18.50,19.60)
        q['usb']=B(92.5737,100.0143,8.3757,17.4673,18.50,e.MODULE_ENVELOPE_TOP_Z)
    for name,(x,y) in SW[module].items():
        q['BOOT0' if name=='BOOT' else 'RST0']=B(x-.8,x+.8,y-1.3,y+1.3,18.50,SW_TOP[module])
    return q

def export(s,name,one=True):
    assert s.is_valid,(name,'invalid')
    assert not one or len(s.solids())==1,(name,'not single solid',len(s.solids()))
    assert s.volume>0,(name,'empty')
    export_step(s,OUT/(name+'.step'))
    export_stl(s,OUT/(name+'.stl'),tolerance=.025,angular_tolerance=.15)
    return {'volume_mm3':round(s.volume,3),'solid_count':len(s.solids()),'bounds_mm':[[round(v,3) for v in tuple(s.bounding_box().min)],[round(v,3) for v in tuple(s.bounding_box().max)]]}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    parts={'base':base(),'base_magnets':base(True)}
    for mod in ['c3','c6']:
        for ant in ['internal','external']: parts[f'lid_{mod}_{ant}']=shell(mod,ant)
        for name,s in component_proxies(mod).items(): parts[mod+'_'+name]=s
    for name,(bottom,top) in PIPES.items(): parts['lightpipe_'+name.lower()]=pipe_shape(bottom,top,1.43)
    parts['fpc_40x20_proxy']=B(*FPC_BOX)
    # Cropped copies of real mechanisms for early slicer/fit trials. They
    # are not extra pieces of a finished assembly and do not touch a module.
    parts['coupon_button_c3']=shell('c3')&B(58.,85.,3.,13.,18.,31.)
    parts['coupon_button_c6']=shell('c6')&B(79.,104.,1.,11.,18.,31.)
    parts['coupon_snap_base']=base()&B(18.,44.,40.5,49.,-2.,14.)
    parts['coupon_snap_lid']=shell('c3')&B(18.,44.,40.5,49.,-2.,14.)
    summary={n:export(s,n) for n,s in parts.items()}
    for mod in ['c3','c6']:
        ink=Compound([legend(name,x,y,size) for name,x,y,size in labels(mod)])&B(-10,110,-10,50,ROOF-.26,ROOF-.01)
        summary[f'label_inlay_{mod}_optional']=export(ink,f'label_inlay_{mod}_optional',False)
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2))
    print('Exported',len(parts),'parts; buttons and snaps integral')

if __name__=='__main__': main()
