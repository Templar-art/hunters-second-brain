# JOB — Strategic Investing: Brian property/equity ads (A/B cam cuts)

- **Client:** Strategic Investing (Brian). Shot 10 Nov 2026, directed by Damon. Brief: `~/Downloads/Strategic Investing — Property and Equity Ad Shoot Brief 10 Nov 2026.md`
- **Footage:** `/Volumes/Kristian T7/Brian Ads/` — A7siii 1/C8202 (A, wide full-body, lav audio, log) + A7siii 2/C9731 (B, close side angle). One continuous take each, vertical 4K25.
- **Sync:** A = B + 63.52 s (audio xcorr, stable 200/600/1000 s). TC not jammed (A 12:06:57:03, B 16:07:31:05).
- **Status:** 2026-11-11 — A/B rough selects built for all 10 scripts (`Brian_AB_cuts.fcpxml`, `picks.md`, `previews/`). Awaiting Hunter review. Not graded, no captions/compliance line yet.
- **Method:** Brian was fed line-by-line; Damon's prompts separated by lav loudness (>41 dB = Brian). Last clean take of each line picked from the FCP transcript; camera flips on every take change to hide jumps.

## 2026-11-11 v2 — graded, 3-angle, captioned
- Resolve project **Brian Ads AB** (10 timelines, `resolve_build.py`): W = A wide, M = A punch-in (zoom 1.5, tilt -150), C = B close; open + close on W, never same angle twice in a row (`angles.json`).
- Grade: A gets `A_SLog3_to_Bcam_match.cube` (Sony LC-709 TypeA + fitted match to B, installed as `Sony/10x_A_to_Bcam_match.cube` in Resolve's LUT folder). B untouched.
- Audio: A lav only; Voice Isolation 40 + Dialogue Leveler per clip; 4-frame centre crossfades on every cut; loudnorm -14 LUFS / -1 dBTP after render.
- Captions: `caption_text.json` (corrected as-spoken text) aligned to whisper word times, one line, Poppins SemiBold on soft dark pill (white alone vanished on the gingham shirt). SRTs in `srt/`.
- Delivered locally: `finals_clean/` + `finals_captions/` (4K vertical), `previews/` 1080.

## Ledger
No credits spent (all local).
