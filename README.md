# ESPHome GE Laundry UART

Local Home Assistant control and monitoring for compatible GE appliances through ESPHome and the appliance's GEA serial bus.

> [!WARNING]
> The appliance uses an 8P8C modular connector that looks like Ethernet, but it is **not Ethernet**. Do not connect it to network equipment.

![Assembled Rev 2-era adapter](pcb/rev2.0/images/assembled-board.jpg)

The project began as an effort to integrate a GE washer and dryer with Home Assistant. An ESP32 powered by the appliance communication port reports information such as remaining time and cycle completion through ESPHome. Early work involved researching the GEA2 and GEA3 protocols and the U+ Connect module; later, [GE Appliances](https://github.com/geappliances) and [FirstBuild](https://firstbuild.com/inventions/home-assistant-adapter/) published additional hardware and protocol information. The maintained ESPHome implementation now lives in [mguaylam/esphome-gea](https://github.com/mguaylam/esphome-gea), while this repository provides compatible hardware, reference configurations, manufacturing files, and enclosures.

## Getting started

### I already have a board

Follow the [firmware setup guide](firmware/README.md) to choose a GEA2 or GEA3
configuration, flash the board, and connect it to Home Assistant. Rev 3A normally
flashes through USB-C; Rev 2.x requires an external 3.3 V serial adapter. Printable
enclosures are available for [Rev 3A](case/rev3a/README.md) and
[Rev 2.x](case/rev2/README.md).

### I want to order a board

Start with [PCB Rev 3A](pcb/rev3a/README.md), then follow the
[step-by-step ordering guide](pcb/ORDERING.md). Rev 3A is the current development
design and supersedes Rev 2.2 for new prototype builds. It adds USB-C, automatic
pin-1/pin-3 appliance-power selection, more efficient power conversion, a
recovery header, and a matching enclosure.

> [!CAUTION]
> Rev 3A passes the documented KiCad and manufacturing-file checks, but assembled
> hardware has not completed electrical or appliance testing. Order only a minimum
> prototype batch until its bring-up procedure passes.

A JLCPCB quote checked on September 19, 2026 was **$149.96 before shipping and tax
for five fully assembled boards**, or about **$29.99 per board**. Prices and part
availability can change. Rev 2.2 remains available as an older, lower-cost design;
older boards and the complete change history are listed in the
[PCB revision index](pcb/README.md).

Hardware reviewers and contributors can inspect the
[Rev 3A validation package](pcb/rev3a/validation/README.md) and should also read
the [contribution guide](CONTRIBUTING.md).

## Related projects

- [GE Appliances organization](https://github.com/geappliances)
- [FirstBuild Home Assistant adapter](https://firstbuild.com/inventions/home-assistant-adapter/)
- [puddly/casserole](https://github.com/puddly/casserole)
- [GEMakers/green-bean](https://github.com/GEMakers/green-bean)
- [doitaljosh/gea-interface-board](https://github.com/doitaljosh/gea-interface-board)
- [doitaljosh/ge-appliances-re](https://github.com/doitaljosh/ge-appliances-re)
- [doitaljosh/geabus-documentation](https://github.com/doitaljosh/geabus-documentation)
- [simbaja/gehome](https://github.com/simbaja/gehome)
- [GE Appliances Home Assistant adapter](https://github.com/geappliances/home-assistant-adapter)
- [GE Appliances Home Assistant examples](https://github.com/geappliances/home-assistant-examples)
- [GE Appliances Home Assistant bridge](https://github.com/geappliances/home-assistant-bridge)
