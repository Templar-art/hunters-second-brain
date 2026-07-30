---
type: project
tags: [lead-gen, ads, google-ads, meta-ads, landing-pages, mvx, cva, 10x-visuals]
status: active
updated: 2026-07-30
---

# Lead Gen Engine — ads + landing pages across three clients

The July 2026 push to build actual lead channels for [[mvx-electrical]], [[cva-architects]] and 10x Visuals itself. Started as "why aren't the ads working" and became "there is nothing for the ads to land on."

## The diagnosis it came out of

Evidence gathered 27 Jul from live sites, sitemaps and page markup, not from ad accounts (no access that session; the `10x-crm` MCP is unauthorised). Full detail in the 27 Jul [[log]] entry.

| Client | Why no leads | Fixable by |
|---|---|---|
| MVX | **No hot water surface exists** anywhere on a 29-page site. Nothing for search demand to land on. Aircon leads flow because aircon is the only funded, page-backed service. | A page, then spend |
| MVX | Both live ad LPs re-added form friction in the Elementor build: six required fields incl. a required free-text message | [FORM-FIX.md](../../projects/mvx-lead-fix/FORM-FIX.md) |
| CVA | Every CTA points at `/contact`, which only catches people who already decided to hire an architect. No top-of-funnel offer against a 6–18 month consideration window | A feasibility offer |
| 10x | **⚠️ Superseded 30 Jul 2026.** A form *does* exist at `/contact-us/`, so the 27 Jul "no lead form at all" reading was wrong. It carries seven fields including a required free-text message, the same friction we bill MVX to remove. The 20 Jul Meta campaign still spent ~$160 for zero leads. The homepage rebuild adds a three-field inline capture, see [[10x-website]] | Cut the contact form to three fields |

## The strategy

[AD-STRATEGY.md](../../projects/lead-audit-2026-07-28/AD-STRATEGY.md) — per-niche research (with sources), campaign structures, keyword sets, negatives, and ready-to-paste Google RSA + Meta copy for all three.

**The organising rule: match the platform to how the buyer arrives.** Something broke → Google Search. Considering a big change → Meta. Getting this backwards is what each of the three accounts was doing.

Three findings that shaped everything:
- **Service-specific landing pages convert ~8–12% vs ~2–3% for generic ones.** One page per service, per intent. This is why hot water gets its own page rather than a section on the electrician page.
- **Trades vs architects need opposite copy.** MVX wants volume (emergency intent converts 15–25%, and emergency calls book at ~78% vs ~23% for general enquiries). CVA wants the *opposite*: qualifying copy with project minimums cut one firm's lead volume 22% while raising revenue. Judge CVA on cost per booked project, never CPL.
- **10x's unfair advantage is unused.** Rotating 30+ creatives cuts CPL by up to ~43%, and 10x is a video production company. The thing that makes ads cheap is the thing they sell. Meanwhile CVA's June job produced 19 stills + ~40 clips sitting idle — a finished, already-paid-for ad library.

**The internal benchmark to copy, not reinvent:** [[strategic-investing-qld]] produced 10–15 leads in 4 business days. Attribution still unconfirmed (two assets shipped, one deliberately CTA-free) — pin down spend, objective and *where the lead landed* before replicating.

## Landing pages built (28 Jul 2026)

All three self-contained, brand-scoped, mobile-first, no-nav (ad pages leak through menus), form last, ≤4 required fields. All carry a pre-launch checklist in the file footer.

- **[MVX hot water](../../projects/mvx-hot-water/landing-page.html)** — reuses the proven aircon-page conversion system (League Gothic/Poppins, volt green, sticky call bar, licence strip). Heat-pump STC rebate as the hook. ⚠️ Written for **Route A** (MVX partners a plumber); every dependent line is marked `ROUTE-A` for a one-edit swap to electrical-only. Includes the correct 4-field form so it can't be rebuilt wrong again.
- **[CVA feasibility](../../projects/cva/landing-page.html)** — monochrome architectural editorial (Fahkwang + Poppins, read off their live site). Offer = free 30-minute Site & Feasibility Chat. Carries a deliberate qualifying block with a project minimum for Cameron to set.
- **[10x lead capture](../../projects/10x-leadgen/landing-page.html)** — brand blue `#61a8d8`, Montserrat/Poppins. Offer = **Listing Film Test Drive**: one property, one film, fixed price, 72 hours. Three-field form. Turns a retainer decision into a trial.

## Blocked on people, not on work

- **Matt** — plumbing route (sub/partner vs electrical-only) + confirmed rebate and price figures. Gates the whole hot water campaign.
- **Cameron** — approve the feasibility offer, set the project minimum, release the June stills/clips as ad creative.
- **Hunter** — test-drive price, whether 72-hour turnaround is always deliverable, and which contact details 10x uses (the live site shows `tyson@`, the new page uses Hunter's number).
- **Every ad budget needs Hunter's explicit go-ahead.** Same money rule as credits.

## Standing lessons this produced

- A shipped page is not a shipped spec. Re-read the live markup after someone else rebuilds it — that is how six required fields got back onto two landing pages.
- Nested `<!-- -->` inside an HTML comment terminates it early and leaks dev notes onto the page. Caught on the hot water build by looking at the render, not the source.
- Track `tel:` clicks as the primary conversion on phone-first pages. Optimising toward form submits on a page designed to generate calls tells Google Ads to chase the weaker action.

## Related

- [[mvx-electrical]] · [[cva-architects]] · [[strategic-investing-qld]] · [[lead-gen-and-sales]]
- Session run sheet: [RUN-SHEET.md](../../projects/lead-audit-2026-07-28/RUN-SHEET.md)
- Dead campaign post-mortem: [fb-ads-handoff.md](../../projects/fb-ads-handoff.md)
