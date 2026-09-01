# Iron Standard — Waitlist Landing Page (Design Spec)

**Client:** Iron Standard (Anthony McCoy), Oslo — premium strength/performance gym, 800m², pre-launch.
**Goal:** Ship a landing page fast that (1) establishes the brand at a premium tier, clearly above SATS/EVO/Pumphouse, and (2) collects waitlist emails into a system Anthony can show investors as a live, exportable list — before doors open.
**Not in scope:** full site, membership sign-up/booking, payment/deposit collection. Those are a later, separately-spec'd build. This page just needs to make the case and capture interest.

## Context gathered

- Current site (`ironstandard.no`) is GoDaddy's free Website Builder "Launching Soon" placeholder with its own inline name/email form (opt-in checkbox, reCAPTCHA). **Likely already holds a handful of real signups.**
- Anthony answered "Need help with this" when asked where his hosting lives — read as: no separate paid hosting plan exists, GoDaddy Website Builder is genuinely all there is. Domain registration stays at GoDaddy regardless of where the site is hosted.
- Real brand guidelines (`260831_IRONSTNDRD-Guidelines.pdf`) reviewed directly (the earlier auto-fetch from the intake-form URL pulled thin/wrong content — don't trust that summary):
  - **Wordmark:** IRONSTNDRD., set in **TASA Orbiter** (regular = body, semi-bold = subtitles, bold = headlines, all caps for subtitle/headline use).
  - **Palette:** black + white + one accent orange, `R244 G80 B42` (`#F4502A`). Guideline text: *"can be used as accent color... is also the color of our machinery... Bright, bold and embodies the ethos of our brand."* Explicitly not a full-orange or oversaturated treatment.
  - **Photography direction (their own words):** *"balance between grit, strength & a subtle elegance"*; people **in motion, not overly posed**; *"smiles vs cold expressions, motion vs static poses, high/low vs perfectly straight-on"* — mix these, don't pick one extreme. Equipment photography: **faces avoided**, focus on machine cleanliness/quality.
  - **Environment/lighting direction:** dark, warm-toned spaces with **thin linear orange (or occasionally red) accent lighting** framing rigs/rooms — not general orange wash.
  - **Logo misuse rules to respect:** never rotate, recolour, restretch, add stroke/shadow, or alter the primary/secondary lockup spacing.
- Reference sites Anthony gave (Equinox, ironforgegymtx, EBT/Gymshark) point at: dark, cinematic, photography-led, uncluttered, both men and women shown training at real loads and shot the same way — never "gym bro," never soft/pastel wellness.
- Competitors to visibly out-class: SATS, EVO, Pumphouse — bright, busy, promo/price-driven. The opposite of all three, obvious within 3 seconds of landing.

## Approach

Single self-contained static page (`index.html` + `assets/`), no framework, no build step — same pattern as [10x's own site](../../../wiki/projects/10x-website.md). Deployed to Netlify (free tier) with `ironstandard.no`'s DNS repointed from GoDaddy; GoDaddy stays domain registrar only, Website Builder retired. Rejected: a no-code builder (Framer/Carrd) — would lock Anthony into a recurring paid tool and diverges from how every other 10x build is done (git-tracked static HTML). Rejected: standing up a framework (Vite/React) now — booking/membership is an explicitly later, separate project; building framework scaffolding for one static page today is pure overhead.

## Page structure

One long-scroll page:

1. **Hero.** Muted, looping stock video reel (chalk, plates, bar, silhouette lifting — warm dark grade with thin orange rim-light on equipment, matching the guideline's own environment photography) plays 3-5s, then dissolves to the IRONSTNDRD. wordmark, then the headline resolves in. Primary CTA scrolls to the waitlist form. Poster-image fallback for slow connections/reduced-motion.
2. **What it is.** 800m² Oslo facility, 24/7 access, platforms/calibrated plates/posing room, opening window (placeholder date, Anthony to confirm).
3. **Who it's for.** Serious lifters, coached athletes, self-employed PTs wanting a base. Confident, standards-led language — not aggression, not "gym bro."
4. **What's different.** 3-4 pillars: equipment & space built for real training / coaching, semi-private & on-site physiotherapy / a membership base training to the same standard / founder credibility (trains, coaches, knows the Oslo scene).
5. **Founding member hook.** Early sign-up = founding-member pricing/priority when doors open. Sets the expectation only — no payment collection in this build.
6. **Waitlist form.** Name + email, single clear CTA, posts to Brevo.
7. **Footer.** Wordmark, Oslo, contact, social placeholders.

Copy is a full first draft written in this build (client has no content ready) — voice: "strength and standards," never aggression, never gendered.

## Visual system

- Colours: black (`#000`/near-black background), white text, **one** accent orange `#F4502A` used sparingly — CTA button, link underline/hover, a hairline divider or two. Never a wash, never the dominant colour of a section.
- Type: TASA Orbiter throughout — bold caps for headlines, semi-bold caps for subtitles/kickers, regular (mixed case) for body.
- Imagery: stock photography, dark/warm grade, men and women shown at equal seriousness and real load, matching the guideline's motion/expression mix — not uniformly stern, not uniformly smiling.
- Load-in: wordmark fades/draws on over the already-rendered page (never gates content — see the standing rule below), sub-1s, respects the primary-lockup-only rule (no rotation/recolour).

**Standing rule carried over from [[10x-website]]:** never gate real page content behind a load animation or scroll-reveal script. The hero/logo animation plays over content that is already present in the DOM and visible without JS; it must fail safe (skip cleanly) on slow connections or JS errors.

## Data flow — where the emails go

**Brevo** (free tier, no contact cap, 300 emails/day free — won't force a plan change while the list is still growing pre-launch). Form posts client-side to Brevo's hosted form/API, no backend needed. Anthony gets:
- A live contact list in Brevo's dashboard, exportable to CSV any time — this is the artifact he shows investors.
- Built-in unsubscribe/compliance handling (relevant operating in Norway/EU).
- A clean upgrade path into actual pre-launch email campaigns later, same tool, same list.

**Before cutover:** export whatever's sitting in the current GoDaddy Website Builder form (if anything) and import it into Brevo, so no early signups are lost when the old site is retired.

## Deployment

- Host: Netlify, deployed from git (this repo's `projects/ironstandard-lp/`).
- Domain: `ironstandard.no` DNS (A/CNAME records) repointed from GoDaddy DNS management to Netlify. Registrar relationship with GoDaddy is untouched.
- Analytics: lightweight (Plausible or GA4) so Anthony can show investors traffic and conversion rate alongside raw signup count. Add if wanted — not a hard blocker for v1.
- Accounts Claude cannot create: Brevo signup, Netlify signup, GoDaddy DNS changes. Spec includes exact copy-paste setup steps for Anthony/Hunter to run themselves.

## Open items to confirm with Anthony before/at cutover

1. Export any existing GoDaddy-collected leads before retiring that site.
2. Confirm there truly is no separate paid GoDaddy hosting plan (his "need help with this" answer implies no, but worth one sentence of confirmation).
3. Opening-date placeholder in section 2 — needs a real value or an intentionally vague one ("Opening [season] 2027" etc.).
