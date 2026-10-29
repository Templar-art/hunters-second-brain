"""Wing-flap SFX for a rendered plate-vfx bird job, synced to the CG gulls.

Re-runs the same flight simulation the render used (lib/flight.py, layout.json + camera.json), finds each
wing downstroke, and drops a real wingbeat grain on it (grains cut from the SFX_10X recordings, pitched
down for gull size). Level and high-cut follow distance, pan follows screen x. Method from
projects/extra-salt-kollosche-birds/scripts/06_flap_real.py.

Usage: python3 flap_sfx.py <job> [--offset 64.69 --length 71.57] [--peak -20]
  --offset/--length place the clip inside a full-film WAV so it lines up at 0:00 with the other stems.
Writes <job>/out/wing-flaps.wav (48 kHz 24-bit stereo).
"""
import argparse
import json
import os
import subprocess
import sys
import wave

import numpy as np
from scipy.signal import butter, find_peaks, resample, sosfilt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "lib"))
import flight  # noqa: E402

SR = 48000
SFX = os.path.join(HERE, "..", "extra-salt-kollosche-birds", "src", "sfx")
SRC = [os.path.join(SFX, f) for f in ("Birds Flapping Whoosh.wav", "Bird Whoosh 2.wav")]


def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def grains():
    out = []
    for p in SRC:
        x = load(p)
        db = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(480) / 480, "same")) + 1e-9)
        pk, _ = find_peaks(db, height=db.max() - 18, distance=int(0.08 * SR), prominence=6)
        for k in pk:
            a, b = k - int(0.035 * SR), k + int(0.17 * SR)
            if a < 0 or b > len(x):
                continue
            g = x[a:b].copy()
            w = np.ones(len(g))
            fi, fo = int(0.01 * SR), int(0.07 * SR)
            w[:fi] = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, fi))
            w[-fo:] = 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, fo))
            out.append(g * w / np.abs(g * w).max())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job")
    ap.add_argument("--offset", type=float, default=0.0)
    ap.add_argument("--length", type=float)
    ap.add_argument("--peak", type=float, default=-20.0)
    a = ap.parse_args()
    job = os.path.abspath(a.job)
    cam = json.load(open(os.path.join(job, "camera.json")))
    shot = json.load(open(os.path.join(job, "shot.json")))
    lay = json.load(open(os.path.join(job, "layout.json")))
    w, h = cam["width"], cam["height"]
    fps = shot["fps"][0] / shot["fps"][1]
    f_px = cam["lens_mm"] / 36 * w
    frames = cam["frames"]
    n = len(frames)
    rng = np.random.default_rng(11)
    G = grains()
    length = a.length or a.offset + n / fps
    mix = np.zeros((int(length * SR) + SR, 2))
    for bird in lay["birds"]:
        keys = flight.simulate(bird, frames[0], f_px, fps, n)
        fr = np.array([k["frame"] for k in keys])
        el = np.array([k["wings"]["elev"] for k in keys])
        bird_pitch = rng.uniform(-4, -2)
        hits = 0
        for i in range(1, len(keys) - 1):
            if not (el[i] >= el[i - 1] and el[i] > el[i + 1]):
                continue
            j = i + 1
            while j < len(keys) - 1 and el[j + 1] < el[j]:
                j += 1
            drop = el[i] - el[j]
            if drop < 12:  # gliding: no beat
                continue
            M = frames[min(n - 1, max(0, int(round(fr[i])) - 1))]
            pr = flight.project(keys[i]["pos"], M, f_px, w, h)
            if pr is None:
                continue
            x, _, dist = pr
            g = G[rng.integers(len(G))]
            g = resample(g, int(len(g) / 2 ** ((bird_pitch + rng.uniform(-0.5, 0.5)) / 12)))
            g = sosfilt(butter(2, float(np.clip(16000 * 8 / dist, 2500, 16000)), btype="low", fs=SR, output="sos"), g)
            gain = (min(1.0, 8.0 / dist) ** 1.3) * (drop / 78) * rng.uniform(0.85, 1.0)
            pan = float(np.clip((x / w - 0.5) * 1.6, -0.9, 0.9))
            s0 = int((a.offset + (fr[i] - 1) / fps + 0.02) * SR)
            s = g[: max(0, len(mix) - s0)]
            mix[s0:s0 + len(s), 0] += s * gain * np.cos((pan + 1) * np.pi / 4)
            mix[s0:s0 + len(s), 1] += s * gain * np.sin((pan + 1) * np.pi / 4)
            hits += 1
        print(f"{bird['tag']}: {hits} flaps")
    mix = mix[: int(length * SR)]
    mix *= 10 ** (a.peak / 20) / max(np.abs(mix).max(), 1e-9)
    out = os.path.join(job, "out", "wing-flaps.wav")
    pcm = (np.clip(mix, -1, 1) * (2 ** 23 - 1)).astype("<i4")
    with wave.open(out, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(3)
        wf.setframerate(SR)
        wf.writeframes(b"".join(int(v).to_bytes(3, "little", signed=True) for v in pcm.ravel()))
    print("->", out)


if __name__ == "__main__":
    main()
