"""Beat-locked music cut-down with long musical crossfades (Hunter 29 Oct: a 60 ms join at 10 s was a hard cut).

Each join: segment 1 plays to beat `a_end`; segment 2's pre-roll (its own bars before `b_start`) overlaps the
last `xf` seconds of segment 1, so both play in time with matching harmony while one fades into the other.
`rise` > 1 makes the incoming part swell in late (for quiet piano -> loud orchestra).

Usage: python tools/reel_cut.py <song> <out.wav> '[[0, 10.8], [99.54, 107.97], [274.04, 288.6]]' '[[2.6, 1.6], [2.6, 1.0]]'
       (segments as [start, end] seconds; one [xfade_s, rise] per join)
"""
import json
import sys

import librosa
import numpy as np
import soundfile as sf

SR = 48000


def main(song, out, segs, joins, tail_fade=1.8):
    y, _ = librosa.load(song, sr=SR, mono=False)
    s0, e0 = segs[0]
    mix = y[:, int(s0 * SR):int(e0 * SR)].copy()
    for (s, e), (xf, rise) in zip(segs[1:], joins):
        n = int(xf * SR)
        pre = y[:, int((s - xf) * SR):int(s * SR)]
        n = min(n, pre.shape[1], mix.shape[1])
        t = np.linspace(0, 1, n)
        fin = np.sin(t ** rise * np.pi / 2)            # incoming: equal-power, held back by `rise`
        fout = np.cos(t * np.pi / 2)                   # outgoing: equal-power
        mix[:, -n:] = mix[:, -n:] * fout + pre[:, -n:] * fin
        mix = np.concatenate([mix, y[:, int(s * SR):int(e * SR)]], axis=1)
    f = int(tail_fade * SR)
    mix[:, -f:] *= np.cos(np.linspace(0, np.pi / 2, f)) ** 2
    k = int(0.01 * SR)
    mix[:, :k] *= np.linspace(0, 1, k)
    sf.write(out, mix.T, SR, subtype="PCM_24")
    print(out, round(mix.shape[1] / SR, 2), "s")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], json.loads(sys.argv[3]), json.loads(sys.argv[4]))
