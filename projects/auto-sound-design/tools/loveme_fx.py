"""Beat-locked creative FX for the Kollosche cinematic cut of JMSN "Love Me" (33.62 s, 80.7 BPM).

Hunter 29 Oct: "little things like a flicker that comes up real quick, really quick beat things" so he can cut
creative visual flickers to the song. Everything sits on the cut's own beat grid (beats measured on the original,
mapped through the cut: intro 0-21.69 as-is, chorus = 21.69 + (orig - 117.08)).

Stems (all start at 0:00, same length as the song, drop at 0 in FCP under the song):
  1 flicker shutters  - camera shutter / flash-bulb ticks, single and 1/16 bursts into downbeats
  2 reverse swells    - the song's own next downbeat, reversed + smeared, sucking into the key bars (replaced the
                        synth glitch flickers: Hunter 29 Oct "i dont like those glitch things")
  3 stutter roll      - the song itself re-triggered 1/8 -> 1/16 -> 1/32 into the drop only
  4 riser + impact    - riser peaking on the drop (21.69) + glimmer hit
plus "Love Me - FX version (mastered).wav" with all of it baked in (stutters replace the song under them),
one-shots/ for free placement, and beat-map.txt (every beat time, downbeats marked).

Usage: python tools/loveme_fx.py
"""
import os
import re
import subprocess

import librosa
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "output", "loveme-kollosche")
SONG = "/Users/10xhunter/Downloads/JMSN - Love Me (Official Video).mp3"
CUT = os.path.join(OUT, "Love Me - Kollosche cinematic cut.wav")
LIB = os.path.expanduser("~/Music/SFX Library/Ocular Sounds")
CAM = os.path.join(LIB, "Aperture", "COMCam", "COMCam_{}_Ocular_Aperture.wav")
JOIN, SEG2 = 21.69, 117.08          # cut point on the output, and where the chorus segment starts in the original
DROP = JOIN
rng = np.random.default_rng(7)


def load(p, sr=SR):
    y, _ = librosa.load(p, sr=sr, mono=False)
    return np.atleast_2d(y)


def mono(p):
    y = load(p)
    return y.mean(0)


def grain(p, length, pre=0.004):
    """Strongest transient of a library file, `length` s long, faded out."""
    y = mono(p)
    k = int(np.argmax(np.abs(y)))
    a = max(0, k - int(pre * SR))
    g = y[a:a + int(length * SR)].copy()
    f = min(len(g) // 2, int(0.03 * SR))
    g[-f:] *= np.linspace(1, 0, f)
    return g / np.abs(g).max()


def beat_grid():
    y, sr = librosa.load(SONG, sr=22050)
    _, b = librosa.beat.beat_track(y=y, sr=sr, units="time", start_bpm=80.7, tightness=400)
    down = b[0::4]                                   # downbeat phase 0 measured on the kick (low-band onsets)
    out = []
    for t in b:
        if t < JOIN - 0.05:
            out.append((t, t in down))
        elif t >= SEG2 - 0.05:
            out.append((JOIN + t - SEG2, t in down))
    return [(round(t, 3), d) for t, d in out if t < 33.62]


def place(buf, g, t, db, pan=0.0):
    s = int(t * SR)
    if s >= buf.shape[1]:
        return
    g = g[: buf.shape[1] - s] * 10 ** (db / 20)
    buf[0, s:s + len(g)] += g * np.cos((pan + 1) * np.pi / 4) * 1.414
    buf[1, s:s + len(g)] += g * np.sin((pan + 1) * np.pi / 4) * 1.414


def swell(song, t, length):
    """Reverse swell into time t: the song's own first `length` s after t, smeared by a soft decaying-noise reverb,
    reversed so it rises and lands on the downbeat. Low-passed so it sits under the mix, harmony always matches."""
    a = int(t * SR)
    x = song[:, a:a + int(length * SR)].mean(0)
    ir = rng.standard_normal(int(1.2 * SR)) * np.exp(-np.arange(int(1.2 * SR)) / (0.35 * SR))
    wet = np.convolve(x, ir)[: int(length * SR)]
    wet = sosfilt(butter(2, 5000, "low", fs=SR, output="sos"), wet)
    r = wet[::-1].copy()
    r *= np.linspace(0, 1, len(r)) ** 2
    f = int(0.006 * SR)
    r[-f:] *= np.linspace(1, 0, f)
    return r / np.abs(r).max()


def stutter(song, start, pattern, out, fx):
    """Re-trigger the song: `pattern` is a list of (n_repeats, slice_s); each slice is cut fresh at its position
    so the harmony moves on, starting at `start`. Writes into `fx` (stem) and replaces `out` (baked version)."""
    t = start
    for reps, L in pattern:
        src = song[:, int(t * SR):int((t + L) * SR)].copy()
        f = int(0.004 * SR)
        src[:, :f] *= np.linspace(0, 1, f)
        src[:, -f:] *= np.linspace(1, 0, f)
        for r in range(reps):
            s = int((t + r * L) * SR)
            gain = 0.85 + 0.15 * r / max(1, reps - 1)
            fx[:, s:s + src.shape[1]] += src * gain
            out[:, s:s + src.shape[1]] = src * gain
        t += reps * L
    return t


def main():
    os.makedirs(os.path.join(OUT, "one-shots"), exist_ok=True)
    song = load(CUT)
    n = song.shape[1]
    beats = beat_grid()
    bt = np.array([b for b, _ in beats])
    downs = [b for b, d in beats if d]
    beat = float(np.median(np.diff(bt)))
    with open(os.path.join(OUT, "beat-map.txt"), "w") as f:
        f.write("Love Me (Kollosche cut) beat map: seconds from 0:00. BAR = downbeat. Drop/chorus = 21.69\n")
        for i, (t, d) in enumerate(beats):
            f.write(f"{t:7.3f}  {'BAR' if d else '   '}\n")

    shut = [grain(CAM.format(f"VINTAGE CAMERA-Konica Shutter 0{i}"), 0.12) for i in (1, 3, 5, 7)]
    kodak = grain(CAM.format("VINTAGE CAMERA-Kodak 1950 Duaflex Shutter 01"), 0.15)
    bulb = grain(CAM.format("VINTAGE FLASHBULB-Camera Flash Bulb C 01"), 0.35)

    s1, s2, s3, s4 = (np.zeros((2, n)) for _ in range(4))
    baked = song.copy()

    # 1 flicker shutters: flash pops on the quiet intro bars, 1/16 shutter bursts leading into each downbeat after
    for d in downs:
        if d < 12.0:
            place(s1, bulb, d, -14, pan=rng.uniform(-0.3, 0.3))
        elif d < DROP - 0.1 or d > DROP + 0.1:
            for k in range(3):                         # three 1/16s ending on the downbeat
                place(s1, shut[k % 4], d - (3 - k) * beat / 4, -16 + 3 * k, pan=(-0.4, 0.4, 0)[k])
            place(s1, kodak, d, -10)
    place(s1, bulb, DROP, -8)

    # 2 reverse swells: half a bar of suck into the bass-in bar, the bars either side of the drop, and the last bar
    for d in [x for x in downs if 12.0 < x < DROP - 0.1] + [x for x in downs if x > DROP + 0.1]:
        L = 2 * beat
        place(s2, swell(song, d, L), d - L, -9)
    # 3 stutter roll: last 2 beats into the drop (1/8 x2, 1/16 x2, 1/32 x4)
    stutter(song, DROP - 2 * beat, [(2, beat / 2), (2, beat / 4), (4, beat / 8)], baked, s3)

    # 4 riser peaking on the drop + glimmer impact
    riser = mono(os.path.join(LIB, "Foundation", "DSGNRise", "DSGNRise_RISER-Into the Light_Ocular_Foundation.wav"))
    pk = int(np.argmax(np.abs(riser)))
    riser = riser[:pk] / np.abs(riser[:pk]).max()
    riser = riser[-int(4 * beat * SR):]                # one bar of rise
    place(s4, riser, DROP - len(riser) / SR, -12)
    hit = mono(os.path.join(LIB, "Foundation", "DSGNImpt", "DSGNImpt_IMPACT-Glimmer Hit_Ocular_Foundation.wav"))
    k = int(np.argmax(np.abs(hit)))
    place(s4, hit[max(0, k - int(0.01 * SR)):] / np.abs(hit).max(), DROP - 0.01, -9)

    stems = [("1 FX - flicker shutters", s1), ("2 FX - reverse swells", s2), ("3 FX - stutter roll into drop (song chops)", s3),
             ("4 FX - riser + impact into drop", s4)]
    for name, s in stems:
        sf.write(os.path.join(OUT, f"{name}.wav"), np.clip(s, -1, 1).T, SR, subtype="PCM_24")
    fx_only = s1 + s2 + s4
    mix = baked + fx_only
    sf.write(os.path.join(OUT, "Love Me - FX version.wav"), np.clip(mix / max(1.0, np.abs(mix).max() / 0.98), -1, 1).T,
             SR, subtype="PCM_24")

    # Song and SFX as two separate tracks (Hunter 29 Oct) that sum back to the FX version at -14 LUFS: one linear gain
    # for both, so they stay balanced when laid together at 0:00. The song track carries the drop stutter (it is an
    # edit of the song itself); the SFX track is shutters + swells + riser/impact.
    tmp = os.path.join(OUT, "_mix.wav")
    sf.write(tmp, mix.T, SR, subtype="FLOAT")
    r = subprocess.run(["ffmpeg", "-nostats", "-i", tmp, "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    os.remove(tmp)
    lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])
    g = 10 ** ((-14 - lufs) / 20)
    g = min(g, 10 ** (-1 / 20) / np.abs(mix).max())    # never past -1 dBFS on the sum
    # "no shutters" is for edits that put their own clicks on the picture cuts (Kollosche cinematic, 29 Oct)
    for name, x in (("Love Me - SONG only (with drop stutter)", baked), ("Love Me - SFX only", fx_only),
                    ("Love Me - SFX swells + riser (no shutters)", s2 + s4)):
        sf.write(os.path.join(OUT, f"{name}.wav"), np.clip(x * g, -1, 1).T, SR, subtype="PCM_24")
    print(f"song + SFX tracks: gain {20 * np.log10(g):+.1f} dB (sum at {lufs + 20 * np.log10(g):.1f} LUFS)")

    shots = {"flicker-shutter-1": shut[0], "flicker-shutter-2": shut[1], "flicker-shutter-3": shut[2],
             "flicker-shutter-4": shut[3], "flicker-kodak": kodak, "flash-bulb-pop": bulb,
             "reverse-swell-into-drop": swell(song, DROP, 2 * beat)}
    burst = np.zeros(int(beat * SR))                   # ready-made 1/16 shutter burst, ends on its last hit
    for k in range(4):
        s = int(k * beat / 4 * SR)
        g = shut[k][: len(burst) - s]
        burst[s:s + len(g)] += g * 10 ** ((-6 + 2 * k) / 20)
    shots["flicker-burst-1-16"] = burst
    for name, g in shots.items():
        sf.write(os.path.join(OUT, "one-shots", f"{name}.wav"), (g / np.abs(g).max() * 0.7), SR, subtype="PCM_24")
    print(f"beat {beat:.4f} s, {len(downs)} bars; stems + FX version + {len(shots)} one-shots -> {OUT}")


if __name__ == "__main__":
    main()
