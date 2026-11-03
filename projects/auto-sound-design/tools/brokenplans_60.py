"""Broken Plans ~60 s cut (2026-11-03). 122.0 BPM exactly. librosa's beat polyfit drifted +/-0.12 s; snapping each
tracked beat to its local onset peak and refitting (robust weights) gives median residual 5 ms, so the grid is used
as-is (argv[2] = that refit bt.txt). Map (beats): hook 0-32 (instrumental, loud), verse 32-64, chorus 64-120,
verse 2 120-160, hook 160-192, verse 192-224, chorus 2 224-280, bridge 280-320, final hook 320-352, real end ~176 s.
The song repeats with a 160-beat period, so cross-section joins all score 0.6-0.75; the only >0.9 single-join path
is: start at beat 224 (110.0 s), the one-beat stop right before chorus 2 (mix -27 dB, vocal gap) -> chorus 2 drops
~1 s in -> bridge -> final hook, with one 4-bar repeat removed inside it, beat 328 -> 344 (same vocal line, vocal-stem
match >= 0.94, score 0.941, level delta < 1.5 dB) -> the song's own ending. FX: swell + riser + sub into the chorus 2
drop (the pre-roll), swell + riser into the final hook, faint swell + whoosh at the splice."""
import sys, numpy as np, librosa, soundfile as sf
from scipy.signal import butter, sosfilt
F = "/Users/10xhunter/Downloads/Broken Plans.mp3"; OUTD = sys.argv[1]
LIB = "/Users/10xhunter/Documents/Hunters Second Brain/projects/committed-coaching/sfx-lib/"
SR = 44100; B = 60 / 122.0; rng = np.random.default_rng(5)
y, _ = librosa.load(F, sr=SR, mono=False)
bt = np.loadtxt(sys.argv[2])
I = lambda t: int(round(t * SR)); H = 0.25
START = bt[224] - 0.02; PRE = 1.0
segs = [(START, bt[328]), (bt[344], y.shape[1] / SR)]
def xf(a, b, m):
    t = np.linspace(0, np.pi / 2, m); a = a.copy(); a[:, -m:] = a[:, -m:] * np.cos(t) + b[:, :m] * np.sin(t)
    return np.concatenate([a, b[:, m:]], 1)
mix = None
for j, (a, b) in enumerate(segs):
    x = y[:, I(a - (H if j else 0)):I(b + (H if j < len(segs) - 1 else 0))]
    mix = x.copy() if mix is None else xf(mix, x, I(2 * H))
f0 = I(0.03); mix[:, :f0] *= np.linspace(0, 1, f0)
mix = np.concatenate([np.zeros((2, I(PRE))), mix], 1)  # pre-roll room for the swell in
J = bt[328] - START + PRE; DROP = bt[225] - START + PRE; HOOK = bt[320] - START + PRE
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
swell(DROP, 2, -9); lib("riser_1.wav", DROP, -14, lo=9000); lib("sub_1.wav", DROP, -11, align="attack", lo=150)  # chorus 2 drop
swell(HOOK, 4, -11); lib("riser_2.wav", HOOK, -18, lo=8000)  # into the final hook
h = 10 ** (-6 / 20)
for name, x in (("mix", mix + fx), ("clean", mix), ("fx", fx)): sf.write(f"{OUTD}/{name}.wav", (x * h).T, SR, subtype="PCM_24")
print("len", round(mix.shape[1] / SR, 2), "splice", round(J, 2), "drop", round(DROP, 2), "hook", round(HOOK, 2))
