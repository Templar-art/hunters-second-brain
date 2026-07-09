# 10x "Scroll-to-Build" Spec Piece — Design

**Date:** 2026-07-09
**Owner:** Hunter (10x Visuals)
**Status:** Built (2026-07-09) — see Build Note below. Pivoted from vector-first to
photoreal frame-scrub mid-build once Hunter supplied the CVA render.

## Purpose

A reusable, 10x-owned sales/portfolio web page that demonstrates scroll-driven
animation ("the house builds as you scroll"). Shown one-to-one to prospects
(CLC, Bespoke, developers) to sell scroll-driven experiences as a 10x service.
It is a spec/demo piece, not a client deliverable and not a public marketing page.

## Decisions (locked during brainstorming)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Client / goal | 10x demo / spec piece | Reusable sales weapon; 10x controls the brand; no client-asset blocker |
| Reveal approach | **Hybrid** — blueprint draws itself → dissolves into photoreal | Tells the "idea → built" story, which is the 10x pitch |
| Page structure | **B · Narrative Sell** | Sells the service without burying the wow |
| Photoreal source | **Vector-first now, photoreal drop-in later** | Ships today, zero cost, zero asset dependency |
| Photoreal upgrade asset | Architect-partner renders (Hunter has them) | Slot in later; genericise/get permission before any PUBLIC use |

## User Experience

Single scrolling page, dark architectural canvas. Flow top to bottom:

1. **Header** — 10x logo, minimal.
2. **Hook** — one line ("Watch it come together.") + scroll cue.
3. **The pinned build (hero)** — a `sticky` stage held on screen while the user
   scrolls through a tall track. A home assembles in ~8 beats:
   ground line → foundation slab → wall framing → roof frame → cladding fills →
   glazing (windows/door) → roof material → landscaping + sky warms →
   **photoreal cross-dissolve finale**. Small uppercase captions fade in at each stage.
4. **Concept · Craft · Delivered** — 3-beat strip that doubles as the pitch.
5. **Proof line** — one line on what 10x does.
6. **CTA** — "Book a call" button in brand blue.

## Architecture

Four isolated parts, each with one responsibility:

1. **Track + stage (CSS only).** A ~500vh parent creates scroll distance; a
   `position: sticky; top: 0; height: 100vh` stage pins the artwork. No JS.
2. **`getScrollProgress()`.** Reads scroll position of the pinned section →
   a single clamped `0→1` number. The only source of truth for the animation.
3. **Build director.** Maps ranges of progress to visible state:
   - `0.00–0.45` — blueprint draws on via SVG `stroke-dashoffset`, stage by stage.
   - `0.40–0.80` — materialise: fills fade/scale in, colours warm.
   - `0.80–1.00` — photoreal cross-dissolve finale.
   Pacing uses an easing/threshold curve so the roof + materialise "money shot"
   gets extra scroll room (not evenly spaced).
4. **Photoreal slot (drop-in).** A `PHOTOREAL_FRAMES` config array at the top of
   the file:
   - Empty (ships today) → finale shows a rich shaded-vector "finished home".
   - Populated with image paths later → finale scrubs those frames instead.
   No other code changes needed to upgrade vector → photoreal.

## Brand & Visual

- Canvas: deep navy `#0e1a24`; blueprint linework in brand `#61a8d8`.
- Type: Poppins (headings) / Montserrat (body), loaded from Google Fonts with a
  system-font fallback so it degrades gracefully if offline.
- Restraint: nothing moves except the build. Captions are small uppercase kickers.
- CTA button in `#61a8d8`.

## Tech & Constraints

- Vanilla HTML/CSS/JS, **one self-contained file**. No build step, no external
  JS libraries, no backend. Opens by double-clicking.
- Scroll handler throttled via `requestAnimationFrame`.
- Honours `prefers-reduced-motion`: shows the finished home immediately.
- Mobile-aware: sticky build works on touch scroll; layout reflows.
- **Location:** `10x Scroll Build/index.html` in the vault (git-backed).
  Alternative if preferred: `~/Desktop/General Folder/10x Premium Kit/`.
- **Cost:** zero. No Higgsfield/Magnific/credit spend at any point in this build.

## Out of Scope (YAGNI)

- No GSAP / Three.js / WebGL.
- No CMS, backend, analytics, or multi-page site.
- No render generation now (photoreal is a later drop-in of existing assets).
- No client-specific branding — this is the 10x-owned demo.

## Photoreal Upgrade Path (future, not this build)

When ready: extract frames from the architect renders (ffmpeg, free) into a
`frames/` folder, populate `PHOTOREAL_FRAMES`, done. Confirm usage permission /
genericise before any public posting.

## Build Note (2026-07-09)

The vector-first build was completed and shown, but on review Hunter wanted the
hyper-realistic look of reference reels, not illustration. Hunter supplied a real
render (`CVA Render Video.mp4`, 4K, ~41s). We pivoted to the **photoreal frame-scrub**:

- Extracted ~164 frames at 1728px via ffmpeg (free, local): `fps=4,scale=1728:-2 -q:v 3`.
- Rebuilt `index.html` as a full-bleed `<canvas>` that preloads the frames and draws the
  one matching scroll progress (retina-aware cover-fit, nearest-loaded fallback, loader).
- Minimal overlay: opening title, one mid caption, hero finale, outro + CTA.
- Honest credit on the page: "Render: CVA Architects · Scroll experience: 10x Visuals."
- Frames are git-ignored (client asset, ~28MB); `README.md` documents regeneration.

The original vector approach and its `PHOTOREAL_FRAMES` drop-in slot are superseded by
this direct canvas scrub. Verified end-to-end in a real browser (scrub, captions,
finale, no console errors).

## Success Criteria

- Opens with no install; the home visibly assembles as you scroll and reverses
  as you scroll back.
- Feels premium and on-brand (dark, blueprint-blue, restrained).
- A prospect immediately understands "10x can build this for me."
- Photoreal frames can be added later by editing one config array.
