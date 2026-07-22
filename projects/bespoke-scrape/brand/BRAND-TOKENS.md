# Bespoke Estate Agents — Brand Tokens (authoritative)

Source: `Bespoke-Brand-Guide-v1.0.html` + `Bespoke-Social-Strategy.pdf` (10x Visuals deliverables).
**This supersedes the colours/fonts guessed from the scraped live site.**

Principal agent: **Jason Ward** (the face/awareness engine). Bespoke = delivery mechanism.
Positioning: boutique, people-first, Gold Coast prestige residential. "Beyond Luxury Real Estate." Quiet confidence, not flash.

## Colour (CSS vars)
```css
--be-green:      #132a24; /* PRIMARY — hero, nav, dark sections */
--be-green-light:#152f2a; /* secondary dark */
--be-white:      #FFFFFF;
--be-off-white:  #F0EDE8; /* warm light section bg (grey-100) */
--be-grey-200:   #E2DDD7; /* cards, dividers */
--be-grey-300:   #C8C2BB; /* borders, lines */
--be-grey-600:   #7A7470; /* secondary text, captions */
--be-charcoal:   #2A2A2A; /* body text on light */
```
Rule: green dominates dark sections; white dominates light. Two greens for subtle depth, never in the same component. Charcoal = only body-text colour on light. No third-party/accent colours (gold, terracotta, navy) unless approved.

## Type
- **Headings:** `Zodiak` Light **300** (Regular 400 only when thin fails at small size). Fallback: Georgia, serif. NEVER 700+ on Zodiak.
- **Body/UI:** `Poppins` — Regular 400 body, Medium 500 UI/nav/captions, Semibold 600 CTAs.
- Scale: H1 56/1.1 (-0.5px) · H2 32/1.2 · H3 20/1.3 · Body 16/1.8 · Caption 14/1.6.

## Spacing / layout (8px base)
`--be-space` xs4 sm8 md16 lg24 xl32 2xl48 3xl64 4xl96.
Max width 1280px · prose 760px · gutter 32 desktop / 20 mobile · section vertical padding min 64 desktop (never <48).

## Components
- **Buttons:** Poppins Medium 500, radius 4px. Primary = green bg / white text, hover darkens 10% → `#0d1f1a`. Outline, Ghost, Light (on dark), Outline-Light variants. Action-led labels ("Book an Appraisal", "View Listings"), no vague CTAs.
- **Cards:** 1px solid `#E2DDD7`, radius 8px, padding 32px. Hover: border → `#132a24` + shadow `0 4px 16px rgba(19,42,36,0.10)`. Card bg only white or `#F0EDE8`. Side-by-side CTAs match width.
- Tokens: `--be-radius-md 4px`, `--be-radius-lg 8px`, `--be-shadow-md 0 4px 16px rgba(19,42,36,0.10)`.

## Photography / video
Natural light, warm/neutral temp, candid-leaning, Gold Coast lifestyle, Jason in most content. No stiff headshots, no heavy filters, no stock. Video: hook in 2s, value by 5s; Reels 9:16, web 16:9. Grade: warm shadows, lifted blacks, clean highlights, slight green tint in shadows.

## Copy voice (for all site text)
Relatable, connectable, informative, expert, grounded. Speak to the person not the property. Lead with insight. Plain language, first person (Jason) for organic. **NO em dashes** (use commas/colons/short sentences). No boastful/corporate/clickbait. No vague superlatives.
Content pillars: Authority · Connection · Visibility · Proof.

## Logos on hand
- `official-logos-from-guide/logo-*.png` — official Bespoke Estate Agents icon + wordmark (white, transparent bg) extracted from guide.
- Scraped vectors in `../assets/.../*.svg` (from live site) + `logos/`, `icons/`.
- ⚠️ MISSING: **Zodiak font files** — not embedded anywhere. Needed to host headings in the real brand face (else Georgia fallback).
