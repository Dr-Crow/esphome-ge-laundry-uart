"""Simplified electronics/RF envelopes only, never printable parts. Units:mm."""
import interface_baseline as e
BOX=e._box
CYL=e._cylinder

def proxies(module):
    p={}
    pcb=BOX(0,99,0,40,e.PCB_SEAT_Z,e.PCB_TOP_Z)
    for x,y in e.MOUNT_HOLES: pcb-=CYL(1.6,e.PCB_SEAT_Z-.1,e.PCB_TOP_Z+.1,x,y)
    p['carrier']=pcb
    p['rj45']=BOX(-.525,18.265,8.49,25.175,e.PCB_TOP_Z,e.PCB_TOP_Z+11.45)
    for i,b in enumerate(e.SOCKET_BBOX): p['socket'+str(i)]=BOX(b['x_min'],b['x_max'],b['y_min'],b['y_max'],e.PCB_TOP_Z,e.SOCKET_TOP_Z_MAX)
    p['module']=BOX(77.463,98.444,4.015,21.82,e.MODULE_PCB_BOTTOM_Z_MAX,e.MODULE_PCB_BOTTOM_Z_MAX+1.6)
    p['shield']=BOX(81.0,93,7,19,e.MODULE_PCB_BOTTOM_Z_MAX+1.6,e.MODULE_PCB_BOTTOM_Z_MAX+4.3)
    p['usb']=BOX(91.939,100.003,8.041,17.794,e.MODULE_PCB_BOTTOM_Z_MAX+1.6,e.MODULE_ENVELOPE_TOP_Z)
    positions=e.BUTTON_POSITIONS if module=='c3' else {'BOOT0':(97.3483,19.4927),'RST0':(97.3483,6.3355)}
    for name,(x,y) in positions.items(): p[name]=BOX(x-1,x+1,y-.85,y+.85,e.MODULE_PCB_BOTTOM_Z_MAX+1.6,e.MODULE_PCB_BOTTOM_Z_MAX+3.1)
    ax,ay=(78.873,12.9175) if module=='c3' else (79.18,8.4725)
    p['ufl']=CYL(1.2,e.MODULE_PCB_BOTTOM_Z_MAX+1.6,e.MODULE_PCB_BOTTOM_Z_MAX+2.5,ax,ay)
    if module=='c6': p['ceramic']=BOX(77.8,80.2,15.5,19.2,e.MODULE_PCB_BOTTOM_Z_MAX+1.6,e.MODULE_PCB_BOTTOM_Z_MAX+3.2)
    for ref,(x,y) in e.LED_POSITIONS.items(): p[ref]=BOX(x-.8,x+.8,y-.4,y+.4,e.PCB_TOP_Z,e.PCB_TOP_Z+.8)
    return p
