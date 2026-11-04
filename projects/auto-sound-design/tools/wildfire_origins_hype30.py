"""wildfire (origins) ~30 s HYPE cut for the company (2026-11-04, Hunter: "around 30 seconds ... same edit but a more
hype version for the company"). 120.0 BPM; librosa's default tracker locks to 161 BPM on this song (median residual
0.1 s), so beats come from start_bpm=120 + onset-snapped robust refit (block offsets <= 0.02 s), saved as
wildfire_origins_bt.txt (argv[2]). Map (beats, 2 s bars): intro/verse 0-36, chorus 1 36-136, verse 2 136-164,
STOP bar 164-171 (mix -30 dB), instrumental hook drop 172-200 (no vocal), chorus 2 200-264, wind-down 264-272,
break 272-296, chorus 3 300-352, hook 352-364, outro 364-400 (quiet, vocal, fade). A hype cut can't use the real
outro (every path into it leaves ~22 s of quiet outro), so it ends on chorus 2's own wind-down (264 -> 272, -6 -> -17 dB)
with a 2 s fade over its last bar. Cut: start at beat 168 (the stop bar; drop at ~3 s) -> hook 172-180 -> join 180 -> 196
(4-bar repeat inside the instrumental hook, score 0.958) -> chorus 2 in at 200 -> join 208 -> 240 (8-bar repeat, both
vocal breath gaps -45/-47 dB, score 0.929) -> end of chorus 2 -> wind-down + fade. FX: swell + riser + sub into the drop,
faint swell at the chorus vocal entry, faint swell + whoosh at each join."""
import sys, numpy as np, librosa, soundfile as sf
from scipy.signal import butter, sosfilt
F = "/Users/10xhunter/Downloads/wildfire (1).mp3"; OUTD = sys.argv[1]
LIB = "/Users/10xhunter/Documents/Hunters Second Brain/projects/committed-coaching/sfx-lib/"
SR = 44100; B = 0.5; rng = np.random.default_rng(5)
y, _ = librosa.load(F, sr=SR, mono=False)
bt = np.loadtxt(sys.argv[2])
I = lambda t: int(round(t * SR)); H = 0.25
START = 84.11 - 0.02; PRE = 1.0; END = bt[272]; FADE = bt[272] - bt[270]
segs = [(START, bt[180]), (bt[196], bt[208]), (bt[240], END)]
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
J1 = bt[180] - START + PRE; J = J1 + bt[208] - bt[196]; DROP = bt[172] - START + PRE; HOOK = J1 + bt[200] - bt[196]
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
swell(J1, 1, -16); lib("whoosh_2.wav", J1, -24, lo=7000, hi=300)
swell(J, 1, -16); lib("whoosh_1.wav", J, -24, lo=7000, hi=300)
swell(DROP, 4, -9); lib("riser_1.wav", DROP, -14, lo=9000); lib("sub_1.wav", DROP, -11, align="attack", lo=150)  # hook drop
swell(HOOK, 2, -14)  # chorus vocal entry
swell(PRE, 2, -12); lib("riser_2.wav", PRE, -20, lo=8000)  # pre-roll into the stop bar
h = 10 ** (-6 / 20)
for name, x in (("mix", mix + fx), ("clean", mix), ("fx", fx)): sf.write(f"{OUTD}/{name}.wav", (x * h).T, SR, subtype="PCM_24")
print("len", round(mix.shape[1] / SR, 2), "splices", round(J1, 2), round(J, 2), "drop", round(DROP, 2), "hook", round(HOOK, 2))
