# Rev2.1 placement-origin review

The three inherited CPL shifts are not arbitrary: J1, U3 and U6 exactly use the center of each native pad bounding box. The native KiCad position exporter emits footprint anchors. Comparing these two conventions without identifying the selected origin created a false-positive CI mismatch. No PCB, BOM, CPL, Gerber or drill byte is changed by this review. A subsequent source-metadata check found Q1’s schematic LCSC field empty even though its PCB and BOM already selected C10493; the schematic field now matches them. All pin nets and purchasing selections are preserved. Native ERC/DRC/parity/unconnected remain zero.

| Reference | Native anchor X/Y, mm | Existing CPL = pad-center X/Y, mm | Delta X/Y, mm |
| --- | --- | --- | --- |
| J1 | 122.425 / −99.2825 | 124.755 / −94.8375 | +2.330 / +4.445 |
| U3 | 95.675 / −103.960 | 93.800 / −103.960 | −1.875 / 0 |
| U6 | 76.525 / −107.000 | 76.825 / −107.000 | +0.300 / 0 |

These centers were calculated independently from all native pad bounding boxes with genuine KiCad 9.0.9, using negative PCB Y for the exported coordinate frame. The exact source hashes, native anchors, pad bounds, rotations and footprint IDs are in [placement-origin-review.json](placement-origin-review.json). All other assembled references use the existing native-anchor convention. [Fabrication Toolkit documents](https://github.com/bennymeg/Fabrication-Toolkit#-override-component-origin) distinct Anchor and Center options; its Center option uses the pad bounding box. This establishes that the convention is supported, without claiming that the historical file's generation tool is known. [JLCPCB defines](https://jlcpcb.com/help/article/pick-place-file-for-pcb-assembly) metric centroid coordinates, side and rotation.

CI can accept these three declared origins only with committed, hash-matched review evidence tied to the exact native source. Any source, proof, reference, footprint, native anchor or rotation change invalidates that policy. Arbitrary offsets remain rejected. This is an export-consistency correction; it does not waive source, electrical or physical findings.

Before assembly approval, compare the supplier's actual package model/DFM placements, pin 1, pads and through-hole drill pattern against the source. Confirm the exact EVERCOM connector fits the inherited footprint and the regulator models align. The native pad center is not proof of a particular pick-and-place machine's package-origin convention. U1 boot loops and legacy power-rating/thermal gates remain unresolved; Rev2.1 stays retired and unapproved for ordering or appliance use.
