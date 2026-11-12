"""9:16 story frames for each @10xconstruction_ highlight. Photo full-bleed, small 10X top-left, project + builder bottom-left."""
import glob, os
from PIL import Image, ImageDraw, ImageFont
CON = os.path.expanduser("~/Documents/10x Drive Pulls/CON")
LOGOS = "/Users/10xhunter/Desktop/_Brand & Tools/10x-Visuals/Logos & Symbols"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stories")
FONT = next(p for p in glob.glob(os.path.expanduser("~/Library/Fonts/Poppins-SemiBold.ttf")) + glob.glob("/Library/Fonts/Poppins-SemiBold.ttf"))
FONT2 = FONT.replace("SemiBold", "Regular") if os.path.exists(FONT.replace("SemiBold", "Regular")) else FONT
SETS = {
 "commercial": [("Ashley Cooper Construction/Maroochy RSL", 29, "Maroochy RSL", "Ashley Cooper Construction"),
                ("SHAPE AUS/Club Robina", 0, "Club Robina", "SHAPE"),
                ("SHAPE AUS/Westside HQ", 10, "Westside HQ", "SHAPE")],
 "hospitality": [("Ashley Cooper Construction/Prince Hotel", 4, "Prince Hotel", "Ashley Cooper Construction"),
                 ("Ashley Cooper Construction/The Montague Hotel ", 18, "The Montague Hotel", "Ashley Cooper Construction"),
                 ("Ashley Cooper Construction/Redcliffe RSL", 1, "Redcliffe RSL", "Ashley Cooper Construction")],
 "education": [("Ashley Cooper Construction/Rivermount College", 3, "Rivermount College", "Ashley Cooper Construction"),
               ("J & D Contracting/Burnside Tuckshop April 2026", 1, "Burnside Tuckshop", "J & D Contracting")],
 "residential": [("Livit Constructions/West End Job Finished Files", 6, "West End Residence", "Livit Constructions"),
                 ("Maker Build/5 Friske Pl - Finished Project", 2, "5 Friske Place", "Maker Build"),
                 ("Newscope Construction/5 Rattan Ct | Final Shoot", 14, "5 Rattan Court", "Newscope Construction"),
                 ("RAMU BUILDER/25 Davenport Drive", 34, "25 Davenport Drive", "RAMU Builder")],
 "films": [("SHAPE AUS/Grandview Hotel", 24, "Grandview Hotel", "SHAPE"),
           ("SHAPE AUS/Nerang RSL", 27, "Nerang RSL", "SHAPE")],
}
W, H = 1080, 1920
icon = Image.open(f"{LOGOS}/10xVisuals_White with Blue X Symbol Icon.png").convert("RGBA"); icon = icon.crop(icon.getbbox())
icon = icon.resize((150, int(150*icon.height/icon.width)), Image.LANCZOS)
f1, f2 = ImageFont.truetype(FONT, 64), ImageFont.truetype(FONT2, 30)
for cat, items in SETS.items():
    os.makedirs(f"{OUT}/{cat}", exist_ok=True)
    for n, (folder, idx, title, builder) in enumerate(items, 1):
        files = sorted(f for f in glob.glob(f"{CON}/{folder}/**/*", recursive=True) if f.lower().endswith((".jpg", ".jpeg")))
        im = Image.open(files[idx]).convert("RGB"); w, h = im.size
        s = max(W/w, H/h); im = im.resize((int(w*s)+1, int(h*s)+1), Image.LANCZOS)
        x, y = (im.width-W)//2, (im.height-H)//2; im = im.crop((x, y, x+W, y+H)).convert("RGBA")
        g = Image.new("RGBA", (W, H)); gd = ImageDraw.Draw(g)
        for i in range(700): gd.line([(0, H-700+i), (W, H-700+i)], fill=(0, 0, 0, int(170*(i/700)**1.6)))
        for i in range(260): gd.line([(0, i), (W, i)], fill=(0, 0, 0, int(90*(1-i/260))))
        im = Image.alpha_composite(im, g); im.paste(icon, (72, 140), icon)
        d = ImageDraw.Draw(im)
        d.text((72, H-330), title, font=f1, fill="white")
        d.text((72, H-245), builder.upper(), font=f2, fill=(220, 220, 220))
        im.convert("RGB").save(f"{OUT}/{cat}/{n:02d}.jpg", quality=92)
print("done")
