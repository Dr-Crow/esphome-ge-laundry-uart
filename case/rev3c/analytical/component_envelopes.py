"""Current selected-carrier analytical proxies, never printable electronics.

Selected rated parts use retained drawing maximum dimensions. Missing carrier
models use source courtyard XY and explicitly assumed screening Z, not a proven
supplier maximum. Module proxies remain conditional/partial; no mating proof.
"""
from pathlib import Path
import json
import interface_baseline as e
BOX=e._box
CYL=e._cylinder

def proxies(module,stack_mm=11.0,switch_height=None):
    if module not in ('c3','c6'): raise ValueError(module)
    if not e.REVIEW_STACK_MIN <= stack_mm <= e.REVIEW_STACK_MAX: raise ValueError(stack_mm)
    bottom=e.PCB_TOP_Z+stack_mm; top=bottom+1.6
    p={}
    pcb=BOX(0,99,0,40,e.PCB_SEAT_Z,e.PCB_TOP_Z)
    for x,y in e.MOUNT_HOLES: pcb-=CYL(1.6,e.PCB_SEAT_Z-.1,e.PCB_TOP_Z+.1,x,y)
    p['carrier']=pcb
    # Current EVERCOM5301 RevA drawing registration. Internal mating detail and
    # locating-post profiles are undimensioned/omitted, so plug fit stays open.
    p['J1_body']=BOX(-.38,17.67,9.395,24.595,e.PCB_TOP_Z,e.PCB_TOP_Z+11.45)
    for n in range(8):
        p['J1_tail_'+str(n+1)]=CYL(.23,e.PCB_TOP_Z-3.0,e.PCB_TOP_Z,13.97+(2.54 if n%2 else 0),12.55+1.27*n)
    for i,b in enumerate(e.SOCKET_MAX_BBOX):
        p['J'+str(i+5)+'_body']=BOX(b['x_min'],b['x_max'],b['y_min'],b['y_max'],e.PCB_TOP_Z,e.SOCKET_TOP_Z_MAX)
        # Conservative full-row maximum-tail prism, not detailed pin/solder CAD.
        p['J'+str(i+5)+'_tails']=BOX(b['x_min'],b['x_max'],b['y_min'],b['y_max'],e.PCB_TOP_Z-3.45,e.PCB_SEAT_Z)
        # Reserved independent clearance screen, not a fitted header solid or
        # proof of engagement. Maximum socket height and minimum total stack
        # are deliberately combined as pessimistic, independent bounds.
        p['male_spacer_'+str(i)]=BOX(b['x_min'],b['x_max'],b['y_min'],b['y_max'],e.SOCKET_TOP_Z_MAX,bottom)
    for ref,(x,y) in {'U9':(65.,8.),'U10':(65.,22.5)}.items():
        p[ref]=BOX(x-2.525,x+2.525,y-1.55,y+1.55,e.PCB_TOP_Z,e.PCB_TOP_Z+1.1)
    for ref,(x,y) in {'F1':(45.5,21.5),'F2':(45.5,7.)}.items():
        p[ref]=BOX(x-2.365,x+2.365,y-1.705,y+1.705,e.PCB_TOP_Z,e.PCB_TOP_Z+1.55)
    for rec in json.loads((Path(__file__).parent/'current_carrier_bounds.json').read_text())['records']:
        p[rec['reference']]=BOX(*rec['bounds_mm'])
    p['module']=BOX(77.476,98.431,4.0275,21.8075,bottom-.04,bottom+1.6)
    # Broad central proxy from retained partial assembly maximum Z. It is an
    # intentionally overfilled screen, not an authentic RF shield.
    p['central_electronics_screen']=BOX(81.,93.,7.,19.,top,bottom+5.5)
    usb=(91.939,100.003,8.041,17.794) if module=='c3' else (92.5737,100.0143,8.3757,17.4673)
    p['usb_shell_screen']=BOX(*usb,top,bottom+5.5)
    sw={'BOOT':(79.,8.4725),'RESET':(79.,17.3625)} if module=='c3' else {'BOOT':(97.3483,19.4927),'RESET':(97.3483,6.3355)}
    for name,(x,y) in sw.items():
        h=(switch_height[name] if isinstance(switch_height,dict) else
           switch_height if switch_height is not None else (1.5 if module=='c3' else .53))
        wx,wy=(2.5,3.0) if module=='c3' else (1.6,2.6)
        p[name+'_switch']=BOX(x-wx/2,x+wx/2,y-wy/2,y+wy/2,top,top+h)
    x,y=(78.873,12.9175) if module=='c3' else (78.8825,8.6215)
    p['ufl_max']=BOX(x-1.55,x+1.55,y-1.5,y+1.5,top,top+1.45)
    # Maximum ceramic XY;1.2mm Z is a screen, not a verified production maximum.
    if module=='c6': p['ceramic_screen']=BOX(77.5285,79.7285,13.3415,18.7415,top,top+1.2)
    return p
