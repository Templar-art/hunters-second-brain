# Critique, round 1

| axis | score | basis |
|---|---|---|
| hook | 10.0 | first sound at 0.00s |
| sync | n/a | not judged: no peak-anchored cue could be measured (clicks only, layers on one moment, a crowded neighbour). Check the frames with zoom.py |
| coverage | n/a | not measured (pass --moments) |
| pacing | 7.2 | 4.7 weighted events per 10 s, longest silence 9.0 s |
| variety | 1.0 | 10 source recordings, 10 families in 44 sounds (runs and interface sounds not counted) |
| hierarchy | 10.0 | 18.6 dB between the loud and the quiet sounds |
| headroom | 10.0 | true peak -1.8 dBTP |
| loudness | 10.0 | final -13.9 LUFS (the author's own balance is kept) |
| balance | 10.0 | median event peak -10 dB vs the original around it, big sounds -6 dB (whole-track gap +13 LU) |
| mono | 10.0 | the SFX track loses 0.9 dB when folded to mono (0 = the channels agree, 3 = unrelated, 6+ = parts cancel); 0 of 44 sounds lose more than 6 dB; the film loses 0.1 LU in mono against 0.1 LU for the original (+0.0 added) |

**FIX**: lowest axis 1.0 (every axis must reach 8; ok to show)

Three worst problems, fix only these, re-render, run again:
1. variety: freesound_community-birds-19624.mp3 is the source of 19 sounds (1.21s, 2.67s, 7.01s, 8.47s, 9.93s, 11.85s, 13.31s, 16.68s, 31.70s, 33.12s, 34.58s, 36.12s, 38.04s, 39.41s, 43.29s, 44.25s, 46.21s, 47.13s, 55.97s); a slice or a pitch step does not make it another sound
2. variety: 19 takes of the same recording family 'freesound community birds' (1.21s, 2.67s, 7.01s, 8.47s, 9.93s, 11.85s, 13.31s, 16.68s, 31.70s, 33.12s, 34.58s, 36.12s, 38.04s, 39.41s, 43.29s, 44.25s, 46.21s, 47.13s, 55.97s); mix in other sounds
3. variety: traian1984-ambience-wind-blowing-through-trees-01-186986.mp3 is the source of 12 sounds (0.00s, 1.21s, 2.67s, 5.55s, 9.93s, 14.26s, 33.12s, 34.58s, 36.12s, 43.29s, 55.97s, 59.73s); a slice or a pitch step does not make it another sound

Listen to these 5 moments, on headphones and then once on a phone speaker. This script cannot hear: they are the places where the numbers above are least certain, and none of them says that it sounds good:
  1.    0.00s  'amb beach aerial (WV)': the first sound of the film: the hook. Listen for: does it land with the picture at once, and is it clearly there under the music or the voice?
  2.   14.26s  'amb twilight front (W)': a quiet recording lifted by 18 dB; sits 7 dB under its plan (a very quiet recording lifted to the +18 dB cap). Listen for: does its noise floor come up with it (hiss)? / is it big enough for its picture?
  3.   31.70s  'amb balcony woman (B)': the highest peak of the film (-6 dBFS before the master); its peak sits -47 ms from the moment. Listen for: is it big without hurting on headphones, and does the music under it pump? / does it feel early or late against the picture?
  4.   33.62s  the busiest two seconds (5 sounds). Listen for: is every sound still distinct, or does it turn to mud?
  5.   39.41s  'amb pool ext (PW)': its peak sits +119 ms from the moment; also 'flare sunburst' at 38.75s: the quietest by perceived loudness among the sounds that are not ticks. Listen for: does it feel early or late against the picture? / can it be heard at all?
  (--listen-out FILE.wav cuts them into one file of the film's own sound)

Still to judge by eye on review.png: character fit (each sound suits its picture), cleanliness (no mud in the low end under music/voice, nothing masks speech), taste (designed, not sprayed on).