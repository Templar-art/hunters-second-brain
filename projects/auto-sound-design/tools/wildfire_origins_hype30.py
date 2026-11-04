"""wildfire (origins) ~32 s HYPE cut for the company, v2 (2026-11-04, Hunter on v1: "i think it could be cut up a bit
better"). v1 (in git) was choppy: three segments, the drop landed on the instrumental hook, and it ended on a fade.
v2 has one join and ends on the song's own decay. 120.0 BPM, grid = wildfire_origins_bt.txt (argv[2], start_bpm=120 +
onset-snap refit). Map (beats, 2 s bars): chorus 2 200-264, break 264-296, build 296-303 (vocal gap 300-303, mix -20 dB),
CHORUS 3 drops at 304, hook 352-364 (instrumental, -7 dB), at 364 the beat drops out and the pad decays (-10 -> -25 dB
over ~3.5 s) while the outro vocal re-enters at 363.
Cut: start at beat 300 (vocal gap in the build) -> chorus 3 drops at ~3 s -> one 2-bar trim, 336 -> 344 (both vocal gaps
-44/-49 dB, score 0.879, the best chorus 3 join; this chorus is less repetitive than chorus 2) -> end of chorus 3 -> hook
-> from beat 362.5 a 0.3 s crossfade to the demucs instrumental (argv[3]) so the outro pickup word drops out and only the
pad's natural decay remains, faded out by beat 372. FX: swell + riser + sub into the chorus 3 drop, swell + riser into
the hook, faint swell + whoosh at the join."""
import sys, numpy as np, librosa, soundfile as sf
from scipy.signal import butter, sosfilt
F = "/Users/10xhunter/Downloads/wildfire (1).mp3"; OUTD = sys.argv[1]
LIB = "/Users/10xhunter/Documents/Hunters Second Brain/projects/committed-coaching/sfx-lib/"
SR = 44100; B = 0.5; rng = np.random.default_rng(5)
y, _ = librosa.load(F, sr=SR, mono=False); nv, _ = librosa.load(sys.argv[3], sr=SR, mono=False)
bt = np.loadtxt(sys.argv[2])
I = lambda t: int(round(t * SR)); H = 0.25
START = bt[300] - 0.02; PRE = 1.0; END = bt[372]; FADE = bt[372] - bt[367]; NV = bt[362] + 0.25
n0 = min(y.shape[1], nv.shape[1]); w = np.clip((np.arange(n0) / SR - NV) / 0.3, 0, 1); w = 0.5 - 0.5 * np.cos(w * np.pi)
y = y[:, :n0] * (1 - w) + nv[:, :n0] * w  # linear (signals are correlated): full mix -> instrumental stem at NV
segs = [(START, bt[336]), (bt[344], END)]
def xf(a, b, m):
    t = np.linspace(0, np.pi / 2, m); a = a.copy(); a[:, -m:] = a[:, -m:] * np.cos(t) + b[:, :m] * np.sin(t)
    return np.concatenate([a, b[:, m:]], 1)
mix = None
for j, (a, b) in enumerate(segs):
    x = y[:, I(a - (H if j else 0)):I(b + (H if j < len(segs) - 1 else 0))]
    mix = x.copy() if mix is None else xf(mix, x, I(2 * H))
f0 = I(0.03); mix[:, :f0] *= np.linspace(0, 1, f0)
fo = I(FADE); mix[:, -fo:] *= np.cos(np.linspace(0, np.pi / 2, fo)) ** 2  # fade over the wind-down's last bar
mix = np.concatenate([np.zeros((2, I(PRE))), mix], 1)  # pre-roll room for the swell in
J = bt[336] - START + PRE; DROP = bt[304] - START + PRE; HOOK = J + bt[352] - bt[344]
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
swell(DROP, 4, -9); lib("riser_1.wav", DROP, -14, lo=9000); lib("sub_1.wav", DROP, -11, align="attack", lo=150)  # chorus 3 drop
swell(HOOK, 2, -12); lib("riser_2.wav", HOOK, -20, lo=8000)  # into the hook
swell(PRE, 2, -13)  # pre-roll into the build
h = 10 ** (-6 / 20)
for name, x in (("mix", mix + fx), ("clean", mix), ("fx", fx)): sf.write(f"{OUTD}/{name}.wav", (x * h).T, SR, subtype="PCM_24")
print("len", round(mix.shape[1] / SR, 2), "splice", round(J, 2), "drop", round(DROP, 2), "hook", round(HOOK, 2))
