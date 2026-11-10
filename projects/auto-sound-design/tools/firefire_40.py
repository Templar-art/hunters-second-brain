"""Fire Fire ~41 s reel for 8 Nassau Ave (2026-11-10), from firefire_30.py: one 8-beat repeat 299 -> 291 inside the 288-299 vocal gap, then the song's own stop.
125.0 BPM exactly, grid = brute-force period + phase fit (firefire_bt.txt, argv[2]; every 32-beat block within 5 ms).
Map (beats): intro 0-51, break 52-79, DROP 1 at 80 (38.8 s), break 176-239, DROP 2 at 240 (115.6 s) to a hard stop at
~147.5 s (the song's own ending, short reverb tail to ~149 s). Drop 2 vocal runs 240-275, gaps 276-283 and 288-299.
Cut: start on the last 2 bars of the break-2 build (beat 232, plain 0.25 s fade-in), drop 2 lands at 3.8 s, one join
279 -> 295 (16 beats, both sides in vocal gaps: -36 / -70 dB; score 0.933, measured onset lag 0 ms, mel 0.939), then
the song's own stop. FX from Ocular: riser "Stop That Train" + song swell + sub_1 + boom "They're Here" on the drop
(the u know picks Hunter approved), whoosh "Speed is Everything" (Earshot rank z +4.95) + faint swell at the join."""
import sys, numpy as np, librosa, soundfile as sf
from scipy.signal import butter, sosfilt
F = "/Users/10xhunter/Downloads/Shimza x AR_CO x Kasango - Fire Fire (Visualizer) [Helix Records].mp3"; OUTD = sys.argv[1]
LIB = "/Users/10xhunter/Documents/Hunters Second Brain/projects/committed-coaching/sfx-lib/"
OC = "/Users/10xhunter/Music/SFX Library/Ocular Sounds/"
SR = 44100; B = 60 / 125.0; rng = np.random.default_rng(5)
y, _ = librosa.load(F, sr=SR, mono=False)
bt = np.loadtxt(sys.argv[2])
I = lambda t: int(round(t * SR)); H = 0.25
START = bt[232] - 0.02; PRE = 0.0
segs = [(START, bt[299]), (bt[291], 149.0)]
def xf(a, b, m):
    t = np.linspace(0, np.pi / 2, m); a = a.copy(); a[:, -m:] = a[:, -m:] * np.cos(t) + b[:, :m] * np.sin(t)
    return np.concatenate([a, b[:, m:]], 1)
mix = None
for j, (a, b) in enumerate(segs):
    x = y[:, I(a - (H if j else 0)):I(b + (H if j < len(segs) - 1 else 0))]
    mix = x.copy() if mix is None else xf(mix, x, I(2 * H))
f0 = I(0.25); mix[:, :f0] *= np.linspace(0, 1, f0)
mix = np.concatenate([np.zeros((2, I(PRE))), mix], 1)  # pre-roll room for the swell in
J = bt[299] - START + PRE; DROP = bt[240] - START + PRE
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
    g, _ = librosa.load(name if name.startswith("/") else LIB + name, sr=SR); g = g / np.abs(g).max()
    if lo: g = lp(g, lo)
    if hi: g = hp(g, hi)
    k = int(np.argmax(np.abs(g)))
    if align == "peak": g = g[: k + I(0.03)]; q = I(0.03); g[-q:] *= np.linspace(1, 0, q); put(g, t - k / SR, db)
    else: put(g[k:], t, db)
swell(J, 1, -16); lib(OC + "Foundation/DSGNWhsh/DSGNWhsh_WHOOSH-Speed is Everything_Ocular_Foundation.wav", J, -22, lo=8000, hi=300)
swell(DROP, 2, -8); lib(OC + "Foundation/DSGNRise/DSGNRise_RISER-Stop That Train_Ocular_Foundation.wav", DROP, -12)
lib("sub_1.wav", DROP, -10, align="attack", lo=150); lib(OC + "Foundation/DSGNBoom/DSGNBoom_BOOM-Theyre Here_Ocular_Foundation.wav", DROP, -14, align="attack")  # the drop
END = 39.35  # the song's own final hit
swell(END, 2, -12); lib(OC + "Foundation/DSGNRise/DSGNRise_RISER-Stop That Train_Ocular_Foundation.wav", END, -18)
lib("sub_1.wav", END, -9, align="attack", lo=150); lib(OC + "Foundation/DSGNBoom/DSGNBoom_BOOM-Theyre Here_Ocular_Foundation.wav", END, -13, align="attack")
h = 10 ** (-6 / 20)
for name, x in (("mix", mix + fx), ("clean", mix), ("fx", fx)): sf.write(f"{OUTD}/{name}.wav", (x * h).T, SR, subtype="PCM_24")
print("len", round(mix.shape[1] / SR, 2), "splice", round(J, 2), "drop", round(DROP, 2))
