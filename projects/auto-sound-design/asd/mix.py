"""Render the effects bus and a preview mix. Source files are only ever read."""

import numpy as np

from . import media

RATE = 48000


def _ramp(length):
    return np.linspace(0.0, 1.0, max(1, length), dtype=np.float32)


def render_clips(placements):
    """Each effect at unity gain with its fades, as (start_sample, samples). Gain is applied later
    so the clipping check can turn individual effects down without re-decoding."""
    clips = []
    for p in placements:
        audio = media.decode_audio(p.source, rate=RATE, channels=2)
        n = min(len(audio), int(round(float(p.duration) * RATE)))
        clip = audio[:n].copy()
        fi = min(n, int(p.fade_in * RATE))
        fo = min(n, int(p.fade_out * RATE))
        if fi:
            clip[:fi] *= _ramp(fi)[:, None]
        if fo:
            clip[n - fo:] *= _ramp(fo)[::-1, None]
        clips.append((int(round(float(p.offset) * RATE)), clip))
    return clips


def mix_bus(placements, clips, total_seconds):
    total = int(round(total_seconds * RATE))
    bus = np.zeros((total, 2), dtype=np.float32)
    for p, (start, clip) in zip(placements, clips):
        end = min(total, start + len(clip))
        if end > start:
            bus[start:end] += clip[: end - start] * np.float32(10 ** (p.gain_db / 20))
    return bus


def db(x):
    return float(20 * np.log10(max(float(x), 1e-9)))


def balance(placements, clips, total_seconds, source, cfg):
    """Clipping check. Turns down only the effects that sit on an over-ceiling moment, 0.5 dB at a
    time and at most max_bus_trim_db each; the source audio is never changed. If the source alone
    is too hot, the preview file (only) gets an overall gain cut. Returns (bus, preview_gain_db, report)."""
    ceiling = cfg["mix"]["ceiling_dbfs"]
    max_trim = cfg["mix"]["max_bus_trim_db"]
    lin_ceiling = 10 ** (ceiling / 20)
    original = {p.id: p.gain_db for p in placements}
    report = {"ceiling_dbfs": ceiling}
    bus = mix_bus(placements, clips, total_seconds)
    report["sfx_bus_peak_dbfs_before"] = round(db(np.abs(bus).max()) if len(bus) else -120, 2)
    src = None
    if source is not None:
        n = min(len(bus), len(source))
        src = np.zeros_like(bus)
        src[:n] = source[:n]
        report["source_peak_dbfs"] = round(db(np.abs(src).max()), 2)
        if report["source_peak_dbfs"] > ceiling:
            report["source_note"] = "The source audio itself peaks above the ceiling; that is left as-is."
    for _ in range(int(max_trim / 0.5) + 1):
        total = bus if src is None else bus + src
        hot = np.abs(total).max(axis=1) > lin_ceiling
        if src is not None:
            hot &= np.abs(src).max(axis=1) <= lin_ceiling  # where the source alone is over, effects aren't the cause
        over = np.nonzero(hot)[0]
        if len(over) == 0:
            break
        changed = False
        for p, (start, clip) in zip(placements, clips):
            if original[p.id] - p.gain_db >= max_trim - 1e-6:
                continue
            hit = np.any((over >= start) & (over < start + len(clip)))
            if hit:
                p.gain_db = round(p.gain_db - 0.5, 2)
                changed = True
        if not changed:
            break
        bus = mix_bus(placements, clips, total_seconds)
    trimmed = {p.id: round(p.gain_db - original[p.id], 2) for p in placements if p.gain_db != original[p.id]}
    for p in placements:
        if p.id in trimmed:
            p.notes.append(f"turned down {-trimmed[p.id]:.1f} dB by the clipping check")
    total = bus if src is None else bus + src
    peak = db(np.abs(total).max()) if len(total) else -120
    preview_gain = min(0.0, ceiling - peak)
    report.update({
        "sfx_bus_peak_dbfs": round(db(np.abs(bus).max()) if len(bus) else -120, 2),
        "effects_turned_down_db": trimmed,
        "mix_peak_dbfs": round(peak, 2),
        "preview_output_gain_db": round(preview_gain, 2),
    })
    if preview_gain < 0:
        report["warning"] = (
            f"Source audio + effects still peak at {peak:.2f} dBFS after turning effects down; the preview "
            f"file is turned down {-preview_gain:.2f} dB overall. Your source file is unchanged. In FCP, pull the "
            f"music down ~{-preview_gain:.0f}-{-preview_gain + 1:.0f} dB under the effects, or limit the master."
        )
    return bus, preview_gain, report
