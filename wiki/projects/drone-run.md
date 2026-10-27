---
type: project
tags: [game, three-js, blender, side-project]
status: playable-prototype
updated: 2026-10-27
---

# Drone Run

A browser game built in one session on 2026-10-27, as a test of whether Claude plus [[blender-blockout-pipeline|Blender]] can make a video game. You fly a DJI-style drone around a procedurally laid-out suburb and pass through blue "shot markers" before golden hour ends. Each shot adds five seconds. Roofs, trees, poles and powerlines crash you.

- **Code:** `projects/drone-run/index.html` is a single file of Three.js 0.160 loaded from the CDN. It runs via the `drone-run` launch config (port 8170).
- **Models:** `drone.blend` → `drone.glb` (a Mavic-style quad whose prop nodes `prop_0..3` spin in the game) and `houses.blend` → `houses.glb` (three variants: a brick hip-roof house with a garage, a double-storey render home with a balcony, and a verandah cottage with solar panels). The game swaps the `wall` and `roof` materials per instance for colour variety.
- **Cost:** no credits. Everything was modelled with bpy primitives through the Blender MCP, with no generators.

## Lessons
- Blender has had no game engine since 2.8, so the split is Blender for assets (GLB) and Three.js in the browser for the game. That gives zero installs, playing on the spot in the preview pane, and a link to share.
- Join each house variant into one mesh before export. That keeps draw calls to about one per material per house.
- Derive colliders from mesh vertices above 0.2 m, so flat driveways and decks stay flyable.
- Axes: Blender +Y front exports as glTF −Z, which is Three.js forward.

## Next ideas
Touch joysticks for phones, parked cars and fences, and a published link.
