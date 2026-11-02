"""Full-length (692-frame, 28.86 s) 9:16 ProRes 4444 alpha overlays for Hunter's FCP reel
timeline, all starting at 00:00 over Edits/Reel.mp4, plus a preview comp.

Layers (Kollosche 9:16 rules: K icon opens, no address super, 9:16 outro): K icon opener,
K badge pin (coast wide r17, 20.9 s), sky gulls (same shot), Taylor Kleinberg outro.

Usage: python3 -I scripts/assemble_reel.py <job_dir> <Reel.mp4> <deliver_dir>
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

job, src, dst = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3])
root = job.parents[1]
W, H, N, FPS = 1080, 1920, 692, "24000/1001"
R17 = 502                      # reel frame where shot r17 (coast wide) starts


def ss(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def with_alpha(im, k):
    if k >= 1:
        return im
    im = im.copy()
    im.putalpha(Image.fromarray((np.array(im.getchannel("A")) * k).astype(np.uint8)))
    return im


def seq(folder, prefix, start):
    files = sorted((job / folder).glob(prefix + "_*.png"))
    return {start + i: f for i, f in enumerate(files)}


k_icon = Image.open(root / "raw/kollosche/brand-logos/K-icon-1080-x-1920.png").convert("RGBA")


def opener(f):
    return with_alpha(k_icon, 1 - ss((f - 62) / 10)) if f < 72 else None   # frame 1, no fade-in; out by 3 s


outro_png = Image.open(job / "cards/kollosche-outro-taylor_thibault-9x16.png").convert("RGBA").resize((W, H), Image.LANCZOS)
OUTRO = N - 60                 # last 2.5 s, same length as the 16:9


def outro(f):
    return with_alpha(outro_png, ss((f - OUTRO + 1) / 15)) if f >= OUTRO else None


LAYERS = {
    "01 Opener - K icon": opener,
    "02 K badge pin (20.9s)": seq("reel/r17/render/gfx", "g", R17),
    "03 Birds - gulls in the sky (20.9s)": seq("reel/r17/render/birds_png", "b", R17),
    "04 Outro - Taylor Kleinberg + Thibault Parolini": outro,
}


def frame(layer, f):
    if callable(layer):
        return layer(f)
    p = layer.get(f)
    return Image.open(p).convert("RGBA") if p else None


dst.mkdir(parents=True, exist_ok=True)
blank = np.zeros((H, W, 4), np.uint8).tobytes()
for name, layer in LAYERS.items():
    out = dst / f"{name}.mov"
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
                           "-r", FPS, "-i", "-", "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
                           "-vendor", "apl0", str(out)], stdin=subprocess.PIPE)
    for f in range(N):
        im = frame(layer, f)
        ff.stdin.write(blank if im is None else im.tobytes())
    ff.stdin.close()
    ff.wait()
    print("wrote", out.name)

audio = sys.argv[4] if len(sys.argv) > 4 else None   # optional SFX mix for the preview
ins, chain, last = [], [], "0:v"
for i, name in enumerate(LAYERS, 1):
    ins += ["-i", str(dst / f"{name}.mov")]
    chain.append(f"[{last}][{i}:v]overlay=format=auto[v{i}]")
    last = f"v{i}"
amap = ["-map", f"{len(LAYERS) + 1}:a"] if audio else ["-map", "0:a?"]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, *ins, *(["-i", audio] if audio else []),
                "-filter_complex", ";".join(chain), "-map", f"[{last}]", *amap, "-c:a", "aac", "-b:a", "256k",
                "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-shortest",
                str(dst / "Reel - Kollosche overlays PREVIEW.mp4")], check=True)
print("preview done")
