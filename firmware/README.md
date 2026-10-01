# Set up and use a Rev 2.x, Rev 3B, or Rev 3C board

These examples use the maintained [ESPHome GEA component](https://github.com/mguaylam/esphome-gea) to connect the adapter to Home Assistant.

[Back to the project overview](../README.md) · [Recommended PCB Rev 2.2](../pcb/rev2.2/README.md) · [Revision history](../pcb/README.md)

## Choose a configuration

| Configuration | Connection | Typical use |
| --- | --- | --- |
| [`gea2.yaml`](gea2.yaml) | GPIO5 TX and GPIO10 RX, inverted, 19,200 baud | Rev 2.x reference for GEA2 appliances. |
| [`gea3.yaml`](gea3.yaml) | GPIO21 TX and GPIO20 RX, non-inverted, 230,400 baud | Rev 2.x reference for GEA3 appliances. |

The appliance model determines whether it uses GEA2 or GEA3. Start with a configuration already known to work with your appliance rather than trying both while connected.

## Prepare ESPHome

If ESPHome is not installed yet, start with the official [ESPHome installation guide](https://esphome.io/install/) and [getting-started guide](https://esphome.io/install/getting-started/).

1. Copy the matching YAML file into your ESPHome configuration directory.
2. Change the `name` and `upper_name` substitutions near the top of the file.
3. Add these values to the `secrets.yaml` file in the same directory:

```yaml
wifi_ssid: "..."
wifi_password: "..."
esp_home_ota_pw: "..."
```

You can use the ESPHome Device Builder or the command line. The examples are starting points, so appliance-specific entities may need to be added or changed.

## Rev 2.x first flash

Rev 2.x boards do not have USB. The first flash needs a **3.3 V logic** USB-to-UART adapter connected to the unpopulated J2 holes or the J3 Tag-Connect pads. Do not connect 5 V to these pins.

| J2 pin | Board signal | Connect to |
| --- | --- | --- |
| 1, square pad | 3.3 V | A regulated 3.3 V source capable of powering the ESP32 |
| 2 | Ground | Adapter ground |
| 3 | Boot | Ground only while entering the bootloader |
| 4 | Board RX | Adapter TX |
| 5 | Board TX | Adapter RX |
| 6 | Enable | Optional reset control |

Use only one power source at a time. Some USB-to-UART adapters cannot provide enough 3.3 V current for an ESP32 Wi-Fi board; use a separate regulated 3.3 V supply when needed and connect its ground to the adapter ground.

1. Connect J2 Boot to Ground.
2. Apply 3.3 V power, or power-cycle the board if it was already on. This starts the serial bootloader.
3. In ESPHome Device Builder, choose **Install** and select the serial adapter. With the command line, run:

   ```console
   esphome run your-config.yaml --device /dev/cu.your-usb-serial-device
   ```

4. When the upload finishes, disconnect Boot from Ground and power-cycle the board.

## Rev 3B and Rev 3C native USB first flash and recovery

Rev 3B and [Rev 3C](../pcb/rev3c/README.md) both use the Seeed XIAO ESP32-C3 module and its native USB-C connector — Rev 3C sockets a pre-soldered module instead of soldering one down, but the firmware steps below are the same for either board. Appliance power energizes the same rail as the USB connector's VBUS; connecting both at once can back-feed a computer through the USB cable. Only one physical power source may be connected at a time. Keep the appliance unplugged whenever USB is connected, including for first flash and recovery. This design has no USB debug logging while the appliance is connected — use the Wi-Fi logs instead once the board has joined the network. In the existing YAML substitutions, change `esp32_board` from its default to `seeed_xiao_esp32c3`:

```yaml
esp32_board: seeed_xiao_esp32c3
```

For USB logging during bring-up, replace the existing `logger:` block with this one (the GEA UART remains on its normal pins):

```yaml
logger:
  baud_rate: 115200
  hardware_uart: USB_SERIAL_JTAG
```

Connect a data-capable USB-C cable to the XIAO USB connector. Hold the onboard BOOT button while connecting USB, then release it when the bootloader port appears; use RESET to retry if needed. Select the USB serial device in ESPHome Device Builder or with `esphome run`.

### J2 backup programming (design candidate)

Rev3B and Rev3C are also planned to have a permanent, factory-populated, SMD 2x3 `J2` header for backup programming when USB access is impractical. This pinout is a design candidate, not yet confirmed on assembled hardware:

| J2 pin | Signal | Connect to |
| --- | --- | --- |
| 1 | Regulated 5 V in (through an isolation diode) | A regulated 5 V supply |
| 2 | Ground | Adapter ground and supply ground |
| 3 | Boot (GPIO9) | A jumper to ground to enter the bootloader |
| 4 | Module RX (GPIO20) | Adapter TX |
| 5 | Module TX (GPIO21) | Adapter RX |
| 6 | Rev 3B: Enable. Rev 3C: not connected | Rev 3B: briefly connect to ground, then release, to reset the processor. Rev 3C: leave unconnected — use the module's **RESET** button instead. |

Before using J2, disconnect both the USB cable and the appliance connection; only one power source may be connected to the board at a time. J2 logic is 3.3 V only; never connect adapter power or signal into the module's `3V3` pad. An ordinary 3.3 V USB-to-UART adapter with TX/RX/GND and jumper leads is sufficient — no special boot-control hardware is required. If the 5 V supply and the adapter are separate devices, connect the supply ground, the adapter ground, and J2 pin 2 together. Rev 3C also removes the carrier's `EN` pull-up and its link between J2 pin 6 and J3 pin 1, since `EN` is not brought out to a side pin on that revision; see the [Rev 3C board guide](../pcb/rev3c/README.md#j2-backup-programming) for details.

To enter the bootloader, connect pin 3 (Boot) to ground and apply the regulated 5 V supply. If already powered: on Rev 3B, briefly ground pin 6 (Enable) then release it while keeping Boot grounded; on Rev 3C, press the module's **RESET** button instead while keeping Boot grounded. Select the UART adapter in ESPHome and flash the firmware. Remove the Boot jumper and reset again (Rev 3B: ground pin 6 briefly; Rev 3C: press RESET) to start the firmware. This pinout still needs confirmation on assembled hardware.

## Later updates

Later updates can be installed over Wi-Fi from ESPHome Device Builder. From the command line, run the same `esphome run` command and choose the network device when prompted.

## Connect to the appliance

These steps apply to qualified boards. Rev3B is still a prototype and is not ready for appliance connection.

1. Disconnect the programming adapter and install the board in its enclosure.
2. With the appliance off, connect the adapter to its service port. This connector is not Ethernet.
3. Power the appliance and wait for the board to join Wi-Fi.
4. Add the discovered ESPHome device in Home Assistant.

With the supplied configurations, the green LED shows Wi-Fi connection and the yellow LED shows GEA bus activity. The red LED is available to ESPHome but is not assigned a status by these examples.
