---
type: concept
tags: [routing, pipeline, video, stills, framework]
status: active
updated: 2026-10-20
---

# Shot-Class Routes

**The canonical route table for [[job-framework-v2]].** Every shot in a job gets a **shot class** at the Spec stage, and the class picks the route, so models aren't re-chosen or re-shot-out on every job. The `10x-ai` skill reads this page before routing. Each pilot's result is written back here, so the defaults get sharper with every job.

Costs are as quoted by `higgsfield generate cost` / `simulate_cost` on the date shown. Re-estimate on every job, because prices move.

## Real photos (listing shoots)

The full rules are in [[higgsfield-pipelines]] and [[staging-rules]]; this is the routing summary.

| Class | Route | Notes |
|---|---|---|
| **P1 Interior staging** (empty or furnished room) | Full-frame generative → `staging-engine` | Model per [[staging-rules]] (default-model question still open, see [[claude-improvement-plan]] P4) |
| **P2 Targeted edit on a detail-heavy exterior** (sky, declutter, removal) | Masked inpaint (Magnific Retouch / HF image-editing) | ❌ never full-frame a drone wide |
| **P3 Reframe / outpaint** | Pad the original, NBP 4k fills the bands, paste the original back 1:1 | |
| **P4 Real photo needs more resolution** | Topaz upscale (opt-in, ask first) | ❌ never full-frame-generate a real photo |

## Renders and CG (developer renders, Blender block-outs)

| Class | Still | Video | Evidence | Status |
|---|---|---|---|---|
| **C1 Render enhance** (make a 3D render read as a photo) | Nano Banana Pro on the **original** render (~75cr/image on Magnific) | — | CVA Woomala, 11/11 delivered | proven |
| **C2 Empty-architecture move** (glide, top-down rise, walkthrough, interior drift) | GPT Image 2.5 Sunburst, high 2K (2.75 HF) from the Blender guide + ID map | Seedance 2.5, omni start frame, 8s 1080p (**96 HF**) | Beach 03/04/05 passed | proven |
| **C3 People in frame** (walking couple, faces) | Sunburst | **Veo 3.1 Fast**, high, 8s, start frame (**32 HF**) | Beach face test 06: no dissolve, faces held. Background drifts late. Hunter's pick 20 Oct; Kling 3.0 Pro (12.5) is the fallback | picked, not yet shipped |
| **C4 Vehicle motion** (car arriving or tracking) | Sunburst | **Untested.** Pilot Veo 3.1 Fast against Kling 3.0 Pro | Seedance 07 failed: car didn't roll | **pilot required** |
| **C5 Big landscape / drone wide move** (surf reveal, aerial) | Sunburst | Veo 3.1 Fast or Seedance; **pilot first** | Seedance 01 barely moved | **pilot required** |

## Pilot rule

Before any batch, run **one generation per shot class present in the job**, picking the riskiest shot of that class (people, vehicles and big camera moves first). Use `gen_runner.py run jobs.json --only <pilot ids>`. Batch only the classes whose pilot passed QC. A class marked "pilot required" above can never be batched blind.

**Why:** on 16 Oct the beach job batched all 7 Seedance clips (672 HF) before a single people or vehicle shot had been tested, and 3 failed.

## Automatic QC flags

gen-runner flags every downloaded video: **NO_MOTION** (barely moves) and **MORPH/DISSOLVE@t** (cross-fade or morph). Calibrated 9/9 on the beach clips. A flagged pilot counts as failed for its class unless Hunter overrides it after looking. Faces and identity still need a human look. Detail is in the [gen-runner README](../../projects/gen-runner/README.md).

## Re-roll ladder (video and CG)

1. Up to **2 re-rolls on the same route**, each changing one thing (prompt, then start frame).
2. Still failing: escalate to the next model in this table for that class.
3. Never re-roll past the job's credit cap without going back to Hunter.
4. Write the outcome back to this page (evidence column).

## Changelog
- 2026-10-20: automatic QC flags added (phase 5).
- 2026-10-20: page created from the beach job and CVA evidence (phase 2 of [[job-framework-v2]]).
