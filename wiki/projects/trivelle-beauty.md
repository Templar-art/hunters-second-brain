---
type: project
tags: [trivelle, ecommerce, dropshipping, ads, side-business]
status: launching
updated: 2026-11-06
---

# Trivelle Beauty (trivellebeauty.com)

Hunter's own Shopify dropshipping store, separate from [[10x-visuals]] client work. One product: the **Trivelle 4-in-1 Sculpt & Glow**, a handheld body and face device (gentle heat, red light, EMS micro-pulses, vacuum massage), sold with an 80 g microcurrent gel. Working folder: [projects/trivelle-beauty](../../projects/trivelle-beauty/).

## Offer and economics
- Price **A$169** kit + gel subscription (from 2026-11-06; was A$219). Gift 2-pack dropped, too confusing. Value-anchor copy only, no fake "was" prices (ACCC reference-pricing risk).
- Supplier ships direct to AU in 7–15 days. Landed cost US$29.23 (~A$45) for device and gel, so ~A$170 margin per sale before ads.
- Launch test: one Meta Sales campaign, one ad set, **$20/day for 5 days**, four ads. Judge on cost per add-to-cart.
- Stock supplier box at launch. Custom carton (~A$900–1,000 for 500) only once sales are steady; draft dieline in `packaging/` is too plain and needs a redesign.

## What shipped (2026-11-04)
- **Ads** (`device-v2/ads/`): four long edits (34–60 s), 30 s cuts and a 10 s hook. AI UGC presenters (Seedance 2.5), Kling B-roll of the device on skin, real stock clips, ElevenLabs Australian VO, karaoke captions (white box, yellow active word), soft music bed. Built by `scripts/build_ads_v2.py`.
- **Store graphics** (`device-v2/graphics/`): eight 1080² images (kit hero, four rituals, how-to, gel card, where-to-use, comparison, in-the-box, guarantee), modelled on the category's standard product-page shot list but our own layouts and photos. `scripts/graphics_v3.py`.
- **Docs:** `LAUNCH-CHECKLIST.md` (full to-do), `STORE-COPY.md` (paste-ready copy and FAQ), `WEBSITE-BREAKDOWN.md` (site audit).

## Cost
Roughly 50k Magnific credits across two device versions (the 3-in-1 ads were made first, then fully redone for the 4-in-1 at ~19.7k), plus 50 Higgsfield credits lost to an nsfw block.

## Lessons
- **Product swaps are expensive.** Switching devices mid-build forced a near-complete redo of stills, B-roll and ads. Lock the product before generating.
- **Pricing claims drift.** "Under a dollar a session" was baked into voiceover at $169 and became false at $219; it had to be cut from the audio. Keep price maths out of VO where possible.
- **Cut rules:** no shot under ~3.5 s, never two clips of the same body part back to back, no presenter flashes under 1.5 s.
- **Real packaging only.** Don't show branded packaging the customer won't receive; the in-the-box image must match what ships.
- **Composites of a flat product photo look fake.** Regenerating the scene with the real product as a reference beat pasting a cut-out.
- **Higgsfield Marketing Studio blocks body-device ads as nsfw**; Magnific (Seedance 2.5) handled them.

## Round 2 plan (2026-11-06)
- Ads went live 2026-11-05 after a long "Preparing" queue (every edit/republish resets it; billing, pixel, Account Quality all clean). Pixel has no Purchase event yet, which only slows optimisation.
- Competitor research: Sculpiflex (A$158 kit, gel subscription, ~730 AU ads). Their long-runners are plain offer ads; their persona, trial stats, fat claims and fake was-prices are NOT usable. Details: [ADS-RESEARCH-SCULPIFLEX](../../projects/trivelle-beauty/ADS-RESEARCH-SCULPIFLEX.md), scripts: [ADS-ROUND2-SCULPIFLEX-COPIES](../../projects/trivelle-beauty/ADS-ROUND2-SCULPIFLEX-COPIES.md).
- **Decision:** no fake doctor or fake trial (ACCC/Meta). Run a REAL tester trial ([TRIAL-KIT](../../projects/trivelle-beauty/TRIAL-KIT.md)): 20-30 testers, 30 days, publish real n. Persona = animated character for volume tests + a real person for the trust ad. Hunter is finding the person and recruiting testers.
- Open: price (A$169 + gel sub vs A$219; live price A$199 vs 219 to confirm), supplier cost/shipping for 20-30 kits.
