---
type: concept
tags: [graphic-design, fitness, coaching, instagram, carousels, offer, research]
status: active
updated: 2026-10-16
---
# Graphic design for fitness coaches — research + what 10x can offer

Research (16 Oct 2026) on the static/graphic side of a fitness coach's content, and how it plugs into the Remotion video system we built for Tyson (`projects/remotion-pipeline/`). Related: [[hormozi-style-motion-playbook]] · [[premium-motion-ui]] · [[talking-head-edit-standards]] · [[brand-system]].

## What the data says (vendor data unless noted, so directional)
- **Carousels = saves + authority; Reels = reach.** A Metricool study of 24.3M posts (Jun 2026) found carousels got **~9× the saves** and ~4× the interactions of single images. Reels get ~36% more reach than carousels (Buffer comparison). → Coaches need **both**: Reels to be found, carousels to be trusted and saved.
- Asking for the save in the caption → **+92% saves** (same dataset).
- Format: **1080×1350 (4:5)** takes the most feed space. One vendor claims ~10 slides is the engagement peak, unverified.
- **Teaching structure that works (coach blogs):** cover → problem → 3 teaching slides → proof → CTA, about 7 slides and ~160 words total. Fitness covers that get saved are technique fixes ("Fix your squat in 5 cues"), "if you feel X, try Y" guides, and routine templates.
- **Trust for coaching comes from peer results, not credentials** (Empower landing-page CRO teardown). Before/after sequences come first, with consistent labels (Week 1–16) and varied body types.
- ⚠️ **AI "goal physique" images:** one vendor case study claims 3× enrolments. It's unverified and ethically risky. If ever used, label them clearly as simulations and never present them as client results. Real before/afters plus testimonials are the defensible route.

## 2026 graphic design direction
- **Bold typography *is* the design:** oversized condensed display type plus tiny supporting text (big/small contrast). Variable fonts make it easy.
- **Soft brutalism:** minimal but rough. Raw textures, asymmetry, imperfect grids.
- **Grain and texture everywhere**, plus warm/structural gradients and paper, Polaroid and sticker touches. It's a move away from flat, sterile layouts.
- Our Tyson system (Barlow Condensed + mono eyebrows, lime/charcoal, grain, shards) already fits this direction, so carousels can reuse it one-for-one.

## The 10x offer for coaches (one design system → every format)
Built once per client in Remotion (it renders stills as well as video), so carousels, covers and Reels share one brand and come out fast:
1. **Brand kit:** palette, type pairing, logo lockup, icon set, grain/texture, and one-page rules. Feeds everything below.
2. **Reel system:** what we built for Tyson (word-synced captions, popups, charts, push-panel scenes), now templated off `script.json`.
3. **Carousel templates (4:5):** a 7-slide teaching layout (cover/problem/3 teach/proof/CTA), plus a technique do/don't, a routine/program card, and a myth-vs-fact. Same components as the video (cards, chips, rings, line charts).
4. **Reel covers + grid system:** a consistent cover for every Reel (big title + face cut-out, reusing `track.py` mattes) so the profile grid reads as a brand.
5. **Proof templates:** transformation (before/after with week labels), client testimonial quote cards, and "client win" stat cards. **Real client data only, with consent.**
6. **Highlight covers + profile polish:** story highlight icons from the same icon set.
7. **Lead magnet design:** a free PDF guide (e.g. "High-protein meal plan", "Beginner 4-week program") with a cover and inside pages, plus a matching Reel/carousel to promote it.
8. **Landing page / link-in-bio:** results first, then method, then CTA (Empower pattern).

### Why this sells
- Coaches need volume plus consistency. A template system turns each new piece into a script/JSON edit instead of a design job → fast turnaround, consistent brand, good margin.
- Video and graphics share one look, so the whole profile feels premium and not "Canva".

## For Tyson specifically (next steps, need Hunter's go-ahead)
- A 7-slide carousel from one of the lesson titles in the reel ("Why you're not losing fat"), as a pilot.
- A Reel cover for the intro video (FOLLOW?/face cut-out style).
- Needs from Tyson: logo/colours if any, real lesson content, before/after photos with consent.

## Sources
- Coachway — carousels for fitness coaches: https://coachway.io/articles/instagram-carousels-for-fitness-coaches/
- True Future Media — carousel strategy 2026: https://www.truefuturemedia.com/articles/instagram-carousel-strategy-2026
- FitBudd — fitness coach content ideas 2026: https://www.fitbudd.com/academy/fitness-coach-instagram-content-ideas-guide-to-marketing-for-professionals-2026
- Krumzi — carousel ideas 2026: https://www.krumzi.com/blog/15-instagram-carousel-ideas-that-actually-drive-engagement-in-2026
- SocialInsider — 2026 Instagram benchmarks: https://socialinsider.io/blog/instagram-carousel-research
- Contentdrips — Reels vs carousels 2026: https://contentdrips.com/blog/2026/06/instagram-reels-vs-carousels-2026-guide/
- Netinfluencer — Instagram views 2026: https://www.netinfluencer.com/instagram-views-up-27-percent-in-early-2026-as-publishing-increases-report-finds/
- Ordinal — carousel posts: https://www.tryordinal.com/blog/carousel-posts
- DesignRush — graphic design trends 2026: https://www.designrush.com/trends/state-of-design
- Picsart — design trends 2026: https://picsart.com/blog/design-trends-2026/
- G2 — graphic design trends 2026: https://learn.g2.com/graphic-design-trends
- Wannathis — typography trends 2026: https://wannathis.one/blog/top-typography-trends-2026-for-designers
- Apexure — Empower coaching landing page CRO: https://www.apexure.com/landing-page-examples/empower-landing-page
- Dreamina — visuals for fitness coaches: https://dreamina.capcut.com/resource/gpt-image-2-for-fitness-coaches-program-visuals
- Lovart — AI transformation case study (vendor claim): https://www.lovart.ai/de/blog/case-study-fitness-coach-ai-body-transformation
