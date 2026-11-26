# Rev3A focused upstream candidate

This package is based on public main bc0d52495bd97ed1504bd0ca0775e47feb01a648 and imports exact reviewed rated-backport d2bde08da836b493f76de03d330aa0489e2c3419. It retains integrated C3, both appliance inputs, automatic PIN1 priority, buck, USB architecture, mounts and 88.7 ×40 mm outline.

Independent native source, 301 pin memberships,97-reference BOM/CPL and 14-member CAM reproduction checks pass. [Schematic-only cleanup](validation/erc-normalization/README.md) now reproduces zero ERC errors/warnings under unchanged rules, preserving all 301 current pin memberships; strict CI needs no waiver. Its separate source-bound proof and native PDF record this cleanup; the prior rated-protection manifest/reports and package schematic PDF need refresh when integrating it. DRC has zero errors/warnings, unconnected and parity findings. Direct native Gerber ZIP viewing hit OS resource error11 after a bounded retry; actual source schematic/copper/drill/3D pixels were inspected.

The J4 exact local SHOU HAN footprint now matches recommended forward shell slots/lands. The 1.6 mm board permits top-mount seating, but short shell legs are recessed; no shell paste apertures are defined. Assembler-approved solder delivery, inspection and retention remain a process gate. UART VCC stays disconnected; never inject the 3V3 regulator-output rail.

The board package includes no enclosure CAD or other-revision changes. A pinned historical case guide is provided only as a separate reference; updated component heights and actual fit need review. Shared CI/firmware and repository-wide comparison are separate candidates.

Native passes are not physical or manufacturing approval. Actual source/current/transient, loaded startup, retry, inrush, whole-chain ratings/energy/thermal, USB-isolation, assembly, case/RF and appliance tests remain open.
