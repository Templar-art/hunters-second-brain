"""Synthetic test media: a 20 s, 24 fps video with known cuts over a 120 BPM track that
jumps in energy at 12 s, plus a small SFX library in a folder whose name has spaces.
Everything is generated, so tests don't depend on Hunter's footage."""

import subprocess
from pathlib import Path

import numpy as np

RATE = 48000
FPS = 24  # 0.5 s kicks land on whole frames
DURATION = 20.0
CUTS = [3.0, 6.0, 9.5, 12.0, 16.5]  # every cut sits on a kick (kicks every 0.5 s)
ENERGY_JUMP = 12.0
COLOURS = ["0x203040", "0xd0b080", "0x305030", "0xe0e0f0", "0x402060", "0xf0c040"]


def _wav(path, samples):
    samples = np.ascontiguousarray(samples, dtype="<f4")
    if samples.ndim == 1:
        samples = np.stack([samples, samples], axis=1)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(RATE), "-ac", "2", "-i", "-",
                    "-c:a", "pcm_s16le", str(path)], input=samples.tobytes(), check=True)


def music(duration=DURATION, seed=1):
    rng = np.random.default_rng(seed)
    n = int(duration * RATE)
    t = np.arange(n) / RATE
    pad = 0.05 * np.sin(2 * np.pi * 110 * t) + 0.03 * np.sin(2 * np.pi * 165 * t)
    out = pad.copy()
    for k in np.arange(0, duration, 0.5):
        i = int(k * RATE)
        m = min(n - i, int(0.25 * RATE))
        env = np.exp(-np.arange(m) / (0.04 * RATE))
        loud = 0.7 if k >= ENERGY_JUMP else 0.12
        kick = loud * env * np.sin(2 * np.pi * 55 * np.arange(m) / RATE)
        kick[: int(0.004 * RATE)] += loud * 0.5 * rng.standard_normal(int(0.004 * RATE))
        out[i: i + m] += kick
    out[int(ENERGY_JUMP * RATE):] += 0.08 * rng.standard_normal(n - int(ENERGY_JUMP * RATE))
    return np.clip(out, -0.7, 0.7)


def video(path, duration=DURATION):
    audio = Path(path).with_suffix(".music.wav")
    _wav(audio, music(duration))
    edges = [0.0] + [c for c in CUTS if c < duration] + [duration]
    inputs, chains = [], []
    for i in range(len(edges) - 1):
        inputs += ["-f", "lavfi", "-i", f"color=c={COLOURS[i % len(COLOURS)]}:s=640x360:r={FPS}:d={edges[i + 1] - edges[i]:.3f}"]
        chains.append(f"[{i}:v]")
    graph = "".join(chains) + f"concat=n={len(chains)}:v=1:a=0[v]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-i", str(audio), "-filter_complex", graph,
                    "-map", "[v]", "-map", f"{len(chains)}:a", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-g", "1",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", str(path)], check=True)
    audio.unlink()
    return Path(path)


def sfx_library(root):
    root = Path(root)
    (root / "Ambience").mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(2)

    def noise(sec):
        return rng.standard_normal(int(sec * RATE))

    def t(sec):
        return np.arange(int(sec * RATE)) / RATE

    def bandish(x, k=8):
        return np.convolve(x, np.ones(k) / k, mode="same")

    for name, sec, peak in (("whoosh soft 01.wav", 1.0, 0.6), ("whoosh fast 02.wav", 0.6, 0.35), ("Whoosh Air 03.wav", 1.4, 0.9)):
        tt = t(sec)
        env = np.exp(-((tt - peak) / (sec / 6)) ** 2)
        _wav(root / name, 0.5 * env * bandish(noise(sec)))
    tt = t(2.0)
    _wav(root / "impact boom 01.wav", 0.8 * np.exp(-tt / 0.35) * np.sin(2 * np.pi * 48 * tt) + 0.3 * np.exp(-tt / 0.01) * noise(2.0))
    tt = t(4.0)
    _wav(root / "riser tension 01.wav", 0.5 * (tt / 4.0) ** 2 * np.sin(2 * np.pi * (200 + 300 * tt) * tt))
    tt = t(2.5)
    _wav(root / "shimmer chime 01.wav", 0.3 * np.exp(-tt / 0.6) * (np.sin(2 * np.pi * 1760 * tt) + np.sin(2 * np.pi * 2637 * tt)))
    _wav(root / "Ambience" / "forest birds 01.wav", 0.05 * bandish(noise(12.0), 3))
    _wav(root / "Mystery Take 7.wav", 0.2 * noise(1.0) * np.exp(-t(1.0) / 0.2))
    (root / "Mystery Take 7.wav.tags").write_text("impact, metal, hit")
    _wav(root / "Weird Thing.wav", 0.1 * noise(0.5))
    return root
