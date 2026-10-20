---
client: extra-salt
address: Kollosche reel — Pottsville drone wide ("Fake birds?")
opened: 2026-10-20
status: delivered     # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 0, aud: 0 }   # derived from ## Ledger — never edit by hand
---

# Job — Kollosche reel: gulls over the drone wide

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 1 | Drone pull-back over Mooball Creek mouth, 1.9s (45 frames + 1 cut frame) | Blender CG comp (no AI on plate) | delivered | 4 silver gulls, plate pixels untouched |

## Log

- 2026-10-20 intake: Hunter wants birds flying past, grade identical to the source. Routed to a Blender comp because AI video-to-video would repaint the drone wide.
- 2026-10-20 track: frame 46 is a hard cut to the next shot, so the solve uses frames 1–45. Blender's free solve was unstable (low parallax), so a flat-ground drone camera was fitted to 1,494 LK tracks: 0.21px median error, 28.4mm-eq, 15° pitch, 4.9m pull-back. → `camera.json`
- 2026-10-20 build: procedural silver gulls (`scripts/03_scene.py`), EEVEE RGBA pass with 0.2 shutter motion blur, ffmpeg overlay. Verified: 0 px change outside the birds and frame 46 identical.
- 2026-10-20 delivered for review: `out/fake-birds_gulls.mp4` (H.264 CRF12) + `out/fake-birds_gulls_prores.mov` (ProRes 422 HQ), original audio.
- 2026-10-20 approved: Hunter signed off on the first full render.
- 2026-10-20 v2: Hunter asked for more polys. Bodies are now 32x16 spheres plus subsurf, wings get creased-outline subsurf L3 (~5.7k polys per gull, was a few hundred). Re-rendered and re-exported over the same out/ files.

## Ledger

<!-- one line per spend; header cost is derived from this. No spends on this job (all local Blender/ffmpeg). -->

---
_Vault: [[jarvis]]_
