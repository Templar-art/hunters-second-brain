"""Per-frame face box → build/face.json ([[x, y, w, h], ...] per frame, 1080x1920 source coords).
Haar detection every 3rd frame, nearest-largest face, smoothed + interpolated. Usage: facetrack.py <build_dir>"""
import glob, json, os, sys
import cv2, numpy as np
build = sys.argv[1]
frames = sorted(glob.glob(f"{build}/frames/f*.jpg"))
det = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
raw = {}
prev = None
for i, f in enumerate(frames):
    if i % 3: continue
    im = cv2.imread(f, cv2.IMREAD_GRAYSCALE); sm = cv2.resize(im, (540, 960))
    faces = det.detectMultiScale(sm, 1.1, 5, minSize=(60, 60))
    if len(faces):
        cand = [np.array(b, float) * 2 for b in faces]
        b = max(cand, key=lambda b: b[2] * b[3] - (0 if prev is None else np.hypot(*(b[:2] - prev[:2])) * 4))
        raw[i] = b; prev = b
idx = sorted(raw)
if not idx: raise SystemExit("no face found")
# reject outliers: size far from the median face, or centre jumping away from the local median
A = np.array([raw[i] for i in idx]); mw = np.median(A[:, 2]); cx = A[:, 0] + A[:, 2] / 2; cy = A[:, 1] + A[:, 3] / 2
keep = []
for k, i in enumerate(idx):
    lo, hi = max(0, k - 7), min(len(idx), k + 8)
    if not (.75 * mw <= A[k, 2] <= 1.3 * mw): continue
    if abs(cx[k] - np.median(cx[lo:hi])) > .35 * mw or abs(cy[k] - np.median(cy[lo:hi])) > .35 * mw: continue
    keep.append(i)
print(f"rejected {len(idx) - len(keep)} outlier detections")
idx = keep
arr = np.array([raw[i] for i in idx]); out = []
for k in range(4): arr[:, k] = np.convolve(np.pad(arr[:, k], 2, mode="edge"), np.ones(5) / 5, mode="valid")
for i in range(len(frames)):
    v = [np.interp(i, idx, arr[:, k]) for k in range(4)]
    # haar box is brow→chin-ish; grow a little to cover forehead to chin
    x, y, w, h = v; out.append([round(x - w * .05), round(y - h * .1), round(w * 1.1), round(h * 1.25)])
json.dump(out, open(f"{build}/face.json", "w"))
print(f"face track: {len(idx)} detections → {len(out)} frames")
