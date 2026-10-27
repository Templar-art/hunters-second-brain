---
type: project
tags: [game, three-js, blender, side-project]
status: playable-prototype
updated: 2026-10-27
---

# Street Racer

A three-lap arcade racer built in the browser on 2026-10-27, straight after [[drone-run]] and on the same stack (Three.js plus Blender-built GLB models). You race three AI rivals around a closed suburban circuit. Grass cuts your top speed and houses and trees stop you dead. The HUD shows position, lap, lap time, a saved best lap, a minimap and km/h.

- **Code:** `projects/street-racer/index.html`, run via the `street-racer` launch config (port 8175).
- **Models:** `car.blend` → `car.glb`, a lofted sports-coupe body with a glass cabin, spoiler and lights. The wheels are nodes `wheel_FL/FR/RL/RR` that spin, and the front pair steer. Each car's colour comes from swapping its `paint` material. The scenery reuses `houses.glb` from Drone Run.
- **Track:** a closed CatmullRom spline sampled into 800 points, giving the road ribbon, red-and-white kerbs, centre dashes, a start/finish chequer and a gantry. The AI aims at a point ahead on the spline and brakes for upcoming corners based on how sharply the track turns.
- **Cost:** no credits.

## Lessons
- A spline track is the right backbone: one sampled point list drives the road mesh, lap counting, AI steering, the off-track check and the minimap.
- Lap counting has to detect the car crossing from the end of the sample list back to the start (and the reverse), so a car that backs over the line doesn't gain a lap.
- A Blender subsurf modifier shrinks the body, so lights and grilles placed against the unsmoothed shape float off it. Place them after a look at the smoothed result.

## Next ideas
Touch controls, engine and skid sound, drift smoke, more tracks, a published link.
