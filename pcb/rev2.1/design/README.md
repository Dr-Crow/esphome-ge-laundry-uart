# Recovered Rev 2.x source libraries

These project-local libraries preserve the definitions embedded in the source at
`bc0d52495bd97ed1504bd0ca0775e47feb01a648`. They are not replacements selected
from a newer package library. The footprint files use a reference prefix because
board-specific pad settings and geometry must not accidentally be merged.
`footprints/source-map.json` records each former library identifier.

All 74 component identities, 223 pad definitions and the exact 45 physical net
memberships are retained in each board. C10 alone moves upward 0.30 mm. Seven
local track endpoints change and two local 0.4064-mm tracks are added, clearing
the C9/C10 courtyard overlap; all other placements and routes are retained. U4 pad 2 alone uses a solid
GND-zone contact, retaining its existing 0.4064 mm routed GND connection and via.
Overhanging silkscreen primitives are removed or clipped; copper and holes are
unchanged. The project connection grid is 25 mil, matching the existing source
connections. Rule severities, exclusions and global clearances are unchanged.

The recovered U4 symbol's hidden supply pin is named +5V to agree with its actual
source net. Power flags identify the intended external input, ground and the
passive-switch output feeding U3; they do not establish ratings or authorize
powering the board. UART net names GEA3_RX/GEA3_TX remain historical appliance
perspective names. J2/J3 and J1 silkscreen uses the adapter/ESP perspective.

KiCad library-derived definitions retain their upstream license and schematic /
PCB distribution exception in `KICAD-LIBRARY-LICENSE.md`. Project-specific
inherited definitions retain the repository license. Read the revision validation
report before using any manufacturing file. A clean ERC is not a power or
appliance qualification, and the clean native courtyard check does not prove physical component fit.
