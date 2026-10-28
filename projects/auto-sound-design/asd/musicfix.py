"""Smoothing a hard edit in the music (e.g. a section that slams back in).

Two parts, both built from the edit's own audio so they're in key and in tempo:
1. A reverse swell: the first second *after* the cut, drenched in reverb, reversed, so it
   rises into the cut. Written as its own WAV and placed as an editable clip (FCPXML too).
2. A filter sweep (preview only): for a moment after the cut the mix opens from muffled to
   full, so the brightness eases back instead of slamming. In FCP: keyframe an EQ/low-pass
   on the music clip over the same span (the report says when).
"""

from fractions import Fraction
from pathlib import Path

import numpy as np

from . import media
from .placement import Placement, snap

RATE = 48000


def _reverb_ir(seconds=1.8, seed=3):
    rng = np.random.default_rng(seed)
    n = int(seconds * RATE)
    t = np.arange(n) / RATE
    ir = rng.standard_normal((n, 2)) * np.exp(-t / (seconds / 5))[:, None]
    return ir / np.sqrt((ir ** 2).sum(0))


def _convolve(x, ir):
    n = len(x) + len(ir) - 1
    size = 1 << (n - 1).bit_length()
    X = np.fft.rfft(x, size, axis=0)
    H = np.fft.rfft(ir, size, axis=0)
    return np.fft.irfft(X * H, size, axis=0)[:n]


def reverse_swell(video_path, cut_time_abs, out_path, length=1.4, grab=1.0):
    """WAV that swells up to the cut. cut_time_abs is in the full video's seconds."""
    after = media.decode_audio(video_path, rate=RATE, channels=2, start=cut_time_abs, duration=grab)
    wet = _convolve(after, _reverb_ir())
    swell = wet[::-1][-int(length * RATE):].copy()
    ramp = np.linspace(0, 1, len(swell)) ** 2  # slow start, fast arrival
    swell *= ramp[:, None]
    swell[-int(0.01 * RATE):] *= np.linspace(1, 0, int(0.01 * RATE))[:, None]  # no click at the cut
    swell /= np.abs(swell).max() + 1e-12
    media.write_wav(out_path, (swell * 10 ** (-3 / 20)).astype(np.float32))
    return out_path


def filter_sweep(source, cut_time, seconds=0.7, start_hz=900):
    """Preview-only: blend from a low-passed copy to the original over `seconds` after the cut.
    `source` is the section's audio (samples, 2); cut_time is relative to the section."""
    a = int(cut_time * RATE)
    b = min(len(source), a + int(seconds * RATE))
    if b <= a:
        return source
    seg = source[a:b]
    spec = np.fft.rfft(seg, axis=0)
    f = np.fft.rfftfreq(len(seg), 1 / RATE)
    spec[f > start_hz] *= (start_hz / f[f > start_hz])[:, None] ** 2  # gentle 12 dB/oct slope
    dull = np.fft.irfft(spec, len(seg), axis=0)
    w = np.linspace(0, 1, len(seg))[:, None] ** 1.5
    out = source.copy()
    out[a:b] = dull * (1 - w) + seg * w
    return out


def plan(fixes, video, window_start, seconds, out_dir, music_level_at):
    """Build placements for the swells; return (placements, sweep_times, notes)."""
    placements, sweeps, notes = [], [], []
    gen = Path(out_dir) / "fx_generated"
    for fx in fixes:
        if fx.get("type") != "smooth_cut":
            continue
        t_abs = float(fx["time"])
        t = t_abs - window_start
        if not (1.5 <= t <= seconds - 0.5):
            continue
        gen.mkdir(exist_ok=True)
        length = float(fx.get("swell_s", 1.4))
        path = reverse_swell(video.path, t_abs, gen / f"reverse_swell_{t_abs:.2f}s.wav", length=length)
        fd = video.frame_duration
        offset = snap(t - length, fd)
        dur = snap(length, fd, "floor")
        # Pitch the swell against the louder side of the cut (the music it's leading into).
        gain = max(music_level_at(t - 0.5), music_level_at(t + 0.7)) - 1 - (-3)
        placements.append(Placement(
            id="fix", category="riser", event_time=round(t, 4), offset=offset, duration=dur,
            source=str(path), source_name=f"fx_generated/{path.name}", gain_db=round(max(-30, min(6, gain)), 2),
            fade_in=0.3, fade_out=0.01, confidence=0.6,
            reason=f"smooths the hard music cut at {t_abs:.2f}s: reverse swell built from the incoming music ({fx.get('why', '')})",
            align="peak", notes=["generated from the edit's own audio"]))
        sweeps.append(t)
        notes.append(f"Music cut at {t_abs:.2f}s: reverse swell clip + {fx.get('sweep_s', 0.7)}s filter sweep "
                     f"(preview only; in FCP keyframe a low-pass on the music from {t_abs:.2f}s to {t_abs + 0.7:.2f}s)")
    return placements, sweeps, notes
