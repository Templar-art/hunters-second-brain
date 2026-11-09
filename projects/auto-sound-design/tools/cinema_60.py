"""Cinema (Judah Earl & boda) ~60 s (v2) cinematic main edit for a very big property (2026-11-09). Earshot + Ocular loop.
Instrumental orchestral/trailer track, 113.0 BPM (brute-force grid, cinema_bt.txt, argv[2]). Map: calm intro 0-17 s, first
hit 17.03 s, strings + beat 17-34, strings dip 34-50, the song's BIGGEST hit 50.98 s (+13 dB), epic 59.5-85, triumphant
85-102, dark dip 102-118, epic 118-171 (repeats the 59-85 material 160 beats later), outro decay 172-186 = real ending.
No early repeats exist (single joins into the ending scored only ~0.74, harmony mismatch), so:
Cut: the full 17 s intro (establishing) -> hit-to-hit cut at the first hit into the biggest hit (51 s; post-hit chroma
0.895, the hit masks the edit, 15 ms crossfade just before both onsets) -> strings/epic run -> join b150 -> b310
(the epic section into its own repeat 160 beats later, score 0.976, chroma 0.989, mel 0.970, lag 0) -> the real ending.
FX (Ocular, Earshot rank): riser "Stop That Train" + song swell into the hit, sub_1 + boom "Rift" (z +4.6) on it,
faint swell at the second join. v2 ending: boom "Quake" (z +4.3) + sub on the last epic downbeat (bt 324),
the song's own decay for 2 bars, 2 s fade: Earshot critique on v1 flagged the 14 s outro as "fading away" (-12.8 LU). No intro swell: the cut starts on the song's own first note."""
import sys, numpy as np, librosa, soundfile as sf
from scipy.signal import butter, sosfilt
F = "/Users/10xhunter/Downloads/Cinema I Judah Earl & boda #music #cinematic #orchestralmusic.mp3"; OUTD = sys.argv[1]
LIB = "/Users/10xhunter/Documents/Hunters Second Brain/projects/committed-coaching/sfx-lib/"
OC = "/Users/10xhunter/Music/SFX Library/Ocular Sounds/"
SR = 44100; rng = np.random.default_rng(5)
y, _ = librosa.load(F, sr=SR, mono=False)
bt = np.loadtxt(sys.argv[2]); B = bt[1] - bt[0]
I = lambda t: int(round(t * SR))
H1, H2 = 0.0075, 0.25           # half-crossfades: tight at the hit, normal at the musical join
HIT1, HIT2 = 17.03 - 0.012, 50.98 - 0.012
END = bt[334] + 2.0   # v2: the song's decay runs 2 bars past the last epic downbeat, then a 2 s fade (the full 14 s outro read as fading away)
segs = [(0.0, HIT1, H1), (HIT2, bt[150], H2), (bt[310], END, None)]
def xf(a, b, m):
    t = np.linspace(0, np.pi / 2, m); a = a.copy(); a[:, -m:] = a[:, -m:] * np.cos(t) + b[:, :m] * np.sin(t)
    return np.concatenate([a, b[:, m:]], 1)
mix = None; prevH = 0
for a, b, h in segs:
    x = y[:, I(a - prevH):I(b + (h or 0))]
    mix = x.copy() if mix is None else xf(mix, x, I(2 * prevH))
    prevH = h or 0
f0 = I(0.02); mix[:, :f0] *= np.linspace(0, 1, f0)
DROP = HIT1 + 0.012; J = HIT1 + (bt[150] - HIT2)
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
    else: put(g[k:], t, db)
swell(DROP, 4, -10); lib(OC + "Foundation/DSGNRise/DSGNRise_RISER-Stop That Train_Ocular_Foundation.wav", DROP, -14)
lib("sub_1.wav", DROP, -12, align="attack", lo=150); lib(OC + "Foundation/DSGNBoom/DSGNBoom_BOOM-Rift_Ocular_Foundation.wav", DROP, -14, align="attack")
swell(J, 2, -20)
LAST = J + (bt[324] - bt[310])   # the epic section's last downbeat, where the song's decay starts
swell(LAST, 2, -16); lib(OC + "Foundation/DSGNBoom/DSGNBoom_BOOM-Quake_Ocular_Foundation.wav", LAST, -6, align="attack")
lib("sub_1.wav", LAST, -9, align="attack", lo=150)
n = I(2.0); ramp = np.cos(np.linspace(0, np.pi / 2, n)) ** 2
for arr in (mix, fx): arr[:, -n:] *= ramp
h = 10 ** (-9 / 20)   # the source is hot (-8 LUFS, clipped): more headroom before the -14 LUFS export
for name, x in (("mix", mix + fx), ("clean", mix), ("fx", fx)): sf.write(f"{OUTD}/{name}.wav", (x * h).T, SR, subtype="PCM_24")
print("len", round(mix.shape[1] / SR, 2), "hit", round(DROP, 2), "join", round(J, 2))
