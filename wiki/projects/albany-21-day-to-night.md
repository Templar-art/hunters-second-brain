---
type: project
tags: [twilight, day-to-dusk, video, magnific, kling, nano-banana]
status: review
updated: 2026-11-06
---

# 21 Albany Ave, Currumbin: day-to-dusk video

**Client:** 21 Albany Avenue, Currumbin. The listing overlays were for [[real-specialists]] (Connor Hewitt).
**Brief (Hunter):** relight `Day.mp4`, a 12.9 s ground gimbal walk-in to the garage, so it matches the dusk example `Main v2.mp4`, and keep Day's camera move exactly.
**Job folder:** `projects/albany-21-day-to-night/` (see JOB.md).
**Delivered to:** `/Volumes/10X SSD3/21 Albany Avenue, Currumbin/Twilight Examples/`
- `Day to Dusk 4K.mp4`: 3840×2160, 23.976 fps, 309 frames, so it is frame-for-frame with Day.
- `Day vs Dusk side-by-side.mp4`

## Route
1. **Dusk still.** Nano Banana 2.1 at 4K, 3 HF. Day frame 0 went in as Image 1 and a frame of the dusk example as Image 2 (light only). Phase correlation against Day frame 0 measured about 0.07 px, so the still is aligned.
2. **Video.** The plan was Kling 3.0 Omni Edit 4K on Higgsfield (72 HF), but it failed with not_enough_credits, so the video ran on **Magnific `video_modify` Kling 4.0 at 1080p, 4,290 cr**. The inputs were the Day clip (re-encoded to 31 MB) and the still as the "dusk" reference. It finished in about 6 minutes, well under its 17-minute estimate.
3. **Finish.** Retimed from Kling's 24 fps to 23.976 (the frames map 1:1), lanczos-upscaled to 4K with a light unsharp, audio stripped.

**Total spend:** 3 HF + 4,290 cr.

## QC
- **Motion:** locked to the source. Edge phase correlation sampled every 12 frames read under 0.5 px off at 960 px wide, all the way through.
- **Fixtures held:** fences, gate, letterbox, pillar, palms and the driveway pattern all stayed put.
- **Lighting:** the eave downlights came on, there are warm pools on the driveway, the shutters glow amber and the orange garage door reads strongly. The sky is a clean gradient.

**Weak points to watch:**
- The charcoal walls and the garage pier drift **olive-grey** under the warm light.
- The gold "5" on the pier goes bronze with low contrast. It is still legible.
- The driveway is warm-yellow toward the end of the clip.

All three are fixable with a grade (pull yellow out of the mids and hold the charcoal) rather than a re-generation.

## Lessons
- Magnific Kling 4.0 `video_modify` with a matched dusk still as the reference **keeps the move frame-exact**. It is a working fallback when Higgsfield credits run dry. It costs much more (4,290 cr for 13 s), so quote it first.
- Higgsfield's cost quote and upload fail on sources over about 40 MB. Re-encode 4K to about 22 Mb/s first.
- Kling outputs 24 fps. Retime it back to the source rate before delivery, or it drifts against the edit.

Related: [[house-twilight]], [[plate-vfx]], [[higgsfield-pipelines]].
