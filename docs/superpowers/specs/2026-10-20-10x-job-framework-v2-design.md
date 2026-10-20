# 10x Job Framework v2 + Blender Kit — Design

**Date:** 2026-10-20 · **Status:** proposed, awaiting Hunter's approval · **Nothing built yet**

## Why

The beach Blender job (12–16 Oct) showed where the time and money go:

| What happened | Cost | Root cause |
|---|---|---|
| About 6 h of Claude building the scene object by object (16 Oct 09:34 → 15:50) | Hunter's day | Every object was a one-off `bpy` call. Only 4 tiny scripts were saved, so the next house starts from zero. |
| v1 (274 objects) judged "too bare" and rebuilt to 1,600 | Several hours | No density or reference spec agreed before building |
| All 7 Seedance clips generated before people or cars were tested; 3 failed (morphing faces, a car that doesn't roll, a shot that barely moves) | 672 HF, then a re-roll | No pilot step and no route-by-shot-content table |
| Model shootouts repeated (5 models, then 2 models × 7 shots) | ~49 HF + time | Evidence never turned into locked defaults |
| Upload errors and retries handled ad hoc in each job's `run.py` | Time | No shared runner |
| JOB.md cost tallies drift from their logs (CVA, ZED-4) | Trust | Tallies are kept by hand |

Hunter's answers (20 Oct): the worst pains were **waiting on the build** and **bad outputs**. Blender is for **off-the-plan client jobs** and **10x R&D**. Target: **under 2 hours from start to rough cut**. Scope: **every 10x job**, with Blender as one route among several.

## Part A — The framework (every job type)

One stage-gated flow for every job: staging, renders, stills, films and Blender. Hunter approves at **three gates only**. Everything between the gates runs without him.

```
0 Intake ─► 1 Spec ─► [GATE A] ─► 2 Prep/Build ─► 3 Preview ─► 4 Pilot ─► [GATE B] ─► 5 Batch ─► 6 QC + re-roll ─► [GATE C] ─► 7 Deliver + Harvest
```

| Stage | What happens | Output |
|---|---|---|
| 0 Intake | Client, address, deliverables, client profile, **credit cap**, deadline | `JOB.md` from the template |
| 1 Spec | Shot list. For each shot: **shot class**, route, reference images, and for Blender the density and reference targets | `spec.json` plus a one-page summary |
| **Gate A** | Hunter approves the spec in one message: scope, look, density and cap. This is where "too bare" gets caught, before any build. | |
| 2 Prep/Build | Free work: folders, triage, masks, Blender build from the kit (Part B) | Source files, `.blend` |
| 3 Preview | Free: guide-frame contact sheet, ID maps, clearance check | `preview.jpg` (Hunter can look, no gate) |
| 4 Pilot | **One generation per shot class**, the riskiest shot of each class first. Cost quote, then run. | Pilot clips/stills plus QC |
| **Gate B** | Hunter approves the pilots and the **total batch quote** in one message | |
| 5 Batch | `gen-runner` runs the rest on the routes that passed their pilot | Outputs |
| 6 QC + re-roll | Automatic checks plus a contact sheet. Re-roll ladder: at most 2 tries on the same route, then escalate to the next model in the route table. Never re-roll silently past the cap. | `qc.jpg`, flags |
| **Gate C** | Hunter approves the finals | |
| 7 Deliver + Harvest | Files to delivered; JOB.md closes itself (tally is automatic); wiki harvest | Wiki paragraph |

**Shot classes** decide the route, so nobody has to re-decide models on every job:

| Shot class | Still | Video | Evidence |
|---|---|---|---|
| Empty-architecture move (glide, top-down, walkthrough, interior drift) | Sunburst (2.75) | Seedance 2.5 8s 1080p (96) | Beach 03/04/05 passed |
| People in frame (walking, faces) | Sunburst | **Veo 3.1 Fast high 8s (32)**, Hunter's pick 20 Oct | Face test 06 |
| Vehicle motion | Sunburst | **Untested.** Pilot Veo 3.1 Fast vs Kling 3.0 Pro | Seedance 07 failed |
| Big landscape / drone wide | Sunburst | Seedance; **pilot first** | 01 barely moved |
| Staging / edits on real photos | existing [[staging-rules]] routes | — | unchanged |

The table lives in the wiki and is updated from every pilot, so each job makes the defaults sharper instead of re-running shootouts.

### Shared tooling (benefits every job)
- **`gen-runner`**: reads `jobs.json` (one row per generation: shot, model, params, inputs).
  - `estimate` → runs `higgsfield generate cost` / `simulate_cost` per row and prints a total.
  - `run` → only after the go-ahead. Up to 8 in parallel, retries on upload/520/timeout errors, downloads outputs, makes a contact sheet, and **appends each spend to JOB.md and recomputes the header tally**. That fixes the drift for good.
  - Works with the Magnific money gate; it never gets around it.
- **QC helpers:** frame grabs at 0/25/50/75/100%, side-by-sides against the guide, and two cheap automatic flags:
  - **morph/dissolve**: a sudden drop in frame-to-frame similarity, which would have caught 06
  - **no motion**: very low optical flow on the subject, which would have caught 01 and 07
- **`10x-ai` skill update:** add the gates, shot classes, pilot step and a **Blender/CG route** (it has none today).

## Part B — Blender kit (the under-2-hours part)

Replace hand-building with a **spec-driven kit**: Claude writes or edits a `scene.json`, and one headless command builds the whole scene in minutes. Iterating means editing JSON and rebuilding, not hours of live MCP calls. Live MCP is kept for looking and tweaking only.

```
scene.json ──► blender -b -P kit/build.py ──► scene.blend + guide frames + ID maps + clay + clearance report + contact sheet
```

Kit modules, all Python run headless and kept in `projects/blender-kit/`:

1. **`house`**: parametric house from a spec. Footprint polygons per storey, wall heights, slab thickness, roof type (flat, skillion, hip, gable), and an opening schedule (windows and doors with sizes and sill heights). Balconies, pergolas, glass balustrades. **Off-the-plan:** Claude reads the plan PDF or floorplan into this spec, and Hunter checks the summary at Gate A. Test case: the Lot 48 Belle job.
2. **`site`**: lot boundary, pool, decks, driveway, fences, retaining walls, street, footpath, street lights, and **neighbour presets** (low-detail houses in house-render white).
3. **`landscape`**: vegetation scatter by zone (lawn, garden bed, dune grass, palms, hedge) from a curated asset set. The SFX/Blender asset-library session is collecting free CC0 models that feed this.
4. **`furnish`**: room presets by type (living, dining, kitchen, master, secondary, bath) placed against named walls, following the existing [[staging-rules]] hierarchy (two bedsides, rug sizing and so on).
5. **`people` / `vehicles`**: MPFB2 walker presets (gender, age, outfit colour, walk path) and car proxies with wheel rotation tied to distance.
6. **`cameras`**: the shot-class presets as functions, each taking a target and a duration: drone reveal, top-down rise, glide, walkthrough, gimbal track (TRACK_TO an empty plus a parallel path), car track. Camera Shakify is applied with the proven presets.
7. **`passes`**: guide frame, material-ID map (existing script), clay, depth, plus an automatic **clearance check** and **density report**. The report shows object count per zone against the agreed targets, so "too bare" is caught by a number, not by eye.

**Density by default:** every preset already lands in the 1,500+ object range the beach rebuild reached. A bare scene would have to be asked for explicitly.

**Time budget (target):** spec 20 min, then Gate A, build 10 min, preview 10 min, pilot run 20 min, then Gate B, batch about 30 min. That puts a rough cut at about 1.5–2 h of wall-clock, with Hunter needed for two short approvals.

## Build order (each phase shippable on its own)

| Phase | What | Pays off for |
|---|---|---|
| 1 | `gen-runner` + JOB.md auto-tally + QC contact sheets | Every job, immediately |
| 2 | Framework into `10x-ai` (gates, shot classes, route table, pilot rule) + wiki route table | Every job |
| 3 | Blender kit v1: refactor the beach scene into `site`, `landscape`, `people`, `cameras` and `passes` modules plus `scene.json`; rebuild beach from JSON as the test | Speed |
| 4 | `house` generator + plan-to-spec; test on Lot 48 | Off-the-plan client work |
| 5 | Automatic motion/morph QC flags | Bad outputs |

Phases 1–3 are free to build (no credits). The only spend is pilots, and only with a go.

## Not doing (YAGNI)
- No paid add-ons (Botaniq, Photographer) until the kit shows a gap.
- No full photoreal Blender rendering: the AI still paints the surfaces.
- No new orchestration service or dashboard. Scripts, the skill and the wiki are enough.

## Open questions for Hunter
1. Credit cap per Blender job by default? (Beach spent 791.5 HF.)
2. Gate B: approve the pilots one class at a time, or all pilots plus the batch quote in a single message?
3. Lot 48 as the phase-4 test case — is it still live?
