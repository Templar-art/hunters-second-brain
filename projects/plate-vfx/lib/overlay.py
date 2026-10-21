"""Tracked property graphics: lot outlines and pins locked to the ground, rendered as an RGBA layer.

marks.json (frame-1 pixel coordinates; edit the copy freely):
  {"lots": [{"poly": [[x,y],...], "label": "Townhouse block", "sub": "4 residences"}],
   "pins": [{"at": [x,y], "label": "Beach", "sub": "2 min walk"}]}

Look: 10x blue #61a8d8 outline with a soft glow, translucent fill, corner dots, white Poppins label cards on
a thin leader line. Timeline: the outline draws on, the fill fades in, then the pins rise. Rendered at 2x
and downsampled for clean anti-aliasing. Graphics get no grain and no blur.
"""
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import ground

BLUE = (216, 168, 97)  # BGR of #61a8d8
WHITE = (255, 255, 255)
INK = (40, 33, 28)
FONT = os.path.expanduser("~/Library/Fonts/Poppins-SemiBold.ttf")
FONT_REG = os.path.expanduser("~/Library/Fonts/Poppins-Regular.ttf")
SS = 2  # supersampling


def ease(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


class Canvas:
    """Premultiplied BGRA float canvas at SS x resolution."""

    def __init__(self, w, h):
        self.rgb = np.zeros((h * SS, w * SS, 3), np.float32)
        self.a = np.zeros((h * SS, w * SS), np.float32)

    def over(self, mask, color, opacity=1.0):
        m = np.clip(mask, 0, 1) * opacity
        self.rgb = np.array(color, np.float32) * m[..., None] + self.rgb * (1 - m[..., None])
        self.a = m + self.a * (1 - m)

    def blank(self):
        return np.zeros(self.a.shape, np.uint8)

    def straight(self, w, h):
        rgb = cv2.resize(self.rgb, (w, h), interpolation=cv2.INTER_AREA)
        a = cv2.resize(self.a, (w, h), interpolation=cv2.INTER_AREA)
        col = rgb / np.maximum(a[..., None], 1e-6)
        return np.dstack([np.clip(col + 0.5, 0, 255), np.clip(a * 255 + 0.5, 0, 255)]).astype(np.uint8)


def partial_path(pts, frac):
    """Closed polygon -> the first `frac` of its perimeter as an open polyline."""
    loop = np.vstack([pts, pts[:1]])
    seg = np.linalg.norm(np.diff(loop, axis=0), axis=1)
    target = seg.sum() * frac
    out, run = [loop[0]], 0.0
    for p, q, L in zip(loop[:-1], loop[1:], seg):
        if run + L >= target:
            out.append(p + (q - p) * ((target - run) / max(L, 1e-9)))
            break
        out.append(q)
        run += L
    return np.array(out)


def card(text, sub, scale):
    """White rounded label card as BGRA uint8 at SS x."""
    f1 = ImageFont.truetype(FONT, int(30 * scale * SS))
    f2 = ImageFont.truetype(FONT_REG if os.path.exists(FONT_REG) else FONT, int(20 * scale * SS))
    pad, gap = int(18 * scale * SS), int(4 * scale * SS)
    b1 = f1.getbbox(text)
    b2 = f2.getbbox(sub) if sub else (0, 0, 0, 0)
    tw = max(b1[2] - b1[0], b2[2] - b2[0])
    th = (b1[3] - b1[1]) + ((b2[3] - b2[1]) + gap if sub else 0)
    W, H = tw + 2 * pad + int(10 * scale * SS), th + 2 * pad
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=int(10 * scale * SS), fill=(255, 255, 255, 240))
    bar = int(6 * scale * SS)
    d.rounded_rectangle([0, 0, bar * 2, H - 1], radius=int(10 * scale * SS), fill=(97, 168, 216, 255))
    d.rectangle([bar, 0, bar * 2, H - 1], fill=(255, 255, 255, 240))
    x = pad + int(10 * scale * SS)
    d.text((x - b1[0], pad - b1[1]), text, font=f1, fill=(28, 33, 40, 255))
    if sub:
        d.text((x - b2[0], pad + (b1[3] - b1[1]) + gap - b2[1]), sub, font=f2, fill=(97, 120, 140, 255))
    a = np.asarray(im).astype(np.float32)
    return a[..., [2, 1, 0]], a[..., 3] / 255


def paste(cv, rgb, a, x, y, opacity):
    """Paste a card (straight rgb + alpha) with its bottom-centre at (x, y) in SS px."""
    h, w = a.shape
    x0, y0 = int(x - w / 2), int(y - h)
    H, W = cv.a.shape
    sx0, sy0, sx1, sy1 = max(0, -x0), max(0, -y0), min(w, W - x0), min(h, H - y0)
    if sx1 <= sx0 or sy1 <= sy0:
        return
    m = np.zeros(cv.a.shape, np.float32)
    col = np.zeros(cv.rgb.shape, np.float32)
    m[y0 + sy0:y0 + sy1, x0 + sx0:x0 + sx1] = a[sy0:sy1, sx0:sx1]
    col[y0 + sy0:y0 + sy1, x0 + sx0:x0 + sx1] = rgb[sy0:sy1, sx0:sx1]
    mm = m * opacity
    cv.rgb = col * mm[..., None] + cv.rgb * (1 - mm[..., None])
    cv.a = mm + cv.a * (1 - mm)


def render(marks, cam, fps, out_dir, log=print):
    w, h = cam["width"], cam["height"]
    n = len(cam["frames"])
    scale = h / 1080
    lots = [dict(l, track=ground.track(l["poly"], cam)) for l in marks.get("lots", [])]
    pins = [dict(p, track=ground.track([p["at"]], cam)) for p in marks.get("pins", [])]
    cards = {id(o): card(o.get("label", ""), o.get("sub", ""), scale) for o in lots + pins if o.get("label")}
    os.makedirs(out_dir, exist_ok=True)
    lw, lead = 3.0 * scale * SS, 130 * scale * SS
    for k in range(n):
        t = k / fps
        cv = Canvas(w, h)
        for i, lot in enumerate(lots):
            pts = lot["track"][k] * SS
            t0 = i * 0.15
            draw, fill = ease((t - t0) / 0.6), ease((t - t0 - 0.3) / 0.6)
            if fill > 0:
                m = cv.blank(); cv2.fillPoly(m, [pts.astype(np.int32)], 255, cv2.LINE_AA)
                cv.over(m / 255, BLUE, 0.22 * fill)
            if draw > 0:
                path = partial_path(pts, draw).astype(np.int32)
                m = cv.blank(); cv2.polylines(m, [path], False, 255, int(round(lw * 3.5)), cv2.LINE_AA)
                cv.over(cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 6 * SS * scale), BLUE, 0.45)
                m = cv.blank(); cv2.polylines(m, [path], False, 255, int(round(lw)), cv2.LINE_AA)
                cv.over(m / 255, BLUE, 1.0)
                for p in pts[: max(1, int(np.ceil(draw * len(pts))))]:
                    m = cv.blank(); cv2.circle(m, tuple(p.astype(int)), int(6 * scale * SS), 255, -1, cv2.LINE_AA)
                    cv.over(m / 255, WHITE, draw)
                    m = cv.blank(); cv2.circle(m, tuple(p.astype(int)), int(3.5 * scale * SS), 255, -1, cv2.LINE_AA)
                    cv.over(m / 255, BLUE, draw)
            if id(lot) in cards:
                c = pts.mean(0)
                top = pts[:, 1].min()
                rise = ease((t - t0 - 0.5) / 0.5)
                if rise > 0:
                    rgb, a = cards[id(lot)]
                    paste(cv, rgb, a, c[0], top - 18 * scale * SS - (1 - rise) * 20 * scale * SS, rise)
        for j, pin in enumerate(pins):
            p = pin["track"][k][0] * SS
            t0 = 0.45 + j * 0.12
            rise = ease((t - t0) / 0.5)
            if rise <= 0:
                continue
            m = cv.blank(); cv2.ellipse(m, tuple(p.astype(int)), (int(16 * scale * SS), int(6 * scale * SS)), 0, 0, 360, 255, -1, cv2.LINE_AA)
            cv.over(cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 3 * SS), BLUE, 0.6 * rise)
            m = cv.blank(); cv2.circle(m, tuple(p.astype(int)), int(5 * scale * SS), 255, -1, cv2.LINE_AA)
            cv.over(m / 255, WHITE, rise)
            tip = p - np.array([0, lead * rise])
            m = cv.blank(); cv2.line(m, tuple(p.astype(int)), tuple(tip.astype(int)), 255, int(round(lw * 0.8)), cv2.LINE_AA)
            cv.over(m / 255, WHITE, 0.95)
            if id(pin) in cards:
                rgb, a = cards[id(pin)]
                paste(cv, rgb, a, tip[0], tip[1], ease((t - t0 - 0.25) / 0.35))
        cv2.imwrite(os.path.join(out_dir, f"b_{k + 1:04d}.png"), cv.straight(w, h))
    log(f"lines: {len(lots)} lots + {len(pins)} pins over {n} frames -> {out_dir}")
