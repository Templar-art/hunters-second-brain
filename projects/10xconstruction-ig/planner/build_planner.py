"""Visual posting planner for @10xconstruction: profile-grid preview + SCHEDULE table.
Edit POSTS (in posting order), then: python3 planner/build_planner.py"""
import os
from datetime import date, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = "/Users/10xhunter/Library/Fonts/Poppins-"
START, EVERY = date(2026, 10, 29), 3
POSTS = [  # offset a day from the real estate page; Ashley Cooper never twice in a row
    ("Broncos Leagues Club, Red Hill", "Carousel", "ACC", "carousels/broncos-leagues-club/01.jpg"),
    ("Grandview Hotel", "Reel", "SHAPE", "planner/grandview-reel.jpg"),
    ("Elysium Noosa, Hastings St", "Carousel", "SHAPE", "carousels/elysium-noosa/01.jpg"),
    ("Redcliffe RSL", "Carousel", "ACC", "carousels/redcliffe-rsl/01.jpg"),
    ("5 Friske Pl", "Carousel", "Maker Build", "carousels/5-friske-place/01.jpg"),
    ("Villa Noosa", "Carousel", "ACC", "carousels/villa-noosa/01.jpg"),
    ("350 Wardell St", "Carousel", "Livit", "carousels/350-wardell-street/01.jpg"),
    ("Arana Leagues Club", "Carousel", "ACC", "carousels/arana-leagues-club/01.jpg"),
    ("Nerang RSL", "Carousel", "SHAPE", "carousels/nerang-rsl/01.jpg"),
    ("Maroochy RSL", "Carousel", "ACC", "carousels/maroochy-rsl/01.jpg"),
    ("5 Rattan Ct", "Carousel", "Newscope", "carousels/5-rattan-court/01.jpg"),
    ("The Montague Hotel", "Carousel", "ACC", "carousels/the-montague-hotel/01.jpg"),
    ("25 Davenport Dr", "Carousel", "RAMU", "carousels/25-davenport-drive/01.jpg"),
    ("Rivermount College", "Carousel", "ACC", "carousels/rivermount-college/01.jpg"),
    ("Ipswich Mental Health Clinic", "Carousel", "Hill", "carousels/mental-health-clinic/01.jpg"),
    ("West End Residence", "Carousel", "Livit", "carousels/west-end-residence/01.jpg"),
    ("Burnside Tuckshop", "Carousel", "J&D", "carousels/burnside-tuckshop/01.jpg"),
]
BLUE, INK, PAPER = (0x61, 0xA8, 0xD8), (22, 26, 30), (0xF6, 0xF4, 0xF0)
f = lambda w, s: ImageFont.truetype(f"{F}{w}.ttf", s)
when = lambda i: START + timedelta(days=EVERY * i)

TW, TH, CAP, COLS = 360, 480, 78, 3
rows = (len(POSTS) + COLS - 1) // COLS
g = Image.new("RGB", (COLS * TW + (COLS - 1) * 6 + 80, 150 + rows * (TH + CAP) + 30), PAPER)
d = ImageDraw.Draw(g)
d.text((40, 50), "@10xconstruction  posting planner", font=f("SemiBold", 40), fill=INK)
d.text((40, 100), "Every 3 days, 7pm AEST. Newest first, as the grid will look after the last post.", font=f("Regular", 22), fill=(90, 90, 90))
for k, (i, (listing, fmt, client, src)) in enumerate(reversed(list(enumerate(POSTS)))):
    x, y = 40 + (k % COLS) * (TW + 6), 150 + (k // COLS) * (TH + CAP)
    g.paste(ImageOps.fit(Image.open(f"{HERE}/{src}").convert("RGB"), (TW, TH)), (x, y))
    d.rectangle((x + 12, y + 12, x + 12 + (70 if fmt == "Reel" else 130), y + 44), fill=BLUE)
    d.text((x + 20, y + 28), fmt.upper(), anchor="lm", font=f("SemiBold", 18), fill="white")
    d.text((x, y + TH + 10), f"{i + 1:02d}  {when(i):%a %-d %b}", font=f("SemiBold", 22), fill=BLUE)
    d.text((x, y + TH + 40), listing, font=f("Regular", 19), fill=INK)
g.save(f"{HERE}/planner/PLANNER.jpg", quality=90)

rows = ["| # | Date (7pm AEST) | Listing | Format | Client |", "|---|---|---|---|---|"]
rows += [f"| {i + 1} | {when(i):%a %-d %b} | {l} | {fm} | {c} |" for i, (l, fm, c, _) in enumerate(POSTS)]
print("\n".join(rows))
