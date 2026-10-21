"""Bird flight simulation shared by the Blender build and the auto-layout router.

Pure numpy (runs in system Python and in Blender's Python). A bird is a dict:
  depth       m from the camera at frame 1
  sx, sy      start screen offset from centre in px (+y up)
  speed       m/s
  hz          wingbeat frequency
  phase       starting beat phase (cycles)
  heading     mid-shot heading, deg: 0 = screen right, +90 = straight away from camera
  bank        deg, far wing raised (drone sees the back); also sets the turn rate
  span        wingspan m
  glides      [[t0, t1], ...] seconds; t0 <= 0 means "gliding from the start"
simulate() returns keys every KEY_STEP frames with world position, euler (XYZ) and wing pose.
"""
import math
import numpy as np

TOP, BOT, DOWN = 50.0, -28.0, 0.58  # arm elevation range (deg); downstroke = 58% of the beat
GLIDE = dict(elev=6.0, arm_sweep=6.0, hand_dih=-6.0, hand_sweep=12.0, twist=0.0)
SUB = 4
KEY_STEP = 0.5
G = 9.81


def smooth(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def elev(u):
    """Arm elevation through one beat: slow powered downstroke, quick recovery."""
    u %= 1.0
    if u < DOWN:
        return TOP + (BOT - TOP) * (1 - math.cos(math.pi * u / DOWN)) / 2
    return BOT + (TOP - BOT) * (1 - math.cos(math.pi * (u - DOWN) / (1 - DOWN))) / 2


def w_up(u):
    u %= 1.0
    return math.sin(math.pi * (u - DOWN) / (1 - DOWN)) if u >= DOWN else 0.0


def w_dn(u):
    u %= 1.0
    return math.sin(math.pi * u / DOWN) if u < DOWN else 0.0


def glide_w(t, windows, ramp=0.15):
    g = 0.0
    for a, b in windows:
        on = 1.0 if a <= 0 else smooth((t - a) / ramp)
        g = max(g, on * (1 - smooth((t - b) / ramp)))
    return g


def cam_basis(M1):
    """Horizontal right / forward vectors of the frame-1 camera (Blender camera: -Z forward)."""
    R = np.asarray(M1)[:3, :3]
    right = R @ np.array([1.0, 0, 0]); right[2] = 0; right /= np.linalg.norm(right)
    fwd = R @ np.array([0, 0, -1.0]); fwd[2] = 0; fwd /= np.linalg.norm(fwd)
    return right, fwd


def start_pos(bird, M1, f_px):
    d = bird["depth"]
    p_cam = np.array([bird["sx"] / f_px * d, bird["sy"] / f_px * d, -d, 1.0])
    return (np.asarray(M1) @ p_cam)[:3]


def simulate(bird, M1, f_px, fps, n_frames):
    right, fwd = cam_basis(M1)
    speed, span, bank = bird["speed"], bird["span"], bird["bank"]
    glides = bird.get("glides", [])
    t_shot = (n_frames - 1) / fps
    omega0 = G * math.tan(math.radians(bank)) / speed
    ang = math.radians(bird["heading"]) + omega0 * t_shot / 2  # mid-shot heading == requested
    pos = start_pos(bird, M1, f_px)
    phase, t, frame, next_key = bird.get("phase", 0.0), 0.0, 1.0, 1.0
    dt = 1 / (fps * SUB)
    seed = bird.get("phase", 0.0) * 6
    keys = []
    while frame <= n_frames + 1e-6:
        g = glide_w(t, glides)
        u = phase % 1.0
        roll = bank + 2.0 * math.sin(1.3 * t + seed)
        if frame >= next_key - 1e-6:
            fl = dict(elev=elev(u), arm_sweep=14 * w_up(u),
                      hand_dih=0.55 * (elev(u - 0.07) - elev(u)) - 4,
                      hand_sweep=40 * w_up(u), twist=-9 * w_dn(u))
            pose = {k: (1 - g) * fl[k] + g * GLIDE[k] for k in fl}
            lowness = (TOP - elev(u - 0.22)) / (TOP - BOT)  # body lifts as the wings come down
            lift = (1 - g) * 0.05 * span * (lowness - 0.5)
            dirv = right * math.cos(ang) + fwd * math.sin(ang)
            heading = math.atan2(dirv[1], dirv[0]) - math.pi / 2  # local +Y faces travel
            keys.append(dict(
                frame=next_key,
                pos=(pos + np.array([0, 0, lift])).tolist(),
                euler=[math.radians(-4 + 2.5 * (1 - g) * w_dn(u) - 1.5 * g), math.radians(roll), heading],
                wings=pose))
            next_key += KEY_STEP
        v = speed * ((1 - g) * (1 + 0.05 * w_dn(u)) + g * 0.97)
        dirv = right * math.cos(ang) + fwd * math.sin(ang)
        pos = pos + dirv * v * dt + np.array([0, 0, ((1 - g) * 0.25 - g * 0.7) * dt])
        ang -= G * math.tan(math.radians(roll)) / v * dt  # right wing low -> turn right
        phase += bird["hz"] * (1 - g) * dt
        t += dt
        frame += 1 / SUB
    return keys


def project(p, M, f_px, w, h):
    """World point -> pixel (x right, y down) for a Blender camera matrix. Returns (x, y, depth)."""
    Minv = np.linalg.inv(np.asarray(M))
    c = Minv @ np.array([*p, 1.0])
    z = -c[2]
    if z <= 0.05:
        return None
    return (f_px * c[0] / z + w / 2, h / 2 - f_px * c[1] / z, z)


# ---------------------------------------------------------------- flocks
def _wing_pose(u, g):
    fl = dict(elev=elev(u), arm_sweep=14 * w_up(u), hand_dih=0.55 * (elev(u - 0.07) - elev(u)) - 4,
              hand_sweep=40 * w_up(u), twist=-9 * w_dn(u))
    return {k: (1 - g) * fl[k] + g * GLIDE[k] for k in fl}


def _smooth_noise(rng, n_terms=3, f_lo=0.15, f_hi=0.6):
    terms = [(rng.uniform(f_lo, f_hi), rng.uniform(0, 2 * math.pi), rng.uniform(0.5, 1.0)) for _ in range(n_terms)]
    norm = sum(a for _, _, a in terms)
    return lambda t: sum(a * math.sin(2 * math.pi * f * t + p) for f, p, a in terms) / norm


def simulate_flock(flock, M1, f_px, fps, n_frames):
    """Loose flock around a leader path. Returns one key list per member (same format as simulate()).

    flock: {"leader": <bird dict>, "count": N, "seed": s, "spread": [lateral, along, vertical] m (half-sizes),
            "drift": m, "sep": m, "follow_glide": 0..1}
    Members hold a drifting slot in the leader's heading frame, trail along the leader's path with their
    own lag, get pushed apart (separation), and derive heading/bank/pitch from their own velocity so the
    flock ripples instead of moving as one rigid block. Each bird has its own wingbeat rate and phase.
    """
    import random
    rng = random.Random(flock.get("seed", 1))
    lead = flock["leader"]
    lw, la, lv = flock.get("spread", [7.0, 9.0, 2.0])
    drift, sep = flock.get("drift", 1.2), flock.get("sep", 1.6 * lead["span"])
    count = flock["count"]
    # simulate the leader over a padded window so lagged members have path to follow
    pad_s = 0.6
    pad_f = int(math.ceil(pad_s * fps))
    lead_keys = simulate(lead, M1, f_px, fps, n_frames + 2 * pad_f)
    # re-time so leader key frame (1 + pad_f) == shot frame 1 (leader starts earlier, off its start point)
    LP = np.array([k["pos"] for k in lead_keys])
    LH = np.array([k["euler"][2] for k in lead_keys])
    LT = (np.array([k["frame"] for k in lead_keys]) - 1) / fps - pad_s
    shift = LP[int(round(pad_f / KEY_STEP))] - LP[0]
    LP = LP - shift  # leader passes the routed start point at shot frame 1
    lead_glides = lead.get("glides", [])

    def at(t, arr):
        return np.array([np.interp(t, LT, arr[:, k]) for k in range(arr.shape[1])]) if arr.ndim == 2 else np.interp(t, LT, arr)

    members = []
    for i in range(count):
        # slot inside an ellipsoid, denser toward the middle
        while True:
            x, y, z = rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1)
            if x * x + y * y + z * z <= 1:
                break
        slot = np.array([x * lw, y * la, z * lv])
        if i == 0:
            slot = np.zeros(3)
        nz = [_smooth_noise(rng) for _ in range(3)]
        jit = rng.uniform(-0.15, 0.15)
        glides = [[a + jit, b + jit + rng.uniform(-0.1, 0.1)] for a, b in lead_glides] if rng.random() < flock.get("follow_glide", 0.75) else []
        if not lead_glides and rng.random() < 0.25:  # a few birds glide on their own
            a = rng.uniform(0.1, (n_frames - 1) / fps * 0.7)
            glides = [[a, a + rng.uniform(0.3, 0.7)]]
        members.append(dict(slot=slot, nz=nz, lag=rng.uniform(-0.25, 0.25), hz=lead["hz"] * rng.uniform(0.88, 1.12),
                            phase=rng.random(), glides=glides, span=lead["span"] * rng.uniform(0.92, 1.06),
                            bank0=lead["bank"] * rng.uniform(0.6, 1.3)))

    times = np.array([(1 + j * KEY_STEP - 1) / fps for j in range(int((n_frames - 1) / KEY_STEP) + 1)])
    pos = np.zeros((count, len(times), 3))
    for i, m in enumerate(members):
        for j, t in enumerate(times):
            tl = t + m["lag"]
            h = at(tl, LH) + math.pi / 2  # leader travel direction angle
            fwd = np.array([math.cos(h), math.sin(h), 0.0])
            side = np.array([math.sin(h), -math.cos(h), 0.0])
            o = m["slot"] + drift * np.array([m["nz"][0](t), m["nz"][1](t), 0.4 * m["nz"][2](t)])
            pos[i, j] = at(tl, LP) + side * o[0] + fwd * o[1] + np.array([0, 0, o[2]])
    # separation: push overlapping pairs apart, a few relaxation passes per key
    for j in range(len(times)):
        P = pos[:, j]
        for _ in range(6):
            d = P[:, None, :] - P[None, :, :]
            dist = np.linalg.norm(d, axis=2) + np.eye(count) * 1e9
            push = np.clip(sep - dist, 0, None) / sep
            P += 0.25 * sep * np.einsum("ij,ijk->ik", push, d / dist[..., None])
        pos[:, j] = P
    # light temporal smoothing so separation never jitters
    k = np.array([1, 2, 3, 2, 1], float); k /= k.sum()
    for i in range(count):
        for c in range(3):
            pos[i, :, c] = np.convolve(np.pad(pos[i, :, c], 2, mode="edge"), k, mode="valid")

    out = []
    dt = KEY_STEP / fps
    for i, m in enumerate(members):
        vel = np.gradient(pos[i], dt, axis=0)
        head = np.unwrap(np.arctan2(vel[:, 1], vel[:, 0]))
        omega = np.gradient(head, dt)
        vh = np.linalg.norm(vel[:, :2], axis=1)
        keys, phase, t_prev = [], m["phase"], 0.0
        for j, t in enumerate(times):
            g = glide_w(t, m["glides"])
            phase += m["hz"] * (1 - g) * (t - t_prev)
            t_prev = t
            u = phase % 1.0
            roll = m["bank0"] + math.degrees(math.atan(-vh[j] * omega[j] / G))  # coordinated: right turn -> right wing low
            roll = max(-35.0, min(35.0, roll))
            pitch = -4 + math.degrees(math.atan2(vel[j, 2], max(vh[j], 1e-3))) * 0.6 + 2.5 * (1 - g) * w_dn(u) - 1.5 * g
            lowness = (TOP - elev(u - 0.22)) / (TOP - BOT)
            lift = (1 - g) * 0.05 * m["span"] * (lowness - 0.5)
            keys.append(dict(frame=1 + j * KEY_STEP, pos=(pos[i, j] + np.array([0, 0, lift])).tolist(),
                             euler=[math.radians(pitch), math.radians(roll), float(head[j] - math.pi / 2)],
                             wings=_wing_pose(u, g), span=m["span"]))
        out.append(keys)
    return out
