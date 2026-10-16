---
type: concept
tags: [ai-video, blender, higgsfield, magnific, pipeline]
status: setup-complete
updated: 2026-10-16
---
# Blender block-out → AI video pipeline

Claude builds a rough 3D block-out (grey geometry, real metre sizes, locked camera path) in Blender, renders a clay/depth pass, and that pass becomes the structure reference for a video-to-video or first/last-frame generation in [[higgsfield-pipelines|Higgsfield]] or Magnific. The block-out fixes camera motion and proportions; the AI only paints the surface. This removes AI video's main failure, random camera drift.

## Install (done 2026-10-12)
- Blender 5.2.2 via Homebrew cask (`/Applications/Blender.app`, CLI `blender`).
- `blender-mcp` server (PyPI, run via `uvx`), registered user-scope in Claude Code as `blender` with `DISABLE_TELEMETRY=true`.
- Addon "MCP for Blender" v1.8 (`~/BlenderMCP/addon.py`, github ahujasid/blender-mcp) installed and enabled in Blender prefs. Addon telemetry is off by default; leave it off. Optional paid add-ons (Hyper3D, Sketchfab, premium) are not needed.
- Headless test passed: Claude rendered a grey room block-out with `blender -b -P script.py` in about 3s.

## Two modes
- **Headless** (no UI): Claude writes `bpy` scripts and runs them with `blender -b`. Best for automated batches.
- **Live MCP**: Blender is open and the addon's "Connect to Claude" is clicked, so Claude edits the scene in real time. Best for iterating with Hunter watching.

## Alternative
Magnific's MCP has a built-in 3D Scene builder (cameras, keyframes, captures) that appears free to build in. Only the generation step is metered. Untested at the time of setup.

## Rules
Building the block-out is free. The generation step always gets a cost quote and Hunter's go-ahead first. Never full-frame a drone wide (see [[staging-rules]]).

## Block-outs built
- 2026-10-12: [living-room-pushin-v1.blend](../../projects/blender-blockouts/living-room-pushin-v1.blend), the first live-MCP test. A 5×4m room with the sofa on the back wall and a 24mm push-in from 1.9m to 0.5m back over 5s (120f @24fps). Gotcha: in a script, calling `frame_set()` between keyframe inserts re-evaluates the animation and overwrites the new pose, so pass `frame=` to `keyframe_insert` instead.

## Default route (2026-10-12, Hunter picked it after the shot-1 test)
Blender guide frame → **GPT Image 2.5 Sunburst** (high, 2K, about 2.75 HF credits) for an **editorial** look → **Seedance 2.5 on Higgsfield** (omni_reference start frame, 96 HF credits per 8s at 1080p). Kling 2.5 on Magnific (725cr for the test) held the move but redesigned the pool late in the clip, so it is not the default.

## Material-ID colour map (2026-10-16)
Each material is rendered as one flat colour, then passed to the image model as a second reference with a key written in prose ("wherever Image 2 is red, the surface is timber…"). The model then knows which surface is which instead of guessing. Script: [material_id_pass.py](../../projects/blender-blockouts/scripts/material_id_pass.py) sorts every material by name into 17 categories: red timber, cyan glass, grey concrete, white render, black metal, blue pool, navy ocean, yellow sand, green grass, dark green plants, brown trunks, magenta fabric/furniture, orange stone, and so on. It uses Standard view transform and flat emission so the colours stay exact. Thin glass (fences, balustrades) is hidden from the map so it doesn't paint over what sits behind it.

## Scene density matters
Hunter's verdict on the first beach build (274 objects): too bare. The rebuild went to about 1,600 objects: dune-grass scatter, hedges, tropical garden beds, potted plants, outdoor dining, an umbrella, mullions, gutters and downpipes, a boardwalk, street lights, cars, eight detailed neighbour houses, and a full walk-through interior (stairs cut through the slabs, a garage, laundry, powder room, and a master suite with ensuite and robe). An empty block-out gives the AI room to invent; a dense one leaves it nothing to make up.

## Add-ons worth installing (research, 2026-10-16, not yet verified live)
Ranked for a Python/MCP-driven pipeline:
1. Poly Haven (free, already wired in)
2. BlenderKit (free tier / about $9 a month)
3. Camera Shakify (free, real gimbal feel)
4. Archipack (free, parametric walls, windows and roofs)
5. Botaniq (about $49+, landscaping)
6. Photographer 5 (about $30)

Skip Geo-Scatter, Kitbash, Fab and Fluent for now: they're weak to drive from a script. Spend on silhouette, vegetation shape and camera motion, because the AI repaints the surfaces anyway.

## Model shootout: guide + colour-ID map, same prompt (2026-10-16, 12.25 HF credits)
Run on the beach house pool shot. Grid: [shootout-grid.jpg](../../projects/blender-blockouts/beach/shootout/shootout-grid.jpg).

| Model | Result |
|---|---|
| **Seedream 5.0 Pro** (2.5 cr) | Most photographic and closest to the layout. It turned the hedge into a concrete wall. Default when realism matters. |
| **GPT Image 2.5 Sunburst** (2.75 cr) | Most editorial and lush, but it re-framed slightly and swapped some elements. Default when the editorial look matters. |
| **Nano Banana 2.1** (2 cr) | Very real, but leaked the magenta and lavender key colours into the image. |
| **FLUX 3** (3 cr) | Faithful, got the hedges right, slightly CG-looking. |
| **Nano Banana Pro** (2 cr) | Weakest; heavy key-colour leaks. |

**Lesson:** key colours that look like real paint (magenta, lavender) leak into the image. Neighbour houses now share the house-render white, and people moved to purple.

## People and camera realism (2026-10-16)
- **MPFB2 2.0.18** (free, official Blender extension, 46MB, checksum-verified) is installed. `HumanService.create_human(macro_detail_dict=…)` takes gender, age, height, weight and muscle; `add_builtin_rig(h,"default")` adds the skeleton. The body faces −y. Bending the leg forward is upperleg01 −X; the knee bends on lowerleg01 +X. Arms rest at upperarm01 Z −45 (L) / +45 (R) from the A-pose. A walk cycle is upperleg ±23°, knee 4–38° and arm swing ±14° over 26 frames with CYCLES modifiers. Each human is parented to a `Rig_` empty that carries its walk path. No clothes or skin pack yet; the AI dresses them from the prompt.
- **Camera Shakify 0.5.1** (free, 78KB) is installed. Walking shots use WALK_TO_THE_STORE at 0.25–0.35; static or glide shots use INVESTIGATION at 0.15–0.2. It replaces the generic F-curve noise on those cameras.
- **Tracking shot:** the camera keeps a TRACK_TO on an empty that copies the walker's location at chest height, while the camera itself runs a parallel path.
