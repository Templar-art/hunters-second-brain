"""u know (Civilian) ~60 s main real-estate edit (2026-11-06). First cut with Earshot in the loop: FX picked by
Earshot rank from Hunter's Ocular library (riser "Stop That Train" z+3.7, boom "They're Here" z+4.8, whoosh Velocity
"Link" z+3.2; envelopes checked: Ocular risers rise to a peak then tail, so they are peak-aligned and cut 30 ms after
the peak), and the render is checked with Earshot timeline before delivery.
124.0 BPM, grid = brute-force period + phase fit (uknow_bt.txt, argv[2]; blocks within 5 ms). Map (beats): intro 0-6,
verse 6-48 (quiet, vocal), DROP 49 (instrumental, 23.6 s), chorus 78-140, break 140-200, build 200-210, drop 2 + chorus
211-268, the song's real ending 268 -> 136.5 s. Chorus 2 sits 130 beats after chorus 1 (a half-bar offset in the
arrangement), the same lines (vocal-stem match 0.98).
Cut (v2): start at beat 19 (9.3 s, a verse breath) with a plain 0.25 s fade-in, no swell, so the drop lands at ~14.5 s (Hunter's
"around 14 or after" for main edits) -> drop -> chorus 1 -> one join 122 -> 254 (both vocal breath gaps, score 0.917,
the only single-join 60 s route) -> the end of chorus 2 -> the real ending. FX: riser + swell + sub + boom into the drop,
faint swell + whoosh at the join. Join lag measured by onset xcorr over +-0.3 s: best at 0 ms, mel 0.876."""
import sys, numpy as np, librosa, soundfile as sf
from scipy.signal import butter, sosfilt
F = "/Users/10xhunter/Downloads/u know.mp3"; OUTD = sys.argv[1]
LIB = "/Users/10xhunter/Documents/Hunters Second Brain/projects/committed-coaching/sfx-lib/"
OC = "/Users/10xhunter/Music/SFX Library/Ocular Sounds/"
SR = 44100; B = 60 / 124.0; rng = np.random.default_rng(5)
y, _ = librosa.load(F, sr=SR, mono=False)
bt = np.loadtxt(sys.argv[2])
I = lambda t: int(round(t * SR)); H = 0.25
START = bt[19] - 0.02; PRE = 0.0  # v2: no intro swell (ZOYA v7 rule); start a half bar earlier so the drop still lands ~14.5 s
segs = [(START, bt[122]), (bt[254], y.shape[1] / SR)]
def xf(a, b, m):
    t = np.linspace(0, np.pi / 2, m); a = a.copy(); a[:, -m:] = a[:, -m:] * np.cos(t) + b[:, :m] * np.sin(t)
    return np.concatenate([a, b[:, m:]], 1)
mix = None
for j, (a, b) in enumerate(segs):
    x = y[:, I(a - (H if j else 0)):I(b + (H if j < len(segs) - 1 else 0))]
    mix = x.copy() if mix is None else xf(mix, x, I(2 * H))
f0 = I(0.25); mix[:, :f0] *= np.linspace(0, 1, f0)
mix = np.concatenate([np.zeros((2, I(PRE))), mix], 1)  # pre-roll room for the swell in
J = bt[122] - START + PRE; DROP = bt[49] - START + PRE
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
swell(J, 1, -16); lib(OC + "Velocity/DSGNWhsh/DSGNWhsh_DESIGNED RACE SEQUENCE-Whoosh Stem 01 Link_Ocular_Velocity.wav", J, -24, lo=8000, hi=300)
swell(DROP, 4, -8); lib(OC + "Foundation/DSGNRise/DSGNRise_RISER-Stop That Train_Ocular_Foundation.wav", DROP, -12)
lib("sub_1.wav", DROP, -10, align="attack", lo=150); lib(OC + "Foundation/DSGNBoom/DSGNBoom_BOOM-Theyre Here_Ocular_Foundation.wav", DROP, -14, align="attack")  # the drop
h = 10 ** (-6 / 20)
for name, x in (("mix", mix + fx), ("clean", mix), ("fx", fx)): sf.write(f"{OUTD}/{name}.wav", (x * h).T, SR, subtype="PCM_24")
print("len", round(mix.shape[1] / SR, 2), "splice", round(J, 2), "drop", round(DROP, 2))
