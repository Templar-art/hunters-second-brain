---
client: REAL Specialists (Connor Hewitt)
address: 21 Albany Avenue, Currumbin
opened: 2026-11-09
status: review            # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 0, aud: 0 }   # all local
---

# Job: 21 Albany Ave Main edit, SFX + REAL pin

**Source:** `/Volumes/10X SSD3/21 Albany Avenue, Currumbin/Exports/21 Albany Avenue | Main.mp4`. It is 64.06 s at 1080p 23.976, -14.0 LUFS, with a 124 BPM house track that ends at 59.3 s. The rest of the film (the whip pan, the dusk aerial and the end card) has no sound.
**Brief (Hunter):** "this need sfx", plus "the real specialist pin on the wide drone".

## SFX (Salerno v3 recipe, adapted)
- Earshot timeline found **no baked-in SFX**. Only the music's own swells and hits are there, and the drop is at 14.1–14.5 s.
- **Scene beds, 24 scenes** (`work/build.py`, calibrated with `work/calib.py`). Each bed sits a target distance under the music; four calibration rounds brought 19 scenes within 1 dB of target:
  - beach waves on the beach shots (owned Pixabay *soft waves* / *sandy beach calm waves*, copied to `beds/`)
  - wind and birds on the aerials
  - birds on the exteriors
  - pool water on the pool shots
  - a birds bleed 23 dB under the music on the interiors
  - soft wind and nature on the twilight front
  - a fixed-level wind bed under the silent tail, fading out over the end card
- **Accents:**
  - whoosh at 34.83 s (balcony to aerial), Weight
  - soft whoosh at 36.60 s as the REAL pin fades in, Sweetener 33 at -8
  - whoosh at 56.22 s (interior to top-down), Sweetener 33
  - whoosh at 60.35 s on the whip pan, Weight
  - soft `lens-flare_soft` on the sunburst window at 38.75 s

  The two whoosh files are the picks Hunter approved on Coastal 34 Albany. The music's drop and kicks are left alone.
- **Checks:**
  - Critique: hook, hierarchy, headroom, loudness, balance and mono all score 10. Variety is 1, which comes from the bed recipe: one birds and one wind field recording run across scenes, the same as the approved Salerno pass.
  - Final mix is -13.9 LUFS / -1.8 dBTP.
  - Whisper heard only "…" plus one "You" at 52–54 s, which is a noise hallucination.
  - The 3.5–9 kHz band only spikes in single half-seconds of birdsong. There is no steady cicada wall (every bed file's median share is 0.00–0.10).

## REAL pin
- The wide drone shot is at Main frames 872–917 (36.37–38.29 s). The house was identified from the cadastre (lot 1RP198415) and the QLD aerial photo: the white two-storey with the grey hip roof, solar, and the pool on the left, with the water reservoir behind. `work/ortho.jpg`, `work/subj_crop.jpg`.
- The roof ridge was LK-tracked with a partial affine, drifting 22 px over the shot (`work/pin_track.json`). The orange logo-only PNG (280 px wide at 1080) sits on the sky above the horizon, with a 4 px white line centred under it down to the ridge. It fades in over frames 3–11 and hard-cuts out with the shot. `pin.py`.

## Delivered (2026-11-09)
- `Exports/SFX/21 Albany Avenue | Main (SFX + REAL pin) preview.mp4`
- `Exports/SFX/21 Albany Main SFX only (starts 00-00-00-00).wav` (48k/24-bit, full length)
- `Video/REAL Overlays/04 REAL pin wide drone 4K (Main 00-00-36-08).mov` (ProRes 4444 alpha, 46 frames; place at 00:00:36:08)

## Reel ambience (2026-11-09)
Hunter: "this one please. I put the whooshes and shings, I just want the ambience stuff. Make sure there's no birds on the inside of the houses."
- **Source:** `Exports/Reel.mp4`, 30.4 s, 9:16, 26 shots.
- **Beds:** 17 outdoor scenes get calibrated beds, built with the same files and calibration as Main (`reel/build.py`). Waves on the beach aerial, wind and birds on the aerials, birds on the exteriors and deck, pool water on the pool shots. All 17 landed on target in 4 rounds.
- **Interiors:** 9.84–14.64 and 16.56–19.44 get **nothing**. The outdoor beds stop at the cut into an interior with a 0.12 s fade, rather than crossfading across it. Measured digital silence in both blocks.
- **Tail:** the beds fade out over Hunter's whip into the end card (out by 27.6 s).
- **Checks:** Whisper produced only its stock non-speech hallucination ("Thanks for watching!" across the whole file). The high band spikes to 0.53 on single birdsong half-seconds only, with no cicada wall.
- **Delivered:** `Exports/SFX/21 Albany Reel ambience only (starts 00-00-00-00).wav` + `21 Albany Reel (ambience) preview.mp4`.

## Ledger
<!-- one line per spend -->
- 2026-11-09 | 0 | all local (Earshot, real-sfx mix, OpenCV track)
