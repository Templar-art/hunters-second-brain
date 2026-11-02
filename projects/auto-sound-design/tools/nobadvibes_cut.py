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
# music: 0 -> END + 1 beat, the dry tail fades over that beat
music = y[:, :I(END + B)].copy()
f = I(B); music[:, -f:] *= np.linspace(1, 0, f) ** 2
# echo-out: last beat into the downbeat, fed through a 1/4-note delay (fb 0.55, darker each repeat) + reverb
src = y[:, I(END - B):I(END + B)] * np.hanning(I(2 * B))
TAIL = 5.0; echo = np.zeros((2, I(2 * B + TAIL)))
g, cut = 0.7, 8000
for n in range(2, 11):  # first repeat lands after the dry beat has faded (n=1 would double the downbeat)
    s = I(n * B); seg = lp(src, max(cut, 800)) * g
    pan = (1.0, 0.6) if n % 2 else (0.6, 1.0)
    for c in (0, 1): echo[c, s:s + seg.shape[1]] += seg[c] * pan[c]
    g *= 0.6; cut *= 0.72
v = lp(np.convolve(src.mean(0), ir(3.5, 0.8))[: echo.shape[1]], 5000); v[: I(2 * B)] *= np.linspace(0, 1, I(2 * B))
v *= 0.3 * np.abs(src).max() / np.abs(v).max()  # IR is unnormalised noise; scale the wet to 30% of the dry peak
verb = np.stack([v] * 2)
echo[:, :verb.shape[1]] += verb
echo *= np.linspace(1, 0, echo.shape[1]) ** 1.2
out = np.zeros((2, I(END - B) + echo.shape[1])); out[:, :music.shape[1]] += music; out[:, I(END - B):] += echo
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
lib("sub_2.wav", END, -14, align="attack", lo=150)
h = 10 ** (-6 / 20)
for name, x in (("mix", out + fx), ("clean", out), ("fx", fx)): sf.write(f"{OUTD}/{name}.wav", (x * h).T, SR, subtype="PCM_24")
print("len", round(out.shape[1] / SR, 2), "drop at", DROP, "echo-out from", END)
