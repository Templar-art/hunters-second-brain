# Construction Mid-Year Wrap — Editorial Carousel

Date: 2026-06-19
Status: Approved (Hunter), ready to build

## Goal
A 10x Visuals showcase carousel for Instagram: a mid-year "look what we shot" reel of construction/trade client work for the first half of 2026. One cohesive editorial carousel, **one slide per client**, that shows range — from finished architectural homes to boots-on-site trade work.

## Format
- **Instagram carousel, 4:5 portrait, 1080 × 1350 px**, 6 slides.
- Cover → 5 client slides. **No sign-off/CTA slide** (Hunter cut it — ends on the last client).
- Render **locally** (PIL + brand fonts). No credits, no paid ops.

## Visual system (brand-accurate)
Derived from the 2026-06-18 editorial system + brand guidelines v1.0.

- **Logo:** real master PNG only, never text. `10xVisuals_White Logo Blue X.png`. **Cover only** — white wordmark top-left, ~78px wide equivalent (≈26% of frame width), soft drop-shadow. **Client slides 01–05 carry NO logo** (Hunter: the small corner mark read badly — work speaks for itself).
- **Light scrim** (photos must breathe — Hunter asked twice for less scrim): navy `#102f41` gradient, transparent at top → ~0.12 at 60% → ~0.66 at base. Text legibility from a drop-shadow on the text block, not a heavy wash.
- **Bottom band** (every client slide, bottom-left): number (`01`–`05`, Poppins Bold, blue `#61a8d8`) · kicker (scope, Montserrat 700 uppercase letter-spaced, sky `#8ec6e8`) · client name (Poppins Bold white).
- **White keylines:** photos sit in a grid with ~3px white gutters on a white base — the "border" device, editorial contact-sheet feel (not a full mat).
- **Palette:** navy `#102f41`/`#0d2734`, blue `#61a8d8`, kicker sky `#8ec6e8`, white. Charcoal `#141414` available. Use colour minimally.
- **Type:** Poppins Bold headings/names, Montserrat kickers/labels. From `~/Library/Fonts/`.
- **Copy rule:** NO dashes — middots `·` and slashes `/` only. Sentence case for body; client names as branded.

## Two slide templates
1. **Cover / single hero** — full-bleed photo, scrim, wordmark top-left, title block bottom-left.
2. **Spread** — big hero pane (left, ~1.45fr) + supporting pane(s) in a right column, 3px white keylines between. Band sits on the hero. Right column holds 1, 2, or 3 stacked supports depending on photo count.

## Slide lineup (locked)

| # | Client | Kicker | Hero | Supports |
|---|--------|--------|------|----------|
| Cover | — | `Construction · Gold Coast` / headline **Mid-year wrap** / `2026` | `Camera-2 (1).jpg` (twilight rear) | — |
| 01 | **MakerBuild** | New build · architectural | `Camera (1).jpg` (twilight entry) | `Maker Build-16.jpg` (kitchen), `Maker Build-2.jpg` (stair) |
| 02 | **Coast Life Constructions** | Site · fitout · drone | `Camera (2).jpg` (fitout) | `Camera-6 (1).jpg` (drone aerial) |
| 03 | **Salisbury Building Projects** | Civil · electrical · reno | `Camera-7 (1).jpg` (worker, golden hour) | `DSC05386.jpg` (groundworks), `Camera-8 (1).jpg` (concrete pump), `Camera-4 (1).jpg` (bathroom) |
| 04 | **MVX Electrical** | Electrical | `Camera-2 (2).jpg` (two electricians) | `Camera-3 (1).jpg` (wide beach / tower) |
| 05 | **Shape** | Commercial · CSI Club Southport | `Camera-5 (1).jpg` (CSI exterior) | `CSi Southport-22.jpg` (umbrellas), `CSi Southport-13.jpg` (bistro) |

Note: slide 05's client is the builder **Shape**; CSI Club Southport is the venue (named in the kicker).

## Focal crops (keep the best part in frame)
Each pane center-crops to fill; focal point per hero set so the subject isn't cut:
- Cover `Camera-2 (1)`: vertical focus ~42% (house + sky).
- 01 hero `Camera (1)`: ~40% (lit entry / soffit).
- 02 hero `Camera (2)`: ~30% (the two chippies high in frame).
- 03 hero `Camera-7`: ~38% (backlit worker); bathroom support biased ~65% horizontal (tub).
- 04 hero `Camera-2 (2)`: ~35% (electricians' faces).
- 05 hero `Camera-5`: ~42% (big CSI sign).

## Source assets
- Main 10 shots: `~/Desktop/Construction mid year wrap up/` (`Camera*.jpg`).
- MakerBuild interiors: `~/Desktop/maker photos for mid year wrap up/` (`Maker Build-2.jpg`, `Maker Build-16.jpg`). **Do NOT pull from `~/Desktop/Maker Carosel/` — reserved for a separate MakerBuild carousel.**
- Salisbury groundworks: `DSC05386.jpg` (from `~/Downloads/`).
- CSI/Shape interiors: `CSi Southport-13.jpg`, `CSi Southport-22.jpg` (from `~/Downloads/`; `-11` also available).
- Logo: `~/Desktop/10x Final Cut stuff/10xVisuals_White Logo Blue X.png`.
- Fonts: Poppins + Montserrat in `~/Library/Fonts/`.

## Output
- New folder: `~/Desktop/Construction Mid-Year Wrap - SLIDES/`
- 6 PNGs at 1080 × 1350: `00_cover.png`, `01_makerbuild.png`, `02_coastlife.png`, `03_salisbury.png`, `04_mvx.png`, `05_shape.png`.
- A re-runnable build script (PIL) saved alongside so copy/photos/crops can be tweaked and re-rendered.

## Render approach
PIL composites each slide: white base → paste focal-cropped photos with 3px gutters → draw navy gradient scrim (hero panes only) → paste logo (cover only) → draw band text (Poppins/Montserrat). Mirrors the brand mockup `editorial-brand-v6.html`.

## Out of scope
- Sign-off / CTA slide (cut).
- Logo on client slides (cut).
- Maker Carosel / extra Maker Build shots (reserved).
- Coast Life RAW interiors (`.ARW`) — excluded; need an edit pass first.
- Any paid generation/upscale (Higgsfield/Magnific) — local render only.
- The separate real-estate mid-year wrap (`~/Desktop/realestate mid year wrap up/`).

## Known caveat
Client branding is visible in-frame (Salisbury jacket, MVX van, CSI signage, Ballina truck). This deliberately bumps the standing **no-third-party-branding** rule for general posts — accepted here because a client wrap is a credit reel; showing client work is the intent.
