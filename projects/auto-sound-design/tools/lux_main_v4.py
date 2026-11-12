"""v4 TRUE GRID: the song is exactly 100 BPM (0.6 s beats, 2.4 s bars, 9.6 s phrases), anchored on the hit at 62.62:
the full section repeats every 9.600 s (waveform lag 0.0 ms) and the final section is 8 phrases (76.800 s) later.
So: open = the full section's last phrase, its closing downbeat (139.42) at 5.9 s, forced down by 6.6 s; strings cut
on their phrase boundary (31.42) straight into the hit at 33.0; whooshes on real 9.6 s phrase starts; argv[2]=="ext"
adds one phrase (jump back 9.6 s at ~96) for an 84 s version. Older notes follow.
v4 (Hunter: at least 1:13, first drop ~32 s, a loud build-up at the start that drops off at 6.5 s because there is
talking): opens on the last 6.2 s of the full section (133.7-139.9, where the song itself lets go into its break),
shaped into a build (-12 dB -> full, riser + boom at 6.2), forced down 10 dB by 6.8 s and crossfaded into the quiet
intro (6.6) -> lift 18.65 (strings held 3 dB down under the talking, released over the last bar) -> hit 32.8 ->
rest as v3. Below: the v3 notes.
Ryan Taubert - Lux, v3 main RE edit (2026-11-12). v1/v2 were built on the beat grid (lux_bt.txt), but this track
has almost no transients (pulse clarity 0.04), the grid is only good to +-80 ms, and it put the "big hit" at 64.11 s
when the real impact is at 62.62 s (a -5 dB hit after the song's own 80 ms breath) - so the boom/riser landed 1.5 s
late and the join sat in a soft passage ("those things are shit"). v3 is built on measurements, no grid:
  start 11.0 (one 4-bar intro phrase, plain 0.25 s fade-in, no intro FX) -> lift 18.37 -> strings' 7 full bars
  -> join 1: 1.2 s crossfade from the strings' soft last bar into the song's own pre-hit swell (61.7), so the hit
     (62.62) lands 8 bars after the lift, on the phrase boundary; no dip
  -> full section 62.62-~100
  -> join 2: the final section contains the same audio 76.800 s later (waveform xcorr 0.63, lag refined here to the
     sample) -> 30 ms in-phase crossfade ~1-2 s before the last hit (177.8) -> the song's real decay.
SFX levels are set by measurement: each whoosh/impact is scaled to sit REL dB under the music RMS at its cue."""
import sys, numpy as np, librosa, soundfile as sf
from scipy.signal import butter, sosfilt, correlate
F = "/Users/10xhunter/Downloads/Ryan Taubert - Lux.mp3"; OUTD = sys.argv[1]
LIB = "/Users/10xhunter/Documents/Hunters Second Brain/projects/committed-coaching/sfx-lib/"
OC = "/Users/10xhunter/Music/SFX Library/Ocular Sounds/"
SR = 44100; rng = np.random.default_rng(5); B = 0.6; EXT = len(sys.argv) > 2 and sys.argv[2] == "ext"
y, _ = librosa.load(F, sr=SR, mono=False); ym = y.mean(0)
I = lambda t: int(round(t * SR))
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x, axis=-1)
hp = lambda x, f: sosfilt(butter(2, f, "high", fs=SR, output="sos"), x, axis=-1)
T0, LIFT, X1, Y1, HIT, LASTsrc, END = 11.0, 17.02, 31.36, 62.56, 62.62, 177.8, 181.3
# join 1 harmony check: strings' last bar vs the pre-hit swell
ch = lambda a, b: librosa.feature.chroma_cqt(y=ym[I(a):I(b)], sr=SR).mean(1)
cj = np.corrcoef(ch(X1 - 0.7, X1 + 0.7), ch(Y1 - 0.7, Y1 + 0.7))[0, 1]; H1 = 0.6
H1 = 0.04   # clash: cut in the song's own breath right before the hit instead
print("join1 chroma", round(cj, 3), "xfade s", 2 * H1)
# join 2: out point = quietest instant in 98.4-100.2, in point = +76.800 refined to the sample by waveform xcorr
bpf = sosfilt(butter(4, [200, 4000], "band", fs=SR, output="sos"), ym)
e = np.sqrt(np.convolve(ym ** 2, np.ones(I(0.03)) / I(0.03), "same")); a0, a1 = I(98.4), I(100.2)
A2 = (a0 + int(np.argmin(e[a0:a1]))) / SR
w = I(1.0); ref = bpf[I(A2) - w:I(A2) + w]; s0 = I(A2 + 76.800) - w - I(0.02); cand = bpf[s0:s0 + 2 * w + I(0.04)]
c = correlate(cand, ref, "valid"); k = int(np.argmax(c)); OFF = (s0 + k - (I(A2) - w)) / SR
print("join2 out", round(A2, 3), "offset", round(OFF, 4), "waveform corr", round(np.corrcoef(ref, cand[k:k + 2 * w])[0, 1], 3))
H2 = 0.015
NB = float(sys.argv[3]) if len(sys.argv) > 3 else 0   # extra bars of opening build (Hunter: "the start needs to be a bit longer"); everything after shifts later
O0, OPK, IN1, H0 = 133.52 - 2.4 * NB, 139.42, 5.32, 0.5   # open: source 139.9 (last loud instant) lands at 6.2 s
e2 = lambda a, b: (I(a) + int(np.argmin(e[I(a):I(b)]))) / SR; AJ = e2(95.7, 96.5)
segs = [(O0, OPK + 1.0, H0), (IN1, X1, H1)] + ([(Y1, AJ, H2), (AJ - 9.6, A2, H2)] if EXT else [(Y1, A2, H2)]) + [(A2 + OFF, END, None)]
g0 = np.ones(I(OPK + 1.0 + H0) - I(O0) + 8); r0, r1 = I(OPK + 0.25 - O0), I(OPK + 0.75 - O0)
g0[r0:r1] = 10 ** (np.linspace(0, -10, r1 - r0) / 20); g0[r1:] = 10 ** (-10 / 20)
def xf(a, b, m):
    t = np.linspace(0, np.pi / 2, m); a = a.copy(); a[:, -m:] = a[:, -m:] * np.cos(t) + b[:, :m] * np.sin(t)
    return np.concatenate([a, b[:, m:]], 1)
mix = None; prevH = 0
for a, b, h in segs:
    x = y[:, I(a - prevH):I(b + (h or 0))]
    if mix is None: x = x * g0[: x.shape[1]]
    mix = x.copy() if mix is None else xf(mix, x, I(2 * prevH))
    prevH = h or 0
f0 = I(0.25); mix[:, :f0] *= np.linspace(0, 1, f0)
OPEN = OPK - O0; LIFTo = OPEN + 1.0 + LIFT - IN1; J1 = LIFTo + X1 - LIFT; DROP = J1 + HIT - Y1; JX = DROP + AJ - HIT; J2 = DROP + A2 - HIT + (9.6 if EXT else 0); LAST = J2 + LASTsrc - (A2 + OFF)
def gain(pts):   # piecewise-linear dB automation over output time
    tt = np.arange(mix.shape[1]) / SR; mix[:] *= 10 ** (np.interp(tt, [p[0] for p in pts], [p[1] for p in pts]) / 20)
gain([(0, -9), (OPEN - 2.9, -2), (OPEN - 1.7, 0), (LIFTo - 0.5, 0), (LIFTo + 1.5, -3), (DROP - 2.4, -3), (DROP - 0.2, 0)])
def ir(sec, tau): n = I(sec); return rng.standard_normal(n) * np.exp(-np.arange(n) / (tau * SR))
fx = np.zeros_like(mix); mm = mix.mean(0)
rms = lambda x: np.sqrt(np.mean(x ** 2) + 1e-12)
def put(g, start, db):
    s = I(start); g = g[max(0, -s):]; s = max(0, s); g = g[: fx.shape[1] - s] * 10 ** (db / 20)
    for c in (0, 1): fx[c, s:s + len(g)] += g
def swell(t, n, db):
    x = mm[I(t):I(t + n * B)]
    w = lp(np.convolve(x, ir(1.6, 0.5))[: len(x)], 5000)[::-1].copy(); w *= np.linspace(0, 1, len(w)) ** 2
    k = I(0.006); w[-k:] *= np.linspace(1, 0, k); put(w / np.abs(w).max(), t - len(w) / SR, db)
REPORT = []
def lib(name, t, db=None, align="peak", lo=None, hi=None, rel=None):
    g, _ = librosa.load(name if name.startswith("/") else LIB + name, sr=SR); g = g / np.abs(g).max()
    if lo: g = lp(g, lo)
    if hi: g = hp(g, hi)
    k = int(np.argmax(np.abs(g)))
    if rel is not None:   # sit `rel` dB under the music at the cue (both measured over the 0.8 s around the peak / cue)
        q = I(0.4); gs = rms(g[max(0, k - q):k + q]); ms = rms(mm[max(0, I(t) - q):I(t) + q]); db = 20 * np.log10(ms / gs) + rel
    REPORT.append((round(t, 2), name.split("_")[-3] if "Ocular" in name else name, round(db, 1)))
    if align == "peak": g = g[: k + I(0.03)]; q = I(0.03); g[-q:] *= np.linspace(1, 0, q); put(g, t - k / SR, db)
    elif align == "center": put(g, t - k / SR, db)
    else: put(g[k:], t, db)
W_ = OC + "Foundation/DSGNWhsh/DSGNWhsh_WHOOSH-%s_Ocular_Foundation.wav"; IM = OC + "Foundation/DSGNImpt/DSGNImpt_IMPACT-%s_Ocular_Foundation.wav"
BOOM = OC + "Foundation/DSGNBoom/DSGNBoom_BOOM-%s_Ocular_Foundation.wav"
RISE = OC + "Foundation/DSGNRise/DSGNRise_RISER-%s_Ocular_Foundation.wav"
# the open: riser through the build, boom + sub where it lets go, a quiet downlifter falling away under the talking
lib(RISE % "Lift Off", OPEN, rel=-5); lib(BOOM % "Groundbreaking", OPEN, rel=-6, align="attack"); lib("sub_1.wav", OPEN, -11, align="attack", lo=150)
lib(OC + "Shift/DSGNMorph/DSGNMorph_SLOW MOTION-Frosty_Ocular_Shift.wav", OPEN + 0.05, -20, align="attack")
# the hit: song-derived reverse swell + riser into it, sub + boom + impact on it
swell(DROP, 4, -12); lib(OC + "Foundation/DSGNRise/DSGNRise_RISER-Stop That Train_Ocular_Foundation.wav", DROP, rel=-9)
lib("sub_1.wav", DROP, -12, align="attack", lo=150); lib(BOOM % "Rift", DROP, rel=-8, align="attack"); lib(IM % "Epic", DROP, rel=-9, align="attack")
# phrase whooshes in the full section (8 and 16 bars after the hit), where picture cuts will fall
for k, nm in enumerate(["Organic Motion", "Dark Air", "Transport", "Organic Motion"][: 4 if EXT else 3]):   # phrase starts (9.6 s)
    lib(W_ % nm, DROP + 9.6 * (k + 1), rel=-8, align="center", hi=120)
# into the ending: whoosh through join 2, boom + shimmer + sub on the last hit
lib(W_ % "Turn of Events", (J2 + LAST) / 2, rel=-9, align="center", hi=120)
swell(LAST, 2, -16); lib(BOOM % "Quake", LAST, rel=-7, align="attack"); lib("sub_1.wav", LAST, -9, align="attack", lo=150)
lib(IM % "Thunderbell", LAST, rel=-10, align="attack")
n = I(1.6); ramp = np.cos(np.linspace(0, np.pi / 2, n)) ** 2
for arr in (mix, fx): arr[:, -n:] *= ramp
h = 10 ** (-9 / 20)
for name, x in (("mix", mix + fx), ("clean", mix), ("fx", fx)): sf.write(f"{OUTD}/{name}.wav", (x * h).T, SR, subtype="PCM_24")
print("open peak", round(OPEN, 2), "len", round(mix.shape[1] / SR, 2), "lift", round(LIFTo, 2), "join1", round(J1, 2), "HIT", round(DROP, 2), "join2", round(J2, 2), "last", round(LAST, 2))
for r in REPORT: print("  sfx", r)
