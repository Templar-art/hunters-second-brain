---
client: kollosche
address: Kollosche Day to Night townhouse (agent Eddie Wardale)
opened: 2026-10-27
status: intake
cost: { credits: 0, hf_credits: 0, aud: 0 }
---

# Job: Kollosche reels, Day to Night townhouse

Two 9:16 reels for the townhouse that the drone graphics job covered ([[kollosche]]).

## Shots

| # | Reel | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 1 | Flythrough | edit (FCP) | todo | Fast-paced with a drop. Track pick: Fred again.. & Swedish House Mafia, "Turn On The Lights again..". Drop on the cut out of the K, about 3 s in. |
| 2 | Cinematic | edit (FCP) | delivered (full sound) | Slow build. ⚠️ Track changed 2026-10-29 to JMSN, "Love Me" (was RÜFÜS DU SOL, "Innerbloom"). |

## Kit (`kit/`)

- `01-K-open-1080x1920.png`: the K overlay. Full frame at 100%, on from frame 1, holds 2–4 s, then fades. No address super: Kollosche's recent reels open on the K only.
- `02-outro-eddie-wardale-9x16.mov`: ProRes 4444 alpha. The 50% navy overlay and EDDIE WARDALE / 0408 881 678 fade in together over 0.6 s, then hold for 4 s. Lay it over the last shot. The PNG is the static version.

## Log

- 2026-10-27 intake: two reels. Kit assembled from the brand pack and the outro generator.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->

---
_Vault: [[jarvis]]_
- 2026-10-29 music: cut "Love Me" (JMSN) to 33.6 s for the cinematic reel. The song is 80.7 BPM with 2.97 s bars. The cut takes the intro from 0:00 to the bar-7 downbeat at 21.69 s, then the chorus bars 39–42 from 117.08 to 129.01 s, ending on the breath before the next chorus with a 1.8 s fade. The join is a one-bar overlap; the harmony matches (chroma 0.98), and the beat stays steady across it. The master is at −14 LUFS. Built with `projects/auto-sound-design/tools/reel_cut.py` and delivered to Desktop `Kollosche - Love Me cinematic cut`. Not yet heard by Hunter.
- 2026-10-29 music FX: Hunter likes the Love Me cut and asked for quick flicker and beat FX to edit to. `tools/loveme_fx.py` builds four beat-locked stems:
  - shutter and flash flickers
  - synthesised glitch flickers
  - stutter rolls cut from the song itself
  - a riser plus glimmer hit into the 21.69 s drop

  It also makes 9 one-shots, a beat map, and `Love Me - FX version (mastered).wav` (−14 LUFS) with all four baked in. Delivered to Desktop `Kollosche - Love Me cinematic cut`. Not yet heard by Hunter.
- 2026-10-29 music FX v2: Hunter didn't like the glitch things, so they're out completely, with no synthesised crush or buzz anywhere. In their place are reverse swells made from the song's own next downbeat, reversed and smeared, landing on the bass-in bar and each chorus bar. The only stutter left is the one into the drop; the last-bar stutter is gone. The FX version is re-mastered to −14 LUFS and the Desktop folder is updated.
- 2026-10-29 SFX pass on Hunter's edit (`Downloads/Kollosche Ester Place/Cinematic Reel.mp4`, 33.62 s). The edit carried the Love Me FX version at 0:00, whose bar shutters would double up with cut clicks, so the delivery swaps in SONG-only plus swells/riser.
  - Shutter clicks sit on 7 picture cuts (14.18, 15.64, 17.14, 18.64, 23.19, 24.65, 26.86 s).
  - Hunter's own click on the multi-photo flash (12.18–12.68) is kept, and nothing else is placed there.
  - Whooshes on 3.96 (street → inside) and 29.11 (inside → aerial); ambience only on the outside shots.
  - Scene map `scene-maps/kollosche-cinematic-reel.json`. Full preview at −14.6 LUFS.
  - Delivered to Desktop `Kollosche - Love Me cinematic cut/SFX pass (your edit)`. Not yet heard by Hunter.
- 2026-10-29 aerial and day-to-night SFX, built with `projects/auto-sound-design/tools/kollosche_aerial_d2n.py`:
  - Track 6, aerials: high-passed altitude air with a slow stereo drift on 0–1.04 and 29.11–end, a distant city bed under the skyline, and a soft air sweep on the 30.61 cut.
  - Track 7, day to night: the window shot 19.39–21.77. Birds through the glass fade out, crickets fade in as the sky turns, and a low "Time and Space" rise ends on the 21.77 drop cut.

  The preview is re-rendered with all 7 layers at −14.6 LUFS. Not yet heard by Hunter.
- 2026-10-29 photo burst: Hunter's own click on the multi-photo flash dropped out once the audio was rebuilt from separate tracks, so the burst is rebuilt inside track 3. There's a shutter on each photo cut (12.18, 12.30, 12.39, 12.51), stepping up in level, and a softer click on the return at 12.68. Hunter liked the aerial and day-to-night tracks ("its good").
- 2026-10-29 delivered: Hunter approved ("yeah it good do the full thing"). All 7 tracks are summed and mastered to −14 LUFS, −1 dBTP, as `0 FULL MIX` plus `FINAL - Kollosche cinematic reel (full sound).mp4`. That's his 720×1280 picture copied untouched with the new audio, 33.62 s, in Desktop `Kollosche - Love Me cinematic cut/SFX pass (your edit)`.
