# Reviewed nominal body-datum export

This is an export-coordinate correction, with no circuit, pad, track, outline, BOM or rotation change. The native footprint anchor is retained in CAD; selected CPL rows use a documented nominal body datum rather than a corner or pad-bounds centre. The source-bound proof and separately hashed authored manufacturer capture identify the exact local/export transform.

- J1: native anchor `[13.97, -12.55]` → nominal body datum `[8.645, -16.995]` mm; `manufacturer_nominal_body_bbox_center`; retained native rotation−90°.
- U2: native anchor `[77.39, -4]` → nominal body datum `[87.89, -12.9]` mm; `module_pcb_body_bbox_center`; retained native rotation−90°.

The USB protrusion/asymmetric lands do not define the XIAO PCB-body centre. The nominal EVERCOM family body differs from its inherited Fab and all-pad centres. Actual supplier-library zero, pin1, orientation, connector process/full suffix and module revision still require review; this is not assembly approval. Frozen earlier quote/CPL snapshots remain historical.
