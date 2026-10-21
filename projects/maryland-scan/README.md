# 18 Maryland: photogrammetry rebuild

Goal: rebuild 18 Maryland 1:1 in Blender so the CG Huracán ([[lambo-huracan]], `../lambo-huracan/maryland/`) can drive down the real drive with a free-moving camera.

Source: 10x's own shoot on the Kristian T7 SSD, `18 Maryland /` (shot 2026-09-30): 18 DJI drone clips (4K50) and 335 Sony clips (4K50, S-Log). Working copies are in `drone/` and `ground/` (gitignored).

Method: Apple Object Capture (RealityKit `PhotogrammetrySession`, free and on-device), wrapped as `tools/scan.swift`.
- Drone set: clips 1, 2, 3, 5, 6, 7, 8, 9, 15, 16 at 3 fps → `frames3/` → `scan_full.usdz` (roof, rear, pool, footprint).
- Ground set: C4909–C4914 (walk up the drive) and C5071–C5077 (gate and sign wall, same vantage as the listing photo) → `frames_ground/` → entry and drive.
- `tools/look.py` renders unlit orbit views of a scan for QC.

Notes: Object Capture closes every mesh with a hull skin; crop it in Blender. Scans come out unscaled (about 1 unit across), so they are scaled from a known dimension and aligned to the listing-photo camera solve.

Also usable: C5075–C5077 are real dusk moving shots through the gate. A tracked composite into those (plate-vfx) is the cheapest route to a real camera move.
