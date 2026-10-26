"""Visual posting planner for @10xrealestate_: profile-grid preview + SCHEDULE table.
Edit POSTS (in posting order), then: python3 planner/build_planner.py"""
import os
from datetime import date, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = "/Users/10xhunter/Library/Fonts/Poppins-"
START, EVERY = date(2026, 10, 28), 3
POSTS = [  # clients alternate: Salt PM never back to back. Reel thumbs are stand-ins; real covers set in the app
    ("13 Mayra Ct, Mermaid Waters", "Reel", "Kollosche", "covers/mayra-ct-cover.jpg"),
    ("59 Cylinders Dr, Kingscliff", "Carousel", "Salt PM", "carousels/59-cylinders-dr/01.jpg"),
    ("47 Somerset Dr, Mudgeeraba", "Carousel", "Whitefox", "carousels/47-somerset-dr/01.jpg"),
    ("Solis, 673 Casuarina Way", "Reel", "Salt PM", "planner/solis-reel.jpg"),
    ("10 Australis Ct, Mermaid Waters", "Reel", "Kollosche", "planner/australis-reel.jpg"),
    ("Elanora Ave townhouses, Pottsville", "Carousel", "Salt PM", "carousels/elanora-ave-townhouses/01.jpg"),
    ("47 Somerset Dr, Mudgeeraba", "Reel", "Whitefox", "planner/somerset-reel.jpg"),
    ("59 Cylinders Dr, Kingscliff", "Reel", "Salt PM", "planner/cylinders-reel.jpg"),
    ("10 Australis Ct, Mermaid Waters", "Carousel", "Kollosche", "carousels/10-australis-ct/01.jpg"),
    ("Solis, 673 Casuarina Way", "Carousel", "Salt PM", "carousels/solis-673-casuarina-way/01.jpg"),
    ("Elanora Ave townhouses, Pottsville", "Reel", "Salt PM", "planner/elanora-reel.jpg"),
]
BLUE, INK, PAPER = (0x61, 0xA8, 0xD8), (22, 26, 30), (0xF6, 0xF4, 0xF0)
f = lambda w, s: ImageFont.truetype(f"{F}{w}.ttf", s)
when = lambda i: START + timedelta(days=EVERY * i)

TW, TH, CAP, COLS = 360, 480, 78, 3
rows = (len(POSTS) + COLS - 1) // COLS
g = Image.new("RGB", (COLS * TW + (COLS - 1) * 6 + 80, 150 + rows * (TH + CAP) + 30), PAPER)
d = ImageDraw.Draw(g)
d.text((40, 50), "@10xrealestate_  posting planner", font=f("SemiBold", 40), fill=INK)
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
