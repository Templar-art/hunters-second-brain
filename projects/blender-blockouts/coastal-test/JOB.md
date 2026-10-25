---
client: internal-rnd
address: Coastal house (invented Gold Coast beach house, test build)
opened: 2026-10-26
status: review        # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 8.25, aud: 0 }   # derived from ## Ledger
---

# Job — Coastal house drone reveal (guide frame for AI)

First build after the Blender MCP add-on update and asset-library switch-on. An invented two-storey beach house built entirely by the kit (`house` generator, beach `site`/`landscape`), no imported geometry. Spec: [coastal.scene.json](coastal.scene.json). 1,405 objects, built in about 4 s (9 s with renders).

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 1 | C1 street drone reveal (8 s, 192 f, 24 mm) | guide + ID → Sunburst stills → video | stills PASS 3/3 | Starts low on the street, rises over the roof and ends on the pool, dunes and ocean. Guides + ID at frames 1 / 97 / 192 in `build/` (local) |

## Log

- 2026-10-26 build: v1 → v3. Added front-fence and entry planting plus verge trees; trimmed the trees that blocked the facade; pushed the end frame higher and toward the sea so the pool clears the balcony.
- 2026-10-26 kit fixes found on this build: (1) `copy_obj` copied the template's hidden flag, so every kit tree came out invisible (beach rebuild included); (2) ID rule order sent "footpath" to timber red; (3) `island_tree` trunks matched the kitchen-island rule and came out stone orange. All fixed in `blender-kit/kit/`.
- 2026-10-26 generate: 3 × GPT Image 2.5 Sunburst (high, 2K, 16:9), guide + ID map as Image 1 / Image 2, quoted 8.25 HF and spent 8.25 HF. QC: **all 3 PASS first time.** Layout, framing, house, pool, boardwalk and people positions all held; the palms and trees came out real (the "placeholder" wording worked). Small drift: the sandy side verge became a gravel path and the front pad became concrete, both acceptable. The house reads the same across all 3 (timber garage door, 3 dark-framed upper windows), so the stills work as start and end frames. Comparison: `stills/guide-vs-still.jpg`.
- 2026-10-26 feedback (Hunter): "needs to look more believable like an actual house", and the drone move was "straight dog shit". The v1 stills are superseded.
- 2026-10-26 rebuild v3 (free):
  - **House:** the upper floor cantilevers 1.5 m over the garage and entry; timber batten screen on the street window; stone entry blade wall with a concrete portico; stone planter; stepping-stone path; rendered fence with timber slats, letterbox and gate piers; driveway runs to the garage; 1.2 m eaves; downpipes, AC unit, 12 solar panels.
  - **Camera:** rebuilt as a flown rise-and-push. 28 mm lens, street at 2.7 m to 22 m over the front yard, gimbal +3° → −12°, eased, no look-at swing.
  - Grey preview: `preview/rise-reveal-v3.mp4`.
- 2026-10-26 audit (read-only, approval workflow). Found 5 defects; all dimensions are invented (no reference supplied). Views are in `audit/`.
- 2026-10-26 **stage A approved (A1–A5 only) and done:**
  - A1: alfresco glass balustrade moved off the stacker doors to the pool-side edge (y −4); posts 0 → 3.3 m at the outer corners under the balcony edge.
  - A2: pool bed moved outside the pool coping. Leaves of one plant rest on the coping, none in the water.
  - A3: entry bed limited to the solid wall between the blade and the garage. Nothing touches the blade, door, garage or pavers.
  - A4: 0.7 × 2.0 × 0.42 m lounger block under the reclining figure (Hunter's choice over removing it).
  - A5: driveway stops at the lot boundary (y 39), no longer overlapping the footpath.
  - Diff: only these objects changed. The camera move is unchanged (1 mm shake jitter only).
  - 2026-10-26: guide frames 1 / 97 / 192 re-rendered from the fixed scene (Hunter: "guides only"). Sheet: `audit/stageA-guides.jpg`. **The ID maps and `preview/rise-reveal-v3.mp4` still predate stage A.** No reference exists (Hunter confirmed), so dimensions stay as built.
- 2026-10-26 seat audit (Hunter's brief):
  - **Before:** the lounger (`Coastal_Lounger`, a 0.7 × 2.0 × 0.42 m block) has no front. The figure (`Body_Person_Lounger`, MPFB rig with 163 bones) was facing +Y toward the house in an upright chair-sit. Its soles were on the seat top (z 0.423), its thighs floated at z 0.87, about 0.45 m above the seat, and its hands hung in the air.
  - **Live fix, unsaved:**
    - rig rotated 180° to face −Y, toward the ocean;
    - rig moved to (6.9, −6.814, 0.222);
    - lowerleg01 65°, foot 21°;
    - upperarm01 (−15°, 0, ∓45°), lowerarm01 −95°.
  - **Measured on skin verts:**
    - soles at z 0.000;
    - thigh gap 1.7 mm;
    - hands 4.8 mm above the seat, within the seat bounds;
    - 0 verts inside the seat.
  - Views: `audit/seat-before-*.png`, `audit/seat-after-side-front-3q.png`. **Awaiting approval** before this goes into the spec or kit.
- Open (not approved): B camera, C lighting/materials, D AI. Questions for Hunter: cantilever support, downpipe position, roof fall, neighbour heights. Waiting on a reference.
- Kit bug noted, not fixed: shake-noise phase uses Python's salted `hash()`, so it varies slightly between builds.
- Superseded: Hunter reviews the v3 motion. Then new Sunburst stills (3 × 2.75 = 8.25 HF, quote again) with house-character wording, then video.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
- 2026-10-26 | 2.75 hf | c1_f001 gpt_image_2_5 (gen-runner)
- 2026-10-26 | 2.75 hf | c1_f097 gpt_image_2_5 (gen-runner)
- 2026-10-26 | 2.75 hf | c1_f192 gpt_image_2_5 (gen-runner)

---
_Vault: [[jarvis]]_
