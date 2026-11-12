"""v2 (Hunter: "dont like the start"): opens 2 beats before the lift (b38) with a plain 0.25 s fade-in, no intro
impact/whoosh; big hit ~18.6 s; join 2 moved to b216->b368 (.870). Was: Ryan Taubert - Lux, ~74 s main RE edit (2026-11-12). Map (lux_bt.txt, 135.7 BPM): calm intro 0-18, lift 18.1,
break 36-53, build 53-64, BIG HIT 64.1, full 64-141, break, final 149-178, real decay. Cut: 0-b68 (30.5) | join
b68->b132 (score .894) | build + big hit + full to b196 | join b196->b370 (.814, mel .868) | final section + real
ending. FX/SFX pattern cloned from cinema_90.py."""
import sys, numpy as np, librosa, soundfile as sf
from scipy.signal import butter, sosfilt
F = "/Users/10xhunter/Downloads/Ryan Taubert - Lux.mp3"; OUTD = sys.argv[1]
LIB = "/Users/10xhunter/Documents/Hunters Second Brain/projects/committed-coaching/sfx-lib/"
OC = "/Users/10xhunter/Music/SFX Library/Ocular Sounds/"
SR = 44100; rng = np.random.default_rng(5)
y, _ = librosa.load(F, sr=SR, mono=False)
bt = np.loadtxt(sys.argv[2]); B = bt[1] - bt[0]
I = lambda t: int(round(t * SR))
def lag(a, b, w=4.0, r=0.3):   # best shift of b vs a over +-r s by onset xcorr
    o = lambda t: librosa.onset.onset_strength(y=y.mean(0)[I(t):I(t + w)], sr=SR, hop_length=256)
    oa = o(a); best = (-9, 0)
    for k in range(-int(r * SR / 256), int(r * SR / 256) + 1):
        ob = o(b + k * 256 / SR); n = min(len(oa), len(ob)); best = max(best, (np.corrcoef(oa[:n], ob[:n])[0, 1], k * 256 / SR))
    return best
c1, L1 = lag(bt[68], bt[132]); c2, L2 = lag(bt[216], bt[368]); L1 = L1 if c1 > 0.4 else 0.0; L2 = L2 if c2 > 0.4 else 0.0; print("lags ms", round(L1*1000), round(L2*1000), "corr", round(c1,3), round(c2,3))
END = 181.3
S0 = bt[38]
segs = [(S0, bt[68], 0.25), (bt[132] + L1, bt[216], 0.25), (bt[368] + L2, END, None)]
def xf(a, b, m):
    t = np.linspace(0, np.pi / 2, m); a = a.copy(); a[:, -m:] = a[:, -m:] * np.cos(t) + b[:, :m] * np.sin(t)
    return np.concatenate([a, b[:, m:]], 1)
mix = None; prevH = 0
for a, b, h in segs:
    x = y[:, I(a - prevH):I(b + (h or 0))]
    mix = x.copy() if mix is None else xf(mix, x, I(2 * prevH))
    prevH = h or 0
f0 = I(0.25); mix[:, :f0] *= np.linspace(0, 1, f0)
J1 = bt[68] - S0; J = J1 + bt[216] - bt[132] - L1; HIT1 = bt[40] - S0; DROP = J1 + bt[144] - bt[132] - L1
LASTsrc = 177.9
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x, axis=-1)
hp = lambda x, f: sosfilt(butter(2, f, "high", fs=SR, output="sos"), x, axis=-1)
def ir(sec, tau): n = I(sec); return rng.standard_normal(n) * np.exp(-np.arange(n) / (tau * SR))
fx = np.zeros_like(mix)
def put(g, start, db):
    s = I(start); g = g[max(0, -s):]; s = max(0, s); g = g[: fx.shape[1] - s] * 10 ** (db / 20)
    for c in (0, 1): fx[c, s:s + len(g)] += g
def swell(t, n, db):
    x = mix[:, I(t):I(t + n * B)].mean(0)
    w = lp(np.convolve(x, ir(1.6, 0.5))[: len(x)], 5000)[::-1].copy(); w *= np.linspace(0, 1, len(w)) ** 2
    k = I(0.006); w[-k:] *= np.linspace(1, 0, k); put(w / np.abs(w).max(), t - len(w) / SR, db)
def lib(name, t, db, align="peak", lo=None, hi=None):
    g, _ = librosa.load(name if name.startswith("/") else LIB + name, sr=SR); g = g / np.abs(g).max()
    if lo: g = lp(g, lo)
    if hi: g = hp(g, hi)
    k = int(np.argmax(np.abs(g)))
    if align == "peak": g = g[: k + I(0.03)]; q = I(0.03); g[-q:] *= np.linspace(1, 0, q); put(g, t - k / SR, db)
    elif align == "center": put(g, t - k / SR, db)   # whooshes: peak on the cue, keep the tail
    else: put(g[k:], t, db)
MODE = sys.argv[3] if len(sys.argv) > 3 else "fx"; SOFT = MODE == "soft"
LAST = J + (LASTsrc - bt[368] - L2)   # the epic section's last downbeat, where the song's decay starts
if SOFT:
    swell(DROP, 4, -14); swell(J1, 2, -24); swell(J, 2, -24); swell(LAST, 2, -20)
else:
    pass
    swell(DROP, 4, -10); lib(OC + "Foundation/DSGNRise/DSGNRise_RISER-Stop That Train_Ocular_Foundation.wav", DROP, -14)
    lib("sub_1.wav", DROP, -12, align="attack", lo=150); lib(OC + "Foundation/DSGNBoom/DSGNBoom_BOOM-Rift_Ocular_Foundation.wav", DROP, -14, align="attack")
    swell(J1, 2, -20); swell(J, 2, -20); swell(LAST, 2, -16); lib(OC + "Foundation/DSGNBoom/DSGNBoom_BOOM-Quake_Ocular_Foundation.wav", LAST, -6, align="attack")
    lib("sub_1.wav", LAST, -9, align="attack", lo=150)
if MODE == "sfx":
    W_ = OC + "Foundation/DSGNWhsh/DSGNWhsh_WHOOSH-%s_Ocular_Foundation.wav"; IM = OC + "Foundation/DSGNImpt/DSGNImpt_IMPACT-%s_Ocular_Foundation.wav"
    lib(W_ % "Turn of Events", J1, -6, align="center", hi=120)                  # covers join 1
    lib(OC + "Shift/DSGNMorph/DSGNMorph_SLOW MOTION-Frosty_Ocular_Shift.wav", J1 + 0.2, -9, align="attack")  # into the build
    lib(IM % "Epic", DROP, -12, align="attack")                                # layered on the big hit
    lib(W_ % "Organic Motion", DROP + 32 * B, -2, align="center", hi=120)      # 8-bar phrase
    lib(W_ % "Dark Air", DROP + 64 * B, -2, align="center", hi=120) if DROP + 64 * B < J - 1 else None
    lib(W_ % "Turn of Events", J, 0, align="center", hi=120)                  # covers join 2
    lib(IM % "Thunderbell", LAST, -11, align="attack")                         # shimmer under the closing boom
    b0, b1 = I(DROP - 0.45), I(DROP - 0.01); g = np.ones(b1 - b0); k = I(0.12)   # the breath before the big hit
    g[:] = 10 ** (-7 / 20); g[:k] = np.linspace(1, 10 ** (-7 / 20), k); mix[:, b0:b1] *= g
n = I(1.6); ramp = np.cos(np.linspace(0, np.pi / 2, n)) ** 2
for arr in (mix, fx): arr[:, -n:] *= ramp
h = 10 ** (-9 / 20)   # the source is hot (-8 LUFS, clipped): more headroom before the -14 LUFS export
for name, x in (("mix", mix + fx), ("clean", mix), ("fx", fx)): sf.write(f"{OUTD}/{name}.wav", (x * h).T, SR, subtype="PCM_24")
print("hit1", round(HIT1,2), "j1", round(J1,2), "len", round(mix.shape[1] / SR, 2), "big hit", DROP, "join", round(J, 2), "last", round(LAST, 2))
