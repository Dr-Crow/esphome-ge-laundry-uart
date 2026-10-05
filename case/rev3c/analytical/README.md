# Parametric Rev3C enclosure review

This is an editable analytical derivative of the [recovered prototype](../prototype/). It keeps a common base, module-specific C3/C6 lids and three light guides. The selected carrier outline and both appliance power inputs are preserved. The four lids support internal/external antenna concepts; exact cable, switch and printed-assembly qualification remains open.

**Use review exports for dimensional review and coupons. They are not approved production files.** Fixed original button reaches fail nominal actuation at an installed stack of 11.0 mm. The common closure permits a wrong lid: a C3 BOOT foot can contact C6 U.FL. Check the module label before assembly; labels do not mechanically prevent this mistake.

The [source-bound report](review/CASE-ANALYSIS.md) records valid solids, installed-stack samples, component envelopes, actual guide routes, plug gauges and antenna provisions. Analytical geometry was generated with build123d 0.10.0 / cadquery-ocp 7.8.1.1.post1. The recovered historical requirements are a separate, not-yet-reproduced toolchain. These versioned checks are not physical fit, material or RF tests.

## Reviewable corrections

- `configure()` sets installed stack from 11.0 to 11.65 mm, independent BOOT/RESET heights, gaps and stops, plus optional stack-adjusted USB height. It does not establish a safe switch overtravel limit.
- A separate C3 leaf-root offset of 17.3 mm, instead of 16.6 mm, lowers the nominal fixed-guided strain screen to 0.427–0.495%. This meets the stated example screen, with material/fatigue and tolerance margin still unproved.
- `pipe_with_cap_relief()` removes only local lower crescents near manufacturer maximum capacitor bodies. The chosen 0.15 mm solder-lift allowance and 0.25 mm clearance are design requirements. The nominal LED inlet projection, upper path and roof retention stay unchanged; reduced inlet area needs optical/print testing.

![Guide relief and preserved LED inlet](review/guide-relief-candidate.png)

## Explicit review export

Use an existing authorized installation of the recorded analysis tools. `export_review.py` requires an explicit module, stack and switch/stop dimensions so a known-bad default is not silently presented as a print-ready assembly. An illustrative C3 command is:

```sh
python export_review.py --module c3 --stack 11.325 \
  --boot-height 1.5 --reset-height 1.5 --boot-stop 0.4 --reset-stop 0.4 \
  --leaf-offset 17.3 --relieved-guides --output exports-review-c3
```

Those are conditional analytical parameters, not measured switch limits or a recommended production calibration. For C6, use its separately verified switch identity and dimensions. The report's 0.53 ±0.10 mm C6 height remains conditional; the nominal 0.36 mm stop is not a manufacturer overtravel allowance. The export includes the explicit parameter/source receipt and five review pieces. Extra coupons or proxy electronics are excluded from that five-piece set.

## Open assembly checks

Current maximum-body and base/lid screens clear at three sampled stacks. A 12 ×6 mm synthetic USB plug gauge clears; a 14 ×8 mm gauge fails the rounded aperture. Choose a real plug and verify shank depth, strain relief, insertion and finger/latch access. Antenna maximum slabs and nominal bulkhead hardware clear their stated screens, while cable terminations, bend/slack, panel tolerance and RF remain open.

Before fitting a board, verify the actual male/female header seating and retention, both switch make/overtravel/force specifications, wrong-lid prevention, slicer/coupon clearances, light transmission and actual antenna/plug envelopes. Leave UART VCC disconnected. Disconnect the appliance cable before powered USB. The 40 V switch selection is not a 40 V rating for the complete carrier.
