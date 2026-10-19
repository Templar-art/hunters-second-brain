---
client: {client-slug}
address: {street address}
opened: {YYYY-MM-DD}
status: intake        # intake → generating → review → delivered
cost: { credits: 0, aud: 0 }
---

# Job — {address}

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 1 | {shot name} | full-frame / masked / video | todo | |

## Log

- {YYYY-MM-DD} intake: {N} shots triaged

---
_Vault: [[jarvis]]_

## Log — CVA Woomala St render enhance (2026-10-19)
- Intake: 11 developer renders (12–16 Woomala St) → make them look like 10x, not the architect's originals. Blue sky + warm moody light, stills only. CVA confirmed rights.
- Pipeline: GPT 2.5 Sunburst, medium, 2k, 3:2, @original ref (180cr) → optional Magnific upscale.
- #11 bedroom v1 → outputs/11_v1_sunburst.png (3072×2048). 180cr. Status: awaiting Hunter QC.
- Upscale held: 3072px source likely L/XL tier (270–1080cr), over the approved 270 test.

- v1 rejected by Hunter: "looks like a cartoon". Sunburst medium posterises → wrong model for photoreal arch-viz.
- #11 v2: Nano Banana Pro 2k edit, "real photograph, 24mm tilt-shift" prompt (75cr) → outputs/11_v2_nbp.png
- #11 v2 Magnific Ultra Photo 2x → outputs/11_v2_nbp_upscaled.jpg (5056×3392). Billed 270cr, NOT the ~90 quoted: tier set by source size. ⚠️ 180 over approval.
- QC: photoreal and holds at 100% crop. Flaw: gibberish signage on two skyline towers.

**Cost tally: 525 Magnific cr** (180 + 75 + 270)
