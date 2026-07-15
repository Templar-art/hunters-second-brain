---
client: strategic-investing-qld
address: n/a (social ad creative, not a property)
opened: 2026-07-10
status: review        # intake → generating → review → delivered
cost: { credits: 150, aud: 6 }
---

# Job — Strategic Investing QLD "Mortgage Gone in Under 10 Years" Meta ad kit

Property investment advisory (new client). Static FB/IG ad from supplied brief + brand guidelines (navy #132A43 / gold #B7893B / cream, Marcellus + Inter).

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 1 | Illustrated hero 1:1 | PIL vector (free) | done | siq-mortgage-ad-1080.png — duotone navy/gold illustration |
| 2 | Stock-photo hero 1:1 | Freepik stock via Magnific (0 cr) | done | siq-mortgage-ad-1080-photo.png — US-ranch look, superseded |
| 3 | Gen hero — QLD brick-and-tile | Nano Banana Pro 4:3 @2k ×2 | done | Option A picked (frontal, clean sky); B unused |
| 4 | Final kit 1:1 / 4:5 / 9:16 | PIL build_kit.py | done | siq-mortgage-ad-{1x1,4x5,9x16}.png, disclaimer in footer |

## Log

- 2026-07-10 intake: brief + brand guidelines pasted; illustrated v1 built (0 cr)
- 2026-07-10 stock: Freepik photo downloaded via Magnific MCP (0 cr), photo v2 built
- 2026-07-10 grill: decisions locked — gen Aussie lowset brick-and-tile hero, 3-format kit, keep invented label + CTA copy, add compliance disclaimer, placeholder logo (swap when client sends file)
- 2026-07-10 generation: Nano Banana Pro, 2 options, 150 credits (~$6 AUD) — Hunter approved before spend
- 2026-07-10 build: 3-format kit rendered; status → review (awaiting Hunter/client sign-off)
- 2026-07-10 revision: placeholder wordmark removed from top-right (Hunter), top scrim softened; kit re-rendered

## Open items

- [ ] Real logo file from client → swap placeholder, regenerate kit (one script run)
- [ ] Client compliance sign-off on headline claim + disclaimer wording

---

# Job 2 — Social Post Batch 1 (2026-07-15)

First social batch: 9 posts (IG-first, FB-adaptable), **20 PNG slides** @ 1080×1350.
Aligned to the established **Quiet Equity** house system (navy #132A43 · gold #B7893B ·
cream · Marcellus serif headlines / Inter body / home line-work). Rendered with PIL —
**0 credits, $0**. Re-runnable generator: `build_siq_posts.py` (fonts vendored in `fonts/`).

| # | Post | Format | Slides | Status |
|---|------|--------|--------|--------|
| 1 | Welcome / brand intro | static | 1 | delivered |
| 2 | Who this is for | carousel | 4 | delivered |
| 3 | Why QLD | static | 1 | delivered |
| 4 | 5 common mistakes | carousel | 6 | delivered |
| 5 | Case study | carousel | 4 | delivered |
| 6 | What happens in a strategy chat | static | 1 | delivered |
| 7 | The right team matters | static | 1 | delivered |
| 8 | Strategy Tip 01 | static | 1 | delivered |
| 9 | Book a chat (CTA) | static | 1 | delivered |

Files: `out/post-NN/`. Captions: `captions.md`.

## Log
- 2026-07-15 intake: new brief (`strategic-investing-qld-claude-brief.md`) + website
  reviewed. Brief asked navy-base + sans-serif; caught the existing Quiet Equity house
  style and re-aligned per Hunter's call.
- 2026-07-15 fonts: vendored Marcellus + Inter into `fonts/` (free, Google Fonts).
- 2026-07-15 delivered: 20 slides rendered in house system. Cost: 0 credits.

## Notes
- ⚠️ Brief tone = calm / no hype. Client site runs bolder claims ("80% pay off mortgage
  <10yrs", "13,000+ clients"). Posts kept claim-light per brief. Revisit if Hunter wants
  the proof numbers in.
- Brand mark = typographic lockup (STRATEGIC INVESTING · QLD). Swap for real SIQ logo
  when supplied.
- FB: 4:5 works in-feed; 1080×1080 square variants on request (generator extendable).
