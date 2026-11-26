# Catalog and primary datasheet verification

Research completed 2026-10-05 UTC. Read-only research; no order, contact, publication, upload, repository change, or physical test.

## LCSC catalog observations

The web reader returned these primary LCSC catalog indications during 12:44:51-12:45:00 UTC on 2026-10-05. This is the observation time, not the stock-count update time. The reader exposes cached/crawled content; counts are neither reservations nor verified ordering/assembly availability. C104108 especially has stale evidence. A separate search excerpt for C17539 later showed a different older count, confirming that retrieved variants should not be represented as a live inventory feed.

| LCSC ID | Manufacturer / exact MPN | Resistance | Stock indication observed | Reader crawl label | Primary URL |
|---|---|---:|---:|---|---|
| C17539 | UNI-ROYAL 0805W8F2003T5E | 200 kohm | 450,500 | today | https://www.lcsc.com/product-detail/C17539.html |
| C17713 | UNI-ROYAL 0805W8F4702T5E | 47 kohm | 1,145,200 | today | https://www.lcsc.com/product-detail/C17713.html |
| C104108 | RALEC RTT052203FTP | 220 kohm | 500 | last month | https://www.lcsc.com/product-detail/C104108.html |
| C17673 | UNI-ROYAL 0805W8F4701T5E | 4.7 kohm | 2,253,500 | today | https://www.lcsc.com/product-detail/C17673.html |

All four primary catalog pages specify thick film, 0805, 125 mW, +/-1%, 150 V voltage rating, +/-100 ppm/C, and -55 to +155 C; minimum and multiple 100; standard full reel 5,000. Catalog identity establishes the supplied resistance, not the original circuit designer's intent. C104108 and C17673 match the proposed 220 kohm and 4.7 kohm values; they change the cataloged 200 kohm and 47 kohm values by +10% and -90%, respectively.

## Manufacturer resistor evidence

UNI-ROYAL SMD-SP-001, Chip Series, V.10, dated 2025-07-28:
https://www.uni-royal.cn/en/images/userfile/file/1769240915c56505e6d9ab55c7.pdf

- Page 2: 0805=package; W8=1/8 W; F=+/-1%; T=tape/reel; 5=5,000; E=standard. The four-digit resistance group uses three significant digits and a power-of-ten multiplier: 2003=200x10^3=200 kohm; 4702=470x10^2=47 kohm; 4701=470x10^1=4.7 kohm.
- Page 4: body L 2.00+/-0.15, W 1.25(+0.15/-0.10), H 0.55+/-0.10 mm; terminal A and B each 0.40+/-0.20 mm; 0805 standard rating 1/8 W.
- Page 5: 150 V maximum working, 300 V maximum overload, 500 V dielectric withstand; -55 to +155 C. Power remains rated through 70 C, then derates to zero at 155 C. Continuous voltage is sqrt(PxR), capped at maximum working voltage; overload is the lesser of 2.5 times rated voltage and maximum overload.
- Page 6: these values, being above 10 ohm, have +/-100 ppm/C TCR. Short-time overload qualification lasts 5 seconds.

RALEC IE-SP-010, RTT Series, version date 2026-01-27:
https://www.ralec.com/upload/media/product/file/IE-SP-010%20.pdf

- Page 1: RTT=thick film series; 05=0805; 2203=220x10^3=220 kohm using four-digit 1% coding; F=+/-1%; TP=4 mm pitch carrier tape, 5,000 pieces.
- Page 2: RTT05 rated 1/8 W at 70 C; 150 V maximum working, 300 V maximum overload; +/-100 ppm/C for 1% values from 10 ohm through 27 Mohm; operating -55 to +155 C.
- Page 3: body L 2.00+/-0.10, W 1.25+/-0.10, H 0.50+/-0.10 mm; L1 0.35+/-0.20 and L2 0.35+/-0.15 mm. Above 70 C, power derates to zero at 155 C; rated voltage=sqrt(RxP).
- Page 5: short-time overload test applies 2.5 times rated voltage for 5 seconds, subject to the general maximum ratings.

Both series use standard 0805/2012 size. Their body-height and terminal dimensions differ slightly; package-size equality alone is not a full land-pattern or assembly-process validation.

Calculated nominal continuous-voltage ceilings at full 125 mW: C17539 150 V; C17713 76.65 V; C104108 150 V; C17673 24.24 V. These derive from min(sqrt(PxR),150 V), and fall with power derating. The catalog 150 V number is therefore not an unconditional continuous voltage across the lower-resistance parts.

## Nexperia BAV99

Primary PDF: https://assets.nexperia.com/documents/data-sheet/BAV99.pdf
Product data sheet dated 2022-07-01, page 2, Table 2: pin 1 A1, anode diode 1; pin 2 K2, cathode diode 2; pin 3 K1/A2, cathode diode 1 and anode diode 2. Table 3 specifies SOT23, 2.9 x 1.3 x 1.0 mm body, 1.9 mm pitch. The internal forward path runs 1 -> 3 -> 2. This confirms pin identities; actual board connections require the schematic/netlist.

## Diodes 74LVC2G07W6-7

Primary PDF: https://www.diodes.com/datasheet/download/74LVC2G07.pdf
DS35162 Rev.6-2, March 2015; currently returned official download.

Page 2: W6=SOT26; -7=7-inch tape/reel, 3,000. Pins: 1=1 A, 2=GND, 3=2 A, 4=2Y, 5=VCC, 6=1Y. Both gates are non-inverting open drain: input HIGH releases the output (Z); input LOW sinks it (L). An external pullup determines the released voltage.

Page 3: VCC 1.65-5.5 V; input 0-5.5 V. At VCC=5.0 V, VIH minimum=3.5 V and VIL maximum=1.5 V. At VCC=3.3 V (3.0-3.6 V band), VIH minimum=2.0 V and VIL maximum=0.8 V. Voltages between these limits have no guaranteed logic state. Input transition-rate limit is 10 ns/V at both supplies.

General caveat: a 3.3 V input is not guaranteed HIGH when this gate is powered from 5 V. Parent context identifies legacy U4 on +5 V and U5 on +3.3 V; this catalog research does not establish a miswired supply or a cross-domain drive.

Page 4: low-output voltage max 0.1 V at 100 uA; higher-current limits depend on supply, load, and temperature. HIGH input does not source a driven HIGH output.

## Other historical identities

C309871 is resolved by the primary catalog to Brightking SMAJ20CA/TR13, SMA(DO-214AC), bidirectional TVS. Catalog: 20 V reverse standoff, 22.2 V breakdown listing, 32.4 V clamping, 12.3 A peak pulse, 400 W peak pulse, 1 uA reverse leakage. Source observed around 12:46:27-12:46:37 UTC, reader crawl label three weeks ago:
https://www.lcsc.com/product-detail/C309871.html

The manufacturer-hosted SMAJ-series entries found in search were unavailable when opened (404):
https://brightking.yageo.com/uploadfiles/file/tvs/202104120053065368203.pdf
https://brightking.yageo.com/uploadfiles/file/tvs/2022120421221522156375.pdf
Consequently the exact catalog identity is confirmed, but no presently reachable manufacturer PDF was downloaded or used to independently confirm the TVS ratings.

C2993047 remains unresolved. Exact-ID searches and primary LCSC English/Chinese/product-image URLs returned no usable identity; a JLCPCB direct-ID URL likewise failed. The historical 5.2 V/SOD-523 description is not enough to choose an MPN. No substitute, guessed manufacturer, nominal-voltage reinterpretation, or current availability claim is made.

## Evidence files and verification

Four manufacturer PDFs were downloaded into this directory. Exact download timestamps, URLs, byte counts, and SHA-256 hashes are in download-manifest.json. Manufacturer revision dates were verified in the PDFs. Selected pages were rendered and visually inspected for resistor dimensions/ratings/ordering and gate/diode pin and threshold tables. Text extraction is provided beside each PDF. evidence-sha256.txt hashes the persisted evidence and this report. No LCSC HTML was downloaded; the catalog observations above came from the web reader and preserve its crawl labels.
