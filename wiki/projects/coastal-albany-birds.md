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
- **B coast wide 44.42–47.05 s:** the tracked Coastal pin goes here, on the house in the middle of the frame (frame-1 ground point 1985, 1335 at 4K). Two looks: the white stem + C° mark (same art and timing as `projects/coastal-katrina/animate.py`), and the same with "34 Albany Avenue / Currumbin" in Poppins. The pin holds on the house from first to last frame. Script: `projects/coastal-albany-birds/coastal_pin.py`.
- **C hazy sunrise 64.69–67.3 s:** four rigged herring gulls at the standard tier, crossing the backlit haze.

Each output has a comp `.mp4` plus an alpha `.mov` to lay over the film in FCP. The gull asset needs the credit "Pofdpoi (Sketchfab), CC BY 4.0".

## What it taught us
- **The track gate has to scale with resolution.** The 0.5 px gate was set on the 1080p benchmark, so it failed all three 4K shots (0.58–0.79 px, the same as 0.29–0.39 px at 1080). `plate_vfx.py track` now uses 0.5 × width/1920.
- **The auto layout puts birds over the treetops when the drone is climbing and pushing in.** The birds sink and get left behind within a second. Hand-placing them in the sky took four draft passes:
  - near and slow: they leave the frame;
  - flying forward with the camera: they shoot off into the distance;
  - far: they're specks;
  - final: depth 30–60 m on the solve's prior scale, 10–18 m/s, a 30–45° heading, starting high in the sky.
  Draft renders take about 8 s at 4K, so iterate on the draft tier and only render the standard tier once.
- **The solve's metric scale is only a prior** (120 m altitude). Bird depth and speed in metres don't mean real metres. Tune them by how they look on screen.
