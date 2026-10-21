"""Synthesise wing-flap SFX synced to the rendered gulls (wings.json from 04_dump_wings.py).

Each downstroke (wing at the top of its beat -> sweeping down) gets a feather "fwump":
band-limited noise burst + low air thump, plus a small feather rustle on the upstroke fold.
Level follows distance (closer = louder, brighter), pan follows screen x, glides get soft air.
Writes out/wing-flaps_synced.wav (48 kHz 24-bit stereo, full clip length incl. the cut frame).
"""
import json, os, wave
import numpy as np
from scipy.signal import butter, sosfilt

JOB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
d = json.load(open(os.path.join(JOB, "wings.json")))
fps = d["fps"]
CLIP_FRAMES = 46
L = int(round(CLIP_FRAMES / fps * SR))
rng = np.random.default_rng(7)
mix = np.zeros((L, 2))


def band(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)


def lowp(x, hi, order=2):
    return sosfilt(butter(order, hi, btype="low", fs=SR, output="sos"), x)


def env(n, attack, decay):
    t = np.arange(n) / SR
    a = np.clip(t / attack, 0, 1) ** 1.5
    return a * np.exp(-np.clip(t - attack, 0, None) / decay)


def place(sig, t0, gain, pan):
    i = int(t0 * SR)
    if i >= L or i + len(sig) <= 0:
        return
    s = sig[max(0, -i): L - i]
    i = max(0, i)
    lg, rg = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)  # equal-power pan
    mix[i:i + len(s), 0] += s * gain * lg
    mix[i:i + len(s), 1] += s * gain * rg


def fwump(dist, power, stroke_s):
    n = int(0.32 * SR)
    noise = rng.standard_normal(n)
    bright = np.clip(14 / dist, 0.25, 1.0)  # distant birds lose highs
    body = band(noise, 350, 900 + 2600 * bright) * env(n, 0.035 * stroke_s / 0.2, 0.09)
    thump = lowp(rng.standard_normal(n), 220) * env(n, 0.012, 0.06) * 2.2
    air = band(rng.standard_normal(n), 1800, 6000) * env(n, 0.05, 0.05) * 0.25 * bright
    return (body + thump + air) * power


def rustle(dist):
    n = int(0.08 * SR)
    bright = np.clip(14 / dist, 0.25, 1.0)
    crack = rng.standard_normal(n) * (rng.random(n) < 0.08)  # sparse feather ticks
    return band(crack, 2500, 7000) * env(n, 0.004, 0.025) * 0.35 * bright


for tag, rows in d["birds"].items():
    R = np.array(rows)  # frame, elev deg, dist m, screen x 0-1, screen y 0-1
    t = (R[:, 0] - 1) / fps
    el, dist, sx = R[:, 1], R[:, 2], R[:, 3]
    n_ev = 0
    for i in range(1, len(R) - 1):
        if el[i] >= el[i - 1] and el[i] > el[i + 1]:  # top of the beat -> downstroke starts
            j = i + 1
            while j < len(R) - 1 and el[j + 1] < el[j]:
                j += 1
            drop = el[i] - el[j]  # beat amplitude: ~78 deg full flap, ~0 gliding
            if drop < 12:
                continue
            power = (drop / 78) ** 1.3
            stroke_s = t[j] - t[i]
            gain = min(1.0, 7.0 / dist[i]) ** 1.15
            pan = float(np.clip((sx[i] - 0.5) * 1.6, -0.9, 0.9))
            place(fwump(dist[i], power, stroke_s), t[i] + rng.uniform(-0.004, 0.004), gain, pan)
            place(rustle(dist[j]), t[j], gain * power, pan)  # wrist fold at the bottom
            n_ev += 1
    # glide air: soft continuous whoosh while the beat amplitude is small
    amp = np.array([np.ptp(el[max(0, k - 8):k + 8]) for k in range(len(el))])
    glide = np.clip((25 - amp) / 25, 0, 1)
    tt = np.arange(L) / SR
    g = np.interp(tt, t, glide) * np.interp(tt, t, np.minimum(1.0, 7.0 / dist)) ** 1.2
    pan_t = np.clip((np.interp(tt, t, sx) - 0.5) * 1.6, -0.9, 0.9)
    w = band(rng.standard_normal(L), 300, 1400) * g * 0.12
    mix[:, 0] += w * np.cos((pan_t + 1) * np.pi / 4)
    mix[:, 1] += w * np.sin((pan_t + 1) * np.pi / 4)
    print(f"{tag}: {n_ev} flaps, nearest {dist.min():.1f} m")

# gentle bus: soft-clip, normalise to -3 dBFS peak, 5 ms fades
mix = np.tanh(mix * 1.2)
mix *= 10 ** (-3 / 20) / np.abs(mix).max()
fade = int(0.005 * SR)
mix[:fade] *= np.linspace(0, 1, fade)[:, None]
mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
pcm = (np.clip(mix, -1, 1) * (2 ** 23 - 1)).astype("<i4")
raw = b"".join(int(v).to_bytes(4, "little", signed=True)[:3] for v in pcm.ravel())
out = os.path.join(JOB, "out", "wing-flaps_synced.wav")
with wave.open(out, "wb") as wf:
    wf.setnchannels(2); wf.setsampwidth(3); wf.setframerate(SR); wf.writeframes(raw)
print("wrote", out, f"{L / SR:.3f}s")
