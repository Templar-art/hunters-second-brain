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

A calls campaign therefore optimises for the *tap*, not the conversation. ✅ **Moot in the end** — the campaign became a form campaign (§3a), where *Maximise number of leads* is the correct and expected goal. Retained here because it stands as a permanent constraint on this account: **do not plan a calls campaign around call duration, it isn't available.**

**No cost cap was set, and that was a deliberate reversal.** The fallback plan was a $45 cost-per-result cap. A call *tap* likely costs $10–25, so a $45 cap binds on nothing; and if calls did run dearer it would throttle delivery on a campaign with no history. Still empty on the form version, same reasoning — set a cap at day 7 with real numbers behind it.

### Ad scheduling IS available on a daily budget — but only for calls campaigns

[BUILD-CALLS.md](BUILD-CALLS.md) said dayparting needs a lifetime budget. **Wrong — for a Calls conversion location.** A Calls ad set exposes *Ad scheduling → Set a schedule for ads* on a plain daily CBO budget, and Meta itself recommended it: *"You could get 25.4% more call conversions by running ads during your business hours."* It was set to Mon–Sat 09:00–18:00 Brisbane.

⚠️ **The option disappears on Instant forms.** Switching conversion location removed the whole Ad scheduling section, so the final campaign runs 24/7. **No loss** — the schedule existed only to stop the phone ringing when nobody could answer, and a form doesn't care what time it lands. Worth knowing as a rule: **dayparting on a daily budget is a calls-campaign privilege.**

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
| 3 | **MVX – General Electrician – Aug → OFF** | 1 lead at $125. Replaced by the new General Electrical campaign |
| 4 | MVX – New Builds & Renos – Aug | **Left running**, $20/day, untouched |
| 5 | General Electrician \| July | Left off |

Nothing was deleted. Every paused campaign is still there for reference.

### Drafts built, not published (Hunter presses Publish)

**New campaign — `MVX | General Electrical | Leads | Aug 2026`**

⚠️ **This was first built as a *calls* campaign and then rebuilt as a *form* campaign later the same day.** Reason and consequences in §3a below; the reasoning trail for the calls version is kept there deliberately, because the decision reversed on new information rather than on a mistake.

```
Objective            Leads
Conversion location  Instant forms      ← locks at publish
Performance goal     Maximise number of leads
Cost per result goal empty, deliberately
Budget               $20/day, campaign level (CBO)
Instant form         General Electrician Enquiry | MVX | August 2026 (existing)
                     with "Call Matt Directly" additional action retained
Schedule             none — runs 24/7 (dayparting is calls-only, see §3a)
Locations            Gold Coast +17 km QLD; Byron Bay +40 km NSW
"Reach more people likely to respond"   UNTICKED
Minimum age          25
Detailed targeting   none
Advantage+ audience  ON     (account-wide decision, Hunter 10 Aug)
Advantage+ placements ON
Ad set               1 · Ads 2
```

- **`GE-List`** → MVX Ad 3 (10.1s) · headline *Get The Whole List Done* · description *Gold Coast & Northern NSW.*
- **`GE-WholeList`** → MVX Ad 2 (12.3s) · headline *One Visit, One Trade* · description *Licensed. Gold Coast & Northern NSW.*
- Both: CTA **Get quote**, multi-advertiser ads off, all Advantage+ creative enhancements off, no AI creative
- Both primary texts rewritten to end on *"tell us what's on the list and we'll come back to you"* rather than pointing at a phone

**New ad in the existing campaign — `NB-Renos-Video`**

Inside `MVX – New Builds & Renos – Aug 2026`. **No budget or targeting change to that campaign** — a new ad only, so the ad set's 13 days of history stays intact.

- MVX Ad 1 (15.2s), the renovations cut
- Headline *Send Us Your Plans* · description *Free quote on your build. Gold Coast & Northern NSW.* · CTA **Get quote**
- Same `New Home & Renos | MVX | August 2026` instant form as the existing ad, with its "Call Matt Directly" action intact
- Multi-advertiser ads off · all four Advantage+ creative enhancements off (video touch-ups, text improvements, relevant comments, enhance CTA) · no AI images

**Total after publish: $50/day** — Aircon Push $10 + New Builds $20 + General Electrical $20. Approved by Hunter, 10 Aug. Note the third ad, `NB-Renos-Video`, costs nothing extra: it rides on New Builds' existing $20.

---

## 3a. Why the calls campaign became a form campaign

**The trigger:** Hunter, on being told the campaign put a Call Now button in front of Gold Coast homeowners — *"wouldn't a form be better cause he is bad at answering the phone?"* That is decisive information that wasn't available when the calls version was specced, and it inverts the logic.

**The argument.** A calls campaign makes Matt's phone habits the product. Every dollar buys a ring, and a missed ring is a paid click that leaves **no name, no number, no record** — nothing to follow up and no way to even know it happened. A form lead sits in the inbox until he gets to it. Against an owner who doesn't reliably answer, a mediocre form beats a good call every time.

**Timing was the whole reason this was cheap.** Conversion location locks at **publish**, not at build. The campaign was still a draft, so the switch cost nothing. An hour later it would have meant a full rebuild.

**What was kept:** the form retains its **"Call Matt Directly"** additional action, so anyone who'd rather ring still can. The choice was never call-or-form; it was which one is the *default*.

### What the switch cost

| Lost | Assessment |
|---|---|
| Mon–Sat 09:00–18:00 schedule | **No real loss.** Ad scheduling on a daily budget is a calls-only feature — it vanished from the ad set on switching. But the only reason for that schedule was to stop the phone ringing when nobody could answer. A form doesn't care what time it arrives. 24/7 is now correct |
| Creative on both ads | ⚠️ **Real cost.** Switching conversion location **silently wiped the video and all copy from both ads.** No warning. Both were rebuilt from scratch. **Lesson: set conversion location before building ads, never after** |
| Message match | ⚠️ Matt says *"give us a call"* on camera while the button reads *Get quote*. A genuine mismatch, accepted deliberately against the missed-call risk, and softened by the call action on the form |

### The WhatsApp ghost

After the switch, `GE-WholeList` refused to validate: *"WhatsApp number required: Reconnect your WhatsApp number to your Facebook Page or Instagram account to run this ad. (#2446880)"* — despite WhatsApp being unticked everywhere visible.

Cause: that ad was duplicated **while the campaign was still on Calls**, and the Calls destination panel carries a *"Call on WhatsApp"* option. The duplicate inherited a reference the form UI no longer displays and therefore can't clear. Fix was to delete the ad and re-duplicate from the already-rebuilt `GE-List`. **If a stale error survives every visible setting, the object is carrying state from a previous conversion location — rebuild it rather than hunt for the toggle.**

### The form: built, then discarded

A purpose-built form (`General Electrical - Qualified - Aug 2026`) was started with **Higher intent** (adds a review step) and **Flexible form delivery OFF** — that last one matters and is easy to miss: it lets Meta *remove your qualifying questions* to lift volume, which would silently delete the entire quality strategy.

Two things happened to it. First, Hunter challenged the opening question — *"why does it matter if you own the property, only people who own would be doing it"* — **and he was right.** Ownership is a hot-water qualifier, where a renter genuinely cannot authorise a $3k system swap. On a fan or a powerpoint it filters almost nobody, and property managers are legitimate buyers. It was swapped for a scope question. Then Hunter's call: **use existing forms.** The new form was discarded unsaved and `General Electrician Enquiry | MVX | August 2026` attached instead.

⚠️ **Live risk, stated plainly:** that is the same form the General Electrician campaign was running when it produced 1 lead at $125. The creative and the geo are materially different now, so this is not a like-for-like repeat — but **if week one produces junk again, the form is the first suspect, not the ads.**

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

**The CTA split is what decided the structure.** Two cuts say *call*, one says *send your plans*, so they could never share a campaign — the two "list" cuts went to General Electrical, the reno cut into the existing New Builds campaign whose form already matches its ask.

⚠️ **The split no longer decides the *mechanism*, only the grouping.** Both campaigns are now forms. The two "list" ads therefore say *"give us a call"* on camera while their button reads *Get quote* — a knowing mismatch, taken because Matt doesn't reliably answer the phone (§3a), and softened by the "Call Matt Directly" action on the form. **If those two are ever re-cut, change the spoken CTA to "tap below" or "send us your list."**

**The two project videos are not lead ads.** They end on scenery with no offer and no ask, and their subject is council/commercial work. In a lead campaign they would spend and return nothing. They belong on the Page and Instagram organically, and later as retargeting creative.

⚠️ **Setup B never happened — there is still no new-build site footage.** Ad 1 mentions renos inside a general-electrical body; it is not the planning-stage angle [BUILD-NEWBUILDS.md](BUILD-NEWBUILDS.md) specced. That campaign's own creative is still unshot.

---

## 5. Open, in priority order

1. **Publish the three drafts.** Hunter. Nothing is live; the account is running $30/day until he does.
2. **⚠️ Watch the form's lead quality specifically.** `General Electrician Enquiry | MVX | August 2026` is the same form that campaign ran when it made 1 lead at $125. Different creative and geo now, so not a repeat — but it is the first suspect if week one is junk. **Downgraded from "who answers the phone", which the switch to forms largely retired.**
3. **SMS verification on both instant forms.** Meta offers it in the duplicate dialog claiming +27% lead quality, and again inside the form builder as *"Require SMS verification to submit form"*. Left off deliberately — it changes a live form's flow, which is a decision not a side effect. Recommended: turn it on. Junk leads are the documented problem and this is the closest substitute for qualifiers these forms don't have.
4. **4:5 crops** on all three videos, checked frame by frame against the caption safe zone. Meta has auto-generated 1024×1280 crops in the library — **inspect before using, they were not reviewed.**
5. **Min job value from Matt** — outstanding since 29 Jul, still sets the kill thresholds.
6. **Business Manager admin bump** — outstanding since 29 Jul. Not on the critical path, blocks everything after it.

⚠️ **If the two "list" ads are ever re-cut**, change Matt's spoken CTA from "give us a call" to something form-shaped.

---

## 6. Review calendar

- **Day 0, +2h** — ads Active, not Rejected.
- **Day 0** — submit a test lead through the form yourself. Confirm it lands where Matt will actually see it. This is the equivalent of ringing the phone on a calls campaign, and it is the single cheapest check available.
- **Day 2** — did it spend the full $20? Short means the audience or goal is too tight. Change one thing.
- **Days 3–6** — hands off. Editing restarts learning.
- **Day 7** — cut the weaker of the two ads on **link CTR** (~1% floor against the ~1.68% AU baseline) and 3-second video views. **No cost-per-lead decisions yet** — the sample is too small to mean anything.
- **Day 14** — ask Matt how many were real jobs. If they're junk, look at the **form** first (item 2), not the creative.
- **Week 3** — cost per lead finally means something. Set a cost cap with real data. Scale the survivor.
- **Throughout** — judge on jobs quoted, not leads received, and compare quality against Aircon Push running on the old settings. Same account, same brand, same audience, different settings: whatever the difference is, it's the settings. That's why the control is back on.

---
_Vault: [[mvx-electrical]] · [BUILD-CALLS.md](BUILD-CALLS.md) · [BUILD.md](BUILD.md) · [ACCOUNT-SETTINGS.md](ACCOUNT-SETTINGS.md) · method: [[paid-ads-diagnostic-rulebook]]_
