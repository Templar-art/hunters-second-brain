# Handoff: Auto Sound Design (from the 28 Oct 2026 cloud session)

Read this first in a new session, then `wiki/projects/auto-sound-design.md` (the full history) and
`wiki/craft/fcp-resolve-workflow.md` (colour/Resolve). Everything below is pushed to `main`.

## Where things stand
- **Tool:** `projects/auto-sound-design/` (Python + FFmpeg + numpy). `./setup.sh` once on the Mac (it asks before installing), then `./run.sh "video.mp4" ...`. 40 tests: `python3 -m unittest discover -s tests`.
- **Hunter's preferred sound recipe** (Kollosche 5 Esther Pl, v11):
  ```
  ./run.sh "Main.mp4" --sfx "$HOME/Music/SFX Library/Ocular Sounds" --sfx sfx/generated \
      --config presets/tasteful.json --scenes scene-maps/<video>.json
  ```
  - `presets/tasteful.json`: whooshes only on zone changes (outside/inside/aerial) or camera motion; the edit's own whooshes count toward a 15% budget; no interior ambience; preview mastered to -16 LUFS / LRA 6 (Desire measured -16.2 / 5.4).
  - The scene map (JSON) labels each stretch (exterior/aerial/dusk/interior/bathroom/balcony/presenter/night_interior/endcard), adds on-screen accents (`accents`, with optional `level_db`) and music fixes (`music_fixes`: `seamless_return` rebuilds a muffled section phrase-aligned and opens it over one bar). Claude writes it after viewing one frame per shot.
  - The tool detects **effects already in the edit** (`existing_sfx`) and keeps clear of them. Hunter adds his own whooshes on speed ramps and a sun-flare shimmer.
- **Ambience:** the synthetic kit was rejected ("doesn't sound good, wind isn't wind"). The cloud previews used licence-unverified GitHub recordings (`sfx/unverified-preview-only/`, flagged LICENCE UNVERIFIED; **never deliver those**). On the Mac use **Ocular ambience** (Rainforest, Cityscapes) tagged with `.tags` sidecars: `ambience, outdoor, birds, day` / `ambience, dusk, crickets, night` / `ambience, aerial, wind`. Recorded beats synthetic automatically.
- **Hunter's feedback that shaped it:** tasteful, not over the top; nothing on static interior cuts; the K-pin glint was tacky (now a soft whoosh); day shots get birds, night shots crickets; Desire uses *fewer* whooshes than we assumed (about 11% of cuts), and its edge is consistent mastering plus small on-screen flavour sounds.
- **Colour: parked.** Automated Desire matching (ffmpeg grade, global LUT, per-type LUT v1–v4) all read wrong to Hunter. **His grade stays.** Kept: `grade/assist.py` (per-shot consistency fixes as FCP Color Wheels words + Resolve Gain numbers; `--contact-sheet`, `--heroes`, exterior-hero mode) and `grade/resolve_bridge.py` (builds a per-shot Resolve Studio timeline + PowerGrade + CDLs). **The bridge has never run against real Resolve:** dry-run first, then a throwaway project.

## Not yet confirmed on the Mac
1. FCPXML import into FCP 12.4 (DTD-valid 1.10; includes `music`-role clips and `audio-channel-source` mutes).
2. `setup.sh` / `run.sh` on macOS.
3. Indexing the full Ocular library (about 1,547 sounds; cached after the first run).
4. The Resolve bridge (Studio, External scripting = Local).

## Next job (Hunter, 29 Oct)
A slower, earthy edit: lifestyle at the start, then the property; lots of pool and drone. He'll supply:
- the graded edit (with his speed-ramp whooshes and sun-flare shimmer already in);
- a flat export (Camera LUT = None), for the consistency check;
- the **full original song** (he hand-cut Kollosche's song to end on its natural ending and landed it off the beat; a bar-aligned **music fitter** is proposed but not built);
- his sound library (on the Mac: `~/Music/SFX Library/Ocular Sounds`).

Deliver: a playable `…_SOUND-MIX.mp4` first as a 20–30 s test section for review, then the full film; FCPXML with editable clips; grade notes (consistency only). Pool water, drone air, birds and crickets need **owned** recordings.

## House rules (from CLAUDE.md / Hunter)
- Money, not git: commit and push freely; any paid op (Magnific, Higgsfield, ElevenLabs) needs Hunter's explicit go-ahead.
- Never call the result "polished" or "FCP-compatible" until Hunter confirms it.
- Keep videos, audio and keys out of git (`input/`, `output/`, `sfx/` are git-ignored).
