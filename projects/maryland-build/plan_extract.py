"""Read the Kollosche floor plan (raw/18-maryland/floorplan-kollosche-2000.jpg) into masks in metres.

  python3 plan_extract.py            -> plan.npz (wall / header / footprint / deck masks per level) + plan_check.jpg

Walls are the dark strokes (gray < 120) after dropping small components (text, fixtures). Gaps in a wall line are
openings: header.mask bridges collinear gaps up to MAXGAP so the build can put a lintel above them. Upper level and
guest house are registered onto the ground level in plan pixels (DX/DY measured from the matching side verandahs).
"""
import cv2
import numpy as np

SRC = "../../raw/18-maryland/floorplan-kollosche-2000.jpg"
UP = 3                     # supersample before thresholding
PX_PER_M = 13.1            # in the 2000 px plan, from the room dimensions (garage 6.0 x 9.0, media 5.7 x 6.2)
MAXGAP = 3.2               # widest opening bridged by a header (m)
# plan-pixel boxes (x0, y0, x1, y1) of each drawing, and the upper level's offset onto the ground level
BOX = {"ground": (600, 320, 1000, 632), "upper": (962, 440, 1352, 678), "guest": (1078, 320, 1304, 412)}
UPPER_DX, UPPER_DY = -355.5, -80.0


def walls(g):
    m = (g < 120).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros_like(m)
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if max(w, h) > UP * PX_PER_M * 1.2 and a > 300:
            keep[lab == i] = 1
    return keep


def headers(w):
    k = int(UP * PX_PER_M * 0.9)
    hs = cv2.morphologyEx(w, cv2.MORPH_OPEN, np.ones((1, k), np.uint8))      # horizontal strokes only
    vs = cv2.morphologyEx(w, cv2.MORPH_OPEN, np.ones((k, 1), np.uint8))
    g = int(UP * PX_PER_M * MAXGAP)
    hc = cv2.morphologyEx(hs, cv2.MORPH_CLOSE, np.ones((1, g), np.uint8))
    vc = cv2.morphologyEx(vs, cv2.MORPH_CLOSE, np.ones((g, 1), np.uint8))
    return ((hc | vc) & (1 - w)).astype(np.uint8)


def footprint(w, h):
    shell = cv2.dilate(w | h, np.ones((5, 5), np.uint8))
    ff = shell.copy() * 255; H, W = ff.shape
    mask = np.zeros((H + 2, W + 2), np.uint8)
    cv2.floodFill(ff, mask, (0, 0), 128)
    return ((ff != 128)).astype(np.uint8)


def decks(g, w, foot):
    """Paved / tiled outdoor areas: grey-beige, not white, not wall, outside the footprint."""
    m = ((g < 240) & (g > 60)).astype(np.uint8) & (1 - cv2.dilate(w, np.ones((7, 7), np.uint8))) & (1 - foot)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    out = np.zeros_like(m); a_min = (UP * PX_PER_M) ** 2 * 5
    for i in range(1, n):
        if st[i][4] > a_min:
            out[lab == i] = 1
    return cv2.morphologyEx(out, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))


def level(gray, box):
    x0, y0, x1, y1 = box
    g = cv2.resize(gray[y0:y1, x0:x1], None, fx=UP, fy=UP, interpolation=cv2.INTER_CUBIC)
    w = walls(g); h = headers(w); f = footprint(w, h); d = decks(g, w, f)
    return dict(wall=w, header=h, foot=f, deck=d)


if __name__ == "__main__":
    gray = cv2.cvtColor(cv2.imread(SRC), cv2.COLOR_BGR2GRAY)
    out = {}
    for name, box in BOX.items():
        for k, v in level(gray, box).items():
            out[f"{name}_{k}"] = v
    origin = {n: np.array(b[:2], float) for n, b in BOX.items()}
    origin["upper"] = origin["upper"] + [UPPER_DX, UPPER_DY]   # upper drawing -> ground plan pixels
    np.savez_compressed("plan.npz", **out, **{f"{n}_origin": o for n, o in origin.items()},
                        px_per_m=PX_PER_M * UP)
    vis = []
    for name in BOX:
        im = np.full(out[name + "_wall"].shape + (3,), 255, np.uint8)
        im[out[name + "_foot"] > 0] = (235, 225, 200); im[out[name + "_deck"] > 0] = (150, 200, 230)
        im[out[name + "_header"] > 0] = (0, 160, 0); im[out[name + "_wall"] > 0] = (0, 0, 200)
        vis.append(cv2.resize(im, None, fx=0.5, fy=0.5))
    hmax = max(v.shape[0] for v in vis)
    cv2.imwrite("plan_check.jpg", np.hstack([np.pad(v, ((0, hmax - v.shape[0]), (0, 8), (0, 0)), constant_values=255) for v in vis]))
    for name in BOX:
        f = out[name + "_foot"]; print(name, "footprint", round(f.sum() / (PX_PER_M * UP) ** 2, 1), "m2",
                                       "deck", round(out[name + "_deck"].sum() / (PX_PER_M * UP) ** 2, 1), "m2")
