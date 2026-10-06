---
type: client
tags: [web-client, website, gym, oslo, pre-launch]
status: Six-page website built 22 Sep 2026 against the approved strategy doc, in projects/ironstandard-site/, pushed to main. The waitlist scope is dead: the strategy removes it entirely and makes an enquiry the primary action. Outstanding before launch = enquiry endpoint deployment, Anthony's founder copy, legal copy, real photography.
updated: 2026-10-07
---

# Iron Standard

Anthony McCoy (anthonygmccoy@gmail.com, +47 41369929), a competitive powerlifter, is opening **Iron Standard**: an 800m² purpose-built strength and performance training facility in Oslo, Norway. Positioned between budget chains (SATS, EVO, Pumphouse) and small niche gyms: proper platforms, calibrated plates, a posing room, 24/7 access, plus on-site coaching and physiotherapy. Engagement has run through three scopes — single-page waitlist (2 Sep), 7-page site with waitlist (16 Sep), and the current six-page enquiry-led site (22 Sep).

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

## Waitlist era, Sept 2026 — **⚠️ superseded 22 Sep 2026**

The 2–16 Sep work built a waitlist page, then a 7-page site around it, in
[projects/ironstandard-lp/](../../projects/ironstandard-lp/). The approved strategy
document kills the waitlist entirely, so that build is history, not the current site.
It is kept intact and untouched for reference. Durable learnings from it:

- **Never put an ESP API key in public-facing JS.** The first pass POSTed to Brevo's
  contacts API with the key in page source. Corrected to the vendor's hosted-form
  endpoint, which needs no client-side credential.
- **Anthony wants detail, not mystery.** The 2 Sep build stripped the page to hero plus
  form; his own instruction was the opposite, that people need enough detail to want to
  sign up. Specific converts, vague does not. That still holds on the new site.
- **Accent colour was contested and settled.** Gold, steel blue, bronze, olive, emerald
  and forest green were all tested live against the built page after Anthony flagged that
  SATS also brands in orange. None beat the brand orange, so `#F4502A` stayed and the
  SATS overlap is accepted rather than forced away. Do not reopen this.
- **A `position: fixed` hero backdrop paints over everything below it.** Content after it
  needs an opaque wrapper or the layout appears to break.
- A known shipped bug in that build's Apps Script is now fixed in the new one. See below.

### The 7-page expansion (16 Sep 2026), also superseded

Anthony's 16 Sep email replaced the single-page waitlist scope with a full 7-page brief, content direction included, and settled two standing questions from the 2 Sep build: **Google Sheets replaces Brevo** for form storage, and **10x hosts** the site instead of Anthony's own Netlify account. Spec: [2026-09-16 design](../../docs/superpowers/specs/2026-09-16-ironstandard-full-site-design.md), superseding the [2026-09-02 design](../../docs/superpowers/specs/2026-09-02-ironstandard-landing-page-design.md). Plan: [2026-09-16 implementation](../../docs/superpowers/plans/2026-09-16-ironstandard-full-site.md). Wireframe (all 7 pages, colour-keyed ready/pending): `docs/superpowers/specs/2026-09-15-ironstandard-wireframes.html`.

Executed via `superpowers:subagent-driven-development` — a fresh implementer subagent per task, a task-scoped reviewer after each, and a final whole-branch review at the end — directly on `main` (no worktree; Hunter chose that over an isolated branch since this is a solo repo and git is cheap to revert). All 10 tasks landed clean:

1. Site-wide nav bar + a semantic z-index scale (`--z-nav`, `--z-intro`), hand-duplicated into every page per the project's existing "copy, not include" pattern (`partials/footer.html`'s own precedent).
2. Intro flash-and-logo sequence gated to once per browser session (`sessionStorage`), not once per page load — a real requirement from the original wireframe round that never made it into the written spec, caught by the plan's own self-review before six more pages could inherit the replay bug.
3. Home reworked: new hero line ("Built by discipline. Driven by community."), a positioning paragraph placing Iron Standard between big commercial chains and inaccessible niche gyms, and the CTA/scroll-arrow retargeted from a dead `#form` anchor (a real live bug since 11 Sep) to the new `waitlist.html`.
4. **About Us** (new) — founder story: ten years coaching, three-time national athlete, SATS Fagerborg background, and strategic advisor Thomas Lilley of Zero Weakness (eleven locations across Australia/NZ/Europe). Narrative is placeholder copy built only from Anthony's own cleared facts; he's writing the final version himself.
5. **The Facility** (new) — 800m² central Oslo, equipment partners Zero Weakness and Texas Power Bars, posing room, 24/7 access, built for powerlifting/bodybuilding/street lifting/hyrox/general serious lifters. Uses the two existing client stills; more photography follows once the fit-out begins.
6. **Coaching** (new) — online/nutrition programming at scale, independent PTs with their own client bases (a marketplace model, not staff), a hosted competitions/events calendar.
7. **FAQ** (new) — reuses Home's `<details>` accordion pattern standalone, 4 placeholder Q&As on the topics Anthony flagged (opening timeline, location, audience, founding membership) pending his real answers.
8. **Join the Waitlist** (new, the real conversion target) + the Google Apps Script backend. Forms POST via a hidden-iframe pattern (Apps Script Web Apps don't return CORS headers for `fetch()`) to a `doPost(e)` script bound to a Sheet Anthony owns, with a honeypot field and an email notification on every submission, writing to separate Waitlist/Contact tabs. Deployment is manual, inside Anthony's own Google account (`google-apps-script/README.md`) — cannot be scripted from outside it.
9. **Contact Us** (new) — reuses the waitlist page's form styling with zero changes plus a message textarea; no invented social links ("Social links are coming soon" instead) and no address block until one's confirmed (HTML-commented placeholder, not a visibly empty section).
10. README rewrite for the 7-page structure and the new data flow, including a live `curl` check that confirmed the two facility photos are no longer missing from the media library (a stale note from the 2 Sep build, deleted rather than carried forward).

**Final whole-branch review caught one real cross-task bug and fixed three more:** the Apps Script's `MailApp` notification call reads `Session.getActiveUser().getEmail()`, which returns empty for anonymous form submitters under the exact "Execute as: Me / Anyone" deployment config the project's own README instructs — so under real deployment, the notification email silently never fires while the visitor still sees a success message. This is baked into the plan's own literal code; **Hunter reviewed it and chose to ship as-is** rather than have it patched, so notifications are a known gap until someone (Anthony or a follow-up job) catches and fixes it post-deployment. Three other findings were fixed in the same pass: a mobile-nav accessibility bug (closed nav links stayed keyboard-focusable while visually off-screen, and the toggle button's `aria-label` never updated), missing Open Graph tags on all 6 inner pages (only Home had them, so sharing a `waitlist.html` link rendered as a bare image-less preview), and a fragile `sessionStorage` read in `main.js` that could have silently aborted the nav-toggle/scroll-reveal/form-submit bindings if session storage access ever threw. A narrow follow-on regression from the nav-accessibility fix (opening the mobile nav ignored `prefers-reduced-motion`, though closing still respected it) was caught in the fix wave's own re-review and closed with Hunter's go-ahead.

Also caught: `projects/ironstandard-lp/preview-local.html` is a stale 15 Sep standalone snapshot with the old dead `#form` links, sitting entirely outside this plan's scope — flagged as a separate cleanup job rather than folded into this build.

## Current site: six pages, enquiry-led (22 Sep 2026)

Built from the approved **Website Strategy & Creative Direction** (27pp, Sept 2026) plus the
**IRONSTNDRD Guidelines 2026**, both supplied by the client. Lives in
[projects/ironstandard-site/](../../projects/ironstandard-site/), pushed to `main`. The old
build is untouched beside it pending Hunter's call on retiring it.

**The strategy changed the job.** No waitlist anywhere, no pricing, no address, no opening
date, no named equipment brands or quantities, no competitor names. Six core pages — Home,
About Us, The Facility, Coaching, FAQ, Contact Us — with a single enquiry as the primary
action. Message order is fixed and must not be reordered: brand belief → market difference
→ proof → culture → support.

Positioning in one line: specialist enough for serious athletes, considered enough to
welcome anyone who trains with intent. Hero is *Built by discipline. Driven by community.*,
supported by *A different standard for serious training.*

Technique and the anti-template discipline behind the build are on [[premium-web-build]].
Iron-Standard-specific decisions:

- **Orange is rationed and never a label colour on white.** `#F4502A` on white is 3.48:1
  and fails WCAG AA; black on orange is 6.03:1 and passes, so every orange button carries a
  black label. This is why the site is dark by default: it is the condition where the brand
  accent is both strongest and compliant. The client's own strategy document states this.
- **The Facility page separates confirmed from planned** with an outlined chip system,
  because the facility is not built and presenting proposals as finished creates liability.
- **Contact routes seven enquiry types to different recipients** so trainer and partnership
  leads never land in the member inbox.
- **⚠️ Numbered section marks and per-section eyebrows: kept, deliberately.**
  `01 / The position` style marks and wide-tracked caps labels sit above every
  section. Both are banned by the impeccable skill's absolute bans and by 10x's own
  [[premium-web-build]] and DESIGN.md (the No-Numbers and No-Eyebrow rules), and 10x
  stripped exactly this pattern from its own homepage in July 2026 on the grounds that
  the numbered-eyebrow combination is the most saturated AI landing-page pattern of
  2026. The approved Iron Standard strategy explicitly instructs it, borrowed from the
  client's own print guidelines. **Hunter's call, 22 Sep 2026: keep it.** Do not strip
  these in a future polish or audit pass without going back to the client first.
- **Imagery is all placeholder.** Extracted from the moodboard inside the brand guidelines
  PDF, so it is on-brand and approved in spirit, but low resolution (588px at widest) since
  those images were cropped for print layout. The named Desktop asset folder the brief
  pointed at did not exist. Everything gets replaced by the real shoot.
- Men and women appear in equal numbers and with equal seriousness. Stated brand principle,
  not a preference.

**Enquiry backend rewritten.** See [[premium-web-build]] and
`projects/ironstandard-site/google-apps-script/` — this fixes the silent notification
failure that the 16 Sep build knowingly shipped.

## Strategy compliance pass (29 Sep 2026)

Walked the approved strategy doc page by page against the shipped site. Most of it held; five
gaps did not, all fixed:

- **Home primary action** was the enquiry. Strategy p19 sets it as *Explore the Facility*;
  enquiry stays in the header and the page close. Hero buttons swapped.
- **Founder credentials were invented.** "Competitive powerlifter", "a decade of coaching",
  "national-level competition" and "operators who have built facilities internationally"
  appear nowhere in the strategy or guidelines. **⚠️ contradicts item 2 below**, which said
  the page carried placeholders, not invented copy. Replaced with the strategy's own pillar-05
  wording and a pending note naming Anthony McCoy's credentials and Thomas Lilley's
  advisory role as client-supplied.
- **Coaching was missing** online programming, nutrition and events, which p19 says must be
  separated. Added as a light index section (events labelled Planned), plus a reusable
  `<template id="coachProfile">` so coach profiles drop in without a redesign.
- **FAQ** now has a category index and an id on every answer; a link to one opens it.
  "Central Oslo" softened to "Oslo" since the location is unapproved.
- **Journeys** (p18): Coaching links to `contact.html?type=coaching|trainer|physiotherapy`,
  which preselects the route.

## Unified photo grade (7 Oct 2026)

Every photograph now runs through one `--grade` token: warm monochrome
(`grayscale(1) sepia(.14) contrast(1.12) brightness(.9)`). The stand-in stock came from many
sources (purple kit, green light, orange racks) and the mismatch was a big part of the
"template" read. One grade makes it one shoot and leaves orange to the buttons alone. Swap the
token back to a light correction once the real shoot is graded. Also replaced the facility pull
quote "Orange is the accent, never the whole room" (internal guideline language leaking into
visitor copy) with the strategy's own "clean, engineered and tactile" wording.

**Equipment brands in photos are fine (Hunter, 7 Oct 2026).** ELEIKO legible on the hero plates
is not a problem: it's a gym, and equipment carries its maker's name. The strategy's "no named
equipment brands" rule applies to copy claims, not to what's printed on plates in a photo. Stop
flagging it. Another *gym's* branding in a photo (e.g. "mk healthhub" on dumbbells in
`detail-b.jpg`) is a different case: it can read as borrowing another facility's photos. Replaced 7 Oct 2026 with an unused, unbranded bench frame from the guideline moodboard (`trainers.jpg`).

## Open items before go-live

1. **Deploy the enquiry handler** in the client's Google account and paste the Web App URL
   into `contact.html`. The form is deliberately inert until then and tells the visitor so,
   rather than appearing to send and discarding the enquiry.
2. **Anthony still owes** the founder narrative, his real credentials and the advisory
   relationship. Shipped as visible placeholder notes on the page, not invented copy.
   Naming SATS Fagerborg as his background is a problem the strategy created for itself:
   the site is not allowed to name competitors, so his history needs rewording.
3. **Legal copy** for the four footer stubs, which need actual legal review.
4. **Real photography.** Every image is a low-resolution stand-in.
5. **Restore the location block** in `contact.html` (currently commented out) once the
   address is approved for publication.
6. **Language decision still open** — English, Norwegian or bilingual. The strategy says
   this must be settled before content production because it changes navigation, search
   visibility and form consent, and retrofitting means rebuilding the structure.
7. **Retire or keep `projects/ironstandard-lp/`?** It still contains the waitlist the
   strategy kills. Undecided.
8. **Hosting / go-live.** ⚠️ The live `ironstandard.no` coming-soon page (checked 29 Sep) is
   **WordPress 7.1 + Elementor** on a host at 110.232.143.108, DNS at GoDaddy
   (domaincontrol.com), not the Netlify LP described above. The six-page site is
   launch-packaged (favicon reused from the live site, canonical tags, 404, robots, sitemap,
   `netlify.toml` and `.htaccess`) as `Desktop/10xVisuals Output/Iron Standard - Website (upload).zip`.
   Either upload into that host's `public_html` (back up WordPress first) or deploy to Netlify
   and repoint the GoDaddy A record. Needs whoever holds the host login.
