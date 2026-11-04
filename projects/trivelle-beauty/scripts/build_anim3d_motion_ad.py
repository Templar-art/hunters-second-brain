"""Trivelle animated ad (9:16, ~24 s): 6 flat illustrations, slow push-ins, mode labels that pop in,
karaoke captions, soft music, logo end card. Reuses caption/mix helpers from build_ads_v2.py.
Usage: python3 build_anim_ad.py <asr_dir> <work_dir>"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_ads_v2.py")).read()
exec(src[:src.index("B = lambda")])  # helpers: words, chunks, caption_track, build, W, H, FPS, ROOT, D2, OUT, WORK...
SCRIPTS["anim3d"] = ("Another salon bill? Yeah... not anymore. Meet Trivelle. Four rituals, one device. Warm, for a relaxing massage feel. "
                   "Glow, with red light. Lift, with gentle EMS pulses. Smooth, with a vacuum massage. "
                   "Ten minutes on the couch. Thirty days to try it.")
A = os.path.join(D2, "animated3d")
VOF = os.path.join(D2, "vo", "anim3d.mp3")
LOGO = os.path.join(ROOT, "brand", "logo-on-dark.png")
ws = words("anim3d")
vo_d = dur(VOF)
def at(w): return next(x[0] for x in ws if _norm(x[2]).startswith(w))
cuts = [0.0, at("warm") - 0.1, at("glow") - 0.1, at("lift") - 0.1, at("smooth") - 0.1, at("ten") - 0.1, vo_d + 0.6]
scenes = ["b1-receipt", "b2-arm-warm", "b3-stomach-glow", "b4-thigh-lift", "b5-jaw-smooth", "b6-relax"]
labels = [None, ("WARM", "Gentle heat"), ("GLOW", "Red light"), ("LIFT", "EMS micro-pulses"), ("SMOOTH", "Vacuum massage"), None]
GREEN, LIME = (29, 42, 38), (196, 206, 38)
anton = lambda s: ImageFont.truetype(os.path.join(FONTS, "Anton-Regular.ttf"), s)
def mont(s, w="SemiBold"):
    f = ImageFont.truetype(os.path.join(FONTS, "Montserrat.ttf"), s); f.set_variation_by_name(w); return f
logo = Image.open(LOGO).convert("RGBA"); logo = logo.crop(logo.getbbox())
logo = logo.resize((560, int(logo.height * 560 / logo.width)), Image.LANCZOS)
ease = lambda t: 1 - (1 - min(max(t, 0), 1)) ** 3

total = cuts[-1]
body = os.path.join(WORK, "anim3d_motion_body.mp4")
# 1) conform each animated clip to its scene length (gentle slow-down only), concat
parts = []
for j in range(6):
    sd = cuts[j + 1] - cuts[j]; src_ = os.path.join(A, f"v{j+1}.mp4")
    sp = max(0.8, min(1.0, (dur(src_) - 0.1) / sd))
    pth = os.path.join(WORK, f"m3d_{j}.mp4"); parts.append(pth)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src_, "-vf",
        f"setpts=PTS/{sp:.4f},scale={W}:{H}:flags=lanczos,unsharp=5:5:0.5:3:3:0.0,fps={FPS},tpad=stop_mode=clone:stop_duration=2,format=yuv420p",
        "-t", f"{sd:.3f}", "-an", "-c:v", "libx264", "-crf", "14", pth], check=True)
lst = os.path.join(WORK, "m3d.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
raw = os.path.join(WORK, "m3d_raw.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", raw], check=True)
# 2) overlay pass (logo reveal, mode labels)
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", raw, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                      "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", body], stdin=subprocess.PIPE)
for k in range(int(total * FPS)):
    t = k / FPS
    i = max(j for j in range(6) if cuts[j] <= t)
    lt, sd = t - cuts[i], cuts[i + 1] - cuts[i]
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    fr = Image.frombytes("RGB", (W, H), buf).convert("RGBA")
    d = ImageDraw.Draw(fr)
    if i == 0 and t >= at("meet") - 0.05:  # logo reveal
        a = ease((t - at("meet")) / 0.5); lg = logo.copy(); lg.putalpha(lg.split()[3].point(lambda v: int(v * a)))
        fr.alpha_composite(lg, ((W - lg.width) // 2, int(330 - 30 * a)))
    if labels[i]:
        a = ease(lt / 0.45); big, small = labels[i]
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        f1 = anton(int(170 * (0.85 + 0.15 * a)))
        w1 = ld.textlength(big, font=f1); ld.text(((W - w1) / 2, 250), big, font=f1, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=GREEN + (255,))
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
out = build("trivelle-G-animated-3d-motion", seq, VOF, chunks(ws), total + 3.5, 0)
print(out)
