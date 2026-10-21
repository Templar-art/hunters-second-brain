"""Tracked sky replacement: an HDRI sky dome driven by the solved camera, composited inside a refined sky matte.

Matte: SegFormer sky probability on frame 1 (lib/sky_matte.py), carried to every frame by the pure-rotation
homography H = A^-1 R1^T Rk A (the horizon is at infinity, so this is exact for distant skylines and cannot
flicker), then edge-refined per frame with a guided filter on the plate. If the propagated matte disagrees
with a fresh inference on the last frame (near objects in the sky = parallax), every frame is inferred instead.

Sky: each pixel's world ray is looked up in an equirect HDRI (Blender convention), with one exposure locked
for the whole shot, a soft highlight shoulder, a touch of the plate's warmth, and the plate's own horizon
haze mixed back in near the skyline. Output is an RGBA layer, so plate.composite()/verify() apply unchanged:
nothing outside the sky matte is touched.
"""
import math
import cv2
import numpy as np


from ground import cam_A  # pixel (x right, y down, 1) -> Blender camera ray (x right, y up, -z forward)


def rot_homography(M1, Mk, f_px, w, h):
    """Maps frame-k pixels to frame-1 pixels for points at infinity."""
    A = cam_A(f_px, w, h)
    R1, Rk = np.asarray(M1)[:3, :3], np.asarray(Mk)[:3, :3]
    return np.linalg.inv(A) @ R1.T @ Rk @ A


def guided(I, p, r=8, eps=2e-3):
    box = lambda x: cv2.boxFilter(x, -1, (2 * r + 1, 2 * r + 1))
    mI, mp = box(I), box(p)
    a = (box(I * p) - mI * mp) / (box(I * I) - mI * mI + eps)
    b = mp - a * mI
    return box(a) * I + box(b)


def refine(prob, plate_bgr):
    g = cv2.cvtColor(plate_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    a = guided(g, prob.astype(np.float32), r=6, eps=1e-3)
    a = np.clip((a - 0.08) / 0.84, 0, 1)  # firm the core, keep a soft skyline edge
    return a


def iou(a, b):
    a, b = a > 0.5, b > 0.5
    return float((a & b).sum() / max(1, (a | b).sum()))


def load_hdri(path):
    hdr = cv2.imread(path, cv2.IMREAD_ANYDEPTH | cv2.IMREAD_COLOR)
    if hdr is None:
        raise SystemExit(f"cannot read {path}")
    return hdr.astype(np.float32)  # BGR linear


def sun_azimuth(hdr):
    """Azimuth (rad, Blender equirect convention) of the brightest blob in the upper hemisphere."""
    H, W = hdr.shape[:2]
    lum = cv2.GaussianBlur(hdr[: H // 2].mean(2), (0, 0), 6)
    r, c = np.unravel_index(np.argmax(lum), lum.shape)
    return (0.5 - (c + 0.5) / W) * 2 * math.pi, float(lum[r, c])


def pixel_dirs(M, f_px, w, h):
    """Unit world ray for every pixel, (h*w, 3)."""
    A = cam_A(f_px, w, h)
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    pix = np.stack([xs, ys, np.ones_like(xs)], -1).reshape(-1, 3)
    d = pix @ (np.asarray(M)[:3, :3] @ A).T
    return d / np.linalg.norm(d, axis=1, keepdims=True)


def sample(hdr, d, w, h, yaw, lift=0.0):
    """Look up world directions d (h*w, 3) in an equirect HDRI (Blender convention). lift: degrees added to every
    ray's elevation. Drones see only the hazy band just above the HDRI horizon; lifting samples the bluer,
    cloud-detailed sky higher up (cloud height is unreadable, so it looks natural)."""
    az = np.arctan2(d[:, 1], d[:, 0]) - yaw
    el = np.clip(np.arcsin(np.clip(d[:, 2], -1, 1)) + math.radians(lift), -math.pi / 2 + 1e-4, math.pi / 2 - 1e-4)
    H, W = hdr.shape[:2]
    u = ((0.5 - az / (2 * math.pi)) % 1.0) * W - 0.5
    v = (0.5 - el / math.pi) * H - 0.5
    return cv2.remap(hdr, u.reshape(h, w).astype(np.float32), v.reshape(h, w).astype(np.float32),
                     cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)


def render_sky(hdr, M, f_px, w, h, yaw, lift=0.0):
    return sample(hdr, pixel_dirs(M, f_px, w, h), w, h, yaw, lift)


def tone_lin(lin, exposure, warmth=1.0, shoulder=4.0):
    """Exposure + highlight shoulder + plate warmth, still linear (0-1)."""
    x = lin * exposure
    x = x * (1 + x / shoulder ** 2) / (1 + x)
    return np.clip(x * np.array([warmth ** -0.25, 1.0, warmth ** 0.25], np.float32), 0, 1)


def tone(lin, exposure, warmth=1.0, shoulder=4.0):
    x = lin * exposure
    x = x * (1 + x / shoulder ** 2) / (1 + x)  # extended Reinhard: clouds/sun roll off instead of clipping
    x = x * np.array([warmth ** -0.25, 1.0, warmth ** 0.25], np.float32)  # BGR: share the plate's grade
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1 / 2.4) - 0.055) * 255


def layer(plate_bgr, sky_srgb, alpha, haze=0.55, haze_px=45):
    """RGBA sky layer (straight alpha). Near the skyline the plate's own haze is mixed back in."""
    inside = (alpha > 0.5).astype(np.uint8)
    dist = cv2.distanceTransform(inside, cv2.DIST_L2, 5)
    m = (haze * np.exp(-dist / haze_px))[..., None]
    rgb = sky_srgb * (1 - m) + plate_bgr.astype(np.float32) * m
    return np.dstack([np.clip(rgb + 0.5, 0, 255), np.clip(alpha * 255 + 0.5, 0, 255)]).astype(np.uint8)
