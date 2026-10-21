---
type: concept
tags: [blender, vfx, camera-tracking, drone, birds, pipeline]
status: active
updated: 2026-10-21
---

# plate-vfx — CG into real footage

Built 2026-10-21 from the [[extra-salt-kollosche-birds]] job. Hunter's brief was "improve this skill and workflow like crazy". It is a local, $0 pipeline that composites CG birds into real footage and guarantees the plate's pixels and grade stay untouched.

- Code: [projects/plate-vfx/](../../projects/plate-vfx/README.md)
- Skill: `plate-vfx` (`~/.claude/skills/plate-vfx/SKILL.md`)
- Benchmark: the Kollosche drone wide (`projects/plate-vfx/bench/kollosche`)

## Pipeline
`prep` runs init (frames and cut detection), track (constrained drone-camera fit, gated at 0.5 px), match (sky, warmth, grain), layout (auto-routed flight paths inside the delivery's safe area) and a draft pilot, then stops for Hunter's approval. `render` builds the scene at the chosen tier, composites with plate-matched grain, verifies 0 px change outside the CG, and exports mp4, ProRes and an alpha layer.

## Tiers: more polys = better but slower (Hunter, 2026-10-21)
| Tier | Gull | Engine | Kollosche time |
|---|---|---|---|
| draft | procedural, ~500 polys | EEVEE, half resolution | ~10 s |
| standard (default) | rigged herring gull, 4.8k faces, feather texture | EEVEE + motion blur | 28 s |
| hero | herring gull + subsurf, ~19k faces | Cycles 128 + denoise | 6 min (near-identical to standard at drone-wide bird sizes) |

## What v1 improved over the first job
- **Real gull.** A CC-BY Sketchfab herring gull (credit Pofdpoi), with the feet removed, re-oriented and hand-rigged (shoulder and wrist bones). It is driven by the same flight simulation as the procedural gull, and the realism jump comes at the same poly count as procedural "standard".
- **Track.** The fit is multi-start over pitch and lens, and adds a `free` 6-DOF model for orbits. On Kollosche it went from 0.36 px to 0.15 px.
- **Auto layout.** Birds are routed for 16:9, 9:16, 4:5 or 1:1. Scoring covers time inside the safe area, edge entry, readable size and spacing. A preview image shows the paths before any render.
- **Plate match.** Sky hue drives the fill light and warmth drives the sun colour. Grain is measured in flat blocks and added only inside the CG alpha.
- **Cut detection** runs at init, which fixes the frame-46 trap.

## Flock (added 2026-10-21)
`layout --flock N` routes a leader, then N members ride drifting slots in a loose elongated flock: own lag along the path, separation ≥1.6 m, banking/pitch from their own velocity, individual wingbeats, mostly-shared glides. Benchmark: 2 hero gulls + 24-bird flock over the Kollosche river mouth, standard tier 33 s, plate untouched.

## Next
Feather cards on the hero wing edges, sun direction read from plate shadows, keyframe-chained tracking for long shots, and new subjects (drones, boats, people).

Related: [[blender-blockout-pipeline]], [[higgsfield-pipelines]] (the drone-wide no-AI rule).

## Beyond birds (2026-10-21)
The same camera solve now drives three more stages: `lines` (tracked lot outlines and pins in 10x blue), `sky` (tracked HDRI sky replacement) and `dusk` (day-to-dusk video). The plan and status are in [[plate-vfx-roadmap]], and internals are in the README. All three run locally at $0. The sky and water mattes come from SegFormer-B5 in `~/.venvs/demucs`.
