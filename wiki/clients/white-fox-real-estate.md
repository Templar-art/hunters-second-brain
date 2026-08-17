---
type: client
tags: [real-estate, website, new-client]
status: active
updated: 2026-08-17
---

# White Fox Real Estate

New client. Website build.

## Brief
- **Aesthetic:** old money, minimal, architectural.
- **Studio intro animation:** letters start in a corner, animate up to top-middle (like a signature reveal). Intro only, not repeated per-page.
- **Coastal Team page:** team page only, distinct treatment from rest of site.
- **Goal statement:** "Luxury for everyone. Property is personal." Families over mansions — premium experience regardless of property price point. Every client (whatever budget) gets the best experience, best deals, best service.

## Reference sites (inspiration/pattern only, not to copy)
- https://www.era-residence.com/
- https://horizonte-village.com/
- https://www.eleos.la/
- https://www.awwwards.com/inspiration/footer-studiofmrg (footer)
- https://horizonestatebali.com/ (footer)
- https://minaleandmann.com/
- https://www.makearchitects.com/

## Pattern research (2026-08-17)
- **era-residence.com** — dark oxblood title-card intro (serif wordmark + script location, held before scroll-unlock) → sky-blue hero, oversized staggered serif headline, numbered chapter index (00/00) down the side, small-caps tracked nav. Old-money serif/sans contrast, drone photography.
- **horizonte-village.com** — hero forces a binary choice (villas/residences), photos masked into torn organic shapes, warm stone-neutral bg. Useful if we ever split audiences.
- **eleos.la** — line-sketch illustration instead of photo, all-caps tracked sans, plain metadata rows for listings — restraint-as-luxury register.
- **Awwwards footer (StudioFMRG)** — footer as full-bleed image "poster," oversized outline nav words overlaid on photography.
- **horizonestatebali.com footer** — multi-column footer organized by property-type taxonomy, doubling as secondary nav/search.
- **minaleandmann.com** — hard color-block wipe transition on load (geometric panel reveal, not fade) — closest existing intro device across all refs.
- **makearchitects.com** — editorial/blog-forward homepage (Featured + Thinking grid), tag pills, minimal bottom-bar cookie notice, studio locations in footer for credibility.
- **Studio intro:** none of the refs do a literal "letters corner → top-middle" animation. era-residence's held title-card and minale+mann's block wipe are the closest analogs — this intro is a novel build for White Fox, not an adaptation.

## UX/design audit (2026-08-17)
Honest verdicts, desktop + mobile (375px) tested via browser.

- **era-residence.com — mediocre.** Clean hierarchy, nice serif/script logo pairing, but **mobile hero is broken** (content confined to a ~155px column, dead space on the right). Numbered "three reasons" filler section. Steal the sub-brand script-under-serif logotype; avoid shipping without real breakpoint testing.
- **horizonte-village.com — bad.** Forces a Villas/Residences choice before showing anything. **Contrast failure** on the gate screen (gray-brown text on beige map bg). Mobile gate cards break (jagged crop, dead space). Forced "LOADING 100%" preloader stalls on mobile. Avoid all of this — gate screens, sub-4.5:1 text, forced waits.
- **eleos.la — genuinely good, closest model for White Fox.** Textbook hierarchy (wordmark → mission → three concretely-named pillars, not "01/02/03" filler → project cards → CTA). Strong contrast throughout, sane type scale, no gratuitous card grids or eyebrow labels, no preloader. Steal: naming differentiators as real nouns instead of numbering them.
- **Awwwards footer (StudioFMRG) — good pattern only.** Circular badge logo overlapping the footer's top rule line is a strong architectural-luxury device — a "White Fox" crest could do the same. Not a real-estate site itself, ignore its playful link-naming voice. (Also: awwwards.com's own cookie modal blocked its hero on load — live example of the anti-pattern to avoid.)
- **horizonestatebali.com — bad, wrong register anyway.** Generic listing-portal look, not luxury. **Two confirmed responsive bugs**: a two-column section clips text off-screen on mobile, and footer text collides ("sales@horizonestatebali" runs into "About us") on both desktop and mobile. Nothing design-wise worth keeping.
- **minaleandmann.com — mediocre.** Six services cards repeat an identical eyebrow-label→name→one-liner formula — the "identical card + tiny tracked eyebrow" anti-pattern, reads templated not bespoke. Tasteful restrained type otherwise. Steal the short recurring strapline ("Design Matters") as a repeated ethos anchor; avoid the repetitive card scaffold.
- **makearchitects.com — mediocre.** Homepage hierarchy miss — leads with a blog/"Thinking" feed instead of actual project work; for White Fox, listings/projects must outrank articles. Comma-tag lists on posts read noisy. Steal the plain multi-office footer (legible scale/credibility signal, no decoration).

**Cross-site takeaway:** eleos.la is the strongest structural model. Avoid gate screens, forced preloaders, low-contrast text-on-texture, and repetitive eyebrow-labeled card grids. QA every breakpoint — 2 of 7 sites had real, reproducible mobile bugs.

## Broader web sweep — additional candidates (2026-08-17)
Wider search for UK/US/int'l old-money-minimal-architectural real estate sites, filtered down to genuine survivors.

**Survivors:**
- **inigo.com** — UK, historic homes (from The Modern House team). Full-bleed warm interior photo + italic serif headline, magazine-spread feel. Tracked serif wordmark. Genuinely old-money, not corporate. **Strong reference.**
- **themodernhouse.com** — UK, architect-designed/Modernist homes; arguably the category-defining "quiet luxury real estate" site. Near-zero UI chrome, editorial tone, journal+listings share one visual language. **Strong reference.**
- **niallmclaughlin.com** — UK architecture firm (crossover ref). Plain black sans wordmark, single photo, no hero gimmicks — confidence through restraint.
- **carusostjohn.com** — UK architecture firm. Stark black-on-white headline, documentary (not staged) photography, reads as portfolio not sales funnel — good study in how little "selling language" a confident brand needs.
- **gingermartin.com** — Napa/Sonoma boutique brokerage (WSJ Top 100 agent). Serif logo + bold grotesque headline pairing, stone/glass architecture photography. More conventional structure than Inigo but restraint keeps it from tipping shiny.
- **luxury-places.ch** — Swiss brokerage (Lake Geneva/Alps), est. 2006, real operating agency. Restrained circular monogram loading state; property collections as a numbered index (01 Waterfront / 02 Historic / etc, a real sequence — not filler); in-house editorial "Journal." *Note: WebGL/animation-heavy, verify visually before leaning on it.*
- **elyse-residence-dev.webflow.io** — designer showcase (Awwwards Honorable Mention), not a live brokerage, but clean pattern ref: twilight photography, no text on first load, near-monochrome charcoal palette.
- **domusnova.com** — Notting Hill boutique (architect-designed London homes, now w/ Barnes Int'l), also active in Ibiza. *Caveat: bot-gated in testing, only partially verified.* Wide-tracked all-caps serif/sans wordmark, plain white nav. Interesting "two very different property registers, one brand voice" case (London townhouses + Ibiza villas).

**Discarded (checked, rejected):**
- villagesite.com — decent photography/logo but floating teal chat bubble widgets read as generic template.
- dahlercompany.com — orange sticky CTA bar, corporate mainstream brokerage chrome.
- bestofluxuryrealty.com — generic MLS aggregator, not a design reference.
- watt.framer.website — generic property-management look (blue gradient hero, navy corporate logo).
- berdanrealestate.com, hodararealestate.com — inaccessible/parked, dropped without guessing.

**Gallery note:** awwwards.com/websites/real-estate/ and the CSS Design Awards real-estate gallery list ~20+ cards each but need individual opening to get live URLs (no direct outbound links on the collection page) — only partially swept. Worth a follow-up pass if we want to exhaust them.

## Status
Brief captured 2026-08-17. Ref-site pattern research + UX audit + broader web sweep done — see above. **inigo.com and themodernhouse.com are the two strongest references found so far** — closer to the old-money/architectural/editorial brief than any of the original 7. Next: concept direction / wireframe.
