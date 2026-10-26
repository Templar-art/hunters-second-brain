"""Visual posting planner for @10xrealestate_: profile-grid preview + SCHEDULE table.
Edit POSTS (in posting order), then: python3 planner/build_planner.py"""
import os
from datetime import date, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = "/Users/10xhunter/Library/Fonts/Poppins-"
START, EVERY = date(2026, 10, 28), 3
POSTS = [  # Salt PM alternates with another client every time. Cylinders main went up 26 Oct, so its reel goes last
    ("13 Mayra Ct, Mermaid Waters", "Reel", "Kollosche", "covers/mayra-ct-cover.jpg"),
    ("Solis, 673 Casuarina Way", "Reel", "Salt PM", "planner/solis-reel.jpg"),
    ("47 Somerset Dr, Mudgeeraba", "Carousel", "Whitefox", "carousels/47-somerset-dr/01.jpg"),
    ("Elanora Ave townhouses, Pottsville", "Carousel", "Salt PM", "carousels/elanora-ave-townhouses/01.jpg"),
    ("10 Australis Ct, Mermaid Waters", "Reel", "Kollosche", "planner/australis-reel.jpg"),
    ("59 Cylinders Dr, Kingscliff", "Carousel", "Salt PM", "carousels/59-cylinders-dr/01.jpg"),
    ("47 Somerset Dr, Mudgeeraba", "Reel", "Whitefox", "planner/somerset-reel.jpg"),
    ("Solis, 673 Casuarina Way", "Carousel", "Salt PM", "carousels/solis-673-casuarina-way/01.jpg"),
    ("10 Australis Ct, Mermaid Waters", "Carousel", "Kollosche", "carousels/10-australis-ct/01.jpg"),
    ("Elanora Ave townhouses, Pottsville", "Reel", "Salt PM", "planner/elanora-reel.jpg"),
    ("59 Cylinders Dr, Kingscliff", "Reel", "Salt PM", "planner/cylinders-reel.jpg"),
    # second wave from the Drive pull (2026-10-26), no client twice in a row
    ("6/446 Marine Pde", "Carousel", "Zed", "carousels/6-446-marine-pde/01.jpg"),
    ("37 Southaven Dr", "Carousel", "Belle", "carousels/37-southaven-dr/01.jpg"),
    ("701/1245 Gold Coast Hwy", "Carousel", "Zed", "carousels/701-1245-gold-coast-hwy/01.jpg"),
    ("43 North View St", "Carousel", "Bespoke", "carousels/43-north-view-st/01.jpg"),
    ("57 Girtin Cct", "Carousel", "YPA", "carousels/57-girtin-cct/01.jpg"),
    ("24A Muscovey Ave", "Carousel", "Zed", "carousels/24a-muscovey-ave/01.jpg"),
    ("71/73 Lydford Cl", "Carousel", "Coastline", "carousels/71-73-lydford-cl/01.jpg"),
    ("Uniq Residences", "Carousel", "Bespoke", "carousels/uniq-waterford-ct/01.jpg"),
    ("3422 Surfers Paradise Blvd", "Carousel", "Zed", "carousels/3422-surfers-paradise-blvd/01.jpg"),
    ("88 Third Ave", "Carousel", "Jessica Wallace", "carousels/88-third-ave/01.jpg"),
    ("4 Mornington Ct", "Carousel", "YPA", "carousels/4-mornington-ct/01.jpg"),
    ("801/1245 Gold Coast Hwy", "Carousel", "Zed", "carousels/801-1245-gold-coast-hwy/01.jpg"),
    ("32 Southern Skies Ave", "Carousel", "Remax", "carousels/32-southern-skies/01.jpg"),
    ("3009 The Boulevard", "Carousel", "Bespoke", "carousels/3009-the-boulevard/01.jpg"),
    ("15 Muston Ct", "Carousel", "Ray White TMG", "carousels/15-muston-ct/01.jpg"),
    ("25 Dungogie Dr", "Carousel", "Zed", "carousels/25-dungogie-dr/01.jpg"),
    ("23 Gillian Dr", "Carousel", "Belle", "carousels/23-gillian-dr/01.jpg"),
    ("41 Sears Rd", "Carousel", "YPA", "carousels/41-sears-rd/01.jpg"),
    ("38 John Lund Dr", "Carousel", "Zed", "carousels/38-john-lund-dr/01.jpg"),
    ("3049/3029 The Boulevard", "Carousel", "Bespoke", "carousels/3029-the-boulevard/01.jpg"),
    ("13 Pyrite St", "Carousel", "Place", "carousels/13-pyrite-st/01.jpg"),
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
