# MVX Meta — account-wide settings

**Date:** 2026-07-29 · **Updated:** 2026-08-10 · **Status:** all three settled

Three settings were specified differently in [BUILD.md](BUILD.md) and [BUILD-NEWBUILDS.md](BUILD-NEWBUILDS.md). That's a bug rather than a difference of opinion, because these are **account-level truths about MVX's service area and audience** — they can't correctly be ON in one campaign and OFF in another for the same business. This file is the single source for them; both build sheets defer here.

| Setting | BUILD.md said | BUILD-NEWBUILDS said | Resolved |
|---|---|---|---|
| Location setting | People living in this location | People living in this location | **Living in. Locked.** |
| Advantage+ audience | OFF | ON | **ON.** Hunter's call, 10 Aug 2026 — locked account-wide |
| Advantage+ placements | Manual, no Audience Network | ON | **ON** |

---

## Locked: location = "People living in this location"

Both sheets already agree, and this is the one that actually caused the damage. Meta's default is *"living in or recently in"*, which includes visitors and anyone who passed through — which is how a Gold Coast + Northern NSW campaign produced leads from Liverpool and Canberra, roughly a third of the total.

Costs nothing, fights nothing, non-negotiable on every MVX campaign.

---

## ⚠️ Correction: Advantage+ audience was probably not the cause of the out-of-area leads

[BUILD.md](BUILD.md) lists Advantage+ audience among the reasons the aircon campaign reached 3.8–4.5M against a ~700k service area, and prescribes OFF. That attribution is shaky and worth correcting before it drives another decision.

**Advantage+ audience can go beyond the interests, age and gender you specify. Location is a hard boundary it does not cross.** So the Sydney and Canberra leads are almost certainly the *location dropdown* — the setting locked above — not audience expansion. [BUILD-NEWBUILDS.md](BUILD-NEWBUILDS.md) makes exactly this argument and has the better analysis of the two.

Which means: the geo problem is already fixed by the locked setting, and Advantage+ audience is a separate, lower-stakes question that was never the root cause.

### Resolved 10 Aug 2026: ON

Hunter's call, taken when the General Electrical calls campaign was built ([BUILD-CALLS.md](BUILD-CALLS.md)). **ON, account-wide, every campaign.** The reasoning below stands as recorded; the recommendation was ON and it was accepted. The geo is hard-locked, so expansion cannot reach another state, and the quality lever now sits in the performance goal — call *duration* on the calls campaign, cost-per-result target elsewhere.

### The decision as it was framed

**The argument for ON** — Meta needs room to find people, especially on $20–40/day. Post-Andromeda, broad-within-a-locked-geography genuinely outperforms hand-built interest stacks, and BUILD-NEWBUILDS notes it worked on Brian's [[strategic-investing-qld]] campaign, which converted.

**The argument for OFF** — a wider audience on a *Maximise number of leads* goal finds cheaper form-fillers, and cheap form-fillers are precisely MVX's documented failure: 13 leads, most of them small jobs or price-shoppers. Widening the net while optimising for volume is how that happened.

**Worth noting the Strategic Investing analogy is weaker than it looks.** That's property advisory — the audience is genuinely wide and not geographically bounded in the same way. MVX is a hard geo-bounded trade whose failure mode is lead *quality*, not lead volume. What worked there doesn't automatically transfer.

**Recommendation: ON, with the quality lever held elsewhere.** The geo is now locked, so expansion can't reach another state, and the tool for lead quality is the **cost-per-result goal** already specced in BUILD.md — telling Meta not to chase the floor — plus the qualifying questions in the form. Those are the right levers. Narrowing the audience on a small budget spends the same money on fewer people, which is the classic way a small lead campaign never leaves learning.

⚠️ Either answer is defensible. **The thing that isn't defensible is different answers in different campaigns**, because then a quality difference between the two tells you nothing. Pick one, apply it everywhere, write it here.

---

## Resolved: Advantage+ placements ON

BUILD.md specified manual placements with Audience Network excluded — the quality-first setting, and a reasonable instinct, since Audience Network is where cheap junk impressions live.

Going with **ON** for two reasons. Meta's delivery is materially more efficient with placements open, which matters most at exactly this budget. And as of the [29 Jul video shoot](../mvx-creatives/MVX-Video-Shoot-Brief.pdf) the creative is **9:16 vertical video built for Reels and Stories** — the placements Advantage+ will favour and the ones manual selection was going to include anyway.

If junk impressions show up in the placement breakdown at day 7, that's the point to reconsider, with data rather than in advance.

---

## Still per-campaign, deliberately

Not everything should be unified. These stay campaign-level and the build sheets remain authoritative:

- **Budget and structure** — hot water runs 5 ad sets with $5 floors at $40/day; new builds runs 1 ad set at $20/day. Different tests, deliberately.
- **Conversion location, performance goal, cost-per-result target** — offer-specific.
- **The form and its qualifying questions** — a hot water budget band and a new-build project type are not the same filter.

⚠️ **Total daily spend across all MVX campaigns.** Hot water at $40/day plus new builds at $20/day plus anything for general electrical is $60+/day against two old campaigns that spent ~$541 over 30 days between them, or about $18/day. **Partly answered 10 Aug:** General Electrical (Calls) is approved at **$50/day** — but that is a number for one campaign, not an account ceiling, and hot water and new builds are both still unbuilt with their own budgets specced. The account-wide ceiling is still unset, and the aircon control's actual daily spend needs reading off the account rather than assumed.

---

_Vault: [[mvx-electrical]] · [BUILD.md](BUILD.md) · [BUILD-NEWBUILDS.md](BUILD-NEWBUILDS.md) · [MATT-ASKS.md](MATT-ASKS.md)_
