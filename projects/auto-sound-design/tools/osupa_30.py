"""Osupa Ti ~30 s REEL cut (Hunter 2026-11-02: "make it 30 seconds ... its for a reel"). Reel = hook fast, so no intro:
start at bar 20 b3 (~43.2 s), the pickup word of the break line after a one-beat breath (bar 20 b2, vocal -30 dB); v1 started at bar 19 = 34 s, too long; the quieter break
plays like an intro, 1 s song-derived reverse swell + riser pre-roll into the first word. Break builds into drop 1
(bar 24, ~8 s in). Then the two v3 splices Hunter already approved: bar 27 b1 -> bar 91 b1 (final vocal line of drop 2),
bar 95 b0 -> bar 111 b0 (the song's own decay ending). bt = librosa beat grid of the radio edit, bar n beat b = bt[2+4n+b].
FX: swell + riser + sub into the drop, faint swell + soft whoosh at both splices."""
import sys, numpy as np, librosa, soundfile as sf
from scipy.signal import butter, sosfilt
F = "/Users/10xhunter/Downloads/Osupa Ti (Radio Edit).mp3"; OUTD = sys.argv[1]
LIB = "/Users/10xhunter/Documents/Hunters Second Brain/projects/committed-coaching/sfx-lib/"
SR = 44100; B = 0.5; rng = np.random.default_rng(5)
y, _ = librosa.load(F, sr=SR, mono=False)
bt = np.loadtxt(sys.argv[2]); beat = lambda n, b: bt[2 + 4 * n + b]
I = lambda t: int(round(t * SR)); H = 0.25
START = beat(20, 3); PRE = 1.0
segs = [(START, beat(27, 1)), (beat(91, 1), beat(95, 0)), (beat(111, 0), y.shape[1] / SR)]
def xf(a, b, m):
    t = np.linspace(0, np.pi / 2, m); a = a.copy(); a[:, -m:] = a[:, -m:] * np.cos(t) + b[:, :m] * np.sin(t)
    return np.concatenate([a, b[:, m:]], 1)
mix = None
for j, (a, b) in enumerate(segs):
    x = y[:, I(a - (H if j else 0)):I(b + (H if j < len(segs) - 1 else 0))]
    mix = x.copy() if mix is None else xf(mix, x, I(2 * H))
f0 = I(0.03); mix[:, :f0] *= np.linspace(0, 1, f0)
mix = np.concatenate([np.zeros((2, I(PRE))), mix], 1)  # pre-roll room for the swell in
J = beat(27, 1) - START + PRE; J2 = J + beat(95, 0) - beat(91, 1); DROP = beat(24, 0) - START + PRE
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x, axis=-1)
hp = lambda x, f: sosfilt(butter(2, f, "high", fs=SR, output="sos"), x, axis=-1)
def ir(sec, tau): n = I(sec); return rng.standard_normal(n) * np.exp(-np.arange(n) / (tau * SR))
fx = np.zeros_like(mix)
def put(g, start, db):
    s = I(start); g = g[max(0, -s):]; s = max(0, s); g = g[: fx.shape[1] - s] * 10 ** (db / 20)  # riser longer than the pre-roll: clip its head
    for c in (0, 1): fx[c, s:s + len(g)] += g
def swell(t, n, db):
    x = mix[:, I(t):I(t + n * B)].mean(0)
    w = lp(np.convolve(x, ir(1.2, 0.35))[: len(x)], 5000)[::-1].copy(); w *= np.linspace(0, 1, len(w)) ** 2
    k = I(0.006); w[-k:] *= np.linspace(1, 0, k); put(w / np.abs(w).max(), t - len(w) / SR, db)
def lib(name, t, db, align="peak", lo=None, hi=None):
    g, _ = librosa.load(LIB + name, sr=SR); g = g / np.abs(g).max()
    if lo: g = lp(g, lo)
    if hi: g = hp(g, hi)
    k = int(np.argmax(np.abs(g)))
    if align == "peak": g = g[: k + I(0.03)]; q = I(0.03); g[-q:] *= np.linspace(1, 0, q); put(g, t - k / SR, db)
    else: put(g[k:], t, db)
swell(J, 1, -16); lib("whoosh_1.wav", J, -24, lo=7000, hi=300)
swell(DROP, 4, -9); lib("riser_1.wav", DROP, -14, lo=9000); lib("sub_1.wav", DROP, -11, align="attack", lo=150)
swell(J2, 1, -16); lib("whoosh_2.wav", J2, -24, lo=7000, hi=300)
swell(PRE, 2, -9); lib("riser_2.wav", PRE, -18, lo=8000)  # swell into the first word
h = 10 ** (-6 / 20)
for name, x in (("mix", mix + fx), ("clean", mix), ("fx", fx)): sf.write(f"{OUTD}/{name}.wav", (x * h).T, SR, subtype="PCM_24")
print("len", round(mix.shape[1] / SR, 2), "splices", round(J, 2), round(J2, 2), "drop", round(DROP, 2))
