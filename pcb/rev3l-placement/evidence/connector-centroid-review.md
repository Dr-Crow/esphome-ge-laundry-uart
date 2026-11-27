# Rev 3L connector placement centers

The assembly placement list now locates both XIAO sockets and the four-pin debug header at their body centers. Their native footprint anchors are pin 1. Coordinates below are millimeters in the exported top-side CPL frame (X-right, Y-up).

| Connector | Earlier CPL X, Y | Corrected CPL X, Y |
| --- | --- | --- |
| J5 | 61.226650, -3.597500 | 53.606650, -3.597500 |
| J6 | 45.986650, -18.837500 | 53.606650, -18.837500 |
| J7 | 37.571895, -10.409707 | 37.571895, -6.599707 |

The generator applies the reviewed footprint-local offsets at the current rotation, then checks the resulting coordinates of all 72 fitted parts against the [body bounds](component-body-edge.csv). The earlier file failed at J5, J6 and J7. The updated file passes with a maximum error of 0.000051 mm or less. Run `python3 pcb/rev3l-placement/manufacturing/generate.py --check-cpl` from the repository root. Native KiCad CLI 9.0.9 reproduced the checked-in CPL and BOM byte for byte on the identical design; all 14 CAM members matched after normalizing timestamps. Confirm JLCPCB's imported footprint centers, rotation, pin 1 and through-hole handling. Factory acceptance and prototype verification remain open.

[Assembly data](../manufacturing/CPL-GEA-Adapter-Rev3L.csv) · [Combined native regeneration evidence](https://github.com/Dr-Crow/esphome-ge-laundry-uart/blob/194dd8f6fec56276e689fa31ccc0178dd1c0d370/pcb/rev3m/evidence/connector-centroid-review.md) · [JLCPCB placement format](https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly)
