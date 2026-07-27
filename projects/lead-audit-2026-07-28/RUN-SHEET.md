# Lead Audit Session — Run Sheet

**When:** Tue 28 Jul 2026, ~4 hours · **Who:** Hunter + Claude
**Clients:** MVX Electrical · CVA Architects · 10x Visuals
**Goal:** not "understand the ads" — the diagnosis is already done (see [[mvx-electrical]], the 27 Jul entry in [[log]]). The goal is **three funded, tracked, live lead channels and a decision log**, ordered so the fastest money happens first.

## Read this before we start (5 min)

- 27 Jul diagnosis: `wiki/log.md`, bottom entry — why each client has no leads.
- [FORM-FIX.md](../mvx-lead-fix/FORM-FIX.md) — the MVX change list, ready to apply.
- [fb-ads-handoff.md](../fb-ads-handoff.md) — the 8 data points for the dead 10x campaign, still uncollected.

**The one thing that already worked:** Strategic Investing QLD, 10–15 leads in 4 business days. Everything tomorrow is either applying that pattern or unblocking a channel so it can be applied. Don't invent a new playbook.

---

## Timetable

### 0:00–0:20 — Open the taps (do this first or the whole session guesses)

- [ ] Google Ads open — MVX account, last 14 days, per landing page: impressions, CTR, cost/conv, **call conversions vs form conversions**
- [ ] Meta Ads Manager open — the 10x investment-leads campaign, and whatever ran for SIQ
- [ ] **Authorise the `10x-crm` MCP** (claude.ai connector settings) — without it Claude can't see real lead counts and we're reading tea leaves off websites again
- [ ] Screenshot the MVX baseline **before** any change (form entries + call conversions per page). Miss this and tonight's fix is unmeasurable forever.

### 0:20–0:35 — Extract the SIQ recipe (highest-value 15 min of the day)

Answer four questions, write them down:
1. Which asset ran — the 10 Jul mortgage-freedom ad kit, or something else? (the 23 organic posts are CTA-free, so they're not the driver)
2. Daily spend + campaign objective?
3. **Where did the leads land** — Meta instant form / website form / phone / DM?
4. What did the ad actually promise? (the offer, in one line)

→ This becomes the template stamped onto MVX, CVA and 10x. #3 is the transferable part.

### 0:35–0:50 — Call Matt (put the call early so the answer arrives before we need it)

Two questions only:
- **Hot water: does he sub or partner a licensed plumber?** QLD water side is licensed plumbing; MVX is electrical/ARC/solar/cabler. This gates the entire hot water build.
- Is he happy to fund a hot water campaign, and at what daily spend?

If he can't be reached: park hot water, note it, move on. Don't design around a guess.

### 0:50–1:20 — Apply the MVX form fix (live)

Straight down [FORM-FIX.md](../mvx-lead-fix/FORM-FIX.md): delete Email, Postcode → Suburb, message optional, keep the honeypot, strip nav from both LPs, fix the "your aircon" validation bug on the electricians form. Needs WP admin — Hunter or Lach, not Claude.

- [ ] Test lead submitted **from a real phone**, both pages, confirmed landing in Matt's inbox
- [ ] `tel:` click confirmed firing as a Google Ads conversion (this is the big one — phone-first page, the calls *are* the leads)

### 1:20–1:50 — MVX hot water: scope or park

Only if Matt said yes. Claude builds the page + campaign after the session; tomorrow just locks the decisions:
- Offer: heat pump + **STC rebate ~$998 as an upfront discount** (from ~$1,600 installed) vs straight electric-storage swap vs both
- Who does the plumbing, and does that change the promise on the page
- Emergency intent ("no hot water") vs planned upgrade intent — different keywords, different page, possibly both
- Daily spend + which suburbs

### 1:50–2:35 — 10x Visuals' own funnel (the embarrassing one)

We sell "Lead Gen" as a nav item from a site with **no lead form**, and spent ~$160 on Meta for zero leads.
- [ ] Decide the capture mechanism: Meta instant form (fastest, matches whatever worked for SIQ) vs a real page with a form
- [ ] Decide the **offer** — what does a real-estate/construction prospect *get* for their details? "Contact us" is not an offer.
- [ ] Decide: relaunch the investment-leads campaign, or kill it and rebuild on the SIQ pattern
- [ ] Fix the contact path — site currently sends everything to `tyson@` mailto + a phone number

### 2:35–3:10 — CVA Architects

- [ ] Confirm whether **any** ads exist (nothing observable from outside)
- [ ] Design the top-of-funnel offer — architects carry a 6–18 month consideration window, so "Begin Project" only catches the already-decided. Feasibility check / "what can I build on my block" is the shape.
- [ ] **Use the assets already paid for:** 19 stills + ~40 clips from the June job are sitting unused. That's a finished ad library. Get Cameron's OK to run them.

### 3:10–3:40 — Cross-client: stamp the pattern

One table, four rows (SIQ / MVX / CVA / 10x): offer · where the lead lands · daily spend · who owns follow-up · **how fast leads get called back**. Speed-to-contact is where "leads don't convert" usually actually lives — and we have no data on it for anyone. If a client is slow to call back, no ad fixes that.

### 3:40–4:00 — Close: decisions, owners, money

- [ ] Decision log written into the vault (Claude does this live)
- [ ] Every action has a name against it: Hunter / Lach / Claude / client
- [ ] **Spend sign-off explicit** — any ad budget, any Magnific/Higgsfield credits. Nothing paid runs without Hunter saying the number out loud.
- [ ] Claude's build queue for tonight/tomorrow, in order

---

## Ground rules for the session

- **Don't re-diagnose.** The 27 Jul findings are evidence-backed (live markup, sitemaps). Start from them.
- **Baseline before every change**, or improvements become unprovable.
- **Two failure modes stay separate:** *no leads* (channel/offer/capture broken) vs *leads don't convert* (follow-up speed, qualification, offer mismatch). Right now we have zero data on the second for any client — if that's the real problem, tomorrow should end with a way to measure it, not more ads.
- **Claude can't:** touch WP admin, log into ad accounts, handle credentials, or spend money. Everything else is fair game.

## Risks

- Matt or Cameron unreachable → hot water and CVA both stall. Mitigation: calls scheduled early, and the MVX form fix + 10x funnel don't depend on anyone else.
- 4 hours goes fast. If we're behind at the 2-hour mark, **protect the MVX form fix and the SIQ recipe** and push CVA to a separate session — those two are the money.
- `10x-crm` not authorised → the whole session runs on inference again.
