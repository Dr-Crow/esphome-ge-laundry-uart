# ESPHome GE Laundry UART

Local Home Assistant control and monitoring for compatible GE appliances through ESPHome and the appliance's GEA serial bus.

> [!WARNING]
> The appliance uses an 8P8C modular connector that looks like Ethernet, but it is **not Ethernet**. Do not connect it to network equipment.

![Assembled Rev 2-era adapter](pcb/rev2.0/images/assembled-board.jpg)

The project began as an effort to integrate a GE washer and dryer with Home Assistant. An ESP32 powered by the appliance communication port reports information such as remaining time and cycle completion through ESPHome. Early work involved researching the GEA2 and GEA3 protocols and the U+ Connect module; later, [GE Appliances](https://github.com/geappliances) and [FirstBuild](https://firstbuild.com/inventions/home-assistant-adapter/) published additional hardware and protocol information. The maintained ESPHome implementation now lives in [mguaylam/esphome-gea](https://github.com/mguaylam/esphome-gea), while this repository provides compatible hardware, reference configurations, manufacturing files, and enclosures.

## Getting started

### I already have a board

Follow the [firmware setup guide](firmware/README.md) to choose a GEA2 or GEA3 configuration, flash the board, connect it to Home Assistant, and check the status LEDs. The [Rev 2 enclosure](case/rev2/README.md) includes ready-to-print files.

### I want to review a new board

The selected development focus is the socketed C3/C6 Rev3C with both appliance inputs, automatic priority and rated protection. This integration includes all seven editable board revisions, eight firmware profiles, native validation and the [illustrated Rev3C ordering guide](pcb/rev3c/ORDERING.md). Start with the [current comparison and validation](docs/revision-comparison/README.md), [exact source handoff](docs/revision-comparison/HANDOFF.md) and [finish registry](docs/revision-comparison/FINISH-PLAN.md).

Fresh pinned KiCad 9.0.9 ERC/DRC and intended-rule checks pass for all seven revisions. The [Rev3C stencil correction](pcb/rev3c/STENCIL-REVIEW.md) removes unintended drill-marker openings. Native/CAM agreement is separate from supplier process, appliance power and physical qualification. The corrected Rev3C trio has refreshed October 5 quotes of $134.64 for five or $168.92 for ten assembled carriers, before shipping, tax and XIAO modules; Rev2.2's old $78.07 quote is historical.

Older boards and the complete change history are listed in the [PCB revision index](pcb/README.md). Hardware contributors should also read the [contribution guide](CONTRIBUTING.md).

For the proposed USB-C revisions, see the [board and enclosure comparison](docs/revision-comparison/README.md), including assembled-board estimates and views from several angles. The [project handoff](docs/revision-comparison/HANDOFF.md) records the development branches and remaining work.

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
