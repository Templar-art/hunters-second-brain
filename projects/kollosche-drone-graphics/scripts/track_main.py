"""Top-down Main.mp4: ground-plane homographies from the sharp last frame back
to frame 1, chained frame to frame (SIFT + RANSAC on half-res greys).

The plate-vfx drone fit fails here (fast spin and heavy motion blur in the
first frames). A straight-down shot sees the ground as a plane facing the
camera, so per-frame homographies are the right model.

Usage: python3 -I track_main.py <job_dir>
Writes <job_dir>/main/homographies.json: H[k] maps last-frame pixels to frame k.
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np

job = Path(sys.argv[1]) / "main"
frames = sorted((job / "frames").glob("f_*.png"))
S = 0.5
sift = cv2.SIFT_create(nfeatures=6000)

def feats(p):
    g = cv2.cvtColor(cv2.imread(str(p)), cv2.COLOR_BGR2GRAY)
    g = cv2.resize(g, None, fx=S, fy=S, interpolation=cv2.INTER_AREA)
    return sift.detectAndCompute(g, None)

matcher = cv2.BFMatcher()
n = len(frames)
H = [None] * n
H[-1] = np.eye(3)
kp_b, de_b = feats(frames[-1])
stats = []
for k in range(n - 2, -1, -1):
    kp_a, de_a = feats(frames[k])
    good = [m for m, m2 in matcher.knnMatch(de_b, de_a, k=2) if m.distance < 0.75 * m2.distance]
    src = np.float32([kp_b[m.queryIdx].pt for m in good]) / S
    dst = np.float32([kp_a[m.trainIdx].pt for m in good]) / S
    Hk, inl = cv2.findHomography(src, dst, cv2.RANSAC, 3.0)
    # Hk maps frame k+1 -> frame k; chain onto last -> k+1.
    H[k] = Hk @ H[k + 1]
    H[k] /= H[k][2, 2]
    err = np.linalg.norm(cv2.perspectiveTransform(src[None], Hk)[0] - dst, axis=1)[inl.ravel() == 1]
    stats.append((k + 1, len(good), int(inl.sum()), float(np.median(err))))
    kp_b, de_b = kp_a, de_a

for s in sorted(stats):
    print("frame %2d  matches %4d  inliers %4d  median err %.2f px" % s)
(job / "homographies.json").write_text(json.dumps({"ref": "last", "H": [h.tolist() for h in H]}))
