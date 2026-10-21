"""Metallic "shinggggg" SFX: a sword-draw / sun-glint ring (procedural, original, royalty-free).

  python3 projects/sfx-custom/shing.py [name ...]   -> out/shing_{name}.wav

"Sh" = a short bright noise scrape sweeping upward (the blade sliding out / the glint striking).
"Ing" = modal ringing of a thin steel blade: inharmonic partials, each a detuned pair so they beat
(that wobbling "nggggg"), higher partials dying faster, a tiny upward pitch flick on the strike.
Shares the reverb / pan / band-pass helpers with lens_flare.py. 48 kHz / 24-bit stereo, -12 dBFS.
"""
import os, wave
import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt
from lens_flare import SR, OUT, sweep_band, reverb_ir

BLADE = [1.0, 1.506, 2.368, 2.837, 3.792, 4.553, 5.921]  # inharmonic steel-plate ratios (no clean octaves)


def make(name, f0, ring, seed, scrape=1.0, scrape_len=0.09, beat=(1.5, 5.0), flick=0.03, bright=1.0,
         pan_sweep=(0.0, 0.0), tail=1.8, dur=None, sparkle=0.0):
    """f0: lowest blade mode (Hz). ring: decay of f0 in seconds (the length of the "ngggg").
    beat: detune range (Hz) between each partial's pair, faster beating = more shimmer.
    flick: upward pitch bend on the strike (fraction). bright: tilt toward the upper partials."""
    rng = np.random.default_rng(seed)
    dur = dur or ring * 2.2
    n = int(dur * SR)
    t = np.arange(n) / SR
    mix = np.zeros((n, 2))
    p_t = np.interp(t, [0, dur * 0.6], pan_sweep)
    gl, gr = np.cos((p_t + 1) * np.pi / 4), np.sin((p_t + 1) * np.pi / 4)

    # "sh": noise scrape sweeping upward, 6 ms attack, starts just before the ring
    s0 = int(0.0 * SR)
    m = int(scrape_len * SR * 2.5)
    sc = sweep_band(rng.standard_normal(m), 2500, 12000, bands=10)
    tt = np.arange(m) / SR
    sc *= np.clip(tt / 0.006, 0, 1) ** 2 * np.exp(-np.clip(tt - scrape_len * 0.5, 0, None) / (scrape_len * 0.45))
    sc *= scrape * 0.5 / (np.abs(sc).max() + 1e-9)
    mix[s0:s0 + m, 0] += sc * gl[s0:s0 + m]
    mix[s0:s0 + m, 1] += sc * gr[s0:s0 + m]

    # "ing": blade modes
    on = int(scrape_len * 0.35 * SR)  # ring catches a beat into the scrape
    te = np.clip(t - on / SR, 0, None)
    bend = 1 - flick * np.exp(-te / 0.035)  # starts a touch flat, snaps up to pitch
    att = np.clip(te / 0.002, 0, 1) * (t >= on / SR)
    ring_sig = np.zeros((n, 2))
    for k, r in enumerate(BLADE):
        f = f0 * r
        if f > 17000:
            continue
        amp = (1 / (1 + k * 0.55)) * (r ** (0.35 * (bright - 1)))
        tau = ring * (1 / r) ** 0.55
        d = rng.uniform(*beat)
        for side, det in ((0, -d / 2), (1, d / 2)):  # pair split across L/R -> wide, wobbling ring
            ph = 2 * np.pi * np.cumsum(f * bend + det) / SR + rng.uniform(0, 2 * np.pi)
            ring_sig[:, side] += np.sin(ph) * amp * np.exp(-te / tau)
            ring_sig[:, 1 - side] += np.sin(ph) * amp * np.exp(-te / tau) * 0.45
    ring_sig *= att[:, None] * 0.12
    mix += ring_sig * np.stack([gl, gr], 1) * np.sqrt(2)

    # optional sparkle dust on the strike (glint flavour)
    for _ in range(int(14 * sparkle)):
        t0 = on / SR + abs(rng.normal(0, 0.12))
        f = rng.uniform(6000, 12000)
        mm = int(0.06 * SR); u = np.arange(mm) / SR
        ping = np.sin(2 * np.pi * f * u) * np.exp(-u / 0.02) * np.clip(u / 0.004, 0, 1) ** 2 * rng.uniform(0.2, 0.5) * 0.08
        i = int(t0 * SR); pp = rng.uniform(-0.8, 0.8)
        seg = ping[: max(0, n - i)]
        mix[i:i + len(seg), 0] += seg * np.cos((pp + 1) * np.pi / 4)
        mix[i:i + len(seg), 1] += seg * np.sin((pp + 1) * np.pi / 4)

    # fade the dry ring out before the buffer ends, then a bright reverb
    rel = int(0.2 * dur * SR)
    mix[-rel:] *= (0.5 + 0.5 * np.cos(np.linspace(0, np.pi, rel)))[:, None]
    ir = reverb_ir(tail, rng, damp=9000)
    wet = np.stack([fftconvolve(mix[:, c], ir[:, c]) for c in range(2)], 1)
    dry = np.vstack([mix, np.zeros((len(ir) - 1, 2))])
    y = dry * 0.85 + wet * 0.3
    y = sosfilt(butter(2, 400, btype="high", fs=SR, output="sos"), y, axis=0)
    y = y[: int((dur + tail * 0.5) * SR)]
    fo = int(0.35 * SR)
    y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
    y *= 10 ** (-12 / 20) / np.abs(y).max()
    pcm = (np.clip(y, -1, 1) * (2 ** 23 - 1)).astype("<i4")
    path = os.path.join(OUT, f"shing_{name}.wav")
    with wave.open(path, "wb") as wf:
        wf.setnchannels(2); wf.setsampwidth(3); wf.setframerate(SR)
        wf.writeframes(b"".join(int(v).to_bytes(4, "little", signed=True)[:3] for v in pcm.ravel()))
    print(f"{path}  {len(y) / SR:.2f}s")


VARIANTS = {
    # name: (f0, ring, seed, kwargs)
    "classic":     (2350, 1.4, 41, dict()),                                          # the textbook sword "shinggg"
    "long":        (2100, 2.6, 42, dict(beat=(1.0, 3.5), tail=2.4)),                 # holds the "ngggggg"
    "bright":      (3100, 1.2, 43, dict(bright=1.6, sparkle=0.6)),                   # higher, sun-glint sharp
    "glint":       (3600, 0.6, 44, dict(scrape=0.6, scrape_len=0.05, sparkle=1.0, tail=1.2)),  # short twinkle-shing
    "heavy":       (1500, 1.8, 45, dict(scrape=1.3, scrape_len=0.14, beat=(0.8, 2.5))),        # bigger blade, deeper
    "wobble":      (2400, 1.8, 46, dict(beat=(4.0, 9.0))),                           # fast shimmer in the ring
    "sweep-lr":    (2500, 1.5, 47, dict(pan_sweep=(-0.8, 0.8), sparkle=0.4)),        # glint travels left to right
    "sweep-rl":    (2500, 1.5, 48, dict(pan_sweep=(0.8, -0.8), sparkle=0.4)),
    "clean":       (2700, 1.6, 49, dict(scrape=0.25, flick=0.0, beat=(0.6, 1.6))),   # almost pure ring, little "sh"
}
if __name__ == "__main__":
    import sys
    for name in sys.argv[1:] or list(VARIANTS):
        f0, ring, seed, kw = VARIANTS[name]
        make(name, f0, ring, seed, **kw)
