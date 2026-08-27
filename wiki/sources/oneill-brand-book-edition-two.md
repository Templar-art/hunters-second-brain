---
type: source
tags: [oneill, branding, brand-book, colour, typography, signage, print, photography, deliverable]
status: draft-pending-client-decisions
updated: 2026-08-27
---

# O'Neill Property — Brand Guidelines, Edition Two

The condensed rewrite of [[oneill-brand-book-edition-one]]. Edition One's 26 spreads become 13; section dividers, repeated scene-setting copy and duplicated explanations are cut, and every rule a designer, printer, developer or agent actually needs to check work against is kept.

Content was written and locked by Hunter before design started — 10x's job on this edition was visual design and layout only, no copy changes. Verified verbatim against the source draft after build: the only text removed anywhere was scaffolding 10x had added itself (see *Design decisions* below).

Deliverables:
- Print PDF, 13 pages, 423×299 mm (A3 landscape): [oneill-property-brand-guidelines-edition-two.pdf](../../projects/oneill-brand-book-edition-two/oneill-property-brand-guidelines-edition-two.pdf)
- Editable canvas (13 artboards, Claude Design preview): [oneill-property-brand-guidelines-canvas.html](../../projects/oneill-brand-book-edition-two/oneill-property-brand-guidelines-canvas.html)
- Artboard source + assets: `projects/oneill-brand-book-edition-two/src/`
- Frozen source content: [source-content-draft-edition-two.pdf](../../projects/oneill-brand-book-edition-two/source-content-draft-edition-two.pdf)

## Format

Landscape 1600×1131 px per page, authored at 96 px/inch. The height was set deliberately: 1600/1131 = 1.4152, so the sheet drops onto A3 or A4 landscape (√2 = 1.4142) without letterboxing. Edition One was A4-landscape HTML spreads that reflowed responsively; Edition Two is fixed print artboards, one page per sheet.

## The type system, as actually built

Edition Two sets itself in the scale it publishes on page 6 — Edition One did not. Eight sizes total, every one a published brand step:

| Step | px | Role |
|---|---|---|
| display | 132 | cover only |
| title | 44 | page titles (published Heading step) |
| subhead | 28 | in-page subheads, the winning voice quote |
| lede | 19 | page ledes, section heads (published Body large) |
| body | 16 | all running text |
| caption | 12 | annotations, table secondary cells |
| label | 11 | masthead, eyebrow labels, all-caps |

Weights are 300/400/500/600 only — the spec says "nothing heavier" than 600, so no 700 appears anywhere. Body leading is 16/1.6 rather than the published 16/1.75, because the book sets multi-column measures and leading scales inversely with line length. **That single deviation is unapproved** — confirm or revert.

Page 6's specimens render the exact values their labels claim (64/44/28/19/16/12/11). Worth stating because Edition Two's first build did not: it labelled samples 64/44/28 while rendering 60/42/27.

### Display-face substitute — nominated, awaiting sign-off

Edition One left this open (its open item 2) and the Edition Two content still lists it as open decision 3. 10x's nomination, measured rather than guessed:

**Antic Didone** (SIL OFL, Google Fonts → covers Windows, Android and web). Sinhala MN measured at 64 px: advance 611 px, cap 41.4, x-height 32.6 (x/cap **0.787**, the largest of every candidate tested), ascender 57, descender 18 — so its Latin is not a Didone by proportion but a wide Scotch Roman.

| Candidate | Δ advance | x/cap | Note |
|---|---|---|---|
| **Antic Didone** | −6.2% | 0.721 | nominated — high contrast, restrained, ships one weight (matches the brand's own one-weight display rule) |
| Prata | +1.6% | 0.658 | best width match, but small x-height lets caps dominate |
| Bodoni Moda | −3.4% | 0.627 | renders much larger at the same px |
| Rosarivo | −0.7% | 0.700 | excellent metrics, wrong voice (warm oldstyle, low contrast) |
| Source Serif 4 | −14.1% | 0.692 | too narrow |

The CSS stack is `'Sinhala MN', 'Antic Didone', 'ONP Display Fallback', Georgia, serif`, where `ONP Display Fallback` pins local Georgia to Sinhala MN's measured metrics so line breaks do not move between platforms:

```css
@font-face{ font-family:'ONP Display Fallback'; src:local('Georgia');
  size-adjust:107.4%; ascent-override:89%; descent-override:28%; }
```

Verified: the pinned fallback renders 611 px against Sinhala MN's 611 px (raw Georgia is 569, −6.9%).

**Inter is served as a webfont in every artboard.** It is not installed on Hunter's Mac, so the first PDF silently set the whole book in Helvetica Neue. The shipped PDF embeds real Sinhala MN plus Inter 300/400/500/600 subsets.

## The mark — an asset gap that is still open

The content specifies three lockups. **Only two exist.** Measured aspect ratios of the supplied files:

- `basalt-logo.png` / `white-logo.png` — 2.31 — primary (wordmark over PROPERTY)
- `stone-logo.png` — 2.56 — primary, Stone
- `icon-basalt.png` / `white-logo-alt.png` — 1.19 — the O′N icon. **`white-logo-alt.png` is the icon in white, not a wordmark**, despite being supplied labelled as a wordmark export.

There is no wordmark-only (secondary) artwork. The first build faked it by CSS-cropping the primary, which mutilated the letterforms and broke the book's own rule ("never crop, box or draw a rule around it") on the secondary demo *and* on the running masthead of all 12 interior pages. Both are fixed: the masthead now uses the intact icon at 34 px (clears the 32 px minimum, with clear space well beyond the O's cap height), and page 4's secondary slot holds a dashed "Artwork to be supplied" placeholder rather than a crop.

**Action on the client: supply the wordmark-only SVG,** or the content's "three lockups, no fourth" ships showing two.

## Design decisions worth recording

- **Sage bookends, Stone interior, one Basalt page.** Cover and closing page are Sage Grey (the brand's "signature field"); reading pages are Stone (its stated long-reading role); page 11 (Website and digital) is full Basalt, the one dark page, because it is the section describing dark grounds and night photography.
- **Icon as running mark.** The brand permits the icon "anywhere the full name already appears nearby" — a masthead is exactly that case. The masthead rule was removed on every page, because a rule sitting under the mark enters its clear space, which the book forbids.
- **One grid break in 13 pages.** Page 10 (Photography) bleeds three 37 Southaven frames full-width off the top edge, with the running head, title and lede below the image. Its own rule is that the property is the hero. Nothing else in the book leaves the 96 px margin.
- **Voice reads as an argument, not a comparison.** The on-brand line is 28 px across an 800 px measure; the off-brand line is 16 px, struck through, offset down in a 424 px column.
- **Scaffolding removed.** The build initially carried a "SECTION 0X" eyebrow on 10 pages plus a second numbering in the masthead — kicker-as-grammar and numbered-markers-on-non-sequences, the same two tells the [[oneill-group]] site critique flagged in August. One numbering system survives, in the masthead, justified because the content genuinely orders its sections 1–10 with a contents page pointing at them.
- **No side-stripe accents.** Four `border-left:2px` coloured stripes (Voice quotes, Brand flag note, Website fix panels) were rewritten with different structure — hairline rule above, or full hairline plus tint panel.
- **8 px vertical grid.** Every page-level block lands on it; 36 arbitrary block positions became zero off-grid.

## Verified, not assumed

All 13 pages measured in-browser at 1600×1131: zero WCAG failures, zero text below 11 px, zero frame overflow, zero clipped boxes, zero collisions between page-level blocks at 0 px tolerance, zero broken images.

Contrast is worth spelling out because the four-value palette has no tint ramp, and using `opacity` as a stand-in for one produced real failures (worst: 2.76:1 on the word-book's "instead of" column). Minimum alpha for 4.5:1, computed from the master hexes:

- Basalt on Stone — full 8.22:1, needs **≥0.76**
- Basalt on Sage Grey — full 6.12:1, needs **≥0.86**
- Stone on Basalt — full 8.22:1, needs **≥0.66**

The book uses 0.78 / 0.88 / 0.70. The six ratios the source prints on page 5 were independently checked and all hold.

## Open decisions carried into Edition Two

Page 13 is the authority. Nothing in the book should be treated as final until these are resolved:

1. **Service area** — Northern Gold Coast, or Gold Coast-wide? Edition One says Northern; an earlier working direction said wide. Affects audience copy, SEO and image selection.
2. **Sold copy** — this draft applies "Sold It". Confirm over Edition One's "Achieved".
3. **Non-Apple display font** — 10x nominates Antic Didone (above). Needs sign-off.
4. **App/social icon finish** — Stone on Basalt, or Sage Grey on Basalt. Carried unresolved from Edition One's open item 5.

Still outstanding from Edition One and *not* covered by the Edition Two content: Pantone/paint/CMYK builds (none selected), and the site still shipping Basalt as `#2D2D2D` against artwork `#3A3A3A` (the book states the fix on page 11; shipping it is a website job).

## Known limits of the deliverable

- **PNG/PDF export from the canvas cannot embed Google Fonts** — exported pages fall back to the metric-pinned Georgia. This is why the metric override exists. The committed PDF was rendered through headless Chrome on a Mac with Sinhala MN installed, so it carries the real face; regenerating it on a machine without Sinhala MN will produce Antic Didone instead.
- **Page 4 (The mark) is airless** — 9 px of slack against the footer, the densest page in the book. It carries three lockups, clear space, four colourways and six misuse rules. The structural fix is splitting it across a spread; the brief allowed 13–16 pages.
- Body leading deviates from the published table (see *The type system*).

## Related
- [[oneill-brand-book-edition-one]] — the edition this condenses
- [[oneill-group]] — the client page
- [[typography]] — type systems across 10x work
- [[brand-system]] — 10x's own system, which this brand deliberately does not use
