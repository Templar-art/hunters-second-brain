---
type: source
tags: [oneill, branding, brand-book, colour, typography, signage, print, photography, deliverable]
status: shipped
updated: 2026-08-26
---

# O'Neill Property — Brand Book, Edition One

The identity manual 10x prepared for O'Neill Property. Twenty-three A4-landscape spreads in one self-contained HTML file that reads as a bound book on desktop, unbinds into a single-column reading view under 1024px, and prints one spread to a sheet.

Deliverable: [oneill-property-brand-book.html](../../projects/oneill-brand-book/oneill-property-brand-book.html). Source document that this revision was built from: `~/Downloads/O'Neill Property - Brand Book.html` (edition zero, 18 spreads).

## ⚠️ Supersedes the earlier brief

[[oneill-group]] recorded the working design direction as 10x's own palette (#61a8d8, Poppins/Montserrat) pending a brand lock. **The identity has landed and it is nothing like that.** Two further corrections:

- The trading name is **O'Neill Property**, not O'Neill Group. `oneillgroup.com.au` is the retired name and still appears on the printed business card and photo board.
- The type system is **Sinhala MN + Inter**, not Poppins/Montserrat. See [[typography]].

## The palette

Four values, no fifth. Sage Grey is the field, not an accent — roughly half of everything the brand makes.

| Role | Name | Hex | RGB | Share |
|---|---|---|---|---|
| Signature field | Sage Grey | `#B7C1B3` | 183 193 179 | 50% |
| Anchor, all type | Basalt | `#3A3A3A` | 58 58 58 | 30% |
| Neutral ground | Stone | `#E2DAD1` | 226 218 209 | 15% |
| Graphic detail only | Deep Sage | `#839C83` | 131 156 131 | 5% |

**The sage rule: no sage in this palette carries body copy** — not Sage Grey, not Deep Sage, at any size or weight. Text is Basalt, or it sits on Basalt.

Measured contrast (verified, not estimated): Sage Grey on Basalt 6.1:1 · Basalt on Stone 8.2:1 · Stone on Basalt 8.2:1 · Basalt on Sage Grey 6.1:1 · Deep Sage on Stone 2.2:1 (graphic only) · Stone on Sage Grey 1.3:1 (graphic only).

## Type

- **Display:** Sinhala MN, one weight, never below 18px. Apple-only — a substitute is still unnominated.
- **Text:** Inter 300/400/500/600. Nothing heavier. Measure ~65 characters, never justified, never hyphenated, never tracked.
- Two families, never a third. One display size per layout.

## Logo

Three lockups: primary (wordmark over PROPERTY), secondary (wordmark alone), icon (O/N monogram). Clear space on all four sides is the cap height of the O. Minimums: primary 40 mm / 150 px, secondary 28 mm / 110 px, icon 8 mm / 32 px. Four colourways, chosen by ground contrast.

## Campaign language

Own It (for sale) · Preparing It (coming soon) · Lease It (for lease) · Achieved (sold). One campaign word per piece, with the plain status word beside it wherever status must be instant — legally or from the footpath. Property Management and Property Appraisal stay plain: they are searched for by name.

## Production

Uncoated always — 350 gsm cards, 170 flyers. Stone specified as the paper, not printed as an ink. Rich black for any large Basalt field. No foil, spot gloss, bevel, gradient or metallic anywhere.

## Photography

Natural light, corrected verticals, honest colour, restrained styling. No composited skies, no filters or vignettes, no stock house that is not the house. No type across a frame: it goes on a solid Basalt, Sage Grey or Stone panel beside the picture, or on a scrim measured against the actual pixels to 4.5:1.

The four frames in the book are from the 37 Southaven shoot, served from `oneill.group.10xvisuals.co`. Captions are deliberately neutral — the book makes no claims about a property it is not selling.

## Open items carried into Edition One

Spread 22 of the book is the authority; summary here so it is findable from the wiki:

1. **Basalt on the website** — artwork is `#3A3A3A`, the site ships `#2D2D2D`. Decided in favour of the artwork, not yet shipped. Any scrim measured against the old value has to be taken again.
2. **Display face substitute** — unnominated for Windows, Android and non-embedding printers.
3. **Pantone, paint and CMYK** — none selected; no CMYK build published, printer sets and proofs one.
4. **Retired domain** — `oneillgroup.com.au` still on the card and photo board; out at the next print run and off the site at the same time.
5. **App icon colourway** — Stone on Basalt and Sage Grey on Basalt are both nominated. Contradiction to resolve.
6. **Scrim ratios** — measured per frame but recorded in the website page files, not in the book.

Production dependency: the four collateral photographs on spreads 15 and 16 load from `./brand-book-assets/`. That folder was not shipped with the source file and is not in the repo — the frames fall back to labelled placeholders without it.

## Related
- [[oneill-group]] — the client page
- [[typography]] — type systems across 10x work
- [[real-estate-design-refs]] — the pattern research that fed the site brief
- [[brand-system]] — 10x's own system, which this brand deliberately does not use
