# Legacy assembly and regulator metadata

Reviewed October 5, 2026. These changes correct assembly bookkeeping and exact-part documentation. They preserve every numbered connection, component value, footprint geometry, route, jumper function and historical fabrication archive.

- Rev1.0 mounting holes H1–H4 and bare test pads TP1–TP7 are excluded from the purchasing BOM. R1 already said `DNP`; it now has an explicit do-not-populate flag and BOM exclusion. Its pads and connections remain present.
- Rev2.0 mounting holes H1/H2 are excluded from the purchasing BOM. They are board features, rather than parts to place. Other existing DNP choices remain intact.
- Rev2.0/2.1 retain C5205181, Diodes AP2205-33Y-13, with its exact [manufacturer datasheet](https://www.diodes.com/assets/Datasheets/AP2205.pdf) and 200 mA description. The historical AP2204R symbol identifier remains an explicitly documented alias. Numerical pins are unchanged: 1 VIN, 2 GND, 3 VOUT.
- Rev2.2 retains C19268131, TECH PUBLIC TPAP2205-33Y, with its [exact manufacturer-authored sheet](https://atta.szlcsc.com/upload/public/pdf/source/20231201/421357A3C66CA1DC6983E93125C75712.pdf) and 200 mA description. That sheet's drawing identifies output pin 3 while its table says pin 5; the conflicting table remains a manufacturer/supplier qualification question.

Rev1's mutually exclusive pull-up/pull-down banks, optional LED/switch and unresolved R5 value are preserved. No assembly variant is silently selected. Missing current Rev1/Rev2.0 supplier BOM/CPL files remain explicit gates.

The 200 mA regulator descriptions are rated-capability limits. Neither regulator establishes the WROOM module's documented supply provision of at least 500 mA plus carrier overhead. These metadata corrections do not implement a regulator or power-topology repair and do not claim a guaranteed field failure. Input gate/capacitor/TVS coordination, linear-regulator thermal margin, startup behavior and actual appliance source limits remain open.

The [exact source delta](legacy-metadata-correction.json) records before/after hashes. Retained native reports and schematic renders describe their stated earlier inputs; current-head native and manufacturing checks must be recorded after publication.
