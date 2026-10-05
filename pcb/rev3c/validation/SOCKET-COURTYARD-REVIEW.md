# Independent socket courtyard delta proof

Baseline: `acbcb6c5a138fedeb8e93d92838b12381bbce4b4`. Current PCB SHA-256: `6c76a83a6cb1af65f7e8a70d77ad9ddd5911f9ab3843b6ca2c365eea0115904b`.

PASS: exactly two design files differ. Their entire source is byte-for-byte identical after replacing only the six allowed start/end coordinate nodes in the J5/J6 embedded and library F.CrtYd rectangles.

PASS: 100 footprint placements, 239 pads, all drill/net fields, routes, vias, zones and filled copper are unchanged.

PASS: new rectangle is 18.98 × 3.15 mm, centred at (-7.62, 0), covering the supplied 18.48 × 2.65 mm maximum symmetric body plus 0.25 mm on every edge.

PASS: no J5/J6 overlap with another authored front courtyard; no outline interference. Outline is unchanged at (0,0)–(99,40) mm.

- J5: bbox [78.4, 3.7225, 97.38, 6.8725] mm; outline gap 1.620 mm, or 1.595 mm including half stroke. Closest authored courtyard is D14: 3.050 mm centreline / 3.000 mm including both half strokes.
- J6: bbox [78.4, 18.9625, 97.38, 22.1125] mm; outline gap 1.620 mm, or 1.595 mm including half stroke. Closest authored courtyard is C13: 0.907 mm centreline / 0.857 mm including both half strokes.

Native supplement: KiCad 9.0.2, all-track-errors + schematic-parity + severity-all + exit-code-violations. Baseline/current both exit 5 with exactly identical 93 library-configuration warnings. Both show zero unconnected items, zero schematic parity issues, and zero courtyard/other geometry violations. This does not replace hosted pinned KiCad 9.0.9.

Scope limits: supplied manufacturer dimensions are not independently reauthenticated here. Missing courtyards, physical body/mating/contact registration, seating, solder and physical qualification are not approved by this evidence. See JSON for exact hashes, group counts, missing-courtyard references and nearest courtyards.

The independent reviewer used source-node substitution, physical PCB tuple comparison and isolated native snapshots. The compact [JSON proof](socket-courtyard-independent-proof.json) preserves hashes, counts and nearest-courtyard evidence. Hosted pinned KiCad 9.0.9 must check the resulting commit.
