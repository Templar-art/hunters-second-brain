---
client: internal-rnd
address: Beachfront Gold Coast house (fictional test build)
opened: 2026-10-12
status: delivered     # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 791.5, aud: 0 }   # derived from ## Ledger
---

# Job — Beach house Blender → AI pipeline test

Second R&D build for the [[blender-blockout-pipeline]]. A dense scene of about 1,700 objects: a full walk-through interior, 8 neighbour houses, mannequin people on walk paths, and 6 shots, including a gimbal tracking shot. Also tests the material-ID colour map.

## Shots

| # | Shot | Status | Notes |
|---|------|--------|-------|
| 1 | Surf reveal | guide | |
| 2 | Pool glide | 5-model shootout done | Model test frame |
| 3 | Living view | guide | |
| 4 | Top-down rise | guide | |
| 5 | Walkthrough (slider → lounge → stair) | guide | Clearance-checked |
| 6 | Beach tracking (gimbal follows walking couple) | guide | Shakify walk shake |
| 7 | Supercar arrival (street → driveway) | blocked | Built supercar; parked car moved off its path; clearance checked |

## Log

- 2026-10-12 intake: beach house built headless, 4 shots
- 2026-10-16 rebuild: detail pass to about 1,600 objects, walk-through interior, realistic neighbours, beds and sofas, people, tracking shot
- 2026-10-16 generate: 5-model shootout on shot 2 with guide + colour-ID map (Sunburst 2.75, Nano Banana 2.1 2, Nano Banana Pro 2, Seedream 5.0 Pro 2.5, FLUX 3 3 = 12.25 HF). Hunter said "try it".

- 2026-10-16 generate: 4 cast face locks, Nano Banana Pro 2K (~8 HF). C has a softbox in frame, so re-roll it.
- 2026-10-16 blender: camera clearance check on all 7 shots (only the walkthrough armchair grazed; chair moved), street facade detailed, supercar built.

- 2026-10-16 generate: face C re-roll (2), 4 outfit stills on Banana Pro (8; A retried after a network error).
- 2026-10-16 generate: 14 hero stills, 7 shots × Seedream 5 Pro (2.5) + Sunburst (2.75) = 36.75, plus the Lambo shot 7 in both (5.25), plus the 02 Seedream retry (upload error, no charge). QC: Sunburst wins 03/04/05/06; Seedream failed 04 (not top-down) and 05 (invented a pool), and copied the Blender low-poly palms literally; shot 7 broken (parked car in the foreground at frame 1300), car moved.

- 2026-10-16 decision: Hunter picked Sunburst for all shots. Shot 7 redone from frame 1380 on Sunburst (2.75): pearl-white Lambo-style car, no badges, PASS.

- 2026-10-16 generate: 7 × Seedance 2.5 8s 1080p from the Sunburst stills, no cast refs (refs would push it to 128/shot) = 672 HF. QC: 03, 04, 05 PASS; 02 pass with minor props appearing; 01 barely moves; 06 has a dissolve/morph at about 2s then cuts to leg tracking; 07 the car doesn't roll. Rough assembly at video/rough-assembly-v1.mp4.

- 2026-10-16 face test, shot 06 (Hunter: 'a lot is shit, faces messing up'): Kling 3.0 Pro 5s (12.5) + Veo 3.1 Fast high 8s (32) = 44.5. Both are one continuous take, no dissolve, faces hold and match the cast. Kling: true sideways tracking with parallax, background stable, slight motion blur. Veo: walks toward camera, sharper faces, but the background houses drift and change late in the clip.

- 2026-10-20 decision: Veo 3.1 Fast chosen for the people shots. Quoted 32 HF each (high, 8s, 16:9, start frame = Sunburst still), so 96 HF to re-roll 01, 06 and 07. **On hold, nothing generated.** Hunter: build the system and framework first; the Blender run took too long ("time was shit").

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
- 2026-10-20 | 791.5 hf | baseline: all Higgsfield spend to 2026-10-16 per header tally, pre-ledger

---
_Vault: [[jarvis]]_
- 2026-10-26 closed: Hunter confirmed the Kling/Veo pick, the 01/06/07 re-rolls and the re-cut are done. Those spends happened outside this ledger, so the tally above undercounts.
