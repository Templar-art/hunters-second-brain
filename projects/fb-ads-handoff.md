# FB Ads Handoff Note — Investment Leads Campaign Diagnosis
Date: 2026-07-20 · From: Claude session in Hunter's Second Brain vault
For: another Claude session. Context + verified research so far + exact diagnostic ask.

## Situation
- Hunter (10x Visuals, Gold Coast AU — real-estate videography/media) running "investment leads" Meta ads.
- 4 days live, $40/day = ~$160 spent, **zero leads**.
- Goal: **volume of leads.**
- Zero leads at $160 usually means a broken funnel or wrong campaign objective, not weak creative — creative problems produce *expensive* leads, not *no* leads.

## Data to collect from Hunter (Ads Manager, 4-day range, per ad)
1. **Objective** — Leads vs Traffic vs Engagement. #1 suspect: Traffic objective optimises for clickers, not leads.
2. **Lead method** — instant form (on-Facebook) vs website form vs Messenger.
3. **Structure** — Advantage+ or manual; CBO or ad-set budget; number of ad sets and ads.
4. **Delivery metrics** — Impressions, Reach, Frequency, CPM, link CTR (not "all"), Link clicks vs Landing-page views (gap = broken page), Results, Cost per result, learning status ("Learning limited" = under-delivering).
5. **Targeting** — location radius, age, interests/Advantage+ audience, placements, audience size.
6. **Creative** — format, first-3-second hook, headline, CTA, and the form itself (each extra form question cuts lead volume).
7. **Funnel check** — if website form: pixel firing? Lead event tracked? Mobile page speed? Submit a test lead from a phone and confirm it arrives.
8. **Offer** — what does the person GET for their details? "Investment leads" needs concrete bait (report, appraisal, callback). Weak/vague offer = high CPM impressions, no conversions.

Likely-culprit ranking at $160/0 leads: wrong objective > weak offer > form friction/broken pixel > creative.

## Verified research findings (adversarially fact-checked, AU real estate, 2025-26)
- **AU real-estate CPM ≈ AU$30** — ~52% above global average (superads.ai). High CPM market; $40/day buys ~1,300 impressions/day.
- **AU real-estate link CTR ≈ 1.68%** for traffic campaigns in 2025, down from 2.60% in 2024 (superads.ai). Use ~1.5-2% as the healthy bar.
- **Vendor (seller-appraisal) lead CPL ≈ AU$48.71 median** for on-Facebook lead forms — Rex Software study, 152 AU agency accounts, AU$285k spend, Oct 2023–Sep 2024. Caveats: single-vendor sample, ~22 months stale, medians. Treat as floor, not guarantee.
- **Generic AU real-estate CPL ≈ AU$26** (superads.ai aggregate) — easier lead type than vendor/investor leads.
- Implication: at $40/day and a realistic $30-60 CPL for investor-grade leads, expect roughly **1 lead per 1-1.5 days** when working. Zero in 4 days = structurally broken, not just unlucky.
- Rex's own marketing benchmarks (CPC etc.) tested 2-6x better than independent averages — **refuted** as market averages; don't cite vendor case-study numbers as norms.
- Everything is post-Andromeda (Meta's ranking overhaul): creative variety matters more, stale/narrow targeting matters less.

## Next steps for receiving Claude
1. Get the 8 data points above from Hunter (screenshots fine).
2. Diagnose funnel-vs-objective-vs-offer first; only touch creative after the pipe is proven to work.
3. For volume: Leads objective + instant form (fewest questions) + broad AU/Gold Coast targeting + 3-5 creative variants; let Advantage+ optimise.
4. Full deep-research report was still synthesising in the origin session; findings above are the verified subset.
