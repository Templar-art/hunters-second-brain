---
type: project
tags: [day-to-dusk, video, ai-people, lifestyle, seedance, kling, higgsfield]
status: delivered
updated: 2026-11-11
---

# 21 Albany Ave, Currumbin: pool day-to-night + lifestyle clips

**Client:** tbc (same listing as [[albany-21-day-to-night]]; overlays for that listing went to [[real-specialists]]).
**Job folder:** [projects/albany-21-pool-day-to-night](../../projects/albany-21-pool-day-to-night/) (JOB.md has the full ledger).
**Shipped (2026-11-09):** a 4K pool day-to-night dissolve, a vertical reel day-to-night, and AI lifestyle clips of two invented women (table + balcony): wides, details, a coffee close-up and a balcony walk-up. **Spend: 678 HF** against an 88 HF intake quote; redos and two add-on shots made up the gap.

## What worked
- **Day-to-night from two handheld passes.** The Day and Night takes were 15–40 px apart, so a straight dissolve ghosts. Kling Omni Edit (`kling_video_edit`, 4K, 42 HF; 10 HF for the 5.3 s vertical reel) re-renders Night onto Day's motion using a Night frame as reference; the result held within about 2 px through the dissolve. Kling's 24 fps frames map 1:1 onto 23.976, same as [[albany-21-day-to-night]]. Second confirmation of the Omni Edit route in [[house-twilight]].
- **Character sheets fix identity.** Once Hunter supplied sheets, Seedance 2.5 omni_reference (80 HF per 1080p clip) with the sheet held the face on details and close-ups. Lanczos upscale to 4K for delivery. Matches auto-memory `feedback-people-clips-seedance`.
- **Short, contained moves land.** Profile turns, hands settling on a rail, a camera drift round a coffee cup: all approved first or second try.

## What failed (and the rule it taught)
- **Looking at camera = reject.** The first kling3_0 balcony wide had her look into the lens and grab the flag. Clips must be candid and never at camera; that is now a standing rule (see [[ai-lifestyle-people]] Gaze).
- **Detail must match the wide's eyeline.** The table detail turned the opposite way to the wide and sat at the same angle, so it read as a crop. Redo: new still from a different angle with the gaze held screen-left. Already in auto-memory `feedback-eyeline-continuity`.
- **Full walks across a wide frame fail.** The kling3_0 walk-up was the wrong model (Hunter wanted Seedance); the Seedance walk-up then had an off face and an unnatural gait. v3 started from a mid-step side-profile still with short steps: **provisional**, awaiting Hunter's verdict as of 2026-11-09.
- **Subtle motion trips QC.** The approved balcony wide v2 flagged NO_MOTION in QC; Hunter kept it. Candid + barely-moving is acceptable for lifestyle wides.

## Cost notes
- Seedance at 80 HF per clip dominated the bill (7 clips = 560 HF). Every rejected people clip costs 80 HF, so pilot one shot per class before batching.
- A session crash lost one paid 3 HF still: log the charge anyway (auto-memory `feedback-crash-recovery`).

Related: [[ai-lifestyle-people]] · [[house-twilight]] · [[albany-21-day-to-night]] · [[albany-21-main-sfx]] · [[higgsfield-pipelines]]
