---
type: concept
tags: [framework, pipeline, blender, jarvis, cost-control]
status: proposed
updated: 2026-10-20
---

# 10x Job Framework v2

A proposed stage-gated flow for every 10x job, with a spec-driven Blender kit as the CG route. Full design: [2026-10-20 spec](../../docs/superpowers/specs/2026-10-20-10x-job-framework-v2-design.md). **Status: awaiting Hunter's approval; nothing built.**

**Why:** the beach Blender job ([[blender-blockout-pipeline]]) lost about 6 hours to hand-building the scene, rebuilt it after it came out "too bare", and spent 672 HF on video before people or cars were tested, so 3 of 7 shots failed. Hunter's target is under 2 hours from start to rough cut, with as little babysitting as possible.

**Shape:** Intake → Spec → **Gate A** → Build (free) → Preview → Pilot (one per shot class) → **Gate B** → Batch → QC + re-roll → **Gate C** → Deliver + Harvest. Shot classes (empty architecture, people, vehicle, drone wide, staging) pick the route from an evidence table that each pilot updates. Shared `gen-runner` handles estimates, retries, downloads, contact sheets and the **automatic JOB.md tally**. The Blender kit is `scene.json` built by one headless command into a dense scene with guide, ID and clay passes plus a density report.

**Build order:** 1) gen-runner + auto-tally, 2) gates into [[jarvis]] / the 10x-ai skill, 3) Blender kit v1 refactored from the beach scene, 4) house-from-plan (Lot 48), 5) automatic motion/morph QC.

Related: [[higgsfield-pipelines]] · [[staging-rules]] · [[claude-improvement-plan]]
