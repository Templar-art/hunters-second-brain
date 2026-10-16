"""Pre-bake 8 grain tiles (public/grain/g0-7.png) — cheap to composite vs live SVG noise."""
from pathlib import Path
import numpy as np, cv2
out = Path(__file__).resolve().parents[1] / 'public' / 'grain'; out.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(3)
for i in range(8):
    cv2.imwrite(str(out / f'g{i}.png'), (rng.standard_normal((960, 540)) * 40 + 128).clip(0, 255).astype(np.uint8))
