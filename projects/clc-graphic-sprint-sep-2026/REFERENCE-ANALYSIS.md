# A. Reference structure analysis

Reference: a public @barlowbuilding carousel, 6 Aug 2026, plus a sweep of their recent grid.
Studied live, measured off the source files by pixel-scanning each canvas.

**Nothing from the reference is used in the output** — no mark, typeface, colour value,
photograph, caption or project name. What follows is layout mechanics only.

---

## Measured structure

Canvas **2160 × 2880 → 1080 × 1440. That is 3:4, not 4:5.** Recent grid confirms it: 1080×1440
dominates, with some 1:1. They have moved to Instagram's taller portrait and are taking the
extra ~90px of feed height.

Vertical bands, measured down the centre column as fractions of canvas height:

| Band | Top | Bottom | Height @1440 | Width (frac) |
|---|---|---|---|---|
| Brand mark | 0.111 | 0.176 | 94px | 0.176 → 0.813 |
| Image | 0.275 | 0.758 | 696px | 0.206 → 0.794 |
| Caption line 1 | 0.860 | 0.874 | 20px | 0.200 → 0.802 |
| Caption line 2 | 0.876 | 0.892 | 22px | 0.201 → 0.789 |

**The rhythm is the point.** Gaps: 160px above the mark, 143px mark→image, 147px image→caption,
156px caption→edge. Four near-equal intervals. Nothing is optically centred by eye; the whole
composition is a set of even rests.

Image is 636 × 696 — **near-square (0.91), floating, with 20.6% side margins.** It is not
full-bleed and it is not a full-width panel. The generous surround is what makes it read as a
plate rather than a post.

## The mechanism that actually does the work

**The ground colour changes per post, sampled from that post's own photograph.**

Measured grounds across recent posts: `#ada79b` greige · `#3d4d42` deep green · `#788097`
blue-grey · `#6c7079` slate · `#8e7b5a` tan · `#b1b1b1` grey · `#222931` near-black. Every one
is desaturated and held to a mid value. The brand mark and caption are a high-value, low-chroma
tint of that same hue.

That is why the grid reads as one book despite wildly different subject matter — each tile is
monochrome-matched to its own image, and the whole feed sits in one tonal register. It is a
production rule, not a palette, which makes it fully transferable.

## Hierarchy

Brand first, image second, caption third — **the inverse of a conventional feed post**, where
the image leads and the logo is a small corner mark. Consequences:

- No headline. The caption is small, tracked, all-caps, centred, two lines, low contrast.
- No slide numbers, no eyebrows, no rules, no counters, no CTA slide.
- Within a carousel every slide is identical except the photograph and the caption line.
- The post is a plate in a series, not a slide in a deck.

## Generic mechanisms — safe to translate

Fixed inset image window · even vertical rhythm · brand mark as the top element · tracked
lower-caption · ground tone derived from the image · one ground per post · identical slide
template across a carousel · named-project highlight archive.

## Must NOT be copied — and are not

The BARLOW wordmark and its "B." monogram · their typeface · `#ada79b` and every other measured
ground value · their photography · their caption wording and voice · their project names
(NAMIYA, Alchemy, AXL, Mexicali, Kokomo, Aruma) · their sub-account structure.

---

# B. Translation to Coast Life

Same mechanics, entirely Coast Life's own expression.

| Mechanism | Reference | Coast Life |
|---|---|---|
| Canvas | 3:4 | **3:4, 1080 × 1440** — adopted |
| Top mark | Wordmark, tone-on-tone | **Coast Life white master**, 340px, 90% opacity |
| Image window | 636 × 696 inset | **636 × 696 at y396** — same proportions |
| Ground | Sampled from photo | **Sampled from Coast Life's own photo**, hue held, saturation clamped 0.06–0.16, lightness pulled to 0.50–0.64 |
| Caption | Tracked caps, 2 lines | **23px Poppins Medium, +0.15em, centred** |
| Typeface | Theirs | **Poppins** — already Coast Life's |
| Close slide | — | **Type plate**: statement in the image band, meta beneath. Our addition; the reference has no CTA slide. |
| Rhythm | ~150px intervals | 150 / 126 / 146 / 150 |

Grounds now computed from Coast Life photography come out cool grey-blue, sage, tan and warm
grey — which sits naturally with the navy-and-blue identity rather than fighting it.

**What was dropped from the previous build:** full-bleed heroes, the off-white framed slides,
navy punctuation slides, kickers, slide counters, section rules, the 4:5 canvas. The plate
system replaces all of it. The prior 4:5 build is preserved at `canvas/build-4x5.py.bak`.

**Retained regardless of the reference:** no AI-generated homes · real projects or a marked slot
· no cost, timeline, approval or compliance claims · Princess Street images excluded.
