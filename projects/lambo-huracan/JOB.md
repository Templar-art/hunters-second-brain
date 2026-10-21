---
client: internal
address: 18 Maryland (Lambo clip, ZED)
opened: 2026-10-21
status: generating        # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 140, aud: 0 }   # derived from ## Ledger
---

# Job: 18 Maryland, CG Huracán clips

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 1 | Drive-in over the listing photo, camera pans with the car | Blender CG over still plate | review | `maryland/maryland_drive_in_pan.mp4` (no zoom, per Hunter) |
| 1s | Shot 1 through Seedance 2.5 video_edit (photoreal pass) | video | generating | 1080p |
| 2 | C5076 push between the gate pillars, car passes the camera and goes up the drive | Blender CG over tracked plate | todo | solve 0.21 px; ground plane pending (re-track on CLAHE copy) |
| 3–7 | Close-ups: low rise, headlight slide, wheel track, profile glide, rear push | pure CG | rendering | `shots/closeups/` |

## Log

- 2026-10-21 intake: Hunter wants the CG Huracán (ZEDDDD, VIC plates) driving at 18 Maryland, from the listing photo.
- 2026-10-22 shot 1 v1 drove out and slid (the Sketchfab root ignored yaw keys). v2: clean rig, drives in, bicycle-model steer. Hunter: "dont zoom in", so v3 = fixed lens, pan only.
- 2026-10-22 Hunter "go" on Seedance 2.5 video_edit, quoted 140 HF. Running on the pan-only v3, the same 7 s as the quoted clip.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
<!-- Higgsfield batches: gen_runner.py run appends here. Magnific/MCP or web spends: gen_runner.py log JOB.md <amount> <hf|cr|aud> <note> -->
- 2026-10-22 | 140 hf | s1_drive_in_photoreal seedance_2_5 (gen-runner)

---
_Vault: [[jarvis]]_
