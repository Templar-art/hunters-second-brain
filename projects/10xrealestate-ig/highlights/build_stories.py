"""9:16 story frames for @10xrealestate_ highlights (same layout as 10xconstruction_). Never Zed."""
import glob, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
Image.MAX_IMAGE_PIXELS = None
REA = os.path.expanduser("~/Documents/10x Drive Pulls/REA")
LOGOS = "/Users/10xhunter/Desktop/_Brand & Tools/10x-Visuals/Logos & Symbols"
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = f"{HERE}/stories"
FONT = os.path.expanduser("~/Library/Fonts/Poppins-SemiBold.ttf")
if not os.path.exists(FONT): FONT = "/Library/Fonts/Poppins-SemiBold.ttf"
FONT2 = FONT.replace("SemiBold", "Regular")
ALL = sorted(f for f in glob.glob(f"{REA}/**/*", recursive=True) if f.lower().endswith((".jpg", ".jpeg")) and "Zed" not in f)
SETS = {  # index into ALL (same order as the picking contact sheet), title, suburb
 "aerials":   [(129, "3049 The Boulevard", "Carrara"), (166, "43 North View Street", "Hope Island"), (79, "3009 The Boulevard", "Carrara"), (432, "57 Girtin Circuit", "Pimpama")],
 "twilight":  [(84, "3009 The Boulevard", "Carrara"), (398, "41 Sears Road", "Yatala"), (83, "3009 The Boulevard", "Carrara")],
 "exteriors": [(237, "88 Third Avenue", "Palm Beach"), (330, "32 Southern Skies Avenue", "Reedy Creek"), (85, "3009 The Boulevard", "Carrara"), (26, "37 Southaven Drive", "Helensvale")],
 "interiors": [(150, "43 North View Street", "Hope Island"), (342, "32 Southern Skies Avenue", "Reedy Creek"), (180, "Uniq Residences", "Bundall"), (20, "23 Gillian Drive", "Coomera")],
}
W, H = 1080, 1920
icon = Image.open(f"{LOGOS}/10xVisuals_White with Blue X Symbol Icon.png").convert("RGBA"); icon = icon.crop(icon.getbbox())
small = icon.resize((150, int(150*icon.height/icon.width)), Image.LANCZOS)
f1, f2 = ImageFont.truetype(FONT, 64), ImageFont.truetype(FONT2, 30)
n = 0; os.makedirs(f"{OUT}/_upload", exist_ok=True)
for cat, items in SETS.items():
    os.makedirs(f"{OUT}/{cat}", exist_ok=True)
    for k, (idx, title, sub) in enumerate(items, 1):
        print(cat, ALL[idx].replace(REA, ""))
        im = Image.open(ALL[idx]); im.draft("RGB", (3000, 3000)); im = im.convert("RGB"); w, h = im.size
        s = max(W/w, H/h); im = im.resize((int(w*s)+1, int(h*s)+1), Image.LANCZOS)
        x, y = (im.width-W)//2, (im.height-H)//2; im = im.crop((x, y, x+W, y+H)).convert("RGBA")
        g = Image.new("RGBA", (W, H)); gd = ImageDraw.Draw(g)
        for i in range(700): gd.line([(0, H-700+i), (W, H-700+i)], fill=(0, 0, 0, int(170*(i/700)**1.6)))
        for i in range(260): gd.line([(0, i), (W, i)], fill=(0, 0, 0, int(90*(1-i/260))))
        im = Image.alpha_composite(im, g); im.paste(small, (72, 140), small)
        d = ImageDraw.Draw(im); d.text((72, H-330), title, font=f1, fill="white")
        if sub: d.text((72, H-245), sub.upper(), font=f2, fill=(220, 220, 220))
        im = im.convert("RGB"); im.save(f"{OUT}/{cat}/{k:02d}.jpg", quality=92)
        n += 1; im.save(f"{OUT}/_upload/{n:02d}-{cat}-{k:02d}.jpg", quality=92)
    if cat in ("exteriors", "interiors"):  # new covers, same treatment as the existing aerials/twilight covers
        c = Image.open(ALL[items[0][0]]); c.draft("RGB", (2000, 2000)); c = c.convert("RGB"); w, h = c.size; m = min(w, h)
        c = c.crop(((w-m)//2, (h-m)//2, (w+m)//2, (h+m)//2)).resize((1080, 1080), Image.LANCZOS)
        c = ImageEnhance.Brightness(ImageEnhance.Color(c).enhance(0.55)).enhance(0.55)
        i2 = icon.resize((324, int(324*icon.height/icon.width)), Image.LANCZOS); c.paste(i2, ((1080-i2.width)//2, (1080-i2.height)//2), i2)
        c.save(f"{HERE}/highlights/{cat}.png") if False else c.save(f"{HERE}/{cat}.png")
fs = sorted(glob.glob(f"{OUT}/_upload/*.jpg")); t = [Image.open(f).resize((216, 384)) for f in fs]
sh = Image.new("RGB", (216*8, 384*2)); [sh.paste(im, ((i % 8)*216, (i//8)*384)) for i, im in enumerate(t)]; sh.save(f"{OUT}/_contact.jpg")
