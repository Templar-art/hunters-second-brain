---
type: project
tags: [trivelle, ecommerce, dropshipping, ads, side-business]
status: launching
updated: 2026-11-04
---

# Trivelle Beauty (trivellebeauty.com)

Hunter's own Shopify dropshipping store, separate from [[10x-visuals]] client work. One product: the **Trivelle 4-in-1 Sculpt & Glow**, a handheld body and face device (gentle heat, red light, EMS micro-pulses, vacuum massage), sold with an 80 g microcurrent gel. Working folder: [projects/trivelle-beauty](../../projects/trivelle-beauty/).

## Offer and economics
- Price **A$219** kit, **A$389** gift 2-pack. Value-anchor copy only, no fake "was" prices (ACCC reference-pricing risk).
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
