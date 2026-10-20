"""List every stretch >= 0.5 s where the frame barely changes (the same measure as gen-runner's FREEZE flag).

    python3 tools/still_scan.py <video.mp4> [min_seconds]

Run it on the OLD render before rebuilding an episode, so dead holds get fixed in the first build.
"""
import sys
import cv2
import numpy as np

path, mn = sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else .5
cap = cv2.VideoCapture(path); fps = cap.get(cv2.CAP_PROP_FPS) or 30
prev, run, i, out = None, 0, 0, []
while True:
    ok, f = cap.read()
    if not ok:
        break
    g = cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (320, 569))
    if prev is not None:
        if float(np.abs(g.astype(np.int16) - prev).mean()) < .15:
            run += 1
        else:
            if run + 1 >= mn * fps:
                out.append(((i - run - 1) / fps, i / fps))
            run = 0
    prev, i = g, i + 1
if run + 1 >= mn * fps:
    out.append(((i - run - 1) / fps, i / fps))
print(" ".join(f"{a:.2f}-{b:.2f}" for a, b in out) or "no still stretches")
