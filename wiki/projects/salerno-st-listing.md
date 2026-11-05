---
type: project
tags: [kollosche, listing-video, sfx, vfx, drone, lot-outline, pin]
status: delivered
updated: 2026-11-05
---

# 42 Salerno Street, Isle of Capri — listing package (Kollosche)

Kollosche listing for Eddie Wardale's team. Hunter cut the main edit (67.8 s, 4K 23.976) to the ZOYA "Pulled Under" v8 cut. Job folder: [JOB.md](../../projects/salerno-st-sfx/JOB.md). Cost: $0, everything ran locally. Same look as the [[kollosche]] 4-6 Buckingham Way job.

## What shipped
- **SFX:** v1 had 7 tasteful cues in the [[desire-the-pilot-reference]] style. v3 (on the 15:14 re-export) dropped the whooshes because Hunter's own SFX were already in the mix, and gave each of the 21 scenes its own calibrated bed instead. See [[sfx-toolkit]].
- **Graphics:** a Kollosche address super, the logos gathered into `Logos/`, and the Eddie Wardale end card.
- **Lot outline:** a thin white outline on the rotating top-down (src f833–899). The lot came from the QLD cadastre (lot 231RP110045) because no pinned stills exist on the SSD. Hunter asked for the front edge to run "to the street", so it was extended to the kerb. The outline is tracked with a SIFT-chained ground-plane homography and draws on from shot frame 22.
- **Pin:** the navy #011A3B K badge (`projects/drone-pin/clients/kollosche.json`) sits on the subject roof in the city wide (src f900–933), on a KLT tip track. There is one pin per video, and the pin shot has no outline (auto-memory `feedback-lot-outline-from-delivered-stills`).
- **Deliverables on the SSD:** the alpha overlays (ProRes 4444) and previews are in `Edits/Overlays/`. The full composite `Main_Kollosche_graphics.mp4` (original audio) is in `Edits/Graphics/`.

## Lessons
- ⚠️ Kollosche team logos go on Agent Focus promos only, never on listing videos.
- A re-export can already carry Hunter's own SFX. Subtract the old audio to find them before adding any cues.
- One beds file (`outside-ambience-with-birds-61606`) has a voice-like component, so it was dropped (auto-memory `feedback-sfx-no-voices`).
- Top-down drone plates have a planar ground. A chained homography tracks the outline correctly in 3D without a full solve.
