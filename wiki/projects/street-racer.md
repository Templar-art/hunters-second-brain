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

## v2: Night GP (same day)
`index.html` is now a night stadium race (v1 is kept as `v1.html`). Six cars, all the real Huracán from [[lambo-huracan|projects/lambo-huracan]], re-exported as `huracan.glb` (4.4 MB). Wheel pivots were added, the car was rotated so its front faces +Y, and the plate text was converted to meshes. Each car gets a clear-coat paint swap, and the head and tail light materials glow. The scene has ACES tone mapping, bloom, RoomEnvironment reflections, floodlight towers, grandstands with an instanced crowd, glowing sponsor walls, a pit building and F1 five-light starts. There's drift physics (separate lateral velocity, handbrake drops grip), smoke sprites, instanced skid marks, a 7-speed automatic box, and a hood/chase/high camera toggle on C.
- **Sound:** the low and high loops are cut from Hunter's Huracán recordings in Downloads (12–19 s cruise, 61–66 s full rev), crossfaded and pitched by RPM. They are local only (`*.wav` is gitignored), with a sawtooth synth fallback.
- **Lesson:** gearbox hysteresis. If the RPM right after an upshift is below the downshift point, the box flip-flops and kills the throttle. Compute RPM as speed over the gear's top speed and keep the downshift threshold well below the post-shift RPM.
- **Lesson:** keep the bloom threshold around 0.95, or every white surface glows.
- **More cars:** a research pass found the vecarz F40 (120k tris, the closest to the Huracán's realism), plus low-poly GT-Rs and CC0 Quaternius/Kenney kits. None are downloaded yet.

## v3: Garage, 14 cars, drift mode (same day)
- **Cars (14):** Huracán, F40, Supra MK4, RX-7 FD, AE86, Skyline R34, Silvia S15, 930 Turbo, BMW M3 Competition G80, M3 CS Touring, M4 GT3 Touring 24h, M5 Competition, Audi R8 and Audi RS5. All came free from Sketchfab via Chrome. An M4 Competition G82 is in the roster code but its download never landed; drop `cars/m4.glb` in and it appears. The McLaren F1 came as a `.7z`, and nothing on the Mac opens that format.
- **Prep pipeline:** headless Blender (`Blender -b -P runcar.py -- name path flip`), four at a time, using the `carprep.py` functions:
  1. Import any of glb, gltf, fbx, obj or blend.
  2. Decimate to 180k tris and shrink textures to 1024.
  3. Normalise to real length, facing +Y.
  4. Detect wheels from tyre-shaped loose parts. Where that fails, place static wheel pivots estimated from the body box.
  5. Tag the largest body material `paint` and export WEBP GLBs.
  6. Run `glbfix.py` to strip texture references whose image never exported. Blender leaves sourceless texture stubs that crash three's GLTFLoader.

  Sources sit in `cars_src/`, which is gitignored.
- **Garage:** a showroom turntable built off to the side of the circuit. It has paint swatches plus a custom colour picker, and five finishes (gloss, metallic, matte, chrome, pearl). There are rim colours, ride height and camber, plus tyre smoke colour, underglow and an exhaust flames toggle with a "Rev it" test. The tune sliders cover power, gearing, grip, drift balance, brakes, steering lock and weight. Setups save per car in localStorage.
- **Handling rewrite:** velocity stays in world space and the body yaws, so rotation becomes slip naturally. Grip bleeds slip off, power-over and the handbrake loosen the rear, and there's counter-steer assist. Steering uses real geometry (`v·tan(δ)/wheelbase`), reverse works on S, and the gearbox has wider hysteresis.
- **Map fix:** walls and gravel crossed the road on tight corners because ribbon offsets bigger than the turn radius fold over. Inside offsets are now clamped to 0.82× the smoothed local radius, and the wall collision follows the clamped line. Grandstands, towers and the pit building now skip any spot within reach of another part of the track.
- **Exhaust spit flames:** additive sprites with a blue core plus an orange flash light, triggered on upshifts and for about half a second of crackle after lifting at high RPM, with noise-burst backfire pops.
- **Drift mode:** a 90-second solo run. Slide angle × speed builds a combo, holding it raises a multiplier up to x5, and a wall hit loses the combo. Best score is saved.
- **Lessons:** source files carry junk that blows out under bloom (flat emission, transmission body shells, magenta missing-texture colours), so neutralise it at load. Splitting 100k+ tri meshes into loose parts in Blender stalls, so decimate first and skip the split on models already in many parts.

## Next ideas
Touch controls, more tracks, wheel detection for the static-wheel cars (G80, M5, R8, RX-7, 930, M4 GT), the G82 M4, a published link.
