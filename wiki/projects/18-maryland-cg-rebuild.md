---
type: project
tags: [kollosche, blender, photogrammetry, cg, lambo, carrara]
status: provisional
updated: 2026-11-11
---
# 18 Maryland CG rebuild (scan + Blender build)

**Client:** [[kollosche]] listing, 18 Maryland Avenue, Carrara (waterfront). **Goal:** a 1:1 digital twin of the house and site so a CG Lamborghini Huracán can drive down the real drive under a free-moving camera, plus interior/aerial stills and moves rendered straight from the twin. Two folders, one job:

- [projects/maryland-scan/](../../projects/maryland-scan/README.md): photogrammetry from 10x's own 2026-09-30 shoot (18 DJI 4K50 drone clips, 335 Sony S-Log clips).
- [projects/maryland-build/](../../projects/maryland-build/build.py): procedural Blender build from the Kollosche floor plan and listing photos (`raw/18-maryland/`), with furnishing, landscape, a shot rig and a review system.

**Outcome: provisional (2026-11-11).** There is no JOB.md, so nothing records a delivery, a client sign-off or a credit spend. The scan finished (`SCAN_OK`) and the build reached v2 with furnished interiors and rendered stills and moves, but no finished Huracán drive is recorded.

## What it taught us

**Floor plan beats scan for the hero geometry.** Apple Object Capture (RealityKit `PhotogrammetrySession`, free and on-device, wrapped as `maryland-scan/tools/scan.swift`) ran on video frames: drone clips at 3 fps for the roof, pool and footprint, and ground walk-ups for the entry. Its output has known limits: every mesh is closed with a hull skin you must crop, it comes out unscaled (about 1 unit across) so it has to be scaled from a known dimension, and it has to be aligned to a camera solve. The usable result was the low-poly house/entry GLBs, which served as a reference. The real build came from the plan instead: `plan_extract.py` turns the plan into wall/opening masks, and the build uses one transform for everything (site plan 2.9 px/m, floor plans 13.1 px/m, upper level registered onto ground via the side verandahs). The facades and roof were then dressed from the footage and listing photos. Reuse this order for any CG house job: plan first for dimensions, scan and photos for materials and detail.

**Listing photos are a second facade pass.** v1 (built from footage alone) got the materials wrong. v2, built from the listing photos, corrected the ground floor (white render, not weatherboard) and added the Chinese Chippendale balustrades, porthole window, frameless pool fence, rock seawall, travertine gate pillars and sign wall. Ingest the listing photos *before* modelling facades. This follows the "never invent details" rule in [Blender Approval Workflow](../../../../.claude/projects/-Users-10xhunter-Documents-Hunters-Second-Brain/memory/feedback-blender-approval-workflow.md).

**Automated scene QC, not eyeballing.** `review.py` checks the 80 placed furniture pieces against the layout and writes `review.json` (fails/warns, plus plan-view sheets). `shots.py` ray-casts every camera position on a path in six directions and refuses any shot that comes within 0.25 m of geometry or has its view line blocked within 1 m. The shot is skipped and reported instead of rendered through a wall. This puts the [Placed Asset Contract](../../../../.claude/projects/-Users-10xhunter-Documents-Hunters-Second-Brain/memory/feedback-placed-asset-contract.md) into practice. Per-shot frustum culling and a shrunk suburb module kept render times workable.

**Cheapest real camera move = plate, not CG.** The shoot contains real dusk moving shots through the gate (C5075–C5077). A tracked composite into those via [[plate-vfx]] gets a real camera move for far less than a full CG drive. Try that route first; see also [[blender-blockout-pipeline]] for the CG→AI video path and [CG Car Clips](../../../../.claude/projects/-Users-10xhunter-Documents-Hunters-Second-Brain/memory/feedback-cg-car-clips.md) for the car-move rules.

Related: [[ai-lifestyle-people]] (cites the Object Capture scan as a placement reference).
