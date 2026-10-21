"""Tracking-only copy of a log plate: strong local contrast (CLAHE on luma) so flat S-Log concrete and lawn
get trackable texture.  python3 trackprep.py <shot dir>   (frames/ -> trk/; the plate itself is never touched)"""
import os, sys, cv2
shot = sys.argv[1]; src = os.path.join(shot, "frames"); dst = os.path.join(shot, "trk"); os.makedirs(dst, exist_ok=True)
cl = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(16, 9))
for f in sorted(os.listdir(src)):
    if f.endswith(".png"):
        im = cv2.imread(os.path.join(src, f)); lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB)
        lab[..., 0] = cl.apply(lab[..., 0]); cv2.imwrite(os.path.join(dst, f), cv2.cvtColor(lab, cv2.COLOR_LAB2BGR))
print("TRK_OK")
