# GE adapter design-review hub

A static website for reviewing the adapter's board revisions without opening KiCad. One page, hash-routed, no server code.

| View | What it shows |
| --- | --- |
| Overview | One card per revision (status, summary, size, placed parts, LCSC codes), recent updates from `site/data/updates.json` |
| Board | Pick a revision: 3D board (real part bodies, clickable parts with value, nets, LCSC, per-board cost), layer stack (copper, mask, paste, silkscreen, drills), top/bottom renders, schematic sheets, and a diff of parts against another revision |
| Compare | Any two revisions side by side (size, layers, part and LCSC counts, cost) and the parts added, removed or changed, matched by reference designator, with a "show changes in 3D" button |
| Cost | JLCPCB cost model for 5 or 10 boards: PCB, parts (live JLCPCB price and stock, cached), extended-part fees, assembly, optional XIAO module and printed case; a revision with a documented JLCPCB quote (`documented_quotes`) shows the quote instead of the estimate |
| Case | The printed case as 3D parts (base, lids, light guides, magnets, antenna references) placed around the board, with print time and filament where a slicer was available |
| Docs | Every markdown document from the repository, rendered in the page, with search |

Everything shown is generated from the files in this repository (`pcb/`, `case/`, `docs/`); nothing is typed in by hand
except `site/data/pricing.json` and `site/data/updates.json`.

## Layout

```
tools/review-hub/
  site/
    index.html            the viewer: hand-written three.js app. The build never touches it.
    data/pricing.json     HAND-EDITED  module prices, case cost, JLCPCB cost-model constants
    data/updates.json     HAND-EDITED  dated change log shown on the Overview
    data/ docs/           GENERATED (git-ignored): per-revision assets, cases, docs mirror
  build/
    build.py              driver (all stages); run it with plain python3
    revisions.config.json THE list of revisions and the pinned KiCad image
    hubenv.py             config, paths, venv and npm setup
    kicad_extract.py glbtools.py optimize_glb.mjs sexp.py models.py   per-revision stages
    cases_build.py        case CAD -> GLB, placement checks
    docs_mirror.py        markdown mirror -> docs.json
    publish_prep.py       writes *.gltf.json twins, strips SVG DOCTYPEs
    validate.py           checks a built site
    pages.sh              build + validate + (optionally) commit to a local gh-pages branch
    package.json, package-lock.json, requirements.txt, requirements-cad.txt   pinned tool versions
```

## Requirements

Docker (the build runs the pinned image `kicad/kicad:9.0.9@sha256:e638b79b...` with `--platform linux/amd64`),
Node 18+, `rsvg-convert` (librsvg) and Python 3.10+ (`uv` is used if present). That is all. On first run the build
creates `build/.venv` (Pillow, numpy, trimesh) and runs `npm ci` in `build/` by itself; the first case build creates
`build/.venv-cad` (build123d 0.11.1) the same way. The first build also downloads KiCad's 3D model library
(`--fetch-models`, done by `pages.sh` automatically) and queries JLCPCB's public parts search for each LCSC code,
caching every answer under `build/cache/`. PrusaSlicer is optional: without it the Case view has no print estimates.

Nothing in the repository is modified by a build: the repo is mounted read-only into the container.

## Build

```sh
python3 tools/review-hub/build/build.py                      # everything into tools/review-hub/site/
python3 tools/review-hub/build/build.py --out /tmp/hub       # ... or into another directory (a complete site)
python3 tools/review-hub/build/build.py --rev rev3g          # one revision (repeat --rev for several) + cost + index
python3 tools/review-hub/build/build.py --docs               # docs mirror + docs.json only
python3 tools/review-hub/build/build.py --cases              # case GLBs + cases.json only (board placement needs rev3c and rev3d built)
python3 tools/review-hub/build/build.py --cost [--refresh]   # cost.json only; --refresh re-queries JLCPCB
python3 tools/review-hub/build/build.py --force              # ignore per-stage caches (build/cache/<rev>/*.stamp)
python3 tools/review-hub/build/validate.py [SITE_DIR]        # JSON parses, GLBs decode, GLB nodes vs parts.json, PNG sizes, doc links, size
```

`--out DIR` makes a self-contained site: `index.html` and the two hand-edited data files are copied in. `--cache DIR`
moves the build cache (`HUB_SITE` and `HUB_CACHE` are the environment equivalents).

Optional local settings, all unset by default: `repo` (defaults to this checkout), `notes` (a private notes folder; see
"What is excluded"), `cad_python` (an interpreter that already has build123d), `ca_bundle` (a corporate proxy CA).
Set them as environment variables (`HUB_REPO`, `HUB_NOTES`, `HUB_CAD_PYTHON`, `HUB_CA_BUNDLE`) or in
`build/config.local.json` (git-ignored):

```json
{ "cad_python": "/path/to/venv/bin/python", "ca_bundle": "/path/to/ca.pem" }
```

If a TLS proxy breaks the JLCPCB, npm or pip downloads, also export `SSL_CERT_FILE` and `NODE_EXTRA_CA_CERTS` to that bundle.

## Add a revision

1. Add one entry to `build/revisions.config.json` (copy the last one). Fields: `id` (matches the folder under `pcb/`), `label`,
   `pcb` and `sch` (paths relative to the repository root), `bom` (a JLC-format CSV path, `{"zip": ..., "member": ...}`, or `null`),
   `case` (a case id from `cases.json`, or `null`), `status` (`original`, `superseded`, `pivot option`, `blocked` or `candidate`),
   `date` and `date_basis` (say where the date comes from: a commit, a file timestamp), a one-sentence `summary` (25 words or fewer),
   `readme` (repo path or `null`) and `documented_quotes` (a list; cite a real quote and the file it is in, never an estimate).
2. `python3 tools/review-hub/build/build.py --rev <id>`, then `python3 tools/review-hub/build/validate.py`.
3. Add a dated entry to `site/data/updates.json` if the change deserves one on the Overview.
4. Rebuild and publish (below). `data/revisions.json` is regenerated from every revision that has been built, in config order.
5. A new case design goes into `build/cases_build.py`, the one place case ids, parts and board placement live.

## Rebuild one revision

```sh
python3 tools/review-hub/build/build.py --rev rev3e            # re-extracts only if the .kicad_pcb or the build scripts changed
python3 tools/review-hub/build/build.py --rev rev3e --force    # rebuild every stage of that revision
```

The stages are cached by content hash under `build/cache/<rev>/`, so an unchanged revision takes seconds.

## What is produced (paths relative to `site/`)

| Path | Producer |
| --- | --- |
| `data/revisions.json` | glue; counts come from the files below |
| `data/<rev>/board.gltf.json` | `kicad-cli pcb export glb --subst-models ...`, then `optimize_glb.mjs` (gltf-transform 4.3.0: join, dedup, meshopt) |
| `data/<rev>/board.json`, `parts.json` | `kicad_extract.py` (pcbnew) plus netlist fields and the manufacturing BOM |
| `data/<rev>/layers/*.png` | `kicad-cli pcb export svg`, rasterised with `rsvg-convert` at 20 px/mm |
| `data/<rev>/renders/{top,bottom}.png`, `sch/` | `kicad-cli pcb render`, `kicad-cli sch export svg` |
| `data/<rev>/cost.json` | JLCPCB public parts search, cached per code in `build/cache/jlc/` |
| `data/cases.json`, `data/cases/<id>/*.gltf.json` | `cases_build.py` (build123d export, STL to GLB, same meshopt step) |
| `docs/`, `data/docs.json` | `docs_mirror.py` (credential-pattern scan first; flagged files are skipped and listed in `build/cache/docs-skipped.json`) |

Frames: board GLBs are in metres with `X = (kx - cx)/1000`, `Z = (ky - cy)/1000`, Y up, 0 at the board bottom, where (cx, cy) is the
Edge.Cuts bounding-box centre; footprint nodes are direct children of the root and named by reference designator. Layer PNGs cover
exactly `bbox_mm` at 20 px/mm. Case GLBs keep the case CAD axes (z up), in metres; `board_placement.matrix_mm` maps case mm to board-GLB mm.

## Hosting

The site is fully static: HTML, JSON, PNG, SVG, Markdown and `.gltf.json`, with hash routing (`#board-rev3g`), relative URLs and no
server code, so it works from a project sub-path such as `https://<user>.github.io/<repo>/`. Libraries load from CDNs at view time:
three.js 0.160 from cdn.jsdelivr.net, marked and DOMPurify from cdnjs.cloudflare.com, fonts from Google Fonts.

GLB files are published as `board.gltf.json` twins (`publish_prep.py`, a base64 buffer inside plain JSON with the meshopt data unchanged),
because some static hosts do not serve `.glb` with a useful content type. The `.glb` files stay in the build output for `validate.py` and are
not published.

**GitHub Pages from a gh-pages branch**

```sh
tools/review-hub/build/pages.sh --commit
git -C ../<repo>-gh-pages push origin gh-pages      # the script prints this exact command; it never pushes itself
```

`pages.sh` builds into `tools/review-hub/out/site`, runs `validate.py`, then commits the site (without `.glb`) to a local orphan `gh-pages`
branch in a separate worktree (`<repo>-gh-pages`, next to the checkout). Then, in the GitHub repository, Settings, Pages: Source "Deploy from
a branch", Branch `gh-pages`, folder `/ (root)`. `--skip-build --commit` republishes an existing build; `--help` lists the other options.

**Any other static host** (Netlify, S3, nginx, `python3 -m http.server`): run `python3 tools/review-hub/build/build.py --out DIR` and serve `DIR`
(delete the `*.glb` files first if size matters). Preview locally with `python3 -m http.server -d DIR`.

The Feedback tab, "Leave feedback" and the per-part feedback buttons need the Claude artifact runtime (`window.claude.use('db')`). On any other
host the page detects that and hides those controls; the Overview says "Feedback is only available in the Claude-hosted copy of this hub."

## What is excluded from the public build

* Private working notes. The maintainer keeps plans, research and Reddit drafts in a notes folder outside this repository; `docs_mirror.py`
  mirrors it ("Plan & findings", "Research" and "Reddit drafts" groups) only when `notes` is configured explicitly. Without it `docs.json` holds
  repository documents only. Do not set `notes` for a build you intend to publish.
* Anything that looks like a credential or an email address: a markdown file with a hit is not copied and is listed in `build/cache/docs-skipped.json`.
* `certs/`, `logs/`, `venvs/`, dotfile paths and linked images of 4 MB or more are never mirrored.
* Absolute local paths: published JSON uses repo-relative paths.
* Generated output, the build cache (`build/cache`, several hundred MB), `build/node_modules`, `build/.venv`, `build/.venv-cad` and
  `build/config.local.json` are git-ignored.

## For AI agents and reviewers

* Do not edit generated files (`site/data/**` other than the two JSON inputs, `site/docs/**`); change the config or a script and rebuild.
* `site/index.html` is hand-written; the build never rewrites it. Keep the data contracts it reads (`revisions.json`, `board.json`, `parts.json`,
  `cost.json`, `cases.json`, `docs.json`, `pricing.json`, `updates.json`).
* Facts in `revisions.config.json` (`summary`, `date_basis`, `documented_quotes`) must come from a file or commit in this repository. Never put an
  estimate in `documented_quotes`.
* Check a change with `build.py --rev <id>` and `validate.py`; both must pass before publishing.

## Known limits

* Without KiCad's 3D model library (`--fetch-models`), only footprints whose model lives in the project's own `models/` folder get a mesh; four
  models are missing upstream (Rev 1 to 2 RJ45, Rev 2 fuses and switches, Rev 3A to 3C inductor) and stay as boxes.
* Rev 1.0 and Rev 2.x reference KICAD6/KICAD8 library models only, so their GLBs contain just the board body.
* Cases are built for the Rev 3C/3D outline. Rev 3E and 3F share it and are listed with that case; Rev 3G has its own closed-USB lids under
  `pcb/rev3g/case/` that `cases_build.py` does not build yet.
* The Overview calls the first revision with status `candidate` the current candidate.
