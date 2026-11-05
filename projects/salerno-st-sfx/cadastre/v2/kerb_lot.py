"""v2 lot for 42 Salerno St in the top-down's last frame (4K).
Cadastre lot 231RP110045 (MGA56) -> QLD LatestStateProgram ortho px -> frame via ECC homography on edge maps
(H_ortho2last.npy; v1's hand-fit affine was ~1 lot width off). Side lines extended outward to the kerb, found
as the first sustained (>=100 px) low-saturation asphalt run, so the concrete footpath is skipped, along each side line (Hunter: "goto the street")."""
import cv2, json, numpy as np, sys
D = 'cadastre/v2/'
H = np.load(D + 'H_ortho2last.npy'); fr = cv2.imread('graphics/main/frames/f_0067.png')
p = np.float64(json.load(open('cadastre/lot_mga.json'))['features'][0]['geometry']['rings'][0][:4])
q = cv2.perspectiveTransform(np.float32(np.c_[(p[:, 0] - 541385.16) / 120 * 1600, (6901236.63 - p[:, 1]) / 120 * 1600])[None], H)[0]
o = np.argsort(q @ np.float32([1, 1])); front, back = q[o[:2]], q[o[2:]]
hsv = cv2.cvtColor(fr, cv2.COLOR_BGR2HSV).astype(np.float32)
kerb = []
for f in front:
    b = back[np.argmin(np.linalg.norm(back - f, axis=1))]; u = (f - b) / np.linalg.norm(f - b)
    sat = []
    for t in range(0, 700, 2):
        x, y = (f + u * t).astype(int)
        sat.append(hsv[max(y - 3, 0):y + 4, max(x - 3, 0):x + 4, 1].mean() if 0 <= x < 3840 and 0 <= y < 2160 else np.nan)
    sat = np.array(sat); lo = sat < 80
    i = next(i for i in range(len(lo) - 50) if (lo[i:i + 50] | np.isnan(sat[i:i + 50])).all() and lo[i])
    kerb.append((f + u * 2 * i, b, 2 * i))
print('kerb offsets px', [k[2] for k in kerb])
# straight street: kerb edge parallel to the frontage at the mean detected offset
off = np.mean([k[2] for k in kerb])
ext = [k[1] + (f - k[1]) / np.linalg.norm(f - k[1]) * (np.linalg.norm(f - k[1]) + off) for f, k in zip(front, kerb)]
poly = np.float32([ext[0], ext[1], kerb[1][1], kerb[0][1]])
json.dump({'lot_last_4k': q.tolist(), 'poly_to_kerb_last_4k': poly.tolist()}, open(D + 'lot_last.json', 'w'))
if len(sys.argv) > 1:
    f = fr.copy(); cv2.polylines(f, [q.astype(np.int32)], True, (0, 255, 255), 4)
    cv2.polylines(f, [np.round(poly * 16).astype(np.int32)], True, (255, 255, 255), 13, cv2.LINE_AA, shift=4)
    cv2.imwrite(sys.argv[1], cv2.resize(f, (1920, 1080)))
