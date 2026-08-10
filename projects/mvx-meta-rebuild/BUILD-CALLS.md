# MVX Meta — General Electrical (Calls) — build sheet

**Date:** 2026-08-10 · **Creative:** 3 talking-head cuts filmed 3 Aug · **Status:** ready to build, three items need Matt
**Decisions locked 10 Aug (Hunter):** conversion location **Calls** · budget **up to $50/day** · Advantage+ audience **ON**

Vault: [[mvx-electrical]] · scripts: [VIDEO-SCRIPTS.md](../mvx-creatives/VIDEO-SCRIPTS.md) · account settings: [ACCOUNT-SETTINGS.md](ACCOUNT-SETTINGS.md) · method: [[paid-ads-diagnostic-rulebook]]

---

## What actually got delivered from the shoot

Five files, three of them ads. Verified by frame extraction, 10 Aug.

| File | Length | Angle | Spoken CTA | Use |
|---|---|---|---|---|
| `MVX Ad 1.mp4` | 15.2s | "Best time to change your plans" → **"including renovations"** | "just give us a call" | **Ad — GE-Renos** |
| `MVX Ad 2.mp4` | 12.3s | "If you're getting a sparky out, get the whole list done" | "give us a call" | **Ad — GE-WholeList** |
| `MVX Ad 3.mp4` | 10.1s | "Everyone's got a list… out since Christmas" | "get in touch and I can help" | **Ad — GE-List** |
| `MVX Elec Green Power Boxes.mp4` | 47.9s | Commercial switchboard/pillar project | — | **Not an ad.** Organic. |
| `MVX Elec — Broadbeach Library.mp4` | 19.9s | Council library fitout | — | **Not an ad.** Organic. |

All three ads: 1080×1920, 30fps, same shirt, same location, burned-in captions, brand green on emphasis words only. They are interchangeable and they are all one angle — **General Electrical, the "list" frame** from VIDEO-SCRIPTS.md. That is a coherent campaign, not a gap.

**Two things that did not arrive:**

- **No New Builds & Renos footage.** Setup B (frame, bare studs, rough-in) never happened. `Ad 1` gestures at renovations inside the general-electrical body, which is not the same as the planning-stage angle in [BUILD-NEWBUILDS.md](BUILD-NEWBUILDS.md). **That campaign stays unbuilt** — it needs its own shoot day on an actual site. Do not launch it off Ad 1.
- **No 4:5 or 1:1 crops.** Everything is 9:16. With Advantage+ placements ON, Meta will pillarbox these into the feed. The captions sit mid-frame, so a centre 4:5 crop survives — worth exporting three 4:5 versions before launch if there's time, but not a blocker.

The two commercial pieces are the wrong audience for this campaign — a homeowner with a dead downlight does not care about a council library. They belong on the Page organically, and later as retargeting creative if a commercial campaign ever gets built.

---

## The consequence of choosing Calls

This is the right call — the creative says "give us a call" three times out of three, and MVX's whole documented position is phone-first, the calls *are* the leads. But it moves where quality control lives, and that has to be handled deliberately.

**What we lose:** the instant form. Every qualifier specced in [BUILD.md](BUILD.md) — do you own the property, what's your budget band, what have you got now — was going to do the filtering privately, after the click. A call has no form. The filtering now has to happen in three other places:

1. **In the creative.** Already done, and this is why the "list" angle is the right one to run on Calls: it self-selects for someone with several small planned jobs, not a price-shopper on one emergency.
2. **In the performance goal.** See below — optimise for *call duration*, not call count. This is the single most important setting on the sheet.
3. **In Matt's first thirty seconds on the phone.** Which is a conversation to have with him, not a setting.

**What we gain:** no form to build, no form-abandon rate, and a lead that is already talking to the business. Meta's own data on trade services has calls converting to job at a materially higher rate than form fills, because the qualifying happens live.

⚠️ **A missed call is a wasted click, and there is no second chance at it.** A form lead sits in an inbox until Matt gets to it; a rung-out phone is gone. This is the one real risk of the Calls choice and it is a business-process risk, not an ad-settings one. It needs Matt's answer — see *Needs Matt* below.

---

## Campaign

```
Campaign:  MVX | General Electrical | Calls | Aug 2026
  Objective:              Leads
  Conversion location:    Calls            ← LOCKS AT PUBLISH. Check it twice.
  Campaign budget:        $50/day (CBO / Advantage campaign budget)
  Budget scheduling:      off
  Schedule:               ongoing, no end date
  Ad sets:                1
  Ads:                    3 (one per hook)
```

### Why one ad set with three ads, not three ad sets with floors

[BUILD.md](BUILD.md) specced five ad sets with $5/day minimum spend limits. **That structure does not carry over here, and this supersedes it for this campaign.**

The floors existed to guarantee each *angle* an independent cost-per-lead read. But these three cuts are not three angles — they are three hooks on one angle, with the body and CTA held constant, which is exactly what VIDEO-SCRIPTS.md built them to be. The comparison we need between them is **hook performance**, and hook performance is read through link CTR and thumbstop rate, both of which are impression-normalised. They do not need equal spend to be comparable. Cost per result does, and cost per result is not what these three are being judged on.

Splitting into three ad sets would fragment the audience, triple the time to fifty optimisation events, and buy nothing the ad-level report doesn't already give us. One ad set at $50/day concentrates the learning, and Meta's own rotation finding a winner among three is the desired outcome rather than a bug.

**Revisit this if** a genuinely different angle gets filmed (new builds, hot water). Different angles, different ad sets — that reasoning in BUILD.md was sound for the case it was written for.

---

## Ad set

Name: `General Electrical – GC + Northern NSW – Calls`

| Setting | Value | Note |
|---|---|---|
| Conversion location | **Calls** | Locks at publish |
| Performance goal | **Maximise number of quality calls** (call duration ≥ 60s) | See below — this is the quality lever |
| Cost per result goal | Leave **empty at launch** | Different event, no baseline. Revisit day 14 with real numbers |
| Phone number | 0427 593 990 | Must be verified on the Page before the ad set will publish |
| Location | Gold Coast + Tweed Heads / Northern NSW | |
| **Location setting** | **People living in this location** | Locked account-wide. The single fix for the Sydney/Canberra leads |
| Age | 30 – 65+ | |
| Gender | All | |
| Detailed targeting | **None** | Broad within a locked geo is correct post-Andromeda |
| Advantage+ audience | **ON** | Hunter's call, 10 Aug. Now settled account-wide — write it into ACCOUNT-SETTINGS.md |
| Advantage+ placements | **ON** | Per ACCOUNT-SETTINGS.md |
| Schedule | Ongoing | ⚠️ see dayparting below |

### The performance goal is the whole quality strategy

Meta offers two goals on a Calls conversion location:

- **Maximise number of calls** — optimises for the *tap*. This is the Calls-objective equivalent of "maximise number of leads", and it will reproduce MVX's exact documented failure: the cheapest available action, performed by the least committed person. Someone who taps and hangs up in four seconds counts as a result.
- **Maximise number of quality calls** — optimises for calls that last past a duration threshold (60 seconds on most accounts). Meta only counts the result if the person stayed on the phone.

**Use the duration goal.** A 60-second call is somebody describing a job. A four-second call is a misdial or a price question. This setting is doing the work the budget-band question was going to do on the form, and it is doing it better, because it measures behaviour instead of asking about it.

⚠️ If the quality-calls goal isn't available in the account, that is a delivery-volume gate on Meta's side. Fall back to *maximise number of calls*, and set a **cost-per-result goal of $45** so it isn't hunting the floor — the same logic as the $60 target in BUILD.md, scaled down because a call is a cheaper event than a form lead.

### Dayparting — a constraint, not an oversight

**Meta only allows ad scheduling on a lifetime budget, not a daily one.** A CBO daily budget runs 24/7. So a call ad will serve at 10pm, someone will ring, and nobody will answer.

Launching 24/7 on the daily budget anyway, deliberately, because:

- The hour-of-day breakdown from week one is the data that decides whether dayparting is even worth the lifetime-budget switch. Guessing at it now is guessing.
- Meta's delivery already skews to when people engage, and for a home-services call that skews toward waking hours without being told.

**Day 7: pull the hour-of-day breakdown.** If meaningful spend is landing outside 7am–7pm, switch the ad set to a lifetime budget and schedule it. That is a deliberate second step with evidence behind it, not a launch setting.

Interim, zero-cost: whatever Matt's phone does after hours needs to say something useful. A voicemail naming the business beats a rung-out phone.

---

## The three ads

One per hook. Body and CTA are constant across all three by design — the hook is the only variable, so a CTR difference between them means something.

**On every ad, before publishing:** Advantage+ creative enhancements **OFF** — both *text improvements* and *visual improvements*. Non-negotiable, and doubly so here: these are 9:16 frames with deliberate caption safe zones, and visual improvements re-crops. See [[paid-ads-diagnostic-rulebook]] Rule 8.

**Call to action button on all three: `Call Now`.**

### Ad 1 — `GE-List` (`MVX Ad 3.mp4`, 10.1s)

*Lead with this one. Purest version of the angle, shortest, strongest hook.*

| Field | Copy |
|---|---|
| Primary text | Everyone's got a list. The fan that stopped, the powerpoint hanging out of the wall, the downlight that's been out since Christmas. Licensed electricians, Gold Coast and Northern NSW — we'll do the lot in one visit, and tell you straight what needs doing and what doesn't. |
| Headline | Get The Whole List Done |
| Description | Gold Coast & Northern NSW |

### Ad 2 — `GE-WholeList` (`MVX Ad 2.mp4`, 12.3s)

| Field | Copy |
|---|---|
| Primary text | If you're getting a sparky out anyway, you may as well get the whole list done while he's here. Fans, lights, powerpoints, switchboards, safety switches, data — all of it's us, so it's one trade and one visit. |
| Headline | One Visit, One Trade |
| Description | Licensed. Gold Coast & Northern NSW |

### Ad 3 — `GE-Renos` (`MVX Ad 1.mp4`, 15.2s)

*The wildcard. Reaches wider than the other two by naming renovations.*

| Field | Copy |
|---|---|
| Primary text | Changing your plans around the house? MVX does the electrical — including renovations. Licensed electricians, Gold Coast and Northern NSW. Give us a call and we'll tell you what it takes. |
| Headline | Electrical, Including Renovations |
| Description | Gold Coast & Northern NSW |

⚠️ **No pricing in any ad.** Hunter's standing call, 28 Jul. Qualification happens through scope in the ad and call duration in the optimisation, never through a public number.

---

## Before this publishes

1. **Pause the old General Electrician campaign.** It was already scheduled for pausing on 28 Jul (3 leads / $89 / 30 days) and it has not been confirmed done. Two live campaigns on the same offer bid against each other and muddy the read. Pause, don't delete.
2. **Leave Aircon Push running, untouched.** It is the control and the only thing producing.
3. **Verify 0427 593 990 on the Page.** The ad set won't publish without it.
4. **Confirm conversion location reads *Calls* and performance goal reads *quality calls*** — screenshot both before hitting publish. Neither can be changed afterwards.
5. **Creative enhancements off on all three ads.** Check per-ad; it defaults on.
6. **Day 2: check actual spend against $50.** Under-delivery on a new conversion location is common and it means the audience or the goal is too tight.

---

## How to judge it

Adapted from BUILD.md's revised kill rules. Same principle: **creative signal at day 7, economics at week 3.** With three ads in one ad set the day-7 read is cleaner than it would have been across five ad sets, because all three share an audience and a budget.

**Day 7 — creative only. No cost decisions.**

| Signal | Cut if | Why it's readable now |
|---|---|---|
| Link CTR | Under ~1% against the ~1.68% AU baseline in [[paid-ads-diagnostic-rulebook]] | Thousands of impressions per ad at $50/day |
| 3-second video views / thumbstop | Bottom of the three by a clear margin | Pure hook performance, independent of call volume |
| Cost per call *tap* | Worst by a wide margin | Not the result metric, but a usable early proxy |

Cut the worst one. Leave two running. Do not cut on cost per *quality call* yet — at $50/day that is a sample of a handful.

**Day 7, separately — the hour-of-day breakdown.** Decides the dayparting question above.

**Day 14 — first quality read.** Ask Matt directly: of the calls that came in, how many were real jobs? If the answer is "they're all tyre-kickers", the problem is the goal (wrong optimisation) or the geo, not the creative — check the quality-calls goal actually applied before touching the ads.

**Week 3 — economics.** Cost per quality call is meaningful now. Scale the survivor.

**Throughout: judge on jobs quoted, not calls received.** Four good calls beats fifteen. This is the number Matt actually feels, and it is the number that decides whether the new settings beat the aircon control.

---

## Needs Matt — three things, and one of them is urgent

1. **⚠️ Who answers the phone, and what happens when nobody does.** This is now the campaign's single biggest failure mode and it did not exist under the form spec. Ask it plainly: is he answering during the day, is there a diversion, and does the voicemail say the business name. A rung-out phone on a Call Now ad is money set on fire with no record that it happened.
2. **Minimum job value worth turning up for.** Outstanding since 29 Jul ([MATT-ASKS.md](MATT-ASKS.md) item 8). Sets the cost-per-result target at day 14 and defines what "quality" means on the call review.
3. **Business Manager admin bump.** Outstanding since 29 Jul (item 6). Needed for the dataset and for domain verification — not on this campaign's critical path, since an on-Facebook call ad loads no website, but it blocks everything after it.

Items 2 and 3 do not block launch. **Item 1 does** — or rather, launching without it is a decision to accept the risk, which is Hunter's to make, not an oversight to discover in week two.

---

## What this leaves unbuilt, on purpose

- **New Builds & Renos** — [BUILD-NEWBUILDS.md](BUILD-NEWBUILDS.md). No footage. Needs setup B on a real site.
- **Hot Water** — [BUILD.md](BUILD.md). Still blocked on Matt's plumbing-licence answer, and no creative was filmed for it.
- **The landing-page form fix** — [FORM-FIX.md](../mvx-lead-fix/FORM-FIX.md). Unrelated to this campaign (call ads load no page), still outstanding, still needs WordPress access.

**Total MVX daily spend after this launches:** $50/day here + whatever Aircon Push is spending. That is the account-wide number ACCOUNT-SETTINGS.md flagged as unbudgeted — it now has a figure for the first campaign, and the aircon control's spend needs reading off the account rather than assumed.

---
_Vault: [[mvx-electrical]] · supersedes BUILD.md's five-ad-set structure **for this campaign only**_
