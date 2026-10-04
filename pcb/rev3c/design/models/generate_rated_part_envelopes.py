"""Drawing-based maximum envelopes for optional rated input parts; not vendor CAD."""
from pathlib import Path
from build123d import Align, Box, Location, Compound, export_step
HERE = Path(__file__).resolve().parent

def box(x0,x1,y0,y1,z0,z1):
    return Box(x1-x0,y1-y0,z1-z0,align=(Align.MIN,Align.MIN,Align.MIN)).locate(Location((x0,y0,z0)))
# TI TPS1H200A-Q1 Rev E p27 DGN0008K-C01: max body3.1 x3.1, lead span5.05,
# lead width0.38, lead pitch0.65, height1.1. Rectangular leads omit bend detail.
parts=[box(-1.55,1.55,-1.55,1.55,.05,1.1)]
for x0,x1 in [(-2.525,-1.45),(1.45,2.525)]:
    for y in [-.975,-.325,.325,.975]:parts.append(box(x0,x1,y-.19,y+.19,0,.23))
export_step(Compound(children=parts),HERE/'TPS1H200A-DGN0008K-max-envelope.step')
# Littelfuse1812L sheet p6 maximum dimensions4.73 x3.41 x1.55; simplified body.
export_step(box(-2.365,2.365,-1.705,1.705,0,1.55),HERE/'1812L075-33DR-max-envelope.step')
print('Wrote two explicitly approximate manufacturer-dimension envelopes')
