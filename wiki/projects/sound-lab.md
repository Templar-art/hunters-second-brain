---
type: project
tags: [audio, sfx, tools, editing]
status: built-unproven
updated: 2026-10-20
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
**v1 (19 Oct):**
1. **Delivery spec by default:** 48 kHz, 24-bit, stereo WAV. The Code tab is gone and the dialog opens on Audio. MP3 and OGG are still available.
2. **Project naming:** every export becomes `PROJECT_category_sound.wav`, for example `CC-EP04_whooshes_whip.wav`.
3. **Kit batch export:** press K to add a sound as tuned, then export everything as one zip with `sfx-list.csv`.
4. **Picture sync:** press P and drop in a clip (it stays local). It shows SMPTE timecode at 23.976, 25, 29.97 DF or 50 fps. M cues the current sound at the playhead, aligned by Start or by Peak. Cues play against the picture. **Stem** exports one WAV the length of the clip.
5. Opens on the Video library.

**v2 (20 Oct):**
6. **Layering (Stack):** press S to add the current sound as a layer, then set each layer's offset (−2 to +12 s) and gain. Play the stack, send it to the kit, or save it as a preset. A riser into an impact with a sub underneath is one item. This is the main fix for single synth sounds sounding thin.
7. **Loudness:** Level is Off, Peak −1, or **LUFS** (−14, −18 or −23). LUFS uses ITU BS.1770 gating and never pushes the peak past −1 dBFS, so if hitting the target would breach that ceiling, the file lands quieter instead. It was checked against ffmpeg `ebur128`: −21.07 vs −21.1, −25.09 vs −25.1, and an exported WAV measured −18.0 LUFS.
8. **Final Cut XML:** in picture mode, **FCP XML** writes each cue as its own WAV plus an `.fcpxml` (v1.11, which DaVinci Resolve also reads). The XML holds one project with a gap the length of the clip and every SFX connected underneath it, on the *effects* role. Each WAV is padded so its clip sits on a whole frame and still lands sample-accurate. The XML points to absolute paths, so the **FCP path** field in Project has to match where the folder ends up. The default is `~/Downloads`, which is where the zip unpacks. The XML validates against FCP 12.4's own `FCPXMLv1_11.dtd`.
9. **Presets:** save a tuned sound or a stack under a name (e.g. "10x whoosh soft"), click it to recall, or send it to the kit. Presets can be exported and imported as JSON, so a house set can live in the vault.
10. **Takes:** export 1, 3 or 5 takes of each kit item, each slightly varied in pitch, tone and length (`_01`, `_01-2`, `_01-3`), so repeated pops don't sound machine-gunned.
11. **Trim effect** (in the Effects menu): fade in, fade out, reverse, and cut the silent tail. It's applied after the engine, so preview, exports, stacks and cues all hear it.
12. **Editor transport in picture mode:** Space or K plays and pauses, L plays (press again for 2× and 4×), J jumps back 1 s, ←/→ or , and . step one frame, and Shift+arrow moves 1 s. HTML video can't play in reverse, so J is a jump rather than a true reverse shuttle.
13. **Find cuts:** scans the clip in the browser (luma-histogram spikes, refined to the exact frame) and lists every hard cut. **Cue on all** drops the current sound peak-aligned on every cut, and skips cuts that already have one.
14. **Save to folder:** Project → *Save to* → Choose… writes exports straight into a folder, such as a job folder or `sfx-lib/`, instead of Downloads. Kits go into a `PROJECT_sfx-kit/` subfolder unzipped. This needs Chrome, Edge or Arc; Safari doesn't support it and falls back to Downloads.

Keys: Space plays, the arrow keys move through sounds, E exports, L loops, K adds to the kit, S adds a layer, P toggles picture mode, M places a cue. In picture mode the transport keys take over.

## Verified (browser preview)
- **19 Oct:** the kit zip passes `unzip -t`. WAVs are PCM 48k/24 stereo. The stem is the clip's length. A Start cue landed 1 ms off, and a whip lined up by its peak landed inside one frame.
- **20 Oct:**
  - Cut detection found 00:00:01:13, 03:05 and 04:20 on a test clip built with cuts at 1.52, 3.20 and 4.80 s, all frame-exact.
  - The FCP XML is DTD-valid. A whip's peak landed exactly on its frame. The thunder's peak (a noisy rumble) landed within 15 ms, under half a frame, once peak detection switched to a 10 ms loudness envelope.
  - The kit export with 3 takes and LUFS −18 gave 9 WAVs, all at −18.0.
  - Transport keys don't clash with the kit and sound-navigation shortcuts.
  - Save-to-folder was tested against the browser's private filesystem. The real OS folder picker needs a click from Hunter.
- **Not yet tested:** whether the sounds hold up in a real edit, and importing the FCP XML into Final Cut itself.

## Feeding the motion engine
The motion engine's curated `projects/committed-coaching/sfx-lib/<kind>_N.wav` is also 48 kHz stereo. A Sound Lab kit WAV can go straight in (ffmpeg converts 24-bit to s16 if needed). See [[sfx-library]].

Research prompts for better SFX sources and FCP plugins: [projects/fcp-plugin-research/perplexity-prompts.md](../../projects/fcp-plugin-research/perplexity-prompts.md) → [[fcp-plugin-research]].

Related: [[sfx-library]] · [[fcp-plugin-research]] · [[motion-and-stills-tools]] · [[use-definitions-series]] · [[audio-for-video]]
