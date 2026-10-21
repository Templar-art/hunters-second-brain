"""Per time-of-day contact sheets of renders/, ranked by a simple looks score (colourfulness + cloud structure)."""
import json, os
import cv2, numpy as np
meta = json.load(open("polyhaven_skies.json"))
sun = json.load(open("sun_el.json"))
ORDER = ["sunrise", "morning", "midday", "afternoon", "sunset", "dusk", "night"]
groups = {}
for k, m in meta.items():
    t = (m.get("attributes") or {}).get("time_of_day") or "unknown"
    groups.setdefault(t, []).append(k)
import sys; SRC, OUT = (sys.argv[1:3] or ["renders", "sheets"]); os.makedirs(OUT, exist_ok=True)
scores = {}
for t, ks in groups.items():
    rows = []
    for k in ks:
        im = cv2.imread(f"{SRC}/{k}.jpg")
        sky = im[: int(im.shape[0] * 0.55)].astype(np.float32)
        b, g, r = sky[..., 0], sky[..., 1], sky[..., 2]
        rg, yb = r - g, 0.5 * (r + g) - b
        colour = np.hypot(rg.std(), yb.std()) + 0.3 * np.hypot(rg.mean(), yb.mean())
        lum = cv2.cvtColor(sky.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
        structure = cv2.Laplacian(cv2.GaussianBlur(lum, (0, 0), 1.5), cv2.CV_32F).std()
        s = colour + 4 * structure
        scores[k] = round(float(s), 1)
        rows.append((s, k, im))
    rows.sort(key=lambda x: -x[0])
    cols = 6
    tiles = []
    for i, (s, k, im) in enumerate(rows):
        im = cv2.resize(im, (320, 180))
        cv2.rectangle(im, (0, 158), (320, 180), (0, 0, 0), -1)
        cv2.putText(im, f"{i+1}. {k[:30]}", (4, 174), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        tiles.append(im)
    while len(tiles) % cols:
        tiles.append(np.zeros_like(tiles[0]))
    sheet = np.vstack([np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)])
    cv2.imwrite(f"{OUT}/{t}.jpg", sheet, [cv2.IMWRITE_JPEG_QUALITY, 85])
    print(t, len(ks))
json.dump(scores, open(f"{OUT}/scores.json", "w"), indent=0)
