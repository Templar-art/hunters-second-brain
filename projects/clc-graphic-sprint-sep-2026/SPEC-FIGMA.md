# Coast Life — Figma build specification

Answers the A–G format in `claude-instagram-layout-reconstruction-brief.md`, using the
**real** Coast Life system already implemented in `canvas/build.py`. Rationale lives in
`DESIGN.md`; copy lives in `build.py`.

---

## ⚠️ Before anything is built to that brief

**1. No reference was supplied.** The system in that document only works against an attached
reference. To run section A properly I need: the reference cover at full resolution, every
carousel slide in sequence, and (if a Reel) the cover plus 3–6 frames. Without them, sections
B–G below are derived from Coast Life's own system rather than from any reference — which is
the safer starting point anyway.

**2. The example brief's brand kit is not Coast Life's.** Lines 540–546 specify:

| Brief says | Coast Life actually uses | Source |
|---|---|---|
| Paper `#F2EFE9` | Cool off-white `#f5f7f9` | Their shipped carousels |
| Ink `#242522` | Ink `#16242e` / navy ground `#102f41` | Shipped + logo |
| Eucalypt `#34443A` | — no green anywhere in the identity | — |
| Sandstone `#CBBEAA` | — no sand anywhere in the identity | — |
| Clay `#AE7256` | — no clay anywhere in the identity | — |
| "Refined editorial serif" + Inter | **Poppins**, three weights | Their shipped system |
| 72px outer margin, 12-col, 24px gutter | **112px margin**, single 856px column | Built system |
| Six-slide carousel | **Five slides maximum** | Hunter, this sprint |

That palette is warm cream / sand / eucalypt / clay — a plausible-looking invention, not
Coast Life's identity. Their real marks are navy `#2a4f8d` and blue `#1884c7`, sampled
directly from `coastlife-logo-1.png`. Building to the brief's kit would discard the brand.
`Inter` and "editorial serif" are also both on the reflex-reject lists.

**Treat that example block as a template placeholder someone filled in speculatively, not as
a brand instruction.** Everything below uses the verified system.

**3. The example brief assumes slab-pour assets.** We don't have them. The Ladds Ridge files
on their site (`LaddsRidge-2.jpg`, `LaddsRidge-4.jpg`) are frame and scaffold stage. The
concrete pour exists only in their March 2026 Instagram post. A slab-pour carousel needs the
original footage from that shoot before it can be built.

---

## A. Reference structure analysis

**Not available — no reference attached.** What must not be copied from any future reference
is set by the brief's own rules and holds regardless: logo lockups, typefaces chosen to mimic,
photography, project names, caption wording, proprietary motifs, exact pixel placement.

The one structural principle already borrowed from the benchmark study (Barlow, Grimmond) and
safe to keep, because it is generic: **named projects carried through highlights, captions and
hashtags**. That is an information architecture, not an expression.

## B. Original design translation

Two deliberately different frame families, so a cover never reads like an interior slide:

**Hero — full bleed.** Photograph edge to edge. A 96 × 3px blue rule, optional service label,
headline and sub-line stacked inside a bottom gradient that reaches ~58% of the canvas. The
build stays fully visible above it. Type size scales to the copy: scale is the drama, not weight.

**Base — framed.** Cool off-white ground, photograph in a fixed window, caption tight beneath.
The window is fixed so every slide in a carousel matches on swipe; the frame is the brand's
consistency device.

Navy punctuates: one mid-slide per carousel and every close slide. Photography carries the
colour; the system stays out of its way.

## C. Design tokens

| Token | Value |
|---|---|
| Canvas | 1080 × 1350 (feed) · 1080 × 1920 (story) |
| Outer margin | 112px left/right · 72px footer baseline |
| Content column | 856px, single column (not a 12-col grid) |
| Photo window — hero | Full bleed, 1080 × 1350 |
| Photo window — service/base | 856 × 880 at y = 52 |
| Photo window — static | 856 × 760 at y = 52 |
| Detail spread | primary 856 × 700 at y = 52 · secondary 412 × 340 at y = 776 |
| Spacing scale | 16 / 24 / 26 / 36 / 44 px |
| Ground light | `#f5f7f9` cool off-white, faint navy tint |
| Ground deep | `#102f41` |
| Navy (wordmark) | `#2a4f8d` |
| Blue (icon/rules) | `#1884c7` |
| Steel (kicker on light) | `#2f6690` |
| Sky (kicker on deep) | `#97c8e8` |
| Ink | `#16242e` · body at 78% |
| Typeface | **Poppins** — 300 Light, 500 Medium, 600 SemiBold. No second family. |
| Fallback | `"Helvetica Neue", Helvetica, Arial, sans-serif` |
| Hero headline | 96 / 84 / 72px by copy length · line-height 1.04 · tracking −0.012em |
| Section headline | 72–76px · line-height 1.12 · tracking −0.005em |
| Service name | 72px Light |
| Body | 34–38px · line-height 1.45 · max 800px measure |
| Kicker | 25px SemiBold · uppercase · tracking +0.22em |
| Slide counter | 22px Medium · tracking +0.16em · **`white-space: nowrap`** |
| Rule | 96 × 3px blue (hero) · 120 × 2px (interior) |
| Logo | 200px wide, bottom-right, every slide. Colour mark on light, white master on deep. |
| Contrast | ink/light ≈ 7:1 · sky/navy ≈ 7:1 · white/navy ≈ 15:1 |

## D. Figma build specification

```
FRAME: Hero / Full Bleed
CANVAS: 1080 x 1350
BACKGROUND: #102f41 (behind image)
GRID: 112px side margins · 72px footer baseline · single 856px column
LAYER STACK:
1. Image — fill frame, object-fit cover, focal point per slide
2. Top scrim — linear-gradient to bottom, rgba(10,31,44,0.40) 0% → 0% at 22%
3. Bottom gradient — to top: rgba(8,26,38,0.93) 0% · 0.80 at 22% · 0.34 at 42% · 0 at 58%
4. Rule — 96 x 3px, #1884c7
5. Kicker (optional, service labels only)
6. Headline
7. Sub-line
8. Footer row — counter left, white logo right
TEXT:
- Kicker | 25px SemiBold | uppercase | +0.22em | #97c8e8
- Headline | 96/84/72px Light | 1.04 | −0.012em | #ffffff | max 856px
- Sub-line | 34px Regular | rgba(255,255,255,0.72) | max 720px
- Counter | 22px Medium | +0.16em | nowrap
IMAGE:
- Portrait sources strongly preferred — landscape stock dies in a 4:5 crop
SHAPES:
- Rule 96x3 #1884c7 · gradients as above, no other fills
LOGO:
- cl-white.png · 200px wide · bottom-right · flex: 0 0 auto
EXPORT: {POST}Cover@2x.png
```

```
FRAME: Base / Service (framed, image-dominant)
CANVAS: 1080 x 1350
BACKGROUND: #f5f7f9
GRID: 112px side margins · 72px footer baseline
LAYER STACK:
1. Image frame — 856 x 880 at x112 y52, square corners, no radius
2. Image — object-fit cover inside frame
3. Headline — y = 52 + 880 + 42
4. Body — 16px below headline
5. Footer row — counter left (steel), colour logo right
TEXT:
- Headline | 72px Light | 1.12 | #16242e
- Body | 34px Regular | 1.45 | rgba(22,36,46,0.78) | max 800px
IMAGE:
- 856 x 880 window, fixed. Never crop or re-grade the supplied file.
SHAPES:
- None. No cards, no radius, no shadow.
LOGO:
- cl-colour.png · 200px · bottom-right
EXPORT: {POST}S{NN}@2x.png
```

```
FRAME: Base / Point (light or navy)
CANVAS: 1080 x 1350
BACKGROUND: #f5f7f9  |  #102f41 for the mid-carousel inversion
GRID: 112px side margins
LAYER STACK:
1. Kicker — absolute, y = 150
2. Content block — vertically centred, translateY(-52%)
   a. Headline
   b. Rule 120 x 2px
   c. Body (one line — anything longer belongs in the caption)
3. Footer row
TEXT:
- Kicker | 25px SemiBold | uppercase | +0.22em | steel / sky
- Headline | 76px Light | 1.12
- Body | 38px Regular | 1.45 | max 700px
EXPORT: {POST}S{NN}@2x.png
```

```
FRAME: Base / Step (numbered — sequences only)
CANVAS: 1080 x 1350
BACKGROUND: #f5f7f9 | #102f41
LAYER STACK:
1. Numeral watermark — 340px SemiBold, x = 98, y = 300, 13% ink / 16% sky
2. Content block — centred, translateY(-38%): headline, rule, body
3. Footer row
NOTE: numerals only where the content genuinely is an ordered sequence.
EXPORT: {POST}S{NN}@2x.png
```

```
FRAME: Static / Pull-quote
CANVAS: 1080 x 1350
BACKGROUND: #f5f7f9
LAYER STACK:
1. Quote block — centred, translateY(-54%)
2. Rule 200 x 2px
3. Attribution — 30px Medium, steel
4. Permission-status line — 22px, 50% ink (removed once cleared)
5. Footer — logo only, no counter
TEXT:
- Quote | 74px Light | 1.20 | #16242e
IMAGE: none — the restraint is the point
EXPORT: {POST}Review@2x.png
```

```
FRAME: Close / Navy
CANVAS: 1080 x 1350
BACKGROUND: #102f41
LAYER STACK:
1. Radial lift — 115% 80% at 84% 88%, rgba(24,132,199,0.32) → 0 at 62%
2. Content block — centred, translateY(-50%): headline, then stacked lines
3. Footer row — counter left, white logo right
TEXT:
- Headline | 92px Light | 1.12 | #ffffff | max 800px
- Lines | 36px Regular | 1.40 | rgba(255,255,255,0.76)
SHAPES:
- None. A rule and a coastline motif were both tried here and both read as noise.
EXPORT: {POST}S05@2x.png
```


```
FRAME: Base / Detail Spread (two-image)
CANVAS: 1080 x 1350
BACKGROUND: #f5f7f9
GRID: 112px side margins · 32px inner gutter · two 412px columns
LAYER STACK:
1. Primary image or slot — 856 x 700 at x112 y52
2. Row at y776, height 340:
   a. Secondary image or slot — 412 x 340, left
   b. Caption column — 412px wide, right: headline then body
3. Footer row — counter left, colour logo right
TEXT:
- Headline | 46px Light | 1.14 | #16242e | caption column only
- Body | 28px Regular | 1.45 | rgba(22,36,46,0.78)
IMAGE:
- Primary landscape 856 x 700 (≈1.22:1) · Secondary square-ish 412 x 340
SHAPES:
- None. Square corners, no radius, no shadow.
EXPORT: {POST}S{NN}@2x.png
```

**Slot system.** Any image position accepts a marked placeholder instead of a photograph:
a hatched field carrying the shot name and the exact crop required. It is never a stand-in
image — it states what is missing, so a slide can be laid out and approved before the shoot.
Swap `label`/`note` for `photo`/`focus` in `build.py` when the file arrives.

## E. Content / asset requirements

**Held now** — 13 processed images in `canvas/`: Ladds Ridge crew, Mondaro frame, Chambers
Lane façade, 32 Garden Grove interiors, under-house living conversion, rear dwelling, pool,
architectural drawings, plus both logo masters.

**Required, not held:**

| Asset | Qty | Format | Framing |
|---|---:|---|---|
| Portrait hero stills | 6–10 | RAW + JPEG | **Vertical 4:5 or taller.** Landscape files fail the hero crop. |
| Portrait of Rob | 1–2 | JPEG | On site, good light. Blocks Post 11 entirely. |
| Secondary-dwelling hero | 2–3 | JPEG | Weakest subject in the set. |
| Slab / early-stage stills | 8–12 | RAW + JPEG | Set-out, reinforcement, pour. Needed for any slab carousel. |
| Project metadata sheet | 1 | Text/CSV | Project, suburb, stage, scope, handover date, permission status |
| Logo | 2 | **SVG** | We only hold PNG; the wordmark softens at 200px |

**Site capture prompts:** shoot vertical as the default, not as an afterthought. Leave clean
negative space in the lower third of every hero candidate — that is where type lands. Capture
craft evidence (set-out, alignment, fixing, finishes) and people in real work, not posed.
Collect trade credits on the day.

## F. Original copy package

All slide copy, captions, CTAs, hashtags and per-post approval notes live in the `POSTS`
structure in `canvas/build.py` — one source of truth, so the spec and the artboards cannot drift.

Standing rules: Australian English · no cost, timeline, approval or compliance guarantees ·
"20 years" is Rob personally, never the company · never publish the builds-per-year figure ·
no aphorisms (rejected July) and no colloquialism (rejected September).

## G. Quality check

- [x] Client-owned assets only — every photograph is a real Coast Life project
- [x] No AI-generated homes, rooms or site scenes anywhere
- [x] Legible at phone size — body floor 34px
- [x] One message per frame
- [x] Consistent tokens across all 49 artboards, generated from one definition
- [x] Original CTA on every carousel
- [x] Slide counter no longer wraps in PNG export
- [ ] **Princess Street images excluded** — five files on their site credit Owen Architecture
      and Simon Devitt. Unresolved; never use.
- [ ] Verbatim review wording and written permission — Post 5
- [ ] Service-area list confirmed — Post 8
- [ ] Warranty wording confirmed current for 2026 — Post 2
- [ ] Which service each photograph actually belongs to
