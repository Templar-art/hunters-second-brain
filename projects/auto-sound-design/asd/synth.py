"""Free, local, seeded synthesis of ambience beds and a soft shimmer, for when the library
has none. These are synthetic stand-ins, not recordings: fine as low beds, but a real
recorded ambience (e.g. Ocular Rainforest/Cityscapes) will sound more natural."""

from pathlib import Path

import numpy as np

from . import media

RATE = 48000


def _noise(rng, n, colour):
    """White/pink/brown noise, normalised to peak 1."""
    white = rng.standard_normal(n)
    if colour == "white":
        x = white
    else:
        spec = np.fft.rfft(white)
        f = np.fft.rfftfreq(n, 1 / RATE)
        f[0] = f[1]
        spec /= np.sqrt(f) if colour == "pink" else f
        x = np.fft.irfft(spec, n)
    return x / (np.abs(x).max() + 1e-12)


def _band(x, lo, hi):
    spec = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / RATE)
    spec[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(spec, len(x))


def _lfo(n, rate_hz, depth, rng):
    t = np.arange(n) / RATE
    phase = rng.uniform(0, 2 * np.pi)
    slow = np.sin(2 * np.pi * rate_hz * t + phase) + 0.5 * np.sin(2 * np.pi * rate_hz * 2.7 * t + phase * 1.3)
    return 1 - depth + depth * (slow - slow.min()) / (np.ptp(slow) + 1e-12)


def _stereo(rng, n, make):
    """Two decorrelated takes for width."""
    return np.stack([make(np.random.default_rng(rng.integers(1 << 31))) for _ in range(2)], axis=1)


def _chirps(rng, n, per_second, f_lo, f_hi):
    """Sparse little bird chirps: short downward FM sweeps in small clusters."""
    out = np.zeros(n)
    t_total = n / RATE
    count = int(per_second * t_total)
    for _ in range(count):
        start = rng.uniform(0, t_total - 1)
        for k in range(rng.integers(1, 4)):
            dur = rng.uniform(0.04, 0.12)
            m = int(dur * RATE)
            tt = np.arange(m) / RATE
            f0 = rng.uniform(f_lo, f_hi)
            sweep = f0 * (1 - 0.35 * tt / dur)
            phase = 2 * np.pi * np.cumsum(sweep) / RATE
            env = np.sin(np.pi * tt / dur) ** 2
            i = int((start + k * rng.uniform(0.09, 0.18)) * RATE)
            if i + m < n:
                out[i: i + m] += rng.uniform(0.3, 1.0) * env * np.sin(phase)
    return out


def _crickets(rng, n):
    t = np.arange(n) / RATE
    out = np.zeros(n)
    for _ in range(3):
        f = rng.uniform(4200, 5200)
        pulse_rate = rng.uniform(14, 22)
        gate = (np.sin(2 * np.pi * pulse_rate * t + rng.uniform(0, 6)) > 0.6).astype(float)
        trill = (np.sin(2 * np.pi * rng.uniform(0.25, 0.5) * t + rng.uniform(0, 6)) > -0.2).astype(float)
        env = np.convolve(gate * trill, np.ones(96) / 96, mode="same")
        out += rng.uniform(0.4, 1.0) * env * np.sin(2 * np.pi * f * t)
    return out


def _fade(x, sec=1.0):
    m = int(sec * RATE)
    ramp = np.linspace(0, 1, m)[:, None] if x.ndim == 2 else np.linspace(0, 1, m)
    x[:m] *= ramp
    x[-m:] *= ramp[::-1]
    return x


def _norm(x, peak_db):
    return x / (np.abs(x).max() + 1e-12) * 10 ** (peak_db / 20)


def make_assets(out_dir, seconds=60, seed=7):
    """Writes the synthetic kit + .tags sidecars. Returns the list of files."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)
    n = int(seconds * RATE)
    files = {}

    def outdoor(r):
        air = _band(_noise(r, n, "pink"), 150, 6000) * _lfo(n, 0.08, 0.6, r)
        leaves = _band(_noise(r, n, "white"), 2500, 9000) * _lfo(n, 0.15, 0.8, r) * 0.25
        birds = _chirps(r, n, 0.35, 2800, 5200) * 0.35
        return air + leaves + birds
    files["ambience_outdoor_breeze_birds.wav"] = (_stereo(rng, n, outdoor), "ambience, outdoor, exterior, breeze, birds, synthetic")

    def aerial(r):
        wind = _band(_noise(r, n, "brown"), 40, 1800) * _lfo(n, 0.05, 0.5, r)
        hiss = _band(_noise(r, n, "pink"), 800, 5000) * _lfo(n, 0.11, 0.7, r) * 0.35
        return wind + hiss
    files["ambience_aerial_wind.wav"] = (_stereo(rng, n, aerial), "ambience, aerial, wind, air, high, synthetic")

    def interior(r):
        tone = _band(_noise(r, n, "brown"), 30, 400) + 0.15 * _band(_noise(r, n, "pink"), 400, 3000)
        outside = _band(_chirps(r, n, 0.12, 2500, 4000), 1500, 3500) * 0.08  # far-off birds through glass
        return tone + outside
    files["ambience_interior_roomtone.wav"] = (_stereo(rng, n, interior), "ambience, interior, roomtone, inside, quiet, synthetic")

    def dusk(r):
        air = _band(_noise(r, n, "pink"), 100, 3000) * _lfo(n, 0.06, 0.5, r) * 0.6
        return air + _crickets(r, n) * 0.25
    files["ambience_dusk_crickets.wav"] = (_stereo(rng, n, dusk), "ambience, dusk, twilight, evening, crickets, exterior, synthetic")

    # Soft shimmer: a cluster of high partials with a slow swell and long glassy tail.
    m = int(3.0 * RATE)
    t = np.arange(m) / RATE
    env = np.minimum(1, t / 0.35) * np.exp(-np.maximum(0, t - 0.35) / 0.9)
    shimmer = np.zeros((m, 2))
    for k, f in enumerate([1760, 2217, 2637, 3520, 4434, 5274]):
        for ch in range(2):
            detune = 1 + rng.uniform(-0.004, 0.004)
            trem = 1 + 0.25 * np.sin(2 * np.pi * rng.uniform(4, 7) * t)
            shimmer[:, ch] += (0.6 ** k) * env * trem * np.sin(2 * np.pi * f * detune * t + rng.uniform(0, 6))
    files["shimmer_soft_glint.wav"] = (shimmer, "shimmer, glint, sparkle, sun, flare, synthetic")

    written = []
    for name, (audio, tags) in files.items():
        audio = _norm(audio, -3.0)
        if audio.shape[0] == n:
            audio = _fade(audio, 1.0)
        path = out_dir / name
        media.write_wav(path, audio.astype(np.float32))
        (out_dir / (name + ".tags")).write_text(tags + "\n")
        written.append(path)
    return written
