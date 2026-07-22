# Bespoke Estate Agents — Phase 2 Build Spec (Source of Truth)

*Version 1.0 · 2026-07-22 · Implementation blueprint. Pairs with [PHASE2-STRATEGY.md](PHASE2-STRATEGY.md) (the "why"). This doc is the "what + how". No build has started.*

## How to use this document
- This is the **source of truth** for Phase 2 implementation. If code and this doc disagree, update the doc in the same PR.
- The **front-end design system, component contracts, page structure, and acceptance criteria are stack-agnostic** — identical whether we build Path A (Next.js + Payload) or Path B (WordPress + ACF + FacetWP). Only the **data layer / implementation notes** differ; those are isolated in §11.
- Anything marked **[P3+]** is explicitly out of scope for Phase 2 — do not build it now, but do not architect in a way that blocks it.
- Handoff: a builder (incl. Lach) should be able to build any page from its section (§8) without needing to ask what a component does (§5–6) or how search behaves (§7).

---

## 1. Approved decisions (locked)
- **Positioning:** boutique GC prestige; adapt WHITEFOX structure, reject its brash voice/scale. Understated, no volume/superlative claims (brand rule).
- **Identity (unchanged):** Zodiak Light headings, Poppins body, Bespoke Green + off-white + charcoal, **no accent colours**.
- **Team face:** Jason & Barbara — premium boutique duo. Two Agent records; joint on About/brand story; bylines individual or duo.
- **Search taxonomy:** Buy / Sold / Upcoming + Suburb · Price · Beds · Baths · Car · Property type. (No land-size/keyword/advanced-sort in P2.)
- **Suburbs:** curated GC prestige guides. Primary 6 proposed (§9), pending Hunter's approval.
- **Editorial:** low-volume evergreen Journal; most editorial feel from photography/type/layout.
- **Data:** hybrid, CRM-ready. Front end works over curated listings now; model maps cleanly to a CRM + live feed later.
- **Stack:** dual-path. A (Next.js + Payload) preferred; B (WP + ACF + FacetWP) fallback. Design identical either way.
- **Motion:** ease-out (expo/quart), **no bounce/elastic** (overrides the UI-tool's `back.out` suggestion). Reveals enhance already-visible content — never gate content visibility on JS (lesson from the live-site audit).

## 2. Remaining assumptions (confirm, don't block)
- Suburb list per §9 is provisional until Hunter approves against real footprint.
- Path A vs B pending the other team's Next.js capability. Build front end to the stack-agnostic contracts until decided.
- Initial listing content seeded from existing 10x shoots (Somerset Dr, Cairngorm, Northview, Monaco St, Paradise Waters, The Boulevard). Assume 6–20 listings at launch (boutique volume → no map, no pagination beyond "load more").
- Currency AUD; locale en-AU; prices often "EOI"/"POA" rather than fixed (model must allow non-numeric display).
- One office (Gold Coast). Office modelled but not surfaced as UI in P2.

---

## 3. Design system (stack-agnostic tokens)

**Colour**
```
--be-green:        #132A24   /* primary surface (dark sections, header over hero), CTA bg */
--be-green-2:      #152F2A   /* secondary dark — NEVER in same component as --be-green */
--be-offwhite:     #F0EDE8   /* light section surface */
--be-white:        #FFFFFF   /* cards on off-white, listing surfaces */
--be-ink:          #2A2A2A   /* body text on light */
--be-grey-500:     #7A7470   /* muted body / meta on light */
--be-grey-300:     #C8C2BB   /* muted text on green, dividers on dark */
--be-grey-200:     #E2DDD7   /* borders/dividers on light */
--be-on-dark:      #F0EDE8   /* text on green */
--be-focus:        #F0EDE8   /* focus ring on dark = off-white; on light = --be-green */
--be-valid-error:  #8A5A4A   /* desaturated clay — validation only, stays in-palette */
```
Green is the only functional accent (active filter, selected tab, hover underline, suburb-record marker). No gold/navy/red.

**Typography**
- Display/headings: **Zodiak** weight 300 (400 only where legibility forces it). Never 700+.
- UI/body: **Poppins** 400 body, 500 UI labels, 600 CTAs.
- Editorial reading body: Poppins 400, ~19px / line-height 1.7, measure **65–75ch**.
- Fallbacks: Zodiak→Georgia,serif; Poppins→system-ui,sans-serif.
- Scale (fluid clamp, ≥1.25 ratio): h1 `clamp(2.5rem,6vw,4.5rem)`; h2 `clamp(2rem,4vw,3rem)`; h3 `clamp(1.5rem,2.5vw,2rem)`; body 1rem; small 0.875rem. Display letter-spacing ≥ -0.02em (never tighter than -0.04em). `text-wrap:balance` on h1–h3.

**Spacing** — 8px base. Scale: 8/16/24/40/64/96/160. Section vertical padding `clamp(6rem,12vh,11rem)` (spacious). Content max-width 1280px; reading max-width 72ch.

**Radius** — 4px buttons/inputs, 8px cards/media. No fully-rounded pills except filter toggles (which use 999px intentionally).

**Motion** — reveal 300–450ms ease-out-expo, stagger 60ms; hover/state 150–200ms. Reveals animate an already-visible default (opacity/transform only; never `display`/layout). `@media (prefers-reduced-motion:reduce)` → instant/crossfade, no transform. Respect it everywhere.

**Breakpoints** — 375 (mobile), 768 (tablet), 1024 (laptop), 1440 (desktop). Mobile-first. No horizontal scroll at any width; wide elements (tables, galleries) scroll inside their own container.

**z-index scale** — dropdown 100 · sticky-header 200 · overlay-menu 300 · modal-backdrop 400 · modal/lightbox 410 · toast 500. No arbitrary 9999.

**A11y baseline (all pages)** — body contrast ≥4.5:1, large text ≥3:1; visible focus rings (never removed); keyboard operable; single h1/page, ordered headings; alt text on all content images; touch targets ≥44×44px with ≥8px spacing; forms have visible labels.

---

## 4. Data model (CRM-ready spine)

Types below are the **canonical contract**. Path A = Payload collections; Path B = ACF field groups on CPTs. Field names identical where possible.

**Enums**
```
ListingStatus = for_sale | under_offer | sold | upcoming | off_market
PropertyType  = house | apartment | townhouse | duplex | land | acreage
PriceDisplay  = numeric (show formatted) | eoi | poa | contact_agent
LeadSource    = appraisal | enquiry | listing_enquiry | subscribe
DealStage     = appraisal | listing | campaign | under_contract | settled   // [P3+]
```

**Listing**
```
id, slug, address{street,suburb→Region,state,postcode},
status: ListingStatus, propertyType: PropertyType,
price:{ display: PriceDisplay, amount?:number, label?:string },  // label e.g. "EOI closing 12 Aug"
beds:int, baths:int, cars:int, landSize?:number(m²), floorSize?:number(m²),
features:string[],                                    // shown on detail page only [not a P2 filter]
heroMedia:Media, gallery:Media[], video?:Media, floorplans?:Media[],
agent→Agent (primary), coAgent?→Agent,
soldData?:{ date:ISO, price?:number, suburbRecord:boolean },
externalId?:string,                                   // feed sync key [P3+], nullable now
seo{title,description}, createdAt, updatedAt
```

**Region (Suburb Guide)**
```
id, slug, name, tier: primary|secondary,
heroMedia:Media, intro:RichText(150–250 words),
stats?:{ label,value }[],           // optional, evergreen only (e.g. "Median house price")
agents:Agent[],                     // structured for future multi-agent
seo{title,description}, order:int
// listings are DERIVED: query Listings where address.suburb == this region
```

**Agent (Person)**
```
id, slug, name, role, photo:Media, bio:RichText, phone, email,
socials?:{instagram?,linkedin?}, seo{title,description}
// Jason Ward, Barbara Ward
```

**Lead**  *(every form writes one — the single CRM seam)*
```
id, name, email, phone?, message?,
source: LeadSource, relatedListing?→Listing, relatedRegion?→Region,
status: new|contacted|qualified|archived (default new),
consent:boolean, createdAt
```

**Media** — `{ url, alt, width, height, type: image|video, focalPoint? }`. All images WebP/AVIF with width variants; explicit dimensions (CLS<0.1).

**[P3+] Contact, Deal, Office** — do not build UI now. Reserve: Contact (dedup Lead by email/phone), Deal (Listing+Contact(s)+DealStage+value), Office (name,region,agents[]). `DealStage` intentionally mirrors `ListingStatus` semantics so the pipeline aligns later.

**Relationship rules**
- Region↔Listing is by `address.suburb` slug (derived lists), not a manual join — add a suburb, its listings appear automatically.
- Deleting an Agent must not orphan Listings (block or reassign).
- `status` is the single source driving search tabs (§7) and, later, the Deal pipeline.

---

## 5. Component inventory

| Component | Purpose | Used on |
|---|---|---|
| `SiteHeader` | Sticky nav; translucent over media, solid on scroll | all |
| `OverlayMenu` | Full-screen nav overlay (large Zodiak links + contact block) | all |
| `MediaHero` | Full-bleed image/video hero + overlaid title/eyebrow/CTA | home, listing, suburb, journal, page heros |
| `EditorialSplit` | Asymmetric text+media block, alternating sides | home, services, about, suburb |
| `FilterBar` | Tabs (Buy/Sold/Upcoming) + filter pills | listings index, suburb (scoped) |
| `PropertyCard` | Large-image listing card + minimal meta | listings grid, suburb, home featured |
| `PropertyGrid` | Responsive 2-up/1-up grid w/ stagger reveal + empty/loading states | listings, suburb, sold |
| `ListingGallery` | Detail-page scroll gallery + lightbox | listing detail |
| `SuburbRecordMarker` | Type-only green "Suburb Record"/"Sold" tag | cards, results band, listing |
| `ResultsBand` | Curated "Recent Results" showcase (hero result + row) | home, sold |
| `SuburbCard` | Suburb guide entry (hero + name) | suburbs index, home |
| `EnquiryForm` | Unified appraisal/enquiry/listing-enquiry form → Lead | contact, listing, suburb, CTA sections |
| `PressStrip` | Row of press/proof logos (monochrome) | home, about |
| `JournalCard` | Article entry (image + title + category) | journal index, related |
| `ArticleBody` | Long-form editorial (Zodiak titles, 65–75ch body, pull-quotes) | journal article |
| `SiteFooter` | Nav, contact, socials, legal, © year | all |
| `Breadcrumbs` | Deep-link context (Suburbs / Mermaid Waters) | listing, suburb, article |

Icons: SVG only (Lucide/Heroicons or brand set). No emoji.

---

## 6. Component behaviour & states

**SiteHeader** — Default: transparent bg, off-white logo+links over media. Scrolled (>hero or >80px): solid `--be-green`, subtle shadow, 150ms. Focus: each link has visible focus ring. Mobile: links collapse to hamburger → `OverlayMenu`. CTA "Book a Private Appraisal" persists (in header on desktop, inside overlay on mobile).

**OverlayMenu** — Trigger: hamburger (`aria-expanded`, `aria-controls`). Open: full-viewport `--be-green`, large Zodiak links, contact footer; focus trapped; `Esc`/backdrop/link closes; body scroll locked; returns focus to trigger. Reduced-motion: instant, no slide.

**MediaHero** — Props `{media, eyebrow?, title, subtitle?, cta?, height:'full'|'tall'}`. Video: muted, autoplay, playsinline, loop, `poster` set (never a blank frame); image fallback if no video. Text always readable: gradient scrim + soft text-shadow on bright media. Title Zodiak, `text-wrap:balance`. **Content is visible by default**; any entrance animation is enhancement only.

**FilterBar** — see §7. States: default, active pill (green fill/underline), open dropdown (price/type), applied-count indicator, "Clear all" when any active. Sticky under header on scroll of the index. Keyboard operable; dropdowns escape overflow via portal/fixed (no clipping).

**PropertyCard** — Props from `Listing`. Shows heroMedia (lazy, explicit dims), address line (street + suburb, Zodiak), meta row (beds·baths·cars, land if present), price display, status/record marker. States: default; hover (image scale 1.03 + underline address, 200ms, GPU transform only); focus (ring on whole card, it's one link); sold (marker + optional muted overlay). No price → shows `price.label`/"EOI"/"POA". Never a Canva badge.

**PropertyGrid** — 2-up ≥1024, 1-up <768, `minmax(340px,1fr)` between. Stagger reveal on scroll (enhancement). **Loading:** skeleton cards (reserve dimensions, no CLS). **Empty:** "No properties match these filters." + Clear-all. **Error:** graceful message + retry, never a blank region.

**ListingGallery** — Grid/scroll of gallery images; click → lightbox (native `<dialog>`/popover, focus-trapped, arrow-key nav, `Esc` close, counter). Lazy-load; first image eager (it's LCP). Floorplans in a labelled sub-section.

**EnquiryForm** — Fields: name, email, phone(optional), message; hidden `source` + `relatedListing`/`relatedRegion` when contextual; consent checkbox. **Visible labels** (not placeholder-only). Inline validation on blur, error text adjacent to field in `--be-valid-error`, `aria-describedby`. States: idle, validating, submitting (disabled + spinner), success (inline confirmation, not just a redirect), error (preserve input, show reason). On success → creates one `Lead`. Anti-spam: honeypot + basic rate-limit. Never store card/credential data.

**SuburbRecordMarker** — Small uppercase Poppins 500 on green (or green text on off-white), no icon/starburst. Variants: "Suburb Record", "Sold", "Under Offer".

**ResultsBand** — One dominant sold hero (full-bleed + marker + address + optional achieved result if publishable) then a small row of 3–4. Understated. No volume/aggregate numbers (brand rule).

**JournalCard / ArticleBody** — Card: image + category tag + Zodiak title, hover underline. Article: MediaHero, ArticleBody (measure 65–75ch, Zodiak title + pull-quotes, Poppins 19/1.7), byline (Jason/Barbara), related JournalCards, closing EnquiryForm CTA.

**SiteFooter** — Explore nav, contact (tel/mailto), socials (real handles — verify before ship), legal, dynamic © year, "Beyond Luxury Real Estate" line.

Global: every clickable has `cursor:pointer` + hover transition (150–300ms) + visible focus; all states respect reduced-motion.

---

## 7. Search / filter logic

**Filter state (canonical, URL-synced for deep-linking & sharing):**
```
{ status:'buy'|'sold'|'upcoming'='buy',
  suburb:string|null, priceMin:number|null, priceMax:number|null,
  beds:number|null, baths:number|null, cars:number|null,
  propertyType:PropertyType|null }
```
Each maps to a query param (`?status=buy&suburb=mermaid-waters&beds=3`). On load, hydrate from URL. Changing a filter updates URL (history-replace) so results are shareable/back-button-safe.

**Status → data mapping:**
- `buy` → Listing.status ∈ {for_sale, under_offer}
- `sold` → Listing.status == sold
- `upcoming` → Listing.status == upcoming
- `off_market` never shown in public search.

**Semantics:** beds/baths/cars = **minimum** ("3+"). price = inclusive range (either bound optional). suburb = exact region match (dropdown from existing Regions). propertyType = exact.

**Sort:** default `sold` → soldData.date desc; `buy`/`upcoming` → newest (createdAt desc) then price desc. (Advanced sort UI = [P3+].)

**Behaviour:** debounce text/range 250ms; results update without full reload (client filter on the fetched set at boutique volume; server/query filter under Path A if set grows). Stagger-reveal new results. Applied-filter count + "Clear all". Empty state per §6. No layout shift on filter change.

**Suburb-scoped search:** on a Suburb Guide, FilterBar is pre-scoped to that suburb (suburb filter locked/hidden) and defaults to `buy`.

---

## 8. Page-by-page structure + acceptance criteria

Legend: **Sections** (top→bottom) · **Data** · **AC** = acceptance criteria (testable).

### 8.1 Home
- **Sections:** MediaHero (video, "Beyond Luxury Real Estate") → brand intro (EditorialSplit) → featured PropertyGrid (3–4 current) → ResultsBand (recent sold/records) → Suburbs teaser (3 SuburbCards) → Journal teaser (2–3 JournalCards) → PressStrip → EnquiryForm CTA → Footer.
- **Data:** featured Listings (status=for_sale, flagged/recent), sold Listings, 3 Regions, latest articles, agents.
- **AC:** hero video autoplays muted/looped with poster (no blank frame); all body content visible without JS/scroll-gating; LCP hero not lazy; featured cards link to detail; suburbs/journal teasers link to their indexes; single h1; passes a11y baseline; no horizontal scroll 375–1440.

### 8.2 Listings index  *(highest-traffic discovery page)*
- **Sections:** MediaHero (short) → sticky FilterBar → PropertyGrid → "Load more" (if >12) → EnquiryForm CTA.
- **Data:** all public Listings.
- **AC:** filters produce correct sets per §7; URL reflects filters and is shareable/back-safe; empty/loading/error states render (never blank); tab switch (Buy/Sold/Upcoming) re-queries correctly; cards keyboard-focusable; results reveal without CLS; touch targets ≥44px; works at all breakpoints.

### 8.3 Listing detail  *(the product page)*
- **Sections:** MediaHero (hero image/video) → address + price + status/record marker + key meta (beds/baths/cars/land) → ListingGallery + lightbox → description (Zodiak/Poppins) → features list → floorplans → suburb context (link to Suburb Guide) → agent(s) block (Jason/Barbara) → EnquiryForm (source=`listing_enquiry`, relatedListing set) → related listings in same suburb.
- **Data:** one Listing + its agent(s) + same-suburb listings.
- **AC:** first gallery image eager (LCP); lightbox keyboard + focus-trapped + Esc; enquiry creates a Lead with correct source+relatedListing; price renders numeric OR EOI/POA label; sold listings show marker + sold context; breadcrumb Suburbs→Suburb→Address; all images have alt; SEO title/description populated; deep-linkable URL `/listings/[slug]`.

### 8.4 Suburbs index
- **Sections:** MediaHero → intro line → grid of SuburbCards (primary tier first) → CTA.
- **Data:** Regions ordered by `order`, tier.
- **AC:** each card links to `/suburbs/[slug]`; primary suburbs surface above secondary; responsive grid; a11y baseline.

### 8.5 Suburb Guide  *(see §9)*
- **Sections:** MediaHero (suburb) → editorial intro (150–250 words) → optional evergreen stats → suburb-scoped PropertyGrid (FilterBar pre-scoped) → agent block → EnquiryForm (source=`enquiry`, relatedRegion set) → related suburbs.
- **Data:** one Region + derived Listings (by suburb) + agents.
- **AC:** listings shown are exactly that suburb's; scoped filter works with suburb locked; intro is real editorial (not lorem); enquiry sets relatedRegion; SEO populated; deep-linkable.

### 8.6 Sold / Recent Results
- **Sections:** MediaHero → ResultsBand → PropertyGrid (status=sold) → CTA.
- **Data:** sold Listings, suburb-record flags.
- **AC:** only sold listings; record markers render; NO aggregate volume numbers; cards link to detail (or sold detail); a11y baseline.

### 8.7 Journal index + Article
- **Index Sections:** MediaHero → JournalCard grid (optional category filter) → CTA.
- **Article Sections:** MediaHero → ArticleBody (65–75ch) → byline → related → EnquiryForm CTA.
- **AC:** article body reading measure 65–75ch; Zodiak title/pull-quotes; byline Jason/Barbara; related links; works with as few as 2–3 articles (no broken empty grid); [content low-volume, evergreen].

### 8.8 About + Contact
- **About:** brand story (EditorialSplit), Jason & Barbara duo block (two agents, joint framing), PressStrip, values, CTA.
- **Contact:** EnquiryForm (source=`appraisal`), phone/email/location, map optional (static, [P3+] for interactive).
- **AC:** duo presented refined (not cheesy); form creates Lead source=appraisal; contact links are tel:/mailto:; a11y baseline.

**Global AC (every page):** a11y baseline (§3); no content hidden behind JS-only reveals; no horizontal scroll 375–1440; Lighthouse a11y ≥95, CLS <0.1, images WebP/AVIF + lazy (except LCP); reduced-motion honored; 404 + basic error page exist.

---

## 9. Suburb Guide structure & proposed list
**Template:** hero (full-bleed suburb image) · name + one-line positioning · editorial intro 150–250 words (why this suburb, buyer profile, Bespoke's angle — evergreen, no time-sensitive claims) · optional 2–3 evergreen stats · suburb-scoped listings grid · agent block · enquiry (relatedRegion) · related suburbs.

**Primary (launch 6 — pending Hunter approval):** Sovereign Islands · Mermaid Waters + Mermaid Beach · Broadbeach Waters · Paradise Waters / Main Beach · Isle of Capri · Sanctuary Cove / Hope Island.
**Secondary (expand-later):** Carrara · Benowa & Benowa Waters · Clear Island Waters · Surfers Paradise · Tallebudgera & Currumbin Valley · Runaway Bay.
Rationale per suburb: see [PHASE2-STRATEGY.md](PHASE2-STRATEGY.md) §"Locked decisions — round 2".

---

## 10. Phase boundaries
**Phase 2 (this spec):** Home, Listings index, Listing detail, Suburbs index + guides, Sold/Results, Journal (light), About, Contact. Curated listings, working Standard search, forms→Leads, CRM-ready model.
**[P3+] (do not build now):** live portal/CRM feed sync (`externalId`), saved searches / accounts, map view, advanced filters (land size, keyword, sort UI), Contact/Deal/Office UI + pipeline, multi-office/multi-agent expansion, interactive maps, newsletter automation.

---

## 11. Stack-dependent implementation notes

Front end (design system §3, components §5–6, pages §8, search §7) is **identical** on both paths. Only data access differs. Build components against the §4 contract via a thin data-access layer (`getListings(filter)`, `getListing(slug)`, `getRegions()`, `getRegion(slug)`, `getAgents()`, `createLead(payload)`) so swapping the source doesn't touch UI.

### Path A — Next.js + Payload (PREFERRED; CRM real)
- **Front:** Next.js App Router, TypeScript, brand tokens as CSS variables, Tailwind or CSS Modules (builder's choice — tokens are the contract), GSAP for reveals/stagger. Host Vercel.
- **Backend:** Payload CMS; collections = §4 entities (Listing, Region, Agent, Lead; reserve Contact/Deal/Office). Postgres (Neon/Supabase). Payload admin = Jason/Barbara's listing entry.
- **Data layer:** server components fetch via Payload local API / REST; ISR or on-demand revalidation on listing publish.
- **Search:** filtered Postgres queries (server) or client filter over fetched set at low volume; add Meilisearch only if volume grows.
- **Forms:** `createLead` → Payload `Lead` collection + email notify (Resend/SMTP). Honeypot + rate-limit.
- **Media:** Payload upload + `next/image` (WebP/AVIF, sizes, blur placeholder).
- **CRM later:** enable Contact/Deal collections + admin views; feed sync = scheduled job upserting Listings by `externalId`. No front-end change.
- **Trade:** highest ceiling + owned relational DB; needs React/Node skill + Vercel/Postgres devops.

### Path B — WordPress + ACF + FacetWP (FALLBACK; CRM capped)
- **Front:** block theme or Elementor to the SAME tokens/components (§3, §5–6). Enqueue Zodiak/Poppins locally. GSAP or CSS for reveals — **content visible by default** (the live-site reveal bug: `.reveal` must not ship at opacity:0 gated on JS; make visible-by-default, animate as enhancement, raise specificity so the theme can't override).
- **Data:** ACF field groups on CPTs — `listing`, `region`, `agent` mirroring §4 field names; `status`/`propertyType`/`priceDisplay` as ACF select matching the enums exactly. Region↔Listing via a suburb taxonomy or ACF relationship.
- **Search:** FacetWP facets — status (tabs), suburb, price (range/slider), beds, baths, car, property type. Results template = PropertyCard markup. Deep-link via FacetWP URL params (mirror §7 param names where possible).
- **Forms:** Gravity Forms / Fluent Forms → map submissions to the Lead shape; FluentCRM for lead capture. `source`/`relatedListing` via hidden fields.
- **Media:** WebP via a plugin (e.g. ShortPixel), explicit sizes, lazy (except LCP hero).
- **CRM later:** FluentCRM is a bolt-on, not a relational Deal model; a proper CRM = separate rebuild. Live feed → CPT import is custom/fragile.
- **Trade:** faster, cheaper, familiar to the current WP team, easy client editing; **CRM ambition capped, pay-twice risk.**

### Choosing
If CRM is genuinely in the $30k scope → Path A. If the team is WP-only and CRM can be deferred/rebuilt → Path B, with the cap acknowledged in writing. Either way, hold the §4 field names and §7 param names constant so a later migration is a data move, not a redesign.

---

## 12. Handoff notes (for Lach / any builder)
- Start from the data layer (§4 + the `get*/createLead` contract), then the shell (SiteHeader, OverlayMenu, MediaHero, SiteFooter), then PropertyCard + FilterBar + PropertyGrid, then Listing detail, then indexes, then Suburb guide, then Journal, then forms.
- Every form must create exactly one `Lead` with the correct `source`; that is non-negotiable (CRM seam).
- Do not ship any page with content hidden behind a JS/scroll reveal that isn't visible by default (see the audited live-site bug).
- Verify real IG/FB/LinkedIn handles before shipping the footer.
- Keep this spec updated in the same PR as any deviation. Questions → resolve here, not in code comments.
