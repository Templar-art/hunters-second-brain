# Critique, round 1

| axis | score | basis |
|---|---|---|
| hook | 10.0 | first sound at 0.00s |
| sync | n/a | not judged: no peak-anchored cue could be measured (clicks only, layers on one moment, a crowded neighbour). Check the frames with zoom.py |
| coverage | n/a | not measured (pass --moments) |
| pacing | 10.0 | 3.2 weighted events per 10 s, longest silence 3.9 s |
| variety | 1.0 | 9 source recordings, 9 families in 32 sounds (runs and interface sounds not counted) |
| hierarchy | 10.0 | 18.6 dB between the loud and the quiet sounds |
| headroom | 7.0 | true peak -0.3 dBTP |
| loudness | 10.0 | final -14.7 LUFS (the author's own balance is kept) |
| balance | 10.0 | median event peak -9 dB vs the original around it (whole-track gap +10 LU) |
| mono | 10.0 | the SFX track loses 0.8 dB when folded to mono (0 = the channels agree, 3 = unrelated, 6+ = parts cancel); 0 of 32 sounds lose more than 6 dB; the film loses 0.3 LU in mono against 0.3 LU for the original (+0.0 added) |

**FIX**: lowest axis 1.0 (every axis must reach 8; ok to show)

Three worst problems, fix only these, re-render, run again:
1. variety: freesound_community-birds-19624.mp3 is the source of 12 sounds (0.00s, 3.29s, 5.67s, 6.88s, 13.01s, 17.93s, 29.75s, 38.71s, 49.59s, 51.01s, 53.85s, 59.06s); a slice or a pitch step does not make it another sound
2. variety: 12 takes of the same recording family 'freesound community birds' (0.00s, 3.29s, 5.67s, 6.88s, 13.01s, 17.93s, 29.75s, 38.71s, 49.59s, 51.01s, 53.85s, 59.06s); mix in other sounds
3. variety: traian1984-ambience-wind-blowing-through-trees-01-186986.mp3 is the source of 5 sounds (0.00s, 5.67s, 9.93s, 34.49s, 1:03.27); a slice or a pitch step does not make it another sound

Listen to these 5 moments, on headphones and then once on a phone speaker. This script cannot hear: they are the places where the numbers above are least certain, and none of them says that it sounds good:
  1.    0.00s  'amb aerial opener (W)': the first sound of the film: the hook. Listen for: does it land with the picture at once, and is it clearly there under the music or the voice?
  2.    6.17s  the busiest two seconds (4 sounds); also 'shing flare' at 6.23s: the quietest by perceived loudness among the sounds that are not ticks. Listen for: is every sound still distinct, or does it turn to mud? / can it be heard at all?
  3.   25.25s  'amb patio / pool (N)': a quiet recording lifted by 18 dB; also 'amb patio / pool (PW2)' at 25.25s: the highest peak of the film (-5 dBFS before the master). Listen for: does its noise floor come up with it (hiss)? / is it big without hurting on headphones, and does the music under it pump?
  4.   34.49s  'amb aerials (W)': sits 9 dB under its plan (a very quiet recording lifted to the +18 dB cap). Listen for: is it big enough for its picture?
  5.   48.63s  'amb curtain window (CUR)': its peak sits -46 ms from the moment. Listen for: does it feel early or late against the picture?
  (--listen-out FILE.wav cuts them into one file of the film's own sound)

Still to judge by eye on review.png: character fit (each sound suits its picture), cleanliness (no mud in the low end under music/voice, nothing masks speech), taste (designed, not sprayed on).