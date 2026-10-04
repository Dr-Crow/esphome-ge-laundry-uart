# Rev1 historical source definitions

This source comes from exact public commit `87984047ee029efb83bf9947dc21818fd18e39b3`, whose input hashes are retained in [restoration provenance](RESTORED-PROVENANCE.json). Current review and hash binding are in [native review](../validation/NATIVE-REVIEW.md).

`symbols/LegacySymbols.kicad_sym` recovers the 21 exact embedded source symbols, including the original custom onionStraws definitions. Only library namespaces change. The additional modelling PWR_FLAG is the exact pinned KiCad 9.0.9 `power:PWR_FLAG` definition with a local namespace. `symbols/source-map.json` retains every source identifier.

`footprints/LegacyBoard.pretty` recovers each source board footprint, paired by reference and original identity in `footprints/source-map.json`. Pads, holes, models, parts and placement geometry are retained; only the documented RJ45 overhanging silk graphics change. The local library exists to preserve historical native geometry, rather than refresh it from today's stock footprints.

The [upstream KiCad library notice](KICAD-LIBRARY-LICENSE.md) is retained for the KiCad library data. Original project custom definitions retain their original provenance. The recovery establishes agreement with the embedded historical design, not a purchased module identity or component rating qualification.
