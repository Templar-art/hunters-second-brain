---
type: reference
tags: [ai-generation, image-tools, staging, reference]
updated: 2026-07-19
---

# AI Image Tools (which tool for which job)

The roles of each image tool in 10x's stack. Routing and money gate → [[higgsfield-pipelines]]; staging rules → [[staging-rules]].

## The stack
| Tool | Role | Notes |
|------|------|-------|
| **Higgsfield — Seedream** (`seedream_v4_5`) | Composition-locked render **enhancement** | ~1cr. Keeps geometry; lifts realism/detail. |
| **Higgsfield — Nano Banana Pro** (`nano_banana_2`) | Creative **full-frame staging** | ~4cr. Default for full-frame staging. |
| **Magnific** (via MCP) | Upscale / reimagine | Credit-metered — `simulate_cost` + ask first, every time. |
| **Freepik / Magnific Retouch** | Masked **inpaint** — sky, declutter, object removal | Targeted edits on detail-heavy exteriors. |
| **Topaz** (`topaz_image`) | Upscale **real photos** | The safe path for real photography; ask before running. |

## Task → tool
| Task | Tool |
|------|------|
| Virtual staging (full-frame) | Nano Banana Pro |
| Render enhance (keep composition) | Seedream |
| Targeted exterior edit (sky/declutter/removal) | Masked inpaint (Freepik / Magnific Retouch) |
| Upscale a real photo | Topaz |
| Upscale / reimagine | Magnific (simulate cost first) |

## The landscape (tool-agnostic)
Categories persist even as specific tools change:
- **Diffusion image models** — generate/transform from a prompt (+ optional reference). Full-frame generative rebuilds the whole frame.
- **Inpaint vs full-frame generative** — inpaint edits only a masked region and leaves the rest untouched (precision, fidelity); full-frame regenerates everything (creative reach, but risks fine detail).
- **Upscalers** — raise resolution/detail. Some are faithful (Topaz), some reimagine (Magnific) and can invent detail — pick per fidelity need.

When a tool changes, map it back to its category and the routing rules still hold.

## Non-negotiables
- **Never full-frame real photos** — renders only. Real photos get Topaz upscale.
- **Never full-frame a drone wide** — regenerates ground detail. Use masked inpaint if an edit is needed.

## Related
[[higgsfield-pipelines]] · [[staging-rules]] · [[ai-prompting]] · [[ai-video-tools]]
