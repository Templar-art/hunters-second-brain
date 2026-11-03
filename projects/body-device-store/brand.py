"""VELLAN brand toolkit: outlined text, logo mark, colour tokens.
All output text is converted to vector paths so print files need no fonts."""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))

# Palette
BONE = '#EEE8E0'      # primary background
SAND = '#DCCFBF'      # secondary surface
CLAY = '#9C5B43'      # accent
ESPRESSO = '#221C18'  # ink
STONE = '#7A6E64'     # secondary ink

_cache = {}
def font(name, wght):
    key = (name, wght)
    if key not in _cache:
        f = TTFont(os.path.join(HERE, 'fonts', f'{name}.ttf'))
        _cache[key] = instancer.instantiateVariableFont(f, {'wght': wght})
    return _cache[key]

SERIF = ('Cormorant', 500)
SERIF_LIGHT = ('Cormorant', 400)
SANS = ('Jost', 400)
SANS_MED = ('Jost', 500)

def measure(text, face, size, track=0):
    f = font(*face); cmap = f.getBestCmap(); hmtx = f['hmtx']
    upm = f['head'].unitsPerEm; s = size / upm
    w = sum(hmtx[cmap.get(ord(c), cmap[ord(' ')])][0] * s for c in text)
    return w + track * max(len(text) - 1, 0)

def text(t, x, y, face, size, fill, anchor='start', track=0):
    """Return an SVG <path> of the string, baseline at y. track in output units."""
    f = font(*face); gs = f.getGlyphSet(); cmap = f.getBestCmap(); hmtx = f['hmtx']
    upm = f['head'].unitsPerEm; s = size / upm
    w = measure(t, face, size, track)
    if anchor == 'middle': x -= w / 2
    elif anchor == 'end': x -= w
    pen = SVGPathPen(gs); cx = x
    for c in t:
        g = cmap.get(ord(c), cmap[ord(' ')])
        tp = TransformPen(pen, (s, 0, 0, -s, cx, y))
        gs[g].draw(tp)
        cx += hmtx[g][0] * s + track
    return f'<path d="{pen.getCommands()}" fill="{fill}"/>'

def lines(paras, x, y, face, size, fill, width, lead=1.45, track=0):
    """Simple word-wrap into outlined lines. Returns (svg, y_after)."""
    out = []
    for para in paras:
        line = ''
        for word in para.split():
            trial = (line + ' ' + word).strip()
            if measure(trial, face, size, track) > width and line:
                out.append(text(line, x, y, face, size, fill, track=track)); y += size * lead; line = word
            else:
                line = trial
        if line:
            out.append(text(line, x, y, face, size, fill, track=track)); y += size * lead
    return ''.join(out), y

def mark(cx, cy, h, fill):
    """The V-contour mark: two tapering curves meeting at a point, like a waistline.
    h = total height; centred on (cx, cy)."""
    w = h * 0.78; t = h * 0.075
    top = cy - h / 2; bot = cy + h / 2
    def half(sign):
        x0 = cx + sign * w / 2
        return (f'M{x0},{top} C{x0 - sign*w*0.02},{top + h*0.38} {cx + sign*w*0.30},{top + h*0.55} {cx},{bot} '
                f'C{cx + sign*w*0.30 - sign*t*1.6},{top + h*0.55} {x0 - sign*t*1.4},{top + h*0.38} {x0 - sign*t*1.1},{top} Z')
    return f'<path d="{half(-1)} {half(1)}" fill="{fill}"/>'

WORD = 'VELLAN'
def wordmark(cx, baseline, size, fill):
    return text(WORD, cx, baseline, SERIF, size, fill, 'middle', track=size * 0.26)

def lockup(cx, cy, size, fill, accent=None):
    """Stacked lockup: mark above wordmark. size = cap height-ish of wordmark."""
    accent = accent or fill
    m = mark(cx, cy - size * 0.78, size * 0.9, accent)
    return m + wordmark(cx, cy + size * 0.62, size, fill)

def svg_doc(w, h, body, bg=None, units='mm'):
    b = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    u = units if units else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}{u}" height="{h}{u}" '
            f'viewBox="0 0 {w} {h}">{b}{body}</svg>')
