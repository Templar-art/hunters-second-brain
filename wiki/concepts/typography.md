---
type: concept
tags: [design, typography, brand, client-work]
updated: 2026-08-10
---

# Typeface Selection

The durable version of the type decision, so it does not get re-researched per client. 10x's own
type is fixed and lives in [[brand-system]] — this page is for choosing type *for a client*.

## Serif vs sans serif

A serif is the small stroke hanging off the end of a letter — the feet on the legs of an **R**,
the flick at the tip of a **g**. *Sans* is French for *without*. That is the whole distinction;
everything after it is register, not structure.

Serifs read as older, established, printed — good for authority, slower at small sizes on screen.
Sans serifs read as current and plain-spoken, and hold up at 13px on a phone. Most brands run
both: serif headlines for weight, sans for everything a person actually has to read (body, buttons,
captions, ad copy).

## The three sans families

Pick the family first, then the face inside it. This is the part that makes the decision fast.

| Family | Shape | Reads as | Watch out for |
|---|---|---|---|
| **Grotesque** | Swiss-descended, deliberately neutral | Institutional, factual — banks, airlines | Anonymous; Inter in particular is everywhere |
| **Geometric** | Circles and straight lines | Modern, friendly, start-up | Tiring in long paragraphs, light on gravitas, eats width |
| **Humanist** | Shaped by handwriting, slightly irregular | Warm, civic, editorial, trustworthy | Least "designed" looking if the brief wants edge |

Long body copy and an older or trust-driven audience → humanist. Fixed-width ad boxes → grotesque
with real condensed widths. Logotype only → geometric is fine.

## Standing rules

- **Never put a client in Poppins.** It is 10x's own face ([[brand-system]]); a client should not
  wear its agency's typeface.
- **Inter is a fallback, not a choice.** Technically excellent, drawn for screens, and the default
  of nearly every app built since 2019 — it contributes zero brand distinction.
- **Two faces, four roles.** Display / kicker / body / figures. Anything beyond that and the
  restraint that reads as premium starts to leak — same principle as the premium law in
  [[brand-system]].
- **`font-variant-numeric: tabular-nums`** wherever prices, rates or counts stack in a column.

## Licensing

- **Google Fonts** — Open Font Licence throughout: free commercially, free to install, free to
  self-host, no attribution. Default here for client work; nothing to check.
- **Fontshare** (Satoshi, General Sans, Switzer, Sora) — free for commercial use, but the licence
  is reported to require the foundry's **written consent before self-hosting the webfont files**.
  Fine for print and video, a question mark on a client website. ⚠️ Confirm current terms with
  Fontshare before specifying one on a build; this has not been verified against the licence text
  itself, only against secondary sources (10 Aug 2026).
- Anything sold per-seat or per-pageview is a client purchase, not an agency one — never bury a
  paid licence inside a deliverable.

## No-serif systems

When a client rules serifs out — as O'Neill Group's did, on the grounds of disliking the pointy
parts — the easy source of contrast disappears. Do **not** answer it by hunting for a second sans:
two sans serifs sitting close together read as a mistake rather than a pairing. Go to **one family
and build the hierarchy from weight, size and tracking**. Single-family systems read as disciplined
rather than sparse, which is the same argument as the premium law in [[brand-system]].

The face then has to survive both ends alone — 13px fine print *and* a 46px Bold hero. That range,
not personality, becomes the selection criterion.

"No serifs" also often means "nothing pointy", which is a different constraint: it is about how the
stroke ends are finished — cut flat, cut at an angle, or blunt and soft. Soft-ended faces worth
knowing: **Manrope** (soft but still has a spine), **Hanken Grotesk** (calm, recedes), **Red Hat
Text** (warm corporate), **Figtree** and **Albert Sans** (soft geometrics), **Nunito Sans**
(genuinely rounded, and too informal for anything financial).

The faces drawn *for* headline-plus-body duty are the ones to reach for when there is no serif to
share the load: **Schibsted Grotesk** (commissioned by a Nordic news group), **Libre Franklin** and
its federal-design-system fork **Public Sans**, and **Red Hat** / **Wix Madefor**, which ship
separate Display and Text cuts. **Lexend** is the outlier worth remembering — drawn with wide
apertures specifically to lower reading effort, with research behind it, which is a real argument
when the audience skews older.

## Applied: O'Neill Group (10 Aug 2026)

Nineteen free faces with the client's own name set in each one, rendered in themselves so the choice
is made by eye: [sans-serif-shortlist.html](../../projects/oneill-group-type/sans-serif-shortlist.html) ·
[artifact](https://claude.ai/code/artifact/80e5acd5-0afb-45ce-a40a-d7b7fc2d6071)

**Recommendation: Libre Franklin across the whole system** — Bold 700 headlines, SemiBold 600
kickers tracked 0.18em caps, Regular 400 body, SemiBold tabular figures. It descends from Franklin
Gothic, the face of American newspapers and civic signage for a century: established without
reading old, and the only candidate equally convincing at 13px and at 46px.

**Closest rival: Schibsted Grotesk** — purpose-drawn for headline and body in one voice, and barely
used in Australian property. Libre Franklin takes it on two counts only: a century of civic and
financial usage behind the shapes, and nine weights against six, which matters when one family
covers hero to disclaimer. Swap them if the brand should look less like the category.

Runner-up on softness **Manrope**; **Hanken Grotesk** if the type should recede; **Lexend** if the
readability argument wins. Ruled out: **Outfit** (fintech register), **Poppins** (agency conflict),
**Inter** (incumbent, flawless and completely undistinctive), **IBM Plex Sans** (engineered, colder
than the brief), **Nunito Sans** and **Gabarito** (trade gravitas for friendliness — wrong when the
subject is somebody's mortgage).

⚠️ **Two things unconfirmed.** Written against the Quiet Equity system on file for Brian O'Neill's
[[strategic-investing-qld]] — navy, gold, Marcellus, Inter. If O'Neill Group is a separate entity
rather than a parent or rebrand of that one, the palette needs re-checking; the eleven candidates
and the family logic hold either way. And if it *is* the same brand, dropping serifs means
**retiring Marcellus** — a live change to an existing identity, not just a body-face choice, and
every asset already built on it would need reissuing.

## Related
[[brand-system]] · [[strategic-investing-qld]] · [[content-systems]]
