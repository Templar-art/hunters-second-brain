"""Picture and music analysis. Everything here is signal-level: cut scores, loudness and
onsets. None of it knows what a shot depicts (drone, room reveal, twilight) and nothing
downstream should claim it does."""

from dataclasses import dataclass, field

import numpy as np

from . import media

SR = 22050
HOP = 512
NFFT = 2048


@dataclass
class Cut:
    time: float  # first frame of the new shot, seconds from the start of the video
    frame: int
    score: float  # FFmpeg scene score, 0..1
    motion: float = 0.0  # motion blur around the cut, 0..1 (whip pans, fast moves)


@dataclass
class MusicAnalysis:
    available: bool
    source: str = ""
    hop_s: float = HOP / SR
    rms_db: np.ndarray = field(default_factory=lambda: np.zeros(0))
    onset_env: np.ndarray = field(default_factory=lambda: np.zeros(0))
    onsets: list = field(default_factory=list)  # [(time, strength 0..1)]
    energy_rises: list = field(default_factory=list)  # [(time, rise_db)]
    tempo_bpm: float = 0.0
    tempo_confidence: float = 0.0
    beats: list = field(default_factory=list)
    beats_reliable: bool = False

    def level_at(self, t, window=1.0):
        """Mean RMS (dBFS) of the music in t±window; -20 dBFS if there's no audio to read."""
        if not self.available or len(self.rms_db) == 0:
            return -20.0
        a = max(0, int((t - window) / self.hop_s))
        b = min(len(self.rms_db), int((t + window) / self.hop_s) + 1)
        if b <= a:
            return float(np.median(self.rms_db))
        power = np.mean(10 ** (self.rms_db[a:b] / 10))
        return float(10 * np.log10(power + 1e-12))


def detect_cuts(video, cfg, limit=None, start=None):
    """Hard cuts from FFmpeg scene scores, kept only where they're a local peak above threshold.
    Dissolves and slow fades score low and are mostly missed; that's a known limit."""
    times, scores = media.scene_scores(video.path, duration=limit, start=start)
    if len(scores) == 0:
        return []
    threshold = cfg["cut_threshold"]
    floor = cfg["cut_min_score"]
    prominence = cfg["cut_prominence"]
    min_shot = cfg["min_shot_s"]
    radius = 3
    fps = float(video.fps)
    cuts = []
    for i, score in enumerate(scores):
        if score < floor or times[i] < min_shot:
            continue
        window = scores[max(0, i - radius): i + radius + 1]
        if score < window.max():
            continue
        # Similar-looking rooms cut together score low; accept them if they stand well clear
        # of the frames around them (camera moves score a steady low, a cut spikes).
        around = np.concatenate([scores[max(0, i - 12): i], scores[i + 1: i + 13]])
        local = float(np.median(around)) if len(around) else 0.0
        if score < threshold and score < prominence * (local + 0.01):
            continue
        if cuts and times[i] - cuts[-1].time < min_shot:
            if score > cuts[-1].score:
                cuts[-1] = Cut(float(times[i]), int(round(times[i] * fps)), float(score))
            continue
        cuts.append(Cut(float(times[i]), int(round(times[i] * fps)), float(score)))
    return cuts


def _frames(signal):
    pad = NFFT // 2
    signal = np.pad(signal, (pad, pad))
    count = 1 + (len(signal) - NFFT) // HOP
    idx = np.arange(NFFT)[None, :] + HOP * np.arange(count)[:, None]
    return signal[idx]


def _peaks(env, min_gap, threshold):
    """Indices of local maxima above threshold, at least min_gap hops apart (strongest wins)."""
    candidates = [i for i in range(1, len(env) - 1) if env[i] >= threshold and env[i] >= env[i - 1] and env[i] > env[i + 1]]
    candidates.sort(key=lambda i: -env[i])
    kept = []
    for i in candidates:
        if all(abs(i - k) >= min_gap for k in kept):
            kept.append(i)
    return sorted(kept)


def _smooth(x, n):
    if n <= 1:
        return x
    kernel = np.ones(n) / n
    return np.convolve(np.pad(x, (n // 2, n - 1 - n // 2), mode="edge"), kernel, mode="valid")


def estimate_tempo(onset_env, hop_s):
    """Autocorrelation tempo in 60-180 BPM. Returns (bpm, confidence 0..1, period in hops)."""
    env = onset_env - onset_env.mean()
    if len(env) < 4 or not np.any(env):
        return 0.0, 0.0, 0
    ac = np.correlate(env, env, mode="full")[len(env) - 1:]
    ac /= ac[0] + 1e-12
    lo = int(round(60 / 180 / hop_s))
    hi = min(len(ac) - 1, int(round(60 / 60 / hop_s)))
    if hi <= lo:
        return 0.0, 0.0, 0
    lags = np.arange(lo, hi + 1)
    bpms = 60 / (lags * hop_s)
    prior = np.exp(-0.5 * (np.log2(bpms / 120) / 0.9) ** 2)  # mild preference for ~120 BPM
    weighted = ac[lo: hi + 1] * prior
    k = int(np.argmax(weighted))
    best = lags[k]
    confidence = float(np.clip(ac[best], 0, 1))
    # Parabolic interpolation: the true period usually falls between two whole hops.
    refined = float(best)
    if 0 < k < len(weighted) - 1:
        a, b, c = weighted[k - 1], weighted[k], weighted[k + 1]
        denom = a - 2 * b + c
        if denom:
            refined = best + 0.5 * (a - c) / denom
    return float(60 / (refined * hop_s)), confidence, int(best)


def analyse_music(path, cfg, limit=None, label="", start=None):
    try:
        samples = media.decode_audio(path, rate=SR, channels=1, start=start, duration=limit)[:, 0]
    except media.MediaError:
        return MusicAnalysis(available=False, source=label)
    if len(samples) < SR:
        return MusicAnalysis(available=False, source=label)
    frames = _frames(samples)
    rms = np.sqrt(np.mean(frames ** 2, axis=1))
    rms_db = 20 * np.log10(rms + 1e-9)
    spec = np.abs(np.fft.rfft(frames * np.hanning(NFFT), axis=1))
    logspec = np.log1p(100 * spec)
    flux = np.maximum(0, np.diff(logspec, axis=0)).sum(axis=1)
    flux = np.concatenate([[0], flux])
    onset_env = flux / (flux.max() + 1e-12)
    hop_s = HOP / SR

    threshold = onset_env.mean() + cfg["onset_sigma"] * onset_env.std()
    onset_idx = _peaks(onset_env, max(1, int(0.25 / hop_s)), threshold)
    onsets = [(i * hop_s, float(onset_env[i])) for i in onset_idx]

    # Energy rise: loudness over the next window vs the previous one (catches drops/builds).
    win = max(1, int(cfg["energy_window_s"] / hop_s))
    smooth_db = _smooth(rms_db, max(1, int(0.25 / hop_s)))
    rise = np.zeros_like(smooth_db)
    cs = np.concatenate([[0.0], np.cumsum(10 ** (smooth_db / 10))])
    i = np.arange(win, len(smooth_db) - win)
    if len(i):
        after = (cs[i + win] - cs[i]) / win
        before = (cs[i] - cs[i - win]) / win
        rise[i] = 10 * np.log10(after / before)
    rise_idx = _peaks(rise, max(1, int(cfg["energy_min_gap_s"] / hop_s)), cfg["energy_rise_db"])
    # A rise is "at" its sharpest onset nearby, not the centre of a 1.5 s window.
    energy_rises = []
    loud_floor = float(np.median(rms_db)) - 3
    for i in rise_idx:
        after_db = 10 * np.log10((cs[min(len(smooth_db), i + win)] - cs[i]) / win + 1e-12)
        if after_db < loud_floor or i * hop_s < cfg["min_shot_s"]:
            continue  # a fade-in from silence or a rise into a quiet passage isn't a "hit"
        a, b = max(0, i - int(0.4 / hop_s)), min(len(onset_env), i + int(0.4 / hop_s))
        j = a + int(np.argmax(onset_env[a:b]))
        energy_rises.append((j * hop_s, float(rise[i])))

    bpm, conf, period = estimate_tempo(onset_env, hop_s)
    beats = []
    reliable = conf >= cfg["beat_confidence"] and period > 0
    if reliable:
        phases = [onset_env[p::period].sum() for p in range(period)]
        phase = int(np.argmax(phases))
        radius = max(1, period // 10)
        for k in range(phase, len(onset_env), period):
            a, b = max(0, k - radius), min(len(onset_env), k + radius + 1)
            beats.append((a + int(np.argmax(onset_env[a:b]))) * hop_s)

    return MusicAnalysis(
        available=True,
        source=label,
        hop_s=hop_s,
        rms_db=rms_db,
        onset_env=onset_env,
        onsets=onsets,
        energy_rises=energy_rises,
        tempo_bpm=round(bpm, 1),
        tempo_confidence=round(conf, 3),
        beats=beats,
        beats_reliable=reliable,
    )


def existing_sfx(path, cuts, cfg, start=None, limit=None):
    """Effects that look already baked into the edit's audio, checked at each cut:
    a whoosh shows as a jump in high-frequency noise just before the cut; a boom as a jump in
    sub-bass right after it. Signal heuristics only: a crash cymbal on the cut can read as a
    whoosh too, which is fine, since it also means the cut already has a sound on it."""
    sr = SR
    try:
        a = media.decode_audio(path, rate=sr, channels=1, start=start, duration=limit)[:, 0]
    except media.MediaError:
        return []
    hop, nfft = 441, 1024  # 20 ms hops
    if len(a) < nfft * 4:
        return []
    # A near-silent track (an edit exported before the music went in) has no effects to keep clear of;
    # the dB rises below would just be noise-floor jitter.
    if np.abs(a).max() < 10 ** (-30 / 20):
        return []
    frames = np.lib.stride_tricks.sliding_window_view(np.pad(a, (nfft // 2, nfft // 2)), nfft)[::hop]
    spec = np.abs(np.fft.rfft(frames * np.hanning(nfft), axis=1)) + 1e-9
    f = np.fft.rfftfreq(nfft, 1 / sr)
    hf = 20 * np.log10(spec[:, f > 5000].mean(1))
    sub = 20 * np.log10(spec[:, f < 90].mean(1))
    mid = spec[:, (f > 200) & (f < 10000)]
    flat = np.exp(np.log(mid).mean(1)) / mid.mean(1)

    def mean(x, t0, t1):
        i, j = max(0, int(t0 / 0.02)), max(1, int(t1 / 0.02))
        return float(x[i:max(i + 1, j)].mean())

    found = []
    for c in cuts:
        t = c.time
        hf_rise = mean(hf, t - 0.35, t + 0.05) - mean(hf, t - 1.5, t - 0.6)
        flat_rise = mean(flat, t - 0.35, t + 0.05) - mean(flat, t - 1.5, t - 0.6)
        sub_hit = mean(sub, t, t + 0.25) - mean(sub, t - 0.6, t - 0.1)
        if hf_rise >= cfg["existing_whoosh_hf_db"] and flat_rise >= cfg["existing_whoosh_flatness"]:
            found.append({"time": t, "kind": "whoosh", "evidence": f"high-frequency noise up {hf_rise:.1f} dB into the cut"})
        i0 = max(0, int(t / 0.02))
        peak_now = float(sub[i0: i0 + 13].max()) if i0 < len(sub) else -200.0
        later = sub[i0 + 15: i0 + 100]
        peak_later = float(later.max()) if len(later) else -200.0
        # A boom is a one-off; kicks in the music come back at the same weight within a couple of seconds.
        if sub_hit >= cfg["existing_boom_sub_db"] and peak_now - peak_later >= 6:
            found.append({"time": t, "kind": "boom", "evidence": f"sub-bass up {sub_hit:.1f} dB on the cut"})
    return found


def cut_motion(path, cuts, fps, start=None, width=160):
    """Motion blur around each cut, 0..1. Whip pans and fast drone moves smear the frames either
    side of the cut; a static shot doesn't. 1 - (sharpness near the cut / sharpness ~1 s away)."""
    out = {}
    fps = float(fps)
    for c in cuts:
        t = c.time + (start or 0.0)
        a = max(0.0, t - 1.0)
        cmd = ["ffmpeg", "-v", "error", "-nostdin", "-ss", f"{a:.3f}", "-i", str(path), "-t", "2.0",
               "-vf", f"scale={width}:-2,format=gray", "-f", "rawvideo", "-"]
        try:
            raw = media._run(cmd, binary=True)
        except media.MediaError:
            continue
        h = None
        for cand in range(60, 200):
            if len(raw) % (width * cand) == 0 and (len(raw) // (width * cand)) >= 4:
                h = cand
                break
        if h is None:
            continue
        frames = np.frombuffer(raw, np.uint8).reshape(-1, h, width).astype(np.float32)
        sharp = np.array([np.abs(np.diff(f, axis=0)).mean() + np.abs(np.diff(f, axis=1)).mean() for f in frames])
        n = len(sharp)
        centre = int(round((t - a) * fps))
        near = sharp[max(0, centre - 3): centre + 3]
        far = np.concatenate([sharp[: max(1, centre - 12)], sharp[min(n - 1, centre + 12):]])
        if len(near) == 0 or len(far) == 0:
            continue
        out[round(c.time, 4)] = float(np.clip(1 - near.min() / (np.median(far) + 1e-6), 0, 1))
    return out
