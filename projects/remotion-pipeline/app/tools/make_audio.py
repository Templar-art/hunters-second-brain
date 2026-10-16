"""Synthesise original music bed + SFX (no samples, no licences needed).
Writes WAVs into ../public/audio/. Deterministic (seeded)."""
import wave
from pathlib import Path
import numpy as np

SR = 44100
OUT = Path(__file__).resolve().parents[1] / 'public' / 'audio'
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(7)


def write(name, x, stereo=None):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    x = x / max(1e-9, np.abs(x).max()) * 0.89
    with wave.open(str(OUT / name), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype('<i2').tobytes())


def t_(d):
    return np.arange(int(d * SR)) / SR


def env(n, a, r):
    e = np.ones(n)
    a, r = int(a * SR), int(r * SR)
    if a: e[:a] = np.linspace(0, 1, a)
    if r: e[-r:] *= np.linspace(1, 0, r) ** 2
    return e


def lowpass(x, cutoff):
    # one-pole, cutoff may be an array (sweeps)
    cutoff = np.broadcast_to(cutoff, x.shape)
    y = np.zeros_like(x); s = 0.0
    k = 1 - np.exp(-2 * np.pi * cutoff / SR)
    for i in range(len(x)):
        s += k[i] * (x[i] - s); y[i] = s
    return y


def mtof(m):
    return 440 * 2 ** ((m - 69) / 12)

# ---------- SFX ----------

def whoosh(d=0.7, up=True):
    t = t_(d); n = rng.standard_normal(len(t))
    sweep = np.geomspace(300, 6000, len(t)) if up else np.geomspace(6000, 300, len(t))
    x = lowpass(n, sweep) - lowpass(n, sweep * 0.25)
    e = np.sin(np.pi * t / d) ** 2
    pan = np.linspace(-0.6, 0.6, len(t))
    return np.stack([x * e * (1 - pan) / 2, x * e * (1 + pan) / 2], 1)


def pop(f0=900, d=0.12):
    t = t_(d); f = f0 * np.exp(-t * 25)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 35)


def click(d=0.05):
    t = t_(d)
    return (np.sin(2 * np.pi * 2400 * t) * 0.6 + rng.standard_normal(len(t)) * 0.4) * np.exp(-t * 160)


def thud(d=0.3):
    t = t_(d); f = 160 * np.exp(-t * 12) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)


def ding(d=1.2):
    t = t_(d)
    x = sum(a * np.sin(2 * np.pi * mtof(m) * t) for m, a in [(84, 1), (91, .5), (96, .25)])
    return x * np.exp(-t * 4) * env(len(t), 0.003, 0.05)


def tick(d=0.04):
    t = t_(d)
    return np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 200)


def shimmer(d=1.0):
    t = t_(d)
    x = sum(np.sin(2 * np.pi * mtof(m) * t + i) for i, m in enumerate([79, 83, 86, 91]))
    return x * np.sin(np.pi * t / d) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t))


for name, x in {
    'whoosh.wav': whoosh(), 'whoosh-out.wav': whoosh(0.6, up=False), 'pop.wav': pop(), 'pop-high.wav': pop(1500),
    'click.wav': click(), 'thud.wav': thud(), 'ding.wav': ding(), 'tick.wav': tick(), 'shimmer.wav': shimmer(),
}.items():
    write(name, x)

# ---------- music bed: warm lo-fi, 96 bpm, Fmaj7 – Am7 – Dm9 – Bbmaj7 ----------
BPM = 96; beat = 60 / BPM; bar = beat * 4
DUR = 30.0
N = int(DUR * SR); t = np.arange(N) / SR
mix = np.zeros((N, 2))
chords = [[53, 57, 60, 64], [57, 60, 64, 67], [50, 57, 60, 64, 65], [46, 53, 57, 62]]
bass = [41, 45, 38, 34]


def add(x, start, gain=1.0, pan=0.0):
    i = int(start * SR)
    if i >= N: return
    x = x[: N - i]
    if x.ndim == 1:
        x = np.stack([x * (1 - pan) / 2 * 2 ** .5, x * (1 + pan) / 2 * 2 ** .5], 1)
    mix[i:i + len(x)] += x * gain


for b in range(int(DUR / bar) + 1):
    c = chords[b % 4]; st = b * bar
    tt = t_(bar)
    pad = sum(np.sin(2 * np.pi * mtof(m) * tt) + 0.3 * np.sin(2 * np.pi * mtof(m) * 2.003 * tt) for m in c)
    pad *= env(len(tt), 0.4, 0.5) * (0.85 + 0.15 * np.sin(2 * np.pi * 0.5 * tt))
    add(lowpass(pad, 1200), st, 0.10)
    for k in range(2):  # bass on 1 and 3
        bt = t_(beat * 1.8)
        add(np.sin(2 * np.pi * mtof(bass[b % 4]) * bt) * env(len(bt), 0.01, 0.3), st + k * 2 * beat, 0.28)
    for k in range(4):
        kt = t_(0.35)
        kick = np.sin(2 * np.pi * np.cumsum(55 + 90 * np.exp(-kt * 30)) / SR) * np.exp(-kt * 9)
        if k in (0, 2): add(kick, st + k * beat, 0.45)
        if k in (1, 3):
            sn = lowpass(rng.standard_normal(int(0.2 * SR)), 3000) * np.exp(-t_(0.2) * 22)
            add(sn, st + k * beat, 0.18)
        for h in range(2):
            hh = rng.standard_normal(int(0.05 * SR)); hh = hh - lowpass(hh, 7000)
            add(hh * np.exp(-t_(0.05) * 90), st + k * beat + h * beat / 2 + (0.02 if h else 0), 0.10, pan=0.3)
    # soft keys arpeggio
    for k, m in enumerate([c[1] + 12, c[2] + 12, c[3] + 12, c[2] + 12]):
        at = t_(beat * 1.2)
        add(np.sin(2 * np.pi * mtof(m) * at) * np.exp(-at * 3) * env(len(at), 0.005, 0.1), st + k * beat + beat / 2, 0.06, pan=-0.3)

# vinyl-ish noise floor + master fades
mix += lowpass(rng.standard_normal(N), 2500)[:, None] * 0.004
mix *= env(N, 1.0, 1.5)[:, None]
write('music.wav', mix)
print('wrote', sorted(p.name for p in OUT.iterdir()))
