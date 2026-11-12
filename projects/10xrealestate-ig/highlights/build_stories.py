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
# Premium clients only (Kollosche, Coastline Prestige, White Fox). Never Zed, never construction jobs.
D = '/Users/10xhunter/Desktop/Websites photos and videos/Photos/'; K = '/Users/10xhunter/Documents/10x Drive Pulls/Kollosche/'; C = '/Users/10xhunter/Documents/10x Drive Pulls/REA/Coastline Prestige/71／73 Lydford Close/'
SETS = {
 "aerials":   [(D+"47  Somerset Drive _ Print-14.jpg", "47 Somerset Drive", "Mudgeeraba", "White Fox"),
               (C+"71-73 Lydford Close - Web-27.jpg", "71/73 Lydford Close", "Bonogin", "Coastline Prestige")],
 "exteriors": [(K+"5 Esther Place Print/Print-17.jpg", "5 Esther Place", "Surfers Paradise", "Kollosche"),
               (C+"71-73 Lydford Close - Web-19.jpg", "71/73 Lydford Close", "Bonogin", "Coastline Prestige"),
               (K+"4-6 Buckingham Way Print/P-06.jpg", "4-6 Buckingham Way", "Elanora", "Kollosche"),
               (D+"47  Somerset Drive _ Print-18.jpg", "47 Somerset Drive", "Mudgeeraba", "White Fox")],
 "interiors": [(K+"5 Esther Place Print/Print-02.jpg", "5 Esther Place", "Surfers Paradise", "Kollosche"),
               (C+"71-73 Lydford Close - Web-8.jpg", "71/73 Lydford Close", "Bonogin", "Coastline Prestige"),
               (K+"5 Esther Place Print/Print-14.jpg", "5 Esther Place", "Surfers Paradise", "Kollosche"),
               (K+"5 Esther Place Print/Print-15.jpg", "5 Esther Place", "Surfers Paradise", "Kollosche")],
}
W, H = 1080, 1920
icon = Image.open(f"{LOGOS}/10xVisuals_White with Blue X Symbol Icon.png").convert("RGBA"); icon = icon.crop(icon.getbbox())
small = icon.resize((150, int(150*icon.height/icon.width)), Image.LANCZOS)
f1, f2 = ImageFont.truetype(FONT, 54), ImageFont.truetype(FONT2, 24)
n = 0; os.makedirs(f"{OUT}/_upload", exist_ok=True)
for cat, items in SETS.items():
    os.makedirs(f"{OUT}/{cat}", exist_ok=True)
    for k, (src, title, sub, agency) in enumerate(items, 1):
        im = Image.open(src); im.draft("RGB", (3000, 3000)); im = im.convert("RGB"); w, h = im.size
        s = max(W/w, H/h); im = im.resize((int(w*s)+1, int(h*s)+1), Image.LANCZOS)
        x, y = (im.width-W)//2, (im.height-H)//2; im = im.crop((x, y, x+W, y+H)).convert("RGBA")
        g = Image.new("RGBA", (W, H)); gd = ImageDraw.Draw(g)
        for i in range(700): gd.line([(0, H-700+i), (W, H-700+i)], fill=(0, 0, 0, int(150*(i/700)**2)))
        for i in range(260): gd.line([(0, i), (W, i)], fill=(0, 0, 0, int(90*(1-i/260))))
        im = Image.alpha_composite(im, g); im.paste(small, (72, 140), small)
        d = ImageDraw.Draw(im); d.text((72, H-300), title, font=f1, fill="white")
        line = f"{sub}   ·   FOR {agency}".upper(); x = 74
        for ch in line: d.text((x, H-222), ch, font=f2, fill=(225, 225, 225)); x += d.textlength(ch, font=f2) + 4
        im = im.convert("RGB"); im.save(f"{OUT}/{cat}/{k:02d}.jpg", quality=92)
        n += 1; im.save(f"{OUT}/_upload/{n:02d}-{cat}-{k:02d}.jpg", quality=92)
    if cat in ("aerials", "exteriors", "interiors"):  # new covers, same treatment as the existing aerials/twilight covers
        c = Image.open(items[0][0]); c.draft("RGB", (2000, 2000)); c = c.convert("RGB"); w, h = c.size; m = min(w, h)
        c = c.crop(((w-m)//2, (h-m)//2, (w+m)//2, (h+m)//2)).resize((1080, 1080), Image.LANCZOS)
        c = ImageEnhance.Brightness(ImageEnhance.Color(c).enhance(0.55)).enhance(0.55)
        i2 = icon.resize((324, int(324*icon.height/icon.width)), Image.LANCZOS); c.paste(i2, ((1080-i2.width)//2, (1080-i2.height)//2), i2)
        c.save(f"{HERE}/{cat}.png")
fs = sorted(glob.glob(f"{OUT}/_upload/*.jpg")); t = [Image.open(f).resize((216, 384)) for f in fs]
sh = Image.new("RGB", (216*5, 384*2)); [sh.paste(im, ((i % 5)*216, (i//5)*384)) for i, im in enumerate(t)]; sh.save(f"{OUT}/_contact.jpg")
