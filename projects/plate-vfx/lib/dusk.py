"""Day-to-dusk for drone video: twilight grade + tracked dusk sky + sky reflected in the water + lights.

Everything happens in linear light, per frame, through the solved camera:
  1. ground grade: exposure down, cool ambient, a little desaturation, a warm glow rising toward the skyline
     and a brighter, warmer side toward the sun.
  2. water: the dusk HDRI sampled along each pixel's mirror ray, mixed in with Schlick Fresnel (grazing water
     far away reflects a lot, water under the drone barely does). Water matte from SegFormer, carried
     through the ground-plane homography.
  3. sky: the tracked HDRI dome from lib/sky.py inside the refined sky matte.
  4. emission: windows, pools and streetlights from marks.json, tracked on the ground plane, with bloom.
Unlike birds/lines/sky this stage regrades the whole plate by design, so there is no untouched check;
QC is the before/after pilot.
"""
import numpy as np
import cv2

import ground
import sky

WIN = np.array([0.30, 0.62, 1.00], np.float32)   # ~2700 K interior, linear BGR
LAMP = np.array([0.42, 0.72, 1.00], np.float32)  # ~3000 K street LED
POOL = np.array([1.00, 0.78, 0.22], np.float32)  # pool LED cyan

LOOK = dict(ev=-2.5, cool=(1.50, 1.04, 0.72), sat=0.60, contrast=1.2, glow=0.30, glow_falloff=0.12, sky_gain=0.32, water_refl=0.7, sun_side=0.15, win=1.1, lamp=2.2,
            pool=0.55, sky_brightness=0.55, water_rough=2.5)

# twilight ramp, linear BGR: warm band on the horizon near the sun, rose further round, deep blue overhead
HORIZON_SUN = np.array([0.10, 0.36, 1.00], np.float32)
HORIZON_AWAY = np.array([0.42, 0.26, 0.40], np.float32)
ZENITH = np.array([0.42, 0.13, 0.04], np.float32)


def twilight(sky_lin, d, sun_az, gain=1.0):
    """Recolour a sampled HDRI into a blue-hour sky. The HDRI keeps its clouds as luminance texture; colour comes
    from elevation (warm band -> deep blue over ~12 deg) and distance from the sun's azimuth."""
    h, w = sky_lin.shape[:2]
    el = np.degrees(np.arcsin(np.clip(d[:, 2], -1, 1))).reshape(h, w, 1)
    az = np.arctan2(d[:, 1], d[:, 0]).reshape(h, w, 1)
    near = np.clip(np.cos(az - sun_az), 0, 1) ** 3
    t = np.clip(el / 12.0, 0, 1)  # drones see ~12 deg of sky: the whole ramp has to fit in it
    t = t * t * (3 - 2 * t)
    horizon = HORIZON_AWAY + (HORIZON_SUN - HORIZON_AWAY) * near
    col = horizon * (1 - t) + ZENITH * t
    lum = sky_lin @ np.array([0.0722, 0.7152, 0.2126], np.float32)
    tex = (lum / max(1e-6, float(np.median(lum))))[..., None]
    tex = np.clip(tex, 0, 4)
    return col * (0.55 + 0.45 * tex) * gain


def to_lin(srgb8):
    x = srgb8.astype(np.float32) / 255
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def to_srgb8(lin):
    x = np.clip(lin, 0, 1)
    return np.clip(np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1 / 2.4) - 0.055) * 255 + 0.5, 0, 255).astype(np.uint8)


def skyline_rows(sky_a):
    """Per column, the lowest row that is still sky (the skyline), smoothed."""
    h, w = sky_a.shape
    s = sky_a > 0.5
    rows = np.where(s.any(0), h - 1 - np.argmax(s[::-1], 0), 0).astype(np.float32)
    return cv2.GaussianBlur(rows[None], (0, 0), 25)[0]


def grade(lin, sky_a, sun_x, horizon_col, L):
    h, w = lin.shape[:2]
    x = lin * 2 ** L["ev"]
    lum = x @ np.array([0.0722, 0.7152, 0.2126], np.float32)
    x = lum[..., None] + (x - lum[..., None]) * L["sat"]
    x = 0.18 * np.power(np.maximum(x, 0) / 0.18, L["contrast"])
    lum = x @ np.array([0.0722, 0.7152, 0.2126], np.float32)
    shadow = np.clip(1 - lum / 0.12, 0, 1)[..., None]  # blue lands in the shadows, highlights stay closer to neutral
    x = x * (1 + (np.array(L["cool"], np.float32) - 1) * (0.45 + 0.55 * shadow))
    # warm atmospheric glow just below the skyline, fading toward the camera
    ys = np.arange(h, dtype=np.float32)[:, None]
    hz = skyline_rows(sky_a)[None]
    below = np.clip(ys - hz, 0, None)
    glow = np.exp(-below / (L["glow_falloff"] * h))[..., None] * horizon_col[None, None] * L["glow"]
    # brighter and warmer on the sun side of frame
    side = np.clip(1 - np.abs(np.arange(w, dtype=np.float32) - sun_x) / (0.9 * w), 0, 1)[None, :, None] ** 2
    x = x * (1 + L["sun_side"] * side * np.array([0.6, 0.9, 1.25], np.float32)) + glow * (0.5 + side)
    return x


def fresnel(d):
    c = np.abs(d[:, 2])
    return 0.02 + 0.98 * (1 - c) ** 5


def emission(marks_trk, k, w, h, L):
    """Linear BGR light image for frame k."""
    E = np.zeros((h, w, 3), np.float32)

    def poly_light(polys, col, gain, blur=0.8):
        m = np.zeros((h, w), np.float32)
        for i, p in enumerate(polys):  # not every room is lit the same
            cv2.fillPoly(m, [np.round(p[k] * 4).astype(np.int32)], 0.7 + 0.5 * ((i * 0.618) % 1), cv2.LINE_AA, shift=2)
        m = cv2.GaussianBlur(m, (0, 0), blur)
        core = m[..., None] * col * gain
        return core + cv2.GaussianBlur(core, (0, 0), 5) * 0.45 + cv2.GaussianBlur(core, (0, 0), 22) * 0.25

    E += poly_light(marks_trk["windows"], WIN, L["win"])
    E += poly_light(marks_trk["pools"], POOL, L["pool"], blur=1.5)
    if marks_trk["lamps"]:
        pts = marks_trk["lamps"][k]
        core = np.zeros((h, w), np.float32)
        spill = np.zeros((h, w), np.float32)
        for x, y in pts:
            cv2.circle(core, (int(round(x * 4)), int(round(y * 4))), 8, 1.0, -1, cv2.LINE_AA, shift=2)
            cv2.ellipse(spill, (int(round(x * 4)), int(round(y * 4))), (170, 60), 0, 0, 360, 1.0, -1, cv2.LINE_AA, shift=2)
        core = core[..., None] * LAMP * L["lamp"]
        E += core + cv2.GaussianBlur(core, (0, 0), 4) * 0.6 + cv2.GaussianBlur(core, (0, 0), 18) * 0.3
        E += cv2.GaussianBlur(spill, (0, 0), 12)[..., None] * LAMP * 0.05 * L["lamp"]
    return E


def track_marks(marks, cam):
    return {"windows": [ground.track(p, cam) for p in marks.get("windows", [])],
            "pools": [ground.track(p, cam) for p in marks.get("pools", [])],
            "lamps": ground.track(marks["lamps"], cam) if marks.get("lamps") else []}


def frame(plate_bgr, sky_a, water_a, hdr, M, f_px, yaw, lift, expo, warmth, sun_x, horizon_col, E, L, sun_az):
    h, w = plate_bgr.shape[:2]
    lin = grade(to_lin(plate_bgr), sky_a, sun_x, horizon_col, L)
    d = sky.pixel_dirs(M, f_px, w, h)
    if water_a is not None and water_a.max() > 0:
        r = d * np.array([1, 1, -1], np.float32)
        refl = twilight(sky.tone_lin(sky.sample(hdr, r, w, h, yaw, lift), expo, warmth), r * np.array([1, 1, -1], np.float32),
                        sun_az, L["sky_gain"])
        refl = cv2.GaussianBlur(refl, (0, 0), L["water_rough"])
        F = (fresnel(d).reshape(h, w) * water_a)[..., None] * L["water_refl"]
        lin = lin * (1 - F) + refl * F
    s = twilight(sky.tone_lin(sky.sample(hdr, d, w, h, yaw, lift), expo, warmth), d, sun_az, L["sky_gain"])
    a = sky_a[..., None]
    lin = lin * (1 - a) + s * a
    return to_srgb8(lin + E)
