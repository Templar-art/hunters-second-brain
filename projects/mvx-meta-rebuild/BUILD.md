# MVX Meta Rebuild — build sheet

**Date:** 2026-07-28 · **Revised:** 2026-07-29 (five-ad-set CBO structure, revised kill rules) · **Goal:** fewer, better leads. Not cheaper leads.
**Why build new rather than edit:** Meta locks conversion location and performance goal once an ad set publishes, so the existing campaigns can't be corrected. **Nothing gets deleted** — hot water launches as a new campaign and aircon keeps running as the control.

## What went wrong (so we don't repeat it)

| Setting | Was | Why it produced junk |
|---|---|---|
| Performance goal | Maximise number of leads | Tells Meta "find people who'll fill a form", so it hunts the cheapest form-fillers on the platform |
| Audience size | 3.8–4.5M | Gold Coast + Northern NSW is ~700k. Reached 5× the service area — that's the Sydney and Canberra leads |
| Advantage+ audience | On | Widens past your targeting whenever cheaper fills exist |
| Instant form | Full prefill, no qualifiers | Name, email, phone in one tap. No thought, no commitment |

Result across 30 days: 13 leads, ~$541 spent, roughly a third outside the service area and most of the rest small or price-shopping jobs. One genuinely good lead (3-phase, ducted Daikin, solar + battery, asked for a quote) came in through **ducted aircon**.

## Sequence change, 28 Jul — hot water goes first

Hunter's call, and it's the right one: build **hot water as a brand-new campaign** instead of deleting anything. A new campaign means a new ad set, which means the conversion location and performance goal can be set correctly from scratch. Nothing running gets touched.

It also gives a clean comparison. Aircon keeps running on the old settings as the control; hot water runs on the new ones. Same account, same audience, same brand. Whatever the difference in lead quality is, it's the settings.

- **Aircon Push** — leave running, untouched. It's the control and it's the only thing producing.
- **General Electrician** — **pause** it. 3 leads at $89 over 30 days is pure waste and pausing costs nothing. Don't delete: keep it for reference until the new structure is proven.
- **Hot water** — new campaign, built to the spec below.
- **Aircon rebuild** — only after hot water shows the new settings produce better leads. Don't rebuild the one thing that works on a theory.

⚠️ **Blocker before this can launch: Matt's plumbing answer.** A Meta instant form doesn't need the landing page, so the campaign can run without it, but we can't advertise a service MVX can't deliver. If Matt subs or partners a plumber, angles 1 and 3 run as written. If he's electrical-only, they get rescoped to changeovers, circuits and compliance, with the plumbing coordinated. One question, and it decides the copy.

**Demand note:** hot water on Meta is thinner than aircon. Nobody plans a hot water upgrade the way they plan aircon before summer, and the emergencies all go to Google. So Meta's hot water job is specifically the **heat pump upgrade with the rebate** — a planned purchase with a real number attached. Expect fewer leads than aircon and judge it on quality, not volume.

## Campaign structure

One campaign. **Five ad sets, one ad each. CBO with a $5/day minimum spend limit per ad set.**

⚠️ **Supersedes the 28 Jul structure** (one ad set, four ads, $20/day), which pooled the angles into a single ad set to concentrate learning. Hunter's call, 29 Jul, on operator advice via [[zidane-meta-ads-tips]]: run the angles as separate ad sets with spend floors so each one is guaranteed a real test and the weak ones are unambiguous to cut. The dated trail for the earlier reasoning is kept below under *Structure tradeoff*.

Budget goes to the **campaign**, not the ad sets. Each ad set carries a **$5/day minimum spend limit**, so $25 of the $40 is guaranteed distributed and the remaining **$15 is the contested pool** — Meta reallocates it toward whichever ad sets are producing, and every angle still gets its floor. One ad per ad set means the ad-set row *is* the angle's scorecard: no ad shares a budget with a rival, so the comparison is clean.

```
Campaign:  MVX | Hot Water | Qualified Leads | Aug 2026
  Objective:              Leads
  Campaign budget:        $40/day  (CBO / Advantage campaign budget)
  Budget scheduling:      off
  5 × Ad set              Gold Coast + Northern NSW, identical targeting
    Min spend limit:      $5/day   ← the floor. 5 × $5 = $25 guaranteed
    Max spend limit:      none     ← leave open so a winner can take the pool
    Conversion:           Instant forms   ← cannot be changed later, get it right now
    Ads:                  1 angle each (5 angles below)

  Contested pool:         $40 − $25 = $15/day
```

Ad sets are named for the angle, because those names become the analytics labels via the dynamic UTM string in [[zidane-meta-ads-tips]] — no spaces or commas:

```
HW-Rebate  ·  HW-WeAreSparkies  ·  HW-RunningCost  ·  HW-JobProof  ·  HW-Timing
```

### Structure tradeoff — what to watch, not a reason to change it

Recorded so that if the campaign disappoints, the first week's numbers get read correctly instead of triggering another rebuild.

- **Every ad set will show "Learning limited," and that is expected here.** Meta exits the learning phase at roughly 50 optimisation events per ad set per week. At $5–15/day against the ~$42 blended CPL from the last 30 days, each ad set books closer to one lead a week. The floors are buying *breadth of test* and paying for it in *depth of signal* — that is the deliberate trade. Don't read "Learning limited" as a fault to fix.
- **Judge the first fortnight on creative signal, not on cost per lead.** See the revised kill rules — one lucky lead on a $35 week reads as a $35 CPL and one dry week reads as failure, and neither is real at this volume.
- **Meta may under-deliver the campaign budget.** Spend limits constrain the optimiser; if an ad set cannot spend its floor, the campaign can come in under $40/day. Check actual spend against $40 on day 2 rather than assuming it delivered.
- **Meta's own guidance is a daily budget at or above the cost of one optimisation event.** $5/day sits well under a ~$42 lead, so expect a warning in the UI at publish. Publishing through it is the decision, not an error.
- **If it does need loosening later, the first lever is the floor, not the structure** — drop to $3/day (contested pool $25) or cut to 3 ad sets at $5 (pool $25), before touching CBO itself.

## Ad set settings

Identical across all five ad sets — the only difference between them is the ad inside.

- **Conversion location:** Instant forms
- **Performance goal:** Maximise number of leads, **with a cost-per-result goal of $60**. Counterintuitive but deliberate: leaving it at "None" tells Meta to chase the floor, which is how we got $27 tyre-kickers. A higher target lets it bid for better people. **Once Lach's call tracking is live and lead statuses feed back, switch to "Maximise number of conversion leads"** — that's the real fix and it needs the data first.
- **Location:** Gold Coast + Tweed Heads / Northern NSW. Set to **"People living in this location"**, not "living in or recently in".
- **Age:** 30–65+. Under 30 rarely owns the house.
- **Advantage+ audience:** **OFF.** Use original audience options so the geo actually holds.
- **Placements:** Manual. Facebook feed, Instagram feed, Reels, Stories. Audience Network stays excluded.
- **Detailed targeting:** none. Broad within the locked geography is correct post-Andromeda; the filtering job belongs to the creative and the form, not to interests.

## The instant form — this is where quality is won

Name it `Hot Water Enquiry | Qualified | Aug 2026`.

**Intro screen** (does half the filtering):
> **Hot water systems, by licensed electricians**
> A few quick questions so we can quote it properly. We supply, install and certify complete systems, so we're not the cheapest option in town and we don't pretend to be.

**Questions, in this order:**
1. **Do you own the property?**
   - I own it · I'm renting · I manage it for the owner
   
   This is the strongest single filter on a hot water ad. A renter cannot authorise a system replacement, and hot water ads attract them because everyone's had a cold shower.
2. **What's happening?**
   - No hot water right now · It's leaking · Old system I want replaced · I want a heat pump upgrade · Not sure
3. **What have you got now?**
   - Electric tank · Gas · Solar · Heat pump · Don't know
   
   Real quoting information, and it separates people who've thought about it from people who haven't.
4. **Roughly what's your budget?**
   - Under $1,500 · $1,500–$3,000 · $3,000–$6,000 · $6,000+ · Not sure
5. **Suburb** — short answer, not postcode
6. **Name** — prefill allowed
7. **Phone** — **prefill OFF.** Making someone type their own number is the single cheapest quality filter available.

Drop the email field. Drop the free-text "tell us about the job" box — on the aircon form people wrote essays and it didn't change whether Matt called.

**Completion screen:**
> **Got it. We'll call you today.**
> One of our licensed electricians will ring the number you gave us. If you'd rather not wait, call 0427 593 990.

⚠️ Turn **on** "Review your info" before submit. Extra friction is the point.

## The five ad angles

One angle per ad set, one ad per ad set. Simple, one message each, real photos, no hype. Black and white with green on the CTA only, ≤10% of the frame. Per brand: plain English, proof first, no urgency.

**1. The rebate, handled** *(the strongest hook — a real number, but on the offer, not the price)*
> Upgrade to a heat pump and the federal rebate comes off the install price upfront. We handle the certificates.
> Licensed Gold Coast electricians. Supply, install, certify.

The rebate figure is a *discount*, not a price, so it doesn't invite comparison shopping or go stale the way a "from $X" would. ⚠️ Confirm the current figure with Matt's supplier before it goes live.

**2. We are the electricians** *(the differentiator, and for hot water it's more true than for aircon)*
> Element, thermostat, circuit, isolator, switchboard: that's where an electric hot water system actually fails, and all of it is licensed electrical work.
> We are the electricians, so the diagnosis and the fix happen on the same visit.

**3. Running cost** *(outcome-led, zero urgency — the brand guide forbids fear)*
> A heat pump runs on a fraction of the power of an old electric tank.
> If your system is over ten years old, the upgrade usually pays for itself on running costs alone. We'll tell you straight whether it's worth it.

**4. Real job proof** *(brand guide: content leads with proof)*
> 15 years on Gold Coast jobs. Photo of an actual changeover, tidy pipework, clean finish.
> Supply, install, compliance certificate. Done as promised.

**5. Worth doing now, or not yet** *(ad set `HW-Timing` — planned-purchase framing, added 29 Jul with the five-ad-set structure)*
> Not every hot water system needs replacing. Over ten years old, on an old electric tank, and the rebate is on the table: that's when the numbers stack up.
> We'll look at it and tell you which one you are.

Written to suit the demand note above — Meta's hot water job is the *planned* heat pump upgrade, not the emergency, and this angle speaks to someone deciding rather than someone panicking. It also tests the willingness-to-be-told-no offer, which is the closest thing to a qualifier that can sit in ad copy while [no pricing](#) holds.

No manufactured urgency in any of the five. Angle 3 is deliberately about **running cost** rather than "before it bursts" — the guide says no fear or pressure, ever, and a burst-tank threat is exactly that. Angle 5 says "or not yet" out loud for the same reason.

## Kill rules

⚠️ **Revised 29 Jul.** The previous rule — *kill any ad over $80 per lead at day 7* — does not survive this structure and has been replaced. With five ad sets on a $40/day campaign, each books roughly one lead a week, so a day-7 per-ad-set CPL is a sample of one: a single lucky lead reads as a $35 winner and a single dry week condemns the best angle. Judging the first fortnight on CPL would kill the wrong ad sets with confidence. Creative signal accumulates thousands of data points a week and is readable on schedule; lead economics needs three.

**Day 7 — cut on creative signal only. No CPL decisions.**

| Signal | Kill if | Why it's readable at day 7 |
|---|---|---|
| Link CTR | Under ~1% against the ~1.68% AU baseline in [[paid-ads-diagnostic-rulebook]] | Thousands of impressions per ad set even at the $5 floor |
| Cost per form open | Worst of the five by a wide margin | The instant-form equivalent of a landing-page view |
| Form open → submit rate | Far below the others | Separates a bad ad from a bad form — if *all five* are low, the form is the problem, not the creative |
| 3-second video views / thumbstop | Bottom of the set, video angles only | Hook performance, independent of lead volume |

Cut the worst one or two, leave three or four running, and let their floors redistribute into the contested pool.

**Day 14 — first quality read.** Now the qualitative filter applies, because there are enough leads to see a pattern: kill any surviving ad set producing only renters and "Not sure" budget bands, regardless of how good its CTR looks. A cheap lead that fails the budget question is the exact failure mode of the last campaign.

**Week 3 — lead economics, finally.** Each survivor should now have 5+ leads, which is when cost per lead means something. Kill over **$80 per lead** at this point, not before. Scale the survivor toward $40–45/day, which is where Brian's winner sits.

**Throughout:** judge on **jobs quoted**, not leads. A week of 4 good leads beats 10 junk ones — and this is the number Matt actually feels.

## Pre-launch settings (from [[zidane-meta-ads-tips]], 29 Jul)

Three items that are cheap now and unrecoverable after launch. Full reasoning in [[paid-ads-diagnostic-rulebook]] Rule 8.

- **Advantage+ creative enhancements OFF** — both *text improvements* and *visual improvements*, on every ad. Meta rewrites ad copy per placement, which would silently strip the scope wording and the no-pricing rule that this campaign's entire qualification strategy rests on. The resulting junk leads would look like a targeting failure and trigger a third rebuild. Non-negotiable, and it applies to every 10x campaign, not just this one.
- **Dataset (formerly Pixel) installed and the Lead event verified firing** before publish, not during. A fresh dataset has no event history in exactly the week the campaign gets judged.
- **Dynamic UTMs — not applicable to this campaign.** Instant forms load no URL, so there are no parameters to populate. The string belongs on the Google Ads landing pages instead. Ad set names still matter here though, because they're the labels everywhere else.

## Assumptions to correct before launch

1. **Minimum job value** worth Matt's time. It sets the budget bands and the kill rules.
2. Ask Matt which of the last 11 leads he'd actually have wanted. That answer defines "quality" better than anything we can infer.

**No pricing in any ad** — Hunter's call, 28 Jul. Public numbers invite comparison shopping, date instantly, and pull the exact bargain-hunter audience we're trying to filter out. Qualification happens through **scope** in the ad and the **budget band** inside the form, where it's private.

## Sequence

1. **Matt confirms the plumbing route** and the current rebate figure. Nothing launches before this.
2. **Pause** General Electrician. Leave Aircon Push running as the control. Delete nothing.
3. **Install the dataset and verify the Lead event fires** — before anything is built, so it has history by the time it's judged.
4. Build the **form** first. Then build **one ad set** complete with its ad, check conversion location and performance goal twice, and only then **duplicate it four times** and swap the angle — the ad set is the step that can't be undone, and duplicating a verified one is safer than configuring five from scratch.
5. Set the **$5/day minimum spend limit** on each of the five ad sets, and the **$40/day budget at campaign level**. Confirm max spend limits are left empty.
6. On every ad, confirm **text improvements and visual improvements are off** before publishing.
7. **Day 2: check actual spend against $40.** Spend limits can cause under-delivery; if the campaign came in short, the floors are too tight for the audience and drop to $3/day.
4. Launch hot water at **$20/day**.
5. **Day 7 review** against the kill rules, comparing lead quality against aircon on the old settings.
6. If the new settings win: rebuild aircon the same way, then Google. Lach's call tracking landing is what lets the performance goal switch to conversion leads.

---
_Vault: [[mvx-electrical]] · method: [[paid-ads-diagnostic-rulebook]] · proven pattern: [[strategic-investing-qld]]_
