---
type: concept
tags: [audio, sfx, motion-graphics, assets]
updated: 2026-10-21
---
# SFX library (Ocular Sounds)

Hunter's licensed sound library, filed 10 Oct 2026 from ~/Downloads.

- **Location:** `~/Music/SFX Library/Ocular Sounds/<Library>/<CatID>/` (9 GB, outside the vault so it stays out of git).
- **Catalog:** `~/Music/SFX Library/Ocular Sounds/catalog.csv` lists path, library, category, title, duration, key and description for every sound. ⚠️ It held 192 sounds on 10 Oct; it was rebuilt on 20 Oct at **1,547 sounds** after eight more packs were added (Forged, Velocity, Shift, Mechanica, Utility, Cityscapes Vol 1, The Provence, full Aperture). See [[sfx-sorter]]. Each library's metadata CSV, asset list and thumbnail are in its `_docs/` folder.
- **Libraries:**
  - **Foundation:** designed impacts, booms, whooshes, whoosh-into-hits and risers. This is the motion-graphics workhorse.
  - **Pendulum:** 120 bpm percussion, synth and rhythm loops. These could serve as free music beds.
  - **Aperture:** designed camera shutter sequences.
  - **Rainforest:** long ambience and rain loops.
- 146 byte-identical " (1)" duplicate downloads went to the Trash, not deleted.

## How the motion engine uses it
`projects/committed-coaching/sfx-lib/` holds curated 48k stereo trims, named `<kind>_N.wav`:

| Kind | Sounds |
|---|---|
| thud | Clean Rumble, Not What You Think, Gut Feeling, Last Time |
| boom | Groundbreaking, Dont Give In, Quake |
| whoosh | Speed is Everything, Passed By, Weight, Turn of Events |
| hit (whoosh into impact, landing on the cue) | Quick and Dirty, Come and Get Me |
| riser | No Time Left, Metallic Tension |

`tools/sfx.py` now keeps samples in stereo, uses barely any reverb on them, and applies only gentle saturation. The old Magnific/ElevenLabs takes are in `sfx-lib/_magnific/`, and only their click and pop sounds are still used.

To add a sound, trim it from the library into `sfx-lib/<kind>_N.wav`. The trim script is in the 10 Oct session; it uses ffmpeg with `-t <keep> -af afade=out -ar 48000 -ac 2 -sample_fmt s16`.

For custom synthesised SFX (UI pops, accents, glitches, title stingers) that aren't in Ocular, use [[sound-lab]]. Its kit WAVs are 48k stereo and go straight into `sfx-lib/`.

Buying more SFX, licences, and how to make them sound expensive: [[sfx-sourcing-and-design]].

Related: [[use-definitions-series]] · [[sound-lab]] · [[sfx-sourcing-and-design]]

## Lifting SFX from reference reels (27 Oct 2026)
Demucs is installed free in `~/.venvs/demucs` (`demucs -n htdemucs -d mps`, about 4 s per 110 s track on MPS). **Caveat:** it splits stems by *instrument*. It has no music-versus-SFX stem, so whooshes and hits get smeared across `vocals` and `other`. A sung vocal also dirties `vocals`. The working method is to find the cuts with ffmpeg scene detect, take transient peaks in vocals+other within 0.6 s of each cut, and trim from 0.5 s before to 1.5 s after with fades and normalise. First run: a Surfers canal-home reel ("The Pilot 17") gave 32 candidates in `~/Music/SFX Library/_Incoming/snapgram-upn69xj4gyxs/hits/`. Audition them; expect some music bleed. Reference-only, because a third-party reel's audio is not licensed for client work.
