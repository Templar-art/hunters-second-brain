"""Wing-flap SFX from REAL recordings, synced to the rendered gulls (v2 — v1 synth read as cloth).

Cuts individual wingbeats ("grains") out of the 10x SFX_10X library recordings, then places one on
every downstroke from wings.json: random grain, pitched down 2-4 semitones (gull wings are bigger and
slower than the pigeon-ish source), distance -> level + high-cut, screen x -> pan. No synthetic layers.
Writes out/wing-flaps_real.wav (48 kHz 24-bit stereo, full clip length) at a quiet -18 dBFS peak.
"""
import json, os, subprocess, wave
import numpy as np
from scipy.signal import butter, find_peaks, resample, sosfilt

JOB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
SRC = [os.path.join(JOB, "src", "sfx", f) for f in ("Birds Flapping Whoosh.wav", "Bird Whoosh 2.wav")]
rng = np.random.default_rng(11)


def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


# ---- grain library: each wingbeat transient, -35 ms .. +170 ms, raised-cosine edges
grains = []
for p in SRC:
    x = load(p)
    e = np.sqrt(np.convolve(x ** 2, np.ones(480) / 480, "same"))
    db = 20 * np.log10(e + 1e-9)
    pk, _ = find_peaks(db, height=db.max() - 18, distance=int(0.08 * SR), prominence=6)
    for k in pk:
        a, b = k - int(0.035 * SR), k + int(0.17 * SR)
        if a < 0 or b > len(x):
            continue
        g = x[a:b].copy()
        n = len(g)
        w = np.ones(n)
        fi, fo = int(0.01 * SR), int(0.07 * SR)
        w[:fi] = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, fi))
        w[-fo:] = 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, fo))
        g *= w
        grains.append(g / np.abs(g).max())
print("grains", len(grains))


def pitch(g, semis):
    f = 2 ** (semis / 12)
    return resample(g, int(len(g) / f))  # slower + lower, like a bigger wing


def highcut(x, hz):
    return sosfilt(butter(2, hz, btype="low", fs=SR, output="sos"), x)


d = json.load(open(os.path.join(JOB, "wings.json")))
fps = d["fps"]
L = int(round(46 / fps * SR))
mix = np.zeros((L, 2))
for tag, rows in d["birds"].items():
    R = np.array(rows)
    t = (R[:, 0] - 1) / fps
    el, dist, sx = R[:, 1], R[:, 2], R[:, 3]
    bird_pitch = rng.uniform(-4, -2)
    n_ev = 0
    for i in range(1, len(R) - 1):
        if not (el[i] >= el[i - 1] and el[i] > el[i + 1]):
            continue
        j = i + 1
        while j < len(R) - 1 and el[j + 1] < el[j]:
            j += 1
        drop = el[i] - el[j]
        if drop < 12:  # gliding: no beat
            continue
        g = pitch(grains[rng.integers(len(grains))], bird_pitch + rng.uniform(-0.5, 0.5))
        g = highcut(g, float(np.clip(16000 * 8 / dist[i], 2500, 16000)))  # air absorbs highs with distance
        gain = (min(1.0, 8.0 / dist[i]) ** 1.3) * (drop / 78) * rng.uniform(0.85, 1.0)
        pan = float(np.clip((sx[i] - 0.5) * 1.6, -0.9, 0.9))
        s0 = int((t[i] + 0.02) * SR)  # transient lands just after the wing starts down
        s = g[: max(0, L - s0)]
        mix[s0:s0 + len(s), 0] += s * gain * np.cos((pan + 1) * np.pi / 4)
        mix[s0:s0 + len(s), 1] += s * gain * np.sin((pan + 1) * np.pi / 4)
        n_ev += 1
    print(f"{tag}: {n_ev} flaps, nearest {dist.min():.1f} m")

mix *= 10 ** (-18 / 20) / np.abs(mix).max()  # quiet: -18 dBFS peak
fade = int(0.005 * SR)
mix[:fade] *= np.linspace(0, 1, fade)[:, None]
mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
pcm = (np.clip(mix, -1, 1) * (2 ** 23 - 1)).astype("<i4")
out = os.path.join(JOB, "out", "wing-flaps_real.wav")
with wave.open(out, "wb") as wf:
    wf.setnchannels(2); wf.setsampwidth(3); wf.setframerate(SR)
    wf.writeframes(b"".join(int(v).to_bytes(4, "little", signed=True)[:3] for v in pcm.ravel()))
print("wrote", out)
