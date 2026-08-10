---
type: concept
tags: [ads, meta, facebook, lead-gen, diagnosis, method, tracking]
status: active
updated: 2026-07-29
---

# Paid Ads Diagnostic Rulebook

A portable method for diagnosing an underperforming Meta/Facebook lead campaign, written so it can be handed to a fresh chat with no prior context. Built during the [[overview|10x Visuals]] investment-leads campaign (4 days, $40/day, zero leads) and generalised. The rules below are the method, not the campaign — they hold for any local-service lead campaign.

Companion artefacts: the live job handoff is [fb-ads-handoff.md](../../projects/fb-ads-handoff.md), which pairs a paste-ready operator prompt with the campaign's own numbers.

## Rule 1 — Read the zero before you read the creative

A campaign producing *expensive* leads and a campaign producing *zero* leads are different diseases with different treatments. Weak creative, a soft offer, or mediocre targeting all still leak some leads through; they raise cost per lead, they do not zero it. A hard zero across several days of real spend almost always means the conversion path is structurally broken or the campaign is optimising for something other than leads.

So the first question is never "how do we improve the ad". It is "is the pipe connected". Rewriting a hook on a campaign whose pixel never fired burns another few days and teaches nothing.

## Rule 2 — Diagnose in fixed priority order

Work the list top to bottom and stop at the first thing that is actually wrong. Do not skip ahead because a later item looks more interesting.

1. **Campaign objective.** Traffic and Engagement objectives optimise for clickers and reactors. Meta will happily deliver a thousand clicks and no leads, and it is doing exactly what it was told. Leads objective, or nothing.
2. **Offer.** What does a person receive in exchange for their details? "Investment leads" is a category, not an offer. A free appraisal, a suburb report, a callback within 24 hours — something concrete and nameable. A vague offer buys impressions and converts none of them.
3. **Funnel mechanics.** Instant form versus website form; pixel firing; Lead event registered; mobile page speed; number of form questions. Every additional question costs volume. Submit a real test lead from a phone and confirm it lands where it is supposed to land.
4. **Creative.** Only once the three above are proven sound. At this point creative is a cost-per-lead lever, not an on/off switch.

## Rule 3 — Collect data before forming an opinion

Eight data points, ideally as Ads Manager screenshots over the campaign's full run, per ad:

- Objective, and the lead method (instant form / website / Messenger)
- Structure: Advantage+ or manual, CBO or ad-set budget, count of ad sets and ads
- Delivery: impressions, reach, frequency, CPM
- Link CTR specifically — not the "all clicks" CTR, which flatters everything
- Link clicks *versus* landing-page views — a large gap between them is a broken or slow page, and it is invisible in any other column
- Results and cost per result
- Learning status: "Learning limited" means the ad set is starved and the numbers are not yet meaningful
- Targeting: radius, age, interests or Advantage+ audience, placements, audience size

An expert guessing at settings is worth less than a novice reading the actual delivery columns. Ask, wait, then diagnose.

## Rule 4 — Ground every judgement in a benchmark, and check the benchmark's source

Numbers only mean something against a market baseline, and ad-industry baselines are full of vendor marketing. Anything published by a platform about its own clients is a case study, not an average — during this research a vendor's published figures ran two to six times better than independent aggregates, which is exactly what a self-selected sample looks like. Prefer independent aggregators, note the data window, and treat anything older than about a year as a floor rather than a forecast.

The AU real-estate baselines established for this work, all adversarially fact-checked:

| Metric | Baseline | Note |
|---|---|---|
| CPM | ~AU$30 | Roughly 52% above global average; AU is an expensive market |
| Link CTR | ~1.68% | 2025 traffic campaigns, down from 2.60% in 2024 |
| Vendor/seller lead CPL | ~AU$48.71 median | Rex study, 152 AU accounts, window ended Sep 2024 |
| Generic real-estate lead CPL | ~AU$26 | Easier lead type than vendor or investor |

## Rule 5 — Convert the benchmark into an expected result, then compare

This is the step that turns benchmarks from trivia into a diagnosis. Divide daily budget by expected cost per lead to get an expected lead rate, then measure the gap.

At $40/day against a $30–60 CPL for investor-grade leads, a working campaign should produce roughly one lead every one to one-and-a-half days. Four days at zero is therefore not bad luck inside normal variance — it is a structural failure, and Rule 2 tells you where to look. Had the same spend produced three leads at $53 each, the correct response would have been the opposite: leave it alone, it is working, and the only question is scale.

## Rule 6 — Rebuild for the goal that was actually stated

When the goal is lead *volume* rather than lead quality, the settings follow mechanically: Leads objective, on-Facebook instant form with the minimum viable question set, broad geographic targeting rather than layered interests, three to five creative variants, and Advantage+ left to optimise. Every qualifying question, narrow audience, and off-platform redirect is a volume tax. Charge it deliberately when quality is the goal; remove it when volume is.

## Rule 7 — Hand off with a prompt, not just a document

A research note alone makes the next chat re-derive the method. Pair the findings with an operator prompt that states the role, the situation, the priority order, and the instruction to gather data before advising — then the next session starts where this one ended instead of starting over. The pattern is in [fb-ads-handoff.md](../../projects/fb-ads-handoff.md).

## Rule 8 — Set up the measurement before the campaign that needs it

The rules above are written from the post-mortem direction: something ran, it underperformed, work out why. Three pieces of setup hygiene make that post-mortem possible at all, and each one is cheap before launch and unrecoverable after. Source: [[zidane-meta-ads-tips]], 29 Jul 2026.

- **Install the dataset early.** Meta's Pixel is now called a *dataset* in Events Manager. A fresh one has no event history, so it cannot optimise or build audiences on the first days of a campaign — which is exactly when a new campaign is being judged. Install it, verify the Lead event fires, and let it accumulate before the spend it is meant to inform. ⚠️ **But know what it does not cover:** a dataset records events on your *website*, so it tracks nothing on an on-Facebook instant-form campaign, where Meta records the lead natively. Diagnosing a dead instant-form campaign by checking the pixel is looking in the wrong place — and installing one won't fix it. Setup and the correct scope for each lead type: [[meta-tracking-setup]].
- **Turn Advantage+ creative enhancements off.** Text improvements and visual improvements let Meta rewrite ad copy and re-crop, filter and re-score creative per placement. On a campaign whose qualification depends on precise wording — scope stated publicly, budget asked privately, no pricing anywhere — a copy rewrite silently removes the filter, and the resulting bad leads look like a targeting failure. Off by default; on only as a deliberate test.
- **Tag website destinations with dynamic UTMs.** `utm_source=facebook&utm_medium=cpc&utm_term={{adset.name}}&utm_content={{ad.name}}&utm_campaign={{campaign.name}}` — Meta fills each placeholder from the asset's own name at delivery, so per-ad attribution needs no manual tagging. It follows that asset names *are* the analytics labels, so name them deliberately and avoid spaces and commas. Irrelevant to on-Facebook instant forms, which load no URL.

## Method note — how the research itself was run

The benchmarks above came from a fan-out research pass: several parallel search angles, source fetching, then a three-vote adversarial verification on each extracted claim, where a claim needed two of three refutations to be killed. That verification layer is what caught the vendor-marketing figures. Any benchmark repeated into a client-facing recommendation should survive the same treatment — a plausible number from a single source is not a fact.
