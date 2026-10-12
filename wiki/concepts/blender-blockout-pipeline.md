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
