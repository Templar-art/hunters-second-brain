"""Render the 10x logo sting to transparent RGBA frames.

Replicates the CSS animation exactly, including the per-keyframe-interval
easing behaviour that CSS uses (the timing function is applied to EACH
keyframe segment, not across the whole animation).
"""
import io, os, sys, math
import cairosvg
from PIL import Image, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")
os.makedirs(OUT, exist_ok=True)

W, H = 1920, 1080
MARK_W = 720                      # rendered mark width in the 1920x1080 frame
CSS_MARK_W = 240                  # mark width the CSS was authored against
K = MARK_W / CSS_MARK_W           # px scale factor for offsets and blurs
FPS = 60
DURATION_MS = 3550                # ends exactly where the glow returns to zero

VB_W, VB_H = 349.575, 262.074
TILE_W = MARK_W
TILE_H = round(MARK_W * VB_H / VB_W)
BASE_X = (W - TILE_W) // 2
BASE_Y = (H - TILE_H) // 2

DEFS = '''
<clipPath id="clip-1"><path d="M 222 20 L 327 20 L 327 132 L 222 132 Z M 222 20 "/></clipPath>
<clipPath id="clip-2"><path d="M 287.886719 20.414062 L 222.839844 103.007812 L 241.789062 131.328125 L 326.578125 20.414062 Z M 287.886719 20.414062 "/></clipPath>
<linearGradient id="lp0" gradientUnits="userSpaceOnUse" x1="-0.117504" y1="0" x2="1.399438" y2="0" gradientTransform="matrix(57.637654, -80.787205, 80.787205, 57.637654, 231.070094, 122.876391)">
<stop offset="0" stop-color="rgb(20%,47.06%,61.96%)"/><stop offset="0.5" stop-color="rgb(31%,60%,76%)"/><stop offset="1" stop-color="rgb(38.04%,65.88%,84.70%)"/>
</linearGradient>
<clipPath id="clip-3"><path d="M 219 131 L 289 131 L 289 201 L 219 201 Z M 219 131 "/></clipPath>
<clipPath id="clip-4"><path d="M 248.371094 200.738281 L 288.0625 200.738281 L 241.789062 131.328125 L 219.847656 157.855469 Z M 248.371094 200.738281 "/></clipPath>
<linearGradient id="lp1" gradientUnits="userSpaceOnUse" x1="-0.0610797" y1="0" x2="1.122118" y2="0" gradientTransform="matrix(50.551057, 64.251812, -64.251812, 50.551057, 221.655575, 136.260999)">
<stop offset="0" stop-color="rgb(20%,47.06%,61.96%)"/><stop offset="0.5" stop-color="rgb(31%,60%,76%)"/><stop offset="1" stop-color="rgb(38.04%,65.88%,84.70%)"/>
</linearGradient>
<clipPath id="clip-5"><path d="M 116 60 L 242 60 L 242 241 L 116 241 Z M 116 60 "/></clipPath>
<clipPath id="clip-6"><path d="M 155.027344 60.722656 L 200.898438 129.535156 L 116.023438 240.738281 L 154.71875 240.738281 L 219.847656 157.855469 L 241.789062 131.328125 L 222.839844 103.007812 L 194.714844 60.722656 Z M 155.027344 60.722656 "/></clipPath>
<linearGradient id="lp2" gradientUnits="userSpaceOnUse" x1="0.103485" y1="0" x2="1.04076" y2="0" gradientTransform="matrix(134.182152, 0, 0, 134.182152, 102.139323, 150.730465)">
<stop offset="0" stop-color="rgb(20%,47.06%,61.96%)"/><stop offset="0.5" stop-color="rgb(30%,57%,73%)"/><stop offset="1" stop-color="rgb(38.04%,65.88%,84.70%)"/>
</linearGradient>
'''

NUM_ONE = '<path fill-rule="nonzero" fill="#fff" d="M 22.574219 93.394531 L 22.574219 63.539062 L 74.585938 63.539062 L 74.585938 200.609375 L 41.164062 200.609375 L 41.164062 93.394531 Z M 22.574219 93.394531 "/>'

STROKE_UPPER = '''
<g clip-path="url(#clip-1)"><g clip-path="url(#clip-2)"><path fill-rule="nonzero" fill="url(#lp0)" d="M 170.398438 93.917969 L 291.585938 180.375 L 379.019531 57.828125 L 257.832031 -28.632812 Z M 170.398438 93.917969 "/></g></g>
<g clip-path="url(#clip-3)"><g clip-path="url(#clip-4)"><path fill-rule="nonzero" fill="url(#lp1)" d="M 261.984375 98.179688 L 186.117188 157.867188 L 245.929688 233.890625 L 321.792969 174.203125 Z M 261.984375 98.179688 "/></g></g>
'''

NUM_ZERO = '<path fill-rule="nonzero" fill="#fff" d="M 119.496094 101.589844 C 122.246094 94.769531 127.945312 91.359375 136.582031 91.359375 C 145.21875 91.359375 150.914062 94.769531 153.671875 101.589844 C 156.421875 108.414062 157.800781 118.148438 157.800781 130.789062 C 157.800781 139.300781 157.300781 146.347656 156.300781 151.914062 C 155.296875 157.484375 153.261719 161.988281 150.199219 165.433594 C 147.128906 168.875 142.589844 170.59375 136.582031 170.59375 C 130.574219 170.59375 126.035156 168.875 122.96875 165.433594 C 119.902344 161.988281 117.867188 157.484375 116.867188 151.914062 C 115.863281 146.347656 115.367188 139.300781 115.367188 130.789062 C 115.367188 118.148438 116.742188 108.414062 119.496094 101.589844 M 134.816406 200.5625 L 189.308594 129.164062 C 189.308594 129.164062 189.308594 129.160156 189.308594 129.160156 L 147.171875 65.957031 L 144.371094 61.757812 C 141.871094 61.488281 139.300781 61.316406 136.582031 61.316406 C 118.054688 61.316406 104.628906 67.511719 96.304688 79.902344 C 87.980469 92.296875 83.820312 109.257812 83.820312 130.789062 C 83.820312 152.570312 87.980469 169.65625 96.304688 182.046875 C 104.355469 194.035156 117.222656 200.167969 134.816406 200.5625 "/>'

STROKE_LOWER = '<g clip-path="url(#clip-5)"><g clip-path="url(#clip-6)"><path fill-rule="nonzero" fill="url(#lp2)" d="M 116.023438 60.722656 L 116.023438 240.738281 L 241.789062 240.738281 L 241.789062 60.722656 Z M 116.023438 60.722656 "/></g></g>'


def render_tile(body):
    svg = ('<?xml version="1.0" encoding="UTF-8"?>'
           f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB_W} {VB_H}">'
           f'<defs>{DEFS}</defs>{body}</svg>')
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=TILE_W, output_height=TILE_H)
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

GLIDE = cubic_bezier(.19, 1, .22, 1)      # cubic-bezier(.19,1,.22,1)
EASE_IN_OUT = cubic_bezier(.42, 0, .58, 1)


def seg(local_ms, dur_ms, start_pct, end_pct, ease):
    """Progress through one keyframe interval, eased the way CSS does it."""
    a = dur_ms * start_pct / 100.0
    b = dur_ms * end_pct / 100.0
    if local_ms <= a: return 0.0
    if local_ms >= b: return 1.0
    return ease((local_ms - a) / (b - a))


class Layer:
    def __init__(self, tile, delay, dur, from_x, blur_css):
        self.tile, self.delay, self.dur = tile, delay, dur
        self.from_x, self.blur_css = from_x, blur_css

    def state(self, t):
        local = t - self.delay
        if local < 0:
            return None                              # base style: opacity 0
        tx = seg(local, self.dur, 0, 100, GLIDE)
        op = seg(local, self.dur, 0, 55, GLIDE)
        bl = seg(local, self.dur, 0, 75, GLIDE)
        return (self.from_x * (1 - tx) * K,           # x offset, render px
                op,
                self.blur_css * (1 - bl) * K)         # blur stdDev, render px


def compose(layers, t):
    logo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for lay in layers:
        st = lay.state(t)
        if st is None:
            continue
        dx, op, blur = st
        if op <= 0.001:
            continue
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        canvas.paste(lay.tile, (BASE_X + round(dx), BASE_Y), lay.tile)
        if blur > 0.15:
            canvas = canvas.filter(ImageFilter.GaussianBlur(blur))
        if op < 0.999:
            a = canvas.getchannel("A").point(lambda v: round(v * op))
            canvas.putalpha(a)
        logo = Image.alpha_composite(logo, canvas)
    return logo


def glow_params(t):
    """glow 2.6s ease-in-out .95s infinite — interpolates radius and alpha."""
    local = t - 950
    if local < 0:
        return 0.0, 0.0
    p = (local % 2600) / 2600.0
    v = EASE_IN_OUT(p / 0.5) if p < 0.5 else EASE_IN_OUT((1 - p) / 0.5)
    return 20.0 * v, 0.30 * v          # css radius px, alpha


def main():
    tiles = [render_tile(NUM_ONE), render_tile(STROKE_UPPER),
             render_tile(NUM_ZERO), render_tile(STROKE_LOWER)]
    for i, tl in enumerate(tiles):
        if tl.getbbox() is None:
            print(f"FATAL: tile {i} rendered empty", file=sys.stderr); sys.exit(1)

    layers = [
        Layer(tiles[0], 500, 950, -165, 5),   # numOne   (the "10", moves as one)
        Layer(tiles[1], 100, 1000, 120, 4),   # strokeUpper — right chevron
        Layer(tiles[2], 500, 950, -165, 5),   # numZero
        Layer(tiles[3], 100, 1000, -120, 4),  # strokeLower — left chevron
    ]

    n = round(DURATION_MS / 1000 * FPS)
    for f in range(n):
        t = f * 1000.0 / FPS
        logo = compose(layers, t)
        radius, alpha = glow_params(t)
        if alpha > 0.002 and radius > 0.05:
            std = (radius / 2.0) * K                      # drop-shadow: stdDev = radius/2
            shadow = Image.new("RGBA", (W, H), (97, 168, 216, 0))
            a = logo.getchannel("A").filter(ImageFilter.GaussianBlur(std))
            shadow.putalpha(a.point(lambda v: round(v * alpha)))
            frame = Image.alpha_composite(shadow, logo)
        else:
            frame = logo
        frame.save(os.path.join(OUT, f"f{f:05d}.png"))
        if f % 30 == 0:
            print(f"  frame {f}/{n}  t={t:.0f}ms", flush=True)
    print(f"done: {n} frames -> {OUT}")


if __name__ == "__main__":
    main()
