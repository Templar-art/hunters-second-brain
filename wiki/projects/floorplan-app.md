---
type: project
tags: [floor-plans, tooling, cubicasa]
status: milestone-1
updated: 2026-10-28
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

## Next milestone

1. Restyle the drawing to the Oct template: grey walls, floor fills by room type, solid fixtures. This depends on proving that walls and floors can be told apart.
2. Build the A4 page: header, bed/bath/car icons, north arrow, area strip, client block, disclaimer, 10x logo.
3. Export to PDF and PNG from the same SVG.
4. The site plan stays a manual drop-in image.
