"""10xconstruction_ highlight covers + avatar, matched to @10xrealestate_ highlights."""
import glob, os
from PIL import Image, ImageEnhance, ImageDraw
CON = os.path.expanduser("~/Documents/10x Drive Pulls/CON")
LOGOS = "/Users/10xhunter/Desktop/_Brand & Tools/10x-Visuals/Logos & Symbols"
OUT = os.path.dirname(os.path.abspath(__file__))
PICKS = {  # name: (folder, sorted-jpg index) — same hero frames as the carousel decks
    "commercial":  ("Ashley Cooper Construction/Maroochy RSL", 29),
    "hospitality": ("Ashley Cooper Construction/Prince Hotel", 4),
    "education":   ("Ashley Cooper Construction/Rivermount College", 3),
    "residential": ("Livit Constructions/West End Job Finished Files", 6),
    "films":       ("SHAPE AUS/Grandview Hotel", 24),
}
S = 1080
icon = Image.open(f"{LOGOS}/10xVisuals_White with Blue X Symbol Icon.png").convert("RGBA")
icon = icon.crop(icon.getbbox())
def square(p):
    im = Image.open(p).convert("RGB"); w, h = im.size; m = min(w, h)
    return im.crop(((w-m)//2, (h-m)//2, (w+m)//2, (h+m)//2)).resize((S, S), Image.LANCZOS)
def with_icon(bg, frac):
    i = icon.resize((int(S*frac), int(S*frac*icon.height/icon.width)), Image.LANCZOS)
    bg.paste(i, ((S-i.width)//2, (S-i.height)//2), i); return bg
thumbs = []
for name, (folder, idx) in PICKS.items():
    files = sorted(f for f in glob.glob(f"{CON}/{folder}/**/*", recursive=True) if f.lower().endswith((".jpg", ".jpeg")))
    im = square(files[idx])
    im = ImageEnhance.Color(im).enhance(0.55)
    im = ImageEnhance.Brightness(im).enhance(0.55)
    im = with_icon(im, 0.30); im.save(f"{OUT}/{name}.png"); thumbs.append(im)
# avatar: white disc + colour 10X, same as @10xrealestate_
px = icon.copy(); data = px.load()
for y in range(px.height):
    for x in range(px.width):
        r, g, b, a = data[x, y]
        if a and min(r, g, b) > 150 and abs(r-b) < 30: data[x, y] = (10, 10, 10, a)  # white "10" -> black, keep blue X
av = Image.new("RGB", (S, S), "white")
bb = px.resize((int(S*0.62), int(S*0.62*px.height/px.width)), Image.LANCZOS)
av.paste(bb, ((S-bb.width)//2, (S-bb.height)//2), bb); av.save(f"{OUT}/avatar.png")
# preview strip
pv = Image.new("RGB", (1600, 330), (12, 15, 20)); d = ImageDraw.Draw(pv)
def disc(im, x, r):
    t = im.resize((2*r, 2*r)); m = Image.new("L", (2*r, 2*r)); ImageDraw.Draw(m).ellipse((0, 0, 2*r, 2*r), 255)
    pv.paste(t, (x, 165-r), m)
disc(av, 20, 130)
for k, t in enumerate(thumbs): disc(t, 320+k*250, 100)
pv.save(f"{OUT}/_preview.png"); print("ok", [os.path.basename(files[0]) for _ in [0]])
