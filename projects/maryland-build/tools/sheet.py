"""contact sheet: python3 tools/sheet.py out.jpg cols img1 img2 ..."""
import sys, os, cv2, numpy as np
out, cols, fs = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
t = []
for f in fs:
    im = cv2.resize(cv2.imread(f), (640, 360)); cv2.putText(im, os.path.basename(f)[:-4], (8, 24), 0, 0.7, (0, 255, 255), 2); t.append(im)
while len(t) % cols: t.append(np.zeros_like(t[0]))
cv2.imwrite(out, np.vstack([np.hstack(t[i:i + cols]) for i in range(0, len(t), cols)]), [1, 85])
