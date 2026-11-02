"""FX for Low Again v6: v5 layers about 5 dB louder (Hunter: "some sfx I can't hear"), a third splice.

v5 notes: (Hunter: "better / more SFX", tasteful). Song-derived swells everywhere + light library layers:
  lift (song's own, 10.283 s): riser_1 + 2-beat reverse swell + sub_1 under the downbeat
  phrase downbeats in the big section (24.0, 37.7 s): faint 1-beat reverse swell
  chorus splice (34.277 s): 1-beat reverse swell + soft whoosh_1 peaking on it
  outro splice (67.697 s): reverse swell + reverb wash of the last beat + soft whoosh_2
Library hits align by their peak (risers/whooshes) or attack (sub). Writes mix + FX stem at -6 dB headroom."""
import sys, numpy as np, librosa, soundfile as sf
from scipy.signal import butter, sosfilt
CUT, OUTD = sys.argv[1], sys.argv[2]; LIB = "/Users/10xhunter/Documents/Hunters Second Brain/projects/committed-coaching/sfx-lib/"
SR = 44100; B = 0.85692; rng = np.random.default_rng(7)
song, _ = librosa.load(CUT, sr=SR, mono=False)
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
hp = lambda x, f: sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)
def ir(sec, tau): n = int(sec * SR); return rng.standard_normal(n) * np.exp(-np.arange(n) / (tau * SR))
fx = np.zeros_like(song)
def put(g, start, db):
    s = int(start * SR); g = g[: fx.shape[1] - s] * 10 ** (db / 20)
    for c in (0, 1): fx[c, s:s + len(g)] += g
def swell(t, n):
    a = int(t * SR); x = song[:, a:a + int(n * B * SR)].mean(0)
    w = lp(np.convolve(x, ir(1.2, 0.35))[: len(x)], 5000)[::-1].copy()
    w *= np.linspace(0, 1, len(w)) ** 2; f = int(0.006 * SR); w[-f:] *= np.linspace(1, 0, f)
    put(w / np.abs(w).max(), t - len(w) / SR, swell.db)
def wash(t, db):
    a = int((t - B) * SR); x = song[:, a:int(t * SR)].mean(0) * np.hanning(int(t * SR) - a)
    w = lp(np.convolve(x, ir(3.0, 0.9)), 4000)[len(x):]; w *= np.linspace(1, 0, len(w)) ** 1.5
    put(w / np.abs(w).max(), t, db)
def lib(name, t, db, align="peak", lowpass=None, highpass=None):
    g, _ = librosa.load(LIB + name, sr=SR); g = g / np.abs(g).max()
    if lowpass: g = lp(g, lowpass)
    if highpass: g = hp(g, highpass)
    k = int(np.argmax(np.abs(g)))
    if align == "peak": g = g[: k + int(0.03 * SR)]; f = int(0.03 * SR); g[-f:] *= np.linspace(1, 0, f); put(g, t - k / SR, db)
    else: put(g[k:], t, db)
LIFT, J1, J2, J3 = 10.283, 34.277, 34.277 + 14.568, 34.277 + 14.568 + 10.283
swell.db = -9; swell(LIFT, 2); lib("riser_1.wav", LIFT, -14, lowpass=8000); lib("sub_1.wav", LIFT, -12, align="attack", lowpass=150)
swell.db = -14; swell(23.994, 1); swell(J1 + 3.428, 1)  # phrase downbeats (b84, b116 in the cut)
swell.db = -13; swell(J1, 1); lib("whoosh_1.wav", J1, -19, lowpass=7000, highpass=300)
swell.db = -13; swell(J2, 1); lib("whoosh_2.wav", J2, -20, lowpass=7000, highpass=300)
OUTRO = J2 + 5.998  # song's own drop into the outro (beat 152)
swell.db = -12; swell(OUTRO, 1); wash(OUTRO, -11)
swell.db = -15; swell(J3, 1); lib("whoosh_1.wav", J3, -21, lowpass=7000, highpass=300)
g = 10 ** (-6 / 20)
for name, x in (("mix6", song + fx), ("fx6", fx)): sf.write(f"{OUTD}/{name}.wav", (x * g).T, SR, subtype="PCM_24")
print("ok")
