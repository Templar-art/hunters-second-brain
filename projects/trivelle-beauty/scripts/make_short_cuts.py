"""15 s ad cuts (cut on a sentence end <= ~12 s, keep the 3.5 s end card) + organic Reels versions (no end card)."""
import os, sys, json, subprocess
ADS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "device-v2", "ads")
SP = sys.argv[1]; MODEL = os.path.expanduser("~/.cache/whisper/ggml-large-v3.bin")
SHORT = ["D-seated-explainer", "F-review-reply"] if len(sys.argv) > 2 else ["A-salon", "D-seated-explainer", "E-animated", "F-review-reply", "G-animated-3d-motion", "B-lived-a-little", "C-drawer"]
REELS = ["E-animated", "G-animated-3d-motion", "H-girls-night", "I-podcast"]
run = lambda *a: subprocess.run(a, check=True)
dur = lambda p: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))
os.makedirs(os.path.join(ADS, "15s"), exist_ok=True); os.makedirs(os.path.join(ADS, "reels"), exist_ok=True)
for n in SHORT:
    src = os.path.join(ADS, f"trivelle-{n}.mp4"); d = dur(src); body = d - 3.5
    wav = os.path.join(SP, f"sc_{n}.wav"); run("ffmpeg", "-v", "error", "-y", "-i", src, "-t", f"{body}", "-ar", "16000", "-ac", "1", wav)
    subprocess.run(["whisper-cli", "-m", MODEL, "-f", wav, "-ml", "1", "-sow", "-oj", "-of", wav[:-4]], capture_output=True)
    segs = [(s["offsets"]["to"] / 1000, s["text"].strip()) for s in json.load(open(wav[:-4] + ".json"))["transcription"] if s["text"].strip()]
    ends = [t for t, w in segs if w[-1] in (".!?" if n not in ("D-seated-explainer","F-review-reply") else ".!?,") and 7.0 <= t <= 12.0]
    cut = {"D-seated-explainer": 11.35, "F-review-reply": 11.35}.get(n, (max(ends) if ends else 11.5) + 0.25)
    out = os.path.join(ADS, "15s", f"trivelle-{n}-15s.mp4")
    run("ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex",
        f"[0:v]trim=0:{cut},setpts=PTS-STARTPTS[v0];[0:a]atrim=0:{cut},asetpts=PTS-STARTPTS,afade=t=out:st={cut-0.25}:d=0.25[a0];"
        f"[0:v]trim={body}:{d},setpts=PTS-STARTPTS[v1];[0:a]atrim={body}:{d},asetpts=PTS-STARTPTS[a1];"
        "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-crf", "20", "-preset", "slow", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out)
    print(f"{n}: cut {cut:.1f}s -> {dur(out):.1f}s")
for n in (REELS if len(sys.argv) < 3 else []):
    src = os.path.join(ADS, f"trivelle-{n}.mp4"); d = dur(src); out = os.path.join(ADS, "reels", f"trivelle-{n}-reel.mp4")
    run("ffmpeg", "-v", "error", "-y", "-i", src, "-t", f"{d-3.5}", "-af", f"afade=t=out:st={d-4.2}:d=0.7",
        "-c:v", "libx264", "-crf", "20", "-preset", "slow", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out)
    print(f"reel {n}: {dur(out):.1f}s")
