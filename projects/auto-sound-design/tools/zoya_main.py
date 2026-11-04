"""v4 (2026-11-05): start beat 112 for a talking video, about 23.6 s before the drop.
ZOYA - Pulled Under, main real-estate edit (~56 s), 2026-11-05.
Grid: tools/zoya_bt.txt (onset-snapped refit, 127.31 BPM). Map (beats): verse 0-156, near-silent break 156-160,
DROP 1 instrumental 160-192, chorus 192-252, verse 2 252-352, DROP 2 356-412, real ending 412-end.
Start beat 128 (61.28 s, first line after a vocal gap) -> 15.1 s calm before drop 1 (recipe 14-17 s).
One same-section join: drop-1 chorus beat 200 -> drop-2 beat 380 (chroma 0.909, level delta 0 dB), placed at the
quietest vocal point within +-1 beat, then the song's own ending.
FX: swell + riser into the first line, swell + riser + sub on the drop, faint swell + whoosh at the join."""
import sys, numpy as np, librosa, soundfile as sf
from scipy.signal import butter, sosfilt
F, VOC, BT, OUTD = sys.argv[1:5]
LIB = "/Users/10xhunter/Documents/Hunters Second Brain/projects/committed-coaching/sfx-lib/"
SR = 44100; rng = np.random.default_rng(5)
y, _ = librosa.load(F, sr=SR, mono=False); v, _ = librosa.load(VOC, sr=SR)
g = np.loadtxt(BT); B = float(np.mean(np.diff(g)))
I = lambda t: int(round(t * SR)); H = 0.04
START = g[112] - 0.02; PRE = 1.0; OFF = g[400] - g[244] + 0.180  # v3: join b244->b400, measured lag (grid drifts ~180 ms)
def vrms(t): x = v[I(t - 0.08):I(t + 0.08)]; return np.sqrt(np.mean(x ** 2))
cand = np.arange(g[244] - B, g[244] + B, 0.005)
JT = cand[np.argmin([max(vrms(t), vrms(t + OFF)) for t in cand])]
print("join out %.2f in %.2f  voc %.1f/%.1f dB" % (JT, JT + OFF, 20*np.log10(vrms(JT)+1e-9), 20*np.log10(vrms(JT+OFF)+1e-9)))
segs = [(START, JT), (JT + OFF, y.shape[1] / SR)]
def xf(a, b, m):
    t = np.linspace(0, np.pi / 2, m); a = a.copy(); a[:, -m:] = a[:, -m:] * np.cos(t) + b[:, :m] * np.sin(t)
    return np.concatenate([a, b[:, m:]], 1)
mix = None
for j, (a, b) in enumerate(segs):
    x = y[:, I(a - (H if j else 0)):I(b + (H if j < len(segs) - 1 else 0))]
    mix = x.copy() if mix is None else xf(mix, x, I(2 * H))
f0 = I(0.03); mix[:, :f0] *= np.linspace(0, 1, f0)
mix = np.concatenate([np.zeros((2, I(PRE))), mix], 1)
J = JT - START + PRE; DROP = g[160] - START + PRE
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x, axis=-1)
hp = lambda x, f: sosfilt(butter(2, f, "high", fs=SR, output="sos"), x, axis=-1)
def ir(sec, tau): n = I(sec); return rng.standard_normal(n) * np.exp(-np.arange(n) / (tau * SR))
fx = np.zeros_like(mix)
def put(s_, start, db):
    s = I(start); s_ = s_[max(0, -s):]; s = max(0, s); s_ = s_[: fx.shape[1] - s] * 10 ** (db / 20)
    for c in (0, 1): fx[c, s:s + len(s_)] += s_
def swell(t, n, db):
    x = mix[:, I(t):I(t + n * B)].mean(0)
    w = lp(np.convolve(x, ir(1.2, 0.35))[: len(x)], 5000)[::-1].copy(); w *= np.linspace(0, 1, len(w)) ** 2
    k = I(0.006); w[-k:] *= np.linspace(1, 0, k); put(w / np.abs(w).max(), t - len(w) / SR, db)
def lib(name, t, db, align="peak", lo=None, hi=None):
    s_, _ = librosa.load(LIB + name, sr=SR); s_ = s_ / np.abs(s_).max()
    if lo: s_ = lp(s_, lo)
    if hi: s_ = hp(s_, hi)
    k = int(np.argmax(np.abs(s_)))
    if align == "peak": s_ = s_[: k + I(0.03)]; q = I(0.03); s_[-q:] *= np.linspace(1, 0, q); put(s_, t - k / SR, db)
    else: put(s_[k:], t, db)
swell(J, 1, -16); lib("whoosh_1.wav", J, -24, lo=7000, hi=300)
swell(PRE, 2, -11); lib("riser_2.wav", PRE, -20, lo=8000)
swell(DROP, 2, -9); lib("riser_1.wav", DROP, -14, lo=9000); lib("sub_1.wav", DROP, -11, align="attack", lo=150)
for name, x in (("mix", mix + fx), ("clean", mix), ("fx", fx)): sf.write(f"{OUTD}/{name}_raw.wav", x.T, SR, subtype="FLOAT")
print("len %.2f  drop %.2f  join %.2f" % (mix.shape[1] / SR, DROP, J))
