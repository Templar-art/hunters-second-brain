---
type: project
tags: [audio, sfx, final-cut-pro, automation, tools, editing]
status: built-unproven
updated: 2026-10-29
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

## 28 Oct, v7: real recordings (preview only)
- Hunter: "If it can reach stuff online do it." Reachable from the cloud: GitHub, PyPI, npm. Everything else (Freesound, Sonniss, Pixabay, HF, Zenodo, archive.org) is blocked.
- Used `github.com/localhostnick/-open-sleep-sounds`, which **claims CC0 but isn't clean**. It's a single-commit repo created 27 Oct 2026; one file carries a YouTube channel's tags ("Mahakatha Meditation Club"), and others carry CC-BY and "(c) 2020" notices. So its birds, crickets and wind are staged in `sfx/unverified-preview-only/` (git-ignored, with a README-LICENCE) and tagged `licence-unverified`. The tool now prints and reports **LICENCE UNVERIFIED: preview only, do not deliver** whenever such a file is used.
- Bed gain can now go up to +24 dB (recordings vary: the crickets file sits about 18 dB under the birds file); the bed peak cap is -4 dBFS.
- v7: birds on day exteriors, crickets on the dusk shot, real wind on aerials, no interior ambience. Measured beds land about 5–18 dB under the music; where the music is loudest the birds are about 28 dB under, effectively masked. Sent.
- **For delivery:** use Hunter's own phone wild-tracks or Ocular ambience, which are verified licences.

## 28 Oct, v8: matching Desire by measurement
- Hunter on v7: "pretty good, right direction, just needs to be like the Desire one."
- **Measured, not guessed** (same detectors on both full mixes):
  - **Whoosh density:** Desire has a whoosh signature on 11% of cuts (HF rise p90 7.1 dB, max 13.5). Hunter's *source* edit already has 19% (max 26 dB), so his own whooshes are already louder and more frequent than Desire's.
  - **Loudness:** Desire is **-16.2 LUFS, LRA 5.4 LU**. Kollosche source is -15.7 LUFS, LRA 8.0; v7 was -18.1 LUFS because of the blunt preview turn-down. The 3 s RMS spread is 5.4 dB for Desire against 10.4 dB for Kollosche. **The biggest gap is mastering consistency, not effect count.**
  - Long-term spectral balance is similar; Kollosche is slightly brighter. My visual read of "continuous highs" in Desire's spectrograms didn't hold up when measured.
- v8 (`tasteful.json`): the whoosh budget is 15% of cuts **including the edit's own**, which left 2 new whooshes. Preview **mastering**: a two-pass EBU R128 loudnorm to -16 LUFS / LRA 6 / -1 dBTP, replacing the turn-down. Result: -16.0 LUFS, LRA 6.3. It applies to the preview only; in FCP use a compressor and limiter on the master to match.
- Placed: impacts at 1.4, 52.8 and 79.9 s, whooshes at 70.5 and 76.4 s, the K-pin glint, and the real (unverified-licence) ambience beds. Sent.

## 28 Oct, v9: "little sounds" + smoothing the music cut
- Hunter: Desire adds **little flavour sounds tied to what's on screen** (e.g. a mechanical switch when the kitchen lights come on). "Our video needs more spice." Also: **"there's a hard cut on the music when it goes back to day"** after the day-to-night section.
- Found the cut by measurement: the music's highs drop at **37.5 s** (dusk timelapse) and slam back at **42.17 s** (balcony returns to day). Hunter's own whoosh sits there too.
- New `asd/musicfix.py` (scene-map `music_fixes`): a **reverse swell** made from the incoming music (1 s after the cut, reverbed, reversed, about 5 dB under the music by the cut), placed as an editable clip in the FCPXML, plus a **0.7 s filter sweep** (preview only; in FCP keyframe a low-pass on the music 42.17→42.87 s).
- New foley categories **click** (switch/tick/latch) and **pop**. Scene-map accents are now exempt from density caps and spacing (they're deliberate flavour) but still respect the presenter and the edit's existing effects; their level floor is the film's median music level -6 dB, so an end card doesn't swallow them.
- Kollosche accents (from frame strips): a glint on the **light-flash transition** (2.79 s), a **pop** as the K pin lands (55.9 s), a **whoosh** on the tilt-up to the end card (80.4 s), a **tick** as the agent title appears (81.2 s), and a soft **hit** on the navy end card (85.3 s). No real light-switch moment exists in this edit; the click category is there for future ones.
- The placeholder accents use `committed-coaching/sfx-lib` click/pop files and the synthetic glint; real foley comes from Ocular Utility/Mechanica on the Mac.

## 28 Oct, v10 + colour
- Hunter: the K-pin glint was **"too tacky and too loud, needs a whoosh"**, so it's now a soft whoosh at -6 dB (scene-map accents can carry `level_db`). He then said **colour difference is the biggest thing**: Desire looks more premium.
- Measured the grade on both films. See the colour table in [[desire-the-pilot-reference]]: ours has lifted blacks, too much saturation and yellow throughout, and no cool tones. Built `grade/measure.py` (CIELAB stats) and the test grade `grade/desire-match.ffmpeg.txt`. Sent before/after stills and a graded copy of v10 (`…_SOUND-MIX_GRADE-TEST.mp4`; re-encoded, so not the picture-untouched deliverable).

## 28 Oct, v11: seamless music return, timing, day→night story, LUT
- Hunter: "time the SFX a bit better… the audio fix isn't as good as I hoped, needs to be seamless… try creative stuff like Desire… the colour grading looks fucked, def not the same."
- **The music cut, diagnosed properly.** The dusk section (37.5–42.2 s) is the same song low-passed (-29 dB above 2 kHz) and about 9 dB down, and the music after 42.17 s comes back **about 180 ms (0.37 beat) off the beat grid**. A swell can't hide a rhythm stumble.
- **`musicfix.seamless_return`:** rebuilds the muffled section from the music **3 bars after the cut** (whole-bar shift, so the grid runs straight through 42.17), applies the measured muffle curve, level-matches it to the original (within about 1 dB), hands over from the original at 39.48 s inside the quietest part with a 0.5 s cosine blend, then opens filter and level together over **one bar** (1.98 s, eased). Verified: onset phase is continuous through the cut, and the level rises -24 → -15 dB without a step. FCP: the rebuilt span is a `music`-role clip, and the source audio is muted over that span via `audio-channel-source`/`mute` (DTD-valid; import untested).
- **Timing:** impacts now land on the music hit (they snap to a cut only within 60 ms, down from 300 ms), and whoosh peaks lead the cut by 40 ms.
- **Creative, day→night story:** a soft downward whoosh at 37.45 s as the timelapse darkens, crickets heard faintly through the glass across the dusk section (`night_interior` label, -6 dB), and birds return at 42.2 s.
- **Colour v2 (`grade/transfer.py`):** a real **.cube LUT** from statistical transfer against Desire's frames (L* quantile tone curve + per-band a*/b* mean/spread, blended by strength). The 75% LUT gives shadow floor 10.2, contrast 69, chroma 14.7, highlight b 6.1: gentler and more natural than the rejected ffmpeg-filter grade. Sent with stills comparing ours, the LUT and Desire. Honest limit: much of Desire's "premium" is exposure, lighting and content (high-key bright interiors, water, dusk), which a global LUT can't create.

## 28 Oct, cause of the 42 s music cut + next test
- Hunter: the 42 s stumble came from **cutting the song by hand to shorten it so it ends on its natural ending** (as Desire does), and the edit landed off the beat. Opportunity: a **music fitter** that shortens or lengthens a song to the film's length with **bar-aligned edits** (matching phrase, crossfade on the downbeat) so it ends on the song's real ending. Not built yet; needs the original full-length song file.
- **Next test video (29 Oct):** slower, earthy real-estate edit, with lifestyle at the start and then the property; lots of pool and drone. Hunter will only add his own whooshes on speed ramps and his sun-flare shimmer, so the tool's existing-effects detector must leave those alone. Hunter warns the **colours are hard** on that one, so it needs grading help as well as sound. He'll upload **his full sound library** (owned Ocular etc., about 9 GB on the Mac; licence-clean, so it replaces the preview-only ambience). Ambience it will want: pool water (lapping, filter hum), drone air/wind, outdoor birds, earthy interiors. These need **owned recordings** for delivery (the current recorded ambience is licence-unverified, preview only).

## 28 Oct, colour verdict
- Hunter: **"I liked the one I did, it suited… the Desire one you did is just dark."** Both grade attempts (the ffmpeg filter and the 75% transfer LUT) are rejected for Kollosche Esther Pl; his own grade stands.
- **Standing rule for colour help:** don't chase a reference's numbers. Matching Desire's deep shadow floor (L p10 7.5) reads as *dark* on a bright 10x interior edit. Keep Hunter's brightness and exposure; only fix shot-to-shot consistency (white balance, exposure matching) and offer subtle tweaks on request. A look LUT, if any, must not lower midtones or blacks.

## 29 Oct, first Mac run: Coastal 34 Albany Ave (Katrina Walsh)
- **Setup on the Mac works**: `setup.sh` clean, 40/40 tests (one test fixed for macOS `/tmp` -> `/private/tmp`), full Ocular library indexed (1,547 sounds, ~45 s, cached).
- **Owned recordings, no downloads**: Pixabay files already on the Mac (Desktop `_Brand & Tools/SFX Library`, Downloads) cover pool water, soft wind, wind in trees, birds, nature, curtain breeze, a gentle creek. Copied into `sfx/pixabay-owned/` with `.tags` sidecars. Ocular City Park loops tagged day birds; Danum Valley night/evening loops tagged dusk crickets.
- **Catalog words leak into tags**: Ocular's catalog descriptions say "pool" and "breeze" for jungle loops, so a scene tag must be a word no catalog uses (`poolside`, `curtainbreeze`, `watersidecreek`).
- **New in the tool**: `pool` and `waterfront` scene labels; **layered beds** (`LAYERS` in `asd/scenes.py`: aerial = wind + birds at -6 dB, pool = water + birds, balcony = birds + curtain breeze, waterfront = creek + birds); `presets/earthy.json` (tasteful minus impacts, risers and shimmer, plus an `avoid_words` blocklist after the first pass picked an "Action Sports Hit", a motorbike throttle and a mouse click); `per_minute: 0` now really switches a category off; **stems**: `<video>_sfx_ambience.wav` + `<video>_sfx_accents.wav` beside `_sfx_only.wav`, so Hunter imports audio into FCP instead of a baked preview.
- Hunter on the test section: "looks pretty good, just in the air needs aerials noise like wind and birds" -> layered aerial beds. No colour work on this job; the song is his.
- Scene map: `scene-maps/coastal-43-albany-main.json`. CG birds + tracked Coastal pins for the same film: [[coastal-albany-birds]].
- **Reel music cut (Einaudi, Experience)**: Hunter's brief was intro 0-10 s, build 10-20/25 s, last stretch the song's own fade. Cut beat-aligned (librosa, 92 BPM) with chroma-matched joins, every join landing back on the song's real drop at 276.64 s and its decay to near-silence at ~288.6 s. Two versions in `output/einaudi-reel/` (A intro -> climax -> drop, 32.6 s; B intro -> build -> peak bar -> drop, 31.2 s), each with a straight-gain master at about -14 LUFS / -1 dBTP (no compression). This is a manual first version of the proposed **music fitter**.

## Not yet known
- **Whether it sounds good.** Nobody has listened to the preview yet.
- Whether the FCPXML imports into FCP 12.4.
- How it does on a full Ocular library (1,547 sounds). Indexing is cached by mtime and size; the first index runs one ffprobe per file.
- No ambience or shimmer in `sfx-lib`. Ocular Rainforest/Cityscapes should cover ambience. Shimmer may not exist in Ocular, in which case [[sound-lab]] could make some.

Related: [[sound-lab]] · [[sfx-library]] · [[sfx-sourcing-and-design]] · [[fcp-plugin-research]] · [[video-edit-pipeline]]
