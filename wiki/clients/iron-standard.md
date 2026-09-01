---
type: client
tags: [web-client, landing-page, gym, oslo, pre-launch]
status: landing page built 2 Sep 2026, awaiting Brevo/Netlify/DNS handoff steps
updated: 2026-09-02
---

# Iron Standard

Anthony McCoy (anthonygmccoy@gmail.com, +47 41369929), a competitive powerlifter, is opening **Iron Standard**: an 800m² purpose-built strength and performance training facility in Oslo, Norway. Positioned between budget chains (SATS, EVO, Pumphouse) and small niche gyms — proper platforms, calibrated plates, a posing room, 24/7 access, plus on-site coaching and physiotherapy. Full site with membership sign-up and booking is a later, separate build; this engagement is the pre-launch waitlist page only.

Existing site `ironstandard.no` is GoDaddy's free Website Builder "Launching Soon" placeholder — Anthony doesn't manage separate hosting beyond that ("Need help with this" on the intake form), so the domain stays at GoDaddy as registrar while hosting moves elsewhere.

Not to be confused with [[anthony]] (a different, unrelated lead named Anthony — Hattie Boydle's podcast proposal).

## Brand

Real guidelines: `raw/` doesn't hold a copy yet — sourced directly from the PDF the client sent (`260831_IRONSTNDRD-Guidelines.pdf`), not from the earlier auto-fetched summary of the intake-form URL, which turned out to be thin/wrong. Wordmark **IRONSTNDRD.** in **TASA Orbiter** (free on Google Fonts — confirmed via search, no licensing cost). Palette: black + white + one accent orange `#F4502A`, explicitly meant as an accent only ("doesn't over-saturate the environment," also the colour of their own equipment/lighting). Photography direction, in the brand's own words: "balance between grit, strength & a subtle elegance," motion over static posing, mixed smiles/serious expressions, equipment shots avoid faces. Reference sites: Equinox (target tier), ironforgegymtx (authenticity, too "gym bro"), EBT/Gymshark (inclusive strength for both genders — the balance Anthony wants). Direct Oslo competitors to visibly outclass: SATS, EVO, Pumphouse — bright/busy/promo-driven, the opposite of this build.

## Landing page build (2 Sep 2026)

Static single-page site: [projects/ironstandard-lp/](../../projects/ironstandard-lp/). Spec: [2026-09-02 design](../../docs/superpowers/specs/2026-09-02-ironstandard-landing-page-design.md). Plan: [2026-09-02 implementation](../../docs/superpowers/plans/2026-09-02-ironstandard-landing-page.md).

- **Email capture → Brevo** (free tier, no contact-cap, created under Hunter's 10x Brevo account as a separate "Iron Standard Waitlist" list — not a new Brevo account). This is the list Anthony shows investors, exportable to CSV anytime.
- **Security fix mid-build:** the first pass wired the waitlist form to POST directly to Brevo's contacts API with an API key inside the page's own JavaScript — that would have exposed the key to anyone viewing source. Corrected to a plain HTML form posting straight to Brevo's hosted Forms endpoint, which needs no client-side credential at all. Worth remembering for any future client site with an ESP integration: never put an API key in public-facing JS: use the vendor's hosted-form pattern instead.
- **Hosting:** Netlify (free), DNS repointed from GoDaddy (registrar stays GoDaddy).
- **Hero:** looping video reel (free-license Pexels clip of a woman deadlifting, warm/dark industrial gym, chosen deliberately to open on a woman per the brand's "not male-only" brief) under the wordmark load-in animation. A second, heavier-load male clip was wanted as a crossfade, but neither Pexels (outdoor/light-weight/generic-CrossFit only) nor Adobe Stock had the heavy indoor powerlifting look. Best remaining option, per README: real footage of Anthony himself lifting — he's a competitive powerlifter, so it's both on-brand and solves the "real weight, real emotion" ask better than stock ever will.
- **Imagery gap:** the "who it's for" section shipped text-only — same pattern as the male hero clip, this niche's stock libraries (free and paid) skew bright/commercial/outdoor rather than dark serious-training. Real photography is the actual fix, not more stock searching.
- Copy (all sections) written from scratch — client had none ready.

## Open items before go-live

1. Fill in the real Brevo Forms action URL + hidden field names in `index.html` (placeholders left in place, exact steps in the project's `README.md`).
2. Export any leads already sitting in the current GoDaddy Website Builder form before retiring it.
3. Confirm real opening date (placeholder "Opening 2027" in the hero).
4. "Who it's for" section imagery.
