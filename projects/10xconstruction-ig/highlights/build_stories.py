"""9:16 story frames for each @10xconstruction_ highlight. Photo full-bleed, small 10X top-left, project + builder bottom-left."""
import glob, os
from PIL import Image, ImageDraw, ImageFont
CON = os.path.expanduser("~/Documents/10x Drive Pulls/CON")
LOGOS = "/Users/10xhunter/Desktop/_Brand & Tools/10x-Visuals/Logos & Symbols"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stories")
FONT = next(p for p in glob.glob(os.path.expanduser("~/Library/Fonts/Poppins-SemiBold.ttf")) + glob.glob("/Library/Fonts/Poppins-SemiBold.ttf"))
FONT2 = FONT.replace("SemiBold", "Regular") if os.path.exists(FONT.replace("SemiBold", "Regular")) else FONT
SETS = {  # premium builders only: (folder, sorted-jpg index, title, suburb, builder)
 "commercial": [("Ashley Cooper Construction/Maroochy RSL", 29, "Maroochy RSL", "Maroochydore", "Ashley Cooper"),
                ("SHAPE AUS/Club Robina", 0, "Club Robina", "Robina", "SHAPE"),
                ("SHAPE AUS/Nerang RSL", 27, "Nerang RSL", "Nerang", "SHAPE"),
                ("SHAPE AUS/Westside HQ", 10, "Westside HQ", "Corinda", "SHAPE"),
                ("Ashley Cooper Construction/Rivermount College", 3, "Rivermount College", "Yatala", "Ashley Cooper")],
 "hospitality": [("Ashley Cooper Construction/Prince Hotel", 4, "Prince Hotel", "", "Ashley Cooper"),
                 ("Ashley Cooper Construction/The Montague Hotel ", 18, "The Montague Hotel", "West End", "Ashley Cooper"),
                 ("Ashley Cooper Construction/Redcliffe RSL", 1, "Redcliffe RSL", "Redcliffe", "Ashley Cooper"),
                 ("SHAPE AUS/Grandview Hotel", 24, "Grandview Hotel", "Cleveland", "SHAPE")],
 "residential": [("Livit Constructions/West End Job Finished Files", 6, "West End Residence", "West End", "Livit Constructions"),
                 ("Maker Build/5 Friske Pl - Finished Project", 2, "5 Friske Place", "Palm Beach", "Maker Build")],
}
W, H = 1080, 1920
icon = Image.open(f"{LOGOS}/10xVisuals_White with Blue X Symbol Icon.png").convert("RGBA"); icon = icon.crop(icon.getbbox())
icon = icon.resize((150, int(150*icon.height/icon.width)), Image.LANCZOS)
f1, f2 = ImageFont.truetype(FONT, 54), ImageFont.truetype(FONT2, 24)
for cat, items in SETS.items():
    os.makedirs(f"{OUT}/{cat}", exist_ok=True)
    for n, (folder, idx, title, sub, builder) in enumerate(items, 1):
        files = sorted(f for f in glob.glob(f"{CON}/{folder}/**/*", recursive=True) if f.lower().endswith((".jpg", ".jpeg")))
        im = Image.open(files[idx]).convert("RGB"); w, h = im.size
        s = max(W/w, H/h); im = im.resize((int(w*s)+1, int(h*s)+1), Image.LANCZOS)
        x, y = (im.width-W)//2, (im.height-H)//2; im = im.crop((x, y, x+W, y+H)).convert("RGBA")
        g = Image.new("RGBA", (W, H)); gd = ImageDraw.Draw(g)
        for i in range(700): gd.line([(0, H-700+i), (W, H-700+i)], fill=(0, 0, 0, int(150*(i/700)**2)))
        for i in range(260): gd.line([(0, i), (W, i)], fill=(0, 0, 0, int(90*(1-i/260))))
        im = Image.alpha_composite(im, g); im.paste(icon, (72, 140), icon)
        d = ImageDraw.Draw(im)
        d.text((72, H-300), title, font=f1, fill="white")
        line = (f"{sub}   ·   " if sub else "") + f"BY {builder}"; x = 74
        for ch in line.upper(): d.text((x, H-222), ch, font=f2, fill=(225, 225, 225)); x += d.textlength(ch, font=f2) + 4
        im.convert("RGB").save(f"{OUT}/{cat}/{n:02d}.jpg", quality=92)
print("done")
