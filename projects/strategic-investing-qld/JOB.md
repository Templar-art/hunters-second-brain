---
client: strategic-investing-qld
address: n/a (social ad creative, not a property)
opened: 2026-07-10
status: delivered     # intake → generating → review → delivered
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

## Revisions (15 Jul, same day)
- **Numbering:** carousel badge now = slide/total within its own carousel (e.g. 02/04),
  not "post N of 9". Standalone posts carry **no number** (posting separately).
- **Filler batch — posts 10–17** for grid variety (the first 9 read too samey — all
  navy). Added templates: `photo_band`, `photo_full`, `cream_quote`, `monogram_tile`.
  - 10 photo-band (home) · 11 photo-full (coffee chat, CTA) · 12 photo-band (suburb
    aerial) · 13 + 14 cream-inverse quotes · 15 monogram stamp · 16 + 17 Strategy Tips
    02/03. Total now **17 posts**.
  - Photos: **free Freepik stock via Magnific (0 credits)** — `photos/home.jpg`,
    `coffee-chat.jpg`, `suburb-aerial.jpg` (Australian residential aerial). Graded to the
    navy/gold system. Freepik free license — attribution may apply per platform.
  - `grid-preview.png` = 3-wide contact sheet of all 17 cover tiles.
- Grid tip: interleave photo / cream / monogram tiles among the navy ones so no 3-in-a-row
  look identical.

## Log (cont.)
- 2026-07-15 revision: numbering fixed; 8 filler posts added (2 cream, 3 photo, 1
  monogram, 2 tips); 3 free stock photos pulled + graded. Cost: 0 credits.

## Revision 2 (15 Jul) — no CTAs, more informative, gaps fixed
- Removed all CTAs: post 9 (was "Book a chat") → why_support "What a good strategy
  balances"; post 11 (was coffee CTA) → "Good strategy starts with good questions". No
  phone/book/message copy anywhere. Captions rewritten CTA-free + dash-free.
- Added informative posts 18–23: Growth vs cashflow · What is equity · Rentvesting ·
  Know your numbers (photo, planning.jpg) · 2 principle cream quotes. **23 posts total.**
- Fixed the big vertical gaps: numbered_step + list_slide now vertically centre their
  content group and carry the house line-work motif; cream_quote mark tightened.
- Grid rhythm balanced across photo / white (cream) / blue (navy). 4 photos, 4 cream,
  rest navy. 1 more free stock photo pulled (planning, 0 credits).

---
_Vault: [[strategic-investing-qld]]_
