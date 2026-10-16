"""Face tracking + person cutouts for the edit.
usage: track.py public/edit.mp4 src/faces.json public/matte "0:3.07,22.03:23.6"
 - faces.json: per-frame smoothed face box {cx, cy, w} in 1080x1920 px (OpenCV Haar, no downloads)
 - matte/fNNNN.png: RGBA person cutout (u2net_human_seg) for frames in the given time ranges"""
import json, sys
from pathlib import Path
import cv2, numpy as np, onnxruntime as ort

src, faces_out, matte_dir, ranges = sys.argv[1:5]
ranges = [tuple(map(float, r.split(':'))) for r in ranges.split(',')]
Path(matte_dir).mkdir(parents=True, exist_ok=True)
casc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
model = Path(__file__).resolve().parents[1] / 'models' / 'u2net_human_seg.onnx'
sess = ort.InferenceSession(str(model), providers=['CPUExecutionProvider'])
inp = sess.get_inputs()[0].name

cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS)
raw, i, last = [], 0, None
while True:
    ok, fr = cap.read()
    if not ok: break
    t = i / fps
    small = cv2.resize(fr, (270, 480)); g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    det = casc.detectMultiScale(g, 1.1, 5, minSize=(50, 50))
    if len(det):
        x, y, w, h = max(det, key=lambda d: d[2] * d[3]); last = [(x + w / 2) * 4, (y + h / 2) * 4, w * 4]
    raw.append(last)
    if any(a <= t < b for a, b in ranges):
        im = cv2.cvtColor(cv2.resize(fr, (320, 320)), cv2.COLOR_BGR2RGB).astype(np.float32) / 255
        im = (im - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
        m = sess.run(None, {inp: im.transpose(2, 0, 1)[None].astype(np.float32)})[0][0, 0]
        m = (m - m.min()) / (m.max() - m.min() + 1e-6)
        m = cv2.resize(m, (540, 960)); m = cv2.GaussianBlur(m, (5, 5), 0)
        rgba = cv2.cvtColor(cv2.resize(fr, (540, 960)), cv2.COLOR_BGR2BGRA); rgba[..., 3] = (np.clip((m - .3) / .4, 0, 1) * 255).astype(np.uint8)
        cv2.imwrite(f'{matte_dir}/f{i:04d}.png', rgba)
    i += 1
# fill + smooth (EMA both directions)
first = next(v for v in raw if v)
raw = [v or first for v in raw]
arr = np.array(raw, float)
for _ in range(2):
    for k in range(1, len(arr)): arr[k] = arr[k - 1] * 0.85 + arr[k] * 0.15
    arr = arr[::-1]
json.dump([{'cx': round(a[0]), 'cy': round(a[1]), 'w': round(a[2])} for a in arr], open(faces_out, 'w'))
print(i, 'frames;', len(list(Path(matte_dir).glob('*.png'))), 'mattes; mean face', arr.mean(0).round())
