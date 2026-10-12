---
client: zed
address: n/a (style guide, no property)
opened: 2026-10-09
status: delivered        # intake → generating → review → delivered
cost: { credits: 4845, aud: 0 }
---

# Job — ZED modern-luxury style guide

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 1 | Option 01 Warm Organic board (10 rooms) | Magnific GPT 2.5 Sunburst, 2k medium, text-to-image | review | 180cr. Guest bed got a rug + art (rule says no rug); invented tagline in footer |
| 2 | Option 02 Gallery Stone board | same | review | 180cr. Title kerning glitch "OPTIO N" |
| 3 | Option 03 Smoked Oak Suite board | same | review | 180cr. Invented tagline in footer |
| 4 | Option 04 Riviera Resort board | same | review | 180cr. Dining table round-ish not oval trestle; outdoor lounge is chair + ottoman, no sofa |
| 5 | Master sheet (2×2 of the four boards) | local PIL composite | review | free; zed-master-style-guide.png (6384×4776) + -web.jpg |

## Purpose

Client-facing: goes to Zed so he can **pick one style** for a furnished home. Not an internal staging doc. Final deliverable drops prompts, credit costs, confidence scores, staging rules and locked/proposed wording.

## Log

- 2026-10-09 intake: HTML style guide (Options 01–04) published as artifact
- 2026-10-09 generating: 4 boards, Sunburst 2k medium, 4 × 180 = 720cr (earlier 100cr quote was wrong, was GPT 2 not 2.5 Sunburst)
- 2026-10-09 review: Hunter asked for one image with everything → stitched 4 boards into master sheet locally, no extra spend

---
_Vault: [[jarvis]]_
- 2026-10-09 Hunter: deliverable is for Zed to pick a style → master sheet header reworded client-facing ("Choose your furnishing style"); deep research running to deepen room kits before rebuild
- 2026-10-12 generating: 4 living-room anchors on Nano Banana Pro 2k, 4 × 75 = 300cr (total 1,020cr). All 4 landed: exact inventory, bright exposure, no text. Awaiting approval before the 36 referenced rooms (2,700cr)
- 2026-10-12 generating: 36 rooms on Nano Banana Pro 2k, each with its option's living anchor as reference, 36 × 75 = 2,700cr (job total 3,720cr). Boards v2 assembled locally in boards-v2/ (code-rendered title, swatches, captions). Known misses: end chairs at 01 dining, 01 outdoor dining, 04 dining, 04 outdoor dining
- 2026-10-12 redo: 4 dining rooms, 300cr (job total 4,020cr). Fixed with round tables + 6 chairs evenly around: 01 outdoor dining, 04 dining, 04 outdoor dining. 01 indoor dining (oval, Zed spec) STILL got 8 chairs incl. ends despite 'exactly six'. v1 rejects in rooms/v1-rejected/
- 2026-10-12 fixes: 01 indoor dining end chairs masked out (Auto retouch failed, no charge; Nano Banana Pro retouch 75cr). Option 02 rebuilt with smoked-oak floors + timber pieces from a new anchor, 10 × 75 = 750cr. Job total 4,845cr. Delivery folder 'ZED Style Guide - For Zed' (4 boards, overview, 40 room JPGs), gitignored, built from rooms/ + boards-v2/
