"""Render the 10x logo stings to transparent RGBA frames.

Two marks: the 10X symbol and the full "10X VISUALS" wordmark.
Geometry is extracted straight from the brand SVGs — nothing is transcribed.

Motion:
  - the X's two chevrons converge (the mark is literally two halves)
  - the "10" glides in from the left
  - "VISUALS" resolves typographically: it starts wide-tracked and the
    letter-spacing closes to its correct setting. Type behaves like type
    rather than repeating the glide a third time.
  - the glow blooms ONCE as the mark lands, then clears. A looping breath is
    a web behaviour; in a linear cut it is just a pulse the editor trims.

Easing reproduces CSS exactly, including the per-keyframe-interval behaviour
(the timing function applies to EACH keyframe segment, not the whole run).

Alpha: a glow is a wide region of very low alpha. Stored as STRAIGHT alpha it
detonates into a white blob in any compositor that treats the file as
premultiplied. Stored PREMULTIPLIED it is correct there and merely subtler in a
straight compositor — so premultiplied is the safe default for a glowing asset.
"""
import io, os, sys, copy
import xml.etree.ElementTree as ET
import cairosvg
from PIL import Image, ImageFilter, ImageChops

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace('', SVG_NS)
BRAND = "/Users/10xhunter/Desktop/_Brand & Tools/10x-Visuals/Logos & Symbols"

MARK    = os.environ.get("MARK", "symbol")
GLOW    = os.environ.get("GLOW", "1") == "1"
PREMULT = os.environ.get("PREMULT", "1") == "1"
OUT     = os.environ.get("OUTDIR", f"frames_{MARK}")
FPS     = 60
W, H    = 1920, 1080

# travel and blur in viewBox units so both marks move identically
# relative to the artwork rather than to the canvas
TRAVEL_X   = 174.8      # each X chevron, toward the centre
TRAVEL_TEN = 240.3      # the "10", from the left
TRACK      = 15.0       # extra letter-spacing per letter at the start
BLUR_X, BLUR_TEN, BLUR_VIS = 5.83, 7.28, 3.0

GLOW_RADIUS = 14.0      # css px at CSS_REF width — a rim, not a cloud
GLOW_ALPHA  = 0.34
GLOW_RGB    = (97, 168, 216)
GLOW_RISE   = 450       # ms, swell as the mark lands
GLOW_FALL   = 850       # ms, clear away
CSS_REF     = 240.0

_wm_letters = [([i], "vis", i) for i in range(7)]
CONF = {
    "symbol": dict(
        src="10xVisuals_10X Symbol Blue X.svg", mark_w=720,
        groups=[([0], "ten", 0), ([1, 2], "xr", 0), ([3], "ten", 0), ([4], "xl", 0)],
        glow_start=1000),
    "wordmark": dict(
        src="10xVisuals_White Logo Blue X.svg", mark_w=1200,
        groups=_wm_letters + [([7], "ten", 0), ([8, 9], "xr", 0),
                              ([10], "ten", 0), ([11], "xl", 0)],
        glow_start=1150),
}[MARK]

ANIM = {   # name: (delay_ms, dur_ms, travel_vb, blur_vb, ease, opacity_end_pct)
    "xr":  (100, 1000,  TRAVEL_X,   BLUR_X,   "glide", 55),
    "xl":  (100, 1000, -TRAVEL_X,   BLUR_X,   "glide", 55),
    "ten": (480,  950, -TRAVEL_TEN, BLUR_TEN, "glide", 55),
    # travel comes from tracking. A gentler curve than the glide, because the
    # glide front-loads so hard the close finishes before the type is legible.
    "vis": (770,  620, 0.0,         BLUR_VIS, "track", 30),
}


def load_source():
    root = ET.parse(os.path.join(BRAND, CONF["src"])).getroot()
    defs = root.find(f"{{{SVG_NS}}}defs")
    kids = [c for c in root if not c.tag.endswith("defs")]
    vb = [float(v) for v in root.get("viewBox").split()]
    return defs, kids, vb[2], vb[3]


def render_tile(defs, kids, idxs, vb_w, vb_h, tw, th):
    svg = ET.Element(f"{{{SVG_NS}}}svg", {"viewBox": f"0 0 {vb_w} {vb_h}"})
    svg.append(copy.deepcopy(defs))
    for i in idxs:
        svg.append(copy.deepcopy(kids[i]))
    data = ET.tostring(svg, encoding="utf-8", xml_declaration=True)
    return Image.open(io.BytesIO(
        cairosvg.svg2png(bytestring=data, output_width=tw, output_height=th))).convert("RGBA")


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

GLIDE       = cubic_bezier(.19, 1, .22, 1)
TRACK_EASE  = cubic_bezier(.55, .30, .30, 1)
SWELL       = cubic_bezier(.16, 1, .3, 1)
EASE_IN_OUT = cubic_bezier(.42, 0, .58, 1)
EASES = {"glide": GLIDE, "track": TRACK_EASE}


def seg(local_ms, dur_ms, a_pct, b_pct, ease):
    a, b = dur_ms * a_pct / 100.0, dur_ms * b_pct / 100.0
    if local_ms <= a: return 0.0
    if local_ms >= b: return 1.0
    return ease((local_ms - a) / (b - a))


def glow_v(t):
    """One bloom: swell as the mark lands, then clear. No loop."""
    local = t - CONF["glow_start"]
    if local < 0:
        return 0.0
    if local < GLOW_RISE:
        return SWELL(local / GLOW_RISE)
    d = local - GLOW_RISE
    if d < GLOW_FALL:
        return 1.0 - EASE_IN_OUT(d / GLOW_FALL)
    return 0.0


def main():
    os.makedirs(OUT, exist_ok=True)
    defs, kids, vb_w, vb_h = load_source()
    tw = CONF["mark_w"]; th = round(tw * vb_h / vb_w)
    vb2px = tw / vb_w
    css2px = tw / CSS_REF
    bx, by = (W - tw) // 2, (H - th) // 2

    layers = []
    for idxs, anim, track_i in CONF["groups"]:
        tile = render_tile(defs, kids, idxs, vb_w, vb_h, tw, th)
        if tile.getbbox() is None:
            print(f"FATAL: group {idxs} rendered empty", file=sys.stderr); sys.exit(1)
        delay, dur, travel, blur, ease, op_end = ANIM[anim]
        travel = travel + track_i * TRACK      # left-anchored tracking
        layers.append((tile, delay, dur, travel, blur, EASES[ease], op_end))

    # stop one frame after the glow stops changing — never ship dead frames
    written = 0
    n = 1
    while True:
        t_end = (n - 1) * 1000.0 / FPS
        if t_end > CONF["glow_start"] + GLOW_RISE and glow_v(t_end) <= 0.004:
            break
        n += 1
    for f in range(n):
        t = f * 1000.0 / FPS
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for tile, delay, dur, travel, blur_vb, ease, op_end in layers:
            local = t - delay
            if local < 0:
                continue
            op = seg(local, dur, 0, op_end, ease)
            if op <= 0.001:
                continue
            dx = travel * (1 - seg(local, dur, 0, 100, ease)) * vb2px
            bl = blur_vb * (1 - seg(local, dur, 0, 75, ease)) * vb2px
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            lay.paste(tile, (bx + round(dx), by), tile)
            if bl > 0.15:
                lay = lay.filter(ImageFilter.GaussianBlur(bl))
            if op < 0.999:
                lay.putalpha(lay.getchannel("A").point(lambda v: round(v * op)))
            frame = Image.alpha_composite(frame, lay)

        if GLOW:
            v = glow_v(t)
            if v > 0.004:
                std = (GLOW_RADIUS * v / 2.0) * css2px
                halo = Image.new("RGBA", (W, H), GLOW_RGB + (0,))
                a = frame.getchannel("A").filter(ImageFilter.GaussianBlur(std))
                halo.putalpha(a.point(lambda q: round(q * GLOW_ALPHA * v)))
                frame = Image.alpha_composite(halo, frame)

        if PREMULT:
            r, g, b, a = frame.split()
            frame = Image.merge("RGBA", (ImageChops.multiply(r, a),
                                         ImageChops.multiply(g, a),
                                         ImageChops.multiply(b, a), a))

        # skip the empty lead-in so frame 0 already has content
        if written == 0 and frame.getbbox() is None:
            continue
        frame.save(os.path.join(OUT, f"f{written:05d}.png"))
        written += 1
        if written % 60 == 1:
            print(f"  {MARK} frame {written}/{n} t={t:.0f}ms", flush=True)
    print(f"done: {written} frames -> {OUT} (mark={MARK} glow={GLOW} premult={PREMULT})")


if __name__ == "__main__":
    main()
