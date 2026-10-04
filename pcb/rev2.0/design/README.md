# Recovered Rev 2.0 native source

The source restored from `af1f2c40029ef67c56910fb2c55feac835553525` is retained
with a bounded native KiCad 9.0.9 cleanup. `RESTORED-PROVENANCE.json` identifies
its original Git blobs. The original schematic symbols and board footprints
are recovered into project-local libraries, with former identifiers recorded
in `symbols/source-map.json` and `footprints/source-map.json`. No newer component
or footprint substitute was selected. The historical AP2205-3.3 value with an
AP2204R-3.3 symbol identity remains visible and unresolved.

The UUID-backed board references are JP2 and TP3. H3/H4 remain pinless DNP
mechanical placeholders excluded from the board; their historical footprint
fields remain, and no holes were invented. All 75 source component identities,
73 board footprints, 222 physical pad definitions, 186 electrical pin memberships
in 45 net partitions, 712 tracks/vias, placements, outline, drills and interfaces
are preserved. U4 pad 2 alone changes its thermal spoke angle from 90 to 45 degrees.
Its gap, width, original minimum-two-spoke rule and routed 0.4064 mm GND connection
remain. Two U2 silkscreen overhangs are removed and two J1 silk segments are
clipped at x=131.5 mm. UART text and its historical direction meaning are retained.

The connection grid is 25 mil: every one of the 725 original connection-bearing
object coordinates lies on that grid. No wires, pins, labels or symbols were
snapped or moved. All original project rules, severities, exclusions and net
classes are unchanged. Three excluded-from-BOM/board power flags model the
intended external VDC supply, GND return and passive selected/protected `/p1`
output feeding U3.IN. They establish ERC intent only, not voltage/current ratings,
source availability, protection performance or appliance compatibility.

KiCad-derived definitions retain their upstream license and schematic/PCB
exception in `KICAD-LIBRARY-LICENSE.md`; inherited project-specific definitions
retain the repository license. See [the native review](../native-review/REVIEW.md)
for exact counts, original-versus-current artifact distinctions, supplier placement
limitations and regeneration effects. A clean native check does not qualify this
historical board for a new order.
