---
type: concept
tags: [web, design, build, client-sites, accessibility]
updated: 2026-09-29
---

# Premium web build

How 10x builds a client site that reads as a different type of business rather than a
darker version of a commercial template. Distilled from [[iron-standard]] (six-page
enquiry-led site, Sept 2026) and the web builds before it. Design *references* live in
[[real-estate-design-refs]]; this page is the build discipline.

## The failure mode to design against

A generic agency template with the brand colours dropped in is a failure even when it is
technically clean. The tells, in order of how badly they give the game away:

1. Three equal boxes in a row with an icon, a heading and two lines of text. The single
   biggest giveaway.
2. The stock section order: hero → three feature cards → testimonial → CTA band → footer.
3. Generic industry icons. For a gym that means dumbbells, flames, stopwatches, hearts.
4. Uniform, centred, symmetrical sections stacked at identical rhythm.
5. Rounded corners, soft shadows and hover-lift on everything.
6. Carousels and sliders of any kind.

## The rule that does most of the work

**No two consecutive sections share a layout pattern.** Alternate full-bleed image,
asymmetric split, editorial text block, oversized type statement, offset image pair. Mirror
a split later in the page so the image bleeds off the opposite edge. This one constraint
forces variety and is the main thing to preserve when extending a site.

Supporting moves:

- **A real 12-column grid, broken deliberately.** Text in columns 2–6, image bleeding off
  the right edge, a headline starting at column 1 and running wide.
- **Extreme type-scale contrast.** Huge bold uppercase display, roughly
  `clamp(48px, 7vw, 110px)`, against 11–13px wide-tracked all-caps eyebrow labels. The gap
  between the two is what creates the premium feel, not the typeface.
- **Let images bleed** past the viewport edge. Never a polite contained rectangle with
  equal margins.
- **Generous negative space.** Confidence to let one image carry a whole screen.
- **Numbers and labels as design elements**: section numbers, thin accent rules,
  wide-tracked category marks. Borrow the structure of the client's own brand guidelines.

## Accent colour is not a text colour

A saturated brand accent usually fails WCAG AA as small text or as a button label on white,
and passes comfortably against black. Iron Standard's `#F4502A` is 3.48:1 on white and
6.03:1 on black, which is exactly why that site is dark by default: dark is the condition
where the accent is both strongest and compliant.

**Test the accent against both grounds before committing to a light or dark default.** The
result often decides the whole visual direction. Buttons in the accent take black labels.

Ration the accent to primary actions plus one emphasis per section. If every section is
accented, the accent dies and the brand reads as a promotion.

## Motion

Purposeful only: motion confirms a change of state or reveals content already on its way,
it never performs.

- 200–300ms, ease-out. No bounce, elastic or spring.
- Reveal = fade plus a 12–20px rise. One idea per reveal, no staggered cascades.
- Never hijack the scroll. No pinned sections, no forced scroll speed.
- `IntersectionObserver` for reveals, never scroll listeners. A sentinel element plus an
  observer also handles the "header goes solid on scroll" case without a listener.
- Respect `prefers-reduced-motion` by making transitions resolve instantly rather than
  removing them, and check both directions of a toggle. A reduced-motion regression on
  *opening* a nav while *closing* still respected it has shipped here before.
- **Animate transform and opacity only.** Animating `gap`, `padding`, `width` or `height`
  causes layout work every frame. A header that condenses on scroll should scale its logo
  and change its background, not animate its padding.

## Structural gotchas that have cost real time

- **`backdrop-filter` (or any filter or transform) on an ancestor makes it the containing
  block for `position: fixed` descendants.** A full-screen fixed nav panel placed inside a
  blurred header gets trapped inside the header's box. Keep overlay panels as direct
  children of `<body>`.
- **A single-line full-bleed trick needs the right maths.** `margin-right: calc(50% - 50vw)`
  only works when the element is as wide as its centred container. For a grid item spanning
  part of the grid, compute the distance from the container's content edge to the viewport
  edge instead:
  `--edge: calc((100vw - min(100vw, var(--maxw))) / 2 + var(--pad))`.
- **The 12-column grid is a desktop layer.** Declare `grid-template-columns: 1fr` mobile-first
  and introduce the 12 columns at the breakpoint, or every unspanned child collapses into a
  single narrow column and text overflows the viewport.
- **Grid children with no explicit span land in column 1.** Section marks and stray notes
  silently wrap. Worth auditing programmatically: walk `.grid > *` and flag any whose
  computed `gridColumn` is `auto`.
- **An inline `style="margin:0"` beats a stylesheet bleed rule.** Reset element defaults in
  CSS instead.
- **Scoped link styles leak into buttons.** A rule like `.nav-panel a { font-size: 40px }`
  will hit an `<a class="btn">` inside that panel. Use `a:not(.btn)`.
- **`position: fixed` on a `<form>`'s sibling iframe is fine, but `100vw` includes the
  scrollbar.** Over-bleeding is safe when the section clips; under-bleeding shows a seam.

## A `position: fixed` hero backdrop paints over what follows

If the hero image is fixed rather than scrolling, every section after it needs an opaque
background wrapper or the page appears to break. Learned on the earlier Iron Standard build.

## Verify by measurement, not by screenshot

The in-app preview pane produces **stale, corrupted composites when a page with a fixed
header is scrolled** — it paints the header mid-viewport with a void above it. This is a
tooling artefact and not a page defect. Confirm with `getBoundingClientRect()` and
`document.elementFromPoint()` before chasing it, then check the page in real Chrome.

Checks worth running on every build, at 375px and at desktop width:

- horizontal overflow (`scrollWidth - clientWidth`)
- heading order, and exactly one `h1` per page
- `alt` on every image
- internal link integrity across every page, including footer legal links
- a closed mobile nav must be genuinely unfocusable. Test by attempting to focus each link,
  not by checking `offsetParent`, which does not detect `visibility: hidden`
- form inputs at 16px, or mobile browsers zoom on focus
- every `<label>` bound to a real input id
- type set in `rem`, not `px`: set the root to 200% and confirm text grows. Pixel type ignores a
  visitor's browser or Android text-size setting entirely (page zoom still works, so it is not a
  hard WCAG fail, but low-vision visitors get nothing). Converting `px/16` keeps the default
  render pixel-identical. Iron Standard shipped px until the 7 Oct 2026 polish.

## Client-site form backends

See [[iron-standard]] and the auto-memory reference on Apps Script form handlers. The
short version: Apps Script Web Apps return no CORS headers, so POST through a hidden
iframe; never notify via `Session.getActiveUser()`; and until the endpoint is live, make
the form **say** it is not connected rather than appearing to send.

**The hidden-iframe submit bug (Iron Standard, found 29 Sep 2026).** A submit handler that
calls `preventDefault()` for validation must re-issue the submit explicitly
(`HTMLFormElement.prototype.submit.call(form)`). The shipped version set `form.action` and
never submitted, then showed "Thank you" on a timer: invisible while the endpoint was a
placeholder, total silent loss the day it went live. Never fake success on a timer. Have the
Apps Script answer with `HtmlService` + `ALLOWALL` and a `window.top.postMessage({ok})`, listen
for it with an origin check, keep the visitor's input until it arrives, and treat 20s of
silence as failure. Also prefix cell values starting `= + - @` with `'` or a message can run as
a Sheets formula.

**Norwegian (and German) compounds break display type.** `overflow-wrap:break-word` does not
reduce min-content, so a single long word still pushes a grid track wider and gets clipped
by an `overflow:hidden` hero. Use `overflow-wrap:anywhere` plus `min-width:0` on grid
children, and size the hero to its longest real word (`min(var(--display), calc((100vw -
64px) / 6.4))`, or `100cqi` with `container-type:inline-size` when the headline sits in a split column, since a viewport formula misses that case) so small phones shrink the type instead of breaking a word mid-way.

## Honesty in a pre-launch build

When the business does not exist yet, the site must not imply it does. Working patterns:

- Label proposed features as planned, visually distinct from confirmed ones.
- Mark placeholder imagery in the footer, once, plainly.
- Leave unconfirmed blocks (address, pricing, dates) as HTML comments with a restore note,
  not as visibly empty sections.
- Where the client still owes copy, ship a visible placeholder note rather than invented
  facts. Fabricated founder credentials are the fastest way to lose a client's trust.
