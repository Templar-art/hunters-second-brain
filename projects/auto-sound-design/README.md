# Auto Sound Design

A first-pass sound-design layer for a finished real-estate edit. You give it a video (with its music), a folder of sound effects you own, and nothing else: no timestamps, no markers. It returns:

- **a preview video**: your picture, untouched, with the music plus the effects
- **an effects-only WAV**, the full length of the video, to drop under the edit at 0:00
- **a Final Cut XML** (`.fcpxml`): a new project where every effect is its own clip you can move, mute or swap
- **`edit_decisions.json` + `REPORT.md`**: every effect's time, file, level, the reason it was placed, and a confidence score

It runs entirely on your Mac. Nothing is uploaded, nothing is bought and nothing is downloaded.

## What it actually knows (and doesn't)

- It finds **hard cuts** in the picture and **loud moments, onsets and big energy rises** in the music. Placements are rules built on those signals, and every one is labelled *heuristic*.
- It **does not know what a shot shows**. It can't tell a drone shot from a kitchen, a sun flare from a cut, or a room reveal or twilight from anything else. No visual-analysis component exists yet.
- **Dissolves and slow fades are mostly missed** by the cut detector.
- Sound categories (whoosh, riser, impact, low drone, shimmer, ambience) are **guessed from file and folder names**, sidecar tags and `catalog.csv`. It doesn't listen to the sounds to decide what they are. It does measure each file's peak and attack so it can line the sound up with the cut.
- There is **no dialogue detection**, so it never ducks anything.

## One-time setup (Mac)

1. Open **Terminal** (Cmd+Space, type Terminal, press Enter).
2. Go to this folder. In Terminal, type `cd ` (with a space), drag the `auto-sound-design` folder from Finder onto the Terminal window, then press Enter.
3. Run:
   ```
   ./setup.sh
   ```
   It checks for Python and FFmpeg, and **asks before installing anything**. You need FFmpeg (installed via [Homebrew](https://brew.sh): `brew install ffmpeg`), numpy and lxml. The last two go into a private `.venv` folder here, not into your system Python.
4. Optional: save your SFX folder so you don't have to type it every time. Create a file called `asd.local.json` in this folder containing:
   ```json
   { "sfx_folder": "/Users/hunter/Music/SFX Library/Ocular Sounds" }
   ```

## Process a video: the one command

Run a short test section first and review it. For example, 27 seconds starting at 16.7 s:
```
./run.sh "/path/to/My Listing Video.mp4" --start 16.7 --test-seconds 27
```
The section starts on the nearest keyframe at or before `--start`, so the picture is copied untouched. The main output is a **playable video with the finished mix**, named `…_SOUND-MIX.mp4`.
Then run the whole video:
```
./run.sh "/path/to/My Listing Video.mp4"
```
If you haven't saved the folder in `asd.local.json`, add `--sfx "/path/to/SFX folder"`. Tip: drag a file or folder onto Terminal to paste its path. Spaces, brackets and apostrophes in paths are fine.

Results go to `output/<video name>_<date-time>/`. Open `REPORT.md` first.

Other options:
- `--seed 3` picks different sound files with the same placements. The same seed always gives the same result.
- `--music "/path/to/track.wav"` analyses a clean music file instead of the video's audio (for analysis only; it isn't added to the mix).
- `--config my.json` overrides any setting from `config.default.json` (density, spacing, levels, fades).
- `--no-xml` skips the Final Cut file.

To search the library manifest:
```
.venv/bin/python sounddesign.py manifest --sfx "/path/to/SFX" --search "whoosh"
```

## Final Cut Pro import (⚠️ not yet confirmed)

The XML is **FCPXML 1.10**, the version on Apple's developer documentation page, checked October 2026. Every test run validates it against that DTD, but **it hasn't been imported into Final Cut yet**, so don't treat it as Final Cut-compatible until that works. To try it safely:

1. In Final Cut: **File → New → Library…** and name it something like `ASD Test`. This keeps your real libraries untouched.
2. With that library selected: **File → Import → XML…** and choose the `.fcpxml` from the output folder.
3. You should get an event called **Auto Sound Design** with a project holding your video and each effect connected underneath it (role: Effects). Media is referenced in place; nothing is copied.
4. Tell Claude what happened. If Final Cut complains about a specific element, the most likely culprit is the volume fades: set `"fcpxml": {"write_fades": false}` in `asd.local.json` and re-run.

If the XML won't import, the **effects-only WAV** still works: drag it under the edit at 0:00.

Each run folder includes `sfx_used/`, a copy of every effect the XML uses, so the folder can be moved as a whole. After moving it (for example from a cloud session to the Mac), relink it:
```
.venv/bin/python sounddesign.py relink "output/<run folder>" --video "/path/to/the video on this Mac.mp4"
```
That writes `…_relinked.fcpxml` pointing at the new locations. Import that one.

## Tested where

| | Cloud session (Linux) | Needs the Mac |
|---|---|---|
| Cut and music analysis, placement, mixing | ✅ tested (37 tests + real 10x videos) | – |
| Playable mixed video, picture untouched | ✅ frame-by-frame identical to the source | play it in QuickTime |
| FCPXML validity | ✅ against Apple's 1.10 DTD | ❌ **actual Final Cut import untested** |
| `relink` to Mac paths | ✅ logic tested | run it on the Mac |
| `setup.sh` (Homebrew, venv) | ❌ written for macOS, not run | run once |
| Full Ocular library (1,547 sounds) | ❌ not in the cloud | first index is slow, then cached |

## How placement works (defaults in `config.default.json`)

- **Impact** on big music energy rises (a drop or section change), snapped to a nearby cut. A **riser** peaks into it when the rise is large.
- **Whoosh**, peaking on a hard cut, only when the cut also lands on a music onset or beat. It's capped at about a third of cuts and 4 per minute: not on every cut.
- **Ambience bed** under the opening seconds, faded in and out. This is generic texture; it doesn't know the scene.
- **Shimmer** on the last cut in the final 20%. It assumes that's an end card, which isn't checked.
- Rules: 3 s minimum spacing between one-shots, at most 8 one-shots per minute, at most 2 sounding at once, 1 bed, no repeated file back to back.
- **Levels** are set relative to the music's loudness at that moment, then capped by a per-category peak ceiling. A clipping check turns down only the effects that push the mix over -1 dBFS, by at most 3 dB each. If the music itself is mastered hot, the *preview* is turned down overall and the report says so. Your source files are never modified.
- Folders starting with `_` (such as `_docs`, `_Archives` or `_magnific`) are skipped when indexing.

## Scene ambience and accents (scene maps)

The tool can't see. A **scene map** is a small JSON file saying what each stretch of the video shows. A person writes it, or Claude writes it after looking at one frame per shot. With one, the tool:
- lays an **ambience bed per scene**: birds and breeze on exteriors, wind on aerials, crickets at dusk, quiet room tone inside. The beds crossfade at the joins, and each starts at a different point in the file;
- keeps **presenter** shots clear of one-shot effects, since someone is probably talking;
- places **accents** listed in the map, such as a glint on a sun flare or on a location pin landing.

```
.venv/bin/python sounddesign.py synth      # free synthetic ambience + shimmer kit -> sfx/generated/
./run.sh "video.mp4" --sfx "/path/to/Ocular Sounds" --sfx sfx/generated \
    --config presets/tasteful.json --scenes scene-maps/kollosche-5-esther-pl-main.json
```
Labels: `exterior, balcony, aerial, dusk, interior, bathroom, presenter, endcard`. The example map is `scene-maps/kollosche-5-esther-pl-main.json`. The synthetic kit is a stand-in; recorded ambience (e.g. Ocular Rainforest/Cityscapes) tagged `ambience, outdoor` (or `aerial`, `dusk`, `interior`) in a `.tags` sidecar will be used the same way.

Presets: `presets/tasteful.json` (Hunter's pick, 28 Oct) and `presets/dense.json` ("jam-packed", judged over the top).

## Missing sounds

When a category has no files, the report says so. Nothing is downloaded or generated. Add files with the word in the name (`soft_shimmer_01.wav`), or give an existing file a sidecar called `name.wav.tags` containing `shimmer, glass`.

`asd/providers.py` is the hook for a future sound-generation service. It is **off by default**, has no real provider wired in (and no Soundbot integration), reads keys only from environment variables, and has to ask for a typed `yes` before any paid request or upload.

## Tests

```
.venv/bin/python -m unittest discover -s tests -v
```
37 tests cover rational frame timing (including 29.97 drop-frame), effect bounds, overlap and spacing rules, reproducibility, missing files and folders, manifest tagging, DTD validation, the clipping check, and a full end-to-end run on generated media with known cuts.
