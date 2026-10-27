"""Tracked white lot outline over Main.mp4 (Hunter's reference: thin white
line, rounded corners, no fill, no labels).

The lot polygon is placed on the last (sharpest) frame and carried to every
frame by the homographies from track_main.py. The line draws on once the
opening spin and blur have settled, then holds.

Usage: python3 -I render_outline.py <job_dir> <clip>
"""
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

job = Path(sys.argv[1])
clip = sys.argv[2]
m = job / "main"
H = [np.array(h) for h in json.loads((m / "homographies.json").read_text())["H"]]
frames = sorted((m / "frames").glob("f_*.png"))
h0, w0 = cv2.imread(str(frames[0])).shape[:2]

# Townhouse lot on the last frame (4K px): street front at the footpath fence,
# north boundary, rear timber fence, south wall beside the driveway.
LOT = np.float32([[1414, 1510], [1245, 955], [2386, 530], [2650, 1195]])
LINE_W = round(w0 * 0.0055)   # ~21 px at 4K, matches the reference weight
DRAW_START, DRAW_FRAMES = 14, 12  # 0-based frame index; ~0.5 s draw-on
SS = 2  # supersample for clean edges

def ease(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)

def partial(poly, frac):
    """The closed polygon traced from its first corner up to frac of its perimeter."""
    pts = np.vstack([poly, poly[:1]])
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    target = seg.sum() * frac
    out = [pts[0]]
    for a, b, L in zip(pts[:-1], pts[1:], seg):
        if target >= L:
            out.append(b)
            target -= L
        else:
            out.append(a + (b - a) * target / L)
            break
    return np.array(out)

alpha_dir = m / "render" / "outline"
alpha_dir.mkdir(parents=True, exist_ok=True)
for k, f in enumerate(frames):
    frac = ease((k - DRAW_START) / DRAW_FRAMES)
    canvas = np.zeros((h0 * SS, w0 * SS), np.uint8)
    if frac > 0:
        poly = cv2.perspectiveTransform(LOT[None], H[k])[0]
        path = partial(poly, frac) * SS
        p = np.round(path * 16).astype(np.int32)  # 4 fractional bits
        cv2.polylines(canvas, [p], frac >= 1, 255, LINE_W * SS, cv2.LINE_AA, shift=4)
        for x, y in path:  # round joins and caps
            cv2.circle(canvas, (int(round(x * 16)), int(round(y * 16))), LINE_W * SS // 2 * 16, 255, -1, cv2.LINE_AA, shift=4)
    a = cv2.resize(canvas, (w0, h0), interpolation=cv2.INTER_AREA)
    rgba = np.dstack([np.full_like(a, 255)] * 3 + [a])
    cv2.imwrite(str(alpha_dir / f"a_{k + 1:04d}.png"), rgba)

out = m / "out"
out.mkdir(exist_ok=True)
fps = "%d/%d" % tuple(json.loads((m / "shot.json").read_text())["fps"])
seq = str(alpha_dir / "a_%04d.png")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(fps), "-i", seq,
                "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
                str(out / "Main_outline_alpha.mov")], check=True)
for name, codec in [("Main_outline.mp4", ["-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p"]),
                    ("Main_outline_ProRes422HQ.mov", ["-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le"])]:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-framerate", str(fps), "-i", seq,
                    "-filter_complex", "[0:v][1:v]overlay=format=auto[v]", "-map", "[v]", "-map", "0:a?",
                    "-c:a", "copy", *codec, str(out / name)], check=True)
print("done", out)
