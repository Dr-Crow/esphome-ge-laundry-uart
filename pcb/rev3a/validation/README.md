# Revision 3A validation package

The KiCad source in [`../design/`](../design/) is authoritative. These files are
review artifacts generated from that source and must be refreshed after a design
change.

## Review artifacts

| Artifact | Purpose |
| --- | --- |
| [`schematic.pdf`](schematic.pdf) | Light-background, grid-free schematic |
| [`top.svg`](top.svg) / [`bottom.svg`](bottom.svg) | Outer copper and silkscreen views; bottom is mirrored |
| [`inner1.svg`](inner1.svg) / [`inner2.svg`](inner2.svg) | Individual internal-layer views |
| [`assembly-top.pdf`](assembly-top.pdf) / [`assembly-bottom.pdf`](assembly-bottom.pdf) | Fabrication outlines and reference designators |
| [`board-outline.pdf`](board-outline.pdf) | Board outline and hole locations |
| [`renders/3d-top.png`](renders/3d-top.png) | Straight-down populated-board view |
| [`renders/3d-isometric.png`](renders/3d-isometric.png) | Connector and component-height view |
| [`renders/3d-bottom.png`](renders/3d-bottom.png) / [`renders/3d-side.png`](renders/3d-side.png) | Underside and side clearances |
| [`reports/erc.json`](reports/erc.json) / [`reports/drc.json`](reports/drc.json) | KiCad 9.0.9 machine-readable checks |
| [`pth-drill-map.pdf`](pth-drill-map.pdf) / [`npth-drill-map.pdf`](npth-drill-map.pdf) | Plated and non-plated hole review |

![Revision 3A populated-board render](renders/3d-top.png)

## Automated-check results

KiCad 9.0.9 reports:

- ERC: zero errors and 55 warnings;
- DRC: zero errors, seven warnings, zero unconnected items, and zero
  schematic-parity findings.

The ERC warnings are 44 embedded-symbol/library differences, two legacy U5
library lookup warnings, eight USB-section grid warnings, and one intentional
`+5V`/hidden-`VCC` alias. The DRC warnings are five retained local-footprint
differences and two antenna-silkscreen edge warnings. Review the current JSON files
rather than relying only on these counts.

The short D18 connection on `In2.Cu` is intentional and passes DRC. `In1.Cu`
remains the continuous USB ground reference; do not describe both inner layers as
uninterrupted planes.

## Review order

1. Review connector pinout, source priority, reverse-current isolation, D18,
   USB-C, J2, and DNP items in the schematic.
2. Check layout, connector orientation, antenna keepout, switching loops, USB return
   path, silkscreen, drills, and enclosure clearances.
3. Confirm every BOM part, package, polarity, rating, and placement rotation.
4. Run ERC and DRC from the current source.
5. Review vendor board, drill, part-selection, and placement previews separately.

Use [REVIEW_CHECKLIST.md](REVIEW_CHECKLIST.md) to track readiness. The
[review brief](REVIEW_REQUEST.md) is formatted for an external schematic/PCB/BOM
review and keeps untested claims explicit.
