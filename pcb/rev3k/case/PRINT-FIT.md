# Rev 3K, 3L and 3M enclosure fit

## C3 antenna and closure

The earlier common base overlapped 9.0 mm³ of the C3 flexible-antenna reservation in each revision. Its forward tongue on the antenna side rose to z = 8.9 mm. The revised tongue and its small bump stop at z = 7.65 mm, below the antenna's lower edge at z = 8 mm. The three other tongues retain their full height. Each variant still uses one common base and its module-specific lid. Total modeled closure interference across the four catches drops from 0.420 to 0.355 mm³ per lid. Print a base in the intended material and check closing force, retention on handling, and release by hand.

Each case generator checks both final enclosure halves against the 40 × 20 × 1.8 mm antenna reservation and a 2 mm diameter coax routing envelope with build123d 0.10.0. The regression rejects contact or positive overlap. Each original STEP base reproduced the 9.0 mm³ collision in a separate import. The corrected STEP bases gave the same minimum clearance as the generators.

| Reservation | Minimum clearance to base | Minimum clearance to C3 lid |
| --- | ---: | ---: |
| Flexible antenna | 0.350 mm | 0.120 mm |
| Coax routing envelope | 14.204 mm | 0.218 mm |

The 0.12 mm gap at the upper rail is small enough that a print or a different antenna can consume it. Fit the real antenna, its feed and the seated plug in the open case. Close gently and reopen to check for pinching and pull on the socket. The 5 mm planar elbow covers only one section of the path. Measure usable cable length, confirm the cable maker's bend limit at the plug and check the installation arc as the lid closes. Antenna performance needs an installed-unit RF check.

## Buttons and light guides

Measure the height of the seated module and its BOOT and RESET switches above the carrier before choosing a printed plunger length. The lids use an 11 mm socket-stack assumption. On C6 the 0.36 mm stop motion minus the 0.25 mm rest gap leaves 0.11 mm. That equals the catalog travel of the assumed switch. A lower module can leave the button short of contact, and a higher module can preload it. Identify the fitted switch, then test both buttons with the assembly disconnected using a continuity meter. Confirm contact before the hard stop, release when let go and absence of contact at rest after repeated operation. Check C3 separately with its own lid and switch height. [Assumed C6 Alps SKTAAAE010 switch dimensions and travel](https://tech.alpsalpine.com/e/products/detail/SKTAAAE010/)

Each 1.76 mm guide sits in a nominal 1.98 mm roof hole. Its lower collar prevents the guide from exiting outward. With the lid removed the guide can slide inward. Test each printed guide with the lid inverted and during ordinary handling. Check optical alignment and visibility with the assembled unit during subsequent bench testing. Guide retention, button actuation, latch force and RF performance remain physical tests.
