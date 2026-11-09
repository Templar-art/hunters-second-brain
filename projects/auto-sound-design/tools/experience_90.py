"""Ludovico Einaudi - Experience ~90 s soft cinematic main edit for a very big property (2026-11-09). The calmer
alternative to Cinema (Judah Earl & boda), whose trailer/electronic character Earshot confirmed was the track itself.
Picked by Earshot rank over Hunter's local tracks ("elegant cinematic orchestral, piano and strings": z +3.4, the only
strong match; runner-up The Progression of Time z +2.8). 92.5 BPM, brute-force grid (experience_bt.txt, +12 ms offset,
blocks within 15 ms; the solo-piano intro and coda are rubato). Map: solo piano 0-28, piano + glock 28-49, strings
enter 48.8 and build to 1:30, full 1:30-2:32, dip, climax 2:53-4:37 (loudest 4:14), the climax ends 4:37.3, piano coda
4:37-5:15 = the real ending.
Cut (v2): intro piano 0-18.45 (a phrase gap, -47 dB) -> the strings entry 48.6 (the gap just before it) -> the whole
build into the full section, to beat 141 (91.8) -> join into the climax at beat 389 (252.6; score 0.823, chroma 0.827,
mel 0.974, a +7.6 dB lift, so a faint song-derived swell leads into it) -> the 4:14 peak -> the orchestra's own final
chord (4:37.3) and its ring-out, faded out by 281.5. No booms or risers: the soft brief. Join lag measured by onset
xcorr over +-0.3 s. v1 ran on into the 30 s piano coda: Earshot critique flagged the ending 23.5 LU below the body
(fading away), the same failure as Cinema v1, so v2 ends on the climax's last chord instead."""
import sys, numpy as np, librosa, soundfile as sf
from scipy.signal import butter, sosfilt
F = "/Users/10xhunter/Downloads/Ludovico Einaudi - Experience (Official Visualizer).mp3"; OUTD = sys.argv[1]
SR = 44100; rng = np.random.default_rng(5)
y, _ = librosa.load(F, sr=SR, mono=False)
bt = np.loadtxt(sys.argv[2]) + 0.012; B = bt[1] - bt[0]
I = lambda t: int(round(t * SR))
def lag(a, b, w=4.0, r=0.3):   # best shift of b vs a over +-r s by onset xcorr (a = out point, b = in point)
    o = lambda t: librosa.onset.onset_strength(y=y.mean(0)[I(t):I(t + w)], sr=SR, hop_length=256)
    oa = o(a); best = (-9, 0)
    for k in range(-int(r * SR / 256), int(r * SR / 256) + 1):
        ob = o(b + k * 256 / SR); n = min(len(oa), len(ob)); c = np.corrcoef(oa[:n], ob[:n])[0, 1]
        best = max(best, (c, k * 256 / SR))
    return best
c, L = lag(bt[141], bt[389]); print("join lag ms", round(L * 1000), "corr", round(c, 3))
JB = bt[389] + L
segs = [(0.0, 18.45, 0.15), (48.6, bt[141], 0.25), (JB, 281.5, None)]
def xf(a, b, m):
    t = np.linspace(0, np.pi / 2, m); a = a.copy(); a[:, -m:] = a[:, -m:] * np.cos(t) + b[:, :m] * np.sin(t)
    return np.concatenate([a, b[:, m:]], 1)
mix = None; prevH = 0; marks = []
for a, b, h in segs:
    x = y[:, I(a - prevH):I(b + (h or 0))]
    if mix is not None: marks.append(round(mix.shape[1] / SR - prevH, 2))
    mix = x.copy() if mix is None else xf(mix, x, I(2 * prevH))
    prevH = h or 0
f0 = I(0.3); mix[:, :f0] *= np.linspace(0, 1, f0)
J = marks[1]
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x, axis=-1)
def ir(sec, tau): n = I(sec); return rng.standard_normal(n) * np.exp(-np.arange(n) / (tau * SR))
fx = np.zeros_like(mix)
def put(g, start, db):
    s = I(start); g = g[max(0, -s):]; s = max(0, s); g = g[: fx.shape[1] - s] * 10 ** (db / 20)
    for ch in (0, 1): fx[ch, s:s + len(g)] += g
def swell(t, n, db):
    x = mix[:, I(t):I(t + n * B)].mean(0)
    w = lp(np.convolve(x, ir(2.0, 0.6))[: len(x)], 4000)[::-1].copy(); w *= np.linspace(0, 1, len(w)) ** 2
    k = I(0.006); w[-k:] *= np.linspace(1, 0, k); put(w / np.abs(w).max(), t - len(w) / SR, db)
swell(J, 4, -18)
n = I(2.5); ramp = np.cos(np.linspace(0, np.pi / 2, n)) ** 2
for arr in (mix, fx): arr[:, -n:] *= ramp
h = 10 ** (-6 / 20)
for name, x in (("mix", mix + fx), ("clean", mix), ("fx", fx)): sf.write(f"{OUTD}/{name}.wav", (x * h).T, SR, subtype="PCM_24")
print("len", round(mix.shape[1] / SR, 2), "joins", marks)
