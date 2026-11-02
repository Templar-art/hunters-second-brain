---
client: kollosche
address: 4-6 Buckingham Way, Elanora
opened: 2026-11-02
status: review            # intake → generating → review → delivered
cost: { credits: 0, hf_credits: 0, aud: 0 }   # derived from - 2026-11-02 review v1 → Hunter: "the end pin is unnecessary, the outline of the property is wrong … birds are shit". v2: pull-out pin and all birds cut; outline rebuilt from Hunter's own Web-02 still (he pointed me to it), cross-checked against the cadastre. Delivery folder now holds 4 overlays: opener, outline, view pin, outro, plus the preview. Old pins/birds/outro files replaced. $0.
- 2026-11-02 SFX: added `05 SFX - all` (+ `05a` beds, `05b` accents) WAVs, 48k/24-bit, 63.48 s, drop at 00:00; the preview is now `Main - Kollosche overlays + SFX PREVIEW.mp4` (preview audio loudnorm'd -7.8 → -16 LUFS; the source mix is very hot, peaks >0 dBFS). Pin whoosh pulled to -10 dB because it landed in a music dip level with the music. $0.
- 2026-11-02 SFX fix: Hunter heard "a weird voice at the start and end". Causes: `kollosche_transition_SFX.wav` is a spoken "Kollosche" voice tag (Whisper: "collection"), and the Ocular City Park beds contain kids and walla. Both are removed; outdoor beds are now The Provence woodland/field birds. The Whisper check on the new stem finds wind "shh" only. Run `auto-sound-design/output/Main_20261102-135726`. `05b` was renamed `05b SFX - whooshes.wav`.
- 2026-11-02 birds v2 (Hunter: "redo the birds"). Diagnosis: v1 gulls were 40–60 px grey specks seen from above against the forest canopy. Added `--sky-y` to plate-vfx `layout`, which keeps birds above the horizon row (330 view / 380 pull-out): 3 gulls each, seed 3, hero 9–10 m (180–260 px). Plate-untouched PASS on both. Delivered `03b Birds - gulls in the sky.mov` and rebuilt the preview with the SFX audio. Awaiting Hunter's look.
- 2026-11-02 SFX fix 2: Hunter: "did you add some annoying ass cicadas". Yes: the Provence woodland/field beds are cicada/insect loops, and 3–12 s was 95% steady 3.5–9 kHz buzz. All Provence beds are untagged; outdoor beds are now the owned Pixabay birds. The stem is now 0–3% high band, and Whisper finds no speech in any bed. `Main.mp4` disappeared from `Edits/` at 14:07 (Hunter moved it), so this run used the local overlays preview, which carries the source audio byte-copied. Run `auto-sound-design/output/Main_20261102-140925`.

- 2026-11-02 reel (Hunter: "I have the reel one now"; scope K opener + outro, outline + pin, sky birds, SFX): `Edits/Reel.mp4` 1080x1920, 692 fr / 28.86 s. Outline = Hunter's Web-06 still corners SIFT-registered to the coast wide r17 (reel 20.9 s), KLT homography track 0.23 px median, one K pin (`scripts/reel_graphics.py`). Gulls: plate-vfx on r17, `--sky-y 690`, 3 birds seed 3, plate-untouched PASS (solve 0.60 px, accepted for airborne birds). Final wide r18 skipped: tilt-up into grey haze, no solve. SFX: scene map `kollosche-buckingham-way-reel.json`, locked preset, birds/wind beds + 3 whooshes; Whisper clean (only 'the'/'You' hallucinations), hi-band no steady buzz. `scripts/assemble_reel.py` → 4 ProRes 4444 overlays + 3 SFX wavs + preview in `Edits/Kollosche Overlays - Reel/`. $0.
- 2026-11-02 Hunter: "for the pin didnt need the outline" → reel outline cut (`SHOW_OUTLINE = False`), pin now grows from frame 2 of r17; outline-draw whoosh dropped, pin whoosh at 21.4 s. Layer renamed `02 K badge pin (20.9s).mov`; SSD folder + preview rebuilt.

## Ledger — never edit by hand
---

# Job — 4-6 Buckingham Way, Elanora (Kollosche, Taylor Kleinberg)

Source: `/Volumes/10X SSD1/4-6 Buckingham Way Elanorra /Edits/Main.mp4` (Hunter's finished edit, 63.5 s, 1920×1080 23.976, AAC). Never modified; deliverables are written beside it.
Brief: "everything done to it" = Kollosche K badge pin + white tracked lot outline, CG gulls, start/end cards. 16:9. No sky, dusk or grade.

## Shots

| # | Shot | Pipeline | Status | Notes |
|---|------|----------|--------|-------|
| 0 | Opener 0–6 s | KOLLOSCHE 4K wordmark frames 0–71 (fade out 62–71) → address super "4-6 BUCKINGHAM WAY / ELANORA" 72–143, Söhne Breit Kräftig cap 47 px@4K, 8% tracking | review | ⚠️ address sits over a white eave at ~4.5 s, "BUCKINGHAM" washes slightly; Hunter can retime in FCP |
| 1 | Top-down pull-up 31.2–34.2 s (src 748–819) | chained SIFT homographies (plate-vfx solve FAILED: speed-ramp whip), white outline draws on f38–51 | review | 0.16–0.24 px/frame. v2: lot = Hunter's own outline from his `Drone Graphics/Web-02` still, SIFT-registered to the last frame (239 inliers, 1.2 px); agrees with QLD cadastre lot 130RP206900 (4,799 m², ~40×120 m). ⚠️ v1 eyeballed outline was wrong (Hunter) |
| 2 | View wide 34.2–36.2 s (820–867) | plate-vfx PASS 0.477 px; K badge pin via KLT roof track | review | gulls rendered then CUT (Hunter: "birds are shit") |
| 3 | Final pull-out 57.7–63.5 s (1383–1521) | CUT: pin ("end pin is unnecessary") and gulls ("birds are shit") | cut | wide solve 1.27 px (fails 0.5 gate: hillside parallax) — accepted for airborne birds only; plate-untouched PASS |
| 5 | SFX (Hunter: "did you do sfx aswell?" → yes, build it) | auto-sound-design, locked preset + `scene-maps/kollosche-buckingham-way-main.json`: outdoor/aerial/pool beds + 5 pinned accents (Kollosche transition at 3.0 + 61.05, Organic Motion on outline 32.75, Be Gentle on pin 34.75 at -10, Weight on pull-out whip 59.45) | review | edit's own whooshes at 7.2/36.2/45.2 s left alone; run `projects/auto-sound-design/output/Main_20261102-135136` |
| 4 | Outro 61.0 s → end (1463–1521) | make_outro.py TAYLOR KLEINBERG / 0447 466 177, 15-frame fade in | review | |

## Log

- 2026-11-02 intake: 35-shot edit, 6 drone shots. Contact sheet at `contact/sheet.jpg`. Scope from Hunter: pin + outline, birds, cards, 16:9. Agent: Taylor Kleinberg 0447 466 177.
- 2026-11-02 Hunter: "just make the overlay and i can do it on fcp" → deliverable switched from finished comp to full-length alpha overlays.
- 2026-11-02 built: `scripts/graphics.py` (outline + pins), plate-vfx birds (view, pullout_wide), `scripts/assemble.py` → 5 ProRes 4444 alpha overlays, 1522 frames / 63.48 s each, all start at 00:00 over Main.mp4, + preview MP4. Copied to `/Volumes/10X SSD1/4-6 Buckingham Way Elanorra /Edits/Kollosche Overlays/` (original Main.mp4 untouched), revealed in Finder. Sent for review. $0, all local.

## Ledger

<!-- one line per spend; the cost: header is derived from this (gen_runner.py tally) -->
<!-- no spend: all local -->

---
_Vault: [[jarvis]]_
