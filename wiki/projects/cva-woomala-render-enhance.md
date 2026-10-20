---
type: project
tags: [cva, render-enhance, magnific, nano-banana-pro]
status: delivered-internal
updated: 2026-10-19
---

# CVA Woomala St — Render Enhance (Oct 2026)

[[cva-architects]] gave 10x eleven developer renders of 12–16 Woomala St (tower, entry, rooftop pool, amenities, apartment interiors). The brief was to make them read as real photography so they don't look like the architect/builder originals: realistic real estate sky, warm moody sun with shadows, stills only. **Layout and camera angle cannot change.**

- **Shipped:** 11 stills at 2528×1696 (bedroom 5056×3392 upscaled) in [projects/cva-woomala-enhance/delivery/](../../projects/cva-woomala-enhance/delivery/). Job log: [JOB.md](../../projects/cva-woomala-enhance/JOB.md).
- **Cost:** 4,035 Magnific credits (**⚠️ supersedes 3,210**: the 825cr moody pass on 19 Oct was never added here; ledger seeded 20 Oct). About half of that went on dead ends; the working recipe costs about 75cr/image.

## The recipe that worked
**Nano Banana Pro, 2k, 3:2**, original render as Image 1, prose prompt: "turn into a real photograph… 24mm tilt-shift… keep exact framing, crop and layout; nothing moves, added or removed", then name every fixed element and furniture count, plus a natural clear blue sky paler at the horizon and warm late-afternoon sun from the side the room's light already comes from. Same method as the Salisbury stills ([[10x-scroll-build]]).

## What didn't
- **GPT 2.5 Sunburst (medium):** posterised the result; Hunter said it "looks like a cartoon".
- **Ideogram 4.5 Precise Edit:** keeps the layout, but skies come out saturated/CGI and too blue.
- **Local colour remaps / LAB grades of the sky:** Hunter spots them straight away. Never fake the sky locally.
- **Outpainting the letterboxed tower** invented a neighbouring office block.
- Hunter's sky taste: natural real estate blue with a gradient and wispy cloud. Not deep saturated, not flat pale.

## Process lessons
- **Shell bug:** zsh arrays are 1-indexed, so a bash-style upload loop sent every file to the wrong slot. NBP then "drifted" because it was given the wrong photo. Verify upload→source mapping (dimensions/names) before generating; use Python for batch loops.
- Magnific upscale bills by source size: a ~2.5k source cost 270cr, not 90.

## Related
[[cva-architects]] · [[woomala-st-9x16-reframe]] · [[higgsfield-pipelines]] · [[staging-rules]]
