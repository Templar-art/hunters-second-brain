"""Real face keep-out check: detect every face in the source frame, compare rendered still vs source inside each
(padded) face box. Usage: facecheck2.py <ep_dir> <times csv>  (stills already in build/qa/s_<t>.png)"""
import sys, cv2, numpy as np
ep, ts = sys.argv[1], sys.argv[2].split(',')
fr = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
pr = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")
FPS = 24000 / 1001; bad = []; nf = 0
for t in ts:
    i = min(1205, int(float(t) * FPS) + 1)
    src = cv2.imread(f"{ep}/build/frames/f{i:04d}.jpg"); out = cv2.imread(f"{ep}/build/qa/s_{t}.png")
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    faces = list(fr.detectMultiScale(gray, 1.1, 6, minSize=(70, 70))) + list(pr.detectMultiScale(gray, 1.1, 6, minSize=(70, 70)))
    for (x, y, w, h) in faces:
        nf += 1; x0, y0 = max(0, x - w // 5), max(0, y - h // 3); x1, y1 = min(1080, x + w + w // 5), min(1920, y + h + h // 4)
        d = np.abs(src[y0:y1, x0:x1].astype(int) - out[y0:y1, x0:x1].astype(int)).sum(2)
        cov = (d > 90).mean()
        if cov > .03: bad.append((t, int(x), int(y), round(cov * 100)))
print(f"faces checked: {nf}")
print("FACE CLEAR" if not bad else "FACE COVERED:\n" + "\n".join(f"  {t}s face@({x},{y}) {c}%" for t, x, y, c in bad))
