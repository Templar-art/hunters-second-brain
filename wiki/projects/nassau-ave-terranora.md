---
type: project
tags: [sfx, ambience, drone-pin, amir-prestige, listing-video, overlays]
status: review
updated: 2026-11-10
---

# 8 Nassau Ave, Terranora ("Bella Vista"): Main + Reel

This is the listing film for [[amir-prestige]]. The T7 shoot folder is labelled "| Coastline". Job: [JOB.md](../../projects/nassau-ave-sfx/JOB.md). Cost: $0, everything ran locally.

- **Main SFX (94.8 s):** ambience beds only, because Hunter does the whooshes and wants no shings. 69 shots were mapped into 18 outdoor scene beds, calibrated 13–15 dB under the music, and the interiors are silent. Built with `work/build.py`; the output is in T7 `Exports/SFX/`.
- **Pin:** in Amir style (white "ap.", a gap, then a thin line), on the wide coast aerial only, tracked with SIFT homography. Built with `pin/pin_wide.py`.
- **Reel music:** "on rewind" was rejected. Fire Fire is used instead, as a 41 s cut with a riser, sub and boom on the drop (`auto-sound-design/tools/firefire_40.py`).
- **Reel SFX (30 s, 9:16, 2026-11-10):** the same recipe. 10 outdoor scenes, interiors from 16.6 to 26.2 s silent, all scenes within 0.4 dB of target. Built with `reel/build.py`, delivered as `Exports/SFX/Nassau_Reel_SFX_ambience.wav` plus a preview.
- **Overlays:** the Amir pack (logo opener, logo on black, address, "bella vista" title, placeholder agent card, end card, grey mat), built with `projects/amir-prestige-overlays/`. It is in T7 `Amir Overlays/` and in the reel kit.

**Lesson:** Whisper can invent a whole sentence on a heavily boosted water and bird bed. Before calling it a voice, run Whisper on each source window on its own and run Earshot `describe` on the mix. Here the sources were clean and the AudioSet top labels were Bird and Environmental noise.
