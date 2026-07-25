# Bespoke Collection — Breadth Pass (Suburbs + Journal)

**Date:** 2026-07-25
**Status:** design approved, awaiting spec review
**Target:** `projects/bespoke-site/prototype/` (the Phase 2 "Collection" section)
**Parent spec:** [BUILD-SPEC.md](../../../projects/bespoke-site/BUILD-SPEC.md) v1.0 — this document amends §8 and §9
**Strategy:** [PHASE2-STRATEGY.md](../../../projects/bespoke-site/PHASE2-STRATEGY.md)

---

## 1. Purpose

The Collection prototype currently ships three real pages (Listings index, Listing detail, `soon.html`). BUILD-SPEC §8 specs eight page types. This pass closes the genuine gap — Suburbs and Journal — and records which of the remaining specced pages are resolved elsewhere and should not be built.

Goal: a prospect can free-roam the Collection without reaching a placeholder, and the Suburb Guide (the differentiator named in PHASE2-STRATEGY) exists as a working, evidence-led template.

---

## 2. Amendments to BUILD-SPEC v1.0

These supersede the parent spec. Recorded here so no builder works from the stale version.

| BUILD-SPEC section | Status | Reason |
|---|---|---|
| §8.8 About + Contact | **Do not build** | The live WP site owns About and Contact. Commit `1d41928` repointed prototype nav to `bespoke.agents.10xvisuals.co/about/` etc. Building local copies forks client content. |
| §8.6 Sold / Recent Results | **Superseded** | Sold is a Buy/Sold/Upcoming tab inside the Listings index (commit `f051fa4`), not a standalone page. |
| §8.1 Home | **Superseded** | The live site is Home. Collection is a section of it, not a site with its own home. |
| §9 primary/secondary suburb tiers | **Revised** | The primary six were inferred from Gold Coast prestige geography, not from Bespoke's evidenced footprint. See §3. |

**Identity note:** commit `1d41928` ("match Collection chrome to live site, live links") changed what this artifact *is* — from an alternative site to a new section proposed for the client's existing site. Every page added here must read as native to the live WP chrome (minimal uppercase nav), and anything the live site already owns is out of scope.

---

## 3. Suburb tier revision

The evidenced footprint on [bespoke-estate-agents.md](../../../wiki/clients/bespoke-estate-agents.md) is: **The Boulevard, Carrara** (suburb-record one-bedroom), 82 Birdlife Court, Vespa Crescent, Marina Drive, and a **Benowa** seller testimonial. Carrara and Benowa Waters both sit in §9's secondary tier. The glamour suburbs placed in the primary tier — Sovereign Islands, Isle of Capri — have no supporting evidence in the vault.

**Decision:** build the two evidence-backed suburbs as the real templates. They can lead with verifiable proof rather than positioning prose.

- **Carrara** (`r10`) → promote to `tier:"primary"`, `guideStatus:"live"`
- **Benowa Waters** (`r9`) → promote to `tier:"primary"`, `guideStatus:"live"`
- All other regions → `guideStatus:"soon"`, tiers unchanged

The remaining eleven regions render as SuburbCards from the same template and become guides by flipping `guideStatus` once their positioning is confirmed. The full §9 tier list is **not** re-derived in this pass — flagged as open (§9 below).

---

## 4. Scope

### Build

1. **`suburbs.html`** — Suburbs index (BUILD-SPEC §8.4). SuburbCard grid, primary tier first, driven off `getRegions()`.
2. **`suburb.html?r=carrara`** — Suburb Guide, Carrara. Leads with the Boulevard suburb record.
3. **`suburb.html?r=benowa`** — same template, Benowa Waters. Leads with the seller testimonial.
4. **`journal.html`** — Journal index (§8.7). JournalCard grid.
5. **`article.html?a=<slug>`** — Article template, 3 evergreen drafts.

Pages 2 and 3 are one file parameterised by `?r=`, matching the existing `listing.html?p=` pattern.

### Do not build

About, Contact, Services, Projects, standalone Sold page, Home. See §2.

---

## 5. Data changes (`data.js`)

### 5.1 Region shape

Existing shape is `{ id, slug, name, tier, order, hero, intro }` — all 13 regions already present. Extend with:

```js
{
  id, slug, name, tier, order, hero, intro,   // existing
  positioning,    // one-line, sits under the name in the hero
  editorial,      // string[] — 150–250 words total, guide body (live guides only)
  heroGrade,      // 'warm' | 'cool' | 'neutral' | 'deep' — CSS filter class
  stats,          // [{label, value}] — 0–3 evergreen only, optional
  guideStatus     // 'live' | 'soon'
}
```

`intro` (existing, ~30 words) is retained for the SuburbCard. `editorial` is new and only populated for live guides — this avoids rewriting eleven intros in a pass that only ships two guides.

`heroGrade` exists because the Somerset Drive placeholder set is reused across all suburb cards, the live site's `#estates` section, and all six seed listings. Per-suburb tonal treatment makes repeats read as a consistent house style rather than a duplicated file.

### 5.2 Listings reassignment

All six seed listings sit in the deprioritised suburbs (`sovereign-islands`, `mermaid-waters`, `broadbeach-waters`, `isle-of-capri`, `paradise-waters`, `sanctuary-cove`). Carrara and Benowa have none, so their scoped grids would render empty and fail §8.5's acceptance criterion.

**Reassign two existing seed listings** — their street addresses are already invented, so only the suburb field moves. No real address receives a fabricated price.

- `34 Monaco Street` (Broadbeach Waters family home, most suburb-neutral description) → **Benowa Waters**
- `2101 / 45 Commodore Drive` (Paradise Waters apartment) → **Carrara**

Street names and `postcode` update to plausible values for the new suburb. Each guide then shows one scoped listing; the thin-results empty state already specced in §7 covers the rest.

### 5.3 Unearned claim removal

The invented Isle of Capri record (`data.js:96`) carries `soldData.suburbRecord: true`. Set to `false`. An invented suburb record in a suburb with no evidenced footprint risks being read as real — and the one genuine record Bespoke holds (Carrara) is not currently in the data at all.

### 5.4 Articles

New collection following the existing pattern:

```js
var ARTICLES = [
  { id, slug, title, dek, category, author,   // 'jason' | 'barbara'
    hero, body,                                // string[] paragraphs
    pullQuote,                                 // optional
    related }                                  // slug[]
];
```

Three evergreen drafts, written in Jason's voice per the caption-voice fingerprint (commit `713093e`). No time-sensitive claims, no volume figures, no always-on-site claims. Each article carries an HTML comment `<!-- DRAFT — client to approve -->` and the index shows nothing indicating draft status to a visitor.

---

## 6. Data-access layer (`app.js`)

Extend the existing seam. No new architecture.

```js
function getRegions(filter)        // add optional {tier, guideStatus}
function getRegion(slug)           // exists
function getArticles()             // new
function getArticle(slug)          // new
```

`getListings({suburb})` already supports suburb scoping — the Suburb Guide grid reuses it directly.

---

## 7. Page structure and acceptance criteria

### 7.1 `suburbs.html` — Suburbs index

**Sections:** MediaHero → intro line → SuburbCard grid (primary first) → appraisal CTA.

**SuburbCard:** hero image with `heroGrade` applied, suburb name (Zodiak), `intro` excerpt, listing count. `guideStatus:'live'` links to `suburb.html?r=<slug>`; `guideStatus:'soon'` renders as a non-interactive card with a quiet "Guide coming" label — no `href`, not focusable, no hover affordance.

**AC:**
- Carrara and Benowa Waters appear first and link through
- The eleven `soon` cards render but are not clickable and are skipped by keyboard tab order
- No horizontal scroll 375–1440px
- Grid collapses to 1-up on mobile
- Zero console errors

### 7.2 `suburb.html?r=<slug>` — Suburb Guide

**Sections:** MediaHero (suburb, graded) → name + `positioning` → `editorial` body → optional stats → scoped PropertyGrid → agent block → EnquiryForm → related suburbs.

**AC:**
- `editorial` is real prose, not lorem (BUILD-SPEC §8.5)
- Grid shows exactly that suburb's listings; thin-result state renders when count is 1
- FilterBar is suburb-locked and cannot be widened past the suburb
- EnquiryForm creates a Lead with `source:'enquiry'` and `relatedRegion:<slug>`
- Deep-linkable; unknown or `soon` slug redirects to `suburbs.html` rather than rendering an empty guide
- Related suburbs link only to `live` guides
- Carrara guide leads with the Boulevard suburb record; Benowa leads with the seller testimonial
- No volume figures, no always-on-site claims

### 7.3 `journal.html` — Journal index

**Sections:** MediaHero → JournalCard grid → appraisal CTA.

**AC:** renders correctly with only three articles (no broken empty grid); cards link to `article.html?a=<slug>`; no category filter this pass (three articles do not warrant one).

### 7.4 `article.html?a=<slug>` — Article

**Sections:** MediaHero → ArticleBody → byline → related → EnquiryForm CTA.

**AC:**
- Body measure 65–75ch at desktop
- Zodiak for title and pull-quote, Poppins for body
- Byline is Jason or Barbara, pulled from `getAgent()`
- Related links resolve; unknown slug redirects to `journal.html`
- No content hidden behind JS-only reveals

### 7.5 Global

- Nav, overlay menu and footer gain **Suburbs** and **Journal** across all six prototype pages, in the minimal uppercase chrome established by `1d41928`
- `aria-current` set correctly per page
- Reduced-motion honoured
- No dead `#` links
- Reveal animations must not gate content — the hidden-pane failsafe already in `app.js` applies (see the 2026-07-22 false-positive lesson in `wiki/log.md`)

---

## 8. Verification

Served on `localhost:8771`, checked at 375px and 1440px:

1. Zero console errors on all six pages
2. Zero dead links across the section
3. Carrara and Benowa guides each render a scoped listing
4. Suburb enquiry writes a Lead with `relatedRegion` set (logged)
5. `soon` cards are non-interactive and skipped by tab order
6. Article body measure within 65–75ch
7. Unknown `?r=` and `?a=` values redirect rather than rendering empty
8. Existing behaviour intact — Buy/Sold/Upcoming tabs, appraisal modal, lightbox, URL sync
9. Screenshot proof of both guides and one article

Verification runs in a visible browser pane. A hidden pane pauses CSS transitions and produces false `opacity:0` readings.

---

## 9. Open items (not blocking this pass)

- **§9 tier list not re-derived.** Carrara and Benowa were promoted on evidence; the remaining eleven keep their inferred tiers. If the evidenced footprint contradicts the prestige-pocket thesis more broadly, §9 needs a full rewrite — a separate decision.
- **Journal articles are drafts** pending Jason's approval.
- **Imagery remains the Somerset Drive placeholder set**, now reused more widely. `heroGrade` mitigates but does not solve this; real photography per suburb is the fix.
- **Stack still unsigned** — Path A (Next.js + Payload) vs Path B (WordPress + ACF + FacetWP). This pass stays stack-agnostic static HTML, so it does not force the decision.
- **The six originally-proposed primary guides** (Sovereign Islands, Mermaid Waters, Broadbeach Waters, Paradise Waters, Isle of Capri, Sanctuary Cove) ship by populating `editorial` and flipping `guideStatus`.

---

## 10. Out of scope

Everything in BUILD-SPEC §10 `[P3+]`, plus: category filtering on Journal, real photography sourcing, live CRM feed, and any change to the live WordPress site.
