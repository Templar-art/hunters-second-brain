"""Render the 10x logo stings to transparent RGBA frames.

Two marks: the 10X symbol and the full "10X VISUALS" wordmark.
Geometry is extracted straight from the brand SVGs — nothing is transcribed.

Easing reproduces the CSS animation exactly, including the per-keyframe-interval
behaviour CSS uses (the timing function applies to EACH keyframe segment).

Alpha note: a glow is a wide region of very low alpha. Stored as STRAIGHT alpha
(colour independent of alpha) it detonates into a white blob in any compositor
that treats the file as premultiplied. Stored PREMULTIPLIED it is correct there
and merely subtler in a straight compositor, so premultiplied is the safe
default for any glowing asset.
"""
import io, os, sys, copy
import xml.etree.ElementTree as ET
import cairosvg
from PIL import Image, ImageFilter, ImageChops

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace('', SVG_NS)
BRAND = "/Users/10xhunter/Desktop/_Brand & Tools/10x-Visuals/Logos & Symbols"

MARK    = os.environ.get("MARK", "symbol")            # symbol | wordmark
GLOW    = os.environ.get("GLOW", "1") == "1"
PREMULT = os.environ.get("PREMULT", "1") == "1"
OUT     = os.environ.get("OUTDIR", f"frames_{MARK}")
FPS     = 60
W, H    = 1920, 1080

# travel and blur are held in viewBox units so both marks move identically
# relative to the artwork rather than to the canvas
TRAVEL_X   = 174.8      # each X chevron, toward the centre
TRAVEL_TEN = 240.3      # the "10", from the left
TRAVEL_VIS = 52.0       # "VISUALS", emerging rightward from the mark
BLUR_X, BLUR_TEN, BLUR_VIS = 5.83, 7.28, 4.0

GLOW_RADIUS = 14.0      # css px at CSS_REF width — tighter than a cloud
GLOW_ALPHA  = 0.34
GLOW_RGB    = (97, 168, 216)
CSS_REF     = 240.0     # the css width the timings were authored against

CONF = {
    "symbol": dict(
        src="10xVisuals_10X Symbol Blue X.svg", mark_w=720,
        groups=[([0], "ten"), ([1, 2], "xr"), ([3], "ten"), ([4], "xl")],
        glow_start=950, duration=3550),
    "wordmark": dict(
        src="10xVisuals_White Logo Blue X.svg", mark_w=1200,
        groups=[(list(range(0, 7)), "vis"), ([7], "ten"),
                ([8, 9], "xr"), ([10], "ten"), ([11], "xl")],
        glow_start=1500, duration=4100),
}[MARK]

ANIM = {   # name: (delay_ms, dur_ms, travel_vb, blur_vb)
    "xr":  (100, 1000,  TRAVEL_X,   BLUR_X),
    "xl":  (100, 1000, -TRAVEL_X,   BLUR_X),
    "ten": (500,  950, -TRAVEL_TEN, BLUR_TEN),
    "vis": (850,  850, -TRAVEL_VIS, BLUR_VIS),
}


def load_source():
    tree = ET.parse(os.path.join(BRAND, CONF["src"]))
    root = tree.getroot()
    defs = root.find(f"{{{SVG_NS}}}defs")
    kids = [c for c in root if not c.tag.endswith("defs")]
    vb = [float(v) for v in root.get("viewBox").split()]
    return defs, kids, vb[2], vb[3]


def render_tile(defs, kids, idxs, vb_w, vb_h, tile_w, tile_h):
    svg = ET.Element(f"{{{SVG_NS}}}svg", {"viewBox": f"0 0 {vb_w} {vb_h}"})
    svg.append(copy.deepcopy(defs))
    for i in idxs:
        svg.append(copy.deepcopy(kids[i]))
    data = ET.tostring(svg, encoding="utf-8", xml_declaration=True)
    png = cairosvg.svg2png(bytestring=data, output_width=tile_w, output_height=tile_h)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def cubic_bezier(x1, y1, x2, y2):
    def bez(a, b, t):
        mt = 1 - t
        return 3 * mt * mt * t * a + 3 * mt * t * t * b + t ** 3
    def f(x):
        if x <= 0: return 0.0
        if x >= 1: return 1.0
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if bez(x1, x2, mid) < x: lo = mid
            else: hi = mid
        return bez(y1, y2, (lo + hi) / 2)
    return f

GLIDE = cubic_bezier(.19, 1, .22, 1)
EASE_IN_OUT = cubic_bezier(.42, 0, .58, 1)


def seg(local_ms, dur_ms, a_pct, b_pct, ease):
    a, b = dur_ms * a_pct / 100.0, dur_ms * b_pct / 100.0
    if local_ms <= a: return 0.0
    if local_ms >= b: return 1.0
    return ease((local_ms - a) / (b - a))


def main():
    os.makedirs(OUT, exist_ok=True)
    defs, kids, vb_w, vb_h = load_source()
    tile_w = CONF["mark_w"]
    tile_h = round(tile_w * vb_h / vb_w)
    vb2px = tile_w / vb_w                      # viewBox unit -> render px
    css2px = tile_w / CSS_REF                  # css px -> render px (glow only)
    bx, by = (W - tile_w) // 2, (H - tile_h) // 2

    layers = []
    for idxs, anim in CONF["groups"]:
        tile = render_tile(defs, kids, idxs, vb_w, vb_h, tile_w, tile_h)
        if tile.getbbox() is None:
            print(f"FATAL: group {idxs} rendered empty", file=sys.stderr); sys.exit(1)
        layers.append((tile, ANIM[anim]))

    n = round(CONF["duration"] / 1000 * FPS)
    for f in range(n):
        t = f * 1000.0 / FPS
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for tile, (delay, dur, travel, blur_vb) in layers:
            local = t - delay
            if local < 0:
                continue                        # base style: opacity 0
            op = seg(local, dur, 0, 55, GLIDE)
            if op <= 0.001:
                continue
            dx = travel * (1 - seg(local, dur, 0, 100, GLIDE)) * vb2px
            bl = blur_vb * (1 - seg(local, dur, 0, 75, GLIDE)) * vb2px
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            lay.paste(tile, (bx + round(dx), by), tile)
            if bl > 0.15:
                lay = lay.filter(ImageFilter.GaussianBlur(bl))
            if op < 0.999:
                lay.putalpha(lay.getchannel("A").point(lambda v: round(v * op)))
            frame = Image.alpha_composite(frame, lay)

        if GLOW:
            local = t - CONF["glow_start"]
            if local >= 0:
                p = (local % 2600) / 2600.0
                v = EASE_IN_OUT(p / .5) if p < .5 else EASE_IN_OUT((1 - p) / .5)
                if v > 0.004:
                    std = (GLOW_RADIUS * v / 2.0) * css2px
                    halo = Image.new("RGBA", (W, H), GLOW_RGB + (0,))
                    a = frame.getchannel("A").filter(ImageFilter.GaussianBlur(std))
                    halo.putalpha(a.point(lambda q: round(q * GLOW_ALPHA * v)))
                    frame = Image.alpha_composite(halo, frame)

        if PREMULT:
            # premultiply: colour *= alpha. ImageChops.multiply is (a*b)/255,
            # which is exactly the premultiply, and runs in C.
            r, g, b, a = frame.split()
            frame = Image.merge("RGBA", (ImageChops.multiply(r, a),
                                         ImageChops.multiply(g, a),
                                         ImageChops.multiply(b, a), a))

        frame.save(os.path.join(OUT, f"f{f:05d}.png"))
        if f % 60 == 0:
            print(f"  {MARK} frame {f}/{n} t={t:.0f}ms", flush=True)
    print(f"done: {n} frames -> {OUT} (mark={MARK} glow={GLOW} premult={PREMULT})")


if __name__ == "__main__":
    main()
