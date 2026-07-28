# MVX new builds & renos landing page

One file: [index.html](index.html). Embedded CSS and JS, no frameworks, no build step.
Assets in `assets/`. Open it in a browser and it works.

Built for Meta ad traffic from the new builds and renovations campaign
(`../mvx-meta-rebuild/BUILD-NEWBUILDS.md`). Single goal: request a free quote.

## Before it goes live

- [ ] **Wire the form.** `data-endpoint="REPLACE_ME"` on the `<form>`. While it reads
  REPLACE_ME the page shows the success state and logs a console warning, so the
  states can be reviewed without pretending in production.
- [ ] **Confirm the licence and insurance line.** Two visible placeholders, in the
  trust strip and the footer. They are deliberately marked, not invented.
- [ ] Upload the two photos and the logo, swap the relative paths for real URLs.
- [ ] Submit a test enquiry from a phone and confirm it arrives where Matt sees it.
- [ ] Track the form submit as a conversion, and `tel:` clicks as secondary.

## Decisions worth knowing

**Neutral off-white, not warm cream.** The brief asked for warm neutrals. A warm
near-white body is the single most saturated look in current AI-generated design,
and MVX's own base is black and white with green as the accent. Neutral off-white
`#f7f7f7`, black grounds, green on the actions only. Calm and premium, but theirs.

**No navigation.** Header carries the wordmark and the phone number. Every nav item
is a way to lose a click that was paid for.

**One CTA, five times.** Hero, why-plan-early, the form itself, the sticky mobile
bar, and the phone as the fallback. No competing actions anywhere.

**The sticky bar hides itself** once the form is on screen, via IntersectionObserver.
It would otherwise cover the button the visitor is already looking at.

**Form is five fields, four required.** Name, phone, email, project type required;
job details optional. Email stays because a quote gets emailed. Typed input is kept
in `sessionStorage`, so an interruption does not wipe the form.

**Validation is progressive enhancement.** The markup ships without `novalidate`, so
a visitor with JS off still gets the browser's checks. The script switches it off once
it is running and replaces the browser bubbles with plain-language messages beside
each field.

**`.err[hidden]{display:none}` is load-bearing.** An author `display:flex` beats the
`hidden` attribute, and without that line every error row renders on page load as a
bare "!" glyph. It has bitten this codebase once already.

## Edge cases handled

Tested rather than assumed:

| Case | Behaviour |
|---|---|
| JavaScript off | `<noscript>` block tells the visitor to call. Without it a valid submit posted to `#` and looked like it worked |
| Offline | Caught before the fetch, so the button does not sit on "Sending" waiting for a timeout |
| Stalled connection | 15s `AbortController` timeout, then the failure state |
| Handler returns 200 with an error body | Read as JSON if it is JSON, treated as a failure, never as a send |
| Network failure | Failure state shown, button reset, form still filled, success never shown |
| Triple-tap submit | Guarded by `aria-busy`; one send, one success |
| Emoji, CJK, RTL input | Accepted, no layout shift |
| Emoji in the phone field | Rejected by `pattern`; `+61 (07) 5555 1234` accepted |
| Very long unbroken words | `overflow-wrap:break-word` on text elements, no page overflow |
| `sessionStorage` unavailable | Wrapped in try/catch, form still works |

**`maxlength` and `pattern` are conveniences for the person typing, not
validation.** A script can set any value and a POST can be hand-crafted, so the
handler must validate length and content itself and rate-limit.

## Verified

No horizontal overflow at 375 or 1280. One `h1`, no heading skips. Every image has
alt text, every input has a label, no dead links, no tap target under 44px. Empty
submit produces four plain-language errors and moves focus to the first one; a wrong
email errors alone while other input survives; a valid submit shows the busy state
then the success block and clears the store.
