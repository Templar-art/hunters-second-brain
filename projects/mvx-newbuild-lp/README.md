# MVX new builds & renos landing page

One file: [index.html](index.html). Embedded CSS and JS, no frameworks, no build step.
Assets in `assets/`. Open it in a browser and it works.

Built for Meta ad traffic from the new builds and renovations campaign
(`../mvx-meta-rebuild/BUILD-NEWBUILDS.md`). Single goal: get a phone call on 0468 049 157.

## Before it goes live

- [ ] **Confirm the licence and insurance line.** Two visible placeholders, in the
  trust strip and the footer. They are deliberately marked, not invented.
- [ ] Nothing to upload. Both photos are live off mvxelectrical.com.au and the logo
  is no longer used, so `assets/` is now unreferenced by the page.
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

**No header, no footer.** Removed 28 Jul. The page is now hero to FAQ and nothing
else, on the assumption it is being dropped into the MVX WordPress theme, which will
supply its own header and footer. Two things went with them, both worth knowing:

- **The logo is no longer on the page at all.** It only ever appeared in the header
  and footer. `assets/logo-white-64.png` and `-96.png` are now unreferenced.
- **One of the two licence placeholders is gone.** The footer carried a legal line;
  the remaining marker is the one in the trust strip under the hero, still reading
  `[Licence and insurance details to confirm]`.

There is also no longer a phone number pinned to the top or bottom of the page. On
mobile the sticky bar covers it. On desktop the number appears in the hero, in the
why-plan-early section and in the not-this-page note, and nowhere else, so a desktop
visitor mid-page has to scroll to find it. Worth letting the sticky bar show on
desktop too if that matters.

**Body margin is scoped, not reset.** The default 8px body margin used to sit behind
the header and now shows as a frame standalone, but a bare `body{margin:0}` in an
embedded style block would fight the theme. It is written as
`body:has(> .mvx-lp){margin:0}`, so it only applies when the wrapper is a direct
child of body, which is this file on its own.

**FAQ is the last section.** The closing "Tell us about your project" band was
removed 28 Jul. It also fixed a rhythm problem: the page previously ended in three
dark bands in a row (FAQ, call band, footer) with no break between them, so it
finished as one undifferentiated mass. Now it runs grey, dark, footer.

**Zero JavaScript.** Removing the form took the validation script, and removing the
call band took the sticky-bar observer with it, because the only thing that observer
did was hide the bar over that band. Nothing on the page depends on JS now. The
sticky call bar is CSS only.

**Photos are live off the client's site, wired through WordPress's own sizes.**
`8166` is the hero, `283` is the rough-in. The bare upload URLs are 2000px files at
**2.4 MB and 1 MB**; using them as given would have made this a ~3.5 MB page and
undone the whole responsive pass. WordPress had already generated 768 / 1024 / 1536
variants of both, so `srcset` comes off those and the full-size file is never served.
A phone at 2x pulls the 1024 hero and the 768 rough-in, about 212 KB of photo.

That is still heavier than the 76 KB the local WebP set managed, because WordPress
serves JPEG only at these sizes and there is no WebP on the origin. The optimised
set is still in `assets/` if that weight is ever worth reclaiming: upload it and
point the `srcset` back at local paths.

**Cross-origin images cannot be weighed from the page.** `encodedBodySize` reports 0
for them without a `Timing-Allow-Origin` header, so the sizes above come from the
origin's `Content-Length`, not from `performance.getEntriesByType`.

**No form. The phone is the action.** Removed 28 Jul on Hunter's call. Every CTA is
now `tel:0427593990`: hero, why-plan-early, the closing band, the sticky mobile bar,
and the header. One action, four places, no competing exits.

Worth knowing what that removed as well as what it cost. Gone: the `REPLACE_ME`
endpoint that would have shown a **fake success state** if it ever shipped unwired,
about 180 lines of validation JS, the `sessionStorage` draft restore, and the whole
error-state surface. The page went 761 lines to 543 and now has no way to fail
silently. What it costs is the out-of-hours enquiry: someone scrolling at 11pm can no
longer leave their details, so that lead depends on them remembering to ring.

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
| JavaScript off | No effect whatsoever. The page ships no JS |
| Emoji, CJK, RTL input | n/a, no inputs left on the page |
| Very long unbroken words | `overflow-wrap:break-word` on text elements, no page overflow |
| Origin images unreachable | Alt text carries the meaning; layout holds, since both images have width and height |

## Verified

Measured at 390 in a real 390px viewport: `scrollWidth` 390, zero elements
overflowing. One `h1`, no heading skips. Every image has alt text, no dead links, no
tap target under 44px, four `tel:` CTAs and no `<form>` left anywhere.

**Headless Chrome cannot verify mobile on this Mac.** Asked for a 390px window it
reports `innerWidth=500`, lays out at 500 and crops the screenshot to 390, which
looks exactly like the page overflowing. Two apparent overflow bugs here were that,
not the page. Narrow-viewport checks go through the browser pane, which honours the
width it is given.
