---
type: concept
tags: [framework, pipeline, blender, jarvis, cost-control]
status: phase-4-built
updated: 2026-10-20
---

# 10x Job Framework v2

A proposed stage-gated flow for every 10x job, with a spec-driven Blender kit as the CG route. Full design: [2026-10-20 spec](../../docs/superpowers/specs/2026-10-20-10x-job-framework-v2-design.md). **Status: approved 20 Oct. Phases 1–4 built: [gen-runner](../../projects/gen-runner/README.md), the gates and routes in the `10x-ai` skill plus [[shot-class-routes]], the [Blender kit](../../projects/blender-kit/README.md) and its house generator. Phase 5 (automatic motion/morph QC) to do.**

**Why:** the beach Blender job ([[blender-blockout-pipeline]]) lost about 6 hours to hand-building the scene, rebuilt it after it came out "too bare", and spent 672 HF on video before people or cars were tested, so 3 of 7 shots failed. Hunter's target is under 2 hours from start to rough cut, with as little babysitting as possible.

**Shape:** Intake → Spec → **Gate A** → Build (free) → Preview → Pilot (one per shot class) → **Gate B** → Batch → QC + re-roll → **Gate C** → Deliver + Harvest. Shot classes (empty architecture, people, vehicle, drone wide, staging) pick the route from an evidence table that each pilot updates. Shared `gen-runner` handles estimates, retries, downloads, contact sheets and the **automatic JOB.md tally**. The Blender kit is `scene.json` built by one headless command into a dense scene with guide, ID and clay passes plus a density report.

**Build order:** 1) gen-runner + auto-tally, 2) gates into [[jarvis]] / the 10x-ai skill, 3) Blender kit v1 refactored from the beach scene, 4) house-from-plan (Lot 48), 5) automatic motion/morph QC.

Related: [[higgsfield-pipelines]] · [[staging-rules]] · [[claude-improvement-plan]]

## Phase 1 — built 2026-10-20

- [gen_runner.py](../../projects/gen-runner/gen_runner.py) has five commands: `estimate` (free), `run` (gated), `log`, `tally` and `sheet`. Test results are in its [README](../../projects/gen-runner/README.md).
- **JOB.md ledger:** the new `## Ledger` section is the only source of spend. The `cost:` header is derived from it, so tallies can't drift again. Seeded on the beach job (791.5 HF) and CVA (4,035 cr). [JOB-template](../../projects/jarvis/JOB-template.md) updated.
- **Money gate widened:** the hook now also gates `higgsfield generate create` and `gen_runner.py run` via Bash. Until 20 Oct, Higgsfield CLI spend had no mechanical gate at all.

## Phase 2 — built 2026-10-20

- **`10x-ai` skill rewritten around the three gates.** Gate A covers the spec, credit cap and pilot spend. Gate B covers the pilot results and the batch quote. Gate C covers the finals.
  - It assigns a shot class per shot, has a Blender route, follows the pilot-before-batch rule, uses gen-runner for batches, writes pilot outcomes back to the route table and harvests at the end.
  - The skill lives outside git; a pre-edit backup is in `~/.claude/backups/10x-ai-2026-10-20/`.
- **[[shot-class-routes]]** is the canonical route table. Real-photo classes P1–P4, render/CG classes C1–C5. C4 (vehicles) and C5 (drone wides) are marked **pilot required**.

## Phase 3 — built 2026-10-20

[Blender kit v1](../../projects/blender-kit/README.md): `scene.json` built into a `.blend`, guide frames, ID maps and a report by one headless command. The beach rebuild took **4.3 s** (about 65 s with renders) against roughly 6 h of hand-building, with output matching the original. Next is phase 4, the house generator plus plan-to-spec (Lot 48), which removes the last import.

## Phase 4 — built 2026-10-20

`kit/house.py` builds a multi-level house from a plan-derived spec: openings per side, built as wall segments with no booleans, plus floors, roof, alfresco, balconies, lift core, observatory and pool.
- **Lot 48 test:** used the summary facts, because the plans PDF was gone from the Mac (the job folder was archived after delivery in July). Level areas match the plans (257/243/205 m² + 62 m² alfresco). 153 objects in under 0.1 s, 1.4 s with renders ([sheet](../../projects/blender-blockouts/lot48-test/build/lot48-sheet.jpg)).
- **Still open:** a real plan-to-spec run on an actual PDF, L-shaped levels, internal walls and stairs.
