---
type: project
tags: [sales-asset, web, demo]
status: built
updated: 2026-07-10
---

# 10x Scroll-Driven Film Demo

Self-contained scroll-scrub web page: scrolling plays a real architectural render frame-by-frame (forward and back). Sales/portfolio piece to sell scroll-driven experiences.

- **Lives at:** [projects/10x-scroll-build/](../../projects/10x-scroll-build/README.md) — open `index.html` in a browser; no build step.
- **Render:** [[cva-architects|CVA Architects]] (their asset). Fine for one-to-one sales demos; genericise or get CVA's OK before posting publicly.
- `frames/` is git-ignored (~28MB, client asset); regenerate with the ffmpeg command in the README, then match `FRAME_COUNT` in `index.html`.
