"""Low Again v5 (Hunter: "close my eyes and not know"; the start was the weak join).
The intro has no arrangement match anywhere later in the song, so any exit from it is audible. Instead:
start at beat 56 (49.0 s, the quiet dip right after a vocal breath, it plays like an intro), let the song make
its own lift at beat 68, splice beat 96 -> 112 (repeat of the same chorus: best-scoring pair in the song, chroma x
timbre x band energy 0.55 vs <=0.13 for any intro exit), then the approved outro splice beat 151 -> 167.
All on a fitted 70.0 BPM grid; each splice extends the outgoing part by half the crossfade so downbeats land exactly."""
import numpy as np, librosa, soundfile as sf, sys
OUT = sys.argv[1]
F = "/Users/10xhunter/Downloads/Low Again (1).mp3"
y, sr = librosa.load(F, sr=None, mono=False)
_b = np.loadtxt(sys.argv[2]); k = np.arange(len(_b)); bt = np.polyval(np.polyfit(k, _b, 1), k)
H = 0.43
def xf(a, b, m):
    t = np.linspace(0, np.pi / 2, m); a = a.copy(); a[:, -m:] = a[:, -m:] * np.cos(t) + b[:, :m] * np.sin(t)
    return np.concatenate([a, b[:, m:]], 1)
I = lambda t: int(round(t * sr)); m = I(2 * H)
segs = [(bt[56], bt[96]), (bt[112], bt[151]), (bt[167], y.shape[1] / sr)]
mix = None
for j, (a, b) in enumerate(segs):
    a0 = a - (H if j else 0.0); b1 = b + (H if j < len(segs) - 1 else 0.0)
    x = y[:, I(a0):I(b1)]
    mix = x.copy() if mix is None else xf(mix, x, m)
f = I(0.06); mix[:, :f] *= np.linspace(0, 1, f)  # click guard only; the dip starts quiet on a downbeat
sf.write(OUT, mix.T, sr, subtype="PCM_24")
o = [0.0]; [o.append(o[-1] + b - a) for a, b in segs]
print("len", round(mix.shape[1] / sr, 2), "lift at", round(bt[68] - bt[56], 3), "splices at", [round(t, 3) for t in o[1:-1]])
