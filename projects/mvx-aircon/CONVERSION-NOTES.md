# MVX Aircon Landing Page — Conversion Redesign Notes

**Deliverable:** `landing-page.html` (self-contained, ready to view in any browser; rebuild in Elementor using this as the visual + copy spec).
**Goal:** Beat the current page's conversion rate and match/exceed T42 Electrical's landing page for Google Ads traffic on "air conditioning Gold Coast" queries. Primary conversion = phone call; form is the fallback at the bottom.

## What was wrong with the current page

1. **One phone CTA on the whole page** (hero only). T42 repeats theirs 10+ times. Every scroll depth needs an exit ramp to the phone.
2. **Form too high and too heavy.** 7 required fields including email + postcode + two free-text questions. Friction kills mobile ad traffic. Brief says: push calls, form last.
3. **H1 doesn't message-match the ad.** "NEED HELP WITH YOUR AIRCON?" ≠ what the visitor searched. Google Ads Quality Score and bounce both punish this.
4. **No sticky mobile call bar.** Most ad clicks are mobile; the number must live under the thumb.
5. **Testimonials are generic electrical**, unlabelled for aircon, and very long.
6. **No differentiator argument.** T42 claims 25 years + 300 reviews; MVX needs its own angle, not a weaker copy of theirs.

## The new structure (top → bottom)

| Section | Job | CTA |
|---|---|---|
| Sticky mobile call bar | Phone always under thumb (T42 doesn't have this — our edge) | Call + quote anchor |
| Header | Logo + phone | Call |
| Hero | Message-match H1 "Air Conditioning Installation & Repair, Gold Coast", 4.9★ chip, 4 tick points | Call (primary) + "prefer we call you?" anchor |
| Licence strip (volt green) | ARC + NSW licence numbers immediately after hero — legitimacy in 1 second | — |
| Services ×4 | Split install / repairs / service & clean / ducted — each ends in a phone CTA | Call ×4 |
| CTA band | "Sweating it out right now?" urgency break | Call |
| Why MVX | The differentiator: **we ARE the electricians — one trade, one visit, one bill** (aircon-only shops subcontract the sparky work) | Call |
| 3 steps | Reduce anxiety about what happens after the call | — |
| Reviews | 4.9 Google badge + 3 trimmed real reviews | — |
| Brands row | Daikin / Mitsubishi / Fujitsu / Panasonic / Hisense / LG — **confirm with Matt which brands he actually supplies** | — |
| Suburbs | Local relevance + keyword surface | — |
| FAQ | Objection handling (speed, cost, repair-vs-replace, "do I need an electrician?") | — |
| Form (last) | Callback framing, 4 fields + optional message. Call CTA sits beside it one final time | Call + submit |
| Footer | All licence numbers | Call |

**11 tap-to-call links total.**

## Key conversion decisions

- **Form cut from 7 required fields to 4** (name, phone, suburb, job type). Email removed — you're calling them back, not emailing. Every removed field measurably lifts completion.
- **"Prefer we call you?"** framing keeps the form as callback-request, not enquiry — consistent with phone-first strategy.
- **Differentiator is structural, not claimed:** T42 can say "25 years"; MVX counters with "every install legally needs a licensed electrician — we are one, so nothing is subcontracted." Verifiable, unique, and hard for aircon-only competitors to copy.
- **Volt green (#7EC004) + black** = existing MVX brand, kept. Green reserved for actions and the licence strip so the eye lands on "call".

## Before going live — checklist

- [ ] Confirm brand list with Matt (Daikin/Mitsubishi/etc.)
- [ ] Confirm "same-day response" promise is deliverable (it's stated ~5 times)
- [ ] Wire form to Formidable (existing plugin) with the 4-field layout; keep spam honeypot
- [ ] Use a **Google Ads call-tracking number** swap (or at least tel: click events in GA4/Google Ads as conversions)
- [ ] Fire conversion events: tel: clicks (primary), form submit (secondary)
- [ ] Real review count/score pulled from actual Google Business Profile before claiming 4.9
- [ ] Strip site-wide nav from the live version (landing pages leak less with no menu — current page has full nav; new design already omits it)
