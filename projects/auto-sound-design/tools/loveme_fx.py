"""Beat-locked creative FX for the Kollosche cinematic cut of JMSN "Love Me" (33.62 s, 80.7 BPM).

Hunter 29 Oct: "little things like a flicker that comes up real quick, really quick beat things" so he can cut
creative visual flickers to the song. Everything sits on the cut's own beat grid (beats measured on the original,
mapped through the cut: intro 0-21.69 as-is, chorus = 21.69 + (orig - 117.08)).

Stems (all start at 0:00, same length as the song, drop at 0 in FCP under the song):
  1 flicker shutters  - camera shutter / flash-bulb ticks, single and 1/16 bursts into downbeats
  2 glitch flickers   - synthesised digital flickers (gated, crushed noise + buzz) on chorus offbeats
  3 stutter rolls     - the song itself re-triggered 1/8 -> 1/16 -> 1/32 into the drop and the last bar
  4 riser + impact    - riser peaking on the drop (21.69) + glimmer hit
plus "Love Me - FX version (mastered).wav" with all of it baked in (stutters replace the song under them),
one-shots/ for free placement, and beat-map.txt (every beat time, downbeats marked).

Usage: python tools/loveme_fx.py
"""
import os

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


def glitch(kind, length):
    n = int(length * SR)
    t = np.arange(n) / SR
    if kind == "crush":                               # gated, bit-crushed noise flicker
        x = rng.standard_normal(n)
        x = sosfilt(butter(2, 2500, "high", fs=SR, output="sos"), x)
        hold = 6
        x = np.repeat(x[::hold], hold)[:n]
        x = np.round(x * 4) / 4
        gate = (np.floor(t / 0.011) % 2 == 0).astype(float)
    else:                                             # digital buzz: square-ish tone with fast on/off
        x = np.sign(np.sin(2 * np.pi * 2200 * t)) * 0.5 + np.sin(2 * np.pi * 4400 * t) * 0.3
        gate = (np.floor(t / 0.0075) % 2 == 0).astype(float)
    env = np.exp(-t / (length * 0.45))
    x = x * gate * env
    k = int(0.002 * SR)
    x[:k] *= np.linspace(0, 1, k)
    return x / np.abs(x).max()


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
    crush, buzz = glitch("crush", 0.11), glitch("buzz", 0.08)

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

    # 2 glitch flickers: chorus, the "and" of beat 4 every bar + a 1/32 double on the 2 of every other bar
    for i, d in enumerate(x for x in downs if x >= DROP - 0.05):
        place(s2, crush, d + 3.5 * beat, -13, pan=0.5 if i % 2 else -0.5)
        if i % 2 == 0:
            place(s2, buzz, d + beat, -18, pan=-0.3)
            place(s2, buzz, d + beat + beat / 8, -20, pan=0.3)
    for d in downs:                                    # intro: light crush ticks on beat 3 of the bass-in bars
        if 12.0 < d < DROP - 3:
            place(s2, crush, d + 2 * beat, -20)

    # 3 stutter rolls: last 2 beats into the drop (1/8 x2, 1/16 x2, 1/32 x4), and a 1/16 roll into the last bar
    stutter(song, DROP - 2 * beat, [(2, beat / 2), (2, beat / 4), (4, beat / 8)], baked, s3)
    last = max(d for d in downs if d < 31.5)
    stutter(song, last - beat, [(2, beat / 4), (4, beat / 8)], baked, s3)

    # 4 riser peaking on the drop + glimmer impact
    riser = mono(os.path.join(LIB, "Foundation", "DSGNRise", "DSGNRise_RISER-Into the Light_Ocular_Foundation.wav"))
    pk = int(np.argmax(np.abs(riser)))
    riser = riser[:pk] / np.abs(riser[:pk]).max()
    riser = riser[-int(4 * beat * SR):]                # one bar of rise
    place(s4, riser, DROP - len(riser) / SR, -12)
    hit = mono(os.path.join(LIB, "Foundation", "DSGNImpt", "DSGNImpt_IMPACT-Glimmer Hit_Ocular_Foundation.wav"))
    k = int(np.argmax(np.abs(hit)))
    place(s4, hit[max(0, k - int(0.01 * SR)):] / np.abs(hit).max(), DROP - 0.01, -9)

    stems = [("1 FX - flicker shutters", s1), ("2 FX - glitch flickers", s2), ("3 FX - stutter rolls (song chops)", s3),
             ("4 FX - riser + impact into drop", s4)]
    for name, s in stems:
        sf.write(os.path.join(OUT, f"{name}.wav"), np.clip(s, -1, 1).T, SR, subtype="PCM_24")
    fx_only = s1 + s2 + s4
    mix = baked + fx_only
    sf.write(os.path.join(OUT, "Love Me - FX version.wav"), np.clip(mix / max(1.0, np.abs(mix).max() / 0.98), -1, 1).T,
             SR, subtype="PCM_24")

    shots = {"flicker-shutter-1": shut[0], "flicker-shutter-2": shut[1], "flicker-shutter-3": shut[2],
             "flicker-shutter-4": shut[3], "flicker-kodak": kodak, "flash-bulb-pop": bulb,
             "glitch-crush": crush, "glitch-buzz": buzz}
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
