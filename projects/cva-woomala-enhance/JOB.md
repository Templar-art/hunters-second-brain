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
- Fix-3 Precise Edit (240cr): 06_precise_FINAL (from the 3:2 outpaint), 08_precise_v2_FINAL, 10_precise_FINAL. #8 strong. #6: sky and sun strong, but the office block on the right came from the OUTPAINT (50cr step), not this pass. #10: blue sky good, but a blue cast crept onto the white sofa and dining chairs.

**Cost tally: 2,125 Magnific cr** (1,885 + 240)
- Hunter: skies must be LIGHT soft blue like #01; deep saturated blue rejected. Local fix (free): sky-only mask (blue hue + smooth texture + upper frame) remapped to #01's sky S/V. Tower recropped to 80% width; #10 blue cast desaturated locally.
- Delivery candidates: outputs/NN_DELIVER.* + deliver-sheet.jpg. Note: Precise Edit outputs are source-res (~1.1–1.7k px); tower only 1073px.

**Cost tally: 2,125 Magnific cr** (no change)
- Hunter: flat light-blue remap rejected ("messing up the sky"). Target = 06_nbp tower sky: natural gradient, deep blue overhead fading pale at the horizon, wispy cloud. Tower final reverted to 06_nbp (uncropped, office block kept as shown). Other skies regraded locally to that gradient (top 54,108,170 → horizon 157,193,227), texture kept. Known flaw: hard band behind the skyline on #02.
- Reverted all local sky hacks per Hunter. Sky-only Precise Edit (560cr) on 02, 03, 04, 05, 08, 09, 10 (10 also de-tinted): natural blue overhead fading to pale at the horizon, wispy cirrus. Layout untouched. DELIVER set = 01 nbp, 02–05/07–10 precise, 06 nbp tower, 11 nbp upscaled.
- Lesson: never fake skies with local colour remaps; Hunter spots it straight away. Use an AI sky-only pass.

**Cost tally: 2,685 Magnific cr** (2,125 + 560)
- Hunter: "do them correctly, use AI like Salisbury" = Nano Banana Pro. Re-ran NBP on the CORRECT originals for 02, 03, 04, 05, 07, 08, 09 (525cr). Layouts held this time, which confirms the earlier "drift" was the upload bug, not NBP. Natural soft-blue sky, warm low sun, real materials. DELIVER = NBP across all 11 (10 = NBP correct-source, 06 = NBP tower).
- Lesson: for CVA render-enhance, NBP from the correct source + framing lock is the recipe. Precise Edit reads too saturated/CGI.

**Cost tally: 3,210 Magnific cr** (2,685 + 525)
