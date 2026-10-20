---
type: concept
tags: [framework, pipeline, blender, jarvis, cost-control]
status: phase-1-built
updated: 2026-10-20
---

# 10x Job Framework v2

A proposed stage-gated flow for every 10x job, with a spec-driven Blender kit as the CG route. Full design: [2026-10-20 spec](../../docs/superpowers/specs/2026-10-20-10x-job-framework-v2-design.md). **Status: approved 20 Oct. Phase 1 built ([gen-runner](../../projects/gen-runner/README.md)); phases 2–5 to do.**

**Why:** the beach Blender job ([[blender-blockout-pipeline]]) lost about 6 hours to hand-building the scene, rebuilt it after it came out "too bare", and spent 672 HF on video before people or cars were tested, so 3 of 7 shots failed. Hunter's target is under 2 hours from start to rough cut, with as little babysitting as possible.

**Shape:** Intake → Spec → **Gate A** → Build (free) → Preview → Pilot (one per shot class) → **Gate B** → Batch → QC + re-roll → **Gate C** → Deliver + Harvest. Shot classes (empty architecture, people, vehicle, drone wide, staging) pick the route from an evidence table that each pilot updates. Shared `gen-runner` handles estimates, retries, downloads, contact sheets and the **automatic JOB.md tally**. The Blender kit is `scene.json` built by one headless command into a dense scene with guide, ID and clay passes plus a density report.

**Build order:** 1) gen-runner + auto-tally, 2) gates into [[jarvis]] / the 10x-ai skill, 3) Blender kit v1 refactored from the beach scene, 4) house-from-plan (Lot 48), 5) automatic motion/morph QC.

Related: [[higgsfield-pipelines]] · [[staging-rules]] · [[claude-improvement-plan]]

## Phase 1 — built 2026-10-20

- [gen_runner.py](../../projects/gen-runner/gen_runner.py) has five commands: `estimate` (free), `run` (gated), `log`, `tally` and `sheet`. Test results are in its [README](../../projects/gen-runner/README.md).
- **JOB.md ledger:** the new `## Ledger` section is the only source of spend. The `cost:` header is derived from it, so tallies can't drift again. Seeded on the beach job (791.5 HF) and CVA (4,035 cr). [JOB-template](../../projects/jarvis/JOB-template.md) updated.
- **Money gate widened:** the hook now also gates `higgsfield generate create` and `gen_runner.py run` via Bash. Until 20 Oct, Higgsfield CLI spend had no mechanical gate at all.
