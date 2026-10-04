# PCB Rev 2.0

Rev 2.0 reworked the board for automated assembly and adopted an ESP32-C3 module and pinout compatible with the project direction at the time.

> [!WARNING]
> UART RX/TX text uses the appliance or attached-programmer perspective: J1.5 is ESP TX and J1.4 is ESP RX. See the exact [UART direction map](native-review/REVIEW.md#exact-uart-label-meanings) before wiring. The inherited warning called the labels swapped, but a blanket mismatch is not established across these perspectives. U1 can cause ESP32 boot loops. This revision is retained for history and is not the recommended starting point for a new order.

## Files

- [Historical PCBA archive](manufacturing/PCBA-OnionStraws-rev2.0.zip)
- [Schematic PDF](validation/schematic.pdf)
- [Board render](validation/board-render.png)
- [Board STEP model](validation/board.step)
- [Historical board photograph](images/assembled-board.jpg)

The photograph was stored as `v2.jpg` in the repository root. Its exact Rev 2.x subrevision was not recorded.

Editable source has now been restored from the exact historical commit and received a bounded native cleanup. See [the editable design](design/README.md) and [current native review package](native-review/REVIEW.md) for the preserved circuit, four intentional ERC alias warnings, thermal/silkscreen exceptions and fresh current CAM. The historical files linked above remain byte-identical original artifacts; they are separate from the current exports.

[Back to the PCB revision index](../README.md) · [Rev 2 enclosure](../../case/rev2/README.md) · [Separate firmware review](STANDALONE-REVIEW.md#firmware-review)

[Standalone candidate scope and release boundaries](STANDALONE-REVIEW.md).
