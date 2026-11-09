"""D2 / D3: new Higgsfield hook + D seated body (from "It's called Trivelle").
Run: python3 scripts/build_d_hooks.py
Hook clips: device-v2/hooks/d2-hook-fixed.mp4, d3-hook-fixed.mp4 (Marketing Studio UGC, trimmed).
"""
import os, json, subprocess
src = open(os.path.join(os.path.dirname(__file__), "build_ads_v2.py")).read()
exec(src[:src.index("B = lambda")])

DV = os.path.join(ROOT, "device-v2")
HK = os.path.join(DV, "hooks")
WORKD = os.path.join(HK, "work"); os.makedirs(WORKD, exist_ok=True)
BODY_START = 2.5  # D at 2.5 s = "It's called Trivelle…"

HOOKS = {
    "D2-salon-swap": ("d2-hook-fixed.mp4", "This is what I use instead of the salon now."),
    "D3-ten-minutes": ("d3-hook-fixed.mp4", "Ten minutes, a few nights a week. That is it."),
}
BODIES = {"30s": os.path.join(DV, "ads", "trivelle-D-seated-explainer-30s.mp4"),
          "15s": os.path.join(DV, "ads", "15s", "trivelle-D-seated-explainer-15s.mp4")}


def run(a): subprocess.run(a, check=True)


def asr_words(clip):
    wav = os.path.join(WORKD, "a.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-ar", "16000", "-ac", "1", wav])
    run(["whisper-cli", "-m", os.path.expanduser("~/.cache/whisper/ggml-large-v3.bin"), "-f", wav,
         "-ml", "1", "-sow", "-oj", "-of", wav[:-4]])
    js = json.load(open(wav[:-4] + ".json"))
    out = []
    for s in js["transcription"]:
        t = s["text"].strip()
        if t:
            out.append((s["offsets"]["from"] / 1000, s["offsets"]["to"] / 1000, t))
    return out


def dur_(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", p]).decode())


for name, (clip, line) in HOOKS.items():
    hp = os.path.join(HK, clip)
    hd = dur_(hp)
    script = line.replace(",", ",").split()
    ws = align(script, asr_words(hp)) if "align" in globals() else None
    if ws is None:  # even spread fallback
        step = (hd - 0.2) / len(script)
        ws = [(0.1 + i * step, 0.1 + (i + 1) * step, w) for i, w in enumerate(script)]
    caps = chunks(ws)
    cap_mov = os.path.join(WORKD, f"{name}_caps.mov")
    caption_track(caps, hd, cap_mov)
    hook_out = os.path.join(WORKD, f"{name}_hook.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", hp, "-i", cap_mov, "-filter_complex",
         f"[0:v]scale={W}:{H}:flags=lanczos,fps=30,setsar=1[b];[1:v]fps=30[c];[b][c]overlay=0:0:shortest=1[v];"
         f"[0:a]aresample=96000,aformat=channel_layouts=stereo[a]",
         "-map", "[v]", "-map", "[a]", "-t", f"{hd:.3f}", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", hook_out])
    for ln, body in BODIES.items():
        out = os.path.join(DV, "ads", f"trivelle-{name}-{ln}.mp4" if ln == "30s" else f"15s/trivelle-{name}-15s.mp4")
        run(["ffmpeg", "-v", "error", "-y", "-i", hook_out, "-ss", str(BODY_START), "-i", body, "-filter_complex",
             "[0:v]setsar=1[v0];[1:v]setsar=1[v1];[0:a]aformat=sample_rates=96000:channel_layouts=stereo[a0];"
             "[1:a]aformat=sample_rates=96000:channel_layouts=stereo,afade=t=in:d=0.03[a1];"
             "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]",
             "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out])
        print(out, round(dur_(out), 2))
