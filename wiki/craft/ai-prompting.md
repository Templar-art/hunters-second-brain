---
type: reference
tags: [ai-generation, prompting, staging, reference]
updated: 2026-07-19
---

# AI Prompting (real-estate generation)

Prompting patterns for real-estate AI generation, distilled from [[staging-rules]]. The full prompt template library (T1–T10) lives in auto-memory `ai-realestate-workflow.md` — this is the pattern summary.

## Core patterns
- **Phrase positively** — describe the target state, not the absence. "Open, empty ends + exact count" beats "no extra chairs". Negation alone fails on Nano Banana.
- **Preserve fixtures** — name what to keep: taps, windows, vanities, cabinetry. Only movable furniture/décor changes.
- **One-shot staging** — pick self-enforcing geometry so it lands in a single pass. Round table when end-chairs are the risk; the shape removes the failure mode.
- **Vary elements across a set** — plants, bedding, cushions must differ room-to-room in one listing. Never identical. Specify the rotation.
- **Isolate tricky objects** — give a fridge (or any high-risk object) its own pass, name the door, and freeze constraints like island size so the model can't drift them.
- **Composition-lock language (render enhance)** — for Seedream, instruct "keep composition/geometry/layout; enhance realism and detail only". Change quality, not structure.
- **Reference-transfer** — supply a reference image and instruct style/furniture transfer while preserving the target room's fixed elements (SOP in auto-memory).
- **Iteration discipline** — every pass costs credits. Plan the prompt to land first time; re-run only with the money gate cleared → [[higgsfield-pipelines]].

## Prompt structure
Build a prompt in this order:
1. **Subject** — the room/scene and its type.
2. **What to keep** — named fixtures and fixed geometry.
3. **What to change** — the staging/edit intent.
4. **Style / quality** — mood, materials, realism level.
5. **Explicit counts** — exact numbers (chairs, cushions, plants) and positive phrasing.

## Related
[[staging-rules]] · [[ai-image-tools]] · [[higgsfield-pipelines]]
