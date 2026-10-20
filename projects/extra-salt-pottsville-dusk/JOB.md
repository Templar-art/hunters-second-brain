---
client: extra-salt
address: Pottsville (Kollosche VO reel)
opened: 2026-10-20
status: review            # intake → generating → review → delivered
cost: { credits: 2080, hf_credits: 0, aud: 0 }   # derived from ## Ledger
---

# Job — Pottsville day-to-night clip (Extra Salt reel, Kollosche VO)

Source: `~/Downloads/Extra Salt Reels/Kollosche VO/Pottsville Edits 1 Day to night.mp4` — 3.46s 1080p 23.976 interior dolly-in (lounge → balcony, hard sun stripes). Target look: [[house-twilight]].

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 1 | Lounge dolly-in → dusk | video (Magnific video_modify, Seedance 2.5, 720p) | review | padded to 4.05s w/ freeze (Seedance min 4s); trim back to 3.46s |

## Log

- 2026-10-20 intake: 1 shot; Hunter approved Seedance 2.5 720p @ 2,080cr. Submitted.
- 2026-10-20 result back (~20 min). Dusk sky, sun stripes gone, downlights on, geometry/motion held. Darker + moodier than locked bright twilight; sky a touch cloudier, little peach. Trimmed to 3.46s → `outputs/` + copied beside source in Downloads.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
<!-- Higgsfield batches: gen_runner.py run appends here. Magnific/MCP or web spends: gen_runner.py log JOB.md <amount> <hf|cr|aud> <note> -->
- 2026-10-20 | 2080 cr | Magnific video_modify Seedance 2.5 720p, dusk conversion

---
_Vault: [[jarvis]]_
