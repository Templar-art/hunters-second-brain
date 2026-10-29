---
type: project
tags: [coastal, blender, vfx, camera-tracking, drone, pin]
status: in-review
updated: 2026-10-29
---

# Coastal 34 Albany Ave: CG gulls + tracked Coastal pin

Drone shots from Hunter's Katrina Walsh / [[coastal]] film of 34 Albany Avenue, Currumbin (`Downloads/Kollosche Ester Place/Costal 43 Albany Stuff/Main.mp4`, 4K 23.976, 71.6 s). Job folder: [JOB.md](../../projects/coastal-albany-birds/JOB.md). Cost: $0, all local. The sound pass for the same film is in [[auto-sound-design]].

**Shots** (cut out of the film as their own clips and run through [[extra-salt-kollosche-birds|plate-vfx]]):
- **A treetops 0–2.2 s:** skipped. There's no sky, the Coastal logo is on screen, and the draft birds came out yellow and huge.
- **B coast wide 44.42–47.05 s:** the tracked Coastal pin goes here, on the house in the middle of the frame (frame-1 ground point 1985, 1335 at 4K). Two looks: the white stem + C° mark (same art and timing as `projects/coastal-katrina/animate.py`), and the same with "34 Albany Avenue / Currumbin" in Poppins. The pin holds on the house from first to last frame. **Hunter picked the plain C° pin (29 Oct)**, which matches the Coastal house style in [[coastal]]. The address card wasn't used. Script: `projects/coastal-albany-birds/coastal_pin.py`.
- **C hazy sunrise 64.69–67.3 s:** four rigged herring gulls at the standard tier, crossing the backlit haze.

Each output has a comp `.mp4` plus an alpha `.mov` to lay over the film in FCP. The gull asset needs the credit "Pofdpoi (Sketchfab), CC BY 4.0".

**29 Oct changes (Hunter):**
- The end card's charcoal gradient read tacky. `projects/coastal-katrina/animate.py endcard-alpha` now renders the name, number and COASTAL° wordmark on transparency only.
- He asked for bird flapping. New `projects/plate-vfx/flap_sfx.py` re-runs the render's flight simulation, finds each downstroke, and places a real wingbeat grain on it, with level and high-cut set by distance and pan set by screen x. 29 flaps for the 4 gulls, written as a full-film-length WAV so it lines up at 0:00.
- The end-card whoosh was removed. Only the two approved whooshes play, locked with `presets/coastal-albany-locked.json`.

## What it taught us
- **The track gate has to scale with resolution.** The 0.5 px gate was set on the 1080p benchmark, so it failed all three 4K shots (0.58–0.79 px, the same as 0.29–0.39 px at 1080). `plate_vfx.py track` now uses 0.5 × width/1920.
- **The auto layout puts birds over the treetops when the drone is climbing and pushing in.** The birds sink and get left behind within a second. Hand-placing them in the sky took four draft passes:
  - near and slow: they leave the frame;
  - flying forward with the camera: they shoot off into the distance;
  - far: they're specks;
  - final: depth 30–60 m on the solve's prior scale, 10–18 m/s, a 30–45° heading, starting high in the sky.
  Draft renders take about 8 s at 4K, so iterate on the draft tier and only render the standard tier once.
- **The solve's metric scale is only a prior** (120 m altitude). Bird depth and speed in metres don't mean real metres. Tune them by how they look on screen.

## 29 Oct, Cinematic Reel (9:16): tracked pin + start/end cards
- Same plain C° pin on the reel's coast-wide drone (27.94-30.49 s). That shot is a tighter, later take than the one in Main, so it was re-tracked from the reel itself rather than reusing B's solve. The track passed at 0.50 px.
- **The plate-vfx track gate now scales by the long side.** At 1080 px wide, a 9:16 clip had been held to 0.28 px and failed a good track.
- **Vertical pins need to be bigger.** At the 16:9 proportion the C° was about 5% of frame width, which reads tiny on a phone. `coastal_pin.py --scale 1.4` fixes it.
- Cards: `projects/coastal-katrina/reel_cards.py` builds the start card (KATRINA WALSH / PRESENTS over the opening drone) and the alpha-only end card at 1080x1920, 23.976 fps. Everything sits above the bottom 25% of the frame, where Instagram's caption UI covers it.

