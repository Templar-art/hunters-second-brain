---
type: client
tags: [web-client, landing-page, gym, oslo, pre-launch]
status: full content + FOMO copy restored, accent switched to gold 8 Sep 2026 — Brevo/DNS handoff steps are the only things left before go-live
updated: 2026-09-08
---

# Iron Standard

Anthony McCoy (anthonygmccoy@gmail.com, +47 41369929), a competitive powerlifter, is opening **Iron Standard**: an 800m² purpose-built strength and performance training facility in Oslo, Norway. Positioned between budget chains (SATS, EVO, Pumphouse) and small niche gyms — proper platforms, calibrated plates, a posing room, 24/7 access, plus on-site coaching and physiotherapy. Full site with membership sign-up and booking is a later, separate build; this engagement is the pre-launch waitlist page only.

Existing site `ironstandard.no` is GoDaddy's free Website Builder "Launching Soon" placeholder — Anthony doesn't manage separate hosting beyond that ("Need help with this" on the intake form), so the domain stays at GoDaddy as registrar while hosting moves elsewhere.

Not to be confused with [[anthony]] (a different, unrelated lead named Anthony — Hattie Boydle's podcast proposal).

## Brand

Real guidelines: `raw/` doesn't hold a copy yet — sourced directly from the PDF the client sent (`260831_IRONSTNDRD-Guidelines.pdf`), not from the earlier auto-fetched summary of the intake-form URL, which turned out to be thin/wrong. Wordmark **IRONSTNDRD.** in **TASA Orbiter** (free on Google Fonts — confirmed via search, no licensing cost). Photography direction, in the brand's own words: "balance between grit, strength & a subtle elegance," motion over static posing, mixed smiles/serious expressions, equipment shots avoid faces. Reference sites: Equinox (target tier), ironforgegymtx (authenticity, too "gym bro"), EBT/Gymshark (inclusive strength for both genders — the balance Anthony wants). Direct Oslo competitors to visibly outclass: SATS, EVO, Pumphouse — bright/busy/promo-driven, the opposite of this build.

**Accent colour changed 8 Sep 2026: `#F4502A` (orange) → `#C9A227` (gold/amber).** The guidelines' original palette was black + white + orange as an accent ("doesn't over-saturate the environment," also the colour of their equipment/lighting) — but Anthony flagged that SATS, the exact competitor this build outclasses, also brands in orange, and explicitly deferred the choice ("happy for you guys to play around with whatever you think is best"). Tested live against the actual built page: steel blue (`#4A7A96`, read too tech/SaaS), bronze (`#B5651D`, still too close to orange), olive green (`#4A6B3A`, tactical but muted/surplus-y), emerald (`#2E6B4A`, leaned corporate). Gold won — visually distinct from SATS (navy/red), EVO (magenta), and Pumphouse, and the "gold tier" association reinforces the founding-member/exclusivity framing below. Single CSS custom property (`--accent` in `assets/css/style.css`), so it was a one-line change once decided.

## Landing page build (2 Sep 2026)

Static single-page site: [projects/ironstandard-lp/](../../projects/ironstandard-lp/). Spec: [2026-09-02 design](../../docs/superpowers/specs/2026-09-02-ironstandard-landing-page-design.md). Plan: [2026-09-02 implementation](../../docs/superpowers/plans/2026-09-02-ironstandard-landing-page.md).

**Structure (as of 8 Sep):** hero (video reel + intro animation + waitlist CTA + scroll arrow) → What-it-is → Who's-it-for → What's-different (4 pillars) → Founding-member (FOMO) → waitlist form → footer. This restores sections Hunter had cut on 2 Sep in favour of a bare hero+waitlist page ("landing page asap, just collect emails") — Anthony's actual direction was the opposite (see feedback below), so the fuller structure is back, with copy limited to what he's actually cleared to say. Hero kicker still reads "Coming soon" rather than a specific date — that part was never in tension with his feedback.

- **Email capture → Brevo** (free tier, no contact-cap, created under Hunter's 10x Brevo account as a separate "Iron Standard Waitlist" list — not a new Brevo account). This is the list Anthony shows investors, exportable to CSV anytime.
- **Security fix mid-build:** the first pass wired the waitlist form to POST directly to Brevo's contacts API with an API key inside the page's own JavaScript — that would have exposed the key to anyone viewing source. Corrected to a plain HTML form posting straight to Brevo's hosted Forms endpoint, which needs no client-side credential at all. Worth remembering for any future client site with an ESP integration: never put an API key in public-facing JS: use the vendor's hosted-form pattern instead.
- **Hosting:** Netlify (free), DNS repointed from GoDaddy (registrar stays GoDaddy).
- **Hero:** rotates through 4 clips of Hunter's own licensed 4K footage (`/Volumes/10X SSD3/Videos for Website/`, from a larger 7-clip batch — 3 were cut as off-brand/generic), transcoded to web weight. Opens on a woman deadlifting, includes a mixed-gender coaching/spotting shot — answers the brand's "not male-only, equal seriousness at real loads" brief with real footage rather than stock, after Pexels/Adobe Stock searches for that specific look came up short.
- **Intro animation:** ~10 B&W still-frame flash (Freepik stock, chalk/barbell/silhouette imagery, 70ms/frame) → instant white flash (occludes the logo, which spawns underneath it) → veil recedes to black, revealing the logo purely through the backdrop contrast change → hold ~1.3s so it registers → logo drags (computed FLIP transform) into its exact on-page position → crossfades into the real logo already there. Iterated several times on user feedback (subtlety, double-logo-visible bug, pacing).
- Copy written from scratch throughout — client had none ready — rewritten again 8 Sep to match Anthony's real feedback (see below) rather than the placeholder version from the 2 Sep build.
- Intro flash also carries a persistent "Coming soon" caption overlaid on the photos, and the caption/flash images are B&W stock chosen to match — bold text card variant was tried and dropped as redundant once the overlay landed.

## Client feedback (8 Sep 2026, email to Lachlan) — actioned same day

Anthony sent real messaging direction plus a brand-colour flag, both now built.

**Contradicted the 2 Sep build's minimal direction, resolved in Anthony's favour.** The 2 Sep build had stripped the page to hero + waitlist only. Anthony's actual instruction was the opposite: *"the point of this page is to build a waiting list before we open, so people need enough detail to actually want to sign up"* — vague doesn't convert, specific does. Full content restored (see structure above), copy limited to exactly what he cleared: premium strength/performance facility opening in Oslo, ~800m² purpose-built with 24/7 access, top-tier equipment and a posing room, on-site coaching/PT/physio, for people who train seriously whether or not they compete. Location, opening date, and pricing still aren't said anywhere — an explicit line in the What-it-is section says those are still being finalised and will be shared here first.

**FOMO/scarcity mechanic — new copy, now live in its own Founding-member section and folded into the waitlist subhead:** founding-member benefits + priority access (never the actual discount figure — Anthony hasn't finalised numbers), first-come-first-served with unclaimed offers passed to the next person on the list, and capped total membership spots.

**Brand colour resolved:** `#F4502A` → `#C9A227` gold, see Brand section above for the comparison process.

## Open items before go-live

1. Fill in the real Brevo Forms action URL + hidden field names in `index.html` (placeholders left in place, exact steps in the project's `README.md`).
2. Export any leads already sitting in the current GoDaddy Website Builder form before retiring it.
3. Send Anthony the updated build for sign-off on the restored copy + gold accent before pointing DNS at it.
