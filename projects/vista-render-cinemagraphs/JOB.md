---
client: salisbury   # per Hunter 2026-10-21
address: "Vista" (render set, 12 renders)
opened: 2026-10-20
status: intake         # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 315, aud: 0 }   # derived from ## Ledger
---

# Job — Vista renders → cinemagraphs

Source: 12 developer renders pasted by Hunter (2000×1368) → `inputs/1–12.jpg`. Brief: camera locked, only real ambient motion (curtains, trees, fans, sun streaks drifting). Recipe from [[solis-pool-cinemagraph]]: Seedance 2.5 i2v, hard camera lock + still-list. Picks cropped centre 16:9 → `hero/*_169.jpg` (1920×1080).

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 8 | Bedroom: 2 fans, curtain, trees, sun band | video (Seedance 2.5 720p 5s, start=end frame) + local loop/upscale | review | `video/08_bedroom_v1_loop15_1080.mp4` |
| 11 | Hallway: sheer curtain, sun beams creep, skylight leaves | video (Seedance 2.5 720p 5s, no loop) + local 1080p50 | review | |
| 5 | Powder: tree in window, wall sun patch dapple | video (Seedance 2.5 720p 5s, no loop) + local 1080p50 | review | |
| 6 | Kitchen: floor sun stripes creep, garden | video (Seedance 2.5 720p 5s, no loop) + local 1080p50 | review | |
| 4 | Living: palms outside, ceiling sun patches | video (Seedance 2.5 720p 5s, no loop) + local 1080p50 | review | |
| 1 | Exterior: palm fronds + their shadows on garage/drive | video (Seedance 2.5 720p 5s, no loop) + local 1080p50 | review | |
| 2,3,7,9,10,12 | gate, office, laundry, towel nook, gym, ensuite | — | reserve | weaker motion or mirror/signage risk |

## Log

- 2026-10-20 intake: 12 renders, 6 picked, 16:9 silent. Hunter asked for cheaper: switched 1080p 10s (160 hf) → 720p 5s with end-image = start-image for a seamless loop (35 hf). Batch est 210 hf (was 960).
- 2026-10-20 bedroom pilot (Hunter go, 35 hf): frame locked, both fans spin, curtain sways, furniture holds. gen_runner NO_MOTION = whole-frame false positive again (fan/curtain region diff ~0.9 vs wardrobe 0.05). Looped 3× with 0.4s crossfades → 15s, lanczos 1920×1080 + light unsharp (0 credits). Awaiting Hunter review.
- 2026-10-20 Hunter: run the other 5, no loop, upscale to 1080 at 50 fps. Ran 5 × 35 hf (Hunter go). QC: frames locked on all; hallway sun beam + curtain, kitchen floor stripes creep and dim toward sunset, living ceiling patches + palms, exterior fronds + their shadows. Powder room barely moves (0.2% px), weakest. All 6 (bedroom un-looped too) → minterpolate mci 50 fps + lanczos 1920×1080 → `deliver/*_1080p50.mp4` (0 credits). Interp leaves a faint ghost on the bedroom fan blades. Total 210 hf.
- 2026-10-20 powder re-roll v2 (Hunter go, 35 hf): stronger prompt (steady breeze, dancing leaf shadows on the wall patch, towel stirs). Only marginally more motion (0.7% px vs 0.2%): faint tree + towel. Seedance won't animate this composition much. Delivered `deliver/05_powder_v2_1080p50.mp4`. Fallback if needed: local leaf-shadow dapple composite over the wall sun patch (0 credits). Total 245 hf.
- 2026-10-20 powder v3 (Hunter asked, 0 credits): local leaf-shadow dapple over v2. Mask = still luminance 190→225 on the wall left of x=600, 6px feather. Two procedural leaf layers (near sharp, far soft) sway on sine offsets with subpixel shift, darken the patch up to ~34% with a slight cool tint. Script `work/dapple.py`. → `deliver/05_powder_v3_dapple_1080p50.mp4`. Awaiting Hunter review.
- 2026-10-21 Hunter: 2 slow reels × 4 clips for Salisbury → client set. Need 2 more clips: gate (#2) + laundry (#7), generated natively 9:16 from local 9:16 crops (Hunter yes, 70 hf). ❌ BOTH FAILED fixture lock: frame 0 is already re-imagined, not the start image. Gate: background trees replaced, framing shifted. Laundry: zoomed in, a sink added to the left bench, tree and path redrawn. The 16:9 runs from 1920×1080 heroes all held. Suspect 9:16 i2v from a soft 770px-wide crop upscaled 2.5×. Not used.
- 2026-10-21 Hunter: skip gate/laundry, 2 reels × 3 clips (0 credits). Clips slowed 0.7× (setpts 1.4 + minterpolate 50 fps, from the 720 sources), powder dapple re-run on the slowed clip with sway periods stretched 1.4×. 608px vertical slice per clip → 1080×1920, 1s dissolves, fade in/out, 18.7s, silent. Reel 1 Arrival: exterior → hallway → kitchen. Reel 2 Inside: living → bedroom → powder v3. Script `work/build_reels.sh` → `reels/`. No text or end card yet (Salisbury branding unknown). Awaiting Hunter review.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
- 2026-10-20 | 35 hf | 08_bedroom seedance_2_5 (gen-runner)
- 2026-10-20 | 35 hf | 11_hallway seedance_2_5 (gen-runner)
- 2026-10-20 | 35 hf | 05_powder seedance_2_5 (gen-runner)
- 2026-10-20 | 35 hf | 06_kitchen seedance_2_5 (gen-runner)
- 2026-10-20 | 35 hf | 04_living seedance_2_5 (gen-runner)
- 2026-10-20 | 35 hf | 01_exterior seedance_2_5 (gen-runner)
- 2026-10-20 | 35 hf | 05_powder_v2 seedance_2_5 (gen-runner)
- 2026-10-21 | 35 hf | 02_gate seedance_2_5 (gen-runner)
- 2026-10-21 | 35 hf | 07_laundry seedance_2_5 (gen-runner)
