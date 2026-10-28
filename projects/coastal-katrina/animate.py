"""Animated end card + Coastal C° drone pin, 4K ProRes 4444 with alpha (25 fps).

end card (8 s): charcoal background fades up over footage, then name, number and
COASTAL° wordmark ease in one after another (fade + small rise), held to the end.
pin (5 s): thin white stem draws up from the ground point, C° mark fades/settles on top.
Pin proportions measured from Coastal's own listing drone stills (4 Lita Ct).

Usage: python3 animate.py            -> out/*.mov + out/coastal-pin-4k.png
"""
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import make_cards as mc  # noqa: E402

W, H, FPS = mc.W, mc.H, 25
OUT = mc.OUT
PIN_MARK = mc.VAULT / "projects/drone-pin/logos/coastal-c-white.png"


def ease_out(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def phase(t, start, dur):
    return ease_out((t - start) / dur)


def layer(draw_fn):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(img), img)
    return np.asarray(img).astype(np.float32) / 255


def over(dst, src, alpha=1.0, dy=0):
    """Premultiplied-free 'over' of src (float RGBA) onto dst, scaled by alpha, shifted down dy px."""
    if alpha <= 0:
        return
    if dy:
        src = np.roll(src, int(round(dy)), axis=0)
    a = src[..., 3:4] * alpha
    da = dst[..., 3:4]
    out_a = a + da * (1 - a)
    safe = np.where(out_a == 0, 1, out_a)
    dst[..., :3] = (src[..., :3] * a + dst[..., :3] * da * (1 - a)) / safe
    dst[..., 3:4] = out_a


def encode(frames_fn, n, path):
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
           "-vendor", "apl0", str(path)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write((np.clip(frames_fn(i / FPS), 0, 1) * 255).astype(np.uint8).tobytes())
    p.stdin.close()
    p.wait()


def end_card():
    blank = np.zeros((H, W, 4), np.float32)
    name = layer(lambda d, i: mc.centred(d, "KATRINA WALSH", mc.font(mc.LIGHT, 190), cy=H * 0.30))
    num = layer(lambda d, i: mc.centred(d, "0429 899 295", mc.font(mc.LIGHT, 190), cy=H * 0.30 + 225))

    def logo_draw(d, img):
        logo = Image.open(mc.LOGO_WHITE).convert("RGBA")
        lw = int(W * 0.30)
        logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
        img.alpha_composite(logo, ((W - lw) // 2, int(H * 0.87) - logo.height // 2))
    logo = layer(logo_draw)

    plain = np.asarray(mc.end_card_background()).astype(np.float32) / 255

    def frame(t):
        f = blank.copy()
        over(f, plain, phase(t, 0.0, 1.0))
        for lyr, start in ((name, 0.6), (num, 0.9), (logo, 1.5)):
            k = phase(t, start, 1.0)
            over(f, lyr, k, dy=(1 - k) * 24)
        return f

    encode(frame, 8 * FPS, OUT / "katrina-walsh-end-card-anim-4k.mov")


def pin():
    # 4K-frame scale from Lita Ct stills (1400 px wide): C° ~68 px wide, stem ~265 px, ~2.5 px thick.
    k = W / 1400
    mark = Image.open(PIN_MARK).convert("RGBA")
    mw = round(68 * k)
    mark = mark.resize((mw, round(mark.height * mw / mark.width)), Image.LANCZOS)
    stem_len, stem_w, gap = round(265 * k), max(2, round(2.5 * k)), round(10 * k)
    gx, gy = W // 2, int(H * 0.72)              # ground point (move the clip in the edit)
    c_centre_x = gx + round(mark.width * 0.08)   # stem sits under the C, not the degree ring
    stem_top = gy - stem_len

    def draw_pin(stem_frac, mark_alpha, mark_scale):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        top = gy - round(stem_len * stem_frac)
        if stem_frac > 0:
            d.rectangle([gx - stem_w // 2, top, gx - stem_w // 2 + stem_w - 1, gy], fill=(255, 255, 255, 255))
        if mark_alpha > 0:
            m = mark.resize((max(1, round(mark.width * mark_scale)), max(1, round(mark.height * mark_scale))), Image.LANCZOS)
            a = m.getchannel("A").point(lambda v: round(v * mark_alpha))
            m.putalpha(a)
            img.alpha_composite(m, (c_centre_x - m.width // 2 - round(mark.width * 0.08 * mark_scale),
                                    stem_top - gap - m.height))
        return img

    still = draw_pin(1, 1, 1)
    still.save(OUT / "coastal-pin-4k.png")
    still.crop(still.getbbox()).save(OUT / "coastal-pin-tight.png")

    def frame(t):
        s = phase(t, 0.0, 0.7)
        m = phase(t, 0.5, 0.6)
        return np.asarray(draw_pin(s, m, 0.92 + 0.08 * m)).astype(np.float32) / 255

    encode(frame, 5 * FPS, OUT / "coastal-pin-anim-4k.mov")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    end_card()
    pin()
    print("written to", OUT)
