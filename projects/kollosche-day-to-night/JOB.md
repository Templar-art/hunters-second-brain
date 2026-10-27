---
client: kollosche
address: 5 Esther (Villas on Esther townhouses, street TBC)
opened: 2026-10-27
status: generating        # intake → generating → review → delivered
cost: { credits: 38148, hf_credits: 56, aud: 0 }   # derived from ## Ledger
---

# Job — Kollosche day-to-night clips, Villas on Esther

Source: `~/Downloads/Kollosche Day to Night/1–4.mp4`. All are 3840×2160 H.264 bt709 at 23.976 fps, between 1.46 and 3.46 s long. Target look: [[house-twilight]]. For the interiors, use the relight-from-fittings method learned on [[extra-salt-pottsville-dusk]]. Prompts: [prompts.md](prompts.md).

This is a different property from the Pottsville reel. Clip 1 was checked frame-by-frame against the Pottsville source, and they are not the same shot.

## Shots

| # | Shot | Len | Pipeline | Status | Notes |
|---|------|-----|----------|--------|-------|
| 1 | Living/dining dolly → corner balcony doors | 3.46 s | video (Seedance 2.5, still-as-reference) | delivered | Hunter: worked |
| 2 | Covered balcony, interior visible through slider | 1.96 s | video (Seedance 2.5) | delivered | pad to 4 s |
| 3 | Close through glass: sofa cushions → balcony chairs, palms | 2.00 s | video (Seedance 2.5) | delivered | pad to 4 s; no sky and no visible fitting, so it's the weakest |
| 4 | Street front, "VILLAS ON ESTHER" sign wall, push-in | 1.46 s | video (Seedance 2.5) | delivered | pad to 4 s; signage lettering at risk |

## Log

- 2026-10-27 intake: 4 clips triaged. Prompts written. Nothing has been spent yet. Waiting on Hunter's go-ahead and a decision on resolution.
- 2026-10-27 Hunter is running it himself: night still per first frame, then that still as the video reference. Credits are on his own account, so no ledger lines from us. Clip 2 still approved ("this one is great"). Clip 4 still: Hunter liked the look but wants it darker. Two problems: the sign misspells the name as "ONTSTHER", and the 5 glows gold. The source frame shows flat black standoff letters with no visible halo LED, so they stay unlit and a darker re-roll was given. Plan: comp the source sign wall back in during post.
- 2026-10-27 Clip 4 darker still approved ("looks great"), using the master prompt with the sign unlit. Built 4K padded 4.2 s copies of all 4 clips in `~/Downloads/Kollosche Day to Night/padded-4s/` for the video step. Trim back to the source lengths afterwards: 3.46 / 1.96 / 2.00 / 1.46 s.
- 2026-10-27 Clip 1 video worked (Hunter). The interior target is the clip 2 look, and the deep-blue-hour "moody/amber" still failed with an orange cast and added lanterns. Clip 3 changed frame because it was under 4 s, so it's being re-run on the 4.3 s padded copy. New standing rule: clips must be at least 4 s.
- 2026-10-27 Finals picked (zip `board-creations (31)` → `Downloads/Kollosche Day to Night/finals-1080p/`). Clip 1: O6IcQ2Oynm. Clip 2: IfO199itvE. Clip 3: nV5mlLuYQD. Clip 4: MBLusy2DCm, with the sign checked and still reading "5 / VILLAS ON ESTHER". The 4K Precision upscale is quoted at 2,297 + 1,897 + 1,897 + 2,297 = 8,388 cr, waiting on Hunter's go.
- 2026-10-27 Upscaled with Magnific Precision 4K x4 (8,388 cr). It returned 2560x1440 again, the same cap as Pottsville, so I scaled to 3840x2160 locally with lanczos. No frozen tails were detected, because Seedance generated real motion for the full 4–5 s, so the clips are delivered at full length and Hunter trims them in the edit. Delivered to `~/Downloads/Kollosche Day to Night/FINAL 4K/` as ProRes 422 HQ and H.264, one each per clip.
- 2026-10-27 Hunter flagged that clip 3's motion drifted from the source. The source was only 3.0 s, so Seedance invented the move. Hunter is redoing all 4 on Higgsfield himself, either with Kling 3.0 Omni Edit at native 4K or with Seedance 2.5 `video_edit`, using at least 4 s of real footage plus a motion-lock line. The current FINAL 4K set stays in place until the replacements land.
- 2026-10-27 Hunter redid the clips on Higgsfield. Seedance was blocked by the copyright filter, so he used Kling 3.0 Omni Edit. Clip 1 came back at 1080p (4.4 s) and clip 3 at 480p (4.0 s). I upscaled both with Topaz at 2160p to a true 3840x2160, with no 2560 cap. Clip 1 is crisp. Clip 3 is usable but softer, because the source was 480p. Delivered as `FINAL 4K/* v2 (Topaz)` in .mp4 and ProRes .mov, and the v1 versions moved to `old v1/`. Clip 2 stays as the Magnific v1. Clip 4 is still open because Omni keeps lighting the sign; the fallback is a free comp of the sign wall.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
<!-- Higgsfield batches: gen_runner.py run appends here. Magnific/MCP or web spends: gen_runner.py log JOB.md <amount> <hf|cr|aud> <note> -->
- 2026-10-27 | 29760 cr | Hunter's Magnific web Seedance 2.5 video runs (6x 1080p + 4x draft 480p, all 4 clips). Image stills not included
- 2026-10-27 | 8388 cr | Magnific video_upscale Precision 4K x4 (clip1 2297, clip2 1897, clip3 1897, clip4 2297)
- 2026-10-27 | 56 hf | Higgsfield topaz_video 2160p x2 (clips 1+3 Omni redo). Estimate ~28/clip, the CLI gives no quote

---
_Vault: [[jarvis]] · Client: [[kollosche]]_
