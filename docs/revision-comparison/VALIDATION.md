# Board validation and current decisions

Snapshot: October 3, 2026. Rev3C is the focus. **Both original appliance
PIN1 and PIN3 inputs and automatic selection are required.** Use the original
dual-input source; the restricted PIN1 experiment is rejected and archived.
Cost optimization must preserve functionality. No revision is a manufacturing
release or a qualified fallback.

## Comparison and recommendation

| Revision | Strengths | Limits and current role |
| --- | --- | --- |
| Rev1.0 | Public editable historical snapshot can be recovered | Historical design with unresolved schematic/board parity; not a new-build candidate |
| Rev2.0 | Built legacy architecture and archived assembly material | Historical source recovered; pairing and native issues unresolved, old UART silk/reset behavior |
| Rev2.1 | Built C3 board with manual input selector | Superseded; known reset behavior, courtyard/centroid and legacy power gates |
| Rev2.2 | Already merged upstream; corrected predecessor board-file defects | Manual selector, external UART, 200 mA regulator and unresolved protection/thermal/courtyard gates |
| Rev3A | Integrated C3, native USB and recovery controls; no removable-module retention issue | Intended Power routing fails, 53 ERC warnings; input protection/headroom and physical behavior unqualified |
| Rev3B | XIAO approach and clean digital source; no socket stack | Module soldering/sourcing and incomplete historical quote; same input-stage qualification gaps |
| Rev3C shared | Replaceable pre-headered module without user soldering; four real C3/C6 firmware builds | Both-input restoration/voltage protection under review; common case, source and physical qualification pending |

Continue Rev3C, with C3 first and C6 flexibility preserved. Keep Rev3A as the
integrated alternative and Rev3B as a soldered-module comparison. Do not reopen
the already merged Rev2.2/file-organization change as a duplicate upstream PR.
Focused cleanup candidates and universal CI/docs remain separate.

## Native checks, with source and engine boundaries

Genuine KiCad **9.0.9**, full severities, schematic parity and expanded track
reporting were used. Error/warning counts are shown separately. No rule or
severity was lowered to make a pass. These checks do not prove source current,
thermal, RF, assembly or appliance qualification.

| Source | ERC errors / warnings | DRC errors / warnings | Unconnected / parity | Meaning |
| --- | ---: | ---: | ---: | --- |
| Rev1.0 historical 8798404 | 3 / 276 | 0 / 51 | 0 / 59 | Exact historical CAD recovered; migration/definitions/parity still need review |
| Rev2.0 historical af1f2c4 | 3 / 168 | 1 / 62 | 0 / 6 | Exact historical CAD recovered; assembly pairing and source issues unresolved |
| Rev2.1/2.2 public bc0d524 | 3 / 164 | 2 / 62 | 0 / 0 | Inherited baseline, not a pass |
| Rev2.1/2.2 reviewed cleanup | 0 / 0 | 1 / 0 | 0 / 0 | C9/C10 courtyard conflict remains; no physical net/pad/route/placement drift |
| Rev3A public a5a9fac, configured rules | 0 / 53 | 0 / 7 | 0 / 0 | Some intended Power patterns miss actual slash-prefixed nets |
| Rev3A corrected intended rules | 0 / 53 | 62 / 5 | 0 / 0 | Real routing clearance gate; standard aggregation reports 57 errors |
| Rev3B public c5db989 and reviewed cleanup | 0 / 0 | 0 / 0 | 0 / 0 | Correct Power/Switching patterns; separate electrical/physical gates remain |
| Shared dual-input Rev3C restoration | 0 / 0 | 0 / 0 | 0 / 0 | Restored sourceade0f40; independent native/manufacturing/netclass checks pass |

Rev3A's 62 expanded findings comprise 26 pad/track, 22 via/track, nine
track/track and five J1 PTH-pad/track conflicts at the retained **0.25 mm**
Power clearance. None are intrinsic pad-spacing or zone findings. The J4 local
locating-hole rule does not waive them. Six courtyard findings observed under
a different native-engine run do not reproduce on the exact public 9.0.9 head;
that does not erase the separate intended-rule findings.

Legacy corrections make the existing 25 mil schematic grid explicit, retain
source-exact local symbol/footprint definitions, fix U4's local GND contact and
UART/silk/documentation, and improve readable exports. The final C9/C10 overlap
was not hidden: simple moves caused new copper errors and were reverted.
Rev2.1 has 60 fitted references, Rev2.2 has 59; original packages are preserved.
Rev2.1's inherited J1/U3/U6 centroid offsets are explicit and still need vendor
placement review.

Historical Rev1.0 CAD comes from 87984047ee029efb83bf9947dc21818fd18e39b3,
whose Gerber ZIP is the exact same Git blob as the current archived Rev1.0 ZIP.
Rev2.0 CAD comes from af1f2c40029ef67c56910fb2c55feac835553525 and labels
itself Revision2.0. Recovery of bytes does not establish current source/export
geometry agreement or electrical qualification. Current package source absence
is distinct from source being unavailable in public history.

## Power and service gates

The old Rev3C has both source paths, source-OR diodes and Q5 PIN1 priority.
Do not confuse removing a required path with validating its ratings. The
minimum correction review considers PMOS orientation/source-referenced gate
clamps, both-path TVS/switch/fuse/diode coordination and actual module headroom.

SUNMATE SMF16A specifies **26 V at 7.7 A** under its stated pulse conditions,
while TPS22810 permits 18 V recommended / 20 V absolute input/enable. Neither
a 16 V standoff label nor GE/FirstBuild collaboration closes that rating gap.
The original PMOS orientation/gate network and unprotected PIN3 need review.
These findings are not proof of inevitable damage on an actual appliance.
[TI TPS22810](https://www.ti.com/lit/ds/symlink/tps22810.pdf).

FirstBuild uses two TPS22810 paths, transistor PIN1 priority, output OR diodes
and an AP2204K-5.0TRG1 **linear** regulator feeding the XIAO5V header. Its
D101 runs from5V0 back toV_INPUT across the LDO. Our AP63205 **buck** path
adds forward D11 loss. Neither topology guarantees regulated5V from the
annotated internal4.3V node. Actual purchased module fuse/diode/regulator
headroom and demand matter, not an ideal5.000V net name.
[FirstBuild schematic](https://github.com/geappliances/home-assistant-adapter/blob/4888a7df56e8ce6382ed91e4b95bd5020f1802f6/doc/schematic-v1.0.pdf),
[AP2204](https://www.diodes.com/assets/Datasheets/AP2204.pdf),
[AP63205](https://www.diodes.com/datasheet/download/AP63200-AP63201-AP63203-AP63205.pdf).

The legacy Rev2.2 ledger includes D7 Brightking SMAJ20CA's32.4V rated clamp
versus Si2309CDS's±20V gate limit and C9's25V rating, plus TPAP2205-33Y's
200mA output rating versus Espressif's≥500mA supply recommendation. Current
recommendation is supply capability, not constant measured draw or an observed
brownout. Regulator/fuse/zener thermal and fault coordination remain open.
[TECH PUBLIC U6](https://datasheet.lcsc.com/datasheet/pdf/fd26d7d3e25ad612545261598570292a.pdf?productCode=C19268131),
[Vishay PMOS](https://www.vishay.com/docs/68980/si2309cd.pdf),
[Brightking D7](https://datasheet.lcsc.com/datasheet/pdf/46ae16a137e777e7cee21219438eb4cc.pdf?productCode=C309871),
[ST L7805](https://www.st.com/resource/en/datasheet/l78.pdf).

Leave UART VCC disconnected. Do not inject 3V3 into a board/module output.
Use one reviewed source only; no safe universal appliance voltage range has
been inferred. Actual refrigerator model, loaded voltage/current, transient
waveforms, cold/hot startup, Wi-Fi peaks, inrush, recovery and thermal limits
remain missing. A direct5V bypass can restrict higherPIN3 sources; buck-boost
changes cost/layout/current demand. Neither is selected without review.

## CI and firmware evidence

Universal public-main CI candidate: **da38953046f20f211e2e4523506fdf58a861a1b8**.
CircleCI schema validation passed with telemetry disabled. Immutable KiCad9.0.9,
ESPHome2026.9.1 and Python container digests are verified. Fresh containers and
hosted jobs have not run; local tools are independently validated.

Jobs separately check source inventory, native full-severity ERC/DRC/parity,
intended netclass assignments, BOM/CPL/native-Gerber agreement, real firmware
compiles and release readiness. Missing source or infrastructure errors remain
failures. Passed qualification gates require tracked, committed evidence and
exact current source hashes; current gates remain blocked. Metadata or geometry
drift, missing patterns/source and untracked evidence are rejected by focused
negative checks. Config/schema validation is not hosted execution.

Both legacy GEA profiles and all four shared C3/C6 profiles passed real local
config/compile checks using ESPHome2026.9.1 and ESP-IDF5.5.5, with factory/OTA
binaries and ELF hashes recorded. GEA is pinned at
283ff2b0dfe90a6d14a5417a23176d433be8a5b3. No module was flashed or attached
to an appliance. Shared Matter/Thread appliance firmware is not implemented.

## Mechanical and package boundary

The retained Rev3C case is **C3-only legacy**. A five-piece common-case concept
exists as an unqualified review prototype; its exact final CAD was not restored
in this pass. C6 button access, antenna clearance, module stack/retention and
physical tests remain gates. The comparison galleries are historical previews;
new cleanup packages include their own matched native review assets.

Current candidates are local and reviewable. No new PR, publication, merge,
purchase, physical qualification or appliance test is claimed.

## Local source package heads

| Candidate branch | Final source head |
| --- | --- |
| fix/legacy-board-review | 7b3201de09d19bec6a10d9e90b4b02792bda6972 |
| fix/rev3a-reviewed-source | 689093fe168f412be0053a483e38277e3121ea2d |
| fix/rev3b-reviewed-source | bc9212a8b66845b3ce0cdf36bdfc96e4851fa9ae |
| design/rev3c-shared-dual-input | ade0f40b17ea30bc8b6f70665dd0e3bf4c579644 |
| ci/native-board-validation | da38953046f20f211e2e4523506fdf58a861a1b8 |

These are unpublished review candidates, preserved separately from public
baselines. They are not links to nonexistent hosted commits. The rejected
PIN1-only head0b600c56a284e1871e153abe6bfdc5839760cdcf is preserved on
archive/rev3c-pin1-only-rejected and is not a candidate for release.
