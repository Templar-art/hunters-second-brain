---
type: client
tags: [web-client, landing-page, gym, oslo, pre-launch]
status: UI/UX polish pass + full /impeccable audit cleared 10 Sep 2026 (interactive details section, scroll reveals, faster intro, waitlist form pulled pending Brevo, footer partial split out, image/a11y/fallback/token fixes) — Brevo/DNS handoff steps are the only things left before go-live
updated: 2026-09-10
---

# Iron Standard

Anthony McCoy (anthonygmccoy@gmail.com, +47 41369929), a competitive powerlifter, is opening **Iron Standard**: an 800m² purpose-built strength and performance training facility in Oslo, Norway. Positioned between budget chains (SATS, EVO, Pumphouse) and small niche gyms — proper platforms, calibrated plates, a posing room, 24/7 access, plus on-site coaching and physiotherapy. Full site with membership sign-up and booking is a later, separate build; this engagement is the pre-launch waitlist page only.

Existing site `ironstandard.no` is GoDaddy's free Website Builder "Launching Soon" placeholder — Anthony doesn't manage separate hosting beyond that ("Need help with this" on the intake form), so the domain stays at GoDaddy as registrar while hosting moves elsewhere.

Not to be confused with [[anthony]] (a different, unrelated lead named Anthony — Hattie Boydle's podcast proposal).

## Brand

Real guidelines: `raw/` doesn't hold a copy yet — sourced directly from the PDF the client sent (`260831_IRONSTNDRD-Guidelines.pdf`), not from the earlier auto-fetched summary of the intake-form URL, which turned out to be thin/wrong. Wordmark **IRONSTNDRD.** in **TASA Orbiter** (free on Google Fonts — confirmed via search, no licensing cost). Photography direction, in the brand's own words: "balance between grit, strength & a subtle elegance," motion over static posing, mixed smiles/serious expressions, equipment shots avoid faces. Reference sites: Equinox (target tier), ironforgegymtx (authenticity, too "gym bro"), EBT/Gymshark (inclusive strength for both genders — the balance Anthony wants). Direct Oslo competitors to visibly outclass: SATS, EVO, Pumphouse — bright/busy/promo-driven, the opposite of this build.

**Accent colour: tested alternatives 8 Sep 2026, landed back on the original `#F4502A` orange.** Anthony flagged that SATS, the exact competitor this build outclasses, also brands in orange, and deferred the choice to 10x's judgement. Tested live against the actual built page: steel blue (`#4A7A96`, too tech/SaaS), bronze (`#B5651D`, still read as orange), olive green (`#4A6B3A`, muted/surplus-y), emerald (`#2E6B4A`, corporate), gold (`#C9A227`, first pick — Hunter rejected it once seen live, read as "AI generated"), deep forest green (`#1B5E3F`, rejected — also read as an off-brand fix). None of the alternatives landed, so the call is to keep the original brand-guideline orange and accept the SATS overlap rather than force a swap nobody's happy with. Single CSS custom property (`--accent` in `assets/css/style.css`), so any future change stays a one-line edit.

## Landing page build (2 Sep 2026)

Static single-page site: [projects/ironstandard-lp/](../../projects/ironstandard-lp/). Spec: [2026-09-02 design](../../docs/superpowers/specs/2026-09-02-ironstandard-landing-page-design.md). Plan: [2026-09-02 implementation](../../docs/superpowers/plans/2026-09-02-ironstandard-landing-page.md).

**Structure (as of 8 Sep, condensed same day):** hero (video reel + intro animation + waitlist CTA + scroll arrow) → a single "More details" accordion (native `<details>`, one open by default) collapsing The facility / Who it's for / What's different / Founding members into short one-paragraph answers → waitlist form → footer. Originally these were 4 full prose sections; Hunter found that too long once built, so it's the same content, condensed and hidden behind click-to-expand rather than always-on scroll. Copy still limited to what Anthony's actually cleared to say. Hero kicker still reads "Coming soon" rather than a specific date. All em dashes removed from on-page copy per Hunter's request (replaced with periods/commas), though not from code comments.

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

**Brand colour tested, kept as-is:** tried gold, blue, bronze, olive, emerald, forest green against the built page — none beat the original orange, so it stayed `#F4502A` despite the SATS overlap. See Brand section above.

## UI/UX polish pass (10 Sep 2026)

Hunter reviewed the live build and asked for a round of polish, all actioned same day:

- **Intro logo-reveal held too long.** The "hold on black" beat before the logo drags into place was cut 35% (1300ms → 845ms in `assets/js/main.js`); the flash sequence and drag itself are unchanged.
- **The info section read flat.** Rebuilt "What you're getting" from a plain accordion into an interactive tab-and-image layout: each of the 4 items (facility, who it's for, what's different, founding members) now has a small line icon, an animated underline on hover/open, and on desktop a photo panel on the right that crossfades to match whichever item is open, pure CSS via `:has()`, no JS. Mobile shows the same photo inline above each item's copy instead of the side panel. Native `<details name="...">` groups them so opening one auto-closes the others.
- **Waitlist form removed for now.** Hunter wants to add the real thing back in manually once Brevo's set up, so the `<form>` (name/email fields + submit) was pulled from `#waitlist` in `index.html`, leaving the section heading/copy/background photo in place plus an HTML comment marking where to paste it back in. README's Brevo section updated to match.
- **Footer split into its own file.** `partials/footer.html` is a standalone, styled copy of the footer so it can be grabbed for another Iron Standard page without opening the full `index.html`. It's a copy, not a live include, editing one doesn't update the other.
- **General animate-in polish.** Added a scroll-reveal system (`data-reveal` + `IntersectionObserver` in `main.js`): sections fade/rise into place as they enter view, staggered across the 4 details items. Built so a no-JS load never hides content, the reveal class is only added at runtime right before observing.

## Open items before go-live

1. Fill in the real Brevo Forms action URL + hidden field names, then paste a `<form>` back into `#waitlist` in `index.html` (exact steps in the project's `README.md`).
2. Export any leads already sitting in the current GoDaddy Website Builder form before retiring it.
3. Send Anthony the updated build for sign-off on the restored copy + colour + this polish pass before pointing DNS at it.
