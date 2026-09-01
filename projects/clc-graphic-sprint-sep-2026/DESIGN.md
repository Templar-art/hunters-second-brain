# DESIGN.md — Coast Life Constructions social system

Register: **brand**. The grid is the product demo. Source of truth is `canvas/build.py`;
this file explains the decisions behind it. Edit copy there, re-run, re-seed.

## Scene

A Gold Coast homeowner, mid-renovation-research, thumb-scrolling at night on a phone.
They have three builders open. Coast Life has ten seconds to look like the expensive one
without looking like it charges for the wrong reasons. That forces **light-dominant with
deep navy punctuation** — not a dark-mode feed (reads as an agency, not a builder) and not
all-white (reads as a template).

## Palette — identity-preserved, sampled from the logo artwork

| Token | Value | Role |
|---|---|---|
| Ground light | `#f5f7f9` | Cool off-white, faint navy tint. **Never warm cream.** |
| Ground deep | `#102f41` | Navy punctuation: close slides, one mid-slide per carousel |
| Navy | `#2a4f8d` | Wordmark navy, from the logo |
| Blue | `#1884c7` | Icon/wave blue, from the logo. Rules and radial lifts. |
| Steel | `#2f6690` | Kicker on light grounds |
| Sky | `#97c8e8` | Kicker on deep grounds |
| Ink | `#16242e` | Body |

Strategy: **Restrained** on interiors, **Drenched** on close slides. The photography carries
the colour; the system stays out of its way.

⚠️ Do not sample `#61a8d8` from `Coast-Life-Constructions-Brand-Uplift.pdf` — that is 10x
Visuals' blue in our own pitch deck about them.

## Type

**Poppins only**, three weights. Headlines at 300 (Light) — at 72–96px the thin weight reads
architectural rather than shouty, which is the whole positioning. Kicker at 600. Body at 400.
A second family was considered and rejected: two families at this size range compete, and
Poppins is already their committed identity.

- Hero headline auto-scales: ≤40 chars → 96px, ≤62 → 84px, else 72px. Scale is the drama.
- Letter-spacing `-0.012em` on heroes, `-0.005em` elsewhere. Never past `-0.04em`.
- `text-wrap: balance` on every heading.
- Contrast verified: ink on light ≈ 7:1, sky on navy ≈ 7:1, white on navy ≈ 15:1.

## Grid

1080 × 1350. Side margins 112 → 856 content column. Footer baseline 72 from the bottom:
slide counter left, logo right (200px), on **every** slide — their shipped system does this.

Two slide families, deliberately different objects:

**Hero — full bleed.** Photo edge to edge. A 96 × 3px blue rule, kicker, headline, sub-line
stacked in the bottom gradient. Gradient reaches ~58% so the build stays fully visible above
it — this is the treatment Rob approved, and it is stronger than a framed cover.

**Base — framed.** Cool off-white ground, photo in an 856 × 880 window at y=52, caption tight
beneath. The window is deliberately tall: at 760 it left a dead band above the footer and read
as a PowerPoint content slide.

## Rules earned the hard way

- **Kickers are service labels, not eyebrows.** `NEW BUILDS`, `EXTENSIONS`, `RENOVATIONS`,
  `SECONDARY DWELLINGS`, `SERVICE AREA` carry information. Voice fragments like "How we work"
  were removed — an eyebrow above everything is the saturated AI tell.
- **No 01/02/03 scaffolding** unless the content genuinely is a sequence (the process post,
  the three-things post). Three services are not a sequence.
- **Never cover or dim the build.** Type lives in the gradient or below the frame.
- **Never crop or re-grade a supplied photo.** The window is fixed so slides match on swipe.
- **Landscape photos die in portrait crops.** Check every hero rendered, not in the abstract —
  the renovations cover was cropping onto a blank wall until it was swapped for a portrait source.
- **Close slides are bare.** Headline, two lines, logo. A rule and a coastline motif were both
  tried and both read as noise on navy.
- **No AI-generated homes, rooms or site scenes.** Ever. Real projects or a marked placeholder.

## Verification

Artboards are static HTML, so they render outside the canvas runtime:

```bash
cd canvas && python3 build.py && node <seed-canvas.mjs> --check ../coast-life-post-templates.html
```

For a visual pass, extract each artboard's inner markup into a contact sheet with images
inlined as data URIs and screenshot it headless. Designing these blind produces plausible
code and broken compositions — the crop failures were invisible in source.
