"""Kollosche address super for 42 Salerno Street, Isle of Capri. The spec is measured from Kollosche's 4K example and
reuses kollosche-buckingham-way/scripts/assemble.py: Söhne Breit Kräftig, ALL CAPS, white, centred, cap height 47 px,
about 8% tracking, 78 px line pitch, no shadow. Also trims the Eddie Wardale team-logo PNGs tight."""
import sys
from pathlib import Path
import uharfbuzz as hb
from PIL import Image, ImageDraw, ImageFont
FONT = str(Path.home() / "Library/Fonts/SöhneBreit-Kräftig.otf"); OUT = Path(sys.argv[1])
hbf = hb.Font(hb.Face(hb.Blob.from_file_path(FONT)))
def address(lines, S=3840, H=2160):
    probe = ImageFont.truetype(FONT, 1000); hb_ = probe.getbbox("H"); size = round(47 / ((hb_[3] - hb_[1]) / 1000))
    font = ImageFont.truetype(FONT, size); ink = font.getbbox("H"); track = 0.08 * size
    im = Image.new("L", (S, H), 0); d = ImageDraw.Draw(im); top0 = H / 2 - (78 * (len(lines) - 1) + 47) / 2
    for i, text in enumerate(lines):
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(hbf, buf, {"kern": True})
        adv = [g.x_advance / hbf.face.upem * size for g in buf.glyph_positions]
        x = S / 2 - (sum(adv) + track * (len(text) - 1)) / 2
        for c, w in zip(text, adv): d.text((x, top0 + i * 78 - ink[1]), c, font=font, fill=255); x += w + track
    out = Image.new("RGBA", (S, H), (255, 255, 255, 0)); out.putalpha(im); return out
a = address(["42 SALERNO STREET", "ISLE OF CAPRI"])
a.save(OUT / "Address_42-Salerno-Street_4K.png")
a.resize((1920, 1080), Image.LANCZOS).save(OUT / "Address_42-Salerno-Street_1080p.png")
for p in sorted((OUT / "Eddie Wardale").glob("EddieWardale_*.png")):
    if p.stem.endswith("_tight"): continue
    im = Image.open(p).convert("RGBA"); bb = im.getchannel("A").getbbox(); pad = 40
    im.crop((bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad)).save(p.with_name(p.stem + "_tight.png"))
print("ok")
