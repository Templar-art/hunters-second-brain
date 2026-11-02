"""No Bad Vibes (Jazzy, KILIMANJARO), ~68 s cut. 120.0 BPM fixed grid, bar 0 at -0.1 s.
Map: intro 0-31.9 (vocal from 6.4), build 31.9-47.9, drop 47.9-71.9, break 71.9-79.9, verse to 127.9, drop 2 127.9-143.9,
post 143.9-160.5. The file ends at full level (no real ending), so: no splices at all, play 0 -> 63.9 (end of the drop's
first 8 bars, a vocal lull), then a tempo-synced echo-out (1/4-note feedback delay + soft reverb, low-passing) of the
final beat. FX: song-derived reverse swell + riser + sub into the drop, faint swells on the 8-bar phrase downbeats."""
import sys, numpy as np, librosa, soundfile as sf
from scipy.signal import butter, sosfilt
F = "/Users/10xhunter/Downloads/Jazzy, KILIMANJARO - No Bad Vibes (Official Video).mp3"
OUTD = sys.argv[1]; LIB = "/Users/10xhunter/Documents/Hunters Second Brain/projects/committed-coaching/sfx-lib/"
SR = 44100; B = 0.5; rng = np.random.default_rng(3)
y, _ = librosa.load(F, sr=SR, mono=False)
bar = lambda k: -0.1 + 2.0 * k
END = bar(32); DROP = bar(24)
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x, axis=-1)
hp = lambda x, f: sosfilt(butter(2, f, "high", fs=SR, output="sos"), x, axis=-1)
def ir(sec, tau): n = int(sec * SR); return rng.standard_normal(n) * np.exp(-np.arange(n) / (tau * SR))
I = lambda t: int(round(t * SR))
MODE = sys.argv[2] if len(sys.argv) > 2 else "stop"   # v2 endings (Hunter: "ending could be better" on the echo-out)
# Final hit = the drop's own downbeat at END (one beat of full mix), rung out by a normalised reverb (60% wet).
hit = y[:, I(END):I(END + B)].copy(); k = I(0.25); hit[:, -k:] *= np.linspace(1, 0, k) ** 2
v = np.convolve(hit.mean(0), ir(4.0, 0.9)); v = lp(v, 6000); v *= 0.6 * np.abs(hit).max() / np.abs(v).max()
v *= np.linspace(1, 0, len(v)) ** 1.6; v[: I(0.03)] *= np.linspace(0, 1, I(0.03))
ring = np.stack([v, v]); ring[:, :hit.shape[1]] += hit
if MODE == "stop":   # music stops on the last eighth before END: a half-beat hole, reverse swell sucks into the hit
    music = y[:, :I(END - B / 2)].copy(); k = I(0.012); music[:, -k:] *= np.linspace(1, 0, k)
    music = np.concatenate([music, np.zeros((2, I(B / 2)))], 1)
else:                # filter-out: low-pass sweeps 16k -> 300 Hz over the last 2 bars, level eases -4 dB, into the hit
    music = y[:, :I(END)].copy(); n = I(4.0); seg = music[:, -n:]; out_ = np.zeros_like(seg); blk = I(0.05)
    for j in range(0, n, blk):
        u = j / n; fc = 16000 * (300 / 16000) ** (u ** 1.5)
        out_[:, j:j + blk] = lp(seg[:, max(0, j - I(0.1)):j + blk], fc)[:, -seg[:, j:j + blk].shape[1]:] * 10 ** (-4 * u / 20)
    music[:, -n:] = out_
out = np.zeros((2, I(END) + ring.shape[1])); out[:, :music.shape[1]] += music; out[:, I(END):] += ring
# FX
fx = np.zeros_like(out)
def put(g_, start, db):
    s = I(start); g_ = g_[: fx.shape[1] - s] * 10 ** (db / 20)
    for c in (0, 1): fx[c, s:s + len(g_)] += g_
def swell(t, n, db):
    x = y[:, I(t):I(t + n * B)].mean(0)
    w = lp(np.convolve(x, ir(1.2, 0.35))[: len(x)], 5000)[::-1].copy(); w *= np.linspace(0, 1, len(w)) ** 2
    k = I(0.006); w[-k:] *= np.linspace(1, 0, k); put(w / np.abs(w).max(), t - len(w) / SR, db)
def lib(name, t, db, align="peak", lo=None, hi=None):
    g_, _ = librosa.load(LIB + name, sr=SR); g_ = g_ / np.abs(g_).max()
    if lo: g_ = lp(g_, lo)
    if hi: g_ = hp(g_, hi)
    k = int(np.argmax(np.abs(g_)))
    if align == "peak": g_ = g_[: k + I(0.03)]; q = I(0.03); g_[-q:] *= np.linspace(1, 0, q); put(g_, t - k / SR, db)
    else: put(g_[k:], t, db)
swell(DROP, 4, -9); lib("riser_1.wav", DROP, -14, lo=9000); lib("sub_1.wav", DROP, -11, align="attack", lo=150)
for t in (bar(8), bar(16), bar(28)): swell(t, 2, -15)
lib("whoosh_1.wav", bar(16), -20, lo=7000, hi=300)
lib("sub_2.wav", END, -12, align="attack", lo=150)
if MODE == "stop": swell(END, 1, -8)   # fills the half-beat hole
else: swell(END, 2, -11)
h = 10 ** (-6 / 20)
for name, x in (("mix", out + fx), ("clean", out), ("fx", fx)): sf.write(f"{OUTD}/{name}_{MODE}.wav", (x * h).T, SR, subtype="PCM_24")
print("len", round(out.shape[1] / SR, 2), "drop at", DROP, "ending", MODE, "at", END)
