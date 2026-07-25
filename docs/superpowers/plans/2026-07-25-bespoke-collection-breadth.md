# Bespoke Collection Breadth Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Suburbs index, two evidence-led Suburb Guides (Carrara, Benowa Waters), and a Journal index + Article template to the Bespoke Collection prototype, so a prospect can free-roam the section without reaching a placeholder.

**Architecture:** Static, dependency-free HTML/CSS/JS in `projects/bespoke-site/prototype/`. `app.js` currently traps every helper inside one IIFE with no exports; Task 2 opens a deliberate `window.BESPOKE` seam so the four new page controllers can live in a separate `editorial.js` instead of pushing `app.js` past 600 lines. Data stays in `data.js` behind the existing `getRegions`/`getListings` access layer, which remains the only swap point for Payload or WordPress later.

**Tech Stack:** Vanilla ES5-style JS (matching existing code), plain CSS layered over `../assets/css/main.css`, no build step, no package manager. Verification is a dependency-free `tests.html` assertion harness plus browser checks.

**Spec:** [2026-07-25-bespoke-collection-breadth-design.md](../specs/2026-07-25-bespoke-collection-breadth-design.md)

## Global Constraints

- **No test framework may be added.** No Node, npm, Jest, or build step. `tests.html` is the harness; it loads real source files and runs assertions in the browser.
- **Match existing code style exactly:** ES5 `var`, `function` declarations, string concatenation for HTML (no template literals), IIFE wrapper, `"use strict"`.
- **All user-facing copy: no em dashes.** Use commas, full stops, or "and". This is an established rule in this codebase.
- **No volume figures** (listing counts as marketing claims, "X sales this year") and **no always-on-site or founder-presence claims** in any copy.
- **No invented suburb records.** Only the Carrara Boulevard record is evidenced.
- **No media, photography, videography or marketing-service talk in client-facing editorial copy.** Bespoke's client voice is home-focused only.
- **Content must never be gated behind JS reveals.** `.reveal` is enhancement only; content is visible by default (`phase2.css:18-26`).
- **Reduced motion must be honoured** via the existing `@media(prefers-reduced-motion:reduce)` block.
- **No horizontal scroll between 375px and 1440px.**
- **Verification must run in a visible browser pane.** A hidden pane pauses CSS transitions and produces false `opacity:0` readings.
- **URL param convention:** `listing.html?id=<slug>`, `suburb.html?r=<slug>`, `article.html?a=<slug>`.
- **Do not modify** `projects/bespoke-site/index.html`, `services.html`, `projects.html` (the parent static site) or anything on the live WordPress site.

---

## File Structure

| File | Status | Responsibility |
|---|---|---|
| `prototype/data.js` | Modify | Seed data only. Region extensions, two listing reassignments, `ARTICLES`. |
| `prototype/app.js` | Modify | Data access, shared helpers, chrome, listings + listing detail + soon controllers. Gains a `window.BESPOKE` export block. |
| `prototype/editorial.js` | Create | The four new page controllers: suburbs index, suburb guide, journal index, article. Consumes `window.BESPOKE`. |
| `prototype/phase2.css` | Modify | Append SuburbCard, guide layout, JournalCard, article body blocks. |
| `prototype/suburbs.html` | Create | Suburbs index shell. |
| `prototype/suburb.html` | Create | Suburb guide shell, parameterised by `?r=`. |
| `prototype/journal.html` | Create | Journal index shell. |
| `prototype/article.html` | Create | Article shell, parameterised by `?a=`. |
| `prototype/tests.html` | Create | Dependency-free assertion harness for the data layer. |
| `prototype/tests.js` | Create | The assertions. |
| `prototype/index.html` | Modify | Nav, overlay menu additions. |
| `prototype/listing.html` | Modify | Nav, overlay menu additions. |
| `prototype/soon.html` | Modify | Nav, overlay menu additions. |

---

## Task 1: Test harness

**Files:**
- Create: `projects/bespoke-site/prototype/tests.html`
- Create: `projects/bespoke-site/prototype/tests.js`

**Interfaces:**
- Consumes: `window.BESPOKE_DATA` from `data.js`
- Produces: `window.T` with `T.eq(actual, expected, label)`, `T.ok(cond, label)`, `T.report()`. Later tasks add assertions to `tests.js`.

- [ ] **Step 1: Create the harness page**

Create `prototype/tests.html`:

```html
<!doctype html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <title>Bespoke prototype tests</title>
  <style>
    body{font:14px/1.6 ui-monospace,monospace;padding:24px;background:#111;color:#eee}
    .pass{color:#6ee7a8}.fail{color:#ff8a8a;font-weight:700}
    h1{font:600 18px/1.4 system-ui;margin:0 0 16px}
    #sum{margin-bottom:16px;padding:10px 14px;border:1px solid #333;display:inline-block}
  </style>
</head>
<body>
  <h1>Bespoke prototype, data layer tests</h1>
  <div id="sum">running</div>
  <div id="out"></div>
  <script src="data.js"></script>
  <script src="app.js"></script>
  <script src="editorial.js"></script>
  <script src="tests.js"></script>
</body>
</html>
```

Note: `editorial.js` does not exist until Task 2. Until then the browser logs a 404 for it and continues; that is expected and harmless.

- [ ] **Step 2: Create the assertion runner with one deliberately failing test**

Create `prototype/tests.js`:

```js
(function () {
  "use strict";
  var results = [], out = document.getElementById("out"), sum = document.getElementById("sum");
  var T = {
    eq: function (actual, expected, label) {
      var pass = JSON.stringify(actual) === JSON.stringify(expected);
      results.push({ pass: pass, label: label, detail: pass ? "" : "got " + JSON.stringify(actual) + ", expected " + JSON.stringify(expected) });
    },
    ok: function (cond, label) {
      results.push({ pass: !!cond, label: label, detail: cond ? "" : "expected truthy" });
    },
    report: function () {
      var failed = results.filter(function (r) { return !r.pass; });
      out.innerHTML = results.map(function (r) {
        return '<div class="' + (r.pass ? "pass" : "fail") + '">' + (r.pass ? "PASS" : "FAIL") + "  " + r.label + (r.detail ? "  (" + r.detail + ")" : "") + "</div>";
      }).join("");
      sum.textContent = results.length + " assertions, " + failed.length + " failed";
      sum.className = failed.length ? "fail" : "pass";
      console.log("[tests] " + results.length + " assertions, " + failed.length + " failed");
    }
  };
  window.T = T;

  // Sanity check that the harness itself reports failures.
  T.ok(false, "harness self-check, this MUST fail on first run");

  T.report();
})();
```

- [ ] **Step 3: Run it and confirm the harness reports the failure**

Start a preview server on the prototype directory and open `tests.html`.

Expected: page shows `1 assertions, 1 failed` and a red `FAIL  harness self-check, this MUST fail on first run`. Console logs `[tests] 1 assertions, 1 failed`.

This proves the harness cannot silently pass.

- [ ] **Step 4: Replace the self-check with a real passing assertion**

In `tests.js`, replace the self-check line with:

```js
  T.eq(window.BESPOKE_DATA.REGIONS.length, 13, "13 regions seeded");
  T.eq(window.BESPOKE_DATA.LISTINGS.length, 6, "6 listings seeded");
```

- [ ] **Step 5: Run and confirm both pass**

Reload `tests.html`.

Expected: `2 assertions, 0 failed`, both green.

- [ ] **Step 6: Commit**

```bash
git add projects/bespoke-site/prototype/tests.html projects/bespoke-site/prototype/tests.js
git commit -m "test(bespoke): dependency-free browser assertion harness for prototype data layer"
```

---

## Task 2: Open the `window.BESPOKE` seam

**Files:**
- Modify: `projects/bespoke-site/prototype/app.js:360-364` (the BOOT block)
- Create: `projects/bespoke-site/prototype/editorial.js`
- Modify: `projects/bespoke-site/prototype/tests.js`

**Interfaces:**
- Produces: `window.BESPOKE` exposing exactly these members, used by every later task:
  - `getRegions(filter)` — `filter` optional `{tier, guideStatus}`, returns `Region[]`
  - `getRegion(slug)` — returns `Region | null`
  - `getListings(filter)` — existing signature
  - `getListing(slug)`, `getAgent(id)`
  - `cardHTML(listing, delay)` — returns HTML string
  - `esc(str)`, `suburbName(slug)`, `priceLine(listing)`
  - `buildEnquiry(prefix, intro, submitLabel)` — returns HTML string
  - `wireForm(formEl, ctx)` — `ctx` is `{source, relatedListing, relatedRegion}`
  - `observeReveals()`
  - `agentRow(agent)`
  - `HERO_FALLBACK` — string URL

- [ ] **Step 1: Add the failing test for the seam**

Append to `tests.js` before `T.report()`:

```js
  T.ok(window.BESPOKE, "BESPOKE namespace exposed");
  ["getRegions","getRegion","getListings","getListing","getAgent","cardHTML","esc",
   "suburbName","priceLine","buildEnquiry","wireForm","observeReveals","agentRow"
  ].forEach(function (k) {
    T.ok(window.BESPOKE && typeof window.BESPOKE[k] === "function", "BESPOKE." + k + " is a function");
  });
  T.ok(window.BESPOKE && typeof window.BESPOKE.HERO_FALLBACK === "string", "BESPOKE.HERO_FALLBACK is a string");
```

- [ ] **Step 2: Run and confirm failures**

Reload `tests.html`.

Expected: 15 new FAIL lines, all reporting `expected truthy`. Total `17 assertions, 15 failed`.

- [ ] **Step 3: Export the namespace from `app.js`**

In `app.js`, replace the BOOT block at lines 360-364:

```js
  /* ------------------------------- BOOT ---------------------------------- */
  document.addEventListener("DOMContentLoaded", function () {
    initChrome(); initReveal(); initListings(); initListing(); initSoon();
  });
})();
```

with:

```js
  /* ------------------------------- EXPORTS -------------------------------- */
  /* The seam other page controllers consume (editorial.js). Data access still
     lives here so swapping to Payload/WP remains a single-file change. */
  window.BESPOKE = {
    getRegions: getRegions, getRegion: getRegion, getListings: getListings,
    getListing: getListing, getAgent: getAgent,
    cardHTML: cardHTML, esc: esc, suburbName: suburbName, priceLine: priceLine,
    buildEnquiry: buildEnquiry, wireForm: wireForm, observeReveals: observeReveals,
    agentRow: agentRow, HERO_FALLBACK: HERO_FALLBACK
  };

  /* ------------------------------- BOOT ---------------------------------- */
  document.addEventListener("DOMContentLoaded", function () {
    initChrome(); initReveal(); initListings(); initListing(); initSoon();
    if (window.BESPOKE_EDITORIAL) window.BESPOKE_EDITORIAL.boot();
  });
})();
```

- [ ] **Step 4: Create `editorial.js` with the boot stub**

Create `prototype/editorial.js`:

```js
/* ==========================================================================
   BESPOKE, editorial page controllers (Suburbs index, Suburb Guide,
   Journal index, Article). Consumes the window.BESPOKE seam from app.js;
   holds no data access of its own.
   ========================================================================== */
(function () {
  "use strict";
  var B = window.BESPOKE;

  function boot() {
    initSuburbs(); initSuburb(); initJournal(); initArticle();
  }

  function initSuburbs() {}
  function initSuburb() {}
  function initJournal() {}
  function initArticle() {}

  window.BESPOKE_EDITORIAL = { boot: boot };
})();
```

- [ ] **Step 5: Run and confirm all pass**

Reload `tests.html`.

Expected: `17 assertions, 0 failed`.

- [ ] **Step 6: Confirm no regression on the existing pages**

Open `index.html` and `listing.html?id=` in the visible browser pane.

Expected: listings grid still renders, filter tabs still switch, console has zero errors. `editorial.js` 404 is gone now that the file exists.

- [ ] **Step 7: Commit**

```bash
git add projects/bespoke-site/prototype/app.js projects/bespoke-site/prototype/editorial.js projects/bespoke-site/prototype/tests.js
git commit -m "refactor(bespoke): expose window.BESPOKE seam, add editorial.js controller module"
```

---

## Task 3: Region data extensions, listing reassignment, unearned claim removal

**Files:**
- Modify: `projects/bespoke-site/prototype/data.js:131-164` (REGIONS)
- Modify: `projects/bespoke-site/prototype/data.js:71-78` (34 Monaco Street listing)
- Modify: `projects/bespoke-site/prototype/data.js:101-115` (2101 / 45 Commodore Drive listing)
- Modify: `projects/bespoke-site/prototype/data.js:96` (Isle of Capri `suburbRecord`)
- Modify: `projects/bespoke-site/prototype/app.js:33` (`getRegions`)
- Modify: `projects/bespoke-site/prototype/tests.js`

**Interfaces:**
- Consumes: `window.BESPOKE` from Task 2
- Produces: `getRegions(filter)` accepting `{tier, guideStatus}`; Region objects carrying `positioning`, `editorial`, `heroGrade`, `stats`, `guideStatus`

- [ ] **Step 1: Write the failing tests**

Append to `tests.js` before `T.report()`:

```js
  var B = window.BESPOKE;

  // Carrara and Benowa promoted to primary, guides live.
  ["carrara", "benowa"].forEach(function (slug) {
    var r = B.getRegion(slug);
    T.eq(r && r.tier, "primary", slug + " is primary tier");
    T.eq(r && r.guideStatus, "live", slug + " guide is live");
    T.ok(r && typeof r.positioning === "string" && r.positioning.length > 10, slug + " has a positioning line");
    T.ok(r && Array.isArray(r.editorial) && r.editorial.length >= 2, slug + " has editorial paragraphs");
    T.ok(r && typeof r.heroGrade === "string", slug + " has a heroGrade");
  });

  // Every other region is 'soon'.
  T.eq(B.getRegions({ guideStatus: "live" }).length, 2, "exactly 2 live guides");
  T.eq(B.getRegions({ guideStatus: "soon" }).length, 11, "11 soon guides");
  T.ok(B.getRegions().every(function (r) { return typeof r.heroGrade === "string"; }), "all regions have heroGrade");

  // getRegions filtering.
  T.ok(B.getRegions({ tier: "primary" }).every(function (r) { return r.tier === "primary"; }), "tier filter returns only primary");
  T.eq(B.getRegions().length, 13, "unfiltered getRegions still returns 13");

  // Listings reassigned so live guides are not empty.
  T.eq(B.getListings({ status: "buy", suburb: "carrara" }).length
     + B.getListings({ status: "sold", suburb: "carrara" }).length
     + B.getListings({ status: "upcoming", suburb: "carrara" }).length, 1, "carrara has 1 listing");
  T.eq(B.getListings({ status: "buy", suburb: "benowa" }).length
     + B.getListings({ status: "sold", suburb: "benowa" }).length
     + B.getListings({ status: "upcoming", suburb: "benowa" }).length, 1, "benowa has 1 listing");

  // No invented suburb record survives.
  T.eq(window.BESPOKE_DATA.LISTINGS.filter(function (l) {
    return l.soldData && l.soldData.suburbRecord === true;
  }).length, 0, "no seed listing claims a suburb record");
```

- [ ] **Step 2: Run and confirm failures**

Reload `tests.html`.

Expected: the Carrara/Benowa tier, guideStatus, positioning, editorial, heroGrade, live/soon count, listing count and suburbRecord assertions all FAIL.

- [ ] **Step 3: Extend `getRegions` in `app.js`**

Replace line 33:

```js
  function getRegions() { return D.REGIONS.slice(); }
```

with:

```js
  function getRegions(f) {
    f = f || {};
    return D.REGIONS.filter(function (r) {
      if (f.tier && r.tier !== f.tier) return false;
      if (f.guideStatus && r.guideStatus !== f.guideStatus) return false;
      return true;
    });
  }
```

Note: `initListings` at `app.js:215` calls `getRegions()` with no argument to populate the suburb dropdown. That still returns all 13. No change needed there.

- [ ] **Step 4: Remove the invented suburb record**

In `data.js:96`, change:

```js
      soldData:{ date:"2026-05-14", price:3850000, suburbRecord:true }, externalId:null,
```

to:

```js
      soldData:{ date:"2026-05-14", price:3850000, suburbRecord:false }, externalId:null,
```

- [ ] **Step 5: Reassign the two listings**

In `data.js:71`, change the 34 Monaco Street address from Broadbeach Waters to Benowa Waters:

```js
      address:{ street:"34 Monaco Street", suburb:"broadbeach-waters", state:"QLD", postcode:"4218" },
```

becomes:

```js
      address:{ street:"18 Wattlebird Place", suburb:"benowa", state:"QLD", postcode:"4217" },
```

Then in `data.js:79`, replace the Broadbeach-specific description with Benowa-appropriate copy (the third paragraph names the suburb):

```js
      description:["A generous family residence on a main-river-adjacent canal, presented in move-in condition. The ground floor is designed for entertaining, with a butler's pantry serving both the kitchen and the outdoor kitchen beyond.","Upstairs, four bedrooms open to a central retreat, with the primary suite taking the full water-facing width.","Central to Benowa's established streets, with the golf course, gardens and river all within a short drive."],
```

In `data.js:101`, change the Commodore Drive apartment to a Carrara house:

```js
      address:{ street:"2101 / 45 Commodore Drive", suburb:"paradise-waters", state:"QLD", postcode:"4217" },
```

becomes:

```js
      address:{ street:"9 Emerald Rise", suburb:"carrara", state:"QLD", postcode:"4211" },
```

Also update that listing's `slug`, `propertyType` and `seo.title` to match. Read lines 101-115 and change:
- `slug` to `9-emerald-rise-carrara`
- `propertyType` from `"apartment"` to `"house"`
- `seo.title` to `"9 Emerald Rise, Carrara"`
- any description paragraph naming Paradise Waters, Main Beach, the Broadwater, Tedder Avenue or the spit, rewritten for Carrara (green heart of the coast, lake and parkland aspect, room and privacy close to the motorway and the coast)

Keep `beds`, `baths`, `cars`, `price`, `status` and gallery unchanged.

- [ ] **Step 6: Extend the REGIONS entries for Carrara and Benowa**

In `data.js`, replace the `r9` (Benowa Waters) entry:

```js
    { id:"r9", slug:"benowa", name:"Benowa Waters", tier:"secondary", order:9, hero:media(IMG.i7,"Benowa Waters"),
      intro:"Central and established, with generous blocks and mature streetscapes. Benowa Waters offers waterfront living close to the heart of the coast." },
```

with:

```js
    { id:"r9", slug:"benowa", name:"Benowa Waters", tier:"primary", order:2, guideStatus:"live", heroGrade:"warm",
      hero:media(IMG.i7,"Benowa Waters"),
      intro:"Central and established, with generous blocks and mature streetscapes. Benowa Waters offers waterfront living close to the heart of the coast.",
      positioning:"Established, central, and quietly held.",
      stats:[{label:"Character",value:"Established waterfront"},{label:"Buyer",value:"Families settling in"},{label:"Aspect",value:"River and canal"}],
      editorial:[] },
```

Replace the `r10` (Carrara) entry:

```js
    { id:"r10", slug:"carrara", name:"Carrara", tier:"secondary", order:10, hero:media(IMG.i33,"Carrara"),
      intro:"Acreage and hidden prestige pockets in the green heart of the Gold Coast, with room and privacy rarely found this close to the coast." },
```

with:

```js
    { id:"r10", slug:"carrara", name:"Carrara", tier:"primary", order:1, guideStatus:"live", heroGrade:"cool",
      hero:media(IMG.i33,"Carrara"),
      intro:"Acreage and hidden prestige pockets in the green heart of the Gold Coast, with room and privacy rarely found this close to the coast.",
      positioning:"The green heart of the coast, with room to breathe.",
      stats:[{label:"Character",value:"Acreage and lakes"},{label:"Buyer",value:"Space over frontage"},{label:"Aspect",value:"Parkland and water"}],
      editorial:[] },
```

`editorial` is filled in Task 7. The empty array keeps the shape correct now, and the Task 3 test only asserts `editorial.length >= 2` for these two, so **that assertion will still fail until Task 7**. Change the two `editorial` assertions in `tests.js` to check the property exists as an array for now:

```js
    T.ok(r && Array.isArray(r.editorial), slug + " has an editorial array");
```

Task 7 tightens it back to `length >= 2`.

- [ ] **Step 7: Add `guideStatus` and `heroGrade` to the remaining eleven regions**

For every other REGIONS entry (`r1` through `r8`, `r11`, `r12`, `r13`), add `guideStatus:"soon"` and a `heroGrade` value. Assign grades so adjacent cards in the grid differ, since all regions reuse the same small Somerset Drive image set:

- `r1` sovereign-islands: `heroGrade:"deep"`
- `r2` mermaid-waters: `heroGrade:"cool"`
- `r3` broadbeach-waters: `heroGrade:"neutral"`
- `r4` paradise-waters: `heroGrade:"warm"`
- `r5` isle-of-capri: `heroGrade:"cool"`
- `r6` sanctuary-cove: `heroGrade:"deep"`
- `r7` main-beach: `heroGrade:"warm"`
- `r8` clear-island-waters: `heroGrade:"neutral"`
- `r11` surfers-paradise: `heroGrade:"deep"`
- `r12` runaway-bay: `heroGrade:"cool"`
- `r13` currumbin-valley: `heroGrade:"warm"`

Leave their `tier` and `order` values unchanged. Carrara and Benowa taking `order` 1 and 2 means `r1` and `r2` now share those numbers with them; sort is by tier first then order, and duplicate order values inside the secondary tier are harmless. Do not renumber.

- [ ] **Step 8: Run and confirm all pass**

Reload `tests.html`.

Expected: all assertions pass. Total is 17 from earlier tasks plus 17 new, `34 assertions, 0 failed`.

- [ ] **Step 9: Confirm the listings page still works**

Open `index.html` in the visible browser pane. Switch to the Sold tab. Select Carrara in the suburb dropdown.

Expected: zero console errors; the Sold tab no longer shows a "Suburb Record" marker anywhere; selecting Carrara on the Buy tab shows the reassigned listing or an empty state, both acceptable depending on that listing's status.

- [ ] **Step 10: Commit**

```bash
git add projects/bespoke-site/prototype/data.js projects/bespoke-site/prototype/app.js projects/bespoke-site/prototype/tests.js
git commit -m "feat(bespoke): promote Carrara + Benowa to primary, extend Region shape, drop invented suburb record"
```

---

## Task 4: Articles data and access

**Files:**
- Modify: `projects/bespoke-site/prototype/data.js` (add `ARTICLES`, extend the `BESPOKE_DATA` export at line 166)
- Modify: `projects/bespoke-site/prototype/app.js` (add `getArticles`, `getArticle`, extend the exports block)
- Modify: `projects/bespoke-site/prototype/tests.js`

**Interfaces:**
- Produces: `B.getArticles()` returning `Article[]` newest first; `B.getArticle(slug)` returning `Article | null`. Article shape: `{id, slug, title, dek, category, author, date, hero, body, pullQuote, related}` where `author` is an AGENTS key, `body` is `string[]`, `related` is `slug[]`.

- [ ] **Step 1: Write the failing tests**

Append to `tests.js` before `T.report()`:

```js
  T.ok(typeof B.getArticles === "function", "B.getArticles is a function");
  T.ok(typeof B.getArticle === "function", "B.getArticle is a function");
  T.eq(B.getArticles().length, 3, "3 articles seeded");
  T.eq(B.getArticle("nope"), null, "unknown article slug returns null");
  B.getArticles().forEach(function (a) {
    T.ok(a.slug && a.title && a.dek, a.slug + " has slug, title, dek");
    T.ok(Array.isArray(a.body) && a.body.length >= 3, a.slug + " has 3+ body paragraphs");
    T.ok(B.getAgent(a.author), a.slug + " author resolves to an agent");
    T.ok(a.related.every(function (s) { return B.getArticle(s) !== null; }), a.slug + " related slugs all resolve");
    T.ok(a.body.join(" ").indexOf("—") === -1, a.slug + " body has no em dashes");
    T.ok(a.title.indexOf("—") === -1, a.slug + " title has no em dashes");
  });
  // Newest first.
  var dates = B.getArticles().map(function (a) { return a.date; });
  T.eq(dates.slice().sort().reverse(), dates, "articles sorted newest first");
```

- [ ] **Step 2: Run and confirm failures**

Reload `tests.html`. Expected: `B.getArticles is not a function` failures and the count assertion failing.

- [ ] **Step 3: Add the ARTICLES collection to `data.js`**

Insert after the REGIONS array, before the `w.BESPOKE_DATA` line. Copy is written in Jason and Barbara's client voice: understated, home-focused, no media or marketing-service talk, no volume figures, no em dashes.

```js
  var ARTICLES = [
    { id:"a1", slug:"what-off-market-really-means", date:"2026-06-18",
      title:"What off market really means",
      dek:"The phrase gets used loosely. Here is what it actually looks like when a home sells quietly, and when it is the right choice.",
      category:"Selling", author:"jason", hero:media(IMG.i15,"A quiet Gold Coast street"),
      pullQuote:"A quiet campaign is a choice about who sees the home, not a shortcut to a faster result.",
      body:[
        "Off market is one of those phrases that has drifted. Used properly it means a home is offered to a considered group of buyers rather than listed publicly. No portal, no signboard, no open homes with strangers moving through the hallway on a Saturday morning.",
        "The reason a seller chooses it is almost never price. It is usually privacy. A family who would rather their neighbours did not know, a home with tenants who deserve some peace, or an owner who simply does not want their living room on the internet.",
        "It works when the buyer pool for a home is genuinely small and genuinely known. A tightly held street, a particular kind of frontage, a floor plan that suits one sort of family. In that situation a quiet approach reaches the right people faster than a public campaign would.",
        "It works less well when a home would benefit from competition. If several buyers might want it, keeping them apart rarely helps the seller. That is a conversation worth having honestly before anything is decided.",
        "The right answer depends on the home and on what the owner actually wants from the process. Both paths are legitimate. What matters is choosing deliberately rather than by default."
      ],
      related:["preparing-a-waterfront-home","reading-a-suburb-record"] },

    { id:"a2", slug:"preparing-a-waterfront-home", date:"2026-05-02",
      title:"Preparing a waterfront home for market",
      dek:"Waterfront homes are judged differently. A short, practical list of what genuinely matters before a home is offered.",
      category:"Selling", author:"jason", hero:media(IMG.drone2,"Canal frontage on the Gold Coast"),
      pullQuote:"Buyers looking at waterfront are buying the water first and the house second.",
      body:[
        "Buyers looking at waterfront are buying the water first and the house second. Everything that sits between the living room and the canal is doing more work than it does in a standard home, and it is worth attending to before anything else.",
        "Start with the sightline. Anything that interrupts the view from the main living space to the water is worth reconsidering, whether that is a screen, a planter, a stored item on the terrace, or an outdoor setting that is simply too large for the space it occupies.",
        "Then the frontage itself. Pontoons, retaining walls and revetment walls all age, and buyers of these homes know it. Knowing the condition and the paperwork before you are asked is far better than being asked and not knowing.",
        "Inside, the north facing rooms carry the home. Salt air is hard on window frames, tracks and hardware, and sliding doors that do not run smoothly get noticed immediately in a home at this level.",
        "None of this is cosmetic in the usual sense. It is about removing the small doubts that accumulate while someone is standing in a room deciding whether they can see themselves living there."
      ],
      related:["what-off-market-really-means","reading-a-suburb-record"] },

    { id:"a3", slug:"reading-a-suburb-record", date:"2026-03-14",
      title:"Reading a suburb record",
      dek:"A record price tells you something, but rarely what people assume. How to read one properly.",
      category:"Market", author:"barbara", hero:media(IMG.i25,"An established Gold Coast streetscape"),
      pullQuote:"A record is one house on one day, not a new floor under every home on the street.",
      body:[
        "A suburb record makes for a clean headline, and it is worth understanding what sits underneath it before drawing conclusions about your own home.",
        "A record is one house on one day. It reflects that specific home, its position, its condition, and the particular buyer who wanted it most. It does not lift every home on the street by the same margin, and treating it as a new baseline usually leads to disappointment.",
        "Records are also category specific. A record for a house is not a record for an apartment, and a record for a canal frontage block is not a record for a dry block two streets back. When you see one quoted, the useful question is always which category it belongs to.",
        "What a record does tell you is that demand at the top of a market is real and that a buyer was prepared to act. That is genuinely useful information about depth, and it matters more in a suburb where very little trades.",
        "The more reliable guide for an individual home is the pattern underneath the record. What has sold, how long it took, and how closely the results cluster. That is a less dramatic picture, and a far more accurate one."
      ],
      related:["what-off-market-really-means","preparing-a-waterfront-home"] }
  ];
```

- [ ] **Step 4: Extend the data export**

Change `data.js:166`:

```js
  w.BESPOKE_DATA = { LISTINGS: LISTINGS, REGIONS: REGIONS, AGENTS: AGENTS };
```

to:

```js
  w.BESPOKE_DATA = { LISTINGS: LISTINGS, REGIONS: REGIONS, AGENTS: AGENTS, ARTICLES: ARTICLES };
```

- [ ] **Step 5: Add the access functions to `app.js`**

After `getRegion` (line 34), add:

```js
  function getArticles() {
    return D.ARTICLES.slice().sort(function (a, b) { return b.date.localeCompare(a.date); });
  }
  function getArticle(slug) { return D.ARTICLES.filter(function (a) { return a.slug === slug; })[0] || null; }
```

Add both to the exports block created in Task 2:

```js
    getArticles: getArticles, getArticle: getArticle,
```

- [ ] **Step 6: Verify the author keys match AGENTS**

Read the `AGENTS` object in `data.js` and confirm the keys used above (`jason`, `barbara`) are the actual keys. If they differ, update the `author` values in ARTICLES to match. Do not change `AGENTS`.

- [ ] **Step 7: Run and confirm all pass**

Reload `tests.html`. Expected: `0 failed`.

- [ ] **Step 8: Commit**

```bash
git add projects/bespoke-site/prototype/data.js projects/bespoke-site/prototype/app.js projects/bespoke-site/prototype/tests.js
git commit -m "feat(bespoke): seed 3 evergreen Journal articles + getArticles/getArticle access"
```

---

## Task 5: Suburbs index

**Files:**
- Create: `projects/bespoke-site/prototype/suburbs.html`
- Modify: `projects/bespoke-site/prototype/editorial.js` (`initSuburbs`)
- Modify: `projects/bespoke-site/prototype/phase2.css` (append)

**Interfaces:**
- Consumes: `B.getRegions(filter)`, `B.getListings`, `B.esc`, `B.observeReveals`
- Produces: `suburbCardHTML(region, delay)` inside `editorial.js`, reused by the related-suburbs block in Task 6

- [ ] **Step 1: Create the page shell**

Create `prototype/suburbs.html`. Copy the full `<head>`, `<header>` and `<div class="site-menu">` blocks verbatim from `index.html:1-45`, then change:
- `<title>` to `Suburb Guides | Bespoke Estate Agents | Gold Coast Prestige Property`
- `<meta name="description">` to `Guides to the Gold Coast suburbs Bespoke Estate Agents works, with current listings and local context for each.`
- remove `aria-current="page"` from the Collection nav link

Body content:

```html
  <main id="suburbs" class="stack-page" style="padding-top:0">
    <section class="p-hero">
      <div class="p-hero__media"><img src="https://bespoke.agents.10xvisuals.co/wp-content/uploads/2026/07/47-Somersert-Drive-_-Print-Drone-2-scaled.jpg" alt="Gold Coast waterfront suburb from above"></div>
      <div class="wrap">
        <span class="eyebrow on-dark">Suburbs</span>
        <h1>The pockets we work.</h1>
        <p>Every suburb on the coast reads differently. These are the ones we know street by street.</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="sub-head">
          <span class="eyebrow" style="margin:0">Guides</span>
        </div>
        <div class="sub-grid" id="sub-grid"></div>
      </div>
    </section>

    <section class="section section--green">
      <div class="wrap center prose">
        <h2 class="reveal">Not sure which pocket suits you?</h2>
        <p class="reveal" data-d="1" style="margin:16px auto 0;color:var(--be-grey-300)">A quiet conversation about what you are after, and where it is most likely to be found.</p>
        <div class="btn-row reveal" data-d="2" style="justify-content:center;margin-top:var(--sp-xl)"><a class="btn btn--light" href="soon.html?s=appraisal" data-appraisal>Book a Private Appraisal</a></div>
      </div>
    </section>
  </main>

  <footer class="site-footer" data-footer></footer>

  <script src="data.js"></script>
  <script src="app.js"></script>
  <script src="editorial.js"></script>
```

- [ ] **Step 2: Implement `suburbCardHTML` and `initSuburbs`**

In `editorial.js`, replace the `initSuburbs` stub:

```js
  function listingCount(slug) {
    return B.getListings({ status: "buy", suburb: slug }).length +
           B.getListings({ status: "sold", suburb: slug }).length +
           B.getListings({ status: "upcoming", suburb: slug }).length;
  }

  function suburbCardHTML(r, delay) {
    var live = r.guideStatus === "live", n = listingCount(r.slug);
    var inner =
      '<div class="sub-card__media grade--' + r.heroGrade + '">' +
        (live ? "" : '<span class="sub-card__soon">Guide coming</span>') +
        '<img src="' + r.hero.url + '" alt="' + B.esc(r.hero.alt) + '" loading="lazy">' +
      '</div>' +
      '<div class="sub-card__body">' +
        '<h3>' + B.esc(r.name) + '</h3>' +
        '<p>' + B.esc(r.intro) + '</p>' +
        '<span class="sub-card__meta">' + (n ? n + (n === 1 ? " listing" : " listings") : "No current listings") + '</span>' +
      '</div>';
    var cls = "sub-card reveal" + (live ? "" : " is-soon");
    var d = delay ? ' data-d="' + delay + '"' : "";
    return live
      ? '<a class="' + cls + '"' + d + ' href="suburb.html?r=' + encodeURIComponent(r.slug) + '">' + inner + '</a>'
      : '<div class="' + cls + '"' + d + ' aria-disabled="true">' + inner + '</div>';
  }

  function initSuburbs() {
    var grid = document.getElementById("sub-grid");
    if (!grid) return;
    var live = B.getRegions({ guideStatus: "live" }).sort(byOrder);
    var soon = B.getRegions({ guideStatus: "soon" }).sort(byOrder);
    grid.innerHTML = live.concat(soon).map(function (r, i) {
      return suburbCardHTML(r, (i % 3) + 1);
    }).join("");
    B.observeReveals();
  }

  function byOrder(a, b) {
    var t = { primary: 0, secondary: 1 };
    if (t[a.tier] !== t[b.tier]) return t[a.tier] - t[b.tier];
    return a.order - b.order;
  }
```

`soon` cards are a `<div>`, not an `<a>`, so they carry no `href` and are not in tab order. That satisfies the acceptance criterion without needing `tabindex="-1"`.

- [ ] **Step 3: Append the CSS**

Add to the end of `phase2.css`:

```css
/* ==========================================================================
   SUBURB CARDS + INDEX
   heroGrade exists because all suburbs reuse one placeholder image set.
   Per-suburb tonal treatment reads as house style, not a repeated file.
   ========================================================================== */
.sub-head{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:var(--sp-xl);}
.sub-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--sp-xl);}
@media(max-width:1024px){.sub-grid{grid-template-columns:repeat(2,1fr);}}
@media(max-width:640px){.sub-grid{grid-template-columns:1fr;}}

.sub-card{display:block;color:inherit;}
.sub-card__media{position:relative;aspect-ratio:4/3;overflow:hidden;background:var(--be-grey-200);}
.sub-card__media img{width:100%;height:100%;object-fit:cover;
  transition:transform .8s var(--be-ease-expo),filter .5s var(--ease);}
a.sub-card:hover .sub-card__media img{transform:scale(1.04);}

.grade--warm img{filter:saturate(1.04) contrast(1.02) sepia(.06);}
.grade--cool img{filter:saturate(.94) contrast(1.05) hue-rotate(-6deg);}
.grade--neutral img{filter:saturate(1) contrast(1.01);}
.grade--deep img{filter:saturate(.9) contrast(1.1) brightness(.94);}

.sub-card__body{padding-top:var(--sp-md);}
.sub-card__body h3{font:300 1.45rem/1.25 var(--be-font-head);color:var(--be-charcoal);}
.sub-card__body p{margin-top:8px;color:var(--be-grey-600);font-size:.94rem;max-width:44ch;}
.sub-card__meta{display:block;margin-top:12px;font:500 .72rem/1 var(--be-font-body);
  letter-spacing:.1em;text-transform:uppercase;color:var(--be-grey-600);}

.sub-card.is-soon{cursor:default;}
.sub-card.is-soon .sub-card__media img{filter:grayscale(.55) brightness(.9);}
.sub-card.is-soon .sub-card__body h3{color:var(--be-grey-600);}
.sub-card__soon{position:absolute;left:14px;top:14px;z-index:2;
  font:500 .66rem/1 var(--be-font-body);letter-spacing:.12em;text-transform:uppercase;
  padding:7px 12px;background:rgba(13,31,26,.72);color:var(--be-off-white);backdrop-filter:blur(4px);}
```

If `--be-font-head`, `--be-grey-200`, `--be-grey-600`, `--be-charcoal` or `--ease` do not exist under those names, grep `../assets/css/main.css` for the real token names and use those. Do not invent new tokens.

- [ ] **Step 4: Verify in the visible browser pane**

Open `suburbs.html`.

Expected:
- Carrara and Benowa Waters render first, as clickable cards, in colour
- Eleven further cards render desaturated with a "Guide coming" label
- Clicking a `soon` card does nothing
- Pressing Tab repeatedly moves through nav, the two live cards, then the CTA, skipping all eleven `soon` cards
- Zero console errors

Run in the console to confirm tab order:

```js
document.querySelectorAll('.sub-card[href]').length
```

Expected output: `2`

- [ ] **Step 5: Check both breakpoints**

Resize to 375px, then 1440px.

Expected: 1-up grid at 375px, 3-up at 1440px, no horizontal scroll at either. Confirm with:

```js
document.documentElement.scrollWidth <= window.innerWidth
```

Expected output: `true`

- [ ] **Step 6: Commit**

```bash
git add projects/bespoke-site/prototype/suburbs.html projects/bespoke-site/prototype/editorial.js projects/bespoke-site/prototype/phase2.css
git commit -m "feat(bespoke): Suburbs index with live/soon SuburbCards and per-suburb hero grades"
```

---

## Task 6: Suburb Guide template

**Files:**
- Create: `projects/bespoke-site/prototype/suburb.html`
- Modify: `projects/bespoke-site/prototype/editorial.js` (`initSuburb`)
- Modify: `projects/bespoke-site/prototype/phase2.css` (append)

**Interfaces:**
- Consumes: `B.getRegion`, `B.getRegions`, `B.getListings`, `B.cardHTML`, `B.esc`, `B.getAgent`, `B.agentRow`, `B.buildEnquiry`, `B.wireForm`, `B.observeReveals`, `suburbCardHTML` from Task 5

- [ ] **Step 1: Create the shell**

Create `prototype/suburb.html` with the same `<head>`/`<header>`/menu blocks as `suburbs.html` (title `Suburb Guide | Bespoke Estate Agents`, set properly by JS), and body:

```html
  <main id="suburb-guide" class="stack-page" style="padding-top:0"></main>
  <footer class="site-footer" data-footer></footer>
  <script src="data.js"></script>
  <script src="app.js"></script>
  <script src="editorial.js"></script>
```

- [ ] **Step 2: Implement `initSuburb`**

Replace the stub in `editorial.js`:

```js
  function initSuburb() {
    var root = document.getElementById("suburb-guide");
    if (!root) return;
    var slug = new URLSearchParams(location.search).get("r");
    var r = slug && B.getRegion(slug);
    // Unknown slug, or a suburb whose guide is not written yet, goes back to the index
    // rather than rendering an empty guide (spec AC).
    if (!r || r.guideStatus !== "live") { location.replace("suburbs.html"); return; }

    document.title = r.name + " Suburb Guide | Bespoke Estate Agents";
    var listings = B.getListings({ status: "buy", suburb: r.slug })
      .concat(B.getListings({ status: "upcoming", suburb: r.slug }))
      .concat(B.getListings({ status: "sold", suburb: r.slug }));
    var jason = B.getAgent("jason"), barbara = B.getAgent("barbara");
    var related = B.getRegions({ guideStatus: "live" }).filter(function (x) { return x.slug !== r.slug; });

    root.innerHTML =
      '<section class="p-hero"><div class="p-hero__media grade--' + r.heroGrade + '">' +
        '<img src="' + r.hero.url + '" alt="' + B.esc(r.hero.alt) + '"></div>' +
        '<div class="wrap"><span class="eyebrow on-dark">Suburb Guide</span>' +
        '<h1>' + B.esc(r.name) + '</h1><p>' + B.esc(r.positioning) + '</p></div></section>' +

      '<section class="section"><div class="wrap guide-cols">' +
        '<div class="guide-body reveal">' +
          r.editorial.map(function (p) { return "<p>" + B.esc(p) + "</p>"; }).join("") +
        '</div>' +
        (r.stats && r.stats.length
          ? '<aside class="guide-stats reveal" data-d="1">' + r.stats.map(function (s) {
              return '<div class="guide-stat"><span class="k">' + B.esc(s.label) + '</span><span class="v">' + B.esc(s.value) + '</span></div>';
            }).join("") + '</aside>'
          : "") +
      '</div></section>' +

      '<section class="section section--offwhite"><div class="wrap">' +
        '<div class="sub-head"><span class="eyebrow" style="margin:0">In ' + B.esc(r.name) + '</span>' +
        '<a class="muted" href="index.html?suburb=' + encodeURIComponent(r.slug) + '" style="text-decoration:underline;text-underline-offset:4px">Open in the full collection</a></div>' +
        (listings.length
          ? '<div class="p-grid">' + listings.map(function (l, i) { return B.cardHTML(l, (i % 3) + 1); }).join("") + '</div>' +
            (listings.length < 3 ? '<p class="muted guide-thin">A small number of homes are offered here at any one time. Speak with us about what is coming.</p>' : "")
          : '<div class="p-empty"><h3>Nothing is currently offered in ' + B.esc(r.name) + '.</h3><p class="muted">Homes here trade quietly. Register your interest and we will be in touch when something suits.</p></div>') +
      '</div></section>' +

      '<section class="section"><div class="wrap guide-cols">' +
        '<div class="reveal"><span class="eyebrow">Your agents</span>' +
          '<div class="agent-card">' + B.agentRow(jason) + B.agentRow(barbara) + '</div></div>' +
        '<aside class="reveal" data-d="1"><form class="enquiry" novalidate>' +
          B.buildEnquiry("g-", "Ask about " + B.esc(r.name) + ".", "Send enquiry") +
        '</form></aside>' +
      '</div></section>' +

      (related.length
        ? '<section class="section section--offwhite"><div class="wrap">' +
            '<div class="sub-head"><span class="eyebrow" style="margin:0">Other guides</span></div>' +
            '<div class="sub-grid">' + related.map(function (x, i) { return suburbCardHTML(x, i + 1); }).join("") + '</div>' +
          '</div></section>'
        : "");

    B.wireForm(root.querySelector(".enquiry"), { source: "enquiry", relatedRegion: r.slug });
    B.observeReveals();
  }
```

Related suburbs are drawn from `guideStatus:"live"` only, so they never link to an unwritten guide.

- [ ] **Step 3: Append the CSS**

```css
/* ==========================================================================
   SUBURB GUIDE
   ========================================================================== */
.guide-cols{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:var(--sp-4xl);align-items:start;}
@media(max-width:900px){.guide-cols{grid-template-columns:1fr;gap:var(--sp-xl);}}
.guide-body p{max-width:var(--read);color:var(--be-grey-600);margin-bottom:var(--sp-md);font-size:1.02rem;}
.guide-body p:first-child{font-size:1.16rem;color:var(--be-charcoal);}
.guide-stats{border-top:1px solid var(--be-line);}
.guide-stat{display:flex;justify-content:space-between;gap:16px;
  padding:14px 0;border-bottom:1px solid var(--be-line);}
.guide-stat .k{font:500 .72rem/1.4 var(--be-font-body);letter-spacing:.1em;
  text-transform:uppercase;color:var(--be-grey-600);}
.guide-stat .v{font:400 .94rem/1.4 var(--be-font-body);color:var(--be-charcoal);text-align:right;}
.guide-thin{margin-top:var(--sp-lg);max-width:52ch;}
```

- [ ] **Step 4: Verify both guides render**

Open `suburb.html?r=carrara`, then `suburb.html?r=benowa`.

Expected on each: hero with the suburb name and positioning line, editorial paragraphs visible, three stat rows, a listings grid with one card plus the thin-results line, agent card with both agents, enquiry form, and one "Other guides" card linking to the other live suburb. Zero console errors.

- [ ] **Step 5: Verify the redirects**

Open `suburb.html?r=sovereign-islands` (a `soon` guide), then `suburb.html?r=nonsense`, then `suburb.html` with no param.

Expected: all three land on `suburbs.html`. No empty guide is ever rendered.

- [ ] **Step 6: Verify the Lead payload**

On `suburb.html?r=carrara`, fill the enquiry form with a valid name, a valid email, tick consent, and submit. Read the console.

Expected: `[Bespoke] Lead captured:` with `source: "enquiry"`, `relatedRegion: "carrara"`, `relatedListing: null`.

- [ ] **Step 7: Check 375px**

Expected: columns stack, no horizontal scroll. Confirm with `document.documentElement.scrollWidth <= window.innerWidth` returning `true`.

- [ ] **Step 8: Commit**

```bash
git add projects/bespoke-site/prototype/suburb.html projects/bespoke-site/prototype/editorial.js projects/bespoke-site/prototype/phase2.css
git commit -m "feat(bespoke): Suburb Guide template with scoped listings, stats, relatedRegion enquiry"
```

---

## Task 7: Carrara and Benowa editorial content

**Files:**
- Modify: `projects/bespoke-site/prototype/data.js` (the `editorial` arrays on `r9` and `r10`)
- Modify: `projects/bespoke-site/prototype/tests.js`

**Interfaces:** none new.

- [ ] **Step 1: Tighten the editorial assertions**

In `tests.js`, change the Task 3 editorial assertion back to a real check and add a word count plus a claims guard:

```js
    T.ok(r && Array.isArray(r.editorial) && r.editorial.length >= 3, slug + " has 3+ editorial paragraphs");
    var words = (r ? r.editorial.join(" ").split(/\s+/).length : 0);
    T.ok(words >= 150 && words <= 260, slug + " editorial is 150 to 260 words (got " + words + ")");
    T.ok(r && r.editorial.join(" ").indexOf("—") === -1, slug + " editorial has no em dashes");
```

- [ ] **Step 2: Run and confirm failures**

Reload `tests.html`. Expected: both suburbs fail the paragraph count and word count assertions (`editorial` is still `[]`).

- [ ] **Step 3: Write the Carrara editorial**

Set `r10.editorial` in `data.js`. This leads with the one genuinely evidenced result Bespoke holds. No volume figures, no always-on-site claims, no media talk, no em dashes.

```js
      editorial:[
        "Carrara sits in the green middle of the Gold Coast, and it does not behave like the suburbs on either side of it. There is no beach and no glitter strip. What there is instead is land, and a set of quiet pockets that most buyers drive past without registering.",
        "The suburb runs from acreage along the Nerang River through to the lake estates, and the range within it is wide. A buyer can find a family home on a conventional block a few streets from a home on a full acre. That variety is the reason Carrara rewards knowing it properly rather than reading it off a portal.",
        "The buyers who end up here are usually choosing space over frontage. Room for the kids, room for the boat and the trailer, a shed that is actually useful, and a commute that still works in both directions. It suits people who want the coast nearby rather than underfoot.",
        "We hold the suburb record for a one bedroom residence in Carrara, which tells you something about how this market behaves. A well presented home in the right pocket can find a buyer who is prepared to move decisively, in a category most people would not expect it in.",
        "If you are considering Carrara, the streets matter more here than almost anywhere else on the coast. We are happy to walk you through which ones, and why."
      ] },
```

- [ ] **Step 4: Write the Benowa Waters editorial**

Set `r9.editorial`. Grounded in the seller testimonial Bespoke holds, without quoting or overstating it.

```js
      editorial:[
        "Benowa Waters is central in a way that is easy to underrate. It sits close to the middle of the Gold Coast, with the river on one side, the golf course on the other, and both Surfers Paradise and Broadbeach a short drive away without being close enough to be noisy.",
        "The housing stock is established. Generous blocks, mature trees, and streets that were laid out when there was still room to be generous with them. Many homes here have been held by the same family for a long time, which is part of why the suburb trades quietly.",
        "Buyers are usually families settling in rather than passing through. The schools are a genuine draw, the blocks give children somewhere to be, and the waterfront streets offer canal frontage at a level that is more approachable than the northern islands.",
        "It is not a suburb that sells itself on a view. It sells on the practical things, which means presentation and honest pricing carry more weight here than they do in the postcard pockets. Sellers who understand that tend to do well.",
        "We have worked with sellers here and know the streets that hold their value best. If Benowa Waters is on your list, that context is worth having before you start looking."
      ] },
```

- [ ] **Step 5: Run and confirm all pass**

Reload `tests.html`.

Expected: `0 failed`. If a word count falls outside 150 to 260, adjust the prose rather than the assertion.

- [ ] **Step 6: Read both guides in the browser**

Open `suburb.html?r=carrara` and `suburb.html?r=benowa`.

Expected: editorial reads as real prose, first paragraph renders at the larger lead size, measure stays within `--read` (70ch), no orphaned single words on the last line at 1440px.

- [ ] **Step 7: Claims audit**

Read both editorial blocks and confirm, line by line:
- The only record claim is Carrara's one bedroom record, which is evidenced
- No sales volume, listing count, or "we sell X" figures
- No claim that Jason or Barbara is always on site or personally present at everything
- No photography, video, marketing or media service talk
- No em dashes

- [ ] **Step 8: Commit**

```bash
git add projects/bespoke-site/prototype/data.js projects/bespoke-site/prototype/tests.js
git commit -m "content(bespoke): Carrara + Benowa Waters suburb guide editorial, evidence-led, claims-audited"
```

---

## Task 8: Journal index

**Files:**
- Create: `projects/bespoke-site/prototype/journal.html`
- Modify: `projects/bespoke-site/prototype/editorial.js` (`initJournal`)
- Modify: `projects/bespoke-site/prototype/phase2.css` (append)

**Interfaces:**
- Consumes: `B.getArticles`, `B.esc`, `B.getAgent`, `B.observeReveals`
- Produces: `journalCardHTML(article, delay)`, reused by the related block in Task 9

- [ ] **Step 1: Create the shell**

Create `prototype/journal.html` with the same head/header/menu pattern. Title `Journal | Bespoke Estate Agents`, description `Considered notes on the Gold Coast prestige market from Jason and Barbara Ward of Bespoke Estate Agents.` Body:

```html
  <main id="journal" class="stack-page" style="padding-top:0">
    <section class="p-hero">
      <div class="p-hero__media"><img src="https://bespoke.agents.10xvisuals.co/wp-content/uploads/2026/07/47-Somersert-Drive-_-Print-Drone-2-scaled.jpg" alt="Gold Coast coastline"></div>
      <div class="wrap">
        <span class="eyebrow on-dark">Journal</span>
        <h1>Notes on the market.</h1>
        <p>Occasional writing on selling, buying and reading the Gold Coast prestige market properly.</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="jr-grid" id="jr-grid"></div>
      </div>
    </section>

    <section class="section section--green">
      <div class="wrap center prose">
        <h2 class="reveal">Thinking about selling?</h2>
        <p class="reveal" data-d="1" style="margin:16px auto 0;color:var(--be-grey-300)">A quiet, private appraisal with real numbers on the table.</p>
        <div class="btn-row reveal" data-d="2" style="justify-content:center;margin-top:var(--sp-xl)"><a class="btn btn--light" href="soon.html?s=appraisal" data-appraisal>Book a Private Appraisal</a></div>
      </div>
    </section>
  </main>

  <footer class="site-footer" data-footer></footer>

  <script src="data.js"></script>
  <script src="app.js"></script>
  <script src="editorial.js"></script>
```

- [ ] **Step 2: Implement `journalCardHTML` and `initJournal`**

```js
  function fmtDate(iso) {
    return new Date(iso).toLocaleDateString("en-AU", { month: "long", year: "numeric" });
  }

  function journalCardHTML(a, delay) {
    var author = B.getAgent(a.author);
    return '<a class="jr-card reveal"' + (delay ? ' data-d="' + delay + '"' : "") +
      ' href="article.html?a=' + encodeURIComponent(a.slug) + '">' +
      '<div class="jr-card__media"><img src="' + a.hero.url + '" alt="' + B.esc(a.hero.alt) + '" loading="lazy"></div>' +
      '<div class="jr-card__body">' +
        '<span class="jr-card__cat">' + B.esc(a.category) + '</span>' +
        '<h3>' + B.esc(a.title) + '</h3>' +
        '<p>' + B.esc(a.dek) + '</p>' +
        '<span class="jr-card__by">' + (author ? B.esc(author.name) + " &middot; " : "") + fmtDate(a.date) + '</span>' +
      '</div></a>';
  }

  function initJournal() {
    var grid = document.getElementById("jr-grid");
    if (!grid) return;
    var arts = B.getArticles();
    if (!arts.length) {
      grid.innerHTML = '<div class="p-empty"><h3>The first notes are being written.</h3><p class="muted">Check back shortly.</p></div>';
      return;
    }
    grid.innerHTML = arts.map(function (a, i) { return journalCardHTML(a, (i % 3) + 1); }).join("");
    B.observeReveals();
  }
```

The empty-state branch is why the grid does not break with zero articles, satisfying the spec AC about working with very few articles.

- [ ] **Step 3: Append the CSS**

```css
/* ==========================================================================
   JOURNAL
   ========================================================================== */
.jr-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--sp-xl);}
@media(max-width:1024px){.jr-grid{grid-template-columns:repeat(2,1fr);}}
@media(max-width:640px){.jr-grid{grid-template-columns:1fr;}}
.jr-card{display:block;color:inherit;}
.jr-card__media{aspect-ratio:3/2;overflow:hidden;background:var(--be-grey-200);}
.jr-card__media img{width:100%;height:100%;object-fit:cover;
  transition:transform .8s var(--be-ease-expo);}
.jr-card:hover .jr-card__media img{transform:scale(1.04);}
.jr-card__body{padding-top:var(--sp-md);}
.jr-card__cat{font:500 .68rem/1 var(--be-font-body);letter-spacing:.12em;
  text-transform:uppercase;color:var(--be-green);}
.jr-card__body h3{margin-top:10px;font:300 1.3rem/1.3 var(--be-font-head);color:var(--be-charcoal);}
.jr-card__body p{margin-top:8px;color:var(--be-grey-600);font-size:.94rem;max-width:42ch;}
.jr-card__by{display:block;margin-top:14px;font:400 .8rem/1 var(--be-font-body);color:var(--be-grey-600);}
```

- [ ] **Step 4: Verify**

Open `journal.html`.

Expected: three cards, newest first (What off market really means, then Preparing a waterfront home, then Reading a suburb record), each with category, title, dek and a byline. Zero console errors. Confirm order:

```js
[...document.querySelectorAll('.jr-card h3')].map(function(h){return h.textContent})
```

Expected output: `["What off market really means", "Preparing a waterfront home for market", "Reading a suburb record"]`

- [ ] **Step 5: Check 375px and 1440px**

Expected: 1-up then 3-up, no horizontal scroll.

- [ ] **Step 6: Commit**

```bash
git add projects/bespoke-site/prototype/journal.html projects/bespoke-site/prototype/editorial.js projects/bespoke-site/prototype/phase2.css
git commit -m "feat(bespoke): Journal index with JournalCard grid and empty state"
```

---

## Task 9: Article template

**Files:**
- Create: `projects/bespoke-site/prototype/article.html`
- Modify: `projects/bespoke-site/prototype/editorial.js` (`initArticle`)
- Modify: `projects/bespoke-site/prototype/phase2.css` (append)

**Interfaces:**
- Consumes: `B.getArticle`, `B.getAgent`, `B.esc`, `B.agentRow`, `B.buildEnquiry`, `B.wireForm`, `B.observeReveals`, `journalCardHTML` from Task 8

- [ ] **Step 1: Create the shell**

Create `prototype/article.html`, same head/header/menu pattern, body:

```html
  <main id="article" class="stack-page" style="padding-top:0"></main>
  <footer class="site-footer" data-footer></footer>
  <script src="data.js"></script>
  <script src="app.js"></script>
  <script src="editorial.js"></script>
```

Add the draft marker as an HTML comment immediately inside `<body>`, so it is visible to anyone reading source but not to a visitor:

```html
  <!-- Journal copy is DRAFT, written for Jason and Barbara to approve before publication. -->
```

- [ ] **Step 2: Implement `initArticle`**

```js
  function initArticle() {
    var root = document.getElementById("article");
    if (!root) return;
    var slug = new URLSearchParams(location.search).get("a");
    var a = slug && B.getArticle(slug);
    if (!a) { location.replace("journal.html"); return; }

    var author = B.getAgent(a.author);
    document.title = a.title + " | Journal | Bespoke Estate Agents";
    var rel = a.related.map(B.getArticle).filter(Boolean);

    root.innerHTML =
      '<section class="p-hero"><div class="p-hero__media"><img src="' + a.hero.url + '" alt="' + B.esc(a.hero.alt) + '"></div>' +
        '<div class="wrap"><span class="eyebrow on-dark">' + B.esc(a.category) + '</span>' +
        '<h1>' + B.esc(a.title) + '</h1></div></section>' +

      '<section class="section"><div class="wrap">' +
        '<article class="art-body reveal">' +
          '<p class="art-dek">' + B.esc(a.dek) + '</p>' +
          a.body.slice(0, 2).map(function (p) { return "<p>" + B.esc(p) + "</p>"; }).join("") +
          (a.pullQuote ? '<blockquote class="art-quote">' + B.esc(a.pullQuote) + "</blockquote>" : "") +
          a.body.slice(2).map(function (p) { return "<p>" + B.esc(p) + "</p>"; }).join("") +
          '<div class="art-by">' + (author ? B.agentRow(author) : "") + '</div>' +
        '</article>' +
      '</div></section>' +

      (rel.length
        ? '<section class="section section--offwhite"><div class="wrap">' +
            '<div class="sub-head"><span class="eyebrow" style="margin:0">Also worth reading</span>' +
            '<a class="muted" href="journal.html" style="text-decoration:underline;text-underline-offset:4px">All notes</a></div>' +
            '<div class="jr-grid">' + rel.map(function (x, i) { return journalCardHTML(x, i + 1); }).join("") + '</div>' +
          '</div></section>'
        : "") +

      '<section class="section"><div class="wrap center prose" style="max-width:560px">' +
        '<span class="eyebrow">Private Appraisal</span>' +
        '<h2 class="reveal" style="margin-top:6px">Considering a move?</h2>' +
        '<form class="enquiry" novalidate style="margin-top:var(--sp-lg);text-align:left">' +
          B.buildEnquiry("a-", "A quiet, no obligation conversation about your property and the current market.", "Request appraisal") +
        '</form></div></section>';

    B.wireForm(root.querySelector(".enquiry"), { source: "appraisal" });
    B.observeReveals();
  }
```

The pull quote is injected after the second paragraph so it breaks the column rather than sitting at the top or bottom.

- [ ] **Step 3: Append the CSS**

```css
/* ==========================================================================
   ARTICLE
   Body measure is held at 65 to 75ch per BUILD-SPEC 8.7.
   ========================================================================== */
.art-body{max-width:70ch;margin-inline:auto;}
.art-body p{color:var(--be-grey-600);font-size:1.02rem;line-height:1.75;margin-bottom:var(--sp-md);}
.art-dek{font-size:1.24rem;line-height:1.6;color:var(--be-charcoal);margin-bottom:var(--sp-lg);}
.art-quote{margin:var(--sp-xl) 0;padding-left:var(--sp-lg);
  border-left:2px solid var(--be-green);
  font:300 1.42rem/1.45 var(--be-font-head);color:var(--be-charcoal);max-width:34ch;}
.art-by{margin-top:var(--sp-xl);padding-top:var(--sp-lg);border-top:1px solid var(--be-line);}
@media(max-width:640px){
  .art-quote{max-width:none;font-size:1.22rem;}
  .art-dek{font-size:1.1rem;}
}
```

- [ ] **Step 4: Verify all three articles**

Open `article.html?a=what-off-market-really-means`, `?a=preparing-a-waterfront-home`, `?a=reading-a-suburb-record`.

Expected on each: hero with category and title, dek at lead size, two paragraphs, pull quote, remaining paragraphs, author row, two related cards, appraisal form. Zero console errors.

- [ ] **Step 5: Verify the measure**

On any article, run in the console:

```js
(function(){var p=document.querySelector('.art-body p:not(.art-dek)');var ch=parseFloat(getComputedStyle(p).fontSize)*0.5;return Math.round(p.getBoundingClientRect().width/ch)})()
```

Expected: a value between 60 and 80 at 1440px. This is an approximation of character measure; if it reads well outside that band, adjust `.art-body{max-width}` rather than the assertion.

- [ ] **Step 6: Verify the redirect and the Lead**

Open `article.html?a=nonsense` and `article.html` with no param. Expected: both land on `journal.html`.

Submit the appraisal form with valid details and consent ticked. Expected console output: `source: "appraisal"`, `relatedListing: null`, `relatedRegion: null`.

- [ ] **Step 7: Commit**

```bash
git add projects/bespoke-site/prototype/article.html projects/bespoke-site/prototype/editorial.js projects/bespoke-site/prototype/phase2.css
git commit -m "feat(bespoke): Article template with 70ch measure, pull quote, related notes"
```

---

## Task 10: Navigation wiring

**Files:**
- Modify: `projects/bespoke-site/prototype/index.html:22-27` (desktop nav), `:34-40` (overlay menu)
- Modify: `projects/bespoke-site/prototype/listing.html` (same two blocks)
- Modify: `projects/bespoke-site/prototype/soon.html` (same two blocks)
- Modify: `projects/bespoke-site/prototype/suburbs.html`, `suburb.html`, `journal.html`, `article.html` (same two blocks)
- Modify: `projects/bespoke-site/prototype/app.js:26` (footer Explore column)

**Interfaces:** none new.

- [ ] **Step 1: Define the canonical nav**

Every one of the seven prototype pages gets exactly this desktop nav. Note that "Sold" is removed: it is a tab inside Collection, and having it link out to the live site's `#estates` anchor while also existing as a tab was a pre-existing inconsistency.

```html
      <nav class="nav-desktop" aria-label="Primary">
        <a href="index.html">Collection</a>
        <a href="suburbs.html">Suburbs</a>
        <a href="journal.html">Journal</a>
        <a href="https://bespoke.agents.10xvisuals.co/projects/">Projects</a>
        <a href="https://bespoke.agents.10xvisuals.co/about/">About</a>
      </nav>
```

And this overlay menu:

```html
    <nav aria-label="Full site">
      <a href="index.html">Collection</a>
      <a href="suburbs.html">Suburbs</a>
      <a href="journal.html">Journal</a>
      <a href="https://bespoke.agents.10xvisuals.co/projects/">Projects</a>
      <a href="https://bespoke.agents.10xvisuals.co/about/">About</a>
    </nav>
```

- [ ] **Step 2: Apply per-page `aria-current`**

Add `aria-current="page"` to exactly one desktop nav link per page:

| Page | Link carrying `aria-current="page"` |
|---|---|
| `index.html` | Collection |
| `listing.html` | Collection |
| `suburbs.html` | Suburbs |
| `suburb.html` | Suburbs |
| `journal.html` | Journal |
| `article.html` | Journal |
| `soon.html` | none |

- [ ] **Step 3: Update the footer Explore column**

In `app.js:26`, replace:

```js
      '<div class="footer-col"><h4>Explore</h4><a href="index.html">Collection</a><a href="https://bespoke.agents.10xvisuals.co/#estates">Sold</a><a href="https://bespoke.agents.10xvisuals.co/projects/">Projects</a><a href="https://bespoke.agents.10xvisuals.co/about/">About</a><a href="https://bespoke.agents.10xvisuals.co/services/">Services</a><a href="https://bespoke.agents.10xvisuals.co/#contact">Contact</a></div>' +
```

with:

```js
      '<div class="footer-col"><h4>Explore</h4><a href="index.html">Collection</a><a href="suburbs.html">Suburbs</a><a href="journal.html">Journal</a><a href="https://bespoke.agents.10xvisuals.co/projects/">Projects</a><a href="https://bespoke.agents.10xvisuals.co/about/">About</a><a href="https://bespoke.agents.10xvisuals.co/services/">Services</a><a href="https://bespoke.agents.10xvisuals.co/#contact">Contact</a></div>' +
```

- [ ] **Step 4: Retire the obsolete soon.html entries**

In `app.js:337-338`, the `suburbs` and `journal` entries in the soon-page map are now dead, since both sections exist. Leave them in place as a safety net for any stale bookmark, but change their copy so they redirect rather than mislead. Replace those two lines with:

```js
      suburbs: { ey: "Suburbs", h: "Suburb guides have moved.", p: "The guides now live in the Collection.", go: "suburbs.html" },
      journal: { ey: "Journal", h: "The Journal has moved.", p: "The notes now live in the Collection.", go: "journal.html" },
```

Then in `initSoon`, immediately after `var d = map[s] || {...};`, add:

```js
    if (d.go) { location.replace(d.go); return; }
```

- [ ] **Step 5: Verify every page**

Open all seven pages in the visible browser pane. On each:

```js
[...document.querySelectorAll('.nav-desktop a')].map(function(a){return a.textContent+(a.getAttribute('aria-current')?'*':'')})
```

Expected: five entries on every page, with the asterisk on the correct one per the Step 2 table, and no asterisk at all on `soon.html`.

- [ ] **Step 6: Verify no dead links across the section**

On each page run:

```js
[...document.querySelectorAll('a[href]')].filter(function(a){return a.getAttribute('href')==='#'||a.getAttribute('href')===''}).length
```

Expected output on every page: `0`

- [ ] **Step 7: Verify the soon redirects**

Open `soon.html?s=suburbs` and `soon.html?s=journal`.

Expected: they land on `suburbs.html` and `journal.html` respectively. `soon.html?s=appraisal` and `soon.html?s=contact` must still render their forms normally.

- [ ] **Step 8: Commit**

```bash
git add projects/bespoke-site/prototype/
git commit -m "feat(bespoke): wire Suburbs + Journal into nav, overlay and footer across all prototype pages"
```

---

## Task 11: Full verification pass

**Files:**
- Modify: any file needing a fix found here
- Modify: `docs/superpowers/specs/2026-07-25-bespoke-collection-breadth-design.md` (correct the `?p=` error)

**Interfaces:** none new.

- [ ] **Step 1: Correct the spec's URL param error**

In the spec, §4 states listing detail uses `listing.html?p=`. The actual convention is `?id=`. Fix that line so the spec matches the code.

- [ ] **Step 2: Run the full test suite**

Open `tests.html`.

Expected: all assertions pass, `0 failed`. Record the total count.

- [ ] **Step 3: Walk the whole section as a prospect would**

In the visible browser pane, starting at `index.html`, click through: Collection to a listing, back, Suburbs, Carrara guide, a listing inside it, back, other-guides card to Benowa, Journal, an article, a related article, then the appraisal CTA from three different places.

Expected: no placeholder page is ever reached, no console error at any point, every back-navigation lands somewhere sensible.

- [ ] **Step 4: Confirm the reveal failsafe**

On `suburb.html?r=carrara`, run:

```js
[...document.querySelectorAll('.reveal')].filter(function(e){return getComputedStyle(e).opacity==='0'}).length
```

Expected output: `0` after scrolling through the page. If any element reports `0`, first confirm the browser pane is visible; a hidden pane pauses transitions and produces a false reading.

- [ ] **Step 5: Confirm reduced motion**

Set the pane to prefers-reduced-motion. Reload `suburbs.html`.

Expected: all content visible immediately, no transitions, zero elements at `opacity: 0`.

- [ ] **Step 6: Check both breakpoints on all seven pages**

At 375px and 1440px, on each page:

```js
document.documentElement.scrollWidth <= window.innerWidth
```

Expected output: `true` on all fourteen combinations.

- [ ] **Step 7: Capture proof**

Screenshot both suburb guides, the suburbs index, the journal index and one article, at 1440px.

- [ ] **Step 8: Verify the existing behaviour still works**

On `index.html`: switch all three status tabs, apply a suburb filter and a price filter, confirm the URL updates, clear filters, open a listing, open the gallery lightbox, open the appraisal modal.

Expected: all behave exactly as before this plan started. Zero console errors.

- [ ] **Step 9: Commit and push**

```bash
git add -A projects/bespoke-site/ docs/superpowers/specs/
git commit -m "verify(bespoke): full Collection breadth-pass QA, correct spec URL param"
git push
```

- [ ] **Step 10: File the work in the wiki**

Append an entry to `wiki/log.md` dated `2026-07-25`, type `build`, titled `Bespoke Collection breadth pass, Suburbs + Journal`. Record: the four new page types, the evidence-led Carrara and Benowa promotion, the `window.BESPOKE` seam and `editorial.js` split, the two reassigned seed listings, the removed invented suburb record, and the open items still outstanding (full §9 tier rewrite, Journal drafts pending Jason's approval, placeholder imagery, unsigned stack). Update the `[[bespoke-estate-agents]]` client page and `wiki/index.md` if the picture has shifted.

```bash
git add wiki/
git commit -m "docs(wiki): log Bespoke Collection breadth pass"
git push
```

---

## Self-Review

**Spec coverage:**

| Spec section | Task |
|---|---|
| §2 amendments (do not build About/Contact/Sold/Home) | Global Constraints, Task 10 nav |
| §3 suburb tier revision | Task 3 |
| §4 build list, 5 pages | Tasks 5, 6, 8, 9 |
| §5.1 Region shape | Task 3 |
| §5.2 listings reassignment | Task 3 |
| §5.3 unearned claim removal | Task 3 |
| §5.4 Articles | Task 4 |
| §6 data-access layer | Tasks 2, 3, 4 |
| §7.1 Suburbs index AC | Task 5 |
| §7.2 Suburb Guide AC | Tasks 6, 7 |
| §7.3 Journal index AC | Task 8 |
| §7.4 Article AC | Task 9 |
| §7.5 global AC (nav, aria-current, reveals, dead links) | Tasks 10, 11 |
| §8 verification, all 9 items | Task 11 |
| §9 open items | Task 11 Step 10 |

No spec requirement is unimplemented.

**Type consistency:** `getRegions(filter)` takes `{tier, guideStatus}` in Tasks 3, 5 and 6. `guideStatus` values are exactly `"live"` and `"soon"` throughout. `heroGrade` values are exactly `warm|cool|neutral|deep`, and `phase2.css` defines a `.grade--` class for each. `suburbCardHTML(region, delay)` is defined in Task 5 and reused in Task 6. `journalCardHTML(article, delay)` is defined in Task 8 and reused in Task 9. `B.wireForm(form, ctx)` receives `{source, relatedRegion}` in Task 6 and `{source}` in Task 9, both matching the existing `app.js:186` shape. URL params are `?id=`, `?r=`, `?a=` consistently.

**Known deviations from the skill's defaults, deliberate:**
- Tasks 5, 6, 8, 9 and 10 have no unit tests. They are DOM rendering and markup, and this codebase has no DOM test harness; adding one would breach the no-build-step constraint. Verification for these tasks is explicit browser console assertions with stated expected output, which is the strongest check available without changing the stack.
- Task 3 Step 6 knowingly leaves two assertions loosened until Task 7 tightens them. This is called out in the step rather than hidden.
