"""Cinema (Judah Earl & boda) 90 s main edit for the very big property (2026-11-09; Hunter: "I wanted cinema 90
seconds"). Same map as cinema_60.py (113 BPM, cinema_bt.txt): calm intro 0-17, first hit 17.03, strings + beat 17-34,
strings dip 34-50, the BIGGEST hit 50.98, epic 59.5-85, ... epic repeat 160 beats later, outro decay = real ending.
At 90 s no hit-to-hit cut is needed: the song plays as written from 0 to beat 143 (76.0 s, inside the epic section),
then ONE join b143 -> b311 (168 beats = 42 bars later, the same epic material in its repeat; score 0.939, chroma 0.937,
mel 0.983, lag by onset xcorr) -> the v2 ending of cinema_60 (boom on the last epic downbeat b324, 2 bars of the
song's decay, 2 s fade). FX: a light sub + swell on the first hit (17.03), the full riser + sub + boom "Rift" on the
biggest hit (50.98), faint swell at the join, boom "Quake" + sub at the end. argv[3] == "soft": swells only.
argv[3] == "sfx" (Hunter: "make it a masterpiece, add supporting sfx"): the FX pass plus a sound-design layer on the
song's 4-bar phrase grid (32-beat phrases: b16, b32 hit, b64 dip, b96 big hit, b112 epic, b128, join, end), all Ocular
picked by Earshot rank: a quiet "Cinematic Opening" impact under the first note, whooshes (Dark Air z +3.4, Transport,
Organic Motion, Turn of Events) peak-aligned on the phrase starts where picture cuts will fall (levels set by measurement to sit ~8 dB under the
music at each cue; the first pass sat 22-26 dB under in the loud section and was inaudible), the "Frosty"
slow-motion downlifter (z +3.4) into the strings dip, the "Epic" impact (z +4.2) layered on the biggest hit, a 0.45 s
"breath" (music ducked -7 dB) right before that hit, and "Thunderbell" (z +3.9) under the closing boom. No ambience
beds: those depend on the picture (no beds on interiors, birds-only outdoors)."""
import sys, numpy as np, librosa, soundfile as sf
from scipy.signal import butter, sosfilt
F = "/Users/10xhunter/Downloads/Cinema I Judah Earl & boda #music #cinematic #orchestralmusic.mp3"; OUTD = sys.argv[1]
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
c, L = lag(bt[143], bt[311]); print("join lag ms", round(L * 1000), "corr", round(c, 3))
END = bt[334] + 2.0   # v2: the song's decay runs 2 bars past the last epic downbeat, then a 2 s fade (the full 14 s outro read as fading away)
segs = [(0.0, bt[143], 0.25), (bt[311] + L, END, None)]
def xf(a, b, m):
    t = np.linspace(0, np.pi / 2, m); a = a.copy(); a[:, -m:] = a[:, -m:] * np.cos(t) + b[:, :m] * np.sin(t)
    return np.concatenate([a, b[:, m:]], 1)
mix = None; prevH = 0
for a, b, h in segs:
    x = y[:, I(a - prevH):I(b + (h or 0))]
    mix = x.copy() if mix is None else xf(mix, x, I(2 * prevH))
    prevH = h or 0
f0 = I(0.02); mix[:, :f0] *= np.linspace(0, 1, f0)
HIT1, DROP = 17.03, 50.98; J = bt[143]
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
LAST = J + (bt[324] - bt[311] - L)   # the epic section's last downbeat, where the song's decay starts
if SOFT:
    swell(HIT1, 4, -16); swell(DROP, 4, -14); swell(J, 2, -24); swell(LAST, 2, -20)
else:
    swell(HIT1, 4, -14); lib("sub_1.wav", HIT1, -16, align="attack", lo=150)
    swell(DROP, 4, -10); lib(OC + "Foundation/DSGNRise/DSGNRise_RISER-Stop That Train_Ocular_Foundation.wav", DROP, -14)
    lib("sub_1.wav", DROP, -12, align="attack", lo=150); lib(OC + "Foundation/DSGNBoom/DSGNBoom_BOOM-Rift_Ocular_Foundation.wav", DROP, -14, align="attack")
    swell(J, 2, -20); swell(LAST, 2, -16); lib(OC + "Foundation/DSGNBoom/DSGNBoom_BOOM-Quake_Ocular_Foundation.wav", LAST, -6, align="attack")
    lib("sub_1.wav", LAST, -9, align="attack", lo=150)
if MODE == "sfx":
    W_ = OC + "Foundation/DSGNWhsh/DSGNWhsh_WHOOSH-%s_Ocular_Foundation.wav"; IM = OC + "Foundation/DSGNImpt/DSGNImpt_IMPACT-%s_Ocular_Foundation.wav"
    lib(IM % "Cinematic Opening", 0.05, -15, align="attack")                   # under the first note
    lib(W_ % "Dark Air", bt[16], -12, align="center", hi=120)                   # intro phrase 2
    lib(W_ % "Transport", HIT1, -12, align="center", hi=120)                    # into the first hit
    lib(OC + "Shift/DSGNMorph/DSGNMorph_SLOW MOTION-Frosty_Ocular_Shift.wav", bt[64], -9, align="attack")  # the strings dip
    lib(IM % "Epic", DROP, -12, align="attack")                                # layered on the biggest hit
    lib(W_ % "Organic Motion", bt[112], -2, align="center", hi=120)           # the epic section
    lib(W_ % "Dark Air", bt[128], -2, align="center", hi=120)
    lib(W_ % "Turn of Events", J, 0, align="center", hi=120)                  # covers the join ("Subtle Pressure" is mostly sub, measured -22 dB under)
    lib(IM % "Thunderbell", LAST, -11, align="attack")                         # shimmer under the closing boom
    b0, b1 = I(DROP - 0.45), I(DROP - 0.01); g = np.ones(b1 - b0); k = I(0.12)   # the breath before the big hit
    g[:] = 10 ** (-7 / 20); g[:k] = np.linspace(1, 10 ** (-7 / 20), k); mix[:, b0:b1] *= g
n = I(2.0); ramp = np.cos(np.linspace(0, np.pi / 2, n)) ** 2
for arr in (mix, fx): arr[:, -n:] *= ramp
h = 10 ** (-9 / 20)   # the source is hot (-8 LUFS, clipped): more headroom before the -14 LUFS export
for name, x in (("mix", mix + fx), ("clean", mix), ("fx", fx)): sf.write(f"{OUTD}/{name}.wav", (x * h).T, SR, subtype="PCM_24")
print("len", round(mix.shape[1] / SR, 2), "big hit", DROP, "join", round(J, 2), "last", round(LAST, 2))
