# MVX new builds & renos landing page

One file: [index.html](index.html). Embedded CSS and JS, no frameworks, no build step.
Assets in `assets/`. Open it in a browser and it works.

Built for Meta ad traffic from the new builds and renovations campaign
(`../mvx-meta-rebuild/BUILD-NEWBUILDS.md`). Single goal: get a phone call.

## Before it goes live

- [ ] **Confirm the licence and insurance line.** Two visible placeholders, in the
  trust strip and the footer. They are deliberately marked, not invented.
- [ ] Upload the photos and the logo, swap the relative paths for real URLs. **Both
  photos ship as a `<picture>` with a WebP `srcset` and a JPEG fallback, so every
  size in `assets/` has to go up, not just one.**
- [ ] Tap every `tel:` link on a real phone and confirm it dials.
- [ ] Track `tel:` clicks as the conversion. There is no form, so a call is the only
  lead this page produces and it is the only thing worth counting.

## Decisions worth knowing

**Neutral off-white, not warm cream.** The brief asked for warm neutrals. A warm
near-white body is the single most saturated look in current AI-generated design,
and MVX's own base is black and white with green as the accent. Neutral off-white
`#f7f7f7`, black grounds, green on the actions only. Calm and premium, but theirs.

**No navigation.** Header carries the wordmark and the phone number. Every nav item
is a way to lose a click that was paid for.

**Services are two tiers, not four equal rows.** They were four identical editorial
rows, so nothing read as more important than anything else and a scroller could not
tell at a glance what MVX actually does. Now the three jobs that matter run at
display scale with a green rule and a scope line, and the smaller work is one dark
strip below them. The tier break is carried by three things at once: scale (a
display face against Poppins at 1.16rem), surface (dark panel against white), and
typeface role. No icons, no fourth identical card.

**No form. The phone is the action.** Removed 28 Jul on Hunter's call. Every CTA is
now `tel:0427593990`: hero, why-plan-early, the closing band, the sticky mobile bar,
and the header. One action, four places, no competing exits.

Worth knowing what that removed as well as what it cost. Gone: the `REPLACE_ME`
endpoint that would have shown a **fake success state** if it ever shipped unwired,
about 180 lines of validation JS, the `sessionStorage` draft restore, and the whole
error-state surface. The page went 761 lines to 543 and now has no way to fail
silently. What it costs is the out-of-hours enquiry: someone scrolling at 11pm can no
longer leave their details, so that lead depends on them remembering to ring.

**The sticky bar hides itself** over the closing call band, via IntersectionObserver.
It would otherwise cover the button the visitor is already looking at.

**Copy had to move with it.** Three lines referred to a form that no longer exists:
step 01 said "fill in the short form", the hero said to ring instead if it was
urgent (now every action is a ring), and the not-this-page note pointed at the phone
as though it were the alternative. All three rewritten, not left to contradict the
page.

## Weight

Measured on the page, not estimated. A visitor on a 390px phone at 2× downloads
**112.5 KB** total, of which 76 KB is images. Before the responsive pass it was
**431 KB** for every visitor regardless of screen, a 74% reduction.

**The hero is an `<img>`, not a CSS background.** A background image is invisible to
the browser until the CSS parses, cannot use `srcset`, and this one is the LCP
element. As an `<img>` with `fetchpriority="high"` it is found while the HTML is
still being read: LCP lands at 96 ms locally. The gradient sits above it on
`z-index:1` and the copy on `z-index:2`, so the look is unchanged.

**No AVIF, deliberately.** It was generated and measured, and at the sizes this page
actually serves it came out *larger* than WebP (hero 119 vs 115 KB, rough-in 39 vs
31 KB). A third format for a negative saving is just more files to keep in sync.

**A 750w step is not enough on its own.** A 390px phone at 2× needs 780px, which
skipped straight past 750w to the 1200w file. The 800w step exists for exactly that
very common case and saves 27 KB on it.

**Logo densities, not a 1181px PNG for a 32px mark.** `logo-white-64.png` at 1×,
`logo-white-96.png` at 2×: 5 KB and 8 KB against the original 24 KB.

## Edge cases handled

Tested rather than assumed:

| Case | Behaviour |
|---|---|
| JavaScript off | Page is fully readable and every CTA still dials. Nothing on it depends on JS except the sticky bar hiding itself |
| Emoji, CJK, RTL input | n/a, no inputs left on the page |
| Very long unbroken words | `overflow-wrap:break-word` on text elements, no page overflow |
| No `IntersectionObserver` | Sticky bar simply stays visible, guarded by a feature check |

## Verified

Measured at 390 in a real 390px viewport: `scrollWidth` 390, zero elements
overflowing. One `h1`, no heading skips. Every image has alt text, no dead links, no
tap target under 44px, four `tel:` CTAs and no `<form>` left anywhere.

**Headless Chrome cannot verify mobile on this Mac.** Asked for a 390px window it
reports `innerWidth=500`, lays out at 500 and crops the screenshot to 390, which
looks exactly like the page overflowing. Two apparent overflow bugs here were that,
not the page. Narrow-viewport checks go through the browser pane, which honours the
width it is given.
