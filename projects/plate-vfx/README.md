# plate-vfx (birds, property lines, sky swap, dusk)

Puts CG birds into real footage. The plate is never re-rendered: CG is composited over it, and the
render step proves that nothing outside the CG alpha changed. The skill that drives it is
`~/.claude/skills/plate-vfx/SKILL.md`. The wiki write-up is [[plate-vfx]].

```bash
python3 plate_vfx.py prep   "<clip>" --job <dir> [--aspect 16:9|9:16|4:5|1:1] [--count 4] [--seed 1] [--direction 1|-1]
python3 plate_vfx.py layout <dir> --seed 2        # re-route
python3 plate_vfx.py pilot  <dir> --tier standard --frame 12
python3 plate_vfx.py render <dir> --tier draft|standard|hero
python3 plate_vfx.py lines  <dir> [--marks marks.json]       # tracked lot outlines + pins
python3 plate_vfx.py sky    <dir> [--sky <polyhaven id>]     # tracked sky replacement
python3 plate_vfx.py dusk   <dir> [--sky belfast_sunset_puresky] [--sun -45] [--ev -2.5]   # day-to-dusk video
```

`lines`, `sky` and `dusk` reuse `camera.json` + `plate.json`, so run `prep` (or init/track/match) first.

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

## Property lines, sky, dusk (added 2026-10-21)
| Stage | File | What it does |
|---|---|---|
| ground | `lib/ground.py` | Back-projects frame-1 pixel marks onto the solved ground plane (z=0) and reprojects them into every frame. Also builds a ground-plane homography. On the benchmark, lot corners hold within 0.4 px of optical flow. |
| lines | `lib/overlay.py` | Reads `marks.json` (`lots` = polygon + label/sub, `pins` = point + label/sub). Draws a 10x blue (#61a8d8) outline with glow, translucent fill, corner dots and white Poppins cards on leader lines. Animated: the outline draws on, the fill fades in, the pins rise. Rendered at 2x for anti-aliasing; no grain or blur. The plate is untouched outside the graphics. First run writes a template. |
| sky matte | `lib/sky_matte.py` | SegFormer-B5 on ADE20K: sky, water (water/sea/river/lake) and pool probabilities. Runs in the ML venv `~/.venvs/demucs` (torch + transformers; override with `PLATE_VFX_ML_PY`). The model downloads from Hugging Face on first use. Only keyframes are inferred. |
| sky | `lib/sky.py` | Carries the frame-1 matte by the pure-rotation homography (the horizon is at infinity, so it can't flicker). Falls back to per-frame inference if the last-frame IoU is below 0.97 (parallax). Edges are refined with a guided filter. A Poly Haven pure-sky HDRI dome is sampled per pixel ray with the solved camera, so 360° turns work. `--lift` samples higher, bluer sky. Exposure is locked per shot. The plate's warmth, grain and horizon haze are matched. The plate is untouched outside the sky. |
| dusk | `lib/dusk.py` | Linear-light twilight grade: exposure down, blue shadows, desaturation, contrast, warm skyline glow. Sky recoloured to a blue-hour ramp, with the HDRI clouds kept as texture. The sky is reflected in the water matte with Schlick Fresnel. Windows, pools and lamps come from `marks.json` `dusk` and are tracked on the ground plane with bloom. It regrades the whole plate by design, so QC is `pilot_dusk_*_before-after.jpg`. |

Skies live in `assets/skies/*.hdr` (Poly Haven, CC0, 4k; gitignored). Fetch more with the Poly Haven API: `https://api.polyhaven.com/files/<id>`. Good picks:
- day: `kloofendal_48d_partly_cloudy_puresky`
- dusk: `belfast_sunset_puresky` (clouds) or `industrial_sunset_02_puresky` (clean)

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
- Lines, sky and dusk inherit the flat-ground prior. Marks on roofs and facades drift only by parallax, so they're fine for small drone moves; verify on big ones.
- Dusk only lights what's marked. Every unmarked window stays dark, so mark the hero home and its neighbours. Big white roofs stay brightish.
- Next: feather-card wing edges for hero, sun direction read from the plate, more subjects (drones, boats), a tracked sun flare.
