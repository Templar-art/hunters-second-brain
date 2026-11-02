"""Low Again v3 FX pass (Hunter: "add tasteful sfx, risers etc, to make it seamless").
Music-derived where possible (synthetic SFX were judged cheap before):
  join 1 (16.395 s, intro -> big section): reverse swell built from the 2 beats after the join, + library riser_1 peaking on it, low.
  join 2 (58.384 s, big section -> outro): reverse swell into it from the outro's first beat, + a reverb wash of the last
  beat before the join so the energy decays into the outro instead of stepping down.
Writes mix and an FX-only stem (same gain) so the levels can be re-balanced in FCP."""
import sys, numpy as np, librosa, soundfile as sf
from scipy.signal import butter, sosfilt
CUT, OUTD = sys.argv[1], sys.argv[2]
SR = 44100; rng = np.random.default_rng(7); BEAT = 0.85692
song, _ = librosa.load(CUT, sr=SR, mono=False)
J1, J2 = 16.395, 16.395 + (130.366 - 88.377)
RISER = "/Users/10xhunter/Documents/Hunters Second Brain/projects/committed-coaching/sfx-lib/riser_1.wav"
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
def ir(sec, tau): n = int(sec * SR); return rng.standard_normal(n) * np.exp(-np.arange(n) / (tau * SR))
def place(buf, g, t, db):
    s = int(t * SR); g = g[: buf.shape[1] - s] * 10 ** (db / 20)
    for c in (0, 1): buf[c, s:s + len(g)] += g
def swell(t, length):
    a = int(t * SR); x = song[:, a:a + int(length * SR)].mean(0)
    w = lp(np.convolve(x, ir(1.2, 0.35))[: len(x)], 5000)[::-1].copy()
    w *= np.linspace(0, 1, len(w)) ** 2; f = int(0.006 * SR); w[-f:] *= np.linspace(1, 0, f)
    return w / np.abs(w).max()
def wash(t, length=BEAT, tail=3.0):
    a = int((t - length) * SR); x = song[:, a:int(t * SR)].mean(0); x = x * np.hanning(len(x))
    w = lp(np.convolve(x, ir(tail, 0.9)), 4000)
    w = w[len(x):]; w *= np.linspace(1, 0, len(w)) ** 1.5
    return w / np.abs(w).max()
fx = np.zeros_like(song)
place(fx, swell(J1, 2 * BEAT), J1 - 2 * BEAT, -14)
r, _ = librosa.load(RISER, sr=SR); k = int(np.argmax(np.abs(r))); r = lp(r[:k + int(0.02 * SR)], 7000); r /= np.abs(r).max()
place(fx, r, J1 - len(r) / SR, -21)
place(fx, swell(J2, BEAT), J2 - BEAT, -17)
place(fx, wash(J2), J2, -15)
mix = song + fx
g = 10 ** (-6 / 20)  # headroom; mastered after
for name, x in (("mix", mix * g), ("fx", fx * g)): sf.write(f"{OUTD}/{name}.wav", x.T, SR, subtype="PCM_24")
print("riser len", round(len(r) / SR, 2), "peak mix", round(20 * np.log10(np.abs(mix).max()), 1))
