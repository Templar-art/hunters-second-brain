---
type: concept
tags: [remotion, motion-graphics, video-editing, research, roadmap]
status: active
updated: 2026-10-16
---
# Remotion motion upgrades — research + roadmap

> Context: built for Hunter's personal side work (fitness coach edits, e.g. Tyson's intro reel). Separate from 10x Visuals.

Research done 16 Oct 2026, after Hunter approved the Tyson explainer v4 (`projects/remotion-pipeline/app/`, composition `Explainer`). This page lists what would lift the next edit from "solid" to the reference quality (Use Software "Definitions" reels), ranked by impact for the effort. Read alongside [[talking-head-edit-standards]].

## Status — 16 Oct 2026 (v5)
Built into the Tyson explainer v5: 1 real word timing (sherpa-onnx zipformer from GitHub releases, aligned to the clean script; 94/100 words matched by ASR, rest interpolated), 2 `CameraMotionBlur` on all graphic layers, 3 face-centred push-ins and word zoom bumps, 4 `<LightLeak>` at the section changes, 5 grain + vignette + grade, 6 face tracking (OpenCV Haar, `tools/track.py`) driving punch-in origin, face circle and caption height, 7 text behind the subject (u2net_human_seg cutouts) on "FOLLOW?" and "FASTER", 8 hand-drawn SVG icons replacing the emoji (not Lottie, since there were no Lottie assets), 9 progress ring counter, 10 impact shake on the shortcut scene, 12 a 3D dumbbell on the end card (`@remotion/three`, render with `--gl=swangle`), 13 shards pulse on the music beat, 14 all copy moved to `src/script.json`.
**Not done:** 11 image/B-roll cards. Needs client photos/footage or paid Higgsfield generation.

## Tier 1 — biggest win, low effort
1. **Real word-level timing.** Captions and SFX are currently timed by guessing (each phrase spread across its words by length). Switch to `@remotion/install-whisper-cpp` → `toCaptions()` → `createTikTokStyleCaptions()` from `@remotion/captions`, with `tokenLevelTimestamps: true` and `combineTokensWithinMilliseconds: 200`. Highlights then land exactly on the spoken word. *Blocker:* the model weights are hosted on Hugging Face, whose file server is blocked from the cloud container. Run it locally on the Mac, or allowlist the HF file server.
2. **Motion blur on fast moves.** Iris wipes, card slide-ins and punch-ins look "digital" without blur. Remotion has a camera-motion-blur component (`@remotion/motion-blur`); check the API for the installed version before using it. Cheap alternative: a CSS `filter: blur()` driven by spring velocity.
3. **Eased zoom ramps instead of hard punch-ins.** Keep hard punch-ins on cuts, but add slow 2–4% push-ins across long takes and a quick zoom "bump" on key words (9 years, mistakes, faster).
4. **Light leaks / film-style transitions between sections.** `@remotion/light-leaks` `<LightLeak>` (v4.0.415+), placed at cuts with `TransitionSeries.Overlay` so the timeline length doesn't change. Give it about 45–60 frames to sweep. `hueShift` lets it match brand colours.
5. **Texture.** A subtle film grain/noise layer plus a light colour grade (lift blacks, warm mids) so the graphics and footage feel like one piece. All in CSS/SVG, so it costs nothing.

## Tier 2 — the reference look
6. **Face tracking** (the kit's `scripts/detect_faces.py` + mediapipe). Use it to keep captions and cards automatically clear of the face and mic, to aim punch-ins at the face, and to place the face circle from the real crop.
7. **Text behind the subject.** Person segmentation (mediapipe selfie segmentation) → put the big title *behind* Tyson. This is the most "premium" short-form trick right now.
8. **Animated icon library.** Lottie (`@remotion/lottie`) for dumbbell, plate, flame, clock and tick icons, replacing the emoji. Build a reusable fitness set once.
9. **Data-viz components.** Proper animated counters, progress rings, macro pie charts, before/after sliders and rep counters. These are reusable for every coach client.
10. **Impact camera shake + SFX sync.** A 2–4 frame shake on thuds and big reveals, with the SFX driven from the same event list as the animations (already partly there in `SoundDesign`).
11. **Image/B-roll cards.** Rounded-corner video or photo cards over the speaker on named things (gym, meals, hotel). Needs client footage or Higgsfield generation (credits → ask first).

## Tier 3 — later
12. **3D elements** (`@remotion/three`): a rotating plate or dumbbell for hooks.
13. **Audio-reactive accents** (the kit's `audio-envelope.mjs`): shards and grain that breathe with the music.
14. **Template-ise the system.** Turn the scenes into props-driven components (`SceneStat`, `SceneCards`, `ScenePath`, `FollowCTA`) plus a JSON script, so a new coach video is a script file rather than new code.

## Craft rules that came out of the research
- Use frame-based animation only (`useCurrentFrame`/`spring`/`interpolate`). CSS transitions flicker in renders.
- Leave caption room in the framing. Never crop so tight that text can't sit at chest height.
- Restraint: one idea per scene, and an effect only when it means something (an SFX or shake marks a reveal, not every element).
- Keep captions on the speaker's cadence. With real word timing (item 1) this becomes automatic.

## Sources
- Remotion light leaks — https://www.remotion.dev/docs/light-leaks
- Remotion transcribing / captions — https://www.remotion.dev/docs/captions/transcribing · https://remotion.dev/docs/install-whisper-cpp/convert-to-captions
- Remotion TikTok template — https://remotion.dev/templates/tiktok
- OpenMontage Remotion skill (transition durations) — https://skills.sh/calesthio/openmontage/remotion
- Opus talking-head guide 2026 — https://www.opus.pro/blog/talking-head-videos-guide
