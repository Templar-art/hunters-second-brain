---
type: concept
tags: [vfx, roadmap, drone, sfx, research]
status: parked
updated: 2026-10-21
---

# Plate-VFX roadmap: what to build after the birds

Research pass on 2026-10-21. The question: now that [[plate-vfx]] can drop CG birds into a drone clip with the plate untouched, what else is worth building for 10x's real-estate clients?

## What we already have (and what it unlocks)
The birds job gave us four reusable parts. Most ideas below only need a new *element*, not a new pipeline:
- **Camera solve.** A constrained drone fit at sub-pixel accuracy, with a known lens, ground plane and camera path per frame. Anything placed in the 3D scene sticks to the footage.
- **Plate match.** Sky-derived fill, sun warmth and grain-matching, so CG sits inside the existing grade.
- **Alpha composite.** It guarantees the plate's pixels outside the alpha are bit-exact. This is the "grade identical" promise.
- **Audio.** Real-recording grain sync plus procedural SFX ([[sfx-custom]]), and Demucs is installed locally (`~/.venvs/demucs`).

## Ranked next steps

| # | Build | Client value | Effort | Reuses |
|---|---|---|---|---|
| 1 | **Tracked sun flare + SFX**, the pending "sunshine lens flare" clip | quick win, polish on every hero shot | low | solve (sun position), [[sfx-custom]] shing/flare WAVs |
| 2 | **3D-tracked property graphics**: lot boundary lines, labels, distance-to-beach callouts locked to the ground | high, since agents love it and it's sold widely as a freelance service | low–med | solve + ground plane; Blender curves, no AI |
| 3 | **Tracked sky replacement** | high, because it rescues grey-day shoots | med | solve drives an HDRI dome, so 360° turns work |
| 4 | **Day-to-dusk *video*** ("virtual twilight" for drone clips) | very high, a market gap | med–high | #3 sky + CG window glow + garden/pool lights placed in 3D + grade |
| 5 | **CG house into an empty lot, video** | very high for off-the-plan sales | high | solve + Blender model (see [[lot-48-belle-property]], the stills version) |
| 6 | **Canal and water life**: boats, a moored yacht, a jet ski with wake foam | high for Gold Coast canal homes | high (water interaction) | solve + layout + flock-style path sim |
| 7 | **Gaussian-splat flythroughs** | new service line | med | separate capture (slow orbits), not the plate pipeline |
| 8 | **Auto sound-design pass**: `sfx` stage in plate-vfx | internal speed | low–med | port `06_flap_real.py`; one-shot library from cut reels |

### 1. Tracked sun flare
The camera solve already knows where the sun sits relative to the camera, because plate-match estimates sun warmth and direction. A flare element (ghosts, streak, glow) can be rendered at the projected sun position in every frame. It then moves correctly with the drone instead of being hand-keyed in Resolve. Pair it with `shing_*.wav` / `lens-flare_*.wav` timed to the flare's peak frame. Next: Hunter's clip with the flare.

### 2. Tracked property graphics
Freelance sellers do this with After Effects 3D camera tracking plus GeoLayers map animation ([Fiverr example](https://fiverr.com/khasiya_editor/edit-real-estate-drone-video-with-3d-camera-tracking-and-geolayers-map)). Our solve already gives a metric ground plane, so lot lines can be drawn in Blender and render as a clean alpha over the untouched plate. No credits are spent. The open question is the lot-outline source: the agent's plan, or tracing from the first frame.

### 3. Tracked sky replacement
Resolve has had a Sky Replacement OFX since 18.1 ([guide](https://dvresolve.com/tutorial/new-sky-replacement-feature/)). Users report it stops working on big drone turns, because the sky is a flat 2D plate that "just stops during the turn" ([forum](https://mavicpilots.com/threads/sky-replacement-in-davcinci-resolve.150613/post-1690753)), and its track-the-original-sky mode works poorly ([BMD forum](https://forum.blackmagicdesign.com/viewtopic.php?p=1043814)). Ours would map a 360° HDRI sky onto a dome driven by the solved camera, so rotation is exact. The hard part is the sky matte: hair-fine tree edges and roof lines. The hard rule applies: masked, never full-frame AI on a drone wide.

### 4. Day-to-dusk video
Every day-to-dusk product found is for stills (Imagen, MyArchitectAI, [Imagen 2026 guide](https://imagen-ai.com/post/ai-day-to-dusk-conversion-real-estate-2026/)). MyArchitectAI's pitch is that cheap twilight edits look fake because they only swap the sky and never relight the building ([source](https://www.myarchitectai.com/virtual-twilight)). That vendor claim matches our instinct. The video version is an open gap. Build it as #3 plus a dusk grade plus window glow (masks tracked to the house) plus warm practical lights placed in 3D. Optional help is Beeble SwitchLight 3.0, which turns video into PBR passes (normals, depth) for relighting without a 3D rebuild ([digitalproduction](https://digitalproduction.com/2025/11/11/beeble-launches-switchlight-3-0/)). It's paid, so the money gate applies, and it's untested on drone wides.

### 5. CG house into an empty lot (video)
This is the video version of the Lot 48 still. It needs the solve, the architect's model or a block-out ([[blender-blockout-pipeline]]), a sun matched by plate-match, and contact shadows on the ground plane. It's the biggest-ticket item, so price it on value ([[cva-woomala-render-enhance]] lesson).

### 6. Canal and water life
Boat-on-water integration is the hard part: wake foam and reflections. Blender Studio's "Gold" production documents boat-wake foam FX ([studio.blender.org](https://studio.blender.org/films/gold/?asset=7351)), and there are procedural Geometry Nodes boat generators ([Cubebrush](https://www.cubebrush.co/3d_tudor/products/wnzooq/3dt-boat-generator-blender-geometry-node-procedural)). Start easy with a *moored* boat (gentle bob, no wake), then add a slow cruiser with a simple foam trail.

### 7. Gaussian-splat flythroughs
Zillow SkyTour uses Gaussian splats for listing exteriors ([lidarnews](https://lidarnews.com/zillow-3d-tours-with-gaussian-splatting/)). Giraffe360 sells splat-rendered "drone-style" video ([thread](https://www.wegetaroundnetwork.com/topic/21085/giraffe360-g-splat-rendering-for-higher-quality-drone-stylecinematic-video)). Luma retired its Flythroughs app on 1 Jan 2026 ([radiancefields](https://radiancefields.com/luma-ai-to-sunset-flythroughs-on-january-1-2026)), which leaves room in the market. Capture is a slow, constant-altitude orbit with heavy overlap, avoiding reflective surfaces and moving objects ([SkyeBrowse](https://www.skyebrowse.com/news/posts/gaussian-splat-from-video)). The upside is that any camera move can be invented after the shoot. It's a separate track from plate-vfx.

### 8. Auto sound-design pass
Open video-to-audio models exist, but HunyuanVideo-Foley is **research/non-commercial only** ([Replicate](https://replicate.com/tencent/hunyuanvideo-foley)), so it can't be used on client work. MMAudio's licence is unverified. The licence-clean route is our own: element-synced placement (as with the gull flaps) from a growing one-shot library. That library comes from [[sfx-custom]] plus reels cut with Demucs.

## Status (2026-10-21)
- **#2 lines: built.** `plate_vfx.py lines` + `marks.json`. On the Kollosche benchmark, lot corners hold within 0.4 px of optical flow and the plate is untouched.
- **#3 sky: built.** `plate_vfx.py sky`. SegFormer matte carried by the camera rotation, Poly Haven CC0 HDRI dome, plate untouched. The best day sky is kloofendal_48d.
- **#4 dusk: SHELVED (2026-10-21).** Hunter rejected both attempts, and day-to-night from a daytime drone wide isn't working.
  - **v1 (2D grade + pasted glows):** read as a dark filter with sticker lights.
  - **v2 (Depth Pro relief mesh on the solved ground plane, Cycles + dusk HDRI, glossy water, marked windows; `lib/relight.py`, `blender/build_relight.py`):** physically lit, but it looked like a dim afternoon. Only the hand-marked hero windows glow.
  - **Hard blocker:** automatic window finding fails at drone scale. SegFormer finds 0 windows, dark-patch detection flags shadows and recesses, and rectangle detection flags solar panels. Without lights in every house, dusk reads fake.
  - **Reusable pieces:** the relief-mesh trick (Depth Pro gives local relief only; the solve owns the metric ground) and the building/water masks.
  - Don't retry without a real window-detection answer, or a client-supplied twilight reference.
- **#2 lines and #3 sky:** Hunter called the lines cheap and the whole direction wrong, so both are parked. See [[feedback-vfx-no-2d-fakes]] in auto-memory.
- **#1 flare:** waiting on Hunter's clip.
- The benchmark barely moves (3–6 px total). Re-test the lock on a clip with a real drone move before selling it.

## Suggested order
#1 (the clip is already coming) → #2 (cheap, sellable now) → #3 → #4 (the differentiator). #5 and #6 wait until a client asks; #7 is a separate experiment.
