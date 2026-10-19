---
type: project
tags: [audio, sfx, tools, editing]
status: built-unproven
updated: 2026-10-19
---

# Sound Lab (local, 10x fork)

A local copy of the React Bits **Sound Lab** ([reactbits.dev/tools/sound-lab](https://reactbits.dev/tools/sound-lab)), with changes for cutting video. It lives in [projects/sound-lab](../../projects/sound-lab/). It was built on 19 Oct 2026 because Hunter wanted custom SFX for his edits.

## What it is
Sound Lab is a browser tool with 200 sounds: 100 **Interface** sounds (taps, toggles, notifications) and 100 **Video** sounds (risers, impacts, whooshes, transitions, accents, drops, glitches, ambience, titles, pops, stingers, tension). Each sound can be tuned for pitch, tone, length, space and punch, and can take reverb, echo, filter, chorus and lo-fi effects. Almost every sound is **synthesised from a Web Audio recipe**; only the keycap sounds use recorded samples. Rendering is free and happens on this Mac, with no credits and no network.

⚠️ Because the sounds are synthesised, the [[motion-and-stills-tools]] verdict ("synth SFX judged poor") still applies to big cinematic hits until it's tested in a real edit. Sound Lab is much better designed than that numpy test, and it should be strong for **UI pops, clicks, accents, glitches and title stingers**. For heavy booms and whoosh-into-hits, the [[sfx-library]] (Ocular Sounds) is still the first choice.

## Source and licence
- Upstream source: `DavidHDev/react-bits`, `src/tools/sound-lab/` plus the engine `src/sounds/ts/react-bits-sound.ts`, at commit `e12c221`. It's pulled out of the docs site into a standalone Vite + React 19 app.
- Licence: **MIT + Commons Clause** (copy at `projects/sound-lab/LICENSE-react-bits.md`). Exported audio can be used in any personal or commercial project, including client videos. The tool itself, and packs of its sounds, **can't be sold, redistributed or hosted**, so the fork stays in this private vault and the exports are never sold as an SFX pack.

## Run it
The launch config is `sound-lab` in `.claude/launch.json`, on port 8160. Or run:
```
cd projects/sound-lab && npm install && npm run dev
```
Then open http://localhost:8160. `node_modules/`, `dist/`, `*.wav` and `*.mp4` are git-ignored.

## What the 10x fork adds
1. **Delivery spec by default:** 48 kHz, 24-bit, stereo WAV. The old Code tab is gone, and the dialog opens on Audio. MP3 and OGG are still available.
2. **Project naming:** in Tune → Project, set a name and every export becomes `PROJECT_category_sound.wav` (for example `CC-EP04_whooshes_whip.wav`). Files then sort by job and by SFX family in the bin.
3. **Normalise to −1 dBFS peak** (on by default). This gives consistent levels across the kit and leaves broadcast-safe headroom.
4. **Kit batch export:** tune a sound and press **K** to add it with its settings, then repeat. **Export kit** renders every sound to a numbered WAV (`PROJECT_category_sound_01.wav`), adds `sfx-list.csv` (file, sound, category, length, tune settings) and downloads one zip.
5. **Picture sync:** press **P** (or click **Picture**) and drop a clip in. The clip stays local and is never uploaded. It shows SMPTE timecode at 23.976, 25, 29.97 DF or 50 fps (default 25 for Australia). Press **M** to cue the current sound at the playhead, aligned by its **Start** or its **Peak**. Peak alignment moves a riser or whoosh so that its loudest moment lands on the cut. Cues fire during playback, so you hear the SFX against the picture. **Stem** exports one WAV the length of the clip with every cue in place: drop it at the first frame of the clip in Premiere or Resolve and it lines up.
6. The default view is the Video library, starting on Swoop.

Keys: Space plays, arrow keys move through sounds, E exports, L loops, K adds to the kit, P toggles picture mode, M places a cue.

## Verified (19 Oct, browser preview)
- The kit zip passes `unzip -t`. Each WAV is PCM, 48000 Hz, 24-bit, stereo, with a −1.00 dBFS peak.
- The 6 s stem is 6.000 s long. A Start cue at 00:00:02:00 sounds at 2.001 s. A Peak-aligned whip at 00:00:04:00 peaks at 3.99 s, inside one frame.
- Cues trigger during playback, and the timecode readout matches the clip's burnt-in counter.
- Not yet tested: whether the sounds hold up in a real edit. That's the open question.

## Feeding the motion engine
The motion engine's curated `projects/committed-coaching/sfx-lib/<kind>_N.wav` is also 48 kHz stereo. A Sound Lab kit WAV can go straight in (ffmpeg converts 24-bit to s16 if needed). See [[sfx-library]].

Related: [[sfx-library]] · [[motion-and-stills-tools]] · [[use-definitions-series]] · [[audio-for-video]]
