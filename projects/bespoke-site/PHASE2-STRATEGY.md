# Bespoke Estate Agents — Phase 2 Design Strategy

*Editorial luxury real-estate site with CRM-ready architecture. Strategy/brief — not a build. Dated 2026-07-22.*

## Positioning call
WHITEFOX is a loud national network (brash tone, 20 offices). Bespoke is the opposite archetype: boutique, understated, one trusted team, confidence through knowledge not volume. **Rule for the whole phase: adapt WHITEFOX's structure and discovery UX; reject its voice and network-scale claims** (which would breach Bespoke's own "no volume/superlative claims" rule).

Design lane (confirmed via UI database): **Exaggerated Minimalism** — luxury/editorial/architecture, oversized type, high contrast, massive whitespace. The editorial *serif* direction (Zodiak) is Bespoke's edge over WHITEFOX's all-sans.

## 1. Visual direction
Architectural editorial — a printed property monograph / architecture journal (Est, The Local Project, Assemble Papers), not a real-estate portal. Full-bleed cinematic photography and film carry every section; type sparse, large, serif; whitespace is the luxury signal. Extends the existing video-hero instinct into browsing and reading, so depth still feels like a gallery, never a database.

## 2. Typography (locked — existing brand)
- **Zodiak Light (300)** — all display/headings. Never bold; Regular 400 only where legibility demands. The differentiator vs WHITEFOX.
- **Poppins** — Regular body, Medium UI, SemiBold CTAs. Fallback Georgia/system.
- New this phase: editorial long-form scale — Zodiak for article titles/pull-quotes, Poppins 400 ~19px/1.7 for reading, capped 65–75ch.

## 3. Colour (locked — existing brand, disciplined)
Bespoke Green `#132a24` (primary) · off-white `#F0EDE8` (surfaces) · charcoal `#2A2A2A` (body) · greys `#E2DDD7 / #C8C2BB / #7A7470`. **No accent colours.** Green is the single functional accent — active filters, selected states, hover underlines, "Suburb Record" markers. Only exception: a muted, desaturated validation state so it doesn't break the palette. (Overrode the UI tool's teal/blue + Cinzel/Josefin picks — identity preservation wins.)

## 4. Spacing & rhythm
8px base. Spacious section padding `clamp(6rem, 12vh, 11rem)`. 12-col grid deliberately broken — asymmetric 60/40 & 70/30 splits, edge-bleeding images, generous single-column reading measures, alternating media-left/right like magazine spreads. One dominant idea per fold.

## 5. Navigation
Primary: **Listings · Suburbs · Sold · Journal · About · Contact** + persistent quiet **"Book a Private Appraisal"** CTA. Full-screen overlay menu (large Zodiak links + location/phone/email footer) — keep, it's a premium moment. Sticky header: translucent-green over imagery, solid on scroll.

## 6. Property discovery / search UX
- **Listings index:** spacious 2-up (desktop) / 1-up (mobile) gallery of large image cards — address, suburb, bed/bath/car, land size, price or EOI. Big imagery, minimal chrome, no badges.
- **Filter bar:** Buy / Sold / Upcoming tabs + Suburb · Price · Beds · Baths · Car · Type. Single quiet horizontal bar, filters as green/off-white pill toggles (not a dense sidebar). Results stagger-reveal.
- **No map initially** — over-engineering for boutique inventory; add later only if volume justifies.
- **Individual listing page** = the actual product: full-bleed hero film, scroll-through gallery, floorplan, suburb context, one enquiry form.
- Search must be genuinely functional (suburb/status/type/price/attributes), never fake UI.

## 7. Regions → "Suburb Guides" (curated GC prestige pockets)
Avoid WHITEFOX's national office map (false signal for one GC team). Reframe as curated Suburb Guides for genuine GC prestige pockets Bespoke works (real list TBC — e.g. Mermaid Waters, Broadbeach Waters, Sovereign Islands, Hope Island, Isle of Capri). Each = full-bleed suburb hero + short editorial intro + that suburb's listings pulled live from the model. Local-authority SEO + positions Jason as *the* authority in a defined patch. Highly curated tone; structured to add/remove suburbs without rework.

## 8. Featured / suburb-record section → "Recent Results"
Adapt WHITEFOX's recent-sales carousel, quieter: a band of full-bleed sold properties, small green type-only **"Suburb Record" / "Sold"** markers (no starburst). One hero result dominates, small row beneath. Understated brag matching the caption voice; proof-of-performance without publishing volume numbers.

## 9. WHITEFOX — adapt vs avoid
| Adapt | Avoid |
|---|---|
| Narrative-before-search (brand story first, tools lower) | Brash "making homes more expensive" tone |
| Recent-sales / suburb-record proof band | National multi-office "global mindset" map |
| Tabbed Buy/Sold/Upcoming + clean filters | Loud all-sans typography |
| Editorial "Journal" hub + press/proof logos | Newsletter jammed in twice / spammy repeats |
| Full-bleed cinematic photography, lavish whitespace | Data-dense card grids, portal clutter |
| Suburb-as-content | Podcast/media-empire scale |

## 10. Decisions (from clarifying round, 2026-07-22)

**Listings data — HYBRID, architected CRM-ready.** This may become a ~$30k deal that also builds the client a CRM, so the site is NOT a dead-end manual showcase. Build premium editorial front end now with working search/filter over curated (manually-entered) listings; architect the data model + components so listings, filters, statuses, regions, and lead capture map cleanly into a CRM and a live feed later. Forms = CRM entry points. Property status/metadata modelled consistently for future sync. Region/office pages structured for future location/agent data.

**Region scope — curated GC prestige pockets** (Option 1). Boutique local authority, quality over quantity, add/remove later.

**Editorial capacity — occasional market pieces** (Option 2). Low-volume evergreen Journal (suburb reports, market notes, notable sales). Most editorial feel comes from photography/layout/typography/suburb pages, not constant article production.

**Stack — RECOMMENDATION: Next.js + schema-first headless backend, not WordPress.** The CRM scope makes WP too limiting (WP-as-CRM = plugin graveyard; live-feed sync into CPT is fragile). Recommended: **Next.js (App Router)** front end + **Payload CMS (Postgres, self-hosted, client owns data)** as the headless backend whose collections *are* the CRM objects; search via Postgres full-text or a light Meilisearch/Typesense index; forms write `Lead` records via the same API; live portal feed staged in later by upserting on `externalId`. Fallback if WP-only is mandated: CPT + ACF + FacetWP — but flag that it caps the CRM ambition and the feed sync is fragile.

## CRM-ready data model
| Object | Key fields | Powers |
|---|---|---|
| **Listing** | slug, address, `suburb→Region`, status (`for_sale`/`under_offer`/`sold`/`upcoming`/`off_market`), price + priceDisplay (EOI/POA), propertyType, beds/baths/cars, land/floor size, features[], heroMedia, gallery[], video, floorplan[], `agent→Agent`, soldDate/soldPrice, suburbRecord(bool), externalId | Gallery, detail page, Buy/Sold/Upcoming tabs, record band |
| **Region (Suburb)** | slug, name, heroMedia, editorialIntro, stats?, agents[] | Suburb guides, suburb filter, SEO |
| **Agent/Person** | slug, name, role, photo, bio, phone, email | About, listing bylines (Jason/Barbara) |
| **Lead** | name, email, phone, message, source (`appraisal`/`enquiry`/`listing_enquiry`/`subscribe`), relatedListing?, relatedRegion?, status | Every form |
| **Contact** | person a Lead converts to (dedup email/phone) | Future CRM |
| **Deal/Transaction** | listing + contact(s) + stage (`appraisal`/`listing`/`campaign`/`under_contract`/`settled`) + value | Future CRM (stage aligns with Listing.status) |
| **Office** | name, region, agents[] | One office now; multi-office later without rework |

Consistency rules: (1) one `status` enum drives both search tabs and the future Deal pipeline; (2) every form is a `Lead` with a `source` — the single CRM seam.

## Roadmap
- **2a Foundation:** Payload schema (Listings/Regions/Agents/Leads) + Next.js shell (nav, brand tokens, full-bleed hero, property card, filter bar). Seed with real curated listings.
- **2b Discovery:** Listings index (filterable) → individual listing page (highest value) → Recent Results / suburb-record band.
- **2c Local authority:** Suburb index + guide template (curated GC pockets).
- **2d Editorial + capture:** low-volume Journal + unified appraisal/enquiry forms → Leads.
- **3 (staged):** live portal/CRM feed sync, saved searches, agent/office expansion, Deal pipeline.

## Reusable components
Filter bar (tabs + pills) · Property card · Full-bleed media hero (image/video) · Editorial split block (asymmetric text+media) · Suburb-record marker (type-only) · Gallery/lightbox · Enquiry/appraisal form (single, consistent, → Lead) · Press-logo strip.

## Locked decisions — round 2 (2026-07-22)

**Team face — Jason & Barbara duo.** Premium boutique husband-and-wife positioning; warm but refined, not family-business cheesy, not a scaled team story yet. Two `Agent` records, joint presence on About + brand story, listing bylines support individual or duo attribution.

**Search taxonomy — Standard (locked).** Buy / Sold / Upcoming tabs + Suburb · Price · Beds · Baths · Car · Property type. No land-size/keyword/advanced-sort this phase (staged to P3). Clean, low-friction, not portal-like.

**Suburb Guides — proposed shortlist (Hunter to approve/correct against real footprint).** Grounded in GC prestige-market reality + Bespoke's inferred footprint from known listings (Broadbeach Waters/Monaco St, Paradise Waters, Carrara/The Boulevard, Benowa testimonial, Somerset Dr/Northview north-corridor shoots).

*Primary (launch 6):*
- **Sovereign Islands** — apex GC address, gated deep-water mega-mansions; anchors the prestige claim.
- **Mermaid Waters + Mermaid Beach** — blue-chip waterfront + Hedges Ave "Millionaires' Row"; broadest recognition.
- **Broadbeach Waters** — established canal luxury, central; Bespoke sold here (Monaco St).
- **Paradise Waters / Main Beach** — tightly-held waterfront enclave; Bespoke listing history.
- **Isle of Capri** — tightly-held island prestige beside Surfers; scarcity.
- **Sanctuary Cove / Hope Island** — gated marina-golf prestige, north GC; ties to Bespoke's north-corridor work.

*Secondary (expand-later):* Carrara · Benowa & Benowa Waters · Clear Island Waters · Surfers Paradise · Tallebudgera & Currumbin Valley · Runaway Bay.

**Stack — dual-path (do not collapse to generic WP; do not assume CRM real until stack capability confirmed).**

*Path A — PREFERRED: Next.js + Payload.* Next.js App Router + brand tokens + GSAP, Vercel host. Payload CMS (Postgres via Neon/Supabase) — collections are the CRM objects, real admin for Jason & Barbara. Filtered Postgres search now (Meilisearch later), forms → Lead collection. CRM path real: add Contacts/Deals + pipeline later; live feed = sync job upserting Listings by externalId. Owned relational DB, best performance/motion ceiling. Cons: higher build skill (React/Node), Vercel + managed Postgres devops, higher cost/maintenance.

*Path B — FALLBACK: WordPress + ACF + FacetWP.* Listings/Regions/Agents = ACF CPTs mirroring the same fields; FacetWP facets (suburb/price/beds/baths/car/type); Gravity/Fluent Forms → FluentCRM. Faster, cheaper, familiar to the current WP team, easy client editing. CRM ambition CAPPED: FluentCRM is a bolt-on not a relational model, live-feed sync into CPTs is fragile/custom, and the future CRM becomes a separate rebuild not an extension.

*Tradeoff:* if the CRM is genuinely part of the $30k, Path A — Path B means paying twice (site now, CRM rebuild later). **Design decision either way: front-end component contracts (card props, filter state) are specified stack-agnostic**, so design and pages are identical on both paths; only the data layer differs. Choosing the stack later then costs nothing on the design.

## Remaining open items
- Hunter to approve/correct the suburb shortlist against where Jason & Barbara actually transact.
- Confirm whether the other team can build/maintain Next.js + Payload (decides Path A vs B).
- Source of initial listings to seed (existing 10x shoots: Somerset Dr, Cairngorm, Northview, etc.).
- Next step: build spec for the other team (both paths) OR Claude prototypes the design language in the real stack.
