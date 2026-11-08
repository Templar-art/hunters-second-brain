---
client: tbc
address: 21 Albany Avenue, Currumbin
opened: 2026-11-09
status: generating
cost: { credits: 0, hf_credits: 63, aud: 0 }   # derived from ## Ledger
---

# Job: 21 Albany Avenue, Currumbin (pool day → night + lifestyle clips)

**Sources:**
- SSD `AI Clips/Day to night/` holds Pool Day.mp4 and Pool Night.mp4. Both are 4K, 23.976 fps and 7.09 s long. They are two handheld passes of the same move and do not line up (15–40 px apart).
- `~/Downloads/hf_20261106_072153…png` is the balcony lady (in/A.jpg).
- `~/Downloads/hf_20261106_074318…png` is the table lady (in/B.jpg).

**Brief (Hunter):** a pool day→night clip on Higgsfield. The lady at the table and the lady on the balcony each get a wide clip of her looking left plus a detail shot. That is 4 lady shots.

## Shots
| # | Shot | Pipeline | Status |
|---|---|---|---|
| 1 | Pool day→night | Kling Omni Edit 4K (Day video + Night f0 ref) → local dissolve | generating |
| 2 | Table lady wide, looks left | kling3_0 i2v 5 s | generating |
| 3 | Table lady detail | NB 2.1 4K still → Hunter approves → kling3_0 | still |
| 4 | Balcony lady wide, looks left | kling3_0 i2v 5 s | generating |
| 5 | Balcony lady detail | NB 2.1 4K still → Hunter approves → kling3_0 | still |

## Log
- 2026-11-09: intake. Quoted 88 HF in total. Hunter said go.
- 2026-11-09 batch 1 (63 HF):
  - **Pool night (Omni 4K):** good. Dissolved from Day at 1.75–5.25 s, mapping Kling's 24 fps frames 1:1 onto 23.976, and delivered to the SSD as `Day to night/Pool Day to Night 4K.mp4`.
  - **Table wide:** the head turn is subtle. Hunter: "fine". Delivered as `AI Clips/Table Lady Wide.mp4`.
  - **Balcony wide:** REJECTED. She looks at the camera and grabs the flag. Hunter's rule: clips must be cinematic and candid, never looking at camera.
  - **Detail stills:** both OK, not animated yet.
  - Hunter supplied character sheets (in/charsheet/) for identity. Seedance 2.5 omni_reference at 1080p is quoted at 80 HF per clip.

## Ledger
- 2026-11-09 | 42 hf | pool_night kling_video_edit (gen-runner)
- 2026-11-09 | 7.5 hf | table_wide kling3_0 (gen-runner)
- 2026-11-09 | 7.5 hf | balcony_wide kling3_0 (gen-runner)
- 2026-11-09 | 3 hf | table_detail_still nano_banana_2_1 (gen-runner)
- 2026-11-09 | 3 hf | balcony_detail_still nano_banana_2_1 (gen-runner)
