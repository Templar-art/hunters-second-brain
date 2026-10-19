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

- Batch (approved ~800cr): tower crop-bars → outpaint 3:2 (50) → NBP (75); 9 others NBP 2k (9×75=675). Outputs NN_nbp.png.
- QC: everything reads as a real photo with blue sky and sun shadows. ⚠️ NBP drifts the composition: #07 entry redesigned (fake "STREET" sign, new car); #08 became a different room; #02 lounger layout changed; #03 pendant/chair count changed; #04 pendant swapped; #06 invented an office tower on the right. Holding well: #01, #05, #09, #10, #11.
- Lesson: NBP = photoreal but loose framing; off-plan marketing must match the design, so drifted frames need a redo.

**Cost tally: 1,325 Magnific cr** (525 + 800)
- ⚠️ BUG (Claude): the batch PUT loop ran in zsh (1-indexed arrays), so upload n got file n+1. #2 dusk pool was never uploaded, and the NBP batch prompts hit the wrong photos, which caused most of the "drift". Mismatched NBP outputs moved to outputs/_mismatched/.
- Precise Edit batch (Ideogram 4.5, 400cr): outputs are faithful, layout and angle locked, labelled by true source: 03 boardroom, 04 rooftop dining, 05 gym, 08 dining, 09 kitchen.
- Good NBP (correct source): 01 pool golden, 06 tower, 10 living, 11 bedroom (+ upscale).
- Still missing: #2 dusk pool, #7 entry.

**Cost tally: 1,725 Magnific cr** (1,325 + 400)
- #2 dusk pool + #7 entry Precise Edit (160cr) → 02/07_precise_FINAL.png. Layout locked, now blue sky and sun.
- Full before/after: outputs/compare-sheet.jpg. Layout and angle hold on 10/11. Weak: #8 dining and #10 living barely changed (sky still pale). ⚠️ #6 tower: NBP widened the angle, turned the façade bronze and invented an office block, so it breaks the no-angle-change rule.

**Cost tally: 1,885 Magnific cr** (1,725 + 160)
