"""Custom sunshine lens-flare SFX (procedural, original, royalty-free).

  python3 projects/sfx-custom/lens_flare.py   -> out/lens-flare_{soft,shimmer,sweep}.wav

Layers: airy noise swell with an opening band-pass (the light "blooming"), a glassy shimmer pad
(detuned high partials of an A-major chord), sparse sparkle pings scattered across the stereo field,
and a synthetic stereo reverb tail. 48 kHz / 24-bit stereo, -12 dBFS peak, fades built in.
"""
import os, wave
import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


def pink(n, rng):
    f = np.fft.rfftfreq(n, 1 / SR)
    spec = (rng.standard_normal(len(f)) + 1j * rng.standard_normal(len(f))) / np.sqrt(np.maximum(f, 20))
    x = np.fft.irfft(spec, n)
    return x / np.abs(x).max()


def sweep_band(x, f_lo, f_hi, bands=14):
    """Band-pass that glides f_lo -> f_hi (log): a fixed filter bank with smoothly crossfaded weights (click-free)."""
    n = len(x)
    centres = np.geomspace(f_lo * 0.8, f_hi * 1.2, bands)
    track = np.geomspace(f_lo, f_hi, n)  # target centre per sample
    out = np.zeros(n)
    for fc in centres:
        sos = butter(2, [fc / 1.35, min(fc * 1.35, SR / 2 - 200)], btype="band", fs=SR, output="sos")
        w = np.exp(-0.5 * (np.log(track / fc) / 0.35) ** 2)  # gaussian in log-frequency
        out += sosfilt(sos, x) * w
    return out


def swell(n, peak, attack_pow=2.2, decay=0.6):
    t = np.arange(n) / SR
    a = np.clip(t / peak, 0, 1) ** attack_pow
    return a * np.exp(-np.clip(t - peak, 0, None) / decay)


def reverb_ir(seconds, rng, damp=6000):
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = []
    for _ in range(2):  # decorrelated L/R
        x = rng.standard_normal(n) * np.exp(-t / (seconds / 6.9))  # ~60 dB decay over `seconds`
        ir.append(sosfilt(butter(1, damp, btype="low", fs=SR, output="sos"), x))
    ir = np.stack(ir, 1)
    return ir / np.sqrt((ir ** 2).sum(0))


def pan(x, p):
    return np.stack([x * np.cos((p + 1) * np.pi / 4), x * np.sin((p + 1) * np.pi / 4)], 1)


def make(name, dur, peak, seed, sparkle=1.0, shimmer=1.0, air=1.0, pan_sweep=(0.0, 0.0), bloom=(500, 7000), tail=2.2,
         attack=2.0, decay=0.35, root=1.0, detune=4, glide=None, low=0.05, spark_hz=(3500, 9500), spark_spread=0.22):
    """attack: swell curve power (higher = later, snappier build). decay: tail length as a fraction of dur.
    root: chord transpose (0.5 = octave down/warmer). detune: shimmer cents (wider = dreamier chorus).
    glide: (f_start, f_end, level) rising/falling tone, the anamorphic streak "sing". spark_spread: sparkle timing spread."""
    rng = np.random.default_rng(seed)
    n = int(dur * SR)
    t = np.arange(n) / SR
    mix = np.zeros((n, 2))

    # 1) air swell: pink noise through an opening band-pass, panned along the flare's travel
    a = sweep_band(pink(n, rng), *bloom) * swell(n, peak, attack, decay * dur) * air
    p_t = np.interp(t, [0, dur], pan_sweep)
    mix += np.stack([a * np.cos((p_t + 1) * np.pi / 4), a * np.sin((p_t + 1) * np.pi / 4)], 1)

    # 2) glassy shimmer pad: detuned high partials, slow beating, fades in just before the peak
    chord = [f * root for f in (1760.0, 2217.5, 2637.0, 3520.0, 4434.9, 5274.0)]
    pad = np.zeros(n)
    for f in chord:
        for det in (-detune, detune):  # cents
            ff = f * 2 ** (det / 1200)
            pad += np.sin(2 * np.pi * ff * t + rng.uniform(0, 2 * np.pi)) * (1.0 / (1 + f / 2500))
    pad *= swell(n, peak * 1.08, attack + 1.0, (decay + 0.1) * dur) * (1 + 0.25 * np.sin(2 * np.pi * 5.5 * t)) * shimmer
    mix += np.stack([pad, pad], 1) * 0.06

    # 3) sparkles: short sine pings clustered around the peak, random pitch + pan
    count = int(26 * sparkle)
    for _ in range(count):
        t0 = abs(rng.normal(peak, spark_spread * dur))
        if t0 >= dur - 0.05:
            continue
        f = rng.uniform(*spark_hz)
        m = int(rng.uniform(0.04, 0.12) * SR)
        tt = np.arange(m) / SR
        ping = np.sin(2 * np.pi * f * tt) * np.exp(-tt / rng.uniform(0.015, 0.045)) * np.clip(tt / 0.006, 0, 1) ** 2
        s0 = int(t0 * SR)
        seg = pan(ping * rng.uniform(0.25, 0.7) * 0.18, rng.uniform(-0.85, 0.85))[: n - s0]
        mix[s0:s0 + len(seg)] += seg

    # 4) soft low bloom under the peak (felt more than heard)
    lo = np.sin(2 * np.pi * 110 * t) * swell(n, peak, attack + 0.5, 0.25 * dur) * low
    mix += np.stack([lo, lo], 1)

    # 5) optional tone glide: phase-integrated sweep, the "sing" of an anamorphic streak
    if glide:
        f0, f1, lvl = glide
        fr = f0 * (f1 / f0) ** np.clip(t / max(peak * 1.2, 1e-3), 0, 1)
        ph = 2 * np.pi * np.cumsum(fr) / SR
        g = (np.sin(ph) + 0.35 * np.sin(2 * ph + 0.3)) * swell(n, peak, attack, decay * dur) * lvl
        mix += np.stack([g * np.cos((p_t + 1) * np.pi / 4), g * np.sin((p_t + 1) * np.pi / 4)], 1)

    # release the dry layers before the buffer ends (no hard cut into the tail)
    rel = int(0.25 * dur * SR)
    mix[-rel:] *= (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, rel)))[:, None]

    # reverb tail + high-pass to keep it airy
    ir = reverb_ir(tail, rng)
    wet = np.stack([fftconvolve(mix[:, c], ir[:, c])[: n + len(ir) - 1] for c in range(2)], 1)
    dry = np.vstack([mix, np.zeros((len(ir) - 1, 2))])
    y = dry * 0.75 + wet * 0.45
    y = sosfilt(butter(2, 180, btype="high", fs=SR, output="sos"), y, axis=0)
    end = int((dur + tail * 0.6) * SR)
    y = y[:end]
    fo = int(0.4 * SR)
    y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
    y[: int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))[:, None]
    y *= 10 ** (-12 / 20) / np.abs(y).max()
    pcm = (np.clip(y, -1, 1) * (2 ** 23 - 1)).astype("<i4")
    path = os.path.join(OUT, f"lens-flare_{name}.wav")
    with wave.open(path, "wb") as wf:
        wf.setnchannels(2); wf.setsampwidth(3); wf.setframerate(SR)
        wf.writeframes(b"".join(int(v).to_bytes(4, "little", signed=True)[:3] for v in pcm.ravel()))
    print(f"{path}  {len(y) / SR:.2f}s, peak at {peak:.2f}s")


VARIANTS = {
    # name: (dur, peak, seed, kwargs)
    "soft":            (1.8, 0.75, 3, dict(sparkle=0.35, shimmer=0.7, air=1.0, bloom=(400, 4500))),
    "shimmer":         (2.2, 0.85, 5, dict(sparkle=1.0, shimmer=1.0, air=0.8, bloom=(600, 8000))),
    "sweep":           (1.5, 0.60, 9, dict(sparkle=0.6, shimmer=0.6, air=1.2, pan_sweep=(-0.8, 0.8), bloom=(500, 9000), tail=1.6)),
    "glint":           (0.7, 0.10, 21, dict(sparkle=0.9, shimmer=0.5, air=0.5, bloom=(2000, 10000), attack=1.2, decay=0.25, tail=1.0, spark_spread=0.12, spark_hz=(5000, 11000))),
    "sunburst":        (1.2, 0.18, 22, dict(sparkle=1.6, shimmer=1.1, air=1.1, bloom=(800, 11000), attack=1.0, decay=0.45, tail=2.0, spark_spread=0.3)),
    "golden-bloom":    (2.6, 1.10, 23, dict(sparkle=0.15, shimmer=0.9, air=0.9, bloom=(250, 2800), root=0.5, detune=7, low=0.09, tail=2.6)),
    "anamorphic":      (1.8, 0.70, 24, dict(sparkle=0.3, shimmer=0.4, air=0.9, pan_sweep=(-0.9, 0.9), bloom=(700, 7000), glide=(900, 3600, 0.035), tail=1.8)),
    "anamorphic-rtl":  (1.8, 0.70, 25, dict(sparkle=0.3, shimmer=0.4, air=0.9, pan_sweep=(0.9, -0.9), bloom=(700, 7000), glide=(900, 3600, 0.035), tail=1.8)),
    "riser-into-flare": (2.4, 2.00, 26, dict(sparkle=1.0, shimmer=0.8, air=1.1, bloom=(300, 10000), attack=4.0, decay=0.12, glide=(400, 2400, 0.03), tail=2.0, spark_spread=0.06)),
    "dreamy":          (3.5, 1.40, 27, dict(sparkle=0.5, shimmer=1.2, air=0.6, bloom=(500, 5000), detune=12, attack=2.6, decay=0.4, tail=3.0, spark_spread=0.3)),
    "subtle-air":      (2.0, 0.90, 28, dict(sparkle=0.0, shimmer=0.25, air=1.0, bloom=(600, 6000), low=0.0, tail=1.8)),
    "crystal":         (1.6, 0.45, 29, dict(sparkle=1.3, shimmer=1.0, air=0.4, bloom=(3000, 12000), root=2.0, detune=3, tail=2.4, spark_hz=(6000, 13000))),
}
if __name__ == "__main__":
    import sys
    pick = sys.argv[1:] or list(VARIANTS)
    for name in pick:
        dur, peak, seed, kw = VARIANTS[name]
        make(name, dur, peak, seed, **kw)
