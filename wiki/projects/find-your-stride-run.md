---
type: project
tags: [reel, talking-head, motion-graphics, social, ashley-cooper-construction]
status: provisional
updated: 2026-11-11
---

# Find Your Stride run reel (Ashley Cooper Construction)

A 9:16 talking-head social reel for **Ashley Cooper Construction** promoting the *Find Your Stride x Find Your Feet* charity run (speakers incl. Tommy and Aleks). Nine versions (v1 to v9, Nov 2026); v9 (`out/run_reel_v9_share.mp4`) is the latest. **Provisional:** no client sign-off recorded, and no JOB.md was kept. Project folder: [projects/find-your-stride-run](../../projects/find-your-stride-run/).

## What it taught us
- **Edit pipeline as code.** `build.py` tightens the talk from a whisper transcript (a segment list in source seconds, remapped onto the cut timeline), alternates a 1.0 and 1.14 punch-in zoom between segments to hide jump cuts, and adds a slow push on every segment plus a light ffmpeg grade. The local ffmpeg has no libass, so captions are PIL-rendered alpha layers (`graphics.py`).
- **Whisper timestamps bunch after pauses.** Words stack onto one timestamp, so caption timing needs spreading by character length, or DTW alignment (adopted in v4).
- **Motion graphics reuse the [[use-definitions-series]] canvas engine**, forked into `motion/` (Playwright renders `engine/page.html` frames; the `episode.js` scenes are race bib, heartbeat ECG, checklist panel, fundraising bars and a CTA panel with confetti). A per-face keep-out check (v5) and the textcheck pass enforce the rules in auto-memory `feedback-motion-never-cover-face-boss-review.md`: graphics never overlap faces, and confetti and pills stay clear of heads.
- **Client feedback trail, now standing defaults for this client's talk reels:** v2 dropped all whooshes, cleaned the voice and went to neutral white captions (the v1 cue report shows 7 Ocular Velocity whooshes at cut points, which was the wrong call for a charity talk piece). v7 removed every shot of a speaker reading off a phone (covered with B-roll and full-screen slides), kept the voice raw and put the AURENZA music bed under it. v8 removed the single-frame "talk flashes" at B-roll and slide boundaries, so **check boundary frames after every B-roll insert**. v9 fixed a name spelling, so **verify spellings of names on screen with the client before rendering.**

Related: [[reel-formats]], [[sfx-library]], [[motion-and-stills-tools]].
