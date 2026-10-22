"""Cut the 18 Maryland film from rendered moves: renders/moves/<shot>/####.png -> renders/film/<name>.mp4

  python3 tools/edit.py [--name maryland_film_v1] [--order aerial,gate,...] [--scope]

Each shot becomes a ProRes-quality intermediate, then they're joined with 0.5 s crossfades, given one film grade
(gentle S-curve, warm highlights / cool shadows, light vignette, fine grain) and a 2.39:1 letterbox, and closed on
a title card (Poppins Light). No AI anywhere: every frame is Blender.
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
argv = sys.argv[1:]


def arg(n, d):
    return argv[argv.index(n) + 1] if n in argv else d


ORDER = arg("--order", "aerial,gate,drive,lounge,kitchen,dining,outdoor,bench_water,pool_hero,master,balcony_dusk,closing").split(",")
NAME = arg("--name", "maryland_film_v1")
FPS = 25
XF = 0.5
OUT = os.path.join(HERE, "renders", "film"); os.makedirs(OUT, exist_ok=True)
GRADE = ("curves=master='0/0 0.08/0.05 0.5/0.5 0.9/0.94 1/1':red='0/0 0.5/0.5 1/1':blue='0/0.02 0.5/0.49 1/0.97',"
         "colorbalance=rs=-0.02:bs=0.03:rh=0.03:bh=-0.03,vignette=PI/5.5,noise=alls=5:allf=t")
BARS = "drawbox=x=0:y=0:w=iw:h=ih*0.1278:color=black:t=fill,drawbox=x=0:y=ih*0.8722:w=iw:h=ih*0.1278:color=black:t=fill"


def run(cmd):
    print(" ".join(cmd[:6]), "..."); subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def title_card(path, w=1920, h=1080):
    im = Image.new("RGB", (w, h), (8, 8, 9)); d = ImageDraw.Draw(im)
    fonts = os.path.expanduser("~/Library/Fonts")
    big = ImageFont.truetype(os.path.join(fonts, "Poppins-Light.ttf"), 78)
    small = ImageFont.truetype(os.path.join(fonts, "Poppins-Light.ttf"), 26)
    for text, f, y, fill in (("18 MARYLAND AVENUE", big, h / 2 - 60, (240, 238, 234)), ("CARRARA  ·  GOLD COAST", small, h / 2 + 40, (160, 160, 158))):
        tw = d.textlength(text, font=f); d.text(((w - tw) / 2, y), text, font=f, fill=fill)
    im.save(path)


def main():
    clips = []
    for s in ORDER:
        d = os.path.join(HERE, "renders", "moves", s)
        if not os.path.isdir(d) or not os.listdir(d):
            print("skip (not rendered)", s); continue
        o = os.path.join(OUT, f"_{s}.mov")
        run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", os.path.join(d, "%04d.png"), "-c:v", "prores_ks", "-profile:v", "3",
             "-pix_fmt", "yuv422p10le", o])
        clips.append(o)
    card = os.path.join(OUT, "_title.png"); title_card(card)
    cm = os.path.join(OUT, "_title.mov")
    run(["ffmpeg", "-y", "-loop", "1", "-t", "4", "-framerate", str(FPS), "-i", card, "-vf", "fade=in:st=0:d=1",
         "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", cm])
    clips.append(cm)
    durs = [float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", c]))
            for c in clips]
    inputs = sum((["-i", c] for c in clips), [])
    fc = []; last = "[0:v]"; t = durs[0]
    for i in range(1, len(clips)):
        off = t - XF
        fc.append(f"{last}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{i}]"); last = f"[x{i}]"; t = off + durs[i]
    fc.append(f"{last}{GRADE},{BARS},format=yuv420p[out]")
    final = os.path.join(OUT, NAME + ".mp4")
    run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[out]", "-c:v", "libx264", "-crf", "14",
         "-preset", "slow", "-r", str(FPS), final])
    print("FILM", final, f"{t:.1f}s")


if __name__ == "__main__":
    main()
