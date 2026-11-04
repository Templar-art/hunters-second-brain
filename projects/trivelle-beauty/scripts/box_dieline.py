"""Trivelle fold-up box: reverse-tuck-end carton dieline + print artwork (SVG, mm units).
Usage: python3 box_dieline.py [L W H]  — inner size in mm (default 140 x 110 x 160, a placeholder:
get the real device + gel + insert size from the supplier / box maker before printing).
Lines: black = cut, red dashed = fold, cyan = 3 mm bleed. Outside face shown; inside is solid lime.
"""
import sys, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{R}/packaging"; os.makedirs(OUT, exist_ok=True)
L, W, H = (float(x) for x in sys.argv[1:4]) if len(sys.argv) == 4 else (140.0, 110.0, 160.0)
GREEN, LIME, WHITE = "#1D2A26", "#C4CE26", "#FFFFFF"
G = 15.0           # glue flap width
T = W * 0.75       # tuck flap depth
DF = W * 0.45      # dust flap depth
M = 20.0           # page margin
# panels left→right: glue | front L | side W | back L | side W
xs = [M, M + G, M + G + L, M + G + L + W, M + G + 2*L + W, M + G + 2*L + 2*W]
y0 = M + W + T      # top of body
y1 = y0 + H         # bottom of body
PW, PH = xs[-1] + M, y1 + W + T + M

cut, fold, art = [], [], []
def C(d): cut.append(f'<path d="{d}"/>')
def F(x1, y1_, x2, y2): fold.append(f'<line x1="{x1}" y1="{y1_}" x2="{x2}" y2="{y2}"/>')

# glue flap (tapered)
C(f"M{xs[1]},{y0} L{xs[0]},{y0+6} L{xs[0]},{y1-6} L{xs[1]},{y1}")
F(xs[1], y0, xs[1], y1)
for x in xs[2:5]: F(x, y0, x, y1)
C(f"M{xs[5]},{y0} L{xs[5]},{y1}")
# top closure on front panel (lid + tuck), bottom closure on back panel (reverse tuck)
def closure(x, w, y, sign):
    lid, tk = y + sign*W, y + sign*(W + T)
    C(f"M{x},{y} L{x},{lid} Q{x},{tk} {x+12},{tk} L{x+w-12},{tk} Q{x+w},{tk} {x+w},{lid} L{x+w},{y}")
    F(x, y, x+w, y); F(x, lid, x+w, lid)
def dust(x, w, y, sign):
    d = y + sign*DF
    C(f"M{x},{y} L{x+2},{d} L{x+w-8},{d} L{x+w},{y}"); F(x, y, x+w, y)
closure(xs[1], L, y0, -1)
closure(xs[3], L, y1, +1)
dust(xs[2], W, y0, -1); dust(xs[4], W, y0, -1)
dust(xs[2], W, y1, +1); dust(xs[4], W, y1, +1)
C(f"M{xs[1]},{y1} L{xs[3]},{y1}")  # under front + side 1: free edge
C(f"M{xs[3]},{y0} L{xs[5]},{y0}")  # over back + side 2: free edge

# artwork: green everywhere outside, with bleed
b = 3
art.append(f'<rect x="{xs[0]-b}" y="{M-b}" width="{xs[5]-xs[0]+2*b}" height="{PH-2*M+2*b}" fill="{GREEN}"/>')
def text(x, y, s, size, fill=WHITE, ls=0, weight=500, rot=0, anchor="middle"):
    tr = f' transform="rotate({rot} {x} {y})"' if rot else ""
    art.append(f'<text x="{x}" y="{y}" font-family="Montserrat, Helvetica, Arial" font-size="{size}" font-weight="{weight}" '
               f'letter-spacing="{ls}" fill="{fill}" text-anchor="{anchor}"{tr}>{s}</text>')
# front: wordmark + lime rule + sub
fx, fy = xs[1] + L/2, y0 + H*0.46
text(fx, fy, "TRIVELLE", L*0.10, ls=L*0.032, weight=500)
art.append(f'<rect x="{fx-9}" y="{fy+7}" width="18" height="0.8" fill="{LIME}"/>')
text(fx, fy + 16, "4-IN-1 SCULPT &amp; GLOW", L*0.034, ls=1.4, weight=400)
# back: same wordmark small + contents + care line
bx = xs[3] + L/2
text(bx, y0 + 30, "TRIVELLE", L*0.06, ls=L*0.02)
for i, s in enumerate(["Heat  ·  Red light  ·  EMS  ·  Vacuum", "",
                       "Contains: 4-in-1 device, microcurrent gel 80 g,", "USB charging cable, user manual",
                       "", "trivellebeauty.com"]):
    text(bx, y0 + H*0.55 + i*7, s, 4.2, weight=400)
# sides: vertical wordmark
for x in (xs[2], xs[4]):
    text(x + W/2, y0 + H/2, "TRIVELLE  ·  SCULPT &amp; GLOW", W*0.05, ls=2.4, rot=-90, weight=400)
# lid (top of front panel when closed): small lime dot mark
text(xs[1] + L/2, y0 - W/2 + 2, "TRIVELLE", L*0.05, fill=LIME, ls=L*0.016)

def svg(name, layers):
    body = "\n".join(layers)
    open(f"{OUT}/{name}", "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{PW}mm" height="{PH}mm" viewBox="0 0 {PW} {PH}">\n'
        f'<rect width="{PW}" height="{PH}" fill="#fff"/>\n{body}\n</svg>\n')

cutg = f'<g fill="none" stroke="#000" stroke-width="0.35">{"".join(cut)}</g>'
foldg = f'<g stroke="#e0001b" stroke-width="0.35" stroke-dasharray="3 2">{"".join(fold)}</g>'
label = (f'<text x="{M}" y="{PH-6}" font-family="Helvetica" font-size="4" fill="#555">Trivelle carton · inner {L:.0f} × {W:.0f} × {H:.0f} mm · '
         f'black = cut · red dashed = fold · artwork has 3 mm bleed · inside face: solid lime {LIME} · PLACEHOLDER SIZE, confirm with box maker</text>')
svg("trivelle-box-dieline.svg", [cutg, foldg, label])
svg("trivelle-box-print.svg", ["".join(art), cutg, foldg, label])
print(f"{OUT}/trivelle-box-print.svg  ({PW:.0f} x {PH:.0f} mm)")
