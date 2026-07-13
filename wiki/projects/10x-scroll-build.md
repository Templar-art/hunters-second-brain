---
type: project
tags: [sales-asset, web, demo]
status: built
updated: 2026-07-14
---

# 10x Scroll-Driven Film Demo

Self-contained scroll-scrub web page: scrolling plays a real architectural render frame-by-frame (forward and back). Sales/portfolio piece to sell scroll-driven experiences.

- **Lives at:** [projects/10x-scroll-build/](../../projects/10x-scroll-build/README.md) — open `index.html` in a browser; no build step.
- **Render:** [[cva-architects|CVA Architects]] (their asset). Fine for one-to-one sales demos; genericise or get CVA's OK before posting publicly.
- `frames/` is git-ignored (~28MB, client asset); regenerate with the ffmpeg command in the README, then match `FRAME_COUNT` in `index.html`.

## Salisbury variant (14 Jul 2026)
Second build of the technique, client-branded: [projects/10x-scroll-salisbury/](../../projects/10x-scroll-salisbury/README.md) — Salisbury voice (near-black, Anton condensed caps, amber accent), 120 Kennedys Lane facade, 120-frame scrub. Pipeline documented in its README: still → motion (free ffmpeg Ken Burns stand-in, IN PLACE now) or Seedance push-in (prompt ready in SEEDANCE-PROMPT.md, M5, 10s — Hunter runs it in Higgsfield, credits gate) → fps=12 frames → harness. Harness improvement over v1: direct scroll-snap fallback when rAF starves (embedded/backgrounded contexts). Verified live in browser (visible state): hero, scrub, captions all working. Photo is 10x's own Salisbury delivery — clear with Murph before public use.
