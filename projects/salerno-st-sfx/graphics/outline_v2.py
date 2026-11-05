"""Salerno St lot outline v2 (Hunter: v1 "dog shit" - 21 px line, lot ~1 width off from a hand-fit affine).
Lot from cadastre/v2/lot_last.json (cadastre -> QLD ortho -> ECC homography, side lines out to the detected kerb).
Track: SIFT homography chain from the last frame back through the top-down (src f833-899).
Draw: Buckingham Way spec - 0.0033*W line (13 px at 4K), round joins, smoothstep draw-on, starts frame 22 (1-based)."""
import cv2, json, numpy as np, subprocess
D = 'graphics/main/frames/f_%04d.png'; N = 67; W, Hh = 3840, 2160
poly = np.float32(json.load(open('cadastre/v2/lot_last.json'))['poly_to_kerb_last_4k'])
sift = cv2.SIFT_create(4000); sc = 0.4
def kd(i):
    g = cv2.resize(cv2.cvtColor(cv2.imread(D % i), cv2.COLOR_BGR2GRAY), None, fx=sc, fy=sc)
    return sift.detectAndCompute(g, None)
Hs = {N: np.eye(3)}; prev = kd(N)
for i in range(N - 1, 0, -1):
    cur = kd(i); m = cv2.BFMatcher().knnMatch(cur[1], prev[1], k=2)
    g = [a for a, b in m if a.distance < 0.75 * b.distance]
    if len(g) < 30: print('lost', i); break
    a = np.float32([cur[0][x.queryIdx].pt for x in g]) / sc; b = np.float32([prev[0][x.trainIdx].pt for x in g]) / sc
    h, _ = cv2.findHomography(a, b, cv2.RANSAC, 4); Hs[i] = Hs[i + 1] @ h; prev = cur
track = {i: cv2.perspectiveTransform(poly[None], np.linalg.inv(Hs[i]))[0] for i in Hs}
json.dump({i: v.tolist() for i, v in track.items()}, open('graphics/out/outline_v2_track.json', 'w'))
START, DRAW, SS = 22, 14, 2; LW = max(2, round(W * 0.0033))
def smooth(t): t = min(max(t, 0.0), 1.0); return t * t * (3 - 2 * t)
def partial(p, frac):
    pts = np.vstack([p, p[:1]]); seg = np.linalg.norm(np.diff(pts, axis=0), axis=1); tgt, out = seg.sum() * frac, [pts[0]]
    for a, b, L in zip(pts[:-1], pts[1:], seg):
        if tgt >= L: out.append(b); tgt -= L
        else: out.append(a + (b - a) * tgt / L); break
    return np.array(out)
import os; os.makedirs('graphics/out/ol2', exist_ok=True); os.makedirs('graphics/out/olp2', exist_ok=True)
for i in range(1, N + 1):
    cv_ = np.zeros((Hh * SS, W * SS), np.uint8); frac = smooth((i - START + 1) / DRAW)
    if i >= START and i in track and frac > 0:
        path = partial(track[i], frac) * SS
        cv2.polylines(cv_, [np.round(path * 16).astype(np.int32)], frac >= 1, 255, LW * SS, cv2.LINE_AA, shift=4)
        for x, y in path: cv2.circle(cv_, (int(round(x * 16)), int(round(y * 16))), LW * SS // 2 * 16, 255, -1, cv2.LINE_AA, shift=4)
    a = cv2.resize(cv_, (W, Hh), interpolation=cv2.INTER_AREA)
    im = np.zeros((Hh, W, 4), np.uint8); im[..., :3] = 255; im[..., 3] = a
    cv2.imwrite('graphics/out/ol2/o_%04d.png' % i, im)
    f = cv2.imread(D % i).astype(np.float32); al = a[..., None] / 255.
    cv2.imwrite('graphics/out/olp2/p_%04d.jpg' % i, (f * (1 - al) + 255 * al).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 92])
fps = '24000/1001'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', fps, '-i', 'graphics/out/ol2/o_%04d.png', '-c:v', 'prores_ks', '-profile:v', '4444',
                '-pix_fmt', 'yuva444p10le', 'graphics/out/Salerno_Outline_TopDown_v2_4444.mov'], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', fps, '-i', 'graphics/out/olp2/p_%04d.jpg', '-vf', 'scale=1920:-2', '-c:v', 'libx264',
                '-crf', '16', '-pix_fmt', 'yuv420p', 'graphics/out/outline_v2_preview.mp4'], check=True)
print('done, tracked from', min(Hs))
