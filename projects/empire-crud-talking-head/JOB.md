# JOB — USE Software: CRUD talking head (motion graphics)

- **Client:** USE Software (usesoftware.com.au, Gold Coast/Brisbane). ⚠️ v1 wrongly used Empire Technologies branding from the reference.
- **Brief:** Restyle the 13 Oct talking head ("CRUD") to match the Empire "AI Defence Protocol" motion reference (assets/reference.mp4).
- **Status:** v2 delivered for Q/A — 2026-10-09
- **Cost:** $0 / 0 credits (local render: Chrome canvas + Playwright + ffmpeg; SFX synthesised in Python)

## Build
- graphics.html: all scenes, timed to the VO word timestamps (faster-whisper)
- render.cjs: renders graphics as ProRes 4444 with alpha; sfx.py: SFX bed
- Cut: 0–5s talking head with hook card → dark wipe → full-screen graphics with VO underneath → end card with Empire logo (22.5s)
- Fonts: DM Sans + JetBrains Mono (closest Google matches to the reference). Logo: vector redraw, traced from the reference frame.

## Log
- 2026-10-09 v1 rendered (empire-crud-v1.mp4). Awaiting Hunter feedback.
- 2026-10-09 Hunter feedback on v1: wrong colours (client is USE Software), easing not matching reference, wants face in corner on some scenes.
- 2026-10-09 v2 rendered (use-crud-v2.mp4). Brand from site: blue gradient #009BEB→#01E5EE, Barlow Condensed 700 headings / Barlow body, official logo (assets/use-logo-long*.png). Motion: expo-out masked line rises (0.55s, 70ms stagger), 26 cps mono typing, drawn rules/arrows, hard cuts. PiP face 8–19.8s bottom-right (mask-reveal hole). Build: ./build.sh v2. Internal QA fixes: Users spacing, REST API timed to its word, PiP recentred.
