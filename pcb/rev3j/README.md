# Rev 3J GE appliance adapter

## Further compaction
Open `pcb/rev3j/design/GEA-Adapter-Rev3J.kicad_pro` for the separate experimental layout. The study redistributes components and routes along the short axis. It retains both protected inputs, the XIAO C3/C6 socket geometry, antenna keepout, the original local buck switch and bootstrap copper, all 72 top-side assembly references, and the numbered J7 monitor header. The alternate-power bus has explicit copper junctions for its taps. The mounting holes move by 0.67 and 0.73 mm along the short axis. The XIAO socket pair shifts 0.55 mm. Use the matching Rev 3J case in case/. It realigns the PCB posts and jack opening, maintains the LED and module datums, and documents the tail clearances. The size gain is 5.15% versus 3I and 13.65% versus 3H. It still has about 2.08 times FirstBuild's PCB area.

Native KiCad 9.0.9 ERC, full DRC and schematic parity pass on both revisions. Rev 3I also passes the repository inventory, hardware, manufacturing and rules checks. The study BOM is identical to 3I, all 72 CPL positions agree with the measured moves, and CAM is available for review. Production review, a printed 3J case fit check, C3/C6 fit, actual harness startup, load steps, source switching, clamp voltage, temperature and USB backfeed remain open. Neither board is released for ordering. No powered test was run.

