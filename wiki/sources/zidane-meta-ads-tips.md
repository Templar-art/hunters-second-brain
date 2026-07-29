---
type: source
tags: [source, ads, meta, facebook, tracking, utm, lead-gen]
status: active
updated: 2026-07-29
---

# Zidane — Meta ads operator tips (verbal, 29 Jul 2026)

Practitioner notes passed to Hunter by **Zidane** (mate, works Meta ads), relayed as a five-line dump. Not a document — no screenshots, no account data, no attribution to a course or agency. Treat as operator opinion from someone running spend, worth testing, not as a benchmark. Benchmarks and the diagnostic order still live in [[paid-ads-diagnostic-rulebook]].

Context for why this arrived now: the [[mvx-electrical]] Meta rebuild ([BUILD.md](../../projects/mvx-meta-rebuild/BUILD.md)) is specced but unlaunched, and the [[lead-gen-engine]] landing pages went live 28 Jul, so anything about structure and tracking is immediately actionable.

## The five tips, decoded

**1. Use CBO — campaign budget optimisation.** Budget set at campaign level, Meta allocates it across ad sets rather than each ad set holding its own fixed slice. Meta's current UI calls this **Advantage campaign budget**; "CBO" is the older name and still what operators say. Already the shape of the MVX rebuild — $20/day at campaign level, four angles as four *ads* inside one ad set so learning pools instead of fragmenting. So this tip confirms an existing decision rather than changing it.

**2. Long videos beat short for VSL.** A video sales letter needs runway to make an argument; a 6-second hook cannot carry an offer that requires explanation. This is the opposite of the reflex short-form advice and it is worth taking seriously here, because long-form video is the one asset 10x can produce better than any competitor in the trade-services space. Untested claim with no numbers attached — the honest framing is that it makes a good A/B test against the four-angle ad set, not that it is established.

**3. Turn off text improvements and visual improvements.** These are Meta's **Advantage+ creative enhancements** — automatic filters, crops, aspect-ratio changes, added music, and *rewritten ad copy*, applied per-placement and on by default. For 10x this should be a standing default, not a per-campaign decision: they overwrite brand colour and type ([[brand-system]]), they crop composed frames, and copy rewrites break the deliberate no-pricing and scope-qualification wording that the MVX ads depend on to filter leads. Turning them off is consistent with [[staging-rules]]-style thinking — the whole point of controlling the frame is that nothing else gets to change it.

**4. Get a pixel / dataset — it collects data.** Meta renamed Pixel to **dataset** inside Events Manager; same object, one per business, shared across ad accounts. The operator point is the second half: a fresh dataset is not useful the day it is installed, it needs event volume before optimisation and audience-building work at all. Which means installing it early, before the campaign that will depend on it, is the actual instruction. This is Rule 2 item 3 in [[paid-ads-diagnostic-rulebook]] — *pixel firing, Lead event registered* — approached from the setup side rather than the diagnosis side.

**5. Tag destination URLs with dynamic UTM parameters.** So that Meta traffic arrives in analytics already broken out by campaign, ad set and ad, without hand-maintaining a tag per ad:

```
utm_source=facebook&utm_medium=cpc&utm_term={{adset.name}}&utm_content={{ad.name}}&utm_campaign={{campaign.name}}
```

Meta substitutes each `{{…}}` at delivery time from the asset's own name, so ads inherit tags automatically and renaming an ad set renames its traffic. Two consequences: **name assets deliberately**, because the names become the analytics labels and a name like "Ad set 1 — copy" is permanent noise; and avoid spaces and commas in names, which arrive URL-encoded.

⚠️ **This does not apply to the MVX Meta rebuild as specced.** That campaign uses on-Facebook instant forms — the user never leaves Facebook, no URL is loaded, so there are no URL parameters to populate. UTMs are relevant to (a) the Google Ads landing pages — [/air-conditioning-electrician-gold-coast/](https://mvxelectrical.com.au/air-conditioning-electrician-gold-coast/), [/gold-coast-electricians/](https://mvxelectrical.com.au/gold-coast-electricians/), the hot water page — and (b) any future Meta ad whose destination is the website. Adopt the string there; ignore it on instant-form campaigns.

## Where the tips sit against what we already decided

| Tip | Verdict |
|---|---|
| CBO | Already the MVX spec. Confirms it. |
| Long VSL | New, untested, plays to 10x's strength. Test — don't rebuild around it. |
| Creative enhancements off | Adopt as a standing 10x default. Add to any launch checklist. |
| Dataset early | Sequencing correction: install before the campaign needs it, not during. |
| Dynamic UTMs | Adopt for website-destination traffic only. Not instant forms. |

Nothing here contradicts [[paid-ads-diagnostic-rulebook]]. Tips 3–5 are setup hygiene the rulebook only covered from the post-mortem direction, which is the gap they fill.
