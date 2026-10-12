---
type: concept
tags: [ai-generation, workflow, higgsfield, magnific]
updated: 2026-10-12
---

# Higgsfield Pipelines (AI generation routing)

How 10x routes real-estate AI image/video work. Full KB with T1–T10 prompt templates, model commands, and client escalation guide lives in auto-memory `ai-realestate-workflow.md`; this page is the vault-side summary.

## Glossary
| Term | Meaning |
|------|---------|
| **Higgsfield** | AI image/video gen platform, run via `higgsfield` CLI |
| **Seedream** | Higgsfield image model (`seedream_v4_5`) — composition-locked render enhance, 1cr |
| **Nano Banana Pro** | Higgsfield image model (`nano_banana_2`) — creative staging, 4cr; the **default for full-frame staging** |
| **Topaz** | Upscale model (`topaz_image`) — optional, ask before using |
| **Magnific** | Second platform via MCP — every MCP generation costs credits; always `simulate_cost` + ask first |
| **job_set_type** | Higgsfield's model ID string passed to `generate create` |

## The two pipelines — route before generating
1. **Full-frame generative** (Higgsfield generate / Magnific reimagine / Seedream) — interiors, staging, renders, tight exteriors.
2. **Masked inpaint** (Freepik Magnific Retouch / Higgsfield `/image-editing`) — any targeted edit on a detail-heavy exterior: sky, declutter, object removal.
3. **Aspect reframe / outpaint** (e.g. landscape render → 9:16): pad the original onto a grey canvas at the target ratio yourself → Nano Banana Pro 4k fills only the bands → paste the original back 1:1. Never feed the raw landscape ref with a new ratio (NBP reframes ~half the time), and never use Magnific expand in Ideogram mode with a long prompt (it draws the text). Real photos: anchor to an edge so only sky gets added. See [[woomala-st-9x16-reframe]].

❌ **Never run full-frame on a drone wide** — it regenerates the ground and wrecks fine detail.
❌ **Never full-frame-generate real photos** — faithful only on renders; real photos get Topaz upscale (auto-memory `feedback-generate-vs-real-photos`).

## Hard rules
- **Money gate:** any credit-spending op needs Hunter's explicit go-ahead. Git is free; credits never are.
- **Editorial by default (2026-10-12):** every generation (stills, staging, renders, video) aims for a clean, magazine-grade editorial finish. Get it from composition and finish, and keep the light bright and airy, because "editorial" wording alone drifts moody (see [[staging-rules]]). Blender → video route: [[blender-blockout-pipeline]].
- Staging rules → [[staging-rules]].
- Skills: vendored in `.agents/skills/` (read the relevant `SKILL.md` first); discover models with unfiltered `higgsfield model list`.

## Used by
[[coast-life-constructions]] · [[bespoke-estate-agents]] · [[belle-property]] · [[cva-architects]]

## Craft
Tool-selection and prompting craft: [[ai-toolkit]] · [[ai-image-tools]] · [[ai-video-tools]] · [[ai-prompting]].
