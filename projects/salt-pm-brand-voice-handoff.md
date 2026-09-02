# Salt PM — Brand Voice Handoff (for Lach)

**Purpose:** brief for building/prompting an IG caption assistant (chatbot) for Salt PM — Kingscliff property management + luxury holiday rentals. This is the voice spec to feed it; not the chatbot build itself.

- Site: [saltpm.com.au](https://saltpm.com.au)
- IG: [@saltpropertymgt](https://www.instagram.com/saltpropertymgt/) — 259 posts, 598 followers
- Full source scrub (bio + site copy + 9 sample posts, pulled 2026-09-02): `wiki/sources/salt-pm-brand-scrub.md`

## The account runs four caption formats — pick the right one before writing

**A. Landlord/authority post** (leasing results, market-leader claims)
- Data-led: cites a real number + timeframe + source when claiming a result.
- Structure: headline claim → 1–2 sentences on approach → soft CTA ("let's talk").
- Brand words: *considered*, *tailored*, *hybrid*, *local knowledge*, *investor-led*.

**B. Team/trust post**
- Introduces the people, not the property. Emphasizes a "considered approach," trusted advice, day-to-day care.
- Closes with a phone-number CTA, not a link.

**C. Listing template — For Lease / Leased** (the most rigid format)
- `For Lease |` or `Leased |` + address, suburb
- Price line: `$X,XXX per week`
- One plain descriptive sentence — bed count, standout feature, proximity to beach/amenity
- Optional spec line: `X Bedrooms | X Bathrooms | X Car Spaces`
- CTA: phone number, or nothing at all
- No emoji. No sensory language. Reads like an agent listing sheet, not "social" copy — don't over-write these.

**D. Holiday/lifestyle reel** — the most voice-driven, loosest format
- Scene-setting hook (sometimes "POV:", sometimes a short mood line).
- 1–2 sensory, present-tense sentences — a lifestyle moment, not property specs.
- A closing line that ties the feeling back to "a stay here" — vary the wording each time, this is a *pattern* to riff on, never a fixed line to reuse verbatim.
- 📍 + property/listing name as a location tag.
- Fixed CTA: "Book your stay via the link in bio."
- **Exception:** seasonal/local-interest reels (e.g. whale season) drop the booking CTA entirely — pure local-insider awareness content, no ask.

## Consistent across all four
- No hashtags, ever.
- No exclamation-heavy hype, no generic real-estate clichés ("dream home", "must see").
- Suburbs named specifically — Kingscliff, Casuarina, Cabarita — never just "the area".
- Emoji use is sparing and functional: 📍 for locations, one thematic emoji on seasonal posts, none on listings or authority/team posts.
- Posting cadence is frequent (5+ posts/week observed) and mixes formats rather than batching by type.

## Practical brief for the chatbot / whoever writes captions
1. Classify the post first: authority (A), team (B), listing (C), or lifestyle (D) — the four voices don't mix within one post.
2. Format C is closest to fill-in-the-blank — resist adding sensory language there.
3. Format D is where brand personality lives — but the "feeling → stay" closing line should be freshly written per post, not templated.
4. Never add hashtags or urgency/discount CTAs — absent from every sample reviewed.
5. Keep it short — nothing sampled ran longer than ~5 sentences total.

## Known gap
9 of 259 posts sampled (up from 2). That's enough to lock the four-format structure with confidence, but thin per-format if the chatbot needs a deeper few-shot set. There's no bulk export path available externally (Instagram's own API rejects unauthenticated bulk calls, and there's no scraping tool configured with its own login) — and pulling all 259 verbatim isn't something we should do regardless, since that's wholesale copying of their copyrighted copy rather than research notes. If more depth is needed, get a caption export from whoever has direct login access to the Salt PM account.

## Next step
Chatbot build not started — this doc is the voice spec input. Vault page for ongoing status: `wiki/clients/salt-pm.md`.
