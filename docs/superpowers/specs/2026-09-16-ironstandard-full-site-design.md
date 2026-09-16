# Iron Standard — Full Pre-Launch Site (Design Spec)

**Client:** Iron Standard (Anthony McCoy), Oslo — premium strength/performance gym, 800m², pre-launch.
**Goal:** Expand the single-page waitlist build into the 7-page site Anthony specified on 16 Sep 2026, using his own content direction throughout. Still pre-launch: no membership sign-up, no payment, no booking.
**Supersedes:** [2026-09-02-ironstandard-landing-page-design.md](2026-09-02-ironstandard-landing-page-design.md) (single-page scope). That page's visual system, brand rules, and photography direction all carry forward unchanged — this spec only extends structure and content.
**Companion artifact:** the block-level wireframe (all 7 pages, colour-coded ready/pending) is published as an Artifact and kept in sync at `docs/superpowers/specs/2026-09-15-ironstandard-wireframes.html`. This document is the prose version of the same plan, plus the parts a wireframe can't carry (data flow, hosting, open questions).

## What changed and why

Anthony's 16 Sep email did three things at once:
1. Specified all 7 pages with a purpose and content direction for each.
2. Supplied real content for About Us and The Facility that didn't exist before — founder background, the Thomas Lilley/Zero Weakness credibility, named equipment partners, the widened athlete audience (powerlifting/bodybuilding/street lifting/hyrox).
3. Replaced two standing assumptions: **Brevo → Google Sheets** for form storage, and **Netlify → 10x hosting** for the domain.

Point 2 is the reason a 7-page site is now the right call. The 11 Sep audit of this project (informal, in-session) had concluded a 4th page (About) would be padding, because the only fact on hand was "founded by a competitive powerlifter." Anthony has since supplied a full paragraph of verifiable background plus a named strategic advisor — that's the strongest asset on the whole site, and it was sitting unused. Nothing here contradicts that earlier read; the input changed.

## Page structure

Seven pages, static HTML, one shared stylesheet and script (extending `projects/ironstandard-lp/`, not a new project). Menu appears on every page: wordmark, links to the other six, waitlist button.

### 1. Home (`index.html`) — rework, not rebuild
- **Purpose:** brand tone on contact, name the gap, drive to waitlist.
- **Hero line replaces the current headline:** *"Built by discipline. Driven by community."*
- **Positioning paragraph:** between big commercial chains (built for volume, not for people who train hard) and niche strength gyms (great equipment, inaccessible to a broader crowd).
- Existing 4-item "What you're getting" dropdown stays, retargeted to link into the new pages instead of standing alone.
- Waitlist CTA, unchanged mechanism, new destination (see Data flow).

### 2. About Us (`about.html`) — new
- **Purpose:** founder story, why this exists.
- **Anthony is writing the narrative copy himself** and sending it through. Structure is built ahead of that copy landing:
  - Ten years coaching athletes, beginner to national level
  - Three-time national athlete himself
  - Sports Management background
  - Worked inside SATS Fagerborg, Oslo — saw the gap directly
  - Oslo has some of the highest gym participation rates in the world, and almost nothing built for people who train seriously
  - **Thomas Lilley**, strategic advisor, founder of **Zero Weakness** — eleven locations across Australia, New Zealand and Europe. Iron Standard localises that proven model to Oslo.
- This page is built and shipped with placeholder narrative copy in the exact structure above; swapping in Anthony's final words is a content-only change, not a rebuild.

### 3. The Facility (`facility.html`) — new
- **Purpose:** what the space offers.
- 800 m², central Oslo (first time an area, not just a city, can be named).
- Competition-grade platforms and racks; specialist strength equipment to the same spec as equipment partners.
- **Equipment partners named:** Zero Weakness, Texas Power Bars.
- Posing room. 24/7 member access.
- Built for a broad range of serious training, explicitly not one discipline: powerlifting, bodybuilding, street lifting, hyrox, general serious lifters.
- **Imagery gap:** Anthony's photos/renders follow once the fit-out begins. Ships with the two client-supplied stills already in hand (the selective-colour equipment floor, the posing room) plus stock, clearly not the final asset set. Flagged in-repo so nobody mistakes placeholder for final.

### 4. Coaching (`coaching.html`) — new
- **Purpose:** what sets the coaching model apart.
- Online and nutrition programming delivered at scale.
- Independent PTs operating out of the facility with their own client bases (not staff — a marketplace model, worth being precise about in copy).
- A hosted calendar of competitions and events — the community argument, not just a room to lift alone in.

### 5. Join the Waitlist (`waitlist.html`) — new, primary conversion target
- **Purpose:** the actual goal of the launch site. Every other page's CTA points here.
- Founding-member framing: early access, a temporary discounted rate, capped and first-come — **Anthony is workshopping the exact offer wording himself.**
- Structure ships ahead of his final copy, same pattern as About Us: the shape is built, his words drop in without a rebuild.
- **The form itself is the one functional dependency the whole site sits on.** See Data flow below — nothing is collected anywhere until this exists.

### 6. FAQ (`faq.html`) — new
- **Purpose:** pre-empt repeat questions.
- **Anthony is sending specific Q&As.** Expected topics: opening timeline, location, who it's for, how founding membership works.
- Built as an accordion (same `<details>` pattern as Home's existing section) with 4 placeholder Q&A slots matching the expected topics, ready for his real answers.

### 7. Contact Us (`contact.html`) — new
- **Purpose:** a contact point that isn't the waitlist.
- Contact form (separate from the waitlist form — see Data flow), email, social links.
- **No physical address yet.** Location isn't locked in. Address block is built into the layout but left empty/hidden, so switching it on later is a content change, not a layout change.

## Visual system

Unchanged from the 2 Sep spec: black/near-black ground, single accent `#F4502A`, TASA Orbiter throughout, dark warm-toned photography with thin orange rim-light, motion-and-expression-mixed people photography, equipment shots without faces. Nothing here revises brand, palette, or type.

**One addition:** a persistent nav bar. The single-page build never needed one — `.site-header` exists in the markup today but sits empty. It becomes real: wordmark, 6 links, waitlist button. Transparent over a hero, solid on scroll or on inner pages that have no hero. Full-screen overlay on mobile.

## Data flow — two changes from the 2 Sep spec

### Google Sheets replaces Brevo

Anthony confirmed he's going with a Google Sheet for form submissions. This replaces the Brevo hosted-form pattern from the 2 Sep spec entirely — there is no Brevo integration in this build.

**Mechanism:** a Google Apps Script deployed as a Web App, bound to a Sheet Anthony owns. The static form POSTs to the Apps Script URL; the script appends a row and returns a response. No credential lives in the page's own JavaScript — the Apps Script URL is a public endpoint by design (that's how Apps Script Web Apps work), not a secret, so this doesn't reintroduce the API-key exposure problem the 2 Sep build explicitly avoided.

**Two things a bare form-to-sheet setup will not do on its own, and needs to:**
1. **Spam.** An open POST endpoint on the public internet gets bot traffic. Needs at minimum a honeypot field (invisible to humans, bots fill it, script silently drops the submission) and ideally a lightweight rate limit in the script itself. No reCAPTCHA in v1 — adds a UI dependency for a marginal gain over a honeypot at this traffic scale.
2. **Notification.** A spreadsheet nobody's watching is a leak, not a list. The Apps Script sends Anthony an email on every new row (Apps Script's own `MailApp`, no separate service needed).

**Two sheets, one spreadsheet, two tabs:** waitlist submissions and contact-form submissions write to separate tabs of the same Google Sheet, so a "just reaching out" enquiry never pollutes the waitlist count Anthony is tracking.

**Anthony owns the Sheet and the Apps Script project** — under his own Google account, not 10x's. He can view, export, or filter it himself with no dependency on 10x staying involved. This is a meaningfully different ownership model from the Brevo plan, where 10x's Brevo account held the list; worth being explicit with Anthony that this is *his* asset from day one.

### Hosting moves to 10x

Anthony asked 10x to host, replacing the 2 Sep spec's Netlify-under-Anthony's-control plan. Domain stays at GoDaddy as registrar (unchanged); DNS gets pointed at wherever 10x hosts static sites. This is a real ongoing commitment, not a one-time deploy — 10x is now responsible for uptime on a site collecting real leads. Confirm with Hunter which of 10x's existing hosting arrangements this lands on before build.

**Not resolved in this spec, needs Hunter's decision before the Data flow section can be built:** the specific hosting target (existing 10x infrastructure vs. a new Netlify/Vercel account under 10x's org). Doesn't block building the 7 pages themselves, which are static regardless of where they end up served from.

## What's explicitly not in this build

- Membership sign-up, booking, payment — later, separately-spec'd work, unchanged from the 2 Sep scope line.
- Pricing figures, opening date, exact address — none of Anthony's cleared content includes these; nothing on any of the 7 pages states them.
- A working waitlist or contact form on day one of this build — both are built to the point of "submits to the Apps Script endpoint" but cannot go live until Anthony's Sheet and Apps Script deployment exist. Every CTA on the site is inert until then, same caveat that applied to the single-page build's `#waitlist` anchor.

## Open items to confirm before/during build

1. **Hosting target** — which 10x-controlled hosting this points at (blocks only the final DNS cutover step, not page-building).
2. **About Us / Waitlist / FAQ final copy** — Anthony is writing/workshopping/sending these three. Pages ship with structurally-accurate placeholder copy in the meantime; swapping in his final words is a content edit, not a rebuild.
3. **Facility photography** — stock + the 2 client stills stand in until his fit-out photos/renders exist.
4. **Social account links** — needed for Contact; not yet supplied.
5. **Spam/notification approach for the Apps Script** — honeypot + email-on-submit is the v1 plan above; flag to Anthony/Hunter before build in case there's a stronger preference.
