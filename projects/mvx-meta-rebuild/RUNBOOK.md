# MVX General Electrical (Calls) — Ads Manager runbook

**Date:** 2026-08-10 · Click-by-click build for [BUILD-CALLS.md](BUILD-CALLS.md). Do the phases in order; Phase 0 is not optional.
Files staged and renamed at `~/Desktop/MVX ads stuff/ready to upload/` — `GE-List.mp4`, `GE-WholeList.mp4`, `GE-Renos.mp4`.

Two settings in here cannot be changed after publish: **conversion location** and **performance goal**. Everything else is editable. Slow down at Phase 2.

---

## Phase 0 — before Ads Manager opens (~15 min)

**0.1 — Baseline the account, or the whole comparison is lost.**
Ads Manager → date range **Last 30 days** → columns *Performance*. Screenshot the campaign rows for **Aircon Push** and **General Electrician**: spend, results, cost per result, impressions. Save to `projects/mvx-meta-rebuild/baseline-2026-08-10.png`.

Do this first, before pausing anything. Once General Electrician is off, its 30-day trailing numbers start decaying and the "did the new settings beat the old ones" question gets unanswerable. This is the step that gets skipped and then regretted.

**0.2 — Pause General Electrician.** Toggle off at campaign level. **Do not delete** — it is the reference for what the symptom-led angle did (3 leads / $89 / 30 days). Two live campaigns on the same offer bid against each other in the same auction and muddy the read.

**0.3 — Leave Aircon Push running.** Untouched. It is the control and the only thing producing.

**0.4 — Verify the phone number on the Page.**
Meta Business Suite → Settings → Business assets → Pages → MVX Electrical → **Page details** → phone `0427 593 990`. If it shows unverified, verify it now — the ad set will not publish without a verified number on a Calls conversion location, and discovering that at Phase 2 means rebuilding.

**0.5 — Ask Matt the phone question.** Text, one line, doesn't need a meeting:

> Quick one before these ads go live — the ads have a Call Now button so people will ring you direct. Are you right to answer through the day, and does your voicemail say MVX if you can't?

A missed call on a Call Now ad is a paid click with no record it happened. Launching before he answers is a decision to accept that, which is fine — just make it on purpose.

---

## Phase 1 — campaign (~2 min)

Ads Manager → **+ Create** → objective **Leads** → Continue.

Buying type: **Auction**. Campaign name:

```
MVX | General Electrical | Calls | Aug 2026
```

- **Special ad categories:** none. (Electrical services is not credit, employment, housing, social issues or politics.)
- **Campaign budget optimisation / Advantage campaign budget:** **ON**
- **Daily budget:** `$50.00`
- **Budget scheduling:** off
- **Campaign bid strategy:** Highest volume
- **A/B test:** off

Next.

---

## Phase 2 — ad set (~8 min) — ⚠️ THE IRREVERSIBLE PHASE

Ad set name:

```
General Electrical – GC + Northern NSW – Calls
```

**2.1 — Conversion location: `Calls`.**
Top of the ad set panel. Options are Website / Instant forms / Instant forms and Messenger / Messenger / Calls / App. **Pick Calls.** This is locked at publish.

**2.2 — Phone number.** Select `0427 593 990` from the dropdown. If it isn't there, Phase 0.4 didn't take.

**2.3 — Performance goal: `Maximise number of quality calls`.**
Also locked at publish, and this is the entire quality strategy — a quality call is one that lasts past ~60 seconds, so Meta only books a result when someone actually described a job. The alternative, *Maximise number of calls*, optimises for the tap and will find you people who hang up in four seconds. That is the exact failure the last campaign had, in a new costume.

⚠️ **If "quality calls" isn't in the dropdown** — it gates on account volume — then: choose *Maximise number of calls*, and set **Cost per result goal = `$45`**. Leaving it empty tells Meta to chase the floor. Note in the JOB/log which one you used, because it changes how day 14 reads.

**2.4 — Cost per result goal:** leave **empty** if you got the quality-calls goal. New event type, no baseline; a made-up target on an unknown event just throttles delivery. Revisit at day 14 with real numbers.

**2.5 — Budget & schedule.** Nothing to set — budget lives at campaign level. Start date today, **no end date**. Ignore the dayparting section: it's greyed out on a daily budget and that's expected (see BUILD-CALLS.md).

**2.6 — Audience.**

| Field | Set to |
|---|---|
| Locations | **Gold Coast** + **Tweed Heads / Northern NSW** |
| Location dropdown | **People living in this location** ← not the default |
| Age | 30 – 65+ |
| Gender | All |
| Detailed targeting | **empty** |
| Advantage+ audience | **ON** |
| Languages | leave blank |

The location dropdown sits *under* the map and defaults to "living in or recently in". That default is what produced the Liverpool and Canberra leads. It is one click and it is the highest-value change on the page.

**2.7 — Placements:** **Advantage+ placements ON.**

**2.8 — Before clicking Next, screenshot the ad set panel.** Conversion location and performance goal both visible in frame. This is the proof that the two locked settings were right, and it takes four seconds.

---

## Phase 3 — the three ads (~15 min)

Build the first one completely, then use **Duplicate** for the other two and swap the video, name and copy. Building three from scratch is three chances to leave creative enhancements on.

### Every ad, identical:

- Identity: Facebook Page **MVX Electrical**, Instagram account linked
- Format: **Single image or video**
- Call to action: **`Call Now`**
- Destination: the phone number (auto-filled from the ad set)
- ⚠️ **Advantage+ creative → OFF.** Both *text improvements* and *visual improvements*. These default ON and they live in a collapsed section — expand it. Meta rewrites the copy per placement and re-crops the frame, and these are 9:16 with deliberate caption safe zones, so a re-crop cuts the captions. This is per-ad, not per-ad-set: check it three times.
- Do **not** add music, do **not** accept a suggested thumbnail change

### Ad 1 — `GE-List`
Video: `GE-List.mp4` (10.1s)

| Field | Copy |
|---|---|
| Primary text | Everyone's got a list. The fan that stopped, the powerpoint hanging out of the wall, the downlight that's been out since Christmas. Licensed electricians, Gold Coast and Northern NSW — we'll do the lot in one visit, and tell you straight what needs doing and what doesn't. |
| Headline | Get The Whole List Done |
| Description | Gold Coast & Northern NSW |

### Ad 2 — `GE-WholeList`
Video: `GE-WholeList.mp4` (12.3s)

| Field | Copy |
|---|---|
| Primary text | If you're getting a sparky out anyway, you may as well get the whole list done while he's here. Fans, lights, powerpoints, switchboards, safety switches, data — all of it's us, so it's one trade and one visit. |
| Headline | One Visit, One Trade |
| Description | Licensed. Gold Coast & Northern NSW |

### Ad 3 — `GE-Renos`
Video: `GE-Renos.mp4` (15.2s)

| Field | Copy |
|---|---|
| Primary text | Changing your plans around the house? MVX does the electrical — including renovations. Licensed electricians, Gold Coast and Northern NSW. Give us a call and we'll tell you what it takes. |
| Headline | Electrical, Including Renovations |
| Description | Gold Coast & Northern NSW |

---

## Phase 4 — pre-publish check (~3 min)

Read this list against the screen, not from memory.

- [ ] Conversion location reads **Calls**
- [ ] Performance goal reads **quality calls** (or *calls* + $45 cost cap, and it's written down which)
- [ ] Location dropdown reads **People living in this location**
- [ ] Detailed targeting is **empty**
- [ ] Advantage+ audience **ON**, Advantage+ placements **ON**
- [ ] Campaign budget **$50/day**, CBO on, ad sets carry no budget of their own
- [ ] Three ads, three different videos, three different names
- [ ] Text improvements **OFF** on all three
- [ ] Visual improvements **OFF** on all three
- [ ] CTA button is **Call Now** on all three
- [ ] No pricing anywhere in any of the copy
- [ ] Preview each ad in **Facebook Reels** and **Instagram Stories** — confirm the burned-in captions aren't sitting under Meta's own UI chrome

Then **Publish**.

Expect a warning about the budget relative to the cost of an optimisation event. Publishing through it is the decision, not an error.

---

## Phase 5 — what you do afterwards, on which day

**Day 0, +2 hours.** Ads in review. Check status is **Active**, not Rejected. A rejection on a trade-services video is unusual, but if it lands, read the specific policy — do not resubmit blind.

**Day 0, one test call.** Ring 0427 593 990 from your own phone. Confirm it rings the right handset and someone or something answers. This tests the actual product, which is Matt's phone, not the ad.

**Day 2 — spend check, 5 min.** Did it spend the full $50 on day 1? A new conversion location under-delivering means the goal or the audience is too tight. If it came in materially short, the first lever is the *quality calls* goal → fall back to *calls* + $45 cap. **Change one thing.**

**Days 3–6 — hands off.** Every edit to an ad set restarts learning and wastes the spend that bought it. The most common way a small budget dies is being adjusted every second day.

**Day 7 — creative read, 20 min.** Ad level, columns: impressions, link CTR, 3-second video plays, cost per result, results.

| Signal | Cut the ad if |
|---|---|
| Link CTR | under ~1% (AU baseline ~1.68%) |
| 3-second plays / thumbstop | bottom of the three by a clear margin |
| Cost per call tap | worst by a wide margin |

Cut the worst **one**. Leave two running. **No decisions on cost per quality call yet** — at $50/day that's a sample of a handful, and a single lucky call reads as a winner.

**Day 7, second thing — Breakdown → By Time → Hour of day (viewer's time).** If real spend is landing outside 7am–7pm, that's the evidence to switch the ad set to a lifetime budget and schedule it. Not before.

**Day 14 — quality read.** Ask Matt, in these words: *of the calls that came in, how many were real jobs?* If the answer is "all tyre-kickers", check the quality-calls goal actually applied before you touch a single ad — a wrong goal looks exactly like bad creative from the outside.

**Week 3 — economics.** Cost per quality call now means something. Scale the survivor. Compare lead quality against Aircon Push on the old settings: same account, same brand, same audience, different settings. Whatever the difference is, it's the settings — that's the whole point of leaving the control running.

---

## When to stop and think instead of adjusting

- **Zero calls after 3 days of full spend** → structural, not creative. [[paid-ads-diagnostic-rulebook]] Rule 1. Check the number is verified, check the ads are Active, ring it yourself.
- **Calls arriving but Matt says nobody's on the line** → the duration goal isn't applied, or it's misdials from an accidental-tap placement. Check placement breakdown.
- **Out-of-area calls** → the location dropdown reverted or was never set. It's the one that caused this last time.

---
_Vault: [[mvx-electrical]] · spec: [BUILD-CALLS.md](BUILD-CALLS.md) · account-wide: [ACCOUNT-SETTINGS.md](ACCOUNT-SETTINGS.md)_
