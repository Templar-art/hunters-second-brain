"""Ground-plane mapping through the solved camera (flat-ground prior, world z = 0).

Anything marked once on frame 1 (lot corners, pins, windows, pools) is back-projected onto the ground and
re-projected into every frame, so it stays locked to the footage. Points that really sit above the ground
(roof edges, facades) drift by parallax only, which is sub-pixel to a few px for drone moves of a few metres.
"""
import numpy as np


def cam_A(f_px, w, h):
    return np.array([[1 / f_px, 0, -w / 2 / f_px], [0, -1 / f_px, h / 2 / f_px], [0, 0, -1.0]])


def to_ground(px, M, f_px, w, h):
    """(N,2) pixels -> (N,3) world points on z=0."""
    M = np.asarray(M)
    px = np.atleast_2d(np.asarray(px, float))
    d = np.c_[px, np.ones(len(px))] @ (M[:3, :3] @ cam_A(f_px, w, h)).T
    C = M[:3, 3]
    t = -C[2] / d[:, 2]
    if np.any(t <= 0):
        raise ValueError("a marked point is above the horizon; it cannot sit on the ground")
    return C + t[:, None] * d


def to_pixel(P, M, f_px, w, h):
    """(N,3) world points -> (N,2) pixels (x right, y down)."""
    Minv = np.linalg.inv(np.asarray(M))
    c = np.c_[np.asarray(P, float), np.ones(len(P))] @ Minv.T
    z = -c[:, 2]
    return np.c_[f_px * c[:, 0] / z + w / 2, h / 2 - f_px * c[:, 1] / z]


def ground_H(M1, Mk, f_px, w, h):
    """3x3 homography: frame-k pixels -> frame-1 pixels for points on the ground plane."""
    import cv2
    xs, ys = np.meshgrid(np.linspace(0, w, 6), np.linspace(h * 0.25, h, 5))
    pk = np.c_[xs.ravel(), ys.ravel()]
    P = to_ground(pk, Mk, f_px, w, h)
    p1 = to_pixel(P, M1, f_px, w, h)
    H, _ = cv2.findHomography(pk.astype(np.float32), p1.astype(np.float32))
    return H


def track(marks_px, cam):
    """Frame-1 pixel marks -> list (per CG frame) of (N,2) pixel positions."""
    w, h = cam["width"], cam["height"]
    f_px = cam["lens_mm"] / 36 * w
    P = to_ground(marks_px, cam["frames"][0], f_px, w, h)
    return [to_pixel(P, M, f_px, w, h) for M in cam["frames"]]
