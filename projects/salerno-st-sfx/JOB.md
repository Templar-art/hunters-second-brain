# JOB: 42 Salerno Street, Isle of Capri — main edit SFX pass

- **Client:** listing package (agent presenter on camera); edit by Hunter
- **Status:** delivered for review (2026-11-05)
- **Source:** `/Volumes/10X SSD2/42 Salerno Street, Isle of Capri | Listing Package/Edits/Main.mp4` (67.8 s, 4K 23.976). Music is the ZOYA "Pulled Under" v8 cut ([[auto-sound-design]]).
- **Brief:** a tasteful SFX pass in the [[desire-the-pilot-reference]] style.

## What shipped
A Real SFX skill pass with 7 cues (about 10% of the 48 cuts), placed on motion and reveals only:
- whooshes at 3.54 (curtain reveal), 8.09 (garden push), 27.65 (interior move), 34.74 (into the rotating top-down) and 63.52 (the presenter whip)
- Hunter's `shing_classic` on the sun-flare peak at 6.23 (measured luma peak)
- the owned Pixabay `birds-19624` bed under the opening exteriors, 0–15 s

Kept clear on purpose: the drop at 15.1 s and the join at 54.7 s (the v8 mix already carries effects there), and the presenter zone at about 50–63 s.

Critique: every axis is 10 except pacing, which is 2.1 by design because the edit is sparse and leaves room for the presenter. The final mix is -15.0 LUFS / -3.9 dBTP, which keeps the edit's own balance.

The Whisper check produced only hallucinations: it "heard" a word on -240 dB silence, and the raw birds file transcribes as just "In." The birds have no cicada band (3.5–9 kHz share 0.01).

Outputs are in `result/`: `Salerno_Main_sfx.mp4`, `Salerno_Main_sfx_sfx_track.wav` (SFX only), the cue report and `critique.md`. Cue sheet: `work/cues.json`.

## Ledger
- Credits: 0. Everything ran locally.

## Graphics (2026-11-05)
- Address super: `Logos/Address_42-Salerno-Street_4K.png` and `_1080p.png` on the SSD, in Kollosche spec (Söhne Breit Kräftig, caps, white, centred; script `graphics/address.py`).
- Logos were gathered into `Logos/` on the SSD: Eddie Wardale team logo PNG/SVG plus `_tight` crops, the Kollosche brand marks and the 10x marks.
- ⚠️ Kollosche rule: team logos appear on Agent Focus promos only, never on listing videos. Flagged to Hunter.
- End card: Eddie Wardale outro (0408 881 678), reused from `projects/kollosche-outro/out/`. Copied to SSD `Logos/End Card/` (16:9 + 9:16 ProRes 4444 alpha + PNG).

## v3: scene-matched beds on the 15:14 re-export (2026-11-05)
The re-export carries Hunter's own SFX (logo 0–3 s, ramps around 27, 32 and 35 s, the whip at 63 s), found by subtracting the old audio. So v3 has **no whooshes**. It runs 21 scenes, each with its own bed (`work/build_v3.py`):
- birds and wind on the exteriors and aerials
- pool water on the pool shots, running water on the dock
- curtain breeze on the curtain shots
- a faint birds bleed (22–23 dB under the music) on the interiors

Each scene is calibrated to a target level under the music (13–15 dB, with `work/calib.py` iterating). Hut/pool and aerials measure +3 to +5 dB because Hunter's ramp whooshes sit in those windows. The shing stays on the flare at 6.23.

⚠️ The `outside-ambience-with-birds-61606` bed has a voice-like component around 91 s (the vocal stem is only 9 dB under), and Whisper read it as "it's fine". It was dropped from all scenes in favour of the birds and nature beds. The final Whisper pass gives only one-word birdsong hallucinations, and the vocal stem has 0% of its energy in the 200–1500 Hz speech band. No cicadas: the 3.5–9 kHz share peaks at 0.11.

Final mix: -14.6 LUFS, -0.1 dBTP (the original itself peaks at +0.9). Output: `result/Salerno_Main_sfx_v3.mp4` + `_sfx_track.wav`.

## 2026-11-05 — Lot outline + K pin
- Outline: QLD cadastre lot 231RP110045, front edge extended to kerb (Hunter: "goto the street"), SIFT-chained track on top-down (src f833–899), draws on from shot frame 22. `graphics/track_outline.py`, `render_outline2.py`.
- Pin: Kollosche navy badge K on subject roof, city wide (src f900–933), KLT tip track (5.8 px travel). `graphics/pin_salerno.py`.
- Delivered ProRes 4444 alpha + previews → SSD `Edits/Overlays/`. Cost: $0 (local).
- Full composite (2026-11-05): `Edits/Graphics/Main_Kollosche_graphics.mp4` = Main.mp4 + both alpha overlays at src frames 833 (outline) / 900 (pin), H.264 CRF 14, original audio. QC frames 832/860/899/900/920/934 checked by eye: graphics appear only inside their shots and stay locked. No pinned stills on the SSD, so the cadastre is the lot source. Wiki: [[salerno-st-listing]]. Cost: $0.

## 2026-11-05 — Outline v2 (Hunter: "the outline is dog shit")
- Diagnosis: v1's sat→drone registration was a hand-fit affine, about 1 lot width off, so the left edge cut across the subject's own roof. The line was also 21 px (Buckingham spec is 0.0033·W = 13 px) with no round joins.
- Fix: cadastre lot 231RP110045 → current QLD LatestStateProgram ortho → last top-down frame via ECC homography on edge maps (`cadastre/v2/H_ortho2last.npy`; the overlay lines up on roofs, pools and jetties). Side lines sit on both neighbours' fences. The front is extended to the kerb, detected as the first ≥100 px asphalt run (about 150 px / 5 m verge, parallel to the frontage), `cadastre/v2/kerb_lot.py`. SIFT chain track over f1–67, 13 px with round joins, draws on from f22: `graphics/outline_v2.py`.
- Hunter approved the pilot (`pilot/outline_v2_*.jpg`) → swapped into SSD `Edits/Overlays/` (v1 kept in `_v1 superseded/`), and `Edits/Graphics/Main_Kollosche_graphics.mp4` re-rendered. $0.
