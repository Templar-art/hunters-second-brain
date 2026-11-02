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
- **Reel music cut (Einaudi, Experience)**: Hunter's brief was intro 0-10 s, build 10-20/25 s, last stretch the song's own fade. Cut beat-aligned (librosa, 92 BPM) with chroma-matched joins, every join landing back on the song's real drop at 276.64 s and its decay to near-silence at ~288.6 s. Two versions in `output/einaudi-reel/` (A intro -> climax -> drop, 32.6 s; B intro -> build -> peak bar -> drop, 31.2 s), each with a straight-gain master at about -14 LUFS / -1 dBTP (no compression). This is a manual first version of the proposed **music fitter**. **v1 was rejected** ("no fade ... to make it smooth"): a 60 ms join from -30 dB piano into -12 dB orchestra is a hard cut. **v2** (`tools/reel_cut.py`) uses bar-long, beat-locked overlaps where the incoming part's own pre-roll bars play under the outgoing ones, joins picked so the overlapping bars share harmony (chroma 0.87-0.91), and a delayed equal-power fade-in (`rise`) so a loud section swells in. Rule: **a level jump over ~6 dB needs a 1-2 bar crossfade, never a cut.** Hunter liked A's shape but said it "didn't fade into the impact smoothly", and called B nice but too quick. **v2-C (slow cinematic, 44.8 s):** intro 0-12.1 s, a 2-bar overlap into the song's own build (100.19 s), its natural hit at 110.57 s continuing straight into the climax (266.24 s; the two match at 0.965), then the drop and the fade. Lesson: **let the song's own crescendo deliver the impact**. **Wildfire (Austin Snell, 103 BPM, vocals), 31.2 s:** instrumental intro 2.4-8.24 s, a 2-bar overlap into the bridge (140.32 s, chord match 0.87), the song's own dip and slam into the final chorus landing at 16 s, a same-line chorus splice 156.78 -> 175.61 (0.99), then the natural fade. **Vocal tracks:** run a demucs split (`~/.venvs/demucs`, about 12 s) and check vocals at every join. In an overlap, bring in the incoming part's *instrumental stem* first and switch to the full mix inside a vocal breath gap, so two lyric lines never cross and the level rises gradually instead of jumping 10 dB. Script: `tools/wildfire_cut.py`. Earlier in the same section:, and don't fade into the middle of a loud section.
- **Approved 29 Oct**: Hunter called the SFX good, with one change: no click on the end card, a whoosh there instead. Scene-map accents now take `"file"` (part of a library path) so approved picks stay pinned when anything else changes. Removing the click on its own had reshuffled the other whooshes into a "Race Sequence Overdrive". Then he dropped the end-card whoosh entirely. Removing it freed a whoosh slot, and the auto pass refilled it with the same "Race Sequence Overdrive". The fix was `presets/coastal-albany-locked.json` (no automatic one-shots; only the pinned accents play), plus "race/overdrive" in the earthy blocklist. **Locking an approved mix = pin the picks AND switch the auto categories off.** Final run: `output/Main_20261029-105451`.

## 29 Oct, Cinematic Reel (Wildfire, C. James) + Get Down flythrough song
- **Hunter cut "Cinematic Reel.mp4" (38.41 s, 9:16) to the Einaudi D song.** Its cuts sit on Einaudi's 2-beat grid: every 1.293 s through the interiors, with the top-down aerial at 22.11 = D's hit. He then asked for the C. James *Wildfire* to fit that picture. **Fit the song to the edit's anchors, not the other way round.** `tools/wildfire_cjames_fit.py` places the chorus hit (43.51 s) on 22.11 with a 0.64 s start trim. The bar-phase constraint `hit = 16.62 + 2.043k - start` meant k=3. Vocals enter about 9.8 s, on the woman-at-door cut. A splice at the 45.6 s vocal gap goes into the final chorus (115.94 s), and the song's natural fade starts on the balcony shot (32.5 s).
- **SFX:** `scene-maps/coastal-cinematic-reel.json` with the locked preset, reusing the two whoosh picks Hunter approved on Main: door at 10.05 and pool at 20.15. **Bug fixed:** a near-silent edit audio track (max -38 dBFS, exported before the music) produced a fake "boom already in the edit" that blocked the door whoosh. `existing_sfx` now returns nothing when the track peaks under -30 dBFS.
- **The "shing"** is Hunter's own sun-flare sound, from [[sfx-custom]] `shing_*.wav`, not a library sound. `tools/reel_mix.py` places hand accents by their own peak (`--accent FILE@TIME@PEAK_DB`). It writes `<video>_sfx_shing.wav`, masters the song with straight gain (-14 LUFS, -1 dBFS sample peak) and renders `<video>_REEL-MIX.mp4`. This reel uses `shing_classic`, peaking at 4.30 s where the flare blooms (luma 133 -> 147 across 4.2-4.5 s), at -17 dBFS.
- **Get Down (Put em up), Ryan James** (80.7 BPM), for the other flythrough reel, no picture yet:
  - The song already has Hunter's flow built in: chant intro 0-12, "Get down" hit at 12.25, build 12-23, drop at 23.0.
  - `tools/getdown_cut.py` runs two bars of the drop, then a half-beat overlap at 28.98 (just before the next vocal line) into the song's own ending at 181.56. That point is a vocal gap, and the splice was scored at chroma 0.86 / onset correlation 0.92.
  - The cut runs through the real hard stop at 189.45, for 36.9 s.
  - Output: `output/getdown-reel/GetDown_reel_mastered.wav`.
- **Get Down v2, PUNCHY** (Hunter on v1: "needs to be more punchy, more of the chorus where it goes quicker").
  - Song map on a 2.9705 s bar grid from 0:00 (chroma-matched sections):
    - intro 0-23.8;
    - verse 23.8-47.5;
    - **chorus 47.53-83**;
    - verse 83-130.7;
    - **chorus 130.7 to the end**.
  - Bar 15 (44.56) is the dip and build into the chorus.
  - `tools/getdown_punchy.py` cut:
    1. intro bars;
    2. the build bar, brought in on the instrumental stem and switching to the full mix in the 45.0 breath gap;
    3. five bars of chorus 1;
    4. a cut at the 62.38 vocal gap into the song's own last chorus bars and ending (181.20 -> 189.45).
  - **A**: 34.7 s, chorus at 11.9 s. **B**: 31.8 s, chorus at 8.9 s.
  - Every join is on a downbeat, with an equal-power crossfade of 0.12 s. Level stays within about 3 dB across each join.
  - Lesson: **for flythrough reels, Hunter wants the chorus early and most of the runtime in it.** The cinematic flow (intro to about 10 s, then build, then the song's own ending) suits slower films.
- **B SMOOTH (Hunter's pick, 32.0 s).** Hunter liked B, but its 0.12 s joins were "too harsh", so every join is now a full bar of overlap:
  - The last intro bar plays over bar 14, which comes in on the instrumental stem so the verse vocal stays out.
  - The last chorus bar fades out on the instrumental stem while bar 60, the ending's lead-in, swells in with its own vocal. Bars 20 and 60 sit in the same slot of their 4-bar phrases.
  - The incoming bar rises on a delayed equal-power curve (`rise` 1.6).
  - Rule, now confirmed on two songs: **joins in a reel are bar-long overlaps, never short crossfades, even between sections at the same level.**
- **B SMOOTH v2.** Hunter: "you can sorta hear it at the start." Two causes, both measured:
  - Bar 14, the pre-roll under the intro, **clashed harmonically** with the intro (chroma 0.58).
  - The intro sits **about 0.1 s off** a fixed 2.9705 s bar grid; the ending join was 70 ms out too.

  Fixes:
  - The reel now opens one bar in (bar 1, no vocals, 0.3 s fade-in), so intro bar 3 overlaps the build bar (chroma 0.98).
  - Every overlap is placed on that bar's **measured downbeat**: cross-correlate its onset envelope against the chorus downbeat.
  - The doubled hits in both overlaps are gone; length and chorus timing are unchanged (31.9 s / 8.9 s).

  Rules:
  - **Before overlapping two bars, check they match harmonically (chroma ≥ ~0.9) and line them up on measured downbeats, never a fixed tempo grid.**
  - Alternate intro bars often differ in harmony, so pick the overlap bar by similarity, not just by position.
- **Flythrough with Katrina's VO** (`34 Albany 1.m4a`). The flythrough video isn't on the Mac yet, so the VO sits at 0:00 as recorded.
  - **Transcript and trims:** transcribed locally with Whisper (`~/.venvs/demucs`, `small.en`). Her lines run 0.7-62.5 s. Her "I love it." aside at 63.2 s and a blip at 68.4 s are trimmed.
  - **Raw VO:** recorded at -37 LUFS. Cleaned with HPF 80, light afftdn and 2.5:1 leveling, then set to -16 LUFS.
  - **Song:** `tools/getdown_vo.py` takes the B SMOOTH v2 opening, then all of chorus 1. Bar 27 overlaps bar 55 (chroma 0.99, downbeats -84/+78 ms measured) into chorus 2, running to the real stop. Total 67.5 s, so about 5 s of song after her last word.
  - **Under the VO:** the song is the demucs instrumental, ducked 11 dB while she speaks (music about 11 dB under her, -26.7 vs -16.3 LUFS).
  - **After her last word:** the full mix with vocals swells back, 4 dB down so it doesn't jump.
  - **Reference mix:** -14.7 LUFS / -1.2 dBTP, made with straight gain plus a peak limiter. The stems are unlimited.
  - **Rule:** a rap or vocal song under a VO = the instrumental stem plus a duck. Lyrics over a spoken line fight it.
- **VO polish v2** (Hunter: "cut up the silences, make her sound more confident, make her voice sound better"). New tool `tools/vo_polish.py`:
  - **Pauses:** cut using Whisper word timings, inside the quietest part of each gap, with 20 ms crossfades. Full stops become 0.40 s, commas 0.24 s, other gaps 0.18 s. 6 s removed in total, so the VO went from 62.5 to 57.4 s.
  - **Voice chain:** set from her *measured* spectrum (phone take: 120-500 Hz +4..+7 dB over the mids, 1-4 kHz -10..-16, nothing above 12 kHz, noise only 31 dB under her). The chain:
    - HPF and afftdn;
    - -2.5 dB at 160 Hz, -3.5 at 320;
    - +2 at 1.6k, +6 at 3k, +3 at 5.2k, high shelf +3;
    - a light exciter;
    - de-ess;
    - 3:1 compression;
    - a soft gate on the pauses;
    - `atempo` 1.04 (brisker, same pitch).
  - **Result:** presence +8 dB, 4-8 kHz +7 dB, noise 46 dB under speech.
  - **QC:** re-transcribe the edited VO and diff it against the original. Every word was intact.
  - **Song re-fit:** chorus bar 25 overlaps bar 55 (chroma 0.98), 61.5 s. Mix -14.9 LUFS / -1.2 dBTP, music 11 dB under her.
  - **Next lever if she still doesn't sound confident enough:** the delivery itself. EQ can't add energy to the read. Options: a paid AI speech enhance (Magnific `audio_clean_speech`, credits, needs Hunter's go), or ask her for a re-record.
- **30-40 s reel cut of the VO.**
  - **Lines dropped:**
    - Hunter flagged that "three additional bedrooms on the lower level" was fluffed. In her take "additional" lasts only 0.34 s.
    - For the reel length, I also cut "with native birdlife and natural surrounds creating a peaceful setting", the balcony clause, and the whole spec sentence (kitchen, floors, 7.8 kW solar, "practical modern comforts").
  - **Script now:** hook -> views/beach -> three levels -> pool and cabana -> Currumbin lifestyle close. Later Hunter also flagged a hesitation in "Set high among the greenery" (her "the" runs 0.58 s), so that line is dropped too. The VO is 30.6 s, placed 1 s into the song.
  - **`vo_polish.py --drop FROM TO`:**
    - The cut lands at the energy minimum of each boundary gap, widened ±60 ms because Whisper often marks no gap between run-on words.
    - The join pauses as the dropped phrase ended (a full stop stays a full stop; otherwise the comma is kept).
    - Word timestamps after the cut are shifted so pause tightening still works.
  - **QC:** re-transcribed; it reads clean.
  - **Song:** chorus bar 22 overlaps bar 60 (the B SMOOTH v2 ending, chroma 1.00). 37.8 s, so about 5 s of hook after her last word. Mix -14.8 LUFS / -1.2 dBTP, music 11 dB under her.
  - **Bar maths for this song:** with the opening fixed, joins on the same 4-bar slot give 31.9 / 43.8 s, and 2-bar-slot joins give 37.8 s. Reel lengths come in those steps.
- **Flythrough flow and pop-ups.** The plan is in `projects/coastal-katrina/flythrough-reel-plan.md`; pop-ups come from `projects/coastal-katrina/popups.py`.
- **Flythrough SFX pass (29 Oct).** This was an SFX-only pass on Hunter's own cut, `Flythrough.mp4` (36.04 s). He had already cut the song and VO into the edit. The scene map is `scene-maps/coastal-flythrough-reel.json`, with the approved whooshes pinned at 8.09 s (into the house) and 16.27 s (out to the pool). The pass placed 24 effects. The existing-SFX heuristic read three music transients (17.73, 21.81 and 28.86 s) as whooshes already in the edit, so it kept clear of them. The output is in Desktop `10 Flythrough SFX`.
  - **Different look from the cinematic reel:** one continuous move; a door punch on the chorus drop (8.89 s); left-margin stem tags in place of centred cards; ending on the song's hard stop.
  - **Six cues,** each snapped to a song beat on or just after the VO word it echoes, with copy taken only from her VO.
  - **Placement:** 62% height, left margin. The script asserts every line clears a 170 px right zone for the IG button column; "…cafes nearby" failed it and was shortened.
  - **⚠️ Rejected (Hunter, 29 Oct): "I don't like those pop ins."** He wants the room-by-room VO map instead. Don't put feature pop-ups on this reel; ask before offering pop-up graphics on Katrina's reels again.
- Delivered as Desktop `Coastal 34 Albany - FCP/6 Cinematic Reel (Wildfire)` (song, ambience, whooshes, shing, preview) and `7 Flythrough Reel song (Get Down)`. Not yet heard by Hunter.

## Not yet known
- **Whether it sounds good.** Nobody has listened to the preview yet.
- Whether the FCPXML imports into FCP 12.4.
- How it does on a full Ocular library (1,547 sounds). Indexing is cached by mtime and size; the first index runs one ffprobe per file.
- No ambience or shimmer in `sfx-lib`. Ocular Rainforest/Cityscapes should cover ambience. Shimmer may not exist in Ocular, in which case [[sound-lab]] could make some.

Related: [[sound-lab]] · [[sfx-library]] · [[sfx-sourcing-and-design]] · [[fcp-plugin-research]] · [[video-edit-pipeline]]

## 2 Nov, Osupa Ti cut for Kollosche (64.3 s)
- Hunter asked for about a minute of *Osupa Ti (Radio Edit)* for a Kollosche listing. A plain trim with a fade (v1) skipped this page's method and was redone.
- The song is 119.7 BPM on a 2.004 s bar, with its downbeat on the 3rd tracked beat (librosa's tempo estimate said 117.5 and drifted, so bars come from the beat times). Map: intro to 33.6 s, break 33.6–49.6, drop 49.6–97.6, break 97.6–129.7, final drop to 225.6, then the decay.
- **v2** (`tools/osupa_cut.py`): two splices, each a whole 4-bar shift landing in a vocal breath gap (from a demucs split): 14.14 → 22.15 inside the intro, and 56.66 → 216.64 out of the first drop into the song's own ending (chroma 0.997, onset correlation 0.82). The levels match, so the joins use 0.24 s equal-power crossfades. Mastered with straight gain to -14.0 LUFS / -5.2 dBTP. Output: `~/Downloads/Osupa Ti - 64s Kollosche Cut v2.{mp3,wav}`. Awaiting Hunter's listen.
- **v2 rejected:** Hunter said it was good up to 48 s, then "jarring". The timing was fine (lag under 12 ms). The cause was the **arrangement**: the 56.66 → 216.64 jump went from a vocal section into the vocal-free instrumental outro, so the vocal and the mid-range dropped out (about 7 dB at 500–2 kHz) within 0.24 s. Rule: **a splice must also match what's playing (vocal or no vocal, which elements), not just chords and beat.**
- **v3:** 56.15 → 184.16 (bar 27 b1 → bar 91 b1, a vocal gap, into the song's *final vocal line*), then 191.63 → 223.63 (bar 95 → bar 111, both vocal-free) into the last bar and the decay. The vocal ends on its own and the mids stay within about 2 dB across each join. 0.5 s crossfades, 64.2 s, -14 LUFS. Output `~/Downloads/Osupa Ti - 64s Kollosche Cut v3.{mp3,wav}`.

## 2 Nov, Low Again cut (75.3 s)
- Hunter asked for *Low Again* at about 1:10, seamless. ~70 BPM, 161 s; the vocal runs almost unbroken, so the only clean joins are its few breath gaps. `tools/lowagain_cut.py`: beat 18 (16.4 s, intro breath) → beat 102 (88.4 s, a breath inside the big section; chroma 0.91), then beat 151 (130.4 s, where the vocal ends before the outro) → beat 167 (144.1 s, outro gap; 0.99). Both are whole-bar shifts with one-beat equal-power crossfades. The level rises ~4 dB over 2–3 s at the first join; the drop at 58 s is the song's own move into its outro. 75.3 s, -14 LUFS. No 70 s version: no pair of vocal gaps gives one without cutting through a sung line.
- Niche track search (for Kollosche) checked on YouTube by view count: under 1M views: Hayden Calnin "Cut Love" (133k), Miss Grit "Follow the Cyborg" (98k), Gordi "Heaven I Know" (903k), Austra "Beat and the Pulse" (677k), Fyfe "Conversations" (9k).
- **Low Again v3** (Hunter: "make it more seamless"). Two real faults: (1) **join 2 landed half a beat early**, because the crossfade overlapped the outgoing tail instead of extending past the join. A splice must extend the outgoing part by half the crossfade, or the incoming downbeat lands early. (2) The tracked beats jitter by up to ±0.08 s, so splices now use a **fitted fixed grid** (70.0 BPM, linear fit over all beats). Join 1 was rebuilt as a one-bar swell: the intro keeps playing while the big section's own pre-roll bar comes in on the instrumental stem, and the full mix takes over at the breath. Verified: beat phase matches the source in every window, and beat intervals stay even through both joins. 75.3 s, -14 LUFS.
- **Low Again v4 FX** (Hunter: "add tasteful SFX, risers etc, to make it seamless"). `tools/lowagain_fx.py` runs on v3. Join 1 (16.4 s) gets a reverse swell built from the song's own next 2 beats, plus `committed-coaching/sfx-lib/riser_1` low-passed and peaking on the join at -21 dB. Join 2 (58.4 s) gets a 1-beat reverse swell from the outro, plus a 3 s reverb wash of the last beat before the cut, so the energy decays into the outro instead of stepping down. The FX stem sits about 20 LU under the mix. Delivered the mix (-14 LUFS / -3.6 dBTP) and an FX-only stem at the same gain for FCP.
- **Low Again v5** (Hunter: "I want to be able to close my eyes and not know"; the start was weak; wants more SFX). A self-similarity search over every beat pair (chroma × MFCC timbre × band energy, averaged over ±4 beats, whole-bar shifts, vocal gaps only) showed the **intro matches nothing later** (best exit 0.13), while the chorus repeat 96→112 scores 0.55. Lesson: **when a section is unique, don't splice out of it; start the cut at a section that plays like an intro and let the song make its own lifts.** `tools/lowagain_v5.py`: start at beat 56 (49.0 s, the quiet dip after a vocal breath), the song's own lift at 10.3 s, the chorus splice at 34.3 s, the outro splice at 67.7 s. 84.6 s. `tools/lowagain_fx5.py`: riser + 2-beat song swell + sub on the lift, faint swells on the phrase downbeats, a swell + soft whoosh at each splice, and a reverb wash into the outro. The FX stem is about 20 LU under the mix; the mix is -14 LUFS. Beat phase is constant through every splice.
- **Low Again v6** (Hunter on v5: "fuck that's good, just seems too long; some sfx I can't hear"). The vocal stem showed the chorus line is **sung twice** (16-beat shift over beats 117–133 matches 0.94–0.98), so a splice inside a repeated line is invisible even mid-vocal. Splices: 96→112, 129→145, 157→173 (an outro pair scoring 0.54 replaced 151→167 at 0.15). 70.9 s. The FX are about 5 dB louder (stem -30.6 LUFS vs -34.5), and the reverb wash moved to the song's own drop into the outro (54.8 s). Beat phase is constant across all 4 windows. Lesson: **search for repeats on the vocal stem, not just the mix; a repeated lyric lets you cut mid-vocal.**

## 2 Nov, No Bad Vibes cut (69.4 s)
- Hunter wanted something more upbeat than Low Again ("the house isn't that good"): *No Bad Vibes* (Jazzy, KILIMANJARO), 120.0 BPM. The YouTube rip **ends at full level** (no real ending). The song's own arc already fits: intro 0–31.9, build 31.9–47.9, drop at 47.9. So **no splices**: it plays 0 → 63.9 (end of the drop's first 8 bars, a vocal lull), then a **tempo-synced echo-out** (1/4-note ping-pong delay, feedback 0.6, each repeat darker, plus a little reverb) fading over about 4 s. Lesson: **when the song's own first act fits the length, don't splice; design the ending.** Gotcha: a convolution reverb with an unnormalised noise IR is about 190× loud, so scale the wet to the dry peak (a first render spiked +7 dB).
- FX (`tools/nobadvibes_cut.py`): a 4-beat song swell + riser_1 + sub_1 into the drop, faint swells on the 8-bar downbeats (15.9, 31.9, 55.9), a whoosh at the build start, sub_2 under the echo-out. -14 LUFS / -3.9 dBTP. Mix, clean and FX stem delivered.
