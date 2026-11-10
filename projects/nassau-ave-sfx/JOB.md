# JOB — 8 Nassau Avenue, Terranora (Amir Prestige, "Bella Vista")
- Opened 2026-11-10. Source: T7 `/8 Nassau Avenue Terranora/Exports/Main.mp4` (94.8 s, 4K 23.976).
- Ask: ambience SFX (Hunter does whooshes; no shings) + pin. Reel needs a new song (pending track pick).

## Ledger
| date | item | cost |
|---|---|---|
| 2026-11-10 | SFX beds + pin, local | $0 |

## Log
- 2026-11-10 SFX: 69 shots mapped; 18 outdoor scene beds (air = wind + birds, garden = birds + nature, pool = pool water, dusk = pool + nature, end sky = wind), calibrated to 13–15 dB under the music. Interiors digitally silent (12.8–17.1, 23.4–24.5, 28.7–38.3, 63.7–79.7). `work/build.py`. Delivered `Exports/SFX/`.
- 2026-11-10 Pin: Amir style (white ap. monogram, gap, thin line) moved to the WIDE coast aerial only (Hunter: "drone pin on this one only"); source f1402–1452 (58.5 s), SIFT-homography tracked on the roof. `pin/pin_wide.py`. Medium-aerial pin removed.
- 2026-11-10 Reel song (picked from library): "on rewind", 129 BPM, closest to Amir's own lo-fi ~132 BPM reel beds. Reused the existing 30 s + 40 s zero-join reel cuts (FX + clean) → T7 `Exports/Music/`.
- 2026-11-10 Reel song: on rewind rejected ("shit"). Fire Fire picked (my rec). 41.1 s cut `auto-sound-design/tools/firefire_40.py`: drop 3.9 s, one 8-beat repeat 299->291 in a vocal gap at 32.2 s (Earshot: steady 125 BPM, coherence 0.95), riser+sub+boom on the drop and on the song's final hit 39.35. Earshot critique 20/20, -14.1 LUFS. → T7 `Exports/Music/` (FX, clean, FX stem).
