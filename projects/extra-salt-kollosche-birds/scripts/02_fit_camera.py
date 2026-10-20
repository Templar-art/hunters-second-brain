"""Fit a physical drone camera to the plate's 2D feature tracks.

Blender's free solve is ill-conditioned here (long push, almost no parallax), so we
constrain it: flat ground at z=0, drone at height H moving in a straight line, base
pitch + focal fitted globally, then per-frame travel + tiny gimbal rotations,
smoothed with a low-order polynomial. Writes camera.json (Blender world matrices).
"""
import json, os
import cv2
import numpy as np
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation as Rot

JOB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N, W, Hh = 45, 1920, 1080
CX, CY = W / 2, Hh / 2
H = 120.0  # assumed altitude (m) — sets metric scale only

g = lambda i: cv2.imread(os.path.join(JOB, "frames", f"f_{i:04d}.png"), 0)

# --- forward/backward-checked LK tracks across all 45 frames
f1 = g(1)
p0 = cv2.goodFeaturesToTrack(f1, 1500, 0.01, 18)
tracks = [p0.reshape(-1, 2)]
alive = np.ones(len(p0), bool)
prev, p = f1, p0
for i in range(2, N + 1):
    b = g(i)
    p2, st, _ = cv2.calcOpticalFlowPyrLK(prev, b, p, None, winSize=(21, 21), maxLevel=3)
    pb, st2, _ = cv2.calcOpticalFlowPyrLK(b, prev, p2, None, winSize=(21, 21), maxLevel=3)
    fb = np.linalg.norm((pb - p).reshape(-1, 2), axis=1)
    alive &= (st.ravel() == 1) & (st2.ravel() == 1) & (fb < 0.3)
    tracks.append(p2.reshape(-1, 2))
    prev, p = b, p2
T = np.stack(tracks)[:, alive]  # (N, M, 2)
print("tracks kept", T.shape[1])


def R_cam(theta, r):
    fwd = np.array([0, np.cos(theta), -np.sin(theta)])
    right = np.array([1.0, 0, 0])
    down = np.array([0, -np.sin(theta), -np.cos(theta)])
    return np.column_stack([right, down, fwd]) @ Rot.from_rotvec(r).as_matrix()


def ground_pts(theta, f):
    R = R_cam(theta, np.zeros(3))
    u = T[0]
    d = (R @ np.column_stack([(u[:, 0] - CX) / f, (u[:, 1] - CY) / f, np.ones(len(u))]).T).T
    t = -1.0 / d[:, 2]
    X = np.array([0, 0, 1.0]) + t[:, None] * d
    return X, d[:, 2] < -1e-3


def project(X, C, R, f):
    Xc = (X - C) @ R
    return np.column_stack([f * Xc[:, 0] / Xc[:, 2] + CX, f * Xc[:, 1] / Xc[:, 2] + CY])


def cam_pos(dist, phi):
    return np.array([0, dist * np.cos(phi), 1 + dist * np.sin(phi)])


# --- global fit on the last frame: theta, f, phi(climb), dist, rot
def res_global(x):
    theta, f, phi, dist, *r = x
    X, ok = ground_pts(theta, f)
    pr = project(X, cam_pos(dist, phi), R_cam(theta, np.array(r)), f)
    e = (pr - T[-1])
    e[~ok] = 0
    return e.ravel()


x0 = [np.radians(18), 1280, 0.0, -0.05, 0, 0, 0]
sol = least_squares(res_global, x0, loss="soft_l1", f_scale=0.5,
                    bounds=([np.radians(5), 900, -0.5, -0.5, -.05, -.05, -.05], [np.radians(60), 2200, 0.5, 0.5, .05, .05, .05]))
theta, f, phi = sol.x[:3]
r45 = np.abs(sol.fun.reshape(-1, 2)).max(1)
print(f"theta={np.degrees(theta):.2f}deg f={f:.1f}px ({f/W*36:.1f}mm eq) phi={np.degrees(phi):.2f}deg dist={sol.x[3]*H:.2f}m "
      f"median err={np.median(np.linalg.norm(sol.fun.reshape(-1,2),axis=1)):.3f}px")

# inliers only for the per-frame pass
X, ok = ground_pts(theta, f)
inl = ok & (np.linalg.norm(sol.fun.reshape(-1, 2), axis=1) < 1.5)
print("inliers", inl.sum())

# --- per-frame travel + rotation
D, RR, E = [0.0], [np.zeros(3)], [0.0]
for i in range(1, N):
    def res_i(x):
        pr = project(X[inl], cam_pos(x[0], phi), R_cam(theta, x[1:]), f)
        return (pr - T[i][inl]).ravel()
    s = least_squares(res_i, [D[-1], *RR[-1]], loss="soft_l1", f_scale=0.5)
    D.append(s.x[0]); RR.append(s.x[1:])
    E.append(np.median(np.linalg.norm(s.fun.reshape(-1, 2), axis=1)))
D, RR = np.array(D), np.array(RR)
t = np.arange(N)
Ds = np.polyval(np.polyfit(t, D, 3), t)
RRs = np.column_stack([np.polyval(np.polyfit(t, RR[:, k], 3), t) for k in range(3)])

# error of the smoothed camera
errs = []
for i in range(N):
    pr = project(X[inl], cam_pos(Ds[i], phi), R_cam(theta, RRs[i]), f)
    errs.append(np.median(np.linalg.norm(pr - T[i][inl], axis=1)))
print("per-frame raw median err max %.3f | smoothed median err mean %.3f max %.3f px" % (max(E), np.mean(errs), max(errs)))
print("travel m:", (Ds[[0, 11, 22, 33, 44]] * H).round(2))

flip = np.diag([1, -1, -1])  # OpenCV cam -> Blender cam axes
out = {"fps": [24000, 1001], "lens_mm": float(f / W * 36), "sensor_mm": 36.0, "altitude_m": H,
       "pitch_deg": float(np.degrees(theta)), "smoothed_err_px": [float(e) for e in errs], "frames": []}
for i in range(N):
    R = R_cam(theta, RRs[i]) @ flip
    C = cam_pos(Ds[i], phi) * H
    M = np.eye(4); M[:3, :3] = R; M[:3, 3] = C
    out["frames"].append(M.tolist())
json.dump(out, open(os.path.join(JOB, "camera.json"), "w"), indent=1)
print("wrote camera.json")
