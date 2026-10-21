"""Find click-in times that land on the music: spectral-flux onsets, strongest one near each target time.
usage: sync_pops.py music.mp3 start_s  -> prints pops (3) and logo cut, comma-separated. 0 credits."""
import sys, subprocess, numpy as np
f, st = sys.argv[1], float(sys.argv[2]); sr, hop = 22050, 256
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(st), "-t", "16", "-i", f, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"], capture_output=True).stdout
a = np.frombuffer(raw, np.int16).astype(float) / 32768
win = np.hanning(1024); frames = np.lib.stride_tricks.sliding_window_view(a, 1024)[::hop] * win
S = np.log1p(np.abs(np.fft.rfft(frames, axis=1)) * 10)
flux = np.maximum(np.diff(S, axis=0), 0).sum(1); flux = np.convolve(flux, np.hanning(5) / 2.5, "same")
t = (np.arange(len(flux)) + 1) * hop / sr
peaks = [i for i in range(2, len(flux) - 2) if flux[i] == flux[i-2:i+3].max() and flux[i] > np.percentile(flux, 80)]
def pick(lo, hi):
    c = [p for p in peaks if lo <= t[p] <= hi]
    return round(float(t[max(c, key=lambda p: flux[p])]), 3) if c else round((lo + hi) / 2, 3)
p1 = pick(0.3, 1.2); p2 = pick(p1 + 2.4, p1 + 3.6); p3 = pick(p2 + 2.4, p2 + 3.6); cut = pick(p3 + 3.4, p3 + 4.4)
print(f"{p1},{p2},{p3},{cut}")
