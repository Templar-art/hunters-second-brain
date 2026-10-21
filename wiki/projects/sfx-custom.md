---
type: project
tags: [sfx, audio, procedural]
status: review
updated: 2026-10-21
---

# Custom SFX (procedural)

These are original sound effects generated in code. They cost $0 and have no licence strings attached. Script and outputs: [projects/sfx-custom/](../../projects/sfx-custom/lens_flare.py).

## Lens flare (2026-10-21)
Hunter wanted a "sunshine lens flare" sound for a clip. There are three variants, all 48 kHz/24-bit stereo with a -12 dBFS peak:
- `lens-flare_soft.wav`: 3.1 s, peak at 0.75 s, mostly air.
- `lens-flare_shimmer.wav`: 3.5 s, peak at 0.85 s, full sparkle.
- `lens-flare_sweep.wav`: 2.5 s, peak at 0.6 s, pans left to right as the flare travels.

The layers are a pink-noise swell through an opening band-pass, a detuned A-major high-partial shimmer, sparse sparkle pings across the stereo field, a faint low bloom, and a synthetic stereo reverb tail.

Lessons:
- A block-wise swept filter clicks every time its coefficients change. Use a fixed filter bank with smoothly crossfaded weights instead.
- Release the dry layers before the buffer ends, or the reverb tail starts with a hard cut.
- Always render a spectrogram to check. I can't listen to these, so vertical lines (clicks) and hard edges are the tells.

Contrast with [[extra-salt-kollosche-birds]]: synthetic *physical* sounds (wing flaps) read as fake ("like a cloth"), while abstract/designed sounds (shimmer, whoosh) are where synthesis works. For physical sounds, use real recordings.
