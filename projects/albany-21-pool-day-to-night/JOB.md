---
client: tbc
address: 21 Albany Avenue, Currumbin
opened: 2026-11-09
status: delivered
cost: { credits: 0, hf_credits: 598, aud: 0 }   # derived from ## Ledger
  - **Balcony wide v2:** candid, she keeps looking out at the view and never at camera. Motion is very subtle (QC flagged NO_MOTION).
  - **Table detail:** strong. She turns slowly into profile; the face matches the character sheet.
  - **Balcony detail:** good. Her hands start hovering just above the rail, then settle onto it.
  - All 3 are delivered to the SSD `AI Clips/`, waiting on Hunter's review.
- 2026-11-09 Hunter: balcony detail approved. Table detail REJECTED because she turns the opposite way to the wide (screen-right vs left) and it's the same angle. Redo plan: new still from her left side, front three-quarter, looking left (3 HF), then Seedance (80 HF). Waiting on go.
- 2026-11-09 table detail v2: new still from a rear three-quarter profile (3 HF), then Seedance (80 HF). Her gaze holds screen-left the whole clip, matching the wide, with a slow push-in. Delivered as `AI Clips/Table Lady Detail v2.mp4`.

- 2026-11-09 Hunter is keeping the subtle balcony wide. All 5 shots are delivered and the job is closed.
- 2026-11-09 reel (vertical 1080×1920, 5.3 s): Reel Day and Reel Night don't line up (handheld). Ran Kling Omni Edit pro (10 HF; the first try was an HTTP 520 upload error with no charge). The night clip stays locked to Day within about 2 px through the dissolve. Dissolve runs 1.2–4.0 s. Delivered as `Day to night/Reel Day to Night.mp4`.
- 2026-11-09 Hunter asked for 2 more balcony shots, both 4K. Approved with "go" (63 HF).
  - **Walk-up:** kling3_0 4K, start frame the empty balcony plate, end frame A. She walks in from frame-left and settles at the rail, never looking at camera. Delivered as `AI Clips/Balcony Lady Walk Up 4K.mp4`.
  - **Coffee close-up still:** done (3 HF). She looks screen-right, matching the wide. Waiting on Hunter before animating (30 HF).
- 2026-11-09 Hunter: the walk-up should have been Seedance, and the coffee detail is the existing rail framing with a cup added. Redo approved with "go".
  - **Walk-up:** Seedance using the character sheet, start frame the empty plate and end frame A (80 HF). Clean walk-in, sandals on, candid. Lanczos-upscaled to 4K and delivered as `Balcony Lady Walk Up Seedance 4K.mp4`.
  - **Coffee rail still:** done (3 HF). The earlier attempt was lost in the session crash, also 3 HF. The clip (80 HF) waits on Hunter.

- 2026-11-09 Hunter REJECTED the Seedance walk-up: her face looks off and the walk is unnatural. A full walk across a wide frame is too much for AI; it needs a shorter move.

- 2026-11-09 **Coffee clip:** Seedance using the character sheet (80 HF). The camera drifts round to reveal her face in three-quarter profile looking out, holding the cup the whole time. Upscaled to 4K and delivered as `Balcony Coffee Detail 4K.mp4`. The walk start still is done (3 HF), with the clip waiting on Hunter's go.

- 2026-11-09 Hunter APPROVED the coffee detail.

## Ledger
---

# Job: 21 Albany Avenue, Currumbin (pool day → night + lifestyle clips)

**Sources:**
- SSD `AI Clips/Day to night/` holds Pool Day.mp4 and Pool Night.mp4. Both are 4K, 23.976 fps and 7.09 s long. They are two handheld passes of the same move and do not line up (15–40 px apart).
- `~/Downloads/hf_20261106_072153…png` is the balcony lady (in/A.jpg).
- `~/Downloads/hf_20261106_074318…png` is the table lady (in/B.jpg).

**Brief (Hunter):** a pool day→night clip on Higgsfield. The lady at the table and the lady on the balcony each get a wide clip of her looking left plus a detail shot. That is 4 lady shots.
- 2026-11-09 | 3 hf | table_detail_v2_still nano_banana_2_1 (gen-runner)
- 2026-11-09 | 80 hf | table_detail_v2 seedance_2_5 (gen-runner)
- 2026-11-09 | 10 hf | reel_night kling_video_edit (gen-runner)
- 2026-11-09 | 30 hf | balcony_walkup kling3_0 (gen-runner)
- 2026-11-09 | 3 hf | coffee_still nano_banana_2_1 (gen-runner)
- 2026-11-09 | 3 hf | coffee_detail_still NB 2.1 lost in session crash (charged, no file)
- 2026-11-09 | 80 hf | walkup_seedance seedance_2_5 (gen-runner)
- 2026-11-09 | 3 hf | coffee_detail_still nano_banana_2_1 (gen-runner)
- 2026-11-09 | 3 hf | walk_start_still nano_banana_2_1 (gen-runner)
- 2026-11-09 | 80 hf | coffee_clip seedance_2_5 (gen-runner)

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
- 2026-11-09 | 80 hf | balcony_wide_v2 seedance_2_5 (gen-runner)
- 2026-11-09 | 80 hf | table_detail_v1 seedance_2_5 (gen-runner)
- 2026-11-09 | 80 hf | balcony_detail_v1 seedance_2_5 (gen-runner)
