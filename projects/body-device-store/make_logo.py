from brand import *
import cairosvg
B=[]
def save(name,w,h,body,bg):
    s=svg_doc(w,h,body,bg,units='')
    open(f'brand/{name}.svg','w').write(s)
    cairosvg.svg2png(bytestring=s.encode(),write_to=f'brand/{name}.png',output_width=w*4)
    cairosvg.svg2pdf(bytestring=s.encode(),write_to=f'brand/{name}.pdf')
save('logo-stacked-espresso',400,260,lockup(200,140,52,ESPRESSO,CLAY),BONE)
save('logo-stacked-bone',400,260,lockup(200,140,52,BONE,SAND),ESPRESSO)
save('logo-wordmark-espresso',420,120,wordmark(210,78,56,ESPRESSO),None)
save('logo-wordmark-bone',420,120,wordmark(210,78,56,BONE),ESPRESSO)
save('logo-mark-clay',200,200,mark(100,100,120,CLAY),None)
save('favicon',64,64,mark(32,32,40,BONE),CLAY)
print('ok')
