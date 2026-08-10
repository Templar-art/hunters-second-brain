# MVX Meta — account state and change log, 10 Aug 2026

**Ad account:** MVX Electrical (977862831831417) · **Business:** 193437025904042
**Who did this:** Hunter, with Claude driving Ads Manager in Chrome. Every irreversible step was Hunter's call.
**Doubles as the Lachlan handoff.** Everything below is either a change that was made or a finding that changes how the account should be run.

Vault: [[mvx-electrical]] · spec: [BUILD-CALLS.md](BUILD-CALLS.md) · account-wide: [ACCOUNT-SETTINGS.md](ACCOUNT-SETTINGS.md)

---

## 1. The account was not in the state the vault said it was

**Three August campaigns were already built and running, and none of them were ever logged.** The vault said the Meta rebuild was blocked on Matt's answers and that only the two July campaigns existed. Wrong. Read off Ads Manager, last 30 days:

| Campaign | Was | Leads | Cost/lead | Spent |
|---|---|---|---|---|
| MVX – General Electrician – Aug 2026 | Active, $10/day | 1 | $124.91 | $124.91 |
| MVX – Air Cons – Aug 2026 | Active, $10/day | 2 | $63.95 | $127.90 |
| MVX – New Builds & Renos – Aug 2026 | Active, $20/day | 2 | $126.58 | $253.16 |
| General Electrician \| Lead Form \| July 2026 | Off | 2 | $131.75 | $263.50 |
| **Aircon Push \| Lead Form \| July 2026** | **Off** | **12** | **$28.02** | $336.22 |

**The number that matters:** the two July campaigns produced **14 leads at $42.84**. The three August campaigns produced **5 leads at $101.19**. The rebuild was running at 2.4× the cost per lead of the thing it replaced — and **Aircon Push, the only strong performer in the account's history, had been switched off**, despite [BUILD.md](BUILD.md) explicitly saying to leave it running as the control.

Root cause was not creative or targeting. It was **$40/day split across three separate learning pools**. At $60–125 a lead, each campaign booked well under one conversion a week against the ~50/week Meta needs to optimise. None of them could ever leave the learning phase. ([[paid-ads-diagnostic-rulebook]] Rule 5 — convert the budget into an expected lead rate before diagnosing anything else.)

---

## 2. Findings that change how this account gets built from now on

### An Advantage+ leads campaign cannot be set to "people living in this location"

All three August campaigns were **Advantage+ leads campaigns**. That campaign type removes the location-type control entirely — under *Show more controls* you get minimum age, audience exclusions and languages, and nothing else. So the single setting [ACCOUNT-SETTINGS.md](ACCOUNT-SETTINGS.md) locked as non-negotiable, the fix for the Sydney and Canberra leads, **could not be applied to any of them.** Not "wasn't". Couldn't.

⚠️ **And it isn't available on a manual campaign either, in this account's UI.** The old *living in / recently in / travelling in* dropdown appears to have been retired. What replaced it is a two-tier audience model:

- **Controls** — "We won't reach people beyond these settings, even with Advantage+ on." Locations and minimum age sit here. Hard boundary.
- **Suggest an audience** — "We'll also reach people beyond any custom audience, age, gender and detailed targeting settings." Soft, and Advantage+ overrides it freely.

So location *is* now a hard boundary, and the correct action is no longer hunting for a dropdown. It is the next item.

### The actual out-of-area leak is a checkbox called "Reach more people likely to respond to your ads"

Sits directly under the location map, **ticked by default**. Its own description: *"We'll also show ads to people interested in your selected cities and regions, in those countries."* That is the mechanism that serves a Gold Coast ad to someone in Sydney who once looked at Gold Coast property — and it is on by default on every new ad set.

**Unticked on the new campaign.** Meta immediately offered it back as "6.7% lower cost per result", which is exactly the trade that produced the junk: cheaper results, wrong people. Declined.

**Lachlan: this needs checking on every existing MVX ad set, and on every campaign you build for anyone else.**

### Radius defaults to +40 km, which alone recreates the failure

Typing "Gold Coast" gives you **Gold Coast + 40 km**, and the audience estimate jumped to **3.9–4.5M** — the exact figure [BUILD.md](BUILD.md) blames for the July out-of-area leads. The 40 km ring from Gold Coast reaches into Brisbane.

Set to the config the account's better campaign was already using: **Gold Coast +17 km, Byron Bay +40 km**. Audience lands near the ~700k service area instead of 5× it.

### There is no call-duration performance goal on this account

The whole quality strategy in [BUILD-CALLS.md](BUILD-CALLS.md) rested on optimising for *quality calls* (60s+ duration), so Meta only books a result when someone actually described a job. Meta's own tooltip: **"Maximise number of calls is the only performance goal available for this conversion location."**

So the calls campaign optimises for the *tap*. Quality control now rests entirely on the creative, the geo, and the ad schedule. ⚠️ **Watch for four-second calls in week one** — that is the failure mode this would have prevented.

**No cost cap was set, and that is a deliberate reversal.** The fallback plan was a $45 cost-per-result cap. On inspection a call *tap* will likely cost $10–25, so a $45 cap binds on nothing; and if calls do run dearer it throttles delivery on a campaign with no history. Better to read the real cost per call at day 7 and set a cap that has data behind it.

### Ad scheduling IS available on a daily budget — for calls campaigns

[BUILD-CALLS.md](BUILD-CALLS.md) said dayparting needs a lifetime budget and the campaign would have to run 24/7. **Wrong for this conversion location.** A Calls ad set exposes *Ad scheduling → Set a schedule for ads* on a plain daily CBO budget, and Meta itself recommended it: *"You could get 25.4% more call conversions by running ads during your business hours."*

Set to **Mon–Sat 09:00–18:00, Brisbane time**. Saturday is in deliberately — the "list" audience does its thinking on weekends. This is the single biggest mitigation of the missed-call risk.

### Minimum age caps at 25

The dropdown does not offer anything above 25, so the specced 30–65 is not achievable. Set to **25**, which still excludes the youngest renter cohort.

### Meta's AI wants to put a different man's face in an owner-led ad

The Advantage+ image generation step offered ~30 AI variants per ad. Several under "High CTR styles" show **a man in a blazer who is not Matt.** For a campaign whose entire premise is "you're speaking to the actual sparky", running a synthetic owner would destroy the only real differentiator. **Zero AI creative selected on any ad.** Every duplicate dialog also pre-ticks a "add an image/video to reach people in different ways" recommendation — untick it every time.

### "Multi-advertiser ads" crops your creative

Ticked by default on every ad. Its own text: *"Your ad creative may be resized or cropped."* On 9:16 with burned-in captions in the mid-frame safe zone, that is the same damage as visual improvements. **Unticked on all three new ads.**

### 9:16 gets masked in feed

Meta's warning, verbatim: *"This video will be masked on mobile News Feed, Instagram Feed, Instagram Explore and Instagram Profile Feed. The tallest supported aspect ratio … is vertical (4:5)."* Reels and Stories run clean.

**Not fixed.** The fix lives at *Customise media → Crop*, which offers separate square / vertical / horizontal crops per ad, all currently "Original". Auto-cropping a 9:16 with burned-in captions can slice the text, so each preview needs eyes on it. **Open job.**

### Placements were already set up correctly

Account-level controls already exclude Audience Network native/banner/interstitial, Audience Network rewarded video, Facebook right column and Facebook Marketplace. Nothing to do — worth knowing it was right.

### The "1 additional task to review" is nothing

It resolves to the **financial products and services declaration** checkbox. Not applicable to an electrician. Leave unticked.

---

## 3. What was actually changed in the account

### Live changes (took effect immediately)

| # | Change | Why |
|---|---|---|
| 1 | **Aircon Push \| July → ON**, $10/day | 12 leads at $28 is the best number in the account's history and it was sitting dark |
| 2 | **MVX – Air Cons – Aug → OFF** | Same offer as #1 at 2.3× the cost. Two campaigns bidding for the same person |
| 3 | **MVX – General Electrician – Aug → OFF** | 1 lead at $125. Replaced by the new calls campaign |
| 4 | MVX – New Builds & Renos – Aug | **Left running**, $20/day, untouched |
| 5 | General Electrician \| July | Left off |

Nothing was deleted. Every paused campaign is still there for reference.

### Drafts built, not published (Hunter presses Publish)

**New campaign — `MVX | General Electrical | Calls | Aug 2026`**

```
Objective            Leads
Conversion location  Calls              ← locks at publish
Performance goal     Maximise number of calls (only option available)
Cost per result goal empty, deliberately
Budget               $20/day, campaign level (CBO)
Phone                0427 593 990
Schedule             Mon–Sat 09:00–18:00 Brisbane
Locations            Gold Coast +17 km QLD; Byron Bay +40 km NSW
"Reach more people likely to respond"   UNTICKED
Minimum age          25
Detailed targeting   none
Advantage+ audience  ON     (account-wide decision, Hunter 10 Aug)
Advantage+ placements ON
Ad set               1 · Ads 2
```

- **`GE-List`** → MVX Ad 3 (10.1s) · headline *Get The Whole List Done*
- **`GE-WholeList`** → MVX Ad 2 (12.3s) · headline *One Visit, One Trade*
- Both: CTA **Call Now**, multi-advertiser ads off, no AI creative, call description *"You'll speak to a licensed MVX electrician, not a call centre."*

**New ad in the existing campaign — `NB-Renos-Video`**

Inside `MVX – New Builds & Renos – Aug 2026`. **No budget or targeting change to that campaign** — a new ad only, so the ad set's 13 days of history stays intact.

- MVX Ad 1 (15.2s), the renovations cut
- Headline *Send Us Your Plans* · description *Free quote on your build. Gold Coast & Northern NSW.* · CTA **Get quote**
- Same `New Home & Renos | MVX | August 2026` instant form as the existing ad, with its "Call Matt Directly" action intact
- Multi-advertiser ads off · all four Advantage+ creative enhancements off (video touch-ups, text improvements, relevant comments, enhance CTA) · no AI images

**Total after publish: $50/day** — Aircon Push $10 + New Builds $20 + Calls $20. Approved by Hunter, 10 Aug.

---

## 4. The creative, corrected

The 3 Aug shoot delivered **five files, three of them ads.** Verified by pulling every burned-in caption frame by frame, because the earlier read of them was wrong twice.

| File | Length | Angle | Spoken CTA | Where it went |
|---|---|---|---|---|
| MVX Ad 1 | 15.2s | New builds & renos | "send us your plans… we'll send you a quote" | `NB-Renos-Video` |
| MVX Ad 2 | 12.3s | General — "get the whole list done" | "just give us a call" | `GE-WholeList` |
| MVX Ad 3 | 10.1s | General — "everyone's got a list" | "give us a call / get in touch" | `GE-List` |
| Green Power Boxes | 47.9s | Commercial switchboard/pillar project | none | organic only |
| Broadbeach Library | 19.9s | Council library fitout | none | organic only |

**The CTA split is what decided the whole structure.** Two cuts say *call*, one says *send your plans*. Conversion location locks at publish, so the mechanism had to follow the creative — a calls campaign for the two, and the existing form campaign for the third. Putting all three in one place would have mismatched the ask on at least one of them.

**The two project videos are not lead ads.** They end on scenery with no offer and no ask, and their subject is council/commercial work. In a lead campaign they would spend and return nothing. They belong on the Page and Instagram organically, and later as retargeting creative.

⚠️ **Setup B never happened — there is still no new-build site footage.** Ad 1 mentions renos inside a general-electrical body; it is not the planning-stage angle [BUILD-NEWBUILDS.md](BUILD-NEWBUILDS.md) specced. That campaign's own creative is still unshot.

---

## 5. Open, in priority order

1. **⚠️ Matt: who answers the phone, and what does voicemail say?** Highest priority and it is not an Ads Manager setting. The calls ads put a Call Now button in front of Gold Coast homeowners six days a week; a rung-out phone is a paid click with no record it happened. The Mon–Sat 9–6 schedule mitigates it, it does not solve it.
2. **Publish the three drafts.** Hunter.
3. **SMS verification on the New Builds instant form.** Meta offers it in the duplicate dialog claiming +27% lead quality. Left off deliberately — it changes a live form's flow, which is a decision not a side effect. Recommended: turn it on. That campaign's documented problem is junk leads at $126 each, and this is the closest available substitute for the qualifying questions the form doesn't have.
4. **4:5 crops** on all three videos, checked frame by frame against the caption safe zone.
5. **Min job value from Matt** — outstanding since 29 Jul, still sets the kill thresholds.
6. **Business Manager admin bump** — outstanding since 29 Jul. Not on the critical path for an on-Facebook calls campaign, blocks everything after it.

---

## 6. Review calendar

- **Day 0, +2h** — ads Active not Rejected. Ring 0427 593 990 yourself; it tests the actual product, which is Matt's phone.
- **Day 2** — did it spend the full $20? Short means the goal or audience is too tight. Change one thing.
- **Days 3–6** — hands off. Editing restarts learning.
- **Day 7** — cut the weaker of the two calls ads on **link CTR** (~1% floor against the ~1.68% AU baseline) and 3-second views. **No cost decisions yet.** Also pull *Breakdown → By Time → Hour of day* to check the schedule is landing where it should.
- **Day 14** — ask Matt how many calls were real jobs. If they're all four-second hang-ups, that's the missing duration goal, not the creative.
- **Week 3** — cost per call means something. Set a cost cap with real data. Scale the survivor.
- **Throughout** — judge on jobs quoted, not calls received, and compare quality against Aircon Push running on the old settings. Same account, same brand, same audience, different settings: whatever the difference is, it's the settings. That's why the control is back on.

---
_Vault: [[mvx-electrical]] · [BUILD-CALLS.md](BUILD-CALLS.md) · [BUILD.md](BUILD.md) · [ACCOUNT-SETTINGS.md](ACCOUNT-SETTINGS.md) · method: [[paid-ads-diagnostic-rulebook]]_
