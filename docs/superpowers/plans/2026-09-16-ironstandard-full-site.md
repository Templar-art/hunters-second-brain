# Iron Standard Full Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand `projects/ironstandard-lp/` from a single-page waitlist landing page into the 7-page site Anthony specified on 16 Sep 2026 (Home, About Us, The Facility, Coaching, Join the Waitlist, FAQ, Contact Us), with a working nav, and a Google Sheets–backed form submission pipeline for both new forms.

**Architecture:** Static HTML/CSS/JS, no framework, no build step — same pattern the site already uses. One shared stylesheet (`assets/css/style.css`) and one shared script (`assets/js/main.js`) extend across all 7 pages; there is no templating engine, so shared markup (nav, footer) is hand-duplicated into each page, exactly as `partials/footer.html` already documents itself as "a copy, not an include." Forms submit via a classic `<form>` POST to a hidden iframe, landing in a Google Sheet through a Google Apps Script Web App — no API key or credential ever touches client-side JS.

**Tech Stack:** Plain HTML5, CSS3 (custom properties, `:has()`, `@starting-style`, `clamp()`), vanilla JS (no dependencies), Google Apps Script (`.gs`, server-side, deployed under Anthony's own Google account).

## Global Constraints

- No build step. Every file must work opening `index.html` directly or via the existing local preview server (`.claude/launch.json`, `ironstandard-lp`, port 8140).
- No framework, no npm dependency, no bundler. This project has never used one and nothing here justifies starting.
- Brand system is locked: `--bg:#0a0a0a`, `--fg:#ffffff`, `--fg-dim:#b8b8b8`, `--accent:#F4502A`, `--font-display:'TASA Orbiter'`. Do not introduce a second accent color or a second display font.
- Every image continues to load from the WordPress media library at `https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/` unless it's a genuinely new local asset with no remote counterpart yet (there are none new in this plan — every image used already exists at that URL).
- Photography stays black-and-white via the existing `grayscale(1)` filter pattern, except the two panels already exempted (`inside-the-facility.jpg`, `posing-room.jpg` use the site's default filter like everything else as of 15 Sep — do not re-introduce the colour exemption that was tried and reverted).
- No fact that Anthony has not cleared may appear on any page: no price, no exact address, no opening date. Where his own final copy is still pending (About Us narrative, Waitlist offer wording, FAQ answers), ship accurate placeholder copy built only from what he has already stated in his 16 Sep email, flagged with an HTML comment saying so.
- Never put a form-submission credential in client-side JavaScript. The Apps Script Web App URL is a public endpoint by design (that's how Apps Script Web Apps work) and is not a secret — this is not the same class of problem the project's earlier Brevo-API-key mistake was, and does not need the same fix, but no *other* credential gets added either.
- `git commit` freely after each task; no push gate defined by this plan (follow the vault's own git conventions).

---

## File Structure

**New files:**
- `about.html` — About Us page
- `facility.html` — The Facility page
- `coaching.html` — Coaching page
- `faq.html` — FAQ page
- `waitlist.html` — Join the Waitlist page (the real destination for every "Join the waitlist" CTA and the real home of `id="form"`)
- `contact.html` — Contact Us page
- `google-apps-script/waitlist-handler.gs` — the form-handling backend, version-controlled here even though it deploys into Anthony's Google account, not this repo
- `google-apps-script/README.md` — deployment steps for the `.gs` file (Anthony/Hunter run these manually; nothing here can be scripted, it requires his Google account)

**Modified files:**
- `index.html` — real nav markup in `.site-header`, new hero line and positioning paragraph, hero CTA retargeted from the dead `#form` anchor to `waitlist.html`, new "Explore" link block replacing the old waitlist-placeholder HTML comment
- `assets/css/style.css` — z-index scale, nav styles, page-header component, `.form-panel` (renamed/generalized from `.waitlist`), honeypot-field styles
- `assets/js/main.js` — intro-plays-once-per-session gate, nav mobile toggle, shared form-submit handler
- `README.md` — reflects the 7-page structure, replaces the Brevo setup section with the Apps Script one, updated "what's still needed" list

**Not touched by this plan (explicitly out of scope, per the spec's own open items):**
- `netlify.toml` / DNS — hosting target is unresolved (spec open item 1); this plan builds pages that work under any static host, and leaves the actual cutover for later
- `assets/video/*` — still unused, still not deleted (matches existing precedent of keeping unused-but-paid-for assets in the repo)
- Favicon — still blocked on the monogram mark per the existing README note

---

### Task 1: Z-index scale and the shared nav bar

**Files:**
- Modify: `assets/css/style.css:1-9` (root tokens), `assets/css/style.css:65` (`.intro-splash` z-index), append new nav rules after the footer block (end of file)
- Modify: `index.html:36` (`<header class="site-header"></header>` → real nav markup)
- Modify: `assets/js/main.js` (append nav toggle logic)

**Interfaces:**
- Produces: the exact nav markup block every other page in this plan copies verbatim into its own `<header class="site-header">`:
  ```html
  <header class="site-header">
    <a href="index.html" class="nav-logo-link" aria-label="Iron Standard, home">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="Iron Standard" class="nav-logo">
    </a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">
      <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
      <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
    <nav class="nav-links" aria-label="Primary">
      <a href="about.html">About Us</a>
      <a href="facility.html">The Facility</a>
      <a href="coaching.html">Coaching</a>
      <a href="faq.html">FAQ</a>
      <a href="contact.html">Contact Us</a>
      <a href="waitlist.html" class="btn-primary">Join the waitlist</a>
    </nav>
  </header>
  ```
  Each page sets `aria-current="page"` on its own matching link (index.html has no matching link since the logo itself is the Home link — leave all 5 links plain on index.html).
- Produces: CSS custom properties `--z-nav: 100` and `--z-intro: 999`, and the classes `.nav-logo-link`, `.nav-logo`, `.nav-toggle` (with `.icon-open`/`.icon-close` children and `[aria-expanded]` state), `.nav-links` (with `.is-open` state on mobile).
- Produces: `main.js` behavior — clicking `.nav-toggle` toggles `.nav-links.is-open` and `aria-expanded`; clicking any link inside `.nav-links` closes it; `Escape` closes it. This wiring must run on every page that includes the nav markup (all 7), so it lives in the shared `main.js`, guarded by `if (navToggle && navLinks)` so it's a no-op on any page that somehow lacks the markup.

- [ ] **Step 1: Add the z-index scale to `:root`**

In `assets/css/style.css`, inside the existing `:root { ... }` block (lines 1-9), add two lines before the closing brace:

```css
  --z-nav: 100;
  --z-intro: 999;
```

- [ ] **Step 2: Point `.intro-splash` at the new token**

Change line 65's block from:
```css
.intro-splash {
  position: fixed;
  inset: 0;
  background: var(--bg);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
```
to use `z-index: var(--z-intro);` instead of the literal `999`. No other line in that rule changes.

- [ ] **Step 3: Append the nav CSS to the end of `style.css`**

```css
/* Nav — fixed on every page, translucent gradient rather than a solid
   fill or scroll-triggered state. The whole site sits on --bg except the
   hero photo, and white nav text/logo already reads fine over both a
   near-black background and the hero's brightness(0.5) photo, so there's
   no scroll-position logic to write or a stacking-context transition to
   get wrong. The gradient exists only to guarantee legibility over the
   brighter patches of the hero photo specifically. */
.site-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: var(--z-nav);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  padding: 1.1rem 1.5rem;
  background: linear-gradient(to bottom, rgba(10, 10, 10, 0.65), rgba(10, 10, 10, 0));
}
.nav-logo-link { display: block; line-height: 0; }
.nav-logo { height: 28px; width: auto; display: block; }

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.75rem;
}
.nav-links a {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-decoration: none;
  color: var(--fg-dim);
  transition: color 0.2s;
}
.nav-links a:hover,
.nav-links a[aria-current="page"] { color: var(--fg); }
.nav-links a.btn-primary { padding: 0.55rem 1.2rem; font-size: 0.8rem; }
.nav-links a.btn-primary:hover { color: #0a0a0a; }

.nav-toggle {
  display: none;
  position: relative;
  /* .nav-toggle and .nav-links are both plain DOM children of
     .site-header, which is the nearest positioned ancestor and therefore
     the stacking context they're compared within — so this z-index only
     has to beat .nav-links' z-index (set below), not var(--z-nav) or
     anything else on the page. That's what keeps the close button
     tappable on top of the full-screen mobile overlay. */
  z-index: 1;
  background: none;
  border: none;
  color: var(--fg);
  padding: 0.5rem;
  cursor: pointer;
}
.nav-toggle svg { width: 24px; height: 24px; display: block; }
.nav-toggle .icon-close { display: none; }
.nav-toggle[aria-expanded="true"] .icon-open { display: none; }
.nav-toggle[aria-expanded="true"] .icon-close { display: block; }

@media (max-width: 860px) {
  .nav-toggle { display: block; }
  .nav-links {
    position: fixed;
    z-index: 0;
    inset: 0;
    background: var(--bg);
    flex-direction: column;
    justify-content: center;
    gap: 2rem;
    transform: translateY(-100%);
    transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .nav-links.is-open { transform: translateY(0); }
  .nav-links a { font-size: 1.4rem; }
}
@media (prefers-reduced-motion: reduce) {
  .nav-links { transition: none; }
}
```

- [ ] **Step 4: Wire the nav markup into `index.html`**

Replace line 36:
```html
  <header class="site-header"></header>
```
with the exact nav markup block from the Interfaces section above.

- [ ] **Step 5: Add the nav toggle script to `main.js`**

Append to the end of the file, inside the existing `document.addEventListener('DOMContentLoaded', () => { ... })` callback, just before its closing `});`:

```javascript
  // --- Nav: mobile menu toggle. The button only renders below 860px
  // (see .nav-toggle in style.css), so there's no matchMedia guard here —
  // a desktop click can never reach it.
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      const isOpen = navLinks.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
    });
    navLinks.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navLinks.classList.contains('is-open')) {
        navLinks.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }
```

- [ ] **Step 6: Verify in the browser**

Start the preview server (`ironstandard-lp`, port 8140) and load `index.html`. Run:

```javascript
({
  headerZ: getComputedStyle(document.querySelector('.site-header')).zIndex,
  introZ: getComputedStyle(document.querySelector('.intro-splash')).zIndex,
  navLinksCount: document.querySelectorAll('.nav-links a').length,
})
```
Expected: `headerZ: "100"`, `introZ: "999"`, `navLinksCount: 6` (5 page links + the waitlist button).

Resize the viewport to 700px wide, click `.nav-toggle`, then check:
```javascript
({
  isOpen: document.querySelector('.nav-links').classList.contains('is-open'),
  ariaExpanded: document.querySelector('.nav-toggle').getAttribute('aria-expanded'),
})
```
Expected: `isOpen: true`, `ariaExpanded: "true"`. Press Escape and confirm both flip back.

- [ ] **Step 7: Commit**

```bash
git add index.html assets/css/style.css assets/js/main.js
git commit -m "Add site-wide nav bar and a semantic z-index scale"
```

---

### Task 2: Intro plays once per browser session, not once per page

**Files:**
- Modify: `assets/js/main.js` (top of the intro-splash block)

**Interfaces:**
- Consumes: nothing new from Task 1.
- Produces: every subsequent page in this plan ships the exact same `.intro-splash` markup block that `index.html` already has (copy verbatim, including the CSS classes) — this task guarantees that markup only actually plays once per `sessionStorage` lifetime, regardless of how many of the 7 pages include it.

**Why this task exists even though it isn't spelled out as its own line in the 16 Sep spec:** the single-page build never needed this, because there was only one page to land on. The moment there are 7, the existing `main.js` — which runs the full ~2.3s flash-and-logo-drag sequence unconditionally on every `DOMContentLoaded` — replays that sequence on every single click between pages. This was already decided during the wireframe round of this project ("intro sequence plays once per session, on whichever page they land on first; clicking between pages goes straight in; a new tab plays it again") and approved then; it just never made it into the written spec document as its own line. Building it now, before six more pages get the splash markup, avoids shipping the replay bug to all of them and then fixing it after the fact.

- [ ] **Step 1: Add the session gate at the top of the intro-splash logic**

In `assets/js/main.js`, find:
```javascript
  const splash = document.querySelector('.intro-splash');
```
Immediately before that line, insert:
```javascript
  // Plays once per browser session, not once per page. Without this, every
  // one of the site's 7 pages replays the full ~2.3s flash-and-logo-drag
  // sequence on every click between them. A new tab (fresh sessionStorage)
  // sees it again, same as a first visit should.
  const introAlreadyPlayed = sessionStorage.getItem('isl-intro-played') === '1';
```

Then find the existing splash-removal fallback branch:
```javascript
  } else {
    // No-JS-equivalent path (reduced motion, or missing elements): don't
    // wait on an intro that isn't playing.
    if (splash) splash.remove();
  }
```
and change the condition just above it — the current line:
```javascript
  if (splash && cloneLogo && whiteFlash && realLogo && !reducedMotion) {
```
becomes:
```javascript
  if (splash && cloneLogo && whiteFlash && realLogo && !reducedMotion && !introAlreadyPlayed) {
```

Finally, inside `runIntro()`, find the line that sets `.js-driven`:
```javascript
  function runIntro() {
    splash.classList.add('js-driven');
```
and add the session flag right after it:
```javascript
  function runIntro() {
    splash.classList.add('js-driven');
    sessionStorage.setItem('isl-intro-played', '1');
```

- [ ] **Step 2: Verify in the browser**

Load `index.html` fresh (clear the tab's sessionStorage first: `sessionStorage.clear()` then reload). Confirm the intro plays. Then run:
```javascript
sessionStorage.getItem('isl-intro-played')
```
Expected: `"1"`.

Reload the same tab (same session) and immediately check `document.querySelector('.intro-splash')` — expected: `null` (removed before it could render), and no flash sequence visible. Then run `sessionStorage.clear()` and reload once more — expected: the intro plays again.

- [ ] **Step 3: Commit**

```bash
git add assets/js/main.js
git commit -m "Intro sequence plays once per session, not once per page"
```

---

### Task 3: Home page — new hero line, positioning paragraph, explore-links block

**Files:**
- Modify: `index.html:56-58` (hero title/paragraph/CTA), `index.html:140-149` (replace the dead waitlist-comment block)
- Modify: `assets/css/style.css` (append explore-links section styles)

**Interfaces:**
- Consumes: the nav markup and `.btn-primary` class from Task 1 (already present).
- Produces: a new `.explore-links` section (class name) that later tasks don't depend on — this is Home-only.
- Produces: every `href="#form"` in the codebase is now `href="waitlist.html"` — this fixes a real, currently-live bug: `#form` resolves to nothing today, so the hero button and scroll arrow scroll into a void.

- [ ] **Step 1: Replace the hero title, paragraph, and CTA targets**

Replace `index.html` lines 56-58:
```html
        <h1 class="hero-title">A different <br class="br-m">standard <br class="br-d">for <br class="br-m">serious training</h1>
        <p class="hero-sub">Something is being built in Oslo. 800m² of it, made for people who train like they mean it, and nothing like the gym you're standing in right now. The location stays quiet a little longer. Get on the list and you'll hear it first.</p>
        <a href="#form" class="btn-primary">Join the waitlist</a>
```
with:
```html
        <h1 class="hero-title">Built by discipline. <br class="br-d">Driven by <br class="br-m">community.</h1>
        <p class="hero-sub">Iron Standard is a performance training facility in Oslo, for people who train seriously. Not a commercial chain built for volume. Not a niche strength gym that only works if you already belong. Somewhere in between, built properly, for both.</p>
        <a href="waitlist.html" class="btn-primary">Join the waitlist</a>
```
Note the `<br class="br-d">`/`<br class="br-m">` placement changed to match the new sentence's natural break (two short sentences, not one long one) — `.br-d` (desktop) breaks after "discipline.", `.br-m` (mobile) additionally breaks after "Driven by" so mobile still reads as three short lines. Both classes already exist in `style.css` and need no CSS changes.

Also on line 59, change:
```html
        <a href="#form" class="scroll-arrow" aria-label="Scroll to join the waitlist">
```
to:
```html
        <a href="waitlist.html" class="scroll-arrow" aria-label="Go to the waitlist">
```

- [ ] **Step 2: Replace the dead placeholder comment with a real explore-links section**

Replace `index.html` lines 140-149 (the `<!-- Waitlist section removed 11 Sep ... -->` comment) with:
```html
    <section class="section explore-links" data-reveal>
      <p class="kicker">Go deeper</p>
      <div class="explore-grid">
        <a href="about.html" class="explore-card">
          <span>About Us</span>
          <p>Why this exists, and who's building it.</p>
        </a>
        <a href="facility.html" class="explore-card">
          <span>The Facility</span>
          <p>800m² in central Oslo, built for one thing.</p>
        </a>
        <a href="coaching.html" class="explore-card">
          <span>Coaching</span>
          <p>Programming, independent PTs, and a real community.</p>
        </a>
        <a href="faq.html" class="explore-card">
          <span>FAQ</span>
          <p>Opening timeline, location, and how founding membership works.</p>
        </a>
      </div>
    </section>
```

- [ ] **Step 3: Add explore-links CSS**

Append to `assets/css/style.css`:
```css
/* Explore-links: Home's only link out to the other 6 pages besides the
   nav. Without this, anyone who scrolls past the nav never learns the
   rest of the site exists. */
.explore-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}
.explore-card {
  display: block;
  border: 1px solid rgba(255, 255, 255, 0.12);
  padding: 1.5rem;
  text-decoration: none;
  transition: border-color 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
.explore-card:hover { border-color: var(--accent); }
.explore-card span {
  font-family: var(--font-display);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: var(--fg);
  font-size: 1.05rem;
}
.explore-card p {
  color: var(--fg-dim);
  margin-top: 0.6rem;
  font-size: 0.95rem;
  max-width: none;
}
```

- [ ] **Step 4: Verify in the browser**

```javascript
({
  h1: document.querySelector('.hero-title').textContent.trim(),
  ctaHref: document.querySelector('.btn-primary').getAttribute('href'),
  arrowHref: document.querySelector('.scroll-arrow').getAttribute('href'),
  exploreLinks: [...document.querySelectorAll('.explore-card')].map(a => a.getAttribute('href')),
  noDeadForm: !document.querySelector('a[href="#form"]'),
})
```
Expected: `ctaHref: "waitlist.html"`, `arrowHref: "waitlist.html"`, `exploreLinks` an array of 4 real `.html` paths, `noDeadForm: true`.

Also re-run the mobile/desktop line-count checks from the 11 Sep and 14 Sep work (two lines desktop, three mobile) against the *new* hero title text at 1280px and 375px widths, confirming no overflow — the new sentence is shorter than the old one, so this is a sanity check, not expected to fail.

- [ ] **Step 5: Commit**

```bash
git add index.html assets/css/style.css
git commit -m "Home: new hero line and positioning copy, explore-links to the other 6 pages"
```

---

### Task 4: Page-header component and the About Us page

**Files:**
- Create: `about.html`
- Modify: `assets/css/style.css` (append page-header styles)

**Interfaces:**
- Produces: `.page-header` (class name) — the short, non-hero title band every one of the remaining 5 new pages uses. Structure:
  ```html
  <div class="page-header">
    <p class="kicker">[Section name]</p>
    <h1>[Page title]</h1>
    <p>[One-sentence intro]</p>
  </div>
  ```
- Consumes: the nav markup from Task 1, the `.section`/`.kicker`/`.pillars`/`.btn-primary` classes already defined in `style.css`, the footer markup already established in `partials/footer.html` (copy it, don't link to it — same "copy, not include" pattern the project already uses).

- [ ] **Step 1: Add `.page-header` CSS**

Append to `assets/css/style.css`:
```css
/* Short title band for the 6 inner pages, none of which get a full-height
   hero — Home already spent that treatment on the intro sequence, and
   repeating it would delay content someone deliberately clicked through
   for. Top padding clears the fixed nav; unlike .hero-sub this doesn't
   need the .section p:not(.kicker) specificity fight, because it isn't
   nested inside .section at all. */
.page-header {
  padding: clamp(7rem, 14vw, 9rem) 1.5rem 2.5rem;
  max-width: var(--max-width);
  margin: 0 auto;
  text-align: center;
}
.page-header .kicker { text-align: center; }
.page-header p:not(.kicker) {
  color: var(--fg-dim);
  max-width: 640px;
  margin: 1rem auto 0;
  font-size: 1.05rem;
}
```

- [ ] **Step 2: Create `about.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>About Us — Iron Standard, Oslo</title>
<meta name="theme-color" content="#0a0a0a">
<meta name="description" content="Founded by a ten-year coach and three-time national athlete, with Zero Weakness's Thomas Lilley as strategic advisor. Why Iron Standard exists.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=TASA+Orbiter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v=12">
</head>
<body>
  <div class="intro-splash" aria-hidden="true">
    <div class="intro-flash-stack">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-1.jpg" alt="" class="intro-flash is-active">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-2.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-3.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-4.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-5.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-6.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-7.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-8.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-9.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-10.jpg" alt="" class="intro-flash">
    </div>
    <div class="intro-caption">Coming soon</div>
    <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="" class="intro-logo">
    <div class="intro-whiteflash"></div>
  </div>
  <header class="site-header">
    <a href="index.html" class="nav-logo-link" aria-label="Iron Standard, home">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="Iron Standard" class="nav-logo">
    </a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">
      <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
      <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
    <nav class="nav-links" aria-label="Primary">
      <a href="about.html" aria-current="page">About Us</a>
      <a href="facility.html">The Facility</a>
      <a href="coaching.html">Coaching</a>
      <a href="faq.html">FAQ</a>
      <a href="contact.html">Contact Us</a>
      <a href="waitlist.html" class="btn-primary">Join the waitlist</a>
    </nav>
  </header>
  <main>
    <div class="page-header">
      <p class="kicker">About Us</p>
      <h1>Built by someone who's lived the gap</h1>
    </div>

    <section class="section" data-reveal>
      <!--
        Anthony is writing the final narrative for this page himself
        (his 16 Sep brief: "I'll write the final narrative copy myself
        and send it through"). The paragraph below is a placeholder,
        built only from the facts he already supplied in that same
        email — it isn't invented, and it isn't in his voice as a
        quote, but it IS provisional. Swap the text inside this <p>
        once his copy lands; nothing else on the page needs to change.
      -->
      <p>Anthony McCoy spent ten years coaching athletes from their first session to national level, and competed as a national athlete himself, three times over. He came up through a Sports Management background before stepping inside SATS Fagerborg in Oslo, where the gap became impossible to ignore: one of the highest gym participation rates anywhere in the world, and almost nothing built for people who actually train hard. Iron Standard is what happens when someone who has coached that exact gap decides to close it.</p>
    </section>

    <section class="section" data-reveal>
      <p class="kicker">Background</p>
      <ul class="pillars">
        <li><strong>Ten years coaching</strong> athletes from beginner to national level.</li>
        <li><strong>Three-time national athlete</strong>, competing at the top of his own sport.</li>
        <li><strong>Sports Management background</strong>, before stepping into gym ownership.</li>
        <li><strong>Worked inside SATS Fagerborg, Oslo</strong>, and saw the gap first-hand.</li>
      </ul>
    </section>

    <section class="section" data-reveal>
      <p class="kicker">Strategic advisor</p>
      <p><strong>Thomas Lilley</strong> is the founder of <strong>Zero Weakness</strong>, an established performance-gym operator with eleven locations across Australia, New Zealand and Europe. Iron Standard localises that proven model for Oslo.</p>
      <a href="waitlist.html" class="btn-primary" style="margin-top: 1.5rem;">Join the waitlist</a>
    </section>
  </main>
  <footer id="footer" class="site-footer">
    <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="Iron Standard" class="footer-logo">
    <p class="footer-location">
      <svg class="location-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11Z"/><circle cx="12" cy="10" r="2.5"/></svg>
      <span>Oslo, Norway</span>
    </p>
    <p><a href="mailto:anthonygmccoy@gmail.com" class="accent-link">anthonygmccoy@gmail.com</a></p>
    <p class="footer-copyright">&copy; 2026 Iron Standard. All rights reserved.</p>
  </footer>
  <script src="assets/js/main.js" defer></script>
</body>
</html>
```

Note: `style="margin-top: 1.5rem;"` on the inline CTA is the one inline style in this plan. It's acceptable here because it's a one-off spacing nudge on a single non-reused element, not a pattern — if a second page needs the same spacing, promote it to a class instead of copying the inline style (see Task 5, which does exactly that with a real class).

- [ ] **Step 3: Verify in the browser**

```javascript
({
  title: document.title,
  hasPageHeader: !!document.querySelector('.page-header'),
  navCurrentIsAbout: document.querySelector('.nav-links a[aria-current="page"]')?.textContent.trim(),
  pillarsCount: document.querySelectorAll('.pillars li').length,
})
```
Expected: `title` starts with "About Us", `hasPageHeader: true`, `navCurrentIsAbout: "About Us"`, `pillarsCount: 4`.

- [ ] **Step 4: Commit**

```bash
git add about.html assets/css/style.css
git commit -m "Add page-header component and the About Us page"
```

---

### Task 5: The Facility page

**Files:**
- Create: `facility.html`

**Interfaces:**
- Consumes: `.page-header` (Task 4), nav markup (Task 1), `.pillars` (existing), `.info-thumb`-style imagery pattern (existing, reused here as a plain `<img>` with the same filter class rather than inside a `<details>`).
- Produces: a new small utility class `.section-media` (image + caption pair) that Task 5 introduces and Task 6 (Coaching) does not need, but is safe for later pages to reuse if a similar image+caption block is wanted.

- [ ] **Step 1: Add `.section-media` CSS**

Append to `assets/css/style.css`:
```css
/* A single full-width photo inside a .section, reusing the same
   grayscale treatment as every other photo on the site. Not the same
   component as .detail-visual-img (that one crossfades between 4 stacked
   images by CSS :has(); this is just one static photo per section). */
.section-media {
  width: 100%;
  max-width: 640px;
  height: 320px;
  object-fit: cover;
  border-radius: 8px;
  margin-top: 1.5rem;
  filter: grayscale(1) contrast(1.1) brightness(0.6);
}
```

- [ ] **Step 2: Create `facility.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Facility — Iron Standard, Oslo</title>
<meta name="theme-color" content="#0a0a0a">
<meta name="description" content="800m² in central Oslo. Competition-grade platforms and racks, a dedicated posing room, and 24/7 access — built for powerlifting, bodybuilding, street lifting, hyrox, and serious lifters generally.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=TASA+Orbiter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v=12">
</head>
<body>
  <div class="intro-splash" aria-hidden="true">
    <div class="intro-flash-stack">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-1.jpg" alt="" class="intro-flash is-active">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-2.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-3.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-4.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-5.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-6.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-7.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-8.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-9.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-10.jpg" alt="" class="intro-flash">
    </div>
    <div class="intro-caption">Coming soon</div>
    <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="" class="intro-logo">
    <div class="intro-whiteflash"></div>
  </div>
  <header class="site-header">
    <a href="index.html" class="nav-logo-link" aria-label="Iron Standard, home">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="Iron Standard" class="nav-logo">
    </a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">
      <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
      <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
    <nav class="nav-links" aria-label="Primary">
      <a href="about.html">About Us</a>
      <a href="facility.html" aria-current="page">The Facility</a>
      <a href="coaching.html">Coaching</a>
      <a href="faq.html">FAQ</a>
      <a href="contact.html">Contact Us</a>
      <a href="waitlist.html" class="btn-primary">Join the waitlist</a>
    </nav>
  </header>
  <main>
    <div class="page-header">
      <p class="kicker">The Facility</p>
      <h1>800m², built for one thing</h1>
      <p>Central Oslo. Competition-grade platforms and racks. Nothing borrowed, nothing bolted on.</p>
    </div>

    <section class="section" data-reveal>
      <p class="kicker">The equipment</p>
      <p>Competition-grade platforms and racks, plus specialist strength equipment built to the same spec as our equipment partners.</p>
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/inside-the-facility.jpg" alt="" class="section-media">
      <ul class="pillars" style="margin-top: 1.5rem;">
        <li><strong>Equipment partners:</strong> Zero Weakness and Texas Power Bars.</li>
      </ul>
    </section>

    <section class="section" data-reveal>
      <p class="kicker">The posing room</p>
      <p>A dedicated room, separate from the training floor.</p>
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/posing-room.jpg" alt="" class="section-media">
    </section>

    <section class="section" data-reveal>
      <p class="kicker">24/7 member access</p>
      <p>Train when you actually train. No opening hours to work around.</p>
    </section>

    <section class="section" data-reveal>
      <p class="kicker">Who trains here</p>
      <ul class="pillars">
        <li><strong>Powerlifting</strong></li>
        <li><strong>Bodybuilding</strong></li>
        <li><strong>Street lifting</strong></li>
        <li><strong>Hyrox</strong></li>
        <li><strong>Serious lifters generally</strong>, whether or not you compete.</li>
      </ul>
      <p>Built for a broad range of serious training, not one discipline.</p>
    </section>

    <section class="section" data-reveal>
      <!--
        Facility photos/renders follow once the fit-out begins, per
        Anthony's 16 Sep brief. The two photos already used above (the
        equipment floor, the posing room) are real client-supplied stills;
        everything else on this page is deliberately text-only rather than
        padded out with stock of a space that doesn't exist yet.
      -->
      <a href="waitlist.html" class="btn-primary">Join the waitlist</a>
    </section>
  </main>
  <footer id="footer" class="site-footer">
    <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="Iron Standard" class="footer-logo">
    <p class="footer-location">
      <svg class="location-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11Z"/><circle cx="12" cy="10" r="2.5"/></svg>
      <span>Oslo, Norway</span>
    </p>
    <p><a href="mailto:anthonygmccoy@gmail.com" class="accent-link">anthonygmccoy@gmail.com</a></p>
    <p class="footer-copyright">&copy; 2026 Iron Standard. All rights reserved.</p>
  </footer>
  <script src="assets/js/main.js" defer></script>
</body>
</html>
```

- [ ] **Step 3: Verify in the browser**

```javascript
({
  title: document.title,
  images: [...document.querySelectorAll('.section-media')].map(i => ({src: i.src.split('/').pop(), loaded: i.naturalWidth > 0})),
  audienceItems: document.querySelectorAll('.pillars li').length,
})
```
Expected: both `.section-media` images report `loaded: true` (they're the two already-live WordPress URLs), `audienceItems` totals 6 across both `.pillars` lists on the page (1 equipment-partners item + 5 audience items).

- [ ] **Step 4: Commit**

```bash
git add facility.html assets/css/style.css
git commit -m "Add The Facility page"
```

---

### Task 6: Coaching page

**Files:**
- Create: `coaching.html`

**Interfaces:**
- Consumes: `.page-header`, nav markup, `.pillars` — no new CSS.

- [ ] **Step 1: Create `coaching.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Coaching — Iron Standard, Oslo</title>
<meta name="theme-color" content="#0a0a0a">
<meta name="description" content="Online and nutrition programming at scale, independent PTs with their own client bases, and a hosted calendar of competitions and events.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=TASA+Orbiter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v=12">
</head>
<body>
  <div class="intro-splash" aria-hidden="true">
    <div class="intro-flash-stack">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-1.jpg" alt="" class="intro-flash is-active">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-2.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-3.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-4.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-5.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-6.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-7.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-8.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-9.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-10.jpg" alt="" class="intro-flash">
    </div>
    <div class="intro-caption">Coming soon</div>
    <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="" class="intro-logo">
    <div class="intro-whiteflash"></div>
  </div>
  <header class="site-header">
    <a href="index.html" class="nav-logo-link" aria-label="Iron Standard, home">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="Iron Standard" class="nav-logo">
    </a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">
      <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
      <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
    <nav class="nav-links" aria-label="Primary">
      <a href="about.html">About Us</a>
      <a href="facility.html">The Facility</a>
      <a href="coaching.html" aria-current="page">Coaching</a>
      <a href="faq.html">FAQ</a>
      <a href="contact.html">Contact Us</a>
      <a href="waitlist.html" class="btn-primary">Join the waitlist</a>
    </nav>
  </header>
  <main>
    <div class="page-header">
      <p class="kicker">Coaching</p>
      <h1>More than a room to lift alone in</h1>
    </div>

    <section class="section" data-reveal>
      <p class="kicker">Programming at scale</p>
      <p>Online coaching and nutrition programming, built to run for far more people than could ever fit in one room at once.</p>
    </section>

    <section class="section" data-reveal>
      <p class="kicker">Independent trainers</p>
      <p>Personal trainers operate out of the facility with their own client bases. They're not staff assigned to you, they're professionals you choose, working from the same standard of equipment and space.</p>
    </section>

    <section class="section" data-reveal>
      <p class="kicker">Competitions and events</p>
      <p>A hosted calendar of competitions and events. The part that makes this a community, not just a place to lift alone in.</p>
      <a href="waitlist.html" class="btn-primary" style="margin-top: 1.5rem;">Join the waitlist</a>
    </section>
  </main>
  <footer id="footer" class="site-footer">
    <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="Iron Standard" class="footer-logo">
    <p class="footer-location">
      <svg class="location-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11Z"/><circle cx="12" cy="10" r="2.5"/></svg>
      <span>Oslo, Norway</span>
    </p>
    <p><a href="mailto:anthonygmccoy@gmail.com" class="accent-link">anthonygmccoy@gmail.com</a></p>
    <p class="footer-copyright">&copy; 2026 Iron Standard. All rights reserved.</p>
  </footer>
  <script src="assets/js/main.js" defer></script>
</body>
</html>
```

- [ ] **Step 2: Verify in the browser**

```javascript
({
  title: document.title,
  sections: document.querySelectorAll('main .section').length,
  navCurrent: document.querySelector('.nav-links a[aria-current="page"]')?.textContent.trim(),
})
```
Expected: `sections: 3`, `navCurrent: "Coaching"`.

- [ ] **Step 3: Commit**

```bash
git add coaching.html
git commit -m "Add Coaching page"
```

---

### Task 7: FAQ page

**Files:**
- Create: `faq.html`

**Interfaces:**
- Consumes: `.page-header`, `.info-item`/`summary`/`.info-body` accordion CSS (already defined for Home's "What you're getting" section — reused here standalone, without the `.details-grid`/`.details-visual` two-column machinery, since FAQ needs no photo panel).

- [ ] **Step 1: Create `faq.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FAQ — Iron Standard, Oslo</title>
<meta name="theme-color" content="#0a0a0a">
<meta name="description" content="Opening timeline, location, who Iron Standard is for, and how founding membership works.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=TASA+Orbiter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v=12">
</head>
<body>
  <div class="intro-splash" aria-hidden="true">
    <div class="intro-flash-stack">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-1.jpg" alt="" class="intro-flash is-active">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-2.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-3.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-4.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-5.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-6.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-7.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-8.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-9.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-10.jpg" alt="" class="intro-flash">
    </div>
    <div class="intro-caption">Coming soon</div>
    <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="" class="intro-logo">
    <div class="intro-whiteflash"></div>
  </div>
  <header class="site-header">
    <a href="index.html" class="nav-logo-link" aria-label="Iron Standard, home">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="Iron Standard" class="nav-logo">
    </a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">
      <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
      <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
    <nav class="nav-links" aria-label="Primary">
      <a href="about.html">About Us</a>
      <a href="facility.html">The Facility</a>
      <a href="coaching.html">Coaching</a>
      <a href="faq.html" aria-current="page">FAQ</a>
      <a href="contact.html">Contact Us</a>
      <a href="waitlist.html" class="btn-primary">Join the waitlist</a>
    </nav>
  </header>
  <main>
    <div class="page-header">
      <p class="kicker">FAQ</p>
      <h1>Common questions</h1>
    </div>

    <!--
      Anthony is sending specific Q&As for this page (16 Sep brief:
      "I'll send specific Q&As"). The four below are safe placeholder
      answers, built only from facts already cleared elsewhere on the
      site, matching the four topics he named: opening timeline,
      location, who it's for, and how founding membership works. Replace
      the text inside each <div class="info-body"> when his real
      answers land; the <details>/<summary> structure doesn't need to
      change unless the question list itself changes.
    -->
    <section class="section details-accordion">
      <div class="details-list">
        <details class="info-item" name="ironstandard-faq" open>
          <summary><span class="info-label"><span>When does Iron Standard open?</span></span></summary>
          <div class="info-body">
            <p>We haven't locked in an exact date yet. Join the waitlist and you'll be the first to know the moment it's confirmed.</p>
          </div>
        </details>
        <details class="info-item" name="ironstandard-faq">
          <summary><span class="info-label"><span>Where is it located?</span></span></summary>
          <div class="info-body">
            <p>Central Oslo. The exact address isn't public yet, we'll share it here as soon as it's confirmed.</p>
          </div>
        </details>
        <details class="info-item" name="ironstandard-faq">
          <summary><span class="info-label"><span>Who is Iron Standard for?</span></span></summary>
          <div class="info-body">
            <p>Powerlifters, bodybuilders, street lifters, hyrox athletes, and anyone who trains seriously, whether or not you compete.</p>
          </div>
        </details>
        <details class="info-item" name="ironstandard-faq">
          <summary><span class="info-label"><span>How does founding membership work?</span></span></summary>
          <div class="info-body">
            <p>Everyone on the waitlist gets priority access and a discounted rate for a limited period once we open. Spots are capped, so the earlier you join, the better your position.</p>
          </div>
        </details>
      </div>
    </section>

    <section class="section">
      <a href="waitlist.html" class="btn-primary">Join the waitlist</a>
    </section>
  </main>
  <footer id="footer" class="site-footer">
    <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="Iron Standard" class="footer-logo">
    <p class="footer-location">
      <svg class="location-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11Z"/><circle cx="12" cy="10" r="2.5"/></svg>
      <span>Oslo, Norway</span>
    </p>
    <p><a href="mailto:anthonygmccoy@gmail.com" class="accent-link">anthonygmccoy@gmail.com</a></p>
    <p class="footer-copyright">&copy; 2026 Iron Standard. All rights reserved.</p>
  </footer>
  <script src="assets/js/main.js" defer></script>
</body>
</html>
```

Note: `name="ironstandard-faq"` is a deliberately different `<details>` group name than Home's `name="ironstandard-details"` — they must not share a group name, or opening an FAQ item on this page would have no effect on Home (different pages, different DOM, so this is actually a non-issue in practice), but using a distinct, page-relevant name keeps the markup self-documenting.

- [ ] **Step 2: Verify in the browser**

```javascript
({
  title: document.title,
  faqCount: document.querySelectorAll('.info-item').length,
  onlyFirstOpen: [...document.querySelectorAll('.info-item')].filter(d => d.open).length,
})
```
Expected: `faqCount: 4`, `onlyFirstOpen: 1`.

Click the second `<summary>` and confirm the first auto-closes (native `<details name="...">` behavior, already proven on Home):
```javascript
document.querySelectorAll('.info-item')[1].querySelector('summary').click();
[...document.querySelectorAll('.info-item')].map(d => d.open)
```
Expected: `[false, true, false, false]`.

- [ ] **Step 3: Commit**

```bash
git add faq.html
git commit -m "Add FAQ page"
```

---

### Task 8: Join the Waitlist page, shared form styles, and the Google Apps Script backend

**Files:**
- Create: `waitlist.html`
- Create: `google-apps-script/waitlist-handler.gs`
- Create: `google-apps-script/README.md`
- Modify: `assets/css/style.css:420-433` region (rename/generalize the `.waitlist` form styles to `.form-panel`) — this replaces the full-bleed background-photo variant of `.waitlist` (`.waitlist-bg`, `.waitlist::before`, `.waitlist-content`, `.waitlist-sub`) that hasn't been used since the single waitlist section was pulled out of `index.html` on 11 Sep; it keeps and renames the form/row/field/label/input rules, which are still exactly right.
- Modify: `assets/js/main.js` (append the shared form-submit handler)

**Interfaces:**
- Produces: `.form-panel`, `.form-panel-content`, `.form-row`, `.field`, `.hp-field` (honeypot), `.form-success` — the classes Task 9 (Contact) reuses without modification.
- Produces: the `data-form-name` attribute contract (`"waitlist"` or `"contact"`) that both the client-side JS and the `.gs` backend read to route a submission to the right Sheet tab.
- Produces: `FORM_ENDPOINT_PLACEHOLDER` string (`"REPLACE_WITH_APPS_SCRIPT_WEB_APP_URL"`) as the literal `action` value on both forms — Task 9's Contact form uses the exact same literal, since both forms POST to the same deployed Apps Script.

- [ ] **Step 1: Replace the old `.waitlist` CSS block with `.form-panel`**

In `assets/css/style.css`, find the block starting at (originally) line 420:
```css
/* Waitlist */
.waitlist {
  position: relative;
  max-width: none;
  padding: 0;
  min-height: 640px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  text-align: center;
}
.waitlist-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 20%;
  filter: grayscale(1) contrast(1.1) brightness(0.5);
}
.waitlist::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at center, rgba(10,10,10,0.55) 0%, rgba(10,10,10,0.88) 65%, var(--bg) 100%);
}
.waitlist-content {
  position: relative;
  z-index: 1;
  max-width: 520px;
  padding: var(--space-lg) 1.5rem;
  margin: 0 auto;
}
.waitlist .kicker { text-align: center; }
.waitlist-sub { color: var(--fg-dim); max-width: 440px; margin: 1rem auto 0; font-size: 1.05rem; }

.waitlist form { display: flex; flex-direction: column; gap: 1.25rem; margin: 2rem auto 0; }
.waitlist-row { display: flex; gap: 1rem; }
.waitlist .field { flex: 1; text-align: left; }
.waitlist label {
  display: block;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--fg-dim);
  margin-bottom: 0.5rem;
}
.waitlist input {
  width: 100%;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.18);
  color: var(--fg);
  padding: 0.9rem 1rem;
  font-family: var(--font-display);
  font-size: 1rem;
  min-height: 48px;
  transition: border-color 0.2s ease, background-color 0.2s ease;
}
.waitlist input:focus {
  outline: none;
  border-color: var(--accent);
  background: rgba(255, 255, 255, 0.07);
}
.waitlist button { align-self: center; padding: 1rem 2.5rem; }
@media (max-width: 560px) {
  .waitlist-row { flex-direction: column; gap: 1.25rem; }
}
```

Replace the entire block with:
```css
/* Form panel — used by both waitlist.html and contact.html. This replaces
   the old .waitlist rules from the single-page build's full-bleed,
   background-photo waitlist section, which hasn't been used since that
   section was pulled out of index.html on 11 Sep. The photo/vignette
   half of that pattern (.waitlist-bg, .waitlist::before) is gone for
   good, since both new pages use the plain .page-header band like every
   other inner page instead. The form/row/field/input rules underneath
   were already exactly right, just renamed off "waitlist" since Contact
   needs them too. */
.form-panel-content {
  max-width: 520px;
  margin: 0 auto;
  text-align: center;
}
.form-panel form { display: flex; flex-direction: column; gap: 1.25rem; margin: 2rem auto 0; }
.form-row { display: flex; gap: 1rem; }
.form-panel .field { flex: 1; text-align: left; }
.form-panel label {
  display: block;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--fg-dim);
  margin-bottom: 0.5rem;
}
.form-panel input,
.form-panel textarea {
  width: 100%;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.18);
  color: var(--fg);
  padding: 0.9rem 1rem;
  font-family: var(--font-display);
  font-size: 1rem;
  min-height: 48px;
  transition: border-color 0.2s ease, background-color 0.2s ease;
}
.form-panel textarea { min-height: 120px; resize: vertical; }
.form-panel input:focus,
.form-panel textarea:focus {
  outline: none;
  border-color: var(--accent);
  background: rgba(255, 255, 255, 0.07);
}
.form-panel button { align-self: center; padding: 1rem 2.5rem; border: none; cursor: pointer; }
@media (max-width: 560px) {
  .form-row { flex-direction: column; gap: 1.25rem; }
}

/* Honeypot: invisible to a real visitor (off-screen, not display:none —
   some bots skip display:none fields specifically but still fill
   off-screen ones, so this is the more effective of the two cheap
   options). Not bulletproof, just enough to filter unsophisticated bot
   traffic without adding a reCAPTCHA dependency for a marginal gain at
   this site's traffic scale. */
.hp-field {
  position: absolute;
  left: -9999px;
  width: 1px;
  height: 1px;
  overflow: hidden;
}

.form-success { display: none; }
.form-panel.is-submitted form { display: none; }
.form-panel.is-submitted .form-success { display: block; }
```

- [ ] **Step 2: Write the shared form-submit JS**

Append to `assets/js/main.js`, inside the `DOMContentLoaded` callback, after the nav toggle block from Task 1:
```javascript
  // --- Forms: POST to a hidden iframe so the page never navigates away,
  // then swap the form for a success message once the iframe finishes
  // loading (which happens right after the Apps Script backend responds).
  // This works without a fetch() call and without a CORS-enabled endpoint
  // — Apps Script Web Apps don't return CORS headers for cross-origin
  // fetch(), but a classic form POST with a hidden iframe target doesn't
  // need them, since the page never reads the response body. See the
  // <noscript> next to each form for what a non-JS visitor sees instead:
  // the submission still succeeds (the browser POSTs regardless of JS),
  // they just don't get the friendly on-page confirmation.
  document.querySelectorAll('form[data-form-name]').forEach((form) => {
    const targetName = form.getAttribute('target');
    const iframe = targetName ? document.querySelector(`iframe[name="${targetName}"]`) : null;
    const panel = form.closest('.form-panel');
    if (!iframe || !panel) return;
    let submitted = false;
    form.addEventListener('submit', () => { submitted = true; });
    iframe.addEventListener('load', () => {
      // The iframe's own initial blank load also fires 'load' — ignore it,
      // only react once an actual form submission has happened.
      if (!submitted) return;
      panel.classList.add('is-submitted');
    });
  });
```

- [ ] **Step 3: Create `waitlist.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Join the Waitlist — Iron Standard, Oslo</title>
<meta name="theme-color" content="#0a0a0a">
<meta name="description" content="Priority access and a founding-member rate for people who join before Iron Standard opens in Oslo.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=TASA+Orbiter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v=12">
</head>
<body>
  <div class="intro-splash" aria-hidden="true">
    <div class="intro-flash-stack">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-1.jpg" alt="" class="intro-flash is-active">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-2.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-3.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-4.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-5.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-6.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-7.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-8.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-9.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-10.jpg" alt="" class="intro-flash">
    </div>
    <div class="intro-caption">Coming soon</div>
    <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="" class="intro-logo">
    <div class="intro-whiteflash"></div>
  </div>
  <header class="site-header">
    <a href="index.html" class="nav-logo-link" aria-label="Iron Standard, home">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="Iron Standard" class="nav-logo">
    </a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">
      <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
      <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
    <nav class="nav-links" aria-label="Primary">
      <a href="about.html">About Us</a>
      <a href="facility.html">The Facility</a>
      <a href="coaching.html">Coaching</a>
      <a href="faq.html">FAQ</a>
      <a href="contact.html">Contact Us</a>
      <a href="waitlist.html" class="btn-primary" aria-current="page">Join the waitlist</a>
    </nav>
  </header>
  <main>
    <div class="page-header">
      <!--
        Anthony is workshopping the exact offer wording himself (16 Sep
        brief). The h1 and intro paragraph below are placeholders built
        only from the structural brief he gave — "should feel like a
        real, capped opportunity rather than a generic sign-up" — not
        his final copy. Swap the text once it lands.
      -->
      <p class="kicker">Join the Waitlist</p>
      <h1>Get in before the doors open</h1>
      <p>Founding members get priority access and a discounted rate, before Iron Standard opens to the public.</p>
    </div>

    <section class="section" data-reveal>
      <ul class="pillars">
        <li><strong>Priority access</strong> when doors open.</li>
        <li><strong>A discounted rate</strong>, for a limited period only.</li>
        <li><strong>Capped spots</strong>, first come, first served — anything unclaimed passes to the next person on the list.</li>
      </ul>
    </section>

    <section class="section form-panel" id="form" data-reveal>
      <div class="form-panel-content">
        <p class="kicker">Sign up</p>
        <form method="POST" action="REPLACE_WITH_APPS_SCRIPT_WEB_APP_URL" target="isl-form-target" data-form-name="waitlist">
          <input type="hidden" name="form" value="waitlist">
          <div class="hp-field" aria-hidden="true">
            <label for="waitlist-website">Website</label>
            <input type="text" id="waitlist-website" name="website" tabindex="-1" autocomplete="off">
          </div>
          <div class="form-row">
            <div class="field">
              <label for="waitlist-name">Name</label>
              <input type="text" id="waitlist-name" name="name" required autocomplete="name">
            </div>
            <div class="field">
              <label for="waitlist-email">Email</label>
              <input type="email" id="waitlist-email" name="email" required autocomplete="email">
            </div>
          </div>
          <button type="submit" class="btn-primary">Join the waitlist</button>
        </form>
        <p class="form-success" hidden>Thanks — you're on the list. We'll be in touch.</p>
        <noscript><p>After you submit, the page will look like nothing happened — that's expected. Your details have been received.</p></noscript>
      </div>
    </section>
    <iframe name="isl-form-target" hidden title="Form submission target"></iframe>
  </main>
  <footer id="footer" class="site-footer">
    <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="Iron Standard" class="footer-logo">
    <p class="footer-location">
      <svg class="location-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11Z"/><circle cx="12" cy="10" r="2.5"/></svg>
      <span>Oslo, Norway</span>
    </p>
    <p><a href="mailto:anthonygmccoy@gmail.com" class="accent-link">anthonygmccoy@gmail.com</a></p>
    <p class="footer-copyright">&copy; 2026 Iron Standard. All rights reserved.</p>
  </footer>
  <script src="assets/js/main.js" defer></script>
</body>
</html>
```

- [ ] **Step 4: Create the Apps Script backend**

Create `google-apps-script/waitlist-handler.gs`:
```javascript
/**
 * Iron Standard — form submission handler.
 *
 * Deployed as a Google Apps Script Web App, bound to the Google Sheet
 * Anthony owns. Both the waitlist form (waitlist.html) and the contact
 * form (contact.html) POST here; the hidden `form` input tells this
 * script which Sheet tab a submission belongs to, so waitlist sign-ups
 * and contact enquiries never mix in the same count.
 *
 * See README.md in this folder for the one-time deployment steps —
 * those steps happen inside Anthony's own Google account and can't be
 * scripted from outside it.
 */
function doPost(e) {
  var params = e.parameter;

  // Honeypot: a real visitor never fills this hidden field. A bot that
  // blindly fills every input on the page does. Silently accept the
  // request (no error shown to the bot) but never write a row for it.
  if (params.website) {
    return jsonResponse({ ok: true });
  }

  var isContact = params.form === 'contact';
  var tabName = isContact ? 'Contact' : 'Waitlist';
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  var tab = sheet.getSheetByName(tabName);
  if (!tab) {
    tab = sheet.insertSheet(tabName);
    var header = isContact
      ? ['Timestamp', 'Name', 'Email', 'Message']
      : ['Timestamp', 'Name', 'Email'];
    tab.appendRow(header);
  }

  var timestamp = new Date();
  var row = isContact
    ? [timestamp, params.name, params.email, params.message]
    : [timestamp, params.name, params.email];
  tab.appendRow(row);

  var subject = isContact
    ? 'Iron Standard: new contact enquiry'
    : 'Iron Standard: new waitlist sign-up';
  var bodyLines = ['Name: ' + params.name, 'Email: ' + params.email];
  if (isContact) bodyLines.push('Message: ' + params.message);
  bodyLines.push('', 'Logged: ' + timestamp);
  MailApp.sendEmail(Session.getActiveUser().getEmail(), subject, bodyLines.join('\n'));

  return jsonResponse({ ok: true });
}

function jsonResponse(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
```

- [ ] **Step 5: Write the deployment README for the Apps Script**

Create `google-apps-script/README.md`:
```markdown
# Iron Standard — form backend (Google Apps Script)

`waitlist-handler.gs` in this folder receives both the waitlist form
(`waitlist.html`) and the contact form (`contact.html`) submissions and
writes each into its own tab of a Google Sheet, plus emails a
notification for every new row.

This has to be deployed from inside Anthony's own Google account — it
can't be scripted from outside it. One-time setup:

1. Create (or open) the Google Sheet that will hold submissions.
2. In that Sheet, **Extensions > Apps Script**.
3. Delete the default empty `Code.gs` content, and paste in the contents
   of `waitlist-handler.gs` from this folder.
4. **Deploy > New deployment > Web app.**
   - Execute as: **Me**.
   - Who has access: **Anyone**. (This has to be public so the form on
     the live site can reach it. It is not a secret — Apps Script Web
     Apps are meant to work this way, the same way the URL you're
     about to copy is not an API key.)
5. Click Deploy, authorize the script when Google prompts for it, and
   copy the **Web app URL** it gives you.
6. In the site's `waitlist.html` and `contact.html`, replace every
   occurrence of `REPLACE_WITH_APPS_SCRIPT_WEB_APP_URL` with that real
   URL (one `<form action="...">` per file).
7. Submit a test entry through the live waitlist form and confirm a row
   appears in the Sheet and a notification email arrives.

**If you ever need to change the script:** edit it in the Apps Script
editor, then **Deploy > Manage deployments > edit (pencil icon) > New
version > Deploy**. Editing the code alone does not update the live
Web App URL's behavior until you deploy a new version.

**Two tabs, one Sheet:** submissions land on a "Waitlist" tab or a
"Contact" tab depending on which form sent them, so a contact enquiry
never inflates the waitlist count. Both tabs are created automatically
on first submission — nothing to set up by hand.
```

- [ ] **Step 6: Verify the client-side wiring in the browser (without a real deployed Apps Script)**

The Apps Script itself can't be end-to-end tested until Anthony deploys it (Step 5's manual steps), but the client-side submit/success-swap logic can be verified independently:

```javascript
({
  formAction: document.querySelector('form[data-form-name="waitlist"]').getAttribute('action'),
  hasHoneypot: !!document.querySelector('#waitlist-website'),
  honeypotHidden: getComputedStyle(document.querySelector('.hp-field')).position === 'absolute' && getComputedStyle(document.querySelector('.hp-field')).left.startsWith('-'),
  iframeTargetMatches: document.querySelector('form[data-form-name="waitlist"]').getAttribute('target') === document.querySelector('iframe[name]')?.getAttribute('name'),
})
```
Expected: `formAction: "REPLACE_WITH_APPS_SCRIPT_WEB_APP_URL"`, `hasHoneypot: true`, `honeypotHidden: true`, `iframeTargetMatches: true`.

To verify the success-swap logic fires correctly, temporarily change the form's `action` to a same-origin URL that returns *any* response (e.g. `action="index.html"` for this test only), submit the form with the Name/Email fields filled, and confirm:
```javascript
document.querySelector('.form-panel').classList.contains('is-submitted')
```
Expected: `true` after the iframe finishes loading. Revert the `action` attribute back to `REPLACE_WITH_APPS_SCRIPT_WEB_APP_URL` afterward — this was a test-only substitution, not a real change.

- [ ] **Step 7: Commit**

```bash
git add waitlist.html google-apps-script assets/css/style.css assets/js/main.js
git commit -m "Add Join the Waitlist page and the Google Apps Script form backend"
```

---

### Task 9: Contact Us page

**Files:**
- Create: `contact.html`
- Modify: `assets/css/style.css` (append `.social-links` and `.address-note` styles)

**Interfaces:**
- Consumes: `.form-panel`, `.form-row`, `.field`, `.hp-field`, `.form-success` (Task 8) — reused with zero changes, plus a `<textarea name="message">` the shared `.form-panel textarea` CSS from Task 8 already styles.
- Consumes: the shared form-submit JS from Task 8 (already generic over any `form[data-form-name]`, no Contact-specific JS needed).

- [ ] **Step 1: Add `.social-links` CSS**

Append to `assets/css/style.css`:
```css
/* Contact page: social links aren't supplied yet (per Anthony's 16 Sep
   brief, "needed for Contact, not yet supplied"). Rather than ship dead
   '#' links or invent URLs, this renders one honest line of real text
   until real links exist. */
.social-links-note { color: var(--fg-dim); }
```

- [ ] **Step 2: Create `contact.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Contact Us — Iron Standard, Oslo</title>
<meta name="theme-color" content="#0a0a0a">
<meta name="description" content="Get in touch with Iron Standard, Oslo.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=TASA+Orbiter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v=12">
</head>
<body>
  <div class="intro-splash" aria-hidden="true">
    <div class="intro-flash-stack">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-1.jpg" alt="" class="intro-flash is-active">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-2.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-3.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-4.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-5.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-6.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-7.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-8.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-9.jpg" alt="" class="intro-flash">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/flash-10.jpg" alt="" class="intro-flash">
    </div>
    <div class="intro-caption">Coming soon</div>
    <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="" class="intro-logo">
    <div class="intro-whiteflash"></div>
  </div>
  <header class="site-header">
    <a href="index.html" class="nav-logo-link" aria-label="Iron Standard, home">
      <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="Iron Standard" class="nav-logo">
    </a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">
      <svg class="icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
      <svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
    </button>
    <nav class="nav-links" aria-label="Primary">
      <a href="about.html">About Us</a>
      <a href="facility.html">The Facility</a>
      <a href="coaching.html">Coaching</a>
      <a href="faq.html">FAQ</a>
      <a href="contact.html" aria-current="page">Contact Us</a>
      <a href="waitlist.html" class="btn-primary">Join the waitlist</a>
    </nav>
  </header>
  <main>
    <div class="page-header">
      <p class="kicker">Contact Us</p>
      <h1>Get in touch</h1>
      <p>Have a question that isn't on the FAQ? Send it here.</p>
    </div>

    <section class="section form-panel" data-reveal>
      <div class="form-panel-content">
        <form method="POST" action="REPLACE_WITH_APPS_SCRIPT_WEB_APP_URL" target="isl-form-target" data-form-name="contact">
          <input type="hidden" name="form" value="contact">
          <div class="hp-field" aria-hidden="true">
            <label for="contact-website">Website</label>
            <input type="text" id="contact-website" name="website" tabindex="-1" autocomplete="off">
          </div>
          <div class="form-row">
            <div class="field">
              <label for="contact-name">Name</label>
              <input type="text" id="contact-name" name="name" required autocomplete="name">
            </div>
            <div class="field">
              <label for="contact-email">Email</label>
              <input type="email" id="contact-email" name="email" required autocomplete="email">
            </div>
          </div>
          <div class="field" style="text-align: left;">
            <label for="contact-message">Message</label>
            <textarea id="contact-message" name="message" required></textarea>
          </div>
          <button type="submit" class="btn-primary">Send</button>
        </form>
        <p class="form-success" hidden>Thanks — your message has been received. We'll be in touch.</p>
        <noscript><p>After you submit, the page will look like nothing happened — that's expected. Your message has been received.</p></noscript>
      </div>
    </section>
    <iframe name="isl-form-target" hidden title="Form submission target"></iframe>

    <section class="section" data-reveal>
      <p class="kicker">Email</p>
      <p><a href="mailto:anthonygmccoy@gmail.com" class="accent-link">anthonygmccoy@gmail.com</a></p>
    </section>

    <section class="section" data-reveal>
      <p class="kicker">Social</p>
      <p class="social-links-note">Social links are coming soon.</p>
    </section>

    <!--
      Address block: intentionally not rendered. Location isn't locked
      in yet (16 Sep brief: "no physical address yet... keep that section
      easy to update later"). When Anthony confirms an address, add a new
      section here following the same .section/.kicker pattern as the
      Email section above — a one-paragraph addition, not a layout change.
    -->
  </main>
  <footer id="footer" class="site-footer">
    <img src="https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/logo-white-scaled.png" alt="Iron Standard" class="footer-logo">
    <p class="footer-location">
      <svg class="location-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11Z"/><circle cx="12" cy="10" r="2.5"/></svg>
      <span>Oslo, Norway</span>
    </p>
    <p><a href="mailto:anthonygmccoy@gmail.com" class="accent-link">anthonygmccoy@gmail.com</a></p>
    <p class="footer-copyright">&copy; 2026 Iron Standard. All rights reserved.</p>
  </footer>
  <script src="assets/js/main.js" defer></script>
</body>
</html>
```

- [ ] **Step 3: Verify in the browser**

```javascript
({
  title: document.title,
  formAction: document.querySelector('form[data-form-name="contact"]').getAttribute('action'),
  hasTextarea: !!document.querySelector('textarea[name="message"]'),
  hasHoneypot: !!document.querySelector('#contact-website'),
  noFakeSocialLinks: document.querySelectorAll('.social-links-note a').length === 0,
})
```
Expected: `formAction: "REPLACE_WITH_APPS_SCRIPT_WEB_APP_URL"`, `hasTextarea: true`, `hasHoneypot: true`, `noFakeSocialLinks: true` (confirms no placeholder `#` links were shipped).

- [ ] **Step 4: Commit**

```bash
git add contact.html assets/css/style.css
git commit -m "Add Contact Us page"
```

---

### Task 10: README overhaul

**Files:**
- Modify: `README.md` (full rewrite of structure; existing per-detail notes about the hero photo, mobile rules, and image sourcing are preserved verbatim where still accurate)

**Interfaces:**
- Consumes: nothing new — this is documentation only, no code interface.

- [ ] **Step 1: Rewrite `README.md`**

Keep every existing note that is still true unmodified (the "hero is a single fixed photo" section, the "mobile hero rules" section, the "two images are not in the media library yet" section — wait, check: those two images **are** now in the media library, per the 14 Sep work already done; re-verify against the live site before assuming this note is stale) — verify first:

```bash
curl -sI "https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/inside-the-facility.jpg" | head -1
curl -sI "https://iron.standard.10xstudios.co/wp-content/uploads/2026/09/posing-room.jpg" | head -1
```
If both return `HTTP/... 200`, that section of the README is stale (the images were uploaded since it was written) and should be deleted rather than carried forward. If either returns 404, keep that section as-is.

Replace the file with (adjusting the two-images section per the check above):

```markdown
# Iron Standard — Full Site

Static site, no build step. Open `index.html` directly, or serve the folder with any static host (`.claude/launch.json` has a local preview server registered as `ironstandard-lp` on port 8140).

## Pages

| Page | File | Purpose |
|---|---|---|
| Home | `index.html` | Brand tone, positioning, links to everything else |
| About Us | `about.html` | Founder story — Anthony's own narrative pending |
| The Facility | `facility.html` | The 800m² space, equipment, posing room |
| Coaching | `coaching.html` | Programming, independent PTs, events |
| Join the Waitlist | `waitlist.html` | The founding-member offer and sign-up form |
| FAQ | `faq.html` | Opening timeline, location, audience, founding membership |
| Contact Us | `contact.html` | Contact form, email, social (pending) |

Nav (`.site-header`, hand-duplicated into every page's `<body>` — there's
no templating engine, so it's a copy in each file, same as
`partials/footer.html` already documents itself as "a copy, not an
include") links all 7 pages together. `waitlist.html` carries `id="form"`
inside its form section — every "Join the waitlist" link across the site
points at `waitlist.html`, and the button/scroll-arrow pattern from the
single-page build era is gone (there's nothing to scroll to any more,
Waitlist is its own page).

**The intro flash-and-logo sequence plays once per browser session, not
once per page** (`sessionStorage`, see `assets/js/main.js`). Landing on
any page for the first time in a session plays it; clicking to another
page goes straight in. A new tab (fresh session) sees it again.

## Data flow — Google Sheets, not Brevo

Anthony confirmed he's going with a Google Sheet, replacing the
Brevo-based plan from the original single-page build. See
`google-apps-script/README.md` for the full deployment steps — they
have to run inside Anthony's own Google account, nothing here can be
scripted. Short version: both forms POST to a Google Apps Script Web
App, which appends a row to the "Waitlist" or "Contact" tab of a Sheet
he owns, and emails him a notification per submission.

**Before either form works, `REPLACE_WITH_APPS_SCRIPT_WEB_APP_URL` in
`waitlist.html` and `contact.html` needs to become the real deployed
Web App URL.** Until then, every "Join the waitlist" and "Send" button
on the site submits to a URL that doesn't exist. This is the same kind
of placeholder the single-page build shipped with while waiting on
Brevo — nothing is broken, it's just not live yet.

**Never** switch either form to a `fetch()` call with a credential in
the JavaScript. The Apps Script Web App URL being public is fine — it's
not a secret, that's how Apps Script Web Apps are meant to work — but no
*other* kind of API key belongs in this codebase's client-side JS,
matching the same rule the original Brevo build followed.

## Hosting

Still unresolved as of this rewrite: Anthony asked 10x to host the site
(replacing the original Netlify-under-his-own-account plan), but which
of 10x's existing hosting arrangements that lands on hasn't been decided.
`netlify.toml` is left in place and untouched — it works under Netlify
regardless of whose account it's deployed from, so this doesn't block
building or reviewing the pages themselves. Domain stays at GoDaddy as
registrar either way; only DNS target changes once hosting is decided.

## Export existing leads from the current GoDaddy site first

Before retiring `ironstandard.no`'s current "Launching Soon" page, log
into GoDaddy Website Builder and check the form responses it's been
collecting — export anything there and add it to the new waitlist Sheet
so no early signups are lost.

## Footer partial

`partials/footer.html` is a standalone copy of the footer (self-contained,
loads the same font/CSS with adjusted relative paths) so it can be
grabbed and reused without digging through a full page's markup. It's a
copy, not an include: editing one doesn't update any of the 7 pages'
inline footers.

## What's still needed

- **Real copy for three pages**, all explicitly pending from Anthony:
  the About Us narrative, the Waitlist offer wording, and the FAQ
  questions and answers. Each page currently ships accurate placeholder
  copy built only from his 16 Sep email, flagged with an HTML comment
  at the exact spot to swap it in.
- **Facility photography.** Two client-supplied stills are live
  (`inside-the-facility.jpg`, `posing-room.jpg`); real photos/renders
  follow once the fit-out begins, per Anthony.
- **Social links for Contact** — not yet supplied. The page currently
  says "Social links are coming soon" rather than shipping dead or
  invented links.
- **The Apps Script deployment** — see Data flow above.
- **Hosting target** — see Hosting above.
- No favicon yet — the only logo files on hand are the 3165x370 extended
  wordmark, and Iron Standard's own brand guidelines forbid cropping or
  altering the brandmark. Their monogram mark (the compact square version
  made for exactly this) is listed as "Work In Progress" in their
  guidelines — add a favicon once that ships.
- Analytics if wanted (Plausible or GA4 — not wired in yet).

## Notes carried over from the single-page build

**The hero is a single fixed photo.** It used to rotate through 4 clips
every 2.2s, which read as the page fading to black and back long after
the intro had finished. It's now one still
(`young-man-sportswear-exercise-class-gym-scaled.jpg`) at
`position: fixed`, so it holds steady while the content scrolls up over
it. The clips in `assets/video/` are no longer referenced by anything
and the rotation code is gone from `main.js`. Because the photo is
fixed, everything below the hero has to sit on an opaque band or the
photo shows through it — that's what the `.page-rest` wrapper and the
`background` on `.site-footer` are for, on `index.html` only (the 6
inner pages have no hero and no fixed photo, so they don't need this).

**Mobile hero rules.** Three things in the hero are viewport-dependent
and easy to break by "tidying":
- The h1 is one sentence with two sets of `<br>`. `.br-d` shows above
  640px, `.br-m` shows at 640px and below. Don't replace them with
  duplicated headings.
- `.hero-bg` uses `height: 100lvh`, never `100vh` or `100%`. On a phone
  the URL bar collapses on first scroll, which changes the viewport
  height, which makes `object-fit: cover` re-crop the photo — it looks
  exactly like the image popping and zooming. `lvh` is the largest
  viewport height and never changes, so the crop is computed once.
- `.hero` uses `min-height: 100svh` for the opposite reason: `svh` is
  the smallest viewport height, so the hero's own content always fits
  above the fold with the URL bar showing.
```

(If the curl check in Step 1 found the two images still return 404, re-insert the "Two images are NOT in the media library yet" paragraph from the pre-existing README, unmodified, into the "What's still needed" section.)

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "README: document the 7-page structure and the Apps Script data flow"
```

---

## Self-Review

**Spec coverage** — checked against every section of `docs/superpowers/specs/2026-09-16-ironstandard-full-site-design.md`:
- All 7 pages: Task 3 (Home), 4 (About), 5 (Facility), 6 (Coaching), 7 (FAQ), 8 (Waitlist), 9 (Contact). ✓
- Nav: Task 1. ✓
- Google Sheets replacing Brevo, honeypot, email notification, two tabs: Task 8. ✓
- Hosting note: explicitly out of scope per spec's own open items, documented in Task 10's README rewrite rather than acted on. ✓
- "What's explicitly not in this build" (pricing/date/address, forms not live until Apps Script deployed): reflected as HTML comments and README notes throughout, no task invents any of it. ✓
- Open items 2-5 from the spec (pending copy, photography, social links, spam/notification approach): each has a task-level flag (HTML comment) and a README line. ✓

**Gap found and added:** the intro-plays-once-per-session behavior isn't in the written spec at all (it surfaced during the earlier wireframe brainstorming round and was never carried into the prose spec). Added as Task 2, with its rationale stated plainly in the task itself rather than silently treated as spec-covered.

**Placeholder scan** — no "TBD"/"TODO" in any code block. Every piece of pending-from-Anthony copy is real, shippable, accurate text with an HTML comment explaining what replaces it and why, not a description of what to write.

**Type/name consistency** — checked across tasks: `.form-panel` / `.form-panel-content` / `.form-row` / `.field` / `.hp-field` / `.form-success` are introduced once in Task 8 and reused with identical names in Task 9. `data-form-name` values (`"waitlist"`, `"contact"`) match between each form's HTML attribute and the `.gs` file's `params.form === 'contact'` check. `FORM_ENDPOINT` literal string is identical (`REPLACE_WITH_APPS_SCRIPT_WEB_APP_URL`) in both forms. Nav markup (link hrefs, labels, order) is identical across all 7 pages' copies, verified by re-reading each Create step against the Task 1 template. `--z-nav`/`--z-intro` tokens are defined once (Task 1) and referenced, never redefined.
