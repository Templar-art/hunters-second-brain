# Import audit 01: 53/3 Robina Town Centre Drive (first look, 2026-10-28)

Sources (untouched, in `~/Downloads`):
- CubiCasa export: `3_robina_town_centre_drive_53_gold_coast/` with SVG, PDF, PNG and JPG, each with and without dimensions. The folders ` 2` and ` 3` are identical copies.
- The supplier's finished plan: `3 Robina Town Centre Drive.pdf`. It is one page made in "DesignCraft", for the client Coastline Prestige.

## CubiCasa SVG (`svg-with-dim`)
- **Size and coordinates:** 4000×3000 px, with a viewBox of about 583×437 user units. The plan sits inside one top group with a `matrix(0.2136,…)` transform, and there are 100 transforms in total.
- **Elements:** 465 `g`, 198 `polygon`, 42 `path`, 37 `line`, 37 `text`, 22 `rect` and 20 `circle`. There are 3 tile `pattern`s.
- **Text is real text, not outlines.** The font is Josefin Sans, embedded as a base64 woff2. Each room has two separate nodes, the name and the dimensions:
  - Example: "PRIMARY BEDROOM" and "4.26 m x 3.43 m".
  - Footer: "1st floor: 126 m2 (Excluded areas 67 m2)" and "Total GLA: 126 m2 | Total: 193 m2".
  - Disclaimer: "FLOOR PLAN CREATED BY CUBICASA APP…".
- **There are no classes or semantic IDs.** About 40 objects are grouped under `data-automation-id` UUIDs; these look like the fixtures, doors and windows. They are grouped, but nothing says what type each one is. About 72 polygons sit outside any object; these are likely walls and room floors, which still has to be confirmed.
- **Nothing dangerous found:** no `script`, `foreignObject`, `image`, `use` or external `href`. Sanitising is still needed in principle.

## What the supplier changed (matched pair)
- **Labels:**
  - Title case.
  - Renamed rooms: Primary Bedroom → Master Bedroom; Bedroom → Bedroom 2 and Bedroom 3; Bath → Ens. and PDR; Laundry → L'dry; Garage → Double Garage; Living Room → Living; Dining Area → Dining.
  - **Dimensions rounded to 1 decimal place**, e.g. 4.26 × 3.43 → 4.3m x 3.4m and 9.15 → 9.2m.
  - Dimensions dropped on small rooms (Kitchen, Foyer, W.I.C., Ens., PDR).
- **Styling:**
  - Black walls.
  - Textured floor fills: carpet in bedrooms, tiles in wet areas and dining, stone in living, concrete in garage and patio.
  - Fixtures drawn as filled black shapes.
- **Composition:**
  - A4 landscape with an address header.
  - Bed, bath and car icons with counts.
  - North arrow.
  - "GROUND FLOOR" title.
  - Areas reworded as "Internal 126 / External 67 / Total 193".
  - Client logo, 10X logo and a disclaimer.
- **Information that isn't in the source:**
  - A site plan: an aerial or illustrated lot with a numbered legend.
  - Land area of 224 m².
  - The north direction.
  - Bed/bath/car counts. These are derivable but should be confirmed.
- **Geometry:** none spotted at preview resolution. This still needs an overlay check.
