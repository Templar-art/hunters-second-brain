---
type: project
tags: [floor-plans, tooling, cubicasa]
status: milestone-2
updated: 2026-11-03
---

# Floor-plan app (in-house finishing of CubiCasa exports)

**Goal:** stop paying an outside drafter to restyle CubiCasa plans. The app takes CubiCasa's own SVG, keeps its geometry and measurements exactly as supplied, and produces the 10x house style (see [[floor-plan-house-style]]; the Oct 2026 template is the standard). It does not use image generation and does not regenerate the plan with an LLM.

Code: `projects/floorplan-app/` contains `fp.py` (stdlib, run with the typeset venv), `review.html` and `house-style.json`. Preview config: `floorplan-app` on port 8790.

## Milestone 1 (built 2026-10-28)

- **Import:** `fp.py import-all` reads every folder in `raw/floorplans/cubicasa/`. It copies the folder to `jobs/<slug>/source/` and makes the copy **read-only**, then picks the `svg-with-dim` SVG. Supplier finals in `raw/floorplans/finals/<slug>.*` are attached so the two can be compared.
- **Sanitise (the SVG is untrusted):**
  - A DOCTYPE or ENTITY declaration is refused outright.
  - Elements and attributes are whitelisted.
  - Script, foreignObject, image, use, `a` links and `on*` handlers are stripped.
  - Any `url()` that isn't `#id` or embedded font/PNG data is stripped, and so is `@import`.
  - Every removal is logged in the job.
  - The page also runs under a strict CSP.
  - Tested against a booby-trapped SVG: everything was stripped, and the entity attack was refused.
- **Labels:** each text node is classified as a room, a dimension or a footer. The app then proposes the house-style text from `house-style.json`:
  - Rename rules: Primary Bedroom → Master Bedroom, Living Room → Living, Laundry → L'dry, and so on.
  - Size format becomes `4.2m x 6.1m`, with the numbers untouched.
  - **Ambiguous labels are always left to a person:** Bedroom (which number?), Bath (Bath, Ens. or PDR?), Garage (single or double?), and unnamed "Room".
  - Rounding to 1 decimal is an opt-in toggle per job, and every rounded value then needs a tick.
- **Areas:** these come from CubiCasa's printed footer text, never from pixels. Each excluded component (walls, garage, patio, deck, balcony) gets an internal/external/none choice. The defaults are walls → internal and garage → internal, matching the Oct 2026 finals.
- **Write + checks:** only `<text>` content changes, and the output goes to `jobs/<slug>/out/<slug>-10x.svg`. The checks are:
  - geometry unchanged (every non-text element identical);
  - every label approved;
  - dimension format;
  - bedrooms numbered uniquely;
  - no `1.061`-style separators;
  - north set by a person (never inferred);
  - land area supplied;
  - source still read-only.
- **Demo run on 86 Ormeau (ZED):** the labels were filled in the way the supplier did them. All checks passed except north, which was deliberately left unset. The geometry was identical across 1,294 drawing elements. The area line came out at Internal 214 / Total 214, matching the supplier's final exactly. The app's rename also avoids the supplier's "Siting" typo.

## Sources (pulled 2026-10-28)

Eight CubiCasa exports came from Tyson's CubiCasa account (Plus package, logged in as marketing@10xvisuals.com.au, free 60-day trial until 10 Nov 2026):

- 86 Ormeau Ridge Rd
- 23 Peter Senior Ct
- 4 Alex Keith Ct
- 6 Wirranina Pl
- 378 Marine Pde
- 1 Arbour Ave (commercial: reception/waiting room)
- 1 Grant Ave
- 53/3 Robina Town Centre Dr

1 Tibbing St and 58 Peter Thomson Dr are archived in CubiCasa and weren't pulled. Supplier finals exist for Robina, Ormeau and Peter Senior only.

## Findings that shape the design

- **All 8 exports share one structure:** live text, a room label followed by its size, and no scripts. Robina is the odd one out. It was exported in CAPS with an embedded Josefin Sans font and sizes to 2 decimals (`4.26 m`). The others are title case, use Verdana and give sizes to 1 decimal. **CubiCasa's style setting decides the rounding**, so the rounding question mostly disappears if the account is set to 1 decimal.
- **The supplier's area method isn't consistent.** Ormeau 214 = CubiCasa 203 + 11 m² walls. Parkwood 223 = 179 + 16 walls + 28 garage. Robina 126 is CubiCasa's GLA with no walls added. ⚠️ An agreed method is needed. The app shows every component instead of guessing.

## Milestone 2: the 10x page (built 2026-10-28)

The goal was "look as good as the supplier final, but better". `render.py` turns the checked SVG into a finished A4 landscape page and exports SVG, a vector PDF and a 300 dpi PNG through headless Chrome. The page tab in the review app shows it, with an Open PDF link.

**Skin (presentation only).** Only fill, stroke, font and display change, plus added `<defs>`. The geometry check still compares every points/d/transform attribute and **passes on all 8 jobs**.

- **Walls:** charcoal `#4b5157` with a soft drop shadow.
- **Openings:** windows and doors are white with hairline outlines. CubiCasa's marker triangles are hidden.
- **Floors:** each floor polygon takes the material of the room label inside it:
  - wood is the default;
  - tile for wet areas;
  - carpet for bedrooms;
  - honed concrete for the garage;
  - timber boards for decks;
  - pavers for patios.

  Textures are drawn **at true scale**, because 1 SVG unit = 1 cm (verified against the printed room sizes, worst error ≤ 10 cm): boards 18 cm wide, tiles 60 cm.
- **Labels:** Poppins, name 500, size 400 grey.

**Page:**

- Header: address, with the suburb in caps.
- Bed, bath and car icons.
- North arrow, **only when a person has set north**.
- Thin frame.
- Storeys laid out side by side at **one shared scale**, ordered Basement → Ground → Upper. They wrap to two rows when that prints bigger: Alex Keith's 1-room basement sits above the other storeys.
- 5 m scale bar, **only when the scale check passes**. Robina's old-style export can't be checked, so it gets no bar.
- Optional site-plan image with a legend.
- Area strip, taken from CubiCasa's footer figures.
- Client logo (from `clients/<name>.json`), disclaimer, 10x logo.

**Why it's better than the supplier's:**

- The scale and textures are true.
- The geometry is provably untouched.
- No typos: the supplier's "Siting" doesn't happen.
- Nothing appears unless it's verified: no guessed north, no unverified scale bar.
- One click to rebuild.

**Still open:**

- **Area rule (needs Hunter):** recommended PCA, where Internal = floors + walls and garage/patio/deck = External. The app currently counts the garage as internal, to match the Oct finals.
- **North:** set per job.
- **Logos:** ZED's full lockup (only the Z mark is on file); Coastline and Harcourts profiles don't exist yet.
- **Storey naming:** Upper or First Floor.
- **Alex Keith:** the upper deck around the pool renders unfilled.

## Site plan from the address (built 2026-11-03)

`sitegen.py <job>` makes the site-plan aerial for any QLD job from the address alone. It doesn't need supplier files or a drone flight.

**How it works:**
- **Lot lookup:** uses the QLD cadastre through [[drone-pin-tool]]'s lookup. Unit addresses are rewritten to the register's `U53/3 …` form.
- **Aerial:** the free QLD government aerial (Spatial Imagery Subscription Plan, the latest public state program). It's fetched at up to 2,048 px, which is the service's limit.
- **Orientation:** the lot is turned so its long side is vertical. `site_flip` in the job turns it 180°.
- **Finish:** the image is lightened a little and faded to white at the edges like the Gen B finals, and the lot line is drawn in white.

**Markers:** the numbered markers are stored as `site_markers` in the job (label plus x/y on the image) and are placed by a person. The page draws them as vector circles in the client's marker colour, and the Legend lists them in order.

**Land area:** the cadastre figure is stored as `land_area_suggested` and is never printed on its own. Robina's cadastre area is 232 m², but the supplier final says 224 m² (probably the listing figure).

**Limits:**
- The government imagery can be years old, so new builds may be missing; use a drone nadir for those.
- QLD only.
- It's a real photo, not the illustrated look the supplier uses.
- An illustrated repaint is about 75 Magnific credits per try (Nano Banana Pro at 2K with 2 references). Not run yet.

## Site plan: drawn from a traced roof (2026-11-03)

The AI repaints looked right but **redrew the house**: the roof shape and proportions came out wrong (Hunter: "that is not what the house looks like"). They cost 150 cr in total.

Building the roof from the CubiCasa footprint failed on a second house, for two reasons:
- Auto-placement flipped Robina 180° and couldn't be trusted.
- Ormeau's scan has no garage, so part of the real roof was missing. **CubiCasa only knows the rooms that were scanned.**

**Current route** (`/trace/<slug>` in the review app, then `sitedraw.main_traced`):
1. A person clicks the roof's eave corners on the QLD aerial, about 30–60 s per job. Each wing is traced as its own "tiled" section, and patios as "flat".
2. The person places the numbered markers.
3. Code draws the illustrated plan: hip planes from a rectangle cover of each section (straight hips and valleys), 60 cm eaves, tile texture, the lot line from the cadastre, and a faded rounded card.

No AI and no credits. The roof is the real roof as seen from above, but it is always drawn as hips, so gables and skillions aren't represented yet.

## Next

1. Hunter signs off the page look and the area rule.
2. Run a live job end to end: CubiCasa export → app → client PDF.
3. Site plan from our own drone top-down via [[drone-pin-tool]] instead of a manual upload.
4. **Parked (Hunter, 2026-10-28):** the page "needs a cool exterior". Exterior treatment is still undefined: site/land outline, landscaping, or a drone aerial. Pick it up after sign-off.
5. **Parked:** area rule undecided ("not sure"). Garage stays Internal, matching the Oct finals, until decided.
