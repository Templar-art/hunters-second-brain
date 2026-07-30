# 10x Visuals Homepage — Prestige Rebuild (Design)

*2026-07-30 · Source of truth for the homepage rebuild. Scope is the homepage only. Other pages inherit this as reference once it is approved.*

## 1. Problem

`10xvisuals.com.au` is a WordPress site with real content and real case studies, but the finish does not match the work 10x sells. Structure is broadly sound; the skin, typography, rhythm and motion are not. Separately, the hero headline is a generic agency claim that says nothing about property, the founders' pull-quote contains a censored swear word that cannot share a page with a quiet-luxury finish, and the homepage offers no enquiry path of its own.

**⚠️ Supersedes** the vault claim that there is no lead form on the site ([lead-gen-engine.md](../../../wiki/projects/lead-gen-engine.md), verified 27 Jul 2026). A form does exist at `/contact-us/`: name, phone, email, company, service dropdown, required free-text message, spam check. Seven fields with a required free-text field is the same friction we told MVX to remove ([FORM-FIX.md](../../../projects/mvx-lead-fix/FORM-FIX.md)). The vault page is corrected as part of this work.

## 2. Approved decisions

| Decision | Value |
|---|---|
| Design standard | 10x Prestige Design System v1.0 (`10x-prestige-design-system.html`) |
| Delivery | Static rebuild. One self-contained `index.html`, iterated in-browser, then shipped or handed to the WP team |
| Scope | Homepage only |
| Hero photograph | SOL drone, golden hour (`DJI_20250917170029_0253_D-HDR`) |
| Hero headline | "Presentation decides the price." |
| Founders quote | Rewritten restrained, no swearing |
| Enquiry | Three-field inline form in the closing section |

Non-negotiables inherited from the design system: Prata for display, Montserrat 300–600 for everything else; paper `#f6f3ec` and night `#111519` surfaces, never pure white or black; blue (`#34789d` / `#61a8d8`) as accent only, never a filled area; one easing curve `cubic-bezier(.16,1,.3,1)`; no bounce or elastic; no em dashes in copy; Australian English; motion is progressive enhancement, never a gate on content visibility.

## 3. Architecture

One file, `projects/10x-site/index.html`, self-contained: inline CSS, inline JS, assets referenced from a sibling `assets/` directory so the page works over `file://` as well as HTTP. Fonts load from Google Fonts with a system-serif and system-sans fallback stack so the page degrades legibly offline.

Assets are pulled down from the live WordPress uploads once, into `projects/10x-site/assets/`, and downscaled: hero at 2400px wide, plates at 1600px, logos at 400px, all re-encoded as progressive JPEG (logos as PNG where transparency matters). Nothing hotlinks to `wp-content` at runtime.

Three JS behaviours only, all in one `requestAnimationFrame`-throttled scroll handler plus one `IntersectionObserver`:

1. Nav gains a paper background past 60px of scroll.
2. A 2px gradient hairline scales across the top as the page advances.
3. The interlude image translates on scroll, transform only, roughly 12% of travel.

The observer removes a `pending` class to trigger fade-ups. Elements only get `pending` if they start below the fold, so above-the-fold content is never hidden. Under `prefers-reduced-motion: reduce` no element is ever marked pending and the parallax is skipped, so the full page renders static.

## 4. Section-by-section

### 0. Nav and scroll progress
Fixed, transparent over the hero, ivory wordmark at 15px with `.34em` tracking. Links at 10px, `.3em`, uppercase, `--ivory-soft`, hovering to `--blue-light`. Past 60px the bar takes `rgba(246,243,236,.94)` with a 10px backdrop blur and a hairline bottom border; wordmark and links flip to ink. Links: Branding, Content, Lead Gen, AI Systems, Contact. Below 900px the link row is replaced by a single Contact link (no hamburger drawer in this scope).

Destinations: `/branding`, `/content-creation`, `/lead-generation`, `/systems-processes`, `/contact-us`.

### 1. Hero
Full-bleed SOL drone photograph, `min-height:100vh`, bottom-aligned content. Veil gradient from `rgba(17,21,25,.62)` at the top through `.28` at 42% to `.86` at the bottom, so the skyline stays readable while the water beneath the type goes dark. Photo drifts `scale(1.1)` to `scale(1)` over 22s on load, once, ease-out.

Content stack, bottom left: 56px blue hairline → label `PRESTIGE PROPERTY & CONSTRUCTION MEDIA · GOLD COAST` → H1 in Prata, `clamp(38px,6.4vw,84px)`, line-height 1.08, `max-width:16ch`:

> Presentation decides the price.

Then a hairline-topped meta row, space-between: a 46ch lede on the left, one tracked text CTA on the right ("Start a project", linking to the closing form anchor). No filled button anywhere in the hero.

Hero lede:

> Photography, film, brand and campaigns for the people building and selling the best property on the Gold Coast.

H1 reveals line by line through a clip mask, staggered 180ms.

### 2. Proof
`--paper-deep` surface. Client logos, but not as a colour tile grid: each rendered monochrome at `--ink-soft` weight, two hairline-divided rows, static, generous gutters. A single tracked label above: `TRUSTED BY`. No counts, no "15+" claim (brand rule: no volume numbers).

**The strip only carries clients whose logo file exists in the live uploads.** Confirmed present: Kollosche, Ray White, PRD, The Agency, Gold Coast BMW, Ashley Cooper Construction, Shape Construction, Salisbury Building Projects, Skye Developments, Mastr. The current homepage also names Maker Build, Broncos Leagues Club, CSi Club Southport, Hill Interior Linings, Ocean Shores and Hour Glass as text, with no logo asset behind them; those are dropped from the strip rather than typeset as words, since mixed logos and wordmarks read cheap. If 10x supplies the missing files they slot straight in.

**Naming note:** the asset is `Sky-Developments-Logo.png` while the homepage copy reads "Skye Developments". The copy spelling is used in the case-study client line; the file is used as-is. Confirm which is correct with 10x before the page ships.

### 3. Positioning
Paper. Ghost numeral `I` at 5% opacity top-right, kicker `I. / THE STUDIO`, Prata H2, two ledes.

The page runs four numbered chapters, `I` Studio, `II` The Work, `III` Disciplines, `IV` Founders. Hero, proof, interlude, testimonial, close and footer are unnumbered.

> **Four disciplines, one standard.**
>
> 10x Visuals is a Gold Coast studio built on a single idea: the way a property or a build is presented decides what people are willing to pay for it. We photograph the homes, film the projects, and brand the businesses behind them.
>
> Brand, content, lead generation and the AI systems that let a small team work at volume. One team across all four, so the standard holds from the first frame to the last ad.

### 4. The work
Paper. Ghost numeral `II`, kicker `II. / THE WORK`. The section that carries the page. Five case studies, alternating full-bleed and half-width plates, each opening from a `clip-path` inset with a slight scale settle on enter.

Each entry: image plate → plate caption row (discipline label left, two-digit numeral right) → Prata title at 26–34px → client line as a tracked label → one-line description → "View Project" as a tracked label with a hairline that extends on hover.

| # | Title | Client | Line | Link |
|---|---|---|---|---|
| 01 | SOL | Skye Developments | A canal side compound, filmed and photographed for the architecture, the water and the finish. | `/sol` |
| 02 | Davenport | PRD Burleigh | A refined hillside residence, captured for its atmosphere rather than its floor area. | `/davenport` |
| 03 | Bespoke Estate Agents | Gold Coast | Brand and web for a boutique prestige agency with two decades behind it. | `/bespoke` |
| 04 | Elysium | Shape Construction | A large scale apartment build, documented for scale and quality once complete. | `/elysium` |
| 05 | Broncos Leagues Club | Ashley Cooper Construction | A major refurbishment recorded from before to completion for the builder's portfolio. | `/broncos-leagues-club` |

### 5. Interlude
Full-bleed night plate with transform parallax at 12% of travel, veil over it, one centred Prata pull-quote at `clamp(24px,3.4vw,42px)` above a tracked label `THE PRINCIPLE`.

> The best marketing doesn't look like marketing. It looks like the work, presented properly.

### 6. Disciplines
Night surface. Ghost `III`, kicker `III. / THE DISCIPLINES`, Prata H2 in ivory, then four hairline-ruled rows. Each row: Prata roman numeral in `--blue-light`, discipline name, one-line description, and a tracked "View" label at the right. Whole row is the link.

> **What we actually do.**

| Numeral | Discipline | Line | Link |
|---|---|---|---|
| I. | Branding | Strategy, identity, and the guidelines that keep it intact. | `/branding` |
| II. | Content | Photography and film for property, construction, and the brands behind them. | `/content-creation` |
| III. | Lead Gen | Campaigns and landing pages built to produce enquiries, not impressions. | `/lead-generation` |
| IV. | AI Systems | Generation and automation that let a small team ship at volume. | `/systems-processes` |

### 7. Founders
Paper. Two columns on desktop, stacked on mobile: the existing headshot (`10x-Headshots-Final-1-of-1`) as a plate on one side, and on the other a ghost `IV`, a kicker `IV. / THE FOUNDERS`, a Prata pull-quote, and the names.

> We started 10x because good work kept being let down by the way it was presented. Fixing that is the whole job.

Attribution line: `TYSON · HUNTER · DAMON`. No founder-always-on-site claim (brand rule).

### 8. Testimonial
Night. One testimonial only, Prata at `clamp(20px,2.6vw,30px)`, ivory, `max-width:34ch` per line rhythm, with a 56px blue hairline above.

> Working with the 10x Visuals team completely changed how our brand shows up online. Their approach was structured, creative, and professional from start to finish. The final content and campaigns elevated our brand and delivered results beyond anything we had experienced previously.

Attribution: `MURPHY S · DIRECTOR & FOUNDER`. The existing YouTube embed is dropped from the homepage: a video player chrome in the middle of the page breaks the finish, and the testimonial reads stronger as type.

### 9. Close and enquiry
Full-bleed night plate, heavy veil, centred content, `id="start"` (the hero CTA target).

> **It's time to raise the standard.**
>
> Tell us what you're building. We will tell you what it needs.

Then the form: three fields only, name, email, phone. Hairline-underlined inputs on the night surface, no boxes, labels as tracked 10px caps, ivory text, focus ring `--ivory`. Submit is a tracked label with a hairline, not a filled button. All three required, validated inline with one **token added to the design system by this build**, `--clay:#8a5a4a`, a desaturated clay that stays in palette and is used for validation only. It is the only new token; everything else comes from DS v1.0 unchanged. No service dropdown, no message field, no company field.

**Submission:** the form posts JSON via `fetch` to a single `FORM_ENDPOINT` constant declared at the top of the script block. Until 10x supplies a real endpoint, `FORM_ENDPOINT` is `null` and the handler falls back to opening a `mailto:hello@10xvisuals.com.au` compose window with a fixed subject and the three values in the body, then shows the success state. The fallback is a `mailto:` compose only, never a URL query string, so personal details never land in a link. Swapping in the endpoint is a one-line change at deploy.

Success state replaces the form in place with a Prata line, "Thank you. We will be in touch within one business day." Failure shows the phone number and email as a fallback path, never a bare error.

### 10. Footer
Night. Prata wordmark `10X VISUALS`, hairline, then one row: copyright, Privacy Policy link, and the three contact points (email, phone, Instagram) as tracked labels. Nothing else.

## 5. Responsive

Three behaviours, no separate mobile design:

- Type scales through `clamp()` at every level, so no breakpoint-specific font sizes exist.
- Below 900px: nav links collapse to a single Contact link; the founders and hero-meta two-column rows stack; discipline rows keep the numeral inline and drop the right-hand "View" label (the row stays the link).
- Below 640px: full-bleed plates go edge to edge with no side padding; the logo proof grid goes from two rows to a three-per-row wrap; section padding drops to the bottom of the `clamp(80px,12vh,150px)` range.

Hero holds `100vh` with `100dvh` where supported so mobile browser chrome does not crop the headline.

## 6. Accessibility

Every image carries real alt text naming the property and the discipline. The nav, plate links and discipline rows are real anchors, focusable in order, with a visible focus ring: `--ivory` on night surfaces, `--blue` on paper. Form inputs have real `<label>` elements, not placeholder-only labelling. Colour contrast: `--ink` on `--paper` and `--ivory` on `--night` both clear AA at body size; `--ink-faint` and `--ivory-faint` are used for meta text at 14px and above only, never for anything a user has to read to act. Under `prefers-reduced-motion` the page is fully static and fully readable.

## 7. Verification

Before the page is called done:

- Rendered in the browser pane at desktop, tablet and mobile widths, screenshots captured at each.
- Console clean, no failed asset requests.
- Loaded over `file://` as well as HTTP, to confirm the self-contained claim.
- `prefers-reduced-motion` emulated: every section visible, no motion, no layout shift.
- Tab through the whole page: focus visible at every stop, order matches reading order.
- Form submitted with the `mailto:` fallback active, and with a stub endpoint, to confirm both paths and the success state.
- Every internal link resolved against the live site so no path 404s.

## 8. Out of scope

The other five pages, the WordPress port itself, DNS or hosting cutover, a mobile nav drawer, the case-study detail pages, any change to `/contact-us/` and its form, analytics or conversion tracking, and the AI-generated scroll-world hero from [10x-prestige-world](../../../projects/10x-prestige-world). None of these are architected out; the homepage is built so each can follow.

## 9. Follow-on work this exposes

Recorded here so it is not lost, not built now:

- `/contact-us/` still carries a seven-field form with a required free-text message. Same friction we bill clients to remove.
- The vault's lead-gen page needs the correction in §1 applied.
- The other five pages have no prestige-standard treatment and will visibly clash with the new homepage until they get one.

---

## 10. Build outcome, 30 Jul 2026

Built at [projects/10x-site/index.html](../../../projects/10x-site/index.html). Five decisions in this spec were overturned during the build. Each is recorded here because the spec above no longer describes the shipped page.

**1. No numbered eyebrows, no ghost numerals.** §4 specified a tracked kicker plus an oversized Prata roman numeral per section, per Prestige DS v1.0. Removed. [DESIGN.md](../../../DESIGN.md) already carries The No-Eyebrow Rule and The No-Numbers Rule, which forbid exactly this on any web surface after two pages were stripped for it in July 2026. Independently: at chapters I to IV the Prata glyphs render as plain vertical bars that read as a stray watermark, and numbered-eyebrow-plus-display-serif is the most saturated AI landing-page pattern of 2026, so it worked against the premium read. Section cadence is now a 56px blue hairline above each heading. The `01` to `05` work index went too, on the same rule: nothing requires reading the projects in order.

**2. Client logos became a typeset roster.** §4.2 specified a monochrome logo strip. The nine available logo files are a mix of dark-on-white JPEGs, an inverse navy lockup and a yellow Ray White square; greyscaled and multiplied they render as pale boxes of unequal weight in a ragged grid, which is the identical-card-grid anti-pattern built from mismatched assets. Replaced with all sixteen client names typeset in Prata on a hairline grid, which also carries the ten clients that have no logo asset. Logos return only if a matched monochrome set on transparent grounds is supplied. The logo files were deleted; restore with the download loop in the project README if needed.

**3. Four design tokens amended for WCAG AA.** DS v1.0 shipped four values that fail against the surfaces they land on: `--ink-faint` 2.64:1, `--ivory-faint` 3.27:1, `--blue` as text 4.39:1, and no validation colour at all. Amended to `.62`, `.55`, `#2e6a8a` and a new `--clay:#bd8270`; `#34789d` survives as `--blue-rule` for hairlines, where nothing must be read. Full table in DESIGN.md under The AA-Amendment Rule.

**4. Reveal bootstrap rewritten.** The first implementation gated content visibility on the IntersectionObserver, so a deep link to `#close`, which the hero CTA itself points at, could land on a blank section. Reveals now arm only when the observer exists, arm after the browser settles any anchor scroll, and a 2.5s failsafe clears every pending element regardless.

**5. Founders section moved to night and monochrome.** The available frame is a wide studio-seamless team shot in black tees, which reads as a team snap rather than a portrait. Now on the night surface, greyscaled and cropped tight. **This is a holding treatment.** The section wants a real environmental portrait; that needs a shoot, not CSS.

### Verification performed

Measured in a real browser at 1440, 768 and 375, plus headless Chrome for the hero.

| Check | Result |
|---|---|
| Text contrast, 11 pairs, alpha-composited on live DOM | 4.68:1 to 6.69:1, **0 failures** |
| Touch targets under 44px | **0** (was 11) |
| Horizontal overflow at 1440 / 768 / 375 | none |
| Page weight | **3.81MB total, 634KB above the fold** (was 6.09MB, all eager) |
| Images lazy-loaded | 8 of 9, hero eager with `fetchpriority=high` |
| Console errors | none |
| Anti-pattern detector | clean, 0 findings (was 17) |
| Form: invalid submit | all three fields flagged, errors shown, focus moves to first bad field |
| Form: success state | fields swap for the thank-you line |
| Deep link `/#close` | scrolls correctly, 0 pending, all reveals at opacity 1 |
| Semantics | `<main>` present, 5 project titles are `h3`, every image has real alt text |

### Still open, needs Hunter

- **Form endpoint.** `FORM_ENDPOINT` is `null`, so submit opens a `mailto:` compose to hello@10xvisuals.com.au. One-line change at deploy.
- **Founders portrait.** Holding treatment per above.
- **Plate grading.** SOL is a night aerial, Davenport and Bespoke are bright daylight. A uniform `saturate(.94) contrast(1.03)` unifies them slightly, but a true one-grade pass needs graded exports, which is a Lightroom job not a CSS one.
- **Skye Development Group** confirmed as the correct spelling, from the logo artwork itself. The site copy said "Skye", the asset filename said "Sky".
- **`/contact-us/`** still carries the seven-field form with a required free-text message.

---
_Vault: [[overview]] · [[brand-system]] · [[lead-gen-engine]] · [[10x-website]]_
