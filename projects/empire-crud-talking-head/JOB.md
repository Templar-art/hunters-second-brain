# JOB — Empire Technologies: CRUD talking head (motion graphics)

- **Client:** Empire Technologies (software)
- **Brief:** Restyle the 13 Oct talking head ("CRUD") to match the Empire "AI Defence Protocol" motion reference (assets/reference.mp4).
- **Status:** v1 delivered for Q/A — 2026-10-09
- **Cost:** $0 / 0 credits (local render: Chrome canvas + Playwright + ffmpeg; SFX synthesised in Python)

## Build
- graphics.html: all scenes, timed to the VO word timestamps (faster-whisper)
- render.cjs: renders graphics as ProRes 4444 with alpha; sfx.py: SFX bed
- Cut: 0–5s talking head with hook card → dark wipe → full-screen graphics with VO underneath → end card with Empire logo (22.5s)
- Fonts: DM Sans + JetBrains Mono (closest Google matches to the reference). Logo: vector redraw, traced from the reference frame.

## Log
- 2026-10-09 v1 rendered (empire-crud-v1.mp4). Awaiting Hunter feedback.
