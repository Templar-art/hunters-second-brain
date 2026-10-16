---
client: internal-rnd
address: Beachfront Gold Coast house (fictional test build)
opened: 2026-10-12
status: review        # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 20.25, aud: 0 }
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

---
_Vault: [[jarvis]]_
