"""Aerial + day-to-night SFX for the Kollosche cinematic reel (Hunter's edit, 33.62 s, Love Me).

Hunter 29 Oct: "need aerials sfx and day to night sfx". Two stems, both from 0:00, same length as the reel:
  aerials     - high-altitude air (soft wind, high-passed, slow stereo drift) on the three aerials
                (0-1.04 K open, 29.11-30.61 block, 30.61-end skyline) + a distant city bed under the skyline
                and a soft filtered-air sweep on the 30.61 cut
  day-to-night - the window shot 19.39-21.77 where the sky turns day -> dusk (~20.1-21.2) and lands on the drop:
                daytime birds through the glass fade out, evening crickets fade in as the sky turns, and a low
                "time" swell (Shift: Time and Space) rises under it. All ends on the 21.77 cut into the drop.

Usage: python tools/kollosche_aerial_d2n.py OUT_DIR
"""
import os
import sys

import librosa
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
LEN = 33.617
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.expanduser("~/Music/SFX Library/Ocular Sounds")
PIX = os.path.join(HERE, "..", "sfx", "pixabay-owned")
rng = np.random.default_rng(3)


def load(p, start=0.0, dur=None):
    y, _ = librosa.load(p, sr=SR, mono=False, offset=start, duration=dur)
    y = np.atleast_2d(y)
    return np.vstack([y, y]) if y.shape[0] == 1 else y[:2]


def filt(x, kind, hz, order=2):
    return sosfilt(butter(order, hz, kind, fs=SR, output="sos"), x, axis=-1)


def rms_to(x, db):
    r = np.sqrt((x ** 2).mean())
    return x * 10 ** (db / 20) / max(r, 1e-9)


def env(n, pts):
    """Piecewise-linear gain over n samples from [(t_s, gain), ...] (t relative to the clip start)."""
    t = np.arange(n) / SR
    return np.interp(t, [p[0] for p in pts], [p[1] for p in pts])


def lay(buf, x, t0, gain_pts):
    s = int(t0 * SR)
    x = x[:, : buf.shape[1] - s]
    buf[:, s:s + x.shape[1]] += x * env(x.shape[1], gain_pts)


def drift(x, rate=0.07, depth=0.35):
    """Slow stereo drift so the air feels like it moves past the drone."""
    t = np.arange(x.shape[1]) / SR
    p = depth * np.sin(2 * np.pi * rate * t + rng.uniform(0, 6))
    return np.vstack([x[0] * np.cos((p + 1) * np.pi / 4) * 1.414, x[1] * np.sin((p + 1) * np.pi / 4) * 1.414])


def air(dur, db):
    """Altitude air: soft wind recording, high-passed so it is breath not rumble, plus a whisper of filtered noise."""
    w = load(os.path.join(PIX, "storegraphic-soft-wind-477404.mp3"))
    while w.shape[1] < dur * SR:
        w = np.hstack([w, w[:, ::-1]])                 # mirror-loop: no click at the seam
    w = filt(w[:, : int(dur * SR)], "high", 250)
    nz = filt(rng.standard_normal((2, int(dur * SR))), "band", [1800, 7000])
    nz = nz * (0.6 + 0.4 * np.sin(2 * np.pi * 0.18 * np.arange(nz.shape[1]) / SR))
    return drift(rms_to(w, db) + rms_to(nz, db - 9))


def main(out):
    n = int(LEN * SR)
    aer, d2n = np.zeros((2, n)), np.zeros((2, n))

    # --- aerials
    lay(aer, air(1.6, -31), 0.0, [(0, 0), (0.25, 1), (1.04, 1), (1.5, 0)])            # K open, gone by the facade
    lay(aer, air(4.6, -30), 29.0, [(0, 0), (0.35, 1), (4.3, 1), (4.6, 0)])            # block + skyline
    city = load(os.path.join(LIB, "Cityscapes Vol 1", "AMBUrbn",
                             "AMBUrbn_CITY PARK-Urban Park Ambience Loop 11_Ocular_Cityscapes Vol 1.wav"), 5, 3.2)
    city = rms_to(filt(filt(city, "low", 1400), "high", 120), -36)                     # far below: hum, no detail
    lay(aer, city, 30.45, [(0, 0), (0.5, 1), (2.85, 1), (3.15, 0)])
    sw = filt(rng.standard_normal((2, int(1.1 * SR))), "band", [500, 4000])
    t = np.arange(sw.shape[1]) / SR
    sw = sw * np.sin(np.pi * np.clip(t / 1.1, 0, 1)) ** 2
    sw = filt(sw, "low", 2500) * np.vstack([np.linspace(1.2, 0.6, len(t)), np.linspace(0.6, 1.2, len(t))])
    lay(aer, rms_to(sw, -30), 30.61 - 0.6, [(0, 1), (1.1, 1)])                         # air sweep on the cut

    # --- day to night (window shot 19.39-21.77)
    birds = load(os.path.join(PIX, "freesound_community-outside-ambience-with-birds-61606.mp3"), 40, 2.6)
    birds = rms_to(filt(birds, "low", 6000), -33)                                      # heard through the glass
    lay(d2n, birds, 19.39, [(0, 0), (0.12, 1), (0.75, 1), (1.9, 0)])
    crick = load(os.path.join(LIB, "The Provence", "AMBGras",
                              "AMBGras_FIELD-Night Ambience Field Loop 01_Ocular_The Provence.wav"), 20, 2.0)
    crick = rms_to(filt(crick, "low", 9000), -33)
    lay(d2n, crick, 20.0, [(0, 0), (0.6, 0.35), (1.5, 1), (1.77, 1), (2.0, 0)])       # in as the sky turns, out on the cut
    ts = load(os.path.join(LIB, "Shift", "DSGNMorph", "DSGNMorph_SLOW MOTION-Stem 02 Time and Space_Ocular_Shift.wav"))
    pk = int(np.argmax(np.abs(ts).sum(0)))
    a = max(0, pk - int(1.6 * SR))
    ts = rms_to(filt(ts[:, a:pk], "low", 3000), -30)                                   # the rise only, no impact
    lay(d2n, ts, 21.72 - ts.shape[1] / SR, [(0, 0), (ts.shape[1] / SR * 0.6, 0.6), (ts.shape[1] / SR, 1)])

    for name, x in (("6 SFX - aerials (air + skyline city).wav", aer), ("7 SFX - day to night (birds to crickets).wav", d2n)):
        sf.write(os.path.join(out, name), np.clip(x, -1, 1).T, SR, subtype="PCM_24")
        print(name, "peak", round(20 * np.log10(np.abs(x).max() + 1e-9), 1), "dBFS")


if __name__ == "__main__":
    main(sys.argv[1])
