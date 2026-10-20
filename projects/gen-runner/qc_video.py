"""Automatic video QC flags for gen-runner (Job Framework v2, phase 5).

NO_MOTION       median optical flow < NO_MOTION_PX px/frame (frames scaled to 320 px wide):
                the shot barely moves, or the subject doesn't (beach 01 surf, 07 car).
MORPH/DISSOLVE  ORB features matched between frames 6 apart stop fitting one homography:
                3-sample minimum of the RANSAC inlier ratio < MORPH_INLIER. A cross-fade or
                morph is two images blended, which no single camera move explains (beach 06).
Calibrated 20 Oct 2026 on the 7 beach Seedance clips + 2 face-test clips: failed clips
01 (0.01 motion), 07 (0.06), 06 (inlier 0.13 at 2.0 s) flagged; every passing clip
>= 0.20 motion and >= 0.61 inlier. WARN bands sit between the thresholds and those floors.
Flags are prompts to look, not verdicts — the contact sheet stays the final check.
"""
import cv2
import numpy as np

NO_MOTION_PX, NO_MOTION_WARN = 0.12, 0.18
MORPH_INLIER, MORPH_WARN = 0.35, 0.50
GAP = 6          # frames between ORB comparisons
STEP = 2         # compare every 2nd frame

_orb = cv2.ORB_create(1500)
_bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)


def _inlier(a, b):
    ka, da = _orb.detectAndCompute(a, None)
    kb, db = _orb.detectAndCompute(b, None)
    if da is None or db is None or len(ka) < 20 or len(kb) < 20:
        return 0.0
    m = _bf.match(da, db)
    if len(m) < 12:
        return 0.0
    pa = np.float32([ka[x.queryIdx].pt for x in m])
    pb = np.float32([kb[x.trainIdx].pt for x in m])
    _, mask = cv2.findHomography(pa, pb, cv2.RANSAC, 4.0)
    return float(mask.sum()) / len(m) if mask is not None else 0.0


def analyse(path, edit=False, allow=()):
    """edit=True: a cut, motion-graphics piece (talking head + slides). NO_MOTION is skipped (a locked-off
    talking head is meant to be still) and continuity dips inside `allow` windows [(a, b) s] — declared
    cuts and deliberate transitions — are ignored; a dip anywhere else is an accidental dissolve.
    Also flags FREEZE: >= 0.7 s of identical frames."""
    cap = cv2.VideoCapture(str(path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    big, small = [], []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        big.append(cv2.resize(g, (480, 480 * g.shape[0] // g.shape[1])))
        small.append(cv2.resize(g, (320, 320 * g.shape[0] // g.shape[1])))
    if len(small) < GAP + 4:
        return {"file": str(path), "error": "too few frames", "flags": ["UNREADABLE"]}
    diffs = [float(np.abs(a.astype(np.int16) - b).mean()) for a, b in zip(small, small[1:])]
    mags = [float(np.median(np.linalg.norm(cv2.calcOpticalFlowFarneback(a, b, None, 0.5, 3, 15, 3, 5, 1.2, 0), axis=2)))
            for a, b in zip(small, small[1:])]
    inl = np.array([_inlier(big[t - GAP], big[t]) for t in range(GAP, len(big), STEP)])
    sm = np.convolve(inl, np.ones(3) / 3, "valid")
    times = (GAP + STEP * np.arange(len(sm)) + STEP) / fps           # centre of each 3-sample window
    if edit:
        keep = np.array([not any(a - .1 <= t <= b + .1 for a, b in allow) for t in times])
        if keep.any():
            sm, times = sm[keep], times[keep]
        else:
            sm, times = np.array([1.0]), np.array([0.0])
    at = float(times[int(sm.argmin())]) * fps
    motion, morph = float(np.median(mags)), float(sm.min())
    flags = []
    run, longest = 0, 0
    for i, d in enumerate(diffs):                                      # FREEZE: identical frames in a row
        run = run + 1 if d < .15 else 0
        if edit and i == len(diffs) - 1:
            break                                                      # a run reaching the last frame = end-card hold
        longest = max(longest, run)
    if longest + 1 >= .7 * fps:
        flags.append(f"FREEZE {(longest + 1) / fps:.1f}s")
    if edit:
        pass
    elif motion < NO_MOTION_PX:
        flags.append("NO_MOTION")
    elif motion < NO_MOTION_WARN:
        flags.append("WARN_LOW_MOTION")
    dips = [round(float(t), 2) for v, t in zip(sm, times) if v < MORPH_INLIER]
    if edit:
        if dips:                                                       # slides swap content on purpose:
            flags.append(f"LOOK@{dips[0]:.1f}s")                       # report, don't fail
    elif morph < MORPH_INLIER:
        flags.append(f"MORPH/DISSOLVE@{at / fps:.1f}s")
    elif morph < MORPH_WARN:
        flags.append(f"WARN_MORPH@{at / fps:.1f}s")
    return {"file": str(path), "motion": round(motion, 3), "continuity_min": round(morph, 2),
            "continuity_at_s": round(at / fps, 2), "frames": len(small), "flags": flags,
            "dips_s": dips[:20]}
