"""Sky probability from SegFormer-B5 (ADE20K class 2 = sky). Runs in the ML venv (torch + transformers).

  ~/.venvs/demucs/bin/python lib/sky_matte.py <job> [frame ...]   -> <job>/sky/{prob,water,pool,build}_####.png (8-bit)

Called by `plate_vfx.py sky`; by default it infers keyframes only (first / middle / last of the CG range)
and the main stage propagates frame 1 through the solved camera rotation.
"""
import json, os, sys
import cv2
import numpy as np
import torch
from transformers import SegformerForSemanticSegmentation

MODEL = "nvidia/segformer-b5-finetuned-ade-640-640"
SKY = 2
WATER = [21, 26, 60, 128]  # water, sea, river, lake
POOL = [109]               # swimming pool
BUILD = [1, 25, 48]        # building, house, skyscraper
dev = "mps" if torch.backends.mps.is_available() else "cpu"


def main():
    job = os.path.abspath(sys.argv[1])
    shot = json.load(open(os.path.join(job, "shot.json")))
    r0, r1 = shot["range"]
    frames = [int(f) for f in sys.argv[2:]] or sorted({r0, (r0 + r1) // 2, r1})
    os.makedirs(os.path.join(job, "sky"), exist_ok=True)
    m = SegformerForSemanticSegmentation.from_pretrained(MODEL).to(dev).eval()
    for f in frames:
        img = cv2.imread(os.path.join(job, "frames", f"f_{f:04d}.png"))[..., ::-1].astype(np.float32) / 255
        h, w = img.shape[:2]
        x = cv2.resize(img, (1280, int(round(1280 * h / w / 32)) * 32))
        x = (x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
        x = torch.tensor(x.transpose(2, 0, 1)[None], dtype=torch.float32).to(dev)
        with torch.no_grad():
            lo = m(pixel_values=x).logits
            sm = torch.nn.functional.interpolate(lo, size=(h, w), mode="bilinear").softmax(1)[0]
            p, wat, pool = sm[SKY].cpu().numpy(), sm[WATER].sum(0).cpu().numpy(), sm[POOL].sum(0).cpu().numpy()
            bld = sm[BUILD].sum(0).cpu().numpy()
        for tag, x in (("prob", p), ("water", wat), ("pool", pool), ("build", bld)):
            cv2.imwrite(os.path.join(job, "sky", f"{tag}_{f:04d}.png"), np.clip(x * 255 + 0.5, 0, 255).astype(np.uint8))
        print(f"SKY_PROB {f} {float((p > 0.5).mean()):.4f}")


if __name__ == "__main__":
    main()
