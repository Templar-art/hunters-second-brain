---
type: project
tags: [project, cinemagraph, seedance, video, 9x16, salt-pm]
status: delivered
updated: 2026-11-11
---

# Solis, 673 Casuarina Way — pool cinemagraph (Oct 2026)

One real listing photo (Solis 673 Casuarina Way, Salt PM, frame 16) made into a 10-second 9:16 cinemagraph for posting. Everything stays frozen except the pool water, the wall spout and the clouds. Client: [[salt-pm]]. Job folder: [projects/solis-673-casuarina-cinemagraph/](../../projects/solis-673-casuarina-cinemagraph/JOB.md). Deliverable: `video/pool_cinemagraph_v2_sky.mp4` (1080×1920, 24 fps, silent). **Cost: 160 hf credits** (one Seedance generation; the sky pass was free).

## What worked
1. **Crop to 9:16 locally first** (full-height 3564px slice at x=3270 of the 9504px original, centred on the pool) and use it as the start image, so the AI isn't the one choosing the framing.
2. **Seedance 2.5 i2v** (`seedance_2_5`, `omni_reference`, 1080p, 10s, audio off, 160 hf; 720p is 70 hf). The prose prompt opens with a hard camera lock ("locked-off tripod, zero camera movement, framing identical to the start image"), says "this is a cinemagraph" and lists everything that stays still, including the woman sitting on the pool edge. Then it describes only the water: ripples, drifting caustics, rings around her feet, a steady sheet from the spout. One pass held: frame locked, she stays still, and the water and spout move convincingly.
3. **Sky motion added locally, not re-rolled** (Hunter asked for it after v1). Build a sky mask from the still (geometry polygon AND colour key: blue or bright/low-sat, which drops the tree; small pockets forced in by hand), then composite the still's sky over every v1 frame with a slow zoom (1.00→1.16) **anchored at the top-right corner of the sky**. Zooming toward an anchor inside the sky only samples sky pixels, so no house or tree edge gets dragged in. A pan would need a clean plate. Script: `work/build_v2.py`. 0 credits.

## Lessons
- For "only X moves" briefs, try Seedance with a hard camera lock plus an explicit still-list before reaching for masks. It held a person still.
- Add secondary motion (sky, clouds) in post over an approved AI pass instead of re-rolling, because a re-roll can lose the water you already approved. Anchored zoom gives clouds a glide, not a billow. If a client needs real billowing time-lapse clouds, that's a re-roll.
- QC the sky mask at the **last** frame, where displacement is largest. A static sky pocket under the eave showed up there as a hard vertical seam.
- `gen_runner` flags cinemagraphs **NO_MOTION**. It measures the whole frame, so that's a false positive here; check motion per region (pool vs house vs sky) instead.

## Reused
- [[vista-renders]] (Oct 2026) ran this recipe on 8 developer renders. It held at 16:9 from full-width heroes, but 9:16 from a narrow upscaled crop re-imagined the frame — **⚠️ qualifies step 1 above**: the local 9:16 crop worked here from a 3564px-tall original, not from a low-res crop. Some compositions barely move at all.
