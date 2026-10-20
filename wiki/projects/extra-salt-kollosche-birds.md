---
type: project
tags: [extra-salt, blender, vfx, camera-tracking, drone]
status: delivered
updated: 2026-10-20
---

# Extra Salt — Kollosche gulls comp

Hunter asked for birds to fly past a 1.9s Pottsville drone wide from the Kollosche reel, with the footage keeping its exact grade. Job folder: [JOB.md](../../projects/extra-salt-kollosche-birds/JOB.md). Cost: $0, all local.

**What shipped:** four procedural silver gulls composited over the untouched plate (verified 0 px change outside the birds). Delivered as H.264 and ProRes 422 HQ with the original audio.

**Route:** Blender CG comp, not AI. Video-to-video models repaint every pixel and shift the grade, which breaks the drone-wide rule in [[higgsfield-pipelines]].

## What it taught us
- **Check the last frame of an exported clip.** Frame 46 was a hard cut to the next shot, and it blew the solve up to 5.6 px on that frame.
- **Low-parallax drone moves defeat Blender's free solve.** It gave 0.1–0.4 px reprojection error, but the camera path flipped between push-in and pull-back across runs and had a fake jerk at frame 2. The fix (`scripts/02_fit_camera.py`) was to fit a constrained drone camera with OpenCV LK tracks and scipy: flat ground, straight-line travel, global pitch and focal length, then per-frame travel and gimbal rotation smoothed with a cubic. Result: 0.21 px median error across 1,478 points. Reuse it for any drone plate.
- **Image scale alone can mislead.** The homography determinant suggested a push-in, but per-row feature motion showed contraction, so it was actually a pull-back.
- **Gulls crossing a drone frame side-on read as crosses or "T" shapes.** Fly them diagonally away from camera and bank them 10–15° so the drone sees their backs and the M-shaped wings.
- **Small CG birds on a warm plate need warm light.** A blue sky fill made them look cold. A ~0.2 shutter (about 1/120 s) keeps wing blur believable.
- Blender clip-tracking ops need the GUI (a Clip Editor area). Run them with `Blender --python` plus a timer and `temp_override`, not `-b`.

Related: [[blender-blockout-pipeline]], [[house-twilight]].
