# Critique, round 1

| axis | score | basis |
|---|---|---|
| hook | 10.0 | first sound at 0.00s |
| sync | 10.0 | 5/5 sounds on their frame (peaks, arrivals, or first onsets for clicks) |
| coverage | n/a | not measured (pass --moments) |
| pacing | 2.1 | 1.0 weighted events per 10 s, longest silence 27.5 s |
| variety | 7.4 | 7 source recordings, 4 families in 7 sounds (runs and interface sounds not counted) |
| hierarchy | 10.0 | 21.2 dB between the loud and the quiet sounds |
| headroom | 10.0 | true peak -3.7 dBTP |
| loudness | 10.0 | final -15.0 LUFS (the author's own balance is kept) |
| balance | 7.0 | median event peak -11 dB vs the original around it, big sounds -11 dB (whole-track gap +15 LU) |
| mono | 10.0 | the SFX track loses 0.7 dB when folded to mono (0 = the channels agree, 3 = unrelated, 6+ = parts cancel); 0 of 7 sounds lose more than 6 dB; the film loses 0.3 LU in mono against 0.3 LU for the original (+0.0 added) |

**FIX**: lowest axis 2.1 (every axis must reach 8; ok to show)

Three worst problems, fix only these, re-render, run again:
1. pacing: nothing happens between 34.74s and 1:02.19 (27.5 s)
2. variety: 4 takes of the same recording family 'dsgnmisc designed race sequence whoosh stem focus ocular velocity' (3.54s, 8.09s, 27.65s, 1:03.52); mix in other sounds
3. balance: median sound is -11 dB under the original, weakest at 0.00s, 34.74s: raise gain_db there (sheet.py gain --db +N --between A B) and render with --no-match-layer: the layer match keeps the whole layer at the loudness of the sound it replaces and takes back a raise that is made on every cue

Listen to these 3 moments, on headphones and then once on a phone speaker. This script cannot hear: they are the places where the numbers above are least certain, and none of them says that it sounds good:
  1.    0.00s  'birds bed (opening exter': the first sound of the film: the hook. Listen for: does it land with the picture at once, and is it clearly there under the music or the voice?
  2.    3.54s  'whoosh curtain reveal': the highest peak of the film (-13 dBFS before the master). Listen for: is it big without hurting on headphones, and does the music under it pump?
  3.    8.09s  'whoosh garden push': the quietest by perceived loudness among the sounds that are not ticks. Listen for: can it be heard at all?
  (--listen-out FILE.wav cuts them into one file of the film's own sound)

Still to judge by eye on review.png: character fit (each sound suits its picture), cleanliness (no mud in the low end under music/voice, nothing masks speech), taste (designed, not sprayed on).

---

# Critique, round 2

| axis | score | basis |
|---|---|---|
| hook | 10.0 | first sound at 0.00s |
| sync | 10.0 | 6/6 sounds on their frame (peaks, arrivals, or first onsets for clicks) |
| coverage | n/a | not measured (pass --moments) |
| pacing | 2.1 | 1.0 weighted events per 10 s, longest silence 27.5 s |
| variety | 10.0 | 7 source recordings, 6 families in 7 sounds (runs and interface sounds not counted) |
| hierarchy | 10.0 | 24.9 dB between the loud and the quiet sounds |
| headroom | 10.0 | true peak -3.9 dBTP |
| loudness | 10.0 | final -15.0 LUFS (the author's own balance is kept) |
| balance | 10.0 | median event peak -6 dB vs the original around it, big sounds -6 dB (whole-track gap +13 LU) |
| mono | 10.0 | the SFX track loses 1.0 dB when folded to mono (0 = the channels agree, 3 = unrelated, 6+ = parts cancel); 0 of 7 sounds lose more than 6 dB; the film loses 0.3 LU in mono against 0.3 LU for the original (+0.0 added) |

**FIX**: lowest axis 2.1 (every axis must reach 8; ok to show)

Three worst problems, fix only these, re-render, run again:
1. pacing: nothing happens between 34.74s and 1:02.19 (27.5 s)

Listen to these 3 moments, on headphones and then once on a phone speaker. This script cannot hear: they are the places where the numbers above are least certain, and none of them says that it sounds good:
  1.    0.00s  'birds bed (opening exter': the first sound of the film: the hook. Listen for: does it land with the picture at once, and is it clearly there under the music or the voice?
  2.    3.54s  'whoosh curtain reveal': the highest peak of the film (-10 dBFS before the master). Listen for: is it big without hurting on headphones, and does the music under it pump?
  3.    6.23s  'shing flare': the quietest by perceived loudness among the sounds that are not ticks. Listen for: can it be heard at all?
  (--listen-out FILE.wav cuts them into one file of the film's own sound)

Still to judge by eye on review.png: character fit (each sound suits its picture), cleanliness (no mud in the low end under music/voice, nothing masks speech), taste (designed, not sprayed on).

---

# Critique, round 3

| axis | score | basis |
|---|---|---|
| hook | 10.0 | first sound at 0.00s |
| sync | 4.9 | 3/7 sounds on their frame (peaks, arrivals, or first onsets for clicks) |
| coverage | n/a | not measured (pass --moments) |
| pacing | 4.8 | 2.1 weighted events per 10 s, longest silence 9.7 s |
| variety | 1.0 | 10 source recordings, 9 families in 18 sounds (runs and interface sounds not counted) |
| hierarchy | 10.0 | 18.0 dB between the loud and the quiet sounds |
| headroom | 10.0 | true peak -3.8 dBTP |
| loudness | 10.0 | final -15.0 LUFS (the author's own balance is kept) |
| balance | 10.0 | median event peak -8 dB vs the original around it, big sounds -6 dB (whole-track gap +14 LU) |
| mono | 10.0 | the SFX track loses 0.8 dB when folded to mono (0 = the channels agree, 3 = unrelated, 6+ = parts cancel); 0 of 18 sounds lose more than 6 dB; the film loses 0.4 LU in mono against 0.3 LU for the original (+0.1 added) |

**FIX**: lowest axis 1.0 (every axis must reach 8; ok to show)

Three worst problems, fix only these, re-render, run again:
1. sync: 'amb pool deck (PW2)' at 27.30s peaks +129 ms from the moment
2. sync: 'amb pool deck (N)' at 27.30s peaks +129 ms from the moment
3. pacing: nothing happens between 12.10s and 21.80s (9.7 s)

Listen to these 5 moments, on headphones and then once on a phone speaker. This script cannot hear: they are the places where the numbers above are least certain, and none of them says that it sounds good:
  1.    0.00s  'amb aerial (W)': the first sound of the film: the hook. Listen for: does it land with the picture at once, and is it clearly there under the music or the voice?
  2.    2.80s  the busiest two seconds (4 sounds). Listen for: is every sound still distinct, or does it turn to mud?
  3.   27.30s  'amb pool deck (PW2)': its peak sits +129 ms from the moment. Listen for: does it feel early or late against the picture?
  4.   34.40s  'amb aerials (W)': a quiet recording lifted by 18 dB. Listen for: does its noise floor come up with it (hiss)?
  5.  1:03.52  'whip presenter whip': the highest peak of the film (-10 dBFS before the master). Listen for: is it big without hurting on headphones, and does the music under it pump?
  (--listen-out FILE.wav cuts them into one file of the film's own sound)

Still to judge by eye on review.png: character fit (each sound suits its picture), cleanliness (no mud in the low end under music/voice, nothing masks speech), taste (designed, not sprayed on).

---

# Critique, round 4

| axis | score | basis |
|---|---|---|
| hook | 10.0 | first sound at 0.00s |
| sync | 4.9 | 3/7 sounds on their frame (peaks, arrivals, or first onsets for clicks) |
| coverage | n/a | not measured (pass --moments) |
| pacing | 4.8 | 2.1 weighted events per 10 s, longest silence 9.7 s |
| variety | 1.2 | 11 source recordings, 10 families in 18 sounds (runs and interface sounds not counted) |
| hierarchy | 10.0 | 18.0 dB between the loud and the quiet sounds |
| headroom | 10.0 | true peak -3.1 dBTP |
| loudness | 10.0 | final -15.0 LUFS (the author's own balance is kept) |
| balance | 10.0 | median event peak -6 dB vs the original around it, big sounds -6 dB (whole-track gap +14 LU) |
| mono | 10.0 | the SFX track loses 0.9 dB when folded to mono (0 = the channels agree, 3 = unrelated, 6+ = parts cancel); 0 of 18 sounds lose more than 6 dB; the film loses 0.4 LU in mono against 0.3 LU for the original (+0.1 added) |

**FIX**: lowest axis 1.2 (every axis must reach 8; ok to show)

Three worst problems, fix only these, re-render, run again:
1. sync: 'amb pool deck (PW2)' at 27.30s peaks +129 ms from the moment
2. sync: 'amb pool deck (N)' at 27.30s peaks +129 ms from the moment
3. pacing: nothing happens between 12.10s and 21.80s (9.7 s)

Listen to these 5 moments, on headphones and then once on a phone speaker. This script cannot hear: they are the places where the numbers above are least certain, and none of them says that it sounds good:
  1.    0.00s  'amb aerial (W)': the first sound of the film: the hook. Listen for: does it land with the picture at once, and is it clearly there under the music or the voice?
  2.    2.80s  the busiest two seconds (4 sounds). Listen for: is every sound still distinct, or does it turn to mud?
  3.   27.30s  'amb pool deck (PW2)': its peak sits +129 ms from the moment. Listen for: does it feel early or late against the picture?
  4.   34.40s  'amb aerials (W)': a quiet recording lifted by 18 dB. Listen for: does its noise floor come up with it (hiss)?
  5.  1:03.52  'whip presenter whip': the highest peak of the film (-10 dBFS before the master). Listen for: is it big without hurting on headphones, and does the music under it pump?
  (--listen-out FILE.wav cuts them into one file of the film's own sound)

Still to judge by eye on review.png: character fit (each sound suits its picture), cleanliness (no mud in the low end under music/voice, nothing masks speech), taste (designed, not sprayed on).