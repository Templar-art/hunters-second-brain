"""Constrained drone-camera fit to a plate's 2D feature tracks.

Why: on drone wides (distant terrain, slow move) Blender's free solve is ill-conditioned:
sub-pixel error but a camera path that flips push/pull and jerks. A flat-ground prior
pins depth, so the pose is observable from 2D tracks alone.

Models
  line  drone travels a straight line (dolly + climb + crab via a fitted direction),
        gimbal adds small per-frame rotations. Best for reveals / pull-backs / pushes.
  free  full 6-DOF pose per frame (orbits, curved paths), smoothed.
  auto  fits both, keeps `line` unless `free` is clearly better.
Altitude only sets metric scale (bird sizes are chosen in camera space anyway).
"""
import cv2
import numpy as np
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation as Rot


def lk_tracks(frames, max_pts=1500, fb_tol=0.3):
    """Forward/backward-checked LK tracks that survive every frame. frames: list of grey images."""
    p0 = cv2.goodFeaturesToTrack(frames[0], max_pts, 0.01, 18)
    tracks, alive, prev, p = [p0.reshape(-1, 2)], np.ones(len(p0), bool), frames[0], p0
    for b in frames[1:]:
        p2, st, _ = cv2.calcOpticalFlowPyrLK(prev, b, p, None, winSize=(21, 21), maxLevel=3)
        pb, st2, _ = cv2.calcOpticalFlowPyrLK(b, prev, p2, None, winSize=(21, 21), maxLevel=3)
        fb = np.linalg.norm((pb - p).reshape(-1, 2), axis=1)
        alive &= (st.ravel() == 1) & (st2.ravel() == 1) & (fb < fb_tol)
        tracks.append(p2.reshape(-1, 2))
        prev, p = b, p2
    return np.stack(tracks)[:, alive]


class Fitter:
    def __init__(self, T, w, h):
        self.T, self.w, self.h = T, w, h
        self.cx, self.cy = w / 2, h / 2

    @staticmethod
    def R_cam(theta, r):
        right = np.array([1.0, 0, 0])
        fwd = np.array([0, np.cos(theta), -np.sin(theta)])
        down = np.array([0, -np.sin(theta), -np.cos(theta)])
        return np.column_stack([right, down, fwd]) @ Rot.from_rotvec(r).as_matrix()

    def ground_pts(self, theta, f):
        u = self.T[0]
        R = self.R_cam(theta, np.zeros(3))
        d = (R @ np.column_stack([(u[:, 0] - self.cx) / f, (u[:, 1] - self.cy) / f, np.ones(len(u))]).T).T
        X = np.array([0, 0, 1.0]) + (-1.0 / d[:, 2])[:, None] * d
        return X, d[:, 2] < -1e-3

    def project(self, X, C, R, f):
        Xc = (X - C) @ R
        return np.column_stack([f * Xc[:, 0] / Xc[:, 2] + self.cx, f * Xc[:, 1] / Xc[:, 2] + self.cy])

    @staticmethod
    def line_pos(dist, phi, psi):
        """Travel `dist` along a direction with climb phi and crab psi (0 = along the view)."""
        return np.array([dist * np.cos(phi) * np.sin(psi), dist * np.cos(phi) * np.cos(psi), 1 + dist * np.sin(phi)])

    def fit_global(self):
        T = self.T

        def res(x):
            theta, f, phi, psi, dist, *r = x
            X, ok = self.ground_pts(theta, f)
            e = self.project(X, self.line_pos(dist, phi, psi), self.R_cam(theta, np.array(r)), f) - T[-1]
            e[~ok] = 0
            return e.ravel()

        best = None
        for th0 in (12, 20, 32):  # multi-start on pitch
            for d0 in (-0.05, 0.05):
                x0 = [np.radians(th0), 0.75 * self.w, 0.0, 0.0, d0, 0, 0, 0]
                lo = [np.radians(3), 0.4 * self.w, -1.2, -1.2, -0.6, -.1, -.1, -.1]
                hi = [np.radians(75), 1.4 * self.w, 1.2, 1.2, 0.6, .1, .1, .1]
                s = least_squares(res, x0, loss="soft_l1", f_scale=0.5, bounds=(lo, hi))
                if best is None or s.cost < best.cost:
                    best = s
        theta, f, phi, psi = best.x[:4]
        X, ok = self.ground_pts(theta, f)
        err = np.linalg.norm(best.fun.reshape(-1, 2), axis=1)
        inl = ok & (err < 1.5)
        return dict(theta=theta, f=f, phi=phi, psi=psi, X=X, inl=inl, global_err=float(np.median(err[ok])))

    def per_frame(self, g, model):
        T, X, inl, theta, f = self.T, g["X"], g["inl"], g["theta"], g["f"]
        n = len(T)
        params = [np.zeros(4 if model == "line" else 6)]
        for i in range(1, n):
            if model == "line":
                def res(x):
                    return (self.project(X[inl], self.line_pos(x[0], g["phi"], g["psi"]), self.R_cam(theta, x[1:]), f) - T[i][inl]).ravel()
            else:
                def res(x):
                    return (self.project(X[inl], np.array([0, 0, 1.0]) + x[:3], self.R_cam(theta, x[3:]), f) - T[i][inl]).ravel()
            params.append(least_squares(res, params[-1], loss="soft_l1", f_scale=0.5).x)
        P = np.array(params)
        t = np.arange(n)
        deg = min(3, max(1, n // 8))
        Ps = np.column_stack([np.polyval(np.polyfit(t, P[:, k], deg), t) for k in range(P.shape[1])])
        poses, errs = [], []
        for i in range(n):
            if model == "line":
                C, R = self.line_pos(Ps[i, 0], g["phi"], g["psi"]), self.R_cam(theta, Ps[i, 1:])
            else:
                C, R = np.array([0, 0, 1.0]) + Ps[i, :3], self.R_cam(theta, Ps[i, 3:])
            errs.append(float(np.median(np.linalg.norm(self.project(X[inl], C, R, f) - T[i][inl], axis=1))))
            poses.append((C, R))
        return poses, errs


def fit(frames, w, h, fps, altitude=120.0, model="auto", log=print):
    T = lk_tracks(frames)
    log(f"tracks surviving all {len(frames)} frames: {T.shape[1]}")
    if T.shape[1] < 60:
        raise RuntimeError("too few full-length tracks (<60); shot too long or too fast for v1 tracker")
    F = Fitter(T, w, h)
    g = F.fit_global()
    log(f"pitch {np.degrees(g['theta']):.1f}deg, lens {g['f'] / w * 36:.1f}mm-eq, global median err {g['global_err']:.3f}px, inliers {g['inl'].sum()}")
    results = {}
    for m in (["line", "free"] if model == "auto" else [model]):
        poses, errs = F.per_frame(g, m)
        results[m] = (poses, errs)
        log(f"  model {m}: mean {np.mean(errs):.3f}px, max {max(errs):.3f}px")
    pick = "line"
    if model == "auto":
        if np.mean(results["free"][1]) < 0.7 * np.mean(results["line"][1]):
            pick = "free"
    else:
        pick = model
    poses, errs = results[pick]
    flip = np.diag([1, -1, -1])  # OpenCV camera axes -> Blender camera axes
    frames_out = []
    for C, R in poses:
        M = np.eye(4); M[:3, :3] = R @ flip; M[:3, 3] = C * altitude
        frames_out.append(M.tolist())
    travel = float(np.linalg.norm(poses[-1][0] - poses[0][0]) * altitude)
    log(f"picked model '{pick}': mean err {np.mean(errs):.3f}px, travel {travel:.2f}m")
    return {"fps": fps, "width": w, "height": h, "lens_mm": float(g["f"] / w * 36), "sensor_mm": 36.0,
            "altitude_m": altitude, "pitch_deg": float(np.degrees(g["theta"])), "model": pick,
            "tracks": int(T.shape[1]), "inliers": int(g["inl"].sum()),
            "mean_err_px": float(np.mean(errs)), "max_err_px": float(max(errs)),
            "err_px": errs, "travel_m": travel, "frames": frames_out}
