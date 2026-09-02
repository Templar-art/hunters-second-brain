# Salt PM — Brand Voice Handoff (for Lach)

**Purpose:** brief for building/prompting an IG caption assistant (chatbot) for Salt PM — Kingscliff property management + luxury holiday rentals. This is the voice spec to feed it; not the chatbot build itself.

- Site: [saltpm.com.au](https://saltpm.com.au)
- IG: [@saltpropertymgt](https://www.instagram.com/saltpropertymgt/) — 259 posts, 598 followers
- Full source scrub (verbatim bio + site copy + 2 sample captions): `wiki/sources/salt-pm-brand-scrub.md`

## The account runs two registers, not one

**1. Landlord/investor posts** (leasing results, team, market updates)
- Data-led: cites a real number + timeframe + source when claiming a result (e.g. properties leased, "past 12 months", source + date range named).
- Structure: short headline claim → 1–2 sentences of substance → soft CTA.
- CTA is always a soft invitation ("let's talk", "connect with the team"), never a hard sell, never urgency/discount language.
- Recurring brand words: *considered*, *tailored*, *hybrid*, *local knowledge*, *investor-led*.

**2. Holiday/guest posts** (site's "Holiday mode" language — carries into the Holiday-tagged content)
- Coastal, sensory, laid-back: surf, gelato, lazy afternoons by the water.
- Local-insider framing (Tweed Coast guide, not generic travel copy).
- Brand phrase: "the good times and the long game" — captures both sides of the business in one line.

## Consistent across both registers
- No hashtags on post copy.
- No exclamation-heavy hype or generic real-estate clichés ("dream home", "must see").
- Suburbs named specifically — Kingscliff, Casuarina, Cabarita — never just "the area".
- Team warmth shown in comments/emoji reactions, not baked into the caption copy itself.
- Sign-off is a phone number or a question, not "link in bio".

## Practical brief for the chatbot / whoever writes captions
1. Identify which register the post is (landlord result vs holiday/lifestyle vs team/brand) before writing — the two voices don't mix in one post.
2. For landlord posts: lead with the number or result, name the source/timeframe if quoting one, keep the CTA soft.
3. For holiday posts: lean sensory and local, skip the data.
4. Never add hashtags or urgency CTAs — both are absent from every sample reviewed.
5. Keep captions short — samples ran 3–5 sentences total, no long-form storytelling.

## Known gap
Only 2 full captions were pulled verbatim for this pass (Instagram blocks bulk/API scraping without their own login, and pulling all 259 captions verbatim isn't something we should store wholesale anyway — it's their copyrighted copy). The two-register pattern above is well-supported by those 2 posts + the site's own copy, but if the chatbot needs a bigger few-shot set, the move is to have someone log into the Salt PM account directly (or get captions exported from them) rather than more scraping from outside.

## Next step
Chatbot build not started — this doc is the voice spec input. Vault page for ongoing status: `wiki/clients/salt-pm.md`.
