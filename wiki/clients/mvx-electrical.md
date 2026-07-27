---
type: client
tags: [client, web-design, electrical, gold-coast]
status: active
updated: 2026-07-27
---

# MVX Electrical

_10x web client — company context: [[overview]]._

Gold Coast + Northern NSW electrical contractor, owner **Matt**. 10x Visuals built their website (WordPress + Elementor, "Web Design by 10x Visuals" credit in footer). Phone 0427 593 990, [mvxelectrical.com.au](https://mvxelectrical.com.au).

**Brand:** volt green `#7EC004` + black, Poppins, white logo on dark. Blokey-straight copy voice ("Aircon packed it in?").

**Credentials:** NSW Contractor Licence 483405C · ARC Licence L198354 · Solar Accreditation S4837975 · ACRS Master Cabler A053105. 4.9★ Google.

**Services:** residential/commercial electrical, aircon (supply/install/repair/service), solar & battery, insurance works, NDIS/aged care, medical fitouts, aviation.

## Live ad landing pages (verified 27 Jul 2026)

Both 14 Jul builds **did go live** as dedicated Google Ads landing pages, separate from the site's service pages:
- [/air-conditioning-electrician-gold-coast/](https://mvxelectrical.com.au/air-conditioning-electrician-gold-coast/) — Formidable `form_id 2` (`air-con`)
- [/gold-coast-electricians/](https://mvxelectrical.com.au/gold-coast-electricians/) — Formidable `form_id 3` (`general-electrician`)

Design shipped to spec (message-matched H1, 7 tap-to-call, sticky call bar, licence strip, "one trade, one visit"). **⚠️ The form did not** — the Elementor/Formidable build re-added email + postcode as required and made the free-text message required, giving six required fields where the approved spec was four with email deleted. Site nav also still present on both (spec said strip it). Fix list: [FORM-FIX.md](../../projects/mvx-lead-fix/FORM-FIX.md). Lesson: a shipped page is not a shipped spec — re-read the live markup after someone else rebuilds it.

**⚠️ No hot water surface exists.** Checked the full 29-page sitemap: zero hot water / heat pump pages, nav items or mentions, including on both ad LPs. Matt wants to shift lead mix from aircon toward hot water electrical systems — there is currently nothing for ads to point at or Google to rank, so the absence of hot water leads is structural, not a performance problem. **Blocked:** MVX holds electrical/ARC/solar/cabler licences but no plumbing licence, and the water side of a HWS swap is licensed plumbing in QLD — need Matt's answer on subbing vs partnering a plumber before building the page or the campaign. Angle if it proceeds: heat pump attracts the federal STC rebate (~$998, applied as an upfront discount), and heat-pump/electric-storage work is genuinely electrician-led.

## Work

- **2026-07-27 — Ad landing page lead-capture fix (spec, unbuilt).** [FORM-FIX.md](../../projects/mvx-lead-fix/FORM-FIX.md): delete Email, relabel Postcode → Suburb, make the message optional (both forms) → back to the 4-field spec; strip site nav from both LPs; confirm `tel:` clicks fire as Google Ads conversions (phone-first page — the calls *are* the leads). Also caught a live bug: the electricians form's job-type validation still reads "How can we help with your **aircon**?" Needs WP admin access to apply; baseline the last 14 days of entries + call conversions first or the lift is unmeasurable.
- **2026-07-14 — Residential electricians landing page.** Same conversion system as the aircon page (League Gothic/Poppins brand build, phone-first, 2x2 services, ends at FAQ, Elementor-ready scoped CSS). Hero = Liversaver-14, blue-chip trust row replaces brands row. Deliverable: [landing-page.html](../../projects/mvx-electricians/landing-page.html) + shareable code note in same folder.
- **2026-07-14 — Aircon landing page conversion redesign.** Existing Google Ads landing page underperforming vs competitor [T42 Electrical](https://t42electrical.com.au/air-conditioning-installation-repair/). Rebuilt phone-first (11 tap-to-call CTAs, sticky mobile call bar, message-match H1, 4-field callback form moved to bottom, "we ARE the electricians — one trade, one visit" differentiator). Deliverable: [landing-page.html](../../projects/mvx-aircon/landing-page.html) + [CONVERSION-NOTES.md](../../projects/mvx-aircon/CONVERSION-NOTES.md) (incl. pre-launch checklist: confirm brands, call tracking, Formidable wiring).
