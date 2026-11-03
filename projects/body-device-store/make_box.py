# Straight-tuck-end folding carton. Units mm. Outputs SVG dieline + print art.
W,D,H=230,80,170   # front width, depth, height (internal approx)
B=3; TUCK=D*0.9; GLUE=15; PX=4  # bleed, tuck depth, glue flap
INK='#2a2420'; ACC='#b4775a'; CREAM='#f4ede4'
x0=20; y0=20+D+TUCK
cols=[(GLUE,'glue'),(W,'front'),(D,'side'),(W,'back'),(D,'side')]
xs=[x0]; 
for w,_ in cols: xs.append(xs[-1]+w)
TW=xs[-1]+20; TH=y0+H+D+TUCK+20
cut=[];fold=[];art=[]
def r(x,y,w,h): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>'
# body outline pieces
gx=xs[0]
cut.append(f'M{gx+GLUE},{y0} L{gx},{y0+6} L{gx},{y0+H-6} L{gx+GLUE},{y0+H}')
for i in range(1,5): fold.append(f'M{xs[i]},{y0} L{xs[i]},{y0+H}')
# top: front panel gets lid (D) + tuck; sides get dust flaps; back plain
fx=xs[1]
cut.append(f'M{fx},{y0} L{fx},{y0-D} Q{fx},{y0-D-TUCK} {fx+12},{y0-D-TUCK} L{fx+W-12},{y0-D-TUCK} Q{fx+W},{y0-D-TUCK} {fx+W},{y0-D} L{fx+W},{y0}')
fold.append(f'M{fx},{y0} L{fx+W},{y0}'); fold.append(f'M{fx},{y0-D} L{fx+W},{y0-D}')
for i in (2,4):
  sx=xs[i]; cut.append(f'M{sx},{y0} L{sx+2},{y0-D*0.8} L{sx+D-8},{y0-D*0.8} L{sx+D},{y0-8} L{sx+D},{y0}'); fold.append(f'M{sx},{y0} L{sx+D},{y0}')
cut.append(f'M{xs[3]},{y0} L{xs[4]},{y0}')
# bottom: back panel gets base + tuck (reverse), sides dust flaps, front plain
yb=y0+H; bx=xs[3]
cut.append(f'M{bx},{yb} L{bx},{yb+D} Q{bx},{yb+D+TUCK} {bx+12},{yb+D+TUCK} L{bx+W-12},{yb+D+TUCK} Q{bx+W},{yb+D+TUCK} {bx+W},{yb+D} L{bx+W},{yb}')
fold.append(f'M{bx},{yb} L{bx+W},{yb}'); fold.append(f'M{bx},{yb+D} L{bx+W},{yb+D}')
for i in (2,4):
  sx=xs[i]; cut.append(f'M{sx},{yb} L{sx},{yb+8} L{sx+8},{yb+D*0.8} L{sx+D-2},{yb+D*0.8} L{sx+D},{yb}'); fold.append(f'M{sx},{yb} L{sx+D},{yb}')
cut.append(f'M{xs[1]},{yb} L{xs[2]},{yb}'); cut.append(f'M{xs[5]},{y0} L{xs[5]},{yb}')
def logo(cx,cy,s,col):
  return f'<g fill="{col}" text-anchor="middle"><circle cx="{cx}" cy="{cy-s*1.1}" r="{s*0.38}" fill="none" stroke="{col}" stroke-width="{s*0.06}"/><circle cx="{cx}" cy="{cy-s*1.1}" r="{s*0.14}"/><text x="{cx+s*0.16}" y="{cy}" font-family="Fraunces, Georgia, serif" font-size="{s}" letter-spacing="{s*0.32}">VELLAN</text></g>'
def txt(x,y,s,t,col=INK,anchor='middle',w=400,ls=0):
  return f'<text x="{x}" y="{y}" font-family="Inter, Helvetica, sans-serif" font-size="{s}" font-weight="{w}" fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{t}</text>'
# artwork backgrounds (with bleed)
art.append(f'<rect x="{xs[1]-B}" y="{y0-D-TUCK-B}" width="{W+2*B}" height="{H+D+TUCK+2*B}" fill="{CREAM}"/>')
art.append(f'<rect x="{xs[0]-B}" y="{y0-B}" width="{xs[5]-xs[0]+2*B}" height="{H+2*B}" fill="{CREAM}"/>')
art.append(f'<rect x="{xs[3]-B}" y="{yb-B}" width="{W+2*B}" height="{D+TUCK+2*B}" fill="{CREAM}"/>')
for i in (2,4): art.append(f'<rect x="{xs[i]}" y="{y0}" width="{D}" height="{H}" fill="{INK}"/>')
art.append(f'<rect x="{xs[1]}" y="{y0-D}" width="{W}" height="{D}" fill="{INK}"/>')
art.append(logo(xs[1]+W/2,y0-D/2+12,16,CREAM))
# front
c=xs[1]+W/2
art.append(logo(c,y0+62,22,INK))
art.append(txt(c,y0+90,6.5,'4-IN-1 BODY SCULPTING DEVICE',ACC,w=600,ls=1.6))
art.append(f'<line x1="{c-30}" y1="{y0+104}" x2="{c+30}" y2="{y0+104}" stroke="{ACC}" stroke-width=".5"/>')
art.append(txt(c,y0+122,5.5,'WARMTH · DYNAMIC SUCTION · RED LIGHT · MICROCURRENT',INK,ls=.8))
art.append(txt(c,y0+H-14,5,'FULL KIT',INK,w=600,ls=2))
# back
c=xs[3]+W/2
art.append(txt(c,y0+28,9,'Fifteen minutes a day, at home.',INK))
for k,(a,b) in enumerate([('In the box','Device · 3 treatment heads · 100ml conductive gel · USB-C cable · Pouch · Guide'),('How to use','Charge, apply gel, set your levels, glide for 15 minutes.'),('Caution','Not for use during pregnancy, with implanted electronic devices, or on broken skin.')]):
  yy=y0+52+k*30
  art.append(txt(xs[3]+18,yy,5.5,a.upper(),ACC,'start',600,1.2)); art.append(txt(xs[3]+18,yy+10,5,b,INK,'start'))
art.append(txt(xs[3]+18,y0+130,5,'Read the guide before first use.',INK,'start'))
art.append(f'<rect x="{xs[3]+W-70}" y="{y0+H-42}" width="52" height="28" fill="#fff" stroke="{INK}" stroke-width=".3"/>')
art.append(txt(xs[3]+W-44,y0+H-26,4,'BARCODE',INK))
art.append(txt(xs[3]+18,y0+H-30,4.5,'[Company name] · ABN [xx xxx xxx xxx]',INK,'start'))
art.append(txt(xs[3]+18,y0+H-22,4.5,'vellan.com.au · Made in [country]',INK,'start'))
art.append(txt(xs[3]+18,y0+H-14,4.5,'Model [xxx] · 5V DC 1A · [battery mAh]  · CE · RCM',INK,'start'))
# sides
for i in (2,4):
  sx=xs[i]+D/2
  art.append(f'<g transform="translate({sx},{y0+H/2}) rotate(-90)">{logo(0,6,13,CREAM)}</g>')
art.append(txt(xs[1]+W/2,yb+D/2+3,6,'VELLAN.COM.AU',INK,ls=2))
def svg(with_art,with_lines,labels):
  o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{TW}mm" height="{TH}mm" viewBox="0 0 {TW} {TH}">','<rect width="100%" height="100%" fill="#fff"/>']
  if with_art: o+=art
  if with_lines:
    o.append('<g fill="none" stroke="#e00" stroke-width=".35">'+''.join(f'<path d="{p}"/>' for p in cut)+'</g>')
    o.append('<g fill="none" stroke="#00a" stroke-width=".35" stroke-dasharray="3 2">'+''.join(f'<path d="{p}"/>' for p in fold)+'</g>')
  if labels:
    o.append(txt(20,10,4.5,f'VELLAN Full Kit — straight tuck end carton · {W}×{D}×{H} mm (W×D×H) · 3 mm bleed · RED=cut  BLUE dashed=fold · confirm against device + supplier template','#000','start',600))
  o.append('</svg>'); return '\n'.join(o)
open('box_dieline_print.svg','w').write(svg(True,True,True))
open('box_dieline_lines_only.svg','w').write(svg(False,True,True))
open('box_artwork_no_lines.svg','w').write(svg(True,False,False))
open('logo.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 140" width="300" height="140"><rect width="300" height="140" fill="#fff"/>{logo(150,108,40,INK)}</svg>')
open('logo_light.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 140" width="300" height="140"><rect width="300" height="140" fill="{INK}"/>{logo(150,108,40,CREAM)}</svg>')
print('ok')
