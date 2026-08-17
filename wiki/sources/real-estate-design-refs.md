---
type: source
tags: [real-estate, design-research, reference]
updated: 2026-08-17
---

# Real Estate Website Design References

General pattern/UX research across luxury and boutique real-estate sites — not tied to one client. Currently feeding [[oneill-group]] (structural base is the real WHITEFOX Gold Coast site, kept separate below).

⚠️ Originally mis-filed as a "White Fox Real Estate" client page — WhiteFox (goldcoast.whitefoxrealestate.com.au) is a **real existing Gold Coast agency**, not our client. It's the structural/UX reference for [[oneill-group]]'s rebrand build. Corrected 2026-08-17.

## Original 7 reference sites
era-residence.com, horizonte-village.com, eleos.la, awwwards footer-studiofmrg, horizonestatebali.com, minaleandmann.com, makearchitects.com

## Pattern research
- **era-residence.com** — dark oxblood title-card intro (serif wordmark + script location, held before scroll-unlock) → sky-blue hero, oversized staggered serif headline, numbered chapter index (00/00) down the side, small-caps tracked nav. Old-money serif/sans contrast, drone photography.
- **horizonte-village.com** — hero forces a binary choice (villas/residences), photos masked into torn organic shapes, warm stone-neutral bg.
- **eleos.la** — line-sketch illustration instead of photo, all-caps tracked sans, plain metadata rows for listings — restraint-as-luxury register.
- **Awwwards footer (StudioFMRG)** — footer as full-bleed image "poster," oversized outline nav words overlaid on photography.
- **horizonestatebali.com footer** — multi-column footer organized by property-type taxonomy, doubling as secondary nav/search.
- **minaleandmann.com** — hard color-block wipe transition on load (geometric panel reveal, not fade).
- **makearchitects.com** — editorial/blog-forward homepage (Featured + Thinking grid), tag pills, minimal bottom-bar cookie notice, studio locations in footer for credibility.

## UX/design audit (honest verdicts, desktop + mobile 375px tested)
- **era-residence.com — mediocre.** Clean hierarchy, nice serif/script logo pairing, but **mobile hero is broken** (content confined to a ~155px column, dead space on the right). Numbered "three reasons" filler section.
- **horizonte-village.com — bad.** Forces a Villas/Residences choice before showing anything. **Contrast failure** on the gate screen. Mobile gate cards break. Forced "LOADING 100%" preloader stalls on mobile.
- **eleos.la — genuinely good.** Textbook hierarchy (wordmark → mission → three concretely-named pillars, not "01/02/03" filler → project cards → CTA). Strong contrast throughout, sane type scale, no gratuitous card grids or eyebrow labels, no preloader.
- **Awwwards footer (StudioFMRG) — good pattern only.** Circular badge logo overlapping the footer's top rule line is a strong architectural-luxury device.
- **horizonestatebali.com — bad, wrong register.** Generic listing-portal look. **Two confirmed responsive bugs**: clipped column text on mobile, footer text collision.
- **minaleandmann.com — mediocre.** Six services cards repeat an identical eyebrow-label→name→one-liner formula — templated, not bespoke.
- **makearchitects.com — mediocre.** Homepage hierarchy miss — leads with blog/"Thinking" feed instead of project work.

**Cross-site takeaway:** eleos.la is the strongest structural model. Avoid gate screens, forced preloaders, low-contrast text-on-texture, repetitive eyebrow-labeled card grids. QA every breakpoint — 2 of 7 sites had real, reproducible mobile bugs.

## Broader web sweep — additional candidates
- **inigo.com** — UK, historic homes. Full-bleed warm interior photo + italic serif headline, magazine-spread feel. **Strong reference.**
- **themodernhouse.com** — UK, architect-designed homes; category-defining "quiet luxury real estate" site. Near-zero UI chrome, editorial tone. **Strong reference.**
- **niallmclaughlin.com** — UK architecture firm crossover. Plain black sans wordmark, single photo, confidence through restraint.
- **carusostjohn.com** — UK architecture firm. Stark black-on-white headline, documentary photography, reads as portfolio not sales funnel.
- **gingermartin.com** — Napa/Sonoma boutique brokerage. Serif logo + bold grotesque headline pairing.
- **luxury-places.ch** — Swiss brokerage. Property collections as a named/numbered index (01 Waterfront / 02 Historic — a real sequence, not filler). *WebGL-heavy, verify visually.*
- **elyse-residence-dev.webflow.io** — designer showcase, not a live brokerage. Twilight photography, no text on first load, near-monochrome charcoal.
- **domusnova.com** — Notting Hill boutique. *Bot-gated in testing, only partially verified.* Wide-tracked all-caps serif/sans wordmark.

**Discarded:** villagesite.com (chat bubble widgets), dahlercompany.com (orange sticky CTA, corporate), bestofluxuryrealty.com (generic MLS aggregator), watt.framer.website (generic property-mgmt look), berdanrealestate.com / hodararealestate.com (inaccessible/parked).

## Warmer/family-personal course-correct
First pass (inigo/themodernhouse) read too architectural/cold for a family-personal brief. Warmer survivors found:
- **corcoran.com** (US) — brand promise stated in plain warm language ("Make yourself at home"), Agents/Offices as top-level nav.
- **livingroomre.com** (US, Portland) — domestic tagline + mark, single warm accent color used sparingly, "Meet Our Agents" equal-weight CTA to listings.
- **featherstoneleigh.co.uk** (UK) — lived-in living-room hero photo, names actual leadership on the homepage.
- **schranerrealty.com** (US, Boise) — "feels like family" headline, husband-and-wife team framing, handwritten script accents.
- **fineandcountry.co.uk** (UK) — real people mid-interaction in hero imagery, traditional-premium repositioned warm.
- **bellisrealtygroup.com** (US) — hyper-local/community framing, warm-toned real interior photography.
- **blushwood.com** (US, TX) — full-motion video hero of the agent herself, personal pitch as primary nav item.

**Rejected as too generic/corporate:** winkworth.co.uk, rivendell-estates.co.uk, anthonypepe.com, bartonwyatt.co.uk (all revert to stock-photo/CTA-banner/cookie-chrome template mechanics despite decent photography). **Rejected as too cold/architectural again:** domusnova.com, kumarawilcoxon.com.

**Pattern worth carrying forward:** warm single-accent color, agents/team given real homepage weight, taglines naming the personal/family promise directly, hero photography showing a lived-in room or a real person rather than an empty architectural frame.

## WHITEFOX Gold Coast — structural base for O'Neill Group
Real, existing agency (goldcoast.whitefoxrealestate.com.au) — the departing principal's new venture ([[oneill-group]]) is using WhiteFox's **structure/UX only** as a base, explicitly not their colours or copy. Full pattern audit done 2026-08-17 (structure/mechanics only, colours/copy excluded):

**Navigation** — horizontal nav + hamburger for secondary items even when top-level nav is short. Region/location-switcher opens a full-screen overlay (vertically-stacked office list). Nav transparent-over-hero, solidifies on scroll/interior pages. Breadcrumb trail on every interior page.

**Hero** — full-bleed, full-viewport video/image, rotates between multiple assets across loads. No headline overlaid on homepage hero — message deferred to the section below (hero = pure mood). **Signature device: pinned/sticky hero with the next panel sliding up over it** — reused on property-detail pages (gallery hero pins, info panel slides over).

**Homepage flow** — hero → brand statement (two-col narrative+imagery) → 4-tile nav-as-content grid (Property/Sell/Projects/People) → featured-listing carousel (one at a time, not grid) → network/offices section (tabbed by country) → **embedded live mini version of the full listings search** (not just 3 teaser cards) → capability/careers section → stats/proof band (4 big numbers) → press logos → blog teaser → footer.

**Listing cards** — full-width photo (staggered fade-in), caption = address (bold) + suburb only, no price/beds/baths at grid level (reserved for detail page/carousel).

**Property detail page** — pinned gallery hero w/ prev/next + "X of Y" counter + floating expand icon. Stat row (Bed/Bath/Car/Land, icon-free). Body copy truncated with "Continue" expand. Right-hand utility column = arrow-suffixed links (Floorplan/Video/Brochure/Enquire), not buttons — keeps page quiet. Inline enquiry form (not modal). "Related Listings" carousel at the bottom.

**Team page** — filter bar (Office/Specialty/Search) reusing listing-search visual language. **Grouped by role-tier headings** (Managing Directors/Associate Directors/Advisors) not one flat grid. Card→individual profile page (contact-card style: name/role/office badge/phone/email/socials + one portrait photo, no bio paragraph).

**Footer** — multi-region link columns (country headings, city links) — footer doubles as network sitemap. Separate socials column. Separate utility list (Contact/Newsletter/Privacy). Bottom bar keeps legal/credits visually separate.

**Mobile (375px)** — nav shrinks to logo+region pill+hamburger. Filter bar collapses many dropdowns into one "Refine" button — reusable pattern for dense filter UI going responsive.

**Motion** — pinned-hero/slide-over is the standout device, worth replicating for cinematic feel. Staggered card fade-in. Carousels use arrow+counter, not dot pagination, consistently.

**Forms** — newsletter has a "long" version (modal: name+name+email) and "short" version (footer: email+phone only). Minimal-chrome inputs (placeholder-as-label, bottom-border style, no boxes).

**Worth reusing directly for O'Neill Group:** the network/offices data-reuse pattern (nav overlay + homepage section + footer, same data three ways — adapt to O'Neill's actual office count even if just one location, still worth a dedicated locations content section if they expand later), the pinned-hero/slide-over transition as a signature device, the embedded-live-search homepage section, role-tiered team directory, and the quiet arrow-link utility column on detail pages instead of a button row.
