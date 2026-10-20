# 10x Blender kit (v1)

Phase 3 of [Job Framework v2](../../wiki/concepts/job-framework-v2.md). You describe a scene in one `scene.json`, and a single headless command builds the whole thing, so nobody hand-builds objects for hours.

```bash
blender -b -P projects/blender-kit/build.py -- path/to/x.scene.json              # build + density/clearance + guide & ID renders
blender -b -P projects/blender-kit/build.py -- path/to/x.scene.json --no-render  # build + checks only (~5 s)
```

Outputs go to the scene's `output` folder: `<name>.blend`, `guides/`, `id/` (material-ID maps), and `report.json` (stage timings, object counts per collection, density fails, camera clearance hits).

## Modules (`kit/`)
| Module | Builds |
|---|---|
| `house` | Parametric multi-level house from a plan-derived spec: rectangular levels, openings per side (stacker, window, bifold, door, garage door, void) built as wall segments with sills, lintels, glazing and mullions (no booleans), floors, flat or pitched roof with fascia, alfresco with posts, balconies with glass balustrades, lift core, rooftop observatory, pool. Spec format in the module docstring. |
| `site` | Lot (lawn, boundary walls, hedges, driveway, letterbox), street (road, footpath, lights), beach terrain from a height profile with dune noise, wet sand, ocean, surf lines, boardwalk, dune posts, and parametric **neighbour houses** (1–4 storeys, piers, glazing, balconies, roof, pool, lawn, hedge, drive) |
| `landscape` | Dune-grass clumps (shared mesh variants, so thousands are cheap), procedural palms, planted beds scattered from asset pools, potted plants, trees. Ground height follows the terrain. |
| `people` | Rigged MPFB2 mannequins from the library, placed or walked along a keyed path (walk cycles included) |
| `cameras` | One camera per shot in its own timeline slot with a marker. Presets: drone_reveal, top_down_rise, glide, interior_drift, walkthrough, gimbal_track, car_track. Look-at can be a point, keyed points, or a followed object. Handheld noise is per preset. |
| `passes` | Density report against targets, camera clearance check (ray-cast at a 0.35 m radius), guide renders, material-ID renders (category colours, see the leak lesson on the pipeline page) |
| `build.py` `imports` | Job-specific geometry from another .blend (for now the house and interior, until the phase-4 house generator), skipping everything the kit regenerates |

## Asset library
`assets/kit-assets.blend` (~290 MB, local only: `*.blend` is gitignored). It holds the Poly Haven grass, anthurium, calathea, fern, potted plant, island tree, dining chair, the 7 rigged mannequins, every material and the morning-sky world. Rebuild it with:

```bash
blender -b projects/blender-blockouts/beach-house-v1.blend -P projects/blender-kit/extract_assets.py -- "$PWD/projects/blender-kit/assets/kit-assets.blend"
```

New assets (for example from the free asset-library session) go in as more `A_<key>` collections.

## Test — beach rebuild (20 Oct 2026)

`projects/blender-blockouts/beach/kit/beach.scene.json` rebuilds the 16 Oct hand-built beach scene.

| | Hand-built (16 Oct) | Kit |
|---|---|---|
| Time to build the scene | ~6 h of live MCP work | **4.3 s** (65 s with 8 guide + 8 ID renders at 50%) |
| Objects | 1,768 | 1,729 (the difference is hidden template objects) |
| Object families matching exactly | — | 78 of 86 |
| Camera clearance hits | checked by hand | 0 |

Side-by-side of all 8 guide frames: `beach/kit/build/compare-guides.jpg`. Camera moves, house, neighbours, people and the car line up. Frame 1300 differs because the original guide predates the parked-car fix.

## Test — Lot 48 house from spec (20 Oct 2026)

`scenes/lot48-test.scene.json` holds the Lot 48 Fairway Bvd house drawn from the plan **summary facts** (the plans PDF isn't on this Mac, so items marked `_assumed` are guesses). Level areas match the plans: 257, 243 and 205 m², plus a 62 m² alfresco. **153 house objects, built in under 0.1 s, 1.4 s total with 2 guide + 2 ID renders.** Sheet: `projects/blender-blockouts/lot48-test/build/lot48-sheet.jpg`. To redo it against the real plans, read their dimensions into the same spec block and rebuild.

## Known gaps (v1)
- `house` v1 handles rectangular levels only (an L-shape needs a list of rectangles per level). No internal walls or rooms, stairs or furniture yet; the beach scene still imports its hand-built house and interior.
- Plan-to-spec is Claude reading the PDF into the spec. Not yet tested on a real plan set.
- Handheld shake uses F-curve noise. Camera Shakify presets aren't wired in yet.
- Vehicles are imported with their animation. There's no vehicle path or wheel-spin module yet.
- The ID category now checks the material name before the object name (fixed 20 Oct after a "Garage" wall in Render came out timber-red).
