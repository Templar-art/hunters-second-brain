---
type: project
tags: [sfx, audio, procedural]
status: review
updated: 2026-10-21
---

# Custom SFX (procedural)

These are original sound effects generated in code. They cost $0 and have no licence strings attached. Script and outputs: [projects/sfx-custom/](../../projects/sfx-custom/lens_flare.py).

## Lens flare (2026-10-21)
Hunter wanted a "sunshine lens flare" sound for a clip, then asked for more versions. There are 12 variants, all 48 kHz/24-bit stereo with a -12 dBFS peak. Re-render one with `python3 lens_flare.py <name>`.

| File (`lens-flare_*.wav`) | Length | Peak | Feel |
|---|---|---|---|
| soft | 3.1 s | 0.75 s | mostly air, gentle |
| shimmer | 3.5 s | 0.85 s | full sparkle |
| sweep | 2.5 s | 0.6 s | pans L→R with the flare |
| glint | 1.3 s | 0.1 s | quick sun-off-glass ping |
| sunburst | 2.4 s | 0.18 s | fast bright hit, sparkle burst, long ring |
| golden-bloom | 4.2 s | 1.1 s | warm octave-down swell, almost no sparkle |
| anamorphic | 2.9 s | 0.7 s | rising "sing" tone streaking L→R |
| anamorphic-rtl | 2.9 s | 0.7 s | the same, R→L |
| riser-into-flare | 3.6 s | 2.0 s | builds up and hits at 2 s (put the flare there) |
| dreamy | 5.3 s | 1.4 s | slow, wide-chorus pad |
| subtle-air | 3.1 s | 0.9 s | quiet air only, sits under VO |
| crystal | 3.0 s | 0.45 s | octave-up, glassy, icy sparkle |

The layers are a pink-noise swell (attack/decay shape per variant) through an opening band-pass, a detuned A-major high-partial shimmer, sparse sparkle pings across the stereo field, a faint low bloom, an optional phase-integrated tone glide (anamorphic/riser), and a synthetic stereo reverb tail.

Lessons:
- A block-wise swept filter clicks every time its coefficients change. Use a fixed filter bank with smoothly crossfaded weights instead.
- Release the dry layers before the buffer ends, or the reverb tail starts with a hard cut.
- Always render a spectrogram to check. I can't listen to these, so vertical lines (clicks) and hard edges are the tells.

Contrast with [[extra-salt-kollosche-birds]]: synthetic *physical* sounds (wing flaps) read as fake ("like a cloth"), while abstract/designed sounds (shimmer, whoosh) are where synthesis works. For physical sounds, use real recordings.
