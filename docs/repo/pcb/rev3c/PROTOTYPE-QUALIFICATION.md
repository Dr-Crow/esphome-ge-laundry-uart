# Rev3C prototype qualification plan

Updated October 5, 2026. Review baseline: `11826a7f6ba1ed19131ddba46e4d62b06196a8c6` on `integration/ge-restored-final-2026-10-04`.

The selected prototype retains both appliance PIN1/PIN3 inputs, automatic PIN1-presence priority, the AP63205 buck, socketed C3/C6 interfaces and the 99 × 40 mm carrier. Its TPS1H200A switches are 40 V-rated components; the complete carrier is not rated for a 40 V supply. C3 is the first qualification target, with independent C6 coverage using the same carrier.

[Carrier overview](README.md) · [Power limits](POWER-QUALIFICATION.md) · [Rated-switch review](RATED-SWITCH-OPTION.md) · [Recovered enclosure source](../../case/rev3c/README.md) · [Shared firmware](../../firmware/shared-rev3c/README.md) · [Ordering files](ORDERING.md)

## Evidence already available

At the baseline, exact hosted native ERC/DRC and intended-rule checks pass for all seven board revisions, 28 validator tests pass, and eight real firmware configurations/builds pass. Current Rev3C CAM/source and its 83-reference BOM/CPL parity pass. Fresh source-matched JLCPCB quotes are $134.64 for five or $168.92 for ten assembled carriers before shipping, tax, modules and case. These results establish digital consistency and an observed quote, not assembly, appliance, enclosure or electrical qualification.

The shared enclosure's editable all-printed source is now recovered. It has useful matching XY datums but historical electronic proxies, provisional heights and untested printed mechanisms. Its earlier renders and nominal collision counts are reference material. No equipment has been energized, no case printed and no physical test performed in this planning pass.

## 1. Freeze the actual prototype and test envelope

Record the carrier/firmware source hashes, populated part markings, module hardware revision, header type and insertion depth, antenna/cable identities, enclosure source/parameters and printer profile. Use the matching selected Gerber/BOM/CPL trio from [ORDERING.md](ORDERING.md); verify supplier pin-1/rotation/body alignment, exposed-pad/stencil coverage, DNI D8 paste treatment and socket/through-hole solder process before assembly approval.

Obtain the exact target appliance model and port pinout, nominal and loaded voltage tolerances, permitted continuous/peak accessory current, source impedance and relevant positive/negative transient envelope. Published nominal 5/7.5/9/13.6 V examples do not supply those missing limits. Define a reviewed, current-limited isolated bench procedure and numerical acceptance criteria before powered testing; do not infer a safe appliance voltage range from a part label or an old guide.

## 2. Close the dual-input power gates on a reviewed bench

Use an approved emulator of the appliance's two rails before any appliance connection. Measure the path and both modules' supply rails at startup and under defined load/RF demand. Test limits and fault energy must be chosen from the actual source and exact parts, not copied from this plan's illustrative component calculations.

| Proposed check | Evidence needed to accept the prototype |
| --- | --- |
| PIN1-only and PIN3-only, each C3/C6 | Reliable cold/hot startup, no unintended resets, adequate chip supply and correct bus levels across the reviewed source/load envelope. AP63205 is a buck; nominal 5 V input does not imply a regulated 5 V output. Evaluate the actual module's supply path. |
| Both appliance rails and source removal | PIN1-presence priority is retained; no unsafe crossfeed; removal/recovery is controlled. Characterize weak or current-limited PIN1 inhibiting healthy PIN3, since this design does not implement fault-aware fallback. |
| Inrush/current limit and retry | Actual startup finishes without indefinite retry. The provisional limit is about 0.606 A nominal, with conditional 0.510–0.704 A bounds; fault retry is approximately 35–45 ms on and 0.8–1.2 s off. These figures are not an OEM current allowance or a system load rating. |
| Positive/negative/reverse steps and clamp energy | Bound PMOS drain/source and gate/source differentials, switch/control voltages, PPTC differential voltage, buck input, TVS current/energy and sustained fault behavior. The SMF16A 26 V table clamp is conditional on its specified pulse/current/temperature. |
| Enclosed thermal and loss budget | Measure fuse, PMOS, switch, OR diode, buck, output diode and module temperatures/voltages with actual copper, ambient, case and load. Hot PPTC hold and diode limits remain independent of switch current limiting. |

The retained PMOS differential rating is 30 V, its gate magnitude limit is 20 V, AP63205 operating maximum is 32 V and PPTCs are 33 V-rated. Use design margin below applicable limits and account for charged nodes; the 40 V switch alone cannot close these gates. The approximately 86 mV added path-loss comparison at 364 mA mixes stated component conditions and is illustrative, not a measured module draw or guaranteed hot budget. Full assumptions remain in [RATED-SWITCH-OPTION.md](RATED-SWITCH-OPTION.md).

Disconnect the appliance cable before powered USB and remove USB before appliance use. Keep UART VCC disconnected; module 3V3 is an output. PIN1/PIN3 from one appliance are supported selected branches, not permission to combine appliance and USB power.

## 3. Qualify C3/C6 firmware and recovery behavior

Use the correct C3/C6 and GEA2/GEA3 profile for the exact appliance, with `JP1` at 1–2 for the documented GEA2 profiles. Destination addresses and example entities are not a verified refrigerator configuration. The pinned builds prove compilation; runtime bus behavior remains to be tested.

For each module, record BOOT/RESET/native-USB recovery, Wi-Fi startup/reconnect, API/OTA recovery, supply/reset behavior and actual appliance bus entities/error counters. Application UART logging is disabled, but ROM boot traffic can still reach the GEA3-connected side-header pins before setup. Check reset/download/brownout effects under the reviewed isolated protocol setup before live appliance use. C6 RF enable/antenna selection must match the installed antenna; do not enable external selection without that antenna connected.

Verify the roof labels against actual firmware: green `WIFI` is Wi-Fi connected, red `AUX` is manual and off at boot, yellow `BUS` is GEA bus connected. A bus-connected indication does not identify individual packets or certify correct appliance control.

## 4. Qualify enclosure fit and usability without power first

Start from the [recovered all-printed source](../../case/rev3c/README.md), keep C3/C6 lids separate and reconcile the current populated-board envelopes before regenerating meshes. Check the real socket/header stack, connector plugs/latches, solder tails, supports, module insertion/removal, button alignment and cable routes. Both power pins share J1, so the existing single appliance opening serves them. The recovered case's 11.65 mm maximum socket/spacer stack differs from the current preview's provisional 11.0 mm; applying that lower assumption would leave a 0.90 mm actuator gap beyond either stop travel. This source-assumption discrepancy must be resolved by actual seated measurements, not by accepting an old render.

Print isolated snap and button coupons first. Inspect the actual slicer layers, bridges, support removal, beam roots and guide gaps. Calibrate released gap, make point and hard stop from the fitted switch's allowed force/travel. The current C6 nominal mechanism can depress 0.01–0.21 mm solely from its conditional switch-height tolerance, versus 0.11 mm nominal travel; an unmeasured stop is not safe actuation evidence. Do not use a button as module retention.

For the assembled unpowered case, require free BOOT/RESET release and simultaneous recovery access, independent module retention, accessible snap release, adequate USB plug and RJ45 latch access, light-guide retention and readable labels. A C3 lid cannot be reused on C6: its contacts approach C6 U.FL and overlap the ceramic antenna projection. Record insertion/removal force, cable strain relief, repeated-use return/wear and heat-related creep under agreed conditions. The current prototype has no validated filament profile or lifetime claim.

Review C3 FPC retention/slack and both U.FL routes; C6 internal uses its ceramic antenna and a distinct lid. Keep metal, magnets, supports and cables clear of the reviewed antenna region. For the external/bulkhead or remote option, verify exact connector polarity/thread, panel/nut access, cable bends and lid-opening slack. Compare RF and thermal behavior with the final case, actual cable/antenna, appliance metal and placement. Do not transfer a generic antenna keepout example into a claim of qualified range.

## Completion record and decisions

Capture measured waveforms, temperatures, dimensions, instrument/settings, source/assembly/print hashes, acceptance limits and pass/fail results for each module/input combination. Keep source, power, physical and supplier gates blocked until their own evidence is reviewed; a compile, quote or nominal CAD pass cannot waive them.

The remaining inputs are the target appliance/model envelope, actual C3/C6/module/header/switch dimensions, a chosen initial enclosure/antenna arrangement and the separately approved physical test/assembly procedure. Editable case-source recovery can proceed now without another file request. No safety-circuit redesign, order or physical appliance test is authorized by this document.
