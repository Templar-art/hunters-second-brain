---
type: project
tags: [project, cinemagraph, seedance, blender, renders, reels, salisbury]
status: active
updated: 2026-11-11
---

# Vista render set: cinemagraphs + 1:1 Blender rebuilds (Oct 2026)

Twelve developer renders of "Vista" (2000×1368) for [[salisbury-building-projects]], worked two ways:

1. **Cinemagraphs → reels** ([projects/vista-render-cinemagraphs/](../../projects/vista-render-cinemagraphs/JOB.md)). Camera-locked Seedance clips with only ambient motion, cut into social reels. **Cost: 465 hf credits** (13 Seedance runs at 35 hf, 8 upscales at 10 hf). Status: reels built, in Hunter's review / FCP edit; client delivery not confirmed (**provisional**, 2026-11-11).
2. **1:1 Blender rebuilds** ([projects/vista-blender-rebuild/](../../projects/vista-blender-rebuild/JOB.md)). Rebuild each render as an owned Cycles scene (same camera, geometry, materials, light) so any time of day and real camera moves become possible with no AI. Only the powder-room pilot is built (v11, 0 credits); the other 11 rooms are todo, awaiting Hunter's review of the pilot.

## Cinemagraph learnings
- **Recipe from [[solis-pool-cinemagraph]] held on renders:** Seedance 2.5 i2v, hard camera lock + explicit still-list. 720p 5s with end frame = start frame (35 hf) instead of 1080p 10s (160 hf) cut the batch estimate from 960 to 210 hf. A seamless loop comes free from start = end.
- **Aspect matters for fixture lock.** 16:9 i2v from a full-width 1920×1080 hero held every time. 9:16 i2v from a soft ~770px crop upscaled 2.5× **re-imagined frame 0** (gate trees replaced, a sink added to the laundry). Generate at 16:9 and cut vertical slices locally.
- **Some compositions won't move.** The powder room gave 0.2% then 0.7% px motion even with a stronger prompt. Stop re-rolling; rank clips by per-region motion and drop the dead ones (living 0.4%, laundry 0.1% dropped from reels). A local procedural leaf-shadow dapple (`work/dapple.py`) was rejected by Hunter as "black dots"; the plain v2 shipped.
- **gen_runner NO_MOTION is a false positive on cinemagraphs** (second time after Solis): measure the moving region, not the whole frame.
- **Upscale on Higgsfield beats lanczos:** Bytedance Video Upscale, 1080p, preset aigc, model pro, 10 hf per 5s (Standard is 1 hf). Clearly sharper fabric/stone/lettering; slightly strengthened a sign glow. Don't pass `--fps` — it makes `higgsfield generate cost` hang.
- Local `minterpolate mci` to 50 fps is free but ghosts fast fan blades.

## Reel learnings
- Hunter's taste across iterations: no dissolves, no fade to black, **hard click-ins/cuts**, slow clips (0.5×–0.75×), 3 best clips per reel beat 4, logo card hard cut at the end with a click + thud. Eased pop-in animation was rejected.
- With music, snap cuts to spectral-flux onsets (`work/sync_pops.py`) and verify within one frame; see also [song cut recipe](../../../../.claude/projects/-Users-10xhunter-Documents-Hunters-Second-Brain/memory/feedback-song-cut-recipe.md) in auto-memory.
- Final direction was **16:9 full-frame, SFX only, no song**: shutter + whoosh on each cut, each clip's own ambience bed under it only (birds/wind outside, curtain + synthesised ceiling fan in the bedroom), hits ~−17 dB over beds ~−30 dB. Commercial songs get muted on IG; Pixabay lofi was the licensed fallback. Builder `work/build_169_seq.py`.

## Blender rebuild learnings (pilot only, provisional)
Method and gotchas live on [[blender-blockout-pipeline]] under "1:1 render rebuild". Headline: camera from the render's vanishing points, primitives sized off the render, CC0 textures, sun matched to shadow directions, QC as a 50% overlay against the render.
