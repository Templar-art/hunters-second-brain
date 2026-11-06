---
client: tbc
address: 21 Albany Avenue, Currumbin
opened: 2026-11-06
status: intake        # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 0, aud: 0 }   # derived from ## Ledger — never edit by hand
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

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
<!-- Higgsfield batches: gen_runner.py run appends here. Magnific/MCP or web spends: gen_runner.py log JOB.md <amount> <hf|cr|aud> <note> -->

---
_Vault: [[jarvis]] · Same workflow as [[house-twilight]] / projects/coastal-day-to-night_
