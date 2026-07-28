# MVX Meta Rebuild — build sheet

**Date:** 2026-07-28 · **Goal:** fewer, better leads. Not cheaper leads.
**Why rebuild rather than edit:** Meta locks conversion location and performance goal after an ad set publishes, so the existing two campaigns can't be corrected. Delete both, start clean.

## What went wrong (so we don't repeat it)

| Setting | Was | Why it produced junk |
|---|---|---|
| Performance goal | Maximise number of leads | Tells Meta "find people who'll fill a form", so it hunts the cheapest form-fillers on the platform |
| Audience size | 3.8–4.5M | Gold Coast + Northern NSW is ~700k. Reached 5× the service area — that's the Sydney and Canberra leads |
| Advantage+ audience | On | Widens past your targeting whenever cheaper fills exist |
| Instant form | Full prefill, no qualifiers | Name, email, phone in one tap. No thought, no commitment |

Result across 30 days: 13 leads, ~$541 spent, roughly a third outside the service area and most of the rest small or price-shopping jobs. One genuinely good lead (3-phase, ducted Daikin, solar + battery, asked for a quote) came in through **ducted aircon**.

## Campaign structure

One campaign. One ad set. Four ads.

Brian's account tested angle-per-campaign and killed four of six. Same principle here, simpler structure: put the four angles as four **ads** in one ad set so the learning pools instead of fragmenting across four budgets. Meta allocates to the winner, we kill the losers after a week.

```
Campaign:  MVX | Aircon | Qualified Leads | Aug 2026
  Objective:        Leads
  Budget:           $20/day, campaign level (CBO)
  Ad set:           Gold Coast + Northern NSW
    Conversion:     Instant forms          ← cannot be changed later, get it right now
    Ads:            4 angles (below)
```

## Ad set settings

- **Conversion location:** Instant forms
- **Performance goal:** Maximise number of leads, **with a cost-per-result goal of $60**. Counterintuitive but deliberate: leaving it at "None" tells Meta to chase the floor, which is how we got $27 tyre-kickers. A higher target lets it bid for better people. **Once Lach's call tracking is live and lead statuses feed back, switch to "Maximise number of conversion leads"** — that's the real fix and it needs the data first.
- **Location:** Gold Coast + Tweed Heads / Northern NSW. Set to **"People living in this location"**, not "living in or recently in".
- **Age:** 30–65+. Under 30 rarely owns the house.
- **Advantage+ audience:** **OFF.** Use original audience options so the geo actually holds.
- **Placements:** Manual. Facebook feed, Instagram feed, Reels, Stories. Audience Network stays excluded.
- **Detailed targeting:** none. Broad within the locked geography is correct post-Andromeda; the filtering job belongs to the creative and the form, not to interests.

## The instant form — this is where quality is won

Name it `Aircon Enquiry | Qualified | Aug 2026`.

**Intro screen** (does half the filtering):
> **Aircon supplied and installed, by licensed electricians**
> A few quick questions so we can price it properly. We supply and install complete systems, so we're not the cheapest option in town and we don't pretend to be.

**Questions, in this order:**
1. **Are you supplying the unit, or do you need us to supply and install?**
   - I need supply and install
   - I already have the unit
   - Not sure yet
2. **What do you need?**
   - New split system installed · Replace an old system · Ducted system · Repair · Service and clean
3. **Roughly what's your budget?**
   - Under $2,000 · $2,000–$4,000 · $4,000–$8,000 · $8,000+ · Not sure
4. **Suburb** — short answer, not postcode
5. **Name** — prefill allowed
6. **Phone** — **prefill OFF.** Making someone type their own number is the single cheapest quality filter available.

Drop the email field. Drop the free-text "tell us about the job" box — people wrote essays and it doesn't change whether Matt calls.

**Completion screen:**
> **Got it. We'll call you today.**
> One of our licensed electricians will ring the number you gave us. If you'd rather not wait, call 0427 593 990.

⚠️ Turn **on** "Review your info" before submit. Extra friction is the point.

## The four ad angles

Simple, one message each, real photos, no hype. Black and white with green on the CTA only, ≤10% of the frame. Per brand: plain English, proof first, no urgency.

**1. Scope filter: we supply and install** *(the main filter)*
> We supply and install complete aircon systems, Gold Coast and Northern NSW.
> One crew handles the unit, the circuit, the install and the compliance certificate. Fixed price agreed before we start.

No price in the ad. **Scope** does the filtering instead: saying plainly that MVX supplies *and* installs tells the "I've already bought the unit off the internet, just fit it" crowd this isn't for them, without quoting a number that invites comparison shopping or goes stale.

**2. We are the electricians** *(the differentiator already proven on the landing page)*
> Every aircon install needs licensed electrical work. Aircon-only shops subcontract it. We are the electricians, so nothing gets handed to a second trade.

**3. Real job proof** *(brand guide: content leads with proof)*
> 15 years on Gold Coast jobs. Photo of an actual install, tidy pipework, clean finish.
> Supply, install, certify. Done as promised.

**4. Ducted and bigger jobs** *(chase the one good lead we got)*
> Ducted systems and whole-home installs, Gold Coast and Northern NSW.
> Three-phase, switchboard work, solar and battery interaction — the jobs that need an actual electrician, not just an installer.

Angle 4 exists because the only high-value lead in the last 30 days came through ducted. Worth its own ad.

## Kill rules

- Review at **day 7**.
- Kill any ad over **$80 per lead**, or any ad producing leads that fail the budget question.
- Kill the whole angle if it only produces "I already have the unit" and "Under $2,000".
- Scale the survivor to $40–45/day, which is where Brian's winner sits.
- Judge on **jobs quoted**, not leads. A week of 4 good leads beats 10 junk ones.

## Assumptions to correct before launch

1. **Minimum job value** worth Matt's time. It sets the budget bands and the kill rules.
2. Ask Matt which of the last 11 leads he'd actually have wanted. That answer defines "quality" better than anything we can infer.

**No pricing in any ad** — Hunter's call, 28 Jul. Public numbers invite comparison shopping, date instantly, and pull the exact bargain-hunter audience we're trying to filter out. Qualification happens through **scope** in the ad and the **budget band** inside the form, where it's private.

## Sequence

1. Delete both existing campaigns (General Electrician $89/lead, Aircon Push)
2. Build the form first, the ad set second, the four ads last
3. Launch at $20/day
4. Lach's call tracking lands → switch the performance goal to conversion leads
5. Then, and only then, rebuild Google

---
_Vault: [[mvx-electrical]] · method: [[paid-ads-diagnostic-rulebook]] · proven pattern: [[strategic-investing-qld]]_
