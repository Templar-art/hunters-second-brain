---
name: 10x Visuals
description: Cinematic film-house identity across two surface classes — own-brand social graphics and client conversion pages.
colors:
  brand-blue: "#61a8d8"
  brand-blue-deep: "#3d87ba"
  brand-blue-ink: "#2b6b96"
  kicker-blue: "#8ec6e8"
  brand-navy: "#102f41"
  shadow-ink: "#050c14"
  page-ink: "#12181c"
  page-charcoal: "#1c2529"
  page-body: "#39454b"
  page-muted: "#67737a"
  page-off-white: "#f5f7f9"
  page-line: "#e3e8eb"
  white: "#ffffff"
  prestige-paper: "#f6f3ec"
  prestige-paper-deep: "#efeadf"
  prestige-ink: "#14181b"
  prestige-night: "#111519"
  prestige-ivory: "#f3efe6"
  prestige-blue: "#2e6a8a"
  prestige-blue-rule: "#34789d"
  prestige-blue-light: "#61a8d8"
  prestige-clay: "#bd8270"
  prestige-nav-veil: "rgba(246,243,236,.94)"
typography:
  prestige-display:
    fontFamily: "Prata, 'Times New Roman', serif"
    fontSize: "clamp(40px, 6.6vw, 88px)"
    fontWeight: 400
    lineHeight: 1.06
    letterSpacing: "0.01em"
  prestige-heading:
    fontFamily: "Prata, 'Times New Roman', serif"
    fontSize: "clamp(31px, 4.6vw, 56px)"
    fontWeight: 400
    lineHeight: 1.12
  prestige-body:
    fontFamily: "Montserrat, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "17px"
    fontWeight: 300
    lineHeight: 1.75
  display:
    fontFamily: "Montserrat, -apple-system, sans-serif"
    fontSize: "clamp(2.3rem, 1.6rem + 3.4vw, 4rem)"
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Montserrat, -apple-system, sans-serif"
    fontSize: "clamp(1.75rem, 1.4rem + 1.8vw, 2.6rem)"
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Montserrat, -apple-system, sans-serif"
    fontSize: "1.15rem"
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: "Poppins, -apple-system, sans-serif"
    fontSize: "16.5px"
    fontWeight: 300
    lineHeight: 1.72
  label:
    fontFamily: "Poppins, -apple-system, sans-serif"
    fontSize: "0.88rem"
    fontWeight: 600
    lineHeight: 1.4
  film-title:
    fontFamily: "Poppins, -apple-system, sans-serif"
    fontWeight: 300
    letterSpacing: "0.09em"
rounded:
  none: "0px"
  sm: "4px"
  md: "6px"
  lg: "10px"
spacing:
  section: "clamp(3.4rem, 7vw, 5.6rem)"
  card: "clamp(1.7rem, 3.5vw, 2.3rem)"
  field: "0.85rem 0.95rem"
  tap: "44px"
components:
  button-primary:
    backgroundColor: "{colors.brand-blue}"
    textColor: "{colors.page-ink}"
    rounded: "{rounded.md}"
    padding: "1.05rem 2rem"
    typography: "{typography.label}"
  button-primary-hover:
    backgroundColor: "{colors.brand-blue-deep}"
    textColor: "{colors.white}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.white}"
    rounded: "{rounded.md}"
    padding: "1.05rem 1.7rem"
  input-field:
    backgroundColor: "{colors.white}"
    textColor: "{colors.page-ink}"
    rounded: "{rounded.md}"
    padding: "{spacing.field}"
  card-surface:
    backgroundColor: "{colors.white}"
    textColor: "{colors.page-body}"
    rounded: "{rounded.lg}"
    padding: "{spacing.card}"
  section-dark:
    backgroundColor: "{colors.page-charcoal}"
    textColor: "{colors.white}"
---

# Design System: 10x Visuals

## Overview

**Creative North Star: "The Film House and the Front Door"**

10x Visuals designs on two surface classes that must never borrow each other's grammar.

The **social layer** is a film house: real footage, quiet tracked type, film-title full stops, and nothing else. Its job is to make a prospect scrolling past a client's credit conclude "these are the expensive ones." Restraint is the proof of premium, verified against The Local Project, AC Media and JUNE: the less graphic design on the grid, the more it reads as work worth paying for. Rendered via PIL from `~/Desktop/General Folder/10x Premium Kit/`, Hunter-approved 7–9 Jul 2026.

The **web layer** is a front door. These are Google and Meta ad landing pages built for clients, and their job is not admiration but a phone call. Restraint is spent differently here: one message-matched headline, an exit ramp to the phone at every scroll depth, and a short form that asks for nothing it doesn't need. Beauty is welcome only where it survives a thumb, a bad signal, and a person who is currently having a cold shower.

The layers share type, blue and voice. They share nothing structurally. A landing page that starts adding decorative kickers is borrowing the social layer's habits without its restraint, and that drift is exactly how AI scaffolding reached two pages in July 2026.

**Key Characteristics:**
- Photography and footage carry the design; type is the quiet layer over it
- One accent blue, spent on actions, never on a surface
- Landing pages are phone-first, nav-free, and end in a short form
- Copy is blokey-Australian, plain, and free of dashes
- Every number on a client page is verified before it ships

## The third surface class: the Prestige layer

Added 30 Jul 2026 with the 10xvisuals.com.au homepage rebuild. Source of truth: `10x-prestige-design-system.html` (Prestige DS v1.0). This is 10x's **own front door**, and it behaves like neither of the first two layers: not a film-house grid card, not a nav-free client ad landing page. It is a long editorial scroll whose job is to make a prospect conclude 10x is the expensive option before they read a word of copy.

**Type.** Prata carries every display moment: headlines, project titles, prices, pull-quotes, the client roster. Montserrat 300 to 600 carries body, labels and detail. This is the one place the identity uses a serif; the pairing is on a genuine contrast axis (display serif against humanist sans) rather than the geometric-against-geometric pairing the other two layers use.

**Colour.** Warm paper `#f6f3ec` and deep night `#111519`, never pure white or black. Roughly 90% of any surface is paper or night; blue appears only as hairlines, numerals, active states and the scroll line. Never a blue fill.

**Motion.** One curve, `cubic-bezier(.16,1,.3,1)`. Hero photo drifts 1.1 to 1.0 over 22s. Reveals rise 32px and are applied only to elements that start below the fold, so nothing above the fold is ever gated on JS.

### Named Rules

**The AA-Amendment Rule.** Prestige DS v1.0 shipped four token values that fail WCAG AA when measured against the surfaces they actually land on. They are amended here, and the amended values are the real system:

| Token | v1.0 | Amended | Measured |
|---|---|---|---|
| `--ink-faint` | `rgba(20,24,27,.42)` | `.62` | 2.64:1 → 4.82:1 on paper |
| `--ivory-faint` | `rgba(243,239,230,.38)` | `.55` | 3.27:1 → 5.51:1 on night |
| `--blue` (as text) | `#34789d` | `#2e6a8a` | 4.39:1 → 5.35:1 on paper |
| `--clay` | absent | `#bd8270` | validation only, 5.76:1 on night |

`#34789d` survives as `--blue-rule` for hairlines and the scroll gradient, where nothing has to be read. This is the Surface-Not-Token Rule applied to a new layer: a token is only compliant on the surface it lands on.

**⚠️ The Eyebrow Contradiction, resolved against the DS.** Prestige DS v1.0 prescribes a tracked uppercase kicker plus an oversized ghost roman numeral on every section. That is precisely what **The No-Eyebrow Rule** and **The No-Numbers Rule** below already forbid on any web surface, after two pages shipped with eyebrows above 9 of 9 and 7 of 7 sections in July 2026 and both were stripped.

The homepage follows the older rules and drops both. Section cadence is a 56px blue hairline above the heading. Two further reasons beyond the existing rule: at chapters I to IV the Prata glyphs render as plain vertical bars, which read as a stray watermark rather than a chapter mark, and the numbered-eyebrow-plus-display-serif combination is the single most saturated AI landing-page pattern of 2026, so it works against the premium read it was meant to create.

No numbered markers survive anywhere on the page. The case-study plates briefly carried a `01` to `05` work index on the argument that a portfolio is an ordered run; it is not one, since nothing requires reading the projects in order, so the numerals came out too. Each plate now carries its discipline label alone on its hairline. The rule holds without exception: a number appears only where the order itself is information the reader needs.

**The Roster-Not-Logos Rule.** The client strip is typeset in Prata, not assembled from logo files. 10x's client logos are a mix of dark-on-white JPEGs, an inverse navy lockup and a yellow Ray White square; greyscaling and multiplying them yields pale boxes of unequal weight in a ragged grid, which is the identical-card-grid anti-pattern made of assets that do not belong together. A typeset roster also carries every client, including the ten with no logo asset at all. Logos return only if a matched monochrome set on transparent backgrounds is supplied.

## Colors

A near-monochrome ink-and-white base with a single cool blue doing all the pointing.

### Primary
- **10x Blue** (`#61a8d8`): the brand accent. On the web layer it fills primary buttons and highlights the one phrase in a headline carrying the offer. On the social layer it is reserved for ads and utility surfaces and never appears on a grid card.
- **Blue Deep** (`#3d87ba`): hover and pressed state beneath the accent. Never a resting surface.
- **Blue Ink** (`#2b6b96`): the accent darkened until it is legible as normal-size text on white and on the off-white tint. Links and small labels use this, never the brand blue itself.

### Secondary
- **Kicker Blue** (`#8ec6e8`): small tracked labels on ad and utility graphics. Not part of the web layer.

### Neutral
- **Brand Navy** (`#102f41`): the dark ground behind the white 10X mark, the dim tint for highlight covers (16% blend, brightness ×0.62), and the hue the legibility scrim is built from. Never a flat tile colour on the grid.
- **Page Ink** (`#12181c`): headers, heroes, and headline type on the web layer.
- **Page Charcoal** (`#1c2529`): the second dark surface, for alternating sections and image-figure grounds.
- **Page Body** (`#39454b`): body copy on white, dark enough that long paragraphs stay comfortable.
- **Page Muted** (`#67737a`): section intros and captions on light surfaces. At the legibility floor deliberately, not for elegance.
- **Page Off-White** (`#f5f7f9`): the alternating section tint. The only background tint in the system.
- **Page Line** (`#e3e8eb`): hairlines, card borders, dividers.
- **Shadow Ink** (`#050c14`): the soft wide drop shadow under white type on footage (blur ~9px @1x, alpha ~150).
- **Scrim**: the "whisper gradient", a black bottom gradient with quadratic falloff. Peak alpha adapts to frame brightness (~165 base, up to 235 on bright interiors).

### Named Rules

**The One Blue Rule.** The accent points at actions and nothing else. It fills buttons, marks the offer phrase, and underlines a live link. It is never a section background, never a large fill, and never two blues on one surface.

**The Surface-Not-Token Rule.** Contrast is checked against the surface a token actually lands on, not the one it was designed for. Muted grey was simultaneously compliant on white and failing on both the tinted section and the dark image figure. When a token changes, re-measure every surface it touches.

**The Not-Ours-To-Set Rule.** Client palettes are not owned here. MVX volt green, CVA monochrome, and every future client's colours live on that client's page and wiki entry; this file owns 10x's blue and the neutral ramp only. Never port one client's palette onto another's page.

## Typography

**Display Font:** Montserrat (with `-apple-system`, sans-serif)
**Body Font:** Poppins (with `-apple-system`, sans-serif)

**Character:** A geometric pair held apart by weight and job rather than by contrast of form. Montserrat appears only at 600–700 and only on headings; Poppins carries everything else, mostly at 300. The gap between a 700 heading and a 300 paragraph *is* the hierarchy, so neither face is asked to be expressive. On the social layer Poppins works alone, in Light and SemiBold.

### Hierarchy
- **Display** (700, `clamp(2.3rem, 1.6rem + 3.4vw, 4rem)`, 1.08, -0.02em): the single page headline, message-matched to the ad that delivered the visitor. One per page.
- **Headline** (700, `clamp(1.75rem, 1.4rem + 1.8vw, 2.6rem)`, 1.08): section headings. These carry the section alone; nothing sits above them.
- **Title** (600, 1.15rem, 1.3): card, step and objection headings.
- **Body** (300, 16.5px, 1.72): all prose, capped at 66ch so a paragraph never runs the full width of a wide container.
- **Label** (600, 0.88rem): form labels and small emphasis. Sentence case, not caps.
- **Film Title** (Poppins Light, all-caps, ~0.09em tracking, auto-shrink to fit width): the social layer only. Ends in a full stop: "THE BOWSPRIT."
- **Social Kicker** (Poppins SemiBold, all-caps, ~19–21px @1x, wide tracking): the social layer's named vocabulary only, listed below.

### Named Rules

**The No-Eyebrow Rule.** On the social layer a tracked uppercase kicker is a *named brand system* with a fixed vocabulary: "A 10X VISUALS FILM", "CRAFT · NO 01", "10X VISUALS · PHOTOGRAPHY", "VIRTUAL STAGING", "THE PROCESS". On the web layer it is banned as section scaffolding. A kicker above every section is not voice, it is grammar borrowed from a template; two pages shipped with one above 9 of 9 and 7 of 7 sections in July 2026 and both were stripped. Headings and hairlines carry the cadence.

**The No-Numbers Rule.** Numbered section markers (01 / 02 / 03) earn their place only when the section genuinely is an ordered sequence the reader must follow. A real three-step process qualifies. "01 About / 02 Services" does not.

**The No-Dashes Rule.** No em dashes or en dashes anywhere in user-facing copy, on either layer. Middots `·` and slashes `/` on graphics; commas, colons and full stops in prose.

**The Balance Rule.** `text-wrap: balance` on headings, `text-wrap: pretty` on prose. Headline copy is tested at every breakpoint; if it overflows, the copy is rewritten rather than the scale reduced.

## Layout

**Web layer.** A single centred wrap at `min(1180px, 91vw)`, with a narrower `min(780px, 91vw)` for long prose. Section padding of `clamp(3.4rem, 7vw, 5.6rem)`, alternating white and off-white grounds with dark sections used sparingly. Rhythm comes from alternating ground, not from varying padding. Grids use `repeat(auto-fit, minmax(275px, 1fr))`; flex-wrap for one-dimensional rows. Explicit breakpoints only at 640px and 880px, where the layout genuinely changes rather than merely shrinks.

**Mobile is the primary case**, because ad traffic is thumb-first. Buttons go full-width, hero gradients switch from horizontal to vertical so type stays legible over the frame, and every interactive target clears 44px. Wide content (tables, image rows) scrolls inside its own `overflow-x: auto` container so the page body never scrolls sideways.

**Social layer formats.**

| Format | Size | Layout |
|---|---|---|
| Project card | 1080×1350 | kicker + title lower-left, gradient 0.42 span |
| Craft card | 1080×1350 | series kicker + title centred, placed in sky/negative space |
| Recap card | 1080×1350 | huge month word centred ("JULY."), "THE MONTH THROUGH OUR LENS" |
| Hero | 1080×1350 | pure photo, zero type (The Local Project pattern) |
| Story frame | 1080×1920 | same grammar; safe zones top 170px / bottom 280px |
| Highlight cover | 1080×1080 | photo dimmed ×0.62 + 16% navy, white 10X mark centred at 34% height |

### Named Rules

**The One-Exit Rule.** An ad landing page has exactly one exit and it is the conversion. No site navigation, no menu, no linked logo. Every nav item on a page you paid for the click on is a way to lose that click, so the wordmark is a `<span>`, not an anchor.

**The Thumb-Reach Rule.** On a phone-first page the number lives under the thumb: a fixed bottom call bar, with the page's bottom padding computed as `calc(bar-height + env(safe-area-inset-bottom))` so the bar never covers the last line of content.

**The Dead-Zone Rule.** Social layer: no type in the IG UI dead zones, top ~170px and bottom ~280px on stories.

## Elevation & Depth

Both layers are essentially flat and build depth from tonal layering rather than shadows. The web layer alternates white, off-white and near-black grounds; the social layer stacks a gradient scrim over footage. Shadows appear in exactly two places: a soft wide ink shadow under white type on photography so it survives a bright frame, and a single diffuse lift under the form card so the conversion element reads as the nearest object on the page.

### Shadow Vocabulary
- **Type shadow** (`~9px blur of shadow-ink at ~alpha 150`): always present under white type on footage, social layer.
- **Form lift** (`box-shadow: 0 14px 40px rgba(16,47,65,.08)`): the form card only, tinted with brand navy rather than neutral black.
- **Hover lift** (`translateY(-2px)` plus the element's own colour shift): buttons and figures on pointer devices only, disabled under `hover: none`.

### Named Rules

**The Flat-Plus-Scrim Rule.** Depth is a change of ground, not a stack of cards. If a surface needs to feel closer, change its background or its scrim before reaching for a shadow. Nested cards are always wrong.

## Shapes

Soft but not rounded. Radii are small and functional: `6px` on buttons and fields, `8px` on image figures, `10px` on the form card, and `0` wherever a client's own identity calls for square edges (CVA's monochrome build uses `0` throughout, deliberately). Borders are single-pixel hairlines carrying structure. A border is never a decorative accent.

### Named Rules

**The No-Side-Stripe Rule.** A coloured border on one side of a card, callout or alert is banned outright. Depth or emphasis comes from a full hairline, a change of ground, or a leading element. The reflex is strong: it appeared on a rebate callout during the July 2026 build and was removed the same day.

## Components

### Buttons
- **Shape:** gently rounded (`6px`), never pill, never square unless the client identity is square.
- **Primary:** brand blue ground, ink-dark label, `1.05rem 2rem` padding, weight 600. Reads as the one thing to press.
- **Hover / Focus:** deepens to Blue Deep with a white label and a 2px lift over ~0.22s. Under `hover: none` the lift is dropped and an `:active` colour shift replaces it. Focus is a 2px brand-blue outline offset 3px, visible on light and dark grounds.
- **Ghost:** transparent with a hairline border, used once per hero as the secondary path. Never more than one per view.
- **Call button:** on trades pages the primary button is a `tel:` link carrying the number as its label, repeated at every scroll depth, with a sub-label naming who answers.

### Cards / Containers
- **Corner Style:** `10px` on the form card, `8px` on figures.
- **Background:** white on light sections; charcoal behind a figure so a loading image has a ground.
- **Shadow Strategy:** flat by default; only the form card lifts. See Elevation & Depth.
- **Border:** single-pixel Page Line hairline.
- **Internal Padding:** `clamp(1.7rem, 3.5vw, 2.3rem)`.

### Inputs / Fields
- **Style:** white ground, single-pixel border dark enough to clear 3:1 against both white and any card tint it sits on, `6px` radius, `0.85rem 0.95rem` padding, body weight at full size (never below 16px, so iOS does not zoom on focus).
- **Focus:** 2px Blue Ink outline offset 1px, border shifting to match. No glow.
- **Labels:** always present, always visible. Placeholder text is never a substitute for a label.

### Navigation
There is none on the web layer, by design. The header carries an unlinked wordmark and the phone number. See The One-Exit Rule.

### Conversion Form (signature component)
The form is the page's purpose and its shape is fixed: **four required fields maximum**, chosen for what the person answering the phone actually needs (name, phone, suburb or agency, one tap-to-choose job type), plus at most one optional free-text field labelled "(optional)". A spam honeypot stays. It sits last on the page, after every objection is answered, framed as a callback request rather than an enquiry.

### Named Rules

**The Four-Field Rule.** Four required fields, and email is not one of them. If the follow-up is a phone call, an email field is a question with no purpose, and every field costs completions. A required free-text message is the heaviest thing you can put on a mobile form and is never required. Written in blood: two live MVX pages shipped with six required fields including a required message, against an approved spec of four.

**The Calls-Are-The-Leads Rule.** On a phone-first page, `tel:` clicks are the primary conversion and the form submit is secondary. Track them that way or the ad platform optimises toward the weaker action and reports a fraction of real performance.

## Do's and Don'ts

### Do:
- **Do** message-match the page headline to the ad that delivered the visitor. One `<h1>`, naming the service and the city.
- **Do** give each service its own page and its own intent. Service-specific landing pages convert several times better than general ones; never point a hot water ad at a general electrician page.
- **Do** strip the site navigation and unlink the wordmark on every ad landing page.
- **Do** keep the form to four required fields, put it last, and label every input.
- **Do** measure contrast rather than eyeballing it: 4.5:1 for body text, 3:1 for large text and for the border of any interactive control, checked on every surface the token touches.
- **Do** clear 44px on every tap target, including phone numbers inside paragraphs and footers.
- **Do** use real photography at a resized variant. A 1024px file at 80–160KB beats an 8MB original nobody waits for.
- **Do** write alt text naming the actual project ("88 Third Avenue, shot by 10x Visuals"), not the category.
- **Do** verify every image URL resolves before shipping. Placeholder filenames that 404 turn an image-led page into a text page.
- **Do** ship pages with no JavaScript when the page doesn't need it. All three current landing pages are JS-free, and it is why they are fast.
- **Do** honour `prefers-reduced-motion` and `hover: none` on every transition.

### Don't:
- **Don't** put a tracked uppercase kicker above every section. On the web layer, don't use one at all.
- **Don't** number sections (01 / 02 / 03) unless the order is information the reader needs.
- **Don't** use a coloured border on one side of anything.
- **Don't** put an em dash in user-facing copy.
- **Don't** require email, postcode, or a free-text message on a callback form.
- **Don't** let a contrast fix on one surface go unchecked on the other surfaces that token appears on.
- **Don't** put an unverified claim, price, rebate figure or review count on a client page. Every number is confirmed with the client first, and figures that move (rebates, prices) are confirmed at quote rather than promised on the page.
- **Don't** port one client's palette, voice or playbook onto another client's page.
- **Don't** assume a page matches its spec because the spec was approved. Re-read the live markup after anyone else rebuilds it.
- **Don't** add motion to an ad landing page for decoration. Motion competes with the conversion.

## Logos

Real files only, never text wordmarks, except on landing pages where the client's own logo is unavailable and a type lockup is a documented placeholder. See auto-memory `reference-brand-assets`. White 10X mark baked at `10x Premium Kit/_assets/10x_mark_white.png`. Only white logos exist; dark export still pending from the designer.

## Imagery rules

**Social layer.** Source from `10x Library/_Selected` (55 curated keepers) plus project folders, picked from eyeballed contact sheets and never from filenames. No third-party branding, map pins, sold signs or watermarks in frames. Never re-post already-published media; check the live feed first. One property per highlight cover, and vary properties across a posting run (no three near-identical sunsets in one pack).

**Web layer.** Client sites are the source: pull the client's own project photography and use the platform's resized variant, not the original upload. Verify every URL returns 200 before shipping. Lazy-load everything below the fold; hero images are CSS backgrounds and load eagerly. Alt text names the project.

---
_Vault: [[overview]] · social-layer context: [[brand-system]] · web-layer pages: [[lead-gen-engine]]_
