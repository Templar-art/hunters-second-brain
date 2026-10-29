"""Reel finishing: place one-off accents by hand (e.g. Hunter's sun-flare shing), master the song with
straight gain, and render a review MP4 of video + song + SFX stems. Stems stay separate for FCP.

  python3 tools/reel_mix.py VIDEO SONG RUN_DIR --accent FILE@TIME[@PEAK_DB] ... [--song-lufs -14]
TIME is where the accent's own peak lands. Writes RUN_DIR/<stem>_sfx_shing.wav (all hand accents),
<song>_mastered.wav next to the song, and RUN_DIR/<stem>_REEL-MIX.mp4."""
import argparse, glob, json, os, subprocess
import numpy as np, soundfile as sf
SR = 48000

def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)

def lufs(p):
    r = subprocess.run(["ffmpeg", "-i", p, "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return float(json.loads(r[r.rindex("{"):r.rindex("}") + 1])["input_i"])

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("song"); ap.add_argument("run")
ap.add_argument("--accent", action="append", default=[])
ap.add_argument("--song-lufs", type=float, default=-14.0)
a = ap.parse_args()
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.video],
                           capture_output=True, text=True).stdout)
stem = os.path.splitext(os.path.basename(a.video))[0]
n = int(dur * SR)

acc = np.zeros((n, 2))
for spec in a.accent:
    f, t, *pk = spec.split("@")
    x = load(f); m = np.abs(x).max(1)
    x *= 10 ** ((float(pk[0]) if pk else -18.0) / 20) / m.max()
    s0 = int(float(t) * SR) - int(m.argmax())
    x = x[max(0, -s0):]; s0 = max(0, s0); x = x[:n - s0]
    acc[s0:s0 + len(x)] += x
    print(f"accent {os.path.basename(f)}: peak at {t}s")
shing = os.path.join(a.run, f"{stem}_sfx_shing.wav")
sf.write(shing, acc, SR, subtype="PCM_24")

gain = a.song_lufs - lufs(a.song)
song = load(a.song)[:n] * 10 ** (gain / 20)
tp = 20 * np.log10(np.abs(song).max())
if tp > -1.0:  # straight gain only, no limiter; trim to keep -1 dBFS sample peak
    song *= 10 ** ((-1.0 - tp) / 20); gain += -1.0 - tp
mastered = os.path.splitext(a.song)[0] + "_mastered.wav"
sf.write(mastered, song, SR, subtype="PCM_24")
print(f"song gain {gain:+.1f} dB -> {mastered}")

sfx = load(glob.glob(os.path.join(a.run, "*_sfx_only.wav"))[0])[:n]
mix = np.zeros((n, 2))
for x in (song, sfx, acc):
    mix[:len(x)] += x
mix *= min(1.0, 10 ** (-1 / 20) / np.abs(mix).max())
tmp = os.path.join(a.run, "_reelmix.wav"); sf.write(tmp, mix, SR, subtype="PCM_24")
out = os.path.join(a.run, f"{stem}_REEL-MIX.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-i", tmp, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "320k", "-shortest", out], check=True)
os.remove(tmp)
print("->", out)
