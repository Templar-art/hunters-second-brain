---
type: project
tags: [web, component, ndis, deliverable, elementor]
status: built
updated: 2026-07-23
---

# Open Arms Australia — Site Header

Redesigned, production-ready website header for **[[open-arms-australia|Open Arms Australia]]** (NDIS support provider, open.arms.10xvisuals.co, WordPress + Elementor). Brief: make a template-y marketing navbar feel like a premium, calm, editorial-restraint healthcare header — inside the existing locked brand system.

- **Lives at:** [projects/open-arms-header/](../../projects/open-arms-header/HANDOFF.md) — one self-contained file, `open-arms-header.html` (markup + CSS + JS). Paste into an Elementor **HTML** widget; no build step. Double-click to preview.
- **Handoff:** [HANDOFF.md](../../projects/open-arms-header/HANDOFF.md) — dev install steps + the two things to check (Poppins double-load, active-page `aria-current`). This is the file to give the developer.
- **Brand (locked):** Poppins only; Dark Green `#368063`, Light Green `#6BA489`, Pastel Purple `#8080B8` (tiny accents only), Charcoal `#161616`, Green Tint `#EAF2EE`. All colours are CSS vars at the top of the `<style>` block.

## Design decisions (why it reads premium, not template)

- **Solid white nav + hairline border**, not glassmorphism/backdrop-blur (the #1 "template" tell the brief called out).
- **Soft green-tint utility bar** (trust strip: NDIS + coverage areas), not a black corporate slab. Green anchors the top, white nav breathes.
- **Nav links = green-tint pill on hover/active** (healthcare-portal calm), not the growing SaaS underline. Active page via `aria-current="page"`.
- **CTA**: pill + soft shadow + nudging arrow (premium-friendly), not a loud green glow. Single clear primary action — the "Enquire today" button is the only loud element in the nav.
- **Purple = a single 7px NDIS dot.** Restraint is the point.

## Built through the impeccable pipeline (redesign → single-number fix → optimize → polish → bug-fix)

- **One phone number, top bar, at every width** — never appears twice. (Started as a desktop-nav/mobile-topbar swap; simplified to top-bar-only after the layout fix below removed the nav phone.)
- **Perf**: single right-sized logo `-768x189` (~14 KB vs the 54 KB `-scaled` 2560px original), render-blocking `@import` replaced with `preconnect` + `<link>`, unused font weight 700 dropped, box reserved via CSS `aspect-ratio` → ~0 CLS.
- **Polish** (verified in-browser): fixed a `:focus-visible` `border-radius` override that snapped the CTA pill to 12px corners on keyboard focus; mobile menu now `overflow-y:auto` + `calc(100vh-130px)` so it scrolls instead of clipping on short/landscape screens; hamburger is a guaranteed 44×44 tap target.
- **Logo-squash bug (Hunter caught it)**: on desktop the nav content (logo + 6 links incl. "For Support Workers" + phone + CTA ≈ 1287px) overflowed the 1240 wrap, so flexbox shrank the **logo** (the only shrinkable item, via `img{max-width:100%}`) → squished to ~84×48. Fixed three ways: `flex-shrink:0` on the logo (hard backstop), pulled the phone out of the nav into the top bar (removed ~130px of the overflow), and raised the hamburger breakpoint 980→**1240px** so the full horizontal nav only shows when it genuinely fits. Verified in real Chrome (logo 195×48, ratio 4.06, no overflow, ~74px margin at the breakpoint).
- **A11y**: focus rings, Esc-to-close, close-on-resize, WCAG-AA contrast, `prefers-reduced-motion`.

## Reuse

The `.oa-x`-namespaced, token-driven, single-file, Elementor-HTML-widget pattern is a clean **reusable header shell for any 10x WordPress/Elementor client** — swap the `--oa-*` colour vars, font, logo `srcset`, and menu `<li>`s; the structure, sticky/scroll behaviour, mobile menu, and a11y carry over. Sits alongside the [[bespoke-estate-agents|Bespoke]] site work as 10x's WordPress-client web surface.

**Note:** kept the two `layout-transition` design-hook findings (sticky-bar shrink `min-height`, mobile accordion `max-height`) — both single-element, low-frequency, `prefers-reduced-motion`-guarded, and the canonical technique for each job. Intentional, not defects.
