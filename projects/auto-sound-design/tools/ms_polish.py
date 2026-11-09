"""Mid/side polish for a finished song-cut mix (2026-11-09, Cinema 90 s). Usage: ms_polish.py IN.wav OUT.wav
Fixes the two Earshot critique flags these cuts usually carry: "very wide" (side scaled x0.7 = -3 dB, and the side
high-passed at 120 Hz, zero-phase, so the bass is mono and survives phone speakers) and "honky/harsh mids" (RBJ
peaking -2 dB at 2 kHz, Q 0.8, on mid and side). The mid keeps its full low end. Loudness-match to -14 LUFS afterwards.
Don't do this with an ffmpeg lowpass/highpass band split + amix: on Cinema that thinned 60-250 Hz by 4 dB."""
import sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfiltfilt, lfilter
x, sr = sf.read(sys.argv[1]); M = (x[:, 0] + x[:, 1]) / 2; S = (x[:, 0] - x[:, 1]) / 2
S = sosfiltfilt(butter(4, 120, "high", fs=sr, output="sos"), S) * 0.7
def peq(y, f0, g, Q):
    A = 10 ** (g / 40); w = 2 * np.pi * f0 / sr; a = np.sin(w) / (2 * Q)
    b = [1 + a * A, -2 * np.cos(w), 1 - a * A]; aa = [1 + a / A, -2 * np.cos(w), 1 - a / A]
    return lfilter(np.array(b) / aa[0], np.array(aa) / aa[0], y)
M, S = peq(M, 2000, -2.0, 0.8), peq(S, 2000, -2.0, 0.8)
sf.write(sys.argv[2], np.stack([M + S, M - S], 1), sr, subtype="PCM_24")
