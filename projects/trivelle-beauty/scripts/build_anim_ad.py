"""Trivelle animated ad (9:16, ~24 s): 6 flat illustrations, slow push-ins, mode labels that pop in,
karaoke captions, soft music, logo end card. Reuses caption/mix helpers from build_ads_v2.py.
Usage: python3 build_anim_ad.py <asr_dir> <work_dir>"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_ads_v2.py")).read()
exec(src[:src.index("B = lambda")])  # helpers: words, chunks, caption_track, build, W, H, FPS, ROOT, D2, OUT, WORK...
SCRIPTS["anim"] = ("Salon treatments, every month? Meet Trivelle. Four rituals, one device. Warm, for a relaxing massage feel. "
                   "Glow, with red light. Lift, with gentle EMS pulses. Smooth, with a vacuum massage. "
                   "Ten minutes on the couch. Thirty days to try it.")
A = os.path.join(D2, "animated")
VOF = os.path.join(D2, "vo", "anim.mp3")
LOGO = os.path.join(ROOT, "brand", "logo-on-light.png")
ws = words("anim")
vo_d = dur(VOF)
def at(w): return next(x[0] for x in ws if _norm(x[2]).startswith(w))
cuts = [0.0, at("warm") - 0.1, at("glow") - 0.1, at("lift") - 0.1, at("smooth") - 0.1, at("ten") - 0.1, vo_d + 0.6]
scenes = ["a1-couch", "a2-arm-warm", "a3-stomach-glow", "a4-thigh-lift", "a5-jaw-smooth", "a6-relax"]
labels = [None, ("WARM", "Gentle heat"), ("GLOW", "Red light"), ("LIFT", "EMS micro-pulses"), ("SMOOTH", "Vacuum massage"), None]
GREEN, LIME = (29, 42, 38), (196, 206, 38)
anton = lambda s: ImageFont.truetype(os.path.join(FONTS, "Anton-Regular.ttf"), s)
def mont(s, w="SemiBold"):
    f = ImageFont.truetype(os.path.join(FONTS, "Montserrat.ttf"), s); f.set_variation_by_name(w); return f
logo = Image.open(LOGO).convert("RGBA"); logo = logo.crop(logo.getbbox())
logo = logo.resize((560, int(logo.height * 560 / logo.width)), Image.LANCZOS)
imgs = [Image.open(os.path.join(A, s + ".png")).convert("RGB").resize((W, int(W * 2752 / 1536)), Image.LANCZOS) for s in scenes]
ease = lambda t: 1 - (1 - min(max(t, 0), 1)) ** 3

total = cuts[-1]
body = os.path.join(WORK, "anim_body.mp4")
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                      "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", body], stdin=subprocess.PIPE)
for k in range(int(total * FPS)):
    t = k / FPS
    i = max(j for j in range(6) if cuts[j] <= t)
    lt, sd = t - cuts[i], cuts[i + 1] - cuts[i]
    def view(img, z):
        y0 = (img.height - H) * 0.5
        cx, cy = W / 2, y0 + H / 2
        # sub-pixel affine zoom about the frame centre: no integer crop steps, no jitter
        return img.transform((W, H), Image.AFFINE, (1 / z, 0, cx - W / (2 * z), 0, 1 / z, cy - H / (2 * z)),
                             resample=Image.BICUBIC).convert("RGBA")
    zf = lambda u: 1.0 + 0.06 * (u * u * (3 - 2 * u))  # eased push-in
    fr = view(imgs[i], zf(lt / sd))
    if lt < 0.25 and i:  # crossfade from where the previous scene ended
        fr = Image.blend(view(imgs[i - 1], zf(1.0)), fr, lt / 0.25)
    d = ImageDraw.Draw(fr)
    if i == 0 and t >= at("meet") - 0.05:  # logo reveal
        a = ease((t - at("meet")) / 0.5); lg = logo.copy(); lg.putalpha(lg.split()[3].point(lambda v: int(v * a)))
        fr.alpha_composite(lg, ((W - lg.width) // 2, int(330 - 30 * a)))
    if labels[i]:
        a = ease(lt / 0.45); big, small = labels[i]
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        f1 = anton(int(170 * (0.85 + 0.15 * a)))
        w1 = ld.textlength(big, font=f1); ld.text(((W - w1) / 2, 250), big, font=f1, fill=GREEN + (255,))
        f2 = mont(46); w2 = ld.textlength(small, font=f2)
        ld.rounded_rectangle(((W - w2) / 2 - 30, 470, (W + w2) / 2 + 30, 545), 38, fill=LIME + (255,))
        ld.text(((W - w2) / 2, 481), small, font=f2, fill=GREEN + (255,))
        lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
        fr.alpha_composite(lay)
    if i == 5:
        a = ease(lt / 0.5); lg = logo.copy(); lg.putalpha(lg.split()[3].point(lambda v: int(v * a)))
        fr.alpha_composite(lg, ((W - lg.width) // 2, 300))
    p.stdin.write(fr.convert("RGB").tobytes())
p.stdin.close(); p.wait()

END = os.path.join(WORK, "endcard.mp4"); end_card(END)
seq = [(body + "#ss=0", total, False), (END, 3.5, False)]
out = build("trivelle-E-animated", seq, VOF, chunks(ws), total + 3.5, 0)
print(out)
