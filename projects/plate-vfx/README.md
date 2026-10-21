# plate-vfx (v1: birds)

Puts CG birds into real footage. The plate is never re-rendered: CG is composited over it, and the
render step proves that nothing outside the CG alpha changed. The skill that drives it is
`~/.claude/skills/plate-vfx/SKILL.md`. The wiki write-up is [[plate-vfx]].

```bash
python3 plate_vfx.py prep   "<clip>" --job <dir> [--aspect 16:9|9:16|4:5|1:1] [--count 4] [--seed 1] [--direction 1|-1]
python3 plate_vfx.py layout <dir> --seed 2        # re-route
python3 plate_vfx.py pilot  <dir> --tier standard --frame 12
python3 plate_vfx.py render <dir> --tier draft|standard|hero
```

## Stages
| Stage | File | What it does |
|---|---|---|
| init | `plate_vfx.py` | Extracts PNG frames and detects hard cuts (frame diff greater than 8× the median). CG only runs inside the longest cut-free range. |
| track | `lib/track_fit.py` | Forward/backward-checked LK tracks feed a flat-ground drone-camera fit. There are two models: `line` (straight travel plus gimbal) and `free` (6-DOF per frame, smoothed). `auto` picks one. The gate is a mean error under 0.5 px. Output: `camera.json`. |
| match | `lib/plate.py` | Measures sky colour (linear), warmth (R/B) and grain sigma in the flattest blocks. Output: `plate.json`. |
| layout | `lib/layout.py` | Random search over flight parameters. Each candidate is simulated through the camera and scored on time inside the safe area, edge entry, readable size and spacing between birds. Outputs: `layout.json` and `layout_preview.jpg`. |
| flock | `lib/flight.py` `simulate_flock` | Leader path (auto-routed) + N members: ellipsoid slots (0.22/0.28/0.06 × depth) with smooth-noise drift, per-member lag ±0.25 s along the leader path, separation relaxation (≥1.6 m), temporal smoothing, heading/bank/pitch from each member's own velocity (coordinated turns), own wingbeat, 75 % share the leader's glide with ±0.15 s jitter. 24 birds sim in 0.04 s; standard render of 26 birds ≈ 33 s. |
| flight | `lib/flight.py` | The shared flight simulation: asymmetric wingbeat, wrist fold, body lift, glides, coordinated banked turns. Keys every half frame. |
| build/render | `blender/build_birds.py` | Builds the tiered scene (camera, plate background, plate-matched light, gulls) and renders an RGBA pass to `render/<tier>/`. |
| comp | `lib/plate.py` | `plate*(1-a) + (cg+grain)*a`, bit-exact outside the alpha, then `verify()`. Exports mp4, ProRes 422 HQ and ProRes 4444 alpha. |

## Tiers (Kollosche benchmark: 1080p, 45 frames, M-series Mac)
| Tier | Gull | Engine | End to end |
|---|---|---|---|
| draft | procedural, ~500 polys, 50 % res, no blur | EEVEE 8 spp | ~10 s |
| standard | rigged herring gull, 4.8k faces, motion blur | EEVEE 64 spp | 28 s |
| hero | herring gull + subsurf L1 (~19k faces) | Cycles 128 + OIDN | 6 min (looks ≈ standard at <200 px bird size; only worth it for close birds) |

## Assets
`assets/gull_herring.blend` contains `GullRig` (body, arm.L/R, hand.L/R) and `GullHerring` (mesh, packed 2K texture).
- Source: "realistic_seagull_3d_model" by Pofdpoi on Sketchfab, CC BY 4.0.
- Credit it when it's used in client work.
- Modified: feet removed (gulls tuck them in flight), rotated so the model faces +Y, origin set between the shoulders, rigged with hand-ramped weights (shoulder blend at |x| 0.035–0.085, wrist blend at 0.21–0.27).
- The wing pose maps to bones as `B⁻¹·R·B`, where B is the bone's rest matrix.

## Limits and next upgrades
- Tracks must survive the whole range, so long or fast shots need keyframe chaining (not built yet).
- Flat-ground prior: fine for aerials. Ground-level shots with big parallax should use Blender's solver (`extra-salt-kollosche-birds/scripts/01_track.py` shows how).
- Next: feather-card wing edges for hero, sun direction read from the plate, more subjects (drones, boats).
