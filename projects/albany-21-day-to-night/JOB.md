---
client: tbc
address: 21 Albany Avenue, Currumbin
opened: 2026-11-06
status: generating        # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 3, aud: 0 }   # derived from ## Ledger
---

# Job — 21 Albany Avenue, Currumbin (day → dusk video)

**Source:** `/Volumes/10X SSD3/21 Albany Avenue, Currumbin/Twilight Examples/Day.mp4`. It is 3840×2160 at 23.976 fps and 12.89 s long. It is a ground gimbal walk-in up the driveway to the garage (orange door, house number 5 on the wall).
**Look reference:** `Main v2.mp4` in the same folder. It is the same house at dusk, 10.0 s, a different take with a different move.
**Brief (Hunter):** give the Day clip the night look while keeping Day's movement.

**Target look (from the reference):**
- Early dusk with a clear sky, pale blue fading to cream at the horizon.
- The garage downlights and the eave downlights are on, casting warm pools.
- The windows glow warm.
- The orange garage door is lit and reads strongly.
- The driveway and road stay readable in cool, even light.
- Only fixtures that already exist are lit.

## Shots

| # | Shot | Len | Pipeline | Status | Notes |
|---|------|-----|----------|--------|-------|
| 1 | Driveway walk-in to garage | 12.89 s | still (NB 2.1, Day frame 0 as Image 1 + reference as light-only Image 2), then video (Kling 3.0 Omni Edit 4K, with the still as reference) | intake | Quoted: still about 3 HF + Omni 4K 72 HF |

## Log

- 2026-11-06 intake: 1 shot, using the Coastal balcony route that worked (projects/coastal-day-to-night). Lessons to carry over:
  - Put the Day frame first as Image 1.
  - Check the still's alignment against Day frame 0 with phase correlation before spending on video.
  - Name every fixed element so nothing gets swapped.
- Quoted with `higgsfield generate cost`: Omni Edit 4K is 30 HF for 5 s and 72 HF for 12.9 s. The full-res 83 MB upload failed on the quote, so the source may need re-encoding smaller before the run. Nothing spent yet, waiting for Hunter's go.

- 2026-11-06 Hunter said go (about 75 HF).
  - **Still v1** (NB 2.1 4K, 3 HF): the Day frame went in as Image 1 and the reference frame as Image 2 (light only). Phase correlation against Day frame 0 measured -0.01/+0.07 px at 1080p, so it is aligned. The sun is gone, the eave downlights and garage door glow, and the window is warm. The large "5" on the garage pier went faint, so it is named in the video prompt.
  - **Upload:** the 4K source has to be under about 40 MB, so I re-encoded it at 22 Mb/s (`in/day_upload.mp4`, 31 MB).
  - **Omni Edit 4K (72 HF) FAILED** with not_enough_credits. The Higgsfield balance is 5.55 HF. Nothing was charged.
  - **Alternative quoted:** Magnific `video_modify` Kling 4.0 at 1080p is 4,290 cr (exact, simulate_cost), then a local lanczos upscale to 4K. Waiting on Hunter: top up Higgsfield, or use Magnific.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
<!-- Higgsfield batches: gen_runner.py run appends here. Magnific/MCP or web spends: gen_runner.py log JOB.md <amount> <hf|cr|aud> <note> -->
- 2026-11-06 | 3 hf | dusk_still_v1 nano_banana_2_1 (gen-runner)

---
_Vault: [[jarvis]] · Same workflow as [[house-twilight]] / projects/coastal-day-to-night_
