
![Legacy Revision 2 hardware](https://github.com/user-attachments/assets/f0ecc78b-20a1-45ff-a41a-00d02f6c67e2)

# esphome-ge-laundry-uart

This project connects compatible GE washers and dryers to Home Assistant through ESPHome. The appliance service port uses an 8P8C connector that looks like RJ45, but it carries appliance power and low-voltage serial signals rather than Ethernet. An ESP32 powered by that port can report information such as remaining cycle time and cycle completion.

The original custom component has moved to the actively maintained [ESPHome GEA external component](https://github.com/mguaylam/esphome-gea). GE Appliances and FirstBuild also publish useful [hardware](https://github.com/geappliances/home-assistant-adapter), [examples](https://github.com/geappliances/home-assistant-examples), and [protocol implementations](https://github.com/geappliances/home-assistant-bridge). Legacy project code remains available in a branch.

## Current status

- The [PCB revision guide](pcb/readme.md) explains the differences, known problems, and order status for each hardware version.
- Revisions 2.0 and 2.1 use the same ESP32-C3 module and pinout as the FirstBuild adapter, but their RX/TX labels are swapped and an optional reset-monitor chip can cause boot loops.
- [Revision 2.2](pcb/rev2.2/README.md) is a manufacturing candidate that leaves the troublesome reset-monitor chip uninstalled, corrects the RX/TX labels, and provides a matched Gerber, bill of materials, and placement file. It still requires fabrication-preview review and prototype testing before production use.
- [Revision 3A](pcb/rev3/README.md) is a quote-ready, unqualified prototype design: an 88.7 mm by 40.0 mm, four-layer board with native USB-C and automatic pin-1/pin-3 appliance-power selection. Its schematic, 43-group/91-part fitted BOM, manufacturing package, review plots, [new-user board guide](pcb/rev3/BOARD_GUIDE.md), and [printable enclosure](case/rev3a/README.md) are available for review. Vendor-preview review, electrical qualification, and appliance testing must pass before an order is released.
- Baseline YAML files for version 2.x boards remain here for reference; new installations should use the maintained ESPHome GEA external component linked above.

## TODO

- Validate the revision 2.2 manufacturing candidate on a small prototype batch.
- Qualify Revision 3A prototypes for onboard USB programming and the automatic dual-input DC/DC power path.
- See if the GEA2 subscribe/publish logic can be worked out for quicker response.

## Related projects

- https://github.com/puddly/casserole
- https://github.com/GEMakers/green-bean
- https://github.com/doitaljosh/gea-interface-board
- https://github.com/doitaljosh/ge-appliances-re
- https://github.com/doitaljosh/geabus-documentation
- https://github.com/simbaja/gehome
- https://github.com/geappliances/home-assistant-adapter
- https://github.com/geappliances/home-assistant-examples
- https://github.com/geappliances/home-assistant-bridge
- https://github.com/mguaylam/esphome-gea
