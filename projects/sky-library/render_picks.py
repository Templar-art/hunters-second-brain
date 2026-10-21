"""Hi-res views of the picks: toward the sun, sun behind, and a 360 strip of the 0-40 deg band."""
import json, math, cv2, numpy as np
import render_views as rv
rv.W, rv.H = 1600, 900
p = json.load(open("picks.json"))
KEY = {"night": 0.22, "dusk": 0.7}  # real night reads dark; auto-exposure would turn it into day
for t, ks in p.items():
    for k in ks:
        hdr = cv2.imread(f"hdr_2k/{k}.hdr", cv2.IMREAD_ANYDEPTH | cv2.IMREAD_COLOR).astype(np.float32)
        saz, sel = rv.sun_az(hdr)
        for tag, off in (("sun", 30), ("away", 150)):
            img, el = rv.view(hdr, saz + math.radians(off))
            im = rv.tonemap(img, KEY.get(t, 0.9)); im[el < 0] = (im[el < 0] * 0.25).astype(np.uint8)
            cv2.imwrite(f"picks/{t}_{k}_{tag}.jpg", im, [cv2.IMWRITE_JPEG_QUALITY, 90])
        h, w = hdr.shape[:2]
        band = hdr[int(h * (0.5 - 40 / 180)):int(h * 0.5)]
        band = np.roll(band, int(w * ((saz / (2 * math.pi)) % 1)) , axis=1)  # sun centred-ish
        cv2.imwrite(f"picks/{t}_{k}_strip.jpg", cv2.resize(rv.tonemap(band, KEY.get(t, 0.9)), (2400, 300)), [cv2.IMWRITE_JPEG_QUALITY, 88])
print("done")
