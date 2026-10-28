---
type: project
tags: [audio, sfx, final-cut-pro, automation, tools, editing]
status: built-unproven
updated: 2026-10-28
---

# Auto Sound Design

A local command-line tool that gives a finished real-estate edit an automatic first sound-design pass, with no timestamps or markers needed. Hunter asked for it on 28 Oct 2026. It lives in [projects/auto-sound-design](../../projects/auto-sound-design/), and setup plus usage are in its [README](../../projects/auto-sound-design/README.md).

**Input:** a video (with its music), an optional separate music file, and a folder of owned SFX. **Output:** a preview video (picture stream-copied, untouched), a full-length effects-only WAV (48k/24-bit), an FCPXML project with each effect as its own clip, and `edit_decisions.json` + `REPORT.md`, which record every effect's time, file, level, reason and confidence.

It needs Python, FFmpeg and numpy (lxml is optional, for XML validation). It runs offline, costs nothing and touches no credits.

## How it decides
- **Cuts:** FFmpeg scene scores. A cut counts when it's a local peak that either clears 0.3 or stands 6× above the surrounding frames (similar-looking interiors cut together score low).
- **Music:** spectral-flux onsets, loudness, an autocorrelation tempo (the beat grid is only used when its confidence is ≥ 0.35), and **energy rises**: the loudness of the next 1.5 s against the previous 1.5 s, at least 5 dB.
- **Rules:** impact on an energy rise, plus a riser peaking into it if the rise is ≥ 7 dB. Whoosh peaking on a hard cut, but only when the cut lands on a music onset or beat, capped at 35% of cuts and 4 per minute. Ambience bed under the opening. Shimmer on the last cut in the final 20%.
- **Limits:** 3 s spacing, at most 8 one-shots per minute, at most 2 sounding at once, 1 bed, no file repeated back to back. Choices are seeded, so they're reproducible.
- **Alignment:** a whoosh or riser lines up its peak with the cut, and an impact its attack (the sharpest jump before the peak, so a whoosh-into-hit lands on the hit). Offsets snap to whole frames as exact rationals; the snap error is logged per effect.
- **Levels:** set relative to the local music RMS, then capped by a per-category peak ceiling (impact -6, whoosh -9, riser -10, shimmer -14, drone -18, ambience -20 dBFS), because RMS under-reads transients. The clipping check turns down only the effects that cause an over (max 3 dB each), and never the source.
- **Library:** categories come from words in filenames, folders, `.tags` sidecars and `catalog.csv` (so the Ocular catalog feeds it). Folders starting with `_` are skipped.

**Honesty labels are built in.** Every placement is marked heuristic. The tool doesn't know what a shot shows (drone, room reveal, flare, twilight), and categories are name-based, not heard. There's no dialogue detection, so it never ducks. The generation-provider interface (`asd/providers.py`) is **off**, with no provider implemented (no Soundbot), keys only from environment variables, and a typed `yes` required before any paid call.

## Final Cut XML
It writes **FCPXML 1.10**, the DTD Apple publishes in its developer docs (checked 28 Oct 2026; a third-party tool lists 1.14 for FCP 12.0, but Apple's page still shows 1.10). The XML has a new event, **Auto Sound Design**, with a project containing the source video and SFX connected below it on the *effects* role, each with `adjust-volume` and fade params. Media is referenced in place by absolute `file://` URL. Connected offsets include the video's timecode start. The XML is DTD-valid in every test. ⚠️ **It has not been imported into Final Cut yet**, so it isn't called compatible until Hunter imports one into a throwaway library. If fades cause trouble, turn them off with `fcpxml.write_fades: false`. [[sound-lab]] writes v1.11 for the same job and is also not import-tested.

## Verified (28 Oct, cloud session)
- **31 unit + end-to-end tests pass.** They cover NTSC and drop-frame rational timing, effects staying inside the video on frame boundaries, peak concurrency and lanes, spacing and sparseness, the per-category peak ceiling, seed reproducibility, missing video/SFX/config errors, manifest tagging (folder, sidecar, catalog, filename), DTD validity, timecode-offset maths, the clipping check, and an end-to-end run on generated media in a path with spaces (all 5 known cuts found within 1 frame, the energy rise found, the preview picture byte-for-byte stream-copied, the source unchanged).
- **Real media:** `projects/10x-site/assets/davenport-hero.mp4` (66 s, 23.976) with the Ocular trims in `committed-coaching/sfx-lib/`. A 20 s short test came first: all 9 cuts were checked by eye on frames either side, and all were real shot changes. The full run placed **8 effects across 41 cuts**: 2 riser+impact pairs on the 17.35 s and 48.37 s energy rises, and 4 whooshes. Whoosh and riser peaks landed within -22 to +9 ms of their targets (under half a frame). Tempo confidence was 0.29, so the beat grid wasn't used.
- **Lessons from the real run:**
  1. Ocular whooshes run 3.6–5.8 s with designed tails, so a 3.5 s whoosh limit excluded every one of them. It's now 6.5 s.
  2. Booms got too loud from RMS matching alone, which is why the peak ceilings were added.
  3. The `_magnific` rejects in `sfx-lib` were being picked, which is why `_` folders are now skipped.
  4. The hero's music is mastered to about 0 dBFS (AAC overshoot to +0.2), so any SFX tips it over. The preview is turned down about 2 dB, and the report says to pull the music or limit the master in FCP.

## 28 Oct, second round: test section + Kollosche
- Hunter sent the **Kollosche 5 Esther Place** edit (`Main.mp4`, 87 s, 960×540, 23.976) from his phone and asked for a reviewable 20–30 s section with a **playable mixed video** as the main deliverable, plus editable effects for FCP.
- Added `--start`. A section begins on the nearest keyframe so the picture is stream-copied: all 649 frames were checked byte-identical to the source. The output is now named `…_SOUND-MIX.mp4`.
- Run folders now carry `sfx_used/` copies, and the new `relink` command re-points the XML at Mac paths after moving the folder.
- **Test section 16.7–43.8 s** (chosen to avoid Eddie on camera at about 6–15 s, since there's no dialogue detection): 16 cuts, tempo 121 BPM (beat grid used). It placed 4 effects: a whoosh at 17.7 s (aerial to aerial), a whoosh at 31.0 s (which happens to land on a whip-pan blur transition), and a riser + boom at 42.2 s on an 8.3 dB music lift. The music is hot, so the preview is turned down 2 dB. **Waiting on Hunter's listening review before the full 87 s.**
- The reference "copy this style" video (YouTube `myH4QIY-y7E`) couldn't be fetched because YouTube is blocked by the cloud network policy. It needs uploading, or the domains allowed. Environment notes: [CLOUD-SETUP.md](../../projects/auto-sound-design/CLOUD-SETUP.md).
- 33 tests pass.

## 28 Oct, dense preset
- Hunter asked for the full video "jam packed with SFX". Added `presets/dense.json`: a whoosh on most cuts, impacts on cuts that land on strong music hits, 1 s spacing, up to 3 overlapping, and tails trimmed (whoosh 1 s, impact 2 s after the hit) so dense layers don't smear.
- Placement now rotates files (unused first, then least-recently-used) and tries the next file when one doesn't fit, instead of dropping the moment.
- Kollosche full run, dense: **44 effects in 87 s** (24 whooshes, 15 impacts, 5 risers). Each of the 4 whooshes is used 6 times, so repeats are audible; the full Ocular library fixes that. Effects land at 9–12 s over Eddie talking, because there's no dialogue detection.
- The first full default run was sparse: 9 effects.

## 28 Oct, tasteful preset (Hunter's direction)
- Hunter's verdict on dense: **"Only tasteful though, nothing over the top."** Added `presets/tasteful.json`: whooshes only on cuts that land with the music (max 30% of cuts), impacts only on real music lifts, 2.5 s spacing, levels about 3 dB under default, short tails.
- Kollosche full run, tasteful: **19 effects in 87 s** (12 whooshes, 4 impacts, 3 risers). Sent for review. A whoosh at 12.3 s still sits over Eddie talking.
- Hunter asked about creating new SFX "with sound bite". No product by that name could be verified (28 Oct web search found only generic App Store "AI Sound Effects Generator" apps), so he's been asked which one he means. Nothing integrated.

## 28 Oct, scene ambience (Hunter: "that's really fucking good" on tasteful; wants scene-specific SFX + ambience)
- A colleague noted **"there's no ambience"**. Measured: the old beds sat 18–25 dB under the music, so effectively inaudible.
- Claude watched one frame per detected shot (55 shots) and wrote `scene-maps/kollosche-5-esther-pl-main.json`: exterior, aerial, dusk, interior, bathroom, balcony, presenter and end-card stretches, plus accents for the sun flare (24.3 s) and the K pin landing (55.9 s; the pin head pops 0.5 s into the shot).
- New `asd/scenes.py`: one ambience bed per scene, tag-matched and crossfaded (0.6 s), with varied in-points. Presenter stretches are kept clear of one-shots, which fixes the earlier whoosh over Eddie. Beds are excluded from the clipping trim. Levels are now about 11–16 dB under the music (exterior/aerial nearer -11, interior -15); the opening exterior is heard before the music swells.
- New `asd/synth.py` (`sounddesign.py synth`): free, seeded **synthetic** stand-ins (outdoor breeze + birds, aerial wind, interior room tone, dusk crickets, soft glint), tagged `synthetic`. Not yet listened to. Recorded Ocular ambience should replace them on the Mac.
- Kollosche tasteful + scenes: 32 placements (about 14 beds plus one-shots and 2 glints). Sent for review. 37 tests pass.
- **Honesty line:** the tool still has no vision. The scene labels come from Claude's frame review, recorded in the map file and in every placement's reason.

## 28 Oct, Desire reference + "I have some effects on some already"
- Hunter uploaded the Desire Media reference ([[desire-the-pilot-reference]]) and warned that some edits already carry effects.
- **`existing_sfx`**: a whoosh counts when high-frequency noise rises ≥7 dB into the cut with higher flatness; a boom when there's a one-off sub spike ≥11 dB that later kicks don't match (so a music drop isn't counted). Placement skips one-shots within 0.6 s of one. On Kollosche Esther Pl it found **6 baked-in whooshes** (16.7, 24.2, 42.2, 43.2, 57.4, 58.4 s); earlier passes had doubled three of them.
- **`cut_motion`**: motion blur across a cut (sharpness near the cut against about 1 s away). It boosts whoosh scores, and a moving cut qualifies even when it isn't on a music hit.
- The tasteful preset now caps whooshes at 22% of cuts, Desire's density. Kollosche v5 placed 10 whooshes, 3 impacts and 1 pin glint plus the scene beds; the sun-flare glint was dropped because the edit already has a whoosh there.
- 37 tests pass. Sent v5 for review.

## 28 Oct, v5 rejected → v6
- Hunter on v5: **"it sounds so bad, and too much SFX especially on interior shots."** He already had his own sun-flare sound (the detector had flagged that cut). Insight: Desire's film has far more camera movement; ours has good *flow* but little movement, so the SFX should **back the flow** rather than decorate cuts.
- v6 rules (`tasteful.json`): whooshes only where the film **changes zone** (outside/inside/aerial, from the scene map) or the camera visibly moves; nothing on static interior→interior cuts; **no interior ambience** (Desire's interiors are clean, and the synthetic room tone was the likeliest "bad" sound); whooshes quieter (-13 relative, -14 dBFS peak cap). Result: 8 one-shots + outdoor/aerial/dusk beds. Sent.
- Hunter also noted that **the models in the Desire film are AI**. That's a separate thread: AI lifestyle talent for 10x edits. Not started; it would go through Higgsfield and needs credit approval.

## 28 Oct, the ambience verdict
- Hunter: **"The ambience doesn't sound good… wind doesn't sound like wind… this is how we go from good to great."** Day shots should have birds and night/dusk shots crickets.
- The synthetic kit is rejected for client work. The aerial wind bed is off and recorded files are always preferred over synthetic (`scenes.prefer_recorded`). A `night` label has been added.
- **Getting real recordings into the cloud is blocked:** freesound.org, cdn.freesound.org, sonniss.com, pixabay.com, archive.org, zapsplat.com and BBC sound effects are all denied by the environment network policy (checked 28 Oct). Options: Hunter uploads recordings (his own phone wild-tracks, or Ocular ambience from Drive), or allowed domains are added in the environment settings, or the work moves to the Mac with the full Ocular library.

## Not yet known
- **Whether it sounds good.** Nobody has listened to the preview yet.
- Whether the FCPXML imports into FCP 12.4.
- How it does on a full Ocular library (1,547 sounds). Indexing is cached by mtime and size; the first index runs one ffprobe per file.
- No ambience or shimmer in `sfx-lib`. Ocular Rainforest/Cityscapes should cover ambience. Shimmer may not exist in Ocular, in which case [[sound-lab]] could make some.

Related: [[sound-lab]] · [[sfx-library]] · [[sfx-sourcing-and-design]] · [[fcp-plugin-research]] · [[video-edit-pipeline]]
