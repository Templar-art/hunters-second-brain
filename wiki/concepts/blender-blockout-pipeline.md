---
type: concept
tags: [ai-video, blender, higgsfield, magnific, pipeline]
status: setup-complete
updated: 2026-10-12
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
