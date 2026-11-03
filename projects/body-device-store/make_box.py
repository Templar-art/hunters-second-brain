"""VELLAN Full Kit: straight tuck end carton. Units mm. All type outlined.
Change W/D/H to the supplier's confirmed internal size and re-run."""
import cairosvg
from brand import *

W, D, H = 230, 80, 170          # front width, depth, height
B = 3; TUCK = 22; GLUE = 15     # bleed, tuck flap, glue flap
x0 = 20; y0 = 30 + D + TUCK
xs = [x0]
for w in (GLUE, W, D, W, D): xs.append(xs[-1] + w)
TW = xs[-1] + 20; TH = y0 + H + D + TUCK + 30
yb = y0 + H
cut, fold, art = [], [], []

# ---- dieline geometry ----
gx = xs[0]
cut.append(f'M{gx+GLUE},{y0} L{gx},{y0+6} L{gx},{yb-6} L{gx+GLUE},{yb}')
for i in range(1, 5): fold.append(f'M{xs[i]},{y0} L{xs[i]},{yb}')
def lid(px, py, up):
    s = -1 if up else 1
    a, b = py + s*D, py + s*(D+TUCK)
    cut.append(f'M{px},{py} L{px},{a} L{px+2},{a} Q{px+2},{b} {px+14},{b} L{px+W-14},{b} Q{px+W-2},{b} {px+W-2},{a} L{px+W},{a} L{px+W},{py}')
    fold.append(f'M{px},{py} L{px+W},{py}'); fold.append(f'M{px+2},{a} L{px+W-2},{a}')
def dust(sx, py, up):
    s = -1 if up else 1; d = D*0.75
    cut.append(f'M{sx},{py} L{sx+2},{py+s*d} L{sx+D-14},{py+s*d} L{sx+D},{py+s*6} L{sx+D},{py}')
    fold.append(f'M{sx},{py} L{sx+D},{py}')
lid(xs[1], y0, True); lid(xs[3], yb, False)
for i in (2, 4): dust(xs[i], y0, True); dust(xs[i], yb, False)
cut += [f'M{xs[3]},{y0} L{xs[4]},{y0}', f'M{xs[1]},{yb} L{xs[2]},{yb}', f'M{xs[5]},{y0} L{xs[5]},{yb}']

# ---- artwork ----
def rect(x, y, w, h, c): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>'
art.append(rect(xs[0]-B, y0-B, xs[5]-xs[0]+2*B, H+2*B, BONE))
art.append(rect(xs[1]-B, y0-D-TUCK-B, W+2*B, D+TUCK+B, ESPRESSO))      # lid + tuck
art.append(rect(xs[3]-B, yb, W+2*B, D+TUCK+B, ESPRESSO))                  # base + tuck
for i in (2, 4):
    art.append(rect(xs[i], y0, D, H, ESPRESSO))
    art.append(rect(xs[i], y0-D*0.75-B, D, D*0.75+B, SAND))
    art.append(rect(xs[i], yb, D, D*0.75+B, SAND))

FACES = {}
def face(name, x, y, w, h, body):
    FACES[name] = (x, y, w, h); art.append(body)

# Front
c = xs[1] + W/2
f = []
f.append(text('THE BODY CONTOUR SYSTEM', c, y0+18, SANS_MED, 4.2, STONE, 'middle', track=1.7))
f.append(mark(c, y0+58, 30, CLAY))
f.append(wordmark(c, y0+101, 30, ESPRESSO))
f.append(f'<line x1="{c-14}" y1="{y0+116}" x2="{c+14}" y2="{y0+116}" stroke="{CLAY}" stroke-width=".35"/>')
f.append(text('Four-in-one at-home body device', c, y0+129, SERIF_LIGHT, 9, ESPRESSO, 'middle'))
f.append(text('WARMTH  ·  SUCTION  ·  RED LIGHT  ·  MICROCURRENT', c, y0+140, SANS, 3.8, STONE, 'middle', track=1.0))
f.append(text('FULL KIT', c, yb-12, SANS_MED, 4.2, ESPRESSO, 'middle', track=2.4))
face('front', xs[1], y0, W, H, ''.join(f))

# Lid (reads correctly when box closed and viewed from top)
lx = xs[1] + W/2; ly = y0 - D/2
art.append(lockup(lx, ly+6, 17, BONE, SAND))
art.append(text('VELLAN.COM.AU', lx, y0-D-TUCK/2+1.5, SANS, 3.4, SAND, 'middle', track=1.6))
# Base
art.append(text('VELLAN  ·  BODY CONTOUR SYSTEM', xs[3]+W/2, yb+D/2+1.5, SANS, 3.8, SAND, 'middle', track=1.8))

# Sides: vertical wordmark + tagline
for i in (2, 4):
    sx = xs[i] + D/2; sy = y0 + H/2
    art.append(f'<g transform="rotate(-90 {sx} {sy})">{wordmark(sx, sy+5, 15, BONE)}</g>')
    art.append(mark(sx, y0+20, 11, SAND))
    art.append(text('FULL KIT', sx, yb-12, SANS_MED, 3.6, SAND, 'middle', track=2))

# Back
bx = xs[3] + 18; bw = W - 36
b = [text('Fifteen minutes a day, at home.', xs[3]+W/2, y0+24, SERIF_LIGHT, 11, ESPRESSO, 'middle')]
yy = y0 + 42
for head, body in [
    ('IN THE BOX', 'VELLAN device  ·  3 treatment heads (belly, arm, leg)  ·  Conductive gel 100 ml  ·  USB-C cable  ·  Travel pouch  ·  User guide'),
    ('HOW TO USE', 'Charge fully. Apply a thin layer of gel. Choose your suction and microcurrent levels. Glide slowly over each area for 15 minutes, once a day.'),
    ('CAUTION', 'Do not use during pregnancy, with a pacemaker or other implanted electronic device, or on broken or irritated skin. Read the user guide before first use.'),
]:
    b.append(text(head, bx, yy, SANS_MED, 3.6, CLAY, track=1.3))
    s, yy = lines([body], bx, yy+6.5, SANS, 3.9, ESPRESSO, bw, lead=1.5); b.append(s); yy += 5
b.append(f'<line x1="{bx}" y1="{yb-38}" x2="{bx+bw}" y2="{yb-38}" stroke="{SAND}" stroke-width=".35"/>')
for k, t in enumerate(['[Company Pty Ltd]  ·  ABN [00 000 000 000]', '[Address, City STATE 0000]  ·  vellan.com.au',
                       'Model [VL-01]  ·  5V DC 1A  ·  Li-ion [0000] mAh  ·  Made in [country]']):
    b.append(text(t, bx, yb-29+k*6, SANS, 3.3, STONE))
b.append(f'<rect x="{xs[3]+W-56}" y="{yb-34}" width="38" height="24" fill="#fff"/>')
b.append(text('EAN-13 BARCODE', xs[3]+W-37, yb-21, SANS, 2.6, STONE, 'middle', track=.5))
face('back', xs[3], y0, W, H, ''.join(b))

def doc(with_art, with_lines, label):
    o = [rect(0, 0, TW, TH, '#fff')]
    if with_art: o += art
    if with_lines:
        o.append('<g fill="none" stroke="#E4002B" stroke-width=".3">' + ''.join(f'<path d="{p}"/>' for p in cut) + '</g>')
        o.append('<g fill="none" stroke="#0055FF" stroke-width=".3" stroke-dasharray="2.5 1.5">' + ''.join(f'<path d="{p}"/>' for p in fold) + '</g>')
    if label:
        o.append(text(f'VELLAN FULL KIT  ·  STRAIGHT TUCK END CARTON  ·  {W} x {D} x {H} MM (W x D x H)  ·  3 MM BLEED  ·  RED = CUT  ·  BLUE DASHED = FOLD  ·  ALL TYPE OUTLINED', 20, 14, SANS_MED, 3.6, '#000', track=.6))
        o.append(text('Colours: Espresso #221C18 · Bone #EEE8E0 · Sand #DCCFBF · Clay #9C5B43 (match to Pantone on press proof). Stock: 350gsm SBS / C1S board, matte laminate, spot gloss UV on wordmark optional.', 20, 20, SANS, 3.2, '#333'))
        o.append(text('Supplier: confirm internal dimensions fit the device + accessories before plate-making. Replace all [bracketed] text and add the barcode.', 20, TH-12, SANS, 3.2, '#333'))
    return svg_doc(TW, TH, ''.join(o))

out = 'box'
import os; os.makedirs(out, exist_ok=True)
for name, a, l, lab in [('VELLAN_box_dieline_with_art', 1, 1, 1), ('VELLAN_box_print_art_only', 1, 0, 0), ('VELLAN_box_cutter_lines_only', 0, 1, 1)]:
    s = doc(a, l, lab)
    open(f'{out}/{name}.svg', 'w').write(s)
    cairosvg.svg2pdf(bytestring=s.encode(), write_to=f'{out}/{name}.pdf')
    cairosvg.svg2png(bytestring=s.encode(), write_to=f'{out}/{name}.png', output_width=3000)

# Individual faces for the web mockup
full = doc(1, 0, 0)
for name, (x, y, w, h) in FACES.items() | {'side': (xs[2], y0, D, H), 'lid': (xs[1], y0-D, W, D)}.items():
    s = full.replace(f'viewBox="0 0 {TW} {TH}"', f'viewBox="{x} {y} {w} {h}"').replace(f'width="{TW}mm" height="{TH}mm"', f'width="{w}mm" height="{h}mm"')
    cairosvg.svg2png(bytestring=s.encode(), write_to=f'{out}/face_{name}.png', output_width=int(w*6))
print('ok')
