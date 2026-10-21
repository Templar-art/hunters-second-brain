"""Render every Poly Haven sky as the band a camera actually shows (0-36 deg above the horizon), looking
30 deg off the sun, tone-mapped with highlight-preserving auto exposure. Output: renders/<id>.jpg + sheets."""
import json, math, os, sys
import cv2
import numpy as np

W, H, HFOV, PITCH = 480, 270, 84.0, 14.0
meta = json.load(open("polyhaven_skies.json"))


def sun_az(hdr):
    h, w = hdr.shape[:2]
    lum = cv2.GaussianBlur(hdr[: h // 2].mean(2), (0, 0), 3)
    r, c = np.unravel_index(np.argmax(lum), lum.shape)
    return (0.5 - (c + 0.5) / w) * 2 * math.pi, 90 * (1 - (r + 0.5) / (h / 2))


def view(hdr, yaw, pitch=PITCH):
    f = (W / 2) / math.tan(math.radians(HFOV / 2))
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    x, y, z = (xs - W / 2) / f, -(ys - H / 2) / f, np.ones_like(xs)
    p = math.radians(pitch)
    y2, z2 = y * math.cos(p) + z * math.sin(p), -y * math.sin(p) + z * math.cos(p)
    el = np.arctan2(y2, np.hypot(x, z2))
    az = yaw - np.arctan2(x, z2)
    hh, ww = hdr.shape[:2]
    u = ((0.5 - az / (2 * math.pi)) % 1.0) * ww - 0.5
    v = (0.5 - el / math.pi) * hh - 0.5
    return cv2.remap(hdr, u.astype(np.float32), v.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP), el


def tonemap(x, key=0.9):
    lum = x @ np.array([0.0722, 0.7152, 0.2126], np.float32)
    k = key / max(np.percentile(lum, 97), 1e-6)  # keep the glow, let the sun clip
    y = x * k
    y = y / (1 + y * 0.35)
    return np.clip(np.power(np.clip(y, 0, 1), 1 / 2.2) * 255, 0, 255).astype(np.uint8)


def main():
    rows = []
    for i, k in enumerate(sorted(meta)):
        out = f"renders/{k}.jpg"
        a = meta[k].get("attributes", {})
        if not os.path.exists(out):
            hdr = cv2.imread(f"hdr_1k/{k}.hdr", cv2.IMREAD_ANYDEPTH | cv2.IMREAD_COLOR)
            if hdr is None:
                continue
            hdr = hdr.astype(np.float32)
            saz, sel = sun_az(hdr)
            img, el = view(hdr, saz + math.radians(30))
            im = tonemap(img)
            im[el < 0] = (im[el < 0] * 0.25).astype(np.uint8)  # dim below-horizon (HDRI ground isn't ours)
            cv2.imwrite(out, im, [cv2.IMWRITE_JPEG_QUALITY, 88])
            meta[k]["_sun_el"] = round(sel, 1)
        rows.append((k, a.get("time_of_day"), a.get("weather")))
    json.dump({k: meta[k].get("_sun_el") for k in meta if "_sun_el" in meta[k]}, open("sun_el.json", "w"))
    print("rendered", len(rows))


if __name__ == "__main__":
    main()
