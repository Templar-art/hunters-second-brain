"""Composite Bebita's real Instagram mirror selfies into arched chrome floor mirrors.
The photo is only cropped and scaled, never repainted; the frame, stand and glass sheen are drawn here."""
import glob, sys
from PIL import Image, ImageDraw, ImageFilter
GROUND = (246, 215, 221)

def chrome(w, h):
    """Vertical-banded brushed chrome: highlight, mid, deep, mid, highlight."""
    g = Image.new("RGB", (w, 1)); px = g.load()
    stops = [(0, 230), (0.18, 250), (0.35, 170), (0.5, 120), (0.65, 175), (0.82, 245), (1, 210)]
    for x in range(w):
        t = x / max(w - 1, 1)
        for (a, va), (b, vb) in zip(stops, stops[1:]):
            if a <= t <= b:
                v = va + (vb - va) * (t - a) / (b - a); break
        px[x, 0] = (int(v), int(v), int(v * 1.02))
    return g.resize((w, h))

def arch_mask(w, h, inset=0):
    m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    r = (w - 2 * inset) / 2
    d.ellipse([inset, inset, w - inset, inset + 2 * r], fill=255)
    d.rectangle([inset, inset + r, w - inset, h - inset], fill=255)
    return m

def tube_arch(canvas, x0, y0, w, h, ring):
    """Draw a round chrome tube as concentric arch outlines, bright along the crown of the tube."""
    d = ImageDraw.Draw(canvas)
    for k in range(ring):
        t = k / max(ring - 1, 1)             # 0 outer edge .. 1 inner edge
        v = 120 + 135 * (1 - abs(t - 0.35) * 1.6) ** 1.5 if abs(t - 0.35) < 0.62 else 110
        c = (int(v), int(v), int(min(v * 1.02, 255)))
        r = (w - 2 * k) / 2
        box = [x0 + k, y0 + k, x0 + w - k, y0 + k + 2 * r]
        d.arc(box, 180, 360, fill=c, width=1)
        d.line([x0 + k, y0 + k + r, x0 + k, y0 + h - 1], fill=c)
        d.line([x0 + w - k - 1, y0 + k + r, x0 + w - k - 1, y0 + h - 1], fill=c)
        d.line([x0 + k, y0 + h - 1 - k, x0 + w - k, y0 + h - 1 - k], fill=c)

def rod(canvas, x, y, w, h):
    g = chrome(w, h); canvas.paste(g, (x, y))

def mirror(photo_path, out, W, H, focus_y=0.42, legs=True):
    S = 3
    w, h = W * S, H * S
    canvas = Image.new("RGB", (w, h), GROUND)
    m = int(w * 0.025)                        # margin the comp keeps around the artwork
    fw = w - 2 * m; fx = m; fy = m
    fh = int((h - 2 * m) * 0.965)
    ring = max(int(fw * 0.042), 6)
    iw, ih = fw - 2 * ring, fh - 2 * ring
    ph = Image.open(photo_path).convert("RGB")
    sc = max(iw / ph.width, ih / ph.height); ph = ph.resize((int(ph.width * sc), int(ph.height * sc)), Image.LANCZOS)
    left = (ph.width - iw) // 2; top = int((ph.height - ih) * focus_y)
    ph = ph.crop((left, top, left + iw, top + ih))
    sheen = Image.new("L", (iw, ih), 0); sd = ImageDraw.Draw(sheen)
    sd.polygon([(int(iw * .62), 0), (int(iw * .78), 0), (int(iw * .30), ih), (int(iw * .14), ih)], fill=20)
    sheen = sheen.filter(ImageFilter.GaussianBlur(iw * .04))
    ph = Image.composite(Image.new("RGB", (iw, ih), (255, 255, 255)), ph, sheen)
    canvas.paste(ph, (fx + ring, fy + ring), arch_mask(iw, ih))
    tube_arch(canvas, fx, fy, fw, fh, ring)
    if legs:
        rw = max(int(ring * 0.8), 4)
        for lx in (fx + int(fw * .07), fx + fw - int(fw * .07) - rw):
            rod(canvas, lx, fy + fh - 1, rw, h - (fy + fh) - m // 2)
    canvas = canvas.resize((W, H), Image.LANCZOS)
    canvas.save(out)

if __name__ == "__main__":
    src, out, W, H = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    fy = float(sys.argv[5]) if len(sys.argv) > 5 else 0.42
    mirror(src, out, W, H, fy)
