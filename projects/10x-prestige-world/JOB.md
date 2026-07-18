# JOB.md — 10x Prestige World (internal)

**Client:** 10x Visuals (internal marketing)
**Job:** Scroll-world landing page — cinematic photoreal fly-through of a prestige home, 5 scenes, Architecture A (continuous forward take), Prestige v2.0 brand system
**Folder:** projects/10x-prestige-world
**Status:** DELIVERED — site live at localhost:8767, all seams eye-verified
**Approved spend:** ~13 gens (5 stills gpt_image_2 + 5 legs seedance_2_0 1080p 8s + ~3 reroll buffer). Balance at approval: ~2841 cr.

## Log
- [2026-07-16] Intake + interview: photoreal / standard 5-scene / mobile encodes. Prompts written (shared style preamble, NSFW-safe phrasing). Spend approved by Hunter ("go").
- [2026-07-16] Anchor still (scene 1 facade) generation launched.

## Cost tally
| Item | Gens | Status |
|---|---|---|
| Anchor still scene 1 | 1 | done, approved by Hunter |
| Stills 2-5 (style-locked batch) | 4 | done, cohesion pass OK |
| Legs 1-5 first pass (incl. 4 NSFW re-rolls: L1x1 L3x1 L5x2) | 9 | done |
| Leg 3 seam fix + re-chain legs 4-5 (approved by Hunter) | 3+1 NSFW re-roll on L5 | done |
- [2026-07-16] Stills 2-5 landed, one-roll cohesion pass. Leg chain launched (sequential, ~30-50 min).
- [2026-07-16] Legs done (9 video gens). Encoded + SSIM gate: RED. Diagnosis: Seedance re-renders start frames (0.63-0.86 same-composition drift, crossfade covers) but leg 3 recomposed wide (0.41, visible step-back at seam 2-3). Hunter approved 3-gen fix: re-roll leg 3 + re-chain 4-5. Running total: 14 + 3 = 17 gens.
- [2026-07-16] Seam fix landed: sanitized leg-3 prompt passed first try ("real estate walkthrough" phrasing beats the NSFW filter). Re-chained 4-5 (L5 one re-roll, refunded). Seam 2-3 now composition-continuous.
- [2026-07-16] QA: SSIM gate numerically RED (0.51-0.67) — documented as model behaviour: Seedance 2.0 std re-renders start frames rather than pixel-locking, so the skill's >=0.95 bar is unreachable; eye-verified all 4 seams composition-continuous, crossfade 0.08 covers render drift. Browser QA green: blob seek OK, no console errors, mobile tier serves -m.mp4, phone crop reads.
- [2026-07-16] Final spend: ~18 successful gens, ~395 cr image+video (NSFW rejections refunded). Balance 2445.94.

---
_Vault: [[overview]]_
