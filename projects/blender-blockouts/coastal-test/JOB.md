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
  - 2026-10-26: guide frames 1 / 97 / 192 re-rendered from the fixed scene (Hunter: "guides only"). Sheet: `audit/stageA-guides.jpg`. ~~The ID maps and the preview still predate stage A~~ (fixed: v4, 26 Oct). No reference exists (Hunter confirmed), so dimensions stay as built.
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
  - Rule check (scene quality rules, pasted the same day):
    - The support surface is `Lot_Lawn` at z 0.020, not paving, so the soles and the lounger base are **20 mm sunk into it**. Proposed fix: raise the lounger and rig together by +0.020 m.
    - The figure is **0% visible** from C2 at frames 1, 97 and 192, hidden by the garage door and the roof.
    - Top view: `audit/seat-after-top.png`.
  - Views: `audit/seat-before-*.png`, `audit/seat-after-side-front-3q.png`.
  - 2026-10-26: **+0.020 m raise approved and done live, still unsaved.** The lounger is now at z 0.02–0.44 and the rig at (6.9, −6.814, 0.242).
    - Re-measured on skin verts:
      - soles at z 0.020, the lawn top is 0.020: 0 mm gap;
      - thighs 1.7 mm above the seat; hands 4.8 mm above it, inside its bounds;
      - 0 skin verts inside the seat; 0 below the lawn.
    - Views: `audit/seat-after-raise.png` (side, front, top, 3/4).
    - **UNKNOWN:** a close-up view of the feet, because `look` frames the whole object. The feet contact is measured only, not seen.
 **Awaiting approval** before this goes into the spec or kit.
- 2026-10-26: **seat fix persisted (approved).**
  - Checkpoints in `build/checkpoints/`, gitignored:
    - `coastal-test-v03-pre-seat.blend`, the file on disk before the fix;
    - `coastal-test-v04-seatfix-live.blend`, the live state.
  - Spec changes:
    - Lounger extra z → [0.02, 0.44];
    - Person_Lounger `at` [6.9, −6.8145, 0.242], `rot_z` π;
    - a new `pose` block with 8 bones.
  - Kit: `people.py` now takes `pose` (bone → XYZ degrees).
  - Rebuilt headless with `--no-render`.
  - The re-measured contacts match the live fix exactly: soles at 0.020 on the lawn, thighs 1.7 mm and hands 4.8 mm above the seat, 0 verts inside the seat or below the lawn.
  - View: `audit/seat-rebuilt-from-spec.png`.
  - Guides, ID maps and the preview were not re-rendered. The figure is hidden from C2 anyway.
- 2026-10-26: **stale outputs refreshed** (Hunter: "go"). Free and local, no credits.
  - Full headless build: the guides and ID maps for frames 1, 97 and 192 are now current with stage A and the seat fix. Sheet: `audit/v4-guides-id.jpg`.
  - Grey EEVEE preview, 192 frames, 1280×720, 79 s: `preview/rise-reveal-v4.mp4`, with frames sheet `preview/rise-reveal-v4-frames.jpg`. v3 is kept for comparison.
  - The camera keys are unchanged.
  - Observation, not acted on: the ocean renders as flat white in the grey guides, though the ID map shows it correctly. This belongs to stage C.
- 2026-10-26: **Stage B proposal, not executed.** I tested candidate camera positions read-only with ray casts from the camera to the skin mesh:
  - **C2 as built (−2, 42.3, 2.7) to (−1, 35, 22):** the figure is 0% visible across the whole move.
  - **Extending C2 over the roof:** the figure stays hidden by the roof or out of frame unless the pitch reaches about −55°, which breaks the ≤15° flown-gimbal rule. Rejected.
  - **New C3 from the ocean side, looking +Y:** start (4, −32, 2.5) at pitch +2°, end (4, −22, 7) at pitch −12°.
    - The figure is 100% visible at the start, middle and end, about 11–14% of the frame height, in the lower-right third.
    - It clears the beach by 4.8 m at the start, 6.0 m in the middle and 7.3 m at the end.
    - At the end the left edge of the house clips (screen x −0.08), so x or yaw needs tuning.
  - Options: B1 keep C2 and drop the figure; B2 keep C2 and add C3; B3 extend C2 (rejected).
- 2026-10-26: **B2 approved.** C2 stays untouched. C3 start and end framing stills are rendered and **awaiting approval**; nothing is animated yet.
  - Tuned read-only: x = 1.5, constant yaw +4°. Start (1.5, −32, 2.5) at pitch +2°; end (1.5, −22, 7) at pitch −12°; 28 mm.
  - Measured:
    - house bounding corners within frame x 0.26–0.78 at the start and 0.10–0.91 at the end (about 9% margin);
    - figure 100% visible, at screen x 0.73 at the start and 0.82 at the end.
  - Rendered headless from a throwaway copy with the markers removed and a temporary camera, never saved: `audit/c3-start.png`, `audit/c3-end.png`. Script: `audit/c3_stills.py`.
  - Not in the spec or kit yet.
- 2026-10-26: **C3 framing approved and added to the spec.** C2 is untouched.
  - `C3_OceanRise`: 28 mm, 192 frames, slot 193–384 on the shared timeline.
    - keys (1.5, −32, 2.5) to (1.5, −22, 7), eased (bezier);
    - rot_keys pitch +2° to −12°, yaw 184° fixed;
    - shake 0.03, same as C2.
  - Rebuilt with `--no-render`, so no guides or ID maps were made.
  - Verified:
    - C2 moved at most 0.84 mm across 5 samples (the known shake-hash jitter); its keys are unchanged;
    - C3 hits the approved start and end exactly;
    - the camera's closest approach to any geometry is 4.38 m (dune grass), so nothing clips.
  - Grey EEVEE preview, 1280×720: `preview/c3-ocean-rise-v1.mp4` (local only, gitignored) and `preview/c3-ocean-rise-v1-frames.jpg`. Script: `audit/preview_range.py`. No AI, no credits.
- 2026-10-26: Hunter said drone moves aren't required and ground gimbal push-ins are fine; memory and wiki updated. **Proposed C4 ground gimbal, read-only tests, not executed:**
  - **Straight push up the boardwalk (x 1.0) at 1.5 m: weak.**
    - Dune grass and a post hide the figure until about y −20.
    - At the end the house overfills the frame and the figure sits at the right edge (x 0.91 at 28 mm).
  - **Angled push-in toward the figure (recommended):** 28 mm, 1.5 m above the beach.
    - Start (5.5, −20, 1.34) at yaw 186°; end (6.0, −13, 1.52) at about yaw 190°; pitch +1°.
    - The figure is 100% visible and grows from 15% to about 38% of the frame height, sitting at screen x about 0.67 → 0.75–0.82.
    - The roof clips at the end, which is expected for a push-in.
  - Camera clearance to the dune posts and grass along the path: UNKNOWN until the framing stills are rendered.
- 2026-10-26: **C4 ground push-in framing stills rendered and awaiting approval. Not in the spec.**
  - 28 mm. Start (5.5, −20, 1.34) at yaw 186°; end (6.0, −13, 1.52) at yaw 190°; pitch +1°.
  - Path clearance, sampled at 41 points:
    - closest is a dune-grass tip 0.53 m from the lens (DuneGrass_389, 17% along the path);
    - next is DuneGrass_309 at 0.64 m near the end;
    - no dune post within 2 m; no intersections.
  - Files: `audit/c4-start.png`, `audit/c4-end.png`; script `audit/c4_stills.py` (throwaway copy, never saved).
- 2026-10-26: **C4 framing approved and added to the spec.** C2 and C3 are untouched.
  - `C4_GroundPushIn`: preset gimbal_track, 28 mm, 192 frames, slot 385–576.
    - keys (5.5, −20, 1.34) to (6.0, −13, 1.52), eased, about 0.9 m/s walking pace;
    - rot_keys pitch +1°, yaw 186° → 190°;
    - shake 0.03.
  - Rebuilt with `--no-render`.
  - Verified: C2 and C3 moved at most 0.85 mm (the shake-hash jitter) with keys unchanged; C4 hits the approved start and end exactly.
  - Grey preview: `preview/c4-ground-pushin-v1.mp4` (local only) and `preview/c4-ground-pushin-v1-frames.jpg`. No AI, no credits.
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
