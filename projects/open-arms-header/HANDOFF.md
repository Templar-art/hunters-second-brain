# Open Arms Australia — Header (developer handoff)

Redesigned, production-ready site header for **open.arms.10xvisuals.co**. Drop-in for an Elementor **HTML** widget. One file, fully self-contained (markup + CSS + JS), no build step, no dependencies.

**Deliverable:** [`open-arms-header.html`](open-arms-header.html)

---

## Install (2 minutes)

1. In Elementor, add (or edit) a section at the very top of the **Header** template.
2. Drop in an **HTML** widget.
3. Open `open-arms-header.html`, copy the **entire** file, paste it into the widget.
4. Set the section to **full width**, no padding/margin, so the sticky bar spans edge to edge.
5. Save / publish. Done — it renders instantly.

> Preview before pasting: just double-click `open-arms-header.html` to open it in any browser.

---

## Two things to check

1. **Poppins font (top 3 `<link>` lines).** The header loads Poppins itself. If the WordPress theme or Elementor Global Fonts **already** loads Poppins, delete those 3 lines to avoid loading it twice (Elementor → Site Settings → Global Fonts). If unsure, leave them — it still works.

2. **Active page highlight.** The current page gets a soft green pill via `aria-current="page"`. It's hard-coded on **Home** in this file. Two options:
   - Move `aria-current="page"` onto whichever `<a>` matches the current page, per template, **or**
   - If you wire this to a real WordPress menu, target WP's `.current-menu-item` class instead of `[aria-current="page"]` in the CSS.

Everything else is turnkey.

---

## What it does

- **Sticky** top-bar + nav; nav compacts and drops a soft shadow on scroll.
- **Responsive**: full horizontal nav at ≥1240px; below that a hamburger menu; small-phone tweaks at 560px.
- **Mobile menu**: accessible disclosure — `aria-expanded`, Esc to close, closes on resize to desktop, scrolls if it can't fit the viewport.
- **Phone number appears once** — it lives in the top bar at every width.
- **Accessibility**: keyboard focus rings, 44×44 tap targets, WCAG-AA contrast, `prefers-reduced-motion` honoured.
- **Performance**: right-sized logo via `srcset` (~5–14 KB vs the 54 KB `-scaled` original), no render-blocking `@import`, zero layout shift.

## Brand (locked — do not alter)

Poppins only. Dark Green `#368063` (primary), Light Green `#6BA489`, Pastel Purple `#8080B8` (tiny accents only). Charcoal `#161616`, Green Tint `#EAF2EE`. All colours are CSS variables at the top of the `<style>` block if anything ever needs tuning.

## Editing later

- **Menu items / links** — edit the one `<ul class="oa-nav-links">` list; the mobile menu reuses it.
- **Phone number** — one place only: the top-bar link (`.oa-topbar-phone`, `href="tel:…"`). Update the number in both the visible text and the `tel:` href.
- **CTA** — the "Enquire today" button → `/contact`.
- All class names are namespaced `.oa-x` / `.oa-*` so nothing leaks into the rest of the theme.
