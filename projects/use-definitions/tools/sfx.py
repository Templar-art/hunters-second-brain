"""Synthesise the SFX bed from build/cues.json (written by render.cjs). Usage: sfx.py <ep_dir> <dur>

Stereo, 48k. Every sound is layered (transient + body + air) and sent to a short room reverb,
so UI moves sound designed rather than beepy. Cue types: whoosh, pop, click, thud, typing,
ticks, glass, shards, riser, chime, swell.
"""
import json, sys, wave
import numpy as np

ep, DUR = sys.argv[1], float(sys.argv[2]); SR = 48000
import glob, os
N = int(SR * DUR) + SR
dry = np.zeros((N, 2)); wet = np.zeros((N, 2)); rs = np.random.default_rng(5)

def place(t, s, gain=1.0, pan=0.0, send=.18):
    """Add mono s at time t, equal-power pan (-1..1), with a reverb send."""
    i = int(t * SR)
    if i < 0 or i >= N: return
    n = min(len(s), N - i); a = (pan + 1) * np.pi / 4
    lr = np.stack([s[:n] * np.cos(a), s[:n] * np.sin(a)], 1) * gain
    dry[i:i + n] += lr; wet[i:i + n] += lr * send

def env(n, a=.003, d=.2):
    t = np.arange(n) / SR; return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)
def onepole(x, a):
    a = np.broadcast_to(a, x.shape); y = np.empty_like(x); p = 0.0
    for k in range(len(x)): p += a[k] * (x[k] - p); y[k] = p
    return y
def bandnoise(n, lo, hi):
    """Noise band-limited by FFT mask; lo/hi can sweep (arrays of length n)."""
    x = rs.standard_normal(n); X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR)
    c = (np.mean(lo) + np.mean(hi)) / 2; bw = (np.mean(hi) - np.mean(lo)) / 2
    X *= np.exp(-((f - c) / max(bw, 1)) ** 2)
    return np.fft.irfft(X, n)

def whoosh(d=.45, bright=.25):
    """Air sweep: filtered noise whose cutoff rises then falls, plus a soft tonal swish."""
    n = int(d * SR); u = np.linspace(0, 1, n); shape = np.sin(np.pi * u) ** 1.6
    cut = .015 + bright * .9 * np.sin(np.pi * np.clip(u * 1.1, 0, 1)) ** 2
    air = onepole(rs.standard_normal(n), cut) * 2.6
    hp = air - onepole(air, np.full(n, .02))
    swish = np.sin(2 * np.pi * np.cumsum(200 + 900 * u * (1 - u) * 2) / SR) * .08
    return (hp + swish) * shape
def click(f=2400):
    """UI click: sharp transient + short resonant body."""
    n = int(.04 * SR); t = np.arange(n) / SR
    tr = rs.standard_normal(n) * env(n, .0002, .0012)
    body = np.sin(2 * np.pi * f * t) * env(n, .0005, .006) * .6
    return tr * .7 + body
def pop(f=900, d=.07):
    """Bubble pop: pitch-dropping sine + click transient + tiny noise tail."""
    n = int((d * 3 + .02) * SR); t = np.arange(n) / SR
    tone = np.sin(2 * np.pi * np.cumsum(f * (1 + 1.2 * np.exp(-t * 60))) / SR) * env(n, .0008, d / 2.5)
    ck = np.zeros(n); c = click(f * 2.2)[:n]; ck[:len(c)] = c
    return tone + ck * .35
def thud(f=55, d=.4):
    """Impact: sub sine with pitch drop + mid knock + noise burst."""
    n = int(d * 2.2 * SR); t = np.arange(n) / SR
    sub = np.sin(2 * np.pi * np.cumsum(f + 110 * np.exp(-t * 30)) / SR) * env(n, .002, d / 2)
    knock = np.sin(2 * np.pi * 180 * t) * env(n, .001, .025) * .5
    burst = onepole(rs.standard_normal(n), np.full(n, .25)) * env(n, .0005, .012) * .8
    return np.tanh((sub + knock + burst) * 1.4)
def key():
    """One keystroke: two clicks (down + release) with random pitch."""
    f = 1800 + rs.random() * 1600; k = click(f); n = len(k) + int(.03 * SR)
    s = np.zeros(n); s[:len(k)] += k; j = int((.018 + rs.random() * .01) * SR); s[j:j + len(k)] += click(f * .8)[:n - j] * .4
    return s * (.7 + rs.random() * .5)
def glass(f):
    """Tiny crystalline tick (for shards / mosaics)."""
    n = int(.12 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 2.76 * t) + .3 * np.sin(2 * np.pi * f * 5.4 * t)) * env(n, .0003, .025)
def riser(d=.8):
    """Rising noise + pitch tone into a hit."""
    n = int(d * SR); u = np.linspace(0, 1, n)
    nz = onepole(rs.standard_normal(n), .005 + .3 * u ** 2) * 2
    tone = np.sin(2 * np.pi * np.cumsum(200 + 1400 * u ** 2) / SR) * .15
    return (nz + tone) * u ** 2.2
def chime(f=880):
    """Soft bell for confirmations (check marks, success)."""
    n = int(1.2 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) + .45 * np.sin(2 * np.pi * f * 2 * t) + .2 * np.sin(2 * np.pi * f * 3.01 * t)) * env(n, .002, .35)
def swell(d=1.5):
    """Low airy pad swell (end cards)."""
    n = int(d * SR); u = np.linspace(0, 1, n); t = np.arange(n) / SR
    pad = sum(np.sin(2 * np.pi * f * t + rs.random() * 6) for f in (110, 164.8, 220, 329.6)) / 4
    return (pad * .5 + onepole(rs.standard_normal(n), np.full(n, .02)) * .8) * np.sin(np.pi * u) ** 2

# ---------- sample library (sfx-lib/<type>_N.wav, Magnific/ElevenLabs takes) ----------
# Takes are trimmed to their first transient, normalised, and skipped if near-silent.
# Placement anchor per type: 'onset' (hits) or 'peak' (whoosh, riser).
LIB, ANCHOR = {}, {"whoosh": "peak", "riser": "peak"}
LIBDIR = os.environ.get("SFX_LIB", "sfx-lib")                         # v2 redo: SFX_LIB=sfx-lib-v2
for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "..", LIBDIR, "*.wav"))):
    kind = os.path.basename(f).rsplit("_", 1)[0]
    w = wave.open(f); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float).reshape(-1, w.getnchannels()) / 32768
    m = x.mean(1); pk = np.abs(m).max()
    if pk < 10 ** (-30 / 20): continue                                  # dead take
    on = int(np.argmax(np.abs(m) > pk * .1))
    if ANCHOR.get(kind) != "peak": m = m[max(0, on - int(.004 * SR)):]
    m = m / pk; n = len(m); fade = int(.03 * SR); m[-fade:] *= np.linspace(1, 0, fade)
    LIB.setdefault(kind, []).append(m)
def sample(kind, rate=1.0):
    """Random take of kind, pitch-shifted by rate (resample). Returns (signal, anchor offset in seconds)."""
    takes = LIB.get(kind)
    if not takes: return None, 0
    m = takes[rs.integers(len(takes))]
    idx = np.arange(0, len(m) - 1, rate); m = np.interp(idx, np.arange(len(m)), m)
    a = int(np.argmax(np.abs(m))) / SR if ANCHOR.get(kind) == "peak" else 0
    return m, a
def placeS(kind, t, gain, pan, send, rate=None, fallback=None):
    """Place a library sample (anchored) or the synth fallback."""
    m, a = sample(kind, rate or (.94 + rs.random() * .12))
    if m is None: place(t, fallback, gain, pan, send); return
    place(t - a, m, gain, pan, send)

# Minimal mix (Hunter: busy SFX sounded cheap). Typing capped to short quiet bursts, small UI sounds
# need 0.15s of space, and nothing small fires under a whoosh that's already playing.
CUES = sorted(json.load(open(f"{ep}/build/cues.json")), key=lambda c: c["t"])
SMALL = {"pop", "click", "ticks", "typing", "shards"}; last_small = -9; kept = []
for c in CUES:
    if c["type"] == "typing": c["n"] = min(int(c["n"]), 8); c["gain"] = (c.get("gain") or .28) * .45
    if c["type"] == "ticks": c["n"] = min(int(c["n"]), 6)
    if c["type"] in SMALL:
        if c["t"] - last_small < .15: continue
        last_small = c["t"]
    kept.append(c)
for c in kept:
    t, k, g = c["t"], c["type"], c.get("gain")
    pan = c.get("pan", (rs.random() - .5) * .5)
    if k == "whoosh":                                   # synth peaks at d/2 → anchor sample peak there
        d = c.get("d", .45); placeS("whoosh", t + d / 2, (g or .4) * .9, pan, .2, rate=1.0 / max(.35, min(1.4, d / .5)) ** .5,
                                    fallback=whoosh(d, c.get("bright", .25)))
    elif k == "pop": placeS("pop", t, (g or .2) * 1.1, pan, .18, rate=.85 + c.get("f", 900) / 3000, fallback=pop(c.get("f", 900), c.get("d", .07)))
    elif k == "click": placeS("click", t, (g or .3) * 1.1, pan, .1, fallback=click(c.get("f", 2400)))
    elif k == "thud": placeS("thud", t, (g or .4) * 1.1, 0, .25, rate=.9 + c.get("f", 55) / 600, fallback=thud(c.get("f", 55), c.get("d", .4)))
    elif k == "typing":
        for i in range(int(c["n"])): placeS("key", t + i / c.get("cps", 30) + rs.random() * .008, (g or .28) * .55, pan + (rs.random() - .5) * .2, .08, fallback=key())
    elif k == "ticks":
        for i in range(int(c["n"])): placeS("click", t + i * c.get("gap", .035), (g or .4) * .55, pan, .1, rate=1 + i * .03, fallback=click(2000 + i * 120))
    elif k == "glass" and "glass" in LIB:              # one real shatter replaces the cloud of synth ticks
        placeS("glass", t, min(.6, (g or .05) * c["n"] * .25), (rs.random() - .5) * .4, .3)
    elif k == "glass":
        for _ in range(int(c["n"])): place(t + rs.random() * c.get("span", .4), glass(2200 + rs.random() * 2400), (g or .05) * 2.2, (rs.random() - .5) * 1.6, .35)
    elif k == "shards":
        placeS("whoosh", t + .17, .22, pan, .2, rate=1.3, fallback=whoosh(.35, .35))
        for i in range(int(c["n"])): place(t + .05 + i * .03, glass(1600 + rs.random() * 1800), .08, (rs.random() - .5) * 1.4, .3)
    elif k == "riser": placeS("riser", t, (g or .25) * .9, 0, .3, rate=1.0, fallback=riser(c.get("d", .8))) if "riser" in LIB else place(t - c.get("d", .8), riser(c.get("d", .8)), g or .25, 0, .3)
    elif k == "chime": placeS("chime", t, g or .12, pan, .45, rate=1.0, fallback=chime(c.get("f", 880)))
    elif k == "swell": place(t, swell(c.get("d", 1.5)), g or .2, 0, .5)

# room reverb: exponentially decaying stereo noise IR, ~0.9s
L = int(.9 * SR); ir = rs.standard_normal((L, 2)) * np.exp(-np.arange(L) / SR / .22)[:, None]
ir = np.stack([onepole(ir[:, i], np.full(L, .35)) for i in range(2)], 1); ir /= np.abs(ir).sum(0) / 6
rev = np.stack([np.fft.irfft(np.fft.rfft(wet[:, i], 2 * N) * np.fft.rfft(ir[:, i], 2 * N), 2 * N)[:N] for i in range(2)], 1)
mix = dry + rev * .9
mix = np.tanh(mix * 1.2) / 1.2
mix *= .5 / max(np.abs(mix).max(), 1e-6)
mix = mix[:int(SR * DUR)]
w = wave.open(f"{ep}/build/sfx.wav", "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
print("sfx →", f"{ep}/build/sfx.wav")
