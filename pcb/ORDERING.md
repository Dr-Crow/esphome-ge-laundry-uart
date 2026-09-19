# Order a Rev 3A board

You do not need KiCad to order the board. This guide uses JLCPCB, but another PCB assembly company can use the same files.

[Back to the project overview](../README.md) · [PCB revision index](README.md)

> [!NOTE]
> Rev 3A has not yet been tested as an assembled board. Order the minimum quantity
> first. If you want to wait for tested hardware, check the
> [Rev 3A status](rev3a/README.md) before ordering.

## Download these three files

- [Gerber ZIP](rev3a/manufacturing/GERBER-GEA-Adapter-Rev3A.zip): the board itself
- [BOM](rev3a/manufacturing/BOM-GEA-Adapter-Rev3A.csv): the parts list
- [CPL](rev3a/manufacturing/CPL-GEA-Adapter-Rev3A.csv): where the parts go

Keep these three Rev 3A files together. Do not use a BOM or CPL from another revision.

## Place the order

1. Open the JLCPCB PCB quote page and upload the Gerber ZIP.
2. The site should detect a 4-layer board about 88.7 mm by 40.0 mm. Use the standard 1.6 mm board thickness.
3. Choose five PCBs and enable PCB assembly for all five boards.
4. Select economic, top-side assembly.
5. Upload the Rev 3A BOM and CPL when prompted.
6. Review the board and component-placement previews. Resolve any missing, unselected, or obviously misplaced parts before continuing.

## Current price estimate

A JLCPCB quote checked on September 19, 2026 was **$149.96 before shipping and
tax for five fully assembled boards**, or about **$29.99 per board**. Treat this
as a dated estimate because component stock, assembly classifications, and pricing
change.

## Before paying

Before continuing, check that:

- The board is about 88.7 mm by 40.0 mm and has four layers.
- Assembly is enabled for all five boards on the top side.
- The component-placement preview looks aligned with the board.
- The parts list has no unresolved or unselected items.

The [Rev 3A manufacturing page](rev3a/manufacturing/README.md) describes the
expected package and current quote if you need to compare them with the order
screen.

## When the boards arrive

1. Check for bent connectors, loose parts, or visible solder bridges.
2. Complete the [Rev 3A bring-up procedure](rev3a/README.md#prototype-bring-up)
   using current-limited bench power.
3. Follow the [firmware setup guide](../firmware/README.md) to flash the board
   through USB-C.
4. Do not connect it to an appliance until every appliance-connection gate in the
   bring-up procedure passes.

If you do not have the tools to perform the power and backfeed checks, wait until
the first Rev 3A batch has been tested and the results are posted.
