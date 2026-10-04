# Rev3C component model assets

The current [component model accuracy checkpoint](../../MODEL-ACCURACY.md) is the
canonical human-readable source/provenance/transform receipt. These are partial
visual references; complete manufacturer assembly CAD and physical fit remain
unverified.

The carrier now associates:

- XIAO_ESP32C3_v1.3_vendor_pcb_visual_reference.step: official Seeed v1.3 PCB/copper,
  40 generic KiCad component models, omitted shields/switches/U.FL/chips/headers in the baked asset.
  A separate licensed named-part U.FL model is associated with the carrier at
  the official C3/C6 ANT datum; its nominal dimensions match the Hirose drawing.
- Socket_HCTL_PM254-1-07-Z-8.5-drawing-detail.step: self-authored manufacturer-drawing
  body/tails, illustrative receiving recesses.
- RJ45_EVERCOM_5301-8P8C-RevA-drawing-detail.step: self-authored Rev A dimensioned
  body and signal tails, illustrative cavity/contact springs; locating-post solids
  omitted because their profile/insertion depth is not established.

XIAO_ESP32C6_v1.0_vendor_pcb_visual_reference.step is a distinct alternative
partial preview. The render script makes a transient model-only swap for C6;
there is one canonical electrical carrier. No male-header SKU, mating depth,
measured installed Z, physical fit or RF qualification is inferred.

See [XIAO asset license](XIAO-ASSET-LICENSE.md), [KiCad library license](KICAD-LIBRARY-LICENSE.md)
and [module provenance](../../validation/xiao-model-provenance.json). Seeed-derived
assets carry CC BY-SA 4.0; KiCad component data has its library exception. The
repository MIT license covers the self-authored connector generator/fallbacks.

The previous C3 installed block, socket and RJ45 envelopes, historical unused J2
recovery-header model and obsolete Bourns fuse model remain as unused reference
files. They are not active exact-part models. U9/U10 and F1/F2 still use explicitly
approximate maximum envelopes; other fitted package models use the inherited
KiCad 9.0.9 library. No exact vendor cosmetic CAD is claimed for those packages.

Regenerate connector fallback assets with generate_connector_detail.py using
build123d 0.11.1. Native rendering and protected-source verification scripts are in
../../validation/. Every model scale is 1:1.
