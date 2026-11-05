"""on rewind (kenu) ~30 s flythrough REEL (2026-11-05, Hunter: "turn this into a 30 second reel flythough").
128.0 BPM exactly, but the groove is syncopated (3-3-2), so the tracker and per-beat onset snapping both fail (residuals
~0.1 s; autocorrelation peaks at 0.47 / 0.70 / 0.94 s). The grid comes from a brute-force period + phase search that
maximises mean onset strength on the grid (P = 0.46875 s, phase 0.36 s, every 32-beat block within 5 ms), saved as
onrewind_bt.txt (argv[2]). Map (beats): intro 0-16, verse 16-72, build 72-79, chorus 1 80-136, verse 2 144-232,
build 232-239, instrumental drop 240-256, final chorus 256-296, the song's own fade-out 296 -> end (146.4 s).
The song's last 28 s are already the reel: start at beat 252 (the last bar of the instrumental drop, full energy),
the sung chorus at ~3 s, then the song's own ending. NO joins. FX: 1 s song-derived reverse swell + riser into the
opening bar with a sub on its downbeat, and a swell into the chorus vocal."""
import sys, numpy as np, librosa, soundfile as sf
from scipy.signal import butter, sosfilt
F = "/Users/10xhunter/Downloads/on rewind.mp3"; OUTD = sys.argv[1]
LIB = "/Users/10xhunter/Documents/Hunters Second Brain/projects/committed-coaching/sfx-lib/"
SR = 44100; B = 60 / 128.0; rng = np.random.default_rng(5)
y, _ = librosa.load(F, sr=SR, mono=False)
bt = np.loadtxt(sys.argv[2])
I = lambda t: int(round(t * SR)); H = 0.25
START = bt[252] - 0.02; PRE = 1.0
segs = [(START, y.shape[1] / SR)]
def xf(a, b, m):
    t = np.linspace(0, np.pi / 2, m); a = a.copy(); a[:, -m:] = a[:, -m:] * np.cos(t) + b[:, :m] * np.sin(t)
    return np.concatenate([a, b[:, m:]], 1)
mix = None
for j, (a, b) in enumerate(segs):
    x = y[:, I(a - (H if j else 0)):I(b + (H if j < len(segs) - 1 else 0))]
    mix = x.copy() if mix is None else xf(mix, x, I(2 * H))
f0 = I(0.03); mix[:, :f0] *= np.linspace(0, 1, f0)
mix = np.concatenate([np.zeros((2, I(PRE))), mix], 1)  # pre-roll room for the swell in
DROP = PRE + 0.02; CHORUS = bt[256] - START + PRE
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
swell(DROP, 2, -4); lib("riser_1.wav", DROP, -7, lo=10000); lib("sub_1.wav", DROP, -9, align="attack", lo=150)  # into the opening bar
swell(CHORUS, 2, -12)  # into the chorus vocal
h = 10 ** (-6 / 20)
for name, x in (("mix", mix + fx), ("clean", mix), ("fx", fx)): sf.write(f"{OUTD}/{name}.wav", (x * h).T, SR, subtype="PCM_24")
print("len", round(mix.shape[1] / SR, 2), "open", round(DROP, 2), "chorus", round(CHORUS, 2))
