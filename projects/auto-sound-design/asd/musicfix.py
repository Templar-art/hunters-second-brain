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


# --- v2: seamless return from a filtered section (rebuild + 1-bar opening) -------------------

def _stft(x, n=2048, hop=512):
    win = np.hanning(n)
    pad = np.pad(x, ((n, n), (0, 0)))
    frames = np.lib.stride_tricks.sliding_window_view(pad, n, axis=0)[::hop]  # (frames, ch, n)
    return np.fft.rfft(frames * win, axis=-1), len(x)


def _istft(spec, length, n=2048, hop=512):
    win = np.hanning(n)
    frames = np.fft.irfft(spec, n, axis=-1) * win  # (frames, ch, n)
    out = np.zeros((length + 2 * n, frames.shape[1]))
    norm = np.zeros(length + 2 * n)
    for i in range(frames.shape[0]):
        out[i * hop: i * hop + n] += frames[i].T
        norm[i * hop: i * hop + n] += win ** 2
    out /= np.maximum(norm, 1e-8)[:, None]
    return out[n: n + length]


def _band_curve(a, b, n=2048):
    """Per-bin dB difference between two audio spans' average spectra (b relative to a), smoothed."""
    def avg(x):
        spec, _ = _stft(x, n)
        return 10 * np.log10((np.abs(spec) ** 2).mean(axis=(0, 1)) + 1e-12)
    diff = avg(b) - avg(a)
    k = 15
    return np.convolve(np.pad(diff, (k, k), mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), mode="valid")


def seamless_return(source, section_start, cut, bpm, open_bars=1.0, n=2048, hop=512):
    """`source` is the full section's audio (samples, 2) at RATE; times are relative to it.
    Rebuilds [section_start, cut] from the music *after* the cut, shifted back a whole number of
    bars (so its beat grid continues straight through the cut), muffled to match the original
    filtered section, then opens the filter + level back up over `open_bars` after the cut.
    Returns (new_source, (seg_start, seg_end), report)."""
    bar = 4 * 60.0 / bpm
    length = cut - section_start
    shift_bars = int(np.ceil(length / bar))
    shift = shift_bars * bar
    s0, c = int(section_start * RATE), int(cut * RATE)
    src_a, src_b = int((section_start + shift) * RATE), int((cut + shift) * RATE)
    open_len = open_bars * bar
    o_end = int((cut + open_len) * RATE)
    if src_b > len(source) or o_end > len(source):
        raise ValueError("not enough music after the cut to rebuild the section")
    # How the original section is muffled relative to the music after the cut.
    muffled = source[s0 + int(0.3 * RATE): c - int(0.1 * RATE)]
    open_music = source[c + int(0.2 * RATE): c + int(min(4.0, shift) * RATE)]
    curve_db = np.clip(_band_curve(open_music, muffled, n), -48, 6)
    gain_curve = 10 ** (curve_db / 20)
    # 1. Rebuilt section, muffled to match.
    rebuilt_spec, ln = _stft(source[src_a:src_b], n, hop)
    rebuilt = _istft(rebuilt_spec * gain_curve[None, None, :], ln, n, hop)
    # The curve matches tone; match level separately to the original muffled section.
    rms = lambda x: np.sqrt(np.mean(x ** 2)) + 1e-12  # noqa: E731
    rebuilt *= rms(muffled) / rms(rebuilt[int(0.3 * RATE): c - s0 - int(0.1 * RATE)])
    # ...and the opening must start from that same level, so scale the curve's overall offset too.
    level_fix = rms(muffled) / (rms(_istft(_stft(open_music, n, hop)[0] * gain_curve[None, None, :], len(open_music), n, hop)))
    gain_curve = gain_curve * level_fix
    # 2. Opening: from the muffled curve to flat over one bar, eased.
    seg = source[c:o_end]
    spec, ln2 = _stft(seg, n, hop)
    frames = spec.shape[0]
    t = np.clip((np.arange(frames) * hop - n) / max(1, ln2), 0, 1)
    ease = (1 - np.cos(np.pi * t)) / 2  # smooth S
    gains = gain_curve[None, :] ** (1 - ease[:, None])
    opened = _istft(spec * gains[:, None, :], ln2, n, hop)
    out = source.copy()
    # Hand over to the rebuilt (re-gridded) music deep inside the muffled section, where it's
    # quietest and softest, so the grid change hides there instead of at the cut. Long blend.
    hand = section_start + (bar if length > 1.5 * bar else length / 3)
    h0 = int(hand * RATE)
    xf = int(min(0.5, (cut - hand) / 2) * RATE)
    ramp = ((1 - np.cos(np.linspace(0, np.pi, xf))) / 2)[:, None]
    out[h0:h0 + xf] = source[h0:h0 + xf] * (1 - ramp) + rebuilt[h0 - s0: h0 - s0 + xf] * ramp
    out[h0 + xf:c] = rebuilt[h0 - s0 + xf: c - s0]
    out[c:o_end] = opened
    report = {"bar_s": round(bar, 4), "rebuilt_from_s": [round(section_start + shift, 3), round(cut + shift, 3)],
              "shift_bars": shift_bars, "opening_s": round(open_len, 3),
              "muffle_db_by_band": {f"{lo}-{hi}Hz": round(float(np.mean(curve_db[(np.fft.rfftfreq(n, 1 / RATE) >= lo) &
                                                                                   (np.fft.rfftfreq(n, 1 / RATE) < hi)])), 1)
                                    for lo, hi in [(40, 400), (400, 2000), (2000, 8000), (8000, 16000)]}}
    report["handover_s"] = round(hand, 3)
    return out, (hand, cut + open_len), report
