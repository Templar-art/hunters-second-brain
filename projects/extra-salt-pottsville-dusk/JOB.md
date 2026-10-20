---
client: extra-salt
address: Pottsville (Kollosche VO reel)
opened: 2026-10-20
status: delivered         # intake → generating → review → delivered
cost: { credits: 8297, hf_credits: 0, aud: 0 }   # derived from ## Ledger
---

# Job — Pottsville day-to-night clip (Extra Salt reel, Kollosche VO)

Source: `~/Downloads/Extra Salt Reels/Kollosche VO/Pottsville Edits 1 Day to night.mp4` — 3.46s 1080p 23.976 interior dolly-in (lounge → balcony, hard sun stripes). Target look: [[house-twilight]].

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 1 | Lounge dolly-in → dusk | video (Magnific video_modify, Seedance 2.5, 720p) | delivered | padded to 4.05s w/ freeze (Seedance min 4s); trim back to 3.46s |

## Log

- 2026-10-20 intake: 1 shot; Hunter approved Seedance 2.5 720p @ 2,080cr. Submitted.
- 2026-10-20 result back (~20 min). Dusk sky, sun stripes gone, downlights on, geometry/motion held. Darker + moodier than locked bright twilight; sky a touch cloudier, little peach. Trimmed to 3.46s → `outputs/` + copied beside source in Downloads.
- 2026-10-20 free local ffmpeg lift (curves mids +~0.17, sat 1.05, lanczos → 1080p) → "DUSK bright.mp4". Brings it to the bright twilight look.
- 2026-10-20 Hunter: "too much like a filter, not real dusk" + needs 4K. Re-roll Seedance 2.5 1080p (4,320cr) w/ relight-from-fixtures prompt; then Magnific Precision 4K (~1,897cr). Approved ~6,200cr.
- 2026-10-20 v2 back: real twilight (deep blue sky, peach horizon, warm downlight pools, cool balcony). Precision upscale came back 2560x1440 despite 3840 target (API cap?) → lanczos to 3840x2160 locally. Delivered "DUSK v2 4K.mp4" + "DUSK v2 1080p.mp4" beside source. Lesson: Seedance relight prompts must name the light SOURCES (fixtures, pools, scallops, spill) not just "make it dusk", else output = dimmed-daylight filter look.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
<!-- Higgsfield batches: gen_runner.py run appends here. Magnific/MCP or web spends: gen_runner.py log JOB.md <amount> <hf|cr|aud> <note> -->
- 2026-10-20 | 2080 cr | Magnific video_modify Seedance 2.5 720p, dusk conversion
- 2026-10-20 | 4320 cr | Magnific video_modify Seedance 2.5 1080p re-roll (real-twilight relight prompt)
- 2026-10-20 | 1897 cr | Magnific video_upscale Precision 4K on v2

---
_Vault: [[jarvis]]_
