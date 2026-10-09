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
- 2026-10-09 Hunter: v1/v2 rejected, match the series refs (Downloads/MCP.mp4, API.mp4: USE "Definitions" episodes, speaker Sam Bruhn, Founder & CEO).
- 2026-10-09 v3 rendered (use-crud-v3.mp4, 23s). Rebuilt in v3.html: TH drawn in-canvas from frames, rembg person matte for title-behind-head, word captions + sliding cyan highlight, Sam Bruhn lower third, triangle shards, triangle mosaic wipes, def card, navy "stands for" inset, endpoint diagram panel, full light slide with method pills / giant verb / users table + circle face, white Definitions end card, 5-subframe motion blur. SFX: sfx3.py. Render: render3.cjs (frames/mattes in build/, regenerate via ffmpeg + rembg).
- 2026-10-09 v4 (use-crud-v4.mp4, v4.html), self-QA against the refs side by side: tighter series framing (zoom 1.22, face at 25% height), punch-in zoom cuts at 3.6s and 12.3s, light slide layout moved up with a smaller circle face, verb swap no longer ghosts (faster exit), bigger endpoint diagram, end card raised, font preload fix.
- 2026-10-09 v5 (use-crud-v5.mp4, v5.html, sfx5.py, 23.6s): matched more reference motion. Vertical whip-blur exits on the slides (8 subframes, full-frame shutter), navy inset rises in and expands back to full frame, curl terminal card during "you are creating users", "200 OK" response card (status rolls, JSON types) that shatters into triangles going into the end-card wipe, name-card divider + moving shard accent. Render: PAGE=v5.html DUR=23.6 node render3.cjs video …
- 2026-10-09 Moved onto the reusable template (`projects/use-definitions/`). v6 = episodes/crud/crud-v6.mp4: same scenes as v5, rebuilt SFX engine (stereo, reverb, layered), last 12 frames ping-pong so Sam doesn't freeze. Folder renamed from empire-crud-talking-head. Wiki: use-software, use-definitions-series.
