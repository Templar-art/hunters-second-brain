# Iron Standard Landing Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a single static waitlist landing page for Iron Standard (`projects/ironstandard-lp/`) that reads as premium/dark/cinematic (Equinox-tier), collects name+email into Brevo, and is deploy-ready on Netlify with `ironstandard.no` pointed at it.

**Architecture:** One `index.html` + `assets/{css,js,img,video}/`, no build step, no framework. Font is Google-Fonts-hosted TASA Orbiter. Form posts client-side to Brevo (no backend).

**Tech Stack:** Plain HTML5, CSS (custom properties, flexbox/grid, no framework), vanilla JS (no dependencies), Google Fonts (TASA Orbiter), Brevo hosted form/API.

## Global Constraints

- Colour tokens: background `#0a0a0a` (near-black, not pure `#000` — matches guideline's "black" swatch feel while keeping shadow detail visible), text `#ffffff`, accent orange `#F4502A` — accent used ONLY for CTA button, link hover/underline, and at most one hairline divider per section. Never a background wash.
- Font: TASA Orbiter (Google Fonts). Bold + all-caps for headlines, semi-bold + all-caps for kickers/subtitles, regular mixed-case for body copy.
- Never rotate, recolour, restretch, add stroke/shadow to, or otherwise alter the IRONSTNDRD. logo lockup (guideline's own "Incorrect Usage" rules).
- Never gate real page content behind the load animation or any scroll-reveal script — content must exist and render in the DOM without JS; animation is a non-blocking enhancement (standing rule from `wiki/projects/10x-website.md`).
- No payment/booking functionality in this build — waitlist form (name + email) only.
- Photography/video direction: motion not static poses, mixed smiles/serious expressions, mixed camera angles, men and women shown at equal seriousness and load; equipment shots avoid faces (per Iron Standard's own brand guidelines PDF).
- File source: `~/Downloads/260529_IRONSTNDRD_Logo_*.png` (4 logo files: Extended/Stacked × Black/White) are the only brand assets already on disk — copy them in, don't regenerate.

---

## File Structure

```
projects/ironstandard-lp/
  index.html                 — full page, all 7 sections
  assets/css/style.css       — tokens, layout, all section styles, responsive
  assets/js/main.js          — hero video→logo sequence, load-in animation, form submit handler, mobile nav toggle
  assets/img/
    logo-white.png           — copied from Downloads (Extended Logo White)
    logo-black.png           — copied from Downloads (Extended Logo Black)
    hero-poster.jpg          — fallback still for hero (no-JS / slow connection)
    section-*.jpg            — stock photography for sections 2-4
  assets/video/
    hero-loop.mp4            — muted looping hero reel
  README.md                  — handoff: Brevo setup steps, Netlify deploy steps, DNS repoint steps, GoDaddy lead-export reminder
```

---

## Task 1: Scaffold + design tokens

**Files:**
- Create: `projects/ironstandard-lp/index.html`
- Create: `projects/ironstandard-lp/assets/css/style.css`

**Interfaces:**
- Produces: CSS custom properties `--bg`, `--fg`, `--accent`, `--font-display` (used by every later task's CSS).
- Produces: HTML section anchors `#hero`, `#what-it-is`, `#who-its-for`, `#whats-different`, `#founding-member`, `#waitlist`, `#footer` (used by nav/scroll-CTA in Task 4 and by JS in Task 5).

- [ ] **Step 1: Create the HTML skeleton with empty semantic sections**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Iron Standard — Oslo</title>
<meta name="description" content="A different standard for serious training. Founding-member waitlist for Iron Standard, Oslo's new 800m² strength facility.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=TASA+Orbiter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
  <header class="site-header"></header>
  <main>
    <section id="hero" class="section"></section>
    <section id="what-it-is" class="section"></section>
    <section id="who-its-for" class="section"></section>
    <section id="whats-different" class="section"></section>
    <section id="founding-member" class="section"></section>
    <section id="waitlist" class="section"></section>
  </main>
  <footer id="footer" class="site-footer"></footer>
  <script src="assets/js/main.js" defer></script>
</body>
</html>
```

- [ ] **Step 2: Write the CSS tokens and reset**

```css
:root {
  --bg: #0a0a0a;
  --fg: #ffffff;
  --fg-dim: #b8b8b8;
  --accent: #F4502A;
  --font-display: 'TASA Orbiter', sans-serif;
  --max-width: 1200px;
  --space-lg: clamp(3rem, 8vw, 8rem);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--bg);
  color: var(--fg);
  font-family: var(--font-display);
  font-weight: 400;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

h1, h2, h3, .kicker {
  font-family: var(--font-display);
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

h1 { font-weight: 700; font-size: clamp(2.5rem, 6vw, 5rem); line-height: 1.05; }
h2 { font-weight: 700; font-size: clamp(1.75rem, 4vw, 3rem); }
.kicker { font-weight: 600; font-size: 0.85rem; letter-spacing: 0.15em; color: var(--accent); }

.section { padding: var(--space-lg) 1.5rem; max-width: var(--max-width); margin: 0 auto; }

a { color: inherit; }
a.accent-link { color: var(--accent); text-decoration: none; border-bottom: 1px solid transparent; transition: border-color 0.2s; }
a.accent-link:hover { border-color: var(--accent); }

.btn-primary {
  display: inline-block;
  background: var(--accent);
  color: #0a0a0a;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.9rem 2rem;
  border: none;
  border-radius: 2px;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-primary:hover { opacity: 0.85; }
```

- [ ] **Step 3: Copy the logo assets in**

```bash
mkdir -p "/Users/10xhunter/Documents/Hunters Second Brain/projects/ironstandard-lp/assets/img"
cp "/Users/10xhunter/Downloads/260529_IRONSTNDRD_Logo_Extended Logo White.png" "/Users/10xhunter/Documents/Hunters Second Brain/projects/ironstandard-lp/assets/img/logo-white.png"
cp "/Users/10xhunter/Downloads/260529_IRONSTNDRD_Logo_Extended Logo Black.png" "/Users/10xhunter/Documents/Hunters Second Brain/projects/ironstandard-lp/assets/img/logo-black.png"
```

- [ ] **Step 4: Verify in browser**

Open `projects/ironstandard-lp/index.html` in the Browser pane. Expected: black page, no console errors, page title "Iron Standard — Oslo" in the tab.

- [ ] **Step 5: Commit**

```bash
git add projects/ironstandard-lp/index.html projects/ironstandard-lp/assets/css/style.css projects/ironstandard-lp/assets/img/logo-white.png projects/ironstandard-lp/assets/img/logo-black.png
git commit -m "Scaffold Iron Standard landing page: HTML skeleton + design tokens"
```

---

## Task 2: Write and place all section copy

**Files:**
- Modify: `projects/ironstandard-lp/index.html`

**Interfaces:**
- Consumes: section IDs from Task 1.
- Produces: final copy text nodes inside each `<section>` — later tasks (imagery, styling) wrap this content, they don't replace it.

- [ ] **Step 1: Fill in the hero section markup (text layer only — video comes in Task 3)**

```html
<section id="hero" class="section hero">
  <div class="hero-content">
    <img src="assets/img/logo-white.png" alt="Iron Standard" class="hero-logo">
    <p class="kicker">Oslo · Opening 2027</p>
    <h1>A different standard for serious training.</h1>
    <p class="hero-sub">800m² built for platforms, plates and people who actually use them. Founding-member waitlist now open.</p>
    <a href="#waitlist" class="btn-primary">Join the waitlist</a>
  </div>
</section>
```

- [ ] **Step 2: Fill in "What it is"**

```html
<section id="what-it-is" class="section">
  <p class="kicker">The facility</p>
  <h2>800m². Built to be used, not looked at.</h2>
  <p>Iron Standard is an 800m² purpose-built strength and performance facility opening in Oslo — proper platforms, calibrated plates, a dedicated posing room, and enough space to actually train the way you want to. Members get 24/7 access, not gym hours.</p>
</section>
```

- [ ] **Step 3: Fill in "Who it's for"**

```html
<section id="who-its-for" class="section">
  <p class="kicker">Who it's for</p>
  <h2>Serious lifters. Coached athletes. No exceptions made for either.</h2>
  <p>Strength and physique athletes, competitive and recreational, training several times a week. People who work with a coach or personal trainer, and the self-employed PTs and physiotherapists looking for a proper base to work from. If commercial gyms have felt crowded, under-equipped for heavy lifting, or restrictive about how you train — this is built for you instead.</p>
</section>
```

- [ ] **Step 4: Fill in "What's different" (4 pillars)**

```html
<section id="whats-different" class="section">
  <p class="kicker">What's different</p>
  <h2>Not a chain. Not a niche box either.</h2>
  <div class="pillars">
    <div class="pillar">
      <h3>Built for load</h3>
      <p>Proper platforms, calibrated plates, and space designed around how serious training actually happens.</p>
    </div>
    <div class="pillar">
      <h3>Coaching on-site</h3>
      <p>Semi-private and small-group programming, self-employed PTs, and a physiotherapist — all in the same building.</p>
    </div>
    <div class="pillar">
      <h3>A membership base to match</h3>
      <p>Everyone training to the same standard. What most serious lifters actually want from a gym.</p>
    </div>
    <div class="pillar">
      <h3>Run by someone from the industry</h3>
      <p>Founded by a coach who trains, coaches, and knows the Oslo scene — not an investor group chasing a franchise model.</p>
    </div>
  </div>
</section>
```

- [ ] **Step 5: Fill in "Founding member" hook**

```html
<section id="founding-member" class="section founding-member">
  <p class="kicker">Founding members</p>
  <h2>Sign up before we open, lock in founding-member standing.</h2>
  <p>Early registrations get priority access and founding-member terms when membership officially opens — ahead of the general public. No payment required to join the waitlist.</p>
</section>
```

- [ ] **Step 6: Verify in browser**

Use `get_page_text` on the opened page. Expected: all six section headlines and body paragraphs present in reading order, no lorem ipsum, no empty sections.

- [ ] **Step 7: Commit**

```bash
git add projects/ironstandard-lp/index.html
git commit -m "Add full section copy to Iron Standard landing page"
```

---

## Task 3: Source imagery + hero video, wire into markup

**⚠️ Requires explicit user permission before downloading any file — state each filename, source URL, and approximate size, and wait for a clear yes before fetching.**

**Files:**
- Create: `projects/ironstandard-lp/assets/img/hero-poster.jpg`
- Create: `projects/ironstandard-lp/assets/img/section-what-it-is.jpg`
- Create: `projects/ironstandard-lp/assets/img/section-who.jpg`
- Create: `projects/ironstandard-lp/assets/video/hero-loop.mp4`
- Modify: `projects/ironstandard-lp/index.html` (hero video tag, section background images)

**Interfaces:**
- Consumes: hero section markup from Task 2.
- Produces: `<video>`/`<img>` elements with classes `.hero-video`, `.section-img` that Task 4's CSS targets.

- [ ] **Step 1: Propose specific free-license stock sources to the user and get permission**

Search Pexels/Unsplash (free, commercial-use license, no attribution required) for: (a) one dark/moody strength-training video clip — chalk, barbell, plates, or a lifting silhouette, for the hero loop; (b) 2-3 still photos matching the guideline's photography direction (motion not posed, mixed genders at equal seriousness, warm dark grade) for the "What it is" and "Who it's for" sections. List the exact URLs, filenames, and sizes, and ask before downloading — this is a file-download action requiring explicit permission regardless of licensing cost.

- [ ] **Step 2: Download the approved files into place**

Save the approved video to `assets/video/hero-loop.mp4` and stills to `assets/img/`. Generate `hero-poster.jpg` as a still frame extracted from the hero video (or a separate approved still) for the no-JS/slow-connection fallback.

- [ ] **Step 3: Wire the hero video into the markup**

```html
<section id="hero" class="section hero">
  <video class="hero-video" autoplay muted loop playsinline poster="assets/img/hero-poster.jpg">
    <source src="assets/video/hero-loop.mp4" type="video/mp4">
  </video>
  <div class="hero-content">
    <!-- unchanged from Task 2 -->
  </div>
</section>
```

- [ ] **Step 4: Add section background images**

```html
<!-- inside #what-it-is, before the closing </section> -->
<img src="assets/img/section-what-it-is.jpg" alt="Iron Standard training floor" class="section-img" loading="lazy">
```

Repeat the pattern for `#who-its-for` with `section-who.jpg`.

- [ ] **Step 5: Verify in browser**

Screenshot the page. Expected: hero video plays muted and loops, poster shows before video loads, section images render with `loading="lazy"` and have non-empty `alt` text (check via `read_page`).

- [ ] **Step 6: Commit**

```bash
git add projects/ironstandard-lp/assets/img projects/ironstandard-lp/assets/video projects/ironstandard-lp/index.html
git commit -m "Add hero video and section imagery to Iron Standard landing page"
```

---

## Task 4: Full visual styling + responsive layout

**Files:**
- Modify: `projects/ironstandard-lp/assets/css/style.css`

**Interfaces:**
- Consumes: tokens from Task 1, markup/classes from Tasks 2-3 (`.hero`, `.hero-video`, `.hero-content`, `.hero-logo`, `.pillars`, `.pillar`, `.section-img`, `.founding-member`).
- Produces: final visual layout — no later task changes core layout CSS (Task 5's JS only toggles classes this task defines).

- [ ] **Step 1: Style the hero (full-bleed video, centered content, dark scrim for text contrast)**

```css
.hero {
  position: relative;
  min-height: 100vh;
  max-width: none;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.hero-video {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(0.55);
}
.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  max-width: 700px;
  padding: 0 1.5rem;
}
.hero-logo {
  width: 220px;
  max-width: 60vw;
  margin: 0 auto 1.5rem;
  opacity: 0;
  transform: translateY(12px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.hero-logo.is-visible { opacity: 1; transform: translateY(0); }
.hero-sub { color: var(--fg-dim); margin: 1rem 0 2rem; font-size: 1.1rem; }
```

- [ ] **Step 2: Style the pillars grid**

```css
.pillars {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  margin-top: 2.5rem;
}
.pillar h3 { font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem; }
.pillar p { color: var(--fg-dim); }
@media (max-width: 640px) {
  .pillars { grid-template-columns: 1fr; }
}
```

- [ ] **Step 3: Style section images and the founding-member callout**

```css
.section-img {
  width: 100%;
  height: auto;
  margin-top: 2rem;
  border-radius: 2px;
  filter: grayscale(0.1) contrast(1.05);
}
.founding-member {
  border-top: 1px solid rgba(244, 80, 42, 0.3);
  border-bottom: 1px solid rgba(244, 80, 42, 0.3);
}
```

- [ ] **Step 4: Verify responsive behaviour**

Use `resize_window` with `preset: "mobile"` then `preset: "tablet"` then `preset: "desktop"` on the open tab, screenshotting each. Expected: pillars stack to one column under 640px, hero text stays legible over the video at every width, no horizontal scrollbar at any width.

- [ ] **Step 5: Commit**

```bash
git add projects/ironstandard-lp/assets/css/style.css
git commit -m "Style Iron Standard landing page hero, pillars, and responsive layout"
```

---

## Task 5: Load-in animation + hero logo reveal (JS)

**Files:**
- Create: `projects/ironstandard-lp/assets/js/main.js`

**Interfaces:**
- Consumes: `.hero-logo` element and `.is-visible` CSS class from Task 4.
- Produces: nothing consumed by later tasks — this script is self-contained and must never block rendering of content it doesn't own.

- [ ] **Step 1: Write the reveal script**

```javascript
document.addEventListener('DOMContentLoaded', () => {
  const heroLogo = document.querySelector('.hero-logo');
  if (heroLogo) {
    // Content is already visible in the DOM without this script running —
    // this only adds a fade/rise polish on top. Never gate content on it.
    requestAnimationFrame(() => {
      setTimeout(() => heroLogo.classList.add('is-visible'), 150);
    });
  }
});
```

- [ ] **Step 2: Verify content renders with JS disabled**

In the Browser pane, use `javascript_tool` to check: `document.querySelector('.hero-content').textContent.length > 0` returns true even before `main.js` finishes running (check by reading the raw HTML via `read_page` — the h1/p text must be literal markup, not injected by JS). Confirm no section is `display:none` or `opacity:0` by default in the CSS (only `.hero-logo` starts at opacity 0, and only for 150-750ms).

- [ ] **Step 3: Verify in browser**

Reload the page and screenshot. Expected: logo fades/rises into place within under a second, rest of hero content is present immediately, no flash of unstyled content.

- [ ] **Step 4: Commit**

```bash
git add projects/ironstandard-lp/assets/js/main.js
git commit -m "Add non-blocking hero logo reveal animation"
```

---

## Task 6: Waitlist form + Brevo wiring

**Files:**
- Modify: `projects/ironstandard-lp/index.html` (waitlist section)
- Modify: `projects/ironstandard-lp/assets/js/main.js` (submit handler + inline success/error state)
- Modify: `projects/ironstandard-lp/assets/css/style.css` (form styles)

**Interfaces:**
- Produces: a `data-brevo-form` marker attribute and `IRONSTANDARD_BREVO_URL` constant that `README.md` (Task 8) tells Anthony/Hunter how to fill in with the real Brevo list endpoint.

- [ ] **Step 1: Add the form markup**

```html
<section id="waitlist" class="section waitlist">
  <p class="kicker">Join the waitlist</p>
  <h2>Be a founding member.</h2>
  <form id="waitlist-form" data-brevo-form novalidate>
    <label for="wl-name">Name</label>
    <input type="text" id="wl-name" name="name" required autocomplete="name">
    <label for="wl-email">Email</label>
    <input type="email" id="wl-email" name="email" required autocomplete="email">
    <button type="submit" class="btn-primary">Join the waitlist</button>
    <p id="waitlist-status" role="status" aria-live="polite"></p>
  </form>
</section>
```

- [ ] **Step 2: Add the submit handler (Brevo endpoint left as a named constant for Task 8's README to explain)**

```javascript
// --- Waitlist form -> Brevo ---
// Replace IRONSTANDARD_BREVO_URL with the real Brevo "Create contact" REST
// endpoint + list ID once the Brevo account exists (see README.md).
const IRONSTANDARD_BREVO_URL = 'REPLACE_WITH_BREVO_ENDPOINT';

const waitlistForm = document.getElementById('waitlist-form');
if (waitlistForm) {
  waitlistForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const status = document.getElementById('waitlist-status');
    const name = document.getElementById('wl-name').value.trim();
    const email = document.getElementById('wl-email').value.trim();

    if (!name || !email) {
      status.textContent = 'Please fill in both fields.';
      return;
    }

    status.textContent = 'Submitting...';
    try {
      const res = await fetch(IRONSTANDARD_BREVO_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, attributes: { FIRSTNAME: name } })
      });
      if (!res.ok) throw new Error('Request failed');
      status.textContent = "You're on the list. We'll be in touch.";
      waitlistForm.reset();
    } catch (err) {
      status.textContent = 'Something went wrong — please try again.';
    }
  });
}
```

- [ ] **Step 3: Style the form**

```css
.waitlist form { display: flex; flex-direction: column; gap: 1rem; max-width: 420px; margin-top: 2rem; }
.waitlist label { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--fg-dim); }
.waitlist input {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.25);
  color: var(--fg);
  padding: 0.75rem;
  font-family: var(--font-display);
  font-size: 1rem;
}
.waitlist input:focus { outline: none; border-color: var(--accent); }
#waitlist-status { color: var(--accent); min-height: 1.2em; font-size: 0.9rem; }
```

- [ ] **Step 4: Verify in browser**

Use `form_input` to fill name/email, click submit, and confirm (via `read_page`) that `#waitlist-status` updates. Since `IRONSTANDARD_BREVO_URL` is still a placeholder, expect the catch-branch message ("Something went wrong...") — that's correct behaviour until Task 8's real endpoint is wired in by Anthony/Hunter; the point of this check is that the JS runs and the status element updates, not that the network call succeeds.

- [ ] **Step 5: Commit**

```bash
git add projects/ironstandard-lp/index.html projects/ironstandard-lp/assets/js/main.js projects/ironstandard-lp/assets/css/style.css
git commit -m "Add waitlist form with Brevo submit handler"
```

---

## Task 7: Footer, meta/SEO tags, accessibility pass

**Files:**
- Modify: `projects/ironstandard-lp/index.html`
- Modify: `projects/ironstandard-lp/assets/css/style.css`

- [ ] **Step 1: Fill in the footer**

```html
<footer id="footer" class="site-footer">
  <img src="assets/img/logo-white.png" alt="Iron Standard" class="footer-logo">
  <p>Oslo, Norway</p>
  <p><a href="mailto:anthonygmccoy@gmail.com" class="accent-link">anthonygmccoy@gmail.com</a></p>
  <p class="footer-copyright">&copy; 2026 Iron Standard. All rights reserved.</p>
</footer>
```

- [ ] **Step 2: Add Open Graph / social preview meta tags to `<head>`**

```html
<meta property="og:title" content="Iron Standard — Oslo">
<meta property="og:description" content="A different standard for serious training. Founding-member waitlist now open.">
<meta property="og:image" content="assets/img/hero-poster.jpg">
<meta property="og:type" content="website">
```

- [ ] **Step 3: Style the footer**

```css
.site-footer {
  text-align: center;
  padding: 3rem 1.5rem;
  color: var(--fg-dim);
  border-top: 1px solid rgba(255,255,255,0.1);
}
.footer-logo { width: 140px; margin-bottom: 1rem; opacity: 0.8; }
.footer-copyright { margin-top: 1rem; font-size: 0.8rem; }
```

- [ ] **Step 4: Accessibility check**

Run through the page with `read_page` and confirm: every `<img>` has non-empty `alt` text, form inputs have associated `<label>` elements (already true from Task 6), heading order is h1 → h2 → h3 with no skipped levels, and the accent orange on black (`#F4502A` on `#0a0a0a`) passes as a large-text/UI-element contrast use (not used for body-sized text, only kickers/buttons/links per the Global Constraints — verify no body-copy text uses `var(--accent)` directly).

- [ ] **Step 5: Verify in browser**

Screenshot full-page scroll (hero through footer) at desktop width. Expected: consistent dark/premium look end to end, footer renders correctly, no console errors.

- [ ] **Step 6: Commit**

```bash
git add projects/ironstandard-lp/index.html projects/ironstandard-lp/assets/css/style.css
git commit -m "Add footer, SEO meta tags, and accessibility pass to Iron Standard landing page"
```

---

## Task 8: Handoff README (Brevo + Netlify + DNS + GoDaddy export steps)

**Files:**
- Create: `projects/ironstandard-lp/README.md`
- Create: `wiki/clients/anthony.md` — check whether this file (from `wiki/clients/anthony.md` seen in Task listing) already documents Iron Standard; if not, add an Iron Standard entry per the wiki's client-page convention.
- Modify: `wiki/index.md` — add an entry for the new project page.
- Modify: `wiki/log.md` — append the ingest/build log line.

**Interfaces:**
- Consumes: the `IRONSTANDARD_BREVO_URL` constant name from Task 6 (README must reference it by that exact name).

- [ ] **Step 1: Write the README**

```markdown
# Iron Standard — Waitlist Landing Page

Static page, no build step. Open `index.html` directly or serve the folder with any static host.

## 1. Set up Brevo (email storage — this is what you show investors)

1. Create a free account at brevo.com (no cost, no card required for the free tier).
2. Create a Contact List called "Iron Standard Waitlist".
3. Go to Contacts > Forms (or use the Transactional/API route) and grab either:
   - A hosted form embed code, **or**
   - Your API key + list ID, for the fetch-based version already wired into `assets/js/main.js`.
4. In `assets/js/main.js`, find the line `const IRONSTANDARD_BREVO_URL = 'REPLACE_WITH_BREVO_ENDPOINT';` and replace it with your real Brevo contacts endpoint (Brevo's dashboard gives you the exact URL + auth header format under Automation > API).
5. Anytime you want to show investors the list: Brevo dashboard > Contacts > Export as CSV.

## 2. Export existing leads from the current GoDaddy site first

Before retiring `ironstandard.no`'s current "Launching Soon" page, log into GoDaddy Website Builder and check the form responses / contact list it's been collecting — export anything there and import it into the new Brevo list so no early signups are lost.

## 3. Deploy to Netlify

1. Create a free account at netlify.com.
2. Drag-and-drop the `ironstandard-lp` folder onto Netlify's deploy area (or connect it to a git repo for auto-deploys).
3. Netlify gives you a temporary `*.netlify.app` URL immediately — check the site there first.

## 4. Point ironstandard.no at Netlify

1. In Netlify: Site settings > Domain management > Add custom domain > enter `ironstandard.no`.
2. Netlify shows you the DNS records to set (usually an A record + CNAME for `www`).
3. Log into GoDaddy > My Products > DNS (for ironstandard.no) and add those records. GoDaddy stays your domain registrar — you're only changing where the domain *points*, not who you bought it from.
4. DNS changes can take a few hours to propagate.

## 5. What's still needed

- Real opening date (currently placeholder "Opening 2027" text in the hero).
- Actual analytics if wanted (Plausible or GA4 — not wired in yet).
```

- [ ] **Step 2: Check and update `wiki/clients/anthony.md`**

Read the existing file first (it may already reference Anthony/Iron Standard from an earlier engagement). Add or update a section covering: business description, this landing-page build, Brevo/Netlify/GoDaddy setup decisions, and a link to `projects/ironstandard-lp/` and this spec/plan pair — following this vault's existing client-page frontmatter convention (`type: client`, `tags`, `updated: 2026-09-02`).

- [ ] **Step 3: Update `wiki/index.md`**

Add a one-line entry under the appropriate category (Projects or Clients) linking to the updated `anthony.md` and describing the Iron Standard landing page build.

- [ ] **Step 4: Append to `wiki/log.md`**

```markdown
## [2026-09-02] build | Iron Standard waitlist landing page
Static landing page built for Iron Standard (Anthony McCoy), Oslo gym pre-launch. Brevo for email capture (investor-exportable), Netlify hosting, GoDaddy DNS repoint. Spec: docs/superpowers/specs/2026-09-02-ironstandard-landing-page-design.md. Plan: docs/superpowers/plans/2026-09-02-ironstandard-landing-page.md.
```

- [ ] **Step 5: Commit**

```bash
git add projects/ironstandard-lp/README.md wiki/clients/anthony.md wiki/index.md wiki/log.md
git commit -m "Add Iron Standard landing page handoff README and wiki entries"
```

---

## Task 9: Final cross-device QA

**Files:** none (verification only)

- [ ] **Step 1: Full-page desktop screenshot**

Open the page in the Browser pane at desktop width, screenshot top to bottom in sections (hero, what-it-is, who-its-for, whats-different, founding-member, waitlist, footer).

- [ ] **Step 2: Mobile screenshot pass**

`resize_window` to `preset: "mobile"`, reload, screenshot the same sections. Expected: no horizontal scroll, pillars stacked, hero text legible over video, form usable with on-screen keyboard sizing (inputs at least 44px tall).

- [ ] **Step 3: Console/network check**

`read_console_messages` with `onlyErrors: true` — expected: empty. `read_network_requests` — confirm the Google Fonts request and video/image assets all return 200.

- [ ] **Step 4: Send the result to the user**

Use `SendUserFile` with the desktop and mobile screenshots, or point them at the Netlify preview URL once Task 8's deploy steps have been run.

- [ ] **Step 5: Reset viewport**

`resize_window` back to `preset: "desktop"` to leave the tab in its default state.
