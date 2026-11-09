# D Seated: hook variants (Nov 9, 2026)

D Seated 30s is the only ad so far with a sale: $44.81 spent, 5.96% link CTR, $0.83 CPC, 1 purchase.
These versions keep the body and ending exactly as they are and change only the first ~3 seconds,
so any difference in results comes from the hook. Same seated presenter, same voice, same cutaways.

**Locked body (unchanged in all three, from "It's called Trivelle"):**
> It's called Trivelle, and it does four things in one. Gentle heat, so it feels like a warm massage. Red light, for that glowy, radiant look. EMS, which feels like tiny little pulses, for a toned, firmer feel. And a vacuum massage through this head here, for skin that looks smoother. There's a little screen so you can see your mode and level. I just pop on some gel and do about ten minutes, a few nights a week, while I watch telly.

**Updated close (all three):**
> It's a hundred and sixty-nine dollars, free shipping, and there's a thirty-day money-back guarantee, so you can try it yourself.

Saying the price filters out clicks that would never buy at $169.

---

## D2: Salon swap
**Frame 0:** cold open on the stomach shot with red light ON (v7-stomach-red), then cut to the presenter at 1.0 s.
**VO hook:** "This is what I use instead of the salon now."
**Caption:** INSTEAD OF THE SALON
**Bridge into body:** "…It's called Trivelle…"
**Why:** the strongest frame in the ad (the red glow) comes first, and the line makes a value comparison with no medical claim.

## D3: In front of the telly
**Frame 0:** presenter already gliding the device on her forearm on the couch, TV light on her face (use the seated plate, mid-glide).
**VO hook:** "Ten minutes, in front of the telly, a few nights a week. That's it."
**Caption:** 10 MINUTES · IN FRONT OF THE TELLY
**Bridge:** "It's called Trivelle…" (drop the later "while I watch telly" line so it isn't said twice)
**Why:** sells how easy it is. The target buyer (35–65) has the time objection, not the money one.

## D4: Comment reply
**Frame 0:** a comment bubble over the presenter: *"does this actually work?? 👀"* (a generic made-up commenter, not a real person's name or photo).
**VO hook:** "Okay, does it actually work? Here's what it does, and here's what it doesn't."
**Caption:** DOES IT ACTUALLY WORK?
**Extra line before the close:** "It's not surgery and it won't work miracles. It's a nice ten-minute routine, and my skin looks smoother for it."
**Why:** builds on what already worked ("a few of you asked…"). Being honest about the limits makes it more believable and keeps the claims safe.

---

## Production
- Reuse `device-v2/ugc-02-seated-v2.mp4` and the existing cutaways. Re-edit with `scripts/build_ads_v2.py`: new VO keys `seated-d2/d3/d4`, everything else the same.
- New VO needed: hook line + new close only (~6–8 s each). Same voice as the original.
- Export 30 s and 15 s cuts of each, 9:16.
- **Cost:** ~150 cr each in the earlier estimate (ADS-IDEAS.md) → ~450 cr for all three. **Not spent yet: quote exactly before generating.**

## Test plan
- One ad set, optimised for **Purchase**, ~$15/day: D (original) + D2 + D3 + D4.
- After about $30–40 spend per ad: kill anything with link CTR under 2% or no add-to-cart. Keep the best one or two.
